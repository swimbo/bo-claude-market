# Plugin Integration Guide

When multiple plugins from this marketplace are installed on the same project, they automatically detect and consume each other's artifacts. This eliminates duplicate scanning, enables a unified development lifecycle, and provides quality gates across planning, design, testing, and enterprise readiness.

## Integrated Lifecycle

The six core plugins form a natural workflow. `bo-planner` owns phases 1–8 (planning) with `agents-argue` as a mandatory debate gate. `implement-bo-plan` owns phases 9–14 (execution) and chains the remaining plugins:

```
/bo-planner:plan                               # Phases 1-8
  ├─ /agents-argue:debate (architecture.md)    # Phase 5 gate
  └─ /agents-argue:debate (tech-guide.md)      # Phase 6 gate
                            ↓
/implement-bo-plan:implement                   # Phases 9-14
  ├─ /standard-design:scaffold                 # Phase 9 (UI)
  ├─ /test-everything:test-plan + scaffold     # Phase 10
  ├─ /test-everything:test-full-suite          # Phase 11
  ├─ /test-everything:test-contract            # Phase 11 on failure
  ├─ /standard-design:review                   # Phase 11.5 gate
  ├─ /enterprise-assessment:assess             # Phase 11.6 gate (≥ B)
  ├─ plan-gaps.md audit (parallel subagents)   # Phase 13
  └─ severity-ordered gap fixes + gate re-runs # Phase 14
                            ↓
/bo-planner:done                               # Final sign-off
```

| Phase | Plugin | What It Does |
|-------|--------|-------------|
| 1–4. Plan (early) | bo-planner | Requirements, pain point research, data map, user stories |
| 5–6. Plan (decisions) | bo-planner + agents-argue | Architecture and tech guide drafted, then debated to consensus |
| 7–8. Plan (UX/UI) | bo-planner | UX and UI plans (when user-facing) |
| 9. Implementation | implement-bo-plan + standard-design | Parallel subagents build tasks; UI work scaffolded against the design system |
| 10. E2E Tests | implement-bo-plan + test-everything | Strategy + generated specs from user stories |
| 11. Testing | implement-bo-plan + test-everything | Full suite run; `test-contract` loop on failure |
| 11.5. Design Gate | implement-bo-plan + standard-design | `review` — blocks on critical issues |
| 11.6. Enterprise Gate | implement-bo-plan + enterprise-assessment | `assess` — blocks if grade < B |
| 12. Delivery | bo-planner | `done` completion protocol |
| 13. Plan Gap Audit | implement-bo-plan | Parallel artifact-vs-code diff → `plan-gaps.md` |
| 14. Fix Gaps | implement-bo-plan | Severity-ordered fixes with gate re-runs until zero open |

## How Plugins Read Each Other's Artifacts

### bo-planner produces artifacts that others consume

bo-planner creates structured artifacts in `docs/planning/` that other plugins detect and use:

| Artifact | Consumed By | How It's Used |
|----------|-------------|--------------|
| `user-stories.md` | test-everything | Acceptance criteria become test assertions; each story maps to an E2E spec |
| `architecture.md` | test-everything | API endpoints generate integration test stubs; service boundaries define test fixtures |
| `architecture.md` | enterprise-assessment | Tech stack context informs all 12 assessment categories |
| `ux-plan.md` | test-everything | User flows (happy + error paths) become E2E test scenarios |
| `ux-plan.md` | standard-design | Interaction patterns inform scaffold error handling and loading states |
| `ui-plan.md` | standard-design | Planned design tokens validated against Standard Design System defaults |
| `phased-plan.md` | enterprise-assessment | Scope fence focuses assessment on in-scope components only |

### standard-design produces artifacts that others consume

| Artifact | Consumed By | How It's Used |
|----------|-------------|--------------|
| `src/theme/ThemeModeProvider.tsx` | enterprise-assessment | Code Quality category credits design system adoption |
| `src/theme/ThemeModeProvider.tsx` | test-everything | Flags need for theme-aware component tests and dark/light visual regression |
| `docs/planning/design-compliance.md` | enterprise-assessment | Code Quality assessor uses compliance findings as evidence |
| `docs/planning/design-compliance.md` | bo-planner `/done` | Warns if critical design issues remain before delivery |

### test-everything produces artifacts that others consume

| Artifact | Consumed By | How It's Used |
|----------|-------------|--------------|
| Test results / `.test-results/` | enterprise-assessment | Testing category uses results as authoritative evidence instead of re-scanning |
| Coverage metrics | enterprise-assessment | Testing score based on actual coverage data |
| Test results | bo-planner `/done` | Blocks delivery if tests are failing |

### enterprise-assessment produces artifacts that others consume

| Artifact | Consumed By | How It's Used |
|----------|-------------|--------------|
| `docs/planning/enterprise-assessment.md` | bo-planner `/done` | Warns if grade < B before delivery; shows risk posture |
| `docs/planning/enterprise-assessment.md` | implement-bo-plan | Phase 11.6 gate — blocks phase 12 if grade < B. Critical/High findings seed `plan-gaps.md`. |
| `docs/planning/enterprise-assessment.md` | test-everything | Testing category gaps become P0 priorities in test plans |
| Assessment report | enterprise-assessment `/compare` | Baseline for measuring improvement over time |

### agents-argue produces artifacts that others consume

| Artifact | Consumed By | How It's Used |
|----------|-------------|--------------|
| `docs/planning/consensus-plan.md` | bo-planner | Phase 5/6 gate — decisions are incorporated back into `architecture.md` and `tech-guide.md` before the phase can be marked complete |
| `docs/planning/debate-transcript.md` | bo-planner `findings.md` | Unresolved items tagged `NEEDS_HUMAN_DECISION` are surfaced to the user |
| `consensus-plan.md` | implement-bo-plan | Phase 9 respects debate outcomes when implementing contested tradeoffs |

### implement-bo-plan produces artifacts that others consume

| Artifact | Consumed By | How It's Used |
|----------|-------------|--------------|
| `docs/planning/plan-gaps.md` | bo-planner `/done` | Blocks final sign-off if open non-`wont_fix` gaps remain |
| `docs/planning/plan-gaps.md` | enterprise-assessment | Gap severities seed remediation priorities on next `assess` run |
| `docs/planning/progress.md` (phase 9–14 entries) | bo-planner `/status` | Unified status across planning + execution |
| Gate results in `progress.md` | implement-bo-plan `/resume` | Identifies the failing gate as the restart point |

## Output Location Convention

When a bo-planner planning session is active (`docs/planning/phased-plan.md` exists), other plugins save their reports to `docs/planning/` instead of the project root:

| Plugin | Default Output | With Active Planning Session |
|--------|---------------|------------------------------|
| enterprise-assessment | `enterprise-assessment-report.md` | `docs/planning/enterprise-assessment.md` |
| standard-design review | Inline only | `docs/planning/design-compliance.md` |
| test-everything | Various | Unchanged (tests live in test directories) |

This consolidation means `/bo-planner:status` shows a unified view of planning, design, testing, and assessment state.

## Quality Gates in `/bo-planner:done`

When you run `/bo-planner:done`, it checks for other plugins' artifacts and includes their results:

```
Completion check:
- Phases: 7/7
- User stories: 12/12 implemented
- Tests: 47/47 passing
- Scope: 8/8 items delivered
- Unresolved errors: 0
- Enterprise assessment: B (82%) — CONDITIONAL
- Design compliance: 0 critical issues
```

| Check | Source | Behavior |
|-------|--------|----------|
| Enterprise assessment grade | `enterprise-assessment.md` | **Warns** if grade < B |
| Design compliance | `design-compliance.md` | **Warns** if critical issues > 0 |
| Test results | Test runner output | **Blocks** if tests are failing |

Warnings are informational — the user decides whether to proceed. Test failures are blockers.

## Standard Design in UI Planning

The bo-planner `ui-plan.md` template includes Standard Design System tokens as defaults:

- Color roles pre-filled with Standard Design tokens (`accent`, `charcoal`, `textPrimary`, etc.)
- Typography scale pre-filled with Standard Design fonts (Outfit, DM Sans, JetBrains Mono)
- Projects can override any token while keeping the rest

When `/standard-design:scaffold` runs, it reads `ui-plan.md` and validates that planned tokens align with Standard Design. Conflicts are flagged so the user can decide whether to use Standard defaults or their custom values.

## Example: Full Integrated Workflow

```bash
# 1. Plan the feature
/bo-planner:plan "user management CRUD with roles"
# Creates docs/planning/ with architecture.md, user-stories.md, ui-plan.md, etc.

# 2. Scaffold pages using planned constraints
/standard-design:scaffold list user
/standard-design:scaffold form user
/standard-design:scaffold detail user
# Reads ui-plan.md for design constraints, ux-plan.md for interaction patterns

# 3. Review design compliance
/standard-design:review src/pages/
# Saves findings to docs/planning/design-compliance.md

# 4. Generate and run tests
/test-everything:test-full-suite
# Reads user-stories.md for E2E test scenarios
# Reads architecture.md for API integration test stubs

# 5. Assess enterprise readiness
/enterprise-assessment:assess
# Reads architecture.md for context
# Consumes test results for Testing category
# Consumes design compliance for Code Quality
# Saves report to docs/planning/enterprise-assessment.md

# 6. Verify and deliver
/bo-planner:done
# Checks: all phases complete, tests passing,
# assessment grade >= B, design compliance clean
```

## Which Plugins to Install

All plugins work independently. Install only what you need:

| If you need... | Install |
|---------------|---------|
| Structured planning | bo-planner |
| Design system compliance | standard-design |
| Test coverage and quality | test-everything |
| Enterprise readiness assessment | enterprise-assessment |
| Full integrated lifecycle | All four |

Cross-plugin features activate automatically when artifacts are detected — no configuration required.
