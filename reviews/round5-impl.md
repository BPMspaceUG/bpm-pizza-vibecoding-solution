OpenAI Codex v0.143.0
--------
workdir: /home/rob/bpm-pizza-vibecoding-solution
model: gpt-5.4
provider: openai
approval: never
sandbox: read-only
reasoning effort: medium
reasoning summaries: none
session id: 019fb900-c8f4-7e21-b2ec-38adbabbc704
--------
user
You are an independent reviewer for the repository in the current working directory. You are read-only; you never write code. Two roles in one pass:
1. Devil's advocate: attack the implementation — bugs, gaps, missing error cases, spec violations, divergence from the approved plan.
2. Judge: score against the fixed rubric.

Task: Review the IMPLEMENTATION (stage 2, round 2 of max 3) against SPEC.md (source of truth) and PLAN.md (the approved stage-1 plan; approved 24/25 in reviews/round3-plan.md, since updated only to document remove_item disambiguation semantics). Implementation: core/, channels/, prompts/, tests/, README.md, .env.example, requirements.txt.

Round 1 (stateless, reviews/round4-impl.md) required four changes; all were applied — verify in the files, do not take this on faith:
1. remove_item ambiguity with same (type, code) and different extras → deterministic semantics in core/state.py (no qty removes all matching lines; qty reduces the most recently added), documented in PLAN.md tool table, tested in tests/test_state.py (test_remove_without_qty_clears_all_variants, test_remove_with_qty_reduces_most_recent_variant). The spec fixes remove_item's parameters, so an extras parameter was not an option.
2. Speech probe now requires 2xx (raise_for_status) in channels/web.py.
3. Gateway timeout aligned to the plan's 30s in core/agent.py.
4. requirements.txt pinned to exact versions.

