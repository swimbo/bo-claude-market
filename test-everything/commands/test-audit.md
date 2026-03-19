---
name: test-audit
description: Analyze a project's current test coverage and identify gaps against comprehensive testing best practices
argument-hint: "[path-to-project]"
allowed-tools: ["Read", "Glob", "Grep", "Bash", "Agent"]
---

# Test Coverage Audit

Perform a comprehensive audit of the project's testing infrastructure and identify gaps against best practices.

## Instructions

Analyze the project at the given path (or current working directory if none provided) and produce a gap analysis report.

### Step 1: Detect Project Type

Scan the project to determine:

* **Languages**: Look for `package.json` (JS/TS), `Cargo.toml` (Rust), `pyproject.toml` / `requirements.txt` (Python), `go.mod` (Go)

* **Frameworks**: React, Vue, Angular, Axum, Express, Django, etc.

* **Project type**: SPA, API service, full-stack, library, monorepo

* **Recommended testing model**: Pyramid (library), Diamond (full-stack/microservices), Trophy (frontend SPA)

### Step 2: Inventory Existing Tests

Search for test files and configurations:

**Test files** (use Glob):

* `**/*.test.{ts,tsx,js,jsx}`, `**/*.spec.{ts,tsx,js,jsx}` — JS/TS unit/integration

* `**/tests/**/*.rs`, `**/*_test.rs` — Rust tests

* `**/test_*.py`, `**/*_test.py` — Python tests

* `**/*.test.go`, `**/*_test.go` — Go tests

* `**/e2e/**`, `**/playwright/**`, `**/cypress/**` — E2E tests

* `**/__tests__/**` — Test directories

* `**/k6/**`, `**/load-test*`, `**/perf*` — Performance tests

**Test configurations** (use Glob):

* `vitest.config.*`, `jest.config.*` — Unit test runners

* `playwright.config.*`, `cypress.config.*` — E2E frameworks

* `.eslintrc*`, `clippy.toml`, `rustfmt.toml` — Static analysis

* `.github/workflows/*`, `.gitlab-ci.yml`, `Jenkinsfile` — CI/CD pipelines

* `sonar-project.properties`, `.semgrep*` — Security scanning

* `k6/*.js`, `locust*.py` — Performance testing

**Coverage reports** (use Glob):

* `coverage/`, `htmlcov/`, `tarpaulin-report*`

### Step 3: Assess Each Testing Layer

For each layer, determine status: Present, Partial, or Missing.

| Layer                   | What to Look For                                              |
| ----------------------- | ------------------------------------------------------------- |
| **Static analysis**     | Linter configs, type checking, SAST tools in CI               |
| **Unit tests**          | Test files co-located or in test dirs, test runner config     |
| **Integration tests**   | Tests touching DB/API/services, test database setup           |
| **Component tests**     | Testing Library usage, Storybook tests                        |
| **E2E tests**           | Playwright/Cypress config and test files; user story coverage |
| **Performance tests**   | k6/Locust/JMeter scripts, perf benchmarks                     |
| **Security scanning**   | SAST in CI, dependency scanning, secret scanning              |
| **Accessibility tests** | axe-core usage, Lighthouse CI, a11y test files                |
| **UX quality**          | Feedback loops, error messages, confirmations, dark patterns  |
| **UI visual quality**   | Color contrast, typography, spacing, component consistency    |
| **CI/CD integration**   | Tests in pipeline configs, quality gates defined              |

### Step 3b: Assess E2E Coverage Against User Stories

Evaluate whether E2E tests cover actual user workflows:

1. **Check for** **`docs/planning/user-stories.md`** in the project root
2. **If found**:

   * Parse each user story and its workflow steps

   * For each story, check if a corresponding E2E spec exists

   * Determine how many workflow steps are covered by test assertions

   * Check if **desired outcomes** are defined for each story

   * Check if desired outcomes have corresponding assessment tests

   * Report coverage per story:

     ```
     | User Story | E2E Spec | Steps Covered | Outcomes Defined | Outcomes Assessed | Status |
     |------------|----------|---------------|------------------|-------------------|--------|
     | US-001     | e2e/...  | 5/5           | 3                | 3/3 ✅            | Full   |
     | US-002     | —        | 0/4           | 0                | —                 | Missing|
     | US-003     | e2e/...  | 3/3           | 2                | 0/2 ❌            | Partial|
     ```
