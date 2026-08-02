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
session id: 019fc109-701b-7fa2-a7c4-2ad49e765bef
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


codex
Reviewing the delta plan gate against the committed tree. I’m loading the required skill instructions first, then I’ll read the referenced plan, spec, QA decisions, and relevant implementation surfaces before scoring round 3.
exec
/bin/bash -lc "sed -n '1,220p' /home/rob/.agents/skills/requesting-code-review/SKILL.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,220p' /home/rob/.agents/skills/using-superpowers/SKILL.md" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 264ms:
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

 succeeded in 293ms:
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
Using `using-superpowers` to enforce the required skill workflow for this review. I’m also loading its Codex-specific tool instructions before inspecting the plan artifacts.
exec
/bin/bash -lc "sed -n '1,220p' /home/rob/.agents/skills/references/codex-tools.md" in /home/rob/bpm-pizza-vibecoding-solution
 exited 2 in 0ms:
sed: can't read /home/rob/.agents/skills/references/codex-tools.md: No such file or directory

codex
The skill’s reference path is slightly different than advertised, so I’m locating the actual Codex tools reference in the skill directory and then reading the review inputs.
exec
/bin/bash -lc "find /home/rob/.agents/skills -path '*using-superpowers*' -o -path '*codex-tools.md'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' SPEC.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc 'tail -n 220 PLAN.md' in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' decisions/qa.md" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 266ms:
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

> Status 2026-08-01: tickets 1-9 all
> implemented; every acceptance box below is verified by the committed
> test suite (101 passed offline incl. 6 browser E2E, live acceptance
> passed).

1. **Prices & totals in core.** Menu price, `Item.unit_price`,
   snapshot totals (Decimal), get_menu result, prompt rule.
   ☑ totals only in core ☑ rounding tested ☑ v1 suite still green.
2. **Session factory & tenancy.** Session v2 fields, `create_session`,
   client per session, agent uses `session.client`, startup preselection
   check kept. ☑ unknown id → typed error ☑ tenant immutable ☑ tests.
3. **Language authority.** `Session.lang`, `set_language` re-render,
   apologies/STT via session.lang. ☑ switch test ☑ no process-global lang.
4. **Confirm path.** `Agent.confirm_and_submit` + synthetic messages.
   ☑ stale revision streams error, nothing submitted ☑ happy path test
   ☑ timeout-recovery reachable from this path.
5. **Web API surface.** /config, /session, /confirm, /language, /health,
   session 404/409 semantics, speech extraction to `channels/speech.py`.
   ☑ httpx TestClient tests with stub PizzaSim ☑ no order logic in routes.
6. **Web UI: frame.** Header (name, selector, dashboard link, language,
   start over), footer (version, UUID, health badges, docs), i18n chrome.
   ☑ switch/start-over create fresh session + abort in-flight stream.
7. **Web UI: conversation contract.** Basket panel, read-back panel +
   confirm button, working indicator, done-without-assistant notice,
   error/resend paths, submitted lock.
   ☑ every notice in session language ☑ no discarded stream events.
8. **Browser E2E suite.** Stub PizzaSim + stub gateway + Playwright;
   scenarios 1–5 above. ☑ fully offline ☑ DOM assertions only.
9. **Harden + docs.** Error-table walk incl. new rows, README (all
   channels + E2E + speech checklist), `.env.example`, `APP_VERSION`
   start at `2.0.0`. ☑ full suite green ☑ live acceptance re-run.

Review protocol: this plan goes to the reviewer (Issue gate) before any
code; implementation follows only after APPROVED under the SPEC rubric.


---

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
5. Name-confirmation regression transcript. ☐ corrected name only,
   after confirmation.
6. deploy/ speech service definition + README voice section.
   ☐ neutral (no vendor/model names) ☐ HTTPS requirement documented.
7. Live voice acceptance test (opt-in) + docs. ☐ DE+EN fixtures
   ☐ gated on `PIZZA_LIVE_VOICE=1` + `PIZZA_LIVE_VOICE_URL` and skips
   cleanly when either is unset ☐ full-order verification via API.

 succeeded in 291ms:
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
5. With speech configured in the target deployment, a spoken conversation
   on the web channel can produce the same verified order outcome as
   points 1–4.

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
- **Speech on the web transport is a required channel capability in
  production.** It is provisioned via the self-hosted speech service
  described in *Speech*; if the service is unavailable at runtime,
  ordering degrades to text-only without breaking ordering.
- **Several pizzerias.** The customer chooses which one they are ordering
  from, and can change it. `PIZZERIA_ID` is the preselection, not a
  restriction.
- **Returning customers.** A known first name can reuse its saved street
  after an explicit confirmation — limited to address reuse via the
  PizzaSim customer data; broader cross-session memory ("the usual")
  stays deferred.
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
| `SPEECH_URL` | Base URL of the self-hosted speech service; required in production releases, optional only for local/dev and explicit text-only test scenarios |
| `SPEECH_STT_MODEL` | Transcription model id |
| `SPEECH_TTS_MODEL` | Synthesis model id |
| `SPEECH_TTS_VOICE` | Voice id |

Rules:

- **Nothing is hardcoded.** No UUID, no model name, no menu, no base URL, no
  vendor — not even as a fallback "just in case".
- Missing or empty required variable → exit before the first turn with a
  message naming the variable and the file it was expected in. Never start
  half-configured. For production completeness, `SPEECH_URL`,
  `SPEECH_STT_MODEL`, `SPEECH_TTS_MODEL` and `SPEECH_TTS_VOICE` are
  required. For local/dev and explicit degraded-mode tests they may be
  absent; in that case speech controls are not rendered and text ordering
  remains fully usable.
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

 succeeded in 313ms:
/home/rob/.agents/skills/using-superpowers
/home/rob/.agents/skills/using-superpowers/references
/home/rob/.agents/skills/using-superpowers/references/antigravity-tools.md
/home/rob/.agents/skills/using-superpowers/references/gemini-tools.md
/home/rob/.agents/skills/using-superpowers/references/pi-tools.md
/home/rob/.agents/skills/using-superpowers/references/codex-tools.md
/home/rob/.agents/skills/using-superpowers/SKILL.md

 succeeded in 284ms:
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
I’ve got the reviewed delta section and the spec decisions. Next I’m checking the Codex tool note plus the existing core/web/test surfaces the delta extends, so I can judge contradictions against the already-approved v2 implementation rather than the plan in isolation.
exec
/bin/bash -lc "sed -n '1,220p' /home/rob/.agents/skills/using-superpowers/references/codex-tools.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc 'rg -n "lookup_customer|set_customer|read_back|submit_order|confirm_order|street_on_file|speech|MediaRecorder|isSecureContext|session.messages|JSONL|jsonl|spoken" core channels tests -S' in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc 'rg -n "saved address|gespeicherte Adresse|saved_street|street_one|street_two|customer_exists|saved_street_available|no_saved_street|invalid_arguments|api_unavailable" SPEC.md PLAN.md decisions/qa.md core channels tests -S' in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 218ms:
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

 succeeded in 237ms:
tests/test_web_e2e.py:71:    assert cfg["speech"] is False
tests/test_web_e2e.py:158:                and e.get("tool") == "read_back"][-1]
tests/test_web_e2e.py:164:                 and e.get("tool") == "submit_order"][-1]
tests/test_web_e2e.py:227:    # speech disabled → controls not rendered
tests/stubs.py:139:        if name == "set_customer":
tests/stubs.py:140:            return _tool_call("read_back", {})
tests/stubs.py:141:        if name == "read_back":
tests/stubs.py:144:        if name == "submit_order":
tests/stubs.py:147:        if name == "confirm_order":
tests/stubs.py:148:            return _tool_call("submit_order", {})
tests/stubs.py:164:        return _tool_call("set_customer", {"first_name": "Eva"})
tests/test_tools.py:98:        ).submit_order({"first_name": "X"}, [])
tests/test_tools.py:127:    result = client.submit_order({"first_name": "Marco"}, [])
tests/test_tools.py:180:    def submit_order(self, customer, items):
tests/test_tools.py:209:    tools.dispatch(order, menu, fake, "set_customer",
tests/test_tools.py:216:    tools.dispatch(order, menu, fake, "read_back", {})
tests/test_tools.py:217:    tools.dispatch(order, menu, fake, "confirm_order",
tests/test_tools.py:234:    assert snap["customer"] is None and snap["read_back_done"] is False
tests/test_tools.py:291:    result = tools.dispatch(order, menu, fake, "submit_order", {})
tests/test_tools.py:301:    result = tools.dispatch(order, menu, fake, "submit_order", {})
tests/test_tools.py:307:    result = tools.dispatch(Order(), menu, fake, "submit_order", {})
tests/test_tools.py:315:    result = tools.dispatch(order, menu, fake, "submit_order", {})
tests/test_tools.py:330:    result = tools.dispatch(order, menu, fake, "submit_order", {})
tests/test_tools.py:341:    tools.dispatch(order, menu, fake, "submit_order", {})
tests/test_tools.py:352:    result = tools.dispatch(order, menu, fake, "submit_order", {})
tests/test_tools.py:363:    tools.dispatch(order, menu, fake, "submit_order", {})
tests/test_tools.py:371:    tools.dispatch(order, menu, fake, "read_back", {})
tests/test_tools.py:372:    tools.dispatch(order, menu, fake, "confirm_order",
tests/test_tools.py:380:    result = tools.dispatch(order, menu, fake, "submit_order", {})
tests/test_tools.py:388:    result = tools.dispatch(order, menu, fake, "submit_order", {})
tests/test_tools.py:395:    result = tools.dispatch(order, menu, fake, "submit_order", {})
tests/test_tools.py:403:    tools.dispatch(order, menu, fake, "submit_order", {})
tests/test_tools.py:405:    result = tools.dispatch(order, menu, fake, "submit_order", {})
tests/test_tools.py:414:    result = tools.dispatch(order, menu, fake, "submit_order", {})
tests/test_tools.py:423:    result = tools.dispatch(order, menu, fake, "submit_order", {})
tests/test_tools.py:433:    tools.dispatch(order, menu, fake, "set_customer",
tests/test_tools.py:435:    tools.dispatch(order, menu, fake, "read_back", {})
tests/test_tools.py:436:    tools.dispatch(order, menu, fake, "confirm_order",
tests/test_tools.py:443:    real_submit = fake.submit_order
tests/test_tools.py:448:    fake.submit_order = spy
tests/test_tools.py:449:    tools.dispatch(order, menu, fake, "submit_order", {})
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
tests/test_tools.py:569:    tools.dispatch(session.order, session.menu, fake, "set_customer",
tests/test_tools.py:571:    tools.dispatch(session.order, session.menu, fake, "read_back", {})
tests/test_tools.py:585:    assert tool_names == ["confirm_order", "submit_order"]
tests/test_tools.py:587:    roles = [m["role"] for m in session.messages]
tests/test_tools.py:589:    assert session.messages[-1]["role"] == "assistant"
tests/test_tools.py:608:    assert session.messages[-2]["role"] == "tool"
tests/test_tools.py:651:        ("set_customer", {"first_name": "Akzeptanz",
tests/test_tools.py:653:        ("read_back", {}),
tests/test_tools.py:657:    result = tools.dispatch(order, menu, client, "confirm_order",
tests/test_tools.py:660:    result = tools.dispatch(order, menu, client, "submit_order", {})
tests/test_state.py:22:    state.set_customer(o, Customer("Marco", "via Roma"))
tests/test_state.py:25:    state.read_back(o)
tests/test_state.py:46:    state.set_customer(o, Customer("Marco", "via Roma"))
tests/test_state.py:48:    state.read_back(o)
tests/test_state.py:60:    state.set_customer(o, Customer("Anna"))
tests/test_state.py:71:    lambda o: state.set_customer(o, Customer("Eve")),
tests/test_state.py:72:    lambda o: state.read_back(o),
tests/test_state.py:89:def test_read_back_empty():
tests/test_state.py:91:        state.read_back(order_in(State.EMPTY))
tests/test_state.py:95:def test_read_back_collecting_needs_customer():
tests/test_state.py:97:        state.read_back(order_in(State.COLLECTING))
tests/test_state.py:146:def test_set_customer_after_confirmed_demotes():
tests/test_state.py:148:    state.set_customer(o, Customer("Mario"))
tests/test_state.py:162:def test_confirm_without_read_back():
tests/test_state.py:166:    assert e.value.code == "read_back_required"
tests/test_state.py:171:    state.read_back(o)
tests/test_state.py:179:def test_read_back_of_old_revision_does_not_allow_confirm():
tests/test_state.py:181:    state.read_back(o)
tests/test_state.py:185:    assert e.value.code == "read_back_required"
tests/test_state.py:194:    state.set_customer(o, Customer("A"))
tests/test_transcripts.py:52:    def submit_order(self, customer, items):
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
core/tools.py:56:    {"name": "set_customer",
core/tools.py:64:    {"name": "read_back",
core/tools.py:68:    {"name": "confirm_order",
core/tools.py:75:    {"name": "submit_order",
core/tools.py:77:                    "after confirm_order.",
core/tools.py:161:    if name == "set_customer":
core/tools.py:166:        state.set_customer(order, customer)
core/tools.py:170:    if name == "read_back":
core/tools.py:171:        state.read_back(order)
core/tools.py:174:    if name == "confirm_order":
core/tools.py:182:    if name == "submit_order":
core/tools.py:249:        result = client.submit_order(customer, items)
core/order.py:53:    read_back_revision: int | None = None
core/order.py:81:            "read_back_done": self.read_back_revision == self.revision,
core/agent.py:2:JSONL event logging. The model only speaks; the order lives in core.
core/agent.py:38:    "en": "This reply will be spoken aloud: name at most three dishes, "
core/agent.py:128:    session.messages[0] = {
core/agent.py:139:    with (LOG_DIR / f"agent-{session.id}.jsonl").open("a") as fh:
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
core/agent.py:281:        failure; CONFIRMED stays reachable only via confirm_order."""
core/agent.py:288:            session, "confirm_order", {"revision": revision}, event)
core/agent.py:290:            self._synthetic_call(session, "submit_order", {}, event)
channels/web.py:5:/health, speech proxies, static UI. Turns are serialized per session;
channels/web.py:26:from channels.speech import SpeechService, SpeechUnavailable
channels/web.py:77:    app.state.speech = SpeechService()
channels/web.py:96:        "speech": app.state.speech.enabled,
channels/web.py:173:    spoken = bool(body.get("spoken"))
channels/web.py:177:                                              spoken=spoken),
channels/web.py:206:def _speech() -> SpeechService:
channels/web.py:207:    if not app.state.speech.enabled:
channels/web.py:208:        raise HTTPException(404, "speech is not available")
channels/web.py:209:    return app.state.speech
channels/web.py:212:@app.post("/speech/stt")
channels/web.py:214:    speech = _speech()
channels/web.py:217:        text = speech.stt(await audio.read(),
channels/web.py:222:        raise HTTPException(502, "speech service unavailable")
channels/web.py:226:@app.post("/speech/tts")
channels/web.py:228:    speech = _speech()
channels/web.py:234:        audio, content_type = speech.tts(text, session.lang)
channels/web.py:236:        raise HTTPException(502, "speech service unavailable")
core/pizzasim.py:153:    def submit_order(self, customer: dict, items: list[dict]) -> dict:
channels/speech.py:5:the session language — there is no separate speech-language config.
channels/speech.py:36:                print("speech service not answering — text-only mode",
channels/speech.py:55:                f"{self.url}/v1/audio/speech",
core/state.py:83:def set_customer(order: Order, customer: Customer) -> None:
core/state.py:89:def read_back(order: Order) -> None:
core/state.py:100:    order.read_back_revision = order.revision
core/state.py:120:    if order.read_back_revision != order.revision:
core/state.py:122:            "read_back_required",
channels/static/app.js:3:   Speech: browser captures/plays audio only (MediaRecorder + <audio>);
channels/static/app.js:4:   recognition/synthesis happen server-side. No browser speech APIs. */
channels/static/app.js:216:            if (ev.tool === "read_back") showReadback(ev.result.snapshot);
channels/static/app.js:284:async function sendTurn(text, spoken = false) {
channels/static/app.js:287:    "/chat", { session_id: session.id, text, spoken }, text ?? undefined);
channels/static/app.js:288:  if (finalText && cfg.speech && $("tts-toggle").checked) speak(finalText);
channels/static/app.js:298:  if (finalText && cfg.speech && $("tts-toggle").checked) speak(finalText);
channels/static/app.js:327:  const speechUsable = cfg.speech;
channels/static/app.js:328:  $("tts-wrap").hidden = !speechUsable;
channels/static/app.js:329:  $("mic").hidden = !(speechUsable && navigator.mediaDevices &&
channels/static/app.js:330:                      window.MediaRecorder);
channels/static/app.js:364:/* ---------- speech (capture/playback only) ------------------------------ */
channels/static/app.js:370:  recorder = new MediaRecorder(stream);
channels/static/app.js:379:    body.append("audio", blob, "speech.webm");
channels/static/app.js:382:        `/speech/stt?session_id=${session.id}`, { method: "POST", body });
channels/static/app.js:403:    const res = await fetch("/speech/tts", {

 succeeded in 211ms:
decisions/qa.md:48:`use_saved_street: true` (mutually exclusive with `street_one`) and the
decisions/qa.md:52:street_one until street_two on POST /orders is verified. SPEC.md updated
tests/test_tools.py:210:                   {"first_name": "Marco", "street_one": "via Roma"})
tests/test_tools.py:424:    assert result["error"]["code"] == "api_unavailable"
tests/test_tools.py:652:                          "street_one": "via Verdi 7"}),
tests/transcripts/unknown_item.json:17:       {"tool": "set_customer", "args": {"first_name": "Luca", "street_one": "via Milano 2"}},
tests/transcripts/mind_change.json:8:       {"tool": "set_customer", "args": {"first_name": "Sara", "street_one": "via Napoli 9"}},
tests/transcripts/submit_timeout.json:8:       {"tool": "set_customer", "args": {"first_name": "Nino", "street_one": "via Genova 1"}},
tests/transcripts/happy_path.json:17:       {"tool": "set_customer", "args": {"first_name": "Marco", "street_one": "via Roma 5"}},
PLAN.md:380:## A. Street lookup (SPEC: lookup_customer / use_saved_street / redaction)
PLAN.md:391:    `{"first_name", "street_one": null, "street_on_file": true}` — the
PLAN.md:395:    the real `street_one`. Submit uses saved `street_one` only — never
PLAN.md:396:    `street_two` (SPEC guardrail).
PLAN.md:399:    `{"customer_exists": bool, "saved_street_available": bool, "snapshot"}`
PLAN.md:401:    uniform error shape with code `api_unavailable` (non-fatal; the model
PLAN.md:403:  - `set_customer` params become `{first_name, street_one?,
PLAN.md:404:    use_saved_street?}` — mutually exclusive; both set → error code
PLAN.md:405:    `invalid_arguments` with a speakable message. With the flag, dispatch
PLAN.md:406:    fetches the customer record in code, copies `street_one`, sets
PLAN.md:408:    `no_saved_street` (speakable), basket untouched.
PLAN.md:412:  reciting the address; yes → `set_customer(use_saved_street: true)`;
PLAN.md:416:  localized label "gespeicherte Adresse"/"saved address", never text.
PLAN.md:421:- `use_saved_street` copies in code; the redaction sweep is end to end:
PLAN.md:428:- Mutual exclusion + `no_saved_street` paths.
SPEC.md:215:  "customer": { "first_name": "Marco", "street_one": "via di Cantieri" },
SPEC.md:235:- `street_one` is optional and **not** validated for deliverability. Asking
SPEC.md:271:  `X-API-Key`) returns `customers[]` with `{id, first_name, street_one,
SPEC.md:272:  street_two, created_at, deleted_at}`. Since customers are unique per
SPEC.md:275:  `street_one`, so address reuse is limited to `street_one` until
SPEC.md:276:  `street_two` support on `POST /orders` is verified as well.
SPEC.md:328:| `lookup_customer` | `first_name` | `{customer_exists, saved_street_available}` — booleans only, **no street text** |
SPEC.md:329:| `set_customer` | `first_name`, plus either `street_one` **or** `use_saved_street: true` (mutually exclusive) — with the flag, the **code** copies the saved street into the order; the text never passes through the model | customer as stored (saved street as a flag, not text) |
SPEC.md:356:  "saved address", never as text. A street the customer dictated in this
SPEC.md:385:  gespeicherte Adresse liefern?") **without reciting the address**; on yes,
SPEC.md:386:  `set_customer(use_saved_street: true)`. If the customer declines, is
SPEC.md:612:  `set_customer(use_saved_street: true)` copying in code; redaction tests
core/tools.py:62:                        "street_one": {"type": "string"}},
core/tools.py:120:        return _error("api_unavailable",
core/tools.py:123:        return _error("api_unavailable",
core/tools.py:126:        return _error("api_unavailable",
core/tools.py:165:        customer = Customer(first_name, args.get("street_one") or None)
core/tools.py:244:    if customer.get("street_one") is None:
core/tools.py:245:        customer.pop("street_one")
core/tools.py:255:        return _error("api_unavailable",
core/order.py:42:    street_one: str | None = None
core/order.py:45:        return {"first_name": self.first_name, "street_one": self.street_one}
channels/static/app.js:172:      (snapshot.customer.street_one
channels/static/app.js:173:        ? `, ${snapshot.customer.street_one}` : "")

exec
/bin/bash -lc "sed -n '1,220p' core/order.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '260,420p' SPEC.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,340p' core/tools.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '560,660p' SPEC.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,460p' channels/static/app.js" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 311ms:
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

 succeeded in 355ms:
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

 succeeded in 369ms:
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

Type or paste a message, get an answer. The exchange a first-time customer
should be able to have, end to end, without help:

> *What have you got?* → *What does a Margherita cost?* → *I'll take two of
> those and a pasta* → *I'm a new customer, my name is …* → read-back →
> confirm → order id and wait time.

After a completed order, a new conversation can start immediately from the
same page.


 succeeded in 375ms:
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

 succeeded in 345ms:
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

codex
The existing UI and tool layer are enough to expose where the delta plan still relies on implementation assumptions. I’m checking the speech service and web boot path now, mainly for whether the new degradation and secure-context requirements are actually compatible with today’s startup-only speech gating.
exec
/bin/bash -lc "sed -n '1,280p' channels/web.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,220p' channels/speech.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,320p' tests/test_web_e2e.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '520,620p' tests/test_tools.py" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 276ms:
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

 succeeded in 282ms:
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

 succeeded in 292ms:
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

 succeeded in 269ms:

def test_set_language_rerenders_system_prompt_in_place():
    session = create_session(config_stub(), FakeBase())
    history_before = len(session.messages)
    german = session.messages[0]["content"]
    set_language(session, "en")
    assert session.lang == "en"
    assert session.messages[0]["content"] != german
    assert "Pizzeria Default" in session.messages[0]["content"]
    assert len(session.messages) == history_before  # history preserved


def test_apology_follows_session_language():
    def dead(messages, tool_schemas):
        raise GatewayError("gateway timed out twice")
    session = create_session(config_stub(), FakeBase())
    set_language(session, "en")
    text = Agent(config_stub(), chat_fn=dead).run_turn(session, "hi")
    assert "sorry" in text.lower()


def test_spoken_note_is_ephemeral_per_turn():
    """The spoken-style note reaches the model for the spoken turn only —
    it is never persisted, and a later typed turn does not inherit it."""
    seen = []

    def say(messages, tool_schemas):
        seen.append([m["content"] for m in messages
                     if m["role"] == "system"])
        return {"content": "ok"}
    session = create_session(config_stub(), FakeBase())
    agent = Agent(config_stub(), chat_fn=say)
    agent.run_turn(session, "hallo", spoken=True)
    assert any("Diese Antwort wird vorgelesen" in c
               for c in seen[-1])  # note seen this turn
    agent.run_turn(session, "hallo")
    assert not any("Diese Antwort wird vorgelesen" in c
                   for c in seen[-1])  # gone next turn
    assert not any(m["role"] == "system"
                   and "Diese Antwort wird vorgelesen" in m["content"]
                   for m in session.messages)  # never persisted


def confirm_ready_session(chat_fn):
    session = create_session(config_stub(), FakeBase())
    fake = session.client
    tools.dispatch(session.order, session.menu, fake, "add_items",
                   {"items": [{"type": "pizza", "code": "margherita",
                               "qty": 2}]})
    tools.dispatch(session.order, session.menu, fake, "set_customer",
                   {"first_name": "Marco"})
    tools.dispatch(session.order, session.menu, fake, "read_back", {})
    return session, Agent(config_stub(), chat_fn=chat_fn)


def test_confirm_and_submit_happy_path():
    def phrase(messages, tool_schemas):
        return {"content": "Bestellt!"}
    session, agent = confirm_ready_session(phrase)
    events = []
    text = agent.confirm_and_submit(session, session.order.revision,
                                    events.append)
    assert text == "Bestellt!"
    assert session.order.state is State.SUBMITTED
    tool_names = [e["tool"] for e in events if e["type"] == "tool_call"]
    assert tool_names == ["confirm_order", "submit_order"]
    # synthetic history is model-shaped: assistant tool_calls + tool result
    roles = [m["role"] for m in session.messages]
    assert roles.count("tool") == 2
    assert session.messages[-1]["role"] == "assistant"


def test_confirm_with_stale_revision_submits_nothing():
    def phrase(messages, tool_schemas):
        return {"content": "Da hat sich etwas geändert."}
    session, agent = confirm_ready_session(phrase)
    stale = session.order.revision
    tools.dispatch(session.order, session.menu, session.client,
                   "add_items", {"items": [{"type": "pasta",
                                            "code": "pesto", "qty": 1}]})
    events = []
    agent.confirm_and_submit(session, stale, events.append)
    errors = [e["result"]["error"]["code"] for e in events
              if e["type"] == "tool_result" and "error" in e["result"]]
    assert errors == ["stale_revision"]
    assert session.client.submits == 0
    assert session.order.state is not State.SUBMITTED
    # the failed dispatch is in the history exactly like a model call
    assert session.messages[-2]["role"] == "tool"


def test_confirm_gateway_death_still_answers():
    """Answer-or-rendered-error invariant on /confirm: dispatches applied,
    apology streamed as an assistant event."""
    def dead(messages, tool_schemas):
        raise GatewayError("gateway request failed")
    session, agent = confirm_ready_session(dead)
    events = []
    text = agent.confirm_and_submit(session, session.order.revision,
                                    events.append)
    assert session.order.state is State.SUBMITTED  # order went through

codex
I’ve narrowed the remaining risk to a couple of places where the detailed prose is stronger than the ticket contract. I’m pulling exact line references now so the verdict is concrete and actionable.
exec
/bin/bash -lc "nl -ba SPEC.md | sed -n '320,420p'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "nl -ba PLAN.md | sed -n '380,490p'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "nl -ba SPEC.md | sed -n '600,640p'" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 306ms:
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
   472	- **Runtime degradation:** when a speech call fails after startup (STT or
   473	  TTS returns an error / the proxy answers 502), the UI hides the mic and
   474	  the TTS toggle for the rest of the session and shows a plain-language
   475	  notice; typed ordering continues untouched. E2E test: StubSpeech is
   476	  switched to failure mode mid-session → controls disappear, a typed
   477	  order still completes. (Startup-down behaviour — probe fails → controls
   478	  never rendered — exists since v1 and keeps its test.)
   479	- **Secure-context gating in the UI, not just in the docs:** the speech
   480	  controls render only when `window.isSecureContext` is true (HTTPS or
   481	  localhost) in addition to `cfg.speech` and the media APIs. E2E test: an
   482	  init script forces `isSecureContext = false` → with speech fully
   483	  configured, neither mic nor TTS toggle is rendered and text ordering
   484	  works — plain HTTP never presents a voice-capable UI.
   485	- Name-confirmation regression, three scripted cases (the saved-address
   486	  question is **not** a substitute for name confirmation):
   487	  1. plausible-but-wrong spoken name: agent repeats the name back, the
   488	     customer corrects, `set_customer` is called exactly once with the
   489	     corrected name, only after the correction — no submit before that;
   490	  2. spoken happy path, dictated street: the name is confirmed before

 succeeded in 338ms:
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
   411	Type or paste a message, get an answer. The exchange a first-time customer
   412	should be able to have, end to end, without help:
   413	
   414	> *What have you got?* → *What does a Margherita cost?* → *I'll take two of
   415	> those and a pasta* → *I'm a new customer, my name is …* → read-back →
   416	> confirm → order id and wait time.
   417	
   418	After a completed order, a new conversation can start immediately from the
   419	same page.
   420	

 succeeded in 289ms:
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

exec
/bin/bash -lc "nl -ba PLAN.md | sed -n '485,520p'" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 0ms:
   485	- Name-confirmation regression, three scripted cases (the saved-address
   486	  question is **not** a substitute for name confirmation):
   487	  1. plausible-but-wrong spoken name: agent repeats the name back, the
   488	     customer corrects, `set_customer` is called exactly once with the
   489	     corrected name, only after the correction — no submit before that;
   490	  2. spoken happy path, dictated street: the name is confirmed before
   491	     submission;
   492	  3. spoken happy path, saved street reused: the name is confirmed before
   493	     submission *in addition to* the saved-address yes/no question.
   494	  Prompts (both languages) state explicitly: in spoken conversations the
   495	  first name is always confirmed before the order is submitted.
   496	
   497	Live proof (opt-in, release-gating per SPEC):
   498	
   499	- `PIZZA_LIVE_VOICE=1` + `PIZZA_LIVE_VOICE_URL=<https base url of the
   500	  voice-capable deployment>`: a real headless browser drives the real
   501	  page over HTTPS end to end — microphone capture via the fake media
   502	  device streaming `order.de.wav` / `order.en.wav` (Chromium
   503	  `--use-file-for-fake-audio-capture`), real STT through the deployed
   504	  speech service, the transcript drives the chat, the confirm control
   505	  places the order, and with the toggle ON the final assistant message
   506	  fetches real TTS audio (response is non-empty browser-playable audio).
   507	  The four acceptance points are then verified via the pizzeria's
   508	  list+detail API endpoints. Not a text replay: if STT does not produce
   509	  an order-driving transcript from the fixture, the test fails. Skipped
   510	  cleanly when the env vars are unset; it cannot run on the current dev
   511	  VPS (no speech service, no HTTPS) and is executed against the
   512	  voice-capable deployment.
   513	
   514	## C. Tickets (≤1h each)
   515	
   516	1. Street-lookup core (client, Customer redaction split, tools, unit
   517	   tests incl. redaction sweep). ☐ booleans-only lookup ☐ submit carries
   518	   real street ☐ no saved-street text in events, logs or
   519	   session.messages.
   520	2. Street-lookup conversation (prompts DE/EN, two golden transcripts, UI

exec
/bin/bash -lc "nl -ba PLAN.md | sed -n '520,540p'" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 0ms:
   520	2. Street-lookup conversation (prompts DE/EN, two golden transcripts, UI
   521	   label). ☐ confirm-without-disclosure flow ☐ decline fallback.
   522	3. StubSpeech + audio fixtures + API-level speech tests. ☐ stt round
   523	   trip with session lang ☐ tts bytes ☐ 404 when unconfigured.
   524	4. Browser E2E voice wiring (fake media device). ☐ mic/toggle visible
   525	   ☐ push-to-talk round trip ☐ single final-message TTS fetch
   526	   ☐ mid-session speech failure degrades to text-only ☐ insecure
   527	   context renders no speech controls.
   528	5. Name-confirmation regression transcript. ☐ corrected name only,
   529	   after confirmation.
   530	6. deploy/ speech service definition + README voice section.
   531	   ☐ neutral (no vendor/model names) ☐ HTTPS requirement documented.
   532	7. Live voice acceptance test (opt-in) + docs. ☐ DE+EN fixtures
   533	   ☐ gated on `PIZZA_LIVE_VOICE=1` + `PIZZA_LIVE_VOICE_URL` and skips
   534	   cleanly when either is unset ☐ full-order verification via API.

codex
SCORES (1-5 each, 5 = best):
completeness: 3
correctness: 4
error_handling: 4
simplicity: 4
spec_compliance: 3
TOTAL: 18/25
VERDICT: CHANGES_REQUIRED
ISSUES: (max 5 bullets, concrete and actionable, empty if approved)
- [PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:421) still weakens the SPEC redaction contract from [SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:612): the sweep names snapshots, emitted events, JSONL logs, and `session.messages`, but not transcript artifacts explicitly. Add an explicit requirement/test that the saved street text is absent from golden transcript fixtures and any transcript-derived serialization, not just runtime events/logs.
- [PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:485) correctly defines three spoken name-confirmation cases, but Ticket 5 collapses that back to one case at [PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:528). Expand Ticket 5 so the execution contract requires all three cases: wrong-name correction, spoken happy path with dictated street, and spoken happy path with saved-street reuse.
- Ticket 7 under-specifies the live voice proof versus its own prose. The detailed requirement at [PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:499) includes real HTTPS browser flow, STT that must actually yield an order-driving transcript, and non-empty real TTS audio; the ticket checkbox at [PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:532) only requires DE/EN fixtures, env gating, and API verification. Add checkboxes for “real HTTPS browser path”, “STT failure to produce the transcript fails the test”, and “final-message TTS returns non-empty playable audio”.
tokens used
50,031
SCORES (1-5 each, 5 = best):
completeness: 3
correctness: 4
error_handling: 4
simplicity: 4
spec_compliance: 3
TOTAL: 18/25
VERDICT: CHANGES_REQUIRED
ISSUES: (max 5 bullets, concrete and actionable, empty if approved)
- [PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:421) still weakens the SPEC redaction contract from [SPEC.md](/home/rob/bpm-pizza-vibecoding-solution/SPEC.md:612): the sweep names snapshots, emitted events, JSONL logs, and `session.messages`, but not transcript artifacts explicitly. Add an explicit requirement/test that the saved street text is absent from golden transcript fixtures and any transcript-derived serialization, not just runtime events/logs.
- [PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:485) correctly defines three spoken name-confirmation cases, but Ticket 5 collapses that back to one case at [PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:528). Expand Ticket 5 so the execution contract requires all three cases: wrong-name correction, spoken happy path with dictated street, and spoken happy path with saved-street reuse.
- Ticket 7 under-specifies the live voice proof versus its own prose. The detailed requirement at [PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:499) includes real HTTPS browser flow, STT that must actually yield an order-driving transcript, and non-empty real TTS audio; the ticket checkbox at [PLAN.md](/home/rob/bpm-pizza-vibecoding-solution/PLAN.md:532) only requires DE/EN fixtures, env gating, and API verification. Add checkboxes for “real HTTPS browser path”, “STT failure to produce the transcript fails the test”, and “final-message TTS returns non-empty playable audio”.
