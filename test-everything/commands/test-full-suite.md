---
name: test-full-suite
description: Full testing workflow — audit gaps, plan strategy, scaffold infrastructure, write tests, run them, and fix until everything passes
argument-hint: "[path-to-project]"
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "Agent"]
---

# Test Everything

End-to-end testing workflow: audit, plan, build, run, fix, repeat until green.

## Instructions

Execute the full testing lifecycle for the project at the given path (or cwd).

### Phase 1: Audit

Perform the same analysis as `/test-everything:test-audit`:

1. Detect project type, languages, frameworks
2. Inventory existing tests and configs
3. Assess each testing layer (unit, integration, component, E2E, performance, security, accessibility)
4. Assess E2E coverage against user stories (check for `docs/planning/user-stories.md` — see test-audit Step 3b)
5. Identify gaps — output a brief summary table (not the full report)

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
3. Write real, meaningful tests — not just boilerplate:

   * Read the source code being tested

   * Write tests that exercise actual behavior, edge cases, and error paths

   * Follow existing project patterns and conventions

   * Co-locate tests with source when that's the project convention
4. Use parallel subagents for independent test files when possible

#### Component Tests (Frontend)

For projects with a frontend, write component tests for complex interactive UI components:

1. Identify components with significant logic: forms, data tables, modals, interactive widgets, permission-gated views
2. Test each component in isolation covering: all visual states (loading, empty, error, success), user interactions (clicks, input, keyboard), prop variations, and conditional rendering
3. Use React Testing Library + Vitest — test behavior, not implementation details
4. Skip simple presentational components that are just markup wrappers

#### User-Story-Driven E2E Tests

E2E tests MUST be derived from user story workflows and MUST use interaction verification.

**Before writing any E2E tests:**
1. Scaffold the browser health fixture (`e2e/fixtures/browser-health.ts`) — see test-scaffold for the template
2. All generated E2E tests must import `test` and `expect` from `./fixtures/browser-health`, not from `@playwright/test`

**Interaction verification rule:** Every interaction (`click()`, `fill()`, `check()`, `selectOption()`, form submission) MUST be followed by at least one assertion verifying the outcome — a URL change, DOM change, network response, or element state change. A test that clicks without verifying is incomplete.

**Generate E2E specs:**

1. **Check for user stories**: Look for `docs/planning/user-stories.md` in the project root
2. **If the file exists**:
   * Parse every user story and its acceptance criteria / workflow steps
   * Create one E2E spec file per user story (e.g., `e2e/user-story-registration.spec.ts`)
   * Each spec must test every step in the user story workflow, in sequence
   * Map acceptance criteria directly to test assertions
   * **Every workflow step must pair the user action with an outcome assertion** — not just perform the action
   * Group related stories into describe blocks by feature area
3. **If the file does NOT exist**:
   * Analyze the codebase to infer user story workflows:
     - Scan routes/pages to identify user-facing features
     - Read API endpoints to understand data flows
     - Examine navigation, forms, and interactive components
     - Identify authentication/authorization boundaries
   * Generate a `docs/planning/user-stories.md` file documenting the inferred stories using this format:
     ```
     ## US-001: [Story Title]
     **As a** [role], **I want to** [action], **so that** [benefit].

     ### Workflow Steps
     1. [Step 1 — specific user action]
     2. [Step 2 — expected system response]
     3. [Step 3 — next user action]
     ...

     ### Acceptance Criteria
     - [ ] [Criterion 1]
     - [ ] [Criterion 2]
     ```
   * Present the inferred user stories to the user for approval before writing E2E tests
   * After approval, create E2E specs covering each story's workflow steps
4. **Coverage mapping**: After writing E2E tests, output a traceability matrix:
   ```
   | User Story | E2E Spec File | Steps Covered | Status |
   |------------|---------------|---------------|--------|
   | US-001     | e2e/...       | 5/5           | Full   |
   | US-002     | e2e/...       | 3/4           | Partial|
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

### Phase 5: Quality Review

After all tests pass, review the test suite for quality issues (same checks as the test-quality-reviewer agent):

1. **Anti-patterns**: Scan new test files for tests with no assertions, snapshot-only tests, excessive mocking, implementation-detail testing, tautological assertions, commented-out tests
2. **Flakiness risks**: Check for hardcoded timeouts, shared mutable state, system time dependencies, missing `await` in async tests, network calls without mocking in unit tests
3. **Architecture alignment**: Verify test distribution matches the recommended model (Pyramid/Diamond/Trophy) — flag if too many E2E tests relative to unit tests or if integration layer has gaps
4. Fix any issues found before proceeding to summary

### Phase 6: Summary

Once everything is green and quality-reviewed, output:

```
## Test Everything — Complete

### Tests Added
- [list of new test files with test counts]

### Infrastructure Created
- [configs, CI files, setup files]
- Browser health fixture: e2e/fixtures/browser-health.ts

### User Story Coverage
| User Story | E2E Spec File | Steps Covered | Status |
|------------|---------------|---------------|--------|
| US-001     | e2e/...       | 5/5           | Full   |
| ...        | ...           | ...           | ...    |

### Interaction Verification
| Check | Result | Status |
|-------|--------|--------|
| Action-outcome pairing | X of Y interactions verified (Z%) | ✅/⚠️/❌ |
| Selector quality | X% accessible locators | ✅/⚠️/❌ |
| Browser health monitoring | Active | ✅ |

### Interaction Coverage
| Page/Route | Interactive Elements | Tested | Coverage |
|------------|---------------------|--------|----------|
| /dashboard | N                   | N      | N%       |
| /settings  | N                   | N      | N%       |

Untested elements:
- [page]: [list of untested buttons, links, forms by accessible name]

Note: Generate this report by using Playwright to visit each route after E2E tests
complete, query for all interactive elements (button, a[href], input, select,
textarea, [role="button"]), and cross-reference against elements the tests
actually interacted with. This report is informational — it does not fail the suite.

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
```

### Guidelines

* Never skip Phase 2 approval — the user must confirm the plan before you write code

* Write tests that would actually catch regressions, not just tests that pass

* If fixing a test failure requires changing source code, explain what the bug is before fixing

* Prefer fixing source code bugs over weakening test assertions

* Use the test-strategy skill for guidance on any testing type

* Don't install tools outside the project's preferred stack without asking