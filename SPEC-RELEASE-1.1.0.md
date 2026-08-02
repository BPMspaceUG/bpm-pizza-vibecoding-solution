# PizzaSim Ordering Agent — Specification

> Hand this to a coding agent as the entire task:
> `FOLLOW INSTRUCTIONS PRECISELY AT "SPEC-RELEASE-1.1.0.md"`.
> This file is the source of truth for what the product is. Everything else in
> the repository — code, tests, prompts, tickets — derives from it.

---

## Where this format comes from

The **shape** of this document is not ours. It is borrowed from Cedric Mössner —
**The Morpheus** (<a href="https://www.youtube.com/@TheMorpheusTutorials" target="_blank">youtube.com/@TheMorpheusTutorials</a>),
who writes exactly one specification file per project and hands the identical
file to every new model in order to compare them. The prompt he sends alongside
it is a single line — `FOLLOW INSTRUCTIONS PRECISELY AT "<the spec file>"` —
which is why that line, and not a long prompt, stands at the top of this file.

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
5. **A spoken conversation on the web channel produces the same verified
   outcome as points 1–4**: the customer speaks the order into the microphone,
   the agent answers aloud, and the order that lands in the API is correct.
   Voice is not a demo mode — it is a way to reach points 1–4.

Nothing else counts as done. A green test suite, a clean architecture, a
pleasant interface: none of it is the product. **The order on the board is the
product.**

**Five failures that look like success**, each a failed run and not a partial
one:

- The order landed under a **different pizzeria** than the one the customer
  chose.
- A retry after a timeout created the order **twice**.
- A misheard or mistyped name created a **new customer** instead of matching
  the intended one.
- The order was submitted **without the customer confirming** the read-back.
- A **saved street address was disclosed** to whoever claimed the matching
  first name — read out, printed on screen, written into a log, or handed to
  the model.

Every rule below — the state machine, the revision-bound confirmation, the ban
on blind retries, the name read-back, the tenant in the URL path, the
saved-address redaction — exists to prevent exactly one of those five.

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
never reaches the kitchen without a confirmed read-back, and never gets to see
a returning customer's saved address.

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
- Data the customer never dictated — a street the code looked up on their
  behalf — is copied **inside the code** and never passes through the model.
- One core serves every channel. A transport carries words in and words out;
  it owns no order logic whatsoever. Speech is a transport concern: it changes
  how words arrive and leave, never what the order is.

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
- **Voice on the web transport is a required product capability.** Push-to-talk
  speech input and read-aloud speech output are served by the self-hosted
  speech service described in *Speech*. A build whose voice path does not work
  is not finished. If the service is unconfigured or unavailable at runtime,
  ordering degrades to text-only without breaking ordering.
- **Several pizzerias.** The customer chooses which one they are ordering
  from, and can change it. `PIZZERIA_ID` is the preselection, not a
  restriction.
- **Returning customers.** A known first name may reuse its saved street after
  exactly one explicit confirmation, and the address text is never disclosed to
  the customer, the model, the page, or the logs. Reuse is limited to the
  address held by the ordering API.
- **Languages:** German and English. The agent answers in the language the
  customer used, per turn, without being told to switch.
- **Menu, prices, cart, customer, submit.** The full happy path plus
  correction ("no, make that three"), removal, and abandonment. The customer
  can ask what is on offer and what items cost, and sees what the basket
  comes to before confirming.
- **Deterministic tests** that run with no network and no LLM, plus browser
  end-to-end tests including the voice path, and opt-in live acceptance tests.
- **Structured logging** of every turn: user text, model tool calls, tool
  results, state transitions. One line per event, JSON, to a file.

### Out (explicitly)

- Payment and anything financial beyond showing prices the API supplies.
- Delivery routing, or an ETA of our own invention.
- Accounts, auth, sessions surviving a process restart.
- Modifying or cancelling an order after it was submitted.
- Any regex or keyword parser that produces an order without the model.
  See **Anti-patterns**; this is a hard ban, not a style preference.
- Reuse of a second saved address line: only the address field the order write
  contract accepts may be reused. See *The PizzaSim API*.
- Cross-session memory beyond saved-address reuse — "the usual" stays out.
- Streaming speech, partial transcripts, barge-in, or turn detection.
- Reading the whole menu aloud when the answer will be spoken.
- Persisting customer data anywhere beyond the process and the PizzaSim API.

---

## Environment and configuration

All configuration comes from environment variables. The process environment
wins; otherwise `~/.env` is read if present. That file is **never written,
never created, and no value from it is ever printed**.

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
| `APP_VERSION` | Version, `x.y.z`, shown in the footer |
| `SPEECH_URL` | Base URL of the self-hosted speech service |
| `SPEECH_STT_MODEL` | Transcription model id |
| `SPEECH_TTS_MODEL` | Synthesis model id |
| `SPEECH_TTS_VOICE` | Voice id |

That table is the complete set. Nothing outside this file is needed to know
which values a deployment must supply.

Rules:

- **Nothing is hardcoded.** No UUID, no model name, no menu, no base URL, no
  vendor — not even as a fallback "just in case".
- A missing or empty **required** variable is a startup failure: the process
  exits before the first turn with a message naming the variable and the file
  it was expected in. Never start half-configured. Required are
  `LITELLM_PIZZA_URL`, `LITELLM_PIZZA_KEY`, `LITELLM_PIZZA_MODEL_1`,
  `PIZZASIM_URL`, `PIZZASIM_API_KEY`, `PIZZERIA_ID`, `PIZZERIA_LANG` and
  `APP_VERSION`.
- `PIZZERIA_LANG` must be exactly `de` or `en`; anything else is a startup
  failure.
- `APP_VERSION` must match `x.y.z` exactly (three dot-separated integers);
  anything else is a startup failure. The version this specification describes
  is `1.1.0`. It is raised on every release: patch for fixes, minor for new
  behaviour, major for a break.
- The four `SPEECH_*` variables are **required for a complete release** and
  optional only for local development and for the explicit text-only test
  scenario. When any of them is absent, the speech path is off, the voice
  controls are not rendered, and text ordering must remain fully usable.
- Secrets never appear in logs, transcripts, error messages or the web UI.
- **Every dependency is pinned to an exact version** — no ranges, no "latest".
  The stack is Python 3.11 or newer with: FastAPI and uvicorn for the web
  channel, `httpx` as the single HTTP client everywhere, `python-multipart` for
  the audio upload, `pytest` as the test runner, and a browser-automation
  library able to launch a headless browser with a fake microphone device.
  A `Procfile` starts the web channel via uvicorn, binding `0.0.0.0` and the
  port from `PORT`, defaulting to 8888.

