OpenAI Codex v0.143.0
--------
workdir: /home/rob/bpm-pizza-vibecoding-solution
model: gpt-5.4
provider: openai
approval: never
sandbox: read-only
reasoning effort: medium
reasoning summaries: none
session id: 019fbc76-54c8-70a1-86fe-38f76438411c
--------
user
You are an independent reviewer for the repository in the current working directory. Read-only; you never write code. Devil's advocate + judge in one pass, scoring against the fixed rubric in SPEC.md.

Task: Review the v2 IMPLEMENTATION (round 2 of max 3) against SPEC.md (v3, patched, gate-approved) and PLAN.md (v2, approved 23/25, tickets checked off). Round 1 (stateless, reviews/round17-impl2.md) required four changes; all applied — verify in the files, do not take this on faith:
1. Spoken-style note is now ephemeral per turn (core/agent.py run_turn: `extra` list passed to the chat call, never appended to session.messages); regression test tests/test_tools.py::test_spoken_note_is_ephemeral_per_turn covers spoken-then-typed.
2. /chat and /confirm 404: channels/static/app.js streamPost now recreates the session transparently and renders a notice with a resend control carrying the original text; E2E test_e2e_lost_session_recreates_and_offers_resend.
3. Real client-side timeout: AbortSignal.any([user abort, AbortSignal.timeout(120s)]) covers request and streamed body; TimeoutError renders the timeout notice with resend.
4. startSession no longer clears chat/basket before /session succeeds; a failed pizzeria switch keeps the live conversation and basket visible and resets the selector; E2E test_e2e_vanished_pizzeria_refreshes_selector now asserts basket+chat survive the failed switch.

Facts you cannot observe from the files, all demonstrated live: the offline suite passes — 102 passed, 1 skipped (opt-in live test), including 11 API-surface tests and 8 Playwright browser E2E tests asserting the DOM (full order with the complete header/footer contract, pizzeria switch + language chrome, vanished pizzeria with preserved basket, lost session with resend, tool error, gateway unreachable, stream without answer with successful resend); the live acceptance test PASSED against the real API (submit, then customer/items/quantities verified via list + detail endpoints). Your sandbox may lack a writable temp dir for pytest; judge from code plus this evidence if so.

