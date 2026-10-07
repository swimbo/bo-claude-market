---
name: test-quality
description: Score a test suite on a numeric five-metric scorecard (mutation score 30%, assertion strength 25%, mock ratio 15%, tautology rate 15%, flaky rate 15%). Verdicts — ≥80 healthy, 60-79 acceptable, <60 decorative.
argument-hint: "[path-to-tests] — defaults to current directory"
allowed-tools: ["Read", "Glob", "Grep", "Bash", "Agent"]
---

# Test Quality Scorecard (Numeric)

A numeric score — not prose impressions — of how much protection a suite actually provides. An audit that only counts tests measures theater.

## Instructions

Score each metric 0–100, then compute the weighted total.

### Metric 1: Mutation Score — weight 30%

Run the mutation tool scoped to the file's scope; killed/total (allow-listed excluded). This is the primary truth metric. See `/test-mutation-loop`.

### Metric 2: Assertion Strength — weight 25%

% of assertions that are **specific and falsifiable**: exact values, roles, URLs, schemas.

```bash
# vague (count these)
grep -rn 'toBeTruthy()\|toBeDefined()\|toBeGreaterThan(0)' tests/ e2e/
# specific (the good kind: toBe(exact), toHaveURL, toHaveRole, schema validation)
```

### Metric 3: Mock Ratio — weight 15%

% of tests where every collaborator is a double (all-mocked tests): `vi.mock` / `unittest.mock` / `#[mock]` counts ÷ test count. Penalize above ~60% all-mocked — a suite of mock-orchestration tests is testing your assumptions, not your system. Pay off mock bets with contract tests at boundaries.

### Metric 4: Tautology Rate — weight 15%

% of tests matching the tautology patterns from `/test-adequacy` Step 3 (self-comparisons, mock-echo assertions, constant assertions). Target: 0.

### Metric 5: Flaky Rate — weight 15%

% of tests with retry/quarantine/flicker history over the last N CI runs.

### Report

```
Score = Σ(metric × weight)
Aggregate: N/100

| File | Mutation | Assertion | Mock | Tautology | Flaky | Total |
|------|----------|-----------|------|-----------|-------|-------|

Three worst files: [file + one concrete fix each]
```

### Verdicts

| Score | Verdict | Action |
|---|---|---|
| ≥ 80 | Healthy | keep |
| 60–79 | Acceptable | schedule improvements |
| < 60 | **Decorative** | run `/test-adequacy` before trusting anything this suite reports |

Details: `skills/test-strategy/references/enhancement-capabilities.md` §9.
