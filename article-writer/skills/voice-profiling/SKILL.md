---
name: Voice Profiling
description: This skill should be used when analyzing writing samples, creating voice profiles, understanding writing style, or matching a writer's voice. It applies when the user mentions "voice profile", "writing style", "analyze my writing", "match my voice", "writing samples", or discusses tone, style characteristics, or author voice.
version: 1.0.0
---

# Voice Profiling

## Overview

A voice profile is a structured document that captures the distinctive characteristics of a writer's style. It enables the article pipeline to produce drafts that sound like a specific author rather than generic AI-generated text. Profiles are created by analyzing writing samples and extracting recurring patterns.

## What a Voice Profile Captures

A voice profile must go beyond describing what a writer does — it must also specify what they never do, what they do especially well (named moves), and provide concrete examples of both success and failure. The sections that most distinguish a useful profile from a generic one are Anti-Patterns, Signature Moves, and the Revision Checklist.

Analyze and document each of the following dimensions:

### Sentence Structure Patterns
Identify the writer's typical sentence lengths (short, medium, long, mixed). Note whether they favor simple, compound, or complex sentences. Record the ratio of declarative to interrogative to exclamatory sentences. Document any signature sentence constructions (e.g., fragments for emphasis, parenthetical asides, em-dash interruptions). Pay attention to how sentence length varies within paragraphs -- some writers alternate between long and short sentences rhythmically, while others maintain consistent length.

### Vocabulary Preferences
Note the general vocabulary level (plain, moderate, elevated). Identify recurring words or phrases the writer favors. Document whether they use jargon freely or explain technical terms. Record preferences for concrete vs. abstract language. Note any verbal tics or filler phrases that recur (e.g., "essentially", "in other words", "the thing is"). Document whether the writer uses first person ("I"), second person ("you"), or third person, and how frequently they shift between them.

### Tone and Register
Characterize the overall tone (formal, conversational, academic, irreverent, etc.). Note how the tone shifts between sections (e.g., casual in intros, precise in analysis). Document the writer's relationship with the reader (peer-to-peer, teacher-student, authority-to-audience). Also note what tone is *wrong* for this voice — the opposite of the target is often more useful than the target itself.

### Paragraph Structure
Record typical paragraph length (in sentences and approximate word count). Note whether paragraphs tend to lead with topic sentences or build to a point. Document the use of single-sentence paragraphs for emphasis. Record whether the writer uses subheadings frequently, sparingly, or never. Note the typical number of paragraphs per section and whether section length is consistent or varied.

### Rhetorical Devices
Identify frequently used devices: repetition, parallelism, rule-of-three, rhetorical questions, direct address, humor, irony, hyperbole, understatement. Note the density of device usage -- some writers use them sparingly for emphasis, while others employ them as a constant stylistic texture. Record specific examples from the samples for each identified device.

### Transition Patterns
Document how the writer moves between ideas. Note whether transitions are explicit ("However," "Moreover,") or implicit (juxtaposition, thematic links). Record the use of transitional paragraphs vs. transitional phrases.

### Opening and Closing Patterns
Characterize how the writer begins pieces (anecdote, bold claim, question, scene-setting, statistic). Document closing patterns (call to action, summary, provocative question, callback to opening, future-looking statement). Note specifically: does the writer earn the thesis slowly or state it upfront? Does the closing preserve energy or deflate into recap?

### Use of Metaphors and Analogies
Note frequency and type of figurative language. Document whether metaphors are drawn from specific domains (sports, science, everyday life). Record extended vs. brief metaphor usage.

### Formality Level
Rate on a scale from 1 (highly informal) to 10 (highly formal). Note use of contractions, colloquialisms, slang, or conversational fillers.

### Unique Signatures
Capture anything distinctive that does not fit the above categories. Examples: consistent use of numbered lists, a habit of citing historical parallels, always ending with a one-word sentence, opening every section with a question.

