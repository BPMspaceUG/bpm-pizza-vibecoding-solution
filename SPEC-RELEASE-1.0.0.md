# PizzaSim Ordering Agent — Specification

> Hand this to a coding agent as the entire task:
> `FOLLOW INSTRUCTIONS PRECISELY AT "SPEC-RELEASE-1.0.0.md"`.
> This file is the source of truth for what the product is. Everything else —
> code, tests, prompts, tickets — derives from it.

---

## Where this format comes from

The **shape** of this document is not ours. It is borrowed from Cedric Mössner —
**The Morpheus** (<a href="https://www.youtube.com/@TheMorpheusTutorials" target="_blank">youtube.com/@TheMorpheusTutorials</a>),
who writes exactly one specification file per project and hands the identical
file to every new model in order to compare them. The prompt he sends alongside
it is a single line — `FOLLOW INSTRUCTIONS PRECISELY AT "SPEC.MD"` — which is
why a line like it, and not a long prompt, stands at the top of this file.

Sections adopted from his specs: *Soul*, *The One Load-Bearing Idea*, hard
*Scope In / Out*, an explicit autonomy clause, work *in passes* with
verification after each, a file-level *Deliverables* list, *Decisions Locked /
Deferred*, and the one-hour *ticket sizing rules*.

Reference specs:
<a href="https://github.com/TheMorpheus407/morphcook" target="_blank">morphcook</a>
— offline Flutter recipe app; one spec, seven model implementations.
<a href="https://github.com/TheMorpheus407/hogwarts-blender-benchmark" target="_blank">hogwarts-blender-benchmark</a>
— fully procedural Blender build; `prompt.txt` plus a spec file.

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
- Every item code is validated against the **menu snapshot fetched for this
  conversation**. An unknown code is a tool error carrying candidate matches —
  never a silent guess, never a fallback to a hardcoded list.
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
  - `web` — an HTTP server on port 8888, browser chat UI, streaming the
    agent's intermediate steps as newline-delimited JSON so tool calls and
    tool results are visible, not just the final answer.
- **Speech on the web transport**, served by a self-hosted CPU-only speech
  container over HTTP, **optional in every sense**. See *Speech*.
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
  acceptance test and a browser end-to-end suite.
- **Structured logging** of every turn: user text, model tool calls, tool
  results, state transitions. One line per event, JSON, to a file.

### Out (explicitly)

- Payment and anything financial beyond showing prices the API supplies.
- Delivery routing, or an ETA of our own invention.
- Accounts, auth, sessions surviving a process restart.
- Modifying or cancelling an order after it was submitted.
- **Any reuse of customer data across conversations** — no customer-record
  lookup, no offering an address a customer gave at some earlier point, no
  filling any field from anything other than what was said in this
  conversation. Every order collects its own name and, optionally, its own
  street, every time.
- Any regex or keyword parser that produces an order without the model.
  See **Anti-patterns**; this is a hard ban, not a style preference.
- Reading the whole menu aloud when the answer will be spoken.
- Persisting customer data anywhere beyond the process and the PizzaSim API.

---

## Environment and configuration

All configuration comes from environment variables. The process environment
wins; otherwise read `~/.env` if it exists. Never write that file, never create
it, never print a value from it.

| Variable | Required | Purpose |
|---|---|---|
| `LITELLM_PIZZA_URL` | yes | OpenAI-compatible gateway base URL (`/chat/completions` appended) |
| `LITELLM_PIZZA_KEY` | yes | Bearer token for the gateway |
| `LITELLM_PIZZA_MODEL_1` | yes | Model the ordering agent calls; no default in code |
| `LITELLM_PIZZA_MODEL_2` | no | Second configured model; read at startup, unused by this build — its absence must never fail the start |
| `PIZZASIM_URL` | yes | PizzaSim API base URL; dashboard and docs links derive from it |
| `PIZZASIM_API_KEY` | yes | Sent as header `X-API-Key` on protected routes |
| `PIZZERIA_ID` | yes | UUID of the pizzeria preselected on first load |
| `PIZZERIA_LANG` | yes | Initial language, exactly `de` or `en`, no default |
| `APP_VERSION` | yes | Release version, `x.y.z`, shown in the web footer |
| `SPEECH_URL` | no | Base URL of the self-hosted speech service |
| `SPEECH_STT_MODEL` | no | Transcription model id |
| `SPEECH_TTS_MODEL` | no | Synthesis model id |
| `SPEECH_TTS_VOICE` | no | Voice id |

Rules:

- **Nothing is hardcoded.** No UUID, no model name, no menu, no base URL, no
  vendor — not even as a fallback "just in case".
- A missing or empty **required** variable must abort before the first turn,
  with a message naming the variable and the file it was expected in. Never
  start half-configured.
- `PIZZERIA_LANG` must be exactly `de` or `en`. Any other value is a
  configuration failure, not a silent fallback.
- `APP_VERSION` must match `x.y.z` (three integers, dot-separated). Anything
  else is a configuration failure at startup. Without a version nobody can
  tell which build is answering, and a version nobody raises is worse than
  none: patch for fixes, minor for new behaviour, major for a break.
- The four `SPEECH_*` variables are the exception and they behave
  **all-or-nothing**: speech is enabled only when all four are set *and* the
  service answers a startup probe. Otherwise the speech features are simply
  not rendered and everything else works unchanged.
- Secrets never appear in logs, transcripts, error messages or the web UI.
- Ship a `.env.example` carrying **names only, never values**.

---

## The PizzaSim API (contract)

The facts below are contract truth about the service this agent talks to. Treat
them as given; confirm anything you doubt against the live service before you
build the component that depends on it. A fact confirmed against the live
service never moves back into the open list; the open list only shrinks.

| Call | Auth | Notes |
|---|---|---|
| `GET /menu` | public | returns `pizzas[]`, `pasta[]` and `toppings[]` |
| `GET /pizzerias` | `X-API-Key` | `{"pizzerias": [{id, name, …}]}` |
| `GET /pizzerias/{id}/orders` | `X-API-Key` | `{"orders": [...]}` — that pizzeria's orders, **without items** |
| `GET /pizzerias/{id}/orders/{order_id}` | `X-API-Key` | the full order **incl. `customer` and `items[]`** |
| `POST /pizzerias/{id}/orders` | `X-API-Key` | places the order |
| `GET /location?street=…` | public | street plausibility check (optional tool) |

