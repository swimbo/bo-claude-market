---
name: test-contract
description: Enforce tests as an immutable contract — run the suite, dispatch agents with confrontational fix mandates, and loop until everything passes. Resolves incomplete work through argue-and-debate agent dynamics.
argument-hint: "[test-command] e.g. 'npm test', 'npx playwright test', 'cargo test'"
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "Agent"]
---

# Test Contract Enforcement

**"The tests are the contract. Everything must pass."**

Run an existing test suite, analyze failures, dispatch parallel agents with specific confrontational mandates, and loop until the entire suite is green. This workflow resolves incomplete work by making agents argue, debate, and prove their implementations work against the test contract.

## Why This Works

Traditional agent workflows produce incomplete work because agents can claim "done" based on code changes alone. This workflow eliminates that:

1. **Tests are written first** (or already exist) — they define the contract
2. **Implementation agents are dispatched** with the mandate: "make these tests pass"
3. **When tests fail**, agents get specific, confrontational feedback: "Your endpoint is not reading the session cookie. Prove it works."
4. **Agents must argue and debate** — if one agent's implementation breaks another's tests, they push back on each other with evidence
5. **No one claims done** — only ALL TESTS PASSING means done

## Instructions

### Step 0: Identify the Test Suite

If the user provided a test command argument, use it. Otherwise, detect:

```bash
# Check package.json scripts
cat package.json 2>/dev/null | grep -E '"test|"test:|"e2e|"spec' || true

# Check for test configs
ls -la vitest.config.* jest.config.* playwright.config.* Cargo.toml pytest.ini 2>/dev/null || true
```

Confirm with the user which test suite to enforce if multiple exist. Common patterns:
- `npm test` — unit tests
- `npx vitest run` — unit/integration
- `npx playwright test` — E2E
- `cargo test` — Rust tests
- `pytest` — Python tests

### Step 1: Run the Suite — Establish the Contract

Run the full test suite and capture every result:

```bash
[test command] 2>&1
```

**If all tests pass:** Report green and exit. The contract is satisfied.

**If any tests fail:** Proceed to Step 2. Count: total, passing, failing, skipped.

**If any tests are skipped:** Flag immediately. Skipped tests are unacceptable — they hide gaps. They must be unskipped and fixed or explicitly removed with user approval.

### Step 2: Analyze Failures — Build the Enforcement Report

Dispatch the **test-driven-enforcer** agent to:
1. Parse every failure — test name, file, error, expected vs actual
2. Trace each failure to the source code that's broken
3. Categorize failures by root cause (auth, UI elements, API contract, state, routing, timing)
4. Generate specific, confrontational fix mandates per category

The enforcer's output is the dispatch plan for implementation agents.

### Step 3: Dispatch Agents — Argue and Debate

For each failure category in the enforcement report, dispatch a parallel agent with:

1. **The mandate** — exact text from the enforcer (specific, confrontational, evidence-based)
2. **The contract** — the test file(s) they must make pass
3. **The prove-it command** — the specific test command to verify their fix
4. **The rule** — "The tests are the contract. They don't change. Your implementation does."

**Dispatch template for each agent:**

```
You are fixing [N] failing tests in [category].

THE TESTS ARE THE CONTRACT. EVERYTHING MUST PASS.

## Your Mandate

[Paste the enforcer's mandate for this category — includes failing tests, root cause, evidence, required fix]

## Rules

1. Fix the APPLICATION code to make the tests pass. Do NOT modify the test files.
2. After making changes, run: `[specific test command]`
3. If tests still fail, read the new error carefully and fix again.
4. You are DONE only when `[test command]` shows all tests in your scope passing.
5. If you believe a test has a genuine bug (contradicts requirements), document the evidence — do NOT silently change or skip it.

## Prove It

Run `[test command]` and show the output. If [test name] still fails with [error pattern], your [component] is [still broken]. Fix it.
```

**Parallel dispatch rules:**
- Independent failure categories → dispatch in parallel (e.g., API auth fixes and UI element fixes)
- Dependent categories → dispatch sequentially (e.g., if frontend depends on API changes)
- Always include the specific test command so agents can self-verify

### Step 4: Verify — Re-Run the Full Suite

After ALL dispatched agents complete:

1. Run the FULL test suite again (not just the previously failing tests)
2. Compare: which tests now pass? Which still fail? Any NEW failures?

**Possible outcomes:**

