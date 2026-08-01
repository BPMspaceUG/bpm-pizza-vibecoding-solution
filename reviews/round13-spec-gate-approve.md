**Judge: Codex** (primary Judge, canonical sanitized invocation; payload = this issue fetched live incl. the revision comment). Verdict verbatim:

> VERDICT: APPROVE
> REASONS:
> - SPEC.md:248-254 now restores the critical live-API fact correctly: `GET /pizzerias/{id}/orders` is shortlist-only, `GET /pizzerias/{id}/orders/{order_id}` is the item-verification path, and the acceptance test is tied to that same detail endpoint.
> - SPEC.md:502-513 fixes the prior contradiction in error handling. Timeout recovery now matches the contract facts: shortlist on the list endpoint, verify items on the detail endpoint, adopt only a verified match, otherwise allow exactly one retry, and tell the customer honestly if lookup fails.
> - SPEC.md:559-565 closes the testing loophole explicitly: presence is checked via the list endpoint, while customer/items/quantities must be checked via the detail endpoint because the list endpoint has no items.
> - I found no remaining conflicting submit-timeout recovery instruction elsewhere in the working-tree SPEC.md; the recovery story is now internally consistent across contract, error handling, and testing.
> - The three rejected points from the prior gate are all resolved in the working tree, and I did not find a new contradiction or regression introduced by these fixes that would block implementation.

Gate result: the patched SPEC.md is build-ready. Committing it now; milestone moves to `plan-approved`. Closing/`DONE` remains human-only.