There is **no endpoint for looking a customer up**, and this agent must not
behave as if there were.

Order request body:

```json
{
  "customer": { "first_name": "Marco", "street_one": "via di Cantieri" },
  "items": [{ "type": "pizza", "code": "margherita", "qty": 2, "extras": [] }]
}
```

`street_one` is optional: when the customer did not give a street, the key is
**omitted from the body**, never sent as `null`.

The response carries `order_id`, `status`, `eta_seconds`.

Derived URLs — built from `PIZZASIM_URL`, never hardcoded:

- Dashboard of a pizzeria: `{PIZZASIM_URL}/dashboard/pizzerias/{id}`.
- API documentation: `{PIZZASIM_URL}/swagger.html` — there is **no** `/docs`.

Facts that shape behaviour:

- The tenant is **always** in the URL path, never in a header. The API key is
  a server key, not a pizzeria id.
- Customers are unique per pizzeria **by first name**. An unknown name
  silently creates a new customer — a misheard name creates a ghost. Dictated
  input must therefore confirm the name explicitly.
- `street_one` is optional and **not** validated for deliverability. Asking
  for it is a policy of this agent — never claim to have checked an address.
- `POST /orders` is **not** idempotent. A retry after a timeout can double a
  real order. See **Error handling**.
- **Menu item shape:** `{"code", "name", "base": [ingredients], "price"}`.
  `price` is a number in euros — the source for every price answer and for the
  basket total; no other financial data exists in the API. `name` is a single
  string, identical in DE and EN; there are no per-language names.
- **`extras[]` is a controlled vocabulary:** the `toppings[]` array returned
  by `GET /menu`. The server rejects an unknown extra with `422`
  (`"items[0].extras contains invalid topping 'unicorn_dust'"`), so the tool
  layer validates extras against `toppings[]` exactly like item codes. Extras
  carry no price of their own; the basket must say so rather than imply a
  charge it cannot compute.
- **Error bodies are machine-readable:**
  `{"error": "<code>", "details": ["<human sentence>", …]}` — for example
  `validation_failed` with HTTP `422`. Map them to typed errors; `details`
  may feed a targeted question back to the customer.
- **Order status values:** `ordered` → `prepared_planned` → `delivered`
  (`delivered_at` set on the last). A fresh order starts as `ordered`.
- **List-entry shape:** `{id, customer_id, created_at, ready_at, status,
  delivered_at, first_name}`. `created_at` and `ready_at` are epoch seconds —
  the remaining wait after a recovery is `ready_at` minus now, never below
  zero. **The list carries no items.**
- **`GET /location?street=` returns** `{"street": "<echo>",
  "deliverable": <bool>}` with HTTP `200` — and answers `true` even for
  nonsense input. It is a weak plausibility signal at best: never tell the
  customer an address was verified.
- **Item codes are unique per type, not globally** — `tonno` exists as a pizza
  *and* as a pasta, at different prices. Validation, pricing and removal
  always key on `(type, code)`; a lookup by code alone is a defect.

### Open contract questions — shrink-only

Resolve against the live API before the affected component is implemented, then
move the answer up into the facts and delete the question. Never guess. A fact
confirmed against the live service never returns here.

*(empty — everything the build needs is in the facts above)*

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

`set_customer` before any item is legal and leaves the order in `EMPTY`: the
state is derived from the facts, not from the call order. After every legal
mutation the code recomputes: no items → `EMPTY`; items but no customer →
`COLLECTING`; items and customer → `READY`.

Invariants, all enforced in code and all covered by unit tests:

1. `submit_order` outside `CONFIRMED` returns an error. It does not
   "helpfully" confirm on the model's behalf.
2. Any mutation after `CONFIRMED` drops the order back to `READY`. A
   confirmation applies to the basket that was read back, not to a later one,
   and it never survives the demotion.
3. `CONFIRMED` is reachable only via `confirm_order`, which is legal only
   after `read_back` for the **current** basket revision. The basket carries a
   revision counter incremented on every mutation, and `confirm_order` must
   name it; a stale number is refused.
4. `SUBMITTED` is terminal. The conversation may continue; the order may not.
   Every mutation attempt afterwards is refused with a speakable message.
5. An item enters the basket only with a `(type, code)` present in the menu
   snapshot fetched for this conversation.
6. A basket never crosses a tenant boundary. Changing pizzeria starts a fresh
   conversation and a fresh order.

Basket mechanics, all normative:

- Two added lines merge only when `(type, code, sorted(extras))` match
  exactly. The same code with different extras is a separate line.
- The timestamp of the first submit attempt is recorded once and only once,
  and is used solely by timeout recovery.
- Any legal mutation clears the recovery bookkeeping of an unverified submit
  attempt. That correlation belongs to the basket that was confirmed then, not
  to whatever the basket becomes now.

---

## Tools

The model sees exactly these eight. Names, parameters and semantics are fixed,
and no ninth tool is added for convenience.

| Tool | Parameters | Returns |
|---|---|---|
| `get_menu` | — | pizzas and pasta with codes, display names, prices, plus the available toppings |
| `add_items` | `items[]` of `{type, code, qty, extras[]}` | new basket snapshot |
| `remove_item` | `type`, `code`, optional `qty` | new basket snapshot |
| `set_customer` | `first_name`, optional `street_one` | customer as stored + snapshot |
| `read_back` | — | the complete order as it stands, incl. the code-computed total |
| `confirm_order` | `revision` | state `CONFIRMED`, or an error if stale |
| `submit_order` | — | `order_id`, `status`, `eta_seconds` |
| `check_street` | `street` | plausibility result (optional, never a guarantee) |

`type` is constrained to `pizza` or `pasta` in the schema; `qty` is an integer
with minimum 1.

Tool result conventions:

- Success: the **full current state**, not a diff. Every successful result
  embeds the same snapshot object:

  ```json
  {"state": "READY", "revision": 3,
   "items": [{"type": "pizza", "code": "margherita", "name": "Margherita",
              "qty": 2, "extras": [], "unit_price": 8.5, "line_total": 17.0}],
   "basket_total": 17.0,
   "customer": {"first_name": "Marco", "street_one": null},
   "read_back_done": false}
  ```

  The model never reconstructs the basket from conversation history.
- Failure: `{"error": {"code": "…", "message": "…", "candidates": […]}}`.
  `message` is written so it can be **spoken to the customer as-is** — plain
  language, no status code, no field path, no JSON. `candidates` is an array,
  empty when there is nothing to suggest.
- The error codes are fixed: `unknown_item`, `invalid_extra`,
  `invalid_quantity`, `empty_basket`, `not_in_basket`, `invalid_state`,
  `stale_revision`, `read_back_required`, `order_closed`, `api_unavailable`,
  `submit_unknown`, `submit_failed`, `unknown_tool`.
- **Dispatch never raises.** Every failure — menu, state machine, API, unknown
  tool name — comes back as a tool result the model must deal with in front of
  the customer. An exception escaping the tool layer is a defect.
- `add_items` with an unknown code returns `unknown_item` plus **at most three**
  candidates from the menu snapshot, preferring the requested type and falling
  back to the other type so "pizza tonno" asked as a pasta still helps. The
  model asks; it does not pick.
- **`add_items` is atomic.** If any item, extra or quantity in the call is
  invalid, the whole call is rejected and the basket is untouched. A partial
  add is a defect.
- An unknown extra returns `invalid_extra` with up to three topping
  candidates, in the same shape.
- Quantities are integers. A tool receiving `"zwei"` returns
  `invalid_quantity`; it does not parse German. Booleans are not integers.
- **Totals are computed in code only.** The unit price is copied from the menu
  snapshot **at add time** into the basket line; line totals and the basket
  total are computed with exact decimal arithmetic and rounded to cents once,
  half-up — never by accumulating binary floats, and never by the model. The
  web basket shows the same code-owned total that `read_back` carries.
- `remove_item`'s parameters are fixed, so when several basket lines share
  `(type, code)` with different `extras[]` the semantics must be
  deterministic: **without `qty` every matching line is removed; with `qty`
  the most recently added matching line is reduced**, and removed entirely
  when `qty` reaches or exceeds its quantity. The full snapshot in the result
  lets the model repair anything else by remove and re-add.
- `confirm_order` with a non-integer revision is refused exactly like a stale
  one.
- `check_street` returns the echoed street and a boolean. It is a courtesy,
  never a precondition, and its `true` means nothing.

---

## Conversation policy

This is what the system prompt must produce. Write the prompt to achieve it;
do not paste this section into it verbatim. One prompt file per language, with
the pizzeria name substituted into it at session creation.

- Greet first, in the session language, one sentence, offering help — not a
  menu recital.

**Language authority — one rule.** The session language starts as
`PIZZERIA_LANG` (greeting, CLI, web UI chrome before any switch). The web
header switch changes the session language: UI chrome, the greeting of a fresh
conversation, and the speech hint (STT language, TTS output). For the agent's
replies, **per-turn mirroring wins**: it answers in the language of the
customer's latest message, even when that differs from the session language,
and it never comments on the switch. The CLI has no switch and stays at
`PIZZERIA_LANG`.

- **One question per turn.** Never stack "name, street and what would you
  like?"
- Never state a menu item or a price that did not come from `get_menu` in this
  conversation. Price questions are normal questions, and so is "what does my
  basket come to?" — quote `price` and `basket_total` verbatim from tool
  results and never do the arithmetic in the reply.
- Collect the first name and the street. If the customer declines the street,
  accept it and move on — it is optional in the API.
- **Repeat the first name back once to confirm it** before submitting. A
  misheard name silently creates a customer nobody will find again.
- Before submitting: call `read_back`, present it, and wait for an explicit
  yes. "Mhm" and silence are not a yes; ask once more, then offer to start
  over.
- Never announce that an order was placed before `submit_order` returned an
  `order_id`.
- On success, state the order id in groups a human can repeat back, and the
  wait time in **minutes**, converted from `eta_seconds`.
- On error, explain in plain language what happened and what the options are.
  Never show a status code, a stack trace or JSON.
- Never claim to have checked an address for deliverability.
- Pass quantities to tools as numbers, always.
- **The customer's data comes from this conversation and nowhere else.** The
  agent never offers a name or an address it was not told here, and never
  implies it knows the customer already.
- When a tool reports an error, follow it: offer the named alternatives or ask
  the missing question. The system is right and the model is not.

---

## The web channel

The web UI is where a stranger decides whether this thing works. Everything
below is required, and each line is written so it can be checked by looking at
the page.

### The fixed HTTP surface

The server listens on **port 8888**. The routes, their bodies and their status
codes are part of the contract and the browser code depends on them:

| Route | Request | Response |
|---|---|---|
| `GET /` | — | the chat page |
| `GET /static/…` | — | the page's assets |
| `GET /config` | — | `{version, speech, lang_default, pizzerias, preselected_id, dashboard_base, docs_url}` |
| `GET /health` | — | `{api: "ok"｜"down", gateway: "ok"｜"down"｜"unknown"}` |
| `POST /session` | `{pizzeria_id?, lang?}` | `{session_id, pizzeria_id, pizzeria_name, lang}` |
| `POST /chat` | `{session_id, text, spoken?}` | NDJSON event stream |
| `POST /confirm` | `{session_id, revision}` | NDJSON event stream |
| `POST /language` | `{session_id, lang}` | `{lang}` |
| `POST /speech/stt` | multipart audio + `session_id` | `{text}` |
| `POST /speech/tts` | `{session_id, text}` | audio bytes |

Status codes, all normative:

- `404` — **unknown session** on any session-bound route, and every speech
  route while speech is disabled.
- `409` — the requested pizzeria is unknown or gone at session creation, and
  a turn already in progress for that session.
