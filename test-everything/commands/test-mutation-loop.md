---
name: test-mutation-loop
description: Run mutation testing on changed code and loop on surviving mutants — strengthen tests at the behaviour level until the mutation-score threshold is met. Mutation score gates acceptance; coverage never does.
argument-hint: "[test-command] e.g. 'npm test', 'cargo test' — scope defaults to changed code (git diff)"
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "Agent", "WebSearch"]
---

# Mutation Testing Loop (Surviving-Mutant Re-Prompt)

Mutation testing is the **acceptance mechanism** for generated or existing tests. Coverage says a line RAN; mutation says a test could TELL the difference. LLM-generated tests are notorious for high-coverage/low-strength — this loop is the deterministic antidote.

**Governing rule: mutation score gates acceptance; coverage only selects gaps.**

## Instructions

### Step 1: Select Scope

Mutated code = changed lines in the PR/commit (`git diff origin/main...HEAD --name-only`), NOT the whole repo. Whole-repo mutation runs are for nightly sampling only.

### Step 2: Run the Mutation Tool

| Stack | Command |
|---|---|
| JS/TS | `npx stryker run` (config in `stryker.config.json`; set `mutate` to changed files) |
| Java/JVM | `mvn org.pitest:pitest-maven:mutationCoverage` (target changed classes) |
| Python | `mutmut run --paths-to-mutate <changed>` or `cosmic-ray baseline && cosmic-ray exec` |
| Rust | `cargo mutants --in-place` (or scope by crate/file) |
| Go | `go-mutesting path/...` or `go test -fuzz` adjacent mutant generation |

Use WebSearch to confirm current tool flags/version if the project's stack is unclear.

### Step 3: Parse the Report

Categorize mutants: killed / survived / timeout / no-coverage. **Survived and no-coverage mutants are the work items.**

### Step 4: Re-Prompt Per Surviving Mutant

For each surviving mutant, feed the authoring loop (via a Task subagent):

- the **mutant diff** (what was changed in the implementation),
- the **tests that execute the mutated line** (from the coverage map),
- the instruction: *"This suite fails to distinguish this mutant from correct behavior. Write or strengthen an assertion at the BEHAVIOUR level (observable output, state, response) that fails under this mutant. Do not assert implementation details."*

### Step 5: Re-Run and Iterate

Re-run mutation after each batch of strengthened tests. Iterate until the mutation-score threshold is met:

- Default threshold: **≥85% killed on changed code**; ratchet upward over time.
- **Equivocal mutants** (semantically identical to the original) may be allow-listed individually with a written justification, capped at ~5% of mutants.

### Step 6: Report

```
Mutation score: N% (killed K / total T, allow-listed A)
Remaining survivors: [list with diffs and justifications]
```

**The mutation score gates acceptance. A suite that raises coverage but kills no mutants is rejected.** Details: `skills/test-strategy/references/enhancement-capabilities.md` §1.
