# User Stories — Interaction Verification Improvements

## US-001: Action-Outcome Pairing in Generated Tests

**As a** plugin user running `/test-everything:test-scaffold e2e`, **I want** the generated E2E tests to pair every interaction (click, submit, navigate) with an assertion verifying the outcome, **so that** tests actually catch broken buttons and failing workflows.

### Workflow Steps
1. User runs `/test-everything:test-scaffold e2e`
2. Plugin reads user stories from `docs/planning/user-stories.md`
3. For each workflow step, plugin generates an action + outcome assertion pair
4. Generated test file includes the verification pattern (not just `page.click()`)

### Acceptance Criteria
- [ ] Every `page.click()`, `page.fill()`, `form.submit()` in generated tests is followed by at least one assertion
- [ ] Assertions verify one of: URL change, DOM change, or network response
- [ ] Template includes comments explaining the verification pattern
- [ ] Existing user-story-driven generation logic is preserved (not broken)

---

## US-002: Console Error Detection

**As a** plugin user running `/test-everything:test-full-suite`, **I want** browser console errors and unhandled JS exceptions to automatically fail my E2E tests, **so that** runtime errors don't silently pass.

### Workflow Steps
1. User runs `/test-everything:test-scaffold e2e` or `/test-everything:test-full-suite`
2. Plugin includes a shared Playwright fixture file in the scaffolded output
3. Fixture registers `pageerror` and `console.error` listeners in `beforeEach`
4. Fixture asserts no errors in `afterEach`
5. Any runtime JS error fails the test with a clear message

### Acceptance Criteria
- [ ] Scaffold output includes `e2e/fixtures/browser-health.ts` template
- [ ] Fixture catches `pageerror` events (uncaught exceptions)
- [ ] Fixture catches `console.error` messages
- [ ] Error messages are included in the test failure output
- [ ] Tests that have expected errors can opt out (allowlist pattern)

---

## US-003: Failed Network Request Detection

**As a** plugin user, **I want** my E2E tests to fail when API requests return 4xx/5xx errors or fail entirely, **so that** broken API integrations are caught.

### Workflow Steps
1. Plugin scaffolds the browser-health fixture (same file as US-002)
2. Fixture registers `requestfailed` and `response` listeners
3. Failed API requests (4xx/5xx on `/api/` URLs) are collected
4. `afterEach` asserts no unexpected failures

### Acceptance Criteria
- [ ] Fixture monitors `requestfailed` events
- [ ] Fixture monitors responses with status >= 400 on API URLs
- [ ] Pattern for API URL detection is configurable (default: `/api/`)
- [ ] Expected error responses can be excluded per-test

---

## US-004: User-Centric Selectors

**As a** plugin user, **I want** generated E2E tests to use accessible selectors (`getByRole`, `getByLabel`, `getByText`) instead of CSS selectors, **so that** tests verify elements are properly accessible and functional.

### Workflow Steps
1. Plugin generates E2E test code from user stories
2. Selectors in generated code prioritize: `getByRole` > `getByLabel` > `getByText` > `data-testid`
3. Quality reviewer flags CSS selector usage as an anti-pattern
4. Audit checks whether existing tests use accessible selectors

### Acceptance Criteria
- [ ] Generated test templates use `page.getByRole()`, `page.getByLabel()`, `page.getByText()` as primary selectors
- [ ] `data-testid` and CSS selectors are documented as last resort
- [ ] test-quality-reviewer flags `page.click('[data-testid=...]')` as a warning
- [ ] test-audit reports selector quality in its assessment

---

## US-005: Post-Suite Smoke Walkthrough

**As a** plugin user, **I want** a single end-to-end walkthrough test that simulates a complete user session, **so that** cross-flow state issues are caught that isolated tests miss.

### Workflow Steps
1. Plugin scaffolds a `walkthrough.spec.ts` template
2. Walkthrough connects user story flows into a single continuous test
3. Test runs after all individual E2E tests pass
4. No page reloads between steps (simulates real session)

### Acceptance Criteria
- [ ] Scaffold includes `e2e/walkthrough.spec.ts` template
- [ ] Template chains the top user story workflows into one test
- [ ] Test maintains browser state between steps (no isolated contexts)
- [ ] full-suite command runs walkthrough after individual E2E tests

---

## US-006: Interaction Coverage Report

**As a** plugin user, **I want** a report showing which interactive elements on each page were tested, **so that** I know where coverage gaps exist.

### Workflow Steps
1. After E2E tests run, plugin crawls each route
2. Plugin inventories all interactive elements (buttons, links, forms, inputs)
3. Plugin cross-references against elements interacted with during tests
4. Plugin outputs coverage report per page

### Acceptance Criteria
- [ ] full-suite Phase 6 includes interaction coverage report
- [ ] Report lists each page/route with interactive element count
- [ ] Report shows which elements were tested vs untested
- [ ] Untested elements are listed by name/label/role

---

## US-007: Visual Regression on Critical Pages

**As a** plugin user, **I want** screenshot-based visual regression tests on critical pages, **so that** layout and rendering breaks are caught.

### Workflow Steps
1. Plugin scaffolds `e2e/visual-regression.spec.ts` template
2. Template uses `expect(page).toHaveScreenshot()` at key workflow endpoints
3. Only critical pages are included (not every test)
4. User opts in during scaffold

### Acceptance Criteria
- [ ] Scaffold includes visual regression template
- [ ] Template covers top 3-5 critical page states
- [ ] Uses Playwright's built-in `toHaveScreenshot()`
- [ ] Template includes guidance on baseline management
