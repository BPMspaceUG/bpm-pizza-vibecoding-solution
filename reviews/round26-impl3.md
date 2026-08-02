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
session id: 019fc11f-3479-7cc2-aa68-6ea3b3b36a72
--------
user
## Context

Delta Plan v3 (street lookup + voice) was gate-approved in #3 (22/25). All seven delta tickets are implemented and checked off in PLAN.md. This issue is the implementation gate under the SPEC rubric.

## Scope of the diff under review

Commits 27de272..HEAD on main: core/pizzasim.py (list_customers, deleted filtered), core/order.py (Customer.street_from_saved, redacted as_dict vs as_submit_dict), core/tools.py (lookup_customer booleans-only, set_customer use_saved_street with mutual exclusion + no_saved_street, submit via as_submit_dict, canonical name casing from the record), prompts (lookup flow, confirm-without-disclosure, spoken name-confirmation rule), channels/static/app.js (saved-address label, isSecureContext gating, runtime degradeSpeech on STT/TTS failure), tests/stubs.py (StubSpeech, spoken-note detection, system-message-skip in the script parser), tests/test_web_speech.py (9 offline tests: API surface + Firefox fake-mic browser E2E incl. push-to-talk round trip, single final-message TTS, runtime outage degradation, insecure-context gating; plus the opt-in live voice acceptance test driving a real HTTPS deployment via Chromium fake-audio-file capture), tests/transcripts (5 new: saved-address reuse, decline fallback, three name-confirmation cases with order-position assertions), tests/fixtures/audio (real synthesized DE/EN spoken orders), deploy/speech-service.compose.yml (neutral, no vendor/model names), README (voice deployment section).

## Facts demonstrated live (you cannot observe these from files)

Offline suite: 124 passed, 3 skipped (the opt-in live tests), exit 0 — including the end-to-end redaction sweep (fixture street appears ONLY in the submit payload; asserted absent from events, logs and session.messages), all 12 golden transcripts, and all 9 speech-wiring tests. The live TEXT acceptance test re-passed against the real API today. The live VOICE test is implemented and skips cleanly here: this dev VPS has no speech service and no HTTPS, so it executes on the voice-capable deployment (SPEC's split of offline wiring vs live proof).

## Documented deviation to judge

decisions/qa.md (2026-08-02): the OFFLINE browser voice E2E runs on Firefox fake streams instead of the plan's Chromium fake-device flags — headless Chromium on this host exposes no audio device even with the flags (verified; enumerateDevices empty). The identical UI path (getUserMedia + MediaRecorder + upload) is exercised; cross-browser operation is itself a SPEC requirement; the Chromium fake-audio-FILE path is used where content matters (live voice test).

## Judge request

Devil's advocate + judge in one pass. Verify the claims in the files — especially: redaction end to end (as_dict vs as_submit_dict call sites; anything else serializing the customer?), mutual exclusion and error codes, prompts vs SPEC conversation policy, isSecureContext + degradation in app.js, single-final-TTS logic, the live voice test really failing when STT yields no order-driving transcript, and the neutral deploy artifact carrying no vendor/model names. Score against the fixed SPEC rubric and end with exactly:

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
I’m treating this as a code review against the SPEC gate, with emphasis on verifying the claimed behaviors in the diff and testing artifacts. I’ll read the relevant review instructions first, then inspect the touched files and tests before scoring each rubric dimension.
exec
/bin/bash -lc "sed -n '1,220p' /home/rob/.agents/skills/using-superpowers/SKILL.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' /home/rob/.agents/skills/receiving-code-review/SKILL.md" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 246ms:
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

 succeeded in 214ms:
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
Using `using-superpowers` for process compliance and `receiving-code-review` for the review posture. Next I’m checking the Codex-specific instructions from the superpowers skill, then I’ll inspect the exact diff and targeted files.
exec
/bin/bash -lc "sed -n '1,240p' /home/rob/.agents/skills/references/codex-tools.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc 'git status --short && git rev-parse --abbrev-ref HEAD && git log --oneline --decorate -n 5' in /home/rob/bpm-pizza-vibecoding-solution
 exited 2 in 280ms:
sed: can't read /home/rob/.agents/skills/references/codex-tools.md: No such file or directory

 succeeded in 292ms:
main
13da540 (HEAD -> main) Check off Delta Plan v3 tickets; live text acceptance re-passed
c483f2f Delta v3 tickets 5-7: name-confirmation transcripts (3 cases), neutral speech deploy definition, README voice section, live voice acceptance test (opt-in)
d0328c8 Delta v3 tickets 3-4: StubSpeech, audio fixtures, speech API tests, browser voice E2E (Firefox fake mic), runtime degradation, secure-context gating
c9ff2ff Delta v3 ticket 2: street-lookup conversation (prompts, saved-address transcripts, UI label)
27de272 Delta v3 ticket 1: street-lookup core (lookup_customer, use_saved_street, end-to-end redaction)

codex
The superpowers reference path in the skill is stale, so I’m proceeding with the repository review itself. I’ve confirmed the review range is `27de272..13da540` on `main`; now I’m reading the touched files and tests that carry the SPEC claims.
exec
/bin/bash -lc 'rg -n "as_dict|as_submit_dict|street_from_saved|lookup_customer|set_customer|use_saved_street|no_saved_street|isSecureContext|degradeSpeech|speak|tts|MediaRecorder|getUserMedia|spoken|vendor|model|speech-service" core prompts channels/static tests deploy README decisions/qa.md PLAN.md' in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc 'git diff --stat 27de272..HEAD && git diff --name-only 27de272..HEAD' in /home/rob/bpm-pizza-vibecoding-solution
 exited 2 in 624ms:
rg: README: No such file or directory (os error 2)
tests/test_web_e2e.py:133:    """The 422-shaped tool error reaches the customer as model-phrased
tests/test_web_e2e.py:229:    assert page.locator("#tts-wrap").is_hidden()
tests/test_web_speech.py:4:control visibility, STT round trip, spoken-turn metadata, final-message
tests/test_web_speech.py:42:        "SPEECH_TTS_MODEL": "stub-tts",
tests/test_web_speech.py:83:def test_tts_returns_playable_audio(stack, api):
tests/test_web_speech.py:85:    before = stack["speech"].tts_calls
tests/test_web_speech.py:86:    result = api.post("/speech/tts", json={"session_id": sid,
tests/test_web_speech.py:91:    assert stack["speech"].tts_calls == before + 1
tests/test_web_speech.py:98:        result = api.post("/speech/tts", json={"session_id": sid,
tests/test_web_speech.py:144:    stack["gateway"].saw_spoken_note = False
tests/test_web_speech.py:148:    assert page.locator("#tts-wrap").is_visible()
tests/test_web_speech.py:149:    assert not page.locator("#tts-toggle").is_checked()  # off by default
tests/test_web_speech.py:158:    assert stack["gateway"].saw_spoken_note  # spoken-style note reached model
tests/test_web_speech.py:162:def test_e2e_tts_fetched_once_for_final_message_only(voice_page_factory,
tests/test_web_speech.py:166:    page.check("#tts-toggle")
tests/test_web_speech.py:167:    before = stack["speech"].tts_calls
tests/test_web_speech.py:175:    assert stack["speech"].tts_calls == before + 1
tests/test_web_speech.py:191:        assert page.locator("#tts-wrap").is_hidden()
tests/test_web_speech.py:216:    microphone capture (fake device streaming the spoken-order fixture),
tests/test_web_speech.py:226:    tts_audio = {"bytes": 0}
tests/test_web_speech.py:239:            if response.url.endswith("/speech/tts") and response.ok:
tests/test_web_speech.py:240:                tts_audio["bytes"] = len(response.body())
tests/test_web_speech.py:248:        page.check("#tts-toggle")
tests/test_web_speech.py:264:        assert tts_audio["bytes"] > 0  # real, non-empty playable audio
tests/test_web_speech.py:286:        init_script="Object.defineProperty(window, 'isSecureContext',"
tests/test_web_speech.py:289:    assert page.locator("#tts-wrap").is_hidden()
tests/stubs.py:2:and a stub LLM gateway (a scripted model in the golden-transcript spirit).
tests/stubs.py:92:    """A scripted, deterministic model. mode: 'ok' plays a fixed order
tests/stubs.py:98:        self.saw_spoken_note = False
tests/stubs.py:109:                self.saw_spoken_note = True
tests/stubs.py:138:        self.tts_calls = 0
tests/stubs.py:142:        @app.get("/v1/models")
tests/stubs.py:143:        def models():
tests/stubs.py:155:        async def tts(request: Request):
tests/stubs.py:158:            self.tts_calls += 1
tests/stubs.py:164:    # Skip trailing system messages: spoken turns append the ephemeral
tests/stubs.py:165:    # spoken-style note after the conversation tail.
tests/stubs.py:191:        if name == "set_customer":
tests/stubs.py:216:        return _tool_call("set_customer", {"first_name": "Eva"})
tests/test_tools.py:214:    tools.dispatch(order, menu, fake, "set_customer",
tests/test_tools.py:249:    assert err["message"]  # speakable
tests/test_tools.py:438:    tools.dispatch(order, menu, fake, "set_customer",
tests/test_tools.py:471:def test_lookup_customer_known_and_unknown(menu, fake):
tests/test_tools.py:473:    result = tools.dispatch(Order(), menu, fake, "lookup_customer",
tests/test_tools.py:478:    result = tools.dispatch(Order(), menu, fake, "lookup_customer",
tests/test_tools.py:485:def test_lookup_customer_without_saved_street(menu, fake):
tests/test_tools.py:487:    result = tools.dispatch(Order(), menu, fake, "lookup_customer",
tests/test_tools.py:493:def test_lookup_customer_api_error_is_nonfatal_tool_error(menu, fake):
tests/test_tools.py:495:    result = tools.dispatch(Order(), menu, fake, "lookup_customer",
tests/test_tools.py:500:def test_use_saved_street_copies_in_code(menu, fake):
tests/test_tools.py:503:    result = tools.dispatch(order, menu, fake, "set_customer",
tests/test_tools.py:505:                             "use_saved_street": True})
tests/test_tools.py:510:    assert order.customer.street_from_saved is True
tests/test_tools.py:511:    # redacted view everywhere the model/UI looks
tests/test_tools.py:519:def test_use_saved_street_mutually_exclusive_and_missing(menu, fake):
tests/test_tools.py:521:    result = tools.dispatch(Order(), menu, fake, "set_customer",
tests/test_tools.py:524:                             "use_saved_street": True})
tests/test_tools.py:527:    result = tools.dispatch(Order(), menu, fake, "set_customer",
tests/test_tools.py:529:                             "use_saved_street": True})
tests/test_tools.py:530:    assert result["error"]["code"] == "no_saved_street"
tests/test_tools.py:535:    result = tools.dispatch(order, menu, fake, "set_customer",
tests/test_tools.py:545:    model-visible message."""
tests/test_tools.py:557:        [("lookup_customer", {"first_name": "Marko"})],
tests/test_tools.py:558:        [("set_customer", {"first_name": "Marko",
tests/test_tools.py:559:                           "use_saved_street": True}),
tests/test_tools.py:630:                       model="stub", lang=lang)
tests/test_tools.py:676:def test_spoken_note_is_ephemeral_per_turn():
tests/test_tools.py:677:    """The spoken-style note reaches the model for the spoken turn only —
tests/test_tools.py:687:    agent.run_turn(session, "hallo", spoken=True)
tests/test_tools.py:704:    tools.dispatch(session.order, session.menu, fake, "set_customer",
tests/test_tools.py:721:    # synthetic history is model-shaped: assistant tool_calls + tool result
tests/test_tools.py:742:    # the failed dispatch is in the history exactly like a model call
tests/test_tools.py:763:                              model="stub", lang="de"),
tests/test_tools.py:786:        ("set_customer", {"first_name": "Akzeptanz",
decisions/qa.md:47:`lookup_customer(first_name)` returns booleans only; `set_customer` gains
decisions/qa.md:48:`use_saved_street: true` (mutually exclusive with `street_one`) and the
decisions/qa.md:49:code copies the saved street — the text never reaches the model, stream,
decisions/qa.md:62:**A (decision, 10 points applied):** Acceptance point 5 (spoken
decisions/qa.md:68:is not a valid acceptance environment; MediaRecorder-format in,
decisions/qa.md:83:exercises the identical UI path (getUserMedia + MediaRecorder + upload).
tests/test_state.py:22:    state.set_customer(o, Customer("Marco", "via Roma"))
tests/test_state.py:46:    state.set_customer(o, Customer("Marco", "via Roma"))
tests/test_state.py:60:    state.set_customer(o, Customer("Anna"))
tests/test_state.py:71:    lambda o: state.set_customer(o, Customer("Eve")),
tests/test_state.py:146:def test_set_customer_after_confirmed_demotes():
tests/test_state.py:148:    state.set_customer(o, Customer("Mario"))
tests/test_state.py:194:    state.set_customer(o, Customer("A"))
channels/static/index.html:40:  <label id="tts-wrap" hidden>
channels/static/index.html:41:    <input type="checkbox" id="tts-toggle"> <span id="tts-label"></span>
tests/test_transcripts.py:2:agent loop against a stub model that replays fixed tool calls. Asserts the
tests/test_transcripts.py:89:                         model="stub", lang="de")
tests/test_transcripts.py:124:        assert session.order.customer.street_from_saved == \
tests/test_transcripts.py:127:            # redaction: the saved street never enters the model context
tests/test_transcripts.py:133:    if "set_customer_calls" in expect:
tests/test_transcripts.py:134:        assert calls.count("set_customer") == expect["set_customer_calls"]
tests/test_transcripts.py:136:        # the spoken name is confirmed BEFORE the customer is stored —
tests/test_transcripts.py:142:                       if kind == "call" and value == "set_customer")
tests/test_transcripts.py:161:                         model="stub", lang="en")
channels/static/app.js:3:   Speech: browser captures/plays audio only (MediaRecorder + <audio>);
channels/static/app.js:30:    ttsLabel: "Antworten vorlesen",
channels/static/app.js:33:    ttsFail: "Vorlesen gerade nicht möglich.",
channels/static/app.js:58:    ttsLabel: "Read replies aloud",
channels/static/app.js:61:    ttsFail: "Read-aloud is unavailable right now.",
channels/static/app.js:83:  $("tts-label").textContent = t("ttsLabel");
channels/static/app.js:288:async function sendTurn(text, spoken = false) {
channels/static/app.js:291:    "/chat", { session_id: session.id, text, spoken }, text ?? undefined);
channels/static/app.js:292:  if (finalText && cfg.speech && $("tts-toggle").checked) speak(finalText);
channels/static/app.js:302:  if (finalText && cfg.speech && $("tts-toggle").checked) speak(finalText);
channels/static/app.js:333:  const speechUsable = cfg.speech && window.isSecureContext;
channels/static/app.js:334:  $("tts-wrap").hidden = !speechUsable;
channels/static/app.js:336:                      window.MediaRecorder);
channels/static/app.js:375:  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
channels/static/app.js:376:  recorder = new MediaRecorder(stream);
channels/static/app.js:395:      degradeSpeech();  // runtime outage → text-only for this session
channels/static/app.js:408:async function speak(text) {
channels/static/app.js:410:    const res = await fetch("/speech/tts", {
channels/static/app.js:418:    notice(t("ttsFail"));
channels/static/app.js:419:    degradeSpeech();  // runtime outage → text-only for this session
channels/static/app.js:423:function degradeSpeech() {
channels/static/app.js:425:  $("tts-wrap").hidden = true;
prompts/system.de.md:16:- Erfrage zuerst den Vornamen und rufe dann `lookup_customer` auf. Gibt es
prompts/system.de.md:19:  Bei Ja: `set_customer` mit `use_saved_street: true`. Bei Nein,
prompts/system.en.md:16:- Collect the first name first, then call `lookup_customer`. If a saved
prompts/system.en.md:19:  `set_customer` with `use_saved_street: true`. On no, an unknown name, or
prompts/system.en.md:24:  creates a ghost customer. In spoken conversations, **always** confirm
prompts/system.en.md:41:- When your reply will be spoken aloud: at most three dishes plus an
channels/static/style.css:71:#tts-wrap { font-size: .8rem; color: #555; }
PLAN.md:13:by code, the model only speaks. What moves: everything tenant-, language-
PLAN.md:32:- `core/agent.py` model loop, retry-once, JSONL logging, stub-model seam
PLAN.md:40:| 2. Core-owned session factory, immutable tenant | "Session model v2" |
PLAN.md:61:## Session model v2 (condition 2)
PLAN.md:92:the model (prompt rule) and always wins over the switch, exactly as SPEC
PLAN.md:110:- The model never computes prices: the prompt instructs it to quote
PLAN.md:138:     `tool_call`/`tool_result`/`state` events. The model's context and
PLAN.md:139:     the JSONL log are identical in shape to a model-initiated call.
PLAN.md:140:  3. One model call then phrases the outcome to the customer — the order
PLAN.md:143:     again"), exactly the SPEC's "the refusal is a tool result the model
PLAN.md:158:- CLI keeps the conversational path: customer says yes → model calls
PLAN.md:187:  model call anywhere; every gateway call by any session through either
PLAN.md:197:  `SpeechService` class (config, probe, stt(audio, lang), tts(text,
PLAN.md:208:- Spoken-answer policy: `POST /chat` gains optional `spoken: true`, set by
PLAN.md:210:  Core appends a one-line per-turn note instructing spoken style (≤3 menu
PLAN.md:251:  parser-shaped guess, and model replies already mirror per turn); the
PLAN.md:278:  tool-level errors reach the customer as model-phrased plain language
PLAN.md:279:  (the model receives the speakable `message`), transport-level failures
PLAN.md:295:  and **stub gateway** (scripted tool-calling model) served locally;
PLAN.md:380:## A. Street lookup (SPEC: lookup_customer / use_saved_street / redaction)
PLAN.md:387:- `core/order.py`: `Customer` gains `street_from_saved: bool = False`.
PLAN.md:389:  - `as_dict()` (used by SNAPSHOT, hence by every tool result, streamed
PLAN.md:390:    event, transcript and log line): when `street_from_saved`, it carries
PLAN.md:394:  - `as_submit_dict()` (used only to build the POST /orders body): always
PLAN.md:398:  - New tool `lookup_customer` `{first_name}` →
PLAN.md:401:    uniform error shape with code `api_unavailable` (non-fatal; the model
PLAN.md:403:  - `set_customer` params become `{first_name, street_one?,
PLAN.md:404:    use_saved_street?}` — mutually exclusive; both set → error code
PLAN.md:405:    `invalid_arguments` with a speakable message. With the flag, dispatch
PLAN.md:407:    `street_from_saved`; unknown name or no saved street → error
PLAN.md:408:    `no_saved_street` (speakable), basket untouched.
PLAN.md:409:  - `_submit` switches from `as_dict()` to `as_submit_dict()`.
PLAN.md:410:- Prompts (both languages): after the name, call `lookup_customer`; if a
PLAN.md:412:  reciting the address; yes → `set_customer(use_saved_street: true)`;
PLAN.md:421:- `use_saved_street` copies in code; the redaction sweep is end to end:
PLAN.md:425:  `session.messages`** (the model-visible tool-message serialization is
PLAN.md:427:  content the model reads must fail this test). The same sweep covers
PLAN.md:430:- Mutual exclusion + `no_saved_street` paths.
PLAN.md:432:  question → flag-based set_customer → order) and decline/fallback
PLAN.md:439:- `deploy/speech-service.compose.yml`: neutral, CPU-only service
PLAN.md:440:  definition — image and models come from environment placeholders
PLAN.md:441:  (`SPEECH_IMAGE`, `SPEECH_*`), no vendor or model names in the file, and
PLAN.md:445:- `tests/fixtures/audio/`: generated spoken fixtures (offline synthesis
PLAN.md:449:  voice test (content = a spoken order).
PLAN.md:450:- `tests/stubs.py`: `StubSpeech` — `GET /v1/models` 200;
PLAN.md:460:  language; `/speech/tts` returns audio bytes; both 404 when speech is
PLAN.md:467:  click-start/click-stop records via real `MediaRecorder` (the fake
PLAN.md:469:  drives a turn (`spoken: true` asserted via the stub gateway seeing the
PLAN.md:470:  spoken-style note); with the toggle ON, exactly one TTS fetch per turn
PLAN.md:482:  controls render only when `window.isSecureContext` is true (HTTPS or
PLAN.md:484:  init script forces `isSecureContext = false` → with speech fully
PLAN.md:489:  1. plausible-but-wrong spoken name: agent repeats the name back, the
PLAN.md:490:     customer corrects, `set_customer` is called exactly once with the
PLAN.md:492:  2. spoken happy path, dictated street: the name is confirmed before
PLAN.md:494:  3. spoken happy path, saved street reused: the name is confirmed before
PLAN.md:496:  Prompts (both languages) state explicitly: in spoken conversations the
PLAN.md:530:   trip with session lang ☑ tts bytes ☑ 404 when unconfigured.
PLAN.md:537:   ☑ spoken happy path, dictated street: name confirmed before submit
PLAN.md:538:   ☑ spoken happy path, saved street: name confirmed in addition to the
PLAN.md:541:   ☑ neutral (no vendor/model names) ☑ HTTPS requirement documented.
tests/transcripts/saved_address.json:8:       {"tool": "lookup_customer", "args": {"first_name": "Marko"}},
tests/transcripts/saved_address.json:13:       {"tool": "set_customer", "args": {"first_name": "Marko", "use_saved_street": true}},
tests/transcripts/saved_address.json:26:    "calls": ["add_items", "lookup_customer", "set_customer", "read_back", "confirm_order", "submit_order"],
tests/transcripts/unknown_item.json:17:       {"tool": "set_customer", "args": {"first_name": "Luca", "street_one": "via Milano 2"}},
tests/transcripts/unknown_item.json:30:    "calls": ["add_items", "add_items", "set_customer", "read_back", "confirm_order", "submit_order"],
tests/transcripts/mind_change.json:8:       {"tool": "set_customer", "args": {"first_name": "Sara", "street_one": "via Napoli 9"}},
tests/transcripts/mind_change.json:28:    "calls": ["add_items", "set_customer", "read_back", "add_items", "confirm_order", "read_back", "confirm_order", "submit_order"],
core/state.py:3:Illegal transitions raise TransitionError with a typed code and a speakable
core/state.py:62:    the result lets the model repair anything else by remove + re-add."""
core/state.py:83:def set_customer(order: Order, customer: Customer) -> None:
tests/transcripts/spoken_wrong_name.json:2:  "name": "spoken_wrong_name_corrected",
tests/transcripts/spoken_wrong_name.json:12:       {"tool": "set_customer", "args": {"first_name": "Eva", "street_one": "via Roma 1"}},
tests/transcripts/spoken_wrong_name.json:25:    "calls": ["add_items", "set_customer", "read_back", "confirm_order", "submit_order"],
tests/transcripts/spoken_wrong_name.json:29:    "set_customer_calls": 1,
core/order.py:29:    # computed here in core only — the model never does arithmetic.
core/order.py:46:    street_from_saved: bool = False
core/order.py:48:    def as_dict(self) -> dict:
core/order.py:50:        streamed event, model-visible message and log line."""
core/order.py:51:        if self.street_from_saved:
core/order.py:56:    def as_submit_dict(self) -> dict:
core/order.py:96:            "customer": self.customer.as_dict() if self.customer else None,
tests/transcripts/submit_timeout.json:8:       {"tool": "set_customer", "args": {"first_name": "Nino", "street_one": "via Genova 1"}},
tests/transcripts/submit_timeout.json:26:    "calls": ["add_items", "set_customer", "read_back", "confirm_order", "submit_order", "submit_order"],
deploy/speech-service.compose.yml:3:# Neutral by design (SPEC): the image and the models are operator
deploy/speech-service.compose.yml:4:# configuration — no vendor or model names live in this repository.
deploy/speech-service.compose.yml:8:#   POST /v1/audio/transcriptions   multipart: file, model, language -> {"text": ...}
deploy/speech-service.compose.yml:9:#   POST /v1/audio/speech           JSON: model, voice, input -> audio bytes
deploy/speech-service.compose.yml:10:#   GET  /v1/models                 2xx = alive (used by the app's startup probe)
core/tools.py:1:"""The eight tool schemas the model sees, plus dispatch.
core/tools.py:4:{"error": {"code", "message", "candidates"}} with a speakable message.
core/tools.py:56:    {"name": "lookup_customer",
core/tools.py:66:    {"name": "set_customer",
core/tools.py:68:                    "pass street_one, or pass use_saved_street=true after "
core/tools.py:75:                        "use_saved_street": {"type": "boolean"}},
core/tools.py:136:    result the model must deal with in front of the customer."""
core/tools.py:185:    if name == "lookup_customer":
core/tools.py:195:    if name == "set_customer":
core/tools.py:200:        if args.get("use_saved_street"):
core/tools.py:208:                    "no_saved_street",
core/tools.py:215:                                street_from_saved=True)
core/tools.py:218:        state.set_customer(order, customer)
core/tools.py:219:        return {"customer": customer.as_dict(),
core/tools.py:295:    customer = order.customer.as_submit_dict()
tests/transcripts/spoken_happy_dictated_street.json:2:  "name": "spoken_happy_dictated_street_confirms_name",
tests/transcripts/spoken_happy_dictated_street.json:8:       {"tool": "lookup_customer", "args": {"first_name": "Nina"}},
tests/transcripts/spoken_happy_dictated_street.json:13:       {"tool": "set_customer", "args": {"first_name": "Nina", "street_one": "via Milano 3"}},
tests/transcripts/spoken_happy_dictated_street.json:26:    "calls": ["add_items", "lookup_customer", "set_customer", "read_back", "confirm_order", "submit_order"],
tests/transcripts/correction.json:17:       {"tool": "set_customer", "args": {"first_name": "Anna"}},
tests/transcripts/correction.json:30:    "calls": ["add_items", "add_items", "set_customer", "read_back", "confirm_order", "submit_order"],
tests/transcripts/spoken_happy_saved_street.json:2:  "name": "spoken_happy_saved_street_still_confirms_name",
tests/transcripts/spoken_happy_saved_street.json:8:       {"tool": "lookup_customer", "args": {"first_name": "Marko"}},
tests/transcripts/spoken_happy_saved_street.json:17:       {"tool": "set_customer", "args": {"first_name": "Marko", "use_saved_street": true}},
tests/transcripts/spoken_happy_saved_street.json:30:    "calls": ["add_items", "lookup_customer", "set_customer", "read_back", "confirm_order", "submit_order"],
core/agent.py:2:JSONL event logging. The model only speaks; the order lives in core.
core/agent.py:38:    "en": "This reply will be spoken aloud: name at most three dishes, "
core/agent.py:51:    model: str
core/agent.py:61:        optional_env("LITELLM_PIZZA_MODEL_2")  # read; unused (single-model)
core/agent.py:65:            model=require_env("LITELLM_PIZZA_MODEL_1"),
core/agent.py:156:            "model": self.config.model,
core/agent.py:183:                 emit=lambda event: None, spoken: bool = False) -> str:
core/agent.py:186:        is the opening/continuation turn — the agent speaks unprompted."""
core/agent.py:195:        # Ephemeral per-turn note: activates the spoken-style policy that
core/agent.py:197:        # not inherit the spoken constraints.
core/agent.py:199:                 if spoken else [])
core/agent.py:254:        """One UI-initiated dispatch, recorded exactly like a model call:
tests/transcripts/saved_address_decline.json:8:       {"tool": "lookup_customer", "args": {"first_name": "Marko"}},
tests/transcripts/saved_address_decline.json:13:       {"tool": "set_customer", "args": {"first_name": "Marko", "street_one": "via Nuova 2"}},
tests/transcripts/saved_address_decline.json:26:    "calls": ["add_items", "lookup_customer", "set_customer", "read_back", "confirm_order", "submit_order"],
tests/transcripts/happy_path.json:17:       {"tool": "set_customer", "args": {"first_name": "Marco", "street_one": "via Roma 5"}},
tests/transcripts/happy_path.json:30:    "calls": ["get_menu", "add_items", "set_customer", "read_back", "confirm_order", "submit_order"],

 succeeded in 681ms:
 PLAN.md                                            |  41 +--
 README.md                                          |  23 +-
 channels/static/app.js                             |  19 +-
 decisions/qa.md                                    |  12 +
 deploy/speech-service.compose.yml                  |  27 ++
 prompts/system.de.md                               |  14 +-
 prompts/system.en.md                               |  14 +-
 tests/fixtures/audio/order.de.wav                  | Bin 0 -> 242156 bytes
 tests/fixtures/audio/order.en.wav                  | Bin 0 -> 224452 bytes
 tests/stubs.py                                     |  56 +++-
 tests/test_transcripts.py                          |  40 ++-
 tests/test_web_speech.py                           | 293 +++++++++++++++++++++
 tests/transcripts/saved_address.json               |  31 +++
 tests/transcripts/saved_address_decline.json       |  31 +++
 .../transcripts/spoken_happy_dictated_street.json  |  32 +++
 tests/transcripts/spoken_happy_saved_street.json   |  37 +++
 tests/transcripts/spoken_wrong_name.json           |  32 +++
 17 files changed, 667 insertions(+), 35 deletions(-)
PLAN.md
README.md
channels/static/app.js
decisions/qa.md
deploy/speech-service.compose.yml
prompts/system.de.md
prompts/system.en.md
tests/fixtures/audio/order.de.wav
tests/fixtures/audio/order.en.wav
tests/stubs.py
tests/test_transcripts.py
tests/test_web_speech.py
tests/transcripts/saved_address.json
tests/transcripts/saved_address_decline.json
tests/transcripts/spoken_happy_dictated_street.json
tests/transcripts/spoken_happy_saved_street.json
tests/transcripts/spoken_wrong_name.json

codex
I have the file map and the main symbols. Next I’m checking the actual implementations and test assertions around redaction, prompt policy, browser degradation, and the live voice acceptance path.
exec
/bin/bash -lc "sed -n '1,360p' core/tools.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,240p' core/order.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' core/agent.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,220p' core/pizzasim.py" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 1574ms:
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
    # True when street_one was copied from saved customer data: the text
    # then never appears in snapshots, events, transcripts or logs — only
    # in the outbound submit payload (SPEC saved-street redaction).
    street_from_saved: bool = False

    def as_dict(self) -> dict:
        """Redacted view: feeds SNAPSHOT and thereby every tool result,
        streamed event, model-visible message and log line."""
        if self.street_from_saved:
            return {"first_name": self.first_name, "street_one": None,
                    "street_on_file": True}
        return {"first_name": self.first_name, "street_one": self.street_one}

    def as_submit_dict(self) -> dict:
        """The real thing — used only to build the POST /orders body."""
        body = {"first_name": self.first_name}
        if self.street_one:
            body["street_one"] = self.street_one
        return body


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

 succeeded in 1435ms:
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
        self.base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._transport = transport
        self._client = httpx.Client(
            base_url=self.base_url,
            headers={"X-API-Key": api_key},
            timeout=_TIMEOUT,
            transport=transport,
        )

    def for_pizzeria(self, pizzeria_id: str) -> "PizzaSim":
        """Tenant-bound sibling client — same server, same key. Used by the
        session factory; a session's tenant never changes afterwards."""
        return PizzaSim(self.base_url, self._api_key, pizzeria_id,
                        transport=self._transport)

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

    def list_customers(self) -> list[dict]:
        """Customer list — used only for address-reuse lookup, never to
        disclose address text (SPEC). Deleted customers are filtered."""
        customers = self._request(
            "GET", f"/pizzerias/{self.pizzeria_id}/customers"
        )["customers"]
        return [c for c in customers if not c.get("deleted_at")]

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

 succeeded in 1751ms:
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
    {"name": "lookup_customer",
     "description": "Check whether a first name is a known customer with "
                    "a saved street. Returns booleans only — never the "
                    "address itself. Use after the customer gave their "
                    "name; on a saved street, ask whether to deliver to "
                    "the saved address without reciting it.",
     "parameters": {"type": "object",
                    "properties": {
                        "first_name": {"type": "string", "minLength": 1}},
                    "required": ["first_name"]}},
    {"name": "set_customer",
     "description": "Store the customer's first name and street. Either "
                    "pass street_one, or pass use_saved_street=true after "
                    "the customer confirmed delivery to their saved "
                    "address — never both.",
     "parameters": {"type": "object",
                    "properties": {
                        "first_name": {"type": "string", "minLength": 1},
                        "street_one": {"type": "string"},
                        "use_saved_street": {"type": "boolean"}},
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


def _saved_customer(client: PizzaSim, first_name: str) -> dict | None:
    """Case-insensitive match on the unique-per-pizzeria first name.
    Deleted customers are already filtered by the client. Raises
    PizzaSimError upward — dispatch maps it to api_unavailable, which the
    prompt treats as non-fatal (fall back to asking for the street)."""
    for record in client.list_customers():
        if record.get("first_name", "").lower() == first_name.lower():
            return record
    return None


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

    if name == "lookup_customer":
        first_name = (args.get("first_name") or "").strip()
        if not first_name:
            return _error("invalid_arguments", "I still need a name.")
        record = _saved_customer(client, first_name)
        return {"customer_exists": record is not None,
                "saved_street_available": bool(record
                                               and record.get("street_one")),
                "snapshot": order.snapshot()}

    if name == "set_customer":
        first_name = (args.get("first_name") or "").strip()
        if not first_name:
            return _error("invalid_state", "I still need a name.")
        street = args.get("street_one") or None
        if args.get("use_saved_street"):
            if street:
                return _error(
                    "invalid_arguments",
                    "Either a street or the saved address — not both.")
            record = _saved_customer(client, first_name)
            if not record or not record.get("street_one"):
                return _error(
                    "no_saved_street",
                    "I don't have a saved address under that name — "
                    "what's the street?")
            # The code copies the saved street; canonical name casing from
            # the record prevents a ghost-customer near-duplicate.
            customer = Customer(record["first_name"],
                                record["street_one"],
                                street_from_saved=True)
        else:
            customer = Customer(first_name, street)
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

    customer = order.customer.as_submit_dict()
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

 succeeded in 1465ms:
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

exec
/bin/bash -lc "sed -n '260,360p' core/agent.py" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 248ms:
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

exec
/bin/bash -lc "sed -n '1,220p' prompts/system.de.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,220p' prompts/system.en.md" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,520p' channels/static/app.js" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "rg -n \"customer\\.|as_dict\\(|as_submit_dict\\(|street_one|street_on_file|json.dumps\\(result|snapshot\\(|submit_order\\(|submit payload|orders body|tool_result\" core tests -g '"'!tests/fixtures/**'"'" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 314ms:
Du nimmst telefonisch und im Chat Bestellungen für {pizzeria_name} entgegen.

Deine einzige Aufgabe: verstehen, was der Gast möchte, und es über die
Werkzeuge in die Bestellung übertragen. Die Bestellung selbst verwaltet das
System — du hältst sie nie selbst im Kopf, du erfindest nie Gerichte, und du
verlässt dich bei jedem Artikel auf `get_menu`.

Ablauf:

- Begrüße den Gast zuerst auf Deutsch, in einem Satz, und biete deine Hilfe
  an. Keine Speisekarten-Aufzählung.
- Antworte danach in jeder Runde in der Sprache der letzten Nachricht des
  Gastes (Deutsch oder Englisch), ohne darauf hinzuweisen.
- Stelle pro Runde genau eine Frage.
- Nenne nur Gerichte, die in dieser Sitzung aus `get_menu` kamen.
- Erfrage zuerst den Vornamen und rufe dann `lookup_customer` auf. Gibt es
  eine gespeicherte Adresse, stelle genau eine Frage: „Soll ich wieder an
  Ihre gespeicherte Adresse liefern?" — **ohne die Adresse zu nennen**.
  Bei Ja: `set_customer` mit `use_saved_street: true`. Bei Nein,
  unbekanntem Namen oder fehlgeschlagenem Lookup: frage wie gewohnt nach
  der Straße. Nenne niemals eine Straße, die aus gespeicherten Daten
  stammt. Lehnt der Gast die Straße ganz ab, geht es ohne sie weiter.
- Wiederhole den Vornamen einmal zur Bestätigung — ein falsch verstandener
  Name legt einen Geisterkunden an. In gesprochenen Gesprächen bestätige
  den Vornamen **immer**, bevor die Bestellung abgeschickt wird; die Frage
  zur gespeicherten Adresse ersetzt diese Bestätigung nicht.
- Vor dem Abschicken: rufe `read_back` auf, lies die Bestellung vor und
  warte auf ein klares Ja. „Mhm" oder Schweigen gilt nicht — frag einmal
  nach, danach biete an, neu zu beginnen.
- Sage niemals, die Bestellung sei abgeschickt, bevor `submit_order` eine
  Bestellnummer zurückgegeben hat.
- Nach dem Abschicken: nenne die Bestellnummer in gut nachsprechbaren
  Gruppen und die Wartezeit in Minuten (aus `eta_seconds` umgerechnet).
- Bei Fehlern erkläre in Alltagssprache, was passiert ist und welche
  Möglichkeiten der Gast hat. Nie Statuscodes, nie JSON.
- Behaupte nie, eine Adresse auf Lieferbarkeit geprüft zu haben.
- Mengen übergibst du den Werkzeugen immer als Zahl (3, nicht „drei").
- Preisfragen sind normale Fragen. Nenne Preise und die Korbsumme wörtlich
  aus den Werkzeug-Ergebnissen (`price`, `basket_total`) — du rechnest nie
  selbst und erfindest keine Beträge.
- Wenn deine Antwort vorgelesen wird: höchstens drei Gerichte nennen und
  zum Nachfragen einladen, Zeiten in Minuten, kurze Sätze.

Wenn ein Werkzeug einen Fehler meldet, richte dich danach: schlage die
genannten Alternativen vor oder stelle die fehlende Frage. Das System hat
immer recht.

 succeeded in 439ms:
You take orders for {pizzeria_name} over the phone and in chat.

Your only job: understand what the customer wants and put it into the order
through the tools. The system owns the order — you never keep it in your
head, you never invent menu items, and every item you mention comes from
`get_menu`.

How to work:

- Greet the customer first in English, in one sentence, and offer to help.
  No menu recital.
- From then on, answer each turn in the language of the customer's latest
  message (German or English), without commenting on the switch.
- Ask exactly one question per turn.
- Only name dishes that came from `get_menu` in this session.
- Collect the first name first, then call `lookup_customer`. If a saved
  street exists, ask exactly one question: "Shall I deliver to your saved
  address again?" — **without reciting the address**. On yes: call
  `set_customer` with `use_saved_street: true`. On no, an unknown name, or
  a failed lookup: ask for the street as usual. Never state a street that
  came from saved data. If the customer declines the street entirely, move
  on without it.
- Repeat the first name back once to confirm it — a misheard name silently
  creates a ghost customer. In spoken conversations, **always** confirm
  the first name before the order is submitted; the saved-address question
  does not replace that confirmation.
- Before submitting: call `read_back`, say it out loud, and wait for an
  explicit yes. "Mhm" or silence is not a yes — ask once more, then offer
  to start over.
- Never say the order was placed before `submit_order` returned an order
  number.
- After submitting: state the order number in groups that are easy to
  repeat, and the wait time in minutes (converted from `eta_seconds`).
- On errors, explain in plain language what happened and what the customer
  can do. Never show status codes or JSON.
- Never claim to have checked an address for deliverability.
- Always pass quantities to tools as numbers (3, not "three").
- Price questions are normal questions. Quote prices and the basket total
  verbatim from tool results (`price`, `basket_total`) — never do the
  arithmetic yourself, never invent an amount.
- When your reply will be spoken aloud: at most three dishes plus an
  invitation to ask for more, times in minutes, short sentences.

When a tool reports an error, follow it: offer the suggested alternatives
or ask the missing question. The system is always right.

 succeeded in 448ms:
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
    savedAddress: "gespeicherte Adresse",
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
    savedAddress: "saved address",
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
      (snapshot.customer.street_on_file
        ? `, ${t("savedAddress")}`  // never the saved text (SPEC redaction)
        : snapshot.customer.street_one
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
  // Voice UI only in a secure context (HTTPS/localhost): plain HTTP must
  // never present a voice-capable UI (SPEC).
  const speechUsable = cfg.speech && window.isSecureContext;
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
      degradeSpeech();  // runtime outage → text-only for this session
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
    degradeSpeech();  // runtime outage → text-only for this session
  }
}

function degradeSpeech() {
  $("mic").hidden = true;
  $("tts-wrap").hidden = true;
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

 succeeded in 511ms:
core/menu.py:29:    def as_tool_result(self) -> dict:
core/agent.py:235:                event({"type": "tool_result", "tool": name,
core/agent.py:243:                    "content": json.dumps(result, ensure_ascii=False),
core/agent.py:267:        event({"type": "tool_result", "tool": name, "result": result})
core/agent.py:273:            "content": json.dumps(result, ensure_ascii=False),
core/pizzasim.py:161:    def submit_order(self, customer: dict, items: list[dict]) -> dict:
core/order.py:42:    street_one: str | None = None
core/order.py:43:    # True when street_one was copied from saved customer data: the text
core/order.py:45:    # in the outbound submit payload (SPEC saved-street redaction).
core/order.py:48:    def as_dict(self) -> dict:
core/order.py:52:            return {"first_name": self.first_name, "street_one": None,
core/order.py:53:                    "street_on_file": True}
core/order.py:54:        return {"first_name": self.first_name, "street_one": self.street_one}
core/order.py:56:    def as_submit_dict(self) -> dict:
core/order.py:57:        """The real thing — used only to build the POST /orders body."""
core/order.py:59:        if self.street_one:
core/order.py:60:            body["street_one"] = self.street_one
core/order.py:75:    def snapshot(self) -> dict:
core/order.py:96:            "customer": self.customer.as_dict() if self.customer else None,
core/tools.py:68:                    "pass street_one, or pass use_saved_street=true after "
core/tools.py:74:                        "street_one": {"type": "string"},
core/tools.py:136:    result the model must deal with in front of the customer."""
core/tools.py:157:        return {"menu": menu.as_tool_result(), "snapshot": order.snapshot()}
core/tools.py:177:        return {"snapshot": order.snapshot()}
core/tools.py:183:        return {"snapshot": order.snapshot()}
core/tools.py:192:                                               and record.get("street_one")),
core/tools.py:193:                "snapshot": order.snapshot()}
core/tools.py:199:        street = args.get("street_one") or None
core/tools.py:206:            if not record or not record.get("street_one"):
core/tools.py:214:                                record["street_one"],
core/tools.py:219:        return {"customer": customer.as_dict(),
core/tools.py:220:                "snapshot": order.snapshot()}
core/tools.py:224:        return {"snapshot": order.snapshot()}
core/tools.py:232:        return {"snapshot": order.snapshot()}
core/tools.py:241:                "snapshot": order.snapshot()}
core/tools.py:276:            if o.get("first_name") == order.customer.first_name
core/tools.py:292:                return {**order.result, "snapshot": order.snapshot()}
core/tools.py:295:    customer = order.customer.as_submit_dict()
core/tools.py:299:        result = client.submit_order(customer, items)
core/tools.py:316:    return {**order.result, "snapshot": order.snapshot()}
tests/test_tools.py:98:        ).submit_order({"first_name": "X"}, [])
tests/test_tools.py:127:    result = client.submit_order({"first_name": "Marco"}, [])
tests/test_tools.py:135:    result = menu.as_tool_result()
tests/test_tools.py:150:    snap = order.snapshot()
tests/test_tools.py:162:    snap = order.snapshot()
tests/test_tools.py:180:    def submit_order(self, customer, items):
tests/test_tools.py:215:                   {"first_name": "Marco", "street_one": "via Roma"})
tests/test_tools.py:228:def test_every_success_carries_full_snapshot(menu, fake):
tests/test_tools.py:467:         "street_one": "Meyer Teststraße 4", "street_two": None,
tests/test_tools.py:477:    assert "Meyer" not in json.dumps(result)  # booleans only, never text
tests/test_tools.py:486:    fake.customers = [{**SAVED, "street_one": None}]
tests/test_tools.py:508:    assert order.customer.first_name == "Marko"
tests/test_tools.py:509:    assert order.customer.street_one == "Meyer Teststraße 4"
tests/test_tools.py:510:    assert order.customer.street_from_saved is True
tests/test_tools.py:513:                                  "street_one": None,
tests/test_tools.py:514:                                  "street_on_file": True}
tests/test_tools.py:515:    assert result["snapshot"]["customer"]["street_on_file"] is True
tests/test_tools.py:516:    assert "Meyer" not in json.dumps(result)
tests/test_tools.py:523:                             "street_one": "via Roma",
tests/test_tools.py:537:                             "street_one": "via Roma 1"})
tests/test_tools.py:538:    assert result["customer"]["street_one"] == "via Roma 1"  # own input
tests/test_tools.py:539:    assert "street_on_file" not in result["customer"]
tests/test_tools.py:544:    submit payload. Not in any snapshot, emitted event, log line, or
tests/test_tools.py:585:    assert captured["customer"]["street_one"] == street  # the ONE place
tests/test_tools.py:738:              if e["type"] == "tool_result" and "error" in e["result"]]
tests/test_tools.py:787:                          "street_one": "via Verdi 7"}),
tests/test_web_e2e.py:140:    errors = [e for e in events if e["type"] == "tool_result"
tests/test_web_e2e.py:157:                if e["type"] == "tool_result"
tests/test_web_e2e.py:163:                 if e["type"] == "tool_result"
tests/test_web_e2e.py:184:              if e["type"] == "tool_result" and "error" in e["result"]]
tests/transcripts/saved_address_decline.json:13:       {"tool": "set_customer", "args": {"first_name": "Marko", "street_one": "via Nuova 2"}},
tests/transcripts/spoken_happy_dictated_street.json:13:       {"tool": "set_customer", "args": {"first_name": "Nina", "street_one": "via Milano 3"}},
tests/transcripts/spoken_wrong_name.json:12:       {"tool": "set_customer", "args": {"first_name": "Eva", "street_one": "via Roma 1"}},
tests/transcripts/happy_path.json:17:       {"tool": "set_customer", "args": {"first_name": "Marco", "street_one": "via Roma 5"}},
tests/transcripts/mind_change.json:8:       {"tool": "set_customer", "args": {"first_name": "Sara", "street_one": "via Napoli 9"}},
tests/transcripts/submit_timeout.json:8:       {"tool": "set_customer", "args": {"first_name": "Nino", "street_one": "via Genova 1"}},
tests/transcripts/unknown_item.json:17:       {"tool": "set_customer", "args": {"first_name": "Luca", "street_one": "via Milano 2"}},
tests/test_transcripts.py:52:    def submit_order(self, customer, items):
tests/test_transcripts.py:76:                 "street_one": "Meyer Teststraße 4", "street_two": None,
tests/test_transcripts.py:104:        if event["type"] == "tool_result" and "error" in event["result"]:
tests/test_transcripts.py:124:        assert session.order.customer.street_from_saved == \
tests/test_transcripts.py:131:        assert session.order.customer.first_name == \

exec
/bin/bash -lc "sed -n '430,620p' tests/test_tools.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' tests/test_transcripts.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,360p' tests/test_web_speech.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,260p' tests/stubs.py" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 445ms:
    assert not order.submit_unknown  # not the retry path


def test_street_omitted_from_submit_body(menu, fake):
    order = Order()
    tools.dispatch(order, menu, fake, "add_items",
                   {"items": [{"type": "pizza", "code": "margherita",
                               "qty": 1}]})
    tools.dispatch(order, menu, fake, "set_customer",
                   {"first_name": "Anna"})  # street declined
    tools.dispatch(order, menu, fake, "read_back", {})
    tools.dispatch(order, menu, fake, "confirm_order",
                   {"revision": order.revision})
    captured = {}

    def submit_effect():
        return fixture("order_created.json")
    fake.submit_effect = submit_effect
    real_submit = fake.submit_order

    def spy(customer, items):
        captured.update(customer=customer, items=items)
        return real_submit(customer, items)
    fake.submit_order = spy
    tools.dispatch(order, menu, fake, "submit_order", {})
    assert captured["customer"] == {"first_name": "Anna"}


def test_check_street(menu, fake):
    result = tools.dispatch(Order(), menu, fake, "check_street",
                            {"street": "via Roma"})
    assert result["deliverable"] is True and "snapshot" in result


# --- street lookup for returning customers (delta v3 ticket 1) ------------

SAVED = {"id": "c-1", "first_name": "Marko",
         "street_one": "Meyer Teststraße 4", "street_two": None,
         "created_at": 1, "deleted_at": None}


def test_lookup_customer_known_and_unknown(menu, fake):
    fake.customers = [SAVED]
    result = tools.dispatch(Order(), menu, fake, "lookup_customer",
                            {"first_name": "marko"})  # case-insensitive
    assert result["customer_exists"] is True
    assert result["saved_street_available"] is True
    assert "Meyer" not in json.dumps(result)  # booleans only, never text
    result = tools.dispatch(Order(), menu, fake, "lookup_customer",
                            {"first_name": "Nessuno"})
    assert result == {"customer_exists": False,
                      "saved_street_available": False,
                      "snapshot": result["snapshot"]}


def test_lookup_customer_without_saved_street(menu, fake):
    fake.customers = [{**SAVED, "street_one": None}]
    result = tools.dispatch(Order(), menu, fake, "lookup_customer",
                            {"first_name": "Marko"})
    assert result["customer_exists"] is True
    assert result["saved_street_available"] is False


def test_lookup_customer_api_error_is_nonfatal_tool_error(menu, fake):
    fake.customers_effect = ApiTimeout("t")
    result = tools.dispatch(Order(), menu, fake, "lookup_customer",
                            {"first_name": "Marko"})
    assert result["error"]["code"] == "api_unavailable"


def test_use_saved_street_copies_in_code(menu, fake):
    fake.customers = [SAVED]
    order = Order()
    result = tools.dispatch(order, menu, fake, "set_customer",
                            {"first_name": "marko",
                             "use_saved_street": True})
    assert "error" not in result
    # canonical casing from the record — no ghost near-duplicate
    assert order.customer.first_name == "Marko"
    assert order.customer.street_one == "Meyer Teststraße 4"
    assert order.customer.street_from_saved is True
    # redacted view everywhere the model/UI looks
    assert result["customer"] == {"first_name": "Marko",
                                  "street_one": None,
                                  "street_on_file": True}
    assert result["snapshot"]["customer"]["street_on_file"] is True
    assert "Meyer" not in json.dumps(result)


def test_use_saved_street_mutually_exclusive_and_missing(menu, fake):
    fake.customers = [SAVED]
    result = tools.dispatch(Order(), menu, fake, "set_customer",
                            {"first_name": "Marko",
                             "street_one": "via Roma",
                             "use_saved_street": True})
    assert result["error"]["code"] == "invalid_arguments"
    fake.customers = []
    result = tools.dispatch(Order(), menu, fake, "set_customer",
                            {"first_name": "Marko",
                             "use_saved_street": True})
    assert result["error"]["code"] == "no_saved_street"


def test_dictated_street_still_echoed_and_submitted(menu, fake):
    order = Order()
    result = tools.dispatch(order, menu, fake, "set_customer",
                            {"first_name": "Anna",
                             "street_one": "via Roma 1"})
    assert result["customer"]["street_one"] == "via Roma 1"  # own input
    assert "street_on_file" not in result["customer"]


def test_saved_street_redaction_end_to_end(menu, fake):
    """The saved street text appears in exactly ONE place: the outbound
    submit payload. Not in any snapshot, emitted event, log line, or
    model-visible message."""
    from core.agent import Agent, LOG_DIR, Session as AgentSession
    fake.customers = [SAVED]
    captured = {}
    real_submit = fake.submit_order

    def spy(customer, items):
        captured["customer"] = customer
        return real_submit(customer, items)
    fake.submit_order = spy

    script = iter([
        [("lookup_customer", {"first_name": "Marko"})],
        [("set_customer", {"first_name": "Marko",
                           "use_saved_street": True}),
         ("add_items", {"items": [{"type": "pizza", "code": "margherita",
                                   "qty": 1}]}),
         ("read_back", {})],
    ])

    def stub(messages, tool_schemas):
        calls = next(script, None)
        if calls:
            return {"tool_calls": [
                {"id": f"c-{name}", "type": "function",
                 "function": {"name": name, "arguments": json.dumps(args)}}
                for name, args in calls]}
        return {"content": "Passt das so?"}

    session = AgentSession(order=Order(), menu=menu,
                           messages=[{"role": "system", "content": "s"}],
                           client=fake)
    agent = Agent(config_stub(), chat_fn=stub)
    events = []
    agent.run_turn(session, "Ich heiße Marko", events.append)
    agent.run_turn(session, "Eine Margherita, gespeicherte Adresse",
                   events.append)
    agent.confirm_and_submit(session, session.order.revision, events.append)

    street = "Meyer Teststraße 4"
    assert captured["customer"]["street_one"] == street  # the ONE place
    assert street not in json.dumps(events, ensure_ascii=False)
    assert street not in json.dumps(session.messages, ensure_ascii=False)
    log_text = "".join(
        f.read_text() for f in LOG_DIR.glob(f"agent-{session.id}.jsonl"))
    assert street not in log_text
    assert session.order.state is State.SUBMITTED


# --- session factory, language, confirm path (tickets 2-4) ----------------

from core.agent import (  # noqa: E402
    Agent,
    AgentConfig,
    GatewayError,
    create_session,
    set_language,
)


class FakeBase(FakeClient):
    """FakeClient plus the tenant-free surface the session factory uses."""

    def __init__(self, pizzerias=None):
        super().__init__()
        self.pizzeria_id = "pz-default"
        self.pizzerias = pizzerias or [
            {"id": "pz-default", "name": "Pizzeria Default"},
            {"id": "pz-two", "name": "Pizzeria Two"},
        ]

    def list_pizzerias(self):
        return self.pizzerias

    def get_menu(self):
        return fixture("menu.json")

 succeeded in 441ms:
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

    def list_customers(self):
        return [{"id": "c-1", "first_name": "Marko",
                 "street_one": "Meyer Teststraße 4", "street_two": None,
                 "created_at": 1, "deleted_at": None}]

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

    calls, error_codes, ordered = [], [], []

    def emit(event):
        if event["type"] == "tool_call":
            calls.append(event["tool"])
            ordered.append(("call", event["tool"]))
        if event["type"] == "assistant":
            ordered.append(("say", event["text"]))
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
    if "customer_saved" in expect:
        assert session.order.customer.street_from_saved == \
            expect["customer_saved"]
        if expect["customer_saved"]:
            # redaction: the saved street never enters the model context
            assert "Meyer Teststraße" not in json.dumps(
                session.messages, ensure_ascii=False)
    if "customer_first_name" in expect:
        assert session.order.customer.first_name == \
            expect["customer_first_name"]
    if "set_customer_calls" in expect:
        assert calls.count("set_customer") == expect["set_customer_calls"]
    if expect.get("name_confirm_before_set"):
        # the spoken name is confirmed BEFORE the customer is stored —
        # the ghost-customer guard for voice flows
        confirm_idx = next(i for i, (kind, value) in enumerate(ordered)
                           if kind == "say"
                           and "richtig verstanden" in value)
        set_idx = next(i for i, (kind, value) in enumerate(ordered)
                       if kind == "call" and value == "set_customer")
        assert confirm_idx < set_idx


def test_transcripts_exist():
    # five v1 flows + saved-address pair + three name-confirmation cases
    assert len(TRANSCRIPTS) == 10


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

 succeeded in 470ms:
"""Voice wiring, fully offline: the app boots against a stub speech
service; a headless Chromium with a fake microphone (streaming the real
audio fixture) exercises the genuine push-to-talk path. Asserts wiring —
control visibility, STT round trip, spoken-turn metadata, final-message
TTS, runtime degradation, secure-context gating — never speech quality.

Runs after tests/test_web_e2e.py (module order matters: this module
re-boots the shared app with SPEECH_* configured)."""
from __future__ import annotations

import os
from pathlib import Path

import httpx
import pytest

from tests.stubs import StubGateway, StubPizzaSim, StubSpeech, run_server

PZ1 = "11111111-aaaa-bbbb-cccc-000000000001"
AUDIO = Path(__file__).parent / "fixtures" / "audio"


@pytest.fixture(scope="module")
def stack():
    pizzasim = StubPizzaSim()
    gateway = StubGateway()
    speech = StubSpeech()
    ps_server, ps_url = run_server(pizzasim.app)
    gw_server, gw_url = run_server(gateway.app)
    sp_server, sp_url = run_server(speech.app)
    os.environ.update({
        "PIZZASIM_URL": ps_url,
        "PIZZASIM_API_KEY": "stub-key",
        "PIZZERIA_ID": PZ1,
        "PIZZERIA_LANG": "de",
        "LITELLM_PIZZA_URL": gw_url,
        "LITELLM_PIZZA_KEY": "stub-key",
        "LITELLM_PIZZA_MODEL_1": "scripted-stub",
        "APP_VERSION": "2.0.0",
        "SPEECH_URL": sp_url,
        "SPEECH_STT_MODEL": "stub-stt",
        "SPEECH_TTS_MODEL": "stub-tts",
        "SPEECH_TTS_VOICE": "stub-voice",
    })
    from channels import web  # boots (again) against the speech-enabled env
    app_server, app_url = run_server(web.app)
    yield {"pizzasim": pizzasim, "gateway": gateway, "speech": speech,
           "url": app_url, "web": web}
    for server in (app_server, ps_server, gw_server, sp_server):
        server.should_exit = True
    for var in ("SPEECH_URL", "SPEECH_STT_MODEL", "SPEECH_TTS_MODEL",
                "SPEECH_TTS_VOICE"):
        os.environ.pop(var, None)


@pytest.fixture()
def api(stack):
    with httpx.Client(base_url=stack["url"], timeout=30.0) as client:
        yield client


# --- API surface -----------------------------------------------------------

def test_config_reports_speech_enabled(api):
    assert api.get("/config").json()["speech"] is True


def test_stt_round_trip_uses_session_language(stack, api):
    sid = api.post("/session", json={}).json()["session_id"]
    audio = (AUDIO / "order.de.wav").read_bytes()
    result = api.post(f"/speech/stt?session_id={sid}",
                      files={"audio": ("order.de.wav", audio, "audio/wav")})
    assert result.json() == {"text": "Zwei Margherita bitte"}
    assert stack["speech"].languages[-1] == "de"
    api.post("/language", json={"session_id": sid, "lang": "en"})
    api.post(f"/speech/stt?session_id={sid}",
             files={"audio": ("order.en.wav",
                              (AUDIO / "order.en.wav").read_bytes(),
                              "audio/wav")})
    assert stack["speech"].languages[-1] == "en"


def test_tts_returns_playable_audio(stack, api):
    sid = api.post("/session", json={}).json()["session_id"]
    before = stack["speech"].tts_calls
    result = api.post("/speech/tts", json={"session_id": sid,
                                           "text": "Hallo"})
    assert result.status_code == 200
    assert result.headers["content-type"].startswith("audio/")
    assert result.content[:4] == b"RIFF"  # a real, playable WAV container
    assert stack["speech"].tts_calls == before + 1


def test_speech_failure_maps_to_502(stack, api):
    sid = api.post("/session", json={}).json()["session_id"]
    stack["speech"].mode = "fail"
    try:
        result = api.post("/speech/tts", json={"session_id": sid,
                                               "text": "x"})
        assert result.status_code == 502
    finally:
        stack["speech"].mode = "ok"


def test_stt_unknown_session_404(api):
    assert api.post("/speech/stt?session_id=ghost",
                    files={"audio": ("a.wav", b"x",
                                     "audio/wav")}).status_code == 404


# --- browser E2E: the real push-to-talk path -------------------------------

@pytest.fixture(scope="module")
def voice_page_factory(stack):
    """Firefox with fake media streams: headless Chromium exposes no audio
    device on this host even with --use-fake-device-for-media-capture
    (verified), while Firefox's fake-stream pref needs no audio backend.
    Spec-aligned: the product must work cross-browser, and the offline
    wiring tests don't care about audio content (the stub returns a fixed
    transcript). The recorded WAV fixtures drive the LIVE voice test via
    Chromium's --use-file-for-fake-audio-capture on the voice deployment."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.firefox.launch(firefox_user_prefs={
            "media.navigator.streams.fake": True,
            "media.navigator.permission.disabled": True,
        })
        context = browser.new_context()
        yield context.new_page
        browser.close()


def open_app(new_page, stack, init_script=None):
    page = new_page()
    if init_script:
        page.add_init_script(init_script)
    page.goto(stack["url"], timeout=30000)
    page.wait_for_selector(".msg.assistant", timeout=30000)
    return page


def test_e2e_voice_push_to_talk_round_trip(voice_page_factory, stack):
    stack["gateway"].mode = "ok"
    stack["gateway"].saw_spoken_note = False
    page = open_app(voice_page_factory, stack)
    # controls visible on a secure context with speech configured
    assert page.locator("#mic").is_visible()
    assert page.locator("#tts-wrap").is_visible()
    assert not page.locator("#tts-toggle").is_checked()  # off by default

    page.click("#mic")  # push-to-talk: start
    page.wait_for_selector("#mic.recording", timeout=10000)  # visible state
    page.wait_for_timeout(1200)
    page.click("#mic")  # stop → upload → stub transcript drives the turn
    page.wait_for_selector("text=Zwei Margherita bitte", timeout=30000)
    page.wait_for_selector("#basket-lines li", timeout=30000)
    assert "2× Margherita" in page.locator("#basket-lines").inner_text()
    assert stack["gateway"].saw_spoken_note  # spoken-style note reached model
    page.close()


def test_e2e_tts_fetched_once_for_final_message_only(voice_page_factory,
                                                     stack):
    stack["gateway"].mode = "ok"
    page = open_app(voice_page_factory, stack)
    page.check("#tts-toggle")
    before = stack["speech"].tts_calls
    page.fill("#text", "Was kostet eine Margherita?")
    page.click("#send")
    page.wait_for_selector("text=8.5 €", timeout=30000)
    page.wait_for_function(
        f"() => fetch('/config').then(() => true) && true", timeout=5000)
    page.wait_for_timeout(800)  # allow the TTS fetch to complete
    # the turn contained a tool step AND a final message → exactly one TTS
    assert stack["speech"].tts_calls == before + 1
    page.close()


def test_e2e_runtime_speech_outage_degrades_to_text(voice_page_factory,
                                                    stack):
    stack["gateway"].mode = "ok"
    page = open_app(voice_page_factory, stack)
    stack["speech"].mode = "fail"
    try:
        page.click("#mic")
        page.wait_for_selector("#mic.recording", timeout=10000)
        page.wait_for_timeout(900)
        page.click("#mic")  # upload fails → degrade
        page.wait_for_selector(".notice", timeout=30000)
        page.wait_for_selector("#mic", state="hidden", timeout=10000)
        assert page.locator("#tts-wrap").is_hidden()
        # typed ordering continues untouched
        page.fill("#text", "Zwei Margherita bitte")
        page.click("#send")
        page.wait_for_selector("#basket-lines li", timeout=30000)
    finally:
        stack["speech"].mode = "ok"
    page.close()


# --- live voice acceptance (opt-in, release-gating per SPEC) ---------------

LIVE_VOICE = (os.environ.get("PIZZA_LIVE_VOICE") == "1"
              and bool(os.environ.get("PIZZA_LIVE_VOICE_URL")))


@pytest.mark.skipif(not LIVE_VOICE,
                    reason="live voice test only with PIZZA_LIVE_VOICE=1 "
                           "and PIZZA_LIVE_VOICE_URL=<https deployment>")
@pytest.mark.parametrize("lang,fixture,name_reply,yes", [
    ("de", "order.de.wav", "Ich heiße VoiceTest", "Ja"),
    ("en", "order.en.wav", "My name is VoiceTest", "Yes"),
])
def test_live_voice_acceptance(lang, fixture, name_reply, yes):
    """The voice agent actually works: real browser over HTTPS, real
    microphone capture (fake device streaming the spoken-order fixture),
    real STT, the confirm control, real TTS — then the order is verified
    via the pizzeria's API endpoints. Not a text replay: if STT does not
    produce an order-driving transcript, this test fails."""
    from playwright.sync_api import sync_playwright

    from core.pizzasim import PizzaSim

    base_url = os.environ["PIZZA_LIVE_VOICE_URL"]
    wav = str((AUDIO / fixture).resolve())
    tts_audio = {"bytes": 0}

    with sync_playwright() as p:
        browser = p.chromium.launch(args=[
            "--use-fake-device-for-media-capture",
            "--use-fake-ui-for-media-capture",
            f"--use-file-for-fake-audio-capture={wav}",
        ])
        context = browser.new_context()
        context.grant_permissions(["microphone"], origin=base_url)
        page = context.new_page()

        def sniff(response):
            if response.url.endswith("/speech/tts") and response.ok:
                tts_audio["bytes"] = len(response.body())
        page.on("response", sniff)

        page.goto(base_url, timeout=60000)
        page.wait_for_selector(".msg.assistant", timeout=120000)
        if lang == "en":
            page.locator("#lang-switch button[data-lang=en]").click()
        assert page.locator("#mic").is_visible()  # HTTPS + speech up
        page.check("#tts-toggle")

        page.click("#mic")
        page.wait_for_selector("#mic.recording", timeout=15000)
        page.wait_for_timeout(7000)  # the fixture is ~5.5s of speech
        page.click("#mic")
        # STT must yield an order-driving transcript: the basket fills.
        page.wait_for_selector("#basket-lines li", timeout=120000)

        page.fill("#text", name_reply)
        page.click("#send")
        page.wait_for_selector(".readback button:enabled", timeout=120000)
        page.locator(".readback button:enabled").click()
        page.wait_for_selector("#submitted-banner:not([hidden])",
                               timeout=120000)
        page.wait_for_timeout(2000)  # allow the final TTS fetch
        assert tts_audio["bytes"] > 0  # real, non-empty playable audio
        pizzeria_id = page.locator("#uuid").inner_text().strip()
        banner = page.locator("#submitted-banner").inner_text()
        order_id = banner.split()[-1]
        browser.close()

    # verify via the API: right customer, items present, right tenant
    client = PizzaSim.from_env().for_pizzeria(pizzeria_id)
    listed = {o["id"] for o in client.list_orders()}
    assert order_id in listed
    detail = client.get_order(order_id)
    assert detail["customer"]["first_name"] == "VoiceTest"
    assert detail["items"], "order carries no items"


def test_e2e_insecure_context_renders_no_voice_ui(voice_page_factory,
                                                  stack):
    """Plain HTTP never presents a voice-capable UI — even with speech
    fully configured server-side."""
    stack["gateway"].mode = "ok"
    page = open_app(
        voice_page_factory, stack,
        init_script="Object.defineProperty(window, 'isSecureContext',"
                    " {value: false});")
    assert page.locator("#mic").is_hidden()
    assert page.locator("#tts-wrap").is_hidden()
    page.fill("#text", "Zwei Margherita bitte")  # text ordering works
    page.click("#send")
    page.wait_for_selector("#basket-lines li", timeout=30000)
    page.close()

 succeeded in 428ms:
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
        self.saw_spoken_note = False
        self.app = app = FastAPI()

        @app.post("/chat/completions")
        async def chat(request: Request):
            if self.mode == "http500":
                return JSONResponse({"error": "boom"}, status_code=500)
            body = await request.json()
            if any(m.get("role") == "system"
                   and "vorgelesen" in (m.get("content") or "")
                   for m in body["messages"]):
                self.saw_spoken_note = True
            if self.mode == "empty":
                return _reply({"content": ""})
            return _reply(self._script(body["messages"]))


def _reply(message: dict) -> dict:
    return {"choices": [{"message": message}]}


def _tiny_wav() -> bytes:
    import io
    import wave
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(8000)
        w.writeframes(b"\x00\x00" * 800)  # 0.1s silence
    return buf.getvalue()


class StubSpeech:
    """OpenAI-compatible speech stub: fixed transcript, tiny TTS audio,
    switchable failure mode. Asserts wiring, not speech quality."""

    def __init__(self):
        self.transcript = "Zwei Margherita bitte"
        self.languages: list[str] = []
        self.tts_calls = 0
        self.mode = "ok"  # "fail" → 502 on both endpoints
        self.app = app = FastAPI()

        @app.get("/v1/models")
        def models():
            return {"data": []}

        @app.post("/v1/audio/transcriptions")
        async def stt(request: Request):
            if self.mode == "fail":
                return JSONResponse({"error": "down"}, status_code=502)
            form = await request.form()
            self.languages.append(str(form.get("language", "")))
            return {"text": self.transcript}

        @app.post("/v1/audio/speech")
        async def tts(request: Request):
            if self.mode == "fail":
                return JSONResponse({"error": "down"}, status_code=502)
            self.tts_calls += 1
            from fastapi.responses import Response
            return Response(_tiny_wav(), media_type="audio/wav")


def _last_tool(messages: list[dict]) -> tuple[str, dict] | None:
    # Skip trailing system messages: spoken turns append the ephemeral
    # spoken-style note after the conversation tail.
    last = next((m for m in reversed(messages)
                 if m.get("role") != "system"), None)
    if not last or last.get("role") != "tool":
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

codex
The core redaction path is clean so far: snapshots/tool results/logged messages are all fed by `Customer.as_dict()`, while submission uses `as_submit_dict()` exactly once in `_submit`. I’m now checking the server speech endpoints and deploy/readme artifacts to see whether the browser tests line up with the real runtime behavior and the neutral deployment claim.
exec
/bin/bash -lc "sed -n '1,260p' channels/web.py" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,220p' deploy/speech-service.compose.yml" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "rg -n \"/speech/stt|/speech/tts|SPEECH_|isSecureContext|speech\" channels core -g '"'!channels/static/app.js'"'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,220p' README.md && printf '\\n---QA---\\n' && sed -n '1,220p' decisions/qa.md" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 579ms:
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

 succeeded in 603ms:
# Self-hosted, CPU-only speech service for the PizzaSim ordering agent.
#
# Neutral by design (SPEC): the image and the models are operator
# configuration — no vendor or model names live in this repository.
# Whatever image the operator picks MUST expose an OpenAI-compatible
# surface on its HTTP port:
#
#   POST /v1/audio/transcriptions   multipart: file, model, language -> {"text": ...}
#   POST /v1/audio/speech           JSON: model, voice, input -> audio bytes
#   GET  /v1/models                 2xx = alive (used by the app's startup probe)
#
# The app and this service are deployed together as first-party artifacts;
# the app reaches it via SPEECH_URL (e.g. http://speech:8000 on a shared
# network, or the routed URL). Voice-capable deployments serve the app
# over HTTPS on a real host name — microphone capture does not exist on
# plain HTTP (SPEC).
services:
  speech:
    image: ${SPEECH_IMAGE}
    restart: unless-stopped
    # CPU-only on purpose: no GPU reservations, modest resources.
    environment:
      - SPEECH_STT_MODEL=${SPEECH_STT_MODEL}
      - SPEECH_TTS_MODEL=${SPEECH_TTS_MODEL}
      - SPEECH_TTS_VOICE=${SPEECH_TTS_VOICE}
    expose:
      - "${SPEECH_CONTAINER_PORT:-8000}"

 succeeded in 593ms:
channels/speech.py:4:here, server-side, against {SPEECH_URL}. The language sent with STT/TTS is
channels/speech.py:5:the session language — there is no separate speech-language config.
channels/speech.py:21:    """All-or-nothing: enabled only if SPEECH_URL is set, all models are
channels/speech.py:25:        self.url = (optional_env("SPEECH_URL") or "").rstrip("/")
channels/speech.py:26:        self.stt_model = optional_env("SPEECH_STT_MODEL")
channels/speech.py:27:        self.tts_model = optional_env("SPEECH_TTS_MODEL")
channels/speech.py:28:        self.voice = optional_env("SPEECH_TTS_VOICE")
channels/speech.py:36:                print("speech service not answering — text-only mode",
channels/speech.py:55:                f"{self.url}/v1/audio/speech",
channels/web.py:5:/health, speech proxies, static UI. Turns are serialized per session;
channels/web.py:26:from channels.speech import SpeechService, SpeechUnavailable
channels/web.py:77:    app.state.speech = SpeechService()
channels/web.py:96:        "speech": app.state.speech.enabled,
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

 succeeded in 501ms:
# PizzaSim Ordering Agent

An ordering agent for the PizzaSim demo kitchen. The order is a state
machine owned by the code; the model only turns customer language into tool
calls. See <a href="SPEC.md">SPEC.md</a> for the full specification and
<a href="PLAN.md">PLAN.md</a> for the design.

## Setup

```bash
python3 -m venv venv
venv/bin/pip install -r requirements.txt
venv/bin/python -m playwright install chromium   # for the browser E2E tests
```

Configuration comes from the environment (or `~/.env`); every variable in
`.env.example` except the four `SPEECH_*` ones is required — including
`PIZZERIA_LANG` (initial language, `de`/`en`) and `APP_VERSION` (`x.y.z`,
shown in the web footer, raised on every release). The process refuses to
start when one is missing, naming the variable. No values are ever printed
or logged.

## CLI channel

```bash
venv/bin/python -m channels.cli            # plain chat
venv/bin/python -m channels.cli --verbose  # + tool calls and states
```

One CLI process serves the preselected `PIZZERIA_ID` in `PIZZERIA_LANG`.
The agent greets first and answers each turn in the language you used
(German or English). Prices and the basket total come verbatim from the
menu. End with Ctrl-D.

## Web channel

```bash
venv/bin/python -m channels.web
```

Then open <a href="http://127.0.0.1:8888" target="_blank">http://127.0.0.1:8888</a>.

- **Header:** the pizzeria you are ordering from, a selector filled live
  from `GET /pizzerias` (name + short UUID; changing it starts a fresh
  conversation — a basket never crosses a tenant boundary), a link to that
  pizzeria's dashboard, a DE/EN language switch, and "Start over".
- **Basket panel:** live from the code-owned order state — quantities,
  line totals, basket total; locked once submitted.
- **Read-back:** a visually distinct panel with an explicit confirm
  button. Confirmation is your click, tied to the exact basket revision
  that was read back.
- **Footer:** `APP_VERSION`, the full pizzeria UUID (selectable),
  connection badges for the ordering API and the model gateway, and a
  link to the API documentation.
- Every message gets an answer: intermediate tool steps stream visibly,
  and any error, timeout, or unanswered turn leaves a plain-language
  notice with a resend button.

## Voice deployment

Voice is a required capability of a production release (SPEC); text-only
is the degraded mode for dev/test and outages. To deploy voice:

1. Provision the self-hosted speech service next to the app —
   `deploy/speech-service.compose.yml` is the neutral definition; the
   image and models are operator configuration (`SPEECH_IMAGE`,
   `SPEECH_*`), never named in this repository.
2. Serve the app over **HTTPS on a real host name** (e.g. via the
   platform's proxy). Microphone capture does not exist on plain HTTP —
   the UI hides all voice controls outside a secure context.
3. Set `SPEECH_URL`, `SPEECH_STT_MODEL`, `SPEECH_TTS_MODEL`,
   `SPEECH_TTS_VOICE` on the app. STT/TTS use the session language.
4. Release-gating proof: run the live voice acceptance test against the
   deployment —
   `PIZZA_LIVE_VOICE=1 PIZZA_LIVE_VOICE_URL=https://<domain> venv/bin/python -m pytest tests/test_web_speech.py -k live_voice`
   (drives the real page with recorded spoken-order fixtures through
   microphone capture, real STT, the confirm control and real TTS, then
   verifies the order via the API).

## Speech (web only, optional in dev)

Set `SPEECH_URL`, `SPEECH_STT_MODEL`, `SPEECH_TTS_MODEL` and
`SPEECH_TTS_VOICE` to a self-hosted OpenAI-compatible speech service. The
mic button is push-to-talk (click to start, click to stop; recording state
is always visible); the read-aloud toggle is off by default and speaks
only final answers. STT and TTS use the session language. With
`SPEECH_URL` unset — or the service down at startup — mic and toggle are
not rendered and the page is fully usable as text chat.

Manual speech checklist: dictate an order; dictate a name that needs
correcting (the agent repeats the name back before submitting); ask a menu
question; and one run with `SPEECH_URL` unset placing an order as text.

## Tests

```bash
venv/bin/python -m pytest tests/                 # offline: no network, no LLM
PIZZA_LIVE_TEST=1 venv/bin/python -m pytest tests/test_tools.py -k live
```

The offline suite includes `tests/test_web_e2e.py`: a headless Chromium
drives the real page against a stub PizzaSim and a stub scripted gateway —
full order to submission, pizzeria switch, and three failure paths (tool
error, gateway unreachable, stream without a final answer), all asserted
against the DOM. The second command is the one opt-in live acceptance test:
it places a real order and verifies customer, items and quantities through
the pizzeria's order endpoints.

## Logs

One JSON line per event (user text, tool calls, tool results, state
transitions) in `logs/agent-<session>.jsonl`. Secrets never appear there.

---QA---
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

## 2026-08-02 — Offline voice E2E runs on Firefox fake streams

**Why:** headless Chromium on this host exposes no audio device even with
--use-fake-device-for-media-capture (verified empirically; enumerateDevices
empty). Firefox's media.navigator.streams.fake needs no audio backend and
exercises the identical UI path (getUserMedia + MediaRecorder + upload).
Spec-aligned: the product is required to work cross-browser. The recorded
WAV fixtures drive the LIVE voice acceptance test via Chromium's
--use-file-for-fake-audio-capture on the voice-capable deployment, where
the transcript content matters. Deviation from the plan's Chromium-flag
wording documented here for the implementation review.

exec
/bin/bash -lc "sed -n '1,220p' channels/speech.py" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 134ms:
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

exec
/bin/bash -lc 'for f in tests/transcripts/saved_address.json tests/transcripts/saved_address_decline.json tests/transcripts/spoken_happy_dictated_street.json tests/transcripts/spoken_happy_saved_street.json tests/transcripts/spoken_wrong_name.json; do echo "--- $f"; sed -n '"'1,220p' \""'$f"; done' in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 139ms:
--- tests/transcripts/saved_address.json
{
  "name": "saved_address_reuse",
  "fake": "ok",
  "turns": [
    {"user": "Eine Margherita bitte, ich heiße Marko.",
     "script": [
       {"tool": "add_items", "args": {"items": [{"type": "pizza", "code": "margherita", "qty": 1, "extras": []}]}},
       {"tool": "lookup_customer", "args": {"first_name": "Marko"}},
       {"say": "Gern, Marko. Soll ich wieder an Ihre gespeicherte Adresse liefern?"}
     ]},
    {"user": "Ja, an die gespeicherte Adresse.",
     "script": [
       {"tool": "set_customer", "args": {"first_name": "Marko", "use_saved_street": true}},
       {"tool": "read_back", "args": {}},
       {"say": "Marko, gespeicherte Adresse — eine Margherita, 8,50 €. Stimmt das?"}
     ]},
    {"user": "Ja.",
     "script": [
       {"tool": "confirm_order", "args": {"revision": 2}},
       {"tool": "submit_order", "args": {}},
       {"say": "Bestellt! Etwa 2 Minuten."}
     ]}
  ],
  "expect": {
    "state": "SUBMITTED",
    "calls": ["add_items", "lookup_customer", "set_customer", "read_back", "confirm_order", "submit_order"],
    "error_codes": [],
    "items": [{"type": "pizza", "code": "margherita", "qty": 1}],
    "customer_saved": true
  }
}
--- tests/transcripts/saved_address_decline.json
{
  "name": "saved_address_declined_fallback",
  "fake": "ok",
  "turns": [
    {"user": "Eine Funghi bitte, ich heiße Marko.",
     "script": [
       {"tool": "add_items", "args": {"items": [{"type": "pizza", "code": "funghi", "qty": 1, "extras": []}]}},
       {"tool": "lookup_customer", "args": {"first_name": "Marko"}},
       {"say": "Gern, Marko. Soll ich wieder an Ihre gespeicherte Adresse liefern?"}
     ]},
    {"user": "Nein, bitte neu: via Nuova 2.",
     "script": [
       {"tool": "set_customer", "args": {"first_name": "Marko", "street_one": "via Nuova 2"}},
       {"tool": "read_back", "args": {}},
       {"say": "Marko, via Nuova 2 — eine Funghi, 9,00 €. Stimmt das?"}
     ]},
    {"user": "Ja.",
     "script": [
       {"tool": "confirm_order", "args": {"revision": 2}},
       {"tool": "submit_order", "args": {}},
       {"say": "Bestellt! Etwa 2 Minuten."}
     ]}
  ],
  "expect": {
    "state": "SUBMITTED",
    "calls": ["add_items", "lookup_customer", "set_customer", "read_back", "confirm_order", "submit_order"],
    "error_codes": [],
    "items": [{"type": "pizza", "code": "funghi", "qty": 1}],
    "customer_saved": false
  }
}
--- tests/transcripts/spoken_happy_dictated_street.json
{
  "name": "spoken_happy_dictated_street_confirms_name",
  "fake": "ok",
  "turns": [
    {"user": "Zwei Margherita, ich heiße Nina, via Milano 3.",
     "script": [
       {"tool": "add_items", "args": {"items": [{"type": "pizza", "code": "margherita", "qty": 2, "extras": []}]}},
       {"tool": "lookup_customer", "args": {"first_name": "Nina"}},
       {"say": "Habe ich Ihren Namen richtig verstanden: Nina?"}
     ]},
    {"user": "Ja, Nina.",
     "script": [
       {"tool": "set_customer", "args": {"first_name": "Nina", "street_one": "via Milano 3"}},
       {"tool": "read_back", "args": {}},
       {"say": "Nina, via Milano 3 — zwei Margherita, 17,00 €. Stimmt das?"}
     ]},
    {"user": "Ja.",
     "script": [
       {"tool": "confirm_order", "args": {"revision": 2}},
       {"tool": "submit_order", "args": {}},
       {"say": "Bestellt! Etwa 2 Minuten."}
     ]}
  ],
  "expect": {
    "state": "SUBMITTED",
    "calls": ["add_items", "lookup_customer", "set_customer", "read_back", "confirm_order", "submit_order"],
    "error_codes": [],
    "items": [{"type": "pizza", "code": "margherita", "qty": 2}],
    "customer_first_name": "Nina",
    "name_confirm_before_set": true
  }
}
--- tests/transcripts/spoken_happy_saved_street.json
{
  "name": "spoken_happy_saved_street_still_confirms_name",
  "fake": "ok",
  "turns": [
    {"user": "Eine Diavolo bitte, hier ist Marko.",
     "script": [
       {"tool": "add_items", "args": {"items": [{"type": "pizza", "code": "diavolo", "qty": 1, "extras": []}]}},
       {"tool": "lookup_customer", "args": {"first_name": "Marko"}},
       {"say": "Habe ich Ihren Namen richtig verstanden: Marko?"}
     ]},
    {"user": "Ja, Marko.",
     "script": [
       {"say": "Danke, Marko. Soll ich wieder an Ihre gespeicherte Adresse liefern?"}
     ]},
    {"user": "Ja bitte.",
     "script": [
       {"tool": "set_customer", "args": {"first_name": "Marko", "use_saved_street": true}},
       {"tool": "read_back", "args": {}},
       {"say": "Marko, gespeicherte Adresse — eine Diavolo, 11,00 €. Stimmt das?"}
     ]},
    {"user": "Ja.",
     "script": [
       {"tool": "confirm_order", "args": {"revision": 2}},
       {"tool": "submit_order", "args": {}},
       {"say": "Bestellt! Etwa 2 Minuten."}
     ]}
  ],
  "expect": {
    "state": "SUBMITTED",
    "calls": ["add_items", "lookup_customer", "set_customer", "read_back", "confirm_order", "submit_order"],
    "error_codes": [],
    "items": [{"type": "pizza", "code": "diavolo", "qty": 1}],
    "customer_first_name": "Marko",
    "customer_saved": true,
    "name_confirm_before_set": true
  }
}
--- tests/transcripts/spoken_wrong_name.json
{
  "name": "spoken_wrong_name_corrected",
  "fake": "ok",
  "turns": [
    {"user": "Eine Margherita bitte, ich bin die Efa.",
     "script": [
       {"tool": "add_items", "args": {"items": [{"type": "pizza", "code": "margherita", "qty": 1, "extras": []}]}},
       {"say": "Gern. Habe ich Ihren Namen richtig verstanden: Efa?"}
     ]},
    {"user": "Nein, Eva mit V.",
     "script": [
       {"tool": "set_customer", "args": {"first_name": "Eva", "street_one": "via Roma 1"}},
       {"tool": "read_back", "args": {}},
       {"say": "Danke, Eva. Eine Margherita, 8,50 € — an via Roma 1. Stimmt das?"}
     ]},
    {"user": "Ja.",
     "script": [
       {"tool": "confirm_order", "args": {"revision": 2}},
       {"tool": "submit_order", "args": {}},
       {"say": "Bestellt, Eva! Etwa 2 Minuten."}
     ]}
  ],
  "expect": {
    "state": "SUBMITTED",
    "calls": ["add_items", "set_customer", "read_back", "confirm_order", "submit_order"],
    "error_codes": [],
    "items": [{"type": "pizza", "code": "margherita", "qty": 1}],
    "customer_first_name": "Eva",
    "set_customer_calls": 1,
    "name_confirm_before_set": true
  }
}

codex
I’ve finished the static pass on the core flow and the high-risk call sites. I’m running the targeted tests that directly back the SPEC claims now: tool-level redaction/error paths, transcript ordering checks, and the offline speech/browser suite excluding the opt-in live acceptance.
exec
/bin/bash -lc "pytest tests/test_tools.py -k 'lookup_customer or saved_street or use_saved_street or street_omitted_from_submit_body'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc 'pytest tests/test_transcripts.py' in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "pytest tests/test_web_speech.py -k 'not live_voice'" in /home/rob/bpm-pizza-vibecoding-solution
 exited 2 in 686ms:
============================= test session starts ==============================
platform linux -- Python 3.13.7, pytest-9.0.2, pluggy-1.6.0
rootdir: /home/rob/bpm-pizza-vibecoding-solution
plugins: typeguard-4.4.2
collected 0 items / 1 error

==================================== ERRORS ====================================
__________________ ERROR collecting tests/test_web_speech.py ___________________
ImportError while importing test module '/home/rob/bpm-pizza-vibecoding-solution/tests/test_web_speech.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/usr/lib/python3.13/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/test_web_speech.py:14: in <module>
    import httpx
E   ModuleNotFoundError: No module named 'httpx'
=========================== short test summary info ============================
ERROR tests/test_web_speech.py
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
=============================== 1 error in 0.12s ===============================

 exited 2 in 746ms:
============================= test session starts ==============================
platform linux -- Python 3.13.7, pytest-9.0.2, pluggy-1.6.0
rootdir: /home/rob/bpm-pizza-vibecoding-solution
plugins: typeguard-4.4.2
collected 0 items / 1 error

==================================== ERRORS ====================================
__________________ ERROR collecting tests/test_transcripts.py __________________
ImportError while importing test module '/home/rob/bpm-pizza-vibecoding-solution/tests/test_transcripts.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/usr/lib/python3.13/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/test_transcripts.py:10: in <module>
    from core.agent import Agent, AgentConfig, Session
core/agent.py:16: in <module>
    import httpx
E   ModuleNotFoundError: No module named 'httpx'
=========================== short test summary info ============================
ERROR tests/test_transcripts.py
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
=============================== 1 error in 0.12s ===============================

 exited 2 in 787ms:
============================= test session starts ==============================
platform linux -- Python 3.13.7, pytest-9.0.2, pluggy-1.6.0
rootdir: /home/rob/bpm-pizza-vibecoding-solution
plugins: typeguard-4.4.2
collected 0 items / 1 error

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
=========================== short test summary info ============================
ERROR tests/test_tools.py
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
=============================== 1 error in 0.18s ===============================

codex
The local test runs are blocked by the bare interpreter: `httpx` is missing in this shell environment, so collection fails before any assertions run. I’m checking whether the project’s virtualenv is present and can run the targeted suites there; if not, I’ll keep the verdict strictly on code inspection plus the in-repo test definitions.
exec
/bin/bash -lc 'test -x venv/bin/python && echo yes || echo no' in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc 'ls -1' in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "sed -n '1,220p' requirements.txt" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 355ms:
yes

 succeeded in 362ms:
PLAN.md
Procfile
README.md
SPEC.md
SPEC_20260801_1.md
SPEC_20260801_2.md
SPEC_20260801_3.md
SPEC_20260801_4.md
channels
core
decisions
deploy
initial_prompt.md
logs
prompts
requirements.txt
reviews
tests
venv

 succeeded in 404ms:
fastapi==0.141.1
httpx==0.28.1
playwright==1.62.0
pytest==9.1.1
python-multipart==0.0.32
uvicorn==0.52.0

exec
/bin/bash -lc 'venv/bin/python -m pytest tests/test_transcripts.py' in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "venv/bin/python -m pytest tests/test_tools.py -k 'lookup_customer or saved_street or use_saved_street or street_omitted_from_submit_body'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "venv/bin/python -m pytest tests/test_web_speech.py -k 'not live_voice'" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 571ms:
============================= test session starts ==============================
platform linux -- Python 3.13.7, pytest-9.1.1, pluggy-1.6.0
rootdir: /home/rob/bpm-pizza-vibecoding-solution
plugins: anyio-4.14.2
collected 51 items / 44 deselected / 7 selected

tests/test_tools.py .......                                              [100%]

======================= 7 passed, 44 deselected in 0.08s =======================

 succeeded in 608ms:
============================= test session starts ==============================
platform linux -- Python 3.13.7, pytest-9.1.1, pluggy-1.6.0
rootdir: /home/rob/bpm-pizza-vibecoding-solution
plugins: anyio-4.14.2
collected 12 items

tests/test_transcripts.py ............                                   [100%]

============================== 12 passed in 0.09s ==============================

codex
The targeted core and transcript suites passed under `venv`. The offline speech suite is still running; once that finishes I’ll consolidate the verdict with file-backed references and any residual risk.
 succeeded in 13431ms:
============================= test session starts ==============================
platform linux -- Python 3.13.7, pytest-9.1.1, pluggy-1.6.0
rootdir: /home/rob/bpm-pizza-vibecoding-solution
plugins: anyio-4.14.2
collected 11 items / 2 deselected / 9 selected

tests/test_web_speech.py .........                                       [100%]

=============================== warnings summary ===============================
tests/test_web_speech.py::test_config_reports_speech_enabled
  /home/rob/bpm-pizza-vibecoding-solution/channels/web.py:51: DeprecationWarning: 
          on_event is deprecated, use lifespan event handlers instead.
  
          Read more about it in the
          [FastAPI docs for Lifespan Events](https://fastapi.tiangolo.com/advanced/events/).
          
    @app.on_event("startup")

tests/test_web_speech.py::test_config_reports_speech_enabled
  /home/rob/bpm-pizza-vibecoding-solution/venv/lib/python3.13/site-packages/fastapi/applications.py:4681: DeprecationWarning: 
          on_event is deprecated, use lifespan event handlers instead.
  
          Read more about it in the
          [FastAPI docs for Lifespan Events](https://fastapi.tiangolo.com/advanced/events/).
          
    return self.router.on_event(event_type)  # ty: ignore[deprecated]

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
================= 9 passed, 2 deselected, 2 warnings in 12.60s =================

exec
/bin/bash -lc "nl -ba core/tools.py | sed -n '50,230p'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "nl -ba core/order.py | sed -n '38,70p'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "nl -ba core/tools.py | sed -n '288,305p'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "nl -ba channels/static/app.js | sed -n '160,440p'" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 667ms:
    50	                    "properties": {
    51	                        "type": {"type": "string",
    52	                                 "enum": ["pizza", "pasta"]},
    53	                        "code": {"type": "string"},
    54	                        "qty": {"type": "integer", "minimum": 1}},
    55	                    "required": ["type", "code"]}},
    56	    {"name": "lookup_customer",
    57	     "description": "Check whether a first name is a known customer with "
    58	                    "a saved street. Returns booleans only — never the "
    59	                    "address itself. Use after the customer gave their "
    60	                    "name; on a saved street, ask whether to deliver to "
    61	                    "the saved address without reciting it.",
    62	     "parameters": {"type": "object",
    63	                    "properties": {
    64	                        "first_name": {"type": "string", "minLength": 1}},
    65	                    "required": ["first_name"]}},
    66	    {"name": "set_customer",
    67	     "description": "Store the customer's first name and street. Either "
    68	                    "pass street_one, or pass use_saved_street=true after "
    69	                    "the customer confirmed delivery to their saved "
    70	                    "address — never both.",
    71	     "parameters": {"type": "object",
    72	                    "properties": {
    73	                        "first_name": {"type": "string", "minLength": 1},
    74	                        "street_one": {"type": "string"},
    75	                        "use_saved_street": {"type": "boolean"}},
    76	                    "required": ["first_name"]}},
    77	    {"name": "read_back",
    78	     "description": "The complete order as it stands — read this back to "
    79	                    "the customer before asking for confirmation.",
    80	     "parameters": {"type": "object", "properties": {}}},
    81	    {"name": "confirm_order",
    82	     "description": "Confirm the order after the customer said yes to the "
    83	                    "read-back. revision must be the revision that was "
    84	                    "read back.",
    85	     "parameters": {"type": "object",
    86	                    "properties": {"revision": {"type": "integer"}},
    87	                    "required": ["revision"]}},
    88	    {"name": "submit_order",
    89	     "description": "Send the confirmed order to the kitchen. Only legal "
    90	                    "after confirm_order.",
    91	     "parameters": {"type": "object", "properties": {}}},
    92	    {"name": "check_street",
    93	     "description": "Rough plausibility check of a street name. Not a "
    94	                    "deliverability check — never claim the address was "
    95	                    "verified.",
    96	     "parameters": {"type": "object",
    97	                    "properties": {"street": {"type": "string"}},
    98	                    "required": ["street"]}},
    99	]
   100	
   101	
   102	def openai_tools() -> list[dict]:
   103	    return [{"type": "function", "function": schema}
   104	            for schema in TOOL_SCHEMAS]
   105	
   106	
   107	def _error(code: str, message: str, candidates: list | None = None) -> dict:
   108	    return {"error": {"code": code, "message": message,
   109	                      "candidates": candidates or []}}
   110	
   111	
   112	def _saved_customer(client: PizzaSim, first_name: str) -> dict | None:
   113	    """Case-insensitive match on the unique-per-pizzeria first name.
   114	    Deleted customers are already filtered by the client. Raises
   115	    PizzaSimError upward — dispatch maps it to api_unavailable, which the
   116	    prompt treats as non-fatal (fall back to asking for the street)."""
   117	    for record in client.list_customers():
   118	        if record.get("first_name", "").lower() == first_name.lower():
   119	            return record
   120	    return None
   121	
   122	
   123	def _int_qty(value) -> int:
   124	    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
   125	        raise MenuError(
   126	            "invalid_quantity",
   127	            "I need the quantity as a plain number, please.",
   128	            [],
   129	        )
   130	    return value
   131	
   132	
   133	def dispatch(order: Order, menu: Menu, client: PizzaSim,
   134	             name: str, args: dict) -> dict:
   135	    """Execute one tool call. Never raises — every failure is a tool
   136	    result the model must deal with in front of the customer."""
   137	    try:
   138	        return _dispatch(order, menu, client, name, args)
   139	    except MenuError as exc:
   140	        return _error(exc.code, exc.message, exc.candidates)
   141	    except state.TransitionError as exc:
   142	        return _error(exc.code, exc.message)
   143	    except AuthError:
   144	        return _error("api_unavailable",
   145	                      "I can't reach the kitchen system right now.")
   146	    except ApiTimeout:
   147	        return _error("api_unavailable",
   148	                      "The kitchen system isn't answering right now.")
   149	    except PizzaSimError:
   150	        return _error("api_unavailable",
   151	                      "The kitchen system isn't answering right now.")
   152	
   153	
   154	def _dispatch(order: Order, menu: Menu, client: PizzaSim,
   155	              name: str, args: dict) -> dict:
   156	    if name == "get_menu":
   157	        return {"menu": menu.as_tool_result(), "snapshot": order.snapshot()}
   158	
   159	    if name == "add_items":
   160	        items = []
   161	        for raw in args.get("items", []):
   162	            extras = raw.get("extras") or []
   163	            menu.validate_extras(extras)
   164	            items.append(Item(
   165	                type=raw.get("type", ""),
   166	                code=raw.get("code", ""),
   167	                name=menu.display_name(raw.get("type", ""),
   168	                                       raw.get("code", "")),
   169	                qty=_int_qty(raw.get("qty")),
   170	                extras=extras,
   171	                unit_price=menu.price(raw.get("type", ""),
   172	                                      raw.get("code", "")),
   173	            ))  # any failure above rejects the whole call — atomic
   174	        if not items:
   175	            return _error("invalid_quantity", "What can I get you?")
   176	        state.add_items(order, items)
   177	        return {"snapshot": order.snapshot()}
   178	
   179	    if name == "remove_item":
   180	        qty = args.get("qty")
   181	        state.remove_item(order, args.get("type", ""), args.get("code", ""),
   182	                          None if qty is None else _int_qty(qty))
   183	        return {"snapshot": order.snapshot()}
   184	
   185	    if name == "lookup_customer":
   186	        first_name = (args.get("first_name") or "").strip()
   187	        if not first_name:
   188	            return _error("invalid_arguments", "I still need a name.")
   189	        record = _saved_customer(client, first_name)
   190	        return {"customer_exists": record is not None,
   191	                "saved_street_available": bool(record
   192	                                               and record.get("street_one")),
   193	                "snapshot": order.snapshot()}
   194	
   195	    if name == "set_customer":
   196	        first_name = (args.get("first_name") or "").strip()
   197	        if not first_name:
   198	            return _error("invalid_state", "I still need a name.")
   199	        street = args.get("street_one") or None
   200	        if args.get("use_saved_street"):
   201	            if street:
   202	                return _error(
   203	                    "invalid_arguments",
   204	                    "Either a street or the saved address — not both.")
   205	            record = _saved_customer(client, first_name)
   206	            if not record or not record.get("street_one"):
   207	                return _error(
   208	                    "no_saved_street",
   209	                    "I don't have a saved address under that name — "
   210	                    "what's the street?")
   211	            # The code copies the saved street; canonical name casing from
   212	            # the record prevents a ghost-customer near-duplicate.
   213	            customer = Customer(record["first_name"],
   214	                                record["street_one"],
   215	                                street_from_saved=True)
   216	        else:
   217	            customer = Customer(first_name, street)
   218	        state.set_customer(order, customer)
   219	        return {"customer": customer.as_dict(),
   220	                "snapshot": order.snapshot()}
   221	
   222	    if name == "read_back":
   223	        state.read_back(order)
   224	        return {"snapshot": order.snapshot()}
   225	
   226	    if name == "confirm_order":
   227	        revision = args.get("revision")
   228	        if isinstance(revision, bool) or not isinstance(revision, int):
   229	            return _error("stale_revision",
   230	                          "The order changed — let me read it back again.")

 succeeded in 651ms:
    38	
    39	@dataclass
    40	class Customer:
    41	    first_name: str
    42	    street_one: str | None = None
    43	    # True when street_one was copied from saved customer data: the text
    44	    # then never appears in snapshots, events, transcripts or logs — only
    45	    # in the outbound submit payload (SPEC saved-street redaction).
    46	    street_from_saved: bool = False
    47	
    48	    def as_dict(self) -> dict:
    49	        """Redacted view: feeds SNAPSHOT and thereby every tool result,
    50	        streamed event, model-visible message and log line."""
    51	        if self.street_from_saved:
    52	            return {"first_name": self.first_name, "street_one": None,
    53	                    "street_on_file": True}
    54	        return {"first_name": self.first_name, "street_one": self.street_one}
    55	
    56	    def as_submit_dict(self) -> dict:
    57	        """The real thing — used only to build the POST /orders body."""
    58	        body = {"first_name": self.first_name}
    59	        if self.street_one:
    60	            body["street_one"] = self.street_one
    61	        return body
    62	
    63	
    64	@dataclass
    65	class Order:
    66	    items: list[Item] = field(default_factory=list)
    67	    customer: Customer | None = None
    68	    revision: int = 0
    69	    read_back_revision: int | None = None
    70	    state: State = State.EMPTY

 succeeded in 596ms:
   160	  document.querySelectorAll(".readback button").forEach((b) => {
   161	    b.disabled = true;
   162	  });
   163	}
   164	
   165	function showReadback(snapshot) {
   166	  disableConfirm();
   167	  const panel = document.createElement("div");
   168	  panel.className = "readback";
   169	  const list = snapshot.items
   170	    .map((i) => `${i.qty}× ${i.name} — ${euro(i.line_total)}`)
   171	    .join("\n");
   172	  const who = snapshot.customer
   173	    ? `${snapshot.customer.first_name}` +
   174	      (snapshot.customer.street_on_file
   175	        ? `, ${t("savedAddress")}`  // never the saved text (SPEC redaction)
   176	        : snapshot.customer.street_one
   177	          ? `, ${snapshot.customer.street_one}` : "")
   178	    : "";
   179	  panel.textContent =
   180	    `${who}\n${list}\n${t("total")}: ${euro(snapshot.basket_total)}`;
   181	  const btn = document.createElement("button");
   182	  btn.textContent = t("confirm");
   183	  btn.onclick = () => { btn.disabled = true; confirmOrder(snapshot.revision); };
   184	  panel.appendChild(btn);
   185	  chat.appendChild(panel);
   186	  chat.scrollTop = chat.scrollHeight;
   187	}
   188	
   189	/* ---------- streaming --------------------------------------------------- */
   190	
   191	async function readStream(response, retry) {
   192	  const steps = document.createElement("details");
   193	  steps.className = "steps";
   194	  steps.innerHTML = `<summary>${t("steps")}</summary>`;
   195	  chat.appendChild(steps);
   196	
   197	  let assistantAnswered = false;
   198	  let finalText = "";
   199	  const reader = response.body.getReader();
   200	  const decoder = new TextDecoder();
   201	  let buffer = "";
   202	  for (;;) {
   203	    const { done, value } = await reader.read();
   204	    if (done) break;
   205	    buffer += decoder.decode(value, { stream: true });
   206	    let nl;
   207	    while ((nl = buffer.indexOf("\n")) >= 0) {
   208	      const line = buffer.slice(0, nl); buffer = buffer.slice(nl + 1);
   209	      if (!line.trim()) continue;
   210	      const ev = JSON.parse(line);
   211	      if (ev.type === "tool_call" || ev.type === "tool_result") {
   212	        const pre = document.createElement("pre");
   213	        pre.textContent = (ev.type === "tool_call" ? "→ " : "← ")
   214	          + (ev.tool || "") + " " + JSON.stringify(ev.args ?? ev.result);
   215	        steps.appendChild(pre);
   216	        if (ev.type === "tool_result" && !ev.result.error) {
   217	          if (ev.result.order_id) lastOrderId = ev.result.order_id;
   218	          if (ev.result.snapshot) {
   219	            renderBasket(ev.result.snapshot);
   220	            if (ev.tool === "read_back") showReadback(ev.result.snapshot);
   221	          }
   222	        }
   223	      } else if (ev.type === "assistant") {
   224	        if (ev.text && ev.text.trim()) {
   225	          assistantAnswered = true;
   226	          finalText = ev.text;
   227	          addMsg("assistant", ev.text);
   228	        }
   229	      } else if (ev.type === "done") {
   230	        renderBasket(ev.state);
   231	      }
   232	    }
   233	  }
   234	  if (!steps.querySelector("pre")) steps.remove();
   235	  if (!assistantAnswered) notice(t("notAnswered"), retry);
   236	  return finalText;
   237	}
   238	
   239	const STREAM_TIMEOUT_MS = 120000;
   240	
   241	async function streamPost(path, body, retry) {
   242	  currentAbort = new AbortController();
   243	  // Real client-side timeout: covers the request AND the streamed body,
   244	  // so the timeout notice + resend control can actually occur.
   245	  const signal = AbortSignal.any(
   246	    [currentAbort.signal, AbortSignal.timeout(STREAM_TIMEOUT_MS)]);
   247	  const working = document.createElement("div");
   248	  working.className = "working";
   249	  working.textContent = t("working");
   250	  chat.appendChild(working);
   251	  $("send").disabled = true;
   252	  let finalText = "";
   253	  try {
   254	    const res = await fetch(path, {
   255	      method: "POST",
   256	      headers: { "Content-Type": "application/json" },
   257	      body: JSON.stringify(body),
   258	      signal,
   259	    });
   260	    if (res.status === 404) {
   261	      // The server no longer knows this session: recreate transparently.
   262	      // A chat message stays recoverable via resend; a pending confirm is
   263	      // NOT re-offered — the new session holds a new, empty order, so its
   264	      // revision would be meaningless.
   265	      working.remove();
   266	      await startSession(session.pizzeriaId);
   267	      notice(t("sessionLost"),
   268	             typeof retry === "string" ? retry : undefined);
   269	      $("send").disabled = false;
   270	      return "";
   271	    }
   272	    if (res.status === 409) { working.remove(); notice(t("busy")); return ""; }
   273	    if (!res.ok) throw new Error("http");
   274	    working.remove();
   275	    finalText = await readStream(res, retry);
   276	  } catch (err) {
   277	    working.remove();
   278	    if (err.name === "AbortError") { /* deliberate: switch/start-over */ }
   279	    else if (err.name === "TimeoutError") notice(t("errTimeout"), retry);
   280	    else if (err.message === "http") notice(t("errHttp"), retry);
   281	    else notice(t("errNetwork"), retry);
   282	  }
   283	  $("send").disabled = false;
   284	  $("text").focus();
   285	  return finalText;
   286	}
   287	
   288	async function sendTurn(text, spoken = false) {
   289	  if (text !== null) addMsg("user", text);
   290	  const finalText = await streamPost(
   291	    "/chat", { session_id: session.id, text, spoken }, text ?? undefined);
   292	  if (finalText && cfg.speech && $("tts-toggle").checked) speak(finalText);
   293	}
   294	
   295	async function confirmOrder(revision) {
   296	  // The retry re-runs the confirm with the SAME revision: if the first
   297	  // attempt actually went through, the state machine refuses it and the
   298	  // agent says so — never a second order.
   299	  const finalText = await streamPost(
   300	    "/confirm", { session_id: session.id, revision },
   301	    () => confirmOrder(revision));
   302	  if (finalText && cfg.speech && $("tts-toggle").checked) speak(finalText);
   303	}
   304	
   305	/* ---------- sessions / tenancy ----------------------------------------- */
   306	
   307	function fillSelector() {
   308	  const select = $("pizzeria-select");
   309	  if (!cfg.pizzerias) {
   310	    select.hidden = true;
   311	    $("list-unavailable").hidden = false;
   312	    return;
   313	  }
   314	  select.hidden = false;
   315	  $("list-unavailable").hidden = true;
   316	  select.textContent = "";
   317	  for (const p of cfg.pizzerias) {
   318	    const opt = document.createElement("option");
   319	    opt.value = p.id;
   320	    opt.textContent = `${p.name} (${p.id.slice(0, 8)})`;
   321	    select.appendChild(opt);
   322	  }
   323	  if (session) select.value = session.pizzeriaId;
   324	}
   325	
   326	async function refreshConfig() {
   327	  cfg = await (await fetch("/config")).json();
   328	  $("version").textContent = "v" + cfg.version;
   329	  $("docs-link").href = cfg.docs_url;
   330	  fillSelector();
   331	  // Voice UI only in a secure context (HTTPS/localhost): plain HTTP must
   332	  // never present a voice-capable UI (SPEC).
   333	  const speechUsable = cfg.speech && window.isSecureContext;
   334	  $("tts-wrap").hidden = !speechUsable;
   335	  $("mic").hidden = !(speechUsable && navigator.mediaDevices &&
   336	                      window.MediaRecorder);
   337	}
   338	
   339	async function startSession(pizzeriaId) {
   340	  // Create the new session FIRST: a failed switch must not hide the
   341	  // still-live conversation and basket the customer can see.
   342	  const res = await fetch("/session", {
   343	    method: "POST",
   344	    headers: { "Content-Type": "application/json" },
   345	    body: JSON.stringify({ pizzeria_id: pizzeriaId, lang }),
   346	  });
   347	  if (!res.ok) {
   348	    notice(t("sessionGone"));
   349	    await refreshConfig();  // fresh selector from the live list
   350	    if (session) $("pizzeria-select").value = session.pizzeriaId;
   351	    return;
   352	  }
   353	  if (currentAbort) currentAbort.abort();
   354	  chat.textContent = "";
   355	  lastOrderId = null;
   356	  renderBasket({ items: [], basket_total: 0, state: "EMPTY",
   357	                 customer: null });
   358	  const data = await res.json();
   359	  session = { id: data.session_id, pizzeriaId: data.pizzeria_id,
   360	              pizzeriaName: data.pizzeria_name };
   361	  $("pizzeria-name").textContent = data.pizzeria_name;
   362	  document.title = data.pizzeria_name;
   363	  $("dashboard-link").hidden = false;
   364	  $("dashboard-link").href = `${cfg.dashboard_base}/${data.pizzeria_id}`;
   365	  $("uuid").textContent = data.pizzeria_id;
   366	  $("pizzeria-select").value = data.pizzeria_id;
   367	  await sendTurn(null);  // the agent greets first
   368	}
   369	
   370	/* ---------- speech (capture/playback only) ------------------------------ */
   371	
   372	let recorder = null;
   373	
   374	async function startRecording() {
   375	  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
   376	  recorder = new MediaRecorder(stream);
   377	  const chunks = [];
   378	  recorder.ondataavailable = (e) => chunks.push(e.data);
   379	  recorder.onstop = async () => {
   380	    stream.getTracks().forEach((tr) => tr.stop());
   381	    $("mic").classList.remove("recording");
   382	    $("mic").setAttribute("aria-pressed", "false");
   383	    const blob = new Blob(chunks, { type: recorder.mimeType });
   384	    const body = new FormData();
   385	    body.append("audio", blob, "speech.webm");
   386	    try {
   387	      const res = await fetch(
   388	        `/speech/stt?session_id=${session.id}`, { method: "POST", body });
   389	      if (!res.ok) throw new Error();
   390	      const { text } = await res.json();
   391	      if (text.trim()) sendTurn(text.trim(), true);
   392	      else notice(t("sttEmpty"));
   393	    } catch {
   394	      notice(t("sttFail"));
   395	      degradeSpeech();  // runtime outage → text-only for this session
   396	    }
   397	  };
   398	  recorder.start();
   399	  $("mic").classList.add("recording");
   400	  $("mic").setAttribute("aria-pressed", "true");
   401	}
   402	
   403	$("mic").addEventListener("click", () => {
   404	  if (recorder && recorder.state === "recording") recorder.stop();
   405	  else startRecording().catch(() => notice(t("micDenied")));
   406	});
   407	
   408	async function speak(text) {
   409	  try {
   410	    const res = await fetch("/speech/tts", {
   411	      method: "POST",
   412	      headers: { "Content-Type": "application/json" },
   413	      body: JSON.stringify({ session_id: session.id, text }),
   414	    });
   415	    if (!res.ok) throw new Error();
   416	    new Audio(URL.createObjectURL(await res.blob())).play();
   417	  } catch {
   418	    notice(t("ttsFail"));
   419	    degradeSpeech();  // runtime outage → text-only for this session
   420	  }
   421	}
   422	
   423	function degradeSpeech() {
   424	  $("mic").hidden = true;
   425	  $("tts-wrap").hidden = true;
   426	}
   427	
   428	/* ---------- health ------------------------------------------------------ */
   429	
   430	async function pollHealth() {
   431	  try {
   432	    const h = await (await fetch("/health")).json();
   433	    for (const [id, state] of [["health-api", h.api],
   434	                               ["health-gateway", h.gateway]]) {
   435	      const el = $(id);
   436	      el.classList.remove("ok", "down", "unknown");
   437	      el.classList.add(state);
   438	      el.title = state;
   439	    }
   440	  } catch { /* footer badge keeps its last state */ }

 succeeded in 639ms:
   288	                    "order_id": found["id"],
   289	                    "status": found.get("status", "ordered"),
   290	                    "eta_seconds": eta,
   291	                })
   292	                return {**order.result, "snapshot": order.snapshot()}
   293	        # verified absent (or a different order) → exactly one real retry
   294	
   295	    customer = order.customer.as_submit_dict()
   296	    items = [{"type": i.type, "code": i.code, "qty": i.qty,
   297	              "extras": list(i.extras)} for i in order.items]
   298	    try:
   299	        result = client.submit_order(customer, items)
   300	    except ValidationError as exc:
   301	        return _error("submit_failed",
   302	                      "The kitchen rejected part of the order: "
   303	                      + "; ".join(exc.details))
   304	    except AuthError:
   305	        return _error("api_unavailable",

exec
/bin/bash -lc "nl -ba tests/test_tools.py | sed -n '467,590p'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "nl -ba deploy/speech-service.compose.yml | sed -n '1,80p'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "nl -ba tests/test_web_speech.py | sed -n '130,320p'" in /home/rob/bpm-pizza-vibecoding-solution
exec
/bin/bash -lc "nl -ba tests/test_transcripts.py | sed -n '75,150p'" in /home/rob/bpm-pizza-vibecoding-solution
 succeeded in 289ms:
   467	         "street_one": "Meyer Teststraße 4", "street_two": None,
   468	         "created_at": 1, "deleted_at": None}
   469	
   470	
   471	def test_lookup_customer_known_and_unknown(menu, fake):
   472	    fake.customers = [SAVED]
   473	    result = tools.dispatch(Order(), menu, fake, "lookup_customer",
   474	                            {"first_name": "marko"})  # case-insensitive
   475	    assert result["customer_exists"] is True
   476	    assert result["saved_street_available"] is True
   477	    assert "Meyer" not in json.dumps(result)  # booleans only, never text
   478	    result = tools.dispatch(Order(), menu, fake, "lookup_customer",
   479	                            {"first_name": "Nessuno"})
   480	    assert result == {"customer_exists": False,
   481	                      "saved_street_available": False,
   482	                      "snapshot": result["snapshot"]}
   483	
   484	
   485	def test_lookup_customer_without_saved_street(menu, fake):
   486	    fake.customers = [{**SAVED, "street_one": None}]
   487	    result = tools.dispatch(Order(), menu, fake, "lookup_customer",
   488	                            {"first_name": "Marko"})
   489	    assert result["customer_exists"] is True
   490	    assert result["saved_street_available"] is False
   491	
   492	
   493	def test_lookup_customer_api_error_is_nonfatal_tool_error(menu, fake):
   494	    fake.customers_effect = ApiTimeout("t")
   495	    result = tools.dispatch(Order(), menu, fake, "lookup_customer",
   496	                            {"first_name": "Marko"})
   497	    assert result["error"]["code"] == "api_unavailable"
   498	
   499	
   500	def test_use_saved_street_copies_in_code(menu, fake):
   501	    fake.customers = [SAVED]
   502	    order = Order()
   503	    result = tools.dispatch(order, menu, fake, "set_customer",
   504	                            {"first_name": "marko",
   505	                             "use_saved_street": True})
   506	    assert "error" not in result
   507	    # canonical casing from the record — no ghost near-duplicate
   508	    assert order.customer.first_name == "Marko"
   509	    assert order.customer.street_one == "Meyer Teststraße 4"
   510	    assert order.customer.street_from_saved is True
   511	    # redacted view everywhere the model/UI looks
   512	    assert result["customer"] == {"first_name": "Marko",
   513	                                  "street_one": None,
   514	                                  "street_on_file": True}
   515	    assert result["snapshot"]["customer"]["street_on_file"] is True
   516	    assert "Meyer" not in json.dumps(result)
   517	
   518	
   519	def test_use_saved_street_mutually_exclusive_and_missing(menu, fake):
   520	    fake.customers = [SAVED]
   521	    result = tools.dispatch(Order(), menu, fake, "set_customer",
   522	                            {"first_name": "Marko",
   523	                             "street_one": "via Roma",
   524	                             "use_saved_street": True})
   525	    assert result["error"]["code"] == "invalid_arguments"
   526	    fake.customers = []
   527	    result = tools.dispatch(Order(), menu, fake, "set_customer",
   528	                            {"first_name": "Marko",
   529	                             "use_saved_street": True})
   530	    assert result["error"]["code"] == "no_saved_street"
   531	
   532	
   533	def test_dictated_street_still_echoed_and_submitted(menu, fake):
   534	    order = Order()
   535	    result = tools.dispatch(order, menu, fake, "set_customer",
   536	                            {"first_name": "Anna",
   537	                             "street_one": "via Roma 1"})
   538	    assert result["customer"]["street_one"] == "via Roma 1"  # own input
   539	    assert "street_on_file" not in result["customer"]
   540	
   541	
   542	def test_saved_street_redaction_end_to_end(menu, fake):
   543	    """The saved street text appears in exactly ONE place: the outbound
   544	    submit payload. Not in any snapshot, emitted event, log line, or
   545	    model-visible message."""
   546	    from core.agent import Agent, LOG_DIR, Session as AgentSession
   547	    fake.customers = [SAVED]
   548	    captured = {}
   549	    real_submit = fake.submit_order
   550	
   551	    def spy(customer, items):
   552	        captured["customer"] = customer
   553	        return real_submit(customer, items)
   554	    fake.submit_order = spy
   555	
   556	    script = iter([
   557	        [("lookup_customer", {"first_name": "Marko"})],
   558	        [("set_customer", {"first_name": "Marko",
   559	                           "use_saved_street": True}),
   560	         ("add_items", {"items": [{"type": "pizza", "code": "margherita",
   561	                                   "qty": 1}]}),
   562	         ("read_back", {})],
   563	    ])
   564	
   565	    def stub(messages, tool_schemas):
   566	        calls = next(script, None)
   567	        if calls:
   568	            return {"tool_calls": [
   569	                {"id": f"c-{name}", "type": "function",
   570	                 "function": {"name": name, "arguments": json.dumps(args)}}
   571	                for name, args in calls]}
   572	        return {"content": "Passt das so?"}
   573	
   574	    session = AgentSession(order=Order(), menu=menu,
   575	                           messages=[{"role": "system", "content": "s"}],
   576	                           client=fake)
   577	    agent = Agent(config_stub(), chat_fn=stub)
   578	    events = []
   579	    agent.run_turn(session, "Ich heiße Marko", events.append)
   580	    agent.run_turn(session, "Eine Margherita, gespeicherte Adresse",
   581	                   events.append)
   582	    agent.confirm_and_submit(session, session.order.revision, events.append)
   583	
   584	    street = "Meyer Teststraße 4"
   585	    assert captured["customer"]["street_one"] == street  # the ONE place
   586	    assert street not in json.dumps(events, ensure_ascii=False)
   587	    assert street not in json.dumps(session.messages, ensure_ascii=False)
   588	    log_text = "".join(
   589	        f.read_text() for f in LOG_DIR.glob(f"agent-{session.id}.jsonl"))
   590	    assert street not in log_text

 succeeded in 318ms:
     1	# Self-hosted, CPU-only speech service for the PizzaSim ordering agent.
     2	#
     3	# Neutral by design (SPEC): the image and the models are operator
     4	# configuration — no vendor or model names live in this repository.
     5	# Whatever image the operator picks MUST expose an OpenAI-compatible
     6	# surface on its HTTP port:
     7	#
     8	#   POST /v1/audio/transcriptions   multipart: file, model, language -> {"text": ...}
     9	#   POST /v1/audio/speech           JSON: model, voice, input -> audio bytes
    10	#   GET  /v1/models                 2xx = alive (used by the app's startup probe)
    11	#
    12	# The app and this service are deployed together as first-party artifacts;
    13	# the app reaches it via SPEECH_URL (e.g. http://speech:8000 on a shared
    14	# network, or the routed URL). Voice-capable deployments serve the app
    15	# over HTTPS on a real host name — microphone capture does not exist on
    16	# plain HTTP (SPEC).
    17	services:
    18	  speech:
    19	    image: ${SPEECH_IMAGE}
    20	    restart: unless-stopped
    21	    # CPU-only on purpose: no GPU reservations, modest resources.
    22	    environment:
    23	      - SPEECH_STT_MODEL=${SPEECH_STT_MODEL}
    24	      - SPEECH_TTS_MODEL=${SPEECH_TTS_MODEL}
    25	      - SPEECH_TTS_VOICE=${SPEECH_TTS_VOICE}
    26	    expose:
    27	      - "${SPEECH_CONTAINER_PORT:-8000}"

 succeeded in 317ms:
   130	        browser.close()
   131	
   132	
   133	def open_app(new_page, stack, init_script=None):
   134	    page = new_page()
   135	    if init_script:
   136	        page.add_init_script(init_script)
   137	    page.goto(stack["url"], timeout=30000)
   138	    page.wait_for_selector(".msg.assistant", timeout=30000)
   139	    return page
   140	
   141	
   142	def test_e2e_voice_push_to_talk_round_trip(voice_page_factory, stack):
   143	    stack["gateway"].mode = "ok"
   144	    stack["gateway"].saw_spoken_note = False
   145	    page = open_app(voice_page_factory, stack)
   146	    # controls visible on a secure context with speech configured
   147	    assert page.locator("#mic").is_visible()
   148	    assert page.locator("#tts-wrap").is_visible()
   149	    assert not page.locator("#tts-toggle").is_checked()  # off by default
   150	
   151	    page.click("#mic")  # push-to-talk: start
   152	    page.wait_for_selector("#mic.recording", timeout=10000)  # visible state
   153	    page.wait_for_timeout(1200)
   154	    page.click("#mic")  # stop → upload → stub transcript drives the turn
   155	    page.wait_for_selector("text=Zwei Margherita bitte", timeout=30000)
   156	    page.wait_for_selector("#basket-lines li", timeout=30000)
   157	    assert "2× Margherita" in page.locator("#basket-lines").inner_text()
   158	    assert stack["gateway"].saw_spoken_note  # spoken-style note reached model
   159	    page.close()
   160	
   161	
   162	def test_e2e_tts_fetched_once_for_final_message_only(voice_page_factory,
   163	                                                     stack):
   164	    stack["gateway"].mode = "ok"
   165	    page = open_app(voice_page_factory, stack)
   166	    page.check("#tts-toggle")
   167	    before = stack["speech"].tts_calls
   168	    page.fill("#text", "Was kostet eine Margherita?")
   169	    page.click("#send")
   170	    page.wait_for_selector("text=8.5 €", timeout=30000)
   171	    page.wait_for_function(
   172	        f"() => fetch('/config').then(() => true) && true", timeout=5000)
   173	    page.wait_for_timeout(800)  # allow the TTS fetch to complete
   174	    # the turn contained a tool step AND a final message → exactly one TTS
   175	    assert stack["speech"].tts_calls == before + 1
   176	    page.close()
   177	
   178	
   179	def test_e2e_runtime_speech_outage_degrades_to_text(voice_page_factory,
   180	                                                    stack):
   181	    stack["gateway"].mode = "ok"
   182	    page = open_app(voice_page_factory, stack)
   183	    stack["speech"].mode = "fail"
   184	    try:
   185	        page.click("#mic")
   186	        page.wait_for_selector("#mic.recording", timeout=10000)
   187	        page.wait_for_timeout(900)
   188	        page.click("#mic")  # upload fails → degrade
   189	        page.wait_for_selector(".notice", timeout=30000)
   190	        page.wait_for_selector("#mic", state="hidden", timeout=10000)
   191	        assert page.locator("#tts-wrap").is_hidden()
   192	        # typed ordering continues untouched
   193	        page.fill("#text", "Zwei Margherita bitte")
   194	        page.click("#send")
   195	        page.wait_for_selector("#basket-lines li", timeout=30000)
   196	    finally:
   197	        stack["speech"].mode = "ok"
   198	    page.close()
   199	
   200	
   201	# --- live voice acceptance (opt-in, release-gating per SPEC) ---------------
   202	
   203	LIVE_VOICE = (os.environ.get("PIZZA_LIVE_VOICE") == "1"
   204	              and bool(os.environ.get("PIZZA_LIVE_VOICE_URL")))
   205	
   206	
   207	@pytest.mark.skipif(not LIVE_VOICE,
   208	                    reason="live voice test only with PIZZA_LIVE_VOICE=1 "
   209	                           "and PIZZA_LIVE_VOICE_URL=<https deployment>")
   210	@pytest.mark.parametrize("lang,fixture,name_reply,yes", [
   211	    ("de", "order.de.wav", "Ich heiße VoiceTest", "Ja"),
   212	    ("en", "order.en.wav", "My name is VoiceTest", "Yes"),
   213	])
   214	def test_live_voice_acceptance(lang, fixture, name_reply, yes):
   215	    """The voice agent actually works: real browser over HTTPS, real
   216	    microphone capture (fake device streaming the spoken-order fixture),
   217	    real STT, the confirm control, real TTS — then the order is verified
   218	    via the pizzeria's API endpoints. Not a text replay: if STT does not
   219	    produce an order-driving transcript, this test fails."""
   220	    from playwright.sync_api import sync_playwright
   221	
   222	    from core.pizzasim import PizzaSim
   223	
   224	    base_url = os.environ["PIZZA_LIVE_VOICE_URL"]
   225	    wav = str((AUDIO / fixture).resolve())
   226	    tts_audio = {"bytes": 0}
   227	
   228	    with sync_playwright() as p:
   229	        browser = p.chromium.launch(args=[
   230	            "--use-fake-device-for-media-capture",
   231	            "--use-fake-ui-for-media-capture",
   232	            f"--use-file-for-fake-audio-capture={wav}",
   233	        ])
   234	        context = browser.new_context()
   235	        context.grant_permissions(["microphone"], origin=base_url)
   236	        page = context.new_page()
   237	
   238	        def sniff(response):
   239	            if response.url.endswith("/speech/tts") and response.ok:
   240	                tts_audio["bytes"] = len(response.body())
   241	        page.on("response", sniff)
   242	
   243	        page.goto(base_url, timeout=60000)
   244	        page.wait_for_selector(".msg.assistant", timeout=120000)
   245	        if lang == "en":
   246	            page.locator("#lang-switch button[data-lang=en]").click()
   247	        assert page.locator("#mic").is_visible()  # HTTPS + speech up
   248	        page.check("#tts-toggle")
   249	
   250	        page.click("#mic")
   251	        page.wait_for_selector("#mic.recording", timeout=15000)
   252	        page.wait_for_timeout(7000)  # the fixture is ~5.5s of speech
   253	        page.click("#mic")
   254	        # STT must yield an order-driving transcript: the basket fills.
   255	        page.wait_for_selector("#basket-lines li", timeout=120000)
   256	
   257	        page.fill("#text", name_reply)
   258	        page.click("#send")
   259	        page.wait_for_selector(".readback button:enabled", timeout=120000)
   260	        page.locator(".readback button:enabled").click()
   261	        page.wait_for_selector("#submitted-banner:not([hidden])",
   262	                               timeout=120000)
   263	        page.wait_for_timeout(2000)  # allow the final TTS fetch
   264	        assert tts_audio["bytes"] > 0  # real, non-empty playable audio
   265	        pizzeria_id = page.locator("#uuid").inner_text().strip()
   266	        banner = page.locator("#submitted-banner").inner_text()
   267	        order_id = banner.split()[-1]
   268	        browser.close()
   269	
   270	    # verify via the API: right customer, items present, right tenant
   271	    client = PizzaSim.from_env().for_pizzeria(pizzeria_id)
   272	    listed = {o["id"] for o in client.list_orders()}
   273	    assert order_id in listed
   274	    detail = client.get_order(order_id)
   275	    assert detail["customer"]["first_name"] == "VoiceTest"
   276	    assert detail["items"], "order carries no items"
   277	
   278	
   279	def test_e2e_insecure_context_renders_no_voice_ui(voice_page_factory,
   280	                                                  stack):
   281	    """Plain HTTP never presents a voice-capable UI — even with speech
   282	    fully configured server-side."""
   283	    stack["gateway"].mode = "ok"
   284	    page = open_app(
   285	        voice_page_factory, stack,
   286	        init_script="Object.defineProperty(window, 'isSecureContext',"
   287	                    " {value: false});")
   288	    assert page.locator("#mic").is_hidden()
   289	    assert page.locator("#tts-wrap").is_hidden()
   290	    page.fill("#text", "Zwei Margherita bitte")  # text ordering works
   291	    page.click("#send")
   292	    page.wait_for_selector("#basket-lines li", timeout=30000)
   293	    page.close()

 succeeded in 320ms:
    75	        return [{"id": "c-1", "first_name": "Marko",
    76	                 "street_one": "Meyer Teststraße 4", "street_two": None,
    77	                 "created_at": 1, "deleted_at": None}]
    78	
    79	    def check_street(self, street):
    80	        return {"street": street, "deliverable": True}
    81	
    82	
    83	@pytest.mark.parametrize("path", TRANSCRIPTS, ids=lambda p: p.stem)
    84	def test_golden_transcript(path):
    85	    transcript = json.loads(path.read_text())
    86	    stub = StubModel(transcript["turns"])
    87	    client = ScriptedClient(transcript["fake"])
    88	    config = AgentConfig(url="http://unused", key="unused",
    89	                         model="stub", lang="de")
    90	    menu = Menu(json.loads((FIXTURES / "menu.json").read_text()))
    91	    session = Session(order=Order(), menu=menu,
    92	                      messages=[{"role": "system", "content": "stub"}],
    93	                      client=client)
    94	    agent = Agent(config, chat_fn=stub)
    95	
    96	    calls, error_codes, ordered = [], [], []
    97	
    98	    def emit(event):
    99	        if event["type"] == "tool_call":
   100	            calls.append(event["tool"])
   101	            ordered.append(("call", event["tool"]))
   102	        if event["type"] == "assistant":
   103	            ordered.append(("say", event["text"]))
   104	        if event["type"] == "tool_result" and "error" in event["result"]:
   105	            error_codes.append(event["result"]["error"]["code"])
   106	
   107	    for turn in transcript["turns"]:
   108	        stub.next_turn()
   109	        final = agent.run_turn(session, turn["user"], emit)
   110	        assert final == turn["script"][-1]["say"]
   111	
   112	    expect = transcript["expect"]
   113	    assert session.order.state.value == expect["state"]
   114	    assert calls == expect["calls"]
   115	    assert error_codes == expect["error_codes"]
   116	    actual_items = [{"type": i.type, "code": i.code, "qty": i.qty}
   117	                    for i in session.order.items]
   118	    assert actual_items == expect["items"]
   119	    if "order_id" in expect:
   120	        assert session.order.result["order_id"] == expect["order_id"]
   121	    if expect["state"] == "SUBMITTED":
   122	        assert session.order.result["order_id"]
   123	    if "customer_saved" in expect:
   124	        assert session.order.customer.street_from_saved == \
   125	            expect["customer_saved"]
   126	        if expect["customer_saved"]:
   127	            # redaction: the saved street never enters the model context
   128	            assert "Meyer Teststraße" not in json.dumps(
   129	                session.messages, ensure_ascii=False)
   130	    if "customer_first_name" in expect:
   131	        assert session.order.customer.first_name == \
   132	            expect["customer_first_name"]
   133	    if "set_customer_calls" in expect:
   134	        assert calls.count("set_customer") == expect["set_customer_calls"]
   135	    if expect.get("name_confirm_before_set"):
   136	        # the spoken name is confirmed BEFORE the customer is stored —
   137	        # the ghost-customer guard for voice flows
   138	        confirm_idx = next(i for i, (kind, value) in enumerate(ordered)
   139	                           if kind == "say"
   140	                           and "richtig verstanden" in value)
   141	        set_idx = next(i for i, (kind, value) in enumerate(ordered)
   142	                       if kind == "call" and value == "set_customer")
   143	        assert confirm_idx < set_idx
   144	
   145	
   146	def test_transcripts_exist():
   147	    # five v1 flows + saved-address pair + three name-confirmation cases
   148	    assert len(TRANSCRIPTS) == 10
   149	
   150	

codex
No blocking findings.

The high-risk SPEC points are implemented coherently and are backed by both code and tests. Redaction is correctly split between [`Customer.as_dict()`](/home/rob/bpm-pizza-vibecoding-solution/core/order.py:48) and [`Customer.as_submit_dict()`](/home/rob/bpm-pizza-vibecoding-solution/core/order.py:56), with the only submit-path use at [`_submit()`](/home/rob/bpm-pizza-vibecoding-solution/core/tools.py:295). `lookup_customer` stays boolean-only and `set_customer` enforces the saved-street mutual exclusion / `no_saved_street` paths at [core/tools.py](/home/rob/bpm-pizza-vibecoding-solution/core/tools.py:185). The end-to-end redaction sweep is explicitly asserted in [tests/test_tools.py](/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:542), including absence from events, logs, and `session.messages`. Prompt policy also matches the requested conversation behavior in [prompts/system.en.md](/home/rob/bpm-pizza-vibecoding-solution/prompts/system.en.md:16) and [prompts/system.de.md](/home/rob/bpm-pizza-vibecoding-solution/prompts/system.de.md:16).

The browser voice path also lines up with the SPEC claims. `isSecureContext` gating, saved-address labeling, runtime `degradeSpeech()`, and single-final-message TTS are implemented in [channels/static/app.js](/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js:165), [channels/static/app.js](/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js:288), [channels/static/app.js](/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js:326), and [channels/static/app.js](/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js:374). The live voice acceptance test does fail if STT does not drive an order, because it blocks on basket population at [tests/test_web_speech.py](/home/rob/bpm-pizza-vibecoding-solution/tests/test_web_speech.py:254). The deploy artifact is neutral: [deploy/speech-service.compose.yml](/home/rob/bpm-pizza-vibecoding-solution/deploy/speech-service.compose.yml:1) contains only environment placeholders, no vendor/model names.

I also ran the relevant local suites under `venv`: `tests/test_tools.py` targeted saved-street cases `7 passed`, `tests/test_transcripts.py` `12 passed`, and `tests/test_web_speech.py -k 'not live_voice'` `9 passed` with only two non-blocking FastAPI deprecation warnings about `on_event`.

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
72,514
No blocking findings.

The high-risk SPEC points are implemented coherently and are backed by both code and tests. Redaction is correctly split between [`Customer.as_dict()`](/home/rob/bpm-pizza-vibecoding-solution/core/order.py:48) and [`Customer.as_submit_dict()`](/home/rob/bpm-pizza-vibecoding-solution/core/order.py:56), with the only submit-path use at [`_submit()`](/home/rob/bpm-pizza-vibecoding-solution/core/tools.py:295). `lookup_customer` stays boolean-only and `set_customer` enforces the saved-street mutual exclusion / `no_saved_street` paths at [core/tools.py](/home/rob/bpm-pizza-vibecoding-solution/core/tools.py:185). The end-to-end redaction sweep is explicitly asserted in [tests/test_tools.py](/home/rob/bpm-pizza-vibecoding-solution/tests/test_tools.py:542), including absence from events, logs, and `session.messages`. Prompt policy also matches the requested conversation behavior in [prompts/system.en.md](/home/rob/bpm-pizza-vibecoding-solution/prompts/system.en.md:16) and [prompts/system.de.md](/home/rob/bpm-pizza-vibecoding-solution/prompts/system.de.md:16).

The browser voice path also lines up with the SPEC claims. `isSecureContext` gating, saved-address labeling, runtime `degradeSpeech()`, and single-final-message TTS are implemented in [channels/static/app.js](/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js:165), [channels/static/app.js](/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js:288), [channels/static/app.js](/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js:326), and [channels/static/app.js](/home/rob/bpm-pizza-vibecoding-solution/channels/static/app.js:374). The live voice acceptance test does fail if STT does not drive an order, because it blocks on basket population at [tests/test_web_speech.py](/home/rob/bpm-pizza-vibecoding-solution/tests/test_web_speech.py:254). The deploy artifact is neutral: [deploy/speech-service.compose.yml](/home/rob/bpm-pizza-vibecoding-solution/deploy/speech-service.compose.yml:1) contains only environment placeholders, no vendor/model names.

I also ran the relevant local suites under `venv`: `tests/test_tools.py` targeted saved-street cases `7 passed`, `tests/test_transcripts.py` `12 passed`, and `tests/test_web_speech.py -k 'not live_voice'` `9 passed` with only two non-blocking FastAPI deprecation warnings about `on_event`.

SCORES (1-5 each, 5 = best):
completeness: 5
correctness: 5
error_handling: 5
simplicity: 4
spec_compliance: 5
TOTAL: 24/25
VERDICT: APPROVED
ISSUES:
