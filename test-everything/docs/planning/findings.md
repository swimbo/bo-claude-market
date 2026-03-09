# Findings — Interaction Verification Research

**Date:** 2026-03-08

## Research Summary

### Problem Statement

The test-everything plugin generates E2E tests from user stories that pass but don't catch real functional issues (broken buttons, failing workflows). Manual testing reveals problems the automated tests missed.

### Root Cause Analysis

1. **Fire-and-forget interactions** — Tests click/submit without verifying the outcome
2. **Silent browser errors** — Console errors and failed network requests don't fail tests
3. **Implementation-detail selectors** — CSS selectors find elements that exist but aren't functional
4. **Isolated test state** — Individual tests don't catch cross-flow issues

### Key Research Sources

| Source | Key Insight |
|--------|-------------|
| [Playwright Best Practices](https://playwright.dev/docs/best-practices) | Use web-first assertions, role-based selectors, avoid manual waits |
| [Kent C. Dodds - Testing Trophy](https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications) | Integration tests give highest ROI; test user behavior, not implementation |
| [Kent C. Dodds - Testing Implementation Details](https://kentcdodds.com/blog/testing-implementation-details) | Implementation-detail tests create false positives (pass when app is broken) |
| [Google Testing Crab](https://web.dev/articles/ta-strategies) | Visual testing deserves significant investment alongside functional testing |
| [Smashing Magazine - Frontend Testing Pitfalls](https://www.smashingmagazine.com/2021/07/frontend-testing-pitfalls/) | Excessive mocking creates false confidence |

### Technical Decisions

| Decision | Chosen | Alternative | Why |
|----------|--------|-------------|-----|
| Error monitoring approach | Shared Playwright fixture | Per-test setup | DRY, automatic for all tests, opt-out for expected errors |
| Verification pattern | Inline after each action | End-of-test batch check | Pinpoints exact failing interaction |
| Selector strategy | Playwright built-in locators | Testing Library locators | No extra dependency, Playwright best practice |
| Walkthrough architecture | Separate spec file | Test hook after suite | Appears in reports, runnable independently |
| Visual regression tool | Playwright `toHaveScreenshot()` | Percy/Chromatic | Free, no vendor dependency, sufficient for critical pages |
| Interaction coverage | Informational report | Failing test | Too many false positives if enforced as pass/fail |

## Open Questions

- None currently — all decisions made during brainstorming
