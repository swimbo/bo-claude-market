# Phase 3: Advanced Features (P5-P7)

**Priority:** Medium — additional verification layers
**User Stories:** US-005, US-006, US-007
**Files:** test-scaffold.md, test-full-suite.md

## Tasks

### 3.1 Add Walkthrough Test Template to test-scaffold.md

**File:** `commands/test-scaffold.md`
**Location:** Inside `### Layer: e2e`, after `**Common E2E Tests**` section

- [ ] Add new subsection: `**Post-Suite Walkthrough**`
- [ ] Define the walkthrough concept: a single test that chains the top user story workflows into one continuous session
- [ ] Include template for `e2e/walkthrough.spec.ts`:
  - Single `test()` block (not separate tests per step)
  - No `page.goto()` between flows — maintains session state
  - Chains: login → core workflow → secondary workflow → verify data → logout
  - Uses the browser health fixture
  - Comments explain why this catches cross-flow bugs
- [ ] Include guidance: "Derive the walkthrough from the top 3-5 user stories"
- [ ] Note: "This test should run AFTER all individual E2E tests pass"

### 3.2 Add Interaction Coverage Report to test-full-suite.md Phase 6

**File:** `commands/test-full-suite.md`
**Location:** Inside `### Phase 6: Summary`

- [ ] Add new section to the Phase 6 output: `### Interaction Coverage`
- [ ] Define the report format:
  ```
  ### Interaction Coverage
  | Page/Route | Interactive Elements | Tested | Coverage |
  |------------|---------------------|--------|----------|
  | /dashboard | 12                  | 8      | 67%      |
  | /settings  | 9                   | 3      | 33%      |

  #### Untested Elements
  - /dashboard: [Export CSV] button, [Filter] dropdown, [Notifications] bell
  - /settings: [Delete Account] button, [Change Password] form
  ```
- [ ] Add instructions for generating this report:
  - After E2E tests complete, use Playwright to visit each route
  - Query for all `button`, `a[href]`, `input`, `select`, `textarea`, `[role="button"]` elements
  - Cross-reference with test trace (which elements were clicked/filled)
  - Output the gap report
- [ ] Note: "This report is informational — it doesn't fail the suite"

### 3.3 Add Visual Regression Template to test-scaffold.md

**File:** `commands/test-scaffold.md`
**Location:** Inside `### Layer: e2e`, update existing `e2e/visual-regression.spec.ts` entry in Common E2E Tests

- [ ] Expand the existing visual regression bullet (currently just a brief mention) into a full template section
- [ ] Include template for `e2e/visual-regression.spec.ts`:
  - Tests for top 3-5 critical page states
  - Uses `expect(page).toHaveScreenshot()` with meaningful names
  - Includes guidance on updating baselines: `npx playwright test --update-snapshots`
  - Notes about CI environment consistency (baselines must match CI OS)
- [ ] Add interaction verification to the visual tests:
  - Navigate to page, perform key action, THEN screenshot
  - Not just static page screenshots — capture state after interaction
- [ ] Keep this as opt-in (scaffold when `e2e` layer is requested, but noted as optional)

### 3.4 Add Walkthrough to test-full-suite.md Phase 3

**File:** `commands/test-full-suite.md`
**Location:** Inside `### Phase 3: Scaffold & Write Tests`, after `#### Common E2E Tests`

- [ ] Add new subsection: `#### Post-Suite Walkthrough`
- [ ] Instructions:
  - After writing all individual E2E tests, write a walkthrough test
  - Chain the top 3-5 user story workflows into a single continuous test
  - Run the walkthrough only after all individual tests pass (Phase 4)
- [ ] Add to Phase 4: "Run walkthrough test after all individual E2E tests pass"

## Dependencies

- Phase 1 must be complete (walkthrough uses browser health fixture)
- Phase 2 should be complete (walkthrough uses accessible selectors)

## Verification

- [ ] Read test-scaffold.md and verify walkthrough template exists with correct pattern
- [ ] Read test-scaffold.md and verify visual regression template is expanded
- [ ] Read test-full-suite.md Phase 3 and verify walkthrough subsection exists
- [ ] Read test-full-suite.md Phase 6 and verify interaction coverage report format is defined
- [ ] Verify walkthrough template imports browser health fixture
- [ ] Verify walkthrough template uses accessible selectors
