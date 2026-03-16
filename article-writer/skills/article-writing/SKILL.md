---
name: Article Writing Pipeline
description: This skill should be used when writing articles, creating content, generating drafts, or orchestrating the article writing pipeline. It applies when the user asks to "write an article", "create content", "generate a draft", "article pipeline", or discusses article structure, writing workflow, or content creation process.
version: 1.0.0
---

# Article Writing Pipeline

## Overview

The article writing pipeline transforms a topic and requirements into a polished, publication-ready article through six sequential stages. Each stage produces artifacts that feed into the next, creating a traceable lineage from raw research to final output.

## The Six-Stage Pipeline

### Stage 1: Research

Gather information on the topic using the configured research depth level. Produce a structured research document containing key facts, statistics, expert opinions, contrarian viewpoints, and source URLs. Use WebSearch for discovery and WebFetch for retrieving full article content. Organize findings into an executive summary, key facts, expert opinions, contrarian viewpoints, sources list, and recommended angles. Store output in `01-research/`.

The research depth level determines the number of queries, depth of cross-referencing, and synthesis model used. See the Research Methodology skill for full details on each level.

### Stage 2: Outline

Read the research output. If a template is configured, load it and follow its structural pattern. Produce a detailed outline with section headings, bullet points for each section's content, estimated word counts per section, and placement notes for statistics and quotes. Include a thesis statement or central argument at the top of the outline. Map research findings to specific sections so each claim has a planned home. Store output in `02-outline/`.

When no template is provided, derive the structure from the topic, audience, and research findings. For argumentative pieces, use claim-evidence-analysis flow. For educational pieces, use progressive complexity. For narrative pieces, use chronological or thematic arcs.

### Stage 3: Draft

Read the outline and research outputs. If a voice profile is configured, load it and adopt the identified writing patterns throughout the draft. Write the full article according to the outline structure, hitting target word count within 10% tolerance. Integrate statistics and quotes from the research document naturally. Ensure each section fulfills its purpose as defined in the outline. Write transitions between sections that maintain narrative momentum. Store output in `03-draft/`.

Do not pad the draft with filler to meet word count. If the content naturally runs short, deepen analysis or add supporting examples. If it runs long, tighten prose rather than cutting substantive content.

### Stage 4: Style Critique

Read the draft. If a voice profile is configured, evaluate the draft against it. Assess sentence variety, vocabulary consistency, tone alignment, transition quality, paragraph rhythm, and overall readability. Produce a critique document with specific line-level feedback and a numerical score (1-10) for each dimension. Identify the three strongest stylistic elements and the three areas most in need of improvement. When a voice profile is active, include a voice fidelity score with examples of successful and unsuccessful voice matching. Store output in `04-style-critique/`.

### Stage 5: Content Critique

Read the draft and research outputs. Evaluate factual accuracy by cross-referencing claims against research sources. Check argument coherence, logical flow, completeness of coverage, and whether the article fulfills its stated purpose. Flag unsupported claims, logical gaps, missing perspectives, and structural weaknesses. Verify that statistics are cited accurately and that quotes are attributed correctly. Check that the article addresses the target audience at the appropriate level. Produce a critique document with actionable revision notes, organized by severity (critical, major, minor). Store output in `05-content-critique/`.

### Stage 6: Final Edit

Read the draft, style critique, and content critique. Apply all valid critique feedback. Fix factual issues, strengthen weak sections, improve transitions, tighten prose, and correct any grammar or punctuation errors. Resolve any conflicts between style and content critique recommendations by prioritizing factual accuracy over stylistic preference. Produce the final polished article. Verify that the final word count is within 10% of the target. Store output in `06-final/`.

## Stage Connectivity

Each stage reads from previous stage output directories and writes to its own. Never skip stages. If a stage has no meaningful work (e.g., style critique with no voice profile), still run it and produce output noting the reduced scope.

The pipeline runner tracks stage completion in `metadata.md` at the article root directory. If the pipeline is interrupted, resume from the last incomplete stage.

## Output Directory Structure

All articles are written to a date-and-topic-stamped directory:

```
/Users/bo/code/articles/<YYYYMMDD>-<topic-slug>/
  metadata.md
  01-research/
    research.md
  02-outline/
    outline.md
  03-draft/
    draft.md
  04-style-critique/
    style-critique.md
  05-content-critique/
    content-critique.md
  06-final/
    final.md
```

Generate the `<topic-slug>` by lowercasing the topic, replacing spaces with hyphens, removing special characters, and truncating to 50 characters.

## Execution Modes

### Automatic Mode (default)

Run all six stages without pausing. Print a one-line status update after each stage completes (e.g., "Stage 2/6 complete: Outline generated, 8 sections, ~2,400 words planned"). Deliver the final article path when finished.

Use `--automatic` or omit mode flag to activate.

Status update format for each stage:
```
Stage N/6 complete: [Stage Name] — [key metric or summary]
```

### Checkpoint Mode

