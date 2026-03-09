# Phase 1: Core Verification Patterns (P1-P3)

**Priority:** Highest — these 3 changes have the most impact on fixing "tests pass, app broken"
**User Stories:** US-001, US-002, US-003
**Files:** test-scaffold.md, test-full-suite.md, testing-types-detail.md

## Tasks

### 1.1 Add Browser Health Fixture Template to test-scaffold.md

**File:** `commands/test-scaffold.md`
**Location:** Inside `### Layer: e2e`, after the Playwright config section

- [ ] Add new subsection: `**Browser Health Monitoring**`
- [ ] Include template for `e2e/fixtures/browser-health.ts` that scaffolds:
  - `beforeEach`: Register `pageerror`, `console.error`, `requestfailed`, `response` listeners
  - `afterEach`: Assert no console errors and no failed API requests
  - Export a custom `test` fixture that extends Playwright's base test
- [ ] Include opt-out pattern for expected errors (e.g., testing error pages)
- [ ] Add instruction: "Always scaffold this fixture alongside E2E test files"

### 1.2 Add Action-Outcome Pairing to test-scaffold.md

**File:** `commands/test-scaffold.md`
**Location:** Inside `**User-Story-Driven Test Generation**` section

- [ ] Add new subsection: `**Interaction Verification Rules**`
- [ ] Define the rule: every `page.click()`, `page.fill()`, `page.goto()` must be followed by an assertion
- [ ] Provide the three verification patterns with examples:
  - Navigation verification: `await expect(page).toHaveURL(...)`
  - DOM change verification: `await expect(page.getByText(...)).toBeVisible()`
  - Network verification: `await page.waitForResponse(...)`
- [ ] Update the example user-story test structure to show action-outcome pairs
- [ ] Replace the current example (lines 141-150) with a verification-aware example

### 1.3 Add Verification Rules to test-full-suite.md Phase 3

**File:** `commands/test-full-suite.md`
**Location:** Inside `#### User-Story-Driven E2E Tests` section

- [ ] Add rule: "Every interaction in generated E2E tests MUST be paired with an outcome assertion"
- [ ] Add instruction: "Scaffold the browser health fixture before writing any E2E tests"
- [ ] Add rule: "Import and use the custom test fixture from `e2e/fixtures/browser-health.ts`"

### 1.4 Add Browser Health Check to test-full-suite.md Phase 4

**File:** `commands/test-full-suite.md`
**Location:** Inside `### Phase 4: Run & Fix`

- [ ] Add step: "Before declaring tests passing, verify browser health fixture caught no silent failures"
- [ ] Add step: "Check test output for console error and network failure assertions"
- [ ] Add step: "If browser health tests reveal runtime errors, fix the source code — don't disable the fixture"

### 1.5 Expand E2E Section in testing-types-detail.md

**File:** `skills/test-strategy/references/testing-types-detail.md`
**Location:** Inside `### End-to-End (E2E) Testing` section

- [ ] Add subsection: `**Interaction Verification**`
  - Explain the action-outcome pairing principle
  - Show before/after code examples
  - List the three verification patterns
- [ ] Add subsection: `**Browser Health Monitoring**`
  - Explain console error and network request detection
  - Show the fixture code pattern
  - Explain why silent failures are dangerous
- [ ] Update the existing Playwright example (lines 164-181) to include verification assertions

## Dependencies

- None — this phase can start immediately

## Verification

- [ ] Read the modified test-scaffold.md and verify the e2e section includes fixture template + action-outcome pairing
- [ ] Read the modified test-full-suite.md and verify Phase 3 includes verification rules and Phase 4 includes health checks
- [ ] Read the modified testing-types-detail.md and verify E2E section has new subsections
- [ ] Verify no existing content was accidentally deleted
- [ ] Verify all code examples are syntactically correct TypeScript/Playwright
