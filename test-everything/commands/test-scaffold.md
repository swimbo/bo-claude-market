---
name: test-scaffold
description: Scaffold test files, configurations, and CI pipeline definitions for a specific testing layer
argument-hint: "<layer> [path-to-project] — layers: unit, integration, component, e2e, performance, security, accessibility, ux, ui, ci"
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash"]
---

# Test Scaffolding

Create test infrastructure files for a specific testing layer.

## Instructions

Parse the argument to determine which layer to scaffold. If no layer specified, ask the user.

Valid layers: `unit`, `integration`, `component`, `e2e`, `performance`, `security`, `accessibility`, `ux`, `ui`, `ci`

### Before Scaffolding

1. Detect project type and existing test infrastructure
2. Check what already exists — never overwrite existing test configs
3. Identify the correct tools based on the preferred stack

### Layer: `unit`

**Frontend (React + Vitest)**:

* Create `vitest.config.ts` if missing (jsdom environment, coverage config, path aliases)

* Create `src/test/setup.ts` with Testing Library matchers

* Create example test file `src/lib/__tests__/example.test.ts`

* Add test scripts to `package.json`: `"test"`, `"test:watch"`, `"test:coverage"`

* Install deps if missing: `vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom`

**Backend (Rust)**:

* Add test module template to an existing source file if no tests exist

* Create `tests/` integration test directory if missing

* Add `dev-dependencies` to `Cargo.toml` if missing (tokio test-util, etc.)

### Layer: `integration`

**Frontend**:

* Set up MSW (Mock Service Worker) if not present: `src/mocks/handlers.ts`, `src/mocks/server.ts`

* Create example integration test: `src/components/__tests__/ExamplePage.test.tsx`

* Configure MSW in Vitest setup file

**Backend (Rust + SQLx)**:

* Create test fixtures or factory functions in `tests/common/mod.rs`

* Create example API integration test in `tests/api/`

* Configure test database URL in `.env.test`

### Layer: `component`

Test UI components in isolation with various states, props, and interactions.

**React + Vitest + Testing Library**:

* Create `src/components/__tests__/` directory if not using co-located tests
* For each complex interactive component, create a test file covering:
  * Default rendering — component mounts without errors
  * All visual states — loading, empty, error, success, disabled
  * User interactions — clicks, form input, keyboard navigation, focus management
  * Prop variations — required vs optional props, edge case values
  * Conditional rendering — permission-gated content, responsive breakpoints
* Example structure:
  ```typescript
  // src/components/__tests__/DataTable.test.tsx
  import { render, screen } from '@testing-library/react';
  import userEvent from '@testing-library/user-event';
  import { DataTable } from '../DataTable';

  describe('DataTable', () => {
    it('renders loading skeleton', () => { ... });
    it('renders empty state with message', () => { ... });
    it('renders rows from data', () => { ... });
    it('sorts by column on header click', () => { ... });
    it('paginates when rows exceed page size', () => { ... });
    it('renders error state on fetch failure', () => { ... });
  });
  ```
* Install deps if missing: `@testing-library/react @testing-library/user-event @testing-library/jest-dom`

**Storybook (optional)**:

* Install Storybook if the team wants visual component documentation: `npx storybook@latest init`
* Create stories alongside components: `ComponentName.stories.tsx`
* Configure Storybook test runner for CI: `@storybook/test-runner`

### Layer: `e2e`

**Playwright**:

* Create `playwright.config.ts` with:

  * Multi-browser projects (Chromium, Firefox, WebKit)

  * Base URL from env var

  * Screenshot on failure

  * HTML reporter

  * Reasonable timeouts

* Create `e2e/` directory structure:

  * `e2e/fixtures/` — test data and auth state

* Add scripts to `package.json`: `"test:e2e"`, `"test:e2e:ui"`

* Install: `@playwright/test` + browsers

**Browser Health Monitoring**:

Scaffold a shared Playwright fixture that automatically detects silent failures across all E2E tests. This fixture MUST be created alongside any E2E test files:

* Create `e2e/fixtures/browser-health.ts`:

  ```typescript
  import { test as base, expect } from '@playwright/test';

  // Extend Playwright's base test with automatic browser health monitoring
  export const test = base.extend<{ browserHealth: void }>({
    browserHealth: [async ({ page }, use) => {
      const consoleErrors: string[] = [];
      const failedRequests: string[] = [];

      // Catch uncaught exceptions
      page.on('pageerror', err => {
        consoleErrors.push(`[PageError] ${err.message}`);
      });

      // Catch console.error messages
      page.on('console', msg => {
        if (msg.type() === 'error') {
          consoleErrors.push(`[ConsoleError] ${msg.text()}`);
        }
      });

      // Catch failed network requests
      page.on('requestfailed', req => {
        failedRequests.push(
          `[RequestFailed] ${req.method()} ${req.url()} - ${req.failure()?.errorText}`
        );
      });

      // Catch API error responses (4xx/5xx)
      page.on('response', resp => {
        if (resp.status() >= 400 && resp.url().includes('/api/')) {
          failedRequests.push(
            `[APIError] ${resp.status()} ${resp.request().method()} ${resp.url()}`
          );
        }
      });

      // Run the test
      await use();

      // After each test: assert no silent failures
      expect(consoleErrors, 'Browser console errors detected during test').toEqual([]);
      expect(failedRequests, 'API requests failed during test').toEqual([]);
    }, { auto: true }],
  });

  export { expect } from '@playwright/test';
  ```

* All generated E2E test files should import from this fixture instead of `@playwright/test`:

  ```typescript
  // Use this:
  import { test, expect } from './fixtures/browser-health';
  // NOT this:
  // import { test, expect } from '@playwright/test';
  ```

* For tests that intentionally trigger errors (e.g., error page tests), opt out per-test:

  ```typescript
  test('shows error page on API failure', async ({ page }) => {
    // Temporarily remove listeners for this test
    page.removeAllListeners('pageerror');
    // ... test error handling ...
  });
  ```

**User-Story-Driven Test Generation**:

E2E specs must be derived from user stories, not invented ad-hoc.

**Interaction Verification Rules**:

Every interaction in generated E2E tests MUST be paired with an outcome assertion. A test that clicks a button without verifying the result provides zero confidence. Apply this rule to every `click()`, `fill()`, `check()`, `selectOption()`, and form submission:

* **Navigation verification** — action should change the URL:
  ```typescript
  await page.getByRole('button', { name: 'Submit' }).click();
  await expect(page).toHaveURL(/\/dashboard/);
  ```

* **DOM change verification** — action should change visible content:
  ```typescript
  await page.getByRole('button', { name: 'Save' }).click();
  await expect(page.getByText('Changes saved')).toBeVisible();
  ```

* **Network verification** — action should trigger an API call:
  ```typescript
  const responsePromise = page.waitForResponse(resp =>
    resp.url().includes('/api/items') && resp.status() === 200
  );
  await page.getByRole('button', { name: 'Load More' }).click();
  await responsePromise;
  ```

* **State verification** — action should change element state:
  ```typescript
  await page.getByRole('checkbox', { name: 'Accept terms' }).check();
  await expect(page.getByRole('button', { name: 'Continue' })).toBeEnabled();
  ```

If a test step cannot verify an outcome with at least one of these patterns, the test step is incomplete and must be revised.

**User-Story-Driven Test Spec Generation**:

1. **Check for** **`docs/planning/user-stories.md`** in the project root
2. **If found**:

   * Parse each user story (`US-XXX`) with its workflow steps and acceptance criteria

   * Create one spec file per story: `e2e/user-story-<slug>.spec.ts`

   * Each spec tests the full workflow step-by-step, with every action paired to an outcome assertion

   * Import `test` and `expect` from `./fixtures/browser-health` (not `@playwright/test`)

   * **Selector Strategy**: Use accessible selectors to verify elements are properly functional, not just present in the DOM:

     1. `page.getByRole('button', { name: '...' })` — buttons, links, headings, checkboxes (preferred)
     2. `page.getByLabel('...')` — form inputs with labels
     3. `page.getByText('...')` — visible text content
     4. `page.getByTestId('...')` — last resort only, when no accessible name exists

     Why: `getByRole('button', { name: 'Submit' })` verifies the element is an actual button with the correct accessible name. A `<div>` styled to look like a button will NOT match `getByRole('button')` — catching a real bug that CSS selectors would miss.

   * Example structure:

     ```typescript
     // e2e/user-story-registration.spec.ts
     import { test, expect } from './fixtures/browser-health';

     test.describe('US-001: User Registration', () => {
       test('Step 1: Navigate to registration page', async ({ page }) => {
         await page.goto('/');
         await page.getByRole('link', { name: 'Sign Up' }).click();
         await expect(page).toHaveURL(/\/register/);  // verify navigation
       });

       test('Step 2: Fill in registration form', async ({ page }) => {
         await page.goto('/register');
         await page.getByLabel('Email').fill('user@example.com');
         await page.getByLabel('Password').fill('SecurePass123!');
         await page.getByLabel('Confirm Password').fill('SecurePass123!');
         // verify form is valid and submit is enabled
         await expect(page.getByRole('button', { name: 'Create Account' })).toBeEnabled();
       });

       test('Step 3: Submit and see confirmation', async ({ page }) => {
         // ... fill form ...
         const responsePromise = page.waitForResponse(resp =>
           resp.url().includes('/api/') && resp.status() < 400
         );
         await page.getByRole('button', { name: 'Create Account' }).click();
         await responsePromise;  // verify API call succeeded
         await expect(page.getByText('Check your email')).toBeVisible();  // verify UI feedback
       });
     });
     ```
3. **If NOT found**:

   * Analyze the codebase to infer user stories:

     * Scan routes/pages for user-facing features

     * Read API endpoints for data flows

     * Identify auth boundaries, forms, and interactive components

   * Generate `docs/planning/user-stories.md` with inferred stories

   * Present to the user for approval before creating specs

   * After approval, create specs as described above
4. After scaffolding, output a coverage matrix showing which user stories have specs

**Common E2E Tests**:

In addition to user-story specs, scaffold these cross-cutting E2E tests that aren't tied to any single story:

* `e2e/smoke.spec.ts` — Quick post-deployment sanity checks:
  * Homepage loads successfully
  * Login/auth flow works
  * Main navigation links resolve
  * API health endpoint responds
* `e2e/error-pages.spec.ts` — Error handling:
  * 404 page renders for unknown routes
  * Unauthorized redirect for protected routes
  * Graceful handling of API errors (500, timeout)
  * Empty states render correctly (no data scenarios)
* `e2e/responsive.spec.ts` — Viewport/responsive tests:
  * Mobile viewport (375px) — navigation collapses, layout adapts
  * Tablet viewport (768px) — intermediate layout
  * Desktop viewport (1280px) — full layout
  * Test critical pages at each breakpoint
* `e2e/navigation.spec.ts` — Routing and navigation:
  * Deep links load correctly (direct URL access)
  * Browser back/forward works after navigation
  * Redirects work (e.g., `/` → `/dashboard` when authenticated)
  * Query parameters and URL state preserved
* `e2e/visual-regression.spec.ts` (optional) — Visual regression testing:
  * Capture screenshots at key workflow completion points (not just static pages)
  * Use `expect(page).toHaveScreenshot('descriptive-name.png')` with meaningful names
  * Focus on top 3-5 critical page states — not every page
  * Include interaction before screenshot (e.g., complete a workflow, then screenshot the result)
  * Only scaffold if user opts in (baselines require maintenance)
  * Template:

    ```typescript
    import { test, expect } from './fixtures/browser-health';

    test.describe('Visual Regression', () => {
      test('dashboard after login', async ({ page }) => {
        await page.goto('/login');
        await page.getByLabel('Email').fill('test@example.com');
        await page.getByLabel('Password').fill('password123');
        await page.getByRole('button', { name: 'Sign In' }).click();
        await expect(page).toHaveURL(/\/dashboard/);
        // Screenshot AFTER interaction, not just page load
        await expect(page).toHaveScreenshot('dashboard-logged-in.png');
      });

      test('settings page', async ({ page }) => {
        // ... navigate and interact ...
        await expect(page).toHaveScreenshot('settings-page.png');
      });
    });
    ```

  * To update baselines: `npx playwright test --update-snapshots`
  * Note: baselines are OS-dependent — generate in the same environment as CI

**Post-Suite Walkthrough**:

Scaffold a single end-to-end walkthrough test that chains the top user story workflows into one continuous session. This catches cross-flow bugs that isolated tests miss (state pollution, navigation issues after certain actions, auth session problems):

