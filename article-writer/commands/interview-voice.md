---
name: interview-voice
description: Build a voice profile through an interactive interview — no writing samples required. Claude asks one question at a time and synthesizes your answers into a full style guide.
argument-hint: "<profile-name>"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Interview Voice

You are building a voice profile through conversation, not sample analysis. This is the right approach when the user doesn't have strong writing samples yet, or when they find it easier to react to examples than to describe their style from scratch.

Parse the user's input to extract:

- **profile-name** (required) — the name for this voice profile

## How This Works

Rather than analyzing existing writing, you will interview the user. Ask one focused question at a time. Use their answers to generate short examples they can react to — concrete sentences, paragraph openings, or side-by-side comparisons. Their reactions will surface preferences they couldn't describe in the abstract.

The interview covers seven areas, in this order:

1. Voice and tone (how the writing should feel)
2. Structure (how pieces open and move)
3. Sentence-level preferences (rhythm, length, diction)
4. Signature moves (what this voice does especially well)
5. Anti-patterns (what to avoid at all costs)
6. Examples (reference pieces they love or hate)
7. Revision standards (how to evaluate a draft)

You do not need to complete all seven areas if the user wants to stop early. A partial profile is better than no profile.

## Interview Protocol

### Starting the Interview

Greet the user and explain the process:

> "I'm going to interview you to build a voice profile for **[profile-name]**. I'll ask one question at a time. For some questions I'll show you sample sentences or paragraphs and ask you to react — that usually surfaces more useful preferences than asking you to describe your style in the abstract.
>
> We'll cover: voice/tone, structure, sentence style, signature moves, things to avoid, reference examples, and how to evaluate a draft. You can stop any time and I'll synthesize what we have.
>
> Let's start: **How should writing in this voice feel at its best?** Try to go beyond words like 'clear' or 'smart' — what specific quality or tension defines it?"

### Question-by-Question Rules

- Ask **one question at a time**. Never present a list of questions.
- After each answer, do one of:
  - Generate 2-3 short example sentences/paragraphs and ask "Which of these sounds most like you, and why?"
  - Ask a follow-up that goes deeper on what they said
  - Confirm you understood and move to the next area
- When the user says something negative ("I hate when…", "definitely not…"), note it as an anti-pattern candidate and probe further: "Can you give me an example of what that looks like in the wild?"
- When the user reacts to examples, ask *why* — the reason is more valuable than the preference itself.
- If the user is unsure, offer contrasting options: "Would you say this piece is closer to [A] or [B]?"

### Key Questions by Area

**Voice and tone:**
- How should this writing feel at its best? (opening question)
- How much emotional temperature does it have? Warm/cool, intimate/distant?
- Is humor welcome? What kind — dry, self-deprecating, absurdist?
- What tone is completely wrong for this voice?

**Structure:**
- How do your pieces typically open? (anecdote, bold claim, problem, scene?)
- How quickly do you get to the point? Do you prefer to earn the argument or state it upfront?
- How do your pieces end — forward momentum, open question, callback, or something else?
- Show 2 opening paragraphs: one that earns its thesis slowly, one that states it in the first sentence. Ask: which feels right?

**Sentence-level preferences:**
- Short and punchy, or long and flowing? Or mixed?
- What words or phrases do you find yourself reaching for?
- What words or constructions make you cringe when you see them in your own writing?
- Show a "not X, but Y" sentence and a direct version of the same thought. Which do they prefer?

**Signature moves:**
- What does this voice do especially well that other voices don't?
- Is there a structural arc you return to often? (e.g., start concrete, zoom out, land on framework)
- Do you have a signature way of introducing ideas — a borrowed lens, an unexpected analogy, a confession?

**Anti-patterns:**
- What do you always correct when you see it in a draft?
- What patterns make AI-generated writing feel most obviously AI-generated?
- Show 3-5 common AI writing tics (correlative constructions, hedge words, tidy summary endings, rhetorical questions as filler). Ask which ones bother them most.

**Examples:**
- Can you name 2-3 pieces — your own or others' — that capture the voice you're aiming for?
- What specifically works about them?
- Is there a piece that missed the mark? What went wrong?

**Revision standards:**
- When you're editing a draft, what's the first thing you look for?
- What's the sign that a draft is working? What's the sign it's failing?
- What questions do you ask yourself before publishing?

### Wrapping Up

When the user indicates they're done (or after all seven areas are covered), say:

> "Great — I have enough to build a strong profile. I'll synthesize this into a full style guide now."

Then proceed to synthesis.

## Synthesis

Synthesize all interview answers into a complete voice profile. The profile must include all sections, including anti-patterns, signature moves, positive/negative examples, and a revision checklist — the sections that most distinguish a real style guide from a generic one.

Where the interview didn't cover a section fully, note it as "Partially established — expand with writing samples" rather than leaving it empty or making things up.

### Profile Template

Write the profile to `~/.claude/article-writer/profiles/<profile-name>.md`:

```markdown
---
name: <profile-name>
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
method: interview
sample_count: 0
sources:
  - "interview (YYYY-MM-DD)"
---

# Voice Profile: <profile-name>

## Summary
<2-3 sentences on what makes this voice distinctive — the tensions, the qualities that set it apart>

## Voice and Tone
<What the writing should feel like. Include tensions (e.g., "rigorous but not academic, warm but not soft"). Include what tone is wrong.>

## Structure
<How pieces open, how quickly they arrive at their point, how they move, how they end. Name any recurring structural arc.>

## Sentence-Level Preferences
<Sentence length, rhythm, diction. Include DO/DON'T pairs where possible.>

**Do:**
- <specific preference with example>
- <specific preference with example>

**Avoid:**
- <specific pattern to avoid with example>
- <specific pattern to avoid with example>

## Signature Moves
<Named patterns this voice does especially well. Give each a short name and description.>

1. **[Move Name]**: <description of what it does and when to use it>
2. **[Move Name]**: <description>

## Anti-Patterns (Blacklist)

This is the highest-value section. These patterns must be avoided regardless of how natural they seem.

| Pattern | Why It Fails | Fix |
|---------|-------------|-----|
| <specific pattern> | <why this voice rejects it> | <what to do instead> |
| <specific pattern> | <why> | <fix> |

**AI writing tics to always cut:**
- <list specific tics that appeared in the interview>

## Positive Examples
<Sentences, paragraphs, or openings that capture the voice at its best. For each, explain what works.>

**Example 1:**
> <quoted text>
*Why it works: <explanation>*

**Example 2:**
> <quoted text>
*Why it works: <explanation>*

## Negative Examples
<Lines or paragraphs that miss the mark. For each, explain what's wrong.>

**Example 1 (what to avoid):**
> <quoted text>
*Why it fails: <explanation>*

## Revision Checklist

Run this checklist on every draft before final edit:

- [ ] <question specific to this voice — e.g., "Does the opening have friction?">
- [ ] <question — e.g., "Are there any 'not X, but Y' constructions?">
- [ ] <question — e.g., "Does the ending preserve energy rather than summarize?">
- [ ] Does this sound like a real person or a polished summary machine?
- [ ] Is the language specific enough, or has abstraction crept in?
- [ ] Are there anti-pattern entries still in the draft?

## Usage Notes
<Direct instructions for the draft writer. The most important patterns to apply and avoid. This section is read first.>
```

## After Creating the Profile

1. Print the profile path.
2. Print the Summary section.
3. Say: "This profile was built from an interview. Consider running `/analyze-voice <profile-name>` with writing samples to strengthen it further — especially the examples and anti-patterns sections."
4. Say: "Set this as your default with: /manage-profiles set-default <profile-name>"
