"""Offline stand-ins for the two external services: a stub PizzaSim API
and a stub LLM gateway (a scripted model in the golden-transcript spirit).
Both run as real HTTP servers so the app under test is exercised through
its production code paths — no network beyond localhost, no LLM."""
from __future__ import annotations

import json
import threading
import time
import uuid
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

FIXTURES = Path(__file__).parent / "fixtures"
MENU = json.loads((FIXTURES / "menu.json").read_text())


class StubPizzaSim:
    def __init__(self):
        self.pizzerias = [
            {"id": "11111111-aaaa-bbbb-cccc-000000000001",
             "name": "Stub Pizzeria Uno"},
            {"id": "22222222-aaaa-bbbb-cccc-000000000002",
             "name": "Stub Pizzeria Due"},
        ]
        self.orders: dict[str, list[dict]] = {}
        self.fail_pizzerias = False
        self.app = app = FastAPI()

        @app.get("/menu")
        def menu():
            return MENU

        @app.get("/pizzerias")
        def pizzerias():
            if self.fail_pizzerias:
                return JSONResponse({"error": "boom"}, status_code=500)
            return {"pizzerias": self.pizzerias}

        @app.get("/pizzerias/{pid}/orders")
        def list_orders(pid: str):
            listed = [{k: o[k] for k in
                       ("id", "created_at", "ready_at", "status")}
                      | {"first_name": o["customer"]["first_name"],
                         "customer_id": o["customer_id"]}
                      for o in self.orders.get(pid, [])]
            return {"orders": list(reversed(listed))}

        @app.post("/pizzerias/{pid}/orders")
        async def create_order(pid: str, request: Request):
            body = await request.json()
            now = int(time.time())
            order = {
                "id": str(uuid.uuid4()),
                "customer_id": str(uuid.uuid4()),
                "customer": body["customer"],
                "items": body["items"],
                "created_at": now,
                "ready_at": now + 120,
                "status": "ordered",
            }
            self.orders.setdefault(pid, []).append(order)
            return {"order_id": order["id"], "status": "ordered",
                    "eta_seconds": 120}

        @app.get("/pizzerias/{pid}/orders/{oid}")
        def order_detail(pid: str, oid: str):
            for order in self.orders.get(pid, []):
                if order["id"] == oid:
                    return {k: order[k] for k in
                            ("id", "customer", "items", "created_at",
                             "ready_at", "status")}
            return JSONResponse({"error": "not_found"}, status_code=404)

        @app.get("/location")
        def location(street: str = ""):
            return {"street": street, "deliverable": True}


def _tool_call(name: str, args: dict) -> dict:
    return {"tool_calls": [{
        "id": f"stub-{name}-{uuid.uuid4().hex[:6]}",
        "type": "function",
        "function": {"name": name, "arguments": json.dumps(args)},
    }]}


class StubGateway:
    """A scripted, deterministic model. mode: 'ok' plays a fixed order
    script; 'http500' simulates the gateway being unreachable; 'empty'
    returns an empty final message (stream ends without an answer)."""

    def __init__(self):
        self.mode = "ok"
        self.saw_spoken_note = False
        self.app = app = FastAPI()

        @app.post("/chat/completions")
        async def chat(request: Request):
            if self.mode == "http500":
                return JSONResponse({"error": "boom"}, status_code=500)
            body = await request.json()
            if any(m.get("role") == "system"
                   and "vorgelesen" in (m.get("content") or "")
                   for m in body["messages"]):
                self.saw_spoken_note = True
            if self.mode == "empty":
                return _reply({"content": ""})
            return _reply(self._script(body["messages"]))


def _reply(message: dict) -> dict:
    return {"choices": [{"message": message}]}


def _tiny_wav() -> bytes:
    import io
    import wave
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(8000)
        w.writeframes(b"\x00\x00" * 800)  # 0.1s silence
    return buf.getvalue()


