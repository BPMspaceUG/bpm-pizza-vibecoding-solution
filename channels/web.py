"""FastAPI web channel on port 8888. Same core, zero order logic here.

Streams the agent's intermediate steps as newline-delimited JSON and
proxies the optional self-hosted speech service (STT/TTS). If SPEECH_URL is
unset or the service doesn't answer at startup, speech endpoints return 404
and the UI renders text-only.

Run:  python -m channels.web
"""
from __future__ import annotations

import json
import queue
import sys
import threading
from pathlib import Path

import httpx
import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse, Response, StreamingResponse
from fastapi.staticfiles import StaticFiles

from core.agent import Agent, AgentConfig, Session, startup
from core.menu import Menu
from core.pizzasim import ConfigError, PizzaSimError, optional_env

STATIC = Path(__file__).resolve().parent / "static"
app = FastAPI(title="PizzaSim ordering agent")


class Speech:
    """Config + probe for the self-hosted speech container. All-or-nothing:
    enabled only if SPEECH_URL is set, answers, and models are configured."""

    def __init__(self):
        self.url = optional_env("SPEECH_URL")
        self.stt_model = optional_env("SPEECH_STT_MODEL")
        self.tts_model = optional_env("SPEECH_TTS_MODEL")
        self.voice = optional_env("SPEECH_TTS_VOICE")
        self.enabled = False
        if self.url and self.stt_model and self.tts_model and self.voice:
            try:
                httpx.get(f"{self.url.rstrip('/')}/v1/models",
                          timeout=3.0).raise_for_status()
                self.enabled = True
            except httpx.HTTPError:
                print("speech service not answering — text-only mode",
                      file=sys.stderr)


@app.on_event("startup")
def boot() -> None:
    try:
        config = AgentConfig.from_env()
        client, pizzeria_name, _menu = startup(config)
    except (ConfigError, ValueError) as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        raise SystemExit(1)
    except PizzaSimError as exc:
        print(f"Startup check against PizzaSim failed: {exc}\n"
              "We're not taking orders right now.", file=sys.stderr)
        raise SystemExit(1)
    app.state.config = config
    app.state.client = client
    app.state.pizzeria_name = pizzeria_name
    app.state.agent = Agent(config, client)
    app.state.sessions = {}
    app.state.locks = {}  # one Lock per session: turns are serialized
    app.state.speech = Speech()


@app.get("/")
def index():
    return FileResponse(STATIC / "index.html")


@app.get("/config")
def ui_config():
    return {"speech": app.state.speech.enabled}  # fixed contract, per plan


def _get_session(session_id: str) -> Session:
    sessions = app.state.sessions
    if session_id not in sessions:
        # Fresh immutable menu snapshot per session (SPEC invariant 5).
        try:
            menu = Menu(app.state.client.get_menu())
        except PizzaSimError:
            raise HTTPException(503, "We're not taking orders right now.")
        sessions[session_id] = Session.create(
            app.state.config, menu, app.state.pizzeria_name)
    return sessions[session_id]


@app.post("/chat")
async def chat(body: dict):
    session_id = str(body.get("session_id") or "")
    if not session_id:
        raise HTTPException(422, "session_id required")
    text = body.get("text")  # None → opening turn, agent greets
    if text is not None and not str(text).strip():
        raise HTTPException(422, "text must not be empty")
    session = _get_session(session_id)
    lock = app.state.locks.setdefault(session_id, threading.Lock())
    if not lock.acquire(blocking=False):
        # One Order per conversation means one turn at a time: overlapping
        # requests would interleave mutations and break the revision-bound
        # confirmation guarantees.
        raise HTTPException(409, "a turn is already in progress")

    events: queue.Queue = queue.Queue()

    def run() -> None:
        try:
            app.state.agent.run_turn(session, text, events.put)
        finally:
            events.put({"type": "done",
                        "state": session.order.snapshot()})
            events.put(None)
            lock.release()

    threading.Thread(target=run, daemon=True).start()

    def ndjson():
        while (event := events.get()) is not None:
            yield json.dumps(event, ensure_ascii=False) + "\n"

    return StreamingResponse(ndjson(), media_type="application/x-ndjson")


def _speech() -> Speech:
    speech = app.state.speech
    if not speech.enabled:
        raise HTTPException(404, "speech is not available")
    return speech


@app.post("/speech/stt")
async def stt(audio: UploadFile):
    speech = _speech()
    files = {"file": (audio.filename or "audio.webm", await audio.read(),
                      audio.content_type or "audio/webm")}
    data = {"model": speech.stt_model,
            "language": app.state.config.lang}  # STT hint only
    try:
        response = httpx.post(
            f"{speech.url.rstrip('/')}/v1/audio/transcriptions",
            files=files, data=data, timeout=60.0)
        response.raise_for_status()
    except httpx.HTTPError:
        raise HTTPException(502, "speech service unavailable")
    return {"text": response.json().get("text", "")}


@app.post("/speech/tts")
async def tts(body: dict):
    speech = _speech()
    text = str(body.get("text") or "")
    if not text:
        raise HTTPException(422, "text required")
    try:
        response = httpx.post(
            f"{speech.url.rstrip('/')}/v1/audio/speech",
            json={"model": speech.tts_model, "voice": speech.voice,
                  "input": text},
            timeout=60.0)
        response.raise_for_status()
    except httpx.HTTPError:
        raise HTTPException(502, "speech service unavailable")
    return Response(response.content,
                    media_type=response.headers.get("content-type",
                                                    "audio/mpeg"))


app.mount("/static", StaticFiles(directory=STATIC), name="static")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8888)
