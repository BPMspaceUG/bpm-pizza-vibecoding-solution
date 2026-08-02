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

> Status 2026-08-01: tickets 1-9 all
> implemented; every acceptance box below is verified by the committed
> test suite (101 passed offline incl. 6 browser E2E, live acceptance
> passed).

1. **Prices & totals in core.** Menu price, `Item.unit_price`,
   snapshot totals (Decimal), get_menu result, prompt rule.
   ☑ totals only in core ☑ rounding tested ☑ v1 suite still green.
2. **Session factory & tenancy.** Session v2 fields, `create_session`,
   client per session, agent uses `session.client`, startup preselection
   check kept. ☑ unknown id → typed error ☑ tenant immutable ☑ tests.
3. **Language authority.** `Session.lang`, `set_language` re-render,
   apologies/STT via session.lang. ☑ switch test ☑ no process-global lang.
4. **Confirm path.** `Agent.confirm_and_submit` + synthetic messages.
   ☑ stale revision streams error, nothing submitted ☑ happy path test
   ☑ timeout-recovery reachable from this path.
5. **Web API surface.** /config, /session, /confirm, /language, /health,
   session 404/409 semantics, speech extraction to `channels/speech.py`.
   ☑ httpx TestClient tests with stub PizzaSim ☑ no order logic in routes.
6. **Web UI: frame.** Header (name, selector, dashboard link, language,
   start over), footer (version, UUID, health badges, docs), i18n chrome.
   ☑ switch/start-over create fresh session + abort in-flight stream.
7. **Web UI: conversation contract.** Basket panel, read-back panel +
   confirm button, working indicator, done-without-assistant notice,
   error/resend paths, submitted lock.
   ☑ every notice in session language ☑ no discarded stream events.
8. **Browser E2E suite.** Stub PizzaSim + stub gateway + Playwright;
   scenarios 1–5 above. ☑ fully offline ☑ DOM assertions only.
9. **Harden + docs.** Error-table walk incl. new rows, README (all
   channels + E2E + speech checklist), `.env.example`, `APP_VERSION`
   start at `2.0.0`. ☑ full suite green ☑ live acceptance re-run.

Review protocol: this plan goes to the reviewer (Issue gate) before any
code; implementation follows only after APPROVED under the SPEC rubric.


---

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
- `use_saved_street` copies in code; the redaction sweep is end to end:
  after the full flow, the fixture street text must appear in exactly one
  place — the outbound submit payload (captured via a client spy) — and in
  no snapshot, no emitted event, no JSONL log line, and **no entry of
  `session.messages`** (the model-visible tool-message serialization is
  string-scanned too; an implementation that leaks the street into tool
  content the model reads must fail this test).
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
  `--use-fake-ui-for-media-capture` +
  `--use-file-for-fake-audio-capture=<fixture wav>`, microphone
  permission granted): mic button and TTS toggle visible; push-to-talk
  click-start/click-stop records via real `MediaRecorder` (the fake
  device streams the audio fixture), uploads to the stub, transcript
  drives a turn (`spoken: true` asserted via the stub gateway seeing the
  spoken-style note); with the toggle ON, exactly one TTS fetch per turn
  and only for the final assistant message (StubSpeech call counter);
  toggle OFF by default. This real UI push-to-talk path is mandatory —
  API-level speech tests supplement it and never substitute for it.
- Name-confirmation regression, three scripted cases (the saved-address
  question is **not** a substitute for name confirmation):
  1. plausible-but-wrong spoken name: agent repeats the name back, the
     customer corrects, `set_customer` is called exactly once with the
     corrected name, only after the correction — no submit before that;
  2. spoken happy path, dictated street: the name is confirmed before
     submission;
  3. spoken happy path, saved street reused: the name is confirmed before
     submission *in addition to* the saved-address yes/no question.
  Prompts (both languages) state explicitly: in spoken conversations the
  first name is always confirmed before the order is submitted.

Live proof (opt-in, release-gating per SPEC):

- `PIZZA_LIVE_VOICE=1` + `PIZZA_LIVE_VOICE_URL=<https base url of the
  voice-capable deployment>`: a real headless browser drives the real
  page over HTTPS end to end — microphone capture via the fake media
  device streaming `order.de.wav` / `order.en.wav` (Chromium
  `--use-file-for-fake-audio-capture`), real STT through the deployed
  speech service, the transcript drives the chat, the confirm control
  places the order, and with the toggle ON the final assistant message
  fetches real TTS audio (response is non-empty browser-playable audio).
  The four acceptance points are then verified via the pizzeria's
  list+detail API endpoints. Not a text replay: if STT does not produce
  an order-driving transcript from the fixture, the test fails. Skipped
  cleanly when the env vars are unset; it cannot run on the current dev
  VPS (no speech service, no HTTPS) and is executed against the
  voice-capable deployment.

## C. Tickets (≤1h each)

1. Street-lookup core (client, Customer redaction split, tools, unit
   tests incl. redaction sweep). ☐ booleans-only lookup ☐ submit carries
   real street ☐ no saved-street text in events, logs or
   session.messages.
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