- `422` — `lang` outside `de|en`; a non-integer `revision`; an empty (but not
  absent) chat text; an empty text to synthesise.
- `502` — the speech service failed a request.
- `503` — the ordering API failed while creating a session.

`/config` contract details:

- `pizzerias` is fetched from the live API **on every call**. On failure it is
  `null` — never an empty list, never a bundled fallback — and the UI must
  then say the list is unavailable instead of offering a choice it cannot
  honour.
- `speech` is a boolean and is the **only** signal the page uses to decide
  whether speech exists at all.
- `dashboard_base` and `docs_url` are derived from the API base URL and never
  written into the page's source.

`/health` details: `api` is measured live per request against the ordering API;
`gateway` is the **process-wide last-known** status set by real model calls
from any session, and is `unknown` until the first one happens. `/health` must
never call the model gateway itself — a health check that costs a completion is
a health check nobody can afford to poll.

`/chat` with `text: null` is the opening turn: the agent speaks unprompted.
`spoken: true` marks a turn that arrived by microphone.

Both streaming routes emit newline-delimited JSON, one object per line, with
these event kinds: `user`, `tool_call`, `tool_result`, `state`, `assistant`,
`error`, and a final `done` carrying the full order snapshot. The last line of
every stream is `done` — including streams that failed. The same events, plus
a `language` event for a switch, are written to the session's log file; the log
is a superset of the stream and never carries a configuration value.

Turns are **serialized per session** by a lock the transport holds for the
whole stream. A second turn arriving while one is running is refused with
`409`, not queued and not run concurrently.

The `/confirm` route is the **only** path into `CONFIRMED` from the UI. It
dispatches `confirm_order` and, only if that succeeded, `submit_order` — both
recorded in the conversation exactly like model-issued calls, with synthetic
assistant tool-call messages and tool results — and then runs one **normal**
model turn to phrase the outcome. Same gateway path, same retry, same apology
behaviour as any other turn. Success and failure travel the same road.

### The conversation

Type or paste a message, get an answer. The exchange a first-time customer
should be able to have, end to end, without help:

> *What have you got?* → *What does a Margherita cost?* → *I'll take two of
> those and a pasta* → *I'm a new customer, my name is …* → read-back →
> confirm → order id and wait time.

After a completed order, a new conversation can start immediately from the
same page.

### Header

- **The pizzeria being ordered from, by name**, prominent and always visible,
  and used as the page title.
- **A selector to change pizzeria, filled from the API and from nowhere
  else.** No hardcoded names, no bundled list, no fallback entry when the call
  fails — if it fails, the page says the list is unavailable instead of
  offering a choice it cannot honour. Each entry shows the name plus a short
  form of its UUID so similar names can be told apart. Changing the selection
  starts a fresh conversation for that pizzeria.
- **A link to that pizzeria's dashboard**, opening in a new tab. Without it
  nobody can check whether the order arrived — and checking that is the entire
  point of the product.
- **Language: German or English**, switchable, applied to the UI chrome
  immediately and to the session language on the server.
- **Start over**, clearing the conversation and the basket by creating a new
  session for the same pizzeria.

### Footer

- **The running version**, `x.y.z`, from `APP_VERSION`.
- **The full pizzeria UUID**, selectable, for pasting into API calls.
- **Connection state** for the ordering API and the model gateway, as two
  badges carrying their state (`ok`, `down`, `unknown`), polled on a fixed
  interval. A failed poll leaves the last known state on screen rather than
  inventing a green one.
- **A link to the API documentation**, opening in a new tab.

### Every message gets an answer

The invariant this channel stands on: **no sent message may end without either
a rendered assistant reply or a rendered error.** Never a silent failure, never
an indicator that stops with nothing after it.

- The moment a message is sent, the UI shows the agent is working, and the
  send control is disabled until the turn ends.
- Intermediate steps render as they stream — which tool was called and what it
  returned — visually distinct from the assistant's words and collapsed by
  default. **A stream whose tool events the page discards is a defect:** the
  customer sees a frozen screen while the agent works normally.
- If the stream ends without a final assistant message, the UI says so and
  offers to resend.
- If the request errors, times out, or the connection drops, the UI says which
  of those happened and offers to resend. The timeout must be a **real
  client-side timeout covering the streamed body**, not only the initial
  response — otherwise a stream that stalls forever produces the one thing
  this invariant forbids: a spinner with nothing after it.
- A `409` (turn already running) is shown as a short, plain "one moment"
  notice — it is not an error and offers no resend.
- Errors in the customer's language, in plain words. No status codes, no
  tracebacks, no raw JSON.

### The order on screen

- The current basket is always visible, with quantities, line totals and what
  it comes to. The code owns the order; the customer must see what the code
  holds. Every snapshot that arrives in the stream re-renders it.
- When any line carries extras, the panel states that extras are not priced
  separately — an unexplained line total invites the belief that the total is
  wrong.
- The read-back is visually distinct and carries an explicit confirm control.
  **Confirmation is an action the customer takes, not a word the agent claims
  to have heard.** The control carries the exact revision that was read back,
  and any earlier read-back's control is disabled the moment a newer one
  appears.
- On success: the order id, readable, and the wait in minutes.
- After submission the basket is locked and shown as submitted, carrying the
  order id. Nothing on the page can modify or resubmit it.

### Sessions and tenancy in the browser

- **Switching pizzeria creates the new session first**, and only then aborts
  any in-flight stream and clears the conversation. If creation fails, the
  page keeps the live conversation and basket, says that pizzeria is not
  available right now, and re-reads the selector from the live list. A failed
  switch must never leave the customer staring at a cleared screen.
- **An unknown session (`404`) is recovered transparently**: the page creates
  a fresh session, tells the customer the session was lost in one plain
  sentence, and — for a chat message only — offers to resend it. A pending
  **confirm is never re-offered** after such a recovery: the new session holds
  a new, empty order, so the old revision means nothing.
- **A failed confirm is retried with the same revision**, never a new one. If
  the first attempt did go through, the state machine refuses the retry and
  the agent says so. A retry can therefore never place a second order.
