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
session id: 019fc107-091a-7363-9bb5-50a8ebd2f2be
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


codex
Using `using-superpowers` first because the skill instructions require it at conversation start, then I’ll read the plan artifact, source spec, QA decisions, and the existing implementation surfaces the delta extends before scoring the revision.
exec
/bin/bash -lc "sed -n '1,220p' /home/rob/.agents/skills/using-superpowers/SKILL.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,220p' /home/rob/.agents/skills/requesting-code-review/SKILL.md" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 126ms:
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

 succeeded in 110ms:
---
name: requesting-code-review
description: Use when completing tasks, implementing major features, or before merging to verify work meets requirements
---

# Requesting Code Review

Dispatch a code reviewer subagent to catch issues before they cascade. The reviewer gets precisely crafted context for evaluation — never your session's history.

**Core principle:** Review early, review often.

## When to Request Review

**Mandatory:**
- After each task in subagent-driven development
- After completing major feature
- Before merge to main

**Optional but valuable:**
- When stuck (fresh perspective)
- Before refactoring (baseline check)
- After fixing complex bug

## How to Request

**1. Get git SHAs:**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

**2. Dispatch code reviewer subagent:**

Dispatch a `general-purpose` subagent, filling the template at [code-reviewer.md](code-reviewer.md)

**Placeholders:**
- `{DESCRIPTION}` - Brief summary of what you built
- `{PLAN_OR_REQUIREMENTS}` - What it should do
- `{BASE_SHA}` - Starting commit
- `{HEAD_SHA}` - Ending commit

**3. Act on feedback:**
- Fix Critical issues immediately
- Fix Important issues before proceeding
- Note Minor issues for later
- Push back if reviewer is wrong (with reasoning)

## Example

```
[Just completed Task 2: Add verification function]

You: Let me request code review before proceeding.

BASE_SHA=$(git log --oneline | grep "Task 1" | head -1 | awk '{print $1}')
HEAD_SHA=$(git rev-parse HEAD)

[Dispatch code reviewer subagent]
  DESCRIPTION: Added verifyIndex() and repairIndex() with 4 issue types
  PLAN_OR_REQUIREMENTS: Task 2 from docs/superpowers/plans/deployment-plan.md
  BASE_SHA: a7981ec
  HEAD_SHA: 3df7661

[Subagent returns]:
  Strengths: Clean architecture, real tests
  Issues:
    Important: Missing progress indicators
    Minor: Magic number (100) for reporting interval
  Assessment: Ready to proceed

You: [Fix progress indicators]
[Continue to Task 3]
```

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "I'll just review the diff myself instead of dispatching a reviewer" | You're the coordinator — reviewing the diff inline burns the context window you need to keep driving the work. Dispatch a reviewer subagent: the diff and the evaluation live in its context, and only the findings come back to you. |
| "The reviewer needs my whole session history to understand the change" | Hand it precisely crafted context, never your session's history. That keeps the reviewer on the work product, not your thought process. |

## Red Flags

**Never:**
- Skip review because "it's simple"
- Ignore Critical issues
- Proceed with unfixed Important issues
- Argue with valid technical feedback

**If reviewer wrong:**
- Push back with technical reasoning
- Show code/tests that prove it works
- Request clarification

See template at: [code-reviewer.md](code-reviewer.md)

codex
I’ve loaded the required process skill. Next I’m reading the Codex-specific instructions for that skill and the exact plan/spec/QA sections the judgment depends on, then I’ll check the current implementation surfaces for conflicts with the proposed delta.
exec
/bin/bash -lc 'rg -n "Delta Plan v3|customers endpoint|Tools table|saved-street|Speech|Testing additions|acceptance point 5|returning-customer|voice" PLAN.md SPEC.md decisions/qa.md' in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,220p' /home/rob/.agents/skills/references/codex-tools.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc 'git rev-parse HEAD && git log --oneline -n 5' in /home/rob/bpm-pizza-vibecoding-solution
 exited 2 in 184ms:
sed: can't read /home/rob/.agents/skills/references/codex-tools.md: No such file or directory

 succeeded in 199ms:
decisions/qa.md:56:## 2026-08-01 — Spec Future: voice becomes first-class (SPEC change only)
decisions/qa.md:58:**Q:** Operator: "a voice agent without voice is a bit stupid" — make voice
decisions/qa.md:60:(reviews/round21-voice-spec-discussion.md).
decisions/qa.md:67:browser context (HTTPS/domain) mandatory for the voice path — plain HTTP
decisions/qa.md:70:multi-second delays are a defect; new "Speech service provisioning"
decisions/qa.md:72:offline speech E2E via stub service (wiring only), opt-in live voice
SPEC.md:126:- **Speech on the web transport is a required channel capability in
SPEC.md:128:  described in *Speech*; if the service is unavailable at runtime,
SPEC.md:233:  silently creates a new customer — a misheard name creates a ghost. Speech
SPEC.md:270:- **The customers endpoint** `GET /pizzerias/{id}/customers` (auth:
SPEC.md:478:## Speech
SPEC.md:480:Speech is an input and an output method on the web channel, served by a
SPEC.md:487:| TTS | `POST {SPEECH_URL}/v1/audio/speech` | JSON: model, voice, input text → audio |
SPEC.md:496:- **The browser speech APIs are forbidden.** `SpeechRecognition` and
SPEC.md:501:  and voice come from the environment, exactly like the chat model; the
SPEC.md:512:- **Speech is a required product capability for release completeness.**
SPEC.md:528:- **Speech shortens answers, it does not change them.** Same core, same
SPEC.md:535:### Speech service provisioning
SPEC.md:565:| Speech service down | hide speech controls | text UI unaffected |
SPEC.md:635:- **Live voice acceptance test** (opt-in, like the live acceptance test):
SPEC.md:640:  voice proof — a manual demo is a release-note aid, not the acceptance
SPEC.md:646:- **Speech, manual** (supplementary): dictate an order, a name that needs
SPEC.md:757:5. **Speech.** Wire the speech service into the web UI, spoken-answer policy,
SPEC.md:793:│   ├── fixtures/audio/      ← recorded audio for offline + live voice tests
SPEC.md:818:| Speech | Self-hosted container, OpenAI-compatible HTTP; no vendor, no browser speech API |
PLAN.md:196:- Speech proxy endpoints move to `channels/speech.py` (deliverable):
PLAN.md:197:  `SpeechService` class (config, probe, stt(audio, lang), tts(text,
PLAN.md:200:**Speech behaviour (full SPEC coverage, not just the STT hint):**
PLAN.md:268:| Speech service down | probe fails → controls not rendered; per-call failure → notice, order untouched |
PLAN.md:322:- **Speech:** manual checklist (README) unchanged + STT language follows
PLAN.md:373:# Delta Plan v3 — Street lookup + Voice (SPEC rev d851966)
PLAN.md:376:> returning-customer street reuse (confirm-without-disclosure) and voice as
PLAN.md:447:  voice test (content = a spoken order).
PLAN.md:448:- `tests/stubs.py`: `StubSpeech` — `GET /v1/models` 200;
PLAN.md:455:- API level (app booted with `SPEECH_*` pointing at StubSpeech):
PLAN.md:469:  and only for the final assistant message (StubSpeech call counter);
PLAN.md:487:  voice-capable deployment>`: a real headless browser drives the real
PLAN.md:499:  voice-capable deployment.
PLAN.md:505:   real street ☐ no saved-street text in events, logs or
PLAN.md:509:3. StubSpeech + audio fixtures + API-level speech tests. ☐ stt round
PLAN.md:511:4. Browser E2E voice wiring (fake media device). ☐ mic/toggle visible
PLAN.md:515:6. deploy/ speech service definition + README voice section.
PLAN.md:517:7. Live voice acceptance test (opt-in) + docs. ☐ DE+EN fixtures ☐ skips

 succeeded in 172ms:
7c5b0c7e9ecf7e903b62a9ff65c7c51bf01fc4fb
7c5b0c7 Apply plan-gate round 1 findings to Delta Plan v3
d51bb93 PLAN v3 delta: street lookup + voice (pre-review)
d851966 SPEC Future: voice is a required release capability
53bab47 Archive SPEC (street-lookup rev) as SPEC_20260801_4.md before voice upgrade
53d8209 Add Procfile for Dokploy/Nixpacks deploy (PORT-aware uvicorn start)

codex
The plan revision is at `7c5b0c7`, and I’ve confirmed the relevant anchors in `SPEC.md`, `PLAN.md`, and `decisions/qa.md`. I’m reading those exact sections now, then I’ll inspect the current `core/`, `channels/`, and `tests/` behavior the delta is supposed to extend so I can judge contradictions rather than just wording.
exec
/bin/bash -lc "sed -n '1,220p' /home/rob/.agents/skills/using-superpowers/references/codex-tools.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '373,540p' PLAN.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '220,340p;478,575p;628,670p;748,765p;810,825p' SPEC.md" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 237ms:
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
  content the model reads must fail this test).
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
   ☐ push-to-talk round trip ☐ single final-message TTS fetch.
5. Name-confirmation regression transcript. ☐ corrected name only,
   after confirmation.
6. deploy/ speech service definition + README voice section.
   ☐ neutral (no vendor/model names) ☐ HTTPS requirement documented.
7. Live voice acceptance test (opt-in) + docs. ☐ DE+EN fixtures ☐ skips
   cleanly without SPEECH_URL ☐ full-order verification via API.

 succeeded in 237ms:
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

 succeeded in 243ms:
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
| Menu | Fetched live per session, no fallback list |
| Tenancy | Customer-selectable; `PIZZERIA_ID` preselects, never restricts; tenant in the URL path |
| Pizzeria selector | Filled from the API only; no fallback entry |
| Prices | Shown from the API; no payment, no invented figures |
| Totals | Computed in code from API prices; the model never does arithmetic |
| Saved addresses | Reusable after one explicit confirmation; the address text never reaches the model, the stream, the transcript or the logs |
| Language | Session language from `PIZZERIA_LANG`, switchable in the web header; per-turn mirroring wins for replies |
| Transports | One core, two channels (CLI, web), no logic in the channels |
| Speech | Self-hosted container, OpenAI-compatible HTTP; no vendor, no browser speech API |
| Voice | Required release capability on the web channel; text-only is degraded operation, not the product |
| Web UI | Pizzeria name, basket and connection state always visible; no message ends unanswered |
| Version | `x.y.z` in the footer, raised every release |
| Derived URLs | Dashboard and docs built from `PIZZASIM_URL`, never literal |
| Languages | DE + EN, mirrored per turn |
| Confirmation | Mandatory read-back tied to a basket revision |
| Parsing | The model parses. No regex order parser, ever. |

exec
/bin/bash -lc "sed -n '1,220p' decisions/qa.md" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 119ms:
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
The spec anchors are clear now. I’m checking the implemented v2 surfaces to see whether the revised delta plan still leaves exploitable ambiguity or conflicts with the current architecture, especially around redacted state serialization, confirm flow, and the existing web/E2E test shape.
exec
/bin/bash -lc 'rg -n "as_dict|submit_order|confirm_order|read_back|set_customer|lookup_customer|Customer|session.messages|snapshot|JSONL|spoken|speech|tts|stt|MediaRecorder|confirm" core channels tests' in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc 'rg --files core channels tests' in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 216ms:
channels/static/index.html:40:  <label id="tts-wrap" hidden>
channels/static/index.html:41:    <input type="checkbox" id="tts-toggle"> <span id="tts-label"></span>
channels/static/style.css:71:#tts-wrap { font-size: .8rem; color: #555; }
tests/test_web_e2e.py:71:    assert cfg["speech"] is False
tests/test_web_e2e.py:148:def test_confirm_endpoint_places_order_in_selected_tenant(stack, api):
tests/test_web_e2e.py:156:    snapshot = [e["result"]["snapshot"] for e in events
tests/test_web_e2e.py:158:                and e.get("tool") == "read_back"][-1]
tests/test_web_e2e.py:159:    events = stream_lines(api, "/confirm",
tests/test_web_e2e.py:161:                           "revision": snapshot["revision"]})
tests/test_web_e2e.py:164:                 and e.get("tool") == "submit_order"][-1]
tests/test_web_e2e.py:176:def test_confirm_stale_revision_streams_error(api):
tests/test_web_e2e.py:181:    events = stream_lines(api, "/confirm",
tests/test_web_e2e.py:227:    # speech disabled → controls not rendered
tests/test_web_e2e.py:229:    assert page.locator("#tts-wrap").is_hidden()
tests/test_web_e2e.py:343:def test_e2e_confirm_failure_offers_retry(page_factory, stack):
tests/test_web_e2e.py:344:    """A confirm whose phrasing turn yields no answer leaves a visible
tests/test_web_e2e.py:345:    notice with a retry that re-runs the SAME confirm action — and the
tests/test_web_e2e.py:366:    page.locator(".notice button").last.click()  # retry the confirm
tests/transcripts/unknown_item.json:17:       {"tool": "set_customer", "args": {"first_name": "Luca", "street_one": "via Milano 2"}},
tests/transcripts/unknown_item.json:18:       {"tool": "read_back", "args": {}},
tests/transcripts/unknown_item.json:23:       {"tool": "confirm_order", "args": {"revision": 2}},
tests/transcripts/unknown_item.json:24:       {"tool": "submit_order", "args": {}},
tests/transcripts/unknown_item.json:30:    "calls": ["add_items", "add_items", "set_customer", "read_back", "confirm_order", "submit_order"],
tests/transcripts/mind_change.json:2:  "name": "mind_change_after_read_back",
tests/transcripts/mind_change.json:8:       {"tool": "set_customer", "args": {"first_name": "Sara", "street_one": "via Napoli 9"}},
tests/transcripts/mind_change.json:9:       {"tool": "read_back", "args": {}},
tests/transcripts/mind_change.json:15:       {"tool": "confirm_order", "args": {"revision": 2}},
tests/transcripts/mind_change.json:16:       {"tool": "read_back", "args": {}},
tests/transcripts/mind_change.json:21:       {"tool": "confirm_order", "args": {"revision": 3}},
tests/transcripts/mind_change.json:22:       {"tool": "submit_order", "args": {}},
tests/transcripts/mind_change.json:28:    "calls": ["add_items", "set_customer", "read_back", "add_items", "confirm_order", "read_back", "confirm_order", "submit_order"],
tests/transcripts/submit_timeout.json:8:       {"tool": "set_customer", "args": {"first_name": "Nino", "street_one": "via Genova 1"}},
tests/transcripts/submit_timeout.json:9:       {"tool": "read_back", "args": {}},
tests/transcripts/submit_timeout.json:14:       {"tool": "confirm_order", "args": {"revision": 2}},
tests/transcripts/submit_timeout.json:15:       {"tool": "submit_order", "args": {}},
tests/transcripts/submit_timeout.json:20:       {"tool": "submit_order", "args": {}},
tests/transcripts/submit_timeout.json:26:    "calls": ["add_items", "set_customer", "read_back", "confirm_order", "submit_order", "submit_order"],
tests/transcripts/happy_path.json:17:       {"tool": "set_customer", "args": {"first_name": "Marco", "street_one": "via Roma 5"}},
tests/transcripts/happy_path.json:18:       {"tool": "read_back", "args": {}},
tests/transcripts/happy_path.json:23:       {"tool": "confirm_order", "args": {"revision": 2}},
tests/transcripts/happy_path.json:24:       {"tool": "submit_order", "args": {}},
tests/transcripts/happy_path.json:30:    "calls": ["get_menu", "add_items", "set_customer", "read_back", "confirm_order", "submit_order"],
tests/transcripts/correction.json:17:       {"tool": "set_customer", "args": {"first_name": "Anna"}},
tests/transcripts/correction.json:18:       {"tool": "read_back", "args": {}},
tests/transcripts/correction.json:23:       {"tool": "confirm_order", "args": {"revision": 3}},
tests/transcripts/correction.json:24:       {"tool": "submit_order", "args": {}},
tests/transcripts/correction.json:30:    "calls": ["add_items", "add_items", "set_customer", "read_back", "confirm_order", "submit_order"],
tests/test_transcripts.py:52:    def submit_order(self, customer, items):
tests/test_tools.py:14:from core.order import Customer, Order, State
tests/test_tools.py:98:        ).submit_order({"first_name": "X"}, [])
tests/test_tools.py:127:    result = client.submit_order({"first_name": "Marco"}, [])
tests/test_tools.py:150:    snap = order.snapshot()
tests/test_tools.py:162:    snap = order.snapshot()
tests/test_tools.py:180:    def submit_order(self, customer, items):
tests/test_tools.py:209:    tools.dispatch(order, menu, fake, "set_customer",
tests/test_tools.py:214:def confirmed_order(menu, fake):
tests/test_tools.py:216:    tools.dispatch(order, menu, fake, "read_back", {})
tests/test_tools.py:217:    tools.dispatch(order, menu, fake, "confirm_order",
tests/test_tools.py:223:def test_every_success_carries_full_snapshot(menu, fake):
tests/test_tools.py:226:    assert result["snapshot"]["state"] == "EMPTY"
tests/test_tools.py:231:    snap = result["snapshot"]
tests/test_tools.py:234:    assert snap["customer"] is None and snap["read_back_done"] is False
tests/test_tools.py:282:    assert result["snapshot"]["items"][0]["qty"] == 1
tests/test_tools.py:285:    assert result["snapshot"]["items"] == []
tests/test_tools.py:286:    assert result["snapshot"]["state"] == "EMPTY"
tests/test_tools.py:290:    order = confirmed_order(menu, fake)
tests/test_tools.py:291:    result = tools.dispatch(order, menu, fake, "submit_order", {})
tests/test_tools.py:295:    assert result["snapshot"]["state"] == "SUBMITTED"
tests/test_tools.py:298:def test_submit_outside_confirmed_is_tool_error(menu, fake):
tests/test_tools.py:299:    """Invariant 1: no helpful auto-confirmation."""
tests/test_tools.py:301:    result = tools.dispatch(order, menu, fake, "submit_order", {})
tests/test_tools.py:307:    result = tools.dispatch(Order(), menu, fake, "submit_order", {})
tests/test_tools.py:313:    order = confirmed_order(menu, fake)
tests/test_tools.py:315:    result = tools.dispatch(order, menu, fake, "submit_order", {})
tests/test_tools.py:330:    result = tools.dispatch(order, menu, fake, "submit_order", {})
tests/test_tools.py:339:    order = confirmed_order(menu, fake)
tests/test_tools.py:341:    tools.dispatch(order, menu, fake, "submit_order", {})
tests/test_tools.py:352:    result = tools.dispatch(order, menu, fake, "submit_order", {})
tests/test_tools.py:358:    """Timeout, then the customer changes the basket and reconfirms: the
tests/test_tools.py:361:    order = confirmed_order(menu, fake)
tests/test_tools.py:363:    tools.dispatch(order, menu, fake, "submit_order", {})
tests/test_tools.py:371:    tools.dispatch(order, menu, fake, "read_back", {})
tests/test_tools.py:372:    tools.dispatch(order, menu, fake, "confirm_order",
tests/test_tools.py:380:    result = tools.dispatch(order, menu, fake, "submit_order", {})
tests/test_tools.py:386:    order = confirmed_order(menu, fake)
tests/test_tools.py:388:    result = tools.dispatch(order, menu, fake, "submit_order", {})
tests/test_tools.py:395:    result = tools.dispatch(order, menu, fake, "submit_order", {})
tests/test_tools.py:396:    assert result["snapshot"]["state"] == "SUBMITTED"
tests/test_tools.py:401:    order = confirmed_order(menu, fake)
tests/test_tools.py:403:    tools.dispatch(order, menu, fake, "submit_order", {})
tests/test_tools.py:405:    result = tools.dispatch(order, menu, fake, "submit_order", {})
tests/test_tools.py:411:    order = confirmed_order(menu, fake)
tests/test_tools.py:414:    result = tools.dispatch(order, menu, fake, "submit_order", {})
tests/test_tools.py:421:    order = confirmed_order(menu, fake)
tests/test_tools.py:423:    result = tools.dispatch(order, menu, fake, "submit_order", {})
tests/test_tools.py:433:    tools.dispatch(order, menu, fake, "set_customer",
tests/test_tools.py:435:    tools.dispatch(order, menu, fake, "read_back", {})
tests/test_tools.py:436:    tools.dispatch(order, menu, fake, "confirm_order",
tests/test_tools.py:443:    real_submit = fake.submit_order
tests/test_tools.py:448:    fake.submit_order = spy
tests/test_tools.py:449:    tools.dispatch(order, menu, fake, "submit_order", {})
tests/test_tools.py:456:    assert result["deliverable"] is True and "snapshot" in result
tests/test_tools.py:459:# --- session factory, language, confirm path (tickets 2-4) ----------------
tests/test_tools.py:506:    assert "Pizzeria Default" in session.messages[0]["content"]
tests/test_tools.py:523:    history_before = len(session.messages)
tests/test_tools.py:524:    german = session.messages[0]["content"]
tests/test_tools.py:527:    assert session.messages[0]["content"] != german
tests/test_tools.py:528:    assert "Pizzeria Default" in session.messages[0]["content"]
tests/test_tools.py:529:    assert len(session.messages) == history_before  # history preserved
tests/test_tools.py:541:def test_spoken_note_is_ephemeral_per_turn():
tests/test_tools.py:542:    """The spoken-style note reaches the model for the spoken turn only —
tests/test_tools.py:552:    agent.run_turn(session, "hallo", spoken=True)
tests/test_tools.py:560:                   for m in session.messages)  # never persisted
tests/test_tools.py:563:def confirm_ready_session(chat_fn):
tests/test_tools.py:569:    tools.dispatch(session.order, session.menu, fake, "set_customer",
tests/test_tools.py:571:    tools.dispatch(session.order, session.menu, fake, "read_back", {})
tests/test_tools.py:575:def test_confirm_and_submit_happy_path():
tests/test_tools.py:578:    session, agent = confirm_ready_session(phrase)
tests/test_tools.py:580:    text = agent.confirm_and_submit(session, session.order.revision,
tests/test_tools.py:585:    assert tool_names == ["confirm_order", "submit_order"]
tests/test_tools.py:587:    roles = [m["role"] for m in session.messages]
tests/test_tools.py:589:    assert session.messages[-1]["role"] == "assistant"
tests/test_tools.py:592:def test_confirm_with_stale_revision_submits_nothing():
tests/test_tools.py:595:    session, agent = confirm_ready_session(phrase)
tests/test_tools.py:601:    agent.confirm_and_submit(session, stale, events.append)
tests/test_tools.py:608:    assert session.messages[-2]["role"] == "tool"
tests/test_tools.py:611:def test_confirm_gateway_death_still_answers():
tests/test_tools.py:612:    """Answer-or-rendered-error invariant on /confirm: dispatches applied,
tests/test_tools.py:616:    session, agent = confirm_ready_session(dead)
tests/test_tools.py:618:    text = agent.confirm_and_submit(session, session.order.revision,
tests/test_tools.py:651:        ("set_customer", {"first_name": "Akzeptanz",
tests/test_tools.py:653:        ("read_back", {}),
tests/test_tools.py:657:    result = tools.dispatch(order, menu, client, "confirm_order",
tests/test_tools.py:660:    result = tools.dispatch(order, menu, client, "submit_order", {})
channels/speech.py:5:the session language — there is no separate speech-language config.
channels/speech.py:26:        self.stt_model = optional_env("SPEECH_STT_MODEL")
channels/speech.py:27:        self.tts_model = optional_env("SPEECH_TTS_MODEL")
channels/speech.py:30:        if self.url and self.stt_model and self.tts_model and self.voice:
channels/speech.py:36:                print("speech service not answering — text-only mode",
channels/speech.py:39:    def stt(self, audio: bytes, filename: str, content_type: str,
channels/speech.py:45:                data={"model": self.stt_model, "language": lang},
channels/speech.py:52:    def tts(self, text: str, lang: str) -> tuple[bytes, str]:
channels/speech.py:55:                f"{self.url}/v1/audio/speech",
channels/speech.py:56:                json={"model": self.tts_model, "voice": self.voice,
tests/test_state.py:6:from core.order import Customer, Item, Order, State
tests/test_state.py:22:    state.set_customer(o, Customer("Marco", "via Roma"))
tests/test_state.py:25:    state.read_back(o)
tests/test_state.py:26:    state.confirm(o, o.revision)
tests/test_state.py:46:    state.set_customer(o, Customer("Marco", "via Roma"))
tests/test_state.py:48:    state.read_back(o)
tests/test_state.py:49:    state.confirm(o, o.revision)
tests/test_state.py:60:    state.set_customer(o, Customer("Anna"))
tests/test_state.py:71:    lambda o: state.set_customer(o, Customer("Eve")),
tests/test_state.py:72:    lambda o: state.read_back(o),
tests/test_state.py:73:    lambda o: state.confirm(o, o.revision),
tests/test_state.py:89:def test_read_back_empty():
tests/test_state.py:91:        state.read_back(order_in(State.EMPTY))
tests/test_state.py:95:def test_read_back_collecting_needs_customer():
tests/test_state.py:97:        state.read_back(order_in(State.COLLECTING))
tests/test_state.py:102:def test_confirm_illegal_states(st):
tests/test_state.py:105:        state.confirm(o, o.revision)
tests/test_state.py:109:def test_confirm_when_already_confirmed():
tests/test_state.py:112:        state.confirm(o, o.revision)
tests/test_state.py:117:def test_submit_outside_confirmed(st):
tests/test_state.py:134:def test_add_after_confirmed_demotes_to_ready():
tests/test_state.py:140:def test_remove_after_confirmed_demotes():
tests/test_state.py:146:def test_set_customer_after_confirmed_demotes():
tests/test_state.py:148:    state.set_customer(o, Customer("Mario"))
tests/test_state.py:152:def test_confirmation_does_not_survive_demotion():
tests/test_state.py:153:    """A confirmation applies to the basket that was read back."""
tests/test_state.py:160:# --- invariant 3: confirm tied to read-back + revision --------------------
tests/test_state.py:162:def test_confirm_without_read_back():
tests/test_state.py:165:        state.confirm(o, o.revision)
tests/test_state.py:166:    assert e.value.code == "read_back_required"
tests/test_state.py:169:def test_confirm_with_stale_revision():
tests/test_state.py:171:    state.read_back(o)
tests/test_state.py:175:        state.confirm(o, stale)
tests/test_state.py:179:def test_read_back_of_old_revision_does_not_allow_confirm():
tests/test_state.py:181:    state.read_back(o)
tests/test_state.py:184:        state.confirm(o, o.revision)
tests/test_state.py:185:    assert e.value.code == "read_back_required"
tests/test_state.py:194:    state.set_customer(o, Customer("A"))
channels/static/app.js:3:   Speech: browser captures/plays audio only (MediaRecorder + <audio>);
channels/static/app.js:4:   recognition/synthesis happen server-side. No browser speech APIs. */
channels/static/app.js:26:    confirm: "Bestellung bestätigen",
channels/static/app.js:29:    ttsLabel: "Antworten vorlesen",
channels/static/app.js:30:    sttFail: "Spracherkennung gerade nicht erreichbar — bitte tippen.",
channels/static/app.js:31:    sttEmpty: "Ich habe nichts verstanden — bitte noch einmal.",
channels/static/app.js:32:    ttsFail: "Vorlesen gerade nicht möglich.",
channels/static/app.js:53:    confirm: "Confirm order",
channels/static/app.js:56:    ttsLabel: "Read replies aloud",
channels/static/app.js:57:    sttFail: "Speech recognition unavailable — please type.",
channels/static/app.js:58:    sttEmpty: "I didn't catch that — please try again.",
channels/static/app.js:59:    ttsFail: "Read-aloud is unavailable right now.",
channels/static/app.js:81:  $("tts-label").textContent = t("ttsLabel");
channels/static/app.js:98:     failed action (e.g. a confirm with its revision). */
channels/static/app.js:121:function renderBasket(snapshot) {
channels/static/app.js:125:  for (const item of snapshot.items) {
channels/static/app.js:142:  totalValue.textContent = euro(snapshot.basket_total);
channels/static/app.js:145:  const submitted = snapshot.state === "SUBMITTED";
channels/static/app.js:155:/* ---------- read-back + confirm ---------------------------------------- */
channels/static/app.js:163:function showReadback(snapshot) {
channels/static/app.js:167:  const list = snapshot.items
channels/static/app.js:170:  const who = snapshot.customer
channels/static/app.js:171:    ? `${snapshot.customer.first_name}` +
channels/static/app.js:172:      (snapshot.customer.street_one
channels/static/app.js:173:        ? `, ${snapshot.customer.street_one}` : "")
channels/static/app.js:176:    `${who}\n${list}\n${t("total")}: ${euro(snapshot.basket_total)}`;
channels/static/app.js:178:  btn.textContent = t("confirm");
channels/static/app.js:179:  btn.onclick = () => { btn.disabled = true; confirmOrder(snapshot.revision); };
channels/static/app.js:214:          if (ev.result.snapshot) {
channels/static/app.js:215:            renderBasket(ev.result.snapshot);
channels/static/app.js:216:            if (ev.tool === "read_back") showReadback(ev.result.snapshot);
channels/static/app.js:258:      // A chat message stays recoverable via resend; a pending confirm is
channels/static/app.js:284:async function sendTurn(text, spoken = false) {
channels/static/app.js:287:    "/chat", { session_id: session.id, text, spoken }, text ?? undefined);
channels/static/app.js:288:  if (finalText && cfg.speech && $("tts-toggle").checked) speak(finalText);
channels/static/app.js:291:async function confirmOrder(revision) {
channels/static/app.js:292:  // The retry re-runs the confirm with the SAME revision: if the first
channels/static/app.js:296:    "/confirm", { session_id: session.id, revision },
channels/static/app.js:297:    () => confirmOrder(revision));
channels/static/app.js:298:  if (finalText && cfg.speech && $("tts-toggle").checked) speak(finalText);
channels/static/app.js:327:  const speechUsable = cfg.speech;
channels/static/app.js:328:  $("tts-wrap").hidden = !speechUsable;
channels/static/app.js:329:  $("mic").hidden = !(speechUsable && navigator.mediaDevices &&
channels/static/app.js:330:                      window.MediaRecorder);
channels/static/app.js:364:/* ---------- speech (capture/playback only) ------------------------------ */
channels/static/app.js:370:  recorder = new MediaRecorder(stream);
channels/static/app.js:379:    body.append("audio", blob, "speech.webm");
channels/static/app.js:382:        `/speech/stt?session_id=${session.id}`, { method: "POST", body });
channels/static/app.js:386:      else notice(t("sttEmpty"));
channels/static/app.js:388:      notice(t("sttFail"));
channels/static/app.js:403:    const res = await fetch("/speech/tts", {
channels/static/app.js:411:    notice(t("ttsFail"));
tests/stubs.py:139:        if name == "set_customer":
tests/stubs.py:140:            return _tool_call("read_back", {})
tests/stubs.py:141:        if name == "read_back":
tests/stubs.py:144:        if name == "submit_order":
tests/stubs.py:147:        if name == "confirm_order":
tests/stubs.py:148:            return _tool_call("submit_order", {})
tests/stubs.py:164:        return _tool_call("set_customer", {"first_name": "Eva"})
channels/web.py:4:Contract (PLAN v2): /config, /session, /chat, /confirm, /language,
channels/web.py:5:/health, speech proxies, static UI. Turns are serialized per session;
channels/web.py:26:from channels.speech import SpeechService, SpeechUnavailable
channels/web.py:77:    app.state.speech = SpeechService()
channels/web.py:96:        "speech": app.state.speech.enabled,
channels/web.py:154:            events.put({"type": "done", "state": session.order.snapshot()})
channels/web.py:173:    spoken = bool(body.get("spoken"))
channels/web.py:177:                                              spoken=spoken),
channels/web.py:181:@app.post("/confirm")
channels/web.py:182:async def confirm(body: dict):
channels/web.py:183:    """The explicit confirm control: the transport forwards two
channels/web.py:191:        lambda emit: app.state.agent.confirm_and_submit(session, revision,
channels/web.py:206:def _speech() -> SpeechService:
channels/web.py:207:    if not app.state.speech.enabled:
channels/web.py:208:        raise HTTPException(404, "speech is not available")
channels/web.py:209:    return app.state.speech
channels/web.py:212:@app.post("/speech/stt")
channels/web.py:213:async def stt(audio: UploadFile, session_id: str = ""):
channels/web.py:214:    speech = _speech()
channels/web.py:217:        text = speech.stt(await audio.read(),
channels/web.py:222:        raise HTTPException(502, "speech service unavailable")
channels/web.py:226:@app.post("/speech/tts")
channels/web.py:227:async def tts(body: dict):
channels/web.py:228:    speech = _speech()
channels/web.py:234:        audio, content_type = speech.tts(text, session.lang)
channels/web.py:236:        raise HTTPException(502, "speech service unavailable")
core/pizzasim.py:153:    def submit_order(self, customer: dict, items: list[dict]) -> dict:
core/tools.py:3:Success results always embed the full state snapshot; failures are
core/tools.py:12:from .order import Customer, Item, Order
core/tools.py:56:    {"name": "set_customer",
core/tools.py:64:    {"name": "read_back",
core/tools.py:66:                    "the customer before asking for confirmation.",
core/tools.py:68:    {"name": "confirm_order",
core/tools.py:75:    {"name": "submit_order",
core/tools.py:76:     "description": "Send the confirmed order to the kitchen. Only legal "
core/tools.py:77:                    "after confirm_order.",
core/tools.py:133:        return {"menu": menu.as_tool_result(), "snapshot": order.snapshot()}
core/tools.py:153:        return {"snapshot": order.snapshot()}
core/tools.py:159:        return {"snapshot": order.snapshot()}
core/tools.py:161:    if name == "set_customer":
core/tools.py:165:        customer = Customer(first_name, args.get("street_one") or None)
core/tools.py:166:        state.set_customer(order, customer)
core/tools.py:167:        return {"customer": customer.as_dict(),
core/tools.py:168:                "snapshot": order.snapshot()}
core/tools.py:170:    if name == "read_back":
core/tools.py:171:        state.read_back(order)
core/tools.py:172:        return {"snapshot": order.snapshot()}
core/tools.py:174:    if name == "confirm_order":
core/tools.py:179:        state.confirm(order, revision)
core/tools.py:180:        return {"snapshot": order.snapshot()}
core/tools.py:182:    if name == "submit_order":
core/tools.py:189:                "snapshot": order.snapshot()}
core/tools.py:240:                return {**order.result, "snapshot": order.snapshot()}
core/tools.py:243:    customer = order.customer.as_dict()
core/tools.py:249:        result = client.submit_order(customer, items)
core/tools.py:266:    return {**order.result, "snapshot": order.snapshot()}
core/order.py:28:    # Copied from the session menu snapshot at add time; totals are
core/order.py:40:class Customer:
core/order.py:44:    def as_dict(self) -> dict:
core/order.py:51:    customer: Customer | None = None
core/order.py:53:    read_back_revision: int | None = None
core/order.py:59:    def snapshot(self) -> dict:
core/order.py:80:            "customer": self.customer.as_dict() if self.customer else None,
core/order.py:81:            "read_back_done": self.read_back_revision == self.revision,
core/menu.py:1:"""Immutable menu snapshot: (type, code) validation, extras validation,
core/menu.py:2:candidate suggestions. One snapshot per session (SPEC invariant 5)."""
core/state.py:10:from .order import Customer, Item, Order, State
core/state.py:33:    # recovery correlation belongs to the basket that was confirmed then,
core/state.py:61:    the most recently added matching line is reduced. The full snapshot in
core/state.py:83:def set_customer(order: Order, customer: Customer) -> None:
core/state.py:89:def read_back(order: Order) -> None:
core/state.py:100:    order.read_back_revision = order.revision
core/state.py:103:def confirm(order: Order, revision: int) -> None:
core/state.py:108:                "invalid_state", "The order is already confirmed."
core/state.py:112:            "The order isn't complete yet, so it can't be confirmed.",
core/state.py:120:    if order.read_back_revision != order.revision:
core/state.py:122:            "read_back_required",
core/state.py:135:            "The order hasn't been confirmed yet."
core/agent.py:2:JSONL event logging. The model only speaks; the order lives in core.
core/agent.py:38:    "en": "This reply will be spoken aloud: name at most three dishes, "
core/agent.py:77:    """One conversation: one Order, one immutable Menu snapshot, one
core/agent.py:96:    immutable menu snapshot, renders the prompt. Raises NotFoundError for
core/agent.py:128:    session.messages[0] = {
core/agent.py:150:        # call from any session (/chat and /confirm share this path).
core/agent.py:183:                 emit=lambda event: None, spoken: bool = False) -> str:
core/agent.py:185:        intermediate step goes to emit() and the JSONL log. user_text None
core/agent.py:193:            session.messages.append({"role": "user", "content": user_text})
core/agent.py:195:        # Ephemeral per-turn note: activates the spoken-style policy that
core/agent.py:197:        # not inherit the spoken constraints.
core/agent.py:199:                 if spoken else [])
core/agent.py:203:                message = self._chat_fn(session.messages + extra,
core/agent.py:208:                session.messages.append({"role": "assistant",
core/agent.py:216:                session.messages.append({"role": "assistant",
core/agent.py:221:            session.messages.append({
core/agent.py:240:                session.messages.append({
core/agent.py:248:        session.messages.append({"role": "assistant", "content": apology})
core/agent.py:258:        session.messages.append({
core/agent.py:270:        session.messages.append({
core/agent.py:277:    def confirm_and_submit(self, session: Session, revision: int,
core/agent.py:279:        """The explicit confirm control (SPEC: confirmation is an action
core/agent.py:281:        failure; CONFIRMED stays reachable only via confirm_order."""
core/agent.py:288:            session, "confirm_order", {"revision": revision}, event)
core/agent.py:290:            self._synthetic_call(session, "submit_order", {}, event)

 succeeded in 242ms:
tests/test_web_e2e.py
tests/__init__.py
tests/stubs.py
tests/test_tools.py
tests/test_state.py
tests/test_transcripts.py
tests/fixtures/pizzerias.json
tests/fixtures/orders_list.json
tests/fixtures/order_created.json
tests/fixtures/menu.json
core/pizzasim.py
core/menu.py
core/__init__.py
core/state.py
core/order.py
core/agent.py
core/tools.py
tests/fixtures/location.json
tests/fixtures/error_422.json
channels/web.py
channels/cli.py
channels/__init__.py
channels/speech.py
channels/static/index.html
channels/static/style.css
channels/static/app.js
tests/transcripts/submit_timeout.json
tests/transcripts/happy_path.json
tests/transcripts/correction.json
tests/transcripts/mind_change.json
tests/transcripts/unknown_item.json

codex
I’ve confirmed the existing code already has speech proxies/UI skeleton and a snapshot-driven event/logging path, which makes redaction and voice-proof details easy to get subtly wrong. I’m reading the specific serializer, agent logging, and web speech code now to see whether the plan closes those gaps tightly enough.
exec
/bin/bash -lc "sed -n '1,140p' core/order.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '180,320p' core/agent.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '150,320p' core/tools.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '150,430p' channels/static/app.js" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,280p' channels/speech.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '140,260p' tests/test_web_e2e.py" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 841ms:
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

 succeeded in 1033ms:
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

 succeeded in 991ms:
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

 succeeded in 889ms:
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

 succeeded in 916ms:
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

 succeeded in 981ms:
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

codex
I’ve narrowed this to a couple of remaining plan-level risks rather than broad coverage problems. I’m pulling numbered excerpts now so the verdict can point to concrete gaps in the revised `Delta Plan v3` instead of speaking generally.
exec
/bin/bash -lc "nl -ba SPEC.md | sed -n '268,305p;478,570p;632,650p;752,760p;815,823p'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "nl -ba channels/static/app.js | sed -n '163,176p;284,330p;364,412p'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "nl -ba PLAN.md | sed -n '373,530p'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "nl -ba channels/speech.py | sed -n '1,120p'" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 195ms:
   268	- **Item codes are unique per type, not globally** — `tonno` exists as a
   269	  pizza and a pasta. Validation and removal always key on `(type, code)`.
   270	- **The customers endpoint** `GET /pizzerias/{id}/customers` (auth:
   271	  `X-API-Key`) returns `customers[]` with `{id, first_name, street_one,
   272	  street_two, created_at, deleted_at}`. Since customers are unique per
   273	  pizzeria by `first_name`, a first name resolves to at most one saved
   274	  address. Guardrail: the verified order-write contract proves only
   275	  `street_one`, so address reuse is limited to `street_one` until
   276	  `street_two` support on `POST /orders` is verified as well.
   277	
   278	### Open contract questions — shrink-only
   279	
   280	Resolve against the live API before the affected component is implemented,
   281	then move the answer up into the facts and delete the question. Never guess.
   282	A verified fact never returns here.
   283	
   284	*(empty — all previous questions were resolved against the live API and
   285	moved into the facts above)*
   286	
   287	---
   288	
   289	## Order state machine
   290	
   291	```
   292	EMPTY ──add_items──▶ COLLECTING ──set_customer──▶ READY
   293	  ▲                      │  ▲                       │
   294	  └──remove last item────┘  └───add/remove/edit─────┘
   295	                                                    │ read_back + customer says yes
   296	                                                    ▼
   297	                                               CONFIRMED ──submit_order──▶ SUBMITTED
   298	                                                    │
   299	                                                    └──any change──▶ back to READY
   300	```
   301	
   302	Invariants, all enforced in code and all covered by unit tests:
   303	
   304	1. `submit_order` outside `CONFIRMED` returns an error. It does not
   305	   "helpfully" confirm on the model's behalf.
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
   752	3. **CLI.** Full conversation, real API, an order visible on the dashboard.
   753	4. **Web.** FastAPI on 8888, same core. Pass only when you have opened the
   754	   page in a browser, switched pizzeria, asked a price question, placed an
   755	   order through the page, and seen it on that pizzeria's dashboard — not
   756	   when the endpoint answers `curl`.
   757	5. **Speech.** Wire the speech service into the web UI, spoken-answer policy,
   758	   and the degraded no-speech path.
   759	6. **Harden.** Walk the error table, force each case, fix what breaks.
   760	
   815	| Saved addresses | Reusable after one explicit confirmation; the address text never reaches the model, the stream, the transcript or the logs |
   816	| Language | Session language from `PIZZERIA_LANG`, switchable in the web header; per-turn mirroring wins for replies |
   817	| Transports | One core, two channels (CLI, web), no logic in the channels |
   818	| Speech | Self-hosted container, OpenAI-compatible HTTP; no vendor, no browser speech API |
   819	| Voice | Required release capability on the web channel; text-only is degraded operation, not the product |
   820	| Web UI | Pizzeria name, basket and connection state always visible; no message ends unanswered |
   821	| Version | `x.y.z` in the footer, raised every release |
   822	| Derived URLs | Dashboard and docs built from `PIZZASIM_URL`, never literal |
   823	| Languages | DE + EN, mirrored per turn |

 succeeded in 217ms:
   163	function showReadback(snapshot) {
   164	  disableConfirm();
   165	  const panel = document.createElement("div");
   166	  panel.className = "readback";
   167	  const list = snapshot.items
   168	    .map((i) => `${i.qty}× ${i.name} — ${euro(i.line_total)}`)
   169	    .join("\n");
   170	  const who = snapshot.customer
   171	    ? `${snapshot.customer.first_name}` +
   172	      (snapshot.customer.street_one
   173	        ? `, ${snapshot.customer.street_one}` : "")
   174	    : "";
   175	  panel.textContent =
   176	    `${who}\n${list}\n${t("total")}: ${euro(snapshot.basket_total)}`;
   284	async function sendTurn(text, spoken = false) {
   285	  if (text !== null) addMsg("user", text);
   286	  const finalText = await streamPost(
   287	    "/chat", { session_id: session.id, text, spoken }, text ?? undefined);
   288	  if (finalText && cfg.speech && $("tts-toggle").checked) speak(finalText);
   289	}
   290	
   291	async function confirmOrder(revision) {
   292	  // The retry re-runs the confirm with the SAME revision: if the first
   293	  // attempt actually went through, the state machine refuses it and the
   294	  // agent says so — never a second order.
   295	  const finalText = await streamPost(
   296	    "/confirm", { session_id: session.id, revision },
   297	    () => confirmOrder(revision));
   298	  if (finalText && cfg.speech && $("tts-toggle").checked) speak(finalText);
   299	}
   300	
   301	/* ---------- sessions / tenancy ----------------------------------------- */
   302	
   303	function fillSelector() {
   304	  const select = $("pizzeria-select");
   305	  if (!cfg.pizzerias) {
   306	    select.hidden = true;
   307	    $("list-unavailable").hidden = false;
   308	    return;
   309	  }
   310	  select.hidden = false;
   311	  $("list-unavailable").hidden = true;
   312	  select.textContent = "";
   313	  for (const p of cfg.pizzerias) {
   314	    const opt = document.createElement("option");
   315	    opt.value = p.id;
   316	    opt.textContent = `${p.name} (${p.id.slice(0, 8)})`;
   317	    select.appendChild(opt);
   318	  }
   319	  if (session) select.value = session.pizzeriaId;
   320	}
   321	
   322	async function refreshConfig() {
   323	  cfg = await (await fetch("/config")).json();
   324	  $("version").textContent = "v" + cfg.version;
   325	  $("docs-link").href = cfg.docs_url;
   326	  fillSelector();
   327	  const speechUsable = cfg.speech;
   328	  $("tts-wrap").hidden = !speechUsable;
   329	  $("mic").hidden = !(speechUsable && navigator.mediaDevices &&
   330	                      window.MediaRecorder);
   364	/* ---------- speech (capture/playback only) ------------------------------ */
   365	
   366	let recorder = null;
   367	
   368	async function startRecording() {
   369	  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
   370	  recorder = new MediaRecorder(stream);
   371	  const chunks = [];
   372	  recorder.ondataavailable = (e) => chunks.push(e.data);
   373	  recorder.onstop = async () => {
   374	    stream.getTracks().forEach((tr) => tr.stop());
   375	    $("mic").classList.remove("recording");
   376	    $("mic").setAttribute("aria-pressed", "false");
   377	    const blob = new Blob(chunks, { type: recorder.mimeType });
   378	    const body = new FormData();
   379	    body.append("audio", blob, "speech.webm");
   380	    try {
   381	      const res = await fetch(
   382	        `/speech/stt?session_id=${session.id}`, { method: "POST", body });
   383	      if (!res.ok) throw new Error();
   384	      const { text } = await res.json();
   385	      if (text.trim()) sendTurn(text.trim(), true);
   386	      else notice(t("sttEmpty"));
   387	    } catch {
   388	      notice(t("sttFail"));
   389	    }
   390	  };
   391	  recorder.start();
   392	  $("mic").classList.add("recording");
   393	  $("mic").setAttribute("aria-pressed", "true");
   394	}
   395	
   396	$("mic").addEventListener("click", () => {
   397	  if (recorder && recorder.state === "recording") recorder.stop();
   398	  else startRecording().catch(() => notice(t("micDenied")));
   399	});
   400	
   401	async function speak(text) {
   402	  try {
   403	    const res = await fetch("/speech/tts", {
   404	      method: "POST",
   405	      headers: { "Content-Type": "application/json" },
   406	      body: JSON.stringify({ session_id: session.id, text }),
   407	    });
   408	    if (!res.ok) throw new Error();
   409	    new Audio(URL.createObjectURL(await res.blob())).play();
   410	  } catch {
   411	    notice(t("ttsFail"));
   412	  }

 succeeded in 209ms:
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
   427	  content the model reads must fail this test).
   428	- Mutual exclusion + `no_saved_street` paths.
   429	- Two new golden transcripts: saved-address reuse (lookup → confirm
   430	  question → flag-based set_customer → order) and decline/fallback
   431	  (customer says no → street asked, dictated street echoed as before).
   432	
   433	## B. Voice (SPEC: required capability; offline wiring tests + live proof)
   434	
   435	Artifacts:
   436	
   437	- `deploy/speech-service.compose.yml`: neutral, CPU-only service
   438	  definition — image and models come from environment placeholders
   439	  (`SPEECH_IMAGE`, `SPEECH_*`), no vendor or model names in the file, and
   440	  a comment pointing at the OpenAI-compatible surface it must expose.
   441	  README gains a "Voice deployment" section: HTTPS/domain requirement
   442	  (secure context), co-deployment with the app, env wiring.
   443	- `tests/fixtures/audio/`: generated spoken fixtures (offline synthesis
   444	  on the build host if a synthesizer is available, otherwise minimal
   445	  valid WAV containers) — `order.de.wav`, `order.en.wav`; used by the
   446	  offline round-trip (content irrelevant to the stub) and by the live
   447	  voice test (content = a spoken order).
   448	- `tests/stubs.py`: `StubSpeech` — `GET /v1/models` 200;
   449	  `POST /v1/audio/transcriptions` → fixed transcript (per stub script,
   450	  e.g. "Zwei Margherita bitte"), records the language field it received;
   451	  `POST /v1/audio/speech` → tiny valid audio bytes, counts calls.
   452	
   453	Offline tests:
   454	
   455	- API level (app booted with `SPEECH_*` pointing at StubSpeech):
   456	  `/config.speech == true`; `/speech/stt` round trip with an audio
   457	  fixture returns the stub transcript and passed `session.lang` as the
   458	  language; `/speech/tts` returns audio bytes; both 404 when speech is
   459	  unconfigured (existing behaviour, kept).
   460	- Browser E2E (Playwright, localhost = secure context, fake media device
   461	  flags `--use-fake-device-for-media-capture` +
   462	  `--use-fake-ui-for-media-capture` +
   463	  `--use-file-for-fake-audio-capture=<fixture wav>`, microphone
   464	  permission granted): mic button and TTS toggle visible; push-to-talk
   465	  click-start/click-stop records via real `MediaRecorder` (the fake
   466	  device streams the audio fixture), uploads to the stub, transcript
   467	  drives a turn (`spoken: true` asserted via the stub gateway seeing the
   468	  spoken-style note); with the toggle ON, exactly one TTS fetch per turn
   469	  and only for the final assistant message (StubSpeech call counter);
   470	  toggle OFF by default. This real UI push-to-talk path is mandatory —
   471	  API-level speech tests supplement it and never substitute for it.
   472	- Name-confirmation regression, three scripted cases (the saved-address
   473	  question is **not** a substitute for name confirmation):
   474	  1. plausible-but-wrong spoken name: agent repeats the name back, the
   475	     customer corrects, `set_customer` is called exactly once with the
   476	     corrected name, only after the correction — no submit before that;
   477	  2. spoken happy path, dictated street: the name is confirmed before
   478	     submission;
   479	  3. spoken happy path, saved street reused: the name is confirmed before
   480	     submission *in addition to* the saved-address yes/no question.
   481	  Prompts (both languages) state explicitly: in spoken conversations the
   482	  first name is always confirmed before the order is submitted.
   483	
   484	Live proof (opt-in, release-gating per SPEC):
   485	
   486	- `PIZZA_LIVE_VOICE=1` + `PIZZA_LIVE_VOICE_URL=<https base url of the
   487	  voice-capable deployment>`: a real headless browser drives the real
   488	  page over HTTPS end to end — microphone capture via the fake media
   489	  device streaming `order.de.wav` / `order.en.wav` (Chromium
   490	  `--use-file-for-fake-audio-capture`), real STT through the deployed
   491	  speech service, the transcript drives the chat, the confirm control
   492	  places the order, and with the toggle ON the final assistant message
   493	  fetches real TTS audio (response is non-empty browser-playable audio).
   494	  The four acceptance points are then verified via the pizzeria's
   495	  list+detail API endpoints. Not a text replay: if STT does not produce
   496	  an order-driving transcript from the fixture, the test fails. Skipped
   497	  cleanly when the env vars are unset; it cannot run on the current dev
   498	  VPS (no speech service, no HTTPS) and is executed against the
   499	  voice-capable deployment.
   500	
   501	## C. Tickets (≤1h each)
   502	
   503	1. Street-lookup core (client, Customer redaction split, tools, unit
   504	   tests incl. redaction sweep). ☐ booleans-only lookup ☐ submit carries
   505	   real street ☐ no saved-street text in events, logs or
   506	   session.messages.
   507	2. Street-lookup conversation (prompts DE/EN, two golden transcripts, UI
   508	   label). ☐ confirm-without-disclosure flow ☐ decline fallback.
   509	3. StubSpeech + audio fixtures + API-level speech tests. ☐ stt round
   510	   trip with session lang ☐ tts bytes ☐ 404 when unconfigured.
   511	4. Browser E2E voice wiring (fake media device). ☐ mic/toggle visible
   512	   ☐ push-to-talk round trip ☐ single final-message TTS fetch.
   513	5. Name-confirmation regression transcript. ☐ corrected name only,
   514	   after confirmation.
   515	6. deploy/ speech service definition + README voice section.
   516	   ☐ neutral (no vendor/model names) ☐ HTTPS requirement documented.
   517	7. Live voice acceptance test (opt-in) + docs. ☐ DE+EN fixtures ☐ skips
   518	   cleanly without SPEECH_URL ☐ full-order verification via API.

 succeeded in 183ms:
     1	"""Speech service client: self-hosted, OpenAI-compatible, optional.
     2	
     3	The browser captures and plays audio; recognition and synthesis happen
     4	here, server-side, against {SPEECH_URL}. The language sent with STT/TTS is
     5	the session language — there is no separate speech-language config.
     6	"""
     7	from __future__ import annotations
     8	
     9	import sys
    10	
    11	import httpx
    12	
    13	from core.pizzasim import optional_env
    14	
    15	
    16	class SpeechUnavailable(Exception):
    17	    pass
    18	
    19	
    20	class SpeechService:
    21	    """All-or-nothing: enabled only if SPEECH_URL is set, all models are
    22	    configured, and the service answered the startup probe with 2xx."""
    23	
    24	    def __init__(self):
    25	        self.url = (optional_env("SPEECH_URL") or "").rstrip("/")
    26	        self.stt_model = optional_env("SPEECH_STT_MODEL")
    27	        self.tts_model = optional_env("SPEECH_TTS_MODEL")
    28	        self.voice = optional_env("SPEECH_TTS_VOICE")
    29	        self.enabled = False
    30	        if self.url and self.stt_model and self.tts_model and self.voice:
    31	            try:
    32	                httpx.get(f"{self.url}/v1/models",
    33	                          timeout=3.0).raise_for_status()
    34	                self.enabled = True
    35	            except httpx.HTTPError:
    36	                print("speech service not answering — text-only mode",
    37	                      file=sys.stderr)
    38	
    39	    def stt(self, audio: bytes, filename: str, content_type: str,
    40	            lang: str) -> str:
    41	        try:
    42	            response = httpx.post(
    43	                f"{self.url}/v1/audio/transcriptions",
    44	                files={"file": (filename, audio, content_type)},
    45	                data={"model": self.stt_model, "language": lang},
    46	                timeout=60.0)
    47	            response.raise_for_status()
    48	        except httpx.HTTPError as exc:
    49	            raise SpeechUnavailable(str(exc)) from exc
    50	        return response.json().get("text", "")
    51	
    52	    def tts(self, text: str, lang: str) -> tuple[bytes, str]:
    53	        try:
    54	            response = httpx.post(
    55	                f"{self.url}/v1/audio/speech",
    56	                json={"model": self.tts_model, "voice": self.voice,
    57	                      "input": text, "language": lang},
    58	                timeout=60.0)
    59	            response.raise_for_status()
    60	        except httpx.HTTPError as exc:
    61	            raise SpeechUnavailable(str(exc)) from exc
    62	        return (response.content,
    63	                response.headers.get("content-type", "audio/mpeg"))

codex
SCORES (1-5 each, 5 = best):
completeness: 4
correctness: 4
error_handling: 3
simplicity: 4
spec_compliance: 3
TOTAL: 18/25
VERDICT: CHANGES_REQUIRED
ISSUES: (max 5 bullets, concrete and actionable, empty if approved)
- [PLAN.md:455-471, 484-499, 509-518] The plan still does not cover the SPEC runtime-outage requirement that speech controls disappear when the speech service becomes unavailable while the app is running, with typed ordering continuing normally ([SPEC.md:512-517, 565]). Add an explicit degrade-to-text-only design and a test that forces STT/TTS failures after startup and proves the mic/TTS controls are hidden or disabled and the text path still places an order.
- [PLAN.md:441-442, 460-471, 515-516] Secure context is only documented, not made an implementation/test requirement. The current UI gating only checks `cfg.speech`, `navigator.mediaDevices`, and `MediaRecorder` ([channels/static/app.js:322-330]), so an implementer could still show speech controls on an insecure non-localhost origin. Add a concrete requirement and test for `window.isSecureContext`/localhost gating so plain HTTP never presents a voice-capable UI ([SPEC.md:518-521]).
- [PLAN.md:486-499, 517-518] Ticket 7’s skip contract is inconsistent with the live-proof contract: the body says the test is gated by `PIZZA_LIVE_VOICE=1` plus `PIZZA_LIVE_VOICE_URL`, but the ticket checkbox says “skips cleanly without `SPEECH_URL`”. Align this so the implementer cannot wire the wrong env gate or document the wrong operator contract.
tokens used
53,303
SCORES (1-5 each, 5 = best):
completeness: 4
correctness: 4
error_handling: 3
simplicity: 4
spec_compliance: 3
TOTAL: 18/25
VERDICT: CHANGES_REQUIRED
ISSUES: (max 5 bullets, concrete and actionable, empty if approved)
- [PLAN.md:455-471, 484-499, 509-518] The plan still does not cover the SPEC runtime-outage requirement that speech controls disappear when the speech service becomes unavailable while the app is running, with typed ordering continuing normally ([SPEC.md:512-517, 565]). Add an explicit degrade-to-text-only design and a test that forces STT/TTS failures after startup and proves the mic/TTS controls are hidden or disabled and the text path still places an order.
- [PLAN.md:441-442, 460-471, 515-516] Secure context is only documented, not made an implementation/test requirement. The current UI gating only checks `cfg.speech`, `navigator.mediaDevices`, and `MediaRecorder` ([channels/static/app.js:322-330]), so an implementer could still show speech controls on an insecure non-localhost origin. Add a concrete requirement and test for `window.isSecureContext`/localhost gating so plain HTTP never presents a voice-capable UI ([SPEC.md:518-521]).
- [PLAN.md:486-499, 517-518] Ticket 7’s skip contract is inconsistent with the live-proof contract: the body says the test is gated by `PIZZA_LIVE_VOICE=1` plus `PIZZA_LIVE_VOICE_URL`, but the ticket checkbox says “skips cleanly without `SPEECH_URL`”. Align this so the implementer cannot wire the wrong env gate or document the wrong operator contract.
