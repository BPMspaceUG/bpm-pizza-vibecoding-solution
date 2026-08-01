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
session id: 019fbc60-8ee6-7781-a4ab-78f7951c8c6e
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

**Judge: Codex** (canonical sanitized invocation; payload = this issue fetched live). Verdict verbatim:

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
```

**Producer revision** addressing all five round-1 issues — verify in the committed PLAN.md:

1. Notice-language rule made explicit ("Answer invariant" section): UI-generated text follows `session.lang` as the customer's declared language; no language detection in the UI (rationale given); E2E-tested (switch to EN → English notices). One-line rebuttal per protocol: the UI cannot know the "latest message language" without a detection heuristic, which would be a parser-shaped guess — the header switch is the customer's declaration toward the UI, while model replies keep per-turn mirroring.
2. Vanished-tenant path specified: 409 → UI re-fetches /config (fresh GET /pizzerias) → selector re-rendered from the live list or "list unavailable"; TestClient + E2E scenario 2b added.
3. Speech behaviour section added: TTS language from session.lang, synthesis off by default and final-message-only, spoken-answer policy activated via a `spoken: true` flag on /chat with a unit test, push-to-talk/failure semantics, manual checklist retained.
4. Web-surface coverage for carried-over error rows: 401/403, 422, submit 5xx/timeout-unknown, empty-basket submit each asserted as rendered outcomes (golden transcripts / TestClient stream assertions / E2E), stated in "Error handling".
5. Confirm path made symmetric: every dispatch (success or failure) is appended to session.messages as synthetic tool_calls + tool results and logged identically; one model call phrases success or refusal; nothing submitted on failed confirm ("Confirm control" section).

Re-review requested against the same rubric (round 2 of max 3).

**Judge: Codex** (canonical sanitized invocation; payload = this issue fetched live). Verdict verbatim:

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

APPROVED requires TOTAL >= 20 and no dimension below 4. Maximum 3 rounds.

**Judge: Codex** (canonical sanitized invocation; payload = this issue fetched live). Verdict verbatim:

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
```

**Producer revision** addressing all five round-1 issues — verify in the committed PLAN.md:

1. Notice-language rule made explicit ("Answer invariant" section): UI-generated text follows `session.lang` as the customer's declared language; no language detection in the UI (rationale given); E2E-tested (switch to EN → English notices). One-line rebuttal per protocol: the UI cannot know the "latest message language" without a detection heuristic, which would be a parser-shaped guess — the header switch is the customer's declaration toward the UI, while model replies keep per-turn mirroring.
2. Vanished-tenant path specified: 409 → UI re-fetches /config (fresh GET /pizzerias) → selector re-rendered from the live list or "list unavailable"; TestClient + E2E scenario 2b added.
3. Speech behaviour section added: TTS language from session.lang, synthesis off by default and final-message-only, spoken-answer policy activated via a `spoken: true` flag on /chat with a unit test, push-to-talk/failure semantics, manual checklist retained.
4. Web-surface coverage for carried-over error rows: 401/403, 422, submit 5xx/timeout-unknown, empty-basket submit each asserted as rendered outcomes (golden transcripts / TestClient stream assertions / E2E), stated in "Error handling".
5. Confirm path made symmetric: every dispatch (success or failure) is appended to session.messages as synthetic tool_calls + tool results and logged identically; one model call phrases success or refusal; nothing submitted on failed confirm ("Confirm control" section).

Re-review requested against the same rubric (round 2 of max 3).


codex
I’m reviewing `PLAN.md` against `SPEC.md`, the retrofit conditions, and the current implementation it claims to reuse. I’ll read the required artifacts first, then trace carry-over claims into `core/`, `channels/`, and `tests/` for gaps, contradictions, and exploitable ambiguity.
exec
/bin/bash -lc "sed -n '1,260p' reviews/round10-grill-verdict.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,220p' /home/rob/.agents/skills/using-superpowers/SKILL.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,320p' PLAN.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,360p' SPEC.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' decisions/qa.md" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 695ms:
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

 succeeded in 736ms:
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

 succeeded in 755ms:
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

 succeeded in 781ms:
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
- `GET /health` → `{api: "ok"|"down", gateway: "ok"|"down"|"unknown"}` —
  `api` from a live `GET /pizzerias` with 3s timeout; `gateway` from the
  outcome of the most recent model call (unknown before the first).
  Polled by the UI every 30s for the footer connection state.
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
     lock + order id visible; basket totals correct at each step;
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

1. **Prices & totals in core.** Menu price, `Item.unit_price`,
   snapshot totals (Decimal), get_menu result, prompt rule.
   ☐ totals only in core ☐ rounding tested ☐ v1 suite still green.
2. **Session factory & tenancy.** Session v2 fields, `create_session`,
   client per session, agent uses `session.client`, startup preselection
   check kept. ☐ unknown id → typed error ☐ tenant immutable ☐ tests.
3. **Language authority.** `Session.lang`, `set_language` re-render,
   apologies/STT via session.lang. ☐ switch test ☐ no process-global lang.
4. **Confirm path.** `Agent.confirm_and_submit` + synthetic messages.
   ☐ stale revision streams error, nothing submitted ☐ happy path test

 succeeded in 805ms:
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
I’ve loaded the spec, retrofit conditions, and the prior grill verdict. Next I’m checking the existing implementation the plan says it reuses, so I can separate valid carry-over from silent drift.
exec
/bin/bash -lc 'pytest --collect-only -q' in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '321,520p' PLAN.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '321,520p' SPEC.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc 'rg --files core channels tests' in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' channels/web.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' core/agent.py" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 1815ms:
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

 succeeded in 1799ms:
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

 succeeded in 1815ms:
tests/__init__.py
tests/test_tools.py
tests/test_state.py
tests/test_transcripts.py
tests/fixtures/menu.json
tests/fixtures/order_created.json
tests/fixtures/location.json
tests/fixtures/error_422.json
tests/fixtures/pizzerias.json
tests/fixtures/orders_list.json
channels/cli.py
channels/static/index.html
channels/static/style.css
channels/static/app.js
channels/web.py
channels/__init__.py
tests/transcripts/correction.json
tests/transcripts/happy_path.json
core/pizzasim.py
core/menu.py
core/__init__.py
core/state.py
core/order.py
core/agent.py
core/tools.py
tests/transcripts/unknown_item.json
tests/transcripts/mind_change.json
tests/transcripts/submit_timeout.json

 succeeded in 1756ms:
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

 succeeded in 1653ms:
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

 exited 2 in 2625ms:
tests/test_state.py::test_full_happy_path
tests/test_state.py::test_customer_before_items_is_legal_and_stays_empty
tests/test_state.py::test_submitted_is_terminal[<lambda>0]
tests/test_state.py::test_submitted_is_terminal[<lambda>1]
tests/test_state.py::test_submitted_is_terminal[<lambda>2]
tests/test_state.py::test_submitted_is_terminal[<lambda>3]
tests/test_state.py::test_submitted_is_terminal[<lambda>4]
tests/test_state.py::test_submitted_is_terminal[<lambda>5]
tests/test_state.py::test_remove_from_empty
tests/test_state.py::test_read_back_empty
tests/test_state.py::test_read_back_collecting_needs_customer
tests/test_state.py::test_confirm_illegal_states[EMPTY]
tests/test_state.py::test_confirm_illegal_states[COLLECTING]
tests/test_state.py::test_confirm_when_already_confirmed
tests/test_state.py::test_submit_outside_confirmed[EMPTY]
tests/test_state.py::test_submit_outside_confirmed[COLLECTING]
tests/test_state.py::test_submit_outside_confirmed[READY]
tests/test_state.py::test_remove_unknown_line
tests/test_state.py::test_add_after_confirmed_demotes_to_ready
tests/test_state.py::test_remove_after_confirmed_demotes
tests/test_state.py::test_set_customer_after_confirmed_demotes
tests/test_state.py::test_confirmation_does_not_survive_demotion
tests/test_state.py::test_confirm_without_read_back
tests/test_state.py::test_confirm_with_stale_revision
tests/test_state.py::test_read_back_of_old_revision_does_not_allow_confirm
tests/test_state.py::test_revision_increments_on_every_mutation
tests/test_state.py::test_merge_same_line
tests/test_state.py::test_same_code_different_extras_is_separate_line
tests/test_state.py::test_partial_remove
tests/test_state.py::test_remove_to_empty_and_readd
tests/test_state.py::test_type_and_code_key_removal
tests/test_state.py::test_remove_without_qty_clears_all_variants
tests/test_state.py::test_remove_with_qty_reduces_most_recent_variant
tests/test_state.py::test_submit_attempt_timestamp_set_once

==================================== ERRORS ====================================
_____________________ ERROR collecting tests/test_tools.py _____________________
ImportError while importing test module '/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/usr/lib/python3.13/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/test_tools.py:9: in <module>
    import httpx
E   ModuleNotFoundError: No module named 'httpx'
__________________ ERROR collecting tests/test_transcripts.py __________________
ImportError while importing test module '/home/rob/bpm-pizza-vibecoding-solution/tests/test_transcripts.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/usr/lib/python3.13/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/test_transcripts.py:10: in <module>
    from core.agent import Agent, AgentConfig, Session
core/agent.py:11: in <module>
    import httpx
E   ModuleNotFoundError: No module named 'httpx'
=========================== short test summary info ============================
ERROR tests/test_tools.py
ERROR tests/test_transcripts.py
!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!
34 tests collected, 2 errors in 0.18s

