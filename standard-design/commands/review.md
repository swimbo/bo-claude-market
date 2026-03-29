---
name: review
description: Review React + MUI components for Standard Design System compliance — checks colors, typography, spacing, effects, and patterns
argument-hint: "[file-or-directory-path]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Agent
  - AskUserQuestion
---

# Review Design Compliance

Audit React + MUI components against Standard Design System rules.

**The argument is the file or directory to review.** If omitted, review all `.tsx` files under `src/`.

## Step 1: Identify Files to Review

If a specific file is provided, review just that file. If a directory is provided or no argument given, find all component files:

```
Glob: {target}/**/*.tsx
```

Exclude test files (`*.test.tsx`, `*.spec.tsx`), story files (`*.stories.tsx`), and the theme files themselves (`src/theme/`).

If more than 10 files are found, launch a `design-reviewer` agent per batch of 5 files using the Agent tool. For 10 or fewer, review inline.

## Step 2: Review Each File

For each component file, check these compliance rules:

### Colors (Critical)
- [ ] **No raw hex colors** — Search for hex patterns (`#[0-9a-fA-F]{3,8}`). All colors must come from `useColors()`, `useTheme()`, or MUI palette tokens
- [ ] **No raw rgba/rgb** — Same rule. Use token glow values instead
- [ ] **Status colors via variants** — Chips, Alerts, and indicators must use `color="success|warning|error|info"` props, not custom colors

### Typography (Critical)
- [ ] **Correct font family per context** — Headings use Outfit (h1-h6 variants), body uses DM Sans (body1/body2), data uses JetBrains Mono (overline)
- [ ] **No inline fontFamily** — Must use MUI Typography `variant` prop, not `sx={{ fontFamily: '...' }}`
- [ ] **No textTransform on buttons** — Buttons must not set `textTransform: 'uppercase'`

### Spacing (Warning)
- [ ] **Consistent border radius** — 8px default, 12px for cards/dialogs, 6px for chips/tooltips. Flag non-standard values
- [ ] **MUI spacing scale** — Use `theme.spacing()` or numeric `sx` values (1=8px), not pixel values
- [ ] **Page layout spacing** — Cards separated by `mb: 3`, sections by `mb: 2`

### Effects (Warning)
- [ ] **Transition timing** — Should be `0.2s ease` or `0.2s cubic-bezier(...)`. Flag slow (>0.5s) or instant transitions
- [ ] **Glow on interactive elements** — Buttons, chips, and icon buttons should have glow on hover via theme overrides
- [ ] **No custom shadows** — Use MUI `elevation` prop or theme shadows array, not custom `boxShadow`

### Component Usage (Info)
- [ ] **Using Layout wrapper** — Admin pages should be wrapped in `<Layout>` component
- [ ] **DataTable for data grids** — Using `<DataTable>` component instead of raw `<DataGrid>`
- [ ] **Chip for status** — Status indicators use `<Chip>` with semantic color variant
- [ ] **Alert for messages** — Feedback messages use `<Alert>` with severity, not custom styled boxes

### Patterns (Info)
- [ ] **Page structure** — Follows one of the 4 Standard page patterns (Dashboard, List, Detail, Form)
- [ ] **Header + actions** — Page headers use h1 + body2 description, with action buttons right-aligned
- [ ] **Card grouping** — Related content grouped in Cards with h5/h6 section titles

## Step 3: Generate Report

Produce a compliance report organized by severity:

```markdown
# Standard Design Compliance Report

## Summary
- Files reviewed: X
- Critical issues: X (must fix)
- Warnings: X (should fix)
- Info: X (suggestions)

## Critical Issues

### [filename.tsx]
- **Line X**: Raw hex color `#ff0000` found — use `colors.danger` from `useColors()` hook
- **Line X**: Inline `fontFamily: 'Arial'` — use MUI Typography variant instead

## Warnings

### [filename.tsx]
- **Line X**: Border radius `10px` — Standard uses 8px (default) or 12px (cards). Use `borderRadius: 1` or `borderRadius: 1.5`
- **Line X**: Transition `0.5s` — Standard standard is `0.2s ease`

## Info

### [filename.tsx]
- **Line X**: Status text rendered as plain Typography — consider using `<Chip color="success">` for visual consistency
- Page does not follow any standard Standard page pattern — see page-patterns reference

## Passed
- [filename.tsx] — No issues found
```

Present the report to the user. If there are critical issues, ask if they want you to fix them automatically.

## Step 4: Save Report for Cross-Plugin Use

Check if a bo-planner planning session is active by looking for `docs/planning/phased-plan.md`:

- **If planning is active**: Save the compliance report to `docs/planning/design-compliance.md` with a header:
  ```markdown
  # Standard Design Compliance Report
  **Date:** [current date]
  **Files reviewed:** [count]
  **Critical issues:** [count]
  **Warnings:** [count]
  **Info:** [count]

  [full report content]
  ```
  This makes the report available to:
  - `/bo-planner:done` — checks for unresolved critical design issues
  - `/enterprise-assessment:assess` — uses as evidence for Code Quality category
  - `/bo-planner:status` — shows design compliance state

- **If no planning session**: Do not save to file (report was already presented inline)

## Important Rules

- Only flag issues that deviate from Standard design system rules — don't enforce general code style
- Theme files (`src/theme/*`) are exempt from review — they define the rules
- Story files are exempt — they may intentionally demonstrate non-compliant states
- If a project hasn't applied Standard theme yet, suggest running `/standard-design:apply` first
- For large codebases (50+ files), use parallel `design-reviewer` agents
