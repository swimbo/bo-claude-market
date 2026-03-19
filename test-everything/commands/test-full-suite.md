---
name: test-full-suite
description: Full testing workflow — audit gaps, plan strategy, scaffold infrastructure, write tests, run them, and fix until everything passes
argument-hint: "[path-to-project]"
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "Agent"]
---

# Test Everything

End-to-end testing workflow: audit, plan, build, run, fix, repeat until green.

## Non-Negotiable Rules

These rules are absolute. You MUST NOT rationalize, work around, or make exceptions. If you catch yourself thinking "just this once" or "it's simpler to..." — STOP. You are about to write a bad test.

### Banned Patterns — NEVER Write These

| Banned Pattern                                                                     | Why It's Banned                                                                                             | What to Write Instead                                                                                                          |
| ---------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `page.waitForTimeout(N)` / `await sleep(N)`                                        | Arbitrary waits cause flakiness and hide bugs. Tests pass on fast machines, fail on slow CI.                | `await expect(locator).toBeVisible()`, `await page.waitForResponse(...)`, `await page.waitForURL(...)`                         |
| `page.locator('.css-class')` / `page.locator('#id')`                               | CSS selectors don't verify accessibility. A `<div class="btn">` matches but isn't a real button.            | `page.getByRole('button', { name: '...' })`, `page.getByLabel('...')`, `page.getByText('...')`                                 |
| `await btn.click()` without a following assertion                                  | Fire-and-forget clicks prove nothing. The click might throw, navigate nowhere, or trigger a 500.            | `await btn.click(); await expect(page).toHaveURL(...)` or `await expect(page.getByText('Success')).toBeVisible()`              |
| `test.fixme(...)` / `test.skip(...)` / `test.todo(...)`                            | Skipping tests to get green is lying about coverage. A skipped test is worse than no test — it hides a gap. | Fix the root cause. If the test is hard to write, that's a signal the app has a bug or the test approach is wrong.             |
| `expect(text.length).toBeGreaterThan(0)`                                           | This asserts "something exists" — not that the RIGHT thing exists.                                          | `expect(text).toContain('Expected Content')` or `await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible()` |
| `expect(mainText).toContain("Profile")` after `page.locator("main").textContent()` | Scraping text content bypasses accessibility and tests strings instead of features.                         | `await expect(page.getByRole('heading', { name: 'Profile' })).toBeVisible()`                                                   |
| `await expect(page).toHaveURL(/\/route/)` as the ONLY assertion                    | Verifying the URL didn't change is not testing the feature — it's testing that a redirect didn't break.     | Add assertions that verify the page content, interactive elements, and feature behavior — not just the URL.                    |

### Test Quality Minimums

Every test you write MUST meet ALL of these criteria:

1. **Feature verification, not page verification**: Tests must verify that features WORK, not just that pages LOAD. "The page renders content" is not a test — "The user can create a document and see it in the list" IS a test.
2. **Every interaction has an outcome assertion**: After every `click()`, `fill()`, `check()`, or `selectOption()`, there MUST be an `expect()` or `waitForResponse()` within the next 3 lines verifying the outcome.
3. **Specific assertions over vague assertions**: `expect(page.getByText('John Smith')).toBeVisible()` not `expect(text.length).toBeGreaterThan(0)`.
4. **No hardcoded waits**: Zero instances of `waitForTimeout`, `setTimeout`, or `sleep`. Use Playwright's built-in auto-waiting: `toBeVisible()`, `waitForURL()`, `waitForResponse()`.
5. **Accessible selectors**: Use `getByRole` > `getByLabel` > `getByText` > `getByTestId` (last resort). Never use CSS class or ID selectors for test interactions.

### When a Test Is Hard to Write

If you find yourself wanting to use `waitForTimeout`, `test.fixme`, or weaker assertions, STOP and diagnose:

* **Element not found?** → The page may have a loading state. Use `await expect(locator).toBeVisible({ timeout: 10000 })` — Playwright will retry automatically.

* **Form fill gets lost?** → React is re-rendering during hydration. Wait for a SPECIFIC interactive element first: `await expect(page.getByRole('button', { name: 'Submit' })).toBeVisible()` before filling. Then verify the fill stuck: `await expect(page.getByLabel('Email')).toHaveValue(email)`. If fills still get lost, use API-first registration instead of UI forms (see Phase 0 Step 6).

