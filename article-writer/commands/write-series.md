---
name: write-series
description: Plan and write a series of related articles on a theme using the full article pipeline for each.
argument-hint: "<theme> [--count <number>] [--voice <name>] [--template <name>] [--research basic|light|medium|deep] [--checkpoints]"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
  - Agent
  - WebSearch
  - WebFetch
---

# Write Series

You are executing the series-writing pipeline. Parse the user's input to extract:

- **theme** (required) — the overarching series theme
- **--count <number>** — number of articles in the series (if not specified, let the series-planner agent decide based on the theme's scope)
- All flags from write-article are also accepted and will be passed through to each article: `--automatic`, `--checkpoints`, `--voice <name>`, `--words <count>`, `--pages <count>`, `--tone <tone>`, `--audience "<description>"`, `--template <name>`, `--research basic|light|medium|deep`

## Workflow

### Step 1: Series Planning

Use the **series-planner** agent. Pass it:
- The theme
- The count (if specified)
- Tone, audience, and template context (if specified)
- Research level preference

The agent should produce a series plan containing:
- Series title
- Series overview/thesis
- Number of articles
- For each article:
  - Title
  - Topic summary (2-3 sentences)
  - Key points to cover
  - How it connects to the previous and next articles
  - Suggested word count
- Reading order rationale
- Cross-referencing strategy (how articles should reference each other)

### Step 2: Save Series Plan

1. Generate a theme slug (lowercase, hyphens, no special chars, max 50 chars).
2. Get today's date as YYYYMMDD.
3. Create the series directory: `/Users/bo/code/articles/<YYYYMMDD>-<theme-slug>/`
4. Save the plan to `series-plan.md` at the series root.

### Step 3: User Approval

**Always pause here, even in automatic mode.** Present the series plan to the user:

```
Series: <title>
Articles: <count>

1. <article-1-title> — <brief description>
2. <article-2-title> — <brief description>
...

Approve this plan? You can also suggest changes.
```

- If the user approves ("yes", "approve", "looks good", "proceed", etc.), continue to Step 4.
- If the user suggests changes, rerun the series-planner agent with the feedback and return to Step 3.
- If the user rejects ("no", "cancel", "stop"), abort and inform the user.

### Step 4: Execute Articles

For each article in the series plan, sequentially:

1. Create a numbered subfolder: `01-<article-slug>/`, `02-<article-slug>/`, etc.
2. Execute the write-article pipeline for that article within its subfolder.
   - Pass all the user's original flags (voice, tone, audience, template, research level, words, checkpoints/automatic mode).
   - Pass the series context to each article's agents so they can reference the series theme and other articles.
3. Print progress after each article completes:
   ```
   [Article N/<total>] "<title>" — Complete
   ```

### Step 5: Series Metadata

After all articles are complete, create `metadata.md` at the series root:

```markdown
---
theme: <theme>
title: <series title>
date: <YYYY-MM-DD>
article_count: <number>
voice_profile: <name or "none">
template: <name or "none">
tone: <tone or "not specified">
audience: <audience or "not specified">
research_level: <level>
---

# Series Metadata

## Articles
1. <title> — `01-<slug>/06-final/article.md`
2. <title> — `02-<slug>/06-final/article.md`
...

## Timeline
- Series planning completed: <timestamp>
- Article 1 completed: <timestamp>
- Article 2 completed: <timestamp>
...
- Series completed: <timestamp>
```

## Completion

Print:
1. The series directory path.
2. Total word count across all articles.
3. List of all final article paths.