- The page holds exactly one session at a time and sends only identifiers to
  the server. It never computes a total, never decides a state, and never
  keeps its own copy of the basket.

---

## Speech

Speech is an input and an output method on the web channel, served by a
**self-hosted speech service**: CPU-only, in its own container, reached over
plain HTTP with an OpenAI-compatible surface.

| Direction | Endpoint | Payload |
|---|---|---|
| STT | `POST {SPEECH_URL}/v1/audio/transcriptions` | multipart audio + model + language |
| TTS | `POST {SPEECH_URL}/v1/audio/speech` | JSON: model, voice, input text, language → audio |

- **Speech is never required.** With the `SPEECH_*` variables unset, or the
  service not answering at startup, the microphone and the read-aloud toggle
  are not rendered, the speech routes answer `404`, and the text UI is fully
  usable — including placing a complete order. A speech failure is never an
  order failure, and no part of the ordering path may depend on speech being
  present.
- **All-or-nothing enablement.** Speech counts as available only when the base
  URL and all three model/voice ids are configured **and** a short startup
  probe against the service returned `2xx`. A half-configured speech stack is
  treated exactly like an absent one, and it says so on standard error rather
  than failing the process.
- **The speech service is the only speech path.** No external speech provider,
  no hosted realtime framework, no audio through the model gateway — that
  gateway carries chat completions only.
- **The browser captures and plays audio; it does not recognise or synthesise
  it.** Capture with `getUserMedia` and `MediaRecorder`, playback through a
  plain audio element. Recognition and synthesis happen server-side.
- **The browser speech APIs are forbidden.** `SpeechRecognition` and
  `speechSynthesis` tie the product to a single browser vendor and send
  customer audio to a third party. The self-hosted service exists to replace
  them.
- **The page must survive plain HTTP.** Whether speech exists at all is
  decided solely by the server's `speech` flag. Only the **microphone** is
  additionally gated, and only on the two capabilities it actually needs —
  `navigator.mediaDevices` and `MediaRecorder`. Read-aloud must therefore
  keep working on a page served over plain HTTP where capture is unavailable;
  gating the whole speech UI on one browser capability check silently kills
  output too, and that is a defect.
- **Nothing about the speech stack is written into source.** Base URL, models
  and voice come from the environment, exactly like the chat model; the
  language sent with STT and TTS requests is the session language (see
  *Language authority* under *Conversation policy*), not a separate
  configuration value.
- **Request/response, not streaming.** Record, upload, transcript back.
  Latency is visible and acceptable; do not build partial results, barge-in or
  turn detection on top — this transport cannot do them, and pretending
  otherwise produces a broken feel.
- **Push-to-talk.** The microphone starts and stops on the customer's action
  and never listens continuously. The recording state is visible at all times
  and exposed to assistive technology.
- **Synthesis is optional and off by default**, toggled by the customer,
  applied **only to the final assistant message** of a turn — never to
  intermediate steps, never to notices.
- A transcription that comes back empty, or a speech request that fails,
  leaves a plain notice on the page and the text input untouched. Denied
  microphone permission says so and changes nothing else.
- **Speech shortens answers, it does not change them.** Same core, same tools,
  same state machine. When a reply will be spoken, the turn carries an
  **ephemeral** instruction to that effect: at most three dishes plus an
  invitation, times in minutes, order ids in groups, short sentences. That
  instruction must **never** be persisted into the conversation history — a
  later typed turn must not inherit the spoken constraints.
- **Confirm the name.** Transcription errors on names are the expensive
  failure: a misheard name silently creates a customer nobody will find again.
  Read the name back before submitting.

---

## Error handling

Every case below needs a test and a phrasing.

| Situation | Code does | Customer sees/hears |
|---|---|---|
| Gateway timeout | exactly one retry, then abort the turn | plain apology, rendered as the turn's assistant message, offer to resend |
| Gateway unreachable / malformed reply | abort the turn, mark the gateway down | same apology, visible on the page |
| Tool loop guard exceeded | abort the turn after a fixed maximum of tool rounds | same apology |
| `401`/`403` from the ordering API | abort, log, **do not retry** | "I can't reach the kitchen system right now" |
| `404` on the preselected `PIZZERIA_ID` | fail at startup, not mid-call | — (process refuses to start) |
| Runtime pizzeria selection invalid/gone | session error (`409`); refresh the selector; process stays up | "that pizzeria isn't available right now" |
| `422` validation on submit | surface the offending detail, **keep the basket** | targeted question about the offending item |
| `5xx` on submit | **no blind retry**; mark the attempt unverified | "I'm not sure that went through — let me check" |
| Timeout on submit | mark the attempt unverified; shortlist, then verify, before any retry | as above |
| Unknown item code | `unknown_item` + up to three candidates | "I have Margherita or Marinara — which one?" |
| Unknown extra | `invalid_extra` + up to three candidates | "I can't add that topping — did you mean …?" |
| Empty basket at submit | reject the transition | "What can I get you?" |
| Mutation after submission | reject the transition | "That order is already on its way to the kitchen" |
| Menu fetch fails at start | fail fast | "We're not taking orders right now" |
| Pizzeria list fetch fails | no selector, say so | list unavailable — no fallback entry |
| Speech service down | hide the speech controls / `404` on speech routes | text UI unaffected |

**The gateway apology is a real assistant message.** It is appended to the
conversation and emitted as an `assistant` event so the page renders it like
any other reply. An apology that exists only in a log is the silent failure
this product forbids.

**The submit-timeout case is the one that matters**, because a blind retry
doubles a real order. Recovery, in this exact order:

1. Mark the attempt unverified and record the attempt time once.
2. On the next submit attempt, read the pizzeria's order **list** and shortlist
   entries whose `first_name` matches and whose `created_at` is no older than
   the attempt time minus a small clock-skew allowance (one minute).
3. For the most recent candidate, fetch the **detail** endpoint and compare its
   items — type, code, quantity and extras, order-independent — against the
   basket. The list carries no items and can never prove a match on its own.
4. Only an exact match is adopted as the order that was placed, with the
   remaining wait derived from its `ready_at`. Anything else — no candidate, a
   candidate whose items differ — allows **exactly one** real retry.