| Outcome | Action |
|---------|--------|
| All tests pass | Proceed to Step 5 (Final Verification) |
| Same tests still fail | Escalate — generate Round 2 mandates (more specific, cite what was tried) |
| Different tests fail | New breakage — one agent's fix broke something else. Generate cross-cutting mandates. |
| Fewer failures | Progress — dispatch focused mandates for remaining failures |

### Step 5: Escalation Loop (If Needed)

If tests still fail after Step 4, escalate with increasingly specific mandates:

**Round 2** — "Your previous fix didn't work":
- Re-run the enforcer with the new failure output
- The enforcer generates escalated mandates that cite what was tried and why it didn't work
- Dispatch new agents (or re-dispatch existing ones) with the escalated mandates

**Round 3** — "Two attempts failed, trace the full path":
- The enforcer traces the complete execution path for each remaining failure
- Mandates cite the full chain: request → middleware → handler → response → assertion
- Include what the previous two attempts changed and why they were insufficient

**Round 4** — "Systemic issue, re-examine architecture":
- If the same tests keep failing, the enforcer explains the architectural pattern that's misunderstood
- Mandates explain HOW the system works, not just WHAT to change

**Round 5** — "Escalate to user":
- If 4 rounds haven't resolved all failures, present the remaining failures to the user with full analysis
- Include: what was tried, what didn't work, the enforcer's best theory for remaining failures
- Ask the user for guidance — there may be a design decision or external dependency involved

**Maximum iterations: 5.** After 5 rounds, always escalate to the user. Infinite loops help nobody.

### Step 6: The Debate Protocol

When one agent's fix causes another agent's tests to fail (Step 4, "Different tests fail"):

1. **Identify the conflict**: Which file(s) were changed by Agent A that broke Agent B's tests?
2. **Present both sides**: "Agent A changed `[file:line]` to fix [test-1], but this broke [test-2] that Agent B owns."
3. **Apply the contract**: Both tests must pass. Neither agent "wins" — both must find a solution that satisfies both tests.
4. **Dispatch a mediator mandate**: "Tests [test-1] and [test-2] have a shared dependency at `[file]`. Your change to fix [test-1] broke [test-2]. Find a solution that makes BOTH pass. The tests are both part of the contract."

### Step 7: Final Verification

When all tests pass:

1. **Run the full suite one more time** — confirm it's stable, not a fluke
2. **Check for weakened tests** — grep for any `test.skip`, `test.fixme`, `waitForTimeout`, or weakened assertions that agents might have introduced
3. **Report the results**

### Output Format

```markdown
# Test Contract — Enforced

**Suite:** `[test command]`
**Rounds:** [N] (1 = first run passed, 2+ = enforcement iterations needed)

## Contract Status: SATISFIED / NOT SATISFIED

## Results
| Metric | Before | After |
|--------|--------|-------|
| Total | N | N |
| Passing | N | N |
| Failing | N | 0 |
| Skipped | N | 0 |

## Enforcement History

### Round 1
- **Failures:** N across [categories]
- **Agents dispatched:** [N agents, what each fixed]
- **Result:** [N tests fixed, N remaining]

### Round 2 (if needed)
- **Escalation:** [What changed in the mandates]
- **Result:** [N tests fixed, N remaining]

## Changes Made
- `[file]` — [what was changed and why]
- `[file]` — [what was changed and why]

## Debates Resolved (if any)
- **[test-1] vs [test-2]**: [Conflict] → [Resolution]

## Test Integrity Check
- Weakened tests found: [N] (must be 0)
- Skipped tests found: [N] (must be 0)
- New `waitForTimeout` found: [N] (must be 0)

## Verdict
[ALL TESTS PASS / ESCALATED TO USER — N remaining failures]
```

## Guidelines

* **Tests are sacred** — the default is ALWAYS "fix the implementation." Only flag a test as buggy with specific evidence.
* **Dispatch in parallel** when failure categories are independent — don't serialize what can be parallelized
* **Each agent must self-verify** — include the prove-it command in every mandate
* **Track what was tried** — escalation mandates must cite previous attempts to avoid repeating the same failed approach
* **Never exceed 5 rounds** — if 5 rounds can't fix it, a human needs to weigh in
* **Watch for weakened tests** — agents under pressure may silently skip or soften assertions. The final integrity check catches this.
* **Cross-cutting failures get mediator mandates** — when Agent A breaks Agent B's tests, don't just re-dispatch both. Give them a shared mandate that demands both tests pass.
