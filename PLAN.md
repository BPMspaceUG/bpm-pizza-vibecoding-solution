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
`requirements.txt` (+playwright). Everything else stands as approved.

## Tickets (each ≤ 1h, tests in the ticket that introduces the behaviour)

1. **Prices & totals in core.** Menu price, `Item.unit_price`,
   snapshot totals (Decimal), get_menu result, prompt rule.
   ☐ totals only in core ☐ rounding tested ☐ v1 suite still green.
2. **Session factory & tenancy.** Session v2 fields, `create_session`,
   client per session, agent uses `session.client`, startup preselection
   check kept. ☐ unknown id → typed error ☐ tenant immutable ☐ tests.
3. **Language authority.** `Session.lang`, `set_language` re-render,
   apologies/STT via session.lang. ☐ switch test ☐ no process-global lang.
4. **Confirm path.** `Agent.confirm_and_submit` + synthetic messages.
   ☐ stale revision streams error, nothing submitted ☐ happy path test
   ☐ timeout-recovery reachable from this path.
5. **Web API surface.** /config, /session, /confirm, /language, /health,
   session 404/409 semantics, speech extraction to `channels/speech.py`.
   ☐ httpx TestClient tests with stub PizzaSim ☐ no order logic in routes.
6. **Web UI: frame.** Header (name, selector, dashboard link, language,
   start over), footer (version, UUID, health badges, docs), i18n chrome.
   ☐ switch/start-over create fresh session + abort in-flight stream.
7. **Web UI: conversation contract.** Basket panel, read-back panel +
   confirm button, working indicator, done-without-assistant notice,
   error/resend paths, submitted lock.
   ☐ every notice in session language ☐ no discarded stream events.
8. **Browser E2E suite.** Stub PizzaSim + stub gateway + Playwright;
   scenarios 1–5 above. ☐ fully offline ☐ DOM assertions only.
9. **Harden + docs.** Error-table walk incl. new rows, README (all
   channels + E2E + speech checklist), `.env.example`, `APP_VERSION`
   start at `2.0.0`. ☐ full suite green ☐ live acceptance re-run.

Review protocol: this plan goes to the reviewer (Issue gate) before any
code; implementation follows only after APPROVED under the SPEC rubric.
