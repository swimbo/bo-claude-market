# top-10

Competitive research plugin for Claude Code. Researches the top 10 solutions in any market category, deep-dives each one, and generates a product requirements document from the findings.

## What It Does

Given a solution area (e.g., "task management", "CRM software"), this plugin:

1. Identifies the top 10 solutions via web research
2. Presents the list for your approval
3. Deep-dives each solution in parallel (features, pricing, user loves, user hates)
4. Synthesizes trends across all solutions
5. Identifies unique features people love
6. Generates a full PRD based on the research

## Usage

```
/top-10:research "task management"
/top-10:research "CRM software"
/top-10:research "note-taking apps"
```

## Generated Files

All files are written to `./research/top-10/` (created automatically if it doesn't exist):

| File | Content |
|------|---------|
| `top-10-{area}-report.md` | Ranked list of top 10 solutions |
| `{solution}-report.md` (x10) | Individual deep-dive reports |
| `{area}-trends.md` | Common patterns across solutions |
| `{area}-unique-features.md` | Standout features people love |
| `{area}-prd.md` | Product requirements document |

## Components

- **Command**: `research` — orchestrates the full workflow
- **Skill**: `competitive-research` — research methodology and report templates
- **Agent**: `solution-researcher` — deep-dives a single solution (runs 10x in parallel)

## Installation

```bash
claude plugin install top-10 --marketplace bo-marketplace
```
