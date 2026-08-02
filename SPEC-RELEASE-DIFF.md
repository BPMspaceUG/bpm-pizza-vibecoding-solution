# SPEC-RELEASE diff — v1.0.0 → v1.1.0

Generated file. Left side (`-`, red): the one-shot spec for release v1.0.0.
Right side (`+`, green): the one-shot spec for release v1.1.0.

The v1.1.0 additions: voice as a required release capability, the
saved-address privacy contract (street lookup with confirm-without-
disclosure), the ninth tool `lookup_customer`, the header read-aloud
toggle, a fifth acceptance point (a spoken order verifies like a typed
one), 5 → 10 golden transcripts, register 24 → 31 rules, plus two new
sections. One intentional tightening: in v1.1.0 the secure-context gate
covers both voice controls; in v1.0.0 only the microphone is gated on
the media APIs. Red lines outside these points are rewording between the
two independently authored files, not removed requirements.

Regenerate after any spec change with:

```
git -c core.pager=cat diff --no-index --no-color -U5 \
    --src-prefix=v1.0.0/ --dst-prefix=v1.1.0/ \
    SPEC-RELEASE-1.0.0.md SPEC-RELEASE-1.1.0.md || true
```

````diff
diff --git v1.0.0/SPEC-RELEASE-1.0.0.md v1.1.0/SPEC-RELEASE-1.1.0.md
index 0d92623..c2710b6 100644
--- v1.0.0/SPEC-RELEASE-1.0.0.md
+++ v1.1.0/SPEC-RELEASE-1.1.0.md
@@ -1,22 +1,22 @@
 # PizzaSim Ordering Agent — Specification
 
 > Hand this to a coding agent as the entire task:
-> `FOLLOW INSTRUCTIONS PRECISELY AT "SPEC-RELEASE-1.0.0.md"`.
-> This file is the source of truth for what the product is. Everything else —
-> code, tests, prompts, tickets — derives from it.
+> `FOLLOW INSTRUCTIONS PRECISELY AT "SPEC-RELEASE-1.1.0.md"`.
+> This file is the source of truth for what the product is. Everything else in
+> the repository — code, tests, prompts, tickets — derives from it.
 
 ---
 
 ## Where this format comes from
 
 The **shape** of this document is not ours. It is borrowed from Cedric Mössner —
 **The Morpheus** (<a href="https://www.youtube.com/@TheMorpheusTutorials" target="_blank">youtube.com/@TheMorpheusTutorials</a>),
 who writes exactly one specification file per project and hands the identical
 file to every new model in order to compare them. The prompt he sends alongside
-it is a single line — `FOLLOW INSTRUCTIONS PRECISELY AT "SPEC.MD"` — which is
-why a line like it, and not a long prompt, stands at the top of this file.
+it is a single line — `FOLLOW INSTRUCTIONS PRECISELY AT "<the spec file>"` —
+which is why that line, and not a long prompt, stands at the top of this file.
 
 Sections adopted from his specs: *Soul*, *The One Load-Bearing Idea*, hard
 *Scope In / Out*, an explicit autonomy clause, work *in passes* with
 verification after each, a file-level *Deliverables* list, *Decisions Locked /
 Deferred*, and the one-hour *ticket sizing rules*.
@@ -46,28 +46,35 @@ Concretely, and this is the acceptance criterion:
 2. Reading that pizzeria's orders back shows the order, and it is visible on
    that pizzeria's dashboard.
 3. The customer name is the one the customer gave.
 4. The items and quantities are the ones that were read back and confirmed —
    not a superset, not a subset, not a near match on the item code.
+5. **A spoken conversation on the web channel produces the same verified
+   outcome as points 1–4**: the customer speaks the order into the microphone,
+   the agent answers aloud, and the order that lands in the API is correct.
+   Voice is not a demo mode — it is a way to reach points 1–4.
 
 Nothing else counts as done. A green test suite, a clean architecture, a
 pleasant interface: none of it is the product. **The order on the board is the
 product.**
 
-**Four failures that look like success**, each a failed run and not a partial
+**Five failures that look like success**, each a failed run and not a partial
 one:
 
 - The order landed under a **different pizzeria** than the one the customer
   chose.
 - A retry after a timeout created the order **twice**.
 - A misheard or mistyped name created a **new customer** instead of matching
   the intended one.
 - The order was submitted **without the customer confirming** the read-back.
+- A **saved street address was disclosed** to whoever claimed the matching
+  first name — read out, printed on screen, written into a log, or handed to
+  the model.
 
 Every rule below — the state machine, the revision-bound confirmation, the ban
-on blind retries, the name read-back, the tenant in the URL path — exists to
-prevent exactly one of those four.
+on blind retries, the name read-back, the tenant in the URL path, the
+saved-address redaction — exists to prevent exactly one of those five.
 
 ---
 
 ## Soul
 
@@ -81,11 +88,12 @@ it feels confident. It works in the demo and fails on the fourth turn, in a
 noisy room, when the customer changes their mind.
 
 This agent puts the order back where it belongs: **in the code**. The model
 does the one thing it is genuinely good at — turning messy human speech into
 intent — and nothing else. It never holds the cart, never invents a menu item,
-and never reaches the kitchen without a confirmed read-back.
+never reaches the kitchen without a confirmed read-back, and never gets to see
+a returning customer's saved address.
 
 **Core belief:** a language model is a great waiter and a terrible order pad.
 
 ---
 
@@ -94,18 +102,21 @@ and never reaches the kitchen without a confirmed read-back.
 **The order is a state machine owned by the code. The model only speaks.**
 
 - Exactly one `Order` object per conversation, held by the runtime.
 - The model cannot write to it directly. It calls tools that request a
   transition, and every transition is validated before it is applied.
-- Every item code is validated against the **menu snapshot fetched for this
-  conversation**. An unknown code is a tool error carrying candidate matches —
-  never a silent guess, never a fallback to a hardcoded list.
+- Every item code is validated against the **live menu**. An unknown code is a
+  tool error carrying candidate matches — never a silent guess, never a
+  fallback to a hardcoded list.
 - `submit_order` is the only network write, legal in exactly one state:
   `CONFIRMED`. The only way into `CONFIRMED` is a read-back the customer
   answered yes to.
+- Data the customer never dictated — a street the code looked up on their
+  behalf — is copied **inside the code** and never passes through the model.
 - One core serves every channel. A transport carries words in and words out;
-  it owns no order logic whatsoever.
+  it owns no order logic whatsoever. Speech is a transport concern: it changes
+  how words arrive and leave, never what the order is.
 
 This one rule replaces prompt-engineering the model into good behaviour. If the
 model misbehaves, the state machine refuses — and the refusal is a tool result
 the model must deal with in front of the customer.
 
@@ -115,123 +126,134 @@ the model must deal with in front of the customer.
 
 ### In
 
 - **Two transports over one core:**
   - `cli` — interactive terminal chat.
-  - `web` — an HTTP server on port 8888, browser chat UI, streaming the
+  - `web` — FastAPI server on port 8888, browser chat UI, streaming the
     agent's intermediate steps as newline-delimited JSON so tool calls and
     tool results are visible, not just the final answer.
-- **Speech on the web transport**, served by a self-hosted CPU-only speech
-  container over HTTP, **optional in every sense**. See *Speech*.
+- **Voice on the web transport is a required product capability.** Push-to-talk
+  speech input and read-aloud speech output are served by the self-hosted
+  speech service described in *Speech*. A build whose voice path does not work
+  is not finished. If the service is unconfigured or unavailable at runtime,
+  ordering degrades to text-only without breaking ordering.
 - **Several pizzerias.** The customer chooses which one they are ordering
   from, and can change it. `PIZZERIA_ID` is the preselection, not a
   restriction.
+- **Returning customers.** A known first name may reuse its saved street after
+  exactly one explicit confirmation, and the address text is never disclosed to
+  the customer, the model, the page, or the logs. Reuse is limited to the
+  address held by the ordering API.
 - **Languages:** German and English. The agent answers in the language the
   customer used, per turn, without being told to switch.
 - **Menu, prices, cart, customer, submit.** The full happy path plus
   correction ("no, make that three"), removal, and abandonment. The customer
   can ask what is on offer and what items cost, and sees what the basket
   comes to before confirming.
-- **Deterministic tests** that run with no network and no LLM, plus one live
-  acceptance test and a browser end-to-end suite.
+- **Deterministic tests** that run with no network and no LLM, plus browser
+  end-to-end tests including the voice path, and opt-in live acceptance tests.
 - **Structured logging** of every turn: user text, model tool calls, tool
   results, state transitions. One line per event, JSON, to a file.
 
 ### Out (explicitly)
 
 - Payment and anything financial beyond showing prices the API supplies.
 - Delivery routing, or an ETA of our own invention.
 - Accounts, auth, sessions surviving a process restart.
 - Modifying or cancelling an order after it was submitted.
-- **Any reuse of customer data across conversations** — no customer-record
-  lookup, no offering an address a customer gave at some earlier point, no
-  filling any field from anything other than what was said in this
-  conversation. Every order collects its own name and, optionally, its own
-  street, every time.
 - Any regex or keyword parser that produces an order without the model.
   See **Anti-patterns**; this is a hard ban, not a style preference.
+- Reuse of a second saved address line: only the address field the order write
+  contract accepts may be reused. See *The PizzaSim API*.
+- Cross-session memory beyond saved-address reuse — "the usual" stays out.
+- Streaming speech, partial transcripts, barge-in, or turn detection.
 - Reading the whole menu aloud when the answer will be spoken.
 - Persisting customer data anywhere beyond the process and the PizzaSim API.
 
 ---
 
 ## Environment and configuration
 
 All configuration comes from environment variables. The process environment
-wins; otherwise read `~/.env` if it exists. Never write that file, never create
-it, never print a value from it.
+wins; otherwise `~/.env` is read if present. That file is **never written,
+never created, and no value from it is ever printed**.
 
-| Variable | Required | Purpose |
-|---|---|---|
-| `LITELLM_PIZZA_URL` | yes | OpenAI-compatible gateway base URL (`/chat/completions` appended) |
-| `LITELLM_PIZZA_KEY` | yes | Bearer token for the gateway |
-| `LITELLM_PIZZA_MODEL_1` | yes | Model the ordering agent calls; no default in code |
-| `LITELLM_PIZZA_MODEL_2` | no | Second configured model; read at startup, unused by this build — its absence must never fail the start |
-| `PIZZASIM_URL` | yes | PizzaSim API base URL; dashboard and docs links derive from it |
-| `PIZZASIM_API_KEY` | yes | Sent as header `X-API-Key` on protected routes |
-| `PIZZERIA_ID` | yes | UUID of the pizzeria preselected on first load |
-| `PIZZERIA_LANG` | yes | Initial language, exactly `de` or `en`, no default |
-| `APP_VERSION` | yes | Release version, `x.y.z`, shown in the web footer |
-| `SPEECH_URL` | no | Base URL of the self-hosted speech service |
-| `SPEECH_STT_MODEL` | no | Transcription model id |
-| `SPEECH_TTS_MODEL` | no | Synthesis model id |
-| `SPEECH_TTS_VOICE` | no | Voice id |
+| Variable | Purpose |
+|---|---|
+| `LITELLM_PIZZA_URL` | OpenAI-compatible gateway base URL (`/chat/completions` appended) |
+| `LITELLM_PIZZA_KEY` | Bearer token for the gateway |
+| `LITELLM_PIZZA_MODEL_1` | Model the ordering agent calls; required, no default in code |
+| `LITELLM_PIZZA_MODEL_2` | Second configured model, where the build uses one |
+| `PIZZASIM_URL` | PizzaSim API base URL; dashboard and docs links derive from it |
+| `PIZZASIM_API_KEY` | Sent as header `X-API-Key` on protected routes |
+| `PIZZERIA_ID` | UUID of the pizzeria preselected on first load |
+| `PIZZERIA_LANG` | Initial language, `de` or `en`: the greeting, the CLI, and the web UI before the customer switches |
+| `APP_VERSION` | Version, `x.y.z`, shown in the footer |
+| `SPEECH_URL` | Base URL of the self-hosted speech service |
+| `SPEECH_STT_MODEL` | Transcription model id |
+| `SPEECH_TTS_MODEL` | Synthesis model id |
+| `SPEECH_TTS_VOICE` | Voice id |
+
+That table is the complete set. Nothing outside this file is needed to know
+which values a deployment must supply.
 
 Rules:
 
 - **Nothing is hardcoded.** No UUID, no model name, no menu, no base URL, no
   vendor — not even as a fallback "just in case".