---

## The PizzaSim API (contract)

Facts below are **verified** — against running code or a live response. A
verified fact never moves back into the open list; the open list only shrinks.

| Call | Auth | Notes |
|---|---|---|
| `GET /menu` | public | returns `pizzas[]` and `pasta[]`, each with `code`, plus `toppings[]` |
| `GET /pizzerias` | `X-API-Key` | list of pizzerias with `id`, `name` |
| `GET /pizzerias/{id}/orders` | `X-API-Key` | that pizzeria's orders; used by timeout recovery |
| `GET /pizzerias/{id}/orders/{order_id}` | `X-API-Key` | the full order incl. `customer` and `items[]` |
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

- Dashboard of a pizzeria: `{PIZZASIM_URL}/dashboard/pizzerias/{id}`.
- API documentation: `{PIZZASIM_URL}/swagger.html` — there is **no** `/docs`.

Facts that shape behaviour:

- The tenant is **always** in the URL path, never in a header. The API key is
  a server key, not a pizzeria id.
- Customers are unique per pizzeria **by first name**. An unknown name
  silently creates a new customer — a misheard name creates a ghost. Spoken
  input must therefore confirm the name explicitly.
- `street_one` is optional and **not** validated for deliverability. Asking
  for it is a policy of this agent — never claim to have checked an address.
- `POST /orders` is **not** idempotent. A retry after a timeout can double a
  real order. See **Error handling**.

Further verified facts:

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
  `GET /pizzerias/{id}/orders/{order_id}` returns the full order incl.
  `customer` and `items[]`. Submit-timeout recovery shortlists by
  `first_name` + `created_at` recency on the list, then **verifies the
  candidate's items via the detail endpoint before adopting it**; the live
  acceptance tests assert items and quantities through the same detail
  endpoint.
- **Item codes are unique per type, not globally** — `tonno` exists as a
  pizza and a pasta. Validation and removal always key on `(type, code)`.
- **The customers endpoint** `GET /pizzerias/{id}/customers` returns
  `customers[]` with `{id, first_name, street_one, street_two, created_at,
  deleted_at}`. Since customers are unique per pizzeria by `first_name`, a
  first name resolves to at most one saved address. **A record with a
  non-empty `deleted_at` does not exist**: the client filters it out before
  any caller sees it, so a deleted customer is indistinguishable from an
  unknown one. Guardrail: the verified order-write contract proves only
  `street_one`, so address reuse **must** be limited to `street_one` until
  `street_two` support on `POST /orders` is verified as well.

### Open contract questions — shrink-only

Resolve against the live API before the affected component is implemented,
then move the answer up into the facts and delete the question. Never guess.
A verified fact never returns here.

*(empty — every fact above is stated as verified. If the live API contradicts
one, verify it against the live API and correct the fact; never work around it
by guessing.)*

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
   revision counter; `confirm_order` must name it, and the revision must be a
   plain integer — a boolean is not an integer and is refused as stale.
4. `SUBMITTED` is terminal. The conversation may continue; the order may not.
   Every mutating transition on a submitted order is refused with a spoken
   sentence offering to start a new order.
5. An item enters the basket only with a `code` present in the menu snapshot
   fetched this session.
6. A basket never crosses a tenant boundary. Changing pizzeria starts a fresh
   conversation and a fresh order.
7. **Any mutation voids an unverified submit attempt.** When a submit timed
   out and the outcome is unknown, and the basket then changes, the pending
   "did it go through?" bookkeeping is cleared: the recovery correlation
   belongs to the basket that was confirmed then, not to whatever the basket
   becomes now.

Every legal mutation raises the revision counter and recomputes the state from
the data: no items → `EMPTY`, items but no customer → `COLLECTING`, items and
customer → `READY`.

---

## Tools

The model sees exactly these nine tools. Names, parameters and semantics are
fixed; nothing else is exposed to the model.

| Tool | Parameters | Returns |
|---|---|---|
| `get_menu` | — | pizzas and pasta with codes, display names, prices, plus the available extra toppings |
| `add_items` | `items[]` of `{type, code, qty, extras[]}` | new basket + revision |
| `remove_item` | `type`, `code`, optional `qty` | new basket + revision |
| `lookup_customer` | `first_name` | `{customer_exists, saved_street_available}` — **booleans only, never street text** |
| `set_customer` | `first_name`, plus either `street_one` **or** `use_saved_street: true` (mutually exclusive) | customer as stored (a saved street appears as a flag, never as text) |
| `read_back` | — | basket, customer name, revision, and the code-computed basket total — the text the agent reads out |
| `confirm_order` | `revision` | state `CONFIRMED`, or an error if stale |
| `submit_order` | — | `order_id`, `status`, `eta_seconds` |
| `check_street` | `street` | plausibility result (optional) |

Tool result conventions:

- Success: the **full current state**, not a diff. Every successful result
  embeds the complete snapshot — state, revision, item lines with unit price
  and line total, basket total, customer, and whether the current revision has
  been read back. The model never reconstructs the basket from history.
- Failure: `{"error": {"code": "...", "message": "...", "candidates": [...]}}`.
  `message` is written so it can be spoken to the customer as-is.
- **Dispatch never raises.** Every failure — an invalid transition, a menu
  error, an API error — comes back as a tool result the model must deal with in
  front of the customer. API failures map to `api_unavailable` with a spoken
  sentence.
- `add_items` with an unknown code returns `unknown_item` plus up to three
  candidates from the menu, matched within the requested type first and the
  other type as fallback. The model asks; it does not pick.
- **`add_items` is atomic.** If any item or extra in the call is unknown, the
  whole call is rejected and the basket is unchanged. A partial add never
  happens.
- Quantities are integers ≥ 1. A tool receiving `"zwei"` returns
  `invalid_quantity`; it does not parse German. A boolean is not an integer.
- **Totals are computed in code**, from the API prices captured in the
  session's menu snapshot, in exact decimal arithmetic rounded to cents
  (half-up) — never by accumulating floats. The model never does arithmetic on
  prices; the web basket shows the same code-owned total that `read_back`
  carries. The unit price is copied onto the basket line at add time.