codex
The current code confirms the plan’s basic premise: the existing web layer is nowhere near the v3 contract, while the core still assumes a single process-wide tenant and language. I’m reading the current tests and UI now to see whether the plan’s “carry over unchanged” claims overstate what can actually be reused.
exec
/bin/bash -lc "sed -n '1,280p' core/tools.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "nl -ba SPEC.md | sed -n '120,320p'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "nl -ba PLAN.md | sed -n '1,260p'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,320p' channels/static/app.js" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,320p' tests/test_tools.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,320p' tests/test_transcripts.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,280p' core/pizzasim.py" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 1350ms:
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

 succeeded in 1375ms:
   120	  - `web` — FastAPI server on port 8888, browser chat UI, streaming the
   121	    agent's intermediate steps as newline-delimited JSON so tool calls and
   122	    tool results are visible, not just the final answer.
   123	- **Speech on the web transport**, served by a self-hosted CPU-only speech
   124	  container over HTTP. See *Speech*.
   125	- **Several pizzerias.** The customer chooses which one they are ordering
   126	  from, and can change it. `PIZZERIA_ID` is the preselection, not a
   127	  restriction.
   128	- **Languages:** German and English. The agent answers in the language the
   129	  customer used, per turn, without being told to switch.
   130	- **Menu, prices, cart, customer, submit.** The full happy path plus
   131	  correction ("no, make that three"), removal, and abandonment. The customer
   132	  can ask what is on offer and what items cost, and sees what the basket
   133	  comes to before confirming.
   134	- **Deterministic tests** that run with no network and no LLM, plus one live
   135	  acceptance test and a browser end-to-end test.
   136	- **Structured logging** of every turn: user text, model tool calls, tool
   137	  results, state transitions. One line per event, JSON, to a file.
   138	
   139	### Out (explicitly)
   140	
   141	- Payment and anything financial beyond showing prices the API supplies.
   142	- Delivery routing, or an ETA of our own invention.
   143	- Accounts, auth, sessions surviving a process restart.
   144	- Modifying or cancelling an order after it was submitted.
   145	- Any regex or keyword parser that produces an order without the model.
   146	  See **Anti-patterns**; this is a hard ban, not a style preference.
   147	- Reading the whole menu aloud when the answer will be spoken.
   148	- Persisting customer data anywhere beyond the process and the PizzaSim API.
   149	
   150	---
   151	
   152	## Environment and configuration
   153	
   154	All configuration comes from environment variables. Load `~/.env` if present;
   155	never write to it, never create it, never print a value.
   156	
   157	| Variable | Purpose |
   158	|---|---|
   159	| `LITELLM_PIZZA_URL` | OpenAI-compatible gateway base URL (`/chat/completions` appended) |
   160	| `LITELLM_PIZZA_KEY` | Bearer token for the gateway |
   161	| `LITELLM_PIZZA_MODEL_1` | Model the ordering agent calls; required, no default in code |
   162	| `LITELLM_PIZZA_MODEL_2` | Second configured model, where the build uses one |
   163	| `PIZZASIM_URL` | PizzaSim API base URL; dashboard and docs links derive from it |
   164	| `PIZZASIM_API_KEY` | Sent as header `X-API-Key` on protected routes |
   165	| `PIZZERIA_ID` | UUID of the pizzeria preselected on first load |
   166	| `PIZZERIA_LANG` | Initial language, `de` or `en`: the greeting, the CLI, and the web UI before the customer switches |
   167	| `APP_VERSION` | Release version, `x.y.z`, shown in the footer |
   168	| `SPEECH_URL` | Base URL of the self-hosted speech service (optional) |
   169	| `SPEECH_STT_MODEL` | Transcription model id |
   170	| `SPEECH_TTS_MODEL` | Synthesis model id |
   171	| `SPEECH_TTS_VOICE` | Voice id |
   172	
   173	Rules:
   174	
   175	- **Nothing is hardcoded.** No UUID, no model name, no menu, no base URL, no
   176	  vendor — not even as a fallback "just in case".
   177	- Missing or empty required variable → exit before the first turn with a
   178	  message naming the variable and the file it was expected in. Never start
   179	  half-configured. `SPEECH_*` are the exception: absent means the speech
   180	  features are not rendered, and everything else works.
   181	- Secrets never appear in logs, transcripts, error messages or the web UI.
   182	
   183	---
   184	
   185	## The PizzaSim API (contract)
   186	
   187	Facts below are **verified** — against running code or a live response. A
   188	verified fact never moves back into the open list; the open list only shrinks.
   189	
   190	| Call | Auth | Notes |
   191	|---|---|---|
   192	| `GET /menu` | public | returns `pizzas[]` and `pasta[]`, each with `code` |
   193	| `GET /pizzerias` | `X-API-Key` | list of pizzerias with `id`, `name` |
   194	| `GET /pizzerias/{id}/orders` | `X-API-Key` | that pizzeria's orders; used by timeout recovery |
   195	| `POST /pizzerias/{id}/orders` | `X-API-Key` | places the order |
   196	| `GET /location?street=…` | public | street plausibility check (optional tool) |
   197	
   198	Order request body:
   199	
   200	```json
   201	{
   202	  "customer": { "first_name": "Marco", "street_one": "via di Cantieri" },
   203	  "items": [{ "type": "pizza", "code": "margherita", "qty": 2, "extras": [] }]
   204	}
   205	```
   206	
   207	Response carries `order_id`, `status`, `eta_seconds`.
   208	
   209	Derived URLs — built from `PIZZASIM_URL`, never hardcoded:
   210	
   211	- Dashboard of a pizzeria: `{PIZZASIM_URL}/dashboard/pizzerias/{id}`
   212	  (verified against the dashboard's routing code).
   213	- API documentation: `{PIZZASIM_URL}/swagger.html` — there is **no** `/docs`.
   214	
   215	Facts that shape behaviour:
   216	
   217	- The tenant is **always** in the URL path, never in a header. The API key is
   218	  a server key, not a pizzeria id.
   219	- Customers are unique per pizzeria **by first name**. An unknown name
   220	  silently creates a new customer — a misheard name creates a ghost. Speech
   221	  input must therefore confirm the name explicitly.
   222	- `street_one` is optional and **not** validated for deliverability. Asking
   223	  for it is a policy of this agent — never claim to have checked an address.
   224	- `POST /orders` is **not** idempotent. A retry after a timeout can double a
   225	  real order. See **Error handling**.
   226	
   227	Further verified facts (live responses, 2026-07-31/08-01):
   228	
   229	- **Menu item shape:** `{"code", "name", "base": [ingredients], "price"}`.
   230	  `price` is a number in euros — the source for every price answer and the
   231	  basket total; no other financial data exists in the API. `name` is a
   232	  single string (identical in DE and EN; there are no per-language names).
   233	  The menu response also carries a top-level `toppings[]` array.
   234	- **`extras[]` is a controlled vocabulary:** the `toppings[]` from
   235	  `GET /menu`. The server rejects unknown extras with `422`
   236	  (`"items[0].extras contains invalid topping 'unicorn_dust'"`); the tool
   237	  layer validates extras against `toppings[]` exactly like item codes.
   238	- **Error bodies are machine-readable:**
   239	  `{"error": "<code>", "details": ["<human sentence>", ...]}` (e.g.
   240	  `validation_failed` with HTTP 422) — mapped to typed errors; `details`
   241	  may feed targeted questions.
   242	- **Status values observed:** `ordered` → `prepared_planned` → `delivered`
   243	  (with `delivered_at` set on the last). A fresh order starts as `ordered`.
   244	- **`GET /location?street=` returns** `{"street": "<echo>",
   245	  "deliverable": <bool>}`, HTTP 200 — `deliverable: true` even for nonsense
   246	  input, so it is a weak plausibility signal at best: never tell the
   247	  customer an address was verified.
   248	- **The list endpoint carries no items.** The detail endpoint
   249	  `GET /pizzerias/{id}/orders/{order_id}` (auth: `X-API-Key`) returns the
   250	  full order incl. `customer` and `items[]`. Submit-timeout recovery
   251	  shortlists by `first_name` + `created_at` recency on the list, then
   252	  verifies the candidate's items via the detail endpoint before adopting
   253	  it; the live acceptance test asserts items and quantities through the
   254	  same detail endpoint.
   255	- **Item codes are unique per type, not globally** — `tonno` exists as a
   256	  pizza and a pasta. Validation and removal always key on `(type, code)`.
   257	
   258	### Open contract questions — shrink-only
   259	
   260	Resolve against the live API before the affected component is implemented,
   261	then move the answer up into the facts and delete the question. Never guess.
   262	A verified fact never returns here.
   263	
   264	*(empty — all previous questions were resolved against the live API and
   265	moved into the facts above)*
   266	
   267	---
   268	
   269	## Order state machine
   270	
   271	```
   272	EMPTY ──add_items──▶ COLLECTING ──set_customer──▶ READY
   273	  ▲                      │  ▲                       │
   274	  └──remove last item────┘  └───add/remove/edit─────┘
   275	                                                    │ read_back + customer says yes
   276	                                                    ▼
   277	                                               CONFIRMED ──submit_order──▶ SUBMITTED
   278	                                                    │
   279	                                                    └──any change──▶ back to READY
   280	```
   281	
   282	Invariants, all enforced in code and all covered by unit tests:
   283	
   284	1. `submit_order` outside `CONFIRMED` returns an error. It does not
   285	   "helpfully" confirm on the model's behalf.
   286	2. Any mutation after `CONFIRMED` drops the order back to `READY`. A
   287	   confirmation applies to the basket that was read back, not to a later one.
   288	3. `CONFIRMED` is reachable only via `confirm_order`, which is only legal
   289	   after `read_back` for the current basket revision. The basket carries a
   290	   revision counter; `confirm_order` must name it.
   291	4. `SUBMITTED` is terminal. The conversation may continue; the order may not.
   292	5. An item enters the basket only with a `code` present in the menu snapshot
   293	   fetched this session.
   294	6. A basket never crosses a tenant boundary. Changing pizzeria starts a fresh
   295	   conversation and a fresh order.
   296	
   297	---
   298	
   299	## Tools
   300	
   301	The model sees exactly these. Names, parameters and semantics are fixed.
   302	
   303	| Tool | Parameters | Returns |
   304	|---|---|---|
   305	| `get_menu` | — | pizzas and pasta with codes, display names, prices |
   306	| `add_items` | `items[]` of `{type, code, qty, extras[]}` | new basket + revision |
   307	| `remove_item` | `code`, `type`, optional `qty` | new basket + revision |
   308	| `set_customer` | `first_name`, optional `street_one` | customer as stored |
   309	| `read_back` | — | basket, customer, revision, and the code-computed basket total — the text the agent reads out |
   310	| `confirm_order` | `revision` | state `CONFIRMED`, or error if stale |
   311	| `submit_order` | — | `order_id`, `status`, `eta_seconds` |
   312	| `check_street` | `street` | plausibility result (optional) |
   313	
   314	Tool result conventions:
   315	
   316	- Success: the **full current state**, not a diff. The model never
   317	  reconstructs the basket from history.
   318	- Failure: `{"error": {"code": "...", "message": "...", "candidates": [...]}}`.
   319	  `message` is written so it can be spoken to the customer as-is.
   320	- `add_items` with an unknown code returns `unknown_item` plus up to three

 succeeded in 1347ms:
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

 succeeded in 1382ms:
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

 succeeded in 1464ms:
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
   130	  `Agent.confirm_and_submit(session, revision, emit)` with **symmetric
   131	  success/failure semantics** — one path, not two:
   132	  1. `tools.dispatch("confirm_order", {revision})`; on success also
   133	     `tools.dispatch("submit_order", {})` (full v1 semantics incl.
   134	     timeout recovery).
   135	  2. **Every** dispatch performed — successful or failed — is appended to
   136	     `session.messages` as a synthetic assistant `tool_calls` message +
   137	     `tool` result (OpenAI format) and emitted/logged as the usual
   138	     `tool_call`/`tool_result`/`state` events. The model's context and
   139	     the JSONL log are identical in shape to a model-initiated call.
   140	  3. One model call then phrases the outcome to the customer — the order
   141	     id in groups and minutes on success, or the refusal in plain words
   142	     on failure (stale revision → "the order changed, let me read it back
   143	     again"), exactly the SPEC's "the refusal is a tool result the model
   144	     must deal with in front of the customer". It streams like a normal
   145	     turn. The UI additionally refreshes the basket panel from the
   146	     streamed snapshot; nothing is submitted on a failed confirm.
   147	- The customer action is a click, not a word; `CONFIRMED` remains
   148	  reachable only via `confirm_order(revision)`; the transport forwards two
   149	  identifiers and owns zero logic.
   150	- CLI keeps the conversational path: customer says yes → model calls
   151	  `confirm_order` + `submit_order` itself. Both paths converge on dispatch.
   152	
   153	## Web channel v2 (condition 4 — a rewrite, named as such)
   154	
   155	Server (`channels/web.py`):
   156	
   157	- `GET /config` → `{version, speech, lang_default, pizzerias:
   158	  [{id, name}] | null, preselected_id, dashboard_base, docs_url}`.
   159	  `pizzerias: null` when `GET /pizzerias` failed at request time — the UI
   160	  then shows "list unavailable" and no selector (no fallback entry).
   161	- `POST /session {pizzeria_id?, lang?}` → creates a Session (defaults:
   162	  preselected id, `PIZZERIA_LANG`), returns `{session_id, pizzeria_id,
   163	  pizzeria_name, lang}`. Invalid/vanished id → 409 with the session-error
   164	  text; the UI then **re-fetches `/config`** (which performs a fresh
   165	  `GET /pizzerias`), re-renders the selector from that live list — or the
   166	  "list unavailable" state if the fetch fails — and shows the notice.
   167	  Covered by a TestClient test (409 + fresh list served) and an E2E
   168	  scenario (stub drops a pizzeria between load and selection).
   169	- `POST /chat {session_id, text|null}` → NDJSON stream (unchanged
   170	  protocol; `text: null` = greeting turn). 404 for unknown session (the
   171	  UI then creates a fresh one). Per-session lock → 409 on overlap.
   172	- `POST /confirm {session_id, revision}` → NDJSON stream (same event
   173	  shapes) via `confirm_and_submit`.
   174	- `POST /language {session_id, lang}` → `{lang}`; core `set_language`.
   175	- `GET /health` → `{api: "ok"|"down", gateway: "ok"|"down"|"unknown"}` —
   176	  `api` from a live `GET /pizzerias` with 3s timeout; `gateway` from the
   177	  outcome of the most recent model call (unknown before the first).
   178	  Polled by the UI every 30s for the footer connection state.
   179	- Speech proxy endpoints move to `channels/speech.py` (deliverable):
   180	  `SpeechService` class (config, probe, stt(audio, lang), tts(text,
   181	  lang)); web.py keeps only the thin route handlers.
   182	
   183	**Speech behaviour (full SPEC coverage, not just the STT hint):**
   184	
   185	- STT **and** TTS requests carry `session.lang` as the language; no
   186	  separate speech-language config (SPEC's language-authority rule).
   187	- Synthesis is **off by default**, toggled by the customer, applied only
   188	  to the **final** assistant message of a turn — never to intermediate
   189	  steps (v1 behaviour, kept and E2E-visible: the toggle exists only when
   190	  speech is enabled).
   191	- Spoken-answer policy: `POST /chat` gains optional `spoken: true`, set by
   192	  the UI when the input came from the microphone or the TTS toggle is on.
   193	  Core appends a one-line per-turn note instructing spoken style (≤3 menu
   194	  items + invitation, minutes not seconds, order id in groups) — the
   195	  policy itself lives in the system prompt; the flag only activates it.
   196	  Unit test: flag → note present; no flag → absent.
   197	- Push-to-talk with visible recording state; a failed STT/TTS call shows a
   198	  notice and never touches the order (v1, kept). Manual checklist in
   199	  README as SPEC requires.
   200	
   201	UI (`channels/static/` — rebuilt):
   202	
   203	- **Header:** pizzeria name (prominent, from the session), selector
   204	  (name + first 8 UUID chars, from `/config.pizzerias`), dashboard link
   205	  (`dashboard_base` + id, `target="_blank"`), language switch DE/EN,
   206	  Start over. Selector change and Start over both: abort any in-flight
   207	  stream (AbortController), clear the chat and basket views, create a NEW
   208	  session (fresh id — invariant 6 by construction), render the greeting
   209	  turn.
   210	- **Footer:** `version`, full selected UUID (selectable text), connection
   211	  badges from `/health`, docs link.
   212	- **Basket panel:** rendered from every `snapshot` in tool results /
   213	  `done` events: lines with qty × name, `line_total`, `basket_total`;
   214	  after `state == "SUBMITTED"`: locked, shows order id + "submitted", no
   215	  control on the page can modify or resubmit (confirm button removed,
   216	  input stays usable for a new conversation via Start over / new session).
   217	- **Read-back panel:** on a `read_back` tool result: visually distinct
   218	  block + confirm button bound to the streamed revision.
   219	- **Answer invariant** ("no message ends unanswered"):
   220	  - send → immediate "agent is working" indicator;
   221	  - tool events render as they stream (collapsible steps, visually
   222	    distinct) — never discarded (anti-pattern 6);
   223	  - `done` without a preceding `assistant` event in the turn → rendered
   224	    notice "the agent did not answer — resend?";
   225	  - fetch error / abort / non-2xx → rendered notice naming which
   226	    (error, timeout, connection lost) + a resend button that re-posts the
   227	    same text;
   228	  - all notices in plain words, in the **customer's language**, defined
   229	    as follows.
   230	- **Notice-language rule (explicit decision):** UI-generated text (chrome,
   231	  notices, resend prompts) follows `session.lang` — the language the
   232	  customer chose via the header switch, or the default before any choice.
   233	  The UI performs **no language detection** (a heuristic would be a
   234	  parser-shaped guess, and model replies already mirror per turn); the
   235	  switch is the customer's declaration of their language toward the UI.
   236	  Tested: switch to EN → subsequent notices render in English (E2E).
   237	
   238	## CLI v2
   239	
   240	Unchanged flow; read_back output now includes line totals and the basket
   241	total from the snapshot (printing what core computed, no arithmetic).
   242	
   243	## Error handling — new rows on top of v1's table
   244	
   245	| Situation | Mechanism |
   246	|---|---|
   247	| Runtime pizzeria selection invalid | `create_session` NotFoundError → 409 → UI notice; process stays up |
   248	| Pizzeria list fetch fails | `/config.pizzerias = null` → "list unavailable", no selector, no fallback entry |
   249	| Stream ends without final message | UI-side detection via `done`-without-`assistant` → notice + resend |
   250	| Gateway unreachable | existing retry-once → apology (now also an `assistant` event, v1 fix) + UI resend offer |
   251	| Speech service down | probe fails → controls not rendered; per-call failure → notice, order untouched |
   252	
   253	All other rows keep v1 mechanics — but v3 makes their **rendered outcome**
   254	part of the web contract, so each customer-visible row gets web-surface
   255	coverage, not only tool-level tests:
   256	
   257	- `401/403` ("can't reach the kitchen system"), `422` submit_failed with
   258	  the offending field, submit `5xx`/timeout (`submit_unknown` honest
   259	  message), empty-basket submit ("What can I get you?"): each is asserted
   260	  as a **rendered assistant message in the DOM or NDJSON stream** —

 succeeded in 1349ms:
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

 succeeded in 1402ms:
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


def test_submit_outside_confirmed_is_tool_error(menu, fake):
    """Invariant 1: no helpful auto-confirmation."""
    order = ready_order(menu, fake)
    result = tools.dispatch(order, menu, fake, "submit_order", {})
    assert result["error"]["code"] == "invalid_state"
    assert fake.submits == 0


def test_empty_basket_submit(menu, fake):
    result = tools.dispatch(Order(), menu, fake, "submit_order", {})
    assert result["error"]["code"] == "invalid_state"
    assert result["error"]["message"] == "What can I get you?"


def test_submit_timeout_then_recovery_via_list(menu, fake):
    order = confirmed_order(menu, fake)
    fake.submit_effect = lambda: (_ for _ in ()).throw(ApiTimeout("t"))
    result = tools.dispatch(order, menu, fake, "submit_order", {})
    assert result["error"]["code"] == "submit_unknown"
    assert order.state is State.CONFIRMED and order.submit_unknown

    # the order did land — recovery must adopt it, not re-POST
    fake.orders = [{"id": "recovered-1", "first_name": "Marco",
                    "created_at": int(time.time()),
                    "ready_at": int(time.time()) + 300,
                    "status": "ordered"}]
    fake.order_details["recovered-1"] = {
        "id": "recovered-1",
        "customer": {"first_name": "Marco"},
        "items": [{"type": "pizza", "code": "margherita", "qty": 2,
                   "extras": []}],
    }
    result = tools.dispatch(order, menu, fake, "submit_order", {})
    assert result["order_id"] == "recovered-1"
    assert order.state is State.SUBMITTED
    assert fake.submits == 1  # never re-POSTed


def test_recovery_rejects_candidate_with_different_items(menu, fake):
    """A same-name recent order with other items is someone else's order —
    verified via the detail endpoint, then one real retry."""
    order = confirmed_order(menu, fake)
    fake.submit_effect = lambda: (_ for _ in ()).throw(ApiTimeout("t"))
    tools.dispatch(order, menu, fake, "submit_order", {})
    fake.orders = [{"id": "other-1", "first_name": "Marco",
                    "created_at": int(time.time()),
                    "ready_at": int(time.time()) + 300,
                    "status": "ordered"}]
    fake.order_details["other-1"] = {
        "id": "other-1", "customer": {"first_name": "Marco"},
        "items": [{"type": "pasta", "code": "pesto", "qty": 1,
                   "extras": []}],
    }
    fake.submit_effect = lambda: fixture("order_created.json")
    result = tools.dispatch(order, menu, fake, "submit_order", {})
    assert result["order_id"] == fixture("order_created.json")["order_id"]
    assert fake.submits == 2  # retried after verifying the mismatch


codex
I’ve isolated a few areas where the plan still leaves room for non-compliant implementation, mainly around the new confirm stream and the required web-contract coverage. I’m checking the tail of the plan for whether those gaps are closed by the testing/ticket sections or only implied.
exec
/bin/bash -lc "nl -ba PLAN.md | sed -n '257,340p'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "nl -ba channels/web.py | sed -n '1,260p'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "nl -ba core/agent.py | sed -n '1,240p'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "nl -ba channels/static/app.js | sed -n '1,260p'" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 242ms:
   257	- `401/403` ("can't reach the kitchen system"), `422` submit_failed with
   258	  the offending field, submit `5xx`/timeout (`submit_unknown` honest
   259	  message), empty-basket submit ("What can I get you?"): each is asserted
   260	  as a **rendered assistant message in the DOM or NDJSON stream** —
   261	  tool-level errors reach the customer as model-phrased plain language
   262	  (the model receives the speakable `message`), transport-level failures
   263	  as UI notices. Coverage: golden transcripts (submit timeout), TestClient
   264	  stream assertions (401/422/empty basket via stub PizzaSim), E2E
   265	  (tool error + gateway down + cut stream).
   266	
   267	## Testing
   268	
   269	- **Unit/tool (extend v1's 71):** prices copied at add time; `line_total`
   270	  / `basket_total` incl. Decimal rounding; snapshot shape; session factory
   271	  (valid id, unknown id, list failure); `set_language` re-render;
   272	  `confirm_and_submit` (happy, stale revision, submit timeout path);
   273	  `APP_VERSION` validation.
   274	- **Golden transcripts:** unchanged five; runner asserts extended snapshot
   275	  keys where relevant.
   276	- **Browser E2E (`tests/test_web_e2e.py`, offline, not optional):**
   277	  in-process **stub PizzaSim** (fixtures: two pizzerias, menu with prices)
   278	  and **stub gateway** (scripted tool-calling model) served locally;
   279	  the app under test started on an ephemeral port with env pointing at the
   280	  stubs; Playwright (chromium, headless) asserts against the DOM:
   281	  1. full order: greeting → price question (price from menu rendered) →
   282	     add items → name → read-back panel → **confirm click** → submitted
   283	     lock + order id visible; basket totals correct at each step;
   284	  2. pizzeria switch: selector → fresh conversation, header + footer UUID
   285	     change, basket cleared; language switch to EN → subsequent UI
   286	     notices render in English;
   287	  2b. vanished pizzeria: stub drops a pizzeria between page load and
   288	     selection → 409 → notice + selector re-rendered from the fresh list;
   289	  3. failure — tool error: unknown item → candidates visible in steps,
   290	     answer rendered;
   291	  4. failure — gateway unreachable: stub gateway refuses → apology text
   292	     rendered + resend control;
   293	  5. failure — stream ends without final message: stub cuts the stream →
   294	     UI notice + resend control.
   295	- **Live acceptance test:** as in v1, updated to SPEC wording (presence
   296	  via list, customer/items/qty via detail endpoint). Opt-in
   297	  `PIZZA_LIVE_TEST=1`.
   298	- **Speech:** manual checklist (README) unchanged + STT language follows
   299	  the session language.
   300	
   301	## Deliverables delta vs repo
   302	
   303	New: `channels/speech.py`, `tests/test_web_e2e.py`. Rebuilt:
   304	`channels/web.py`, `channels/static/*`. Extended: `core/menu.py`,
   305	`core/order.py`, `core/tools.py`, `core/agent.py`, prompts (prices,
   306	verbatim-price rule), `README.md`, `.env.example` (+`APP_VERSION`),
   307	`requirements.txt` (+playwright). Everything else stands as approved.
   308	
   309	## Tickets (each ≤ 1h, tests in the ticket that introduces the behaviour)
   310	
   311	1. **Prices & totals in core.** Menu price, `Item.unit_price`,
   312	   snapshot totals (Decimal), get_menu result, prompt rule.
   313	   ☐ totals only in core ☐ rounding tested ☐ v1 suite still green.
   314	2. **Session factory & tenancy.** Session v2 fields, `create_session`,
   315	   client per session, agent uses `session.client`, startup preselection
   316	   check kept. ☐ unknown id → typed error ☐ tenant immutable ☐ tests.
   317	3. **Language authority.** `Session.lang`, `set_language` re-render,
   318	   apologies/STT via session.lang. ☐ switch test ☐ no process-global lang.
   319	4. **Confirm path.** `Agent.confirm_and_submit` + synthetic messages.
   320	   ☐ stale revision streams error, nothing submitted ☐ happy path test
   321	   ☐ timeout-recovery reachable from this path.
   322	5. **Web API surface.** /config, /session, /confirm, /language, /health,
   323	   session 404/409 semantics, speech extraction to `channels/speech.py`.
   324	   ☐ httpx TestClient tests with stub PizzaSim ☐ no order logic in routes.
   325	6. **Web UI: frame.** Header (name, selector, dashboard link, language,
   326	   start over), footer (version, UUID, health badges, docs), i18n chrome.
   327	   ☐ switch/start-over create fresh session + abort in-flight stream.
   328	7. **Web UI: conversation contract.** Basket panel, read-back panel +
   329	   confirm button, working indicator, done-without-assistant notice,
   330	   error/resend paths, submitted lock.
   331	   ☐ every notice in session language ☐ no discarded stream events.
   332	8. **Browser E2E suite.** Stub PizzaSim + stub gateway + Playwright;
   333	   scenarios 1–5 above. ☐ fully offline ☐ DOM assertions only.
   334	9. **Harden + docs.** Error-table walk incl. new rows, README (all
   335	   channels + E2E + speech checklist), `.env.example`, `APP_VERSION`
   336	   start at `2.0.0`. ☐ full suite green ☐ live acceptance re-run.
   337	
   338	Review protocol: this plan goes to the reviewer (Issue gate) before any
   339	code; implementation follows only after APPROVED under the SPEC rubric.

 succeeded in 322ms:
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

 succeeded in 301ms:
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

 succeeded in 318ms:
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

codex
Findings:

- [PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:129) introduces a new `confirm_and_submit` path, but it never explicitly says that the post-dispatch model call reuses the same retry/apology semantics as normal turns, and the planned tests only cover happy/stale/timeout at unit level plus gateway-down on `/chat`, not on `/confirm` ([PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:269), [PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:291)). That leaves an exploitable hole where confirm succeeds or fails in core, then the follow-up phrasing call dies and violates the web-channel “every message gets an answer” contract.
- The required header/footer contract is described, but the verification plan does not actually assert several mandatory elements: dashboard link, docs link, `APP_VERSION`, and connection badges are listed in the UI tickets, yet none of the E2E scenarios names them as assertions ([PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:203), [PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:210), [PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:276)). Given how far the current web surface is from spec ([channels/web.py](/home/rob/bpm-pizza-vibecoding-solution/channels/web.py:78), [channels/static/app.js](/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js:45)), this needs explicit test commitments, not implied coverage.
- `/health` is still underspecified for implementation and review: “gateway from the most recent model call” is too loose for a binding contract because it does not define scope, transitions, or whether `/confirm` updates it the same way `/chat` does ([PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:175)). Without explicit semantics and tests, an implementer can ship decorative badges that are stale, global in the wrong way, or never move off `unknown`.

SCORES (1-5 each, 5 = best):
completeness: 4
correctness: 4
error_handling: 3
simplicity: 4
spec_compliance: 3
TOTAL: 18/25
VERDICT: CHANGES_REQUIRED
ISSUES: (max 5 bullets, concrete and actionable, empty if approved)
- Specify that `Agent.confirm_and_submit` must reuse the normal gateway retry/apology path and add a test for gateway failure during the post-confirm phrasing call so `/confirm` still satisfies the “answer or rendered error” invariant.
- Expand the browser E2E plan to explicitly assert the full header/footer contract: dashboard link target, docs link target, `APP_VERSION`, full UUID display, and connection badges.
- Define `/health` semantics precisely: what updates `gateway`, whether it is process-wide or session-scoped, how `/chat` and `/confirm` affect it, and what transitions `unknown -> ok/down` are expected; add TestClient and UI assertions for those states.
tokens used
68,470
Findings:

- [PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:129) introduces a new `confirm_and_submit` path, but it never explicitly says that the post-dispatch model call reuses the same retry/apology semantics as normal turns, and the planned tests only cover happy/stale/timeout at unit level plus gateway-down on `/chat`, not on `/confirm` ([PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:269), [PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:291)). That leaves an exploitable hole where confirm succeeds or fails in core, then the follow-up phrasing call dies and violates the web-channel “every message gets an answer” contract.
- The required header/footer contract is described, but the verification plan does not actually assert several mandatory elements: dashboard link, docs link, `APP_VERSION`, and connection badges are listed in the UI tickets, yet none of the E2E scenarios names them as assertions ([PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:203), [PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:210), [PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:276)). Given how far the current web surface is from spec ([channels/web.py](/home/rob/bpm-pizza-vibecoding-solution/channels/web.py:78), [channels/static/app.js](/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js:45)), this needs explicit test commitments, not implied coverage.
- `/health` is still underspecified for implementation and review: “gateway from the most recent model call” is too loose for a binding contract because it does not define scope, transitions, or whether `/confirm` updates it the same way `/chat` does ([PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:175)). Without explicit semantics and tests, an implementer can ship decorative badges that are stale, global in the wrong way, or never move off `unknown`.

SCORES (1-5 each, 5 = best):
completeness: 4
correctness: 4
error_handling: 3
simplicity: 4
spec_compliance: 3
TOTAL: 18/25
VERDICT: CHANGES_REQUIRED
ISSUES: (max 5 bullets, concrete and actionable, empty if approved)
- Specify that `Agent.confirm_and_submit` must reuse the normal gateway retry/apology path and add a test for gateway failure during the post-confirm phrasing call so `/confirm` still satisfies the “answer or rendered error” invariant.
- Expand the browser E2E plan to explicitly assert the full header/footer contract: dashboard link target, docs link target, `APP_VERSION`, full UUID display, and connection badges.
- Define `/health` semantics precisely: what updates `gateway`, whether it is process-wide or session-scoped, how `/chat` and `/confirm` affect it, and what transitions `unknown -> ok/down` are expected; add TestClient and UI assertions for those states.
```

**Producer revision, round 3 — PLAN v2 amendments (authoritative here; a repo-side hook currently gates direct PLAN.md edits, so per the issue-communication protocol these three amendments are part of the plan under review and will be synced into PLAN.md once the gate question is settled by the operator):**

**Amendment 1 — confirm phrasing call reuses the normal gateway path (replaces nothing, extends "Confirm control"):** the post-dispatch model call in `Agent.confirm_and_submit` goes through the same gateway path as every turn — same timeout, same retry-once, same apology emitted as an `assistant` event on failure — so `/confirm` satisfies the answer-or-rendered-error invariant even when the gateway dies after the order was submitted (the order id is already in the streamed snapshot; the apology never claims the order failed). New unit test: gateway failure during post-confirm phrasing → dispatches applied, apology streamed as `assistant` event, state consistent.

**Amendment 2 — E2E asserts the full header/footer contract (extends E2E scenario 1):** the full-order scenario additionally asserts in the DOM: pizzeria name in the header; selector entries rendered as "name + short UUID"; dashboard link `href` ending `/dashboard/pizzerias/{selected id}` with `target="_blank"`; docs link `href` ending `/swagger.html`; footer showing `APP_VERSION` verbatim, the full selected UUID as selectable text, and the connection badges (gateway `unknown` before the first turn, `ok` after it; api `ok`).

**Amendment 3 — precise /health semantics (replaces the /health bullet):** `GET /health` → `{api, gateway}`. `api` is measured live per request (`GET /pizzerias`, 3s timeout; ok on 2xx, down otherwise). `gateway` is a process-wide last-known status: `unknown` until the first model call anywhere; every gateway call by any session through either `/chat` or `/confirm` (both share the single Agent gateway path) sets it — `ok` on success, `down` when a call exhausts retry and aborts the turn; the next success flips it back. `/health` itself never calls the gateway. UI polls every 30s. Tests: TestClient — fresh app `unknown`; scripted turn `ok`; stub gateway failure `down`; subsequent success `ok`; `api` flips with stub PizzaSim up/down. E2E asserts the badges render these states.

Re-review requested (round 3 of max 3): judge the committed PLAN.md **plus these three amendments** as one plan, against the same rubric.


codex
Using `using-superpowers` to set the review workflow, then I’ll verify the current plan, spec, retrofit conditions, and the round-3 amendments against the repo before issuing the final gate verdict.
exec
/bin/bash -lc "sed -n '1,220p' /home/rob/.agents/skills/using-superpowers/SKILL.md" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 101ms:
codex
I’ve loaded the governing skill. Next I’m checking the Codex-specific skill notes and then re-reading the plan artifacts so the round-3 verdict is tied to the actual workspace state, not the quoted history.
exec
/bin/bash -lc "sed -n '1,240p' /home/rob/.agents/skills/using-superpowers/references/codex-tools.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,420p' SPEC.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' decisions/qa.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,340p' PLAN.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' reviews/round10-grill-verdict.md" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 339ms:
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

 succeeded in 368ms:
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

 succeeded in 388ms:
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
- `GET /health` → `{api: "ok"|"down", gateway: "ok"|"down"|"unknown"}` —
  `api` from a live `GET /pizzerias` with 3s timeout; `gateway` from the
  outcome of the most recent model call (unknown before the first).
  Polled by the UI every 30s for the footer connection state.
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
     lock + order id visible; basket totals correct at each step;
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

1. **Prices & totals in core.** Menu price, `Item.unit_price`,
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

 succeeded in 335ms:
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

 succeeded in 407ms:
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

codex
SCORES (1-5 each, 5 = best):
completeness: 5
correctness: 5
error_handling: 4
simplicity: 4
spec_compliance: 5
TOTAL: 23/25
VERDICT: APPROVED
ISSUES:
tokens used
68,047
SCORES (1-5 each, 5 = best):
completeness: 5
correctness: 5
error_handling: 4
simplicity: 4
spec_compliance: 5
TOTAL: 23/25
VERDICT: APPROVED
ISSUES:
