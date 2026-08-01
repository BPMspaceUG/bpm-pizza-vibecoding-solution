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
session id: 019fbc5a-992c-7b23-8f5f-1da51e2784d2
--------
user
## Context

SPEC.md v3 (patched) was gate-approved in #1. Per the RETROFIT verdict with 5 binding conditions (decisions/qa.md, reviews/round10-grill-verdict.md), the implementer wrote PLAN.md v2 — the stage-1 plan for retrofitting the approved v1 build to SPEC v3. This issue is the plan gate; SPEC stage order is binding: no implementation before the plan is APPROVED.

## Judge request

You are the devil's advocate and judge for the PLAN stage. In the workspace (committed tree), read: PLAN.md (the artifact under review), SPEC.md (source of truth, v3 patched), decisions/qa.md (the 5 binding retrofit conditions), and — for what "carries over" claims refer to — the existing core/, channels/, tests/. Attack the plan: spec coverage gaps (especially the new web-channel contract, language authority, totals ownership, confirm control, browser E2E incl. the three failure paths, error-table additions), violations of the 5 conditions, contradictions with the approved v1 core it claims to reuse, and any underspecification an implementer could exploit.

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
I’m reviewing `PLAN.md` against `SPEC.md`, the retrofit conditions, and the current implementation it claims to reuse. I’ll read the required artifacts first, then trace carry-over claims into `core/`, `channels/`, and `tests/` to look for gaps, contradictions, and exploitable ambiguity.
exec
/bin/bash -lc "sed -n '1,220p' /home/rob/.agents/skills/using-superpowers/SKILL.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,320p' SPEC.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' decisions/qa.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' reviews/round10-grill-verdict.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' PLAN.md" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 409ms:
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

 succeeded in 454ms:
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
| `set_customer` | `first_name`, optional `street_one` | customer as stored |
| `read_back` | — | basket, customer, revision, and the code-computed basket total — the text the agent reads out |
| `confirm_order` | `revision` | state `CONFIRMED`, or error if stale |
| `submit_order` | — | `order_id`, `status`, `eta_seconds` |
| `check_street` | `street` | plausibility result (optional) |

Tool result conventions:

- Success: the **full current state**, not a diff. The model never
  reconstructs the basket from history.
- Failure: `{"error": {"code": "...", "message": "...", "candidates": [...]}}`.
  `message` is written so it can be spoken to the customer as-is.
