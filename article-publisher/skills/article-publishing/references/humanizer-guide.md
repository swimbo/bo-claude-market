# Humanizer Guide

Reference for detecting and removing signs of LLM-generated writing. Apply these rules when rewriting article content to sound naturally human.

## Banned Words and Phrases

Replace or remove these. They are disproportionately common in LLM output and rare in human writing.

### Overused "Fancy" Words

Remove or replace with simpler alternatives:

| LLM Word | Human Alternatives |
|---|---|
| delve | dig into, explore, look at |
| tapestry | mix, combination, blend |
| multifaceted | complex, varied, many-sided |
| nuanced / nuances | subtle, detailed, fine points |
| comprehensive | full, complete, thorough |
| intricate / intricacies | complex, detailed, tricky |
| pivotal | key, important, turning point |
| landscape (metaphorical) | world, space, field, scene |
| leverage (verb) | use, take advantage of, build on |
| foster | encourage, build, grow, support |
| robust | strong, solid, reliable |
| streamline | simplify, speed up, cut down |
| underscores | shows, highlights, proves |
| commendable | impressive, good, solid |
| meticulous / meticulously | careful, thorough, precise |
| realm | area, field, world, space |
| aforementioned | (just remove — refer to the thing directly) |
| paramount | critical, top priority, essential |
| testament | proof, sign, evidence |
| endeavor / endeavors | effort, project, attempt, work |
| embark | start, begin, kick off |
| bolster | strengthen, support, boost |
| catalyze / catalyst | trigger, spark, cause, driver |
| elucidate | explain, clarify, spell out |
| spearhead | lead, drive, run |
| harness | use, tap into, put to work |
| seamless / seamlessly | smooth, easy, without friction |
| groundbreaking | new, original, first-of-its-kind |
| cutting-edge | latest, newest, advanced |

### Overused Transition Adverbs

Cut these by 70% or more. Use sparingly, never consecutively:

- Moreover
- Furthermore
- Additionally
- Notably
- Importantly
- Crucially
- Essentially
- Fundamentally
- Interestingly
- Remarkably
- Ultimately

Replace with: nothing (just start the sentence), "and", "but", "also", "still", "though", or restructure so the connection is implicit.

### Hollow Filler Phrases

Delete entirely — they add nothing:

- "It's important to note that..."
- "It's worth mentioning that..."
- "It's crucial to understand that..."
- "It should be noted that..."
- "It bears mentioning..."
- "One cannot overstate..."
- "The importance of X cannot be overstated"

### Formulaic Collocations

Replace with direct, specific language:

| LLM Phrase | Fix |
|---|---|
| "plays a crucial role in" | matters for, shapes, drives |
| "a wide range of" | many, various, all kinds of |
| "in today's rapidly evolving world" | (delete or be specific about what changed) |
| "serves as a reminder" | reminds us, shows |
| "paving the way for" | making room for, enabling, opening up |
| "navigate the complexities of" | deal with, work through, figure out |
| "shed light on" | reveal, explain, show |
| "at the forefront of" | leading, ahead in, pushing |
| "strikes a balance between" | balances, splits the difference |
| "a double-edged sword" | (find a specific description of the tradeoff) |
| "gain a deeper understanding" | learn more, understand better |
| "take a holistic approach" | look at the whole picture, consider everything |
| "have a profound impact on" | change, reshape, affect |
| "resonate with" | connect with, appeal to, hit home for |
| "bridge the gap between" | connect, link, close the distance |
| "the intersection of X and Y" | where X meets Y, the overlap of |

## Structural Fixes

### Vary Sentence Length (Burstiness)

This is the single most measurable AI signal. AI text clusters around 15-25 words per sentence.

**Fix:**
- Mix very short sentences (3-8 words) with long ones (30+)
- Include sentence fragments for emphasis
- Use one-word sentences occasionally. Seriously.
- Aim for high variance — some paragraphs with all short sentences, some with long meandering ones

### Break the Topic-Sentence-First Pattern

AI always starts paragraphs with a broad claim, then elaborates, then transitions.

**Fix:**
- Sometimes put the point at the end of the paragraph
- Start with a specific detail or example, then zoom out
- Start with a question or reaction
- Use one-sentence paragraphs

### Vary Paragraph Length

AI paragraphs are almost always 3-5 sentences.

**Fix:**
- Include one-sentence paragraphs
- Include longer 6-8 sentence paragraphs where the idea needs room
- Let some paragraphs be just 2 sentences

### Reduce Parallel Constructions

AI loves: "It improves X, enhances Y, and fosters Z."

**Fix:**
- Break parallel lists into separate sentences
- Use different grammatical structures for related points
- Don't always group things in threes

### Cut Excessive Signposting

Remove most explicit transitions like:
- "Turning to the next point..."
- "Having discussed X, let us now consider Y..."
- "Building on this idea..."
- "With that in mind..."

Let ideas flow naturally. Readers can follow without being led by the hand.

## Tone Fixes

### Add Contractions

AI avoids contractions. Humans use them constantly in all but the most formal writing.

- "do not" → "don't"
- "it is" → "it's"
- "cannot" → "can't"
- "will not" → "won't"
- "they are" → "they're"

Use contractions 80%+ of the time unless the formality is deliberate for emphasis ("I do *not* agree").

### Kill the Relentless Positivity

AI always hedges, balances, and ends optimistically.

**Fix:**
- Take actual positions. Say "this is wrong" not "this presents challenges"
- Don't feel obligated to present "both sides" when one is clearly stronger
- It's okay to end on an unresolved note, a question, or even pessimism
- Replace "room for improvement" with direct language — "bad", "broken", "lacking"

### Remove Excessive Hedging

Cut phrases like:
- "It could be argued that..."
- "Many experts believe..."
- "While opinions vary..."
- "This is a complex issue with no easy answers"

If you're making a point, make it. Hedging once is fine. Hedging every claim sounds like an AI covering its bases.

### Add Informal Register

Human writing shifts between formal and casual within a piece.

**Fix:**
- Sprinkle in casual phrasing: "turns out", "pretty much", "kind of", "the thing is"
- Use rhetorical questions that sound conversational, not formulaic
- Include the occasional aside or tangent
- Write like you're explaining to a smart friend, not presenting to a committee

## Opening and Closing Fixes

### Banned Openings

Never start an article with:
- "In today's rapidly evolving world..."
- "In the ever-changing landscape of..."
- "[Topic] has become increasingly important in recent years."
- "When it comes to [topic]..."
- "Have you ever wondered..." (rhetorical hook)
- "[Topic] is a [complex/multifaceted/nuanced] issue that..."

**Instead:** Start with a specific story, a surprising fact, a bold claim, a question that genuinely matters, or just jump straight into the point.

### Banned Closings

Never end an article with:
- "In conclusion, [restate thesis]"
- "Ultimately, [topic] is about..."
- "As we move forward..."
- "Only time will tell..."
- "The future of X remains to be seen"
- "It's up to all of us to..."
- Restating the opening almost verbatim

**Instead:** End with the strongest specific insight, a provocative question, a concrete recommendation, or just stop when you're done. Not every piece needs a bow on top.

### Remove Summary/Conclusion Sections

If the article ends with a section that restates everything that was already said, cut it or replace it with a single punchy closing thought. Readers don't need a recap of something they just read.

## Punctuation and Formatting Fixes

### Reduce Em Dashes

AI (especially Claude) overuses em dashes. Limit to 1-2 per article.

Replace with: commas, parentheses, periods (splitting into two sentences), or just restructuring.

### Reduce Semicolons

Limit to 1-2 per article. Replace with periods or restructure.

### Remove Excessive Bold

Don't bold **key terms** on first use. This isn't a textbook. Use bold sparingly for genuine emphasis only.

### Reduce Bullet Lists in Prose

If the article is supposed to be prose, convert bullet lists back into flowing paragraphs. Lists are fine for genuinely list-like content (steps, requirements, options) but not for every set of related points.

## Specificity Fixes

### Replace Vague Claims with Concrete Details

| Vague (AI) | Specific (Human) |
|---|---|
| "Studies show..." | cite a specific study or drop the claim |
| "Experts agree..." | name an expert or say who specifically |
| "Research suggests..." | which research? link it or qualify it |
| "significantly improved" | by how much? 20%? 3x? |
| "in recent years" | since when? 2020? last quarter? |
| "many people" | how many? what kind of people? |

### Add Asymmetry

AI gives equal weight to every point. Humans focus on what matters.

**Fix:**
- Spend 3 paragraphs on the most important point and 1 sentence on a minor one
- Skip points that aren't worth making
- Go deep on specifics rather than broad on generalities

## Process

When humanizing an article, follow this order:

1. **Scan for banned words/phrases** — Replace all instances from the lists above
2. **Fix openings and closings** — Rewrite if they match banned patterns
3. **Vary sentence structure** — Adjust sentence lengths for burstiness, break parallel constructions
4. **Fix paragraph structure** — Vary lengths, break topic-sentence-first pattern
5. **Adjust tone** — Add contractions, remove hedging, inject informal register, take positions
6. **Add specificity** — Replace vague claims with concrete details where possible
7. **Clean punctuation** — Reduce em dashes, semicolons, bold, bullet lists in prose
8. **Remove redundancy** — Cut summary/conclusion sections that just restate, remove filler phrases
9. **Final read** — Read the whole piece looking for anything that still sounds "committee-written"

## What NOT to Change

- The author's core arguments, facts, and opinions
- Technical terminology that's genuinely needed
- Intentional structure (if the article is meant to be a listicle, keep it as a list)
- Specific examples, data, and citations
- The overall length (don't pad or drastically shorten)
- Section headers that serve real navigation purposes