### Sentence-Level Preferences (DO/DON'T Pairs)
Extract 3-5 concrete DO/DON'T pairs from the samples. Look for patterns the writer consistently chooses vs. avoids. Quote actual examples from the samples.

Examples of what to look for:
- Concrete nouns + active verbs vs. abstract nouns + passive constructions
- Direct statement vs. correlative scaffolding ("not X, but Y")
- Specific numbers/names vs. vague quantifiers ("many," "some," "various")
- Embodied/sensory language vs. purely cognitive description
- Short declarative sentences for emphasis vs. qualifications and hedges

### Signature Moves
Named, reusable structural or rhetorical patterns this voice uses especially well. These are the things the voice does that other voices don't, or does distinctively.

Look for:
- A recurring structural arc (e.g., start with personal friction → zoom out to cultural context → deliver usable framework)
- A characteristic way of introducing arguments (borrowed lens from an unexpected domain, confession, bold claim)
- A signature pivot or turn (e.g., a wry observation that reframes what came before)
- A recurring closing gesture

Give each move a short name (like "The Friction Zoom-Out" or "The Borrowed Lens") and a 1-2 sentence description. Document where it appears in the samples.

### Anti-Patterns (Blacklist)
This is the highest-value section in a voice profile. AI models have strong tendencies toward patterns that the writer may find intolerable — identifying these specifically is what separates a useful profile from a flattering description.

Look for patterns the writer consistently avoids. Also note which common AI writing tics are most at odds with this voice:

- **Correlative constructions** ("not X, but Y") — Creates padding; state Y directly
- **Hedge words** ("actually," "essentially," "just," "simply") — Weakens authority unless doing real work
- **Rhetorical questions as filler** — Stalls momentum; cut or convert to statement
- **Tidy summary endings** that recap rather than extend or reframe
- **Meandering introductions** that take more than 2-3 paragraphs to reach the stakes
- **Abstract industry analysis** without personal stakes or concrete examples
- **Fake profundity** — vague philosophical endings, "at the end of the day" constructions
- **Generic transitions** ("Furthermore," "Moreover," "In conclusion")
- **Voice-specific anti-patterns** found in the samples — these are the most important

For each anti-pattern: state the pattern specifically, explain why it's particularly wrong for this voice, and give the fix.

### Positive Examples
Pull 2-3 sentences or short paragraphs from the samples that best capture this voice working at full strength. For each, add a brief explanation of what makes it work — rhythm, specificity, the particular move it makes. These are reference points for the draft writer.

### Negative Examples
Identify 1-2 moments in the samples where the writing falters (often in transitions, section openings, or conclusions), or construct what a generic AI version of a key passage would sound like and explain why it fails. These are as instructive as the positive examples.

### Revision Checklist
A per-draft checklist built from this voice's specific requirements. Each item should be answerable yes/no by looking at the draft. Start with questions derived from the anti-patterns and signature moves, then add general quality checks.

Examples:
- Does the opening have friction, a bold claim, or a charged scene — not a contextual warm-up?
- Is the ending extending or reframing, not summarizing?
- Are there any correlative constructions left in the draft?
- Are there hedge words that can be deleted?
- Did the draft deploy at least one of the voice's signature moves?
- Does this sound like a real person or a polished summary machine?
- Is the language specific enough throughout, or has abstraction crept into any section?

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
method: sample-analysis  # or: interview, hybrid
sample_count: 5
sources:
  - path/to/sample1.md
  - https://example.com/article
  - "pasted text (first 50 chars...)"
---

# Voice Profile: Display Name

## Summary
[2-3 sentences on what makes this voice distinctive — the tensions, the qualities that set it apart]

## Voice and Tone
[How the writing should feel. Include tensions (e.g., "rigorous but not academic"). Include what tone is wrong.]

## Structure
[How pieces open, how quickly they arrive at their argument, how they move, how they end. Name any recurring structural arc.]

## Sentence Structure
[Analysis of sentence patterns]

## Vocabulary
[Analysis of vocabulary preferences]

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

## Sentence-Level Preferences

