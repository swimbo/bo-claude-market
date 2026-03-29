---
description: Deep-dive into a specific enterprise assessment category with risk-scored findings, compliance mapping, and remediation
tools: Read, Grep, Glob, Bash, AskUserQuestion
argument-hint: "<category>"
---

# Category Deep Dive

Perform a thorough analysis of a single enterprise assessment category with risk-scored findings, compliance mapping, and prioritized remediation.

## Usage
- `/enterprise-assessment:drill security` — Deep-dive into Security Posture
- `/enterprise-assessment:drill iam` — Deep-dive into Access Control & IAM
- `/enterprise-assessment:drill testing` — Deep-dive into Testing

## Argument Handling

**Category requested:** $ARGUMENTS

If no argument provided, list all available categories and ask the user to choose.

## Instructions

## Step 1: Identify the Category

Match the user's input to a category (accept partial matches, case-insensitive):

| Input | Category | Key |
|-------|----------|-----|
| `security`, `sec` | Security Posture | `security` |
| `iam`, `access`, `auth` | Access Control & IAM | `iam` |
| `data`, `privacy`, `governance` | Data Governance & Privacy | `data_governance` |
| `compliance`, `regulatory`, `audit` | Compliance & Regulatory | `compliance` |
| `ops`, `operational`, `readiness` | Operational Readiness | `ops_readiness` |
| `incident`, `bcp`, `disaster`, `ir` | Incident Response & BCP | `incident_response` |
| `infra`, `infrastructure`, `deploy` | Infrastructure & Deployment | `infrastructure` |
| `quality`, `code` | Code Quality | `code_quality` |
| `testing`, `tests`, `test` | Testing | `testing` |
| `docs`, `documentation`, `knowledge` | Documentation & Knowledge | `documentation` |
| `third-party`, `vendor`, `deps`, `license` | Third-Party Risk | `third_party` |
| `change`, `release`, `pr`, `branching` | Change Management | `change_management` |

If no match, list categories and ask.

## Step 2: Load Rubric

Reference the full rubric for this category from the enterprise-rubric skill at `references/categories.md`. Also load `references/compliance-mapping.md` for the compliance controls that apply.

## Step 3: Deep Analysis

Thoroughly scan the project for everything related to this category. Go **deeper** than the quick scan:
- Read actual file contents, not just check for existence
- Check specific implementations and configurations
- Look for edge cases and misconfigurations
- Verify that documented capabilities actually work

For each check within the category, determine:
- **Status**: Pass / Partial / Fail / Unknown
- **Severity**: Critical / High / Medium / Low (for Partial or Fail findings)
- **Evidence**: Specific files, line numbers, patterns found
- **Details**: Why it received that status
- **Compliance**: Which framework controls are affected

## Step 4: Present Findings

Use the drill-down format from `references/report-templates.md`.

Include:
- Grade and risk level header
- Each check with status, severity, evidence, details, and compliance refs
- Gaps table with severity and compliance impact
- Remediation table with severity and effort estimate

## Step 5: Interactive Review

After presenting findings, ask:

> **Accept this assessment?**
> - **yes** — keep the grade as-is
> - **override [grade]** — change the grade (e.g., "override B"). Provide justification.
> - **notes** — add context without changing grade (e.g., "tests are in a separate repo")
> - **explain [check]** — get more detail on a specific check

Wait for the user's response and acknowledge it.

If overridden, confirm: "Grade updated to [grade]. Justification: [reason]"
If notes added, confirm: "Notes recorded. Grade remains [grade]."
If explain requested, provide more detail on the specific check and re-prompt.

## Remediation Guidelines

Keep remediation **light** — identify what's missing and where, but do not generate code or create files. Include effort estimates:

- **Low effort**: Configuration change, adding a file, updating a setting
- **Medium effort**: Implementing a new capability (e.g., adding audit logging)
- **High effort**: Architectural change or new system (e.g., implementing RBAC)

## Important Guidelines

- Reference specific files and paths in all findings
- Every finding must include compliance framework references
- Be precise about what exists vs. what's missing
- If you can't verify without running code, mark "Unknown" and score conservatively
- Acknowledge partial implementations — not everything is binary pass/fail
