---
name: phase
description: "Run a single implementation phase (9-14) from the bo-planner plan. Useful for resuming, re-running a gate, or driving one phase at a time."
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
  - AskUserQuestion
  - Skill
argument-hint: "<phase-number> (9, 10, 11, 11.5, 11.6, 12, 13, or 14)"
---

Invoke the `implement-bo-plan:enterprise-implementation` skill but execute only the phase specified in `$ARGUMENTS`.

## Accepted Phase Arguments

| Phase | Name | Skill Dispatched |
| ----- | ---- | ---------------- |
| 9     | Implementation | `standard-design:scaffold` (UI), parallel subagents, `agents-argue:debate` (unresolved tradeoffs) |
| 10    | E2E Test Generation | `test-everything:test-plan`, `test-everything:test-scaffold` |
| 11    | Testing & Verification | `test-everything:test-full-suite`, `test-everything:test-contract` on failure |
| 11.5  | Design Quality Gate | `standard-design:review` |
| 11.6  | Enterprise Quality Gate | `enterprise-assessment:assess` |
| 12    | Delivery | `bo-planner:done` |
| 13    | Plan Gap Audit | Parallel artifact-vs-code audits → `plan-gaps.md` |
| 14    | Fix All Gaps | Severity-ordered fixes, gate re-runs, loop to zero |

## Preflight (phase-specific)

Always check:

1. `docs/planning/phased-plan.md` exists.
2. For phase N, all prior non-conditional phases are marked `complete`. If not, ask the user whether to continue anyway (some phases, e.g. 13, can run independently).

Phase-specific checks:

- Phase 9 — phases 1–8 complete, `phase-9-plan.md` exists, debates cleared.
- Phase 10 — phase 9 complete OR user acknowledges implementation is partial, `e2e-tests.md` exists.
- Phase 11 — build succeeds locally.
- Phase 11.5 — project has a UI.
- Phase 11.6 — tests have been run at least once (phase 11 attempted).
- Phase 12 — phases 9–11.6 complete.
- Phase 13 — phase 12 complete OR user explicitly wants a mid-implementation audit.
- Phase 14 — `plan-gaps.md` exists with at least one `open` row.

## Execution

Run only the specified phase, following its section in the
`enterprise-implementation` skill. On completion:

- Update the corresponding row in `phased-plan.md`.
- Append a phase result block to `progress.md`.
- Report status. Do **not** auto-advance to the next phase — the user may
  want to inspect results first. Ask: "Phase N complete. Run phase N+1?"

## Rules

- Each phase's verification gate still applies — running in isolation doesn't
  bypass the gate.
- If the user passes an invalid phase number, list the accepted values and stop.
- If the user passes `14` but there is no `plan-gaps.md`, prompt them to run
  phase 13 first.
