---
name: test-plan
description: Generate a phased testing strategy and implementation plan tailored to the current project
argument-hint: "[path-to-project]"
allowed-tools: ["Read", "Glob", "Grep", "Bash", "Agent"]
---

# Testing Strategy Plan Generator

Generate a comprehensive, phased testing implementation plan tailored to the project.

## Instructions

Analyze the project and produce an actionable testing strategy with prioritized phases.

### Step 1: Assess Current State

If a `/test-everything:test-audit` was recently run, use those results. Otherwise, perform a quick assessment:

* Detect project type, languages, frameworks

* Inventory existing test infrastructure

* Identify major gaps

#### Cross-Plugin Intelligence

Before planning, check for artifacts from other plugins that can inform the test strategy:

1. **Check for `docs/planning/user-stories.md`** (bo-planner artifact):
   - If found, parse all user stories with their acceptance criteria and desired outcomes
   - Each user story maps to at least one E2E test spec
   - Acceptance criteria map directly to test assertions
   - Include a "Story-Driven Tests" section in the plan

2. **Check for `docs/planning/architecture.md`** (bo-planner artifact):
   - If found, extract API endpoints, service boundaries, and data models
   - API endpoints → integration test stubs (one per endpoint)
   - Service boundaries → integration test fixtures
   - Data models → unit test coverage targets for validation logic

3. **Check for `docs/planning/ux-plan.md`** (bo-planner artifact):
   - If found, extract user flows (happy path + error paths)
   - Each user flow → E2E test covering the complete flow
   - Error paths → negative E2E tests

4. **Check for `enterprise-assessment-report.md`** or `docs/planning/enterprise-assessment.md`:
   - If found, read the Testing category findings
   - Use identified gaps as P0 priorities in the test plan
   - Reference compliance requirements that need test evidence (e.g., SOC2 CC8.1)

5. **Check for `src/theme/ThemeModeProvider.tsx`** (standard-design artifact):
   - If found, the project uses Standard Design System
   - Plan component tests that verify theme token usage
   - Plan visual regression tests for dark/light mode switching

### Step 2: Select Testing Architecture Model

Based on project type, recommend:

| Project Type          | Model             | Rationale                     |
| --------------------- | ----------------- | ----------------------------- |
| Library / utility     | Pyramid           | Unit tests ARE the product    |
| API / backend service | Pyramid           | Business logic-heavy          |
| Frontend SPA          | Trophy            | Integration + static analysis |
| Full-stack web app    | Diamond           | Integration-heavy with E2E    |
| Microservices         | Diamond/Honeycomb | Service interaction focus     |

### Step 3: Define Target State

For each testing layer, specify:

* Target tool (from preferred stack: Vitest, Rust `#[test]`, Playwright, k6, etc.)

* Target coverage or scope

* Priority (P0 = must have, P1 = should have, P2 = nice to have)

### Step 4: Generate Phased Plan

Create an implementation plan organized in 2-week phases:

**Phase 0 (E2E Environment)**: Sandbox-safe Playwright setup (browser path, no webServer, API-first auth, timeouts)
**Phase 1 (Foundation)**: Static analysis + unit testing framework
**Phase 2 (Integration)**: Integration tests + test database setup
**Phase 3 (E2E)**: User-story-driven Playwright tests with desired outcome assessment + clickable element outcome testing + exhaustive interaction crawl
**Phase 4 (Security + Performance)**: SAST in CI + k6 load tests
**Phase 5 (Polish)**: Accessibility + cross-browser + documentation

For each phase, provide:

* Specific files to create or modify

* Tool installation commands

* Configuration snippets

* Estimated effort (hours/days)

* Dependencies on previous phases

#### Phase 0 — E2E Environment Setup (MANDATORY for Phase 3)

Before planning E2E tests, ensure the environment will work reliably in sandbox (Claude Code). These steps prevent the most common E2E failures — not test bugs, but environment bugs that cause 100% failure rates.

Plan these tasks:
- [ ] Install Playwright browsers to writable path: `PLAYWRIGHT_BROWSERS_PATH=.playwright-browsers npx playwright install chromium`
- [ ] Add `.playwright-browsers/` to `.gitignore`
- [ ] Create `playwright.config.ts` with NO `webServer` block, `timeout: 60000`, `expect.timeout: 10000`
- [ ] Set `PLAYWRIGHT_BROWSERS_PATH` in ALL npm scripts: `"test:e2e": "PLAYWRIGHT_BROWSERS_PATH=.playwright-browsers playwright test"`
- [ ] Create API-first auth fixture (`e2e/fixtures/auth.ts`) — register users via API, not UI forms
- [ ] Create browser health fixture (`e2e/fixtures/browser-health.ts`)
- [ ] Create server startup/readiness verification script or instructions

