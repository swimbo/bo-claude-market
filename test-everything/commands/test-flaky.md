---
name: test-flaky
description: Quarantine flaky tests with typed labels and tiered SLAs instead of disabling them. Quarantined tests keep running in a continue-on-error CI job; retries are masking, never the fix.
argument-hint: "[flaky-test-file-or-name]"
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "Agent"]
---

# Flaky Test Quarantine (Quarantine, Don't Disable)

A flaky test is a bug with a bad disguise. **Investigate the root cause** (race condition, missing loading state, auth-state leak, order dependence, real time/timeouts) and fix it in the application or the test's waiting strategy. Never fix flakiness with `waitForTimeout`, retries-as-policy, `test.skip`/`test.fixme`, or weakened assertions.

## Instructions

### Step 1: Retry-vs-Quarantine Rule

- **First flake** → root-cause investigation. Flakiness is a bug.
- **Second occurrence** → typed quarantine with the investigation notes attached.
- CI-level retries are masking, not fixing — allowed only as a temporary, dated exception tied to an open investigation.

### Step 2: Quarantine with a Typed Label

Move the test to a labeled quarantine suite that **still RUNS in CI (continue-on-error) and reports daily**. Never deleted, never silently skipped, never left failing randomly in the main suite.

Exactly ONE label per quarantined test, each carrying owner + ticket link + date quarantined:

| Label | Meaning | SLA |
|---|---|---|
| `env` | infrastructure/environment (browser cache, containers, network) | ≤ 7 days |
| `timing` | race condition, timeout tuning | ≤ 7 days |
| `data` | fixture/seed drift | ≤ 14 days |
| `order` | inter-test dependence | ≤ 14 days |
| `app` | real product bug (must link a ticket) | until ticket closes, re-triaged every 30 days |

Expired quarantine escalates automatically to the owner.

### Step 3: Enforce the Weighted Bucket Cap (~1%)

Total quarantine weight (env=1, timing=2, data=2, order=2, app=1) ≤ **~1% of suite size**. At cap, new quarantines are BLOCKED until existing ones resolve — forced repayment instead of debt accumulation.

### Step 4: Separate CI Job

Quarantined tests run in their own continue-on-error CI job so their redness is visible and trended without blocking the merge gate.

### Step 5: Record

Per-test retry/pass history over the last N CI runs feeds the flaky-rate metric of `/test-quality`.

Details: `skills/test-strategy/references/enhancement-capabilities.md` §8.