* Create `e2e/walkthrough.spec.ts`:

  ```typescript
  import { test, expect } from './fixtures/browser-health';

  test('complete user session walkthrough', async ({ page }) => {
    // This test chains the top 3-5 user stories into a single
    // continuous session WITHOUT page reloads between flows.
    // It catches bugs that only appear when flows interact.

    // --- Flow 1: Login ---
    await page.goto('/login');
    await page.getByLabel('Email').fill('test@example.com');
    await page.getByLabel('Password').fill('password123');
    await page.getByRole('button', { name: 'Sign In' }).click();
    await expect(page).toHaveURL(/\/dashboard/);

    // --- Flow 2: Core workflow (adapt to project) ---
    // Navigate from dashboard to main feature
    await page.getByRole('link', { name: 'Projects' }).click();
    await expect(page).toHaveURL(/\/projects/);
    // Create something
    await page.getByRole('button', { name: 'New Project' }).click();
    await page.getByLabel('Project Name').fill('Walkthrough Test');
    await page.getByRole('button', { name: 'Create' }).click();
    await expect(page.getByText('Walkthrough Test')).toBeVisible();

    // --- Flow 3: Settings / profile ---
    await page.getByRole('link', { name: 'Settings' }).click();
    await expect(page).toHaveURL(/\/settings/);
    // Verify settings page loads with user data
    await expect(page.getByLabel('Email')).toHaveValue('test@example.com');

    // --- Flow 4: Logout ---
    await page.getByRole('button', { name: 'Sign Out' }).click();
    await expect(page).toHaveURL(/\/login/);

    // Browser health fixture checks for console errors
    // and failed network requests across the entire session
  });
  ```

* This test should run AFTER all individual E2E tests pass
* Derive the walkthrough steps from the top 3-5 user stories in `docs/planning/user-stories.md`
* Do NOT use separate `test()` blocks — maintain session state in one continuous test
* Add script: `"test:e2e:walkthrough": "playwright test walkthrough.spec.ts"`

### Layer: `performance`

**k6**:

* Create `k6/` directory

* Create `k6/load-test.js` — basic load test template with stages and thresholds

* Create `k6/smoke-test.js` — quick smoke test for post-deployment

* Create `k6/stress-test.js` — stress test finding breaking points

* Include common thresholds: p95 < 500ms, error rate < 1%

* Add npm script: `"test:perf"`

### Layer: `security`

* Create `.semgrep.yml` or `semgrepconfig` with recommended rules

* Add `cargo audit` step to CI if Rust project

* Add `npm audit` / Snyk check to CI

* Create `.github/dependabot.yml` if using GitHub

* Add secret scanning config if available

### Layer: `accessibility`

* Install `@axe-core/playwright` if Playwright exists

* Create `e2e/accessibility.spec.ts` with axe-core integration

* Add Lighthouse CI config (`lighthouserc.json`) for CI scoring

* Create example accessibility test for homepage

### Layer: `ux`

Audit and improve the application's User Experience against established heuristics and cognitive frameworks. This layer does NOT generate test files — it produces an audit report with prioritized improvements and then implements fixes.

**Phase 1: Automated UX Audit**

Use Playwright to crawl the running application and evaluate against these frameworks:

1. **Nielsen's 10 Usability Heuristics** — For each, score the app 1-5:

   | Heuristic | What to Check |
   |-----------|--------------|
   | Visibility of system status | Loading indicators, progress bars, submission confirmations. Does the app go silent during async operations? |
   | Match system and real world | Jargon-free labels, familiar icons, logical menu ordering. Are technical terms exposed to non-technical users? |
   | User control and freedom | Undo/redo support, cancel buttons, back navigation. Can users escape from any state without data loss? |
   | Consistency and standards | Same styling for same actions across all pages. Are warning colors consistent? Are button positions predictable? |
   | Error prevention | Confirmation dialogs for destructive actions, input constraints, dry-run options. Can users accidentally delete data? |
   | Recognition over recall | Autocomplete, recent items, contextual hints. Are users forced to memorize values from previous screens? |
   | Flexibility and efficiency | Keyboard shortcuts, power-user features, customizable workflows. Is the app equally efficient for novice and expert? |
   | Aesthetic and minimalist design | Information density, whitespace usage, visual noise. Does irrelevant content compete with primary tasks? |
   | Help users recover from errors | Error message quality (plain language + resolution steps). Are errors actionable or cryptic? |
   | Help and documentation | Searchable docs, contextual tooltips, onboarding. Can a new user complete core tasks without external guidance? |

2. **Dark Pattern Detection** — Scan for manipulative UI patterns:

   * Trick questions (confusing double negatives in settings/checkboxes)
   * Hidden costs (dependencies or requirements revealed late in workflows)
   * Forced continuity (difficult-to-find cancellation or opt-out paths)
   * Confirmshaming (guilt-tripping language on decline buttons)
   * Misdirection (visual hierarchy that draws attention away from user-beneficial options)
   * Bad defaults (settings that optimize for data collection over user privacy/safety)
   * Roach motel (easy to start, hard to exit — check account deletion, subscription management)

3. **Feedback Loop Quality** — Evaluate interactive responsiveness:

   * Every button click produces visible feedback within 100ms
   * Form submissions show loading state, then success/error
   * Long-running operations display progress (not just a spinner)
   * Error states provide recovery paths (not dead ends)
   * Success states confirm what happened (not just "Done")

4. **CLI/Terminal UX** (if applicable):

   * Help available via `--help`, `-h`, and `help` subcommand
   * Consistent command structure: `tool [noun] [verb] [flags]`
   * Flags preferred over positional arguments (self-documenting)
   * `stdout` for data, `stderr` for messages/progress (pipeable output)
   * Error messages include: error code, description, resolution steps, docs URL
   * Non-destructive by default (require `--force` for dangerous operations)

**Phase 2: Audit Report**

Output a structured report:

```
## UX Audit Report

### Heuristic Scores
| Heuristic | Score (1-5) | Key Finding | Priority |
|-----------|------------|-------------|----------|
| Visibility of system status | 3 | No loading indicator on data fetch | High |
| Error prevention | 2 | Delete button has no confirmation | Critical |
| ... | ... | ... | ... |

### Dark Patterns Found
- [None found / List each with severity]

### Feedback Loop Issues
1. [Page]: [Element] — no feedback after click
2. [Page]: [Form] — no loading state on submit

### Top 5 UX Improvements (Prioritized)
1. [Highest impact fix with specific implementation guidance]
2. ...
```

**Phase 3: Implement Improvements**

After presenting the audit, implement the top prioritized improvements:

* Add missing loading states and progress indicators
* Add confirmation dialogs for destructive actions
* Improve error messages (plain language + resolution steps)
* Fix feedback gaps (buttons that produce no visible response)
* Remove or fix any detected dark patterns
* Add keyboard shortcuts for common actions
* Improve form validation (inline, real-time, not just on submit)

Use the browser health fixture from the e2e layer to verify improvements don't introduce console errors.

### Layer: `ui`

Audit and improve the application's visual User Interface against strict design principles. This layer evaluates the pixel-level visual quality — typography, color, spacing, consistency, and accessibility of the rendered UI — then implements fixes.

**Phase 1: Automated UI Audit**

Use Playwright to screenshot and analyze each page/route, evaluating against these criteria:

1. **Color & Contrast Compliance** — WCAG 2.2 standards:

   | Check | Standard | How to Verify |
   |-------|----------|--------------|
   | Body text contrast | ≥ 4.5:1 ratio | Use axe-core or Lighthouse to check all text elements |
   | Large text contrast (≥18pt or 14pt bold) | ≥ 3.0:1 ratio | Check headings, buttons, nav items |
   | Non-text contrast (icons, borders, focus rings) | ≥ 3.0:1 ratio | Check interactive element boundaries |
   | Color not sole indicator | N/A | Error states must use icon + text + color (not just red) |
   | Dark/light theme parity | Same ratios in both themes | Run audit in both themes if available |

   Use `@axe-core/playwright` for automated contrast checking. Flag every failure with the specific element, current ratio, and required ratio.

2. **Typography Audit**:

   * Count distinct font families in use — flag if more than 3
   * Check for consistent heading hierarchy (h1 > h2 > h3, no skipped levels)
   * Verify monospaced font used for code elements
   * Check line height (body: 1.4-1.6, code: 1.3-1.5)
   * Check max line length (prose: 60-80 characters, code: 80-120)
   * Flag excessively small text (< 12px body, < 11px labels)
   * Verify font loading fallbacks (no FOUT/FOIT flashes)