**Why**: In all observed failure sessions, these environment issues caused more test failures than actual test bugs. `webServer` timeouts, `EPERM` on browser install, and React re-render swallowing `page.fill()` were the top 3 failure causes.

See `references/e2e-sandbox-patterns.md` for full patterns and rationale.

#### Phase 3 — User Story Discovery

Before planning E2E tests, discover user stories:

1. **Check for** **`docs/planning/user-stories.md`** in the project root
2. **If found**: Parse each user story's workflow steps and acceptance criteria. Plan one E2E spec per story, with tests covering every workflow step.
3. **If not found**: Analyze the codebase to infer user stories:

   * Scan routes, pages, and navigation to identify user-facing features

   * Read API endpoints to understand data flows and CRUD operations

   * Identify authentication, authorization, and role-based access

   * Examine forms, interactive components, and error handling

   * Document inferred stories in `docs/planning/user-stories.md` (using `US-XXX` identifiers, workflow steps, and acceptance criteria)

   * Present to the user for review before proceeding
4. **Plan E2E specs**: Map each approved user story to a spec file, listing which workflow steps, acceptance criteria, and desired outcomes each test will cover
5. **Plan desired outcome assessment**: For each user story, define 2-5 desired outcomes — measurable end-states that prove the feature works. Include:
   * What success looks like (e.g., "User account exists and is accessible")
   * How to verify it (e.g., "API returns 201, user can log in")
   * Expected result (e.g., "Redirect to /dashboard after login")
   * Plan a dedicated outcome assessment test per story that verifies all outcomes after executing the full workflow
6. **Plan clickable element outcome tests**: For each page/route, build an element outcome map:
   * Identify every interactive element on the page (buttons, links, form fields, tabs, dropdowns, checkboxes, file inputs, etc.)
   * Define the expected outcome for each element (navigates to URL, opens modal, toggles state, accepts input, opens file chooser, etc.)
   * Plan one test per element verifying expected outcome = actual outcome through the rendered DOM
   * CRITICAL: file uploads MUST use `waitForEvent('filechooser')`, forms MUST use `fill()` + `click()` — no API shortcuts
   * This catches "button does nothing" bugs that user-story tests miss because they only test the happy path
7. **Plan exhaustive interaction crawl**: After clickable element tests, plan an exhaustive interaction test:
   * List all routes to crawl (from router config)
   * Identify pages with tabs, accordions, dropdowns, or modals that hide interactive elements
   * Plan the crawl to reveal hidden elements, then test every button, link, input, and dropdown
   * This is the safety net — catches errors on elements missed by clickable element tests

### Step 4b: Architecture-Driven Integration Tests

If `docs/planning/architecture.md` was found in Step 1:

1. Extract every API endpoint listed in the "API Design" section
2. For each endpoint, plan an integration test covering:
   - Happy path (valid request → expected response)
   - Auth required (unauthenticated → 401)
   - Validation (invalid input → 400 with error details)
   - Not found (missing resource → 404)
3. Extract service boundaries and plan integration tests for each boundary
4. Include these in Phase 2 of the implementation plan as "Architecture-Driven Tests"
5. Cross-reference with user stories — if a story maps to an endpoint, note the traceability

### Step 5: Define Quality Gates

Specify what must pass at each pipeline stage:

* Pre-commit hooks

* PR/MR checks

* Staging deployment gates

* Release criteria

### Step 6: Output the Plan

Format as a structured, actionable document:

```
## Testing Strategy Plan for [Project Name]

### Current State
[Summary of existing test infrastructure]

### Target Architecture: [Model Name]

### Implementation Phases

#### Phase 1: Foundation (Week 1-2)
Priority: P0
- [ ] Task 1 — [specific action with file paths]
- [ ] Task 2 — [specific action]
Install: `[exact install command]`
Config: [what to configure]

#### Phase 2: Integration (Week 3-4)
...

### Quality Gates
[Table of gates with specific pass criteria]

### Tool Stack
| Purpose | Tool | Install |
|---------|------|---------|
| Unit (frontend) | Vitest | `pnpm add -D vitest` |
| ... | ... | ... |

### Estimated Total Effort
[Rough estimate per phase]
```

### Tips

* Make every task specific and actionable — include file paths and commands

* Don't recommend tools outside the preferred stack unless there's a strong reason

* Phase 1 should be achievable in a single sprint

* Include "quick wins" in Phase 1 to build momentum

* Reference the test-strategy skill for deeper guidance on any testing type