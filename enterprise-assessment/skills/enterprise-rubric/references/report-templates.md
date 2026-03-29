# Report Templates

Output formats for all enterprise assessment commands.

---

## Scorecard Format (`/enterprise-assessment:assess`)

```markdown
# Enterprise Readiness Assessment

**Project:** [project name]
**Tech Stack:** [detected languages/frameworks]
**Date:** [current date]
**Profile:** [assessment profile used]
**Overall Grade:** [LETTER] ([percentage]%)
**Risk Posture:** [APPROVED / CONDITIONAL / DEFERRED / BLOCKED / REJECTED]

## Scorecard

| # | Category | Grade | Score | Findings | Risk |
|---|----------|-------|-------|----------|------|
| 1 | Security Posture | [grade] | [pct]% | [critical/high/med/low counts] | [highest severity] |
| 2 | Access Control & IAM | [grade] | [pct]% | [counts] | [severity] |
| 3 | Data Governance & Privacy | [grade] | [pct]% | [counts] | [severity] |
| 4 | Compliance & Regulatory | [grade] | [pct]% | [counts] | [severity] |
| 5 | Operational Readiness | [grade] | [pct]% | [counts] | [severity] |
| 6 | Incident Response & BCP | [grade] | [pct]% | [counts] | [severity] |
| 7 | Infrastructure & Deployment | [grade] | [pct]% | [counts] | [severity] |
| 8 | Code Quality | [grade] | [pct]% | [counts] | [severity] |
| 9 | Testing | [grade] | [pct]% | [counts] | [severity] |
| 10 | Documentation & Knowledge | [grade] | [pct]% | [counts] | [severity] |
| 11 | Third-Party Risk | [grade] | [pct]% | [counts] | [severity] |
| 12 | Change Management | [grade] | [pct]% | [counts] | [severity] |
| | **Overall** | **[grade]** | **[pct]%** | **[totals]** | **[posture]** |

[If must-pass failed: "**Must-Pass Failed:** [category] received F — overall grade capped at C"]

## Executive Summary

[2-3 sentence risk posture summary for leadership. Include: overall readiness level, number of critical/high findings, and the single biggest risk.]

## Top 5 Priorities

| # | Category | Severity | Finding | Compliance |
|---|----------|----------|---------|------------|
| 1 | [cat] | Critical | [finding] | [NIST/SOC2/ISO ref] |
| 2 | [cat] | Critical | [finding] | [ref] |
| 3 | [cat] | High | [finding] | [ref] |
| 4 | [cat] | High | [finding] | [ref] |
| 5 | [cat] | High | [finding] | [ref] |

---

Run `/enterprise-assessment:drill [category]` to deep-dive into any category.
Run `/enterprise-assessment:report` to generate a full markdown report.
```

---

## Drill-Down Format (`/enterprise-assessment:drill`)

```markdown
## [CATEGORY NAME] — Deep Dive

**Grade:** [letter] ([percentage]%)
**Risk Level:** [Critical/High/Medium/Low]

### Findings

#### [Check Name]
- **Status:** Pass / Partial / Fail / Unknown
- **Severity:** [Critical/High/Medium/Low]
- **Evidence:** [specific files, line numbers, patterns]
- **Details:** [explanation]
- **Compliance:** [NIST: XX-X, SOC2: CCX.X, ISO: A.X.XX]

[Repeat for each check]

### Gaps Identified

| # | Gap | Severity | Compliance Impact |
|---|-----|----------|------------------|
| 1 | [gap with file/location context] | [severity] | [framework refs] |

### Remediation

| # | Action | Severity | Effort |
|---|--------|----------|--------|
| 1 | [actionable step — light, no code generation] | [severity] | [Low/Medium/High] |
```

---

## Full Report Format (`/enterprise-assessment:report`)

```markdown
# Enterprise Readiness Assessment Report

**Project:** [project name]
**Tech Stack:** [detected languages/frameworks]
**Date:** [current date]
**Assessor:** Claude Code (enterprise-assessment plugin v0.1.0)
**Profile:** [assessment profile]

---

## Executive Summary

[3-5 sentence summary for executive stakeholders. Include:
- Overall readiness posture and grade
- Number of critical and high findings
- Top risk area
- Recommended action (approve, defer, block)]

**Risk Posture:** [APPROVED / CONDITIONAL / DEFERRED / BLOCKED / REJECTED]

---

## Scorecard Summary

| # | Category | Grade | Score | Critical | High | Medium | Low |
|---|----------|-------|-------|----------|------|--------|-----|
| 1 | Security Posture | [grade] | [pct]% | [n] | [n] | [n] | [n] |
| ... | ... | ... | ... | ... | ... | ... | ... |
| | **Overall** | **[grade]** | **[pct]%** | **[n]** | **[n]** | **[n]** | **[n]** |

---

## Category Details

### 1. Security Posture — [Grade] ([pct]%)

**Findings:**
- [finding with severity, file references, and compliance mapping]

**Gaps:**
- [gap description with severity and compliance impact]

**Remediation:**
- [action item with severity and effort estimate]

---

[Repeat for each category]

---

## Risk Register

All Critical and High findings consolidated:

| # | Category | Finding | Severity | Compliance | Remediation | Effort |
|---|----------|---------|----------|------------|-------------|--------|
| 1 | [cat] | [finding] | Critical | [refs] | [action] | [effort] |
| ... | ... | ... | ... | ... | ... | ... |

---

## Remediation Checklist

### Critical (Fix Before Deployment)
- [ ] [Action item 1]
- [ ] [Action item 2]

### High (Fix Within 30 Days)
- [ ] [Action item 3]
- [ ] [Action item 4]

### Medium (Fix Within 90 Days)
- [ ] [Action item 5]

### Low (Track in Backlog)
- [ ] [Action item 6]

---

## Compliance Coverage

| Framework | Controls Assessed | Controls Satisfied | Coverage |
|-----------|------------------|--------------------|----------|
| NIST 800-53 | [n] | [n] | [pct]% |
| SOC2 TSC | [n] | [n] | [pct]% |
| ISO 27001 | [n] | [n] | [pct]% |

---

*Report generated by enterprise-assessment plugin v0.1.0*
```

---

## Comparison Format (`/enterprise-assessment:compare`)

```markdown
# Assessment Comparison

**Project:** [project name]
**Baseline:** [date of earlier report]
**Current:** [date of newer report]

## Grade Trend

| Category | Baseline | Current | Change |
|----------|----------|---------|--------|
| Security Posture | B (82%) | A (93%) | +11% |
| Access Control & IAM | C (65%) | B (78%) | +13% |
| ... | ... | ... | ... |
| **Overall** | **C (68%)** | **B (81%)** | **+13%** |

## Risk Posture Change

**[DEFERRED → CONDITIONAL]** — [summary of improvement]

## Resolved Findings

- [Finding that was remediated, with category and previous severity]

## New Findings

- [Finding that appeared in current but not baseline]

## Persistent Findings

- [Finding present in both, with severity and staleness note]

## Recommendations

[2-3 sentences on trajectory and what to focus on next]
```
