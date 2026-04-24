# Phase 10 — E2E Test Generation: Done Means Done

## Objective recap

Generate Playwright (or equivalent CLI) tests derived from user stories and UX flows so Phase 11 has executable evidence, not vibes.

## Artifacts (must exist and be non-empty)

- `docs/planning/e2e-tests.md` — populated from the template.
- `docs/planning/findings.md` — contains `## Phase 10 Kickoff Research`.
- Test files checked into the project's conventional test directory.

## Hard Gates

- [ ] **Kickoff research done**: current Playwright API surface and best practices captured in `findings.md > ## Phase 10 Kickoff Research` (web-app projects) or current CLI-testing practice (CLI projects).
- [ ] **Story-to-test traceability**: `e2e-tests.md > ## Coverage Matrix` maps every P0 story — and every P1 story with observable UX — to at least one test file/test case with a stable ID.
- [ ] **Flow-to-test traceability**: every primary flow in `ux-plan.md` is exercised by at least one test.
- [ ] **Happy-path + error-path coverage**: for each mapped story, both a happy-path case and at least one error/edge case exist.
- [ ] **Test files committed**: test source files exist, conform to `tech-guide.md` conventions, and are discovered by the canonical test runner command.
- [ ] **Runner config**: `playwright.config.*` (or equivalent) committed with correct base URL, browsers, timeouts, and retries for CI vs. local.
- [ ] **Selectors policy**: tests use stable selectors (roles, labels, `data-testid`) — not brittle CSS/XPath. Policy stated in `e2e-tests.md > ## Selector Policy`.
- [ ] **Dry run**: the test runner can at minimum **collect/discover** all tests without errors. Evidence: command output pasted into `progress.md`.
- [ ] **Flakiness stance**: condition-based waits used instead of arbitrary sleeps. `e2e-tests.md > ## Waiting Strategy` explicitly forbids sleeps except where documented.

## Soft Checks

- [ ] Fixtures / test data factories documented.
- [ ] Page objects or equivalent abstractions used for non-trivial flows.
- [ ] Visual-regression strategy declared (even if "none, out of scope").

## Skip condition

Phase 10 may be skipped when the project has no testable UI or CLI. API-only backends still get **integration tests** (not fully e2e) — not a skip.

**If skipped**: record skip reason in `e2e-tests.md` (stub), mark phase `skipped` in `phased-plan.md`.

## Exit Signal

> "Tests exist, discover cleanly, and every P0/P1 user story and primary UX flow has at least one test."

After this phase, Phase 11 can run these tests against a real build.