- `remove_item` parameters are fixed, so when several basket lines share
  `(type, code)` with different `extras[]`, the semantics are
  deterministic: without `qty` every matching line is removed; with `qty`
  the most recently added matching line is reduced, and removed entirely if
  `qty` covers it. The full snapshot in the result lets the model repair
  anything else by remove + re-add.
- `lookup_customer` matches the first name case-insensitively against the
  pizzeria's customer list and returns **exactly two booleans plus the
  snapshot**: whether a customer with that name exists, and whether that
  customer has a saved street. It **never** returns the street, a masked form
  of it, its length, or any other derivative. An empty name returns
  `invalid_arguments`.
- **A failing `lookup_customer` is not fatal.** If the customer list cannot be
  fetched, the tool returns `api_unavailable` and the conversation continues by
  asking for the street as usual. Address reuse is a convenience; losing it
  must never lose the order.
- `set_customer` accepts a dictated `street_one` **or** `use_saved_street:
  true`, and **never both**: passing both returns `invalid_arguments` with a
  spoken sentence. With the flag set and no saved street behind that name, it
  returns `no_saved_street` and asks for the street. With the flag set and a
  saved street present, **the code copies the street into the order** and
  simultaneously adopts the **canonical first-name casing from the stored
  record** — so `marko` reuses Marko's address under the name `Marko` and does
  not create a near-duplicate ghost customer.
- `read_back` refuses on an empty basket and refuses while no customer is set,
  each with a sentence that says what is still missing.
- `check_street` is a plausibility signal only. Its result may never be
  presented as a deliverability guarantee.

---

## The saved-address privacy contract

A returning customer's street is the one piece of data in this product that the
customer did **not** dictate in this conversation. It is therefore governed by
its own rule, and that rule outranks convenience everywhere.

**The threat.** Customers are keyed by first name alone. There is no password,
no PIN, no second factor. Anyone who claims a common first name would otherwise
be able to make the agent read a stranger's home address out loud. **The first
name is a lookup key, never an authentication.**

**Two serializations, one redaction rule.** The customer record inside the
order has exactly two representations, and the difference between them is the
whole contract:

| View | Who sees it | Saved street |
|---|---|---|
| **Redacted view** | every tool result, every streamed event, every model-visible message, the web UI, the transcripts, the structured logs | `street_one: null` plus `street_on_file: true` |
| **Submit view** | the outbound `POST /pizzerias/{id}/orders` body, and nothing else | the real street text |

- The redacted view is the **only** view that feeds the snapshot, and the
  snapshot is embedded in every successful tool result — so the redaction is
  structural, not a filter someone has to remember to apply.
- The submit view is built **only** when the order write is assembled. There is
  no other caller, and no code path may add one.
- **The outbound submit payload is the only legal occurrence of the saved
  street text anywhere in a run.** Not in a snapshot, not in an emitted event,
  not in a log line, not in the model's message history, not on the page.
- Only `street_one` is ever reused. A stored second address line is never read,
  never copied, never sent, because the verified write contract does not
  accept it.
- **A street the customer dictated in this conversation is not covered by this
  rule.** It is their own input, arriving in their own turn; it is echoed,
  read back and stored exactly as given. The redaction exists for data the
  code fetched on the customer's behalf, not for data the customer just said.
- **The agent never recites a saved address, in any form** — not in the
  confirmation question, not in the read-back, not in the closing summary, not
  as a partial hint ("your address on Meyer street, correct?").
- Where the interface must show that an address exists, it shows a **localized
  label** — "gespeicherte Adresse" in German, "saved address" in English —
  and never the text.
- The redaction is a **testable claim, not a promise**: a string-scanning
  end-to-end test drives a full saved-address order and asserts the street text
  appears in the captured submit payload and in nothing else. See *Testing*.

---

## Conversation policy

This is what the system prompt must produce. Write the prompt to achieve it;
do not paste this section into it verbatim.

- Greet first, in the session language, and offer help — one sentence, not a
  menu recital.

**Language authority — one rule.** The session language starts as
`PIZZERIA_LANG` (greeting, CLI, web UI chrome before any switch). The web
header switch changes the session language: UI chrome, the greeting of a
fresh conversation, and the language sent with every speech request in both
directions. For the agent's replies, per-turn mirroring wins: it answers in the
language of the customer's latest message, even when that differs from the
session language. The CLI has no switch and stays at `PIZZERIA_LANG`.

- **One question per turn.** Never stack "name, street and what would you
  like?"
- Never state a menu item or a price that did not come from `get_menu` in this
  session. Price questions are normal questions, and so is "what does my
  basket come to?" Prices and the basket total are quoted verbatim from tool
  results; the agent never computes an amount.
- Collect the first name; **then** call `lookup_customer`. If a saved street
  exists, ask **exactly one** confirmation question — "Soll ich wieder an Ihre
  gespeicherte Adresse liefern?" / "Shall I deliver to your saved address
  again?" — **without reciting the address**. On an explicit yes, call
  `set_customer` with `use_saved_street: true`. If the customer declines, is
  unknown, or the lookup failed, ask for the street as usual. If the customer
  declines the street entirely, accept it — it is optional in the API.
- **Confirm the first name.** Repeat it back once. A misheard name silently
  creates a ghost customer nobody will find again. **In spoken conversations
  the name must always be confirmed before the order is submitted, and the
  saved-address question never substitutes for that confirmation** — they are
  two different questions answering two different risks.
- Before submitting: call `read_back`, present it, and wait for an explicit
  yes. "Mhm" and silence are not a yes; ask once more, then offer to start
  over.
- Never announce that an order was placed before `submit_order` returned an
  `order_id`.
- On success, state the order id in groups a human can repeat back, and the
  wait time in **minutes**, converted from `eta_seconds`.
- On error, explain in plain language what happened and what the options are.
  Never show a status code, stack trace or JSON.
- Never claim to have checked an address for deliverability.
- When a reply will be spoken aloud: at most three dishes plus an invitation to
  ask for more, times in minutes, order ids in groups, short sentences.
- When a tool reports an error, follow it: offer the named alternatives or ask
  the missing question. The system is always right.

The prompt exists in one file per language, rendered with the pizzeria name at
session creation. Switching the language re-renders the same policy in the
other language in place; the conversation history is preserved.

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
  route while speech is unavailable.
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
  whether the speech path exists at all.
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
every stream is `done` — including streams that failed. `done` is a transport
event only: it is emitted to the stream and is **never** written to the session's
log file. The log carries the events a turn explicitly logs — the `user`,
`tool_call`, `tool_result`, `state`, `assistant` and `error` records the stream
also shows — and additionally a `language` event for a switch, which the stream
never carries. Neither side is a superset of the other: they overlap on the
explicitly logged turn events, the stream alone carries `done`, and the log alone
carries `language`. The log never carries a configuration value or a saved
address.

