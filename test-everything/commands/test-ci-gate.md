---
name: test-ci-gate
description: Configure impact-based selective test execution and a deterministic merge gate — changed paths map to owning test scopes, the merge queue runs only tool verdicts (no LLM checks), and nightly runs the slow guarantees.
argument-hint: "[ci-config-path] — .github/workflows by default"
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "Agent", "WebSearch"]
---

# CI Gate (Impact-Based Selective Execution + Deterministic Merge Gate)

**Pass/fail in the merge gate comes only from deterministic executors** — the test runner, the mutation tool, the contract verifier, the linter. An LLM may write tests and analyze failures; an LLM never declares the gate green.

## Instructions

### Step 1: Impact-Based Selection (diff-aware)

Map changed paths → owning test scopes. Mechanisms:

- CODEOWNERS-style test maps
- `nx affected` / `turbo run --filter=...[origin/main]`
- Bazel `cquery --affected`
- Vitest `--changed`
- `git diff --name-only | <test-map>`

**Fallback rule**: a map MISS (changed file with no owning scope) triggers the FULL suite for that PR — misses never silently shrink CI.

### Step 2: Merge-Queue Gating (the deterministic gate plane in CI)

The merge queue runs:

- the affected suite (full on map misses),
- the mutation gate on changed code (`/test-mutation-loop`),
- contract verification (Pact `can-i-deploy`, schemathesis, buf breaking),
- linters/typecheck.

All verdicts come from tools; **no LLM checks in the queue**, no skipped-must-pass. Quarantined tests run in their continue-on-error job (`/test-flaky`), not in the gate.

### Step 3: Nightly Full Run

The complete suite + full-repo mutation sampling + fuzz campaigns (`/test-fuzz`) + quarantine-trend + scorecard trend (`/test-quality`). Slow guarantees live here so PR CI stays fast.

### Step 4: Skipped-Log + Incident Rule

Every selective run logs which scopes it skipped and why. **A nightly red in a scope that PRs repeatedly skipped is an automatic incident on the selection map**, not just on the code.

Details: `skills/test-strategy/references/enhancement-capabilities.md` §13.
