# Test-Everything Plugin — Consensus Plan

> Produced by adversarial debate on 2026-04-01
> Source plan: docs/planning/phased-plan.md
> Personas: Senior QA Architect, Senior E2E Test Engineer, Senior Design Systems Engineer, Senior DX Engineer
> Rounds: 2
> Resolution: 6 resolved, 3 majority, 0 unresolved

## Key Decisions

| # | Topic | Resolution | Decision | Rationale |
|---|-------|-----------|----------|-----------|
| 1 | Terminology | RESOLVED (4:0) | Adopt **"semantic locators"** | "Accessible selectors" conflates test strategy with a11y compliance. "Semantic locators" precisely describes querying by meaning, not implementation. |
| 2 | Coverage report | RESOLVED (3:1) | Replace with **embedded checklist** | No viable data source for automated report. Checklist provides coverage thinking without overhead. |
| 3 | Selector allowlist | RESOLVED (3:0) | **Default set + per-project override** | Ship common patterns; projects extend with justification. Prevents first-run noise. |
| 4 | Component prerequisite | RESOLVED (4:0) | **Diagnostic, not gate** | Flag missing component tests, don't block E2E generation. |
| 5 | Output examples | RESOLVED (4:0) | **2 examples per template section** (happy path + failure), inline | LLMs follow examples more reliably than rules. |
| 6 | Audit commands | RESOLVED (4:0) | **Concrete grep/rg commands** per anti-pattern | Replace free-form audit guidance with runnable detection commands. |
| 7 | Walkthrough | MAJORITY (3:1) | Replace with **3-5 independent cross-flow transition tests** + session smoke | E2E Engineer dissents: prefers killing the category entirely. |
| 8 | Test pyramid | MAJORITY (3:1) | **Test Distribution Check** in Phase 5; encourage component extraction | Design Systems Engineer dissents: wants 10:1 ratio enforced in Phase 2. |
| 9 | Timing strategy | MAJORITY (2:1:1) | **Mandatory timing section** in templates | DX Engineer rates LOW (already handled by banned patterns). Majority says explicit guidance prevents flaky tests. |

## Revised Plan

### Phase 1: Core Verification Patterns

#### 1.1 Fixture & Test Structure Template
- Standard Playwright test file scaffold with `test.describe` / `test` blocks
- Fixture initialization pattern (page, context, browser — when each is appropriate)
- 2 inline examples: happy-path fixture setup + failure showing missing fixture error

#### 1.2 Semantic Locators ~~(formerly "selectors")~~
- Default allowlist: `getByRole` (preferred) > `getByLabel` > `getByText` > `getByPlaceholder` > `getByAltText` > `getByTestId` (fallback, requires justification comment)
- Per-project override mechanism with required `justification` field
- Banned patterns: raw CSS selectors, XPath, nth-child, fragile class-based selectors
- 2 inline examples: correct semantic locator chain + failure showing why `.btn-3` breaks

#### 1.3 Action-Outcome Pairing
- Every user action (`click`, `fill`, `check`) immediately followed by assertion on expected outcome
- No "fire and forget" interactions
- Formal definition: an interaction is verified if and only if it is followed (before the next interaction or end of test block) by an `expect()`, `waitForResponse()`, or `waitForURL()` call
- 2 inline examples: correct action-outcome pair + failure showing assertion gap

#### 1.4 Three Verification Patterns
1. **Content verification** — visible text, element presence, attribute values
2. **State verification** — enabled/disabled, checked/unchecked, expanded/collapsed (ARIA states)
3. **Navigation verification** — URL changes, page transitions, route guards

Each pattern with 2 inline examples (happy + failure).

#### 1.5 Browser Health Fixture
- Shared `browser-health.ts` fixture with `beforeEach`/`afterEach`
- Console error + network failure detection
- **Default allowlist** for known false positives (Vite HMR, React DevTools, browser extension noise, favicon 404)
- Per-test opt-out for expected errors: `test.use({ expectedErrors: [/pattern/] })`
- Playwright trace capture on failure: `trace: 'retain-on-failure'`
- 2 inline examples: fixture catching real error + allowlist filtering benign warning

### Phase 2: Quality & Audit Enhancements

