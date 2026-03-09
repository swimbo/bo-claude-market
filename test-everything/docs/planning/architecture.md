# Architecture — Interaction Verification Improvements

## Plugin Structure (No Changes)

The test-everything plugin is a Claude Code plugin consisting of markdown templates. It does not contain executable code — it instructs Claude how to generate tests for target projects.

```
test-everything/
├── commands/      # Slash commands (user-invocable)
├── agents/        # Specialized sub-agents
├── skills/        # Knowledge bases with references
└── research/      # Design documents
```

## Change Architecture

All changes are **additive** — extending existing markdown templates with new sections and patterns. No structural changes to the plugin.

### Key Design Decisions

**1. Shared Fixture Approach (for P2-P3)**

Console error monitoring and network request detection are implemented as a single shared Playwright fixture file (`e2e/fixtures/browser-health.ts`) that gets scaffolded alongside test files. This is preferred over:
- Embedding monitoring in every test (repetitive, easy to forget)
- A custom Playwright config (too opaque, harder to customize)

The fixture pattern uses `beforeEach`/`afterEach` hooks so it applies automatically to all tests.

**2. Inline Verification vs. Separate Assertion Step (for P1)**

Action-outcome pairing is implemented as inline assertions immediately after each interaction, not as a separate validation step at the end of the test. This is preferred because:
- Failures pinpoint exactly which interaction broke
- Matches how users think about workflows ("click submit → see confirmation")
- Easier for Claude to generate (action + assertion is a natural pair)

**3. Selector Strategy (for P4)**

Playwright's built-in accessible locators (`getByRole`, `getByLabel`, `getByText`) are preferred over Testing Library's `@testing-library/test-id` pattern. This is a Playwright best practice and doesn't require additional dependencies.

**4. Walkthrough as Separate Test (for P5)**

The post-suite walkthrough is a separate spec file (`walkthrough.spec.ts`) rather than a test hook, so it:
- Appears in test reports as its own entry
- Can be run independently
- Can be skipped without affecting other tests

## Files Modified and Why

| File | What Changes | Why |
|------|-------------|-----|
| `test-scaffold.md` | Add verification patterns to e2e section, add fixture template, add walkthrough + visual regression templates, update selector guidance | This is where test generation templates live |
| `test-full-suite.md` | Add verification rules to Phase 3, browser health to Phase 4, coverage report to Phase 6 | This orchestrates the full testing workflow |
| `test-audit.md` | Add interaction verification and selector quality checks | This audits existing test suites |
| `test-quality-reviewer.md` | Add fire-and-forget and selector anti-patterns | This reviews test quality |
| `SKILL.md` | Add interaction verification principles | This is the knowledge base |
| `testing-types-detail.md` | Expand E2E section with patterns and fixtures | This is the detailed reference |
| `implementation-roadmap.md` | Add verification to Phase 3 checklist | This guides phased implementation |
| `plugin.json` | Version 0.4.0 → 0.5.0 | Reflects new capabilities |
