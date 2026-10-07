# test-everything

Comprehensive testing toolkit for Claude Code. Audit coverage gaps, plan strategies, scaffold infrastructure, and review quality across all testing layers — with user-story-driven E2E, exhaustive interaction crawling, desired outcome assessment, UX/UI auditing, and 13 AI-agent testing capabilities (mutation gating, property/fuzz/differential testing, flaky quarantine, quality scorecards, selective CI gating).

## Governing Rule

> **LLMs author tests and state invariants. Deterministic tools — test runners, mutation engines, fuzzers, contract verifiers — decide pass/fail and whether tests are acceptable. No LLM judgment sits in the merge gate. Mutation score gates test acceptance; coverage only selects where to write next; every new suite must pass a negative control (break the code, the suite must go red).**

Every command in this plugin obeys this rule. AI agents write the tests; deterministic tools decide whether the tests count. See the skill's [enhancement-capabilities](skills/test-strategy/references/enhancement-capabilities.md) reference for the 13 mechanisms behind it.


## Features

* **Coverage Audit** — Scan any project and produce a gap report across all testing layers, including interaction verification quality, selector usage, exhaustive element coverage, and desired outcome completeness

* **Testing Strategy Plan** — Generate a phased implementation plan (Foundation → Integration → E2E → Security/Performance → Polish) tailored to your project type and current state

* **Test Scaffolding** — Create test files, configs, and CI pipelines for any testing layer: unit, integration, component, E2E, performance, security, accessibility, UX, UI, or CI

* **User-Story-Driven E2E** — E2E specs derived from user stories in `docs/planning/user-stories.md` (or inferred from the codebase); one spec per story covering every workflow step

* **Desired Outcome Assessment** — Defines measurable desired outcomes for each user story and assesses actual software results against those outcomes, producing a pass/fail report per story

* **Exhaustive Interaction Crawl** — Systematically discovers and tests EVERY interactive element on every page, including buttons and links hidden behind sub-tabs, accordions, modals, and dropdowns — catches dead buttons, broken links, and non-functional fields that user-story tests miss

* **Interaction Verification** — Every E2E interaction is paired with an outcome assertion (URL change, DOM change, network response, or element state); fire-and-forget clicks are flagged as anti-patterns

* **Browser Health Monitoring** — Shared Playwright fixture that automatically fails tests on console errors, uncaught JS exceptions, and failed API requests (4xx/5xx), catching silent failures across all E2E tests

* **Walkthrough Test** — Single continuous test chaining top user story workflows in one browser session to catch cross-flow bugs that isolated tests miss

* **Common E2E Tests** — Scaffolds cross-cutting tests: smoke, error pages (404/unauthorized/API errors), responsive (375/768/1280px), navigation (deep links, back/forward, redirects), and optional visual regression

* **UX Quality Audit** — Evaluate against Nielsen's 10 usability heuristics, detect dark patterns (confirmshaming, roach motel, bad defaults), check feedback loops and error messages, then implement top improvements

* **UI Visual Quality Audit** — Check color contrast (WCAG 2.2), typography consistency, spacing grid alignment, component uniformity, and visual hierarchy via axe-core + screenshots, then fix issues

* **Gap Analysis** — Proactive agent that identifies missing tests after code changes, including missing outcome assessments and uncovered interactive elements

* **Quality Review** — Agent that finds anti-patterns (fire-and-forget clicks, CSS selectors over accessible locators, missing outcome assessment, incomplete element coverage), flakiness risks, and architecture misalignment; issues a PASS/FAIL verdict with automated grep checks

* **Non-Negotiable Rules** — Banned patterns table (waitForTimeout, CSS selectors, fire-and-forget clicks, test.fixme, vague assertions) with enforcement at every phase; BAD vs GOOD test examples sourced from real failures

* **Mandatory Self-Review (Phase 3.5)** — Blocking checkpoint where all generated tests are grepped for banned patterns before running; prevents the "147 tests passing but testing nothing" failure mode

* **Shallow Test Detection** — Audit and gap-analysis agents now detect "page loads" tests that verify existence instead of feature behavior, and report them as higher priority than missing tests

* **Sandbox-Safe E2E Setup** — Proven patterns for running Playwright reliably in macOS Sandbox (Claude Code): writable browser cache (`PLAYWRIGHT_BROWSERS_PATH`), no `webServer` config (pre-start servers), API-first user registration (immune to React re-render issues), React hydration waits, strict mode handling, and increased timeouts. Every pattern battle-tested through real failures.