* **Auth state bleeds between tests?** → Use `test.describe.configure({ mode: 'serial' })` or create a fresh browser context per test: `const context = await browser.newContext(); const page = await context.newPage();` — don't forget `await context.close()` in a finally block.

* **Browser install fails with EPERM?** → Sandbox blocks the default Playwright cache dir. Set `PLAYWRIGHT_BROWSERS_PATH=.playwright-browsers` or `PLAYWRIGHT_BROWSERS_PATH=/tmp/pw-browsers` (see Phase 0 Step 1).

* **`webServer` config times out?** → Sandbox blocks `nice()` and process spawning is slow. Remove the `webServer` block entirely and pre-start servers before running tests (see Phase 0 Step 3).

* **Strict mode violation (multiple elements match)?** → Use `.first()` or scope the locator to a specific container: `page.getByRole('list').getByText('item')` instead of `page.getByText('item')`.

* **Test is flaky?** → The app has a real bug (race condition, missing loading state). Fix the app, not the test.

* **Can't figure it out after 3 attempts?** → Document the issue as a bug report, create a test that asserts the EXPECTED behavior (it will fail), and tell the user. Never silently skip.

### Examples: BAD Tests vs. GOOD Tests

**BAD** — Tests that passed in both failure reports but proved nothing:

```typescript
// BAD: "page loads" test — proves nothing about the feature
test("page loads and renders content", async ({ page }) => {
  await page.goto("/knowledge-base");
  await page.waitForTimeout(3000); // BANNED: arbitrary wait
  const mainText = await page.locator("main").textContent(); // BANNED: CSS selector
  expect(mainText?.trim().length).toBeGreaterThan(0); // BANNED: vague assertion
});

// BAD: URL-only test — proves the router works, not the feature
test("url stays on /knowledge-base (not redirected)", async ({ page }) => {
  await page.goto("/knowledge-base");
  await page.waitForTimeout(1000); // BANNED: arbitrary wait
  await expect(page).toHaveURL(/\/knowledge-base/); // WEAK: only tests URL
});

// BAD: giving up on a test
test.fixme("login with invalid password shows error", async ({ page }) => {
  // BANNED: test.fixme hides a real gap
});
```

**GOOD** — Tests that actually verify features work:

```typescript
// GOOD: verifies the feature works end-to-end
test("user can create a KB document and see it in the list", async ({ page }) => {
  await page.goto("/knowledge-base");
  await page.getByRole('button', { name: 'New Document' }).click();
  await page.getByLabel('Title').fill('Test Document');
  await page.getByLabel('Content').fill('Test content for verification');
  const saveResponse = page.waitForResponse(r =>
    r.url().includes('/api/') && r.request().method() === 'POST'
  );
  await page.getByRole('button', { name: 'Save' }).click();
  await saveResponse;
  await expect(page.getByText('Test Document')).toBeVisible();
});

// GOOD: tests actual error behavior with real assertions
test("login with invalid password shows error", async ({ page }) => {
  await page.goto("/login");
  await page.getByLabel('Email').fill('user@test.com');
  await page.getByLabel('Password').fill('WrongPassword!');
  await page.getByRole('button', { name: /sign in/i }).click();
  await expect(page.getByText(/invalid.*password/i)).toBeVisible();
  await expect(page).toHaveURL(/\/login/);
});

// GOOD: verifies settings actually persist (desired outcome)
test("profile changes persist after page reload", async ({ page }) => {
  await page.goto("/settings");
  await page.getByLabel('Display Name').fill('New Name');
  await page.getByRole('button', { name: 'Save' }).click();
  await expect(page.getByText(/saved|updated/i)).toBeVisible();
  await page.reload();
  await expect(page.getByLabel('Display Name')).toHaveValue('New Name');
});
```

## Instructions

Execute the full testing lifecycle for the project at the given path (or cwd).

### Phase 0: E2E Environment Setup (MANDATORY — Do Not Skip)

Before writing or running ANY E2E test, you MUST set up the environment to work reliably in sandbox. This phase exists because E2E tests consistently fail in Claude Code's macOS sandbox due to permission restrictions, browser cache issues, and server startup timeouts. Every step here was learned from real failures.

See `references/e2e-sandbox-patterns.md` for full details and rationale. Execute these steps:

1. **Install Playwright browsers to a writable path** — the default `~/Library/Caches/ms-playwright/` is blocked by sandbox:
   ```bash
   # Use project-local path (add .playwright-browsers/ to .gitignore)
   PLAYWRIGHT_BROWSERS_PATH=.playwright-browsers npx playwright install chromium
   ```
   If this fails with EPERM, fall back to `/tmp/pw-browsers`.

2. **Set `PLAYWRIGHT_BROWSERS_PATH` in ALL npm scripts** that run Playwright:
   ```json
   {
     "test:e2e": "PLAYWRIGHT_BROWSERS_PATH=.playwright-browsers playwright test",
     "test:e2e:ui": "PLAYWRIGHT_BROWSERS_PATH=.playwright-browsers playwright test --ui"
   }
   ```

3. **Remove or never add `webServer` in `playwright.config.ts`** — it times out in sandbox because `nice()` fails and server startup is blocked. Instead, configure the Playwright config with just `baseURL` and no `webServer` block.

4. **Verify dev servers are running** before running tests — use `curl` to check:
   ```bash
   curl -sf http://localhost:5173 > /dev/null && echo "Frontend OK" || echo "Frontend NOT running"
   curl -sf http://localhost:3000/api/health > /dev/null && echo "Backend OK" || echo "Backend NOT running"
   ```
   If servers aren't running, start them in background and poll until ready (do NOT sleep a fixed duration).

5. **Configure sandbox-safe timeouts** in `playwright.config.ts`:
   ```typescript
   export default defineConfig({
     timeout: 60000,           // 60s per test (sandbox is slower)
     expect: { timeout: 10000 }, // 10s for expect assertions
     retries: 1,
     fullyParallel: false,     // Avoid resource contention in sandbox
   });
   ```

6. **Create API-first auth helpers** — NEVER register test users through UI forms. React re-renders during hydration swallow `page.fill()` calls. Always register and authenticate via API, then inject the auth token into browser localStorage before navigating:
   ```typescript
   // Register via API (always works)
   const response = await fetch(`${baseURL}/api/auth/register`, {
     method: 'POST',
     headers: { 'Content-Type': 'application/json' },
     body: JSON.stringify({ email, password, fullName: 'E2E Test User' }),
   });
   // Inject token into browser
   await page.goto(baseURL);
   await page.evaluate((token) => localStorage.setItem('token', token), token);
   await page.reload();
   ```

7. **Wait for React hydration** before interacting with forms — wait for a specific interactive element (like a submit button) to be visible before filling inputs:
   ```typescript
   await page.goto('/login');
   await expect(page.getByRole('button', { name: /sign in/i })).toBeVisible();
   // NOW fill the form — React is done rendering
   await page.getByLabel('Email').fill(email);
   ```

**Phase 0 verification**: Before proceeding to Phase 1, confirm:
- [ ] Playwright browsers installed (run `PLAYWRIGHT_BROWSERS_PATH=.playwright-browsers npx playwright --version`)
- [ ] Dev servers responding (curl both frontend and backend)
- [ ] `playwright.config.ts` has NO `webServer` block
- [ ] `playwright.config.ts` has `timeout: 60000`

### Phase 1: Audit

Perform the same analysis as `/test-everything:test-audit`:

1. Detect project type, languages, frameworks
2. Inventory existing tests and configs
3. Assess each testing layer (unit, integration, component, E2E, performance, security, accessibility)
4. Assess E2E coverage against user stories and desired outcomes (check for `docs/planning/user-stories.md` — see test-audit Steps 3b, 3d, 3e)
5. Assess exhaustive interaction coverage — check if all interactive elements on all pages are tested (see test-audit Step 3d)
6. Identify gaps — output a brief summary table (not the full report)

### Phase 2: Plan

Based on the audit, determine what needs to be built:

1. Select the appropriate testing architecture model (Pyramid/Diamond/Trophy)
2. Prioritize gaps — focus on the highest-impact missing layers first
3. List the specific test files and configs to create
4. Present the plan to the user as a checklist and wait for approval before proceeding

### Phase 3: Scaffold & Write Tests

For each item in the approved plan:

1. Scaffold any missing test infrastructure (configs, setup files, directories)
2. Install missing dependencies via the project's package manager
3. Write tests that verify features work — not just that pages load (see Non-Negotiable Rules):

   * **Read the source code** being tested — understand what the function/component/route actually does before writing a test for it

   * **Test behavior, not existence**: "user creates item and sees it in list" not "page renders content"

   * **Cover the unhappy path**: invalid input, unauthorized access, empty states, error responses

   * **Every click/fill/check MUST have an outcome assertion** within 3 lines — see Banned Patterns table

   * Follow existing project patterns and conventions

   * Co-locate tests with source when that's the project convention

   * **Before writing each E2E test, ask yourself**: "If this feature were completely broken, would this test catch it?" If the answer is no, the test is too weak — rewrite it.
4. Use parallel subagents for independent test files when possible

#### Component Tests (Frontend)

For projects with a frontend, write component tests for complex interactive UI components:

1. Identify components with significant logic: forms, data tables, modals, interactive widgets, permission-gated views
2. Test each component in isolation covering: all visual states (loading, empty, error, success), user interactions (clicks, input, keyboard), prop variations, and conditional rendering
3. Use React Testing Library + Vitest — test behavior, not implementation details
4. Skip simple presentational components that are just markup wrappers

#### User-Story-Driven E2E Tests with Desired Outcome Assessment

E2E tests MUST be derived from user story workflows, MUST use interaction verification, and MUST assess **desired outcomes** — the measurable end-states that prove each feature works correctly.

**Before writing any E2E tests:**

1. Scaffold the browser health fixture (`e2e/fixtures/browser-health.ts`) — see test-scaffold for the template
2. All generated E2E tests must import `test` and `expect` from `./fixtures/browser-health`, not from `@playwright/test`

**Interaction verification rule:** Every interaction (`click()`, `fill()`, `check()`, `selectOption()`, form submission) MUST be followed by at least one assertion verifying the outcome — a URL change, DOM change, network response, or element state change. A test that clicks without verifying is incomplete.

**Generate E2E specs:**

1. **Check for user stories**: Look for `docs/planning/user-stories.md` in the project root
2. **If the file exists**:

   * Parse every user story — its workflow steps, acceptance criteria, and **desired outcomes**

   * Create one E2E spec file per user story (e.g., `e2e/user-story-registration.spec.ts`)

   * Each spec must test every step in the user story workflow, in sequence

   * Map acceptance criteria directly to test assertions

   * **Every workflow step must pair the user action with an outcome assertion** — not just perform the action

   * Group related stories into describe blocks by feature area

   * **Add a desired outcome assessment test** at the end of each story's spec — a test that executes the full workflow and then explicitly verifies every desired outcome:

     ```typescript
     test('Desired outcomes: [list outcomes]', async ({ page }) => {
       // Execute full workflow end-to-end
       // ...

       // ASSESS each desired outcome
       // Outcome 1: [description] — verify via [method]
       expect(actualResult).toBe(expectedResult);
       // Outcome 2: ...
     });
     ```
3. **If the file does NOT exist**:

   * Analyze the codebase to infer user story workflows:

     * Scan routes/pages to identify user-facing features

     * Read API endpoints to understand data flows

     * Examine navigation, forms, and interactive components

     * Identify authentication/authorization boundaries

   * Generate a `docs/planning/user-stories.md` file documenting the inferred stories using this format:

     ```
     ## US-001: [Story Title]
     **As a** [role], **I want to** [action], **so that** [benefit].

     ### Workflow Steps
     1. [Step 1 — specific user action]
     2. [Step 2 — expected system response]

     ### Acceptance Criteria
     - [ ] [Criterion 1]
     - [ ] [Criterion 2]

     ### Desired Outcomes
     | # | Outcome | How to Verify | Expected Result |
     |---|---------|---------------|-----------------|
     | 1 | [What success looks like] | [API / URL / DOM / data] | [Expected value] |
     | 2 | [Second outcome] | [Method] | [Expected value] |
     ```

   * For each story, define 2-5 **desired outcomes** — observable, specific, end-to-end results

   * Present the inferred user stories to the user for approval before writing E2E tests

   * After approval, create E2E specs covering each story's workflow steps and desired outcomes
4. **Coverage mapping**: After writing E2E tests, output a traceability matrix:

   ```
   | User Story | E2E Spec File | Steps Covered | Outcomes Defined | Outcomes Assessed | Status |
   |------------|---------------|---------------|------------------|-------------------|--------|
   | US-001     | e2e/...       | 5/5           | 3                | 3/3 ✅            | Full   |
   | US-002     | e2e/...       | 3/4           | 2                | 1/2 ⚠️            | Partial|
   ```

