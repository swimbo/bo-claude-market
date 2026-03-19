# Incident Postmortem Template

Use this exact structure for all postmortems. Every section is required.

***

## Document Header

```markdown
# Incident Postmortem: <Title — concise description of what happened>

| Field | Value |
|-------|-------|
| **Date** | <Report creation date: Month DD, YYYY> |
| **Authors** | <Team or individuals> |
| **Status** | <Draft / In Review / Completed> |
| **Incident Date** | <When the incident occurred: Month DD, YYYY ~HH:MM AM/PM TZ (HH:MM UTC)> |
```

### Title Guidelines

* Lead with the user-visible or system-visible effect, not the internal cause

* Good: "Cluster-wide Disruption Triggered by Spot VM Preemption"

* Good: "Complete Login Outage Due to Redis Single Point of Failure"

* Bad: "Kyverno Bug" (too vague)

* Bad: "Production Issue on Feb 26" (no information)

***

## Section 1: Summary

One paragraph (3-6 sentences) covering:

* When it started (exact timestamp in local + UTC)

* What system/application was affected

* How long it lasted

* What triggered it (one sentence)

* What the root cause was (one sentence)

* How it was resolved (one sentence)

**Tone:** Factual, blameless, concise. This paragraph should stand alone as a complete incident overview.

***

## Section 2: Impact

Three subsections:

### Duration

Single line: `~XX minutes of total degradation (HH:MM UTC to ~HH:MM UTC).`

### User Impact

1-3 sentences describing what users experienced. Be specific:

* Could they log in? Use the product? See errors?

* Was it total or partial outage?

* How many users were affected (if known)?

### System Impact

Bulleted list of technical impacts with metrics:

```markdown
- <System/component>: <what happened> (<count/metric>, severity).
- <System/component>: <what happened> (<count/metric>, severity).
```

Use severity labels: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`

***

## Section 3: Root Causes

Numbered list of contributing causes, ordered from most fundamental to most proximate. Each cause gets:

* **Bold title** summarizing the cause

* 2-4 sentences explaining *why* this was a problem and *how* it contributed

Look for multiple contributing causes — incidents rarely have a single root cause. Common patterns:

* Single point of failure + missing redundancy

* Strict policy + no fallback

* Dependency chain with no circuit breaker

* Configuration drift + missing alerting

***

## Section 4: Trigger

The specific event that initiated the incident:

* Exact timestamp (UTC)

* What happened (e.g., VM preemption, deploy, config change)

* Any audit log references or event IDs

Format:

```markdown
The incident was triggered at HH:MM:SS UTC when <specific event>.

Audit Log Event: `<log line or event reference>`
```

**Important:** The trigger is NOT the root cause. The trigger is the proximate event; root causes explain why the trigger led to an incident.

***

## Section 5: Resolution

Two parts:

### Immediate Resolution

How the acute issue was resolved (automated recovery, manual intervention, rollback, etc.). Include timestamps.

### Full Recovery

How long until the system was fully stable. Explain any cascading recovery process (e.g., dependent services restarting sequentially).

Include specific timestamps for key recovery milestones.

***

## Section 6: Detection

Two subsections:

### How It Was Detected

How the team actually learned about the incident:

* Automated alert? Which one?

* User report? Through what channel?

* Synthetic monitoring? Which check?

* Post-hoc discovery?

### Detection Gaps

What *should* have detected it but didn't:

* Missing alerts

* Missing monitors

* Gaps in synthetic checks

* Log-based signals that were present but not monitored

This section should directly inform Detect-type action items.

***

## Section 7: Action Items

Table format with these exact columns:

```markdown
| Action Item | Type | Priority | Status |
|-------------|------|----------|--------|
| <Description of what to do> | <Type> | <Priority> | <Status> |
```

### Type Values

* **Prevent** — Eliminates the root cause so this class of incident cannot recur

* **Detect** — Ensures earlier/faster detection if a similar incident occurs

* **Mitigate** — Reduces blast radius or impact severity

* **Fix** — Addresses a related bug or config issue discovered during investigation

### Priority Values

* **Critical** — Must be done within 1 week; incident will recur without this

* **High** — Must be done within 1 month; significant risk remains

* **Medium** — Should be done within 1 quarter; improves resilience

* **Low** — Nice to have; minor improvement

### Status Values

* **TODO** — Not yet started

* **IN PROGRESS** — Work has begun

* **DONE** — Completed (include date)

### Action Item Quality

Each action item description should:

* Start with a verb (Remove, Implement, Migrate, Improve, Evaluate, Fix, Add)

* Be specific enough that an engineer can start working on it

* Include the *why* after a colon if not obvious

Aim for 5-10 action items. Every postmortem should have at least:

* 1 Prevent item

* 1 Detect item

* 1 Mitigate item

***

## Section 8: Lessons Learned

Three required subsections:

### What Went Well

Things that worked as designed, limited damage, or aided recovery:

* Automated systems that helped

* Good engineering decisions that paid off

* Effective team response

### What Went Wrong

Systemic failures exposed by the incident:

* Missing redundancy or HA

* Gaps in observability

* Architectural weaknesses

* Process failures

### Where We Got Lucky

Things that could have made the incident worse but didn't:

* Timing (off-peak hours, quick provisioning)

* Scope limitations (only affected subset)

* Coincidences that helped (someone happened to be watching)

This subsection is often overlooked but critical — it reveals hidden risks that need addressing even though they didn't materialize this time.

***

## Formatting Requirements

* All timestamps in UTC (with local time in parentheses where helpful)

* Use markdown headers (`##`, `###`) for sections

* Use code blocks for log entries, audit events, and commands

* Use tables for structured data (impact metrics, action items)

* Bold key terms and service names on first mention

* Severity labels in ALL CAPS: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`

* Keep paragraphs concise — 2-5 sentences each

* Use bulleted lists for enumerations of 3+ items