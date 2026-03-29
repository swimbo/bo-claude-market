---
description: Compare two enterprise assessment reports side-by-side to track improvement over time
tools: Read, Glob, Grep, AskUserQuestion
argument-hint: "<baseline-report> <current-report>"
---

# Assessment Comparison

Compare two enterprise assessment reports to track improvement, identify resolved and persistent findings, and measure remediation progress.

## Usage
- `/enterprise-assessment:compare` — Auto-detect reports in project
- `/enterprise-assessment:compare report-v1.md report-v2.md` — Compare specific files

## Instructions

## Step 1: Locate Reports

If arguments provided, use those file paths.

If no arguments, search for assessment reports:
```
Glob: **/enterprise-assessment-report*.md
```

If multiple reports found, list them with dates and ask the user to select baseline and current:

> **Found assessment reports:**
> 1. `enterprise-assessment-report.md` (2026-03-15)
> 2. `enterprise-assessment-report-2026-03-01.md` (2026-03-01)
>
> Which is the **baseline** (earlier)? Which is the **current** (newer)?

If only one report found, tell the user they need at least two reports to compare. Suggest running `/enterprise-assessment:report` first and renaming the existing report.

If zero reports found, tell the user to run `/enterprise-assessment:report` first.

## Step 2: Parse Reports

Read both reports and extract for each:
- Overall grade and percentage
- Risk posture
- Per-category grades and percentages
- All findings with severity levels
- Finding descriptions (for matching resolved vs. persistent)

## Step 3: Calculate Deltas

For each category:
- Calculate score change (current - baseline)
- Determine grade change
- Flag improvements (+) and regressions (-)

For findings:
- **Resolved**: Present in baseline but not in current
- **New**: Present in current but not in baseline
- **Persistent**: Present in both (match by description similarity)

## Step 4: Generate Comparison

Use the comparison format from `references/report-templates.md`.

Include:
1. **Grade Trend** — Table with baseline, current, and change per category
2. **Risk Posture Change** — Previous → Current with summary
3. **Resolved Findings** — What was fixed (with previous severity)
4. **New Findings** — What appeared (with current severity)
5. **Persistent Findings** — What remains (with severity and staleness note)
6. **Recommendations** — 2-3 sentences on trajectory and next priorities

## Step 5: Present Results

Display the comparison inline. If the user wants it saved, write to `enterprise-assessment-comparison.md`.

Highlight key metrics:
- Overall score change (+/-X%)
- Number of resolved findings
- Number of new findings
- Risk posture change

## Important Guidelines

- Match findings by description similarity, not exact string match
- A finding that changed severity (e.g., Critical → Medium) is partially resolved — note the change
- If a category was added or removed between reports, note it rather than showing a delta
- Focus recommendations on persistent Critical/High findings — these represent unaddressed risk