Facts you cannot observe from the files, all demonstrated live: the deterministic suite passes (69 passed, 1 skipped opt-in live test); the web channel started with SPEECH_URL unset (speech:false, mic not rendered) and placed a real order end to end via the real gateway (read_back -> confirm_order(revision) -> submit_order -> order_id 3fe1deaa-... visible in the pizzeria's order list, ETA converted to minutes, id read in groups); a missing required env var exits before the first turn naming the variable and file. Your sandbox may lack a writable temp dir for pytest; judge from the code plus this evidence if so.

Scope notes: tests/fixtures/*.json are recorded real API responses (UUIDs there are recorded data, not hardcoded config). venv/ and logs/ are gitignored runtime artifacts, out of scope.

Output MUST end with exactly this block (numbers 1-5, 5 best):
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
I’m reviewing the implementation against `SPEC.md`, `PLAN.md`, and the round-1 review findings first, then I’ll inspect the implementation and tests to verify each claimed fix before scoring.
exec
/bin/bash -lc "sed -n '1,220p' /home/rob/.agents/skills/using-superpowers/SKILL.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc pwd in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 112ms:
/home/rob/bpm-pizza-vibecoding-solution

 succeeded in 137ms:
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

codex
Using `using-superpowers` to select the required workflow, then I’m moving into the repo documents and target files for the actual review.
exec
/bin/bash -lc "sed -n '1,240p' /home/rob/.agents/skills/using-superpowers/references/codex-tools.md" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 0ms:
## Subagent dispatch requires multi-agent support

Add to your Codex config (`~/.codex/config.toml`):

```toml
[features]
multi_agent = true
```

This enables `spawn_agent`, `wait_agent`, and `close_agent` for skills like `dispatching-parallel-agents` and `subagent-driven-development`. When using subagent-driven-development, close reviewer subagents when their review returns. Keep each implementer subagent open until its task's review passes — the fix loop resumes the implementer — then close it. If your harness cannot send another message to a spawned agent, dispatch each fix round as a fresh implementer carrying the brief, the report file, and the findings.

## Environment Detection

Skills that create worktrees or finish branches should detect their
environment with read-only git commands before proceeding:

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
BRANCH=$(git branch --show-current)
```

- `GIT_DIR != GIT_COMMON` → already in a linked worktree (skip creation)
- `BRANCH` empty → detached HEAD (cannot branch/push/PR from sandbox)

See `using-git-worktrees` Step 0 and `finishing-a-development-branch`
Step 1 for how each skill uses these signals.

## Codex App Finishing

When the sandbox blocks branch/push operations (detached HEAD in an
externally managed worktree), the agent commits all work and informs
the user to use the App's native controls:

- **"Create branch"** — names the branch, then commit/push/PR via App UI
- **"Hand off to local"** — transfers work to the user's local checkout

The agent can still run tests, stage files, and output suggested branch
names, commit messages, and PR descriptions for the user to copy.

exec
/bin/bash -lc "rg --files -g 'SPEC.md' -g 'PLAN.md' -g 'reviews/round3-plan.md' -g 'reviews/round4-impl.md' -g 'README.md' -g '.env.example' -g 'requirements.txt' -g 'core/**' -g 'channels/**' -g 'prompts/**' -g 'tests/**'" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 0ms:
requirements.txt
.env.example
PLAN.md
reviews/round4-impl.md
reviews/round3-plan.md
core/tools.py
README.md
core/order.py
SPEC.md
channels/web.py
channels/cli.py
channels/__pycache__/cli.cpython-313.pyc
channels/__init__.py
channels/__pycache__/__init__.cpython-313.pyc
core/menu.py
core/__init__.py
core/state.py
core/pizzasim.py
core/agent.py
channels/__pycache__/web.cpython-313.pyc
core/__pycache__/menu.cpython-313.pyc
core/__pycache__/agent.cpython-313.pyc
core/__pycache__/pizzasim.cpython-313.pyc
core/__pycache__/tools.cpython-313.pyc
core/__pycache__/state.cpython-313.pyc
core/__pycache__/order.cpython-313.pyc
core/__pycache__/__init__.cpython-313.pyc
prompts/system.en.md
prompts/system.de.md
channels/static/index.html
channels/static/style.css
channels/static/app.js
tests/test_transcripts.py
tests/test_tools.py
tests/test_state.py
tests/__init__.py
tests/__pycache__/test_tools.cpython-313-pytest-9.1.1.pyc
tests/__pycache__/__init__.cpython-313.pyc
tests/__pycache__/test_transcripts.cpython-313-pytest-9.1.1.pyc
tests/__pycache__/test_state.cpython-313-pytest-9.1.1.pyc
tests/transcripts/unknown_item.json
tests/transcripts/mind_change.json
tests/transcripts/submit_timeout.json
tests/transcripts/happy_path.json
tests/transcripts/correction.json
tests/fixtures/menu.json
tests/fixtures/order_created.json
tests/fixtures/pizzerias.json
tests/fixtures/orders_list.json
tests/fixtures/location.json
tests/fixtures/error_422.json

codex
I have the review surface. Next I’m checking the spec, approved plan, and prior round findings side by side, then I’ll trace the implementation and tests for conformance and regressions.
Reviewing implementation against spec, approved plan, and round-1 required fixes before issuing findings and rubric scores.
  → Read SPEC.md, PLAN.md, and prior review docs to extract required behavior and prior mandatory fixes
  • Inspect implementation files in core/, channels/, prompts/, README.md, .env.example, requirements.txt for compliance and regressions
  • Inspect tests for coverage of required behavior, especially round-1 fixes and spec-critical flows
  • Produce findings ordered by severity and score against the rubric
exec
/bin/bash -lc "sed -n '1,320p' PLAN.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' reviews/round3-plan.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' SPEC.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' reviews/round4-impl.md" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 219ms:
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
`submit_unknown` and first calls `list_orders()`, looking for an order with
our customer's `first_name` and `created_at >= submit_attempted_at - 60`
(60s clock-skew allowance). Found → adopt its `id` as order_id, state
`SUBMITTED`, message says the order went through. Not found → exactly one
real retry. List endpoint itself fails → error `submit_unknown` with an
honest message ("I'm not sure that went through — let me check" phrasing);
never a blind re-POST.

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
- Live smoke (`PIZZA_LIVE_TEST=1` opt-in, in `test_tools.py`): one real
  order via the real API, asserts `order_id` present.
- Speech: manual checklist in README (dictation, name correction, menu
  question, `SPEECH_URL` unset run).

## Tickets

1. **Scaffold + config.** `.env.example`, `requirements.txt`, README
   skeleton, gitignore for `logs/`, env loader (process env, else `~/.env`)
   with named-var `ConfigError`.
   ☐ `.env.example` lists all 12 vars (incl. `PIZZERIA_LANG`), names only
   ☐ missing var exits pre-turn with var + file name ☐ nothing prints
   values.

 succeeded in 251ms:
# PizzaSim Ordering Agent — Specification

> Hand this to a coding agent as the entire task:
> `FOLLOW INSTRUCTIONS PRECISELY AT "SPEC.MD"`.
> This file is the source of truth for what the agent is. Everything else in the
> repo — code, tests, prompts, tickets — derives from it.

---

## Where this format comes from

The **shape** of this document is not ours. It is borrowed from Cedric Mössner —
**The Morpheus** ([youtube.com/@TheMorpheusTutorials](https://www.youtube.com/@TheMorpheusTutorials)),
who writes exactly one `SPEC.md` per project and hands the identical file to every
new model in order to compare them. The prompt he sends alongside it is a single
line — `FOLLOW INSTRUCTIONS PRECISELY AT "SPEC.MD"` — which is why that line, and
not a long prompt, stands at the top of this file.

The sections adopted from his specs: *Soul*, *The One Load-Bearing Idea*, hard
*Scope In / Out*, an explicit autonomy clause, work *in passes* with verification
after each, a file-level *Deliverables* list, *Decisions Locked / Deferred*, and
the one-hour *ticket sizing rules*.

Reference specs:

- [github.com/TheMorpheus407/morphcook](https://github.com/TheMorpheus407/morphcook)
  — offline Flutter recipe app; one spec, seven model implementations.
- [github.com/TheMorpheus407/hogwarts-blender-benchmark](https://github.com/TheMorpheus407/hogwarts-blender-benchmark)
  — fully procedural Blender build; `prompt.txt` plus `SPEC.md`.

The content below is ours. The form is his — with thanks.

---

## Soul

Ordering food by phone works because the person on the other end keeps the order
in their head, reads it back to you, and only then walks to the kitchen. Nothing
is cooked before you said yes.

Most LLM ordering demos invert this. The model holds the order in its context,
guesses item names that sound close enough, and fires the write call the moment
it feels confident. It works in the demo and fails on the fourth turn, in a noisy
room, when the customer changes their mind.

This agent puts the order back where it belongs: **in the code**. The model does
the one thing it is genuinely good at — turning messy human speech into intent —
and nothing else. It never holds the cart, never invents a menu item, and never
reaches the kitchen without a spoken confirmation.

**Core belief:** a language model is a great waiter and a terrible order pad.

---

## The One Load-Bearing Idea

**The order is a state machine owned by the code. The model only speaks.**

- There is exactly one `Order` object per conversation, held by the runtime.
- The model cannot write to it directly. It can only call tools that request a
  transition, and every transition is validated before it is applied.
- Every item code is validated against the **live menu**. An unknown code is a
  tool error carrying candidate matches — never a silent guess, never a fallback
  to a hardcoded list.
- `submit_order` is the only call that reaches the network as a write, and it is
  legal in exactly one state: `CONFIRMED`. The only way into `CONFIRMED` is a
  read-back the customer answered yes to.
- The same core serves every channel. A transport carries words in and words
  out; it owns no order logic whatsoever.

This one rule replaces prompt-engineering the model into good behaviour. If the
model misbehaves, the state machine refuses — and the refusal is a tool result
the model must deal with in front of the customer.

---

## Scope

### In

- **Two transports over one core:**
  - `cli` — interactive terminal chat.
  - `web` — local FastAPI server on port 8888, browser chat UI, streaming the
    agent's intermediate steps as newline-delimited JSON so tool calls and tool
    results are visible and not just the final answer.
- **Speech on the web transport**, served by a self-hosted CPU-only speech
  container over HTTP. See *Speech*.
- **Languages:** German and English. The agent answers in the language the
  customer used, per turn, without being told to switch.
- **Menu, cart, customer, submit.** The full happy path plus correction
  ("no, make that three"), removal, and abandonment.
- **The success moment:** the order appears in the PizzaSim dashboard under the
  configured pizzeria, with the right customer, items and quantities.
- **Deterministic tests** that run with no network and no LLM.
- **Structured logging** of every turn: user text, model tool calls, tool
  results, state transitions. One line per event, JSON, to a file.

### Out (explicitly)

- Payment, pricing totals, delivery routing, ETA prediction of our own.
- Accounts, auth, sessions surviving a process restart.
- Modifying or cancelling an order after it was submitted.
- Switching pizzeria at runtime — one process serves one `PIZZERIA_ID`.
- Any regex or keyword parser that produces an order without the model.
  See **Anti-patterns**; this is not a style preference, it is a hard ban.
- Reading the whole menu aloud when the answer will be spoken.
- Persisting customer data anywhere beyond the process and the PizzaSim API.

---

## Environment and configuration

All configuration comes from environment variables. Load `~/.env` if present;
never write to it, never create it, never print a value.

| Variable | Purpose |
|---|---|
| `LITELLM_PIZZA_URL` | OpenAI-compatible gateway base URL (`/chat/completions` appended) |
| `LITELLM_PIZZA_KEY` | Bearer token for the gateway |
| `PIZZASIM_URL` | PizzaSim API base URL |
| `PIZZASIM_API_KEY` | Sent as header `X-API-Key` on protected routes |
| `PIZZERIA_ID` | UUID of the pizzeria this process serves |
| `LITELLM_PIZZA_MODEL_1` | Model the ordering agent calls; required, no default in code |
| `LITELLM_PIZZA_MODEL_2` | Second configured model, where the build uses one |

Rules:

- **Nothing is hardcoded.** No UUID, no model name, no menu, no base URL —
  not even as a fallback "just in case".
- Missing or empty variable → exit before the first turn with a message naming
  the variable and the file it was expected in. Never start half-configured.
- Secrets never appear in logs, transcripts, error messages or the web UI.

---

## The PizzaSim API (contract)

| Call | Auth | Notes |
|---|---|---|
| `GET /menu` | public | returns `pizzas[]` and `pasta[]`, each with `code` |
| `GET /pizzerias` | `X-API-Key` | list of pizzerias with `id`, `name` |
| `POST /pizzerias/{PIZZERIA_ID}/orders` | `X-API-Key` | places the order |
| `GET /location?street=…` | public | street plausibility check |

Order request body:

```json
{
  "customer": { "first_name": "Marco", "street_one": "via di Cantieri" },
  "items": [{ "type": "pizza", "code": "margherita", "qty": 2, "extras": [] }]
}
```

Response carries `order_id`, `status`, `eta_seconds`.

Facts that shape behaviour:

- The tenant is **always** in the URL path, never in a header.
- Customers are unique per pizzeria **by first name**. An unknown name silently
  creates a new customer — so a misheard name creates a ghost. Speech input must
  therefore confirm the name explicitly.
- `street_one` is optional and is **not** validated for deliverability. Asking
  for it is a policy of this agent, not an API requirement — do not pretend to
  the customer that we checked something we did not.
- `POST` is **not idempotent**. A retry after a timeout can double the order.
  See **Error handling**.

### Contract facts — verified against the live API (2026-07-31)

All seven former open questions were resolved by probing the live API
(`GET /menu`, `GET /pizzerias`, `POST /pizzerias/{id}/orders` — valid and
invalid bodies —, `GET /pizzerias/{id}/orders`, `GET /location`). Facts below
are from real responses, not documentation.

1. **Order response field name: `order_id`.** A successful
   `POST /pizzerias/{id}/orders` returns
   `{"order_id": "<uuid>", "status": "ordered", "eta_seconds": <int>}`.
   The **list** endpoint uses `id` for the same value — the two names coexist,
   one per endpoint.
2. **The list endpoint exists.** `GET /pizzerias/{id}/orders` (auth:
   `X-API-Key`) returns `{"orders": [...]}`, newest first, each with `id`,
   `customer_id`, `created_at`, `ready_at`, `status`, `delivered_at`,
   `first_name`. It does **not** include items, so submit-timeout recovery
   matches on `first_name` + `created_at` recency.
3. **Menu item shape:** `{"code", "name", "base": [ingredients], "price"}`.
   `name` is a single string (Italian proper names, identical in DE and EN) —
   there are no per-language names in the API; read-back uses `name` as-is in
   both languages. The menu response also carries a top-level `toppings[]`
   array of ingredient codes.
4. **`extras[]` is a controlled vocabulary:** the top-level `toppings[]` from
   `GET /menu` (e.g. `mozzarella`, `mushrooms`, `pineapple`). The server
   rejects unknown extras with `422` (`"items[0].extras contains invalid
   topping 'unicorn_dust'"`), so the tool layer validates extras against
   `toppings[]` exactly like item codes.
5. **Error bodies are machine-readable:**
   `{"error": "<code>", "details": ["<human sentence>", ...]}` — e.g.
   `{"error": "validation_failed", "details": ["items[0].code must be a valid
   pizza code"]}` with HTTP 422. The tool layer maps `error` to typed errors
   and may surface `details` to targeted questions.
6. **Status values observed in the lifecycle:** `ordered` →
   `prepared_planned` → `delivered` (with `delivered_at` set on the last).
   A fresh order starts as `ordered`.
7. **`GET /location?street=` returns** `{"street": "<echo>",
   "deliverable": <bool>}` with HTTP 200. In probing, even a nonsense street
   returned `deliverable: true` — the check is a weak plausibility signal at
   best, which confirms the policy above: never tell the customer an address
   was verified.

Additional verified fact: item `code`s are unique **per type**, not globally —
`tonno` exists as both a pizza and a pasta. Validation and removal must always
key on `(type, code)`.

---

## Order state machine

```
EMPTY ──add_items──▶ COLLECTING ──set_customer──▶ READY
  ▲                      │  ▲                       │
  └──remove last item────┘  └───add/remove/edit─────┘
                                                    │ read_back + customer says yes
                                                    ▼
                                               CONFIRMED ──submit_order──▶ SUBMITTED
                                                    │                          
                                                    └──any change──▶ back to READY
```

Invariants, all enforced in code and all covered by unit tests:

1. `submit_order` outside `CONFIRMED` returns an error. It does not "helpfully"
   confirm on the model's behalf.
2. Any mutation after `CONFIRMED` drops the order back to `READY`. A confirmation
   applies to the basket that was read back, not to a later one.
3. `CONFIRMED` is reachable only via `confirm_order`, and `confirm_order` is only
   legal after `read_back` has been called for the current basket revision. The
   basket carries a revision counter; `confirm_order` must name it.
4. `SUBMITTED` is terminal. The conversation may continue; the order may not.
5. An item may only enter the basket with a `code` present in the menu snapshot
   fetched this session.

---

## Tools

The model sees exactly these. Names, parameters and semantics are fixed.

| Tool | Parameters | Returns |
|---|---|---|
| `get_menu` | — | pizzas and pasta with codes and display names in both languages |
| `add_items` | `items[]` of `{type, code, qty, extras[]}` | new basket + revision |
| `remove_item` | `code`, `type`, optional `qty` | new basket + revision |
| `set_customer` | `first_name`, optional `street_one` | customer as stored |
| `read_back` | — | basket, customer, revision — the text the agent must read out |
| `confirm_order` | `revision` | state `CONFIRMED`, or error if stale |
| `submit_order` | — | `order_id`, `status`, `eta_seconds` |
| `check_street` | `street` | plausibility result (optional) |

Tool result conventions:

- Success: the **full current state**, not a diff. The model should never have to

 succeeded in 266ms:
OpenAI Codex v0.143.0
--------
workdir: /home/rob/bpm-pizza-vibecoding-solution
model: gpt-5.4
provider: openai
approval: never
sandbox: read-only
reasoning effort: medium
reasoning summaries: none
session id: 019fb8f1-b725-77e0-a4a6-a6b6792e6f1a
--------
user
You are an independent reviewer for the repository in the current working directory. You are read-only; you never write code. You play two roles in one pass:
1. Devil's advocate: attack the plan — gaps, wrong assumptions, missing error cases, spec violations.
2. Judge: score against the fixed rubric.

Task: Read SPEC.md (the source of truth) and PLAN.md (the stage-1 implementation plan under review, round 3 of max 3). Judge whether PLAN.md is a complete, correct, spec-compliant plan such that implementing exactly it satisfies SPEC.md. The "Contract facts" section in SPEC.md was verified against the live API and is trustworthy. decisions/qa.md records an oracle decision on the greeting language (required env var PIZZERIA_LANG) taken between rounds.

Round 2 (stateless, see reviews/round2-plan.md) required: (1) one exact tool-result contract per tool composing the per-tool table with the full-current-state rule, and fixing an eta_minutes test regression; (2) a spec-compliant, non-hardcoded, non-UI source for the greeting language; (3) explicit persisted state for submit-timeout recovery correlation; (4) removing lang from the chat contract or fencing it to an STT hint; (5) per-session immutable menu snapshot ownership. All five were addressed in the current PLAN.md — verify in the file, do not take this note on faith: see the SNAPSHOT definition in "Tool schemas", the PIZZERIA_LANG paragraph in "Configuration", submit_attempted_at in the state-machine section, the web protocol section, and the "Session model" paragraph.

Judging guidance: score the plan that exists. If remaining concerns are implementation-detail-sized rather than plan-sized, they belong in the implementation review, not in a plan rejection.

Output MUST end with exactly this block (numbers 1-5, 5 best):
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
I’m reviewing `SPEC.md`, `PLAN.md`, the prior round review, and the QA decision first. I’m using the `using-superpowers` skill to ensure the required workflow, then I’ll assess the plan strictly against the spec and rubric.
exec
/bin/bash -lc "sed -n '1,260p' reviews/round2-plan.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,220p' decisions/qa.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,220p' /home/rob/.agents/skills/using-superpowers/SKILL.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' PLAN.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' SPEC.md" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 714ms:
OpenAI Codex v0.143.0
--------
workdir: /home/rob/bpm-pizza-vibecoding-solution
model: gpt-5.4
provider: openai
approval: never
sandbox: read-only
reasoning effort: medium
reasoning summaries: none
session id: 019fb8ed-b319-73c0-a451-4882d153ad38
--------
user
You are an independent reviewer for the repository in the current working directory. You are read-only; you never write code. You play two roles in one pass:
1. Devil's advocate: attack the plan — gaps, wrong assumptions, missing error cases, spec violations.
2. Judge: score against the fixed rubric.

Task: Read SPEC.md (the source of truth) and PLAN.md (the stage-1 implementation plan under review, round 2). Judge whether PLAN.md is a complete, correct, spec-compliant plan such that implementing exactly it satisfies SPEC.md. The "Contract facts" section in SPEC.md was verified against the live API and is trustworthy.

Context from round 1 (a previous stateless review): it required (a) no ./.env fallback and no extra config vars, (b) tool results matching the spec's fixed contract exactly, (c) greeting in the pizzeria-country language with per-turn mirroring not driven by UI controls, (d) one explicit startup sequence validating PIZZERIA_ID via GET /pizzerias, (e) a confirmation path no broader than the spec. All five were applied; verify they are actually resolved in the current PLAN.md rather than taking this note on faith.

Output MUST end with exactly this block (numbers 1-5, 5 best):
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
Reviewing `SPEC.md` and `PLAN.md` against each other first, then I’ll score the plan strictly against the rubric and the round-1 carryover requirements.
exec
/bin/bash -lc "sed -n '1,220p' /home/rob/.agents/skills/using-superpowers/SKILL.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' SPEC.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' PLAN.md" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 263ms:
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

 succeeded in 361ms:
# PizzaSim Ordering Agent — Specification

> Hand this to a coding agent as the entire task:
> `FOLLOW INSTRUCTIONS PRECISELY AT "SPEC.MD"`.
> This file is the source of truth for what the agent is. Everything else in the
> repo — code, tests, prompts, tickets — derives from it.

---

## Where this format comes from

The **shape** of this document is not ours. It is borrowed from Cedric Mössner —
**The Morpheus** ([youtube.com/@TheMorpheusTutorials](https://www.youtube.com/@TheMorpheusTutorials)),
who writes exactly one `SPEC.md` per project and hands the identical file to every
new model in order to compare them. The prompt he sends alongside it is a single
line — `FOLLOW INSTRUCTIONS PRECISELY AT "SPEC.MD"` — which is why that line, and
not a long prompt, stands at the top of this file.

The sections adopted from his specs: *Soul*, *The One Load-Bearing Idea*, hard
*Scope In / Out*, an explicit autonomy clause, work *in passes* with verification
after each, a file-level *Deliverables* list, *Decisions Locked / Deferred*, and
the one-hour *ticket sizing rules*.

Reference specs:

- [github.com/TheMorpheus407/morphcook](https://github.com/TheMorpheus407/morphcook)
  — offline Flutter recipe app; one spec, seven model implementations.
- [github.com/TheMorpheus407/hogwarts-blender-benchmark](https://github.com/TheMorpheus407/hogwarts-blender-benchmark)
  — fully procedural Blender build; `prompt.txt` plus `SPEC.md`.

The content below is ours. The form is his — with thanks.

---

## Soul

Ordering food by phone works because the person on the other end keeps the order
in their head, reads it back to you, and only then walks to the kitchen. Nothing
is cooked before you said yes.

Most LLM ordering demos invert this. The model holds the order in its context,
guesses item names that sound close enough, and fires the write call the moment
it feels confident. It works in the demo and fails on the fourth turn, in a noisy
room, when the customer changes their mind.

This agent puts the order back where it belongs: **in the code**. The model does
the one thing it is genuinely good at — turning messy human speech into intent —
and nothing else. It never holds the cart, never invents a menu item, and never
reaches the kitchen without a spoken confirmation.

**Core belief:** a language model is a great waiter and a terrible order pad.

---

## The One Load-Bearing Idea

**The order is a state machine owned by the code. The model only speaks.**

- There is exactly one `Order` object per conversation, held by the runtime.
- The model cannot write to it directly. It can only call tools that request a
  transition, and every transition is validated before it is applied.
- Every item code is validated against the **live menu**. An unknown code is a
  tool error carrying candidate matches — never a silent guess, never a fallback
  to a hardcoded list.
- `submit_order` is the only call that reaches the network as a write, and it is
  legal in exactly one state: `CONFIRMED`. The only way into `CONFIRMED` is a
  read-back the customer answered yes to.
- The same core serves every channel. A transport carries words in and words
  out; it owns no order logic whatsoever.

This one rule replaces prompt-engineering the model into good behaviour. If the
model misbehaves, the state machine refuses — and the refusal is a tool result
the model must deal with in front of the customer.

---

## Scope

### In

- **Two transports over one core:**
  - `cli` — interactive terminal chat.
  - `web` — local FastAPI server on port 8888, browser chat UI, streaming the
    agent's intermediate steps as newline-delimited JSON so tool calls and tool
    results are visible and not just the final answer.
- **Speech on the web transport**, served by a self-hosted CPU-only speech
  container over HTTP. See *Speech*.
- **Languages:** German and English. The agent answers in the language the
  customer used, per turn, without being told to switch.
- **Menu, cart, customer, submit.** The full happy path plus correction
  ("no, make that three"), removal, and abandonment.
- **The success moment:** the order appears in the PizzaSim dashboard under the
  configured pizzeria, with the right customer, items and quantities.
- **Deterministic tests** that run with no network and no LLM.
- **Structured logging** of every turn: user text, model tool calls, tool
  results, state transitions. One line per event, JSON, to a file.

### Out (explicitly)

- Payment, pricing totals, delivery routing, ETA prediction of our own.
- Accounts, auth, sessions surviving a process restart.
- Modifying or cancelling an order after it was submitted.
- Switching pizzeria at runtime — one process serves one `PIZZERIA_ID`.
- Any regex or keyword parser that produces an order without the model.
  See **Anti-patterns**; this is not a style preference, it is a hard ban.
- Reading the whole menu aloud when the answer will be spoken.

 succeeded in 280ms:
OpenAI Codex v0.143.0
--------
workdir: /home/rob/bpm-pizza-vibecoding-solution
model: gpt-5.4
provider: openai
approval: never
sandbox: read-only
reasoning effort: medium
reasoning summaries: none
session id: 019fb8fd-0481-7041-b49f-c9ab1a56622b
--------
user
You are an independent reviewer for the repository in the current working directory. You are read-only; you never write code. Two roles in one pass:
1. Devil's advocate: attack the implementation — bugs, gaps, missing error cases, spec violations, divergence from the approved plan.
2. Judge: score against the fixed rubric.

Task: Review the IMPLEMENTATION (stage 2) against SPEC.md (source of truth) and PLAN.md (the approved stage-1 plan, 24/25 APPROVED in reviews/round3-plan.md). The implementation is: core/ (order, state, menu, pizzasim, tools, agent), channels/ (cli.py, web.py, static/), prompts/, tests/ (state, tools, transcripts + fixtures), README.md, .env.example, requirements.txt.

Facts you cannot observe from the files, all demonstrated live before this review: the full deterministic suite passes (67 passed, 1 skipped opt-in live test); the web channel started with SPEECH_URL unset (speech:false, mic not rendered) and placed a real order end to end via the real gateway (read_back -> confirm_order(revision) -> submit_order -> order_id 3fe1deaa-... visible in the pizzeria's order list); a missing required env var exits before the first turn naming the variable and file. You may run the test suite yourself if your sandbox permits; otherwise judge from the code.

Scope notes: tests/fixtures/*.json are recorded real API responses (UUIDs in them are recorded data, not hardcoded config). The venv/ and logs/ directories are gitignored runtime artifacts, out of scope.

Output MUST end with exactly this block (numbers 1-5, 5 best):
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
Using `using-superpowers` first to load the required workflow, then I’ll inspect `SPEC.md`, `PLAN.md`, and the implementation files to review against the approved plan and rubric.
exec
/bin/bash -lc "sed -n '1,220p' /home/rob/.agents/skills/using-superpowers/SKILL.md" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 125ms:
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

codex
I’m pulling the Codex-specific skill instructions next, then I’ll read the spec, approved plan, and the review target files in parallel.
exec
/bin/bash -lc "sed -n '1,240p' /home/rob/.agents/skills/using-superpowers/references/codex-tools.md" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 0ms:
## Subagent dispatch requires multi-agent support

Add to your Codex config (`~/.codex/config.toml`):

```toml
[features]
multi_agent = true
```

This enables `spawn_agent`, `wait_agent`, and `close_agent` for skills like `dispatching-parallel-agents` and `subagent-driven-development`. When using subagent-driven-development, close reviewer subagents when their review returns. Keep each implementer subagent open until its task's review passes — the fix loop resumes the implementer — then close it. If your harness cannot send another message to a spawned agent, dispatch each fix round as a fresh implementer carrying the brief, the report file, and the findings.

## Environment Detection

Skills that create worktrees or finish branches should detect their
environment with read-only git commands before proceeding:

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
BRANCH=$(git branch --show-current)
```

- `GIT_DIR != GIT_COMMON` → already in a linked worktree (skip creation)
- `BRANCH` empty → detached HEAD (cannot branch/push/PR from sandbox)

See `using-git-worktrees` Step 0 and `finishing-a-development-branch`
Step 1 for how each skill uses these signals.

## Codex App Finishing

When the sandbox blocks branch/push operations (detached HEAD in an
externally managed worktree), the agent commits all work and informs
the user to use the App's native controls:

- **"Create branch"** — names the branch, then commit/push/PR via App UI
- **"Hand off to local"** — transfers work to the user's local checkout

The agent can still run tests, stage files, and output suggested branch
names, commit messages, and PR descriptions for the user to copy.

exec
/bin/bash -lc "pwd && rg --files -g 'SPEC.md' -g 'PLAN.md' -g 'README.md' -g '.env.example' -g 'requirements.txt' -g 'reviews/**' -g 'core/**' -g 'channels/**' -g 'prompts/**' -g 'tests/**'" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 130ms:
requirements.txt
PLAN.md
.env.example
README.md
SPEC.md
core/tools.py
core/order.py
core/__pycache__/menu.cpython-313.pyc
core/__pycache__/agent.cpython-313.pyc
core/__pycache__/pizzasim.cpython-313.pyc
core/__pycache__/tools.cpython-313.pyc
core/__pycache__/state.cpython-313.pyc
core/__pycache__/order.cpython-313.pyc
core/__pycache__/__init__.cpython-313.pyc
core/agent.py
core/pizzasim.py
core/menu.py
core/__init__.py
core/state.py
channels/__pycache__/web.cpython-313.pyc
channels/__pycache__/__init__.cpython-313.pyc
channels/__pycache__/cli.cpython-313.pyc
channels/__init__.py
channels/web.py
channels/cli.py
channels/static/index.html
channels/static/style.css
channels/static/app.js
prompts/system.de.md
prompts/system.en.md
tests/__pycache__/test_tools.cpython-313-pytest-9.1.1.pyc
tests/__pycache__/__init__.cpython-313.pyc
tests/__pycache__/test_transcripts.cpython-313-pytest-9.1.1.pyc
tests/__pycache__/test_state.cpython-313-pytest-9.1.1.pyc
tests/__init__.py
tests/test_tools.py
tests/test_state.py
tests/test_transcripts.py
tests/fixtures/menu.json
tests/fixtures/order_created.json
tests/fixtures/pizzerias.json
tests/fixtures/orders_list.json
tests/fixtures/location.json
tests/fixtures/error_422.json
tests/transcripts/unknown_item.json
tests/transcripts/mind_change.json
tests/transcripts/submit_timeout.json
tests/transcripts/happy_path.json
tests/transcripts/correction.json
reviews/scores.md
reviews/round1-plan.md
reviews/round4-impl.md
reviews/round3-plan.md
reviews/round2-plan.md

Setting a short review workflow: read the source-of-truth docs first, inspect implementation areas against them, then produce findings and rubric scores.
  → Read SPEC.md, PLAN.md, and approved-plan review context
  • Inspect implementation files and tests against spec/plan requirements
  • Draft findings, rubric scores, and verdict
exec
/bin/bash -lc "sed -n '1,260p' SPEC.md" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 0ms:
# PizzaSim Ordering Agent — Specification

> Hand this to a coding agent as the entire task:
> `FOLLOW INSTRUCTIONS PRECISELY AT "SPEC.MD"`.
> This file is the source of truth for what the agent is. Everything else in the
> repo — code, tests, prompts, tickets — derives from it.

---

## Where this format comes from

The **shape** of this document is not ours. It is borrowed from Cedric Mössner —
**The Morpheus** ([youtube.com/@TheMorpheusTutorials](https://www.youtube.com/@TheMorpheusTutorials)),
who writes exactly one `SPEC.md` per project and hands the identical file to every
new model in order to compare them. The prompt he sends alongside it is a single
line — `FOLLOW INSTRUCTIONS PRECISELY AT "SPEC.MD"` — which is why that line, and
not a long prompt, stands at the top of this file.

The sections adopted from his specs: *Soul*, *The One Load-Bearing Idea*, hard
*Scope In / Out*, an explicit autonomy clause, work *in passes* with verification
after each, a file-level *Deliverables* list, *Decisions Locked / Deferred*, and
the one-hour *ticket sizing rules*.

Reference specs:

- [github.com/TheMorpheus407/morphcook](https://github.com/TheMorpheus407/morphcook)
  — offline Flutter recipe app; one spec, seven model implementations.
- [github.com/TheMorpheus407/hogwarts-blender-benchmark](https://github.com/TheMorpheus407/hogwarts-blender-benchmark)
  — fully procedural Blender build; `prompt.txt` plus `SPEC.md`.

The content below is ours. The form is his — with thanks.

---

## Soul

Ordering food by phone works because the person on the other end keeps the order
in their head, reads it back to you, and only then walks to the kitchen. Nothing
is cooked before you said yes.

Most LLM ordering demos invert this. The model holds the order in its context,
guesses item names that sound close enough, and fires the write call the moment
it feels confident. It works in the demo and fails on the fourth turn, in a noisy
room, when the customer changes their mind.

This agent puts the order back where it belongs: **in the code**. The model does
the one thing it is genuinely good at — turning messy human speech into intent —

  ✓ Read SPEC.md, PLAN.md, and prior review docs to extract required behavior and prior mandatory fixes
  → Inspect implementation files in core/, channels/, prompts/, README.md, .env.example, requirements.txt for compliance and regressions
  • Inspect tests for coverage of required behavior, especially round-1 fixes and spec-critical flows
  • Produce findings ordered by severity and score against the rubric
codex
I’ve confirmed the plan-side requirements. Now I’m tracing the code paths that correspond to the four mandatory round-1 fixes, then I’ll check for broader spec and plan divergence.
exec
/bin/bash -lc "sed -n '1,260p' core/tools.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' core/state.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,200p' requirements.txt" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,280p' core/agent.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,280p' channels/web.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' tests/test_state.py" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 359ms:
"""State machine: every Order mutation goes through here.

Illegal transitions raise TransitionError with a typed code and a speakable
message. Messages are written to be said to the customer as-is.
"""
from __future__ import annotations

import time

from .order import Customer, Item, Order, State


class TransitionError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


def _reject_closed(order: Order) -> None:
    if order.state is State.SUBMITTED:
        raise TransitionError(
            "order_closed",
            "That order is already on its way to the kitchen and can't be "
            "changed. I can take a new order if you like.",
        )


def _recompute(order: Order) -> None:
    """Derived-state rule after any legal mutation (demotes CONFIRMED)."""
    order.revision += 1
    if not order.items:
        order.state = State.EMPTY
    elif order.customer is None:
        order.state = State.COLLECTING
    else:
        order.state = State.READY


def add_items(order: Order, items: list[Item]) -> None:
    _reject_closed(order)
    for new in items:
        for line in order.items:
            if line.line_key() == new.line_key():
                line.qty += new.qty
                break
        else:
            order.items.append(new)
    _recompute(order)


def remove_item(order: Order, type_: str, code: str, qty: int | None) -> None:
    """The spec fixes remove_item's parameters to (type, code, qty), so a
    basket holding the same (type, code) with different extras needs
    deterministic semantics: without qty every matching line goes; with qty
    the most recently added matching line is reduced. The full snapshot in
    the result lets the model repair anything else by remove + re-add."""
    _reject_closed(order)
    if not order.items:
        raise TransitionError("empty_basket", "Your basket is already empty.")
    lines = [i for i in order.items if i.type == type_ and i.code == code]
    if not lines:
        raise TransitionError(
            "not_in_basket", "That item isn't in your basket."
        )
    if qty is None:
        for line in lines:
            order.items.remove(line)
    else:
        line = lines[-1]
        if qty >= line.qty:
            order.items.remove(line)
        else:
            line.qty -= qty
    _recompute(order)


def set_customer(order: Order, customer: Customer) -> None:
    _reject_closed(order)
    order.customer = customer
    _recompute(order)


def read_back(order: Order) -> None:
    _reject_closed(order)
    if order.state is State.EMPTY:
        raise TransitionError(
            "empty_basket", "There's nothing in the basket yet."
        )
    if order.state is State.COLLECTING:
        raise TransitionError(
            "invalid_state",
            "I still need a name for the order before I can read it back.",
        )
    order.read_back_revision = order.revision


def confirm(order: Order, revision: int) -> None:
    _reject_closed(order)
    if order.state is not State.READY:
        if order.state is State.CONFIRMED:
            raise TransitionError(
                "invalid_state", "The order is already confirmed."
            )
        raise TransitionError(
            "invalid_state",
            "The order isn't complete yet, so it can't be confirmed.",
        )
    if revision != order.revision:
        raise TransitionError(
            "stale_revision",
            "The order changed since it was last read back — let me read it "
            "back again.",
        )
    if order.read_back_revision != order.revision:
        raise TransitionError(
            "read_back_required",
            "Let me read the order back to you first.",
        )
    order.state = State.CONFIRMED


def begin_submit(order: Order) -> None:
    """Guard + bookkeeping before the submit POST. No state change."""
    if order.state is State.SUBMITTED:
        _reject_closed(order)
    if order.state is not State.CONFIRMED:
        raise TransitionError(
            "invalid_state",
            "The order hasn't been confirmed yet."
            if order.items
            else "What can I get you?",
        )
    if order.submit_attempted_at is None:
        order.submit_attempted_at = time.time()


def mark_submitted(order: Order, result: dict) -> None:
    order.result = result
    order.submit_unknown = False
    order.state = State.SUBMITTED

 succeeded in 406ms:
"""The eight tool schemas the model sees, plus dispatch.

Success results always embed the full state snapshot; failures are
{"error": {"code", "message", "candidates"}} with a speakable message.
"""
from __future__ import annotations

import time

from . import state
from .menu import Menu, MenuError
from .order import Customer, Item, Order
from .pizzasim import (
    ApiTimeout,
    AuthError,
    PizzaSim,
    PizzaSimError,
    ServerError,
    ValidationError,
)

_ITEM_SCHEMA = {
    "type": "object",
    "properties": {
        "type": {"type": "string", "enum": ["pizza", "pasta"]},
        "code": {"type": "string"},
        "qty": {"type": "integer", "minimum": 1},
        "extras": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["type", "code", "qty"],
}

TOOL_SCHEMAS = [
    {"name": "get_menu",
     "description": "The menu: pizzas and pasta with codes and display "
                    "names, and the available extra toppings.",
     "parameters": {"type": "object", "properties": {}}},
    {"name": "add_items",
     "description": "Add items to the basket. Codes must come from "
                    "get_menu. Rejects the whole call if any item or extra "
                    "is unknown.",
     "parameters": {"type": "object",
                    "properties": {"items": {"type": "array",
                                             "items": _ITEM_SCHEMA}},
                    "required": ["items"]}},
    {"name": "remove_item",
     "description": "Remove an item line (or reduce its quantity when qty "
                    "is given).",
     "parameters": {"type": "object",
                    "properties": {
                        "type": {"type": "string",
                                 "enum": ["pizza", "pasta"]},
                        "code": {"type": "string"},
                        "qty": {"type": "integer", "minimum": 1}},
                    "required": ["type", "code"]}},
    {"name": "set_customer",
     "description": "Store the customer's first name and, optionally, "
                    "street.",
     "parameters": {"type": "object",
                    "properties": {
                        "first_name": {"type": "string", "minLength": 1},
                        "street_one": {"type": "string"}},
                    "required": ["first_name"]}},
    {"name": "read_back",
     "description": "The complete order as it stands — read this back to "
                    "the customer before asking for confirmation.",
     "parameters": {"type": "object", "properties": {}}},
    {"name": "confirm_order",
     "description": "Confirm the order after the customer said yes to the "
                    "read-back. revision must be the revision that was "
                    "read back.",
     "parameters": {"type": "object",
                    "properties": {"revision": {"type": "integer"}},
                    "required": ["revision"]}},
    {"name": "submit_order",
     "description": "Send the confirmed order to the kitchen. Only legal "
                    "after confirm_order.",
     "parameters": {"type": "object", "properties": {}}},
    {"name": "check_street",
     "description": "Rough plausibility check of a street name. Not a "
                    "deliverability check — never claim the address was "
                    "verified.",
     "parameters": {"type": "object",
                    "properties": {"street": {"type": "string"}},
                    "required": ["street"]}},
]


def openai_tools() -> list[dict]:
    return [{"type": "function", "function": schema}
            for schema in TOOL_SCHEMAS]


def _error(code: str, message: str, candidates: list | None = None) -> dict:
    return {"error": {"code": code, "message": message,
                      "candidates": candidates or []}}


def _int_qty(value) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise MenuError(
            "invalid_quantity",
            "I need the quantity as a plain number, please.",
            [],
        )
    return value


def dispatch(order: Order, menu: Menu, client: PizzaSim,
             name: str, args: dict) -> dict:
    """Execute one tool call. Never raises — every failure is a tool
    result the model must deal with in front of the customer."""
    try:
        return _dispatch(order, menu, client, name, args)
    except MenuError as exc:
        return _error(exc.code, exc.message, exc.candidates)
    except state.TransitionError as exc:
        return _error(exc.code, exc.message)
    except AuthError:
        return _error("api_unavailable",
                      "I can't reach the kitchen system right now.")
    except ApiTimeout:
        return _error("api_unavailable",
                      "The kitchen system isn't answering right now.")
    except PizzaSimError:
        return _error("api_unavailable",
                      "The kitchen system isn't answering right now.")


def _dispatch(order: Order, menu: Menu, client: PizzaSim,
              name: str, args: dict) -> dict:
    if name == "get_menu":
        return {"menu": menu.as_tool_result(), "snapshot": order.snapshot()}

    if name == "add_items":
        items = []
        for raw in args.get("items", []):
            extras = raw.get("extras") or []
            menu.validate_extras(extras)
            items.append(Item(
                type=raw.get("type", ""),
                code=raw.get("code", ""),
                name=menu.display_name(raw.get("type", ""),
                                       raw.get("code", "")),
                qty=_int_qty(raw.get("qty")),
                extras=extras,
            ))  # any failure above rejects the whole call — atomic
        if not items:
            return _error("invalid_quantity", "What can I get you?")
        state.add_items(order, items)
        return {"snapshot": order.snapshot()}

    if name == "remove_item":
        qty = args.get("qty")
        state.remove_item(order, args.get("type", ""), args.get("code", ""),
                          None if qty is None else _int_qty(qty))
        return {"snapshot": order.snapshot()}

    if name == "set_customer":
        first_name = (args.get("first_name") or "").strip()
        if not first_name:
            return _error("invalid_state", "I still need a name.")
        customer = Customer(first_name, args.get("street_one") or None)
        state.set_customer(order, customer)
        return {"customer": customer.as_dict(),
                "snapshot": order.snapshot()}

    if name == "read_back":
        state.read_back(order)
        return {"snapshot": order.snapshot()}

    if name == "confirm_order":
        revision = args.get("revision")
        if isinstance(revision, bool) or not isinstance(revision, int):
            return _error("stale_revision",
                          "The order changed — let me read it back again.")
        state.confirm(order, revision)
        return {"snapshot": order.snapshot()}

    if name == "submit_order":
        return _submit(order, client)

    if name == "check_street":
        result = client.check_street(args.get("street", ""))
        return {"street": result.get("street", ""),
                "deliverable": bool(result.get("deliverable")),
                "snapshot": order.snapshot()}

    return _error("unknown_tool", "Something went wrong on my side.")


_UNSURE = ("I'm not sure that went through — let me check before I try "
           "again.")


def _submit(order: Order, client: PizzaSim) -> dict:
    state.begin_submit(order)

    if order.submit_unknown:
        # A previous attempt timed out: verify against the order list
        # before any retry — a blind retry doubles a real order.
        try:
            existing = client.list_orders()
        except PizzaSimError:
            return _error("submit_unknown", _UNSURE)
        cutoff = order.submit_attempted_at - 60  # clock-skew allowance
        matches = [
            o for o in existing
            if o.get("first_name") == order.customer.first_name
            and o.get("created_at", 0) >= cutoff
        ]
        if matches:
            found = max(matches, key=lambda o: o.get("created_at", 0))
            eta = max(0, int(found.get("ready_at", 0) - time.time()))
            state.mark_submitted(order, {
                "order_id": found["id"],
                "status": found.get("status", "ordered"),
                "eta_seconds": eta,
            })
            return {**order.result, "snapshot": order.snapshot()}
        # verified absent → exactly one real retry, below

    customer = order.customer.as_dict()
    if customer.get("street_one") is None:
        customer.pop("street_one")
    items = [{"type": i.type, "code": i.code, "qty": i.qty,
              "extras": list(i.extras)} for i in order.items]
    try:
        result = client.submit_order(customer, items)
    except ValidationError as exc:
        return _error("submit_failed",
                      "The kitchen rejected part of the order: "
                      + "; ".join(exc.details))
    except AuthError:
        return _error("api_unavailable",
                      "I can't reach the kitchen system right now.")
    except (ApiTimeout, ServerError):
        order.submit_unknown = True
        return _error("submit_unknown", _UNSURE)

    state.mark_submitted(order, {
        "order_id": result["order_id"],
        "status": result["status"],
        "eta_seconds": result["eta_seconds"],
    })
    return {**order.result, "snapshot": order.snapshot()}

 succeeded in 410ms:
fastapi==0.141.1
httpx==0.28.1
pytest==9.1.1
python-multipart==0.0.32
uvicorn==0.52.0

 succeeded in 374ms:
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
    app.state.speech = Speech()


@app.get("/")
def index():
    return FileResponse(STATIC / "index.html")


@app.get("/config")
def ui_config():
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

    events: queue.Queue = queue.Queue()

    def run() -> None:
        try:
            app.state.agent.run_turn(session, text, events.put)
        finally:
            events.put({"type": "done",
                        "state": session.order.snapshot()})
            events.put(None)

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

 succeeded in 399ms:
"""Model loop: prompt assembly, chat-completions calls, tool dispatch,
JSONL event logging. The model only speaks; the order lives in core."""
from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path

import httpx

from . import tools
from .menu import Menu
from .order import Order
from .pizzasim import PizzaSim, optional_env, require_env

PROMPT_DIR = Path(__file__).resolve().parent.parent / "prompts"
LOG_DIR = Path("logs")
MAX_TOOL_ROUNDS = 8
GATEWAY_TIMEOUT = httpx.Timeout(30.0, connect=10.0)  # per approved plan

APOLOGY = {
    "de": "Entschuldigung, da ist gerade etwas schiefgegangen. "
          "Können Sie das bitte noch einmal sagen?",
    "en": "I'm sorry, something went wrong on my end just now. "
          "Could you say that again, please?",
}


class GatewayError(Exception):
    pass


@dataclass
class AgentConfig:
    url: str
    key: str
    model: str
    lang: str  # PIZZERIA_LANG: greeting language = pizzeria country

    @classmethod
    def from_env(cls) -> "AgentConfig":
        lang = require_env("PIZZERIA_LANG").lower()
        if lang not in ("de", "en"):
            raise ValueError(
                "PIZZERIA_LANG must be 'de' or 'en', got something else"
            )
        optional_env("LITELLM_PIZZA_MODEL_2")  # read; unused (single-model)
        return cls(
            url=require_env("LITELLM_PIZZA_URL").rstrip("/"),
            key=require_env("LITELLM_PIZZA_KEY"),
            model=require_env("LITELLM_PIZZA_MODEL_1"),
            lang=lang,
        )


def system_prompt(lang: str, pizzeria_name: str) -> str:
    text = (PROMPT_DIR / f"system.{lang}.md").read_text()
    return text.replace("{pizzeria_name}", pizzeria_name)


@dataclass
class Session:
    """One conversation: one Order, one immutable Menu snapshot, one
    history."""
    order: Order
    menu: Menu
    messages: list[dict]
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])

    @classmethod
    def create(cls, config: AgentConfig, menu: Menu,
               pizzeria_name: str) -> "Session":
        return cls(
            order=Order(),
            menu=menu,
            messages=[{"role": "system",
                       "content": system_prompt(config.lang,
                                                pizzeria_name)}],
        )


def log_event(session: Session, event: dict) -> None:
    """One line per event, JSON, to a file. Never carries config values."""
    LOG_DIR.mkdir(exist_ok=True)
    record = {"ts": round(time.time(), 3), "session": session.id, **event}
    with (LOG_DIR / f"agent-{session.id}.jsonl").open("a") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")


class Agent:
    def __init__(self, config: AgentConfig, client: PizzaSim,
                 chat_fn=None):
        self.config = config
        self.client = client
        # chat_fn(messages, tools) -> assistant message dict; injectable so
        # the golden transcripts run against a stub with no network.
        self._chat_fn = chat_fn or self._gateway_chat

    def _gateway_chat(self, messages: list[dict],
                      tool_schemas: list[dict]) -> dict:
        payload = {
            "model": self.config.model,
            "messages": messages,
            "tools": tool_schemas,
        }
        headers = {"Authorization": f"Bearer {self.config.key}"}
        last_exc: Exception | None = None
        for attempt in range(2):  # one retry on timeout, then abort turn
            try:
                response = httpx.post(
                    f"{self.config.url}/chat/completions",
                    json=payload, headers=headers, timeout=GATEWAY_TIMEOUT,
                )
                response.raise_for_status()
                return response.json()["choices"][0]["message"]
            except httpx.TimeoutException as exc:
                last_exc = exc
                continue
            except (httpx.HTTPError, KeyError, ValueError) as exc:
                raise GatewayError(f"gateway request failed: "
                                   f"{type(exc).__name__}") from exc
        raise GatewayError("gateway timed out twice") from last_exc

    def run_turn(self, session: Session, user_text: str | None,
                 emit=lambda event: None) -> str:
        """One customer turn: returns the assistant's final text. Every
        intermediate step goes to emit() and the JSONL log. user_text None
        is the opening turn — the agent greets first, unprompted."""

        def event(payload: dict) -> None:
            log_event(session, payload)
            emit(payload)

        if user_text is not None:
            session.messages.append({"role": "user", "content": user_text})
            event({"type": "user", "text": user_text})

        for _ in range(MAX_TOOL_ROUNDS):
            try:
                message = self._chat_fn(session.messages,
                                        tools.openai_tools())
            except GatewayError as exc:
                event({"type": "error", "error": str(exc)})
                apology = APOLOGY[self.config.lang]
                session.messages.append({"role": "assistant",
                                         "content": apology})
                return apology

            tool_calls = message.get("tool_calls")
            if not tool_calls:
                text = message.get("content") or ""
                session.messages.append({"role": "assistant",
                                         "content": text})
                event({"type": "assistant", "text": text})
                return text

            session.messages.append({
                "role": "assistant",
                "content": message.get("content"),
                "tool_calls": tool_calls,
            })
            for call in tool_calls:
                name = call["function"]["name"]
                try:
                    args = json.loads(call["function"]["arguments"] or "{}")
                except ValueError:
                    args = {}
                event({"type": "tool_call", "tool": name, "args": args})
                result = tools.dispatch(session.order, session.menu,
                                        self.client, name, args)
                event({"type": "tool_result", "tool": name,
                       "result": result})
                event({"type": "state",
                       "state": session.order.state.value,
                       "revision": session.order.revision})
                session.messages.append({
                    "role": "tool",
                    "tool_call_id": call.get("id", name),
                    "content": json.dumps(result, ensure_ascii=False),
                })

        event({"type": "error", "error": "tool loop guard exceeded"})
        apology = APOLOGY[self.config.lang]
        session.messages.append({"role": "assistant", "content": apology})
        return apology


def startup(config: AgentConfig) -> tuple[PizzaSim, str, Menu]:
    """The one startup sequence (PLAN): env → pizzeria check → menu.
    Raises before the first turn on any failure."""
    client = PizzaSim.from_env()
    pizzeria_name = client.pizzeria_name()
    menu = Menu(client.get_menu())
    return client, pizzeria_name, menu

 succeeded in 367ms:
"""State machine, exhaustively: every ✗ cell of the transition table in
PLAN.md and every SPEC invariant 1-4 (invariant 5, menu validation, lives in
test_tools.py)."""
import pytest

from core.order import Customer, Item, Order, State
from core import state


def item(code="margherita", type_="pizza", qty=1, extras=None):
    return Item(type=type_, code=code, name=code.title(), qty=qty,
                extras=extras or [])


def order_in(target: State) -> Order:
    o = Order()
    if target is State.EMPTY:
        return o
    state.add_items(o, [item()])
    if target is State.COLLECTING:
        return o
    state.set_customer(o, Customer("Marco", "via Roma"))
    if target is State.READY:
        return o
    state.read_back(o)
    state.confirm(o, o.revision)
    if target is State.CONFIRMED:
        return o
    state.begin_submit(o)
    state.mark_submitted(o, {"order_id": "x", "status": "ordered",
                             "eta_seconds": 600})
    return o


def expect(code):
    return pytest.raises(state.TransitionError, match="")


# --- happy path -----------------------------------------------------------

def test_full_happy_path():
    o = Order()
    assert o.state is State.EMPTY
    state.add_items(o, [item(qty=2)])
    assert o.state is State.COLLECTING
    state.set_customer(o, Customer("Marco", "via Roma"))
    assert o.state is State.READY
    state.read_back(o)
    state.confirm(o, o.revision)
    assert o.state is State.CONFIRMED
    state.begin_submit(o)
    state.mark_submitted(o, {"order_id": "abc", "status": "ordered",
                             "eta_seconds": 90})
    assert o.state is State.SUBMITTED
    assert o.result["order_id"] == "abc"


def test_customer_before_items_is_legal_and_stays_empty():
    o = Order()
    state.set_customer(o, Customer("Anna"))
    assert o.state is State.EMPTY
    state.add_items(o, [item()])
    assert o.state is State.READY  # customer already known


# --- illegal cells, one test per ✗ ---------------------------------------

@pytest.mark.parametrize("mutate", [
    lambda o: state.add_items(o, [item()]),
    lambda o: state.remove_item(o, "pizza", "margherita", None),
    lambda o: state.set_customer(o, Customer("Eve")),
    lambda o: state.read_back(o),
    lambda o: state.confirm(o, o.revision),
    lambda o: state.begin_submit(o),
])
def test_submitted_is_terminal(mutate):
    o = order_in(State.SUBMITTED)
    with pytest.raises(state.TransitionError) as e:
        mutate(o)
    assert e.value.code == "order_closed"


def test_remove_from_empty():
    with pytest.raises(state.TransitionError) as e:
        state.remove_item(order_in(State.EMPTY), "pizza", "margherita", None)
    assert e.value.code == "empty_basket"


def test_read_back_empty():
    with pytest.raises(state.TransitionError) as e:
        state.read_back(order_in(State.EMPTY))
    assert e.value.code == "empty_basket"


def test_read_back_collecting_needs_customer():
    with pytest.raises(state.TransitionError) as e:
        state.read_back(order_in(State.COLLECTING))
    assert e.value.code == "invalid_state"


@pytest.mark.parametrize("st", [State.EMPTY, State.COLLECTING])
def test_confirm_illegal_states(st):
    o = order_in(st)
    with pytest.raises(state.TransitionError) as e:
        state.confirm(o, o.revision)
    assert e.value.code == "invalid_state"


def test_confirm_when_already_confirmed():
    o = order_in(State.CONFIRMED)
    with pytest.raises(state.TransitionError) as e:
        state.confirm(o, o.revision)
    assert e.value.code == "invalid_state"


@pytest.mark.parametrize("st", [State.EMPTY, State.COLLECTING, State.READY])
def test_submit_outside_confirmed(st):
    """Invariant 1: submit outside CONFIRMED is refused (incl. empty)."""
    o = order_in(st)
    with pytest.raises(state.TransitionError) as e:
        state.begin_submit(o)
    assert e.value.code == "invalid_state"


def test_remove_unknown_line():
    o = order_in(State.COLLECTING)
    with pytest.raises(state.TransitionError) as e:
        state.remove_item(o, "pasta", "pesto", None)
    assert e.value.code == "not_in_basket"


# --- invariant 2: mutation after CONFIRMED demotes ------------------------

def test_add_after_confirmed_demotes_to_ready():
    o = order_in(State.CONFIRMED)
    state.add_items(o, [item("funghi")])
    assert o.state is State.READY


def test_remove_after_confirmed_demotes():
    o = order_in(State.CONFIRMED)
    state.remove_item(o, "pizza", "margherita", None)
    assert o.state is State.EMPTY  # last item gone, customer kept


def test_set_customer_after_confirmed_demotes():
    o = order_in(State.CONFIRMED)
    state.set_customer(o, Customer("Mario"))
    assert o.state is State.READY


def test_confirmation_does_not_survive_demotion():
    """A confirmation applies to the basket that was read back."""
    o = order_in(State.CONFIRMED)
    state.add_items(o, [item("funghi")])
    with pytest.raises(state.TransitionError):
        state.begin_submit(o)


# --- invariant 3: confirm tied to read-back + revision --------------------

def test_confirm_without_read_back():
    o = order_in(State.READY)
    with pytest.raises(state.TransitionError) as e:
        state.confirm(o, o.revision)
    assert e.value.code == "read_back_required"


def test_confirm_with_stale_revision():
    o = order_in(State.READY)
    state.read_back(o)
    stale = o.revision
    state.add_items(o, [item("funghi")])
    with pytest.raises(state.TransitionError) as e:
        state.confirm(o, stale)
    assert e.value.code == "stale_revision"


def test_read_back_of_old_revision_does_not_allow_confirm():
    o = order_in(State.READY)
    state.read_back(o)
    state.add_items(o, [item("funghi")])  # bumps revision
    with pytest.raises(state.TransitionError) as e:
        state.confirm(o, o.revision)
    assert e.value.code == "read_back_required"


# --- basket mechanics -----------------------------------------------------

def test_revision_increments_on_every_mutation():
    o = Order()
    r0 = o.revision
    state.add_items(o, [item()])
    state.set_customer(o, Customer("A"))
    state.remove_item(o, "pizza", "margherita", None)
    assert o.revision == r0 + 3


def test_merge_same_line():
    o = Order()
    state.add_items(o, [item(qty=1)])
    state.add_items(o, [item(qty=2)])
    assert len(o.items) == 1 and o.items[0].qty == 3


def test_same_code_different_extras_is_separate_line():
    o = Order()
    state.add_items(o, [item(qty=1)])
    state.add_items(o, [item(qty=1, extras=["mushrooms"])])
    assert len(o.items) == 2


def test_partial_remove():
    o = Order()
    state.add_items(o, [item(qty=3)])
    state.remove_item(o, "pizza", "margherita", 1)
    assert o.items[0].qty == 2
    state.remove_item(o, "pizza", "margherita", 5)  # >= qty removes line
    assert o.items == []
    assert o.state is State.EMPTY


def test_remove_to_empty_and_readd():
    o = order_in(State.READY)
    state.remove_item(o, "pizza", "margherita", None)
    assert o.state is State.EMPTY
    state.add_items(o, [item("funghi")])
    assert o.state is State.READY  # customer survived


def test_type_and_code_key_removal():
    """tonno exists as pizza and pasta — removal must key on (type, code)."""
    o = Order()
    state.add_items(o, [item("tonno", "pizza"), item("tonno", "pasta")])
    state.remove_item(o, "pasta", "tonno", None)
    assert [i.type for i in o.items] == ["pizza"]


def test_remove_without_qty_clears_all_variants():
    """Same (type, code), different extras: no-qty removal takes them all."""
    o = Order()
    state.add_items(o, [item(qty=1), item(qty=1, extras=["mushrooms"])])
    state.remove_item(o, "pizza", "margherita", None)
    assert o.items == []


def test_remove_with_qty_reduces_most_recent_variant():
    o = Order()
    state.add_items(o, [item(qty=2), item(qty=2, extras=["mushrooms"])])
    state.remove_item(o, "pizza", "margherita", 1)
    assert [(i.extras, i.qty) for i in o.items] == \
        [([], 2), (["mushrooms"], 1)]


def test_submit_attempt_timestamp_set_once():
    o = order_in(State.CONFIRMED)
    state.begin_submit(o)
    first = o.submit_attempted_at
    assert first is not None
    state.begin_submit(o)

exec
/bin/bash -lc "sed -n '261,520p' tests/test_state.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' channels/cli.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,320p' core/menu.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' tests/test_transcripts.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' core/order.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,340p' core/pizzasim.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' tests/test_tools.py" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 423ms:
    assert o.submit_attempted_at == first

 succeeded in 486ms:
"""Order data: items, customer, revision, submit bookkeeping. Pure data."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class State(str, Enum):
    EMPTY = "EMPTY"
    COLLECTING = "COLLECTING"
    READY = "READY"
    CONFIRMED = "CONFIRMED"
    SUBMITTED = "SUBMITTED"


@dataclass
class Item:
    type: str  # "pizza" | "pasta"
    code: str
    name: str
    qty: int
    extras: list[str] = field(default_factory=list)

    def line_key(self) -> tuple:
        return (self.type, self.code, tuple(sorted(self.extras)))


@dataclass
class Customer:
    first_name: str
    street_one: str | None = None

    def as_dict(self) -> dict:
        return {"first_name": self.first_name, "street_one": self.street_one}


@dataclass
class Order:
    items: list[Item] = field(default_factory=list)
    customer: Customer | None = None
    revision: int = 0
    read_back_revision: int | None = None
    state: State = State.EMPTY
    submit_attempted_at: float | None = None
    submit_unknown: bool = False
    result: dict | None = None  # order_id, status, eta_seconds after submit

    def snapshot(self) -> dict:
        """Full current state — every successful tool result embeds this."""
        return {
            "state": self.state.value,
            "revision": self.revision,
            "items": [
                {
                    "type": i.type,
                    "code": i.code,
                    "name": i.name,
                    "qty": i.qty,
                    "extras": list(i.extras),
                }
                for i in self.items
            ],
            "customer": self.customer.as_dict() if self.customer else None,
            "read_back_done": self.read_back_revision == self.revision,
        }

 succeeded in 573ms:
"""Interactive terminal chat over the core. A transport only: words in,
words out, no order logic.

Run:  python -m channels.cli [--verbose]
"""
from __future__ import annotations

import argparse
import sys

from core.agent import Agent, AgentConfig, Session, startup
from core.pizzasim import ConfigError, PizzaSimError


def make_emit(verbose: bool):
    def emit(event: dict) -> None:
        if not verbose:
            return
        kind = event["type"]
        if kind == "tool_call":
            print(f"  ⚙ {event['tool']} {event['args']}", file=sys.stderr)
        elif kind == "tool_result":
            print(f"  ← {event['result']}", file=sys.stderr)
        elif kind == "state":
            print(f"  ▸ {event['state']} r{event['revision']}",
                  file=sys.stderr)
    return emit


def main() -> int:
    parser = argparse.ArgumentParser(description="PizzaSim ordering agent")
    parser.add_argument("--verbose", action="store_true",
                        help="show tool calls and state transitions")
    args = parser.parse_args()

    try:
        config = AgentConfig.from_env()
        client, pizzeria_name, menu = startup(config)
    except (ConfigError, ValueError) as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 1
    except PizzaSimError as exc:
        print(f"Startup check against PizzaSim failed: {exc}\n"
              "We're not taking orders right now.", file=sys.stderr)
        return 1

    agent = Agent(config, client)
    session = Session.create(config, menu, pizzeria_name)
    emit = make_emit(args.verbose)

    print(f"[{pizzeria_name} — type your order, Ctrl-D to hang up]")
    print(agent.run_turn(session, None, emit))  # agent greets first
    while True:
        try:
            text = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not text:
            continue
        print(agent.run_turn(session, text, emit))


if __name__ == "__main__":
    sys.exit(main())

 succeeded in 569ms:
"""Golden transcripts: five scripted conversations run through the real
agent loop against a stub model that replays fixed tool calls. Asserts the
final state and the calls actually made. No network, no LLM."""
import json
import time
from pathlib import Path

import pytest

from core.agent import Agent, AgentConfig, Session
from core.menu import Menu
from core.order import Order
from core.pizzasim import ApiTimeout

FIXTURES = Path(__file__).parent / "fixtures"
TRANSCRIPTS = sorted((Path(__file__).parent / "transcripts").glob("*.json"))


class StubModel:
    """Replays a transcript's scripted actions, one per chat call."""

    def __init__(self, turns):
        self._queues = [list(turn["script"]) for turn in turns]
        self._current = None

    def next_turn(self):
        self._current = self._queues.pop(0)

    def __call__(self, messages, tool_schemas):
        action = self._current.pop(0)
        if "tool" in action:
            assert any(t["function"]["name"] == action["tool"]
                       for t in tool_schemas), action["tool"]
            return {"tool_calls": [{
                "id": f"call-{action['tool']}",
                "function": {"name": action["tool"],
                             "arguments": json.dumps(action["args"])},
            }]}
        return {"content": action["say"]}


class ScriptedClient:
    """Fake PizzaSim: 'ok' submits succeed; 'timeout_then_recover' times
    out once, then the order shows up in the list."""

    def __init__(self, mode):
        self.mode = mode
        self.submits = 0
        self.created = json.loads((FIXTURES / "order_created.json")
                                  .read_text())

    def submit_order(self, customer, items):
        self.submits += 1
        if self.mode == "timeout_then_recover" and self.submits == 1:
            self._customer = customer
            raise ApiTimeout("simulated submit timeout")
        return self.created

    def list_orders(self):
        if self.mode == "timeout_then_recover":
            return [{"id": "recovered-1",
                     "first_name": self._customer["first_name"],
                     "created_at": int(time.time()),
                     "ready_at": int(time.time()) + 300,
                     "status": "ordered"}]
        return []

    def check_street(self, street):
        return {"street": street, "deliverable": True}


@pytest.mark.parametrize("path", TRANSCRIPTS, ids=lambda p: p.stem)
def test_golden_transcript(path):
    transcript = json.loads(path.read_text())
    stub = StubModel(transcript["turns"])
    client = ScriptedClient(transcript["fake"])
    config = AgentConfig(url="http://unused", key="unused",
                         model="stub", lang="de")
    menu = Menu(json.loads((FIXTURES / "menu.json").read_text()))
    session = Session(order=Order(), menu=menu,
                      messages=[{"role": "system", "content": "stub"}])
    agent = Agent(config, client, chat_fn=stub)

    calls, error_codes = [], []

    def emit(event):
        if event["type"] == "tool_call":
            calls.append(event["tool"])
        if event["type"] == "tool_result" and "error" in event["result"]:
            error_codes.append(event["result"]["error"]["code"])

    for turn in transcript["turns"]:
        stub.next_turn()
        final = agent.run_turn(session, turn["user"], emit)
        assert final == turn["script"][-1]["say"]

    expect = transcript["expect"]
    assert session.order.state.value == expect["state"]
    assert calls == expect["calls"]
    assert error_codes == expect["error_codes"]
    actual_items = [{"type": i.type, "code": i.code, "qty": i.qty}
                    for i in session.order.items]
    assert actual_items == expect["items"]
    if "order_id" in expect:
        assert session.order.result["order_id"] == expect["order_id"]
    if expect["state"] == "SUBMITTED":
        assert session.order.result["order_id"]


def test_five_transcripts_exist():
    assert len(TRANSCRIPTS) == 5


def test_gateway_timeout_apology():
    """Gateway timeout: one retry, then abort the turn with an apology."""
    attempts = []

    def flaky(messages, tool_schemas):
        attempts.append(1)
        from core.agent import GatewayError
        raise GatewayError("gateway timed out twice")

    config = AgentConfig(url="http://unused", key="unused",
                         model="stub", lang="en")
    menu = Menu(json.loads((FIXTURES / "menu.json").read_text()))
    session = Session(order=Order(), menu=menu,
                      messages=[{"role": "system", "content": "stub"}])
    agent = Agent(config, ScriptedClient("ok"), chat_fn=flaky)
    text = agent.run_turn(session, "hello")
    assert "sorry" in text.lower()
    assert session.order.state.value == "EMPTY"  # turn aborted cleanly

 succeeded in 587ms:
"""Immutable menu snapshot: (type, code) validation, extras validation,
candidate suggestions. One snapshot per session (SPEC invariant 5)."""
from __future__ import annotations

import difflib


class MenuError(Exception):
    def __init__(self, code: str, message: str, candidates: list[dict]):
        super().__init__(message)
        self.code = code
        self.message = message
        self.candidates = candidates


class Menu:
    def __init__(self, payload: dict):
        self._by_type: dict[str, dict[str, str]] = {
            "pizza": {p["code"]: p["name"] for p in payload["pizzas"]},
            "pasta": {p["code"]: p["name"] for p in payload["pasta"]},
        }
        self.toppings: list[str] = list(payload.get("toppings", []))

    def as_tool_result(self) -> dict:
        return {
            "pizzas": [{"code": c, "name": n}
                       for c, n in self._by_type["pizza"].items()],
            "pasta": [{"code": c, "name": n}
                      for c, n in self._by_type["pasta"].items()],
            "toppings": self.toppings,
        }

    def display_name(self, type_: str, code: str) -> str:
        """Validate (type, code); return display name or raise unknown_item
        with up to three candidates."""
        if type_ not in self._by_type:
            raise MenuError(
                "unknown_item",
                "I only have pizza and pasta on the menu.",
                self.candidates("pizza", code),
            )
        name = self._by_type[type_].get(code)
        if name is None:
            cands = self.candidates(type_, code)
            raise MenuError(
                "unknown_item",
                "I don't have that on the menu."
                + (
                    " Did you mean "
                    + " or ".join(c["name"] for c in cands)
                    + "?"
                    if cands
                    else ""
                ),
                cands,
            )
        return name

    def validate_extras(self, extras: list[str]) -> None:
        for extra in extras:
            if extra not in self.toppings:
                cands = [
                    {"type": "topping", "code": t, "name": t.replace("_", " ")}
                    for t in difflib.get_close_matches(
                        extra.lower(), self.toppings, n=3, cutoff=0.5
                    )
                ]
                raise MenuError(
                    "invalid_extra",
                    "I can't add that topping."
                    + (
                        " Did you mean "
                        + " or ".join(c["name"] for c in cands)
                        + "?"
                        if cands
                        else ""
                    ),
                    cands,
                )

    def candidates(self, type_: str, query: str) -> list[dict]:
        """Up to three close matches, same type first, other type as
        fallback so 'pizza tonno' asked as pasta still helps."""
        out: list[dict] = []
        order = [type_] + [t for t in self._by_type if t != type_]
        for t in order:
            if t not in self._by_type or len(out) >= 3:
                continue
            table = self._by_type[t]
            keys = list(table) + [n.lower() for n in table.values()]
            for match in difflib.get_close_matches(
                query.lower(), keys, n=3, cutoff=0.4
            ):
                code = next(
                    c for c, n in table.items()
                    if c == match or n.lower() == match
                )
                entry = {"type": t, "code": code, "name": table[code]}
                if entry not in out:
                    out.append(entry)
        return out[:3]

 succeeded in 552ms:
"""PizzaSim API client: httpx, explicit timeouts, typed errors.

Also owns the env-config loading shared by the whole app: process env wins,
else ~/.env if present (never written, never printed).
"""
from __future__ import annotations

import os
from pathlib import Path

import httpx

ENV_FILE = Path.home() / ".env"
_TIMEOUT = httpx.Timeout(10.0)


class ConfigError(Exception):
    pass


def _env_file_values() -> dict[str, str]:
    values: dict[str, str] = {}
    if ENV_FILE.is_file():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                values[key.strip()] = val.strip().strip('"').strip("'")
    return values


def require_env(name: str) -> str:
    value = os.environ.get(name) or _env_file_values().get(name)
    if not value:
        raise ConfigError(
            f"{name} is not set (expected in the environment or {ENV_FILE})"
        )
    return value


def optional_env(name: str) -> str | None:
    return os.environ.get(name) or _env_file_values().get(name) or None


class PizzaSimError(Exception):
    """Base for typed API errors."""


class AuthError(PizzaSimError):
    pass


class NotFoundError(PizzaSimError):
    pass


class ValidationError(PizzaSimError):
    def __init__(self, details: list[str]):
        super().__init__("; ".join(details))
        self.details = details


class ServerError(PizzaSimError):
    pass


class ApiTimeout(PizzaSimError):
    pass


def _raise_for(response: httpx.Response) -> None:
    if response.status_code in (401, 403):
        raise AuthError(f"auth rejected ({response.status_code})")
    if response.status_code == 404:
        raise NotFoundError("not found")
    if response.status_code == 422:
        try:
            details = response.json().get("details", [])
        except ValueError:
            details = []
        raise ValidationError(details or ["invalid request"])
    if response.status_code >= 500:
        raise ServerError(f"server error ({response.status_code})")
    response.raise_for_status()


class PizzaSim:
    def __init__(self, base_url: str, api_key: str, pizzeria_id: str,
                 transport: httpx.BaseTransport | None = None):
        self.pizzeria_id = pizzeria_id
        self._client = httpx.Client(
            base_url=base_url.rstrip("/"),
            headers={"X-API-Key": api_key},
            timeout=_TIMEOUT,
            transport=transport,
        )

    @classmethod
    def from_env(cls) -> "PizzaSim":
        return cls(
            require_env("PIZZASIM_URL"),
            require_env("PIZZASIM_API_KEY"),
            require_env("PIZZERIA_ID"),
        )

    def _request(self, method: str, path: str, **kw) -> dict:
        try:
            response = self._client.request(method, path, **kw)
        except httpx.TimeoutException as exc:
            raise ApiTimeout(str(exc)) from exc
        except httpx.HTTPError as exc:
            raise ServerError(str(exc)) from exc
        _raise_for(response)
        return response.json()

    def get_menu(self) -> dict:
        return self._request("GET", "/menu")

    def list_pizzerias(self) -> list[dict]:
        return self._request("GET", "/pizzerias")["pizzerias"]

    def pizzeria_name(self) -> str:
        """Startup step 2: auth + tenant check. Unknown PIZZERIA_ID is the
        404-pizzeria case — the process must refuse to start."""
        for pizzeria in self.list_pizzerias():
            if pizzeria["id"] == self.pizzeria_id:
                return pizzeria["name"]
        raise NotFoundError(
            f"pizzeria {self.pizzeria_id} not found on the PizzaSim server"
        )

    def list_orders(self) -> list[dict]:
        return self._request(
            "GET", f"/pizzerias/{self.pizzeria_id}/orders"
        )["orders"]

    def submit_order(self, customer: dict, items: list[dict]) -> dict:
        """The only network write. Returns order_id, status, eta_seconds."""
        return self._request(
            "POST",
            f"/pizzerias/{self.pizzeria_id}/orders",
            json={"customer": customer, "items": items},
        )

    def check_street(self, street: str) -> dict:
        return self._request("GET", "/location", params={"street": street})

 succeeded in 562ms:
"""Tool layer against recorded fixtures. No network, no LLM.

Includes the one opt-in live smoke test (PIZZA_LIVE_TEST=1)."""
import json
import os
import time
from pathlib import Path

import httpx
import pytest

from core import state, tools
from core.menu import Menu, MenuError
from core.order import Customer, Order, State
from core.pizzasim import (
    ApiTimeout,
    AuthError,
    NotFoundError,
    PizzaSim,
    ServerError,
    ValidationError,
)

FIXTURES = Path(__file__).parent / "fixtures"


def fixture(name):
    return json.loads((FIXTURES / name).read_text())


@pytest.fixture
def menu():
    return Menu(fixture("menu.json"))


# --- menu validation ------------------------------------------------------

def test_known_codes(menu):
    assert menu.display_name("pizza", "margherita") == "Margherita"
    assert menu.display_name("pasta", "pesto") == "Pasta Pesto"


def test_tonno_collision_is_per_type(menu):
    """Codes are unique per type, not globally."""
    assert menu.display_name("pizza", "tonno") == "Tonno"
    assert menu.display_name("pasta", "tonno") == "Pasta Tonno"


def test_unknown_code_gives_candidates(menu):
    with pytest.raises(MenuError) as e:
        menu.display_name("pizza", "margarita")  # misspelt
    assert e.value.code == "unknown_item"
    assert 1 <= len(e.value.candidates) <= 3
    assert e.value.candidates[0]["code"] == "margherita"


def test_wrong_type_falls_back_to_other_type(menu):
    with pytest.raises(MenuError) as e:
        menu.display_name("pasta", "hawaii")
    codes = [c["code"] for c in e.value.candidates]
    assert "hawaii" in codes  # found as pizza


def test_extras_controlled_vocabulary(menu):
    menu.validate_extras(["mushrooms", "pineapple"])  # ok
    with pytest.raises(MenuError) as e:
        menu.validate_extras(["unicorn_dust"])
    assert e.value.code == "invalid_extra"


# --- pizzasim client typed errors (httpx MockTransport) -------------------

def client_returning(handler):
    return PizzaSim("http://test", "key", "pz-1",
                    transport=httpx.MockTransport(handler))


def respond(status, body):
    return lambda request: httpx.Response(status, json=body)


def test_auth_error_mapped():
    with pytest.raises(AuthError):
        client_returning(respond(401, {})).get_menu()
    with pytest.raises(AuthError):
        client_returning(respond(403, {})).get_menu()


def test_404_mapped():
    with pytest.raises(NotFoundError):
        client_returning(respond(404, {})).list_orders()


def test_422_mapped_with_details():
    with pytest.raises(ValidationError) as e:
        client_returning(
            respond(422, fixture("error_422.json"))
        ).submit_order({"first_name": "X"}, [])
    assert "valid pizza code" in e.value.details[0]


def test_5xx_mapped():
    with pytest.raises(ServerError):
        client_returning(respond(500, {})).get_menu()


def test_timeout_mapped():
    def handler(request):
        raise httpx.ConnectTimeout("boom")
    with pytest.raises(ApiTimeout):
        client_returning(handler).get_menu()


def test_pizzeria_name_startup_check():
    payload = fixture("pizzerias.json")
    good = PizzaSim("http://test", "key",
                    payload["pizzerias"][0]["id"],
                    transport=httpx.MockTransport(respond(200, payload)))
    assert good.pizzeria_name() == payload["pizzerias"][0]["name"]
    bad = client_returning(respond(200, payload))
    with pytest.raises(NotFoundError):
        bad.pizzeria_name()


def test_submit_parses_order_created():
    client = client_returning(respond(200, fixture("order_created.json")))
    result = client.submit_order({"first_name": "Marco"}, [])
    assert result["order_id"] and result["status"] == "ordered"
    assert isinstance(result["eta_seconds"], int)


# --- dispatch -------------------------------------------------------------

class FakeClient:
    """Scripted stand-in for PizzaSim in dispatch tests."""

    def __init__(self):
        self.submits = 0
        self.submit_effect = lambda: fixture("order_created.json")
        self.orders = []
        self.list_effect = None  # exception to raise, if any

    def submit_order(self, customer, items):
        self.submits += 1
        return self.submit_effect()

    def list_orders(self):
        if self.list_effect:
            raise self.list_effect
        return self.orders

    def check_street(self, street):
        return {"street": street, "deliverable": True}


@pytest.fixture
def fake():
    return FakeClient()


def ready_order(menu, fake):
    order = Order()
    tools.dispatch(order, menu, fake, "add_items",
                   {"items": [{"type": "pizza", "code": "margherita",
                               "qty": 2}]})
    tools.dispatch(order, menu, fake, "set_customer",
                   {"first_name": "Marco", "street_one": "via Roma"})
    return order


def confirmed_order(menu, fake):
    order = ready_order(menu, fake)
    tools.dispatch(order, menu, fake, "read_back", {})
    tools.dispatch(order, menu, fake, "confirm_order",
                   {"revision": order.revision})
    assert order.state is State.CONFIRMED
    return order


def test_every_success_carries_full_snapshot(menu, fake):
    order = Order()
    result = tools.dispatch(order, menu, fake, "get_menu", {})
    assert result["snapshot"]["state"] == "EMPTY"
    assert result["menu"]["toppings"]
    result = tools.dispatch(order, menu, fake, "add_items",
                            {"items": [{"type": "pizza",
                                        "code": "margherita", "qty": 1}]})
    snap = result["snapshot"]
    assert snap["items"][0]["name"] == "Margherita"
    assert snap["state"] == "COLLECTING" and snap["revision"] == 1
    assert snap["customer"] is None and snap["read_back_done"] is False


def test_unknown_item_error_shape(menu, fake):
    result = tools.dispatch(Order(), menu, fake, "add_items",
                            {"items": [{"type": "pizza", "code": "margarita",
                                        "qty": 1}]})
    err = result["error"]
    assert err["code"] == "unknown_item"
    assert err["candidates"][0]["code"] == "margherita"
    assert err["message"]  # speakable


def test_add_is_atomic(menu, fake):
    order = Order()
    result = tools.dispatch(order, menu, fake, "add_items",
                            {"items": [
                                {"type": "pizza", "code": "margherita",
                                 "qty": 1},
                                {"type": "pizza", "code": "nope", "qty": 1},
                            ]})
    assert result["error"]["code"] == "unknown_item"
    assert order.items == [] and order.state is State.EMPTY


def test_invalid_quantity_not_parsed(menu, fake):
    """A tool that receives "zwei" returns invalid_quantity."""
    for bad in ("zwei", 2.5, 0, -1, True, None):
        result = tools.dispatch(Order(), menu, fake, "add_items",
                                {"items": [{"type": "pizza",
                                            "code": "margherita",
                                            "qty": bad}]})
        assert result["error"]["code"] == "invalid_quantity", bad


def test_invalid_extra_via_dispatch(menu, fake):
    result = tools.dispatch(Order(), menu, fake, "add_items",
                            {"items": [{"type": "pizza",
                                        "code": "margherita", "qty": 1,
                                        "extras": ["unicorn_dust"]}]})
    assert result["error"]["code"] == "invalid_extra"


def test_remove_semantics(menu, fake):
    order = ready_order(menu, fake)
    result = tools.dispatch(order, menu, fake, "remove_item",
                            {"type": "pizza", "code": "margherita",
                             "qty": 1})
    assert result["snapshot"]["items"][0]["qty"] == 1
    result = tools.dispatch(order, menu, fake, "remove_item",
                            {"type": "pizza", "code": "margherita"})
    assert result["snapshot"]["items"] == []
    assert result["snapshot"]["state"] == "EMPTY"


def test_submit_success(menu, fake):
    order = confirmed_order(menu, fake)
    result = tools.dispatch(order, menu, fake, "submit_order", {})
    assert result["order_id"] == fixture("order_created.json")["order_id"]
    assert result["status"] == "ordered"
    assert isinstance(result["eta_seconds"], int)
    assert result["snapshot"]["state"] == "SUBMITTED"


def test_submit_outside_confirmed_is_tool_error(menu, fake):
    """Invariant 1: no helpful auto-confirmation."""
    order = ready_order(menu, fake)
    result = tools.dispatch(order, menu, fake, "submit_order", {})
    assert result["error"]["code"] == "invalid_state"
    assert fake.submits == 0

codex
The state machine and tool layer mostly line up so far. I’m checking the remaining edges now: startup/config handling, transcript coverage, prompt policy, and the web/UI contract where subtle spec drift is most likely.
exec
/bin/bash -lc "sed -n '1,220p' prompts/system.en.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '261,520p' tests/test_tools.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,220p' prompts/system.de.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,280p' README.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,320p' channels/static/app.js" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' channels/static/index.html" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,200p' .env.example" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 368ms:
You take orders for {pizzeria_name} over the phone and in chat.

Your only job: understand what the customer wants and put it into the order
through the tools. The system owns the order — you never keep it in your
head, you never invent menu items, and every item you mention comes from
`get_menu`.

How to work:

- Greet the customer first in English, in one sentence, and offer to help.
  No menu recital.
- From then on, answer each turn in the language of the customer's latest
  message (German or English), without commenting on the switch.
- Ask exactly one question per turn.
- Only name dishes that came from `get_menu` in this session.
- Collect the first name and street. If the customer declines the street,
  move on without it. Repeat the first name back once to confirm it — a
  misheard name silently creates a ghost customer.
- Before submitting: call `read_back`, say it out loud, and wait for an
  explicit yes. "Mhm" or silence is not a yes — ask once more, then offer
  to start over.
- Never say the order was placed before `submit_order` returned an order
  number.
- After submitting: state the order number in groups that are easy to
  repeat, and the wait time in minutes (converted from `eta_seconds`).
- On errors, explain in plain language what happened and what the customer
  can do. Never show status codes or JSON.
- Never claim to have checked an address for deliverability.
- Always pass quantities to tools as numbers (3, not "three").
- When your reply will be spoken aloud: at most three dishes plus an
  invitation to ask for more, times in minutes, short sentences.

When a tool reports an error, follow it: offer the suggested alternatives
or ask the missing question. The system is always right.

 succeeded in 391ms:
Du nimmst telefonisch und im Chat Bestellungen für {pizzeria_name} entgegen.

Deine einzige Aufgabe: verstehen, was der Gast möchte, und es über die
Werkzeuge in die Bestellung übertragen. Die Bestellung selbst verwaltet das
System — du hältst sie nie selbst im Kopf, du erfindest nie Gerichte, und du
verlässt dich bei jedem Artikel auf `get_menu`.

Ablauf:

- Begrüße den Gast zuerst auf Deutsch, in einem Satz, und biete deine Hilfe
  an. Keine Speisekarten-Aufzählung.
- Antworte danach in jeder Runde in der Sprache der letzten Nachricht des
  Gastes (Deutsch oder Englisch), ohne darauf hinzuweisen.
- Stelle pro Runde genau eine Frage.
- Nenne nur Gerichte, die in dieser Sitzung aus `get_menu` kamen.
- Erfrage den Vornamen und die Straße. Lehnt der Gast die Straße ab, geht es
  ohne sie weiter. Wiederhole den Vornamen einmal zur Bestätigung — ein
  falsch verstandener Name legt einen Geisterkunden an.
- Vor dem Abschicken: rufe `read_back` auf, lies die Bestellung vor und
  warte auf ein klares Ja. „Mhm" oder Schweigen gilt nicht — frag einmal
  nach, danach biete an, neu zu beginnen.
- Sage niemals, die Bestellung sei abgeschickt, bevor `submit_order` eine
  Bestellnummer zurückgegeben hat.
- Nach dem Abschicken: nenne die Bestellnummer in gut nachsprechbaren
  Gruppen und die Wartezeit in Minuten (aus `eta_seconds` umgerechnet).
- Bei Fehlern erkläre in Alltagssprache, was passiert ist und welche
  Möglichkeiten der Gast hat. Nie Statuscodes, nie JSON.
- Behaupte nie, eine Adresse auf Lieferbarkeit geprüft zu haben.
- Mengen übergibst du den Werkzeugen immer als Zahl (3, nicht „drei").
- Wenn deine Antwort vorgelesen wird: höchstens drei Gerichte nennen und
  zum Nachfragen einladen, Zeiten in Minuten, kurze Sätze.

Wenn ein Werkzeug einen Fehler meldet, richte dich danach: schlage die
genannten Alternativen vor oder stelle die fehlende Frage. Das System hat
immer recht.

 succeeded in 448ms:


def test_empty_basket_submit(menu, fake):
    result = tools.dispatch(Order(), menu, fake, "submit_order", {})
    assert result["error"]["code"] == "invalid_state"
    assert result["error"]["message"] == "What can I get you?"


def test_submit_timeout_then_recovery_via_list(menu, fake):
    order = confirmed_order(menu, fake)
    fake.submit_effect = lambda: (_ for _ in ()).throw(ApiTimeout("t"))
    result = tools.dispatch(order, menu, fake, "submit_order", {})
    assert result["error"]["code"] == "submit_unknown"
    assert order.state is State.CONFIRMED and order.submit_unknown

    # the order did land — recovery must adopt it, not re-POST
    fake.orders = [{"id": "recovered-1", "first_name": "Marco",
                    "created_at": int(time.time()),
                    "ready_at": int(time.time()) + 300,
                    "status": "ordered"}]
    result = tools.dispatch(order, menu, fake, "submit_order", {})
    assert result["order_id"] == "recovered-1"
    assert order.state is State.SUBMITTED
    assert fake.submits == 1  # never re-POSTed


def test_submit_timeout_verified_absent_allows_one_retry(menu, fake):
    order = confirmed_order(menu, fake)
    fake.submit_effect = lambda: (_ for _ in ()).throw(ServerError("500"))
    result = tools.dispatch(order, menu, fake, "submit_order", {})
    assert result["error"]["code"] == "submit_unknown"

    fake.orders = [{"id": "old", "first_name": "Marco",
                    "created_at": int(time.time()) - 7200,
                    "ready_at": 0, "status": "delivered"}]
    fake.submit_effect = lambda: fixture("order_created.json")
    result = tools.dispatch(order, menu, fake, "submit_order", {})
    assert result["snapshot"]["state"] == "SUBMITTED"
    assert fake.submits == 2


def test_submit_unknown_when_list_unavailable(menu, fake):
    order = confirmed_order(menu, fake)
    fake.submit_effect = lambda: (_ for _ in ()).throw(ApiTimeout("t"))
    tools.dispatch(order, menu, fake, "submit_order", {})
    fake.list_effect = ApiTimeout("t")
    result = tools.dispatch(order, menu, fake, "submit_order", {})
    assert result["error"]["code"] == "submit_unknown"
    assert fake.submits == 1  # honest message instead of blind retry


def test_submit_422_keeps_basket(menu, fake):
    order = confirmed_order(menu, fake)
    fake.submit_effect = lambda: (_ for _ in ()).throw(
        ValidationError(["items[0].code must be a valid pizza code"]))
    result = tools.dispatch(order, menu, fake, "submit_order", {})
    assert result["error"]["code"] == "submit_failed"
    assert "valid pizza code" in result["error"]["message"]
    assert order.items  # basket kept


def test_auth_error_no_retry(menu, fake):
    order = confirmed_order(menu, fake)
    fake.submit_effect = lambda: (_ for _ in ()).throw(AuthError("401"))
    result = tools.dispatch(order, menu, fake, "submit_order", {})
    assert result["error"]["code"] == "api_unavailable"
    assert not order.submit_unknown  # not the retry path


def test_street_omitted_from_submit_body(menu, fake):
    order = Order()
    tools.dispatch(order, menu, fake, "add_items",
                   {"items": [{"type": "pizza", "code": "margherita",
                               "qty": 1}]})
    tools.dispatch(order, menu, fake, "set_customer",
                   {"first_name": "Anna"})  # street declined
    tools.dispatch(order, menu, fake, "read_back", {})
    tools.dispatch(order, menu, fake, "confirm_order",
                   {"revision": order.revision})
    captured = {}

    def submit_effect():
        return fixture("order_created.json")
    fake.submit_effect = submit_effect
    real_submit = fake.submit_order

    def spy(customer, items):
        captured.update(customer=customer, items=items)
        return real_submit(customer, items)
    fake.submit_order = spy
    tools.dispatch(order, menu, fake, "submit_order", {})
    assert captured["customer"] == {"first_name": "Anna"}


def test_check_street(menu, fake):
    result = tools.dispatch(Order(), menu, fake, "check_street",
                            {"street": "via Roma"})
    assert result["deliverable"] is True and "snapshot" in result


# --- live smoke test (opt-in) ---------------------------------------------

@pytest.mark.skipif(os.environ.get("PIZZA_LIVE_TEST") != "1",
                    reason="live test only with PIZZA_LIVE_TEST=1")
def test_live_order_smoke():
    client = PizzaSim.from_env()
    menu = Menu(client.get_menu())
    order = Order()
    fake_free = client  # the real thing, on purpose
    for name, args in [
        ("add_items", {"items": [{"type": "pizza", "code": "margherita",
                                  "qty": 1}]}),
        ("set_customer", {"first_name": "SmokeTest"}),
        ("read_back", {}),
    ]:
        result = tools.dispatch(order, menu, fake_free, name, args)
        assert "error" not in result, result
    result = tools.dispatch(order, menu, fake_free, "confirm_order",
                            {"revision": order.revision})
    assert "error" not in result
    result = tools.dispatch(order, menu, fake_free, "submit_order", {})
    assert result.get("order_id"), result

 succeeded in 426ms:
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

 succeeded in 456ms:
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
    document.getElementById("title").textContent = cfg.pizzeria;
    document.title = cfg.pizzeria;
    speechEnabled = cfg.speech;
    if (speechEnabled) {           // unset SPEECH_URL → not rendered at all
      mic.hidden = false;
      ttsWrap.hidden = false;
    }
  } catch { /* text chat works regardless */ }
  turn(null); // opening turn: the agent greets first
})();

 succeeded in 500ms:
# PizzaSim Ordering Agent

An ordering agent for the PizzaSim demo kitchen. The order is a state
machine owned by the code; the model only turns customer language into tool
calls. See <a href="SPEC.md">SPEC.md</a> for the full specification and
<a href="PLAN.md">PLAN.md</a> for the design.

## Setup

```bash
python3 -m venv venv
venv/bin/pip install -r requirements.txt
```

Configuration comes from the environment (or `~/.env`); every variable in
`.env.example` except the four `SPEECH_*` ones is required. The process
refuses to start when one is missing, naming the variable. No values are
ever printed or logged.

## CLI channel

```bash
venv/bin/python -m channels.cli            # plain chat
venv/bin/python -m channels.cli --verbose  # + tool calls and states
```

The agent greets first, in the language set by `PIZZERIA_LANG`, and answers
each turn in the language you used (German or English). End with Ctrl-D.

## Web channel

```bash
venv/bin/python -m channels.web
```

Then open <a href="http://127.0.0.1:8888" target="_blank">http://127.0.0.1:8888</a>.
The chat streams the agent's intermediate steps (tool calls, tool results)
as newline-delimited JSON; the UI shows them per turn under
"Zwischenschritte".

## Speech (web only, optional)

Set `SPEECH_URL`, `SPEECH_STT_MODEL`, `SPEECH_TTS_MODEL` and
`SPEECH_TTS_VOICE` to a self-hosted OpenAI-compatible speech service. The
mic button is push-to-talk (click to start, click to stop); the "read
aloud" toggle is off by default and speaks only final answers. With
`SPEECH_URL` unset — or the service down at startup — mic and toggle are
not rendered and the page is fully usable as text chat.