Scope notes: tests/fixtures/*.json are recorded real API responses; tests/stubs.py is the offline stub pair (scripted model in the golden-transcript spirit — the product itself contains no parser). decisions/qa.md holds the binding oracle decisions.

Judging guidance: score the implementation that exists. Remaining nice-to-haves a maintainer would file as minor follow-ups belong in ISSUES only if they breach SPEC.

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

2026-08-01T08:35:02.075791Z ERROR codex_api::endpoint::responses_websocket: failed to connect to websocket: IO error: Connection reset by peer (os error 104), url: wss://chatgpt.com/backend-api/codex/responses
codex
Using `using-superpowers` first, then I’ll read `SPEC.md`, `PLAN.md`, the prior round review, and the implementation/tests that claim to address those four required changes.
exec
/bin/bash -lc "sed -n '1,260p' PLAN.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,220p' /home/rob/.agents/skills/using-superpowers/SKILL.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,240p' reviews/round17-impl2.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' SPEC.md" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 283ms:
# PizzaSim Ordering Agent — Implementation Plan v2

> Stage-1 artifact for SPEC.md (v3, patched, gate-approved in Issue #1).
> Retrofit of the approved v1 build per the grill verdict in
> `decisions/qa.md` (RETROFIT, 5 binding conditions). Design only — no code.

**Goal:** Extend the approved v1 agent to SPEC v3: customer-selectable
pizzerias, prices and code-owned totals, the full web-channel contract
(header/footer/basket/confirm control/answer invariant), APP_VERSION,
per-session language, and a mandatory offline browser E2E suite.

**Architecture:** unchanged core idea — the order is a state machine owned
by code, the model only speaks. What moves: everything tenant-, language-
and menu-scoped moves from process-global into a per-session `Session`
owned by core. Channels stay transports; the web UI is rebuilt to the new
contract.

**Tech stack:** Python 3.13, httpx, FastAPI + uvicorn, pytest, Playwright
(browser E2E, already installed), stdlib elsewhere. No new dependencies
beyond Playwright.

## What carries over unchanged from v1 (approved 24/25)

- `core/order.py` Order/Item/Customer + revision + submit bookkeeping
- `core/state.py` transitions, invariants 1–5, demotion, terminality,
  deterministic `remove_item` semantics (now also written into SPEC)
- `core/menu.py` (type, code) validation, candidates, extras vocabulary
- `core/pizzasim.py` typed errors, timeouts, list+detail endpoints,
  submit-timeout recovery (shortlist via list, verify items via detail —
  exactly what the patched SPEC now demands)
- `core/tools.py` schemas/dispatch incl. atomic add, error shape
- `core/agent.py` model loop, retry-once, JSONL logging, stub-model seam
- CLI channel, prompts, 71 deterministic tests, golden transcripts

## The five binding retrofit conditions (decisions/qa.md) → where honored

| Condition | Where in this plan |
|---|---|
| 1. `PIZZERIA_LANG` documented | now in SPEC's env table; config section below |
| 2. Core-owned session factory, immutable tenant | "Session model v2" |
| 3. Confirm path via one core method | "Confirm control" |
| 4. Web = substantial rewrite | "Web channel v2" + tickets 6–7 |
| 5. Totals canonical in core + E2E coverage | "Prices and totals", ticket 1, 9 |

## Configuration

| Module | Vars |
|---|---|
| `core/agent.py` | `LITELLM_PIZZA_URL`, `LITELLM_PIZZA_KEY`, `LITELLM_PIZZA_MODEL_1`, `PIZZERIA_LANG` (required; `LITELLM_PIZZA_MODEL_2` read, unused) |
| `core/pizzasim.py` | `PIZZASIM_URL`, `PIZZASIM_API_KEY`, `PIZZERIA_ID` (required) |
| `channels/web.py` | `APP_VERSION` (required) |
| `channels/speech.py` | `SPEECH_URL`, `SPEECH_STT_MODEL`, `SPEECH_TTS_MODEL`, `SPEECH_TTS_VOICE` (all optional; absence disables speech) |

Loading unchanged: process env, else `~/.env`; missing required var →
exit before the first turn naming variable and file. `APP_VERSION` must
match `x.y.z` (regex on the value is config validation, not order
parsing). Derived URLs, never literal: dashboard
`{PIZZASIM_URL}/dashboard/pizzerias/{id}`, docs
`{PIZZASIM_URL}/swagger.html`.

## Session model v2 (condition 2)

`Session` (core/agent.py): `{id, pizzeria_id, pizzeria_name, client,
menu, lang, order, messages}` — pizzeria fields and client are set at
creation and never mutated (a tenant switch is a NEW session; invariant 6).

Core factory `create_session(config, base, pizzeria_id, lang)`:

1. `base.list_pizzerias()` (tenant-free call) → id must be present, else
   typed `NotFoundError` → channel renders "that pizzeria isn't available
   right now" (session error; process stays up, per the new error row).
2. Build a tenant-bound `PizzaSim` client for `pizzeria_id`.
3. Fetch the fresh, immutable menu snapshot for this session (invariant 5).
4. Render `prompts/system.{lang}.md` with the pizzeria name.

Startup (unchanged semantics, now explicit about roles): validate required
env; `GET /pizzerias` must contain the preselected `PIZZERIA_ID` (else the
process refuses to start — the startup 404 row); fetch `/menu` once as a
health check ("We're not taking orders right now" on failure). The
preselection is only the default for new sessions.

CLI: one session from `PIZZERIA_ID` + `PIZZERIA_LANG`; no switching (per
SPEC's language-authority rule and header-only selector).

## Language authority (condition 1)

`Session.lang` starts from the channel: CLI and web default =
`PIZZERIA_LANG`; the web header switch calls `set_language(session, lang)`
(core), which re-renders `messages[0]` from the prompt file in the new
language — same policy text, history preserved. Apologies and the STT/TTS
language read `session.lang`. Reply language stays per-turn mirroring by
the model (prompt rule) and always wins over the switch, exactly as SPEC
states. UI chrome strings are a small de/en dictionary in `app.js`, keyed
by the session language.

## Prices and totals (condition 5)

- `Menu` keeps `price` per (type, code); `as_tool_result()` returns
  `{code, name, price}` per item plus `toppings[]`.
- `Item` gains `unit_price`, copied at add time from the session menu
  snapshot (prices are stable for the session, like the menu itself).
- `Order.snapshot()` gains per line `unit_price`, `line_total`
  (= qty × unit_price) and top-level `basket_total` — computed in
  `core/order.py` only. Money is rounded to cents with `Decimal`;
  no float accumulation.
- `read_back` carries the snapshot and therefore the canonical total; the
  web basket renders the same numbers. Extras carry no API price → lines
  show base prices; the UI labels extras "not separately priced" — no
  invented figures.
- The model never computes prices: the prompt instructs it to quote
  `price`/`basket_total` from tool results verbatim.

## Tools — v1 contract plus prices

Schemas and parameters unchanged (fixed by SPEC). Result changes only:

- `get_menu` → `{menu: {pizzas: [{code, name, price}], pasta: [...],
  toppings: [...]}, snapshot}`
- `SNAPSHOT` → `{state, revision, items: [{type, code, name, qty, extras,
  unit_price, line_total}], basket_total, customer, read_back_done}`
- everything else exactly as approved in v1 (uniform error shape,
  atomicity, invalid_quantity, deterministic remove).

## Confirm control (condition 3)

- `read_back` results stream to the UI (they already do); the UI renders a
  visually distinct read-back panel with a **Bestellen/Confirm** button
  bound to the streamed `revision`.
- Click → `POST /confirm {session_id, revision}` → **one core method**
  `Agent.confirm_and_submit(session, revision, emit)` with **symmetric
  success/failure semantics** — one path, not two:
  1. `tools.dispatch("confirm_order", {revision})`; on success also
     `tools.dispatch("submit_order", {})` (full v1 semantics incl.
     timeout recovery).
  2. **Every** dispatch performed — successful or failed — is appended to
     `session.messages` as a synthetic assistant `tool_calls` message +
     `tool` result (OpenAI format) and emitted/logged as the usual
     `tool_call`/`tool_result`/`state` events. The model's context and
     the JSONL log are identical in shape to a model-initiated call.
  3. One model call then phrases the outcome to the customer — the order
     id in groups and minutes on success, or the refusal in plain words
     on failure (stale revision → "the order changed, let me read it back
     again"), exactly the SPEC's "the refusal is a tool result the model
     must deal with in front of the customer". It streams like a normal
     turn. The UI additionally refreshes the basket panel from the
     streamed snapshot; nothing is submitted on a failed confirm.
  4. The phrasing call goes through the **same gateway path as every
     turn** — same timeout, same retry-once, same apology emitted as an
     `assistant` event on failure — so `/confirm` satisfies the
     answer-or-rendered-error invariant even when the gateway dies after
     the order was submitted (the order id is already in the snapshot the
     UI received; the apology never claims the order failed). Unit test:
     gateway failure during post-confirm phrasing → dispatches applied,
     apology streamed as `assistant`, state consistent.
- The customer action is a click, not a word; `CONFIRMED` remains
  reachable only via `confirm_order(revision)`; the transport forwards two
  identifiers and owns zero logic.
- CLI keeps the conversational path: customer says yes → model calls
  `confirm_order` + `submit_order` itself. Both paths converge on dispatch.

## Web channel v2 (condition 4 — a rewrite, named as such)

Server (`channels/web.py`):

- `GET /config` → `{version, speech, lang_default, pizzerias:
  [{id, name}] | null, preselected_id, dashboard_base, docs_url}`.
  `pizzerias: null` when `GET /pizzerias` failed at request time — the UI
  then shows "list unavailable" and no selector (no fallback entry).
- `POST /session {pizzeria_id?, lang?}` → creates a Session (defaults:
  preselected id, `PIZZERIA_LANG`), returns `{session_id, pizzeria_id,
  pizzeria_name, lang}`. Invalid/vanished id → 409 with the session-error
  text; the UI then **re-fetches `/config`** (which performs a fresh
  `GET /pizzerias`), re-renders the selector from that live list — or the
  "list unavailable" state if the fetch fails — and shows the notice.
  Covered by a TestClient test (409 + fresh list served) and an E2E
  scenario (stub drops a pizzeria between load and selection).
- `POST /chat {session_id, text|null}` → NDJSON stream (unchanged
  protocol; `text: null` = greeting turn). 404 for unknown session (the
  UI then creates a fresh one). Per-session lock → 409 on overlap.
- `POST /confirm {session_id, revision}` → NDJSON stream (same event
  shapes) via `confirm_and_submit`.
- `POST /language {session_id, lang}` → `{lang}`; core `set_language`.
- `GET /health` → `{api: "ok"|"down", gateway: "ok"|"down"|"unknown"}`.
  Exact semantics: `api` is measured live per `/health` request
  (`GET /pizzerias`, 3s timeout — ok on 2xx, down otherwise). `gateway`
  is a **process-wide** last-known status: `unknown` until the first
  model call anywhere; every gateway call by any session through either
  `/chat` or `/confirm` (both share the single Agent gateway path) sets
  it — `ok` on a successful completion, `down` when a call exhausts its
  retry and aborts the turn; the next success flips it back to `ok`.
  `/health` itself never calls the gateway (no cost, no side effects).
  Polled by the UI every 30s for the footer badges. Tests: TestClient —
  fresh app → `unknown`; scripted turn → `ok`; stub gateway failure →
  `down`; subsequent success → `ok`; `api` flips with the stub PizzaSim
  up/down. E2E asserts the badges render these states.
- Speech proxy endpoints move to `channels/speech.py` (deliverable):
  `SpeechService` class (config, probe, stt(audio, lang), tts(text,
  lang)); web.py keeps only the thin route handlers.

**Speech behaviour (full SPEC coverage, not just the STT hint):**

- STT **and** TTS requests carry `session.lang` as the language; no
  separate speech-language config (SPEC's language-authority rule).
- Synthesis is **off by default**, toggled by the customer, applied only
  to the **final** assistant message of a turn — never to intermediate
  steps (v1 behaviour, kept and E2E-visible: the toggle exists only when
  speech is enabled).
- Spoken-answer policy: `POST /chat` gains optional `spoken: true`, set by
  the UI when the input came from the microphone or the TTS toggle is on.
  Core appends a one-line per-turn note instructing spoken style (≤3 menu
  items + invitation, minutes not seconds, order id in groups) — the
  policy itself lives in the system prompt; the flag only activates it.
  Unit test: flag → note present; no flag → absent.
- Push-to-talk with visible recording state; a failed STT/TTS call shows a
  notice and never touches the order (v1, kept). Manual checklist in
  README as SPEC requires.

UI (`channels/static/` — rebuilt):

- **Header:** pizzeria name (prominent, from the session), selector
  (name + first 8 UUID chars, from `/config.pizzerias`), dashboard link
  (`dashboard_base` + id, `target="_blank"`), language switch DE/EN,
  Start over. Selector change and Start over both: abort any in-flight
  stream (AbortController), clear the chat and basket views, create a NEW
  session (fresh id — invariant 6 by construction), render the greeting
  turn.
- **Footer:** `version`, full selected UUID (selectable text), connection
  badges from `/health`, docs link.
- **Basket panel:** rendered from every `snapshot` in tool results /
  `done` events: lines with qty × name, `line_total`, `basket_total`;
  after `state == "SUBMITTED"`: locked, shows order id + "submitted", no
  control on the page can modify or resubmit (confirm button removed,
  input stays usable for a new conversation via Start over / new session).
- **Read-back panel:** on a `read_back` tool result: visually distinct
  block + confirm button bound to the streamed revision.
- **Answer invariant** ("no message ends unanswered"):
  - send → immediate "agent is working" indicator;
  - tool events render as they stream (collapsible steps, visually
    distinct) — never discarded (anti-pattern 6);
  - `done` without a preceding `assistant` event in the turn → rendered
    notice "the agent did not answer — resend?";
  - fetch error / abort / non-2xx → rendered notice naming which
    (error, timeout, connection lost) + a resend button that re-posts the
    same text;
  - all notices in plain words, in the **customer's language**, defined
    as follows.
- **Notice-language rule (explicit decision):** UI-generated text (chrome,
  notices, resend prompts) follows `session.lang` — the language the
  customer chose via the header switch, or the default before any choice.
  The UI performs **no language detection** (a heuristic would be a
  parser-shaped guess, and model replies already mirror per turn); the
  switch is the customer's declaration of their language toward the UI.
  Tested: switch to EN → subsequent notices render in English (E2E).

## CLI v2

Unchanged flow; read_back output now includes line totals and the basket
total from the snapshot (printing what core computed, no arithmetic).

## Error handling — new rows on top of v1's table

 succeeded in 334ms:
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

 succeeded in 390ms:
OpenAI Codex v0.143.0
--------
workdir: /home/rob/bpm-pizza-vibecoding-solution
model: gpt-5.4
provider: openai
approval: never
sandbox: read-only
reasoning effort: medium
reasoning summaries: none
session id: 019fbc71-7bb8-7f82-9cc1-4cebe594c151
--------
user
You are an independent reviewer for the repository in the current working directory. Read-only; you never write code. Two roles in one pass:
1. Devil's advocate: attack the implementation — bugs, gaps, missing error cases, spec violations, divergence from the approved plan.
2. Judge: score against the fixed rubric in SPEC.md.

Task: Review the v2 IMPLEMENTATION against SPEC.md (v3, patched, gate-approved) and PLAN.md (v2, approved 23/25, all tickets checked off). The v2 delta on top of the previously approved v1 build: prices/totals in core (core/order.py, core/menu.py, core/tools.py), per-session tenancy via a core session factory + language authority + confirm_and_submit (core/agent.py), web API v2 (channels/web.py: /config /session /chat /confirm /language /health), channels/speech.py, fully rebuilt UI (channels/static/), offline stubs (tests/stubs.py) and the browser E2E suite (tests/test_web_e2e.py), plus extended unit/tool tests.

Facts you cannot observe from the files, all demonstrated live before this review: the offline suite passes — 101 passed, 1 skipped (the opt-in live test), including 11 API-surface tests and 6 Playwright browser E2E tests asserting against the DOM (full order with header/footer contract, pizzeria switch + language, vanished pizzeria, tool error, gateway unreachable, stream without answer); the live acceptance test PASSED against the real API (full conversation at the tool layer, submit, then customer/items/quantities verified via the pizzeria's list + detail endpoints). Your sandbox may lack a writable temp dir for pytest; judge from code plus this evidence if so.

Scope notes: tests/fixtures/*.json are recorded real API responses. venv/, logs/, node-free static assets are as committed. decisions/qa.md records oracle decisions; the five retrofit conditions there are binding and PLAN.md maps them.

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

APPROVED requires TOTAL >= 20 and no dimension below 4. Maximum 3 rounds.

codex
Reviewing the repository against `SPEC.md`, `PLAN.md`, and the cited implementation areas. I’ll gather the spec/plan context first, then inspect the v2 delta and tests, and I’ll keep this read-only.
exec
/bin/bash -lc "sed -n '1,220p' /home/rob/.agents/skills/using-superpowers/SKILL.md" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 156ms:
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
Using `using-superpowers` to determine the required review workflow before inspecting the code. Next I’m checking the Codex-specific instructions and then the review-relevant skills.
exec
/bin/bash -lc "sed -n '1,240p' /home/rob/.agents/skills/using-superpowers/references/codex-tools.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' /home/rob/.agents/skills/requesting-code-review/SKILL.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' /home/rob/.agents/skills/brainstorming/SKILL.md" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 124ms:
---
name: requesting-code-review
description: Use when completing tasks, implementing major features, or before merging to verify work meets requirements
---

# Requesting Code Review

Dispatch a code reviewer subagent to catch issues before they cascade. The reviewer gets precisely crafted context for evaluation — never your session's history.

**Core principle:** Review early, review often.

## When to Request Review

**Mandatory:**
- After each task in subagent-driven development
- After completing major feature
- Before merge to main

**Optional but valuable:**
- When stuck (fresh perspective)
- Before refactoring (baseline check)
- After fixing complex bug

## How to Request

**1. Get git SHAs:**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

**2. Dispatch code reviewer subagent:**

Dispatch a `general-purpose` subagent, filling the template at [code-reviewer.md](code-reviewer.md)

**Placeholders:**
- `{DESCRIPTION}` - Brief summary of what you built
- `{PLAN_OR_REQUIREMENTS}` - What it should do
- `{BASE_SHA}` - Starting commit
- `{HEAD_SHA}` - Ending commit

**3. Act on feedback:**
- Fix Critical issues immediately
- Fix Important issues before proceeding
- Note Minor issues for later
- Push back if reviewer is wrong (with reasoning)

## Example

```
[Just completed Task 2: Add verification function]

You: Let me request code review before proceeding.

BASE_SHA=$(git log --oneline | grep "Task 1" | head -1 | awk '{print $1}')
HEAD_SHA=$(git rev-parse HEAD)

[Dispatch code reviewer subagent]
  DESCRIPTION: Added verifyIndex() and repairIndex() with 4 issue types
  PLAN_OR_REQUIREMENTS: Task 2 from docs/superpowers/plans/deployment-plan.md
  BASE_SHA: a7981ec
  HEAD_SHA: 3df7661

[Subagent returns]:
  Strengths: Clean architecture, real tests
  Issues:
    Important: Missing progress indicators
    Minor: Magic number (100) for reporting interval
  Assessment: Ready to proceed

You: [Fix progress indicators]
[Continue to Task 3]
```

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "I'll just review the diff myself instead of dispatching a reviewer" | You're the coordinator — reviewing the diff inline burns the context window you need to keep driving the work. Dispatch a reviewer subagent: the diff and the evaluation live in its context, and only the findings come back to you. |
| "The reviewer needs my whole session history to understand the change" | Hand it precisely crafted context, never your session's history. That keeps the reviewer on the work product, not your thought process. |

## Red Flags

**Never:**
- Skip review because "it's simple"
- Ignore Critical issues
- Proceed with unfixed Important issues
- Argue with valid technical feedback

**If reviewer wrong:**
- Push back with technical reasoning
- Show code/tests that prove it works
- Request clarification

See template at: [code-reviewer.md](code-reviewer.md)

 succeeded in 142ms:
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

 succeeded in 367ms:
# PizzaSim Ordering Agent — Specification

> Hand this to a coding agent as the entire task:
> `FOLLOW INSTRUCTIONS PRECISELY AT "SPEC.MD"`.
> This file is the source of truth for what the product is. Everything else in
> the repo — code, tests, prompts, tickets — derives from it.

---

## Where this format comes from

The **shape** of this document is not ours. It is borrowed from Cedric Mössner —
**The Morpheus** ([youtube.com/@TheMorpheusTutorials](https://www.youtube.com/@TheMorpheusTutorials)),
who writes exactly one `SPEC.md` per project and hands the identical file to
every new model in order to compare them. The prompt he sends alongside it is a
single line — `FOLLOW INSTRUCTIONS PRECISELY AT "SPEC.MD"` — which is why that
line, and not a long prompt, stands at the top of this file.

Sections adopted from his specs: *Soul*, *The One Load-Bearing Idea*, hard
*Scope In / Out*, an explicit autonomy clause, work *in passes* with
verification after each, a file-level *Deliverables* list, *Decisions Locked /
Deferred*, and the one-hour *ticket sizing rules*.

Reference specs:
[morphcook](https://github.com/TheMorpheus407/morphcook) — offline Flutter
recipe app; one spec, seven model implementations.
[hogwarts-blender-benchmark](https://github.com/TheMorpheus407/hogwarts-blender-benchmark)
— fully procedural Blender build; `prompt.txt` plus `SPEC.md`.

The content below is ours. The form is his — with thanks.

---

## What done looks like

There is exactly one success condition, and everything else in this document
exists to serve it:

**A customer talks to the agent, and the resulting order appears in the API
under the pizzeria they chose — with the right customer, the right items, the
right quantities.**

Concretely, and this is the acceptance criterion:

1. `POST /pizzerias/{id}/orders` returned an order id.
2. Reading that pizzeria's orders back shows the order, and it is visible on
   that pizzeria's dashboard.
3. The customer name is the one the customer gave.
4. The items and quantities are the ones that were read back and confirmed —
   not a superset, not a subset, not a near match on the item code.

Nothing else counts as done. A green test suite, a clean architecture, a
pleasant interface: none of it is the product. **The order on the board is the
product.**

**Four failures that look like success**, each a failed run and not a partial
one:

- The order landed under a **different pizzeria** than the one the customer
  chose.
- A retry after a timeout created the order **twice**.
- A misheard or mistyped name created a **new customer** instead of matching
  the intended one.
- The order was submitted **without the customer confirming** the read-back.

Every rule below — the state machine, the revision-bound confirmation, the ban
on blind retries, the name read-back, the tenant in the URL path — exists to
prevent exactly one of those four.

---

## Soul

Ordering food by phone works because the person on the other end keeps the
order in their head, reads it back to you, and only then walks to the kitchen.
Nothing is cooked before you said yes.

Most LLM ordering demos invert this. The model holds the order in its context,
guesses item names that sound close enough, and fires the write call the moment
it feels confident. It works in the demo and fails on the fourth turn, in a
noisy room, when the customer changes their mind.

This agent puts the order back where it belongs: **in the code**. The model
does the one thing it is genuinely good at — turning messy human speech into
intent — and nothing else. It never holds the cart, never invents a menu item,
and never reaches the kitchen without a confirmed read-back.

**Core belief:** a language model is a great waiter and a terrible order pad.

---

## The One Load-Bearing Idea

**The order is a state machine owned by the code. The model only speaks.**

- Exactly one `Order` object per conversation, held by the runtime.
- The model cannot write to it directly. It calls tools that request a
  transition, and every transition is validated before it is applied.
- Every item code is validated against the **live menu**. An unknown code is a
  tool error carrying candidate matches — never a silent guess, never a
  fallback to a hardcoded list.
- `submit_order` is the only network write, legal in exactly one state:
  `CONFIRMED`. The only way into `CONFIRMED` is a read-back the customer
  answered yes to.
- One core serves every channel. A transport carries words in and words out;
  it owns no order logic whatsoever.

This one rule replaces prompt-engineering the model into good behaviour. If the
model misbehaves, the state machine refuses — and the refusal is a tool result
the model must deal with in front of the customer.

---

## Scope

### In

- **Two transports over one core:**
  - `cli` — interactive terminal chat.
  - `web` — FastAPI server on port 8888, browser chat UI, streaming the
    agent's intermediate steps as newline-delimited JSON so tool calls and
    tool results are visible, not just the final answer.
- **Speech on the web transport**, served by a self-hosted CPU-only speech
  container over HTTP. See *Speech*.
- **Several pizzerias.** The customer chooses which one they are ordering
  from, and can change it. `PIZZERIA_ID` is the preselection, not a
  restriction.
- **Languages:** German and English. The agent answers in the language the
  customer used, per turn, without being told to switch.
- **Menu, prices, cart, customer, submit.** The full happy path plus
  correction ("no, make that three"), removal, and abandonment. The customer
  can ask what is on offer and what items cost, and sees what the basket
  comes to before confirming.
- **Deterministic tests** that run with no network and no LLM, plus one live
  acceptance test and a browser end-to-end test.
- **Structured logging** of every turn: user text, model tool calls, tool
  results, state transitions. One line per event, JSON, to a file.

### Out (explicitly)

- Payment and anything financial beyond showing prices the API supplies.
- Delivery routing, or an ETA of our own invention.
- Accounts, auth, sessions surviving a process restart.
- Modifying or cancelling an order after it was submitted.
- Any regex or keyword parser that produces an order without the model.
  See **Anti-patterns**; this is a hard ban, not a style preference.
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
| `LITELLM_PIZZA_MODEL_1` | Model the ordering agent calls; required, no default in code |
| `LITELLM_PIZZA_MODEL_2` | Second configured model, where the build uses one |
| `PIZZASIM_URL` | PizzaSim API base URL; dashboard and docs links derive from it |
| `PIZZASIM_API_KEY` | Sent as header `X-API-Key` on protected routes |
| `PIZZERIA_ID` | UUID of the pizzeria preselected on first load |
| `PIZZERIA_LANG` | Initial language, `de` or `en`: the greeting, the CLI, and the web UI before the customer switches |
| `APP_VERSION` | Release version, `x.y.z`, shown in the footer |
| `SPEECH_URL` | Base URL of the self-hosted speech service (optional) |
| `SPEECH_STT_MODEL` | Transcription model id |
| `SPEECH_TTS_MODEL` | Synthesis model id |
| `SPEECH_TTS_VOICE` | Voice id |

Rules:

- **Nothing is hardcoded.** No UUID, no model name, no menu, no base URL, no
  vendor — not even as a fallback "just in case".
- Missing or empty required variable → exit before the first turn with a
  message naming the variable and the file it was expected in. Never start
  half-configured. `SPEECH_*` are the exception: absent means the speech
  features are not rendered, and everything else works.
- Secrets never appear in logs, transcripts, error messages or the web UI.

---

## The PizzaSim API (contract)

Facts below are **verified** — against running code or a live response. A
verified fact never moves back into the open list; the open list only shrinks.

| Call | Auth | Notes |
|---|---|---|
| `GET /menu` | public | returns `pizzas[]` and `pasta[]`, each with `code` |
| `GET /pizzerias` | `X-API-Key` | list of pizzerias with `id`, `name` |
| `GET /pizzerias/{id}/orders` | `X-API-Key` | that pizzeria's orders; used by timeout recovery |
| `POST /pizzerias/{id}/orders` | `X-API-Key` | places the order |
| `GET /location?street=…` | public | street plausibility check (optional tool) |

Order request body:

```json
{
  "customer": { "first_name": "Marco", "street_one": "via di Cantieri" },
  "items": [{ "type": "pizza", "code": "margherita", "qty": 2, "extras": [] }]
}
```

Response carries `order_id`, `status`, `eta_seconds`.

Derived URLs — built from `PIZZASIM_URL`, never hardcoded:

- Dashboard of a pizzeria: `{PIZZASIM_URL}/dashboard/pizzerias/{id}`
  (verified against the dashboard's routing code).
- API documentation: `{PIZZASIM_URL}/swagger.html` — there is **no** `/docs`.

Facts that shape behaviour:

- The tenant is **always** in the URL path, never in a header. The API key is
  a server key, not a pizzeria id.
- Customers are unique per pizzeria **by first name**. An unknown name
  silently creates a new customer — a misheard name creates a ghost. Speech
  input must therefore confirm the name explicitly.
- `street_one` is optional and **not** validated for deliverability. Asking
  for it is a policy of this agent — never claim to have checked an address.
- `POST /orders` is **not** idempotent. A retry after a timeout can double a
  real order. See **Error handling**.

Further verified facts (live responses, 2026-07-31/08-01):

- **Menu item shape:** `{"code", "name", "base": [ingredients], "price"}`.
  `price` is a number in euros — the source for every price answer and the
  basket total; no other financial data exists in the API. `name` is a
  single string (identical in DE and EN; there are no per-language names).
  The menu response also carries a top-level `toppings[]` array.
- **`extras[]` is a controlled vocabulary:** the `toppings[]` from
  `GET /menu`. The server rejects unknown extras with `422`
  (`"items[0].extras contains invalid topping 'unicorn_dust'"`); the tool
  layer validates extras against `toppings[]` exactly like item codes.
- **Error bodies are machine-readable:**
  `{"error": "<code>", "details": ["<human sentence>", ...]}` (e.g.
  `validation_failed` with HTTP 422) — mapped to typed errors; `details`
  may feed targeted questions.
- **Status values observed:** `ordered` → `prepared_planned` → `delivered`
  (with `delivered_at` set on the last). A fresh order starts as `ordered`.
- **`GET /location?street=` returns** `{"street": "<echo>",
  "deliverable": <bool>}`, HTTP 200 — `deliverable: true` even for nonsense
  input, so it is a weak plausibility signal at best: never tell the
  customer an address was verified.
- **The list endpoint carries no items.** The detail endpoint
  `GET /pizzerias/{id}/orders/{order_id}` (auth: `X-API-Key`) returns the
  full order incl. `customer` and `items[]`. Submit-timeout recovery
  shortlists by `first_name` + `created_at` recency on the list, then
  verifies the candidate's items via the detail endpoint before adopting
  it; the live acceptance test asserts items and quantities through the
  same detail endpoint.
- **Item codes are unique per type, not globally** — `tonno` exists as a
  pizza and a pasta. Validation and removal always key on `(type, code)`.

### Open contract questions — shrink-only

Resolve against the live API before the affected component is implemented,

codex
Using `using-superpowers` for workflow discipline. No implementation skill applies here; this is a repository review, so I’m inspecting the concrete code paths and tests that should prove the four round-1 fixes and the remaining SPEC/PLAN obligations.
exec
/bin/bash -lc 'rg -n "run_turn|spoken|extra|streamPost|AbortSignal|startSession|/confirm|/chat|timeout|recreates_and_offers_resend|vanished_pizzeria|spoken_note_is_ephemeral_per_turn|TimeoutError|resend" core channels tests -S' in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,220p' /home/rob/.agents/skills/using-superpowers/references/codex-tools.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc 'rg --files core channels tests decisions | sort' in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 674ms:
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

 succeeded in 733ms:
tests/test_web_e2e.py:57:    with httpx.Client(base_url=stack["url"], timeout=30.0) as client:
tests/test_web_e2e.py:93:    events = stream_lines(api, "/chat",
tests/test_web_e2e.py:107:    assert api.post("/chat", json={"session_id": "ghost",
tests/test_web_e2e.py:116:        response = api.post("/chat", json={"session_id": sid, "text": "x"})
tests/test_web_e2e.py:136:    stream_lines(api, "/chat", {"session_id": sid, "text": None})
tests/test_web_e2e.py:137:    events = stream_lines(api, "/chat",
tests/test_web_e2e.py:151:    stream_lines(api, "/chat", {"session_id": sid, "text": None})
tests/test_web_e2e.py:152:    stream_lines(api, "/chat", {"session_id": sid,
tests/test_web_e2e.py:154:    events = stream_lines(api, "/chat", {"session_id": sid,
tests/test_web_e2e.py:159:    events = stream_lines(api, "/confirm",
tests/test_web_e2e.py:173:                                "qty": 2, "extras": []}]
tests/test_web_e2e.py:179:    stream_lines(api, "/chat", {"session_id": sid,
tests/test_web_e2e.py:181:    events = stream_lines(api, "/confirm",
tests/test_web_e2e.py:202:    page.goto(stack["url"], timeout=30000)
tests/test_web_e2e.py:203:    page.wait_for_selector(".msg.assistant", timeout=30000)
tests/test_web_e2e.py:225:    page.wait_for_selector("#health-api.ok", timeout=15000)
tests/test_web_e2e.py:226:    page.wait_for_selector("#health-gateway.ok", timeout=15000)
tests/test_web_e2e.py:236:    page.wait_for_selector("text=8.5 €", timeout=30000)
tests/test_web_e2e.py:239:    page.wait_for_selector("#basket-lines li", timeout=30000)
tests/test_web_e2e.py:244:    page.wait_for_selector(".readback button:enabled", timeout=30000)
tests/test_web_e2e.py:250:                           timeout=30000)
tests/test_web_e2e.py:265:    page.wait_for_selector("#basket-lines li", timeout=30000)
tests/test_web_e2e.py:270:        "'Stub Pizzeria Due'", timeout=30000)
tests/test_web_e2e.py:273:    page.wait_for_selector(".msg.assistant", timeout=30000)  # fresh greet
tests/test_web_e2e.py:278:        "'Start over'", timeout=15000)  # chrome follows the declared lang
tests/test_web_e2e.py:282:def test_e2e_vanished_pizzeria_refreshes_selector(page_factory, stack):
tests/test_web_e2e.py:287:    page.wait_for_selector("#basket-lines li", timeout=30000)
tests/test_web_e2e.py:292:        page.wait_for_selector(".notice", timeout=30000)
tests/test_web_e2e.py:295:            ".length === 1", timeout=15000)
tests/test_web_e2e.py:304:def test_e2e_lost_session_recreates_and_offers_resend(page_factory,
tests/test_web_e2e.py:307:    sees a plain notice, gets a fresh session, and can resend."""
tests/test_web_e2e.py:313:    page.wait_for_selector(".notice button", timeout=30000)  # resend
tests/test_web_e2e.py:315:    page.wait_for_selector("text=8.5 €", timeout=30000)
tests/test_web_e2e.py:324:    page.wait_for_selector("text=nicht im Angebot", timeout=30000)
tests/test_web_e2e.py:337:        page.wait_for_selector("text=schiefgegangen", timeout=30000)
tests/test_web_e2e.py:343:def test_e2e_stream_without_answer_offers_resend(page_factory, stack):
tests/test_web_e2e.py:350:        page.wait_for_selector(".notice button", timeout=30000)
tests/test_web_e2e.py:353:    page.locator(".notice button").last.click()  # resend, now answered
tests/test_web_e2e.py:356:        timeout=30000)
tests/transcripts/submit_timeout.json:2:  "name": "submit_timeout",
tests/transcripts/submit_timeout.json:3:  "fake": "timeout_then_recover",
tests/transcripts/submit_timeout.json:7:       {"tool": "add_items", "args": {"items": [{"type": "pizza", "code": "hawaii", "qty": 1, "extras": []}]}},
tests/transcripts/mind_change.json:7:       {"tool": "add_items", "args": {"items": [{"type": "pizza", "code": "diavolo", "qty": 1, "extras": []}]}},
tests/transcripts/mind_change.json:14:       {"tool": "add_items", "args": {"items": [{"type": "pizza", "code": "funghi", "qty": 1, "extras": []}]}},
channels/cli.py:54:    print(agent.run_turn(session, None, emit))  # agent greets first
channels/cli.py:63:        print(agent.run_turn(session, text, emit))
channels/static/index.html:29:    <div id="basket-extras-note" class="muted" hidden></div>
channels/static/app.js:19:    resend: "Erneut senden",
channels/static/app.js:24:    extrasNote: "Extras sind nicht separat bepreist.",
channels/static/app.js:46:    resend: "Resend",
channels/static/app.js:51:    extrasNote: "Extras are not separately priced.",
channels/static/app.js:96:function notice(text, resendText) {
channels/static/app.js:100:  if (resendText !== undefined) {
channels/static/app.js:102:    btn.textContent = t("resend");
channels/static/app.js:103:    btn.onclick = () => { div.remove(); sendTurn(resendText); };
channels/static/app.js:124:      (item.extras.length ? ` (+${item.extras.join(", ")})` : "");
channels/static/app.js:125:    if (item.extras.length) hasExtras = true;
channels/static/app.js:131:  $("basket-extras-note").hidden = !hasExtras;
channels/static/app.js:132:  $("basket-extras-note").textContent = t("extrasNote");
channels/static/app.js:182:async function readStream(response, resendText) {
channels/static/app.js:226:  if (!assistantAnswered) notice(t("notAnswered"), resendText);
channels/static/app.js:232:async function streamPost(path, body, resendText) {
channels/static/app.js:234:  // Real client-side timeout: covers the request AND the streamed body,
channels/static/app.js:235:  // so the timeout notice + resend control can actually occur.
channels/static/app.js:236:  const signal = AbortSignal.any(
channels/static/app.js:237:    [currentAbort.signal, AbortSignal.timeout(STREAM_TIMEOUT_MS)]);
channels/static/app.js:253:      // keep the customer's message recoverable via resend.
channels/static/app.js:255:      await startSession(session.pizzeriaId);
channels/static/app.js:256:      notice(t("sessionLost"), resendText);
channels/static/app.js:263:    finalText = await readStream(res, resendText);
channels/static/app.js:267:    else if (err.name === "TimeoutError") notice(t("errTimeout"), resendText);
channels/static/app.js:268:    else if (err.message === "http") notice(t("errHttp"), resendText);
channels/static/app.js:269:    else notice(t("errNetwork"), resendText);
channels/static/app.js:276:async function sendTurn(text, spoken = false) {
channels/static/app.js:278:  const finalText = await streamPost(
channels/static/app.js:279:    "/chat", { session_id: session.id, text, spoken }, text ?? undefined);
channels/static/app.js:284:  const finalText = await streamPost(
channels/static/app.js:285:    "/confirm", { session_id: session.id, revision });
channels/static/app.js:321:async function startSession(pizzeriaId) {
channels/static/app.js:429:  startSession(e.target.value);
channels/static/app.js:433:  if (session) startSession(session.pizzeriaId);
channels/static/app.js:456:    await startSession(cfg.preselected_id);
channels/web.py:4:Contract (PLAN v2): /config, /session, /chat, /confirm, /language,
channels/web.py:167:@app.post("/chat")
channels/web.py:173:    spoken = bool(body.get("spoken"))
channels/web.py:176:        lambda emit: app.state.agent.run_turn(session, text, emit,
channels/web.py:177:                                              spoken=spoken),
channels/web.py:181:@app.post("/confirm")
tests/transcripts/correction.json:7:       {"tool": "add_items", "args": {"items": [{"type": "pizza", "code": "margherita", "qty": 1, "extras": []}]}},
tests/transcripts/correction.json:12:       {"tool": "add_items", "args": {"items": [{"type": "pizza", "code": "margherita", "qty": 2, "extras": []}]}},
tests/test_state.py:10:def item(code="margherita", type_="pizza", qty=1, extras=None):
tests/test_state.py:12:                extras=extras or [])
tests/test_state.py:206:def test_same_code_different_extras_is_separate_line():
tests/test_state.py:209:    state.add_items(o, [item(qty=1, extras=["mushrooms"])])
tests/test_state.py:240:    """Same (type, code), different extras: no-qty removal takes them all."""
tests/test_state.py:242:    state.add_items(o, [item(qty=1), item(qty=1, extras=["mushrooms"])])
tests/test_state.py:249:    state.add_items(o, [item(qty=2), item(qty=2, extras=["mushrooms"])])
tests/test_state.py:251:    assert [(i.extras, i.qty) for i in o.items] == \
tests/stubs.py:100:        @app.post("/chat/completions")
tests/transcripts/unknown_item.json:7:       {"tool": "add_items", "args": {"items": [{"type": "pasta", "code": "bolognese", "qty": 1, "extras": []}]}},
tests/transcripts/unknown_item.json:12:       {"tool": "add_items", "args": {"items": [{"type": "pasta", "code": "funghi", "qty": 1, "extras": []}]}},
tests/test_transcripts.py:43:    """Fake PizzaSim: 'ok' submits succeed; 'timeout_then_recover' times
tests/test_transcripts.py:54:        if self.mode == "timeout_then_recover" and self.submits == 1:
tests/test_transcripts.py:57:            raise ApiTimeout("simulated submit timeout")
tests/test_transcripts.py:61:        if self.mode == "timeout_then_recover":
tests/test_transcripts.py:101:        final = agent.run_turn(session, turn["user"], emit)
tests/test_transcripts.py:121:def test_gateway_timeout_apology():
tests/test_transcripts.py:122:    """Gateway timeout: one retry, then abort the turn with an apology."""
tests/test_transcripts.py:137:    text = agent.run_turn(session, "hello")
channels/speech.py:33:                          timeout=3.0).raise_for_status()
channels/speech.py:46:                timeout=60.0)
channels/speech.py:58:                timeout=60.0)
tests/test_tools.py:64:def test_extras_controlled_vocabulary(menu):
tests/test_tools.py:65:    menu.validate_extras(["mushrooms", "pineapple"])  # ok
tests/test_tools.py:67:        menu.validate_extras(["unicorn_dust"])
tests/test_tools.py:68:    assert e.value.code == "invalid_extra"
tests/test_tools.py:107:def test_timeout_mapped():
tests/test_tools.py:269:def test_invalid_extra_via_dispatch(menu, fake):
tests/test_tools.py:273:                                        "extras": ["unicorn_dust"]}]})
tests/test_tools.py:274:    assert result["error"]["code"] == "invalid_extra"
tests/test_tools.py:312:def test_submit_timeout_then_recovery_via_list(menu, fake):
tests/test_tools.py:328:                   "extras": []}],
tests/test_tools.py:349:                   "extras": []}],
tests/test_tools.py:357:def test_mutation_after_submit_timeout_clears_recovery_state(menu, fake):
tests/test_tools.py:385:def test_submit_timeout_verified_absent_allows_one_retry(menu, fake):
tests/test_tools.py:537:    text = Agent(config_stub(), chat_fn=dead).run_turn(session, "hi")
tests/test_tools.py:541:def test_spoken_note_is_ephemeral_per_turn():
tests/test_tools.py:542:    """The spoken-style note reaches the model for the spoken turn only —
tests/test_tools.py:552:    agent.run_turn(session, "hallo", spoken=True)
tests/test_tools.py:555:    agent.run_turn(session, "hallo")
tests/test_tools.py:612:    """Answer-or-rendered-error invariant on /confirm: dispatches applied,
tests/test_tools.py:631:    text = agent.run_turn(session, "hi")  # closed port → down + apology
tests/transcripts/happy_path.json:12:       {"tool": "add_items", "args": {"items": [{"type": "pizza", "code": "margherita", "qty": 2, "extras": []}]}},
core/menu.py:1:"""Immutable menu snapshot: (type, code) validation, extras validation,
core/menu.py:69:    def validate_extras(self, extras: list[str]) -> None:
core/menu.py:70:        for extra in extras:
core/menu.py:71:            if extra not in self.toppings:
core/menu.py:75:                        extra.lower(), self.toppings, n=3, cutoff=0.5
core/menu.py:79:                    "invalid_extra",
core/tools.py:28:        "extras": {"type": "array", "items": {"type": "string"}},
core/tools.py:36:                    "names, and the available extra toppings.",
core/tools.py:40:                    "get_menu. Rejects the whole call if any item or extra "
core/tools.py:138:            extras = raw.get("extras") or []
core/tools.py:139:            menu.validate_extras(extras)
core/tools.py:146:                extras=extras,
core/tools.py:201:            (e["type"], e["code"], e["qty"], tuple(sorted(e["extras"])))
core/tools.py:205:             "extras": list(i.extras)} for i in basket]
core/tools.py:247:              "extras": list(i.extras)} for i in order.items]
core/state.py:59:    basket holding the same (type, code) with different extras needs
core/pizzasim.py:1:"""PizzaSim API client: httpx, explicit timeouts, typed errors.
core/pizzasim.py:97:            timeout=_TIMEOUT,
core/order.py:27:    extras: list[str] = field(default_factory=list)
core/order.py:33:        return (self.type, self.code, tuple(sorted(self.extras)))
core/order.py:70:                    "extras": list(i.extras),
core/agent.py:38:    "en": "This reply will be spoken aloud: name at most three dishes, "
core/agent.py:150:        # call from any session (/chat and /confirm share this path).
core/agent.py:162:        for attempt in range(2):  # one retry on timeout, then abort turn
core/agent.py:165:                    f"{self.config.url}/chat/completions",
core/agent.py:166:                    json=payload, headers=headers, timeout=GATEWAY_TIMEOUT,
core/agent.py:182:    def run_turn(self, session: Session, user_text: str | None,
core/agent.py:183:                 emit=lambda event: None, spoken: bool = False) -> str:
core/agent.py:195:        # Ephemeral per-turn note: activates the spoken-style policy that
core/agent.py:197:        # not inherit the spoken constraints.
core/agent.py:198:        extra = ([{"role": "system", "content": SPOKEN_NOTE[session.lang]}]
core/agent.py:199:                 if spoken else [])
core/agent.py:203:                message = self._chat_fn(session.messages + extra,
core/agent.py:293:        return self.run_turn(session, None, emit)

 succeeded in 714ms:
channels/__init__.py
channels/cli.py
channels/speech.py
channels/static/app.js
channels/static/index.html
channels/static/style.css
channels/web.py
core/__init__.py
core/agent.py
core/menu.py
core/order.py
core/pizzasim.py
core/state.py
core/tools.py
decisions/qa.md
tests/__init__.py
tests/fixtures/error_422.json
tests/fixtures/location.json
tests/fixtures/menu.json
tests/fixtures/order_created.json
tests/fixtures/orders_list.json
tests/fixtures/pizzerias.json
tests/stubs.py
tests/test_state.py
tests/test_tools.py
tests/test_transcripts.py
tests/test_web_e2e.py
tests/transcripts/correction.json
tests/transcripts/happy_path.json
tests/transcripts/mind_change.json
tests/transcripts/submit_timeout.json
tests/transcripts/unknown_item.json

Reviewing the repository implementation against SPEC/PLAN and verifying the four round-1 fixes in code and tests before scoring.
  ✓ Read the binding spec/plan/oracle documents and prior review requirements
  → Inspect the implementation paths for the four claimed fixes and their tests
  • Inspect remaining v2 obligations in core/web/UI/tests for spec or plan breaches
  • Produce findings-first review with rubric scores and verdict
codex
The initial scan shows the claimed round-1 fixes are present in the expected files and tests. I’m reading those implementations now to check that the behavior actually matches the spec rather than only matching the changelog description.
exec
/bin/bash -lc "sed -n '1,360p' core/agent.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '260,380p' tests/test_web_e2e.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,320p' channels/web.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '520,700p' tests/test_tools.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' decisions/qa.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,520p' channels/static/app.js" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 476ms:
"""Model loop: prompt assembly, chat-completions calls, tool dispatch,
JSONL event logging. The model only speaks; the order lives in core.

v2: everything tenant-, language- and menu-scoped lives in the per-session
Session; the session factory owns tenant validation and construction. The
transport passes identifiers only.
"""
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
from .pizzasim import NotFoundError, PizzaSim, optional_env, require_env

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

SPOKEN_NOTE = {
    "de": "Diese Antwort wird vorgelesen: höchstens drei Gerichte nennen, "
          "Zeiten in Minuten, Bestellnummern in Gruppen, kurze Sätze.",
    "en": "This reply will be spoken aloud: name at most three dishes, "
          "times in minutes, order ids in groups, short sentences.",
}


class GatewayError(Exception):
    pass


@dataclass
class AgentConfig:
    url: str
    key: str
    model: str
    lang: str  # PIZZERIA_LANG: the initial/default session language

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
    tenant-bound client, one language, one history. The tenant fields are
    set at creation and never mutated — switching pizzeria is a new
    Session (SPEC invariant 6)."""
    order: Order
    menu: Menu
    messages: list[dict]
    client: PizzaSim | None = None
    pizzeria_id: str = ""
    pizzeria_name: str = ""
    lang: str = "de"
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])


def create_session(config: AgentConfig, base: PizzaSim,
                   pizzeria_id: str | None = None,
                   lang: str | None = None) -> Session:
    """Core-owned session factory. Validates the tenant against the live
    pizzeria list, builds the tenant-bound client, fetches the session's
    immutable menu snapshot, renders the prompt. Raises NotFoundError for
    an unknown/vanished pizzeria (session error — the process stays up)."""
    pizzeria_id = pizzeria_id or base.pizzeria_id
    lang = (lang or config.lang).lower()
    if lang not in ("de", "en"):
        lang = config.lang
    names = {p["id"]: p["name"] for p in base.list_pizzerias()}
    if pizzeria_id not in names:
        raise NotFoundError(
            f"pizzeria {pizzeria_id} not found on the PizzaSim server"
        )
    client = base.for_pizzeria(pizzeria_id)
    menu = Menu(client.get_menu())
    return Session(
        order=Order(),
        menu=menu,
        messages=[{"role": "system",
                   "content": system_prompt(lang, names[pizzeria_id])}],
        client=client,
        pizzeria_id=pizzeria_id,
        pizzeria_name=names[pizzeria_id],
        lang=lang,
    )


def set_language(session: Session, lang: str) -> None:
    """The customer's language declaration (web header switch). Re-renders
    the system prompt in place — same policy text, history preserved."""
    lang = lang.lower()
    if lang not in ("de", "en") or lang == session.lang:
        return
    session.lang = lang
    session.messages[0] = {
        "role": "system",
        "content": system_prompt(lang, session.pizzeria_name),
    }
    log_event(session, {"type": "language", "lang": lang})


def log_event(session: Session, event: dict) -> None:
    """One line per event, JSON, to a file. Never carries config values."""
    LOG_DIR.mkdir(exist_ok=True)
    record = {"ts": round(time.time(), 3), "session": session.id, **event}
    with (LOG_DIR / f"agent-{session.id}.jsonl").open("a") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")


class Agent:
    def __init__(self, config: AgentConfig, chat_fn=None, status_cb=None):
        self.config = config
        # chat_fn(messages, tools) -> assistant message dict; injectable so
        # the golden transcripts and E2E stubs run without the gateway.
        self._chat_fn = chat_fn or self._gateway_chat
        # status_cb("ok"|"down"): process-wide gateway health, fed by every
        # call from any session (/chat and /confirm share this path).
        self._status_cb = status_cb or (lambda status: None)

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
                message = response.json()["choices"][0]["message"]
                self._status_cb("ok")
                return message
            except httpx.TimeoutException as exc:
                last_exc = exc
                continue
            except (httpx.HTTPError, KeyError, ValueError) as exc:
                self._status_cb("down")
                raise GatewayError(f"gateway request failed: "
                                   f"{type(exc).__name__}") from exc
        self._status_cb("down")
        raise GatewayError("gateway timed out twice") from last_exc

    def run_turn(self, session: Session, user_text: str | None,
                 emit=lambda event: None, spoken: bool = False) -> str:
        """One customer turn: returns the assistant's final text. Every
        intermediate step goes to emit() and the JSONL log. user_text None
        is the opening/continuation turn — the agent speaks unprompted."""

        def event(payload: dict) -> None:
            log_event(session, payload)
            emit(payload)

        if user_text is not None:
            session.messages.append({"role": "user", "content": user_text})
            event({"type": "user", "text": user_text})
        # Ephemeral per-turn note: activates the spoken-style policy that
        # lives in the prompt. Never persisted — a later typed turn must
        # not inherit the spoken constraints.
        extra = ([{"role": "system", "content": SPOKEN_NOTE[session.lang]}]
                 if spoken else [])

        for _ in range(MAX_TOOL_ROUNDS):
            try:
                message = self._chat_fn(session.messages + extra,
                                        tools.openai_tools())
            except GatewayError as exc:
                event({"type": "error", "error": str(exc)})
                apology = APOLOGY[session.lang]
                session.messages.append({"role": "assistant",
                                         "content": apology})
                event({"type": "assistant", "text": apology})
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
                                        session.client, name, args)
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
        apology = APOLOGY[session.lang]
        session.messages.append({"role": "assistant", "content": apology})
        event({"type": "assistant", "text": apology})
        return apology

    def _synthetic_call(self, session: Session, name: str, args: dict,
                        event) -> dict:
        """One UI-initiated dispatch, recorded exactly like a model call:
        synthetic assistant tool_calls message + tool result + events."""
        call_id = f"ui-{name}-{session.order.revision}"
        event({"type": "tool_call", "tool": name, "args": args})
        session.messages.append({
            "role": "assistant",
            "content": None,
            "tool_calls": [{"id": call_id, "type": "function",
                            "function": {"name": name,
                                         "arguments": json.dumps(args)}}],
        })
        result = tools.dispatch(session.order, session.menu,
                                session.client, name, args)
        event({"type": "tool_result", "tool": name, "result": result})
        event({"type": "state", "state": session.order.state.value,
               "revision": session.order.revision})
        session.messages.append({
            "role": "tool",
            "tool_call_id": call_id,
            "content": json.dumps(result, ensure_ascii=False),
        })
        return result

    def confirm_and_submit(self, session: Session, revision: int,
                           emit=lambda event: None) -> str:
        """The explicit confirm control (SPEC: confirmation is an action
        the customer takes). One core path, symmetric for success and
        failure; CONFIRMED stays reachable only via confirm_order."""

        def event(payload: dict) -> None:
            log_event(session, payload)
            emit(payload)

        result = self._synthetic_call(
            session, "confirm_order", {"revision": revision}, event)
        if "error" not in result:
            self._synthetic_call(session, "submit_order", {}, event)
        # The phrasing call is a normal turn: same gateway path, same
        # retry-once, same apology-as-assistant-event on failure.
        return self.run_turn(session, None, emit)


def startup(config: AgentConfig) -> tuple[PizzaSim, str, Menu]:
    """The one startup sequence: env → preselected-pizzeria check → menu
    health check. Raises before the first turn on any failure. The
    preselection is only the default tenant for new sessions."""
    client = PizzaSim.from_env()
    pizzeria_name = client.pizzeria_name()
    menu = Menu(client.get_menu())
    return client, pizzeria_name, menu

 succeeded in 469ms:
def test_e2e_pizzeria_switch_and_language(page_factory, stack):
    stack["gateway"].mode = "ok"
    page = open_app(page_factory, stack)
    page.fill("#text", "Zwei Margherita bitte")
    page.click("#send")
    page.wait_for_selector("#basket-lines li", timeout=30000)

    page.select_option("#pizzeria-select", PZ2)
    page.wait_for_function(
        "document.getElementById('pizzeria-name').textContent === "
        "'Stub Pizzeria Due'", timeout=30000)
    assert page.locator("#uuid").inner_text() == PZ2
    assert page.locator("#basket-lines li").count() == 0  # basket cleared
    page.wait_for_selector(".msg.assistant", timeout=30000)  # fresh greet

    page.locator("#lang-switch button[data-lang=en]").click()
    page.wait_for_function(
        "document.getElementById('start-over').textContent === "
        "'Start over'", timeout=15000)  # chrome follows the declared lang
    page.close()


def test_e2e_vanished_pizzeria_refreshes_selector(page_factory, stack):
    stack["gateway"].mode = "ok"
    page = open_app(page_factory, stack)
    page.fill("#text", "Zwei Margherita bitte")
    page.click("#send")
    page.wait_for_selector("#basket-lines li", timeout=30000)
    stack["pizzasim"].pizzerias = [p for p in stack["pizzasim"].pizzerias
                                   if p["id"] != PZ2]
    try:
        page.select_option("#pizzeria-select", PZ2)
        page.wait_for_selector(".notice", timeout=30000)
        page.wait_for_function(
            "document.querySelectorAll('#pizzeria-select option')"
            ".length === 1", timeout=15000)
        # the failed switch must NOT hide the still-live order
        assert page.locator("#basket-lines li").count() == 1
        assert page.locator(".msg.user").count() == 1
    finally:
        stack["pizzasim"].pizzerias.append(PZ2_ENTRY)
    page.close()


def test_e2e_lost_session_recreates_and_offers_resend(page_factory,
                                                      stack):
    """Server no longer knows the session (e.g. restart): the customer
    sees a plain notice, gets a fresh session, and can resend."""
    stack["gateway"].mode = "ok"
    page = open_app(page_factory, stack)
    stack["web"].app.state.sessions.clear()  # simulate a lost session
    page.fill("#text", "Was kostet eine Margherita?")
    page.click("#send")
    page.wait_for_selector(".notice button", timeout=30000)  # resend
    page.locator(".notice button").last.click()
    page.wait_for_selector("text=8.5 €", timeout=30000)
    page.close()


def test_e2e_tool_error_leaves_visible_message(page_factory, stack):
    stack["gateway"].mode = "ok"
    page = open_app(page_factory, stack)
    page.fill("#text", "Einmal Bolognese bitte")
    page.click("#send")
    page.wait_for_selector("text=nicht im Angebot", timeout=30000)
    page.close()


def test_e2e_gateway_unreachable_leaves_visible_message(page_factory,
                                                        stack):
    stack["gateway"].mode = "ok"
    page = open_app(page_factory, stack)
    stack["gateway"].mode = "http500"
    try:
        page.fill("#text", "Hallo?")
        page.click("#send")
        # the retry-once path ends in a rendered apology — an answer
        page.wait_for_selector("text=schiefgegangen", timeout=30000)
    finally:
        stack["gateway"].mode = "ok"
    page.close()


def test_e2e_stream_without_answer_offers_resend(page_factory, stack):
    stack["gateway"].mode = "ok"
    page = open_app(page_factory, stack)
    stack["gateway"].mode = "empty"
    try:
        page.fill("#text", "Hallo?")
        page.click("#send")
        page.wait_for_selector(".notice button", timeout=30000)
    finally:
        stack["gateway"].mode = "ok"
    page.locator(".notice button").last.click()  # resend, now answered
    page.wait_for_function(
        "document.querySelectorAll('.msg.assistant').length >= 2",
        timeout=30000)
    page.close()

 succeeded in 446ms:
/* Web UI over the NDJSON stream. The invariant this file serves: no sent
   message ends without a rendered assistant reply or a rendered error.
   Speech: browser captures/plays audio only (MediaRecorder + <audio>);
   recognition/synthesis happen server-side. No browser speech APIs. */
