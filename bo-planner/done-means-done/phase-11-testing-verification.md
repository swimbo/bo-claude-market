# Phase 11 — Testing & Verification: Done Means Done

## Objective recap

Run every test layer, verify user-story acceptance criteria, and produce evidence that the system actually works.

## Artifacts (must exist and be non-empty)

- `docs/planning/progress.md > ## Test Results` — latest test run summary with timestamp.
- Test runner output (logs, reports) linked or pasted.

## Hard Gates

- [ ] **Unit tests pass**: full suite run, exit code 0. Evidence: command + output timestamp.
- [ ] **Integration tests pass** (if present): exit code 0.
- [ ] **E2E / Playwright tests pass** (if Phase 10 applies): exit code 0; no tests skipped without a logged reason.
- [ ] **Lint clean**: canonical lint command exit code 0.
- [ ] **Type-check clean** (typed languages): exit code 0.
- [ ] **Build succeeds**: canonical build exit code 0.
- [ ] **User-story acceptance**: for each P0 story, acceptance criteria have been walked through and checked off. For web/CLI projects, this means a live run of the flow — not code inspection.
- [ ] **Dark-pattern sanity**: for UX projects, a manual pass against `ux-plan.md > ## Dark Pattern Audit` confirms no regressions.
- [ ] **Accessibility spot-check** (UI projects): keyboard navigation, focus order, and contrast sampled on primary flows. Issues filed as `plan-gaps` if found.
- [ ] **No unresolved errors**: `progress.md > ## Errors` has zero open entries.
- [ ] **Cross-plugin verification considered**: `/done` warnings on Enterprise Assessment, Design Compliance, and Test Coverage reviewed (if those artifacts exist). Blocker-class issues either fixed or explicitly accepted by the user in `progress.md`.

## Soft Checks

- [ ] Coverage metric captured (even if not a hard target) for triage later.
- [ ] Smoke test harness runs in under a documented time budget.
- [ ] Flaky tests quarantined with tickets, not silently re-run.

## Blocking condition

If the `test-everything:test-full-suite` or `test-everything:test-audit` skills are applicable, they should be invoked. Skipping requires explicit user decision logged in `progress.md`.

## Exit Signal

> "Every automated test layer is green, every P0 story has been exercised for real, and the error log is empty."

After this phase, Phase 12 can present the result to the user for final sign-off.