**Do:**
- [specific preference with quoted example]
- [specific preference with quoted example]

**Avoid:**
- [specific pattern to avoid with example]
- [specific pattern to avoid with example]

## Signature Moves

Named patterns this voice uses especially well:

1. **[Move Name]**: [description of what it does, when it appears, why it works]
2. **[Move Name]**: [description]

## Anti-Patterns (Blacklist)

These patterns must be avoided regardless of how natural they seem. This is the most important section for producing writing that sounds like this voice.

| Pattern | Why It Fails Here | Fix |
|---------|------------------|-----|
| [specific pattern] | [why this voice rejects it] | [what to do instead] |

## Positive Examples

**Example 1:**
> [quoted text from samples]
*Why it works: [explanation]*

**Example 2:**
> [quoted text from samples]
*Why it works: [explanation]*

## Negative Examples

**Example 1 (what to avoid):**
> [quoted text or reconstructed AI-style version]
*Why it fails: [explanation]*

## Revision Checklist

- [ ] [question specific to this voice]
- [ ] [question specific to this voice]
- [ ] Does this sound like a real person or a polished summary machine?
- [ ] Is the language specific enough, or has abstraction crept in?
- [ ] Are there entries from the anti-patterns table still in the draft?

## Usage Notes
[Direct instructions for the draft writer — read this section first. Most important patterns to apply, signature moves to deploy, anti-patterns to hunt for.]

## Refinement Log

| Date | Source | Change |
|------|--------|--------|
| [date] | [source] | [what was added/changed] |
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

- **Draft Writer (Stage 3)**: Read Usage Notes first. Then internalize Anti-Patterns (treat as hard constraints), Signature Moves (deploy where they fit), Positive Examples (use as the quality target), and Sentence-Level Preferences. Keep the Revision Checklist in mind while writing.
- **Style Critic (Stage 4)**: Lead with an anti-pattern audit — scan the entire draft against the Blacklist table. Then run the Revision Checklist item by item. Then evaluate signature move deployment. Score voice consistency based on anti-pattern hits and checklist failures.
- **Final Editor (Stage 6)**: Sweep the draft for remaining anti-pattern hits. Run the Revision Checklist as a final gate before writing output.

## Setting a Default Profile

Set the default voice profile using the manage-profiles command. The default profile name is stored in the article-writer configuration. When no `--voice` flag is passed to the pipeline, the default profile is used. If no default is set and no flag is provided, the pipeline runs without voice profiling.

## Profile Maturity Levels

Profiles improve over time. Treat them as living documents, not one-time artifacts.

**Starter profile** (interview or 3 samples): Voice/tone, basic structure, initial anti-patterns from common AI tics. Enough to reduce generic output. Create with `/interview-voice` or `/analyze-voice`.

**Working profile** (5-10 samples + editorial feedback): Full anti-patterns table built from real draft corrections, named signature moves, positive/negative examples, revision checklist derived from actual problems. Requires several rounds of `/refine-voice` after real articles. This is where profiles become genuinely useful.

**Compound profile** (ongoing refinement): Anti-patterns table has 10+ entries, each added from a real draft. Revision checklist catches the specific ways *this voice's* AI drafts fail. Profile is the first thing loaded and the last thing checked. Gets better with every article.

## Tips for Better Profiles

- Use samples from diverse topics. A profile built from articles about only one subject may capture topic-specific language as style.
- Include samples of different lengths. Short-form and long-form writing often reveal different aspects of voice.
- Include both the writer's best work and their everyday writing. Published pieces may be heavily edited; informal writing reveals natural voice.
- Revisit profiles after 6-12 months of writing. Voices evolve, and profiles should reflect current style.
- When the writer has multiple distinct registers (e.g., technical blog vs. social media), consider creating separate profiles for each register rather than one blended profile.
- Run `/refine-voice <name> --article <path>` after every article. The anti-patterns table should grow with every use.
- If you keep making the same correction to AI drafts, that correction belongs in the profile — not just your head.

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
