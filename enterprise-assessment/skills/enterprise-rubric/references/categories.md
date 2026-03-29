# Enterprise Assessment Categories

Full rubric with percentage breakdowns for each check within each category.

---

## 1. Security Posture
Key: `security` | Default Weight: 1.5

| Check | Weight | What to Look For |
|-------|--------|-----------------|
| No hardcoded secrets | 25% | Grep for API keys, passwords, tokens, connection strings in source. Check `.env` files are gitignored. |
| Dependency vulnerabilities | 20% | Check lock files for known vulnerable versions. Look for `npm audit`, `pip-audit`, `cargo audit` in CI. |
| Input validation | 20% | User-facing endpoints validate and sanitize input. Parameterized queries (no SQL injection). |
| Security headers | 15% | CSP, HSTS, X-Frame-Options, X-Content-Type-Options configured. CORS properly scoped. |
| Rate limiting | 10% | Rate limiting on auth endpoints and public APIs. |
| Encryption in transit | 10% | TLS enforced. No HTTP-only endpoints for sensitive data. |

---

## 2. Access Control & IAM
Key: `iam` | Default Weight: 1.5

| Check | Weight | What to Look For |
|-------|--------|-----------------|
| Authentication implemented | 25% | Auth system exists (JWT, OAuth, SAML, session-based). Login/logout flows. |
| Authorization / RBAC | 25% | Role-based or permission-based access checks on protected routes/resources. |
| Session management | 20% | Token expiry, refresh flow, secure cookie flags (HttpOnly, Secure, SameSite). |
| Privilege separation | 15% | Admin vs. user paths separated. No privilege escalation paths. |
| Password / credential policy | 15% | Minimum complexity, hashing (bcrypt/argon2), no plaintext storage. |

---

## 3. Data Governance & Privacy
Key: `data_governance` | Default Weight: 1.25

| Check | Weight | What to Look For |
|-------|--------|-----------------|
| PII identification | 25% | Data models annotated or documented for PII fields. |
| Encryption at rest | 25% | Database encryption, encrypted backups, sensitive field encryption. |
| Data retention policy | 20% | Retention/deletion logic documented or implemented. Soft delete vs. hard delete. |
| Data classification | 15% | Data categorized (public, internal, confidential, restricted). |
| Privacy compliance | 15% | Consent mechanisms, data export/deletion capabilities (GDPR/CCPA readiness). |

---

## 4. Compliance & Regulatory
Key: `compliance` | Default Weight: 1.25

| Check | Weight | What to Look For |
|-------|--------|-----------------|
| Audit logging | 30% | Security-relevant events logged (auth, data access, admin actions) with timestamps and actor. |
| Policy documentation | 25% | Security policies, acceptable use, data handling documented. |
| Compliance framework mapping | 25% | Controls mapped to a framework (SOC2, NIST, ISO 27001, HIPAA). |
| Evidence collection | 20% | Artifacts exist for audit (access reviews, change logs, incident reports). |

---

## 5. Operational Readiness
Key: `ops_readiness` | Default Weight: 1.0

| Check | Weight | What to Look For |
|-------|--------|-----------------|
| Runbooks / playbooks | 30% | Documented procedures for common operations (deploy, rollback, scale, rotate secrets). |
| SLA / SLO definitions | 25% | Uptime targets, latency targets, error budget defined. |
| Capacity planning | 25% | Load expectations documented. Auto-scaling configured or documented. |
| On-call / escalation | 20% | On-call rotation documented. Escalation paths defined. |

---

## 6. Incident Response & BCP
Key: `incident_response` | Default Weight: 1.0

| Check | Weight | What to Look For |
|-------|--------|-----------------|
| Incident response plan | 30% | IR process documented (detect, respond, recover, post-mortem). |
| Backup & restore | 25% | Database backups configured. Restore procedure tested or documented. |
| Disaster recovery | 25% | RTO/RPO defined. Multi-region or failover strategy documented. |
| Post-incident process | 20% | Post-mortem template or past post-mortems exist. Lessons-learned tracking. |

---

## 7. Infrastructure & Deployment
Key: `infrastructure` | Default Weight: 1.0

| Check | Weight | What to Look For |
|-------|--------|-----------------|
| Containerization / IaC | 25% | Dockerfile, docker-compose, Terraform, Pulumi, or similar. |
| CI/CD pipeline | 25% | Pipeline config exists (.github/workflows, .gitlab-ci.yml, etc.) with build, test, deploy stages. |
| Environment parity | 25% | Dev/staging/prod environments documented. Config differences clear. |
| Deployment documentation | 25% | Deploy process documented. Required env vars, ports, dependencies listed. |

---

## 8. Code Quality
Key: `code_quality` | Default Weight: 0.75

| Check | Weight | What to Look For |
|-------|--------|-----------------|
| Linter / formatter configured | 25% | ESLint, Prettier, Ruff, Clippy, or equivalent configured and enforced. |
| Manageable complexity | 25% | No excessively long functions (>100 lines) or files (>500 lines). |
| Minimal dead code | 25% | No unused imports, unreachable code, commented-out blocks. |
| Consistent patterns | 25% | Consistent naming, error handling, file organization throughout. |

---

## 9. Testing
Key: `testing` | Default Weight: 1.0

| Check | Weight | What to Look For |
|-------|--------|-----------------|
| Unit tests exist | 25% | Tests for core business logic, utilities, and models. |
| Integration tests exist | 25% | Tests for API endpoints, service boundaries, database interactions. |
| E2E tests exist | 20% | Tests for critical user flows (login, CRUD, payment, etc.). |
| Tests appear to pass | 15% | No obviously broken test files. CI runs tests. |
| Reasonable coverage | 15% | Coverage config exists. Core paths covered. |

---

## 10. Documentation & Knowledge
Key: `documentation` | Default Weight: 0.75

| Check | Weight | What to Look For |
|-------|--------|-----------------|
| Architecture documentation | 25% | System design, component diagram, data flow documented. |
| API documentation | 25% | OpenAPI/Swagger spec, endpoint docs, or comprehensive inline docs. |
| Setup / onboarding guide | 25% | README with build, run, and development setup steps. |
| Decision records | 25% | ADRs, design docs, or rationale for key technical decisions. |

---

## 11. Third-Party Risk
Key: `third_party` | Default Weight: 1.0

| Check | Weight | What to Look For |
|-------|--------|-----------------|
| Dependency freshness | 25% | No critically outdated dependencies. Major versions within 1-2 of latest. |
| License compliance | 25% | LICENSE file present. No GPL in proprietary projects. Compatible licenses. |
| Dependency count | 25% | Reasonable dependency tree. No unnecessary packages. |
| Vendor risk assessment | 25% | Critical third-party services documented. Fallback plans for vendor outages. |

---

## 12. Change Management
Key: `change_management` | Default Weight: 1.0

| Check | Weight | What to Look For |
|-------|--------|-----------------|
| Branch strategy | 25% | Branch protection on main. PR-based workflow. |
| PR / review process | 25% | PR templates, review requirements, approval gates. |
| Release process | 25% | Versioning scheme (semver). Changelog maintained. Release tags. |
| Rollback capability | 25% | Rollback documented or automated. Previous version deployable. |
