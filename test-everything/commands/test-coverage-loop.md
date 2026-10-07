---
name: test-coverage-loop
description: Iterative test-generation refinement loop — coverage SELECTS where to write tests, mutation score DECIDES what survives. Candidates that raise coverage but kill no mutants are rejected.
argument-hint: "[scope] — defaults to changed code"
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "Agent"]
---

# Coverage Loop (Coverage Selects, Mutation Decides)

Refinement loop for generated tests. **Coverage chooses WHERE; mutation verdicts choose WHAT SURVIVES. Never invert.**

## Instructions

### Step 1: Run Coverage

```bash
npx vitest run --coverage    # JS/TS
cargo llvm-cov               # Rust
pytest --cov                 # Python
go test ./... -cover         # Go
```

### Step 2: Rank Gaps by Risk

Rank uncovered/under-covered regions by risk tier (auth/payments/data mutation = high; business logic = medium; presentation = low), **not by line count**.

### Step 3: Author Candidate Tests

Dispatch test authoring as a Task subagent for the top region. Apply the reward-hacking guardrails: don't include the grading criteria in the subagent brief; grade against them separately.

### Step 4: Gate on Mutation, Not Coverage

Run the mutation tool on that region (see `/test-mutation-loop`). **Candidate tests that raise coverage but kill no mutants are REJECTED** — rewritten until they kill the region's mutants. Coverage gain never substitutes for mutant kills.

### Step 5: Loop

Repeat until BOTH the coverage target and the mutation threshold hold on the touched scope.

**Loop bound**: cap iterations (~5 per region). A region still failing the gate after the cap **escalates with evidence** (surviving-mutant list) rather than looping forever.

Details: `skills/test-strategy/references/enhancement-capabilities.md` §6.
