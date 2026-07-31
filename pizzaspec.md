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

- **Three transports over one core:**
  - `cli` — interactive terminal chat.
  - `web` — local FastAPI server on port 8888, browser chat UI.
  - `voice` — LiveKit agent, browser client, full duplex speech.
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
- Reading the whole menu aloud in the voice channel.
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
| `AGENT_MODEL` | Model the ordering agent calls; required, no default in code |

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
  creates a new customer — so a misheard name creates a ghost. The voice channel
  must therefore confirm the name explicitly.
- `street_one` is optional and is **not** validated for deliverability. Asking
  for it is a policy of this agent, not an API requirement — do not pretend to
  the customer that we checked something we did not.
- `POST` is **not idempotent**. A retry after a timeout can double the order.
  See **Error handling**.

### Open contract questions

The endpoints above are confirmed from the exercise material and from working
code. The following must be resolved against the API documentation
(`/swagger.html`) **before implementation starts**, and this section updated —
guessing any of them produces a demo that breaks on the second order.

1. **Order response field name.** The exercise text names `order_id`; existing
   working code checks for `id`. One of the two is wrong. The confirmation
   message and the log record both depend on it.
2. **Is there a list endpoint** for a pizzeria's orders
   (`GET /pizzerias/{id}/orders`)? The submit-timeout recovery path in
   *Error handling* requires it. Without it, a timed-out submit cannot be
   verified and the only honest option is to tell the customer.
3. **Menu item shape.** Which fields besides `code` — display name, per
   language? price? ingredients? The read-back text and the candidate
   suggestions on `unknown_item` are built from these.
4. **`extras[]`** — a controlled vocabulary or free text? If controlled,
   validate like item codes; if free text, do not pretend to validate.
5. **Error bodies** on `4xx` / `422` — is there a machine-readable field the
   tool layer can map to typed errors, or only a message?
6. **Status values** and their order in the lifecycle.
7. **`GET /location?street=`** — response shape and what a negative result
   actually means.

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
| `check_street` | `street` | plausibility result (optional, voice only) |

Tool result conventions:

- Success: the **full current state**, not a diff. The model should never have to
  reconstruct the basket from history.
- Failure: `{"error": {"code": "...", "message": "...", "candidates": [...]}}`.
  `message` is written to be spoken to the customer as-is if the model chooses to.
- `add_items` with an unknown code returns `unknown_item` plus up to three
  candidates from the menu. The model asks; it does not pick.
- Quantities are integers. A tool that receives `"zwei"` returns
  `invalid_quantity`; it does not parse German.

---

## Conversation policy

This is what the system prompt must produce. Write the prompt to achieve it;
do not paste this section into the prompt verbatim.

- Greet first, in the language of the pizzeria's country, and offer help — one
  sentence, not a menu recital.
- **One question per turn.** Never stack "name, street and what would you like?"
- Never state a menu item that did not come from `get_menu` in this session.
- Collect first name and street. If the customer declines the street, accept it
  and move on — it is optional in the API.
- Before submitting: call `read_back`, say it, and wait for an explicit yes.
  "Mhm" and silence are not a yes; ask again once, then offer to start over.
- Never announce that an order was placed before `submit_order` returned an
  `order_id`. No "I've sent that to the kitchen" while the call is in flight.
- On confirmation, state the order id in a form a human can repeat back, and the
  wait time in **minutes**, converted from `eta_seconds`.
- On error, explain in plain language what happened and what the customer's
  options are. Never show a status code, stack trace or JSON.
- Never claim to have checked an address for deliverability.

---

## The voice channel

Voice is not a wrapper around the text agent; it is the same core with a
different set of constraints on the words that come out.

- **Transport:** LiveKit agent plus browser client. `AGENT_NAME` must match on
  both sides and must be unique per running instance.
- **Audio path:** STT and TTS run over the LiveKit stack. The LLM gateway proxies
  chat completions only — do not attempt to route audio through it.
- **Barge-in is mandatory.** The customer interrupts; TTS stops within 300 ms and
  the partial utterance is discarded, not queued.
- **Never read a list.** Menu questions are answered with at most three items and
  an invitation ("…or tell me what you're in the mood for"). The full menu exists
  in the web channel; in voice it is a conversation, not a recitation.
- **Numbers as words.** "twenty-five minutes", not "25". Order ids are read in
  groups with a pause, and offered again on request.
- **Confirm the name by spelling** when STT confidence is low or the name is not
  already a customer of this pizzeria — a misheard name creates a new customer
  that nobody will ever find again.