-- A missing or empty **required** variable must abort before the first turn,
-  with a message naming the variable and the file it was expected in. Never
-  start half-configured.
-- `PIZZERIA_LANG` must be exactly `de` or `en`. Any other value is a
-  configuration failure, not a silent fallback.
-- `APP_VERSION` must match `x.y.z` (three integers, dot-separated). Anything
-  else is a configuration failure at startup. Without a version nobody can
-  tell which build is answering, and a version nobody raises is worse than
-  none: patch for fixes, minor for new behaviour, major for a break.
-- The four `SPEECH_*` variables are the exception and they behave
-  **all-or-nothing**: speech is enabled only when all four are set *and* the
-  service answers a startup probe. Otherwise the speech features are simply
-  not rendered and everything else works unchanged.
+- A missing or empty **required** variable is a startup failure: the process
+  exits before the first turn with a message naming the variable and the file
+  it was expected in. Never start half-configured. Required are
+  `LITELLM_PIZZA_URL`, `LITELLM_PIZZA_KEY`, `LITELLM_PIZZA_MODEL_1`,
+  `PIZZASIM_URL`, `PIZZASIM_API_KEY`, `PIZZERIA_ID`, `PIZZERIA_LANG` and
+  `APP_VERSION`.
+- `PIZZERIA_LANG` must be exactly `de` or `en`; anything else is a startup
+  failure.
+- `APP_VERSION` must match `x.y.z` exactly (three dot-separated integers);
+  anything else is a startup failure. The version this specification describes
+  is `1.1.0`. It is raised on every release: patch for fixes, minor for new
+  behaviour, major for a break.
+- The four `SPEECH_*` variables are **required for a complete release** and
+  optional only for local development and for the explicit text-only test
+  scenario. When any of them is absent, the speech path is off, the voice
+  controls are not rendered, and text ordering must remain fully usable.
 - Secrets never appear in logs, transcripts, error messages or the web UI.
-- Ship a `.env.example` carrying **names only, never values**.
+- **Every dependency is pinned to an exact version** — no ranges, no "latest".
+  The stack is Python 3.11 or newer with: FastAPI and uvicorn for the web
+  channel, `httpx` as the single HTTP client everywhere, `python-multipart` for
+  the audio upload, `pytest` as the test runner, and a browser-automation
+  library able to launch a headless browser with a fake microphone device.
+  A `Procfile` starts the web channel via uvicorn, binding `0.0.0.0` and the
+  port from `PORT`, defaulting to 8888.
 
 ---
 
 ## The PizzaSim API (contract)
 
-The facts below are contract truth about the service this agent talks to. Treat
-them as given; confirm anything you doubt against the live service before you
-build the component that depends on it. A fact confirmed against the live
-service never moves back into the open list; the open list only shrinks.
+Facts below are **verified** — against running code or a live response. A
+verified fact never moves back into the open list; the open list only shrinks.
 
 | Call | Auth | Notes |
 |---|---|---|
-| `GET /menu` | public | returns `pizzas[]`, `pasta[]` and `toppings[]` |
-| `GET /pizzerias` | `X-API-Key` | `{"pizzerias": [{id, name, …}]}` |
-| `GET /pizzerias/{id}/orders` | `X-API-Key` | `{"orders": [...]}` — that pizzeria's orders, **without items** |
-| `GET /pizzerias/{id}/orders/{order_id}` | `X-API-Key` | the full order **incl. `customer` and `items[]`** |
+| `GET /menu` | public | returns `pizzas[]` and `pasta[]`, each with `code`, plus `toppings[]` |
+| `GET /pizzerias` | `X-API-Key` | list of pizzerias with `id`, `name` |
+| `GET /pizzerias/{id}/orders` | `X-API-Key` | that pizzeria's orders; used by timeout recovery |
+| `GET /pizzerias/{id}/orders/{order_id}` | `X-API-Key` | the full order incl. `customer` and `items[]` |
+| `GET /pizzerias/{id}/customers` | `X-API-Key` | customer list — used **only** for address-reuse lookup, never to disclose address text |
 | `POST /pizzerias/{id}/orders` | `X-API-Key` | places the order |
 | `GET /location?street=…` | public | street plausibility check (optional tool) |
 
-There is **no endpoint for looking a customer up**, and this agent must not
-behave as if there were.
-
 Order request body:
 
 ```json
 {
   "customer": { "first_name": "Marco", "street_one": "via di Cantieri" },
   "items": [{ "type": "pizza", "code": "margherita", "qty": 2, "extras": [] }]
 }
 ```
 
-`street_one` is optional: when the customer did not give a street, the key is
-**omitted from the body**, never sent as `null`.
-
-The response carries `order_id`, `status`, `eta_seconds`.
+Response carries `order_id`, `status`, `eta_seconds`.
 
 Derived URLs — built from `PIZZASIM_URL`, never hardcoded:
 
 - Dashboard of a pizzeria: `{PIZZASIM_URL}/dashboard/pizzerias/{id}`.
 - API documentation: `{PIZZASIM_URL}/swagger.html` — there is **no** `/docs`.
@@ -239,51 +261,66 @@ Derived URLs — built from `PIZZASIM_URL`, never hardcoded:
 Facts that shape behaviour:
 
 - The tenant is **always** in the URL path, never in a header. The API key is
   a server key, not a pizzeria id.
 - Customers are unique per pizzeria **by first name**. An unknown name
-  silently creates a new customer — a misheard name creates a ghost. Dictated
+  silently creates a new customer — a misheard name creates a ghost. Spoken
   input must therefore confirm the name explicitly.
 - `street_one` is optional and **not** validated for deliverability. Asking
   for it is a policy of this agent — never claim to have checked an address.
 - `POST /orders` is **not** idempotent. A retry after a timeout can double a
   real order. See **Error handling**.
+
+Further verified facts:
+
 - **Menu item shape:** `{"code", "name", "base": [ingredients], "price"}`.
-  `price` is a number in euros — the source for every price answer and for the
-  basket total; no other financial data exists in the API. `name` is a single
-  string, identical in DE and EN; there are no per-language names.
-- **`extras[]` is a controlled vocabulary:** the `toppings[]` array returned
-  by `GET /menu`. The server rejects an unknown extra with `422`
-  (`"items[0].extras contains invalid topping 'unicorn_dust'"`), so the tool
-  layer validates extras against `toppings[]` exactly like item codes. Extras
-  carry no price of their own; the basket must say so rather than imply a
-  charge it cannot compute.
+  `price` is a number in euros — the source for every price answer and the
+  basket total; no other financial data exists in the API. `name` is a
+  single string (identical in DE and EN; there are no per-language names).
+  The menu response also carries a top-level `toppings[]` array.
+- **`extras[]` is a controlled vocabulary:** the `toppings[]` from
+  `GET /menu`. The server rejects unknown extras with `422`
+  (`"items[0].extras contains invalid topping 'unicorn_dust'"`); the tool
+  layer validates extras against `toppings[]` exactly like item codes.
 - **Error bodies are machine-readable:**
-  `{"error": "<code>", "details": ["<human sentence>", …]}` — for example
-  `validation_failed` with HTTP `422`. Map them to typed errors; `details`
-  may feed a targeted question back to the customer.
-- **Order status values:** `ordered` → `prepared_planned` → `delivered`
-  (`delivered_at` set on the last). A fresh order starts as `ordered`.
-- **List-entry shape:** `{id, customer_id, created_at, ready_at, status,
-  delivered_at, first_name}`. `created_at` and `ready_at` are epoch seconds —
-  the remaining wait after a recovery is `ready_at` minus now, never below
-  zero. **The list carries no items.**
+  `{"error": "<code>", "details": ["<human sentence>", ...]}` (e.g.
+  `validation_failed` with HTTP 422) — mapped to typed errors; `details`
+  may feed targeted questions.
+- **Status values observed:** `ordered` → `prepared_planned` → `delivered`
+  (with `delivered_at` set on the last). A fresh order starts as `ordered`.
 - **`GET /location?street=` returns** `{"street": "<echo>",
-  "deliverable": <bool>}` with HTTP `200` — and answers `true` even for
-  nonsense input. It is a weak plausibility signal at best: never tell the
+  "deliverable": <bool>}`, HTTP 200 — `deliverable: true` even for nonsense
+  input, so it is a weak plausibility signal at best: never tell the
   customer an address was verified.
-- **Item codes are unique per type, not globally** — `tonno` exists as a pizza
-  *and* as a pasta, at different prices. Validation, pricing and removal
-  always key on `(type, code)`; a lookup by code alone is a defect.
+- **The list endpoint carries no items.** The detail endpoint
+  `GET /pizzerias/{id}/orders/{order_id}` returns the full order incl.
+  `customer` and `items[]`. Submit-timeout recovery shortlists by
+  `first_name` + `created_at` recency on the list, then **verifies the
+  candidate's items via the detail endpoint before adopting it**; the live
+  acceptance tests assert items and quantities through the same detail
+  endpoint.
+- **Item codes are unique per type, not globally** — `tonno` exists as a
+  pizza and a pasta. Validation and removal always key on `(type, code)`.
+- **The customers endpoint** `GET /pizzerias/{id}/customers` returns
+  `customers[]` with `{id, first_name, street_one, street_two, created_at,
+  deleted_at}`. Since customers are unique per pizzeria by `first_name`, a
+  first name resolves to at most one saved address. **A record with a
+  non-empty `deleted_at` does not exist**: the client filters it out before
+  any caller sees it, so a deleted customer is indistinguishable from an
+  unknown one. Guardrail: the verified order-write contract proves only
+  `street_one`, so address reuse **must** be limited to `street_one` until
+  `street_two` support on `POST /orders` is verified as well.
 
 ### Open contract questions — shrink-only
 
-Resolve against the live API before the affected component is implemented, then
-move the answer up into the facts and delete the question. Never guess. A fact
-confirmed against the live service never returns here.
+Resolve against the live API before the affected component is implemented,
+then move the answer up into the facts and delete the question. Never guess.
+A verified fact never returns here.
 
-*(empty — everything the build needs is in the facts above)*
+*(empty — every fact above is stated as verified. If the live API contradicts
+one, verify it against the live API and correct the fact; never work around it
+by guessing.)*
 
 ---
 
 ## Order state machine
 
@@ -296,163 +333,211 @@ EMPTY ──add_items──▶ COLLECTING ──set_customer──▶ READY
                                                CONFIRMED ──submit_order──▶ SUBMITTED
                                                     │
                                                     └──any change──▶ back to READY
 ```
 
-`set_customer` before any item is legal and leaves the order in `EMPTY`: the
-state is derived from the facts, not from the call order. After every legal
-mutation the code recomputes: no items → `EMPTY`; items but no customer →
-`COLLECTING`; items and customer → `READY`.
-
 Invariants, all enforced in code and all covered by unit tests:
 
 1. `submit_order` outside `CONFIRMED` returns an error. It does not
    "helpfully" confirm on the model's behalf.
 2. Any mutation after `CONFIRMED` drops the order back to `READY`. A
