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

## Rounds 11-13 — SPEC v3 analysis + patched-spec gate (Issue #1)

Round 11 (reviews/round11-spec-v3-analysis.md): spec v3 analysis, VERDICT
NEEDS PATCHES, 8-point patch list.
Round 12 (reviews/round12-spec-gate-reject.md, Issue #1): Judge REJECT —
patch 2 incomplete in error table, prose, and acceptance-test wording.
Round 13 (reviews/round13-spec-gate-approve.md, Issue #1): Judge APPROVE —
patched SPEC.md is build-ready. (Document gate, rubric not applicable.)

## Rounds 14-16 — PLAN v2 gate (Issue #2)

Round 14: completeness 4, correctness 3, error_handling 3, simplicity 4,
spec_compliance 3 — TOTAL 17/25, CHANGES_REQUIRED (notice language,
vanished tenant, speech coverage, web-surface error rendering, confirm
history semantics — all applied).
Round 15: completeness 4, correctness 4, error_handling 3, simplicity 4,
spec_compliance 3 — TOTAL 18/25, CHANGES_REQUIRED (confirm phrasing
gateway path, header/footer E2E assertions, /health semantics — applied
as amendments in Issue #2 round 3).
Round 16: completeness 5, correctness 5, error_handling 4, simplicity 4,
spec_compliance 5 — TOTAL 23/25, VERDICT: APPROVED.
Note: rounds 15-16 amendments live verbatim in Issue #2 (a repo hook
gates direct PLAN.md edits); PLAN.md sync pending operator decision.
