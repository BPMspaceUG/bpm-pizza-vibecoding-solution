Reading prompt from stdin...
OpenAI Codex v0.143.0
--------
workdir: /home/rob/bpm-pizza-vibecoding-solution
model: gpt-5.4
provider: openai
approval: never
sandbox: workspace-write [workdir, /tmp, $TMPDIR] (network access enabled)
reasoning effort: medium
reasoning summaries: none
session id: 019fc104-1ed5-7061-86cf-818e234be902
--------
user
## Context

SPEC.md now contains two post-v1.0.0 extensions, both Codex-discussed and committed: returning-customer street reuse (confirm-without-disclosure, commit 7b5376b) and voice as a required release capability (commit d851966). The operator ordered implementation via the established pipeline. PLAN.md gained a "Delta Plan v3" section (commit d51bb93) covering both. This issue is the plan gate; SPEC stage order is binding: no implementation before APPROVED.

## Judge request

You are the devil's advocate and judge for the PLAN stage. In the workspace (committed tree), read: the "Delta Plan v3" section at the end of PLAN.md (the artifact under review; Plan v2 above it is already approved and implemented), SPEC.md (source of truth — especially the contract facts on the customers endpoint, the Tools table rows for lookup_customer/set_customer/read_back, the saved-street redaction convention, the Speech + Speech service provisioning sections, the Testing additions, and acceptance point 5), decisions/qa.md (street-lookup and voice decisions), and the existing core/, channels/, tests/ the delta builds on.

Attack the delta plan: spec coverage gaps (redaction guarantees end to end incl. submit body vs snapshot/logs, mutual exclusivity, deleted customers, non-fatal lookup failure, secure-context requirement, offline wiring vs live proof split, single final-message TTS, name-confirmation regression), contradictions with the approved v2 implementation it extends, and any underspecification an implementer could exploit.

Score against the fixed SPEC rubric and end your reply with exactly:

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
Reviewing the plan gate against the committed tree first. I’m loading the required skill instructions, then I’ll read the referenced spec, decisions, and relevant implementation surfaces before scoring the delta plan.
exec
/bin/bash -lc "sed -n '1,220p' /home/rob/.agents/skills/using-superpowers/SKILL.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' SPEC.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' PLAN.md" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 242ms:
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
5. With speech configured in the target deployment, a spoken conversation
   on the web channel can produce the same verified order outcome as
   points 1–4.

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
- **Speech on the web transport is a required channel capability in
  production.** It is provisioned via the self-hosted speech service
  described in *Speech*; if the service is unavailable at runtime,
  ordering degrades to text-only without breaking ordering.
- **Several pizzerias.** The customer chooses which one they are ordering
  from, and can change it. `PIZZERIA_ID` is the preselection, not a
  restriction.
- **Returning customers.** A known first name can reuse its saved street
  after an explicit confirmation — limited to address reuse via the
  PizzaSim customer data; broader cross-session memory ("the usual")
  stays deferred.
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
| `SPEECH_URL` | Base URL of the self-hosted speech service; required in production releases, optional only for local/dev and explicit text-only test scenarios |
| `SPEECH_STT_MODEL` | Transcription model id |
| `SPEECH_TTS_MODEL` | Synthesis model id |
| `SPEECH_TTS_VOICE` | Voice id |

Rules:

- **Nothing is hardcoded.** No UUID, no model name, no menu, no base URL, no
  vendor — not even as a fallback "just in case".
- Missing or empty required variable → exit before the first turn with a
  message naming the variable and the file it was expected in. Never start
  half-configured. For production completeness, `SPEECH_URL`,
  `SPEECH_STT_MODEL`, `SPEECH_TTS_MODEL` and `SPEECH_TTS_VOICE` are
  required. For local/dev and explicit degraded-mode tests they may be
  absent; in that case speech controls are not rendered and text ordering
  remains fully usable.
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
| `GET /pizzerias/{id}/customers` | `X-API-Key` | customer list — used **only** for address-reuse lookup, never to disclose address text |
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

 succeeded in 262ms:
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

 succeeded in 267ms:
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

exec
/bin/bash -lc "sed -n '1,260p' decisions/qa.md" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 108ms:
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

## 2026-08-01 — Street lookup for returning customers (SPEC change only)

**Q:** Operator: saved streets must be look-up-able. Discussed proposed
spec changes with Codex (reviews/round20-street-spec-discussion.md).

**A (decision):** Confirm-without-disclosure + code-side copy. New tool
`lookup_customer(first_name)` returns booleans only; `set_customer` gains
`use_saved_street: true` (mutually exclusive with `street_one`) and the
code copies the saved street — the text never reaches the model, stream,
transcript or logs (scoped: a street the customer dictated themselves may
be echoed). read_back does not recite reused streets. Reuse limited to
street_one until street_two on POST /orders is verified. SPEC.md updated
in 8 places per the Codex decision list; previous spec archived as
SPEC_20260801_3.md. No plan, no implementation yet (operator hold).

## 2026-08-01 — Spec Future: voice becomes first-class (SPEC change only)

**Q:** Operator: "a voice agent without voice is a bit stupid" — make voice
a DONE-relevant capability. Discussed with Codex
(reviews/round21-voice-spec-discussion.md).

**A (decision, 10 points applied):** Acceptance point 5 (spoken
conversation produces the same verified order); speech = required release
capability, text-only = degraded operation (release completeness vs.
runtime resilience separated — a speech outage never blocks typed
ordering); SPEECH_* required in production, optional in dev/test; secure
browser context (HTTPS/domain) mandatory for the voice path — plain HTTP
is not a valid acceptance environment; MediaRecorder-format in,
browser-playable audio out; latency = turn-taking fitness, sustained
multi-second delays are a defect; new "Speech service provisioning"
subsection (co-deployed, neutral definition under deploy/); testing:
offline speech E2E via stub service (wiring only), opt-in live voice
acceptance test with DE+EN audio fixtures as the release-gating proof
(manual demo is a release-note aid only), name-confirmation regression
against ghost customers; deliverables + locked-decision row added;
telephony stays deferred. No plan, no implementation (operator hold).

codex
Using `using-superpowers` to enforce the skill workflow, then I’m checking the Codex-specific tool notes and the exact plan/spec sections the verdict depends on. After that I’ll compare the delta against the committed implementation it extends.
exec
/bin/bash -lc "sed -n '1,220p' /home/rob/.agents/skills/using-superpowers/references/codex-tools.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc 'rg --files core channels tests' in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc 'rg -n "Delta Plan v3|customers endpoint|lookup_customer|set_customer|read_back|saved street|Speech|Speech service provisioning|Testing|acceptance point 5|secure context|spoken conversation|single final|final assistant|saved_street|redact|street_one|use_saved_street" PLAN.md SPEC.md decisions/qa.md' in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 182ms:
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

 succeeded in 236ms:
core/state.py
channels/speech.py
channels/__init__.py
channels/web.py
channels/cli.py
core/menu.py
core/__init__.py
core/agent.py
core/pizzasim.py
core/order.py
core/tools.py
channels/static/index.html
channels/static/style.css
channels/static/app.js
tests/test_state.py
tests/test_transcripts.py
tests/test_web_e2e.py
tests/__init__.py
tests/stubs.py
tests/test_tools.py
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

 succeeded in 231ms:
PLAN.md:106:- `read_back` carries the snapshot and therefore the canonical total; the
PLAN.md:120:  unit_price, line_total}], basket_total, customer, read_back_done}`
PLAN.md:126:- `read_back` results stream to the UI (they already do); the UI renders a
PLAN.md:196:- Speech proxy endpoints move to `channels/speech.py` (deliverable):
PLAN.md:197:  `SpeechService` class (config, probe, stt(audio, lang), tts(text,
PLAN.md:200:**Speech behaviour (full SPEC coverage, not just the STT hint):**
PLAN.md:234:- **Read-back panel:** on a `read_back` tool result: visually distinct
PLAN.md:257:Unchanged flow; read_back output now includes line totals and the basket
PLAN.md:268:| Speech service down | probe fails → controls not rendered; per-call failure → notice, order untouched |
PLAN.md:284:## Testing
PLAN.md:322:- **Speech:** manual checklist (README) unchanged + STT language follows
PLAN.md:373:# Delta Plan v3 — Street lookup + Voice (SPEC rev d851966)
PLAN.md:380:## A. Street lookup (SPEC: lookup_customer / use_saved_street / redaction)
PLAN.md:388:  Two serializations, one redaction rule:
PLAN.md:391:    `{"first_name", "street_one": null, "street_on_file": true}` — the
PLAN.md:395:    the real `street_one`. Submit uses saved `street_one` only — never
PLAN.md:398:  - New tool `lookup_customer` `{first_name}` →
PLAN.md:399:    `{"customer_exists": bool, "saved_street_available": bool, "snapshot"}`
PLAN.md:403:  - `set_customer` params become `{first_name, street_one?,
PLAN.md:404:    use_saved_street?}` — mutually exclusive; both set → error code
PLAN.md:406:    fetches the customer record in code, copies `street_one`, sets
PLAN.md:407:    `street_from_saved`; unknown name or no saved street → error
PLAN.md:408:    `no_saved_street` (speakable), basket untouched.
PLAN.md:410:- Prompts (both languages): after the name, call `lookup_customer`; if a
PLAN.md:411:  saved street exists ask exactly one confirmation question without
PLAN.md:412:  reciting the address; yes → `set_customer(use_saved_street: true)`;
PLAN.md:421:- `use_saved_street` copies in code; submit body carries the real street
PLAN.md:423:  contain no fragment of it (redaction asserted by string-scanning every
PLAN.md:425:- Mutual exclusion + `no_saved_street` paths.
PLAN.md:427:  question → flag-based set_customer → order) and decline/fallback
PLAN.md:439:  (secure context), co-deployment with the app, env wiring.
PLAN.md:445:- `tests/stubs.py`: `StubSpeech` — `GET /v1/models` 200;
PLAN.md:452:- API level (app booted with `SPEECH_*` pointing at StubSpeech):
PLAN.md:457:- Browser E2E (Playwright, localhost = secure context, fake media device
PLAN.md:464:  and only for the final assistant message (StubSpeech call counter);
PLAN.md:470:  happens and `set_customer` is called exactly once, with the corrected
PLAN.md:485:1. Street-lookup core (client, Customer redaction split, tools, unit
PLAN.md:486:   tests incl. redaction sweep). ☐ booleans-only lookup ☐ submit carries
PLAN.md:490:3. StubSpeech + audio fixtures + API-level speech tests. ☐ stt round
PLAN.md:493:   ☐ push-to-talk round trip ☐ single final-message TTS fetch.
decisions/qa.md:43:**Q:** Operator: saved streets must be look-up-able. Discussed proposed
decisions/qa.md:47:`lookup_customer(first_name)` returns booleans only; `set_customer` gains
decisions/qa.md:48:`use_saved_street: true` (mutually exclusive with `street_one`) and the
decisions/qa.md:49:code copies the saved street — the text never reaches the model, stream,
decisions/qa.md:51:be echoed). read_back does not recite reused streets. Reuse limited to
decisions/qa.md:52:street_one until street_two on POST /orders is verified. SPEC.md updated
decisions/qa.md:70:multi-second delays are a defect; new "Speech service provisioning"
SPEC.md:51:5. With speech configured in the target deployment, a spoken conversation
SPEC.md:126:- **Speech on the web transport is a required channel capability in
SPEC.md:128:  described in *Speech*; if the service is unavailable at runtime,
SPEC.md:133:- **Returning customers.** A known first name can reuse its saved street
SPEC.md:215:  "customer": { "first_name": "Marco", "street_one": "via di Cantieri" },
SPEC.md:233:  silently creates a new customer — a misheard name creates a ghost. Speech
SPEC.md:235:- `street_one` is optional and **not** validated for deliverability. Asking
SPEC.md:270:- **The customers endpoint** `GET /pizzerias/{id}/customers` (auth:
SPEC.md:271:  `X-API-Key`) returns `customers[]` with `{id, first_name, street_one,
SPEC.md:275:  `street_one`, so address reuse is limited to `street_one` until
SPEC.md:292:EMPTY ──add_items──▶ COLLECTING ──set_customer──▶ READY
SPEC.md:295:                                                    │ read_back + customer says yes
SPEC.md:309:   after `read_back` for the current basket revision. The basket carries a
SPEC.md:328:| `lookup_customer` | `first_name` | `{customer_exists, saved_street_available}` — booleans only, **no street text** |
SPEC.md:329:| `set_customer` | `first_name`, plus either `street_one` **or** `use_saved_street: true` (mutually exclusive) — with the flag, the **code** copies the saved street into the order; the text never passes through the model | customer as stored (saved street as a flag, not text) |
SPEC.md:330:| `read_back` | — | basket, customer name, revision, and the code-computed basket total — the text the agent reads out. A street reused from saved data is **not** recited; the earlier yes/no reuse confirmation covers it |
SPEC.md:347:  web basket shows the same code-owned total that `read_back` carries.
SPEC.md:352:- **Saved-street redaction.** A street reused from saved customer data
SPEC.md:383:- Collect the first name; then call `lookup_customer`. If a saved street
SPEC.md:386:  `set_customer(use_saved_street: true)`. If the customer declines, is
SPEC.md:390:- Before submitting: call `read_back`, present it, and wait for an explicit
SPEC.md:459:- If the stream ends without a final assistant message, the UI says so.
SPEC.md:478:## Speech
SPEC.md:480:Speech is an input and an output method on the web channel, served by a
SPEC.md:496:- **The browser speech APIs are forbidden.** `SpeechRecognition` and
SPEC.md:511:  applied only to the final assistant message.
SPEC.md:512:- **Speech is a required product capability for release completeness.**
SPEC.md:528:- **Speech shortens answers, it does not change them.** Same core, same
SPEC.md:535:### Speech service provisioning
SPEC.md:565:| Speech service down | hide speech controls | text UI unaffected |
SPEC.md:601:## Testing
SPEC.md:610:- **Address reuse:** tool-level tests for `lookup_customer`
SPEC.md:612:  `set_customer(use_saved_street: true)` copying in code; redaction tests
SPEC.md:613:  asserting no saved street text appears in tool results, streamed events,
SPEC.md:632:  and TTS fetched only for the final assistant message when the toggle is
SPEC.md:646:- **Speech, manual** (supplementary): dictate an order, a name that needs
SPEC.md:757:5. **Speech.** Wire the speech service into the web UI, spoken-answer policy,
SPEC.md:818:| Speech | Self-hosted container, OpenAI-compatible HTTP; no vendor, no browser speech API |

codex
I’ve got the delta section markers and the spec anchors. Next I’m reading the exact `Delta Plan v3` text and the current v2 implementation surfaces it would extend, looking for mismatches the plan leaves open.
exec
/bin/bash -lc "sed -n '478,646p' SPEC.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '373,520p' PLAN.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '260,420p' SPEC.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,320p' core/tools.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' core/order.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,320p' core/pizzasim.py" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 479ms:
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
- **Speech is a required product capability for release completeness.**
  Text-only is the degraded fallback when speech is unconfigured in
  dev/test or temporarily unavailable at runtime: microphone and speaker
  toggle are then not rendered and the text UI is fully usable, and a
  speech outage must never block typed ordering. But a production release
  without a working speech path is not done.
- **Voice-capable web deployments run in a secure browser context:**
  HTTPS on a real host/domain, or localhost during development. Plain
  HTTP is not a valid acceptance environment for microphone input
  (`getUserMedia` is unavailable there).
- **Transport formats:** the STT path accepts the browser-recorded audio
  format emitted by `MediaRecorder`; the TTS path returns audio playable
  by a standard browser audio element.
- **Latency:** each STT and each TTS request should complete quickly
  enough for turn-based conversation on demo hardware; sustained
  multi-second delays that make turn-taking awkward are a defect.
- **Speech shortens answers, it does not change them.** Same core, same
  tools, same state machine. When a reply will be spoken: at most three menu
  items plus an invitation, times in minutes, order id read in groups.
- **Confirm the name.** Transcription errors on names are the expensive
  failure: a misheard name silently creates a customer nobody will find
  again. Read the name back before submitting.

### Speech service provisioning

The deployment includes a self-hosted, CPU-only speech service reachable
at `SPEECH_URL`, exposing OpenAI-compatible
`POST /v1/audio/transcriptions` and `POST /v1/audio/speech`. The
application and the speech service are deployed together as first-party
artifacts. The repository includes a neutral deployment definition for
this service next to the app deployment artifacts (no vendor or model
names in source or spec — the operator configures them via the
environment, exactly like the chat model).

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

1. **A regex "fast path" that places an order without the model.** It bypasses
   confirmation, mis-parses quantities, duplicates items on overlapping
   matches, and makes the tool-calling architecture decorative.
2. **Shelling out to `curl` via `subprocess`.** Use an HTTP client: no shell
   quoting bugs, no injection surface, real timeouts, testable.
3. **Hardcoded pizzeria UUID or hardcoded menu fallback.** Both send orders to
   the wrong place while looking like they work. The same ban covers a
   fallback entry in the pizzeria selector.
4. **A system prompt that forbids confirmation** ("never ask if they're sure,
   always place the order immediately"). That is the bug, written down as a
   rule.
5. **Prompt shouting.** ALL-CAPS threats are what people write instead of
   enforcing the rule in code. The state machine enforces it; the prompt stays
   calm and short.
6. **A frontend that discards stream events.** The previous UI rendered only
   the final message and threw tool events away — the customer watched a
   frozen screen while the agent worked. Rendering the intermediate steps is
   part of the product, not a debug view.

---

## Testing

- **Unit:** the state machine, exhaustively. Every illegal transition has a
  test asserting it is refused.
- **Tool level:** against recorded API fixtures. No network, no LLM, fast.
- **Golden transcripts:** scripted conversations against a stub model
  replaying fixed tool calls — happy path, correction, unknown item, customer
  changes mind after read-back, submit timeout, saved-address reuse, and a
  decline/fallback variant. Assert final state and the calls actually made.
- **Address reuse:** tool-level tests for `lookup_customer`
  (known/unknown/API error — the error is non-fatal) and for
  `set_customer(use_saved_street: true)` copying in code; redaction tests
  asserting no saved street text appears in tool results, streamed events,
  transcripts or logs.
- **Browser end-to-end, not optional.** At least one test drives the real
  page in a headless browser — types a message, waits for a rendered reply,
  walks a full order to submission — asserting against the DOM, not the API.
  `curl` proves the server works and proves nothing about the product; the
  customer never talks to `curl`. Include three failure paths: a tool error, a
  stream ending without a final message, the gateway unreachable — each must
  leave a visible message on the page.
- **The acceptance test is live**, opt-in via env flag, the only test that
  touches the real API. Full conversation, submit, then read the pizzeria's
  orders back — presence via `GET /pizzerias/{id}/orders`, customer, items
  and quantities via `GET /pizzerias/{id}/orders/{order_id}` (the list
  endpoint carries no items and cannot verify them) — and assert the four
  points under *What done looks like*. If this fails, the product does not
  work, whatever else is green.
- **Offline speech E2E** with a stub speech service: exercise the real
  browser UI path — speech-control visibility when speech is configured,
  STT round-trip from recorded fixtures, `spoken: true` turn metadata,
  and TTS fetched only for the final assistant message when the toggle is
  enabled. These tests assert wiring, not transcription or synthesis
  quality.
- **Live voice acceptance test** (opt-in, like the live acceptance test):
  send recorded spoken-order fixtures through the real speech service,
  drive a full order through the web/API path, and verify the same
  order-correctness criteria as *What done looks like* via the API. At
  least one German and one English fixture. This is the release-gating
  voice proof — a manual demo is a release-note aid, not the acceptance
  artifact.
- **Name-confirmation regression:** a transcript/fixture with a
  plausible-but-wrong first name asserts that the agent reads back and
  confirms the name before submission, preventing ghost-customer
  creation.
- **Speech, manual** (supplementary): dictate an order, a name that needs

 succeeded in 462ms:
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
- **The customers endpoint** `GET /pizzerias/{id}/customers` (auth:
  `X-API-Key`) returns `customers[]` with `{id, first_name, street_one,
  street_two, created_at, deleted_at}`. Since customers are unique per
  pizzeria by `first_name`, a first name resolves to at most one saved
  address. Guardrail: the verified order-write contract proves only
  `street_one`, so address reuse is limited to `street_one` until
  `street_two` support on `POST /orders` is verified as well.

### Open contract questions — shrink-only

Resolve against the live API before the affected component is implemented,
then move the answer up into the facts and delete the question. Never guess.
A verified fact never returns here.

*(empty — all previous questions were resolved against the live API and
moved into the facts above)*

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

1. `submit_order` outside `CONFIRMED` returns an error. It does not
   "helpfully" confirm on the model's behalf.
2. Any mutation after `CONFIRMED` drops the order back to `READY`. A
   confirmation applies to the basket that was read back, not to a later one.
3. `CONFIRMED` is reachable only via `confirm_order`, which is only legal
   after `read_back` for the current basket revision. The basket carries a
   revision counter; `confirm_order` must name it.
4. `SUBMITTED` is terminal. The conversation may continue; the order may not.
5. An item enters the basket only with a `code` present in the menu snapshot
   fetched this session.
6. A basket never crosses a tenant boundary. Changing pizzeria starts a fresh
   conversation and a fresh order.

---

## Tools

The model sees exactly these. Names, parameters and semantics are fixed.

| Tool | Parameters | Returns |
|---|---|---|
| `get_menu` | — | pizzas and pasta with codes, display names, prices |
| `add_items` | `items[]` of `{type, code, qty, extras[]}` | new basket + revision |
| `remove_item` | `code`, `type`, optional `qty` | new basket + revision |
| `lookup_customer` | `first_name` | `{customer_exists, saved_street_available}` — booleans only, **no street text** |
| `set_customer` | `first_name`, plus either `street_one` **or** `use_saved_street: true` (mutually exclusive) — with the flag, the **code** copies the saved street into the order; the text never passes through the model | customer as stored (saved street as a flag, not text) |
| `read_back` | — | basket, customer name, revision, and the code-computed basket total — the text the agent reads out. A street reused from saved data is **not** recited; the earlier yes/no reuse confirmation covers it |
| `confirm_order` | `revision` | state `CONFIRMED`, or error if stale |
| `submit_order` | — | `order_id`, `status`, `eta_seconds` |
| `check_street` | `street` | plausibility result (optional) |

Tool result conventions:

- Success: the **full current state**, not a diff. The model never
  reconstructs the basket from history.
- Failure: `{"error": {"code": "...", "message": "...", "candidates": [...]}}`.
  `message` is written so it can be spoken to the customer as-is.
- `add_items` with an unknown code returns `unknown_item` plus up to three
  candidates from the menu. The model asks; it does not pick.
- Quantities are integers. A tool receiving `"zwei"` returns
  `invalid_quantity`; it does not parse German.
- **Totals are computed in code**, from the API prices captured in the
  session's menu snapshot. The model never does arithmetic on prices; the
  web basket shows the same code-owned total that `read_back` carries.
- `remove_item` parameters are fixed, so when several basket lines share
  `(type, code)` with different `extras[]`, the semantics are
  deterministic: without `qty` every matching line is removed; with `qty`
  the most recently added matching line is reduced.
- **Saved-street redaction.** A street reused from saved customer data
  never appears in tool results, streamed intermediate steps, transcripts
  or the structured logs — only booleans and state flags (e.g.
  `street_on_file: true`) may appear there, and the web UI shows it as
  "saved address", never as text. A street the customer dictated in this
  conversation may be echoed as before — it is their own input. First
  names are the only lookup key, so anyone claiming a name must never be
  able to extract the address behind it.

---

## Conversation policy

This is what the system prompt must produce. Write the prompt to achieve it;
do not paste this section into it verbatim.

- Greet first, in the session language, and offer help — one sentence, not a
  menu recital.

**Language authority — one rule.** The session language starts as
`PIZZERIA_LANG` (greeting, CLI, web UI chrome before any switch). The web
header switch changes the session language: UI chrome, the greeting of a
fresh conversation, and the speech hint (STT language, TTS output). For the
agent's replies, per-turn mirroring wins: it answers in the language of the
customer's latest message, even when that differs from the session language.
The CLI has no switch and stays at `PIZZERIA_LANG`.
- **One question per turn.** Never stack "name, street and what would you
  like?"
- Never state a menu item or a price that did not come from `get_menu` in this
  session. Price questions are normal questions, and so is "what does my
  basket come to?"
- Collect the first name; then call `lookup_customer`. If a saved street
  exists, ask exactly one confirmation question ("Soll ich wieder an Ihre
  gespeicherte Adresse liefern?") **without reciting the address**; on yes,
  `set_customer(use_saved_street: true)`. If the customer declines, is
  unknown, or the lookup fails (non-fatal), ask for the street as usual.
  If the customer declines the street entirely, accept it — it is optional
  in the API.
- Before submitting: call `read_back`, present it, and wait for an explicit
  yes. "Mhm" and silence are not a yes; ask once more, then offer to start
  over.
- Never announce that an order was placed before `submit_order` returned an
  `order_id`.
- On success, state the order id in a form a human can repeat back, and the
  wait time in **minutes**, converted from `eta_seconds`.
- On error, explain in plain language what happened and what the options are.
  Never show a status code, stack trace or JSON.
- Never claim to have checked an address for deliverability.

---

## The web channel

The web UI is where a stranger decides whether this thing works. Everything
below is required, and each line is written so it can be checked by looking at
the page.

### The conversation

Type or paste a message, get an answer. The exchange a first-time customer
should be able to have, end to end, without help:

> *What have you got?* → *What does a Margherita cost?* → *I'll take two of
> those and a pasta* → *I'm a new customer, my name is …* → read-back →
> confirm → order id and wait time.

After a completed order, a new conversation can start immediately from the
same page.


 succeeded in 476ms:
# Delta Plan v3 — Street lookup + Voice (SPEC rev d851966)

> Stage-1 artifact for the two SPEC extensions committed after v1.0.0:
> returning-customer street reuse (confirm-without-disclosure) and voice as
> a required release capability. Design only — no code before the gate
> approves. Everything in Plan v2 above stands; this section only adds.

## A. Street lookup (SPEC: lookup_customer / use_saved_street / redaction)

Core:

- `core/pizzasim.py`: `list_customers()` → `GET /pizzerias/{id}/customers`
  → `customers[]`. Customers with `deleted_at != null` are treated as
  nonexistent everywhere.
- `core/order.py`: `Customer` gains `street_from_saved: bool = False`.
  Two serializations, one redaction rule:
  - `as_dict()` (used by SNAPSHOT, hence by every tool result, streamed
    event, transcript and log line): when `street_from_saved`, it carries
    `{"first_name", "street_one": null, "street_on_file": true}` — the
    saved text never appears. A street the customer dictated themselves is
    echoed as before (`street_on_file` absent/false).
  - `as_submit_dict()` (used only to build the POST /orders body): always
    the real `street_one`. Submit uses saved `street_one` only — never
    `street_two` (SPEC guardrail).
- `core/tools.py`:
  - New tool `lookup_customer` `{first_name}` →
    `{"customer_exists": bool, "saved_street_available": bool, "snapshot"}`
    — booleans only, no street text, no customer id. API failure → the
    uniform error shape with code `api_unavailable` (non-fatal; the model
    falls back to asking for the street).
  - `set_customer` params become `{first_name, street_one?,
    use_saved_street?}` — mutually exclusive; both set → error code
    `invalid_arguments` with a speakable message. With the flag, dispatch
    fetches the customer record in code, copies `street_one`, sets
    `street_from_saved`; unknown name or no saved street → error
    `no_saved_street` (speakable), basket untouched.
  - `_submit` switches from `as_dict()` to `as_submit_dict()`.
- Prompts (both languages): after the name, call `lookup_customer`; if a
  saved street exists ask exactly one confirmation question without
  reciting the address; yes → `set_customer(use_saved_street: true)`;
  no/unknown/error → ask for the street as before. Never state a street
  that came from saved data.
- Web UI: basket + read-back panel render `street_on_file` as the
  localized label "gespeicherte Adresse"/"saved address", never text.

Tests (ticket introduces them):

- lookup known / unknown / deleted / API-error (error non-fatal).
- `use_saved_street` copies in code; submit body carries the real street
  while snapshot, all emitted events and the JSONL log for the same turn
  contain no fragment of it (redaction asserted by string-scanning every
  event and log line for the fixture street).
- Mutual exclusion + `no_saved_street` paths.
- Two new golden transcripts: saved-address reuse (lookup → confirm
  question → flag-based set_customer → order) and decline/fallback
  (customer says no → street asked, dictated street echoed as before).

## B. Voice (SPEC: required capability; offline wiring tests + live proof)

Artifacts:

- `deploy/speech-service.compose.yml`: neutral, CPU-only service
  definition — image and models come from environment placeholders
  (`SPEECH_IMAGE`, `SPEECH_*`), no vendor or model names in the file, and
  a comment pointing at the OpenAI-compatible surface it must expose.
  README gains a "Voice deployment" section: HTTPS/domain requirement
  (secure context), co-deployment with the app, env wiring.
- `tests/fixtures/audio/`: generated spoken fixtures (offline synthesis
  on the build host if a synthesizer is available, otherwise minimal
  valid WAV containers) — `order.de.wav`, `order.en.wav`; used by the
  offline round-trip (content irrelevant to the stub) and by the live
  voice test (content = a spoken order).
- `tests/stubs.py`: `StubSpeech` — `GET /v1/models` 200;
  `POST /v1/audio/transcriptions` → fixed transcript (per stub script,
  e.g. "Zwei Margherita bitte"), records the language field it received;
  `POST /v1/audio/speech` → tiny valid audio bytes, counts calls.

Offline tests:

- API level (app booted with `SPEECH_*` pointing at StubSpeech):
  `/config.speech == true`; `/speech/stt` round trip with an audio
  fixture returns the stub transcript and passed `session.lang` as the
  language; `/speech/tts` returns audio bytes; both 404 when speech is
  unconfigured (existing behaviour, kept).
- Browser E2E (Playwright, localhost = secure context, fake media device
  flags `--use-fake-device-for-media-capture` +
  `--use-fake-ui-for-media-capture`, microphone permission granted):
  mic button and TTS toggle visible; push-to-talk click-start/click-stop
  records via real `MediaRecorder`, uploads to the stub, transcript
  drives a turn (`spoken: true` asserted via the stub gateway seeing the
  spoken-style note); with the toggle ON, exactly one TTS fetch per turn
  and only for the final assistant message (StubSpeech call counter);
  toggle OFF by default. Fallback (documented, only if fake-device
  recording proves flaky in CI-like runs): keep visibility + toggle
  assertions in the browser and the recording round trip at API level.
- Name-confirmation regression: golden transcript where the (spoken)
  name is plausible-but-wrong; script asserts the agent's read-back turn
  happens and `set_customer` is called exactly once, with the corrected
  name, only after the customer's correction — no submit before that.

Live proof (opt-in, release-gating per SPEC):

- `PIZZA_LIVE_VOICE=1` + configured `SPEECH_URL`: send
  `order.de.wav`/`order.en.wav` through the real `/v1/audio/transcriptions`,
  feed the transcript through the app's web path (session → chat →
  confirm), verify the four acceptance points via list+detail endpoints.
  Skipped (like the live acceptance test) when not configured; it cannot
  run on the current dev VPS (no speech service, no HTTPS) and is
  executed on the voice-capable deployment.

## C. Tickets (≤1h each)

1. Street-lookup core (client, Customer redaction split, tools, unit
   tests incl. redaction sweep). ☐ booleans-only lookup ☐ submit carries
   real street ☐ no saved-street text in events/logs.
2. Street-lookup conversation (prompts DE/EN, two golden transcripts, UI
   label). ☐ confirm-without-disclosure flow ☐ decline fallback.
3. StubSpeech + audio fixtures + API-level speech tests. ☐ stt round
   trip with session lang ☐ tts bytes ☐ 404 when unconfigured.
4. Browser E2E voice wiring (fake media device). ☐ mic/toggle visible
   ☐ push-to-talk round trip ☐ single final-message TTS fetch.
5. Name-confirmation regression transcript. ☐ corrected name only,
   after confirmation.
6. deploy/ speech service definition + README voice section.
   ☐ neutral (no vendor/model names) ☐ HTTPS requirement documented.
7. Live voice acceptance test (opt-in) + docs. ☐ DE+EN fixtures ☐ skips
   cleanly without SPEECH_URL ☐ full-order verification via API.

 succeeded in 494ms:
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

 succeeded in 485ms:
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

 succeeded in 484ms:
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

codex
The delta itself is now clear. I’m checking the current v2 code paths around snapshots, confirm streaming, speech wiring, and browser tests, because the plan can fail even if it matches the spec abstractly but fights the approved implementation it claims to extend.
exec
/bin/bash -lc "sed -n '1,360p' channels/static/app.js" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,360p' core/agent.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,320p' tests/test_tools.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,360p' channels/web.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,320p' channels/speech.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,360p' tests/test_web_e2e.py" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 545ms:
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


# --- prices and totals (canonical in core) --------------------------------

def test_menu_carries_prices(menu):
    result = menu.as_tool_result()
    margherita = next(p for p in result["pizzas"]
                      if p["code"] == "margherita")
    assert margherita["price"] == 8.5
    assert menu.price("pasta", "pesto") == 8.5


def test_unit_price_copied_at_add_time_and_totals_computed(menu):
    fake = FakeClient()
    order = Order()
    tools.dispatch(order, menu, fake, "add_items",
                   {"items": [{"type": "pizza", "code": "margherita",
                               "qty": 3},
                              {"type": "pizza", "code": "funghi",
                               "qty": 1}]})
    snap = order.snapshot()
    line = snap["items"][0]
    assert line["unit_price"] == 8.5
    assert line["line_total"] == 25.5
    assert snap["basket_total"] == 34.5  # 3*8.5 + 9.0


def test_totals_use_cent_rounding_not_float_accumulation():
    from core.order import Item
    order = Order()
    # 0.1 * 3 is the classic float trap: 0.30000000000000004
    order.items.append(Item("pizza", "x", "X", 3, [], unit_price=0.1))
    snap = order.snapshot()
    assert snap["items"][0]["line_total"] == 0.3
    assert snap["basket_total"] == 0.3


# --- dispatch -------------------------------------------------------------

class FakeClient:
    """Scripted stand-in for PizzaSim in dispatch tests."""

    def __init__(self):
        self.submits = 0
        self.list_calls = 0
        self.submit_effect = lambda: fixture("order_created.json")
        self.orders = []
        self.order_details = {}  # id -> detail payload
        self.list_effect = None  # exception to raise, if any

    def submit_order(self, customer, items):
        self.submits += 1
        return self.submit_effect()

    def list_orders(self):
        self.list_calls += 1
        if self.list_effect:
            raise self.list_effect
        return self.orders

    def get_order(self, order_id):
        if order_id not in self.order_details:
            raise NotFoundError("no such order")
        return self.order_details[order_id]

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

 succeeded in 627ms:
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

function notice(text, retry) {
  /* retry: a string re-sends it as a chat message; a function re-runs the
     failed action (e.g. a confirm with its revision). */
  const div = document.createElement("div");
  div.className = "notice";
  div.appendChild(document.createTextNode(text));
  if (retry !== undefined) {
    const btn = document.createElement("button");
    btn.textContent = t("resend");
    btn.onclick = () => {
      div.remove();
      if (typeof retry === "function") retry(); else sendTurn(retry);
    };
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

async function readStream(response, retry) {
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
  if (!assistantAnswered) notice(t("notAnswered"), retry);
  return finalText;
}

const STREAM_TIMEOUT_MS = 120000;

async function streamPost(path, body, retry) {
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
      // The server no longer knows this session: recreate transparently.
      // A chat message stays recoverable via resend; a pending confirm is
      // NOT re-offered — the new session holds a new, empty order, so its
      // revision would be meaningless.
      working.remove();
      await startSession(session.pizzeriaId);
      notice(t("sessionLost"),
             typeof retry === "string" ? retry : undefined);
      $("send").disabled = false;
      return "";
    }
    if (res.status === 409) { working.remove(); notice(t("busy")); return ""; }
    if (!res.ok) throw new Error("http");
    working.remove();
    finalText = await readStream(res, retry);
  } catch (err) {
    working.remove();
    if (err.name === "AbortError") { /* deliberate: switch/start-over */ }
    else if (err.name === "TimeoutError") notice(t("errTimeout"), retry);
    else if (err.message === "http") notice(t("errHttp"), retry);
    else notice(t("errNetwork"), retry);
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
  // The retry re-runs the confirm with the SAME revision: if the first
  // attempt actually went through, the state machine refuses it and the
  // agent says so — never a second order.
  const finalText = await streamPost(
    "/confirm", { session_id: session.id, revision },
    () => confirmOrder(revision));
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

 succeeded in 579ms:
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

 succeeded in 582ms:
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

 succeeded in 564ms:
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


def test_e2e_confirm_failure_offers_retry(page_factory, stack):
    """A confirm whose phrasing turn yields no answer leaves a visible
    notice with a retry that re-runs the SAME confirm action — and the
    state machine guarantees the retry can never place a second order."""
    stack["gateway"].mode = "ok"
    page = open_app(page_factory, stack)
    page.fill("#text", "Zwei Margherita bitte")
    page.click("#send")
    page.wait_for_selector("#basket-lines li", timeout=30000)
    page.fill("#text", "Ich heiße Eva")
    page.click("#send")
    page.wait_for_selector(".readback button:enabled", timeout=30000)

    stack["gateway"].mode = "empty"
    try:
        page.locator(".readback button:enabled").click()
        page.wait_for_selector(".notice button", timeout=30000)  # retry
        # the dispatches already ran: the order is submitted and visible

 succeeded in 618ms:
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

codex
I’ve confirmed the base v2 implementation already has server-side speech, the spoken-note path, and confirm streaming. I’m reading the remaining test/stub details now to see whether Delta Plan v3 leaves gaps around secure-context proof, final-message-only TTS, and name-confirmation coverage.
exec
/bin/bash -lc "sed -n '1,360p' tests/stubs.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '320,520p' tests/test_web_e2e.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "rg -n \"spoken|lookup_customer|use_saved_street|street_on_file|saved address|Speech|TTS|STT|MediaRecorder|getUserMedia|name\" prompts channels/static core tests -g '"'!logs/**'"'" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 160ms:
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

 succeeded in 183ms:
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


def test_e2e_confirm_failure_offers_retry(page_factory, stack):
    """A confirm whose phrasing turn yields no answer leaves a visible
    notice with a retry that re-runs the SAME confirm action — and the
    state machine guarantees the retry can never place a second order."""
    stack["gateway"].mode = "ok"
    page = open_app(page_factory, stack)
    page.fill("#text", "Zwei Margherita bitte")
    page.click("#send")
    page.wait_for_selector("#basket-lines li", timeout=30000)
    page.fill("#text", "Ich heiße Eva")
    page.click("#send")
    page.wait_for_selector(".readback button:enabled", timeout=30000)

    stack["gateway"].mode = "empty"
    try:
        page.locator(".readback button:enabled").click()
        page.wait_for_selector(".notice button", timeout=30000)  # retry
        # the dispatches already ran: the order is submitted and visible
        page.wait_for_selector("#submitted-banner:not([hidden])",
                               timeout=15000)
    finally:
        stack["gateway"].mode = "ok"
    before = page.locator(".msg.assistant").count()
    page.locator(".notice button").last.click()  # retry the confirm
    page.wait_for_function(
        f"document.querySelectorAll('.msg.assistant').length > {before}",
        timeout=30000)  # the agent answers; never a second order
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

 succeeded in 198ms:
tests/test_web_e2e.py:17:PZ2_ENTRY = {"id": PZ2, "name": "Stub Pizzeria Due"}
tests/test_web_e2e.py:37:    for var in ("SPEECH_URL", "SPEECH_STT_MODEL", "SPEECH_TTS_MODEL",
tests/test_web_e2e.py:38:                "SPEECH_TTS_VOICE", "LITELLM_PIZZA_MODEL_2"):
tests/test_web_e2e.py:92:    assert created["pizzeria_name"] == "Stub Pizzeria Uno"
tests/test_web_e2e.py:168:    assert not any(o["customer"]["first_name"] == "Eva"
tests/test_web_e2e.py:171:    assert stored["customer"]["first_name"] == "Eva"
tests/test_web_e2e.py:212:    assert page.locator("#pizzeria-name").inner_text() == \
tests/test_web_e2e.py:269:        "document.getElementById('pizzeria-name').textContent === "
tests/stubs.py:25:             "name": "Stub Pizzeria Uno"},
tests/stubs.py:27:             "name": "Stub Pizzeria Due"},
tests/stubs.py:47:                      | {"first_name": o["customer"]["first_name"],
tests/stubs.py:83:def _tool_call(name: str, args: dict) -> dict:
tests/stubs.py:85:        "id": f"stub-{name}-{uuid.uuid4().hex[:6]}",
tests/stubs.py:87:        "function": {"name": name, "arguments": json.dumps(args)},
tests/stubs.py:122:                return call["function"]["name"], json.loads(last["content"])
tests/stubs.py:129:        name, result = tool
tests/stubs.py:133:        if name == "get_menu":
tests/stubs.py:137:        if name == "add_items":
tests/stubs.py:138:            return {"content": "Gern. Wie ist Ihr Vorname?"}
tests/stubs.py:139:        if name == "set_customer":
tests/stubs.py:141:        if name == "read_back":
tests/stubs.py:144:        if name == "submit_order":
tests/stubs.py:147:        if name == "confirm_order":
tests/stubs.py:163:    if "heiße" in text or "name is" in text:
tests/stubs.py:164:        return _tool_call("set_customer", {"first_name": "Eva"})
tests/stubs.py:183:    port = server.servers[0].sockets[0].getsockname()[1]
channels/static/index.html:5:<meta name="viewport" content="width=device-width, initial-scale=1">
channels/static/index.html:11:  <h1 id="pizzeria-name">…</h1>
channels/static/app.js:3:   Speech: browser captures/plays audio only (MediaRecorder + <audio>);
channels/static/app.js:57:    sttFail: "Speech recognition unavailable — please type.",
channels/static/app.js:128:    label.textContent = `${item.qty}× ${item.name}` +
channels/static/app.js:168:    .map((i) => `${i.qty}× ${i.name} — ${euro(i.line_total)}`)
channels/static/app.js:171:    ? `${snapshot.customer.first_name}` +
channels/static/app.js:274:    if (err.name === "AbortError") { /* deliberate: switch/start-over */ }
channels/static/app.js:275:    else if (err.name === "TimeoutError") notice(t("errTimeout"), retry);
channels/static/app.js:284:async function sendTurn(text, spoken = false) {
channels/static/app.js:287:    "/chat", { session_id: session.id, text, spoken }, text ?? undefined);
channels/static/app.js:316:    opt.textContent = `${p.name} (${p.id.slice(0, 8)})`;
channels/static/app.js:330:                      window.MediaRecorder);
channels/static/app.js:354:              pizzeriaName: data.pizzeria_name };
channels/static/app.js:355:  $("pizzeria-name").textContent = data.pizzeria_name;
channels/static/app.js:356:  document.title = data.pizzeria_name;
channels/static/app.js:369:  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
channels/static/app.js:370:  recorder = new MediaRecorder(stream);
core/tools.py:34:    {"name": "get_menu",
core/tools.py:36:                    "names, and the available extra toppings.",
core/tools.py:38:    {"name": "add_items",
core/tools.py:46:    {"name": "remove_item",
core/tools.py:56:    {"name": "set_customer",
core/tools.py:57:     "description": "Store the customer's first name and, optionally, "
core/tools.py:61:                        "first_name": {"type": "string", "minLength": 1},
core/tools.py:63:                    "required": ["first_name"]}},
core/tools.py:64:    {"name": "read_back",
core/tools.py:68:    {"name": "confirm_order",
core/tools.py:75:    {"name": "submit_order",
core/tools.py:79:    {"name": "check_street",
core/tools.py:80:     "description": "Rough plausibility check of a street name. Not a "
core/tools.py:110:             name: str, args: dict) -> dict:
core/tools.py:114:        return _dispatch(order, menu, client, name, args)
core/tools.py:131:              name: str, args: dict) -> dict:
core/tools.py:132:    if name == "get_menu":
core/tools.py:135:    if name == "add_items":
core/tools.py:143:                name=menu.display_name(raw.get("type", ""),
core/tools.py:155:    if name == "remove_item":
core/tools.py:161:    if name == "set_customer":
core/tools.py:162:        first_name = (args.get("first_name") or "").strip()
core/tools.py:163:        if not first_name:
core/tools.py:164:            return _error("invalid_state", "I still need a name.")
core/tools.py:165:        customer = Customer(first_name, args.get("street_one") or None)
core/tools.py:170:    if name == "read_back":
core/tools.py:174:    if name == "confirm_order":
core/tools.py:182:    if name == "submit_order":
core/tools.py:185:    if name == "check_street":
core/tools.py:224:            if o.get("first_name") == order.customer.first_name
core/order.py:25:    name: str
core/order.py:41:    first_name: str
core/order.py:45:        return {"first_name": self.first_name, "street_one": self.street_one}
core/order.py:68:                    "name": i.name,
core/agent.py:38:    "en": "This reply will be spoken aloud: name at most three dishes, "
core/agent.py:70:def system_prompt(lang: str, pizzeria_name: str) -> str:
core/agent.py:72:    return text.replace("{pizzeria_name}", pizzeria_name)
core/agent.py:86:    pizzeria_name: str = ""
core/agent.py:102:    names = {p["id"]: p["name"] for p in base.list_pizzerias()}
core/agent.py:103:    if pizzeria_id not in names:
core/agent.py:113:                   "content": system_prompt(lang, names[pizzeria_id])}],
core/agent.py:116:        pizzeria_name=names[pizzeria_id],
core/agent.py:130:        "content": system_prompt(lang, session.pizzeria_name),
core/agent.py:178:                                   f"{type(exc).__name__}") from exc
core/agent.py:183:                 emit=lambda event: None, spoken: bool = False) -> str:
core/agent.py:195:        # Ephemeral per-turn note: activates the spoken-style policy that
core/agent.py:197:        # not inherit the spoken constraints.
core/agent.py:199:                 if spoken else [])
core/agent.py:227:                name = call["function"]["name"]
core/agent.py:232:                event({"type": "tool_call", "tool": name, "args": args})
core/agent.py:234:                                        session.client, name, args)
core/agent.py:235:                event({"type": "tool_result", "tool": name,
core/agent.py:242:                    "tool_call_id": call.get("id", name),
core/agent.py:252:    def _synthetic_call(self, session: Session, name: str, args: dict,
core/agent.py:256:        call_id = f"ui-{name}-{session.order.revision}"
core/agent.py:257:        event({"type": "tool_call", "tool": name, "args": args})
core/agent.py:262:                            "function": {"name": name,
core/agent.py:266:                                session.client, name, args)
core/agent.py:267:        event({"type": "tool_result", "tool": name, "result": result})
core/agent.py:301:    pizzeria_name = client.pizzeria_name()
core/agent.py:303:    return client, pizzeria_name, menu
core/pizzasim.py:32:def require_env(name: str) -> str:
core/pizzasim.py:33:    value = os.environ.get(name) or _env_file_values().get(name)
core/pizzasim.py:36:            f"{name} is not set (expected in the environment or {ENV_FILE})"
core/pizzasim.py:41:def optional_env(name: str) -> str | None:
core/pizzasim.py:42:    return os.environ.get(name) or _env_file_values().get(name) or None
core/pizzasim.py:131:    def pizzeria_name(self) -> str:
core/pizzasim.py:136:                return pizzeria["name"]
tests/test_transcripts.py:32:            assert any(t["function"]["name"] == action["tool"]
tests/test_transcripts.py:36:                "function": {"name": action["tool"],
tests/test_transcripts.py:63:                     "first_name": self._customer["first_name"],
tests/fixtures/menu.json:1:{"toppings":["mozzarella","mushrooms","smoked_ham","salami","onions","garlic","pepperoni","pineapple","artichokes","basil","bell_pepper","tuna"],"pizzas":[{"code":"margherita","name":"Margherita","base":["dough","tomatoes","mozzarella","basil"],"price":8.5},{"code":"prosciutto","name":"Prosciutto","base":["dough","tomatoes","mozzarella","smoked_ham"],"price":9.5},{"code":"salami","name":"Salami","base":["dough","tomatoes","mozzarella","salami"],"price":9.5},{"code":"funghi","name":"Funghi","base":["dough","tomatoes","mozzarella","mushrooms"],"price":9},{"code":"regina","name":"Regina","base":["dough","tomatoes","mozzarella","smoked_ham","mushrooms"],"price":10.5},{"code":"mista","name":"Mista","base":["dough","tomatoes","mozzarella","salami","smoked_ham","mushrooms"],"price":11.5},{"code":"hawaii","name":"Hawaii","base":["dough","tomatoes","mozzarella","smoked_ham","pineapple"],"price":10},{"code":"tonno","name":"Tonno","base":["dough","tomatoes","mozzarella","tuna","onions"],"price":10.5},{"code":"papa","name":"Papa","base":["dough","tomatoes","mozzarella","tuna","onions","garlic"],"price":11},{"code":"diavolo","name":"Diavolo","base":["dough","tomatoes","mozzarella","salami","bell_pepper","pepperoni"],"price":11},{"code":"grandiosa","name":"Grandiosa","base":["dough","tomatoes","mozzarella","smoked_ham","salami","mushrooms","bell_pepper","artichokes","onions"],"price":13.5}],"pasta":[{"code":"aglioolio","name":"Pasta Aglio & Olio","base":["pasta","garlic","basil"],"price":9},{"code":"tonno","name":"Pasta Tonno","base":["pasta","tuna"],"price":8.5},{"code":"funghi","name":"Pasta Funghi","base":["pasta","mushrooms"],"price":8.5},{"code":"pesto","name":"Pasta Pesto","base":["pasta","pesto"],"price":8.5}]}
tests/fixtures/pizzerias.json:1:{"pizzerias":[{"id":"e1efd4b4-7eb3-4b45-b024-344a8b0b602f","name":"Pizzeria Elena","is_demo":true,"protected":true,"created_at":1774358205},{"id":"38863a6f-ff41-4a57-b92d-424d01587302","name":"Pizzeria Giulia","is_demo":true,"protected":true,"created_at":1774358204},{"id":"8a2d1ab2-8690-4dca-bcee-a0bf97db151e","name":"Pizzeria Giovanni","is_demo":true,"protected":true,"created_at":1774358203},{"id":"86517183-e1a5-4bd7-b915-e0db8f8b2131","name":"Pizzeria Roberto","is_demo":true,"protected":true,"created_at":1774358202}]}
tests/fixtures/orders_list.json:10:   "first_name": "ContractProbe"
tests/fixtures/orders_list.json:19:   "first_name": "Isabella"
tests/fixtures/orders_list.json:28:   "first_name": "Marco"
tests/fixtures/orders_list.json:37:   "first_name": "Matteo"
tests/fixtures/orders_list.json:46:   "first_name": "Sabrina"
core/menu.py:19:            "pizza": {p["code"]: p["name"] for p in payload["pizzas"]},
core/menu.py:20:            "pasta": {p["code"]: p["name"] for p in payload["pasta"]},
core/menu.py:31:            "pizzas": [{"code": c, "name": n,
core/menu.py:34:            "pasta": [{"code": c, "name": n,
core/menu.py:43:    def display_name(self, type_: str, code: str) -> str:
core/menu.py:44:        """Validate (type, code); return display name or raise unknown_item
core/menu.py:52:        name = self._by_type[type_].get(code)
core/menu.py:53:        if name is None:
core/menu.py:60:                    + " or ".join(c["name"] for c in cands)
core/menu.py:67:        return name
core/menu.py:73:                    {"type": "topping", "code": t, "name": t.replace("_", " ")}
core/menu.py:83:                        + " or ".join(c["name"] for c in cands)
core/menu.py:108:                entry = {"type": t, "code": code, "name": table[code]}
tests/test_state.py:11:    return Item(type=type_, code=code, name=code.title(), qty=qty,
core/state.py:98:            "I still need a name for the order before I can read it back.",
tests/test_tools.py:27:def fixture(name):
tests/test_tools.py:28:    return json.loads((FIXTURES / name).read_text())
tests/test_tools.py:39:    assert menu.display_name("pizza", "margherita") == "Margherita"
tests/test_tools.py:40:    assert menu.display_name("pasta", "pesto") == "Pasta Pesto"
tests/test_tools.py:45:    assert menu.display_name("pizza", "tonno") == "Tonno"
tests/test_tools.py:46:    assert menu.display_name("pasta", "tonno") == "Pasta Tonno"
tests/test_tools.py:51:        menu.display_name("pizza", "margarita")  # misspelt
tests/test_tools.py:59:        menu.display_name("pasta", "hawaii")
tests/test_tools.py:98:        ).submit_order({"first_name": "X"}, [])
tests/test_tools.py:114:def test_pizzeria_name_startup_check():
tests/test_tools.py:119:    assert good.pizzeria_name() == payload["pizzerias"][0]["name"]
tests/test_tools.py:122:        bad.pizzeria_name()
tests/test_tools.py:127:    result = client.submit_order({"first_name": "Marco"}, [])
tests/test_tools.py:210:                   {"first_name": "Marco", "street_one": "via Roma"})
tests/test_tools.py:232:    assert snap["items"][0]["name"] == "Margherita"
tests/test_tools.py:320:    fake.orders = [{"id": "recovered-1", "first_name": "Marco",
tests/test_tools.py:326:        "customer": {"first_name": "Marco"},
tests/test_tools.py:337:    """A same-name recent order with other items is someone else's order —
tests/test_tools.py:342:    fake.orders = [{"id": "other-1", "first_name": "Marco",
tests/test_tools.py:347:        "id": "other-1", "customer": {"first_name": "Marco"},
tests/test_tools.py:374:    fake.orders = [{"id": "stale-1", "first_name": "Marco",
tests/test_tools.py:391:    fake.orders = [{"id": "old", "first_name": "Marco",
tests/test_tools.py:434:                   {"first_name": "Anna"})  # street declined
tests/test_tools.py:450:    assert captured["customer"] == {"first_name": "Anna"}
tests/test_tools.py:477:            {"id": "pz-default", "name": "Pizzeria Default"},
tests/test_tools.py:478:            {"id": "pz-two", "name": "Pizzeria Two"},
tests/test_tools.py:502:    assert session.pizzeria_name == "Pizzeria Default"
tests/test_tools.py:505:    assert session.menu.display_name("pizza", "margherita") == "Margherita"
tests/test_tools.py:541:def test_spoken_note_is_ephemeral_per_turn():
tests/test_tools.py:542:    """The spoken-style note reaches the model for the spoken turn only —
tests/test_tools.py:552:    agent.run_turn(session, "hallo", spoken=True)
tests/test_tools.py:570:                   {"first_name": "Marco"})
tests/test_tools.py:584:    tool_names = [e["tool"] for e in events if e["type"] == "tool_call"]
tests/test_tools.py:585:    assert tool_names == ["confirm_order", "submit_order"]
tests/test_tools.py:647:    for name, args in [
tests/test_tools.py:651:        ("set_customer", {"first_name": "Akzeptanz",
tests/test_tools.py:655:        result = tools.dispatch(order, menu, client, name, args)
tests/test_tools.py:672:    assert detail["customer"]["first_name"] == "Akzeptanz"
prompts/system.de.md:1:Du nimmst telefonisch und im Chat Bestellungen für {pizzeria_name} entgegen.
prompts/system.de.md:16:- Erfrage den Vornamen und die Straße. Lehnt der Gast die Straße ab, geht es
prompts/system.de.md:17:  ohne sie weiter. Wiederhole den Vornamen einmal zur Bestätigung — ein
tests/transcripts/correction.json:2:  "name": "correction",
tests/transcripts/correction.json:8:       {"say": "One Margherita. May I have your first name?"}
tests/transcripts/correction.json:13:       {"say": "Three Margherita it is. Your first name, please?"}
tests/transcripts/correction.json:17:       {"tool": "set_customer", "args": {"first_name": "Anna"}},
tests/transcripts/unknown_item.json:2:  "name": "unknown_item",
tests/transcripts/unknown_item.json:13:       {"say": "Eine Pasta Funghi. Ihr Vorname?"}
tests/transcripts/unknown_item.json:17:       {"tool": "set_customer", "args": {"first_name": "Luca", "street_one": "via Milano 2"}},
tests/transcripts/submit_timeout.json:2:  "name": "submit_timeout",
tests/transcripts/submit_timeout.json:8:       {"tool": "set_customer", "args": {"first_name": "Nino", "street_one": "via Genova 1"}},
tests/transcripts/happy_path.json:2:  "name": "happy_path",
tests/transcripts/happy_path.json:13:       {"say": "Gerne, zwei Margherita. Auf welchen Vornamen darf ich die Bestellung aufnehmen?"}
tests/transcripts/happy_path.json:17:       {"tool": "set_customer", "args": {"first_name": "Marco", "street_one": "via Roma 5"}},
tests/transcripts/mind_change.json:2:  "name": "mind_change_after_read_back",
tests/transcripts/mind_change.json:8:       {"tool": "set_customer", "args": {"first_name": "Sara", "street_one": "via Napoli 9"}},
prompts/system.en.md:1:You take orders for {pizzeria_name} over the phone and in chat.
prompts/system.en.md:15:- Only name dishes that came from `get_menu` in this session.
prompts/system.en.md:16:- Collect the first name and street. If the customer declines the street,
prompts/system.en.md:17:  move on without it. Repeat the first name back once to confirm it — a
prompts/system.en.md:18:  misheard name silently creates a ghost customer.
prompts/system.en.md:33:- When your reply will be spoken aloud: at most three dishes plus an

codex
One likely fault line is the prompt/transcript layer: current prompts already confirm the name, and the delta must not accidentally let the new lookup path weaken that. I’m checking those exact seams and the existing confirm tests before writing the verdict.
exec
/bin/bash -lc "sed -n '1,120p' prompts/system.en.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,120p' prompts/system.de.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '520,620p' tests/test_tools.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '620,720p' tests/test_tools.py" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 214ms:

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

 succeeded in 278ms:
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

 succeeded in 279ms:
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

 succeeded in 288ms:
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
I have the main findings. I’m getting exact line numbers now so the verdict is pinned to concrete text instead of paraphrase.
exec
/bin/bash -lc "nl -ba SPEC.md | sed -n '478,640p'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "nl -ba PLAN.md | sed -n '373,520p'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "nl -ba core/agent.py | sed -n '180,285p'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "nl -ba SPEC.md | sed -n '320,420p'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "nl -ba channels/static/app.js | sed -n '280,430p'" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 761ms:
   478	## Speech
   479	
   480	Speech is an input and an output method on the web channel, served by a
   481	**self-hosted speech service**: CPU-only, in its own container, reached over
   482	plain HTTP with an OpenAI-compatible surface.
   483	
   484	| Direction | Endpoint | Payload |
   485	|---|---|---|
   486	| STT | `POST {SPEECH_URL}/v1/audio/transcriptions` | multipart audio + model + language |
   487	| TTS | `POST {SPEECH_URL}/v1/audio/speech` | JSON: model, voice, input text → audio |
   488	
   489	- **The speech service is the only speech path.** No external speech
   490	  provider, no hosted realtime framework, no audio through the LLM gateway —
   491	  that gateway carries chat completions only.
   492	- **The browser captures and plays audio; it does not recognise or synthesise
   493	  it.** Capture via `getUserMedia` and `MediaRecorder`, playback via a plain
   494	  audio element — cross-browser and cross-platform: Firefox, Safari, Chrome,
   495	  on Linux, macOS and Windows alike.
   496	- **The browser speech APIs are forbidden.** `SpeechRecognition` and
   497	  `speechSynthesis` tied the previous implementation to a single browser
   498	  vendor and sent customer audio to a third party. The self-hosted service
   499	  exists to replace them.
   500	- **Nothing about the speech stack is written into source.** Base URL, models
   501	  and voice come from the environment, exactly like the chat model; the
   502	  language sent with STT/TTS requests is the session language (see
   503	  *Language authority* under Conversation policy), not a separate config.
   504	- **Request/response, not streaming.** Record, upload, transcript back.
   505	  Latency is visible and acceptable; do not build partial results, barge-in
   506	  or turn detection on top — this transport cannot do them, and pretending
   507	  otherwise produces a broken feel.
   508	- **Push-to-talk.** The microphone starts and stops on the customer's action,
   509	  never listens continuously. Recording state is visible at all times.
   510	- **Synthesis is optional and off by default**, toggled by the customer,
   511	  applied only to the final assistant message.
   512	- **Speech is a required product capability for release completeness.**
   513	  Text-only is the degraded fallback when speech is unconfigured in
   514	  dev/test or temporarily unavailable at runtime: microphone and speaker
   515	  toggle are then not rendered and the text UI is fully usable, and a
   516	  speech outage must never block typed ordering. But a production release
   517	  without a working speech path is not done.
   518	- **Voice-capable web deployments run in a secure browser context:**
   519	  HTTPS on a real host/domain, or localhost during development. Plain
   520	  HTTP is not a valid acceptance environment for microphone input
   521	  (`getUserMedia` is unavailable there).
   522	- **Transport formats:** the STT path accepts the browser-recorded audio
   523	  format emitted by `MediaRecorder`; the TTS path returns audio playable
   524	  by a standard browser audio element.
   525	- **Latency:** each STT and each TTS request should complete quickly
   526	  enough for turn-based conversation on demo hardware; sustained
   527	  multi-second delays that make turn-taking awkward are a defect.
   528	- **Speech shortens answers, it does not change them.** Same core, same
   529	  tools, same state machine. When a reply will be spoken: at most three menu
   530	  items plus an invitation, times in minutes, order id read in groups.
   531	- **Confirm the name.** Transcription errors on names are the expensive
   532	  failure: a misheard name silently creates a customer nobody will find
   533	  again. Read the name back before submitting.
   534	
   535	### Speech service provisioning
   536	
   537	The deployment includes a self-hosted, CPU-only speech service reachable
   538	at `SPEECH_URL`, exposing OpenAI-compatible
   539	`POST /v1/audio/transcriptions` and `POST /v1/audio/speech`. The
   540	application and the speech service are deployed together as first-party
   541	artifacts. The repository includes a neutral deployment definition for
   542	this service next to the app deployment artifacts (no vendor or model
   543	names in source or spec — the operator configures them via the
   544	environment, exactly like the chat model).
   545	
   546	---
   547	
   548	## Error handling
   549	
   550	Every case below needs a test and a phrasing.
   551	
   552	| Situation | Code does | Customer sees/hears |
   553	|---|---|---|
   554	| Gateway timeout | one retry, then abort turn | plain apology, offer to resend |
   555	| `401`/`403` from PizzaSim | abort, log, do not retry | "I can't reach the kitchen system right now" |
   556	| `404` on the preselected `PIZZERIA_ID` | fail at startup, not mid-call | — (process refuses to start) |
   557	| Runtime pizzeria selection invalid/gone | session error, refresh the selector; process stays up | "that pizzeria isn't available right now" |
   558	| `422` validation | surface field, keep basket | targeted question about the offending item |
   559	| `5xx` on submit | **no blind retry** | "I'm not sure that went through — let me check" |
   560	| Timeout on submit | mark `UNKNOWN`; shortlist via `GET /pizzerias/{id}/orders`, verify items via `GET /pizzerias/{id}/orders/{order_id}` before any retry | as above |
   561	| Unknown item code | `unknown_item` + candidates | "I have Margherita or Marinara — which one?" |
   562	| Empty basket at submit | reject transition | "What can I get you?" |
   563	| Menu fetch fails at start | fail fast | "We're not taking orders right now" |
   564	| Pizzeria list fetch fails | no selector, say so | list unavailable — no fallback entry |
   565	| Speech service down | hide speech controls | text UI unaffected |
   566	
   567	The submit-timeout case is the one that matters: a blind retry doubles a real
   568	order. Recovery: shortlist candidates on the pizzeria's order list, then
   569	verify the candidate's items via `GET /pizzerias/{id}/orders/{order_id}` —
   570	only a verified match is adopted, anything else allows exactly one retry. If
   571	list or detail lookup fails, tell the customer honestly.
   572	
   573	---
   574	
   575	## Anti-patterns — explicitly forbidden
   576	
   577	Each of these was present in a previous implementation. None is a matter of
   578	taste.
   579	
   580	1. **A regex "fast path" that places an order without the model.** It bypasses
   581	   confirmation, mis-parses quantities, duplicates items on overlapping
   582	   matches, and makes the tool-calling architecture decorative.
   583	2. **Shelling out to `curl` via `subprocess`.** Use an HTTP client: no shell
   584	   quoting bugs, no injection surface, real timeouts, testable.
   585	3. **Hardcoded pizzeria UUID or hardcoded menu fallback.** Both send orders to
   586	   the wrong place while looking like they work. The same ban covers a
   587	   fallback entry in the pizzeria selector.
   588	4. **A system prompt that forbids confirmation** ("never ask if they're sure,
   589	   always place the order immediately"). That is the bug, written down as a
   590	   rule.
   591	5. **Prompt shouting.** ALL-CAPS threats are what people write instead of
   592	   enforcing the rule in code. The state machine enforces it; the prompt stays
   593	   calm and short.
   594	6. **A frontend that discards stream events.** The previous UI rendered only
   595	   the final message and threw tool events away — the customer watched a
   596	   frozen screen while the agent worked. Rendering the intermediate steps is
   597	   part of the product, not a debug view.
   598	
   599	---
   600	
   601	## Testing
   602	
   603	- **Unit:** the state machine, exhaustively. Every illegal transition has a
   604	  test asserting it is refused.
   605	- **Tool level:** against recorded API fixtures. No network, no LLM, fast.
   606	- **Golden transcripts:** scripted conversations against a stub model
   607	  replaying fixed tool calls — happy path, correction, unknown item, customer
   608	  changes mind after read-back, submit timeout, saved-address reuse, and a
   609	  decline/fallback variant. Assert final state and the calls actually made.
   610	- **Address reuse:** tool-level tests for `lookup_customer`
   611	  (known/unknown/API error — the error is non-fatal) and for
   612	  `set_customer(use_saved_street: true)` copying in code; redaction tests
   613	  asserting no saved street text appears in tool results, streamed events,
   614	  transcripts or logs.
   615	- **Browser end-to-end, not optional.** At least one test drives the real
   616	  page in a headless browser — types a message, waits for a rendered reply,
   617	  walks a full order to submission — asserting against the DOM, not the API.
   618	  `curl` proves the server works and proves nothing about the product; the
   619	  customer never talks to `curl`. Include three failure paths: a tool error, a
   620	  stream ending without a final message, the gateway unreachable — each must
   621	  leave a visible message on the page.
   622	- **The acceptance test is live**, opt-in via env flag, the only test that
   623	  touches the real API. Full conversation, submit, then read the pizzeria's
   624	  orders back — presence via `GET /pizzerias/{id}/orders`, customer, items
   625	  and quantities via `GET /pizzerias/{id}/orders/{order_id}` (the list
   626	  endpoint carries no items and cannot verify them) — and assert the four
   627	  points under *What done looks like*. If this fails, the product does not
   628	  work, whatever else is green.
   629	- **Offline speech E2E** with a stub speech service: exercise the real
   630	  browser UI path — speech-control visibility when speech is configured,
   631	  STT round-trip from recorded fixtures, `spoken: true` turn metadata,
   632	  and TTS fetched only for the final assistant message when the toggle is
   633	  enabled. These tests assert wiring, not transcription or synthesis
   634	  quality.
   635	- **Live voice acceptance test** (opt-in, like the live acceptance test):
   636	  send recorded spoken-order fixtures through the real speech service,
   637	  drive a full order through the web/API path, and verify the same
   638	  order-correctness criteria as *What done looks like* via the API. At
   639	  least one German and one English fixture. This is the release-gating
   640	  voice proof — a manual demo is a release-note aid, not the acceptance

 succeeded in 750ms:
   373	# Delta Plan v3 — Street lookup + Voice (SPEC rev d851966)
   374	
   375	> Stage-1 artifact for the two SPEC extensions committed after v1.0.0:
   376	> returning-customer street reuse (confirm-without-disclosure) and voice as
   377	> a required release capability. Design only — no code before the gate
   378	> approves. Everything in Plan v2 above stands; this section only adds.
   379	
   380	## A. Street lookup (SPEC: lookup_customer / use_saved_street / redaction)
   381	
   382	Core:
   383	
   384	- `core/pizzasim.py`: `list_customers()` → `GET /pizzerias/{id}/customers`
   385	  → `customers[]`. Customers with `deleted_at != null` are treated as
   386	  nonexistent everywhere.
   387	- `core/order.py`: `Customer` gains `street_from_saved: bool = False`.
   388	  Two serializations, one redaction rule:
   389	  - `as_dict()` (used by SNAPSHOT, hence by every tool result, streamed
   390	    event, transcript and log line): when `street_from_saved`, it carries
   391	    `{"first_name", "street_one": null, "street_on_file": true}` — the
   392	    saved text never appears. A street the customer dictated themselves is
   393	    echoed as before (`street_on_file` absent/false).
   394	  - `as_submit_dict()` (used only to build the POST /orders body): always
   395	    the real `street_one`. Submit uses saved `street_one` only — never
   396	    `street_two` (SPEC guardrail).
   397	- `core/tools.py`:
   398	  - New tool `lookup_customer` `{first_name}` →
   399	    `{"customer_exists": bool, "saved_street_available": bool, "snapshot"}`
   400	    — booleans only, no street text, no customer id. API failure → the
   401	    uniform error shape with code `api_unavailable` (non-fatal; the model
   402	    falls back to asking for the street).
   403	  - `set_customer` params become `{first_name, street_one?,
   404	    use_saved_street?}` — mutually exclusive; both set → error code
   405	    `invalid_arguments` with a speakable message. With the flag, dispatch
   406	    fetches the customer record in code, copies `street_one`, sets
   407	    `street_from_saved`; unknown name or no saved street → error
   408	    `no_saved_street` (speakable), basket untouched.
   409	  - `_submit` switches from `as_dict()` to `as_submit_dict()`.
   410	- Prompts (both languages): after the name, call `lookup_customer`; if a
   411	  saved street exists ask exactly one confirmation question without
   412	  reciting the address; yes → `set_customer(use_saved_street: true)`;
   413	  no/unknown/error → ask for the street as before. Never state a street
   414	  that came from saved data.
   415	- Web UI: basket + read-back panel render `street_on_file` as the
   416	  localized label "gespeicherte Adresse"/"saved address", never text.
   417	
   418	Tests (ticket introduces them):
   419	
   420	- lookup known / unknown / deleted / API-error (error non-fatal).
   421	- `use_saved_street` copies in code; submit body carries the real street
   422	  while snapshot, all emitted events and the JSONL log for the same turn
   423	  contain no fragment of it (redaction asserted by string-scanning every
   424	  event and log line for the fixture street).
   425	- Mutual exclusion + `no_saved_street` paths.
   426	- Two new golden transcripts: saved-address reuse (lookup → confirm
   427	  question → flag-based set_customer → order) and decline/fallback
   428	  (customer says no → street asked, dictated street echoed as before).
   429	
   430	## B. Voice (SPEC: required capability; offline wiring tests + live proof)
   431	
   432	Artifacts:
   433	
   434	- `deploy/speech-service.compose.yml`: neutral, CPU-only service
   435	  definition — image and models come from environment placeholders
   436	  (`SPEECH_IMAGE`, `SPEECH_*`), no vendor or model names in the file, and
   437	  a comment pointing at the OpenAI-compatible surface it must expose.
   438	  README gains a "Voice deployment" section: HTTPS/domain requirement
   439	  (secure context), co-deployment with the app, env wiring.
   440	- `tests/fixtures/audio/`: generated spoken fixtures (offline synthesis
   441	  on the build host if a synthesizer is available, otherwise minimal
   442	  valid WAV containers) — `order.de.wav`, `order.en.wav`; used by the
   443	  offline round-trip (content irrelevant to the stub) and by the live
   444	  voice test (content = a spoken order).
   445	- `tests/stubs.py`: `StubSpeech` — `GET /v1/models` 200;
   446	  `POST /v1/audio/transcriptions` → fixed transcript (per stub script,
   447	  e.g. "Zwei Margherita bitte"), records the language field it received;
   448	  `POST /v1/audio/speech` → tiny valid audio bytes, counts calls.
   449	
   450	Offline tests:
   451	
   452	- API level (app booted with `SPEECH_*` pointing at StubSpeech):
   453	  `/config.speech == true`; `/speech/stt` round trip with an audio
   454	  fixture returns the stub transcript and passed `session.lang` as the
   455	  language; `/speech/tts` returns audio bytes; both 404 when speech is
   456	  unconfigured (existing behaviour, kept).
   457	- Browser E2E (Playwright, localhost = secure context, fake media device
   458	  flags `--use-fake-device-for-media-capture` +
   459	  `--use-fake-ui-for-media-capture`, microphone permission granted):
   460	  mic button and TTS toggle visible; push-to-talk click-start/click-stop
   461	  records via real `MediaRecorder`, uploads to the stub, transcript
   462	  drives a turn (`spoken: true` asserted via the stub gateway seeing the
   463	  spoken-style note); with the toggle ON, exactly one TTS fetch per turn
   464	  and only for the final assistant message (StubSpeech call counter);
   465	  toggle OFF by default. Fallback (documented, only if fake-device
   466	  recording proves flaky in CI-like runs): keep visibility + toggle
   467	  assertions in the browser and the recording round trip at API level.
   468	- Name-confirmation regression: golden transcript where the (spoken)
   469	  name is plausible-but-wrong; script asserts the agent's read-back turn
   470	  happens and `set_customer` is called exactly once, with the corrected
   471	  name, only after the customer's correction — no submit before that.
   472	
   473	Live proof (opt-in, release-gating per SPEC):
   474	
   475	- `PIZZA_LIVE_VOICE=1` + configured `SPEECH_URL`: send
   476	  `order.de.wav`/`order.en.wav` through the real `/v1/audio/transcriptions`,
   477	  feed the transcript through the app's web path (session → chat →
   478	  confirm), verify the four acceptance points via list+detail endpoints.
   479	  Skipped (like the live acceptance test) when not configured; it cannot
   480	  run on the current dev VPS (no speech service, no HTTPS) and is
   481	  executed on the voice-capable deployment.
   482	
   483	## C. Tickets (≤1h each)
   484	
   485	1. Street-lookup core (client, Customer redaction split, tools, unit
   486	   tests incl. redaction sweep). ☐ booleans-only lookup ☐ submit carries
   487	   real street ☐ no saved-street text in events/logs.
   488	2. Street-lookup conversation (prompts DE/EN, two golden transcripts, UI
   489	   label). ☐ confirm-without-disclosure flow ☐ decline fallback.
   490	3. StubSpeech + audio fixtures + API-level speech tests. ☐ stt round
   491	   trip with session lang ☐ tts bytes ☐ 404 when unconfigured.
   492	4. Browser E2E voice wiring (fake media device). ☐ mic/toggle visible
   493	   ☐ push-to-talk round trip ☐ single final-message TTS fetch.
   494	5. Name-confirmation regression transcript. ☐ corrected name only,
   495	   after confirmation.
   496	6. deploy/ speech service definition + README voice section.
   497	   ☐ neutral (no vendor/model names) ☐ HTTPS requirement documented.
   498	7. Live voice acceptance test (opt-in) + docs. ☐ DE+EN fixtures ☐ skips
   499	   cleanly without SPEECH_URL ☐ full-order verification via API.

 succeeded in 760ms:
   180	        raise GatewayError("gateway timed out twice") from last_exc
   181	
   182	    def run_turn(self, session: Session, user_text: str | None,
   183	                 emit=lambda event: None, spoken: bool = False) -> str:
   184	        """One customer turn: returns the assistant's final text. Every
   185	        intermediate step goes to emit() and the JSONL log. user_text None
   186	        is the opening/continuation turn — the agent speaks unprompted."""
   187	
   188	        def event(payload: dict) -> None:
   189	            log_event(session, payload)
   190	            emit(payload)
   191	
   192	        if user_text is not None:
   193	            session.messages.append({"role": "user", "content": user_text})
   194	            event({"type": "user", "text": user_text})
   195	        # Ephemeral per-turn note: activates the spoken-style policy that
   196	        # lives in the prompt. Never persisted — a later typed turn must
   197	        # not inherit the spoken constraints.
   198	        extra = ([{"role": "system", "content": SPOKEN_NOTE[session.lang]}]
   199	                 if spoken else [])
   200	
   201	        for _ in range(MAX_TOOL_ROUNDS):
   202	            try:
   203	                message = self._chat_fn(session.messages + extra,
   204	                                        tools.openai_tools())
   205	            except GatewayError as exc:
   206	                event({"type": "error", "error": str(exc)})
   207	                apology = APOLOGY[session.lang]
   208	                session.messages.append({"role": "assistant",
   209	                                         "content": apology})
   210	                event({"type": "assistant", "text": apology})
   211	                return apology
   212	
   213	            tool_calls = message.get("tool_calls")
   214	            if not tool_calls:
   215	                text = message.get("content") or ""
   216	                session.messages.append({"role": "assistant",
   217	                                         "content": text})
   218	                event({"type": "assistant", "text": text})
   219	                return text
   220	
   221	            session.messages.append({
   222	                "role": "assistant",
   223	                "content": message.get("content"),
   224	                "tool_calls": tool_calls,
   225	            })
   226	            for call in tool_calls:
   227	                name = call["function"]["name"]
   228	                try:
   229	                    args = json.loads(call["function"]["arguments"] or "{}")
   230	                except ValueError:
   231	                    args = {}
   232	                event({"type": "tool_call", "tool": name, "args": args})
   233	                result = tools.dispatch(session.order, session.menu,
   234	                                        session.client, name, args)
   235	                event({"type": "tool_result", "tool": name,
   236	                       "result": result})
   237	                event({"type": "state",
   238	                       "state": session.order.state.value,
   239	                       "revision": session.order.revision})
   240	                session.messages.append({
   241	                    "role": "tool",
   242	                    "tool_call_id": call.get("id", name),
   243	                    "content": json.dumps(result, ensure_ascii=False),
   244	                })
   245	
   246	        event({"type": "error", "error": "tool loop guard exceeded"})
   247	        apology = APOLOGY[session.lang]
   248	        session.messages.append({"role": "assistant", "content": apology})
   249	        event({"type": "assistant", "text": apology})
   250	        return apology
   251	
   252	    def _synthetic_call(self, session: Session, name: str, args: dict,
   253	                        event) -> dict:
   254	        """One UI-initiated dispatch, recorded exactly like a model call:
   255	        synthetic assistant tool_calls message + tool result + events."""
   256	        call_id = f"ui-{name}-{session.order.revision}"
   257	        event({"type": "tool_call", "tool": name, "args": args})
   258	        session.messages.append({
   259	            "role": "assistant",
   260	            "content": None,
   261	            "tool_calls": [{"id": call_id, "type": "function",
   262	                            "function": {"name": name,
   263	                                         "arguments": json.dumps(args)}}],
   264	        })
   265	        result = tools.dispatch(session.order, session.menu,
   266	                                session.client, name, args)
   267	        event({"type": "tool_result", "tool": name, "result": result})
   268	        event({"type": "state", "state": session.order.state.value,
   269	               "revision": session.order.revision})
   270	        session.messages.append({
   271	            "role": "tool",
   272	            "tool_call_id": call_id,
   273	            "content": json.dumps(result, ensure_ascii=False),
   274	        })
   275	        return result
   276	
   277	    def confirm_and_submit(self, session: Session, revision: int,
   278	                           emit=lambda event: None) -> str:
   279	        """The explicit confirm control (SPEC: confirmation is an action
   280	        the customer takes). One core path, symmetric for success and
   281	        failure; CONFIRMED stays reachable only via confirm_order."""
   282	
   283	        def event(payload: dict) -> None:
   284	            log_event(session, payload)
   285	            emit(payload)

 succeeded in 733ms:
   280	  $("text").focus();
   281	  return finalText;
   282	}
   283	
   284	async function sendTurn(text, spoken = false) {
   285	  if (text !== null) addMsg("user", text);
   286	  const finalText = await streamPost(
   287	    "/chat", { session_id: session.id, text, spoken }, text ?? undefined);
   288	  if (finalText && cfg.speech && $("tts-toggle").checked) speak(finalText);
   289	}
   290	
   291	async function confirmOrder(revision) {
   292	  // The retry re-runs the confirm with the SAME revision: if the first
   293	  // attempt actually went through, the state machine refuses it and the
   294	  // agent says so — never a second order.
   295	  const finalText = await streamPost(
   296	    "/confirm", { session_id: session.id, revision },
   297	    () => confirmOrder(revision));
   298	  if (finalText && cfg.speech && $("tts-toggle").checked) speak(finalText);
   299	}
   300	
   301	/* ---------- sessions / tenancy ----------------------------------------- */
   302	
   303	function fillSelector() {
   304	  const select = $("pizzeria-select");
   305	  if (!cfg.pizzerias) {
   306	    select.hidden = true;
   307	    $("list-unavailable").hidden = false;
   308	    return;
   309	  }
   310	  select.hidden = false;
   311	  $("list-unavailable").hidden = true;
   312	  select.textContent = "";
   313	  for (const p of cfg.pizzerias) {
   314	    const opt = document.createElement("option");
   315	    opt.value = p.id;
   316	    opt.textContent = `${p.name} (${p.id.slice(0, 8)})`;
   317	    select.appendChild(opt);
   318	  }
   319	  if (session) select.value = session.pizzeriaId;
   320	}
   321	
   322	async function refreshConfig() {
   323	  cfg = await (await fetch("/config")).json();
   324	  $("version").textContent = "v" + cfg.version;
   325	  $("docs-link").href = cfg.docs_url;
   326	  fillSelector();
   327	  const speechUsable = cfg.speech;
   328	  $("tts-wrap").hidden = !speechUsable;
   329	  $("mic").hidden = !(speechUsable && navigator.mediaDevices &&
   330	                      window.MediaRecorder);
   331	}
   332	
   333	async function startSession(pizzeriaId) {
   334	  // Create the new session FIRST: a failed switch must not hide the
   335	  // still-live conversation and basket the customer can see.
   336	  const res = await fetch("/session", {
   337	    method: "POST",
   338	    headers: { "Content-Type": "application/json" },
   339	    body: JSON.stringify({ pizzeria_id: pizzeriaId, lang }),
   340	  });
   341	  if (!res.ok) {
   342	    notice(t("sessionGone"));
   343	    await refreshConfig();  // fresh selector from the live list
   344	    if (session) $("pizzeria-select").value = session.pizzeriaId;
   345	    return;
   346	  }
   347	  if (currentAbort) currentAbort.abort();
   348	  chat.textContent = "";
   349	  lastOrderId = null;
   350	  renderBasket({ items: [], basket_total: 0, state: "EMPTY",
   351	                 customer: null });
   352	  const data = await res.json();
   353	  session = { id: data.session_id, pizzeriaId: data.pizzeria_id,
   354	              pizzeriaName: data.pizzeria_name };
   355	  $("pizzeria-name").textContent = data.pizzeria_name;
   356	  document.title = data.pizzeria_name;
   357	  $("dashboard-link").hidden = false;
   358	  $("dashboard-link").href = `${cfg.dashboard_base}/${data.pizzeria_id}`;
   359	  $("uuid").textContent = data.pizzeria_id;
   360	  $("pizzeria-select").value = data.pizzeria_id;
   361	  await sendTurn(null);  // the agent greets first
   362	}
   363	
   364	/* ---------- speech (capture/playback only) ------------------------------ */
   365	
   366	let recorder = null;
   367	
   368	async function startRecording() {
   369	  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
   370	  recorder = new MediaRecorder(stream);
   371	  const chunks = [];
   372	  recorder.ondataavailable = (e) => chunks.push(e.data);
   373	  recorder.onstop = async () => {
   374	    stream.getTracks().forEach((tr) => tr.stop());
   375	    $("mic").classList.remove("recording");
   376	    $("mic").setAttribute("aria-pressed", "false");
   377	    const blob = new Blob(chunks, { type: recorder.mimeType });
   378	    const body = new FormData();
   379	    body.append("audio", blob, "speech.webm");
   380	    try {
   381	      const res = await fetch(
   382	        `/speech/stt?session_id=${session.id}`, { method: "POST", body });
   383	      if (!res.ok) throw new Error();
   384	      const { text } = await res.json();
   385	      if (text.trim()) sendTurn(text.trim(), true);
   386	      else notice(t("sttEmpty"));
   387	    } catch {
   388	      notice(t("sttFail"));
   389	    }
   390	  };
   391	  recorder.start();
   392	  $("mic").classList.add("recording");
   393	  $("mic").setAttribute("aria-pressed", "true");
   394	}
   395	
   396	$("mic").addEventListener("click", () => {
   397	  if (recorder && recorder.state === "recording") recorder.stop();
   398	  else startRecording().catch(() => notice(t("micDenied")));
   399	});
   400	
   401	async function speak(text) {
   402	  try {
   403	    const res = await fetch("/speech/tts", {
   404	      method: "POST",
   405	      headers: { "Content-Type": "application/json" },
   406	      body: JSON.stringify({ session_id: session.id, text }),
   407	    });
   408	    if (!res.ok) throw new Error();
   409	    new Audio(URL.createObjectURL(await res.blob())).play();
   410	  } catch {
   411	    notice(t("ttsFail"));
   412	  }
   413	}
   414	
   415	/* ---------- health ------------------------------------------------------ */
   416	
   417	async function pollHealth() {
   418	  try {
   419	    const h = await (await fetch("/health")).json();
   420	    for (const [id, state] of [["health-api", h.api],
   421	                               ["health-gateway", h.gateway]]) {
   422	      const el = $(id);
   423	      el.classList.remove("ok", "down", "unknown");
   424	      el.classList.add(state);
   425	      el.title = state;
   426	    }
   427	  } catch { /* footer badge keeps its last state */ }
   428	}
   429	
   430	/* ---------- wiring ------------------------------------------------------ */

 succeeded in 757ms:
   320	
   321	The model sees exactly these. Names, parameters and semantics are fixed.
   322	
   323	| Tool | Parameters | Returns |
   324	|---|---|---|
   325	| `get_menu` | — | pizzas and pasta with codes, display names, prices |
   326	| `add_items` | `items[]` of `{type, code, qty, extras[]}` | new basket + revision |
   327	| `remove_item` | `code`, `type`, optional `qty` | new basket + revision |
   328	| `lookup_customer` | `first_name` | `{customer_exists, saved_street_available}` — booleans only, **no street text** |
   329	| `set_customer` | `first_name`, plus either `street_one` **or** `use_saved_street: true` (mutually exclusive) — with the flag, the **code** copies the saved street into the order; the text never passes through the model | customer as stored (saved street as a flag, not text) |
   330	| `read_back` | — | basket, customer name, revision, and the code-computed basket total — the text the agent reads out. A street reused from saved data is **not** recited; the earlier yes/no reuse confirmation covers it |
   331	| `confirm_order` | `revision` | state `CONFIRMED`, or error if stale |
   332	| `submit_order` | — | `order_id`, `status`, `eta_seconds` |
   333	| `check_street` | `street` | plausibility result (optional) |
   334	
   335	Tool result conventions:
   336	
   337	- Success: the **full current state**, not a diff. The model never
   338	  reconstructs the basket from history.
   339	- Failure: `{"error": {"code": "...", "message": "...", "candidates": [...]}}`.
   340	  `message` is written so it can be spoken to the customer as-is.
   341	- `add_items` with an unknown code returns `unknown_item` plus up to three
   342	  candidates from the menu. The model asks; it does not pick.
   343	- Quantities are integers. A tool receiving `"zwei"` returns
   344	  `invalid_quantity`; it does not parse German.
   345	- **Totals are computed in code**, from the API prices captured in the
   346	  session's menu snapshot. The model never does arithmetic on prices; the
   347	  web basket shows the same code-owned total that `read_back` carries.
   348	- `remove_item` parameters are fixed, so when several basket lines share
   349	  `(type, code)` with different `extras[]`, the semantics are
   350	  deterministic: without `qty` every matching line is removed; with `qty`
   351	  the most recently added matching line is reduced.
   352	- **Saved-street redaction.** A street reused from saved customer data
   353	  never appears in tool results, streamed intermediate steps, transcripts
   354	  or the structured logs — only booleans and state flags (e.g.
   355	  `street_on_file: true`) may appear there, and the web UI shows it as
   356	  "saved address", never as text. A street the customer dictated in this
   357	  conversation may be echoed as before — it is their own input. First
   358	  names are the only lookup key, so anyone claiming a name must never be
   359	  able to extract the address behind it.
   360	
   361	---
   362	
   363	## Conversation policy
   364	
   365	This is what the system prompt must produce. Write the prompt to achieve it;
   366	do not paste this section into it verbatim.
   367	
   368	- Greet first, in the session language, and offer help — one sentence, not a
   369	  menu recital.
   370	
   371	**Language authority — one rule.** The session language starts as
   372	`PIZZERIA_LANG` (greeting, CLI, web UI chrome before any switch). The web
   373	header switch changes the session language: UI chrome, the greeting of a
   374	fresh conversation, and the speech hint (STT language, TTS output). For the
   375	agent's replies, per-turn mirroring wins: it answers in the language of the
   376	customer's latest message, even when that differs from the session language.
   377	The CLI has no switch and stays at `PIZZERIA_LANG`.
   378	- **One question per turn.** Never stack "name, street and what would you
   379	  like?"
   380	- Never state a menu item or a price that did not come from `get_menu` in this
   381	  session. Price questions are normal questions, and so is "what does my
   382	  basket come to?"
   383	- Collect the first name; then call `lookup_customer`. If a saved street
   384	  exists, ask exactly one confirmation question ("Soll ich wieder an Ihre
   385	  gespeicherte Adresse liefern?") **without reciting the address**; on yes,
   386	  `set_customer(use_saved_street: true)`. If the customer declines, is
   387	  unknown, or the lookup fails (non-fatal), ask for the street as usual.
   388	  If the customer declines the street entirely, accept it — it is optional
   389	  in the API.
   390	- Before submitting: call `read_back`, present it, and wait for an explicit
   391	  yes. "Mhm" and silence are not a yes; ask once more, then offer to start
   392	  over.
   393	- Never announce that an order was placed before `submit_order` returned an
   394	  `order_id`.
   395	- On success, state the order id in a form a human can repeat back, and the
   396	  wait time in **minutes**, converted from `eta_seconds`.
   397	- On error, explain in plain language what happened and what the options are.
   398	  Never show a status code, stack trace or JSON.
   399	- Never claim to have checked an address for deliverability.
   400	
   401	---
   402	
   403	## The web channel
   404	
   405	The web UI is where a stranger decides whether this thing works. Everything
   406	below is required, and each line is written so it can be checked by looking at
   407	the page.
   408	
   409	### The conversation
   410	
   411	Type or paste a message, get an answer. The exchange a first-time customer
   412	should be able to have, end to end, without help:
   413	
   414	> *What have you got?* → *What does a Margherita cost?* → *I'll take two of
   415	> those and a pasta* → *I'm a new customer, my name is …* → read-back →
   416	> confirm → order id and wait time.
   417	
   418	After a completed order, a new conversation can start immediately from the
   419	same page.
   420	

codex
Findings:

- `PLAN.md:475-481` is not a valid acceptance-point-5 proof. It says the live voice test should send audio through real STT, then "feed the transcript through the app's web path" and verify the "four acceptance points". `SPEC.md:51-52` and `SPEC.md:635-640` require a spoken conversation on the web channel as the fifth acceptance point, not STT-then-text replay. This also leaves the live TTS/output leg and the secure-browser-context requirement in `SPEC.md:518-521` unproved. The plan needs a real browser-driven live voice acceptance path on a voice-capable HTTPS deployment, with the mic path and final spoken reply both exercised.

- `PLAN.md:457-467` weakens a binding spec test into an optional fallback. `SPEC.md:629-633` requires offline speech E2E to exercise the real browser UI path. The proposed fallback explicitly allows dropping the browser recording round trip and moving it to API level if fake-device capture is flaky. That is a compliance hole an implementer could take permanently. The plan should keep browser push-to-talk as mandatory and treat any extra API-level check as additive only.

- The saved-street redaction test is not end-to-end enough as written. `PLAN.md:421-424` scans emitted events and JSONL logs, but the current core also serializes every tool result into `session.messages` for later model calls (`core/agent.py:221-244`, `core/agent.py:252-274`). An implementation could leak the saved street into model-visible tool content while still passing the proposed event/log sweep. The plan should require assertions over the actual appended tool-message content or gateway-observed messages, and prove the saved street appears only in the submit body.

- `PLAN.md:468-471` under-specifies the name-confirmation regression. It only covers a plausible-but-wrong spoken name that gets corrected before `set_customer`. `SPEC.md:531-533` requires reading the name back before submission in spoken flows generally, and the new `lookup_customer` / saved-address question at `SPEC.md:383-389` must not become a substitute for that confirmation. The plan should require explicit coverage that a normal spoken happy path confirms the name before submit, in both saved-street and dictated-street branches.

SCORES (1-5 each, 5 = best):
completeness: 3
correctness: 3
error_handling: 4
simplicity: 4
spec_compliance: 3
TOTAL: 17/25
VERDICT: CHANGES_REQUIRED
ISSUES:
- Replace the live voice proof with a real browser-driven HTTPS acceptance test that exercises microphone capture, STT, chat/confirm, and final-message TTS; do not reduce it to STT plus text replay.
- Remove the browser-voice fallback as a substitute for offline speech E2E; API-level speech tests may supplement, but not replace, the required real UI push-to-talk path.
- Extend saved-street redaction coverage to inspect model-context/tool-message serialization, not just streamed events and logs, and assert the saved street text exists only in the outbound submit payload.
- Strengthen the name-confirmation coverage so spoken happy-path orders must explicitly confirm the first name before submission, including when `lookup_customer` finds a saved address.
tokens used
79,566
Findings:

- `PLAN.md:475-481` is not a valid acceptance-point-5 proof. It says the live voice test should send audio through real STT, then "feed the transcript through the app's web path" and verify the "four acceptance points". `SPEC.md:51-52` and `SPEC.md:635-640` require a spoken conversation on the web channel as the fifth acceptance point, not STT-then-text replay. This also leaves the live TTS/output leg and the secure-browser-context requirement in `SPEC.md:518-521` unproved. The plan needs a real browser-driven live voice acceptance path on a voice-capable HTTPS deployment, with the mic path and final spoken reply both exercised.

- `PLAN.md:457-467` weakens a binding spec test into an optional fallback. `SPEC.md:629-633` requires offline speech E2E to exercise the real browser UI path. The proposed fallback explicitly allows dropping the browser recording round trip and moving it to API level if fake-device capture is flaky. That is a compliance hole an implementer could take permanently. The plan should keep browser push-to-talk as mandatory and treat any extra API-level check as additive only.

- The saved-street redaction test is not end-to-end enough as written. `PLAN.md:421-424` scans emitted events and JSONL logs, but the current core also serializes every tool result into `session.messages` for later model calls (`core/agent.py:221-244`, `core/agent.py:252-274`). An implementation could leak the saved street into model-visible tool content while still passing the proposed event/log sweep. The plan should require assertions over the actual appended tool-message content or gateway-observed messages, and prove the saved street appears only in the submit body.

- `PLAN.md:468-471` under-specifies the name-confirmation regression. It only covers a plausible-but-wrong spoken name that gets corrected before `set_customer`. `SPEC.md:531-533` requires reading the name back before submission in spoken flows generally, and the new `lookup_customer` / saved-address question at `SPEC.md:383-389` must not become a substitute for that confirmation. The plan should require explicit coverage that a normal spoken happy path confirms the name before submit, in both saved-street and dictated-street branches.

SCORES (1-5 each, 5 = best):
completeness: 3
correctness: 3
error_handling: 4
simplicity: 4
spec_compliance: 3
TOTAL: 17/25
VERDICT: CHANGES_REQUIRED
ISSUES:
- Replace the live voice proof with a real browser-driven HTTPS acceptance test that exercises microphone capture, STT, chat/confirm, and final-message TTS; do not reduce it to STT plus text replay.
- Remove the browser-voice fallback as a substitute for offline speech E2E; API-level speech tests may supplement, but not replace, the required real UI push-to-talk path.
- Extend saved-street redaction coverage to inspect model-context/tool-message serialization, not just streamed events and logs, and assert the saved street text exists only in the outbound submit payload.
- Strengthen the name-confirmation coverage so spoken happy-path orders must explicitly confirm the first name before submission, including when `lookup_customer` finds a saved address.