3. **If NOT found**:

   * Note the absence in the gap report: "No user stories document found — E2E tests may not cover real user workflows"

   * Recommend creating `docs/planning/user-stories.md` with desired outcomes to drive E2E test coverage

   * If E2E tests exist, check whether they appear to cover coherent workflows or just isolated page checks

### Step 3b2: Assess E2E Infrastructure for Sandbox Safety

Check if the E2E test infrastructure will work reliably in sandbox environments (Claude Code). These are the most common causes of E2E test failure — not test bugs, but environment bugs.

```bash
# Check 1: PLAYWRIGHT_BROWSERS_PATH in npm scripts
grep -n 'PLAYWRIGHT_BROWSERS_PATH' package.json
# If missing from test:e2e scripts → CRITICAL: browsers won't be found in sandbox

# Check 2: webServer block in Playwright config (MUST NOT EXIST)
grep -n 'webServer' playwright.config.* 2>/dev/null
# If found → CRITICAL: will timeout in sandbox because nice() fails

# Check 3: UI-based registration in test helpers
grep -rn 'page.goto.*register\|page.fill.*password' e2e/ --include='*.ts' --include='*.js'
# If test helpers register users through UI → HIGH: page.fill() gets lost during React re-renders

# Check 4: Timeout configuration
grep -n 'timeout' playwright.config.* 2>/dev/null
# If default (30000) or missing → MEDIUM: sandbox is slower, needs 60000
```

Report:
```
### E2E Sandbox Safety
| Check | Result | Status |
|-------|--------|--------|
| PLAYWRIGHT_BROWSERS_PATH in npm scripts | Set / Missing | ✅/❌ |
| No webServer in playwright.config | Absent / Present | ✅/❌ |
| API-first auth (not UI-based registration) | Yes / No | ✅/⚠️ |
| Timeout ≥ 60000 | Yes / No | ✅/⚠️ |
```

**CRITICAL**: If `PLAYWRIGHT_BROWSERS_PATH` is missing or `webServer` is present, E2E tests WILL fail 100% of the time in sandbox. Flag these as highest priority.

### Step 3c: Assess Test Quality and Interaction Verification

Evaluate whether existing tests actually verify features work, or just verify pages load. This is the most common failure mode — a test suite with many tests that all pass but catch zero real bugs.

**Step 3c-i: Shallow Test Detection (CRITICAL)**

Grep existing test files for these patterns that indicate tests prove nothing:

```bash
# Vague assertions — assert "something exists" instead of "the right thing exists"
grep -rn 'toBeGreaterThan(0)' e2e/ tests/ --include='*.spec.*' --include='*.test.*'
grep -rn 'toBeTruthy()' e2e/ --include='*.spec.*'
grep -rn 'textContent()' e2e/ --include='*.spec.*'

# Hardcoded waits — hide real timing issues
grep -rn 'waitForTimeout' e2e/ tests/ --include='*.spec.*' --include='*.test.*'

# Skipped tests — hidden coverage gaps
grep -rn 'test\.fixme\|test\.skip\|test\.todo' e2e/ tests/ --include='*.spec.*' --include='*.test.*'

# CSS selectors in interactions
grep -rn "locator('\.\|locator('#" e2e/ --include='*.spec.*'
```

For each E2E test file, answer: "If the feature this test covers broke completely, would this test fail?" If the answer is no, flag it as a shallow test.

Report:

```
### Shallow Test Detection
| Check | Count | Status |
|-------|-------|--------|
| "Page loads" tests (no feature verification) | N | ❌ if >0 |
| Hardcoded waits (waitForTimeout) | N | ❌ if >0 |
| Skipped tests (fixme/skip/todo) | N | ❌ if >0 |
| CSS/ID selectors in interactions | N | ❌ if >0 |
| Vague assertions (toBeGreaterThan(0), toBeTruthy on content) | N | ⚠️ if >0 |
```

**Step 3c-ii: Interaction Verification Quality**

Evaluate whether E2E tests actually verify that interactions produce expected outcomes:

1. **Action-outcome pairing**: Check if interactions are followed by assertions

   * Grep E2E test files for `\.click(` and `\.fill(` calls

   * For each interaction, check if the next meaningful line contains `expect(`, `waitFor(`, or `waitForResponse(`

   * Count: verified interactions vs. fire-and-forget interactions

   * Report: "X of Y interactions (Z%) have outcome assertions"

