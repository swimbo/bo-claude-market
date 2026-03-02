---
name: test-strategy
description: This skill should be used when the user asks about "testing strategy", "what tests to write", "testing types", "test pyramid", "test diamond", "testing trophy", "what should I test", "testing architecture", "quality gates", "CI/CD testing", "shift-left testing", "test coverage gaps", "performance testing", "security testing", "accessibility testing", "E2E testing", "integration testing", "how to test", "test automation", "testing best practices", "test plan", "test coverage", or discusses how to plan, structure, or improve testing in a project. Provides comprehensive knowledge of all software testing types, architecture models, and implementation strategies tailored to React + Vitest, Rust, Playwright, and k6.
version: 0.1.0
---

# Testing Strategy Knowledge Base

Comprehensive testing knowledge covering all testing types, architecture models, quality gates, and implementation strategies. Tailored to projects using React + Vitest (frontend), Rust `#[test]` (backend), Playwright (E2E), and k6 (performance).

## Testing Classification

Testing divides along three axes:

| Axis     | Categories                                                       |
| -------- | ---------------------------------------------------------------- |
| **What** | Functional (correctness) vs. Non-Functional (quality attributes) |
| **How**  | Manual vs. Automated                                             |
| **When** | Static (no execution) vs. Dynamic (running code)                 |

## Functional Testing Layers

### Unit Testing

* **Scope**: Individual functions, methods, classes in isolation

* **Speed**: Milliseconds | **Run**: Every commit

* **Tools**: Vitest (frontend), Rust `#[test]` (backend)

* **Target**: 80%+ line coverage on business logic

### Integration Testing

* **Scope**: Module interactions — DB queries, API calls, service boundaries

* **Speed**: Seconds | **Run**: Every PR/merge

* **Tools**: Testcontainers, supertest, SQLx test fixtures, React Testing Library

* **Target**: All critical paths covered

### End-to-End (E2E) Testing

* **Scope**: Full user workflows through real UI

* **Speed**: Seconds to minutes | **Run**: Before releases, on staging

* **Tools**: Playwright (multi-browser)

* **Target**: Top 10-20 critical user journeys

### Other Functional Types

* **Regression**: Re-run full suite after changes — automate heavily

* **Smoke**: "Does the build work?" — run immediately after deployment

* **Sanity**: Targeted check after a narrow fix

* **Contract**: API agreements between services (Pact)

* **Component**: UI components in isolation (Testing Library, Storybook)

* **Acceptance (UAT)**: Business requirement validation with stakeholders

## Non-Functional Testing

### Performance Testing

| Subtype | Purpose               | Tool |
| ------- | --------------------- | ---- |
| Load    | Expected user volume  | k6   |
| Stress  | Where does it break?  | k6   |
| Spike   | Sudden traffic surges | k6   |
| Soak    | Degradation over time | k6   |

### Security Testing

| Subtype             | Purpose            | Tool                                  |
| ------------------- | ------------------ | ------------------------------------- |
| SAST                | Scan source code   | Semgrep, cargo-audit                  |
| Dependency scanning | Vuln in packages   | Snyk, Trivy, Dependabot               |
| Secret scanning     | Hardcoded creds    | git-secrets, GitHub Advanced Security |
| DAST                | Attack running app | OWASP ZAP                             |
| Penetration         | Simulated attacks  | Manual / specialized tools            |

### Accessibility Testing

* **Standard**: WCAG 2.1/2.2 (target AA level)

* **Automated**: axe-core, Lighthouse, Pa11y

* **Manual**: Keyboard navigation, screen reader testing, color contrast

* **Run**: Automated in CI + quarterly manual audit

### Other Non-Functional Types

* **Compatibility**: Cross-browser (Playwright multi-browser), cross-device (BrowserStack)

* **Resilience**: Chaos engineering, failover, disaster recovery

* **Localization**: Language, currency, date formats

* **Compliance**: GDPR, HIPAA, SOC 2, PCI-DSS

## Testing Architecture Models

Choose based on project type:

| Project Type                   | Model                    | Distribution                            |
| ------------------------------ | ------------------------ | --------------------------------------- |
| Library / package              | **Pyramid**              | Many unit, few integration, minimal E2E |
| Monolithic web app             | **Pyramid or Diamond**   | Balanced unit + integration             |
| Frontend SPA                   | **Trophy**               | Heavy integration + static analysis     |
| Microservices                  | **Diamond or Honeycomb** | Heavy integration                       |
| Full-stack (React + Rust + PG) | **Diamond**              | Integration-heavy, good E2E coverage    |

### Recommended Stack Distribution

For a typical React + Rust + PostgreSQL project:

| Layer                               | Target                | Automation                  |
| ----------------------------------- | --------------------- | --------------------------- |
| Static analysis (lint, types, SAST) | 100% of code          | Fully automated             |
| Unit tests                          | 80%+ business logic   | Fully automated             |
| Integration tests                   | All critical paths    | Fully automated             |
| Component tests                     | Key UI components     | Fully automated             |
| E2E tests                           | Top 15 user journeys  | Fully automated             |
| Performance                         | Key API endpoints     | Automated in CI             |
| Security                            | All code + deps       | Automated + periodic manual |
| Accessibility                       | All user-facing pages | Automated + manual audit    |

## Quality Gates

| Gate       | When              | Must Pass                                        |
| ---------- | ----------------- | ------------------------------------------------ |
| Pre-commit | Before push       | Lint, type-check, unit tests                     |
| PR/MR      | Before merge      | All unit + integration, SAST, coverage threshold |
| Staging    | Before production | E2E smoke suite, performance baseline            |
| Release    | Before go-live    | Full regression, security scan, accessibility    |

## CI/CD Pipeline Speed Targets

| Stage             | Duration | Tests                            |
| ----------------- | -------- | -------------------------------- |
| Pre-commit hooks  | <10s     | Format, lint                     |
| Commit stage      | <5min    | Unit tests, type-check, SAST     |
| Integration stage | <15min   | Integration, contract tests      |
| E2E stage         | <30min   | Critical path E2E, accessibility |
| Nightly           | 1-2hr    | Full regression, perf, security  |

## Manual vs. Automated Decision

**Automate**: Regression, unit, integration, smoke, performance, security scans, accessibility scans
**Keep manual**: Exploratory testing, usability, visual/aesthetic review, UAT, accessibility with real users

**Automate when**: Runs >3 times, data-driven, critical path, needs CI/CD
**Keep manual when**: Requires human judgment, run rarely, unstable requirements, exploratory

## Additional Resources

### Reference Files

For detailed information on each testing type, tools, and implementation:

* **`references/testing-types-detail.md`** — Complete breakdown of all testing types with examples, tools, and when to use each

* **`references/implementation-roadmap.md`** — Phased 10-week implementation plan with checklists for building comprehensive testing from scratch