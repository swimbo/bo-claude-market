# Phase 4: Documentation & Finalization

**Priority:** Required — ties everything together
**User Stories:** All (documentation)
**Files:** SKILL.md, implementation-roadmap.md, plugin.json

## Tasks

### 4.1 Add Interaction Verification Principles to SKILL.md

**File:** `skills/test-strategy/SKILL.md`
**Location:** After `### End-to-End (E2E) Testing` section, before `### Other Functional Types`

- [ ] Add new subsection: `### Interaction Verification`
- [ ] Content:
  - **Principle:** Every test interaction must have a paired outcome assertion
  - **Three verification patterns:** navigation, DOM change, network response
  - **Browser health monitoring:** console errors + network failures = automatic test failure
  - **Selector strategy:** `getByRole` > `getByLabel` > `getByText` > `data-testid`
- [ ] Add to the Recommended Stack Distribution table:
  - Update E2E row: "All user story workflows + **interaction verification**"
- [ ] Add to Quality Gates:
  - Staging gate: add "E2E interaction verification passing"

### 4.2 Add Interaction Verification to implementation-roadmap.md Phase 3

**File:** `skills/test-strategy/references/implementation-roadmap.md`
**Location:** Inside `## Phase 3: E2E & UI (Week 5-6)`

- [ ] Add to `### Playwright Setup` checklist:
  - `[ ] Scaffold browser health fixture (console error + network failure detection)`
  - `[ ] Configure custom test fixture extending Playwright's base test`
- [ ] Add to `### User-Story-Driven E2E Tests` checklist:
  - `[ ] Apply action-outcome pairing to all generated test interactions`
  - `[ ] Use accessible selectors (getByRole, getByLabel, getByText) — avoid CSS selectors`
  - `[ ] Write post-suite walkthrough test chaining top 3-5 user story flows`
- [ ] Add new checklist item:
  - `[ ] Add visual regression tests for critical page states (opt-in)`

### 4.3 Update Plugin Description and Version

**File:** `.claude-plugin/plugin.json`

- [ ] Bump version: `"0.4.0"` → `"0.5.0"`
- [ ] Update description to mention interaction verification:
  - Current: "Comprehensive testing toolkit: audit coverage gaps, plan testing strategies, scaffold test infrastructure, and review test quality across all testing layers — with user-story-driven E2E testing"
  - New: "Comprehensive testing toolkit: audit coverage gaps, plan testing strategies, scaffold test infrastructure, and review test quality across all testing layers — with user-story-driven E2E testing and interaction verification"
- [ ] Add keyword: `"interaction-verification"` to keywords array

### 4.4 Update README.md

**File:** `README.md`

- [ ] Add brief mention of interaction verification in the feature list
- [ ] Note the new browser health monitoring capability
- [ ] Keep changes minimal — just reflect the new features

## Dependencies

- Phases 1-3 must be complete

## Verification

- [ ] Read SKILL.md and verify interaction verification section exists
- [ ] Read implementation-roadmap.md Phase 3 and verify new checklist items
- [ ] Read plugin.json and verify version = 0.5.0, updated description, new keyword
- [ ] Read README.md and verify new features mentioned
- [ ] Run a full diff of all changed files to verify no unintended changes
- [ ] Verify plugin.json is valid JSON