"use strict";

const $ = (id) => document.getElementById(id);
const chat = $("chat");

const I18N = {
  de: {
    working: "Der Agent arbeitet …",
    steps: "Zwischenschritte",
    notAnswered: "Der Agent hat nicht geantwortet.",
    errNetwork: "Verbindung fehlgeschlagen.",
    errTimeout: "Zeitüberschreitung.",
    errHttp: "Es gab einen technischen Fehler.",
    busy: "Es läuft gerade eine Antwort — einen Moment.",
    resend: "Erneut senden",
    listUnavailable: "Pizzeria-Liste nicht verfügbar",
    startOver: "Neu beginnen",
    basket: "Warenkorb",
    total: "Summe",
    extrasNote: "Extras sind nicht separat bepreist.",
    submitted: "Bestellung abgeschickt — Nummer:",
    confirm: "Bestellung bestätigen",
    placeholder: "Nachricht schreiben …",
    send: "Senden",
    ttsLabel: "Antworten vorlesen",
    sttFail: "Spracherkennung gerade nicht erreichbar — bitte tippen.",
    sttEmpty: "Ich habe nichts verstanden — bitte noch einmal.",
    ttsFail: "Vorlesen gerade nicht möglich.",
    micDenied: "Kein Mikrofonzugriff.",
    sessionGone: "Diese Pizzeria ist gerade nicht verfügbar.",
    sessionLost: "Die Sitzung ist verloren gegangen — neue Sitzung " +
      "gestartet.",
  },
  en: {
    working: "The agent is working …",
    steps: "Intermediate steps",
    notAnswered: "The agent did not answer.",
    errNetwork: "Connection failed.",
    errTimeout: "The request timed out.",
    errHttp: "A technical error occurred.",
    busy: "A reply is already in progress — one moment.",
    resend: "Resend",
    listUnavailable: "Pizzeria list unavailable",
    startOver: "Start over",
    basket: "Basket",
    total: "Total",
    extrasNote: "Extras are not separately priced.",
    submitted: "Order submitted — number:",
    confirm: "Confirm order",
    placeholder: "Type a message …",
    send: "Send",
    ttsLabel: "Read replies aloud",
    sttFail: "Speech recognition unavailable — please type.",
    sttEmpty: "I didn't catch that — please try again.",
    ttsFail: "Read-aloud is unavailable right now.",
    micDenied: "No microphone access.",
    sessionGone: "That pizzeria isn't available right now.",
    sessionLost: "The session was lost — a new one was started.",
  },
};

