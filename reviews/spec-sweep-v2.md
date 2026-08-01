# Final SPEC sweep — v2 implementation (2026-08-01)

Every SPEC.md requirement, table row, invariant and deliverable, top to
bottom. Status: covered (where) — zero open rows.

## What done looks like
| Req | Where |
|---|---|
| POST returns order id | test_live_acceptance (live, passed) |
| Order in list + dashboard | test_live_acceptance (list endpoint); dashboard link E2E |
| Right customer name | test_live_acceptance (detail endpoint) |
| Exact items/qty, no near match | test_live_acceptance via tools._same_items |
| Failure: wrong pizzeria | immutable Session tenant; test_confirm_endpoint_places_order_in_selected_tenant |
| Failure: double order on retry | recovery verify (test_submit_timeout_then_recovery_via_list, test_recovery_rejects_candidate_with_different_items); confirm retry refused when closed (state order_closed tests) |
| Failure: ghost customer | prompts name confirm; read_back before submit (invariant 3 tests) |
| Failure: submit w/o confirmation | invariant 1 tests; confirm control bound to revision |

## Scope In
| Req | Where |
|---|---|
| CLI transport | channels/cli.py |
| Web FastAPI :8888, NDJSON steps | channels/web.py (__main__ 8888); E2E steps assertions |
| Speech via self-hosted service | channels/speech.py; manual checklist README |
| Several pizzerias, selectable+changeable, PIZZERIA_ID preselects | create_session; /session; selector E2E (switch + vanished) |
| DE+EN mirrored per turn | prompts (both); language-authority in agent.py |
| Menu/prices/cart/customer/submit + correction/removal/abandonment | tools.py; transcripts (correction); remove tests; Start over UI |
| Deterministic tests + live acceptance + browser E2E | 103 offline passed; live passed; 9 Playwright tests |
| Structured logging, 1 JSON line/event | core/agent.py log_event → logs/agent-<session>.jsonl |

## Scope Out — nothing out-of-scope built (prices shown only; no payment,
no own ETA, no accounts, no post-submit changes, no regex parser
(grep-verified), no menu recital in spoken replies, no persistence).

## Environment & config
| Req | Where |
|---|---|
| All 12 vars incl. PIZZERIA_LANG + APP_VERSION | .env.example; require_env/optional_env |
| SPEECH_* optional exception | SpeechService (all-or-nothing) |
| Missing var → exit naming var+file | ConfigError w/ file path; demonstrated live |
| Nothing hardcoded (UUID/model/menu/URL/vendor) | grep-verified; all from env |
| Secrets never in logs/UI | log_event carries no config; reviewed |
| APP_VERSION x.y.z validated | web.boot regex; test via stack env 2.0.0 |

## API contract (verified facts)
| Fact | Where used |
|---|---|
| order_id on POST / id on list | pizzasim.submit_order / list_orders tests |
| Detail endpoint for items | get_order; recovery + acceptance tests |
| Menu shape incl. price | core/menu.py; test_menu_carries_prices |
| extras = toppings vocabulary | validate_extras; tests |
| Error bodies {"error","details"} | _raise_for; test_422_mapped_with_details |
| Status lifecycle | fixtures; recovery status adoption |
| /location weak signal | check_street tool + prompt "never claim checked" |
| Dashboard/docs derived URLs | /config dashboard_base+docs_url; E2E href asserts |
| (type,code) uniqueness | test_tonno_collision_is_per_type; removal tests |

## State machine — invariants
| Inv | Where |
|---|---|
| 1 submit only CONFIRMED | test_submit_outside_confirmed; empty-basket test |
| 2 mutation demotes CONFIRMED | demotion tests (add/remove/set_customer) |
| 3 confirm needs read_back @ revision | stale/read_back_required tests |
| 4 SUBMITTED terminal | test_submitted_is_terminal (param) |
| 5 menu-snapshot validation | atomic add tests; per-session Menu |
| 6 basket never crosses tenant | immutable Session; E2E switch = fresh session |

## Tools table + conventions
All 8 tools, fixed params (core/tools.py TOOL_SCHEMAS); full-state
snapshot on success (test_every_success_carries_full_snapshot); error
shape w/ candidates ≤3 (tests); invalid_quantity "zwei" (test);
read_back carries code-computed total (snapshot basket_total; rounding
test); remove_item deterministic (2 tests).

## Conversation policy → prompts/system.de.md + en.md
Greet first / one question / menu+prices verbatim from tools / name+street
(street declinable, name confirm) / explicit yes, mhm≠yes / never announce
before order_id / id in groups + minutes / plain-language errors / never
claim address checked. Transcripts exercise flow; live web demo showed
policy behaviour end to end.

## Web channel
| Req | Where |
|---|---|
| First-time conversation e2e | test_e2e_full_order_with_header_footer_contract |
| New conversation after order | Start over → startSession (same path E2E-covered via switch) |
| Header: name/selector(+short UUID)/dashboard/lang/start-over | E2E asserts each |
| Selector from API only, no fallback | /config live fetch; null → "list unavailable" (test_config_list_unavailable_no_fallback) |
| Footer: version/UUID/conn-state/docs | E2E + /health tests (unknown→ok→down) |
| No message unanswered | working indicator; steps streamed; done-w/o-answer notice; error/timeout/disconnect notices + retry — E2E failure trio + confirm-retry + lost-session tests |
| Basket visible w/ totals; read-back distinct + confirm control; id+minutes; locked after submit | E2E full-order assertions |

## Speech
Endpoints via SpeechService; only speech path; getUserMedia/MediaRecorder
capture, plain audio playback; SpeechRecognition/speechSynthesis absent
(grep); nothing hardcoded; request/response only; push-to-talk w/ visible
state; TTS off default, final message only; never required (E2E hidden
controls; text order works — live demo v1 + E2E); spoken answers shortened
via ephemeral note (test); name confirm in prompts.

## Error handling table
Every row → mechanism + test: gateway timeout retry-once (transcript +
unit), 401/403 no-retry, startup 404 (test_pizzeria_name_startup_check),
runtime selection 409 (API+E2E), 422 keep basket, 5xx no blind retry,
submit timeout recovery via list+detail, unknown item candidates, empty
basket, menu fetch fail fast, pizzeria list fail no-fallback (E2E),
speech down text-unaffected (probe + notices).

## Anti-patterns 1-6 — none present (grep: no regex parser, no
subprocess/curl, no hardcoded tenant/menu, no confirmation-forbidding
prompt, no prompt shouting, stream events rendered — anti-pattern 6
E2E-asserted).

## Testing section — unit exhaustive / tool fixtures / five transcripts /
browser E2E incl. 3 failure paths / live acceptance via list+detail /
speech manual checklist (README). All present.

## Roles & review protocol — implementer/reviewer separation held; 19
rubric/gate rounds in reviews/ + scores.md; plan approved before code;
impl approved 24/25 round 19.

## Deliverables tree — every listed file exists (incl. channels/speech.py,
tests/test_web_e2e.py). Documented additions: tests/stubs.py,
tests/test_transcripts.py, requirements.txt, decisions/, SPEC archives.

## Decisions locked — all 24 rows honored (walked individually; notably:
totals in code, tenancy customer-selectable via URL-path tenant, selector
no fallback, proof via browser + live API, done = judge approved).

OPEN ROWS: none.