- **Latency budget:** first audible response ≤ 1.2 s after end of speech. Any
  tool round trip longer than 800 ms is covered by a short filler utterance
  chosen from a small set, never the same one twice in a row. No dead air beyond
  2 s at any point.
- **Failure is audible.** If STT returns nothing twice in a row, the agent says
  so and offers the web channel — it does not sit silently.

---

## Error handling

Every case below needs a test and a phrasing.

| Situation | Code does | Customer hears |
|---|---|---|
| Gateway timeout | one retry, then abort turn | "I didn't catch that, one moment" then a plain apology |
| `401` / `403` from PizzaSim | abort, log, do not retry | "I can't reach the kitchen system right now" |
| `404` on the pizzeria path | fail at startup, not mid-call | — (process refuses to start) |
| `422` validation | surface field, keep basket | targeted question about the offending item |
| `5xx` on submit | **do not blind-retry** | "I'm not sure that went through — let me check" |
| Timeout on submit | mark `UNKNOWN`, verify before any retry | as above |
| Unknown item code | `unknown_item` + candidates | "I have Margherita or Marinara — which one?" |
| Empty basket at submit | reject transition | "What can I get you?" |
| Menu fetch fails at start | fail fast | "We're not taking orders right now" |

The submit-timeout case is the one that matters: a blind retry doubles a real
order. The recovery path is to verify against the order list for this pizzeria
before retrying, and if that is not possible, to tell the customer honestly.

---

## Anti-patterns — explicitly forbidden

Each of these was present in a previous implementation of this task. None is a
matter of taste.

1. **A regex "fast path" that places an order without the model.** It bypasses
   confirmation, mis-parses quantities, duplicates items on overlapping matches,
   and makes the whole tool-calling architecture decorative.
2. **Shelling out to `curl` via `subprocess`.** Use an HTTP client. No shell
   quoting bugs, no injection surface, real timeouts, testable.
3. **Hardcoded pizzeria UUID or hardcoded menu fallback.** Both send orders to
   the wrong place while looking like they work.
