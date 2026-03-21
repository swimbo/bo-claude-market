---
name: refine-voice
description: Feed editorial corrections and observations from real drafts back into a voice profile, sharpening its anti-patterns and revision checklist over time.
argument-hint: "<profile-name> [--article <path>] [--note \"<correction>\"]"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Refine Voice

You are updating a voice profile based on feedback from real drafts. This is how profiles improve over time — every correction you make to an AI-generated draft that keeps happening is a signal that the profile needs to be sharper.

Parse the user's input to extract:

- **profile-name** (required) — the profile to refine
- **--article <path>** (optional) — path to a recently generated article to analyze for recurring problems
- **--note "<text>"** (optional) — a specific correction or observation to add directly

## Load the Profile

Read `~/.claude/article-writer/profiles/<profile-name>.md`. If it doesn't exist, print an error and list available profiles.

## Refinement Modes

### Mode 1: Article Analysis (`--article`)

Read the article at the given path. If a corresponding draft exists at `../03-draft/draft.md` relative to the article, read that too — comparing draft to final edit reveals what corrections were made.

Look for:
- Patterns that appear in the draft but not (or less) in the final article (these are things the editor cut — prime anti-pattern candidates)
- AI writing tics: correlative constructions ("not X, but Y"), hedge words ("actually," "essentially," "just"), meandering introductions, tidy summary endings, rhetorical questions used as filler, abstract language where concrete was possible
- Deviations from the voice profile's documented signature moves
- Openings or closings that don't match the profile's patterns

For each pattern found:
1. Quote an example from the draft
2. State what's wrong with it in the context of this voice
3. Propose either a fix or an addition to the anti-patterns table

Present findings to the user and ask: "Which of these should I add to the anti-patterns list? Any patterns I should add to the revision checklist?"

### Mode 2: Direct Note (`--note`)

The user has provided a correction directly (e.g., "stop ending sections with a rhetorical question" or "the AI keeps summarizing at the end instead of extending the idea").

Parse the note into:
- **Pattern**: what behavior to avoid
- **Why it fails**: in the context of this voice
- **Fix**: what to do instead

Then ask: "Should I add this to the anti-patterns table, the revision checklist, or both?"

### Mode 3: Interactive (no flags)

Ask: "What pattern or problem do you want to address? You can describe a correction you keep making, paste a sentence that felt wrong, or tell me what the AI keeps doing that doesn't sound like you."

Listen to their answer and probe:
- "Can you give me an example of what this looks like?"
- "What would the right version sound like?"
- "Is this always wrong, or wrong in specific situations?"

Then propose updates to the profile.

## Updating the Profile

After determining what changes to make, update `~/.claude/article-writer/profiles/<profile-name>.md`:

1. **Anti-patterns table**: Add new rows for confirmed anti-patterns. Use specific pattern descriptions, not vague ones ("don't be generic" is not useful; "avoid correlative constructions — state Y directly without the 'not X' scaffolding" is).

2. **Revision checklist**: Add new checklist items for patterns that are hard to catch but easy to verify. Frame as yes/no questions.

3. **Negative examples**: If the user provides a sentence that failed, add it with an explanation.

4. **Positive examples**: If discussion surfaces a sentence that works well, add it.

5. **Updated timestamp**: Set `updated:` to today's date.

6. **Refinement log** (append to bottom of profile if not present):

```markdown
## Refinement Log

| Date | Source | Change |
|------|--------|--------|
| <YYYY-MM-DD> | <article path or "direct note"> | <what was added/changed> |
```

## After Updating

1. Print the updated anti-patterns table.
2. Print the updated revision checklist.
3. Say how many items were added to each section.
4. Say: "The more you refine this profile, the less you'll need to correct future drafts. Run `/refine-voice <profile-name> --article <path>` after each article to keep building the blacklist."