let cfg = null;
let session = null;          // {id, pizzeriaId, pizzeriaName}
let lang = "de";
let currentAbort = null;
let lastOrderId = null;
const t = (key) => I18N[lang][key];

/* ---------- chrome ------------------------------------------------------ */

function applyChrome() {
  document.documentElement.lang = lang;
  $("text").placeholder = t("placeholder");
  $("send").textContent = t("send");
  $("start-over").textContent = t("startOver");
  $("basket-title").textContent = t("basket");
  $("tts-label").textContent = t("ttsLabel");
  $("list-unavailable").textContent = t("listUnavailable");
  document.querySelectorAll("#lang-switch button").forEach((b) =>
    b.classList.toggle("active", b.dataset.lang === lang));
}

function addMsg(cls, text) {
  const div = document.createElement("div");
  div.className = "msg " + cls;
  div.textContent = text;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
  return div;
}

function notice(text, resendText) {
  const div = document.createElement("div");
  div.className = "notice";
  div.appendChild(document.createTextNode(text));
  if (resendText !== undefined) {
    const btn = document.createElement("button");
    btn.textContent = t("resend");
    btn.onclick = () => { div.remove(); sendTurn(resendText); };
    div.appendChild(btn);
  }
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

/* ---------- basket ------------------------------------------------------ */

function euro(n) {
  return n.toFixed(2).replace(".", lang === "de" ? "," : ".") + " €";
}

function renderBasket(snapshot) {
  const lines = $("basket-lines");
  lines.textContent = "";
  let hasExtras = false;
  for (const item of snapshot.items) {
    const li = document.createElement("li");
    const label = document.createElement("span");
    label.textContent = `${item.qty}× ${item.name}` +
      (item.extras.length ? ` (+${item.extras.join(", ")})` : "");
    if (item.extras.length) hasExtras = true;
    const price = document.createElement("span");
    price.textContent = euro(item.line_total);
    li.append(label, price);
    lines.appendChild(li);
  }
  $("basket-extras-note").hidden = !hasExtras;
  $("basket-extras-note").textContent = t("extrasNote");
  $("basket-total").textContent = "";
  const totalLabel = document.createElement("span");
  totalLabel.textContent = t("total");
  const totalValue = document.createElement("span");
  totalValue.textContent = euro(snapshot.basket_total);
  $("basket-total").append(totalLabel, totalValue);

  const submitted = snapshot.state === "SUBMITTED";
  $("basket").classList.toggle("locked", submitted);
  $("submitted-banner").hidden = !submitted;
  if (submitted) {
    $("submitted-banner").textContent =
      `${t("submitted")} ${lastOrderId || "—"}`;
    disableConfirm();
  }
}

/* ---------- read-back + confirm ---------------------------------------- */

function disableConfirm() {
  document.querySelectorAll(".readback button").forEach((b) => {
    b.disabled = true;
  });
}

function showReadback(snapshot) {
  disableConfirm();
  const panel = document.createElement("div");
  panel.className = "readback";
  const list = snapshot.items
    .map((i) => `${i.qty}× ${i.name} — ${euro(i.line_total)}`)
    .join("\n");
  const who = snapshot.customer
    ? `${snapshot.customer.first_name}` +
      (snapshot.customer.street_one
        ? `, ${snapshot.customer.street_one}` : "")
    : "";
  panel.textContent =
    `${who}\n${list}\n${t("total")}: ${euro(snapshot.basket_total)}`;
  const btn = document.createElement("button");
  btn.textContent = t("confirm");
  btn.onclick = () => { btn.disabled = true; confirmOrder(snapshot.revision); };
  panel.appendChild(btn);
  chat.appendChild(panel);
  chat.scrollTop = chat.scrollHeight;
}

/* ---------- streaming --------------------------------------------------- */

async function readStream(response, resendText) {
  const steps = document.createElement("details");
  steps.className = "steps";
  steps.innerHTML = `<summary>${t("steps")}</summary>`;
  chat.appendChild(steps);

  let assistantAnswered = false;
  let finalText = "";
  const reader = response.body.getReader();
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
          + (ev.tool || "") + " " + JSON.stringify(ev.args ?? ev.result);
        steps.appendChild(pre);
        if (ev.type === "tool_result" && !ev.result.error) {
          if (ev.result.order_id) lastOrderId = ev.result.order_id;
          if (ev.result.snapshot) {
            renderBasket(ev.result.snapshot);
            if (ev.tool === "read_back") showReadback(ev.result.snapshot);
          }
        }
      } else if (ev.type === "assistant") {
        if (ev.text && ev.text.trim()) {
          assistantAnswered = true;
          finalText = ev.text;
          addMsg("assistant", ev.text);
        }
      } else if (ev.type === "done") {
        renderBasket(ev.state);
      }
    }
  }
  if (!steps.querySelector("pre")) steps.remove();
  if (!assistantAnswered) notice(t("notAnswered"), resendText);
  return finalText;
}

const STREAM_TIMEOUT_MS = 120000;

async function streamPost(path, body, resendText) {
  currentAbort = new AbortController();
  // Real client-side timeout: covers the request AND the streamed body,
  // so the timeout notice + resend control can actually occur.
  const signal = AbortSignal.any(
    [currentAbort.signal, AbortSignal.timeout(STREAM_TIMEOUT_MS)]);
  const working = document.createElement("div");
  working.className = "working";
  working.textContent = t("working");
  chat.appendChild(working);
  $("send").disabled = true;
  let finalText = "";
  try {
    const res = await fetch(path, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
      signal,
    });
    if (res.status === 404) {
      // The server no longer knows this session: recreate transparently,
      // keep the customer's message recoverable via resend.
      working.remove();
      await startSession(session.pizzeriaId);
      notice(t("sessionLost"), resendText);
      $("send").disabled = false;
      return "";
    }
    if (res.status === 409) { working.remove(); notice(t("busy")); return ""; }
    if (!res.ok) throw new Error("http");
    working.remove();
    finalText = await readStream(res, resendText);
  } catch (err) {
    working.remove();
    if (err.name === "AbortError") { /* deliberate: switch/start-over */ }
    else if (err.name === "TimeoutError") notice(t("errTimeout"), resendText);
    else if (err.message === "http") notice(t("errHttp"), resendText);
    else notice(t("errNetwork"), resendText);
  }
  $("send").disabled = false;
  $("text").focus();
  return finalText;
}

async function sendTurn(text, spoken = false) {
  if (text !== null) addMsg("user", text);
  const finalText = await streamPost(
    "/chat", { session_id: session.id, text, spoken }, text ?? undefined);
  if (finalText && cfg.speech && $("tts-toggle").checked) speak(finalText);
}

async function confirmOrder(revision) {
  const finalText = await streamPost(
    "/confirm", { session_id: session.id, revision });
  if (finalText && cfg.speech && $("tts-toggle").checked) speak(finalText);
}

/* ---------- sessions / tenancy ----------------------------------------- */

function fillSelector() {
  const select = $("pizzeria-select");
  if (!cfg.pizzerias) {
    select.hidden = true;
    $("list-unavailable").hidden = false;
    return;
  }
  select.hidden = false;
  $("list-unavailable").hidden = true;
  select.textContent = "";
  for (const p of cfg.pizzerias) {
    const opt = document.createElement("option");
    opt.value = p.id;
    opt.textContent = `${p.name} (${p.id.slice(0, 8)})`;
    select.appendChild(opt);
  }
  if (session) select.value = session.pizzeriaId;
}

async function refreshConfig() {
  cfg = await (await fetch("/config")).json();
  $("version").textContent = "v" + cfg.version;
  $("docs-link").href = cfg.docs_url;
  fillSelector();
  const speechUsable = cfg.speech;
  $("tts-wrap").hidden = !speechUsable;
  $("mic").hidden = !(speechUsable && navigator.mediaDevices &&
                      window.MediaRecorder);
}

async function startSession(pizzeriaId) {
  // Create the new session FIRST: a failed switch must not hide the
  // still-live conversation and basket the customer can see.
  const res = await fetch("/session", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ pizzeria_id: pizzeriaId, lang }),
  });
  if (!res.ok) {
    notice(t("sessionGone"));
    await refreshConfig();  // fresh selector from the live list
    if (session) $("pizzeria-select").value = session.pizzeriaId;
    return;
  }
  if (currentAbort) currentAbort.abort();
  chat.textContent = "";
  lastOrderId = null;
  renderBasket({ items: [], basket_total: 0, state: "EMPTY",
                 customer: null });
  const data = await res.json();
  session = { id: data.session_id, pizzeriaId: data.pizzeria_id,
              pizzeriaName: data.pizzeria_name };
  $("pizzeria-name").textContent = data.pizzeria_name;
  document.title = data.pizzeria_name;
  $("dashboard-link").hidden = false;
  $("dashboard-link").href = `${cfg.dashboard_base}/${data.pizzeria_id}`;
  $("uuid").textContent = data.pizzeria_id;
  $("pizzeria-select").value = data.pizzeria_id;
  await sendTurn(null);  // the agent greets first
}

/* ---------- speech (capture/playback only) ------------------------------ */

let recorder = null;

async function startRecording() {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  recorder = new MediaRecorder(stream);
  const chunks = [];
  recorder.ondataavailable = (e) => chunks.push(e.data);
  recorder.onstop = async () => {
    stream.getTracks().forEach((tr) => tr.stop());
    $("mic").classList.remove("recording");
    $("mic").setAttribute("aria-pressed", "false");
    const blob = new Blob(chunks, { type: recorder.mimeType });
    const body = new FormData();
    body.append("audio", blob, "speech.webm");
    try {
      const res = await fetch(
        `/speech/stt?session_id=${session.id}`, { method: "POST", body });
      if (!res.ok) throw new Error();
      const { text } = await res.json();
      if (text.trim()) sendTurn(text.trim(), true);
      else notice(t("sttEmpty"));
    } catch {
      notice(t("sttFail"));
    }
  };
  recorder.start();
  $("mic").classList.add("recording");
  $("mic").setAttribute("aria-pressed", "true");
}

$("mic").addEventListener("click", () => {
  if (recorder && recorder.state === "recording") recorder.stop();
  else startRecording().catch(() => notice(t("micDenied")));
});

async function speak(text) {
  try {
    const res = await fetch("/speech/tts", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: session.id, text }),
    });
    if (!res.ok) throw new Error();
    new Audio(URL.createObjectURL(await res.blob())).play();
  } catch {
    notice(t("ttsFail"));
  }
}

/* ---------- health ------------------------------------------------------ */

async function pollHealth() {
  try {
    const h = await (await fetch("/health")).json();
    for (const [id, state] of [["health-api", h.api],
                               ["health-gateway", h.gateway]]) {
      const el = $(id);
      el.classList.remove("ok", "down", "unknown");
      el.classList.add(state);
      el.title = state;
    }
  } catch { /* footer badge keeps its last state */ }
}

/* ---------- wiring ------------------------------------------------------ */

$("composer").addEventListener("submit", (e) => {
  e.preventDefault();
  const text = $("text").value.trim();
  if (!text || !session) return;
  $("text").value = "";
  sendTurn(text);
});

$("pizzeria-select").addEventListener("change", (e) => {
  startSession(e.target.value);
});

$("start-over").addEventListener("click", () => {
  if (session) startSession(session.pizzeriaId);
});

document.querySelectorAll("#lang-switch button").forEach((btn) => {
  btn.addEventListener("click", async () => {
    if (btn.dataset.lang === lang) return;
    lang = btn.dataset.lang;
    applyChrome();
    if (session) {
      await fetch("/language", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: session.id, lang }),
      }).catch(() => {});
    }
  });
});

(async () => {
  try {
    await refreshConfig();
    lang = cfg.lang_default || "de";
    applyChrome();
    await startSession(cfg.preselected_id);
    pollHealth();
    setInterval(pollHealth, 30000);
  } catch {
    notice(I18N[lang].errNetwork);
  }
})();

 succeeded in 471ms:
# Oracle Q&A (Codex, read-only)

## 2026-07-31 — Greeting language source

**Q:** SPEC requires greeting in the pizzeria-country language; the live API
exposes no country field; DE/EN only; nothing hardcoded, config from env.
Which mechanism: (a) optional env `PIZZERIA_LANG` default de, (b) required
env var failing at startup, (c) constant in source, (d) other?

**A (decision):** **(b)** — `PIZZERIA_LANG` (de|en) is a required env var.
A default would smuggle in a hardcoded fallback, conflicting with "nothing
is hardcoded" and the missing-var-fails-startup rule. If missing/empty, exit
before the first turn naming `PIZZERIA_LANG` and where it was expected; no
default applied.

## 2026-08-01 — SPEC v2: Nachbessern oder Neustart?

**Q:** Operator replaced SPEC.md (v2: prices+totals, customer-selectable
multi-pizzeria, APP_VERSION, full "The web channel" contract, mandatory
browser E2E). Retrofit the approved v1 codebase or restart from scratch?

**Process:** Codex audit of the v1 claims (PASS — review trail, artifacts,
test count verified in-repo; reviews/round9-audit-grill.md), then a 6-question
grill of the retrofit position and answers (reviews/round10-grill-verdict.md).

**A (decision): RETROFIT**, under 5 binding conditions:
1. `PIZZERIA_LANG` must be documented in SPEC.md's env table — no hidden
   required var.
2. Core-owned session factory; immutable per-session
   {pizzeria_id, pizzeria_name, client, menu, lang, order, messages};
   no app-wide tenant-bound client/agent.
3. Confirm path exactly: UI control → POST /confirm {session_id, revision}
   → one core method dispatching confirm_order(revision) then submit_order,
   synthetic tool messages appended, stale revisions rejected.
4. Web channel treated as substantial rewrite (done-event, unanswered/
   resend paths, header/footer contract, basket+total, connection states,
   start over, switch-race abandonment via fresh session ids).
5. Prices/totals canonical in core only, copied at add time, unit-tested +
   Playwright E2E incl. tenant switch and the three failure paths.

 succeeded in 546ms:
"""FastAPI web channel on port 8888. Same core, zero order logic here —
routes forward identifiers to core and stream its events.

Contract (PLAN v2): /config, /session, /chat, /confirm, /language,
/health, speech proxies, static UI. Turns are serialized per session;
tenants are immutable per session; the pizzeria selector list comes from
the live API and from nowhere else.

Run:  python -m channels.web
"""
from __future__ import annotations

import json
import queue
import re
import sys
import threading

from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse, Response, StreamingResponse
from fastapi.staticfiles import StaticFiles

from channels.speech import SpeechService, SpeechUnavailable
from core.agent import (
    Agent,
    AgentConfig,
    Session,
    create_session,
    set_language,
    startup,
)
from core.pizzasim import (
    ConfigError,
    NotFoundError,
    PizzaSimError,
    require_env,
)

STATIC = Path(__file__).resolve().parent / "static"
app = FastAPI(title="PizzaSim ordering agent")

SESSION_ERROR = {
    "de": "Diese Pizzeria ist gerade nicht verfügbar.",
    "en": "That pizzeria isn't available right now.",
}


@app.on_event("startup")
def boot() -> None:
    try:
        config = AgentConfig.from_env()
        version = require_env("APP_VERSION")
        if not re.fullmatch(r"\d+\.\d+\.\d+", version):
            raise ConfigError("APP_VERSION must look like x.y.z")
        base, _pizzeria_name, _menu = startup(config)
    except (ConfigError, ValueError) as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        raise SystemExit(1)
    except PizzaSimError as exc:
        print(f"Startup check against PizzaSim failed: {exc}\n"
              "We're not taking orders right now.", file=sys.stderr)
        raise SystemExit(1)
    app.state.config = config
    app.state.version = version
    app.state.base = base  # tenant-free surface + preselection default
    app.state.gateway_status = "unknown"  # process-wide, set by any call
    app.state.agent = Agent(
        config,
        status_cb=lambda status: setattr(app.state, "gateway_status",
                                         status),
    )
    app.state.sessions: dict[str, Session] = {}
    app.state.locks: dict[str, threading.Lock] = {}
    app.state.speech = SpeechService()


@app.get("/")
def index():
    return FileResponse(STATIC / "index.html")


@app.get("/config")
def ui_config():
    """UI bootstrap. The pizzeria list comes from the live API on every
    call; on failure it is null and the UI must not offer a selector."""
    try:
        pizzerias = [{"id": p["id"], "name": p["name"]}
                     for p in app.state.base.list_pizzerias()]
    except PizzaSimError:
        pizzerias = None
    return {
        "version": app.state.version,
        "speech": app.state.speech.enabled,
        "lang_default": app.state.config.lang,
        "pizzerias": pizzerias,
        "preselected_id": app.state.base.pizzeria_id,
        "dashboard_base": f"{app.state.base.base_url}/dashboard/pizzerias",
        "docs_url": f"{app.state.base.base_url}/swagger.html",
    }


@app.get("/health")
def health():
    """api: measured live per request. gateway: process-wide last-known
    status from real calls; /health itself never calls the gateway."""
    try:
        app.state.base.list_pizzerias()
        api = "ok"
    except PizzaSimError:
        api = "down"
    return {"api": api, "gateway": app.state.gateway_status}


@app.post("/session")
def new_session(body: dict):
    pizzeria_id = body.get("pizzeria_id") or None
    lang = body.get("lang") or None
    try:
        session = create_session(app.state.config, app.state.base,
                                 pizzeria_id, lang)
    except NotFoundError:
        lang = lang if lang in SESSION_ERROR else app.state.config.lang
        raise HTTPException(409, SESSION_ERROR[lang])
    except PizzaSimError:
        raise HTTPException(503, "We're not taking orders right now.")
    app.state.sessions[session.id] = session
    app.state.locks[session.id] = threading.Lock()
    return {"session_id": session.id, "pizzeria_id": session.pizzeria_id,
            "pizzeria_name": session.pizzeria_name, "lang": session.lang}


def _session(session_id: str) -> Session:
    session = app.state.sessions.get(session_id or "")
    if session is None:
        raise HTTPException(404, "unknown session")
    return session


