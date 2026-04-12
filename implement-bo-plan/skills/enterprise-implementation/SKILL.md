---
name: enterprise-implementation
description: >
  Execute phases 9-14 of a bo-planner plan at enterprise level. Orchestrates
  agents-argue, standard-design, test-everything, and enterprise-assessment
  through a gated phase loop. Use when a bo-planner plan exists in
  docs/planning/ and the user is ready to implement, test, assess, and audit.
user-invocable: true
allowed-tools: "Read, Write, Edit, Bash, Glob, Grep, Task, AskUserQuestion, Skill"
metadata:
  version: "0.1.0"
---

# Enterprise Implementation

This skill drives phases 9–14 of a `bo-planner` plan. It assumes the planning
artifacts in `docs/planning/` are complete through phase 8.

## Preflight: Verify the Plan Is Ready

Before touching code, verify the plan in `docs/planning/`:

1. Read `phased-plan.md`. Confirm phases 1–8 (or the applicable subset) are
   `complete`. If not, **stop** and tell the user which phases are unfinished.
2. Read `architecture.md` and `tech-guide.md`. Confirm each contains a note that
   `agents-argue:debate` was run and consensus incorporated. If not, stop and
   tell the user to run the debate gates first.
3. Confirm `phase-9-plan.md` exists. If not, stop.
4. Conditional checks:
   - UI project → `ux-plan.md` and `ui-plan.md` must exist
   - Testable UI/CLI → `e2e-tests.md` must exist
5. Read `findings.md` for any `NEEDS_HUMAN_DECISION` tags. If present, block
   and surface them to the user.

Record preflight results in `progress.md` before proceeding.

## Phase 9 — Implementation

**Goal**: every task in `phase-9-plan.md` complete, committed, and green on
local build.

1. Read `phase-9-plan.md` task checklist.
2. Group tasks by dependency. Independent tasks → dispatch parallel subagents
   in a single message (one `Task` tool call per subagent).
3. For UI tasks, invoke `Skill("standard-design:scaffold", args: "<page-spec>")`
   to generate layouts consistent with `ui-plan.md`. Follow up with
   `Skill("standard-design:review", args: "<files>")` after each batch.
4. For backend/data tasks, use `test-driven-development` — write the test from
   `user-stories.md` acceptance criteria first, then implement.
5. When a tradeoff surfaces that the plan did not resolve (e.g. two viable
   library choices discovered mid-implementation), invoke
   `Skill("agents-argue:debate", args: "<scratch doc with the tradeoff>")`.
   Log the outcome in `findings.md`.
6. After each task: update the checkbox in `phase-9-plan.md`, append a
   one-line entry to `progress.md`.
7. Verification: project builds cleanly, lints pass, any unit tests written
   during implementation pass. Do **not** declare phase 9 complete on build
   success alone — phase 11 is the real gate.

## Phase 10 — E2E Test Generation (conditional)

Skip if `e2e-tests.md` does not exist (backend-only/library project).

1. Invoke `Skill("test-everything:test-plan")` to produce a phased test
   strategy tailored to the current project. It will read `user-stories.md`,
   `architecture.md`, and `ux-plan.md` automatically.
2. Invoke `Skill("test-everything:test-scaffold", args: "e2e")` to generate
   test files and CI pipeline stubs.
3. Cross-reference generated specs against `e2e-tests.md`. Every listed
   scenario must have a generated spec. File the remaining gaps as tasks in
   `phase-10-plan.md`.
4. Verification: `npx playwright test --list` (or equivalent) shows every
   planned scenario. Log output path in `progress.md`.

## Phase 11 — Testing & Verification

**Goal**: the full test suite is green, with coverage acceptable to
`test-everything`.

1. Invoke `Skill("test-everything:test-full-suite")`. This runs unit →
   integration → e2e in sequence.
2. If anything fails, invoke `Skill("test-everything:test-contract")`. This
   dispatches fix agents with confrontational mandates until tests pass. Do
   **not** mute or skip failing tests — the contract skill exists to resolve
   incomplete work, not paper over it.
3. Repeat until green or escalation (3-strike protocol from `bo-planner`).
4. Record final results (pass count, coverage, flakes observed) in
   `progress.md` under a `## Phase 11 Results` block.

### Phase 11.5 — Design Quality Gate (conditional)

Skip if project has no UI.

1. Invoke `Skill("standard-design:review")`. It writes
   `docs/planning/design-compliance.md`.
2. Read the critical issue count. Gate rule:
   - `0 critical` → pass, proceed to 11.6
   - `> 0 critical` → block. Return to Phase 9 to fix, then re-run 11 + 11.5.
3. Users may override with `--skip-design-review` but must confirm via
   `AskUserQuestion` and the override reason is logged in `progress.md`.

### Phase 11.6 — Enterprise Quality Gate

1. Invoke `Skill("enterprise-assessment:assess")`. It writes
   `docs/planning/enterprise-assessment.md` (or project-root report if no
   planning session is active).
2. Read overall grade and risk posture. Default gate rule:
   - Grade `A` or `B` → pass
   - Grade `C` or worse → block. Surface Critical/High findings. Return to
     Phase 9 to remediate, then re-run 11→11.6.
3. Users may lower the threshold (`--enterprise-threshold=C`) but must confirm
   and the override is logged in `progress.md`.
4. The Critical + High findings are imported as rows in the next phase's
   `plan-gaps.md` seed (with `Source = enterprise-assessment.md:<category>`).

## Phase 12 — Delivery

1. Invoke `Skill("bo-planner:done")` (runs the completion verification
   protocol). It checks cross-plugin quality gates and surfaces a unified
   completion summary.
2. If the user confirms, mark phases 9–12 `complete` in `phased-plan.md`.
3. Do **not** stop here — phases 13–14 are the difference between "delivered"
   and "delivered without plan drift".

## Phase 13 — Plan Gap Audit

**Goal**: produce `docs/planning/plan-gaps.md` listing every delta between the
planning artifact set and the implemented code.

1. If `docs/planning/plan-gaps.md` does not exist, copy the template from the
   bo-planner plugin (`skills/bo-planning/templates/plan-gaps.md`).
2. Audit each artifact against the code. Dispatch one subagent per artifact
   for parallel speed (they share no state):

   | Subagent | Reads | Checks |
   | -------- | ----- | ------ |
   | user-stories auditor | `user-stories.md` + code | Every story has an implementation and test |
   | architecture auditor | `architecture.md` + code | Every component/boundary/endpoint exists |
   | tech-guide auditor | `tech-guide.md` + `package.json`/`Cargo.toml`/`pyproject.toml` | Dependency versions match, conventions followed |
   | ux auditor | `ux-plan.md` + running app | Every user flow reachable, error paths implemented |
   | ui auditor | `ui-plan.md` + rendered UI | Tokens match, components follow design system |
   | e2e auditor | `e2e-tests.md` + test files | Every planned scenario has a passing spec |
   | phase auditor | each `phase-#-plan.md` | Every task checkbox matches reality |

3. Seed gaps from Phase 11.6 (Critical/High findings from
   `enterprise-assessment.md`).
4. Each gap gets a row: id, source, expected, actual, severity, owner phase,
   status.
5. Also capture **out-of-scope deviations** (code that exists but was never
   planned) in the dedicated table. Decide per row: keep + document, or
   remove.
6. Present the gap list to the user. Ask:
   - "Confirm severities look right?"
   - "Any gaps to mark `wont_fix` with reason?"
7. Verification: see the checklist at the bottom of `plan-gaps.md`. Phase 13
   is complete only when user approves.

## Phase 14 — Fix All Gaps

**Goal**: `plan-gaps.md` shows zero `open` non-`wont_fix` rows.

1. Sort gaps by severity: `blocker` → `major` → `minor` → `nit`.
2. Work blockers serially (they may depend on each other). Dispatch parallel
   subagents for independent `major`/`minor`/`nit` gaps.
3. For each gap:
   - Implement the fix in the owner layer (frontend, backend, tests, docs).
   - Re-run the relevant verification (unit test for unit-test gap, e2e for
     flow gap, design-review for design gap, etc.).
   - Flip status to `fixed` with a one-line note.
4. After all gaps in a severity tier are closed, re-run the gates that
   produced them:
   - Test gaps → `test-everything:test-full-suite`
   - Design gaps → `standard-design:review`
   - Enterprise gaps → `enterprise-assessment:assess`
5. Any new gaps surfaced by re-run get appended to `plan-gaps.md`. Loop back
   to step 1.
6. Verification: gap count = 0 open non-`wont_fix`, all three gates pass,
   `bo-planner:done` re-run is clean. Mark phases 13 and 14 `complete` in
   `phased-plan.md`.

## Resume Behavior

If interrupted, `/implement-bo-plan:resume` picks up where progress stopped:

1. Read `phased-plan.md` to find the first non-`complete` phase.
2. Read `progress.md` for the last entry. If mid-phase, continue from the
   next unchecked task in that `phase-#-plan.md`.
3. If any gate failed previously (recorded in `progress.md`), restart from
   the failing gate, not from phase 9.

## Override Flags

When invoked as `/implement` with flags, apply these overrides and log each
to `progress.md`:

| Flag | Effect |
| ---- | ------ |
| `--skip-design-review` | Design gate becomes informational (warn, don't block) |
| `--skip-enterprise` | Enterprise gate becomes informational |
| `--enterprise-threshold=<A|B|C>` | Lower the passing grade |
| `--allow-failing-tests` | **Discouraged.** Tests warn instead of block. Requires typed confirmation. |
| `--gaps-ok` | Phase 14 exits when only `wont_fix` gaps remain, user must accept |
| `--phase=<n>` | Run only that phase (same as `/phase <n>`) |

Every override requires `AskUserQuestion` confirmation and is recorded.

## Anti-Patterns

| Don't | Do Instead |
| ----- | ---------- |
| Start Phase 9 with incomplete planning artifacts | Run preflight; block until `bo-planner:plan` is done |
| Skip the test-contract loop to "get it over with" | Let `test-everything:test-contract` drive until green |
| Mute or delete failing tests to clear Phase 11 | Fix the code; the test failure is the signal |
| Accept a C grade silently | Surface Critical/High findings; require user override |
| Stop at Phase 12 because the user said "looks good" | Phase 13 still runs — gap audit is the real contract |
| Fix gaps without re-running gates | Every severity tier closes with a re-run of its gate |
| Add features found during gap audit as "scope expansion" | They're either gaps (plan says so → fix) or OOS deviations (plan doesn't say so → decide with user) |
| Run audit subagents sequentially | Artifact audits are independent → dispatch in parallel |

## Integration with Other Skills

| Skill | When |
| ----- | ---- |
| `bo-planner:bo-planning` | Prerequisite — produces the plan this skill consumes |
| `agents-argue:debate` | Phase 9 when an unplanned tradeoff appears |
| `standard-design:scaffold` | Phase 9 for UI pages/components |
| `standard-design:review` | Phase 11.5 gate, Phase 13 UI audits |
| `test-everything:test-plan` | Phase 10 — strategy |
| `test-everything:test-scaffold` | Phase 10 — generation |
| `test-everything:test-full-suite` | Phase 11 — execution |
| `test-everything:test-contract` | Phase 11 — failure remediation loop |
| `enterprise-assessment:assess` | Phase 11.6 gate |
| `enterprise-assessment:drill` | Phase 14 when remediating a specific category |
| `bo-planner:done` | Phase 12 — completion protocol |
| `superpowers:dispatching-parallel-agents` | Whenever 2+ independent tasks exist |
| `superpowers:verification-before-completion` | Before marking any phase `complete` |

## Core Pattern

```
Plan is memory. Gates are contracts. Gaps are the diff.
Phase 9 implements; phase 11 verifies; phase 13 audits; phase 14 closes.
Nothing ships with open plan gaps.
```
