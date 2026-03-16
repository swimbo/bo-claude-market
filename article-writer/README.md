# Article Writer

A Claude Code plugin for writing well-researched, professional articles with voice profiles, multi-stage pipelines, templates, and series support.

## Features

- **6-stage article pipeline**: Research, Outline, Draft, Style Critique, Content Critique, Final Edit
- **Voice profiles**: Analyze writing samples to capture your authentic voice
- **40 built-in templates**: Blog posts, case studies, thought leadership, executive communications, and more
- **Series writing**: Plan and execute multi-article series with narrative arcs
- **4 research depth levels**: Basic (web search), Light (Perplexity), Medium (Gemini), Deep (Opus)
- **Two execution modes**: Automatic (hands-off) or Checkpoints (interactive feedback)
- **Ideas tracking**: Store and track article ideas with production counts
- **Template creation**: Extract reusable templates from example articles

## Installation

```bash
claude --plugin-dir /path/to/article-writer
```

## Commands

| Command | Description |
|---------|-------------|
| `/write-article <topic>` | Write a complete article through the 6-stage pipeline |
| `/write-series <theme>` | Plan and write a multi-article series |
| `/analyze-voice <name>` | Create a voice profile from writing samples |
| `/manage-profiles` | List, view, set-default, or delete voice profiles |
| `/create-template <name>` | Create a template from example articles |
| `/manage-templates` | List, view, edit, or delete templates |

### write-article flags

```
--automatic          Run all stages without pausing (default)
--checkpoints        Pause after each stage for feedback
--voice <name>       Voice profile to use
--template <name>    Article template to follow
--research <level>   basic | light | medium | deep (default: basic)
--words <count>      Target word count (default: 1500)
--pages <count>      Target page count (1 page = 500 words)
--tone <descriptor>  e.g., conversational, academic, authoritative
--audience "<desc>"  Target audience description
--idea <text>        Link to an idea in ideas.md
```

### write-series flags

All `write-article` flags plus:

```
--count <number>     Number of articles in the series
```

## Output Structure

Articles are saved to `/Users/bo/code/articles/`:

```
<YYYYMMDD>-<topic-slug>/
  metadata.md
  01-research/research.md
  02-outline/outline.md
  03-draft/draft.md
  04-style-critique/critique.md
  05-content-critique/critique.md
  06-final/article.md
```

Series add a wrapper:

```
<YYYYMMDD>-<theme-slug>/
  series-plan.md
  metadata.md
  01-<article-slug>/
    01-research/research.md
    ...
    06-final/article.md
  02-<article-slug>/
    ...
```

## Voice Profiles

Create a voice profile by providing 3+ writing samples (files, URLs, or pasted text):

```
/analyze-voice my-voice
```

The profile captures: sentence structure, vocabulary, tone, paragraph patterns, rhetorical devices, transitions, openings, closings, and unique stylistic signatures.

Set a default profile so all articles use it automatically:

```
/manage-profiles set-default my-voice
```

Profiles are stored at `~/.claude/article-writer/profiles/`.

## Templates

### Built-in categories (40 templates)

- **Content Marketing** (3): Blog Post, Product Review, Email Newsletter
- **Technical Writing** (2): How-To Guide, Explained Simply
- **Business** (6): Case Study, White Paper, Problem/Root Cause/Solution, 5 Things I Learned, Myth vs Reality, The Pyramid
- **Marketing** (4): Landing Page, Social Media Campaign, Event Announcement, Framework Reveal
- **Journalism** (1): News Article
- **Personal Brand** (8): Kitchen Table Wisdom, Hero's Journey, Wounds to Wisdom, Then vs Now, Letter to Younger Self, This Made Me Cry, I Believe, Open Letter
- **Opinion & Analysis** (6): X Mistakes I Made, Before You Build, Prediction Post, What No One's Talking About, If I Ran the World, Imagine a World Where
- **Cross-Domain** (1): What X Can Teach Us About Y
- **Startup** (1): Build in Public
- **Executive** (10): Executive Summary, All-Hands Script, Strategic Initiative Brief, Performance Review, Crisis Playbook, Board Presentation, Change Management, Market Analysis, Decision Memo, Investor Update

### Create custom templates

```
/create-template my-template
```

Provide one or more example articles and the plugin extracts the structural pattern into a reusable template.

User templates are stored at `~/.claude/article-writer/templates/`.

## Research Depth Levels

| Level | Queries | Method | Best for |
|-------|---------|--------|----------|
| basic | 3-5 | WebSearch | Familiar topics, opinion pieces |
| light | 8-12 | Perplexity Sonar Deep | Most articles |
| medium | 15-20 | Gemini 3.1 Pro | Thought leadership, in-depth pieces |
| deep | 25+ | Opus 4.6 | Definitive, authoritative articles |

## Ideas Tracking

Link articles to ideas with `--idea`:

```
/write-article "Why Rust is eating the world" --idea "Rust adoption trends"
```

Ideas are tracked in `~/.claude/article-writer/ideas.md` with article counts.

## Configuration

Settings are stored in `~/.claude/article-writer.local.md`:

```yaml
default_profile: my-voice
```

## Agents

The pipeline uses 7 specialized agents:

| Agent | Model | Role |
|-------|-------|------|
| article-researcher | Opus | Deep research with tiered depth |
| content-planner | Sonnet | Outline creation |
| series-planner | Opus | Multi-article series design |
| draft-writer | Opus | Full draft with voice matching |
| style-critic | Sonnet | Voice and style evaluation |
| content-critic | Sonnet | Fact-checking and content review |
| final-editor | Opus | Final polish incorporating critiques |

## Skills

4 auto-activating skills provide domain knowledge:

- **Article Writing Pipeline** — pipeline orchestration and stage sequencing
- **Voice Profiling** — writing sample analysis and profile creation
- **Research Methodology** — research strategies and source evaluation
- **Template Engineering** — template creation from example articles
