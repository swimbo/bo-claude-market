# implement-bo-plan

Execute a [bo-planner](../bo-planner/) plan at enterprise level. This plugin is the implementation counterpart to `bo-planner`: where `bo-planner` produces `docs/planning/` artifacts, `implement-bo-plan` drives phases 9–14 to shipped, audited, enterprise-ready code by chaining the rest of the marketplace.

## What It Does

Reads the planning artifact set in `docs/planning/` and runs a phased execution loop:

| Phase | Action | Plugins Used |
| ----- | ------ | ------------ |
| 9  | Implementation | `standard-design:scaffold` (UI), parallel subagents, `agents-argue:debate` for unresolved tradeoffs |
| 10 | E2E Test Generation | `test-everything:test-plan`, `test-everything:test-scaffold` |
| 11 | Testing & Verification | `test-everything:test-full-suite`, `test-everything:test-contract` (loops until green) |
| 11.5 | Design Quality Gate | `standard-design:review` — blocks on critical issues |
| 11.6 | Enterprise Quality Gate | `enterprise-assessment:assess` — blocks if grade < B (configurable) |
| 12 | Delivery | `bo-planner:done` verification protocol |
| 13 | Plan Gap Audit | Produces/updates `docs/planning/plan-gaps.md` |
| 14 | Fix All Gaps | Works gaps in severity order, re-runs gates, loops until zero open |

Phases 1–8 are **not** run by this plugin — they belong to `bo-planner`. If `docs/planning/` is incomplete or the adversarial debate gates (phases 5, 6) haven't been cleared, `/implement` refuses to start.

## Prerequisites

Before running `/implement-bo-plan:implement`, the following must be present in `docs/planning/`:

- `phased-plan.md` with phases 1–8 marked `complete` (conditional phases may be skipped)
- `architecture.md` and `tech-guide.md` with adversarial debate consensus incorporated
- `user-stories.md` with acceptance criteria
- `phase-9-plan.md` (and onward) with filled task checklists
- `ux-plan.md` and `ui-plan.md` if the project has user-facing components
- `e2e-tests.md` if the project has testable UI or CLI

If any are missing, `/implement` reports what's missing and stops.

## Install

```bash
claude plugin install implement-bo-plan@bo-claude-market
```

Recommended companion plugins (the orchestrator invokes their skills/commands):

- `bo-planner` (required — produces the plan)
- `agents-argue` (for unresolved design tradeoffs)
- `standard-design` (when project has a UI)
- `test-everything` (always — for test planning and contract loops)
- `enterprise-assessment` (always — for the final quality gate)

## Commands

| Command   | Description |
| --------- | ----------- |
| `/implement` | Run the full 9→14 loop from current phase through delivery and gap-free shipment |
| `/phase`  | Run a single phase (e.g. `/phase 11`), useful for resuming or re-running |
| `/continue-implementation` | Inspect `docs/planning/progress.md` and continue from the last completed phase (named `continue-implementation` because `/resume` is reserved by Claude Code for resuming conversations) |
| `/impl-status` | One-screen status: current phase, gate results, open gaps |

## Quality Gates

The orchestrator blocks phase transitions on these gates. All are configurable via flags on `/implement` or by editing `docs/planning/phased-plan.md` notes.

| Gate | Default Threshold | Override |
| ---- | ----------------- | -------- |
| Tests passing | 100% required | `--allow-failing-tests` (not recommended) |
| Design compliance | 0 critical issues | `--skip-design-review` (sets gate to informational) |
| Enterprise grade | ≥ B (75%) | `--enterprise-threshold=C` or `--skip-enterprise` |
| Plan gap count | 0 open, non-`wont_fix` | `--gaps-ok` (marks remaining gaps as accepted, requires user confirm) |

## Workflow Integration

`implement-bo-plan` sits between `bo-planner:plan` and `bo-planner:done`:

```
/bo-planner:plan                     # Phases 1-8 (planning)
/implement-bo-plan:implement         # Phases 9-14 (execution + audit)
/bo-planner:done                     # Final user sign-off
```

For granular control, drive one phase at a time:

```
/implement-bo-plan:phase 9           # Implementation only
/implement-bo-plan:phase 11          # Testing + quality gates
/implement-bo-plan:phase 13          # Audit only — generate plan-gaps.md
/implement-bo-plan:phase 14          # Fix the open gaps
```

## Philosophy

- **Orchestrate, don't reinvent.** Every capability lives in another plugin; this one sequences them.
- **Gates over optimism.** Phases don't advance on "it should work" — they advance on evidence from `test-everything` and `enterprise-assessment`.
- **Parallel where independent.** User stories with no shared state are dispatched to subagents concurrently.
- **Close the loop.** Phase 13 guarantees "done" matches "planned" by diffing code against every planning artifact. Phase 14 keeps going until the diff is empty.
- **User confirms, never Claude.** Gate overrides require explicit user input.
