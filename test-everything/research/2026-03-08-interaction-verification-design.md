# Interaction Verification Design — test-everything Plugin

**Date:** 2026-03-08
**Status:** Brainstormed, ready for planning
**Problem:** Tests pass but app is still broken — buttons don't work, workflows fail

## Problem Analysis

After running the full test suite (`/test-everything:test-full-suite`), applications still have functional issues discovered through manual testing. The plugin generates Playwright E2E tests from user stories, they run against a live full-stack app, they pass — but the app is broken.

### Root Causes

1. **Missing outcome assertions** — Tests click buttons but don't verify what happened next. Playwright won't fail if a click does nothing.
2. **Ignoring browser errors** — Uncaught JS exceptions, failed network requests, and console errors happen silently during test runs.
3. **Testing existence, not behavior** — `expect(button).toBeVisible()` proves the button renders, not that it works.
4. **Implementation-detail testing** — Tests interact with the app in ways no real user would (CSS selectors, internal state checks).

### Key Insight

> "The more your tests resemble the way your software is used, the more confidence they can give you." — Kent C. Dodds

## Chosen Approach: Interaction Verification

Make the generated tests smarter — every click/submit/navigate MUST have a paired assertion verifying the outcome. Add console error monitoring and network request validation.

### Current (broken pattern)

```typescript
await page.click('#submit-btn');
// test passes even if nothing happened
```

### Proposed (verification pattern)

```typescript
await page.click('#submit-btn');
// MUST verify one of:
await expect(page).toHaveURL('/dashboard');            // navigation
await expect(page.getByText('Saved')).toBeVisible();   // DOM change
await page.waitForResponse(resp =>                      // network
  resp.url().includes('/api/') && resp.status() === 200
);
```

## Prioritized Recommendations

### Priority 1: Action-Outcome Pairing (Very High Impact, Medium Effort)

Every generated test action MUST be followed by an assertion verifying the outcome.

**Changes needed:**
- Update E2E scaffold templates in `commands/test-scaffold.md`
- Update full-suite test generation in `commands/test-full-suite.md`
- Enforce action + expected outcome pairs when mapping user story acceptance criteria to test steps
- Add guidance in `skills/test-strategy/` references

### Priority 2: Console Error = Test Failure (High Impact, Low Effort)

Any uncaught JS error or unhandled promise rejection during a test should automatically fail it.

**Implementation — shared Playwright fixture:**

```typescript
test.beforeEach(async ({ page }) => {
  const errors: string[] = [];
  page.on('pageerror', err => errors.push(err.message));
  page.on('console', msg => {
    if (msg.type() === 'error') errors.push(msg.text());
  });
  (page as any).__consoleErrors = errors;
});

test.afterEach(async ({ page }) => {
  const errors = (page as any).__consoleErrors || [];
  expect(errors, 'Browser console errors detected').toEqual([]);
});
```

### Priority 3: Failed Network Request Detection (High Impact, Low Effort)

Track API calls during tests. If an expected API call returns 4xx/5xx or fails, the test should fail.

**Implementation — shared fixture addition:**

```typescript
test.beforeEach(async ({ page }) => {
  const failedRequests: string[] = [];
  page.on('requestfailed', req => {
    failedRequests.push(`${req.method()} ${req.url()} - ${req.failure()?.errorText}`);
  });
  page.on('response', resp => {
    if (resp.status() >= 400 && resp.url().includes('/api/')) {
      failedRequests.push(`${resp.status()} ${resp.url()}`);
    }
  });
  (page as any).__failedRequests = failedRequests;
});

test.afterEach(async ({ page }) => {
  const failed = (page as any).__failedRequests || [];
  expect(failed, 'API requests failed during test').toEqual([]);
});
```

### Priority 4: User-Centric Selectors (Medium-High Impact, Medium Effort)

Generated tests should use accessible selectors instead of CSS selectors or data-testid.

**Selector priority order:**
1. `getByRole` (button, link, textbox, etc.)
2. `getByLabel` (form inputs)
3. `getByText` (visible text)
4. `data-testid` (last resort)

**Why:** If an element can't be found by its accessible role/name, it's often not properly wired up. Using `getByRole('button', { name: 'Submit' })` verifies the element is actually a functioning button, not just a `<div>` styled to look like one.

### Priority 5: Post-Suite Smoke Walkthrough (Medium Impact, Medium Effort)

After all individual tests pass, run one final "happy path walkthrough" test that simulates a real user session end-to-end.

**Why:** Individual tests run in isolation with clean state. A full walkthrough catches issues that only appear when steps interact (state pollution, navigation breaking after certain actions, auth session issues).

**Implementation:** Add a `walkthrough` test template to E2E scaffold. Generated from user stories but run as a single connected flow.

### Priority 6: Interaction Coverage Report (Medium Impact, High Effort)

After running E2E tests, generate a coverage report showing which interactive elements on each page were actually tested.

**Output example:**
```
/dashboard: 12 interactive elements, 8 tested (67%)
  UNTESTED: [Export CSV] button, [Filter] dropdown, [Settings] link, [Notifications] bell
```

### Priority 7: Visual Regression on Critical Pages (Medium Impact, Low Effort)

Take screenshots at key workflow completion points using Playwright's `toHaveScreenshot()`.

**Not every test** — just the top 3-5 most important pages/states. Lightweight visual regression without needing an external service.

## Research Sources

### Primary Sources
- [Playwright Best Practices](https://playwright.dev/docs/best-practices)
- [Playwright Assertions](https://playwright.dev/docs/test-assertions)
- [Kent C. Dodds - Testing Implementation Details](https://kentcdodds.com/blog/testing-implementation-details)
- [Kent C. Dodds - The Testing Trophy](https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications)
- [Kent C. Dodds - Write tests. Not too many. Mostly integration.](https://kentcdodds.com/blog/write-tests)
- [Kent C. Dodds - Avoid the Test User](https://kentcdodds.com/blog/avoid-the-test-user)

### Supporting Sources
- [Playwright Network Interception](https://playwright.dev/docs/network)
- [Smashing Magazine - Frontend Testing Pitfalls](https://www.smashingmagazine.com/2021/07/frontend-testing-pitfalls/)
- [Google Testing Crab - web.dev](https://web.dev/articles/ta-strategies)
- [BrowserStack - Playwright Best Practices 2026](https://www.browserstack.com/guide/playwright-best-practices)
- [Better Stack - Playwright Best Practices](https://betterstack.com/community/guides/testing/playwright-best-practices/)
- [Chromatic - Visual Testing with Playwright](https://www.chromatic.com/blog/how-to-visual-test-ui-using-playwright/)
- [User-Centric Testing with React Testing Library](https://marmelab.com/blog/2023/05/26/react-user-centric-testing.html)
- [MSW - Mock Service Worker](https://mswjs.io/)
- [Mocking is an Anti-Pattern - AmazingCTO](https://www.amazingcto.com/mocking-is-an-antipattern-how-to-test-without-mocking/)

## Anti-Patterns to Address in Plugin

| Anti-Pattern | Current Risk | Fix |
|---|---|---|
| Testing implementation details | Tests use CSS selectors, internal state | Switch to role/label/text selectors |
| Fire-and-forget interactions | Tests click without verifying outcome | Action-outcome pairing |
| Ignoring runtime errors | Console errors don't fail tests | Console error monitoring fixture |
| Happy-path-only coverage | Missing error states, edge cases | Generate negative path tests |
| Isolated test state | Tests don't catch cross-flow bugs | Post-suite walkthrough |
| No visual verification | Layout breaks pass functional tests | Screenshot assertions on critical pages |
