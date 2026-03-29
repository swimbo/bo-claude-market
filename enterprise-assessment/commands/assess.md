---
description: Run a full enterprise readiness assessment with risk-scored grades and compliance mapping
tools: Bash, Glob, Grep, Read, Agent, AskUserQuestion
argument-hint: "[--profile <name>]"
---

# Enterprise Readiness Assessment

Evaluate a project against 12 enterprise readiness categories, assign risk-scored letter grades, and produce a scorecard with executive summary and compliance mapping.

## Usage
- `/enterprise-assessment:assess` — Assess with default profile
- `/enterprise-assessment:assess --profile fedramp` — Assess with FedRAMP profile

## Instructions

## Step 1: Detect Project

Scan the project root to identify:
- Backend language and frameworks
- Frontend framework (if any)
- Package managers and build tools
- Project structure and size

Report findings briefly before proceeding.

## Step 2: Select Assessment Profile

Parse the argument for `--profile`. If provided, use that profile. Otherwise, check for `.enterprise-assessment.yml` in the project root.

If neither exists, ask the user:

> **Which assessment profile should I use?**
>
> | Profile | Focus | Best For |
> |---------|-------|----------|
> | `default` | General enterprise readiness | Most projects |
> | `fedramp` | Federal compliance (NIST heavy) | Government workloads |
> | `hipaa` | Healthcare data protection | PHI/ePHI systems |
> | `financial` | SOX, change control, audit | Financial services |
> | `minimal` | Security basics only | Internal tools, startups |
>
> Type a profile name, or press enter for `default`.

Wait for response before proceeding.

## Step 3: Select Must-Pass Categories

If using a profile, apply that profile's default must-pass categories (see rubric skill).

If using `default` profile, ask the user:

> **Which categories are must-pass?** (F in these caps overall grade at C)
>
> Default must-pass: Security Posture, Access Control & IAM
>
> Available categories:
> 1. Security Posture
> 2. Access Control & IAM
> 3. Data Governance & Privacy
> 4. Compliance & Regulatory
> 5. Operational Readiness
> 6. Incident Response & BCP
> 7. Infrastructure & Deployment
> 8. Code Quality
> 9. Testing
> 10. Documentation & Knowledge
> 11. Third-Party Risk
> 12. Change Management
>
> Type numbers (e.g., "1, 2, 4"), or press enter for defaults.

Wait for response.

## Step 4: Evaluate All Categories in Parallel

Spawn `category-assessor` subagents in parallel using the Agent tool — one per enabled category.

For each agent, provide:
1. Category name and key
2. Project root path
3. Detected tech stack
4. Assessment profile being used

Launch all evaluators in a single message for parallel execution. Skip categories disabled via `.enterprise-assessment.yml`.

Wait for all to complete before proceeding.

## Step 5: Aggregate Results

Collect results from all subagents. For each category:
- Extract score, grade, findings (with severity), gaps, and remediation items
- Apply category weights from profile or config

Calculate the overall score as a **weighted average**:
```
overall = sum(category_score * category_weight) / sum(category_weights)
```

Apply must-pass enforcement: if any must-pass category is F, cap overall at C.

Determine risk posture from overall grade (see rubric skill).

## Step 6: Build Executive Summary

Write a 2-3 sentence executive summary covering:
- Overall readiness level and risk posture
- Count of Critical and High findings across all categories
- The single biggest risk area

## Step 7: Output the Scorecard

Use the scorecard format from `references/report-templates.md` in the enterprise-rubric skill.

Include:
- Full scorecard table with finding counts per severity
- Must-pass failure callout (if applicable)
- Executive summary
- Top 5 priorities table (highest severity findings across all categories)

End with:
```
Run `/enterprise-assessment:drill [category]` to deep-dive into any category.
Run `/enterprise-assessment:report` to generate a full markdown report.
```

## Important Rules

- Wait for user input on profile and must-pass selection — do not skip
- Launch all category assessors in parallel, not sequentially
- Every finding must have a severity level (Critical/High/Medium/Low)
- Every finding must include compliance framework references
- Keep remediation light — identify gaps, do not generate code
- Reference specific files and paths in all findings