4. **A system prompt that forbids confirmation** ("never ask if they're sure,
   always call `place_order` immediately"). That is the bug, written down as a
   rule.
5. **Prompt shouting.** ALL-CAPS threats and "NEVER BREAK THIS RULE" are what
   people write instead of enforcing the rule in code. The state machine enforces
   it; the prompt can then be calm and short.

---

## Testing

- **Unit:** the state machine, exhaustively. Every illegal transition has a test
  asserting it is refused.
- **Tool level:** against recorded API fixtures. No network, no LLM, fast.
- **Golden transcripts:** five scripted conversations run against a stub model
  that replays fixed tool calls — happy path, correction, unknown item, customer
  changes mind after read-back, submit timeout. Assert final state and the calls
  actually made.
- **One live smoke test**, opt-in via env flag: places a real order and asserts
  an `order_id` came back. This is the only test that touches the real API.
- **Voice**, manual and scripted: barge-in mid-sentence, a name that needs
  spelling, and a menu question — each with an expected observable behaviour.

---

## Who builds this — and who judges it

This spec is implemented inside the PizzaSim training environment. Two harnesses
are installed there and their roles are **not** interchangeable.

| Role | Harness | Model | Permission |
|---|---|---|---|
| Implementer | Claude Code | set by the environment | writes every file |
| Reviewer / judge | Codex | set by the environment | read-only, never writes |

- **The model is deliberately not named in this spec.** Which weights sit behind
  each harness is environment configuration and differs between environments —
  a training simulator may proxy both harnesses onto third-party models, another
  environment may run them on their vendors' own. Read the model from
  configuration. Never hardcode it, never assume a default, and never write a
  model name into code, prompts, tests or documentation.
- **Harness is not model.** A harness does not necessarily run on the weights of
  the company that built it. Never ask an agent which model it is — a
  self-report is not evidence, the configuration is binding.
- **Both sides may run inexpensive models.** That is a constraint to design for,
  not an obstacle to work around: it is why review requests must be short,
  stateless and self-contained, and why the rubric is numeric.
- **Claude Code is the only thing that develops.** Every artefact in
  *Deliverables* is produced by it. No second implementer, no other model
  writing "just this one file", no hand-patched fixes smuggled in between rounds.
- **Codex never writes the code it judges.** It runs read-only and plays two
  roles in the same call: *devil's advocate* — attack the work, find gaps, wrong
  assumptions, missing error cases — and *judge*, scoring against the fixed
  rubric below so that quality is measurable across rounds instead of a vibe.

### Review protocol

Reviewer calls are **stateless** — nothing is remembered between rounds, so every
request must be short and self-contained. Commit before each review so the
reviewer always sees a committed tree.

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

- `APPROVED` requires `TOTAL >= 20` **and** no single dimension below 4. If the
  verdict line says approved but the scores miss that bar, **the numbers win**.
- Maximum 3 rounds per stage. Still not approved after round 3 → stop, show the
  scores and the open issues. That is a valid outcome, not a failure.
- Disagreeing with the reviewer is allowed — state a one-line rebuttal in the
  next request. Never ignore a finding silently.
- Every reviewer stdout goes into `reviews/`, every round's scores get appended
  to `reviews/scores.md`, and `reviews/` is committed. The review trail belongs
  in the repo.

### Two stages, in this order

1. **PLAN.** Write `PLAN.md`: file layout, tool schemas, state machine, agent
   loop, error handling, conversation state. **No code.** Send it to the reviewer
   and iterate until the verdict is `APPROVED`. Implement nothing before that.
2. **IMPLEMENT.** Only after the plan is approved. Build exactly the approved
   plan, then send the diff for review and iterate until approved.

"Done" means the judge approved — not that the code runs. Working code that
fails the rubric is not done.

---

## How to work

This is an autonomous build. There will be no clarifying questions answered and
no feedback until you are done — every decision inside these constraints is
yours. Work in passes and verify after each; do not write the whole thing and
then run it once.

1. **Core.** Order model, state machine, tool layer, tests. No LLM, no network.
   Pass when the unit tests are green.
2. **Agent loop.** Model, tools, system prompt, one turn end to end.
3. **CLI.** Full conversation, real API, an order visible in the dashboard.
4. **Web.** FastAPI on 8888, same core, streamed intermediate steps visible.
5. **Voice.** LiveKit agent and client, voice-specific policy, latency budget.
6. **Harden.** Walk the error table, force each case, fix what breaks.

After each pass, review your own work as if you were the reviewer who has to
reject it: what would a hostile reader find first? Fix that, then move on. Stop
only when a full pass over the spec finds nothing left that you know how to
improve.

---

## Deliverables

```
.
├── SPEC.md                  ← this file
├── README.md                ← how to run each of the three channels
├── PLAN.md                  ← written before any code, updated as you go
├── core/
│   ├── order.py             ← Order, basket, revision
│   ├── state.py             ← state machine, transitions, invariants
│   ├── menu.py              ← menu fetch, code validation, candidates
│   ├── pizzasim.py          ← API client, typed errors, timeouts
│   ├── tools.py             ← tool schemas + dispatch
│   └── agent.py             ← model loop, prompt assembly
├── channels/
│   ├── cli.py
│   ├── web.py               ← FastAPI, port 8888
│   └── voice/               ← LiveKit agent + client config
├── prompts/
│   ├── system.de.md
│   └── system.en.md
├── tests/
│   ├── fixtures/            ← recorded API responses
│   ├── test_state.py
│   ├── test_tools.py
│   └── transcripts/         ← the five golden conversations
├── reviews/                 ← one file per review round, plus scores.md
└── .env.example             ← names only, never values
```

---

## Decisions locked

| Area | Decision |
|---|---|
| Order ownership | Code. The model never holds the cart. |
| Submit | Single call, only from `CONFIRMED`, never auto-retried |
| Menu | Fetched live per session, no fallback list |
| Tenant | One `PIZZERIA_ID` per process, from env, never hardcoded |
| Transports | One core, three channels, no logic in the channels |
| Languages | DE + EN, mirrored per turn |
| Confirmation | Mandatory read-back tied to a basket revision |
| Parsing | The model parses. No regex order parser, ever. |
| HTTP | A real client with timeouts. No `subprocess curl`. |
| Persistence | None beyond the process and the PizzaSim API |
| Errors | Typed in code, plain language to the customer |
| Implementer | Claude Code only — nothing else writes code |
| Reviewer | Codex, read-only, devil's advocate and judge in one |
| Models | Never named, never hardcoded — environment configuration |
| Definition of done | The judge approved, not "it runs" |

## Decisions deferred

- Extras and modifiers beyond a passthrough `extras[]`.
- Pricing, totals, and anything financial.
- Post-submit modification or cancellation.
- Multi-turn memory across sessions ("the usual").
- Additional languages beyond DE + EN.
- Telephony (SIP) as a fourth channel.

---

## Ticket sizing rules

- Each ticket is **one hour or less** of implementation.
- Prefer three narrow tickets over one broad one. Split by file, by component,
  or by "schema / implementation / tests".
- Every ticket carries acceptance criteria as a checklist.
- Tests belong to the ticket that introduces the behaviour, never to a follow-up.