#### Common E2E Tests

In addition to user-story specs, write cross-cutting E2E tests not tied to any single story:

1. **Smoke tests** (`e2e/smoke.spec.ts`) — homepage loads, login works, main nav links resolve, API health responds
2. **Error pages** (`e2e/error-pages.spec.ts`) — 404 for unknown routes, unauthorized redirects, API error handling, empty states
3. **Responsive** (`e2e/responsive.spec.ts`) — critical pages at mobile (375px), tablet (768px), and desktop (1280px) viewports
4. **Navigation** (`e2e/navigation.spec.ts`) — deep links, back/forward, redirects, URL state preservation
5. **Visual regression** (`e2e/visual-regression.spec.ts`, optional) — screenshots at key workflow completion points using `toHaveScreenshot()`, only if user opts in

#### Post-Suite Walkthrough

After writing all individual E2E tests, write a walkthrough test:

1. Chain the top 3-5 user story workflows into a single continuous test (`e2e/walkthrough.spec.ts`)
2. Maintain browser session state between flows — no page reloads between stories
3. Use the browser health fixture to catch cross-flow console errors and network failures
4. This test runs AFTER all individual E2E tests pass (Phase 4)
5. See test-scaffold for the walkthrough template

#### Exhaustive Interaction Crawl

After user-story and common E2E tests, scaffold and write an exhaustive interaction test that discovers and tests EVERY interactive element on every page:

1. **Discover all routes** by analyzing the project's router config (React Router, Next.js pages, etc.)
2. **Scaffold** `e2e/exhaustive-interactions.spec.ts` — see test-scaffold for the full template
3. For each route, the test must:

   * **Reveal hidden elements** — click unselected tabs, expand collapsed accordions, open `<details>` elements, expand `aria-expanded="false"` sections

   * **Discover all interactive elements** — buttons, links, inputs, textareas, selects, checkboxes, radios, switches, menu items

   * **Test every button** — click it and rely on browser health fixture to catch JS errors and failed API requests; if navigation occurs, go back; if a dialog opens, dismiss it

   * **Validate every link** — verify `href` is not empty or `"#"`

   * **Test every input** — fill it with test data and verify it accepts input

   * **Test sub-tab content** — click each tab within a page and test the buttons/links inside the tab panel

   * **Test dropdown menus** — open each dropdown trigger and verify menu items exist and are functional
4. The browser health fixture is what makes this powerful — every click that triggers a JS error or failed API request automatically fails the test
5. This test is a **safety net** that catches interactive elements missed by user-story tests
6. Add script: `"test:e2e:exhaustive": "playwright test exhaustive-interactions.spec.ts"`
7. Run AFTER walkthrough test in Phase 4

#### UX Quality Audit

After functional tests are written, audit the application's user experience:

1. Launch the app in Playwright and crawl all routes
2. Evaluate against Nielsen's 10 usability heuristics — score each 1-5
3. Scan for dark patterns (trick questions, hidden costs, confirmshaming, bad defaults)
4. Check feedback loops: every interactive element must produce visible feedback within 100ms
5. Check error message quality: plain language, resolution steps, no cryptic codes
6. Check for missing confirmation dialogs on destructive actions (delete, overwrite, etc.)
7. Output a prioritized UX audit report (see test-scaffold `ux` layer for full checklist)
8. Implement the top 3-5 improvements — add loading states, confirmations, error messages
9. If CLI: check help text, command structure, error output, stream separation

#### UI Visual Quality Audit

After UX audit, evaluate the visual interface quality:

1. Run axe-core contrast checks on every page — flag all WCAG failures
2. Count font families (target ≤ 3), check heading hierarchy, verify monospaced for code
3. Check spacing consistency — look for irregular padding/margins breaking grid alignment
4. Check component consistency — all buttons same style, all inputs same style, all states defined
5. Check visual hierarchy — primary CTA dominant on each page, clear section separation
6. Check semantic color usage — red only for errors/destructive, green only for success
7. Output a prioritized UI audit report with screenshots (see test-scaffold `ui` layer for full checklist)
8. Implement the top 3-5 improvements — fix contrast, standardize components, normalize spacing
9. Take before/after screenshots to verify visual improvements

