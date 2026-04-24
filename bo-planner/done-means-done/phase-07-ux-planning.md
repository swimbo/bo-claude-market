# Phase 7 — UX Planning: Done Means Done

## Objective recap

Design user flows, interaction patterns, accessibility, and error handling. Skip only for backend-only or pure-library projects.

## Artifacts (must exist and be non-empty)

- `docs/planning/ux-plan.md` — populated from the template.
- `docs/planning/findings.md` — contains `## Phase 7 Kickoff Research`.

## Hard Gates

- [ ] **Kickoff research done**: `findings.md > ## Phase 7 Kickoff Research` captures current WCAG guidance, interaction patterns, and AI/agent UX references applicable to this project.
- [ ] **Primary flows mapped**: `ux-plan.md > ## Flows` traces every P0/P1 user story step-by-step from entry to outcome, including branch points and dead-ends.
- [ ] **Interaction patterns**: inputs, controls, navigation, state persistence, and feedback described per surface.
- [ ] **Error handling**: every flow lists error states (validation, network, auth, permission, rate-limit) and recovery affordances.
- [ ] **Empty / loading / partial states**: every flow calls out its empty, loading, and partial-data states.
- [ ] **Accessibility**: WCAG 2.2 AA target declared and applied. Keyboard operation, focus order, screen-reader labels, contrast, motion preferences addressed.
- [ ] **Dark pattern audit**: `ux-plan.md > ## Dark Pattern Audit` confirms we are not dark-patterning the user (no forced continuity, roach motels, confirmshaming, sneak-into-basket).
- [ ] **CLI / TUI guidance** *(if applicable)*: 12-Factor CLI principles and Heroku CLI standards referenced; help output, exit codes, progress signals, machine-readable mode planned.
- [ ] **IDE plugin guidance** *(if applicable)*: host-platform affordances (VS Code containers, JetBrains UI paradigms) respected.
- [ ] **AI interaction guidance** *(if applicable)*: Microsoft HAX guidelines considered — disclose AI, handle uncertainty, allow correction/undo.
- [ ] **Cross-reference to research**: `research/ux-design.md` cited where applicable.
- [ ] **User stories covered**: every P0/P1 story from `user-stories.md` is represented in at least one flow.

## Soft Checks

- [ ] Latency budgets per interaction (e.g. "first meaningful paint < 1s").
- [ ] Internationalization / localization stance declared even if deferred.
- [ ] Offline / flaky-network behavior described.

## Skip condition

Phase 7 may be skipped for backend-only or pure-library projects. **Partial UX** (API ergonomics, tool descriptions for LLM "users") may still apply — see `SKILL.md` table.

**If skipped**: record skip reason in `ux-plan.md` (a stub file with a single paragraph is fine), mark phase `skipped` in `phased-plan.md`.

## Exit Signal

> "Every P0/P1 user story has a walked-through flow with errors, empty states, and accessibility addressed."

After this phase, Phase 8 can style flows that are already structurally correct.
