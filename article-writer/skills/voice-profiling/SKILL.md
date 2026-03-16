---
name: Voice Profiling
description: This skill should be used when analyzing writing samples, creating voice profiles, understanding writing style, or matching a writer's voice. It applies when the user mentions "voice profile", "writing style", "analyze my writing", "match my voice", "writing samples", or discusses tone, style characteristics, or author voice.
version: 1.0.0
---

# Voice Profiling

## Overview

A voice profile is a structured document that captures the distinctive characteristics of a writer's style. It enables the article pipeline to produce drafts that sound like a specific author rather than generic AI-generated text. Profiles are created by analyzing writing samples and extracting recurring patterns.

## What a Voice Profile Captures

Analyze and document each of the following dimensions:

### Sentence Structure Patterns
Identify the writer's typical sentence lengths (short, medium, long, mixed). Note whether they favor simple, compound, or complex sentences. Record the ratio of declarative to interrogative to exclamatory sentences. Document any signature sentence constructions (e.g., fragments for emphasis, parenthetical asides, em-dash interruptions). Pay attention to how sentence length varies within paragraphs -- some writers alternate between long and short sentences rhythmically, while others maintain consistent length.

### Vocabulary Preferences
Note the general vocabulary level (plain, moderate, elevated). Identify recurring words or phrases the writer favors. Document whether they use jargon freely or explain technical terms. Record preferences for concrete vs. abstract language. Note any verbal tics or filler phrases that recur (e.g., "essentially", "in other words", "the thing is"). Document whether the writer uses first person ("I"), second person ("you"), or third person, and how frequently they shift between them.

### Tone and Register
Characterize the overall tone (formal, conversational, academic, irreverent, etc.). Note how the tone shifts between sections (e.g., casual in intros, precise in analysis). Document the writer's relationship with the reader (peer-to-peer, teacher-student, authority-to-audience).

### Paragraph Structure
Record typical paragraph length (in sentences and approximate word count). Note whether paragraphs tend to lead with topic sentences or build to a point. Document the use of single-sentence paragraphs for emphasis. Record whether the writer uses subheadings frequently, sparingly, or never. Note the typical number of paragraphs per section and whether section length is consistent or varied.

### Rhetorical Devices
Identify frequently used devices: repetition, parallelism, rule-of-three, rhetorical questions, direct address, humor, irony, hyperbole, understatement. Note the density of device usage -- some writers use them sparingly for emphasis, while others employ them as a constant stylistic texture. Record specific examples from the samples for each identified device.

### Transition Patterns
Document how the writer moves between ideas. Note whether transitions are explicit ("However," "Moreover,") or implicit (juxtaposition, thematic links). Record the use of transitional paragraphs vs. transitional phrases.

### Opening and Closing Patterns
Characterize how the writer begins pieces (anecdote, bold claim, question, scene-setting, statistic). Document closing patterns (call to action, summary, provocative question, callback to opening, future-looking statement).

### Use of Metaphors and Analogies
Note frequency and type of figurative language. Document whether metaphors are drawn from specific domains (sports, science, everyday life). Record extended vs. brief metaphor usage.

### Formality Level
Rate on a scale from 1 (highly informal) to 10 (highly formal). Note use of contractions, colloquialisms, slang, or conversational fillers.

### Unique Signatures
Capture anything distinctive that does not fit the above categories. Examples: consistent use of numbered lists, a habit of citing historical parallels, always ending with a one-word sentence, opening every section with a question.

## Sample Requirements

Require a minimum of 3 writing samples for a reliable profile. More samples produce better profiles. Ideal sample count is 5-10.

Accept samples from these sources:

- **File paths**: Use the Read tool to load local files.
- **URLs**: Use WebFetch to retrieve web-published articles.
- **Pasted text**: Accept text provided directly in the conversation.

Each sample should be at least 500 words. Shorter samples can supplement but should not be the only inputs. When possible, collect samples that span different topics, contexts, and time periods to capture the writer's full range rather than a narrow slice of their output.

## Analysis Methodology

Follow this process when creating or updating a profile:

1. Read all provided samples completely before beginning analysis.
2. For each dimension listed above, scan across all samples looking for recurring patterns.
3. Only document patterns that appear in at least 2 of 3 samples (or the majority of samples if more are provided). A pattern appearing in a single sample may be incidental rather than characteristic.
4. Note the frequency of each pattern (always, usually, sometimes, occasionally).
5. Distinguish between deliberate style choices and incidental occurrences. Deliberate choices are consistent and appear across different topics and contexts. Incidental patterns appear sporadically or are topic-dependent.
6. When patterns conflict across samples (e.g., formal in one, casual in another), note the range and hypothesize about the conditions that trigger each mode.
7. Produce a confidence rating for each dimension: high (pattern clearly established across most samples), medium (pattern present but with notable exceptions), or low (insufficient evidence, pattern may be incidental).
8. Write a "Usage Notes" section at the end of the profile that synthesizes the most important patterns into practical guidance for the draft writer. This section should read as a brief, actionable style guide.

