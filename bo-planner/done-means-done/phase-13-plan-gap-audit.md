# Phase 13 — Plan Gap Audit: Done Means Done

## Objective recap

Diff the implemented code against every planning artifact and record each missing, partial, or deviated item. Produce a single authoritative gap list for Phase 14 to close.

## Artifacts (must exist and be non-empty)

- `docs/planning/plan-gaps.md` — populated from the template.

## Hard Gates

- [ ] **Full artifact coverage**: the audit has diffed the implemented code against **each** of these artifacts:
  - `user-stories.md` (every story ID)
  - `architecture.md` (every component + API)
  - `tech-guide.md` (every version + convention)
  - `ux-plan.md` (every flow, error/empty/loading state)
  - `ui-plan.md` (every token, component, state)
  - `e2e-tests.md` (every mapped story/flow)
  - Each `phase-#-plan.md` (every task in Tasks + every item in Verification)
- [ ] **Per-gap fields**: every row in `plan-gaps.md` has: `id`, `source artifact`, `source item`, `gap type (missing | partial | deviated)`, `severity (blocker | major | minor | nit)`, `proposed fix`, `status (open)`.
- [ ] **Severity rubric applied**:
  - `blocker` — IN-scope requirement missing or broken core flow.
  - `major` — significant quality, accessibility, or correctness gap.
  - `minor` — cosmetic or low-impact drift.
  - `nit` — style / polish.
  Rubric stated at the top of `plan-gaps.md`.
- [ ] **No phantom gaps**: every gap cites a concrete source line (artifact file + heading) and, where applicable, a concrete code file + location showing absence or deviation.
- [ ] **No missed artifacts**: a completeness line at the top of `plan-gaps.md` of the form `Audited against: user-stories.md, architecture.md, tech-guide.md, ux-plan.md, ui-plan.md, e2e-tests.md, phase-1-plan.md … phase-N-plan.md`. Any "not applicable" entry lists the reason.
- [ ] **User review**: the gap list has been presented to the user. The user has confirmed severities (or corrected them) and identified `wont_fix` rows with rationale. Confirmation recorded in `progress.md`.
- [ ] **Sorted by severity**: `plan-gaps.md` rows are ordered `blocker → major → minor → nit`.
- [ ] **Silent volatile decisions flagged**: the audit has identified any volatile-category choice (LLM/model, AI SDK, third-party service, datastore, framework version, dep major, architectural pattern, auth strategy, data contract, deploy/CI, observability) that was adopted during Phase 9 without a Mode B debate brief. Each one is recorded as a `major` gap in `plan-gaps.md`.

## Soft Checks

- [ ] For each blocker/major gap, an estimate (rough T-shirt size) of fix effort is recorded.
- [ ] Related gaps are grouped or cross-referenced (avoid redundant Phase-14 work).
- [ ] Any deviation discovered that is **better** than the plan is recorded with a recommendation to update the source artifact rather than the code.

## Exit Signal

> "We have an honest, complete, user-confirmed list of every way the implementation drifted from the plan, ordered by severity."

After this phase, Phase 14 closes every non-`wont_fix` gap.
