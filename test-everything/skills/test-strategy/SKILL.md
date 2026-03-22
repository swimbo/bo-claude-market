---
name: test-strategy
description: This skill should be used when the user asks about "testing strategy", "what tests to write", "testing types", "test pyramid", "test diamond", "testing trophy", "what should I test", "testing architecture", "quality gates", "CI/CD testing", "shift-left testing", "test coverage gaps", "performance testing", "security testing", "accessibility testing", "E2E testing", "integration testing", "how to test", "test automation", "testing best practices", "test plan", "test coverage", "desired outcomes", "outcome assessment", "exhaustive testing", "interaction crawl", "click every button", or discusses how to plan, structure, or improve testing in a project. Provides comprehensive knowledge of all software testing types, architecture models, and implementation strategies tailored to React + Vitest, Rust, Playwright, and k6.
version: 0.1.0
---

# Testing Strategy Knowledge Base

Comprehensive testing knowledge covering all testing types, architecture models, quality gates, and implementation strategies. Tailored to projects using React + Vitest (frontend), Rust `#[test]` (backend), Playwright (E2E), and k6 (performance).

## Testing Classification

Testing divides along three axes:

| Axis     | Categories                                                       |
| -------- | ---------------------------------------------------------------- |
| **What** | Functional (correctness) vs. Non-Functional (quality attributes) |
| **How**  | Manual vs. Automated                                             |
| **When** | Static (no execution) vs. Dynamic (running code)                 |

## Functional Testing Layers

### Unit Testing

* **Scope**: Individual functions, methods, classes in isolation

* **Speed**: Milliseconds | **Run**: Every commit

* **Tools**: Vitest (frontend), Rust `#[test]` (backend)

* **Target**: 80%+ line coverage on business logic

### Integration Testing

* **Scope**: Module interactions — DB queries, API calls, service boundaries

* **Speed**: Seconds | **Run**: Every PR/merge

* **Tools**: Testcontainers, supertest, SQLx test fixtures, React Testing Library

* **Target**: All critical paths covered

### End-to-End (E2E) Testing

* **Scope**: Full user workflows through real UI

* **Speed**: Seconds to minutes | **Run**: Before releases, on staging

* **Tools**: Playwright (multi-browser)

* **Target**: Every user story workflow in `docs/planning/user-stories.md`; if no user stories file exists, infer stories from the codebase first

* **Approach**: User-story-driven — one spec per story, each step tested in sequence, acceptance criteria mapped to assertions

### Interaction Verification

Every E2E test interaction must be paired with an outcome assertion. A test that clicks without verifying the result is the #1 cause of "tests pass but app is broken."

* **Principle**: Every `click()`, `fill()`, `check()`, `selectOption()` MUST be followed by an assertion verifying the outcome

* **Three verification patterns**:

  * Navigation: `await expect(page).toHaveURL(...)` — action changed the URL

  * DOM change: `await expect(page.getByText(...)).toBeVisible()` — action changed visible content

  * Network: `await page.waitForResponse(...)` — action triggered an API call

* **Browser health monitoring**: Use a shared Playwright fixture that automatically fails tests on:

  * Uncaught JS exceptions (`pageerror` events)

  * Console errors (`console.error` messages)

  * Failed API requests (4xx/5xx responses, `requestfailed` events)

* **Selector strategy**: Use accessible locators — `getByRole` > `getByLabel` > `getByText` > `data-testid` (last resort). Accessible selectors verify the element is functional, not just present in the DOM.

### Desired Outcome Assessment

User-story tests verify individual steps work. Desired outcome assessment verifies the feature achieves its purpose.

* **Concept**: For each user story, define 2-5 **desired outcomes** — the measurable end-states that prove the feature works correctly

* **Desired outcomes are**:

  * **Observable** — verifiable through UI state, API response, URL, or data

  * **Specific** — not "it works" but "user sees dashboard with their name displayed"

  * **End-to-end** — cover the full result, not just intermediate steps

* **Assessment pattern**: Each user story spec includes a final test that executes the full workflow and then explicitly assesses every desired outcome:

  1. Execute the complete workflow (registration, purchase, configuration, etc.)
  2. For each desired outcome, verify actual result matches expected result
  3. Report pass/fail per outcome with evidence

