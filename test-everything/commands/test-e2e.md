---
name: test-e2e
description: Deterministic E2E tests from LLM exploration — discover flows via exploratory browser automation or the accessibility tree, then FREEZE them as deterministic Playwright specs. Healing is a proposed diff for human approval, never a silent self-edit.
argument-hint: "[base-url or dev-server-command]"
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "Agent", "WebSearch"]
---

# E2E: Deterministic Specs from LLM Exploration

Exploration is the probe; the frozen script is the asset that runs in CI. **Never let a live-LLM session be the regression test.**

## Instructions

### Step 1: Explore (choose one mode)

- **Accessibility-tree mode**: drive the app via the accessibility tree — roles, accessible names, states. This is the same model as accessible selectors (`getByRole`), so exploration naturally produces selector-compatible observations. Verify each interaction's outcome before the next.
- **Discover-then-freeze mode**: use exploratory browser automation (LLM-driven discovery — wander flows, open hidden tabs/modals/dropdowns, try edge states and empty states) to map the flow.

### Step 2: Freeze

Export a deterministic Playwright script:

- `npx playwright codegen` during exploration, or
- hand-freeze the discovered steps into a spec with accessible locators (`getByRole` > `getByLabel` > `getByText` > `data-testid` last resort).

Apply the plugin's existing E2E doctrine: every interaction paired with an outcome assertion within ~3 lines; no API shortcuts for feature actions (setup/seeding only); browser-health fixture (pageerror / console.error / 4xx-5xx fail the test); sandbox-safe setup per `references/e2e-sandbox-patterns.md`.

### Step 3: Healing Rules

When a frozen E2E test breaks on a legitimate UI change:

- The fix is a **PROPOSAL** — a diff for human approval with failure evidence attached. The agent never silently self-edits a frozen script. Unapproved scripts are immutable.
- **Attempt caps**: bounded retries per selector/action (~3); bounded heal proposals per run (~2); repeated failure surfaces to a human with the evidence bundle instead of looping.

### Step 4: Mandatory Failure Evidence

Every E2E failure must capture, at failure time: **screenshot + DOM/HTML snapshot** (+ accessibility-tree dump when reachable) + console errors + failed network requests. Wire this into a `takeSnapshot`-style fixture or an `afterEach` on-failure hook.

**"Selector not found" with no page evidence is not a filed bug.**

Details: `skills/test-strategy/references/enhancement-capabilities.md` §7.