-   confirmation applies to the basket that was read back, not to a later one,
-   and it never survives the demotion.
-3. `CONFIRMED` is reachable only via `confirm_order`, which is legal only
-   after `read_back` for the **current** basket revision. The basket carries a
-   revision counter incremented on every mutation, and `confirm_order` must
-   name it; a stale number is refused.
+   confirmation applies to the basket that was read back, not to a later one.
+3. `CONFIRMED` is reachable only via `confirm_order`, which is only legal
+   after `read_back` for the current basket revision. The basket carries a
+   revision counter; `confirm_order` must name it, and the revision must be a
+   plain integer — a boolean is not an integer and is refused as stale.
 4. `SUBMITTED` is terminal. The conversation may continue; the order may not.
-   Every mutation attempt afterwards is refused with a speakable message.
-5. An item enters the basket only with a `(type, code)` present in the menu
-   snapshot fetched for this conversation.
+   Every mutating transition on a submitted order is refused with a spoken
+   sentence offering to start a new order.
+5. An item enters the basket only with a `code` present in the menu snapshot
+   fetched this session.
 6. A basket never crosses a tenant boundary. Changing pizzeria starts a fresh
    conversation and a fresh order.
+7. **Any mutation voids an unverified submit attempt.** When a submit timed
+   out and the outcome is unknown, and the basket then changes, the pending
+   "did it go through?" bookkeeping is cleared: the recovery correlation
+   belongs to the basket that was confirmed then, not to whatever the basket
+   becomes now.
 
-Basket mechanics, all normative:
-
-- Two added lines merge only when `(type, code, sorted(extras))` match
-  exactly. The same code with different extras is a separate line.
-- The timestamp of the first submit attempt is recorded once and only once,
-  and is used solely by timeout recovery.
-- Any legal mutation clears the recovery bookkeeping of an unverified submit
-  attempt. That correlation belongs to the basket that was confirmed then, not
-  to whatever the basket becomes now.
+Every legal mutation raises the revision counter and recomputes the state from
+the data: no items → `EMPTY`, items but no customer → `COLLECTING`, items and
+customer → `READY`.
 
 ---
 
 ## Tools
 
-The model sees exactly these eight. Names, parameters and semantics are fixed,
-and no ninth tool is added for convenience.
+The model sees exactly these nine tools. Names, parameters and semantics are
+fixed; nothing else is exposed to the model.
 
 | Tool | Parameters | Returns |
 |---|---|---|
-| `get_menu` | — | pizzas and pasta with codes, display names, prices, plus the available toppings |
-| `add_items` | `items[]` of `{type, code, qty, extras[]}` | new basket snapshot |
-| `remove_item` | `type`, `code`, optional `qty` | new basket snapshot |
-| `set_customer` | `first_name`, optional `street_one` | customer as stored + snapshot |
-| `read_back` | — | the complete order as it stands, incl. the code-computed total |
+| `get_menu` | — | pizzas and pasta with codes, display names, prices, plus the available extra toppings |
+| `add_items` | `items[]` of `{type, code, qty, extras[]}` | new basket + revision |
+| `remove_item` | `type`, `code`, optional `qty` | new basket + revision |
+| `lookup_customer` | `first_name` | `{customer_exists, saved_street_available}` — **booleans only, never street text** |
+| `set_customer` | `first_name`, plus either `street_one` **or** `use_saved_street: true` (mutually exclusive) | customer as stored (a saved street appears as a flag, never as text) |
+| `read_back` | — | basket, customer name, revision, and the code-computed basket total — the text the agent reads out |
 | `confirm_order` | `revision` | state `CONFIRMED`, or an error if stale |
 | `submit_order` | — | `order_id`, `status`, `eta_seconds` |
-| `check_street` | `street` | plausibility result (optional, never a guarantee) |
-
-`type` is constrained to `pizza` or `pasta` in the schema; `qty` is an integer
-with minimum 1.
+| `check_street` | `street` | plausibility result (optional) |
 
 Tool result conventions:
 
 - Success: the **full current state**, not a diff. Every successful result
-  embeds the same snapshot object:
-
-  ```json
-  {"state": "READY", "revision": 3,
-   "items": [{"type": "pizza", "code": "margherita", "name": "Margherita",
-              "qty": 2, "extras": [], "unit_price": 8.5, "line_total": 17.0}],
-   "basket_total": 17.0,
-   "customer": {"first_name": "Marco", "street_one": null},
-   "read_back_done": false}
-  ```
-
-  The model never reconstructs the basket from conversation history.
-- Failure: `{"error": {"code": "…", "message": "…", "candidates": […]}}`.
-  `message` is written so it can be **spoken to the customer as-is** — plain
-  language, no status code, no field path, no JSON. `candidates` is an array,
-  empty when there is nothing to suggest.
-- The error codes are fixed: `unknown_item`, `invalid_extra`,
-  `invalid_quantity`, `empty_basket`, `not_in_basket`, `invalid_state`,
-  `stale_revision`, `read_back_required`, `order_closed`, `api_unavailable`,
-  `submit_unknown`, `submit_failed`, `unknown_tool`.
-- **Dispatch never raises.** Every failure — menu, state machine, API, unknown
-  tool name — comes back as a tool result the model must deal with in front of
-  the customer. An exception escaping the tool layer is a defect.
-- `add_items` with an unknown code returns `unknown_item` plus **at most three**
-  candidates from the menu snapshot, preferring the requested type and falling
-  back to the other type so "pizza tonno" asked as a pasta still helps. The
-  model asks; it does not pick.
-- **`add_items` is atomic.** If any item, extra or quantity in the call is
-  invalid, the whole call is rejected and the basket is untouched. A partial
-  add is a defect.
-- An unknown extra returns `invalid_extra` with up to three topping
-  candidates, in the same shape.
-- Quantities are integers. A tool receiving `"zwei"` returns
-  `invalid_quantity`; it does not parse German. Booleans are not integers.
-- **Totals are computed in code only.** The unit price is copied from the menu
-  snapshot **at add time** into the basket line; line totals and the basket
-  total are computed with exact decimal arithmetic and rounded to cents once,
-  half-up — never by accumulating binary floats, and never by the model. The
-  web basket shows the same code-owned total that `read_back` carries.
-- `remove_item`'s parameters are fixed, so when several basket lines share
-  `(type, code)` with different `extras[]` the semantics must be
-  deterministic: **without `qty` every matching line is removed; with `qty`
-  the most recently added matching line is reduced**, and removed entirely
-  when `qty` reaches or exceeds its quantity. The full snapshot in the result
-  lets the model repair anything else by remove and re-add.
-- `confirm_order` with a non-integer revision is refused exactly like a stale
-  one.
-- `check_street` returns the echoed street and a boolean. It is a courtesy,
-  never a precondition, and its `true` means nothing.
+  embeds the complete snapshot — state, revision, item lines with unit price
+  and line total, basket total, customer, and whether the current revision has
+  been read back. The model never reconstructs the basket from history.
+- Failure: `{"error": {"code": "...", "message": "...", "candidates": [...]}}`.
+  `message` is written so it can be spoken to the customer as-is.
+- **Dispatch never raises.** Every failure — an invalid transition, a menu
+  error, an API error — comes back as a tool result the model must deal with in
+  front of the customer. API failures map to `api_unavailable` with a spoken
+  sentence.
+- `add_items` with an unknown code returns `unknown_item` plus up to three
+  candidates from the menu, matched within the requested type first and the
+  other type as fallback. The model asks; it does not pick.
+- **`add_items` is atomic.** If any item or extra in the call is unknown, the
+  whole call is rejected and the basket is unchanged. A partial add never
+  happens.
+- Quantities are integers ≥ 1. A tool receiving `"zwei"` returns
+  `invalid_quantity`; it does not parse German. A boolean is not an integer.
+- **Totals are computed in code**, from the API prices captured in the
+  session's menu snapshot, in exact decimal arithmetic rounded to cents
+  (half-up) — never by accumulating floats. The model never does arithmetic on
+  prices; the web basket shows the same code-owned total that `read_back`
+  carries. The unit price is copied onto the basket line at add time.
+- `remove_item` parameters are fixed, so when several basket lines share
+  `(type, code)` with different `extras[]`, the semantics are
+  deterministic: without `qty` every matching line is removed; with `qty`
+  the most recently added matching line is reduced, and removed entirely if
+  `qty` covers it. The full snapshot in the result lets the model repair
+  anything else by remove + re-add.
+- `lookup_customer` matches the first name case-insensitively against the
+  pizzeria's customer list and returns **exactly two booleans plus the
+  snapshot**: whether a customer with that name exists, and whether that
+  customer has a saved street. It **never** returns the street, a masked form
+  of it, its length, or any other derivative. An empty name returns
+  `invalid_arguments`.
+- **A failing `lookup_customer` is not fatal.** If the customer list cannot be
+  fetched, the tool returns `api_unavailable` and the conversation continues by
+  asking for the street as usual. Address reuse is a convenience; losing it
+  must never lose the order.
+- `set_customer` accepts a dictated `street_one` **or** `use_saved_street:
+  true`, and **never both**: passing both returns `invalid_arguments` with a
+  spoken sentence. With the flag set and no saved street behind that name, it
+  returns `no_saved_street` and asks for the street. With the flag set and a
+  saved street present, **the code copies the street into the order** and
+  simultaneously adopts the **canonical first-name casing from the stored
+  record** — so `marko` reuses Marko's address under the name `Marko` and does
+  not create a near-duplicate ghost customer.
+- `read_back` refuses on an empty basket and refuses while no customer is set,
+  each with a sentence that says what is still missing.
+- `check_street` is a plausibility signal only. Its result may never be
+  presented as a deliverability guarantee.
+
+---
+
+## The saved-address privacy contract
+
+A returning customer's street is the one piece of data in this product that the
+customer did **not** dictate in this conversation. It is therefore governed by
+its own rule, and that rule outranks convenience everywhere.
+
+**The threat.** Customers are keyed by first name alone. There is no password,
+no PIN, no second factor. Anyone who claims a common first name would otherwise
+be able to make the agent read a stranger's home address out loud. **The first
+name is a lookup key, never an authentication.**
+
+**Two serializations, one redaction rule.** The customer record inside the
+order has exactly two representations, and the difference between them is the
+whole contract:
+
+| View | Who sees it | Saved street |
+|---|---|---|
+| **Redacted view** | every tool result, every streamed event, every model-visible message, the web UI, the transcripts, the structured logs | `street_one: null` plus `street_on_file: true` |
+| **Submit view** | the outbound `POST /pizzerias/{id}/orders` body, and nothing else | the real street text |
+
+- The redacted view is the **only** view that feeds the snapshot, and the
+  snapshot is embedded in every successful tool result — so the redaction is
+  structural, not a filter someone has to remember to apply.
+- The submit view is built **only** when the order write is assembled. There is
+  no other caller, and no code path may add one.
+- **The outbound submit payload is the only legal occurrence of the saved
+  street text anywhere in a run.** Not in a snapshot, not in an emitted event,
+  not in a log line, not in the model's message history, not on the page.
+- Only `street_one` is ever reused. A stored second address line is never read,
+  never copied, never sent, because the verified write contract does not
+  accept it.
+- **A street the customer dictated in this conversation is not covered by this
+  rule.** It is their own input, arriving in their own turn; it is echoed,
+  read back and stored exactly as given. The redaction exists for data the
+  code fetched on the customer's behalf, not for data the customer just said.
+- **The agent never recites a saved address, in any form** — not in the
+  confirmation question, not in the read-back, not in the closing summary, not
+  as a partial hint ("your address on Meyer street, correct?").
+- Where the interface must show that an address exists, it shows a **localized
+  label** — "gespeicherte Adresse" in German, "saved address" in English —
+  and never the text.
+- The redaction is a **testable claim, not a promise**: a string-scanning
+  end-to-end test drives a full saved-address order and asserts the street text
+  appears in the captured submit payload and in nothing else. See *Testing*.
 
 ---
 
 ## Conversation policy
 
 This is what the system prompt must produce. Write the prompt to achieve it;
