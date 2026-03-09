# Phase 2: Quality & Audit Enhancements (P4)

**Priority:** Medium-High — improves selector quality and catches anti-patterns
**User Stories:** US-004
**Files:** test-scaffold.md, test-audit.md, test-quality-reviewer.md

## Tasks

### 2.1 Add User-Centric Selector Guidance to test-scaffold.md

**File:** `commands/test-scaffold.md`
**Location:** Inside `### Layer: e2e`, in the User-Story-Driven Test Generation section

- [ ] Add new subsection: `**Selector Strategy**`
- [ ] Define selector priority order:
  1. `page.getByRole('button', { name: '...' })` — buttons, links, headings, etc.
  2. `page.getByLabel('...')` — form inputs with labels
  3. `page.getByText('...')` — visible text content
  4. `page.getByTestId('...')` — last resort only
- [ ] Explain why: accessible selectors verify the element is properly wired up, not just present in DOM
- [ ] Update all existing code examples in the e2e section to use `getByRole`/`getByLabel`/`getByText` instead of CSS selectors
- [ ] Replace `page.fill('[name="email"]', ...)` with `page.getByLabel('Email').fill(...)`
- [ ] Replace `page.click('button[type="submit"]')` with `page.getByRole('button', { name: 'Submit' }).click()`

### 2.2 Add Interaction Verification Check to test-audit.md

**File:** `commands/test-audit.md`
**Location:** Inside `### Step 3: Assess Each Testing Layer`, after the E2E row

- [ ] Add new subsection: `### Step 3c: Assess Interaction Verification Quality`
- [ ] Check if existing E2E tests follow action-outcome pairing:
  - Grep for `page.click(` without a following `expect(` or `waitFor(`
  - Count fire-and-forget interactions vs. verified interactions
  - Report ratio: "X of Y interactions have outcome assertions"
- [ ] Check selector quality:
  - Count usage of `page.getByRole`, `page.getByLabel`, `page.getByText` (good)
  - Count usage of `page.click('[data-testid=`, `page.click('.`, `page.click('#` (poor)
  - Report ratio: "X% of selectors use accessible locators"
- [ ] Check for browser health fixture:
  - Look for `pageerror` listener in test setup
  - Look for `requestfailed` listener
  - Report: "Browser health monitoring: present/absent"
- [ ] Add these checks to the gap report output table

### 2.3 Add Anti-Patterns to test-quality-reviewer.md

**File:** `agents/test-quality-reviewer.md`
**Location:** Inside `### Step 2: Check for Anti-Patterns`

- [ ] Add to **Quality issues** list:
  - "Fire-and-forget interactions — `page.click()` or `page.fill()` without a subsequent assertion verifying the outcome"
  - "CSS/data-testid selectors over accessible locators — using `page.click('[data-testid=...]')` instead of `page.getByRole()`"
  - "No browser health monitoring — E2E tests without console error or network failure detection"
- [ ] Each new anti-pattern should include:
  - What to grep for
  - Impact description
  - Recommended fix

## Dependencies

- Phase 1 must be complete (defines the patterns that Phase 2 audits for)

## Verification

- [ ] Read test-scaffold.md e2e section and verify all code examples use accessible selectors
- [ ] Read test-audit.md and verify Step 3c exists with interaction verification + selector quality checks
- [ ] Read test-quality-reviewer.md and verify 3 new anti-patterns are listed
- [ ] Verify the anti-patterns have grep-able detection patterns
- [ ] Verify no existing anti-patterns were removed
