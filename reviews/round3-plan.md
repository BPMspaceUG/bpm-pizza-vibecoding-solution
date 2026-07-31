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

 succeeded in 753ms:
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

 succeeded in 501ms:
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

 succeeded in 618ms:
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

 succeeded in 680ms:
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
| `remove_item` | `{type: enum, code: str, qty: int ≥1 optional}` (absent qty = remove all of that line) | `{"snapshot": SNAPSHOT}` |
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

codex
I’ve got the core documents loaded. One more skill reference applies for this harness, then I’ll finish the spec-to-plan cross-check and produce the ruling with concrete issues only if they are plan-level gaps.
exec
/bin/bash -lc "sed -n '1,220p' /home/rob/.agents/skills/using-superpowers/references/codex-tools.md" in /home/rob/bpm-pizza-vibecoding-solution
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

codex
I’m checking the remaining spec sections against the rest of `PLAN.md` now, especially the web protocol, speech flow, testing, and deliverables, because those are where plan-sized omissions usually hide.
exec
/bin/bash -lc "sed -n '261,520p' SPEC.md" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 0ms:
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
- **No browser speech APIs.** `SpeechRecognition` and `speechSynthesis` are not
  used. The previous implementation relied on them, which tied the product to
  one browser vendor and sent customer audio to a third party. The service
  replaces them.
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
- **One live smoke test**, opt-in via env flag: places a real order and asserts
  an `order_id` came back. This is the only test that touches the real API.
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
4. **Web.** FastAPI on 8888, same core, streamed intermediate steps visible.
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

exec
/bin/bash -lc "sed -n '261,520p' PLAN.md" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 154ms:
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
2. **Order + state machine + tests.** `core/order.py`, `core/state.py`,
   `tests/test_state.py`.
   ☐ all five invariants tested ☐ every ✗ cell tested ☐ demotion +
   revision staleness tested ☐ pytest green.
3. **Menu.** `core/menu.py`, `fixtures/menu.json` (recorded), validation +
   candidates. ☐ (type, code) validation ☐ `tonno` collision test ☐
   extras vocabulary ☐ ≤3 candidates.
4. **PizzaSim client.** `core/pizzasim.py`, typed errors, timeouts,
   fixtures for orders/422/location, httpx MockTransport tests.
   ☐ every error class mapped ☐ no call without timeout ☐ submit returns
   typed result ☐ list_orders parsed.
5. **Tools.** `core/tools.py` schemas + dispatch, `tests/test_tools.py`.
   ☐ schemas match this plan exactly ☐ atomic add ☐ error shape uniform
   ☐ snapshot on every success.
6. **Agent loop + prompts + transcripts.** `core/agent.py`, both prompts,
   stub model, five transcripts.
   ☐ tool loop with guard ☐ gateway retry-once ☐ JSONL logging ☐ five
   transcripts green.
7. **CLI.** `channels/cli.py`. ☐ full conversation against real API
   possible ☐ --verbose shows tool events ☐ startup checks enforced.
8. **Web text channel.** `channels/web.py` + `static/` (no speech yet).
   ☐ port 8888 ☐ NDJSON steps visible in UI ☐ per-session orders ☐
   startup checks enforced.
9. **Speech.** Proxy endpoints + mic/TTS UI.
   ☐ push-to-talk with visible state ☐ TTS off by default, final message
   only ☐ `SPEECH_URL` unset → no mic, no speaker, text works ☐ speech
   failure never touches the order.
10. **Harden + docs.** Walk the SPEC error table end to end, README
    complete, `.env.example` final, live smoke test.
    ☐ each error row demonstrably handled ☐ README covers all channels +
    speech + tests ☐ full suite green.

Each ticket ≤ 1h, tests live in the ticket that introduces the behaviour.

