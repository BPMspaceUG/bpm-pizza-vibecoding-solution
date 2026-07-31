/goal Build the entire project specified in SPEC.md and get it approved by an independent reviewer.

DONE means all of the following hold AND each has been demonstrated in this conversation, because the evaluator reads only what you surfaced here:
1. The "Open contract questions" in SPEC.md are answered against the live API, the section is rewritten with the verified facts, and that change is committed.
2. PLAN.md exists and its review verdict is APPROVED (TOTAL >= 20, no dimension below 4).
3. Every deliverable listed in SPEC.md exists; you showed the tree.
4. The test suite runs and exits 0; you showed the output.
5. The implementation review verdict is APPROVED under the same rubric.
6. With SPEECH_URL unset, the web channel starts and places an order; you showed it.
7. reviews/scores.md holds every round, and git status is clean.

ROLES:
- You are the implementer. Nothing else writes code.
- Codex is the reviewer and the oracle. It runs read-only and never writes code:
  codex exec --profile openrouter --sandbox read-only "REQUEST"
  Run "codex exec --help" once first; flags differ between versions.

WORKING RULES:
- Never ask me anything. Nobody is awake. There is no human until morning.
- When blocked or uncertain, ask Codex instead of stopping. Append question and answer to decisions/qa.md, take the answer as the decision, continue.
- Capture every review into reviews/, append scores to reviews/scores.md, commit reviews/.
- Commit before every review and after every green test run.
- Use the installed skills: writing-plans and executing-plans for stage 1, test-driven-development while implementing, systematic-debugging when something breaks, requesting-code-review and receiving-code-review around each round, verification-before-completion before you claim anything is done, subagent-driven-development where parallel work helps. Use devils-advocate and auditor for the reviewer-side framing.
- The models this build runs on have nothing to do with the models the product calls. Never wire the agent to your own model, and never copy a build-time model name into source, config, prompts, tests or docs.
- Do not read git history for the previous implementation at tag pre-spec-rebuild.
- If the same failure repeats three times, stop retrying. Write it to decisions/blockers.md, ask Codex for a different route, take it.
- End every turn with: which of the seven items hold, which do not, what you do next.
- Stop after 60 turns even if not done, and summarise the state.