#### 2.1 Anti-Pattern Detection
Concrete grep commands for each banned pattern:
```bash
# Detect hardcoded waits
rg 'waitForTimeout|page\.wait\(\d' --type ts

# Detect raw CSS selectors in locators
rg "page\.locator\(['\"][^'\"]*[.#>\[\]]" --type ts

# Detect fire-and-forget interactions (actions without assertions)
rg '(click|fill|check|press)\(' --type ts -A 3 | rg -v 'expect|assert|toHave|toBe'

# Detect test interdependence (shared mutable state)
rg 'let\s+\w+\s*=' --type ts -B 2 | rg 'describe|beforeAll'
```

#### 2.2 Mandatory Timing Strategy
- **Dynamic waits:** `waitForSelector`, `waitForResponse`, `waitForURL`, `expect().toBeVisible()`
- **Network idle:** `waitForLoadState('networkidle')` only at navigation boundaries
- **Retry budgets:** `expect.toPass({ timeout: 5000 })` for eventually-consistent UI
- **Banned:** `waitForTimeout()`, arbitrary `sleep`, hardcoded delays
- 2 inline examples: correct dynamic wait chain + failure showing flaky timeout

#### 2.3 Coverage Checklist
Embedded in the test template as a thinking prompt:
```
// Coverage Checklist:
// [ ] Happy path tested
// [ ] Primary error/edge case tested
// [ ] Empty state tested (if applicable)
// [ ] Loading state tested (if applicable)
// [ ] Auth boundary tested (if applicable)
// [ ] Mobile viewport tested (if applicable)
```

#### 2.4 Component Test Diagnostic
- When generating E2E tests, check for corresponding component test files
- If missing: emit warning comment in generated test
- Does not block E2E test generation

### Phase 3: Advanced Features

#### 3.1 Cross-Flow Transition Tests ~~(replaces "Walkthrough")~~
- **3-5 independent specs** per application, each testing a meaningful user journey transition
- Each spec fully self-contained (own setup, own teardown, no shared state)
- Each transition test: < 30 seconds, < 10 actions
- Example transitions: Search → Detail → Cart, Login → Dashboard → Settings
- **Thin session durability smoke test:** one spec verifying session/auth persists across 2 navigations
- 2 inline examples: correct independent transition test + failure showing shared-state leak

#### 3.2 Visual Regression Hooks
- `toHaveScreenshot()` integration points identified but not mandatory
- Configuration template for threshold, maxDiffPixels, and viewport list
- Guidance on baseline management and CI/OS consistency
- Opt-in, not default

#### 3.3 Test Distribution Check (Phase 5 Validation)
- After all tests generated, count E2E vs component tests
- Flag if E2E count > component count (advisory, not blocking)
- Include in validation report

### Phase 4: Documentation & Finalization

#### 4.1 Template Documentation
- All examples inline (per Output Examples decision)
- Quick-start section: "Generate your first test in 3 commands"

#### 4.2 CI/CD Integration Checklist
Embedded checklist (pipeline configuration is a separate deliverable):
```
// CI/CD Readiness:
// [ ] Playwright installed in CI image
// [ ] Browser binaries cached
// [ ] Test command in package.json scripts
// [ ] Failure screenshots/traces uploaded as artifacts
// [ ] Retry count configured (suggest: 2)
// [ ] Parallelism configured (suggest: workers=4)
```

#### 4.3 Validation & Success Metrics
- Primary: defect escape rate (tracked over 4-sprint window)
- Secondary: mean time to first green

## Unresolved Items

No 2:2 splits. All items reached at least majority consensus. Two MAJORITY items carry strong dissent worth monitoring:

### Walkthrough Replacement — E2E Engineer Dissent
> The "cross-flow transition test" naming could encourage over-scoped tests that recreate walkthrough problems. After 30 days, audit generated transition tests for action count (<10), duration (<30s), and state isolation.

### Test Distribution — Design Systems Engineer Dissent
> Phase 5 advisory check may be too late. If data shows persistent E2E-heavy generation, promote the DSE's ratio constraint to Phase 2 as an opt-in "strict mode."

## Dissenting Opinions

**E2E Engineer on Cross-Flow Tests:** "Kill the category. Independent specs plus a single session durability test are sufficient. The naming creates a false category that risks recreating coupled, brittle mega-tests."

**Design Systems Engineer on Test Pyramid:** "A 10:1 component-to-E2E instruction ratio should be embedded in Phase 2 template generation, not deferred to Phase 5. By the time the distribution check runs, the agent has already generated an E2E-heavy suite."

**DX Engineer on Timing Strategy:** "Already handled by the banned patterns table and sandbox config. Adding a dedicated section is redundant and increases template length, which hurts adoption."