5. If the list or the detail lookup fails, tell the customer honestly that it
   is unclear whether the order went through. Never guess, never retry blind.

Every legal basket mutation clears this recovery bookkeeping: after a change,
the unverified attempt no longer describes the basket in hand.

The ordering API client uses explicit timeouts on every call and maps
responses to typed errors — auth, not-found, validation (with details), server
error, timeout. No caller inspects a status code directly.

---

## Anti-patterns — explicitly forbidden

Each of these is a way to make this product look finished while it is broken.
None is a matter of taste.

1. **A regex "fast path" that places an order without the model.** It bypasses
   confirmation, mis-parses quantities, duplicates items on overlapping
   matches, and makes the tool-calling architecture decorative.
2. **Shelling out to `curl` via a subprocess.** Use an HTTP client: no shell
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
6. **A frontend that discards stream events.** Rendering only the final
   message and throwing the tool events away leaves the customer watching a
   frozen screen while the agent works normally. Rendering the intermediate
   steps is part of the product, not a debug view.
7. **Order logic in a transport.** A channel that computes a total, decides a
   state, or keeps its own copy of the basket has forked the truth. Channels
   forward identifiers and render events; that is all.
8. **Proving the web channel with `curl`.** It proves the server answers and
   proves nothing about the product. The customer never talks to `curl`.

---

## Testing

- **Unit: the state machine, exhaustively.** Every illegal transition has a
  test asserting it is refused, and every invariant above has a test naming it
  — including demotion after confirmation, the revision-bound confirm, the
  read-back requirement, terminal `SUBMITTED`, line merging, both removal
  semantics, and the single submit-attempt timestamp.
- **Tool level, against recorded API fixtures.** No network, no LLM, fast.
  Cover at least: per-type code collisions, candidates for an unknown code and
  an unknown extra, atomic rejection of a bad add, refusal to parse a spelled
  quantity, price copied at add time, cent-exact totals that do not drift, the
  street key omitted from the submit body, typed mapping of `401`/`404`/`422`/
  `5xx`/timeout, and the **complete submit-timeout recovery matrix**: recovery
  via list plus detail, a candidate with different items rejected, verified
  absence allowing exactly one retry, an unavailable list reported honestly,
  and a mutation clearing the recovery state.
- **Golden transcripts:** five scripted conversations against a stub model
  replaying fixed tool calls — happy path, correction, unknown item, customer
  changes their mind after the read-back, submit timeout. Assert the final
  state, the exact sequence of tool calls made, the error codes raised, and
  the final basket.
- **Browser end-to-end, not optional.** Headless-browser tests drive the real
  page against a stub ordering API and a stub scripted gateway — type a
  message, wait for a rendered reply, walk a full order to submission —
  asserting **against the DOM**, never against the API. The suite must cover
  the header and footer contract, a pizzeria switch, a vanished pizzeria
  refreshing the selector, a lost session recreating and offering resend, and
  three failure paths: a tool error, a stream ending without a final message,
  and the gateway unreachable. Each must leave a visible message on the page.
- **API-surface tests** for the fixed contract above: the `/config` payload,
  `pizzerias: null` with no fallback, `gateway: "unknown"` before the first
  turn and `"ok"` after it, `404` for an unknown session, `409` for an unknown
  pizzeria and for a turn already in flight, `422` for a bad language and a
  stale/non-integer revision, and a tool error surfacing as plain language in
  the stream.
- **The acceptance test is live**, opt-in behind an environment flag, and is
  the only test that touches the real API. It runs a full order through the
  tools, submits, then reads the order back — **presence via the order list,
  and customer, items and quantities via the detail endpoint**, because the
  list carries no items and cannot verify them — and asserts the four points
  under *What done looks like*. If this fails, the product does not work,
  whatever else is green.
- **Speech, manual:** dictate an order; dictate a name that needs correcting
  and check that the agent repeats it back; ask a menu question; and one run
  with the speech configuration removed, which must render a usable text-only
  UI and place an order normally.
- The whole offline suite runs with no network and no LLM, in one command.

---

## Who builds this — and who judges it

Two roles take part and they are **not** interchangeable.

| Role | Permission |
|---|---|
| Implementer — one coding agent | writes every file |
| Reviewer / judge — a second, independent agent | read-only, never writes |

Which products and models fill these roles is the operator's decision and is
deliberately left out of this spec: tools are replaced long before the product
is. The roles and the protocol are binding; the tooling is not.

- **One implementer, and nothing else develops.** Every artefact in
  *Deliverables* comes from it. No second implementer, no hand-patched fixes
  between rounds.
- **The reviewer never writes the code it judges.** Read-only, two roles in
  one call: *devil's advocate* — attack the work, find gaps, wrong
  assumptions, missing error cases — and *judge*, scoring against the fixed
  rubric so quality is measurable instead of a vibe.
- **The reviewer is a different agent from the implementer.** Independence is
  the point; a model reviewing its own output is not a review.

### Two model domains, never mixed

- **Build-time models** power the harnesses. Configured outside this product,
  none of this spec's business. Nothing in the deliverables reads, references
  or depends on them.
- **Runtime models** are what the ordering agent calls while serving a
  customer: `LITELLM_PIZZA_MODEL_1` and `_2` from the environment.

Binding consequences:

- The implementer never wires the agent to whatever model the implementer
  itself runs on, and never copies a build-time model name into source,
  configuration, prompts, tests or documentation.
- No model name of any kind is hardcoded. A missing runtime value is a startup
  failure, not a default.
- **Harness is not model.** Never ask an agent which model it is — a
  self-report is not evidence; the configuration is binding.
- Whatever the build runs on, it does not lower the bar. Do not simplify the
  design, skip a test, or accept a weaker answer on the assumption that the
  model behind you is limited.

### Review protocol

Reviewer calls are **stateless** — a fresh reviewer sees nothing of the
previous round, so every request carries its own context. Commit before each
review so the reviewer always sees a committed tree.