- `add_items` with an unknown code returns `unknown_item` plus up to three

 succeeded in 481ms:
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

 succeeded in 467ms:
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
  `Agent.confirm_and_submit(session, revision, emit)`:
  1. `tools.dispatch("confirm_order", {revision})` — stale revision or
     wrong state returns the typed error; it streams to the UI as a
     notice and nothing is submitted.
  2. On success `tools.dispatch("submit_order", {})` (full v1 semantics
     incl. timeout recovery).
  3. Both calls are appended to `session.messages` as a synthetic
     assistant `tool_calls` message + `tool` results (OpenAI format), so
     the model's context stays consistent.
  4. One model call phrases the outcome (order id in groups, minutes);
     it streams like a normal turn and is logged.
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
  pizzeria_name, lang}`. Invalid id → 409 with the session-error text.
- `POST /chat {session_id, text|null}` → NDJSON stream (unchanged
  protocol; `text: null` = greeting turn). 404 for unknown session (the
  UI then creates a fresh one). Per-session lock → 409 on overlap.
- `POST /confirm {session_id, revision}` → NDJSON stream (same event
  shapes) via `confirm_and_submit`.
- `POST /language {session_id, lang}` → `{lang}`; core `set_language`.
- `GET /health` → `{api: "ok"|"down", gateway: "ok"|"down"|"unknown"}` —
  `api` from a live `GET /pizzerias` with 3s timeout; `gateway` from the
  outcome of the most recent model call (unknown before the first).
  Polled by the UI every 30s for the footer connection state.
- Speech proxy endpoints move to `channels/speech.py` (deliverable):
  `SpeechService` class (config, probe, stt(audio, lang), tts(text,
  lang)); web.py keeps only the thin route handlers.

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
  - all notices in the session language, plain words.

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

All other rows: unchanged v1 mechanics, already tested.

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
     lock + order id visible; basket totals correct at each step;
  2. pizzeria switch: selector → fresh conversation, header + footer UUID
     change, basket cleared;
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

 succeeded in 487ms:
OpenAI Codex v0.143.0
--------
workdir: /home/rob/bpm-pizza-vibecoding-solution
model: gpt-5.4
provider: openai
approval: never
sandbox: read-only
reasoning effort: medium
reasoning summaries: none
session id: 019fbc15-55c4-7c62-bf4a-80276d9ad662
--------
user
You are the devil's advocate/judge continuing a grill session (stateless — context follows). Repository in cwd; read files as needed.

Previous round (reviews/round9-audit-grill.md): you audited the repo (PASS) and asked 6 questions about the implementer's decision to RETROFIT the v1 codebase to the new SPEC.md v2 instead of restarting. Preliminary leaning was RETROFIT conditional on honest answers. Here are the implementer's answers; judge them, then give the final verdict.

A1 (tenancy): Session (core) gains pizzeria_id, pizzeria_name, client, lang. A core factory create_session(pizzeria_id) validates the id against GET /pizzerias, builds a tenant-bound PizzaSim client, fetches a fresh menu snapshot, renders the prompt with that pizzeria's name. Agent becomes stateless w.r.t. tenant: run_turn uses session.client (dispatch already takes client as a parameter). The transport only passes identifiers (session_id, pizzeria_id) — construction and validation live in core. The startup PIZZERIA_ID check remains: the preselected tenant must exist or the process refuses to start.

A2 (language): lang moves from AgentConfig into Session (initial value = PIZZERIA_LANG, which stays the greeting-language default). The UI switch sets session.lang server-side; messages[0] (system prompt) is re-rendered in the new language in place — same policy text, history preserved, no stale prompt. Apologies and the STT hint read session.lang. No cross-session leakage because nothing language-related remains process-global.

A3 (confirm control): the read_back tool result already streams the revision. The UI renders an explicit confirm button bound to that revision. Click -> POST /confirm {session_id, revision} -> ONE core entry point Agent.confirm_and_submit(session, revision, emit): it calls tools.dispatch("confirm_order", {revision}) and then tools.dispatch("submit_order") — the state machine still enforces read-back-bound revision (stale revision = error to the UI); the synthetic tool_calls + tool results are appended to the message history in OpenAI format so the model's context stays consistent; then one model call phrases the outcome to the customer. Customer action is explicit (a click, not a word); CONFIRMED is reachable only via confirm_order(revision); the transport owns zero logic (it forwards two identifiers to core). The CLI keeps the conversational yes -> model calls confirm_order path; both paths converge on the same dispatch.

A4 (tenant switch race): switching pizzeria generates a NEW client-side session_id (fresh conversation per spec); the old session is abandoned, its in-flight fetch is aborted client-side (AbortController) and the chat view cleared. Server-side a Session's tenant is immutable after creation, so old-tenant tool results structurally cannot land in a new-tenant session; locks stay per session_id; resend-after-switch posts into the new session which has no old basket.

A5 (prices): canonical in core. Menu keeps price per (type, code); Item copies unit_price at add time from the immutable session menu; Order.snapshot() gains unit_price, line_total and basket_total computed in core only. get_menu result includes prices; read_back includes the total so the agent reads back exactly what the UI shows — one computation, two renderings. Extras: the API prices only base items (toppings carry no price), so the total is the sum of base prices and the UI labels extras as not separately priced — no invented figures, per spec.

A6 (honesty about the web layer): conceded — the web layer is a substantial rewrite, not an additive patch, and the retrofit claim applies to the repo, not to app.js line counts. Survives: server-side NDJSON streaming, speech proxies + probe, per-session locking, startup checks, and in the client the stream reader, push-to-talk recorder and TTS playback as functions. New: header (name, selector with short UUIDs, dashboard link, language switch, start over), footer (APP_VERSION, full UUID, connection states, docs link), visible basket with total, confirm control, the no-message-unanswered invariant paths (done-event handling, stream-ended-without-answer notice, typed error notices with resend), UI i18n. The browser E2E harness (Playwright, already working on this host) is new work in BOTH scenarios, so it does not differentiate retrofit vs restart. What restart would additionally cost: rewriting core/state/tools/client/agent (approved, 71 tests) with fresh bug risk for zero spec gain, and losing the committed review trail.

Also note: the implementer already restored the verified contract-facts section into SPEC.md v2 and probed the two new contract facts live (dashboard path /dashboard/pizzerias/{id} from the dashboard's own routing code; API docs at /swagger.html).

Judge the answers. If an answer is wrong or evasive, say so concretely. Then output exactly:
VERDICT: RETROFIT | RESTART
CONDITIONS: max 5 bullets the retrofit plan MUST satisfy (empty if none)

codex
Using `using-superpowers` first, then I’ll read the prior grill notes and the spec context so I can judge these answers against the repository rather than against memory.
exec
/bin/bash -lc "sed -n '1,220p' /home/rob/.agents/skills/using-superpowers/SKILL.md" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 115ms:
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
Using `using-superpowers` to set the workflow. I’m checking its Codex-specific instructions, then I’ll inspect the prior audit and the current spec/contracts that these answers rely on.
exec
/bin/bash -lc "sed -n '1,260p' reviews/round9-audit-grill.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,220p' /home/rob/.agents/skills/using-superpowers/references/codex-tools.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' SPEC.md" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 231ms:
OpenAI Codex v0.143.0
--------
workdir: /home/rob/bpm-pizza-vibecoding-solution
model: gpt-5.4
provider: openai
approval: never
sandbox: read-only
reasoning effort: medium
reasoning summaries: none
session id: 019fbc11-d581-7033-bfbd-377e84f2715b
--------
user
You are the independent auditor and devil's advocate for the repository in the current working directory. Read-only. Two jobs in this pass.

JOB 1 — AUDIT (trust nothing, verify in the repo):
The implementer claims: SPEC v1 was fully built and approved (reviews/round1..8, reviews/scores.md with plan approved 24/25 and implementation approved 24/25, hotfix approved 24/25); 71 deterministic tests exist and are self-consistent; core/ implements the state machine, tool dispatch, PizzaSim client with submit-timeout recovery; channels/cli.py and channels/web.py + static UI exist; decisions/qa.md records oracle decisions. Verify each claim against the files and git log. Report discrepancies bluntly.

JOB 2 — GRILL THE DECISION:
SPEC.md was just replaced by the operator with v2 (git show HEAD -- SPEC.md; previous version is SPEC_20260801.md and in git history). Delta: prices + basket total in scope; multi-pizzeria (customer-selectable in the UI, PIZZERIA_ID only preselects; basket never crosses tenants; fresh conversation on switch); APP_VERSION env shown in footer; an entirely new "The web channel" section (header: pizzeria name, selector from GET /pizzerias with short UUIDs, dashboard link per pizzeria, DE/EN language switch applied to replies and speech, start-over; footer: version, full UUID, connection state for API+gateway, API docs link; "no message ends unanswered" invariant; visible basket with total; read-back with an explicit confirm CONTROL; basket locked after submit); mandatory headless-browser E2E tests incl. three failure paths; getUserMedia/MediaRecorder now explicitly sanctioned.

The implementer's position, which you must attack: RETROFIT the existing codebase (do not restart from scratch). Rationale: the unchanged spec sections (soul, load-bearing idea, state machine, tools, error handling, anti-patterns, speech service, CLI) are already built, reviewed and tested (71 tests); the delta is additive and concentrated in the web layer + a session-level tenancy generalization + price fields; a restart would rewrite identical core code with fresh bug risk and lose the review trail. Planned retrofit sketch: (a) core: menu carries prices, get_menu/read_back expose price + basket total; PizzaSim client instantiated per session for the session's pizzeria (preselected id validated at startup; selector list from GET /pizzerias); (b) web: new header/footer/basket UI per spec, confirm control wired as customer action, language switch selects prompt+STT language per session (PIZZERIA_LANG stays the startup default), APP_VERSION required env; (c) tests: extend unit/tool tests for prices+tenancy, add Playwright browser E2E incl. the three failure paths (Playwright already proven working on this host); (d) PLAN.md updated first, re-reviewed before implementation.

Attack this: where does retrofit risk silently violating v2? Is any v1 architectural decision now invalid (e.g. one client per process, PIZZERIA_LANG required var vs the new UI language switch, /config contract)? Is the confirm-control design sound given "the transport owns no order logic" and "CONFIRMED only via confirm_order(revision)"? Would a restart actually be cheaper or safer anywhere? Ask your hardest questions (max 6, numbered) — the implementer will answer them in the next call before you give a verdict. If the audit in JOB 1 found discrepancies, include them as questions.

End with:
AUDIT: PASS | DISCREPANCIES (list)
QUESTIONS: numbered list, max 6
PRELIMINARY LEANING: RETROFIT | RESTART | UNDECIDED (one line why)

codex
I’m treating this as a repo audit plus an architectural challenge to the retrofit plan. I’ll first load the required skill instructions, then inspect the repository, test artifacts, and git history to verify each claim against the files.
exec
/bin/bash -lc "sed -n '1,220p' /home/rob/.agents/skills/using-superpowers/SKILL.md" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 137ms:
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
Using `using-superpowers` to establish the required workflow, then I’ll inspect the repo and git history under that process. After that I’ll verify each claimed artifact and look for architectural faults in the retrofit argument.
exec
/bin/bash -lc "sed -n '1,240p' /home/rob/.agents/skills/references/codex-tools.md" in /home/rob/bpm-pizza-vibecoding-solution
 exited 2 in 345ms:
sed: can't read /home/rob/.agents/skills/references/codex-tools.md: No such file or directory

codex
The skill reference path in the skill file is stale. I’m locating the actual Codex reference file now, then continuing the audit once the required instructions are loaded.
exec
/bin/bash -lc "rg --files /home/rob/.agents/skills | rg 'codex-tools\\.md|using-superpowers|references'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "rg --files /home/rob/.codex/skills | rg 'codex-tools\\.md|using-superpowers|references'" in /home/rob/bpm-pizza-vibecoding-solution
 exited 1 in 455ms:
 succeeded in 737ms:
/home/rob/.agents/skills/using-superpowers/SKILL.md
/home/rob/.agents/skills/using-superpowers/references/codex-tools.md
/home/rob/.agents/skills/using-superpowers/references/pi-tools.md
/home/rob/.agents/skills/using-superpowers/references/gemini-tools.md
/home/rob/.agents/skills/using-superpowers/references/antigravity-tools.md
/home/rob/.agents/skills/skill-creator/references/output-patterns.md
/home/rob/.agents/skills/skill-creator/references/workflows.md
/home/rob/.agents/skills/excalidraw-diagram-generator/references/element-types.md
/home/rob/.agents/skills/excalidraw-diagram-generator/references/excalidraw-schema.md

exec
/bin/bash -lc "sed -n '1,240p' /home/rob/.agents/skills/using-superpowers/references/codex-tools.md" in /home/rob/bpm-pizza-vibecoding-solution
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

codex
Using `using-superpowers` to set the workflow. Next I’m checking the approved v1 implementation surfaces the plan says it will reuse, because any mismatch there is a plan defect, not an implementation detail.
exec
/bin/bash -lc 'rg --files core channels tests | sort' in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,320p' core/state.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,360p' core/tools.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,320p' core/menu.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,360p' core/agent.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' core/order.py" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 544ms:
channels/__init__.py
channels/cli.py
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
tests/__init__.py
tests/fixtures/error_422.json
tests/fixtures/location.json
tests/fixtures/menu.json
tests/fixtures/order_created.json
tests/fixtures/orders_list.json
tests/fixtures/pizzerias.json
tests/test_state.py
tests/test_tools.py
tests/test_transcripts.py
tests/transcripts/correction.json
tests/transcripts/happy_path.json
tests/transcripts/mind_change.json
tests/transcripts/submit_timeout.json
tests/transcripts/unknown_item.json

 succeeded in 865ms:
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

 succeeded in 952ms:
"""Model loop: prompt assembly, chat-completions calls, tool dispatch,
JSONL event logging. The model only speaks; the order lives in core."""
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
from .pizzasim import PizzaSim, optional_env, require_env

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


class GatewayError(Exception):
    pass


@dataclass
class AgentConfig:
    url: str
    key: str
    model: str
    lang: str  # PIZZERIA_LANG: greeting language = pizzeria country

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
    history."""
    order: Order
    menu: Menu
    messages: list[dict]
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])

    @classmethod
    def create(cls, config: AgentConfig, menu: Menu,
               pizzeria_name: str) -> "Session":
        return cls(
            order=Order(),
            menu=menu,
            messages=[{"role": "system",
                       "content": system_prompt(config.lang,
                                                pizzeria_name)}],
        )


def log_event(session: Session, event: dict) -> None:
    """One line per event, JSON, to a file. Never carries config values."""
    LOG_DIR.mkdir(exist_ok=True)
    record = {"ts": round(time.time(), 3), "session": session.id, **event}
    with (LOG_DIR / f"agent-{session.id}.jsonl").open("a") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")


class Agent:
    def __init__(self, config: AgentConfig, client: PizzaSim,
                 chat_fn=None):
        self.config = config
        self.client = client
        # chat_fn(messages, tools) -> assistant message dict; injectable so
        # the golden transcripts run against a stub with no network.
        self._chat_fn = chat_fn or self._gateway_chat

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
                return response.json()["choices"][0]["message"]
            except httpx.TimeoutException as exc:
                last_exc = exc
                continue
            except (httpx.HTTPError, KeyError, ValueError) as exc:
                raise GatewayError(f"gateway request failed: "
                                   f"{type(exc).__name__}") from exc
        raise GatewayError("gateway timed out twice") from last_exc

    def run_turn(self, session: Session, user_text: str | None,
                 emit=lambda event: None) -> str:
        """One customer turn: returns the assistant's final text. Every
        intermediate step goes to emit() and the JSONL log. user_text None
        is the opening turn — the agent greets first, unprompted."""

        def event(payload: dict) -> None:
            log_event(session, payload)
            emit(payload)

        if user_text is not None:
            session.messages.append({"role": "user", "content": user_text})
            event({"type": "user", "text": user_text})

        for _ in range(MAX_TOOL_ROUNDS):
            try:
                message = self._chat_fn(session.messages,
                                        tools.openai_tools())
            except GatewayError as exc:
                event({"type": "error", "error": str(exc)})
                apology = APOLOGY[self.config.lang]
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
                                        self.client, name, args)
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
        apology = APOLOGY[self.config.lang]
        session.messages.append({"role": "assistant", "content": apology})
        event({"type": "assistant", "text": apology})
        return apology


def startup(config: AgentConfig) -> tuple[PizzaSim, str, Menu]:
    """The one startup sequence (PLAN): env → pizzeria check → menu.
    Raises before the first turn on any failure."""
    client = PizzaSim.from_env()
    pizzeria_name = client.pizzeria_name()
    menu = Menu(client.get_menu())
    return client, pizzeria_name, menu

 succeeded in 1018ms:
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

 succeeded in 992ms:
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
        self.toppings: list[str] = list(payload.get("toppings", []))

    def as_tool_result(self) -> dict:
        return {
            "pizzas": [{"code": c, "name": n}
                       for c, n in self._by_type["pizza"].items()],
            "pasta": [{"code": c, "name": n}
                      for c, n in self._by_type["pasta"].items()],
            "toppings": self.toppings,
        }

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

 succeeded in 963ms:
"""Order data: items, customer, revision, submit bookkeeping. Pure data."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


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

    def line_key(self) -> tuple:
        return (self.type, self.code, tuple(sorted(self.extras)))


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
                }
                for i in self.items
            ],
            "customer": self.customer.as_dict() if self.customer else None,
            "read_back_done": self.read_back_revision == self.revision,
        }

codex
The existing core is mostly as the plan describes, but the current `Agent` is still process-tenant and process-language scoped. I’m checking whether `PLAN.md` fully accounts for every place that architecture leaks into the web contract and tests.
exec
/bin/bash -lc "sed -n '1,260p' tests/test_tools.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,240p' tests/test_state.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,320p' channels/static/app.js" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,360p' channels/web.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' tests/test_transcripts.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc 'rg -n "APP_VERSION|confirm|health|session|language|pizzer|done|assistant|tool_result|gateway|speech|resend|basket_total|unit_price|line_total" -S channels tests core PLAN.md SPEC.md' in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 1070ms:
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

 succeeded in 1048ms:
"""State machine, exhaustively: every ✗ cell of the transition table in
PLAN.md and every SPEC invariant 1-4 (invariant 5, menu validation, lives in
test_tools.py)."""
import pytest

from core.order import Customer, Item, Order, State
from core import state


def item(code="margherita", type_="pizza", qty=1, extras=None):
    return Item(type=type_, code=code, name=code.title(), qty=qty,
                extras=extras or [])


def order_in(target: State) -> Order:
    o = Order()
    if target is State.EMPTY:
        return o
    state.add_items(o, [item()])
    if target is State.COLLECTING:
        return o
    state.set_customer(o, Customer("Marco", "via Roma"))
    if target is State.READY:
        return o
    state.read_back(o)
    state.confirm(o, o.revision)
    if target is State.CONFIRMED:
        return o
    state.begin_submit(o)
    state.mark_submitted(o, {"order_id": "x", "status": "ordered",
                             "eta_seconds": 600})
    return o


def expect(code):
    return pytest.raises(state.TransitionError, match="")


# --- happy path -----------------------------------------------------------

def test_full_happy_path():
    o = Order()
    assert o.state is State.EMPTY
    state.add_items(o, [item(qty=2)])
    assert o.state is State.COLLECTING
    state.set_customer(o, Customer("Marco", "via Roma"))
    assert o.state is State.READY
    state.read_back(o)
    state.confirm(o, o.revision)
    assert o.state is State.CONFIRMED
    state.begin_submit(o)
    state.mark_submitted(o, {"order_id": "abc", "status": "ordered",
                             "eta_seconds": 90})
    assert o.state is State.SUBMITTED
    assert o.result["order_id"] == "abc"


def test_customer_before_items_is_legal_and_stays_empty():
    o = Order()
    state.set_customer(o, Customer("Anna"))
    assert o.state is State.EMPTY
    state.add_items(o, [item()])
    assert o.state is State.READY  # customer already known


# --- illegal cells, one test per ✗ ---------------------------------------

@pytest.mark.parametrize("mutate", [
    lambda o: state.add_items(o, [item()]),
    lambda o: state.remove_item(o, "pizza", "margherita", None),
    lambda o: state.set_customer(o, Customer("Eve")),
    lambda o: state.read_back(o),
    lambda o: state.confirm(o, o.revision),
    lambda o: state.begin_submit(o),
])
def test_submitted_is_terminal(mutate):
    o = order_in(State.SUBMITTED)
    with pytest.raises(state.TransitionError) as e:
        mutate(o)
    assert e.value.code == "order_closed"


def test_remove_from_empty():
    with pytest.raises(state.TransitionError) as e:
        state.remove_item(order_in(State.EMPTY), "pizza", "margherita", None)
    assert e.value.code == "empty_basket"


def test_read_back_empty():
    with pytest.raises(state.TransitionError) as e:
        state.read_back(order_in(State.EMPTY))
    assert e.value.code == "empty_basket"


def test_read_back_collecting_needs_customer():
    with pytest.raises(state.TransitionError) as e:
        state.read_back(order_in(State.COLLECTING))
    assert e.value.code == "invalid_state"


@pytest.mark.parametrize("st", [State.EMPTY, State.COLLECTING])
def test_confirm_illegal_states(st):
    o = order_in(st)
    with pytest.raises(state.TransitionError) as e:
        state.confirm(o, o.revision)
    assert e.value.code == "invalid_state"


def test_confirm_when_already_confirmed():
    o = order_in(State.CONFIRMED)
    with pytest.raises(state.TransitionError) as e:
        state.confirm(o, o.revision)
    assert e.value.code == "invalid_state"


@pytest.mark.parametrize("st", [State.EMPTY, State.COLLECTING, State.READY])
def test_submit_outside_confirmed(st):
    """Invariant 1: submit outside CONFIRMED is refused (incl. empty)."""
    o = order_in(st)
    with pytest.raises(state.TransitionError) as e:
        state.begin_submit(o)
    assert e.value.code == "invalid_state"


def test_remove_unknown_line():
    o = order_in(State.COLLECTING)
    with pytest.raises(state.TransitionError) as e:
        state.remove_item(o, "pasta", "pesto", None)
    assert e.value.code == "not_in_basket"


# --- invariant 2: mutation after CONFIRMED demotes ------------------------

def test_add_after_confirmed_demotes_to_ready():
    o = order_in(State.CONFIRMED)
    state.add_items(o, [item("funghi")])
    assert o.state is State.READY


def test_remove_after_confirmed_demotes():
    o = order_in(State.CONFIRMED)
    state.remove_item(o, "pizza", "margherita", None)
    assert o.state is State.EMPTY  # last item gone, customer kept


def test_set_customer_after_confirmed_demotes():
    o = order_in(State.CONFIRMED)
    state.set_customer(o, Customer("Mario"))
    assert o.state is State.READY


def test_confirmation_does_not_survive_demotion():
    """A confirmation applies to the basket that was read back."""
    o = order_in(State.CONFIRMED)
    state.add_items(o, [item("funghi")])
    with pytest.raises(state.TransitionError):
        state.begin_submit(o)


# --- invariant 3: confirm tied to read-back + revision --------------------

def test_confirm_without_read_back():
    o = order_in(State.READY)
    with pytest.raises(state.TransitionError) as e:
        state.confirm(o, o.revision)
    assert e.value.code == "read_back_required"


def test_confirm_with_stale_revision():
    o = order_in(State.READY)
    state.read_back(o)
    stale = o.revision
    state.add_items(o, [item("funghi")])
    with pytest.raises(state.TransitionError) as e:
        state.confirm(o, stale)
    assert e.value.code == "stale_revision"


def test_read_back_of_old_revision_does_not_allow_confirm():
    o = order_in(State.READY)
    state.read_back(o)
    state.add_items(o, [item("funghi")])  # bumps revision
    with pytest.raises(state.TransitionError) as e:
        state.confirm(o, o.revision)
    assert e.value.code == "read_back_required"


# --- basket mechanics -----------------------------------------------------

def test_revision_increments_on_every_mutation():
    o = Order()
    r0 = o.revision
    state.add_items(o, [item()])
    state.set_customer(o, Customer("A"))
    state.remove_item(o, "pizza", "margherita", None)
    assert o.revision == r0 + 3


def test_merge_same_line():
    o = Order()
    state.add_items(o, [item(qty=1)])
    state.add_items(o, [item(qty=2)])
    assert len(o.items) == 1 and o.items[0].qty == 3


def test_same_code_different_extras_is_separate_line():
    o = Order()
    state.add_items(o, [item(qty=1)])
    state.add_items(o, [item(qty=1, extras=["mushrooms"])])
    assert len(o.items) == 2


def test_partial_remove():
    o = Order()
    state.add_items(o, [item(qty=3)])
    state.remove_item(o, "pizza", "margherita", 1)
    assert o.items[0].qty == 2
    state.remove_item(o, "pizza", "margherita", 5)  # >= qty removes line
    assert o.items == []
    assert o.state is State.EMPTY


def test_remove_to_empty_and_readd():
    o = order_in(State.READY)
    state.remove_item(o, "pizza", "margherita", None)
    assert o.state is State.EMPTY
    state.add_items(o, [item("funghi")])
    assert o.state is State.READY  # customer survived


def test_type_and_code_key_removal():
    """tonno exists as pizza and pasta — removal must key on (type, code)."""
    o = Order()
    state.add_items(o, [item("tonno", "pizza"), item("tonno", "pasta")])
    state.remove_item(o, "pasta", "tonno", None)
    assert [i.type for i in o.items] == ["pizza"]


def test_remove_without_qty_clears_all_variants():
    """Same (type, code), different extras: no-qty removal takes them all."""

 succeeded in 963ms:
/* Web chat over the NDJSON stream. Speech is push-to-talk via
   MediaRecorder + the server's speech proxy — no browser speech APIs. */
"use strict";

const chat = document.getElementById("chat");
const form = document.getElementById("composer");
const input = document.getElementById("text");
const send = document.getElementById("send");
const mic = document.getElementById("mic");
const ttsWrap = document.getElementById("tts-wrap");
const ttsToggle = document.getElementById("tts-toggle");

// crypto.randomUUID needs a secure context (HTTPS/localhost); the demo may
// be served over plain HTTP, so fall back to getRandomValues.
const sessionId = crypto.randomUUID
  ? crypto.randomUUID()
  : Array.from(crypto.getRandomValues(new Uint8Array(16)),
               (b) => b.toString(16).padStart(2, "0")).join("");
let speechEnabled = false;

function add(cls, text) {
  const div = document.createElement("div");
  div.className = "msg " + cls;
  div.textContent = text;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
  return div;
}

function notice(text) {
  const div = document.createElement("div");
  div.className = "notice";
  div.textContent = text;
  chat.appendChild(div);
}

function stepsBlock() {
  const details = document.createElement("details");
  details.className = "steps";
  details.innerHTML = "<summary>Zwischenschritte</summary>";
  chat.appendChild(details);
  return details;
}

async function turn(text) {
  send.disabled = true;
  if (text !== null) add("user", text);
  const steps = stepsBlock();
  let finalText = "";
  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: sessionId, text }),
    });
    if (!res.ok) throw new Error(await res.text());
    const reader = res.body.getReader();
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
            + (ev.tool || "") + " "
            + JSON.stringify(ev.args ?? ev.result);
          steps.appendChild(pre);
        } else if (ev.type === "assistant") {
          finalText = ev.text;
          add("assistant", ev.text);
        } else if (ev.type === "error") {
          notice("Es gab einen technischen Fehler.");
        }
      }
    }
  } catch (err) {
    notice("Verbindung fehlgeschlagen — bitte noch einmal versuchen.");
  }
  if (!steps.querySelector("pre")) steps.remove();
  send.disabled = false;
  input.focus();
  if (finalText && speechEnabled && ttsToggle.checked) speak(finalText);
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text) return;
  input.value = "";
  turn(text);
});

/* --- speech: push-to-talk, server-proxied ------------------------------ */

let recorder = null;

async function startRecording() {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  recorder = new MediaRecorder(stream);
  const chunks = [];
  recorder.ondataavailable = (e) => chunks.push(e.data);
  recorder.onstop = async () => {
    stream.getTracks().forEach((t) => t.stop());
    mic.classList.remove("recording");
    mic.setAttribute("aria-pressed", "false");
    const blob = new Blob(chunks, { type: recorder.mimeType });
    const body = new FormData();
    body.append("audio", blob, "speech.webm");
    try {
      const res = await fetch("/speech/stt", { method: "POST", body });
      if (!res.ok) throw new Error();
      const { text } = await res.json();
      if (text.trim()) turn(text.trim());
      else notice("Ich habe nichts verstanden — bitte noch einmal.");
    } catch {
      notice("Spracherkennung gerade nicht erreichbar — bitte tippen.");
    }
  };
  recorder.start();
  mic.classList.add("recording");
  mic.setAttribute("aria-pressed", "true");
}

mic.addEventListener("click", () => {
  if (recorder && recorder.state === "recording") recorder.stop();
  else startRecording().catch(() => notice("Kein Mikrofonzugriff."));
});

async function speak(text) {
  try {
    const res = await fetch("/speech/tts", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    if (!res.ok) throw new Error();
    new Audio(URL.createObjectURL(await res.blob())).play();
  } catch {
    notice("Vorlesen gerade nicht möglich.");
  }
}

/* --- boot -------------------------------------------------------------- */

(async () => {
  try {
    const cfg = await (await fetch("/config")).json();
    if (cfg.pizzeria) {
      document.getElementById("title").textContent = cfg.pizzeria;
      document.title = cfg.pizzeria;
    }
    // TTS is server-proxied audio and works in any context; only the mic
    // needs getUserMedia/MediaRecorder, which insecure contexts lack.
    speechEnabled = cfg.speech;    // unset SPEECH_URL → nothing rendered
    if (speechEnabled) {
      ttsWrap.hidden = false;
      if (navigator.mediaDevices && window.MediaRecorder) mic.hidden = false;
    }
  } catch { /* text chat works regardless */ }
  turn(null); // opening turn: the agent greets first
})();

 succeeded in 979ms:
"""FastAPI web channel on port 8888. Same core, zero order logic here.

Streams the agent's intermediate steps as newline-delimited JSON and
proxies the optional self-hosted speech service (STT/TTS). If SPEECH_URL is
unset or the service doesn't answer at startup, speech endpoints return 404
and the UI renders text-only.

Run:  python -m channels.web
"""
from __future__ import annotations

import json
import queue
import sys
import threading
from pathlib import Path

import httpx
import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse, Response, StreamingResponse
from fastapi.staticfiles import StaticFiles

from core.agent import Agent, AgentConfig, Session, startup
from core.menu import Menu
from core.pizzasim import ConfigError, PizzaSimError, optional_env

STATIC = Path(__file__).resolve().parent / "static"
app = FastAPI(title="PizzaSim ordering agent")


class Speech:
    """Config + probe for the self-hosted speech container. All-or-nothing:
    enabled only if SPEECH_URL is set, answers, and models are configured."""

    def __init__(self):
        self.url = optional_env("SPEECH_URL")
        self.stt_model = optional_env("SPEECH_STT_MODEL")
        self.tts_model = optional_env("SPEECH_TTS_MODEL")
        self.voice = optional_env("SPEECH_TTS_VOICE")
        self.enabled = False
        if self.url and self.stt_model and self.tts_model and self.voice:
            try:
                httpx.get(f"{self.url.rstrip('/')}/v1/models",
                          timeout=3.0).raise_for_status()
                self.enabled = True
            except httpx.HTTPError:
                print("speech service not answering — text-only mode",
                      file=sys.stderr)


@app.on_event("startup")
def boot() -> None:
    try:
        config = AgentConfig.from_env()
        client, pizzeria_name, _menu = startup(config)
    except (ConfigError, ValueError) as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        raise SystemExit(1)
    except PizzaSimError as exc:
        print(f"Startup check against PizzaSim failed: {exc}\n"
              "We're not taking orders right now.", file=sys.stderr)
        raise SystemExit(1)
    app.state.config = config
    app.state.client = client
    app.state.pizzeria_name = pizzeria_name
    app.state.agent = Agent(config, client)
    app.state.sessions = {}
    app.state.locks = {}  # one Lock per session: turns are serialized
    app.state.speech = Speech()


@app.get("/")
def index():
    return FileResponse(STATIC / "index.html")


@app.get("/config")
def ui_config():
    # Contract per plan: speech flag + pizzeria display name. The customer
    # must see which pizzeria they are ordering at.
    return {"speech": app.state.speech.enabled,
            "pizzeria": app.state.pizzeria_name}


def _get_session(session_id: str) -> Session:
    sessions = app.state.sessions
    if session_id not in sessions:
        # Fresh immutable menu snapshot per session (SPEC invariant 5).
        try:
            menu = Menu(app.state.client.get_menu())
        except PizzaSimError:
            raise HTTPException(503, "We're not taking orders right now.")
        sessions[session_id] = Session.create(
            app.state.config, menu, app.state.pizzeria_name)
    return sessions[session_id]


@app.post("/chat")
async def chat(body: dict):
    session_id = str(body.get("session_id") or "")
    if not session_id:
        raise HTTPException(422, "session_id required")
    text = body.get("text")  # None → opening turn, agent greets
    if text is not None and not str(text).strip():
        raise HTTPException(422, "text must not be empty")
    session = _get_session(session_id)
    lock = app.state.locks.setdefault(session_id, threading.Lock())
    if not lock.acquire(blocking=False):
        # One Order per conversation means one turn at a time: overlapping
        # requests would interleave mutations and break the revision-bound
        # confirmation guarantees.
        raise HTTPException(409, "a turn is already in progress")

    events: queue.Queue = queue.Queue()

    def run() -> None:
        try:
            app.state.agent.run_turn(session, text, events.put)
        finally:
            events.put({"type": "done",
                        "state": session.order.snapshot()})
            events.put(None)
            lock.release()

    threading.Thread(target=run, daemon=True).start()

    def ndjson():
        while (event := events.get()) is not None:
            yield json.dumps(event, ensure_ascii=False) + "\n"

    return StreamingResponse(ndjson(), media_type="application/x-ndjson")


def _speech() -> Speech:
    speech = app.state.speech
    if not speech.enabled:
        raise HTTPException(404, "speech is not available")
    return speech


@app.post("/speech/stt")
async def stt(audio: UploadFile):
    speech = _speech()
    files = {"file": (audio.filename or "audio.webm", await audio.read(),
                      audio.content_type or "audio/webm")}
    data = {"model": speech.stt_model,
            "language": app.state.config.lang}  # STT hint only
    try:
        response = httpx.post(
            f"{speech.url.rstrip('/')}/v1/audio/transcriptions",
            files=files, data=data, timeout=60.0)
        response.raise_for_status()
    except httpx.HTTPError:
        raise HTTPException(502, "speech service unavailable")
    return {"text": response.json().get("text", "")}


@app.post("/speech/tts")
async def tts(body: dict):
    speech = _speech()
    text = str(body.get("text") or "")
    if not text:
        raise HTTPException(422, "text required")
    try:
        response = httpx.post(
            f"{speech.url.rstrip('/')}/v1/audio/speech",
            json={"model": speech.tts_model, "voice": speech.voice,
                  "input": text},
            timeout=60.0)
        response.raise_for_status()
    except httpx.HTTPError:
        raise HTTPException(502, "speech service unavailable")
    return Response(response.content,
                    media_type=response.headers.get("content-type",
                                                    "audio/mpeg"))


app.mount("/static", StaticFiles(directory=STATIC), name="static")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8888)

 succeeded in 989ms:
"""Golden transcripts: five scripted conversations run through the real
agent loop against a stub model that replays fixed tool calls. Asserts the
final state and the calls actually made. No network, no LLM."""
import json
import time
from pathlib import Path

import pytest

from core.agent import Agent, AgentConfig, Session
from core.menu import Menu
from core.order import Order
from core.pizzasim import ApiTimeout

FIXTURES = Path(__file__).parent / "fixtures"
TRANSCRIPTS = sorted((Path(__file__).parent / "transcripts").glob("*.json"))


class StubModel:
    """Replays a transcript's scripted actions, one per chat call."""

    def __init__(self, turns):
        self._queues = [list(turn["script"]) for turn in turns]
        self._current = None

    def next_turn(self):
        self._current = self._queues.pop(0)

    def __call__(self, messages, tool_schemas):
        action = self._current.pop(0)
        if "tool" in action:
            assert any(t["function"]["name"] == action["tool"]
                       for t in tool_schemas), action["tool"]
            return {"tool_calls": [{
                "id": f"call-{action['tool']}",
                "function": {"name": action["tool"],
                             "arguments": json.dumps(action["args"])},
            }]}
        return {"content": action["say"]}


class ScriptedClient:
    """Fake PizzaSim: 'ok' submits succeed; 'timeout_then_recover' times
    out once, then the order shows up in the list."""

    def __init__(self, mode):
        self.mode = mode
        self.submits = 0
        self.created = json.loads((FIXTURES / "order_created.json")
                                  .read_text())

    def submit_order(self, customer, items):
        self.submits += 1
        if self.mode == "timeout_then_recover" and self.submits == 1:
            self._customer = customer
            self._items = items
            raise ApiTimeout("simulated submit timeout")
        return self.created

    def list_orders(self):
        if self.mode == "timeout_then_recover":
            return [{"id": "recovered-1",
                     "first_name": self._customer["first_name"],
                     "created_at": int(time.time()),
                     "ready_at": int(time.time()) + 300,
                     "status": "ordered"}]
        return []

    def get_order(self, order_id):
        return {"id": order_id,
                "customer": self._customer,
                "items": self._items}

    def check_street(self, street):
        return {"street": street, "deliverable": True}


@pytest.mark.parametrize("path", TRANSCRIPTS, ids=lambda p: p.stem)
def test_golden_transcript(path):
    transcript = json.loads(path.read_text())
    stub = StubModel(transcript["turns"])
    client = ScriptedClient(transcript["fake"])
    config = AgentConfig(url="http://unused", key="unused",
                         model="stub", lang="de")
    menu = Menu(json.loads((FIXTURES / "menu.json").read_text()))
    session = Session(order=Order(), menu=menu,
                      messages=[{"role": "system", "content": "stub"}])
    agent = Agent(config, client, chat_fn=stub)

    calls, error_codes = [], []

    def emit(event):
        if event["type"] == "tool_call":
            calls.append(event["tool"])
        if event["type"] == "tool_result" and "error" in event["result"]:
            error_codes.append(event["result"]["error"]["code"])

    for turn in transcript["turns"]:
        stub.next_turn()
        final = agent.run_turn(session, turn["user"], emit)
        assert final == turn["script"][-1]["say"]

    expect = transcript["expect"]
    assert session.order.state.value == expect["state"]
    assert calls == expect["calls"]
    assert error_codes == expect["error_codes"]
    actual_items = [{"type": i.type, "code": i.code, "qty": i.qty}
                    for i in session.order.items]
    assert actual_items == expect["items"]
    if "order_id" in expect:
        assert session.order.result["order_id"] == expect["order_id"]
    if expect["state"] == "SUBMITTED":
        assert session.order.result["order_id"]


def test_five_transcripts_exist():
    assert len(TRANSCRIPTS) == 5


def test_gateway_timeout_apology():
    """Gateway timeout: one retry, then abort the turn with an apology."""
    attempts = []

    def flaky(messages, tool_schemas):
        attempts.append(1)
        from core.agent import GatewayError
        raise GatewayError("gateway timed out twice")

    config = AgentConfig(url="http://unused", key="unused",
                         model="stub", lang="en")
    menu = Menu(json.loads((FIXTURES / "menu.json").read_text()))
    session = Session(order=Order(), menu=menu,
                      messages=[{"role": "system", "content": "stub"}])
    agent = Agent(config, ScriptedClient("ok"), chat_fn=flaky)
    text = agent.run_turn(session, "hello")
    assert "sorry" in text.lower()
    assert session.order.state.value == "EMPTY"  # turn aborted cleanly

 succeeded in 1001ms:
SPEC.md:34:## What done looks like
SPEC.md:40:under the pizzeria they chose — with the right customer, the right items, the
SPEC.md:45:1. `POST /pizzerias/{id}/orders` returned an order id.
SPEC.md:46:2. Reading that pizzeria's orders back shows the order, and it is visible on
SPEC.md:47:   that pizzeria's dashboard.
SPEC.md:49:4. The items and quantities are the ones that were read back and confirmed —
SPEC.md:52:Nothing else counts as done. A green test suite, a clean architecture, a
SPEC.md:59:- The order landed under a **different pizzeria** than the one the customer
SPEC.md:64:- The order was submitted **without the customer confirming** the read-back.
SPEC.md:66:Every rule below — the state machine, the revision-bound confirmation, the ban
SPEC.md:84:does the one thing it is genuinely good at — turning messy human speech into
SPEC.md:86:and never reaches the kitchen without a confirmed read-back.
SPEC.md:88:**Core belief:** a language model is a great waiter and a terrible order pad.
SPEC.md:123:- **Speech on the web transport**, served by a self-hosted CPU-only speech
SPEC.md:125:- **Several pizzerias.** The customer chooses which one they are ordering
SPEC.md:128:- **Languages:** German and English. The agent answers in the language the
SPEC.md:133:  comes to before confirming.
SPEC.md:143:- Accounts, auth, sessions surviving a process restart.
SPEC.md:159:| `LITELLM_PIZZA_URL` | OpenAI-compatible gateway base URL (`/chat/completions` appended) |
SPEC.md:160:| `LITELLM_PIZZA_KEY` | Bearer token for the gateway |
SPEC.md:165:| `PIZZERIA_ID` | UUID of the pizzeria preselected on first load |
SPEC.md:166:| `PIZZERIA_LANG` | Initial language, `de` or `en`: the greeting, the CLI, and the web UI before the customer switches |
SPEC.md:167:| `APP_VERSION` | Release version, `x.y.z`, shown in the footer |
SPEC.md:168:| `SPEECH_URL` | Base URL of the self-hosted speech service (optional) |
SPEC.md:179:  half-configured. `SPEECH_*` are the exception: absent means the speech
SPEC.md:193:| `GET /pizzerias` | `X-API-Key` | list of pizzerias with `id`, `name` |
SPEC.md:194:| `GET /pizzerias/{id}/orders` | `X-API-Key` | that pizzeria's orders; used by timeout recovery |
SPEC.md:195:| `POST /pizzerias/{id}/orders` | `X-API-Key` | places the order |
SPEC.md:211:- Dashboard of a pizzeria: `{PIZZASIM_URL}/dashboard/pizzerias/{id}`
SPEC.md:218:  a server key, not a pizzeria id.
SPEC.md:219:- Customers are unique per pizzeria **by first name**. An unknown name
SPEC.md:221:  input must therefore confirm the name explicitly.
SPEC.md:232:  single string (identical in DE and EN; there are no per-language names).
SPEC.md:249:  `GET /pizzerias/{id}/orders/{order_id}` (auth: `X-API-Key`) returns the
SPEC.md:285:   "helpfully" confirm on the model's behalf.
SPEC.md:287:   confirmation applies to the basket that was read back, not to a later one.
SPEC.md:288:3. `CONFIRMED` is reachable only via `confirm_order`, which is only legal
SPEC.md:290:   revision counter; `confirm_order` must name it.
SPEC.md:293:   fetched this session.
SPEC.md:294:6. A basket never crosses a tenant boundary. Changing pizzeria starts a fresh
SPEC.md:310:| `confirm_order` | `revision` | state `CONFIRMED`, or error if stale |
SPEC.md:325:  session's menu snapshot. The model never does arithmetic on prices; the
SPEC.md:339:- Greet first, in the session language, and offer help — one sentence, not a
SPEC.md:342:**Language authority — one rule.** The session language starts as
SPEC.md:344:header switch changes the session language: UI chrome, the greeting of a
SPEC.md:345:fresh conversation, and the speech hint (STT language, TTS output). For the
SPEC.md:346:agent's replies, per-turn mirroring wins: it answers in the language of the
SPEC.md:347:customer's latest message, even when that differs from the session language.
SPEC.md:352:  session. Price questions are normal questions, and so is "what does my
SPEC.md:363:- On error, explain in plain language what happened and what the options are.
SPEC.md:382:> confirm → order id and wait time.
SPEC.md:389:- **The pizzeria being ordered from, by name**, prominent and always visible.
SPEC.md:390:- **A selector to change pizzeria, filled from the API and from nowhere
SPEC.md:391:  else.** The list comes from `GET /pizzerias` at load time. No hardcoded
SPEC.md:396:  conversation for that pizzeria.
SPEC.md:397:- **A link to that pizzeria's dashboard**
SPEC.md:398:  (`{PIZZASIM_URL}/dashboard/pizzerias/{id}`), opening in a new tab. Without
SPEC.md:402:  and to speech in both directions.
SPEC.md:403:- **Start over**, clearing the session and the basket.
SPEC.md:407:- **The running version**, `x.y.z`, from `APP_VERSION`, raised on every
SPEC.md:410:- **The full pizzeria UUID**, selectable, for pasting into API calls.
SPEC.md:411:- **Connection state** for the ordering API and the model gateway.
SPEC.md:417:a rendered assistant reply or a rendered error.** Never a silent failure,
SPEC.md:422:  returned — visually distinct from the assistant's words. A stream whose tool
SPEC.md:425:- If the stream ends without a final assistant message, the UI says so.
SPEC.md:427:  happened and offers to resend.
SPEC.md:428:- Errors in the customer's language, in plain words. No status codes, no
SPEC.md:435:- The read-back is visually distinct and carries an explicit confirm control.
SPEC.md:447:**self-hosted speech service**: CPU-only, in its own container, reached over
SPEC.md:452:| STT | `POST {SPEECH_URL}/v1/audio/transcriptions` | multipart audio + model + language |
SPEC.md:453:| TTS | `POST {SPEECH_URL}/v1/audio/speech` | JSON: model, voice, input text → audio |
SPEC.md:455:- **The speech service is the only speech path.** No external speech
SPEC.md:456:  provider, no hosted realtime framework, no audio through the LLM gateway —
SPEC.md:457:  that gateway carries chat completions only.
SPEC.md:462:- **The browser speech APIs are forbidden.** `SpeechRecognition` and
SPEC.md:463:  `speechSynthesis` tied the previous implementation to a single browser
SPEC.md:466:- **Nothing about the speech stack is written into source.** Base URL, models
SPEC.md:468:  language sent with STT/TTS requests is the session language (see
SPEC.md:477:  applied only to the final assistant message.
SPEC.md:480:  usable. A speech failure is never an order failure.
SPEC.md:496:| Gateway timeout | one retry, then abort turn | plain apology, offer to resend |
SPEC.md:499:| Runtime pizzeria selection invalid/gone | session error, refresh the selector; process stays up | "that pizzeria isn't available right now" |
SPEC.md:502:| Timeout on submit | mark `UNKNOWN`; shortlist via `GET /pizzerias/{id}/orders`, verify items via `GET /pizzerias/{id}/orders/{order_id}` before any retry | as above |
SPEC.md:507:| Speech service down | hide speech controls | text UI unaffected |
SPEC.md:510:order. Recovery: shortlist candidates on the pizzeria's order list, then
SPEC.md:511:verify the candidate's items via `GET /pizzerias/{id}/orders/{order_id}` —
SPEC.md:523:   confirmation, mis-parses quantities, duplicates items on overlapping
SPEC.md:527:3. **Hardcoded pizzeria UUID or hardcoded menu fallback.** Both send orders to
SPEC.md:529:   fallback entry in the pizzeria selector.
SPEC.md:530:4. **A system prompt that forbids confirmation** ("never ask if they're sure,
SPEC.md:557:  stream ending without a final message, the gateway unreachable — each must
SPEC.md:560:  touches the real API. Full conversation, submit, then read the pizzeria's
SPEC.md:561:  orders back — presence via `GET /pizzerias/{id}/orders`, customer, items
SPEC.md:562:  and quantities via `GET /pizzerias/{id}/orders/{order_id}` (the list
SPEC.md:564:  points under *What done looks like*. If this fails, the product does not
SPEC.md:655:fails the rubric is not done.
SPEC.md:662:feedback arrives until you are done — every decision inside these constraints
SPEC.md:674:   page in a browser, switched pizzeria, asked a price question, placed an
SPEC.md:675:   order through the page, and seen it on that pizzeria's dashboard — not
SPEC.md:677:5. **Speech.** Wire the speech service into the web UI, spoken-answer policy,
SPEC.md:678:   and the degraded no-speech path.
SPEC.md:704:│   ├── speech.py            ← speech service client
SPEC.md:705:│   └── static/              ← web UI incl. speech input/output
SPEC.md:727:| Menu | Fetched live per session, no fallback list |
SPEC.md:732:| Language | Session language from `PIZZERIA_LANG`, switchable in the web header; per-turn mirroring wins for replies |
SPEC.md:734:| Speech | Self-hosted container, OpenAI-compatible HTTP; no vendor, no browser speech API |
SPEC.md:743:| Errors | Typed in code, plain language to the customer |
SPEC.md:750:| Definition of done | The judge approved, not "it runs" |
SPEC.md:756:- Multi-turn memory across sessions ("the usual").
SPEC.md:757:- Additional languages beyond DE + EN.
PLAN.md:8:pizzerias, prices and code-owned totals, the full web-channel contract
PLAN.md:9:(header/footer/basket/confirm control/answer invariant), APP_VERSION,
PLAN.md:10:per-session language, and a mandatory offline browser E2E suite.
PLAN.md:13:by code, the model only speaks. What moves: everything tenant-, language-
PLAN.md:14:and menu-scoped moves from process-global into a per-session `Session`
PLAN.md:40:| 2. Core-owned session factory, immutable tenant | "Session model v2" |
PLAN.md:51:| `channels/web.py` | `APP_VERSION` (required) |
PLAN.md:52:| `channels/speech.py` | `SPEECH_URL`, `SPEECH_STT_MODEL`, `SPEECH_TTS_MODEL`, `SPEECH_TTS_VOICE` (all optional; absence disables speech) |
PLAN.md:55:exit before the first turn naming variable and file. `APP_VERSION` must
PLAN.md:58:`{PIZZASIM_URL}/dashboard/pizzerias/{id}`, docs
PLAN.md:63:`Session` (core/agent.py): `{id, pizzeria_id, pizzeria_name, client,
PLAN.md:64:menu, lang, order, messages}` — pizzeria fields and client are set at
PLAN.md:65:creation and never mutated (a tenant switch is a NEW session; invariant 6).
PLAN.md:67:Core factory `create_session(config, base, pizzeria_id, lang)`:
PLAN.md:69:1. `base.list_pizzerias()` (tenant-free call) → id must be present, else
PLAN.md:70:   typed `NotFoundError` → channel renders "that pizzeria isn't available
PLAN.md:71:   right now" (session error; process stays up, per the new error row).
PLAN.md:72:2. Build a tenant-bound `PizzaSim` client for `pizzeria_id`.
PLAN.md:73:3. Fetch the fresh, immutable menu snapshot for this session (invariant 5).
PLAN.md:74:4. Render `prompts/system.{lang}.md` with the pizzeria name.
PLAN.md:77:env; `GET /pizzerias` must contain the preselected `PIZZERIA_ID` (else the
PLAN.md:79:health check ("We're not taking orders right now" on failure). The
PLAN.md:80:preselection is only the default for new sessions.
PLAN.md:82:CLI: one session from `PIZZERIA_ID` + `PIZZERIA_LANG`; no switching (per
PLAN.md:83:SPEC's language-authority rule and header-only selector).
PLAN.md:88:`PIZZERIA_LANG`; the web header switch calls `set_language(session, lang)`
PLAN.md:90:language — same policy text, history preserved. Apologies and the STT/TTS
PLAN.md:91:language read `session.lang`. Reply language stays per-turn mirroring by
PLAN.md:94:by the session language.
PLAN.md:98:- `Menu` keeps `price` per (type, code); `as_tool_result()` returns
PLAN.md:100:- `Item` gains `unit_price`, copied at add time from the session menu
PLAN.md:101:  snapshot (prices are stable for the session, like the menu itself).
PLAN.md:102:- `Order.snapshot()` gains per line `unit_price`, `line_total`
PLAN.md:103:  (= qty × unit_price) and top-level `basket_total` — computed in
PLAN.md:111:  `price`/`basket_total` from tool results verbatim.
PLAN.md:120:  unit_price, line_total}], basket_total, customer, read_back_done}`
PLAN.md:129:- Click → `POST /confirm {session_id, revision}` → **one core method**
PLAN.md:130:  `Agent.confirm_and_submit(session, revision, emit)`:
PLAN.md:131:  1. `tools.dispatch("confirm_order", {revision})` — stale revision or
PLAN.md:136:  3. Both calls are appended to `session.messages` as a synthetic
PLAN.md:137:     assistant `tool_calls` message + `tool` results (OpenAI format), so
PLAN.md:142:  reachable only via `confirm_order(revision)`; the transport forwards two
PLAN.md:145:  `confirm_order` + `submit_order` itself. Both paths converge on dispatch.
PLAN.md:151:- `GET /config` → `{version, speech, lang_default, pizzerias:
PLAN.md:153:  `pizzerias: null` when `GET /pizzerias` failed at request time — the UI
PLAN.md:155:- `POST /session {pizzeria_id?, lang?}` → creates a Session (defaults:
PLAN.md:156:  preselected id, `PIZZERIA_LANG`), returns `{session_id, pizzeria_id,
PLAN.md:157:  pizzeria_name, lang}`. Invalid id → 409 with the session-error text.
PLAN.md:158:- `POST /chat {session_id, text|null}` → NDJSON stream (unchanged
PLAN.md:159:  protocol; `text: null` = greeting turn). 404 for unknown session (the
PLAN.md:160:  UI then creates a fresh one). Per-session lock → 409 on overlap.
PLAN.md:161:- `POST /confirm {session_id, revision}` → NDJSON stream (same event
PLAN.md:162:  shapes) via `confirm_and_submit`.
PLAN.md:163:- `POST /language {session_id, lang}` → `{lang}`; core `set_language`.
PLAN.md:164:- `GET /health` → `{api: "ok"|"down", gateway: "ok"|"down"|"unknown"}` —
PLAN.md:165:  `api` from a live `GET /pizzerias` with 3s timeout; `gateway` from the
PLAN.md:168:- Speech proxy endpoints move to `channels/speech.py` (deliverable):
PLAN.md:174:- **Header:** pizzeria name (prominent, from the session), selector
PLAN.md:175:  (name + first 8 UUID chars, from `/config.pizzerias`), dashboard link
PLAN.md:176:  (`dashboard_base` + id, `target="_blank"`), language switch DE/EN,
PLAN.md:179:  session (fresh id — invariant 6 by construction), render the greeting
PLAN.md:182:  badges from `/health`, docs link.
PLAN.md:184:  `done` events: lines with qty × name, `line_total`, `basket_total`;
PLAN.md:186:  control on the page can modify or resubmit (confirm button removed,
PLAN.md:187:  input stays usable for a new conversation via Start over / new session).
PLAN.md:189:  block + confirm button bound to the streamed revision.
PLAN.md:194:  - `done` without a preceding `assistant` event in the turn → rendered
PLAN.md:195:    notice "the agent did not answer — resend?";
PLAN.md:197:    (error, timeout, connection lost) + a resend button that re-posts the
PLAN.md:199:  - all notices in the session language, plain words.
PLAN.md:210:| Runtime pizzeria selection invalid | `create_session` NotFoundError → 409 → UI notice; process stays up |
PLAN.md:211:| Pizzeria list fetch fails | `/config.pizzerias = null` → "list unavailable", no selector, no fallback entry |
PLAN.md:212:| Stream ends without final message | UI-side detection via `done`-without-`assistant` → notice + resend |
PLAN.md:213:| Gateway unreachable | existing retry-once → apology (now also an `assistant` event, v1 fix) + UI resend offer |
PLAN.md:220:- **Unit/tool (extend v1's 71):** prices copied at add time; `line_total`
PLAN.md:221:  / `basket_total` incl. Decimal rounding; snapshot shape; session factory
PLAN.md:222:  (valid id, unknown id, list failure); `set_language` re-render;
PLAN.md:223:  `confirm_and_submit` (happy, stale revision, submit timeout path);
PLAN.md:224:  `APP_VERSION` validation.
PLAN.md:228:  in-process **stub PizzaSim** (fixtures: two pizzerias, menu with prices)
PLAN.md:229:  and **stub gateway** (scripted tool-calling model) served locally;
PLAN.md:233:     add items → name → read-back panel → **confirm click** → submitted
PLAN.md:235:  2. pizzeria switch: selector → fresh conversation, header + footer UUID
PLAN.md:239:  4. failure — gateway unreachable: stub gateway refuses → apology text
PLAN.md:240:     rendered + resend control;
PLAN.md:242:     UI notice + resend control.
PLAN.md:246:- **Speech:** manual checklist (README) unchanged + STT language follows
PLAN.md:247:  the session language.
PLAN.md:251:New: `channels/speech.py`, `tests/test_web_e2e.py`. Rebuilt:
PLAN.md:254:verbatim-price rule), `README.md`, `.env.example` (+`APP_VERSION`),
PLAN.md:259:1. **Prices & totals in core.** Menu price, `Item.unit_price`,
PLAN.md:262:2. **Session factory & tenancy.** Session v2 fields, `create_session`,
PLAN.md:263:   client per session, agent uses `session.client`, startup preselection
PLAN.md:265:3. **Language authority.** `Session.lang`, `set_language` re-render,
PLAN.md:266:   apologies/STT via session.lang. ☐ switch test ☐ no process-global lang.
PLAN.md:267:4. **Confirm path.** `Agent.confirm_and_submit` + synthetic messages.
PLAN.md:270:5. **Web API surface.** /config, /session, /confirm, /language, /health,
PLAN.md:271:   session 404/409 semantics, speech extraction to `channels/speech.py`.
PLAN.md:273:6. **Web UI: frame.** Header (name, selector, dashboard link, language,
PLAN.md:274:   start over), footer (version, UUID, health badges, docs), i18n chrome.
PLAN.md:275:   ☐ switch/start-over create fresh session + abort in-flight stream.
PLAN.md:277:   confirm button, working indicator, done-without-assistant notice,
PLAN.md:278:   error/resend paths, submitted lock.
PLAN.md:279:   ☐ every notice in session language ☐ no discarded stream events.
PLAN.md:280:8. **Browser E2E suite.** Stub PizzaSim + stub gateway + Playwright;
PLAN.md:283:   channels + E2E + speech checklist), `.env.example`, `APP_VERSION`
channels/web.py:4:proxies the optional self-hosted speech service (STT/TTS). If SPEECH_URL is
channels/web.py:5:unset or the service doesn't answer at startup, speech endpoints return 404
channels/web.py:33:    """Config + probe for the self-hosted speech container. All-or-nothing:
channels/web.py:48:                print("speech service not answering — text-only mode",
channels/web.py:56:        client, pizzeria_name, _menu = startup(config)
channels/web.py:66:    app.state.pizzeria_name = pizzeria_name
channels/web.py:68:    app.state.sessions = {}
channels/web.py:69:    app.state.locks = {}  # one Lock per session: turns are serialized
channels/web.py:70:    app.state.speech = Speech()
channels/web.py:80:    # Contract per plan: speech flag + pizzeria display name. The customer
channels/web.py:81:    # must see which pizzeria they are ordering at.
channels/web.py:82:    return {"speech": app.state.speech.enabled,
channels/web.py:83:            "pizzeria": app.state.pizzeria_name}
channels/web.py:86:def _get_session(session_id: str) -> Session:
channels/web.py:87:    sessions = app.state.sessions
channels/web.py:88:    if session_id not in sessions:
channels/web.py:89:        # Fresh immutable menu snapshot per session (SPEC invariant 5).
channels/web.py:94:        sessions[session_id] = Session.create(
channels/web.py:95:            app.state.config, menu, app.state.pizzeria_name)
channels/web.py:96:    return sessions[session_id]
channels/web.py:101:    session_id = str(body.get("session_id") or "")
channels/web.py:102:    if not session_id:
channels/web.py:103:        raise HTTPException(422, "session_id required")
channels/web.py:107:    session = _get_session(session_id)
channels/web.py:108:    lock = app.state.locks.setdefault(session_id, threading.Lock())
channels/web.py:112:        # confirmation guarantees.
channels/web.py:119:            app.state.agent.run_turn(session, text, events.put)
channels/web.py:121:            events.put({"type": "done",
channels/web.py:122:                        "state": session.order.snapshot()})
channels/web.py:135:def _speech() -> Speech:
channels/web.py:136:    speech = app.state.speech
channels/web.py:137:    if not speech.enabled:
channels/web.py:138:        raise HTTPException(404, "speech is not available")
channels/web.py:139:    return speech
channels/web.py:142:@app.post("/speech/stt")
channels/web.py:144:    speech = _speech()
channels/web.py:147:    data = {"model": speech.stt_model,
channels/web.py:148:            "language": app.state.config.lang}  # STT hint only
channels/web.py:151:            f"{speech.url.rstrip('/')}/v1/audio/transcriptions",
channels/web.py:155:        raise HTTPException(502, "speech service unavailable")
channels/web.py:159:@app.post("/speech/tts")
channels/web.py:161:    speech = _speech()
channels/web.py:167:            f"{speech.url.rstrip('/')}/v1/audio/speech",
channels/web.py:168:            json={"model": speech.tts_model, "voice": speech.voice,
channels/web.py:173:        raise HTTPException(502, "speech service unavailable")
channels/static/style.css:15:.assistant { background: #fff; border: 1px solid #e5ded2; }
core/order.py:64:            "read_back_done": self.read_back_revision == self.revision,
core/state.py:33:    # recovery correlation belongs to the basket that was confirmed then,
core/state.py:103:def confirm(order: Order, revision: int) -> None:
core/state.py:108:                "invalid_state", "The order is already confirmed."
core/state.py:112:            "The order isn't complete yet, so it can't be confirmed.",
core/state.py:135:            "The order hasn't been confirmed yet."
channels/static/app.js:2:   MediaRecorder + the server's speech proxy — no browser speech APIs. */
channels/static/app.js:15:const sessionId = crypto.randomUUID
channels/static/app.js:19:let speechEnabled = false;
channels/static/app.js:54:      body: JSON.stringify({ session_id: sessionId, text }),
channels/static/app.js:61:      const { done, value } = await reader.read();
channels/static/app.js:62:      if (done) break;
channels/static/app.js:69:        if (ev.type === "tool_call" || ev.type === "tool_result") {
channels/static/app.js:75:        } else if (ev.type === "assistant") {
channels/static/app.js:77:          add("assistant", ev.text);
channels/static/app.js:89:  if (finalText && speechEnabled && ttsToggle.checked) speak(finalText);
channels/static/app.js:100:/* --- speech: push-to-talk, server-proxied ------------------------------ */
channels/static/app.js:115:    body.append("audio", blob, "speech.webm");
channels/static/app.js:117:      const res = await fetch("/speech/stt", { method: "POST", body });
channels/static/app.js:138:    const res = await fetch("/speech/tts", {
channels/static/app.js:155:    if (cfg.pizzeria) {
channels/static/app.js:156:      document.getElementById("title").textContent = cfg.pizzeria;
channels/static/app.js:157:      document.title = cfg.pizzeria;
channels/static/app.js:161:    speechEnabled = cfg.speech;    // unset SPEECH_URL → nothing rendered
channels/static/app.js:162:    if (speechEnabled) {
core/agent.py:40:    lang: str  # PIZZERIA_LANG: greeting language = pizzeria country
core/agent.py:58:def system_prompt(lang: str, pizzeria_name: str) -> str:
core/agent.py:60:    return text.replace("{pizzeria_name}", pizzeria_name)
core/agent.py:74:               pizzeria_name: str) -> "Session":
core/agent.py:80:                                                pizzeria_name)}],
core/agent.py:84:def log_event(session: Session, event: dict) -> None:
core/agent.py:87:    record = {"ts": round(time.time(), 3), "session": session.id, **event}
core/agent.py:88:    with (LOG_DIR / f"agent-{session.id}.jsonl").open("a") as fh:
core/agent.py:97:        # chat_fn(messages, tools) -> assistant message dict; injectable so
core/agent.py:99:        self._chat_fn = chat_fn or self._gateway_chat
core/agent.py:101:    def _gateway_chat(self, messages: list[dict],
core/agent.py:122:                raise GatewayError(f"gateway request failed: "
core/agent.py:124:        raise GatewayError("gateway timed out twice") from last_exc
core/agent.py:126:    def run_turn(self, session: Session, user_text: str | None,
core/agent.py:128:        """One customer turn: returns the assistant's final text. Every
core/agent.py:133:            log_event(session, payload)
core/agent.py:137:            session.messages.append({"role": "user", "content": user_text})
core/agent.py:142:                message = self._chat_fn(session.messages,
core/agent.py:147:                session.messages.append({"role": "assistant",
core/agent.py:149:                event({"type": "assistant", "text": apology})
core/agent.py:155:                session.messages.append({"role": "assistant",
core/agent.py:157:                event({"type": "assistant", "text": text})
core/agent.py:160:            session.messages.append({
core/agent.py:161:                "role": "assistant",
core/agent.py:172:                result = tools.dispatch(session.order, session.menu,
core/agent.py:174:                event({"type": "tool_result", "tool": name,
core/agent.py:177:                       "state": session.order.state.value,
core/agent.py:178:                       "revision": session.order.revision})
core/agent.py:179:                session.messages.append({
core/agent.py:187:        session.messages.append({"role": "assistant", "content": apology})
core/agent.py:188:        event({"type": "assistant", "text": apology})
core/agent.py:193:    """The one startup sequence (PLAN): env → pizzeria check → menu.
core/agent.py:196:    pizzeria_name = client.pizzeria_name()
core/agent.py:198:    return client, pizzeria_name, menu
core/tools.py:66:                    "the customer before asking for confirmation.",
core/tools.py:68:    {"name": "confirm_order",
core/tools.py:76:     "description": "Send the confirmed order to the kitchen. Only legal "
core/tools.py:77:                    "after confirm_order.",
core/tools.py:133:        return {"menu": menu.as_tool_result(), "snapshot": order.snapshot()}
core/tools.py:172:    if name == "confirm_order":
core/tools.py:177:        state.confirm(order, revision)
channels/cli.py:22:        elif kind == "tool_result":
channels/cli.py:38:        client, pizzeria_name, menu = startup(config)
channels/cli.py:48:    session = Session.create(config, menu, pizzeria_name)
channels/cli.py:51:    print(f"[{pizzeria_name} — type your order, Ctrl-D to hang up]")
channels/cli.py:52:    print(agent.run_turn(session, None, emit))  # agent greets first
channels/cli.py:61:        print(agent.run_turn(session, text, emit))
core/pizzasim.py:88:    def __init__(self, base_url: str, api_key: str, pizzeria_id: str,
core/pizzasim.py:90:        self.pizzeria_id = pizzeria_id
core/pizzasim.py:119:    def list_pizzerias(self) -> list[dict]:
core/pizzasim.py:120:        return self._request("GET", "/pizzerias")["pizzerias"]
core/pizzasim.py:122:    def pizzeria_name(self) -> str:
core/pizzasim.py:124:        404-pizzeria case — the process must refuse to start."""
core/pizzasim.py:125:        for pizzeria in self.list_pizzerias():
core/pizzasim.py:126:            if pizzeria["id"] == self.pizzeria_id:
core/pizzasim.py:127:                return pizzeria["name"]
core/pizzasim.py:129:            f"pizzeria {self.pizzeria_id} not found on the PizzaSim server"
core/pizzasim.py:134:            "GET", f"/pizzerias/{self.pizzeria_id}/orders"
core/pizzasim.py:141:            "GET", f"/pizzerias/{self.pizzeria_id}/orders/{order_id}"
core/pizzasim.py:148:            f"/pizzerias/{self.pizzeria_id}/orders",
core/menu.py:2:candidate suggestions. One snapshot per session (SPEC invariant 5)."""
core/menu.py:24:    def as_tool_result(self) -> dict:
tests/test_transcripts.py:86:    session = Session(order=Order(), menu=menu,
tests/test_transcripts.py:95:        if event["type"] == "tool_result" and "error" in event["result"]:
tests/test_transcripts.py:100:        final = agent.run_turn(session, turn["user"], emit)
tests/test_transcripts.py:104:    assert session.order.state.value == expect["state"]
tests/test_transcripts.py:108:                    for i in session.order.items]
tests/test_transcripts.py:111:        assert session.order.result["order_id"] == expect["order_id"]
tests/test_transcripts.py:113:        assert session.order.result["order_id"]
tests/test_transcripts.py:120:def test_gateway_timeout_apology():
tests/test_transcripts.py:127:        raise GatewayError("gateway timed out twice")
tests/test_transcripts.py:132:    session = Session(order=Order(), menu=menu,
tests/test_transcripts.py:135:    text = agent.run_turn(session, "hello")
tests/test_transcripts.py:137:    assert session.order.state.value == "EMPTY"  # turn aborted cleanly
tests/test_tools.py:114:def test_pizzeria_name_startup_check():
tests/test_tools.py:115:    payload = fixture("pizzerias.json")
tests/test_tools.py:117:                    payload["pizzerias"][0]["id"],
tests/test_tools.py:119:    assert good.pizzeria_name() == payload["pizzerias"][0]["name"]
tests/test_tools.py:122:        bad.pizzeria_name()
tests/test_tools.py:179:def confirmed_order(menu, fake):
tests/test_tools.py:182:    tools.dispatch(order, menu, fake, "confirm_order",
tests/test_tools.py:199:    assert snap["customer"] is None and snap["read_back_done"] is False
tests/test_tools.py:255:    order = confirmed_order(menu, fake)
tests/test_tools.py:263:def test_submit_outside_confirmed_is_tool_error(menu, fake):
tests/test_tools.py:264:    """Invariant 1: no helpful auto-confirmation."""
tests/test_tools.py:278:    order = confirmed_order(menu, fake)
tests/test_tools.py:304:    order = confirmed_order(menu, fake)
tests/test_tools.py:323:    """Timeout, then the customer changes the basket and reconfirms: the
tests/test_tools.py:326:    order = confirmed_order(menu, fake)
tests/test_tools.py:337:    tools.dispatch(order, menu, fake, "confirm_order",
tests/test_tools.py:351:    order = confirmed_order(menu, fake)
tests/test_tools.py:366:    order = confirmed_order(menu, fake)
tests/test_tools.py:376:    order = confirmed_order(menu, fake)
tests/test_tools.py:386:    order = confirmed_order(menu, fake)
tests/test_tools.py:401:    tools.dispatch(order, menu, fake, "confirm_order",
tests/test_tools.py:425:# SPEC "What done looks like": full conversation, submit, then read the
tests/test_tools.py:426:# pizzeria's orders back and assert the order is there with the right
tests/test_tools.py:445:    result = tools.dispatch(order, menu, client, "confirm_order",
tests/test_tools.py:454:    # 2. reading the pizzeria's orders back shows the order
tests/transcripts/submit_timeout.json:14:       {"tool": "confirm_order", "args": {"revision": 2}},
tests/transcripts/submit_timeout.json:26:    "calls": ["add_items", "set_customer", "read_back", "confirm_order", "submit_order", "submit_order"],
tests/transcripts/unknown_item.json:23:       {"tool": "confirm_order", "args": {"revision": 2}},
tests/transcripts/unknown_item.json:30:    "calls": ["add_items", "add_items", "set_customer", "read_back", "confirm_order", "submit_order"],
tests/transcripts/happy_path.json:23:       {"tool": "confirm_order", "args": {"revision": 2}},
tests/transcripts/happy_path.json:30:    "calls": ["get_menu", "add_items", "set_customer", "read_back", "confirm_order", "submit_order"],
tests/transcripts/correction.json:23:       {"tool": "confirm_order", "args": {"revision": 3}},
tests/transcripts/correction.json:30:    "calls": ["add_items", "add_items", "set_customer", "read_back", "confirm_order", "submit_order"],
tests/transcripts/mind_change.json:15:       {"tool": "confirm_order", "args": {"revision": 2}},
tests/transcripts/mind_change.json:21:       {"tool": "confirm_order", "args": {"revision": 3}},
tests/transcripts/mind_change.json:28:    "calls": ["add_items", "set_customer", "read_back", "add_items", "confirm_order", "read_back", "confirm_order", "submit_order"],
tests/fixtures/pizzerias.json:1:{"pizzerias":[{"id":"e1efd4b4-7eb3-4b45-b024-344a8b0b602f","name":"Pizzeria Elena","is_demo":true,"protected":true,"created_at":1774358205},{"id":"38863a6f-ff41-4a57-b92d-424d01587302","name":"Pizzeria Giulia","is_demo":true,"protected":true,"created_at":1774358204},{"id":"8a2d1ab2-8690-4dca-bcee-a0bf97db151e","name":"Pizzeria Giovanni","is_demo":true,"protected":true,"created_at":1774358203},{"id":"86517183-e1a5-4bd7-b915-e0db8f8b2131","name":"Pizzeria Roberto","is_demo":true,"protected":true,"created_at":1774358202}]}
tests/test_state.py:26:    state.confirm(o, o.revision)
tests/test_state.py:49:    state.confirm(o, o.revision)
tests/test_state.py:73:    lambda o: state.confirm(o, o.revision),
tests/test_state.py:102:def test_confirm_illegal_states(st):
tests/test_state.py:105:        state.confirm(o, o.revision)
tests/test_state.py:109:def test_confirm_when_already_confirmed():
tests/test_state.py:112:        state.confirm(o, o.revision)
tests/test_state.py:117:def test_submit_outside_confirmed(st):
tests/test_state.py:134:def test_add_after_confirmed_demotes_to_ready():
tests/test_state.py:140:def test_remove_after_confirmed_demotes():
tests/test_state.py:146:def test_set_customer_after_confirmed_demotes():
tests/test_state.py:152:def test_confirmation_does_not_survive_demotion():
tests/test_state.py:153:    """A confirmation applies to the basket that was read back."""
tests/test_state.py:160:# --- invariant 3: confirm tied to read-back + revision --------------------
tests/test_state.py:162:def test_confirm_without_read_back():
tests/test_state.py:165:        state.confirm(o, o.revision)
tests/test_state.py:169:def test_confirm_with_stale_revision():
tests/test_state.py:175:        state.confirm(o, stale)
tests/test_state.py:179:def test_read_back_of_old_revision_does_not_allow_confirm():
tests/test_state.py:184:        state.confirm(o, o.revision)

codex
I’ve confirmed the repo state the plan is retrofitting from. Now I’m pinning the plan against the exact v3 contract language and rubric, because several risks here are omissions that would let an implementer technically “follow the plan” while still missing the spec.
exec
/bin/bash -lc "sed -n '260,340p' PLAN.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '520,760p' SPEC.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '320,520p' SPEC.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc 'rg -n "rubric|score|1-5|completeness|correctness|error_handling|simplicity|spec_compliance" SPEC.md PLAN.md reviews decisions -S' in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 498ms:
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

 succeeded in 550ms:
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

 succeeded in 617ms:
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
  orders back — presence via `GET /pizzerias/{id}/orders`, customer, items
  and quantities via `GET /pizzerias/{id}/orders/{order_id}` (the list
  endpoint carries no items and cannot verify them) — and assert the four
  points under *What done looks like*. If this fails, the product does not
  work, whatever else is green.
- **Speech**, manual: dictate an order, a name that needs correcting, a menu
  question — plus one run with `SPEECH_URL` unset, which must render a usable
  text-only UI and place an order normally.

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
| Totals | Computed in code from API prices; the model never does arithmetic |
| Language | Session language from `PIZZERIA_LANG`, switchable in the web header; per-turn mirroring wins for replies |
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

 succeeded in 599ms:
SPEC.md:593:  rubric so quality is measurable across rounds instead of a vibe.
SPEC.md:625:SCORES (1-5 each, 5 = best):
SPEC.md:626:completeness: N
SPEC.md:627:correctness: N
SPEC.md:628:error_handling: N
SPEC.md:629:simplicity: N
SPEC.md:630:spec_compliance: N
SPEC.md:637:  verdict line says approved but the scores miss that bar, **the numbers
SPEC.md:640:  the scores and the open issues. A valid outcome, not a failure.
SPEC.md:643:- Every reviewer stdout goes into `reviews/`, every round's scores into
SPEC.md:644:  `reviews/scores.md`, and `reviews/` is committed.
SPEC.md:655:fails the rubric is not done.
SPEC.md:715:├── reviews/                 ← one file per review round, plus scores.md
PLAN.md:287:code; implementation follows only after APPROVED under the SPEC rubric.
reviews/round4-impl.md:15:2. Judge: score against the fixed rubric.
reviews/round4-impl.md:23:Output MUST end with exactly this block (numbers 1-5, 5 best):
reviews/round4-impl.md:24:SCORES (1-5 each, 5 = best):
reviews/round4-impl.md:25:completeness: N
reviews/round4-impl.md:26:correctness: N
reviews/round4-impl.md:27:error_handling: N
reviews/round4-impl.md:28:simplicity: N
reviews/round4-impl.md:29:spec_compliance: N
reviews/round4-impl.md:37:Using `using-superpowers` first to load the required workflow, then I’ll inspect `SPEC.md`, `PLAN.md`, and the implementation files to review against the approved plan and rubric.
reviews/round4-impl.md:201:reviews/scores.md
reviews/round4-impl.md:207:Setting a short review workflow: read the source-of-truth docs first, inspect implementation areas against them, then produce findings and rubric scores.
reviews/round4-impl.md:210:  • Draft findings, rubric scores, and verdict
reviews/round4-impl.md:553:reviews/       One file per review round + scores.md.
reviews/round4-impl.md:756:2. Judge: score against the fixed rubric.
reviews/round4-impl.md:762:Judging guidance: score the plan that exists. If remaining concerns are implementation-detail-sized rather than plan-sized, they belong in the implementation review, not in a plan rejection.
reviews/round4-impl.md:764:Output MUST end with exactly this block (numbers 1-5, 5 best):
reviews/round4-impl.md:765:SCORES (1-5 each, 5 = best):
reviews/round4-impl.md:766:completeness: N
reviews/round4-impl.md:767:correctness: N
reviews/round4-impl.md:768:error_handling: N
reviews/round4-impl.md:769:simplicity: N
reviews/round4-impl.md:770:spec_compliance: N
reviews/round4-impl.md:778:I’m reviewing `SPEC.md`, `PLAN.md`, the prior round review, and the QA decision first. I’m using the `using-superpowers` skill to ensure the required workflow, then I’ll assess the plan strictly against the spec and rubric.
reviews/round4-impl.md:804:2. Judge: score against the fixed rubric.
reviews/round4-impl.md:810:Output MUST end with exactly this block (numbers 1-5, 5 best):
reviews/round4-impl.md:811:SCORES (1-5 each, 5 = best):
reviews/round4-impl.md:812:completeness: N
reviews/round4-impl.md:813:correctness: N
reviews/round4-impl.md:814:error_handling: N
reviews/round4-impl.md:815:simplicity: N
reviews/round4-impl.md:816:spec_compliance: N
reviews/round4-impl.md:824:Reviewing `SPEC.md` and `PLAN.md` against each other first, then I’ll score the plan strictly against the rubric and the round-1 carryover requirements.
reviews/round4-impl.md:1007:  • Draft findings, rubric scores, and verdict
reviews/round4-impl.md:3585:  `submit_attempted_at`), 422 mapping, snapshot completeness.
reviews/round4-impl.md:3999:    76	reviews/       One file per review round + scores.md.
reviews/round4-impl.md:4038:SCORES (1-5 each, 5 = best):
reviews/round4-impl.md:4039:completeness: 4
reviews/round4-impl.md:4040:correctness: 3
reviews/round4-impl.md:4041:error_handling: 4
reviews/round4-impl.md:4042:simplicity: 4
reviews/round4-impl.md:4043:spec_compliance: 3
reviews/round4-impl.md:4050:- `requirements.txt:1-5` diverges from the approved plan (`PLAN.md:79-84`), which called for pinned dependencies for reproducibility. `>=` constraints make this benchmark repo less deterministic across environments; pin exact versions.
reviews/round4-impl.md:4055:SCORES (1-5 each, 5 = best):
reviews/round4-impl.md:4056:completeness: 4
reviews/round4-impl.md:4057:correctness: 3
reviews/round4-impl.md:4058:error_handling: 4
reviews/round4-impl.md:4059:simplicity: 4
reviews/round4-impl.md:4060:spec_compliance: 3
reviews/round4-impl.md:4067:- `requirements.txt:1-5` diverges from the approved plan (`PLAN.md:79-84`), which called for pinned dependencies for reproducibility. `>=` constraints make this benchmark repo less deterministic across environments; pin exact versions.
reviews/round3-plan.md:15:2. Judge: score against the fixed rubric.
reviews/round3-plan.md:21:Judging guidance: score the plan that exists. If remaining concerns are implementation-detail-sized rather than plan-sized, they belong in the implementation review, not in a plan rejection.
reviews/round3-plan.md:23:Output MUST end with exactly this block (numbers 1-5, 5 best):
reviews/round3-plan.md:24:SCORES (1-5 each, 5 = best):
reviews/round3-plan.md:25:completeness: N
reviews/round3-plan.md:26:correctness: N
reviews/round3-plan.md:27:error_handling: N
reviews/round3-plan.md:28:simplicity: N
reviews/round3-plan.md:29:spec_compliance: N
reviews/round3-plan.md:37:I’m reviewing `SPEC.md`, `PLAN.md`, the prior round review, and the QA decision first. I’m using the `using-superpowers` skill to ensure the required workflow, then I’ll assess the plan strictly against the spec and rubric.
reviews/round3-plan.md:63:2. Judge: score against the fixed rubric.
reviews/round3-plan.md:69:Output MUST end with exactly this block (numbers 1-5, 5 best):
reviews/round3-plan.md:70:SCORES (1-5 each, 5 = best):
reviews/round3-plan.md:71:completeness: N
reviews/round3-plan.md:72:correctness: N
reviews/round3-plan.md:73:error_handling: N
reviews/round3-plan.md:74:simplicity: N
reviews/round3-plan.md:75:spec_compliance: N
reviews/round3-plan.md:83:Reviewing `SPEC.md` and `PLAN.md` against each other first, then I’ll score the plan strictly against the rubric and the round-1 carryover requirements.
reviews/round3-plan.md:728:reviews/       One file per review round + scores.md.
reviews/round3-plan.md:1153:  rubric below so that quality is measurable across rounds instead of a vibe.
reviews/round3-plan.md:1164:SCORES (1-5 each, 5 = best):
reviews/round3-plan.md:1165:completeness: N
reviews/round3-plan.md:1166:correctness: N
reviews/round3-plan.md:1167:error_handling: N
reviews/round3-plan.md:1168:simplicity: N
reviews/round3-plan.md:1169:spec_compliance: N
reviews/round3-plan.md:1176:  verdict line says approved but the scores miss that bar, **the numbers win**.
reviews/round3-plan.md:1178:  scores and the open issues. That is a valid outcome, not a failure.
reviews/round3-plan.md:1181:- Every reviewer stdout goes into `reviews/`, every round's scores get appended
reviews/round3-plan.md:1182:  to `reviews/scores.md`, and `reviews/` is committed. The review trail belongs
reviews/round3-plan.md:1194:fails the rubric is not done.
reviews/round3-plan.md:1269:  `submit_attempted_at`), 422 mapping, snapshot completeness.
reviews/round3-plan.md:1685:    76	reviews/       One file per review round + scores.md.
reviews/round3-plan.md:1876:SCORES (1-5 each, 5 = best):
reviews/round3-plan.md:1877:completeness: 5
reviews/round3-plan.md:1878:correctness: 5
reviews/round3-plan.md:1879:error_handling: 5
reviews/round3-plan.md:1880:simplicity: 4
reviews/round3-plan.md:1881:spec_compliance: 5
reviews/round3-plan.md:1891:SCORES (1-5 each, 5 = best):
reviews/round3-plan.md:1892:completeness: 5
reviews/round3-plan.md:1893:correctness: 5
reviews/round3-plan.md:1894:error_handling: 5
reviews/round3-plan.md:1895:simplicity: 4
reviews/round3-plan.md:1896:spec_compliance: 5
reviews/scores.md:1:# Review scores
reviews/scores.md:5:completeness: 4
reviews/scores.md:6:correctness: 3
reviews/scores.md:7:error_handling: 4
reviews/scores.md:8:simplicity: 4
reviews/scores.md:9:spec_compliance: 3
reviews/scores.md:21:completeness: 3
reviews/scores.md:22:correctness: 3
reviews/scores.md:23:error_handling: 4
reviews/scores.md:24:simplicity: 4
reviews/scores.md:25:spec_compliance: 2
reviews/scores.md:39:completeness: 5
reviews/scores.md:40:correctness: 5
reviews/scores.md:41:error_handling: 5
reviews/scores.md:42:simplicity: 4
reviews/scores.md:43:spec_compliance: 5
reviews/scores.md:49:completeness: 4
reviews/scores.md:50:correctness: 3
reviews/scores.md:51:error_handling: 4
reviews/scores.md:52:simplicity: 4
reviews/scores.md:53:spec_compliance: 3
reviews/scores.md:65:completeness: 4
reviews/scores.md:66:correctness: 3
reviews/scores.md:67:error_handling: 3
reviews/scores.md:68:simplicity: 4
reviews/scores.md:69:spec_compliance: 3
reviews/scores.md:88:completeness: 5
reviews/scores.md:89:correctness: 5
reviews/scores.md:90:error_handling: 5
reviews/scores.md:91:simplicity: 4
reviews/scores.md:92:spec_compliance: 5
reviews/scores.md:98:completeness: 4
reviews/scores.md:99:correctness: 4
reviews/scores.md:100:error_handling: 3
reviews/scores.md:101:simplicity: 4
reviews/scores.md:102:spec_compliance: 3
reviews/scores.md:113:completeness: 5
reviews/scores.md:114:correctness: 5
reviews/scores.md:115:error_handling: 4
reviews/scores.md:116:simplicity: 5
reviews/scores.md:117:spec_compliance: 5
reviews/scores.md:132:patched SPEC.md is build-ready. (Document gate, rubric not applicable.)
reviews/round10-grill-verdict.md:127:The implementer claims: SPEC v1 was fully built and approved (reviews/round1..8, reviews/scores.md with plan approved 24/25 and implementation approved 24/25, hotfix approved 24/25); 71 deterministic tests exist and are self-consistent; core/ implements the state machine, tool dispatch, PizzaSim client with submit-timeout recovery; channels/cli.py and channels/web.py + static UI exist; decisions/qa.md records oracle decisions. Verify each claim against the files and git log. Report discrepancies bluntly.
reviews/round10-grill-verdict.md:324:./reviews/scores.md
reviews/round10-grill-verdict.md:352:* a133c09 Apply plan review round 1 findings, capture review + scores
reviews/round10-grill-verdict.md:368:/bin/bash -lc "sed -n '1,220p' reviews/scores.md" in /home/rob/bpm-pizza-vibecoding-solution
reviews/round10-grill-verdict.md:877:278:2. Judge: score against the fixed rubric.
reviews/round10-grill-verdict.md:881:499:2. Judge: score against the fixed rubric.
reviews/round10-grill-verdict.md:883:720:2. Judge: score against the fixed rubric.
reviews/round10-grill-verdict.md:885:768:2. Judge: score against the fixed rubric.
reviews/round10-grill-verdict.md:887:941:2. Judge: score against the fixed rubric.
reviews/round10-grill-verdict.md:889:1162:2. Judge: score against the fixed rubric.
reviews/round10-grill-verdict.md:895:1383:2. Judge: score against the fixed rubric.
reviews/round8-hotfix.md:22:SCORES (1-5 each, 5 = best):
reviews/round8-hotfix.md:23:completeness: N
reviews/round8-hotfix.md:24:correctness: N
reviews/round8-hotfix.md:25:error_handling: N
reviews/round8-hotfix.md:26:simplicity: N
reviews/round8-hotfix.md:27:spec_compliance: N
reviews/round8-hotfix.md:343:SCORES (1-5 each, 5 = best):
reviews/round8-hotfix.md:344:completeness: N
reviews/round8-hotfix.md:345:correctness: N
reviews/round8-hotfix.md:346:error_handling: N
reviews/round8-hotfix.md:347:simplicity: N
reviews/round8-hotfix.md:348:spec_compliance: N
reviews/round8-hotfix.md:753:SCORES (1-5 each, 5 = best):
reviews/round8-hotfix.md:754:completeness: N
reviews/round8-hotfix.md:755:correctness: N
reviews/round8-hotfix.md:756:error_handling: N
reviews/round8-hotfix.md:757:simplicity: N
reviews/round8-hotfix.md:758:spec_compliance: N
reviews/round8-hotfix.md:1136:    76	reviews/       One file per review round + scores.md.
reviews/round8-hotfix.md:1471:SCORES (1-5 each, 5 = best):
reviews/round8-hotfix.md:1472:completeness: 5
reviews/round8-hotfix.md:1473:correctness: 5
reviews/round8-hotfix.md:1474:error_handling: 4
reviews/round8-hotfix.md:1475:simplicity: 5
reviews/round8-hotfix.md:1476:spec_compliance: 5
reviews/round8-hotfix.md:1488:SCORES (1-5 each, 5 = best):
reviews/round8-hotfix.md:1489:completeness: 5
reviews/round8-hotfix.md:1490:correctness: 5
reviews/round8-hotfix.md:1491:error_handling: 4
reviews/round8-hotfix.md:1492:simplicity: 5
reviews/round8-hotfix.md:1493:spec_compliance: 5
reviews/round6-impl.md:15:2. Judge: score against the fixed rubric.
reviews/round6-impl.md:30:Judging guidance: this is the final allowed round. Score the implementation that exists against SPEC.md; remaining nice-to-haves that a maintainer would file as minor follow-ups do not belong in a rejection.
reviews/round6-impl.md:32:Output MUST end with exactly this block (numbers 1-5, 5 best):
reviews/round6-impl.md:33:SCORES (1-5 each, 5 = best):
reviews/round6-impl.md:34:completeness: N
reviews/round6-impl.md:35:correctness: N
reviews/round6-impl.md:36:error_handling: N
reviews/round6-impl.md:37:simplicity: N
reviews/round6-impl.md:38:spec_compliance: N
reviews/round6-impl.md:528:reviews/       One file per review round + scores.md.
reviews/round6-impl.md:727:./reviews/scores.md
reviews/round6-impl.md:3054:2. Judge: score against the fixed rubric.
reviews/round6-impl.md:3068:Output MUST end with exactly this block (numbers 1-5, 5 best):
reviews/round6-impl.md:3069:SCORES (1-5 each, 5 = best):
reviews/round6-impl.md:3070:completeness: N
reviews/round6-impl.md:3071:correctness: N
reviews/round6-impl.md:3072:error_handling: N
reviews/round6-impl.md:3073:simplicity: N
reviews/round6-impl.md:3074:spec_compliance: N
reviews/round6-impl.md:3256:Reviewing implementation against spec, approved plan, and round-1 required fixes before issuing findings and rubric scores.
reviews/round6-impl.md:3260:  • Produce findings ordered by severity and score against the rubric
reviews/round6-impl.md:3507:SCORES (1-5 each, 5 = best):
reviews/round6-impl.md:3508:completeness: 5
reviews/round6-impl.md:3509:correctness: 5
reviews/round6-impl.md:3510:error_handling: 5
reviews/round6-impl.md:3511:simplicity: 4
reviews/round6-impl.md:3512:spec_compliance: 5
reviews/round6-impl.md:3522:SCORES (1-5 each, 5 = best):
reviews/round6-impl.md:3523:completeness: 5
reviews/round6-impl.md:3524:correctness: 5
reviews/round6-impl.md:3525:error_handling: 5
reviews/round6-impl.md:3526:simplicity: 4
reviews/round6-impl.md:3527:spec_compliance: 5
reviews/round1-plan.md:15:2. Judge: score against the fixed rubric.
reviews/round1-plan.md:19:Output MUST end with exactly this block (numbers 1-5, 5 best):
reviews/round1-plan.md:20:SCORES (1-5 each, 5 = best):
reviews/round1-plan.md:21:completeness: N
reviews/round1-plan.md:22:correctness: N
reviews/round1-plan.md:23:error_handling: N
reviews/round1-plan.md:24:simplicity: N
reviews/round1-plan.md:25:spec_compliance: N
reviews/round1-plan.md:378:reviews/       One file per review round + scores.md.
reviews/round1-plan.md:629:I have the spec and most of the plan in view. I’m reading the remaining review-relevant instructions and the rest of `PLAN.md`, then I’ll score it against the spec with concrete gaps only.
reviews/round1-plan.md:642:  unknown → recovery-by-list, 422 mapping, snapshot completeness.
reviews/round1-plan.md:925:  rubric below so that quality is measurable across rounds instead of a vibe.
reviews/round1-plan.md:936:SCORES (1-5 each, 5 = best):
reviews/round1-plan.md:937:completeness: N
reviews/round1-plan.md:938:correctness: N
reviews/round1-plan.md:939:error_handling: N
reviews/round1-plan.md:940:simplicity: N
reviews/round1-plan.md:941:spec_compliance: N
reviews/round1-plan.md:948:  verdict line says approved but the scores miss that bar, **the numbers win**.
reviews/round1-plan.md:950:  scores and the open issues. That is a valid outcome, not a failure.
reviews/round1-plan.md:953:- Every reviewer stdout goes into `reviews/`, every round's scores get appended
reviews/round1-plan.md:954:  to `reviews/scores.md`, and `reviews/` is committed. The review trail belongs
reviews/round1-plan.md:966:fails the rubric is not done.
reviews/round1-plan.md:1382:    76	reviews/       One file per review round + scores.md.
reviews/round1-plan.md:1569:One last check: I’m verifying the deliverables section to make sure the plan’s file layout doesn’t quietly drift from the required tree. Then I’ll finalize the rubric judgment.
reviews/round1-plan.md:1596:   543	├── reviews/                 ← one file per review round, plus scores.md
reviews/round1-plan.md:1649:478:- Every reviewer stdout goes into `reviews/`, every round's scores get appended
reviews/round1-plan.md:1650:479:  to `reviews/scores.md`, and `reviews/` is committed. The review trail belongs
reviews/round1-plan.md:1654:543:├── reviews/                 ← one file per review round, plus scores.md
reviews/round1-plan.md:1669:SCORES (1-5 each, 5 = best):
reviews/round1-plan.md:1670:completeness: 4
reviews/round1-plan.md:1671:correctness: 3
reviews/round1-plan.md:1672:error_handling: 4
reviews/round1-plan.md:1673:simplicity: 4
reviews/round1-plan.md:1674:spec_compliance: 3
reviews/round1-plan.md:1697:SCORES (1-5 each, 5 = best):
reviews/round1-plan.md:1698:completeness: 4
reviews/round1-plan.md:1699:correctness: 3
reviews/round1-plan.md:1700:error_handling: 4
reviews/round1-plan.md:1701:simplicity: 4
reviews/round1-plan.md:1702:spec_compliance: 3
reviews/round9-audit-grill.md:16:The implementer claims: SPEC v1 was fully built and approved (reviews/round1..8, reviews/scores.md with plan approved 24/25 and implementation approved 24/25, hotfix approved 24/25); 71 deterministic tests exist and are self-consistent; core/ implements the state machine, tool dispatch, PizzaSim client with submit-timeout recovery; channels/cli.py and channels/web.py + static UI exist; decisions/qa.md records oracle decisions. Verify each claim against the files and git log. Report discrepancies bluntly.
reviews/round9-audit-grill.md:213:./reviews/scores.md
reviews/round9-audit-grill.md:241:* a133c09 Apply plan review round 1 findings, capture review + scores
reviews/round9-audit-grill.md:257:/bin/bash -lc "sed -n '1,220p' reviews/scores.md" in /home/rob/bpm-pizza-vibecoding-solution
reviews/round9-audit-grill.md:278:2. Judge: score against the fixed rubric.
reviews/round9-audit-grill.md:282:Output MUST end with exactly this block (numbers 1-5, 5 best):
reviews/round9-audit-grill.md:283:SCORES (1-5 each, 5 = best):
reviews/round9-audit-grill.md:284:completeness: N
reviews/round9-audit-grill.md:285:correctness: N
reviews/round9-audit-grill.md:286:error_handling: N
reviews/round9-audit-grill.md:287:simplicity: N
reviews/round9-audit-grill.md:288:spec_compliance: N
reviews/round9-audit-grill.md:499:2. Judge: score against the fixed rubric.
reviews/round9-audit-grill.md:505:Output MUST end with exactly this block (numbers 1-5, 5 best):
reviews/round9-audit-grill.md:506:SCORES (1-5 each, 5 = best):
reviews/round9-audit-grill.md:507:completeness: N
reviews/round9-audit-grill.md:508:correctness: N
reviews/round9-audit-grill.md:509:error_handling: N
reviews/round9-audit-grill.md:510:simplicity: N
reviews/round9-audit-grill.md:511:spec_compliance: N
reviews/round9-audit-grill.md:519:Reviewing `SPEC.md` and `PLAN.md` against each other first, then I’ll score the plan strictly against the rubric and the round-1 carryover requirements.
reviews/round9-audit-grill.md:720:2. Judge: score against the fixed rubric.
reviews/round9-audit-grill.md:726:Judging guidance: score the plan that exists. If remaining concerns are implementation-detail-sized rather than plan-sized, they belong in the implementation review, not in a plan rejection.
reviews/round9-audit-grill.md:728:Output MUST end with exactly this block (numbers 1-5, 5 best):
reviews/round9-audit-grill.md:729:SCORES (1-5 each, 5 = best):
reviews/round9-audit-grill.md:730:completeness: N
reviews/round9-audit-grill.md:731:correctness: N
reviews/round9-audit-grill.md:732:error_handling: N
reviews/round9-audit-grill.md:733:simplicity: N
reviews/round9-audit-grill.md:734:spec_compliance: N
reviews/round9-audit-grill.md:742:I’m reviewing `SPEC.md`, `PLAN.md`, the prior round review, and the QA decision first. I’m using the `using-superpowers` skill to ensure the required workflow, then I’ll assess the plan strictly against the spec and rubric.
reviews/round9-audit-grill.md:768:2. Judge: score against the fixed rubric.
reviews/round9-audit-grill.md:774:Output MUST end with exactly this block (numbers 1-5, 5 best):
reviews/round9-audit-grill.md:775:SCORES (1-5 each, 5 = best):
reviews/round9-audit-grill.md:776:completeness: N
reviews/round9-audit-grill.md:777:correctness: N
reviews/round9-audit-grill.md:778:error_handling: N
reviews/round9-audit-grill.md:779:simplicity: N
reviews/round9-audit-grill.md:780:spec_compliance: N
reviews/round9-audit-grill.md:788:Reviewing `SPEC.md` and `PLAN.md` against each other first, then I’ll score the plan strictly against the rubric and the round-1 carryover requirements.
reviews/round9-audit-grill.md:941:2. Judge: score against the fixed rubric.
reviews/round9-audit-grill.md:949:Output MUST end with exactly this block (numbers 1-5, 5 best):
reviews/round9-audit-grill.md:950:SCORES (1-5 each, 5 = best):
reviews/round9-audit-grill.md:951:completeness: N
reviews/round9-audit-grill.md:952:correctness: N
reviews/round9-audit-grill.md:953:error_handling: N
reviews/round9-audit-grill.md:954:simplicity: N
reviews/round9-audit-grill.md:955:spec_compliance: N
reviews/round9-audit-grill.md:963:Using `using-superpowers` first to load the required workflow, then I’ll inspect `SPEC.md`, `PLAN.md`, and the implementation files to review against the approved plan and rubric.
reviews/round9-audit-grill.md:1127:reviews/scores.md
reviews/round9-audit-grill.md:1133:Setting a short review workflow: read the source-of-truth docs first, inspect implementation areas against them, then produce findings and rubric scores.
reviews/round9-audit-grill.md:1136:  • Draft findings, rubric scores, and verdict
reviews/round9-audit-grill.md:1162:2. Judge: score against the fixed rubric.
reviews/round9-audit-grill.md:1176:Output MUST end with exactly this block (numbers 1-5, 5 best):
reviews/round9-audit-grill.md:1177:SCORES (1-5 each, 5 = best):
reviews/round9-audit-grill.md:1178:completeness: N
reviews/round9-audit-grill.md:1179:correctness: N
reviews/round9-audit-grill.md:1180:error_handling: N
reviews/round9-audit-grill.md:1181:simplicity: N
reviews/round9-audit-grill.md:1182:spec_compliance: N
reviews/round9-audit-grill.md:1364:Reviewing implementation against spec, approved plan, and round-1 required fixes before issuing findings and rubric scores.
reviews/round9-audit-grill.md:1383:2. Judge: score against the fixed rubric.
reviews/round9-audit-grill.md:1398:Judging guidance: this is the final allowed round. Score the implementation that exists against SPEC.md; remaining nice-to-haves that a maintainer would file as minor follow-ups do not belong in a rejection.
reviews/round9-audit-grill.md:1400:Output MUST end with exactly this block (numbers 1-5, 5 best):
reviews/round9-audit-grill.md:1401:SCORES (1-5 each, 5 = best):
reviews/round9-audit-grill.md:1402:completeness: N
reviews/round9-audit-grill.md:1403:correctness: N
reviews/round9-audit-grill.md:1404:error_handling: N
reviews/round9-audit-grill.md:1405:simplicity: N
reviews/round9-audit-grill.md:1406:spec_compliance: N
reviews/round9-audit-grill.md:1609:SCORES (1-5 each, 5 = best):
reviews/round9-audit-grill.md:1610:completeness: N
reviews/round9-audit-grill.md:1611:correctness: N
reviews/round9-audit-grill.md:1612:error_handling: N
reviews/round9-audit-grill.md:1613:simplicity: N
reviews/round9-audit-grill.md:1614:spec_compliance: N
reviews/round9-audit-grill.md:1832:SCORES (1-5 each, 5 = best):
reviews/round9-audit-grill.md:1833:completeness: N
reviews/round9-audit-grill.md:1834:correctness: N
reviews/round9-audit-grill.md:1835:error_handling: N
reviews/round9-audit-grill.md:1836:simplicity: N
reviews/round9-audit-grill.md:1837:spec_compliance: N
reviews/round9-audit-grill.md:2122:reviews/       One file per review round + scores.md.
reviews/round9-audit-grill.md:2336:# Review scores
reviews/round9-audit-grill.md:2340:completeness: 4
reviews/round9-audit-grill.md:2341:correctness: 3
reviews/round9-audit-grill.md:2342:error_handling: 4
reviews/round9-audit-grill.md:2343:simplicity: 4
reviews/round9-audit-grill.md:2344:spec_compliance: 3
reviews/round9-audit-grill.md:2356:completeness: 3
reviews/round9-audit-grill.md:2357:correctness: 3
reviews/round9-audit-grill.md:2358:error_handling: 4
reviews/round9-audit-grill.md:2359:simplicity: 4
reviews/round9-audit-grill.md:2360:spec_compliance: 2
reviews/round9-audit-grill.md:2374:completeness: 5
reviews/round9-audit-grill.md:2375:correctness: 5
reviews/round9-audit-grill.md:2376:error_handling: 5
reviews/round9-audit-grill.md:2377:simplicity: 4
reviews/round9-audit-grill.md:2378:spec_compliance: 5
reviews/round9-audit-grill.md:2384:completeness: 4
reviews/round9-audit-grill.md:2385:correctness: 3
reviews/round9-audit-grill.md:2386:error_handling: 4
reviews/round9-audit-grill.md:2387:simplicity: 4
reviews/round9-audit-grill.md:2388:spec_compliance: 3
reviews/round9-audit-grill.md:2400:completeness: 4
reviews/round9-audit-grill.md:2401:correctness: 3
reviews/round9-audit-grill.md:2402:error_handling: 3
reviews/round9-audit-grill.md:2403:simplicity: 4
reviews/round9-audit-grill.md:2404:spec_compliance: 3
reviews/round9-audit-grill.md:2423:completeness: 5
reviews/round9-audit-grill.md:2424:correctness: 5
reviews/round9-audit-grill.md:2425:error_handling: 5
reviews/round9-audit-grill.md:2426:simplicity: 4
reviews/round9-audit-grill.md:2427:spec_compliance: 5
reviews/round9-audit-grill.md:2433:completeness: 4
reviews/round9-audit-grill.md:2434:correctness: 4
reviews/round9-audit-grill.md:2435:error_handling: 3
reviews/round9-audit-grill.md:2436:simplicity: 4
reviews/round9-audit-grill.md:2437:spec_compliance: 3
reviews/round9-audit-grill.md:2448:completeness: 5
reviews/round9-audit-grill.md:2449:correctness: 5
reviews/round9-audit-grill.md:2450:error_handling: 4
reviews/round9-audit-grill.md:2451:simplicity: 5
reviews/round9-audit-grill.md:2452:spec_compliance: 5
reviews/round9-audit-grill.md:2964:I’ve confirmed the review-score trail and the SPEC v2 delta in git. Now I’m checking whether the repository content actually matches the v1 claims, including test count, core behavior, web/CLI presence, and whether the code still bakes in assumptions that v2 invalidates.
reviews/round9-audit-grill.md:6093:/bin/bash -lc "git log --oneline -- reviews/scores.md reviews/round1-plan.md reviews/round2-plan.md reviews/round3-plan.md reviews/round4-impl.md reviews/round5-impl.md reviews/round6-impl.md reviews/round7-hotfix.md reviews/round8-hotfix.md decisions/qa.md core channels tests | sed -n '1,120p'" in /home/rob/bpm-pizza-vibecoding-solution
reviews/round9-audit-grill.md:6379:a133c09 Apply plan review round 1 findings, capture review + scores
reviews/round9-audit-grill.md:6433: reviews/scores.md        |   29 +
reviews/round9-audit-grill.md:6535:- The v1 approval trail is real. [reviews/scores.md](/home/rob/bpm-pizza-vibecoding-solution/reviews/scores.md) records plan `24/25`, implementation `24/25`, hotfix `24/25`, and the git history shows the corresponding approval commits through `36131ca`.
reviews/round9-audit-grill.md:6555:- The v1 approval trail is real. [reviews/scores.md](/home/rob/bpm-pizza-vibecoding-solution/reviews/scores.md) records plan `24/25`, implementation `24/25`, hotfix `24/25`, and the git history shows the corresponding approval commits through `36131ca`.
reviews/round11-spec-v3-analysis.md:19:- Context you may trust: the repo implements v1 fully (approved, see reviews/scores.md); contract facts in v2's committed SPEC were verified against the live API, including: menu items carry {code,name,base[],price}; extras[] is the controlled toppings[] vocabulary with server 422 on unknowns; error bodies are {"error","details[]"}; statuses ordered->prepared_planned->delivered; /location returns {street,deliverable} and returned deliverable:true even for nonsense; there IS a detail endpoint GET /pizzerias/{id}/orders/{order_id} returning customer+items[] while the LIST endpoint carries NO items; codes unique per type (tonno pizza+pasta); dashboard at {PIZZASIM_URL}/dashboard/pizzerias/{id}; docs at {PIZZASIM_URL}/swagger.html.
reviews/round11-spec-v3-analysis.md:44:1. Attack: what is wrong or overstated in R1-R4/A1-A3/I1-I5? What did the implementer miss (check yourself: env table completeness, error table, testing section, deliverables tree vs existing repo, decisions-locked table consistency, anything contradicting the approved v1 core)?
reviews/round11-spec-v3-analysis.md:992:  rubric below so that quality is measurable across rounds instead of a vibe.
reviews/round11-spec-v3-analysis.md:1003:SCORES (1-5 each, 5 = best):
reviews/round11-spec-v3-analysis.md:1004:completeness: N
reviews/round11-spec-v3-analysis.md:1005:correctness: N
reviews/round11-spec-v3-analysis.md:1006:error_handling: N
reviews/round11-spec-v3-analysis.md:1007:simplicity: N
reviews/round11-spec-v3-analysis.md:1008:spec_compliance: N
reviews/round11-spec-v3-analysis.md:1015:  verdict line says approved but the scores miss that bar, **the numbers win**.
reviews/round11-spec-v3-analysis.md:1017:  scores and the open issues. That is a valid outcome, not a failure.
reviews/round11-spec-v3-analysis.md:1020:- Every reviewer stdout goes into `reviews/`, every round's scores get appended
reviews/round11-spec-v3-analysis.md:1021:  to `reviews/scores.md`, and `reviews/` is committed. The review trail belongs
reviews/round11-spec-v3-analysis.md:1033:fails the rubric is not done.
reviews/round11-spec-v3-analysis.md:1088:├── reviews/                 ← one file per review round, plus scores.md
reviews/round11-spec-v3-analysis.md:1217:/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:618:error_handling: N
reviews/round11-spec-v3-analysis.md:1320:/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:579:error_handling: N
reviews/round11-spec-v3-analysis.md:1352:/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:27:error_handling: N
reviews/round11-spec-v3-analysis.md:1467:/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:768:error_handling: N
reviews/round11-spec-v3-analysis.md:1470:/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:814:error_handling: N
reviews/round11-spec-v3-analysis.md:1824:/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:4041:error_handling: 4
reviews/round11-spec-v3-analysis.md:1826:/home/rob/bpm-pizza-vibecoding-solution/reviews/round4-impl.md:4058:error_handling: 4
reviews/round11-spec-v3-analysis.md:1952:/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:510:error_handling: N
reviews/round11-spec-v3-analysis.md:2098:/home/rob/bpm-pizza-vibecoding-solution/reviews/round11-spec-v3-analysis.md:19:- Context you may trust: the repo implements v1 fully (approved, see reviews/scores.md); contract facts in v2's committed SPEC were verified against the live API, including: menu items carry {code,name,base[],price}; extras[] is the controlled toppings[] vocabulary with server 422 on unknowns; error bodies are {"error","details[]"}; statuses ordered->prepared_planned->delivered; /location returns {street,deliverable} and returned deliverable:true even for nonsense; there IS a detail endpoint GET /pizzerias/{id}/orders/{order_id} returning customer+items[] while the LIST endpoint carries NO items; codes unique per type (tonno pizza+pasta); dashboard at {PIZZASIM_URL}/dashboard/pizzerias/{id}; docs at {PIZZASIM_URL}/swagger.html.
reviews/round11-spec-v3-analysis.md:2108:/home/rob/bpm-pizza-vibecoding-solution/reviews/round11-spec-v3-analysis.md:44:1. Attack: what is wrong or overstated in R1-R4/A1-A3/I1-I5? What did the implementer miss (check yourself: env table completeness, error table, testing section, deliverables tree vs existing repo, decisions-locked table consistency, anything contradicting the approved v1 core)?
reviews/round11-spec-v3-analysis.md:2112:/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:25:error_handling: N
reviews/round11-spec-v3-analysis.md:2122:/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:346:error_handling: N
reviews/round11-spec-v3-analysis.md:2138:/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:756:error_handling: N
reviews/round11-spec-v3-analysis.md:2205:/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1474:error_handling: 4
reviews/round11-spec-v3-analysis.md:2207:/home/rob/bpm-pizza-vibecoding-solution/reviews/round8-hotfix.md:1491:error_handling: 4
reviews/round11-spec-v3-analysis.md:2213:/home/rob/bpm-pizza-vibecoding-solution/reviews/scores.md:7:error_handling: 4
reviews/round11-spec-v3-analysis.md:2214:/home/rob/bpm-pizza-vibecoding-solution/reviews/scores.md:14:results restored to the spec's fixed contract; greeting language =
reviews/round11-spec-v3-analysis.md:2215:/home/rob/bpm-pizza-vibecoding-solution/reviews/scores.md:16:single explicit startup sequence via `GET /pizzerias`; read_back/confirm
reviews/round11-spec-v3-analysis.md:2216:/home/rob/bpm-pizza-vibecoding-solution/reviews/scores.md:17:path tightened (read_back only in READY/CONFIRMED, confirm only in READY).
reviews/round11-spec-v3-analysis.md:2217:/home/rob/bpm-pizza-vibecoding-solution/reviews/scores.md:23:error_handling: 4
reviews/round11-spec-v3-analysis.md:2218:/home/rob/bpm-pizza-vibecoding-solution/reviews/scores.md:31:greeting language now required env var PIZZERIA_LANG (oracle decision in
reviews/round11-spec-v3-analysis.md:2219:/home/rob/bpm-pizza-vibecoding-solution/reviews/scores.md:34:hint = PIZZERIA_LANG only; per-session immutable menu snapshot defined via
reviews/round11-spec-v3-analysis.md:2220:/home/rob/bpm-pizza-vibecoding-solution/reviews/scores.md:41:error_handling: 5
reviews/round11-spec-v3-analysis.md:2221:/home/rob/bpm-pizza-vibecoding-solution/reviews/scores.md:51:error_handling: 4
reviews/round11-spec-v3-analysis.md:2222:/home/rob/bpm-pizza-vibecoding-solution/reviews/scores.md:57:Findings applied: remove_item now deterministic across same-(type,code)
reviews/round11-spec-v3-analysis.md:2223:/home/rob/bpm-pizza-vibecoding-solution/reviews/scores.md:58:lines with different extras (no qty = all matching lines, qty = most recent
reviews/round11-spec-v3-analysis.md:2224:/home/rob/bpm-pizza-vibecoding-solution/reviews/scores.md:59:line; two new tests; PLAN.md updated); speech probe requires 2xx via
reviews/round11-spec-v3-analysis.md:2225:/home/rob/bpm-pizza-vibecoding-solution/reviews/scores.md:67:error_handling: 3
reviews/round11-spec-v3-analysis.md:2226:/home/rob/bpm-pizza-vibecoding-solution/reviews/scores.md:90:error_handling: 5
reviews/round11-spec-v3-analysis.md:2227:/home/rob/bpm-pizza-vibecoding-solution/reviews/scores.md:100:error_handling: 3
reviews/round11-spec-v3-analysis.md:2228:/home/rob/bpm-pizza-vibecoding-solution/reviews/scores.md:115:error_handling: 4
reviews/round11-spec-v3-analysis.md:2229:/home/rob/bpm-pizza-vibecoding-solution/reviews/scores.md:122:(isSecureContext=false): no JS errors, greeting, pizzeria name in header,
reviews/round11-spec-v3-analysis.md:2250:/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:25:error_handling: N
reviews/round11-spec-v3-analysis.md:2357:/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:883:error_handling: N
reviews/round11-spec-v3-analysis.md:2477:/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1507:error_handling: 4
reviews/round11-spec-v3-analysis.md:2483:/home/rob/bpm-pizza-vibecoding-solution/reviews/round2-plan.md:1531:error_handling: 4
reviews/round11-spec-v3-analysis.md:2489:/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:27:error_handling: N
reviews/round11-spec-v3-analysis.md:2492:/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:73:error_handling: N
reviews/round11-spec-v3-analysis.md:2615:/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1167:error_handling: N
reviews/round11-spec-v3-analysis.md:2746:/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1879:error_handling: 5
reviews/round11-spec-v3-analysis.md:2749:/home/rob/bpm-pizza-vibecoding-solution/reviews/round3-plan.md:1894:error_handling: 5
reviews/round11-spec-v3-analysis.md:2750:/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:23:error_handling: N
reviews/round11-spec-v3-analysis.md:2834:/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:1236:error_handling: 3
reviews/round11-spec-v3-analysis.md:2835:/home/rob/bpm-pizza-vibecoding-solution/reviews/round7-hotfix.md:1254:error_handling: 3
reviews/round11-spec-v3-analysis.md:2845:/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:23:error_handling: N
reviews/round11-spec-v3-analysis.md:2962:/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:939:error_handling: N
reviews/round11-spec-v3-analysis.md:3060:/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1569:One last check: I’m verifying the deliverables section to make sure the plan’s file layout doesn’t quietly drift from the required tree. Then I’ll finalize the rubric judgment.
reviews/round11-spec-v3-analysis.md:3070:/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1672:error_handling: 4
reviews/round11-spec-v3-analysis.md:3075:/home/rob/bpm-pizza-vibecoding-solution/reviews/round1-plan.md:1700:error_handling: 4
reviews/round11-spec-v3-analysis.md:3088:/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:33:error_handling: N
reviews/round11-spec-v3-analysis.md:3213:/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:841:error_handling: N
reviews/round11-spec-v3-analysis.md:3216:/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:887:error_handling: N
reviews/round11-spec-v3-analysis.md:3227:/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:1103:error_handling: N
reviews/round11-spec-v3-analysis.md:3508:/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:4629:error_handling: 3
reviews/round11-spec-v3-analysis.md:3512:/home/rob/bpm-pizza-vibecoding-solution/reviews/round5-impl.md:4653:error_handling: 3
reviews/round11-spec-v3-analysis.md:3524:/home/rob/bpm-pizza-vibecoding-solution/reviews/round10-grill-verdict.md:127:The implementer claims: SPEC v1 was fully built and approved (reviews/round1..8, reviews/scores.md with plan approved 24/25 and implementation approved 24/25, hotfix approved 24/25); 71 deterministic tests exist and are self-consistent; core/ implements the state machine, tool dispatch, PizzaSim client with submit-timeout recovery; channels/cli.py and channels/web.py + static UI exist; decisions/qa.md records oracle decisions. Verify each claim against the files and git log. Report discrepancies bluntly.
reviews/round11-spec-v3-analysis.md:3733:/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:36:error_handling: N
reviews/round11-spec-v3-analysis.md:4026:/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3072:error_handling: N
reviews/round11-spec-v3-analysis.md:4062:/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3510:error_handling: 5
reviews/round11-spec-v3-analysis.md:4064:/home/rob/bpm-pizza-vibecoding-solution/reviews/round6-impl.md:3525:error_handling: 5
reviews/round11-spec-v3-analysis.md:4065:/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:16:The implementer claims: SPEC v1 was fully built and approved (reviews/round1..8, reviews/scores.md with plan approved 24/25 and implementation approved 24/25, hotfix approved 24/25); 71 deterministic tests exist and are self-consistent; core/ implements the state machine, tool dispatch, PizzaSim client with submit-timeout recovery; channels/cli.py and channels/web.py + static UI exist; decisions/qa.md records oracle decisions. Verify each claim against the files and git log. Report discrepancies bluntly.
reviews/round11-spec-v3-analysis.md:4090:/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:286:error_handling: N
reviews/round11-spec-v3-analysis.md:4103:/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:509:error_handling: N
reviews/round11-spec-v3-analysis.md:4113:/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:732:error_handling: N
reviews/round11-spec-v3-analysis.md:4116:/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:778:error_handling: N
reviews/round11-spec-v3-analysis.md:4124:/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:953:error_handling: N
reviews/round11-spec-v3-analysis.md:4153:/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1180:error_handling: N
reviews/round11-spec-v3-analysis.md:4184:/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1404:error_handling: N
reviews/round11-spec-v3-analysis.md:4189:/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1612:error_handling: N
reviews/round11-spec-v3-analysis.md:4199:/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:1835:error_handling: N
reviews/round11-spec-v3-analysis.md:4263:/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2342:error_handling: 4
reviews/round11-spec-v3-analysis.md:4267:/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2358:error_handling: 4
reviews/round11-spec-v3-analysis.md:4270:/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2376:error_handling: 5
reviews/round11-spec-v3-analysis.md:4271:/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2386:error_handling: 4
reviews/round11-spec-v3-analysis.md:4275:/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2402:error_handling: 3
reviews/round11-spec-v3-analysis.md:4276:/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2425:error_handling: 5
reviews/round11-spec-v3-analysis.md:4277:/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2435:error_handling: 3
reviews/round11-spec-v3-analysis.md:4278:/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:2450:error_handling: 4
reviews/round11-spec-v3-analysis.md:4619:/home/rob/bpm-pizza-vibecoding-solution/reviews/round9-audit-grill.md:6093:/bin/bash -lc "git log --oneline -- reviews/scores.md reviews/round1-plan.md reviews/round2-plan.md reviews/round3-plan.md reviews/round4-impl.md reviews/round5-impl.md reviews/round6-impl.md reviews/round7-hotfix.md reviews/round8-hotfix.md decisions/qa.md core channels tests | sed -n '1,120p'" in /home/rob/bpm-pizza-vibecoding-solution
reviews/round11-spec-v3-analysis.md:5332:  rubric so quality is measurable across rounds instead of a vibe.
reviews/round11-spec-v3-analysis.md:5364:SCORES (1-5 each, 5 = best):
reviews/round11-spec-v3-analysis.md:5365:completeness: N
reviews/round11-spec-v3-analysis.md:5366:correctness: N
reviews/round11-spec-v3-analysis.md:5367:error_handling: N
reviews/round11-spec-v3-analysis.md:5368:simplicity: N
reviews/round11-spec-v3-analysis.md:5369:spec_compliance: N
reviews/round11-spec-v3-analysis.md:5376:  verdict line says approved but the scores miss that bar, **the numbers
reviews/round11-spec-v3-analysis.md:5379:  the scores and the open issues. A valid outcome, not a failure.
reviews/round11-spec-v3-analysis.md:5382:- Every reviewer stdout goes into `reviews/`, every round's scores into
reviews/round11-spec-v3-analysis.md:5383:  `reviews/scores.md`, and `reviews/` is committed.
reviews/round11-spec-v3-analysis.md:5394:fails the rubric is not done.
reviews/round11-spec-v3-analysis.md:5454:├── reviews/                 ← one file per review round, plus scores.md
reviews/round11-spec-v3-analysis.md:6418:scores.md
reviews/round11-spec-v3-analysis.md:6589:/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_2.md:633:  to `reviews/scores.md`, and `reviews/` is committed. The review trail belongs
reviews/round11-spec-v3-analysis.md:6600:/home/rob/bpm-pizza-vibecoding-solution/SPEC_20260801_1.md:525:  to `reviews/scores.md`, and `reviews/` is committed. The review trail belongs
reviews/round2-plan.md:15:2. Judge: score against the fixed rubric.
reviews/round2-plan.md:21:Output MUST end with exactly this block (numbers 1-5, 5 best):
reviews/round2-plan.md:22:SCORES (1-5 each, 5 = best):
reviews/round2-plan.md:23:completeness: N
reviews/round2-plan.md:24:correctness: N
reviews/round2-plan.md:25:error_handling: N
reviews/round2-plan.md:26:simplicity: N
reviews/round2-plan.md:27:spec_compliance: N
reviews/round2-plan.md:35:Reviewing `SPEC.md` and `PLAN.md` against each other first, then I’ll score the plan strictly against the rubric and the round-1 carryover requirements.
reviews/round2-plan.md:444:reviews/       One file per review round + scores.md.
reviews/round2-plan.md:869:  rubric below so that quality is measurable across rounds instead of a vibe.
reviews/round2-plan.md:880:SCORES (1-5 each, 5 = best):
reviews/round2-plan.md:881:completeness: N
reviews/round2-plan.md:882:correctness: N
reviews/round2-plan.md:883:error_handling: N
reviews/round2-plan.md:884:simplicity: N
reviews/round2-plan.md:885:spec_compliance: N
reviews/round2-plan.md:892:  verdict line says approved but the scores miss that bar, **the numbers win**.
reviews/round2-plan.md:894:  scores and the open issues. That is a valid outcome, not a failure.
reviews/round2-plan.md:897:- Every reviewer stdout goes into `reviews/`, every round's scores get appended
reviews/round2-plan.md:898:  to `reviews/scores.md`, and `reviews/` is committed. The review trail belongs
reviews/round2-plan.md:910:fails the rubric is not done.
reviews/round2-plan.md:961:  unknown → recovery-by-list, 422 mapping, snapshot completeness.
reviews/round2-plan.md:1443:   280	  unknown → recovery-by-list, 422 mapping, snapshot completeness.
reviews/round2-plan.md:1504:SCORES (1-5 each, 5 = best):
reviews/round2-plan.md:1505:completeness: 3
reviews/round2-plan.md:1506:correctness: 3
reviews/round2-plan.md:1507:error_handling: 4
reviews/round2-plan.md:1508:simplicity: 4
reviews/round2-plan.md:1509:spec_compliance: 2
reviews/round2-plan.md:1528:SCORES (1-5 each, 5 = best):
reviews/round2-plan.md:1529:completeness: 3
reviews/round2-plan.md:1530:correctness: 3
reviews/round2-plan.md:1531:error_handling: 4
reviews/round2-plan.md:1532:simplicity: 4
reviews/round2-plan.md:1533:spec_compliance: 2
reviews/round5-impl.md:15:2. Judge: score against the fixed rubric.
reviews/round5-impl.md:29:Output MUST end with exactly this block (numbers 1-5, 5 best):
reviews/round5-impl.md:30:SCORES (1-5 each, 5 = best):
reviews/round5-impl.md:31:completeness: N
reviews/round5-impl.md:32:correctness: N
reviews/round5-impl.md:33:error_handling: N
reviews/round5-impl.md:34:simplicity: N
reviews/round5-impl.md:35:spec_compliance: N
reviews/round5-impl.md:217:Reviewing implementation against spec, approved plan, and round-1 required fixes before issuing findings and rubric scores.
reviews/round5-impl.md:221:  • Produce findings ordered by severity and score against the rubric
reviews/round5-impl.md:306:reviews/       One file per review round + scores.md.
reviews/round5-impl.md:532:  `submit_attempted_at`), 422 mapping, snapshot completeness.
reviews/round5-impl.md:829:2. Judge: score against the fixed rubric.
reviews/round5-impl.md:835:Judging guidance: score the plan that exists. If remaining concerns are implementation-detail-sized rather than plan-sized, they belong in the implementation review, not in a plan rejection.
reviews/round5-impl.md:837:Output MUST end with exactly this block (numbers 1-5, 5 best):
reviews/round5-impl.md:838:SCORES (1-5 each, 5 = best):
reviews/round5-impl.md:839:completeness: N
reviews/round5-impl.md:840:correctness: N
reviews/round5-impl.md:841:error_handling: N
reviews/round5-impl.md:842:simplicity: N
reviews/round5-impl.md:843:spec_compliance: N
reviews/round5-impl.md:851:I’m reviewing `SPEC.md`, `PLAN.md`, the prior round review, and the QA decision first. I’m using the `using-superpowers` skill to ensure the required workflow, then I’ll assess the plan strictly against the spec and rubric.
reviews/round5-impl.md:877:2. Judge: score against the fixed rubric.
reviews/round5-impl.md:883:Output MUST end with exactly this block (numbers 1-5, 5 best):
reviews/round5-impl.md:884:SCORES (1-5 each, 5 = best):
reviews/round5-impl.md:885:completeness: N
reviews/round5-impl.md:886:correctness: N
reviews/round5-impl.md:887:error_handling: N
reviews/round5-impl.md:888:simplicity: N
reviews/round5-impl.md:889:spec_compliance: N
reviews/round5-impl.md:897:Reviewing `SPEC.md` and `PLAN.md` against each other first, then I’ll score the plan strictly against the rubric and the round-1 carryover requirements.
reviews/round5-impl.md:1091:2. Judge: score against the fixed rubric.
reviews/round5-impl.md:1099:Output MUST end with exactly this block (numbers 1-5, 5 best):
reviews/round5-impl.md:1100:SCORES (1-5 each, 5 = best):
reviews/round5-impl.md:1101:completeness: N
reviews/round5-impl.md:1102:correctness: N
reviews/round5-impl.md:1103:error_handling: N
reviews/round5-impl.md:1104:simplicity: N
reviews/round5-impl.md:1105:spec_compliance: N
reviews/round5-impl.md:1113:Using `using-superpowers` first to load the required workflow, then I’ll inspect `SPEC.md`, `PLAN.md`, and the implementation files to review against the approved plan and rubric.
reviews/round5-impl.md:1277:reviews/scores.md
reviews/round5-impl.md:1283:Setting a short review workflow: read the source-of-truth docs first, inspect implementation areas against them, then produce findings and rubric scores.
reviews/round5-impl.md:1286:  • Draft findings, rubric scores, and verdict
reviews/round5-impl.md:1341:  • Produce findings ordered by severity and score against the rubric
reviews/round5-impl.md:4612:I have enough to score. I’m grabbing one last reference around submit-timeout recovery so the highest-severity finding is tied to the exact recovery code path, not just the state bookkeeping.
reviews/round5-impl.md:4626:SCORES (1-5 each, 5 = best):
reviews/round5-impl.md:4627:completeness: 4
reviews/round5-impl.md:4628:correctness: 3
reviews/round5-impl.md:4629:error_handling: 3
reviews/round5-impl.md:4630:simplicity: 4
reviews/round5-impl.md:4631:spec_compliance: 3
reviews/round5-impl.md:4650:SCORES (1-5 each, 5 = best):
reviews/round5-impl.md:4651:completeness: 4
reviews/round5-impl.md:4652:correctness: 3
reviews/round5-impl.md:4653:error_handling: 3
reviews/round5-impl.md:4654:simplicity: 4
reviews/round5-impl.md:4655:spec_compliance: 3
reviews/round7-hotfix.md:20:SCORES (1-5 each, 5 = best):
reviews/round7-hotfix.md:21:completeness: N
reviews/round7-hotfix.md:22:correctness: N
reviews/round7-hotfix.md:23:error_handling: N
reviews/round7-hotfix.md:24:simplicity: N
reviews/round7-hotfix.md:25:spec_compliance: N
reviews/round7-hotfix.md:305:reviews/       One file per review round + scores.md.
reviews/round7-hotfix.md:1002:I found one substantive regression risk in the hotfix path, and I’m pulling exact line numbers now so the review can be concrete. After that I’ll score it against the approval bar.
reviews/round7-hotfix.md:1233:SCORES (1-5 each, 5 = best):
reviews/round7-hotfix.md:1234:completeness: 4
reviews/round7-hotfix.md:1235:correctness: 4
reviews/round7-hotfix.md:1236:error_handling: 3
reviews/round7-hotfix.md:1237:simplicity: 4
reviews/round7-hotfix.md:1238:spec_compliance: 3
reviews/round7-hotfix.md:1251:SCORES (1-5 each, 5 = best):
reviews/round7-hotfix.md:1252:completeness: 4
reviews/round7-hotfix.md:1253:correctness: 4
reviews/round7-hotfix.md:1254:error_handling: 3
reviews/round7-hotfix.md:1255:simplicity: 4
reviews/round7-hotfix.md:1256:spec_compliance: 3

codex
I have enough to judge. I’m doing one final pass for omissions around failure semantics and “customer’s language” handling, because those are the easiest places for a stage-1 plan to leave escape hatches.
exec
/bin/bash -lc "nl -ba PLAN.md | sed -n '1,260p'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "nl -ba SPEC.md | sed -n '338,520p'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "nl -ba core/agent.py | sed -n '1,240p'" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 314ms:
     1	# PizzaSim Ordering Agent — Implementation Plan v2
     2	
     3	> Stage-1 artifact for SPEC.md (v3, patched, gate-approved in Issue #1).
     4	> Retrofit of the approved v1 build per the grill verdict in
     5	> `decisions/qa.md` (RETROFIT, 5 binding conditions). Design only — no code.
     6	
     7	**Goal:** Extend the approved v1 agent to SPEC v3: customer-selectable
     8	pizzerias, prices and code-owned totals, the full web-channel contract
     9	(header/footer/basket/confirm control/answer invariant), APP_VERSION,
    10	per-session language, and a mandatory offline browser E2E suite.
    11	
    12	**Architecture:** unchanged core idea — the order is a state machine owned
    13	by code, the model only speaks. What moves: everything tenant-, language-
    14	and menu-scoped moves from process-global into a per-session `Session`
    15	owned by core. Channels stay transports; the web UI is rebuilt to the new
    16	contract.
    17	
    18	**Tech stack:** Python 3.13, httpx, FastAPI + uvicorn, pytest, Playwright
    19	(browser E2E, already installed), stdlib elsewhere. No new dependencies
    20	beyond Playwright.
    21	
    22	## What carries over unchanged from v1 (approved 24/25)
    23	
    24	- `core/order.py` Order/Item/Customer + revision + submit bookkeeping
    25	- `core/state.py` transitions, invariants 1–5, demotion, terminality,
    26	  deterministic `remove_item` semantics (now also written into SPEC)
    27	- `core/menu.py` (type, code) validation, candidates, extras vocabulary
    28	- `core/pizzasim.py` typed errors, timeouts, list+detail endpoints,
    29	  submit-timeout recovery (shortlist via list, verify items via detail —
    30	  exactly what the patched SPEC now demands)
    31	- `core/tools.py` schemas/dispatch incl. atomic add, error shape
    32	- `core/agent.py` model loop, retry-once, JSONL logging, stub-model seam
    33	- CLI channel, prompts, 71 deterministic tests, golden transcripts
    34	
    35	## The five binding retrofit conditions (decisions/qa.md) → where honored
    36	
    37	| Condition | Where in this plan |
    38	|---|---|
    39	| 1. `PIZZERIA_LANG` documented | now in SPEC's env table; config section below |
    40	| 2. Core-owned session factory, immutable tenant | "Session model v2" |
    41	| 3. Confirm path via one core method | "Confirm control" |
    42	| 4. Web = substantial rewrite | "Web channel v2" + tickets 6–7 |
    43	| 5. Totals canonical in core + E2E coverage | "Prices and totals", ticket 1, 9 |
    44	
    45	## Configuration
    46	
    47	| Module | Vars |
    48	|---|---|
    49	| `core/agent.py` | `LITELLM_PIZZA_URL`, `LITELLM_PIZZA_KEY`, `LITELLM_PIZZA_MODEL_1`, `PIZZERIA_LANG` (required; `LITELLM_PIZZA_MODEL_2` read, unused) |
    50	| `core/pizzasim.py` | `PIZZASIM_URL`, `PIZZASIM_API_KEY`, `PIZZERIA_ID` (required) |
    51	| `channels/web.py` | `APP_VERSION` (required) |
    52	| `channels/speech.py` | `SPEECH_URL`, `SPEECH_STT_MODEL`, `SPEECH_TTS_MODEL`, `SPEECH_TTS_VOICE` (all optional; absence disables speech) |
    53	
    54	Loading unchanged: process env, else `~/.env`; missing required var →
    55	exit before the first turn naming variable and file. `APP_VERSION` must
    56	match `x.y.z` (regex on the value is config validation, not order
    57	parsing). Derived URLs, never literal: dashboard
    58	`{PIZZASIM_URL}/dashboard/pizzerias/{id}`, docs
    59	`{PIZZASIM_URL}/swagger.html`.
    60	
    61	## Session model v2 (condition 2)
    62	
    63	`Session` (core/agent.py): `{id, pizzeria_id, pizzeria_name, client,
    64	menu, lang, order, messages}` — pizzeria fields and client are set at
    65	creation and never mutated (a tenant switch is a NEW session; invariant 6).
    66	
    67	Core factory `create_session(config, base, pizzeria_id, lang)`:
    68	
    69	1. `base.list_pizzerias()` (tenant-free call) → id must be present, else
    70	   typed `NotFoundError` → channel renders "that pizzeria isn't available
    71	   right now" (session error; process stays up, per the new error row).
    72	2. Build a tenant-bound `PizzaSim` client for `pizzeria_id`.
    73	3. Fetch the fresh, immutable menu snapshot for this session (invariant 5).
    74	4. Render `prompts/system.{lang}.md` with the pizzeria name.
    75	
    76	Startup (unchanged semantics, now explicit about roles): validate required
    77	env; `GET /pizzerias` must contain the preselected `PIZZERIA_ID` (else the
    78	process refuses to start — the startup 404 row); fetch `/menu` once as a
    79	health check ("We're not taking orders right now" on failure). The
    80	preselection is only the default for new sessions.
    81	
    82	CLI: one session from `PIZZERIA_ID` + `PIZZERIA_LANG`; no switching (per
    83	SPEC's language-authority rule and header-only selector).
    84	
    85	## Language authority (condition 1)
    86	
    87	`Session.lang` starts from the channel: CLI and web default =
    88	`PIZZERIA_LANG`; the web header switch calls `set_language(session, lang)`
    89	(core), which re-renders `messages[0]` from the prompt file in the new
    90	language — same policy text, history preserved. Apologies and the STT/TTS
    91	language read `session.lang`. Reply language stays per-turn mirroring by
    92	the model (prompt rule) and always wins over the switch, exactly as SPEC
    93	states. UI chrome strings are a small de/en dictionary in `app.js`, keyed
    94	by the session language.
    95	
    96	## Prices and totals (condition 5)
    97	
    98	- `Menu` keeps `price` per (type, code); `as_tool_result()` returns
    99	  `{code, name, price}` per item plus `toppings[]`.
   100	- `Item` gains `unit_price`, copied at add time from the session menu
   101	  snapshot (prices are stable for the session, like the menu itself).
   102	- `Order.snapshot()` gains per line `unit_price`, `line_total`
   103	  (= qty × unit_price) and top-level `basket_total` — computed in
   104	  `core/order.py` only. Money is rounded to cents with `Decimal`;
   105	  no float accumulation.
   106	- `read_back` carries the snapshot and therefore the canonical total; the
   107	  web basket renders the same numbers. Extras carry no API price → lines
   108	  show base prices; the UI labels extras "not separately priced" — no
   109	  invented figures.
   110	- The model never computes prices: the prompt instructs it to quote
   111	  `price`/`basket_total` from tool results verbatim.
   112	
   113	## Tools — v1 contract plus prices
   114	
   115	Schemas and parameters unchanged (fixed by SPEC). Result changes only:
   116	
   117	- `get_menu` → `{menu: {pizzas: [{code, name, price}], pasta: [...],
   118	  toppings: [...]}, snapshot}`
   119	- `SNAPSHOT` → `{state, revision, items: [{type, code, name, qty, extras,
   120	  unit_price, line_total}], basket_total, customer, read_back_done}`
   121	- everything else exactly as approved in v1 (uniform error shape,
   122	  atomicity, invalid_quantity, deterministic remove).
   123	
   124	## Confirm control (condition 3)
   125	
   126	- `read_back` results stream to the UI (they already do); the UI renders a
   127	  visually distinct read-back panel with a **Bestellen/Confirm** button
   128	  bound to the streamed `revision`.
   129	- Click → `POST /confirm {session_id, revision}` → **one core method**
   130	  `Agent.confirm_and_submit(session, revision, emit)`:
   131	  1. `tools.dispatch("confirm_order", {revision})` — stale revision or
   132	     wrong state returns the typed error; it streams to the UI as a
   133	     notice and nothing is submitted.
   134	  2. On success `tools.dispatch("submit_order", {})` (full v1 semantics
   135	     incl. timeout recovery).
   136	  3. Both calls are appended to `session.messages` as a synthetic
   137	     assistant `tool_calls` message + `tool` results (OpenAI format), so
   138	     the model's context stays consistent.
   139	  4. One model call phrases the outcome (order id in groups, minutes);
   140	     it streams like a normal turn and is logged.
   141	- The customer action is a click, not a word; `CONFIRMED` remains
   142	  reachable only via `confirm_order(revision)`; the transport forwards two
   143	  identifiers and owns zero logic.
   144	- CLI keeps the conversational path: customer says yes → model calls
   145	  `confirm_order` + `submit_order` itself. Both paths converge on dispatch.
   146	
   147	## Web channel v2 (condition 4 — a rewrite, named as such)
   148	
   149	Server (`channels/web.py`):
   150	
   151	- `GET /config` → `{version, speech, lang_default, pizzerias:
   152	  [{id, name}] | null, preselected_id, dashboard_base, docs_url}`.
   153	  `pizzerias: null` when `GET /pizzerias` failed at request time — the UI
   154	  then shows "list unavailable" and no selector (no fallback entry).
   155	- `POST /session {pizzeria_id?, lang?}` → creates a Session (defaults:
   156	  preselected id, `PIZZERIA_LANG`), returns `{session_id, pizzeria_id,
   157	  pizzeria_name, lang}`. Invalid id → 409 with the session-error text.
   158	- `POST /chat {session_id, text|null}` → NDJSON stream (unchanged
   159	  protocol; `text: null` = greeting turn). 404 for unknown session (the
   160	  UI then creates a fresh one). Per-session lock → 409 on overlap.
   161	- `POST /confirm {session_id, revision}` → NDJSON stream (same event
   162	  shapes) via `confirm_and_submit`.
   163	- `POST /language {session_id, lang}` → `{lang}`; core `set_language`.
   164	- `GET /health` → `{api: "ok"|"down", gateway: "ok"|"down"|"unknown"}` —
   165	  `api` from a live `GET /pizzerias` with 3s timeout; `gateway` from the
   166	  outcome of the most recent model call (unknown before the first).
   167	  Polled by the UI every 30s for the footer connection state.
   168	- Speech proxy endpoints move to `channels/speech.py` (deliverable):
   169	  `SpeechService` class (config, probe, stt(audio, lang), tts(text,
   170	  lang)); web.py keeps only the thin route handlers.
   171	
   172	UI (`channels/static/` — rebuilt):
   173	
   174	- **Header:** pizzeria name (prominent, from the session), selector
   175	  (name + first 8 UUID chars, from `/config.pizzerias`), dashboard link
   176	  (`dashboard_base` + id, `target="_blank"`), language switch DE/EN,
   177	  Start over. Selector change and Start over both: abort any in-flight
   178	  stream (AbortController), clear the chat and basket views, create a NEW
   179	  session (fresh id — invariant 6 by construction), render the greeting
   180	  turn.
   181	- **Footer:** `version`, full selected UUID (selectable text), connection
   182	  badges from `/health`, docs link.
   183	- **Basket panel:** rendered from every `snapshot` in tool results /
   184	  `done` events: lines with qty × name, `line_total`, `basket_total`;
   185	  after `state == "SUBMITTED"`: locked, shows order id + "submitted", no
   186	  control on the page can modify or resubmit (confirm button removed,
   187	  input stays usable for a new conversation via Start over / new session).
   188	- **Read-back panel:** on a `read_back` tool result: visually distinct
   189	  block + confirm button bound to the streamed revision.
   190	- **Answer invariant** ("no message ends unanswered"):
   191	  - send → immediate "agent is working" indicator;
   192	  - tool events render as they stream (collapsible steps, visually
   193	    distinct) — never discarded (anti-pattern 6);
   194	  - `done` without a preceding `assistant` event in the turn → rendered
   195	    notice "the agent did not answer — resend?";
   196	  - fetch error / abort / non-2xx → rendered notice naming which
   197	    (error, timeout, connection lost) + a resend button that re-posts the
   198	    same text;
   199	  - all notices in the session language, plain words.
   200	
   201	## CLI v2
   202	
   203	Unchanged flow; read_back output now includes line totals and the basket
   204	total from the snapshot (printing what core computed, no arithmetic).
   205	
   206	## Error handling — new rows on top of v1's table
   207	
   208	| Situation | Mechanism |
   209	|---|---|
   210	| Runtime pizzeria selection invalid | `create_session` NotFoundError → 409 → UI notice; process stays up |
   211	| Pizzeria list fetch fails | `/config.pizzerias = null` → "list unavailable", no selector, no fallback entry |
   212	| Stream ends without final message | UI-side detection via `done`-without-`assistant` → notice + resend |
   213	| Gateway unreachable | existing retry-once → apology (now also an `assistant` event, v1 fix) + UI resend offer |
   214	| Speech service down | probe fails → controls not rendered; per-call failure → notice, order untouched |
   215	
   216	All other rows: unchanged v1 mechanics, already tested.
   217	
   218	## Testing
   219	
   220	- **Unit/tool (extend v1's 71):** prices copied at add time; `line_total`
   221	  / `basket_total` incl. Decimal rounding; snapshot shape; session factory
   222	  (valid id, unknown id, list failure); `set_language` re-render;
   223	  `confirm_and_submit` (happy, stale revision, submit timeout path);
   224	  `APP_VERSION` validation.
   225	- **Golden transcripts:** unchanged five; runner asserts extended snapshot
   226	  keys where relevant.
   227	- **Browser E2E (`tests/test_web_e2e.py`, offline, not optional):**
   228	  in-process **stub PizzaSim** (fixtures: two pizzerias, menu with prices)
   229	  and **stub gateway** (scripted tool-calling model) served locally;
   230	  the app under test started on an ephemeral port with env pointing at the
   231	  stubs; Playwright (chromium, headless) asserts against the DOM:
   232	  1. full order: greeting → price question (price from menu rendered) →
   233	     add items → name → read-back panel → **confirm click** → submitted
   234	     lock + order id visible; basket totals correct at each step;
   235	  2. pizzeria switch: selector → fresh conversation, header + footer UUID
   236	     change, basket cleared;
   237	  3. failure — tool error: unknown item → candidates visible in steps,
   238	     answer rendered;
   239	  4. failure — gateway unreachable: stub gateway refuses → apology text
   240	     rendered + resend control;
   241	  5. failure — stream ends without final message: stub cuts the stream →
   242	     UI notice + resend control.
   243	- **Live acceptance test:** as in v1, updated to SPEC wording (presence
   244	  via list, customer/items/qty via detail endpoint). Opt-in
   245	  `PIZZA_LIVE_TEST=1`.
   246	- **Speech:** manual checklist (README) unchanged + STT language follows
   247	  the session language.
   248	
   249	## Deliverables delta vs repo
   250	
   251	New: `channels/speech.py`, `tests/test_web_e2e.py`. Rebuilt:
   252	`channels/web.py`, `channels/static/*`. Extended: `core/menu.py`,
   253	`core/order.py`, `core/tools.py`, `core/agent.py`, prompts (prices,
   254	verbatim-price rule), `README.md`, `.env.example` (+`APP_VERSION`),
   255	`requirements.txt` (+playwright). Everything else stands as approved.
   256	
   257	## Tickets (each ≤ 1h, tests in the ticket that introduces the behaviour)
   258	
   259	1. **Prices & totals in core.** Menu price, `Item.unit_price`,
   260	   snapshot totals (Decimal), get_menu result, prompt rule.

 succeeded in 276ms:
     1	"""Model loop: prompt assembly, chat-completions calls, tool dispatch,
     2	JSONL event logging. The model only speaks; the order lives in core."""
     3	from __future__ import annotations
     4	
     5	import json
     6	import time
     7	import uuid
     8	from dataclasses import dataclass, field
     9	from pathlib import Path
    10	
    11	import httpx
    12	
    13	from . import tools
    14	from .menu import Menu
    15	from .order import Order
    16	from .pizzasim import PizzaSim, optional_env, require_env
    17	
    18	PROMPT_DIR = Path(__file__).resolve().parent.parent / "prompts"
    19	LOG_DIR = Path("logs")
    20	MAX_TOOL_ROUNDS = 8
    21	GATEWAY_TIMEOUT = httpx.Timeout(30.0, connect=10.0)  # per approved plan
    22	
    23	APOLOGY = {
    24	    "de": "Entschuldigung, da ist gerade etwas schiefgegangen. "
    25	          "Können Sie das bitte noch einmal sagen?",
    26	    "en": "I'm sorry, something went wrong on my end just now. "
    27	          "Could you say that again, please?",
    28	}
    29	
    30	
    31	class GatewayError(Exception):
    32	    pass
    33	
    34	
    35	@dataclass
    36	class AgentConfig:
    37	    url: str
    38	    key: str
    39	    model: str
    40	    lang: str  # PIZZERIA_LANG: greeting language = pizzeria country
    41	
    42	    @classmethod
    43	    def from_env(cls) -> "AgentConfig":
    44	        lang = require_env("PIZZERIA_LANG").lower()
    45	        if lang not in ("de", "en"):
    46	            raise ValueError(
    47	                "PIZZERIA_LANG must be 'de' or 'en', got something else"
    48	            )
    49	        optional_env("LITELLM_PIZZA_MODEL_2")  # read; unused (single-model)
    50	        return cls(
    51	            url=require_env("LITELLM_PIZZA_URL").rstrip("/"),
    52	            key=require_env("LITELLM_PIZZA_KEY"),
    53	            model=require_env("LITELLM_PIZZA_MODEL_1"),
    54	            lang=lang,
    55	        )
    56	
    57	
    58	def system_prompt(lang: str, pizzeria_name: str) -> str:
    59	    text = (PROMPT_DIR / f"system.{lang}.md").read_text()
    60	    return text.replace("{pizzeria_name}", pizzeria_name)
    61	
    62	
    63	@dataclass
    64	class Session:
    65	    """One conversation: one Order, one immutable Menu snapshot, one
    66	    history."""
    67	    order: Order
    68	    menu: Menu
    69	    messages: list[dict]
    70	    id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    71	
    72	    @classmethod
    73	    def create(cls, config: AgentConfig, menu: Menu,
    74	               pizzeria_name: str) -> "Session":
    75	        return cls(
    76	            order=Order(),
    77	            menu=menu,
    78	            messages=[{"role": "system",
    79	                       "content": system_prompt(config.lang,
    80	                                                pizzeria_name)}],
    81	        )
    82	
    83	
    84	def log_event(session: Session, event: dict) -> None:
    85	    """One line per event, JSON, to a file. Never carries config values."""
    86	    LOG_DIR.mkdir(exist_ok=True)
    87	    record = {"ts": round(time.time(), 3), "session": session.id, **event}
    88	    with (LOG_DIR / f"agent-{session.id}.jsonl").open("a") as fh:
    89	        fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    90	
    91	
    92	class Agent:
    93	    def __init__(self, config: AgentConfig, client: PizzaSim,
    94	                 chat_fn=None):
    95	        self.config = config
    96	        self.client = client
    97	        # chat_fn(messages, tools) -> assistant message dict; injectable so
    98	        # the golden transcripts run against a stub with no network.
    99	        self._chat_fn = chat_fn or self._gateway_chat
   100	
   101	    def _gateway_chat(self, messages: list[dict],
   102	                      tool_schemas: list[dict]) -> dict:
   103	        payload = {
   104	            "model": self.config.model,
   105	            "messages": messages,
   106	            "tools": tool_schemas,
   107	        }
   108	        headers = {"Authorization": f"Bearer {self.config.key}"}
   109	        last_exc: Exception | None = None
   110	        for attempt in range(2):  # one retry on timeout, then abort turn
   111	            try:
   112	                response = httpx.post(
   113	                    f"{self.config.url}/chat/completions",
   114	                    json=payload, headers=headers, timeout=GATEWAY_TIMEOUT,
   115	                )
   116	                response.raise_for_status()
   117	                return response.json()["choices"][0]["message"]
   118	            except httpx.TimeoutException as exc:
   119	                last_exc = exc
   120	                continue
   121	            except (httpx.HTTPError, KeyError, ValueError) as exc:
   122	                raise GatewayError(f"gateway request failed: "
   123	                                   f"{type(exc).__name__}") from exc
   124	        raise GatewayError("gateway timed out twice") from last_exc
   125	
   126	    def run_turn(self, session: Session, user_text: str | None,
   127	                 emit=lambda event: None) -> str:
   128	        """One customer turn: returns the assistant's final text. Every
   129	        intermediate step goes to emit() and the JSONL log. user_text None
   130	        is the opening turn — the agent greets first, unprompted."""
   131	
   132	        def event(payload: dict) -> None:
   133	            log_event(session, payload)
   134	            emit(payload)
   135	
   136	        if user_text is not None:
   137	            session.messages.append({"role": "user", "content": user_text})
   138	            event({"type": "user", "text": user_text})
   139	
   140	        for _ in range(MAX_TOOL_ROUNDS):
   141	            try:
   142	                message = self._chat_fn(session.messages,
   143	                                        tools.openai_tools())
   144	            except GatewayError as exc:
   145	                event({"type": "error", "error": str(exc)})
   146	                apology = APOLOGY[self.config.lang]
   147	                session.messages.append({"role": "assistant",
   148	                                         "content": apology})
   149	                event({"type": "assistant", "text": apology})
   150	                return apology
   151	
   152	            tool_calls = message.get("tool_calls")
   153	            if not tool_calls:
   154	                text = message.get("content") or ""
   155	                session.messages.append({"role": "assistant",
   156	                                         "content": text})
   157	                event({"type": "assistant", "text": text})
   158	                return text
   159	
   160	            session.messages.append({
   161	                "role": "assistant",
   162	                "content": message.get("content"),
   163	                "tool_calls": tool_calls,
   164	            })
   165	            for call in tool_calls:
   166	                name = call["function"]["name"]
   167	                try:
   168	                    args = json.loads(call["function"]["arguments"] or "{}")
   169	                except ValueError:
   170	                    args = {}
   171	                event({"type": "tool_call", "tool": name, "args": args})
   172	                result = tools.dispatch(session.order, session.menu,
   173	                                        self.client, name, args)
   174	                event({"type": "tool_result", "tool": name,
   175	                       "result": result})
   176	                event({"type": "state",
   177	                       "state": session.order.state.value,
   178	                       "revision": session.order.revision})
   179	                session.messages.append({
   180	                    "role": "tool",
   181	                    "tool_call_id": call.get("id", name),
   182	                    "content": json.dumps(result, ensure_ascii=False),
   183	                })
   184	
   185	        event({"type": "error", "error": "tool loop guard exceeded"})
   186	        apology = APOLOGY[self.config.lang]
   187	        session.messages.append({"role": "assistant", "content": apology})
   188	        event({"type": "assistant", "text": apology})
   189	        return apology
   190	
   191	
   192	def startup(config: AgentConfig) -> tuple[PizzaSim, str, Menu]:
   193	    """The one startup sequence (PLAN): env → pizzeria check → menu.
   194	    Raises before the first turn on any failure."""
   195	    client = PizzaSim.from_env()
   196	    pizzeria_name = client.pizzeria_name()
   197	    menu = Menu(client.get_menu())
   198	    return client, pizzeria_name, menu

 succeeded in 311ms:
   338	
   339	- Greet first, in the session language, and offer help — one sentence, not a
   340	  menu recital.
   341	
   342	**Language authority — one rule.** The session language starts as
   343	`PIZZERIA_LANG` (greeting, CLI, web UI chrome before any switch). The web
   344	header switch changes the session language: UI chrome, the greeting of a
   345	fresh conversation, and the speech hint (STT language, TTS output). For the
   346	agent's replies, per-turn mirroring wins: it answers in the language of the
   347	customer's latest message, even when that differs from the session language.
   348	The CLI has no switch and stays at `PIZZERIA_LANG`.
   349	- **One question per turn.** Never stack "name, street and what would you
   350	  like?"
   351	- Never state a menu item or a price that did not come from `get_menu` in this
   352	  session. Price questions are normal questions, and so is "what does my
   353	  basket come to?"
   354	- Collect first name and street. If the customer declines the street, accept
   355	  it — it is optional in the API.
   356	- Before submitting: call `read_back`, present it, and wait for an explicit
   357	  yes. "Mhm" and silence are not a yes; ask once more, then offer to start
   358	  over.
   359	- Never announce that an order was placed before `submit_order` returned an
   360	  `order_id`.
   361	- On success, state the order id in a form a human can repeat back, and the
   362	  wait time in **minutes**, converted from `eta_seconds`.
   363	- On error, explain in plain language what happened and what the options are.
   364	  Never show a status code, stack trace or JSON.
   365	- Never claim to have checked an address for deliverability.
   366	
   367	---
   368	
   369	## The web channel
   370	
   371	The web UI is where a stranger decides whether this thing works. Everything
   372	below is required, and each line is written so it can be checked by looking at
   373	the page.
   374	
   375	### The conversation
   376	
   377	Type or paste a message, get an answer. The exchange a first-time customer
   378	should be able to have, end to end, without help:
   379	
   380	> *What have you got?* → *What does a Margherita cost?* → *I'll take two of
   381	> those and a pasta* → *I'm a new customer, my name is …* → read-back →
   382	> confirm → order id and wait time.
   383	
   384	After a completed order, a new conversation can start immediately from the
   385	same page.
   386	
   387	### Header
   388	
   389	- **The pizzeria being ordered from, by name**, prominent and always visible.
   390	- **A selector to change pizzeria, filled from the API and from nowhere
   391	  else.** The list comes from `GET /pizzerias` at load time. No hardcoded
   392	  names, no bundled list, no fallback entry when the call fails — if it
   393	  fails, the page says the list is unavailable instead of offering a choice
   394	  it cannot honour. Each entry shows the name plus a short form of its UUID
   395	  so similar names can be told apart. Changing the selection starts a fresh
   396	  conversation for that pizzeria.
   397	- **A link to that pizzeria's dashboard**
   398	  (`{PIZZASIM_URL}/dashboard/pizzerias/{id}`), opening in a new tab. Without
   399	  it nobody can check whether the order arrived — and checking that is the
   400	  entire point of the product.
   401	- **Language: German or English**, switchable, applied to the agent's replies
   402	  and to speech in both directions.
   403	- **Start over**, clearing the session and the basket.
   404	
   405	### Footer
   406	
   407	- **The running version**, `x.y.z`, from `APP_VERSION`, raised on every
   408	  release: patch for fixes, minor for new behaviour, major for a break.
   409	  Without it nobody can tell which build is answering.
   410	- **The full pizzeria UUID**, selectable, for pasting into API calls.
   411	- **Connection state** for the ordering API and the model gateway.
   412	- **A link to the API documentation** (`{PIZZASIM_URL}/swagger.html`).
   413	
   414	### Every message gets an answer
   415	
   416	The invariant this channel stands on: **no sent message may end without either
   417	a rendered assistant reply or a rendered error.** Never a silent failure,
   418	never an indicator that stops with nothing after it.
   419	
   420	- The moment a message is sent, the UI shows the agent is working.
   421	- Intermediate steps render as they stream — which tool was called and what it
   422	  returned — visually distinct from the assistant's words. A stream whose tool
   423	  events the page discards is a defect: the customer sees a frozen screen
   424	  while the agent works normally.
   425	- If the stream ends without a final assistant message, the UI says so.
   426	- If the request errors, times out, or the connection drops, the UI says which
   427	  happened and offers to resend.
   428	- Errors in the customer's language, in plain words. No status codes, no
   429	  tracebacks, no raw JSON.
   430	
   431	### The order on screen
   432	
   433	- The current basket is visible, with quantities and what it comes to. The
   434	  code owns the order; the customer must see what the code holds.
   435	- The read-back is visually distinct and carries an explicit confirm control.
   436	  Confirmation is an action the customer takes, not a word the agent claims to
   437	  have heard.
   438	- On success: the order id, readable, and the wait in minutes.
   439	- After submission the basket is locked and shown as submitted. Nothing on the
   440	  page can modify or resubmit it.
   441	
   442	---
   443	
   444	## Speech
   445	
   446	Speech is an input and an output method on the web channel, served by a
   447	**self-hosted speech service**: CPU-only, in its own container, reached over
   448	plain HTTP with an OpenAI-compatible surface.
   449	
   450	| Direction | Endpoint | Payload |
   451	|---|---|---|
   452	| STT | `POST {SPEECH_URL}/v1/audio/transcriptions` | multipart audio + model + language |
   453	| TTS | `POST {SPEECH_URL}/v1/audio/speech` | JSON: model, voice, input text → audio |
   454	
   455	- **The speech service is the only speech path.** No external speech
   456	  provider, no hosted realtime framework, no audio through the LLM gateway —
   457	  that gateway carries chat completions only.
   458	- **The browser captures and plays audio; it does not recognise or synthesise
   459	  it.** Capture via `getUserMedia` and `MediaRecorder`, playback via a plain
   460	  audio element — cross-browser and cross-platform: Firefox, Safari, Chrome,
   461	  on Linux, macOS and Windows alike.
   462	- **The browser speech APIs are forbidden.** `SpeechRecognition` and
   463	  `speechSynthesis` tied the previous implementation to a single browser
   464	  vendor and sent customer audio to a third party. The self-hosted service
   465	  exists to replace them.
   466	- **Nothing about the speech stack is written into source.** Base URL, models
   467	  and voice come from the environment, exactly like the chat model; the
   468	  language sent with STT/TTS requests is the session language (see
   469	  *Language authority* under Conversation policy), not a separate config.
   470	- **Request/response, not streaming.** Record, upload, transcript back.
   471	  Latency is visible and acceptable; do not build partial results, barge-in
   472	  or turn detection on top — this transport cannot do them, and pretending
   473	  otherwise produces a broken feel.
   474	- **Push-to-talk.** The microphone starts and stops on the customer's action,
   475	  never listens continuously. Recording state is visible at all times.
   476	- **Synthesis is optional and off by default**, toggled by the customer,
   477	  applied only to the final assistant message.
   478	- **Speech is never required.** With `SPEECH_URL` unset or the service down,
   479	  microphone and speaker toggle are not rendered and the text UI is fully
   480	  usable. A speech failure is never an order failure.
   481	- **Speech shortens answers, it does not change them.** Same core, same
   482	  tools, same state machine. When a reply will be spoken: at most three menu
   483	  items plus an invitation, times in minutes, order id read in groups.
   484	- **Confirm the name.** Transcription errors on names are the expensive
   485	  failure: a misheard name silently creates a customer nobody will find
   486	  again. Read the name back before submitting.
   487	
   488	---
   489	
   490	## Error handling
   491	
   492	Every case below needs a test and a phrasing.
   493	
   494	| Situation | Code does | Customer sees/hears |
   495	|---|---|---|
   496	| Gateway timeout | one retry, then abort turn | plain apology, offer to resend |
   497	| `401`/`403` from PizzaSim | abort, log, do not retry | "I can't reach the kitchen system right now" |
   498	| `404` on the preselected `PIZZERIA_ID` | fail at startup, not mid-call | — (process refuses to start) |
   499	| Runtime pizzeria selection invalid/gone | session error, refresh the selector; process stays up | "that pizzeria isn't available right now" |
   500	| `422` validation | surface field, keep basket | targeted question about the offending item |
   501	| `5xx` on submit | **no blind retry** | "I'm not sure that went through — let me check" |
   502	| Timeout on submit | mark `UNKNOWN`; shortlist via `GET /pizzerias/{id}/orders`, verify items via `GET /pizzerias/{id}/orders/{order_id}` before any retry | as above |
   503	| Unknown item code | `unknown_item` + candidates | "I have Margherita or Marinara — which one?" |
   504	| Empty basket at submit | reject transition | "What can I get you?" |
   505	| Menu fetch fails at start | fail fast | "We're not taking orders right now" |
   506	| Pizzeria list fetch fails | no selector, say so | list unavailable — no fallback entry |
   507	| Speech service down | hide speech controls | text UI unaffected |
   508	
   509	The submit-timeout case is the one that matters: a blind retry doubles a real
   510	order. Recovery: shortlist candidates on the pizzeria's order list, then
   511	verify the candidate's items via `GET /pizzerias/{id}/orders/{order_id}` —
   512	only a verified match is adopted, anything else allows exactly one retry. If
   513	list or detail lookup fails, tell the customer honestly.
   514	
   515	---
   516	
   517	## Anti-patterns — explicitly forbidden
   518	
   519	Each of these was present in a previous implementation. None is a matter of
   520	taste.

exec
/bin/bash -lc "nl -ba channels/web.py | sed -n '1,240p'" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 109ms:
     1	"""FastAPI web channel on port 8888. Same core, zero order logic here.
     2	
     3	Streams the agent's intermediate steps as newline-delimited JSON and
     4	proxies the optional self-hosted speech service (STT/TTS). If SPEECH_URL is
     5	unset or the service doesn't answer at startup, speech endpoints return 404
     6	and the UI renders text-only.
     7	
     8	Run:  python -m channels.web
     9	"""
    10	from __future__ import annotations
    11	
    12	import json
    13	import queue
    14	import sys
    15	import threading
    16	from pathlib import Path
    17	
    18	import httpx
    19	import uvicorn
    20	from fastapi import FastAPI, HTTPException, UploadFile
    21	from fastapi.responses import FileResponse, Response, StreamingResponse
    22	from fastapi.staticfiles import StaticFiles
    23	
    24	from core.agent import Agent, AgentConfig, Session, startup
    25	from core.menu import Menu
    26	from core.pizzasim import ConfigError, PizzaSimError, optional_env
    27	
    28	STATIC = Path(__file__).resolve().parent / "static"
    29	app = FastAPI(title="PizzaSim ordering agent")
    30	
    31	
    32	class Speech:
    33	    """Config + probe for the self-hosted speech container. All-or-nothing:
    34	    enabled only if SPEECH_URL is set, answers, and models are configured."""
    35	
    36	    def __init__(self):
    37	        self.url = optional_env("SPEECH_URL")
    38	        self.stt_model = optional_env("SPEECH_STT_MODEL")
    39	        self.tts_model = optional_env("SPEECH_TTS_MODEL")
    40	        self.voice = optional_env("SPEECH_TTS_VOICE")
    41	        self.enabled = False
    42	        if self.url and self.stt_model and self.tts_model and self.voice:
    43	            try:
    44	                httpx.get(f"{self.url.rstrip('/')}/v1/models",
    45	                          timeout=3.0).raise_for_status()
    46	                self.enabled = True
    47	            except httpx.HTTPError:
    48	                print("speech service not answering — text-only mode",
    49	                      file=sys.stderr)
    50	
    51	
    52	@app.on_event("startup")
    53	def boot() -> None:
    54	    try:
    55	        config = AgentConfig.from_env()
    56	        client, pizzeria_name, _menu = startup(config)
    57	    except (ConfigError, ValueError) as exc:
    58	        print(f"Configuration error: {exc}", file=sys.stderr)
    59	        raise SystemExit(1)
    60	    except PizzaSimError as exc:
    61	        print(f"Startup check against PizzaSim failed: {exc}\n"
    62	              "We're not taking orders right now.", file=sys.stderr)
    63	        raise SystemExit(1)
    64	    app.state.config = config
    65	    app.state.client = client
    66	    app.state.pizzeria_name = pizzeria_name
    67	    app.state.agent = Agent(config, client)
    68	    app.state.sessions = {}
    69	    app.state.locks = {}  # one Lock per session: turns are serialized
    70	    app.state.speech = Speech()
    71	
    72	
    73	@app.get("/")
    74	def index():
    75	    return FileResponse(STATIC / "index.html")
    76	
    77	
    78	@app.get("/config")
    79	def ui_config():
    80	    # Contract per plan: speech flag + pizzeria display name. The customer
    81	    # must see which pizzeria they are ordering at.
    82	    return {"speech": app.state.speech.enabled,
    83	            "pizzeria": app.state.pizzeria_name}
    84	
    85	
    86	def _get_session(session_id: str) -> Session:
    87	    sessions = app.state.sessions
    88	    if session_id not in sessions:
    89	        # Fresh immutable menu snapshot per session (SPEC invariant 5).
    90	        try:
    91	            menu = Menu(app.state.client.get_menu())
    92	        except PizzaSimError:
    93	            raise HTTPException(503, "We're not taking orders right now.")
    94	        sessions[session_id] = Session.create(
    95	            app.state.config, menu, app.state.pizzeria_name)
    96	    return sessions[session_id]
    97	
    98	
    99	@app.post("/chat")
   100	async def chat(body: dict):
   101	    session_id = str(body.get("session_id") or "")
   102	    if not session_id:
   103	        raise HTTPException(422, "session_id required")
   104	    text = body.get("text")  # None → opening turn, agent greets
   105	    if text is not None and not str(text).strip():
   106	        raise HTTPException(422, "text must not be empty")
   107	    session = _get_session(session_id)
   108	    lock = app.state.locks.setdefault(session_id, threading.Lock())
   109	    if not lock.acquire(blocking=False):
   110	        # One Order per conversation means one turn at a time: overlapping
   111	        # requests would interleave mutations and break the revision-bound
   112	        # confirmation guarantees.
   113	        raise HTTPException(409, "a turn is already in progress")
   114	
   115	    events: queue.Queue = queue.Queue()
   116	
   117	    def run() -> None:
   118	        try:
   119	            app.state.agent.run_turn(session, text, events.put)
   120	        finally:
   121	            events.put({"type": "done",
   122	                        "state": session.order.snapshot()})
   123	            events.put(None)
   124	            lock.release()
   125	
   126	    threading.Thread(target=run, daemon=True).start()
   127	
   128	    def ndjson():
   129	        while (event := events.get()) is not None:
   130	            yield json.dumps(event, ensure_ascii=False) + "\n"
   131	
   132	    return StreamingResponse(ndjson(), media_type="application/x-ndjson")
   133	
   134	
   135	def _speech() -> Speech:
   136	    speech = app.state.speech
   137	    if not speech.enabled:
   138	        raise HTTPException(404, "speech is not available")
   139	    return speech
   140	
   141	
   142	@app.post("/speech/stt")
   143	async def stt(audio: UploadFile):
   144	    speech = _speech()
   145	    files = {"file": (audio.filename or "audio.webm", await audio.read(),
   146	                      audio.content_type or "audio/webm")}
   147	    data = {"model": speech.stt_model,
   148	            "language": app.state.config.lang}  # STT hint only
   149	    try:
   150	        response = httpx.post(
   151	            f"{speech.url.rstrip('/')}/v1/audio/transcriptions",
   152	            files=files, data=data, timeout=60.0)
   153	        response.raise_for_status()
   154	    except httpx.HTTPError:
   155	        raise HTTPException(502, "speech service unavailable")
   156	    return {"text": response.json().get("text", "")}
   157	
   158	
   159	@app.post("/speech/tts")
   160	async def tts(body: dict):
   161	    speech = _speech()
   162	    text = str(body.get("text") or "")
   163	    if not text:
   164	        raise HTTPException(422, "text required")
   165	    try:
   166	        response = httpx.post(
   167	            f"{speech.url.rstrip('/')}/v1/audio/speech",
   168	            json={"model": speech.tts_model, "voice": speech.voice,
   169	                  "input": text},
   170	            timeout=60.0)
   171	        response.raise_for_status()
   172	    except httpx.HTTPError:
   173	        raise HTTPException(502, "speech service unavailable")
   174	    return Response(response.content,
   175	                    media_type=response.headers.get("content-type",
   176	                                                    "audio/mpeg"))
   177	
   178	
   179	app.mount("/static", StaticFiles(directory=STATIC), name="static")
   180	
   181	
   182	if __name__ == "__main__":
   183	    uvicorn.run(app, host="127.0.0.1", port=8888)

codex
`PLAN.md` is close, but not approvable as written. It captures the main retrofit shape and correctly recognizes that the web layer is effectively a rewrite, but it still leaves several spec-critical gaps an implementer could exploit.

SCORES (1-5 each, 5 = best):
completeness: 4
correctness: 3
error_handling: 3
simplicity: 4
spec_compliance: 3
TOTAL: 17/25
VERDICT: CHANGES_REQUIRED
ISSUES: (max 5 bullets, concrete and actionable, empty if approved)
- `PLAN.md:190-199` says all notices are in the session language, but `SPEC.md:426-429` requires request errors in the customer's language, and `SPEC.md:346-347` makes the latest customer message authoritative for replies. Define how the web/UI layer tracks last-user language separately from `session.lang`, and test resend/error notices against that rule.
- `PLAN.md:155-157` and `210-214` cover invalid runtime pizzeria selection as a `409`, but omit the spec-required selector refresh path from `SPEC.md:499` and the header contract in `SPEC.md:390-396`. The plan must say how the UI refreshes the live `/pizzerias` list when a selected tenant is gone and how that is tested.
- `PLAN.md:246-247` reduces speech verification to “STT language follows the session language”, but `SPEC.md:468-483` also requires TTS language from the session language, synthesis off by default, final-message-only playback, and the spoken-answer shortening policy. Add explicit implementation and verification coverage for those behaviors.
- `PLAN.md:206-216` treats the old error table as carried over, but the v3 web contract adds new customer-visible phrasing obligations. The plan needs explicit web-surface coverage for unchanged rows that now matter in the browser too: `401/403`, `422`, submit `5xx`/timeout-unknown, and empty-basket submit, with plain-language rendered outcomes rather than only tool-level tests.
- `PLAN.md:129-140` leaves the failed confirm path underspecified: stale/wrong-state confirm is shown as a UI notice, but it is not stated whether that failed `confirm_order` attempt is appended/logged in `session.messages` the same way as the success path. Define the exact event/history semantics for both success and failure so condition 3 remains a single core path with consistent model context.
tokens used
78,800
`PLAN.md` is close, but not approvable as written. It captures the main retrofit shape and correctly recognizes that the web layer is effectively a rewrite, but it still leaves several spec-critical gaps an implementer could exploit.

SCORES (1-5 each, 5 = best):
completeness: 4
correctness: 3
error_handling: 3
simplicity: 4
spec_compliance: 3
TOTAL: 17/25
VERDICT: CHANGES_REQUIRED
ISSUES: (max 5 bullets, concrete and actionable, empty if approved)
- `PLAN.md:190-199` says all notices are in the session language, but `SPEC.md:426-429` requires request errors in the customer's language, and `SPEC.md:346-347` makes the latest customer message authoritative for replies. Define how the web/UI layer tracks last-user language separately from `session.lang`, and test resend/error notices against that rule.
- `PLAN.md:155-157` and `210-214` cover invalid runtime pizzeria selection as a `409`, but omit the spec-required selector refresh path from `SPEC.md:499` and the header contract in `SPEC.md:390-396`. The plan must say how the UI refreshes the live `/pizzerias` list when a selected tenant is gone and how that is tested.
- `PLAN.md:246-247` reduces speech verification to “STT language follows the session language”, but `SPEC.md:468-483` also requires TTS language from the session language, synthesis off by default, final-message-only playback, and the spoken-answer shortening policy. Add explicit implementation and verification coverage for those behaviors.
- `PLAN.md:206-216` treats the old error table as carried over, but the v3 web contract adds new customer-visible phrasing obligations. The plan needs explicit web-surface coverage for unchanged rows that now matter in the browser too: `401/403`, `422`, submit `5xx`/timeout-unknown, and empty-basket submit, with plain-language rendered outcomes rather than only tool-level tests.
- `PLAN.md:129-140` leaves the failed confirm path underspecified: stale/wrong-state confirm is shown as a UI notice, but it is not stated whether that failed `confirm_order` attempt is appended/logged in `session.messages` the same way as the success path. Define the exact event/history semantics for both success and failure so condition 3 remains a single core path with consistent model context.
