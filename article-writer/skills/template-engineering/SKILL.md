---
name: Template Engineering
description: This skill should be used when creating article templates from examples, designing content structures, or working with article templates. It applies when the user mentions "create template", "template from example", "article structure", "content template", "section pattern", or discusses how to turn an example article into a reusable template.
version: 1.0.0
---

# Template Engineering

## Overview

Templates capture the structural DNA of effective articles. A template defines the section skeleton, per-section guidance, variable placeholders, and length distribution of an article type so that the content planner can produce consistently structured outlines without starting from scratch each time.

## What Templates Capture

### Section Structure
The ordered list of sections that make up the article. Each section has a heading pattern, a defined purpose, and its position in the article's logical flow.

### Section Purposes
A brief description of what each section accomplishes for the reader. Examples: "Hook the reader with a surprising fact or provocative question", "Present the core argument with supporting evidence", "Address the primary counterargument and rebut it".

### Typical Lengths
Estimated word count for each section, expressed as a range (e.g., 200-400 words) or as a percentage of total article length. The sum of section lengths should approximate the template's estimated total length.

### Variable Placeholders
Named insertion points where topic-specific content goes. Each variable has a name, type, and description. Variables let the same template serve different topics.

### Tone Markers
Notes on the expected tone for each section. Some templates call for a shift in tone across sections (e.g., conversational opening, analytical middle, inspirational closing).

### Transition Patterns
Guidance on how sections should connect. Note whether transitions are explicit or implicit, whether sections end with a forward-looking statement, and whether the template uses recurring structural motifs.

### Opening and Closing Patterns
Specific patterns for how the article begins and ends. Templates often have strong opinions about openings (anecdote, statistic, bold claim) and closings (call to action, summary, callback).

### Evidence Patterns
The types of supporting evidence the template expects in each section: data, case studies, expert quotes, anecdotes, logical arguments, comparisons. Some templates call for specific evidence types at specific positions (e.g., "a case study always appears in section 3").

## Creating Templates from Examples

Follow this process when reverse-engineering a template from one or more example articles.

### Step 1: Read the Example Article(s)

Read each example article completely using the Read tool (for local files) or WebFetch (for URLs). Do not skim. Understanding the full piece is necessary to distinguish structural patterns from content-specific choices.

### Step 2: Identify the Structural Skeleton

Break the article into its component sections. For each section, record:

- The heading (or implied heading if the article uses prose transitions instead of headers)
- The section's start and end boundaries
- The section's role in the overall argument or narrative
- The approximate word count

Look for structural patterns that exist independent of the specific topic. The skeleton should be transferable to a different topic. Test this by mentally substituting a completely different topic and checking whether the structure still makes sense.

### Step 3: Determine Variables vs. Constants

Classify each element of the article as either variable (changes with topic) or constant (stays the same across articles using this template).

**Variables** include: the specific topic, names, data points, examples, quotes, and domain-specific terminology.

**Constants** include: the section ordering, the flow pattern (e.g., problem-solution-result), the types of evidence used (e.g., "always includes a case study in section 3"), and structural signatures (e.g., "every section opens with a one-sentence summary").

### Step 4: Extract Variable Placeholders

For each identified variable, create a placeholder with:

- **name**: A descriptive, snake_case identifier (e.g., `opening_anecdote`, `primary_statistic`, `expert_quote`).
- **type**: One of `text` (short, single-line), `textarea` (long, multi-paragraph), or `select` (choose from predefined options).
- **description**: What this variable represents and guidance for filling it.

For `select` type variables, include the list of valid options.

Mark variables as required or optional. Required variables must be filled for the template to work. Optional variables enhance the article but the template remains functional without them.

### Step 5: Note Length Distribution

Record the estimated total word count for the template. Then calculate each section's share of that total, expressed as both a word count range and a percentage.

Example:
```
Total: ~2,000 words
- Opening hook: 150-200 words (8-10%)
- Problem statement: 300-400 words (15-20%)
- Solution framework: 500-600 words (25-30%)
- Case study: 400-500 words (20-25%)
- Implementation guide: 300-400 words (15-20%)
- Closing: 100-150 words (5-8%)
```

### Step 6: Identify Difficulty and Tags

Assess the difficulty level of writing to this template: `beginner`, `intermediate`, or `advanced`. Consider the complexity of the structure, the sophistication of transitions required, and the depth of analysis expected.

Assign 2-5 tags from the template categories (see below) that describe the template's domain and purpose.

### Step 7: Write Transition Notes and Common Pitfalls

Document how sections should flow into each other. Note any recurring transition patterns observed in the example(s). Include a "Common Pitfalls" section that warns about mistakes writers commonly make when following this structure -- for example, making a case study too long and crowding out the analysis, or writing an opening hook that does not connect to the thesis.

## Template File Format