```
SCORES (1-5 each, 5 = best):
completeness: N
correctness: N
error_handling: N
simplicity: N
spec_compliance: N
TOTAL: N/25
VERDICT: APPROVED | CHANGES_REQUIRED
ISSUES: (max 5 bullets, concrete and actionable, empty if approved)
```

- `APPROVED` requires `TOTAL >= 20` **and** no dimension below 4. If the
  verdict line says approved but the scores miss that bar, **the numbers
  win** — a verdict is a sentence and the scores are the measurement.
- Maximum 3 rounds per stage. Still not approved after round 3 → stop, show
  the scores and the open issues. A valid outcome, not a failure.
- Disagreeing is allowed — a one-line rebuttal in the next request. Never
  ignore a finding silently.
- Every reviewer output is written to a file under `reviews/`, every round's
  scores into `reviews/scores.md`, and `reviews/` is committed.

### Two stages, in this order

1. **PLAN.** Write `PLAN.md`: file layout, tool schemas, state machine, agent
   loop, error handling, conversation state. **No code.** Iterate with the
   reviewer until `APPROVED`. Implement nothing before that.
2. **IMPLEMENT.** Only after the plan is approved. Build exactly the approved
   plan, then iterate the diff with the reviewer until approved.

"Done" means the judge approved — not that the code runs. Working code that
fails the rubric is not done.

---

## How to work

This is an autonomous build. No clarifying questions will be answered and no
feedback arrives until you are done — every decision inside these constraints
is yours. Work in passes and verify after each; do not write the whole thing
and then run it once.

The stack: Python with one virtual environment, an HTTP framework and an ASGI
server for the web channel, one HTTP client used everywhere, one test runner,
one headless-browser driver, and multipart support for the audio upload.
Nothing else. Pin every dependency to an exact version in `requirements.txt`.

0. **Contracts.** Confirm the contract facts against the live API, move any
   answer into the facts, commit. The open list only shrinks — a fact
   confirmed against the live service never becomes a question again.
1. **Core.** Order model, state machine, menu snapshot, tool layer, tests. No
   LLM, no network. Pass when the unit tests are green.
2. **Agent loop.** Model, tools, system prompts, JSONL logging, one turn end
   to end.
3. **CLI.** Full conversation, real API, an order visible on the dashboard.
4. **Web.** The fixed HTTP surface on 8888, same core. Pass **only** when you
   have opened the page in a browser, switched pizzeria, asked a price
   question, placed an order through the page, and seen it on that pizzeria's
   dashboard — not when the endpoint answers `curl`.
5. **Speech.** Wire the speech service into the web UI, the spoken-answer
   policy, and the degraded no-speech path. Verify the no-speech path by
   removing the configuration and placing a complete order as text.
6. **Harden.** Walk the error table, force each case, fix what breaks.

After each pass, review your own work as the reviewer who has to reject it:
what would a hostile reader find first? Fix that, then move on. Stop only when
a full pass over this file finds nothing left that you know how to improve.

---

## Deliverables

```
.
├── SPEC-RELEASE-1.0.0.md    ← this file
├── README.md                ← how to run each channel
├── PLAN.md                  ← written before any code, updated as you go
├── requirements.txt         ← exact pins
├── .env.example             ← names only, never values
├── core/
│   ├── order.py             ← Order, basket, revision, snapshot, money
│   ├── state.py             ← state machine, transitions, invariants
│   ├── menu.py              ← menu snapshot, (type, code) validation, candidates
│   ├── pizzasim.py          ← API client, typed errors, timeouts, env loading
│   ├── tools.py             ← the eight tool schemas + dispatch
│   └── agent.py             ← session factory, model loop, prompts, logging
├── channels/
│   ├── cli.py
│   ├── web.py               ← the fixed HTTP surface, port 8888
│   ├── speech.py            ← speech service client
│   └── static/
│       ├── index.html
│       ├── app.js           ← stream rendering, basket, confirm, speech
│       └── style.css
├── prompts/
│   ├── system.de.md
│   └── system.en.md
├── tests/
│   ├── fixtures/            ← recorded API responses
│   ├── stubs.py             ← stub ordering API + stub gateway, on localhost
│   ├── test_state.py
│   ├── test_tools.py        ← incl. the opt-in live acceptance test
│   ├── test_transcripts.py  ← the five golden conversations
│   ├── test_web_e2e.py      ← API surface + headless browser, DOM assertions
│   └── transcripts/
└── reviews/                 ← one file per review round, plus scores.md
```

Event logs are written at runtime to `logs/agent-<session>.jsonl`, one JSON
line per event, and are not committed. `logs/`, the virtual environment and
any local `.env` belong in `.gitignore`.

---

## Decisions locked

| Area | Decision |
|---|---|
| Order ownership | Code. The model never holds the cart. |
| Submit | Single call, only from `CONFIRMED`, never auto-retried |
| Submit recovery | Shortlist on the order list, verify items on the detail endpoint, adopt only an exact match |
| Menu | Fetched live once per conversation, immutable for its lifetime, no fallback list |
| Item identity | `(type, code)` — never a code alone |
| Tenancy | Customer-selectable; `PIZZERIA_ID` preselects, never restricts; tenant in the URL path |
| Session | One order, one menu snapshot, one tenant-bound client, one language; the tenant never changes |
| Pizzeria selector | Filled from the API only; no fallback entry |
| Prices | Shown from the API; no payment, no invented figures |
| Totals | Computed in code with exact decimal arithmetic; the model never does arithmetic |
| Language | Session language from `PIZZERIA_LANG`, switchable in the web header; per-turn mirroring wins for replies |
| Transports | One core, two channels (CLI, web), no logic in the channels |
| Concurrency | One turn at a time per session, enforced by the transport |
| Speech | Optional, self-hosted container, OpenAI-compatible HTTP; no vendor, no browser speech API |
| Web UI | Pizzeria name, basket and connection state always visible; no message ends unanswered |
| Confirmation | Mandatory read-back tied to a basket revision, taken as an explicit customer action |
| Version | `x.y.z` in the footer, validated at startup, raised every release |
| Derived URLs | Dashboard and docs built from `PIZZASIM_URL`, never literal |
| Languages | DE + EN, mirrored per turn |
| Parsing | The model parses. No regex order parser, ever. |
| HTTP | A real client with explicit timeouts. No subprocess `curl`. |
| Persistence | None beyond the process and the PizzaSim API |
| Errors | Typed in code, plain language to the customer, never a raised exception out of the tool layer |
| Contract facts | Confirmed facts never return to the open list; the list only shrinks |
| Implementer | One agent only — nothing else writes code |
| Reviewer | A second, independent agent, read-only, judge and devil's advocate |
| Models | Never named, never hardcoded — environment configuration |
| Build tooling | Not specified here; the operator picks it |
| Proof | Verified through the browser and the live API, never only through `curl` |
| Definition of done | The judge approved, not "it runs" |

