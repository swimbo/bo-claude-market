---
name: write-article
description: Write a complete article through a multi-stage pipeline with research, outlining, drafting, critique, and final editing.
argument-hint: "<topic> [--voice <name>] [--template <name>] [--research basic|light|medium|deep] [--words <count>] [--tone <tone>] [--audience \"<desc>\"] [--checkpoints]"
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

# Write Article

You are executing the article-writing pipeline. Parse the user's input to extract:

- **topic** (required) — the article subject
- **--automatic** (default if neither mode flag given) — run all stages without pausing
- **--checkpoints** — pause after each stage for user feedback
- **--voice <name>** — voice profile to apply
- **--words <count>** — target word count
- **--pages <count>** — target page count (estimate ~300 words/page if --words not also given)
- **--tone <tone>** — e.g. conversational, academic, professional, witty
- **--audience "<description>"** — target reader description
- **--template <name>** — article template to follow
- **--research basic|light|medium|deep** — research depth (default: basic)
- **--idea <idea-text>** — links this article to an idea in ideas.md

## Setup

1. Generate a topic slug from the topic (lowercase, hyphens, no special chars, max 50 chars).
2. Get today's date as YYYYMMDD.
3. Create the article directory: `/Users/bo/code/articles/<YYYYMMDD>-<topic-slug>/`
4. Create numbered stage subdirectories as you reach each stage.

### Voice Profile

- If `--voice` is specified, read the profile from `~/.claude/article-writer/profiles/<name>.md`.
- If `--voice` is not specified, read `~/.claude/article-writer.local.md` and check for a `default_profile` setting. If found, load that profile.
- If no profile is found by either method, proceed without a voice profile.
- Pass the voice profile content to every agent that produces prose (draft-writer, final-editor).

### Template

- If `--template` is specified, search for the template in this order:
  1. `${CLAUDE_PLUGIN_ROOT}/templates/` (search recursively)
  2. `~/.claude/article-writer/templates/`
- Read the template file and pass its structure to the content-planner agent.

### Idea Linking

- If `--idea` is specified, read `~/.claude/article-writer/ideas.md`.
- Search for a matching idea. If not found, append it as a new idea entry.
- After the pipeline completes successfully, increment the article count for that idea.

## Pipeline Stages

Execute these stages sequentially. Each stage saves its output to a numbered subfolder within the article directory.

### Stage 1: Research → `01-research/research.md`

Use the **article-researcher** agent. Pass it the topic, audience, and tone context.

Research depth determines the approach:
- **basic**: Use the WebSearch tool for straightforward queries about the topic. Gather key facts, statistics, and expert perspectives.
- **light**: Conduct multi-query research using Perplexity Sonar Deep. Break the topic into 3-5 research questions and synthesize findings.
- **medium**: Conduct multi-query research using Gemini 3.1 Pro. Break into 5-8 research questions, cross-reference sources, identify contradictions and consensus.
- **deep**: Conduct comprehensive multi-query research using Opus 4.6. Break into 8-12 research questions, cross-reference extensively, evaluate source credibility, identify gaps in available information.

Save the research output to `01-research/research.md`.

### Stage 2: Outline → `02-outline/outline.md`

Use the **content-planner** agent. Pass it:
- The research from Stage 1
- Word/page count targets
- Tone and audience requirements
- Template structure (if a template was specified)

The agent should produce a detailed outline with section headings, key points per section, estimated word counts per section, and transition notes.

Save to `02-outline/outline.md`.

### Stage 3: Draft → `03-draft/draft.md`

Use the **draft-writer** agent. Pass it:
- The outline from Stage 2
- The research from Stage 1
- Voice profile (if loaded)
- Tone and audience requirements

The agent writes the full first draft following the outline.

Save to `03-draft/draft.md`.

### Stage 4: Style Critique → `04-style-critique/critique.md`

Use the **style-critic** agent. Pass it:
- The draft from Stage 3
- Voice profile (if loaded)
- Tone and audience requirements

The agent evaluates: prose quality, voice consistency, readability, sentence variety, word choice, flow and transitions, opening/closing effectiveness.

Save the critique to `04-style-critique/critique.md`.

### Stage 5: Content Critique → `05-content-critique/critique.md`

Use the **content-critic** agent. Pass it:
- The draft from Stage 3
- The research from Stage 1
- The outline from Stage 2

The agent evaluates: factual accuracy against research, argument strength, completeness (does it cover all outline points?), logical flow, evidence usage, missing perspectives, potential counterarguments not addressed.

Save the critique to `05-content-critique/critique.md`.

### Stage 6: Final Edit → `06-final/article.md`

Use the **final-editor** agent. Pass it:
- The draft from Stage 3
- Both critiques from Stages 4 and 5
- Voice profile (if loaded)
- Word/page count targets

The agent produces the final polished article, incorporating feedback from both critiques.

Save to `06-final/article.md`.

## Mode Behavior

### Automatic Mode (default)

Between each stage, print a brief status update:
```
[Stage N/6] <Stage Name> — Complete ✓
```
Do not ask for user input. Proceed directly to the next stage.

### Checkpoints Mode

After each stage completes:
1. Print the stage name and a brief summary of the output (e.g., key sections in outline, word count of draft, top critique points).
2. Ask: "Review the output at `<path>`. Provide feedback to revise this stage, or say 'proceed' to continue."
3. If the user provides feedback, rerun the stage with the feedback incorporated.
4. If the user says "proceed", "continue", "next", "ok", "looks good", or similar, move to the next stage.

## Metadata

After all stages complete, create `metadata.md` at the article directory root with:

```markdown
---
topic: <topic>
date: <YYYY-MM-DD>
words_target: <count or "not specified">
pages_target: <count or "not specified">
tone: <tone or "not specified">
audience: <audience or "not specified">
voice_profile: <name or "none">
template: <name or "none">
research_level: <basic|light|medium|deep>
idea_origin: <idea text or "none">
---

# Article Metadata

## Timeline
- Research started: <timestamp>
- Research completed: <timestamp>
- Outline completed: <timestamp>
- Draft completed: <timestamp>
- Style critique completed: <timestamp>
- Content critique completed: <timestamp>
- Final edit completed: <timestamp>

## Files
- Research: 01-research/research.md
- Outline: 02-outline/outline.md
- Draft: 03-draft/draft.md
- Style Critique: 04-style-critique/critique.md
- Content Critique: 05-content-critique/critique.md
- Final Article: 06-final/article.md
```

## Completion

After writing metadata:
1. If `--idea` was used, update the idea's article count in `~/.claude/article-writer/ideas.md`.
2. Print the path to the final article.
3. Print word count of the final article.
4. Print a one-line summary of the article.
