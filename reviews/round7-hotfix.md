OpenAI Codex v0.143.0
--------
workdir: /home/rob/bpm-pizza-vibecoding-solution
model: gpt-5.4
provider: openai
approval: never
sandbox: read-only
reasoning effort: medium
reasoning summaries: none
session id: 019fbbfc-e3c5-7330-8e4f-ec9044da3cf0
--------
user
You are an independent reviewer for the repository in the current working directory. Read-only; you never write code. Devil's advocate + judge in one pass.

Context: The implementation was APPROVED 24/25 in reviews/round6-impl.md. After approval, a production defect surfaced: the web UI, served over plain HTTP on a public IP (not localhost), was completely dead in the browser — crypto.randomUUID() requires a secure context, so app.js crashed at load: no greeting, no working send button. The operator also required the pizzeria display name to be visible to the end user.

Task: Review the hotfix commit HEAD (0580866, "Hotfix: end-user browser path over plain HTTP") — run `git show HEAD` or read the changed files: channels/static/app.js (session id fallback via crypto.getRandomValues; mic additionally gated on navigator.mediaDevices; title set from /config), channels/web.py (/config returns {speech, pizzeria}), PLAN.md (contract line updated). Judge: (a) does the fix actually solve the insecure-context failure, (b) does it introduce new problems (security, contract drift, spec violations), (c) is anything else in the static UI still secure-context-dependent that would break the same way?

Output MUST end with exactly this block:
SCORES (1-5 each, 5 = best):
completeness: N
correctness: N
error_handling: N
simplicity: N
spec_compliance: N
TOTAL: N/25
VERDICT: APPROVED | CHANGES_REQUIRED
ISSUES: (max 5 bullets, concrete and actionable, empty if approved)

APPROVED requires TOTAL >= 20 and no dimension below 4.

codex
Using `using-superpowers` first, then I’ll inspect the hotfix diff and the affected files to judge the fix against the reported production failure and the UI contract.
exec
/bin/bash -lc "sed -n '1,240p' channels/web.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,220p' PLAN.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "git show --stat --oneline HEAD && printf '\\n---DIFF---\\n' && git show --format=medium --no-ext-diff --patch HEAD -- channels/static/app.js channels/web.py PLAN.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,220p' /home/rob/.agents/skills/using-superpowers/SKILL.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' channels/static/app.js" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 574ms:
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
    # Contract per plan: speech flag + pizzeria display name. The customer
    # must see which pizzeria they are ordering at.
    return {"speech": app.state.speech.enabled,
            "pizzeria": app.state.pizzeria_name}


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

 succeeded in 597ms:
# PizzaSim Ordering Agent — Implementation Plan

> Written before any code, per SPEC.md stage 1. Updated as implementation
> proceeds. Contains design and tickets only — no code.

**Goal:** A two-channel (CLI + web) pizza-ordering agent where the order is a
state machine owned by the code and the model only converts speech/text into
tool calls.

**Architecture:** One Python core (`core/`) holds the order state machine, menu
validation, PizzaSim client, tool dispatch and the model loop. Channels
(`channels/cli.py`, `channels/web.py`) are transports only: words in, words
out, zero order logic. Speech is an optional proxy on the web channel to a
self-hosted OpenAI-compatible speech service.

**Tech stack:** Python 3.13, `httpx` (all HTTP, with timeouts), `fastapi` +
`uvicorn` (web channel), `pytest` (tests), stdlib `difflib` (candidate
matching), stdlib `json`/`dataclasses`/`enum`. No other dependencies.

## Global constraints (from SPEC.md, binding for every ticket)

- Nothing hardcoded: no UUID, no model name, no menu, no base URL, no
  fallbacks. All config from environment; `~/.env` loaded if present, never
  written, never printed.
- Missing/empty required env var → exit before the first turn, naming the
  variable and the file it was expected in.
- Secrets never appear in logs, transcripts, errors, or the web UI.
- No regex/keyword parser that produces an order without the model (hard ban).
- No `subprocess` + `curl` — `httpx` only, explicit timeouts everywhere.
- No browser speech APIs (`SpeechRecognition`, `speechSynthesis`).
- No build-time model name anywhere in source, config, prompts, tests, docs.
- `submit_order` is the only network write; legal only in `CONFIRMED`.
- Item codes are unique per type, not globally (`tonno` is a pizza and a
  pasta) — every validation and removal keys on `(type, code)`.
- Deterministic tests: no network, no LLM (one opt-in live smoke test).
- German + English, mirrored per turn.

## File layout

```
core/
  order.py     Order dataclass: items, customer, revision, state field,
               read-back tracking, submit bookkeeping. Pure data + snapshots.
  state.py     OrderState enum + transition functions. Every mutation goes
               through here; illegal transitions raise TransitionError.
  menu.py      Immutable Menu snapshot (pizzas, pasta, toppings), one per
               session; (type, code) validation; extras validation;
               candidate suggestions via difflib over codes and names.
  pizzasim.py  httpx client for PizzaSim: get_menu, list_orders,
               submit_order, check_street; typed errors; timeouts;
               startup pizzeria check.
  tools.py     The eight tool JSON schemas + dispatch(tool_name, args) →
               result dict. Success = full state snapshot; failure =
               {"error": {code, message, candidates}}.
  agent.py     Config loading for gateway vars, prompt assembly, the model
               loop (chat completions + tool calls until a plain assistant
               message), gateway retry policy, JSONL event logging.
channels/
  cli.py       Terminal REPL over the core. Prints assistant text; --verbose
               shows tool events.
  web.py       FastAPI on port 8888. Serves static/, POST /chat streaming
               NDJSON events, speech proxy endpoints, /config for UI
               feature flags. In-memory session dict.
  static/      index.html, app.js, style.css — chat UI, NDJSON consumer,
               push-to-talk recorder (MediaRecorder → upload), TTS toggle.
prompts/
  system.de.md German system prompt (default deployment language).
  system.en.md English system prompt, same policy.
tests/
  fixtures/    Recorded real API responses (menu, order created, orders
               list, 422 bodies, location).
  test_state.py       State machine, exhaustive incl. every illegal move.
  test_tools.py       Tool dispatch against fixture-backed fakes.
  test_transcripts.py Runner for the five golden transcripts.
  transcripts/        Five scripted conversations as JSON.
reviews/       One file per review round + scores.md.
.env.example   Names only.
README.md      How to run CLI, web, speech; how to test.
requirements.txt  Pinned: fastapi, uvicorn, httpx, pytest, python-multipart.
```

