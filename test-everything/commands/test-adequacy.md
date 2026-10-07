---
name: test-adequacy
description: Audit the auditor — verify a green test suite is actually sufficient before trusting it. Runs the mutation gate, samples tests for falsifiability, detects tautologies and assertion-free tests, and runs E2E negative controls.
argument-hint: "[path-to-tests] — defaults to current directory"
allowed-tools: ["Read", "Glob", "Grep", "Bash", "Agent"]
---

# Test Adequacy Audit (Test the Tests)

Before trusting a green suite — especially one an AI agent wrote or touched — verify the suite itself is sufficient. An audit that only counts tests measures theater, not protection.

## Instructions

### Step 1: Run the Mutation Gate

Run mutation testing scoped to the suite's target code (see `/test-mutation-loop`). **Surviving mutants are direct inadequacy evidence** — each one is a behavior the suite cannot protect.

### Step 2: Falsifiability Sampling

For each test (or a random sample of large suites), ask: **"What exact input would make this test fail?"**

- If no such input can be named, the test is **decorative** — rewrite or delete it.
- Dispatch this analysis as a Task subagent per file batch for speed; a test with no imaginable failing input is worth less than no test.

### Step 3: Tautology Detection

Grep + review for:

- `expect(f(x)).toBe(f(x))` shapes — assertions comparing a value to itself
- asserting a mock's return value that the test itself configured in the same file
- asserting constants (expected values with no production-code dependence)
- snapshot tests whose snapshot was generated from the current (possibly broken) output

### Step 4: Assertion-Free Tests

Find `it('works', ...)` bodies with only arrangement and action — no expect/assert. These are steps, not tests.

### Step 5: E2E Negative Controls

On sampled E2E flows, apply the governing-rule negative controls:

- **Break-the-flow control**: deliberately break the behavior under test (flip a comparison, drop a side-effect, hide the submit button) and re-run. **The suite MUST go RED.** A suite that stays green on a broken implementation is worth less than no suite.
- **Cannot-run = RED**: if the suite cannot execute (missing deps, env broken, harness error), that is a FAILURE — never "0 tests, exit 0".
- **Distinguish correct from incorrect**: the suite must pass the original and fail a mutated build.

### Step 6: Adequacy Verdict

Output per sampled file: adequacy verdict + mutation score + a concrete fix list.

```
| File | Mutation Score | Tautologies | Assertion-free | Falsifiability | Verdict |
|------|---------------|-------------|----------------|----------------|---------|
```

Details: `skills/test-strategy/references/enhancement-capabilities.md` §3.
