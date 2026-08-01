OpenAI Codex v0.143.0
--------
workdir: /home/rob/bpm-pizza-vibecoding-solution
model: gpt-5.4
provider: openai
approval: never
sandbox: read-only
reasoning effort: medium
reasoning summaries: none
session id: 019fbc41-341a-7b53-9afb-4298787af2b0
--------
user
You are the independent reviewer (devil's advocate). Read-only, no writes. Task: judge whether the NEW spec is optimal, what is missing, and what got worse ("verschlimmbessert") versus its two predecessors. Then grill the implementer's own analysis: attack it, find what it missed, correct what is wrong.

Files to read in the current working directory:
- SPEC.md — version 3, just delivered by the operator (uncommitted working-tree version; read the file, not git).
- Git HEAD SPEC.md — version 2 (run: git show HEAD:SPEC.md).
- SPEC_20260801.md — version 1.
- Context you may trust: the repo implements v1 fully (approved, see reviews/scores.md); contract facts in v2's committed SPEC were verified against the live API, including: menu items carry {code,name,base[],price}; extras[] is the controlled toppings[] vocabulary with server 422 on unknowns; error bodies are {"error","details[]"}; statuses ordered->prepared_planned->delivered; /location returns {street,deliverable} and returned deliverable:true even for nonsense; there IS a detail endpoint GET /pizzerias/{id}/orders/{order_id} returning customer+items[] while the LIST endpoint carries NO items; codes unique per type (tonno pizza+pasta); dashboard at {PIZZASIM_URL}/dashboard/pizzerias/{id}; docs at {PIZZASIM_URL}/swagger.html.

THE IMPLEMENTER'S ANALYSIS TO GRILL (attack, extend, correct):

Regressions in v3:
R1. Five already-verified contract facts were demoted back into "Open contract questions" (menu shape incl. price, extras vocabulary, error bodies, status values, /location) — directly violating v3's own new shrink-only rule ("a verified fact never moves back into the open list").
R2. The order-detail endpoint fact was deleted entirely. Consequence: v3's submit-timeout recovery says "verify via GET /pizzerias/{id}/orders", but that list endpoint carries no items — so neither the recovery's item verification nor acceptance criterion #4 (exact items/quantities read back from the API) is satisfiable as written.
R3. The greeting changed to "in the customer's UI language", but the initial UI language before any switch is undefined, and the CLI has no UI language at all — with "nothing is hardcoded" this is unresolvable without an env var (v1/v2 builds used PIZZERIA_LANG per an oracle decision; a prior grill condition required documenting it in the spec; v3 omits it).
R4. Basket-total ownership is unspecified: the spec demands the customer "sees what the basket comes to" and allows "what does my basket come to?" questions, but the fixed tools table gives no total anywhere (read_back returns basket/customer/revision only), inviting the implementer to let the LLM do arithmetic — which "no invented figures" should forbid.

Ambiguities carried or new:
A1. Language precedence unresolved: "answers in the language the customer used, per turn" vs header switch "applied to the agent's replies" — which wins when they conflict?
A2. CLI tenancy: scope says the customer chooses and can change the pizzeria; the web header has the selector; whether the CLI must also support switching is unstated.
A3. remove_item semantics when several lines share (type,code) with different extras remain unspecified (params are fixed).

Improvements in v3 (to keep):
I1. Shrink-only contracts principle + new pass 0 "Contracts".
I2. Anti-pattern #6 (frontend discarding stream events) and invariant 6 (basket never crosses tenant).
I3. SPEECH_* optionality now explicit in the env rules; speech browser capture (getUserMedia/MediaRecorder) sanctioned cross-browser; channels/speech.py and tests/test_web_e2e.py named in deliverables.
I4. Acceptance criterion reworded to "the pizzeria they chose" — consistent with customer-selectable tenancy.
I5. Derived URLs (dashboard, swagger) kept verified and explicitly never-literal.

Overall the implementer's verdict-to-be-attacked: v3 is structurally the best of the three but NOT optimal; it needs a small patch list (restore the five facts + detail endpoint per shrink-only rule; define initial/default language incl. CLI, e.g. a documented env var; state that read_back carries a code-computed basket total; one line on language precedence; one line on CLI tenancy) — after which building against it is safe.

Your output:
1. Attack: what is wrong or overstated in R1-R4/A1-A3/I1-I5? What did the implementer miss (check yourself: env table completeness, error table, testing section, deliverables tree vs existing repo, decisions-locked table consistency, anything contradicting the approved v1 core)?
2. Answer the operator's three questions explicitly: (a) Is v3 the optimal spec? (b) What is missing? (c) What got worse vs v1/v2?
3. End with:
VERDICT ON SPEC v3: BUILD-READY AS IS | NEEDS PATCHES | PREFER v2
PATCH LIST: numbered, max 10, each one line, empty if build-ready

codex
I’m reviewing the three spec versions and the implementer’s critique as a hostile reviewer. First I’ll load the mandatory skill instructions, then read the specs and compare them against the claimed regressions, ambiguities, and improvements.
exec
/bin/bash -lc "sed -n '1,260p' /home/rob/bpm-pizza-vibecoding-solution/SPEC.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc 'rg -n "PIZZERIA_LANG|language|read_back|remove_item|error|details|location|deliverable|prepared_planned|delivered|extras|toppings|dashboard|swagger|Contracts|Decisions locked|deliverables|tests|SPEECH_" /home/rob/bpm-pizza-vibecoding-solution -S' in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc 'git show HEAD:SPEC.md' in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' /home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,220p' /home/rob/.agents/skills/using-superpowers/SKILL.md" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 228ms:
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

 succeeded in 260ms:
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

### Open contract questions — shrink-only

Resolve against the live API before the affected component is implemented,
then move the answer up into the facts and delete the question. Never guess.

1. **Menu item shape** beyond `code` — display names per language, price
   field, ingredients. Read-back text, price answers and `unknown_item`
   candidates are built from these.
2. **`extras[]`** — controlled vocabulary or free text? If controlled,
   validate like item codes; if free text, do not pretend to validate.
3. **Error bodies** on `4xx`/`422` — a machine-readable field the tool layer
   can map to typed errors, or only a message?
4. **Status values** and their order in the lifecycle.
5. **`GET /location` response shape** and what a negative result means.

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

 succeeded in 254ms:
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

## What done looks like

There is exactly one success condition, and everything else in this document
exists to serve it:

**A customer talks to the agent, and the resulting order appears in the API
under the configured pizzeria — with the right customer, the right items, the
right quantities.**

Concretely, and this is the acceptance criterion:

1. `POST /pizzerias/{PIZZERIA_ID}/orders` returned an order id.
2. Reading that pizzeria's orders back shows the order, and it is visible on the
   dashboard for that pizzeria.
3. The customer name is the one the customer gave.
4. The items and quantities are the ones that were read back and confirmed —
   not a superset, not a subset, not a near match on the item code.

Nothing else counts as done. A green test suite, a clean architecture, a
pleasant interface: none of it is the product. The order on the board is the
product.

**Four failures that look like success**, each of which is a failed run and not
a partial one:

- The order landed under a **different pizzeria** than the configured one.
- A retry after a timeout created the order **twice**.
- A misheard or mistyped name created a **new customer** instead of matching the
  intended one.
- The order was submitted **without the customer confirming** the read-back.

Every rule in this spec — the state machine, the revision-bound confirmation,
the ban on blind retries, the name read-back, the tenant coming from the URL
path — exists to prevent exactly one of those four.

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
- **Menu, prices, cart, customer, submit.** The full happy path plus correction
  ("no, make that three"), removal, and abandonment. The customer can ask what
  is on offer and what individual items cost, and can see what the basket comes
  to before confirming.
- **Several pizzerias.** The customer chooses which one they are ordering from,
  and can change it. `PIZZERIA_ID` is the preselection, not a restriction.
- **The success moment:** the order appears in the PizzaSim dashboard under the
  configured pizzeria, with the right customer, items and quantities.
- **Deterministic tests** that run with no network and no LLM.
- **Structured logging** of every turn: user text, model tool calls, tool
  results, state transitions. One line per event, JSON, to a file.

### Out (explicitly)

- Payment and anything financial beyond showing prices the API supplies.
- Delivery routing, or an ETA of our own invention.
- Accounts, auth, sessions surviving a process restart.
- Modifying or cancelling an order after it was submitted.
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
| `PIZZERIA_ID` | UUID of the pizzeria preselected on first load |
| `APP_VERSION` | Release version, `x.y.z`, shown in the footer |
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

### Contract facts — verified against the live API (2026-07-31/08-01)

All former open questions were resolved by probing the live API
(`GET /menu`, `GET /pizzerias`, `POST /pizzerias/{id}/orders` — valid and
invalid bodies —, `GET /pizzerias/{id}/orders`,
`GET /pizzerias/{id}/orders/{order_id}`, `GET /location`, plus the dashboard
and documentation pages). Facts below are from real responses, not
documentation.

1. **Order response field name: `order_id`.** A successful
   `POST /pizzerias/{id}/orders` returns
   `{"order_id": "<uuid>", "status": "ordered", "eta_seconds": <int>}`.
   The **list** endpoint uses `id` for the same value — the two names coexist,
   one per endpoint.
2. **The list endpoint exists.** `GET /pizzerias/{id}/orders` (auth:
   `X-API-Key`) returns `{"orders": [...]}`, newest first, each with `id`,
   `customer_id`, `created_at`, `ready_at`, `status`, `delivered_at`,
   `first_name` — but **no items**. A detail endpoint
   `GET /pizzerias/{id}/orders/{order_id}` (auth: `X-API-Key`) returns the
   full order incl. `customer` and `items[]`, so submit-timeout recovery
   shortlists by `first_name` + `created_at` recency and then verifies the
   candidate's items against the basket before adopting it. The acceptance
   test asserts items and quantities through the same detail endpoint.
3. **Menu item shape:** `{"code", "name", "base": [ingredients], "price"}`.
   `price` is a number in euros (e.g. `8.5`) — the source for every price
   answer and the basket total; no other financial data exists in the API.
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
8. **The pizzeria dashboard** lives at
   `{PIZZASIM_URL}/dashboard/pizzerias/{id}` (confirmed in the dashboard's
   own routing code); the overview is `{PIZZASIM_URL}/dashboard`. The
   header's dashboard link is derived from `PIZZASIM_URL` — nothing
   hardcoded.
9. **The API documentation** is served at `{PIZZASIM_URL}/swagger.html`
   (HTTP 200); there is no `/docs` or `/openapi.json`. The footer's
   documentation link is derived from `PIZZASIM_URL`.

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

## The web channel

The web UI is where a stranger decides whether this thing works. Everything
below is required, and each line is written so it can be checked by looking at
the page.

### The conversation

Type or paste a message, get an answer. The exchange a first-time customer
should be able to have, end to end, without help:

> *What have you got?* → *What does a Margherita cost?* → *I'll take two of
> those and a pasta* → *I'm a new customer, my name is …* → read-back → confirm
> → order id and wait time.

- Prices come from the menu the API returns. Asking what something costs is a
  normal question, not an edge case, and so is asking what the basket comes to.
- After a completed order, a new conversation can be started immediately from
  the same page.

### Header

- **The pizzeria being ordered from, by name**, prominent and always visible.
- **A selector to change pizzeria, filled from the API and from nowhere else.**
  The list comes from `GET /pizzerias` at load time. No hardcoded names, no
  bundled list, no fallback entry when the call fails — if the call fails the
  page says the pizzeria list is unavailable and does not offer a choice it
  cannot honour. Each entry shows the name together with a short form of its
  UUID, so two similar names can be told apart. Changing the selection starts a
  fresh conversation for that pizzeria; a basket never crosses a tenant
  boundary.
- **A link to that pizzeria's dashboard**, opening in a new tab, pointing at the
  dashboard path for the selected pizzeria id. Without it nobody can check
  whether the order actually arrived, and checking that is the entire point of
  the product.
- **Language: German or English**, switchable, applied to the agent's replies
  and to speech in both directions.
- **Start over**, which clears the session and the basket.

### Footer

- **The running version**, `x.y.z`, taken from `APP_VERSION`. It is raised on
  every release: patch for fixes, minor for new behaviour, major for a break.
  Without it nobody can tell which build is answering.
- **The full pizzeria UUID**, selectable, for pasting into API calls.
- **Connection state** for the ordering API and the model gateway.
- **A link to the API documentation.**

### Every message gets an answer

The invariant the channel stands on: **no sent message may end without either a
rendered assistant reply or a rendered error.** Never a silent failure, never an
indicator that stops with nothing after it.

- The moment a message is sent, the UI shows that the agent is working.
- Intermediate steps are rendered as they stream — which tool was called and what
  it returned — visually distinct from the assistant's own words. A stream that
  carries tool events the page then discards is a defect: the customer sees a
  frozen screen while the agent is working normally.
- If the stream ends without a final assistant message, the UI says so.
- If the request errors, times out, or the connection drops, the UI says which
  of those happened and offers to resend.
- Errors in the customer's language, in plain words. No status codes, no
  tracebacks, no raw JSON.

### The order on screen

- The current basket is visible, with quantities and what it comes to. The code
  owns the order; the customer must be able to see what the code holds.
- The read-back is visually distinct and carries an explicit confirm control.
  Confirmation is an action the customer takes, not a word the agent claims to
  have heard.
- On success: the order id in a form a human can read back, and the wait in
  minutes.
- After submission the basket is locked and shown as submitted. Nothing on the
  page can modify or resubmit it.

---

## Speech

Speech is an input and an output method on the web channel. It is served by a
**self-hosted speech service**, CPU-only, in its own container, reached over
plain HTTP with an OpenAI-compatible surface:

| Direction | Endpoint | Payload |
|---|---|---|
| STT | `POST {SPEECH_URL}/v1/audio/transcriptions` | multipart audio file + model + language |
| TTS | `POST {SPEECH_URL}/v1/audio/speech` | JSON with model, voice, input text; returns audio |

- **The speech service is the only speech path.** No external speech provider,
  no hosted realtime framework, no audio through the LLM gateway — that gateway
  carries chat completions only.
- **The browser captures and plays audio; it does not recognise or synthesise
  it.** Capture uses the standard `getUserMedia` and `MediaRecorder`; playback
  uses a plain audio element. Both are cross-browser and cross-platform, so the
  product works in Firefox, Safari and Chrome, on Linux, macOS and Windows
  alike.
- **The browser speech APIs are not used.** `SpeechRecognition` and
  `speechSynthesis` are forbidden. The previous implementation relied on them,
  which tied the product to a single browser vendor and sent customer audio to a
  third party. The self-hosted service replaces them, and that is the whole
  reason it exists.
- **Nothing about the speech stack is written into source.** Base URL, STT
  model, TTS model, voice and language all come from the environment, exactly
  like the chat model:

  | Variable | Purpose |
  |---|---|
  | `SPEECH_URL` | base URL of the self-hosted speech service |
  | `SPEECH_STT_MODEL` | transcription model id |
  | `SPEECH_TTS_MODEL` | synthesis model id |
  | `SPEECH_TTS_VOICE` | voice id |

- **Request/response, not streaming.** The customer records, the recording is
  uploaded, the transcript comes back. Latency is visible and acceptable; do not
  build partial-result handling, barge-in or turn detection on top of it — this
  transport cannot do them, and pretending otherwise produces a broken feel.
- **The microphone is push-to-talk.** It starts and stops on the customer's
  action, never listens continuously. Recording state is visible in the UI at
  all times.
- **Synthesis is optional and off by default**, toggled by the customer, applied
  only to the final assistant message and never to intermediate steps.
- **Speech is never required.** If `SPEECH_URL` is unset or the service does not
  answer, the microphone and the speaker toggle are not rendered and the web
  channel stays fully usable as text. A speech failure is never an order failure.
- **Speech shortens answers, it does not change them.** Same core, same tools,
  same state machine. When a reply will be spoken: at most three menu items and
  an invitation, times in minutes rather than seconds, order id read in groups.
- **Confirm the name.** Transcription errors on names are the expensive failure:
  customers are unique per pizzeria by first name, so a misheard name silently
  creates a customer nobody will find again. Read the name back before
  submitting.

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
- **Browser end-to-end, and it is not optional.** At least one test drives the
  real page in a headless browser — types a message, waits for a rendered reply,
  walks a full order to submission — and asserts against the DOM, not against
  the API. Testing the API with `curl` proves the server works and proves
  nothing about the product; the customer never talks to `curl`. Include the
  three failure paths: a tool error, a stream that ends without a final message,
  and the gateway unreachable. Each must leave a visible message on the page.
- **The acceptance test is live**, and it is the only test that touches the real
  API. Opt-in via env flag so the rest of the suite stays offline. It runs a full
  conversation, submits, then reads the pizzeria's orders back and asserts the
  order is present with the right customer, items and quantities — the four
  points under *What done looks like*. If this test fails, the product does not
  work, whatever else is green.
- **Speech**, manual: dictate an order, a name that needs correcting, and a
  menu question — plus one run with `SPEECH_URL` unset, which must render a
  usable text-only UI and place an order normally.

---

## Who builds this — and who judges it

The build runs locally, on the operator's own subscriptions, with the most
capable models available. Two harnesses take part and their roles are **not**
interchangeable.

| Role | Permission |
|---|---|
| Implementer — one coding agent | writes every file |
| Reviewer / judge — a second, independent agent | read-only, never writes |

Which products and which models fill these two roles is the operator's decision
and is deliberately left out of this spec. Naming them would tie the build to
tools that will be replaced long before the product is. The roles and the
protocol below are binding; the tooling is not.

### Two model domains, never mixed

The models that build this project and the models it calls at runtime are
unrelated, and confusing them is the easiest way to break the build.

- **Build-time models** power the harnesses. Configured outside this repository,
  **none of this spec's business**. Nothing in the deliverables reads them,
  references them, or depends on them.
- **Runtime models** are what the ordering agent calls while serving a customer:
  `LITELLM_PIZZA_MODEL_1` and `LITELLM_PIZZA_MODEL_2` from the environment.

Binding consequences:

- The implementer must **never** wire the agent to whatever model the implementer
  itself happens to run on, and must never copy a build-time model name into
  source, config, prompts, tests or documentation.
- No model name of any kind is hardcoded. The runtime model is read from the
  environment at startup; a missing value is a startup failure, not a default.
- **Harness is not model.** Never ask an agent which model it is — a self-report
  is not evidence, the configuration is binding.
- Whatever the build runs on, it does not lower the bar. Do not simplify the
  design, skip a test, or accept a weaker answer on the assumption that the model
  behind you is limited.
- **One implementer, and nothing else develops.** Every artefact in
  *Deliverables* comes from it. No second implementer, no other agent writing
  "just this one file", no hand-patched fixes smuggled in between rounds.
- **The reviewer never writes the code it judges.** It runs read-only and plays
  two roles in the same call: *devil's advocate* — attack the work, find gaps,
  wrong assumptions, missing error cases — and *judge*, scoring against the fixed
  rubric below so that quality is measurable across rounds instead of a vibe.
- **The reviewer is a different agent from the implementer.** Independence is the
  point; a model reviewing its own output is not a review.

### Review protocol

Reviewer calls are **stateless** — a fresh reviewer sees nothing of the previous
round, so every request must carry its own context and be self-contained. Commit before each review so the
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
4. **Web.** FastAPI on 8888, same core. Pass only when you have opened the page
   in a browser, switched pizzeria, asked a price question, placed an order
   through the page, and then seen that order on that pizzeria's dashboard.
   Not when the endpoint answers `curl`.
5. **Speech.** Wire the speech service into the web UI, spoken-answer policy.
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
│   └── static/              ← web UI incl. speech input/output
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
| Transports | One core, two channels (CLI, web), no logic in the channels |
| Tenancy | Customer-selectable; `PIZZERIA_ID` preselects, never restricts |
| Prices | Shown from the API; no payment, no invented figures |
| Version | `x.y.z` in the footer, raised every release |
| Speech | Self-hosted container, OpenAI-compatible HTTP; no vendor, no browser API |
| Web UI | Pizzeria name, basket and connection state always visible; no message ends unanswered |
| Proof | Verified through the browser, never only through the API |
| Languages | DE + EN, mirrored per turn |
| Confirmation | Mandatory read-back tied to a basket revision |
| Parsing | The model parses. No regex order parser, ever. |
| HTTP | A real client with timeouts. No `subprocess curl`. |
| Persistence | None beyond the process and the PizzaSim API |
| Errors | Typed in code, plain language to the customer |
| Implementer | One agent only — nothing else writes code |
| Reviewer | A second, independent agent, read-only, judge and devil's advocate |
| Models | Never named, never hardcoded — environment configuration |
| Build tooling | Not specified here; the operator picks it |
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

 exited 2 in 244ms:
sed: can't read /home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801.md: No such file or directory

 succeeded in 340ms:
/home/rob/bpm-pizza-vibecoding-solution/channels/static/style.css:17:details.steps { font-size: .78rem; color: #666; margin: .2rem 0 .6rem; }
/home/rob/bpm-pizza-vibecoding-solution/channels/static/style.css:18:details.steps summary { cursor: pointer; user-select: none; }
/home/rob/bpm-pizza-vibecoding-solution/channels/static/style.css:19:details.steps pre { white-space: pre-wrap; word-break: break-all;
/home/rob/bpm-pizza-vibecoding-solution/core/state.py:57:def remove_item(order: Order, type_: str, code: str, qty: int | None) -> None:
/home/rob/bpm-pizza-vibecoding-solution/core/state.py:58:    """The spec fixes remove_item's parameters to (type, code, qty), so a
/home/rob/bpm-pizza-vibecoding-solution/core/state.py:59:    basket holding the same (type, code) with different extras needs
/home/rob/bpm-pizza-vibecoding-solution/core/state.py:89:def read_back(order: Order) -> None:
/home/rob/bpm-pizza-vibecoding-solution/core/state.py:100:    order.read_back_revision = order.revision
/home/rob/bpm-pizza-vibecoding-solution/core/state.py:120:    if order.read_back_revision != order.revision:
/home/rob/bpm-pizza-vibecoding-solution/core/state.py:122:            "read_back_required",
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:6:> repo — code, tests, prompts, tickets — derives from it.
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:51:**Core belief:** a language model is a great waiter and a terrible order pad.
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:63:  tool error carrying candidate matches — never a silent guess, never a fallback
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:90:   dashboard for that pizzeria.
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:125:- **Languages:** German and English. The agent answers in the language the
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:133:- **The success moment:** the order appears in the PizzaSim dashboard under the
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:135:- **Deterministic tests** that run with no network and no LLM.
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:174:- Secrets never appear in logs, transcripts, error messages or the web UI.
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:185:| `GET /location?street=…` | public | street plausibility check |
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:192:  "items": [{ "type": "pizza", "code": "margherita", "qty": 2, "extras": [] }]
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:215:`GET /pizzerias/{id}/orders/{order_id}`, `GET /location`, plus the dashboard
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:226:   `customer_id`, `created_at`, `ready_at`, `status`, `delivered_at`,
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:237:   there are no per-language names in the API; read-back uses `name` as-is in
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:238:   both languages. The menu response also carries a top-level `toppings[]`
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:240:4. **`extras[]` is a controlled vocabulary:** the top-level `toppings[]` from
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:242:   rejects unknown extras with `422` (`"items[0].extras contains invalid
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:243:   topping 'unicorn_dust'"`), so the tool layer validates extras against
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:244:   `toppings[]` exactly like item codes.
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:246:   `{"error": "<code>", "details": ["<human sentence>", ...]}` — e.g.
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:247:   `{"error": "validation_failed", "details": ["items[0].code must be a valid
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:248:   pizza code"]}` with HTTP 422. The tool layer maps `error` to typed errors
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:249:   and may surface `details` to targeted questions.
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:251:   `prepared_planned` → `delivered` (with `delivered_at` set on the last).
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:253:7. **`GET /location?street=` returns** `{"street": "<echo>",
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:254:   "deliverable": <bool>}` with HTTP 200. In probing, even a nonsense street
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:255:   returned `deliverable: true` — the check is a weak plausibility signal at
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:258:8. **The pizzeria dashboard** lives at
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:259:   `{PIZZASIM_URL}/dashboard/pizzerias/{id}` (confirmed in the dashboard's
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:260:   own routing code); the overview is `{PIZZASIM_URL}/dashboard`. The
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:261:   header's dashboard link is derived from `PIZZASIM_URL` — nothing
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:263:9. **The API documentation** is served at `{PIZZASIM_URL}/swagger.html`
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:279:                                                    │ read_back + customer says yes
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:286:Invariants, all enforced in code and all covered by unit tests:
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:288:1. `submit_order` outside `CONFIRMED` returns an error. It does not "helpfully"
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:293:   legal after `read_back` has been called for the current basket revision. The
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:307:| `get_menu` | — | pizzas and pasta with codes and display names in both languages |
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:308:| `add_items` | `items[]` of `{type, code, qty, extras[]}` | new basket + revision |
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:309:| `remove_item` | `code`, `type`, optional `qty` | new basket + revision |
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:311:| `read_back` | — | basket, customer, revision — the text the agent must read out |
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:312:| `confirm_order` | `revision` | state `CONFIRMED`, or error if stale |
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:320:- Failure: `{"error": {"code": "...", "message": "...", "candidates": [...]}}`.
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:334:- Greet first, in the language of the pizzeria's country, and offer help — one
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:340:- Before submitting: call `read_back`, say it, and wait for an explicit yes.
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:346:- On error, explain in plain language what happened and what the customer's
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:383:- **A link to that pizzeria's dashboard**, opening in a new tab, pointing at the
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:384:  dashboard path for the selected pizzeria id. Without it nobody can check
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:403:rendered assistant reply or a rendered error.** Never a silent failure, never an
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:412:- If the request errors, times out, or the connection drops, the UI says which
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:414:- Errors in the customer's language, in plain words. No status codes, no
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:439:| STT | `POST {SPEECH_URL}/v1/audio/transcriptions` | multipart audio file + model + language |
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:440:| TTS | `POST {SPEECH_URL}/v1/audio/speech` | JSON with model, voice, input text; returns audio |
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:456:  model, TTS model, voice and language all come from the environment, exactly
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:461:  | `SPEECH_URL` | base URL of the self-hosted speech service |
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:462:  | `SPEECH_STT_MODEL` | transcription model id |
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:463:  | `SPEECH_TTS_MODEL` | synthesis model id |
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:464:  | `SPEECH_TTS_VOICE` | voice id |
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:475:- **Speech is never required.** If `SPEECH_URL` is unset or the service does not
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:481:- **Confirm the name.** Transcription errors on names are the expensive failure:
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:545:  three failure paths: a tool error, a stream that ends without a final message,
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:554:  menu question — plus one run with `SPEECH_URL` unset, which must render a
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:581:  **none of this spec's business**. Nothing in the deliverables reads them,
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:590:  source, config, prompts, tests or documentation.
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:603:  wrong assumptions, missing error cases — and *judge*, scoring against the fixed
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:618:error_handling: N
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:639:   loop, error handling, conversation state. **No code.** Send it to the reviewer
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:656:1. **Core.** Order model, state machine, tool layer, tests. No LLM, no network.
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:657:   Pass when the unit tests are green.
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:659:3. **CLI.** Full conversation, real API, an order visible in the dashboard.
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:662:   through the page, and then seen that order on that pizzeria's dashboard.
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:665:6. **Harden.** Walk the error table, force each case, fix what breaks.
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:685:│   ├── pizzasim.py          ← API client, typed errors, timeouts
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:695:├── tests/
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:706:## Decisions locked
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:726:| Errors | Typed in code, plain language to the customer |
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:735:- Extras and modifiers beyond a passthrough `extras[]`.
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:739:- Additional languages beyond DE + EN.
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:748:  or by "schema / implementation / tests".
/home/rob/bpm-pizza-vibecoding-solution/core/tools.py:4:{"error": {"code", "message", "candidates"}} with a speakable message.
/home/rob/bpm-pizza-vibecoding-solution/core/tools.py:28:        "extras": {"type": "array", "items": {"type": "string"}},
/home/rob/bpm-pizza-vibecoding-solution/core/tools.py:36:                    "names, and the available extra toppings.",
/home/rob/bpm-pizza-vibecoding-solution/core/tools.py:46:    {"name": "remove_item",
/home/rob/bpm-pizza-vibecoding-solution/core/tools.py:64:    {"name": "read_back",
/home/rob/bpm-pizza-vibecoding-solution/core/tools.py:94:def _error(code: str, message: str, candidates: list | None = None) -> dict:
/home/rob/bpm-pizza-vibecoding-solution/core/tools.py:95:    return {"error": {"code": code, "message": message,
/home/rob/bpm-pizza-vibecoding-solution/core/tools.py:116:        return _error(exc.code, exc.message, exc.candidates)
/home/rob/bpm-pizza-vibecoding-solution/core/tools.py:118:        return _error(exc.code, exc.message)
/home/rob/bpm-pizza-vibecoding-solution/core/tools.py:120:        return _error("api_unavailable",
/home/rob/bpm-pizza-vibecoding-solution/core/tools.py:123:        return _error("api_unavailable",
/home/rob/bpm-pizza-vibecoding-solution/core/tools.py:126:        return _error("api_unavailable",
/home/rob/bpm-pizza-vibecoding-solution/core/tools.py:138:            extras = raw.get("extras") or []
/home/rob/bpm-pizza-vibecoding-solution/core/tools.py:139:            menu.validate_extras(extras)
/home/rob/bpm-pizza-vibecoding-solution/core/tools.py:146:                extras=extras,
/home/rob/bpm-pizza-vibecoding-solution/core/tools.py:149:            return _error("invalid_quantity", "What can I get you?")
/home/rob/bpm-pizza-vibecoding-solution/core/tools.py:153:    if name == "remove_item":
/home/rob/bpm-pizza-vibecoding-solution/core/tools.py:155:        state.remove_item(order, args.get("type", ""), args.get("code", ""),
/home/rob/bpm-pizza-vibecoding-solution/core/tools.py:162:            return _error("invalid_state", "I still need a name.")
/home/rob/bpm-pizza-vibecoding-solution/core/tools.py:168:    if name == "read_back":
/home/rob/bpm-pizza-vibecoding-solution/core/tools.py:169:        state.read_back(order)
/home/rob/bpm-pizza-vibecoding-solution/core/tools.py:175:            return _error("stale_revision",
/home/rob/bpm-pizza-vibecoding-solution/core/tools.py:186:                "deliverable": bool(result.get("deliverable")),
/home/rob/bpm-pizza-vibecoding-solution/core/tools.py:189:    return _error("unknown_tool", "Something went wrong on my side.")
/home/rob/bpm-pizza-vibecoding-solution/core/tools.py:199:            (e["type"], e["code"], e["qty"], tuple(sorted(e["extras"])))
/home/rob/bpm-pizza-vibecoding-solution/core/tools.py:203:             "extras": list(i.extras)} for i in basket]
/home/rob/bpm-pizza-vibecoding-solution/core/tools.py:218:            return _error("submit_unknown", _UNSURE)
/home/rob/bpm-pizza-vibecoding-solution/core/tools.py:230:                return _error("submit_unknown", _UNSURE)
/home/rob/bpm-pizza-vibecoding-solution/core/tools.py:245:              "extras": list(i.extras)} for i in order.items]
/home/rob/bpm-pizza-vibecoding-solution/core/tools.py:249:        return _error("submit_failed",
/home/rob/bpm-pizza-vibecoding-solution/core/tools.py:251:                      + "; ".join(exc.details))
/home/rob/bpm-pizza-vibecoding-solution/core/tools.py:253:        return _error("api_unavailable",
/home/rob/bpm-pizza-vibecoding-solution/core/tools.py:257:        return _error("submit_unknown", _UNSURE)
/home/rob/bpm-pizza-vibecoding-solution/decisions/qa.md:3:## 2026-07-31 — Greeting language source
/home/rob/bpm-pizza-vibecoding-solution/decisions/qa.md:5:**Q:** SPEC requires greeting in the pizzeria-country language; the live API
/home/rob/bpm-pizza-vibecoding-solution/decisions/qa.md:7:Which mechanism: (a) optional env `PIZZERIA_LANG` default de, (b) required
/home/rob/bpm-pizza-vibecoding-solution/decisions/qa.md:10:**A (decision):** **(b)** — `PIZZERIA_LANG` (de|en) is a required env var.
/home/rob/bpm-pizza-vibecoding-solution/decisions/qa.md:13:before the first turn naming `PIZZERIA_LANG` and where it was expected; no
/home/rob/bpm-pizza-vibecoding-solution/decisions/qa.md:27:1. `PIZZERIA_LANG` must be documented in SPEC.md's env table — no hidden
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:6:> the repo — code, tests, prompts, tickets — derives from it.
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:47:   that pizzeria's dashboard.
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:88:**Core belief:** a language model is a great waiter and a terrible order pad.
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:100:  tool error carrying candidate matches — never a silent guess, never a
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:128:- **Languages:** German and English. The agent answers in the language the
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:134:- **Deterministic tests** that run with no network and no LLM, plus one live
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:163:| `PIZZASIM_URL` | PizzaSim API base URL; dashboard and docs links derive from it |
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:167:| `SPEECH_URL` | Base URL of the self-hosted speech service (optional) |
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:168:| `SPEECH_STT_MODEL` | Transcription model id |
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:169:| `SPEECH_TTS_MODEL` | Synthesis model id |
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:170:| `SPEECH_TTS_VOICE` | Voice id |
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:178:  half-configured. `SPEECH_*` are the exception: absent means the speech
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:180:- Secrets never appear in logs, transcripts, error messages or the web UI.
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:195:| `GET /location?street=…` | public | street plausibility check (optional tool) |
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:202:  "items": [{ "type": "pizza", "code": "margherita", "qty": 2, "extras": [] }]
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:210:- Dashboard of a pizzeria: `{PIZZASIM_URL}/dashboard/pizzerias/{id}`
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:211:  (verified against the dashboard's routing code).
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:212:- API documentation: `{PIZZASIM_URL}/swagger.html` — there is **no** `/docs`.
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:231:1. **Menu item shape** beyond `code` — display names per language, price
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:234:2. **`extras[]`** — controlled vocabulary or free text? If controlled,
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:237:   can map to typed errors, or only a message?
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:239:5. **`GET /location` response shape** and what a negative result means.
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:249:                                                    │ read_back + customer says yes
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:256:Invariants, all enforced in code and all covered by unit tests:
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:258:1. `submit_order` outside `CONFIRMED` returns an error. It does not
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:263:   after `read_back` for the current basket revision. The basket carries a
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:280:| `add_items` | `items[]` of `{type, code, qty, extras[]}` | new basket + revision |
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:281:| `remove_item` | `code`, `type`, optional `qty` | new basket + revision |
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:283:| `read_back` | — | basket, customer, revision — the text the agent reads out |
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:284:| `confirm_order` | `revision` | state `CONFIRMED`, or error if stale |
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:292:- Failure: `{"error": {"code": "...", "message": "...", "candidates": [...]}}`.
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:306:- Greet first, in the customer's UI language, and offer help — one sentence,
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:315:- Before submitting: call `read_back`, present it, and wait for an explicit
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:322:- On error, explain in plain language what happened and what the options are.
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:356:- **A link to that pizzeria's dashboard**
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:357:  (`{PIZZASIM_URL}/dashboard/pizzerias/{id}`), opening in a new tab. Without
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:371:- **A link to the API documentation** (`{PIZZASIM_URL}/swagger.html`).
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:376:a rendered assistant reply or a rendered error.** Never a silent failure,
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:385:- If the request errors, times out, or the connection drops, the UI says which
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:387:- Errors in the customer's language, in plain words. No status codes, no
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:411:| STT | `POST {SPEECH_URL}/v1/audio/transcriptions` | multipart audio + model + language |
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:412:| TTS | `POST {SPEECH_URL}/v1/audio/speech` | JSON: model, voice, input text → audio |
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:426:  voice and language come from the environment, exactly like the chat model.
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:435:- **Speech is never required.** With `SPEECH_URL` unset or the service down,
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:441:- **Confirm the name.** Transcription errors on names are the expensive
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:510:  customer never talks to `curl`. Include three failure paths: a tool error, a
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:518:  question — plus one run with `SPEECH_URL` unset, which must render a usable
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:543:  assumptions, missing error cases — and *judge*, scoring against the fixed
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:551:  repository, none of this spec's business. Nothing in the deliverables
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:560:  config, prompts, tests or docs.
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:579:error_handling: N
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:600:   loop, error handling, conversation state. **No code.** Iterate with the
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:617:0. **Contracts.** Resolve the open contract questions against the live API,
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:620:1. **Core.** Order model, state machine, tool layer, tests. No LLM, no
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:621:   network. Pass when the unit tests are green.
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:623:3. **CLI.** Full conversation, real API, an order visible on the dashboard.
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:626:   order through the page, and seen it on that pizzeria's dashboard — not
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:630:6. **Harden.** Walk the error table, force each case, fix what breaks.
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:649:│   ├── pizzasim.py          ← API client, typed errors, timeouts
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:660:├── tests/
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:672:## Decisions locked
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:692:| Errors | Typed in code, plain language to the customer |
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:703:- Extras and modifiers beyond a passthrough `extras[]`.
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:706:- Additional languages beyond DE + EN.
/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:715:  or by "schema / implementation / tests".
/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js:38:  const details = document.createElement("details");
/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js:39:  details.className = "steps";
/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js:40:  details.innerHTML = "<summary>Zwischenschritte</summary>";
/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js:41:  chat.appendChild(details);
/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js:42:  return details;
/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js:78:        } else if (ev.type === "error") {
/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js:161:    speechEnabled = cfg.speech;    // unset SPEECH_URL → nothing rendered
/home/rob/bpm-pizza-vibecoding-solution/channels/cli.py:40:        print(f"Configuration error: {exc}", file=sys.stderr)
/home/rob/bpm-pizza-vibecoding-solution/core/order.py:22:    extras: list[str] = field(default_factory=list)
/home/rob/bpm-pizza-vibecoding-solution/core/order.py:25:        return (self.type, self.code, tuple(sorted(self.extras)))
/home/rob/bpm-pizza-vibecoding-solution/core/order.py:42:    read_back_revision: int | None = None
/home/rob/bpm-pizza-vibecoding-solution/core/order.py:59:                    "extras": list(i.extras),
/home/rob/bpm-pizza-vibecoding-solution/core/order.py:64:            "read_back_done": self.read_back_revision == self.revision,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:14:1. Devil's advocate: attack the implementation — bugs, gaps, missing error cases, spec violations, divergence from the approved plan.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:17:Task: Review the IMPLEMENTATION (stage 2) against SPEC.md (source of truth) and PLAN.md (the approved stage-1 plan, 24/25 APPROVED in reviews/round3-plan.md). The implementation is: core/ (order, state, menu, pizzasim, tools, agent), channels/ (cli.py, web.py, static/), prompts/, tests/ (state, tools, transcripts + fixtures), README.md, .env.example, requirements.txt.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:19:Facts you cannot observe from the files, all demonstrated live before this review: the full deterministic suite passes (67 passed, 1 skipped opt-in live test); the web channel started with SPEECH_URL unset (speech:false, mic not rendered) and placed a real order end to end via the real gateway (read_back -> confirm_order(revision) -> submit_order -> order_id 3fe1deaa-... visible in the pizzeria's order list); a missing required env var exits before the first turn naming the variable and file. You may run the test suite yourself if your sandbox permits; otherwise judge from the code.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:21:Scope notes: tests/fixtures/*.json are recorded real API responses (UUIDs in them are recorded data, not hardcoded config). The venv/ and logs/ directories are gitignored runtime artifacts, out of scope.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:27:error_handling: N
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:146:The agent can still run tests, stage files, and output suggested branch
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:150:/bin/bash -lc "pwd && rg --files -g 'SPEC.md' -g 'PLAN.md' -g 'README.md' -g '.env.example' -g 'requirements.txt' -g 'reviews/**' -g 'core/**' -g 'channels/**' -g 'prompts/**' -g 'tests/**'" in /home/rob/bpm-pizza-vibecoding-solution
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:182:tests/__pycache__/test_tools.cpython-313-pytest-9.1.1.pyc
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:183:tests/__pycache__/__init__.cpython-313.pyc
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:184:tests/__pycache__/test_transcripts.cpython-313-pytest-9.1.1.pyc
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:185:tests/__pycache__/test_state.cpython-313-pytest-9.1.1.pyc
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:186:tests/__init__.py
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:187:tests/test_tools.py
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:188:tests/test_state.py
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:189:tests/test_transcripts.py
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:190:tests/fixtures/menu.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:191:tests/fixtures/order_created.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:192:tests/fixtures/pizzerias.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:193:tests/fixtures/orders_list.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:194:tests/fixtures/location.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:195:tests/fixtures/error_422.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:196:tests/transcripts/unknown_item.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:197:tests/transcripts/mind_change.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:198:tests/transcripts/submit_timeout.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:199:tests/transcripts/happy_path.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:200:tests/transcripts/correction.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:209:  • Inspect implementation files and tests against spec/plan requirements
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:219:> repo — code, tests, prompts, tickets — derives from it.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:264:**Core belief:** a language model is a great waiter and a terrible order pad.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:276:  tool error carrying candidate matches — never a silent guess, never a fallback
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:301:- **Languages:** German and English. The agent answers in the language the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:305:- **The success moment:** the order appears in the PizzaSim dashboard under the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:307:- **Deterministic tests** that run with no network and no LLM.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:345:- Secrets never appear in logs, transcripts, error messages or the web UI.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:356:| `GET /location?street=…` | public | street plausibility check |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:363:  "items": [{ "type": "pizza", "code": "margherita", "qty": 2, "extras": [] }]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:385:invalid bodies —, `GET /pizzerias/{id}/orders`, `GET /location`). Facts below
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:395:   `customer_id`, `created_at`, `ready_at`, `status`, `delivered_at`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:400:   there are no per-language names in the API; read-back uses `name` as-is in
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:401:   both languages. The menu response also carries a top-level `toppings[]`
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:403:4. **`extras[]` is a controlled vocabulary:** the top-level `toppings[]` from
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:405:   rejects unknown extras with `422` (`"items[0].extras contains invalid
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:406:   topping 'unicorn_dust'"`), so the tool layer validates extras against
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:407:   `toppings[]` exactly like item codes.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:409:   `{"error": "<code>", "details": ["<human sentence>", ...]}` — e.g.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:410:   `{"error": "validation_failed", "details": ["items[0].code must be a valid
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:411:   pizza code"]}` with HTTP 422. The tool layer maps `error` to typed errors
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:412:   and may surface `details` to targeted questions.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:414:   `prepared_planned` → `delivered` (with `delivered_at` set on the last).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:416:7. **`GET /location?street=` returns** `{"street": "<echo>",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:417:   "deliverable": <bool>}` with HTTP 200. In probing, even a nonsense street
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:418:   returned `deliverable: true` — the check is a weak plausibility signal at
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:434:                                                    │ read_back + customer says yes
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:441:Invariants, all enforced in code and all covered by unit tests:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:443:1. `submit_order` outside `CONFIRMED` returns an error. It does not "helpfully"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:448:   legal after `read_back` has been called for the current basket revision. The
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:462:| `get_menu` | — | pizzas and pasta with codes and display names in both languages |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:463:| `add_items` | `items[]` of `{type, code, qty, extras[]}` | new basket + revision |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:464:| `remove_item` | `code`, `type`, optional `qty` | new basket + revision |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:466:| `read_back` | — | basket, customer, revision — the text the agent must read out |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:467:| `confirm_order` | `revision` | state `CONFIRMED`, or error if stale |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:494:`uvicorn` (web channel), `pytest` (tests), stdlib `difflib` (candidate
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:504:- Secrets never appear in logs, transcripts, errors, or the web UI.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:508:- No build-time model name anywhere in source, config, prompts, tests, docs.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:512:- Deterministic tests: no network, no LLM (one opt-in live smoke test).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:523:  menu.py      Immutable Menu snapshot (pizzas, pasta, toppings), one per
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:524:               session; (type, code) validation; extras validation;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:527:               submit_order, check_street; typed errors; timeouts;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:531:               {"error": {code, message, candidates}}.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:544:  system.de.md German system prompt (default deployment language).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:546:tests/
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:548:               list, 422 bodies, location).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:559:Deviation from the SPEC tree, documented: `tests/test_transcripts.py` and
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:569:| `core/agent.py` | `LITELLM_PIZZA_URL`, `LITELLM_PIZZA_KEY`, `LITELLM_PIZZA_MODEL_1`, `PIZZERIA_LANG` (all required; `LITELLM_PIZZA_MODEL_2` read but unused — single-model build) |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:571:| `channels/web.py` | `SPEECH_URL`, `SPEECH_STT_MODEL`, `SPEECH_TTS_MODEL`, `SPEECH_TTS_VOICE` (all optional; absence disables speech) |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:573:`PIZZERIA_LANG` ∈ {`de`, `en`} is the pizzeria-country greeting language.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:577:`decisions/qa.md`). It selects the system prompt file and the STT language
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:578:hint; it never overrides per-turn language mirroring.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:591:   404-pizzeria case from the error table → process refuses to start;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:609:Order fields: `items: list[Item(type, code, qty, extras)]`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:611:(increments on every basket or customer mutation), `read_back_revision:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:612:int | None` (set by `read_back`), `state`, `submit_attempted_at: int | None`
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:626:Transition table (✓ legal, ✗ → typed error):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:631:| remove_item | ✗ empty_basket | ✓ | ✓ | ✓ demote | ✗ order_closed |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:633:| read_back | ✗ empty_basket | ✗ invalid_state (no customer yet) | ✓ | ✓ (same basket, idempotent) | ✗ order_closed |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:639:(else `stale_revision`) and `read_back_revision == order.revision` (else
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:640:`read_back_required`). So the only path into `CONFIRMED` is: state `READY`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:641:`read_back` called at the current revision, then `confirm_order` naming that
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:652:real retry. List endpoint itself fails → error `submit_unknown` with an
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:662:`{state, revision, items: [{type, code, name, qty, extras}], customer:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:663:{first_name, street_one} | null, read_back_done: bool}` — never a diff.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:667:| `get_menu` | `{}` | `{"menu": {"pizzas": [{code, name}], "pasta": [{code, name}], "toppings": [str]}, "snapshot": SNAPSHOT}` — `name` is the API's single display name, which the verified contract facts show serves both languages |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:668:| `add_items` | `{items: [{type: enum[pizza,pasta], code: str, qty: int ≥1, extras: [str]}]}` (required: items; extras default `[]`) | `{"snapshot": SNAPSHOT}` (basket + revision live in SNAPSHOT) |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:669:| `remove_item` | `{type: enum, code: str, qty: int ≥1 optional}` (absent qty = remove all of that line) | `{"snapshot": SNAPSHOT}` |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:671:| `read_back` | `{}` | `{"snapshot": SNAPSHOT}` — basket, customer, revision: the material the agent reads out |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:672:| `confirm_order` | `{revision: int}` | `{"snapshot": SNAPSHOT}` with `state == "CONFIRMED"`, or error if stale |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:674:| `check_street` | `{street: str}` | `{"street": str, "deliverable": bool, "snapshot": SNAPSHOT}` — the never-claim-verified rule lives in the prompt, not the tool |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:676:Failure shape: `{"error": {"code": "<one of the codes below>", "message":
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:680:candidate toppings), `invalid_quantity` (non-integer or < 1 — the tool does
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:682:`read_back_required`, `order_closed`, `submit_failed`, `submit_unknown`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:683:`api_unavailable`, `not_in_basket` (remove_item for a line that isn't there).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:686:snapshot and every extra against `toppings[]`; any failure rejects the whole
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:687:call atomically (no partial adds), returning the first error with candidates
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:696:  `lang = PIZZERIA_LANG` — the pizzeria-country greeting language, a
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:699:  language of the customer's latest message (German or English), unprompted.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:700:  Language mirroring is model behaviour; the runtime never detects language.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:707:  the plain apology from the error table. Gateway 4xx/5xx: no retry, abort
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:710:  `tool_result`, `state`, `error` — the CLI prints them (verbose), the web
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:718:`prompts/system.de.md` / `system.en.md`, same content in two languages, calm
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:720:greet once in the file's language and offer help in one sentence; mirror the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:721:customer's language per turn (German ↔ English); one question per turn; menu
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:723:came from speech) and street, street declinable; read back via `read_back`
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:726:state order id in speakable groups and ETA in minutes; errors in plain
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:727:language, never codes or JSON; never claim the address was checked for
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:734:  `SPEECH_URL` set and a probe succeeded at startup). No language field:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:735:  language is never a UI control — the greeting comes from `PIZZERIA_LANG`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:755:1. Devil's advocate: attack the plan — gaps, wrong assumptions, missing error cases, spec violations.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:758:Task: Read SPEC.md (the source of truth) and PLAN.md (the stage-1 implementation plan under review, round 3 of max 3). Judge whether PLAN.md is a complete, correct, spec-compliant plan such that implementing exactly it satisfies SPEC.md. The "Contract facts" section in SPEC.md was verified against the live API and is trustworthy. decisions/qa.md records an oracle decision on the greeting language (required env var PIZZERIA_LANG) taken between rounds.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:760:Round 2 (stateless, see reviews/round2-plan.md) required: (1) one exact tool-result contract per tool composing the per-tool table with the full-current-state rule, and fixing an eta_minutes test regression; (2) a spec-compliant, non-hardcoded, non-UI source for the greeting language; (3) explicit persisted state for submit-timeout recovery correlation; (4) removing lang from the chat contract or fencing it to an STT hint; (5) per-session immutable menu snapshot ownership. All five were addressed in the current PLAN.md — verify in the file, do not take this note on faith: see the SNAPSHOT definition in "Tool schemas", the PIZZERIA_LANG paragraph in "Configuration", submit_attempted_at in the state-machine section, the web protocol section, and the "Session model" paragraph.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:768:error_handling: N
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:803:1. Devil's advocate: attack the plan — gaps, wrong assumptions, missing error cases, spec violations.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:808:Context from round 1 (a previous stateless review): it required (a) no ./.env fallback and no extra config vars, (b) tool results matching the spec's fixed contract exactly, (c) greeting in the pizzeria-country language with per-turn mirroring not driven by UI controls, (d) one explicit startup sequence validating PIZZERIA_ID via GET /pizzerias, (e) a confirmation path no broader than the spec. All five were applied; verify they are actually resolved in the current PLAN.md rather than taking this note on faith.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:814:error_handling: N
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:901:> repo — code, tests, prompts, tickets — derives from it.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:946:**Core belief:** a language model is a great waiter and a terrible order pad.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:958:  tool error carrying candidate matches — never a silent guess, never a fallback
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:983:- **Languages:** German and English. The agent answers in the language the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:987:- **The success moment:** the order appears in the PizzaSim dashboard under the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:989:- **Deterministic tests** that run with no network and no LLM.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1004:I’ve got the spec and approved plan loaded. Next I’m checking the core and channel code against the plan’s promised behavior, then I’ll cross-check tests for the failure modes the spec requires.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1006:  → Inspect implementation files and tests against spec/plan requirements
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1013:/bin/bash -lc 'rg -n "''^(class|def) |OrderState|TOOL_SCHEMAS|FastAPI|@app|httpx|PIZZERIA_LANG|SPEECH_URL|submit_unknown|submit_attempted_at|read_back_revision|application/x-ndjson" core channels tests README.md .env.example requirements.txt' in /home/rob/bpm-pizza-vibecoding-solution
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1038:    extras: list[str] = field(default_factory=list)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1041:        return (self.type, self.code, tuple(sorted(self.extras)))
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1058:    read_back_revision: int | None = None
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1075:                    "extras": list(i.extras),
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1080:            "read_back_done": self.read_back_revision == self.revision,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1135:def remove_item(order: Order, type_: str, code: str, qty: int | None) -> None:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1158:def read_back(order: Order) -> None:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1169:    order.read_back_revision = order.revision
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1189:    if order.read_back_revision != order.revision:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1191:            "read_back_required",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1218:"""Immutable menu snapshot: (type, code) validation, extras validation,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1239:        self.toppings: list[str] = list(payload.get("toppings", []))
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1247:            "toppings": self.toppings,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1276:    def validate_extras(self, extras: list[str]) -> None:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1277:        for extra in extras:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1278:            if extra not in self.toppings:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1282:                        extra.lower(), self.toppings, n=3, cutoff=0.5
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1321:.env.example:15:PIZZERIA_LANG=
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1322:.env.example:18:SPEECH_URL=
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1323:README.md:27:The agent greets first, in the language set by `PIZZERIA_LANG`, and answers
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1324:README.md:43:Set `SPEECH_URL`, `SPEECH_STT_MODEL`, `SPEECH_TTS_MODEL` and
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1325:README.md:47:`SPEECH_URL` unset — or the service down at startup — mic and toggle are
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1326:README.md:52:question; and one run with `SPEECH_URL` unset placing an order as text.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1327:core/pizzasim.py:1:"""PizzaSim API client: httpx, explicit timeouts, typed errors.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1350:core/agent.py:40:    lang: str  # PIZZERIA_LANG: greeting language = pizzeria country
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1351:core/agent.py:44:        lang = require_env("PIZZERIA_LANG").lower()
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1352:core/agent.py:47:                "PIZZERIA_LANG must be 'de' or 'en', got something else"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1364:core/tools.py:94:def _error(code: str, message: str, candidates: list | None = None) -> dict:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1370:core/tools.py:205:            return _error("submit_unknown", _UNSURE)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1373:core/tools.py:239:        return _error("submit_unknown", _UNSURE)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1378:channels/web.py:4:proxies the optional self-hosted speech service (STT/TTS). If SPEECH_URL is
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1383:channels/web.py:34:    enabled only if SPEECH_URL is set, answers, and models are configured."""
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1384:channels/web.py:37:        self.url = optional_env("SPEECH_URL")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1405:channels/static/app.js:153:    if (speechEnabled) {           // unset SPEECH_URL → not rendered at all
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1410:core/order.py:42:    read_back_revision: int | None = None
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1413:core/order.py:64:            "read_back_done": self.read_back_revision == self.revision,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1414:tests/test_transcripts.py:19:class StubModel:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1415:tests/test_transcripts.py:42:class ScriptedClient:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1416:tests/test_transcripts.py:73:def test_golden_transcript(path):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1417:tests/test_transcripts.py:110:def test_five_transcripts_exist():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1418:tests/test_transcripts.py:114:def test_gateway_timeout_apology():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1419:tests/transcripts/submit_timeout.json:27:    "error_codes": ["submit_unknown"],
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1420:tests/test_tools.py:9:import httpx
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1421:tests/test_tools.py:27:def fixture(name):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1422:tests/test_tools.py:32:def menu():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1423:tests/test_tools.py:38:def test_known_codes(menu):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1424:tests/test_tools.py:43:def test_tonno_collision_is_per_type(menu):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1425:tests/test_tools.py:49:def test_unknown_code_gives_candidates(menu):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1426:tests/test_tools.py:57:def test_wrong_type_falls_back_to_other_type(menu):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1427:tests/test_tools.py:64:def test_extras_controlled_vocabulary(menu):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1428:tests/test_tools.py:71:# --- pizzasim client typed errors (httpx MockTransport) -------------------
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1429:tests/test_tools.py:73:def client_returning(handler):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1430:tests/test_tools.py:75:                    transport=httpx.MockTransport(handler))
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1431:tests/test_tools.py:78:def respond(status, body):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1432:tests/test_tools.py:79:    return lambda request: httpx.Response(status, json=body)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1433:tests/test_tools.py:82:def test_auth_error_mapped():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1434:tests/test_tools.py:89:def test_404_mapped():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1435:tests/test_tools.py:94:def test_422_mapped_with_details():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1436:tests/test_tools.py:102:def test_5xx_mapped():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1437:tests/test_tools.py:107:def test_timeout_mapped():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1438:tests/test_tools.py:109:        raise httpx.ConnectTimeout("boom")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1439:tests/test_tools.py:114:def test_pizzeria_name_startup_check():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1440:tests/test_tools.py:118:                    transport=httpx.MockTransport(respond(200, payload)))
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1441:tests/test_tools.py:125:def test_submit_parses_order_created():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1442:tests/test_tools.py:134:class FakeClient:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1443:tests/test_tools.py:157:def fake():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1444:tests/test_tools.py:161:def ready_order(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1445:tests/test_tools.py:171:def confirmed_order(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1446:tests/test_tools.py:180:def test_every_success_carries_full_snapshot(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1447:tests/test_tools.py:194:def test_unknown_item_error_shape(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1448:tests/test_tools.py:204:def test_add_is_atomic(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1449:tests/test_tools.py:216:def test_invalid_quantity_not_parsed(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1450:tests/test_tools.py:226:def test_invalid_extra_via_dispatch(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1451:tests/test_tools.py:234:def test_remove_semantics(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1452:tests/test_tools.py:246:def test_submit_success(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1453:tests/test_tools.py:255:def test_submit_outside_confirmed_is_tool_error(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1454:tests/test_tools.py:263:def test_empty_basket_submit(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1455:tests/test_tools.py:269:def test_submit_timeout_then_recovery_via_list(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1456:tests/test_tools.py:273:    assert result["error"]["code"] == "submit_unknown"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1457:tests/test_tools.py:274:    assert order.state is State.CONFIRMED and order.submit_unknown
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1458:tests/test_tools.py:287:def test_submit_timeout_verified_absent_allows_one_retry(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1459:tests/test_tools.py:291:    assert result["error"]["code"] == "submit_unknown"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1460:tests/test_tools.py:302:def test_submit_unknown_when_list_unavailable(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1461:tests/test_tools.py:308:    assert result["error"]["code"] == "submit_unknown"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1462:tests/test_tools.py:312:def test_submit_422_keeps_basket(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1463:tests/test_tools.py:322:def test_auth_error_no_retry(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1464:tests/test_tools.py:327:    assert not order.submit_unknown  # not the retry path
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1465:tests/test_tools.py:330:def test_street_omitted_from_submit_body(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1466:tests/test_tools.py:355:def test_check_street(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1467:tests/test_tools.py:365:def test_live_order_smoke():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1468:tests/test_state.py:10:def item(code="margherita", type_="pizza", qty=1, extras=None):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1469:tests/test_state.py:15:def order_in(target: State) -> Order:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1470:tests/test_state.py:35:def expect(code):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1471:tests/test_state.py:41:def test_full_happy_path():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1472:tests/test_state.py:58:def test_customer_before_items_is_legal_and_stays_empty():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1473:tests/test_state.py:76:def test_submitted_is_terminal(mutate):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1474:tests/test_state.py:83:def test_remove_from_empty():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1475:tests/test_state.py:89:def test_read_back_empty():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1476:tests/test_state.py:95:def test_read_back_collecting_needs_customer():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1477:tests/test_state.py:102:def test_confirm_illegal_states(st):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1478:tests/test_state.py:109:def test_confirm_when_already_confirmed():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1479:tests/test_state.py:117:def test_submit_outside_confirmed(st):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1480:tests/test_state.py:125:def test_remove_unknown_line():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1481:tests/test_state.py:134:def test_add_after_confirmed_demotes_to_ready():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1482:tests/test_state.py:140:def test_remove_after_confirmed_demotes():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1483:tests/test_state.py:146:def test_set_customer_after_confirmed_demotes():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1484:tests/test_state.py:152:def test_confirmation_does_not_survive_demotion():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1485:tests/test_state.py:162:def test_confirm_without_read_back():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1486:tests/test_state.py:169:def test_confirm_with_stale_revision():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1487:tests/test_state.py:179:def test_read_back_of_old_revision_does_not_allow_confirm():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1488:tests/test_state.py:190:def test_revision_increments_on_every_mutation():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1489:tests/test_state.py:199:def test_merge_same_line():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1490:tests/test_state.py:206:def test_same_code_different_extras_is_separate_line():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1491:tests/test_state.py:213:def test_partial_remove():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1492:tests/test_state.py:223:def test_remove_to_empty_and_readd():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1493:tests/test_state.py:231:def test_type_and_code_key_removal():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1494:tests/test_state.py:239:def test_submit_attempt_timestamp_set_once():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1495:tests/test_state.py:242:    first = o.submit_attempted_at
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1496:tests/test_state.py:245:    assert o.submit_attempted_at == first
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1501:core/state.py:52:def remove_item(order: Order, type_: str, code: str, qty: int | None) -> None:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1503:core/state.py:75:def read_back(order: Order) -> None:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1504:core/state.py:86:    order.read_back_revision = order.revision
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1506:core/state.py:106:    if order.read_back_revision != order.revision:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1527:{"error": {"code", "message", "candidates"}} with a speakable message.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1551:        "extras": {"type": "array", "items": {"type": "string"}},
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1559:                    "names, and the available extra toppings.",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1569:    {"name": "remove_item",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1587:    {"name": "read_back",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1617:def _error(code: str, message: str, candidates: list | None = None) -> dict:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1618:    return {"error": {"code": code, "message": message,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1639:        return _error(exc.code, exc.message, exc.candidates)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1641:        return _error(exc.code, exc.message)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1643:        return _error("api_unavailable",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1646:        return _error("api_unavailable",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1649:        return _error("api_unavailable",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1661:            extras = raw.get("extras") or []
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1662:            menu.validate_extras(extras)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1669:                extras=extras,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1672:            return _error("invalid_quantity", "What can I get you?")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1676:    if name == "remove_item":
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1678:        state.remove_item(order, args.get("type", ""), args.get("code", ""),
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1685:            return _error("invalid_state", "I still need a name.")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1691:    if name == "read_back":
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1692:        state.read_back(order)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1698:            return _error("stale_revision",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1709:                "deliverable": bool(result.get("deliverable")),
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1712:    return _error("unknown_tool", "Something went wrong on my side.")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1728:            return _error("submit_unknown", _UNSURE)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1750:              "extras": list(i.extras)} for i in order.items]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1754:        return _error("submit_failed",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1756:                      + "; ".join(exc.details))
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1758:        return _error("api_unavailable",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1762:        return _error("submit_unknown", _UNSURE)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1775:proxies the optional self-hosted speech service (STT/TTS). If SPEECH_URL is
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1805:    enabled only if SPEECH_URL is set, answers, and models are configured."""
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1808:        self.url = optional_env("SPEECH_URL")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1809:        self.stt_model = optional_env("SPEECH_STT_MODEL")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1810:        self.tts_model = optional_env("SPEECH_TTS_MODEL")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1811:        self.voice = optional_env("SPEECH_TTS_VOICE")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1828:        print(f"Configuration error: {exc}", file=sys.stderr)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1908:            "language": app.state.config.lang}  # STT hint only
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1946:"""PizzaSim API client: httpx, explicit timeouts, typed errors.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:1991:    """Base for typed API errors."""
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2003:    def __init__(self, details: list[str]):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2004:        super().__init__("; ".join(details))
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2005:        self.details = details
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2023:            details = response.json().get("details", [])
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2025:            details = []
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2026:        raise ValidationError(details or ["invalid request"])
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2028:        raise ServerError(f"server error ({response.status_code})")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2091:        return self._request("GET", "/location", params={"street": street})
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2133:        print(f"Configuration error: {exc}", file=sys.stderr)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2200:    lang: str  # PIZZERIA_LANG: greeting language = pizzeria country
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2204:        lang = require_env("PIZZERIA_LANG").lower()
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2207:                "PIZZERIA_LANG must be 'de' or 'en', got something else"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2305:                event({"type": "error", "error": str(exc)})
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2344:        event({"type": "error", "error": "tool loop guard exceeded"})
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2361:/bin/bash -lc "sed -n '1,320p' tests/test_state.py" in /home/rob/bpm-pizza-vibecoding-solution
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2363:/bin/bash -lc "sed -n '1,260p' tests/test_transcripts.py" in /home/rob/bpm-pizza-vibecoding-solution
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2365:/bin/bash -lc "sed -n '1,420p' tests/test_tools.py" in /home/rob/bpm-pizza-vibecoding-solution
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2380:- From then on, answer each turn in the language of the customer's latest
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2387:- Before submitting: call `read_back`, say it out loud, and wait for an
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2394:- On errors, explain in plain language what happened and what the customer
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2401:When a tool reports an error, follow it: offer the suggested alternatives
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2473:        return {"street": street, "deliverable": True}
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2488:    calls, error_codes = [], []
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2493:        if event["type"] == "tool_result" and "error" in event["result"]:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2494:            error_codes.append(event["result"]["error"]["code"])
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2504:    assert error_codes == expect["error_codes"]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2601:def test_extras_controlled_vocabulary(menu):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2602:    menu.validate_extras(["mushrooms", "pineapple"])  # ok
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2604:        menu.validate_extras(["unicorn_dust"])
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2608:# --- pizzasim client typed errors (httpx MockTransport) -------------------
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2619:def test_auth_error_mapped():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2631:def test_422_mapped_with_details():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2634:            respond(422, fixture("error_422.json"))
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2636:    assert "valid pizza code" in e.value.details[0]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2672:    """Scripted stand-in for PizzaSim in dispatch tests."""
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2690:        return {"street": street, "deliverable": True}
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2710:    tools.dispatch(order, menu, fake, "read_back", {})
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2721:    assert result["menu"]["toppings"]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2728:    assert snap["customer"] is None and snap["read_back_done"] is False
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2731:def test_unknown_item_error_shape(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2735:    err = result["error"]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2749:    assert result["error"]["code"] == "unknown_item"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2760:        assert result["error"]["code"] == "invalid_quantity", bad
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2767:                                        "extras": ["unicorn_dust"]}]})
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2768:    assert result["error"]["code"] == "invalid_extra"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2773:    result = tools.dispatch(order, menu, fake, "remove_item",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2777:    result = tools.dispatch(order, menu, fake, "remove_item",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2792:def test_submit_outside_confirmed_is_tool_error(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2796:    assert result["error"]["code"] == "invalid_state"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2802:    assert result["error"]["code"] == "invalid_state"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2803:    assert result["error"]["message"] == "What can I get you?"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2810:    assert result["error"]["code"] == "submit_unknown"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2828:    assert result["error"]["code"] == "submit_unknown"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2832:                    "ready_at": 0, "status": "delivered"}]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2845:    assert result["error"]["code"] == "submit_unknown"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2854:    assert result["error"]["code"] == "submit_failed"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2855:    assert "valid pizza code" in result["error"]["message"]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2859:def test_auth_error_no_retry(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2863:    assert result["error"]["code"] == "api_unavailable"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2874:    tools.dispatch(order, menu, fake, "read_back", {})
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2895:    assert result["deliverable"] is True and "snapshot" in result
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2911:        ("read_back", {}),
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2914:        assert "error" not in result, result
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2917:    assert "error" not in result
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2931:def item(code="margherita", type_="pizza", qty=1, extras=None):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2933:                extras=extras or [])
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2946:    state.read_back(o)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2969:    state.read_back(o)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2991:    lambda o: state.remove_item(o, "pizza", "margherita", None),
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:2993:    lambda o: state.read_back(o),
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3006:        state.remove_item(order_in(State.EMPTY), "pizza", "margherita", None)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3010:def test_read_back_empty():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3012:        state.read_back(order_in(State.EMPTY))
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3016:def test_read_back_collecting_needs_customer():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3018:        state.read_back(order_in(State.COLLECTING))
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3049:        state.remove_item(o, "pasta", "pesto", None)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3063:    state.remove_item(o, "pizza", "margherita", None)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3083:def test_confirm_without_read_back():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3087:    assert e.value.code == "read_back_required"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3092:    state.read_back(o)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3100:def test_read_back_of_old_revision_does_not_allow_confirm():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3102:    state.read_back(o)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3106:    assert e.value.code == "read_back_required"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3116:    state.remove_item(o, "pizza", "margherita", None)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3127:def test_same_code_different_extras_is_separate_line():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3130:    state.add_items(o, [item(qty=1, extras=["mushrooms"])])
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3137:    state.remove_item(o, "pizza", "margherita", 1)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3139:    state.remove_item(o, "pizza", "margherita", 5)  # >= qty removes line
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3146:    state.remove_item(o, "pizza", "margherita", None)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3156:    state.remove_item(o, "pasta", "tonno", None)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3187:- Vor dem Abschicken: rufe `read_back` auf, lies die Bestellung vor und
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3250:  const details = document.createElement("details");
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3251:  details.className = "steps";
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3252:  details.innerHTML = "<summary>Zwischenschritte</summary>";
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3253:  chat.appendChild(details);
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3254:  return details;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3290:        } else if (ev.type === "error") {
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3370:    if (speechEnabled) {           // unset SPEECH_URL → not rendered at all
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3426:details.steps { font-size: .78rem; color: #666; margin: .2rem 0 .6rem; }
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3427:details.steps summary { cursor: pointer; user-select: none; }
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3428:details.steps pre { white-space: pre-wrap; word-break: break-all;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3461:# Greeting language of the pizzeria's country: de or en
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3462:PIZZERIA_LANG=
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3465:SPEECH_URL=
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3466:SPEECH_STT_MODEL=
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3467:SPEECH_TTS_MODEL=
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3468:SPEECH_TTS_VOICE=
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3474:machine owned by the code; the model only turns customer language into tool
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3486:`.env.example` except the four `SPEECH_*` ones is required. The process
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3497:The agent greets first, in the language set by `PIZZERIA_LANG`, and answers
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3498:each turn in the language you used (German or English). End with Ctrl-D.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3513:Set `SPEECH_URL`, `SPEECH_STT_MODEL`, `SPEECH_TTS_MODEL` and
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3514:`SPEECH_TTS_VOICE` to a self-hosted OpenAI-compatible speech service. The
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3517:`SPEECH_URL` unset — or the service down at startup — mic and toggle are
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3522:question; and one run with `SPEECH_URL` unset placing an order as text.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3527:venv/bin/python -m pytest tests/            # deterministic: no network, no LLM
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3528:PIZZA_LIVE_TEST=1 venv/bin/python -m pytest tests/test_tools.py -k live
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3546:  `{SPEECH_URL}/v1/audio/transcriptions` with `SPEECH_STT_MODEL` and
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3547:  `PIZZERIA_LANG` as the language hint (an STT hint only — it never
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3548:  influences assistant output language) → `{text}`. `POST /speech/tts` body `{text}` forwarded to
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3549:  `{SPEECH_URL}/v1/audio/speech` with `SPEECH_TTS_MODEL` +
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3550:  `SPEECH_TTS_VOICE` → audio bytes. Proxying keeps the speech URL and
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3567:| 422 validation | typed `ValidationError(details)` → tool error `submit_failed` with field text, basket kept |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3594:  question, `SPEECH_URL` unset run).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3601:   ☐ `.env.example` lists all 12 vars (incl. `PIZZERIA_LANG`), names only
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3604:2. **Order + state machine + tests.** `core/order.py`, `core/state.py`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3605:   `tests/test_state.py`.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3610:   extras vocabulary ☐ ≤3 candidates.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3611:4. **PizzaSim client.** `core/pizzasim.py`, typed errors, timeouts,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3612:   fixtures for orders/422/location, httpx MockTransport tests.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3613:   ☐ every error class mapped ☐ no call without timeout ☐ submit returns
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3615:5. **Tools.** `core/tools.py` schemas + dispatch, `tests/test_tools.py`.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3616:   ☐ schemas match this plan exactly ☐ atomic add ☐ error shape uniform
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3629:   only ☐ `SPEECH_URL` unset → no mic, no speaker, text works ☐ speech
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3631:10. **Harden + docs.** Walk the SPEC error table end to end, README
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3633:    ☐ each error row demonstrably handled ☐ README covers all channels +
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3634:    speech + tests ☐ full suite green.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3636:Each ticket ≤ 1h, tests live in the ticket that introduces the behaviour.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3641:/bin/bash -lc 'PYTHONDONTWRITEBYTECODE=1 pytest tests/ -q' in /home/rob/bpm-pizza-vibecoding-solution
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3678:    self.hook.pytest_load_initial_conftests(
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3695:  File "/home/rob/.local/lib/python3.13/site-packages/_pytest/warnings.py", line 128, in pytest_load_initial_conftests
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3701:  File "/home/rob/.local/lib/python3.13/site-packages/_pytest/capture.py", line 170, in pytest_load_initial_conftests
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3740:/bin/bash -lc "nl -ba tests/test_state.py | sed -n '195,235p'" in /home/rob/bpm-pizza-vibecoding-solution
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3765:    17	`uvicorn` (web channel), `pytest` (tests), stdlib `difflib` (candidate
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3775:    27	- Secrets never appear in logs, transcripts, errors, or the web UI.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3779:    31	- No build-time model name anywhere in source, config, prompts, tests, docs.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3783:    35	- Deterministic tests: no network, no LLM (one opt-in live smoke test).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3791:   195	    state.remove_item(o, "pizza", "margherita", None)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3802:   206	def test_same_code_different_extras_is_separate_line():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3805:   209	    state.add_items(o, [item(qty=1, extras=["mushrooms"])])
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3812:   216	    state.remove_item(o, "pizza", "margherita", 1)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3814:   218	    state.remove_item(o, "pizza", "margherita", 5)  # >= qty removes line
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3821:   225	    state.remove_item(o, "pizza", "margherita", None)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3831:   235	    state.remove_item(o, "pasta", "tonno", None)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3859:    52	def remove_item(order: Order, type_: str, code: str, qty: int | None) -> None:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3882:    75	def read_back(order: Order) -> None:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3893:    86	    order.read_back_revision = order.revision
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3913:   106	    if order.read_back_revision != order.revision:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3915:   108	            "read_back_required",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3927:    34	    enabled only if SPEECH_URL is set, answers, and models are configured."""
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3930:    37	        self.url = optional_env("SPEECH_URL")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3931:    38	        self.stt_model = optional_env("SPEECH_STT_MODEL")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3932:    39	        self.tts_model = optional_env("SPEECH_TTS_MODEL")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3933:    40	        self.voice = optional_env("SPEECH_TTS_VOICE")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3957:   222	  language of the customer's latest message (German or English), unprompted.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3958:   223	  Language mirroring is model behaviour; the runtime never detects language.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3965:   230	  the plain apology from the error table. Gateway 4xx/5xx: no retry, abort
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3968:   233	  `tool_result`, `state`, `error` — the CLI prints them (verbose), the web
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3976:   241	`prompts/system.de.md` / `system.en.md`, same content in two languages, calm
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3978:   243	greet once in the file's language and offer help in one sentence; mirror the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3979:   244	customer's language per turn (German ↔ English); one question per turn; menu
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3981:   246	came from speech) and street, street declinable; read back via `read_back`
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3984:   249	state order id in speakable groups and ETA in minutes; errors in plain
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3985:   250	language, never codes or JSON; never claim the address was checked for
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:3994:    71	               list, 422 bodies, location).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:4005:    82	Deviation from the SPEC tree, documented: `tests/test_transcripts.py` and
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:4015:    92	| `core/agent.py` | `LITELLM_PIZZA_URL`, `LITELLM_PIZZA_KEY`, `LITELLM_PIZZA_MODEL_1`, `PIZZERIA_LANG` (all required; `LITELLM_PIZZA_MODEL_2` read but unused — single-model build) |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:4017:    94	| `channels/web.py` | `SPEECH_URL`, `SPEECH_STT_MODEL`, `SPEECH_TTS_MODEL`, `SPEECH_TTS_VOICE` (all optional; absence disables speech) |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:4019:    96	`PIZZERIA_LANG` ∈ {`de`, `en`} is the pizzeria-country greeting language.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:4023:   100	`decisions/qa.md`). It selects the system prompt file and the STT language
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:4024:   101	hint; it never overrides per-turn language mirroring.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:4041:error_handling: 4
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:4047:- `core/state.py:52-66` removes the first line matching `(type, code)` and ignores `extras`. That becomes wrong as soon as the basket contains the same item code with different extras, which the code explicitly supports in [tests/test_state.py](/home/rob/bpm-pizza-vibecoding-solution/tests/test_state.py:206). Make removal address a full line identity or otherwise eliminate that ambiguity, and add a test for it.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:4058:error_handling: 4
/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:4064:- `core/state.py:52-66` removes the first line matching `(type, code)` and ignores `extras`. That becomes wrong as soon as the basket contains the same item code with different extras, which the code explicitly supports in [tests/test_state.py](/home/rob/bpm-pizza-vibecoding-solution/tests/test_state.py:206). Make removal address a full line identity or otherwise eliminate that ambiguity, and add a test for it.
/home/rob/bpm-pizza-vibecoding-solution/initial_prompt.md:6:3. Every deliverable listed in SPEC.md exists; you showed the tree.
/home/rob/bpm-pizza-vibecoding-solution/initial_prompt.md:9:6. With SPEECH_URL unset, the web channel starts and places an order; you showed it.
/home/rob/bpm-pizza-vibecoding-solution/initial_prompt.md:24:- The models this build runs on have nothing to do with the models the product calls. Never wire the agent to your own model, and never copy a build-time model name into source, config, prompts, tests or docs.
/home/rob/bpm-pizza-vibecoding-solution/tests/test_transcripts.py:75:        return {"street": street, "deliverable": True}
/home/rob/bpm-pizza-vibecoding-solution/tests/test_transcripts.py:90:    calls, error_codes = [], []
/home/rob/bpm-pizza-vibecoding-solution/tests/test_transcripts.py:95:        if event["type"] == "tool_result" and "error" in event["result"]:
/home/rob/bpm-pizza-vibecoding-solution/tests/test_transcripts.py:96:            error_codes.append(event["result"]["error"]["code"])
/home/rob/bpm-pizza-vibecoding-solution/tests/test_transcripts.py:106:    assert error_codes == expect["error_codes"]
/home/rob/bpm-pizza-vibecoding-solution/channels/web.py:4:proxies the optional self-hosted speech service (STT/TTS). If SPEECH_URL is
/home/rob/bpm-pizza-vibecoding-solution/channels/web.py:34:    enabled only if SPEECH_URL is set, answers, and models are configured."""
/home/rob/bpm-pizza-vibecoding-solution/channels/web.py:37:        self.url = optional_env("SPEECH_URL")
/home/rob/bpm-pizza-vibecoding-solution/channels/web.py:38:        self.stt_model = optional_env("SPEECH_STT_MODEL")
/home/rob/bpm-pizza-vibecoding-solution/channels/web.py:39:        self.tts_model = optional_env("SPEECH_TTS_MODEL")
/home/rob/bpm-pizza-vibecoding-solution/channels/web.py:40:        self.voice = optional_env("SPEECH_TTS_VOICE")
/home/rob/bpm-pizza-vibecoding-solution/channels/web.py:58:        print(f"Configuration error: {exc}", file=sys.stderr)
/home/rob/bpm-pizza-vibecoding-solution/channels/web.py:148:            "language": app.state.config.lang}  # STT hint only
/home/rob/bpm-pizza-vibecoding-solution/README.md:4:machine owned by the code; the model only turns customer language into tool
/home/rob/bpm-pizza-vibecoding-solution/README.md:16:`.env.example` except the four `SPEECH_*` ones is required. The process
/home/rob/bpm-pizza-vibecoding-solution/README.md:27:The agent greets first, in the language set by `PIZZERIA_LANG`, and answers
/home/rob/bpm-pizza-vibecoding-solution/README.md:28:each turn in the language you used (German or English). End with Ctrl-D.
/home/rob/bpm-pizza-vibecoding-solution/README.md:43:Set `SPEECH_URL`, `SPEECH_STT_MODEL`, `SPEECH_TTS_MODEL` and
/home/rob/bpm-pizza-vibecoding-solution/README.md:44:`SPEECH_TTS_VOICE` to a self-hosted OpenAI-compatible speech service. The
/home/rob/bpm-pizza-vibecoding-solution/README.md:47:`SPEECH_URL` unset — or the service down at startup — mic and toggle are
/home/rob/bpm-pizza-vibecoding-solution/README.md:52:question; and one run with `SPEECH_URL` unset placing an order as text.
/home/rob/bpm-pizza-vibecoding-solution/README.md:57:venv/bin/python -m pytest tests/            # deterministic: no network, no LLM
/home/rob/bpm-pizza-vibecoding-solution/README.md:58:PIZZA_LIVE_TEST=1 venv/bin/python -m pytest tests/test_tools.py -k live
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:64:def test_extras_controlled_vocabulary(menu):
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:65:    menu.validate_extras(["mushrooms", "pineapple"])  # ok
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:67:        menu.validate_extras(["unicorn_dust"])
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:71:# --- pizzasim client typed errors (httpx MockTransport) -------------------
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:82:def test_auth_error_mapped():
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:94:def test_422_mapped_with_details():
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:97:            respond(422, fixture("error_422.json"))
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:99:    assert "valid pizza code" in e.value.details[0]
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:135:    """Scripted stand-in for PizzaSim in dispatch tests."""
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:142:        self.order_details = {}  # id -> detail payload
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:156:        if order_id not in self.order_details:
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:158:        return self.order_details[order_id]
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:161:        return {"street": street, "deliverable": True}
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:181:    tools.dispatch(order, menu, fake, "read_back", {})
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:192:    assert result["menu"]["toppings"]
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:199:    assert snap["customer"] is None and snap["read_back_done"] is False
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:202:def test_unknown_item_error_shape(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:206:    err = result["error"]
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:220:    assert result["error"]["code"] == "unknown_item"
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:231:        assert result["error"]["code"] == "invalid_quantity", bad
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:238:                                        "extras": ["unicorn_dust"]}]})
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:239:    assert result["error"]["code"] == "invalid_extra"
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:244:    result = tools.dispatch(order, menu, fake, "remove_item",
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:248:    result = tools.dispatch(order, menu, fake, "remove_item",
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:263:def test_submit_outside_confirmed_is_tool_error(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:267:    assert result["error"]["code"] == "invalid_state"
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:273:    assert result["error"]["code"] == "invalid_state"
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:274:    assert result["error"]["message"] == "What can I get you?"
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:281:    assert result["error"]["code"] == "submit_unknown"
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:289:    fake.order_details["recovered-1"] = {
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:293:                   "extras": []}],
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:311:    fake.order_details["other-1"] = {
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:314:                   "extras": []}],
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:336:    tools.dispatch(order, menu, fake, "read_back", {})
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:354:    assert result["error"]["code"] == "submit_unknown"
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:358:                    "ready_at": 0, "status": "delivered"}]
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:371:    assert result["error"]["code"] == "submit_unknown"
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:380:    assert result["error"]["code"] == "submit_failed"
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:381:    assert "valid pizza code" in result["error"]["message"]
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:385:def test_auth_error_no_retry(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:389:    assert result["error"]["code"] == "api_unavailable"
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:400:    tools.dispatch(order, menu, fake, "read_back", {})
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:421:    assert result["deliverable"] is True and "snapshot" in result
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:441:        ("read_back", {}),
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:444:        assert "error" not in result, result
/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:447:    assert "error" not in result, result
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:6:> repo — code, tests, prompts, tickets — derives from it.
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:51:**Core belief:** a language model is a great waiter and a terrible order pad.
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:63:  tool error carrying candidate matches — never a silent guess, never a fallback
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:90:   dashboard for that pizzeria.
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:125:- **Languages:** German and English. The agent answers in the language the
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:129:- **The success moment:** the order appears in the PizzaSim dashboard under the
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:131:- **Deterministic tests** that run with no network and no LLM.
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:169:- Secrets never appear in logs, transcripts, error messages or the web UI.
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:180:| `GET /location?street=…` | public | street plausibility check |
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:187:  "items": [{ "type": "pizza", "code": "margherita", "qty": 2, "extras": [] }]
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:210:`GET /pizzerias/{id}/orders/{order_id}`, `GET /location`). Facts below are
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:220:   `customer_id`, `created_at`, `ready_at`, `status`, `delivered_at`,
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:229:   there are no per-language names in the API; read-back uses `name` as-is in
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:230:   both languages. The menu response also carries a top-level `toppings[]`
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:232:4. **`extras[]` is a controlled vocabulary:** the top-level `toppings[]` from
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:234:   rejects unknown extras with `422` (`"items[0].extras contains invalid
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:235:   topping 'unicorn_dust'"`), so the tool layer validates extras against
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:236:   `toppings[]` exactly like item codes.
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:238:   `{"error": "<code>", "details": ["<human sentence>", ...]}` — e.g.
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:239:   `{"error": "validation_failed", "details": ["items[0].code must be a valid
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:240:   pizza code"]}` with HTTP 422. The tool layer maps `error` to typed errors
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:241:   and may surface `details` to targeted questions.
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:243:   `prepared_planned` → `delivered` (with `delivered_at` set on the last).
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:245:7. **`GET /location?street=` returns** `{"street": "<echo>",
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:246:   "deliverable": <bool>}` with HTTP 200. In probing, even a nonsense street
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:247:   returned `deliverable: true` — the check is a weak plausibility signal at
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:263:                                                    │ read_back + customer says yes
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:270:Invariants, all enforced in code and all covered by unit tests:
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:272:1. `submit_order` outside `CONFIRMED` returns an error. It does not "helpfully"
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:277:   legal after `read_back` has been called for the current basket revision. The
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:291:| `get_menu` | — | pizzas and pasta with codes and display names in both languages |
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:292:| `add_items` | `items[]` of `{type, code, qty, extras[]}` | new basket + revision |
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:293:| `remove_item` | `code`, `type`, optional `qty` | new basket + revision |
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:295:| `read_back` | — | basket, customer, revision — the text the agent must read out |
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:296:| `confirm_order` | `revision` | state `CONFIRMED`, or error if stale |
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:304:- Failure: `{"error": {"code": "...", "message": "...", "candidates": [...]}}`.
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:318:- Greet first, in the language of the pizzeria's country, and offer help — one
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:324:- Before submitting: call `read_back`, say it, and wait for an explicit yes.
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:330:- On error, explain in plain language what happened and what the customer's
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:344:| STT | `POST {SPEECH_URL}/v1/audio/transcriptions` | multipart audio file + model + language |
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:345:| TTS | `POST {SPEECH_URL}/v1/audio/speech` | JSON with model, voice, input text; returns audio |
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:355:  model, TTS model, voice and language all come from the environment, exactly
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:360:  | `SPEECH_URL` | base URL of the self-hosted speech service |
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:361:  | `SPEECH_STT_MODEL` | transcription model id |
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:362:  | `SPEECH_TTS_MODEL` | synthesis model id |
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:363:  | `SPEECH_TTS_VOICE` | voice id |
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:374:- **Speech is never required.** If `SPEECH_URL` is unset or the service does not
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:380:- **Confirm the name.** Transcription errors on names are the expensive failure:
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:446:  menu question — plus one run with `SPEECH_URL` unset, which must render a
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:473:  **none of this spec's business**. Nothing in the deliverables reads them,
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:482:  source, config, prompts, tests or documentation.
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:495:  wrong assumptions, missing error cases — and *judge*, scoring against the fixed
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:510:error_handling: N
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:531:   loop, error handling, conversation state. **No code.** Send it to the reviewer
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:548:1. **Core.** Order model, state machine, tool layer, tests. No LLM, no network.
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:549:   Pass when the unit tests are green.
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:551:3. **CLI.** Full conversation, real API, an order visible in the dashboard.
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:554:6. **Harden.** Walk the error table, force each case, fix what breaks.
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:574:│   ├── pizzasim.py          ← API client, typed errors, timeouts
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:584:├── tests/
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:595:## Decisions locked
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:610:| Errors | Typed in code, plain language to the customer |
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:619:- Extras and modifiers beyond a passthrough `extras[]`.
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:623:- Additional languages beyond DE + EN.
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:632:  or by "schema / implementation / tests".
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:17:`uvicorn` (web channel), `pytest` (tests), stdlib `difflib` (candidate
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:27:- Secrets never appear in logs, transcripts, errors, or the web UI.
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:31:- No build-time model name anywhere in source, config, prompts, tests, docs.
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:35:- Deterministic tests: no network, no LLM (one opt-in live smoke test).
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:46:  menu.py      Immutable Menu snapshot (pizzas, pasta, toppings), one per
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:47:               session; (type, code) validation; extras validation;
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:50:               submit_order, check_street; typed errors; timeouts;
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:54:               {"error": {code, message, candidates}}.
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:67:  system.de.md German system prompt (default deployment language).
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:69:tests/
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:71:               list, 422 bodies, location).
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:82:Deviation from the SPEC tree, documented: `tests/test_transcripts.py` and
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:92:| `core/agent.py` | `LITELLM_PIZZA_URL`, `LITELLM_PIZZA_KEY`, `LITELLM_PIZZA_MODEL_1`, `PIZZERIA_LANG` (all required; `LITELLM_PIZZA_MODEL_2` read but unused — single-model build) |
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:94:| `channels/web.py` | `SPEECH_URL`, `SPEECH_STT_MODEL`, `SPEECH_TTS_MODEL`, `SPEECH_TTS_VOICE` (all optional; absence disables speech) |
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:96:`PIZZERIA_LANG` ∈ {`de`, `en`} is the pizzeria-country greeting language.
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:100:`decisions/qa.md`). It selects the system prompt file and the STT language
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:101:hint; it never overrides per-turn language mirroring.
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:114:   404-pizzeria case from the error table → process refuses to start;
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:132:Order fields: `items: list[Item(type, code, qty, extras)]`,
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:134:(increments on every basket or customer mutation), `read_back_revision:
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:135:int | None` (set by `read_back`), `state`, `submit_attempted_at: int | None`
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:149:Transition table (✓ legal, ✗ → typed error):
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:154:| remove_item | ✗ empty_basket | ✓ | ✓ | ✓ demote | ✗ order_closed |
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:156:| read_back | ✗ empty_basket | ✗ invalid_state (no customer yet) | ✓ | ✓ (same basket, idempotent) | ✗ order_closed |
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:162:(else `stale_revision`) and `read_back_revision == order.revision` (else
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:163:`read_back_required`). So the only path into `CONFIRMED` is: state `READY`,
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:164:`read_back` called at the current revision, then `confirm_order` naming that
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:177:exactly one real retry. List or detail call fails → error `submit_unknown`
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:189:`{state, revision, items: [{type, code, name, qty, extras}], customer:
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:190:{first_name, street_one} | null, read_back_done: bool}` — never a diff.
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:194:| `get_menu` | `{}` | `{"menu": {"pizzas": [{code, name}], "pasta": [{code, name}], "toppings": [str]}, "snapshot": SNAPSHOT}` — `name` is the API's single display name, which the verified contract facts show serves both languages |
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:195:| `add_items` | `{items: [{type: enum[pizza,pasta], code: str, qty: int ≥1, extras: [str]}]}` (required: items; extras default `[]`) | `{"snapshot": SNAPSHOT}` (basket + revision live in SNAPSHOT) |
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:196:| `remove_item` | `{type: enum, code: str, qty: int ≥1 optional}` — the spec fixes these params, so when several lines share (type, code) with different extras: absent qty removes **all** matching lines, qty reduces the **most recently added** matching line (deterministic; the snapshot lets the model repair by remove + re-add) | `{"snapshot": SNAPSHOT}` |
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:198:| `read_back` | `{}` | `{"snapshot": SNAPSHOT}` — basket, customer, revision: the material the agent reads out |
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:199:| `confirm_order` | `{revision: int}` | `{"snapshot": SNAPSHOT}` with `state == "CONFIRMED"`, or error if stale |
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:201:| `check_street` | `{street: str}` | `{"street": str, "deliverable": bool, "snapshot": SNAPSHOT}` — the never-claim-verified rule lives in the prompt, not the tool |
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:203:Failure shape: `{"error": {"code": "<one of the codes below>", "message":
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:207:candidate toppings), `invalid_quantity` (non-integer or < 1 — the tool does
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:209:`read_back_required`, `order_closed`, `submit_failed`, `submit_unknown`,
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:210:`api_unavailable`, `not_in_basket` (remove_item for a line that isn't there).
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:213:snapshot and every extra against `toppings[]`; any failure rejects the whole
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:214:call atomically (no partial adds), returning the first error with candidates
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:223:  `lang = PIZZERIA_LANG` — the pizzeria-country greeting language, a
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:226:  language of the customer's latest message (German or English), unprompted.
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:227:  Language mirroring is model behaviour; the runtime never detects language.
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:234:  the plain apology from the error table. Gateway 4xx/5xx: no retry, abort
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:237:  `tool_result`, `state`, `error` — the CLI prints them (verbose), the web
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:245:`prompts/system.de.md` / `system.en.md`, same content in two languages, calm
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:247:greet once in the file's language and offer help in one sentence; mirror the
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:248:customer's language per turn (German ↔ English); one question per turn; menu
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:250:came from speech) and street, street declinable; read back via `read_back`
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:253:state order id in speakable groups and ETA in minutes; errors in plain
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:254:language, never codes or JSON; never claim the address was checked for
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:261:  (`speech` true only if `SPEECH_URL` set and a probe succeeded at startup;
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:263:  see which pizzeria they are ordering at). No language field: language is
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:264:  never a UI control — the greeting comes from `PIZZERIA_LANG`, mirroring
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:271:  `{SPEECH_URL}/v1/audio/transcriptions` with `SPEECH_STT_MODEL` and
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:272:  `PIZZERIA_LANG` as the language hint (an STT hint only — it never
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:273:  influences assistant output language) → `{text}`. `POST /speech/tts` body `{text}` forwarded to
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:274:  `{SPEECH_URL}/v1/audio/speech` with `SPEECH_TTS_MODEL` +
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:275:  `SPEECH_TTS_VOICE` → audio bytes. Proxying keeps the speech URL and
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:292:| 422 validation | typed `ValidationError(details)` → tool error `submit_failed` with field text, basket kept |
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:323:  question, `SPEECH_URL` unset run).
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:330:   ☐ `.env.example` lists all 12 vars (incl. `PIZZERIA_LANG`), names only
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:333:2. **Order + state machine + tests.** `core/order.py`, `core/state.py`,
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:334:   `tests/test_state.py`.
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:339:   extras vocabulary ☐ ≤3 candidates.
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:340:4. **PizzaSim client.** `core/pizzasim.py`, typed errors, timeouts,
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:341:   fixtures for orders/422/location, httpx MockTransport tests.
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:342:   ☐ every error class mapped ☐ no call without timeout ☐ submit returns
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:344:5. **Tools.** `core/tools.py` schemas + dispatch, `tests/test_tools.py`.
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:345:   ☐ schemas match this plan exactly ☐ atomic add ☐ error shape uniform
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:358:   only ☐ `SPEECH_URL` unset → no mic, no speaker, text works ☐ speech
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:360:10. **Harden + docs.** Walk the SPEC error table end to end, README
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:362:    ☐ each error row demonstrably handled ☐ README covers all channels +
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:363:    speech + tests ☐ full suite green.
/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:365:Each ticket ≤ 1h, tests live in the ticket that introduces the behaviour.
/home/rob/bpm-pizza-vibecoding-solution/core/pizzasim.py:1:"""PizzaSim API client: httpx, explicit timeouts, typed errors.
/home/rob/bpm-pizza-vibecoding-solution/core/pizzasim.py:46:    """Base for typed API errors."""
/home/rob/bpm-pizza-vibecoding-solution/core/pizzasim.py:58:    def __init__(self, details: list[str]):
/home/rob/bpm-pizza-vibecoding-solution/core/pizzasim.py:59:        super().__init__("; ".join(details))
/home/rob/bpm-pizza-vibecoding-solution/core/pizzasim.py:60:        self.details = details
/home/rob/bpm-pizza-vibecoding-solution/core/pizzasim.py:78:            details = response.json().get("details", [])
/home/rob/bpm-pizza-vibecoding-solution/core/pizzasim.py:80:            details = []
/home/rob/bpm-pizza-vibecoding-solution/core/pizzasim.py:81:        raise ValidationError(details or ["invalid request"])
/home/rob/bpm-pizza-vibecoding-solution/core/pizzasim.py:83:        raise ServerError(f"server error ({response.status_code})")
/home/rob/bpm-pizza-vibecoding-solution/core/pizzasim.py:153:        return self._request("GET", "/location", params={"street": street})
/home/rob/bpm-pizza-vibecoding-solution/core/agent.py:40:    lang: str  # PIZZERIA_LANG: greeting language = pizzeria country
/home/rob/bpm-pizza-vibecoding-solution/core/agent.py:44:        lang = require_env("PIZZERIA_LANG").lower()
/home/rob/bpm-pizza-vibecoding-solution/core/agent.py:47:                "PIZZERIA_LANG must be 'de' or 'en', got something else"
/home/rob/bpm-pizza-vibecoding-solution/core/agent.py:145:                event({"type": "error", "error": str(exc)})
/home/rob/bpm-pizza-vibecoding-solution/core/agent.py:185:        event({"type": "error", "error": "tool loop guard exceeded"})
/home/rob/bpm-pizza-vibecoding-solution/core/menu.py:1:"""Immutable menu snapshot: (type, code) validation, extras validation,
/home/rob/bpm-pizza-vibecoding-solution/core/menu.py:22:        self.toppings: list[str] = list(payload.get("toppings", []))
/home/rob/bpm-pizza-vibecoding-solution/core/menu.py:30:            "toppings": self.toppings,
/home/rob/bpm-pizza-vibecoding-solution/core/menu.py:59:    def validate_extras(self, extras: list[str]) -> None:
/home/rob/bpm-pizza-vibecoding-solution/core/menu.py:60:        for extra in extras:
/home/rob/bpm-pizza-vibecoding-solution/core/menu.py:61:            if extra not in self.toppings:
/home/rob/bpm-pizza-vibecoding-solution/core/menu.py:65:                        extra.lower(), self.toppings, n=3, cutoff=0.5
/home/rob/bpm-pizza-vibecoding-solution/tests/fixtures/menu.json:1:{"toppings":["mozzarella","mushrooms","smoked_ham","salami","onions","garlic","pepperoni","pineapple","artichokes","basil","bell_pepper","tuna"],"pizzas":[{"code":"margherita","name":"Margherita","base":["dough","tomatoes","mozzarella","basil"],"price":8.5},{"code":"prosciutto","name":"Prosciutto","base":["dough","tomatoes","mozzarella","smoked_ham"],"price":9.5},{"code":"salami","name":"Salami","base":["dough","tomatoes","mozzarella","salami"],"price":9.5},{"code":"funghi","name":"Funghi","base":["dough","tomatoes","mozzarella","mushrooms"],"price":9},{"code":"regina","name":"Regina","base":["dough","tomatoes","mozzarella","smoked_ham","mushrooms"],"price":10.5},{"code":"mista","name":"Mista","base":["dough","tomatoes","mozzarella","salami","smoked_ham","mushrooms"],"price":11.5},{"code":"hawaii","name":"Hawaii","base":["dough","tomatoes","mozzarella","smoked_ham","pineapple"],"price":10},{"code":"tonno","name":"Tonno","base":["dough","tomatoes","mozzarella","tuna","onions"],"price":10.5},{"code":"papa","name":"Papa","base":["dough","tomatoes","mozzarella","tuna","onions","garlic"],"price":11},{"code":"diavolo","name":"Diavolo","base":["dough","tomatoes","mozzarella","salami","bell_pepper","pepperoni"],"price":11},{"code":"grandiosa","name":"Grandiosa","base":["dough","tomatoes","mozzarella","smoked_ham","salami","mushrooms","bell_pepper","artichokes","onions"],"price":13.5}],"pasta":[{"code":"aglioolio","name":"Pasta Aglio & Olio","base":["pasta","garlic","basil"],"price":9},{"code":"tonno","name":"Pasta Tonno","base":["pasta","tuna"],"price":8.5},{"code":"funghi","name":"Pasta Funghi","base":["pasta","mushrooms"],"price":8.5},{"code":"pesto","name":"Pasta Pesto","base":["pasta","pesto"],"price":8.5}]}
/home/rob/bpm-pizza-vibecoding-solution/tests/test_state.py:10:def item(code="margherita", type_="pizza", qty=1, extras=None):
/home/rob/bpm-pizza-vibecoding-solution/tests/test_state.py:12:                extras=extras or [])
/home/rob/bpm-pizza-vibecoding-solution/tests/test_state.py:25:    state.read_back(o)
/home/rob/bpm-pizza-vibecoding-solution/tests/test_state.py:48:    state.read_back(o)
/home/rob/bpm-pizza-vibecoding-solution/tests/test_state.py:70:    lambda o: state.remove_item(o, "pizza", "margherita", None),
/home/rob/bpm-pizza-vibecoding-solution/tests/test_state.py:72:    lambda o: state.read_back(o),
/home/rob/bpm-pizza-vibecoding-solution/tests/test_state.py:85:        state.remove_item(order_in(State.EMPTY), "pizza", "margherita", None)
/home/rob/bpm-pizza-vibecoding-solution/tests/test_state.py:89:def test_read_back_empty():
/home/rob/bpm-pizza-vibecoding-solution/tests/test_state.py:91:        state.read_back(order_in(State.EMPTY))
/home/rob/bpm-pizza-vibecoding-solution/tests/test_state.py:95:def test_read_back_collecting_needs_customer():
/home/rob/bpm-pizza-vibecoding-solution/tests/test_state.py:97:        state.read_back(order_in(State.COLLECTING))
/home/rob/bpm-pizza-vibecoding-solution/tests/test_state.py:128:        state.remove_item(o, "pasta", "pesto", None)
/home/rob/bpm-pizza-vibecoding-solution/tests/test_state.py:142:    state.remove_item(o, "pizza", "margherita", None)
/home/rob/bpm-pizza-vibecoding-solution/tests/test_state.py:162:def test_confirm_without_read_back():
/home/rob/bpm-pizza-vibecoding-solution/tests/test_state.py:166:    assert e.value.code == "read_back_required"
/home/rob/bpm-pizza-vibecoding-solution/tests/test_state.py:171:    state.read_back(o)
/home/rob/bpm-pizza-vibecoding-solution/tests/test_state.py:179:def test_read_back_of_old_revision_does_not_allow_confirm():
/home/rob/bpm-pizza-vibecoding-solution/tests/test_state.py:181:    state.read_back(o)
/home/rob/bpm-pizza-vibecoding-solution/tests/test_state.py:185:    assert e.value.code == "read_back_required"
/home/rob/bpm-pizza-vibecoding-solution/tests/test_state.py:195:    state.remove_item(o, "pizza", "margherita", None)
/home/rob/bpm-pizza-vibecoding-solution/tests/test_state.py:206:def test_same_code_different_extras_is_separate_line():
/home/rob/bpm-pizza-vibecoding-solution/tests/test_state.py:209:    state.add_items(o, [item(qty=1, extras=["mushrooms"])])
/home/rob/bpm-pizza-vibecoding-solution/tests/test_state.py:216:    state.remove_item(o, "pizza", "margherita", 1)
/home/rob/bpm-pizza-vibecoding-solution/tests/test_state.py:218:    state.remove_item(o, "pizza", "margherita", 5)  # >= qty removes line
/home/rob/bpm-pizza-vibecoding-solution/tests/test_state.py:225:    state.remove_item(o, "pizza", "margherita", None)
/home/rob/bpm-pizza-vibecoding-solution/tests/test_state.py:235:    state.remove_item(o, "pasta", "tonno", None)
/home/rob/bpm-pizza-vibecoding-solution/tests/test_state.py:240:    """Same (type, code), different extras: no-qty removal takes them all."""
/home/rob/bpm-pizza-vibecoding-solution/tests/test_state.py:242:    state.add_items(o, [item(qty=1), item(qty=1, extras=["mushrooms"])])
/home/rob/bpm-pizza-vibecoding-solution/tests/test_state.py:243:    state.remove_item(o, "pizza", "margherita", None)
/home/rob/bpm-pizza-vibecoding-solution/tests/test_state.py:249:    state.add_items(o, [item(qty=2), item(qty=2, extras=["mushrooms"])])
/home/rob/bpm-pizza-vibecoding-solution/tests/test_state.py:250:    state.remove_item(o, "pizza", "margherita", 1)
/home/rob/bpm-pizza-vibecoding-solution/tests/test_state.py:251:    assert [(i.extras, i.qty) for i in o.items] == \
/home/rob/bpm-pizza-vibecoding-solution/reviews/round11-spec-v3-analysis.md:16:- SPEC.md — version 3, just delivered by the operator (uncommitted working-tree version; read the file, not git).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round11-spec-v3-analysis.md:19:- Context you may trust: the repo implements v1 fully (approved, see reviews/scores.md); contract facts in v2's committed SPEC were verified against the live API, including: menu items carry {code,name,base[],price}; extras[] is the controlled toppings[] vocabulary with server 422 on unknowns; error bodies are {"error","details[]"}; statuses ordered->prepared_planned->delivered; /location returns {street,deliverable} and returned deliverable:true even for nonsense; there IS a detail endpoint GET /pizzerias/{id}/orders/{order_id} returning customer+items[] while the LIST endpoint carries NO items; codes unique per type (tonno pizza+pasta); dashboard at {PIZZASIM_URL}/dashboard/pizzerias/{id}; docs at {PIZZASIM_URL}/swagger.html.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round11-spec-v3-analysis.md:24:R1. Five already-verified contract facts were demoted back into "Open contract questions" (menu shape incl. price, extras vocabulary, error bodies, status values, /location) — directly violating v3's own new shrink-only rule ("a verified fact never moves back into the open list").
/home/rob/bpm-pizza-vibecoding-solution/reviews/round11-spec-v3-analysis.md:26:R3. The greeting changed to "in the customer's UI language", but the initial UI language before any switch is undefined, and the CLI has no UI language at all — with "nothing is hardcoded" this is unresolvable without an env var (v1/v2 builds used PIZZERIA_LANG per an oracle decision; a prior grill condition required documenting it in the spec; v3 omits it).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round11-spec-v3-analysis.md:27:R4. Basket-total ownership is unspecified: the spec demands the customer "sees what the basket comes to" and allows "what does my basket come to?" questions, but the fixed tools table gives no total anywhere (read_back returns basket/customer/revision only), inviting the implementer to let the LLM do arithmetic — which "no invented figures" should forbid.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round11-spec-v3-analysis.md:30:A1. Language precedence unresolved: "answers in the language the customer used, per turn" vs header switch "applied to the agent's replies" — which wins when they conflict?
/home/rob/bpm-pizza-vibecoding-solution/reviews/round11-spec-v3-analysis.md:32:A3. remove_item semantics when several lines share (type,code) with different extras remain unspecified (params are fixed).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round11-spec-v3-analysis.md:35:I1. Shrink-only contracts principle + new pass 0 "Contracts".
/home/rob/bpm-pizza-vibecoding-solution/reviews/round11-spec-v3-analysis.md:37:I3. SPEECH_* optionality now explicit in the env rules; speech browser capture (getUserMedia/MediaRecorder) sanctioned cross-browser; channels/speech.py and tests/test_web_e2e.py named in deliverables.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round11-spec-v3-analysis.md:39:I5. Derived URLs (dashboard, swagger) kept verified and explicitly never-literal.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round11-spec-v3-analysis.md:41:Overall the implementer's verdict-to-be-attacked: v3 is structurally the best of the three but NOT optimal; it needs a small patch list (restore the five facts + detail endpoint per shrink-only rule; define initial/default language incl. CLI, e.g. a documented env var; state that read_back carries a code-computed basket total; one line on language precedence; one line on CLI tenancy) — after which building against it is safe.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round11-spec-v3-analysis.md:44:1. Attack: what is wrong or overstated in R1-R4/A1-A3/I1-I5? What did the implementer miss (check yourself: env table completeness, error table, testing section, deliverables tree vs existing repo, decisions-locked table consistency, anything contradicting the approved v1 core)?
/home/rob/bpm-pizza-vibecoding-solution/reviews/round11-spec-v3-analysis.md:55:/bin/bash -lc 'rg -n "PIZZERIA_LANG|language|read_back|remove_item|error|details|location|deliverable|prepared_planned|delivered|extras|toppings|dashboard|swagger|Contracts|Decisions locked|deliverables|tests|SPEECH_" /home/rob/bpm-pizza-vibecoding-solution -S' in /home/rob/bpm-pizza-vibecoding-solution
/home/rob/bpm-pizza-vibecoding-solution/tests/fixtures/error_422.json:1:{"error":"validation_failed","details":["items[0].code must be a valid pizza code"]}
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:17:Additional live evidence since round 7: a real headless Chromium was driven against the public URL http://<host>:8888 with window.isSecureContext === false. Results: zero page errors; greeting rendered; pizzeria name shown in the header; mic and TTS controls hidden (speech disabled in this deployment); a typed customer message produced a correct menu answer with the intermediate-steps block visible. Full-page screenshot captured.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:25:error_handling: N
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:142:  const details = document.createElement("details");
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:143:  details.className = "steps";
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:144:  details.innerHTML = "<summary>Zwischenschritte</summary>";
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:145:  chat.appendChild(details);
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:146:  return details;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:182:        } else if (ev.type === "error") {
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:265:    speechEnabled = cfg.speech;    // unset SPEECH_URL → nothing rendered
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:318:The agent can still run tests, stage files, and output suggested branch
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:322:/bin/bash -lc "sed -n '1,220p' reviews/round7-hotfix.md && printf '\\n--- secure-context scan ---\\n' && rg -n \"randomUUID|getRandomValues|mediaDevices|MediaRecorder|isSecureContext|speechSynthesis|SpeechRecognition|crypto\\.subtle|serviceWorker|clipboard|geolocation|Notification|PaymentRequest|CredentialsContainer|AudioContext\" channels/static" in /home/rob/bpm-pizza-vibecoding-solution
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:346:error_handling: N
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:371:proxies the optional self-hosted speech service (STT/TTS). If SPEECH_URL is
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:401:    enabled only if SPEECH_URL is set, answers, and models are configured."""
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:404:        self.url = optional_env("SPEECH_URL")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:405:        self.stt_model = optional_env("SPEECH_STT_MODEL")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:406:        self.tts_model = optional_env("SPEECH_TTS_MODEL")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:407:        self.voice = optional_env("SPEECH_TTS_VOICE")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:425:        print(f"Configuration error: {exc}", file=sys.stderr)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:515:            "language": app.state.config.lang}  # STT hint only
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:595:    38	  const details = document.createElement("details");
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:596:    39	  details.className = "steps";
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:597:    40	  details.innerHTML = "<summary>Zwischenschritte</summary>";
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:598:    41	  chat.appendChild(details);
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:599:    42	  return details;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:635:    78	        } else if (ev.type === "error") {
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:718:   161	    speechEnabled = cfg.speech;    // unset SPEECH_URL → nothing rendered
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:756:error_handling: N
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:781:proxies the optional self-hosted speech service (STT/TTS). If SPEECH_URL is
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:811:    enabled only if SPEECH_URL is set, answers, and models are configured."""
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:814:        self.url = optional_env("SPEECH_URL")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:815:        self.stt_model = optional_env("SPEECH_STT_MODEL")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:816:        self.tts_model = optional_env("SPEECH_TTS_MODEL")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:817:        self.voice = optional_env("SPEECH_TTS_VOICE")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:835:        print(f"Configuration error: {exc}", file=sys.stderr)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:925:            "language": app.state.config.lang}  # STT hint only
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:991:-  `SPEECH_URL` set and a probe succeeded at startup). No language field:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:992:-  language is never a UI control — the greeting comes from `PIZZERIA_LANG`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:995:+  (`speech` true only if `SPEECH_URL` set and a probe succeeded at startup;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:997:+  see which pizzeria they are ordering at). No language field: language is
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:998:+  never a UI control — the greeting comes from `PIZZERIA_LANG`, mirroring
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1026:-    if (speechEnabled) {           // unset SPEECH_URL → not rendered at all
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1034:+    speechEnabled = cfg.speech;    // unset SPEECH_URL → nothing rendered
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1077:    17	`uvicorn` (web channel), `pytest` (tests), stdlib `difflib` (candidate
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1087:    27	- Secrets never appear in logs, transcripts, errors, or the web UI.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1091:    31	- No build-time model name anywhere in source, config, prompts, tests, docs.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1095:    35	- Deterministic tests: no network, no LLM (one opt-in live smoke test).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1106:    46	  menu.py      Immutable Menu snapshot (pizzas, pasta, toppings), one per
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1107:    47	               session; (type, code) validation; extras validation;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1110:    50	               submit_order, check_street; typed errors; timeouts;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1114:    54	               {"error": {code, message, candidates}}.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1127:    67	  system.de.md German system prompt (default deployment language).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1129:    69	tests/
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1131:    71	               list, 422 bodies, location).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1142:    82	Deviation from the SPEC tree, documented: `tests/test_transcripts.py` and
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1152:    92	| `core/agent.py` | `LITELLM_PIZZA_URL`, `LITELLM_PIZZA_KEY`, `LITELLM_PIZZA_MODEL_1`, `PIZZERIA_LANG` (all required; `LITELLM_PIZZA_MODEL_2` read but unused — single-model build) |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1154:    94	| `channels/web.py` | `SPEECH_URL`, `SPEECH_STT_MODEL`, `SPEECH_TTS_MODEL`, `SPEECH_TTS_VOICE` (all optional; absence disables speech) |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1156:    96	`PIZZERIA_LANG` ∈ {`de`, `en`} is the pizzeria-country greeting language.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1160:   100	`decisions/qa.md`). It selects the system prompt file and the STT language
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1161:   101	hint; it never overrides per-turn language mirroring.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1174:   114	   404-pizzeria case from the error table → process refuses to start;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1192:   132	Order fields: `items: list[Item(type, code, qty, extras)]`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1194:   134	(increments on every basket or customer mutation), `read_back_revision:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1195:   135	int | None` (set by `read_back`), `state`, `submit_attempted_at: int | None`
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1209:   149	Transition table (✓ legal, ✗ → typed error):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1214:   154	| remove_item | ✗ empty_basket | ✓ | ✓ | ✓ demote | ✗ order_closed |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1216:   156	| read_back | ✗ empty_basket | ✗ invalid_state (no customer yet) | ✓ | ✓ (same basket, idempotent) | ✗ order_closed |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1222:   162	(else `stale_revision`) and `read_back_revision == order.revision` (else
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1223:   163	`read_back_required`). So the only path into `CONFIRMED` is: state `READY`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1224:   164	`read_back` called at the current revision, then `confirm_order` naming that
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1237:   177	exactly one real retry. List or detail call fails → error `submit_unknown`
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1249:   189	`{state, revision, items: [{type, code, name, qty, extras}], customer:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1250:   190	{first_name, street_one} | null, read_back_done: bool}` — never a diff.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1254:   194	| `get_menu` | `{}` | `{"menu": {"pizzas": [{code, name}], "pasta": [{code, name}], "toppings": [str]}, "snapshot": SNAPSHOT}` — `name` is the API's single display name, which the verified contract facts show serves both languages |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1255:   195	| `add_items` | `{items: [{type: enum[pizza,pasta], code: str, qty: int ≥1, extras: [str]}]}` (required: items; extras default `[]`) | `{"snapshot": SNAPSHOT}` (basket + revision live in SNAPSHOT) |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1256:   196	| `remove_item` | `{type: enum, code: str, qty: int ≥1 optional}` — the spec fixes these params, so when several lines share (type, code) with different extras: absent qty removes **all** matching lines, qty reduces the **most recently added** matching line (deterministic; the snapshot lets the model repair by remove + re-add) | `{"snapshot": SNAPSHOT}` |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1258:   198	| `read_back` | `{}` | `{"snapshot": SNAPSHOT}` — basket, customer, revision: the material the agent reads out |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1259:   199	| `confirm_order` | `{revision: int}` | `{"snapshot": SNAPSHOT}` with `state == "CONFIRMED"`, or error if stale |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1261:   201	| `check_street` | `{street: str}` | `{"street": str, "deliverable": bool, "snapshot": SNAPSHOT}` — the never-claim-verified rule lives in the prompt, not the tool |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1263:   203	Failure shape: `{"error": {"code": "<one of the codes below>", "message":
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1267:   207	candidate toppings), `invalid_quantity` (non-integer or < 1 — the tool does
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1269:   209	`read_back_required`, `order_closed`, `submit_failed`, `submit_unknown`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1270:   210	`api_unavailable`, `not_in_basket` (remove_item for a line that isn't there).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1273:   213	snapshot and every extra against `toppings[]`; any failure rejects the whole
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1274:   214	call atomically (no partial adds), returning the first error with candidates
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1286:     4	proxies the optional self-hosted speech service (STT/TTS). If SPEECH_URL is
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1316:    34	    enabled only if SPEECH_URL is set, answers, and models are configured."""
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1319:    37	        self.url = optional_env("SPEECH_URL")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1320:    38	        self.stt_model = optional_env("SPEECH_STT_MODEL")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1321:    39	        self.tts_model = optional_env("SPEECH_TTS_MODEL")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1322:    40	        self.voice = optional_env("SPEECH_TTS_VOICE")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1340:    58	        print(f"Configuration error: {exc}", file=sys.stderr)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1430:   148	            "language": app.state.config.lang}  # STT hint only
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1469:I also checked the remaining static UI for other secure-context traps. The only secure-context-dependent browser features left are the microphone path (`getUserMedia` / `MediaRecorder`) at [channels/static/app.js](/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js:104), and those are now isolated behind UI gating plus runtime error handling. Text chat, greeting bootstrap, intermediate-steps rendering, and server-proxied TTS do not share that dependency. The supplied headless Chromium evidence on plain HTTP is consistent with the code: no load-time crash, greeting renders, pizzeria name is shown, typed chat works, and speech controls stay hidden when deployment speech is disabled.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1474:error_handling: 4
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1486:I also checked the remaining static UI for other secure-context traps. The only secure-context-dependent browser features left are the microphone path (`getUserMedia` / `MediaRecorder`) at [channels/static/app.js](/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js:104), and those are now isolated behind UI gating plus runtime error handling. Text chat, greeting bootstrap, intermediate-steps rendering, and server-proxied TTS do not share that dependency. The supplied headless Chromium evidence on plain HTTP is consistent with the code: no load-time crash, greeting renders, pizzeria name is shown, typed chat works, and speech controls stay hidden when deployment speech is disabled.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1491:error_handling: 4
/home/rob/bpm-pizza-vibecoding-solution/tests/transcripts/unknown_item.json:7:       {"tool": "add_items", "args": {"items": [{"type": "pasta", "code": "bolognese", "qty": 1, "extras": []}]}},
/home/rob/bpm-pizza-vibecoding-solution/tests/transcripts/unknown_item.json:12:       {"tool": "add_items", "args": {"items": [{"type": "pasta", "code": "funghi", "qty": 1, "extras": []}]}},
/home/rob/bpm-pizza-vibecoding-solution/tests/transcripts/unknown_item.json:18:       {"tool": "read_back", "args": {}},
/home/rob/bpm-pizza-vibecoding-solution/tests/transcripts/unknown_item.json:30:    "calls": ["add_items", "add_items", "set_customer", "read_back", "confirm_order", "submit_order"],
/home/rob/bpm-pizza-vibecoding-solution/tests/transcripts/unknown_item.json:31:    "error_codes": ["unknown_item"],
/home/rob/bpm-pizza-vibecoding-solution/reviews/scores.md:7:error_handling: 4
/home/rob/bpm-pizza-vibecoding-solution/reviews/scores.md:14:results restored to the spec's fixed contract; greeting language =
/home/rob/bpm-pizza-vibecoding-solution/reviews/scores.md:16:single explicit startup sequence via `GET /pizzerias`; read_back/confirm
/home/rob/bpm-pizza-vibecoding-solution/reviews/scores.md:17:path tightened (read_back only in READY/CONFIRMED, confirm only in READY).
/home/rob/bpm-pizza-vibecoding-solution/reviews/scores.md:23:error_handling: 4
/home/rob/bpm-pizza-vibecoding-solution/reviews/scores.md:31:greeting language now required env var PIZZERIA_LANG (oracle decision in
/home/rob/bpm-pizza-vibecoding-solution/reviews/scores.md:34:hint = PIZZERIA_LANG only; per-session immutable menu snapshot defined via
/home/rob/bpm-pizza-vibecoding-solution/reviews/scores.md:41:error_handling: 5
/home/rob/bpm-pizza-vibecoding-solution/reviews/scores.md:51:error_handling: 4
/home/rob/bpm-pizza-vibecoding-solution/reviews/scores.md:57:Findings applied: remove_item now deterministic across same-(type,code)
/home/rob/bpm-pizza-vibecoding-solution/reviews/scores.md:58:lines with different extras (no qty = all matching lines, qty = most recent
/home/rob/bpm-pizza-vibecoding-solution/reviews/scores.md:59:line; two new tests; PLAN.md updated); speech probe requires 2xx via
/home/rob/bpm-pizza-vibecoding-solution/reviews/scores.md:67:error_handling: 3
/home/rob/bpm-pizza-vibecoding-solution/reviews/scores.md:90:error_handling: 5
/home/rob/bpm-pizza-vibecoding-solution/reviews/scores.md:100:error_handling: 3
/home/rob/bpm-pizza-vibecoding-solution/reviews/scores.md:115:error_handling: 4
/home/rob/bpm-pizza-vibecoding-solution/reviews/scores.md:122:(isSecureContext=false): no JS errors, greeting, pizzeria name in header,
/home/rob/bpm-pizza-vibecoding-solution/tests/fixtures/location.json:1:{"street":"via Roma","deliverable":true}
/home/rob/bpm-pizza-vibecoding-solution/tests/fixtures/orders_list.json:8:   "status": "prepared_planned",
/home/rob/bpm-pizza-vibecoding-solution/tests/fixtures/orders_list.json:9:   "delivered_at": null,
/home/rob/bpm-pizza-vibecoding-solution/tests/fixtures/orders_list.json:17:   "status": "prepared_planned",
/home/rob/bpm-pizza-vibecoding-solution/tests/fixtures/orders_list.json:18:   "delivered_at": null,
/home/rob/bpm-pizza-vibecoding-solution/tests/fixtures/orders_list.json:26:   "status": "prepared_planned",
/home/rob/bpm-pizza-vibecoding-solution/tests/fixtures/orders_list.json:27:   "delivered_at": null,
/home/rob/bpm-pizza-vibecoding-solution/tests/fixtures/orders_list.json:35:   "status": "prepared_planned",
/home/rob/bpm-pizza-vibecoding-solution/tests/fixtures/orders_list.json:36:   "delivered_at": null,
/home/rob/bpm-pizza-vibecoding-solution/tests/fixtures/orders_list.json:44:   "status": "prepared_planned",
/home/rob/bpm-pizza-vibecoding-solution/tests/fixtures/orders_list.json:45:   "delivered_at": null,
/home/rob/bpm-pizza-vibecoding-solution/tests/transcripts/mind_change.json:2:  "name": "mind_change_after_read_back",
/home/rob/bpm-pizza-vibecoding-solution/tests/transcripts/mind_change.json:7:       {"tool": "add_items", "args": {"items": [{"type": "pizza", "code": "diavolo", "qty": 1, "extras": []}]}},
/home/rob/bpm-pizza-vibecoding-solution/tests/transcripts/mind_change.json:9:       {"tool": "read_back", "args": {}},
/home/rob/bpm-pizza-vibecoding-solution/tests/transcripts/mind_change.json:14:       {"tool": "add_items", "args": {"items": [{"type": "pizza", "code": "funghi", "qty": 1, "extras": []}]}},
/home/rob/bpm-pizza-vibecoding-solution/tests/transcripts/mind_change.json:16:       {"tool": "read_back", "args": {}},
/home/rob/bpm-pizza-vibecoding-solution/tests/transcripts/mind_change.json:28:    "calls": ["add_items", "set_customer", "read_back", "add_items", "confirm_order", "read_back", "confirm_order", "submit_order"],
/home/rob/bpm-pizza-vibecoding-solution/tests/transcripts/mind_change.json:29:    "error_codes": ["stale_revision"],
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:14:1. Devil's advocate: attack the plan — gaps, wrong assumptions, missing error cases, spec violations.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:19:Context from round 1 (a previous stateless review): it required (a) no ./.env fallback and no extra config vars, (b) tool results matching the spec's fixed contract exactly, (c) greeting in the pizzeria-country language with per-turn mirroring not driven by UI controls, (d) one explicit startup sequence validating PIZZERIA_ID via GET /pizzerias, (e) a confirmation path no broader than the spec. All five were applied; verify they are actually resolved in the current PLAN.md rather than taking this note on faith.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:25:error_handling: N
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:112:> repo — code, tests, prompts, tickets — derives from it.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:157:**Core belief:** a language model is a great waiter and a terrible order pad.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:169:  tool error carrying candidate matches — never a silent guess, never a fallback
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:194:- **Languages:** German and English. The agent answers in the language the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:198:- **The success moment:** the order appears in the PizzaSim dashboard under the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:200:- **Deterministic tests** that run with no network and no LLM.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:238:- Secrets never appear in logs, transcripts, error messages or the web UI.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:249:| `GET /location?street=…` | public | street plausibility check |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:256:  "items": [{ "type": "pizza", "code": "margherita", "qty": 2, "extras": [] }]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:278:invalid bodies —, `GET /pizzerias/{id}/orders`, `GET /location`). Facts below
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:288:   `customer_id`, `created_at`, `ready_at`, `status`, `delivered_at`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:293:   there are no per-language names in the API; read-back uses `name` as-is in
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:294:   both languages. The menu response also carries a top-level `toppings[]`
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:296:4. **`extras[]` is a controlled vocabulary:** the top-level `toppings[]` from
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:298:   rejects unknown extras with `422` (`"items[0].extras contains invalid
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:299:   topping 'unicorn_dust'"`), so the tool layer validates extras against
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:300:   `toppings[]` exactly like item codes.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:302:   `{"error": "<code>", "details": ["<human sentence>", ...]}` — e.g.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:303:   `{"error": "validation_failed", "details": ["items[0].code must be a valid
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:304:   pizza code"]}` with HTTP 422. The tool layer maps `error` to typed errors
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:305:   and may surface `details` to targeted questions.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:307:   `prepared_planned` → `delivered` (with `delivered_at` set on the last).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:309:7. **`GET /location?street=` returns** `{"street": "<echo>",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:310:   "deliverable": <bool>}` with HTTP 200. In probing, even a nonsense street
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:311:   returned `deliverable: true` — the check is a weak plausibility signal at
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:327:                                                    │ read_back + customer says yes
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:334:Invariants, all enforced in code and all covered by unit tests:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:336:1. `submit_order` outside `CONFIRMED` returns an error. It does not "helpfully"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:341:   legal after `read_back` has been called for the current basket revision. The
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:355:| `get_menu` | — | pizzas and pasta with codes and display names in both languages |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:356:| `add_items` | `items[]` of `{type, code, qty, extras[]}` | new basket + revision |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:357:| `remove_item` | `code`, `type`, optional `qty` | new basket + revision |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:359:| `read_back` | — | basket, customer, revision — the text the agent must read out |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:360:| `confirm_order` | `revision` | state `CONFIRMED`, or error if stale |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:385:`uvicorn` (web channel), `pytest` (tests), stdlib `difflib` (candidate
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:395:- Secrets never appear in logs, transcripts, errors, or the web UI.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:399:- No build-time model name anywhere in source, config, prompts, tests, docs.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:403:- Deterministic tests: no network, no LLM (one opt-in live smoke test).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:414:  menu.py      Menu snapshot (pizzas, pasta, toppings) fetched once per
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:415:               session; (type, code) validation; extras validation;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:418:               submit_order, check_street; typed errors; timeouts;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:422:               {"error": {code, message, candidates}}.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:435:  system.de.md German system prompt (default deployment language).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:437:tests/
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:439:               list, 422 bodies, location).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:450:Deviation from the SPEC tree, documented: `tests/test_transcripts.py` and
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:462:| `channels/web.py` | `SPEECH_URL`, `SPEECH_STT_MODEL`, `SPEECH_TTS_MODEL`, `SPEECH_TTS_VOICE` (all optional; absence disables speech) |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:475:   404-pizzeria case from the error table → process refuses to start;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:484:Order fields: `items: list[Item(type, code, qty, extras)]`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:486:(increments on every basket or customer mutation), `read_back_revision:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:487:int | None` (set by `read_back`), `state`, `submit_unknown: bool` (a submit
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:499:Transition table (✓ legal, ✗ → typed error):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:504:| remove_item | ✗ empty_basket | ✓ | ✓ | ✓ demote | ✗ order_closed |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:506:| read_back | ✗ empty_basket | ✗ invalid_state (no customer yet) | ✓ | ✓ (same basket, idempotent) | ✗ order_closed |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:512:(else `stale_revision`) and `read_back_revision == order.revision` (else
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:513:`read_back_required`). So the only path into `CONFIRMED` is: state `READY`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:514:`read_back` called at the current revision, then `confirm_order` naming that
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:524:error `submit_unknown` with an honest message ("I'm not sure that went
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:533:| `get_menu` | `{}` | `{pizzas: [{code, name}], pasta: [{code, name}], toppings: [...]}` — `name` is the API's single display name, which the verified contract facts show serves both languages |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:534:| `add_items` | `{items: [{type: enum[pizza,pasta], code: str, qty: int ≥1, extras: [str]}]}` (required: items; extras default `[]`) | snapshot |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:535:| `remove_item` | `{type: enum, code: str, qty: int ≥1 optional}` (absent qty = remove all of that line) | snapshot |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:537:| `read_back` | `{}` | snapshot (basket, customer, revision) — the material the agent reads out |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:538:| `confirm_order` | `{revision: int}` | snapshot (state CONFIRMED), or error if stale |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:540:| `check_street` | `{street: str}` | `{street, deliverable}` — the never-claim-verified rule lives in the prompt, not the tool |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:543:qty, extras}], customer: {first_name, street_one} | null, read_back_done:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:546:Failure shape: `{"error": {"code": "<one of the codes below>", "message":
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:550:candidate toppings), `invalid_quantity` (non-integer or < 1 — the tool does
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:552:`read_back_required`, `order_closed`, `submit_failed`, `submit_unknown`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:553:`api_unavailable`, `not_in_basket` (remove_item for a line that isn't there).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:556:snapshot and every extra against `toppings[]`; any failure rejects the whole
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:557:call atomically (no partial adds), returning the first error with candidates
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:566:  the pizzeria's country language — the greeting language the spec requires.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:570:  the language of the customer's latest message (German or English),
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:572:  detects language.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:579:  the plain apology from the error table. Gateway 4xx/5xx: no retry, abort
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:582:  `tool_result`, `state`, `error` — the CLI prints them (verbose), the web
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:590:`prompts/system.de.md` / `system.en.md`, same content in two languages, calm
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:592:greet once in the file's language and offer help in one sentence; mirror the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:593:customer's language per turn (German ↔ English); one question per turn; menu
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:595:came from speech) and street, street declinable; read back via `read_back`
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:598:state order id in speakable groups and ETA in minutes; errors in plain
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:599:language, never codes or JSON; never claim the address was checked for
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:606:  (speech true only if `SPEECH_URL` set and a probe succeeded at startup).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:611:  `{SPEECH_URL}/v1/audio/transcriptions` with `SPEECH_STT_MODEL` and the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:612:  session language → `{text}`. `POST /speech/tts` body `{text}` forwarded to
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:613:  `{SPEECH_URL}/v1/audio/speech` with `SPEECH_TTS_MODEL` +
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:614:  `SPEECH_TTS_VOICE` → audio bytes. Proxying keeps the speech URL and
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:631:I have the core structure; now I’m checking the exact contract details, error semantics, and the round-1 fixes against the rest of both documents before scoring.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:676:The agent can still run tests, stage files, and output suggested branch
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:681:- Failure: `{"error": {"code": "...", "message": "...", "candidates": [...]}}`.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:695:- Greet first, in the language of the pizzeria's country, and offer help — one
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:701:- Before submitting: call `read_back`, say it, and wait for an explicit yes.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:707:- On error, explain in plain language what happened and what the customer's
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:721:| STT | `POST {SPEECH_URL}/v1/audio/transcriptions` | multipart audio file + model + language |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:722:| TTS | `POST {SPEECH_URL}/v1/audio/speech` | JSON with model, voice, input text; returns audio |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:732:  model, TTS model, voice and language all come from the environment, exactly
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:737:  | `SPEECH_URL` | base URL of the self-hosted speech service |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:738:  | `SPEECH_STT_MODEL` | transcription model id |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:739:  | `SPEECH_TTS_MODEL` | synthesis model id |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:740:  | `SPEECH_TTS_VOICE` | voice id |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:751:- **Speech is never required.** If `SPEECH_URL` is unset or the service does not
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:757:- **Confirm the name.** Transcription errors on names are the expensive failure:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:819:  menu question — plus one run with `SPEECH_URL` unset, which must render a
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:846:  **none of this spec's business**. Nothing in the deliverables reads them,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:855:  source, config, prompts, tests or documentation.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:868:  wrong assumptions, missing error cases — and *judge*, scoring against the fixed
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:883:error_handling: N
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:904:   loop, error handling, conversation state. **No code.** Send it to the reviewer
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:921:1. **Core.** Order model, state machine, tool layer, tests. No LLM, no network.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:922:   Pass when the unit tests are green.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:924:3. **CLI.** Full conversation, real API, an order visible in the dashboard.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:927:6. **Harden.** Walk the error table, force each case, fix what breaks.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:944:| 422 validation | typed `ValidationError(details)` → tool error `submit_failed` with field text, basket kept |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:970:  question, `SPEECH_URL` unset run).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:979:2. **Order + state machine + tests.** `core/order.py`, `core/state.py`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:980:   `tests/test_state.py`.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:985:   extras vocabulary ☐ ≤3 candidates.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:986:4. **PizzaSim client.** `core/pizzasim.py`, typed errors, timeouts,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:987:   fixtures for orders/422/location, httpx MockTransport tests.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:988:   ☐ every error class mapped ☐ no call without timeout ☐ submit returns
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:990:5. **Tools.** `core/tools.py` schemas + dispatch, `tests/test_tools.py`.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:991:   ☐ schemas match this plan exactly ☐ atomic add ☐ error shape uniform
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1004:   only ☐ `SPEECH_URL` unset → no mic, no speaker, text works ☐ speech
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1006:10. **Harden + docs.** Walk the SPEC error table end to end, README
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1008:    ☐ each error row demonstrably handled ☐ README covers all channels +
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1009:    speech + tests ☐ full suite green.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1011:Each ticket ≤ 1h, tests live in the ticket that introduces the behaviour.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1026:    82	Deviation from the SPEC tree, documented: `tests/test_transcripts.py` and
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1038:    94	| `channels/web.py` | `SPEECH_URL`, `SPEECH_STT_MODEL`, `SPEECH_TTS_MODEL`, `SPEECH_TTS_VOICE` (all optional; absence disables speech) |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1051:   107	   404-pizzeria case from the error table → process refuses to start;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1060:   116	Order fields: `items: list[Item(type, code, qty, extras)]`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1062:   118	(increments on every basket or customer mutation), `read_back_revision:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1063:   119	int | None` (set by `read_back`), `state`, `submit_unknown: bool` (a submit
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1075:   131	Transition table (✓ legal, ✗ → typed error):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1080:   136	| remove_item | ✗ empty_basket | ✓ | ✓ | ✓ demote | ✗ order_closed |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1082:   138	| read_back | ✗ empty_basket | ✗ invalid_state (no customer yet) | ✓ | ✓ (same basket, idempotent) | ✗ order_closed |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1088:   144	(else `stale_revision`) and `read_back_revision == order.revision` (else
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1089:   145	`read_back_required`). So the only path into `CONFIRMED` is: state `READY`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1090:   146	`read_back` called at the current revision, then `confirm_order` naming that
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1100:   156	error `submit_unknown` with an honest message ("I'm not sure that went
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1109:   165	| `get_menu` | `{}` | `{pizzas: [{code, name}], pasta: [{code, name}], toppings: [...]}` — `name` is the API's single display name, which the verified contract facts show serves both languages |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1110:   166	| `add_items` | `{items: [{type: enum[pizza,pasta], code: str, qty: int ≥1, extras: [str]}]}` (required: items; extras default `[]`) | snapshot |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1111:   167	| `remove_item` | `{type: enum, code: str, qty: int ≥1 optional}` (absent qty = remove all of that line) | snapshot |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1113:   169	| `read_back` | `{}` | snapshot (basket, customer, revision) — the material the agent reads out |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1114:   170	| `confirm_order` | `{revision: int}` | snapshot (state CONFIRMED), or error if stale |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1116:   172	| `check_street` | `{street: str}` | `{street, deliverable}` — the never-claim-verified rule lives in the prompt, not the tool |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1119:   175	qty, extras}], customer: {first_name, street_one} | null, read_back_done:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1122:   178	Failure shape: `{"error": {"code": "<one of the codes below>", "message":
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1126:   182	candidate toppings), `invalid_quantity` (non-integer or < 1 — the tool does
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1128:   184	`read_back_required`, `order_closed`, `submit_failed`, `submit_unknown`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1129:   185	`api_unavailable`, `not_in_basket` (remove_item for a line that isn't there).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1132:   188	snapshot and every extra against `toppings[]`; any failure rejects the whole
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1133:   189	call atomically (no partial adds), returning the first error with candidates
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1142:   198	  the pizzeria's country language — the greeting language the spec requires.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1146:   202	  the language of the customer's latest message (German or English),
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1148:   204	  detects language.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1155:   211	  the plain apology from the error table. Gateway 4xx/5xx: no retry, abort
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1158:   214	  `tool_result`, `state`, `error` — the CLI prints them (verbose), the web
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1167:   230	1. `submit_order` outside `CONFIRMED` returns an error. It does not "helpfully"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1172:   235	   legal after `read_back` has been called for the current basket revision. The
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1186:   249	| `get_menu` | — | pizzas and pasta with codes and display names in both languages |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1187:   250	| `add_items` | `items[]` of `{type, code, qty, extras[]}` | new basket + revision |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1188:   251	| `remove_item` | `code`, `type`, optional `qty` | new basket + revision |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1190:   253	| `read_back` | — | basket, customer, revision — the text the agent must read out |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1191:   254	| `confirm_order` | `revision` | state `CONFIRMED`, or error if stale |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1199:   262	- Failure: `{"error": {"code": "...", "message": "...", "candidates": [...]}}`.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1213:   276	- Greet first, in the language of the pizzeria's country, and offer help — one
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1219:   282	- Before submitting: call `read_back`, say it, and wait for an explicit yes.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1225:   288	- On error, explain in plain language what happened and what the customer's
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1239:   302	| STT | `POST {SPEECH_URL}/v1/audio/transcriptions` | multipart audio file + model + language |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1240:   303	| TTS | `POST {SPEECH_URL}/v1/audio/speech` | JSON with model, voice, input text; returns audio |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1250:   313	  model, TTS model, voice and language all come from the environment, exactly
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1255:   318	  | `SPEECH_URL` | base URL of the self-hosted speech service |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1256:   319	  | `SPEECH_STT_MODEL` | transcription model id |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1257:   320	  | `SPEECH_TTS_MODEL` | synthesis model id |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1258:   321	  | `SPEECH_TTS_VOICE` | voice id |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1269:   332	- **Speech is never required.** If `SPEECH_URL` is unset or the service does not
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1275:   338	- **Confirm the name.** Transcription errors on names are the expensive failure:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1302:   132	- Secrets never appear in logs, transcripts, error messages or the web UI.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1313:   143	| `GET /location?street=…` | public | street plausibility check |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1320:   150	  "items": [{ "type": "pizza", "code": "margherita", "qty": 2, "extras": [] }]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1342:   172	invalid bodies —, `GET /pizzerias/{id}/orders`, `GET /location`). Facts below
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1352:   182	   `customer_id`, `created_at`, `ready_at`, `status`, `delivered_at`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1357:   187	   there are no per-language names in the API; read-back uses `name` as-is in
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1358:   188	   both languages. The menu response also carries a top-level `toppings[]`
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1360:   190	4. **`extras[]` is a controlled vocabulary:** the top-level `toppings[]` from
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1362:   192	   rejects unknown extras with `422` (`"items[0].extras contains invalid
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1363:   193	   topping 'unicorn_dust'"`), so the tool layer validates extras against
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1364:   194	   `toppings[]` exactly like item codes.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1366:   196	   `{"error": "<code>", "details": ["<human sentence>", ...]}` — e.g.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1367:   197	   `{"error": "validation_failed", "details": ["items[0].code must be a valid
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1368:   198	   pizza code"]}` with HTTP 422. The tool layer maps `error` to typed errors
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1369:   199	   and may surface `details` to targeted questions.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1371:   201	   `prepared_planned` → `delivered` (with `delivered_at` set on the last).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1373:   203	7. **`GET /location?street=` returns** `{"street": "<echo>",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1374:   204	   "deliverable": <bool>}` with HTTP 200. In probing, even a nonsense street
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1375:   205	   returned `deliverable: true` — the check is a weak plausibility signal at
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1385:   222	`prompts/system.de.md` / `system.en.md`, same content in two languages, calm
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1387:   224	greet once in the file's language and offer help in one sentence; mirror the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1388:   225	customer's language per turn (German ↔ English); one question per turn; menu
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1390:   227	came from speech) and street, street declinable; read back via `read_back`
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1393:   230	state order id in speakable groups and ETA in minutes; errors in plain
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1394:   231	language, never codes or JSON; never claim the address was checked for
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1401:   238	  (speech true only if `SPEECH_URL` set and a probe succeeded at startup).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1406:   243	  `{SPEECH_URL}/v1/audio/transcriptions` with `SPEECH_STT_MODEL` and the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1407:   244	  session language → `{text}`. `POST /speech/tts` body `{text}` forwarded to
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1408:   245	  `{SPEECH_URL}/v1/audio/speech` with `SPEECH_TTS_MODEL` +
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1409:   246	  `SPEECH_TTS_VOICE` → audio bytes. Proxying keeps the speech URL and
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1426:   263	| 422 validation | typed `ValidationError(details)` → tool error `submit_failed` with field text, basket kept |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1452:   289	  question, `SPEECH_URL` unset run).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1461:   298	2. **Order + state machine + tests.** `core/order.py`, `core/state.py`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1462:   299	   `tests/test_state.py`.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1467:   304	   extras vocabulary ☐ ≤3 candidates.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1468:   305	4. **PizzaSim client.** `core/pizzasim.py`, typed errors, timeouts,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1469:   306	   fixtures for orders/422/location, httpx MockTransport tests.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1470:   307	   ☐ every error class mapped ☐ no call without timeout ☐ submit returns
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1472:   309	5. **Tools.** `core/tools.py` schemas + dispatch, `tests/test_tools.py`.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1473:   310	   ☐ schemas match this plan exactly ☐ atomic add ☐ error shape uniform
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1486:   323	   only ☐ `SPEECH_URL` unset → no mic, no speaker, text works ☐ speech
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1488:   325	10. **Harden + docs.** Walk the SPEC error table end to end, README
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1490:   327	    ☐ each error row demonstrably handled ☐ README covers all channels +
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1491:   328	    speech + tests ☐ full suite green.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1493:   330	Each ticket ≤ 1h, tests live in the ticket that introduces the behaviour.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1498:- `get_menu` and `submit_order` are still not pinned to one exact spec contract. The spec fixes `get_menu` as “codes and display names in both languages” and separately says every successful tool result must expose full current state; the plan instead defines `get_menu` as `{pizzas:[{code,name}], pasta:[{code,name}], toppings:[...]}`, `submit_order` as only `{order_id,status,eta_seconds}`, and then adds a separate “snapshot on every success” rule. The tests also regress to `eta_minutes`, which is explicitly not the API/tool field. This is not implementable unambiguously and does not satisfy the “match the fixed contract exactly” round-1 requirement. [SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:247) [SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:258) [PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:163) [PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:174) [PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:279)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1499:- The greeting-language requirement is not actually resolved. The spec requires greeting first in the pizzeria country’s language; the plan says the live API has no country field and therefore uses deployment default `de`. That is still a hardcoded assumption about country/language selection, and implementing exactly that plan will greet incorrectly for any non-German deployment. [SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:276) [PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:196)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1501:- The web contract reintroduces a language control without fencing it off tightly enough. `GET /config` exposes `langs`, and `POST /chat` accepts `lang`; elsewhere the plan says language mirroring must not be runtime-detected or UI-controlled. Unless the plan explicitly states that `lang` is used only for STT hints and never for assistant response language, this reopens the exact round-1 failure mode. [SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:83) [PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:196) [PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:237)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1507:error_handling: 4
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1514:- Replace the hardcoded startup default `de` with a spec-compliant source of pizzeria-country language, or explicitly revise the plan so this requirement is met without UI control or hardcoding.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1516:- Remove `lang` from the text chat contract, or state unambiguously that it is an STT hint only and can never influence assistant output language or greeting behavior.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1522:- `get_menu` and `submit_order` are still not pinned to one exact spec contract. The spec fixes `get_menu` as “codes and display names in both languages” and separately says every successful tool result must expose full current state; the plan instead defines `get_menu` as `{pizzas:[{code,name}], pasta:[{code,name}], toppings:[...]}`, `submit_order` as only `{order_id,status,eta_seconds}`, and then adds a separate “snapshot on every success” rule. The tests also regress to `eta_minutes`, which is explicitly not the API/tool field. This is not implementable unambiguously and does not satisfy the “match the fixed contract exactly” round-1 requirement. [SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:247) [SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:258) [PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:163) [PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:174) [PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:279)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1523:- The greeting-language requirement is not actually resolved. The spec requires greeting first in the pizzeria country’s language; the plan says the live API has no country field and therefore uses deployment default `de`. That is still a hardcoded assumption about country/language selection, and implementing exactly that plan will greet incorrectly for any non-German deployment. [SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:276) [PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:196)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1525:- The web contract reintroduces a language control without fencing it off tightly enough. `GET /config` exposes `langs`, and `POST /chat` accepts `lang`; elsewhere the plan says language mirroring must not be runtime-detected or UI-controlled. Unless the plan explicitly states that `lang` is used only for STT hints and never for assistant response language, this reopens the exact round-1 failure mode. [SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:83) [PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:196) [PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:237)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1531:error_handling: 4
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1538:- Replace the hardcoded startup default `de` with a spec-compliant source of pizzeria-country language, or explicitly revise the plan so this requirement is met without UI control or hardcoding.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1540:- Remove `lang` from the text chat contract, or state unambiguously that it is an STT hint only and can never influence assistant output language or greeting behavior.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:14:1. Devil's advocate: attack the plan — gaps, wrong assumptions, missing error cases, spec violations.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:17:Task: Read SPEC.md (the source of truth) and PLAN.md (the stage-1 implementation plan under review, round 3 of max 3). Judge whether PLAN.md is a complete, correct, spec-compliant plan such that implementing exactly it satisfies SPEC.md. The "Contract facts" section in SPEC.md was verified against the live API and is trustworthy. decisions/qa.md records an oracle decision on the greeting language (required env var PIZZERIA_LANG) taken between rounds.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:19:Round 2 (stateless, see reviews/round2-plan.md) required: (1) one exact tool-result contract per tool composing the per-tool table with the full-current-state rule, and fixing an eta_minutes test regression; (2) a spec-compliant, non-hardcoded, non-UI source for the greeting language; (3) explicit persisted state for submit-timeout recovery correlation; (4) removing lang from the chat contract or fencing it to an STT hint; (5) per-session immutable menu snapshot ownership. All five were addressed in the current PLAN.md — verify in the file, do not take this note on faith: see the SNAPSHOT definition in "Tool schemas", the PIZZERIA_LANG paragraph in "Configuration", submit_attempted_at in the state-machine section, the web protocol section, and the "Session model" paragraph.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:27:error_handling: N
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:62:1. Devil's advocate: attack the plan — gaps, wrong assumptions, missing error cases, spec violations.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:67:Context from round 1 (a previous stateless review): it required (a) no ./.env fallback and no extra config vars, (b) tool results matching the spec's fixed contract exactly, (c) greeting in the pizzeria-country language with per-turn mirroring not driven by UI controls, (d) one explicit startup sequence validating PIZZERIA_ID via GET /pizzerias, (e) a confirmation path no broader than the spec. All five were applied; verify they are actually resolved in the current PLAN.md rather than taking this note on faith.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:73:error_handling: N
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:160:> repo — code, tests, prompts, tickets — derives from it.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:205:**Core belief:** a language model is a great waiter and a terrible order pad.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:217:  tool error carrying candidate matches — never a silent guess, never a fallback
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:242:- **Languages:** German and English. The agent answers in the language the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:246:- **The success moment:** the order appears in the PizzaSim dashboard under the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:248:- **Deterministic tests** that run with no network and no LLM.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:286:- Secrets never appear in logs, transcripts, error messages or the web UI.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:297:| `GET /location?street=…` | public | street plausibility check |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:304:  "items": [{ "type": "pizza", "code": "margherita", "qty": 2, "extras": [] }]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:313:## 2026-07-31 — Greeting language source
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:315:**Q:** SPEC requires greeting in the pizzeria-country language; the live API
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:317:Which mechanism: (a) optional env `PIZZERIA_LANG` default de, (b) required
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:320:**A (decision):** **(b)** — `PIZZERIA_LANG` (de|en) is a required env var.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:323:before the first turn naming `PIZZERIA_LANG` and where it was expected; no
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:332:> repo — code, tests, prompts, tickets — derives from it.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:377:**Core belief:** a language model is a great waiter and a terrible order pad.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:389:  tool error carrying candidate matches — never a silent guess, never a fallback
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:414:- **Languages:** German and English. The agent answers in the language the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:418:- **The success moment:** the order appears in the PizzaSim dashboard under the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:420:- **Deterministic tests** that run with no network and no LLM.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:458:- Secrets never appear in logs, transcripts, error messages or the web UI.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:469:| `GET /location?street=…` | public | street plausibility check |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:476:  "items": [{ "type": "pizza", "code": "margherita", "qty": 2, "extras": [] }]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:498:invalid bodies —, `GET /pizzerias/{id}/orders`, `GET /location`). Facts below
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:508:   `customer_id`, `created_at`, `ready_at`, `status`, `delivered_at`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:513:   there are no per-language names in the API; read-back uses `name` as-is in
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:514:   both languages. The menu response also carries a top-level `toppings[]`
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:516:4. **`extras[]` is a controlled vocabulary:** the top-level `toppings[]` from
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:518:   rejects unknown extras with `422` (`"items[0].extras contains invalid
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:519:   topping 'unicorn_dust'"`), so the tool layer validates extras against
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:520:   `toppings[]` exactly like item codes.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:522:   `{"error": "<code>", "details": ["<human sentence>", ...]}` — e.g.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:523:   `{"error": "validation_failed", "details": ["items[0].code must be a valid
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:524:   pizza code"]}` with HTTP 422. The tool layer maps `error` to typed errors
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:525:   and may surface `details` to targeted questions.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:527:   `prepared_planned` → `delivered` (with `delivered_at` set on the last).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:529:7. **`GET /location?street=` returns** `{"street": "<echo>",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:530:   "deliverable": <bool>}` with HTTP 200. In probing, even a nonsense street
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:531:   returned `deliverable: true` — the check is a weak plausibility signal at
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:547:                                                    │ read_back + customer says yes
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:554:Invariants, all enforced in code and all covered by unit tests:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:556:1. `submit_order` outside `CONFIRMED` returns an error. It does not "helpfully"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:561:   legal after `read_back` has been called for the current basket revision. The
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:575:| `get_menu` | — | pizzas and pasta with codes and display names in both languages |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:576:| `add_items` | `items[]` of `{type, code, qty, extras[]}` | new basket + revision |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:577:| `remove_item` | `code`, `type`, optional `qty` | new basket + revision |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:579:| `read_back` | — | basket, customer, revision — the text the agent must read out |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:580:| `confirm_order` | `revision` | state `CONFIRMED`, or error if stale |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:669:`uvicorn` (web channel), `pytest` (tests), stdlib `difflib` (candidate
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:679:- Secrets never appear in logs, transcripts, errors, or the web UI.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:683:- No build-time model name anywhere in source, config, prompts, tests, docs.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:687:- Deterministic tests: no network, no LLM (one opt-in live smoke test).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:698:  menu.py      Immutable Menu snapshot (pizzas, pasta, toppings), one per
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:699:               session; (type, code) validation; extras validation;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:702:               submit_order, check_street; typed errors; timeouts;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:706:               {"error": {code, message, candidates}}.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:719:  system.de.md German system prompt (default deployment language).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:721:tests/
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:723:               list, 422 bodies, location).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:734:Deviation from the SPEC tree, documented: `tests/test_transcripts.py` and
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:744:| `core/agent.py` | `LITELLM_PIZZA_URL`, `LITELLM_PIZZA_KEY`, `LITELLM_PIZZA_MODEL_1`, `PIZZERIA_LANG` (all required; `LITELLM_PIZZA_MODEL_2` read but unused — single-model build) |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:746:| `channels/web.py` | `SPEECH_URL`, `SPEECH_STT_MODEL`, `SPEECH_TTS_MODEL`, `SPEECH_TTS_VOICE` (all optional; absence disables speech) |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:748:`PIZZERIA_LANG` ∈ {`de`, `en`} is the pizzeria-country greeting language.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:752:`decisions/qa.md`). It selects the system prompt file and the STT language
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:753:hint; it never overrides per-turn language mirroring.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:766:   404-pizzeria case from the error table → process refuses to start;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:784:Order fields: `items: list[Item(type, code, qty, extras)]`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:786:(increments on every basket or customer mutation), `read_back_revision:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:787:int | None` (set by `read_back`), `state`, `submit_attempted_at: int | None`
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:801:Transition table (✓ legal, ✗ → typed error):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:806:| remove_item | ✗ empty_basket | ✓ | ✓ | ✓ demote | ✗ order_closed |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:808:| read_back | ✗ empty_basket | ✗ invalid_state (no customer yet) | ✓ | ✓ (same basket, idempotent) | ✗ order_closed |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:814:(else `stale_revision`) and `read_back_revision == order.revision` (else
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:815:`read_back_required`). So the only path into `CONFIRMED` is: state `READY`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:816:`read_back` called at the current revision, then `confirm_order` naming that
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:827:real retry. List endpoint itself fails → error `submit_unknown` with an
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:837:`{state, revision, items: [{type, code, name, qty, extras}], customer:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:838:{first_name, street_one} | null, read_back_done: bool}` — never a diff.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:842:| `get_menu` | `{}` | `{"menu": {"pizzas": [{code, name}], "pasta": [{code, name}], "toppings": [str]}, "snapshot": SNAPSHOT}` — `name` is the API's single display name, which the verified contract facts show serves both languages |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:843:| `add_items` | `{items: [{type: enum[pizza,pasta], code: str, qty: int ≥1, extras: [str]}]}` (required: items; extras default `[]`) | `{"snapshot": SNAPSHOT}` (basket + revision live in SNAPSHOT) |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:844:| `remove_item` | `{type: enum, code: str, qty: int ≥1 optional}` (absent qty = remove all of that line) | `{"snapshot": SNAPSHOT}` |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:846:| `read_back` | `{}` | `{"snapshot": SNAPSHOT}` — basket, customer, revision: the material the agent reads out |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:847:| `confirm_order` | `{revision: int}` | `{"snapshot": SNAPSHOT}` with `state == "CONFIRMED"`, or error if stale |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:849:| `check_street` | `{street: str}` | `{"street": str, "deliverable": bool, "snapshot": SNAPSHOT}` — the never-claim-verified rule lives in the prompt, not the tool |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:851:Failure shape: `{"error": {"code": "<one of the codes below>", "message":
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:855:candidate toppings), `invalid_quantity` (non-integer or < 1 — the tool does
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:857:`read_back_required`, `order_closed`, `submit_failed`, `submit_unknown`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:858:`api_unavailable`, `not_in_basket` (remove_item for a line that isn't there).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:861:snapshot and every extra against `toppings[]`; any failure rejects the whole
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:862:call atomically (no partial adds), returning the first error with candidates
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:871:  `lang = PIZZERIA_LANG` — the pizzeria-country greeting language, a
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:874:  language of the customer's latest message (German or English), unprompted.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:875:  Language mirroring is model behaviour; the runtime never detects language.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:882:  the plain apology from the error table. Gateway 4xx/5xx: no retry, abort
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:885:  `tool_result`, `state`, `error` — the CLI prints them (verbose), the web
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:893:`prompts/system.de.md` / `system.en.md`, same content in two languages, calm
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:895:greet once in the file's language and offer help in one sentence; mirror the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:896:customer's language per turn (German ↔ English); one question per turn; menu
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:898:came from speech) and street, street declinable; read back via `read_back`
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:901:state order id in speakable groups and ETA in minutes; errors in plain
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:902:language, never codes or JSON; never claim the address was checked for
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:909:  `SPEECH_URL` set and a probe succeeded at startup). No language field:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:910:  language is never a UI control — the greeting comes from `PIZZERIA_LANG`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:956:The agent can still run tests, stage files, and output suggested branch
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:960:I’m checking the remaining spec sections against the rest of `PLAN.md` now, especially the web protocol, speech flow, testing, and deliverables, because those are where plan-sized omissions usually hide.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:965:- Failure: `{"error": {"code": "...", "message": "...", "candidates": [...]}}`.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:979:- Greet first, in the language of the pizzeria's country, and offer help — one
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:985:- Before submitting: call `read_back`, say it, and wait for an explicit yes.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:991:- On error, explain in plain language what happened and what the customer's
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1005:| STT | `POST {SPEECH_URL}/v1/audio/transcriptions` | multipart audio file + model + language |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1006:| TTS | `POST {SPEECH_URL}/v1/audio/speech` | JSON with model, voice, input text; returns audio |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1016:  model, TTS model, voice and language all come from the environment, exactly
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1021:  | `SPEECH_URL` | base URL of the self-hosted speech service |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1022:  | `SPEECH_STT_MODEL` | transcription model id |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1023:  | `SPEECH_TTS_MODEL` | synthesis model id |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1024:  | `SPEECH_TTS_VOICE` | voice id |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1035:- **Speech is never required.** If `SPEECH_URL` is unset or the service does not
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1041:- **Confirm the name.** Transcription errors on names are the expensive failure:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1103:  menu question — plus one run with `SPEECH_URL` unset, which must render a
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1130:  **none of this spec's business**. Nothing in the deliverables reads them,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1139:  source, config, prompts, tests or documentation.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1152:  wrong assumptions, missing error cases — and *judge*, scoring against the fixed
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1167:error_handling: N
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1188:   loop, error handling, conversation state. **No code.** Send it to the reviewer
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1205:1. **Core.** Order model, state machine, tool layer, tests. No LLM, no network.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1206:   Pass when the unit tests are green.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1208:3. **CLI.** Full conversation, real API, an order visible in the dashboard.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1211:6. **Harden.** Walk the error table, force each case, fix what breaks.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1230:  `{SPEECH_URL}/v1/audio/transcriptions` with `SPEECH_STT_MODEL` and
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1231:  `PIZZERIA_LANG` as the language hint (an STT hint only — it never
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1232:  influences assistant output language) → `{text}`. `POST /speech/tts` body `{text}` forwarded to
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1233:  `{SPEECH_URL}/v1/audio/speech` with `SPEECH_TTS_MODEL` +
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1234:  `SPEECH_TTS_VOICE` → audio bytes. Proxying keeps the speech URL and
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1251:| 422 validation | typed `ValidationError(details)` → tool error `submit_failed` with field text, basket kept |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1278:  question, `SPEECH_URL` unset run).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1285:   ☐ `.env.example` lists all 12 vars (incl. `PIZZERIA_LANG`), names only
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1288:2. **Order + state machine + tests.** `core/order.py`, `core/state.py`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1289:   `tests/test_state.py`.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1294:   extras vocabulary ☐ ≤3 candidates.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1295:4. **PizzaSim client.** `core/pizzasim.py`, typed errors, timeouts,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1296:   fixtures for orders/422/location, httpx MockTransport tests.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1297:   ☐ every error class mapped ☐ no call without timeout ☐ submit returns
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1299:5. **Tools.** `core/tools.py` schemas + dispatch, `tests/test_tools.py`.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1300:   ☐ schemas match this plan exactly ☐ atomic add ☐ error shape uniform
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1313:   only ☐ `SPEECH_URL` unset → no mic, no speaker, text works ☐ speech
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1315:10. **Harden + docs.** Walk the SPEC error table end to end, README
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1317:    ☐ each error row demonstrably handled ☐ README covers all channels +
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1318:    speech + tests ☐ full suite green.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1320:Each ticket ≤ 1h, tests live in the ticket that introduces the behaviour.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1323:The cross-check is down to edge cases now: tool contracts, submit-timeout recovery, language handling, and session/menu ownership. I’m pulling line-numbered excerpts so the verdict is tied to the actual plan text rather than general impressions.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1363:   132	- Secrets never appear in logs, transcripts, error messages or the web UI.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1374:   143	| `GET /location?street=…` | public | street plausibility check |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1381:   150	  "items": [{ "type": "pizza", "code": "margherita", "qty": 2, "extras": [] }]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1403:   172	invalid bodies —, `GET /pizzerias/{id}/orders`, `GET /location`). Facts below
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1413:   182	   `customer_id`, `created_at`, `ready_at`, `status`, `delivered_at`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1418:   187	   there are no per-language names in the API; read-back uses `name` as-is in
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1419:   188	   both languages. The menu response also carries a top-level `toppings[]`
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1421:   190	4. **`extras[]` is a controlled vocabulary:** the top-level `toppings[]` from
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1423:   192	   rejects unknown extras with `422` (`"items[0].extras contains invalid
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1424:   193	   topping 'unicorn_dust'"`), so the tool layer validates extras against
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1425:   194	   `toppings[]` exactly like item codes.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1427:   196	   `{"error": "<code>", "details": ["<human sentence>", ...]}` — e.g.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1428:   197	   `{"error": "validation_failed", "details": ["items[0].code must be a valid
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1429:   198	   pizza code"]}` with HTTP 422. The tool layer maps `error` to typed errors
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1430:   199	   and may surface `details` to targeted questions.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1432:   201	   `prepared_planned` → `delivered` (with `delivered_at` set on the last).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1434:   203	7. **`GET /location?street=` returns** `{"street": "<echo>",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1435:   204	   "deliverable": <bool>}` with HTTP 200. In probing, even a nonsense street
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1436:   205	   returned `deliverable: true` — the check is a weak plausibility signal at
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1452:   221	                                                    │ read_back + customer says yes
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1459:   228	Invariants, all enforced in code and all covered by unit tests:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1461:   230	1. `submit_order` outside `CONFIRMED` returns an error. It does not "helpfully"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1466:   235	   legal after `read_back` has been called for the current basket revision. The
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1480:   249	| `get_menu` | — | pizzas and pasta with codes and display names in both languages |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1481:   250	| `add_items` | `items[]` of `{type, code, qty, extras[]}` | new basket + revision |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1482:   251	| `remove_item` | `code`, `type`, optional `qty` | new basket + revision |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1484:   253	| `read_back` | — | basket, customer, revision — the text the agent must read out |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1485:   254	| `confirm_order` | `revision` | state `CONFIRMED`, or error if stale |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1493:   262	- Failure: `{"error": {"code": "...", "message": "...", "candidates": [...]}}`.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1507:   276	- Greet first, in the language of the pizzeria's country, and offer help — one
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1513:   282	- Before submitting: call `read_back`, say it, and wait for an explicit yes.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1519:   288	- On error, explain in plain language what happened and what the customer's
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1533:   302	| STT | `POST {SPEECH_URL}/v1/audio/transcriptions` | multipart audio file + model + language |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1534:   303	| TTS | `POST {SPEECH_URL}/v1/audio/speech` | JSON with model, voice, input text; returns audio |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1544:   313	  model, TTS model, voice and language all come from the environment, exactly
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1549:   318	  | `SPEECH_URL` | base URL of the self-hosted speech service |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1550:   319	  | `SPEECH_STT_MODEL` | transcription model id |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1551:   320	  | `SPEECH_TTS_MODEL` | synthesis model id |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1552:   321	  | `SPEECH_TTS_VOICE` | voice id |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1563:   332	- **Speech is never required.** If `SPEECH_URL` is unset or the service does not
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1569:   338	- **Confirm the name.** Transcription errors on names are the expensive failure:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1596:     3	## 2026-07-31 — Greeting language source
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1598:     5	**Q:** SPEC requires greeting in the pizzeria-country language; the live API
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1600:     7	Which mechanism: (a) optional env `PIZZERIA_LANG` default de, (b) required
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1603:    10	**A (decision):** **(b)** — `PIZZERIA_LANG` (de|en) is a required env var.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1606:    13	before the first turn naming `PIZZERIA_LANG` and where it was expected; no
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1626:    17	`uvicorn` (web channel), `pytest` (tests), stdlib `difflib` (candidate
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1636:    27	- Secrets never appear in logs, transcripts, errors, or the web UI.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1640:    31	- No build-time model name anywhere in source, config, prompts, tests, docs.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1644:    35	- Deterministic tests: no network, no LLM (one opt-in live smoke test).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1655:    46	  menu.py      Immutable Menu snapshot (pizzas, pasta, toppings), one per
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1656:    47	               session; (type, code) validation; extras validation;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1659:    50	               submit_order, check_street; typed errors; timeouts;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1663:    54	               {"error": {code, message, candidates}}.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1676:    67	  system.de.md German system prompt (default deployment language).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1678:    69	tests/
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1680:    71	               list, 422 bodies, location).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1691:    82	Deviation from the SPEC tree, documented: `tests/test_transcripts.py` and
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1701:    92	| `core/agent.py` | `LITELLM_PIZZA_URL`, `LITELLM_PIZZA_KEY`, `LITELLM_PIZZA_MODEL_1`, `PIZZERIA_LANG` (all required; `LITELLM_PIZZA_MODEL_2` read but unused — single-model build) |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1703:    94	| `channels/web.py` | `SPEECH_URL`, `SPEECH_STT_MODEL`, `SPEECH_TTS_MODEL`, `SPEECH_TTS_VOICE` (all optional; absence disables speech) |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1705:    96	`PIZZERIA_LANG` ∈ {`de`, `en`} is the pizzeria-country greeting language.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1709:   100	`decisions/qa.md`). It selects the system prompt file and the STT language
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1710:   101	hint; it never overrides per-turn language mirroring.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1723:   114	   404-pizzeria case from the error table → process refuses to start;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1741:   132	Order fields: `items: list[Item(type, code, qty, extras)]`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1743:   134	(increments on every basket or customer mutation), `read_back_revision:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1744:   135	int | None` (set by `read_back`), `state`, `submit_attempted_at: int | None`
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1758:   149	Transition table (✓ legal, ✗ → typed error):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1763:   154	| remove_item | ✗ empty_basket | ✓ | ✓ | ✓ demote | ✗ order_closed |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1765:   156	| read_back | ✗ empty_basket | ✗ invalid_state (no customer yet) | ✓ | ✓ (same basket, idempotent) | ✗ order_closed |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1771:   162	(else `stale_revision`) and `read_back_revision == order.revision` (else
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1772:   163	`read_back_required`). So the only path into `CONFIRMED` is: state `READY`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1773:   164	`read_back` called at the current revision, then `confirm_order` naming that
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1784:   175	real retry. List endpoint itself fails → error `submit_unknown` with an
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1794:   185	`{state, revision, items: [{type, code, name, qty, extras}], customer:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1795:   186	{first_name, street_one} | null, read_back_done: bool}` — never a diff.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1799:   190	| `get_menu` | `{}` | `{"menu": {"pizzas": [{code, name}], "pasta": [{code, name}], "toppings": [str]}, "snapshot": SNAPSHOT}` — `name` is the API's single display name, which the verified contract facts show serves both languages |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1800:   191	| `add_items` | `{items: [{type: enum[pizza,pasta], code: str, qty: int ≥1, extras: [str]}]}` (required: items; extras default `[]`) | `{"snapshot": SNAPSHOT}` (basket + revision live in SNAPSHOT) |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1801:   192	| `remove_item` | `{type: enum, code: str, qty: int ≥1 optional}` (absent qty = remove all of that line) | `{"snapshot": SNAPSHOT}` |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1803:   194	| `read_back` | `{}` | `{"snapshot": SNAPSHOT}` — basket, customer, revision: the material the agent reads out |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1804:   195	| `confirm_order` | `{revision: int}` | `{"snapshot": SNAPSHOT}` with `state == "CONFIRMED"`, or error if stale |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1806:   197	| `check_street` | `{street: str}` | `{"street": str, "deliverable": bool, "snapshot": SNAPSHOT}` — the never-claim-verified rule lives in the prompt, not the tool |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1808:   199	Failure shape: `{"error": {"code": "<one of the codes below>", "message":
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1812:   203	candidate toppings), `invalid_quantity` (non-integer or < 1 — the tool does
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1814:   205	`read_back_required`, `order_closed`, `submit_failed`, `submit_unknown`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1815:   206	`api_unavailable`, `not_in_basket` (remove_item for a line that isn't there).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1818:   209	snapshot and every extra against `toppings[]`; any failure rejects the whole
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1819:   210	call atomically (no partial adds), returning the first error with candidates
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1828:   219	  `lang = PIZZERIA_LANG` — the pizzeria-country greeting language, a
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1831:   222	  language of the customer's latest message (German or English), unprompted.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1832:   223	  Language mirroring is model behaviour; the runtime never detects language.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1839:   230	  the plain apology from the error table. Gateway 4xx/5xx: no retry, abort
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1842:   233	  `tool_result`, `state`, `error` — the CLI prints them (verbose), the web
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1850:   241	`prompts/system.de.md` / `system.en.md`, same content in two languages, calm
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1852:   243	greet once in the file's language and offer help in one sentence; mirror the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1853:   244	customer's language per turn (German ↔ English); one question per turn; menu
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1855:   246	came from speech) and street, street declinable; read back via `read_back`
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1858:   249	state order id in speakable groups and ETA in minutes; errors in plain
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1859:   250	language, never codes or JSON; never claim the address was checked for
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1866:   257	  `SPEECH_URL` set and a probe succeeded at startup). No language field:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1867:   258	  language is never a UI control — the greeting comes from `PIZZERIA_LANG`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1872:No plan-sized findings. `PLAN.md` now closes the round-2 gaps with concrete plan text rather than hand-waving: the per-tool full-state contract is explicit via `SNAPSHOT` and the exact return table ([PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:183)), `PIZZERIA_LANG` is required and matches the oracle decision ([PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:96), [decisions/qa.md](/home/rob/bpm-pizza-vibecoding-solution/decisions/qa.md:10)), submit-timeout correlation is persisted as `submit_attempted_at` with verify-before-retry recovery ([PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:132)), the web contract removes any UI/chat language control and fences language use to the STT hint only ([PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:256)), and menu snapshot ownership is per-session and immutable ([PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:119)).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1874:As devil’s advocate, I looked for remaining spec mismatches in the confirmation path, timeout handling, speech path, and tool contracts. The few remaining risks are implementation-sensitive rather than missing-plan-sensitive: the plan specifies the required behavior, tests, and boundaries tightly enough that implementing exactly it should satisfy `SPEC.md`.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1879:error_handling: 5
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1887:No plan-sized findings. `PLAN.md` now closes the round-2 gaps with concrete plan text rather than hand-waving: the per-tool full-state contract is explicit via `SNAPSHOT` and the exact return table ([PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:183)), `PIZZERIA_LANG` is required and matches the oracle decision ([PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:96), [decisions/qa.md](/home/rob/bpm-pizza-vibecoding-solution/decisions/qa.md:10)), submit-timeout correlation is persisted as `submit_attempted_at` with verify-before-retry recovery ([PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:132)), the web contract removes any UI/chat language control and fences language use to the STT hint only ([PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:256)), and menu snapshot ownership is per-session and immutable ([PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:119)).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1889:As devil’s advocate, I looked for remaining spec mismatches in the confirmation path, timeout handling, speech path, and tool contracts. The few remaining risks are implementation-sensitive rather than missing-plan-sensitive: the plan specifies the required behavior, tests, and boundaries tightly enough that implementing exactly it should satisfy `SPEC.md`.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1894:error_handling: 5
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:23:error_handling: N
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:48:proxies the optional self-hosted speech service (STT/TTS). If SPEECH_URL is
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:78:    enabled only if SPEECH_URL is set, answers, and models are configured."""
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:81:        self.url = optional_env("SPEECH_URL")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:82:        self.stt_model = optional_env("SPEECH_STT_MODEL")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:83:        self.tts_model = optional_env("SPEECH_TTS_MODEL")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:84:        self.voice = optional_env("SPEECH_TTS_VOICE")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:102:        print(f"Configuration error: {exc}", file=sys.stderr)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:192:            "language": app.state.config.lang}  # STT hint only
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:246:`uvicorn` (web channel), `pytest` (tests), stdlib `difflib` (candidate
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:256:- Secrets never appear in logs, transcripts, errors, or the web UI.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:260:- No build-time model name anywhere in source, config, prompts, tests, docs.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:264:- Deterministic tests: no network, no LLM (one opt-in live smoke test).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:275:  menu.py      Immutable Menu snapshot (pizzas, pasta, toppings), one per
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:276:               session; (type, code) validation; extras validation;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:279:               submit_order, check_street; typed errors; timeouts;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:283:               {"error": {code, message, candidates}}.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:296:  system.de.md German system prompt (default deployment language).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:298:tests/
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:300:               list, 422 bodies, location).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:311:Deviation from the SPEC tree, documented: `tests/test_transcripts.py` and
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:321:| `core/agent.py` | `LITELLM_PIZZA_URL`, `LITELLM_PIZZA_KEY`, `LITELLM_PIZZA_MODEL_1`, `PIZZERIA_LANG` (all required; `LITELLM_PIZZA_MODEL_2` read but unused — single-model build) |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:323:| `channels/web.py` | `SPEECH_URL`, `SPEECH_STT_MODEL`, `SPEECH_TTS_MODEL`, `SPEECH_TTS_VOICE` (all optional; absence disables speech) |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:325:`PIZZERIA_LANG` ∈ {`de`, `en`} is the pizzeria-country greeting language.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:329:`decisions/qa.md`). It selects the system prompt file and the STT language
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:330:hint; it never overrides per-turn language mirroring.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:343:   404-pizzeria case from the error table → process refuses to start;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:361:Order fields: `items: list[Item(type, code, qty, extras)]`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:363:(increments on every basket or customer mutation), `read_back_revision:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:364:int | None` (set by `read_back`), `state`, `submit_attempted_at: int | None`
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:378:Transition table (✓ legal, ✗ → typed error):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:383:| remove_item | ✗ empty_basket | ✓ | ✓ | ✓ demote | ✗ order_closed |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:385:| read_back | ✗ empty_basket | ✗ invalid_state (no customer yet) | ✓ | ✓ (same basket, idempotent) | ✗ order_closed |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:391:(else `stale_revision`) and `read_back_revision == order.revision` (else
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:392:`read_back_required`). So the only path into `CONFIRMED` is: state `READY`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:393:`read_back` called at the current revision, then `confirm_order` naming that
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:406:exactly one real retry. List or detail call fails → error `submit_unknown`
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:418:`{state, revision, items: [{type, code, name, qty, extras}], customer:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:419:{first_name, street_one} | null, read_back_done: bool}` — never a diff.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:423:| `get_menu` | `{}` | `{"menu": {"pizzas": [{code, name}], "pasta": [{code, name}], "toppings": [str]}, "snapshot": SNAPSHOT}` — `name` is the API's single display name, which the verified contract facts show serves both languages |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:424:| `add_items` | `{items: [{type: enum[pizza,pasta], code: str, qty: int ≥1, extras: [str]}]}` (required: items; extras default `[]`) | `{"snapshot": SNAPSHOT}` (basket + revision live in SNAPSHOT) |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:425:| `remove_item` | `{type: enum, code: str, qty: int ≥1 optional}` — the spec fixes these params, so when several lines share (type, code) with different extras: absent qty removes **all** matching lines, qty reduces the **most recently added** matching line (deterministic; the snapshot lets the model repair by remove + re-add) | `{"snapshot": SNAPSHOT}` |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:427:| `read_back` | `{}` | `{"snapshot": SNAPSHOT}` — basket, customer, revision: the material the agent reads out |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:428:| `confirm_order` | `{revision: int}` | `{"snapshot": SNAPSHOT}` with `state == "CONFIRMED"`, or error if stale |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:430:| `check_street` | `{street: str}` | `{"street": str, "deliverable": bool, "snapshot": SNAPSHOT}` — the never-claim-verified rule lives in the prompt, not the tool |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:432:Failure shape: `{"error": {"code": "<one of the codes below>", "message":
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:436:candidate toppings), `invalid_quantity` (non-integer or < 1 — the tool does
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:438:`read_back_required`, `order_closed`, `submit_failed`, `submit_unknown`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:439:`api_unavailable`, `not_in_basket` (remove_item for a line that isn't there).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:442:snapshot and every extra against `toppings[]`; any failure rejects the whole
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:443:call atomically (no partial adds), returning the first error with candidates
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:484:-  `SPEECH_URL` set and a probe succeeded at startup). No language field:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:485:-  language is never a UI control — the greeting comes from `PIZZERIA_LANG`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:488:+  (`speech` true only if `SPEECH_URL` set and a probe succeeded at startup;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:490:+  see which pizzeria they are ordering at). No language field: language is
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:491:+  never a UI control — the greeting comes from `PIZZERIA_LANG`, mirroring
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:525:     if (speechEnabled) {           // unset SPEECH_URL → not rendered at all
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:647:  const details = document.createElement("details");
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:648:  details.className = "steps";
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:649:  details.innerHTML = "<summary>Zwischenschritte</summary>";
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:650:  chat.appendChild(details);
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:651:  return details;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:687:        } else if (ev.type === "error") {
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:770:    if (speechEnabled) {           // unset SPEECH_URL → not rendered at all
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:781:/bin/bash -lc "rg -n \"randomUUID|getRandomValues|mediaDevices|getUserMedia|MediaRecorder|Audio\\(|serviceWorker|Notification|clipboard|storage|indexedDB|geolocation|WebSocket|RTCPeerConnection|speechSynthesis|SpeechRecognition|crypto\\.subtle\" channels/static channels -g '"'!**/*.pyc'"'" in /home/rob/bpm-pizza-vibecoding-solution
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:851:  const details = document.createElement("details");
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:852:  details.className = "steps";
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:853:  details.innerHTML = "<summary>Zwischenschritte</summary>";
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:854:  chat.appendChild(details);
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:855:  return details;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:891:        } else if (ev.type === "error") {
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:969:    if (speechEnabled) {           // unset SPEECH_URL → not rendered at all
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:1075:    38	  const details = document.createElement("details");
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:1076:    39	  details.className = "steps";
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:1077:    40	  details.innerHTML = "<summary>Zwischenschritte</summary>";
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:1078:    41	  chat.appendChild(details);
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:1079:    42	  return details;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:1115:    78	        } else if (ev.type === "error") {
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:1198:   161	    if (speechEnabled) {           // unset SPEECH_URL → not rendered at all
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:1213:   261	  (`speech` true only if `SPEECH_URL` set and a probe succeeded at startup;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:1215:   263	  see which pizzeria they are ordering at). No language field: language is
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:1216:   264	  never a UI control — the greeting comes from `PIZZERIA_LANG`, mirroring
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:1223:   271	  `{SPEECH_URL}/v1/audio/transcriptions` with `SPEECH_STT_MODEL` and
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:1224:   272	  `PIZZERIA_LANG` as the language hint (an STT hint only — it never
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:1236:error_handling: 3
/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:1254:error_handling: 3
/home/rob/bpm-pizza-vibecoding-solution/tests/transcripts/happy_path.json:12:       {"tool": "add_items", "args": {"items": [{"type": "pizza", "code": "margherita", "qty": 2, "extras": []}]}},
/home/rob/bpm-pizza-vibecoding-solution/tests/transcripts/happy_path.json:18:       {"tool": "read_back", "args": {}},
/home/rob/bpm-pizza-vibecoding-solution/tests/transcripts/happy_path.json:30:    "calls": ["get_menu", "add_items", "set_customer", "read_back", "confirm_order", "submit_order"],
/home/rob/bpm-pizza-vibecoding-solution/tests/transcripts/happy_path.json:31:    "error_codes": [],
/home/rob/bpm-pizza-vibecoding-solution/tests/transcripts/submit_timeout.json:7:       {"tool": "add_items", "args": {"items": [{"type": "pizza", "code": "hawaii", "qty": 1, "extras": []}]}},
/home/rob/bpm-pizza-vibecoding-solution/tests/transcripts/submit_timeout.json:9:       {"tool": "read_back", "args": {}},
/home/rob/bpm-pizza-vibecoding-solution/tests/transcripts/submit_timeout.json:26:    "calls": ["add_items", "set_customer", "read_back", "confirm_order", "submit_order", "submit_order"],
/home/rob/bpm-pizza-vibecoding-solution/tests/transcripts/submit_timeout.json:27:    "error_codes": ["submit_unknown"],
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:14:1. Devil's advocate: attack the plan — gaps, wrong assumptions, missing error cases, spec violations.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:23:error_handling: N
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:46:> repo — code, tests, prompts, tickets — derives from it.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:91:**Core belief:** a language model is a great waiter and a terrible order pad.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:103:  tool error carrying candidate matches — never a silent guess, never a fallback
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:128:- **Languages:** German and English. The agent answers in the language the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:132:- **The success moment:** the order appears in the PizzaSim dashboard under the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:134:- **Deterministic tests** that run with no network and no LLM.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:172:- Secrets never appear in logs, transcripts, error messages or the web UI.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:183:| `GET /location?street=…` | public | street plausibility check |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:190:  "items": [{ "type": "pizza", "code": "margherita", "qty": 2, "extras": [] }]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:212:invalid bodies —, `GET /pizzerias/{id}/orders`, `GET /location`). Facts below
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:222:   `customer_id`, `created_at`, `ready_at`, `status`, `delivered_at`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:227:   there are no per-language names in the API; read-back uses `name` as-is in
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:228:   both languages. The menu response also carries a top-level `toppings[]`
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:230:4. **`extras[]` is a controlled vocabulary:** the top-level `toppings[]` from
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:232:   rejects unknown extras with `422` (`"items[0].extras contains invalid
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:233:   topping 'unicorn_dust'"`), so the tool layer validates extras against
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:234:   `toppings[]` exactly like item codes.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:236:   `{"error": "<code>", "details": ["<human sentence>", ...]}` — e.g.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:237:   `{"error": "validation_failed", "details": ["items[0].code must be a valid
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:238:   pizza code"]}` with HTTP 422. The tool layer maps `error` to typed errors
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:239:   and may surface `details` to targeted questions.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:241:   `prepared_planned` → `delivered` (with `delivered_at` set on the last).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:243:7. **`GET /location?street=` returns** `{"street": "<echo>",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:244:   "deliverable": <bool>}` with HTTP 200. In probing, even a nonsense street
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:245:   returned `deliverable: true` — the check is a weak plausibility signal at
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:261:                                                    │ read_back + customer says yes
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:268:Invariants, all enforced in code and all covered by unit tests:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:270:1. `submit_order` outside `CONFIRMED` returns an error. It does not "helpfully"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:275:   legal after `read_back` has been called for the current basket revision. The
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:289:| `get_menu` | — | pizzas and pasta with codes and display names in both languages |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:290:| `add_items` | `items[]` of `{type, code, qty, extras[]}` | new basket + revision |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:291:| `remove_item` | `code`, `type`, optional `qty` | new basket + revision |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:293:| `read_back` | — | basket, customer, revision — the text the agent must read out |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:294:| `confirm_order` | `revision` | state `CONFIRMED`, or error if stale |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:319:`uvicorn` (web channel), `pytest` (tests), stdlib `difflib` (candidate
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:329:- Secrets never appear in logs, transcripts, errors, or the web UI.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:333:- No build-time model name anywhere in source, config, prompts, tests, docs.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:337:- Deterministic tests: no network, no LLM (one opt-in live smoke test).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:348:  menu.py      Menu snapshot (pizzas, pasta, toppings) fetched once per
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:349:               session; (type, code) validation; extras validation;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:352:               submit_order, check_street; typed errors; timeouts;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:356:               {"error": {code, message, candidates}}.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:369:  system.de.md German system prompt (default deployment language).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:371:tests/
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:373:               list, 422 bodies, location).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:384:Deviation from the SPEC tree, documented: `tests/test_transcripts.py` and
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:396:| `channels/web.py` | `SPEECH_URL`, `SPEECH_STT_MODEL`, `SPEECH_TTS_MODEL`, `SPEECH_TTS_VOICE` (all optional; absence disables speech) |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:405:(404 → process refuses to start, per error table).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:411:Order fields: `items: list[Item(type, code, qty, extras)]`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:413:(increments on every basket or customer mutation), `read_back_revision:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:414:int | None` (set by `read_back`), `state`, `submit_unknown: bool` (a submit
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:426:Transition table (✓ legal, ✗ → typed error):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:431:| remove_item | ✗ empty_basket | ✓ | ✓ | ✓ demote | ✗ order_closed |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:433:| read_back | ✗ empty_basket | ✓ | ✓ | ✓ | ✗ order_closed |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:439:(else `stale_revision`) and `read_back_revision == order.revision` (else
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:440:`read_back_required`). Every ✗ cell gets a unit test (invariants 1–5).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:448:error `submit_unknown` with an honest message ("I'm not sure that went
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:457:| `get_menu` | `{}` | `{pizzas: [{code, name, ingredients, price}], pasta: [...], toppings: [...]}` |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:458:| `add_items` | `{items: [{type: enum[pizza,pasta], code: str, qty: int ≥1, extras: [str]}]}` (required: items; extras default `[]`) | snapshot |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:459:| `remove_item` | `{type: enum, code: str, qty: int ≥1 optional}` (absent qty = remove all of that line) | snapshot |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:461:| `read_back` | `{}` | snapshot + `read_back_text` (preformatted lines the agent reads out) |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:464:| `check_street` | `{street: str}` | `{street, deliverable}` + caveat text that this is a plausibility hint only |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:467:qty, extras}], customer: {first_name, street_one} | null, read_back_done:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:470:Failure shape: `{"error": {"code": "<one of the codes below>", "message":
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:474:candidate toppings), `invalid_quantity` (non-integer or < 1 — the tool does
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:476:`read_back_required`, `order_closed`, `submit_failed`, `submit_unknown`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:477:`api_unavailable`, `not_in_basket` (remove_item for a line that isn't there).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:480:snapshot and every extra against `toppings[]`; any failure rejects the whole
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:481:call atomically (no partial adds), returning the first error with candidates
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:490:  `GET /pizzerias`), where `lang` is the channel's default language
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:498:  the plain apology from the error table. Gateway 4xx/5xx: no retry, abort
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:501:  `tool_result`, `state`, `error` — the CLI prints them (verbose), the web
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:510:`prompts/system.de.md` / `system.en.md`, same content in two languages, calm
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:512:greet once in the file's language and offer help in one sentence; mirror the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:513:customer's language per turn (German ↔ English); one question per turn; menu
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:515:came from speech) and street, street declinable; read back via `read_back`
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:518:state order id in speakable groups and ETA in minutes; errors in plain
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:519:language, never codes or JSON; never claim the address was checked for
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:526:  (speech true only if `SPEECH_URL` set and a probe succeeded at startup).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:531:  `{SPEECH_URL}/v1/audio/transcriptions` with `SPEECH_STT_MODEL` and the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:532:  session language → `{text}`. `POST /speech/tts` body `{text}` forwarded to
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:533:  `{SPEECH_URL}/v1/audio/speech` with `SPEECH_TTS_MODEL` +
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:534:  `SPEECH_TTS_VOICE` → audio bytes. Proxying keeps the speech URL and
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:551:| 422 validation | typed `ValidationError(details)` → tool error `submit_failed` with field text, basket kept |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:651:  question, `SPEECH_URL` unset run).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:660:2. **Order + state machine + tests.** `core/order.py`, `core/state.py`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:661:   `tests/test_state.py`.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:666:   extras vocabulary ☐ ≤3 candidates.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:667:4. **PizzaSim client.** `core/pizzasim.py`, typed errors, timeouts,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:668:   fixtures for orders/422/location, httpx MockTransport tests.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:669:   ☐ every error class mapped ☐ no call without timeout ☐ submit returns
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:671:5. **Tools.** `core/tools.py` schemas + dispatch, `tests/test_tools.py`.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:672:   ☐ schemas match this plan exactly ☐ atomic add ☐ error shape uniform
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:685:   only ☐ `SPEECH_URL` unset → no mic, no speaker, text works ☐ speech
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:687:10. **Harden + docs.** Walk the SPEC error table end to end, README
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:689:    ☐ each error row demonstrably handled ☐ README covers all channels +
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:690:    speech + tests ☐ full suite green.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:692:Each ticket ≤ 1h, tests live in the ticket that introduces the behaviour.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:732:The agent can still run tests, stage files, and output suggested branch
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:737:- Failure: `{"error": {"code": "...", "message": "...", "candidates": [...]}}`.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:751:- Greet first, in the language of the pizzeria's country, and offer help — one
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:757:- Before submitting: call `read_back`, say it, and wait for an explicit yes.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:763:- On error, explain in plain language what happened and what the customer's
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:777:| STT | `POST {SPEECH_URL}/v1/audio/transcriptions` | multipart audio file + model + language |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:778:| TTS | `POST {SPEECH_URL}/v1/audio/speech` | JSON with model, voice, input text; returns audio |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:788:  model, TTS model, voice and language all come from the environment, exactly
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:793:  | `SPEECH_URL` | base URL of the self-hosted speech service |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:794:  | `SPEECH_STT_MODEL` | transcription model id |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:795:  | `SPEECH_TTS_MODEL` | synthesis model id |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:796:  | `SPEECH_TTS_VOICE` | voice id |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:807:- **Speech is never required.** If `SPEECH_URL` is unset or the service does not
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:813:- **Confirm the name.** Transcription errors on names are the expensive failure:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:875:  menu question — plus one run with `SPEECH_URL` unset, which must render a
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:902:  **none of this spec's business**. Nothing in the deliverables reads them,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:911:  source, config, prompts, tests or documentation.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:924:  wrong assumptions, missing error cases — and *judge*, scoring against the fixed
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:939:error_handling: N
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:960:   loop, error handling, conversation state. **No code.** Send it to the reviewer
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:977:1. **Core.** Order model, state machine, tool layer, tests. No LLM, no network.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:978:   Pass when the unit tests are green.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:980:3. **CLI.** Full conversation, real API, an order visible in the dashboard.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:983:6. **Harden.** Walk the error table, force each case, fix what breaks.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1016:   132	- Secrets never appear in logs, transcripts, error messages or the web UI.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1027:   143	| `GET /location?street=…` | public | street plausibility check |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1034:   150	  "items": [{ "type": "pizza", "code": "margherita", "qty": 2, "extras": [] }]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1056:   172	invalid bodies —, `GET /pizzerias/{id}/orders`, `GET /location`). Facts below
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1066:   182	   `customer_id`, `created_at`, `ready_at`, `status`, `delivered_at`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1071:   187	   there are no per-language names in the API; read-back uses `name` as-is in
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1072:   188	   both languages. The menu response also carries a top-level `toppings[]`
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1074:   190	4. **`extras[]` is a controlled vocabulary:** the top-level `toppings[]` from
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1076:   192	   rejects unknown extras with `422` (`"items[0].extras contains invalid
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1077:   193	   topping 'unicorn_dust'"`), so the tool layer validates extras against
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1078:   194	   `toppings[]` exactly like item codes.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1080:   196	   `{"error": "<code>", "details": ["<human sentence>", ...]}` — e.g.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1081:   197	   `{"error": "validation_failed", "details": ["items[0].code must be a valid
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1082:   198	   pizza code"]}` with HTTP 422. The tool layer maps `error` to typed errors
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1083:   199	   and may surface `details` to targeted questions.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1085:   201	   `prepared_planned` → `delivered` (with `delivered_at` set on the last).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1087:   203	7. **`GET /location?street=` returns** `{"street": "<echo>",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1088:   204	   "deliverable": <bool>}` with HTTP 200. In probing, even a nonsense street
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1089:   205	   returned `deliverable: true` — the check is a weak plausibility signal at
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1105:   221	                                                    │ read_back + customer says yes
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1112:   228	Invariants, all enforced in code and all covered by unit tests:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1114:   230	1. `submit_order` outside `CONFIRMED` returns an error. It does not "helpfully"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1119:   235	   legal after `read_back` has been called for the current basket revision. The
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1133:   249	| `get_menu` | — | pizzas and pasta with codes and display names in both languages |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1134:   250	| `add_items` | `items[]` of `{type, code, qty, extras[]}` | new basket + revision |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1135:   251	| `remove_item` | `code`, `type`, optional `qty` | new basket + revision |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1137:   253	| `read_back` | — | basket, customer, revision — the text the agent must read out |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1138:   254	| `confirm_order` | `revision` | state `CONFIRMED`, or error if stale |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1146:   262	- Failure: `{"error": {"code": "...", "message": "...", "candidates": [...]}}`.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1160:   276	- Greet first, in the language of the pizzeria's country, and offer help — one
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1166:   282	- Before submitting: call `read_back`, say it, and wait for an explicit yes.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1172:   288	- On error, explain in plain language what happened and what the customer's
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1186:   302	| STT | `POST {SPEECH_URL}/v1/audio/transcriptions` | multipart audio file + model + language |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1187:   303	| TTS | `POST {SPEECH_URL}/v1/audio/speech` | JSON with model, voice, input text; returns audio |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1197:   313	  model, TTS model, voice and language all come from the environment, exactly
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1202:   318	  | `SPEECH_URL` | base URL of the self-hosted speech service |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1203:   319	  | `SPEECH_STT_MODEL` | transcription model id |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1204:   320	  | `SPEECH_TTS_MODEL` | synthesis model id |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1205:   321	  | `SPEECH_TTS_VOICE` | voice id |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1216:   332	- **Speech is never required.** If `SPEECH_URL` is unset or the service does not
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1222:   338	- **Confirm the name.** Transcription errors on names are the expensive failure:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1284:   400	  menu question — plus one run with `SPEECH_URL` unset, which must render a
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1323:    17	`uvicorn` (web channel), `pytest` (tests), stdlib `difflib` (candidate
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1333:    27	- Secrets never appear in logs, transcripts, errors, or the web UI.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1337:    31	- No build-time model name anywhere in source, config, prompts, tests, docs.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1341:    35	- Deterministic tests: no network, no LLM (one opt-in live smoke test).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1352:    46	  menu.py      Menu snapshot (pizzas, pasta, toppings) fetched once per
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1353:    47	               session; (type, code) validation; extras validation;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1356:    50	               submit_order, check_street; typed errors; timeouts;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1360:    54	               {"error": {code, message, candidates}}.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1373:    67	  system.de.md German system prompt (default deployment language).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1375:    69	tests/
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1377:    71	               list, 422 bodies, location).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1388:    82	Deviation from the SPEC tree, documented: `tests/test_transcripts.py` and
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1400:    94	| `channels/web.py` | `SPEECH_URL`, `SPEECH_STT_MODEL`, `SPEECH_TTS_MODEL`, `SPEECH_TTS_VOICE` (all optional; absence disables speech) |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1409:   103	(404 → process refuses to start, per error table).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1415:   109	Order fields: `items: list[Item(type, code, qty, extras)]`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1417:   111	(increments on every basket or customer mutation), `read_back_revision:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1418:   112	int | None` (set by `read_back`), `state`, `submit_unknown: bool` (a submit
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1430:   124	Transition table (✓ legal, ✗ → typed error):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1435:   129	| remove_item | ✗ empty_basket | ✓ | ✓ | ✓ demote | ✗ order_closed |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1437:   131	| read_back | ✗ empty_basket | ✓ | ✓ | ✓ | ✗ order_closed |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1443:   137	(else `stale_revision`) and `read_back_revision == order.revision` (else
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1444:   138	`read_back_required`). Every ✗ cell gets a unit test (invariants 1–5).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1452:   146	error `submit_unknown` with an honest message ("I'm not sure that went
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1461:   155	| `get_menu` | `{}` | `{pizzas: [{code, name, ingredients, price}], pasta: [...], toppings: [...]}` |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1462:   156	| `add_items` | `{items: [{type: enum[pizza,pasta], code: str, qty: int ≥1, extras: [str]}]}` (required: items; extras default `[]`) | snapshot |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1463:   157	| `remove_item` | `{type: enum, code: str, qty: int ≥1 optional}` (absent qty = remove all of that line) | snapshot |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1465:   159	| `read_back` | `{}` | snapshot + `read_back_text` (preformatted lines the agent reads out) |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1468:   162	| `check_street` | `{street: str}` | `{street, deliverable}` + caveat text that this is a plausibility hint only |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1471:   165	qty, extras}], customer: {first_name, street_one} | null, read_back_done:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1474:   168	Failure shape: `{"error": {"code": "<one of the codes below>", "message":
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1478:   172	candidate toppings), `invalid_quantity` (non-integer or < 1 — the tool does
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1480:   174	`read_back_required`, `order_closed`, `submit_failed`, `submit_unknown`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1481:   175	`api_unavailable`, `not_in_basket` (remove_item for a line that isn't there).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1484:   178	snapshot and every extra against `toppings[]`; any failure rejects the whole
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1485:   179	call atomically (no partial adds), returning the first error with candidates
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1494:   188	  `GET /pizzerias`), where `lang` is the channel's default language
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1502:   196	  the plain apology from the error table. Gateway 4xx/5xx: no retry, abort
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1505:   199	  `tool_result`, `state`, `error` — the CLI prints them (verbose), the web
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1514:   208	`prompts/system.de.md` / `system.en.md`, same content in two languages, calm
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1516:   210	greet once in the file's language and offer help in one sentence; mirror the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1517:   211	customer's language per turn (German ↔ English); one question per turn; menu
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1519:   213	came from speech) and street, street declinable; read back via `read_back`
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1522:   216	state order id in speakable groups and ETA in minutes; errors in plain
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1523:   217	language, never codes or JSON; never claim the address was checked for
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1530:   224	  (speech true only if `SPEECH_URL` set and a probe succeeded at startup).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1535:   229	  `{SPEECH_URL}/v1/audio/transcriptions` with `SPEECH_STT_MODEL` and the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1536:   230	  session language → `{text}`. `POST /speech/tts` body `{text}` forwarded to
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1537:   231	  `{SPEECH_URL}/v1/audio/speech` with `SPEECH_TTS_MODEL` +
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1538:   232	  `SPEECH_TTS_VOICE` → audio bytes. Proxying keeps the speech URL and
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1555:   249	| 422 validation | typed `ValidationError(details)` → tool error `submit_failed` with field text, basket kept |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1569:One last check: I’m verifying the deliverables section to make sure the plan’s file layout doesn’t quietly drift from the required tree. Then I’ll finalize the rubric judgment.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1581:   528	│   ├── pizzasim.py          ← API client, typed errors, timeouts
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1591:   538	├── tests/
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1602:   549	## Decisions locked
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1617:   564	| Errors | Typed in code, plain language to the customer |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1626:   573	- Extras and modifiers beyond a passthrough `extras[]`.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1630:   577	- Additional languages beyond DE + EN.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1639:   586	  or by "schema / implementation / tests".
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1663:- The language strategy is not spec-safe. The plan chooses the system prompt from channel defaults and a web UI language toggle ([PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:186), [PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:223)), but the spec requires greeting first in the pizzeria-country language and then answering in the language the customer used on each turn, without being told to switch ([SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:276), [SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:559)). As written, the plan can produce the wrong first-turn language and makes language a UI control instead of runtime behavior.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1667:- The state-machine section weakens the confirmation path the spec is trying to lock down. It allows `read_back` in `COLLECTING` and `confirm_order` as a no-op in `CONFIRMED` ([PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:124)), while the spec’s only path into `CONFIRMED` is a current-basket read-back plus explicit customer yes from a complete order ([SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:217), [SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:234)). The plan should make the legal confirmation path unambiguous, not broader than the spec.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1672:error_handling: 4
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1678:- Remove non-spec config behavior: no `./.env` fallback, no extra config vars like `PIZZA_LOG_DIR`, and keep startup error text aligned to `~/.env`/environment only.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1680:- Redefine language handling so the first greeting comes from pizzeria-country context and every reply mirrors the user’s turn language; do not rely on CLI/UI language selection for core behavior.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1691:- The language strategy is not spec-safe. The plan chooses the system prompt from channel defaults and a web UI language toggle ([PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:186), [PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:223)), but the spec requires greeting first in the pizzeria-country language and then answering in the language the customer used on each turn, without being told to switch ([SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:276), [SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:559)). As written, the plan can produce the wrong first-turn language and makes language a UI control instead of runtime behavior.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1695:- The state-machine section weakens the confirmation path the spec is trying to lock down. It allows `read_back` in `COLLECTING` and `confirm_order` as a no-op in `CONFIRMED` ([PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:124)), while the spec’s only path into `CONFIRMED` is a current-basket read-back plus explicit customer yes from a complete order ([SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:217), [SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:234)). The plan should make the legal confirmation path unambiguous, not broader than the spec.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1700:error_handling: 4
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1706:- Remove non-spec config behavior: no `./.env` fallback, no extra config vars like `PIZZA_LOG_DIR`, and keep startup error text aligned to `~/.env`/environment only.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1708:- Redefine language handling so the first greeting comes from pizzeria-country context and every reply mirrors the user’s turn language; do not rely on CLI/UI language selection for core behavior.
/home/rob/bpm-pizza-vibecoding-solution/tests/transcripts/correction.json:7:       {"tool": "add_items", "args": {"items": [{"type": "pizza", "code": "margherita", "qty": 1, "extras": []}]}},
/home/rob/bpm-pizza-vibecoding-solution/tests/transcripts/correction.json:12:       {"tool": "add_items", "args": {"items": [{"type": "pizza", "code": "margherita", "qty": 2, "extras": []}]}},
/home/rob/bpm-pizza-vibecoding-solution/tests/transcripts/correction.json:18:       {"tool": "read_back", "args": {}},
/home/rob/bpm-pizza-vibecoding-solution/tests/transcripts/correction.json:30:    "calls": ["add_items", "add_items", "set_customer", "read_back", "confirm_order", "submit_order"],
/home/rob/bpm-pizza-vibecoding-solution/tests/transcripts/correction.json:31:    "error_codes": [],
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:14:1. Devil's advocate: attack the implementation — bugs, gaps, missing error cases, spec violations, divergence from the approved plan.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:17:Task: Review the IMPLEMENTATION (stage 2, round 2 of max 3) against SPEC.md (source of truth) and PLAN.md (the approved stage-1 plan; approved 24/25 in reviews/round3-plan.md, since updated only to document remove_item disambiguation semantics). Implementation: core/, channels/, prompts/, tests/, README.md, .env.example, requirements.txt.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:20:1. remove_item ambiguity with same (type, code) and different extras → deterministic semantics in core/state.py (no qty removes all matching lines; qty reduces the most recently added), documented in PLAN.md tool table, tested in tests/test_state.py (test_remove_without_qty_clears_all_variants, test_remove_with_qty_reduces_most_recent_variant). The spec fixes remove_item's parameters, so an extras parameter was not an option.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:25:Facts you cannot observe from the files, all demonstrated live: the deterministic suite passes (69 passed, 1 skipped opt-in live test); the web channel started with SPEECH_URL unset (speech:false, mic not rendered) and placed a real order end to end via the real gateway (read_back -> confirm_order(revision) -> submit_order -> order_id 3fe1deaa-... visible in the pizzeria's order list, ETA converted to minutes, id read in groups); a missing required env var exits before the first turn naming the variable and file. Your sandbox may lack a writable temp dir for pytest; judge from the code plus this evidence if so.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:27:Scope notes: tests/fixtures/*.json are recorded real API responses (UUIDs there are recorded data, not hardcoded config). venv/ and logs/ are gitignored runtime artifacts, out of scope.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:33:error_handling: N
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:43:I’m reviewing the implementation against `SPEC.md`, `PLAN.md`, and the round-1 review findings first, then I’ll inspect the implementation and tests to verify each claimed fix before scoring.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:157:The agent can still run tests, stage files, and output suggested branch
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:161:/bin/bash -lc "rg --files -g 'SPEC.md' -g 'PLAN.md' -g 'reviews/round3-plan.md' -g 'reviews/round4-impl.md' -g 'README.md' -g '.env.example' -g 'requirements.txt' -g 'core/**' -g 'channels/**' -g 'prompts/**' -g 'tests/**'" in /home/rob/bpm-pizza-vibecoding-solution
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:195:tests/test_transcripts.py
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:196:tests/test_tools.py
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:197:tests/test_state.py
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:198:tests/__init__.py
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:199:tests/__pycache__/test_tools.cpython-313-pytest-9.1.1.pyc
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:200:tests/__pycache__/__init__.cpython-313.pyc
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:201:tests/__pycache__/test_transcripts.cpython-313-pytest-9.1.1.pyc
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:202:tests/__pycache__/test_state.cpython-313-pytest-9.1.1.pyc
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:203:tests/transcripts/unknown_item.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:204:tests/transcripts/mind_change.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:205:tests/transcripts/submit_timeout.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:206:tests/transcripts/happy_path.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:207:tests/transcripts/correction.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:208:tests/fixtures/menu.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:209:tests/fixtures/order_created.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:210:tests/fixtures/pizzerias.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:211:tests/fixtures/orders_list.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:212:tests/fixtures/location.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:213:tests/fixtures/error_422.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:216:I have the review surface. Next I’m checking the spec, approved plan, and prior round findings side by side, then I’ll trace the implementation and tests for conformance and regressions.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:220:  • Inspect tests for coverage of required behavior, especially round-1 fixes and spec-critical flows
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:247:`uvicorn` (web channel), `pytest` (tests), stdlib `difflib` (candidate
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:257:- Secrets never appear in logs, transcripts, errors, or the web UI.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:261:- No build-time model name anywhere in source, config, prompts, tests, docs.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:265:- Deterministic tests: no network, no LLM (one opt-in live smoke test).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:276:  menu.py      Immutable Menu snapshot (pizzas, pasta, toppings), one per
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:277:               session; (type, code) validation; extras validation;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:280:               submit_order, check_street; typed errors; timeouts;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:284:               {"error": {code, message, candidates}}.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:297:  system.de.md German system prompt (default deployment language).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:299:tests/
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:301:               list, 422 bodies, location).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:312:Deviation from the SPEC tree, documented: `tests/test_transcripts.py` and
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:322:| `core/agent.py` | `LITELLM_PIZZA_URL`, `LITELLM_PIZZA_KEY`, `LITELLM_PIZZA_MODEL_1`, `PIZZERIA_LANG` (all required; `LITELLM_PIZZA_MODEL_2` read but unused — single-model build) |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:324:| `channels/web.py` | `SPEECH_URL`, `SPEECH_STT_MODEL`, `SPEECH_TTS_MODEL`, `SPEECH_TTS_VOICE` (all optional; absence disables speech) |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:326:`PIZZERIA_LANG` ∈ {`de`, `en`} is the pizzeria-country greeting language.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:330:`decisions/qa.md`). It selects the system prompt file and the STT language
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:331:hint; it never overrides per-turn language mirroring.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:344:   404-pizzeria case from the error table → process refuses to start;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:362:Order fields: `items: list[Item(type, code, qty, extras)]`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:364:(increments on every basket or customer mutation), `read_back_revision:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:365:int | None` (set by `read_back`), `state`, `submit_attempted_at: int | None`
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:379:Transition table (✓ legal, ✗ → typed error):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:384:| remove_item | ✗ empty_basket | ✓ | ✓ | ✓ demote | ✗ order_closed |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:386:| read_back | ✗ empty_basket | ✗ invalid_state (no customer yet) | ✓ | ✓ (same basket, idempotent) | ✗ order_closed |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:392:(else `stale_revision`) and `read_back_revision == order.revision` (else
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:393:`read_back_required`). So the only path into `CONFIRMED` is: state `READY`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:394:`read_back` called at the current revision, then `confirm_order` naming that
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:405:real retry. List endpoint itself fails → error `submit_unknown` with an
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:415:`{state, revision, items: [{type, code, name, qty, extras}], customer:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:416:{first_name, street_one} | null, read_back_done: bool}` — never a diff.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:420:| `get_menu` | `{}` | `{"menu": {"pizzas": [{code, name}], "pasta": [{code, name}], "toppings": [str]}, "snapshot": SNAPSHOT}` — `name` is the API's single display name, which the verified contract facts show serves both languages |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:421:| `add_items` | `{items: [{type: enum[pizza,pasta], code: str, qty: int ≥1, extras: [str]}]}` (required: items; extras default `[]`) | `{"snapshot": SNAPSHOT}` (basket + revision live in SNAPSHOT) |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:422:| `remove_item` | `{type: enum, code: str, qty: int ≥1 optional}` — the spec fixes these params, so when several lines share (type, code) with different extras: absent qty removes **all** matching lines, qty reduces the **most recently added** matching line (deterministic; the snapshot lets the model repair by remove + re-add) | `{"snapshot": SNAPSHOT}` |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:424:| `read_back` | `{}` | `{"snapshot": SNAPSHOT}` — basket, customer, revision: the material the agent reads out |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:425:| `confirm_order` | `{revision: int}` | `{"snapshot": SNAPSHOT}` with `state == "CONFIRMED"`, or error if stale |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:427:| `check_street` | `{street: str}` | `{"street": str, "deliverable": bool, "snapshot": SNAPSHOT}` — the never-claim-verified rule lives in the prompt, not the tool |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:429:Failure shape: `{"error": {"code": "<one of the codes below>", "message":
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:433:candidate toppings), `invalid_quantity` (non-integer or < 1 — the tool does
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:435:`read_back_required`, `order_closed`, `submit_failed`, `submit_unknown`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:436:`api_unavailable`, `not_in_basket` (remove_item for a line that isn't there).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:439:snapshot and every extra against `toppings[]`; any failure rejects the whole
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:440:call atomically (no partial adds), returning the first error with candidates
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:449:  `lang = PIZZERIA_LANG` — the pizzeria-country greeting language, a
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:452:  language of the customer's latest message (German or English), unprompted.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:453:  Language mirroring is model behaviour; the runtime never detects language.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:460:  the plain apology from the error table. Gateway 4xx/5xx: no retry, abort
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:463:  `tool_result`, `state`, `error` — the CLI prints them (verbose), the web
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:471:`prompts/system.de.md` / `system.en.md`, same content in two languages, calm
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:473:greet once in the file's language and offer help in one sentence; mirror the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:474:customer's language per turn (German ↔ English); one question per turn; menu
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:476:came from speech) and street, street declinable; read back via `read_back`
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:479:state order id in speakable groups and ETA in minutes; errors in plain
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:480:language, never codes or JSON; never claim the address was checked for
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:487:  `SPEECH_URL` set and a probe succeeded at startup). No language field:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:488:  language is never a UI control — the greeting comes from `PIZZERIA_LANG`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:493:  `{SPEECH_URL}/v1/audio/transcriptions` with `SPEECH_STT_MODEL` and
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:494:  `PIZZERIA_LANG` as the language hint (an STT hint only — it never
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:495:  influences assistant output language) → `{text}`. `POST /speech/tts` body `{text}` forwarded to
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:496:  `{SPEECH_URL}/v1/audio/speech` with `SPEECH_TTS_MODEL` +
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:497:  `SPEECH_TTS_VOICE` → audio bytes. Proxying keeps the speech URL and
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:514:| 422 validation | typed `ValidationError(details)` → tool error `submit_failed` with field text, basket kept |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:541:  question, `SPEECH_URL` unset run).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:548:   ☐ `.env.example` lists all 12 vars (incl. `PIZZERIA_LANG`), names only
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:558:> repo — code, tests, prompts, tickets — derives from it.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:603:**Core belief:** a language model is a great waiter and a terrible order pad.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:615:  tool error carrying candidate matches — never a silent guess, never a fallback
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:640:- **Languages:** German and English. The agent answers in the language the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:644:- **The success moment:** the order appears in the PizzaSim dashboard under the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:646:- **Deterministic tests** that run with no network and no LLM.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:684:- Secrets never appear in logs, transcripts, error messages or the web UI.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:695:| `GET /location?street=…` | public | street plausibility check |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:702:  "items": [{ "type": "pizza", "code": "margherita", "qty": 2, "extras": [] }]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:724:invalid bodies —, `GET /pizzerias/{id}/orders`, `GET /location`). Facts below
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:734:   `customer_id`, `created_at`, `ready_at`, `status`, `delivered_at`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:739:   there are no per-language names in the API; read-back uses `name` as-is in
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:740:   both languages. The menu response also carries a top-level `toppings[]`
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:742:4. **`extras[]` is a controlled vocabulary:** the top-level `toppings[]` from
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:744:   rejects unknown extras with `422` (`"items[0].extras contains invalid
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:745:   topping 'unicorn_dust'"`), so the tool layer validates extras against
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:746:   `toppings[]` exactly like item codes.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:748:   `{"error": "<code>", "details": ["<human sentence>", ...]}` — e.g.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:749:   `{"error": "validation_failed", "details": ["items[0].code must be a valid
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:750:   pizza code"]}` with HTTP 422. The tool layer maps `error` to typed errors
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:751:   and may surface `details` to targeted questions.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:753:   `prepared_planned` → `delivered` (with `delivered_at` set on the last).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:755:7. **`GET /location?street=` returns** `{"street": "<echo>",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:756:   "deliverable": <bool>}` with HTTP 200. In probing, even a nonsense street
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:757:   returned `deliverable: true` — the check is a weak plausibility signal at
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:773:                                                    │ read_back + customer says yes
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:780:Invariants, all enforced in code and all covered by unit tests:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:782:1. `submit_order` outside `CONFIRMED` returns an error. It does not "helpfully"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:787:   legal after `read_back` has been called for the current basket revision. The
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:801:| `get_menu` | — | pizzas and pasta with codes and display names in both languages |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:802:| `add_items` | `items[]` of `{type, code, qty, extras[]}` | new basket + revision |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:803:| `remove_item` | `code`, `type`, optional `qty` | new basket + revision |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:805:| `read_back` | — | basket, customer, revision — the text the agent must read out |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:806:| `confirm_order` | `revision` | state `CONFIRMED`, or error if stale |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:828:1. Devil's advocate: attack the plan — gaps, wrong assumptions, missing error cases, spec violations.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:831:Task: Read SPEC.md (the source of truth) and PLAN.md (the stage-1 implementation plan under review, round 3 of max 3). Judge whether PLAN.md is a complete, correct, spec-compliant plan such that implementing exactly it satisfies SPEC.md. The "Contract facts" section in SPEC.md was verified against the live API and is trustworthy. decisions/qa.md records an oracle decision on the greeting language (required env var PIZZERIA_LANG) taken between rounds.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:833:Round 2 (stateless, see reviews/round2-plan.md) required: (1) one exact tool-result contract per tool composing the per-tool table with the full-current-state rule, and fixing an eta_minutes test regression; (2) a spec-compliant, non-hardcoded, non-UI source for the greeting language; (3) explicit persisted state for submit-timeout recovery correlation; (4) removing lang from the chat contract or fencing it to an STT hint; (5) per-session immutable menu snapshot ownership. All five were addressed in the current PLAN.md — verify in the file, do not take this note on faith: see the SNAPSHOT definition in "Tool schemas", the PIZZERIA_LANG paragraph in "Configuration", submit_attempted_at in the state-machine section, the web protocol section, and the "Session model" paragraph.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:841:error_handling: N
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:876:1. Devil's advocate: attack the plan — gaps, wrong assumptions, missing error cases, spec violations.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:881:Context from round 1 (a previous stateless review): it required (a) no ./.env fallback and no extra config vars, (b) tool results matching the spec's fixed contract exactly, (c) greeting in the pizzeria-country language with per-turn mirroring not driven by UI controls, (d) one explicit startup sequence validating PIZZERIA_ID via GET /pizzerias, (e) a confirmation path no broader than the spec. All five were applied; verify they are actually resolved in the current PLAN.md rather than taking this note on faith.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:887:error_handling: N
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:974:> repo — code, tests, prompts, tickets — derives from it.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1019:**Core belief:** a language model is a great waiter and a terrible order pad.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1031:  tool error carrying candidate matches — never a silent guess, never a fallback
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1056:- **Languages:** German and English. The agent answers in the language the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1060:- **The success moment:** the order appears in the PizzaSim dashboard under the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1062:- **Deterministic tests** that run with no network and no LLM.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1090:1. Devil's advocate: attack the implementation — bugs, gaps, missing error cases, spec violations, divergence from the approved plan.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1093:Task: Review the IMPLEMENTATION (stage 2) against SPEC.md (source of truth) and PLAN.md (the approved stage-1 plan, 24/25 APPROVED in reviews/round3-plan.md). The implementation is: core/ (order, state, menu, pizzasim, tools, agent), channels/ (cli.py, web.py, static/), prompts/, tests/ (state, tools, transcripts + fixtures), README.md, .env.example, requirements.txt.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1095:Facts you cannot observe from the files, all demonstrated live before this review: the full deterministic suite passes (67 passed, 1 skipped opt-in live test); the web channel started with SPEECH_URL unset (speech:false, mic not rendered) and placed a real order end to end via the real gateway (read_back -> confirm_order(revision) -> submit_order -> order_id 3fe1deaa-... visible in the pizzeria's order list); a missing required env var exits before the first turn naming the variable and file. You may run the test suite yourself if your sandbox permits; otherwise judge from the code.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1097:Scope notes: tests/fixtures/*.json are recorded real API responses (UUIDs in them are recorded data, not hardcoded config). The venv/ and logs/ directories are gitignored runtime artifacts, out of scope.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1103:error_handling: N
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1222:The agent can still run tests, stage files, and output suggested branch
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1226:/bin/bash -lc "pwd && rg --files -g 'SPEC.md' -g 'PLAN.md' -g 'README.md' -g '.env.example' -g 'requirements.txt' -g 'reviews/**' -g 'core/**' -g 'channels/**' -g 'prompts/**' -g 'tests/**'" in /home/rob/bpm-pizza-vibecoding-solution
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1258:tests/__pycache__/test_tools.cpython-313-pytest-9.1.1.pyc
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1259:tests/__pycache__/__init__.cpython-313.pyc
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1260:tests/__pycache__/test_transcripts.cpython-313-pytest-9.1.1.pyc
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1261:tests/__pycache__/test_state.cpython-313-pytest-9.1.1.pyc
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1262:tests/__init__.py
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1263:tests/test_tools.py
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1264:tests/test_state.py
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1265:tests/test_transcripts.py
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1266:tests/fixtures/menu.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1267:tests/fixtures/order_created.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1268:tests/fixtures/pizzerias.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1269:tests/fixtures/orders_list.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1270:tests/fixtures/location.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1271:tests/fixtures/error_422.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1272:tests/transcripts/unknown_item.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1273:tests/transcripts/mind_change.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1274:tests/transcripts/submit_timeout.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1275:tests/transcripts/happy_path.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1276:tests/transcripts/correction.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1285:  • Inspect implementation files and tests against spec/plan requirements
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1295:> repo — code, tests, prompts, tickets — derives from it.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1340:  • Inspect tests for coverage of required behavior, especially round-1 fixes and spec-critical flows
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1355:/bin/bash -lc "sed -n '1,260p' tests/test_state.py" in /home/rob/bpm-pizza-vibecoding-solution
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1408:def remove_item(order: Order, type_: str, code: str, qty: int | None) -> None:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1409:    """The spec fixes remove_item's parameters to (type, code, qty), so a
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1410:    basket holding the same (type, code) with different extras needs
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1440:def read_back(order: Order) -> None:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1451:    order.read_back_revision = order.revision
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1471:    if order.read_back_revision != order.revision:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1473:            "read_back_required",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1503:{"error": {"code", "message", "candidates"}} with a speakable message.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1527:        "extras": {"type": "array", "items": {"type": "string"}},
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1535:                    "names, and the available extra toppings.",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1545:    {"name": "remove_item",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1563:    {"name": "read_back",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1593:def _error(code: str, message: str, candidates: list | None = None) -> dict:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1594:    return {"error": {"code": code, "message": message,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1615:        return _error(exc.code, exc.message, exc.candidates)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1617:        return _error(exc.code, exc.message)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1619:        return _error("api_unavailable",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1622:        return _error("api_unavailable",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1625:        return _error("api_unavailable",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1637:            extras = raw.get("extras") or []
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1638:            menu.validate_extras(extras)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1645:                extras=extras,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1648:            return _error("invalid_quantity", "What can I get you?")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1652:    if name == "remove_item":
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1654:        state.remove_item(order, args.get("type", ""), args.get("code", ""),
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1661:            return _error("invalid_state", "I still need a name.")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1667:    if name == "read_back":
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1668:        state.read_back(order)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1674:            return _error("stale_revision",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1685:                "deliverable": bool(result.get("deliverable")),
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1688:    return _error("unknown_tool", "Something went wrong on my side.")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1704:            return _error("submit_unknown", _UNSURE)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1726:              "extras": list(i.extras)} for i in order.items]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1730:        return _error("submit_failed",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1732:                      + "; ".join(exc.details))
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1734:        return _error("api_unavailable",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1738:        return _error("submit_unknown", _UNSURE)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1758:proxies the optional self-hosted speech service (STT/TTS). If SPEECH_URL is
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1788:    enabled only if SPEECH_URL is set, answers, and models are configured."""
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1791:        self.url = optional_env("SPEECH_URL")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1792:        self.stt_model = optional_env("SPEECH_STT_MODEL")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1793:        self.tts_model = optional_env("SPEECH_TTS_MODEL")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1794:        self.voice = optional_env("SPEECH_TTS_VOICE")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1812:        print(f"Configuration error: {exc}", file=sys.stderr)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1892:            "language": app.state.config.lang}  # STT hint only
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1969:    lang: str  # PIZZERIA_LANG: greeting language = pizzeria country
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1973:        lang = require_env("PIZZERIA_LANG").lower()
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1976:                "PIZZERIA_LANG must be 'de' or 'en', got something else"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2074:                event({"type": "error", "error": str(exc)})
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2113:        event({"type": "error", "error": "tool loop guard exceeded"})
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2137:def item(code="margherita", type_="pizza", qty=1, extras=None):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2139:                extras=extras or [])
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2152:    state.read_back(o)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2175:    state.read_back(o)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2197:    lambda o: state.remove_item(o, "pizza", "margherita", None),
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2199:    lambda o: state.read_back(o),
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2212:        state.remove_item(order_in(State.EMPTY), "pizza", "margherita", None)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2216:def test_read_back_empty():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2218:        state.read_back(order_in(State.EMPTY))
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2222:def test_read_back_collecting_needs_customer():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2224:        state.read_back(order_in(State.COLLECTING))
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2255:        state.remove_item(o, "pasta", "pesto", None)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2269:    state.remove_item(o, "pizza", "margherita", None)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2289:def test_confirm_without_read_back():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2293:    assert e.value.code == "read_back_required"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2298:    state.read_back(o)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2306:def test_read_back_of_old_revision_does_not_allow_confirm():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2308:    state.read_back(o)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2312:    assert e.value.code == "read_back_required"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2322:    state.remove_item(o, "pizza", "margherita", None)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2333:def test_same_code_different_extras_is_separate_line():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2336:    state.add_items(o, [item(qty=1, extras=["mushrooms"])])
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2343:    state.remove_item(o, "pizza", "margherita", 1)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2345:    state.remove_item(o, "pizza", "margherita", 5)  # >= qty removes line
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2352:    state.remove_item(o, "pizza", "margherita", None)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2362:    state.remove_item(o, "pasta", "tonno", None)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2367:    """Same (type, code), different extras: no-qty removal takes them all."""
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2369:    state.add_items(o, [item(qty=1), item(qty=1, extras=["mushrooms"])])
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2370:    state.remove_item(o, "pizza", "margherita", None)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2376:    state.add_items(o, [item(qty=2), item(qty=2, extras=["mushrooms"])])
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2377:    state.remove_item(o, "pizza", "margherita", 1)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2378:    assert [(i.extras, i.qty) for i in o.items] == \
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2390:/bin/bash -lc "sed -n '261,520p' tests/test_state.py" in /home/rob/bpm-pizza-vibecoding-solution
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2396:/bin/bash -lc "sed -n '1,260p' tests/test_transcripts.py" in /home/rob/bpm-pizza-vibecoding-solution
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2402:/bin/bash -lc "sed -n '1,260p' tests/test_tools.py" in /home/rob/bpm-pizza-vibecoding-solution
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2428:    extras: list[str] = field(default_factory=list)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2431:        return (self.type, self.code, tuple(sorted(self.extras)))
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2448:    read_back_revision: int | None = None
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2465:                    "extras": list(i.extras),
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2470:            "read_back_done": self.read_back_revision == self.revision,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2513:        print(f"Configuration error: {exc}", file=sys.stderr)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2609:        return {"street": street, "deliverable": True}
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2624:    calls, error_codes = [], []
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2629:        if event["type"] == "tool_result" and "error" in event["result"]:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2630:            error_codes.append(event["result"]["error"]["code"])
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2640:    assert error_codes == expect["error_codes"]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2674:"""Immutable menu snapshot: (type, code) validation, extras validation,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2695:        self.toppings: list[str] = list(payload.get("toppings", []))
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2703:            "toppings": self.toppings,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2732:    def validate_extras(self, extras: list[str]) -> None:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2733:        for extra in extras:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2734:            if extra not in self.toppings:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2738:                        extra.lower(), self.toppings, n=3, cutoff=0.5
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2777:"""PizzaSim API client: httpx, explicit timeouts, typed errors.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2822:    """Base for typed API errors."""
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2834:    def __init__(self, details: list[str]):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2835:        super().__init__("; ".join(details))
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2836:        self.details = details
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2854:            details = response.json().get("details", [])
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2856:            details = []
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2857:        raise ValidationError(details or ["invalid request"])
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2859:        raise ServerError(f"server error ({response.status_code})")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2922:        return self._request("GET", "/location", params={"street": street})
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2988:def test_extras_controlled_vocabulary(menu):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2989:    menu.validate_extras(["mushrooms", "pineapple"])  # ok
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2991:        menu.validate_extras(["unicorn_dust"])
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:2995:# --- pizzasim client typed errors (httpx MockTransport) -------------------
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3006:def test_auth_error_mapped():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3018:def test_422_mapped_with_details():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3021:            respond(422, fixture("error_422.json"))
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3023:    assert "valid pizza code" in e.value.details[0]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3059:    """Scripted stand-in for PizzaSim in dispatch tests."""
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3077:        return {"street": street, "deliverable": True}
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3097:    tools.dispatch(order, menu, fake, "read_back", {})
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3108:    assert result["menu"]["toppings"]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3115:    assert snap["customer"] is None and snap["read_back_done"] is False
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3118:def test_unknown_item_error_shape(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3122:    err = result["error"]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3136:    assert result["error"]["code"] == "unknown_item"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3147:        assert result["error"]["code"] == "invalid_quantity", bad
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3154:                                        "extras": ["unicorn_dust"]}]})
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3155:    assert result["error"]["code"] == "invalid_extra"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3160:    result = tools.dispatch(order, menu, fake, "remove_item",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3164:    result = tools.dispatch(order, menu, fake, "remove_item",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3179:def test_submit_outside_confirmed_is_tool_error(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3183:    assert result["error"]["code"] == "invalid_state"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3191:/bin/bash -lc "sed -n '261,520p' tests/test_tools.py" in /home/rob/bpm-pizza-vibecoding-solution
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3214:- From then on, answer each turn in the language of the customer's latest
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3221:- Before submitting: call `read_back`, say it out loud, and wait for an
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3228:- On errors, explain in plain language what happened and what the customer
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3235:When a tool reports an error, follow it: offer the suggested alternatives
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3257:- Vor dem Abschicken: rufe `read_back` auf, lies die Bestellung vor und
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3280:    assert result["error"]["code"] == "invalid_state"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3281:    assert result["error"]["message"] == "What can I get you?"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3288:    assert result["error"]["code"] == "submit_unknown"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3306:    assert result["error"]["code"] == "submit_unknown"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3310:                    "ready_at": 0, "status": "delivered"}]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3323:    assert result["error"]["code"] == "submit_unknown"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3332:    assert result["error"]["code"] == "submit_failed"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3333:    assert "valid pizza code" in result["error"]["message"]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3337:def test_auth_error_no_retry(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3341:    assert result["error"]["code"] == "api_unavailable"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3352:    tools.dispatch(order, menu, fake, "read_back", {})
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3373:    assert result["deliverable"] is True and "snapshot" in result
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3389:        ("read_back", {}),
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3392:        assert "error" not in result, result
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3395:    assert "error" not in result
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3463:  const details = document.createElement("details");
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3464:  details.className = "steps";
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3465:  details.innerHTML = "<summary>Zwischenschritte</summary>";
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3466:  chat.appendChild(details);
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3467:  return details;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3503:        } else if (ev.type === "error") {
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3583:    if (speechEnabled) {           // unset SPEECH_URL → not rendered at all
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3595:machine owned by the code; the model only turns customer language into tool
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3607:`.env.example` except the four `SPEECH_*` ones is required. The process
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3618:The agent greets first, in the language set by `PIZZERIA_LANG`, and answers
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3619:each turn in the language you used (German or English). End with Ctrl-D.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3634:Set `SPEECH_URL`, `SPEECH_STT_MODEL`, `SPEECH_TTS_MODEL` and
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3635:`SPEECH_TTS_VOICE` to a self-hosted OpenAI-compatible speech service. The
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3638:`SPEECH_URL` unset — or the service down at startup — mic and toggle are
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3643:question; and one run with `SPEECH_URL` unset placing an order as text.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3648:venv/bin/python -m pytest tests/            # deterministic: no network, no LLM
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3649:PIZZA_LIVE_TEST=1 venv/bin/python -m pytest tests/test_tools.py -k live
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3673:# Greeting language of the pizzeria's country: de or en
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3674:PIZZERIA_LANG=
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3677:SPEECH_URL=
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3678:SPEECH_STT_MODEL=
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3679:SPEECH_TTS_MODEL=
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3680:SPEECH_TTS_VOICE=
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3685:/bin/bash -lc 'cat tests/fixtures/orders_list.json' in /home/rob/bpm-pizza-vibecoding-solution
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3687:/bin/bash -lc 'cat tests/fixtures/menu.json' in /home/rob/bpm-pizza-vibecoding-solution
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3689:/bin/bash -lc 'cat tests/fixtures/pizzerias.json' in /home/rob/bpm-pizza-vibecoding-solution
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3691:/bin/bash -lc 'cat tests/fixtures/order_created.json' in /home/rob/bpm-pizza-vibecoding-solution
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3693:/bin/bash -lc 'for f in tests/transcripts/*.json; do echo "FILE:$f"; cat "$f"; done' in /home/rob/bpm-pizza-vibecoding-solution
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3702:   "status": "prepared_planned",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3703:   "delivered_at": null,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3711:   "status": "prepared_planned",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3712:   "delivered_at": null,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3720:   "status": "prepared_planned",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3721:   "delivered_at": null,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3729:   "status": "prepared_planned",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3730:   "delivered_at": null,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3738:   "status": "prepared_planned",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3739:   "delivered_at": null,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3749:{"toppings":["mozzarella","mushrooms","smoked_ham","salami","onions","garlic","pepperoni","pineapple","artichokes","basil","bell_pepper","tuna"],"pizzas":[{"code":"margherita","name":"Margherita","base":["dough","tomatoes","mozzarella","basil"],"price":8.5},{"code":"prosciutto","name":"Prosciutto","base":["dough","tomatoes","mozzarella","smoked_ham"],"price":9.5},{"code":"salami","name":"Salami","base":["dough","tomatoes","mozzarella","salami"],"price":9.5},{"code":"funghi","name":"Funghi","base":["dough","tomatoes","mozzarella","mushrooms"],"price":9},{"code":"regina","name":"Regina","base":["dough","tomatoes","mozzarella","smoked_ham","mushrooms"],"price":10.5},{"code":"mista","name":"Mista","base":["dough","tomatoes","mozzarella","salami","smoked_ham","mushrooms"],"price":11.5},{"code":"hawaii","name":"Hawaii","base":["dough","tomatoes","mozzarella","smoked_ham","pineapple"],"price":10},{"code":"tonno","name":"Tonno","base":["dough","tomatoes","mozzarella","tuna","onions"],"price":10.5},{"code":"papa","name":"Papa","base":["dough","tomatoes","mozzarella","tuna","onions","garlic"],"price":11},{"code":"diavolo","name":"Diavolo","base":["dough","tomatoes","mozzarella","salami","bell_pepper","pepperoni"],"price":11},{"code":"grandiosa","name":"Grandiosa","base":["dough","tomatoes","mozzarella","smoked_ham","salami","mushrooms","bell_pepper","artichokes","onions"],"price":13.5}],"pasta":[{"code":"aglioolio","name":"Pasta Aglio & Olio","base":["pasta","garlic","basil"],"price":9},{"code":"tonno","name":"Pasta Tonno","base":["pasta","tuna"],"price":8.5},{"code":"funghi","name":"Pasta Funghi","base":["pasta","mushrooms"],"price":8.5},{"code":"pesto","name":"Pasta Pesto","base":["pasta","pesto"],"price":8.5}]}
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3751:FILE:tests/transcripts/correction.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3758:       {"tool": "add_items", "args": {"items": [{"type": "pizza", "code": "margherita", "qty": 1, "extras": []}]}},
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3763:       {"tool": "add_items", "args": {"items": [{"type": "pizza", "code": "margherita", "qty": 2, "extras": []}]}},
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3769:       {"tool": "read_back", "args": {}},
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3781:    "calls": ["add_items", "add_items", "set_customer", "read_back", "confirm_order", "submit_order"],
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3782:    "error_codes": [],
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3786:FILE:tests/transcripts/happy_path.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3798:       {"tool": "add_items", "args": {"items": [{"type": "pizza", "code": "margherita", "qty": 2, "extras": []}]}},
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3804:       {"tool": "read_back", "args": {}},
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3816:    "calls": ["get_menu", "add_items", "set_customer", "read_back", "confirm_order", "submit_order"],
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3817:    "error_codes": [],
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3821:FILE:tests/transcripts/mind_change.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3823:  "name": "mind_change_after_read_back",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3828:       {"tool": "add_items", "args": {"items": [{"type": "pizza", "code": "diavolo", "qty": 1, "extras": []}]}},
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3830:       {"tool": "read_back", "args": {}},
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3835:       {"tool": "add_items", "args": {"items": [{"type": "pizza", "code": "funghi", "qty": 1, "extras": []}]}},
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3837:       {"tool": "read_back", "args": {}},
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3849:    "calls": ["add_items", "set_customer", "read_back", "add_items", "confirm_order", "read_back", "confirm_order", "submit_order"],
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3850:    "error_codes": ["stale_revision"],
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3854:FILE:tests/transcripts/submit_timeout.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3861:       {"tool": "add_items", "args": {"items": [{"type": "pizza", "code": "hawaii", "qty": 1, "extras": []}]}},
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3863:       {"tool": "read_back", "args": {}},
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3880:    "calls": ["add_items", "set_customer", "read_back", "confirm_order", "submit_order", "submit_order"],
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3881:    "error_codes": ["submit_unknown"],
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3886:FILE:tests/transcripts/unknown_item.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3893:       {"tool": "add_items", "args": {"items": [{"type": "pasta", "code": "bolognese", "qty": 1, "extras": []}]}},
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3898:       {"tool": "add_items", "args": {"items": [{"type": "pasta", "code": "funghi", "qty": 1, "extras": []}]}},
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3904:       {"tool": "read_back", "args": {}},
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3916:    "calls": ["add_items", "add_items", "set_customer", "read_back", "confirm_order", "submit_order"],
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3917:    "error_codes": ["unknown_item"],
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3938:     4	proxies the optional self-hosted speech service (STT/TTS). If SPEECH_URL is
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3968:    34	    enabled only if SPEECH_URL is set, answers, and models are configured."""
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3971:    37	        self.url = optional_env("SPEECH_URL")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3972:    38	        self.stt_model = optional_env("SPEECH_STT_MODEL")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3973:    39	        self.tts_model = optional_env("SPEECH_TTS_MODEL")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3974:    40	        self.voice = optional_env("SPEECH_TTS_VOICE")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:3992:    58	        print(f"Configuration error: {exc}", file=sys.stderr)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:4072:   138	            "language": app.state.config.lang}  # STT hint only
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:4161:    52	def remove_item(order: Order, type_: str, code: str, qty: int | None) -> None:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:4162:    53	    """The spec fixes remove_item's parameters to (type, code, qty), so a
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:4163:    54	    basket holding the same (type, code) with different extras needs
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:4193:    84	def read_back(order: Order) -> None:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:4204:    95	    order.read_back_revision = order.revision
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:4224:   115	    if order.read_back_revision != order.revision:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:4226:   117	            "read_back_required",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:4285:    33	  const details = document.createElement("details");
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:4286:    34	  details.className = "steps";
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:4287:    35	  details.innerHTML = "<summary>Zwischenschritte</summary>";
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:4288:    36	  chat.appendChild(details);
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:4289:    37	  return details;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:4325:    73	        } else if (ev.type === "error") {
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:4405:   153	    if (speechEnabled) {           // unset SPEECH_URL → not rendered at all
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:4453:    40	    lang: str  # PIZZERIA_LANG: greeting language = pizzeria country
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:4457:    44	        lang = require_env("PIZZERIA_LANG").lower()
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:4460:    47	                "PIZZERIA_LANG must be 'de' or 'en', got something else"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:4558:   145	                event({"type": "error", "error": str(exc)})
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:4597:   184	        event({"type": "error", "error": "tool loop guard exceeded"})
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:4621:- [core/agent.py](/home/rob/bpm-pizza-vibecoding-solution/core/agent.py:144), [channels/web.py](/home/rob/bpm-pizza-vibecoding-solution/channels/web.py:108), and [channels/static/app.js](/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js:70): on gateway failure or loop-guard exhaustion, `run_turn()` returns the apology text but emits only an `error` event, not an `assistant` event. The web transport streams only emitted events, and the UI renders final assistant text only from `assistant` events. In those error paths, the browser user gets a generic technical notice instead of the promised apology, and the JSONL log also misses the assistant’s final turn.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:4624:I verified the four round-1 required changes in the files: deterministic `remove_item` semantics and tests, 2xx-required speech probe, 30s gateway timeout, and exact dependency pins. I did not rerun `pytest` in this read-only sandbox; the verdict below is from code inspection plus the live evidence you provided.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:4629:error_handling: 3
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:4635:- Clear `submit_unknown` and `submit_attempted_at` on any basket/customer mutation that demotes the order, and add tests covering “timeout, mutate, reconfirm, submit again”.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:4645:- [core/agent.py](/home/rob/bpm-pizza-vibecoding-solution/core/agent.py:144), [channels/web.py](/home/rob/bpm-pizza-vibecoding-solution/channels/web.py:108), and [channels/static/app.js](/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js:70): on gateway failure or loop-guard exhaustion, `run_turn()` returns the apology text but emits only an `error` event, not an `assistant` event. The web transport streams only emitted events, and the UI renders final assistant text only from `assistant` events. In those error paths, the browser user gets a generic technical notice instead of the promised apology, and the JSONL log also misses the assistant’s final turn.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:4648:I verified the four round-1 required changes in the files: deterministic `remove_item` semantics and tests, 2xx-required speech probe, 30s gateway timeout, and exact dependency pins. I did not rerun `pytest` in this read-only sandbox; the verdict below is from code inspection plus the live evidence you provided.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:4653:error_handling: 3
/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:4659:- Clear `submit_unknown` and `submit_attempted_at` on any basket/customer mutation that demotes the order, and add tests covering “timeout, mutate, reconfirm, submit again”.
/home/rob/bpm-pizza-vibecoding-solution/prompts/system.en.md:12:- From then on, answer each turn in the language of the customer's latest
/home/rob/bpm-pizza-vibecoding-solution/prompts/system.en.md:19:- Before submitting: call `read_back`, say it out loud, and wait for an
/home/rob/bpm-pizza-vibecoding-solution/prompts/system.en.md:26:- On errors, explain in plain language what happened and what the customer
/home/rob/bpm-pizza-vibecoding-solution/prompts/system.en.md:33:When a tool reports an error, follow it: offer the suggested alternatives
/home/rob/bpm-pizza-vibecoding-solution/prompts/system.de.md:19:- Vor dem Abschicken: rufe `read_back` auf, lies die Bestellung vor und
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:19:A2 (language): lang moves from AgentConfig into Session (initial value = PIZZERIA_LANG, which stays the greeting-language default). The UI switch sets session.lang server-side; messages[0] (system prompt) is re-rendered in the new language in place — same policy text, history preserved, no stale prompt. Apologies and the STT hint read session.lang. No cross-session leakage because nothing language-related remains process-global.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:21:A3 (confirm control): the read_back tool result already streams the revision. The UI renders an explicit confirm button bound to that revision. Click -> POST /confirm {session_id, revision} -> ONE core entry point Agent.confirm_and_submit(session, revision, emit): it calls tools.dispatch("confirm_order", {revision}) and then tools.dispatch("submit_order") — the state machine still enforces read-back-bound revision (stale revision = error to the UI); the synthetic tool_calls + tool results are appended to the message history in OpenAI format so the model's context stays consistent; then one model call phrases the outcome to the customer. Customer action is explicit (a click, not a word); CONFIRMED is reachable only via confirm_order(revision); the transport owns zero logic (it forwards two identifiers to core). The CLI keeps the conversational yes -> model calls confirm_order path; both paths converge on the same dispatch.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:25:A5 (prices): canonical in core. Menu keeps price per (type, code); Item copies unit_price at add time from the immutable session menu; Order.snapshot() gains unit_price, line_total and basket_total computed in core only. get_menu result includes prices; read_back includes the total so the agent reads back exactly what the UI shows — one computation, two renderings. Extras: the API prices only base items (toppings carry no price), so the total is the sum of base prices and the UI labels extras as not separately priced — no invented figures, per spec.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:27:A6 (honesty about the web layer): conceded — the web layer is a substantial rewrite, not an additive patch, and the retrofit claim applies to the repo, not to app.js line counts. Survives: server-side NDJSON streaming, speech proxies + probe, per-session locking, startup checks, and in the client the stream reader, push-to-talk recorder and TTS playback as functions. New: header (name, selector with short UUIDs, dashboard link, language switch, start over), footer (APP_VERSION, full UUID, connection states, docs link), visible basket with total, confirm control, the no-message-unanswered invariant paths (done-event handling, stream-ended-without-answer notice, typed error notices with resend), UI i18n. The browser E2E harness (Playwright, already working on this host) is new work in BOTH scenarios, so it does not differentiate retrofit vs restart. What restart would additionally cost: rewriting core/state/tools/client/agent (approved, 71 tests) with fresh bug risk for zero spec gain, and losing the committed review trail.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:29:Also note: the implementer already restored the verified contract-facts section into SPEC.md v2 and probed the two new contract facts live (dashboard path /dashboard/pizzerias/{id} from the dashboard's own routing code; API docs at /swagger.html).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:127:The implementer claims: SPEC v1 was fully built and approved (reviews/round1..8, reviews/scores.md with plan approved 24/25 and implementation approved 24/25, hotfix approved 24/25); 71 deterministic tests exist and are self-consistent; core/ implements the state machine, tool dispatch, PizzaSim client with submit-timeout recovery; channels/cli.py and channels/web.py + static UI exist; decisions/qa.md records oracle decisions. Verify each claim against the files and git log. Report discrepancies bluntly.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:130:SPEC.md was just replaced by the operator with v2 (git show HEAD -- SPEC.md; previous version is SPEC_20260801.md and in git history). Delta: prices + basket total in scope; multi-pizzeria (customer-selectable in the UI, PIZZERIA_ID only preselects; basket never crosses tenants; fresh conversation on switch); APP_VERSION env shown in footer; an entirely new "The web channel" section (header: pizzeria name, selector from GET /pizzerias with short UUIDs, dashboard link per pizzeria, DE/EN language switch applied to replies and speech, start-over; footer: version, full UUID, connection state for API+gateway, API docs link; "no message ends unanswered" invariant; visible basket with total; read-back with an explicit confirm CONTROL; basket locked after submit); mandatory headless-browser E2E tests incl. three failure paths; getUserMedia/MediaRecorder now explicitly sanctioned.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:132:The implementer's position, which you must attack: RETROFIT the existing codebase (do not restart from scratch). Rationale: the unchanged spec sections (soul, load-bearing idea, state machine, tools, error handling, anti-patterns, speech service, CLI) are already built, reviewed and tested (71 tests); the delta is additive and concentrated in the web layer + a session-level tenancy generalization + price fields; a restart would rewrite identical core code with fresh bug risk and lose the review trail. Planned retrofit sketch: (a) core: menu carries prices, get_menu/read_back expose price + basket total; PizzaSim client instantiated per session for the session's pizzeria (preselected id validated at startup; selector list from GET /pizzerias); (b) web: new header/footer/basket UI per spec, confirm control wired as customer action, language switch selects prompt+STT language per session (PIZZERIA_LANG stays the startup default), APP_VERSION required env; (c) tests: extend unit/tool tests for prices+tenancy, add Playwright browser E2E incl. the three failure paths (Playwright already proven working on this host); (d) PLAN.md updated first, re-reviewed before implementation.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:134:Attack this: where does retrofit risk silently violating v2? Is any v1 architectural decision now invalid (e.g. one client per process, PIZZERIA_LANG required var vs the new UI language switch, /config contract)? Is the confirm-control design sound given "the transport owns no order logic" and "CONFIRMED only via confirm_order(revision)"? Would a restart actually be cheaper or safer anywhere? Ask your hardest questions (max 6, numbered) — the implementer will answer them in the next call before you give a verdict. If the audit in JOB 1 found discrepancies, include them as questions.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:274:The agent can still run tests, stage files, and output suggested branch
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:303:./tests/__init__.py
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:304:./tests/test_tools.py
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:305:./tests/test_state.py
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:306:./tests/test_transcripts.py
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:307:./tests/fixtures/menu.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:308:./tests/fixtures/order_created.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:309:./tests/fixtures/pizzerias.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:310:./tests/fixtures/orders_list.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:311:./tests/fixtures/location.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:312:./tests/fixtures/error_422.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:313:./tests/transcripts/unknown_item.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:314:./tests/transcripts/mind_change.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:315:./tests/transcripts/submit_timeout.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:316:./tests/transcripts/happy_path.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:317:./tests/transcripts/correction.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:339:* bb8a00c (HEAD -> main) New SPEC v2 (web channel section, multi-pizzeria, prices, APP_VERSION); restore verified contract facts + dashboard/docs paths
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:348:* 0ce98c6 Menu validation, PizzaSim client, tool dispatch + fixture tests
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:349:* f670920 Core order model + state machine, exhaustive unit tests
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:358:* 2a1827f Add pizzeria-specific dashboard link
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:379:> repo — code, tests, prompts, tickets — derives from it.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:424:**Core belief:** a language model is a great waiter and a terrible order pad.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:436:  tool error carrying candidate matches — never a silent guess, never a fallback
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:463:   dashboard for that pizzeria.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:498:- **Languages:** German and English. The agent answers in the language the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:506:- **The success moment:** the order appears in the PizzaSim dashboard under the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:508:- **Deterministic tests** that run with no network and no LLM.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:547:- Secrets never appear in logs, transcripts, error messages or the web UI.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:558:| `GET /location?street=…` | public | street plausibility check |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:565:  "items": [{ "type": "pizza", "code": "margherita", "qty": 2, "extras": [] }]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:588:`GET /pizzerias/{id}/orders/{order_id}`, `GET /location`, plus the dashboard
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:599:   `customer_id`, `created_at`, `ready_at`, `status`, `delivered_at`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:610:   there are no per-language names in the API; read-back uses `name` as-is in
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:611:   both languages. The menu response also carries a top-level `toppings[]`
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:613:4. **`extras[]` is a controlled vocabulary:** the top-level `toppings[]` from
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:615:   rejects unknown extras with `422` (`"items[0].extras contains invalid
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:616:   topping 'unicorn_dust'"`), so the tool layer validates extras against
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:617:   `toppings[]` exactly like item codes.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:619:   `{"error": "<code>", "details": ["<human sentence>", ...]}` — e.g.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:620:   `{"error": "validation_failed", "details": ["items[0].code must be a valid
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:621:   pizza code"]}` with HTTP 422. The tool layer maps `error` to typed errors
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:622:   and may surface `details` to targeted questions.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:624:   `prepared_planned` → `delivered` (with `delivered_at` set on the last).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:626:7. **`GET /location?street=` returns** `{"street": "<echo>",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:627:   "deliverable": <bool>}` with HTTP 200. In probing, even a nonsense street
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:628:   returned `deliverable: true` — the check is a weak plausibility signal at
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:631:8. **The pizzeria dashboard** lives at
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:632:   `{PIZZASIM_URL}/dashboard/pizzerias/{id}` (confirmed in the dashboard's
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:633:   own routing code); the overview is `{PIZZASIM_URL}/dashboard`. The
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:673:The agent can still run tests, stage files, and output suggested branch
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:692:proxies the optional self-hosted speech service (STT/TTS). If SPEECH_URL is
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:722:    enabled only if SPEECH_URL is set, answers, and models are configured."""
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:725:        self.url = optional_env("SPEECH_URL")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:726:        self.stt_model = optional_env("SPEECH_STT_MODEL")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:727:        self.tts_model = optional_env("SPEECH_TTS_MODEL")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:728:        self.voice = optional_env("SPEECH_TTS_VOICE")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:746:        print(f"Configuration error: {exc}", file=sys.stderr)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:836:            "language": app.state.config.lang}  # STT hint only
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:876:277:1. Devil's advocate: attack the plan — gaps, wrong assumptions, missing error cases, spec violations.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:880:498:1. Devil's advocate: attack the plan — gaps, wrong assumptions, missing error cases, spec violations.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:882:719:1. Devil's advocate: attack the plan — gaps, wrong assumptions, missing error cases, spec violations.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:884:767:1. Devil's advocate: attack the plan — gaps, wrong assumptions, missing error cases, spec violations.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:886:940:1. Devil's advocate: attack the implementation — bugs, gaps, missing error cases, spec violations, divergence from the approved plan.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:888:1161:1. Devil's advocate: attack the implementation — bugs, gaps, missing error cases, spec violations, divergence from the approved plan.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:890:1167:1. remove_item ambiguity with same (type, code) and different extras → deterministic semantics in core/state.py (no qty removes all matching lines; qty reduces the most recently added), documented in PLAN.md tool table, tested in tests/test_state.py (test_remove_without_qty_clears_all_variants, test_remove_with_qty_reduces_most_recent_variant). The spec fixes remove_item's parameters, so an extras parameter was not an option.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:894:1382:1. Devil's advocate: attack the implementation — bugs, gaps, missing error cases, spec violations.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:896:1388:1. Mutations clear submit_unknown/submit_attempted_at (core/state.py _recompute); tested in tests/test_tools.py::test_mutation_after_submit_timeout_clears_recovery_state.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:910:2933:4. **`extras[]` is a controlled vocabulary:** the top-level `toppings[]` from
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:914:6543:1. `channels/web.py` currently creates one app-wide `PizzaSim` client and one app-wide `Agent`, both bound to a single `PIZZERIA_ID`. How exactly will retrofit remove that singleton tenant assumption without smuggling tenant logic into the transport, and where will per-session `{pizzeria_id, pizzeria_name, menu, order, language}` live?
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:915:6544:2. `core/agent.py` bakes `PIZZERIA_LANG` into `AgentConfig.lang`, the system prompt is fixed at session creation, and even fallback apologies use that startup language. V2 requires a UI language switch that affects replies and STT/TTS per session. What is the migration path that avoids stale prompts, mixed-language error messages, and cross-session leakage?
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:920:6550:PRELIMINARY LEANING: RETROFIT | The core and review trail are worth preserving, but only if you first admit that tenant and language are no longer process-global and that the web contract needs a substantial redesign, not a cosmetic patch.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:922:6563:1. `channels/web.py` currently creates one app-wide `PizzaSim` client and one app-wide `Agent`, both bound to a single `PIZZERIA_ID`. How exactly will retrofit remove that singleton tenant assumption without smuggling tenant logic into the transport, and where will per-session `{pizzeria_id, pizzeria_name, menu, order, language}` live?
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:923:6564:2. `core/agent.py` bakes `PIZZERIA_LANG` into `AgentConfig.lang`, the system prompt is fixed at session creation, and even fallback apologies use that startup language. V2 requires a UI language switch that affects replies and STT/TTS per session. What is the migration path that avoids stale prompts, mixed-language error messages, and cross-session leakage?
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:928:6570:PRELIMINARY LEANING: RETROFIT | The core and review trail are worth preserving, but only if you first admit that tenant and language are no longer process-global and that the web contract needs a substantial redesign, not a cosmetic patch.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:934:{"error": {"code", "message", "candidates"}} with a speakable message.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:958:        "extras": {"type": "array", "items": {"type": "string"}},
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:966:                    "names, and the available extra toppings.",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:976:    {"name": "remove_item",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:994:    {"name": "read_back",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1024:def _error(code: str, message: str, candidates: list | None = None) -> dict:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1025:    return {"error": {"code": code, "message": message,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1046:        return _error(exc.code, exc.message, exc.candidates)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1048:        return _error(exc.code, exc.message)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1050:        return _error("api_unavailable",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1053:        return _error("api_unavailable",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1056:        return _error("api_unavailable",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1068:            extras = raw.get("extras") or []
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1069:            menu.validate_extras(extras)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1076:                extras=extras,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1079:            return _error("invalid_quantity", "What can I get you?")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1083:    if name == "remove_item":
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1085:        state.remove_item(order, args.get("type", ""), args.get("code", ""),
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1092:            return _error("invalid_state", "I still need a name.")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1098:    if name == "read_back":
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1099:        state.read_back(order)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1105:            return _error("stale_revision",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1116:                "deliverable": bool(result.get("deliverable")),
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1119:    return _error("unknown_tool", "Something went wrong on my side.")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1129:            (e["type"], e["code"], e["qty"], tuple(sorted(e["extras"])))
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1133:             "extras": list(i.extras)} for i in basket]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1148:            return _error("submit_unknown", _UNSURE)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1160:                return _error("submit_unknown", _UNSURE)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1175:              "extras": list(i.extras)} for i in order.items]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1179:        return _error("submit_failed",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1181:                      + "; ".join(exc.details))
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1183:        return _error("api_unavailable",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1187:        return _error("submit_unknown", _UNSURE)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1232:    lang: str  # PIZZERIA_LANG: greeting language = pizzeria country
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1236:        lang = require_env("PIZZERIA_LANG").lower()
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1239:                "PIZZERIA_LANG must be 'de' or 'en', got something else"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1337:                event({"type": "error", "error": str(exc)})
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1377:        event({"type": "error", "error": "tool loop guard exceeded"})
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1430:  const details = document.createElement("details");
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1431:  details.className = "steps";
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1432:  details.innerHTML = "<summary>Zwischenschritte</summary>";
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1433:  chat.appendChild(details);
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1434:  return details;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1470:        } else if (ev.type === "error") {
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1553:    speechEnabled = cfg.speech;    // unset SPEECH_URL → nothing rendered
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1563:The current code confirms the exact weak points I asked about: app-wide tenant/client, startup language in `AgentConfig`, and a thin web contract. I’m checking the order/menu/state shapes next so I can decide whether the proposed price and confirmation retrofits are actually coherent.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1573:/bin/bash -lc "sed -n '1,260p' tests/fixtures/menu.json" in /home/rob/bpm-pizza-vibecoding-solution
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1631:def remove_item(order: Order, type_: str, code: str, qty: int | None) -> None:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1632:    """The spec fixes remove_item's parameters to (type, code, qty), so a
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1633:    basket holding the same (type, code) with different extras needs
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1663:def read_back(order: Order) -> None:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1674:    order.read_back_revision = order.revision
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1694:    if order.read_back_revision != order.revision:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1696:            "read_back_required",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1723:"""Immutable menu snapshot: (type, code) validation, extras validation,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1744:        self.toppings: list[str] = list(payload.get("toppings", []))
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1752:            "toppings": self.toppings,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1781:    def validate_extras(self, extras: list[str]) -> None:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1782:        for extra in extras:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1783:            if extra not in self.toppings:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1787:                        extra.lower(), self.toppings, n=3, cutoff=0.5
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1826:"""PizzaSim API client: httpx, explicit timeouts, typed errors.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1871:    """Base for typed API errors."""
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1883:    def __init__(self, details: list[str]):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1884:        super().__init__("; ".join(details))
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1885:        self.details = details
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1903:            details = response.json().get("details", [])
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1905:            details = []
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1906:        raise ValidationError(details or ["invalid request"])
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1908:        raise ServerError(f"server error ({response.status_code})")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:1978:        return self._request("GET", "/location", params={"street": street})
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2002:    extras: list[str] = field(default_factory=list)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2005:        return (self.type, self.code, tuple(sorted(self.extras)))
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2022:    read_back_revision: int | None = None
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2039:                    "extras": list(i.extras),
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2044:            "read_back_done": self.read_back_revision == self.revision,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2048:{"toppings":["mozzarella","mushrooms","smoked_ham","salami","onions","garlic","pepperoni","pineapple","artichokes","basil","bell_pepper","tuna"],"pizzas":[{"code":"margherita","name":"Margherita","base":["dough","tomatoes","mozzarella","basil"],"price":8.5},{"code":"prosciutto","name":"Prosciutto","base":["dough","tomatoes","mozzarella","smoked_ham"],"price":9.5},{"code":"salami","name":"Salami","base":["dough","tomatoes","mozzarella","salami"],"price":9.5},{"code":"funghi","name":"Funghi","base":["dough","tomatoes","mozzarella","mushrooms"],"price":9},{"code":"regina","name":"Regina","base":["dough","tomatoes","mozzarella","smoked_ham","mushrooms"],"price":10.5},{"code":"mista","name":"Mista","base":["dough","tomatoes","mozzarella","salami","smoked_ham","mushrooms"],"price":11.5},{"code":"hawaii","name":"Hawaii","base":["dough","tomatoes","mozzarella","smoked_ham","pineapple"],"price":10},{"code":"tonno","name":"Tonno","base":["dough","tomatoes","mozzarella","tuna","onions"],"price":10.5},{"code":"papa","name":"Papa","base":["dough","tomatoes","mozzarella","tuna","onions","garlic"],"price":11},{"code":"diavolo","name":"Diavolo","base":["dough","tomatoes","mozzarella","salami","bell_pepper","pepperoni"],"price":11},{"code":"grandiosa","name":"Grandiosa","base":["dough","tomatoes","mozzarella","smoked_ham","salami","mushrooms","bell_pepper","artichokes","onions"],"price":13.5}],"pasta":[{"code":"aglioolio","name":"Pasta Aglio & Olio","base":["pasta","garlic","basil"],"price":9},{"code":"tonno","name":"Pasta Tonno","base":["pasta","tuna"],"price":8.5},{"code":"funghi","name":"Pasta Funghi","base":["pasta","mushrooms"],"price":8.5},{"code":"pesto","name":"Pasta Pesto","base":["pasta","pesto"],"price":8.5}]}
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2050:There’s one possible fault line left: whether `PIZZERIA_LANG` even survives in v2, because the new env table appears to drop it while still requiring a per-session switch. I’m verifying that before I hand down the verdict.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2052:/bin/bash -lc 'rg -n "PIZZERIA_LANG|language switch|Languages:|greeting-language" SPEC.md SPEC_20260801.md PLAN.md README.md reviews/round9-audit-grill.md' in /home/rob/bpm-pizza-vibecoding-solution
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2054:/bin/bash -lc 'rg -n "confirm_order|read_back|/config|done event|resend|connection state|APP_VERSION|dashboard|pizzerias" channels/static/index.html channels/static/style.css channels/static/app.js channels/web.py core/agent.py core/tools.py core/order.py' in /home/rob/bpm-pizza-vibecoding-solution
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2056:reviews/round9-audit-grill.md:19:SPEC.md was just replaced by the operator with v2 (git show HEAD -- SPEC.md; previous version is SPEC_20260801.md and in git history). Delta: prices + basket total in scope; multi-pizzeria (customer-selectable in the UI, PIZZERIA_ID only preselects; basket never crosses tenants; fresh conversation on switch); APP_VERSION env shown in footer; an entirely new "The web channel" section (header: pizzeria name, selector from GET /pizzerias with short UUIDs, dashboard link per pizzeria, DE/EN language switch applied to replies and speech, start-over; footer: version, full UUID, connection state for API+gateway, API docs link; "no message ends unanswered" invariant; visible basket with total; read-back with an explicit confirm CONTROL; basket locked after submit); mandatory headless-browser E2E tests incl. three failure paths; getUserMedia/MediaRecorder now explicitly sanctioned.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2057:reviews/round9-audit-grill.md:21:The implementer's position, which you must attack: RETROFIT the existing codebase (do not restart from scratch). Rationale: the unchanged spec sections (soul, load-bearing idea, state machine, tools, error handling, anti-patterns, speech service, CLI) are already built, reviewed and tested (71 tests); the delta is additive and concentrated in the web layer + a session-level tenancy generalization + price fields; a restart would rewrite identical core code with fresh bug risk and lose the review trail. Planned retrofit sketch: (a) core: menu carries prices, get_menu/read_back expose price + basket total; PizzaSim client instantiated per session for the session's pizzeria (preselected id validated at startup; selector list from GET /pizzerias); (b) web: new header/footer/basket UI per spec, confirm control wired as customer action, language switch selects prompt+STT language per session (PIZZERIA_LANG stays the startup default), APP_VERSION required env; (c) tests: extend unit/tool tests for prices+tenancy, add Playwright browser E2E incl. the three failure paths (Playwright already proven working on this host); (d) PLAN.md updated first, re-reviewed before implementation.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2058:reviews/round9-audit-grill.md:23:Attack this: where does retrofit risk silently violating v2? Is any v1 architectural decision now invalid (e.g. one client per process, PIZZERIA_LANG required var vs the new UI language switch, /config contract)? Is the confirm-control design sound given "the transport owns no order logic" and "CONFIRMED only via confirm_order(revision)"? Would a restart actually be cheaper or safer anywhere? Ask your hardest questions (max 6, numbered) — the implementer will answer them in the next call before you give a verdict. If the audit in JOB 1 found discrepancies, include them as questions.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2059:reviews/round9-audit-grill.md:391:- **Languages:** German and English. The agent answers in the language the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2060:reviews/round9-audit-grill.md:678:- **Languages:** German and English. The agent answers in the language the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2061:reviews/round9-audit-grill.md:722:Task: Read SPEC.md (the source of truth) and PLAN.md (the stage-1 implementation plan under review, round 3 of max 3). Judge whether PLAN.md is a complete, correct, spec-compliant plan such that implementing exactly it satisfies SPEC.md. The "Contract facts" section in SPEC.md was verified against the live API and is trustworthy. decisions/qa.md records an oracle decision on the greeting language (required env var PIZZERIA_LANG) taken between rounds.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2062:reviews/round9-audit-grill.md:724:Round 2 (stateless, see reviews/round2-plan.md) required: (1) one exact tool-result contract per tool composing the per-tool table with the full-current-state rule, and fixing an eta_minutes test regression; (2) a spec-compliant, non-hardcoded, non-UI source for the greeting language; (3) explicit persisted state for submit-timeout recovery correlation; (4) removing lang from the chat contract or fencing it to an STT hint; (5) per-session immutable menu snapshot ownership. All five were addressed in the current PLAN.md — verify in the file, do not take this note on faith: see the SNAPSHOT definition in "Tool schemas", the PIZZERIA_LANG paragraph in "Configuration", submit_attempted_at in the state-machine section, the web protocol section, and the "Session model" paragraph.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2063:reviews/round9-audit-grill.md:2038:Which mechanism: (a) optional env `PIZZERIA_LANG` default de, (b) required
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2064:reviews/round9-audit-grill.md:2041:**A (decision):** **(b)** — `PIZZERIA_LANG` (de|en) is a required env var.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2065:reviews/round9-audit-grill.md:2044:before the first turn naming `PIZZERIA_LANG` and where it was expected; no
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2066:reviews/round9-audit-grill.md:2138:| `core/agent.py` | `LITELLM_PIZZA_URL`, `LITELLM_PIZZA_KEY`, `LITELLM_PIZZA_MODEL_1`, `PIZZERIA_LANG` (all required; `LITELLM_PIZZA_MODEL_2` read but unused — single-model build) |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2067:reviews/round9-audit-grill.md:2142:`PIZZERIA_LANG` ∈ {`de`, `en`} is the pizzeria-country greeting language.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2068:reviews/round9-audit-grill.md:2294:The agent greets first, in the language set by `PIZZERIA_LANG`, and answers
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2069:reviews/round9-audit-grill.md:2366:greeting language now required env var PIZZERIA_LANG (oracle decision in
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2070:reviews/round9-audit-grill.md:2369:hint = PIZZERIA_LANG only; per-session immutable menu snapshot defined via
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2071:reviews/round9-audit-grill.md:2475: - **Languages:** German and English. The agent answers in the language the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2072:reviews/round9-audit-grill.md:2826:- **Languages:** German and English. The agent answers in the language the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2073:reviews/round9-audit-grill.md:3970:    40	    lang: str  # PIZZERIA_LANG: greeting language = pizzeria country
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2074:reviews/round9-audit-grill.md:3974:    44	        lang = require_env("PIZZERIA_LANG").lower()
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2075:reviews/round9-audit-grill.md:3977:    47	                "PIZZERIA_LANG must be 'de' or 'en', got something else"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2076:reviews/round9-audit-grill.md:5468:    40	    lang: str  # PIZZERIA_LANG: greeting language = pizzeria country
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2077:reviews/round9-audit-grill.md:5472:    44	        lang = require_env("PIZZERIA_LANG").lower()
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2078:reviews/round9-audit-grill.md:5475:    47	                "PIZZERIA_LANG must be 'de' or 'en', got something else"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2079:reviews/round9-audit-grill.md:6536:- The claimed artifacts exist. `core/` contains the state machine, tool dispatcher, PizzaSim client, and timeout-recovery path in [core/state.py](/home/rob/bpm-pizza-vibecoding-solution/core/state.py), [core/tools.py](/home/rob/bpm-pizza-vibecoding-solution/core/tools.py), [core/pizzasim.py](/home/rob/bpm-pizza-vibecoding-solution/core/pizzasim.py), and [core/agent.py](/home/rob/bpm-pizza-vibecoding-solution/core/agent.py). `channels/cli.py`, `channels/web.py`, and the static web UI files exist. [decisions/qa.md](/home/rob/bpm-pizza-vibecoding-solution/decisions/qa.md) exists and records the `PIZZERIA_LANG` oracle decision.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2080:reviews/round9-audit-grill.md:6544:2. `core/agent.py` bakes `PIZZERIA_LANG` into `AgentConfig.lang`, the system prompt is fixed at session creation, and even fallback apologies use that startup language. V2 requires a UI language switch that affects replies and STT/TTS per session. What is the migration path that avoids stale prompts, mixed-language error messages, and cross-session leakage?
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2081:reviews/round9-audit-grill.md:6556:- The claimed artifacts exist. `core/` contains the state machine, tool dispatcher, PizzaSim client, and timeout-recovery path in [core/state.py](/home/rob/bpm-pizza-vibecoding-solution/core/state.py), [core/tools.py](/home/rob/bpm-pizza-vibecoding-solution/core/tools.py), [core/pizzasim.py](/home/rob/bpm-pizza-vibecoding-solution/core/pizzasim.py), and [core/agent.py](/home/rob/bpm-pizza-vibecoding-solution/core/agent.py). `channels/cli.py`, `channels/web.py`, and the static web UI files exist. [decisions/qa.md](/home/rob/bpm-pizza-vibecoding-solution/decisions/qa.md) exists and records the `PIZZERIA_LANG` oracle decision.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2082:reviews/round9-audit-grill.md:6564:2. `core/agent.py` bakes `PIZZERIA_LANG` into `AgentConfig.lang`, the system prompt is fixed at session creation, and even fallback apologies use that startup language. V2 requires a UI language switch that affects replies and STT/TTS per session. What is the migration path that avoids stale prompts, mixed-language error messages, and cross-session leakage?
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2083:README.md:27:The agent greets first, in the language set by `PIZZERIA_LANG`, and answers
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2084:SPEC_20260801.md:125:- **Languages:** German and English. The agent answers in the language the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2085:SPEC.md:125:- **Languages:** German and English. The agent answers in the language the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2086:PLAN.md:92:| `core/agent.py` | `LITELLM_PIZZA_URL`, `LITELLM_PIZZA_KEY`, `LITELLM_PIZZA_MODEL_1`, `PIZZERIA_LANG` (all required; `LITELLM_PIZZA_MODEL_2` read but unused — single-model build) |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2087:PLAN.md:96:`PIZZERIA_LANG` ∈ {`de`, `en`} is the pizzeria-country greeting language.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2088:PLAN.md:223:  `lang = PIZZERIA_LANG` — the pizzeria-country greeting language, a
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2089:PLAN.md:264:  never a UI control — the greeting comes from `PIZZERIA_LANG`, mirroring
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2090:PLAN.md:272:  `PIZZERIA_LANG` as the language hint (an STT hint only — it never
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2091:PLAN.md:330:   ☐ `.env.example` lists all 12 vars (incl. `PIZZERIA_LANG`), names only
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2094:core/tools.py:64:    {"name": "read_back",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2097:core/tools.py:168:    if name == "read_back":
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2098:core/tools.py:169:        state.read_back(order)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2102:core/order.py:42:    read_back_revision: int | None = None
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2103:core/order.py:64:            "read_back_done": self.read_back_revision == self.revision,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2108:- A2 is not acceptable as stated unless `PIZZERIA_LANG` is explicitly restored to `SPEC.md` and the config contract; v2’s current env table omits it, so retrofit cannot keep a hidden required env var or undocumented default.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2112:- Price and basket-total computation must be canonical in core only, copied into item snapshots at add time, surfaced through tool results/read-back, and covered by deterministic unit tests plus Playwright E2E for tenant switching and the three required failure paths.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2117:- A2 is not acceptable as stated unless `PIZZERIA_LANG` is explicitly restored to `SPEC.md` and the config contract; v2’s current env table omits it, so retrofit cannot keep a hidden required env var or undocumented default.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:2121:- Price and basket-total computation must be canonical in core only, copied into item snapshots at add time, surfaced through tool results/read-back, and covered by deterministic unit tests plus Playwright E2E for tenant switching and the three required failure paths.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:14:1. Devil's advocate: attack the implementation — bugs, gaps, missing error cases, spec violations.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:17:Task: Review the IMPLEMENTATION (stage 2, round 3 of max 3) against SPEC.md (source of truth — note it now contains the operator-added "What done looks like" acceptance section) and PLAN.md (approved stage-1 plan, updated alongside). Implementation: core/, channels/, prompts/, tests/, README.md, .env.example, requirements.txt.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:20:1. Mutations clear submit_unknown/submit_attempted_at (core/state.py _recompute); tested in tests/test_tools.py::test_mutation_after_submit_timeout_clears_recovery_state.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:24:Additionally, per the updated SPEC: submit-timeout recovery now verifies the shortlisted candidate's items via GET /pizzerias/{id}/orders/{order_id} before adopting it (core/tools.py, tests test_recovery_rejects_candidate_with_different_items), and the opt-in live test is now the full acceptance test (tests/test_tools.py::test_live_acceptance) asserting order id, presence in the pizzeria's list, exact customer name, and exact items/quantities.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:26:Facts you cannot observe from the files, all demonstrated live: deterministic suite passes (71 passed, 1 skipped); the live acceptance test PASSED against the real API (real order, read back via list + detail endpoints, exact match); the web channel with SPEECH_URL unset reported speech:false and placed a real order end to end via the real gateway (order 3fe1deaa-... under the configured pizzeria with exactly the read-back items — independently confirmed via the detail endpoint); a missing required env var exits before the first turn naming the variable and file. Your sandbox may lack a writable temp dir for pytest; judge from code plus this evidence if so.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:28:Scope notes: tests/fixtures/*.json are recorded real API responses (UUIDs there are recorded data, not hardcoded config). venv/ and logs/ are gitignored runtime artifacts, out of scope. decisions/qa.md records oracle decisions.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:36:error_handling: N
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:48:/bin/bash -lc "rg --files /home/rob/bpm-pizza-vibecoding-solution | rg '"'^(SPEC'"\\.md|PLAN\\.md|README\\.md|requirements\\.txt|\\.env\\.example|core/|channels/|prompts/|tests/|decisions/qa\\.md)'" in /home/rob/bpm-pizza-vibecoding-solution
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:158:The agent can still run tests, stage files, and output suggested branch
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:162:/bin/bash -lc "rg --files . | rg '"'^(SPEC'"\\.md|PLAN\\.md|README\\.md|requirements\\.txt|\\.env\\.example|core/|channels/|prompts/|tests/|decisions/qa\\.md)'" in /home/rob/bpm-pizza-vibecoding-solution
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:180:> repo — code, tests, prompts, tickets — derives from it.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:225:**Core belief:** a language model is a great waiter and a terrible order pad.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:237:  tool error carrying candidate matches — never a silent guess, never a fallback
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:264:   dashboard for that pizzeria.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:299:- **Languages:** German and English. The agent answers in the language the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:303:- **The success moment:** the order appears in the PizzaSim dashboard under the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:305:- **Deterministic tests** that run with no network and no LLM.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:343:- Secrets never appear in logs, transcripts, error messages or the web UI.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:354:| `GET /location?street=…` | public | street plausibility check |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:361:  "items": [{ "type": "pizza", "code": "margherita", "qty": 2, "extras": [] }]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:384:`GET /pizzerias/{id}/orders/{order_id}`, `GET /location`). Facts below are
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:394:   `customer_id`, `created_at`, `ready_at`, `status`, `delivered_at`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:403:   there are no per-language names in the API; read-back uses `name` as-is in
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:404:   both languages. The menu response also carries a top-level `toppings[]`
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:406:4. **`extras[]` is a controlled vocabulary:** the top-level `toppings[]` from
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:408:   rejects unknown extras with `422` (`"items[0].extras contains invalid
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:409:   topping 'unicorn_dust'"`), so the tool layer validates extras against
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:410:   `toppings[]` exactly like item codes.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:412:   `{"error": "<code>", "details": ["<human sentence>", ...]}` — e.g.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:413:   `{"error": "validation_failed", "details": ["items[0].code must be a valid
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:414:   pizza code"]}` with HTTP 422. The tool layer maps `error` to typed errors
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:415:   and may surface `details` to targeted questions.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:417:   `prepared_planned` → `delivered` (with `delivered_at` set on the last).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:419:7. **`GET /location?street=` returns** `{"street": "<echo>",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:420:   "deliverable": <bool>}` with HTTP 200. In probing, even a nonsense street
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:421:   returned `deliverable: true` — the check is a weak plausibility signal at
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:439:## 2026-07-31 — Greeting language source
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:441:**Q:** SPEC requires greeting in the pizzeria-country language; the live API
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:443:Which mechanism: (a) optional env `PIZZERIA_LANG` default de, (b) required
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:446:**A (decision):** **(b)** — `PIZZERIA_LANG` (de|en) is a required env var.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:449:before the first turn naming `PIZZERIA_LANG` and where it was expected; no
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:469:`uvicorn` (web channel), `pytest` (tests), stdlib `difflib` (candidate
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:479:- Secrets never appear in logs, transcripts, errors, or the web UI.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:483:- No build-time model name anywhere in source, config, prompts, tests, docs.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:487:- Deterministic tests: no network, no LLM (one opt-in live smoke test).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:498:  menu.py      Immutable Menu snapshot (pizzas, pasta, toppings), one per
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:499:               session; (type, code) validation; extras validation;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:502:               submit_order, check_street; typed errors; timeouts;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:506:               {"error": {code, message, candidates}}.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:519:  system.de.md German system prompt (default deployment language).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:521:tests/
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:523:               list, 422 bodies, location).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:534:Deviation from the SPEC tree, documented: `tests/test_transcripts.py` and
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:544:| `core/agent.py` | `LITELLM_PIZZA_URL`, `LITELLM_PIZZA_KEY`, `LITELLM_PIZZA_MODEL_1`, `PIZZERIA_LANG` (all required; `LITELLM_PIZZA_MODEL_2` read but unused — single-model build) |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:546:| `channels/web.py` | `SPEECH_URL`, `SPEECH_STT_MODEL`, `SPEECH_TTS_MODEL`, `SPEECH_TTS_VOICE` (all optional; absence disables speech) |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:548:`PIZZERIA_LANG` ∈ {`de`, `en`} is the pizzeria-country greeting language.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:552:`decisions/qa.md`). It selects the system prompt file and the STT language
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:553:hint; it never overrides per-turn language mirroring.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:566:   404-pizzeria case from the error table → process refuses to start;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:584:Order fields: `items: list[Item(type, code, qty, extras)]`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:586:(increments on every basket or customer mutation), `read_back_revision:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:587:int | None` (set by `read_back`), `state`, `submit_attempted_at: int | None`
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:601:Transition table (✓ legal, ✗ → typed error):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:606:| remove_item | ✗ empty_basket | ✓ | ✓ | ✓ demote | ✗ order_closed |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:608:| read_back | ✗ empty_basket | ✗ invalid_state (no customer yet) | ✓ | ✓ (same basket, idempotent) | ✗ order_closed |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:614:(else `stale_revision`) and `read_back_revision == order.revision` (else
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:615:`read_back_required`). So the only path into `CONFIRMED` is: state `READY`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:616:`read_back` called at the current revision, then `confirm_order` naming that
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:629:exactly one real retry. List or detail call fails → error `submit_unknown`
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:641:`{state, revision, items: [{type, code, name, qty, extras}], customer:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:642:{first_name, street_one} | null, read_back_done: bool}` — never a diff.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:646:| `get_menu` | `{}` | `{"menu": {"pizzas": [{code, name}], "pasta": [{code, name}], "toppings": [str]}, "snapshot": SNAPSHOT}` — `name` is the API's single display name, which the verified contract facts show serves both languages |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:647:| `add_items` | `{items: [{type: enum[pizza,pasta], code: str, qty: int ≥1, extras: [str]}]}` (required: items; extras default `[]`) | `{"snapshot": SNAPSHOT}` (basket + revision live in SNAPSHOT) |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:648:| `remove_item` | `{type: enum, code: str, qty: int ≥1 optional}` — the spec fixes these params, so when several lines share (type, code) with different extras: absent qty removes **all** matching lines, qty reduces the **most recently added** matching line (deterministic; the snapshot lets the model repair by remove + re-add) | `{"snapshot": SNAPSHOT}` |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:650:| `read_back` | `{}` | `{"snapshot": SNAPSHOT}` — basket, customer, revision: the material the agent reads out |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:651:| `confirm_order` | `{revision: int}` | `{"snapshot": SNAPSHOT}` with `state == "CONFIRMED"`, or error if stale |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:653:| `check_street` | `{street: str}` | `{"street": str, "deliverable": bool, "snapshot": SNAPSHOT}` — the never-claim-verified rule lives in the prompt, not the tool |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:655:Failure shape: `{"error": {"code": "<one of the codes below>", "message":
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:659:candidate toppings), `invalid_quantity` (non-integer or < 1 — the tool does
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:661:`read_back_required`, `order_closed`, `submit_failed`, `submit_unknown`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:662:`api_unavailable`, `not_in_basket` (remove_item for a line that isn't there).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:665:snapshot and every extra against `toppings[]`; any failure rejects the whole
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:666:call atomically (no partial adds), returning the first error with candidates
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:675:  `lang = PIZZERIA_LANG` — the pizzeria-country greeting language, a
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:678:  language of the customer's latest message (German or English), unprompted.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:679:  Language mirroring is model behaviour; the runtime never detects language.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:686:  the plain apology from the error table. Gateway 4xx/5xx: no retry, abort
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:689:  `tool_result`, `state`, `error` — the CLI prints them (verbose), the web
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:697:`prompts/system.de.md` / `system.en.md`, same content in two languages, calm
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:699:greet once in the file's language and offer help in one sentence; mirror the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:700:customer's language per turn (German ↔ English); one question per turn; menu
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:702:came from speech) and street, street declinable; read back via `read_back`
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:705:state order id in speakable groups and ETA in minutes; errors in plain
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:706:language, never codes or JSON; never claim the address was checked for
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:735:./tests/__init__.py
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:736:./tests/test_tools.py
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:737:./tests/test_state.py
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:738:./tests/test_transcripts.py
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:739:./tests/fixtures/menu.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:740:./tests/fixtures/order_created.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:741:./tests/fixtures/pizzerias.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:742:./tests/fixtures/orders_list.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:743:./tests/fixtures/location.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:744:./tests/fixtures/error_422.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:745:./tests/transcripts/submit_timeout.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:746:./tests/transcripts/mind_change.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:747:./tests/transcripts/unknown_item.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:754:./tests/transcripts/happy_path.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:755:./tests/transcripts/correction.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:770:/bin/bash -lc "sed -n '1,280p' tests/test_tools.py" in /home/rob/bpm-pizza-vibecoding-solution
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:775:{"error": {"code", "message", "candidates"}} with a speakable message.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:799:        "extras": {"type": "array", "items": {"type": "string"}},
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:807:                    "names, and the available extra toppings.",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:817:    {"name": "remove_item",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:835:    {"name": "read_back",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:865:def _error(code: str, message: str, candidates: list | None = None) -> dict:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:866:    return {"error": {"code": code, "message": message,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:887:        return _error(exc.code, exc.message, exc.candidates)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:889:        return _error(exc.code, exc.message)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:891:        return _error("api_unavailable",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:894:        return _error("api_unavailable",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:897:        return _error("api_unavailable",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:909:            extras = raw.get("extras") or []
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:910:            menu.validate_extras(extras)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:917:                extras=extras,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:920:            return _error("invalid_quantity", "What can I get you?")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:924:    if name == "remove_item":
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:926:        state.remove_item(order, args.get("type", ""), args.get("code", ""),
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:933:            return _error("invalid_state", "I still need a name.")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:939:    if name == "read_back":
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:940:        state.read_back(order)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:946:            return _error("stale_revision",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:957:                "deliverable": bool(result.get("deliverable")),
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:960:    return _error("unknown_tool", "Something went wrong on my side.")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:970:            (e["type"], e["code"], e["qty"], tuple(sorted(e["extras"])))
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:974:             "extras": list(i.extras)} for i in basket]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:989:            return _error("submit_unknown", _UNSURE)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1001:                return _error("submit_unknown", _UNSURE)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1016:              "extras": list(i.extras)} for i in order.items]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1020:        return _error("submit_failed",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1022:                      + "; ".join(exc.details))
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1024:        return _error("api_unavailable",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1028:        return _error("submit_unknown", _UNSURE)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1041:proxies the optional self-hosted speech service (STT/TTS). If SPEECH_URL is
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1071:    enabled only if SPEECH_URL is set, answers, and models are configured."""
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1074:        self.url = optional_env("SPEECH_URL")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1075:        self.stt_model = optional_env("SPEECH_STT_MODEL")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1076:        self.tts_model = optional_env("SPEECH_TTS_MODEL")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1077:        self.voice = optional_env("SPEECH_TTS_VOICE")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1095:        print(f"Configuration error: {exc}", file=sys.stderr)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1182:            "language": app.state.config.lang}  # STT hint only
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1276:def remove_item(order: Order, type_: str, code: str, qty: int | None) -> None:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1277:    """The spec fixes remove_item's parameters to (type, code, qty), so a
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1278:    basket holding the same (type, code) with different extras needs
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1308:def read_back(order: Order) -> None:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1319:    order.read_back_revision = order.revision
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1339:    if order.read_back_revision != order.revision:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1341:            "read_back_required",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1407:    lang: str  # PIZZERIA_LANG: greeting language = pizzeria country
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1411:        lang = require_env("PIZZERIA_LANG").lower()
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1414:                "PIZZERIA_LANG must be 'de' or 'en', got something else"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1512:                event({"type": "error", "error": str(exc)})
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1552:        event({"type": "error", "error": "tool loop guard exceeded"})
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1631:def test_extras_controlled_vocabulary(menu):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1632:    menu.validate_extras(["mushrooms", "pineapple"])  # ok
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1634:        menu.validate_extras(["unicorn_dust"])
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1638:# --- pizzasim client typed errors (httpx MockTransport) -------------------
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1649:def test_auth_error_mapped():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1661:def test_422_mapped_with_details():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1664:            respond(422, fixture("error_422.json"))
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1666:    assert "valid pizza code" in e.value.details[0]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1702:    """Scripted stand-in for PizzaSim in dispatch tests."""
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1709:        self.order_details = {}  # id -> detail payload
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1723:        if order_id not in self.order_details:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1725:        return self.order_details[order_id]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1728:        return {"street": street, "deliverable": True}
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1748:    tools.dispatch(order, menu, fake, "read_back", {})
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1759:    assert result["menu"]["toppings"]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1766:    assert snap["customer"] is None and snap["read_back_done"] is False
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1769:def test_unknown_item_error_shape(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1773:    err = result["error"]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1787:    assert result["error"]["code"] == "unknown_item"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1798:        assert result["error"]["code"] == "invalid_quantity", bad
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1805:                                        "extras": ["unicorn_dust"]}]})
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1806:    assert result["error"]["code"] == "invalid_extra"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1811:    result = tools.dispatch(order, menu, fake, "remove_item",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1815:    result = tools.dispatch(order, menu, fake, "remove_item",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1830:def test_submit_outside_confirmed_is_tool_error(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1834:    assert result["error"]["code"] == "invalid_state"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1840:    assert result["error"]["code"] == "invalid_state"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1841:    assert result["error"]["message"] == "What can I get you?"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1850:/bin/bash -lc "sed -n '281,520p' tests/test_tools.py" in /home/rob/bpm-pizza-vibecoding-solution
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1852:    assert result["error"]["code"] == "submit_unknown"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1860:    fake.order_details["recovered-1"] = {
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1864:                   "extras": []}],
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1882:    fake.order_details["other-1"] = {
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1885:                   "extras": []}],
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1907:    tools.dispatch(order, menu, fake, "read_back", {})
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1925:    assert result["error"]["code"] == "submit_unknown"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1929:                    "ready_at": 0, "status": "delivered"}]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1942:    assert result["error"]["code"] == "submit_unknown"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1951:    assert result["error"]["code"] == "submit_failed"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1952:    assert "valid pizza code" in result["error"]["message"]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1956:def test_auth_error_no_retry(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1960:    assert result["error"]["code"] == "api_unavailable"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1971:    tools.dispatch(order, menu, fake, "read_back", {})
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:1992:    assert result["deliverable"] is True and "snapshot" in result
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2012:        ("read_back", {}),
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2015:        assert "error" not in result, result
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2018:    assert "error" not in result, result
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2039:/bin/bash -lc "sed -n '1,260p' tests/test_state.py" in /home/rob/bpm-pizza-vibecoding-solution
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2045:/bin/bash -lc "sed -n '1,280p' tests/test_transcripts.py" in /home/rob/bpm-pizza-vibecoding-solution
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2068:    extras: list[str] = field(default_factory=list)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2071:        return (self.type, self.code, tuple(sorted(self.extras)))
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2088:    read_back_revision: int | None = None
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2105:                    "extras": list(i.extras),
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2110:            "read_back_done": self.read_back_revision == self.revision,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2123:def item(code="margherita", type_="pizza", qty=1, extras=None):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2125:                extras=extras or [])
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2138:    state.read_back(o)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2161:    state.read_back(o)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2183:    lambda o: state.remove_item(o, "pizza", "margherita", None),
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2185:    lambda o: state.read_back(o),
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2198:        state.remove_item(order_in(State.EMPTY), "pizza", "margherita", None)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2202:def test_read_back_empty():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2204:        state.read_back(order_in(State.EMPTY))
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2208:def test_read_back_collecting_needs_customer():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2210:        state.read_back(order_in(State.COLLECTING))
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2241:        state.remove_item(o, "pasta", "pesto", None)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2255:    state.remove_item(o, "pizza", "margherita", None)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2275:def test_confirm_without_read_back():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2279:    assert e.value.code == "read_back_required"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2284:    state.read_back(o)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2292:def test_read_back_of_old_revision_does_not_allow_confirm():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2294:    state.read_back(o)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2298:    assert e.value.code == "read_back_required"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2308:    state.remove_item(o, "pizza", "margherita", None)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2319:def test_same_code_different_extras_is_separate_line():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2322:    state.add_items(o, [item(qty=1, extras=["mushrooms"])])
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2329:    state.remove_item(o, "pizza", "margherita", 1)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2331:    state.remove_item(o, "pizza", "margherita", 5)  # >= qty removes line
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2338:    state.remove_item(o, "pizza", "margherita", None)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2348:    state.remove_item(o, "pasta", "tonno", None)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2353:    """Same (type, code), different extras: no-qty removal takes them all."""
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2355:    state.add_items(o, [item(qty=1), item(qty=1, extras=["mushrooms"])])
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2356:    state.remove_item(o, "pizza", "margherita", None)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2362:    state.add_items(o, [item(qty=2), item(qty=2, extras=["mushrooms"])])
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2363:    state.remove_item(o, "pizza", "margherita", 1)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2364:    assert [(i.extras, i.qty) for i in o.items] == \
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2450:        return {"street": street, "deliverable": True}
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2465:    calls, error_codes = [], []
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2470:        if event["type"] == "tool_result" and "error" in event["result"]:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2471:            error_codes.append(event["result"]["error"]["code"])
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2481:    assert error_codes == expect["error_codes"]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2515:"""PizzaSim API client: httpx, explicit timeouts, typed errors.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2560:    """Base for typed API errors."""
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2572:    def __init__(self, details: list[str]):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2573:        super().__init__("; ".join(details))
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2574:        self.details = details
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2592:            details = response.json().get("details", [])
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2594:            details = []
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2595:        raise ValidationError(details or ["invalid request"])
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2597:        raise ServerError(f"server error ({response.status_code})")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2667:        return self._request("GET", "/location", params={"street": street})
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2670:"""Immutable menu snapshot: (type, code) validation, extras validation,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2691:        self.toppings: list[str] = list(payload.get("toppings", []))
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2699:            "toppings": self.toppings,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2728:    def validate_extras(self, extras: list[str]) -> None:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2729:        for extra in extras:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2730:            if extra not in self.toppings:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2734:                        extra.lower(), self.toppings, n=3, cutoff=0.5
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2773:/bin/bash -lc "sed -n '261,380p' tests/test_state.py" in /home/rob/bpm-pizza-vibecoding-solution
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2803:- From then on, answer each turn in the language of the customer's latest
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2810:- Before submitting: call `read_back`, say it out loud, and wait for an
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2817:- On errors, explain in plain language what happened and what the customer
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2824:When a tool reports an error, follow it: offer the suggested alternatives
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2838:machine owned by the code; the model only turns customer language into tool
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2850:`.env.example` except the four `SPEECH_*` ones is required. The process
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2861:The agent greets first, in the language set by `PIZZERIA_LANG`, and answers
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2862:each turn in the language you used (German or English). End with Ctrl-D.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2877:Set `SPEECH_URL`, `SPEECH_STT_MODEL`, `SPEECH_TTS_MODEL` and
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2878:`SPEECH_TTS_VOICE` to a self-hosted OpenAI-compatible speech service. The
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2881:`SPEECH_URL` unset — or the service down at startup — mic and toggle are
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2886:question; and one run with `SPEECH_URL` unset placing an order as text.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2891:venv/bin/python -m pytest tests/            # deterministic: no network, no LLM
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2892:PIZZA_LIVE_TEST=1 venv/bin/python -m pytest tests/test_tools.py -k live
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2942:        print(f"Configuration error: {exc}", file=sys.stderr)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2983:# Greeting language of the pizzeria's country: de or en
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2984:PIZZERIA_LANG=
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2987:SPEECH_URL=
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2988:SPEECH_STT_MODEL=
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2989:SPEECH_TTS_MODEL=
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:2990:SPEECH_TTS_VOICE=
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3011:- Vor dem Abschicken: rufe `read_back` auf, lies die Bestellung vor und
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3053:1. Devil's advocate: attack the implementation — bugs, gaps, missing error cases, spec violations, divergence from the approved plan.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3056:Task: Review the IMPLEMENTATION (stage 2, round 2 of max 3) against SPEC.md (source of truth) and PLAN.md (the approved stage-1 plan; approved 24/25 in reviews/round3-plan.md, since updated only to document remove_item disambiguation semantics). Implementation: core/, channels/, prompts/, tests/, README.md, .env.example, requirements.txt.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3059:1. remove_item ambiguity with same (type, code) and different extras → deterministic semantics in core/state.py (no qty removes all matching lines; qty reduces the most recently added), documented in PLAN.md tool table, tested in tests/test_state.py (test_remove_without_qty_clears_all_variants, test_remove_with_qty_reduces_most_recent_variant). The spec fixes remove_item's parameters, so an extras parameter was not an option.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3064:Facts you cannot observe from the files, all demonstrated live: the deterministic suite passes (69 passed, 1 skipped opt-in live test); the web channel started with SPEECH_URL unset (speech:false, mic not rendered) and placed a real order end to end via the real gateway (read_back -> confirm_order(revision) -> submit_order -> order_id 3fe1deaa-... visible in the pizzeria's order list, ETA converted to minutes, id read in groups); a missing required env var exits before the first turn naming the variable and file. Your sandbox may lack a writable temp dir for pytest; judge from the code plus this evidence if so.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3066:Scope notes: tests/fixtures/*.json are recorded real API responses (UUIDs there are recorded data, not hardcoded config). venv/ and logs/ are gitignored runtime artifacts, out of scope.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3072:error_handling: N
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3082:I’m reviewing the implementation against `SPEC.md`, `PLAN.md`, and the round-1 review findings first, then I’ll inspect the implementation and tests to verify each claimed fix before scoring.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3196:The agent can still run tests, stage files, and output suggested branch
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3200:/bin/bash -lc "rg --files -g 'SPEC.md' -g 'PLAN.md' -g 'reviews/round3-plan.md' -g 'reviews/round4-impl.md' -g 'README.md' -g '.env.example' -g 'requirements.txt' -g 'core/**' -g 'channels/**' -g 'prompts/**' -g 'tests/**'" in /home/rob/bpm-pizza-vibecoding-solution
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3234:tests/test_transcripts.py
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3235:tests/test_tools.py
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3236:tests/test_state.py
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3237:tests/__init__.py
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3238:tests/__pycache__/test_tools.cpython-313-pytest-9.1.1.pyc
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3239:tests/__pycache__/__init__.cpython-313.pyc
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3240:tests/__pycache__/test_transcripts.cpython-313-pytest-9.1.1.pyc
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3241:tests/__pycache__/test_state.cpython-313-pytest-9.1.1.pyc
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3242:tests/transcripts/unknown_item.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3243:tests/transcripts/mind_change.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3244:tests/transcripts/submit_timeout.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3245:tests/transcripts/happy_path.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3246:tests/transcripts/correction.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3247:tests/fixtures/menu.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3248:tests/fixtures/order_created.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3249:tests/fixtures/pizzerias.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3250:tests/fixtures/orders_list.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3251:tests/fixtures/location.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3252:tests/fixtures/error_422.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3255:I have the review surface. Next I’m checking the spec, approved plan, and prior round findings side by side, then I’ll trace the implementation and tests for conformance and regressions.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3259:  • Inspect tests for coverage of required behavior, especially round-1 fixes and spec-critical flows
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3329:details.steps { font-size: .78rem; color: #666; margin: .2rem 0 .6rem; }
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3330:details.steps summary { cursor: pointer; user-select: none; }
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3331:details.steps pre { white-space: pre-wrap; word-break: break-all;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3376:  const details = document.createElement("details");
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3377:  details.className = "steps";
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3378:  details.innerHTML = "<summary>Zwischenschritte</summary>";
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3379:  chat.appendChild(details);
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3380:  return details;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3416:        } else if (ev.type === "error") {
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3494:    if (speechEnabled) {           // unset SPEECH_URL → not rendered at all
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3505:The implementation now matches the spec’s hard requirements and the approved plan closely enough to approve. I verified the round-2 fixes in code, not by claim: mutation demotion clears submit recovery state in [core/state.py](/home/rob/bpm-pizza-vibecoding-solution/core/state.py), the web channel serializes turns per session and returns `409` on overlap in [channels/web.py](/home/rob/bpm-pizza-vibecoding-solution/channels/web.py), gateway-timeout and loop-guard apologies emit assistant events in [core/agent.py](/home/rob/bpm-pizza-vibecoding-solution/core/agent.py), and `GET /config` returns exactly `{speech: bool}` in [channels/web.py](/home/rob/bpm-pizza-vibecoding-solution/channels/web.py). I also verified the updated submit-timeout recovery behavior: shortlisted candidates are checked via order detail before adoption in [core/tools.py](/home/rob/bpm-pizza-vibecoding-solution/core/tools.py), with coverage in [tests/test_tools.py](/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py). Given the supplied live evidence that the deterministic suite passed, the full live acceptance test passed against the real API, the web flow placed a real order under the configured pizzeria, and missing env fails before first turn, there is no remaining spec-level defect that justifies rejection in the final round.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3510:error_handling: 5
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3520:The implementation now matches the spec’s hard requirements and the approved plan closely enough to approve. I verified the round-2 fixes in code, not by claim: mutation demotion clears submit recovery state in [core/state.py](/home/rob/bpm-pizza-vibecoding-solution/core/state.py), the web channel serializes turns per session and returns `409` on overlap in [channels/web.py](/home/rob/bpm-pizza-vibecoding-solution/channels/web.py), gateway-timeout and loop-guard apologies emit assistant events in [core/agent.py](/home/rob/bpm-pizza-vibecoding-solution/core/agent.py), and `GET /config` returns exactly `{speech: bool}` in [channels/web.py](/home/rob/bpm-pizza-vibecoding-solution/channels/web.py). I also verified the updated submit-timeout recovery behavior: shortlisted candidates are checked via order detail before adoption in [core/tools.py](/home/rob/bpm-pizza-vibecoding-solution/core/tools.py), with coverage in [tests/test_tools.py](/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py). Given the supplied live evidence that the deterministic suite passed, the full live acceptance test passed against the real API, the web flow placed a real order under the configured pizzeria, and missing env fails before first turn, there is no remaining spec-level defect that justifies rejection in the final round.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3525:error_handling: 5
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:16:The implementer claims: SPEC v1 was fully built and approved (reviews/round1..8, reviews/scores.md with plan approved 24/25 and implementation approved 24/25, hotfix approved 24/25); 71 deterministic tests exist and are self-consistent; core/ implements the state machine, tool dispatch, PizzaSim client with submit-timeout recovery; channels/cli.py and channels/web.py + static UI exist; decisions/qa.md records oracle decisions. Verify each claim against the files and git log. Report discrepancies bluntly.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:19:SPEC.md was just replaced by the operator with v2 (git show HEAD -- SPEC.md; previous version is SPEC_20260801.md and in git history). Delta: prices + basket total in scope; multi-pizzeria (customer-selectable in the UI, PIZZERIA_ID only preselects; basket never crosses tenants; fresh conversation on switch); APP_VERSION env shown in footer; an entirely new "The web channel" section (header: pizzeria name, selector from GET /pizzerias with short UUIDs, dashboard link per pizzeria, DE/EN language switch applied to replies and speech, start-over; footer: version, full UUID, connection state for API+gateway, API docs link; "no message ends unanswered" invariant; visible basket with total; read-back with an explicit confirm CONTROL; basket locked after submit); mandatory headless-browser E2E tests incl. three failure paths; getUserMedia/MediaRecorder now explicitly sanctioned.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:21:The implementer's position, which you must attack: RETROFIT the existing codebase (do not restart from scratch). Rationale: the unchanged spec sections (soul, load-bearing idea, state machine, tools, error handling, anti-patterns, speech service, CLI) are already built, reviewed and tested (71 tests); the delta is additive and concentrated in the web layer + a session-level tenancy generalization + price fields; a restart would rewrite identical core code with fresh bug risk and lose the review trail. Planned retrofit sketch: (a) core: menu carries prices, get_menu/read_back expose price + basket total; PizzaSim client instantiated per session for the session's pizzeria (preselected id validated at startup; selector list from GET /pizzerias); (b) web: new header/footer/basket UI per spec, confirm control wired as customer action, language switch selects prompt+STT language per session (PIZZERIA_LANG stays the startup default), APP_VERSION required env; (c) tests: extend unit/tool tests for prices+tenancy, add Playwright browser E2E incl. the three failure paths (Playwright already proven working on this host); (d) PLAN.md updated first, re-reviewed before implementation.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:23:Attack this: where does retrofit risk silently violating v2? Is any v1 architectural decision now invalid (e.g. one client per process, PIZZERIA_LANG required var vs the new UI language switch, /config contract)? Is the confirm-control design sound given "the transport owns no order logic" and "CONFIRMED only via confirm_order(revision)"? Would a restart actually be cheaper or safer anywhere? Ask your hardest questions (max 6, numbered) — the implementer will answer them in the next call before you give a verdict. If the audit in JOB 1 found discrepancies, include them as questions.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:163:The agent can still run tests, stage files, and output suggested branch
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:192:./tests/__init__.py
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:193:./tests/test_tools.py
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:194:./tests/test_state.py
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:195:./tests/test_transcripts.py
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:196:./tests/fixtures/menu.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:197:./tests/fixtures/order_created.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:198:./tests/fixtures/pizzerias.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:199:./tests/fixtures/orders_list.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:200:./tests/fixtures/location.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:201:./tests/fixtures/error_422.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:202:./tests/transcripts/unknown_item.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:203:./tests/transcripts/mind_change.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:204:./tests/transcripts/submit_timeout.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:205:./tests/transcripts/happy_path.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:206:./tests/transcripts/correction.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:228:* bb8a00c (HEAD -> main) New SPEC v2 (web channel section, multi-pizzeria, prices, APP_VERSION); restore verified contract facts + dashboard/docs paths
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:237:* 0ce98c6 Menu validation, PizzaSim client, tool dispatch + fixture tests
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:238:* f670920 Core order model + state machine, exhaustive unit tests
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:247:* 2a1827f Add pizzeria-specific dashboard link
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:277:1. Devil's advocate: attack the plan — gaps, wrong assumptions, missing error cases, spec violations.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:286:error_handling: N
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:309:> repo — code, tests, prompts, tickets — derives from it.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:354:**Core belief:** a language model is a great waiter and a terrible order pad.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:366:  tool error carrying candidate matches — never a silent guess, never a fallback
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:391:- **Languages:** German and English. The agent answers in the language the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:395:- **The success moment:** the order appears in the PizzaSim dashboard under the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:397:- **Deterministic tests** that run with no network and no LLM.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:435:- Secrets never appear in logs, transcripts, error messages or the web UI.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:446:| `GET /location?street=…` | public | street plausibility check |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:453:  "items": [{ "type": "pizza", "code": "margherita", "qty": 2, "extras": [] }]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:475:invalid bodies —, `GET /pizzerias/{id}/orders`, `GET /location`). Facts below
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:498:1. Devil's advocate: attack the plan — gaps, wrong assumptions, missing error cases, spec violations.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:503:Context from round 1 (a previous stateless review): it required (a) no ./.env fallback and no extra config vars, (b) tool results matching the spec's fixed contract exactly, (c) greeting in the pizzeria-country language with per-turn mirroring not driven by UI controls, (d) one explicit startup sequence validating PIZZERIA_ID via GET /pizzerias, (e) a confirmation path no broader than the spec. All five were applied; verify they are actually resolved in the current PLAN.md rather than taking this note on faith.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:509:error_handling: N
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:596:> repo — code, tests, prompts, tickets — derives from it.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:641:**Core belief:** a language model is a great waiter and a terrible order pad.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:653:  tool error carrying candidate matches — never a silent guess, never a fallback
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:678:- **Languages:** German and English. The agent answers in the language the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:682:- **The success moment:** the order appears in the PizzaSim dashboard under the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:684:- **Deterministic tests** that run with no network and no LLM.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:719:1. Devil's advocate: attack the plan — gaps, wrong assumptions, missing error cases, spec violations.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:722:Task: Read SPEC.md (the source of truth) and PLAN.md (the stage-1 implementation plan under review, round 3 of max 3). Judge whether PLAN.md is a complete, correct, spec-compliant plan such that implementing exactly it satisfies SPEC.md. The "Contract facts" section in SPEC.md was verified against the live API and is trustworthy. decisions/qa.md records an oracle decision on the greeting language (required env var PIZZERIA_LANG) taken between rounds.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:724:Round 2 (stateless, see reviews/round2-plan.md) required: (1) one exact tool-result contract per tool composing the per-tool table with the full-current-state rule, and fixing an eta_minutes test regression; (2) a spec-compliant, non-hardcoded, non-UI source for the greeting language; (3) explicit persisted state for submit-timeout recovery correlation; (4) removing lang from the chat contract or fencing it to an STT hint; (5) per-session immutable menu snapshot ownership. All five were addressed in the current PLAN.md — verify in the file, do not take this note on faith: see the SNAPSHOT definition in "Tool schemas", the PIZZERIA_LANG paragraph in "Configuration", submit_attempted_at in the state-machine section, the web protocol section, and the "Session model" paragraph.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:732:error_handling: N
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:767:1. Devil's advocate: attack the plan — gaps, wrong assumptions, missing error cases, spec violations.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:772:Context from round 1 (a previous stateless review): it required (a) no ./.env fallback and no extra config vars, (b) tool results matching the spec's fixed contract exactly, (c) greeting in the pizzeria-country language with per-turn mirroring not driven by UI controls, (d) one explicit startup sequence validating PIZZERIA_ID via GET /pizzerias, (e) a confirmation path no broader than the spec. All five were applied; verify they are actually resolved in the current PLAN.md rather than taking this note on faith.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:778:error_handling: N
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:865:> repo — code, tests, prompts, tickets — derives from it.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:910:**Core belief:** a language model is a great waiter and a terrible order pad.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:922:  tool error carrying candidate matches — never a silent guess, never a fallback
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:940:1. Devil's advocate: attack the implementation — bugs, gaps, missing error cases, spec violations, divergence from the approved plan.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:943:Task: Review the IMPLEMENTATION (stage 2) against SPEC.md (source of truth) and PLAN.md (the approved stage-1 plan, 24/25 APPROVED in reviews/round3-plan.md). The implementation is: core/ (order, state, menu, pizzasim, tools, agent), channels/ (cli.py, web.py, static/), prompts/, tests/ (state, tools, transcripts + fixtures), README.md, .env.example, requirements.txt.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:945:Facts you cannot observe from the files, all demonstrated live before this review: the full deterministic suite passes (67 passed, 1 skipped opt-in live test); the web channel started with SPEECH_URL unset (speech:false, mic not rendered) and placed a real order end to end via the real gateway (read_back -> confirm_order(revision) -> submit_order -> order_id 3fe1deaa-... visible in the pizzeria's order list); a missing required env var exits before the first turn naming the variable and file. You may run the test suite yourself if your sandbox permits; otherwise judge from the code.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:947:Scope notes: tests/fixtures/*.json are recorded real API responses (UUIDs in them are recorded data, not hardcoded config). The venv/ and logs/ directories are gitignored runtime artifacts, out of scope.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:953:error_handling: N
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1072:The agent can still run tests, stage files, and output suggested branch
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1076:/bin/bash -lc "pwd && rg --files -g 'SPEC.md' -g 'PLAN.md' -g 'README.md' -g '.env.example' -g 'requirements.txt' -g 'reviews/**' -g 'core/**' -g 'channels/**' -g 'prompts/**' -g 'tests/**'" in /home/rob/bpm-pizza-vibecoding-solution
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1108:tests/__pycache__/test_tools.cpython-313-pytest-9.1.1.pyc
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1109:tests/__pycache__/__init__.cpython-313.pyc
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1110:tests/__pycache__/test_transcripts.cpython-313-pytest-9.1.1.pyc
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1111:tests/__pycache__/test_state.cpython-313-pytest-9.1.1.pyc
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1112:tests/__init__.py
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1113:tests/test_tools.py
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1114:tests/test_state.py
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1115:tests/test_transcripts.py
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1116:tests/fixtures/menu.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1117:tests/fixtures/order_created.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1118:tests/fixtures/pizzerias.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1119:tests/fixtures/orders_list.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1120:tests/fixtures/location.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1121:tests/fixtures/error_422.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1122:tests/transcripts/unknown_item.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1123:tests/transcripts/mind_change.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1124:tests/transcripts/submit_timeout.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1125:tests/transcripts/happy_path.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1126:tests/transcripts/correction.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1135:  • Inspect implementation files and tests against spec/plan requirements
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1145:> repo — code, tests, prompts, tickets — derives from it.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1161:1. Devil's advocate: attack the implementation — bugs, gaps, missing error cases, spec violations, divergence from the approved plan.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1164:Task: Review the IMPLEMENTATION (stage 2, round 2 of max 3) against SPEC.md (source of truth) and PLAN.md (the approved stage-1 plan; approved 24/25 in reviews/round3-plan.md, since updated only to document remove_item disambiguation semantics). Implementation: core/, channels/, prompts/, tests/, README.md, .env.example, requirements.txt.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1167:1. remove_item ambiguity with same (type, code) and different extras → deterministic semantics in core/state.py (no qty removes all matching lines; qty reduces the most recently added), documented in PLAN.md tool table, tested in tests/test_state.py (test_remove_without_qty_clears_all_variants, test_remove_with_qty_reduces_most_recent_variant). The spec fixes remove_item's parameters, so an extras parameter was not an option.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1172:Facts you cannot observe from the files, all demonstrated live: the deterministic suite passes (69 passed, 1 skipped opt-in live test); the web channel started with SPEECH_URL unset (speech:false, mic not rendered) and placed a real order end to end via the real gateway (read_back -> confirm_order(revision) -> submit_order -> order_id 3fe1deaa-... visible in the pizzeria's order list, ETA converted to minutes, id read in groups); a missing required env var exits before the first turn naming the variable and file. Your sandbox may lack a writable temp dir for pytest; judge from the code plus this evidence if so.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1174:Scope notes: tests/fixtures/*.json are recorded real API responses (UUIDs there are recorded data, not hardcoded config). venv/ and logs/ are gitignored runtime artifacts, out of scope.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1180:error_handling: N
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1190:I’m reviewing the implementation against `SPEC.md`, `PLAN.md`, and the round-1 review findings first, then I’ll inspect the implementation and tests to verify each claimed fix before scoring.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1304:The agent can still run tests, stage files, and output suggested branch
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1308:/bin/bash -lc "rg --files -g 'SPEC.md' -g 'PLAN.md' -g 'reviews/round3-plan.md' -g 'reviews/round4-impl.md' -g 'README.md' -g '.env.example' -g 'requirements.txt' -g 'core/**' -g 'channels/**' -g 'prompts/**' -g 'tests/**'" in /home/rob/bpm-pizza-vibecoding-solution
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1342:tests/test_transcripts.py
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1343:tests/test_tools.py
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1344:tests/test_state.py
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1345:tests/__init__.py
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1346:tests/__pycache__/test_tools.cpython-313-pytest-9.1.1.pyc
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1347:tests/__pycache__/__init__.cpython-313.pyc
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1348:tests/__pycache__/test_transcripts.cpython-313-pytest-9.1.1.pyc
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1349:tests/__pycache__/test_state.cpython-313-pytest-9.1.1.pyc
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1350:tests/transcripts/unknown_item.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1351:tests/transcripts/mind_change.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1352:tests/transcripts/submit_timeout.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1353:tests/transcripts/happy_path.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1354:tests/transcripts/correction.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1355:tests/fixtures/menu.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1356:tests/fixtures/order_created.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1357:tests/fixtures/pizzerias.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1358:tests/fixtures/orders_list.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1359:tests/fixtures/location.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1360:tests/fixtures/error_422.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1363:I have the review surface. Next I’m checking the spec, approved plan, and prior round findings side by side, then I’ll trace the implementation and tests for conformance and regressions.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1367:  • Inspect tests for coverage of required behavior, especially round-1 fixes and spec-critical flows
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1382:1. Devil's advocate: attack the implementation — bugs, gaps, missing error cases, spec violations.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1385:Task: Review the IMPLEMENTATION (stage 2, round 3 of max 3) against SPEC.md (source of truth — note it now contains the operator-added "What done looks like" acceptance section) and PLAN.md (approved stage-1 plan, updated alongside). Implementation: core/, channels/, prompts/, tests/, README.md, .env.example, requirements.txt.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1388:1. Mutations clear submit_unknown/submit_attempted_at (core/state.py _recompute); tested in tests/test_tools.py::test_mutation_after_submit_timeout_clears_recovery_state.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1392:Additionally, per the updated SPEC: submit-timeout recovery now verifies the shortlisted candidate's items via GET /pizzerias/{id}/orders/{order_id} before adopting it (core/tools.py, tests test_recovery_rejects_candidate_with_different_items), and the opt-in live test is now the full acceptance test (tests/test_tools.py::test_live_acceptance) asserting order id, presence in the pizzeria's list, exact customer name, and exact items/quantities.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1394:Facts you cannot observe from the files, all demonstrated live: deterministic suite passes (71 passed, 1 skipped); the live acceptance test PASSED against the real API (real order, read back via list + detail endpoints, exact match); the web channel with SPEECH_URL unset reported speech:false and placed a real order end to end via the real gateway (order 3fe1deaa-... under the configured pizzeria with exactly the read-back items — independently confirmed via the detail endpoint); a missing required env var exits before the first turn naming the variable and file. Your sandbox may lack a writable temp dir for pytest; judge from code plus this evidence if so.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1396:Scope notes: tests/fixtures/*.json are recorded real API responses (UUIDs there are recorded data, not hardcoded config). venv/ and logs/ are gitignored runtime artifacts, out of scope. decisions/qa.md records oracle decisions.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1404:error_handling: N
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1416:/bin/bash -lc "rg --files /home/rob/bpm-pizza-vibecoding-solution | rg '"'^(SPEC'"\\.md|PLAN\\.md|README\\.md|requirements\\.txt|\\.env\\.example|core/|channels/|prompts/|tests/|decisions/qa\\.md)'" in /home/rob/bpm-pizza-vibecoding-solution
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1526:The agent can still run tests, stage files, and output suggested branch
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1530:/bin/bash -lc "rg --files . | rg '"'^(SPEC'"\\.md|PLAN\\.md|README\\.md|requirements\\.txt|\\.env\\.example|core/|channels/|prompts/|tests/|decisions/qa\\.md)'" in /home/rob/bpm-pizza-vibecoding-solution
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1548:> repo — code, tests, prompts, tickets — derives from it.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1612:error_handling: N
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1637:proxies the optional self-hosted speech service (STT/TTS). If SPEECH_URL is
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1667:    enabled only if SPEECH_URL is set, answers, and models are configured."""
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1670:        self.url = optional_env("SPEECH_URL")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1671:        self.stt_model = optional_env("SPEECH_STT_MODEL")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1672:        self.tts_model = optional_env("SPEECH_TTS_MODEL")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1673:        self.voice = optional_env("SPEECH_TTS_VOICE")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1691:        print(f"Configuration error: {exc}", file=sys.stderr)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1781:            "language": app.state.config.lang}  # STT hint only
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1827:Additional live evidence since round 7: a real headless Chromium was driven against the public URL http://<host>:8888 with window.isSecureContext === false. Results: zero page errors; greeting rendered; pizzeria name shown in the header; mic and TTS controls hidden (speech disabled in this deployment); a typed customer message produced a correct menu answer with the intermediate-steps block visible. Full-page screenshot captured.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1835:error_handling: N
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1952:  const details = document.createElement("details");
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1953:  details.className = "steps";
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1954:  details.innerHTML = "<summary>Zwischenschritte</summary>";
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1955:  chat.appendChild(details);
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1956:  return details;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1992:        } else if (ev.type === "error") {
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2034:## 2026-07-31 — Greeting language source
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2036:**Q:** SPEC requires greeting in the pizzeria-country language; the live API
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2038:Which mechanism: (a) optional env `PIZZERIA_LANG` default de, (b) required
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2041:**A (decision):** **(b)** — `PIZZERIA_LANG` (de|en) is a required env var.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2044:before the first turn naming `PIZZERIA_LANG` and where it was expected; no
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2063:`uvicorn` (web channel), `pytest` (tests), stdlib `difflib` (candidate
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2073:- Secrets never appear in logs, transcripts, errors, or the web UI.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2077:- No build-time model name anywhere in source, config, prompts, tests, docs.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2081:- Deterministic tests: no network, no LLM (one opt-in live smoke test).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2092:  menu.py      Immutable Menu snapshot (pizzas, pasta, toppings), one per
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2093:               session; (type, code) validation; extras validation;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2096:               submit_order, check_street; typed errors; timeouts;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2100:               {"error": {code, message, candidates}}.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2113:  system.de.md German system prompt (default deployment language).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2115:tests/
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2117:               list, 422 bodies, location).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2128:Deviation from the SPEC tree, documented: `tests/test_transcripts.py` and
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2138:| `core/agent.py` | `LITELLM_PIZZA_URL`, `LITELLM_PIZZA_KEY`, `LITELLM_PIZZA_MODEL_1`, `PIZZERIA_LANG` (all required; `LITELLM_PIZZA_MODEL_2` read but unused — single-model build) |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2140:| `channels/web.py` | `SPEECH_URL`, `SPEECH_STT_MODEL`, `SPEECH_TTS_MODEL`, `SPEECH_TTS_VOICE` (all optional; absence disables speech) |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2142:`PIZZERIA_LANG` ∈ {`de`, `en`} is the pizzeria-country greeting language.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2146:`decisions/qa.md`). It selects the system prompt file and the STT language
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2147:hint; it never overrides per-turn language mirroring.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2160:   404-pizzeria case from the error table → process refuses to start;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2178:Order fields: `items: list[Item(type, code, qty, extras)]`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2180:(increments on every basket or customer mutation), `read_back_revision:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2181:int | None` (set by `read_back`), `state`, `submit_attempted_at: int | None`
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2195:Transition table (✓ legal, ✗ → typed error):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2200:| remove_item | ✗ empty_basket | ✓ | ✓ | ✓ demote | ✗ order_closed |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2202:| read_back | ✗ empty_basket | ✗ invalid_state (no customer yet) | ✓ | ✓ (same basket, idempotent) | ✗ order_closed |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2208:(else `stale_revision`) and `read_back_revision == order.revision` (else
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2209:`read_back_required`). So the only path into `CONFIRMED` is: state `READY`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2210:`read_back` called at the current revision, then `confirm_order` naming that
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2223:exactly one real retry. List or detail call fails → error `submit_unknown`
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2235:`{state, revision, items: [{type, code, name, qty, extras}], customer:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2236:{first_name, street_one} | null, read_back_done: bool}` — never a diff.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2240:| `get_menu` | `{}` | `{"menu": {"pizzas": [{code, name}], "pasta": [{code, name}], "toppings": [str]}, "snapshot": SNAPSHOT}` — `name` is the API's single display name, which the verified contract facts show serves both languages |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2241:| `add_items` | `{items: [{type: enum[pizza,pasta], code: str, qty: int ≥1, extras: [str]}]}` (required: items; extras default `[]`) | `{"snapshot": SNAPSHOT}` (basket + revision live in SNAPSHOT) |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2242:| `remove_item` | `{type: enum, code: str, qty: int ≥1 optional}` — the spec fixes these params, so when several lines share (type, code) with different extras: absent qty removes **all** matching lines, qty reduces the **most recently added** matching line (deterministic; the snapshot lets the model repair by remove + re-add) | `{"snapshot": SNAPSHOT}` |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2244:| `read_back` | `{}` | `{"snapshot": SNAPSHOT}` — basket, customer, revision: the material the agent reads out |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2245:| `confirm_order` | `{revision: int}` | `{"snapshot": SNAPSHOT}` with `state == "CONFIRMED"`, or error if stale |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2247:| `check_street` | `{street: str}` | `{"street": str, "deliverable": bool, "snapshot": SNAPSHOT}` — the never-claim-verified rule lives in the prompt, not the tool |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2249:Failure shape: `{"error": {"code": "<one of the codes below>", "message":
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2253:candidate toppings), `invalid_quantity` (non-integer or < 1 — the tool does
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2255:`read_back_required`, `order_closed`, `submit_failed`, `submit_unknown`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2256:`api_unavailable`, `not_in_basket` (remove_item for a line that isn't there).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2259:snapshot and every extra against `toppings[]`; any failure rejects the whole
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2260:call atomically (no partial adds), returning the first error with candidates
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2271:machine owned by the code; the model only turns customer language into tool
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2283:`.env.example` except the four `SPEECH_*` ones is required. The process
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2294:The agent greets first, in the language set by `PIZZERIA_LANG`, and answers
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2295:each turn in the language you used (German or English). End with Ctrl-D.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2310:Set `SPEECH_URL`, `SPEECH_STT_MODEL`, `SPEECH_TTS_MODEL` and
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2311:`SPEECH_TTS_VOICE` to a self-hosted OpenAI-compatible speech service. The
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2314:`SPEECH_URL` unset — or the service down at startup — mic and toggle are
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2319:question; and one run with `SPEECH_URL` unset placing an order as text.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2324:venv/bin/python -m pytest tests/            # deterministic: no network, no LLM
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2325:PIZZA_LIVE_TEST=1 venv/bin/python -m pytest tests/test_tools.py -k live
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2342:error_handling: 4
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2349:results restored to the spec's fixed contract; greeting language =
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2351:single explicit startup sequence via `GET /pizzerias`; read_back/confirm
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2352:path tightened (read_back only in READY/CONFIRMED, confirm only in READY).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2358:error_handling: 4
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2366:greeting language now required env var PIZZERIA_LANG (oracle decision in
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2369:hint = PIZZERIA_LANG only; per-session immutable menu snapshot defined via
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2376:error_handling: 5
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2386:error_handling: 4
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2392:Findings applied: remove_item now deterministic across same-(type,code)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2393:lines with different extras (no qty = all matching lines, qty = most recent
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2394:line; two new tests; PLAN.md updated); speech probe requires 2xx via
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2402:error_handling: 3
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2425:error_handling: 5
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2435:error_handling: 3
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2450:error_handling: 4
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2457:(isSecureContext=false): no JS errors, greeting, pizzeria name in header,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2465:    New SPEC v2 (web channel section, multi-pizzeria, prices, APP_VERSION); restore verified contract facts + dashboard/docs paths
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2475: - **Languages:** German and English. The agent answers in the language the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2485: - **The success moment:** the order appears in the PizzaSim dashboard under the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2487: - **Deterministic tests** that run with no network and no LLM.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2522:-`GET /pizzerias/{id}/orders/{order_id}`, `GET /location`). Facts below are
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2524:+`GET /pizzerias/{id}/orders/{order_id}`, `GET /location`, plus the dashboard
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2537:    there are no per-language names in the API; read-back uses `name` as-is in
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2538:    both languages. The menu response also carries a top-level `toppings[]`
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2540:    returned `deliverable: true` — the check is a weak plausibility signal at
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2543:+8. **The pizzeria dashboard** lives at
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2544:+   `{PIZZASIM_URL}/dashboard/pizzerias/{id}` (confirmed in the dashboard's
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2545:+   own routing code); the overview is `{PIZZASIM_URL}/dashboard`. The
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2546:+   header's dashboard link is derived from `PIZZASIM_URL` — nothing
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2548:+9. **The API documentation** is served at `{PIZZASIM_URL}/swagger.html`
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2589:+- **A link to that pizzeria's dashboard**, opening in a new tab, pointing at the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2590:+  dashboard path for the selected pizzeria id. Without it nobody can check
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2609:+rendered assistant reply or a rendered error.** Never a silent failure, never an
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2618:+- If the request errors, times out, or the connection drops, the UI says which
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2620:+- Errors in the customer's language, in plain words. No status codes, no
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2659:   model, TTS model, voice and language all come from the environment, exactly
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2670:+  three failure paths: a tool error, a stream that ends without a final message,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2676:    Pass when the unit tests are green.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2678: 3. **CLI.** Full conversation, real API, an order visible in the dashboard.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2682:+   through the page, and then seen that order on that pizzeria's dashboard.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2685: 6. **Harden.** Walk the error table, force each case, fix what breaks.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2707:> repo — code, tests, prompts, tickets — derives from it.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2752:**Core belief:** a language model is a great waiter and a terrible order pad.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2764:  tool error carrying candidate matches — never a silent guess, never a fallback
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2791:   dashboard for that pizzeria.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2826:- **Languages:** German and English. The agent answers in the language the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2830:- **The success moment:** the order appears in the PizzaSim dashboard under the
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2832:- **Deterministic tests** that run with no network and no LLM.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2870:- Secrets never appear in logs, transcripts, error messages or the web UI.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2881:| `GET /location?street=…` | public | street plausibility check |
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2888:  "items": [{ "type": "pizza", "code": "margherita", "qty": 2, "extras": [] }]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2911:`GET /pizzerias/{id}/orders/{order_id}`, `GET /location`). Facts below are
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2921:   `customer_id`, `created_at`, `ready_at`, `status`, `delivered_at`,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2930:   there are no per-language names in the API; read-back uses `name` as-is in
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2931:   both languages. The menu response also carries a top-level `toppings[]`
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2933:4. **`extras[]` is a controlled vocabulary:** the top-level `toppings[]` from
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2935:   rejects unknown extras with `422` (`"items[0].extras contains invalid
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2936:   topping 'unicorn_dust'"`), so the tool layer validates extras against
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2937:   `toppings[]` exactly like item codes.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2939:   `{"error": "<code>", "details": ["<human sentence>", ...]}` — e.g.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2940:   `{"error": "validation_failed", "details": ["items[0].code must be a valid
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2941:   pizza code"]}` with HTTP 422. The tool layer maps `error` to typed errors
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2942:   and may surface `details` to targeted questions.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2944:   `prepared_planned` → `delivered` (with `delivered_at` set on the last).
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2946:7. **`GET /location?street=` returns** `{"street": "<echo>",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2947:   "deliverable": <bool>}` with HTTP 200. In probing, even a nonsense street
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2948:   returned `deliverable: true` — the check is a weak plausibility signal at
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2966:/bin/bash -lc "for f in core/order.py core/state.py core/menu.py core/pizzasim.py core/tools.py core/agent.py channels/cli.py channels/web.py channels/static/index.html channels/static/app.js channels/static/style.css tests/test_state.py tests/test_tools.py tests/test_transcripts.py; do echo '---'\" "'$f"; nl -ba "$f" | sed -n '"'1,260p'; done" in /home/rob/bpm-pizza-vibecoding-solution
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2968:/bin/bash -lc "for f in tests/transcripts/*.json tests/fixtures/*.json; do echo '---'\" "'$f"; sed -n '"'1,220p' \""'$f"; done' in /home/rob/bpm-pizza-vibecoding-solution
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2970:/bin/bash -lc 'pytest --collect-only -q -p no:cacheprovider tests' in /home/rob/bpm-pizza-vibecoding-solution
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2972:--- tests/transcripts/correction.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2979:       {"tool": "add_items", "args": {"items": [{"type": "pizza", "code": "margherita", "qty": 1, "extras": []}]}},
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2984:       {"tool": "add_items", "args": {"items": [{"type": "pizza", "code": "margherita", "qty": 2, "extras": []}]}},
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2990:       {"tool": "read_back", "args": {}},
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3002:    "calls": ["add_items", "add_items", "set_customer", "read_back", "confirm_order", "submit_order"],
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3003:    "error_codes": [],
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3007:--- tests/transcripts/happy_path.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3019:       {"tool": "add_items", "args": {"items": [{"type": "pizza", "code": "margherita", "qty": 2, "extras": []}]}},
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3025:       {"tool": "read_back", "args": {}},
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3037:    "calls": ["get_menu", "add_items", "set_customer", "read_back", "confirm_order", "submit_order"],
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3038:    "error_codes": [],
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3042:--- tests/transcripts/mind_change.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3044:  "name": "mind_change_after_read_back",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3049:       {"tool": "add_items", "args": {"items": [{"type": "pizza", "code": "diavolo", "qty": 1, "extras": []}]}},
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3051:       {"tool": "read_back", "args": {}},
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3056:       {"tool": "add_items", "args": {"items": [{"type": "pizza", "code": "funghi", "qty": 1, "extras": []}]}},
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3058:       {"tool": "read_back", "args": {}},
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3070:    "calls": ["add_items", "set_customer", "read_back", "add_items", "confirm_order", "read_back", "confirm_order", "submit_order"],
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3071:    "error_codes": ["stale_revision"],
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3075:--- tests/transcripts/submit_timeout.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3082:       {"tool": "add_items", "args": {"items": [{"type": "pizza", "code": "hawaii", "qty": 1, "extras": []}]}},
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3084:       {"tool": "read_back", "args": {}},
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3101:    "calls": ["add_items", "set_customer", "read_back", "confirm_order", "submit_order", "submit_order"],
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3102:    "error_codes": ["submit_unknown"],
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3107:--- tests/transcripts/unknown_item.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3114:       {"tool": "add_items", "args": {"items": [{"type": "pasta", "code": "bolognese", "qty": 1, "extras": []}]}},
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3119:       {"tool": "add_items", "args": {"items": [{"type": "pasta", "code": "funghi", "qty": 1, "extras": []}]}},
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3125:       {"tool": "read_back", "args": {}},
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3137:    "calls": ["add_items", "add_items", "set_customer", "read_back", "confirm_order", "submit_order"],
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3138:    "error_codes": ["unknown_item"],
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3142:--- tests/fixtures/error_422.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3143:{"error":"validation_failed","details":["items[0].code must be a valid pizza code"]}--- tests/fixtures/location.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3144:{"street":"via Roma","deliverable":true}--- tests/fixtures/menu.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3145:{"toppings":["mozzarella","mushrooms","smoked_ham","salami","onions","garlic","pepperoni","pineapple","artichokes","basil","bell_pepper","tuna"],"pizzas":[{"code":"margherita","name":"Margherita","base":["dough","tomatoes","mozzarella","basil"],"price":8.5},{"code":"prosciutto","name":"Prosciutto","base":["dough","tomatoes","mozzarella","smoked_ham"],"price":9.5},{"code":"salami","name":"Salami","base":["dough","tomatoes","mozzarella","salami"],"price":9.5},{"code":"funghi","name":"Funghi","base":["dough","tomatoes","mozzarella","mushrooms"],"price":9},{"code":"regina","name":"Regina","base":["dough","tomatoes","mozzarella","smoked_ham","mushrooms"],"price":10.5},{"code":"mista","name":"Mista","base":["dough","tomatoes","mozzarella","salami","smoked_ham","mushrooms"],"price":11.5},{"code":"hawaii","name":"Hawaii","base":["dough","tomatoes","mozzarella","smoked_ham","pineapple"],"price":10},{"code":"tonno","name":"Tonno","base":["dough","tomatoes","mozzarella","tuna","onions"],"price":10.5},{"code":"papa","name":"Papa","base":["dough","tomatoes","mozzarella","tuna","onions","garlic"],"price":11},{"code":"diavolo","name":"Diavolo","base":["dough","tomatoes","mozzarella","salami","bell_pepper","pepperoni"],"price":11},{"code":"grandiosa","name":"Grandiosa","base":["dough","tomatoes","mozzarella","smoked_ham","salami","mushrooms","bell_pepper","artichokes","onions"],"price":13.5}],"pasta":[{"code":"aglioolio","name":"Pasta Aglio & Olio","base":["pasta","garlic","basil"],"price":9},{"code":"tonno","name":"Pasta Tonno","base":["pasta","tuna"],"price":8.5},{"code":"funghi","name":"Pasta Funghi","base":["pasta","mushrooms"],"price":8.5},{"code":"pesto","name":"Pasta Pesto","base":["pasta","pesto"],"price":8.5}]}--- tests/fixtures/order_created.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3146:{"order_id":"35711fad-9cf0-4962-bf13-da2f78add431","status":"ordered","eta_seconds":103}--- tests/fixtures/orders_list.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3154:   "status": "prepared_planned",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3155:   "delivered_at": null,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3163:   "status": "prepared_planned",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3164:   "delivered_at": null,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3172:   "status": "prepared_planned",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3173:   "delivered_at": null,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3181:   "status": "prepared_planned",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3182:   "delivered_at": null,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3190:   "status": "prepared_planned",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3191:   "delivered_at": null,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3197:--- tests/fixtures/pizzerias.json
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3222:    22	    extras: list[str] = field(default_factory=list)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3225:    25	        return (self.type, self.code, tuple(sorted(self.extras)))
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3242:    42	    read_back_revision: int | None = None
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3259:    59	                    "extras": list(i.extras),
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3264:    64	            "read_back_done": self.read_back_revision == self.revision,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3323:    57	def remove_item(order: Order, type_: str, code: str, qty: int | None) -> None:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3324:    58	    """The spec fixes remove_item's parameters to (type, code, qty), so a
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3325:    59	    basket holding the same (type, code) with different extras needs
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3355:    89	def read_back(order: Order) -> None:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3366:   100	    order.read_back_revision = order.revision
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3386:   120	    if order.read_back_revision != order.revision:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3388:   122	            "read_back_required",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3414:     1	"""Immutable menu snapshot: (type, code) validation, extras validation,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3435:    22	        self.toppings: list[str] = list(payload.get("toppings", []))
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3443:    30	            "toppings": self.toppings,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3472:    59	    def validate_extras(self, extras: list[str]) -> None:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3473:    60	        for extra in extras:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3474:    61	            if extra not in self.toppings:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3478:    65	                        extra.lower(), self.toppings, n=3, cutoff=0.5
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3516:     1	"""PizzaSim API client: httpx, explicit timeouts, typed errors.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3561:    46	    """Base for typed API errors."""
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3573:    58	    def __init__(self, details: list[str]):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3574:    59	        super().__init__("; ".join(details))
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3575:    60	        self.details = details
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3593:    78	            details = response.json().get("details", [])
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3595:    80	            details = []
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3596:    81	        raise ValidationError(details or ["invalid request"])
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3598:    83	        raise ServerError(f"server error ({response.status_code})")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3668:   153	        return self._request("GET", "/location", params={"street": street})
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3673:     4	{"error": {"code", "message", "candidates"}} with a speakable message.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3697:    28	        "extras": {"type": "array", "items": {"type": "string"}},
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3705:    36	                    "names, and the available extra toppings.",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3715:    46	    {"name": "remove_item",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3733:    64	    {"name": "read_back",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3763:    94	def _error(code: str, message: str, candidates: list | None = None) -> dict:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3764:    95	    return {"error": {"code": code, "message": message,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3785:   116	        return _error(exc.code, exc.message, exc.candidates)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3787:   118	        return _error(exc.code, exc.message)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3789:   120	        return _error("api_unavailable",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3792:   123	        return _error("api_unavailable",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3795:   126	        return _error("api_unavailable",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3807:   138	            extras = raw.get("extras") or []
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3808:   139	            menu.validate_extras(extras)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3815:   146	                extras=extras,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3818:   149	            return _error("invalid_quantity", "What can I get you?")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3822:   153	    if name == "remove_item":
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3824:   155	        state.remove_item(order, args.get("type", ""), args.get("code", ""),
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3831:   162	            return _error("invalid_state", "I still need a name.")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3837:   168	    if name == "read_back":
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3838:   169	        state.read_back(order)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3844:   175	            return _error("stale_revision",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3855:   186	                "deliverable": bool(result.get("deliverable")),
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3858:   189	    return _error("unknown_tool", "Something went wrong on my side.")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3868:   199	            (e["type"], e["code"], e["qty"], tuple(sorted(e["extras"])))
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3872:   203	             "extras": list(i.extras)} for i in basket]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3887:   218	            return _error("submit_unknown", _UNSURE)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3899:   230	                return _error("submit_unknown", _UNSURE)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3914:   245	              "extras": list(i.extras)} for i in order.items]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3918:   249	        return _error("submit_failed",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3920:   251	                      + "; ".join(exc.details))
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3922:   253	        return _error("api_unavailable",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3926:   257	        return _error("submit_unknown", _UNSURE)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3970:    40	    lang: str  # PIZZERIA_LANG: greeting language = pizzeria country
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3974:    44	        lang = require_env("PIZZERIA_LANG").lower()
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:3977:    47	                "PIZZERIA_LANG must be 'de' or 'en', got something else"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4075:   145	                event({"type": "error", "error": str(exc)})
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4115:   185	        event({"type": "error", "error": "tool loop guard exceeded"})
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4169:    40	        print(f"Configuration error: {exc}", file=sys.stderr)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4199:     4	proxies the optional self-hosted speech service (STT/TTS). If SPEECH_URL is
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4229:    34	    enabled only if SPEECH_URL is set, answers, and models are configured."""
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4232:    37	        self.url = optional_env("SPEECH_URL")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4233:    38	        self.stt_model = optional_env("SPEECH_STT_MODEL")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4234:    39	        self.tts_model = optional_env("SPEECH_TTS_MODEL")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4235:    40	        self.voice = optional_env("SPEECH_TTS_VOICE")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4253:    58	        print(f"Configuration error: {exc}", file=sys.stderr)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4343:   148	            "language": app.state.config.lang}  # STT hint only
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4447:    38	  const details = document.createElement("details");
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4448:    39	  details.className = "steps";
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4449:    40	  details.innerHTML = "<summary>Zwischenschritte</summary>";
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4450:    41	  chat.appendChild(details);
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4451:    42	  return details;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4487:    78	        } else if (ev.type === "error") {
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4570:   161	    speechEnabled = cfg.speech;    // unset SPEECH_URL → nothing rendered
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4595:    17	details.steps { font-size: .78rem; color: #666; margin: .2rem 0 .6rem; }
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4596:    18	details.steps summary { cursor: pointer; user-select: none; }
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4597:    19	details.steps pre { white-space: pre-wrap; word-break: break-all;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4608:--- tests/test_state.py
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4618:    10	def item(code="margherita", type_="pizza", qty=1, extras=None):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4620:    12	                extras=extras or [])
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4633:    25	    state.read_back(o)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4656:    48	    state.read_back(o)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4678:    70	    lambda o: state.remove_item(o, "pizza", "margherita", None),
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4680:    72	    lambda o: state.read_back(o),
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4693:    85	        state.remove_item(order_in(State.EMPTY), "pizza", "margherita", None)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4697:    89	def test_read_back_empty():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4699:    91	        state.read_back(order_in(State.EMPTY))
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4703:    95	def test_read_back_collecting_needs_customer():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4705:    97	        state.read_back(order_in(State.COLLECTING))
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4736:   128	        state.remove_item(o, "pasta", "pesto", None)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4750:   142	    state.remove_item(o, "pizza", "margherita", None)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4770:   162	def test_confirm_without_read_back():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4774:   166	    assert e.value.code == "read_back_required"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4779:   171	    state.read_back(o)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4787:   179	def test_read_back_of_old_revision_does_not_allow_confirm():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4789:   181	    state.read_back(o)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4793:   185	    assert e.value.code == "read_back_required"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4803:   195	    state.remove_item(o, "pizza", "margherita", None)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4814:   206	def test_same_code_different_extras_is_separate_line():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4817:   209	    state.add_items(o, [item(qty=1, extras=["mushrooms"])])
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4824:   216	    state.remove_item(o, "pizza", "margherita", 1)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4826:   218	    state.remove_item(o, "pizza", "margherita", 5)  # >= qty removes line
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4833:   225	    state.remove_item(o, "pizza", "margherita", None)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4843:   235	    state.remove_item(o, "pasta", "tonno", None)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4848:   240	    """Same (type, code), different extras: no-qty removal takes them all."""
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4850:   242	    state.add_items(o, [item(qty=1), item(qty=1, extras=["mushrooms"])])
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4851:   243	    state.remove_item(o, "pizza", "margherita", None)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4857:   249	    state.add_items(o, [item(qty=2), item(qty=2, extras=["mushrooms"])])
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4858:   250	    state.remove_item(o, "pizza", "margherita", 1)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4859:   251	    assert [(i.extras, i.qty) for i in o.items] == \
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4869:--- tests/test_tools.py
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4933:    64	def test_extras_controlled_vocabulary(menu):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4934:    65	    menu.validate_extras(["mushrooms", "pineapple"])  # ok
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4936:    67	        menu.validate_extras(["unicorn_dust"])
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4940:    71	# --- pizzasim client typed errors (httpx MockTransport) -------------------
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4951:    82	def test_auth_error_mapped():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4963:    94	def test_422_mapped_with_details():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4966:    97	            respond(422, fixture("error_422.json"))
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:4968:    99	    assert "valid pizza code" in e.value.details[0]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5004:   135	    """Scripted stand-in for PizzaSim in dispatch tests."""
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5011:   142	        self.order_details = {}  # id -> detail payload
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5025:   156	        if order_id not in self.order_details:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5027:   158	        return self.order_details[order_id]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5030:   161	        return {"street": street, "deliverable": True}
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5050:   181	    tools.dispatch(order, menu, fake, "read_back", {})
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5061:   192	    assert result["menu"]["toppings"]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5068:   199	    assert snap["customer"] is None and snap["read_back_done"] is False
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5071:   202	def test_unknown_item_error_shape(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5075:   206	    err = result["error"]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5089:   220	    assert result["error"]["code"] == "unknown_item"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5100:   231	        assert result["error"]["code"] == "invalid_quantity", bad
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5107:   238	                                        "extras": ["unicorn_dust"]}]})
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5108:   239	    assert result["error"]["code"] == "invalid_extra"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5113:   244	    result = tools.dispatch(order, menu, fake, "remove_item",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5117:   248	    result = tools.dispatch(order, menu, fake, "remove_item",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5130:--- tests/test_transcripts.py
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5205:    75	        return {"street": street, "deliverable": True}
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5220:    90	    calls, error_codes = [], []
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5225:    95	        if event["type"] == "tool_result" and "error" in event["result"]:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5226:    96	            error_codes.append(event["result"]["error"]["code"])
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5236:   106	    assert error_codes == expect["error_codes"]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5305:    self.hook.pytest_load_initial_conftests(
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5322:  File "/home/rob/.local/lib/python3.13/site-packages/_pytest/warnings.py", line 128, in pytest_load_initial_conftests
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5328:  File "/home/rob/.local/lib/python3.13/site-packages/_pytest/capture.py", line 170, in pytest_load_initial_conftests
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5359:/bin/bash -lc "rg -n '"'^def test_'"' tests/test_state.py tests/test_tools.py tests/test_transcripts.py" in /home/rob/bpm-pizza-vibecoding-solution
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5367:tests/test_transcripts.py:79:def test_golden_transcript(path):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5368:tests/test_transcripts.py:116:def test_five_transcripts_exist():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5369:tests/test_transcripts.py:120:def test_gateway_timeout_apology():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5370:tests/test_state.py:41:def test_full_happy_path():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5371:tests/test_state.py:58:def test_customer_before_items_is_legal_and_stays_empty():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5372:tests/test_state.py:76:def test_submitted_is_terminal(mutate):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5373:tests/test_state.py:83:def test_remove_from_empty():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5374:tests/test_state.py:89:def test_read_back_empty():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5375:tests/test_state.py:95:def test_read_back_collecting_needs_customer():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5376:tests/test_state.py:102:def test_confirm_illegal_states(st):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5377:tests/test_state.py:109:def test_confirm_when_already_confirmed():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5378:tests/test_state.py:117:def test_submit_outside_confirmed(st):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5379:tests/test_state.py:125:def test_remove_unknown_line():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5380:tests/test_state.py:134:def test_add_after_confirmed_demotes_to_ready():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5381:tests/test_state.py:140:def test_remove_after_confirmed_demotes():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5382:tests/test_state.py:146:def test_set_customer_after_confirmed_demotes():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5383:tests/test_state.py:152:def test_confirmation_does_not_survive_demotion():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5384:tests/test_state.py:162:def test_confirm_without_read_back():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5385:tests/test_state.py:169:def test_confirm_with_stale_revision():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5386:tests/test_state.py:179:def test_read_back_of_old_revision_does_not_allow_confirm():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5387:tests/test_state.py:190:def test_revision_increments_on_every_mutation():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5388:tests/test_state.py:199:def test_merge_same_line():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5389:tests/test_state.py:206:def test_same_code_different_extras_is_separate_line():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5390:tests/test_state.py:213:def test_partial_remove():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5391:tests/test_state.py:223:def test_remove_to_empty_and_readd():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5392:tests/test_state.py:231:def test_type_and_code_key_removal():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5393:tests/test_state.py:239:def test_remove_without_qty_clears_all_variants():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5394:tests/test_state.py:247:def test_remove_with_qty_reduces_most_recent_variant():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5395:tests/test_state.py:255:def test_submit_attempt_timestamp_set_once():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5396:tests/test_tools.py:38:def test_known_codes(menu):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5397:tests/test_tools.py:43:def test_tonno_collision_is_per_type(menu):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5398:tests/test_tools.py:49:def test_unknown_code_gives_candidates(menu):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5399:tests/test_tools.py:57:def test_wrong_type_falls_back_to_other_type(menu):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5400:tests/test_tools.py:64:def test_extras_controlled_vocabulary(menu):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5401:tests/test_tools.py:82:def test_auth_error_mapped():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5402:tests/test_tools.py:89:def test_404_mapped():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5403:tests/test_tools.py:94:def test_422_mapped_with_details():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5404:tests/test_tools.py:102:def test_5xx_mapped():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5405:tests/test_tools.py:107:def test_timeout_mapped():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5406:tests/test_tools.py:114:def test_pizzeria_name_startup_check():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5407:tests/test_tools.py:125:def test_submit_parses_order_created():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5408:tests/test_tools.py:188:def test_every_success_carries_full_snapshot(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5409:tests/test_tools.py:202:def test_unknown_item_error_shape(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5410:tests/test_tools.py:212:def test_add_is_atomic(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5411:tests/test_tools.py:224:def test_invalid_quantity_not_parsed(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5412:tests/test_tools.py:234:def test_invalid_extra_via_dispatch(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5413:tests/test_tools.py:242:def test_remove_semantics(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5414:tests/test_tools.py:254:def test_submit_success(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5415:tests/test_tools.py:263:def test_submit_outside_confirmed_is_tool_error(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5416:tests/test_tools.py:271:def test_empty_basket_submit(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5417:tests/test_tools.py:277:def test_submit_timeout_then_recovery_via_list(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5418:tests/test_tools.py:301:def test_recovery_rejects_candidate_with_different_items(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5419:tests/test_tools.py:322:def test_mutation_after_submit_timeout_clears_recovery_state(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5420:tests/test_tools.py:350:def test_submit_timeout_verified_absent_allows_one_retry(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5421:tests/test_tools.py:365:def test_submit_unknown_when_list_unavailable(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5422:tests/test_tools.py:375:def test_submit_422_keeps_basket(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5423:tests/test_tools.py:385:def test_auth_error_no_retry(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5424:tests/test_tools.py:393:def test_street_omitted_from_submit_body(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5425:tests/test_tools.py:418:def test_check_street(menu, fake):
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5426:tests/test_tools.py:431:def test_live_acceptance():
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5468:    40	    lang: str  # PIZZERIA_LANG: greeting language = pizzeria country
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5472:    44	        lang = require_env("PIZZERIA_LANG").lower()
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5475:    47	                "PIZZERIA_LANG must be 'de' or 'en', got something else"
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5573:   145	                event({"type": "error", "error": str(exc)})
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5613:   185	        event({"type": "error", "error": "tool loop guard exceeded"})
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5697:    38	  const details = document.createElement("details");
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5698:    39	  details.className = "steps";
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5699:    40	  details.innerHTML = "<summary>Zwischenschritte</summary>";
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5700:    41	  chat.appendChild(details);
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5701:    42	  return details;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5737:    78	        } else if (ev.type === "error") {
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5820:   161	    speechEnabled = cfg.speech;    // unset SPEECH_URL → nothing rendered
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5846:    17	details.steps { font-size: .78rem; color: #666; margin: .2rem 0 .6rem; }
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5847:    18	details.steps summary { cursor: pointer; user-select: none; }
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5848:    19	details.steps pre { white-space: pre-wrap; word-break: break-all;
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5864:     4	proxies the optional self-hosted speech service (STT/TTS). If SPEECH_URL is
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5894:    34	    enabled only if SPEECH_URL is set, answers, and models are configured."""
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5897:    37	        self.url = optional_env("SPEECH_URL")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5898:    38	        self.stt_model = optional_env("SPEECH_STT_MODEL")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5899:    39	        self.tts_model = optional_env("SPEECH_TTS_MODEL")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5900:    40	        self.voice = optional_env("SPEECH_TTS_VOICE")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:5918:    58	        print(f"Configuration error: {exc}", file=sys.stderr)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6008:   148	            "language": app.state.config.lang}  # STT hint only
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6052:base=pathlib.Path('tests')
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6073:base=pathlib.Path('tests')
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6093:/bin/bash -lc "git log --oneline -- reviews/scores.md reviews/round1-plan.md reviews/round2-plan.md reviews/round3-plan.md reviews/round4-impl.md reviews/round5-impl.md reviews/round6-impl.md reviews/round7-hotfix.md reviews/round8-hotfix.md decisions/qa.md core channels tests | sed -n '1,120p'" in /home/rob/bpm-pizza-vibecoding-solution
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6098:     4	{"error": {"code", "message", "candidates"}} with a speakable message.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6122:    28	        "extras": {"type": "array", "items": {"type": "string"}},
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6130:    36	                    "names, and the available extra toppings.",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6140:    46	    {"name": "remove_item",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6158:    64	    {"name": "read_back",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6188:    94	def _error(code: str, message: str, candidates: list | None = None) -> dict:
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6189:    95	    return {"error": {"code": code, "message": message,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6210:   116	        return _error(exc.code, exc.message, exc.candidates)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6212:   118	        return _error(exc.code, exc.message)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6214:   120	        return _error("api_unavailable",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6217:   123	        return _error("api_unavailable",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6220:   126	        return _error("api_unavailable",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6232:   138	            extras = raw.get("extras") or []
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6233:   139	            menu.validate_extras(extras)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6240:   146	                extras=extras,
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6243:   149	            return _error("invalid_quantity", "What can I get you?")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6247:   153	    if name == "remove_item":
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6249:   155	        state.remove_item(order, args.get("type", ""), args.get("code", ""),
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6256:   162	            return _error("invalid_state", "I still need a name.")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6262:   168	    if name == "read_back":
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6263:   169	        state.read_back(order)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6269:   175	            return _error("stale_revision",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6280:   186	                "deliverable": bool(result.get("deliverable")),
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6283:   189	    return _error("unknown_tool", "Something went wrong on my side.")
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6293:   199	            (e["type"], e["code"], e["qty"], tuple(sorted(e["extras"])))
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6297:   203	             "extras": list(i.extras)} for i in basket]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6312:   218	            return _error("submit_unknown", _UNSURE)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6324:   230	                return _error("submit_unknown", _UNSURE)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6339:   245	              "extras": list(i.extras)} for i in order.items]
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6343:   249	        return _error("submit_failed",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6345:   251	                      + "; ".join(exc.details))
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6347:   253	        return _error("api_unavailable",
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6351:   257	        return _error("submit_unknown", _UNSURE)
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6375:0ce98c6 Menu validation, PizzaSim client, tool dispatch + fixture tests
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6376:f670920 Core order model + state machine, exhaustive unit tests
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6386:base=pathlib.Path('tests')
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6439:base=pathlib.Path('tests')
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6470:state test_read_back_empty 1
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6471:state test_read_back_collecting_needs_customer 1
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6480:state test_confirm_without_read_back 1
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6482:state test_read_back_of_old_revision_does_not_allow_confirm 1
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6485:state test_same_code_different_extras_is_separate_line 1
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6497:tools test_extras_controlled_vocabulary 1
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6498:tools test_auth_error_mapped 1
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6500:tools test_422_mapped_with_details 1
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6506:tools test_unknown_item_error_shape 1
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6512:tools test_submit_outside_confirmed_is_tool_error 1
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6520:tools test_auth_error_no_retry 1
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6536:- The claimed artifacts exist. `core/` contains the state machine, tool dispatcher, PizzaSim client, and timeout-recovery path in [core/state.py](/home/rob/bpm-pizza-vibecoding-solution/core/state.py), [core/tools.py](/home/rob/bpm-pizza-vibecoding-solution/core/tools.py), [core/pizzasim.py](/home/rob/bpm-pizza-vibecoding-solution/core/pizzasim.py), and [core/agent.py](/home/rob/bpm-pizza-vibecoding-solution/core/agent.py). `channels/cli.py`, `channels/web.py`, and the static web UI files exist. [decisions/qa.md](/home/rob/bpm-pizza-vibecoding-solution/decisions/qa.md) exists and records the `PIZZERIA_LANG` oracle decision.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6537:- The “71 deterministic tests” claim is internally supported by the source, but I could not rerun `pytest` in this sandbox because there is no usable temp directory. Source count is still consistent: 72 total collected cases by definition, of which 1 is the opt-in live acceptance test in [tests/test_tools.py](/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py), leaving 71 deterministic tests.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6538:- The dangerous part is not “is there enough v1 code?” There is. The dangerous part is that v1 bakes in some assumptions that v2 directly kills: one process-wide `PizzaSim` client pinned to one tenant in [channels/web.py](/home/rob/bpm-pizza-vibecoding-solution/channels/web.py), one process-wide language in [core/agent.py](/home/rob/bpm-pizza-vibecoding-solution/core/agent.py), and a web contract/UI that is nowhere close to the new spec in [channels/static/index.html](/home/rob/bpm-pizza-vibecoding-solution/channels/static/index.html) and [channels/static/app.js](/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js). Current UI also does not enforce the new “no message ends unanswered” invariant.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6543:1. `channels/web.py` currently creates one app-wide `PizzaSim` client and one app-wide `Agent`, both bound to a single `PIZZERIA_ID`. How exactly will retrofit remove that singleton tenant assumption without smuggling tenant logic into the transport, and where will per-session `{pizzeria_id, pizzeria_name, menu, order, language}` live?
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6544:2. `core/agent.py` bakes `PIZZERIA_LANG` into `AgentConfig.lang`, the system prompt is fixed at session creation, and even fallback apologies use that startup language. V2 requires a UI language switch that affects replies and STT/TTS per session. What is the migration path that avoids stale prompts, mixed-language error messages, and cross-session leakage?
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6550:PRELIMINARY LEANING: RETROFIT | The core and review trail are worth preserving, but only if you first admit that tenant and language are no longer process-global and that the web contract needs a substantial redesign, not a cosmetic patch.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6556:- The claimed artifacts exist. `core/` contains the state machine, tool dispatcher, PizzaSim client, and timeout-recovery path in [core/state.py](/home/rob/bpm-pizza-vibecoding-solution/core/state.py), [core/tools.py](/home/rob/bpm-pizza-vibecoding-solution/core/tools.py), [core/pizzasim.py](/home/rob/bpm-pizza-vibecoding-solution/core/pizzasim.py), and [core/agent.py](/home/rob/bpm-pizza-vibecoding-solution/core/agent.py). `channels/cli.py`, `channels/web.py`, and the static web UI files exist. [decisions/qa.md](/home/rob/bpm-pizza-vibecoding-solution/decisions/qa.md) exists and records the `PIZZERIA_LANG` oracle decision.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6557:- The “71 deterministic tests” claim is internally supported by the source, but I could not rerun `pytest` in this sandbox because there is no usable temp directory. Source count is still consistent: 72 total collected cases by definition, of which 1 is the opt-in live acceptance test in [tests/test_tools.py](/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py), leaving 71 deterministic tests.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6558:- The dangerous part is not “is there enough v1 code?” There is. The dangerous part is that v1 bakes in some assumptions that v2 directly kills: one process-wide `PizzaSim` client pinned to one tenant in [channels/web.py](/home/rob/bpm-pizza-vibecoding-solution/channels/web.py), one process-wide language in [core/agent.py](/home/rob/bpm-pizza-vibecoding-solution/core/agent.py), and a web contract/UI that is nowhere close to the new spec in [channels/static/index.html](/home/rob/bpm-pizza-vibecoding-solution/channels/static/index.html) and [channels/static/app.js](/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js). Current UI also does not enforce the new “no message ends unanswered” invariant.
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6563:1. `channels/web.py` currently creates one app-wide `PizzaSim` client and one app-wide `Agent`, both bound to a single `PIZZERIA_ID`. How exactly will retrofit remove that singleton tenant assumption without smuggling tenant logic into the transport, and where will per-session `{pizzeria_id, pizzeria_name, menu, order, language}` live?
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6564:2. `core/agent.py` bakes `PIZZERIA_LANG` into `AgentConfig.lang`, the system prompt is fixed at session creation, and even fallback apologies use that startup language. V2 requires a UI language switch that affects replies and STT/TTS per session. What is the migration path that avoids stale prompts, mixed-language error messages, and cross-session leakage?
/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6570:PRELIMINARY LEANING: RETROFIT | The core and review trail are worth preserving, but only if you first admit that tenant and language are no longer process-global and that the web contract needs a substantial redesign, not a cosmetic patch.

codex
I have v2 and most of v3 loaded. One of the named files does not exist as given, so I’m checking the exact v1 filename and pulling the remaining v3 sections plus the local oracle decision that the implementer’s critique relies on.
exec
/bin/bash -lc "ls -1 /home/rob/bpm-pizza-vibecoding-solution | rg '"'^SPEC'"'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,220p' /home/rob/.agents/skills/using-superpowers/references/codex-tools.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '520,820p' /home/rob/bpm-pizza-vibecoding-solution/SPEC.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,220p' /home/rob/bpm-pizza-vibecoding-solution/decisions/qa.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '260,520p' /home/rob/bpm-pizza-vibecoding-solution/SPEC.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' /home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 431ms:
SPEC.md
SPEC_20260801_1.md
SPEC_20260801_2.md

 succeeded in 409ms:
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

 succeeded in 542ms:
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
| `set_customer` | `first_name`, optional `street_one` | customer as stored |
| `read_back` | — | basket, customer, revision — the text the agent reads out |
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

---

## Conversation policy

This is what the system prompt must produce. Write the prompt to achieve it;
do not paste this section into it verbatim.

- Greet first, in the customer's UI language, and offer help — one sentence,
  not a menu recital.
- **One question per turn.** Never stack "name, street and what would you
  like?"
- Never state a menu item or a price that did not come from `get_menu` in this
  session. Price questions are normal questions, and so is "what does my
  basket come to?"
- Collect first name and street. If the customer declines the street, accept
  it — it is optional in the API.
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

### Header

- **The pizzeria being ordered from, by name**, prominent and always visible.
- **A selector to change pizzeria, filled from the API and from nowhere
  else.** The list comes from `GET /pizzerias` at load time. No hardcoded
  names, no bundled list, no fallback entry when the call fails — if it
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
- **Nothing about the speech stack is written into source.** Base URL, models,
  voice and language come from the environment, exactly like the chat model.
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
| `404` on the pizzeria path | fail at startup, not mid-call | — (process refuses to start) |
| `422` validation | surface field, keep basket | targeted question about the offending item |
| `5xx` on submit | **no blind retry** | "I'm not sure that went through — let me check" |
| Timeout on submit | mark `UNKNOWN`, verify via `GET /pizzerias/{id}/orders` before any retry | as above |
| Unknown item code | `unknown_item` + candidates | "I have Margherita or Marinara — which one?" |
| Empty basket at submit | reject transition | "What can I get you?" |
| Menu fetch fails at start | fail fast | "We're not taking orders right now" |
| Pizzeria list fetch fails | no selector, say so | list unavailable — no fallback entry |
| Speech service down | hide speech controls | text UI unaffected |

The submit-timeout case is the one that matters: a blind retry doubles a real
order. Recovery: verify against the pizzeria's order list; if that too fails,
tell the customer honestly.

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
- **Golden transcripts:** five scripted conversations against a stub model
  replaying fixed tool calls — happy path, correction, unknown item, customer
  changes mind after read-back, submit timeout. Assert final state and the
  calls actually made.
- **Browser end-to-end, not optional.** At least one test drives the real
  page in a headless browser — types a message, waits for a rendered reply,
  walks a full order to submission — asserting against the DOM, not the API.
  `curl` proves the server works and proves nothing about the product; the
  customer never talks to `curl`. Include three failure paths: a tool error, a
  stream ending without a final message, the gateway unreachable — each must
  leave a visible message on the page.
- **The acceptance test is live**, opt-in via env flag, the only test that
  touches the real API. Full conversation, submit, then read the pizzeria's
  orders back and assert the four points under *What done looks like*. If
  this fails, the product does not work, whatever else is green.
- **Speech**, manual: dictate an order, a name that needs correcting, a menu
  question — plus one run with `SPEECH_URL` unset, which must render a usable
  text-only UI and place an order normally.


 succeeded in 605ms:
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

 succeeded in 584ms:
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

## What done looks like

There is exactly one success condition, and everything else in this document
exists to serve it:

**A customer talks to the agent, and the resulting order appears in the API
under the configured pizzeria — with the right customer, the right items, the
right quantities.**

Concretely, and this is the acceptance criterion:

1. `POST /pizzerias/{PIZZERIA_ID}/orders` returned an order id.
2. Reading that pizzeria's orders back shows the order, and it is visible on the
   dashboard for that pizzeria.
3. The customer name is the one the customer gave.
4. The items and quantities are the ones that were read back and confirmed —
   not a superset, not a subset, not a near match on the item code.

Nothing else counts as done. A green test suite, a clean architecture, a
pleasant interface: none of it is the product. The order on the board is the
product.

**Four failures that look like success**, each of which is a failed run and not
a partial one:

- The order landed under a **different pizzeria** than the configured one.
- A retry after a timeout created the order **twice**.
- A misheard or mistyped name created a **new customer** instead of matching the
  intended one.
- The order was submitted **without the customer confirming** the read-back.

Every rule in this spec — the state machine, the revision-bound confirmation,
the ban on blind retries, the name read-back, the tenant coming from the URL
path — exists to prevent exactly one of those four.

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
- **Menu, prices, cart, customer, submit.** The full happy path plus correction
  ("no, make that three"), removal, and abandonment. The customer can ask what
  is on offer and what individual items cost, and can see what the basket comes
  to before confirming.
- **Several pizzerias.** The customer chooses which one they are ordering from,
  and can change it. `PIZZERIA_ID` is the preselection, not a restriction.
- **The success moment:** the order appears in the PizzaSim dashboard under the
  configured pizzeria, with the right customer, items and quantities.
- **Deterministic tests** that run with no network and no LLM.
- **Structured logging** of every turn: user text, model tool calls, tool
  results, state transitions. One line per event, JSON, to a file.

### Out (explicitly)

- Payment and anything financial beyond showing prices the API supplies.
- Delivery routing, or an ETA of our own invention.
- Accounts, auth, sessions surviving a process restart.
- Modifying or cancelling an order after it was submitted.
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
| `PIZZERIA_ID` | UUID of the pizzeria preselected on first load |
| `APP_VERSION` | Release version, `x.y.z`, shown in the footer |
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

### Contract facts — verified against the live API (2026-07-31/08-01)

All former open questions were resolved by probing the live API
(`GET /menu`, `GET /pizzerias`, `POST /pizzerias/{id}/orders` — valid and
invalid bodies —, `GET /pizzerias/{id}/orders`,
`GET /pizzerias/{id}/orders/{order_id}`, `GET /location`, plus the dashboard
and documentation pages). Facts below are from real responses, not
documentation.

1. **Order response field name: `order_id`.** A successful
   `POST /pizzerias/{id}/orders` returns
   `{"order_id": "<uuid>", "status": "ordered", "eta_seconds": <int>}`.
   The **list** endpoint uses `id` for the same value — the two names coexist,
   one per endpoint.
2. **The list endpoint exists.** `GET /pizzerias/{id}/orders` (auth:
   `X-API-Key`) returns `{"orders": [...]}`, newest first, each with `id`,
   `customer_id`, `created_at`, `ready_at`, `status`, `delivered_at`,
   `first_name` — but **no items**. A detail endpoint
   `GET /pizzerias/{id}/orders/{order_id}` (auth: `X-API-Key`) returns the
   full order incl. `customer` and `items[]`, so submit-timeout recovery
   shortlists by `first_name` + `created_at` recency and then verifies the
   candidate's items against the basket before adopting it. The acceptance
   test asserts items and quantities through the same detail endpoint.
3. **Menu item shape:** `{"code", "name", "base": [ingredients], "price"}`.
   `price` is a number in euros (e.g. `8.5`) — the source for every price
   answer and the basket total; no other financial data exists in the API.
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
8. **The pizzeria dashboard** lives at
   `{PIZZASIM_URL}/dashboard/pizzerias/{id}` (confirmed in the dashboard's
   own routing code); the overview is `{PIZZASIM_URL}/dashboard`. The

 succeeded in 618ms:

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
- No model name of any kind is hardcoded. A missing runtime value is a
  startup failure, not a default.
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

0. **Contracts.** Resolve the open contract questions against the live API,
   move the answers into the facts, commit. The open list only shrinks — a
   verified fact never becomes a question again.
1. **Core.** Order model, state machine, tool layer, tests. No LLM, no
   network. Pass when the unit tests are green.
2. **Agent loop.** Model, tools, system prompt, one turn end to end.
3. **CLI.** Full conversation, real API, an order visible on the dashboard.
4. **Web.** FastAPI on 8888, same core. Pass only when you have opened the
   page in a browser, switched pizzeria, asked a price question, placed an
   order through the page, and seen it on that pizzeria's dashboard — not
   when the endpoint answers `curl`.
5. **Speech.** Wire the speech service into the web UI, spoken-answer policy,
   and the degraded no-speech path.
6. **Harden.** Walk the error table, force each case, fix what breaks.

After each pass, review your own work as the reviewer who has to reject it:
what would a hostile reader find first? Fix that, then move on. Stop only when
a full pass over the spec finds nothing left that you know how to improve.

---

## Deliverables

```
.
├── SPEC.md                  ← this file
├── README.md                ← how to run each channel
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
│   ├── speech.py            ← speech service client
│   └── static/              ← web UI incl. speech input/output
├── prompts/
│   ├── system.de.md
│   └── system.en.md
├── tests/
│   ├── fixtures/            ← recorded API responses
│   ├── test_state.py
│   ├── test_tools.py
│   ├── test_web_e2e.py      ← headless browser, DOM assertions
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
| Tenancy | Customer-selectable; `PIZZERIA_ID` preselects, never restricts; tenant in the URL path |
| Pizzeria selector | Filled from the API only; no fallback entry |
| Prices | Shown from the API; no payment, no invented figures |
| Transports | One core, two channels (CLI, web), no logic in the channels |
| Speech | Self-hosted container, OpenAI-compatible HTTP; no vendor, no browser speech API |
| Web UI | Pizzeria name, basket and connection state always visible; no message ends unanswered |
| Version | `x.y.z` in the footer, raised every release |
| Derived URLs | Dashboard and docs built from `PIZZASIM_URL`, never literal |
| Languages | DE + EN, mirrored per turn |
| Confirmation | Mandatory read-back tied to a basket revision |
| Parsing | The model parses. No regex order parser, ever. |
| HTTP | A real client with timeouts. No `subprocess curl`. |
| Persistence | None beyond the process and the PizzaSim API |
| Errors | Typed in code, plain language to the customer |
| Contract facts | Verified facts never return to the open list; the list only shrinks |
| Implementer | One agent only — nothing else writes code |
| Reviewer | A second, independent agent, read-only, judge and devil's advocate |
| Models | Never named, never hardcoded — environment configuration |
| Build tooling | Not specified here; the operator picks it |
| Proof | Verified through the browser and the live API, never only through `curl` |
| Definition of done | The judge approved, not "it runs" |

## Decisions deferred

- Extras and modifiers beyond a passthrough `extras[]`.
- Post-submit modification or cancellation.
- Multi-turn memory across sessions ("the usual").
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

codex
The main gaps are now visible in v3 itself; I’m checking v1 and the actual repo layout so I can distinguish “spec flaw” from “already implemented in approved v1”. Then I’ll attack the implementer’s list point by point instead of just endorsing it.
exec
/bin/bash -lc "ls -R /home/rob/bpm-pizza-vibecoding-solution | sed -n '1,260p'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "diff -u /home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md /home/rob/bpm-pizza-vibecoding-solution/SPEC.md | sed -n '1,260p'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' /home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "diff -u /home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md /home/rob/bpm-pizza-vibecoding-solution/SPEC.md | sed -n '1,260p'" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 263ms:
--- /home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md	2026-08-01 08:30:48.275979896 +0200
+++ /home/rob/bpm-pizza-vibecoding-solution/SPEC.md	2026-08-01 09:34:41.309119224 +0200
@@ -2,8 +2,8 @@
 
 > Hand this to a coding agent as the entire task:
 > `FOLLOW INSTRUCTIONS PRECISELY AT "SPEC.MD"`.
-> This file is the source of truth for what the agent is. Everything else in the
-> repo — code, tests, prompts, tickets — derives from it.
+> This file is the source of truth for what the product is. Everything else in
+> the repo — code, tests, prompts, tickets — derives from it.
 
 ---
 
@@ -11,42 +11,79 @@
 
 The **shape** of this document is not ours. It is borrowed from Cedric Mössner —
 **The Morpheus** ([youtube.com/@TheMorpheusTutorials](https://www.youtube.com/@TheMorpheusTutorials)),
-who writes exactly one `SPEC.md` per project and hands the identical file to every
-new model in order to compare them. The prompt he sends alongside it is a single
-line — `FOLLOW INSTRUCTIONS PRECISELY AT "SPEC.MD"` — which is why that line, and
-not a long prompt, stands at the top of this file.
-
-The sections adopted from his specs: *Soul*, *The One Load-Bearing Idea*, hard
-*Scope In / Out*, an explicit autonomy clause, work *in passes* with verification
-after each, a file-level *Deliverables* list, *Decisions Locked / Deferred*, and
-the one-hour *ticket sizing rules*.
+who writes exactly one `SPEC.md` per project and hands the identical file to
+every new model in order to compare them. The prompt he sends alongside it is a
+single line — `FOLLOW INSTRUCTIONS PRECISELY AT "SPEC.MD"` — which is why that
+line, and not a long prompt, stands at the top of this file.
+
+Sections adopted from his specs: *Soul*, *The One Load-Bearing Idea*, hard
+*Scope In / Out*, an explicit autonomy clause, work *in passes* with
+verification after each, a file-level *Deliverables* list, *Decisions Locked /
+Deferred*, and the one-hour *ticket sizing rules*.
 
 Reference specs:
-
-- [github.com/TheMorpheus407/morphcook](https://github.com/TheMorpheus407/morphcook)
-  — offline Flutter recipe app; one spec, seven model implementations.
-- [github.com/TheMorpheus407/hogwarts-blender-benchmark](https://github.com/TheMorpheus407/hogwarts-blender-benchmark)
-  — fully procedural Blender build; `prompt.txt` plus `SPEC.md`.
+[morphcook](https://github.com/TheMorpheus407/morphcook) — offline Flutter
+recipe app; one spec, seven model implementations.
+[hogwarts-blender-benchmark](https://github.com/TheMorpheus407/hogwarts-blender-benchmark)
+— fully procedural Blender build; `prompt.txt` plus `SPEC.md`.
 
 The content below is ours. The form is his — with thanks.
 
 ---
 
+## What done looks like
+
+There is exactly one success condition, and everything else in this document
+exists to serve it:
+
+**A customer talks to the agent, and the resulting order appears in the API
+under the pizzeria they chose — with the right customer, the right items, the
+right quantities.**
+
+Concretely, and this is the acceptance criterion:
+
+1. `POST /pizzerias/{id}/orders` returned an order id.
+2. Reading that pizzeria's orders back shows the order, and it is visible on
+   that pizzeria's dashboard.
+3. The customer name is the one the customer gave.
+4. The items and quantities are the ones that were read back and confirmed —
+   not a superset, not a subset, not a near match on the item code.
+
+Nothing else counts as done. A green test suite, a clean architecture, a
+pleasant interface: none of it is the product. **The order on the board is the
+product.**
+
+**Four failures that look like success**, each a failed run and not a partial
+one:
+
+- The order landed under a **different pizzeria** than the one the customer
+  chose.
+- A retry after a timeout created the order **twice**.
+- A misheard or mistyped name created a **new customer** instead of matching
+  the intended one.
+- The order was submitted **without the customer confirming** the read-back.
+
+Every rule below — the state machine, the revision-bound confirmation, the ban
+on blind retries, the name read-back, the tenant in the URL path — exists to
+prevent exactly one of those four.
+
+---
+
 ## Soul
 
-Ordering food by phone works because the person on the other end keeps the order
-in their head, reads it back to you, and only then walks to the kitchen. Nothing
-is cooked before you said yes.
+Ordering food by phone works because the person on the other end keeps the
+order in their head, reads it back to you, and only then walks to the kitchen.
+Nothing is cooked before you said yes.
 
 Most LLM ordering demos invert this. The model holds the order in its context,
 guesses item names that sound close enough, and fires the write call the moment
-it feels confident. It works in the demo and fails on the fourth turn, in a noisy
-room, when the customer changes their mind.
+it feels confident. It works in the demo and fails on the fourth turn, in a
+noisy room, when the customer changes their mind.
 
-This agent puts the order back where it belongs: **in the code**. The model does
-the one thing it is genuinely good at — turning messy human speech into intent —
-and nothing else. It never holds the cart, never invents a menu item, and never
-reaches the kitchen without a spoken confirmation.
+This agent puts the order back where it belongs: **in the code**. The model
+does the one thing it is genuinely good at — turning messy human speech into
+intent — and nothing else. It never holds the cart, never invents a menu item,
+and never reaches the kitchen without a confirmed read-back.
 
 **Core belief:** a language model is a great waiter and a terrible order pad.
 
@@ -56,17 +93,17 @@
 
 **The order is a state machine owned by the code. The model only speaks.**
 
-- There is exactly one `Order` object per conversation, held by the runtime.
-- The model cannot write to it directly. It can only call tools that request a
+- Exactly one `Order` object per conversation, held by the runtime.
+- The model cannot write to it directly. It calls tools that request a
   transition, and every transition is validated before it is applied.
 - Every item code is validated against the **live menu**. An unknown code is a
-  tool error carrying candidate matches — never a silent guess, never a fallback
-  to a hardcoded list.
-- `submit_order` is the only call that reaches the network as a write, and it is
-  legal in exactly one state: `CONFIRMED`. The only way into `CONFIRMED` is a
-  read-back the customer answered yes to.
-- The same core serves every channel. A transport carries words in and words
-  out; it owns no order logic whatsoever.
+  tool error carrying candidate matches — never a silent guess, never a
+  fallback to a hardcoded list.
+- `submit_order` is the only network write, legal in exactly one state:
+  `CONFIRMED`. The only way into `CONFIRMED` is a read-back the customer
+  answered yes to.
+- One core serves every channel. A transport carries words in and words out;
+  it owns no order logic whatsoever.
 
 This one rule replaces prompt-engineering the model into good behaviour. If the
 model misbehaves, the state machine refuses — and the refusal is a tool result
@@ -74,72 +111,39 @@
 
 ---
 
-## What done looks like
-
-There is exactly one success condition, and everything else in this document
-exists to serve it:
-
-**A customer talks to the agent, and the resulting order appears in the API
-under the configured pizzeria — with the right customer, the right items, the
-right quantities.**
-
-Concretely, and this is the acceptance criterion:
-
-1. `POST /pizzerias/{PIZZERIA_ID}/orders` returned an order id.
-2. Reading that pizzeria's orders back shows the order, and it is visible on the
-   dashboard for that pizzeria.
-3. The customer name is the one the customer gave.
-4. The items and quantities are the ones that were read back and confirmed —
-   not a superset, not a subset, not a near match on the item code.
-
-Nothing else counts as done. A green test suite, a clean architecture, a
-pleasant interface: none of it is the product. The order on the board is the
-product.
-
-**Four failures that look like success**, each of which is a failed run and not
-a partial one:
-
-- The order landed under a **different pizzeria** than the configured one.
-- A retry after a timeout created the order **twice**.
-- A misheard or mistyped name created a **new customer** instead of matching the
-  intended one.
-- The order was submitted **without the customer confirming** the read-back.
-
-Every rule in this spec — the state machine, the revision-bound confirmation,
-the ban on blind retries, the name read-back, the tenant coming from the URL
-path — exists to prevent exactly one of those four.
-
----
-
 ## Scope
 
 ### In
 
 - **Two transports over one core:**
   - `cli` — interactive terminal chat.
-  - `web` — local FastAPI server on port 8888, browser chat UI, streaming the
-    agent's intermediate steps as newline-delimited JSON so tool calls and tool
-    results are visible and not just the final answer.
+  - `web` — FastAPI server on port 8888, browser chat UI, streaming the
+    agent's intermediate steps as newline-delimited JSON so tool calls and
+    tool results are visible, not just the final answer.
 - **Speech on the web transport**, served by a self-hosted CPU-only speech
   container over HTTP. See *Speech*.
+- **Several pizzerias.** The customer chooses which one they are ordering
+  from, and can change it. `PIZZERIA_ID` is the preselection, not a
+  restriction.
 - **Languages:** German and English. The agent answers in the language the
   customer used, per turn, without being told to switch.
-- **Menu, cart, customer, submit.** The full happy path plus correction
-  ("no, make that three"), removal, and abandonment.
-- **The success moment:** the order appears in the PizzaSim dashboard under the
-  configured pizzeria, with the right customer, items and quantities.
-- **Deterministic tests** that run with no network and no LLM.
+- **Menu, prices, cart, customer, submit.** The full happy path plus
+  correction ("no, make that three"), removal, and abandonment. The customer
+  can ask what is on offer and what items cost, and sees what the basket
+  comes to before confirming.
+- **Deterministic tests** that run with no network and no LLM, plus one live
+  acceptance test and a browser end-to-end test.
 - **Structured logging** of every turn: user text, model tool calls, tool
   results, state transitions. One line per event, JSON, to a file.
 
 ### Out (explicitly)
 
-- Payment, pricing totals, delivery routing, ETA prediction of our own.
+- Payment and anything financial beyond showing prices the API supplies.
+- Delivery routing, or an ETA of our own invention.
 - Accounts, auth, sessions surviving a process restart.
 - Modifying or cancelling an order after it was submitted.
-- Switching pizzeria at runtime — one process serves one `PIZZERIA_ID`.
 - Any regex or keyword parser that produces an order without the model.
-  See **Anti-patterns**; this is not a style preference, it is a hard ban.
+  See **Anti-patterns**; this is a hard ban, not a style preference.
 - Reading the whole menu aloud when the answer will be spoken.
 - Persisting customer data anywhere beyond the process and the PizzaSim API.
 
@@ -154,30 +158,41 @@
 |---|---|
 | `LITELLM_PIZZA_URL` | OpenAI-compatible gateway base URL (`/chat/completions` appended) |
 | `LITELLM_PIZZA_KEY` | Bearer token for the gateway |
-| `PIZZASIM_URL` | PizzaSim API base URL |
-| `PIZZASIM_API_KEY` | Sent as header `X-API-Key` on protected routes |
-| `PIZZERIA_ID` | UUID of the pizzeria this process serves |
 | `LITELLM_PIZZA_MODEL_1` | Model the ordering agent calls; required, no default in code |
 | `LITELLM_PIZZA_MODEL_2` | Second configured model, where the build uses one |
+| `PIZZASIM_URL` | PizzaSim API base URL; dashboard and docs links derive from it |
+| `PIZZASIM_API_KEY` | Sent as header `X-API-Key` on protected routes |
+| `PIZZERIA_ID` | UUID of the pizzeria preselected on first load |
+| `APP_VERSION` | Release version, `x.y.z`, shown in the footer |
+| `SPEECH_URL` | Base URL of the self-hosted speech service (optional) |
+| `SPEECH_STT_MODEL` | Transcription model id |
+| `SPEECH_TTS_MODEL` | Synthesis model id |
+| `SPEECH_TTS_VOICE` | Voice id |
 
 Rules:
 
-- **Nothing is hardcoded.** No UUID, no model name, no menu, no base URL —
-  not even as a fallback "just in case".
-- Missing or empty variable → exit before the first turn with a message naming
-  the variable and the file it was expected in. Never start half-configured.
+- **Nothing is hardcoded.** No UUID, no model name, no menu, no base URL, no
+  vendor — not even as a fallback "just in case".
+- Missing or empty required variable → exit before the first turn with a
+  message naming the variable and the file it was expected in. Never start
+  half-configured. `SPEECH_*` are the exception: absent means the speech

 succeeded in 270ms:
--- /home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md	2026-08-01 09:28:02.310052326 +0200
+++ /home/rob/bpm-pizza-vibecoding-solution/SPEC.md	2026-08-01 09:34:41.309119224 +0200
@@ -2,8 +2,8 @@
 
 > Hand this to a coding agent as the entire task:
 > `FOLLOW INSTRUCTIONS PRECISELY AT "SPEC.MD"`.
-> This file is the source of truth for what the agent is. Everything else in the
-> repo — code, tests, prompts, tickets — derives from it.
+> This file is the source of truth for what the product is. Everything else in
+> the repo — code, tests, prompts, tickets — derives from it.
 
 ---
 
@@ -11,42 +11,79 @@
 
 The **shape** of this document is not ours. It is borrowed from Cedric Mössner —
 **The Morpheus** ([youtube.com/@TheMorpheusTutorials](https://www.youtube.com/@TheMorpheusTutorials)),
-who writes exactly one `SPEC.md` per project and hands the identical file to every
-new model in order to compare them. The prompt he sends alongside it is a single
-line — `FOLLOW INSTRUCTIONS PRECISELY AT "SPEC.MD"` — which is why that line, and
-not a long prompt, stands at the top of this file.
-
-The sections adopted from his specs: *Soul*, *The One Load-Bearing Idea*, hard
-*Scope In / Out*, an explicit autonomy clause, work *in passes* with verification
-after each, a file-level *Deliverables* list, *Decisions Locked / Deferred*, and
-the one-hour *ticket sizing rules*.
+who writes exactly one `SPEC.md` per project and hands the identical file to
+every new model in order to compare them. The prompt he sends alongside it is a
+single line — `FOLLOW INSTRUCTIONS PRECISELY AT "SPEC.MD"` — which is why that
+line, and not a long prompt, stands at the top of this file.
+
+Sections adopted from his specs: *Soul*, *The One Load-Bearing Idea*, hard
+*Scope In / Out*, an explicit autonomy clause, work *in passes* with
+verification after each, a file-level *Deliverables* list, *Decisions Locked /
+Deferred*, and the one-hour *ticket sizing rules*.
 
 Reference specs:
-
-- [github.com/TheMorpheus407/morphcook](https://github.com/TheMorpheus407/morphcook)
-  — offline Flutter recipe app; one spec, seven model implementations.
-- [github.com/TheMorpheus407/hogwarts-blender-benchmark](https://github.com/TheMorpheus407/hogwarts-blender-benchmark)
-  — fully procedural Blender build; `prompt.txt` plus `SPEC.md`.
+[morphcook](https://github.com/TheMorpheus407/morphcook) — offline Flutter
+recipe app; one spec, seven model implementations.
+[hogwarts-blender-benchmark](https://github.com/TheMorpheus407/hogwarts-blender-benchmark)
+— fully procedural Blender build; `prompt.txt` plus `SPEC.md`.
 
 The content below is ours. The form is his — with thanks.
 
 ---
 
+## What done looks like
+
+There is exactly one success condition, and everything else in this document
+exists to serve it:
+
+**A customer talks to the agent, and the resulting order appears in the API
+under the pizzeria they chose — with the right customer, the right items, the
+right quantities.**
+
+Concretely, and this is the acceptance criterion:
+
+1. `POST /pizzerias/{id}/orders` returned an order id.
+2. Reading that pizzeria's orders back shows the order, and it is visible on
+   that pizzeria's dashboard.
+3. The customer name is the one the customer gave.
+4. The items and quantities are the ones that were read back and confirmed —
+   not a superset, not a subset, not a near match on the item code.
+
+Nothing else counts as done. A green test suite, a clean architecture, a
+pleasant interface: none of it is the product. **The order on the board is the
+product.**
+
+**Four failures that look like success**, each a failed run and not a partial
+one:
+
+- The order landed under a **different pizzeria** than the one the customer
+  chose.
+- A retry after a timeout created the order **twice**.
+- A misheard or mistyped name created a **new customer** instead of matching
+  the intended one.
+- The order was submitted **without the customer confirming** the read-back.
+
+Every rule below — the state machine, the revision-bound confirmation, the ban
+on blind retries, the name read-back, the tenant in the URL path — exists to
+prevent exactly one of those four.
+
+---
+
 ## Soul
 
-Ordering food by phone works because the person on the other end keeps the order
-in their head, reads it back to you, and only then walks to the kitchen. Nothing
-is cooked before you said yes.
+Ordering food by phone works because the person on the other end keeps the
+order in their head, reads it back to you, and only then walks to the kitchen.
+Nothing is cooked before you said yes.
 
 Most LLM ordering demos invert this. The model holds the order in its context,
 guesses item names that sound close enough, and fires the write call the moment
-it feels confident. It works in the demo and fails on the fourth turn, in a noisy
-room, when the customer changes their mind.
+it feels confident. It works in the demo and fails on the fourth turn, in a
+noisy room, when the customer changes their mind.
 
-This agent puts the order back where it belongs: **in the code**. The model does
-the one thing it is genuinely good at — turning messy human speech into intent —
-and nothing else. It never holds the cart, never invents a menu item, and never
-reaches the kitchen without a spoken confirmation.
+This agent puts the order back where it belongs: **in the code**. The model
+does the one thing it is genuinely good at — turning messy human speech into
+intent — and nothing else. It never holds the cart, never invents a menu item,
+and never reaches the kitchen without a confirmed read-back.
 
 **Core belief:** a language model is a great waiter and a terrible order pad.
 
@@ -56,17 +93,17 @@
 
 **The order is a state machine owned by the code. The model only speaks.**
 
-- There is exactly one `Order` object per conversation, held by the runtime.
-- The model cannot write to it directly. It can only call tools that request a
+- Exactly one `Order` object per conversation, held by the runtime.
+- The model cannot write to it directly. It calls tools that request a
   transition, and every transition is validated before it is applied.
 - Every item code is validated against the **live menu**. An unknown code is a
-  tool error carrying candidate matches — never a silent guess, never a fallback
-  to a hardcoded list.
-- `submit_order` is the only call that reaches the network as a write, and it is
-  legal in exactly one state: `CONFIRMED`. The only way into `CONFIRMED` is a
-  read-back the customer answered yes to.
-- The same core serves every channel. A transport carries words in and words
-  out; it owns no order logic whatsoever.
+  tool error carrying candidate matches — never a silent guess, never a
+  fallback to a hardcoded list.
+- `submit_order` is the only network write, legal in exactly one state:
+  `CONFIRMED`. The only way into `CONFIRMED` is a read-back the customer
+  answered yes to.
+- One core serves every channel. A transport carries words in and words out;
+  it owns no order logic whatsoever.
 
 This one rule replaces prompt-engineering the model into good behaviour. If the
 model misbehaves, the state machine refuses — and the refusal is a tool result
@@ -74,65 +111,28 @@
 
 ---
 
-## What done looks like
-
-There is exactly one success condition, and everything else in this document
-exists to serve it:
-
-**A customer talks to the agent, and the resulting order appears in the API
-under the configured pizzeria — with the right customer, the right items, the
-right quantities.**
-
-Concretely, and this is the acceptance criterion:
-
-1. `POST /pizzerias/{PIZZERIA_ID}/orders` returned an order id.
-2. Reading that pizzeria's orders back shows the order, and it is visible on the
-   dashboard for that pizzeria.
-3. The customer name is the one the customer gave.
-4. The items and quantities are the ones that were read back and confirmed —
-   not a superset, not a subset, not a near match on the item code.
-
-Nothing else counts as done. A green test suite, a clean architecture, a
-pleasant interface: none of it is the product. The order on the board is the
-product.
-
-**Four failures that look like success**, each of which is a failed run and not
-a partial one:
-
-- The order landed under a **different pizzeria** than the configured one.
-- A retry after a timeout created the order **twice**.
-- A misheard or mistyped name created a **new customer** instead of matching the
-  intended one.
-- The order was submitted **without the customer confirming** the read-back.
-
-Every rule in this spec — the state machine, the revision-bound confirmation,
-the ban on blind retries, the name read-back, the tenant coming from the URL
-path — exists to prevent exactly one of those four.
-
----
-
 ## Scope
 
 ### In
 
 - **Two transports over one core:**
   - `cli` — interactive terminal chat.
-  - `web` — local FastAPI server on port 8888, browser chat UI, streaming the
-    agent's intermediate steps as newline-delimited JSON so tool calls and tool
-    results are visible and not just the final answer.
+  - `web` — FastAPI server on port 8888, browser chat UI, streaming the
+    agent's intermediate steps as newline-delimited JSON so tool calls and
+    tool results are visible, not just the final answer.
 - **Speech on the web transport**, served by a self-hosted CPU-only speech
   container over HTTP. See *Speech*.
+- **Several pizzerias.** The customer chooses which one they are ordering
+  from, and can change it. `PIZZERIA_ID` is the preselection, not a
+  restriction.
 - **Languages:** German and English. The agent answers in the language the
   customer used, per turn, without being told to switch.
-- **Menu, prices, cart, customer, submit.** The full happy path plus correction
-  ("no, make that three"), removal, and abandonment. The customer can ask what
-  is on offer and what individual items cost, and can see what the basket comes
-  to before confirming.
-- **Several pizzerias.** The customer chooses which one they are ordering from,
-  and can change it. `PIZZERIA_ID` is the preselection, not a restriction.
-- **The success moment:** the order appears in the PizzaSim dashboard under the
-  configured pizzeria, with the right customer, items and quantities.
-- **Deterministic tests** that run with no network and no LLM.
+- **Menu, prices, cart, customer, submit.** The full happy path plus
+  correction ("no, make that three"), removal, and abandonment. The customer
+  can ask what is on offer and what items cost, and sees what the basket
+  comes to before confirming.
+- **Deterministic tests** that run with no network and no LLM, plus one live
+  acceptance test and a browser end-to-end test.
 - **Structured logging** of every turn: user text, model tool calls, tool
   results, state transitions. One line per event, JSON, to a file.
 
@@ -143,7 +143,7 @@
 - Accounts, auth, sessions surviving a process restart.
 - Modifying or cancelling an order after it was submitted.
 - Any regex or keyword parser that produces an order without the model.
-  See **Anti-patterns**; this is not a style preference, it is a hard ban.
+  See **Anti-patterns**; this is a hard ban, not a style preference.
 - Reading the whole menu aloud when the answer will be spoken.
 - Persisting customer data anywhere beyond the process and the PizzaSim API.
 
@@ -158,31 +158,41 @@
 |---|---|
 | `LITELLM_PIZZA_URL` | OpenAI-compatible gateway base URL (`/chat/completions` appended) |
 | `LITELLM_PIZZA_KEY` | Bearer token for the gateway |
-| `PIZZASIM_URL` | PizzaSim API base URL |
+| `LITELLM_PIZZA_MODEL_1` | Model the ordering agent calls; required, no default in code |
+| `LITELLM_PIZZA_MODEL_2` | Second configured model, where the build uses one |
+| `PIZZASIM_URL` | PizzaSim API base URL; dashboard and docs links derive from it |
 | `PIZZASIM_API_KEY` | Sent as header `X-API-Key` on protected routes |
 | `PIZZERIA_ID` | UUID of the pizzeria preselected on first load |
 | `APP_VERSION` | Release version, `x.y.z`, shown in the footer |
-| `LITELLM_PIZZA_MODEL_1` | Model the ordering agent calls; required, no default in code |
-| `LITELLM_PIZZA_MODEL_2` | Second configured model, where the build uses one |
+| `SPEECH_URL` | Base URL of the self-hosted speech service (optional) |
+| `SPEECH_STT_MODEL` | Transcription model id |
+| `SPEECH_TTS_MODEL` | Synthesis model id |
+| `SPEECH_TTS_VOICE` | Voice id |
 
 Rules:
 
-- **Nothing is hardcoded.** No UUID, no model name, no menu, no base URL —
-  not even as a fallback "just in case".
-- Missing or empty variable → exit before the first turn with a message naming
-  the variable and the file it was expected in. Never start half-configured.
+- **Nothing is hardcoded.** No UUID, no model name, no menu, no base URL, no
+  vendor — not even as a fallback "just in case".
+- Missing or empty required variable → exit before the first turn with a
+  message naming the variable and the file it was expected in. Never start
+  half-configured. `SPEECH_*` are the exception: absent means the speech
+  features are not rendered, and everything else works.

 succeeded in 331ms:
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

## What done looks like

There is exactly one success condition, and everything else in this document
exists to serve it:

**A customer talks to the agent, and the resulting order appears in the API
under the configured pizzeria — with the right customer, the right items, the
right quantities.**

Concretely, and this is the acceptance criterion:

1. `POST /pizzerias/{PIZZERIA_ID}/orders` returned an order id.
2. Reading that pizzeria's orders back shows the order, and it is visible on the
   dashboard for that pizzeria.
3. The customer name is the one the customer gave.
4. The items and quantities are the ones that were read back and confirmed —
   not a superset, not a subset, not a near match on the item code.

Nothing else counts as done. A green test suite, a clean architecture, a
pleasant interface: none of it is the product. The order on the board is the
product.

**Four failures that look like success**, each of which is a failed run and not
a partial one:

- The order landed under a **different pizzeria** than the configured one.
- A retry after a timeout created the order **twice**.
- A misheard or mistyped name created a **new customer** instead of matching the
  intended one.
- The order was submitted **without the customer confirming** the read-back.

Every rule in this spec — the state machine, the revision-bound confirmation,
the ban on blind retries, the name read-back, the tenant coming from the URL
path — exists to prevent exactly one of those four.

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
invalid bodies —, `GET /pizzerias/{id}/orders`,
`GET /pizzerias/{id}/orders/{order_id}`, `GET /location`). Facts below are
from real responses, not documentation.

1. **Order response field name: `order_id`.** A successful
   `POST /pizzerias/{id}/orders` returns
   `{"order_id": "<uuid>", "status": "ordered", "eta_seconds": <int>}`.
   The **list** endpoint uses `id` for the same value — the two names coexist,
   one per endpoint.
2. **The list endpoint exists.** `GET /pizzerias/{id}/orders` (auth:
   `X-API-Key`) returns `{"orders": [...]}`, newest first, each with `id`,
   `customer_id`, `created_at`, `ready_at`, `status`, `delivered_at`,
   `first_name` — but **no items**. A detail endpoint
   `GET /pizzerias/{id}/orders/{order_id}` (auth: `X-API-Key`) returns the
   full order incl. `customer` and `items[]`, so submit-timeout recovery
   shortlists by `first_name` + `created_at` recency and then verifies the
   candidate's items against the basket before adopting it. The acceptance
   test asserts items and quantities through the same detail endpoint.
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

 succeeded in 619ms:
/home/rob/bpm-pizza-vibecoding-solution:
PLAN.md
README.md
SPEC.md
SPEC_20260801_1.md
SPEC_20260801_2.md
channels
core
decisions
initial_prompt.md
logs
prompts
requirements.txt
reviews
tests
venv

/home/rob/bpm-pizza-vibecoding-solution/channels:
__init__.py
__pycache__
cli.py
static
web.py

/home/rob/bpm-pizza-vibecoding-solution/channels/__pycache__:
__init__.cpython-313.pyc
cli.cpython-313.pyc
web.cpython-313.pyc

/home/rob/bpm-pizza-vibecoding-solution/channels/static:
app.js
index.html
style.css

/home/rob/bpm-pizza-vibecoding-solution/core:
__init__.py
__pycache__
agent.py
menu.py
order.py
pizzasim.py
state.py
tools.py

/home/rob/bpm-pizza-vibecoding-solution/core/__pycache__:
__init__.cpython-313.pyc
agent.cpython-313.pyc
menu.cpython-313.pyc
order.cpython-313.pyc
pizzasim.cpython-313.pyc
state.cpython-313.pyc
tools.cpython-313.pyc

/home/rob/bpm-pizza-vibecoding-solution/decisions:
qa.md

/home/rob/bpm-pizza-vibecoding-solution/logs:
agent-00982bb3f615.jsonl
agent-13fdc31c8676.jsonl
agent-157a4a595d26.jsonl
agent-17920a8e05d6.jsonl
agent-1d17032c6d37.jsonl
agent-1f7817f7c1d7.jsonl
agent-2132714b639a.jsonl
agent-240d215627b2.jsonl
agent-25089a3f74e2.jsonl
agent-28d98ee95f01.jsonl
agent-3574cb4002c5.jsonl
agent-3e53745aef92.jsonl
agent-3f3fdcf2b6a3.jsonl
agent-42f7a034420b.jsonl
agent-543c7e7e255b.jsonl
agent-5bf831ab0607.jsonl
agent-6cc1997d2d7c.jsonl
agent-70d733a05a19.jsonl
agent-76bde6d93f57.jsonl
agent-7855ee7a96bc.jsonl
agent-78ba16436fe6.jsonl
agent-8764d5437132.jsonl
agent-8df66e30bb5b.jsonl
agent-934a882c2272.jsonl
agent-936c3cc8b83b.jsonl
agent-93b8f27713d0.jsonl
agent-a6f1f7740908.jsonl
agent-b35547c63c6b.jsonl
agent-b7ce1571592b.jsonl
agent-bccf9e552652.jsonl
agent-bd1ad952d813.jsonl
agent-bf3556391c51.jsonl
agent-e1f4c22e630a.jsonl
agent-e492c91da0d4.jsonl
agent-e62ed84c9e14.jsonl
agent-f0df5da78dbb.jsonl
agent-f14fbd6d6f4a.jsonl
agent-f8d96ea16be9.jsonl
agent-fec857eb943e.jsonl

/home/rob/bpm-pizza-vibecoding-solution/prompts:
system.de.md
system.en.md

/home/rob/bpm-pizza-vibecoding-solution/reviews:
round1-plan.md
round10-grill-verdict.md
round11-spec-v3-analysis.md
round2-plan.md
round3-plan.md
round4-impl.md
round5-impl.md
round6-impl.md
round7-hotfix.md
round8-hotfix.md
round9-audit-grill.md
scores.md

/home/rob/bpm-pizza-vibecoding-solution/tests:
__init__.py
__pycache__
fixtures
test_state.py
test_tools.py
test_transcripts.py
transcripts

/home/rob/bpm-pizza-vibecoding-solution/tests/__pycache__:
__init__.cpython-313.pyc
test_state.cpython-313-pytest-9.1.1.pyc
test_tools.cpython-313-pytest-9.1.1.pyc
test_transcripts.cpython-313-pytest-9.1.1.pyc

/home/rob/bpm-pizza-vibecoding-solution/tests/fixtures:
error_422.json
location.json
menu.json
order_created.json
orders_list.json
pizzerias.json

/home/rob/bpm-pizza-vibecoding-solution/tests/transcripts:
correction.json
happy_path.json
mind_change.json
submit_timeout.json
unknown_item.json

/home/rob/bpm-pizza-vibecoding-solution/venv:
bin
include
lib
lib64
pyvenv.cfg

/home/rob/bpm-pizza-vibecoding-solution/venv/bin:
Activate.ps1
activate
activate.csh
activate.fish
dotenv
fastapi
httpx
idna
pip
pip3
pip3.13
playwright
py.test
pygmentize
pytest
python
python3
python3.13
uvicorn
watchfiles
websockets

/home/rob/bpm-pizza-vibecoding-solution/venv/include:
python3.13
site

/home/rob/bpm-pizza-vibecoding-solution/venv/include/python3.13:

/home/rob/bpm-pizza-vibecoding-solution/venv/include/site:
python3.13

/home/rob/bpm-pizza-vibecoding-solution/venv/include/site/python3.13:
greenlet

/home/rob/bpm-pizza-vibecoding-solution/venv/include/site/python3.13/greenlet:
greenlet.h

/home/rob/bpm-pizza-vibecoding-solution/venv/lib:
python3.13

/home/rob/bpm-pizza-vibecoding-solution/venv/lib/python3.13:
site-packages

/home/rob/bpm-pizza-vibecoding-solution/venv/lib/python3.13/site-packages:
__pycache__
_pytest
_yaml
annotated_doc
annotated_doc-0.0.5.dist-info
annotated_types
annotated_types-0.8.0.dist-info
anyio
anyio-4.14.2.dist-info
certifi
certifi-2026.7.22.dist-info
click
click-8.4.2.dist-info
dotenv
fastapi
fastapi-0.141.1.dist-info
greenlet
greenlet-3.5.4.dist-info
h11
h11-0.16.0.dist-info
httpcore
httpcore-1.0.9.dist-info
httptools
httptools-0.8.0.dist-info
httpx
httpx-0.28.1.dist-info
idna
idna-3.18.dist-info
iniconfig
iniconfig-2.3.0.dist-info
multipart
packaging
packaging-26.2.dist-info
pip
pip-25.1.1.dist-info
playwright
playwright-1.62.0.dist-info
pluggy
pluggy-1.6.0.dist-info
py.py
pydantic
pydantic-2.13.4.dist-info
pydantic_core
pydantic_core-2.46.4.dist-info
pyee
pyee-13.0.1.dist-info
pygments
pygments-2.20.0.dist-info
pytest
pytest-9.1.1.dist-info
python_dotenv-1.2.2.dist-info
python_multipart
python_multipart-0.0.32.dist-info
pyyaml-6.0.3.dist-info
starlette
starlette-1.3.1.dist-info
typing_extensions-4.16.0.dist-info
typing_extensions.py
typing_inspection
typing_inspection-0.4.2.dist-info
uvicorn
uvicorn-0.52.0.dist-info
uvloop

codex
I’ve got the substance. I’m pulling exact line references now so the verdict is anchored in the spec text, not in paraphrase.
exec
/bin/bash -lc "rg -n \"Open contract questions|verified fact never moves back|GET /pizzerias/\\{id\\}/orders\\}|GET /pizzerias/\\{id\\}/orders/\\{order_id\\}|customer's UI language|Language: German or English|language the customer used|what does my basket come to|read_back|remove_item|SPEECH_URL|SPEECH_STT_MODEL|SPEECH_TTS_MODEL|SPEECH_TTS_VOICE|voice and language come from the environment|verify via "'`GET /pizzerias/'"\\{id\\}/orders"'`|The current basket is visible|Decisions locked|Decisions deferred|typed in code|APP_VERSION|test_web_e2e|speech.py|display names, prices|display names per language|Error bodies|Status values|GET /location response shape|derived from `PIZZASIM_URL`|customer chooses which one they are ordering from|can change it|Greet first" /home/rob/bpm-pizza-vibecoding-solution/SPEC.md -n -S' in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "rg -n \"PIZZERIA_LANG|prices/totals canonical|detail endpoint|items\\[\\]|orders/\\{order_id\\}|review trail|one process serves one|pricing totals|Switching pizzeria at runtime|configured pizzeria|several pizzerias|APP_VERSION|speech.py|test_web_e2e\" /home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md /home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md /home/rob/bpm-pizza-vibecoding-solution/decisions/qa.md -n -S" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 0ms:
/home/rob/bpm-pizza-vibecoding-solution/decisions/qa.md:7:Which mechanism: (a) optional env `PIZZERIA_LANG` default de, (b) required
/home/rob/bpm-pizza-vibecoding-solution/decisions/qa.md:10:**A (decision):** **(b)** — `PIZZERIA_LANG` (de|en) is a required env var.
/home/rob/bpm-pizza-vibecoding-solution/decisions/qa.md:13:before the first turn naming `PIZZERIA_LANG` and where it was expected; no
/home/rob/bpm-pizza-vibecoding-solution/decisions/qa.md:19:multi-pizzeria, APP_VERSION, full "The web channel" contract, mandatory
/home/rob/bpm-pizza-vibecoding-solution/decisions/qa.md:22:**Process:** Codex audit of the v1 claims (PASS — review trail, artifacts,
/home/rob/bpm-pizza-vibecoding-solution/decisions/qa.md:27:1. `PIZZERIA_LANG` must be documented in SPEC.md's env table — no hidden
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:83:under the configured pizzeria — with the right customer, the right items, the
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:134:  configured pizzeria, with the right customer, items and quantities.
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:164:| `APP_VERSION` | Release version, `x.y.z`, shown in the footer |
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:215:`GET /pizzerias/{id}/orders/{order_id}`, `GET /location`, plus the dashboard
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:227:   `first_name` — but **no items**. A detail endpoint
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:228:   `GET /pizzerias/{id}/orders/{order_id}` (auth: `X-API-Key`) returns the
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:229:   full order incl. `customer` and `items[]`, so submit-timeout recovery
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:232:   test asserts items and quantities through the same detail endpoint.
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:308:| `add_items` | `items[]` of `{type, code, qty, extras[]}` | new basket + revision |
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:393:- **The running version**, `x.y.z`, taken from `APP_VERSION`. It is raised on
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:633:  to `reviews/scores.md`, and `reviews/` is committed. The review trail belongs
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:83:under the configured pizzeria — with the right customer, the right items, the
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:130:  configured pizzeria, with the right customer, items and quantities.
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:137:- Payment, pricing totals, delivery routing, ETA prediction of our own.
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:140:- Switching pizzeria at runtime — one process serves one `PIZZERIA_ID`.
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:210:`GET /pizzerias/{id}/orders/{order_id}`, `GET /location`). Facts below are
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:221:   `first_name` — but **no items**. A detail endpoint
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:222:   `GET /pizzerias/{id}/orders/{order_id}` (auth: `X-API-Key`) returns the
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:223:   full order incl. `customer` and `items[]`, so submit-timeout recovery
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:226:   test asserts items and quantities through the same detail endpoint.
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:292:| `add_items` | `items[]` of `{type, code, qty, extras[]}` | new basket + revision |
/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:525:  to `reviews/scores.md`, and `reviews/` is committed. The review trail belongs

 succeeded in 216ms:
/bin/bash: line 1: PIZZASIM_URL: command not found
126:  from, and can change it. `PIZZERIA_ID` is the preselection, not a
166:| `APP_VERSION` | Release version, `x.y.z`, shown in the footer |
167:| `SPEECH_URL` | Base URL of the self-hosted speech service (optional) |
168:| `SPEECH_STT_MODEL` | Transcription model id |
169:| `SPEECH_TTS_MODEL` | Synthesis model id |
170:| `SPEECH_TTS_VOICE` | Voice id |
187:verified fact never moves back into the open list; the open list only shrinks.
226:### Open contract questions — shrink-only
231:1. **Menu item shape** beyond `code` — display names per language, price
236:3. **Error bodies** on `4xx`/`422` — a machine-readable field the tool layer
238:4. **Status values** and their order in the lifecycle.
249:                                                    │ read_back + customer says yes
263:   after `read_back` for the current basket revision. The basket carries a
279:| `get_menu` | — | pizzas and pasta with codes, display names, prices |
281:| `remove_item` | `code`, `type`, optional `qty` | new basket + revision |
283:| `read_back` | — | basket, customer, revision — the text the agent reads out |
306:- Greet first, in the customer's UI language, and offer help — one sentence,
315:- Before submitting: call `read_back`, present it, and wait for an explicit
360:- **Language: German or English**, switchable, applied to the agent's replies
366:- **The running version**, `x.y.z`, from `APP_VERSION`, raised on every
392:- The current basket is visible, with quantities and what it comes to. The
411:| STT | `POST {SPEECH_URL}/v1/audio/transcriptions` | multipart audio + model + language |
412:| TTS | `POST {SPEECH_URL}/v1/audio/speech` | JSON: model, voice, input text → audio |
426:  voice and language come from the environment, exactly like the chat model.
435:- **Speech is never required.** With `SPEECH_URL` unset or the service down,
458:| Timeout on submit | mark `UNKNOWN`, verify via `GET /pizzerias/{id}/orders` before any retry | as above |
518:  question — plus one run with `SPEECH_URL` unset, which must render a usable
655:│   ├── speech.py            ← speech service client
664:│   ├── test_web_e2e.py      ← headless browser, DOM assertions
672:## Decisions locked
701:## Decisions deferred

codex
**Findings**
1. The implementer is right about the main regression, but understates it: v3 does not just “re-open five facts”; it makes the contract internally self-contradictory. It declares shrink-only verified facts in [SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:187), then re-opens menu shape, extras, error bodies, statuses, and `/location` in the open list at [SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:226). At the same time, fixed tool semantics already depend on prices and display names at [SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:279). That is worse than v2, not merely incomplete.

2. R2 is correct, but the sharper point is this: v3 prescribes the wrong recovery mechanism. It says submit-timeout recovery verifies via the list endpoint at [SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:458), while the trusted contract says the list endpoint has no `items[]` and only the detail endpoint can verify basket contents. So recovery is not just “hard”; it is specified against the wrong endpoint. This also breaks the live acceptance test wording.

3. R3 is correct, but again too narrow. The language model is now split across four incompatible rules:
   - per-turn customer language in scope at [SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:128)
   - greeting in the customer’s UI language at [SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:306)
   - web header language switch applies to replies at [SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:360)
   - speech “voice and language come from the environment” at [SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:426)
   The implementer missed that this is not just a missing default; it is a contradictory language authority model. Also, the repo’s oracle decision requires `PIZZERIA_LANG` in the env table, and v3 omits it entirely: [decisions/qa.md](/home/rob/bpm-pizza-vibecoding-solution/decisions/qa.md:10), [decisions/qa.md](/home/rob/bpm-pizza-vibecoding-solution/decisions/qa.md:27).

4. R4 is correct and still understated. The total is unspecified in both tool and UI contracts: `read_back` returns only basket/customer/revision at [SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:283), yet the customer may ask “what does my basket come to?” at [SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:311) and the web basket must show “what it comes to” at [SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:392). Without a code-owned total, the spec invites LLM arithmetic, which conflicts with “no invented figures.”

5. The implementer missed an environment-table defect beyond `PIZZERIA_LANG`: v3 says speech base URL, models, voice, and language come from env, but only four vars are defined and none carries speech language ([SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:167), [SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:426)). So the env table is incomplete even on its own terms.

6. The implementer also missed an error-table regression: “404 on the pizzeria path -> fail at startup” at [SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:456) is a single-tenant leftover. In v3, the customer can change pizzeria at runtime ([SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:126)). Startup cannot validate every later selection. That row no longer matches the tenancy model.

7. A2 and A3 are valid. CLI tenancy is underspecified because scope grants customer-selectable pizzeria product-wide, but only the web header defines how that choice happens. `remove_item` is also still underspecified when multiple lines share `(type, code)` but differ by `extras[]`; the trusted contract that codes are unique only per type makes this a real ambiguity, not a corner case.

8. I1-I5 mostly stand, but with corrections. I1 is only a paper improvement because v3 violates it immediately. I2, I4, and I5 are real improvements. I3 is only partial: speech optionality is clearer, but the language/config contract is now inconsistent, and the deliverables expanded beyond the current approved repo shape (`channels/speech.py`, `tests/test_web_e2e.py`) without fully specifying the missing behavior.

**Answers**
(a) v3 is not the optimal spec as written. Patched, it is the best baseline of the three; unpatched, v2 is safer.

(b) Missing:
- Restoration of the verified contract facts and the order-detail endpoint fact.
- A single language authority rule, including initial/default behavior and CLI behavior.
- Explicit code ownership of basket totals and where totals appear in tool results/UI.
- Precise `remove_item` semantics for duplicate `(type, code)` lines with different extras.
- A multi-tenant-correct error rule for pizzeria-path failures.
- A complete env table, including `PIZZERIA_LANG` and resolving speech-language config.

(c) Worse vs v1/v2:
- v3 regresses contract certainty by reopening already verified facts from v1/v2.
- v3 deletes the detail-endpoint fact and thereby breaks timeout recovery and live verification.
- v3 makes language behavior less coherent than v2.
- v3 keeps the new totals/pricing requirement but drops the mechanism that keeps totals code-owned.
- v3 carries a single-tenant startup error rule into a multi-tenant product.

VERDICT ON SPEC v3: NEEDS PATCHES

PATCH LIST:
1. Restore the verified live-API facts from v2 into the contract facts section: menu `{code,name,base[],price}`, `toppings[]`/`extras[]`, error body `{"error","details[]"}`, status order, `/location` shape, and the detail endpoint.
2. Replace submit-timeout recovery text so verification uses `GET /pizzerias/{id}/orders/{order_id}` after shortlist-from-list, and state that live acceptance asserts items via the detail endpoint.
3. Add `PIZZERIA_LANG` to the env table and define one language precedence rule covering greeting, per-turn replies, header switch, CLI, and STT/TTS hints.
4. Either add an explicit speech-language env var or remove the claim that speech language comes from environment and bind it to the chosen reply language instead.
5. Define basket totals as code-computed from API-supplied menu prices cached in the session/order state; never computed by the LLM.
6. Extend `read_back` success payload to include the canonical total, and state that the web basket view uses that same code-owned total.
7. Define `remove_item` semantics for multiple lines with the same `(type, code)` but different `extras[]`, or add a line identifier to the tool contract.
8. Rewrite the `404` pizzeria-path error rule so it matches runtime tenant switching instead of assuming single-tenant startup validation.
tokens used
70,075
**Findings**
1. The implementer is right about the main regression, but understates it: v3 does not just “re-open five facts”; it makes the contract internally self-contradictory. It declares shrink-only verified facts in [SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:187), then re-opens menu shape, extras, error bodies, statuses, and `/location` in the open list at [SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:226). At the same time, fixed tool semantics already depend on prices and display names at [SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:279). That is worse than v2, not merely incomplete.

2. R2 is correct, but the sharper point is this: v3 prescribes the wrong recovery mechanism. It says submit-timeout recovery verifies via the list endpoint at [SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:458), while the trusted contract says the list endpoint has no `items[]` and only the detail endpoint can verify basket contents. So recovery is not just “hard”; it is specified against the wrong endpoint. This also breaks the live acceptance test wording.

3. R3 is correct, but again too narrow. The language model is now split across four incompatible rules:
   - per-turn customer language in scope at [SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:128)
   - greeting in the customer’s UI language at [SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:306)
   - web header language switch applies to replies at [SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:360)
   - speech “voice and language come from the environment” at [SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:426)
   The implementer missed that this is not just a missing default; it is a contradictory language authority model. Also, the repo’s oracle decision requires `PIZZERIA_LANG` in the env table, and v3 omits it entirely: [decisions/qa.md](/home/rob/bpm-pizza-vibecoding-solution/decisions/qa.md:10), [decisions/qa.md](/home/rob/bpm-pizza-vibecoding-solution/decisions/qa.md:27).

4. R4 is correct and still understated. The total is unspecified in both tool and UI contracts: `read_back` returns only basket/customer/revision at [SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:283), yet the customer may ask “what does my basket come to?” at [SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:311) and the web basket must show “what it comes to” at [SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:392). Without a code-owned total, the spec invites LLM arithmetic, which conflicts with “no invented figures.”

5. The implementer missed an environment-table defect beyond `PIZZERIA_LANG`: v3 says speech base URL, models, voice, and language come from env, but only four vars are defined and none carries speech language ([SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:167), [SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:426)). So the env table is incomplete even on its own terms.

6. The implementer also missed an error-table regression: “404 on the pizzeria path -> fail at startup” at [SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:456) is a single-tenant leftover. In v3, the customer can change pizzeria at runtime ([SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:126)). Startup cannot validate every later selection. That row no longer matches the tenancy model.

7. A2 and A3 are valid. CLI tenancy is underspecified because scope grants customer-selectable pizzeria product-wide, but only the web header defines how that choice happens. `remove_item` is also still underspecified when multiple lines share `(type, code)` but differ by `extras[]`; the trusted contract that codes are unique only per type makes this a real ambiguity, not a corner case.

8. I1-I5 mostly stand, but with corrections. I1 is only a paper improvement because v3 violates it immediately. I2, I4, and I5 are real improvements. I3 is only partial: speech optionality is clearer, but the language/config contract is now inconsistent, and the deliverables expanded beyond the current approved repo shape (`channels/speech.py`, `tests/test_web_e2e.py`) without fully specifying the missing behavior.

**Answers**
(a) v3 is not the optimal spec as written. Patched, it is the best baseline of the three; unpatched, v2 is safer.

(b) Missing:
- Restoration of the verified contract facts and the order-detail endpoint fact.
- A single language authority rule, including initial/default behavior and CLI behavior.
- Explicit code ownership of basket totals and where totals appear in tool results/UI.
- Precise `remove_item` semantics for duplicate `(type, code)` lines with different extras.
- A multi-tenant-correct error rule for pizzeria-path failures.
- A complete env table, including `PIZZERIA_LANG` and resolving speech-language config.

(c) Worse vs v1/v2:
- v3 regresses contract certainty by reopening already verified facts from v1/v2.
- v3 deletes the detail-endpoint fact and thereby breaks timeout recovery and live verification.
- v3 makes language behavior less coherent than v2.
- v3 keeps the new totals/pricing requirement but drops the mechanism that keeps totals code-owned.
- v3 carries a single-tenant startup error rule into a multi-tenant product.

VERDICT ON SPEC v3: NEEDS PATCHES

PATCH LIST:
1. Restore the verified live-API facts from v2 into the contract facts section: menu `{code,name,base[],price}`, `toppings[]`/`extras[]`, error body `{"error","details[]"}`, status order, `/location` shape, and the detail endpoint.
2. Replace submit-timeout recovery text so verification uses `GET /pizzerias/{id}/orders/{order_id}` after shortlist-from-list, and state that live acceptance asserts items via the detail endpoint.
3. Add `PIZZERIA_LANG` to the env table and define one language precedence rule covering greeting, per-turn replies, header switch, CLI, and STT/TTS hints.
4. Either add an explicit speech-language env var or remove the claim that speech language comes from environment and bind it to the chosen reply language instead.
5. Define basket totals as code-computed from API-supplied menu prices cached in the session/order state; never computed by the LLM.
6. Extend `read_back` success payload to include the canonical total, and state that the web basket view uses that same code-owned total.
7. Define `remove_item` semantics for multiple lines with the same `(type, code)` but different `extras[]`, or add a line identifier to the tool contract.
8. Rewrite the `404` pizzeria-path error rule so it matches runtime tenant switching instead of assuming single-tenant startup validation.