Deviation from the SPEC tree, documented: `tests/test_transcripts.py` and
`requirements.txt` are added (the transcripts need a runner; the deps need
pinning). Everything listed in SPEC.md exists exactly where listed.

## Configuration

Each module owns its own env vars and exposes `from_env()`:

| Module | Vars |
|---|---|
| `core/agent.py` | `LITELLM_PIZZA_URL`, `LITELLM_PIZZA_KEY`, `LITELLM_PIZZA_MODEL_1`, `PIZZERIA_LANG` (all required; `LITELLM_PIZZA_MODEL_2` read but unused — single-model build) |
| `core/pizzasim.py` | `PIZZASIM_URL`, `PIZZASIM_API_KEY`, `PIZZERIA_ID` (required) |
| `channels/web.py` | `SPEECH_URL`, `SPEECH_STT_MODEL`, `SPEECH_TTS_MODEL`, `SPEECH_TTS_VOICE` (all optional; absence disables speech) |

`PIZZERIA_LANG` ∈ {`de`, `en`} is the pizzeria-country greeting language.
The live API exposes no country field (verified), so per the config-from-env
rule this deployment fact is a **required** env var — no default, missing →
startup failure like any other required var (oracle decision,
`decisions/qa.md`). It selects the system prompt file and the STT language
hint; it never overrides per-turn language mirroring.

Loading order: process env wins; else `~/.env` if present (parsed key=value,
never written, never printed). No other sources. A missing required var
raises `ConfigError("LITELLM_PIZZA_URL is not set (expected in the
environment or ~/.env)")` and the channel exits before the first turn.
Logs go to `./logs/` (fixed path, gitignored) — not configurable.

Startup sequence, identical for both channels, all before the first turn:

1. Load and validate all required env vars (exit naming var + file).
2. `GET /pizzerias` with `X-API-Key` — a 401/403 aborts startup ("cannot
   reach the kitchen system"); `PIZZERIA_ID` not in the returned list is the
   404-pizzeria case from the error table → process refuses to start;
   otherwise capture `pizzeria_name` for the system prompt.
3. `GET /menu` — failure aborts startup with "We're not taking orders right
   now".

**Session model.** A session (conversation) = one `Order` + one immutable
`Menu` snapshot + one message history, bundled in a `Session` object owned
by the channel. The CLI process is exactly one session and reuses the
startup menu fetch as its snapshot. The web channel creates a `Session` per
`session_id`, fetching a **fresh menu snapshot at session creation**; that
snapshot is immutable for the session's lifetime (spec invariant 5: "menu
snapshot fetched this session"). A failed session-creation fetch yields the
"We're not taking orders right now" message for that session only.

## Order state machine

States: `EMPTY`, `COLLECTING`, `READY`, `CONFIRMED`, `SUBMITTED`.

Order fields: `items: list[Item(type, code, qty, extras)]`,
`customer: Customer(first_name, street_one) | None`, `revision: int`
(increments on every basket or customer mutation), `read_back_revision:
int | None` (set by `read_back`), `state`, `submit_attempted_at: int | None`
(unix seconds captured immediately **before** the first submit POST — the
correlation key for timeout recovery), `submit_unknown: bool` (that attempt
timed out / 5xx'd and is unverified), `result` (order_id, status,
eta_seconds after submit).

Derived-state rule after any legal mutation: `SUBMITTED` is terminal and
`CONFIRMED` is only ever entered by `confirm_order`; otherwise state is
recomputed as `EMPTY` (no items), `COLLECTING` (items, no customer), `READY`
(items + customer). A mutation while `CONFIRMED` succeeds and demotes to the
recomputed state (invariant 2). `set_customer` before any item is legal
(customer stored, state stays `EMPTY`) — the diagram's path is the common
case, not an ordering constraint.

Transition table (✓ legal, ✗ → typed error):

| Tool | EMPTY | COLLECTING | READY | CONFIRMED | SUBMITTED |
|---|---|---|---|---|---|
| add_items | ✓ | ✓ | ✓ | ✓ demote | ✗ order_closed |
| remove_item | ✗ empty_basket | ✓ | ✓ | ✓ demote | ✗ order_closed |
| set_customer | ✓ | ✓ | ✓ | ✓ demote | ✗ order_closed |
| read_back | ✗ empty_basket | ✗ invalid_state (no customer yet) | ✓ | ✓ (same basket, idempotent) | ✗ order_closed |
| confirm_order | ✗ invalid_state | ✗ invalid_state | ✓ | ✗ invalid_state (already confirmed) | ✗ order_closed |
| submit_order | ✗ invalid_state | ✗ invalid_state | ✗ invalid_state | ✓ | ✗ order_closed |
| get_menu / check_street | ✓ any state, read-only | | | | |

`confirm_order(revision)` additionally requires `revision == order.revision`
(else `stale_revision`) and `read_back_revision == order.revision` (else
`read_back_required`). So the only path into `CONFIRMED` is: state `READY`,
`read_back` called at the current revision, then `confirm_order` naming that
same revision — exactly the spec's path, nothing broader. Every ✗ cell gets
a unit test (invariants 1–5).

Submit-timeout path: `submit_order` sets `submit_attempted_at = now()`
before its first POST. On httpx timeout or 5xx, the order stays `CONFIRMED`
with `submit_unknown = True`. The next `submit_order` call sees
`submit_unknown` and first calls `list_orders()`, shortlisting orders with
our customer's `first_name` and `created_at >= submit_attempted_at - 60`
(60s clock-skew allowance); the best candidate is then **verified via the
detail endpoint** (`GET /pizzerias/{id}/orders/{order_id}`, which carries
items) — adopted only if its items equal the basket exactly. Verified →
state `SUBMITTED` with the recovered id. Absent or different items →
exactly one real retry. List or detail call fails → error `submit_unknown`
with an honest message ("I'm not sure that went through — let me check"
phrasing); never a blind re-POST. Any basket/customer mutation clears
`submit_unknown` and `submit_attempted_at`: the correlation belongs to the
basket that was confirmed then, and a demoted order must POST fresh.

## Tool schemas

All eight tools, OpenAI function-calling format.

`SNAPSHOT` (one fixed shape, embedded in **every** success result — this is
how the per-tool return table and the "full current state" rule compose):
`{state, revision, items: [{type, code, name, qty, extras}], customer:
{first_name, street_one} | null, read_back_done: bool}` — never a diff.

| Tool | Parameters (JSON schema) | Success result — exact JSON |
|---|---|---|
| `get_menu` | `{}` | `{"menu": {"pizzas": [{code, name}], "pasta": [{code, name}], "toppings": [str]}, "snapshot": SNAPSHOT}` — `name` is the API's single display name, which the verified contract facts show serves both languages |
| `add_items` | `{items: [{type: enum[pizza,pasta], code: str, qty: int ≥1, extras: [str]}]}` (required: items; extras default `[]`) | `{"snapshot": SNAPSHOT}` (basket + revision live in SNAPSHOT) |
| `remove_item` | `{type: enum, code: str, qty: int ≥1 optional}` — the spec fixes these params, so when several lines share (type, code) with different extras: absent qty removes **all** matching lines, qty reduces the **most recently added** matching line (deterministic; the snapshot lets the model repair by remove + re-add) | `{"snapshot": SNAPSHOT}` |
| `set_customer` | `{first_name: str minLength 1, street_one: str optional}` | `{"customer": {first_name, street_one}, "snapshot": SNAPSHOT}` — customer as stored |
| `read_back` | `{}` | `{"snapshot": SNAPSHOT}` — basket, customer, revision: the material the agent reads out |
| `confirm_order` | `{revision: int}` | `{"snapshot": SNAPSHOT}` with `state == "CONFIRMED"`, or error if stale |
| `submit_order` | `{}` | `{"order_id": str, "status": str, "eta_seconds": int, "snapshot": SNAPSHOT}` — the minutes conversion is the model's job, instructed by the prompt |
| `check_street` | `{street: str}` | `{"street": str, "deliverable": bool, "snapshot": SNAPSHOT}` — the never-claim-verified rule lives in the prompt, not the tool |

Failure shape: `{"error": {"code": "<one of the codes below>", "message":
"<speakable sentence>", "candidates": [up to 3 of {type, code, name}]}}`.

Error codes: `unknown_item` (with candidates), `invalid_extra` (with
candidate toppings), `invalid_quantity` (non-integer or < 1 — the tool does
not parse "zwei"), `empty_basket`, `invalid_state`, `stale_revision`,
`read_back_required`, `order_closed`, `submit_failed`, `submit_unknown`,
`api_unavailable`, `not_in_basket` (remove_item for a line that isn't there).

Validation order in `add_items`: every item's `(type, code)` against the menu
snapshot and every extra against `toppings[]`; any failure rejects the whole
call atomically (no partial adds), returning the first error with candidates
from `difflib.get_close_matches` over codes and lowercased names of the same
type (falling back to the other type's matches so "pasta tonno" asked as
pizza still gets a useful suggestion).

## Agent loop (`core/agent.py`)


 succeeded in 598ms:
0580866 Hotfix: end-user browser path over plain HTTP
 PLAN.md                | 10 ++++++----
 channels/static/app.js | 14 ++++++++++++--
 channels/web.py        |  5 ++++-
 3 files changed, 22 insertions(+), 7 deletions(-)

---DIFF---
commit 05808661a4b886a703b3ab55e76c786d4de84e10
Author: Robert Kuhlig <16413104+Kuhlig@users.noreply.github.com>
Date:   Sat Aug 1 08:21:37 2026 +0200

    Hotfix: end-user browser path over plain HTTP
    
    - crypto.randomUUID needs a secure context; fall back to getRandomValues
      so the UI works on http://<host>:8888 (the bug: app.js died at load,
      no greeting, dead send button)
    - /config carries the pizzeria display name again; UI shows it (PLAN.md
      contract updated accordingly)
    - mic additionally gated on navigator.mediaDevices (absent in insecure
      contexts)
    
    Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>

diff --git a/PLAN.md b/PLAN.md
index 497431f..cbb8d75 100644
--- a/PLAN.md
+++ b/PLAN.md
@@ -257,10 +257,12 @@ an invitation.
 
 ## Web channel protocol
 
-- `GET /` → static UI. `GET /config` → `{speech: bool}` (true only if
-  `SPEECH_URL` set and a probe succeeded at startup). No language field:
-  language is never a UI control — the greeting comes from `PIZZERIA_LANG`,
-  mirroring is model behaviour.
+- `GET /` → static UI. `GET /config` → `{speech: bool, pizzeria: str}`
+  (`speech` true only if `SPEECH_URL` set and a probe succeeded at startup;
+  `pizzeria` is the display name from startup step 2 — the customer must
+  see which pizzeria they are ordering at). No language field: language is
+  never a UI control — the greeting comes from `PIZZERIA_LANG`, mirroring
+  is model behaviour.
 - `POST /chat` body `{session_id, text}` → `application/x-ndjson` stream of
   the agent-loop events, ending with `{"type": "done", "state": ...}`.
   Turns are serialized per session (one `Order` per conversation = one turn
diff --git a/channels/static/app.js b/channels/static/app.js
index d5c9de7..27d979a 100644
--- a/channels/static/app.js
+++ b/channels/static/app.js
@@ -10,7 +10,12 @@ const mic = document.getElementById("mic");
 const ttsWrap = document.getElementById("tts-wrap");
 const ttsToggle = document.getElementById("tts-toggle");
 
-const sessionId = crypto.randomUUID();
+// crypto.randomUUID needs a secure context (HTTPS/localhost); the demo may
+// be served over plain HTTP, so fall back to getRandomValues.
+const sessionId = crypto.randomUUID
+  ? crypto.randomUUID()
+  : Array.from(crypto.getRandomValues(new Uint8Array(16)),
+               (b) => b.toString(16).padStart(2, "0")).join("");
 let speechEnabled = false;
 
 function add(cls, text) {
@@ -147,7 +152,12 @@ async function speak(text) {
 (async () => {
   try {
     const cfg = await (await fetch("/config")).json();
-    speechEnabled = cfg.speech;
+    if (cfg.pizzeria) {
+      document.getElementById("title").textContent = cfg.pizzeria;
+      document.title = cfg.pizzeria;
+    }
+    // Mic needs getUserMedia, which insecure contexts don't provide.
+    speechEnabled = cfg.speech && !!navigator.mediaDevices;
     if (speechEnabled) {           // unset SPEECH_URL → not rendered at all
       mic.hidden = false;
       ttsWrap.hidden = false;
diff --git a/channels/web.py b/channels/web.py
index b44ac86..f6e6fd2 100644
--- a/channels/web.py
+++ b/channels/web.py
@@ -77,7 +77,10 @@ def index():
 
 @app.get("/config")
 def ui_config():
-    return {"speech": app.state.speech.enabled}  # fixed contract, per plan
+    # Contract per plan: speech flag + pizzeria display name. The customer
+    # must see which pizzeria they are ordering at.
+    return {"speech": app.state.speech.enabled,
+            "pizzeria": app.state.pizzeria_name}
 
 
 def _get_session(session_id: str) -> Session:

 succeeded in 608ms:
---
name: using-superpowers
description: Use when starting any conversation - establishes how to find and use skills, requiring skill invocation before ANY response including clarifying questions
---

<SUBAGENT-STOP>
If you were dispatched as a subagent to execute a specific task, ignore this skill.
</SUBAGENT-STOP>

<EXTREMELY-IMPORTANT>
If you think there is even a 1% chance a skill might apply to what you are doing, you ABSOLUTELY MUST invoke the skill.

IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT.

This is not negotiable. You cannot rationalize your way out of this.
</EXTREMELY-IMPORTANT>

## The Rule

**Invoke relevant or requested skills BEFORE any response or action** — including clarifying questions, exploring the codebase, or checking files. If it turns out wrong for the situation, you don't have to use it.

**Before entering plan mode:** if you haven't already brainstormed, invoke the brainstorming skill first.

Then announce "Using [skill] to [purpose]" and follow the skill exactly. If it has a checklist, create a todo per item.

## Skill Priority

When multiple skills apply, process skills come first — they set the approach, then implementation skills (frontend-design, etc.) carry it out. Brainstorming and systematic-debugging are Superpowers' most common process skills, but the rule holds for any of them.

- "Let's build X" → superpowers:brainstorming first, then implementation skills.
- "Fix this bug" → superpowers:systematic-debugging first, then domain skills.

## Red Flags

These thoughts mean STOP—you're rationalizing:

| Thought | Reality |
|---------|---------|
| "This is just a simple question" | Questions are tasks. Check for skills. |
| "I need more context first" | Skill check comes BEFORE clarifying questions. |
| "Let me explore the codebase first" | Skills tell you HOW to explore. Check first. |
| "I can check git/files quickly" | Files lack conversation context. Check for skills. |
| "Let me gather information first" | Skills tell you HOW to gather information. |
| "This doesn't need a formal skill" | If a skill exists, use it. |
| "I remember this skill" | Skills evolve. Read current version. |
| "This doesn't count as a task" | Action = task. Check for skills. |
| "The skill is overkill" | Simple things become complex. Use it. |
| "I'll just do this one thing first" | Check BEFORE doing anything. |
| "This feels productive" | Undisciplined action wastes time. Skills prevent this. |
| "I know what that means" | Knowing the concept ≠ using the skill. Invoke it. |

## Platform Adaptation

If your harness appears here, read its reference file for special instructions:

- Codex: `references/codex-tools.md`
- Pi: `references/pi-tools.md`
- Antigravity: `references/antigravity-tools.md`

## User Instructions

User instructions (CLAUDE.md, AGENTS.md, GEMINI.md, etc, direct requests) take precedence over skills, which in turn override default behavior. Only skip skill workflows or instructions when your human partner has explicitly told you to.

 succeeded in 587ms:
/* Web chat over the NDJSON stream. Speech is push-to-talk via
   MediaRecorder + the server's speech proxy — no browser speech APIs. */
"use strict";

const chat = document.getElementById("chat");
const form = document.getElementById("composer");
const input = document.getElementById("text");
const send = document.getElementById("send");
const mic = document.getElementById("mic");
const ttsWrap = document.getElementById("tts-wrap");
const ttsToggle = document.getElementById("tts-toggle");

// crypto.randomUUID needs a secure context (HTTPS/localhost); the demo may
// be served over plain HTTP, so fall back to getRandomValues.
const sessionId = crypto.randomUUID
  ? crypto.randomUUID()
  : Array.from(crypto.getRandomValues(new Uint8Array(16)),
               (b) => b.toString(16).padStart(2, "0")).join("");
let speechEnabled = false;

function add(cls, text) {
  const div = document.createElement("div");
  div.className = "msg " + cls;
  div.textContent = text;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
  return div;
}

function notice(text) {
  const div = document.createElement("div");
  div.className = "notice";
  div.textContent = text;
  chat.appendChild(div);
}

function stepsBlock() {
  const details = document.createElement("details");
  details.className = "steps";
  details.innerHTML = "<summary>Zwischenschritte</summary>";
  chat.appendChild(details);
  return details;
}

async function turn(text) {
  send.disabled = true;
  if (text !== null) add("user", text);
  const steps = stepsBlock();
  let finalText = "";
  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: sessionId, text }),
    });
    if (!res.ok) throw new Error(await res.text());
    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";
    for (;;) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      let nl;
      while ((nl = buffer.indexOf("\n")) >= 0) {
        const line = buffer.slice(0, nl); buffer = buffer.slice(nl + 1);
        if (!line.trim()) continue;
        const ev = JSON.parse(line);
        if (ev.type === "tool_call" || ev.type === "tool_result") {
          const pre = document.createElement("pre");
          pre.textContent = (ev.type === "tool_call" ? "→ " : "← ")
            + (ev.tool || "") + " "
            + JSON.stringify(ev.args ?? ev.result);
          steps.appendChild(pre);
        } else if (ev.type === "assistant") {
          finalText = ev.text;
          add("assistant", ev.text);
        } else if (ev.type === "error") {
          notice("Es gab einen technischen Fehler.");
        }
      }
    }
  } catch (err) {
    notice("Verbindung fehlgeschlagen — bitte noch einmal versuchen.");
  }
  if (!steps.querySelector("pre")) steps.remove();
  send.disabled = false;
  input.focus();
  if (finalText && speechEnabled && ttsToggle.checked) speak(finalText);
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text) return;
  input.value = "";
  turn(text);
});