## Profile Storage

Store profiles at:

```
~/.claude/article-writer/profiles/<name>.md
```

The `<name>` is a lowercase, hyphen-separated identifier (e.g., `bo-chen`, `marketing-team`, `technical-blog`).

## Profile Structure

Each profile file uses the following format:

```markdown
---
name: Display Name
created: 2026-03-15T10:30:00Z
updated: 2026-03-15T10:30:00Z
sample_count: 5
sources:
  - path/to/sample1.md
  - https://example.com/article
  - "pasted text (first 50 chars...)"
---

# Voice Profile: Display Name

## Sentence Structure
[Analysis of sentence patterns]

## Vocabulary
[Analysis of vocabulary preferences]

## Tone and Register
[Analysis of tone characteristics]

## Paragraph Structure
[Analysis of paragraph patterns]

## Rhetorical Devices
[Analysis of device usage]

## Transitions
[Analysis of transition patterns]

## Openings and Closings
[Analysis of opening/closing patterns]

## Figurative Language
[Analysis of metaphor/analogy usage]

## Formality
[Formality rating and evidence]

## Unique Signatures
[Distinctive characteristics]

## Usage Notes
[Guidance for the draft writer on how to apply this profile]
```

## Updating Profiles

When new samples are provided for an existing profile:

1. Read the existing profile.
2. Analyze the new samples.
3. Merge findings: strengthen patterns confirmed by new samples, weaken or remove patterns contradicted by new evidence, add newly identified patterns.
4. Increment `sample_count`.
5. Add new sources to the `sources` list.
6. Update the `updated` timestamp.
7. Write the merged profile back to disk.

Do not discard previous analysis. Treat profile updates as refinements, not replacements.

If new samples significantly contradict established patterns, note the conflict and consider whether the writer's style has evolved or whether the new samples represent a different register. In the latter case, suggest creating a separate profile for that register.

## How Profiles Are Used in the Pipeline

- **Draft Writer (Stage 3)**: Load the active profile before writing. Adopt the documented patterns for sentence structure, vocabulary, tone, transitions, and all other dimensions. The profile is a target to match, not a rigid template. Prioritize naturalness over mechanical pattern matching.
- **Style Critic (Stage 4)**: Load the active profile and evaluate the draft against each dimension. Flag significant deviations. Score voice consistency on a 1-10 scale. Provide specific examples of both successful voice matching and deviations.

## Setting a Default Profile

Set the default voice profile using the manage-profiles command. The default profile name is stored in the article-writer configuration. When no `--voice` flag is passed to the pipeline, the default profile is used. If no default is set and no flag is provided, the pipeline runs without voice profiling.

## Tips for Better Profiles

- Use samples from diverse topics. A profile built from articles about only one subject may capture topic-specific language as style.
- Include samples of different lengths. Short-form and long-form writing often reveal different aspects of voice.
- Include both the writer's best work and their everyday writing. Published pieces may be heavily edited; informal writing reveals natural voice.
- Revisit profiles after 6-12 months of writing. Voices evolve, and profiles should reflect current style.
- When the writer has multiple distinct registers (e.g., technical blog vs. social media), consider creating separate profiles for each register rather than one blended profile.

## Profile Comparison

When asked to compare two voice profiles, produce a side-by-side analysis highlighting:

- Key differences in tone, formality, and sentence structure.
- Shared patterns that appear in both profiles.
- Which profile would be more appropriate for a given article type or audience.
- Recommendations for blending elements from both profiles if requested.

## Common Pitfalls

- Do not confuse topic-specific vocabulary with the writer's general vocabulary preferences. If a writer uses technical jargon in a technical article, that reflects the topic, not necessarily their default register.
- Do not over-index on a single memorable sentence or paragraph. Voice profiles should reflect habitual patterns, not exceptional moments.
- Do not assume that the most recent sample represents the writer's current style. Explicitly check publication dates and note any temporal evolution.
- Do not create profiles with fewer than 3 samples. The risk of capturing noise instead of signal is too high. If fewer samples are available, flag the profile as provisional and recommend additional samples.