## Decisions deferred

- Extras and modifiers beyond a passthrough `extras[]`.
- Post-submit modification or cancellation.
- Reusing a returning customer's stored address instead of asking for it
  again, and any other memory across conversations ("the usual").
- Additional languages beyond DE + EN.
- Telephony as a third channel.

---

## Ticket sizing rules

- Each ticket is **one hour or less** of implementation.
- Prefer three narrow tickets over one broad one. Split by file, by component,
  or by "schema / implementation / tests".
- Every ticket carries acceptance criteria as a checklist.
- Tests belong to the ticket that introduces the behaviour, never to a
  follow-up.

---

## Twenty-four rules that decide whether this works

Everything above is binding. These twenty-four are the ones that quietly decide
whether the order lands correctly, and each is the compressed form of a rule
stated in full in the section named after it.

1. **List versus detail.** The order list carries no items, so items and
   quantities must **only** ever be verified through the single-order detail
   endpoint — in timeout recovery and in the acceptance test alike. *(The
   PizzaSim API; Error handling; Testing)*
2. **Language authority.** The session language comes from `PIZZERIA_LANG` and
   the header switch, but for the agent's replies per-turn mirroring wins: it
   **must** answer in the language of the customer's latest message and never
   comment on the switch. *(Conversation policy)*
3. **Money in code.** Totals are computed in code with exact decimal
   arithmetic from the prices captured in the menu snapshot; the model never
   does arithmetic on prices. *(Tools)*
4. **One immutable snapshot per conversation.** A conversation fetches its menu
   once, at creation, and never refetches; the session factory owns tenant
   validation, client construction and prompt rendering. *(The One
   Load-Bearing Idea; Decisions locked)*
5. **Revision-bound confirmation.** `confirm_order` must name the revision that
   was read back, and a stale or non-integer revision is refused. *(Order
   state machine, invariant 3)*
6. **Never a blind retry after a submit timeout.** Shortlist by name and time,
   verify items on the detail endpoint, adopt only an exact match; anything
   else allows exactly one retry, and a failed lookup is reported honestly.
   *(Error handling)*
7. **Every message gets an answer.** No sent message may end without a
   rendered assistant reply or a rendered error — including a stream that
   stalls, which a real client-side timeout must catch. *(The web channel)*
8. **Deterministic removal.** Without `qty` every line matching `(type, code)`
   is removed; with `qty` only the most recently added matching line is
   reduced. *(Tools)*
9. **A mutation clears recovery state.** Any legal basket change **must**
   discard the correlation of an unverified submit attempt — it described a
   basket that no longer exists, and it is never carried into a new one.
   *(Order state machine)*
10. **One turn at a time per session.** A second turn arriving mid-stream is
    refused with `409`; it is never queued and never run concurrently. *(The
    web channel)*
11. **Apologies are assistant events.** A gateway failure produces a real
    assistant message, appended to the conversation and emitted to the page —
    never a failure that exists only in a log. *(Error handling)*
12. **The `/config` contract.** The pizzeria list is read live on every call
    and is `null` on failure — never an empty list, never a fallback entry —
    and the page must then say the list is unavailable. *(The web channel)*
13. **`APP_VERSION` is validated.** It must match `x.y.z` at startup or the
    process refuses to start, and it is shown in the footer. *(Environment)*
14. **Plain-HTTP survivability.** Whether speech exists is decided only by the
    server's `speech` flag; **only** the microphone is additionally gated, and
    only on `mediaDevices` and `MediaRecorder`, so read-aloud keeps working
    where capture does not. *(Speech)*
15. **A lost session is recreated transparently.** A `404` creates a fresh
    session with one plain notice; a chat message may be resent, a pending
    confirm never is. *(The web channel)*
16. **A confirm retry uses the same revision.** Never a new one — so a retry
    can never place a second order. *(The web channel)*
17. **The spoken-style instruction is ephemeral.** It applies to the one turn
    that will be spoken and is never persisted into the conversation history.
    *(Speech)*
18. **Item codes are per type.** The same code exists as a pizza and as a
    pasta at different prices, so validation, pricing and removal **must** key
    on `(type, code)` and never on a code alone. *(The PizzaSim API; Tools)*
19. **Adds are atomic.** One invalid item, extra or quantity **must** reject
    the whole call and leave the basket untouched; a partial add is a defect.
    *(Tools)*
20. **Switch order and stream timeout.** Switching pizzeria **must** create the
    new session before aborting the in-flight stream and clearing the screen,
    and the stream timeout **must** cover the streamed body, not only the
    response headers. *(The web channel)*
21. **Gateway status is observed, never probed.** `/health` measures the
    ordering API live and reports the process-wide last-known gateway status
    from real calls; it is `unknown` until the first one and `/health` never
    calls the gateway itself. *(The web channel)*
22. **The numbers win.** An `APPROVED` verdict that misses `TOTAL >= 20` with
    no dimension below 4 must **never** be treated as an approval. *(Review
    protocol)*
23. **The open list only shrinks.** A fact confirmed against the live service
    never returns to the open contract questions. *(The PizzaSim API)*
24. **The live acceptance test is the definition of working.** It is opt-in and
    the **only** test that touches the real API: presence via the order list,
    customer, items and quantities via the detail endpoint. If it fails the
    product does not work, whatever else is green. *(Testing)*
