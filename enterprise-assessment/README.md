# Enterprise Assessment

A Claude Code plugin for evaluating software project readiness against enterprise standards. Scans projects across 12 categories, assigns risk-scored letter grades, maps findings to compliance frameworks (NIST, SOC2, ISO 27001), and produces executive-ready reports with prioritized remediation.

## Features

- **12 enterprise categories** — Security, IAM, Data Governance, Compliance, Ops Readiness, Incident Response, Infrastructure, Code Quality, Testing, Documentation, Third-Party Risk, Change Management
- **Risk-scored findings** — Critical/High/Medium/Low severity with likelihood x impact assessment
- **Compliance mapping** — Findings mapped to NIST 800-53, SOC2 TSC, and ISO 27001 controls
- **Executive summary** — Leadership-ready overview with risk posture and top priorities
- **Must-pass enforcement** — F in critical categories caps overall grade
- **Historical comparison** — Compare assessments over time to track improvement
- **Configurable** — `.enterprise-assessment.yml` for custom weights, categories, and profiles
- **Parallel evaluation** — All categories assessed simultaneously via subagents

## Commands

| Command | Description |
|---------|-------------|
| `/enterprise-assessment:assess` | Run a full enterprise readiness assessment |
| `/enterprise-assessment:drill` | Deep-dive into a specific category |
| `/enterprise-assessment:report` | Generate a comprehensive markdown report |
| `/enterprise-assessment:init` | Initialize a configuration file interactively |
| `/enterprise-assessment:compare` | Compare two assessment reports side-by-side |

## Agents

| Agent | Description |
|-------|-------------|
| `category-assessor` | Evaluates a single category with risk scoring and compliance mapping |

## Categories

| # | Category | Key | Focus |
|---|----------|-----|-------|
| 1 | Security Posture | `security` | Secrets, vulnerabilities, input validation, headers |
| 2 | Access Control & IAM | `iam` | Auth, RBAC, session management, privilege separation |
| 3 | Data Governance & Privacy | `data_governance` | PII handling, encryption, retention, classification |
| 4 | Compliance & Regulatory | `compliance` | Framework adherence, audit trails, policy documentation |
| 5 | Operational Readiness | `ops_readiness` | Runbooks, SLAs, capacity planning, on-call |
| 6 | Incident Response & BCP | `incident_response` | IR plans, backup/restore, disaster recovery, RTO/RPO |
| 7 | Infrastructure & Deployment | `infrastructure` | IaC, containers, CI/CD, environment parity |
| 8 | Code Quality | `code_quality` | Linting, complexity, dead code, style consistency |
| 9 | Testing | `testing` | Unit, integration, E2E, coverage, test hygiene |
| 10 | Documentation & Knowledge | `documentation` | Architecture, API docs, onboarding, decision records |
| 11 | Third-Party Risk | `third_party` | Dependency freshness, license compliance, vendor risk |
| 12 | Change Management | `change_management` | Branch strategy, PR process, release process, rollback |

## Grading System

| Grade | Score | Meaning |
|-------|-------|---------|
| A | 90-100% | Enterprise ready |
| B | 75-89% | Minor gaps — low risk |
| C | 60-74% | Significant gaps — moderate risk |
| D | 40-59% | Major gaps — high risk |
| F | < 40% | Not enterprise ready — critical risk |

## Installation

```bash
claude plugin install enterprise-assessment --marketplace bo-marketplace
```
