---
name: create
description: This skill should be used when the user asks to "create a postmortem", "write an incident postmortem", "build a postmortem from logs", "postmortem this incident", "write up this outage", "incident report", "RCA", "root cause analysis", "document this incident", or "post-incident review". It also applies when the user provides incident artifacts (logs, chat threads, screenshots, configs, monitoring data) and asks for an incident analysis or structured write-up.
argument-hint: "[description of what happened and where artifacts are]"
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "Agent"]
---

# Incident Postmortem Creator

Build comprehensive, structured incident postmortems from raw artifacts — chat threads, logs, screenshots, Kubernetes manifests, monitoring dashboards, and any other incident evidence.

## Workflow

### Step 1: Gather Artifacts

Collect all available incident evidence. Accept any combination of:

* **Pasted text** — chat threads, log snippets, timeline notes

* **Files on disk** — log files, exports, config files (read with Read/Glob)

* **Screenshots** — monitoring dashboards, error pages, alert screenshots (read with Read)

* **Kubernetes manifests / YAML configs** — deployments, services, webhooks

* **Slack/Teams exports** — conversation threads from incident channels

If the user provides a directory path, scan it recursively for relevant files:

```
Glob pattern: <artifact-dir>/**/*
```

If artifacts are sparse, ask the user what else is available. Do not proceed with fewer than one concrete artifact — a postmortem built purely from a verbal description is just a summary, not a postmortem.

### Step 2: Analyze Artifacts

For multiple artifact sources, dispatch the `artifact-analyzer` agent in parallel using the Agent tool — one agent per distinct artifact source (e.g., one for logs, one for chat thread, one for screenshots). Each agent returns structured findings.

For a single artifact source, analyze inline without dispatching an agent.

Extract from each artifact:

* **Timeline events** — timestamps, state changes, error onsets, recovery markers

* **Error signatures** — error messages, stack traces, HTTP status codes, exit codes

* **Metrics** — request counts, error rates, latency, resource utilization

* **Causal signals** — what triggered what, dependency chains, cascading failures

* **Root cause hypotheses** — patterns suggesting underlying causes

* **Resolution signals** — what fixed it, when recovery started/completed

### Step 3: Draft the Postmortem

Synthesize all artifact analysis into the fixed 8-section postmortem template defined in `references/postmortem-template.md`. Read that file for the exact structure and formatting requirements.

Key drafting principles:

* **Be specific** — use exact timestamps (UTC), error counts, service names, pod counts

* **Show causation** — connect trigger → root cause → cascading failure → impact

* **Quantify impact** — duration, affected users/services, error counts, revenue impact if known

* **Blameless tone** — focus on systems and processes, never individuals

* **Action items must be actionable** — each one has a type (Prevent/Detect/Mitigate/Fix), priority (Critical/High/Medium/Low), and clear next step

### Step 4: Identify and Fill Gaps

After drafting, review each section for completeness. Common gaps:

| Section         | Common gaps                                            |
| --------------- | ------------------------------------------------------ |
| Summary         | Missing duration or severity                           |
| Impact          | No user-facing impact described                        |
| Root Causes     | Single cause listed (look for contributing factors)    |
| Trigger         | Missing exact timestamp or audit log reference         |
| Resolution      | No distinction between immediate fix and full recovery |
| Detection       | Missing how it *should* have been detected             |
| Action Items    | Missing Detect-type items, or all items same priority  |
| Lessons Learned | Missing "where we got lucky"                           |

Present gaps to the user as specific questions:

```
I've drafted the postmortem but have gaps in these areas:
1. [Section]: [specific missing info]
2. [Section]: [specific missing info]
```

Incorporate answers and re-draft affected sections.

### Step 5: Write Output

Generate the postmortem slug from the incident description (kebab-case, max 60 chars). Example: `postmortems/2026-02-26-spot-vm-preemption-cluster-disruption.md`

Auto-fill metadata:

* **Date**: today's date (report creation date)

* **Incident Date**: extracted from artifacts, or ask user

* **Authors**: ask user

* **Status**: "Draft"

Write the final postmortem to:

```
./postmortems/YYYY-MM-DD-<slug>.md
```

Create the `postmortems/` directory if it doesn't exist. Then show the user a summary:

* File path written

* Key findings: root cause, impact duration, number of action items

* Any sections that could benefit from additional detail

## Quality Checklist

Before finalizing, verify:

* [ ] All 8 sections present and substantive

* [ ] Timestamps in UTC with consistent format

* [ ] Impact quantified with specific numbers

* [ ] Root causes explain the full causal chain (not just the trigger)

* [ ] Action items table has Type, Priority, and Status columns

* [ ] At least one Prevent, one Detect, and one Mitigate action item

* [ ] Lessons Learned has all three subsections (went well / went wrong / got lucky)

* [ ] Blameless tone throughout — no individual names in negative context

* [ ] Technical accuracy — service names, error messages match artifacts

## Reference Files

* **`references/postmortem-template.md`** — The complete 8-section postmortem template with formatting requirements and field descriptions. Read this before drafting.