# AI-Agent Testing: Enhancement Capabilities

Thirteen mechanisms that close the failure modes of AI-agent test suites. They share one governing rule:

> **GOVERNING RULE: LLMs author tests and state invariants. Deterministic tools (test runners, mutation engines, fuzzers, contract verifiers) decide pass/fail and whether tests are acceptable. No LLM judgment sits in the merge gate. Mutation score gates test acceptance; coverage only selects where to write next; every new suite must pass a negative control (break the code, suite goes red).**

Index — §1 Mutation · §2 Mutation-gated generation · §3 Adequacy audit · §4 Negative controls · §5 Property · §6 Coverage loop · §7 E2E determinism · §8 Flaky quarantine · §9 Quality scorecard · §10 Contract · §11 Differential · §12 Fuzz · §13 CI gate

---

## 1. Mutation Testing Loop (Surviving-Mutant Re-Prompt)

- Killed/survived mutants per mutant type — a suite that raises coverage while killing no mutants is REJECTED.
- **Per surviving mutant, the LLM gets a Task-subagent re-prompt**: mutant diff + the executing tests + "strengthen at the behavior level" instruction.
- The loop from Rule #3: run mutation on diff code → re-prompt per surviving mutant → regenerate → repeat to threshold (~85% on changed code; allow-list equivocal mutants individually).
- Scope to changed lines (PR/commit), never whole repo except for nightly sampling.

## 2. Mutation-Gated Test Generation

The refiner: generate candidate tests → run mutation score → low score → feed back → regenerate. Must apply the reward-hacking guardrails of Rule #2 (don't show the grader to the generator). Ends when the mutation threshold is met, not when the loop "feels done."

## 3. Test Adequacy Audit (Test the Tests)

