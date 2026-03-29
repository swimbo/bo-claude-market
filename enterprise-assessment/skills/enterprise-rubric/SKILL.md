---
name: enterprise-rubric
description: >
  Shared evaluation rubric for the enterprise assessment plugin — 12 category definitions,
  grading thresholds, risk severity levels, compliance framework mapping, and output formats.
  Load this skill when running any enterprise-assessment command (assess, drill, report, init, compare).
version: 1.0.0
---

# Enterprise Assessment Rubric

## Overview

Evaluates software projects against 12 enterprise readiness categories spanning security, compliance, operational maturity, and engineering quality. Each finding is risk-scored and mapped to industry compliance frameworks.

## Grading System

| Grade | Score Range | Risk Level | Meaning |
|-------|-----------|------------|---------|
| **A** | 90-100% | Minimal | Enterprise ready — meets or exceeds standards |
| **B** | 75-89% | Low | Minor gaps — acceptable with tracked remediation |
| **C** | 60-74% | Moderate | Significant gaps — remediation required before production |
| **D** | 40-59% | High | Major gaps — not safe for enterprise deployment |
| **F** | Below 40% | Critical | Not enterprise ready — fundamental rework needed |

### Must-Pass Enforcement

Must-pass categories are selected during assessment. If any must-pass category receives an F, the overall grade is **capped at C** regardless of other scores.

**Default must-pass:** Security Posture, Access Control & IAM

### Risk Posture Summary

Based on the overall grade, assign a risk posture:

| Grade | Posture | Action |
|-------|---------|--------|
| A | **APPROVED** | Ready for enterprise deployment |
| B | **CONDITIONAL** | Approved with remediation plan and timeline |
| C | **DEFERRED** | Requires remediation before deployment approval |
| D | **BLOCKED** | Cannot proceed — critical gaps must be addressed |
| F | **REJECTED** | Fundamental enterprise readiness criteria unmet |

## Finding Severity Levels

Every finding is assigned a severity based on likelihood of exploitation/occurrence and business impact:

| Severity | Definition | SLA |
|----------|-----------|-----|
| **Critical** | Actively exploitable or regulatory violation — immediate business risk | Fix before deployment |
| **High** | Likely to cause incidents or compliance findings in audit | Fix within 30 days |
| **Medium** | Could cause issues under specific conditions — defense-in-depth gap | Fix within 90 days |
| **Low** | Best practice gap — minimal immediate risk | Track in backlog |

## Categories (12)

See `references/categories.md` for full rubric with percentage breakdowns per check.

| # | Category | Key | Default Weight |
|---|----------|-----|---------------|
| 1 | Security Posture | `security` | 1.5 |
| 2 | Access Control & IAM | `iam` | 1.5 |
| 3 | Data Governance & Privacy | `data_governance` | 1.25 |
| 4 | Compliance & Regulatory | `compliance` | 1.25 |
| 5 | Operational Readiness | `ops_readiness` | 1.0 |
| 6 | Incident Response & BCP | `incident_response` | 1.0 |
| 7 | Infrastructure & Deployment | `infrastructure` | 1.0 |
| 8 | Code Quality | `code_quality` | 0.75 |
| 9 | Testing | `testing` | 1.0 |
| 10 | Documentation & Knowledge | `documentation` | 0.75 |
| 11 | Third-Party Risk | `third_party` | 1.0 |
| 12 | Change Management | `change_management` | 1.0 |

**Note:** Security and IAM are weighted 1.5x by default. Code Quality and Documentation are weighted 0.75x. All weights are configurable via `.enterprise-assessment.yml`.

## Compliance Framework Mapping

See `references/compliance-mapping.md` for the full mapping of each category to:
- **NIST 800-53** control families
- **SOC2** Trust Services Criteria
- **ISO 27001** Annex A controls

## Configuration Override

Projects can include a `.enterprise-assessment.yml` file:

```yaml
# Enterprise Assessment Configuration
profile: default  # or: fedramp, hipaa, financial, minimal

must_pass:
  - security
  - iam

categories:
  # Adjust weight
  testing:
    weight: 1.5

  # Disable a category
  change_management:
    enabled: false

  # Custom category
  api_standards:
    name: "Internal API Standards"
    weight: 1.0
    checks:
      - "All endpoints follow REST naming conventions"
      - "Pagination implemented on list endpoints"
      - "Rate limiting configured per endpoint"
```

### Assessment Profiles

| Profile | Must-Pass | Extra Weight | Notes |
|---------|-----------|-------------|-------|
| `default` | security, iam | Security 1.5x, IAM 1.5x | General enterprise |
| `fedramp` | security, iam, compliance, data_governance | Compliance 2.0x | Federal workloads |
| `hipaa` | security, data_governance, iam | Data Governance 2.0x | Healthcare data |
| `financial` | security, iam, compliance, change_management | Change Mgmt 1.5x | Financial services |
| `minimal` | security | All equal weight | Startup/internal tools |

## Output Formats

See `references/report-templates.md` for all output formats (scorecard, drill-down, full report, comparison).

## Evaluation Guidelines

- **Evidence-based only** — grade what you can verify by reading the codebase
- **Conservative scoring** — if you cannot determine something without running code, mark "Unknown" and score conservatively
- **No inflation** — a missing capability is a missing capability
- **Specific references** — cite files, line numbers, and patterns in every finding
- **Risk-first remediation** — order by severity, not by category
- **Light remediation** — identify gaps, do not generate code or create files

## Reference Files

- **`references/categories.md`** — Full rubric with percentage breakdowns for all 12 categories
- **`references/compliance-mapping.md`** — NIST 800-53, SOC2, ISO 27001 control mapping
- **`references/report-templates.md`** — Scorecard, drill-down, report, and comparison output formats
