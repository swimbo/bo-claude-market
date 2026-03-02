---
name: scaffold
description: Scaffold test files, configurations, and CI pipeline definitions for a specific testing layer
argument-hint: "<layer> [path-to-project] — layers: unit, integration, e2e, performance, security, accessibility, ci"
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash"]
---

# Test Scaffolding

Create test infrastructure files for a specific testing layer.

## Instructions

Parse the argument to determine which layer to scaffold. If no layer specified, ask the user.

Valid layers: `unit`, `integration`, `e2e`, `performance`, `security`, `accessibility`, `ci`

### Before Scaffolding

1. Detect project type and existing test infrastructure
2. Check what already exists — never overwrite existing test configs
3. Identify the correct tools based on the preferred stack

### Layer: `unit`

**Frontend (React + Vitest)**:

* Create `vitest.config.ts` if missing (jsdom environment, coverage config, path aliases)

* Create `src/test/setup.ts` with Testing Library matchers

* Create example test file `src/lib/__tests__/example.test.ts`

* Add test scripts to `package.json`: `"test"`, `"test:watch"`, `"test:coverage"`

* Install deps if missing: `vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom`

**Backend (Rust)**:

* Add test module template to an existing source file if no tests exist

* Create `tests/` integration test directory if missing

* Add `dev-dependencies` to `Cargo.toml` if missing (tokio test-util, etc.)

### Layer: `integration`

**Frontend**:

* Set up MSW (Mock Service Worker) if not present: `src/mocks/handlers.ts`, `src/mocks/server.ts`

* Create example integration test: `src/components/__tests__/ExamplePage.test.tsx`

* Configure MSW in Vitest setup file

**Backend (Rust + SQLx)**:

* Create test fixtures or factory functions in `tests/common/mod.rs`

* Create example API integration test in `tests/api/`

* Configure test database URL in `.env.test`

### Layer: `e2e`

**Playwright**:

* Create `playwright.config.ts` with:

  * Multi-browser projects (Chromium, Firefox, WebKit)

  * Base URL from env var

  * Screenshot on failure

  * HTML reporter

  * Reasonable timeouts

* Create `e2e/` directory structure:

  * `e2e/auth.spec.ts` — login/logout flow template

  * `e2e/fixtures/` — test data and auth state

* Add scripts to `package.json`: `"test:e2e"`, `"test:e2e:ui"`

* Install: `@playwright/test` + browsers

### Layer: `performance`

**k6**:

* Create `k6/` directory

* Create `k6/load-test.js` — basic load test template with stages and thresholds

* Create `k6/smoke-test.js` — quick smoke test for post-deployment

* Create `k6/stress-test.js` — stress test finding breaking points

* Include common thresholds: p95 < 500ms, error rate < 1%

* Add npm script: `"test:perf"`

### Layer: `security`

* Create `.semgrep.yml` or `semgrepconfig` with recommended rules

* Add `cargo audit` step to CI if Rust project

* Add `npm audit` / Snyk check to CI

* Create `.github/dependabot.yml` if using GitHub

* Add secret scanning config if available

### Layer: `accessibility`

* Install `@axe-core/playwright` if Playwright exists

* Create `e2e/accessibility.spec.ts` with axe-core integration

* Add Lighthouse CI config (`lighthouserc.json`) for CI scoring

* Create example accessibility test for homepage

### Layer: `ci`

Generate CI pipeline configuration:

**GitHub Actions** (`.github/workflows/test.yml`):

```yaml
# Full testing pipeline with stages:
# 1. Lint + typecheck + SAST (<5 min)
# 2. Unit + integration tests (<15 min)
# 3. E2E tests (<30 min)
# 4. Security + performance (nightly)
```

**GitLab CI** (`.gitlab-ci.yml`):

```yaml
# Equivalent stages for GitLab
```

Detect which CI system the project uses (look for `.github/`, `.gitlab-ci.yml`, `Jenkinsfile`) and generate the appropriate config.

### After Scaffolding

1. List all files created
2. Show next steps (what to customize, what to run first)
3. Note any manual steps needed (e.g., "Add test database URL to .env.test")

### Tips

* Always check existing files first — append to configs, don't overwrite

* Use the project's existing code style and patterns

* Include helpful comments in generated files explaining what each section does

* Reference the testing-strategy skill for deeper context on any testing type