/* --- speech: push-to-talk, server-proxied ------------------------------ */

let recorder = null;

async function startRecording() {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  recorder = new MediaRecorder(stream);
  const chunks = [];
  recorder.ondataavailable = (e) => chunks.push(e.data);
  recorder.onstop = async () => {
    stream.getTracks().forEach((t) => t.stop());
    mic.classList.remove("recording");
    mic.setAttribute("aria-pressed", "false");
    const blob = new Blob(chunks, { type: recorder.mimeType });
    const body = new FormData();
    body.append("audio", blob, "speech.webm");
    try {
      const res = await fetch("/speech/stt", { method: "POST", body });
      if (!res.ok) throw new Error();
      const { text } = await res.json();
      if (text.trim()) turn(text.trim());
      else notice("Ich habe nichts verstanden — bitte noch einmal.");
    } catch {
      notice("Spracherkennung gerade nicht erreichbar — bitte tippen.");
    }
  };
  recorder.start();
  mic.classList.add("recording");
  mic.setAttribute("aria-pressed", "true");
}

mic.addEventListener("click", () => {
  if (recorder && recorder.state === "recording") recorder.stop();
  else startRecording().catch(() => notice("Kein Mikrofonzugriff."));
});

async function speak(text) {
  try {
    const res = await fetch("/speech/tts", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    if (!res.ok) throw new Error();
    new Audio(URL.createObjectURL(await res.blob())).play();
  } catch {
    notice("Vorlesen gerade nicht möglich.");
  }
}

/* --- boot -------------------------------------------------------------- */

(async () => {
  try {
    const cfg = await (await fetch("/config")).json();
    if (cfg.pizzeria) {
      document.getElementById("title").textContent = cfg.pizzeria;
      document.title = cfg.pizzeria;
    }
    // Mic needs getUserMedia, which insecure contexts don't provide.
    speechEnabled = cfg.speech && !!navigator.mediaDevices;
    if (speechEnabled) {           // unset SPEECH_URL → not rendered at all
      mic.hidden = false;
      ttsWrap.hidden = false;
    }
  } catch { /* text chat works regardless */ }
  turn(null); // opening turn: the agent greets first
})();

codex
I’ve got the hotfix diff. Next I’m checking for any remaining browser APIs in the static UI that still require a secure context and whether the new `/config` contract matches the implementation.
exec
/bin/bash -lc "rg -n \"randomUUID|getRandomValues|mediaDevices|getUserMedia|MediaRecorder|Audio\\(|serviceWorker|Notification|clipboard|storage|indexedDB|geolocation|WebSocket|RTCPeerConnection|speechSynthesis|SpeechRecognition|crypto\\.subtle\" channels/static channels -g '"'!**/*.pyc'"'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,220p' channels/static/index.html" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc 'git rev-parse HEAD && git show HEAD''^:channels/static/app.js | sed -n '"'1,240p'" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 130ms:
<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pizza bestellen</title>
<link rel="stylesheet" href="/static/style.css">
</head>
<body>
<header>
  <h1 id="title">Pizza bestellen</h1>
  <label id="tts-wrap" hidden>
    <input type="checkbox" id="tts-toggle"> Antworten vorlesen
  </label>
</header>

<main id="chat" aria-live="polite"></main>

<form id="composer">
  <button type="button" id="mic" hidden aria-pressed="false"
          title="Push-to-talk: Klick startet, Klick stoppt">🎤</button>
  <input id="text" autocomplete="off"
         placeholder="Nachricht schreiben …" autofocus>
  <button type="submit" id="send">Senden</button>
</form>

<script src="/static/app.js"></script>
</body>
</html>

 succeeded in 130ms:
05808661a4b886a703b3ab55e76c786d4de84e10
/* Web chat over the NDJSON stream. Speech is push-to-talk via
   MediaRecorder + the server's speech proxy — no browser speech APIs. */
"use strict";

const chat = document.getElementById("chat");
const form = document.getElementById("composer");
const input = document.getElementById("text");
const send = document.getElementById("send");
const mic = document.getElementById("mic");
const ttsWrap = document.getElementById("tts-wrap");
const ttsToggle = document.getElementById("tts-toggle");

const sessionId = crypto.randomUUID();
let speechEnabled = false;

function add(cls, text) {
  const div = document.createElement("div");
  div.className = "msg " + cls;
  div.textContent = text;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
  return div;
}

function notice(text) {
  const div = document.createElement("div");
  div.className = "notice";
  div.textContent = text;
  chat.appendChild(div);
}

function stepsBlock() {
  const details = document.createElement("details");
  details.className = "steps";
  details.innerHTML = "<summary>Zwischenschritte</summary>";
  chat.appendChild(details);
  return details;
}

async function turn(text) {
  send.disabled = true;
  if (text !== null) add("user", text);
  const steps = stepsBlock();
  let finalText = "";
  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: sessionId, text }),
    });
    if (!res.ok) throw new Error(await res.text());
    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";
    for (;;) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      let nl;
      while ((nl = buffer.indexOf("\n")) >= 0) {
        const line = buffer.slice(0, nl); buffer = buffer.slice(nl + 1);
        if (!line.trim()) continue;
        const ev = JSON.parse(line);
        if (ev.type === "tool_call" || ev.type === "tool_result") {
          const pre = document.createElement("pre");
          pre.textContent = (ev.type === "tool_call" ? "→ " : "← ")
            + (ev.tool || "") + " "
            + JSON.stringify(ev.args ?? ev.result);
          steps.appendChild(pre);
        } else if (ev.type === "assistant") {
          finalText = ev.text;
          add("assistant", ev.text);
        } else if (ev.type === "error") {
          notice("Es gab einen technischen Fehler.");
        }
      }
    }
  } catch (err) {
    notice("Verbindung fehlgeschlagen — bitte noch einmal versuchen.");
  }
  if (!steps.querySelector("pre")) steps.remove();
  send.disabled = false;
  input.focus();
  if (finalText && speechEnabled && ttsToggle.checked) speak(finalText);
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text) return;
  input.value = "";
  turn(text);
});

