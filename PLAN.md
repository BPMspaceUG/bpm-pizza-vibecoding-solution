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

- Messages: `[system] + history`. System prompt = `prompts/system.{lang}.md`
  with `{pizzeria_name}` substituted (captured in startup step 2), where
  `lang = PIZZERIA_LANG` — the pizzeria-country greeting language, a
  required env var (see Configuration), **not** a channel or UI control.
  Both prompt files state the same per-turn rule: always answer in the
  language of the customer's latest message (German or English), unprompted.
  Language mirroring is model behaviour; the runtime never detects language.
- Per turn: POST `{LITELLM_PIZZA_URL}/chat/completions`, bearer
  `LITELLM_PIZZA_KEY`, model `LITELLM_PIZZA_MODEL_1`, `tools` = the eight
  schemas. While the response contains `tool_calls`: dispatch each through
  `core/tools.py`, append tool result messages, call again. Stop on a plain
  assistant message or after 8 tool iterations (loop guard → apology).
- Gateway timeout (httpx timeout, 30s): one retry, then abort the turn with
  the plain apology from the error table. Gateway 4xx/5xx: no retry, abort
  turn, log.
- The loop emits events to a callback: `user`, `assistant`, `tool_call`,
  `tool_result`, `state`, `error` — the CLI prints them (verbose), the web
  channel streams them as NDJSON, and every event is also appended as one
  JSON line to `logs/agent-<session>.jsonl` (fixed path, gitignored). Log
  records carry no secrets: config values never enter events; tool results
  are logged as-is (they contain no secrets by construction).

## Conversation policy → prompts

`prompts/system.de.md` / `system.en.md`, same content in two languages, calm
and short (no shouting — the state machine enforces the rules). Each covers:
greet once in the file's language and offer help in one sentence; mirror the
customer's language per turn (German ↔ English); one question per turn; menu
facts only from `get_menu`; collect first name (confirm spelling when it
came from speech) and street, street declinable; read back via `read_back`
and wait for an explicit yes — "mhm"/silence is not yes, ask once more, then
offer to start over; never announce success before `submit_order` returns;
state order id in speakable groups and ETA in minutes; errors in plain
language, never codes or JSON; never claim the address was checked for
deliverability; when the reply will be spoken, at most three menu items plus
an invitation.

## Web channel protocol

- `GET /` → static UI. `GET /config` → `{speech: bool}` (true only if
  `SPEECH_URL` set and a probe succeeded at startup). No language field:
  language is never a UI control — the greeting comes from `PIZZERIA_LANG`,
  mirroring is model behaviour.
- `POST /chat` body `{session_id, text}` → `application/x-ndjson` stream of
  the agent-loop events, ending with `{"type": "done", "state": ...}`.
  Turns are serialized per session (one `Order` per conversation = one turn
  at a time); a second request while one is in flight gets `409`.
- `POST /speech/stt`: multipart audio forwarded to
  `{SPEECH_URL}/v1/audio/transcriptions` with `SPEECH_STT_MODEL` and
  `PIZZERIA_LANG` as the language hint (an STT hint only — it never
  influences assistant output language) → `{text}`. `POST /speech/tts` body `{text}` forwarded to
  `{SPEECH_URL}/v1/audio/speech` with `SPEECH_TTS_MODEL` +
  `SPEECH_TTS_VOICE` → audio bytes. Proxying keeps the speech URL and
  models server-side.
- UI: chat pane, collapsible per-turn tool-step feed (rendered from
  `tool_call`/`tool_result` events), push-to-talk mic button (MediaRecorder,
  visible recording state, click-start/click-stop), speaker toggle
  (default off, applies only to the final assistant message). If
  `/config.speech` is false, mic and speaker are simply not rendered; text
  chat is fully usable. A failed STT/TTS call shows a small notice and never
  touches the order.

## Error handling (SPEC table → implementation)

| Situation | Mechanism |
|---|---|
| Gateway timeout | httpx timeout 30s, one retry in agent loop, then apology; test via transport stub |
| PizzaSim 401/403 | typed `AuthError`, no retry, turn aborted with "can't reach the kitchen system" |
| 404 pizzeria at startup | startup check refuses to start with clear stderr message |
| 422 validation | typed `ValidationError(details)` → tool error `submit_failed` with field text, basket kept |
| 5xx on submit | no blind retry; `submit_unknown=True`, honest message |
| Submit timeout | same as 5xx + verify-via-list recovery on the next attempt |
| Unknown item / extra | `unknown_item` / `invalid_extra` + candidates |
| Empty basket at submit | `invalid_state` from transition table |
| Menu fetch fails at start | both channels exit with "We're not taking orders right now" |

## Testing

- `test_state.py`: every ✗ cell of the transition table, every invariant
  1–5, revision/read-back staleness, demotion from CONFIRMED, terminality of
  SUBMITTED, empty-basket edge (remove to empty and re-add).
- `test_tools.py`: dispatch against a `Menu` built from
  `fixtures/menu.json` and a fake PizzaSim client returning fixture
  payloads: unknown code candidates, per-type code collision (`tonno`),
  invalid extra, `"zwei"` quantity, atomic multi-item add, remove semantics,
  submit success mapping (`order_id`, `status`, `eta_seconds`), submit
  timeout → unknown → recovery-by-list (correlation via
  `submit_attempted_at`), 422 mapping, snapshot completeness.
- `test_transcripts.py` + `transcripts/`: five golden conversations (happy
  path, correction "no make that three", unknown item, mind change after
  read-back, submit timeout) as JSON: each step = user text, scripted model
  tool calls (a stub model replays them), expected tool result codes,
  expected final state and exact call sequence. No network, no LLM.
- Live acceptance test (`PIZZA_LIVE_TEST=1` opt-in, in `test_tools.py`),
  per SPEC "What done looks like": full conversation at the tool layer,
  submit, then read the pizzeria's orders back and assert the order is
  listed with the right customer and **exactly** the read-back items and
  quantities (via the order-detail endpoint). The only test touching the
  real API.
- Speech: manual checklist in README (dictation, name correction, menu
  question, `SPEECH_URL` unset run).

## Tickets

1. **Scaffold + config.** `.env.example`, `requirements.txt`, README
   skeleton, gitignore for `logs/`, env loader (process env, else `~/.env`)
   with named-var `ConfigError`.
   ☐ `.env.example` lists all 12 vars (incl. `PIZZERIA_LANG`), names only
   ☐ missing var exits pre-turn with var + file name ☐ nothing prints
   values.
2. **Order + state machine + tests.** `core/order.py`, `core/state.py`,
   `tests/test_state.py`.
   ☐ all five invariants tested ☐ every ✗ cell tested ☐ demotion +
   revision staleness tested ☐ pytest green.
3. **Menu.** `core/menu.py`, `fixtures/menu.json` (recorded), validation +
   candidates. ☐ (type, code) validation ☐ `tonno` collision test ☐
   extras vocabulary ☐ ≤3 candidates.
4. **PizzaSim client.** `core/pizzasim.py`, typed errors, timeouts,
   fixtures for orders/422/location, httpx MockTransport tests.
   ☐ every error class mapped ☐ no call without timeout ☐ submit returns
   typed result ☐ list_orders parsed.
5. **Tools.** `core/tools.py` schemas + dispatch, `tests/test_tools.py`.
   ☐ schemas match this plan exactly ☐ atomic add ☐ error shape uniform
   ☐ snapshot on every success.
6. **Agent loop + prompts + transcripts.** `core/agent.py`, both prompts,
   stub model, five transcripts.
   ☐ tool loop with guard ☐ gateway retry-once ☐ JSONL logging ☐ five
   transcripts green.
7. **CLI.** `channels/cli.py`. ☐ full conversation against real API
   possible ☐ --verbose shows tool events ☐ startup checks enforced.
8. **Web text channel.** `channels/web.py` + `static/` (no speech yet).
   ☐ port 8888 ☐ NDJSON steps visible in UI ☐ per-session orders ☐
   startup checks enforced.
9. **Speech.** Proxy endpoints + mic/TTS UI.
   ☐ push-to-talk with visible state ☐ TTS off by default, final message
   only ☐ `SPEECH_URL` unset → no mic, no speaker, text works ☐ speech
   failure never touches the order.
10. **Harden + docs.** Walk the SPEC error table end to end, README
    complete, `.env.example` final, live smoke test.
    ☐ each error row demonstrably handled ☐ README covers all channels +
    speech + tests ☐ full suite green.

Each ticket ≤ 1h, tests live in the ticket that introduces the behaviour.