## Commands

| Command                                  | Description                                                                                                                                                          |
| ---------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/test-everything:test-audit`            | Analyze test coverage across all layers and produce a gap report including interaction verification, exhaustive element coverage, and desired outcome completeness   |
| `/test-everything:test-plan`             | Generate a phased testing strategy with user story discovery, outcome definitions, exhaustive crawl planning, and quality gates                                      |
| `/test-everything:test-scaffold <layer>` | Scaffold test infrastructure for a specific layer                                                                                                                    |
| `/test-everything:test-full-suite`       | Full workflow: audit → plan → scaffold → write → self-review → run → fix → quality review until green                                                                            |
| `/test-everything:test-mutation-loop`    | Run mutation testing on changed code and re-prompt per surviving mutant until the mutation-score threshold is met (mutation gates acceptance, coverage never does)   |
| `/test-everything:test-adequacy`         | Audit the auditor: mutation gate + falsifiability sampling + tautology/assertion-free detection + E2E negative controls (break the code, suite must go red)         |
| `/test-everything:test-property`         | Property-based testing: LLM states invariants, deterministic engine (Hypothesis/fast-check/proptest/gopter) falsifies; counterexamples become regression tests      |
| `/test-everything:test-coverage-loop`    | Test-generation refinement loop: coverage selects where to write, mutation score decides what survives; reward-hacking guardrails included                          |
| `/test-everything:test-e2e`              | Deterministic E2E specs from LLM exploration (accessibility tree / discover-then-freeze); healing is a diff for approval, never a silent self-edit                   |
| `/test-everything:test-flaky`            | Quarantine flaky tests with typed labels, tiered SLAs, and a ~1% weighted bucket cap — quarantined tests keep running and reporting; never disabled                  |
| `/test-everything:test-quality`          | Numeric five-metric scorecard: mutation 30%, assertion strength 25%, mock ratio 15%, tautology 15%, flaky 15%; <60 = decorative                                    |
| `/test-everything:test-differential`     | Old-vs-new / oracle-vs-impl divergence testing with golden masters; every divergence gets a bug-or-intended ruling                                                  |
| `/test-everything:test-fuzz`             | LLM-crafted adversarial seed corpora into deterministic fuzzers (atheris/Jazzer/cargo-fuzz/go-fuzz); findings become minimized deterministic regressions            |
| `/test-everything:test-ci-gate`          | Impact-based selective test execution + deterministic merge-queue gating; map misses trigger the full suite; nightly runs the slow guarantees                        |

### Scaffold Layers

| Layer           | What gets created                                                                                                                                                                     |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `unit`          | Vitest config, setup file, example test; Rust test module                                                                                                                             |
| `integration`   | MSW handlers + server (frontend); SQLx test fixtures (backend)                                                                                                                        |
| `component`     | React Testing Library tests for complex UI components                                                                                                                                 |
| `e2e`           | Playwright config, browser health fixture, user-story specs with desired outcome assessments, exhaustive interaction crawl, smoke/error/responsive/navigation tests, walkthrough test |
| `performance`   | k6 load, smoke, and stress test scripts                                                                                                                                               |
| `security`      | Semgrep config, dependabot, cargo/npm audit CI steps                                                                                                                                  |
| `accessibility` | axe-core + Playwright spec, Lighthouse CI config                                                                                                                                      |
| `ux`            | UX audit (Nielsen heuristics, dark patterns, feedback loops) + implement improvements                                                                                                 |
| `ui`            | UI visual audit (contrast, typography, spacing, consistency) + implement improvements                                                                                                 |
| `ci`            | GitHub Actions or GitLab CI pipeline with staged quality gates                                                                                                                        |

## Agents

| Agent                     | Trigger                                              | What it does                                                                                                                                                                                                                                                                                   |
| ------------------------- | ---------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **test-gap-analyzer**     | After implementing features or modifying code        | <span data-proof="suggestion" data-id="m1773844771186_6" data-by="ai:external-agent" data-kind="replace">Analyzes git changes, categorizes risk, identifies missing unit/integration/E2E tests, flags missing outcome assessments and uncovered interactive elements</span>                    |
| **test-quality-reviewer** | "Review my tests", flaky CI, test suite optimization | <span data-proof="suggestion" data-id="m1773844771184_5" data-by="ai:external-agent" data-kind="replace">Finds anti-patterns (no assertions, fire-and-forget clicks, CSS selectors, missing outcome tests), flakiness risks, architecture misalignment, and incomplete element coverage</span> |

## Skill

The **test-strategy** skill auto-activates when discussing testing strategy, types, architecture models, CI/CD testing, desired outcomes, exhaustive testing, or interaction crawling. Covers:

* All functional testing layers (unit, integration, E2E, component, smoke, regression, contract)

* Interaction verification and exhaustive crawling methodology

* Desired outcome assessment pattern (vs. acceptance criteria)

* Browser health monitoring

* Non-functional layers (performance, security, accessibility, UX, UI)

* Testing architecture models: Pyramid, Diamond, Trophy, Honeycomb

* Quality gates (pre-commit, PR, staging, release)

* CI/CD speed targets<span data-proof="suggestion" data-id="m1773844771181_4" data-by="ai:external-agent" data-kind="insert">
  Common failure modes — "page loads" tests, hardcoded waits, giving up with test.fixme, fire-and-forget clicks, CSS selectors, premature completion claims</span>

## Workflow

```
/test-everything:test-audit        ← understand current state
/test-everything:test-plan         ← approve strategy before writing
/test-everything:test-scaffold e2e ← scaffold infrastructure for a layer
/test-everything:test-full-suite   ← do everything end-to-end
```

## Stack

Tailored to: React + Vitest + Testing Library, Rust `#[test]`, Playwright, k6, Semgrep, axe-core