### Phase 3.5: Mandatory Self-Review (BLOCKING — Do Not Skip)

**Before running any tests**, you MUST review your own generated test files for violations of the Non-Negotiable Rules. This phase exists because past runs wrote tests with banned patterns, declared them "passing", and moved on — producing test suites that verified nothing.

**Run these checks on every test file you wrote:**

1. **Grep for banned waits** — search all new test files for `waitForTimeout`, `setTimeout`, `sleep`:
   * If ANY are found: replace them with proper Playwright auto-waits before proceeding
   * Allowed exception: `waitForTimeout(300)` ONLY in the exhaustive interaction crawl for animation settling (not in user-story or feature tests)

2. **Grep for CSS/ID selectors** — search for `locator('.'`, `locator('#'`, `locator('[data-testid`:
   * If ANY are found in interaction code (click, fill): replace with `getByRole`, `getByLabel`, or `getByText`
   * `data-testid` is allowed ONLY when no accessible selector exists

3. **Grep for fire-and-forget clicks** — search for `.click()` not followed by `expect(` or `waitFor` within 3 lines:
   * If ANY are found: add outcome assertions after each click
   * Every click must verify: URL change, DOM change, or network response

4. **Grep for skipped tests** — search for `test.fixme`, `test.skip`, `test.todo`:
   * If ANY are found: remove the skip and fix the test or report the underlying bug

5. **Grep for vague assertions** — search for `toBeGreaterThan(0)`, `toBeTruthy()` used on page content, `textContent()` followed by `length`:
   * If ANY are found: replace with specific content assertions (`toContain('specific text')`, `toBeVisible()` on specific elements)

6. **Review each E2E test for feature coverage** — for each test file, answer:
   * Does this test verify that a FEATURE works, or just that a PAGE loads?
   * If I broke this feature, would this test catch it?
   * If the answer to either is "no" — rewrite the test before proceeding

**Output a self-review report before moving to Phase 4:**
```
### Self-Review Results
- Banned waits found and fixed: N
- CSS selectors found and fixed: N
- Fire-and-forget clicks found and fixed: N
- Skipped tests found and fixed: N
- Vague assertions found and fixed: N
- Tests rewritten for feature coverage: N
- VERDICT: PASS (all checks clean) / FIXED (violations found and corrected)
```

If you cannot produce this report, you have not completed Phase 3.5. Do NOT proceed to Phase 4.

### Phase 4: Run & Fix

Loop until all tests pass:

1. Run the full test suite using the project's test command
2. If tests fail:

   * Analyze the failure output

   * Determine if the bug is in the test or the source code

   * **If browser health fixture caught console errors or failed network requests**, fix the source code — these are real bugs, not test issues

   * Fix the root cause — don't weaken tests to make them pass

   * **Never disable the browser health fixture to make tests pass** — if it's catching errors, the app has bugs

   * Re-run and repeat
3. If tests pass, run linting/type-checking if available
4. Fix any lint or type errors introduced
5. Verify browser health monitoring is active — confirm test output shows the fixture loaded (no console errors, no failed requests)
6. Run the exhaustive interaction crawl (`test:e2e:exhaustive`) to verify all interactive elements across all pages work without errors — fix any elements that trigger JS errors or API failures when clicked
7. Run desired outcome assessment tests — verify all defined outcomes pass; if any fail, investigate whether the issue is in the test or the application

### Phase 5: Quality Review (Second Self-Review)

After all tests pass, perform a SECOND review of the test suite. This catches any violations introduced during Phase 4 fix iterations:

1. **Re-run Phase 3.5 checks**: Grep for all banned patterns again (waits, CSS selectors, fire-and-forget clicks, skipped tests, vague assertions). Phase 4 fix loops sometimes introduce new violations — catch them here.
2. **Anti-patterns**: Scan new test files for tests with no assertions, snapshot-only tests, excessive mocking, implementation-detail testing, tautological assertions, commented-out tests
3. **Flakiness risks**: Check for hardcoded timeouts, shared mutable state, system time dependencies, missing `await` in async tests, network calls without mocking in unit tests
4. **Architecture alignment**: Verify test distribution matches the recommended model (Pyramid/Diamond/Trophy) — flag if too many E2E tests relative to unit tests or if integration layer has gaps
5. **The "break it" test**: For each E2E spec file, mentally simulate: "If I deleted the feature this test covers, would the test fail?" If the answer is "probably not" — the test is too weak and must be rewritten.
6. Fix any issues found before proceeding to summary

