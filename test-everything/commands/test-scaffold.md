---
name: test-scaffold
description: Scaffold test files, configurations, and CI pipeline definitions for a specific testing layer
argument-hint: "<layer> [path-to-project] — layers: unit, integration, component, e2e, performance, security, accessibility, ci"
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash"]
---

# Test Scaffolding

Create test infrastructure files for a specific testing layer.

## Instructions

Parse the argument to determine which layer to scaffold. If no layer specified, ask the user.

Valid layers: `unit`, `integration`, `component`, `e2e`, `performance`, `security`, `accessibility`, `ci`

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

**User-Story-Driven Test Generation**:

E2E specs must be derived from user stories, not invented ad-hoc:

1. **Check for** **`docs/planning/user-stories.md`** in the project root
2. **If found**:

   * Parse each user story (`US-XXX`) with its workflow steps and acceptance criteria

   * Create one spec file per story: `e2e/user-story-<slug>.spec.ts`

   * Each spec tests the full workflow step-by-step, with assertions matching acceptance criteria

   * Example structure:

     ```typescript
     // e2e/user-story-registration.spec.ts
     import { test, expect } from '@playwright/test';

     test.describe('US-001: User Registration', () => {
       test('Step 1: Navigate to registration page', async ({ page }) => { ... });
       test('Step 2: Fill in registration form', async ({ page }) => { ... });
       test('Step 3: Submit and see confirmation', async ({ page }) => { ... });
       test('Acceptance: Email verification sent', async ({ page }) => { ... });
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
* `e2e/visual-regression.spec.ts` (optional) — Screenshot comparison:
  * Capture baseline screenshots of key pages
  * Use `expect(page).toHaveScreenshot()` for visual diff
  * Only scaffold if user opts in (can be noisy)

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