Turns are **serialized per session** by a lock the transport holds for the
whole stream. A second turn arriving while one is running is refused with
`409`, not queued and not run concurrently.

The `/confirm` route is the **only** path into `CONFIRMED` from the UI. It
dispatches `confirm_order` and, only if that succeeded, `submit_order` — both
recorded in the conversation exactly like model-issued calls, with synthetic
assistant tool-call messages and tool results — and then runs one **normal**
model turn to phrase the outcome. Same gateway path, same retry, same apology
behaviour as any other turn. Success and failure travel the same road.

The two speech routes are proxies and nothing more: they forward the session's
language to the speech service and hand the result back. They hold no order
logic, and while the speech path is unavailable they do not exist as far as the
page is concerned.

### The conversation

Type or paste a message, get an answer. The exchange a first-time customer
should be able to have, end to end, without help:

> *What have you got?* → *What does a Margherita cost?* → *I'll take two of
> those and a pasta* → *I'm a new customer, my name is …* → read-back →
> confirm → order id and wait time.

The same exchange must be possible spoken, using the microphone control and
read-aloud, with no typed input except where the customer chooses to type.
After a completed order, a new conversation can start immediately from the
same page.

### Header

- **The pizzeria being ordered from, by name**, prominent and always visible.
- **A selector to change pizzeria, filled from the API and from nowhere
  else.** No hardcoded names, no bundled list, no fallback entry when the call fails — if it
  fails, the page says the list is unavailable instead of offering a choice
  it cannot honour. Each entry shows the name plus a short form of its UUID
  so similar names can be told apart. Changing the selection starts a fresh
  conversation for that pizzeria.
- **A link to that pizzeria's dashboard**
  (`{PIZZASIM_URL}/dashboard/pizzerias/{id}`), opening in a new tab. Without
  it nobody can check whether the order arrived — and checking that is the
  entire point of the product.
- **Language: German or English**, switchable, applied to the agent's replies
  and to speech in both directions.
