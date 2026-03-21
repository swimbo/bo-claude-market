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

**Style dimensions:**
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

**Higher-value dimensions (these most distinguish a real style guide from a generic one):**

12. **Sentence-Level Preferences** — Extract 3-5 concrete DO/DON'T pairs from the samples. Look for patterns the writer consistently chooses vs. avoids: abstract nouns vs. concrete verbs, symmetrical constructions vs. direct statements, specific numbers vs. vague quantifiers. Quote actual examples from the samples.

13. **Signature Moves** — Named, reusable structural patterns this voice uses especially well. Look for: how the writer opens arguments, how they introduce ideas (borrowed lens? personal friction? bold claim?), recurring arcs (e.g., start concrete → zoom out → framework; anecdote → pattern → takeaway). Give each move a short name and description.

14. **Anti-Patterns** — This is the highest-value section. Identify what this voice consistently avoids. Look for: correlative constructions ("not X, but Y"), hedge words ("actually," "essentially," "just," "simply"), rhetorical questions used as filler, abstract industry analysis without personal stakes, tidy summary endings that recap rather than extend, meandering introductions. For each, note the pattern, why it fails in this voice, and what to do instead.

15. **Positive Examples** — Pull 2-3 sentences or short paragraphs that best capture this voice working at full strength. For each, add a brief explanation of what makes it work.

16. **Negative Examples** — Identify moments in the samples where the voice falters or sounds generic (these often occur in transitions, introductions, and conclusions). For each, explain what went wrong.

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
method: sample-analysis
sample_count: <number>
sources:
  - <source description or filename for each sample>
---

# Voice Profile: <profile-name>

## Summary
<2-3 sentence overview of this voice — what makes it distinctive, including the tensions that define it>

## Voice and Tone
<How the writing should feel. Include specific tensions (e.g., "rigorous but not academic"). Include what tone is completely wrong for this voice.>

## Structure
<How pieces open, how quickly they arrive at their argument, how they move between ideas, how they end. Name any recurring structural arc.>

## Sentence Structure
<analysis>

## Vocabulary
<analysis with specific examples from the samples>

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

## Formality
<analysis>

## Unique Signatures
<analysis of distinctive quirks>

## Sentence-Level Preferences

**Do:**
- <specific preference with quoted example from samples>
- <specific preference with quoted example>

**Avoid:**
- <specific pattern to avoid with quoted example of the bad version>
- <specific pattern to avoid>

## Signature Moves

Named patterns this voice uses especially well:

1. **[Move Name]**: <description of what it does, when it appears, and why it works for this voice>
2. **[Move Name]**: <description>

## Anti-Patterns (Blacklist)

These patterns must be avoided regardless of how natural they seem to an AI model. This is the most important section for producing writing that sounds like this voice.

| Pattern | Why It Fails Here | Fix |
|---------|------------------|-----|
| <specific pattern with example> | <why this voice rejects it> | <what to do instead> |
| Correlative constructions ("not X, but Y") | Creates false balance, padding | State Y directly |
| Hedge words ("actually," "essentially," "just") | Weakens authority | Delete unless doing real work |
| Tidy summary ending that recaps | Deflates the piece | End by extending or reframing |
| Rhetorical questions as filler | Stalls momentum | Cut or convert to statement |
| <voice-specific pattern> | <reason> | <fix> |

## Positive Examples

Sentences or paragraphs that capture this voice working at its best:

**Example 1:**
> <quoted text from samples>
*Why it works: <explanation>*

**Example 2:**
> <quoted text from samples>
*Why it works: <explanation>*

## Negative Examples

Moments where the voice falters or sounds generic:

**Example 1 (what to avoid):**
> <quoted text — or a reconstructed AI-style version of a weak moment>
*Why it fails: <explanation>*

## Revision Checklist

Run before every final edit:

- [ ] <question specific to this voice — e.g., "Does the opening have friction?">
- [ ] <question — e.g., "Are there correlative constructions left?">
- [ ] <question — e.g., "Does the ending extend or reframe rather than summarize?">
- [ ] Does this sound like a real person or a polished summary machine?
- [ ] Is the language specific enough, or has abstraction crept in?
- [ ] Are there entries from the anti-patterns table still in the draft?

## Usage Notes
<Concise instructions for the draft writer — read this section first. The most important patterns to apply, the signature moves to deploy, and the anti-patterns to actively hunt for. This is directly actionable.>
```

### Step 5: Confirm

Print:
1. The profile path.
2. The summary section of the profile.
3. How many samples were analyzed.
4. Suggest: "You can set this as your default profile with: /manage-profiles set-default <profile-name>"