/* --- speech: push-to-talk, server-proxied ------------------------------ */

let recorder = null;

async function startRecording() {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  recorder = new MediaRecorder(stream);
  const chunks = [];
  recorder.ondataavailable = (e) => chunks.push(e.data);
  recorder.onstop = async () => {
    stream.getTracks().forEach((t) => t.stop());
    mic.classList.remove("recording");
    mic.setAttribute("aria-pressed", "false");
    const blob = new Blob(chunks, { type: recorder.mimeType });
    const body = new FormData();
    body.append("audio", blob, "speech.webm");
    try {
      const res = await fetch("/speech/stt", { method: "POST", body });
      if (!res.ok) throw new Error();
      const { text } = await res.json();
      if (text.trim()) turn(text.trim());
      else notice("Ich habe nichts verstanden — bitte noch einmal.");
    } catch {
      notice("Spracherkennung gerade nicht erreichbar — bitte tippen.");
    }
  };
  recorder.start();
  mic.classList.add("recording");
  mic.setAttribute("aria-pressed", "true");
}

mic.addEventListener("click", () => {
  if (recorder && recorder.state === "recording") recorder.stop();
  else startRecording().catch(() => notice("Kein Mikrofonzugriff."));
});

async function speak(text) {
  try {
    const res = await fetch("/speech/tts", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    if (!res.ok) throw new Error();
    new Audio(URL.createObjectURL(await res.blob())).play();
  } catch {
    notice("Vorlesen gerade nicht möglich.");
  }
}

/* --- boot -------------------------------------------------------------- */

(async () => {
  try {
    const cfg = await (await fetch("/config")).json();
    speechEnabled = cfg.speech;
    if (speechEnabled) {           // unset SPEECH_URL → not rendered at all
      mic.hidden = false;
      ttsWrap.hidden = false;
    }
  } catch { /* text chat works regardless */ }
  turn(null); // opening turn: the agent greets first
})();

 succeeded in 247ms:
channels/static/app.js:2:   MediaRecorder + the server's speech proxy — no browser speech APIs. */
channels/static/app.js:13:// crypto.randomUUID needs a secure context (HTTPS/localhost); the demo may
channels/static/app.js:14:// be served over plain HTTP, so fall back to getRandomValues.
channels/static/app.js:15:const sessionId = crypto.randomUUID
channels/static/app.js:16:  ? crypto.randomUUID()
channels/static/app.js:17:  : Array.from(crypto.getRandomValues(new Uint8Array(16)),
channels/static/app.js:105:  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
channels/static/app.js:106:  recorder = new MediaRecorder(stream);
channels/static/app.js:144:    new Audio(URL.createObjectURL(await res.blob())).play();
channels/static/app.js:159:    // Mic needs getUserMedia, which insecure contexts don't provide.
channels/static/app.js:160:    speechEnabled = cfg.speech && !!navigator.mediaDevices;
channels/static/app.js:2:   MediaRecorder + the server's speech proxy — no browser speech APIs. */
channels/static/app.js:13:// crypto.randomUUID needs a secure context (HTTPS/localhost); the demo may
channels/static/app.js:14:// be served over plain HTTP, so fall back to getRandomValues.
channels/static/app.js:15:const sessionId = crypto.randomUUID
channels/static/app.js:16:  ? crypto.randomUUID()
channels/static/app.js:17:  : Array.from(crypto.getRandomValues(new Uint8Array(16)),
channels/static/app.js:105:  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
channels/static/app.js:106:  recorder = new MediaRecorder(stream);
channels/static/app.js:144:    new Audio(URL.createObjectURL(await res.blob())).play();
channels/static/app.js:159:    // Mic needs getUserMedia, which insecure contexts don't provide.
channels/static/app.js:160:    speechEnabled = cfg.speech && !!navigator.mediaDevices;

codex
I found one substantive regression risk in the hotfix path, and I’m pulling exact line numbers now so the review can be concrete. After that I’ll score it against the approval bar.
exec
/bin/bash -lc "nl -ba channels/web.py | sed -n '70,95p'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "nl -ba PLAN.md | sed -n '255,272p'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "nl -ba channels/static/app.js | sed -n '1,220p'" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 159ms:
    70	    app.state.speech = Speech()
    71	
    72	
    73	@app.get("/")
    74	def index():
    75	    return FileResponse(STATIC / "index.html")
    76	
    77	
    78	@app.get("/config")
    79	def ui_config():
    80	    # Contract per plan: speech flag + pizzeria display name. The customer
    81	    # must see which pizzeria they are ordering at.
    82	    return {"speech": app.state.speech.enabled,
    83	            "pizzeria": app.state.pizzeria_name}
    84	
    85	
    86	def _get_session(session_id: str) -> Session:
    87	    sessions = app.state.sessions
    88	    if session_id not in sessions:
    89	        # Fresh immutable menu snapshot per session (SPEC invariant 5).
    90	        try:
    91	            menu = Menu(app.state.client.get_menu())
    92	        except PizzaSimError:
    93	            raise HTTPException(503, "We're not taking orders right now.")
    94	        sessions[session_id] = Session.create(
    95	            app.state.config, menu, app.state.pizzeria_name)

 succeeded in 271ms:
     1	/* Web chat over the NDJSON stream. Speech is push-to-talk via
     2	   MediaRecorder + the server's speech proxy — no browser speech APIs. */
     3	"use strict";
     4	
     5	const chat = document.getElementById("chat");
     6	const form = document.getElementById("composer");
     7	const input = document.getElementById("text");
     8	const send = document.getElementById("send");
     9	const mic = document.getElementById("mic");
    10	const ttsWrap = document.getElementById("tts-wrap");
    11	const ttsToggle = document.getElementById("tts-toggle");
    12	
    13	// crypto.randomUUID needs a secure context (HTTPS/localhost); the demo may
    14	// be served over plain HTTP, so fall back to getRandomValues.
    15	const sessionId = crypto.randomUUID
    16	  ? crypto.randomUUID()
    17	  : Array.from(crypto.getRandomValues(new Uint8Array(16)),
    18	               (b) => b.toString(16).padStart(2, "0")).join("");
    19	let speechEnabled = false;
    20	
    21	function add(cls, text) {
    22	  const div = document.createElement("div");
    23	  div.className = "msg " + cls;
    24	  div.textContent = text;
    25	  chat.appendChild(div);
    26	  chat.scrollTop = chat.scrollHeight;
    27	  return div;
    28	}
    29	
    30	function notice(text) {
    31	  const div = document.createElement("div");
    32	  div.className = "notice";
    33	  div.textContent = text;
    34	  chat.appendChild(div);
    35	}
    36	
    37	function stepsBlock() {
    38	  const details = document.createElement("details");
    39	  details.className = "steps";
    40	  details.innerHTML = "<summary>Zwischenschritte</summary>";
    41	  chat.appendChild(details);
    42	  return details;
    43	}
    44	
    45	async function turn(text) {
    46	  send.disabled = true;
    47	  if (text !== null) add("user", text);
    48	  const steps = stepsBlock();
    49	  let finalText = "";
    50	  try {
    51	    const res = await fetch("/chat", {
    52	      method: "POST",
    53	      headers: { "Content-Type": "application/json" },
    54	      body: JSON.stringify({ session_id: sessionId, text }),
    55	    });
    56	    if (!res.ok) throw new Error(await res.text());
    57	    const reader = res.body.getReader();
    58	    const decoder = new TextDecoder();
    59	    let buffer = "";
    60	    for (;;) {
    61	      const { done, value } = await reader.read();
    62	      if (done) break;
    63	      buffer += decoder.decode(value, { stream: true });
    64	      let nl;
    65	      while ((nl = buffer.indexOf("\n")) >= 0) {
    66	        const line = buffer.slice(0, nl); buffer = buffer.slice(nl + 1);
    67	        if (!line.trim()) continue;
    68	        const ev = JSON.parse(line);
    69	        if (ev.type === "tool_call" || ev.type === "tool_result") {
    70	          const pre = document.createElement("pre");
    71	          pre.textContent = (ev.type === "tool_call" ? "→ " : "← ")
    72	            + (ev.tool || "") + " "
    73	            + JSON.stringify(ev.args ?? ev.result);
    74	          steps.appendChild(pre);
    75	        } else if (ev.type === "assistant") {
    76	          finalText = ev.text;
    77	          add("assistant", ev.text);
    78	        } else if (ev.type === "error") {
    79	          notice("Es gab einen technischen Fehler.");
    80	        }
    81	      }
    82	    }
    83	  } catch (err) {
    84	    notice("Verbindung fehlgeschlagen — bitte noch einmal versuchen.");
    85	  }
    86	  if (!steps.querySelector("pre")) steps.remove();
    87	  send.disabled = false;
    88	  input.focus();
    89	  if (finalText && speechEnabled && ttsToggle.checked) speak(finalText);
    90	}
    91	
    92	form.addEventListener("submit", (e) => {
    93	  e.preventDefault();
    94	  const text = input.value.trim();
    95	  if (!text) return;
    96	  input.value = "";
    97	  turn(text);
    98	});
    99	
   100	/* --- speech: push-to-talk, server-proxied ------------------------------ */
   101	
   102	let recorder = null;
   103	
   104	async function startRecording() {
   105	  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
   106	  recorder = new MediaRecorder(stream);
   107	  const chunks = [];
   108	  recorder.ondataavailable = (e) => chunks.push(e.data);
   109	  recorder.onstop = async () => {
   110	    stream.getTracks().forEach((t) => t.stop());
   111	    mic.classList.remove("recording");
   112	    mic.setAttribute("aria-pressed", "false");
   113	    const blob = new Blob(chunks, { type: recorder.mimeType });
   114	    const body = new FormData();
   115	    body.append("audio", blob, "speech.webm");
   116	    try {
   117	      const res = await fetch("/speech/stt", { method: "POST", body });
   118	      if (!res.ok) throw new Error();
   119	      const { text } = await res.json();
   120	      if (text.trim()) turn(text.trim());
   121	      else notice("Ich habe nichts verstanden — bitte noch einmal.");
   122	    } catch {
   123	      notice("Spracherkennung gerade nicht erreichbar — bitte tippen.");
   124	    }
   125	  };
   126	  recorder.start();
   127	  mic.classList.add("recording");
   128	  mic.setAttribute("aria-pressed", "true");
   129	}
   130	
   131	mic.addEventListener("click", () => {
   132	  if (recorder && recorder.state === "recording") recorder.stop();
   133	  else startRecording().catch(() => notice("Kein Mikrofonzugriff."));
   134	});
   135	
   136	async function speak(text) {
   137	  try {
   138	    const res = await fetch("/speech/tts", {
   139	      method: "POST",
   140	      headers: { "Content-Type": "application/json" },
   141	      body: JSON.stringify({ text }),
   142	    });
   143	    if (!res.ok) throw new Error();
   144	    new Audio(URL.createObjectURL(await res.blob())).play();
   145	  } catch {
   146	    notice("Vorlesen gerade nicht möglich.");
   147	  }
   148	}
   149	
   150	/* --- boot -------------------------------------------------------------- */
   151	
   152	(async () => {
   153	  try {
   154	    const cfg = await (await fetch("/config")).json();
   155	    if (cfg.pizzeria) {
   156	      document.getElementById("title").textContent = cfg.pizzeria;
   157	      document.title = cfg.pizzeria;
   158	    }
   159	    // Mic needs getUserMedia, which insecure contexts don't provide.
   160	    speechEnabled = cfg.speech && !!navigator.mediaDevices;
   161	    if (speechEnabled) {           // unset SPEECH_URL → not rendered at all
   162	      mic.hidden = false;
   163	      ttsWrap.hidden = false;
   164	    }
   165	  } catch { /* text chat works regardless */ }
   166	  turn(null); // opening turn: the agent greets first
   167	})();

 succeeded in 318ms:
   255	deliverability; when the reply will be spoken, at most three menu items plus
   256	an invitation.
   257	
   258	## Web channel protocol
   259	
   260	- `GET /` → static UI. `GET /config` → `{speech: bool, pizzeria: str}`
   261	  (`speech` true only if `SPEECH_URL` set and a probe succeeded at startup;
   262	  `pizzeria` is the display name from startup step 2 — the customer must
   263	  see which pizzeria they are ordering at). No language field: language is
   264	  never a UI control — the greeting comes from `PIZZERIA_LANG`, mirroring
   265	  is model behaviour.
   266	- `POST /chat` body `{session_id, text}` → `application/x-ndjson` stream of
   267	  the agent-loop events, ending with `{"type": "done", "state": ...}`.
   268	  Turns are serialized per session (one `Order` per conversation = one turn
   269	  at a time); a second request while one is in flight gets `409`.
   270	- `POST /speech/stt`: multipart audio forwarded to
   271	  `{SPEECH_URL}/v1/audio/transcriptions` with `SPEECH_STT_MODEL` and
   272	  `PIZZERIA_LANG` as the language hint (an STT hint only — it never

codex
1. [channels/static/app.js](/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js:160) conflates microphone availability with all speech features. `speechEnabled = cfg.speech && !!navigator.mediaDevices` means that on plain HTTP the UI hides both the mic and the TTS toggle, and `turn()` will never call `speak()` because `speechEnabled` is false. That fixes the insecure-context mic path, but it also disables server-side TTS on HTTP even though `/speech/tts` + `Audio(...).play()` do not require a secure context. This is a regression and a drift from the `/config.speech` contract in [PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:260), which still describes service availability, not secure-context gating.

On the reported production defect itself: the hotfix does address the main failure mode. Replacing unconditional `crypto.randomUUID()` with a `crypto.getRandomValues()` fallback removes the load-time crash path in `app.js`, so greeting and send should work again over plain HTTP on a public IP. The pizzeria name requirement is also satisfied: `/config` now returns `pizzeria`, and the client sets both the visible heading and `document.title` via `textContent`, which is the safe way to render that string.

I do not see other static-UI features that are still secure-context-dependent in a way that would kill the whole page at load. The remaining secure-context-sensitive area is microphone capture (`navigator.mediaDevices.getUserMedia`, effectively also `MediaRecorder` in practice), and that path is now kept off the main boot path and hidden on insecure HTTP. Text chat, `/config`, NDJSON streaming, and TTS playback are not blocked the same way.

SCORES (1-5 each, 5 = best):
completeness: 4
correctness: 4
error_handling: 3
simplicity: 4
spec_compliance: 3
TOTAL: 18/25
VERDICT: CHANGES_REQUIRED
ISSUES: (max 5 bullets, concrete and actionable, empty if approved)
- Split speech capability flags in `channels/static/app.js`: keep TTS enabled from `cfg.speech`, and gate only the mic button on `navigator.mediaDevices` (and ideally `MediaRecorder`) so plain-HTTP users can still use server-side TTS.
tokens used
22,960
1. [channels/static/app.js](/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js:160) conflates microphone availability with all speech features. `speechEnabled = cfg.speech && !!navigator.mediaDevices` means that on plain HTTP the UI hides both the mic and the TTS toggle, and `turn()` will never call `speak()` because `speechEnabled` is false. That fixes the insecure-context mic path, but it also disables server-side TTS on HTTP even though `/speech/tts` + `Audio(...).play()` do not require a secure context. This is a regression and a drift from the `/config.speech` contract in [PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:260), which still describes service availability, not secure-context gating.

On the reported production defect itself: the hotfix does address the main failure mode. Replacing unconditional `crypto.randomUUID()` with a `crypto.getRandomValues()` fallback removes the load-time crash path in `app.js`, so greeting and send should work again over plain HTTP on a public IP. The pizzeria name requirement is also satisfied: `/config` now returns `pizzeria`, and the client sets both the visible heading and `document.title` via `textContent`, which is the safe way to render that string.

I do not see other static-UI features that are still secure-context-dependent in a way that would kill the whole page at load. The remaining secure-context-sensitive area is microphone capture (`navigator.mediaDevices.getUserMedia`, effectively also `MediaRecorder` in practice), and that path is now kept off the main boot path and hidden on insecure HTTP. Text chat, `/config`, NDJSON streaming, and TTS playback are not blocked the same way.

SCORES (1-5 each, 5 = best):
completeness: 4
correctness: 4
error_handling: 3
simplicity: 4
spec_compliance: 3
TOTAL: 18/25
VERDICT: CHANGES_REQUIRED
ISSUES: (max 5 bullets, concrete and actionable, empty if approved)
- Split speech capability flags in `channels/static/app.js`: keep TTS enabled from `cfg.speech`, and gate only the mic button on `navigator.mediaDevices` (and ideally `MediaRecorder`) so plain-HTTP users can still use server-side TTS.