3. **Spacing & Layout Consistency**:

   * Check for consistent spacing scale (e.g., 4px/8px grid system)
   * Verify alignment — elements within groups should share a common edge
   * Check padding consistency on similar components (all cards have same padding)
   * Verify responsive behavior at mobile (375px), tablet (768px), desktop (1280px)
   * Flag horizontal scrolling on any viewport
   * Check whitespace between sections (adequate breathing room)

4. **Component Visual Consistency**:

   * All buttons of same type share identical styling (border-radius, padding, font-size)
   * All form inputs share identical styling (height, border, focus ring)
   * Consistent icon sizing and weight throughout
   * Hover/focus/active/disabled states defined for all interactive elements
   * No "Frankenstein layouts" — components from different design systems mixed inconsistently

5. **Visual Hierarchy & Gestalt Principles**:

   * Primary CTA is visually dominant on each page (largest, most contrasted)
   * Related elements are grouped with proximity (tight spacing)
   * Unrelated sections are separated with whitespace or borders
   * Reading flow follows predictable F-pattern or Z-pattern
   * No competing visual elements fighting for attention at the same level

6. **Semantic Color Usage**:

   * Red/destructive styling used ONLY for destructive actions and errors
   * Green/success styling used ONLY for success states and confirmations
   * Yellow/warning styling used ONLY for warnings and caution states
   * Primary brand color used consistently for primary actions
   * Neutral colors used for secondary UI elements and borders

**Phase 2: Visual Audit Report**

Output a structured report with screenshots:

```
## UI Visual Audit Report

### Color & Contrast
| Element | Page | Current Ratio | Required | Status |
|---------|------|--------------|----------|--------|
| Body text | /dashboard | 3.2:1 | 4.5:1 | ❌ FAIL |
| Button text | /settings | 5.1:1 | 4.5:1 | ✅ PASS |

### Typography
- Font families in use: N (target: ≤ 3)
- Heading hierarchy: [correct / broken at X]
- Minimum text size: Npx [OK / too small]

### Spacing Consistency
- Grid system detected: [yes (Npx) / no / inconsistent]
- Inconsistent padding: [list of components]

### Component Consistency
- Button variants: N styles found (target: 3-4 max)
- Input variants: N styles found (target: 1-2 max)
- Missing states: [list of components missing hover/focus/disabled]

### Visual Hierarchy Issues
1. [Page]: [description of hierarchy problem]
2. ...

### Top 5 UI Improvements (Prioritized)
1. [Fix contrast failures — affects accessibility compliance]
2. [Standardize button styling — N variants → 3]
3. ...
```

**Phase 3: Implement Improvements**

After presenting the audit, implement the top prioritized improvements:

* Fix all contrast ratio failures (adjust text color, background, or both)
* Standardize component styling (consolidate button/input variants)
* Fix typography hierarchy (correct heading levels, consistent sizing)
* Add missing interactive states (hover, focus, active, disabled)
* Normalize spacing to a consistent grid (4px or 8px increments)
* Fix visual hierarchy (make primary CTAs dominant, separate sections)
* Fix semantic color misuse (red only for errors/destructive, etc.)
* Add focus-visible rings for keyboard navigation

Take before/after screenshots using `expect(page).toHaveScreenshot()` to verify visual improvements.

### Layer: `ci`

Generate CI pipeline configuration:

**GitHub Actions** (`.github/workflows/test.yml`):

```yaml
# Full testing pipeline with stages:
# 1. Lint + typecheck + SAST (<5 min)
# 2. Unit + integration tests (<15 min)
# 3. E2E tests (<30 min)
# 4. Security + performance (nightly)
```

**GitLab CI** (`.gitlab-ci.yml`):

```yaml
# Equivalent stages for GitLab
```

Detect which CI system the project uses (look for `.github/`, `.gitlab-ci.yml`, `Jenkinsfile`) and generate the appropriate config.

### After Scaffolding

1. List all files created
2. Show next steps (what to customize, what to run first)
3. Note any manual steps needed (e.g., "Add test database URL to .env.test")

### Tips

* Always check existing files first — append to configs, don't overwrite

* Use the project's existing code style and patterns

* Include helpful comments in generated files explaining what each section does

* Reference the test-strategy skill for deeper context on any testing type