```markdown
---
name: Template Display Name
description: One-sentence description of what this template produces
category: content-marketing
estimated_length: 2000
difficulty_level: intermediate
tags:
  - content-marketing
  - how-to
  - educational
variables:
  - name: topic
    type: text
    description: The main subject of the article
  - name: target_audience
    type: text
    description: Who this article is written for
  - name: primary_problem
    type: textarea
    description: The core problem or challenge the article addresses
  - name: article_tone
    type: select
    description: The overall tone of the piece
    options:
      - conversational
      - authoritative
      - inspirational
---

# Template: Display Name

## Overview
Brief description of this template's purpose, ideal use cases, and the type of article it produces.

## Section 1: [Heading Pattern]
**Purpose**: [What this section accomplishes]
**Length**: [Word count range] ([percentage]%)
**Tone**: [Tone guidance]
**Guidance**: [Specific instructions for writing this section]

## Section 2: [Heading Pattern]
**Purpose**: [What this section accomplishes]
**Length**: [Word count range] ([percentage]%)
**Tone**: [Tone guidance]
**Guidance**: [Specific instructions for writing this section]

[Continue for all sections...]

## Transition Notes
[How sections should flow into each other]

## Common Pitfalls
[Mistakes to avoid when using this template]
```

## Working with Multiple Example Articles

When multiple examples are provided for the same template:

1. Read all examples completely before beginning analysis.
2. Identify patterns that appear across all (or most) examples. These are strong structural signals.
3. Note patterns that appear in only one example. These may be content-specific rather than structural.
4. Where examples disagree on structure, favor the pattern that appears most frequently.
5. If examples show meaningful variation in a section (e.g., some include a case study, others do not), make that section optional in the template and note the conditions under which it should be included.
6. Build the template from the consensus structure, noting variations as alternatives.
7. When examples come from different authors, focus purely on structural patterns and ignore voice characteristics, which belong in voice profiles rather than templates.
8. If examples vary significantly in length, note the length range in the template metadata and provide guidance on how to scale sections up or down.

## Template Storage

### Built-in Templates
Stored at `${CLAUDE_PLUGIN_ROOT}/templates/`, organized by category subdirectory. These ship with the article-writer plugin and serve as starting points.

### User Templates
Stored at `~/.claude/article-writer/templates/`. User-created templates take precedence over built-in templates with the same name.

When resolving a template name, check user templates first, then built-in templates.

## Template Usage in the Pipeline

The content planner (Stage 2: Outline) consumes templates as follows:

1. Load the specified template file.
2. Parse the YAML frontmatter for metadata, variables, and structural parameters.
3. Follow the section structure defined in the template body when constructing the outline.
4. Fill variable placeholders with topic-specific content derived from the research output.
5. Respect the per-section length guidance when estimating word counts in the outline.
6. Apply section-specific tone markers and transition guidance.

The template constrains the article's structure. It does not constrain the article's content, voice, or specific arguments. Those come from research, the topic requirements, and the voice profile.

When a template and voice profile are both active, the template governs structure and the profile governs style. There should be no conflict between them. If a template's tone markers conflict with a voice profile, the voice profile takes precedence on matters of style while the template takes precedence on matters of structure.

## Template Validation

Before saving a new template, validate it by checking:

- Every section has a defined purpose and length guidance.
- Variable placeholders have clear descriptions and appropriate types.
- The sum of per-section word counts approximates the estimated total length.
- The template works for at least two different topics (mentally test by substituting a different subject).
- Transition notes exist and provide actionable guidance.
- The difficulty level accurately reflects the structural complexity.

## Editing Existing Templates

When modifying a template:

1. Read the existing template fully before making changes.
2. Preserve the original structure unless the user explicitly requests restructuring.
3. When adding sections, consider the impact on the overall flow and adjust transition notes accordingly.
4. When removing sections, redistribute their word count allocation to remaining sections.
5. Update the estimated_length in frontmatter if section changes affect total word count.
6. Increment the version in a comment or description if the template is used by multiple users.

## Template Categories

Organize templates into these categories:

- **content-marketing**: Blog posts, lead magnets, SEO articles, newsletter content
- **technical-writing**: Tutorials, API guides, architecture docs, technical deep-dives
- **business**: Case studies, white papers, industry analysis, market reports
- **marketing**: Landing page copy, product announcements, campaign briefs
- **journalism**: News articles, feature stories, investigative pieces, interviews
- **personal-brand**: Thought leadership, LinkedIn articles, personal essays, career narratives
- **opinion-analysis**: Op-eds, commentary, analysis pieces, hot takes
- **cross-domain**: Templates that blend elements from multiple categories
- **startup**: Pitch narratives, launch announcements, fundraising updates, culture posts
- **executive**: Executive communications, shareholder letters, vision statements, internal memos

When creating a template, assign it to the single most appropriate category. Use tags for secondary categorization.

## Quick-Start Templates

When no example articles are provided and the user requests a template for a common article type, generate a template from domain knowledge. Base the structure on established patterns for that article type. For example:

- **How-to article**: Problem statement, prerequisites, step-by-step instructions, troubleshooting, conclusion.
- **Listicle**: Introduction with promise, numbered items with consistent structure, conclusion with takeaway.
- **Case study**: Context, challenge, approach, results, lessons learned.
- **Opinion piece**: Hook, thesis, supporting arguments (3), counterargument, rebuttal, conclusion.
- **Industry analysis**: Executive summary, market context, key trends, implications, forecast.

Mark quick-start templates as generated (not derived from examples) in the description so users know they may benefit from refinement based on actual example articles.