def _stream(session: Session, work) -> StreamingResponse:
    """Serialize turns per session and stream core events as NDJSON."""
    lock = app.state.locks[session.id]
    if not lock.acquire(blocking=False):
        raise HTTPException(409, "a turn is already in progress")

    events: queue.Queue = queue.Queue()

    def run() -> None:
        try:
            work(events.put)
        finally:
            events.put({"type": "done", "state": session.order.snapshot()})
            events.put(None)
            lock.release()

    threading.Thread(target=run, daemon=True).start()

    def ndjson():
        while (event := events.get()) is not None:
            yield json.dumps(event, ensure_ascii=False) + "\n"

    return StreamingResponse(ndjson(), media_type="application/x-ndjson")


@app.post("/chat")
async def chat(body: dict):
    session = _session(str(body.get("session_id") or ""))
    text = body.get("text")  # None → opening turn, the agent greets
    if text is not None and not str(text).strip():
        raise HTTPException(422, "text must not be empty")
    spoken = bool(body.get("spoken"))
    return _stream(
        session,
        lambda emit: app.state.agent.run_turn(session, text, emit,
                                              spoken=spoken),
    )


@app.post("/confirm")
async def confirm(body: dict):
    """The explicit confirm control: the transport forwards two
    identifiers; core owns the rest."""
    session = _session(str(body.get("session_id") or ""))
    revision = body.get("revision")
    if isinstance(revision, bool) or not isinstance(revision, int):
        raise HTTPException(422, "revision must be an integer")
    return _stream(
        session,
        lambda emit: app.state.agent.confirm_and_submit(session, revision,
                                                        emit),
    )


@app.post("/language")
async def language(body: dict):
    session = _session(str(body.get("session_id") or ""))
    lang = str(body.get("lang") or "")
    if lang not in ("de", "en"):
        raise HTTPException(422, "lang must be de or en")
    set_language(session, lang)
    return {"lang": session.lang}


def _speech() -> SpeechService:
    if not app.state.speech.enabled:
        raise HTTPException(404, "speech is not available")
    return app.state.speech


@app.post("/speech/stt")
async def stt(audio: UploadFile, session_id: str = ""):
    speech = _speech()
    session = _session(session_id)
    try:
        text = speech.stt(await audio.read(),
                          audio.filename or "audio.webm",
                          audio.content_type or "audio/webm",
                          session.lang)
    except SpeechUnavailable:
        raise HTTPException(502, "speech service unavailable")
    return {"text": text}


@app.post("/speech/tts")
async def tts(body: dict):
    speech = _speech()
    session = _session(str(body.get("session_id") or ""))
    text = str(body.get("text") or "")
    if not text:
        raise HTTPException(422, "text required")
    try:
        audio, content_type = speech.tts(text, session.lang)
    except SpeechUnavailable:
        raise HTTPException(502, "speech service unavailable")
    return Response(audio, media_type=content_type)


app.mount("/static", StaticFiles(directory=STATIC), name="static")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8888)

 succeeded in 518ms:

def test_set_language_rerenders_system_prompt_in_place():
    session = create_session(config_stub(), FakeBase())
    history_before = len(session.messages)
    german = session.messages[0]["content"]
    set_language(session, "en")
    assert session.lang == "en"
    assert session.messages[0]["content"] != german
    assert "Pizzeria Default" in session.messages[0]["content"]
    assert len(session.messages) == history_before  # history preserved


def test_apology_follows_session_language():
    def dead(messages, tool_schemas):
        raise GatewayError("gateway timed out twice")
    session = create_session(config_stub(), FakeBase())
    set_language(session, "en")
    text = Agent(config_stub(), chat_fn=dead).run_turn(session, "hi")
    assert "sorry" in text.lower()


def test_spoken_note_is_ephemeral_per_turn():
    """The spoken-style note reaches the model for the spoken turn only —
    it is never persisted, and a later typed turn does not inherit it."""
    seen = []

    def say(messages, tool_schemas):
        seen.append([m["content"] for m in messages
                     if m["role"] == "system"])
        return {"content": "ok"}
    session = create_session(config_stub(), FakeBase())
    agent = Agent(config_stub(), chat_fn=say)
    agent.run_turn(session, "hallo", spoken=True)
    assert any("Diese Antwort wird vorgelesen" in c
               for c in seen[-1])  # note seen this turn
    agent.run_turn(session, "hallo")
    assert not any("Diese Antwort wird vorgelesen" in c
                   for c in seen[-1])  # gone next turn
    assert not any(m["role"] == "system"
                   and "Diese Antwort wird vorgelesen" in m["content"]
                   for m in session.messages)  # never persisted


def confirm_ready_session(chat_fn):
    session = create_session(config_stub(), FakeBase())
    fake = session.client
    tools.dispatch(session.order, session.menu, fake, "add_items",
                   {"items": [{"type": "pizza", "code": "margherita",
                               "qty": 2}]})
    tools.dispatch(session.order, session.menu, fake, "set_customer",
                   {"first_name": "Marco"})
    tools.dispatch(session.order, session.menu, fake, "read_back", {})
    return session, Agent(config_stub(), chat_fn=chat_fn)


def test_confirm_and_submit_happy_path():
    def phrase(messages, tool_schemas):
        return {"content": "Bestellt!"}
    session, agent = confirm_ready_session(phrase)
    events = []
    text = agent.confirm_and_submit(session, session.order.revision,
                                    events.append)
    assert text == "Bestellt!"
    assert session.order.state is State.SUBMITTED
    tool_names = [e["tool"] for e in events if e["type"] == "tool_call"]
    assert tool_names == ["confirm_order", "submit_order"]
    # synthetic history is model-shaped: assistant tool_calls + tool result
    roles = [m["role"] for m in session.messages]
    assert roles.count("tool") == 2
    assert session.messages[-1]["role"] == "assistant"


def test_confirm_with_stale_revision_submits_nothing():
    def phrase(messages, tool_schemas):
        return {"content": "Da hat sich etwas geändert."}
    session, agent = confirm_ready_session(phrase)
    stale = session.order.revision
    tools.dispatch(session.order, session.menu, session.client,
                   "add_items", {"items": [{"type": "pasta",
                                            "code": "pesto", "qty": 1}]})
    events = []
    agent.confirm_and_submit(session, stale, events.append)
    errors = [e["result"]["error"]["code"] for e in events
              if e["type"] == "tool_result" and "error" in e["result"]]
    assert errors == ["stale_revision"]
    assert session.client.submits == 0
    assert session.order.state is not State.SUBMITTED
    # the failed dispatch is in the history exactly like a model call
    assert session.messages[-2]["role"] == "tool"


def test_confirm_gateway_death_still_answers():
    """Answer-or-rendered-error invariant on /confirm: dispatches applied,
    apology streamed as an assistant event."""
    def dead(messages, tool_schemas):
        raise GatewayError("gateway request failed")
    session, agent = confirm_ready_session(dead)
    events = []
    text = agent.confirm_and_submit(session, session.order.revision,
                                    events.append)
    assert session.order.state is State.SUBMITTED  # order went through
    assert any(e["type"] == "assistant" for e in events)
    assert text  # the apology is the rendered answer


def test_gateway_status_callback_reports_down():
    statuses = []
    agent = Agent(AgentConfig(url="http://127.0.0.1:9", key="k",
                              model="stub", lang="de"),
                  status_cb=statuses.append)
    session = create_session(config_stub(), FakeBase())
    text = agent.run_turn(session, "hi")  # closed port → down + apology
    assert statuses and statuses[-1] == "down"
    assert text


# --- the live acceptance test (opt-in) ------------------------------------
# SPEC "What done looks like": full conversation, submit, then read the
# pizzeria's orders back and assert the order is there with the right
# customer, items and quantities — exactly, not a near match.

@pytest.mark.skipif(os.environ.get("PIZZA_LIVE_TEST") != "1",
                    reason="live test only with PIZZA_LIVE_TEST=1")
def test_live_acceptance():
    client = PizzaSim.from_env()
    menu = Menu(client.get_menu())
    order = Order()
    for name, args in [
        ("add_items", {"items": [
            {"type": "pizza", "code": "margherita", "qty": 2},
            {"type": "pasta", "code": "funghi", "qty": 1}]}),
        ("set_customer", {"first_name": "Akzeptanz",
                          "street_one": "via Verdi 7"}),
        ("read_back", {}),
    ]:
        result = tools.dispatch(order, menu, client, name, args)
        assert "error" not in result, result
    result = tools.dispatch(order, menu, client, "confirm_order",
                            {"revision": order.revision})
    assert "error" not in result, result
    result = tools.dispatch(order, menu, client, "submit_order", {})

    # 1. POST returned an order id
    order_id = result.get("order_id")
    assert order_id, result

    # 2. reading the pizzeria's orders back shows the order
    listed = {o["id"] for o in client.list_orders()}
    assert order_id in listed

    # 3. + 4. right customer, exact items and quantities
    detail = client.get_order(order_id)
    assert detail["customer"]["first_name"] == "Akzeptanz"
    assert tools._same_items(detail["items"], order.items)

codex
I’ve verified the four round-1 change claims in code and tests. Next I’m checking for residual breaches against the patched SPEC and approved plan: submission semantics, startup/session invariants, web contract details, and any test blind spots that would still matter for this round’s score.
exec
/bin/bash -lc "sed -n '1,340p' core/tools.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,240p' core/menu.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,220p' channels/speech.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' core/pizzasim.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' core/order.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' tests/test_web_e2e.py" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 442ms:
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
        self._prices: dict[tuple[str, str], float] = {
            (t, p["code"]): p.get("price", 0.0)
            for t, key in (("pizza", "pizzas"), ("pasta", "pasta"))
            for p in payload[key]
        }
        self.toppings: list[str] = list(payload.get("toppings", []))

    def as_tool_result(self) -> dict:
        return {
            "pizzas": [{"code": c, "name": n,
                        "price": self._prices[("pizza", c)]}
                       for c, n in self._by_type["pizza"].items()],
            "pasta": [{"code": c, "name": n,
                       "price": self._prices[("pasta", c)]}
                      for c, n in self._by_type["pasta"].items()],
            "toppings": self.toppings,
        }

    def price(self, type_: str, code: str) -> float:
        return self._prices[(type_, code)]

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

 succeeded in 609ms:
"""Speech service client: self-hosted, OpenAI-compatible, optional.

The browser captures and plays audio; recognition and synthesis happen
here, server-side, against {SPEECH_URL}. The language sent with STT/TTS is
the session language — there is no separate speech-language config.
"""
from __future__ import annotations

import sys

import httpx

from core.pizzasim import optional_env


class SpeechUnavailable(Exception):
    pass


class SpeechService:
    """All-or-nothing: enabled only if SPEECH_URL is set, all models are
    configured, and the service answered the startup probe with 2xx."""

    def __init__(self):
        self.url = (optional_env("SPEECH_URL") or "").rstrip("/")
        self.stt_model = optional_env("SPEECH_STT_MODEL")
        self.tts_model = optional_env("SPEECH_TTS_MODEL")
        self.voice = optional_env("SPEECH_TTS_VOICE")
        self.enabled = False
        if self.url and self.stt_model and self.tts_model and self.voice:
            try:
                httpx.get(f"{self.url}/v1/models",
                          timeout=3.0).raise_for_status()
                self.enabled = True
            except httpx.HTTPError:
                print("speech service not answering — text-only mode",
                      file=sys.stderr)

    def stt(self, audio: bytes, filename: str, content_type: str,
            lang: str) -> str:
        try:
            response = httpx.post(
                f"{self.url}/v1/audio/transcriptions",
                files={"file": (filename, audio, content_type)},
                data={"model": self.stt_model, "language": lang},
                timeout=60.0)
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise SpeechUnavailable(str(exc)) from exc
        return response.json().get("text", "")

    def tts(self, text: str, lang: str) -> tuple[bytes, str]:
        try:
            response = httpx.post(
                f"{self.url}/v1/audio/speech",
                json={"model": self.tts_model, "voice": self.voice,
                      "input": text, "language": lang},
                timeout=60.0)
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise SpeechUnavailable(str(exc)) from exc
        return (response.content,
                response.headers.get("content-type", "audio/mpeg"))

 succeeded in 672ms:
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
                unit_price=menu.price(raw.get("type", ""),
                                      raw.get("code", "")),
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


def _same_items(api_items: list[dict], basket) -> bool:
    def norm(entries):
        return sorted(
            (e["type"], e["code"], e["qty"], tuple(sorted(e["extras"])))
            for e in entries
        )
    ours = [{"type": i.type, "code": i.code, "qty": i.qty,
             "extras": list(i.extras)} for i in basket]
    return norm(api_items) == norm(ours)


def _submit(order: Order, client: PizzaSim) -> dict:
    state.begin_submit(order)

    if order.submit_unknown:
        # A previous attempt timed out: verify against the order list
        # before any retry — a blind retry doubles a real order. The list
        # carries no items, so a shortlisted candidate is verified via the
        # detail endpoint before it is adopted.
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
            try:
                detail = client.get_order(found["id"])
            except PizzaSimError:
                return _error("submit_unknown", _UNSURE)
            if _same_items(detail.get("items", []), order.items):
                eta = max(0, int(found.get("ready_at", 0) - time.time()))
                state.mark_submitted(order, {
                    "order_id": found["id"],
                    "status": found.get("status", "ordered"),
                    "eta_seconds": eta,
                })
                return {**order.result, "snapshot": order.snapshot()}
        # verified absent (or a different order) → exactly one real retry

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

 succeeded in 582ms:
"""Web channel: API-surface tests plus the mandatory headless-browser
end-to-end tests asserting against the DOM. Fully offline: the app under
test talks to a stub PizzaSim and a stub (scripted) gateway on localhost.
The customer never talks to curl — and neither do these assertions."""
from __future__ import annotations

import json
import os

import httpx
import pytest

from tests.stubs import StubGateway, StubPizzaSim, run_server

PZ1 = "11111111-aaaa-bbbb-cccc-000000000001"
PZ2 = "22222222-aaaa-bbbb-cccc-000000000002"
PZ2_ENTRY = {"id": PZ2, "name": "Stub Pizzeria Due"}


@pytest.fixture(scope="module")
def stack():
    """Stub PizzaSim + stub gateway + the real app, all on localhost."""
    pizzasim = StubPizzaSim()
    gateway = StubGateway()
    ps_server, ps_url = run_server(pizzasim.app)
    gw_server, gw_url = run_server(gateway.app)
    os.environ.update({
        "PIZZASIM_URL": ps_url,
        "PIZZASIM_API_KEY": "stub-key",
        "PIZZERIA_ID": PZ1,
        "PIZZERIA_LANG": "de",
        "LITELLM_PIZZA_URL": gw_url,
        "LITELLM_PIZZA_KEY": "stub-key",
        "LITELLM_PIZZA_MODEL_1": "scripted-stub",
        "APP_VERSION": "2.0.0",
    })
    for var in ("SPEECH_URL", "SPEECH_STT_MODEL", "SPEECH_TTS_MODEL",
                "SPEECH_TTS_VOICE", "LITELLM_PIZZA_MODEL_2"):
        os.environ.pop(var, None)
    from channels import web  # app boots against the stub env
    app_server, app_url = run_server(web.app)
    yield {"pizzasim": pizzasim, "gateway": gateway, "url": app_url,
           "web": web, "ps_url": ps_url}
    for server in (app_server, ps_server, gw_server):
        server.should_exit = True


def stream_lines(client, path, body):
    with client.stream("POST", path, json=body) as response:
        response.raise_for_status()
        return [json.loads(line) for line in response.iter_lines()
                if line.strip()]


@pytest.fixture()
def api(stack):
    with httpx.Client(base_url=stack["url"], timeout=30.0) as client:
        yield client


# --- API surface (ordering matters: health-unknown runs first) ------------

def test_health_gateway_unknown_before_first_turn(api):
    health = api.get("/health").json()
    assert health == {"api": "ok", "gateway": "unknown"}


def test_config_contract(stack, api):
    cfg = api.get("/config").json()
    assert cfg["version"] == "2.0.0"
    assert cfg["speech"] is False
    assert cfg["lang_default"] == "de"
    assert [p["id"] for p in cfg["pizzerias"]] == [PZ1, PZ2]
    assert cfg["preselected_id"] == PZ1
    assert cfg["dashboard_base"] == f"{stack['ps_url']}/dashboard/pizzerias"
    assert cfg["docs_url"] == f"{stack['ps_url']}/swagger.html"


def test_config_list_unavailable_no_fallback(stack, api):
    stack["pizzasim"].fail_pizzerias = True
    try:
        cfg = api.get("/config").json()
        assert cfg["pizzerias"] is None  # never a bundled fallback list
        assert api.get("/health").json()["api"] == "down"
    finally:
        stack["pizzasim"].fail_pizzerias = False


def test_session_and_greeting_then_gateway_ok(api):
    created = api.post("/session", json={}).json()
    assert created["pizzeria_id"] == PZ1
    assert created["pizzeria_name"] == "Stub Pizzeria Uno"
    events = stream_lines(api, "/chat",
                          {"session_id": created["session_id"],
                           "text": None})
    kinds = [e["type"] for e in events]
    assert "assistant" in kinds and kinds[-1] == "done"
    assert api.get("/health").json()["gateway"] == "ok"


def test_session_unknown_pizzeria_409(api):
    response = api.post("/session", json={"pizzeria_id": "no-such-id"})
    assert response.status_code == 409


def test_chat_unknown_session_404(api):
    assert api.post("/chat", json={"session_id": "ghost",
                                   "text": "hi"}).status_code == 404


def test_turn_in_flight_409(stack, api):
    sid = api.post("/session", json={}).json()["session_id"]
    lock = stack["web"].app.state.locks[sid]
    assert lock.acquire(blocking=False)
    try:
        response = api.post("/chat", json={"session_id": sid, "text": "x"})
        assert response.status_code == 409
    finally:
        lock.release()


def test_language_switch(api):
    sid = api.post("/session", json={}).json()["session_id"]
    assert api.post("/language",
                    json={"session_id": sid,
                          "lang": "en"}).json() == {"lang": "en"}
    assert api.post("/language",
                    json={"session_id": sid,
                          "lang": "xx"}).status_code == 422


def test_tool_error_surfaces_as_rendered_answer(api):
    """The 422-shaped tool error reaches the customer as model-phrased
    plain language in the stream, never as a code."""
    sid = api.post("/session", json={}).json()["session_id"]
    stream_lines(api, "/chat", {"session_id": sid, "text": None})
    events = stream_lines(api, "/chat",
                          {"session_id": sid,
                           "text": "Einmal Bolognese bitte"})
    errors = [e for e in events if e["type"] == "tool_result"
              and "error" in e["result"]]
    assert errors and errors[0]["result"]["error"]["code"] == "unknown_item"
    final = [e for e in events if e["type"] == "assistant"][-1]
    assert "nicht im Angebot" in final["text"]
    assert "unknown_item" not in final["text"]


def test_confirm_endpoint_places_order_in_selected_tenant(stack, api):
    created = api.post("/session", json={"pizzeria_id": PZ2}).json()
    sid = created["session_id"]
    stream_lines(api, "/chat", {"session_id": sid, "text": None})
    stream_lines(api, "/chat", {"session_id": sid,
                                "text": "Zwei Margherita bitte"})
    events = stream_lines(api, "/chat", {"session_id": sid,
                                         "text": "Ich heiße Eva"})
    snapshot = [e["result"]["snapshot"] for e in events
                if e["type"] == "tool_result"
                and e.get("tool") == "read_back"][-1]
    events = stream_lines(api, "/confirm",
                          {"session_id": sid,
                           "revision": snapshot["revision"]})
    submitted = [e["result"] for e in events
                 if e["type"] == "tool_result"
                 and e.get("tool") == "submit_order"][-1]
    assert submitted["order_id"]
    # the order landed under the CHOSEN tenant, not the preselected one
    assert stack["pizzasim"].orders.get(PZ2), "order missing in tenant"
    assert not any(o["customer"]["first_name"] == "Eva"
                   for o in stack["pizzasim"].orders.get(PZ1, []))
    stored = stack["pizzasim"].orders[PZ2][-1]
    assert stored["customer"]["first_name"] == "Eva"
    assert stored["items"] == [{"type": "pizza", "code": "margherita",
                                "qty": 2, "extras": []}]


