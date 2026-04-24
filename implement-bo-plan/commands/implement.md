---
name: implement
description: "Execute a bo-planner plan at enterprise level. Runs phases 9-14 (Implementation → E2E Tests → Verification → Design Gate → Enterprise Gate → Delivery → Plan Gap Audit → Fix All Gaps) using standard-design, test-everything, enterprise-assessment, and agents-argue."
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
argument-hint: "[--skip-design-review] [--skip-enterprise] [--enterprise-threshold=B] [--allow-failing-tests] [--gaps-ok] [--phase=<n>]"
---

Invoke the `implement-bo-plan:enterprise-implementation` skill and follow it exactly.

## Preflight (must pass before any work)

1. Confirm `docs/planning/phased-plan.md` exists. If not, tell the user to run `/bo-planner:plan` first and stop.
2. Read `docs/planning/phased-plan.md`. Phases 1–8 (or the applicable subset) must be `complete`. If not, list the unfinished phases and stop.
3. Confirm `docs/planning/architecture.md` and `docs/planning/tech-guide.md` both show that `agents-argue:debate` was run and consensus incorporated. If the debate gate is not cleared, stop.
4. Confirm `docs/planning/phase-9-plan.md` exists with a filled task list.
5. For UI projects: confirm `ux-plan.md` and `ui-plan.md` exist.
6. For testable UI/CLI projects: confirm `e2e-tests.md` exists.
7. Read `findings.md` for `NEEDS_HUMAN_DECISION` tags. If present, block and surface to user.

Log preflight results in `docs/planning/progress.md` under a `## Implementation Preflight` section before proceeding.

## Execution Loop

Run phases in order. Do not advance past a gate without evidence:

1. **Phase 9 — Implementation**
   - Dispatch parallel subagents for independent tasks from `phase-9-plan.md`.
   - UI work: `Skill("standard-design:scaffold")`.
   - Tradeoffs the plan didn't resolve: `Skill("agents-argue:debate", args: "<scratch doc>")`.
   - Update `phase-9-plan.md` checkboxes and `progress.md` after each task.

2. **Phase 10 — E2E Test Generation** (skip if no `e2e-tests.md`)
   - `Skill("test-everything:test-plan")`
   - `Skill("test-everything:test-scaffold", args: "e2e")`
   - Cross-reference generated specs against `e2e-tests.md`.

3. **Phase 11 — Testing & Verification**
   - `Skill("test-everything:test-full-suite")`
   - On failure: `Skill("test-everything:test-contract")` until green (3-strike protocol).
   - Record results in `progress.md`.

4. **Phase 11.5 — Design Quality Gate** (skip if no UI)
   - `Skill("standard-design:review")` → reads `docs/planning/design-compliance.md`.
   - **Block** if `critical > 0`. Return to Phase 9. Override via `--skip-design-review` requires user confirmation.

5. **Phase 11.6 — Enterprise Quality Gate**
   - `Skill("enterprise-assessment:assess")` → reads `docs/planning/enterprise-assessment.md`.
   - **Block** if grade < B (default). Return to Phase 9 with Critical/High as remediation tasks. Overrides `--skip-enterprise` and `--enterprise-threshold=<grade>` require user confirmation.

6. **Phase 12 — Delivery**
   - `Skill("bo-planner:done")` to run completion verification.
   - If user confirms, mark phases 9–12 `complete` in `phased-plan.md`. **Do not stop here.**

7. **Phase 13 — Plan Gap Audit**
   - Ensure `docs/planning/plan-gaps.md` exists (copy template from bo-planner if missing).
   - Dispatch one subagent per planning artifact (user-stories, architecture, tech-guide, ux, ui, e2e, each phase-#-plan) to diff it against code — in parallel.
   - Seed gaps from Phase 11.6 Critical/High findings.
   - Present gap list to user; confirm severities; mark any `wont_fix` with reason.

8. **Phase 14 — Fix All Gaps**
   - Sort by severity: `blocker` → `major` → `minor` → `nit`.
   - Blockers serial, others parallel by owner layer.
   - After each severity tier, re-run the gate that produced those gaps (test / design / enterprise).
   - Append newly surfaced gaps to `plan-gaps.md`. Loop until 0 open non-`wont_fix`.
   - Mark phases 13 and 14 `complete`.

9. **Final Gate — Done-Means-Done Checklist Pass**
   - Locate `bo-planner/done-means-done/` via `Glob` on `**/bo-planner/done-means-done/phase-*.md`. If missing, stop and tell the user.
   - For every non-skipped phase in `phased-plan.md`, load the matching `phase-##-*.md` checklist and verify every **Hard Gate** has evidence in `docs/planning/`.
   - Record results in `progress.md > ## Done-Means-Done Audit` as a table (phase | gate | status | evidence).
   - **Block** if any Hard Gate is `fail` or `missing`. Return to the responsible phase to remediate, then re-run this gate.
   - Soft-check warnings do not block but must be logged with a reason.
   - Only after this pass is green may the project be declared complete. Require `AskUserQuestion` confirmation.

## Override Flags

Parse from `$ARGUMENTS`. Every override requires `AskUserQuestion` confirmation and is logged in `progress.md`:

| Flag | Effect |
| ---- | ------ |
| `--skip-design-review` | Design gate → informational |
| `--skip-enterprise` | Enterprise gate → informational |
| `--enterprise-threshold=<A|B|C>` | Lower the passing grade |
| `--allow-failing-tests` | Tests warn instead of block (discouraged) |
| `--gaps-ok` | Phase 14 exits when only `wont_fix` gaps remain, user accepts |
| `--phase=<n>` | Run only that phase (same as `/phase <n>`) |

## Rules

- Preflight is non-negotiable. No phase 9 without a complete phase 1–8.
- Every phase transition requires evidence, not optimism.
- Independent tasks → parallel subagents in a single message.
- Muting a failing test to pass phase 11 is forbidden. Fix the code.
- Phase 13 is never "skipped because phase 12 looked good" — the audit is the contract.
- A gap is only closed when its owning gate is re-run green.
- User confirms overrides. Claude never decides to lower a gate on its own.
- The project is not complete until the Done-Means-Done final gate passes and the user confirms.