codex
The cross-check is down to edge cases now: tool contracts, submit-timeout recovery, language handling, and session/menu ownership. I’m pulling line-numbered excerpts so the verdict is tied to the actual plan text rather than general impressions.
exec
/bin/bash -lc "nl -ba SPEC.md | sed -n '100,360p'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "nl -ba PLAN.md | sed -n '1,260p'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "nl -ba decisions/qa.md | sed -n '1,120p'" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 284ms:
   100	- Payment, pricing totals, delivery routing, ETA prediction of our own.
   101	- Accounts, auth, sessions surviving a process restart.
   102	- Modifying or cancelling an order after it was submitted.
   103	- Switching pizzeria at runtime — one process serves one `PIZZERIA_ID`.
   104	- Any regex or keyword parser that produces an order without the model.
   105	  See **Anti-patterns**; this is not a style preference, it is a hard ban.
   106	- Reading the whole menu aloud when the answer will be spoken.
   107	- Persisting customer data anywhere beyond the process and the PizzaSim API.
   108	
   109	---
   110	
   111	## Environment and configuration
   112	
   113	All configuration comes from environment variables. Load `~/.env` if present;
   114	never write to it, never create it, never print a value.
   115	
   116	| Variable | Purpose |
   117	|---|---|
   118	| `LITELLM_PIZZA_URL` | OpenAI-compatible gateway base URL (`/chat/completions` appended) |
   119	| `LITELLM_PIZZA_KEY` | Bearer token for the gateway |
   120	| `PIZZASIM_URL` | PizzaSim API base URL |
   121	| `PIZZASIM_API_KEY` | Sent as header `X-API-Key` on protected routes |
   122	| `PIZZERIA_ID` | UUID of the pizzeria this process serves |
   123	| `LITELLM_PIZZA_MODEL_1` | Model the ordering agent calls; required, no default in code |
   124	| `LITELLM_PIZZA_MODEL_2` | Second configured model, where the build uses one |
   125	
   126	Rules:
   127	
   128	- **Nothing is hardcoded.** No UUID, no model name, no menu, no base URL —
   129	  not even as a fallback "just in case".
   130	- Missing or empty variable → exit before the first turn with a message naming
   131	  the variable and the file it was expected in. Never start half-configured.
   132	- Secrets never appear in logs, transcripts, error messages or the web UI.
   133	
   134	---
   135	
   136	## The PizzaSim API (contract)
   137	
   138	| Call | Auth | Notes |
   139	|---|---|---|
   140	| `GET /menu` | public | returns `pizzas[]` and `pasta[]`, each with `code` |
   141	| `GET /pizzerias` | `X-API-Key` | list of pizzerias with `id`, `name` |
   142	| `POST /pizzerias/{PIZZERIA_ID}/orders` | `X-API-Key` | places the order |
   143	| `GET /location?street=…` | public | street plausibility check |
   144	
   145	Order request body:
   146	
   147	```json
   148	{
   149	  "customer": { "first_name": "Marco", "street_one": "via di Cantieri" },
   150	  "items": [{ "type": "pizza", "code": "margherita", "qty": 2, "extras": [] }]
   151	}
   152	```
   153	
   154	Response carries `order_id`, `status`, `eta_seconds`.
   155	
   156	Facts that shape behaviour:
   157	
   158	- The tenant is **always** in the URL path, never in a header.
   159	- Customers are unique per pizzeria **by first name**. An unknown name silently
   160	  creates a new customer — so a misheard name creates a ghost. Speech input must
   161	  therefore confirm the name explicitly.
   162	- `street_one` is optional and is **not** validated for deliverability. Asking
   163	  for it is a policy of this agent, not an API requirement — do not pretend to
   164	  the customer that we checked something we did not.
   165	- `POST` is **not idempotent**. A retry after a timeout can double the order.
   166	  See **Error handling**.
   167	
   168	### Contract facts — verified against the live API (2026-07-31)
   169	
   170	All seven former open questions were resolved by probing the live API
   171	(`GET /menu`, `GET /pizzerias`, `POST /pizzerias/{id}/orders` — valid and
   172	invalid bodies —, `GET /pizzerias/{id}/orders`, `GET /location`). Facts below
   173	are from real responses, not documentation.
   174	
   175	1. **Order response field name: `order_id`.** A successful
   176	   `POST /pizzerias/{id}/orders` returns
   177	   `{"order_id": "<uuid>", "status": "ordered", "eta_seconds": <int>}`.
   178	   The **list** endpoint uses `id` for the same value — the two names coexist,
   179	   one per endpoint.
   180	2. **The list endpoint exists.** `GET /pizzerias/{id}/orders` (auth:
   181	   `X-API-Key`) returns `{"orders": [...]}`, newest first, each with `id`,
   182	   `customer_id`, `created_at`, `ready_at`, `status`, `delivered_at`,
   183	   `first_name`. It does **not** include items, so submit-timeout recovery
   184	   matches on `first_name` + `created_at` recency.
   185	3. **Menu item shape:** `{"code", "name", "base": [ingredients], "price"}`.
   186	   `name` is a single string (Italian proper names, identical in DE and EN) —
   187	   there are no per-language names in the API; read-back uses `name` as-is in
   188	   both languages. The menu response also carries a top-level `toppings[]`
   189	   array of ingredient codes.
   190	4. **`extras[]` is a controlled vocabulary:** the top-level `toppings[]` from
   191	   `GET /menu` (e.g. `mozzarella`, `mushrooms`, `pineapple`). The server
   192	   rejects unknown extras with `422` (`"items[0].extras contains invalid
   193	   topping 'unicorn_dust'"`), so the tool layer validates extras against
   194	   `toppings[]` exactly like item codes.
   195	5. **Error bodies are machine-readable:**
   196	   `{"error": "<code>", "details": ["<human sentence>", ...]}` — e.g.
   197	   `{"error": "validation_failed", "details": ["items[0].code must be a valid
   198	   pizza code"]}` with HTTP 422. The tool layer maps `error` to typed errors
   199	   and may surface `details` to targeted questions.
   200	6. **Status values observed in the lifecycle:** `ordered` →
   201	   `prepared_planned` → `delivered` (with `delivered_at` set on the last).
   202	   A fresh order starts as `ordered`.
   203	7. **`GET /location?street=` returns** `{"street": "<echo>",
   204	   "deliverable": <bool>}` with HTTP 200. In probing, even a nonsense street
   205	   returned `deliverable: true` — the check is a weak plausibility signal at
   206	   best, which confirms the policy above: never tell the customer an address
   207	   was verified.
   208	
   209	Additional verified fact: item `code`s are unique **per type**, not globally —
   210	`tonno` exists as both a pizza and a pasta. Validation and removal must always
   211	key on `(type, code)`.
   212	
   213	---
   214	
   215	## Order state machine
   216	
   217	```
   218	EMPTY ──add_items──▶ COLLECTING ──set_customer──▶ READY
   219	  ▲                      │  ▲                       │
   220	  └──remove last item────┘  └───add/remove/edit─────┘
   221	                                                    │ read_back + customer says yes
   222	                                                    ▼
   223	                                               CONFIRMED ──submit_order──▶ SUBMITTED
   224	                                                    │                          
   225	                                                    └──any change──▶ back to READY
   226	```
   227	
   228	Invariants, all enforced in code and all covered by unit tests:
   229	
   230	1. `submit_order` outside `CONFIRMED` returns an error. It does not "helpfully"
   231	   confirm on the model's behalf.
   232	2. Any mutation after `CONFIRMED` drops the order back to `READY`. A confirmation
   233	   applies to the basket that was read back, not to a later one.
   234	3. `CONFIRMED` is reachable only via `confirm_order`, and `confirm_order` is only
   235	   legal after `read_back` has been called for the current basket revision. The
   236	   basket carries a revision counter; `confirm_order` must name it.
   237	4. `SUBMITTED` is terminal. The conversation may continue; the order may not.
   238	5. An item may only enter the basket with a `code` present in the menu snapshot
   239	   fetched this session.
   240	
   241	---
   242	
   243	## Tools
   244	
   245	The model sees exactly these. Names, parameters and semantics are fixed.
   246	
   247	| Tool | Parameters | Returns |
   248	|---|---|---|
   249	| `get_menu` | — | pizzas and pasta with codes and display names in both languages |
   250	| `add_items` | `items[]` of `{type, code, qty, extras[]}` | new basket + revision |
   251	| `remove_item` | `code`, `type`, optional `qty` | new basket + revision |
   252	| `set_customer` | `first_name`, optional `street_one` | customer as stored |
   253	| `read_back` | — | basket, customer, revision — the text the agent must read out |
   254	| `confirm_order` | `revision` | state `CONFIRMED`, or error if stale |
   255	| `submit_order` | — | `order_id`, `status`, `eta_seconds` |
   256	| `check_street` | `street` | plausibility result (optional) |
   257	
   258	Tool result conventions:
   259	
   260	- Success: the **full current state**, not a diff. The model should never have to
   261	  reconstruct the basket from history.
   262	- Failure: `{"error": {"code": "...", "message": "...", "candidates": [...]}}`.
   263	  `message` is written to be spoken to the customer as-is if the model chooses to.
   264	- `add_items` with an unknown code returns `unknown_item` plus up to three
   265	  candidates from the menu. The model asks; it does not pick.
   266	- Quantities are integers. A tool that receives `"zwei"` returns
   267	  `invalid_quantity`; it does not parse German.
   268	
   269	---
   270	
   271	## Conversation policy
   272	
   273	This is what the system prompt must produce. Write the prompt to achieve it;
   274	do not paste this section into the prompt verbatim.
   275	
   276	- Greet first, in the language of the pizzeria's country, and offer help — one
   277	  sentence, not a menu recital.
   278	- **One question per turn.** Never stack "name, street and what would you like?"
   279	- Never state a menu item that did not come from `get_menu` in this session.
   280	- Collect first name and street. If the customer declines the street, accept it
   281	  and move on — it is optional in the API.
   282	- Before submitting: call `read_back`, say it, and wait for an explicit yes.
   283	  "Mhm" and silence are not a yes; ask again once, then offer to start over.
   284	- Never announce that an order was placed before `submit_order` returned an
   285	  `order_id`. No "I've sent that to the kitchen" while the call is in flight.
   286	- On confirmation, state the order id in a form a human can repeat back, and the
   287	  wait time in **minutes**, converted from `eta_seconds`.
   288	- On error, explain in plain language what happened and what the customer's
   289	  options are. Never show a status code, stack trace or JSON.
   290	- Never claim to have checked an address for deliverability.
   291	
   292	---
   293	
   294	## Speech
   295	
   296	Speech is an input and an output method on the web channel. It is served by a
   297	**self-hosted speech service**, CPU-only, in its own container, reached over
   298	plain HTTP with an OpenAI-compatible surface:
   299	
   300	| Direction | Endpoint | Payload |
   301	|---|---|---|
   302	| STT | `POST {SPEECH_URL}/v1/audio/transcriptions` | multipart audio file + model + language |
   303	| TTS | `POST {SPEECH_URL}/v1/audio/speech` | JSON with model, voice, input text; returns audio |
   304	
   305	- **The speech service is the only speech path.** No external speech provider,
   306	  no hosted realtime framework, no audio through the LLM gateway — that gateway
   307	  carries chat completions only.
   308	- **No browser speech APIs.** `SpeechRecognition` and `speechSynthesis` are not
   309	  used. The previous implementation relied on them, which tied the product to
   310	  one browser vendor and sent customer audio to a third party. The service
   311	  replaces them.
   312	- **Nothing about the speech stack is written into source.** Base URL, STT
   313	  model, TTS model, voice and language all come from the environment, exactly
   314	  like the chat model:
   315	
   316	  | Variable | Purpose |
   317	  |---|---|
   318	  | `SPEECH_URL` | base URL of the self-hosted speech service |
   319	  | `SPEECH_STT_MODEL` | transcription model id |
   320	  | `SPEECH_TTS_MODEL` | synthesis model id |
   321	  | `SPEECH_TTS_VOICE` | voice id |
   322	
   323	- **Request/response, not streaming.** The customer records, the recording is
   324	  uploaded, the transcript comes back. Latency is visible and acceptable; do not
   325	  build partial-result handling, barge-in or turn detection on top of it — this
   326	  transport cannot do them, and pretending otherwise produces a broken feel.
   327	- **The microphone is push-to-talk.** It starts and stops on the customer's
   328	  action, never listens continuously. Recording state is visible in the UI at
   329	  all times.
   330	- **Synthesis is optional and off by default**, toggled by the customer, applied
   331	  only to the final assistant message and never to intermediate steps.
   332	- **Speech is never required.** If `SPEECH_URL` is unset or the service does not
   333	  answer, the microphone and the speaker toggle are not rendered and the web
   334	  channel stays fully usable as text. A speech failure is never an order failure.
   335	- **Speech shortens answers, it does not change them.** Same core, same tools,
   336	  same state machine. When a reply will be spoken: at most three menu items and
   337	  an invitation, times in minutes rather than seconds, order id read in groups.
   338	- **Confirm the name.** Transcription errors on names are the expensive failure:
   339	  customers are unique per pizzeria by first name, so a misheard name silently
   340	  creates a customer nobody will find again. Read the name back before
   341	  submitting.
   342	
   343	---
   344	
   345	## Error handling
   346	
   347	Every case below needs a test and a phrasing.
   348	
   349	| Situation | Code does | Customer hears |
   350	|---|---|---|
   351	| Gateway timeout | one retry, then abort turn | "I didn't catch that, one moment" then a plain apology |
   352	| `401` / `403` from PizzaSim | abort, log, do not retry | "I can't reach the kitchen system right now" |
   353	| `404` on the pizzeria path | fail at startup, not mid-call | — (process refuses to start) |
   354	| `422` validation | surface field, keep basket | targeted question about the offending item |
   355	| `5xx` on submit | **do not blind-retry** | "I'm not sure that went through — let me check" |
   356	| Timeout on submit | mark `UNKNOWN`, verify before any retry | as above |
   357	| Unknown item code | `unknown_item` + candidates | "I have Margherita or Marinara — which one?" |
   358	| Empty basket at submit | reject transition | "What can I get you?" |
   359	| Menu fetch fails at start | fail fast | "We're not taking orders right now" |
   360	

 succeeded in 292ms:
     1	# Oracle Q&A (Codex, read-only)
     2	
     3	## 2026-07-31 — Greeting language source
     4	
     5	**Q:** SPEC requires greeting in the pizzeria-country language; the live API
     6	exposes no country field; DE/EN only; nothing hardcoded, config from env.
     7	Which mechanism: (a) optional env `PIZZERIA_LANG` default de, (b) required
     8	env var failing at startup, (c) constant in source, (d) other?
     9	
    10	**A (decision):** **(b)** — `PIZZERIA_LANG` (de|en) is a required env var.
    11	A default would smuggle in a hardcoded fallback, conflicting with "nothing
    12	is hardcoded" and the missing-var-fails-startup rule. If missing/empty, exit
    13	before the first turn naming `PIZZERIA_LANG` and where it was expected; no
    14	default applied.

 succeeded in 308ms:
     1	# PizzaSim Ordering Agent — Implementation Plan
     2	
     3	> Written before any code, per SPEC.md stage 1. Updated as implementation
     4	> proceeds. Contains design and tickets only — no code.
     5	
     6	**Goal:** A two-channel (CLI + web) pizza-ordering agent where the order is a
     7	state machine owned by the code and the model only converts speech/text into
     8	tool calls.
     9	
    10	**Architecture:** One Python core (`core/`) holds the order state machine, menu
    11	validation, PizzaSim client, tool dispatch and the model loop. Channels
    12	(`channels/cli.py`, `channels/web.py`) are transports only: words in, words
    13	out, zero order logic. Speech is an optional proxy on the web channel to a
    14	self-hosted OpenAI-compatible speech service.
    15	
    16	**Tech stack:** Python 3.13, `httpx` (all HTTP, with timeouts), `fastapi` +
    17	`uvicorn` (web channel), `pytest` (tests), stdlib `difflib` (candidate
    18	matching), stdlib `json`/`dataclasses`/`enum`. No other dependencies.
    19	
    20	## Global constraints (from SPEC.md, binding for every ticket)
    21	
    22	- Nothing hardcoded: no UUID, no model name, no menu, no base URL, no
    23	  fallbacks. All config from environment; `~/.env` loaded if present, never
    24	  written, never printed.
    25	- Missing/empty required env var → exit before the first turn, naming the
    26	  variable and the file it was expected in.
    27	- Secrets never appear in logs, transcripts, errors, or the web UI.
    28	- No regex/keyword parser that produces an order without the model (hard ban).
    29	- No `subprocess` + `curl` — `httpx` only, explicit timeouts everywhere.
    30	- No browser speech APIs (`SpeechRecognition`, `speechSynthesis`).
    31	- No build-time model name anywhere in source, config, prompts, tests, docs.
    32	- `submit_order` is the only network write; legal only in `CONFIRMED`.
    33	- Item codes are unique per type, not globally (`tonno` is a pizza and a
    34	  pasta) — every validation and removal keys on `(type, code)`.
    35	- Deterministic tests: no network, no LLM (one opt-in live smoke test).
    36	- German + English, mirrored per turn.
    37	
    38	## File layout
    39	
    40	```
    41	core/
    42	  order.py     Order dataclass: items, customer, revision, state field,
    43	               read-back tracking, submit bookkeeping. Pure data + snapshots.
    44	  state.py     OrderState enum + transition functions. Every mutation goes
    45	               through here; illegal transitions raise TransitionError.
    46	  menu.py      Immutable Menu snapshot (pizzas, pasta, toppings), one per
    47	               session; (type, code) validation; extras validation;
    48	               candidate suggestions via difflib over codes and names.
    49	  pizzasim.py  httpx client for PizzaSim: get_menu, list_orders,
    50	               submit_order, check_street; typed errors; timeouts;
    51	               startup pizzeria check.
    52	  tools.py     The eight tool JSON schemas + dispatch(tool_name, args) →
    53	               result dict. Success = full state snapshot; failure =
    54	               {"error": {code, message, candidates}}.
    55	  agent.py     Config loading for gateway vars, prompt assembly, the model
    56	               loop (chat completions + tool calls until a plain assistant
    57	               message), gateway retry policy, JSONL event logging.
    58	channels/
    59	  cli.py       Terminal REPL over the core. Prints assistant text; --verbose
    60	               shows tool events.
    61	  web.py       FastAPI on port 8888. Serves static/, POST /chat streaming
    62	               NDJSON events, speech proxy endpoints, /config for UI
    63	               feature flags. In-memory session dict.
    64	  static/      index.html, app.js, style.css — chat UI, NDJSON consumer,
    65	               push-to-talk recorder (MediaRecorder → upload), TTS toggle.
    66	prompts/
    67	  system.de.md German system prompt (default deployment language).
    68	  system.en.md English system prompt, same policy.
    69	tests/
    70	  fixtures/    Recorded real API responses (menu, order created, orders
    71	               list, 422 bodies, location).
    72	  test_state.py       State machine, exhaustive incl. every illegal move.
    73	  test_tools.py       Tool dispatch against fixture-backed fakes.
    74	  test_transcripts.py Runner for the five golden transcripts.
    75	  transcripts/        Five scripted conversations as JSON.
    76	reviews/       One file per review round + scores.md.
    77	.env.example   Names only.
    78	README.md      How to run CLI, web, speech; how to test.
    79	requirements.txt  Pinned: fastapi, uvicorn, httpx, pytest, python-multipart.
    80	```
    81	
    82	Deviation from the SPEC tree, documented: `tests/test_transcripts.py` and
    83	`requirements.txt` are added (the transcripts need a runner; the deps need
    84	pinning). Everything listed in SPEC.md exists exactly where listed.
    85	
    86	## Configuration
    87	
    88	Each module owns its own env vars and exposes `from_env()`:
    89	
    90	| Module | Vars |
    91	|---|---|
    92	| `core/agent.py` | `LITELLM_PIZZA_URL`, `LITELLM_PIZZA_KEY`, `LITELLM_PIZZA_MODEL_1`, `PIZZERIA_LANG` (all required; `LITELLM_PIZZA_MODEL_2` read but unused — single-model build) |
    93	| `core/pizzasim.py` | `PIZZASIM_URL`, `PIZZASIM_API_KEY`, `PIZZERIA_ID` (required) |
    94	| `channels/web.py` | `SPEECH_URL`, `SPEECH_STT_MODEL`, `SPEECH_TTS_MODEL`, `SPEECH_TTS_VOICE` (all optional; absence disables speech) |
    95	
    96	`PIZZERIA_LANG` ∈ {`de`, `en`} is the pizzeria-country greeting language.
    97	The live API exposes no country field (verified), so per the config-from-env
    98	rule this deployment fact is a **required** env var — no default, missing →
    99	startup failure like any other required var (oracle decision,
   100	`decisions/qa.md`). It selects the system prompt file and the STT language
   101	hint; it never overrides per-turn language mirroring.
   102	
   103	Loading order: process env wins; else `~/.env` if present (parsed key=value,
   104	never written, never printed). No other sources. A missing required var
   105	raises `ConfigError("LITELLM_PIZZA_URL is not set (expected in the
   106	environment or ~/.env)")` and the channel exits before the first turn.
   107	Logs go to `./logs/` (fixed path, gitignored) — not configurable.
   108	
   109	Startup sequence, identical for both channels, all before the first turn:
   110	
   111	1. Load and validate all required env vars (exit naming var + file).
   112	2. `GET /pizzerias` with `X-API-Key` — a 401/403 aborts startup ("cannot
   113	   reach the kitchen system"); `PIZZERIA_ID` not in the returned list is the
   114	   404-pizzeria case from the error table → process refuses to start;
   115	   otherwise capture `pizzeria_name` for the system prompt.
   116	3. `GET /menu` — failure aborts startup with "We're not taking orders right
   117	   now".
   118	
   119	**Session model.** A session (conversation) = one `Order` + one immutable
   120	`Menu` snapshot + one message history, bundled in a `Session` object owned
   121	by the channel. The CLI process is exactly one session and reuses the
   122	startup menu fetch as its snapshot. The web channel creates a `Session` per
   123	`session_id`, fetching a **fresh menu snapshot at session creation**; that
   124	snapshot is immutable for the session's lifetime (spec invariant 5: "menu
   125	snapshot fetched this session"). A failed session-creation fetch yields the
   126	"We're not taking orders right now" message for that session only.
   127	
   128	## Order state machine
   129	
   130	States: `EMPTY`, `COLLECTING`, `READY`, `CONFIRMED`, `SUBMITTED`.
   131	
   132	Order fields: `items: list[Item(type, code, qty, extras)]`,
   133	`customer: Customer(first_name, street_one) | None`, `revision: int`
   134	(increments on every basket or customer mutation), `read_back_revision:
   135	int | None` (set by `read_back`), `state`, `submit_attempted_at: int | None`
   136	(unix seconds captured immediately **before** the first submit POST — the
   137	correlation key for timeout recovery), `submit_unknown: bool` (that attempt
   138	timed out / 5xx'd and is unverified), `result` (order_id, status,
   139	eta_seconds after submit).
   140	
   141	Derived-state rule after any legal mutation: `SUBMITTED` is terminal and
   142	`CONFIRMED` is only ever entered by `confirm_order`; otherwise state is
   143	recomputed as `EMPTY` (no items), `COLLECTING` (items, no customer), `READY`
   144	(items + customer). A mutation while `CONFIRMED` succeeds and demotes to the
   145	recomputed state (invariant 2). `set_customer` before any item is legal
   146	(customer stored, state stays `EMPTY`) — the diagram's path is the common
   147	case, not an ordering constraint.
   148	
   149	Transition table (✓ legal, ✗ → typed error):
   150	
   151	| Tool | EMPTY | COLLECTING | READY | CONFIRMED | SUBMITTED |
   152	|---|---|---|---|---|---|
   153	| add_items | ✓ | ✓ | ✓ | ✓ demote | ✗ order_closed |
   154	| remove_item | ✗ empty_basket | ✓ | ✓ | ✓ demote | ✗ order_closed |
   155	| set_customer | ✓ | ✓ | ✓ | ✓ demote | ✗ order_closed |
   156	| read_back | ✗ empty_basket | ✗ invalid_state (no customer yet) | ✓ | ✓ (same basket, idempotent) | ✗ order_closed |
   157	| confirm_order | ✗ invalid_state | ✗ invalid_state | ✓ | ✗ invalid_state (already confirmed) | ✗ order_closed |
   158	| submit_order | ✗ invalid_state | ✗ invalid_state | ✗ invalid_state | ✓ | ✗ order_closed |
   159	| get_menu / check_street | ✓ any state, read-only | | | | |
   160	
   161	`confirm_order(revision)` additionally requires `revision == order.revision`
   162	(else `stale_revision`) and `read_back_revision == order.revision` (else
   163	`read_back_required`). So the only path into `CONFIRMED` is: state `READY`,
   164	`read_back` called at the current revision, then `confirm_order` naming that
   165	same revision — exactly the spec's path, nothing broader. Every ✗ cell gets
   166	a unit test (invariants 1–5).
   167	
   168	Submit-timeout path: `submit_order` sets `submit_attempted_at = now()`
   169	before its first POST. On httpx timeout or 5xx, the order stays `CONFIRMED`
   170	with `submit_unknown = True`. The next `submit_order` call sees
   171	`submit_unknown` and first calls `list_orders()`, looking for an order with
   172	our customer's `first_name` and `created_at >= submit_attempted_at - 60`
   173	(60s clock-skew allowance). Found → adopt its `id` as order_id, state
   174	`SUBMITTED`, message says the order went through. Not found → exactly one
   175	real retry. List endpoint itself fails → error `submit_unknown` with an
   176	honest message ("I'm not sure that went through — let me check" phrasing);
   177	never a blind re-POST.
   178	
   179	## Tool schemas
   180	
   181	All eight tools, OpenAI function-calling format.
   182	
   183	`SNAPSHOT` (one fixed shape, embedded in **every** success result — this is
   184	how the per-tool return table and the "full current state" rule compose):
   185	`{state, revision, items: [{type, code, name, qty, extras}], customer:
   186	{first_name, street_one} | null, read_back_done: bool}` — never a diff.
   187	
   188	| Tool | Parameters (JSON schema) | Success result — exact JSON |
   189	|---|---|---|
   190	| `get_menu` | `{}` | `{"menu": {"pizzas": [{code, name}], "pasta": [{code, name}], "toppings": [str]}, "snapshot": SNAPSHOT}` — `name` is the API's single display name, which the verified contract facts show serves both languages |
   191	| `add_items` | `{items: [{type: enum[pizza,pasta], code: str, qty: int ≥1, extras: [str]}]}` (required: items; extras default `[]`) | `{"snapshot": SNAPSHOT}` (basket + revision live in SNAPSHOT) |
   192	| `remove_item` | `{type: enum, code: str, qty: int ≥1 optional}` (absent qty = remove all of that line) | `{"snapshot": SNAPSHOT}` |
   193	| `set_customer` | `{first_name: str minLength 1, street_one: str optional}` | `{"customer": {first_name, street_one}, "snapshot": SNAPSHOT}` — customer as stored |
   194	| `read_back` | `{}` | `{"snapshot": SNAPSHOT}` — basket, customer, revision: the material the agent reads out |
   195	| `confirm_order` | `{revision: int}` | `{"snapshot": SNAPSHOT}` with `state == "CONFIRMED"`, or error if stale |
   196	| `submit_order` | `{}` | `{"order_id": str, "status": str, "eta_seconds": int, "snapshot": SNAPSHOT}` — the minutes conversion is the model's job, instructed by the prompt |
   197	| `check_street` | `{street: str}` | `{"street": str, "deliverable": bool, "snapshot": SNAPSHOT}` — the never-claim-verified rule lives in the prompt, not the tool |
   198	
   199	Failure shape: `{"error": {"code": "<one of the codes below>", "message":
   200	"<speakable sentence>", "candidates": [up to 3 of {type, code, name}]}}`.
   201	
   202	Error codes: `unknown_item` (with candidates), `invalid_extra` (with
   203	candidate toppings), `invalid_quantity` (non-integer or < 1 — the tool does
   204	not parse "zwei"), `empty_basket`, `invalid_state`, `stale_revision`,
   205	`read_back_required`, `order_closed`, `submit_failed`, `submit_unknown`,
   206	`api_unavailable`, `not_in_basket` (remove_item for a line that isn't there).
   207	
   208	Validation order in `add_items`: every item's `(type, code)` against the menu
   209	snapshot and every extra against `toppings[]`; any failure rejects the whole
   210	call atomically (no partial adds), returning the first error with candidates
   211	from `difflib.get_close_matches` over codes and lowercased names of the same
   212	type (falling back to the other type's matches so "pasta tonno" asked as
   213	pizza still gets a useful suggestion).
   214	
   215	## Agent loop (`core/agent.py`)
   216	
   217	- Messages: `[system] + history`. System prompt = `prompts/system.{lang}.md`
   218	  with `{pizzeria_name}` substituted (captured in startup step 2), where
   219	  `lang = PIZZERIA_LANG` — the pizzeria-country greeting language, a
   220	  required env var (see Configuration), **not** a channel or UI control.
   221	  Both prompt files state the same per-turn rule: always answer in the
   222	  language of the customer's latest message (German or English), unprompted.
   223	  Language mirroring is model behaviour; the runtime never detects language.
   224	- Per turn: POST `{LITELLM_PIZZA_URL}/chat/completions`, bearer
   225	  `LITELLM_PIZZA_KEY`, model `LITELLM_PIZZA_MODEL_1`, `tools` = the eight
   226	  schemas. While the response contains `tool_calls`: dispatch each through
   227	  `core/tools.py`, append tool result messages, call again. Stop on a plain
   228	  assistant message or after 8 tool iterations (loop guard → apology).
   229	- Gateway timeout (httpx timeout, 30s): one retry, then abort the turn with
   230	  the plain apology from the error table. Gateway 4xx/5xx: no retry, abort
   231	  turn, log.
   232	- The loop emits events to a callback: `user`, `assistant`, `tool_call`,
   233	  `tool_result`, `state`, `error` — the CLI prints them (verbose), the web
   234	  channel streams them as NDJSON, and every event is also appended as one
   235	  JSON line to `logs/agent-<session>.jsonl` (fixed path, gitignored). Log
   236	  records carry no secrets: config values never enter events; tool results
   237	  are logged as-is (they contain no secrets by construction).
   238	
   239	## Conversation policy → prompts
   240	
   241	`prompts/system.de.md` / `system.en.md`, same content in two languages, calm
   242	and short (no shouting — the state machine enforces the rules). Each covers:
   243	greet once in the file's language and offer help in one sentence; mirror the
   244	customer's language per turn (German ↔ English); one question per turn; menu
   245	facts only from `get_menu`; collect first name (confirm spelling when it
   246	came from speech) and street, street declinable; read back via `read_back`
   247	and wait for an explicit yes — "mhm"/silence is not yes, ask once more, then
   248	offer to start over; never announce success before `submit_order` returns;
   249	state order id in speakable groups and ETA in minutes; errors in plain
   250	language, never codes or JSON; never claim the address was checked for
   251	deliverability; when the reply will be spoken, at most three menu items plus
   252	an invitation.
   253	
   254	## Web channel protocol
   255	
   256	- `GET /` → static UI. `GET /config` → `{speech: bool}` (true only if
   257	  `SPEECH_URL` set and a probe succeeded at startup). No language field:
   258	  language is never a UI control — the greeting comes from `PIZZERIA_LANG`,
   259	  mirroring is model behaviour.
   260	- `POST /chat` body `{session_id, text}` → `application/x-ndjson` stream of

codex
No plan-sized findings. `PLAN.md` now closes the round-2 gaps with concrete plan text rather than hand-waving: the per-tool full-state contract is explicit via `SNAPSHOT` and the exact return table ([PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:183)), `PIZZERIA_LANG` is required and matches the oracle decision ([PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:96), [decisions/qa.md](/home/rob/bpm-pizza-vibecoding-solution/decisions/qa.md:10)), submit-timeout correlation is persisted as `submit_attempted_at` with verify-before-retry recovery ([PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:132)), the web contract removes any UI/chat language control and fences language use to the STT hint only ([PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:256)), and menu snapshot ownership is per-session and immutable ([PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:119)).

As devil’s advocate, I looked for remaining spec mismatches in the confirmation path, timeout handling, speech path, and tool contracts. The few remaining risks are implementation-sensitive rather than missing-plan-sensitive: the plan specifies the required behavior, tests, and boundaries tightly enough that implementing exactly it should satisfy `SPEC.md`.

SCORES (1-5 each, 5 = best):
completeness: 5
correctness: 5
error_handling: 5
simplicity: 4
spec_compliance: 5
TOTAL: 24/25
VERDICT: APPROVED
ISSUES:
tokens used
33,828
No plan-sized findings. `PLAN.md` now closes the round-2 gaps with concrete plan text rather than hand-waving: the per-tool full-state contract is explicit via `SNAPSHOT` and the exact return table ([PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:183)), `PIZZERIA_LANG` is required and matches the oracle decision ([PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:96), [decisions/qa.md](/home/rob/bpm-pizza-vibecoding-solution/decisions/qa.md:10)), submit-timeout correlation is persisted as `submit_attempted_at` with verify-before-retry recovery ([PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:132)), the web contract removes any UI/chat language control and fences language use to the STT hint only ([PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:256)), and menu snapshot ownership is per-session and immutable ([PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:119)).

As devil’s advocate, I looked for remaining spec mismatches in the confirmation path, timeout handling, speech path, and tool contracts. The few remaining risks are implementation-sensitive rather than missing-plan-sensitive: the plan specifies the required behavior, tests, and boundaries tightly enough that implementing exactly it should satisfy `SPEC.md`.

SCORES (1-5 each, 5 = best):
completeness: 5
correctness: 5
error_handling: 5
simplicity: 4
spec_compliance: 5
TOTAL: 24/25
VERDICT: APPROVED
ISSUES:
