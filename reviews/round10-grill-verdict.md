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

 succeeded in 151ms:
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

 succeeded in 259ms:
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
I have the v2 spec loaded. Now I’m pulling the earlier six questions and the current implementation points they target so I can grade each answer against concrete code structure rather than against the implementer’s narrative.
exec
/bin/bash -lc "sed -n '1,260p' channels/web.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' core/tools.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' core/agent.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc 'rg -n "''^QUESTIONS:|''^1'"\\.|"'^2'"\\.|"'^3'"\\.|"'^4'"\\.|"'^5'"\\.|"'^6'"\\.|"'^PRELIMINARY" reviews/round9-audit-grill.md' in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' channels/static/app.js" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 271ms:
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

 succeeded in 278ms:
27:QUESTIONS: numbered list, max 6
28:PRELIMINARY LEANING: RETROFIT | RESTART | UNDECIDED (one line why)
277:1. Devil's advocate: attack the plan — gaps, wrong assumptions, missing error cases, spec violations.
278:2. Judge: score against the fixed rubric.
478:1. **Order response field name: `order_id`.** A successful
483:2. **The list endpoint exists.** `GET /pizzerias/{id}/orders` (auth:
498:1. Devil's advocate: attack the plan — gaps, wrong assumptions, missing error cases, spec violations.
499:2. Judge: score against the fixed rubric.
719:1. Devil's advocate: attack the plan — gaps, wrong assumptions, missing error cases, spec violations.
720:2. Judge: score against the fixed rubric.
767:1. Devil's advocate: attack the plan — gaps, wrong assumptions, missing error cases, spec violations.
768:2. Judge: score against the fixed rubric.
940:1. Devil's advocate: attack the implementation — bugs, gaps, missing error cases, spec violations, divergence from the approved plan.
941:2. Judge: score against the fixed rubric.
1161:1. Devil's advocate: attack the implementation — bugs, gaps, missing error cases, spec violations, divergence from the approved plan.
1162:2. Judge: score against the fixed rubric.
1167:1. remove_item ambiguity with same (type, code) and different extras → deterministic semantics in core/state.py (no qty removes all matching lines; qty reduces the most recently added), documented in PLAN.md tool table, tested in tests/test_state.py (test_remove_without_qty_clears_all_variants, test_remove_with_qty_reduces_most_recent_variant). The spec fixes remove_item's parameters, so an extras parameter was not an option.
1168:2. Speech probe now requires 2xx (raise_for_status) in channels/web.py.
1169:3. Gateway timeout aligned to the plan's 30s in core/agent.py.
1170:4. requirements.txt pinned to exact versions.
1382:1. Devil's advocate: attack the implementation — bugs, gaps, missing error cases, spec violations.
1383:2. Judge: score against the fixed rubric.
1388:1. Mutations clear submit_unknown/submit_attempted_at (core/state.py _recompute); tested in tests/test_tools.py::test_mutation_after_submit_timeout_clears_recovery_state.
1389:2. Web /chat serializes turns per session (lock; 409 when a turn is in flight) in channels/web.py.
1390:3. Gateway-timeout and loop-guard apology paths emit assistant events (core/agent.py), so the web UI shows the apology and it is logged.
1391:4. GET /config returns exactly {speech: bool}.
2157:1. Load and validate all required env vars (exit naming var + file).
2158:2. `GET /pizzerias` with `X-API-Key` — a 401/403 aborts startup ("cannot
2162:3. `GET /menu` — failure aborts startup with "We're not taking orders right
2789:1. `POST /pizzerias/{PIZZERIA_ID}/orders` returned an order id.
2790:2. Reading that pizzeria's orders back shows the order, and it is visible on the
2792:3. The customer name is the one the customer gave.
2793:4. The items and quantities are the ones that were read back and confirmed —
2914:1. **Order response field name: `order_id`.** A successful
2919:2. **The list endpoint exists.** `GET /pizzerias/{id}/orders` (auth:
2928:3. **Menu item shape:** `{"code", "name", "base": [ingredients], "price"}`.
2933:4. **`extras[]` is a controlled vocabulary:** the top-level `toppings[]` from
2938:5. **Error bodies are machine-readable:**
2943:6. **Status values observed in the lifecycle:** `ordered` →
6542:QUESTIONS:
6543:1. `channels/web.py` currently creates one app-wide `PizzaSim` client and one app-wide `Agent`, both bound to a single `PIZZERIA_ID`. How exactly will retrofit remove that singleton tenant assumption without smuggling tenant logic into the transport, and where will per-session `{pizzeria_id, pizzeria_name, menu, order, language}` live?
6544:2. `core/agent.py` bakes `PIZZERIA_LANG` into `AgentConfig.lang`, the system prompt is fixed at session creation, and even fallback apologies use that startup language. V2 requires a UI language switch that affects replies and STT/TTS per session. What is the migration path that avoids stale prompts, mixed-language error messages, and cross-session leakage?
6545:3. Your confirm-control sketch is underspecified. If the button just sends text like “confirm”, the action is not really transport-owned and the model can still miss or mishandle it. If the button calls `confirm_order(revision)` directly, the transport now owns order logic. What is the exact control path that preserves both invariants: “customer action is explicit” and “CONFIRMED only via confirm_order(revision)”?
6546:4. V2 says switching pizzeria starts a fresh conversation and a basket never crosses tenants. Today the session key is just `session_id`, `_get_session()` memoizes one `Session`, and `/chat` serializes only by that key. What happens if the user switches pizzeria while a streamed turn is still in flight, or resends after switch? Where is the race-proof boundary that prevents old-tenant tool results from landing in the new-tenant UI?
6547:5. Prices are not just a view concern. Current `Menu` drops `price`, `Order.snapshot()` has no line prices or total, and the web basket is supposed to reflect what “the code holds.” Are you planning one canonical price/total computation in core, or are you about to duplicate financial display logic in the web layer and risk the UI total diverging from what the agent reads back?
6548:6. The current web channel already violates an important piece of v2 spirit: `app.js` ignores the terminal `done` event, has no explicit “stream ended without final answer” path, no resend affordance, no gateway/API connection state, and no basket/confirm UI. Why are you confident this is an additive retrofit rather than a partial rewrite of the web contract? Be specific about which existing web pieces survive unchanged and why.
6550:PRELIMINARY LEANING: RETROFIT | The core and review trail are worth preserving, but only if you first admit that tenant and language are no longer process-global and that the web contract needs a substantial redesign, not a cosmetic patch.
6562:QUESTIONS:
6563:1. `channels/web.py` currently creates one app-wide `PizzaSim` client and one app-wide `Agent`, both bound to a single `PIZZERIA_ID`. How exactly will retrofit remove that singleton tenant assumption without smuggling tenant logic into the transport, and where will per-session `{pizzeria_id, pizzeria_name, menu, order, language}` live?
6564:2. `core/agent.py` bakes `PIZZERIA_LANG` into `AgentConfig.lang`, the system prompt is fixed at session creation, and even fallback apologies use that startup language. V2 requires a UI language switch that affects replies and STT/TTS per session. What is the migration path that avoids stale prompts, mixed-language error messages, and cross-session leakage?
6565:3. Your confirm-control sketch is underspecified. If the button just sends text like “confirm”, the action is not really transport-owned and the model can still miss or mishandle it. If the button calls `confirm_order(revision)` directly, the transport now owns order logic. What is the exact control path that preserves both invariants: “customer action is explicit” and “CONFIRMED only via confirm_order(revision)”?
6566:4. V2 says switching pizzeria starts a fresh conversation and a basket never crosses tenants. Today the session key is just `session_id`, `_get_session()` memoizes one `Session`, and `/chat` serializes only by that key. What happens if the user switches pizzeria while a streamed turn is still in flight, or resends after switch? Where is the race-proof boundary that prevents old-tenant tool results from landing in the new-tenant UI?
6567:5. Prices are not just a view concern. Current `Menu` drops `price`, `Order.snapshot()` has no line prices or total, and the web basket is supposed to reflect what “the code holds.” Are you planning one canonical price/total computation in core, or are you about to duplicate financial display logic in the web layer and risk the UI total diverging from what the agent reads back?
6568:6. The current web channel already violates an important piece of v2 spirit: `app.js` ignores the terminal `done` event, has no explicit “stream ended without final answer” path, no resend affordance, no gateway/API connection state, and no basket/confirm UI. Why are you confident this is an additive retrofit rather than a partial rewrite of the web contract? Be specific about which existing web pieces survive unchanged and why.
6570:PRELIMINARY LEANING: RETROFIT | The core and review trail are worth preserving, but only if you first admit that tenant and language are no longer process-global and that the web contract needs a substantial redesign, not a cosmetic patch.

 succeeded in 316ms:
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

 succeeded in 320ms:
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

 succeeded in 267ms:
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

codex
The current code confirms the exact weak points I asked about: app-wide tenant/client, startup language in `AgentConfig`, and a thin web contract. I’m checking the order/menu/state shapes next so I can decide whether the proposed price and confirmation retrofits are actually coherent.
exec
/bin/bash -lc "sed -n '1,260p' core/state.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' core/menu.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' core/order.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' core/pizzasim.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' tests/fixtures/menu.json" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 161ms:
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

 succeeded in 293ms:
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

 succeeded in 324ms:
"""PizzaSim API client: httpx, explicit timeouts, typed errors.

Also owns the env-config loading shared by the whole app: process env wins,
else ~/.env if present (never written, never printed).
"""
from __future__ import annotations

import os
from pathlib import Path

import httpx

ENV_FILE = Path.home() / ".env"
_TIMEOUT = httpx.Timeout(10.0)


class ConfigError(Exception):
    pass


def _env_file_values() -> dict[str, str]:
    values: dict[str, str] = {}
    if ENV_FILE.is_file():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                values[key.strip()] = val.strip().strip('"').strip("'")
    return values


def require_env(name: str) -> str:
    value = os.environ.get(name) or _env_file_values().get(name)
    if not value:
        raise ConfigError(
            f"{name} is not set (expected in the environment or {ENV_FILE})"
        )
    return value


def optional_env(name: str) -> str | None:
    return os.environ.get(name) or _env_file_values().get(name) or None


class PizzaSimError(Exception):
    """Base for typed API errors."""


class AuthError(PizzaSimError):
    pass


class NotFoundError(PizzaSimError):
    pass


class ValidationError(PizzaSimError):
    def __init__(self, details: list[str]):
        super().__init__("; ".join(details))
        self.details = details


class ServerError(PizzaSimError):
    pass


class ApiTimeout(PizzaSimError):
    pass


def _raise_for(response: httpx.Response) -> None:
    if response.status_code in (401, 403):
        raise AuthError(f"auth rejected ({response.status_code})")
    if response.status_code == 404:
        raise NotFoundError("not found")
    if response.status_code == 422:
        try:
            details = response.json().get("details", [])
        except ValueError:
            details = []
        raise ValidationError(details or ["invalid request"])
    if response.status_code >= 500:
        raise ServerError(f"server error ({response.status_code})")
    response.raise_for_status()


class PizzaSim:
    def __init__(self, base_url: str, api_key: str, pizzeria_id: str,
                 transport: httpx.BaseTransport | None = None):
        self.pizzeria_id = pizzeria_id
        self._client = httpx.Client(
            base_url=base_url.rstrip("/"),
            headers={"X-API-Key": api_key},
            timeout=_TIMEOUT,
            transport=transport,
        )

    @classmethod
    def from_env(cls) -> "PizzaSim":
        return cls(
            require_env("PIZZASIM_URL"),
            require_env("PIZZASIM_API_KEY"),
            require_env("PIZZERIA_ID"),
        )

    def _request(self, method: str, path: str, **kw) -> dict:
        try:
            response = self._client.request(method, path, **kw)
        except httpx.TimeoutException as exc:
            raise ApiTimeout(str(exc)) from exc
        except httpx.HTTPError as exc:
            raise ServerError(str(exc)) from exc
        _raise_for(response)
        return response.json()

    def get_menu(self) -> dict:
        return self._request("GET", "/menu")

    def list_pizzerias(self) -> list[dict]:
        return self._request("GET", "/pizzerias")["pizzerias"]

    def pizzeria_name(self) -> str:
        """Startup step 2: auth + tenant check. Unknown PIZZERIA_ID is the
        404-pizzeria case — the process must refuse to start."""
        for pizzeria in self.list_pizzerias():
            if pizzeria["id"] == self.pizzeria_id:
                return pizzeria["name"]
        raise NotFoundError(
            f"pizzeria {self.pizzeria_id} not found on the PizzaSim server"
        )

    def list_orders(self) -> list[dict]:
        return self._request(
            "GET", f"/pizzerias/{self.pizzeria_id}/orders"
        )["orders"]

    def get_order(self, order_id: str) -> dict:
        """Full order incl. customer and items — the list endpoint carries
        neither."""
        return self._request(
            "GET", f"/pizzerias/{self.pizzeria_id}/orders/{order_id}"
        )

    def submit_order(self, customer: dict, items: list[dict]) -> dict:
        """The only network write. Returns order_id, status, eta_seconds."""
        return self._request(
            "POST",
            f"/pizzerias/{self.pizzeria_id}/orders",
            json={"customer": customer, "items": items},
        )

    def check_street(self, street: str) -> dict:
        return self._request("GET", "/location", params={"street": street})

 succeeded in 357ms:
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

 succeeded in 323ms:
{"toppings":["mozzarella","mushrooms","smoked_ham","salami","onions","garlic","pepperoni","pineapple","artichokes","basil","bell_pepper","tuna"],"pizzas":[{"code":"margherita","name":"Margherita","base":["dough","tomatoes","mozzarella","basil"],"price":8.5},{"code":"prosciutto","name":"Prosciutto","base":["dough","tomatoes","mozzarella","smoked_ham"],"price":9.5},{"code":"salami","name":"Salami","base":["dough","tomatoes","mozzarella","salami"],"price":9.5},{"code":"funghi","name":"Funghi","base":["dough","tomatoes","mozzarella","mushrooms"],"price":9},{"code":"regina","name":"Regina","base":["dough","tomatoes","mozzarella","smoked_ham","mushrooms"],"price":10.5},{"code":"mista","name":"Mista","base":["dough","tomatoes","mozzarella","salami","smoked_ham","mushrooms"],"price":11.5},{"code":"hawaii","name":"Hawaii","base":["dough","tomatoes","mozzarella","smoked_ham","pineapple"],"price":10},{"code":"tonno","name":"Tonno","base":["dough","tomatoes","mozzarella","tuna","onions"],"price":10.5},{"code":"papa","name":"Papa","base":["dough","tomatoes","mozzarella","tuna","onions","garlic"],"price":11},{"code":"diavolo","name":"Diavolo","base":["dough","tomatoes","mozzarella","salami","bell_pepper","pepperoni"],"price":11},{"code":"grandiosa","name":"Grandiosa","base":["dough","tomatoes","mozzarella","smoked_ham","salami","mushrooms","bell_pepper","artichokes","onions"],"price":13.5}],"pasta":[{"code":"aglioolio","name":"Pasta Aglio & Olio","base":["pasta","garlic","basil"],"price":9},{"code":"tonno","name":"Pasta Tonno","base":["pasta","tuna"],"price":8.5},{"code":"funghi","name":"Pasta Funghi","base":["pasta","mushrooms"],"price":8.5},{"code":"pesto","name":"Pasta Pesto","base":["pasta","pesto"],"price":8.5}]}
codex
There’s one possible fault line left: whether `PIZZERIA_LANG` even survives in v2, because the new env table appears to drop it while still requiring a per-session switch. I’m verifying that before I hand down the verdict.
exec
/bin/bash -lc 'rg -n "PIZZERIA_LANG|language switch|Languages:|greeting-language" SPEC.md SPEC_20260801.md PLAN.md README.md reviews/round9-audit-grill.md' in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc 'rg -n "confirm_order|read_back|/config|done event|resend|connection state|APP_VERSION|dashboard|pizzerias" channels/static/index.html channels/static/style.css channels/static/app.js channels/web.py core/agent.py core/tools.py core/order.py' in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 181ms:
reviews/round9-audit-grill.md:19:SPEC.md was just replaced by the operator with v2 (git show HEAD -- SPEC.md; previous version is SPEC_20260801.md and in git history). Delta: prices + basket total in scope; multi-pizzeria (customer-selectable in the UI, PIZZERIA_ID only preselects; basket never crosses tenants; fresh conversation on switch); APP_VERSION env shown in footer; an entirely new "The web channel" section (header: pizzeria name, selector from GET /pizzerias with short UUIDs, dashboard link per pizzeria, DE/EN language switch applied to replies and speech, start-over; footer: version, full UUID, connection state for API+gateway, API docs link; "no message ends unanswered" invariant; visible basket with total; read-back with an explicit confirm CONTROL; basket locked after submit); mandatory headless-browser E2E tests incl. three failure paths; getUserMedia/MediaRecorder now explicitly sanctioned.
reviews/round9-audit-grill.md:21:The implementer's position, which you must attack: RETROFIT the existing codebase (do not restart from scratch). Rationale: the unchanged spec sections (soul, load-bearing idea, state machine, tools, error handling, anti-patterns, speech service, CLI) are already built, reviewed and tested (71 tests); the delta is additive and concentrated in the web layer + a session-level tenancy generalization + price fields; a restart would rewrite identical core code with fresh bug risk and lose the review trail. Planned retrofit sketch: (a) core: menu carries prices, get_menu/read_back expose price + basket total; PizzaSim client instantiated per session for the session's pizzeria (preselected id validated at startup; selector list from GET /pizzerias); (b) web: new header/footer/basket UI per spec, confirm control wired as customer action, language switch selects prompt+STT language per session (PIZZERIA_LANG stays the startup default), APP_VERSION required env; (c) tests: extend unit/tool tests for prices+tenancy, add Playwright browser E2E incl. the three failure paths (Playwright already proven working on this host); (d) PLAN.md updated first, re-reviewed before implementation.
reviews/round9-audit-grill.md:23:Attack this: where does retrofit risk silently violating v2? Is any v1 architectural decision now invalid (e.g. one client per process, PIZZERIA_LANG required var vs the new UI language switch, /config contract)? Is the confirm-control design sound given "the transport owns no order logic" and "CONFIRMED only via confirm_order(revision)"? Would a restart actually be cheaper or safer anywhere? Ask your hardest questions (max 6, numbered) — the implementer will answer them in the next call before you give a verdict. If the audit in JOB 1 found discrepancies, include them as questions.
reviews/round9-audit-grill.md:391:- **Languages:** German and English. The agent answers in the language the
reviews/round9-audit-grill.md:678:- **Languages:** German and English. The agent answers in the language the
reviews/round9-audit-grill.md:722:Task: Read SPEC.md (the source of truth) and PLAN.md (the stage-1 implementation plan under review, round 3 of max 3). Judge whether PLAN.md is a complete, correct, spec-compliant plan such that implementing exactly it satisfies SPEC.md. The "Contract facts" section in SPEC.md was verified against the live API and is trustworthy. decisions/qa.md records an oracle decision on the greeting language (required env var PIZZERIA_LANG) taken between rounds.
reviews/round9-audit-grill.md:724:Round 2 (stateless, see reviews/round2-plan.md) required: (1) one exact tool-result contract per tool composing the per-tool table with the full-current-state rule, and fixing an eta_minutes test regression; (2) a spec-compliant, non-hardcoded, non-UI source for the greeting language; (3) explicit persisted state for submit-timeout recovery correlation; (4) removing lang from the chat contract or fencing it to an STT hint; (5) per-session immutable menu snapshot ownership. All five were addressed in the current PLAN.md — verify in the file, do not take this note on faith: see the SNAPSHOT definition in "Tool schemas", the PIZZERIA_LANG paragraph in "Configuration", submit_attempted_at in the state-machine section, the web protocol section, and the "Session model" paragraph.
reviews/round9-audit-grill.md:2038:Which mechanism: (a) optional env `PIZZERIA_LANG` default de, (b) required
reviews/round9-audit-grill.md:2041:**A (decision):** **(b)** — `PIZZERIA_LANG` (de|en) is a required env var.
reviews/round9-audit-grill.md:2044:before the first turn naming `PIZZERIA_LANG` and where it was expected; no
reviews/round9-audit-grill.md:2138:| `core/agent.py` | `LITELLM_PIZZA_URL`, `LITELLM_PIZZA_KEY`, `LITELLM_PIZZA_MODEL_1`, `PIZZERIA_LANG` (all required; `LITELLM_PIZZA_MODEL_2` read but unused — single-model build) |
reviews/round9-audit-grill.md:2142:`PIZZERIA_LANG` ∈ {`de`, `en`} is the pizzeria-country greeting language.
reviews/round9-audit-grill.md:2294:The agent greets first, in the language set by `PIZZERIA_LANG`, and answers
reviews/round9-audit-grill.md:2366:greeting language now required env var PIZZERIA_LANG (oracle decision in
reviews/round9-audit-grill.md:2369:hint = PIZZERIA_LANG only; per-session immutable menu snapshot defined via
reviews/round9-audit-grill.md:2475: - **Languages:** German and English. The agent answers in the language the
reviews/round9-audit-grill.md:2826:- **Languages:** German and English. The agent answers in the language the
reviews/round9-audit-grill.md:3970:    40	    lang: str  # PIZZERIA_LANG: greeting language = pizzeria country
reviews/round9-audit-grill.md:3974:    44	        lang = require_env("PIZZERIA_LANG").lower()
reviews/round9-audit-grill.md:3977:    47	                "PIZZERIA_LANG must be 'de' or 'en', got something else"
reviews/round9-audit-grill.md:5468:    40	    lang: str  # PIZZERIA_LANG: greeting language = pizzeria country
reviews/round9-audit-grill.md:5472:    44	        lang = require_env("PIZZERIA_LANG").lower()
reviews/round9-audit-grill.md:5475:    47	                "PIZZERIA_LANG must be 'de' or 'en', got something else"
reviews/round9-audit-grill.md:6536:- The claimed artifacts exist. `core/` contains the state machine, tool dispatcher, PizzaSim client, and timeout-recovery path in [core/state.py](/home/rob/bpm-pizza-vibecoding-solution/core/state.py), [core/tools.py](/home/rob/bpm-pizza-vibecoding-solution/core/tools.py), [core/pizzasim.py](/home/rob/bpm-pizza-vibecoding-solution/core/pizzasim.py), and [core/agent.py](/home/rob/bpm-pizza-vibecoding-solution/core/agent.py). `channels/cli.py`, `channels/web.py`, and the static web UI files exist. [decisions/qa.md](/home/rob/bpm-pizza-vibecoding-solution/decisions/qa.md) exists and records the `PIZZERIA_LANG` oracle decision.
reviews/round9-audit-grill.md:6544:2. `core/agent.py` bakes `PIZZERIA_LANG` into `AgentConfig.lang`, the system prompt is fixed at session creation, and even fallback apologies use that startup language. V2 requires a UI language switch that affects replies and STT/TTS per session. What is the migration path that avoids stale prompts, mixed-language error messages, and cross-session leakage?
reviews/round9-audit-grill.md:6556:- The claimed artifacts exist. `core/` contains the state machine, tool dispatcher, PizzaSim client, and timeout-recovery path in [core/state.py](/home/rob/bpm-pizza-vibecoding-solution/core/state.py), [core/tools.py](/home/rob/bpm-pizza-vibecoding-solution/core/tools.py), [core/pizzasim.py](/home/rob/bpm-pizza-vibecoding-solution/core/pizzasim.py), and [core/agent.py](/home/rob/bpm-pizza-vibecoding-solution/core/agent.py). `channels/cli.py`, `channels/web.py`, and the static web UI files exist. [decisions/qa.md](/home/rob/bpm-pizza-vibecoding-solution/decisions/qa.md) exists and records the `PIZZERIA_LANG` oracle decision.
reviews/round9-audit-grill.md:6564:2. `core/agent.py` bakes `PIZZERIA_LANG` into `AgentConfig.lang`, the system prompt is fixed at session creation, and even fallback apologies use that startup language. V2 requires a UI language switch that affects replies and STT/TTS per session. What is the migration path that avoids stale prompts, mixed-language error messages, and cross-session leakage?
README.md:27:The agent greets first, in the language set by `PIZZERIA_LANG`, and answers
SPEC_20260801.md:125:- **Languages:** German and English. The agent answers in the language the
SPEC.md:125:- **Languages:** German and English. The agent answers in the language the
PLAN.md:92:| `core/agent.py` | `LITELLM_PIZZA_URL`, `LITELLM_PIZZA_KEY`, `LITELLM_PIZZA_MODEL_1`, `PIZZERIA_LANG` (all required; `LITELLM_PIZZA_MODEL_2` read but unused — single-model build) |
PLAN.md:96:`PIZZERIA_LANG` ∈ {`de`, `en`} is the pizzeria-country greeting language.
PLAN.md:223:  `lang = PIZZERIA_LANG` — the pizzeria-country greeting language, a
PLAN.md:264:  never a UI control — the greeting comes from `PIZZERIA_LANG`, mirroring
PLAN.md:272:  `PIZZERIA_LANG` as the language hint (an STT hint only — it never
PLAN.md:330:   ☐ `.env.example` lists all 12 vars (incl. `PIZZERIA_LANG`), names only

 succeeded in 190ms:
core/tools.py:64:    {"name": "read_back",
core/tools.py:68:    {"name": "confirm_order",
core/tools.py:77:                    "after confirm_order.",
core/tools.py:168:    if name == "read_back":
core/tools.py:169:        state.read_back(order)
core/tools.py:172:    if name == "confirm_order":
channels/web.py:78:@app.get("/config")
channels/static/app.js:154:    const cfg = await (await fetch("/config")).json();
core/order.py:42:    read_back_revision: int | None = None
core/order.py:64:            "read_back_done": self.read_back_revision == self.revision,

codex
VERDICT: RETROFIT
CONDITIONS:
- A2 is not acceptable as stated unless `PIZZERIA_LANG` is explicitly restored to `SPEC.md` and the config contract; v2’s current env table omits it, so retrofit cannot keep a hidden required env var or undocumented default.
- Tenancy must move into a core-owned session factory with immutable per-session `{pizzeria_id, pizzeria_name, client, menu, lang, order, messages}`; the web layer may pass identifiers, but it must not mutate tenant state in place or keep an app-wide tenant-bound client/agent.
- The confirm path must be exactly the A3 design: explicit UI control -> `POST /confirm {session_id, revision}` -> one core method that dispatches `confirm_order(revision)` then `submit_order`, appends synthetic tool messages/results, and rejects stale revisions.
- The web channel must be treated as a substantial rewrite, not an additive patch: done-event handling, explicit unanswered/resend paths, header/footer contract, basket+total, connection states, start-over, and switch-race abandonment with fresh session IDs are mandatory.
- Price and basket-total computation must be canonical in core only, copied into item snapshots at add time, surfaced through tool results/read-back, and covered by deterministic unit tests plus Playwright E2E for tenant switching and the three required failure paths.
tokens used
34,965
VERDICT: RETROFIT
CONDITIONS:
- A2 is not acceptable as stated unless `PIZZERIA_LANG` is explicitly restored to `SPEC.md` and the config contract; v2’s current env table omits it, so retrofit cannot keep a hidden required env var or undocumented default.
- Tenancy must move into a core-owned session factory with immutable per-session `{pizzeria_id, pizzeria_name, client, menu, lang, order, messages}`; the web layer may pass identifiers, but it must not mutate tenant state in place or keep an app-wide tenant-bound client/agent.
- The confirm path must be exactly the A3 design: explicit UI control -> `POST /confirm {session_id, revision}` -> one core method that dispatches `confirm_order(revision)` then `submit_order`, appends synthetic tool messages/results, and rejects stale revisions.
- The web channel must be treated as a substantial rewrite, not an additive patch: done-event handling, explicit unanswered/resend paths, header/footer contract, basket+total, connection states, start-over, and switch-race abandonment with fresh session IDs are mandatory.
- Price and basket-total computation must be canonical in core only, copied into item snapshots at add time, surfaced through tool results/read-back, and covered by deterministic unit tests plus Playwright E2E for tenant switching and the three required failure paths.
