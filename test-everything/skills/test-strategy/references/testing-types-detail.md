# Testing Types — Detailed Reference

## Functional Testing Types

### Unit Testing

**Purpose**: Verify individual functions, methods, and classes work correctly in isolation.

**Characteristics**:

* Dependencies mocked/stubbed

* Milliseconds per test

* Developers write them alongside production code

* Highest ROI for pure business logic, calculations, transformations

**What to unit test**:

* Business logic and calculations

* Data transformations and parsing

* Validation rules

* State management reducers/selectors

* Utility functions and helpers

**What NOT to unit test**:

* Simple getters/setters with no logic

* Framework boilerplate (React component renders with no logic)

* Third-party library internals

* Database queries (use integration tests)

**Stack-specific guidance**:

*Vitest (Frontend)*:

```typescript
import { describe, it, expect } from 'vitest'
import { calculateTotal } from './pricing'

describe('calculateTotal', () => {
  it('applies discount for orders over $100', () => {
    expect(calculateTotal(150, 0.1)).toBe(135)
  })
})
```

*Rust (Backend)*:

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_calculate_total_with_discount() {
        assert_eq!(calculate_total(150.0, 0.1), 135.0);
    }
}
```

### Integration Testing

**Purpose**: Verify that modules work correctly together — database queries return expected data, API endpoints handle requests properly, services communicate correctly.

**Characteristics**:

* Uses real dependencies (databases, filesystems) or realistic fakes

* Seconds per test

* Highest confidence-per-test of any automated test type

* Catches the most real-world bugs

**What to integration test**:

* API endpoint request/response cycles

* Database queries and transactions

* Authentication/authorization flows

* External service integrations (with mocked HTTP)

* Message queue producers/consumers

* File upload/download workflows

**Stack-specific guidance**:

*React Testing Library (Frontend)*:

```typescript
import { render, screen, waitFor } from '@testing-library/react'
import { UserProfile } from './UserProfile'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

it('loads and displays user data', async () => {
  const queryClient = new QueryClient()
  render(
    <QueryClientProvider client={queryClient}>
      <UserProfile userId="123" />
    </QueryClientProvider>
  )
  await waitFor(() => {
    expect(screen.getByText('John Doe')).toBeInTheDocument()
  })
})
```

*SQLx (Backend)*:

```rust
#[sqlx::test]
async fn test_create_user(pool: PgPool) {
    let user = create_user(&pool, "test@example.com", "Test User")
        .await
        .unwrap();
    assert_eq!(user.email, "test@example.com");
}
```

### End-to-End (E2E) Testing

**Purpose**: Validate complete user workflows through the real UI, ensuring the entire system works together.

**Characteristics**:

* Slowest but highest-fidelity tests

* Simulates real user behavior

* Tests the full stack: UI → API → Database → Response

* Keep to 10-20 critical journeys maximum

**What to E2E test** (critical user journeys):

* Sign up / login / logout

* Core business workflow (the main thing users do)

* Payment/checkout flow

* Search and filtering

* Data creation, editing, deletion

* Permission-based access (admin vs. regular user)

* Error recovery (network failure, invalid input)

**Playwright example**:

```typescript
import { test, expect } from '@playwright/test'

test('user can create and publish a post', async ({ page }) => {
  await page.goto('/login')
  await page.fill('[name="email"]', 'test@example.com')
  await page.fill('[name="password"]', 'password123')
  await page.click('button[type="submit"]')

  await page.click('text=New Post')
  await page.fill('[name="title"]', 'My Test Post')
  await page.fill('[name="body"]', 'Post content here')
  await page.click('text=Publish')

  await expect(page.locator('.toast-success')).toBeVisible()
  await expect(page).toHaveURL(/\/posts\/\d+/)
})
```

### Regression Testing

**Purpose**: Catch unintended side effects from new changes.

**Strategy**:

* Automate the full test suite (unit + integration + key E2E)

* Run on every PR and before every release

* Track which tests fail most often — those are your most valuable regression tests

* When a bug is found in production, write a regression test FIRST before fixing

### Smoke Testing

**Purpose**: Quick verification that a deployment didn't break core functionality.

**Characteristics**:

* Run immediately after deployment (staging and production)

* <5 minutes execution time

* Tests only critical paths: login works, homepage loads, core API responds

* If smoke tests fail, roll back immediately

### Contract Testing

**Purpose**: Ensure API changes don't break consumers without running full integration.

**When to use**: Microservices, separate frontend/backend teams, public APIs.

**Tools**: Pact (consumer-driven contracts)

### Component Testing

**Purpose**: Test UI components in isolation with realistic data and interactions.

**Tools**: Testing Library + Vitest, Storybook interaction tests

## Non-Functional Testing Types

### Performance Testing — Subtypes

**Load Testing**: Simulate expected concurrent users. Establish baselines for response times (p50, p95, p99). Alert when response times degrade beyond threshold.

**Stress Testing**: Push beyond expected load to find breaking points. Identify which component fails first (database, API server, network). Document system limits.

**Spike Testing**: Sudden burst of traffic (e.g., flash sale, viral content). Verify auto-scaling triggers correctly. Measure recovery time.

**Soak Testing**: Run at moderate load for extended periods (hours/days). Detect memory leaks, connection pool exhaustion, disk space growth.

**k6 example**:

```javascript
import http from 'k6/http'
import { check, sleep } from 'k6'

