---
name: analyze-voice
description: Analyze writing samples to create or update a voice profile for use in article generation.
argument-hint: "<profile-name>"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - WebFetch
  - WebSearch
---

# Analyze Voice

You are creating or updating a voice profile by analyzing writing samples. Parse the user's input to extract:

- **profile-name** (required) — the name for this voice profile

## Workflow

### Step 1: Collect Samples

Ask the user to provide writing samples. Require a minimum of 3 samples for a reliable profile. Accept any combination of:

- **File paths** — Read using the Read tool
- **URLs** — Fetch using the WebFetch tool (extract the main article/post content, ignore navigation, ads, etc.)
- **Pasted text** — Use directly as provided

If the user provides fewer than 3 samples, inform them: "Voice profiles work best with at least 3 samples. You've provided <N>. Would you like to add more, or proceed with what you have?"

### Step 2: Analyze Samples

Analyze all samples collectively, looking for consistent patterns across the body of work. Evaluate each of the following dimensions:

1. **Sentence Structure** — Average sentence length, variation patterns, use of simple vs. compound vs. complex sentences, fragment usage, rhetorical questions
2. **Vocabulary Level** — Reading level estimate, jargon usage, preferred word choices, words/phrases that recur, avoidance patterns
3. **Tone and Register** — Formal/informal spectrum, authoritative vs. conversational, humor usage, sarcasm/irony, emotional register
4. **Paragraph Structure** — Average paragraph length, topic sentence patterns, development patterns, one-sentence paragraph usage
5. **Rhetorical Devices** — Metaphor/simile frequency and style, repetition for emphasis, parallel construction, alliteration, other notable devices
6. **Transition Patterns** — How sections connect, use of transitional phrases vs. implicit transitions, paragraph-to-paragraph flow
7. **Opening Patterns** — How pieces begin (anecdote, question, statement, statistic, etc.), hook style
8. **Closing Patterns** — How pieces end (call to action, summary, open question, callback, etc.)
9. **Use of Examples and Analogies** — Frequency, source domains (tech, nature, sports, etc.), complexity
10. **Formality Level** — Contractions, first/second/third person usage, passive vs. active voice ratio, colloquialisms
11. **Unique Stylistic Signatures** — Anything distinctive that doesn't fit the above categories: catchphrases, structural quirks, punctuation habits (em dashes, semicolons, ellipses), list usage patterns

### Step 3: Check for Existing Profile

Check if `~/.claude/article-writer/profiles/<profile-name>.md` already exists.

- **If it exists**: Ask the user: "A profile named '<profile-name>' already exists. Would you like to (1) update it by merging new analysis with existing, or (2) replace it entirely?"
  - **Update/merge**: Read the existing profile, combine the analyses, note the increased sample count, and write the merged profile.
  - **Replace**: Overwrite with the new analysis.
- **If it does not exist**: Proceed to create it.

### Step 4: Create Profile

Ensure the directory `~/.claude/article-writer/profiles/` exists (create it if needed via Bash `mkdir -p`).

Write the profile to `~/.claude/article-writer/profiles/<profile-name>.md` with this structure:

```markdown
---
name: <profile-name>
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
sample_count: <number>
sources:
  - <source description or filename for each sample>
---

# Voice Profile: <profile-name>

## Summary
<2-3 sentence overview of this voice — what makes it distinctive>

## Sentence Structure
<analysis>

## Vocabulary
<analysis with specific examples from the samples>

## Tone and Register
<analysis>

## Paragraph Structure
<analysis>

## Rhetorical Devices
<analysis with specific examples>

## Transitions
<analysis>

## Openings
<analysis with examples of opening patterns>

## Closings
<analysis with examples of closing patterns>

## Examples and Analogies
<analysis>

## Formality
<analysis>

## Unique Signatures
<analysis of distinctive quirks>

## Usage Guide
<Concise instructions for an AI writing in this voice. Include DO and DON'T lists. This section should be directly actionable — it's what gets passed to the draft-writer and final-editor agents.>
```

### Step 5: Confirm

Print:
1. The profile path.
2. The summary section of the profile.
3. How many samples were analyzed.
4. Suggest: "You can set this as your default profile with: /manage-profiles set-default <profile-name>"
