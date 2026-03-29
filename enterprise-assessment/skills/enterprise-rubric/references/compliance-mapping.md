# Compliance Framework Mapping

Maps each enterprise assessment category to controls in NIST 800-53, SOC2 Trust Services Criteria, and ISO 27001 Annex A.

Use this mapping to annotate findings with the specific compliance controls they affect.

---

## Category → Framework Controls

| Category | NIST 800-53 | SOC2 TSC | ISO 27001 |
|----------|------------|----------|-----------|
| **Security Posture** | SC-8 (Transmission Confidentiality), SC-12 (Crypto Key Mgmt), SI-10 (Input Validation), SC-28 (Data at Rest) | CC6.1 (Logical Access), CC6.6 (System Boundaries), CC6.7 (Data Transmission) | A.8.24 (Cryptography), A.8.26 (App Security), A.8.28 (Secure Coding) |
| **Access Control & IAM** | AC-2 (Account Mgmt), AC-3 (Access Enforcement), AC-6 (Least Privilege), IA-2 (Identification & Auth), IA-5 (Authenticator Mgmt) | CC6.1 (Logical Access), CC6.2 (Auth Credentials), CC6.3 (Access Authorization) | A.5.15 (Access Control), A.5.16 (Identity Mgmt), A.5.17 (Authentication), A.8.3 (Access Restriction) |
| **Data Governance & Privacy** | MP-4 (Media Storage), MP-6 (Media Sanitization), SI-12 (Info Handling), PM-11 (Privacy Program) | P1-P8 (Privacy Criteria), CC6.5 (Data Disposal) | A.5.33 (PII Protection), A.5.34 (Privacy), A.8.10 (Information Deletion), A.8.11 (Data Masking) |
| **Compliance & Regulatory** | AU-2 (Event Logging), AU-3 (Audit Content), AU-6 (Audit Review), CA-2 (Control Assessments) | CC4.1 (Monitoring), CC4.2 (Evaluation), CC7.2 (System Monitoring) | A.5.35 (Independent Review), A.5.36 (Compliance with Policies), A.8.15 (Logging) |
| **Operational Readiness** | CP-2 (Contingency Plan), SA-5 (System Documentation), IR-7 (Incident Response Assistance) | CC7.4 (Incident Response), CC7.5 (Incident Recovery), A1.2 (Recovery Objectives) | A.5.29 (ICT Readiness for BC), A.5.30 (ICT Readiness for BC), A.7.4 (Physical Security Monitoring) |
| **Incident Response & BCP** | IR-1 (IR Policy), IR-4 (Incident Handling), IR-5 (Incident Monitoring), IR-8 (IR Plan), CP-9 (System Backup), CP-10 (System Recovery) | CC7.3 (Incident Detection), CC7.4 (Incident Response), CC7.5 (Recovery), A1.2 (Recovery Objectives), A1.3 (Recovery Testing) | A.5.24 (IR Planning), A.5.25 (Assessment of Info Security Events), A.5.26 (Response to Incidents), A.8.13 (Backup) |
| **Infrastructure & Deployment** | CM-2 (Baseline Config), CM-3 (Configuration Change Control), SA-10 (Dev Config Mgmt) | CC8.1 (Change Management), CC7.1 (Infrastructure Monitoring) | A.8.9 (Configuration Mgmt), A.8.25 (Secure Development Lifecycle), A.8.27 (Secure Architecture) |
| **Code Quality** | SA-11 (Developer Testing), SA-15 (Development Process), SI-2 (Flaw Remediation) | CC8.1 (Change Management) | A.8.25 (Secure Development Lifecycle), A.8.28 (Secure Coding) |
| **Testing** | SA-11 (Developer Testing), CA-8 (Penetration Testing), SI-6 (Security Function Verification) | CC8.1 (Change Management), CC7.1 (Infrastructure Monitoring) | A.8.25 (Secure Development Lifecycle), A.8.29 (Security Testing) |
| **Documentation & Knowledge** | SA-5 (System Documentation), PL-2 (System Security Plan), AT-3 (Role-Based Training) | CC2.1 (COSO Communication), CC2.2 (Internal Communication) | A.5.37 (Operating Procedures), A.6.3 (Awareness & Training) |
| **Third-Party Risk** | SA-4 (Acquisition Process), SA-9 (External Services), SR-3 (Supply Chain Controls) | CC9.2 (Vendor Risk), CC3.2 (Risk Assessment) | A.5.19 (Supplier Relationships), A.5.20 (Supplier Agreements), A.5.21 (ICT Supply Chain), A.5.22 (Supplier Monitoring) |
| **Change Management** | CM-3 (Change Control), CM-4 (Change Impact Analysis), CM-5 (Access Restrictions for Change) | CC8.1 (Change Management), CC6.8 (Unauthorized Changes) | A.8.32 (Change Management), A.8.33 (Test Information), A.8.25 (Secure Development Lifecycle) |

---

## How to Use in Findings

When reporting a finding, include the compliance references:

```
FINDING: No audit logging for admin actions
SEVERITY: High
COMPLIANCE:
  - NIST: AU-2 (Event Logging), AU-3 (Audit Content)
  - SOC2: CC4.1 (Monitoring), CC7.2 (System Monitoring)
  - ISO 27001: A.8.15 (Logging)
REMEDIATION: Implement structured audit logging for all admin actions with timestamp, actor, action, and target resource.
```

This allows stakeholders to understand the compliance impact of each finding and prioritize based on their regulatory requirements.

---

## Profile-Specific Emphasis

### FedRAMP Profile
Emphasizes: NIST 800-53 controls. All AC, AU, SC, SI families must score B+ or higher.

### HIPAA Profile
Emphasizes: Data Governance (PHI handling), IAM (minimum necessary access), Audit Logging (access to PHI).

### Financial Services Profile
Emphasizes: Change Management (SOX compliance), Audit Logging, Access Control, Third-Party Risk (vendor due diligence).

### SOC2 Type II Profile
Emphasizes: All CC (Common Criteria) and A1 (Availability) controls. Evidence of operating effectiveness over time.
