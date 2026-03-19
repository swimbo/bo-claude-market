# incident-postmortem

A Claude Code plugin that builds comprehensive incident postmortems from raw artifacts — chat threads, logs, screenshots, Kubernetes manifests, and monitoring data.

## Features

- **Multi-source artifact intake** — paste text, point to files on disk, or provide screenshots
- **Parallel analysis** — dispatches analyzer agents to process multiple artifact sources simultaneously
- **Structured 8-section template** — Summary, Impact, Root Causes, Trigger, Resolution, Detection, Action Items, Lessons Learned
- **Gap detection** — identifies missing information and asks targeted questions
- **File output** — writes postmortems to `postmortems/YYYY-MM-DD-<slug>.md`

## Installation

```bash
claude --plugin-dir /path/to/incident-postmortem
```

## Usage

```
/incident-postmortem:create <description of what happened and where artifacts are>
```

### Examples

```
/incident-postmortem:create Production outage triggered by Spot VM preemption, logs in /tmp/incident-logs/
```

```
/incident-postmortem:create Redis connection failures caused cascading pod failures — chat thread pasted above, screenshots in ./screenshots/
```

Or provide artifacts first (paste logs, share file paths) and then run:

```
/incident-postmortem:create
```

## Components

| Component | Name | Purpose |
|-----------|------|---------|
| Skill | `create` | Main postmortem creation workflow — intake, analyze, draft, fill gaps, write |
| Agent | `artifact-analyzer` | Parallel analysis of individual artifact sources |

## Output

Postmortems are written to `./postmortems/` with the naming convention:

```
postmortems/YYYY-MM-DD-<incident-slug>.md
```

## Template Sections

1. **Summary** — One-paragraph incident overview
2. **Impact** — Duration, user impact, system impact with metrics
3. **Root Causes** — Numbered contributing causes with causal chain
4. **Trigger** — Specific initiating event with timestamp
5. **Resolution** — Immediate fix and full recovery timeline
6. **Detection** — How it was found and what should have caught it
7. **Action Items** — Table with Type (Prevent/Detect/Mitigate/Fix), Priority, Status
8. **Lessons Learned** — What went well, what went wrong, where we got lucky
