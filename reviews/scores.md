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
