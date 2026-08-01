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
I’ve loaded the required process skill. Next I’m enumerating the repo, the review artifacts, and the relevant git history so each claim is checked against primary evidence rather than the implementer’s summary.
exec
/bin/bash -lc 'pwd && rg --files .' in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc 'git log --oneline --decorate --graph --all -n 40' in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc 'git status --short' in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 139ms:
?? reviews/round9-audit-grill.md

 succeeded in 251ms:
/home/rob/bpm-pizza-vibecoding-solution
./requirements.txt
./SPEC_20260801.md
./README.md
./SPEC.md
./initial_prompt.md
./PLAN.md
./core/tools.py
./core/order.py
./core/agent.py
./core/pizzasim.py
./core/menu.py
./core/__init__.py
./core/state.py
./tests/__init__.py
./tests/test_tools.py
./tests/test_state.py
./tests/test_transcripts.py
./tests/fixtures/menu.json
./tests/fixtures/order_created.json
./tests/fixtures/pizzerias.json
./tests/fixtures/orders_list.json
./tests/fixtures/location.json
./tests/fixtures/error_422.json
./tests/transcripts/unknown_item.json
./tests/transcripts/mind_change.json
./tests/transcripts/submit_timeout.json
./tests/transcripts/happy_path.json
./tests/transcripts/correction.json
./decisions/qa.md
./prompts/system.de.md
./reviews/round9-audit-grill.md
./reviews/round4-impl.md
./prompts/system.en.md
./reviews/round3-plan.md
./reviews/scores.md
./reviews/round8-hotfix.md
./reviews/round6-impl.md
./reviews/round5-impl.md
./reviews/round7-hotfix.md
./reviews/round2-plan.md
./reviews/round1-plan.md
./channels/cli.py
./channels/web.py
./channels/__init__.py
./channels/static/index.html
./channels/static/style.css
./channels/static/app.js

 succeeded in 189ms:
* bb8a00c (HEAD -> main) New SPEC v2 (web channel section, multi-pizzeria, prices, APP_VERSION); restore verified contract facts + dashboard/docs paths
* 36131ca Hotfix reviews round 7-8: APPROVED 24/25 after browser-verified fix
* 2ce8431 Hotfix review follow-up: TTS available without mic support
* 0580866 Hotfix: end-user browser path over plain HTTP
* 4ce7523 Implementation review round 3: APPROVED 24/25
* 49b0fa3 Apply impl review round 2 findings; new SPEC acceptance test implemented
* 7f2e501 Apply implementation review round 1 findings
* e6e237d CLI + web channels, static UI with push-to-talk speech, README, scaffold
* 635b6b8 Agent loop, prompts, five golden transcripts
* 0ce98c6 Menu validation, PizzaSim client, tool dispatch + fixture tests
* f670920 Core order model + state machine, exhaustive unit tests
* a412582 Plan review round 3: APPROVED 24/25
* 4776e3c Apply plan review round 2 findings; record oracle decision
* a133c09 Apply plan review round 1 findings, capture review + scores
* 941b474 Add PLAN.md (stage 1, pre-review)
* 724b6c0 Answer open contract questions against live API
* 951e541 Add SPEC.md and initial prompt, drop pizzaspec.md
* 54697a0 (origin/main, origin/HEAD) Reset repo for vibecoding rebuild: remove legacy app, add pizzaspec.md
* bb0b906 (tag: pre-spec-rebuild) Bump version to v1.4
* 2a1827f Add pizzeria-specific dashboard link
* 1d45f6b Switch API calls to curl, show UUIDs in dropdown and footer
* 42d7819 Bump version to v1.3
* 3d95fe6 Dynamische Pizzerien von API laden
* 78476f6 Fix critical bugs: add missing import, fix async generator, improve order parsing
* 5d8e2fb Initial commit with security fixes applied

exec
/bin/bash -lc "for f in reviews/round1-plan.md reviews/round2-plan.md reviews/round3-plan.md reviews/round4-impl.md reviews/round5-impl.md reviews/round6-impl.md reviews/round7-hotfix.md reviews/round8-hotfix.md decisions/qa.md PLAN.md README.md; do echo '---'\" "'$f"; sed -n '"'1,220p' \""'$f"; done' in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,220p' reviews/scores.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc 'git show HEAD -- SPEC.md' in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc 'git show HEAD''^:SPEC.md | sed -n '"'1,260p'" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 371ms:
--- reviews/round1-plan.md
OpenAI Codex v0.143.0
--------
workdir: /home/rob/bpm-pizza-vibecoding-solution
model: gpt-5.4
provider: openai
approval: never
sandbox: read-only
reasoning effort: medium
reasoning summaries: none
session id: 019fb8ea-5fd8-7353-9d63-a631230c462b
--------
user
You are an independent reviewer for the repository in the current working directory. You are read-only; you never write code. You play two roles in one pass:
1. Devil's advocate: attack the plan — gaps, wrong assumptions, missing error cases, spec violations.
2. Judge: score against the fixed rubric.

Task: Read SPEC.md (the source of truth) and PLAN.md (the stage-1 implementation plan under review). Judge whether PLAN.md is a complete, correct, spec-compliant plan such that implementing exactly it satisfies SPEC.md. The "Contract facts" section in SPEC.md was verified against the live API and is trustworthy.

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
I’m reviewing `SPEC.md` and `PLAN.md` as a read-only pass, with the spec treated as source of truth. I’ll read the required skill instructions first, then inspect both files and judge whether the plan is sufficient to satisfy the spec exactly.
exec
/bin/bash -lc "printf '--- SPEC ---\\n'; sed -n '1,260p' SPEC.md; printf '\\n--- PLAN ---\\n'; sed -n '1,260p' PLAN.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,220p' /home/rob/.agents/skills/using-superpowers/SKILL.md" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 342ms:
/bin/bash: line 1: printf: --: invalid option
printf: usage: printf [-v var] format [arguments]
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
--- reviews/round2-plan.md
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
--- reviews/round3-plan.md
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
--- reviews/round4-impl.md
OpenAI Codex v0.143.0
--------
workdir: /home/rob/bpm-pizza-vibecoding-solution
model: gpt-5.4
provider: openai
approval: never
sandbox: read-only
reasoning effort: medium
reasoning summaries: none
session id: 019fb8fd-0481-7041-b49f-c9ab1a56622b
--------
user
You are an independent reviewer for the repository in the current working directory. You are read-only; you never write code. Two roles in one pass:
1. Devil's advocate: attack the implementation — bugs, gaps, missing error cases, spec violations, divergence from the approved plan.
2. Judge: score against the fixed rubric.

Task: Review the IMPLEMENTATION (stage 2) against SPEC.md (source of truth) and PLAN.md (the approved stage-1 plan, 24/25 APPROVED in reviews/round3-plan.md). The implementation is: core/ (order, state, menu, pizzasim, tools, agent), channels/ (cli.py, web.py, static/), prompts/, tests/ (state, tools, transcripts + fixtures), README.md, .env.example, requirements.txt.

Facts you cannot observe from the files, all demonstrated live before this review: the full deterministic suite passes (67 passed, 1 skipped opt-in live test); the web channel started with SPEECH_URL unset (speech:false, mic not rendered) and placed a real order end to end via the real gateway (read_back -> confirm_order(revision) -> submit_order -> order_id 3fe1deaa-... visible in the pizzeria's order list); a missing required env var exits before the first turn naming the variable and file. You may run the test suite yourself if your sandbox permits; otherwise judge from the code.

Scope notes: tests/fixtures/*.json are recorded real API responses (UUIDs in them are recorded data, not hardcoded config). The venv/ and logs/ directories are gitignored runtime artifacts, out of scope.

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
Using `using-superpowers` first to load the required workflow, then I’ll inspect `SPEC.md`, `PLAN.md`, and the implementation files to review against the approved plan and rubric.
exec
/bin/bash -lc "sed -n '1,220p' /home/rob/.agents/skills/using-superpowers/SKILL.md" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 125ms:
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
I’m pulling the Codex-specific skill instructions next, then I’ll read the spec, approved plan, and the review target files in parallel.
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

exec
/bin/bash -lc "pwd && rg --files -g 'SPEC.md' -g 'PLAN.md' -g 'README.md' -g '.env.example' -g 'requirements.txt' -g 'reviews/**' -g 'core/**' -g 'channels/**' -g 'prompts/**' -g 'tests/**'" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 130ms:
requirements.txt
PLAN.md
.env.example
README.md
SPEC.md
core/tools.py
core/order.py
core/__pycache__/menu.cpython-313.pyc
core/__pycache__/agent.cpython-313.pyc
core/__pycache__/pizzasim.cpython-313.pyc
core/__pycache__/tools.cpython-313.pyc
core/__pycache__/state.cpython-313.pyc
core/__pycache__/order.cpython-313.pyc
core/__pycache__/__init__.cpython-313.pyc
core/agent.py
core/pizzasim.py
core/menu.py
core/__init__.py
core/state.py
channels/__pycache__/web.cpython-313.pyc
channels/__pycache__/__init__.cpython-313.pyc
channels/__pycache__/cli.cpython-313.pyc
channels/__init__.py
channels/web.py
channels/cli.py
channels/static/index.html
channels/static/style.css
channels/static/app.js
prompts/system.de.md
prompts/system.en.md
tests/__pycache__/test_tools.cpython-313-pytest-9.1.1.pyc
tests/__pycache__/__init__.cpython-313.pyc
tests/__pycache__/test_transcripts.cpython-313-pytest-9.1.1.pyc
tests/__pycache__/test_state.cpython-313-pytest-9.1.1.pyc
tests/__init__.py
tests/test_tools.py
tests/test_state.py
tests/test_transcripts.py
tests/fixtures/menu.json
tests/fixtures/order_created.json
tests/fixtures/pizzerias.json
tests/fixtures/orders_list.json
tests/fixtures/location.json
tests/fixtures/error_422.json
tests/transcripts/unknown_item.json
tests/transcripts/mind_change.json
tests/transcripts/submit_timeout.json
tests/transcripts/happy_path.json
tests/transcripts/correction.json
reviews/scores.md
reviews/round1-plan.md
reviews/round4-impl.md
reviews/round3-plan.md
reviews/round2-plan.md

Setting a short review workflow: read the source-of-truth docs first, inspect implementation areas against them, then produce findings and rubric scores.
  → Read SPEC.md, PLAN.md, and approved-plan review context
  • Inspect implementation files and tests against spec/plan requirements
  • Draft findings, rubric scores, and verdict
exec
/bin/bash -lc "sed -n '1,260p' SPEC.md" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 0ms:
# PizzaSim Ordering Agent — Specification

> Hand this to a coding agent as the entire task:
> `FOLLOW INSTRUCTIONS PRECISELY AT "SPEC.MD"`.
> This file is the source of truth for what the agent is. Everything else in the
> repo — code, tests, prompts, tickets — derives from it.

--- reviews/round5-impl.md
OpenAI Codex v0.143.0
--------
workdir: /home/rob/bpm-pizza-vibecoding-solution
model: gpt-5.4
provider: openai
approval: never
sandbox: read-only
reasoning effort: medium
reasoning summaries: none
session id: 019fb900-c8f4-7e21-b2ec-38adbabbc704
--------
user
You are an independent reviewer for the repository in the current working directory. You are read-only; you never write code. Two roles in one pass:
1. Devil's advocate: attack the implementation — bugs, gaps, missing error cases, spec violations, divergence from the approved plan.
2. Judge: score against the fixed rubric.

Task: Review the IMPLEMENTATION (stage 2, round 2 of max 3) against SPEC.md (source of truth) and PLAN.md (the approved stage-1 plan; approved 24/25 in reviews/round3-plan.md, since updated only to document remove_item disambiguation semantics). Implementation: core/, channels/, prompts/, tests/, README.md, .env.example, requirements.txt.

Round 1 (stateless, reviews/round4-impl.md) required four changes; all were applied — verify in the files, do not take this on faith:
1. remove_item ambiguity with same (type, code) and different extras → deterministic semantics in core/state.py (no qty removes all matching lines; qty reduces the most recently added), documented in PLAN.md tool table, tested in tests/test_state.py (test_remove_without_qty_clears_all_variants, test_remove_with_qty_reduces_most_recent_variant). The spec fixes remove_item's parameters, so an extras parameter was not an option.
2. Speech probe now requires 2xx (raise_for_status) in channels/web.py.
3. Gateway timeout aligned to the plan's 30s in core/agent.py.
4. requirements.txt pinned to exact versions.

Facts you cannot observe from the files, all demonstrated live: the deterministic suite passes (69 passed, 1 skipped opt-in live test); the web channel started with SPEECH_URL unset (speech:false, mic not rendered) and placed a real order end to end via the real gateway (read_back -> confirm_order(revision) -> submit_order -> order_id 3fe1deaa-... visible in the pizzeria's order list, ETA converted to minutes, id read in groups); a missing required env var exits before the first turn naming the variable and file. Your sandbox may lack a writable temp dir for pytest; judge from the code plus this evidence if so.

Scope notes: tests/fixtures/*.json are recorded real API responses (UUIDs there are recorded data, not hardcoded config). venv/ and logs/ are gitignored runtime artifacts, out of scope.

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
I’m reviewing the implementation against `SPEC.md`, `PLAN.md`, and the round-1 review findings first, then I’ll inspect the implementation and tests to verify each claimed fix before scoring.
exec
/bin/bash -lc "sed -n '1,220p' /home/rob/.agents/skills/using-superpowers/SKILL.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc pwd in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 112ms:
/home/rob/bpm-pizza-vibecoding-solution

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
Using `using-superpowers` to select the required workflow, then I’m moving into the repo documents and target files for the actual review.
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

exec
/bin/bash -lc "rg --files -g 'SPEC.md' -g 'PLAN.md' -g 'reviews/round3-plan.md' -g 'reviews/round4-impl.md' -g 'README.md' -g '.env.example' -g 'requirements.txt' -g 'core/**' -g 'channels/**' -g 'prompts/**' -g 'tests/**'" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 0ms:
requirements.txt
.env.example
PLAN.md
reviews/round4-impl.md
reviews/round3-plan.md
core/tools.py
README.md
core/order.py
SPEC.md
channels/web.py
channels/cli.py
channels/__pycache__/cli.cpython-313.pyc
channels/__init__.py
channels/__pycache__/__init__.cpython-313.pyc
core/menu.py
core/__init__.py
core/state.py
core/pizzasim.py
core/agent.py
channels/__pycache__/web.cpython-313.pyc
core/__pycache__/menu.cpython-313.pyc
core/__pycache__/agent.cpython-313.pyc
core/__pycache__/pizzasim.cpython-313.pyc
core/__pycache__/tools.cpython-313.pyc
core/__pycache__/state.cpython-313.pyc
core/__pycache__/order.cpython-313.pyc
core/__pycache__/__init__.cpython-313.pyc
prompts/system.en.md
prompts/system.de.md
channels/static/index.html
channels/static/style.css
channels/static/app.js
tests/test_transcripts.py
tests/test_tools.py
tests/test_state.py
tests/__init__.py
tests/__pycache__/test_tools.cpython-313-pytest-9.1.1.pyc
tests/__pycache__/__init__.cpython-313.pyc
tests/__pycache__/test_transcripts.cpython-313-pytest-9.1.1.pyc
tests/__pycache__/test_state.cpython-313-pytest-9.1.1.pyc
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

codex
I have the review surface. Next I’m checking the spec, approved plan, and prior round findings side by side, then I’ll trace the implementation and tests for conformance and regressions.
Reviewing implementation against spec, approved plan, and round-1 required fixes before issuing findings and rubric scores.
  → Read SPEC.md, PLAN.md, and prior review docs to extract required behavior and prior mandatory fixes
  • Inspect implementation files in core/, channels/, prompts/, README.md, .env.example, requirements.txt for compliance and regressions
  • Inspect tests for coverage of required behavior, especially round-1 fixes and spec-critical flows
--- reviews/round6-impl.md
OpenAI Codex v0.143.0
--------
workdir: /home/rob/bpm-pizza-vibecoding-solution
model: gpt-5.4
provider: openai
approval: never
sandbox: read-only
reasoning effort: medium
reasoning summaries: none
session id: 019fb907-23d4-7ff3-babf-cab4f0e1904f
--------
user
You are an independent reviewer for the repository in the current working directory. You are read-only; you never write code. Two roles in one pass:
1. Devil's advocate: attack the implementation — bugs, gaps, missing error cases, spec violations.
2. Judge: score against the fixed rubric.

Task: Review the IMPLEMENTATION (stage 2, round 3 of max 3) against SPEC.md (source of truth — note it now contains the operator-added "What done looks like" acceptance section) and PLAN.md (approved stage-1 plan, updated alongside). Implementation: core/, channels/, prompts/, tests/, README.md, .env.example, requirements.txt.

Round 2 (stateless, reviews/round5-impl.md) required four changes; all applied — verify in the files, do not take this on faith:
1. Mutations clear submit_unknown/submit_attempted_at (core/state.py _recompute); tested in tests/test_tools.py::test_mutation_after_submit_timeout_clears_recovery_state.
2. Web /chat serializes turns per session (lock; 409 when a turn is in flight) in channels/web.py.
3. Gateway-timeout and loop-guard apology paths emit assistant events (core/agent.py), so the web UI shows the apology and it is logged.
4. GET /config returns exactly {speech: bool}.
Additionally, per the updated SPEC: submit-timeout recovery now verifies the shortlisted candidate's items via GET /pizzerias/{id}/orders/{order_id} before adopting it (core/tools.py, tests test_recovery_rejects_candidate_with_different_items), and the opt-in live test is now the full acceptance test (tests/test_tools.py::test_live_acceptance) asserting order id, presence in the pizzeria's list, exact customer name, and exact items/quantities.

Facts you cannot observe from the files, all demonstrated live: deterministic suite passes (71 passed, 1 skipped); the live acceptance test PASSED against the real API (real order, read back via list + detail endpoints, exact match); the web channel with SPEECH_URL unset reported speech:false and placed a real order end to end via the real gateway (order 3fe1deaa-... under the configured pizzeria with exactly the read-back items — independently confirmed via the detail endpoint); a missing required env var exits before the first turn naming the variable and file. Your sandbox may lack a writable temp dir for pytest; judge from code plus this evidence if so.

Scope notes: tests/fixtures/*.json are recorded real API responses (UUIDs there are recorded data, not hardcoded config). venv/ and logs/ are gitignored runtime artifacts, out of scope. decisions/qa.md records oracle decisions.

Judging guidance: this is the final allowed round. Score the implementation that exists against SPEC.md; remaining nice-to-haves that a maintainer would file as minor follow-ups do not belong in a rejection.

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
Using `using-superpowers` first to load the session workflow, then I’ll inspect `SPEC.md`, `PLAN.md`, and the implementation files directly and verify the round-2 fixes in code rather than by claim.
exec
/bin/bash -lc "rg --files /home/rob/bpm-pizza-vibecoding-solution | rg '"'^(SPEC'"\\.md|PLAN\\.md|README\\.md|requirements\\.txt|\\.env\\.example|core/|channels/|prompts/|tests/|decisions/qa\\.md)'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,220p' /home/rob/.agents/skills/using-superpowers/SKILL.md" in /home/rob/bpm-pizza-vibecoding-solution
 exited 1 in 104ms:
 succeeded in 109ms:
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
I’ve loaded the base workflow. Next I’m reading the Codex-specific skill instructions, then I’ll open the spec, plan, and the exact implementation files under review.
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

exec
/bin/bash -lc "rg --files . | rg '"'^(SPEC'"\\.md|PLAN\\.md|README\\.md|requirements\\.txt|\\.env\\.example|core/|channels/|prompts/|tests/|decisions/qa\\.md)'" in /home/rob/bpm-pizza-vibecoding-solution
 exited 1 in 0ms:
codex
The repository scan needs a broader pass; I’m switching to a direct file listing and then reading the review targets and decision notes in parallel.
exec
/bin/bash -lc "sed -n '1,220p' decisions/qa.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' SPEC.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' PLAN.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc 'rg --files .' in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 429ms:
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
--- reviews/round7-hotfix.md
OpenAI Codex v0.143.0
--------
workdir: /home/rob/bpm-pizza-vibecoding-solution
model: gpt-5.4
provider: openai
approval: never
sandbox: read-only
reasoning effort: medium
reasoning summaries: none
session id: 019fbbfc-e3c5-7330-8e4f-ec9044da3cf0
--------
user
You are an independent reviewer for the repository in the current working directory. Read-only; you never write code. Devil's advocate + judge in one pass.

Context: The implementation was APPROVED 24/25 in reviews/round6-impl.md. After approval, a production defect surfaced: the web UI, served over plain HTTP on a public IP (not localhost), was completely dead in the browser — crypto.randomUUID() requires a secure context, so app.js crashed at load: no greeting, no working send button. The operator also required the pizzeria display name to be visible to the end user.

Task: Review the hotfix commit HEAD (0580866, "Hotfix: end-user browser path over plain HTTP") — run `git show HEAD` or read the changed files: channels/static/app.js (session id fallback via crypto.getRandomValues; mic additionally gated on navigator.mediaDevices; title set from /config), channels/web.py (/config returns {speech, pizzeria}), PLAN.md (contract line updated). Judge: (a) does the fix actually solve the insecure-context failure, (b) does it introduce new problems (security, contract drift, spec violations), (c) is anything else in the static UI still secure-context-dependent that would break the same way?

Output MUST end with exactly this block:
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
Using `using-superpowers` first, then I’ll inspect the hotfix diff and the affected files to judge the fix against the reported production failure and the UI contract.
exec
/bin/bash -lc "sed -n '1,240p' channels/web.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,220p' PLAN.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "git show --stat --oneline HEAD && printf '\\n---DIFF---\\n' && git show --format=medium --no-ext-diff --patch HEAD -- channels/static/app.js channels/web.py PLAN.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,220p' /home/rob/.agents/skills/using-superpowers/SKILL.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' channels/static/app.js" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 574ms:
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
--- reviews/round8-hotfix.md
OpenAI Codex v0.143.0
--------
workdir: /home/rob/bpm-pizza-vibecoding-solution
model: gpt-5.4
provider: openai
approval: never
sandbox: read-only
reasoning effort: medium
reasoning summaries: none
session id: 019fbbff-3015-70c2-917b-5cffe233985f
--------
user
You are an independent reviewer for the repository in the current working directory. Read-only; you never write code. Devil's advocate + judge in one pass.

Context: reviews/round7-hotfix.md (stateless previous round) reviewed the plain-HTTP hotfix and required exactly one change: split the speech capability flags so server-proxied TTS stays available from cfg.speech while only the mic button is gated on navigator.mediaDevices and MediaRecorder. That change is applied in commit HEAD (2ce8431) — verify in channels/static/app.js, do not take it on faith.

Additional live evidence since round 7: a real headless Chromium was driven against the public URL http://<host>:8888 with window.isSecureContext === false. Results: zero page errors; greeting rendered; pizzeria name shown in the header; mic and TTS controls hidden (speech disabled in this deployment); a typed customer message produced a correct menu answer with the intermediate-steps block visible. Full-page screenshot captured.

Review the current state of the hotfix (both commits 0580866 + 2ce8431 relative to the approved round-6 state).

Output MUST end with exactly this block:
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
I’m reviewing the current hotfix as a read-only code review, starting by loading the required skill instructions and then checking the referenced review note, the target commit, and the relevant files in `HEAD`.
exec
/bin/bash -lc "sed -n '1,220p' /home/rob/.agents/skills/using-superpowers/SKILL.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "git rev-parse --verify HEAD && git rev-parse --verify 0580866 && git rev-parse --verify 2ce8431 && sed -n '1,260p' reviews/round7-hotfix.md && sed -n '1,260p' channels/static/app.js" in /home/rob/bpm-pizza-vibecoding-solution
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

 succeeded in 102ms:
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
--- decisions/qa.md
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
--- PLAN.md
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
`submit_unknown` and first calls `list_orders()`, shortlisting orders with
our customer's `first_name` and `created_at >= submit_attempted_at - 60`
(60s clock-skew allowance); the best candidate is then **verified via the
detail endpoint** (`GET /pizzerias/{id}/orders/{order_id}`, which carries
items) — adopted only if its items equal the basket exactly. Verified →
state `SUBMITTED` with the recovered id. Absent or different items →
exactly one real retry. List or detail call fails → error `submit_unknown`
with an honest message ("I'm not sure that went through — let me check"
phrasing); never a blind re-POST. Any basket/customer mutation clears
`submit_unknown` and `submit_attempted_at`: the correlation belongs to the
basket that was confirmed then, and a demoted order must POST fresh.

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
| `remove_item` | `{type: enum, code: str, qty: int ≥1 optional}` — the spec fixes these params, so when several lines share (type, code) with different extras: absent qty removes **all** matching lines, qty reduces the **most recently added** matching line (deterministic; the snapshot lets the model repair by remove + re-add) | `{"snapshot": SNAPSHOT}` |
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

--- README.md
# PizzaSim Ordering Agent

An ordering agent for the PizzaSim demo kitchen. The order is a state
machine owned by the code; the model only turns customer language into tool
calls. See <a href="SPEC.md">SPEC.md</a> for the full specification and
<a href="PLAN.md">PLAN.md</a> for the design.

## Setup

```bash
python3 -m venv venv
venv/bin/pip install -r requirements.txt
```

Configuration comes from the environment (or `~/.env`); every variable in
`.env.example` except the four `SPEECH_*` ones is required. The process
refuses to start when one is missing, naming the variable. No values are
ever printed or logged.

## CLI channel

```bash
venv/bin/python -m channels.cli            # plain chat
venv/bin/python -m channels.cli --verbose  # + tool calls and states
```

The agent greets first, in the language set by `PIZZERIA_LANG`, and answers
each turn in the language you used (German or English). End with Ctrl-D.

## Web channel

```bash
venv/bin/python -m channels.web
```

Then open <a href="http://127.0.0.1:8888" target="_blank">http://127.0.0.1:8888</a>.
The chat streams the agent's intermediate steps (tool calls, tool results)
as newline-delimited JSON; the UI shows them per turn under
"Zwischenschritte".

## Speech (web only, optional)

Set `SPEECH_URL`, `SPEECH_STT_MODEL`, `SPEECH_TTS_MODEL` and
`SPEECH_TTS_VOICE` to a self-hosted OpenAI-compatible speech service. The
mic button is push-to-talk (click to start, click to stop); the "read
aloud" toggle is off by default and speaks only final answers. With
`SPEECH_URL` unset — or the service down at startup — mic and toggle are
not rendered and the page is fully usable as text chat.

Manual speech checklist: dictate an order; dictate a name that needs
correcting (the agent repeats the name back before submitting); ask a menu
question; and one run with `SPEECH_URL` unset placing an order as text.

## Tests

```bash
venv/bin/python -m pytest tests/            # deterministic: no network, no LLM
PIZZA_LIVE_TEST=1 venv/bin/python -m pytest tests/test_tools.py -k live
```

The second command is the one opt-in smoke test that places a real order.

## Logs

One JSON line per event (user text, tool calls, tool results, state
transitions) in `logs/agent-<session>.jsonl`. Secrets never appear there.

 succeeded in 417ms:
# Review scores

## Round 1 — PLAN.md (reviews/round1-plan.md)

completeness: 4
correctness: 3
error_handling: 4
simplicity: 4
spec_compliance: 3
TOTAL: 18/25
VERDICT: CHANGES_REQUIRED

Findings applied: removed `./.env` fallback and `PIZZA_LOG_DIR`; tool
results restored to the spec's fixed contract; greeting language =
pizzeria-country startup constant with per-turn mirroring (no UI control);
single explicit startup sequence via `GET /pizzerias`; read_back/confirm
path tightened (read_back only in READY/CONFIRMED, confirm only in READY).

## Round 2 — PLAN.md (reviews/round2-plan.md)

completeness: 3
correctness: 3
error_handling: 4
simplicity: 4
spec_compliance: 2
TOTAL: 16/25
VERDICT: CHANGES_REQUIRED

Findings applied: exact per-tool success JSON with one fixed SNAPSHOT shape
embedded everywhere; eta_minutes test regression fixed to eta_seconds;
greeting language now required env var PIZZERIA_LANG (oracle decision in
decisions/qa.md); submit_attempted_at added as recovery correlation key
(with 60s skew allowance); lang removed from web /chat and /config, STT
hint = PIZZERIA_LANG only; per-session immutable menu snapshot defined via
a Session model.

## Round 3 — PLAN.md (reviews/round3-plan.md)

completeness: 5
correctness: 5
error_handling: 5
simplicity: 4
spec_compliance: 5
TOTAL: 24/25
VERDICT: APPROVED

## Round 4 — implementation (reviews/round4-impl.md)

completeness: 4
correctness: 3
error_handling: 4
simplicity: 4
spec_compliance: 3
TOTAL: 18/25
VERDICT: CHANGES_REQUIRED

Findings applied: remove_item now deterministic across same-(type,code)
lines with different extras (no qty = all matching lines, qty = most recent
line; two new tests; PLAN.md updated); speech probe requires 2xx via
raise_for_status; gateway timeout aligned to the plan's 30s; requirements
pinned to exact versions. Suite: 69 passed, 1 skipped.

## Round 5 — implementation (reviews/round5-impl.md)

completeness: 4
correctness: 3
error_handling: 3
simplicity: 4
spec_compliance: 3
TOTAL: 17/25
VERDICT: CHANGES_REQUIRED

Findings applied: mutations now clear submit_unknown/submit_attempted_at
(recovery correlation is void once the confirmed basket changes; tested);
web /chat serializes turns per session via a lock, concurrent request →
409; gateway-timeout and loop-guard apologies now emitted as assistant
events (visible in web UI and JSONL); /config reduced to the fixed
{speech: bool} contract.

Note: between rounds the operator updated SPEC.md ("What done looks like"
acceptance criterion; live smoke test upgraded to a full acceptance test).
Implemented: recovery now verifies candidate items via the newly probed
order-detail endpoint before adopting; the live test is now the full
acceptance test and passed against the real API.

## Round 6 — implementation (reviews/round6-impl.md)

completeness: 5
correctness: 5
error_handling: 5
simplicity: 4
spec_compliance: 5
TOTAL: 24/25
VERDICT: APPROVED

## Round 7 — hotfix (reviews/round7-hotfix.md)

completeness: 4
correctness: 4
error_handling: 3
simplicity: 4
spec_compliance: 3
TOTAL: 18/25
VERDICT: CHANGES_REQUIRED

Context: post-approval production defect — app.js dead over plain HTTP
(crypto.randomUUID needs a secure context), pizzeria name missing from the
UI. Finding applied: TTS stays available from cfg.speech; only the mic is
gated on navigator.mediaDevices + MediaRecorder.

## Round 8 — hotfix (reviews/round8-hotfix.md)

completeness: 5
correctness: 5
error_handling: 4
simplicity: 5
spec_compliance: 5
TOTAL: 24/25
VERDICT: APPROVED

Verified with a real headless Chromium against the public URL
(isSecureContext=false): no JS errors, greeting, pizzeria name in header,
typed order question answered, steps visible, speech controls hidden.

 succeeded in 499ms:
commit bb8a00c2aa04fa484cabcda80f35ca1dccee95fb
Author: Robert Kuhlig <16413104+Kuhlig@users.noreply.github.com>
Date:   Sat Aug 1 08:44:27 2026 +0200

    New SPEC v2 (web channel section, multi-pizzeria, prices, APP_VERSION); restore verified contract facts + dashboard/docs paths
    
    Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>

diff --git a/SPEC.md b/SPEC.md
index 37c8597..4446417 100644
--- a/SPEC.md
+++ b/SPEC.md
@@ -124,8 +124,12 @@ path — exists to prevent exactly one of those four.
   container over HTTP. See *Speech*.
 - **Languages:** German and English. The agent answers in the language the
   customer used, per turn, without being told to switch.
-- **Menu, cart, customer, submit.** The full happy path plus correction
-  ("no, make that three"), removal, and abandonment.
+- **Menu, prices, cart, customer, submit.** The full happy path plus correction
+  ("no, make that three"), removal, and abandonment. The customer can ask what
+  is on offer and what individual items cost, and can see what the basket comes
+  to before confirming.
+- **Several pizzerias.** The customer chooses which one they are ordering from,
+  and can change it. `PIZZERIA_ID` is the preselection, not a restriction.
 - **The success moment:** the order appears in the PizzaSim dashboard under the
   configured pizzeria, with the right customer, items and quantities.
 - **Deterministic tests** that run with no network and no LLM.
@@ -134,10 +138,10 @@ path — exists to prevent exactly one of those four.
 
 ### Out (explicitly)
 
-- Payment, pricing totals, delivery routing, ETA prediction of our own.
+- Payment and anything financial beyond showing prices the API supplies.
+- Delivery routing, or an ETA of our own invention.
 - Accounts, auth, sessions surviving a process restart.
 - Modifying or cancelling an order after it was submitted.
-- Switching pizzeria at runtime — one process serves one `PIZZERIA_ID`.
 - Any regex or keyword parser that produces an order without the model.
   See **Anti-patterns**; this is not a style preference, it is a hard ban.
 - Reading the whole menu aloud when the answer will be spoken.
@@ -156,7 +160,8 @@ never write to it, never create it, never print a value.
 | `LITELLM_PIZZA_KEY` | Bearer token for the gateway |
 | `PIZZASIM_URL` | PizzaSim API base URL |
 | `PIZZASIM_API_KEY` | Sent as header `X-API-Key` on protected routes |
-| `PIZZERIA_ID` | UUID of the pizzeria this process serves |
+| `PIZZERIA_ID` | UUID of the pizzeria preselected on first load |
+| `APP_VERSION` | Release version, `x.y.z`, shown in the footer |
 | `LITELLM_PIZZA_MODEL_1` | Model the ordering agent calls; required, no default in code |
 | `LITELLM_PIZZA_MODEL_2` | Second configured model, where the build uses one |
 
@@ -202,13 +207,14 @@ Facts that shape behaviour:
 - `POST` is **not idempotent**. A retry after a timeout can double the order.
   See **Error handling**.
 
-### Contract facts — verified against the live API (2026-07-31)
+### Contract facts — verified against the live API (2026-07-31/08-01)
 
-All seven former open questions were resolved by probing the live API
+All former open questions were resolved by probing the live API
 (`GET /menu`, `GET /pizzerias`, `POST /pizzerias/{id}/orders` — valid and
 invalid bodies —, `GET /pizzerias/{id}/orders`,
-`GET /pizzerias/{id}/orders/{order_id}`, `GET /location`). Facts below are
-from real responses, not documentation.
+`GET /pizzerias/{id}/orders/{order_id}`, `GET /location`, plus the dashboard
+and documentation pages). Facts below are from real responses, not
+documentation.
 
 1. **Order response field name: `order_id`.** A successful
    `POST /pizzerias/{id}/orders` returns
@@ -225,6 +231,8 @@ from real responses, not documentation.
    candidate's items against the basket before adopting it. The acceptance
    test asserts items and quantities through the same detail endpoint.
 3. **Menu item shape:** `{"code", "name", "base": [ingredients], "price"}`.
+   `price` is a number in euros (e.g. `8.5`) — the source for every price
+   answer and the basket total; no other financial data exists in the API.
    `name` is a single string (Italian proper names, identical in DE and EN) —
    there are no per-language names in the API; read-back uses `name` as-is in
    both languages. The menu response also carries a top-level `toppings[]`
@@ -247,6 +255,14 @@ from real responses, not documentation.
    returned `deliverable: true` — the check is a weak plausibility signal at
    best, which confirms the policy above: never tell the customer an address
    was verified.
+8. **The pizzeria dashboard** lives at
+   `{PIZZASIM_URL}/dashboard/pizzerias/{id}` (confirmed in the dashboard's
+   own routing code); the overview is `{PIZZASIM_URL}/dashboard`. The
+   header's dashboard link is derived from `PIZZASIM_URL` — nothing
+   hardcoded.
+9. **The API documentation** is served at `{PIZZASIM_URL}/swagger.html`
+   (HTTP 200); there is no `/docs` or `/openapi.json`. The footer's
+   documentation link is derived from `PIZZASIM_URL`.
 
 Additional verified fact: item `code`s are unique **per type**, not globally —
 `tonno` exists as both a pizza and a pasta. Validation and removal must always
@@ -333,6 +349,85 @@ do not paste this section into the prompt verbatim.
 
 ---
 
+## The web channel
+
+The web UI is where a stranger decides whether this thing works. Everything
+below is required, and each line is written so it can be checked by looking at
+the page.
+
+### The conversation
+
+Type or paste a message, get an answer. The exchange a first-time customer
+should be able to have, end to end, without help:
+
+> *What have you got?* → *What does a Margherita cost?* → *I'll take two of
+> those and a pasta* → *I'm a new customer, my name is …* → read-back → confirm
+> → order id and wait time.
+
+- Prices come from the menu the API returns. Asking what something costs is a
+  normal question, not an edge case, and so is asking what the basket comes to.
+- After a completed order, a new conversation can be started immediately from
+  the same page.
+
+### Header
+
+- **The pizzeria being ordered from, by name**, prominent and always visible.
+- **A selector to change pizzeria, filled from the API and from nowhere else.**
+  The list comes from `GET /pizzerias` at load time. No hardcoded names, no
+  bundled list, no fallback entry when the call fails — if the call fails the
+  page says the pizzeria list is unavailable and does not offer a choice it
+  cannot honour. Each entry shows the name together with a short form of its
+  UUID, so two similar names can be told apart. Changing the selection starts a
+  fresh conversation for that pizzeria; a basket never crosses a tenant
+  boundary.
+- **A link to that pizzeria's dashboard**, opening in a new tab, pointing at the
+  dashboard path for the selected pizzeria id. Without it nobody can check
+  whether the order actually arrived, and checking that is the entire point of
+  the product.
+- **Language: German or English**, switchable, applied to the agent's replies
+  and to speech in both directions.
+- **Start over**, which clears the session and the basket.
+
+### Footer
+
+- **The running version**, `x.y.z`, taken from `APP_VERSION`. It is raised on
+  every release: patch for fixes, minor for new behaviour, major for a break.
+  Without it nobody can tell which build is answering.
+- **The full pizzeria UUID**, selectable, for pasting into API calls.
+- **Connection state** for the ordering API and the model gateway.
+- **A link to the API documentation.**
+
+### Every message gets an answer
+
+The invariant the channel stands on: **no sent message may end without either a
+rendered assistant reply or a rendered error.** Never a silent failure, never an
+indicator that stops with nothing after it.
+
+- The moment a message is sent, the UI shows that the agent is working.
+- Intermediate steps are rendered as they stream — which tool was called and what
+  it returned — visually distinct from the assistant's own words. A stream that
+  carries tool events the page then discards is a defect: the customer sees a
+  frozen screen while the agent is working normally.
+- If the stream ends without a final assistant message, the UI says so.
+- If the request errors, times out, or the connection drops, the UI says which
+  of those happened and offers to resend.
+- Errors in the customer's language, in plain words. No status codes, no
+  tracebacks, no raw JSON.
+
+### The order on screen
+
+- The current basket is visible, with quantities and what it comes to. The code
+  owns the order; the customer must be able to see what the code holds.
+- The read-back is visually distinct and carries an explicit confirm control.
+  Confirmation is an action the customer takes, not a word the agent claims to
+  have heard.
+- On success: the order id in a form a human can read back, and the wait in
+  minutes.
+- After submission the basket is locked and shown as submitted. Nothing on the
+  page can modify or resubmit it.
+
+---
+
 ## Speech
 
 Speech is an input and an output method on the web channel. It is served by a
@@ -347,10 +442,16 @@ plain HTTP with an OpenAI-compatible surface:
 - **The speech service is the only speech path.** No external speech provider,
   no hosted realtime framework, no audio through the LLM gateway — that gateway
   carries chat completions only.
-- **No browser speech APIs.** `SpeechRecognition` and `speechSynthesis` are not
-  used. The previous implementation relied on them, which tied the product to
-  one browser vendor and sent customer audio to a third party. The service
-  replaces them.
+- **The browser captures and plays audio; it does not recognise or synthesise
+  it.** Capture uses the standard `getUserMedia` and `MediaRecorder`; playback
+  uses a plain audio element. Both are cross-browser and cross-platform, so the
+  product works in Firefox, Safari and Chrome, on Linux, macOS and Windows
+  alike.
+- **The browser speech APIs are not used.** `SpeechRecognition` and
+  `speechSynthesis` are forbidden. The previous implementation relied on them,
+  which tied the product to a single browser vendor and sent customer audio to a
+  third party. The self-hosted service replaces them, and that is the whole
+  reason it exists.
 - **Nothing about the speech stack is written into source.** Base URL, STT
   model, TTS model, voice and language all come from the environment, exactly
   like the chat model:
@@ -436,6 +537,13 @@ matter of taste.
   that replays fixed tool calls — happy path, correction, unknown item, customer
   changes mind after read-back, submit timeout. Assert final state and the calls
   actually made.
+- **Browser end-to-end, and it is not optional.** At least one test drives the
+  real page in a headless browser — types a message, waits for a rendered reply,
+  walks a full order to submission — and asserts against the DOM, not against
+  the API. Testing the API with `curl` proves the server works and proves
+  nothing about the product; the customer never talks to `curl`. Include the
+  three failure paths: a tool error, a stream that ends without a final message,
+  and the gateway unreachable. Each must leave a visible message on the page.
 - **The acceptance test is live**, and it is the only test that touches the real
   API. Opt-in via env flag so the rest of the suite stays offline. It runs a full
   conversation, submits, then reads the pizzeria's orders back and asserts the
@@ -549,7 +657,10 @@ then run it once.
    Pass when the unit tests are green.
 2. **Agent loop.** Model, tools, system prompt, one turn end to end.
 3. **CLI.** Full conversation, real API, an order visible in the dashboard.
-4. **Web.** FastAPI on 8888, same core, streamed intermediate steps visible.
+4. **Web.** FastAPI on 8888, same core. Pass only when you have opened the page
+   in a browser, switched pizzeria, asked a price question, placed an order
+   through the page, and then seen that order on that pizzeria's dashboard.
+   Not when the endpoint answers `curl`.
 5. **Speech.** Wire the speech service into the web UI, spoken-answer policy.
 6. **Harden.** Walk the error table, force each case, fix what breaks.
 
@@ -601,7 +712,12 @@ improve.
 | Menu | Fetched live per session, no fallback list |
 | Tenant | One `PIZZERIA_ID` per process, from env, never hardcoded |
 | Transports | One core, two channels (CLI, web), no logic in the channels |
+| Tenancy | Customer-selectable; `PIZZERIA_ID` preselects, never restricts |
+| Prices | Shown from the API; no payment, no invented figures |
+| Version | `x.y.z` in the footer, raised every release |
 | Speech | Self-hosted container, OpenAI-compatible HTTP; no vendor, no browser API |
+| Web UI | Pizzeria name, basket and connection state always visible; no message ends unanswered |
+| Proof | Verified through the browser, never only through the API |
 | Languages | DE + EN, mirrored per turn |
 | Confirmation | Mandatory read-back tied to a basket revision |
 | Parsing | The model parses. No regex order parser, ever. |

 succeeded in 449ms:
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

codex
I’ve confirmed the review-score trail and the SPEC v2 delta in git. Now I’m checking whether the repository content actually matches the v1 claims, including test count, core behavior, web/CLI presence, and whether the code still bakes in assumptions that v2 invalidates.
exec
/bin/bash -lc "for f in core/order.py core/state.py core/menu.py core/pizzasim.py core/tools.py core/agent.py channels/cli.py channels/web.py channels/static/index.html channels/static/app.js channels/static/style.css tests/test_state.py tests/test_tools.py tests/test_transcripts.py; do echo '---'\" "'$f"; nl -ba "$f" | sed -n '"'1,260p'; done" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "for f in tests/transcripts/*.json tests/fixtures/*.json; do echo '---'\" "'$f"; sed -n '"'1,220p' \""'$f"; done' in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc 'pytest --collect-only -q -p no:cacheprovider tests' in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 376ms:
--- tests/transcripts/correction.json
{
  "name": "correction",
  "fake": "ok",
  "turns": [
    {"user": "One margherita please.",
     "script": [
       {"tool": "add_items", "args": {"items": [{"type": "pizza", "code": "margherita", "qty": 1, "extras": []}]}},
       {"say": "One Margherita. May I have your first name?"}
     ]},
    {"user": "No wait, make that three.",
     "script": [
       {"tool": "add_items", "args": {"items": [{"type": "pizza", "code": "margherita", "qty": 2, "extras": []}]}},
       {"say": "Three Margherita it is. Your first name, please?"}
     ]},
    {"user": "Anna. No street, I'll pick it up.",
     "script": [
       {"tool": "set_customer", "args": {"first_name": "Anna"}},
       {"tool": "read_back", "args": {}},
       {"say": "Anna, pick-up — three Margherita. Shall I send it to the kitchen?"}
     ]},
    {"user": "Yes.",
     "script": [
       {"tool": "confirm_order", "args": {"revision": 3}},
       {"tool": "submit_order", "args": {}},
       {"say": "Done! Ready in about 2 minutes."}
     ]}
  ],
  "expect": {
    "state": "SUBMITTED",
    "calls": ["add_items", "add_items", "set_customer", "read_back", "confirm_order", "submit_order"],
    "error_codes": [],
    "items": [{"type": "pizza", "code": "margherita", "qty": 3}]
  }
}
--- tests/transcripts/happy_path.json
{
  "name": "happy_path",
  "fake": "ok",
  "turns": [
    {"user": "Hallo, was für Pizzen haben Sie?",
     "script": [
       {"tool": "get_menu", "args": {}},
       {"say": "Wir haben zum Beispiel Margherita, Salami und Funghi. Was darf es sein?"}
     ]},
    {"user": "Zwei Margherita bitte.",
     "script": [
       {"tool": "add_items", "args": {"items": [{"type": "pizza", "code": "margherita", "qty": 2, "extras": []}]}},
       {"say": "Gerne, zwei Margherita. Auf welchen Vornamen darf ich die Bestellung aufnehmen?"}
     ]},
    {"user": "Marco, via Roma 5.",
     "script": [
       {"tool": "set_customer", "args": {"first_name": "Marco", "street_one": "via Roma 5"}},
       {"tool": "read_back", "args": {}},
       {"say": "Marco, via Roma 5 — zwei Margherita. Stimmt das so?"}
     ]},
    {"user": "Ja, passt.",
     "script": [
       {"tool": "confirm_order", "args": {"revision": 2}},
       {"tool": "submit_order", "args": {}},
       {"say": "Bestellt! Ihre Bestellnummer endet auf 431, fertig in etwa 2 Minuten."}
     ]}
  ],
  "expect": {
    "state": "SUBMITTED",
    "calls": ["get_menu", "add_items", "set_customer", "read_back", "confirm_order", "submit_order"],
    "error_codes": [],
    "items": [{"type": "pizza", "code": "margherita", "qty": 2}]
  }
}
--- tests/transcripts/mind_change.json
{
  "name": "mind_change_after_read_back",
  "fake": "ok",
  "turns": [
    {"user": "Eine Diavolo bitte, auf den Namen Sara, via Napoli 9.",
     "script": [
       {"tool": "add_items", "args": {"items": [{"type": "pizza", "code": "diavolo", "qty": 1, "extras": []}]}},
       {"tool": "set_customer", "args": {"first_name": "Sara", "street_one": "via Napoli 9"}},
       {"tool": "read_back", "args": {}},
       {"say": "Sara, via Napoli 9 — eine Diavolo. Stimmt das?"}
     ]},
    {"user": "Halt, nehmen Sie noch eine Funghi dazu.",
     "script": [
       {"tool": "add_items", "args": {"items": [{"type": "pizza", "code": "funghi", "qty": 1, "extras": []}]}},
       {"tool": "confirm_order", "args": {"revision": 2}},
       {"tool": "read_back", "args": {}},
       {"say": "Jetzt: eine Diavolo und eine Funghi. Stimmt es so?"}
     ]},
    {"user": "Ja, genau so.",
     "script": [
       {"tool": "confirm_order", "args": {"revision": 3}},
       {"tool": "submit_order", "args": {}},
       {"say": "Bestellt! Etwa 2 Minuten."}
     ]}
  ],
  "expect": {
    "state": "SUBMITTED",
    "calls": ["add_items", "set_customer", "read_back", "add_items", "confirm_order", "read_back", "confirm_order", "submit_order"],
    "error_codes": ["stale_revision"],
    "items": [{"type": "pizza", "code": "diavolo", "qty": 1}, {"type": "pizza", "code": "funghi", "qty": 1}]
  }
}
--- tests/transcripts/submit_timeout.json
{
  "name": "submit_timeout",
  "fake": "timeout_then_recover",
  "turns": [
    {"user": "A Hawaii for Nino, via Genova 1.",
     "script": [
       {"tool": "add_items", "args": {"items": [{"type": "pizza", "code": "hawaii", "qty": 1, "extras": []}]}},
       {"tool": "set_customer", "args": {"first_name": "Nino", "street_one": "via Genova 1"}},
       {"tool": "read_back", "args": {}},
       {"say": "Nino, via Genova 1 — one Hawaii. Shall I place it?"}
     ]},
    {"user": "Yes please.",
     "script": [
       {"tool": "confirm_order", "args": {"revision": 2}},
       {"tool": "submit_order", "args": {}},
       {"say": "I'm not sure that went through — give me a moment to check."}
     ]},
    {"user": "Okay, did it work?",
     "script": [
       {"tool": "submit_order", "args": {}},
       {"say": "Yes — it's in. Your order number ends in 1, ready in about 5 minutes."}
     ]}
  ],
  "expect": {
    "state": "SUBMITTED",
    "calls": ["add_items", "set_customer", "read_back", "confirm_order", "submit_order", "submit_order"],
    "error_codes": ["submit_unknown"],
    "order_id": "recovered-1",
    "items": [{"type": "pizza", "code": "hawaii", "qty": 1}]
  }
}
--- tests/transcripts/unknown_item.json
{
  "name": "unknown_item",
  "fake": "ok",
  "turns": [
    {"user": "Einmal Pasta Bolognese bitte.",
     "script": [
       {"tool": "add_items", "args": {"items": [{"type": "pasta", "code": "bolognese", "qty": 1, "extras": []}]}},
       {"say": "Bolognese habe ich leider nicht. Ich hätte Pasta Pesto, Pasta Funghi oder Pasta Tonno — was davon?"}
     ]},
    {"user": "Dann die Funghi.",
     "script": [
       {"tool": "add_items", "args": {"items": [{"type": "pasta", "code": "funghi", "qty": 1, "extras": []}]}},
       {"say": "Eine Pasta Funghi. Ihr Vorname?"}
     ]},
    {"user": "Luca, via Milano 2.",
     "script": [
       {"tool": "set_customer", "args": {"first_name": "Luca", "street_one": "via Milano 2"}},
       {"tool": "read_back", "args": {}},
       {"say": "Luca, via Milano 2 — eine Pasta Funghi. Passt das?"}
     ]},
    {"user": "Ja.",
     "script": [
       {"tool": "confirm_order", "args": {"revision": 2}},
       {"tool": "submit_order", "args": {}},
       {"say": "Bestellt, in etwa 2 Minuten fertig."}
     ]}
  ],
  "expect": {
    "state": "SUBMITTED",
    "calls": ["add_items", "add_items", "set_customer", "read_back", "confirm_order", "submit_order"],
    "error_codes": ["unknown_item"],
    "items": [{"type": "pasta", "code": "funghi", "qty": 1}]
  }
}
--- tests/fixtures/error_422.json
{"error":"validation_failed","details":["items[0].code must be a valid pizza code"]}--- tests/fixtures/location.json
{"street":"via Roma","deliverable":true}--- tests/fixtures/menu.json
{"toppings":["mozzarella","mushrooms","smoked_ham","salami","onions","garlic","pepperoni","pineapple","artichokes","basil","bell_pepper","tuna"],"pizzas":[{"code":"margherita","name":"Margherita","base":["dough","tomatoes","mozzarella","basil"],"price":8.5},{"code":"prosciutto","name":"Prosciutto","base":["dough","tomatoes","mozzarella","smoked_ham"],"price":9.5},{"code":"salami","name":"Salami","base":["dough","tomatoes","mozzarella","salami"],"price":9.5},{"code":"funghi","name":"Funghi","base":["dough","tomatoes","mozzarella","mushrooms"],"price":9},{"code":"regina","name":"Regina","base":["dough","tomatoes","mozzarella","smoked_ham","mushrooms"],"price":10.5},{"code":"mista","name":"Mista","base":["dough","tomatoes","mozzarella","salami","smoked_ham","mushrooms"],"price":11.5},{"code":"hawaii","name":"Hawaii","base":["dough","tomatoes","mozzarella","smoked_ham","pineapple"],"price":10},{"code":"tonno","name":"Tonno","base":["dough","tomatoes","mozzarella","tuna","onions"],"price":10.5},{"code":"papa","name":"Papa","base":["dough","tomatoes","mozzarella","tuna","onions","garlic"],"price":11},{"code":"diavolo","name":"Diavolo","base":["dough","tomatoes","mozzarella","salami","bell_pepper","pepperoni"],"price":11},{"code":"grandiosa","name":"Grandiosa","base":["dough","tomatoes","mozzarella","smoked_ham","salami","mushrooms","bell_pepper","artichokes","onions"],"price":13.5}],"pasta":[{"code":"aglioolio","name":"Pasta Aglio & Olio","base":["pasta","garlic","basil"],"price":9},{"code":"tonno","name":"Pasta Tonno","base":["pasta","tuna"],"price":8.5},{"code":"funghi","name":"Pasta Funghi","base":["pasta","mushrooms"],"price":8.5},{"code":"pesto","name":"Pasta Pesto","base":["pasta","pesto"],"price":8.5}]}--- tests/fixtures/order_created.json
{"order_id":"35711fad-9cf0-4962-bf13-da2f78add431","status":"ordered","eta_seconds":103}--- tests/fixtures/orders_list.json
{
 "orders": [
  {
   "id": "35711fad-9cf0-4962-bf13-da2f78add431",
   "customer_id": "5c8dd73d-00b9-4ba7-99ab-5bbb1be47501",
   "created_at": 1785513532,
   "ready_at": 1785513635,
   "status": "prepared_planned",
   "delivered_at": null,
   "first_name": "ContractProbe"
  },
  {
   "id": "637698d7-13ad-463b-a881-1e7c67d5ac20",
   "customer_id": "a7666746-3f0d-48f3-b774-6a1dada59077",
   "created_at": 1785477732,
   "ready_at": 1785478272,
   "status": "prepared_planned",
   "delivered_at": null,
   "first_name": "Isabella"
  },
  {
   "id": "a425fb11-2f4c-4258-ac92-80e0f5552232",
   "customer_id": "904f4899-17b5-41a9-99f8-db2d23be89d2",
   "created_at": 1785477432,
   "ready_at": 1785478092,
   "status": "prepared_planned",
   "delivered_at": null,
   "first_name": "Marco"
  },
  {
   "id": "61b54278-53de-4c72-946d-3c018b17040d",
   "customer_id": "f24a552e-3f81-4e97-846f-ff4d74ab2aa1",
   "created_at": 1785477432,
   "ready_at": 1785478092,
   "status": "prepared_planned",
   "delivered_at": null,
   "first_name": "Matteo"
  },
  {
   "id": "9f3e22c2-58a4-4440-95b9-a9de593c62b6",
   "customer_id": "dff59240-f0fc-4394-a26c-4b18fdd2a548",
   "created_at": 1785476952,
   "ready_at": 1785477312,
   "status": "prepared_planned",
   "delivered_at": null,
   "first_name": "Sabrina"
  }
 ],
 "total": 10859
}
--- tests/fixtures/pizzerias.json
{"pizzerias":[{"id":"e1efd4b4-7eb3-4b45-b024-344a8b0b602f","name":"Pizzeria Elena","is_demo":true,"protected":true,"created_at":1774358205},{"id":"38863a6f-ff41-4a57-b92d-424d01587302","name":"Pizzeria Giulia","is_demo":true,"protected":true,"created_at":1774358204},{"id":"8a2d1ab2-8690-4dca-bcee-a0bf97db151e","name":"Pizzeria Giovanni","is_demo":true,"protected":true,"created_at":1774358203},{"id":"86517183-e1a5-4bd7-b915-e0db8f8b2131","name":"Pizzeria Roberto","is_demo":true,"protected":true,"created_at":1774358202}]}
 succeeded in 420ms:
--- core/order.py
     1	"""Order data: items, customer, revision, submit bookkeeping. Pure data."""
     2	from __future__ import annotations
     3	
     4	from dataclasses import dataclass, field
     5	from enum import Enum
     6	
     7	
     8	class State(str, Enum):
     9	    EMPTY = "EMPTY"
    10	    COLLECTING = "COLLECTING"
    11	    READY = "READY"
    12	    CONFIRMED = "CONFIRMED"
    13	    SUBMITTED = "SUBMITTED"
    14	
    15	
    16	@dataclass
    17	class Item:
    18	    type: str  # "pizza" | "pasta"
    19	    code: str
    20	    name: str
    21	    qty: int
    22	    extras: list[str] = field(default_factory=list)
    23	
    24	    def line_key(self) -> tuple:
    25	        return (self.type, self.code, tuple(sorted(self.extras)))
    26	
    27	
    28	@dataclass
    29	class Customer:
    30	    first_name: str
    31	    street_one: str | None = None
    32	
    33	    def as_dict(self) -> dict:
    34	        return {"first_name": self.first_name, "street_one": self.street_one}
    35	
    36	
    37	@dataclass
    38	class Order:
    39	    items: list[Item] = field(default_factory=list)
    40	    customer: Customer | None = None
    41	    revision: int = 0
    42	    read_back_revision: int | None = None
    43	    state: State = State.EMPTY
    44	    submit_attempted_at: float | None = None
    45	    submit_unknown: bool = False
    46	    result: dict | None = None  # order_id, status, eta_seconds after submit
    47	
    48	    def snapshot(self) -> dict:
    49	        """Full current state — every successful tool result embeds this."""
    50	        return {
    51	            "state": self.state.value,
    52	            "revision": self.revision,
    53	            "items": [
    54	                {
    55	                    "type": i.type,
    56	                    "code": i.code,
    57	                    "name": i.name,
    58	                    "qty": i.qty,
    59	                    "extras": list(i.extras),
    60	                }
    61	                for i in self.items
    62	            ],
    63	            "customer": self.customer.as_dict() if self.customer else None,
    64	            "read_back_done": self.read_back_revision == self.revision,
    65	        }
--- core/state.py
     1	"""State machine: every Order mutation goes through here.
     2	
     3	Illegal transitions raise TransitionError with a typed code and a speakable
     4	message. Messages are written to be said to the customer as-is.
     5	"""
     6	from __future__ import annotations
     7	
     8	import time
     9	
    10	from .order import Customer, Item, Order, State
    11	
    12	
    13	class TransitionError(Exception):
    14	    def __init__(self, code: str, message: str):
    15	        super().__init__(message)
    16	        self.code = code
    17	        self.message = message
    18	
    19	
    20	def _reject_closed(order: Order) -> None:
    21	    if order.state is State.SUBMITTED:
    22	        raise TransitionError(
    23	            "order_closed",
    24	            "That order is already on its way to the kitchen and can't be "
    25	            "changed. I can take a new order if you like.",
    26	        )
    27	
    28	
    29	def _recompute(order: Order) -> None:
    30	    """Derived-state rule after any legal mutation (demotes CONFIRMED)."""
    31	    order.revision += 1
    32	    # A mutation makes any unverified submit attempt meaningless: the
    33	    # recovery correlation belongs to the basket that was confirmed then,
    34	    # not to whatever the basket becomes now.
    35	    order.submit_unknown = False
    36	    order.submit_attempted_at = None
    37	    if not order.items:
    38	        order.state = State.EMPTY
    39	    elif order.customer is None:
    40	        order.state = State.COLLECTING
    41	    else:
    42	        order.state = State.READY
    43	
    44	
    45	def add_items(order: Order, items: list[Item]) -> None:
    46	    _reject_closed(order)
    47	    for new in items:
    48	        for line in order.items:
    49	            if line.line_key() == new.line_key():
    50	                line.qty += new.qty
    51	                break
    52	        else:
    53	            order.items.append(new)
    54	    _recompute(order)
    55	
    56	
    57	def remove_item(order: Order, type_: str, code: str, qty: int | None) -> None:
    58	    """The spec fixes remove_item's parameters to (type, code, qty), so a
    59	    basket holding the same (type, code) with different extras needs
    60	    deterministic semantics: without qty every matching line goes; with qty
    61	    the most recently added matching line is reduced. The full snapshot in
    62	    the result lets the model repair anything else by remove + re-add."""
    63	    _reject_closed(order)
    64	    if not order.items:
    65	        raise TransitionError("empty_basket", "Your basket is already empty.")
    66	    lines = [i for i in order.items if i.type == type_ and i.code == code]
    67	    if not lines:
    68	        raise TransitionError(
    69	            "not_in_basket", "That item isn't in your basket."
    70	        )
    71	    if qty is None:
    72	        for line in lines:
    73	            order.items.remove(line)
    74	    else:
    75	        line = lines[-1]
    76	        if qty >= line.qty:
    77	            order.items.remove(line)
    78	        else:
    79	            line.qty -= qty
    80	    _recompute(order)
    81	
    82	
    83	def set_customer(order: Order, customer: Customer) -> None:
    84	    _reject_closed(order)
    85	    order.customer = customer
    86	    _recompute(order)
    87	
    88	
    89	def read_back(order: Order) -> None:
    90	    _reject_closed(order)
    91	    if order.state is State.EMPTY:
    92	        raise TransitionError(
    93	            "empty_basket", "There's nothing in the basket yet."
    94	        )
    95	    if order.state is State.COLLECTING:
    96	        raise TransitionError(
    97	            "invalid_state",
    98	            "I still need a name for the order before I can read it back.",
    99	        )
   100	    order.read_back_revision = order.revision
   101	
   102	
   103	def confirm(order: Order, revision: int) -> None:
   104	    _reject_closed(order)
   105	    if order.state is not State.READY:
   106	        if order.state is State.CONFIRMED:
   107	            raise TransitionError(
   108	                "invalid_state", "The order is already confirmed."
   109	            )
   110	        raise TransitionError(
   111	            "invalid_state",
   112	            "The order isn't complete yet, so it can't be confirmed.",
   113	        )
   114	    if revision != order.revision:
   115	        raise TransitionError(
   116	            "stale_revision",
   117	            "The order changed since it was last read back — let me read it "
   118	            "back again.",
   119	        )
   120	    if order.read_back_revision != order.revision:
   121	        raise TransitionError(
   122	            "read_back_required",
   123	            "Let me read the order back to you first.",
   124	        )
   125	    order.state = State.CONFIRMED
   126	
   127	
   128	def begin_submit(order: Order) -> None:
   129	    """Guard + bookkeeping before the submit POST. No state change."""
   130	    if order.state is State.SUBMITTED:
   131	        _reject_closed(order)
   132	    if order.state is not State.CONFIRMED:
   133	        raise TransitionError(
   134	            "invalid_state",
   135	            "The order hasn't been confirmed yet."
   136	            if order.items
   137	            else "What can I get you?",
   138	        )
   139	    if order.submit_attempted_at is None:
   140	        order.submit_attempted_at = time.time()
   141	
   142	
   143	def mark_submitted(order: Order, result: dict) -> None:
   144	    order.result = result
   145	    order.submit_unknown = False
   146	    order.state = State.SUBMITTED
--- core/menu.py
     1	"""Immutable menu snapshot: (type, code) validation, extras validation,
     2	candidate suggestions. One snapshot per session (SPEC invariant 5)."""
     3	from __future__ import annotations
     4	
     5	import difflib
     6	
     7	
     8	class MenuError(Exception):
     9	    def __init__(self, code: str, message: str, candidates: list[dict]):
    10	        super().__init__(message)
    11	        self.code = code
    12	        self.message = message
    13	        self.candidates = candidates
    14	
    15	
    16	class Menu:
    17	    def __init__(self, payload: dict):
    18	        self._by_type: dict[str, dict[str, str]] = {
    19	            "pizza": {p["code"]: p["name"] for p in payload["pizzas"]},
    20	            "pasta": {p["code"]: p["name"] for p in payload["pasta"]},
    21	        }
    22	        self.toppings: list[str] = list(payload.get("toppings", []))
    23	
    24	    def as_tool_result(self) -> dict:
    25	        return {
    26	            "pizzas": [{"code": c, "name": n}
    27	                       for c, n in self._by_type["pizza"].items()],
    28	            "pasta": [{"code": c, "name": n}
    29	                      for c, n in self._by_type["pasta"].items()],
    30	            "toppings": self.toppings,
    31	        }
    32	
    33	    def display_name(self, type_: str, code: str) -> str:
    34	        """Validate (type, code); return display name or raise unknown_item
    35	        with up to three candidates."""
    36	        if type_ not in self._by_type:
    37	            raise MenuError(
    38	                "unknown_item",
    39	                "I only have pizza and pasta on the menu.",
    40	                self.candidates("pizza", code),
    41	            )
    42	        name = self._by_type[type_].get(code)
    43	        if name is None:
    44	            cands = self.candidates(type_, code)
    45	            raise MenuError(
    46	                "unknown_item",
    47	                "I don't have that on the menu."
    48	                + (
    49	                    " Did you mean "
    50	                    + " or ".join(c["name"] for c in cands)
    51	                    + "?"
    52	                    if cands
    53	                    else ""
    54	                ),
    55	                cands,
    56	            )
    57	        return name
    58	
    59	    def validate_extras(self, extras: list[str]) -> None:
    60	        for extra in extras:
    61	            if extra not in self.toppings:
    62	                cands = [
    63	                    {"type": "topping", "code": t, "name": t.replace("_", " ")}
    64	                    for t in difflib.get_close_matches(
    65	                        extra.lower(), self.toppings, n=3, cutoff=0.5
    66	                    )
    67	                ]
    68	                raise MenuError(
    69	                    "invalid_extra",
    70	                    "I can't add that topping."
    71	                    + (
    72	                        " Did you mean "
    73	                        + " or ".join(c["name"] for c in cands)
    74	                        + "?"
    75	                        if cands
    76	                        else ""
    77	                    ),
    78	                    cands,
    79	                )
    80	
    81	    def candidates(self, type_: str, query: str) -> list[dict]:
    82	        """Up to three close matches, same type first, other type as
    83	        fallback so 'pizza tonno' asked as pasta still helps."""
    84	        out: list[dict] = []
    85	        order = [type_] + [t for t in self._by_type if t != type_]
    86	        for t in order:
    87	            if t not in self._by_type or len(out) >= 3:
    88	                continue
    89	            table = self._by_type[t]
    90	            keys = list(table) + [n.lower() for n in table.values()]
    91	            for match in difflib.get_close_matches(
    92	                query.lower(), keys, n=3, cutoff=0.4
    93	            ):
    94	                code = next(
    95	                    c for c, n in table.items()
    96	                    if c == match or n.lower() == match
    97	                )
    98	                entry = {"type": t, "code": code, "name": table[code]}
    99	                if entry not in out:
   100	                    out.append(entry)
   101	        return out[:3]
--- core/pizzasim.py
     1	"""PizzaSim API client: httpx, explicit timeouts, typed errors.
     2	
     3	Also owns the env-config loading shared by the whole app: process env wins,
     4	else ~/.env if present (never written, never printed).
     5	"""
     6	from __future__ import annotations
     7	
     8	import os
     9	from pathlib import Path
    10	
    11	import httpx
    12	
    13	ENV_FILE = Path.home() / ".env"
    14	_TIMEOUT = httpx.Timeout(10.0)
    15	
    16	
    17	class ConfigError(Exception):
    18	    pass
    19	
    20	
    21	def _env_file_values() -> dict[str, str]:
    22	    values: dict[str, str] = {}
    23	    if ENV_FILE.is_file():
    24	        for line in ENV_FILE.read_text().splitlines():
    25	            line = line.strip()
    26	            if line and not line.startswith("#") and "=" in line:
    27	                key, _, val = line.partition("=")
    28	                values[key.strip()] = val.strip().strip('"').strip("'")
    29	    return values
    30	
    31	
    32	def require_env(name: str) -> str:
    33	    value = os.environ.get(name) or _env_file_values().get(name)
    34	    if not value:
    35	        raise ConfigError(
    36	            f"{name} is not set (expected in the environment or {ENV_FILE})"
    37	        )
    38	    return value
    39	
    40	
    41	def optional_env(name: str) -> str | None:
    42	    return os.environ.get(name) or _env_file_values().get(name) or None
    43	
    44	
    45	class PizzaSimError(Exception):
    46	    """Base for typed API errors."""
    47	
    48	
    49	class AuthError(PizzaSimError):
    50	    pass
    51	
    52	
    53	class NotFoundError(PizzaSimError):
    54	    pass
    55	
    56	
    57	class ValidationError(PizzaSimError):
    58	    def __init__(self, details: list[str]):
    59	        super().__init__("; ".join(details))
    60	        self.details = details
    61	
    62	
    63	class ServerError(PizzaSimError):
    64	    pass
    65	
    66	
    67	class ApiTimeout(PizzaSimError):
    68	    pass
    69	
    70	
    71	def _raise_for(response: httpx.Response) -> None:
    72	    if response.status_code in (401, 403):
    73	        raise AuthError(f"auth rejected ({response.status_code})")
    74	    if response.status_code == 404:
    75	        raise NotFoundError("not found")
    76	    if response.status_code == 422:
    77	        try:
    78	            details = response.json().get("details", [])
    79	        except ValueError:
    80	            details = []
    81	        raise ValidationError(details or ["invalid request"])
    82	    if response.status_code >= 500:
    83	        raise ServerError(f"server error ({response.status_code})")
    84	    response.raise_for_status()
    85	
    86	
    87	class PizzaSim:
    88	    def __init__(self, base_url: str, api_key: str, pizzeria_id: str,
    89	                 transport: httpx.BaseTransport | None = None):
    90	        self.pizzeria_id = pizzeria_id
    91	        self._client = httpx.Client(
    92	            base_url=base_url.rstrip("/"),
    93	            headers={"X-API-Key": api_key},
    94	            timeout=_TIMEOUT,
    95	            transport=transport,
    96	        )
    97	
    98	    @classmethod
    99	    def from_env(cls) -> "PizzaSim":
   100	        return cls(
   101	            require_env("PIZZASIM_URL"),
   102	            require_env("PIZZASIM_API_KEY"),
   103	            require_env("PIZZERIA_ID"),
   104	        )
   105	
   106	    def _request(self, method: str, path: str, **kw) -> dict:
   107	        try:
   108	            response = self._client.request(method, path, **kw)
   109	        except httpx.TimeoutException as exc:
   110	            raise ApiTimeout(str(exc)) from exc
   111	        except httpx.HTTPError as exc:
   112	            raise ServerError(str(exc)) from exc
   113	        _raise_for(response)
   114	        return response.json()
   115	
   116	    def get_menu(self) -> dict:
   117	        return self._request("GET", "/menu")
   118	
   119	    def list_pizzerias(self) -> list[dict]:
   120	        return self._request("GET", "/pizzerias")["pizzerias"]
   121	
   122	    def pizzeria_name(self) -> str:
   123	        """Startup step 2: auth + tenant check. Unknown PIZZERIA_ID is the
   124	        404-pizzeria case — the process must refuse to start."""
   125	        for pizzeria in self.list_pizzerias():
   126	            if pizzeria["id"] == self.pizzeria_id:
   127	                return pizzeria["name"]
   128	        raise NotFoundError(
   129	            f"pizzeria {self.pizzeria_id} not found on the PizzaSim server"
   130	        )
   131	
   132	    def list_orders(self) -> list[dict]:
   133	        return self._request(
   134	            "GET", f"/pizzerias/{self.pizzeria_id}/orders"
   135	        )["orders"]
   136	
   137	    def get_order(self, order_id: str) -> dict:
   138	        """Full order incl. customer and items — the list endpoint carries
   139	        neither."""
   140	        return self._request(
   141	            "GET", f"/pizzerias/{self.pizzeria_id}/orders/{order_id}"
   142	        )
   143	
   144	    def submit_order(self, customer: dict, items: list[dict]) -> dict:
   145	        """The only network write. Returns order_id, status, eta_seconds."""
   146	        return self._request(
   147	            "POST",
   148	            f"/pizzerias/{self.pizzeria_id}/orders",
   149	            json={"customer": customer, "items": items},
   150	        )
   151	
   152	    def check_street(self, street: str) -> dict:
   153	        return self._request("GET", "/location", params={"street": street})
--- core/tools.py
     1	"""The eight tool schemas the model sees, plus dispatch.
     2	
     3	Success results always embed the full state snapshot; failures are
     4	{"error": {"code", "message", "candidates"}} with a speakable message.
     5	"""
     6	from __future__ import annotations
     7	
     8	import time
     9	
    10	from . import state
    11	from .menu import Menu, MenuError
    12	from .order import Customer, Item, Order
    13	from .pizzasim import (
    14	    ApiTimeout,
    15	    AuthError,
    16	    PizzaSim,
    17	    PizzaSimError,
    18	    ServerError,
    19	    ValidationError,
    20	)
    21	
    22	_ITEM_SCHEMA = {
    23	    "type": "object",
    24	    "properties": {
    25	        "type": {"type": "string", "enum": ["pizza", "pasta"]},
    26	        "code": {"type": "string"},
    27	        "qty": {"type": "integer", "minimum": 1},
    28	        "extras": {"type": "array", "items": {"type": "string"}},
    29	    },
    30	    "required": ["type", "code", "qty"],
    31	}
    32	
    33	TOOL_SCHEMAS = [
    34	    {"name": "get_menu",
    35	     "description": "The menu: pizzas and pasta with codes and display "
    36	                    "names, and the available extra toppings.",
    37	     "parameters": {"type": "object", "properties": {}}},
    38	    {"name": "add_items",
    39	     "description": "Add items to the basket. Codes must come from "
    40	                    "get_menu. Rejects the whole call if any item or extra "
    41	                    "is unknown.",
    42	     "parameters": {"type": "object",
    43	                    "properties": {"items": {"type": "array",
    44	                                             "items": _ITEM_SCHEMA}},
    45	                    "required": ["items"]}},
    46	    {"name": "remove_item",
    47	     "description": "Remove an item line (or reduce its quantity when qty "
    48	                    "is given).",
    49	     "parameters": {"type": "object",
    50	                    "properties": {
    51	                        "type": {"type": "string",
    52	                                 "enum": ["pizza", "pasta"]},
    53	                        "code": {"type": "string"},
    54	                        "qty": {"type": "integer", "minimum": 1}},
    55	                    "required": ["type", "code"]}},
    56	    {"name": "set_customer",
    57	     "description": "Store the customer's first name and, optionally, "
    58	                    "street.",
    59	     "parameters": {"type": "object",
    60	                    "properties": {
    61	                        "first_name": {"type": "string", "minLength": 1},
    62	                        "street_one": {"type": "string"}},
    63	                    "required": ["first_name"]}},
    64	    {"name": "read_back",
    65	     "description": "The complete order as it stands — read this back to "
    66	                    "the customer before asking for confirmation.",
    67	     "parameters": {"type": "object", "properties": {}}},
    68	    {"name": "confirm_order",
    69	     "description": "Confirm the order after the customer said yes to the "
    70	                    "read-back. revision must be the revision that was "
    71	                    "read back.",
    72	     "parameters": {"type": "object",
    73	                    "properties": {"revision": {"type": "integer"}},
    74	                    "required": ["revision"]}},
    75	    {"name": "submit_order",
    76	     "description": "Send the confirmed order to the kitchen. Only legal "
    77	                    "after confirm_order.",
    78	     "parameters": {"type": "object", "properties": {}}},
    79	    {"name": "check_street",
    80	     "description": "Rough plausibility check of a street name. Not a "
    81	                    "deliverability check — never claim the address was "
    82	                    "verified.",
    83	     "parameters": {"type": "object",
    84	                    "properties": {"street": {"type": "string"}},
    85	                    "required": ["street"]}},
    86	]
    87	
    88	
    89	def openai_tools() -> list[dict]:
    90	    return [{"type": "function", "function": schema}
    91	            for schema in TOOL_SCHEMAS]
    92	
    93	
    94	def _error(code: str, message: str, candidates: list | None = None) -> dict:
    95	    return {"error": {"code": code, "message": message,
    96	                      "candidates": candidates or []}}
    97	
    98	
    99	def _int_qty(value) -> int:
   100	    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
   101	        raise MenuError(
   102	            "invalid_quantity",
   103	            "I need the quantity as a plain number, please.",
   104	            [],
   105	        )
   106	    return value
   107	
   108	
   109	def dispatch(order: Order, menu: Menu, client: PizzaSim,
   110	             name: str, args: dict) -> dict:
   111	    """Execute one tool call. Never raises — every failure is a tool
   112	    result the model must deal with in front of the customer."""
   113	    try:
   114	        return _dispatch(order, menu, client, name, args)
   115	    except MenuError as exc:
   116	        return _error(exc.code, exc.message, exc.candidates)
   117	    except state.TransitionError as exc:
   118	        return _error(exc.code, exc.message)
   119	    except AuthError:
   120	        return _error("api_unavailable",
   121	                      "I can't reach the kitchen system right now.")
   122	    except ApiTimeout:
   123	        return _error("api_unavailable",
   124	                      "The kitchen system isn't answering right now.")
   125	    except PizzaSimError:
   126	        return _error("api_unavailable",
   127	                      "The kitchen system isn't answering right now.")
   128	
   129	
   130	def _dispatch(order: Order, menu: Menu, client: PizzaSim,
   131	              name: str, args: dict) -> dict:
   132	    if name == "get_menu":
   133	        return {"menu": menu.as_tool_result(), "snapshot": order.snapshot()}
   134	
   135	    if name == "add_items":
   136	        items = []
   137	        for raw in args.get("items", []):
   138	            extras = raw.get("extras") or []
   139	            menu.validate_extras(extras)
   140	            items.append(Item(
   141	                type=raw.get("type", ""),
   142	                code=raw.get("code", ""),
   143	                name=menu.display_name(raw.get("type", ""),
   144	                                       raw.get("code", "")),
   145	                qty=_int_qty(raw.get("qty")),
   146	                extras=extras,
   147	            ))  # any failure above rejects the whole call — atomic
   148	        if not items:
   149	            return _error("invalid_quantity", "What can I get you?")
   150	        state.add_items(order, items)
   151	        return {"snapshot": order.snapshot()}
   152	
   153	    if name == "remove_item":
   154	        qty = args.get("qty")
   155	        state.remove_item(order, args.get("type", ""), args.get("code", ""),
   156	                          None if qty is None else _int_qty(qty))
   157	        return {"snapshot": order.snapshot()}
   158	
   159	    if name == "set_customer":
   160	        first_name = (args.get("first_name") or "").strip()
   161	        if not first_name:
   162	            return _error("invalid_state", "I still need a name.")
   163	        customer = Customer(first_name, args.get("street_one") or None)
   164	        state.set_customer(order, customer)
   165	        return {"customer": customer.as_dict(),
   166	                "snapshot": order.snapshot()}
   167	
   168	    if name == "read_back":
   169	        state.read_back(order)
   170	        return {"snapshot": order.snapshot()}
   171	
   172	    if name == "confirm_order":
   173	        revision = args.get("revision")
   174	        if isinstance(revision, bool) or not isinstance(revision, int):
   175	            return _error("stale_revision",
   176	                          "The order changed — let me read it back again.")
   177	        state.confirm(order, revision)
   178	        return {"snapshot": order.snapshot()}
   179	
   180	    if name == "submit_order":
   181	        return _submit(order, client)
   182	
   183	    if name == "check_street":
   184	        result = client.check_street(args.get("street", ""))
   185	        return {"street": result.get("street", ""),
   186	                "deliverable": bool(result.get("deliverable")),
   187	                "snapshot": order.snapshot()}
   188	
   189	    return _error("unknown_tool", "Something went wrong on my side.")
   190	
   191	
   192	_UNSURE = ("I'm not sure that went through — let me check before I try "
   193	           "again.")
   194	
   195	
   196	def _same_items(api_items: list[dict], basket) -> bool:
   197	    def norm(entries):
   198	        return sorted(
   199	            (e["type"], e["code"], e["qty"], tuple(sorted(e["extras"])))
   200	            for e in entries
   201	        )
   202	    ours = [{"type": i.type, "code": i.code, "qty": i.qty,
   203	             "extras": list(i.extras)} for i in basket]
   204	    return norm(api_items) == norm(ours)
   205	
   206	
   207	def _submit(order: Order, client: PizzaSim) -> dict:
   208	    state.begin_submit(order)
   209	
   210	    if order.submit_unknown:
   211	        # A previous attempt timed out: verify against the order list
   212	        # before any retry — a blind retry doubles a real order. The list
   213	        # carries no items, so a shortlisted candidate is verified via the
   214	        # detail endpoint before it is adopted.
   215	        try:
   216	            existing = client.list_orders()
   217	        except PizzaSimError:
   218	            return _error("submit_unknown", _UNSURE)
   219	        cutoff = order.submit_attempted_at - 60  # clock-skew allowance
   220	        matches = [
   221	            o for o in existing
   222	            if o.get("first_name") == order.customer.first_name
   223	            and o.get("created_at", 0) >= cutoff
   224	        ]
   225	        if matches:
   226	            found = max(matches, key=lambda o: o.get("created_at", 0))
   227	            try:
   228	                detail = client.get_order(found["id"])
   229	            except PizzaSimError:
   230	                return _error("submit_unknown", _UNSURE)
   231	            if _same_items(detail.get("items", []), order.items):
   232	                eta = max(0, int(found.get("ready_at", 0) - time.time()))
   233	                state.mark_submitted(order, {
   234	                    "order_id": found["id"],
   235	                    "status": found.get("status", "ordered"),
   236	                    "eta_seconds": eta,
   237	                })
   238	                return {**order.result, "snapshot": order.snapshot()}
   239	        # verified absent (or a different order) → exactly one real retry
   240	
   241	    customer = order.customer.as_dict()
   242	    if customer.get("street_one") is None:
   243	        customer.pop("street_one")
   244	    items = [{"type": i.type, "code": i.code, "qty": i.qty,
   245	              "extras": list(i.extras)} for i in order.items]
   246	    try:
   247	        result = client.submit_order(customer, items)
   248	    except ValidationError as exc:
   249	        return _error("submit_failed",
   250	                      "The kitchen rejected part of the order: "
   251	                      + "; ".join(exc.details))
   252	    except AuthError:
   253	        return _error("api_unavailable",
   254	                      "I can't reach the kitchen system right now.")
   255	    except (ApiTimeout, ServerError):
   256	        order.submit_unknown = True
   257	        return _error("submit_unknown", _UNSURE)
   258	
   259	    state.mark_submitted(order, {
   260	        "order_id": result["order_id"],
--- core/agent.py
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
--- channels/cli.py
     1	"""Interactive terminal chat over the core. A transport only: words in,
     2	words out, no order logic.
     3	
     4	Run:  python -m channels.cli [--verbose]
     5	"""
     6	from __future__ import annotations
     7	
     8	import argparse
     9	import sys
    10	
    11	from core.agent import Agent, AgentConfig, Session, startup
    12	from core.pizzasim import ConfigError, PizzaSimError
    13	
    14	
    15	def make_emit(verbose: bool):
    16	    def emit(event: dict) -> None:
    17	        if not verbose:
    18	            return
    19	        kind = event["type"]
    20	        if kind == "tool_call":
    21	            print(f"  ⚙ {event['tool']} {event['args']}", file=sys.stderr)
    22	        elif kind == "tool_result":
    23	            print(f"  ← {event['result']}", file=sys.stderr)
    24	        elif kind == "state":
    25	            print(f"  ▸ {event['state']} r{event['revision']}",
    26	                  file=sys.stderr)
    27	    return emit
    28	
    29	
    30	def main() -> int:
    31	    parser = argparse.ArgumentParser(description="PizzaSim ordering agent")
    32	    parser.add_argument("--verbose", action="store_true",
    33	                        help="show tool calls and state transitions")
    34	    args = parser.parse_args()
    35	
    36	    try:
    37	        config = AgentConfig.from_env()
    38	        client, pizzeria_name, menu = startup(config)
    39	    except (ConfigError, ValueError) as exc:
    40	        print(f"Configuration error: {exc}", file=sys.stderr)
    41	        return 1
    42	    except PizzaSimError as exc:
    43	        print(f"Startup check against PizzaSim failed: {exc}\n"
    44	              "We're not taking orders right now.", file=sys.stderr)
    45	        return 1
    46	
    47	    agent = Agent(config, client)
    48	    session = Session.create(config, menu, pizzeria_name)
    49	    emit = make_emit(args.verbose)
    50	
    51	    print(f"[{pizzeria_name} — type your order, Ctrl-D to hang up]")
    52	    print(agent.run_turn(session, None, emit))  # agent greets first
    53	    while True:
    54	        try:
    55	            text = input("> ").strip()
    56	        except (EOFError, KeyboardInterrupt):
    57	            print()
    58	            return 0
    59	        if not text:
    60	            continue
    61	        print(agent.run_turn(session, text, emit))
    62	
    63	
    64	if __name__ == "__main__":
    65	    sys.exit(main())
--- channels/web.py
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
--- channels/static/index.html
     1	<!doctype html>
     2	<html lang="de">
     3	<head>
     4	<meta charset="utf-8">
     5	<meta name="viewport" content="width=device-width, initial-scale=1">
     6	<title>Pizza bestellen</title>
     7	<link rel="stylesheet" href="/static/style.css">
     8	</head>
     9	<body>
    10	<header>
    11	  <h1 id="title">Pizza bestellen</h1>
    12	  <label id="tts-wrap" hidden>
    13	    <input type="checkbox" id="tts-toggle"> Antworten vorlesen
    14	  </label>
    15	</header>
    16	
    17	<main id="chat" aria-live="polite"></main>
    18	
    19	<form id="composer">
    20	  <button type="button" id="mic" hidden aria-pressed="false"
    21	          title="Push-to-talk: Klick startet, Klick stoppt">🎤</button>
    22	  <input id="text" autocomplete="off"
    23	         placeholder="Nachricht schreiben …" autofocus>
    24	  <button type="submit" id="send">Senden</button>
    25	</form>
    26	
    27	<script src="/static/app.js"></script>
    28	</body>
    29	</html>
--- channels/static/app.js
     1	/* Web chat over the NDJSON stream. Speech is push-to-talk via
     2	   MediaRecorder + the server's speech proxy — no browser speech APIs. */
     3	"use strict";
     4	
     5	const chat = document.getElementById("chat");
     6	const form = document.getElementById("composer");
     7	const input = document.getElementById("text");
     8	const send = document.getElementById("send");
     9	const mic = document.getElementById("mic");
    10	const ttsWrap = document.getElementById("tts-wrap");
    11	const ttsToggle = document.getElementById("tts-toggle");
    12	
    13	// crypto.randomUUID needs a secure context (HTTPS/localhost); the demo may
    14	// be served over plain HTTP, so fall back to getRandomValues.
    15	const sessionId = crypto.randomUUID
    16	  ? crypto.randomUUID()
    17	  : Array.from(crypto.getRandomValues(new Uint8Array(16)),
    18	               (b) => b.toString(16).padStart(2, "0")).join("");
    19	let speechEnabled = false;
    20	
    21	function add(cls, text) {
    22	  const div = document.createElement("div");
    23	  div.className = "msg " + cls;
    24	  div.textContent = text;
    25	  chat.appendChild(div);
    26	  chat.scrollTop = chat.scrollHeight;
    27	  return div;
    28	}
    29	
    30	function notice(text) {
    31	  const div = document.createElement("div");
    32	  div.className = "notice";
    33	  div.textContent = text;
    34	  chat.appendChild(div);
    35	}
    36	
    37	function stepsBlock() {
    38	  const details = document.createElement("details");
    39	  details.className = "steps";
    40	  details.innerHTML = "<summary>Zwischenschritte</summary>";
    41	  chat.appendChild(details);
    42	  return details;
    43	}
    44	
    45	async function turn(text) {
    46	  send.disabled = true;
    47	  if (text !== null) add("user", text);
    48	  const steps = stepsBlock();
    49	  let finalText = "";
    50	  try {
    51	    const res = await fetch("/chat", {
    52	      method: "POST",
    53	      headers: { "Content-Type": "application/json" },
    54	      body: JSON.stringify({ session_id: sessionId, text }),
    55	    });
    56	    if (!res.ok) throw new Error(await res.text());
    57	    const reader = res.body.getReader();
    58	    const decoder = new TextDecoder();
    59	    let buffer = "";
    60	    for (;;) {
    61	      const { done, value } = await reader.read();
    62	      if (done) break;
    63	      buffer += decoder.decode(value, { stream: true });
    64	      let nl;
    65	      while ((nl = buffer.indexOf("\n")) >= 0) {
    66	        const line = buffer.slice(0, nl); buffer = buffer.slice(nl + 1);
    67	        if (!line.trim()) continue;
    68	        const ev = JSON.parse(line);
    69	        if (ev.type === "tool_call" || ev.type === "tool_result") {
    70	          const pre = document.createElement("pre");
    71	          pre.textContent = (ev.type === "tool_call" ? "→ " : "← ")
    72	            + (ev.tool || "") + " "
    73	            + JSON.stringify(ev.args ?? ev.result);
    74	          steps.appendChild(pre);
    75	        } else if (ev.type === "assistant") {
    76	          finalText = ev.text;
    77	          add("assistant", ev.text);
    78	        } else if (ev.type === "error") {
    79	          notice("Es gab einen technischen Fehler.");
    80	        }
    81	      }
    82	    }
    83	  } catch (err) {
    84	    notice("Verbindung fehlgeschlagen — bitte noch einmal versuchen.");
    85	  }
    86	  if (!steps.querySelector("pre")) steps.remove();
    87	  send.disabled = false;
    88	  input.focus();
    89	  if (finalText && speechEnabled && ttsToggle.checked) speak(finalText);
    90	}
    91	
    92	form.addEventListener("submit", (e) => {
    93	  e.preventDefault();
    94	  const text = input.value.trim();
    95	  if (!text) return;
    96	  input.value = "";
    97	  turn(text);
    98	});
    99	
   100	/* --- speech: push-to-talk, server-proxied ------------------------------ */
   101	
   102	let recorder = null;
   103	
   104	async function startRecording() {
   105	  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
   106	  recorder = new MediaRecorder(stream);
   107	  const chunks = [];
   108	  recorder.ondataavailable = (e) => chunks.push(e.data);
   109	  recorder.onstop = async () => {
   110	    stream.getTracks().forEach((t) => t.stop());
   111	    mic.classList.remove("recording");
   112	    mic.setAttribute("aria-pressed", "false");
   113	    const blob = new Blob(chunks, { type: recorder.mimeType });
   114	    const body = new FormData();
   115	    body.append("audio", blob, "speech.webm");
   116	    try {
   117	      const res = await fetch("/speech/stt", { method: "POST", body });
   118	      if (!res.ok) throw new Error();
   119	      const { text } = await res.json();
   120	      if (text.trim()) turn(text.trim());
   121	      else notice("Ich habe nichts verstanden — bitte noch einmal.");
   122	    } catch {
   123	      notice("Spracherkennung gerade nicht erreichbar — bitte tippen.");
   124	    }
   125	  };
   126	  recorder.start();
   127	  mic.classList.add("recording");
   128	  mic.setAttribute("aria-pressed", "true");
   129	}
   130	
   131	mic.addEventListener("click", () => {
   132	  if (recorder && recorder.state === "recording") recorder.stop();
   133	  else startRecording().catch(() => notice("Kein Mikrofonzugriff."));
   134	});
   135	
   136	async function speak(text) {
   137	  try {
   138	    const res = await fetch("/speech/tts", {
   139	      method: "POST",
   140	      headers: { "Content-Type": "application/json" },
   141	      body: JSON.stringify({ text }),
   142	    });
   143	    if (!res.ok) throw new Error();
   144	    new Audio(URL.createObjectURL(await res.blob())).play();
   145	  } catch {
   146	    notice("Vorlesen gerade nicht möglich.");
   147	  }
   148	}
   149	
   150	/* --- boot -------------------------------------------------------------- */
   151	
   152	(async () => {
   153	  try {
   154	    const cfg = await (await fetch("/config")).json();
   155	    if (cfg.pizzeria) {
   156	      document.getElementById("title").textContent = cfg.pizzeria;
   157	      document.title = cfg.pizzeria;
   158	    }
   159	    // TTS is server-proxied audio and works in any context; only the mic
   160	    // needs getUserMedia/MediaRecorder, which insecure contexts lack.
   161	    speechEnabled = cfg.speech;    // unset SPEECH_URL → nothing rendered
   162	    if (speechEnabled) {
   163	      ttsWrap.hidden = false;
   164	      if (navigator.mediaDevices && window.MediaRecorder) mic.hidden = false;
   165	    }
   166	  } catch { /* text chat works regardless */ }
   167	  turn(null); // opening turn: the agent greets first
   168	})();
--- channels/static/style.css
     1	* { box-sizing: border-box; margin: 0; }
     2	body {
     3	  font: 16px/1.5 system-ui, sans-serif;
     4	  max-width: 720px; margin: 0 auto; padding: 1rem;
     5	  display: flex; flex-direction: column; height: 100vh;
     6	  background: #faf7f2; color: #222;
     7	}
     8	header { display: flex; justify-content: space-between; align-items: baseline; }
     9	h1 { font-size: 1.2rem; padding-bottom: .5rem; }
    10	#tts-wrap { font-size: .85rem; color: #555; }
    11	main { flex: 1; overflow-y: auto; padding: .5rem 0; }
    12	.msg { margin: .4rem 0; padding: .6rem .9rem; border-radius: 12px;
    13	       max-width: 85%; white-space: pre-wrap; }
    14	.user { background: #2f6f4f; color: #fff; margin-left: auto; }
    15	.assistant { background: #fff; border: 1px solid #e5ded2; }
    16	.notice { color: #a33; font-size: .85rem; margin: .3rem 0; }
    17	details.steps { font-size: .78rem; color: #666; margin: .2rem 0 .6rem; }
    18	details.steps summary { cursor: pointer; user-select: none; }
    19	details.steps pre { white-space: pre-wrap; word-break: break-all;
    20	  background: #f2ede4; padding: .4rem .6rem; border-radius: 8px; margin: .2rem 0; }
    21	#composer { display: flex; gap: .5rem; padding-top: .6rem; }
    22	#text { flex: 1; padding: .55rem .8rem; border: 1px solid #ccc;
    23	        border-radius: 10px; font: inherit; }
    24	button { padding: .55rem 1rem; border: 0; border-radius: 10px;
    25	         background: #2f6f4f; color: #fff; font: inherit; cursor: pointer; }
    26	button:disabled { opacity: .5; cursor: default; }
    27	#mic { background: #eee; color: #222; }
    28	#mic.recording { background: #c0392b; color: #fff; animation: pulse 1s infinite; }
    29	@keyframes pulse { 50% { opacity: .6; } }
--- tests/test_state.py
     1	"""State machine, exhaustively: every ✗ cell of the transition table in
     2	PLAN.md and every SPEC invariant 1-4 (invariant 5, menu validation, lives in
     3	test_tools.py)."""
     4	import pytest
     5	
     6	from core.order import Customer, Item, Order, State
     7	from core import state
     8	
     9	
    10	def item(code="margherita", type_="pizza", qty=1, extras=None):
    11	    return Item(type=type_, code=code, name=code.title(), qty=qty,
    12	                extras=extras or [])
    13	
    14	
    15	def order_in(target: State) -> Order:
    16	    o = Order()
    17	    if target is State.EMPTY:
    18	        return o
    19	    state.add_items(o, [item()])
    20	    if target is State.COLLECTING:
    21	        return o
    22	    state.set_customer(o, Customer("Marco", "via Roma"))
    23	    if target is State.READY:
    24	        return o
    25	    state.read_back(o)
    26	    state.confirm(o, o.revision)
    27	    if target is State.CONFIRMED:
    28	        return o
    29	    state.begin_submit(o)
    30	    state.mark_submitted(o, {"order_id": "x", "status": "ordered",
    31	                             "eta_seconds": 600})
    32	    return o
    33	
    34	
    35	def expect(code):
    36	    return pytest.raises(state.TransitionError, match="")
    37	
    38	
    39	# --- happy path -----------------------------------------------------------
    40	
    41	def test_full_happy_path():
    42	    o = Order()
    43	    assert o.state is State.EMPTY
    44	    state.add_items(o, [item(qty=2)])
    45	    assert o.state is State.COLLECTING
    46	    state.set_customer(o, Customer("Marco", "via Roma"))
    47	    assert o.state is State.READY
    48	    state.read_back(o)
    49	    state.confirm(o, o.revision)
    50	    assert o.state is State.CONFIRMED
    51	    state.begin_submit(o)
    52	    state.mark_submitted(o, {"order_id": "abc", "status": "ordered",
    53	                             "eta_seconds": 90})
    54	    assert o.state is State.SUBMITTED
    55	    assert o.result["order_id"] == "abc"
    56	
    57	
    58	def test_customer_before_items_is_legal_and_stays_empty():
    59	    o = Order()
    60	    state.set_customer(o, Customer("Anna"))
    61	    assert o.state is State.EMPTY
    62	    state.add_items(o, [item()])
    63	    assert o.state is State.READY  # customer already known
    64	
    65	
    66	# --- illegal cells, one test per ✗ ---------------------------------------
    67	
    68	@pytest.mark.parametrize("mutate", [
    69	    lambda o: state.add_items(o, [item()]),
    70	    lambda o: state.remove_item(o, "pizza", "margherita", None),
    71	    lambda o: state.set_customer(o, Customer("Eve")),
    72	    lambda o: state.read_back(o),
    73	    lambda o: state.confirm(o, o.revision),
    74	    lambda o: state.begin_submit(o),
    75	])
    76	def test_submitted_is_terminal(mutate):
    77	    o = order_in(State.SUBMITTED)
    78	    with pytest.raises(state.TransitionError) as e:
    79	        mutate(o)
    80	    assert e.value.code == "order_closed"
    81	
    82	
    83	def test_remove_from_empty():
    84	    with pytest.raises(state.TransitionError) as e:
    85	        state.remove_item(order_in(State.EMPTY), "pizza", "margherita", None)
    86	    assert e.value.code == "empty_basket"
    87	
    88	
    89	def test_read_back_empty():
    90	    with pytest.raises(state.TransitionError) as e:
    91	        state.read_back(order_in(State.EMPTY))
    92	    assert e.value.code == "empty_basket"
    93	
    94	
    95	def test_read_back_collecting_needs_customer():
    96	    with pytest.raises(state.TransitionError) as e:
    97	        state.read_back(order_in(State.COLLECTING))
    98	    assert e.value.code == "invalid_state"
    99	
   100	
   101	@pytest.mark.parametrize("st", [State.EMPTY, State.COLLECTING])
   102	def test_confirm_illegal_states(st):
   103	    o = order_in(st)
   104	    with pytest.raises(state.TransitionError) as e:
   105	        state.confirm(o, o.revision)
   106	    assert e.value.code == "invalid_state"
   107	
   108	
   109	def test_confirm_when_already_confirmed():
   110	    o = order_in(State.CONFIRMED)
   111	    with pytest.raises(state.TransitionError) as e:
   112	        state.confirm(o, o.revision)
   113	    assert e.value.code == "invalid_state"
   114	
   115	
   116	@pytest.mark.parametrize("st", [State.EMPTY, State.COLLECTING, State.READY])
   117	def test_submit_outside_confirmed(st):
   118	    """Invariant 1: submit outside CONFIRMED is refused (incl. empty)."""
   119	    o = order_in(st)
   120	    with pytest.raises(state.TransitionError) as e:
   121	        state.begin_submit(o)
   122	    assert e.value.code == "invalid_state"
   123	
   124	
   125	def test_remove_unknown_line():
   126	    o = order_in(State.COLLECTING)
   127	    with pytest.raises(state.TransitionError) as e:
   128	        state.remove_item(o, "pasta", "pesto", None)
   129	    assert e.value.code == "not_in_basket"
   130	
   131	
   132	# --- invariant 2: mutation after CONFIRMED demotes ------------------------
   133	
   134	def test_add_after_confirmed_demotes_to_ready():
   135	    o = order_in(State.CONFIRMED)
   136	    state.add_items(o, [item("funghi")])
   137	    assert o.state is State.READY
   138	
   139	
   140	def test_remove_after_confirmed_demotes():
   141	    o = order_in(State.CONFIRMED)
   142	    state.remove_item(o, "pizza", "margherita", None)
   143	    assert o.state is State.EMPTY  # last item gone, customer kept
   144	
   145	
   146	def test_set_customer_after_confirmed_demotes():
   147	    o = order_in(State.CONFIRMED)
   148	    state.set_customer(o, Customer("Mario"))
   149	    assert o.state is State.READY
   150	
   151	
   152	def test_confirmation_does_not_survive_demotion():
   153	    """A confirmation applies to the basket that was read back."""
   154	    o = order_in(State.CONFIRMED)
   155	    state.add_items(o, [item("funghi")])
   156	    with pytest.raises(state.TransitionError):
   157	        state.begin_submit(o)
   158	
   159	
   160	# --- invariant 3: confirm tied to read-back + revision --------------------
   161	
   162	def test_confirm_without_read_back():
   163	    o = order_in(State.READY)
   164	    with pytest.raises(state.TransitionError) as e:
   165	        state.confirm(o, o.revision)
   166	    assert e.value.code == "read_back_required"
   167	
   168	
   169	def test_confirm_with_stale_revision():
   170	    o = order_in(State.READY)
   171	    state.read_back(o)
   172	    stale = o.revision
   173	    state.add_items(o, [item("funghi")])
   174	    with pytest.raises(state.TransitionError) as e:
   175	        state.confirm(o, stale)
   176	    assert e.value.code == "stale_revision"
   177	
   178	
   179	def test_read_back_of_old_revision_does_not_allow_confirm():
   180	    o = order_in(State.READY)
   181	    state.read_back(o)
   182	    state.add_items(o, [item("funghi")])  # bumps revision
   183	    with pytest.raises(state.TransitionError) as e:
   184	        state.confirm(o, o.revision)
   185	    assert e.value.code == "read_back_required"
   186	
   187	
   188	# --- basket mechanics -----------------------------------------------------
   189	
   190	def test_revision_increments_on_every_mutation():
   191	    o = Order()
   192	    r0 = o.revision
   193	    state.add_items(o, [item()])
   194	    state.set_customer(o, Customer("A"))
   195	    state.remove_item(o, "pizza", "margherita", None)
   196	    assert o.revision == r0 + 3
   197	
   198	
   199	def test_merge_same_line():
   200	    o = Order()
   201	    state.add_items(o, [item(qty=1)])
   202	    state.add_items(o, [item(qty=2)])
   203	    assert len(o.items) == 1 and o.items[0].qty == 3
   204	
   205	
   206	def test_same_code_different_extras_is_separate_line():
   207	    o = Order()
   208	    state.add_items(o, [item(qty=1)])
   209	    state.add_items(o, [item(qty=1, extras=["mushrooms"])])
   210	    assert len(o.items) == 2
   211	
   212	
   213	def test_partial_remove():
   214	    o = Order()
   215	    state.add_items(o, [item(qty=3)])
   216	    state.remove_item(o, "pizza", "margherita", 1)
   217	    assert o.items[0].qty == 2
   218	    state.remove_item(o, "pizza", "margherita", 5)  # >= qty removes line
   219	    assert o.items == []
   220	    assert o.state is State.EMPTY
   221	
   222	
   223	def test_remove_to_empty_and_readd():
   224	    o = order_in(State.READY)
   225	    state.remove_item(o, "pizza", "margherita", None)
   226	    assert o.state is State.EMPTY
   227	    state.add_items(o, [item("funghi")])
   228	    assert o.state is State.READY  # customer survived
   229	
   230	
   231	def test_type_and_code_key_removal():
   232	    """tonno exists as pizza and pasta — removal must key on (type, code)."""
   233	    o = Order()
   234	    state.add_items(o, [item("tonno", "pizza"), item("tonno", "pasta")])
   235	    state.remove_item(o, "pasta", "tonno", None)
   236	    assert [i.type for i in o.items] == ["pizza"]
   237	
   238	
   239	def test_remove_without_qty_clears_all_variants():
   240	    """Same (type, code), different extras: no-qty removal takes them all."""
   241	    o = Order()
   242	    state.add_items(o, [item(qty=1), item(qty=1, extras=["mushrooms"])])
   243	    state.remove_item(o, "pizza", "margherita", None)
   244	    assert o.items == []
   245	
   246	
   247	def test_remove_with_qty_reduces_most_recent_variant():
   248	    o = Order()
   249	    state.add_items(o, [item(qty=2), item(qty=2, extras=["mushrooms"])])
   250	    state.remove_item(o, "pizza", "margherita", 1)
   251	    assert [(i.extras, i.qty) for i in o.items] == \
   252	        [([], 2), (["mushrooms"], 1)]
   253	
   254	
   255	def test_submit_attempt_timestamp_set_once():
   256	    o = order_in(State.CONFIRMED)
   257	    state.begin_submit(o)
   258	    first = o.submit_attempted_at
   259	    assert first is not None
   260	    state.begin_submit(o)
--- tests/test_tools.py
     1	"""Tool layer against recorded fixtures. No network, no LLM.
     2	
     3	Includes the one opt-in live smoke test (PIZZA_LIVE_TEST=1)."""
     4	import json
     5	import os
     6	import time
     7	from pathlib import Path
     8	
     9	import httpx
    10	import pytest
    11	
    12	from core import state, tools
    13	from core.menu import Menu, MenuError
    14	from core.order import Customer, Order, State
    15	from core.pizzasim import (
    16	    ApiTimeout,
    17	    AuthError,
    18	    NotFoundError,
    19	    PizzaSim,
    20	    ServerError,
    21	    ValidationError,
    22	)
    23	
    24	FIXTURES = Path(__file__).parent / "fixtures"
    25	
    26	
    27	def fixture(name):
    28	    return json.loads((FIXTURES / name).read_text())
    29	
    30	
    31	@pytest.fixture
    32	def menu():
    33	    return Menu(fixture("menu.json"))
    34	
    35	
    36	# --- menu validation ------------------------------------------------------
    37	
    38	def test_known_codes(menu):
    39	    assert menu.display_name("pizza", "margherita") == "Margherita"
    40	    assert menu.display_name("pasta", "pesto") == "Pasta Pesto"
    41	
    42	
    43	def test_tonno_collision_is_per_type(menu):
    44	    """Codes are unique per type, not globally."""
    45	    assert menu.display_name("pizza", "tonno") == "Tonno"
    46	    assert menu.display_name("pasta", "tonno") == "Pasta Tonno"
    47	
    48	
    49	def test_unknown_code_gives_candidates(menu):
    50	    with pytest.raises(MenuError) as e:
    51	        menu.display_name("pizza", "margarita")  # misspelt
    52	    assert e.value.code == "unknown_item"
    53	    assert 1 <= len(e.value.candidates) <= 3
    54	    assert e.value.candidates[0]["code"] == "margherita"
    55	
    56	
    57	def test_wrong_type_falls_back_to_other_type(menu):
    58	    with pytest.raises(MenuError) as e:
    59	        menu.display_name("pasta", "hawaii")
    60	    codes = [c["code"] for c in e.value.candidates]
    61	    assert "hawaii" in codes  # found as pizza
    62	
    63	
    64	def test_extras_controlled_vocabulary(menu):
    65	    menu.validate_extras(["mushrooms", "pineapple"])  # ok
    66	    with pytest.raises(MenuError) as e:
    67	        menu.validate_extras(["unicorn_dust"])
    68	    assert e.value.code == "invalid_extra"
    69	
    70	
    71	# --- pizzasim client typed errors (httpx MockTransport) -------------------
    72	
    73	def client_returning(handler):
    74	    return PizzaSim("http://test", "key", "pz-1",
    75	                    transport=httpx.MockTransport(handler))
    76	
    77	
    78	def respond(status, body):
    79	    return lambda request: httpx.Response(status, json=body)
    80	
    81	
    82	def test_auth_error_mapped():
    83	    with pytest.raises(AuthError):
    84	        client_returning(respond(401, {})).get_menu()
    85	    with pytest.raises(AuthError):
    86	        client_returning(respond(403, {})).get_menu()
    87	
    88	
    89	def test_404_mapped():
    90	    with pytest.raises(NotFoundError):
    91	        client_returning(respond(404, {})).list_orders()
    92	
    93	
    94	def test_422_mapped_with_details():
    95	    with pytest.raises(ValidationError) as e:
    96	        client_returning(
    97	            respond(422, fixture("error_422.json"))
    98	        ).submit_order({"first_name": "X"}, [])
    99	    assert "valid pizza code" in e.value.details[0]
   100	
   101	
   102	def test_5xx_mapped():
   103	    with pytest.raises(ServerError):
   104	        client_returning(respond(500, {})).get_menu()
   105	
   106	
   107	def test_timeout_mapped():
   108	    def handler(request):
   109	        raise httpx.ConnectTimeout("boom")
   110	    with pytest.raises(ApiTimeout):
   111	        client_returning(handler).get_menu()
   112	
   113	
   114	def test_pizzeria_name_startup_check():
   115	    payload = fixture("pizzerias.json")
   116	    good = PizzaSim("http://test", "key",
   117	                    payload["pizzerias"][0]["id"],
   118	                    transport=httpx.MockTransport(respond(200, payload)))
   119	    assert good.pizzeria_name() == payload["pizzerias"][0]["name"]
   120	    bad = client_returning(respond(200, payload))
   121	    with pytest.raises(NotFoundError):
   122	        bad.pizzeria_name()
   123	
   124	
   125	def test_submit_parses_order_created():
   126	    client = client_returning(respond(200, fixture("order_created.json")))
   127	    result = client.submit_order({"first_name": "Marco"}, [])
   128	    assert result["order_id"] and result["status"] == "ordered"
   129	    assert isinstance(result["eta_seconds"], int)
   130	
   131	
   132	# --- dispatch -------------------------------------------------------------
   133	
   134	class FakeClient:
   135	    """Scripted stand-in for PizzaSim in dispatch tests."""
   136	
   137	    def __init__(self):
   138	        self.submits = 0
   139	        self.list_calls = 0
   140	        self.submit_effect = lambda: fixture("order_created.json")
   141	        self.orders = []
   142	        self.order_details = {}  # id -> detail payload
   143	        self.list_effect = None  # exception to raise, if any
   144	
   145	    def submit_order(self, customer, items):
   146	        self.submits += 1
   147	        return self.submit_effect()
   148	
   149	    def list_orders(self):
   150	        self.list_calls += 1
   151	        if self.list_effect:
   152	            raise self.list_effect
   153	        return self.orders
   154	
   155	    def get_order(self, order_id):
   156	        if order_id not in self.order_details:
   157	            raise NotFoundError("no such order")
   158	        return self.order_details[order_id]
   159	
   160	    def check_street(self, street):
   161	        return {"street": street, "deliverable": True}
   162	
   163	
   164	@pytest.fixture
   165	def fake():
   166	    return FakeClient()
   167	
   168	
   169	def ready_order(menu, fake):
   170	    order = Order()
   171	    tools.dispatch(order, menu, fake, "add_items",
   172	                   {"items": [{"type": "pizza", "code": "margherita",
   173	                               "qty": 2}]})
   174	    tools.dispatch(order, menu, fake, "set_customer",
   175	                   {"first_name": "Marco", "street_one": "via Roma"})
   176	    return order
   177	
   178	
   179	def confirmed_order(menu, fake):
   180	    order = ready_order(menu, fake)
   181	    tools.dispatch(order, menu, fake, "read_back", {})
   182	    tools.dispatch(order, menu, fake, "confirm_order",
   183	                   {"revision": order.revision})
   184	    assert order.state is State.CONFIRMED
   185	    return order
   186	
   187	
   188	def test_every_success_carries_full_snapshot(menu, fake):
   189	    order = Order()
   190	    result = tools.dispatch(order, menu, fake, "get_menu", {})
   191	    assert result["snapshot"]["state"] == "EMPTY"
   192	    assert result["menu"]["toppings"]
   193	    result = tools.dispatch(order, menu, fake, "add_items",
   194	                            {"items": [{"type": "pizza",
   195	                                        "code": "margherita", "qty": 1}]})
   196	    snap = result["snapshot"]
   197	    assert snap["items"][0]["name"] == "Margherita"
   198	    assert snap["state"] == "COLLECTING" and snap["revision"] == 1
   199	    assert snap["customer"] is None and snap["read_back_done"] is False
   200	
   201	
   202	def test_unknown_item_error_shape(menu, fake):
   203	    result = tools.dispatch(Order(), menu, fake, "add_items",
   204	                            {"items": [{"type": "pizza", "code": "margarita",
   205	                                        "qty": 1}]})
   206	    err = result["error"]
   207	    assert err["code"] == "unknown_item"
   208	    assert err["candidates"][0]["code"] == "margherita"
   209	    assert err["message"]  # speakable
   210	
   211	
   212	def test_add_is_atomic(menu, fake):
   213	    order = Order()
   214	    result = tools.dispatch(order, menu, fake, "add_items",
   215	                            {"items": [
   216	                                {"type": "pizza", "code": "margherita",
   217	                                 "qty": 1},
   218	                                {"type": "pizza", "code": "nope", "qty": 1},
   219	                            ]})
   220	    assert result["error"]["code"] == "unknown_item"
   221	    assert order.items == [] and order.state is State.EMPTY
   222	
   223	
   224	def test_invalid_quantity_not_parsed(menu, fake):
   225	    """A tool that receives "zwei" returns invalid_quantity."""
   226	    for bad in ("zwei", 2.5, 0, -1, True, None):
   227	        result = tools.dispatch(Order(), menu, fake, "add_items",
   228	                                {"items": [{"type": "pizza",
   229	                                            "code": "margherita",
   230	                                            "qty": bad}]})
   231	        assert result["error"]["code"] == "invalid_quantity", bad
   232	
   233	
   234	def test_invalid_extra_via_dispatch(menu, fake):
   235	    result = tools.dispatch(Order(), menu, fake, "add_items",
   236	                            {"items": [{"type": "pizza",
   237	                                        "code": "margherita", "qty": 1,
   238	                                        "extras": ["unicorn_dust"]}]})
   239	    assert result["error"]["code"] == "invalid_extra"
   240	
   241	
   242	def test_remove_semantics(menu, fake):
   243	    order = ready_order(menu, fake)
   244	    result = tools.dispatch(order, menu, fake, "remove_item",
   245	                            {"type": "pizza", "code": "margherita",
   246	                             "qty": 1})
   247	    assert result["snapshot"]["items"][0]["qty"] == 1
   248	    result = tools.dispatch(order, menu, fake, "remove_item",
   249	                            {"type": "pizza", "code": "margherita"})
   250	    assert result["snapshot"]["items"] == []
   251	    assert result["snapshot"]["state"] == "EMPTY"
   252	
   253	
   254	def test_submit_success(menu, fake):
   255	    order = confirmed_order(menu, fake)
   256	    result = tools.dispatch(order, menu, fake, "submit_order", {})
   257	    assert result["order_id"] == fixture("order_created.json")["order_id"]
   258	    assert result["status"] == "ordered"
   259	    assert isinstance(result["eta_seconds"], int)
   260	    assert result["snapshot"]["state"] == "SUBMITTED"
--- tests/test_transcripts.py
     1	"""Golden transcripts: five scripted conversations run through the real
     2	agent loop against a stub model that replays fixed tool calls. Asserts the
     3	final state and the calls actually made. No network, no LLM."""
     4	import json
     5	import time
     6	from pathlib import Path
     7	
     8	import pytest
     9	
    10	from core.agent import Agent, AgentConfig, Session
    11	from core.menu import Menu
    12	from core.order import Order
    13	from core.pizzasim import ApiTimeout
    14	
    15	FIXTURES = Path(__file__).parent / "fixtures"
    16	TRANSCRIPTS = sorted((Path(__file__).parent / "transcripts").glob("*.json"))
    17	
    18	
    19	class StubModel:
    20	    """Replays a transcript's scripted actions, one per chat call."""
    21	
    22	    def __init__(self, turns):
    23	        self._queues = [list(turn["script"]) for turn in turns]
    24	        self._current = None
    25	
    26	    def next_turn(self):
    27	        self._current = self._queues.pop(0)
    28	
    29	    def __call__(self, messages, tool_schemas):
    30	        action = self._current.pop(0)
    31	        if "tool" in action:
    32	            assert any(t["function"]["name"] == action["tool"]
    33	                       for t in tool_schemas), action["tool"]
    34	            return {"tool_calls": [{
    35	                "id": f"call-{action['tool']}",
    36	                "function": {"name": action["tool"],
    37	                             "arguments": json.dumps(action["args"])},
    38	            }]}
    39	        return {"content": action["say"]}
    40	
    41	
    42	class ScriptedClient:
    43	    """Fake PizzaSim: 'ok' submits succeed; 'timeout_then_recover' times
    44	    out once, then the order shows up in the list."""
    45	
    46	    def __init__(self, mode):
    47	        self.mode = mode
    48	        self.submits = 0
    49	        self.created = json.loads((FIXTURES / "order_created.json")
    50	                                  .read_text())
    51	
    52	    def submit_order(self, customer, items):
    53	        self.submits += 1
    54	        if self.mode == "timeout_then_recover" and self.submits == 1:
    55	            self._customer = customer
    56	            self._items = items
    57	            raise ApiTimeout("simulated submit timeout")
    58	        return self.created
    59	
    60	    def list_orders(self):
    61	        if self.mode == "timeout_then_recover":
    62	            return [{"id": "recovered-1",
    63	                     "first_name": self._customer["first_name"],
    64	                     "created_at": int(time.time()),
    65	                     "ready_at": int(time.time()) + 300,
    66	                     "status": "ordered"}]
    67	        return []
    68	
    69	    def get_order(self, order_id):
    70	        return {"id": order_id,
    71	                "customer": self._customer,
    72	                "items": self._items}
    73	
    74	    def check_street(self, street):
    75	        return {"street": street, "deliverable": True}
    76	
    77	
    78	@pytest.mark.parametrize("path", TRANSCRIPTS, ids=lambda p: p.stem)
    79	def test_golden_transcript(path):
    80	    transcript = json.loads(path.read_text())
    81	    stub = StubModel(transcript["turns"])
    82	    client = ScriptedClient(transcript["fake"])
    83	    config = AgentConfig(url="http://unused", key="unused",
    84	                         model="stub", lang="de")
    85	    menu = Menu(json.loads((FIXTURES / "menu.json").read_text()))
    86	    session = Session(order=Order(), menu=menu,
    87	                      messages=[{"role": "system", "content": "stub"}])
    88	    agent = Agent(config, client, chat_fn=stub)
    89	
    90	    calls, error_codes = [], []
    91	
    92	    def emit(event):
    93	        if event["type"] == "tool_call":
    94	            calls.append(event["tool"])
    95	        if event["type"] == "tool_result" and "error" in event["result"]:
    96	            error_codes.append(event["result"]["error"]["code"])
    97	
    98	    for turn in transcript["turns"]:
    99	        stub.next_turn()
   100	        final = agent.run_turn(session, turn["user"], emit)
   101	        assert final == turn["script"][-1]["say"]
   102	
   103	    expect = transcript["expect"]
   104	    assert session.order.state.value == expect["state"]
   105	    assert calls == expect["calls"]
   106	    assert error_codes == expect["error_codes"]
   107	    actual_items = [{"type": i.type, "code": i.code, "qty": i.qty}
   108	                    for i in session.order.items]
   109	    assert actual_items == expect["items"]
   110	    if "order_id" in expect:
   111	        assert session.order.result["order_id"] == expect["order_id"]
   112	    if expect["state"] == "SUBMITTED":
   113	        assert session.order.result["order_id"]
   114	
   115	
   116	def test_five_transcripts_exist():
   117	    assert len(TRANSCRIPTS) == 5
   118	
   119	
   120	def test_gateway_timeout_apology():
   121	    """Gateway timeout: one retry, then abort the turn with an apology."""
   122	    attempts = []
   123	
   124	    def flaky(messages, tool_schemas):
   125	        attempts.append(1)
   126	        from core.agent import GatewayError
   127	        raise GatewayError("gateway timed out twice")
   128	
   129	    config = AgentConfig(url="http://unused", key="unused",
   130	                         model="stub", lang="en")
   131	    menu = Menu(json.loads((FIXTURES / "menu.json").read_text()))
   132	    session = Session(order=Order(), menu=menu,
   133	                      messages=[{"role": "system", "content": "stub"}])
   134	    agent = Agent(config, ScriptedClient("ok"), chat_fn=flaky)
   135	    text = agent.run_turn(session, "hello")
   136	    assert "sorry" in text.lower()
   137	    assert session.order.state.value == "EMPTY"  # turn aborted cleanly

 exited 1 in 963ms:
Traceback (most recent call last):
  File "/home/rob/.local/bin/pytest", line 8, in <module>
    sys.exit(console_main())
             ~~~~~~~~~~~~^^
  File "/home/rob/.local/lib/python3.13/site-packages/_pytest/config/__init__.py", line 223, in console_main
    code = main()
  File "/home/rob/.local/lib/python3.13/site-packages/_pytest/config/__init__.py", line 193, in main
    config = _prepareconfig(new_args, plugins)
  File "/home/rob/.local/lib/python3.13/site-packages/_pytest/config/__init__.py", line 361, in _prepareconfig
    config: Config = pluginmanager.hook.pytest_cmdline_parse(
                     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        pluginmanager=pluginmanager, args=args
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/rob/.local/lib/python3.13/site-packages/pluggy/_hooks.py", line 512, in __call__
    return self._hookexec(self.name, self._hookimpls.copy(), kwargs, firstresult)
           ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/rob/.local/lib/python3.13/site-packages/pluggy/_manager.py", line 120, in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
           ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/rob/.local/lib/python3.13/site-packages/pluggy/_callers.py", line 167, in _multicall
    raise exception
  File "/home/rob/.local/lib/python3.13/site-packages/pluggy/_callers.py", line 139, in _multicall
    teardown.throw(exception)
    ~~~~~~~~~~~~~~^^^^^^^^^^^
  File "/home/rob/.local/lib/python3.13/site-packages/_pytest/helpconfig.py", line 124, in pytest_cmdline_parse
    config = yield
             ^^^^^
  File "/home/rob/.local/lib/python3.13/site-packages/pluggy/_callers.py", line 121, in _multicall
    res = hook_impl.function(*args)
  File "/home/rob/.local/lib/python3.13/site-packages/_pytest/config/__init__.py", line 1186, in pytest_cmdline_parse
    self.parse(args)
    ~~~~~~~~~~^^^^^^
  File "/home/rob/.local/lib/python3.13/site-packages/_pytest/config/__init__.py", line 1556, in parse
    self.hook.pytest_load_initial_conftests(
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        early_config=self, args=args, parser=self._parser
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/rob/.local/lib/python3.13/site-packages/pluggy/_hooks.py", line 512, in __call__
    return self._hookexec(self.name, self._hookimpls.copy(), kwargs, firstresult)
           ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/rob/.local/lib/python3.13/site-packages/pluggy/_manager.py", line 120, in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
           ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/rob/.local/lib/python3.13/site-packages/pluggy/_callers.py", line 167, in _multicall
    raise exception
  File "/home/rob/.local/lib/python3.13/site-packages/pluggy/_callers.py", line 139, in _multicall
    teardown.throw(exception)
    ~~~~~~~~~~~~~~^^^^^^^^^^^
  File "/home/rob/.local/lib/python3.13/site-packages/_pytest/warnings.py", line 128, in pytest_load_initial_conftests
    return (yield)
            ^^^^^
  File "/home/rob/.local/lib/python3.13/site-packages/pluggy/_callers.py", line 116, in _multicall
    next(function_gen)  # first yield
    ~~~~^^^^^^^^^^^^^^
  File "/home/rob/.local/lib/python3.13/site-packages/_pytest/capture.py", line 170, in pytest_load_initial_conftests
    capman.start_global_capturing()
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/rob/.local/lib/python3.13/site-packages/_pytest/capture.py", line 773, in start_global_capturing
    self._global_capturing = _get_multicapture(self._method)
                             ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^
  File "/home/rob/.local/lib/python3.13/site-packages/_pytest/capture.py", line 714, in _get_multicapture
    return MultiCapture(in_=FDCapture(0), out=FDCapture(1), err=FDCapture(2))
                                              ~~~~~~~~~^^^
  File "/home/rob/.local/lib/python3.13/site-packages/_pytest/capture.py", line 493, in __init__
    TemporaryFile(buffering=0),
    ~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "/usr/lib/python3.13/tempfile.py", line 823, in TemporaryFile
    prefix, suffix, dir, output_type = _sanitize_params(prefix, suffix, dir)
                                       ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.13/tempfile.py", line 317, in _sanitize_params
    dir = gettempdir()
  File "/usr/lib/python3.13/tempfile.py", line 507, in gettempdir
    return _os.fsdecode(_gettempdir())
                        ~~~~~~~~~~~^^
  File "/usr/lib/python3.13/tempfile.py", line 500, in _gettempdir
    tempdir = _get_default_tempdir()
  File "/usr/lib/python3.13/tempfile.py", line 415, in _get_default_tempdir
    raise FileNotFoundError(_errno.ENOENT,
                            "No usable temporary directory found in %s" %
                            dirlist)
FileNotFoundError: [Errno 2] No usable temporary directory found in ['/tmp', '/var/tmp', '/usr/tmp', '/home/rob/bpm-pizza-vibecoding-solution']

codex
The code inspection is enough to start identifying where v2 collides with existing assumptions. I’m tightening the audit now with concrete counts and line-level evidence, because the hardest questions need to be grounded in what the repo actually does today, not what the plan says it will do.
exec
/bin/bash -lc "rg -n '"'^def test_'"' tests/test_state.py tests/test_tools.py tests/test_transcripts.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "nl -ba channels/static/index.html | sed -n '1,260p'; printf '\\n---\\n'; nl -ba channels/static/app.js | sed -n '1,360p'; printf '\\n---\\n'; nl -ba channels/static/style.css | sed -n '1,260p'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "nl -ba core/agent.py | sed -n '1,320p'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "nl -ba channels/web.py | sed -n '1,340p'" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 351ms:
tests/test_transcripts.py:79:def test_golden_transcript(path):
tests/test_transcripts.py:116:def test_five_transcripts_exist():
tests/test_transcripts.py:120:def test_gateway_timeout_apology():
tests/test_state.py:41:def test_full_happy_path():
tests/test_state.py:58:def test_customer_before_items_is_legal_and_stays_empty():
tests/test_state.py:76:def test_submitted_is_terminal(mutate):
tests/test_state.py:83:def test_remove_from_empty():
tests/test_state.py:89:def test_read_back_empty():
tests/test_state.py:95:def test_read_back_collecting_needs_customer():
tests/test_state.py:102:def test_confirm_illegal_states(st):
tests/test_state.py:109:def test_confirm_when_already_confirmed():
tests/test_state.py:117:def test_submit_outside_confirmed(st):
tests/test_state.py:125:def test_remove_unknown_line():
tests/test_state.py:134:def test_add_after_confirmed_demotes_to_ready():
tests/test_state.py:140:def test_remove_after_confirmed_demotes():
tests/test_state.py:146:def test_set_customer_after_confirmed_demotes():
tests/test_state.py:152:def test_confirmation_does_not_survive_demotion():
tests/test_state.py:162:def test_confirm_without_read_back():
tests/test_state.py:169:def test_confirm_with_stale_revision():
tests/test_state.py:179:def test_read_back_of_old_revision_does_not_allow_confirm():
tests/test_state.py:190:def test_revision_increments_on_every_mutation():
tests/test_state.py:199:def test_merge_same_line():
tests/test_state.py:206:def test_same_code_different_extras_is_separate_line():
tests/test_state.py:213:def test_partial_remove():
tests/test_state.py:223:def test_remove_to_empty_and_readd():
tests/test_state.py:231:def test_type_and_code_key_removal():
tests/test_state.py:239:def test_remove_without_qty_clears_all_variants():
tests/test_state.py:247:def test_remove_with_qty_reduces_most_recent_variant():
tests/test_state.py:255:def test_submit_attempt_timestamp_set_once():
tests/test_tools.py:38:def test_known_codes(menu):
tests/test_tools.py:43:def test_tonno_collision_is_per_type(menu):
tests/test_tools.py:49:def test_unknown_code_gives_candidates(menu):
tests/test_tools.py:57:def test_wrong_type_falls_back_to_other_type(menu):
tests/test_tools.py:64:def test_extras_controlled_vocabulary(menu):
tests/test_tools.py:82:def test_auth_error_mapped():
tests/test_tools.py:89:def test_404_mapped():
tests/test_tools.py:94:def test_422_mapped_with_details():
tests/test_tools.py:102:def test_5xx_mapped():
tests/test_tools.py:107:def test_timeout_mapped():
tests/test_tools.py:114:def test_pizzeria_name_startup_check():
tests/test_tools.py:125:def test_submit_parses_order_created():
tests/test_tools.py:188:def test_every_success_carries_full_snapshot(menu, fake):
tests/test_tools.py:202:def test_unknown_item_error_shape(menu, fake):
tests/test_tools.py:212:def test_add_is_atomic(menu, fake):
tests/test_tools.py:224:def test_invalid_quantity_not_parsed(menu, fake):
tests/test_tools.py:234:def test_invalid_extra_via_dispatch(menu, fake):
tests/test_tools.py:242:def test_remove_semantics(menu, fake):
tests/test_tools.py:254:def test_submit_success(menu, fake):
tests/test_tools.py:263:def test_submit_outside_confirmed_is_tool_error(menu, fake):
tests/test_tools.py:271:def test_empty_basket_submit(menu, fake):
tests/test_tools.py:277:def test_submit_timeout_then_recovery_via_list(menu, fake):
tests/test_tools.py:301:def test_recovery_rejects_candidate_with_different_items(menu, fake):
tests/test_tools.py:322:def test_mutation_after_submit_timeout_clears_recovery_state(menu, fake):
tests/test_tools.py:350:def test_submit_timeout_verified_absent_allows_one_retry(menu, fake):
tests/test_tools.py:365:def test_submit_unknown_when_list_unavailable(menu, fake):
tests/test_tools.py:375:def test_submit_422_keeps_basket(menu, fake):
tests/test_tools.py:385:def test_auth_error_no_retry(menu, fake):
tests/test_tools.py:393:def test_street_omitted_from_submit_body(menu, fake):
tests/test_tools.py:418:def test_check_street(menu, fake):
tests/test_tools.py:431:def test_live_acceptance():

 succeeded in 370ms:
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

 succeeded in 403ms:
     1	<!doctype html>
     2	<html lang="de">
     3	<head>
     4	<meta charset="utf-8">
     5	<meta name="viewport" content="width=device-width, initial-scale=1">
     6	<title>Pizza bestellen</title>
     7	<link rel="stylesheet" href="/static/style.css">
     8	</head>
     9	<body>
    10	<header>
    11	  <h1 id="title">Pizza bestellen</h1>
    12	  <label id="tts-wrap" hidden>
    13	    <input type="checkbox" id="tts-toggle"> Antworten vorlesen
    14	  </label>
    15	</header>
    16	
    17	<main id="chat" aria-live="polite"></main>
    18	
    19	<form id="composer">
    20	  <button type="button" id="mic" hidden aria-pressed="false"
    21	          title="Push-to-talk: Klick startet, Klick stoppt">🎤</button>
    22	  <input id="text" autocomplete="off"
    23	         placeholder="Nachricht schreiben …" autofocus>
    24	  <button type="submit" id="send">Senden</button>
    25	</form>
    26	
    27	<script src="/static/app.js"></script>
    28	</body>
    29	</html>

---
     1	/* Web chat over the NDJSON stream. Speech is push-to-talk via
     2	   MediaRecorder + the server's speech proxy — no browser speech APIs. */
     3	"use strict";
     4	
     5	const chat = document.getElementById("chat");
     6	const form = document.getElementById("composer");
     7	const input = document.getElementById("text");
     8	const send = document.getElementById("send");
     9	const mic = document.getElementById("mic");
    10	const ttsWrap = document.getElementById("tts-wrap");
    11	const ttsToggle = document.getElementById("tts-toggle");
    12	
    13	// crypto.randomUUID needs a secure context (HTTPS/localhost); the demo may
    14	// be served over plain HTTP, so fall back to getRandomValues.
    15	const sessionId = crypto.randomUUID
    16	  ? crypto.randomUUID()
    17	  : Array.from(crypto.getRandomValues(new Uint8Array(16)),
    18	               (b) => b.toString(16).padStart(2, "0")).join("");
    19	let speechEnabled = false;
    20	
    21	function add(cls, text) {
    22	  const div = document.createElement("div");
    23	  div.className = "msg " + cls;
    24	  div.textContent = text;
    25	  chat.appendChild(div);
    26	  chat.scrollTop = chat.scrollHeight;
    27	  return div;
    28	}
    29	
    30	function notice(text) {
    31	  const div = document.createElement("div");
    32	  div.className = "notice";
    33	  div.textContent = text;
    34	  chat.appendChild(div);
    35	}
    36	
    37	function stepsBlock() {
    38	  const details = document.createElement("details");
    39	  details.className = "steps";
    40	  details.innerHTML = "<summary>Zwischenschritte</summary>";
    41	  chat.appendChild(details);
    42	  return details;
    43	}
    44	
    45	async function turn(text) {
    46	  send.disabled = true;
    47	  if (text !== null) add("user", text);
    48	  const steps = stepsBlock();
    49	  let finalText = "";
    50	  try {
    51	    const res = await fetch("/chat", {
    52	      method: "POST",
    53	      headers: { "Content-Type": "application/json" },
    54	      body: JSON.stringify({ session_id: sessionId, text }),
    55	    });
    56	    if (!res.ok) throw new Error(await res.text());
    57	    const reader = res.body.getReader();
    58	    const decoder = new TextDecoder();
    59	    let buffer = "";
    60	    for (;;) {
    61	      const { done, value } = await reader.read();
    62	      if (done) break;
    63	      buffer += decoder.decode(value, { stream: true });
    64	      let nl;
    65	      while ((nl = buffer.indexOf("\n")) >= 0) {
    66	        const line = buffer.slice(0, nl); buffer = buffer.slice(nl + 1);
    67	        if (!line.trim()) continue;
    68	        const ev = JSON.parse(line);
    69	        if (ev.type === "tool_call" || ev.type === "tool_result") {
    70	          const pre = document.createElement("pre");
    71	          pre.textContent = (ev.type === "tool_call" ? "→ " : "← ")
    72	            + (ev.tool || "") + " "
    73	            + JSON.stringify(ev.args ?? ev.result);
    74	          steps.appendChild(pre);
    75	        } else if (ev.type === "assistant") {
    76	          finalText = ev.text;
    77	          add("assistant", ev.text);
    78	        } else if (ev.type === "error") {
    79	          notice("Es gab einen technischen Fehler.");
    80	        }
    81	      }
    82	    }
    83	  } catch (err) {
    84	    notice("Verbindung fehlgeschlagen — bitte noch einmal versuchen.");
    85	  }
    86	  if (!steps.querySelector("pre")) steps.remove();
    87	  send.disabled = false;
    88	  input.focus();
    89	  if (finalText && speechEnabled && ttsToggle.checked) speak(finalText);
    90	}
    91	
    92	form.addEventListener("submit", (e) => {
    93	  e.preventDefault();
    94	  const text = input.value.trim();
    95	  if (!text) return;
    96	  input.value = "";
    97	  turn(text);
    98	});
    99	
   100	/* --- speech: push-to-talk, server-proxied ------------------------------ */
   101	
   102	let recorder = null;
   103	
   104	async function startRecording() {
   105	  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
   106	  recorder = new MediaRecorder(stream);
   107	  const chunks = [];
   108	  recorder.ondataavailable = (e) => chunks.push(e.data);
   109	  recorder.onstop = async () => {
   110	    stream.getTracks().forEach((t) => t.stop());
   111	    mic.classList.remove("recording");
   112	    mic.setAttribute("aria-pressed", "false");
   113	    const blob = new Blob(chunks, { type: recorder.mimeType });
   114	    const body = new FormData();
   115	    body.append("audio", blob, "speech.webm");
   116	    try {
   117	      const res = await fetch("/speech/stt", { method: "POST", body });
   118	      if (!res.ok) throw new Error();
   119	      const { text } = await res.json();
   120	      if (text.trim()) turn(text.trim());
   121	      else notice("Ich habe nichts verstanden — bitte noch einmal.");
   122	    } catch {
   123	      notice("Spracherkennung gerade nicht erreichbar — bitte tippen.");
   124	    }
   125	  };
   126	  recorder.start();
   127	  mic.classList.add("recording");
   128	  mic.setAttribute("aria-pressed", "true");
   129	}
   130	
   131	mic.addEventListener("click", () => {
   132	  if (recorder && recorder.state === "recording") recorder.stop();
   133	  else startRecording().catch(() => notice("Kein Mikrofonzugriff."));
   134	});
   135	
   136	async function speak(text) {
   137	  try {
   138	    const res = await fetch("/speech/tts", {
   139	      method: "POST",
   140	      headers: { "Content-Type": "application/json" },
   141	      body: JSON.stringify({ text }),
   142	    });
   143	    if (!res.ok) throw new Error();
   144	    new Audio(URL.createObjectURL(await res.blob())).play();
   145	  } catch {
   146	    notice("Vorlesen gerade nicht möglich.");
   147	  }
   148	}
   149	
   150	/* --- boot -------------------------------------------------------------- */
   151	
   152	(async () => {
   153	  try {
   154	    const cfg = await (await fetch("/config")).json();
   155	    if (cfg.pizzeria) {
   156	      document.getElementById("title").textContent = cfg.pizzeria;
   157	      document.title = cfg.pizzeria;
   158	    }
   159	    // TTS is server-proxied audio and works in any context; only the mic
   160	    // needs getUserMedia/MediaRecorder, which insecure contexts lack.
   161	    speechEnabled = cfg.speech;    // unset SPEECH_URL → nothing rendered
   162	    if (speechEnabled) {
   163	      ttsWrap.hidden = false;
   164	      if (navigator.mediaDevices && window.MediaRecorder) mic.hidden = false;
   165	    }
   166	  } catch { /* text chat works regardless */ }
   167	  turn(null); // opening turn: the agent greets first
   168	})();

---
     1	* { box-sizing: border-box; margin: 0; }
     2	body {
     3	  font: 16px/1.5 system-ui, sans-serif;
     4	  max-width: 720px; margin: 0 auto; padding: 1rem;
     5	  display: flex; flex-direction: column; height: 100vh;
     6	  background: #faf7f2; color: #222;
     7	}
     8	header { display: flex; justify-content: space-between; align-items: baseline; }
     9	h1 { font-size: 1.2rem; padding-bottom: .5rem; }
    10	#tts-wrap { font-size: .85rem; color: #555; }
    11	main { flex: 1; overflow-y: auto; padding: .5rem 0; }
    12	.msg { margin: .4rem 0; padding: .6rem .9rem; border-radius: 12px;
    13	       max-width: 85%; white-space: pre-wrap; }
    14	.user { background: #2f6f4f; color: #fff; margin-left: auto; }
    15	.assistant { background: #fff; border: 1px solid #e5ded2; }
    16	.notice { color: #a33; font-size: .85rem; margin: .3rem 0; }
    17	details.steps { font-size: .78rem; color: #666; margin: .2rem 0 .6rem; }
    18	details.steps summary { cursor: pointer; user-select: none; }
    19	details.steps pre { white-space: pre-wrap; word-break: break-all;
    20	  background: #f2ede4; padding: .4rem .6rem; border-radius: 8px; margin: .2rem 0; }
    21	#composer { display: flex; gap: .5rem; padding-top: .6rem; }
    22	#text { flex: 1; padding: .55rem .8rem; border: 1px solid #ccc;
    23	        border-radius: 10px; font: inherit; }
    24	button { padding: .55rem 1rem; border: 0; border-radius: 10px;
    25	         background: #2f6f4f; color: #fff; font: inherit; cursor: pointer; }
    26	button:disabled { opacity: .5; cursor: default; }
    27	#mic { background: #eee; color: #222; }
    28	#mic.recording { background: #c0392b; color: #fff; animation: pulse 1s infinite; }
    29	@keyframes pulse { 50% { opacity: .6; } }

 succeeded in 368ms:
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
The current web channel is plainly v1-shaped: single fixed pizzeria, `/config` carries only speech and one display name, startup binds one `PizzaSim` client for the whole process, and the UI has no basket, no selector, no footer state, no confirm control. I’m drilling into the tool and agent boundaries now to see which of those can be retrofitted cleanly and which ones threaten silent spec drift.
exec
/bin/bash -lc "nl -ba core/tools.py | sed -n '1,340p'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "python - <<'PY'
import ast, pathlib
base=pathlib.Path('tests')
files=['test_state.py','test_tools.py','test_transcripts.py']
for f in files:
    src=(base/f).read_text()
    tree=ast.parse(src)
    n=0
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
            marks=[]
            if node.decorator_list:
                for d in node.decorator_list:
                    if isinstance(d, ast.Call) and isinstance(d.func, ast.Attribute) and d.func.attr=='parametrize':
                        if len(d.args)>=2 and isinstance(d.args[1], (ast.List, ast.Tuple)):
                            marks.append(len(d.args[1].elts))
            n += max(marks) if marks else 1
    print(f'{f}: {n}')
print('TOTAL:', sum(int(line.split(': ')[1]) for line in []))
PY" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "python - <<'PY'
import ast, pathlib
base=pathlib.Path('tests')
files=['test_state.py','test_tools.py','test_transcripts.py']
total=0
for f in files:
    src=(base/f).read_text()
    tree=ast.parse(src)
    n=0
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
            count=1
            for d in node.decorator_list:
                if isinstance(d, ast.Call) and isinstance(d.func, ast.Attribute) and d.func.attr=='parametrize':
                    if len(d.args)>=2 and isinstance(d.args[1], (ast.List, ast.Tuple)):
                        count*=len(d.args[1].elts)
            n += count
    total += n
    print(f'{f}: {n}')
print('TOTAL:', total)
PY" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "git log --oneline -- reviews/scores.md reviews/round1-plan.md reviews/round2-plan.md reviews/round3-plan.md reviews/round4-impl.md reviews/round5-impl.md reviews/round6-impl.md reviews/round7-hotfix.md reviews/round8-hotfix.md decisions/qa.md core channels tests | sed -n '1,120p'" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 147ms:
     1	"""The eight tool schemas the model sees, plus dispatch.
     2	
     3	Success results always embed the full state snapshot; failures are
     4	{"error": {"code", "message", "candidates"}} with a speakable message.
     5	"""
     6	from __future__ import annotations
     7	
     8	import time
     9	
    10	from . import state
    11	from .menu import Menu, MenuError
    12	from .order import Customer, Item, Order
    13	from .pizzasim import (
    14	    ApiTimeout,
    15	    AuthError,
    16	    PizzaSim,
    17	    PizzaSimError,
    18	    ServerError,
    19	    ValidationError,
    20	)
    21	
    22	_ITEM_SCHEMA = {
    23	    "type": "object",
    24	    "properties": {
    25	        "type": {"type": "string", "enum": ["pizza", "pasta"]},
    26	        "code": {"type": "string"},
    27	        "qty": {"type": "integer", "minimum": 1},
    28	        "extras": {"type": "array", "items": {"type": "string"}},
    29	    },
    30	    "required": ["type", "code", "qty"],
    31	}
    32	
    33	TOOL_SCHEMAS = [
    34	    {"name": "get_menu",
    35	     "description": "The menu: pizzas and pasta with codes and display "
    36	                    "names, and the available extra toppings.",
    37	     "parameters": {"type": "object", "properties": {}}},
    38	    {"name": "add_items",
    39	     "description": "Add items to the basket. Codes must come from "
    40	                    "get_menu. Rejects the whole call if any item or extra "
    41	                    "is unknown.",
    42	     "parameters": {"type": "object",
    43	                    "properties": {"items": {"type": "array",
    44	                                             "items": _ITEM_SCHEMA}},
    45	                    "required": ["items"]}},
    46	    {"name": "remove_item",
    47	     "description": "Remove an item line (or reduce its quantity when qty "
    48	                    "is given).",
    49	     "parameters": {"type": "object",
    50	                    "properties": {
    51	                        "type": {"type": "string",
    52	                                 "enum": ["pizza", "pasta"]},
    53	                        "code": {"type": "string"},
    54	                        "qty": {"type": "integer", "minimum": 1}},
    55	                    "required": ["type", "code"]}},
    56	    {"name": "set_customer",
    57	     "description": "Store the customer's first name and, optionally, "
    58	                    "street.",
    59	     "parameters": {"type": "object",
    60	                    "properties": {
    61	                        "first_name": {"type": "string", "minLength": 1},
    62	                        "street_one": {"type": "string"}},
    63	                    "required": ["first_name"]}},
    64	    {"name": "read_back",
    65	     "description": "The complete order as it stands — read this back to "
    66	                    "the customer before asking for confirmation.",
    67	     "parameters": {"type": "object", "properties": {}}},
    68	    {"name": "confirm_order",
    69	     "description": "Confirm the order after the customer said yes to the "
    70	                    "read-back. revision must be the revision that was "
    71	                    "read back.",
    72	     "parameters": {"type": "object",
    73	                    "properties": {"revision": {"type": "integer"}},
    74	                    "required": ["revision"]}},
    75	    {"name": "submit_order",
    76	     "description": "Send the confirmed order to the kitchen. Only legal "
    77	                    "after confirm_order.",
    78	     "parameters": {"type": "object", "properties": {}}},
    79	    {"name": "check_street",
    80	     "description": "Rough plausibility check of a street name. Not a "
    81	                    "deliverability check — never claim the address was "
    82	                    "verified.",
    83	     "parameters": {"type": "object",
    84	                    "properties": {"street": {"type": "string"}},
    85	                    "required": ["street"]}},
    86	]
    87	
    88	
    89	def openai_tools() -> list[dict]:
    90	    return [{"type": "function", "function": schema}
    91	            for schema in TOOL_SCHEMAS]
    92	
    93	
    94	def _error(code: str, message: str, candidates: list | None = None) -> dict:
    95	    return {"error": {"code": code, "message": message,
    96	                      "candidates": candidates or []}}
    97	
    98	
    99	def _int_qty(value) -> int:
   100	    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
   101	        raise MenuError(
   102	            "invalid_quantity",
   103	            "I need the quantity as a plain number, please.",
   104	            [],
   105	        )
   106	    return value
   107	
   108	
   109	def dispatch(order: Order, menu: Menu, client: PizzaSim,
   110	             name: str, args: dict) -> dict:
   111	    """Execute one tool call. Never raises — every failure is a tool
   112	    result the model must deal with in front of the customer."""
   113	    try:
   114	        return _dispatch(order, menu, client, name, args)
   115	    except MenuError as exc:
   116	        return _error(exc.code, exc.message, exc.candidates)
   117	    except state.TransitionError as exc:
   118	        return _error(exc.code, exc.message)
   119	    except AuthError:
   120	        return _error("api_unavailable",
   121	                      "I can't reach the kitchen system right now.")
   122	    except ApiTimeout:
   123	        return _error("api_unavailable",
   124	                      "The kitchen system isn't answering right now.")
   125	    except PizzaSimError:
   126	        return _error("api_unavailable",
   127	                      "The kitchen system isn't answering right now.")
   128	
   129	
   130	def _dispatch(order: Order, menu: Menu, client: PizzaSim,
   131	              name: str, args: dict) -> dict:
   132	    if name == "get_menu":
   133	        return {"menu": menu.as_tool_result(), "snapshot": order.snapshot()}
   134	
   135	    if name == "add_items":
   136	        items = []
   137	        for raw in args.get("items", []):
   138	            extras = raw.get("extras") or []
   139	            menu.validate_extras(extras)
   140	            items.append(Item(
   141	                type=raw.get("type", ""),
   142	                code=raw.get("code", ""),
   143	                name=menu.display_name(raw.get("type", ""),
   144	                                       raw.get("code", "")),
   145	                qty=_int_qty(raw.get("qty")),
   146	                extras=extras,
   147	            ))  # any failure above rejects the whole call — atomic
   148	        if not items:
   149	            return _error("invalid_quantity", "What can I get you?")
   150	        state.add_items(order, items)
   151	        return {"snapshot": order.snapshot()}
   152	
   153	    if name == "remove_item":
   154	        qty = args.get("qty")
   155	        state.remove_item(order, args.get("type", ""), args.get("code", ""),
   156	                          None if qty is None else _int_qty(qty))
   157	        return {"snapshot": order.snapshot()}
   158	
   159	    if name == "set_customer":
   160	        first_name = (args.get("first_name") or "").strip()
   161	        if not first_name:
   162	            return _error("invalid_state", "I still need a name.")
   163	        customer = Customer(first_name, args.get("street_one") or None)
   164	        state.set_customer(order, customer)
   165	        return {"customer": customer.as_dict(),
   166	                "snapshot": order.snapshot()}
   167	
   168	    if name == "read_back":
   169	        state.read_back(order)
   170	        return {"snapshot": order.snapshot()}
   171	
   172	    if name == "confirm_order":
   173	        revision = args.get("revision")
   174	        if isinstance(revision, bool) or not isinstance(revision, int):
   175	            return _error("stale_revision",
   176	                          "The order changed — let me read it back again.")
   177	        state.confirm(order, revision)
   178	        return {"snapshot": order.snapshot()}
   179	
   180	    if name == "submit_order":
   181	        return _submit(order, client)
   182	
   183	    if name == "check_street":
   184	        result = client.check_street(args.get("street", ""))
   185	        return {"street": result.get("street", ""),
   186	                "deliverable": bool(result.get("deliverable")),
   187	                "snapshot": order.snapshot()}
   188	
   189	    return _error("unknown_tool", "Something went wrong on my side.")
   190	
   191	
   192	_UNSURE = ("I'm not sure that went through — let me check before I try "
   193	           "again.")
   194	
   195	
   196	def _same_items(api_items: list[dict], basket) -> bool:
   197	    def norm(entries):
   198	        return sorted(
   199	            (e["type"], e["code"], e["qty"], tuple(sorted(e["extras"])))
   200	            for e in entries
   201	        )
   202	    ours = [{"type": i.type, "code": i.code, "qty": i.qty,
   203	             "extras": list(i.extras)} for i in basket]
   204	    return norm(api_items) == norm(ours)
   205	
   206	
   207	def _submit(order: Order, client: PizzaSim) -> dict:
   208	    state.begin_submit(order)
   209	
   210	    if order.submit_unknown:
   211	        # A previous attempt timed out: verify against the order list
   212	        # before any retry — a blind retry doubles a real order. The list
   213	        # carries no items, so a shortlisted candidate is verified via the
   214	        # detail endpoint before it is adopted.
   215	        try:
   216	            existing = client.list_orders()
   217	        except PizzaSimError:
   218	            return _error("submit_unknown", _UNSURE)
   219	        cutoff = order.submit_attempted_at - 60  # clock-skew allowance
   220	        matches = [
   221	            o for o in existing
   222	            if o.get("first_name") == order.customer.first_name
   223	            and o.get("created_at", 0) >= cutoff
   224	        ]
   225	        if matches:
   226	            found = max(matches, key=lambda o: o.get("created_at", 0))
   227	            try:
   228	                detail = client.get_order(found["id"])
   229	            except PizzaSimError:
   230	                return _error("submit_unknown", _UNSURE)
   231	            if _same_items(detail.get("items", []), order.items):
   232	                eta = max(0, int(found.get("ready_at", 0) - time.time()))
   233	                state.mark_submitted(order, {
   234	                    "order_id": found["id"],
   235	                    "status": found.get("status", "ordered"),
   236	                    "eta_seconds": eta,
   237	                })
   238	                return {**order.result, "snapshot": order.snapshot()}
   239	        # verified absent (or a different order) → exactly one real retry
   240	
   241	    customer = order.customer.as_dict()
   242	    if customer.get("street_one") is None:
   243	        customer.pop("street_one")
   244	    items = [{"type": i.type, "code": i.code, "qty": i.qty,
   245	              "extras": list(i.extras)} for i in order.items]
   246	    try:
   247	        result = client.submit_order(customer, items)
   248	    except ValidationError as exc:
   249	        return _error("submit_failed",
   250	                      "The kitchen rejected part of the order: "
   251	                      + "; ".join(exc.details))
   252	    except AuthError:
   253	        return _error("api_unavailable",
   254	                      "I can't reach the kitchen system right now.")
   255	    except (ApiTimeout, ServerError):
   256	        order.submit_unknown = True
   257	        return _error("submit_unknown", _UNSURE)
   258	
   259	    state.mark_submitted(order, {
   260	        "order_id": result["order_id"],
   261	        "status": result["status"],
   262	        "eta_seconds": result["eta_seconds"],
   263	    })
   264	    return {**order.result, "snapshot": order.snapshot()}

 exited 127 in 126ms:
/bin/bash: line 1: python: command not found

 exited 127 in 154ms:
/bin/bash: line 1: python: command not found

 succeeded in 207ms:
36131ca Hotfix reviews round 7-8: APPROVED 24/25 after browser-verified fix
2ce8431 Hotfix review follow-up: TTS available without mic support
0580866 Hotfix: end-user browser path over plain HTTP
4ce7523 Implementation review round 3: APPROVED 24/25
49b0fa3 Apply impl review round 2 findings; new SPEC acceptance test implemented
7f2e501 Apply implementation review round 1 findings
e6e237d CLI + web channels, static UI with push-to-talk speech, README, scaffold
635b6b8 Agent loop, prompts, five golden transcripts
0ce98c6 Menu validation, PizzaSim client, tool dispatch + fixture tests
f670920 Core order model + state machine, exhaustive unit tests
a412582 Plan review round 3: APPROVED 24/25
4776e3c Apply plan review round 2 findings; record oracle decision
a133c09 Apply plan review round 1 findings, capture review + scores

codex
`pytest` itself can’t run in this sandbox because there is no writable temp directory, so I’m deriving the test count from the source and cross-checking it against the review trail instead of pretending I executed the suite here.
exec
/bin/bash -lc "python3 - <<'PY'
import ast, pathlib
base=pathlib.Path('tests')
files=['test_state.py','test_tools.py','test_transcripts.py']
total=0
for f in files:
    src=(base/f).read_text()
    tree=ast.parse(src)
    n=0
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
            count=1
            for d in node.decorator_list:
                if isinstance(d, ast.Call) and isinstance(d.func, ast.Attribute) and d.func.attr=='parametrize':
                    if len(d.args)>=2 and isinstance(d.args[1], (ast.List, ast.Tuple)):
                        count*=len(d.args[1].elts)
                    elif len(d.args)>=2 and isinstance(d.args[1], ast.Name):
                        # Resolve simple module-level names like TRANSCRIPTS conservatively.
                        assign = next((n for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id==d.args[1].id for t in n.targets)), None)
                        if assign and isinstance(assign.value, ast.Call) and isinstance(assign.value.func, ast.Name) and assign.value.func.id == 'sorted':
                            # test_transcripts.py also has an explicit count assertion; handle separately.
                            pass
            n += count
    print(f'{f}: {n}')
    total += n
print('STATIC_TOTAL:', total)
print('ADJUSTED_TOTAL_WITH_TRANSCRIPTS_PARAMETRIZE:', total + 4)
PY" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,220p' requirements.txt" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 165ms:
fastapi==0.141.1
httpx==0.28.1
pytest==9.1.1
python-multipart==0.0.32
uvicorn==0.52.0

 succeeded in 205ms:
test_state.py: 34
test_tools.py: 31
test_transcripts.py: 3
STATIC_TOTAL: 68
ADJUSTED_TOTAL_WITH_TRANSCRIPTS_PARAMETRIZE: 72

exec
/bin/bash -lc 'git show 36131ca --stat --oneline' in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 0ms:
36131ca Hotfix reviews round 7-8: APPROVED 24/25 after browser-verified fix
 reviews/round8-hotfix.md | 1496 ++++++++++++++++++++++++++++++++++++++++++++++
 reviews/scores.md        |   29 +
 2 files changed, 1525 insertions(+)

exec
/bin/bash -lc "python3 - <<'PY'
import ast, pathlib
base=pathlib.Path('tests')
state_src=(base/'test_state.py').read_text(); state=ast.parse(state_src)
tools_src=(base/'test_tools.py').read_text(); tools=ast.parse(tools_src)
trans_src=(base/'test_transcripts.py').read_text(); trans=ast.parse(trans_src)

def count(tree, file):
    total=0
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
            count=1
            for d in node.decorator_list:
                if isinstance(d, ast.Call) and isinstance(d.func, ast.Attribute) and d.func.attr=='parametrize':
                    arg=d.args[1]
                    if isinstance(arg, (ast.List, ast.Tuple)):
                        count*=len(arg.elts)
                    elif isinstance(arg, ast.Name) and arg.id=='TRANSCRIPTS':
                        count*=len(list((base/'transcripts').glob('*.json')))
            print(file, node.name, count)
            total += count
    print(file, 'TOTAL', total)
    return total

t = count(state, 'state') + count(tools, 'tools') + count(trans, 'trans')
print('GRAND TOTAL', t)
print('DETERMINISTIC', t-1)
PY" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 0ms:
state test_full_happy_path 1
state test_customer_before_items_is_legal_and_stays_empty 1
state test_submitted_is_terminal 6
state test_remove_from_empty 1
state test_read_back_empty 1
state test_read_back_collecting_needs_customer 1
state test_confirm_illegal_states 2
state test_confirm_when_already_confirmed 1
state test_submit_outside_confirmed 3
state test_remove_unknown_line 1
state test_add_after_confirmed_demotes_to_ready 1
state test_remove_after_confirmed_demotes 1
state test_set_customer_after_confirmed_demotes 1
state test_confirmation_does_not_survive_demotion 1
state test_confirm_without_read_back 1
state test_confirm_with_stale_revision 1
state test_read_back_of_old_revision_does_not_allow_confirm 1
state test_revision_increments_on_every_mutation 1
state test_merge_same_line 1
state test_same_code_different_extras_is_separate_line 1
state test_partial_remove 1
state test_remove_to_empty_and_readd 1
state test_type_and_code_key_removal 1
state test_remove_without_qty_clears_all_variants 1
state test_remove_with_qty_reduces_most_recent_variant 1
state test_submit_attempt_timestamp_set_once 1
state TOTAL 34
tools test_known_codes 1
tools test_tonno_collision_is_per_type 1
tools test_unknown_code_gives_candidates 1
tools test_wrong_type_falls_back_to_other_type 1
tools test_extras_controlled_vocabulary 1
tools test_auth_error_mapped 1
tools test_404_mapped 1
tools test_422_mapped_with_details 1
tools test_5xx_mapped 1
tools test_timeout_mapped 1
tools test_pizzeria_name_startup_check 1
tools test_submit_parses_order_created 1
tools test_every_success_carries_full_snapshot 1
tools test_unknown_item_error_shape 1
tools test_add_is_atomic 1
tools test_invalid_quantity_not_parsed 1
tools test_invalid_extra_via_dispatch 1
tools test_remove_semantics 1
tools test_submit_success 1
tools test_submit_outside_confirmed_is_tool_error 1
tools test_empty_basket_submit 1
tools test_submit_timeout_then_recovery_via_list 1
tools test_recovery_rejects_candidate_with_different_items 1
tools test_mutation_after_submit_timeout_clears_recovery_state 1
tools test_submit_timeout_verified_absent_allows_one_retry 1
tools test_submit_unknown_when_list_unavailable 1
tools test_submit_422_keeps_basket 1
tools test_auth_error_no_retry 1
tools test_street_omitted_from_submit_body 1
tools test_check_street 1
tools test_live_acceptance 1
tools TOTAL 31
trans test_golden_transcript 5
trans test_five_transcripts_exist 1
trans test_gateway_timeout_apology 1
trans TOTAL 7
GRAND TOTAL 72
DETERMINISTIC 71

codex
Findings first.

- The v1 approval trail is real. [reviews/scores.md](/home/rob/bpm-pizza-vibecoding-solution/reviews/scores.md) records plan `24/25`, implementation `24/25`, hotfix `24/25`, and the git history shows the corresponding approval commits through `36131ca`.
- The claimed artifacts exist. `core/` contains the state machine, tool dispatcher, PizzaSim client, and timeout-recovery path in [core/state.py](/home/rob/bpm-pizza-vibecoding-solution/core/state.py), [core/tools.py](/home/rob/bpm-pizza-vibecoding-solution/core/tools.py), [core/pizzasim.py](/home/rob/bpm-pizza-vibecoding-solution/core/pizzasim.py), and [core/agent.py](/home/rob/bpm-pizza-vibecoding-solution/core/agent.py). `channels/cli.py`, `channels/web.py`, and the static web UI files exist. [decisions/qa.md](/home/rob/bpm-pizza-vibecoding-solution/decisions/qa.md) exists and records the `PIZZERIA_LANG` oracle decision.
- The “71 deterministic tests” claim is internally supported by the source, but I could not rerun `pytest` in this sandbox because there is no usable temp directory. Source count is still consistent: 72 total collected cases by definition, of which 1 is the opt-in live acceptance test in [tests/test_tools.py](/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py), leaving 71 deterministic tests.
- The dangerous part is not “is there enough v1 code?” There is. The dangerous part is that v1 bakes in some assumptions that v2 directly kills: one process-wide `PizzaSim` client pinned to one tenant in [channels/web.py](/home/rob/bpm-pizza-vibecoding-solution/channels/web.py), one process-wide language in [core/agent.py](/home/rob/bpm-pizza-vibecoding-solution/core/agent.py), and a web contract/UI that is nowhere close to the new spec in [channels/static/index.html](/home/rob/bpm-pizza-vibecoding-solution/channels/static/index.html) and [channels/static/app.js](/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js). Current UI also does not enforce the new “no message ends unanswered” invariant.

AUDIT: PASS | DISCREPANCIES (`pytest` could not be rerun in this read-only sandbox because no temp dir; test-count verification is from source + review trail, not a fresh execution)

QUESTIONS:
1. `channels/web.py` currently creates one app-wide `PizzaSim` client and one app-wide `Agent`, both bound to a single `PIZZERIA_ID`. How exactly will retrofit remove that singleton tenant assumption without smuggling tenant logic into the transport, and where will per-session `{pizzeria_id, pizzeria_name, menu, order, language}` live?
2. `core/agent.py` bakes `PIZZERIA_LANG` into `AgentConfig.lang`, the system prompt is fixed at session creation, and even fallback apologies use that startup language. V2 requires a UI language switch that affects replies and STT/TTS per session. What is the migration path that avoids stale prompts, mixed-language error messages, and cross-session leakage?
3. Your confirm-control sketch is underspecified. If the button just sends text like “confirm”, the action is not really transport-owned and the model can still miss or mishandle it. If the button calls `confirm_order(revision)` directly, the transport now owns order logic. What is the exact control path that preserves both invariants: “customer action is explicit” and “CONFIRMED only via confirm_order(revision)”?
4. V2 says switching pizzeria starts a fresh conversation and a basket never crosses tenants. Today the session key is just `session_id`, `_get_session()` memoizes one `Session`, and `/chat` serializes only by that key. What happens if the user switches pizzeria while a streamed turn is still in flight, or resends after switch? Where is the race-proof boundary that prevents old-tenant tool results from landing in the new-tenant UI?
5. Prices are not just a view concern. Current `Menu` drops `price`, `Order.snapshot()` has no line prices or total, and the web basket is supposed to reflect what “the code holds.” Are you planning one canonical price/total computation in core, or are you about to duplicate financial display logic in the web layer and risk the UI total diverging from what the agent reads back?
6. The current web channel already violates an important piece of v2 spirit: `app.js` ignores the terminal `done` event, has no explicit “stream ended without final answer” path, no resend affordance, no gateway/API connection state, and no basket/confirm UI. Why are you confident this is an additive retrofit rather than a partial rewrite of the web contract? Be specific about which existing web pieces survive unchanged and why.

PRELIMINARY LEANING: RETROFIT | The core and review trail are worth preserving, but only if you first admit that tenant and language are no longer process-global and that the web contract needs a substantial redesign, not a cosmetic patch.
tokens used
68,389
Findings first.

- The v1 approval trail is real. [reviews/scores.md](/home/rob/bpm-pizza-vibecoding-solution/reviews/scores.md) records plan `24/25`, implementation `24/25`, hotfix `24/25`, and the git history shows the corresponding approval commits through `36131ca`.
- The claimed artifacts exist. `core/` contains the state machine, tool dispatcher, PizzaSim client, and timeout-recovery path in [core/state.py](/home/rob/bpm-pizza-vibecoding-solution/core/state.py), [core/tools.py](/home/rob/bpm-pizza-vibecoding-solution/core/tools.py), [core/pizzasim.py](/home/rob/bpm-pizza-vibecoding-solution/core/pizzasim.py), and [core/agent.py](/home/rob/bpm-pizza-vibecoding-solution/core/agent.py). `channels/cli.py`, `channels/web.py`, and the static web UI files exist. [decisions/qa.md](/home/rob/bpm-pizza-vibecoding-solution/decisions/qa.md) exists and records the `PIZZERIA_LANG` oracle decision.
- The “71 deterministic tests” claim is internally supported by the source, but I could not rerun `pytest` in this sandbox because there is no usable temp directory. Source count is still consistent: 72 total collected cases by definition, of which 1 is the opt-in live acceptance test in [tests/test_tools.py](/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py), leaving 71 deterministic tests.
- The dangerous part is not “is there enough v1 code?” There is. The dangerous part is that v1 bakes in some assumptions that v2 directly kills: one process-wide `PizzaSim` client pinned to one tenant in [channels/web.py](/home/rob/bpm-pizza-vibecoding-solution/channels/web.py), one process-wide language in [core/agent.py](/home/rob/bpm-pizza-vibecoding-solution/core/agent.py), and a web contract/UI that is nowhere close to the new spec in [channels/static/index.html](/home/rob/bpm-pizza-vibecoding-solution/channels/static/index.html) and [channels/static/app.js](/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js). Current UI also does not enforce the new “no message ends unanswered” invariant.

AUDIT: PASS | DISCREPANCIES (`pytest` could not be rerun in this read-only sandbox because no temp dir; test-count verification is from source + review trail, not a fresh execution)

QUESTIONS:
1. `channels/web.py` currently creates one app-wide `PizzaSim` client and one app-wide `Agent`, both bound to a single `PIZZERIA_ID`. How exactly will retrofit remove that singleton tenant assumption without smuggling tenant logic into the transport, and where will per-session `{pizzeria_id, pizzeria_name, menu, order, language}` live?
2. `core/agent.py` bakes `PIZZERIA_LANG` into `AgentConfig.lang`, the system prompt is fixed at session creation, and even fallback apologies use that startup language. V2 requires a UI language switch that affects replies and STT/TTS per session. What is the migration path that avoids stale prompts, mixed-language error messages, and cross-session leakage?
3. Your confirm-control sketch is underspecified. If the button just sends text like “confirm”, the action is not really transport-owned and the model can still miss or mishandle it. If the button calls `confirm_order(revision)` directly, the transport now owns order logic. What is the exact control path that preserves both invariants: “customer action is explicit” and “CONFIRMED only via confirm_order(revision)”?
4. V2 says switching pizzeria starts a fresh conversation and a basket never crosses tenants. Today the session key is just `session_id`, `_get_session()` memoizes one `Session`, and `/chat` serializes only by that key. What happens if the user switches pizzeria while a streamed turn is still in flight, or resends after switch? Where is the race-proof boundary that prevents old-tenant tool results from landing in the new-tenant UI?
5. Prices are not just a view concern. Current `Menu` drops `price`, `Order.snapshot()` has no line prices or total, and the web basket is supposed to reflect what “the code holds.” Are you planning one canonical price/total computation in core, or are you about to duplicate financial display logic in the web layer and risk the UI total diverging from what the agent reads back?
6. The current web channel already violates an important piece of v2 spirit: `app.js` ignores the terminal `done` event, has no explicit “stream ended without final answer” path, no resend affordance, no gateway/API connection state, and no basket/confirm UI. Why are you confident this is an additive retrofit rather than a partial rewrite of the web contract? Be specific about which existing web pieces survive unchanged and why.

PRELIMINARY LEANING: RETROFIT | The core and review trail are worth preserving, but only if you first admit that tenant and language are no longer process-global and that the web contract needs a substantial redesign, not a cosmetic patch.
