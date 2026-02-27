---
name: research
description: Research the top 10 solutions in any market category, deep-dive each, and generate a PRD
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
  - WebSearch
  - WebFetch
  - AskUserQuestion
argument-hint: "<solution area>"
---

# Top 10 Competitive Research

Conduct a comprehensive competitive analysis of a solution area and generate a suite of research reports culminating in a PRD.

**The argument is the solution area to research** (e.g., "task management", "CRM software", "note-taking apps"). If no argument is provided, ask the user what solution area to research.

## Step 0: Create Output Directory

All reports are written to `./research/top-10/`. If the `research/` directory does not exist, create it. Always create the `top-10/` subdirectory inside it.

```bash
mkdir -p ./research/top-10
```

All file paths in subsequent steps are relative to `./research/top-10/`.

## Step 1: Identify Top 10 Solutions

Search the web to identify the top 10 solutions in the given area. Use multiple queries to cross-reference:

- `"best {area} software 2026"`
- `"top {area} tools"`
- `"G2 best {area}"`
- `"{area} market leaders"`
- `"{area} comparison"`

Cross-reference across sources (G2, Capterra, Gartner, industry blogs, Reddit). Rank by frequency of appearance, market share data, and review volume.

**Present the top 10 list to the user using AskUserQuestion.** Show the ranked list and ask the user to approve or suggest changes. Do not proceed until the user approves the list.

Once approved, slugify the area name (lowercase, hyphens for spaces, strip special characters) and write `research/top-10/top-10-{area}-report.md` using the template from the competitive-research skill's `references/report-templates.md`.

## Step 2: Deep Dive Each Solution (Parallel)

For each of the 10 approved solutions, launch a `solution-researcher` agent using the Task tool. **Launch all 10 in a single message to run them in parallel.**

For each agent, provide this prompt:

```
Research "{solution name}" as a {solution area} solution. Write a comprehensive deep-dive report covering features, pricing, what users love (with evidence from G2/Capterra/Reddit), and what users hate (with evidence).

Write the report to: research/top-10/{solution-slug}-report.md

Solution area: {area}
```

Use `subagent_type: "general-purpose"` for each Task tool call. The `solution-researcher` agent definition provides the research methodology — include its key instructions (features, pricing, user loves/hates with evidence, sources) in the prompt for each agent.

Wait for all 10 to complete before proceeding.

## Step 3: Generate Trends Report

Read all 10 individual solution reports. Analyze across these dimensions:

- **Common features**: Present in 7+ solutions (table stakes)
- **Common strengths**: What users consistently love
- **Common pain points**: What users consistently hate
- **Pricing patterns**: How pricing models compare
- **Architecture patterns**: Technical commonalities
- **Market convergence**: Previously differentiating features now standard

Write `research/top-10/{area}-trends.md` following the template from the competitive-research skill's `references/report-templates.md`.

## Step 4: Generate Unique Features Report

Read all 10 individual solution reports again. For each solution, extract features that:

- Are unique to that solution (not in most competitors)
- Are specifically called out as loved by users
- Represent innovative approaches

Write `research/top-10/{area}-unique-features.md` following the template from the competitive-research skill's `references/report-templates.md`.

## Step 5: Generate PRD

Read `{area}-trends.md` and `{area}-unique-features.md`. Synthesize into a full product requirements document:

1. **Problem Statement** — from common pain points
2. **Target Users** — from user bases of researched solutions
3. **Product Vision** — how to build something better
4. **Feature Requirements** — prioritized as P0 (table stakes), P1 (competitive parity), P2 (differentiation), P3 (blue ocean innovation)
5. **Success Metrics** — based on competitor benchmarks
6. **Competitive Positioning** — where the new product fits

Write `research/top-10/{area}-prd.md` following the template from the competitive-research skill's `references/report-templates.md`.

## Step 6: Summary

Present a summary to the user listing all files generated:

```
Research complete! Generated files in research/top-10/:
- top-10-{area}-report.md (overview of top 10 solutions)
- {solution-1}-report.md through {solution-10}-report.md (individual deep dives)
- {area}-trends.md (cross-solution trends and patterns)
- {area}-unique-features.md (standout features people love)
- {area}-prd.md (product requirements document)
```

## Important Rules

- Never skip the user approval step for the top 10 list
- Launch all 10 deep-dive agents in parallel, not sequentially
- Every claim in reports must be sourced
- Use the current year in search queries for recency
- Slugify all file names consistently (lowercase, hyphens, no special chars)
- Write all files to `./research/top-10/` — create the directory if it doesn't exist
- If a solution cannot be adequately researched (too niche, no reviews), note this in the report rather than fabricating content