2. **Selector quality**: Check if tests use accessible selectors

   * Count usage of accessible locators: `getByRole`, `getByLabel`, `getByText`, `getByPlaceholder` (good)

   * Count usage of CSS/attribute selectors: `.click('[data-testid=`, `.click('.`, `.click('#`, `.fill('[name=` (poor)

   * Report: "X% of selectors use accessible locators"

3. **Browser health monitoring**: Check if silent failures are being caught

   * Look for `pageerror` listener in test fixtures or setup files

   * Look for `requestfailed` listener

   * Look for console error monitoring

   * Report: "Browser health monitoring: Present / Absent"

4. Include findings in the gap report:

```
### Interaction Verification
| Check | Result | Status |
|-------|--------|--------|
| Action-outcome pairing | X of Y interactions verified (Z%) | ✅/⚠️/❌ |
| Selector quality | X% accessible locators | ✅/⚠️/❌ |
| Browser health monitoring | Present/Absent | ✅/❌ |
```

Thresholds: ✅ >80%, ⚠️ 50-80%, ❌ <50% for pairing and selectors.

### Step 3d: Assess Exhaustive Interaction Coverage

Evaluate whether the test suite covers ALL interactive elements across all pages, not just those in user story workflows:

1. **Check for exhaustive interaction tests**: Look for `e2e/exhaustive-interactions.spec.ts` or similar files that crawl pages and test all interactive elements
2. **If found**:

   * Check which routes are included in the crawl list

   * Verify the test reveals hidden elements (tabs, accordions, dropdowns) before testing

   * Verify the test covers buttons, links, inputs, checkboxes, and dropdown menus

   * Report: "Exhaustive crawl covers N of M routes"
3. **If NOT found**:

   * Note the absence: "No exhaustive interaction tests — elements not covered by user stories may be untested (dead buttons, broken links behind sub-tabs, non-functional dropdown items)"

   * Recommend scaffolding `e2e/exhaustive-interactions.spec.ts` to cover all interactive elements
4. **Cross-reference with user-story tests**:

   * Estimate how many interactive elements exist across all pages (use Playwright to query `button, a[href], input, select, textarea, [role="button"], [role="checkbox"], [role="switch"]`)

   * Estimate how many are covered by user-story E2E tests

   * Report: "Estimated N interactive elements across M routes; user-story tests cover approximately X%"

   * Flag pages with zero E2E coverage (no user story touches them)

Include in the gap report:

```
### Exhaustive Interaction Coverage
| Check | Result | Status |
|-------|--------|--------|
| Exhaustive crawl test exists | Yes/No | ✅/❌ |
| Routes covered by crawl | N of M | ✅/⚠️/❌ |
| Hidden element discovery | Tabs, accordions, dropdowns tested | ✅/❌ |
| Pages with zero E2E coverage | [list] | ⚠️ |
```

### Step 3e: Assess Desired Outcome Coverage

Evaluate whether user story tests verify desired outcomes — the measurable end-states that prove features work:

1. **Check if user stories define desired outcomes**: Look for "Desired Outcomes" sections in `docs/planning/user-stories.md`

   * If present: count how many stories have desired outcomes defined

   * If absent: note "User stories lack desired outcomes — tests may verify steps without confirming the feature actually works end-to-end"

2. **Check if E2E tests assess desired outcomes**: For each user story with a test spec:

   * Look for a test block that explicitly assesses outcomes (named "Desired outcomes:" or similar)

   * A test that just walks through steps without checking the final result is NOT an outcome assessment

   * Report: "X of Y user stories have outcome assessment tests"

3. **Evaluate outcome quality**: For stories that do have outcome tests, check:

   * Are outcomes **observable** (verified via UI state, API response, URL)?

   * Are outcomes **specific** (expected value defined, not just "it works")?

   * Are outcomes **end-to-end** (cover the full result, not just an intermediate step)?

   * Report: "Outcome quality: X% observable, Y% specific, Z% end-to-end"

Include in the gap report:

```
### Desired Outcome Assessment
| Check | Result | Status |
|-------|--------|--------|
| Stories with desired outcomes defined | X of Y | ✅/⚠️/❌ |
| Stories with outcome assessment tests | X of Y | ✅/⚠️/❌ |
| Outcome quality (observable, specific, E2E) | X% pass | ✅/⚠️/❌ |
```

