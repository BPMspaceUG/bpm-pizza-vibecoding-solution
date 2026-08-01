**Judge: Codex** (primary Judge, canonical sanitized invocation per c-bpm-sk-devils-advocate; payload = this issue fetched live). Verdict verbatim:

> Seven of the eight required patches are present in the working-tree SPEC.md: the verified API facts were restored, `PIZZERIA_LANG` and the language-authority rule were added, speech language is bound to the session language, totals are code-owned and surfaced, `remove_item` is deterministic, and the `404` handling is split correctly.
>
> VERDICT: REJECT
> REASONS:
> - Patch 2 is still not correctly specified. The contract facts say timeout recovery must shortlist on the list endpoint and then verify basket contents via the detail endpoint (SPEC.md:248), but the error table still instructs `Timeout on submit -> verify via GET /pizzerias/{id}/orders before any retry` and the prose repeats "verify against the pizzeria's order list" (SPEC.md:502). That reintroduces the wrong recovery path, because the list endpoint has no `items[]`.
> - The live acceptance-test wording is still looser than the restored contract fact. It says only "read the pizzeria's orders back and assert the four points" (SPEC.md:557). Make it explicitly require shortlist-from-list plus item assertion via `GET /pizzerias/{id}/orders/{order_id}` so the test cannot be implemented against the insufficient list endpoint.
> - This remaining inconsistency is not cosmetic. Timeout recovery is one of the four explicit failure modes in "What done looks like", so leaving two conflicting recovery instructions in the document means the spec is not build-ready as a source of truth.