def test_confirm_stale_revision_streams_error(api):
    created = api.post("/session", json={}).json()
    sid = created["session_id"]
    stream_lines(api, "/chat", {"session_id": sid,
                                "text": "Zwei Margherita bitte"})
    events = stream_lines(api, "/confirm",
                          {"session_id": sid, "revision": 99})
    errors = [e["result"]["error"]["code"] for e in events
              if e["type"] == "tool_result" and "error" in e["result"]]
    assert errors  # refused by the state machine, streamed to the UI
    assert events[-1]["state"]["state"] != "SUBMITTED"


# --- browser end-to-end (Playwright, DOM assertions) ----------------------

@pytest.fixture(scope="module")
def page_factory(stack):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield lambda: browser.new_page()
        browser.close()


def open_app(page_factory, stack):
    page = page_factory()
    page.goto(stack["url"], timeout=30000)
    page.wait_for_selector(".msg.assistant", timeout=30000)
    return page


def test_e2e_full_order_with_header_footer_contract(page_factory, stack):
    stack["gateway"].mode = "ok"
    page = open_app(page_factory, stack)

    # header contract
    assert page.locator("#pizzeria-name").inner_text() == \
        "Stub Pizzeria Uno"
    first_option = page.locator("#pizzeria-select option").first
    assert "Stub Pizzeria Uno (11111111)" == first_option.inner_text()
    dash = page.locator("#dashboard-link")
    assert dash.get_attribute("href").endswith(
        f"/dashboard/pizzerias/{PZ1}")
    assert dash.get_attribute("target") == "_blank"
    # footer contract
    assert page.locator("#version").inner_text() == "v2.0.0"
    assert page.locator("#uuid").inner_text() == PZ1
    assert page.locator("#docs-link").get_attribute("href").endswith(
        "/swagger.html")
    page.wait_for_selector("#health-api.ok", timeout=15000)
    page.wait_for_selector("#health-gateway.ok", timeout=15000)
    # speech disabled → controls not rendered
    assert page.locator("#mic").is_hidden()
    assert page.locator("#tts-wrap").is_hidden()

    def say(text):
        page.fill("#text", text)
        page.click("#send")

    say("Was kostet eine Margherita?")
    page.wait_for_selector("text=8.5 €", timeout=30000)

    say("Zwei Margherita bitte")
    page.wait_for_selector("#basket-lines li", timeout=30000)
    assert "2× Margherita" in page.locator("#basket-lines").inner_text()
    assert "17,00 €" in page.locator("#basket-total").inner_text()

    say("Ich heiße Eva")
    page.wait_for_selector(".readback button:enabled", timeout=30000)
    readback = page.locator(".readback").last
    assert "17,00 €" in readback.inner_text()

    page.locator(".readback button:enabled").click()
    page.wait_for_selector("#submitted-banner:not([hidden])",
                           timeout=30000)
    banner = page.locator("#submitted-banner").inner_text()
    order_id = banner.split()[-1]
    assert len(order_id) == 36  # a real order id, visible to the customer
    assert page.locator("#basket.locked").count() == 1
    assert page.locator(".readback button").last.is_disabled()
    assert page.locator("details.steps").count() >= 3  # steps rendered
    page.close()


def test_e2e_pizzeria_switch_and_language(page_factory, stack):

 succeeded in 639ms:
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
        self.base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._transport = transport
        self._client = httpx.Client(
            base_url=self.base_url,
            headers={"X-API-Key": api_key},
            timeout=_TIMEOUT,
            transport=transport,
        )

    def for_pizzeria(self, pizzeria_id: str) -> "PizzaSim":
        """Tenant-bound sibling client — same server, same key. Used by the
        session factory; a session's tenant never changes afterwards."""
        return PizzaSim(self.base_url, self._api_key, pizzeria_id,
                        transport=self._transport)

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

    def get_order(self, order_id: str) -> dict:
        """Full order incl. customer and items — the list endpoint carries
        neither."""
        return self._request(
            "GET", f"/pizzerias/{self.pizzeria_id}/orders/{order_id}"
        )

    def submit_order(self, customer: dict, items: list[dict]) -> dict:
        """The only network write. Returns order_id, status, eta_seconds."""
        return self._request(
            "POST",
            f"/pizzerias/{self.pizzeria_id}/orders",
            json={"customer": customer, "items": items},
        )

    def check_street(self, street: str) -> dict:
        return self._request("GET", "/location", params={"street": street})

 succeeded in 631ms:
"""Order data: items, customer, revision, submit bookkeeping. Pure data."""
from __future__ import annotations

from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal
from enum import Enum


def _cents(value: Decimal) -> float:
    return float(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


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
    # Copied from the session menu snapshot at add time; totals are
    # computed here in core only — the model never does arithmetic.
    unit_price: float = 0.0

    def line_key(self) -> tuple:
        return (self.type, self.code, tuple(sorted(self.extras)))

    def line_total(self) -> float:
        return _cents(Decimal(str(self.unit_price)) * self.qty)


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
                    "unit_price": i.unit_price,
                    "line_total": i.line_total(),
                }
                for i in self.items
            ],
            "basket_total": _cents(
                sum((Decimal(str(i.unit_price)) * i.qty
                     for i in self.items), Decimal("0"))
            ),
            "customer": self.customer.as_dict() if self.customer else None,
            "read_back_done": self.read_back_revision == self.revision,
        }

exec
/bin/bash -lc "sed -n '1,320p' core/state.py" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 0ms:
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
    # A mutation makes any unverified submit attempt meaningless: the
    # recovery correlation belongs to the basket that was confirmed then,
    # not to whatever the basket becomes now.
    order.submit_unknown = False
    order.submit_attempted_at = None
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

exec
/bin/bash -lc "sed -n '1,220p' tests/stubs.py" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 0ms:
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
        self.app = app = FastAPI()

        @app.post("/chat/completions")
        async def chat(request: Request):
            if self.mode == "http500":
                return JSONResponse({"error": "boom"}, status_code=500)
            body = await request.json()
            if self.mode == "empty":
                return _reply({"content": ""})
            return _reply(self._script(body["messages"]))


def _reply(message: dict) -> dict:
    return {"choices": [{"message": message}]}


def _last_tool(messages: list[dict]) -> tuple[str, dict] | None:
    last = messages[-1]
    if last.get("role") != "tool":
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

exec
/bin/bash -lc 'rg -n "404|sessionLost|lost session|resend|TimeoutError|AbortSignal|startSession no longer clears|basket survive|/confirm" SPEC.md PLAN.md reviews/round17-impl2.md decisions/qa.md -S' in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 0ms:
reviews/round17-impl2.md:17:Task: Review the v2 IMPLEMENTATION against SPEC.md (v3, patched, gate-approved) and PLAN.md (v2, approved 23/25, all tickets checked off). The v2 delta on top of the previously approved v1 build: prices/totals in core (core/order.py, core/menu.py, core/tools.py), per-session tenancy via a core session factory + language authority + confirm_and_submit (core/agent.py), web API v2 (channels/web.py: /config /session /chat /confirm /language /health), channels/speech.py, fully rebuilt UI (channels/static/), offline stubs (tests/stubs.py) and the browser E2E suite (tests/test_web_e2e.py), plus extended unit/tool tests.
reviews/round17-impl2.md:684:(header/footer/basket/confirm control/answer invariant), APP_VERSION,
reviews/round17-impl2.md:753:process refuses to start — the startup 404 row); fetch `/menu` once as a
reviews/round17-impl2.md:804:- Click → `POST /confirm {session_id, revision}` → **one core method**
reviews/round17-impl2.md:824:     `assistant` event on failure — so `/confirm` satisfies the
reviews/round17-impl2.md:853:  protocol; `text: null` = greeting turn). 404 for unknown session (the
reviews/round17-impl2.md:855:- `POST /confirm {session_id, revision}` → NDJSON stream (same event
reviews/round17-impl2.md:863:  `/chat` or `/confirm` (both share the single Agent gateway path) sets
reviews/round17-impl2.md:916:    notice "the agent did not answer — resend?";
reviews/round17-impl2.md:918:    (error, timeout, connection lost) + a resend button that re-posts the
reviews/round17-impl2.md:923:  notices, resend prompts) follows `session.lang` — the language the
reviews/round17-impl2.md:969:3. Confirm path exactly: UI control → POST /confirm {session_id, revision}
reviews/round17-impl2.md:973:   resend paths, header/footer contract, basket+total, connection states,
reviews/round17-impl2.md:1172:        # call from any session (/chat and /confirm share this path).
reviews/round17-impl2.md:1861:Contract (PLAN v2): /config, /session, /chat, /confirm, /language,
reviews/round17-impl2.md:1995:        raise HTTPException(404, "unknown session")
reviews/round17-impl2.md:2038:@app.post("/confirm")
reviews/round17-impl2.md:2065:        raise HTTPException(404, "speech is not available")
reviews/round17-impl2.md:2480:    if response.status_code == 404:
reviews/round17-impl2.md:2539:        404-pizzeria case — the process must refuse to start."""
reviews/round17-impl2.md:2676:def test_chat_unknown_session_404(api):
reviews/round17-impl2.md:2678:                                   "text": "hi"}).status_code == 404
reviews/round17-impl2.md:2729:    events = stream_lines(api, "/confirm",
reviews/round17-impl2.md:2751:    events = stream_lines(api, "/confirm",
reviews/round17-impl2.md:2892:def test_e2e_stream_without_answer_offers_resend(page_factory, stack):
reviews/round17-impl2.md:2902:    page.locator(".notice button").last.click()  # resend, now answered
reviews/round17-impl2.md:2927:    resend: "Erneut senden",
reviews/round17-impl2.md:2952:    resend: "Resend",
reviews/round17-impl2.md:3001:function notice(text, resendText) {
reviews/round17-impl2.md:3005:  if (resendText !== undefined) {
reviews/round17-impl2.md:3007:    btn.textContent = t("resend");
reviews/round17-impl2.md:3008:    btn.onclick = () => { div.remove(); sendTurn(resendText); };
reviews/round17-impl2.md:3087:async function readStream(response, resendText) {
reviews/round17-impl2.md:3131:  if (!assistantAnswered) notice(t("notAnswered"), resendText);
reviews/round17-impl2.md:3135:async function streamPost(path, body, resendText) {
reviews/round17-impl2.md:3150:    if (res.status === 404) { await startSession(session.pizzeriaId); return ""; }
reviews/round17-impl2.md:3154:    finalText = await readStream(res, resendText);
reviews/round17-impl2.md:3158:    else if (err.name === "TimeoutError") notice(t("errTimeout"), resendText);
reviews/round17-impl2.md:3159:    else if (err.message === "http") notice(t("errHttp"), resendText);
reviews/round17-impl2.md:3160:    else notice(t("errNetwork"), resendText);
reviews/round17-impl2.md:3176:    "/confirm", { session_id: session.id, revision });
reviews/round17-impl2.md:3455:def test_404_mapped():
reviews/round17-impl2.md:3457:        client_returning(respond(404, {})).list_orders()
reviews/round17-impl2.md:3945:            return JSONResponse({"error": "not_found"}, status_code=404)
reviews/round17-impl2.md:4063:channels/web.py:4:Contract (PLAN v2): /config, /session, /chat, /confirm, /language,
reviews/round17-impl2.md:4085:channels/web.py:208:        raise HTTPException(404, "speech is not available")
reviews/round17-impl2.md:4427:    """Answer-or-rendered-error invariant on /confirm: dispatches applied,
reviews/round17-impl2.md:4664:  happened and offers to resend.
reviews/round17-impl2.md:4733:| Gateway timeout | one retry, then abort turn | plain apology, offer to resend |
reviews/round17-impl2.md:4735:| `404` on the preselected `PIZZERIA_ID` | fail at startup, not mid-call | — (process refuses to start) |
reviews/round17-impl2.md:4760:PLAN.md:9:(header/footer/basket/confirm control/answer invariant), APP_VERSION,
reviews/round17-impl2.md:4786:PLAN.md:129:- Click → `POST /confirm {session_id, revision}` → **one core method**
reviews/round17-impl2.md:4795:PLAN.md:178:  protocol; `text: null` = greeting turn). 404 for unknown session (the
reviews/round17-impl2.md:4797:PLAN.md:180:- `POST /confirm {session_id, revision}` → NDJSON stream (same event
reviews/round17-impl2.md:4813:PLAN.md:248:  notices, resend prompts) follows `session.lang` — the language the
reviews/round17-impl2.md:4830:PLAN.md:351:5. **Web API surface.** /config, /session, /confirm, /language, /health,
reviews/round17-impl2.md:4831:PLAN.md:352:   session 404/409 semantics, speech extraction to `channels/speech.py`.
reviews/round17-impl2.md:4900:decisions/qa.md:32:3. Confirm path exactly: UI control → POST /confirm {session_id, revision}
reviews/round17-impl2.md:4901:decisions/qa.md:36:   resend paths, header/footer contract, basket+total, connection states,
reviews/round17-impl2.md:4911:| Stream ends without final message | UI-side detection via `done`-without-`assistant` → notice + resend |
reviews/round17-impl2.md:4912:| Gateway unreachable | existing retry-once → apology (now also an `assistant` event, v1 fix) + UI resend offer |
reviews/round17-impl2.md:4961:     rendered + resend control;
reviews/round17-impl2.md:4963:     UI notice + resend control.
reviews/round17-impl2.md:4996:5. **Web API surface.** /config, /session, /confirm, /language, /health,
reviews/round17-impl2.md:4997:   session 404/409 semantics, speech extraction to `channels/speech.py`.
reviews/round17-impl2.md:5004:   error/resend paths, submitted lock.
reviews/round17-impl2.md:5100:   404	  $("text").value = "";
reviews/round17-impl2.md:5154:   223	  if (!assistantAnswered) notice(t("notAnswered"), resendText);
reviews/round17-impl2.md:5158:   227	async function streamPost(path, body, resendText) {
reviews/round17-impl2.md:5173:   242	    if (res.status === 404) { await startSession(session.pizzeriaId); return ""; }
reviews/round17-impl2.md:5177:   246	    finalText = await readStream(res, resendText);
reviews/round17-impl2.md:5181:   250	    else if (err.name === "TimeoutError") notice(t("errTimeout"), resendText);
reviews/round17-impl2.md:5182:   251	    else if (err.message === "http") notice(t("errHttp"), resendText);
reviews/round17-impl2.md:5183:   252	    else notice(t("errNetwork"), resendText);
reviews/round17-impl2.md:5199:   268	    "/confirm", { session_id: session.id, revision });
reviews/round17-impl2.md:5342:- Important: [channels/static/app.js](/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js:242) breaks the web-channel answer invariant on expired/unknown sessions. A `404` from `/chat` or `/confirm` triggers `startSession(session.pizzeriaId)` and returns immediately, so the user’s sent message is neither answered nor rendered as an error/resend path. SPEC requires every sent message to end in a visible assistant reply or visible error.
reviews/round17-impl2.md:5344:- Important: [channels/static/app.js](/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js:236) does not implement request timeouts even though the UI claims to distinguish them. There is no timer-based abort around `fetch`; the `TimeoutError` branch at [app.js:250](/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js:250) is effectively dead. If `/chat` or `/confirm` hangs, the page can sit on “agent is working” indefinitely instead of showing the required timeout notice plus resend affordance.
reviews/round17-impl2.md:5361:- Handle `/chat`/`/confirm` `404` by rendering a visible error/resend path for the user’s original message, or by transparently recreating the session and replaying the same request.
reviews/round17-impl2.md:5362:- Add a real client-side timeout/abort for streamed requests so the timeout notice and resend control can actually occur.
reviews/round17-impl2.md:5369:- Important: [channels/static/app.js](/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js:242) breaks the web-channel answer invariant on expired/unknown sessions. A `404` from `/chat` or `/confirm` triggers `startSession(session.pizzeriaId)` and returns immediately, so the user’s sent message is neither answered nor rendered as an error/resend path. SPEC requires every sent message to end in a visible assistant reply or visible error.
reviews/round17-impl2.md:5371:- Important: [channels/static/app.js](/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js:236) does not implement request timeouts even though the UI claims to distinguish them. There is no timer-based abort around `fetch`; the `TimeoutError` branch at [app.js:250](/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js:250) is effectively dead. If `/chat` or `/confirm` hangs, the page can sit on “agent is working” indefinitely instead of showing the required timeout notice plus resend affordance.
reviews/round17-impl2.md:5388:- Handle `/chat`/`/confirm` `404` by rendering a visible error/resend path for the user’s original message, or by transparently recreating the session and replaying the same request.
reviews/round17-impl2.md:5389:- Add a real client-side timeout/abort for streamed requests so the timeout notice and resend control can actually occur.
SPEC.md:427:  happened and offers to resend.
SPEC.md:496:| Gateway timeout | one retry, then abort turn | plain apology, offer to resend |
SPEC.md:498:| `404` on the preselected `PIZZERIA_ID` | fail at startup, not mid-call | — (process refuses to start) |
decisions/qa.md:32:3. Confirm path exactly: UI control → POST /confirm {session_id, revision}
decisions/qa.md:36:   resend paths, header/footer contract, basket+total, connection states,
PLAN.md:9:(header/footer/basket/confirm control/answer invariant), APP_VERSION,
PLAN.md:78:process refuses to start — the startup 404 row); fetch `/menu` once as a
PLAN.md:129:- Click → `POST /confirm {session_id, revision}` → **one core method**
PLAN.md:149:     `assistant` event on failure — so `/confirm` satisfies the
PLAN.md:178:  protocol; `text: null` = greeting turn). 404 for unknown session (the
PLAN.md:180:- `POST /confirm {session_id, revision}` → NDJSON stream (same event
PLAN.md:188:  `/chat` or `/confirm` (both share the single Agent gateway path) sets
PLAN.md:241:    notice "the agent did not answer — resend?";
PLAN.md:243:    (error, timeout, connection lost) + a resend button that re-posts the
PLAN.md:248:  notices, resend prompts) follows `session.lang` — the language the
PLAN.md:266:| Stream ends without final message | UI-side detection via `done`-without-`assistant` → notice + resend |
PLAN.md:267:| Gateway unreachable | existing retry-once → apology (now also an `assistant` event, v1 fix) + UI resend offer |
PLAN.md:316:     rendered + resend control;
PLAN.md:318:     UI notice + resend control.
PLAN.md:351:5. **Web API surface.** /config, /session, /confirm, /language, /health,
PLAN.md:352:   session 404/409 semantics, speech extraction to `channels/speech.py`.
PLAN.md:359:   error/resend paths, submitted lock.

codex
One likely edge case has emerged: the shared `404` session-loss path recreates the session for both `/chat` and `/confirm`, but only `/chat` has resend payload available. I’m checking whether the governing SPEC/PLAN text makes that a real breach or just an untested nice-to-have.
exec
/bin/bash -lc "sed -n '400,520p' SPEC.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '260,520p' tests/test_web_e2e.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '232,330p' PLAN.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "wc -l tests/test_web_e2e.py && nl -ba tests/test_web_e2e.py | sed -n '1,420p'" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 365ms:
def test_e2e_pizzeria_switch_and_language(page_factory, stack):
    stack["gateway"].mode = "ok"
    page = open_app(page_factory, stack)
    page.fill("#text", "Zwei Margherita bitte")
    page.click("#send")
    page.wait_for_selector("#basket-lines li", timeout=30000)

    page.select_option("#pizzeria-select", PZ2)
    page.wait_for_function(
        "document.getElementById('pizzeria-name').textContent === "
        "'Stub Pizzeria Due'", timeout=30000)
    assert page.locator("#uuid").inner_text() == PZ2
    assert page.locator("#basket-lines li").count() == 0  # basket cleared
    page.wait_for_selector(".msg.assistant", timeout=30000)  # fresh greet

    page.locator("#lang-switch button[data-lang=en]").click()
    page.wait_for_function(
        "document.getElementById('start-over').textContent === "
        "'Start over'", timeout=15000)  # chrome follows the declared lang
    page.close()


def test_e2e_vanished_pizzeria_refreshes_selector(page_factory, stack):
    stack["gateway"].mode = "ok"
    page = open_app(page_factory, stack)
    page.fill("#text", "Zwei Margherita bitte")
    page.click("#send")
    page.wait_for_selector("#basket-lines li", timeout=30000)
    stack["pizzasim"].pizzerias = [p for p in stack["pizzasim"].pizzerias
                                   if p["id"] != PZ2]
    try:
        page.select_option("#pizzeria-select", PZ2)
        page.wait_for_selector(".notice", timeout=30000)
        page.wait_for_function(
            "document.querySelectorAll('#pizzeria-select option')"
            ".length === 1", timeout=15000)
        # the failed switch must NOT hide the still-live order
        assert page.locator("#basket-lines li").count() == 1
        assert page.locator(".msg.user").count() == 1
    finally:
        stack["pizzasim"].pizzerias.append(PZ2_ENTRY)
    page.close()


def test_e2e_lost_session_recreates_and_offers_resend(page_factory,
                                                      stack):
    """Server no longer knows the session (e.g. restart): the customer
    sees a plain notice, gets a fresh session, and can resend."""
    stack["gateway"].mode = "ok"
    page = open_app(page_factory, stack)
    stack["web"].app.state.sessions.clear()  # simulate a lost session
    page.fill("#text", "Was kostet eine Margherita?")
    page.click("#send")
    page.wait_for_selector(".notice button", timeout=30000)  # resend
    page.locator(".notice button").last.click()
    page.wait_for_selector("text=8.5 €", timeout=30000)
    page.close()


def test_e2e_tool_error_leaves_visible_message(page_factory, stack):
    stack["gateway"].mode = "ok"
    page = open_app(page_factory, stack)
    page.fill("#text", "Einmal Bolognese bitte")
    page.click("#send")
    page.wait_for_selector("text=nicht im Angebot", timeout=30000)
    page.close()


def test_e2e_gateway_unreachable_leaves_visible_message(page_factory,
                                                        stack):
    stack["gateway"].mode = "ok"
    page = open_app(page_factory, stack)
    stack["gateway"].mode = "http500"
    try:
        page.fill("#text", "Hallo?")
        page.click("#send")
        # the retry-once path ends in a rendered apology — an answer
        page.wait_for_selector("text=schiefgegangen", timeout=30000)
    finally:
        stack["gateway"].mode = "ok"
    page.close()


def test_e2e_stream_without_answer_offers_resend(page_factory, stack):
    stack["gateway"].mode = "ok"
    page = open_app(page_factory, stack)
    stack["gateway"].mode = "empty"
    try:
        page.fill("#text", "Hallo?")
        page.click("#send")
        page.wait_for_selector(".notice button", timeout=30000)
    finally:
        stack["gateway"].mode = "ok"
    page.locator(".notice button").last.click()  # resend, now answered
    page.wait_for_function(
        "document.querySelectorAll('.msg.assistant').length >= 2",
        timeout=30000)
    page.close()

 succeeded in 996ms:
357 tests/test_web_e2e.py
     1	"""Web channel: API-surface tests plus the mandatory headless-browser
     2	end-to-end tests asserting against the DOM. Fully offline: the app under
     3	test talks to a stub PizzaSim and a stub (scripted) gateway on localhost.
     4	The customer never talks to curl — and neither do these assertions."""
     5	from __future__ import annotations
     6	
     7	import json
     8	import os
     9	
    10	import httpx
    11	import pytest
    12	
    13	from tests.stubs import StubGateway, StubPizzaSim, run_server
    14	
    15	PZ1 = "11111111-aaaa-bbbb-cccc-000000000001"
    16	PZ2 = "22222222-aaaa-bbbb-cccc-000000000002"
    17	PZ2_ENTRY = {"id": PZ2, "name": "Stub Pizzeria Due"}
    18	
    19	
    20	@pytest.fixture(scope="module")
    21	def stack():
    22	    """Stub PizzaSim + stub gateway + the real app, all on localhost."""
    23	    pizzasim = StubPizzaSim()
    24	    gateway = StubGateway()
    25	    ps_server, ps_url = run_server(pizzasim.app)
    26	    gw_server, gw_url = run_server(gateway.app)
    27	    os.environ.update({
    28	        "PIZZASIM_URL": ps_url,
    29	        "PIZZASIM_API_KEY": "stub-key",
    30	        "PIZZERIA_ID": PZ1,
    31	        "PIZZERIA_LANG": "de",
    32	        "LITELLM_PIZZA_URL": gw_url,
    33	        "LITELLM_PIZZA_KEY": "stub-key",
    34	        "LITELLM_PIZZA_MODEL_1": "scripted-stub",
    35	        "APP_VERSION": "2.0.0",
    36	    })
    37	    for var in ("SPEECH_URL", "SPEECH_STT_MODEL", "SPEECH_TTS_MODEL",
    38	                "SPEECH_TTS_VOICE", "LITELLM_PIZZA_MODEL_2"):
    39	        os.environ.pop(var, None)
    40	    from channels import web  # app boots against the stub env
    41	    app_server, app_url = run_server(web.app)
    42	    yield {"pizzasim": pizzasim, "gateway": gateway, "url": app_url,
    43	           "web": web, "ps_url": ps_url}
    44	    for server in (app_server, ps_server, gw_server):
    45	        server.should_exit = True
    46	
    47	
    48	def stream_lines(client, path, body):
    49	    with client.stream("POST", path, json=body) as response:
    50	        response.raise_for_status()
    51	        return [json.loads(line) for line in response.iter_lines()
    52	                if line.strip()]
    53	
    54	
    55	@pytest.fixture()
    56	def api(stack):
    57	    with httpx.Client(base_url=stack["url"], timeout=30.0) as client:
    58	        yield client
    59	
    60	
    61	# --- API surface (ordering matters: health-unknown runs first) ------------
    62	
    63	def test_health_gateway_unknown_before_first_turn(api):
    64	    health = api.get("/health").json()
    65	    assert health == {"api": "ok", "gateway": "unknown"}
    66	
    67	
    68	def test_config_contract(stack, api):
    69	    cfg = api.get("/config").json()
    70	    assert cfg["version"] == "2.0.0"
    71	    assert cfg["speech"] is False
    72	    assert cfg["lang_default"] == "de"
    73	    assert [p["id"] for p in cfg["pizzerias"]] == [PZ1, PZ2]
    74	    assert cfg["preselected_id"] == PZ1
    75	    assert cfg["dashboard_base"] == f"{stack['ps_url']}/dashboard/pizzerias"
    76	    assert cfg["docs_url"] == f"{stack['ps_url']}/swagger.html"
    77	
    78	
    79	def test_config_list_unavailable_no_fallback(stack, api):
    80	    stack["pizzasim"].fail_pizzerias = True
    81	    try:
    82	        cfg = api.get("/config").json()
    83	        assert cfg["pizzerias"] is None  # never a bundled fallback list
    84	        assert api.get("/health").json()["api"] == "down"
    85	    finally:
    86	        stack["pizzasim"].fail_pizzerias = False
    87	
    88	
    89	def test_session_and_greeting_then_gateway_ok(api):
    90	    created = api.post("/session", json={}).json()
    91	    assert created["pizzeria_id"] == PZ1
    92	    assert created["pizzeria_name"] == "Stub Pizzeria Uno"
    93	    events = stream_lines(api, "/chat",
    94	                          {"session_id": created["session_id"],
    95	                           "text": None})
    96	    kinds = [e["type"] for e in events]
    97	    assert "assistant" in kinds and kinds[-1] == "done"
    98	    assert api.get("/health").json()["gateway"] == "ok"
    99	
   100	
   101	def test_session_unknown_pizzeria_409(api):
   102	    response = api.post("/session", json={"pizzeria_id": "no-such-id"})
   103	    assert response.status_code == 409
   104	
   105	
   106	def test_chat_unknown_session_404(api):
   107	    assert api.post("/chat", json={"session_id": "ghost",
   108	                                   "text": "hi"}).status_code == 404
   109	
   110	
   111	def test_turn_in_flight_409(stack, api):
   112	    sid = api.post("/session", json={}).json()["session_id"]
   113	    lock = stack["web"].app.state.locks[sid]
   114	    assert lock.acquire(blocking=False)
   115	    try:
   116	        response = api.post("/chat", json={"session_id": sid, "text": "x"})
   117	        assert response.status_code == 409
   118	    finally:
   119	        lock.release()
   120	
   121	
   122	def test_language_switch(api):
   123	    sid = api.post("/session", json={}).json()["session_id"]
   124	    assert api.post("/language",
   125	                    json={"session_id": sid,
   126	                          "lang": "en"}).json() == {"lang": "en"}
   127	    assert api.post("/language",
   128	                    json={"session_id": sid,
   129	                          "lang": "xx"}).status_code == 422
   130	
   131	
   132	def test_tool_error_surfaces_as_rendered_answer(api):
   133	    """The 422-shaped tool error reaches the customer as model-phrased
   134	    plain language in the stream, never as a code."""
   135	    sid = api.post("/session", json={}).json()["session_id"]
   136	    stream_lines(api, "/chat", {"session_id": sid, "text": None})
   137	    events = stream_lines(api, "/chat",
   138	                          {"session_id": sid,
   139	                           "text": "Einmal Bolognese bitte"})
   140	    errors = [e for e in events if e["type"] == "tool_result"
   141	              and "error" in e["result"]]
   142	    assert errors and errors[0]["result"]["error"]["code"] == "unknown_item"
   143	    final = [e for e in events if e["type"] == "assistant"][-1]
   144	    assert "nicht im Angebot" in final["text"]
   145	    assert "unknown_item" not in final["text"]
   146	
   147	
   148	def test_confirm_endpoint_places_order_in_selected_tenant(stack, api):
   149	    created = api.post("/session", json={"pizzeria_id": PZ2}).json()
   150	    sid = created["session_id"]
   151	    stream_lines(api, "/chat", {"session_id": sid, "text": None})
   152	    stream_lines(api, "/chat", {"session_id": sid,
   153	                                "text": "Zwei Margherita bitte"})
   154	    events = stream_lines(api, "/chat", {"session_id": sid,
   155	                                         "text": "Ich heiße Eva"})
   156	    snapshot = [e["result"]["snapshot"] for e in events
   157	                if e["type"] == "tool_result"
   158	                and e.get("tool") == "read_back"][-1]
   159	    events = stream_lines(api, "/confirm",
   160	                          {"session_id": sid,
   161	                           "revision": snapshot["revision"]})
   162	    submitted = [e["result"] for e in events
   163	                 if e["type"] == "tool_result"
   164	                 and e.get("tool") == "submit_order"][-1]
   165	    assert submitted["order_id"]
   166	    # the order landed under the CHOSEN tenant, not the preselected one
   167	    assert stack["pizzasim"].orders.get(PZ2), "order missing in tenant"
   168	    assert not any(o["customer"]["first_name"] == "Eva"
   169	                   for o in stack["pizzasim"].orders.get(PZ1, []))
   170	    stored = stack["pizzasim"].orders[PZ2][-1]
   171	    assert stored["customer"]["first_name"] == "Eva"
   172	    assert stored["items"] == [{"type": "pizza", "code": "margherita",
   173	                                "qty": 2, "extras": []}]
   174	
   175	
   176	def test_confirm_stale_revision_streams_error(api):
   177	    created = api.post("/session", json={}).json()
   178	    sid = created["session_id"]
   179	    stream_lines(api, "/chat", {"session_id": sid,
   180	                                "text": "Zwei Margherita bitte"})
   181	    events = stream_lines(api, "/confirm",
   182	                          {"session_id": sid, "revision": 99})
   183	    errors = [e["result"]["error"]["code"] for e in events
   184	              if e["type"] == "tool_result" and "error" in e["result"]]
   185	    assert errors  # refused by the state machine, streamed to the UI
   186	    assert events[-1]["state"]["state"] != "SUBMITTED"
   187	
   188	
   189	# --- browser end-to-end (Playwright, DOM assertions) ----------------------
   190	
   191	@pytest.fixture(scope="module")
   192	def page_factory(stack):
   193	    from playwright.sync_api import sync_playwright
   194	    with sync_playwright() as p:
   195	        browser = p.chromium.launch()
   196	        yield lambda: browser.new_page()
   197	        browser.close()
   198	
   199	
   200	def open_app(page_factory, stack):
   201	    page = page_factory()
   202	    page.goto(stack["url"], timeout=30000)
   203	    page.wait_for_selector(".msg.assistant", timeout=30000)
   204	    return page
   205	
   206	
   207	def test_e2e_full_order_with_header_footer_contract(page_factory, stack):
   208	    stack["gateway"].mode = "ok"
   209	    page = open_app(page_factory, stack)
   210	
   211	    # header contract
   212	    assert page.locator("#pizzeria-name").inner_text() == \
   213	        "Stub Pizzeria Uno"
   214	    first_option = page.locator("#pizzeria-select option").first
   215	    assert "Stub Pizzeria Uno (11111111)" == first_option.inner_text()
   216	    dash = page.locator("#dashboard-link")
   217	    assert dash.get_attribute("href").endswith(
   218	        f"/dashboard/pizzerias/{PZ1}")
   219	    assert dash.get_attribute("target") == "_blank"
   220	    # footer contract
   221	    assert page.locator("#version").inner_text() == "v2.0.0"
   222	    assert page.locator("#uuid").inner_text() == PZ1
   223	    assert page.locator("#docs-link").get_attribute("href").endswith(
   224	        "/swagger.html")
   225	    page.wait_for_selector("#health-api.ok", timeout=15000)
   226	    page.wait_for_selector("#health-gateway.ok", timeout=15000)
   227	    # speech disabled → controls not rendered
   228	    assert page.locator("#mic").is_hidden()
   229	    assert page.locator("#tts-wrap").is_hidden()
   230	
   231	    def say(text):
   232	        page.fill("#text", text)
   233	        page.click("#send")
   234	
   235	    say("Was kostet eine Margherita?")
   236	    page.wait_for_selector("text=8.5 €", timeout=30000)
   237	
   238	    say("Zwei Margherita bitte")
   239	    page.wait_for_selector("#basket-lines li", timeout=30000)
   240	    assert "2× Margherita" in page.locator("#basket-lines").inner_text()
   241	    assert "17,00 €" in page.locator("#basket-total").inner_text()
   242	
   243	    say("Ich heiße Eva")
   244	    page.wait_for_selector(".readback button:enabled", timeout=30000)
   245	    readback = page.locator(".readback").last
   246	    assert "17,00 €" in readback.inner_text()
   247	
   248	    page.locator(".readback button:enabled").click()
   249	    page.wait_for_selector("#submitted-banner:not([hidden])",
   250	                           timeout=30000)
   251	    banner = page.locator("#submitted-banner").inner_text()
   252	    order_id = banner.split()[-1]
   253	    assert len(order_id) == 36  # a real order id, visible to the customer
   254	    assert page.locator("#basket.locked").count() == 1
   255	    assert page.locator(".readback button").last.is_disabled()
   256	    assert page.locator("details.steps").count() >= 3  # steps rendered
   257	    page.close()
   258	
   259	
   260	def test_e2e_pizzeria_switch_and_language(page_factory, stack):
   261	    stack["gateway"].mode = "ok"
   262	    page = open_app(page_factory, stack)
   263	    page.fill("#text", "Zwei Margherita bitte")
   264	    page.click("#send")
   265	    page.wait_for_selector("#basket-lines li", timeout=30000)
   266	
   267	    page.select_option("#pizzeria-select", PZ2)
   268	    page.wait_for_function(
   269	        "document.getElementById('pizzeria-name').textContent === "
   270	        "'Stub Pizzeria Due'", timeout=30000)
   271	    assert page.locator("#uuid").inner_text() == PZ2
   272	    assert page.locator("#basket-lines li").count() == 0  # basket cleared
   273	    page.wait_for_selector(".msg.assistant", timeout=30000)  # fresh greet
   274	
   275	    page.locator("#lang-switch button[data-lang=en]").click()
   276	    page.wait_for_function(
   277	        "document.getElementById('start-over').textContent === "
   278	        "'Start over'", timeout=15000)  # chrome follows the declared lang
   279	    page.close()
   280	
   281	
   282	def test_e2e_vanished_pizzeria_refreshes_selector(page_factory, stack):
   283	    stack["gateway"].mode = "ok"
   284	    page = open_app(page_factory, stack)
   285	    page.fill("#text", "Zwei Margherita bitte")
   286	    page.click("#send")
   287	    page.wait_for_selector("#basket-lines li", timeout=30000)
   288	    stack["pizzasim"].pizzerias = [p for p in stack["pizzasim"].pizzerias
   289	                                   if p["id"] != PZ2]
   290	    try:
   291	        page.select_option("#pizzeria-select", PZ2)
   292	        page.wait_for_selector(".notice", timeout=30000)
   293	        page.wait_for_function(
   294	            "document.querySelectorAll('#pizzeria-select option')"
   295	            ".length === 1", timeout=15000)
   296	        # the failed switch must NOT hide the still-live order
   297	        assert page.locator("#basket-lines li").count() == 1
   298	        assert page.locator(".msg.user").count() == 1
   299	    finally:
   300	        stack["pizzasim"].pizzerias.append(PZ2_ENTRY)
   301	    page.close()
   302	
   303	
   304	def test_e2e_lost_session_recreates_and_offers_resend(page_factory,
   305	                                                      stack):
   306	    """Server no longer knows the session (e.g. restart): the customer
   307	    sees a plain notice, gets a fresh session, and can resend."""
   308	    stack["gateway"].mode = "ok"
   309	    page = open_app(page_factory, stack)
   310	    stack["web"].app.state.sessions.clear()  # simulate a lost session
   311	    page.fill("#text", "Was kostet eine Margherita?")
   312	    page.click("#send")
   313	    page.wait_for_selector(".notice button", timeout=30000)  # resend
   314	    page.locator(".notice button").last.click()
   315	    page.wait_for_selector("text=8.5 €", timeout=30000)
   316	    page.close()
   317	
   318	
   319	def test_e2e_tool_error_leaves_visible_message(page_factory, stack):
   320	    stack["gateway"].mode = "ok"
   321	    page = open_app(page_factory, stack)
   322	    page.fill("#text", "Einmal Bolognese bitte")
   323	    page.click("#send")
   324	    page.wait_for_selector("text=nicht im Angebot", timeout=30000)
   325	    page.close()
   326	
   327	
   328	def test_e2e_gateway_unreachable_leaves_visible_message(page_factory,
   329	                                                        stack):
   330	    stack["gateway"].mode = "ok"
   331	    page = open_app(page_factory, stack)
   332	    stack["gateway"].mode = "http500"
   333	    try:
   334	        page.fill("#text", "Hallo?")
   335	        page.click("#send")
   336	        # the retry-once path ends in a rendered apology — an answer
   337	        page.wait_for_selector("text=schiefgegangen", timeout=30000)
   338	    finally:
   339	        stack["gateway"].mode = "ok"
   340	    page.close()
   341	
   342	
   343	def test_e2e_stream_without_answer_offers_resend(page_factory, stack):
   344	    stack["gateway"].mode = "ok"
   345	    page = open_app(page_factory, stack)
   346	    stack["gateway"].mode = "empty"
   347	    try:
   348	        page.fill("#text", "Hallo?")
   349	        page.click("#send")
   350	        page.wait_for_selector(".notice button", timeout=30000)
   351	    finally:
   352	        stack["gateway"].mode = "ok"
   353	    page.locator(".notice button").last.click()  # resend, now answered
   354	    page.wait_for_function(
   355	        "document.querySelectorAll('.msg.assistant').length >= 2",
   356	        timeout=30000)
   357	    page.close()

 succeeded in 1420ms:
  entire point of the product.
- **Language: German or English**, switchable, applied to the agent's replies
  and to speech in both directions.
- **Start over**, clearing the session and the basket.

### Footer

- **The running version**, `x.y.z`, from `APP_VERSION`, raised on every
  release: patch for fixes, minor for new behaviour, major for a break.
  Without it nobody can tell which build is answering.
- **The full pizzeria UUID**, selectable, for pasting into API calls.
- **Connection state** for the ordering API and the model gateway.
- **A link to the API documentation** (`{PIZZASIM_URL}/swagger.html`).

### Every message gets an answer

The invariant this channel stands on: **no sent message may end without either
a rendered assistant reply or a rendered error.** Never a silent failure,
never an indicator that stops with nothing after it.

- The moment a message is sent, the UI shows the agent is working.
- Intermediate steps render as they stream — which tool was called and what it
  returned — visually distinct from the assistant's words. A stream whose tool
  events the page discards is a defect: the customer sees a frozen screen
  while the agent works normally.
- If the stream ends without a final assistant message, the UI says so.
- If the request errors, times out, or the connection drops, the UI says which
  happened and offers to resend.
- Errors in the customer's language, in plain words. No status codes, no
  tracebacks, no raw JSON.

### The order on screen

- The current basket is visible, with quantities and what it comes to. The
  code owns the order; the customer must see what the code holds.
- The read-back is visually distinct and carries an explicit confirm control.
  Confirmation is an action the customer takes, not a word the agent claims to
  have heard.
- On success: the order id, readable, and the wait in minutes.
- After submission the basket is locked and shown as submitted. Nothing on the
  page can modify or resubmit it.

---

## Speech

Speech is an input and an output method on the web channel, served by a
**self-hosted speech service**: CPU-only, in its own container, reached over
plain HTTP with an OpenAI-compatible surface.

| Direction | Endpoint | Payload |
|---|---|---|
| STT | `POST {SPEECH_URL}/v1/audio/transcriptions` | multipart audio + model + language |
| TTS | `POST {SPEECH_URL}/v1/audio/speech` | JSON: model, voice, input text → audio |

- **The speech service is the only speech path.** No external speech
  provider, no hosted realtime framework, no audio through the LLM gateway —
  that gateway carries chat completions only.
- **The browser captures and plays audio; it does not recognise or synthesise
  it.** Capture via `getUserMedia` and `MediaRecorder`, playback via a plain
  audio element — cross-browser and cross-platform: Firefox, Safari, Chrome,
  on Linux, macOS and Windows alike.
- **The browser speech APIs are forbidden.** `SpeechRecognition` and
  `speechSynthesis` tied the previous implementation to a single browser
  vendor and sent customer audio to a third party. The self-hosted service
  exists to replace them.
- **Nothing about the speech stack is written into source.** Base URL, models
  and voice come from the environment, exactly like the chat model; the
  language sent with STT/TTS requests is the session language (see
  *Language authority* under Conversation policy), not a separate config.
- **Request/response, not streaming.** Record, upload, transcript back.
  Latency is visible and acceptable; do not build partial results, barge-in
  or turn detection on top — this transport cannot do them, and pretending
  otherwise produces a broken feel.
- **Push-to-talk.** The microphone starts and stops on the customer's action,
  never listens continuously. Recording state is visible at all times.
- **Synthesis is optional and off by default**, toggled by the customer,
  applied only to the final assistant message.
- **Speech is never required.** With `SPEECH_URL` unset or the service down,
  microphone and speaker toggle are not rendered and the text UI is fully
  usable. A speech failure is never an order failure.
- **Speech shortens answers, it does not change them.** Same core, same
  tools, same state machine. When a reply will be spoken: at most three menu
  items plus an invitation, times in minutes, order id read in groups.
- **Confirm the name.** Transcription errors on names are the expensive
  failure: a misheard name silently creates a customer nobody will find
  again. Read the name back before submitting.

---

## Error handling

Every case below needs a test and a phrasing.

| Situation | Code does | Customer sees/hears |
|---|---|---|
| Gateway timeout | one retry, then abort turn | plain apology, offer to resend |
| `401`/`403` from PizzaSim | abort, log, do not retry | "I can't reach the kitchen system right now" |
| `404` on the preselected `PIZZERIA_ID` | fail at startup, not mid-call | — (process refuses to start) |
| Runtime pizzeria selection invalid/gone | session error, refresh the selector; process stays up | "that pizzeria isn't available right now" |
| `422` validation | surface field, keep basket | targeted question about the offending item |
| `5xx` on submit | **no blind retry** | "I'm not sure that went through — let me check" |
| Timeout on submit | mark `UNKNOWN`; shortlist via `GET /pizzerias/{id}/orders`, verify items via `GET /pizzerias/{id}/orders/{order_id}` before any retry | as above |
| Unknown item code | `unknown_item` + candidates | "I have Margherita or Marinara — which one?" |
| Empty basket at submit | reject transition | "What can I get you?" |
| Menu fetch fails at start | fail fast | "We're not taking orders right now" |
| Pizzeria list fetch fails | no selector, say so | list unavailable — no fallback entry |
| Speech service down | hide speech controls | text UI unaffected |

The submit-timeout case is the one that matters: a blind retry doubles a real
order. Recovery: shortlist candidates on the pizzeria's order list, then
verify the candidate's items via `GET /pizzerias/{id}/orders/{order_id}` —
only a verified match is adopted, anything else allows exactly one retry. If
list or detail lookup fails, tell the customer honestly.

---

## Anti-patterns — explicitly forbidden

Each of these was present in a previous implementation. None is a matter of
taste.

 succeeded in 1365ms:
  control on the page can modify or resubmit (confirm button removed,
  input stays usable for a new conversation via Start over / new session).
- **Read-back panel:** on a `read_back` tool result: visually distinct
  block + confirm button bound to the streamed revision.
- **Answer invariant** ("no message ends unanswered"):
  - send → immediate "agent is working" indicator;
  - tool events render as they stream (collapsible steps, visually
    distinct) — never discarded (anti-pattern 6);
  - `done` without a preceding `assistant` event in the turn → rendered
    notice "the agent did not answer — resend?";
  - fetch error / abort / non-2xx → rendered notice naming which
    (error, timeout, connection lost) + a resend button that re-posts the
    same text;
  - all notices in plain words, in the **customer's language**, defined
    as follows.
- **Notice-language rule (explicit decision):** UI-generated text (chrome,
  notices, resend prompts) follows `session.lang` — the language the
  customer chose via the header switch, or the default before any choice.
  The UI performs **no language detection** (a heuristic would be a
  parser-shaped guess, and model replies already mirror per turn); the
  switch is the customer's declaration of their language toward the UI.
  Tested: switch to EN → subsequent notices render in English (E2E).

## CLI v2

Unchanged flow; read_back output now includes line totals and the basket
total from the snapshot (printing what core computed, no arithmetic).

## Error handling — new rows on top of v1's table

| Situation | Mechanism |
|---|---|
| Runtime pizzeria selection invalid | `create_session` NotFoundError → 409 → UI notice; process stays up |
| Pizzeria list fetch fails | `/config.pizzerias = null` → "list unavailable", no selector, no fallback entry |
| Stream ends without final message | UI-side detection via `done`-without-`assistant` → notice + resend |
| Gateway unreachable | existing retry-once → apology (now also an `assistant` event, v1 fix) + UI resend offer |
| Speech service down | probe fails → controls not rendered; per-call failure → notice, order untouched |

All other rows keep v1 mechanics — but v3 makes their **rendered outcome**
part of the web contract, so each customer-visible row gets web-surface
coverage, not only tool-level tests:

- `401/403` ("can't reach the kitchen system"), `422` submit_failed with
  the offending field, submit `5xx`/timeout (`submit_unknown` honest
  message), empty-basket submit ("What can I get you?"): each is asserted
  as a **rendered assistant message in the DOM or NDJSON stream** —
  tool-level errors reach the customer as model-phrased plain language
  (the model receives the speakable `message`), transport-level failures
  as UI notices. Coverage: golden transcripts (submit timeout), TestClient
  stream assertions (401/422/empty basket via stub PizzaSim), E2E
  (tool error + gateway down + cut stream).

## Testing

- **Unit/tool (extend v1's 71):** prices copied at add time; `line_total`
  / `basket_total` incl. Decimal rounding; snapshot shape; session factory
  (valid id, unknown id, list failure); `set_language` re-render;
  `confirm_and_submit` (happy, stale revision, submit timeout path);
  `APP_VERSION` validation.
- **Golden transcripts:** unchanged five; runner asserts extended snapshot
  keys where relevant.
- **Browser E2E (`tests/test_web_e2e.py`, offline, not optional):**
  in-process **stub PizzaSim** (fixtures: two pizzerias, menu with prices)
  and **stub gateway** (scripted tool-calling model) served locally;
  the app under test started on an ephemeral port with env pointing at the
  stubs; Playwright (chromium, headless) asserts against the DOM:
  1. full order: greeting → price question (price from menu rendered) →
     add items → name → read-back panel → **confirm click** → submitted
     lock + order id visible; basket totals correct at each step. The
     same scenario asserts the full header/footer contract in the DOM:
     pizzeria name in the header; selector entries "name + short UUID";
     dashboard link `href` ending `/dashboard/pizzerias/{selected id}`
     with `target="_blank"`; docs link `href` ending `/swagger.html`;
     footer showing `APP_VERSION` verbatim, the full selected UUID as
     selectable text, and the connection badges (gateway `unknown`
     before the first turn, `ok` after it; api `ok`);
  2. pizzeria switch: selector → fresh conversation, header + footer UUID
     change, basket cleared; language switch to EN → subsequent UI
     notices render in English;
  2b. vanished pizzeria: stub drops a pizzeria between page load and
     selection → 409 → notice + selector re-rendered from the fresh list;
  3. failure — tool error: unknown item → candidates visible in steps,
     answer rendered;
  4. failure — gateway unreachable: stub gateway refuses → apology text
     rendered + resend control;
  5. failure — stream ends without final message: stub cuts the stream →
     UI notice + resend control.
- **Live acceptance test:** as in v1, updated to SPEC wording (presence
  via list, customer/items/qty via detail endpoint). Opt-in
  `PIZZA_LIVE_TEST=1`.
- **Speech:** manual checklist (README) unchanged + STT language follows
  the session language.

## Deliverables delta vs repo

New: `channels/speech.py`, `tests/test_web_e2e.py`. Rebuilt:
`channels/web.py`, `channels/static/*`. Extended: `core/menu.py`,
`core/order.py`, `core/tools.py`, `core/agent.py`, prompts (prices,
verbatim-price rule), `README.md`, `.env.example` (+`APP_VERSION`),

exec
/bin/bash -lc 'rg -n "unit_price|basket_total|APP_VERSION|TimeoutError|speech|confirm_and_submit|read_back_required|submit_unknown|dashboard|swagger" tests/test_tools.py tests/test_transcripts.py tests/test_state.py -S' in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "rg --files prompts && sed -n '1,220p' prompts/system.de.md && printf '\\n---\\n' && sed -n '1,220p' prompts/system.en.md" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 297ms:
tests/test_tools.py:142:def test_unit_price_copied_at_add_time_and_totals_computed(menu):
tests/test_tools.py:152:    assert line["unit_price"] == 8.5
tests/test_tools.py:154:    assert snap["basket_total"] == 34.5  # 3*8.5 + 9.0
tests/test_tools.py:161:    order.items.append(Item("pizza", "x", "X", 3, [], unit_price=0.1))
tests/test_tools.py:164:    assert snap["basket_total"] == 0.3
tests/test_tools.py:316:    assert result["error"]["code"] == "submit_unknown"
tests/test_tools.py:317:    assert order.state is State.CONFIRMED and order.submit_unknown
tests/test_tools.py:364:    assert order.submit_unknown
tests/test_tools.py:369:    assert not order.submit_unknown
tests/test_tools.py:389:    assert result["error"]["code"] == "submit_unknown"
tests/test_tools.py:400:def test_submit_unknown_when_list_unavailable(menu, fake):
tests/test_tools.py:406:    assert result["error"]["code"] == "submit_unknown"
tests/test_tools.py:425:    assert not order.submit_unknown  # not the retry path
tests/test_tools.py:575:def test_confirm_and_submit_happy_path():
tests/test_tools.py:580:    text = agent.confirm_and_submit(session, session.order.revision,
tests/test_tools.py:601:    agent.confirm_and_submit(session, stale, events.append)
tests/test_tools.py:618:    text = agent.confirm_and_submit(session, session.order.revision,
tests/test_state.py:166:    assert e.value.code == "read_back_required"
tests/test_state.py:185:    assert e.value.code == "read_back_required"

 succeeded in 307ms:
prompts/system.de.md
prompts/system.en.md
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
- Preisfragen sind normale Fragen. Nenne Preise und die Korbsumme wörtlich
  aus den Werkzeug-Ergebnissen (`price`, `basket_total`) — du rechnest nie
  selbst und erfindest keine Beträge.
- Wenn deine Antwort vorgelesen wird: höchstens drei Gerichte nennen und
  zum Nachfragen einladen, Zeiten in Minuten, kurze Sätze.

Wenn ein Werkzeug einen Fehler meldet, richte dich danach: schlage die
genannten Alternativen vor oder stelle die fehlende Frage. Das System hat
immer recht.

---
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
- Price questions are normal questions. Quote prices and the basket total
  verbatim from tool results (`price`, `basket_total`) — never do the
  arithmetic yourself, never invent an amount.
- When your reply will be spoken aloud: at most three dishes plus an
  invitation to ask for more, times in minutes, short sentences.

When a tool reports an error, follow it: offer the suggested alternatives
or ask the missing question. The system is always right.

exec
/bin/bash -lc "rg -n \"TimeoutError|errTimeout|STREAM_TIMEOUT_MS|timed out|request timed out|offer to resend|sessionLost|confirmOrder\\(|streamPost\\(\" channels/static/app.js tests -S" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 0ms:
channels/static/app.js:16:    errTimeout: "Zeitüberschreitung.",
channels/static/app.js:35:    sessionLost: "Die Sitzung ist verloren gegangen — neue Sitzung " +
channels/static/app.js:43:    errTimeout: "The request timed out.",
channels/static/app.js:62:    sessionLost: "The session was lost — a new one was started.",
channels/static/app.js:174:  btn.onclick = () => { btn.disabled = true; confirmOrder(snapshot.revision); };
channels/static/app.js:230:const STREAM_TIMEOUT_MS = 120000;
channels/static/app.js:232:async function streamPost(path, body, resendText) {
channels/static/app.js:237:    [currentAbort.signal, AbortSignal.timeout(STREAM_TIMEOUT_MS)]);
channels/static/app.js:256:      notice(t("sessionLost"), resendText);
channels/static/app.js:267:    else if (err.name === "TimeoutError") notice(t("errTimeout"), resendText);
channels/static/app.js:278:  const finalText = await streamPost(
channels/static/app.js:283:async function confirmOrder(revision) {
channels/static/app.js:284:  const finalText = await streamPost(
tests/test_transcripts.py:128:        raise GatewayError("gateway timed out twice")
tests/test_tools.py:534:        raise GatewayError("gateway timed out twice")

exec
/bin/bash -lc "nl -ba channels/static/app.js | sed -n '228,292p'" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 0ms:
   228	}
   229	
   230	const STREAM_TIMEOUT_MS = 120000;
   231	
   232	async function streamPost(path, body, resendText) {
   233	  currentAbort = new AbortController();
   234	  // Real client-side timeout: covers the request AND the streamed body,
   235	  // so the timeout notice + resend control can actually occur.
   236	  const signal = AbortSignal.any(
   237	    [currentAbort.signal, AbortSignal.timeout(STREAM_TIMEOUT_MS)]);
   238	  const working = document.createElement("div");
   239	  working.className = "working";
   240	  working.textContent = t("working");
   241	  chat.appendChild(working);
   242	  $("send").disabled = true;
   243	  let finalText = "";
   244	  try {
   245	    const res = await fetch(path, {
   246	      method: "POST",
   247	      headers: { "Content-Type": "application/json" },
   248	      body: JSON.stringify(body),
   249	      signal,
   250	    });
   251	    if (res.status === 404) {
   252	      // The server no longer knows this session: recreate transparently,
   253	      // keep the customer's message recoverable via resend.
   254	      working.remove();
   255	      await startSession(session.pizzeriaId);
   256	      notice(t("sessionLost"), resendText);
   257	      $("send").disabled = false;
   258	      return "";
   259	    }
   260	    if (res.status === 409) { working.remove(); notice(t("busy")); return ""; }
   261	    if (!res.ok) throw new Error("http");
   262	    working.remove();
   263	    finalText = await readStream(res, resendText);
   264	  } catch (err) {
   265	    working.remove();
   266	    if (err.name === "AbortError") { /* deliberate: switch/start-over */ }
   267	    else if (err.name === "TimeoutError") notice(t("errTimeout"), resendText);
   268	    else if (err.message === "http") notice(t("errHttp"), resendText);
   269	    else notice(t("errNetwork"), resendText);
   270	  }
   271	  $("send").disabled = false;
   272	  $("text").focus();
   273	  return finalText;
   274	}
   275	
   276	async function sendTurn(text, spoken = false) {
   277	  if (text !== null) addMsg("user", text);
   278	  const finalText = await streamPost(
   279	    "/chat", { session_id: session.id, text, spoken }, text ?? undefined);
   280	  if (finalText && cfg.speech && $("tts-toggle").checked) speak(finalText);
   281	}
   282	
   283	async function confirmOrder(revision) {
   284	  const finalText = await streamPost(
   285	    "/confirm", { session_id: session.id, revision });
   286	  if (finalText && cfg.speech && $("tts-toggle").checked) speak(finalText);
   287	}
   288	
   289	/* ---------- sessions / tenancy ----------------------------------------- */
   290	
   291	function fillSelector() {
   292	  const select = $("pizzeria-select");

codex
Findings:

- Important: [channels/static/app.js](/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js:251) still leaves the `/confirm` recovery path short of the stated/spec-required resend behavior. `streamPost()` only renders a resend control when `resendText` is defined, but [confirmOrder()](/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js:283) calls it without any recovery payload. Result: a lost session, timeout, or other transport failure during `/confirm` shows only a notice, with no way to retry the confirm action from the UI. That means round-1 fix #2 is only fully implemented for `/chat`, not `/confirm`, and the web-channel “request errors … offers to resend” rule is still unmet for confirm requests. The current browser regression also only covers the `/chat` case in [tests/test_web_e2e.py](/home/rob/bpm-pizza-vibecoding-solution/tests/test_web_e2e.py:304).

I verified the other claimed round-1 repairs in the files: the spoken note is ephemeral per turn in [core/agent.py](/home/rob/bpm-pizza-vibecoding-solution/core/agent.py:195), the client-side timeout is real and wraps the streamed body in [channels/static/app.js](/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js:232), and failed pizzeria switches preserve the live chat/basket in [channels/static/app.js](/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js:321). Core/session ownership, confirm-and-submit symmetry, tenant scoping, prices/totals in core, and the main web contract are otherwise implemented coherently and align well with `SPEC.md` and `PLAN.md`.

SCORES (1-5 each, 5 = best):
completeness: 4
correctness: 4
error_handling: 3
simplicity: 4
spec_compliance: 3
TOTAL: 18/25
VERDICT: CHANGES_REQUIRED
ISSUES: (max 5 bullets, concrete and actionable, empty if approved)
- Add a real resend/retry path for `/confirm` failures in the UI: preserve the pending confirm action (at least the `revision`, or auto-reissue `/confirm` after session recreation where valid), render a resend control on `404`/timeout/non-2xx just as `/chat` does, and add a browser regression that exercises lost-session or timeout during confirm.
tokens used
72,679
Findings:

- Important: [channels/static/app.js](/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js:251) still leaves the `/confirm` recovery path short of the stated/spec-required resend behavior. `streamPost()` only renders a resend control when `resendText` is defined, but [confirmOrder()](/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js:283) calls it without any recovery payload. Result: a lost session, timeout, or other transport failure during `/confirm` shows only a notice, with no way to retry the confirm action from the UI. That means round-1 fix #2 is only fully implemented for `/chat`, not `/confirm`, and the web-channel “request errors … offers to resend” rule is still unmet for confirm requests. The current browser regression also only covers the `/chat` case in [tests/test_web_e2e.py](/home/rob/bpm-pizza-vibecoding-solution/tests/test_web_e2e.py:304).

I verified the other claimed round-1 repairs in the files: the spoken note is ephemeral per turn in [core/agent.py](/home/rob/bpm-pizza-vibecoding-solution/core/agent.py:195), the client-side timeout is real and wraps the streamed body in [channels/static/app.js](/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js:232), and failed pizzeria switches preserve the live chat/basket in [channels/static/app.js](/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js:321). Core/session ownership, confirm-and-submit symmetry, tenant scoping, prices/totals in core, and the main web contract are otherwise implemented coherently and align well with `SPEC.md` and `PLAN.md`.

SCORES (1-5 each, 5 = best):
completeness: 4
correctness: 4
error_handling: 3
simplicity: 4
spec_compliance: 3
TOTAL: 18/25
VERDICT: CHANGES_REQUIRED
ISSUES: (max 5 bullets, concrete and actionable, empty if approved)
- Add a real resend/retry path for `/confirm` failures in the UI: preserve the pending confirm action (at least the `revision`, or auto-reissue `/confirm` after session recreation where valid), render a resend control on `404`/timeout/non-2xx just as `/chat` does, and add a browser regression that exercises lost-session or timeout during confirm.
