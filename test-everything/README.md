# test-everything

Comprehensive testing toolkit for Claude Code. Audit coverage gaps, plan testing strategies, scaffold test infrastructure, and review test quality across all testing layers.

## Features

* **Audit** — Scan a project and identify testing gaps against best practices, including interaction verification quality and selector usage

* **Plan** — Generate a phased testing implementation strategy tailored to your project

* **Scaffold** — Create test files, configs, and CI pipelines for any testing layer

* **Interaction Verification** — Generated E2E tests pair every interaction with an outcome assertion, catching broken buttons and failing workflows

* **Browser Health Monitoring** — Shared Playwright fixture that automatically fails tests on console errors, uncaught exceptions, and failed API requests

* **Gap Analysis** — Proactive agent that identifies missing tests after code changes

* **UX Quality Audit** — Evaluate against Nielsen's heuristics, detect dark patterns, check feedback loops and error messages, then implement improvements

* **UI Visual Quality Audit** — Check color contrast (WCAG), typography, spacing consistency, component uniformity, and visual hierarchy, then fix issues

* **Quality Review** — Agent that finds anti-patterns (including fire-and-forget clicks and poor selector usage), flakiness risks, and architecture issues in tests

## Stack

Tailored to: React + Vitest, Rust `#[test]`, Playwright, k6, Semgrep, axe-core

## Commands

| Command                             | Description                                                                                     |
| ----------------------------------- | ----------------------------------------------------------------------------------------------- |
| `/test-everything:test-audit`            | Analyze test coverage and produce gap report                                                    |
| `/test-everything:test-plan`             | Generate phased testing strategy                                                                |
| `/test-everything:test-scaffold <layer>` | Scaffold test infrastructure (unit, integration, e2e, performance, security, accessibility, ux, ui, ci) |
| `/test-everything:test-full-suite`       | Full workflow: audit, plan, scaffold, write, run, fix until green                               |

## Agents

| Agent                     | Trigger                                                              |
| ------------------------- | -------------------------------------------------------------------- |
| **test-gap-analyzer**     | Proactively after implementing features or modifying code            |
| **test-quality-reviewer** | When asked to review tests, find flaky tests, or optimize test suite |

## Skill

The **test-strategy** skill auto-activates when discussing testing types, strategy, architecture models, or CI/CD testing.

## Installation

```bash
claude --plugin-dir ~/.claude/plugins/test-everything
```