Audits the AUDITOR: a green suite is not trusted until it has passed the mutation gate, **falsifiability sampling** (per test: "what exact input would make this fail?" — if nothing, it's decorative), tautology checks, and assertion-presence checks.

## 4. E2E Negative Controls

- **Break-the-flow control**: deliberately break the behavior under test; the suite MUST go red.
- **Cannot-run = red**: harness errors are failures, not "0 tests, exit 0".
- **Distinguish correct from incorrect**: pass on original, fail on a mutated build.

## 5. Property-Based Testing (LLM Proposes, Engine Falsifies)

LLM states invariants in precise English first (round-trip, idempotence, order-independence, conservation, bounds, monotonicity); deterministic engine (Hypothesis / fast-check / proptest / gopter) falsifies. Every counterexample is either a found bug or a wrong invariant. Shrunk counterexamples become regression tests; seeds are recorded. A property suite that never falsified anything is untested machinery — inject one known-bad implementation once and confirm it fires.

## 6. Coverage-Selection-Only Loop (with reward-hacking guardrails)

Refinement loop where **coverage selects gaps, mutation verdicts decide survival** — never inverted. Agent ranks coverage gaps by risk tier and cost, writes candidate tests, gates on mutation score, and loops. Reward-hacking guardrails (from agent-training research on graders-as-goals): never give the agent the grading function; grade its output against separate criteria; don't let it modify the grader (here: the mutation config) without review; cap self-improvement iterations and require evidence at the cap.

## 7. E2E Determinism Layer: Discover-then-Freeze + Failure-Evidence Capture

- **Discover-then-freeze**: LLM exploration (playwright codegen, accessibility-tree navigation) maps flows, then FREEZES them into deterministic scripts. CI runs the frozen script; exploration is for discovery, never regression.
- **Healing as diff-for-approval**: broken selectors trigger a heal proposal that is a DIFF for human approval — bounded retries per selector (~3) and per run (~2). No silent self-edits.
- **Mandatory failure evidence**: screenshot + DOM snapshot (+ a11y tree) + console errors + failed network requests captured at failure time. "Selector not found" without page evidence is not a filed bug.

## 8. Flaky-Test Quarantine Discipline

Quarantine with typed labels — never disable. Each quarantined test keeps running in CI (continue-on-error job) and reports daily, and carries owner/ticket/date. Exactly one label per test with tiered SLAs: env ≤ 7d, timing ≤ 7d, data ≤ 14d, order ≤ 14d, app until ticket closes (re-triage every 30d). **Weighted bucket cap ~1% of suite size**; at cap, new quarantines are blocked until existing ones resolve (forced repayment). Fix root causes: races, missing loading states, auth-state leaks, order dependence. `waitForTimeout`, retry-as-policy, `test.skip/fixme`, and weakened assertions are masking, never fixing.

## 9. Numeric Test-Quality Scorecard

Five metrics, weighted — **mutation score 30%**, assertion strength 25%, mock ratio 15%, tautology rate 15%, flaky rate 15%. Verdicts: ≥80 healthy / 60–79 acceptable / <60 decorative (run `/test-adequacy` before trusting anything the suite reports). Mutation score is the primary truth metric; mock ratio penalizes >~60% all-mocked suites (mock-orchestration tests verify assumptions, not the system); each all-mocked bet is paid off with contract tests at the boundary.

## 10. Contract Testing (Provider/Consumer Pairs)

Contract specs for every API boundary — explicit schema (OpenAPI/GraphQL SDL/protobuf) with explicit version pinning. CI contract check: provider's implementation vs published contract, consumer's expectations vs published contract, and **`can-i-deploy` compatibility on version ranges** — preventing integration breakage without full integration suites. Schema evolution gates reject breaking changes; automated compatibility verdicts come from the contract tool (Pact/schemathesis/buf), never from an LLM reading the diff.

## 11. Differential Testing (Old vs New, Oracle vs Impl)

LLM specifies WHAT to compare; deterministic tooling runs both implementations and diffs. **Golden master testing** during refactors/migrations/rewrites: capture old outputs as fixtures → assert new == golden. Divergence report: every discrepancy gets a bug/intended ruling, a ticket, and (if bug) a regression test. Old code never deleted with unruled divergences. When no oracle exists, don't invent one — fall back to invariants and metamorphic relations.

## 12. LLM-Crafted Fuzzing Seeds

LLM invents adversarial input CLASSES (unicode edges, deep nesting, INT boundaries, malformed encodings, protocol confusion, oversized, hostile-valid); the deterministic fuzzing engine (go-fuzz / atheris / Jazzer / cargo-fuzz) mutates and executes. Harnesses are reviewed deterministic artifacts; campaigns are bounded nightly; every crash/timeout/OOM becomes a minimized deterministic regression test — findings that don't reproduce deterministically are not filed.

## 13. Impact-Based Selective CI Test Execution + Merge-Queue Gating

Coverage-graph mapping of changed paths → owning test scopes (CODEOWNERS-style maps / nx affected / turbo filter / Bazel cquery / vitest --changed / git diff + script). **Diff to fail: a changed file with no owning test scope triggers the FULL suite for that PR — map misses never silently shrink CI.** Merge queue runs only deterministic verdicts: affected suite (full on misses), mutation gate, contract verification, lint/typecheck — no LLM checks, no skipped-must-pass. Nightly runs the full suite, full-repo mutation sampling, fuzz campaigns, quarantine trends, scorecard trends. Skipped-scope logging + incident rule: nightly red in a repeatedly-skipped scope is an incident on the selection map, not just the code.

---

## Command Mapping

| Mechanism | Command |
|---|---|
| §1–2 Mutation loop / mutation-gated generation | `/test-mutation-loop` |
| §3–4 Adequacy audit + negative controls | `/test-adequacy` |
| §5 Property-based testing | `/test-property` |
| §6 Coverage-selection loop | `/test-coverage-loop` |
| §7 E2E determinism layer | `/test-e2e` |
| §8 Flaky quarantine | `/test-flaky` |
| §9 Quality scorecard | `/test-quality` |
| §10 Contract testing | `/test-contract` (existing) + `references/testing-types-detail.md` |
| §11 Differential testing | `/test-differential` |
| §12 Fuzz seeds | `/test-fuzz` |
| §13 CI gate | `/test-ci-gate` |