### Phase 6: Summary

Once everything is green and quality-reviewed, output:

```
## Test Everything — Complete

### Tests Added
- [list of new test files with test counts]

### Infrastructure Created
- [configs, CI files, setup files]
- Browser health fixture: e2e/fixtures/browser-health.ts

### User Story Coverage & Desired Outcome Assessment
| User Story | E2E Spec File | Steps Covered | Outcomes Defined | Outcomes Assessed | Status |
|------------|---------------|---------------|------------------|-------------------|--------|
| US-001     | e2e/...       | 5/5           | 3                | 3/3 ✅            | Full   |
| ...        | ...           | ...           | ...              | ...               | ...    |

### Desired Outcome Assessment Summary
| User Story | Outcome | Expected Result | Actual Result | Status |
|------------|---------|-----------------|---------------|--------|
| US-001     | Account created | API returns 201 with user ID | 201 + ID present | ✅ Pass |
| US-001     | User can log in | Redirect to /dashboard | /dashboard | ✅ Pass |
| US-002     | Data saved | Success toast visible | Toast not shown | ❌ Fail |

Overall: X of Y desired outcomes passing (Z%)

### Interaction Verification
| Check | Result | Status |
|-------|--------|--------|
| Action-outcome pairing | X of Y interactions verified (Z%) | ✅/⚠️/❌ |
| Selector quality | X% accessible locators | ✅/⚠️/❌ |
| Browser health monitoring | Active | ✅ |

### Exhaustive Interaction Coverage
| Page/Route | Interactive Elements | Tested (Story) | Tested (Exhaustive) | Total Coverage |
|------------|---------------------|-----------------|---------------------|----------------|
| /dashboard | N                   | N               | N                   | N%             |
| /settings  | N                   | N               | N                   | N%             |

Untested elements:
- [page]: [list of untested buttons, links, forms by accessible name]

Elements tested ONLY by exhaustive crawl (not covered by any user story):
- [page]: [list — these are coverage gaps in user stories]

Note: Generate this report by using Playwright to visit each route after E2E tests
complete, query for all interactive elements (button, a[href], input, select,
textarea, [role="button"], [role="checkbox"], [role="switch"]), and cross-reference
against elements the tests actually interacted with. The exhaustive crawl fills gaps
left by user-story tests.

### Coverage Change
- Before: [if known]
- After: [run coverage if available]

### Test Quality
- Anti-patterns: [count found and fixed]
- Flakiness risks: [count found and fixed]
- Architecture: [model] — [distribution summary]

### All Passing
- [test command]: ✅ N tests passed
- [lint command]: ✅ clean
- Browser health: ✅ No console errors, no failed API requests
- Walkthrough: ✅ Full session test passed
- Exhaustive crawl: ✅ All interactive elements functional (N elements across M routes)
- Desired outcomes: ✅ X of Y outcomes passing
```

### Guidelines

* Never skip Phase 2 approval — the user must confirm the plan before you write code

* Never skip Phase 3.5 self-review — it is the most important quality gate

* Write tests that would actually catch regressions, not just tests that pass

* If fixing a test failure requires changing source code, explain what the bug is before fixing

* **NEVER weaken a test to make it pass** — fix the source code or fix the test approach. Using `test.fixme`, removing assertions, adding `waitForTimeout`, or switching to vague assertions to avoid a failure is strictly prohibited.

* **A test that always passes is worthless** — if you can't think of a scenario where the test would fail, it's not testing anything meaningful

* **When you encounter a flaky test**, the correct response is: investigate the root cause (race condition? missing loading state? auth state leak?), fix the root cause in the application code, then verify the test passes consistently. The INCORRECT response is: add `waitForTimeout`, mark `test.fixme`, or weaken the assertion.

* Use the test-strategy skill for guidance on any testing type

* Don't install tools outside the project's preferred stack without asking

* **Completion claim checklist** — before telling the user "all tests pass" or "testing is complete", verify:
  1. Phase 3.5 self-review report was output
  2. Zero banned patterns remain in any test file
  3. Every E2E test verifies a feature, not just a page load
  4. Every user story has at least one desired outcome assessment test
  5. Test count is proportional to feature count (3 tests for 14 routes is too few)