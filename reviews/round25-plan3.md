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
session id: 019fc110-e06d-7b01-9157-57b2bd536ab8
--------
user
## Context

SPEC.md now contains two post-v1.0.0 extensions, both Codex-discussed and committed: returning-customer street reuse (confirm-without-disclosure, commit 7b5376b) and voice as a required release capability (commit d851966). The operator ordered implementation via the established pipeline. PLAN.md gained a "Delta Plan v3" section (commit d51bb93) covering both. This issue is the plan gate; SPEC stage order is binding: no implementation before APPROVED.

## Judge request

You are the devil's advocate and judge for the PLAN stage. In the workspace (committed tree), read: the "Delta Plan v3" section at the end of PLAN.md (the artifact under review; Plan v2 above it is already approved and implemented), SPEC.md (source of truth — especially the contract facts on the customers endpoint, the Tools table rows for lookup_customer/set_customer/read_back, the saved-street redaction convention, the Speech + Speech service provisioning sections, the Testing additions, and acceptance point 5), decisions/qa.md (street-lookup and voice decisions), and the existing core/, channels/, tests/ the delta builds on.

Attack the delta plan: spec coverage gaps (redaction guarantees end to end incl. submit body vs snapshot/logs, mutual exclusivity, deleted customers, non-fatal lookup failure, secure-context requirement, offline wiring vs live proof split, single final-message TTS, name-confirmation regression), contradictions with the approved v2 implementation it extends, and any underspecification an implementer could exploit.

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
Reviewing the plan gate against the committed tree first. I’m loading the required skill instructions, then I’ll read the referenced spec, decisions, and relevant implementation surfaces before scoring the delta plan.
exec
```

**Producer revision** addressing all four round-1 issues — verify in the committed PLAN.md (commit 7c5b0c7), Delta Plan v3 section:

1. Live voice proof is now a real browser-driven HTTPS acceptance test: headless Chromium with `--use-file-for-fake-audio-capture` streams the spoken-order fixtures through real microphone capture, real STT, chat + confirm control, and asserts non-empty real TTS audio for the final message with the toggle ON; the four acceptance points are then verified via the list+detail API. Explicitly "not a text replay: if STT does not produce an order-driving transcript from the fixture, the test fails".
2. The fallback clause is removed: the real UI push-to-talk path in the offline browser E2E is mandatory; API-level speech tests "supplement it and never substitute for it". The offline E2E also gained the fake-audio-file flag so recording is deterministic.
3. The redaction sweep is end to end: the fixture street text must appear in exactly one place — the outbound submit payload (client spy) — and in no snapshot, emitted event, JSONL log line, and no entry of session.messages (model-visible tool-message serialization string-scanned). Ticket 1 checkbox updated accordingly.
4. Name confirmation is three scripted cases: wrong-name correction; spoken happy path with dictated street; spoken happy path with saved street (name confirmed in addition to the saved-address yes/no question, which is explicitly not a substitute). Prompts in both languages state that spoken conversations always confirm the first name before submission.

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

**Producer revision, round 3** — all three round-2 issues addressed in commit 3ba2eaa, Delta Plan v3 section; verify in the file:

1. Runtime degradation designed and tested: a failing speech call after startup hides mic + TTS toggle for the session with a plain notice; typed ordering continues; E2E flips StubSpeech into failure mode mid-session and proves controls disappear while a typed order still completes. Startup-down behaviour keeps its existing test.
2. Secure-context gating is now an implementation + test requirement: controls render only when window.isSecureContext is true (in addition to cfg.speech and the media APIs); an E2E init script forces isSecureContext=false and asserts no speech controls render even with speech fully configured, while text ordering works.
3. Ticket 7 skip contract aligned: gated on PIZZA_LIVE_VOICE=1 + PIZZA_LIVE_VOICE_URL, skips cleanly when either is unset. Ticket 4 checkboxes extended with the two new E2E scenarios.

Re-review requested (round 3 of max 3) against the same rubric.

**Judge: Codex — round 3 verdict verbatim:**

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

```

**Gate result per SPEC protocol:** maximum 3 rounds reached without APPROVED — the stage stops here and the open state goes to the operator. The three round-3 findings were editorial (transcript fixtures named in the redaction sweep; tickets 5 and 7 aligned with their own prose) and have been applied in commit 61c8d9b so the artifact is complete; the formal verdict of this gate remains CHANGES_REQUIRED 18/25. Operator decision requested: accept the plan and proceed to implementation, or order a fresh gate round.

**Operator decision:** a fresh gate round was ordered (the previous stage stopped at 3 rounds per protocol; the round-3 editorial findings were applied in commit 61c8d9b).

**Fresh gate round requested.** Verify in the committed PLAN.md, Delta Plan v3 section: (1) the redaction sweep now explicitly covers golden transcript fixtures and any transcript-derived serialization in addition to snapshots, events, JSONL logs and session.messages, with the saved street allowed in exactly one place — the outbound submit payload; (2) Ticket 5 lists all three name-confirmation cases as execution contract; (3) Ticket 7 checkboxes now require the real HTTPS browser path, failure when STT yields no order-driving transcript, and non-empty playable final-message TTS audio. All earlier round-1/2 fixes remain in place. Same rubric, same rules.


codex
Reviewing the fresh gate request against the committed tree. I’m loading the required skill instructions first, then I’ll read the delta plan, spec, decisions, and the implementation surfaces it extends before issuing a verdict.
exec
/bin/bash -lc "sed -n '1,260p' /home/rob/.agents/skills/receiving-code-review/SKILL.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,220p' /home/rob/.agents/skills/using-superpowers/SKILL.md" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 139ms:
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

 succeeded in 142ms:
---
name: receiving-code-review
description: Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear or technically questionable - requires technical rigor and verification, not performative agreement or blind implementation
---

# Code Review Reception

## Overview

Code review requires technical evaluation, not emotional performance.

**Core principle:** Verify before implementing. Ask before assuming. Technical correctness over social comfort.

## The Response Pattern

```
WHEN receiving code review feedback:

1. READ: Complete feedback without reacting
2. UNDERSTAND: Restate requirement in own words (or ask)
3. VERIFY: Check against codebase reality
4. EVALUATE: Technically sound for THIS codebase?
5. RESPOND: Technical acknowledgment or reasoned pushback
6. IMPLEMENT: One item at a time, test each
```

## Forbidden Responses

**NEVER:**
- "You're absolutely right!" (explicit instruction-file violation)
- "Great point!" / "Excellent feedback!" (performative)
- "Let me implement that now" (before verification)

**INSTEAD:**
- Restate the technical requirement
- Ask clarifying questions
- Push back with technical reasoning if wrong
- Just start working (actions > words)

## Handling Unclear Feedback

```
IF any item is unclear:
  STOP - do not implement anything yet
  ASK for clarification on unclear items

WHY: Items may be related. Partial understanding = wrong implementation.
```

**Example:**
```
your human partner: "Fix 1-6"
You understand 1,2,3,6. Unclear on 4,5.

❌ WRONG: Implement 1,2,3,6 now, ask about 4,5 later
✅ RIGHT: "I understand items 1,2,3,6. Need clarification on 4 and 5 before proceeding."
```

## Source-Specific Handling

### From your human partner
- **Trusted** - implement after understanding
- **Still ask** if scope unclear
- **No performative agreement**
- **Skip to action** or technical acknowledgment

### From External Reviewers
```
BEFORE implementing:
  1. Check: Technically correct for THIS codebase?
  2. Check: Breaks existing functionality?
  3. Check: Reason for current implementation?
  4. Check: Works on all platforms/versions?
  5. Check: Does reviewer understand full context?

IF suggestion seems wrong:
  Push back with technical reasoning

IF can't easily verify:
  Say so: "I can't verify this without [X]. Should I [investigate/ask/proceed]?"

IF conflicts with your human partner's prior decisions:
  Stop and discuss with your human partner first
```

**your human partner's rule:** "External feedback - be skeptical, but check carefully"

## YAGNI Check for "Professional" Features

```
IF reviewer suggests "implementing properly":
  grep codebase for actual usage

  IF unused: "This endpoint isn't called. Remove it (YAGNI)?"
  IF used: Then implement properly
```

**your human partner's rule:** "You and reviewer both report to me. If we don't need this feature, don't add it."

## Implementation Order

```
FOR multi-item feedback:
  1. Clarify anything unclear FIRST
  2. Then implement in this order:
     - Blocking issues (breaks, security)
     - Simple fixes (typos, imports)
     - Complex fixes (refactoring, logic)
  3. Test each fix individually
  4. Verify no regressions
```

## When To Push Back

Push back when:
- Suggestion breaks existing functionality
- Reviewer lacks full context
- Violates YAGNI (unused feature)
- Technically incorrect for this stack
- Legacy/compatibility reasons exist
- Conflicts with your human partner's architectural decisions

**How to push back:**
- Use technical reasoning, not defensiveness
- Ask specific questions
- Reference working tests/code
- Involve your human partner if architectural

**If you're uncomfortable pushing back out loud:** Name that tension, then tell your partner about the issue you've seen. They'll appreciate your honesty.

## Acknowledging Correct Feedback

When feedback IS correct:
```
✅ "Fixed. [Brief description of what changed]"
✅ "Good catch - [specific issue]. Fixed in [location]."
✅ [Just fix it and show in the code]

❌ "You're absolutely right!"
❌ "Great point!"
❌ "Thanks for catching that!"
❌ "Thanks for [anything]"
❌ ANY gratitude expression
```

**Why no thanks:** Actions speak. Just fix it. The code itself shows you heard the feedback.

**If you catch yourself about to write "Thanks":** DELETE IT. State the fix instead.

## Gracefully Correcting Your Pushback

If you pushed back and were wrong:
```
✅ "You were right - I checked [X] and it does [Y]. Implementing now."
✅ "Verified this and you're correct. My initial understanding was wrong because [reason]. Fixing."

❌ Long apology
❌ Defending why you pushed back
❌ Over-explaining
```

State the correction factually and move on.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Performative agreement | State requirement or just act |
| Blind implementation | Verify against codebase first |
| Batch without testing | One at a time, test each |
| Assuming reviewer is right | Check if breaks things |
| Avoiding pushback | Technical correctness > comfort |
| Partial implementation | Clarify all items first |
| Can't verify, proceed anyway | State limitation, ask for direction |

## Real Examples

**Performative Agreement (Bad):**
```
Reviewer: "Remove legacy code"
❌ "You're absolutely right! Let me remove that..."
```

**Technical Verification (Good):**
```
Reviewer: "Remove legacy code"
✅ "Checking... build target is 10.15+, this API needs 13+. Need legacy for backward compat. Current impl has wrong bundle ID - fix it or drop pre-13 support?"
```

**YAGNI (Good):**
```
Reviewer: "Implement proper metrics tracking with database, date filters, CSV export"
✅ "Grepped codebase - nothing calls this endpoint. Remove it (YAGNI)? Or is there usage I'm missing?"
```

**Unclear Item (Good):**
```
your human partner: "Fix items 1-6"
You understand 1,2,3,6. Unclear on 4,5.
✅ "Understand 1,2,3,6. Need clarification on 4 and 5 before implementing."
```

## GitHub Thread Replies

When replying to inline review comments on GitHub, reply in the comment thread (`gh api repos/{owner}/{repo}/pulls/{pr}/comments/{id}/replies`), not as a top-level PR comment.

codex
Using `using-superpowers` to set the process, plus `receiving-code-review` as the closest fit for adversarial technical verification of a revised artifact. Next I’m reading the Codex-specific skill notes and the committed files under review.
exec
/bin/bash -lc "sed -n '1,220p' /home/rob/.agents/skills/references/codex-tools.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc 'rg --files core channels tests' in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc 'rg -n "Delta Plan v3|customers endpoint|lookup_customer|set_customer|read_back|saved-street|Speech|Speech service provisioning|Testing|acceptance point 5" PLAN.md SPEC.md decisions/qa.md' in /home/rob/bpm-pizza-vibecoding-solution
 exited 2 in 244ms:
sed: can't read /home/rob/.agents/skills/references/codex-tools.md: No such file or directory

 succeeded in 433ms:
decisions/qa.md:47:`lookup_customer(first_name)` returns booleans only; `set_customer` gains
decisions/qa.md:51:be echoed). read_back does not recite reused streets. Reuse limited to
decisions/qa.md:70:multi-second delays are a defect; new "Speech service provisioning"
PLAN.md:106:- `read_back` carries the snapshot and therefore the canonical total; the
PLAN.md:120:  unit_price, line_total}], basket_total, customer, read_back_done}`
PLAN.md:126:- `read_back` results stream to the UI (they already do); the UI renders a
PLAN.md:196:- Speech proxy endpoints move to `channels/speech.py` (deliverable):
PLAN.md:197:  `SpeechService` class (config, probe, stt(audio, lang), tts(text,
PLAN.md:200:**Speech behaviour (full SPEC coverage, not just the STT hint):**
PLAN.md:234:- **Read-back panel:** on a `read_back` tool result: visually distinct
PLAN.md:257:Unchanged flow; read_back output now includes line totals and the basket
PLAN.md:268:| Speech service down | probe fails → controls not rendered; per-call failure → notice, order untouched |
PLAN.md:284:## Testing
PLAN.md:322:- **Speech:** manual checklist (README) unchanged + STT language follows
PLAN.md:373:# Delta Plan v3 — Street lookup + Voice (SPEC rev d851966)
PLAN.md:380:## A. Street lookup (SPEC: lookup_customer / use_saved_street / redaction)
PLAN.md:398:  - New tool `lookup_customer` `{first_name}` →
PLAN.md:403:  - `set_customer` params become `{first_name, street_one?,
PLAN.md:410:- Prompts (both languages): after the name, call `lookup_customer`; if a
PLAN.md:412:  reciting the address; yes → `set_customer(use_saved_street: true)`;
PLAN.md:432:  question → flag-based set_customer → order) and decline/fallback
PLAN.md:450:- `tests/stubs.py`: `StubSpeech` — `GET /v1/models` 200;
PLAN.md:457:- API level (app booted with `SPEECH_*` pointing at StubSpeech):
PLAN.md:471:  and only for the final assistant message (StubSpeech call counter);
PLAN.md:477:  notice; typed ordering continues untouched. E2E test: StubSpeech is
PLAN.md:490:     customer corrects, `set_customer` is called exactly once with the
PLAN.md:520:   real street ☐ no saved-street text in events, logs or
PLAN.md:524:3. StubSpeech + audio fixtures + API-level speech tests. ☐ stt round
SPEC.md:126:- **Speech on the web transport is a required channel capability in
SPEC.md:128:  described in *Speech*; if the service is unavailable at runtime,
SPEC.md:233:  silently creates a new customer — a misheard name creates a ghost. Speech
SPEC.md:270:- **The customers endpoint** `GET /pizzerias/{id}/customers` (auth:
SPEC.md:292:EMPTY ──add_items──▶ COLLECTING ──set_customer──▶ READY
SPEC.md:295:                                                    │ read_back + customer says yes
SPEC.md:309:   after `read_back` for the current basket revision. The basket carries a
SPEC.md:328:| `lookup_customer` | `first_name` | `{customer_exists, saved_street_available}` — booleans only, **no street text** |
SPEC.md:329:| `set_customer` | `first_name`, plus either `street_one` **or** `use_saved_street: true` (mutually exclusive) — with the flag, the **code** copies the saved street into the order; the text never passes through the model | customer as stored (saved street as a flag, not text) |
SPEC.md:330:| `read_back` | — | basket, customer name, revision, and the code-computed basket total — the text the agent reads out. A street reused from saved data is **not** recited; the earlier yes/no reuse confirmation covers it |
SPEC.md:347:  web basket shows the same code-owned total that `read_back` carries.
SPEC.md:383:- Collect the first name; then call `lookup_customer`. If a saved street
SPEC.md:386:  `set_customer(use_saved_street: true)`. If the customer declines, is
SPEC.md:390:- Before submitting: call `read_back`, present it, and wait for an explicit
SPEC.md:478:## Speech
SPEC.md:480:Speech is an input and an output method on the web channel, served by a
SPEC.md:496:- **The browser speech APIs are forbidden.** `SpeechRecognition` and
SPEC.md:512:- **Speech is a required product capability for release completeness.**
SPEC.md:528:- **Speech shortens answers, it does not change them.** Same core, same
SPEC.md:535:### Speech service provisioning
SPEC.md:565:| Speech service down | hide speech controls | text UI unaffected |
SPEC.md:601:## Testing
SPEC.md:610:- **Address reuse:** tool-level tests for `lookup_customer`
SPEC.md:612:  `set_customer(use_saved_street: true)` copying in code; redaction tests
SPEC.md:646:- **Speech, manual** (supplementary): dictate an order, a name that needs
SPEC.md:757:5. **Speech.** Wire the speech service into the web UI, spoken-answer policy,
SPEC.md:818:| Speech | Self-hosted container, OpenAI-compatible HTTP; no vendor, no browser speech API |

 succeeded in 471ms:
tests/test_web_e2e.py
tests/__init__.py
tests/stubs.py
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
channels/speech.py
channels/__init__.py
channels/web.py
channels/cli.py
channels/static/index.html
channels/static/style.css
channels/static/app.js
core/tools.py
core/order.py
core/agent.py
core/pizzasim.py
core/menu.py
core/__init__.py
core/state.py

codex
The core references are located. I also hit a bad path in the skill reference, so I’m resolving that and then reading the exact sections in `PLAN.md`, `SPEC.md`, `decisions/qa.md`, plus the current tool/state/web test surfaces for contradictions.
exec
/bin/bash -lc "sed -n '373,560p' PLAN.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "find /home/rob/.agents/skills -path '*codex-tools.md' -print" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '478,670p' SPEC.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '260,410p' SPEC.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,220p' decisions/qa.md" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 455ms:
# Delta Plan v3 — Street lookup + Voice (SPEC rev d851966)

> Stage-1 artifact for the two SPEC extensions committed after v1.0.0:
> returning-customer street reuse (confirm-without-disclosure) and voice as
> a required release capability. Design only — no code before the gate
> approves. Everything in Plan v2 above stands; this section only adds.

## A. Street lookup (SPEC: lookup_customer / use_saved_street / redaction)

Core:

- `core/pizzasim.py`: `list_customers()` → `GET /pizzerias/{id}/customers`
  → `customers[]`. Customers with `deleted_at != null` are treated as
  nonexistent everywhere.
- `core/order.py`: `Customer` gains `street_from_saved: bool = False`.
  Two serializations, one redaction rule:
  - `as_dict()` (used by SNAPSHOT, hence by every tool result, streamed
    event, transcript and log line): when `street_from_saved`, it carries
    `{"first_name", "street_one": null, "street_on_file": true}` — the
    saved text never appears. A street the customer dictated themselves is
    echoed as before (`street_on_file` absent/false).
  - `as_submit_dict()` (used only to build the POST /orders body): always
    the real `street_one`. Submit uses saved `street_one` only — never
    `street_two` (SPEC guardrail).
- `core/tools.py`:
  - New tool `lookup_customer` `{first_name}` →
    `{"customer_exists": bool, "saved_street_available": bool, "snapshot"}`
    — booleans only, no street text, no customer id. API failure → the
    uniform error shape with code `api_unavailable` (non-fatal; the model
    falls back to asking for the street).
  - `set_customer` params become `{first_name, street_one?,
    use_saved_street?}` — mutually exclusive; both set → error code
    `invalid_arguments` with a speakable message. With the flag, dispatch
    fetches the customer record in code, copies `street_one`, sets
    `street_from_saved`; unknown name or no saved street → error
    `no_saved_street` (speakable), basket untouched.
  - `_submit` switches from `as_dict()` to `as_submit_dict()`.
- Prompts (both languages): after the name, call `lookup_customer`; if a
  saved street exists ask exactly one confirmation question without
  reciting the address; yes → `set_customer(use_saved_street: true)`;
  no/unknown/error → ask for the street as before. Never state a street
  that came from saved data.
- Web UI: basket + read-back panel render `street_on_file` as the
  localized label "gespeicherte Adresse"/"saved address", never text.

Tests (ticket introduces them):

- lookup known / unknown / deleted / API-error (error non-fatal).
- `use_saved_street` copies in code; the redaction sweep is end to end:
  after the full flow, the fixture street text must appear in exactly one
  place — the outbound submit payload (captured via a client spy) — and in
  no snapshot, no emitted event, no JSONL log line, and **no entry of
  `session.messages`** (the model-visible tool-message serialization is
  string-scanned too; an implementation that leaks the street into tool
  content the model reads must fail this test). The same sweep covers
  transcript artifacts: golden transcript fixtures and any
  transcript-derived serialization must not contain saved street text.
- Mutual exclusion + `no_saved_street` paths.
- Two new golden transcripts: saved-address reuse (lookup → confirm
  question → flag-based set_customer → order) and decline/fallback
  (customer says no → street asked, dictated street echoed as before).

## B. Voice (SPEC: required capability; offline wiring tests + live proof)

Artifacts:

- `deploy/speech-service.compose.yml`: neutral, CPU-only service
  definition — image and models come from environment placeholders
  (`SPEECH_IMAGE`, `SPEECH_*`), no vendor or model names in the file, and
  a comment pointing at the OpenAI-compatible surface it must expose.
  README gains a "Voice deployment" section: HTTPS/domain requirement
  (secure context), co-deployment with the app, env wiring.
- `tests/fixtures/audio/`: generated spoken fixtures (offline synthesis
  on the build host if a synthesizer is available, otherwise minimal
  valid WAV containers) — `order.de.wav`, `order.en.wav`; used by the
  offline round-trip (content irrelevant to the stub) and by the live
  voice test (content = a spoken order).
- `tests/stubs.py`: `StubSpeech` — `GET /v1/models` 200;
  `POST /v1/audio/transcriptions` → fixed transcript (per stub script,
  e.g. "Zwei Margherita bitte"), records the language field it received;
  `POST /v1/audio/speech` → tiny valid audio bytes, counts calls.

Offline tests:

- API level (app booted with `SPEECH_*` pointing at StubSpeech):
  `/config.speech == true`; `/speech/stt` round trip with an audio
  fixture returns the stub transcript and passed `session.lang` as the
  language; `/speech/tts` returns audio bytes; both 404 when speech is
  unconfigured (existing behaviour, kept).
- Browser E2E (Playwright, localhost = secure context, fake media device
  flags `--use-fake-device-for-media-capture` +
  `--use-fake-ui-for-media-capture` +
  `--use-file-for-fake-audio-capture=<fixture wav>`, microphone
  permission granted): mic button and TTS toggle visible; push-to-talk
  click-start/click-stop records via real `MediaRecorder` (the fake
  device streams the audio fixture), uploads to the stub, transcript
  drives a turn (`spoken: true` asserted via the stub gateway seeing the
  spoken-style note); with the toggle ON, exactly one TTS fetch per turn
  and only for the final assistant message (StubSpeech call counter);
  toggle OFF by default. This real UI push-to-talk path is mandatory —
  API-level speech tests supplement it and never substitute for it.
- **Runtime degradation:** when a speech call fails after startup (STT or
  TTS returns an error / the proxy answers 502), the UI hides the mic and
  the TTS toggle for the rest of the session and shows a plain-language
  notice; typed ordering continues untouched. E2E test: StubSpeech is
  switched to failure mode mid-session → controls disappear, a typed
  order still completes. (Startup-down behaviour — probe fails → controls
  never rendered — exists since v1 and keeps its test.)
- **Secure-context gating in the UI, not just in the docs:** the speech
  controls render only when `window.isSecureContext` is true (HTTPS or
  localhost) in addition to `cfg.speech` and the media APIs. E2E test: an
  init script forces `isSecureContext = false` → with speech fully
  configured, neither mic nor TTS toggle is rendered and text ordering
  works — plain HTTP never presents a voice-capable UI.
- Name-confirmation regression, three scripted cases (the saved-address
  question is **not** a substitute for name confirmation):
  1. plausible-but-wrong spoken name: agent repeats the name back, the
     customer corrects, `set_customer` is called exactly once with the
     corrected name, only after the correction — no submit before that;
  2. spoken happy path, dictated street: the name is confirmed before
     submission;
  3. spoken happy path, saved street reused: the name is confirmed before
     submission *in addition to* the saved-address yes/no question.
  Prompts (both languages) state explicitly: in spoken conversations the
  first name is always confirmed before the order is submitted.

Live proof (opt-in, release-gating per SPEC):

- `PIZZA_LIVE_VOICE=1` + `PIZZA_LIVE_VOICE_URL=<https base url of the
  voice-capable deployment>`: a real headless browser drives the real
  page over HTTPS end to end — microphone capture via the fake media
  device streaming `order.de.wav` / `order.en.wav` (Chromium
  `--use-file-for-fake-audio-capture`), real STT through the deployed
  speech service, the transcript drives the chat, the confirm control
  places the order, and with the toggle ON the final assistant message
  fetches real TTS audio (response is non-empty browser-playable audio).
  The four acceptance points are then verified via the pizzeria's
  list+detail API endpoints. Not a text replay: if STT does not produce
  an order-driving transcript from the fixture, the test fails. Skipped
  cleanly when the env vars are unset; it cannot run on the current dev
  VPS (no speech service, no HTTPS) and is executed against the
  voice-capable deployment.

## C. Tickets (≤1h each)

1. Street-lookup core (client, Customer redaction split, tools, unit
   tests incl. redaction sweep). ☐ booleans-only lookup ☐ submit carries
   real street ☐ no saved-street text in events, logs or
   session.messages.
2. Street-lookup conversation (prompts DE/EN, two golden transcripts, UI
   label). ☐ confirm-without-disclosure flow ☐ decline fallback.
3. StubSpeech + audio fixtures + API-level speech tests. ☐ stt round
   trip with session lang ☐ tts bytes ☐ 404 when unconfigured.
4. Browser E2E voice wiring (fake media device). ☐ mic/toggle visible
   ☐ push-to-talk round trip ☐ single final-message TTS fetch
   ☐ mid-session speech failure degrades to text-only ☐ insecure
   context renders no speech controls.
5. Name-confirmation regression transcripts, all three cases.
   ☐ wrong-name correction: corrected name only, after confirmation
   ☐ spoken happy path, dictated street: name confirmed before submit
   ☐ spoken happy path, saved street: name confirmed in addition to the
   saved-address yes/no question.
6. deploy/ speech service definition + README voice section.
   ☐ neutral (no vendor/model names) ☐ HTTPS requirement documented.
7. Live voice acceptance test (opt-in) + docs. ☐ DE+EN fixtures
   ☐ gated on `PIZZA_LIVE_VOICE=1` + `PIZZA_LIVE_VOICE_URL` and skips
   cleanly when either is unset ☐ real HTTPS browser path (mic capture →
   STT → chat → confirm control) ☐ STT failing to produce an
   order-driving transcript fails the test ☐ final-message TTS returns
   non-empty playable audio ☐ full-order verification via API.

 succeeded in 467ms:
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
- **The customers endpoint** `GET /pizzerias/{id}/customers` (auth:
  `X-API-Key`) returns `customers[]` with `{id, first_name, street_one,
  street_two, created_at, deleted_at}`. Since customers are unique per
  pizzeria by `first_name`, a first name resolves to at most one saved
  address. Guardrail: the verified order-write contract proves only
  `street_one`, so address reuse is limited to `street_one` until
  `street_two` support on `POST /orders` is verified as well.

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
| `lookup_customer` | `first_name` | `{customer_exists, saved_street_available}` — booleans only, **no street text** |
| `set_customer` | `first_name`, plus either `street_one` **or** `use_saved_street: true` (mutually exclusive) — with the flag, the **code** copies the saved street into the order; the text never passes through the model | customer as stored (saved street as a flag, not text) |
| `read_back` | — | basket, customer name, revision, and the code-computed basket total — the text the agent reads out. A street reused from saved data is **not** recited; the earlier yes/no reuse confirmation covers it |
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
- **Saved-street redaction.** A street reused from saved customer data
  never appears in tool results, streamed intermediate steps, transcripts
  or the structured logs — only booleans and state flags (e.g.
  `street_on_file: true`) may appear there, and the web UI shows it as
  "saved address", never as text. A street the customer dictated in this
  conversation may be echoed as before — it is their own input. First
  names are the only lookup key, so anyone claiming a name must never be
  able to extract the address behind it.

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
- Collect the first name; then call `lookup_customer`. If a saved street
  exists, ask exactly one confirmation question ("Soll ich wieder an Ihre
  gespeicherte Adresse liefern?") **without reciting the address**; on yes,
  `set_customer(use_saved_street: true)`. If the customer declines, is
  unknown, or the lookup fails (non-fatal), ask for the street as usual.
  If the customer declines the street entirely, accept it — it is optional
  in the API.
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


 succeeded in 502ms:
/home/rob/.agents/skills/using-superpowers/references/codex-tools.md

 succeeded in 503ms:
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
- **Speech is a required product capability for release completeness.**
  Text-only is the degraded fallback when speech is unconfigured in
  dev/test or temporarily unavailable at runtime: microphone and speaker
  toggle are then not rendered and the text UI is fully usable, and a
  speech outage must never block typed ordering. But a production release
  without a working speech path is not done.
- **Voice-capable web deployments run in a secure browser context:**
  HTTPS on a real host/domain, or localhost during development. Plain
  HTTP is not a valid acceptance environment for microphone input
  (`getUserMedia` is unavailable there).
- **Transport formats:** the STT path accepts the browser-recorded audio
  format emitted by `MediaRecorder`; the TTS path returns audio playable
  by a standard browser audio element.
- **Latency:** each STT and each TTS request should complete quickly
  enough for turn-based conversation on demo hardware; sustained
  multi-second delays that make turn-taking awkward are a defect.
- **Speech shortens answers, it does not change them.** Same core, same
  tools, same state machine. When a reply will be spoken: at most three menu
  items plus an invitation, times in minutes, order id read in groups.
- **Confirm the name.** Transcription errors on names are the expensive
  failure: a misheard name silently creates a customer nobody will find
  again. Read the name back before submitting.

### Speech service provisioning

The deployment includes a self-hosted, CPU-only speech service reachable
at `SPEECH_URL`, exposing OpenAI-compatible
`POST /v1/audio/transcriptions` and `POST /v1/audio/speech`. The
application and the speech service are deployed together as first-party
artifacts. The repository includes a neutral deployment definition for
this service next to the app deployment artifacts (no vendor or model
names in source or spec — the operator configures them via the
environment, exactly like the chat model).

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
- **Golden transcripts:** scripted conversations against a stub model
  replaying fixed tool calls — happy path, correction, unknown item, customer
  changes mind after read-back, submit timeout, saved-address reuse, and a
  decline/fallback variant. Assert final state and the calls actually made.
- **Address reuse:** tool-level tests for `lookup_customer`
  (known/unknown/API error — the error is non-fatal) and for
  `set_customer(use_saved_street: true)` copying in code; redaction tests
  asserting no saved street text appears in tool results, streamed events,
  transcripts or logs.
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
- **Offline speech E2E** with a stub speech service: exercise the real
  browser UI path — speech-control visibility when speech is configured,
  STT round-trip from recorded fixtures, `spoken: true` turn metadata,
  and TTS fetched only for the final assistant message when the toggle is
  enabled. These tests assert wiring, not transcription or synthesis
  quality.
- **Live voice acceptance test** (opt-in, like the live acceptance test):
  send recorded spoken-order fixtures through the real speech service,
  drive a full order through the web/API path, and verify the same
  order-correctness criteria as *What done looks like* via the API. At
  least one German and one English fixture. This is the release-gating
  voice proof — a manual demo is a release-note aid, not the acceptance
  artifact.
- **Name-confirmation regression:** a transcript/fixture with a
  plausible-but-wrong first name asserts that the agent reads back and
  confirms the name before submission, preventing ghost-customer
  creation.
- **Speech, manual** (supplementary): dictate an order, a name that needs
  correcting, a menu question — plus one run with `SPEECH_URL` unset,
  which must render a usable text-only UI and place an order normally.

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

 succeeded in 498ms:
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

## 2026-08-01 — Street lookup for returning customers (SPEC change only)

**Q:** Operator: saved streets must be look-up-able. Discussed proposed
spec changes with Codex (reviews/round20-street-spec-discussion.md).

**A (decision):** Confirm-without-disclosure + code-side copy. New tool
`lookup_customer(first_name)` returns booleans only; `set_customer` gains
`use_saved_street: true` (mutually exclusive with `street_one`) and the
code copies the saved street — the text never reaches the model, stream,
transcript or logs (scoped: a street the customer dictated themselves may
be echoed). read_back does not recite reused streets. Reuse limited to
street_one until street_two on POST /orders is verified. SPEC.md updated
in 8 places per the Codex decision list; previous spec archived as
SPEC_20260801_3.md. No plan, no implementation yet (operator hold).

## 2026-08-01 — Spec Future: voice becomes first-class (SPEC change only)

**Q:** Operator: "a voice agent without voice is a bit stupid" — make voice
a DONE-relevant capability. Discussed with Codex
(reviews/round21-voice-spec-discussion.md).

**A (decision, 10 points applied):** Acceptance point 5 (spoken
conversation produces the same verified order); speech = required release
capability, text-only = degraded operation (release completeness vs.
runtime resilience separated — a speech outage never blocks typed
ordering); SPEECH_* required in production, optional in dev/test; secure
browser context (HTTPS/domain) mandatory for the voice path — plain HTTP
is not a valid acceptance environment; MediaRecorder-format in,
browser-playable audio out; latency = turn-taking fitness, sustained
multi-second delays are a defect; new "Speech service provisioning"
subsection (co-deployed, neutral definition under deploy/); testing:
offline speech E2E via stub service (wiring only), opt-in live voice
acceptance test with DE+EN audio fixtures as the release-gating proof
(manual demo is a release-note aid only), name-confirmation regression
against ghost customers; deliverables + locked-decision row added;
telephony stays deferred. No plan, no implementation (operator hold).

codex
I’ve got the spec and plan text. Now I’m checking the current v2 implementation surfaces to see whether the delta plan is consistent with the code it extends or leaves room for spec-violating shortcuts.
exec
/bin/bash -lc "sed -n '1,240p' core/order.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' core/state.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,320p' core/tools.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,320p' channels/static/app.js" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,340p' channels/web.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' tests/test_tools.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,320p' tests/test_web_e2e.py" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 726ms:
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

 succeeded in 903ms:
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
                unit_price=menu.price(raw.get("type", ""),
                                      raw.get("code", "")),
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

 succeeded in 1117ms:
"""Order data: items, customer, revision, submit bookkeeping. Pure data."""
from __future__ import annotations

from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal
from enum import Enum


def _cents(value: Decimal) -> float:
    return float(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


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
    # Copied from the session menu snapshot at add time; totals are
    # computed here in core only — the model never does arithmetic.
    unit_price: float = 0.0

    def line_key(self) -> tuple:
        return (self.type, self.code, tuple(sorted(self.extras)))

    def line_total(self) -> float:
        return _cents(Decimal(str(self.unit_price)) * self.qty)


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
                    "unit_price": i.unit_price,
                    "line_total": i.line_total(),
                }
                for i in self.items
            ],
            "basket_total": _cents(
                sum((Decimal(str(i.unit_price)) * i.qty
                     for i in self.items), Decimal("0"))
            ),
            "customer": self.customer.as_dict() if self.customer else None,
            "read_back_done": self.read_back_revision == self.revision,
        }

 succeeded in 1062ms:
/* Web UI over the NDJSON stream. The invariant this file serves: no sent
   message ends without a rendered assistant reply or a rendered error.
   Speech: browser captures/plays audio only (MediaRecorder + <audio>);
   recognition/synthesis happen server-side. No browser speech APIs. */
"use strict";

const $ = (id) => document.getElementById(id);
const chat = $("chat");

const I18N = {
  de: {
    working: "Der Agent arbeitet …",
    steps: "Zwischenschritte",
    notAnswered: "Der Agent hat nicht geantwortet.",
    errNetwork: "Verbindung fehlgeschlagen.",
    errTimeout: "Zeitüberschreitung.",
    errHttp: "Es gab einen technischen Fehler.",
    busy: "Es läuft gerade eine Antwort — einen Moment.",
    resend: "Erneut senden",
    listUnavailable: "Pizzeria-Liste nicht verfügbar",
    startOver: "Neu beginnen",
    basket: "Warenkorb",
    total: "Summe",
    extrasNote: "Extras sind nicht separat bepreist.",
    submitted: "Bestellung abgeschickt — Nummer:",
    confirm: "Bestellung bestätigen",
    placeholder: "Nachricht schreiben …",
    send: "Senden",
    ttsLabel: "Antworten vorlesen",
    sttFail: "Spracherkennung gerade nicht erreichbar — bitte tippen.",
    sttEmpty: "Ich habe nichts verstanden — bitte noch einmal.",
    ttsFail: "Vorlesen gerade nicht möglich.",
    micDenied: "Kein Mikrofonzugriff.",
    sessionGone: "Diese Pizzeria ist gerade nicht verfügbar.",
    sessionLost: "Die Sitzung ist verloren gegangen — neue Sitzung " +
      "gestartet.",
  },
  en: {
    working: "The agent is working …",
    steps: "Intermediate steps",
    notAnswered: "The agent did not answer.",
    errNetwork: "Connection failed.",
    errTimeout: "The request timed out.",
    errHttp: "A technical error occurred.",
    busy: "A reply is already in progress — one moment.",
    resend: "Resend",
    listUnavailable: "Pizzeria list unavailable",
    startOver: "Start over",
    basket: "Basket",
    total: "Total",
    extrasNote: "Extras are not separately priced.",
    submitted: "Order submitted — number:",
    confirm: "Confirm order",
    placeholder: "Type a message …",
    send: "Send",
    ttsLabel: "Read replies aloud",
    sttFail: "Speech recognition unavailable — please type.",
    sttEmpty: "I didn't catch that — please try again.",
    ttsFail: "Read-aloud is unavailable right now.",
    micDenied: "No microphone access.",
    sessionGone: "That pizzeria isn't available right now.",
    sessionLost: "The session was lost — a new one was started.",
  },
};

let cfg = null;
let session = null;          // {id, pizzeriaId, pizzeriaName}
let lang = "de";
let currentAbort = null;
let lastOrderId = null;
const t = (key) => I18N[lang][key];

/* ---------- chrome ------------------------------------------------------ */

function applyChrome() {
  document.documentElement.lang = lang;
  $("text").placeholder = t("placeholder");
  $("send").textContent = t("send");
  $("start-over").textContent = t("startOver");
  $("basket-title").textContent = t("basket");
  $("tts-label").textContent = t("ttsLabel");
  $("list-unavailable").textContent = t("listUnavailable");
  document.querySelectorAll("#lang-switch button").forEach((b) =>
    b.classList.toggle("active", b.dataset.lang === lang));
}

function addMsg(cls, text) {
  const div = document.createElement("div");
  div.className = "msg " + cls;
  div.textContent = text;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
  return div;
}

function notice(text, retry) {
  /* retry: a string re-sends it as a chat message; a function re-runs the
     failed action (e.g. a confirm with its revision). */
  const div = document.createElement("div");
  div.className = "notice";
  div.appendChild(document.createTextNode(text));
  if (retry !== undefined) {
    const btn = document.createElement("button");
    btn.textContent = t("resend");
    btn.onclick = () => {
      div.remove();
      if (typeof retry === "function") retry(); else sendTurn(retry);
    };
    div.appendChild(btn);
  }
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

/* ---------- basket ------------------------------------------------------ */

function euro(n) {
  return n.toFixed(2).replace(".", lang === "de" ? "," : ".") + " €";
}

function renderBasket(snapshot) {
  const lines = $("basket-lines");
  lines.textContent = "";
  let hasExtras = false;
  for (const item of snapshot.items) {
    const li = document.createElement("li");
    const label = document.createElement("span");
    label.textContent = `${item.qty}× ${item.name}` +
      (item.extras.length ? ` (+${item.extras.join(", ")})` : "");
    if (item.extras.length) hasExtras = true;
    const price = document.createElement("span");
    price.textContent = euro(item.line_total);
    li.append(label, price);
    lines.appendChild(li);
  }
  $("basket-extras-note").hidden = !hasExtras;
  $("basket-extras-note").textContent = t("extrasNote");
  $("basket-total").textContent = "";
  const totalLabel = document.createElement("span");
  totalLabel.textContent = t("total");
  const totalValue = document.createElement("span");
  totalValue.textContent = euro(snapshot.basket_total);
  $("basket-total").append(totalLabel, totalValue);

  const submitted = snapshot.state === "SUBMITTED";
  $("basket").classList.toggle("locked", submitted);
  $("submitted-banner").hidden = !submitted;
  if (submitted) {
    $("submitted-banner").textContent =
      `${t("submitted")} ${lastOrderId || "—"}`;
    disableConfirm();
  }
}

/* ---------- read-back + confirm ---------------------------------------- */

function disableConfirm() {
  document.querySelectorAll(".readback button").forEach((b) => {
    b.disabled = true;
  });
}

function showReadback(snapshot) {
  disableConfirm();
  const panel = document.createElement("div");
  panel.className = "readback";
  const list = snapshot.items
    .map((i) => `${i.qty}× ${i.name} — ${euro(i.line_total)}`)
    .join("\n");
  const who = snapshot.customer
    ? `${snapshot.customer.first_name}` +
      (snapshot.customer.street_one
        ? `, ${snapshot.customer.street_one}` : "")
    : "";
  panel.textContent =
    `${who}\n${list}\n${t("total")}: ${euro(snapshot.basket_total)}`;
  const btn = document.createElement("button");
  btn.textContent = t("confirm");
  btn.onclick = () => { btn.disabled = true; confirmOrder(snapshot.revision); };
  panel.appendChild(btn);
  chat.appendChild(panel);
  chat.scrollTop = chat.scrollHeight;
}

/* ---------- streaming --------------------------------------------------- */

async function readStream(response, retry) {
  const steps = document.createElement("details");
  steps.className = "steps";
  steps.innerHTML = `<summary>${t("steps")}</summary>`;
  chat.appendChild(steps);

  let assistantAnswered = false;
  let finalText = "";
  const reader = response.body.getReader();
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
          + (ev.tool || "") + " " + JSON.stringify(ev.args ?? ev.result);
        steps.appendChild(pre);
        if (ev.type === "tool_result" && !ev.result.error) {
          if (ev.result.order_id) lastOrderId = ev.result.order_id;
          if (ev.result.snapshot) {
            renderBasket(ev.result.snapshot);
            if (ev.tool === "read_back") showReadback(ev.result.snapshot);
          }
        }
      } else if (ev.type === "assistant") {
        if (ev.text && ev.text.trim()) {
          assistantAnswered = true;
          finalText = ev.text;
          addMsg("assistant", ev.text);
        }
      } else if (ev.type === "done") {
        renderBasket(ev.state);
      }
    }
  }
  if (!steps.querySelector("pre")) steps.remove();
  if (!assistantAnswered) notice(t("notAnswered"), retry);
  return finalText;
}

const STREAM_TIMEOUT_MS = 120000;

async function streamPost(path, body, retry) {
  currentAbort = new AbortController();
  // Real client-side timeout: covers the request AND the streamed body,
  // so the timeout notice + resend control can actually occur.
  const signal = AbortSignal.any(
    [currentAbort.signal, AbortSignal.timeout(STREAM_TIMEOUT_MS)]);
  const working = document.createElement("div");
  working.className = "working";
  working.textContent = t("working");
  chat.appendChild(working);
  $("send").disabled = true;
  let finalText = "";
  try {
    const res = await fetch(path, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
      signal,
    });
    if (res.status === 404) {
      // The server no longer knows this session: recreate transparently.
      // A chat message stays recoverable via resend; a pending confirm is
      // NOT re-offered — the new session holds a new, empty order, so its
      // revision would be meaningless.
      working.remove();
      await startSession(session.pizzeriaId);
      notice(t("sessionLost"),
             typeof retry === "string" ? retry : undefined);
      $("send").disabled = false;
      return "";
    }
    if (res.status === 409) { working.remove(); notice(t("busy")); return ""; }
    if (!res.ok) throw new Error("http");
    working.remove();
    finalText = await readStream(res, retry);
  } catch (err) {
    working.remove();
    if (err.name === "AbortError") { /* deliberate: switch/start-over */ }
    else if (err.name === "TimeoutError") notice(t("errTimeout"), retry);
    else if (err.message === "http") notice(t("errHttp"), retry);
    else notice(t("errNetwork"), retry);
  }
  $("send").disabled = false;
  $("text").focus();
  return finalText;
}

async function sendTurn(text, spoken = false) {
  if (text !== null) addMsg("user", text);
  const finalText = await streamPost(
    "/chat", { session_id: session.id, text, spoken }, text ?? undefined);
  if (finalText && cfg.speech && $("tts-toggle").checked) speak(finalText);
}

async function confirmOrder(revision) {
  // The retry re-runs the confirm with the SAME revision: if the first
  // attempt actually went through, the state machine refuses it and the
  // agent says so — never a second order.
  const finalText = await streamPost(
    "/confirm", { session_id: session.id, revision },
    () => confirmOrder(revision));
  if (finalText && cfg.speech && $("tts-toggle").checked) speak(finalText);
}

/* ---------- sessions / tenancy ----------------------------------------- */

function fillSelector() {
  const select = $("pizzeria-select");
  if (!cfg.pizzerias) {
    select.hidden = true;
    $("list-unavailable").hidden = false;
    return;
  }
  select.hidden = false;
  $("list-unavailable").hidden = true;
  select.textContent = "";
  for (const p of cfg.pizzerias) {
    const opt = document.createElement("option");
    opt.value = p.id;
    opt.textContent = `${p.name} (${p.id.slice(0, 8)})`;
    select.appendChild(opt);
  }
  if (session) select.value = session.pizzeriaId;
}

 succeeded in 1015ms:
"""Web channel: API-surface tests plus the mandatory headless-browser
end-to-end tests asserting against the DOM. Fully offline: the app under
test talks to a stub PizzaSim and a stub (scripted) gateway on localhost.
The customer never talks to curl — and neither do these assertions."""
from __future__ import annotations

import json
import os

import httpx
import pytest

from tests.stubs import StubGateway, StubPizzaSim, run_server

PZ1 = "11111111-aaaa-bbbb-cccc-000000000001"
PZ2 = "22222222-aaaa-bbbb-cccc-000000000002"
PZ2_ENTRY = {"id": PZ2, "name": "Stub Pizzeria Due"}


@pytest.fixture(scope="module")
def stack():
    """Stub PizzaSim + stub gateway + the real app, all on localhost."""
    pizzasim = StubPizzaSim()
    gateway = StubGateway()
    ps_server, ps_url = run_server(pizzasim.app)
    gw_server, gw_url = run_server(gateway.app)
    os.environ.update({
        "PIZZASIM_URL": ps_url,
        "PIZZASIM_API_KEY": "stub-key",
        "PIZZERIA_ID": PZ1,
        "PIZZERIA_LANG": "de",
        "LITELLM_PIZZA_URL": gw_url,
        "LITELLM_PIZZA_KEY": "stub-key",
        "LITELLM_PIZZA_MODEL_1": "scripted-stub",
        "APP_VERSION": "2.0.0",
    })
    for var in ("SPEECH_URL", "SPEECH_STT_MODEL", "SPEECH_TTS_MODEL",
                "SPEECH_TTS_VOICE", "LITELLM_PIZZA_MODEL_2"):
        os.environ.pop(var, None)
    from channels import web  # app boots against the stub env
    app_server, app_url = run_server(web.app)
    yield {"pizzasim": pizzasim, "gateway": gateway, "url": app_url,
           "web": web, "ps_url": ps_url}
    for server in (app_server, ps_server, gw_server):
        server.should_exit = True


def stream_lines(client, path, body):
    with client.stream("POST", path, json=body) as response:
        response.raise_for_status()
        return [json.loads(line) for line in response.iter_lines()
                if line.strip()]


@pytest.fixture()
def api(stack):
    with httpx.Client(base_url=stack["url"], timeout=30.0) as client:
        yield client


# --- API surface (ordering matters: health-unknown runs first) ------------

def test_health_gateway_unknown_before_first_turn(api):
    health = api.get("/health").json()
    assert health == {"api": "ok", "gateway": "unknown"}


def test_config_contract(stack, api):
    cfg = api.get("/config").json()
    assert cfg["version"] == "2.0.0"
    assert cfg["speech"] is False
    assert cfg["lang_default"] == "de"
    assert [p["id"] for p in cfg["pizzerias"]] == [PZ1, PZ2]
    assert cfg["preselected_id"] == PZ1
    assert cfg["dashboard_base"] == f"{stack['ps_url']}/dashboard/pizzerias"
    assert cfg["docs_url"] == f"{stack['ps_url']}/swagger.html"


def test_config_list_unavailable_no_fallback(stack, api):
    stack["pizzasim"].fail_pizzerias = True
    try:
        cfg = api.get("/config").json()
        assert cfg["pizzerias"] is None  # never a bundled fallback list
        assert api.get("/health").json()["api"] == "down"
    finally:
        stack["pizzasim"].fail_pizzerias = False


def test_session_and_greeting_then_gateway_ok(api):
    created = api.post("/session", json={}).json()
    assert created["pizzeria_id"] == PZ1
    assert created["pizzeria_name"] == "Stub Pizzeria Uno"
    events = stream_lines(api, "/chat",
                          {"session_id": created["session_id"],
                           "text": None})
    kinds = [e["type"] for e in events]
    assert "assistant" in kinds and kinds[-1] == "done"
    assert api.get("/health").json()["gateway"] == "ok"


def test_session_unknown_pizzeria_409(api):
    response = api.post("/session", json={"pizzeria_id": "no-such-id"})
    assert response.status_code == 409


def test_chat_unknown_session_404(api):
    assert api.post("/chat", json={"session_id": "ghost",
                                   "text": "hi"}).status_code == 404


def test_turn_in_flight_409(stack, api):
    sid = api.post("/session", json={}).json()["session_id"]
    lock = stack["web"].app.state.locks[sid]
    assert lock.acquire(blocking=False)
    try:
        response = api.post("/chat", json={"session_id": sid, "text": "x"})
        assert response.status_code == 409
    finally:
        lock.release()


def test_language_switch(api):
    sid = api.post("/session", json={}).json()["session_id"]
    assert api.post("/language",
                    json={"session_id": sid,
                          "lang": "en"}).json() == {"lang": "en"}
    assert api.post("/language",
                    json={"session_id": sid,
                          "lang": "xx"}).status_code == 422


def test_tool_error_surfaces_as_rendered_answer(api):
    """The 422-shaped tool error reaches the customer as model-phrased
    plain language in the stream, never as a code."""
    sid = api.post("/session", json={}).json()["session_id"]
    stream_lines(api, "/chat", {"session_id": sid, "text": None})
    events = stream_lines(api, "/chat",
                          {"session_id": sid,
                           "text": "Einmal Bolognese bitte"})
    errors = [e for e in events if e["type"] == "tool_result"
              and "error" in e["result"]]
    assert errors and errors[0]["result"]["error"]["code"] == "unknown_item"
    final = [e for e in events if e["type"] == "assistant"][-1]
    assert "nicht im Angebot" in final["text"]
    assert "unknown_item" not in final["text"]


def test_confirm_endpoint_places_order_in_selected_tenant(stack, api):
    created = api.post("/session", json={"pizzeria_id": PZ2}).json()
    sid = created["session_id"]
    stream_lines(api, "/chat", {"session_id": sid, "text": None})
    stream_lines(api, "/chat", {"session_id": sid,
                                "text": "Zwei Margherita bitte"})
    events = stream_lines(api, "/chat", {"session_id": sid,
                                         "text": "Ich heiße Eva"})
    snapshot = [e["result"]["snapshot"] for e in events
                if e["type"] == "tool_result"
                and e.get("tool") == "read_back"][-1]
    events = stream_lines(api, "/confirm",
                          {"session_id": sid,
                           "revision": snapshot["revision"]})
    submitted = [e["result"] for e in events
                 if e["type"] == "tool_result"
                 and e.get("tool") == "submit_order"][-1]
    assert submitted["order_id"]
    # the order landed under the CHOSEN tenant, not the preselected one
    assert stack["pizzasim"].orders.get(PZ2), "order missing in tenant"
    assert not any(o["customer"]["first_name"] == "Eva"
                   for o in stack["pizzasim"].orders.get(PZ1, []))
    stored = stack["pizzasim"].orders[PZ2][-1]
    assert stored["customer"]["first_name"] == "Eva"
    assert stored["items"] == [{"type": "pizza", "code": "margherita",
                                "qty": 2, "extras": []}]


def test_confirm_stale_revision_streams_error(api):
    created = api.post("/session", json={}).json()
    sid = created["session_id"]
    stream_lines(api, "/chat", {"session_id": sid,
                                "text": "Zwei Margherita bitte"})
    events = stream_lines(api, "/confirm",
                          {"session_id": sid, "revision": 99})
    errors = [e["result"]["error"]["code"] for e in events
              if e["type"] == "tool_result" and "error" in e["result"]]
    assert errors  # refused by the state machine, streamed to the UI
    assert events[-1]["state"]["state"] != "SUBMITTED"


# --- browser end-to-end (Playwright, DOM assertions) ----------------------

@pytest.fixture(scope="module")
def page_factory(stack):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield lambda: browser.new_page()
        browser.close()


def open_app(page_factory, stack):
    page = page_factory()
    page.goto(stack["url"], timeout=30000)
    page.wait_for_selector(".msg.assistant", timeout=30000)
    return page


def test_e2e_full_order_with_header_footer_contract(page_factory, stack):
    stack["gateway"].mode = "ok"
    page = open_app(page_factory, stack)

    # header contract
    assert page.locator("#pizzeria-name").inner_text() == \
        "Stub Pizzeria Uno"
    first_option = page.locator("#pizzeria-select option").first
    assert "Stub Pizzeria Uno (11111111)" == first_option.inner_text()
    dash = page.locator("#dashboard-link")
    assert dash.get_attribute("href").endswith(
        f"/dashboard/pizzerias/{PZ1}")
    assert dash.get_attribute("target") == "_blank"
    # footer contract
    assert page.locator("#version").inner_text() == "v2.0.0"
    assert page.locator("#uuid").inner_text() == PZ1
    assert page.locator("#docs-link").get_attribute("href").endswith(
        "/swagger.html")
    page.wait_for_selector("#health-api.ok", timeout=15000)
    page.wait_for_selector("#health-gateway.ok", timeout=15000)
    # speech disabled → controls not rendered
    assert page.locator("#mic").is_hidden()
    assert page.locator("#tts-wrap").is_hidden()

    def say(text):
        page.fill("#text", text)
        page.click("#send")

    say("Was kostet eine Margherita?")
    page.wait_for_selector("text=8.5 €", timeout=30000)

    say("Zwei Margherita bitte")
    page.wait_for_selector("#basket-lines li", timeout=30000)
    assert "2× Margherita" in page.locator("#basket-lines").inner_text()
    assert "17,00 €" in page.locator("#basket-total").inner_text()

    say("Ich heiße Eva")
    page.wait_for_selector(".readback button:enabled", timeout=30000)
    readback = page.locator(".readback").last
    assert "17,00 €" in readback.inner_text()

    page.locator(".readback button:enabled").click()
    page.wait_for_selector("#submitted-banner:not([hidden])",
                           timeout=30000)
    banner = page.locator("#submitted-banner").inner_text()
    order_id = banner.split()[-1]
    assert len(order_id) == 36  # a real order id, visible to the customer
    assert page.locator("#basket.locked").count() == 1
    assert page.locator(".readback button").last.is_disabled()
    assert page.locator("details.steps").count() >= 3  # steps rendered
    page.close()


def test_e2e_pizzeria_switch_and_language(page_factory, stack):
    stack["gateway"].mode = "ok"
    page = open_app(page_factory, stack)
    page.fill("#text", "Zwei Margherita bitte")
    page.click("#send")
    page.wait_for_selector("#basket-lines li", timeout=30000)

    page.select_option("#pizzeria-select", PZ2)
    page.wait_for_function(
        "document.getElementById('pizzeria-name').textContent === "
        "'Stub Pizzeria Due'", timeout=30000)
    assert page.locator("#uuid").inner_text() == PZ2
    assert page.locator("#basket-lines li").count() == 0  # basket cleared
    page.wait_for_selector(".msg.assistant", timeout=30000)  # fresh greet

    page.locator("#lang-switch button[data-lang=en]").click()
    page.wait_for_function(
        "document.getElementById('start-over').textContent === "
        "'Start over'", timeout=15000)  # chrome follows the declared lang
    page.close()


def test_e2e_vanished_pizzeria_refreshes_selector(page_factory, stack):
    stack["gateway"].mode = "ok"
    page = open_app(page_factory, stack)
    page.fill("#text", "Zwei Margherita bitte")
    page.click("#send")
    page.wait_for_selector("#basket-lines li", timeout=30000)
    stack["pizzasim"].pizzerias = [p for p in stack["pizzasim"].pizzerias
                                   if p["id"] != PZ2]
    try:
        page.select_option("#pizzeria-select", PZ2)
        page.wait_for_selector(".notice", timeout=30000)
        page.wait_for_function(
            "document.querySelectorAll('#pizzeria-select option')"
            ".length === 1", timeout=15000)
        # the failed switch must NOT hide the still-live order
        assert page.locator("#basket-lines li").count() == 1
        assert page.locator(".msg.user").count() == 1
    finally:
        stack["pizzasim"].pizzerias.append(PZ2_ENTRY)
    page.close()


def test_e2e_lost_session_recreates_and_offers_resend(page_factory,
                                                      stack):
    """Server no longer knows the session (e.g. restart): the customer
    sees a plain notice, gets a fresh session, and can resend."""
    stack["gateway"].mode = "ok"
    page = open_app(page_factory, stack)
    stack["web"].app.state.sessions.clear()  # simulate a lost session
    page.fill("#text", "Was kostet eine Margherita?")
    page.click("#send")
    page.wait_for_selector(".notice button", timeout=30000)  # resend
    page.locator(".notice button").last.click()
    page.wait_for_selector("text=8.5 €", timeout=30000)
    page.close()


def test_e2e_tool_error_leaves_visible_message(page_factory, stack):
    stack["gateway"].mode = "ok"

 succeeded in 1094ms:
"""FastAPI web channel on port 8888. Same core, zero order logic here —
routes forward identifiers to core and stream its events.

Contract (PLAN v2): /config, /session, /chat, /confirm, /language,
/health, speech proxies, static UI. Turns are serialized per session;
tenants are immutable per session; the pizzeria selector list comes from
the live API and from nowhere else.

Run:  python -m channels.web
"""
from __future__ import annotations

import json
import queue
import re
import sys
import threading

from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse, Response, StreamingResponse
from fastapi.staticfiles import StaticFiles

from channels.speech import SpeechService, SpeechUnavailable
from core.agent import (
    Agent,
    AgentConfig,
    Session,
    create_session,
    set_language,
    startup,
)
from core.pizzasim import (
    ConfigError,
    NotFoundError,
    PizzaSimError,
    require_env,
)

STATIC = Path(__file__).resolve().parent / "static"
app = FastAPI(title="PizzaSim ordering agent")

SESSION_ERROR = {
    "de": "Diese Pizzeria ist gerade nicht verfügbar.",
    "en": "That pizzeria isn't available right now.",
}


@app.on_event("startup")
def boot() -> None:
    try:
        config = AgentConfig.from_env()
        version = require_env("APP_VERSION")
        if not re.fullmatch(r"\d+\.\d+\.\d+", version):
            raise ConfigError("APP_VERSION must look like x.y.z")
        base, _pizzeria_name, _menu = startup(config)
    except (ConfigError, ValueError) as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        raise SystemExit(1)
    except PizzaSimError as exc:
        print(f"Startup check against PizzaSim failed: {exc}\n"
              "We're not taking orders right now.", file=sys.stderr)
        raise SystemExit(1)
    app.state.config = config
    app.state.version = version
    app.state.base = base  # tenant-free surface + preselection default
    app.state.gateway_status = "unknown"  # process-wide, set by any call
    app.state.agent = Agent(
        config,
        status_cb=lambda status: setattr(app.state, "gateway_status",
                                         status),
    )
    app.state.sessions: dict[str, Session] = {}
    app.state.locks: dict[str, threading.Lock] = {}
    app.state.speech = SpeechService()


@app.get("/")
def index():
    return FileResponse(STATIC / "index.html")


@app.get("/config")
def ui_config():
    """UI bootstrap. The pizzeria list comes from the live API on every
    call; on failure it is null and the UI must not offer a selector."""
    try:
        pizzerias = [{"id": p["id"], "name": p["name"]}
                     for p in app.state.base.list_pizzerias()]
    except PizzaSimError:
        pizzerias = None
    return {
        "version": app.state.version,
        "speech": app.state.speech.enabled,
        "lang_default": app.state.config.lang,
        "pizzerias": pizzerias,
        "preselected_id": app.state.base.pizzeria_id,
        "dashboard_base": f"{app.state.base.base_url}/dashboard/pizzerias",
        "docs_url": f"{app.state.base.base_url}/swagger.html",
    }


@app.get("/health")
def health():
    """api: measured live per request. gateway: process-wide last-known
    status from real calls; /health itself never calls the gateway."""
    try:
        app.state.base.list_pizzerias()
        api = "ok"
    except PizzaSimError:
        api = "down"
    return {"api": api, "gateway": app.state.gateway_status}


@app.post("/session")
def new_session(body: dict):
    pizzeria_id = body.get("pizzeria_id") or None
    lang = body.get("lang") or None
    try:
        session = create_session(app.state.config, app.state.base,
                                 pizzeria_id, lang)
    except NotFoundError:
        lang = lang if lang in SESSION_ERROR else app.state.config.lang
        raise HTTPException(409, SESSION_ERROR[lang])
    except PizzaSimError:
        raise HTTPException(503, "We're not taking orders right now.")
    app.state.sessions[session.id] = session
    app.state.locks[session.id] = threading.Lock()
    return {"session_id": session.id, "pizzeria_id": session.pizzeria_id,
            "pizzeria_name": session.pizzeria_name, "lang": session.lang}


def _session(session_id: str) -> Session:
    session = app.state.sessions.get(session_id or "")
    if session is None:
        raise HTTPException(404, "unknown session")
    return session


def _stream(session: Session, work) -> StreamingResponse:
    """Serialize turns per session and stream core events as NDJSON."""
    lock = app.state.locks[session.id]
    if not lock.acquire(blocking=False):
        raise HTTPException(409, "a turn is already in progress")

    events: queue.Queue = queue.Queue()

    def run() -> None:
        try:
            work(events.put)
        finally:
            events.put({"type": "done", "state": session.order.snapshot()})
            events.put(None)
            lock.release()

    threading.Thread(target=run, daemon=True).start()

    def ndjson():
        while (event := events.get()) is not None:
            yield json.dumps(event, ensure_ascii=False) + "\n"

    return StreamingResponse(ndjson(), media_type="application/x-ndjson")


@app.post("/chat")
async def chat(body: dict):
    session = _session(str(body.get("session_id") or ""))
    text = body.get("text")  # None → opening turn, the agent greets
    if text is not None and not str(text).strip():
        raise HTTPException(422, "text must not be empty")
    spoken = bool(body.get("spoken"))
    return _stream(
        session,
        lambda emit: app.state.agent.run_turn(session, text, emit,
                                              spoken=spoken),
    )


@app.post("/confirm")
async def confirm(body: dict):
    """The explicit confirm control: the transport forwards two
    identifiers; core owns the rest."""
    session = _session(str(body.get("session_id") or ""))
    revision = body.get("revision")
    if isinstance(revision, bool) or not isinstance(revision, int):
        raise HTTPException(422, "revision must be an integer")
    return _stream(
        session,
        lambda emit: app.state.agent.confirm_and_submit(session, revision,
                                                        emit),
    )


@app.post("/language")
async def language(body: dict):
    session = _session(str(body.get("session_id") or ""))
    lang = str(body.get("lang") or "")
    if lang not in ("de", "en"):
        raise HTTPException(422, "lang must be de or en")
    set_language(session, lang)
    return {"lang": session.lang}


def _speech() -> SpeechService:
    if not app.state.speech.enabled:
        raise HTTPException(404, "speech is not available")
    return app.state.speech


@app.post("/speech/stt")
async def stt(audio: UploadFile, session_id: str = ""):
    speech = _speech()
    session = _session(session_id)
    try:
        text = speech.stt(await audio.read(),
                          audio.filename or "audio.webm",
                          audio.content_type or "audio/webm",
                          session.lang)
    except SpeechUnavailable:
        raise HTTPException(502, "speech service unavailable")
    return {"text": text}


@app.post("/speech/tts")
async def tts(body: dict):
    speech = _speech()
    session = _session(str(body.get("session_id") or ""))
    text = str(body.get("text") or "")
    if not text:
        raise HTTPException(422, "text required")
    try:
        audio, content_type = speech.tts(text, session.lang)
    except SpeechUnavailable:
        raise HTTPException(502, "speech service unavailable")
    return Response(audio, media_type=content_type)


app.mount("/static", StaticFiles(directory=STATIC), name="static")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8888)

 succeeded in 1131ms:
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


# --- prices and totals (canonical in core) --------------------------------

def test_menu_carries_prices(menu):
    result = menu.as_tool_result()
    margherita = next(p for p in result["pizzas"]
                      if p["code"] == "margherita")
    assert margherita["price"] == 8.5
    assert menu.price("pasta", "pesto") == 8.5


def test_unit_price_copied_at_add_time_and_totals_computed(menu):
    fake = FakeClient()
    order = Order()
    tools.dispatch(order, menu, fake, "add_items",
                   {"items": [{"type": "pizza", "code": "margherita",
                               "qty": 3},
                              {"type": "pizza", "code": "funghi",
                               "qty": 1}]})
    snap = order.snapshot()
    line = snap["items"][0]
    assert line["unit_price"] == 8.5
    assert line["line_total"] == 25.5
    assert snap["basket_total"] == 34.5  # 3*8.5 + 9.0


def test_totals_use_cent_rounding_not_float_accumulation():
    from core.order import Item
    order = Order()
    # 0.1 * 3 is the classic float trap: 0.30000000000000004
    order.items.append(Item("pizza", "x", "X", 3, [], unit_price=0.1))
    snap = order.snapshot()
    assert snap["items"][0]["line_total"] == 0.3
    assert snap["basket_total"] == 0.3


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

exec
/bin/bash -lc "sed -n '1,260p' core/order.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' tests/stubs.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' channels/speech.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' tests/test_transcripts.py" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 503ms:
"""Offline stand-ins for the two external services: a stub PizzaSim API
and a stub LLM gateway (a scripted model in the golden-transcript spirit).
Both run as real HTTP servers so the app under test is exercised through
its production code paths — no network beyond localhost, no LLM."""
from __future__ import annotations

import json
import threading
import time
import uuid
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

FIXTURES = Path(__file__).parent / "fixtures"
MENU = json.loads((FIXTURES / "menu.json").read_text())


class StubPizzaSim:
    def __init__(self):
        self.pizzerias = [
            {"id": "11111111-aaaa-bbbb-cccc-000000000001",
             "name": "Stub Pizzeria Uno"},
            {"id": "22222222-aaaa-bbbb-cccc-000000000002",
             "name": "Stub Pizzeria Due"},
        ]
        self.orders: dict[str, list[dict]] = {}
        self.fail_pizzerias = False
        self.app = app = FastAPI()

        @app.get("/menu")
        def menu():
            return MENU

        @app.get("/pizzerias")
        def pizzerias():
            if self.fail_pizzerias:
                return JSONResponse({"error": "boom"}, status_code=500)
            return {"pizzerias": self.pizzerias}

        @app.get("/pizzerias/{pid}/orders")
        def list_orders(pid: str):
            listed = [{k: o[k] for k in
                       ("id", "created_at", "ready_at", "status")}
                      | {"first_name": o["customer"]["first_name"],
                         "customer_id": o["customer_id"]}
                      for o in self.orders.get(pid, [])]
            return {"orders": list(reversed(listed))}

        @app.post("/pizzerias/{pid}/orders")
        async def create_order(pid: str, request: Request):
            body = await request.json()
            now = int(time.time())
            order = {
                "id": str(uuid.uuid4()),
                "customer_id": str(uuid.uuid4()),
                "customer": body["customer"],
                "items": body["items"],
                "created_at": now,
                "ready_at": now + 120,
                "status": "ordered",
            }
            self.orders.setdefault(pid, []).append(order)
            return {"order_id": order["id"], "status": "ordered",
                    "eta_seconds": 120}

        @app.get("/pizzerias/{pid}/orders/{oid}")
        def order_detail(pid: str, oid: str):
            for order in self.orders.get(pid, []):
                if order["id"] == oid:
                    return {k: order[k] for k in
                            ("id", "customer", "items", "created_at",
                             "ready_at", "status")}
            return JSONResponse({"error": "not_found"}, status_code=404)

        @app.get("/location")
        def location(street: str = ""):
            return {"street": street, "deliverable": True}


def _tool_call(name: str, args: dict) -> dict:
    return {"tool_calls": [{
        "id": f"stub-{name}-{uuid.uuid4().hex[:6]}",
        "type": "function",
        "function": {"name": name, "arguments": json.dumps(args)},
    }]}


class StubGateway:
    """A scripted, deterministic model. mode: 'ok' plays a fixed order
    script; 'http500' simulates the gateway being unreachable; 'empty'
    returns an empty final message (stream ends without an answer)."""

    def __init__(self):
        self.mode = "ok"
        self.app = app = FastAPI()

        @app.post("/chat/completions")
        async def chat(request: Request):
            if self.mode == "http500":
                return JSONResponse({"error": "boom"}, status_code=500)
            body = await request.json()
            if self.mode == "empty":
                return _reply({"content": ""})
            return _reply(self._script(body["messages"]))


def _reply(message: dict) -> dict:
    return {"choices": [{"message": message}]}


def _last_tool(messages: list[dict]) -> tuple[str, dict] | None:
    last = messages[-1]
    if last.get("role") != "tool":
        return None
    call_id = last.get("tool_call_id")
    for msg in reversed(messages):
        for call in (msg.get("tool_calls") or []):
            if call["id"] == call_id:
                return call["function"]["name"], json.loads(last["content"])
    return None


def _script_impl(messages: list[dict]) -> dict:
    tool = _last_tool(messages)
    if tool:
        name, result = tool
        if "error" in result:
            return {"content": "Das habe ich leider nicht im Angebot — "
                               "vielleicht Pasta Funghi?"}
        if name == "get_menu":
            price = next(p["price"] for p in result["menu"]["pizzas"]
                         if p["code"] == "margherita")
            return {"content": f"Eine Margherita kostet {price} €."}
        if name == "add_items":
            return {"content": "Gern. Wie ist Ihr Vorname?"}
        if name == "set_customer":
            return _tool_call("read_back", {})
        if name == "read_back":
            return {"content": "Ich lese vor — bitte bestätigen Sie die "
                               "Bestellung."}
        if name == "submit_order":
            return {"content": "Bestellt! Ihre Nummer ist "
                               f"{result['order_id']}."}
        if name == "confirm_order":
            return _tool_call("submit_order", {})
        return {"content": "Alles klar."}

    users = [m for m in messages if m.get("role") == "user"]
    if not users:
        return {"content": "Willkommen! Was darf es sein?"}
    text = users[-1]["content"].lower()
    if "kostet" in text or "cost" in text:
        return _tool_call("get_menu", {})
    if "bolognese" in text:
        return _tool_call("add_items", {"items": [
            {"type": "pasta", "code": "bolognese", "qty": 1}]})
    if "margherita" in text:
        return _tool_call("add_items", {"items": [
            {"type": "pizza", "code": "margherita", "qty": 2}]})
    if "heiße" in text or "name is" in text:
        return _tool_call("set_customer", {"first_name": "Eva"})
    return {"content": "Was darf es sein?"}


StubGateway._script = staticmethod(_script_impl)


def run_server(app: FastAPI) -> tuple[uvicorn.Server, str]:
    config = uvicorn.Config(app, host="127.0.0.1", port=0,
                            log_level="warning")
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    for _ in range(200):
        if server.started:
            break
        time.sleep(0.025)
    else:
        raise RuntimeError("stub server did not start")
    port = server.servers[0].sockets[0].getsockname()[1]
    return server, f"http://127.0.0.1:{port}"

 succeeded in 531ms:
"""Order data: items, customer, revision, submit bookkeeping. Pure data."""
from __future__ import annotations

from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal
from enum import Enum


def _cents(value: Decimal) -> float:
    return float(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


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
    # Copied from the session menu snapshot at add time; totals are
    # computed here in core only — the model never does arithmetic.
    unit_price: float = 0.0

    def line_key(self) -> tuple:
        return (self.type, self.code, tuple(sorted(self.extras)))

    def line_total(self) -> float:
        return _cents(Decimal(str(self.unit_price)) * self.qty)


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
                    "unit_price": i.unit_price,
                    "line_total": i.line_total(),
                }
                for i in self.items
            ],
            "basket_total": _cents(
                sum((Decimal(str(i.unit_price)) * i.qty
                     for i in self.items), Decimal("0"))
            ),
            "customer": self.customer.as_dict() if self.customer else None,
            "read_back_done": self.read_back_revision == self.revision,
        }

 succeeded in 607ms:
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
                      messages=[{"role": "system", "content": "stub"}],
                      client=client)
    agent = Agent(config, chat_fn=stub)

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
                      messages=[{"role": "system", "content": "stub"}],
                      client=ScriptedClient("ok"), lang="en")
    agent = Agent(config, chat_fn=flaky)
    text = agent.run_turn(session, "hello")
    assert "sorry" in text.lower()
    assert session.order.state.value == "EMPTY"  # turn aborted cleanly

 succeeded in 634ms:
"""Speech service client: self-hosted, OpenAI-compatible, optional.

The browser captures and plays audio; recognition and synthesis happen
here, server-side, against {SPEECH_URL}. The language sent with STT/TTS is
the session language — there is no separate speech-language config.
"""
from __future__ import annotations

import sys

import httpx

from core.pizzasim import optional_env


class SpeechUnavailable(Exception):
    pass


class SpeechService:
    """All-or-nothing: enabled only if SPEECH_URL is set, all models are
    configured, and the service answered the startup probe with 2xx."""

    def __init__(self):
        self.url = (optional_env("SPEECH_URL") or "").rstrip("/")
        self.stt_model = optional_env("SPEECH_STT_MODEL")
        self.tts_model = optional_env("SPEECH_TTS_MODEL")
        self.voice = optional_env("SPEECH_TTS_VOICE")
        self.enabled = False
        if self.url and self.stt_model and self.tts_model and self.voice:
            try:
                httpx.get(f"{self.url}/v1/models",
                          timeout=3.0).raise_for_status()
                self.enabled = True
            except httpx.HTTPError:
                print("speech service not answering — text-only mode",
                      file=sys.stderr)

    def stt(self, audio: bytes, filename: str, content_type: str,
            lang: str) -> str:
        try:
            response = httpx.post(
                f"{self.url}/v1/audio/transcriptions",
                files={"file": (filename, audio, content_type)},
                data={"model": self.stt_model, "language": lang},
                timeout=60.0)
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise SpeechUnavailable(str(exc)) from exc
        return response.json().get("text", "")

    def tts(self, text: str, lang: str) -> tuple[bytes, str]:
        try:
            response = httpx.post(
                f"{self.url}/v1/audio/speech",
                json={"model": self.tts_model, "voice": self.voice,
                      "input": text, "language": lang},
                timeout=60.0)
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise SpeechUnavailable(str(exc)) from exc
        return (response.content,
                response.headers.get("content-type", "audio/mpeg"))

codex
The current code confirms the main extension points: snapshot-based tool results, `session.messages` as the model-visible trace, and a startup-probed `SpeechService`. I’m reading the agent loop and the rest of the web tests now to judge whether the plan’s tests really fence off the known failure modes.
exec
/bin/bash -lc "sed -n '1,360p' core/agent.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '320,520p' tests/test_web_e2e.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc 'rg -n "spoken|session.messages|tool_result|JSONL|log|saved address|street_on_file|read_back" core channels tests' in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 212ms:
"""Model loop: prompt assembly, chat-completions calls, tool dispatch,
JSONL event logging. The model only speaks; the order lives in core.

v2: everything tenant-, language- and menu-scoped lives in the per-session
Session; the session factory owns tenant validation and construction. The
transport passes identifiers only.
"""
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
from .pizzasim import NotFoundError, PizzaSim, optional_env, require_env

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

SPOKEN_NOTE = {
    "de": "Diese Antwort wird vorgelesen: höchstens drei Gerichte nennen, "
          "Zeiten in Minuten, Bestellnummern in Gruppen, kurze Sätze.",
    "en": "This reply will be spoken aloud: name at most three dishes, "
          "times in minutes, order ids in groups, short sentences.",
}


class GatewayError(Exception):
    pass


@dataclass
class AgentConfig:
    url: str
    key: str
    model: str
    lang: str  # PIZZERIA_LANG: the initial/default session language

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
    tenant-bound client, one language, one history. The tenant fields are
    set at creation and never mutated — switching pizzeria is a new
    Session (SPEC invariant 6)."""
    order: Order
    menu: Menu
    messages: list[dict]
    client: PizzaSim | None = None
    pizzeria_id: str = ""
    pizzeria_name: str = ""
    lang: str = "de"
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])


def create_session(config: AgentConfig, base: PizzaSim,
                   pizzeria_id: str | None = None,
                   lang: str | None = None) -> Session:
    """Core-owned session factory. Validates the tenant against the live
    pizzeria list, builds the tenant-bound client, fetches the session's
    immutable menu snapshot, renders the prompt. Raises NotFoundError for
    an unknown/vanished pizzeria (session error — the process stays up)."""
    pizzeria_id = pizzeria_id or base.pizzeria_id
    lang = (lang or config.lang).lower()
    if lang not in ("de", "en"):
        lang = config.lang
    names = {p["id"]: p["name"] for p in base.list_pizzerias()}
    if pizzeria_id not in names:
        raise NotFoundError(
            f"pizzeria {pizzeria_id} not found on the PizzaSim server"
        )
    client = base.for_pizzeria(pizzeria_id)
    menu = Menu(client.get_menu())
    return Session(
        order=Order(),
        menu=menu,
        messages=[{"role": "system",
                   "content": system_prompt(lang, names[pizzeria_id])}],
        client=client,
        pizzeria_id=pizzeria_id,
        pizzeria_name=names[pizzeria_id],
        lang=lang,
    )


def set_language(session: Session, lang: str) -> None:
    """The customer's language declaration (web header switch). Re-renders
    the system prompt in place — same policy text, history preserved."""
    lang = lang.lower()
    if lang not in ("de", "en") or lang == session.lang:
        return
    session.lang = lang
    session.messages[0] = {
        "role": "system",
        "content": system_prompt(lang, session.pizzeria_name),
    }
    log_event(session, {"type": "language", "lang": lang})


def log_event(session: Session, event: dict) -> None:
    """One line per event, JSON, to a file. Never carries config values."""
    LOG_DIR.mkdir(exist_ok=True)
    record = {"ts": round(time.time(), 3), "session": session.id, **event}
    with (LOG_DIR / f"agent-{session.id}.jsonl").open("a") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")


class Agent:
    def __init__(self, config: AgentConfig, chat_fn=None, status_cb=None):
        self.config = config
        # chat_fn(messages, tools) -> assistant message dict; injectable so
        # the golden transcripts and E2E stubs run without the gateway.
        self._chat_fn = chat_fn or self._gateway_chat
        # status_cb("ok"|"down"): process-wide gateway health, fed by every
        # call from any session (/chat and /confirm share this path).
        self._status_cb = status_cb or (lambda status: None)

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
                message = response.json()["choices"][0]["message"]
                self._status_cb("ok")
                return message
            except httpx.TimeoutException as exc:
                last_exc = exc
                continue
            except (httpx.HTTPError, KeyError, ValueError) as exc:
                self._status_cb("down")
                raise GatewayError(f"gateway request failed: "
                                   f"{type(exc).__name__}") from exc
        self._status_cb("down")
        raise GatewayError("gateway timed out twice") from last_exc

    def run_turn(self, session: Session, user_text: str | None,
                 emit=lambda event: None, spoken: bool = False) -> str:
        """One customer turn: returns the assistant's final text. Every
        intermediate step goes to emit() and the JSONL log. user_text None
        is the opening/continuation turn — the agent speaks unprompted."""

        def event(payload: dict) -> None:
            log_event(session, payload)
            emit(payload)

        if user_text is not None:
            session.messages.append({"role": "user", "content": user_text})
            event({"type": "user", "text": user_text})
        # Ephemeral per-turn note: activates the spoken-style policy that
        # lives in the prompt. Never persisted — a later typed turn must
        # not inherit the spoken constraints.
        extra = ([{"role": "system", "content": SPOKEN_NOTE[session.lang]}]
                 if spoken else [])

        for _ in range(MAX_TOOL_ROUNDS):
            try:
                message = self._chat_fn(session.messages + extra,
                                        tools.openai_tools())
            except GatewayError as exc:
                event({"type": "error", "error": str(exc)})
                apology = APOLOGY[session.lang]
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
                                        session.client, name, args)
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
        apology = APOLOGY[session.lang]
        session.messages.append({"role": "assistant", "content": apology})
        event({"type": "assistant", "text": apology})
        return apology

    def _synthetic_call(self, session: Session, name: str, args: dict,
                        event) -> dict:
        """One UI-initiated dispatch, recorded exactly like a model call:
        synthetic assistant tool_calls message + tool result + events."""
        call_id = f"ui-{name}-{session.order.revision}"
        event({"type": "tool_call", "tool": name, "args": args})
        session.messages.append({
            "role": "assistant",
            "content": None,
            "tool_calls": [{"id": call_id, "type": "function",
                            "function": {"name": name,
                                         "arguments": json.dumps(args)}}],
        })
        result = tools.dispatch(session.order, session.menu,
                                session.client, name, args)
        event({"type": "tool_result", "tool": name, "result": result})
        event({"type": "state", "state": session.order.state.value,
               "revision": session.order.revision})
        session.messages.append({
            "role": "tool",
            "tool_call_id": call_id,
            "content": json.dumps(result, ensure_ascii=False),
        })
        return result

    def confirm_and_submit(self, session: Session, revision: int,
                           emit=lambda event: None) -> str:
        """The explicit confirm control (SPEC: confirmation is an action
        the customer takes). One core path, symmetric for success and
        failure; CONFIRMED stays reachable only via confirm_order."""

        def event(payload: dict) -> None:
            log_event(session, payload)
            emit(payload)

        result = self._synthetic_call(
            session, "confirm_order", {"revision": revision}, event)
        if "error" not in result:
            self._synthetic_call(session, "submit_order", {}, event)
        # The phrasing call is a normal turn: same gateway path, same
        # retry-once, same apology-as-assistant-event on failure.
        return self.run_turn(session, None, emit)


def startup(config: AgentConfig) -> tuple[PizzaSim, str, Menu]:
    """The one startup sequence: env → preselected-pizzeria check → menu
    health check. Raises before the first turn on any failure. The
    preselection is only the default tenant for new sessions."""
    client = PizzaSim.from_env()
    pizzeria_name = client.pizzeria_name()
    menu = Menu(client.get_menu())
    return client, pizzeria_name, menu

 succeeded in 217ms:
    stack["gateway"].mode = "ok"
    page = open_app(page_factory, stack)
    page.fill("#text", "Einmal Bolognese bitte")
    page.click("#send")
    page.wait_for_selector("text=nicht im Angebot", timeout=30000)
    page.close()


def test_e2e_gateway_unreachable_leaves_visible_message(page_factory,
                                                        stack):
    stack["gateway"].mode = "ok"
    page = open_app(page_factory, stack)
    stack["gateway"].mode = "http500"
    try:
        page.fill("#text", "Hallo?")
        page.click("#send")
        # the retry-once path ends in a rendered apology — an answer
        page.wait_for_selector("text=schiefgegangen", timeout=30000)
    finally:
        stack["gateway"].mode = "ok"
    page.close()


def test_e2e_confirm_failure_offers_retry(page_factory, stack):
    """A confirm whose phrasing turn yields no answer leaves a visible
    notice with a retry that re-runs the SAME confirm action — and the
    state machine guarantees the retry can never place a second order."""
    stack["gateway"].mode = "ok"
    page = open_app(page_factory, stack)
    page.fill("#text", "Zwei Margherita bitte")
    page.click("#send")
    page.wait_for_selector("#basket-lines li", timeout=30000)
    page.fill("#text", "Ich heiße Eva")
    page.click("#send")
    page.wait_for_selector(".readback button:enabled", timeout=30000)

    stack["gateway"].mode = "empty"
    try:
        page.locator(".readback button:enabled").click()
        page.wait_for_selector(".notice button", timeout=30000)  # retry
        # the dispatches already ran: the order is submitted and visible
        page.wait_for_selector("#submitted-banner:not([hidden])",
                               timeout=15000)
    finally:
        stack["gateway"].mode = "ok"
    before = page.locator(".msg.assistant").count()
    page.locator(".notice button").last.click()  # retry the confirm
    page.wait_for_function(
        f"document.querySelectorAll('.msg.assistant').length > {before}",
        timeout=30000)  # the agent answers; never a second order
    page.close()


def test_e2e_stream_without_answer_offers_resend(page_factory, stack):
    stack["gateway"].mode = "ok"
    page = open_app(page_factory, stack)
    stack["gateway"].mode = "empty"
    try:
        page.fill("#text", "Hallo?")
        page.click("#send")
        page.wait_for_selector(".notice button", timeout=30000)
    finally:
        stack["gateway"].mode = "ok"
    page.locator(".notice button").last.click()  # resend, now answered
    page.wait_for_function(
        "document.querySelectorAll('.msg.assistant').length >= 2",
        timeout=30000)
    page.close()

 succeeded in 260ms:
channels/web.py:1:"""FastAPI web channel on port 8888. Same core, zero order logic here —
channels/web.py:173:    spoken = bool(body.get("spoken"))
channels/web.py:177:                                              spoken=spoken),
channels/cli.py:2:words out, no order logic.
channels/cli.py:22:        elif kind == "tool_result":
channels/static/app.js:207:      if (ev.type === "tool_call" || ev.type === "tool_result") {
channels/static/app.js:212:        if (ev.type === "tool_result" && !ev.result.error) {
channels/static/app.js:216:            if (ev.tool === "read_back") showReadback(ev.result.snapshot);
channels/static/app.js:284:async function sendTurn(text, spoken = false) {
channels/static/app.js:287:    "/chat", { session_id: session.id, text, spoken }, text ?? undefined);
tests/test_state.py:25:    state.read_back(o)
tests/test_state.py:48:    state.read_back(o)
tests/test_state.py:72:    lambda o: state.read_back(o),
tests/test_state.py:89:def test_read_back_empty():
tests/test_state.py:91:        state.read_back(order_in(State.EMPTY))
tests/test_state.py:95:def test_read_back_collecting_needs_customer():
tests/test_state.py:97:        state.read_back(order_in(State.COLLECTING))
tests/test_state.py:162:def test_confirm_without_read_back():
tests/test_state.py:166:    assert e.value.code == "read_back_required"
tests/test_state.py:171:    state.read_back(o)
tests/test_state.py:179:def test_read_back_of_old_revision_does_not_allow_confirm():
tests/test_state.py:181:    state.read_back(o)
tests/test_state.py:185:    assert e.value.code == "read_back_required"
tests/test_transcripts.py:96:        if event["type"] == "tool_result" and "error" in event["result"]:
tests/test_transcripts.py:121:def test_gateway_timeout_apology():
tests/test_transcripts.py:122:    """Gateway timeout: one retry, then abort the turn with an apology."""
core/menu.py:29:    def as_tool_result(self) -> dict:
tests/transcripts/unknown_item.json:5:    {"user": "Einmal Pasta Bolognese bitte.",
tests/transcripts/unknown_item.json:7:       {"tool": "add_items", "args": {"items": [{"type": "pasta", "code": "bolognese", "qty": 1, "extras": []}]}},
tests/transcripts/unknown_item.json:8:       {"say": "Bolognese habe ich leider nicht. Ich hätte Pasta Pesto, Pasta Funghi oder Pasta Tonno — was davon?"}
tests/transcripts/unknown_item.json:18:       {"tool": "read_back", "args": {}},
tests/transcripts/unknown_item.json:30:    "calls": ["add_items", "add_items", "set_customer", "read_back", "confirm_order", "submit_order"],
core/state.py:89:def read_back(order: Order) -> None:
core/state.py:100:    order.read_back_revision = order.revision
core/state.py:120:    if order.read_back_revision != order.revision:
core/state.py:122:            "read_back_required",
tests/transcripts/mind_change.json:2:  "name": "mind_change_after_read_back",
tests/transcripts/mind_change.json:9:       {"tool": "read_back", "args": {}},
tests/transcripts/mind_change.json:16:       {"tool": "read_back", "args": {}},
tests/transcripts/mind_change.json:28:    "calls": ["add_items", "set_customer", "read_back", "add_items", "confirm_order", "read_back", "confirm_order", "submit_order"],
tests/transcripts/submit_timeout.json:9:       {"tool": "read_back", "args": {}},
tests/transcripts/submit_timeout.json:26:    "calls": ["add_items", "set_customer", "read_back", "confirm_order", "submit_order", "submit_order"],
tests/transcripts/correction.json:18:       {"tool": "read_back", "args": {}},
tests/transcripts/correction.json:30:    "calls": ["add_items", "add_items", "set_customer", "read_back", "confirm_order", "submit_order"],
core/agent.py:2:JSONL event logging. The model only speaks; the order lives in core.
core/agent.py:24:LOG_DIR = Path("logs")
core/agent.py:38:    "en": "This reply will be spoken aloud: name at most three dishes, "
core/agent.py:128:    session.messages[0] = {
core/agent.py:132:    log_event(session, {"type": "language", "lang": lang})
core/agent.py:135:def log_event(session: Session, event: dict) -> None:
core/agent.py:183:                 emit=lambda event: None, spoken: bool = False) -> str:
core/agent.py:185:        intermediate step goes to emit() and the JSONL log. user_text None
core/agent.py:189:            log_event(session, payload)
core/agent.py:193:            session.messages.append({"role": "user", "content": user_text})
core/agent.py:195:        # Ephemeral per-turn note: activates the spoken-style policy that
core/agent.py:197:        # not inherit the spoken constraints.
core/agent.py:199:                 if spoken else [])
core/agent.py:203:                message = self._chat_fn(session.messages + extra,
core/agent.py:207:                apology = APOLOGY[session.lang]
core/agent.py:208:                session.messages.append({"role": "assistant",
core/agent.py:209:                                         "content": apology})
core/agent.py:210:                event({"type": "assistant", "text": apology})
core/agent.py:211:                return apology
core/agent.py:216:                session.messages.append({"role": "assistant",
core/agent.py:221:            session.messages.append({
core/agent.py:235:                event({"type": "tool_result", "tool": name,
core/agent.py:240:                session.messages.append({
core/agent.py:247:        apology = APOLOGY[session.lang]
core/agent.py:248:        session.messages.append({"role": "assistant", "content": apology})
core/agent.py:249:        event({"type": "assistant", "text": apology})
core/agent.py:250:        return apology
core/agent.py:258:        session.messages.append({
core/agent.py:267:        event({"type": "tool_result", "tool": name, "result": result})
core/agent.py:270:        session.messages.append({
core/agent.py:284:            log_event(session, payload)
core/agent.py:292:        # retry-once, same apology-as-assistant-event on failure.
core/order.py:53:    read_back_revision: int | None = None
core/order.py:81:            "read_back_done": self.read_back_revision == self.revision,
tests/test_tools.py:135:    result = menu.as_tool_result()
tests/test_tools.py:216:    tools.dispatch(order, menu, fake, "read_back", {})
tests/test_tools.py:234:    assert snap["customer"] is None and snap["read_back_done"] is False
tests/test_tools.py:371:    tools.dispatch(order, menu, fake, "read_back", {})
tests/test_tools.py:435:    tools.dispatch(order, menu, fake, "read_back", {})
tests/test_tools.py:506:    assert "Pizzeria Default" in session.messages[0]["content"]
tests/test_tools.py:523:    history_before = len(session.messages)
tests/test_tools.py:524:    german = session.messages[0]["content"]
tests/test_tools.py:527:    assert session.messages[0]["content"] != german
tests/test_tools.py:528:    assert "Pizzeria Default" in session.messages[0]["content"]
tests/test_tools.py:529:    assert len(session.messages) == history_before  # history preserved
tests/test_tools.py:532:def test_apology_follows_session_language():
tests/test_tools.py:541:def test_spoken_note_is_ephemeral_per_turn():
tests/test_tools.py:542:    """The spoken-style note reaches the model for the spoken turn only —
tests/test_tools.py:552:    agent.run_turn(session, "hallo", spoken=True)
tests/test_tools.py:560:                   for m in session.messages)  # never persisted
tests/test_tools.py:571:    tools.dispatch(session.order, session.menu, fake, "read_back", {})
tests/test_tools.py:587:    roles = [m["role"] for m in session.messages]
tests/test_tools.py:589:    assert session.messages[-1]["role"] == "assistant"
tests/test_tools.py:603:              if e["type"] == "tool_result" and "error" in e["result"]]
tests/test_tools.py:608:    assert session.messages[-2]["role"] == "tool"
tests/test_tools.py:613:    apology streamed as an assistant event."""
tests/test_tools.py:622:    assert text  # the apology is the rendered answer
tests/test_tools.py:631:    text = agent.run_turn(session, "hi")  # closed port → down + apology
tests/test_tools.py:653:        ("read_back", {}),
core/tools.py:64:    {"name": "read_back",
core/tools.py:133:        return {"menu": menu.as_tool_result(), "snapshot": order.snapshot()}
core/tools.py:170:    if name == "read_back":
core/tools.py:171:        state.read_back(order)
tests/transcripts/happy_path.json:18:       {"tool": "read_back", "args": {}},
tests/transcripts/happy_path.json:30:    "calls": ["get_menu", "add_items", "set_customer", "read_back", "confirm_order", "submit_order"],
tests/test_web_e2e.py:139:                           "text": "Einmal Bolognese bitte"})
tests/test_web_e2e.py:140:    errors = [e for e in events if e["type"] == "tool_result"
tests/test_web_e2e.py:157:                if e["type"] == "tool_result"
tests/test_web_e2e.py:158:                and e.get("tool") == "read_back"][-1]
tests/test_web_e2e.py:163:                 if e["type"] == "tool_result"
tests/test_web_e2e.py:184:              if e["type"] == "tool_result" and "error" in e["result"]]
tests/test_web_e2e.py:322:    page.fill("#text", "Einmal Bolognese bitte")
tests/test_web_e2e.py:336:        # the retry-once path ends in a rendered apology — an answer
tests/stubs.py:140:            return _tool_call("read_back", {})
tests/stubs.py:141:        if name == "read_back":
tests/stubs.py:157:    if "bolognese" in text:
tests/stubs.py:159:            {"type": "pasta", "code": "bolognese", "qty": 1}]})
tests/stubs.py:173:                            log_level="warning")

codex
I’ve checked the known round-1/2 fault lines against the current code paths. One more pass on the remaining speech UI code is enough to decide whether the plan is now airtight or still leaves an exploitable gap.
exec
/bin/bash -lc "nl -ba PLAN.md | sed -n '373,560p'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '320,520p' channels/static/app.js" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "nl -ba SPEC.md | sed -n '320,410p;478,670p;748,770p'" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 172ms:
   373	# Delta Plan v3 — Street lookup + Voice (SPEC rev d851966)
   374	
   375	> Stage-1 artifact for the two SPEC extensions committed after v1.0.0:
   376	> returning-customer street reuse (confirm-without-disclosure) and voice as
   377	> a required release capability. Design only — no code before the gate
   378	> approves. Everything in Plan v2 above stands; this section only adds.
   379	
   380	## A. Street lookup (SPEC: lookup_customer / use_saved_street / redaction)
   381	
   382	Core:
   383	
   384	- `core/pizzasim.py`: `list_customers()` → `GET /pizzerias/{id}/customers`
   385	  → `customers[]`. Customers with `deleted_at != null` are treated as
   386	  nonexistent everywhere.
   387	- `core/order.py`: `Customer` gains `street_from_saved: bool = False`.
   388	  Two serializations, one redaction rule:
   389	  - `as_dict()` (used by SNAPSHOT, hence by every tool result, streamed
   390	    event, transcript and log line): when `street_from_saved`, it carries
   391	    `{"first_name", "street_one": null, "street_on_file": true}` — the
   392	    saved text never appears. A street the customer dictated themselves is
   393	    echoed as before (`street_on_file` absent/false).
   394	  - `as_submit_dict()` (used only to build the POST /orders body): always
   395	    the real `street_one`. Submit uses saved `street_one` only — never
   396	    `street_two` (SPEC guardrail).
   397	- `core/tools.py`:
   398	  - New tool `lookup_customer` `{first_name}` →
   399	    `{"customer_exists": bool, "saved_street_available": bool, "snapshot"}`
   400	    — booleans only, no street text, no customer id. API failure → the
   401	    uniform error shape with code `api_unavailable` (non-fatal; the model
   402	    falls back to asking for the street).
   403	  - `set_customer` params become `{first_name, street_one?,
   404	    use_saved_street?}` — mutually exclusive; both set → error code
   405	    `invalid_arguments` with a speakable message. With the flag, dispatch
   406	    fetches the customer record in code, copies `street_one`, sets
   407	    `street_from_saved`; unknown name or no saved street → error
   408	    `no_saved_street` (speakable), basket untouched.
   409	  - `_submit` switches from `as_dict()` to `as_submit_dict()`.
   410	- Prompts (both languages): after the name, call `lookup_customer`; if a
   411	  saved street exists ask exactly one confirmation question without
   412	  reciting the address; yes → `set_customer(use_saved_street: true)`;
   413	  no/unknown/error → ask for the street as before. Never state a street
   414	  that came from saved data.
   415	- Web UI: basket + read-back panel render `street_on_file` as the
   416	  localized label "gespeicherte Adresse"/"saved address", never text.
   417	
   418	Tests (ticket introduces them):
   419	
   420	- lookup known / unknown / deleted / API-error (error non-fatal).
   421	- `use_saved_street` copies in code; the redaction sweep is end to end:
   422	  after the full flow, the fixture street text must appear in exactly one
   423	  place — the outbound submit payload (captured via a client spy) — and in
   424	  no snapshot, no emitted event, no JSONL log line, and **no entry of
   425	  `session.messages`** (the model-visible tool-message serialization is
   426	  string-scanned too; an implementation that leaks the street into tool
   427	  content the model reads must fail this test). The same sweep covers
   428	  transcript artifacts: golden transcript fixtures and any
   429	  transcript-derived serialization must not contain saved street text.
   430	- Mutual exclusion + `no_saved_street` paths.
   431	- Two new golden transcripts: saved-address reuse (lookup → confirm
   432	  question → flag-based set_customer → order) and decline/fallback
   433	  (customer says no → street asked, dictated street echoed as before).
   434	
   435	## B. Voice (SPEC: required capability; offline wiring tests + live proof)
   436	
   437	Artifacts:
   438	
   439	- `deploy/speech-service.compose.yml`: neutral, CPU-only service
   440	  definition — image and models come from environment placeholders
   441	  (`SPEECH_IMAGE`, `SPEECH_*`), no vendor or model names in the file, and
   442	  a comment pointing at the OpenAI-compatible surface it must expose.
   443	  README gains a "Voice deployment" section: HTTPS/domain requirement
   444	  (secure context), co-deployment with the app, env wiring.
   445	- `tests/fixtures/audio/`: generated spoken fixtures (offline synthesis
   446	  on the build host if a synthesizer is available, otherwise minimal
   447	  valid WAV containers) — `order.de.wav`, `order.en.wav`; used by the
   448	  offline round-trip (content irrelevant to the stub) and by the live
   449	  voice test (content = a spoken order).
   450	- `tests/stubs.py`: `StubSpeech` — `GET /v1/models` 200;
   451	  `POST /v1/audio/transcriptions` → fixed transcript (per stub script,
   452	  e.g. "Zwei Margherita bitte"), records the language field it received;
   453	  `POST /v1/audio/speech` → tiny valid audio bytes, counts calls.
   454	
   455	Offline tests:
   456	
   457	- API level (app booted with `SPEECH_*` pointing at StubSpeech):
   458	  `/config.speech == true`; `/speech/stt` round trip with an audio
   459	  fixture returns the stub transcript and passed `session.lang` as the
   460	  language; `/speech/tts` returns audio bytes; both 404 when speech is
   461	  unconfigured (existing behaviour, kept).
   462	- Browser E2E (Playwright, localhost = secure context, fake media device
   463	  flags `--use-fake-device-for-media-capture` +
   464	  `--use-fake-ui-for-media-capture` +
   465	  `--use-file-for-fake-audio-capture=<fixture wav>`, microphone
   466	  permission granted): mic button and TTS toggle visible; push-to-talk
   467	  click-start/click-stop records via real `MediaRecorder` (the fake
   468	  device streams the audio fixture), uploads to the stub, transcript
   469	  drives a turn (`spoken: true` asserted via the stub gateway seeing the
   470	  spoken-style note); with the toggle ON, exactly one TTS fetch per turn
   471	  and only for the final assistant message (StubSpeech call counter);
   472	  toggle OFF by default. This real UI push-to-talk path is mandatory —
   473	  API-level speech tests supplement it and never substitute for it.
   474	- **Runtime degradation:** when a speech call fails after startup (STT or
   475	  TTS returns an error / the proxy answers 502), the UI hides the mic and
   476	  the TTS toggle for the rest of the session and shows a plain-language
   477	  notice; typed ordering continues untouched. E2E test: StubSpeech is
   478	  switched to failure mode mid-session → controls disappear, a typed
   479	  order still completes. (Startup-down behaviour — probe fails → controls
   480	  never rendered — exists since v1 and keeps its test.)
   481	- **Secure-context gating in the UI, not just in the docs:** the speech
   482	  controls render only when `window.isSecureContext` is true (HTTPS or
   483	  localhost) in addition to `cfg.speech` and the media APIs. E2E test: an
   484	  init script forces `isSecureContext = false` → with speech fully
   485	  configured, neither mic nor TTS toggle is rendered and text ordering
   486	  works — plain HTTP never presents a voice-capable UI.
   487	- Name-confirmation regression, three scripted cases (the saved-address
   488	  question is **not** a substitute for name confirmation):
   489	  1. plausible-but-wrong spoken name: agent repeats the name back, the
   490	     customer corrects, `set_customer` is called exactly once with the
   491	     corrected name, only after the correction — no submit before that;
   492	  2. spoken happy path, dictated street: the name is confirmed before
   493	     submission;
   494	  3. spoken happy path, saved street reused: the name is confirmed before
   495	     submission *in addition to* the saved-address yes/no question.
   496	  Prompts (both languages) state explicitly: in spoken conversations the
   497	  first name is always confirmed before the order is submitted.
   498	
   499	Live proof (opt-in, release-gating per SPEC):
   500	
   501	- `PIZZA_LIVE_VOICE=1` + `PIZZA_LIVE_VOICE_URL=<https base url of the
   502	  voice-capable deployment>`: a real headless browser drives the real
   503	  page over HTTPS end to end — microphone capture via the fake media
   504	  device streaming `order.de.wav` / `order.en.wav` (Chromium
   505	  `--use-file-for-fake-audio-capture`), real STT through the deployed
   506	  speech service, the transcript drives the chat, the confirm control
   507	  places the order, and with the toggle ON the final assistant message
   508	  fetches real TTS audio (response is non-empty browser-playable audio).
   509	  The four acceptance points are then verified via the pizzeria's
   510	  list+detail API endpoints. Not a text replay: if STT does not produce
   511	  an order-driving transcript from the fixture, the test fails. Skipped
   512	  cleanly when the env vars are unset; it cannot run on the current dev
   513	  VPS (no speech service, no HTTPS) and is executed against the
   514	  voice-capable deployment.
   515	
   516	## C. Tickets (≤1h each)
   517	
   518	1. Street-lookup core (client, Customer redaction split, tools, unit
   519	   tests incl. redaction sweep). ☐ booleans-only lookup ☐ submit carries
   520	   real street ☐ no saved-street text in events, logs or
   521	   session.messages.
   522	2. Street-lookup conversation (prompts DE/EN, two golden transcripts, UI
   523	   label). ☐ confirm-without-disclosure flow ☐ decline fallback.
   524	3. StubSpeech + audio fixtures + API-level speech tests. ☐ stt round
   525	   trip with session lang ☐ tts bytes ☐ 404 when unconfigured.
   526	4. Browser E2E voice wiring (fake media device). ☐ mic/toggle visible
   527	   ☐ push-to-talk round trip ☐ single final-message TTS fetch
   528	   ☐ mid-session speech failure degrades to text-only ☐ insecure
   529	   context renders no speech controls.
   530	5. Name-confirmation regression transcripts, all three cases.
   531	   ☐ wrong-name correction: corrected name only, after confirmation
   532	   ☐ spoken happy path, dictated street: name confirmed before submit
   533	   ☐ spoken happy path, saved street: name confirmed in addition to the
   534	   saved-address yes/no question.
   535	6. deploy/ speech service definition + README voice section.
   536	   ☐ neutral (no vendor/model names) ☐ HTTPS requirement documented.
   537	7. Live voice acceptance test (opt-in) + docs. ☐ DE+EN fixtures
   538	   ☐ gated on `PIZZA_LIVE_VOICE=1` + `PIZZA_LIVE_VOICE_URL` and skips
   539	   cleanly when either is unset ☐ real HTTPS browser path (mic capture →
   540	   STT → chat → confirm control) ☐ STT failing to produce an
   541	   order-driving transcript fails the test ☐ final-message TTS returns
   542	   non-empty playable audio ☐ full-order verification via API.

 succeeded in 202ms:
}

async function refreshConfig() {
  cfg = await (await fetch("/config")).json();
  $("version").textContent = "v" + cfg.version;
  $("docs-link").href = cfg.docs_url;
  fillSelector();
  const speechUsable = cfg.speech;
  $("tts-wrap").hidden = !speechUsable;
  $("mic").hidden = !(speechUsable && navigator.mediaDevices &&
                      window.MediaRecorder);
}

async function startSession(pizzeriaId) {
  // Create the new session FIRST: a failed switch must not hide the
  // still-live conversation and basket the customer can see.
  const res = await fetch("/session", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ pizzeria_id: pizzeriaId, lang }),
  });
  if (!res.ok) {
    notice(t("sessionGone"));
    await refreshConfig();  // fresh selector from the live list
    if (session) $("pizzeria-select").value = session.pizzeriaId;
    return;
  }
  if (currentAbort) currentAbort.abort();
  chat.textContent = "";
  lastOrderId = null;
  renderBasket({ items: [], basket_total: 0, state: "EMPTY",
                 customer: null });
  const data = await res.json();
  session = { id: data.session_id, pizzeriaId: data.pizzeria_id,
              pizzeriaName: data.pizzeria_name };
  $("pizzeria-name").textContent = data.pizzeria_name;
  document.title = data.pizzeria_name;
  $("dashboard-link").hidden = false;
  $("dashboard-link").href = `${cfg.dashboard_base}/${data.pizzeria_id}`;
  $("uuid").textContent = data.pizzeria_id;
  $("pizzeria-select").value = data.pizzeria_id;
  await sendTurn(null);  // the agent greets first
}

/* ---------- speech (capture/playback only) ------------------------------ */

let recorder = null;

async function startRecording() {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  recorder = new MediaRecorder(stream);
  const chunks = [];
  recorder.ondataavailable = (e) => chunks.push(e.data);
  recorder.onstop = async () => {
    stream.getTracks().forEach((tr) => tr.stop());
    $("mic").classList.remove("recording");
    $("mic").setAttribute("aria-pressed", "false");
    const blob = new Blob(chunks, { type: recorder.mimeType });
    const body = new FormData();
    body.append("audio", blob, "speech.webm");
    try {
      const res = await fetch(
        `/speech/stt?session_id=${session.id}`, { method: "POST", body });
      if (!res.ok) throw new Error();
      const { text } = await res.json();
      if (text.trim()) sendTurn(text.trim(), true);
      else notice(t("sttEmpty"));
    } catch {
      notice(t("sttFail"));
    }
  };
  recorder.start();
  $("mic").classList.add("recording");
  $("mic").setAttribute("aria-pressed", "true");
}

$("mic").addEventListener("click", () => {
  if (recorder && recorder.state === "recording") recorder.stop();
  else startRecording().catch(() => notice(t("micDenied")));
});

async function speak(text) {
  try {
    const res = await fetch("/speech/tts", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: session.id, text }),
    });
    if (!res.ok) throw new Error();
    new Audio(URL.createObjectURL(await res.blob())).play();
  } catch {
    notice(t("ttsFail"));
  }
}

/* ---------- health ------------------------------------------------------ */

async function pollHealth() {
  try {
    const h = await (await fetch("/health")).json();
    for (const [id, state] of [["health-api", h.api],
                               ["health-gateway", h.gateway]]) {
      const el = $(id);
      el.classList.remove("ok", "down", "unknown");
      el.classList.add(state);
      el.title = state;
    }
  } catch { /* footer badge keeps its last state */ }
}

/* ---------- wiring ------------------------------------------------------ */

$("composer").addEventListener("submit", (e) => {
  e.preventDefault();
  const text = $("text").value.trim();
  if (!text || !session) return;
  $("text").value = "";
  sendTurn(text);
});

$("pizzeria-select").addEventListener("change", (e) => {
  startSession(e.target.value);
});

$("start-over").addEventListener("click", () => {
  if (session) startSession(session.pizzeriaId);
});

document.querySelectorAll("#lang-switch button").forEach((btn) => {
  btn.addEventListener("click", async () => {
    if (btn.dataset.lang === lang) return;
    lang = btn.dataset.lang;
    applyChrome();
    if (session) {
      await fetch("/language", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: session.id, lang }),
      }).catch(() => {});
    }
  });
});

(async () => {
  try {
    await refreshConfig();
    lang = cfg.lang_default || "de";
    applyChrome();
    await startSession(cfg.preselected_id);
    pollHealth();
    setInterval(pollHealth, 30000);
  } catch {
    notice(I18N[lang].errNetwork);
  }
})();

 succeeded in 175ms:
   320	
   321	The model sees exactly these. Names, parameters and semantics are fixed.
   322	
   323	| Tool | Parameters | Returns |
   324	|---|---|---|
   325	| `get_menu` | — | pizzas and pasta with codes, display names, prices |
   326	| `add_items` | `items[]` of `{type, code, qty, extras[]}` | new basket + revision |
   327	| `remove_item` | `code`, `type`, optional `qty` | new basket + revision |
   328	| `lookup_customer` | `first_name` | `{customer_exists, saved_street_available}` — booleans only, **no street text** |
   329	| `set_customer` | `first_name`, plus either `street_one` **or** `use_saved_street: true` (mutually exclusive) — with the flag, the **code** copies the saved street into the order; the text never passes through the model | customer as stored (saved street as a flag, not text) |
   330	| `read_back` | — | basket, customer name, revision, and the code-computed basket total — the text the agent reads out. A street reused from saved data is **not** recited; the earlier yes/no reuse confirmation covers it |
   331	| `confirm_order` | `revision` | state `CONFIRMED`, or error if stale |
   332	| `submit_order` | — | `order_id`, `status`, `eta_seconds` |
   333	| `check_street` | `street` | plausibility result (optional) |
   334	
   335	Tool result conventions:
   336	
   337	- Success: the **full current state**, not a diff. The model never
   338	  reconstructs the basket from history.
   339	- Failure: `{"error": {"code": "...", "message": "...", "candidates": [...]}}`.
   340	  `message` is written so it can be spoken to the customer as-is.
   341	- `add_items` with an unknown code returns `unknown_item` plus up to three
   342	  candidates from the menu. The model asks; it does not pick.
   343	- Quantities are integers. A tool receiving `"zwei"` returns
   344	  `invalid_quantity`; it does not parse German.
   345	- **Totals are computed in code**, from the API prices captured in the
   346	  session's menu snapshot. The model never does arithmetic on prices; the
   347	  web basket shows the same code-owned total that `read_back` carries.
   348	- `remove_item` parameters are fixed, so when several basket lines share
   349	  `(type, code)` with different `extras[]`, the semantics are
   350	  deterministic: without `qty` every matching line is removed; with `qty`
   351	  the most recently added matching line is reduced.
   352	- **Saved-street redaction.** A street reused from saved customer data
   353	  never appears in tool results, streamed intermediate steps, transcripts
   354	  or the structured logs — only booleans and state flags (e.g.
   355	  `street_on_file: true`) may appear there, and the web UI shows it as
   356	  "saved address", never as text. A street the customer dictated in this
   357	  conversation may be echoed as before — it is their own input. First
   358	  names are the only lookup key, so anyone claiming a name must never be
   359	  able to extract the address behind it.
   360	
   361	---
   362	
   363	## Conversation policy
   364	
   365	This is what the system prompt must produce. Write the prompt to achieve it;
   366	do not paste this section into it verbatim.
   367	
   368	- Greet first, in the session language, and offer help — one sentence, not a
   369	  menu recital.
   370	
   371	**Language authority — one rule.** The session language starts as
   372	`PIZZERIA_LANG` (greeting, CLI, web UI chrome before any switch). The web
   373	header switch changes the session language: UI chrome, the greeting of a
   374	fresh conversation, and the speech hint (STT language, TTS output). For the
   375	agent's replies, per-turn mirroring wins: it answers in the language of the
   376	customer's latest message, even when that differs from the session language.
   377	The CLI has no switch and stays at `PIZZERIA_LANG`.
   378	- **One question per turn.** Never stack "name, street and what would you
   379	  like?"
   380	- Never state a menu item or a price that did not come from `get_menu` in this
   381	  session. Price questions are normal questions, and so is "what does my
   382	  basket come to?"
   383	- Collect the first name; then call `lookup_customer`. If a saved street
   384	  exists, ask exactly one confirmation question ("Soll ich wieder an Ihre
   385	  gespeicherte Adresse liefern?") **without reciting the address**; on yes,
   386	  `set_customer(use_saved_street: true)`. If the customer declines, is
   387	  unknown, or the lookup fails (non-fatal), ask for the street as usual.
   388	  If the customer declines the street entirely, accept it — it is optional
   389	  in the API.
   390	- Before submitting: call `read_back`, present it, and wait for an explicit
   391	  yes. "Mhm" and silence are not a yes; ask once more, then offer to start
   392	  over.
   393	- Never announce that an order was placed before `submit_order` returned an
   394	  `order_id`.
   395	- On success, state the order id in a form a human can repeat back, and the
   396	  wait time in **minutes**, converted from `eta_seconds`.
   397	- On error, explain in plain language what happened and what the options are.
   398	  Never show a status code, stack trace or JSON.
   399	- Never claim to have checked an address for deliverability.
   400	
   401	---
   402	
   403	## The web channel
   404	
   405	The web UI is where a stranger decides whether this thing works. Everything
   406	below is required, and each line is written so it can be checked by looking at
   407	the page.
   408	
   409	### The conversation
   410	
   478	## Speech
   479	
   480	Speech is an input and an output method on the web channel, served by a
   481	**self-hosted speech service**: CPU-only, in its own container, reached over
   482	plain HTTP with an OpenAI-compatible surface.
   483	
   484	| Direction | Endpoint | Payload |
   485	|---|---|---|
   486	| STT | `POST {SPEECH_URL}/v1/audio/transcriptions` | multipart audio + model + language |
   487	| TTS | `POST {SPEECH_URL}/v1/audio/speech` | JSON: model, voice, input text → audio |
   488	
   489	- **The speech service is the only speech path.** No external speech
   490	  provider, no hosted realtime framework, no audio through the LLM gateway —
   491	  that gateway carries chat completions only.
   492	- **The browser captures and plays audio; it does not recognise or synthesise
   493	  it.** Capture via `getUserMedia` and `MediaRecorder`, playback via a plain
   494	  audio element — cross-browser and cross-platform: Firefox, Safari, Chrome,
   495	  on Linux, macOS and Windows alike.
   496	- **The browser speech APIs are forbidden.** `SpeechRecognition` and
   497	  `speechSynthesis` tied the previous implementation to a single browser
   498	  vendor and sent customer audio to a third party. The self-hosted service
   499	  exists to replace them.
   500	- **Nothing about the speech stack is written into source.** Base URL, models
   501	  and voice come from the environment, exactly like the chat model; the
   502	  language sent with STT/TTS requests is the session language (see
   503	  *Language authority* under Conversation policy), not a separate config.
   504	- **Request/response, not streaming.** Record, upload, transcript back.
   505	  Latency is visible and acceptable; do not build partial results, barge-in
   506	  or turn detection on top — this transport cannot do them, and pretending
   507	  otherwise produces a broken feel.
   508	- **Push-to-talk.** The microphone starts and stops on the customer's action,
   509	  never listens continuously. Recording state is visible at all times.
   510	- **Synthesis is optional and off by default**, toggled by the customer,
   511	  applied only to the final assistant message.
   512	- **Speech is a required product capability for release completeness.**
   513	  Text-only is the degraded fallback when speech is unconfigured in
   514	  dev/test or temporarily unavailable at runtime: microphone and speaker
   515	  toggle are then not rendered and the text UI is fully usable, and a
   516	  speech outage must never block typed ordering. But a production release
   517	  without a working speech path is not done.
   518	- **Voice-capable web deployments run in a secure browser context:**
   519	  HTTPS on a real host/domain, or localhost during development. Plain
   520	  HTTP is not a valid acceptance environment for microphone input
   521	  (`getUserMedia` is unavailable there).
   522	- **Transport formats:** the STT path accepts the browser-recorded audio
   523	  format emitted by `MediaRecorder`; the TTS path returns audio playable
   524	  by a standard browser audio element.
   525	- **Latency:** each STT and each TTS request should complete quickly
   526	  enough for turn-based conversation on demo hardware; sustained
   527	  multi-second delays that make turn-taking awkward are a defect.
   528	- **Speech shortens answers, it does not change them.** Same core, same
   529	  tools, same state machine. When a reply will be spoken: at most three menu
   530	  items plus an invitation, times in minutes, order id read in groups.
   531	- **Confirm the name.** Transcription errors on names are the expensive
   532	  failure: a misheard name silently creates a customer nobody will find
   533	  again. Read the name back before submitting.
   534	
   535	### Speech service provisioning
   536	
   537	The deployment includes a self-hosted, CPU-only speech service reachable
   538	at `SPEECH_URL`, exposing OpenAI-compatible
   539	`POST /v1/audio/transcriptions` and `POST /v1/audio/speech`. The
   540	application and the speech service are deployed together as first-party
   541	artifacts. The repository includes a neutral deployment definition for
   542	this service next to the app deployment artifacts (no vendor or model
   543	names in source or spec — the operator configures them via the
   544	environment, exactly like the chat model).
   545	
   546	---
   547	
   548	## Error handling
   549	
   550	Every case below needs a test and a phrasing.
   551	
   552	| Situation | Code does | Customer sees/hears |
   553	|---|---|---|
   554	| Gateway timeout | one retry, then abort turn | plain apology, offer to resend |
   555	| `401`/`403` from PizzaSim | abort, log, do not retry | "I can't reach the kitchen system right now" |
   556	| `404` on the preselected `PIZZERIA_ID` | fail at startup, not mid-call | — (process refuses to start) |
   557	| Runtime pizzeria selection invalid/gone | session error, refresh the selector; process stays up | "that pizzeria isn't available right now" |
   558	| `422` validation | surface field, keep basket | targeted question about the offending item |
   559	| `5xx` on submit | **no blind retry** | "I'm not sure that went through — let me check" |
   560	| Timeout on submit | mark `UNKNOWN`; shortlist via `GET /pizzerias/{id}/orders`, verify items via `GET /pizzerias/{id}/orders/{order_id}` before any retry | as above |
   561	| Unknown item code | `unknown_item` + candidates | "I have Margherita or Marinara — which one?" |
   562	| Empty basket at submit | reject transition | "What can I get you?" |
   563	| Menu fetch fails at start | fail fast | "We're not taking orders right now" |
   564	| Pizzeria list fetch fails | no selector, say so | list unavailable — no fallback entry |
   565	| Speech service down | hide speech controls | text UI unaffected |
   566	
   567	The submit-timeout case is the one that matters: a blind retry doubles a real
   568	order. Recovery: shortlist candidates on the pizzeria's order list, then
   569	verify the candidate's items via `GET /pizzerias/{id}/orders/{order_id}` —
   570	only a verified match is adopted, anything else allows exactly one retry. If
   571	list or detail lookup fails, tell the customer honestly.
   572	
   573	---
   574	
   575	## Anti-patterns — explicitly forbidden
   576	
   577	Each of these was present in a previous implementation. None is a matter of
   578	taste.
   579	
   580	1. **A regex "fast path" that places an order without the model.** It bypasses
   581	   confirmation, mis-parses quantities, duplicates items on overlapping
   582	   matches, and makes the tool-calling architecture decorative.
   583	2. **Shelling out to `curl` via `subprocess`.** Use an HTTP client: no shell
   584	   quoting bugs, no injection surface, real timeouts, testable.
   585	3. **Hardcoded pizzeria UUID or hardcoded menu fallback.** Both send orders to
   586	   the wrong place while looking like they work. The same ban covers a
   587	   fallback entry in the pizzeria selector.
   588	4. **A system prompt that forbids confirmation** ("never ask if they're sure,
   589	   always place the order immediately"). That is the bug, written down as a
   590	   rule.
   591	5. **Prompt shouting.** ALL-CAPS threats are what people write instead of
   592	   enforcing the rule in code. The state machine enforces it; the prompt stays
   593	   calm and short.
   594	6. **A frontend that discards stream events.** The previous UI rendered only
   595	   the final message and threw tool events away — the customer watched a
   596	   frozen screen while the agent worked. Rendering the intermediate steps is
   597	   part of the product, not a debug view.
   598	
   599	---
   600	
   601	## Testing
   602	
   603	- **Unit:** the state machine, exhaustively. Every illegal transition has a
   604	  test asserting it is refused.
   605	- **Tool level:** against recorded API fixtures. No network, no LLM, fast.
   606	- **Golden transcripts:** scripted conversations against a stub model
   607	  replaying fixed tool calls — happy path, correction, unknown item, customer
   608	  changes mind after read-back, submit timeout, saved-address reuse, and a
   609	  decline/fallback variant. Assert final state and the calls actually made.
   610	- **Address reuse:** tool-level tests for `lookup_customer`
   611	  (known/unknown/API error — the error is non-fatal) and for
   612	  `set_customer(use_saved_street: true)` copying in code; redaction tests
   613	  asserting no saved street text appears in tool results, streamed events,
   614	  transcripts or logs.
   615	- **Browser end-to-end, not optional.** At least one test drives the real
   616	  page in a headless browser — types a message, waits for a rendered reply,
   617	  walks a full order to submission — asserting against the DOM, not the API.
   618	  `curl` proves the server works and proves nothing about the product; the
   619	  customer never talks to `curl`. Include three failure paths: a tool error, a
   620	  stream ending without a final message, the gateway unreachable — each must
   621	  leave a visible message on the page.
   622	- **The acceptance test is live**, opt-in via env flag, the only test that
   623	  touches the real API. Full conversation, submit, then read the pizzeria's
   624	  orders back — presence via `GET /pizzerias/{id}/orders`, customer, items
   625	  and quantities via `GET /pizzerias/{id}/orders/{order_id}` (the list
   626	  endpoint carries no items and cannot verify them) — and assert the four
   627	  points under *What done looks like*. If this fails, the product does not
   628	  work, whatever else is green.
   629	- **Offline speech E2E** with a stub speech service: exercise the real
   630	  browser UI path — speech-control visibility when speech is configured,
   631	  STT round-trip from recorded fixtures, `spoken: true` turn metadata,
   632	  and TTS fetched only for the final assistant message when the toggle is
   633	  enabled. These tests assert wiring, not transcription or synthesis
   634	  quality.
   635	- **Live voice acceptance test** (opt-in, like the live acceptance test):
   636	  send recorded spoken-order fixtures through the real speech service,
   637	  drive a full order through the web/API path, and verify the same
   638	  order-correctness criteria as *What done looks like* via the API. At
   639	  least one German and one English fixture. This is the release-gating
   640	  voice proof — a manual demo is a release-note aid, not the acceptance
   641	  artifact.
   642	- **Name-confirmation regression:** a transcript/fixture with a
   643	  plausible-but-wrong first name asserts that the agent reads back and
   644	  confirms the name before submission, preventing ghost-customer
   645	  creation.
   646	- **Speech, manual** (supplementary): dictate an order, a name that needs
   647	  correcting, a menu question — plus one run with `SPEECH_URL` unset,
   648	  which must render a usable text-only UI and place an order normally.
   649	
   650	---
   651	
   652	## Who builds this — and who judges it
   653	
   654	The build runs locally, on the operator's own subscriptions, with the most
   655	capable models available. Two roles take part and they are **not**
   656	interchangeable.
   657	
   658	| Role | Permission |
   659	|---|---|
   660	| Implementer — one coding agent | writes every file |
   661	| Reviewer / judge — a second, independent agent | read-only, never writes |
   662	
   663	Which products and models fill these roles is the operator's decision and is
   664	deliberately left out of this spec: tools are replaced long before the product
   665	is. The roles and the protocol are binding; the tooling is not.
   666	
   667	- **One implementer, and nothing else develops.** Every artefact in
   668	  *Deliverables* comes from it. No second implementer, no hand-patched fixes
   669	  between rounds.
   670	- **The reviewer never writes the code it judges.** Read-only, two roles in
   748	   verified fact never becomes a question again.
   749	1. **Core.** Order model, state machine, tool layer, tests. No LLM, no
   750	   network. Pass when the unit tests are green.
   751	2. **Agent loop.** Model, tools, system prompt, one turn end to end.
   752	3. **CLI.** Full conversation, real API, an order visible on the dashboard.
   753	4. **Web.** FastAPI on 8888, same core. Pass only when you have opened the
   754	   page in a browser, switched pizzeria, asked a price question, placed an
   755	   order through the page, and seen it on that pizzeria's dashboard — not
   756	   when the endpoint answers `curl`.
   757	5. **Speech.** Wire the speech service into the web UI, spoken-answer policy,
   758	   and the degraded no-speech path.
   759	6. **Harden.** Walk the error table, force each case, fix what breaks.
   760	
   761	After each pass, review your own work as the reviewer who has to reject it:
   762	what would a hostile reader find first? Fix that, then move on. Stop only when
   763	a full pass over the spec finds nothing left that you know how to improve.
   764	
   765	---
   766	
   767	## Deliverables
   768	
   769	```
   770	.

codex
SCORES (1-5 each, 5 = best):
completeness: 5
correctness: 4
error_handling: 4
simplicity: 4
spec_compliance: 5
TOTAL: 22/25
VERDICT: APPROVED
ISSUES: empty
tokens used
54,508
SCORES (1-5 each, 5 = best):
completeness: 5
correctness: 4
error_handling: 4
simplicity: 4
spec_compliance: 5
TOTAL: 22/25
VERDICT: APPROVED
ISSUES: empty
