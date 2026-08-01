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