Manual speech checklist: dictate an order; dictate a name that needs
correcting (the agent repeats the name back before submitting); ask a menu
question; and one run with `SPEECH_URL` unset placing an order as text.

## Tests

```bash
venv/bin/python -m pytest tests/            # deterministic: no network, no LLM
PIZZA_LIVE_TEST=1 venv/bin/python -m pytest tests/test_tools.py -k live
```

The second command is the one opt-in smoke test that places a real order.

## Logs

One JSON line per event (user text, tool calls, tool results, state
transitions) in `logs/agent-<session>.jsonl`. Secrets never appear there.

 succeeded in 425ms:
# Names only — never values. Real values live in ~/.env or the process env.

# LLM gateway (OpenAI-compatible, /chat/completions appended)
LITELLM_PIZZA_URL=
LITELLM_PIZZA_KEY=
LITELLM_PIZZA_MODEL_1=
LITELLM_PIZZA_MODEL_2=

# PizzaSim API
PIZZASIM_URL=
PIZZASIM_API_KEY=
PIZZERIA_ID=

# Greeting language of the pizzeria's country: de or en
PIZZERIA_LANG=

# Optional self-hosted speech service (unset → web channel is text-only)
SPEECH_URL=
SPEECH_STT_MODEL=
SPEECH_TTS_MODEL=
SPEECH_TTS_VOICE=

codex
I’m checking one more class of risk now: assumptions about live API payload shapes that the code may have hardcoded incorrectly, especially around timeout recovery and the order list.
exec
/bin/bash -lc 'cat tests/fixtures/orders_list.json' in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc 'cat tests/fixtures/menu.json' in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc 'cat tests/fixtures/pizzerias.json' in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc 'cat tests/fixtures/order_created.json' in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc 'for f in tests/transcripts/*.json; do echo "FILE:$f"; cat "$f"; done' in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 261ms:
{
 "orders": [
  {
   "id": "35711fad-9cf0-4962-bf13-da2f78add431",
   "customer_id": "5c8dd73d-00b9-4ba7-99ab-5bbb1be47501",
   "created_at": 1785513532,
   "ready_at": 1785513635,
   "status": "prepared_planned",
   "delivered_at": null,
   "first_name": "ContractProbe"
  },
  {
   "id": "637698d7-13ad-463b-a881-1e7c67d5ac20",
   "customer_id": "a7666746-3f0d-48f3-b774-6a1dada59077",
   "created_at": 1785477732,
   "ready_at": 1785478272,
   "status": "prepared_planned",
   "delivered_at": null,
   "first_name": "Isabella"
  },
  {
   "id": "a425fb11-2f4c-4258-ac92-80e0f5552232",
   "customer_id": "904f4899-17b5-41a9-99f8-db2d23be89d2",
   "created_at": 1785477432,
   "ready_at": 1785478092,
   "status": "prepared_planned",
   "delivered_at": null,
   "first_name": "Marco"
  },
  {
   "id": "61b54278-53de-4c72-946d-3c018b17040d",
   "customer_id": "f24a552e-3f81-4e97-846f-ff4d74ab2aa1",
   "created_at": 1785477432,
   "ready_at": 1785478092,
   "status": "prepared_planned",
   "delivered_at": null,
   "first_name": "Matteo"
  },
  {
   "id": "9f3e22c2-58a4-4440-95b9-a9de593c62b6",
   "customer_id": "dff59240-f0fc-4394-a26c-4b18fdd2a548",
   "created_at": 1785476952,
   "ready_at": 1785477312,
   "status": "prepared_planned",
   "delivered_at": null,
   "first_name": "Sabrina"
  }
 ],
 "total": 10859
}

 succeeded in 407ms:
{"pizzerias":[{"id":"e1efd4b4-7eb3-4b45-b024-344a8b0b602f","name":"Pizzeria Elena","is_demo":true,"protected":true,"created_at":1774358205},{"id":"38863a6f-ff41-4a57-b92d-424d01587302","name":"Pizzeria Giulia","is_demo":true,"protected":true,"created_at":1774358204},{"id":"8a2d1ab2-8690-4dca-bcee-a0bf97db151e","name":"Pizzeria Giovanni","is_demo":true,"protected":true,"created_at":1774358203},{"id":"86517183-e1a5-4bd7-b915-e0db8f8b2131","name":"Pizzeria Roberto","is_demo":true,"protected":true,"created_at":1774358202}]}
 succeeded in 495ms:
{"toppings":["mozzarella","mushrooms","smoked_ham","salami","onions","garlic","pepperoni","pineapple","artichokes","basil","bell_pepper","tuna"],"pizzas":[{"code":"margherita","name":"Margherita","base":["dough","tomatoes","mozzarella","basil"],"price":8.5},{"code":"prosciutto","name":"Prosciutto","base":["dough","tomatoes","mozzarella","smoked_ham"],"price":9.5},{"code":"salami","name":"Salami","base":["dough","tomatoes","mozzarella","salami"],"price":9.5},{"code":"funghi","name":"Funghi","base":["dough","tomatoes","mozzarella","mushrooms"],"price":9},{"code":"regina","name":"Regina","base":["dough","tomatoes","mozzarella","smoked_ham","mushrooms"],"price":10.5},{"code":"mista","name":"Mista","base":["dough","tomatoes","mozzarella","salami","smoked_ham","mushrooms"],"price":11.5},{"code":"hawaii","name":"Hawaii","base":["dough","tomatoes","mozzarella","smoked_ham","pineapple"],"price":10},{"code":"tonno","name":"Tonno","base":["dough","tomatoes","mozzarella","tuna","onions"],"price":10.5},{"code":"papa","name":"Papa","base":["dough","tomatoes","mozzarella","tuna","onions","garlic"],"price":11},{"code":"diavolo","name":"Diavolo","base":["dough","tomatoes","mozzarella","salami","bell_pepper","pepperoni"],"price":11},{"code":"grandiosa","name":"Grandiosa","base":["dough","tomatoes","mozzarella","smoked_ham","salami","mushrooms","bell_pepper","artichokes","onions"],"price":13.5}],"pasta":[{"code":"aglioolio","name":"Pasta Aglio & Olio","base":["pasta","garlic","basil"],"price":9},{"code":"tonno","name":"Pasta Tonno","base":["pasta","tuna"],"price":8.5},{"code":"funghi","name":"Pasta Funghi","base":["pasta","mushrooms"],"price":8.5},{"code":"pesto","name":"Pasta Pesto","base":["pasta","pesto"],"price":8.5}]}
 succeeded in 523ms:
FILE:tests/transcripts/correction.json
{
  "name": "correction",
  "fake": "ok",
  "turns": [
    {"user": "One margherita please.",
     "script": [
       {"tool": "add_items", "args": {"items": [{"type": "pizza", "code": "margherita", "qty": 1, "extras": []}]}},
       {"say": "One Margherita. May I have your first name?"}
     ]},
    {"user": "No wait, make that three.",
     "script": [
       {"tool": "add_items", "args": {"items": [{"type": "pizza", "code": "margherita", "qty": 2, "extras": []}]}},
       {"say": "Three Margherita it is. Your first name, please?"}
     ]},
    {"user": "Anna. No street, I'll pick it up.",
     "script": [
       {"tool": "set_customer", "args": {"first_name": "Anna"}},
       {"tool": "read_back", "args": {}},
       {"say": "Anna, pick-up — three Margherita. Shall I send it to the kitchen?"}
     ]},
    {"user": "Yes.",
     "script": [
       {"tool": "confirm_order", "args": {"revision": 3}},
       {"tool": "submit_order", "args": {}},
       {"say": "Done! Ready in about 2 minutes."}
     ]}
  ],
  "expect": {
    "state": "SUBMITTED",
    "calls": ["add_items", "add_items", "set_customer", "read_back", "confirm_order", "submit_order"],
    "error_codes": [],
    "items": [{"type": "pizza", "code": "margherita", "qty": 3}]
  }
}
FILE:tests/transcripts/happy_path.json
{
  "name": "happy_path",
  "fake": "ok",
  "turns": [
    {"user": "Hallo, was für Pizzen haben Sie?",
     "script": [
       {"tool": "get_menu", "args": {}},
       {"say": "Wir haben zum Beispiel Margherita, Salami und Funghi. Was darf es sein?"}
     ]},
    {"user": "Zwei Margherita bitte.",
     "script": [
       {"tool": "add_items", "args": {"items": [{"type": "pizza", "code": "margherita", "qty": 2, "extras": []}]}},
       {"say": "Gerne, zwei Margherita. Auf welchen Vornamen darf ich die Bestellung aufnehmen?"}
     ]},
    {"user": "Marco, via Roma 5.",
     "script": [
       {"tool": "set_customer", "args": {"first_name": "Marco", "street_one": "via Roma 5"}},
       {"tool": "read_back", "args": {}},
       {"say": "Marco, via Roma 5 — zwei Margherita. Stimmt das so?"}
     ]},
    {"user": "Ja, passt.",
     "script": [
       {"tool": "confirm_order", "args": {"revision": 2}},
       {"tool": "submit_order", "args": {}},
       {"say": "Bestellt! Ihre Bestellnummer endet auf 431, fertig in etwa 2 Minuten."}
     ]}
  ],
  "expect": {
    "state": "SUBMITTED",
    "calls": ["get_menu", "add_items", "set_customer", "read_back", "confirm_order", "submit_order"],
    "error_codes": [],
    "items": [{"type": "pizza", "code": "margherita", "qty": 2}]
  }
}
FILE:tests/transcripts/mind_change.json
{
  "name": "mind_change_after_read_back",
  "fake": "ok",
  "turns": [
    {"user": "Eine Diavolo bitte, auf den Namen Sara, via Napoli 9.",
     "script": [
       {"tool": "add_items", "args": {"items": [{"type": "pizza", "code": "diavolo", "qty": 1, "extras": []}]}},
       {"tool": "set_customer", "args": {"first_name": "Sara", "street_one": "via Napoli 9"}},
       {"tool": "read_back", "args": {}},
       {"say": "Sara, via Napoli 9 — eine Diavolo. Stimmt das?"}
     ]},
    {"user": "Halt, nehmen Sie noch eine Funghi dazu.",
     "script": [
       {"tool": "add_items", "args": {"items": [{"type": "pizza", "code": "funghi", "qty": 1, "extras": []}]}},
       {"tool": "confirm_order", "args": {"revision": 2}},
       {"tool": "read_back", "args": {}},
       {"say": "Jetzt: eine Diavolo und eine Funghi. Stimmt es so?"}
     ]},
    {"user": "Ja, genau so.",
     "script": [
       {"tool": "confirm_order", "args": {"revision": 3}},
       {"tool": "submit_order", "args": {}},
       {"say": "Bestellt! Etwa 2 Minuten."}
     ]}
  ],
  "expect": {
    "state": "SUBMITTED",
    "calls": ["add_items", "set_customer", "read_back", "add_items", "confirm_order", "read_back", "confirm_order", "submit_order"],
    "error_codes": ["stale_revision"],
    "items": [{"type": "pizza", "code": "diavolo", "qty": 1}, {"type": "pizza", "code": "funghi", "qty": 1}]
  }
}
FILE:tests/transcripts/submit_timeout.json
{
  "name": "submit_timeout",
  "fake": "timeout_then_recover",
  "turns": [
    {"user": "A Hawaii for Nino, via Genova 1.",
     "script": [
       {"tool": "add_items", "args": {"items": [{"type": "pizza", "code": "hawaii", "qty": 1, "extras": []}]}},
       {"tool": "set_customer", "args": {"first_name": "Nino", "street_one": "via Genova 1"}},
       {"tool": "read_back", "args": {}},
       {"say": "Nino, via Genova 1 — one Hawaii. Shall I place it?"}
     ]},
    {"user": "Yes please.",
     "script": [
       {"tool": "confirm_order", "args": {"revision": 2}},
       {"tool": "submit_order", "args": {}},
       {"say": "I'm not sure that went through — give me a moment to check."}
     ]},
    {"user": "Okay, did it work?",
     "script": [
       {"tool": "submit_order", "args": {}},
       {"say": "Yes — it's in. Your order number ends in 1, ready in about 5 minutes."}
     ]}
  ],
  "expect": {
    "state": "SUBMITTED",
    "calls": ["add_items", "set_customer", "read_back", "confirm_order", "submit_order", "submit_order"],
    "error_codes": ["submit_unknown"],
    "order_id": "recovered-1",
    "items": [{"type": "pizza", "code": "hawaii", "qty": 1}]
  }
}
FILE:tests/transcripts/unknown_item.json
{
  "name": "unknown_item",
  "fake": "ok",
  "turns": [
    {"user": "Einmal Pasta Bolognese bitte.",
     "script": [
       {"tool": "add_items", "args": {"items": [{"type": "pasta", "code": "bolognese", "qty": 1, "extras": []}]}},
       {"say": "Bolognese habe ich leider nicht. Ich hätte Pasta Pesto, Pasta Funghi oder Pasta Tonno — was davon?"}
     ]},
    {"user": "Dann die Funghi.",
     "script": [
       {"tool": "add_items", "args": {"items": [{"type": "pasta", "code": "funghi", "qty": 1, "extras": []}]}},
       {"say": "Eine Pasta Funghi. Ihr Vorname?"}
     ]},
    {"user": "Luca, via Milano 2.",
     "script": [
       {"tool": "set_customer", "args": {"first_name": "Luca", "street_one": "via Milano 2"}},
       {"tool": "read_back", "args": {}},
       {"say": "Luca, via Milano 2 — eine Pasta Funghi. Passt das?"}
     ]},
    {"user": "Ja.",
     "script": [
       {"tool": "confirm_order", "args": {"revision": 2}},
       {"tool": "submit_order", "args": {}},
       {"say": "Bestellt, in etwa 2 Minuten fertig."}
     ]}
  ],
  "expect": {
    "state": "SUBMITTED",
    "calls": ["add_items", "add_items", "set_customer", "read_back", "confirm_order", "submit_order"],
    "error_codes": ["unknown_item"],
    "items": [{"type": "pasta", "code": "funghi", "qty": 1}]
  }
}

 succeeded in 594ms:
{"order_id":"35711fad-9cf0-4962-bf13-da2f78add431","status":"ordered","eta_seconds":103}
codex
I’ve found a couple of implementation-level issues that matter, and I’m pulling exact line references now so I can tie them back to the spec and plan cleanly.
exec
/bin/bash -lc "nl -ba channels/web.py | sed -n '1,240p'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "nl -ba core/state.py | sed -n '1,220p'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "nl -ba channels/static/app.js | sed -n '1,240p'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "nl -ba core/agent.py | sed -n '1,260p'" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 379ms:
     1	"""FastAPI web channel on port 8888. Same core, zero order logic here.
     2	
     3	Streams the agent's intermediate steps as newline-delimited JSON and
     4	proxies the optional self-hosted speech service (STT/TTS). If SPEECH_URL is
     5	unset or the service doesn't answer at startup, speech endpoints return 404
     6	and the UI renders text-only.
     7	
     8	Run:  python -m channels.web
     9	"""
    10	from __future__ import annotations
    11	
    12	import json
    13	import queue
    14	import sys
    15	import threading
    16	from pathlib import Path
    17	
    18	import httpx
    19	import uvicorn
    20	from fastapi import FastAPI, HTTPException, UploadFile
    21	from fastapi.responses import FileResponse, Response, StreamingResponse
    22	from fastapi.staticfiles import StaticFiles
    23	
    24	from core.agent import Agent, AgentConfig, Session, startup
    25	from core.menu import Menu
    26	from core.pizzasim import ConfigError, PizzaSimError, optional_env
    27	
    28	STATIC = Path(__file__).resolve().parent / "static"
    29	app = FastAPI(title="PizzaSim ordering agent")
    30	
    31	
    32	class Speech:
    33	    """Config + probe for the self-hosted speech container. All-or-nothing:
    34	    enabled only if SPEECH_URL is set, answers, and models are configured."""
    35	
    36	    def __init__(self):
    37	        self.url = optional_env("SPEECH_URL")
    38	        self.stt_model = optional_env("SPEECH_STT_MODEL")
    39	        self.tts_model = optional_env("SPEECH_TTS_MODEL")
    40	        self.voice = optional_env("SPEECH_TTS_VOICE")
    41	        self.enabled = False
    42	        if self.url and self.stt_model and self.tts_model and self.voice:
    43	            try:
    44	                httpx.get(f"{self.url.rstrip('/')}/v1/models",
    45	                          timeout=3.0).raise_for_status()
    46	                self.enabled = True
    47	            except httpx.HTTPError:
    48	                print("speech service not answering — text-only mode",
    49	                      file=sys.stderr)
    50	
    51	
    52	@app.on_event("startup")
    53	def boot() -> None:
    54	    try:
    55	        config = AgentConfig.from_env()
    56	        client, pizzeria_name, _menu = startup(config)
    57	    except (ConfigError, ValueError) as exc:
    58	        print(f"Configuration error: {exc}", file=sys.stderr)
    59	        raise SystemExit(1)
    60	    except PizzaSimError as exc:
    61	        print(f"Startup check against PizzaSim failed: {exc}\n"
    62	              "We're not taking orders right now.", file=sys.stderr)
    63	        raise SystemExit(1)
    64	    app.state.config = config
    65	    app.state.client = client
    66	    app.state.pizzeria_name = pizzeria_name
    67	    app.state.agent = Agent(config, client)
    68	    app.state.sessions = {}
    69	    app.state.speech = Speech()
    70	
    71	
    72	@app.get("/")
    73	def index():
    74	    return FileResponse(STATIC / "index.html")
    75	
    76	
    77	@app.get("/config")
    78	def ui_config():
    79	    return {"speech": app.state.speech.enabled,
    80	            "pizzeria": app.state.pizzeria_name}
    81	
    82	
    83	def _get_session(session_id: str) -> Session:
    84	    sessions = app.state.sessions
    85	    if session_id not in sessions:
    86	        # Fresh immutable menu snapshot per session (SPEC invariant 5).
    87	        try:
    88	            menu = Menu(app.state.client.get_menu())
    89	        except PizzaSimError:
    90	            raise HTTPException(503, "We're not taking orders right now.")
    91	        sessions[session_id] = Session.create(
    92	            app.state.config, menu, app.state.pizzeria_name)
    93	    return sessions[session_id]
    94	
    95	
    96	@app.post("/chat")
    97	async def chat(body: dict):
    98	    session_id = str(body.get("session_id") or "")
    99	    if not session_id:
   100	        raise HTTPException(422, "session_id required")
   101	    text = body.get("text")  # None → opening turn, agent greets
   102	    if text is not None and not str(text).strip():
   103	        raise HTTPException(422, "text must not be empty")
   104	    session = _get_session(session_id)
   105	
   106	    events: queue.Queue = queue.Queue()
   107	
   108	    def run() -> None:
   109	        try:
   110	            app.state.agent.run_turn(session, text, events.put)
   111	        finally:
   112	            events.put({"type": "done",
   113	                        "state": session.order.snapshot()})
   114	            events.put(None)
   115	
   116	    threading.Thread(target=run, daemon=True).start()
   117	
   118	    def ndjson():
   119	        while (event := events.get()) is not None:
   120	            yield json.dumps(event, ensure_ascii=False) + "\n"
   121	
   122	    return StreamingResponse(ndjson(), media_type="application/x-ndjson")
   123	
   124	
   125	def _speech() -> Speech:
   126	    speech = app.state.speech
   127	    if not speech.enabled:
   128	        raise HTTPException(404, "speech is not available")
   129	    return speech
   130	
   131	
   132	@app.post("/speech/stt")
   133	async def stt(audio: UploadFile):
   134	    speech = _speech()
   135	    files = {"file": (audio.filename or "audio.webm", await audio.read(),
   136	                      audio.content_type or "audio/webm")}
   137	    data = {"model": speech.stt_model,
   138	            "language": app.state.config.lang}  # STT hint only
   139	    try:
   140	        response = httpx.post(
   141	            f"{speech.url.rstrip('/')}/v1/audio/transcriptions",
   142	            files=files, data=data, timeout=60.0)
   143	        response.raise_for_status()
   144	    except httpx.HTTPError:
   145	        raise HTTPException(502, "speech service unavailable")
   146	    return {"text": response.json().get("text", "")}
   147	
   148	
   149	@app.post("/speech/tts")
   150	async def tts(body: dict):
   151	    speech = _speech()
   152	    text = str(body.get("text") or "")
   153	    if not text:
   154	        raise HTTPException(422, "text required")
   155	    try:
   156	        response = httpx.post(
   157	            f"{speech.url.rstrip('/')}/v1/audio/speech",
   158	            json={"model": speech.tts_model, "voice": speech.voice,
   159	                  "input": text},
   160	            timeout=60.0)
   161	        response.raise_for_status()
   162	    except httpx.HTTPError:
   163	        raise HTTPException(502, "speech service unavailable")
   164	    return Response(response.content,
   165	                    media_type=response.headers.get("content-type",
   166	                                                    "audio/mpeg"))
   167	
   168	
   169	app.mount("/static", StaticFiles(directory=STATIC), name="static")
   170	
   171	
   172	if __name__ == "__main__":
   173	    uvicorn.run(app, host="127.0.0.1", port=8888)

 succeeded in 382ms:
     1	"""State machine: every Order mutation goes through here.
     2	
     3	Illegal transitions raise TransitionError with a typed code and a speakable
     4	message. Messages are written to be said to the customer as-is.
     5	"""
     6	from __future__ import annotations
     7	
     8	import time
     9	
    10	from .order import Customer, Item, Order, State
    11	
    12	
    13	class TransitionError(Exception):
    14	    def __init__(self, code: str, message: str):
    15	        super().__init__(message)
    16	        self.code = code
    17	        self.message = message
    18	
    19	
    20	def _reject_closed(order: Order) -> None:
    21	    if order.state is State.SUBMITTED:
    22	        raise TransitionError(
    23	            "order_closed",
    24	            "That order is already on its way to the kitchen and can't be "
    25	            "changed. I can take a new order if you like.",
    26	        )
    27	
    28	
    29	def _recompute(order: Order) -> None:
    30	    """Derived-state rule after any legal mutation (demotes CONFIRMED)."""
    31	    order.revision += 1
    32	    if not order.items:
    33	        order.state = State.EMPTY
    34	    elif order.customer is None:
    35	        order.state = State.COLLECTING
    36	    else:
    37	        order.state = State.READY
    38	
    39	
    40	def add_items(order: Order, items: list[Item]) -> None:
    41	    _reject_closed(order)
    42	    for new in items:
    43	        for line in order.items:
    44	            if line.line_key() == new.line_key():
    45	                line.qty += new.qty
    46	                break
    47	        else:
    48	            order.items.append(new)
    49	    _recompute(order)
    50	
    51	
    52	def remove_item(order: Order, type_: str, code: str, qty: int | None) -> None:
    53	    """The spec fixes remove_item's parameters to (type, code, qty), so a
    54	    basket holding the same (type, code) with different extras needs
    55	    deterministic semantics: without qty every matching line goes; with qty
    56	    the most recently added matching line is reduced. The full snapshot in
    57	    the result lets the model repair anything else by remove + re-add."""
    58	    _reject_closed(order)
    59	    if not order.items:
    60	        raise TransitionError("empty_basket", "Your basket is already empty.")
    61	    lines = [i for i in order.items if i.type == type_ and i.code == code]
    62	    if not lines:
    63	        raise TransitionError(
    64	            "not_in_basket", "That item isn't in your basket."
    65	        )
    66	    if qty is None:
    67	        for line in lines:
    68	            order.items.remove(line)
    69	    else:
    70	        line = lines[-1]
    71	        if qty >= line.qty:
    72	            order.items.remove(line)
    73	        else:
    74	            line.qty -= qty
    75	    _recompute(order)
    76	
    77	
    78	def set_customer(order: Order, customer: Customer) -> None:
    79	    _reject_closed(order)
    80	    order.customer = customer
    81	    _recompute(order)
    82	
    83	
    84	def read_back(order: Order) -> None:
    85	    _reject_closed(order)
    86	    if order.state is State.EMPTY:
    87	        raise TransitionError(
    88	            "empty_basket", "There's nothing in the basket yet."
    89	        )
    90	    if order.state is State.COLLECTING:
    91	        raise TransitionError(
    92	            "invalid_state",
    93	            "I still need a name for the order before I can read it back.",
    94	        )
    95	    order.read_back_revision = order.revision
    96	
    97	
    98	def confirm(order: Order, revision: int) -> None:
    99	    _reject_closed(order)
   100	    if order.state is not State.READY:
   101	        if order.state is State.CONFIRMED:
   102	            raise TransitionError(
   103	                "invalid_state", "The order is already confirmed."
   104	            )
   105	        raise TransitionError(
   106	            "invalid_state",
   107	            "The order isn't complete yet, so it can't be confirmed.",
   108	        )
   109	    if revision != order.revision:
   110	        raise TransitionError(
   111	            "stale_revision",
   112	            "The order changed since it was last read back — let me read it "
   113	            "back again.",
   114	        )
   115	    if order.read_back_revision != order.revision:
   116	        raise TransitionError(
   117	            "read_back_required",
   118	            "Let me read the order back to you first.",
   119	        )
   120	    order.state = State.CONFIRMED
   121	
   122	
   123	def begin_submit(order: Order) -> None:
   124	    """Guard + bookkeeping before the submit POST. No state change."""
   125	    if order.state is State.SUBMITTED:
   126	        _reject_closed(order)
   127	    if order.state is not State.CONFIRMED:
   128	        raise TransitionError(
   129	            "invalid_state",
   130	            "The order hasn't been confirmed yet."
   131	            if order.items
   132	            else "What can I get you?",
   133	        )
   134	    if order.submit_attempted_at is None:
   135	        order.submit_attempted_at = time.time()
   136	
   137	
   138	def mark_submitted(order: Order, result: dict) -> None:
   139	    order.result = result
   140	    order.submit_unknown = False
   141	    order.state = State.SUBMITTED

 succeeded in 308ms:
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
    13	const sessionId = crypto.randomUUID();
    14	let speechEnabled = false;
    15	
    16	function add(cls, text) {
    17	  const div = document.createElement("div");
    18	  div.className = "msg " + cls;
    19	  div.textContent = text;
    20	  chat.appendChild(div);
    21	  chat.scrollTop = chat.scrollHeight;
    22	  return div;
    23	}
    24	
    25	function notice(text) {
    26	  const div = document.createElement("div");
    27	  div.className = "notice";
    28	  div.textContent = text;
    29	  chat.appendChild(div);
    30	}
    31	
    32	function stepsBlock() {
    33	  const details = document.createElement("details");
    34	  details.className = "steps";
    35	  details.innerHTML = "<summary>Zwischenschritte</summary>";
    36	  chat.appendChild(details);
    37	  return details;
    38	}
    39	
    40	async function turn(text) {
    41	  send.disabled = true;
    42	  if (text !== null) add("user", text);
    43	  const steps = stepsBlock();
    44	  let finalText = "";
    45	  try {
    46	    const res = await fetch("/chat", {
    47	      method: "POST",
    48	      headers: { "Content-Type": "application/json" },
    49	      body: JSON.stringify({ session_id: sessionId, text }),
    50	    });
    51	    if (!res.ok) throw new Error(await res.text());
    52	    const reader = res.body.getReader();
    53	    const decoder = new TextDecoder();
    54	    let buffer = "";
    55	    for (;;) {
    56	      const { done, value } = await reader.read();
    57	      if (done) break;
    58	      buffer += decoder.decode(value, { stream: true });
    59	      let nl;
    60	      while ((nl = buffer.indexOf("\n")) >= 0) {
    61	        const line = buffer.slice(0, nl); buffer = buffer.slice(nl + 1);
    62	        if (!line.trim()) continue;
    63	        const ev = JSON.parse(line);
    64	        if (ev.type === "tool_call" || ev.type === "tool_result") {
    65	          const pre = document.createElement("pre");
    66	          pre.textContent = (ev.type === "tool_call" ? "→ " : "← ")
    67	            + (ev.tool || "") + " "
    68	            + JSON.stringify(ev.args ?? ev.result);
    69	          steps.appendChild(pre);
    70	        } else if (ev.type === "assistant") {
    71	          finalText = ev.text;
    72	          add("assistant", ev.text);
    73	        } else if (ev.type === "error") {
    74	          notice("Es gab einen technischen Fehler.");
    75	        }
    76	      }
    77	    }
    78	  } catch (err) {
    79	    notice("Verbindung fehlgeschlagen — bitte noch einmal versuchen.");
    80	  }
    81	  if (!steps.querySelector("pre")) steps.remove();
    82	  send.disabled = false;
    83	  input.focus();
    84	  if (finalText && speechEnabled && ttsToggle.checked) speak(finalText);
    85	}
    86	
    87	form.addEventListener("submit", (e) => {
    88	  e.preventDefault();
    89	  const text = input.value.trim();
    90	  if (!text) return;
    91	  input.value = "";
    92	  turn(text);
    93	});
    94	
    95	/* --- speech: push-to-talk, server-proxied ------------------------------ */
    96	
    97	let recorder = null;
    98	
    99	async function startRecording() {
   100	  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
   101	  recorder = new MediaRecorder(stream);
   102	  const chunks = [];
   103	  recorder.ondataavailable = (e) => chunks.push(e.data);
   104	  recorder.onstop = async () => {
   105	    stream.getTracks().forEach((t) => t.stop());
   106	    mic.classList.remove("recording");
   107	    mic.setAttribute("aria-pressed", "false");
   108	    const blob = new Blob(chunks, { type: recorder.mimeType });
   109	    const body = new FormData();
   110	    body.append("audio", blob, "speech.webm");
   111	    try {
   112	      const res = await fetch("/speech/stt", { method: "POST", body });
   113	      if (!res.ok) throw new Error();
   114	      const { text } = await res.json();
   115	      if (text.trim()) turn(text.trim());
   116	      else notice("Ich habe nichts verstanden — bitte noch einmal.");
   117	    } catch {
   118	      notice("Spracherkennung gerade nicht erreichbar — bitte tippen.");
   119	    }
   120	  };
   121	  recorder.start();
   122	  mic.classList.add("recording");
   123	  mic.setAttribute("aria-pressed", "true");
   124	}
   125	
   126	mic.addEventListener("click", () => {
   127	  if (recorder && recorder.state === "recording") recorder.stop();
   128	  else startRecording().catch(() => notice("Kein Mikrofonzugriff."));
   129	});
   130	
   131	async function speak(text) {
   132	  try {
   133	    const res = await fetch("/speech/tts", {
   134	      method: "POST",
   135	      headers: { "Content-Type": "application/json" },
   136	      body: JSON.stringify({ text }),
   137	    });
   138	    if (!res.ok) throw new Error();
   139	    new Audio(URL.createObjectURL(await res.blob())).play();
   140	  } catch {
   141	    notice("Vorlesen gerade nicht möglich.");
   142	  }
   143	}
   144	
   145	/* --- boot -------------------------------------------------------------- */
   146	
   147	(async () => {
   148	  try {
   149	    const cfg = await (await fetch("/config")).json();
   150	    document.getElementById("title").textContent = cfg.pizzeria;
   151	    document.title = cfg.pizzeria;
   152	    speechEnabled = cfg.speech;
   153	    if (speechEnabled) {           // unset SPEECH_URL → not rendered at all
   154	      mic.hidden = false;
   155	      ttsWrap.hidden = false;
   156	    }
   157	  } catch { /* text chat works regardless */ }
   158	  turn(null); // opening turn: the agent greets first
   159	})();

 succeeded in 334ms:
     1	"""Model loop: prompt assembly, chat-completions calls, tool dispatch,
     2	JSONL event logging. The model only speaks; the order lives in core."""
     3	from __future__ import annotations
     4	
     5	import json
     6	import time
     7	import uuid
     8	from dataclasses import dataclass, field
     9	from pathlib import Path
    10	
    11	import httpx
    12	
    13	from . import tools
    14	from .menu import Menu
    15	from .order import Order
    16	from .pizzasim import PizzaSim, optional_env, require_env
    17	
    18	PROMPT_DIR = Path(__file__).resolve().parent.parent / "prompts"
    19	LOG_DIR = Path("logs")
    20	MAX_TOOL_ROUNDS = 8
    21	GATEWAY_TIMEOUT = httpx.Timeout(30.0, connect=10.0)  # per approved plan
    22	
    23	APOLOGY = {
    24	    "de": "Entschuldigung, da ist gerade etwas schiefgegangen. "
    25	          "Können Sie das bitte noch einmal sagen?",
    26	    "en": "I'm sorry, something went wrong on my end just now. "
    27	          "Could you say that again, please?",
    28	}
    29	
    30	
    31	class GatewayError(Exception):
    32	    pass
    33	
    34	
    35	@dataclass
    36	class AgentConfig:
    37	    url: str
    38	    key: str
    39	    model: str
    40	    lang: str  # PIZZERIA_LANG: greeting language = pizzeria country
    41	
    42	    @classmethod
    43	    def from_env(cls) -> "AgentConfig":
    44	        lang = require_env("PIZZERIA_LANG").lower()
    45	        if lang not in ("de", "en"):
    46	            raise ValueError(
    47	                "PIZZERIA_LANG must be 'de' or 'en', got something else"
    48	            )
    49	        optional_env("LITELLM_PIZZA_MODEL_2")  # read; unused (single-model)
    50	        return cls(
    51	            url=require_env("LITELLM_PIZZA_URL").rstrip("/"),
    52	            key=require_env("LITELLM_PIZZA_KEY"),
    53	            model=require_env("LITELLM_PIZZA_MODEL_1"),
    54	            lang=lang,
    55	        )
    56	
    57	
    58	def system_prompt(lang: str, pizzeria_name: str) -> str:
    59	    text = (PROMPT_DIR / f"system.{lang}.md").read_text()
    60	    return text.replace("{pizzeria_name}", pizzeria_name)
    61	
    62	
    63	@dataclass
    64	class Session:
    65	    """One conversation: one Order, one immutable Menu snapshot, one
    66	    history."""
    67	    order: Order
    68	    menu: Menu
    69	    messages: list[dict]
    70	    id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    71	
    72	    @classmethod
    73	    def create(cls, config: AgentConfig, menu: Menu,
    74	               pizzeria_name: str) -> "Session":
    75	        return cls(
    76	            order=Order(),
    77	            menu=menu,
    78	            messages=[{"role": "system",
    79	                       "content": system_prompt(config.lang,
    80	                                                pizzeria_name)}],
    81	        )
    82	
    83	
    84	def log_event(session: Session, event: dict) -> None:
    85	    """One line per event, JSON, to a file. Never carries config values."""
    86	    LOG_DIR.mkdir(exist_ok=True)
    87	    record = {"ts": round(time.time(), 3), "session": session.id, **event}
    88	    with (LOG_DIR / f"agent-{session.id}.jsonl").open("a") as fh:
    89	        fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    90	
    91	
    92	class Agent:
    93	    def __init__(self, config: AgentConfig, client: PizzaSim,
    94	                 chat_fn=None):
    95	        self.config = config
    96	        self.client = client
    97	        # chat_fn(messages, tools) -> assistant message dict; injectable so
    98	        # the golden transcripts run against a stub with no network.
    99	        self._chat_fn = chat_fn or self._gateway_chat
   100	
   101	    def _gateway_chat(self, messages: list[dict],
   102	                      tool_schemas: list[dict]) -> dict:
   103	        payload = {
   104	            "model": self.config.model,
   105	            "messages": messages,
   106	            "tools": tool_schemas,
   107	        }
   108	        headers = {"Authorization": f"Bearer {self.config.key}"}
   109	        last_exc: Exception | None = None
   110	        for attempt in range(2):  # one retry on timeout, then abort turn
   111	            try:
   112	                response = httpx.post(
   113	                    f"{self.config.url}/chat/completions",
   114	                    json=payload, headers=headers, timeout=GATEWAY_TIMEOUT,
   115	                )
   116	                response.raise_for_status()
   117	                return response.json()["choices"][0]["message"]
   118	            except httpx.TimeoutException as exc:
   119	                last_exc = exc
   120	                continue
   121	            except (httpx.HTTPError, KeyError, ValueError) as exc:
   122	                raise GatewayError(f"gateway request failed: "
   123	                                   f"{type(exc).__name__}") from exc
   124	        raise GatewayError("gateway timed out twice") from last_exc
   125	
   126	    def run_turn(self, session: Session, user_text: str | None,
   127	                 emit=lambda event: None) -> str:
   128	        """One customer turn: returns the assistant's final text. Every
   129	        intermediate step goes to emit() and the JSONL log. user_text None
   130	        is the opening turn — the agent greets first, unprompted."""
   131	
   132	        def event(payload: dict) -> None:
   133	            log_event(session, payload)
   134	            emit(payload)
   135	
   136	        if user_text is not None:
   137	            session.messages.append({"role": "user", "content": user_text})
   138	            event({"type": "user", "text": user_text})
   139	
   140	        for _ in range(MAX_TOOL_ROUNDS):
   141	            try:
   142	                message = self._chat_fn(session.messages,
   143	                                        tools.openai_tools())
   144	            except GatewayError as exc:
   145	                event({"type": "error", "error": str(exc)})
   146	                apology = APOLOGY[self.config.lang]
   147	                session.messages.append({"role": "assistant",
   148	                                         "content": apology})
   149	                return apology
   150	
   151	            tool_calls = message.get("tool_calls")
   152	            if not tool_calls:
   153	                text = message.get("content") or ""
   154	                session.messages.append({"role": "assistant",
   155	                                         "content": text})
   156	                event({"type": "assistant", "text": text})
   157	                return text
   158	
   159	            session.messages.append({
   160	                "role": "assistant",
   161	                "content": message.get("content"),
   162	                "tool_calls": tool_calls,
   163	            })
   164	            for call in tool_calls:
   165	                name = call["function"]["name"]
   166	                try:
   167	                    args = json.loads(call["function"]["arguments"] or "{}")
   168	                except ValueError:
   169	                    args = {}
   170	                event({"type": "tool_call", "tool": name, "args": args})
   171	                result = tools.dispatch(session.order, session.menu,
   172	                                        self.client, name, args)
   173	                event({"type": "tool_result", "tool": name,
   174	                       "result": result})
   175	                event({"type": "state",
   176	                       "state": session.order.state.value,
   177	                       "revision": session.order.revision})
   178	                session.messages.append({
   179	                    "role": "tool",
   180	                    "tool_call_id": call.get("id", name),
   181	                    "content": json.dumps(result, ensure_ascii=False),
   182	                })
   183	
   184	        event({"type": "error", "error": "tool loop guard exceeded"})
   185	        apology = APOLOGY[self.config.lang]
   186	        session.messages.append({"role": "assistant", "content": apology})
   187	        return apology
   188	
   189	
   190	def startup(config: AgentConfig) -> tuple[PizzaSim, str, Menu]:
   191	    """The one startup sequence (PLAN): env → pizzeria check → menu.
   192	    Raises before the first turn on any failure."""
   193	    client = PizzaSim.from_env()
   194	    pizzeria_name = client.pizzeria_name()
   195	    menu = Menu(client.get_menu())
   196	    return client, pizzeria_name, menu

codex
I have enough to score. I’m grabbing one last reference around submit-timeout recovery so the highest-severity finding is tied to the exact recovery code path, not just the state bookkeeping.
exec
/bin/bash -lc "nl -ba core/tools.py | sed -n '170,270p'" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 105ms:
codex
Findings:

- [core/state.py](/home/rob/bpm-pizza-vibecoding-solution/core/state.py:29) and [core/tools.py](/home/rob/bpm-pizza-vibecoding-solution/core/tools.py:196): submit-timeout recovery state is not scoped to a basket revision. `_recompute()` demotes `CONFIRMED`, but it never clears `submit_unknown` or `submit_attempted_at`. `_submit()` later uses those stale fields to recover by `first_name` + `created_at`. If a timed-out submit is followed by any basket/customer change and a fresh confirmation, the next `submit_order` can incorrectly adopt the old order for the new basket, or skip the required fresh POST entirely.
- [channels/web.py](/home/rob/bpm-pizza-vibecoding-solution/channels/web.py:96): the web channel allows concurrent turns against the same shared `Session`. Each `/chat` request starts a new thread over the same `session.order` and `session.messages`, with no per-session lock or in-flight guard. Two overlapping requests for one `session_id` can interleave mutations and break the revision-based confirmation guarantees from the spec.
- [core/agent.py](/home/rob/bpm-pizza-vibecoding-solution/core/agent.py:144), [channels/web.py](/home/rob/bpm-pizza-vibecoding-solution/channels/web.py:108), and [channels/static/app.js](/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js:70): on gateway failure or loop-guard exhaustion, `run_turn()` returns the apology text but emits only an `error` event, not an `assistant` event. The web transport streams only emitted events, and the UI renders final assistant text only from `assistant` events. In those error paths, the browser user gets a generic technical notice instead of the promised apology, and the JSONL log also misses the assistant’s final turn.
- [channels/web.py](/home/rob/bpm-pizza-vibecoding-solution/channels/web.py:77): `GET /config` returns `{"speech": ..., "pizzeria": ...}` even though the spec/approved plan fixed that contract to `{speech: bool}`. This is minor, but it is still API drift.

I verified the four round-1 required changes in the files: deterministic `remove_item` semantics and tests, 2xx-required speech probe, 30s gateway timeout, and exact dependency pins. I did not rerun `pytest` in this read-only sandbox; the verdict below is from code inspection plus the live evidence you provided.

SCORES (1-5 each, 5 = best):
completeness: 4
correctness: 3
error_handling: 3
simplicity: 4
spec_compliance: 3
TOTAL: 17/25
VERDICT: CHANGES_REQUIRED
ISSUES: (max 5 bullets, concrete and actionable, empty if approved)
- Clear `submit_unknown` and `submit_attempted_at` on any basket/customer mutation that demotes the order, and add tests covering “timeout, mutate, reconfirm, submit again”.
- Serialize turns per `session_id` in the web channel, or reject a second `/chat` while one is already in flight for that session.
- Emit and log an `assistant` event for gateway-timeout and loop-guard apology paths so the web UI shows the promised final response.
- Align `GET /config` with the fixed contract `{speech: bool}`, or update the approved plan/spec if the extra `pizzeria` field is intentionally part of the API.
tokens used
96,717
Findings:

- [core/state.py](/home/rob/bpm-pizza-vibecoding-solution/core/state.py:29) and [core/tools.py](/home/rob/bpm-pizza-vibecoding-solution/core/tools.py:196): submit-timeout recovery state is not scoped to a basket revision. `_recompute()` demotes `CONFIRMED`, but it never clears `submit_unknown` or `submit_attempted_at`. `_submit()` later uses those stale fields to recover by `first_name` + `created_at`. If a timed-out submit is followed by any basket/customer change and a fresh confirmation, the next `submit_order` can incorrectly adopt the old order for the new basket, or skip the required fresh POST entirely.
- [channels/web.py](/home/rob/bpm-pizza-vibecoding-solution/channels/web.py:96): the web channel allows concurrent turns against the same shared `Session`. Each `/chat` request starts a new thread over the same `session.order` and `session.messages`, with no per-session lock or in-flight guard. Two overlapping requests for one `session_id` can interleave mutations and break the revision-based confirmation guarantees from the spec.
- [core/agent.py](/home/rob/bpm-pizza-vibecoding-solution/core/agent.py:144), [channels/web.py](/home/rob/bpm-pizza-vibecoding-solution/channels/web.py:108), and [channels/static/app.js](/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js:70): on gateway failure or loop-guard exhaustion, `run_turn()` returns the apology text but emits only an `error` event, not an `assistant` event. The web transport streams only emitted events, and the UI renders final assistant text only from `assistant` events. In those error paths, the browser user gets a generic technical notice instead of the promised apology, and the JSONL log also misses the assistant’s final turn.
- [channels/web.py](/home/rob/bpm-pizza-vibecoding-solution/channels/web.py:77): `GET /config` returns `{"speech": ..., "pizzeria": ...}` even though the spec/approved plan fixed that contract to `{speech: bool}`. This is minor, but it is still API drift.

I verified the four round-1 required changes in the files: deterministic `remove_item` semantics and tests, 2xx-required speech probe, 30s gateway timeout, and exact dependency pins. I did not rerun `pytest` in this read-only sandbox; the verdict below is from code inspection plus the live evidence you provided.

SCORES (1-5 each, 5 = best):
completeness: 4
correctness: 3
error_handling: 3
simplicity: 4
spec_compliance: 3
TOTAL: 17/25
VERDICT: CHANGES_REQUIRED
ISSUES: (max 5 bullets, concrete and actionable, empty if approved)
- Clear `submit_unknown` and `submit_attempted_at` on any basket/customer mutation that demotes the order, and add tests covering “timeout, mutate, reconfirm, submit again”.
- Serialize turns per `session_id` in the web channel, or reject a second `/chat` while one is already in flight for that session.
- Emit and log an `assistant` event for gateway-timeout and loop-guard apology paths so the web UI shows the promised final response.
- Align `GET /config` with the fixed contract `{speech: bool}`, or update the approved plan/spec if the extra `pizzeria` field is intentionally part of the API.
