# Proven E2E Patterns for Sandbox Environments

This document captures battle-tested patterns for running Playwright E2E tests reliably inside macOS Sandbox (Claude Code) and similar restricted environments. Every pattern here was discovered through real failures and verified through successful runs.

## The Problem

Claude Code runs inside macOS Sandbox, which blocks:
- `nice(5)` syscalls (used by many process managers)
- Writing to `~/Library/Caches/ms-playwright/` (Playwright's default browser cache)
- Starting child processes via `config.webServer` in Playwright configs (timeouts)
- Certain network operations and file permission changes

These restrictions cause E2E tests to fail in ways that look like test bugs but are actually environment bugs. The failures are consistent and predictable — and so are the fixes.

## Mandatory E2E Environment Setup (Phase 0)

Before writing or running ANY E2E test, you MUST complete these steps. Skip none of them.

### Step 1: Install Playwright Browsers to a Writable Path

The default Playwright browser cache (`~/Library/Caches/ms-playwright/`) is blocked by sandbox. Always use a project-local or `/tmp` path.

```bash
# Option A: Project-local (persists across sessions, recommended)
PLAYWRIGHT_BROWSERS_PATH=.playwright-browsers npx playwright install chromium

# Option B: /tmp (always writable, lost on reboot)
PLAYWRIGHT_BROWSERS_PATH=/tmp/pw-browsers npx playwright install chromium
```

**CRITICAL**: Add `.playwright-browsers/` to `.gitignore` if using Option A.

**CRITICAL**: Set `PLAYWRIGHT_BROWSERS_PATH` in ALL npm scripts that run Playwright:
```json
{
  "scripts": {
    "test:e2e": "PLAYWRIGHT_BROWSERS_PATH=.playwright-browsers playwright test",
    "test:e2e:ui": "PLAYWRIGHT_BROWSERS_PATH=.playwright-browsers playwright test --ui",
    "test:e2e:headed": "PLAYWRIGHT_BROWSERS_PATH=.playwright-browsers playwright test --headed"
  }
}
```

**Why**: Without this, Playwright will try to use the default cache, get `EPERM`, and either fail to install or fail to launch. The ICU data error (`Could not find ICU data`) is also caused by this.

### Step 2: Do NOT Use `config.webServer` — Use Pre-Running Servers

Playwright's `webServer` config starts dev servers as child processes. In sandbox, this reliably times out because:
- `nice()` fails (process priority)
- Server startup takes longer than the `timeout` allows
- Port detection races with server readiness

**WRONG — will timeout in sandbox:**
```typescript
// playwright.config.ts — DO NOT USE THIS
export default defineConfig({
  webServer: {
    command: 'npm run dev',
    port: 3000,
    timeout: 15000,
  },
});
```

**RIGHT — pre-start servers, then run tests:**
```typescript
// playwright.config.ts — SANDBOX-SAFE
export default defineConfig({
  testDir: './tests',
  timeout: 60000,
  expect: { timeout: 10000 },
  fullyParallel: false,
  retries: 1,
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:5173',
    screenshot: 'only-on-failure',
    trace: 'on-first-retry',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
  ],
  // NO webServer block — servers must be running before tests start
});
```

**The startup script** that replaces `webServer`:
```bash
#!/bin/bash
# e2e/run-e2e.sh — Start servers, wait for ready, run tests, cleanup

set -e

# Detect if servers are already running
check_server() {
  curl -sf "$1" > /dev/null 2>&1
}

FRONTEND_URL="${BASE_URL:-http://localhost:5173}"
BACKEND_URL="${API_URL:-http://localhost:3000}"
STARTED_SERVERS=false

if ! check_server "$FRONTEND_URL"; then
  echo "Starting dev servers..."
  # Start in background — adjust these commands per project
  cd "$(dirname "$0")/.."
  npm run dev > /tmp/e2e-dev-server.log 2>&1 &
  DEV_PID=$!
  STARTED_SERVERS=true

  # Wait for servers to be ready (poll, don't sleep)
  echo "Waiting for servers..."
  for i in $(seq 1 30); do
    if check_server "$FRONTEND_URL" && check_server "$BACKEND_URL/api/health" 2>/dev/null; then
      echo "Servers ready!"
      break
    fi
    if [ $i -eq 30 ]; then
      echo "ERROR: Servers failed to start within 30 seconds"
      kill $DEV_PID 2>/dev/null
      exit 1
    fi
    sleep 1
  done
fi

# Run Playwright tests
PLAYWRIGHT_BROWSERS_PATH="${PLAYWRIGHT_BROWSERS_PATH:-.playwright-browsers}" \
  npx playwright test "$@"
TEST_EXIT=$?

# Cleanup only if we started the servers
if [ "$STARTED_SERVERS" = true ]; then
  kill $DEV_PID 2>/dev/null
fi

exit $TEST_EXIT
```

### Step 3: Use API-First User Registration

NEVER register test users through the UI. React form fills get lost during re-renders, especially in fresh contexts. Always register via API, then use the browser for testing features.

**WRONG — form fills lost during React re-renders:**
```typescript
async function registerUser(page: Page) {
  await page.goto('/register');
  await page.getByLabel('Email').fill(email);      // ← gets lost during re-render
  await page.getByLabel('Password').fill(password); // ← gets lost during re-render
  await page.getByRole('button', { name: 'Register' }).click();
  await page.waitForURL('/dashboard');              // ← times out
}
```

**RIGHT — register via API, authenticate via stored state:**
```typescript
import { test as base, expect } from '@playwright/test';
import type { Page } from '@playwright/test';

// Auth helper that ALWAYS works
async function apiRegisterAndLogin(
  baseURL: string
): Promise<{ email: string; password: string; token: string }> {
  const email = `e2e-${crypto.randomUUID().slice(0, 8)}@test.com`;
  const password = 'TestPass123!';

  // Register via API — never fails due to UI issues
  const regResponse = await fetch(`${baseURL}/api/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password, fullName: 'E2E Test User' }),
  });
  if (!regResponse.ok && regResponse.status !== 409) {
    throw new Error(`Registration failed: ${regResponse.status}`);
  }

  // Login via API to get token
  const loginResponse = await fetch(`${baseURL}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });
  if (!loginResponse.ok) {
    throw new Error(`Login failed: ${loginResponse.status}`);
  }
  const { token } = await loginResponse.json();

  return { email, password, token };
}

// Fixture that provides an authenticated page
export const test = base.extend<{ authedPage: Page }>({
  authedPage: async ({ page, baseURL }, use) => {
    const { token } = await apiRegisterAndLogin(baseURL!);

    // Inject auth token into browser storage BEFORE navigating
    await page.goto(baseURL!);
    await page.evaluate((t) => {
      localStorage.setItem('token', t);
      // Also set any other auth state your app expects
    }, token);

    await page.reload();
    await use(page);
  },
});

export { expect } from '@playwright/test';
```

### Step 4: Use Fresh Browser Contexts for Test Isolation

Auth state in localStorage bleeds between tests in the same browser context. Use fresh contexts for tests that need clean state.

```typescript
test('login with invalid password shows error', async ({ browser }) => {
  // Fresh context — no auth state from previous tests
  const context = await browser.newContext();
  const page = await context.newPage();

  try {
    await page.goto('/login');
    await page.getByLabel('Email').fill('user@test.com');
    await page.getByLabel('Password').fill('WrongPassword!');
    await page.getByRole('button', { name: /sign in/i }).click();
    await expect(page.getByText(/invalid|incorrect|wrong/i)).toBeVisible();
  } finally {
    await context.close();
  }
});
```

### Step 5: Wait for React Hydration Before Interacting

React apps re-render during hydration. Forms filled during re-renders get cleared. Always wait for a stable interactive element before filling forms.

**WRONG:**
```typescript
await page.goto('/login');
await page.waitForSelector('#email');  // ← resolves before hydration
await page.locator('#email').fill(email);  // ← lost during re-render
```

**RIGHT:**
```typescript
await page.goto('/login');
// Wait for a SPECIFIC interactive element that proves React is done rendering
await expect(page.getByRole('button', { name: /sign in/i })).toBeVisible();
// NOW interact with the form
await page.getByLabel('Email').fill(email);
await expect(page.getByLabel('Email')).toHaveValue(email); // Verify fill stuck
```

### Step 6: Handle Strict Mode Violations

When Playwright finds multiple elements matching a locator, it throws a strict mode error. Always use `.first()` or more specific locators.

```typescript
// WRONG — fails if filename appears in both a banner and a list item
await expect(page.locator(`text=${filename}`)).toBeVisible();

// RIGHT — target the first match, or use a more specific locator
await expect(page.getByText(filename).first()).toBeVisible();
// OR: scope to a specific container
await expect(
  page.getByRole('list').getByText(filename)
).toBeVisible();
```

### Step 7: Use Increased Timeouts

Sandbox environments are slower. Default 30s timeouts are insufficient for tests that register users, navigate, and interact with APIs.

```typescript
// playwright.config.ts
export default defineConfig({
  timeout: 60000,       // 60s per test (up from 30s default)
  expect: { timeout: 10000 },  // 10s for assertions (up from 5s)
  retries: 1,           // One retry for transient failures
});
```

## E2E Server Management Decision Tree

```
Is the dev server already running?
├── YES → Run tests directly (use baseURL matching the running server)
│         PLAYWRIGHT_BROWSERS_PATH=.playwright-browsers npx playwright test
│
└── NO → Start server(s) in background, wait for ready, then run tests
          DO NOT use config.webServer (times out in sandbox)
          Use the run-e2e.sh script pattern above
```

## Debugging E2E Failures

When a test fails, diagnose in this order:

1. **Check the error message** — Is it `EPERM`? → Browser path issue. Is it `Timed out`? → Server not running or React not hydrated.
2. **Check screenshots** — Playwright captures on failure. Are form fields empty? → React re-render issue. Is the page blank? → Server not responding.
3. **Check the Playwright trace** — `npx playwright show-trace test-results/*/trace.zip` shows every action and its timing.
4. **Use Playwright MCP for live debugging** — Navigate the running app, take snapshots, click elements interactively to find the real issue.
5. **Never use `waitForTimeout` as a fix** — If timing is the issue, use proper waits (`toBeVisible`, `waitForResponse`, `waitForURL`).
6. **Never use `test.fixme` as a fix** — If a test is hard to write, the app probably has a bug. Document it and fix it.

## Checklist: Before Running E2E Tests

- [ ] `PLAYWRIGHT_BROWSERS_PATH` set in environment or npm scripts
- [ ] Playwright browsers installed to writable location
- [ ] `.playwright-browsers/` in `.gitignore`
- [ ] Dev server(s) running and responding (verified with curl)
- [ ] No `webServer` block in `playwright.config.ts`
- [ ] `timeout: 60000` in playwright config
- [ ] Auth helpers use API registration, not UI forms
- [ ] All test files import from `./fixtures/browser-health`, not `@playwright/test`
- [ ] File uploads tested via `waitForEvent('filechooser')`, not `page.request.post()`
- [ ] Form submissions tested via real `fill()` + `click()`, not API calls
- [ ] Every interactive element tested through the rendered DOM, not programmatic shortcuts

## Case Study: The File Upload That Passed Tests But Never Worked (failure4)

This is the canonical example of API-shortcut testing — the most dangerous E2E anti-pattern, because it produces a green suite while the feature is completely broken.

### What Happened

A file upload feature on a Documents page used a `<label>` wrapping a hidden `<input type="file">`. The E2E test for upload used `page.request.post('/api/documents/upload', formData)` — testing the upload API directly. The test passed.

The actual "Select Files" button was completely broken. The `hidden` Tailwind class used `display: none`, which prevented the `<label>` click from reaching the `<input>`. The `onChange` handler never fired. No file was ever uploaded through the browser.

The user discovered this manually after the test suite reported full coverage.

### The Debugging Spiral

Once discovered, Claude attempted 5 fixes over ~20 minutes:

1. Changed `hidden` to `sr-only` — still broken (input was clipped, onChange didn't fire)
2. Replaced `<label>` with `<button>` + `ref.click()` — still broken (React re-render cleared the FileList)
3. Moved input to `position: absolute` off-screen — still broken
4. Added native `input.onchange` listener — still broken (stale closure, files cleared before mutation read them)
5. Added `setTimeout(() => { input.value = ""; }, 100)` to delay clearing — **finally worked**

The root cause was that `input.value = ""` was clearing the FileList synchronously before the React mutation could read it. This bug would have been caught immediately if the E2E test had clicked the real button.

### The Root Cause

The E2E test used the API-shortcut pattern:

```typescript
// WHAT THE TEST DID (wrong — API shortcut)
const response = await page.request.post('/api/documents/upload', {
  multipart: { file: fs.createReadStream('test.pdf') }
});
expect(response.ok()).toBeTruthy();
```

This tested that the upload API worked. It told us nothing about:
- Whether the "Select Files" button was clickable
- Whether the file input's `onChange` handler fired
- Whether the `hidden` class prevented label click propagation
- Whether `input.value = ""` cleared files before the mutation read them

### What The Test Should Have Done

```typescript
// WHAT THE TEST SHOULD HAVE DONE (right — real user interaction)
test('user can upload a document via Select Files button', async ({ authedPage: page }) => {
  await page.goto('/documents');

  // Click the REAL button — tests the full click → input → onChange chain
  const fileChooserPromise = page.waitForEvent('filechooser');
  await page.getByRole('button', { name: /select files/i }).click();
  const fileChooser = await fileChooserPromise;
  await fileChooser.setFiles('test-fixtures/sample.pdf');

  // Verify the upload completed through the UI
  await expect(page.getByText('sample.pdf')).toBeVisible();
});
```

This test would have caught the bug immediately — the `fileChooser` event would never fire because the hidden input wasn't reachable.

### The Lesson

**API-first is correct for test SETUP (auth, data seeding). API-first is disastrous for test VERIFICATION.**

The test should exercise the same path the user takes. If the user clicks a button, the test clicks the button. If the user drags a file, the test drags a file. If the user fills a form and clicks submit, the test fills the form and clicks submit.

Every API shortcut in a feature test is a lie about whether the feature works.