class StubSpeech:
    """OpenAI-compatible speech stub: fixed transcript, tiny TTS audio,
    switchable failure mode. Asserts wiring, not speech quality."""

    def __init__(self):
        self.transcript = "Zwei Margherita bitte"
        self.languages: list[str] = []
        self.tts_calls = 0
        self.tts_requests: list[tuple[str, str]] = []  # (model, voice)
        self.mode = "ok"  # "fail" → 502 on both endpoints
        self.app = app = FastAPI()

        @app.get("/v1/models")
        def models():
            return {"data": []}

        @app.post("/v1/audio/transcriptions")
        async def stt(request: Request):
            if self.mode == "fail":
                return JSONResponse({"error": "down"}, status_code=502)
            form = await request.form()
            self.languages.append(str(form.get("language", "")))
            return {"text": self.transcript}

        @app.post("/v1/audio/speech")
        async def tts(request: Request):
            if self.mode == "fail":
                return JSONResponse({"error": "down"}, status_code=502)
            self.tts_calls += 1
            body = await request.json()
            self.tts_requests.append(
                (str(body.get("model", "")), str(body.get("voice", ""))))
            from fastapi.responses import Response
            return Response(_tiny_wav(), media_type="audio/wav")


def _last_tool(messages: list[dict]) -> tuple[str, dict] | None:
    # Skip trailing system messages: spoken turns append the ephemeral
    # spoken-style note after the conversation tail.
    last = next((m for m in reversed(messages)
                 if m.get("role") != "system"), None)
    if not last or last.get("role") != "tool":
        return None
    call_id = last.get("tool_call_id")
    for msg in reversed(messages):
        for call in (msg.get("tool_calls") or []):
            if call["id"] == call_id:
                return call["function"]["name"], json.loads(last["content"])
    return None


def _script_impl(messages: list[dict]) -> dict:
    tool = _last_tool(messages)
    if tool:
        name, result = tool
        if "error" in result:
            return {"content": "Das habe ich leider nicht im Angebot — "
                               "vielleicht Pasta Funghi?"}
        if name == "get_menu":
            price = next(p["price"] for p in result["menu"]["pizzas"]
                         if p["code"] == "margherita")
            return {"content": f"Eine Margherita kostet {price} €."}
        if name == "add_items":
            return {"content": "Gern. Wie ist Ihr Vorname?"}
        if name == "set_customer":
            return _tool_call("read_back", {})
        if name == "read_back":
            return {"content": "Ich lese vor — bitte bestätigen Sie die "
                               "Bestellung."}
        if name == "submit_order":
            return {"content": "Bestellt! Ihre Nummer ist "
                               f"{result['order_id']}."}
        if name == "confirm_order":
            return _tool_call("submit_order", {})
        return {"content": "Alles klar."}

    users = [m for m in messages if m.get("role") == "user"]
    if not users:
        return {"content": "Willkommen! Was darf es sein?"}
    text = users[-1]["content"].lower()
    if "ja, bestellen" in text or "yes, order" in text:
        # explicit yes after a read_back: the model confirms the revision
        # it read back (extracted from the tool history, like a real model)
        for m in reversed(messages):
            if m.get("role") == "tool":
                try:
                    content = json.loads(m["content"])
                except (ValueError, TypeError):
                    continue
                revision = (content.get("snapshot") or {}).get("revision")
                if isinstance(revision, int):
                    return _tool_call("confirm_order", {"revision": revision})
        return {"content": "Ich habe noch nichts vorgelesen."}
    if "kostet" in text or "cost" in text:
        return _tool_call("get_menu", {})
    if "bolognese" in text:
        return _tool_call("add_items", {"items": [
            {"type": "pasta", "code": "bolognese", "qty": 1}]})
    if "margherita" in text:
        return _tool_call("add_items", {"items": [
            {"type": "pizza", "code": "margherita", "qty": 2}]})
    if "heiße" in text or "name is" in text:
        return _tool_call("set_customer", {"first_name": "Eva"})
    return {"content": "Was darf es sein?"}


StubGateway._script = staticmethod(_script_impl)


def run_server(app: FastAPI) -> tuple[uvicorn.Server, str]:
    config = uvicorn.Config(app, host="127.0.0.1", port=0,
                            log_level="warning")
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    for _ in range(200):
        if server.started:
            break
        time.sleep(0.025)
    else:
        raise RuntimeError("stub server did not start")
    port = server.servers[0].sockets[0].getsockname()[1]
    return server, f"http://127.0.0.1:{port}"