-do not paste this section into it verbatim. One prompt file per language, with
-the pizzeria name substituted into it at session creation.
+do not paste this section into it verbatim.
 
-- Greet first, in the session language, one sentence, offering help — not a
+- Greet first, in the session language, and offer help — one sentence, not a
   menu recital.
 
 **Language authority — one rule.** The session language starts as
 `PIZZERIA_LANG` (greeting, CLI, web UI chrome before any switch). The web
-header switch changes the session language: UI chrome, the greeting of a fresh
-conversation, and the speech hint (STT language, TTS output). For the agent's
-replies, **per-turn mirroring wins**: it answers in the language of the
-customer's latest message, even when that differs from the session language,
-and it never comments on the switch. The CLI has no switch and stays at
-`PIZZERIA_LANG`.
+header switch changes the session language: UI chrome, the greeting of a
+fresh conversation, and the language sent with every speech request in both
+directions. For the agent's replies, per-turn mirroring wins: it answers in the
+language of the customer's latest message, even when that differs from the
+session language. The CLI has no switch and stays at `PIZZERIA_LANG`.
 
 - **One question per turn.** Never stack "name, street and what would you
   like?"
 - Never state a menu item or a price that did not come from `get_menu` in this
-  conversation. Price questions are normal questions, and so is "what does my
-  basket come to?" — quote `price` and `basket_total` verbatim from tool
-  results and never do the arithmetic in the reply.
-- Collect the first name and the street. If the customer declines the street,
-  accept it and move on — it is optional in the API.
-- **Repeat the first name back once to confirm it** before submitting. A
-  misheard name silently creates a customer nobody will find again.
+  session. Price questions are normal questions, and so is "what does my
+  basket come to?" Prices and the basket total are quoted verbatim from tool
+  results; the agent never computes an amount.
+- Collect the first name; **then** call `lookup_customer`. If a saved street
+  exists, ask **exactly one** confirmation question — "Soll ich wieder an Ihre
+  gespeicherte Adresse liefern?" / "Shall I deliver to your saved address
+  again?" — **without reciting the address**. On an explicit yes, call
+  `set_customer` with `use_saved_street: true`. If the customer declines, is
+  unknown, or the lookup failed, ask for the street as usual. If the customer
+  declines the street entirely, accept it — it is optional in the API.
+- **Confirm the first name.** Repeat it back once. A misheard name silently
+  creates a ghost customer nobody will find again. **In spoken conversations
+  the name must always be confirmed before the order is submitted, and the
+  saved-address question never substitutes for that confirmation** — they are
+  two different questions answering two different risks.
 - Before submitting: call `read_back`, present it, and wait for an explicit
   yes. "Mhm" and silence are not a yes; ask once more, then offer to start
   over.
 - Never announce that an order was placed before `submit_order` returned an
   `order_id`.
 - On success, state the order id in groups a human can repeat back, and the
   wait time in **minutes**, converted from `eta_seconds`.
 - On error, explain in plain language what happened and what the options are.
-  Never show a status code, a stack trace or JSON.
+  Never show a status code, stack trace or JSON.
 - Never claim to have checked an address for deliverability.
-- Pass quantities to tools as numbers, always.
-- **The customer's data comes from this conversation and nowhere else.** The
-  agent never offers a name or an address it was not told here, and never
-  implies it knows the customer already.
+- When a reply will be spoken aloud: at most three dishes plus an invitation to
+  ask for more, times in minutes, order ids in groups, short sentences.
 - When a tool reports an error, follow it: offer the named alternatives or ask
-  the missing question. The system is right and the model is not.
+  the missing question. The system is always right.
+
+The prompt exists in one file per language, rendered with the pizzeria name at
+session creation. Switching the language re-renders the same policy in the
+other language in place; the conversation history is preserved.
 
 ---
 
 ## The web channel
 
@@ -479,11 +564,11 @@ codes are part of the contract and the browser code depends on them:
 | `POST /speech/tts` | `{session_id, text}` | audio bytes |
 
 Status codes, all normative:
 
 - `404` — **unknown session** on any session-bound route, and every speech
-  route while speech is disabled.
+  route while speech is unavailable.
 - `409` — the requested pizzeria is unknown or gone at session creation, and
   a turn already in progress for that session.
 - `422` — `lang` outside `de|en`; a non-integer `revision`; an empty (but not
   absent) chat text; an empty text to synthesise.
 - `502` — the speech service failed a request.
@@ -494,11 +579,11 @@ Status codes, all normative:
 - `pizzerias` is fetched from the live API **on every call**. On failure it is
   `null` — never an empty list, never a bundled fallback — and the UI must
   then say the list is unavailable instead of offering a choice it cannot
   honour.
 - `speech` is a boolean and is the **only** signal the page uses to decide
-  whether speech exists at all.
+  whether the speech path exists at all.
 - `dashboard_base` and `docs_url` are derived from the API base URL and never
   written into the page's source.
 
 `/health` details: `api` is measured live per request against the ordering API;
 `gateway` is the **process-wide last-known** status set by real model calls
@@ -510,13 +595,19 @@ a health check nobody can afford to poll.
 `spoken: true` marks a turn that arrived by microphone.
 
 Both streaming routes emit newline-delimited JSON, one object per line, with
 these event kinds: `user`, `tool_call`, `tool_result`, `state`, `assistant`,
 `error`, and a final `done` carrying the full order snapshot. The last line of
-every stream is `done` — including streams that failed. The same events, plus
-a `language` event for a switch, are written to the session's log file; the log
-is a superset of the stream and never carries a configuration value.
+every stream is `done` — including streams that failed. `done` is a transport
+event only: it is emitted to the stream and is **never** written to the session's
+log file. The log carries the events a turn explicitly logs — the `user`,
+`tool_call`, `tool_result`, `state`, `assistant` and `error` records the stream
+also shows — and additionally a `language` event for a switch, which the stream
+never carries. Neither side is a superset of the other: they overlap on the
+explicitly logged turn events, the stream alone carries `done`, and the log alone
+carries `language`. The log never carries a configuration value or a saved
+address.
 
 Turns are **serialized per session** by a lock the transport holds for the
 whole stream. A second turn arriving while one is running is refused with
 `409`, not queued and not run concurrently.
 
@@ -525,90 +616,111 @@ dispatches `confirm_order` and, only if that succeeded, `submit_order` — both
 recorded in the conversation exactly like model-issued calls, with synthetic
 assistant tool-call messages and tool results — and then runs one **normal**
 model turn to phrase the outcome. Same gateway path, same retry, same apology
 behaviour as any other turn. Success and failure travel the same road.
 
+The two speech routes are proxies and nothing more: they forward the session's
+language to the speech service and hand the result back. They hold no order
+logic, and while the speech path is unavailable they do not exist as far as the
+page is concerned.
+
 ### The conversation
 
 Type or paste a message, get an answer. The exchange a first-time customer
 should be able to have, end to end, without help:
 
 > *What have you got?* → *What does a Margherita cost?* → *I'll take two of
 > those and a pasta* → *I'm a new customer, my name is …* → read-back →
 > confirm → order id and wait time.
 
+The same exchange must be possible spoken, using the microphone control and
+read-aloud, with no typed input except where the customer chooses to type.
 After a completed order, a new conversation can start immediately from the
 same page.
 
 ### Header
 
-- **The pizzeria being ordered from, by name**, prominent and always visible,
-  and used as the page title.
+- **The pizzeria being ordered from, by name**, prominent and always visible.
 - **A selector to change pizzeria, filled from the API and from nowhere
