---
name: full-suite
description: Full testing workflow — audit gaps, plan strategy, scaffold infrastructure, write tests, run them, and fix until everything passes
argument-hint: "[path-to-project]"
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "Agent"]
---

# Test Everything

End-to-end testing workflow: audit, plan, build, run, fix, repeat until green.

## Instructions

Execute the full testing lifecycle for the project at the given path (or cwd).

### Phase 1: Audit

Perform the same analysis as `/test-everything:audit`:

1. Detect project type, languages, frameworks
2. Inventory existing tests and configs
3. Assess each testing layer (unit, integration, E2E, performance, security, accessibility)
4. Identify gaps — output a brief summary table (not the full report)

### Phase 2: Plan

Based on the audit, determine what needs to be built:

1. Select the appropriate testing architecture model (Pyramid/Diamond/Trophy)
2. Prioritize gaps — focus on the highest-impact missing layers first
3. List the specific test files and configs to create
4. Present the plan to the user as a checklist and wait for approval before proceeding

### Phase 3: Scaffold & Write Tests

For each item in the approved plan:

1. Scaffold any missing test infrastructure (configs, setup files, directories)
2. Install missing dependencies via the project's package manager
3. Write real, meaningful tests — not just boilerplate:

   * Read the source code being tested

   * Write tests that exercise actual behavior, edge cases, and error paths

   * Follow existing project patterns and conventions

   * Co-locate tests with source when that's the project convention
4. Use parallel subagents for independent test files when possible

### Phase 4: Run & Fix

Loop until all tests pass:

1. Run the full test suite using the project's test command
2. If tests fail:

   * Analyze the failure output

   * Determine if the bug is in the test or the source code

   * Fix the root cause — don't weaken tests to make them pass

   * Re-run and repeat
3. If tests pass, run linting/type-checking if available
4. Fix any lint or type errors introduced

### Phase 5: Summary

Once everything is green, output:

```
## Test Everything — Complete

### Tests Added
- [list of new test files with test counts]

### Infrastructure Created
- [configs, CI files, setup files]

### Coverage Change
- Before: [if known]
- After: [run coverage if available]

### All Passing
- [test command]: ✅ N tests passed
- [lint command]: ✅ clean
```

### Guidelines

* Never skip Phase 2 approval — the user must confirm the plan before you write code

* Write tests that would actually catch regressions, not just tests that pass

* If fixing a test failure requires changing source code, explain what the bug is before fixing

* Prefer fixing source code bugs over weakening test assertions

* Use the testing-strategy skill for guidance on any testing type

* Don't install tools outside the project's preferred stack without asking