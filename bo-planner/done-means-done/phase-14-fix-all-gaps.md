# Phase 14 — Fix All Gaps: Done Means Done

## Objective recap

Work through `plan-gaps.md` in severity order. Every non-`wont_fix` row ends the phase as `fixed` with evidence.

## Artifacts (must exist and be non-empty)

- `docs/planning/plan-gaps.md` — each row resolved to `fixed` or `wont_fix` (no rows left `open` or `in_progress`).
- `docs/planning/progress.md` — Phase 14 session log with per-gap resolutions linked.

## Hard Gates

- [ ] **Severity order respected**: `blocker` rows closed before `major`, `major` before `minor`, `minor` before `nit`. Evidence: timestamps in `progress.md` show monotonic order by severity bucket.
- [ ] **Zero open blockers**: `plan-gaps.md` contains no `blocker` rows with status `open`, `in_progress`, or `wont_fix`. Blockers **cannot** be accepted as `wont_fix`; they must be fixed or scope must be renegotiated with the user.
- [ ] **Zero open majors**: every `major` row is `fixed` or `wont_fix` with explicit user sign-off in `progress.md`.
- [ ] **Minors & nits**: every row is `fixed` or `wont_fix` (user sign-off line optional for `nit` but recommended for `minor`).
- [ ] **Per-fix evidence**: every `fixed` row cites the resolving commit SHA / PR / diff and the re-run test result.
- [ ] **Re-run relevant tests per fix**: tests exercising each fixed item were re-run and pass. Evidence: test output linked from `progress.md`.
- [ ] **Full-suite re-run at end**: after the last fix, the full test suite (unit + integration + e2e, as applicable) has been re-run and passes. Evidence timestamped in `progress.md > ## Test Results`.
- [ ] **Artifact reconciliation**: where a gap was resolved by updating a planning artifact (rather than code), the artifact edit is committed and `plan-gaps.md` notes `fix type: artifact-update`.
- [ ] **Volatile replacements debated**: any fix that introduces a replacement library, service, model, or architectural pattern (i.e. falls into a Volatile Decision Category) has a Mode B debate brief in `docs/planning/decisions/` and an entry in `decisions/INDEX.md` **before** its gap row is flipped to `fixed`.
- [ ] **Re-audit**: a quick re-check of the most-affected artifacts confirms no new drift was introduced by the fixes. Summary line in `progress.md`.
- [ ] **User final sign-off**: the user has confirmed `plan-gaps.md` is clean and the project is deliverable. Evidence: timestamped `progress.md` entry.

## Soft Checks

- [ ] For each `wont_fix`, the rationale is durable (points to scope, cost, or external dependency) rather than "we ran out of time".
- [ ] `wont_fix` items that should become future work are copied to `findings.md > ## Follow-ups`.
- [ ] If any fix introduced non-trivial refactor, a short note captured in `progress.md` for future maintenance.

## Blocking condition

Phase 14 is **never** complete with any `open` or `in_progress` row. `wont_fix` is only valid for `major`, `minor`, `nit` (never `blocker`) and requires a logged user sign-off.

## Exit Signal

> "Plan and implementation match. Every gap was fixed or explicitly accepted. Tests are green. The user has confirmed closure."

After this phase, the project is genuinely done — not "code complete," but plan-reconciled-done.