* **Example outcomes**:

  * Registration: "Account is created" → API returns 201 + user can log in

  * Purchase: "Order is placed" → confirmation page shows order ID + email received

  * Settings: "Preference is saved" → page reload preserves the setting

* **vs. acceptance criteria**: Acceptance criteria define what to test; desired outcomes define what success looks like. "User can fill the form" is a criterion. "User account is created and immediately usable" is a desired outcome.

### Exhaustive Interaction Crawling

User-story tests cover the happy paths. The exhaustive crawl covers everything else — the settings tab nobody tested, the admin dropdown behind a sub-menu, the modal with a broken close button.

* **Concept**: Systematically discover and interact with EVERY interactive element on every page, including elements hidden behind tabs, accordions, modals, and dropdowns

* **What it catches**:

  * Dead buttons (click produces no response and no error)

  * Broken links (empty or `"#"` href)

  * Non-functional form fields (input doesn't accept text)

  * JavaScript errors triggered by clicking elements nobody usually clicks

  * Failed API requests triggered by forgotten/untested features

  * Empty dropdowns (trigger opens but no menu items inside)

* **How it works**:

  1. Visit every route in the application
  2. **Reveal hidden content**: Click unselected tabs, expand collapsed accordions, open `<details>` elements, expand `aria-expanded="false"` sections
  3. **Discover all interactive elements**: query for buttons, links, inputs, textareas, selects, checkboxes, radios, switches, menu items
  4. **Test each element**: click buttons, validate link hrefs, fill inputs, open dropdowns
  5. **Browser health fixture catches errors**: every click that triggers a JS error or failed API request automatically fails the test

* **Runs AFTER** user-story and common E2E tests — it's a safety net, not a replacement

* **Not a substitute for user-story tests**: Exhaustive crawling verifies elements don't break. User-story tests verify features work correctly. Both are needed.

### Real-User Interaction Testing (Click-Through Verification)

API-first auth is correct for test setup. API-first *everything* is a test-quality disaster. The #1 way E2E tests create false confidence is by testing features through API shortcuts instead of the actual rendered UI.

* **The Rule**: Any user-facing interactive element — buttons, file inputs, dropdowns, modals, form submissions, tab switches — MUST be tested through the rendered DOM, not via `page.request.post()` or `page.evaluate()`. API shortcuts verify the backend works; they tell you nothing about whether the user can actually click the button.

* **The Canonical Failure** (failure4): An E2E test for file upload used `page.request.post('/api/documents/upload', ...)` and passed. The actual "Select Files" button was completely broken — a `hidden` class prevented the `<label>` click from reaching the `<input>`, and `onChange` never fired. The test passed for weeks while no user could upload a file. It took 5 rounds of debugging to fix once discovered manually.

* **API shortcuts are BANNED for feature verification**:

  * File uploads: use `page.waitForEvent('filechooser')` + `fileChooser.setFiles()`, not `page.request.post()`

  * Form submissions: use `page.getByLabel().fill()` + `page.getByRole('button').click()`, not `page.request.post()`

  * Button actions: use `page.getByRole('button').click()`, not `page.evaluate(() => document.querySelector('button').click())`

  * Navigation: use `page.getByRole('link').click()`, not `page.goto('/target-url')`

* **API shortcuts are CORRECT for test setup**:

  * User registration/login (auth fixture) — bypasses React re-render issues

  * Seeding test data before the test begins

  * Cleaning up test data after the test ends

  * Verifying backend state after a UI action (complementary, not a replacement)

* **The distinction**: Use APIs to *set up* the test. Use the real UI to *run* the test. Use APIs to *verify backend side-effects* after the test.

* **File upload testing pattern** (the right way):

  ```typescript
  test('user can upload a document via the UI', async ({ authedPage: page }) => {
    await page.goto('/documents');
    // Click the REAL button — this tests the full click → input → onChange chain
    const fileChooserPromise = page.waitForEvent('filechooser');
    await page.getByRole('button', { name: /select files|upload/i }).click();
    const fileChooser = await fileChooserPromise;
    await fileChooser.setFiles('test-fixtures/sample.pdf');
    // Verify the upload completed through the UI
    await expect(page.getByText('sample.pdf')).toBeVisible();
  });
  ```

* **Modal/dialog testing pattern**:

  ```typescript
  test('user can open and submit a modal form', async ({ authedPage: page }) => {
    await page.goto('/items');
    await page.getByRole('button', { name: /create|new/i }).click();
    // Verify modal opened
    await expect(page.getByRole('dialog')).toBeVisible();
    // Fill and submit through the modal's real form
    await page.getByLabel('Name').fill('Test Item');
    await page.getByRole('button', { name: /save|submit/i }).click();
    // Verify modal closed and item appeared
    await expect(page.getByRole('dialog')).not.toBeVisible();
    await expect(page.getByText('Test Item')).toBeVisible();
  });
  ```

### Clickable Element Testing (Outcome Verification)

The exhaustive crawl asks "does this element error when clicked?" Clickable element testing asks "does this element **do what it's supposed to do** when clicked?" Every interactive element on every page gets a defined expected outcome, and the test verifies expected = actual.

* **Concept**: For each page/route, build an **element outcome map** — a structured list of every interactive element and what should happen when a user interacts with it. Then write tests that verify each one through the rendered DOM.

* **What it covers** (by element type):

  | Element Type | Interaction | Expected Outcome to Verify |
  |---|---|---|
  | **Nav links** | Click | Correct URL + page heading/content renders |
  | **In-page links** | Click | Correct scroll target or anchor navigation |
  | **Action buttons** | Click | State change, API call + response, DOM update, or navigation |
  | **Submit buttons** | Click | Form data sent, success/error feedback shown |
  | **Modal triggers** | Click | Dialog opens with correct content |
  | **Modal close/cancel** | Click | Dialog closes, no state change |
  | **Form text fields** | Click/focus + type | Field gains focus, accepts input, value persists |
  | **Form field validation** | Type invalid input + blur/submit | Validation message appears |
  | **Checkboxes** | Click | Checked state toggles, dependent UI updates |
  | **Radio buttons** | Click | Selection changes, siblings deselect |
  | **Toggles/switches** | Click | State flips, associated feature enables/disables |
  | **Dropdowns/selects** | Click + select option | Menu opens, selection persists, dependent UI updates |
  | **Tabs** | Click | Correct panel shows, other panels hide |
  | **Accordions** | Click | Content expands/collapses |
  | **File inputs** | Click | File chooser opens (via `waitForEvent('filechooser')`) |
  | **Delete/destructive buttons** | Click | Confirmation dialog appears (never immediate delete) |
  | **Pagination** | Click next/prev/page | Correct page of data loads |
  | **Sort headers** | Click | Data reorders, indicator shows direction |
  | **Search/filter inputs** | Type + enter/submit | Results filter, empty state if no matches |
  | **Copy buttons** | Click | Clipboard updated, toast/feedback shown |
  | **Expand/collapse** | Click | Content toggles visibility |

* **How to build the element outcome map**:

  1. Visit each route in the running app
  2. Discover all interactive elements (buttons, links, inputs, selects, checkboxes, tabs, etc.)
  3. For each element, determine its expected outcome by reading the component source, the page context, or the user story
  4. Write one test assertion per element verifying expected = actual

* **Scaffold pattern** — one spec per page:

  ```typescript
  // e2e/clickable-elements/dashboard.spec.ts
  import { test, expect } from '../fixtures/auth';

  test.describe('Dashboard — clickable element outcomes', () => {
    test.beforeEach(async ({ authedPage: page }) => {
      await page.goto('/dashboard');
    });

    // --- Navigation links ---
    test('sidebar "Documents" link navigates to /documents', async ({ authedPage: page }) => {
      await page.getByRole('link', { name: /documents/i }).click();
      await expect(page).toHaveURL(/\/documents/);
      await expect(page.getByRole('heading', { name: /documents/i })).toBeVisible();
    });

    test('sidebar "Settings" link navigates to /settings', async ({ authedPage: page }) => {
      await page.getByRole('link', { name: /settings/i }).click();
      await expect(page).toHaveURL(/\/settings/);
    });

    // --- Action buttons ---
    test('"New Project" button opens creation modal', async ({ authedPage: page }) => {
      await page.getByRole('button', { name: /new project/i }).click();
      await expect(page.getByRole('dialog')).toBeVisible();
      await expect(page.getByRole('dialog').getByRole('heading')).toContainText(/create|new/i);
    });

    // --- Form fields ---
    test('search input accepts text and filters results', async ({ authedPage: page }) => {
      await page.getByRole('searchbox').click();
      await page.getByRole('searchbox').fill('test query');
      await expect(page.getByRole('searchbox')).toHaveValue('test query');
      // Verify filtering happened
      await page.waitForTimeout(300); // debounce
      await expect(page.getByText(/no results|test query/i)).toBeVisible();
    });

    // --- Tabs ---
    test('"Analytics" tab shows analytics panel', async ({ authedPage: page }) => {
      await page.getByRole('tab', { name: /analytics/i }).click();
      await expect(page.getByRole('tabpanel')).toBeVisible();
      await expect(page.getByRole('tabpanel').getByText(/chart|metric|data/i)).toBeVisible();
    });

    // --- File upload ---
    test('"Upload" button opens file chooser', async ({ authedPage: page }) => {
      const fileChooserPromise = page.waitForEvent('filechooser');
      await page.getByRole('button', { name: /upload|select files/i }).click();
      const fileChooser = await fileChooserPromise;
      expect(fileChooser).toBeTruthy();
    });
  });
  ```

* **Runs AFTER** user-story tests and common E2E tests — it fills the gap between "feature workflows work" and "every individual element works"

* **Relationship to other E2E layers**:

  | Layer | Question It Answers |
  |---|---|
  | User-story tests | "Does the workflow work end-to-end?" |
  | Desired outcome assessment | "Does the feature achieve its purpose?" |
  | Clickable element testing | "Does every individual element do what it should?" |
  | Exhaustive interaction crawl | "Does anything error when clicked?" |

* **vs. exhaustive crawl**: The crawl is automated discovery + error detection. Clickable element testing is deliberate mapping + outcome verification. The crawl catches "something broke." Clickable element testing catches "this button does nothing when it should open a modal." Both are needed.

### Other Functional Types

* **Regression**: Re-run full suite after changes — automate heavily

* **Smoke**: "Does the build work?" — run immediately after deployment

* **Sanity**: Targeted check after a narrow fix

* **Contract**: API agreements between services (Pact)

* **Component**: UI components in isolation (Testing Library, Storybook)

* **Acceptance (UAT)**: Business requirement validation with stakeholders

## Non-Functional Testing

### Performance Testing

| Subtype | Purpose               | Tool |
| ------- | --------------------- | ---- |
| Load    | Expected user volume  | k6   |
| Stress  | Where does it break?  | k6   |
| Spike   | Sudden traffic surges | k6   |
| Soak    | Degradation over time | k6   |

### Security Testing

| Subtype             | Purpose            | Tool                                  |
| ------------------- | ------------------ | ------------------------------------- |
| SAST                | Scan source code   | Semgrep, cargo-audit                  |
| Dependency scanning | Vuln in packages   | Snyk, Trivy, Dependabot               |
| Secret scanning     | Hardcoded creds    | git-secrets, GitHub Advanced Security |
| DAST                | Attack running app | OWASP ZAP                             |
| Penetration         | Simulated attacks  | Manual / specialized tools            |

### Accessibility Testing

* **Standard**: WCAG 2.1/2.2 (target AA level)

* **Automated**: axe-core, Lighthouse, Pa11y

* **Manual**: Keyboard navigation, screen reader testing, color contrast

* **Run**: Automated in CI + quarterly manual audit

### UX Quality Testing

* **Scope**: Heuristic evaluation, feedback loops, error messages, dark pattern detection

* **Framework**: Nielsen's 10 usability heuristics scored 1-5

* **Tools**: Playwright (crawl and interact), manual checklist, axe-core

* **Target**: All heuristics score ≥ 3, no dark patterns, all destructive actions confirmed

* **Approach**: Audit → Report → Implement top improvements → Verify

### UI Visual Quality Testing

* **Scope**: Color contrast, typography, spacing, component consistency, visual hierarchy

* **Framework**: WCAG 2.2 contrast ratios, Gestalt principles, design system auditing

* **Tools**: axe-core (contrast), Playwright screenshots, Lighthouse

* **Target**: Zero WCAG contrast failures, ≤ 3 font families, consistent component styling

* **Approach**: Audit → Report with screenshots → Implement fixes → Before/after comparison

### Other Non-Functional Types

* **Compatibility**: Cross-browser (Playwright multi-browser), cross-device (BrowserStack)

* **Resilience**: Chaos engineering, failover, disaster recovery

* **Localization**: Language, currency, date formats

* **Compliance**: GDPR, HIPAA, SOC 2, PCI-DSS

## Testing Architecture Models

Choose based on project type:

| Project Type                   | Model                    | Distribution                            |
| ------------------------------ | ------------------------ | --------------------------------------- |
| Library / package              | **Pyramid**              | Many unit, few integration, minimal E2E |
| Monolithic web app             | **Pyramid or Diamond**   | Balanced unit + integration             |
| Frontend SPA                   | **Trophy**               | Heavy integration + static analysis     |
| Microservices                  | **Diamond or Honeycomb** | Heavy integration                       |
| Full-stack (React + Rust + PG) | **Diamond**              | Integration-heavy, good E2E coverage    |

### Recommended Stack Distribution

For a typical React + Rust + PostgreSQL project:

| Layer                               | Target                                                                           | Automation                  |
| ----------------------------------- | -------------------------------------------------------------------------------- | --------------------------- |
| Static analysis (lint, types, SAST) | 100% of code                                                                     | Fully automated             |
| Unit tests                          | 80%+ business logic                                                              | Fully automated             |
| Integration tests                   | All critical paths                                                               | Fully automated             |
| Component tests                     | Key UI components                                                                | Fully automated             |
| E2E tests (user stories)            | All user story workflows + interaction verification + desired outcome assessment | Fully automated             |
| E2E tests (common)                  | Smoke, errors, responsive, navigation, walkthrough                               | Fully automated             |
| E2E tests (clickable elements)      | Every interactive element mapped to expected outcome, verified through DOM       | Fully automated             |
| E2E tests (exhaustive crawl)        | Every interactive element on every page, including sub-tabs and dropdowns        | Fully automated             |
| Performance                         | Key API endpoints                                                                | Automated in CI             |
| Security                            | All code + deps                                                                  | Automated + periodic manual |
| Accessibility                       | All user-facing pages                                                            | Automated + manual audit    |
| UX quality                          | All user flows                                                                   | Audit + implement           |
| UI visual quality                   | All pages                                                                        | Automated contrast + audit  |

## Quality Gates

| Gate       | When              | Must Pass                                                        |
| ---------- | ----------------- | ---------------------------------------------------------------- |
| Pre-commit | Before push       | Lint, type-check, unit tests                                     |
| PR/MR      | Before merge      | All unit + integration, SAST, coverage threshold                 |
| Staging    | Before production | E2E smoke suite + interaction verification, performance baseline |
| Release    | Before go-live    | Full regression, security scan, accessibility                    |

## CI/CD Pipeline Speed Targets

| Stage             | Duration | Tests                            |
| ----------------- | -------- | -------------------------------- |
| Pre-commit hooks  | <10s     | Format, lint                     |
| Commit stage      | <5min    | Unit tests, type-check, SAST     |
| Integration stage | <15min   | Integration, contract tests      |
| E2E stage         | <30min   | Critical path E2E, accessibility |
| Nightly           | 1-2hr    | Full regression, perf, security  |

## Manual vs. Automated Decision

**Automate**: Regression, unit, integration, smoke, performance, security scans, accessibility scans
**Keep manual**: Exploratory testing, usability, visual/aesthetic review, UAT, accessibility with real users

**Automate when**: Runs >3 times, data-driven, critical path, needs CI/CD
**Keep manual when**: Requires human judgment, run rarely, unstable requirements, exploratory

## Common Failure Modes (Learn From Past Mistakes)

These patterns have caused test suites to pass while catching zero real bugs. They are the #1 reason test-everything runs fail to deliver confidence.

### 1. "Page Loads" Tests

Tests that only verify a page renders content — NOT that features work. Example: `expect(mainText.length).toBeGreaterThan(0)`. These pass even if every feature on the page is completely broken. **Fix**: Test actual features — create, read, update, delete operations with specific assertions.

### 2. Hardcoded Waits (`waitForTimeout`)

Using `waitForTimeout(3000)` hides real timing bugs and makes tests flaky. Tests pass on fast machines, fail on slow CI. **Fix**: Use Playwright's auto-waiting: `toBeVisible()`, `waitForURL()`, `waitForResponse()`.

### 3. Giving Up on Hard Tests (`test.fixme`)

Marking a test as `test.fixme` or `test.skip` to get a green suite hides real coverage gaps. A skipped test is worse than no test — it creates false confidence. **Fix**: Diagnose root cause (race condition? auth state leak? React re-renders?) and fix it.

### 4. Fire-and-Forget Clicks

Clicking a button without asserting the outcome. The click may silently fail, navigate nowhere, or trigger a 500 error. **Fix**: Every `.click()` must be followed by `expect()` or `waitForResponse()` within 3 lines.

### 5. CSS Selectors Instead of Accessible Locators

Using `page.locator('.text-red-400')` or `page.locator('#email')` instead of `page.getByRole()` or `page.getByLabel()`. CSS selectors don't verify accessibility and match non-functional elements. **Fix**: Use `getByRole` > `getByLabel` > `getByText`.

### 6. Premature Completion Claims

Declaring "147 tests passing!" when the tests verify nothing meaningful. **Fix**: Always ask "If every feature broke, would these tests catch it?" before claiming done.

### 7. API-Shortcut Testing (E2E-Specific)

Testing user-facing features via API calls instead of through the rendered UI. The test proves the backend works but says nothing about whether the user can actually interact with the feature.

**Examples of the anti-pattern:**

* File upload tested via `page.request.post('/api/documents/upload', ...)` — the upload API works, but the "Select Files" button is completely broken (hidden input, broken onChange, wrong CSS class)

* Form submission tested via `page.request.post('/api/items', { data })` — the API accepts the request, but the submit button does nothing when clicked

* Navigation tested via `page.goto('/target')` instead of clicking the actual link — the page renders, but the nav link points to `#` or is obscured by another element

**Why it's devastating:** These tests pass with 100% reliability while the feature is completely broken for every real user. The false confidence is worse than having no test at all, because the team sees a green suite and ships.

**Fix:** Use the real UI interaction for every user-facing action. Use API calls only for test setup (auth, data seeding) and backend verification.

**Canonical case:** failure4 — file upload test passed via API for weeks while no user could upload a file through the browser. Took 5 rounds of manual debugging to fix. See `references/e2e-sandbox-patterns.md` for the full story.

### 8. Sandbox Environment Failures (E2E-Specific)

E2E tests that work locally but fail in sandbox environments (Claude Code, CI) due to:

* **Browser cache permission denied** — Playwright tries to use `~/Library/Caches/ms-playwright/` which is blocked. **Fix**: Set `PLAYWRIGHT_BROWSERS_PATH=.playwright-browsers` in all npm scripts.

* **`webServer` timeout** — Playwright's `config.webServer` tries to start dev servers as child processes, which times out because `nice()` fails in sandbox. **Fix**: Remove `webServer` from config entirely. Pre-start servers before running tests and verify they're ready with `curl`.

* **React form fills lost** — `page.fill()` gets swallowed during React hydration re-renders, leaving form fields empty. **Fix**: Register users via API instead of UI forms. Wait for a specific interactive element (`getByRole('button')`) before filling forms. Verify fills with `toHaveValue()`.

* **Auth state bleeding** — localStorage persists between tests in the same context, causing later tests to see stale auth. **Fix**: Use fresh browser contexts (`browser.newContext()`) for tests that need clean auth state.

* **Port mismatches** — Playwright config expects one port, dev server runs on another. **Fix**: Use `process.env.BASE_URL` in config with a sensible default. Verify the port with `curl` before running tests.

* **Strict mode violations** — Playwright finds multiple elements matching a locator. **Fix**: Use `.first()` or scope locators to specific containers (`page.getByRole('list').getByText(...)`)

See `references/e2e-sandbox-patterns.md` for the complete playbook with code examples.

## Additional Resources

### Reference Files

For detailed information on each testing type, tools, and implementation:

* **`references/testing-types-detail.md`** — Complete breakdown of all testing types with examples, tools, and when to use each

* **`references/implementation-roadmap.md`** — Phased 10-week implementation plan with checklists for building comprehensive testing from scratch

* **`references/e2e-sandbox-patterns.md`** — Battle-tested patterns for running Playwright E2E tests reliably in macOS Sandbox (Claude Code): browser installation, server management, API-first auth, React hydration waits, strict mode handling, and debugging guide