-  else.** No hardcoded names, no bundled list, no fallback entry when the call
-  fails — if it fails, the page says the list is unavailable instead of
-  offering a choice it cannot honour. Each entry shows the name plus a short
-  form of its UUID so similar names can be told apart. Changing the selection
-  starts a fresh conversation for that pizzeria.
-- **A link to that pizzeria's dashboard**, opening in a new tab. Without it
-  nobody can check whether the order arrived — and checking that is the entire
-  point of the product.
-- **Language: German or English**, switchable, applied to the UI chrome
-  immediately and to the session language on the server.
-- **Start over**, clearing the conversation and the basket by creating a new
-  session for the same pizzeria.
+  else.** No hardcoded names, no bundled list, no fallback entry when the call fails — if it
+  fails, the page says the list is unavailable instead of offering a choice
+  it cannot honour. Each entry shows the name plus a short form of its UUID
+  so similar names can be told apart. Changing the selection starts a fresh
+  conversation for that pizzeria.
+- **A link to that pizzeria's dashboard**
+  (`{PIZZASIM_URL}/dashboard/pizzerias/{id}`), opening in a new tab. Without
+  it nobody can check whether the order arrived — and checking that is the
+  entire point of the product.
+- **Language: German or English**, switchable, applied to the agent's replies
+  and to speech in both directions.
+- **A read-aloud toggle, rendered as a speaker icon**, and it lives **in the
+  header, between the language switch and Start over** — read-aloud is a
+  session preference like the language, not a per-message action, so it
+  belongs with the other session controls and not in the composer. Its
+  required behaviour:
+  - It is a real button, reachable by keyboard, and **operable with both
+    Space and Enter**.
+  - It carries `aria-pressed`, which is `false` on load: **read-aloud is off
+    by default** and every page load starts silent.
+  - Its `title` and `aria-label` carry the same localized sentence ("Antworten
+    vorlesen" / "Read replies aloud"), which follows the language switch
+    immediately. **Changing the language must never change the pressed
+    state** — localization and state are independent.
+  - Its icon reflects the state (speaker on / speaker muted).
+  - It is **rendered only when voice is usable** (see *Speech*); otherwise it
+    is not on the page at all.
+- **Start over**, clearing the session and the basket.
 
 ### Footer
 
-- **The running version**, `x.y.z`, from `APP_VERSION`.
+- **The running version**, `x.y.z`, from `APP_VERSION`. Without it nobody can
+  tell which build is answering.
 - **The full pizzeria UUID**, selectable, for pasting into API calls.
-- **Connection state** for the ordering API and the model gateway, as two
-  badges carrying their state (`ok`, `down`, `unknown`), polled on a fixed
-  interval. A failed poll leaves the last known state on screen rather than
-  inventing a green one.
-- **A link to the API documentation**, opening in a new tab.
+- **Connection state** for the ordering API and the model gateway, refreshed
+  periodically. The gateway badge reports the process-wide outcome of real
+  gateway calls; the health check itself never calls the gateway just to
+  colour a badge.
+- **A link to the API documentation** (`{PIZZASIM_URL}/swagger.html`).
 
 ### Every message gets an answer
 
 The invariant this channel stands on: **no sent message may end without either
-a rendered assistant reply or a rendered error.** Never a silent failure, never
-an indicator that stops with nothing after it.
+a rendered assistant reply or a rendered error.** Never a silent failure,
+never an indicator that stops with nothing after it.
 
-- The moment a message is sent, the UI shows the agent is working, and the
-  send control is disabled until the turn ends.
+- The moment a message is sent, the UI shows the agent is working.
 - Intermediate steps render as they stream — which tool was called and what it
-  returned — visually distinct from the assistant's words and collapsed by
-  default. **A stream whose tool events the page discards is a defect:** the
-  customer sees a frozen screen while the agent works normally.
+  returned — visually distinct from the assistant's words. A stream whose tool
+  events the page discards is a defect: the customer sees a frozen screen
+  while the agent works normally.
 - If the stream ends without a final assistant message, the UI says so and
   offers to resend.
+- **The client timeout covers the streamed body, not only the response
+  headers.** A stream that stalls halfway must actually time out, so the
+  timeout notice and its resend control can occur at all.
 - If the request errors, times out, or the connection drops, the UI says which
-  of those happened and offers to resend. The timeout must be a **real
-  client-side timeout covering the streamed body**, not only the initial
-  response — otherwise a stream that stalls forever produces the one thing
-  this invariant forbids: a spinner with nothing after it.
+  happened and offers to resend.
 - A `409` (turn already running) is shown as a short, plain "one moment"
   notice — it is not an error and offers no resend.
 - Errors in the customer's language, in plain words. No status codes, no
   tracebacks, no raw JSON.
+- **Nothing in the text UI may depend on a browser API that exists only in a
+  secure context.** Typed ordering must work fully over plain HTTP, and it must
+  keep working when the voice controls are absent or have been withdrawn.
 
 ### The order on screen
 
-- The current basket is always visible, with quantities, line totals and what
-  it comes to. The code owns the order; the customer must see what the code
-  holds. Every snapshot that arrives in the stream re-renders it.
-- When any line carries extras, the panel states that extras are not priced
-  separately — an unexplained line total invites the belief that the total is
-  wrong.
+- The current basket is visible, with quantities and what it comes to. The
+  code owns the order; the customer must see what the code holds.
 - The read-back is visually distinct and carries an explicit confirm control.
-  **Confirmation is an action the customer takes, not a word the agent claims
-  to have heard.** The control carries the exact revision that was read back,
-  and any earlier read-back's control is disabled the moment a newer one
-  appears.
+  Confirmation is an action the customer takes, not a word the agent claims to
+  have heard. Older read-back panels are disabled as soon as a new one appears.
+- A customer whose street came from saved data is shown with the localized
+  "saved address" label and never with the address text.
 - On success: the order id, readable, and the wait in minutes.
-- After submission the basket is locked and shown as submitted, carrying the
-  order id. Nothing on the page can modify or resubmit it.
+- After submission the basket is locked and shown as submitted. Nothing on the
+  page can modify or resubmit it.
 
 ### Sessions and tenancy in the browser
 
 - **Switching pizzeria creates the new session first**, and only then aborts
   any in-flight stream and clears the conversation. If creation fails, the
@@ -622,221 +734,316 @@ an indicator that stops with nothing after it.
   a new, empty order, so the old revision means nothing.
 - **A failed confirm is retried with the same revision**, never a new one. If
   the first attempt did go through, the state machine refuses the retry and
   the agent says so. A retry can therefore never place a second order.
 - The page holds exactly one session at a time and sends only identifiers to
-  the server. It never computes a total, never decides a state, and never
-  keeps its own copy of the basket.
+  the server. It never computes a total, never decides a state, never keeps
+  its own copy of the basket, and never holds a customer's saved address.
 
 ---
 
 ## Speech
 
-Speech is an input and an output method on the web channel, served by a
+Voice is an input and an output method on the web channel, served by a
 **self-hosted speech service**: CPU-only, in its own container, reached over
-plain HTTP with an OpenAI-compatible surface.
+HTTP with an OpenAI-compatible surface.
 
 | Direction | Endpoint | Payload |
 |---|---|---|
-| STT | `POST {SPEECH_URL}/v1/audio/transcriptions` | multipart audio + model + language |
-| TTS | `POST {SPEECH_URL}/v1/audio/speech` | JSON: model, voice, input text, language → audio |
-
-- **Speech is never required.** With the `SPEECH_*` variables unset, or the
-  service not answering at startup, the microphone and the read-aloud toggle
-  are not rendered, the speech routes answer `404`, and the text UI is fully
-  usable — including placing a complete order. A speech failure is never an
-  order failure, and no part of the ordering path may depend on speech being
-  present.
-- **All-or-nothing enablement.** Speech counts as available only when the base
-  URL and all three model/voice ids are configured **and** a short startup
-  probe against the service returned `2xx`. A half-configured speech stack is
-  treated exactly like an absent one, and it says so on standard error rather
-  than failing the process.
+| STT | `POST {SPEECH_URL}/v1/audio/transcriptions` | multipart: the recorded audio file, the model id, the language → `{"text": …}` |
+| TTS | `POST {SPEECH_URL}/v1/audio/speech` | JSON: model, voice, input text, language → audio bytes |
+| Probe | `GET {SPEECH_URL}/v1/models` | any 2xx means alive |
+
 - **The speech service is the only speech path.** No external speech provider,
-  no hosted realtime framework, no audio through the model gateway — that
+  no hosted realtime framework, no audio through the LLM gateway — that
   gateway carries chat completions only.
 - **The browser captures and plays audio; it does not recognise or synthesise
-  it.** Capture with `getUserMedia` and `MediaRecorder`, playback through a
-  plain audio element. Recognition and synthesis happen server-side.
+  it.** Capture via `getUserMedia` and `MediaRecorder`, playback via a plain
+  audio element — cross-browser and cross-platform, on Linux, macOS and
+  Windows alike.
 - **The browser speech APIs are forbidden.** `SpeechRecognition` and
   `speechSynthesis` tie the product to a single browser vendor and send
-  customer audio to a third party. The self-hosted service exists to replace
-  them.
-- **The page must survive plain HTTP.** Whether speech exists at all is
-  decided solely by the server's `speech` flag. Only the **microphone** is
-  additionally gated, and only on the two capabilities it actually needs —
-  `navigator.mediaDevices` and `MediaRecorder`. Read-aloud must therefore
-  keep working on a page served over plain HTTP where capture is unavailable;
-  gating the whole speech UI on one browser capability check silently kills
-  output too, and that is a defect.
+  customer audio to a third party. The self-hosted service exists so that
+  neither is ever needed.
 - **Nothing about the speech stack is written into source.** Base URL, models
-  and voice come from the environment, exactly like the chat model; the
-  language sent with STT and TTS requests is the session language (see
-  *Language authority* under *Conversation policy*), not a separate
-  configuration value.
+  and voice come from the environment, exactly like the chat model. The
+  language sent with every STT and TTS request is the session language — there
+  is no separate speech-language setting.
+- **Enablement is all-or-nothing, and it is probed.** The speech path counts as
+  available only when `SPEECH_URL`, both model ids and the voice id are all
+  configured **and** the service answered the startup probe with a 2xx. Three
+  of four variables set is off, not partly on. While it is off, both speech
+  endpoints answer `404`; a speech request that fails once the service is up
+  answers `502`.
 - **Request/response, not streaming.** Record, upload, transcript back.
-  Latency is visible and acceptable; do not build partial results, barge-in or
-  turn detection on top — this transport cannot do them, and pretending
+  Latency is visible and acceptable; do not build partial results, barge-in
+  or turn detection on top — this transport cannot do them, and pretending
   otherwise produces a broken feel.
-- **Push-to-talk.** The microphone starts and stops on the customer's action
-  and never listens continuously. The recording state is visible at all times
-  and exposed to assistive technology.
-- **Synthesis is optional and off by default**, toggled by the customer,
-  applied **only to the final assistant message** of a turn — never to
-  intermediate steps, never to notices.
-- A transcription that comes back empty, or a speech request that fails,
-  leaves a plain notice on the page and the text input untouched. Denied
-  microphone permission says so and changes nothing else.
+- **Push-to-talk.** The microphone control sits in the composer next to the
+  text field. Recording starts and stops on the customer's action and never
+  listens continuously; the recording state is visible at all times and is also
+  exposed as `aria-pressed`. When the transcript comes back empty, the page
+  says it did not catch that and the turn is not sent.
+- **A spoken turn is marked as spoken**, and the marking is **ephemeral**: the
+  spoken-style instruction is attached to that one request only and is never
+  written into the conversation history. A later typed turn must not inherit
+  the spoken constraints.
+- **Synthesis is optional and off by default**, toggled by the customer in the
+  header, and **applied only to the final assistant message of a turn** — never
+  to intermediate steps, never to tool output, never once per streamed event.
+  A turn containing several tool calls and one final message produces exactly
+  one synthesis request.
+- **Voice controls are rendered only in a secure browser context, and that
+  check lives in the UI.** The page renders the microphone and the read-aloud
+  toggle only when the speech path is available **and** the browser reports a
+  secure context (HTTPS, or localhost during development), and the microphone
+  only when the browser's capture APIs exist as well. Over plain HTTP the page must
+  present **no** voice-capable UI at all, even when the server is fully
+  configured for speech — a microphone button that cannot work is worse than no
+  button. Documenting the HTTPS requirement is not a substitute for the check.
+- **Runtime degradation.** If a speech request fails while the customer is
+  using it, the page says so in plain language and **hides both voice controls
+  for the rest of the session**, while typed ordering continues untouched. A
+  speech outage must never block ordering.
+- **Voice is a required product capability for release completeness.**
+  Text-only is the degraded fallback when speech is unconfigured in
+  development or temporarily unavailable at runtime: microphone and read-aloud
+  toggle are then not rendered and the text UI is fully usable. A release
+  without a working voice path is not done.
+- **Transport formats:** the STT path accepts the browser-recorded audio format
+  emitted by `MediaRecorder`; the TTS path returns audio playable by a standard
+  browser audio element, and the response's own content type is what the page
+  plays.
+- **Latency:** each STT and each TTS request should complete quickly enough for
+  turn-based conversation on modest hardware; sustained multi-second delays
+  that make turn-taking awkward are a defect.
 - **Speech shortens answers, it does not change them.** Same core, same tools,
-  same state machine. When a reply will be spoken, the turn carries an
-  **ephemeral** instruction to that effect: at most three dishes plus an
-  invitation, times in minutes, order ids in groups, short sentences. That
-  instruction must **never** be persisted into the conversation history — a
-  later typed turn must not inherit the spoken constraints.
+  same state machine, same order.
 - **Confirm the name.** Transcription errors on names are the expensive
   failure: a misheard name silently creates a customer nobody will find again.
-  Read the name back before submitting.
+  In spoken conversations the name is read back and confirmed before
+  submission, always.
+
+### Speech service provisioning
+
+The deployment includes a self-hosted, CPU-only speech service reachable at
+`SPEECH_URL`, exposing the OpenAI-compatible endpoints in the table above. The
+application and the speech service are deployed together as first-party
+artifacts, and the repository carries a **neutral deployment definition** for
+the service next to the application's deployment artifacts.
+
+Neutral means exactly this, and it is a hard rule:
+
+- **No real image name, no real engine or model name, no real voice name, and
+  no host name appears in a production-facing artifact — source, this
+  specification, or any deployment file.** The image, the models and the voice
+  are operator configuration supplied through the environment, exactly like the
+  chat model. One exemption, and only this one: the offline test harness may use
+  opaque local stub identifiers (`scripted-stub`, `stub-stt`, `stub-tts`,
+  `stub-voice` and the like) that name no real vendor, engine, model or voice.
+  They are fixtures that let tests run without a network; no production-facing
+  artifact may read one, default to one, or ship one.
+- The definition states the required **interface** — the two endpoints, the
+  probe endpoint, an HTTP port, CPU-only resources with no accelerator
+  reservation — and nothing about which implementation satisfies it.
+- Nothing in the repository may recommend, default to, or hint at a particular
+  engine.
+- **A voice-capable deployment serves the application over HTTPS on a real host
+  name.** Microphone capture does not exist on plain HTTP, so a plain-HTTP
+  deployment is a text-only deployment by definition and can never be a valid
+  voice acceptance environment.
 
 ---
 
 ## Error handling
 
 Every case below needs a test and a phrasing.
 
 | Situation | Code does | Customer sees/hears |
 |---|---|---|
-| Gateway timeout | exactly one retry, then abort the turn | plain apology, rendered as the turn's assistant message, offer to resend |
-| Gateway unreachable / malformed reply | abort the turn, mark the gateway down | same apology, visible on the page |
-| Tool loop guard exceeded | abort the turn after a fixed maximum of tool rounds | same apology |
-| `401`/`403` from the ordering API | abort, log, **do not retry** | "I can't reach the kitchen system right now" |
+| Gateway timeout | one retry, then abort the turn | plain apology, offer to resend |
+| Gateway unreachable or malformed reply | abort the turn, mark the gateway down | plain apology, rendered as a normal reply |
+| Tool loop guard exceeded | abort the turn after a fixed number of tool rounds | plain apology |
+| `401`/`403` from PizzaSim | abort, log, do not retry | "I can't reach the kitchen system right now" |
 | `404` on the preselected `PIZZERIA_ID` | fail at startup, not mid-call | — (process refuses to start) |
-| Runtime pizzeria selection invalid/gone | session error (`409`); refresh the selector; process stays up | "that pizzeria isn't available right now" |
-| `422` validation on submit | surface the offending detail, **keep the basket** | targeted question about the offending item |
-| `5xx` on submit | **no blind retry**; mark the attempt unverified | "I'm not sure that went through — let me check" |
-| Timeout on submit | mark the attempt unverified; shortlist, then verify, before any retry | as above |
+| Runtime pizzeria selection invalid/gone | session error, refresh the selector; process stays up | "that pizzeria isn't available right now" |
+| `422` validation | surface the offending field, keep the basket | targeted question about the offending item |
+| `5xx` on submit | **no blind retry** | "I'm not sure that went through — let me check" |
+| Timeout on submit | mark unknown; shortlist via `GET /pizzerias/{id}/orders`, verify items via the detail endpoint before any retry | as above |
 | Unknown item code | `unknown_item` + up to three candidates | "I have Margherita or Marinara — which one?" |
-| Unknown extra | `invalid_extra` + up to three candidates | "I can't add that topping — did you mean …?" |
+| Unknown extra topping | `invalid_extra` + candidates, whole call rejected | "I can't add that topping — did you mean …?" |
 | Empty basket at submit | reject the transition | "What can I get you?" |
-| Mutation after submission | reject the transition | "That order is already on its way to the kitchen" |
 | Menu fetch fails at start | fail fast | "We're not taking orders right now" |
 | Pizzeria list fetch fails | no selector, say so | list unavailable — no fallback entry |
-| Speech service down | hide the speech controls / `404` on speech routes | text UI unaffected |
-
-**The gateway apology is a real assistant message.** It is appended to the
-conversation and emitted as an `assistant` event so the page renders it like
-any other reply. An apology that exists only in a log is the silent failure
-this product forbids.
-
-**The submit-timeout case is the one that matters**, because a blind retry
-doubles a real order. Recovery, in this exact order:
-
-1. Mark the attempt unverified and record the attempt time once.
-2. On the next submit attempt, read the pizzeria's order **list** and shortlist
-   entries whose `first_name` matches and whose `created_at` is no older than
-   the attempt time minus a small clock-skew allowance (one minute).
-3. For the most recent candidate, fetch the **detail** endpoint and compare its
-   items — type, code, quantity and extras, order-independent — against the
-   basket. The list carries no items and can never prove a match on its own.
-4. Only an exact match is adopted as the order that was placed, with the
-   remaining wait derived from its `ready_at`. Anything else — no candidate, a
-   candidate whose items differ — allows **exactly one** real retry.
-5. If the list or the detail lookup fails, tell the customer honestly that it
-   is unclear whether the order went through. Never guess, never retry blind.
-
-Every legal basket mutation clears this recovery bookkeeping: after a change,
-the unverified attempt no longer describes the basket in hand.
-
-The ordering API client uses explicit timeouts on every call and maps
-responses to typed errors — auth, not-found, validation (with details), server
-error, timeout. No caller inspects a status code directly.
+| Customer lookup fails | non-fatal tool error, continue | ask for the street as usual |
+| `set_customer` with both street and saved-street flag | `invalid_arguments`, no state change | "Either a street or the saved address — not both" |
+| Saved-street flag with no saved street | `no_saved_street`, no state change | "I don't have a saved address under that name — what's the street?" |
+| Speech unconfigured | speech endpoints answer `404`; controls not rendered | text UI unaffected |
+| Speech service down at startup | speech stays off; a line on standard error | text UI unaffected |
+| Speech request fails at runtime | `502`; the page hides both voice controls for the session | "Read-aloud isn't possible right now" / "please type" |
+| Empty transcript | no turn is sent | "I didn't catch that — please try again" |
+| Microphone permission refused | no turn is sent | "No microphone access" |
+
+The submit-timeout case is the one that matters: a blind retry doubles a real
+order. Recovery, in this exact order: shortlist candidates on the pizzeria's
+order list by first name and by creation time no older than the submit attempt
+minus a **60-second clock-skew allowance**; take the most recent candidate;
+fetch its detail; compare its items and quantities against the basket; adopt it
+**only** on an exact match — and otherwise allow exactly **one** real retry. If
+the list or the detail lookup fails, tell the customer honestly and retry
+nothing.
 
 ---
 
 ## Anti-patterns — explicitly forbidden
 
-Each of these is a way to make this product look finished while it is broken.
-None is a matter of taste.
+None of these is a matter of taste.
 
 1. **A regex "fast path" that places an order without the model.** It bypasses
    confirmation, mis-parses quantities, duplicates items on overlapping
    matches, and makes the tool-calling architecture decorative.
-2. **Shelling out to `curl` via a subprocess.** Use an HTTP client: no shell
+2. **Shelling out to `curl` via `subprocess`.** Use an HTTP client: no shell
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
-6. **A frontend that discards stream events.** Rendering only the final
-   message and throwing the tool events away leaves the customer watching a
+6. **A frontend that discards stream events.** A UI that renders only the final
+   message and throws the tool events away leaves the customer watching a
    frozen screen while the agent works normally. Rendering the intermediate
    steps is part of the product, not a debug view.
-7. **Order logic in a transport.** A channel that computes a total, decides a
-   state, or keeps its own copy of the basket has forked the truth. Channels
-   forward identifiers and render events; that is all.
-8. **Proving the web channel with `curl`.** It proves the server answers and
-   proves nothing about the product. The customer never talks to `curl`.
+7. **Reciting a saved address in any form** — in the confirmation question, in
+   the read-back, in a summary, in a log line, in a streamed event, as a hint
+   or as a partial match. The first name is a lookup key and not a credential;
+   whoever claims a name must never be able to extract the address behind it.
+8. **A voice control rendered outside a secure context.** A microphone button
+   on plain HTTP promises a capability the browser will refuse, and it teaches
+   the customer that the product is broken. The check belongs in the UI, not
+   only in a deployment note.
 
 ---
 
 ## Testing
 
-- **Unit: the state machine, exhaustively.** Every illegal transition has a
-  test asserting it is refused, and every invariant above has a test naming it
-  — including demotion after confirmation, the revision-bound confirm, the
-  read-back requirement, terminal `SUBMITTED`, line merging, both removal
-  semantics, and the single submit-attempt timestamp.
-- **Tool level, against recorded API fixtures.** No network, no LLM, fast.
-  Cover at least: per-type code collisions, candidates for an unknown code and
-  an unknown extra, atomic rejection of a bad add, refusal to parse a spelled
-  quantity, price copied at add time, cent-exact totals that do not drift, the
-  street key omitted from the submit body, typed mapping of `401`/`404`/`422`/
-  `5xx`/timeout, and the **complete submit-timeout recovery matrix**: recovery
-  via list plus detail, a candidate with different items rejected, verified
-  absence allowing exactly one retry, an unavailable list reported honestly,
-  and a mutation clearing the recovery state.
-- **Golden transcripts:** five scripted conversations against a stub model
-  replaying fixed tool calls — happy path, correction, unknown item, customer
-  changes their mind after the read-back, submit timeout. Assert the final
-  state, the exact sequence of tool calls made, the error codes raised, and
-  the final basket.
-- **Browser end-to-end, not optional.** Headless-browser tests drive the real
-  page against a stub ordering API and a stub scripted gateway — type a
-  message, wait for a rendered reply, walk a full order to submission —
-  asserting **against the DOM**, never against the API. The suite must cover
-  the header and footer contract, a pizzeria switch, a vanished pizzeria
-  refreshing the selector, a lost session recreating and offering resend, and
-  three failure paths: a tool error, a stream ending without a final message,
-  and the gateway unreachable. Each must leave a visible message on the page.
-- **API-surface tests** for the fixed contract above: the `/config` payload,
-  `pizzerias: null` with no fallback, `gateway: "unknown"` before the first
-  turn and `"ok"` after it, `404` for an unknown session, `409` for an unknown
-  pizzeria and for a turn already in flight, `422` for a bad language and a
-  stale/non-integer revision, and a tool error surfacing as plain language in
-  the stream.
-- **The acceptance test is live**, opt-in behind an environment flag, and is
-  the only test that touches the real API. It runs a full order through the
-  tools, submits, then reads the order back — **presence via the order list,
-  and customer, items and quantities via the detail endpoint**, because the
-  list carries no items and cannot verify them — and asserts the four points
-  under *What done looks like*. If this fails, the product does not work,
-  whatever else is green.
-- **Speech, manual:** dictate an order; dictate a name that needs correcting
-  and check that the agent repeats it back; ask a menu question; and one run
-  with the speech configuration removed, which must render a usable text-only
-  UI and place an order normally.
-- The whole offline suite runs with no network and no LLM, in one command.
+- **Unit:** the state machine, exhaustively. Every illegal transition has a
+  test asserting it is refused.
+- **Tool level:** against recorded API fixtures. No network, no LLM, fast.
+  Includes cent-exact totals, the atomic add, deterministic removal, and the
+  `(type, code)` collision.
+- **Golden transcripts:** **ten** scripted conversations against a stub model
+  replaying fixed tool calls, each asserting the final state, the calls
+  actually made, the error codes raised, and the resulting basket:
+  1. happy path,
+  2. correction ("make that three"),
+  3. unknown item with candidates,
+  4. customer changes their mind after the read-back (stale revision, second
+     read-back, then confirm),
+  5. submit timeout with recovery,
+  6. saved-address reuse,
+  7. saved-address decline falling back to a dictated street,
+  8. a spoken order using the saved street, name confirmed first,
+  9. a spoken order with a dictated street, name confirmed first,
+  10. a spoken order whose name was misheard and corrected before it was
+      stored.
+  The three spoken cases assert that the name-confirmation sentence occurs
+  **before** the `set_customer` call, and the misheard case also
+  asserts that `set_customer` ran **exactly once** — a corrected name must not
+  leave a ghost customer behind. The saved-address cases assert that the street
+  text never entered the model's message history.
+- **Address reuse, tool level:** `lookup_customer` known / unknown / saved
+  street missing / customer list unavailable (non-fatal), and
+  `set_customer(use_saved_street: true)` copying in code, adopting canonical
+  casing, refusing both arguments at once, and refusing when no saved street
+  exists.
+- **The redaction sweep is a string scan, and it is the oracle for the privacy
+  contract.** One test drives a complete saved-address order through the real
+  agent loop — lookup, reuse, add, read back, confirm, submit — capturing the
+  outbound submit payload. It then asserts the street text appears in that
+  payload and searches for it in every other artifact the run produced: the
+  emitted events, the model's message history, and the session's log file. **A
+  hit anywhere but the submit payload fails the test.** A redaction that is
+  merely stated and not scanned for does not count as implemented.
+- **Browser end-to-end, not optional.** Tests drive the real page in a headless
+  browser — type a message, wait for a rendered reply, walk a full order to
+  submission — asserting against the DOM, not the API. `curl` proves the server
+  works and proves nothing about the product; the customer never talks to
+  `curl`. Cover the header and footer contract, the pizzeria switch, the
+  language switch, and four failure paths: a tool error, a stream ending
+  without a final message, the gateway unreachable, and a lost session — each
+  must leave a visible message on the page.
+- **Offline voice end-to-end with a fake microphone is mandatory and cannot be
+  substituted.** A headless browser configured with a fake media stream drives
+  the genuine push-to-talk path against a stub speech service. An API-level
+  test of the speech proxies is a supplement, never a replacement: the wiring
+  that breaks is in the page. These tests assert wiring — control visibility,
+  the STT round trip, the spoken-turn marking reaching the model, read-aloud
+  behaviour, header placement and labelling, keyboard operation, runtime
+  degradation, secure-context gating — and never transcription or synthesis
+  quality. Specifically:
+  - the microphone and the toggle are visible when speech is configured and the
+    context is secure, and the toggle starts at `aria-pressed="false"`;
+  - a recorded fixture pushed through push-to-talk drives a real turn and fills
+    the basket, and the spoken-style marking reached the model;
+  - **the stub's synthesis call counter is the oracle for read-aloud, not the
+    button's own state**: with the toggle on, a turn containing a tool step and
+    a final message produces exactly **one** synthesis call — and the **off
+    path is asserted too**: after toggling back off, a further turn produces
+    **no** additional call;
+  - the toggle sits inside the header with the language switch as its previous
+    sibling and Start over as its next sibling;
+  - its `title` and `aria-label` follow the language switch, and its pressed
+    state does not;
+  - it is operable with Space and with Enter;
+  - a speech outage mid-session hides both controls and leaves typed ordering
+    working;
+  - with the browser reporting an insecure context, **neither control is
+    rendered** while typed ordering still works.
+- **API-level speech tests** supplement the browser tests: availability
+  reported in the UI bootstrap, the STT round trip using the session language,
+  synthesis returning playable audio, a failing service mapping to `502`, and
+  an unknown session mapping to `404`.
+- **The acceptance test is live**, opt-in via an environment flag, and it is
+  one of only two tests that touch the real API. Full conversation, submit,
+  then read the pizzeria's orders back — presence via
+  `GET /pizzerias/{id}/orders`, customer, items and quantities via the detail
+  endpoint (the list endpoint carries no items and cannot verify them) — and
+  assert points 1–4 under *What done looks like*. If this fails, the product
+  does not work, whatever else is green.
+- **The live voice acceptance test is the release-gating voice proof**, opt-in
+  via its own environment flag plus the URL of a deployment served over HTTPS.
+  It launches a real browser with a fake audio device streaming a recorded
+  spoken order, clicks the real microphone control, and lets **real speech
+  recognition** produce the transcript that drives the order; it enables
+  read-aloud and asserts the synthesis response carried **non-empty audio**;
+  then it confirms through the page's confirm control and verifies the
+  resulting order through the API — order present under the tenant, right
+  customer, items present. At least one German and one English recorded
+  fixture. **A text replay is not a substitute and must fail this test**: if
+  recognition does not produce an order-driving transcript, the test fails
+  rather than falling back to typing. When the flags are absent the test skips
+  cleanly, and it is never silently satisfied by the offline stub. A manual
+  demo is a release-note aid, not the acceptance artifact.
+- **Manual checklist (supplementary, never a substitute):** dictate an order,
+  dictate a name that needs correcting, ask a menu question aloud — plus one
+  run with the speech variables unset, which must render a usable text-only UI
+  and place an order normally.
+
+Recorded audio fixtures live with the tests and serve both the offline voice
+end-to-end tests and the live voice acceptance test.
 
 ---
 
 ## Who builds this — and who judges it
 
-Two roles take part and they are **not** interchangeable.
+The build runs locally, on the operator's own subscriptions, with the most
+capable models available. Two roles take part and they are **not**
+interchangeable.
 
 | Role | Permission |
 |---|---|
 | Implementer — one coding agent | writes every file |
 | Reviewer / judge — a second, independent agent | read-only, never writes |
@@ -849,29 +1056,37 @@ is. The roles and the protocol are binding; the tooling is not.
   *Deliverables* comes from it. No second implementer, no hand-patched fixes
   between rounds.
 - **The reviewer never writes the code it judges.** Read-only, two roles in
   one call: *devil's advocate* — attack the work, find gaps, wrong
   assumptions, missing error cases — and *judge*, scoring against the fixed
-  rubric so quality is measurable instead of a vibe.
+  rubric so quality is measurable across rounds instead of a vibe.
 - **The reviewer is a different agent from the implementer.** Independence is
   the point; a model reviewing its own output is not a review.
 
 ### Two model domains, never mixed
 
-- **Build-time models** power the harnesses. Configured outside this product,
-  none of this spec's business. Nothing in the deliverables reads, references
-  or depends on them.
+- **Build-time models** power the harnesses. Configured outside this
+  repository, none of this spec's business. Nothing in the deliverables
+  reads, references, or depends on them.
 - **Runtime models** are what the ordering agent calls while serving a
   customer: `LITELLM_PIZZA_MODEL_1` and `_2` from the environment.
 
 Binding consequences:
 
 - The implementer never wires the agent to whatever model the implementer
   itself runs on, and never copies a build-time model name into source,
-  configuration, prompts, tests or documentation.
-- No model name of any kind is hardcoded. A missing runtime value is a startup
-  failure, not a default.
+  config, prompts, tests or docs.
+- No real vendor, engine or model name is hardcoded in a production-facing
+  artifact — not in source, not in the deployment definition, not in this
+  document. A missing runtime value is a startup failure, not a default.
+- The same rule covers speech: no real engine, image, model or voice name
+  reaches source, the deployment definition or this document.
+- Exempt from both, and nothing else is: opaque local stub identifiers used by
+  the offline test harness (`scripted-stub`, `stub-stt`, `stub-tts`,
+  `stub-voice` and the like). They name no real vendor, engine, model or voice,
+  they exist only so tests run without a network, and no production-facing
+  artifact may read one or default to one.
 - **Harness is not model.** Never ask an agent which model it is — a
   self-report is not evidence; the configuration is binding.
 - Whatever the build runs on, it does not lower the bar. Do not simplify the
   design, skip a test, or accept a weaker answer on the assumption that the
   model behind you is limited.
@@ -894,23 +1109,24 @@ VERDICT: APPROVED | CHANGES_REQUIRED
 ISSUES: (max 5 bullets, concrete and actionable, empty if approved)
 ```
 
 - `APPROVED` requires `TOTAL >= 20` **and** no dimension below 4. If the
   verdict line says approved but the scores miss that bar, **the numbers
-  win** — a verdict is a sentence and the scores are the measurement.
+  win**.
 - Maximum 3 rounds per stage. Still not approved after round 3 → stop, show
   the scores and the open issues. A valid outcome, not a failure.
-- Disagreeing is allowed — a one-line rebuttal in the next request. Never
+- Disagreeing is allowed — one-line rebuttal in the next request. Never
   ignore a finding silently.
-- Every reviewer output is written to a file under `reviews/`, every round's
-  scores into `reviews/scores.md`, and `reviews/` is committed.
+- Every reviewer stdout goes into `reviews/`, every round's scores into
+  `reviews/scores.md`, and `reviews/` is committed.
 
 ### Two stages, in this order
 
 1. **PLAN.** Write `PLAN.md`: file layout, tool schemas, state machine, agent
-   loop, error handling, conversation state. **No code.** Iterate with the
-   reviewer until `APPROVED`. Implement nothing before that.
+   loop, error handling, conversation state, the privacy contract, the speech
+   wiring. **No code.** Iterate with the reviewer until `APPROVED`. Implement
+   nothing before that.
 2. **IMPLEMENT.** Only after the plan is approved. Build exactly the approved
    plan, then iterate the diff with the reviewer until approved.
 
 "Done" means the judge approved — not that the code runs. Working code that
 fails the rubric is not done.
@@ -922,124 +1138,141 @@ fails the rubric is not done.
 This is an autonomous build. No clarifying questions will be answered and no
 feedback arrives until you are done — every decision inside these constraints
 is yours. Work in passes and verify after each; do not write the whole thing
 and then run it once.
 
-The stack: Python with one virtual environment, an HTTP framework and an ASGI
-server for the web channel, one HTTP client used everywhere, one test runner,
-one headless-browser driver, and multipart support for the audio upload.
-Nothing else. Pin every dependency to an exact version in `requirements.txt`.
-
-0. **Contracts.** Confirm the contract facts against the live API, move any
-   answer into the facts, commit. The open list only shrinks — a fact
-   confirmed against the live service never becomes a question again.
-1. **Core.** Order model, state machine, menu snapshot, tool layer, tests. No
-   LLM, no network. Pass when the unit tests are green.
-2. **Agent loop.** Model, tools, system prompts, JSONL logging, one turn end
-   to end.
+0. **Contracts.** Verify the API facts above against the live API before the
+   components that depend on them are implemented. The open list only shrinks —
+   a verified fact never becomes a question again.
+1. **Core.** Order model, state machine, tool layer, tests. No LLM, no
+   network. Pass when the unit tests are green.
+2. **Agent loop.** Model, tools, system prompt, one turn end to end.
 3. **CLI.** Full conversation, real API, an order visible on the dashboard.
-4. **Web.** The fixed HTTP surface on 8888, same core. Pass **only** when you
-   have opened the page in a browser, switched pizzeria, asked a price
-   question, placed an order through the page, and seen it on that pizzeria's
-   dashboard — not when the endpoint answers `curl`.
-5. **Speech.** Wire the speech service into the web UI, the spoken-answer
-   policy, and the degraded no-speech path. Verify the no-speech path by
-   removing the configuration and placing a complete order as text.
-6. **Harden.** Walk the error table, force each case, fix what breaks.
+4. **Web.** FastAPI on 8888, same core. Pass only when you have opened the
+   page in a browser, switched pizzeria, asked a price question, placed an
+   order through the page, and seen it on that pizzeria's dashboard — not
+   when the endpoint answers `curl`.
+5. **Voice.** Wire the speech service into the web UI: push-to-talk, the header
+   read-aloud toggle, the secure-context gate, the spoken-answer policy, and
+   the degraded no-speech path. Pass only when the fake-microphone browser test
+   is green **and** a spoken order has gone through a real HTTPS deployment.
+6. **Privacy.** Saved-address lookup and reuse end to end, and the redaction
+   scan. Pass only when the string sweep finds the saved street in the submit
+   payload and nowhere else.
+7. **Harden.** Walk the error table, force each case, fix what breaks.
 
 After each pass, review your own work as the reviewer who has to reject it:
 what would a hostile reader find first? Fix that, then move on. Stop only when
-a full pass over this file finds nothing left that you know how to improve.
+a full pass over the spec finds nothing left that you know how to improve.
 
 ---
 
 ## Deliverables
 
 ```
 .
-├── SPEC-RELEASE-1.0.0.md    ← this file
-├── README.md                ← how to run each channel
+├── SPEC-RELEASE-1.1.0.md    ← this file
+├── README.md                ← how to run each channel, and the voice setup
 ├── PLAN.md                  ← written before any code, updated as you go
-├── requirements.txt         ← exact pins
+├── requirements.txt         ← every dependency pinned to an exact version
+├── Procfile                 ← the web channel's process definition
 ├── .env.example             ← names only, never values
 ├── core/
-│   ├── order.py             ← Order, basket, revision, snapshot, money
+│   ├── order.py             ← Order, basket, revision, the two customer views
 │   ├── state.py             ← state machine, transitions, invariants
-│   ├── menu.py              ← menu snapshot, (type, code) validation, candidates
+│   ├── menu.py              ← menu snapshot, code validation, candidates
 │   ├── pizzasim.py          ← API client, typed errors, timeouts, env loading
-│   ├── tools.py             ← the eight tool schemas + dispatch
-│   └── agent.py             ← session factory, model loop, prompts, logging
+│   ├── tools.py             ← the nine tool schemas + dispatch
+│   └── agent.py             ← model loop, prompt assembly, event log
 ├── channels/
-│   ├── cli.py
-│   ├── web.py               ← the fixed HTTP surface, port 8888
-│   ├── speech.py            ← speech service client
-│   └── static/
-│       ├── index.html
-│       ├── app.js           ← stream rendering, basket, confirm, speech
-│       └── style.css
+│   ├── cli.py               ← terminal transport
+│   ├── web.py               ← FastAPI, port 8888, NDJSON stream, speech proxies
+│   ├── speech.py            ← speech service client, all-or-nothing enablement
+│   └── static/              ← page, styles, and the UI script incl. voice
 ├── prompts/
 │   ├── system.de.md
 │   └── system.en.md
+├── deploy/
+│   └── speech service definition ← neutral, self-hosted, CPU-only
 ├── tests/
 │   ├── fixtures/            ← recorded API responses
-│   ├── stubs.py             ← stub ordering API + stub gateway, on localhost
-│   ├── test_state.py
-│   ├── test_tools.py        ← incl. the opt-in live acceptance test
-│   ├── test_transcripts.py  ← the five golden conversations
-│   ├── test_web_e2e.py      ← API surface + headless browser, DOM assertions
-│   └── transcripts/
-└── reviews/                 ← one file per review round, plus scores.md
+│   ├── fixtures/audio/      ← recorded spoken orders, DE and EN
+│   ├── stubs.py             ← stub API, stub gateway, stub speech service
+│   ├── test_state.py        ← the state machine, exhaustively
+│   ├── test_tools.py        ← tools, redaction sweep, live acceptance
+│   ├── test_transcripts.py  ← the ten golden conversations
+│   ├── test_web_e2e.py      ← headless browser, DOM assertions
+│   ├── test_web_speech.py   ← stub speech + fake mic, live voice acceptance
+│   └── transcripts/         ← the ten scripted conversations
+├── reviews/                 ← one file per review round, plus scores.md
+└── logs/                    ← one JSONL file per session, written at runtime
 ```
 
-Event logs are written at runtime to `logs/agent-<session>.jsonl`, one JSON
-line per event, and are not committed. `logs/`, the virtual environment and
-any local `.env` belong in `.gitignore`.
+Roles of the parts, so nothing is misplaced:
+
+- `core/` owns the order and everything that may change it. It never imports a
+  transport and never knows a channel exists.
+- `channels/` carries words in and words out. No order logic, no validation, no
+  arithmetic. The web channel forwards identifiers to core and streams core's
+  events; the speech client is a transport detail of that channel.
+- `prompts/` holds one file per language, rendered with the pizzeria name.
+- `deploy/` holds the neutral speech-service definition — interface only.
+- `tests/` holds the deterministic suite plus the two opt-in live tests.
 
 ---
 
 ## Decisions locked
 
 | Area | Decision |
 |---|---|
 | Order ownership | Code. The model never holds the cart. |
 | Submit | Single call, only from `CONFIRMED`, never auto-retried |
-| Submit recovery | Shortlist on the order list, verify items on the detail endpoint, adopt only an exact match |
-| Menu | Fetched live once per conversation, immutable for its lifetime, no fallback list |
-| Item identity | `(type, code)` — never a code alone |
+| Menu | Fetched live per session, no fallback list |
 | Tenancy | Customer-selectable; `PIZZERIA_ID` preselects, never restricts; tenant in the URL path |
-| Session | One order, one menu snapshot, one tenant-bound client, one language; the tenant never changes |
 | Pizzeria selector | Filled from the API only; no fallback entry |
 | Prices | Shown from the API; no payment, no invented figures |
-| Totals | Computed in code with exact decimal arithmetic; the model never does arithmetic |
-| Language | Session language from `PIZZERIA_LANG`, switchable in the web header; per-turn mirroring wins for replies |
+| Totals | Computed in code in exact decimal cents; the model never does arithmetic |
+| Saved addresses | Reusable after one explicit confirmation; the address text never reaches the model, the stream, the page, the transcript or the logs |
+| Saved-address scope | `street_one` only; a second stored line is never reused |
+| Address disclosure | Never, in any form. The first name is a lookup key, not a credential |
+| Redaction proof | A string scan over every produced artifact; the submit payload is the only legal occurrence |
+| Name confirmation | Mandatory in every spoken flow before submission; the saved-address question is not a substitute |
+| Language | Session language from `PIZZERIA_LANG`, switchable in the web header; per-turn mirroring wins for replies; speech follows the session language |
 | Transports | One core, two channels (CLI, web), no logic in the channels |
-| Concurrency | One turn at a time per session, enforced by the transport |
-| Speech | Optional, self-hosted container, OpenAI-compatible HTTP; no vendor, no browser speech API |
+| Speech | Self-hosted container, OpenAI-compatible HTTP; no vendor, no browser speech API |
+| Speech enablement | All-or-nothing, probed at startup; three of four variables is off |
+| Voice | Required product capability on the web channel; text-only is degraded operation, not the product |
+| Read-aloud | Off by default, header speaker toggle, final assistant message only |
+| Voice context | Rendered only in a secure context, enforced in the UI; HTTPS for any voice-capable deployment |
+| Voice failure | Runtime outage hides the voice controls and never blocks typed ordering |
 | Web UI | Pizzeria name, basket and connection state always visible; no message ends unanswered |
-| Confirmation | Mandatory read-back tied to a basket revision, taken as an explicit customer action |
 | Version | `x.y.z` in the footer, validated at startup, raised every release |
 | Derived URLs | Dashboard and docs built from `PIZZASIM_URL`, never literal |
 | Languages | DE + EN, mirrored per turn |
+| Confirmation | Mandatory read-back tied to a basket revision |
 | Parsing | The model parses. No regex order parser, ever. |
-| HTTP | A real client with explicit timeouts. No subprocess `curl`. |
+| HTTP | A real client with timeouts. No `subprocess curl`. |
+| Dependencies | Pinned to exact versions, no ranges |
 | Persistence | None beyond the process and the PizzaSim API |
-| Errors | Typed in code, plain language to the customer, never a raised exception out of the tool layer |
-| Contract facts | Confirmed facts never return to the open list; the list only shrinks |
+| Errors | Typed in code, plain language to the customer |
+| Contract facts | Verified facts never return to the open list; the list only shrinks |
 | Implementer | One agent only — nothing else writes code |
 | Reviewer | A second, independent agent, read-only, judge and devil's advocate |
 | Models | Never named, never hardcoded — environment configuration |
 | Build tooling | Not specified here; the operator picks it |
-| Proof | Verified through the browser and the live API, never only through `curl` |
+| Proof | Verified through the browser and the live API, never only through `curl` — including one spoken order end to end |
 | Definition of done | The judge approved, not "it runs" |
 
 ## Decisions deferred
 
 - Extras and modifiers beyond a passthrough `extras[]`.
 - Post-submit modification or cancellation.
-- Reusing a returning customer's stored address instead of asking for it
-  again, and any other memory across conversations ("the usual").
+- Reuse of a second stored address line, until the order write contract for it
+  is verified.
+- Multi-turn memory across sessions beyond saved-address reuse ("the usual").
 - Additional languages beyond DE + EN.
+- Streaming speech, barge-in and turn detection.
 - Telephony as a third channel.
 
 ---
 
 ## Ticket sizing rules
@@ -1047,23 +1280,24 @@ any local `.env` belong in `.gitignore`.
 - Each ticket is **one hour or less** of implementation.
 - Prefer three narrow tickets over one broad one. Split by file, by component,
   or by "schema / implementation / tests".
 - Every ticket carries acceptance criteria as a checklist.
 - Tests belong to the ticket that introduces the behaviour, never to a
-  follow-up.
+  follow-up. A privacy or voice guarantee ships in the same ticket as the test
+  that proves it.
 
 ---
 
-## Twenty-four rules that decide whether this works
+## Thirty-one rules that decide whether this works
 
-Everything above is binding. These twenty-four are the ones that quietly decide
+Everything above is binding. These thirty-one are the ones that quietly decide
 whether the order lands correctly, and each is the compressed form of a rule
 stated in full in the section named after it.
 
 1. **List versus detail.** The order list carries no items, so items and
    quantities must **only** ever be verified through the single-order detail
-   endpoint — in timeout recovery and in the acceptance test alike. *(The
+   endpoint — in timeout recovery and in the acceptance tests alike. *(The
    PizzaSim API; Error handling; Testing)*
 2. **Language authority.** The session language comes from `PIZZERIA_LANG` and
    the header switch, but for the agent's replies per-turn mirroring wins: it
    **must** answer in the language of the customer's latest message and never
    comment on the switch. *(Conversation policy)*
@@ -1100,14 +1334,15 @@ stated in full in the section named after it.
 12. **The `/config` contract.** The pizzeria list is read live on every call
     and is `null` on failure — never an empty list, never a fallback entry —
     and the page must then say the list is unavailable. *(The web channel)*
 13. **`APP_VERSION` is validated.** It must match `x.y.z` at startup or the
     process refuses to start, and it is shown in the footer. *(Environment)*
-14. **Plain-HTTP survivability.** Whether speech exists is decided only by the
-    server's `speech` flag; **only** the microphone is additionally gated, and
-    only on `mediaDevices` and `MediaRecorder`, so read-aloud keeps working
-    where capture does not. *(Speech)*
+14. **The secure-context gate lives in the UI.** Both voice controls are
+    rendered **only** when the server reports the speech path available **and**
+    the browser reports a secure context; the microphone is gated
+    on the capture APIs as well. Over plain HTTP the page presents no voice-capable UI
+    at all, and typed ordering is unaffected. *(Speech; Anti-patterns)*
 15. **A lost session is recreated transparently.** A `404` creates a fresh
     session with one plain notice; a chat message may be resent, a pending
     confirm never is. *(The web channel)*
 16. **A confirm retry uses the same revision.** Never a new one — so a retry
     can never place a second order. *(The web channel)*
@@ -1132,8 +1367,41 @@ stated in full in the section named after it.
     no dimension below 4 must **never** be treated as an approval. *(Review
     protocol)*
 23. **The open list only shrinks.** A fact confirmed against the live service
     never returns to the open contract questions. *(The PizzaSim API)*
 24. **The live acceptance test is the definition of working.** It is opt-in and
-    the **only** test that touches the real API: presence via the order list,
+    one of only two tests that touch the real API: presence via the order list,
     customer, items and quantities via the detail endpoint. If it fails the
     product does not work, whatever else is green. *(Testing)*
+25. **Booleans only.** `lookup_customer` returns exactly two booleans and the
+    snapshot — never the street, never a masked form of it, never its length.
+    `set_customer` takes a dictated street **or** the saved-street flag and
+    never both, and refuses the flag with `no_saved_street` when nothing is
+    stored. *(Tools)*
+26. **One legal occurrence.** The saved street text may appear **only** in the
+    outbound submit payload — never in a snapshot, an event, a log line, the
+    model's history or the page — and a string-scanning end-to-end test is
+    what proves it. Only `street_one` is ever reused. *(The saved-address
+    privacy contract; Testing)*
+27. **Never recite a saved address.** Reuse is settled by exactly one
+    confirmation question that does not name the address, and the interface
+    shows a localized "saved address" label instead of the text. A street the
+    customer dictated in this conversation is their own input and is exempt.
+    *(The saved-address privacy contract; Conversation policy)*
+28. **Name confirmation is its own question.** In every spoken flow the first
+    name **must** be confirmed before submission, and the saved-address
+    question never substitutes for it — a misheard name creates a ghost
+    customer nobody will find again, and the code adopts the stored record's
+    canonical casing to avoid a near-duplicate. *(Conversation policy; Tools)*
+29. **Read-aloud discipline.** It is off on every page load, it applies **only**
+    to the final assistant message of a turn, and the proof is the speech
+    service's own call counter — including the off path, where toggling back
+    off must produce no further synthesis call. *(Speech; Testing)*
+30. **Speech is all-or-nothing, probed, and neutral.** All four speech
+    variables plus a 2xx startup probe, or the path is off and both endpoints
+    answer `404`; a runtime failure withdraws the controls without touching
+    typed ordering; and no engine, image, model, voice or host name appears
+    anywhere in the repository. *(Speech; Environment)*
+31. **Voice is proved, not demonstrated.** A fake-microphone browser test is
+    mandatory and cannot be replaced by API-level tests, and the release-gating
+    live voice test drives a real browser over HTTPS with real recognition and
+    non-empty synthesised audio — a text replay **must** fail it. *(Testing)*
````