- **A read-aloud toggle, rendered as a speaker icon**, and it lives **in the
  header, between the language switch and Start over** — read-aloud is a
  session preference like the language, not a per-message action, so it
  belongs with the other session controls and not in the composer. Its
  required behaviour:
  - It is a real button, reachable by keyboard, and **operable with both
    Space and Enter**.
  - It carries `aria-pressed`, which is `false` on load: **read-aloud is off
    by default** and every page load starts silent.
  - Its `title` and `aria-label` carry the same localized sentence ("Antworten
    vorlesen" / "Read replies aloud"), which follows the language switch
    immediately. **Changing the language must never change the pressed
    state** — localization and state are independent.
  - Its icon reflects the state (speaker on / speaker muted).
  - It is **rendered only when voice is usable** (see *Speech*); otherwise it
    is not on the page at all.
- **Start over**, clearing the session and the basket.

### Footer

- **The running version**, `x.y.z`, from `APP_VERSION`. Without it nobody can
  tell which build is answering.
- **The full pizzeria UUID**, selectable, for pasting into API calls.
- **Connection state** for the ordering API and the model gateway, refreshed
  periodically. The gateway badge reports the process-wide outcome of real
  gateway calls; the health check itself never calls the gateway just to
  colour a badge.
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
- If the stream ends without a final assistant message, the UI says so and
  offers to resend.
- **The client timeout covers the streamed body, not only the response
  headers.** A stream that stalls halfway must actually time out, so the
  timeout notice and its resend control can occur at all.
- If the request errors, times out, or the connection drops, the UI says which
  happened and offers to resend.
- A `409` (turn already running) is shown as a short, plain "one moment"
  notice — it is not an error and offers no resend.
- Errors in the customer's language, in plain words. No status codes, no
  tracebacks, no raw JSON.
- **Nothing in the text UI may depend on a browser API that exists only in a
  secure context.** Typed ordering must work fully over plain HTTP, and it must
  keep working when the voice controls are absent or have been withdrawn.

### The order on screen

- The current basket is visible, with quantities and what it comes to. The
  code owns the order; the customer must see what the code holds.
- The read-back is visually distinct and carries an explicit confirm control.
  Confirmation is an action the customer takes, not a word the agent claims to
  have heard. Older read-back panels are disabled as soon as a new one appears.
- A customer whose street came from saved data is shown with the localized
  "saved address" label and never with the address text.
- On success: the order id, readable, and the wait in minutes.
- After submission the basket is locked and shown as submitted. Nothing on the
  page can modify or resubmit it.

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
  the server. It never computes a total, never decides a state, never keeps
  its own copy of the basket, and never holds a customer's saved address.

---

## Speech

Voice is an input and an output method on the web channel, served by a
**self-hosted speech service**: CPU-only, in its own container, reached over
HTTP with an OpenAI-compatible surface.

| Direction | Endpoint | Payload |
|---|---|---|
| STT | `POST {SPEECH_URL}/v1/audio/transcriptions` | multipart: the recorded audio file, the model id, the language → `{"text": …}` |
| TTS | `POST {SPEECH_URL}/v1/audio/speech` | JSON: model, voice, input text, language → audio bytes |
| Probe | `GET {SPEECH_URL}/v1/models` | any 2xx means alive |

- **The speech service is the only speech path.** No external speech provider,
  no hosted realtime framework, no audio through the LLM gateway — that
  gateway carries chat completions only.
- **The browser captures and plays audio; it does not recognise or synthesise
  it.** Capture via `getUserMedia` and `MediaRecorder`, playback via a plain
  audio element — cross-browser and cross-platform, on Linux, macOS and
  Windows alike.
- **The browser speech APIs are forbidden.** `SpeechRecognition` and
  `speechSynthesis` tie the product to a single browser vendor and send
  customer audio to a third party. The self-hosted service exists so that
  neither is ever needed.
- **Nothing about the speech stack is written into source.** Base URL, models
  and voice come from the environment, exactly like the chat model. The
  language sent with every STT and TTS request is the session language — there
  is no separate speech-language setting.
- **Enablement is all-or-nothing, and it is probed.** The speech path counts as
  available only when `SPEECH_URL`, both model ids and the voice id are all
  configured **and** the service answered the startup probe with a 2xx. Three
  of four variables set is off, not partly on. While it is off, both speech
  endpoints answer `404`; a speech request that fails once the service is up
  answers `502`.
- **Request/response, not streaming.** Record, upload, transcript back.
  Latency is visible and acceptable; do not build partial results, barge-in
  or turn detection on top — this transport cannot do them, and pretending
  otherwise produces a broken feel.
- **Push-to-talk.** The microphone control sits in the composer next to the
  text field. Recording starts and stops on the customer's action and never
  listens continuously; the recording state is visible at all times and is also
  exposed as `aria-pressed`. When the transcript comes back empty, the page
  says it did not catch that and the turn is not sent.
- **A spoken turn is marked as spoken**, and the marking is **ephemeral**: the
  spoken-style instruction is attached to that one request only and is never
  written into the conversation history. A later typed turn must not inherit
  the spoken constraints.
- **Synthesis is optional and off by default**, toggled by the customer in the
  header, and **applied only to the final assistant message of a turn** — never
  to intermediate steps, never to tool output, never once per streamed event.
  A turn containing several tool calls and one final message produces exactly
  one synthesis request.
- **Voice controls are rendered only in a secure browser context, and that
  check lives in the UI.** The page renders the microphone and the read-aloud
  toggle only when the speech path is available **and** the browser reports a
  secure context (HTTPS, or localhost during development), and the microphone
  only when the browser's capture APIs exist as well. Over plain HTTP the page must
  present **no** voice-capable UI at all, even when the server is fully
  configured for speech — a microphone button that cannot work is worse than no
  button. Documenting the HTTPS requirement is not a substitute for the check.
- **Runtime degradation.** If a speech request fails while the customer is
  using it, the page says so in plain language and **hides both voice controls
  for the rest of the session**, while typed ordering continues untouched. A
  speech outage must never block ordering.
- **Voice is a required product capability for release completeness.**
  Text-only is the degraded fallback when speech is unconfigured in
  development or temporarily unavailable at runtime: microphone and read-aloud
  toggle are then not rendered and the text UI is fully usable. A release
  without a working voice path is not done.
- **Transport formats:** the STT path accepts the browser-recorded audio format
  emitted by `MediaRecorder`; the TTS path returns audio playable by a standard
  browser audio element, and the response's own content type is what the page
  plays.
- **Latency:** each STT and each TTS request should complete quickly enough for
  turn-based conversation on modest hardware; sustained multi-second delays
  that make turn-taking awkward are a defect.
- **Speech shortens answers, it does not change them.** Same core, same tools,
  same state machine, same order.
- **Confirm the name.** Transcription errors on names are the expensive
  failure: a misheard name silently creates a customer nobody will find again.
  In spoken conversations the name is read back and confirmed before
  submission, always.

### Speech service provisioning

The deployment includes a self-hosted, CPU-only speech service reachable at
`SPEECH_URL`, exposing the OpenAI-compatible endpoints in the table above. The
application and the speech service are deployed together as first-party
artifacts, and the repository carries a **neutral deployment definition** for
the service next to the application's deployment artifacts.

Neutral means exactly this, and it is a hard rule:

- **No real image name, no real engine or model name, no real voice name, and
  no host name appears in a production-facing artifact — source, this
  specification, or any deployment file.** The image, the models and the voice
  are operator configuration supplied through the environment, exactly like the
  chat model. One exemption, and only this one: the offline test harness may use
  opaque local stub identifiers (`scripted-stub`, `stub-stt`, `stub-tts`,
  `stub-voice` and the like) that name no real vendor, engine, model or voice.
  They are fixtures that let tests run without a network; no production-facing
  artifact may read one, default to one, or ship one.
- The definition states the required **interface** — the two endpoints, the
  probe endpoint, an HTTP port, CPU-only resources with no accelerator
  reservation — and nothing about which implementation satisfies it.
- Nothing in the repository may recommend, default to, or hint at a particular
  engine.
- **A voice-capable deployment serves the application over HTTPS on a real host
  name.** Microphone capture does not exist on plain HTTP, so a plain-HTTP
  deployment is a text-only deployment by definition and can never be a valid
  voice acceptance environment.

---

## Error handling

Every case below needs a test and a phrasing.

| Situation | Code does | Customer sees/hears |
|---|---|---|
| Gateway timeout | one retry, then abort the turn | plain apology, offer to resend |
| Gateway unreachable or malformed reply | abort the turn, mark the gateway down | plain apology, rendered as a normal reply |
| Tool loop guard exceeded | abort the turn after a fixed number of tool rounds | plain apology |
| `401`/`403` from PizzaSim | abort, log, do not retry | "I can't reach the kitchen system right now" |
| `404` on the preselected `PIZZERIA_ID` | fail at startup, not mid-call | — (process refuses to start) |
| Runtime pizzeria selection invalid/gone | session error, refresh the selector; process stays up | "that pizzeria isn't available right now" |
| `422` validation | surface the offending field, keep the basket | targeted question about the offending item |
| `5xx` on submit | **no blind retry** | "I'm not sure that went through — let me check" |
| Timeout on submit | mark unknown; shortlist via `GET /pizzerias/{id}/orders`, verify items via the detail endpoint before any retry | as above |
| Unknown item code | `unknown_item` + up to three candidates | "I have Margherita or Marinara — which one?" |
| Unknown extra topping | `invalid_extra` + candidates, whole call rejected | "I can't add that topping — did you mean …?" |
| Empty basket at submit | reject the transition | "What can I get you?" |
| Menu fetch fails at start | fail fast | "We're not taking orders right now" |
| Pizzeria list fetch fails | no selector, say so | list unavailable — no fallback entry |
| Customer lookup fails | non-fatal tool error, continue | ask for the street as usual |
| `set_customer` with both street and saved-street flag | `invalid_arguments`, no state change | "Either a street or the saved address — not both" |
| Saved-street flag with no saved street | `no_saved_street`, no state change | "I don't have a saved address under that name — what's the street?" |
| Speech unconfigured | speech endpoints answer `404`; controls not rendered | text UI unaffected |
| Speech service down at startup | speech stays off; a line on standard error | text UI unaffected |
| Speech request fails at runtime | `502`; the page hides both voice controls for the session | "Read-aloud isn't possible right now" / "please type" |
| Empty transcript | no turn is sent | "I didn't catch that — please try again" |
| Microphone permission refused | no turn is sent | "No microphone access" |

The submit-timeout case is the one that matters: a blind retry doubles a real
order. Recovery, in this exact order: shortlist candidates on the pizzeria's
order list by first name and by creation time no older than the submit attempt
minus a **60-second clock-skew allowance**; take the most recent candidate;
fetch its detail; compare its items and quantities against the basket; adopt it
**only** on an exact match — and otherwise allow exactly **one** real retry. If
the list or the detail lookup fails, tell the customer honestly and retry
nothing.

---

## Anti-patterns — explicitly forbidden

None of these is a matter of taste.

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
6. **A frontend that discards stream events.** A UI that renders only the final
   message and throws the tool events away leaves the customer watching a
   frozen screen while the agent works normally. Rendering the intermediate
   steps is part of the product, not a debug view.
7. **Reciting a saved address in any form** — in the confirmation question, in
   the read-back, in a summary, in a log line, in a streamed event, as a hint
   or as a partial match. The first name is a lookup key and not a credential;
   whoever claims a name must never be able to extract the address behind it.
8. **A voice control rendered outside a secure context.** A microphone button
   on plain HTTP promises a capability the browser will refuse, and it teaches
   the customer that the product is broken. The check belongs in the UI, not
   only in a deployment note.

---

## Testing

- **Unit:** the state machine, exhaustively. Every illegal transition has a
  test asserting it is refused.
- **Tool level:** against recorded API fixtures. No network, no LLM, fast.
  Includes cent-exact totals, the atomic add, deterministic removal, and the
  `(type, code)` collision.
- **Golden transcripts:** **ten** scripted conversations against a stub model
  replaying fixed tool calls, each asserting the final state, the calls
  actually made, the error codes raised, and the resulting basket:
  1. happy path,
  2. correction ("make that three"),
  3. unknown item with candidates,
  4. customer changes their mind after the read-back (stale revision, second
     read-back, then confirm),
  5. submit timeout with recovery,
  6. saved-address reuse,
  7. saved-address decline falling back to a dictated street,
  8. a spoken order using the saved street, name confirmed first,
  9. a spoken order with a dictated street, name confirmed first,
  10. a spoken order whose name was misheard and corrected before it was
      stored.
  The three spoken cases assert that the name-confirmation sentence occurs
  **before** the `set_customer` call, and the misheard case also
  asserts that `set_customer` ran **exactly once** — a corrected name must not
  leave a ghost customer behind. The saved-address cases assert that the street
  text never entered the model's message history.
- **Address reuse, tool level:** `lookup_customer` known / unknown / saved
  street missing / customer list unavailable (non-fatal), and
  `set_customer(use_saved_street: true)` copying in code, adopting canonical
  casing, refusing both arguments at once, and refusing when no saved street
  exists.
- **The redaction sweep is a string scan, and it is the oracle for the privacy
  contract.** One test drives a complete saved-address order through the real
  agent loop — lookup, reuse, add, read back, confirm, submit — capturing the
  outbound submit payload. It then asserts the street text appears in that
  payload and searches for it in every other artifact the run produced: the
  emitted events, the model's message history, and the session's log file. **A
  hit anywhere but the submit payload fails the test.** A redaction that is
  merely stated and not scanned for does not count as implemented.
- **Browser end-to-end, not optional.** Tests drive the real page in a headless
  browser — type a message, wait for a rendered reply, walk a full order to
  submission — asserting against the DOM, not the API. `curl` proves the server
  works and proves nothing about the product; the customer never talks to
  `curl`. Cover the header and footer contract, the pizzeria switch, the
  language switch, and four failure paths: a tool error, a stream ending
  without a final message, the gateway unreachable, and a lost session — each
  must leave a visible message on the page.
- **Offline voice end-to-end with a fake microphone is mandatory and cannot be
  substituted.** A headless browser configured with a fake media stream drives
  the genuine push-to-talk path against a stub speech service. An API-level
  test of the speech proxies is a supplement, never a replacement: the wiring
  that breaks is in the page. These tests assert wiring — control visibility,
  the STT round trip, the spoken-turn marking reaching the model, read-aloud
  behaviour, header placement and labelling, keyboard operation, runtime
  degradation, secure-context gating — and never transcription or synthesis
  quality. Specifically:
  - the microphone and the toggle are visible when speech is configured and the
    context is secure, and the toggle starts at `aria-pressed="false"`;
  - a recorded fixture pushed through push-to-talk drives a real turn and fills
    the basket, and the spoken-style marking reached the model;
  - **the stub's synthesis call counter is the oracle for read-aloud, not the
    button's own state**: with the toggle on, a turn containing a tool step and
    a final message produces exactly **one** synthesis call — and the **off
    path is asserted too**: after toggling back off, a further turn produces
    **no** additional call;
  - the toggle sits inside the header with the language switch as its previous
    sibling and Start over as its next sibling;
  - its `title` and `aria-label` follow the language switch, and its pressed
    state does not;
  - it is operable with Space and with Enter;
  - a speech outage mid-session hides both controls and leaves typed ordering
    working;
  - with the browser reporting an insecure context, **neither control is
    rendered** while typed ordering still works.
- **API-level speech tests** supplement the browser tests: availability
  reported in the UI bootstrap, the STT round trip using the session language,
  synthesis returning playable audio, a failing service mapping to `502`, and
  an unknown session mapping to `404`.
- **The acceptance test is live**, opt-in via an environment flag, and it is
  one of only two tests that touch the real API. Full conversation, submit,
  then read the pizzeria's orders back — presence via
  `GET /pizzerias/{id}/orders`, customer, items and quantities via the detail
  endpoint (the list endpoint carries no items and cannot verify them) — and
  assert points 1–4 under *What done looks like*. If this fails, the product
  does not work, whatever else is green.
- **The live voice acceptance test is the release-gating voice proof**, opt-in
  via its own environment flag plus the URL of a deployment served over HTTPS.
  It launches a real browser with a fake audio device streaming a recorded
  spoken order, clicks the real microphone control, and lets **real speech
  recognition** produce the transcript that drives the order; it enables
  read-aloud and asserts the synthesis response carried **non-empty audio**;
  then it confirms through the page's confirm control and verifies the
  resulting order through the API — order present under the tenant, right
  customer, items present. At least one German and one English recorded
  fixture. **A text replay is not a substitute and must fail this test**: if
  recognition does not produce an order-driving transcript, the test fails
  rather than falling back to typing. When the flags are absent the test skips
  cleanly, and it is never silently satisfied by the offline stub. A manual
  demo is a release-note aid, not the acceptance artifact.
- **Manual checklist (supplementary, never a substitute):** dictate an order,
  dictate a name that needs correcting, ask a menu question aloud — plus one
  run with the speech variables unset, which must render a usable text-only UI
  and place an order normally.

Recorded audio fixtures live with the tests and serve both the offline voice
end-to-end tests and the live voice acceptance test.

---

## Who builds this — and who judges it

The build runs locally, on the operator's own subscriptions, with the most
capable models available. Two roles take part and they are **not**
interchangeable.

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
  rubric so quality is measurable across rounds instead of a vibe.
- **The reviewer is a different agent from the implementer.** Independence is
  the point; a model reviewing its own output is not a review.

### Two model domains, never mixed

- **Build-time models** power the harnesses. Configured outside this
  repository, none of this spec's business. Nothing in the deliverables
  reads, references, or depends on them.
- **Runtime models** are what the ordering agent calls while serving a
  customer: `LITELLM_PIZZA_MODEL_1` and `_2` from the environment.

Binding consequences:

- The implementer never wires the agent to whatever model the implementer
  itself runs on, and never copies a build-time model name into source,
  config, prompts, tests or docs.
- No real vendor, engine or model name is hardcoded in a production-facing
  artifact — not in source, not in the deployment definition, not in this
  document. A missing runtime value is a startup failure, not a default.
- The same rule covers speech: no real engine, image, model or voice name
  reaches source, the deployment definition or this document.
- Exempt from both, and nothing else is: opaque local stub identifiers used by
  the offline test harness (`scripted-stub`, `stub-stt`, `stub-tts`,
  `stub-voice` and the like). They name no real vendor, engine, model or voice,
  they exist only so tests run without a network, and no production-facing
  artifact may read one or default to one.
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
  win**.
- Maximum 3 rounds per stage. Still not approved after round 3 → stop, show
  the scores and the open issues. A valid outcome, not a failure.
- Disagreeing is allowed — one-line rebuttal in the next request. Never
  ignore a finding silently.
- Every reviewer stdout goes into `reviews/`, every round's scores into
  `reviews/scores.md`, and `reviews/` is committed.

### Two stages, in this order

1. **PLAN.** Write `PLAN.md`: file layout, tool schemas, state machine, agent
   loop, error handling, conversation state, the privacy contract, the speech
   wiring. **No code.** Iterate with the reviewer until `APPROVED`. Implement
   nothing before that.
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

0. **Contracts.** Verify the API facts above against the live API before the
   components that depend on them are implemented. The open list only shrinks —
   a verified fact never becomes a question again.
1. **Core.** Order model, state machine, tool layer, tests. No LLM, no
   network. Pass when the unit tests are green.
2. **Agent loop.** Model, tools, system prompt, one turn end to end.
3. **CLI.** Full conversation, real API, an order visible on the dashboard.
4. **Web.** FastAPI on 8888, same core. Pass only when you have opened the
   page in a browser, switched pizzeria, asked a price question, placed an
   order through the page, and seen it on that pizzeria's dashboard — not
   when the endpoint answers `curl`.
5. **Voice.** Wire the speech service into the web UI: push-to-talk, the header
   read-aloud toggle, the secure-context gate, the spoken-answer policy, and
   the degraded no-speech path. Pass only when the fake-microphone browser test
   is green **and** a spoken order has gone through a real HTTPS deployment.
6. **Privacy.** Saved-address lookup and reuse end to end, and the redaction
   scan. Pass only when the string sweep finds the saved street in the submit
   payload and nowhere else.
7. **Harden.** Walk the error table, force each case, fix what breaks.

After each pass, review your own work as the reviewer who has to reject it:
what would a hostile reader find first? Fix that, then move on. Stop only when
a full pass over the spec finds nothing left that you know how to improve.

---

## Deliverables

```
.
├── SPEC-RELEASE-1.1.0.md    ← this file
├── README.md                ← how to run each channel, and the voice setup
├── PLAN.md                  ← written before any code, updated as you go
├── requirements.txt         ← every dependency pinned to an exact version
├── Procfile                 ← the web channel's process definition
├── .env.example             ← names only, never values
├── core/
│   ├── order.py             ← Order, basket, revision, the two customer views
│   ├── state.py             ← state machine, transitions, invariants
│   ├── menu.py              ← menu snapshot, code validation, candidates
│   ├── pizzasim.py          ← API client, typed errors, timeouts, env loading
│   ├── tools.py             ← the nine tool schemas + dispatch
│   └── agent.py             ← model loop, prompt assembly, event log
├── channels/
│   ├── cli.py               ← terminal transport
│   ├── web.py               ← FastAPI, port 8888, NDJSON stream, speech proxies
│   ├── speech.py            ← speech service client, all-or-nothing enablement
│   └── static/              ← page, styles, and the UI script incl. voice
├── prompts/
│   ├── system.de.md
│   └── system.en.md
├── deploy/
│   └── speech service definition ← neutral, self-hosted, CPU-only
├── tests/
│   ├── fixtures/            ← recorded API responses
│   ├── fixtures/audio/      ← recorded spoken orders, DE and EN
│   ├── stubs.py             ← stub API, stub gateway, stub speech service
│   ├── test_state.py        ← the state machine, exhaustively
│   ├── test_tools.py        ← tools, redaction sweep, live acceptance
│   ├── test_transcripts.py  ← the ten golden conversations
│   ├── test_web_e2e.py      ← headless browser, DOM assertions
│   ├── test_web_speech.py   ← stub speech + fake mic, live voice acceptance
│   └── transcripts/         ← the ten scripted conversations
├── reviews/                 ← one file per review round, plus scores.md
└── logs/                    ← one JSONL file per session, written at runtime
```

Roles of the parts, so nothing is misplaced:

- `core/` owns the order and everything that may change it. It never imports a
  transport and never knows a channel exists.
- `channels/` carries words in and words out. No order logic, no validation, no
  arithmetic. The web channel forwards identifiers to core and streams core's
  events; the speech client is a transport detail of that channel.
- `prompts/` holds one file per language, rendered with the pizzeria name.
- `deploy/` holds the neutral speech-service definition — interface only.
- `tests/` holds the deterministic suite plus the two opt-in live tests.

---

## Decisions locked

| Area | Decision |
|---|---|
| Order ownership | Code. The model never holds the cart. |
| Submit | Single call, only from `CONFIRMED`, never auto-retried |
| Menu | Fetched live per session, no fallback list |
| Tenancy | Customer-selectable; `PIZZERIA_ID` preselects, never restricts; tenant in the URL path |
| Pizzeria selector | Filled from the API only; no fallback entry |
| Prices | Shown from the API; no payment, no invented figures |
| Totals | Computed in code in exact decimal cents; the model never does arithmetic |
| Saved addresses | Reusable after one explicit confirmation; the address text never reaches the model, the stream, the page, the transcript or the logs |
| Saved-address scope | `street_one` only; a second stored line is never reused |
| Address disclosure | Never, in any form. The first name is a lookup key, not a credential |
| Redaction proof | A string scan over every produced artifact; the submit payload is the only legal occurrence |
| Name confirmation | Mandatory in every spoken flow before submission; the saved-address question is not a substitute |
| Language | Session language from `PIZZERIA_LANG`, switchable in the web header; per-turn mirroring wins for replies; speech follows the session language |
| Transports | One core, two channels (CLI, web), no logic in the channels |
| Speech | Self-hosted container, OpenAI-compatible HTTP; no vendor, no browser speech API |
| Speech enablement | All-or-nothing, probed at startup; three of four variables is off |
| Voice | Required product capability on the web channel; text-only is degraded operation, not the product |
| Read-aloud | Off by default, header speaker toggle, final assistant message only |
| Voice context | Rendered only in a secure context, enforced in the UI; HTTPS for any voice-capable deployment |
| Voice failure | Runtime outage hides the voice controls and never blocks typed ordering |
| Web UI | Pizzeria name, basket and connection state always visible; no message ends unanswered |
| Version | `x.y.z` in the footer, validated at startup, raised every release |
| Derived URLs | Dashboard and docs built from `PIZZASIM_URL`, never literal |
| Languages | DE + EN, mirrored per turn |
| Confirmation | Mandatory read-back tied to a basket revision |
| Parsing | The model parses. No regex order parser, ever. |
| HTTP | A real client with timeouts. No `subprocess curl`. |
| Dependencies | Pinned to exact versions, no ranges |
| Persistence | None beyond the process and the PizzaSim API |
| Errors | Typed in code, plain language to the customer |
| Contract facts | Verified facts never return to the open list; the list only shrinks |
| Implementer | One agent only — nothing else writes code |
| Reviewer | A second, independent agent, read-only, judge and devil's advocate |
| Models | Never named, never hardcoded — environment configuration |
| Build tooling | Not specified here; the operator picks it |
| Proof | Verified through the browser and the live API, never only through `curl` — including one spoken order end to end |
| Definition of done | The judge approved, not "it runs" |

## Decisions deferred

- Extras and modifiers beyond a passthrough `extras[]`.
- Post-submit modification or cancellation.
- Reuse of a second stored address line, until the order write contract for it
  is verified.
- Multi-turn memory across sessions beyond saved-address reuse ("the usual").
- Additional languages beyond DE + EN.
- Streaming speech, barge-in and turn detection.
- Telephony as a third channel.

---

## Ticket sizing rules

- Each ticket is **one hour or less** of implementation.
- Prefer three narrow tickets over one broad one. Split by file, by component,
  or by "schema / implementation / tests".
- Every ticket carries acceptance criteria as a checklist.
- Tests belong to the ticket that introduces the behaviour, never to a
  follow-up. A privacy or voice guarantee ships in the same ticket as the test
  that proves it.

---

## Thirty-one rules that decide whether this works

Everything above is binding. These thirty-one are the ones that quietly decide
whether the order lands correctly, and each is the compressed form of a rule
stated in full in the section named after it.

1. **List versus detail.** The order list carries no items, so items and
   quantities must **only** ever be verified through the single-order detail
   endpoint — in timeout recovery and in the acceptance tests alike. *(The
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
14. **The secure-context gate lives in the UI.** Both voice controls are
    rendered **only** when the server reports the speech path available **and**
    the browser reports a secure context; the microphone is gated
    on the capture APIs as well. Over plain HTTP the page presents no voice-capable UI
    at all, and typed ordering is unaffected. *(Speech; Anti-patterns)*
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
    one of only two tests that touch the real API: presence via the order list,
    customer, items and quantities via the detail endpoint. If it fails the
    product does not work, whatever else is green. *(Testing)*
25. **Booleans only.** `lookup_customer` returns exactly two booleans and the
    snapshot — never the street, never a masked form of it, never its length.
    `set_customer` takes a dictated street **or** the saved-street flag and
    never both, and refuses the flag with `no_saved_street` when nothing is
    stored. *(Tools)*
26. **One legal occurrence.** The saved street text may appear **only** in the
    outbound submit payload — never in a snapshot, an event, a log line, the
    model's history or the page — and a string-scanning end-to-end test is
    what proves it. Only `street_one` is ever reused. *(The saved-address
    privacy contract; Testing)*
27. **Never recite a saved address.** Reuse is settled by exactly one
    confirmation question that does not name the address, and the interface
    shows a localized "saved address" label instead of the text. A street the
    customer dictated in this conversation is their own input and is exempt.
    *(The saved-address privacy contract; Conversation policy)*
28. **Name confirmation is its own question.** In every spoken flow the first
    name **must** be confirmed before submission, and the saved-address
    question never substitutes for it — a misheard name creates a ghost
    customer nobody will find again, and the code adopts the stored record's
    canonical casing to avoid a near-duplicate. *(Conversation policy; Tools)*
29. **Read-aloud discipline.** It is off on every page load, it applies **only**
    to the final assistant message of a turn, and the proof is the speech
    service's own call counter — including the off path, where toggling back
    off must produce no further synthesis call. *(Speech; Testing)*
30. **Speech is all-or-nothing, probed, and neutral.** All four speech
    variables plus a 2xx startup probe, or the path is off and both endpoints
    answer `404`; a runtime failure withdraws the controls without touching
    typed ordering; and no engine, image, model, voice or host name appears
    anywhere in the repository. *(Speech; Environment)*
31. **Voice is proved, not demonstrated.** A fake-microphone browser test is
    mandatory and cannot be replaced by API-level tests, and the release-gating
    live voice test drives a real browser over HTTPS with real recognition and
    non-empty synthesised audio — a text replay **must** fail it. *(Testing)*