Thresholds: ✅ >80%, ⚠️ 50-80%, ❌ <50%.

### Step 3f: Assess UX Quality

Evaluate the application's user experience quality (requires a running app):

1. **Feedback loops**: Check that interactive elements produce visible responses

   * Scan for buttons, form submits, and links — do they show loading/success/error states?

   * Look for bare `onClick` handlers without associated loading or feedback UI

   * Check for "dead end" error states (errors without recovery paths)

   * Report: "Feedback coverage: X of Y interactive flows have visible feedback"

2. **Error message quality**: Check error handling UX

   * Grep source code for error messages, toast notifications, alert text

   * Evaluate: Are messages plain language? Do they include resolution steps?

   * Look for raw HTTP status codes, stack traces, or technical jargon exposed to users

   * Report: "Error UX: X of Y error messages are user-friendly"

3. **Destructive action safety**: Check for confirmation patterns

   * Find all delete/remove/destroy actions in the UI

   * Check if they have confirmation dialogs or undo mechanisms

   * Report: "Destructive action safety: X of Y destructive actions have confirmations"

4. **Dark pattern scan**: Check for manipulative UI

   * Look for confirmshaming language on opt-out buttons

   * Check if cancellation/unsubscribe paths are equally accessible as signup paths

   * Look for pre-checked checkboxes that opt users into non-essential features

   * Report: "Dark patterns: None found / \[list each]"

### Step 3g: Assess UI Visual Quality

Evaluate the visual design quality (requires a running app):

1. **Color contrast**: Run axe-core contrast audit

   * Count total WCAG contrast failures (body text, large text, non-text)

   * Report: "Contrast: X failures across Y pages"

2. **Typography consistency**: Analyze CSS/rendered output

   * Count distinct font families in use

   * Check heading hierarchy (h1 > h2 > h3, no skipped levels)

   * Report: "Typography: N font families, heading hierarchy \[correct/broken]"

3. **Component consistency**: Visual pattern matching

   * Count distinct button styles, input styles, card styles

   * Check for missing interactive states (hover, focus, disabled)

   * Report: "Component consistency: N button variants (target ≤ 4), N missing states"

4. **Spacing and alignment**: Grid analysis

   * Check if spacing follows a consistent scale

   * Look for irregular padding on similar components

   * Report: "Spacing: \[consistent N-px grid / inconsistent]"

### Step 4: Count and Categorize

For each test file found, categorize as: unit, integration, E2E, performance, security, accessibility, or other.

Produce counts:

* Total test files per category

* Estimated test count (grep for `test(`, `it(`, `describe(`, `#[test]`, `def test_`)

* Coverage percentage if reports exist

### Step 5: Generate Gap Report

Output a structured report:

```
## Test Coverage Audit Report

### Project Profile
- Type: [SPA / API / Full-stack / Library]
- Languages: [detected languages]
- Recommended Model: [Pyramid / Diamond / Trophy]

### Coverage Summary

| Layer | Status | Files | Tests | Notes |
|-------|--------|-------|-------|-------|
| Static Analysis | ✅ Present / ⚠️ Partial / ❌ Missing | N | - | details |
| Unit Tests | ... | N | ~N | ... |
| Integration Tests | ... | N | ~N | ... |
| Component Tests | ... | N | ~N | ... |
| E2E Tests | ... | N | ~N | ... |
| Performance Tests | ... | N | ~N | ... |
| Security Scanning | ... | N | - | ... |
| Accessibility | ... | N | ~N | ... |
| UX Quality | ✅ / ⚠️ / ❌ | - | - | heuristic scores, feedback, errors |
| UI Visual Quality | ✅ / ⚠️ / ❌ | - | - | contrast, typography, consistency |
| CI/CD Gates | ... | - | - | ... |

### Top Priority Gaps
1. [Most critical missing layer with explanation]
2. [Second priority]
3. [Third priority]

### Recommendations
- [Specific actionable recommendations per gap]
```

### Tips

* Be specific about what's missing — "No integration tests for API endpoints" not just "Missing integration tests"

* Prioritize gaps by impact: security and regression testing gaps are usually highest priority

* Note if test quality looks low (e.g., many tests but no assertions, snapshot-only tests)

* Reference the test-strategy skill for detailed guidance on any testing type