export const options = {
  stages: [
    { duration: '2m', target: 100 },  // ramp up
    { duration: '5m', target: 100 },  // steady
    { duration: '2m', target: 0 },    // ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% under 500ms
    http_req_failed: ['rate<0.01'],    // <1% error rate
  },
}

export default function () {
  const res = http.get('http://localhost:3000/api/v1/users')
  check(res, { 'status is 200': (r) => r.status === 200 })
  sleep(1)
}
```

### Security Testing — Subtypes

**SAST (Static Analysis)**:

* Run on every commit in CI

* Tools: Semgrep (multi-language), cargo-audit (Rust), eslint-plugin-security (JS)

* Catches: SQL injection patterns, XSS, hardcoded secrets, unsafe deserialization

**Dependency Scanning**:

* Run on every PR

* Tools: Snyk, Trivy, Dependabot, npm audit, cargo-audit

* Catches: Known CVEs in third-party packages

* Action: Auto-create PRs for upgrades, block merges for critical vulns

**DAST (Dynamic Analysis)**:

* Run against staging environment

* Tools: OWASP ZAP

* Catches: XSS, CSRF, insecure headers, authentication bypasses

* Schedule: Weekly automated scans + before releases

**Penetration Testing**:

* Quarterly or before major releases

* Usually requires external security experts

* Produces actionable findings with severity ratings

* Track remediation timelines

### Accessibility Testing

**Automated checks** (run in CI):

* Missing alt text, incorrect heading hierarchy

* Color contrast failures

* Missing form labels

* ARIA attribute errors

* Tools: axe-core (via @axe-core/playwright), Lighthouse CI

**Manual checks** (quarterly):

* Full keyboard navigation test

* Screen reader walkthrough (VoiceOver, NVDA)

* Focus management and tab order

* Dynamic content announcements

* Form error handling with assistive technology

**Playwright + axe-core example**:

```typescript
import { test, expect } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'

test('homepage meets accessibility standards', async ({ page }) => {
  await page.goto('/')
  const results = await new AxeBuilder({ page }).analyze()
  expect(results.violations).toEqual([])
})
```

### Compatibility Testing

**Browser matrix** (Playwright handles this natively):

* Chromium, Firefox, WebKit (Safari)

* Configure in `playwright.config.ts` with multiple projects

**Device testing**:

* Use Playwright's device emulation for common viewports

* BrowserStack/Sauce Labs for real device testing when needed

### Resilience Testing

**Chaos engineering principles**:

* Start with the smallest blast radius

* Define steady state behavior first

* Run experiments in staging before production

* Automate rollback

**What to test**:

* Database connection loss

* External API timeouts

* Disk full scenarios

* Memory pressure

* Network partitions

## Testing Methods

### Static Testing

* Code reviews, linting (ESLint, clippy), type checking (TypeScript strict mode, Rust compiler)

* SAST security scanning

* Run on every commit, fail fast

### Exploratory Testing

* Unscripted, human-driven investigation

* Best for new features, complex UX flows, edge cases

* Cannot and should not be automated

* Schedule dedicated sessions (e.g., 1 hour per sprint)

### Property-Based Testing

* Generate random inputs and verify properties hold

* Excellent for parsers, serializers, mathematical functions

* Tools: fast-check (JS), proptest (Rust), Hypothesis (Python)

```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn parse_roundtrip(s in "\\PC*") {
        let parsed = parse(&s);
        if let Ok(value) = parsed {
            assert_eq!(format!("{}", value), s);
        }
    }
}
```