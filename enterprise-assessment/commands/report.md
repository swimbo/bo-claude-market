---
description: Generate a comprehensive enterprise assessment report with executive summary, risk register, compliance coverage, and remediation checklist
tools: Bash, Glob, Grep, Read, Write, Agent
argument-hint: "[--profile <name>]"
---

# Enterprise Assessment Report

Generate a comprehensive, shareable markdown report of the enterprise readiness assessment.

## Usage
- `/enterprise-assessment:report` — Generate report with default profile
- `/enterprise-assessment:report --profile fedramp` — Generate with FedRAMP profile

## Instructions

## Step 1: Detect Project

Scan the project root to identify:
- Project name (from directory, package.json, Cargo.toml, etc.)
- Backend language and frameworks
- Frontend framework (if any)
- Tech stack summary

## Step 2: Determine Profile and Configuration

Parse `--profile` from arguments. Check for `.enterprise-assessment.yml`. Default to `default` profile.

Load category weights and must-pass settings from the profile. Reference the rubric at the enterprise-rubric skill.

## Step 3: Evaluate All Categories in Parallel

Spawn `category-assessor` subagents in parallel using the Agent tool — one per enabled category.

For each agent, provide:
1. Category name and key
2. Project root path
3. Detected tech stack
4. Assessment profile

Do NOT ask for must-pass categories interactively — use profile defaults for the report.

Wait for all to complete.

## Step 4: Generate Report

Collect all subagent results. Use the full report format from `references/report-templates.md`.

The report must include all sections:

1. **Header** — Project name, tech stack, date, profile, overall grade, risk posture
2. **Executive Summary** — 3-5 sentences for leadership. Overall posture, critical/high finding count, top risk, recommended action.
3. **Scorecard Summary** — Table with all categories, grades, scores, finding counts by severity
4. **Category Details** — For each category: findings, gaps, and remediation with severity and compliance refs
5. **Risk Register** — Consolidated table of all Critical and High findings across categories
6. **Remediation Checklist** — Organized by severity tier (Critical → High → Medium → Low) with checkboxes
7. **Compliance Coverage** — Table showing controls assessed vs. satisfied for NIST, SOC2, ISO 27001

## Step 5: Save and Notify

Save the report as `enterprise-assessment-report.md` in the project root.

Tell the user:
```
Report saved to `enterprise-assessment-report.md`.

Key metrics:
- Overall Grade: [grade] ([pct]%)
- Risk Posture: [posture]
- Critical findings: [n]
- High findings: [n]
- Compliance coverage: NIST [pct]%, SOC2 [pct]%, ISO 27001 [pct]%

The risk register and remediation checklist can be used to track progress toward enterprise readiness.
Run `/enterprise-assessment:compare` after remediation to measure improvement.
```

## Important Guidelines

- This report may be shared with executive stakeholders and auditors — be thorough and precise
- Reference specific files and paths in all findings
- Every finding must include severity and compliance framework references
- Order the remediation checklist by severity (Critical first)
- The risk register must consolidate all Critical and High findings into one table
- The compliance coverage section must show concrete numbers, not vague percentages
- The report should stand on its own without needing prior scorecard context