## Installation

```bash
claude --plugin-dir ~/.claude/plugins/test-everything
```

## What's New

### v0.12.0 — 13 AI-agent testing capabilities from field research

* **10 new commands**: `test-mutation-loop`, `test-adequacy`, `test-property`, `test-coverage-loop`, `test-e2e`, `test-flaky`, `test-quality`, `test-differential`, `test-fuzz`, `test-ci-gate`
* **Governing rule** added to the skill and README: LLMs author tests; deterministic tools decide pass/fail; no LLM in the merge gate; mutation score gates; coverage selects; negative controls required
* New skill reference: [enhancement-capabilities](skills/test-strategy/references/enhancement-capabilities.md) — the 13 mechanisms in detail
* Built from real AI-agent test-suite failure modes: high-coverage/low-strength suites, reward hacking in generation loops, silent E2E self-healing, flaky-test debt, mock-orchestration theater

### Changelog

* **0.12.0** — 13 AI-agent testing capabilities (mutation gating, adequacy audit, property/fuzz/differential testing, flaky quarantine, scorecard, selective CI gate)
* **0.11.0** — agent-team enforcement, argue-and-debate, sandbox-safe E2E, UX/UI audits

<!-- PROOF
{
  "version": 2,
  "marks": {
    "m1773844771186_6": {
      "kind": "replace",
      "by": "ai:external-agent",
      "createdAt": "2026-03-18T14:39:31.186Z",
      "range": {
        "from": 5450,
        "to": 5605
      },
      "content": "Analyzes git changes, categorizes risk, identifies missing unit/integration/E2E tests, flags missing outcome assessments and uncovered interactive elements; detects shallow existing tests that verify page loads but not features",
      "status": "pending"
    },
    "m1773844771184_5": {
      "kind": "replace",
      "by": "ai:external-agent",
      "createdAt": "2026-03-18T14:39:31.184Z",
      "range": {
        "from": 5692,
        "to": 5866
      },
      "content": "Runs 6 mandatory grep checks for banned patterns; finds anti-patterns (fire-and-forget clicks, CSS selectors, missing outcome tests), flakiness risks, architecture misalignment; issues PASS/FAIL verdict",
      "status": "pending"
    },
    "m1773844771181_4": {
      "kind": "insert",
      "by": "ai:external-agent",
      "createdAt": "2026-03-18T14:39:31.181Z",
      "range": {
        "from": 6534,
        "to": 6688
      },
      "content": "\nCommon failure modes — \"page loads\" tests, hardcoded waits, giving up with test.fixme, fire-and-forget clicks, CSS selectors, premature completion claims",
      "status": "pending"
    }
  }
}
-->

<!-- PROOF:END -->