Pause after each stage and present the output summary to the user. Wait for explicit approval or feedback before proceeding to the next stage. If the user provides feedback, incorporate it before moving on. Use this mode when the user wants creative control over the process.

Use `--checkpoints` to activate.

At each checkpoint, present:
1. A summary of what was produced (key decisions, word counts, structure choices).
2. Any open questions or trade-offs that could go either way.
3. A prompt asking the user to approve, provide feedback, or request revisions.

If the user requests revisions, re-run only the current stage with the feedback incorporated. Do not re-run previous stages unless the user explicitly asks.

## Voice Profile Integration

When a voice profile is specified (via `--voice <profile-name>` or the default profile in config), load the profile before Stage 3 (Draft). The draft writer must adopt the voice characteristics documented in the profile. In Stage 4 (Style Critique), evaluate the draft against the profile's documented patterns and flag deviations.

If no voice profile is specified and no default is set, skip voice-specific evaluation in the style critique but still assess general writing quality.

## Template Integration

When a template is specified (via `--template <template-name>`), load the template before Stage 2 (Outline). The content planner must follow the template's section structure, variable placeholders, and length guidance when constructing the outline. The template constrains structure, not content.

If no template is specified, the outline stage uses the research output and topic requirements to determine an appropriate structure organically.

## Research Depth Levels

Control research thoroughness with `--research <level>`:

- **basic**: Fast, surface-level research. Suitable for familiar topics or opinion pieces.
- **light**: Moderate research with cross-referencing. Default level. Good for most articles.
- **medium**: Thorough research across multiple angles. For thought leadership and in-depth pieces.
- **deep**: Exhaustive, comprehensive research. For definitive, authoritative articles.

See the Research Methodology skill for detailed behavior at each level.

## Article Requirements

Specify article parameters with these flags:

- `--words <count>`: Target word count for the final article.
- `--pages <count>`: Alternative to `--words`. Convert using 1 page = 500 words.
- `--tone <descriptor>`: Tone guidance (e.g., "conversational", "authoritative", "playful"). Passed to draft writer and style critic.
- `--audience <descriptor>`: Target audience (e.g., "senior engineers", "startup founders", "general public"). Influences vocabulary, assumed knowledge level, and examples.

If both `--words` and `--pages` are provided, `--words` takes precedence. If neither is specified, default to 1,500 words.

## Ideas Tracking

When `--idea <idea-title>` is provided, link the article to the corresponding entry in `ideas.md`. On successful pipeline completion (Stage 6 produces output), increment the article count for that idea entry. If the idea title does not exist in `ideas.md`, create a new entry.

The ideas file is located at `~/.claude/article-writer/ideas.md`. Each entry tracks: idea title, description, article count, and list of article paths produced from this idea. This enables the user to see which ideas have been explored and which remain unwritten.

## Metadata Generation

At pipeline start, create `metadata.md` in the article root directory containing:

- Article title and topic
- All parameter values (words, tone, audience, voice, template, research level)
- Pipeline start timestamp (ISO 8601)
- Stage completion timestamps (updated as each stage finishes)
- Idea link (if applicable)
- Final word count (updated after Stage 6)
- Output file paths

Update `metadata.md` after each stage completes.

## Quality Standards

A minimum viable article must meet all of the following criteria:

- **Well-researched**: Claims are supported by identified sources. Statistics are verified.
- **Clearly structured**: Logical flow from introduction through body to conclusion. Each section has a clear purpose.
- **Voice-consistent**: If a voice profile is active, the article reads as though the profiled author wrote it.
- **Fact-checked**: No unverified claims presented as fact. Uncertain claims are qualified.
- **Polished**: Free of grammatical errors, awkward phrasing, and structural issues. Transitions are smooth. Opening hooks the reader. Closing provides resolution.

Do not mark the pipeline as complete if the final article fails any of these criteria. Instead, note the deficiency and run an additional editing pass.

## Error Handling and Recovery

If a stage fails (e.g., WebSearch is unavailable during research, or the draft exceeds word count by more than 20%), log the error in `metadata.md` and attempt recovery:

- **Research failures**: Retry failed queries. If WebSearch is entirely unavailable, note the limitation and proceed with available information, flagging the research as incomplete.
- **Word count overruns**: In the final edit stage, tighten prose and remove redundant content. If still over target, prioritize cutting the weakest sections identified in the content critique.
- **Stage file missing**: If a previous stage's output file is missing or corrupted, re-run that stage before proceeding.

When resuming an interrupted pipeline, read `metadata.md` to determine the last completed stage and start from the next one. Do not re-run completed stages unless explicitly requested.

## Command Summary

```
write-article <topic>
  --words <count>          Target word count (default: 1500)
  --pages <count>          Target page count (1 page = 500 words)
  --tone <descriptor>      Tone guidance
  --audience <descriptor>  Target audience
  --voice <profile>        Voice profile name
  --template <name>        Article template name
  --research <level>       Research depth: basic|light|medium|deep (default: light)
  --idea <title>           Link to idea in ideas.md
  --automatic              Run without pausing (default)
  --checkpoints            Pause after each stage for feedback
```
