---
name: create-template
description: Analyze example articles to extract their structural pattern and create a reusable article template.
argument-hint: "<template-name>"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - WebFetch
  - WebSearch
---

# Create Template

You are creating an article template by analyzing example articles. Parse the user's input to extract:

- **template-name** (required) — the name for this template

## Workflow

### Step 1: Collect Examples

Ask the user to provide one or more example articles that follow the pattern they want to template. Accept:

- **File paths** — Read using the Read tool
- **URLs** — Fetch using the WebFetch tool (extract the main article content, ignore navigation, ads, sidebars, etc.)

At least one example is required. More examples produce better templates because patterns can be validated across multiple instances.

### Step 2: Analyze Structure

For each example article, analyze and map out:

1. **Structural Pattern** — Identify each section, its role (introduction, background, argument, evidence, counterpoint, conclusion, etc.), and the ordering logic
2. **Section Lengths** — Typical word count or proportion for each section relative to the whole
3. **Tone and Style Markers** — Per-section tone shifts (e.g., introduction is conversational, evidence sections are more formal)
4. **Variable Placeholders** — Identify what changes between articles using this pattern vs. what stays constant. Variables are the "fill-in" parts: topic, examples, data, arguments. Constants are structural: section order, transition styles, opening pattern type.
5. **Opening Pattern** — How the article begins (hook type, length, relationship to thesis)
6. **Closing Pattern** — How the article ends (summary, call to action, callback, open question)
7. **Transition Patterns** — How sections connect to each other, recurring transitional devices

If multiple examples are provided, identify the common patterns across all of them and note any variations.

### Step 3: Generate Template

Ensure the directory `~/.claude/article-writer/templates/` exists (create it if needed via Bash).

Determine appropriate metadata:
- **category** — Infer from the content type (e.g., "technical", "opinion", "tutorial", "narrative", "analysis", "how-to", "listicle", "case-study", "review")
- **estimated_length** — Based on the example articles' word counts
- **difficulty_level** — How complex the structure is: "beginner", "intermediate", "advanced"
- **tags** — Relevant topic/format tags

Write the template to `~/.claude/article-writer/templates/<template-name>.md`:

```markdown
---
name: <template-name>
description: <1-2 sentence description of what this template is for>
category: <category>
estimated_length: <word count range, e.g., "1500-2000">
difficulty_level: <beginner|intermediate|advanced>
tags:
  - <tag1>
  - <tag2>
variables:
  - name: <variable-name>
    type: <text|list|number|choice>
    description: <what this variable represents>
  - name: <variable-name>
    type: <type>
    description: <description>
source_articles:
  - <source description for each example>
created: <YYYY-MM-DD>
---

# Template: <template-name>

## Overview
<Description of the article pattern this template captures. When to use it, what kind of topics it works well for, what audience it targets.>

## Structure

### Section 1: <Section Name>
- **Purpose**: <What this section accomplishes>
- **Length**: <Approximate word count or proportion>
- **Tone**: <Tone for this section>
- **Content Guide**: <What to include, how to approach it>
- **Example Opening**: <An example of how this section might start>

### Section 2: <Section Name>
- **Purpose**: <purpose>
- **Length**: <length>
- **Tone**: <tone>
- **Content Guide**: <guidance>
- **Transition from Previous**: <How to connect from the prior section>

<...repeat for all sections...>

## Variables
<For each variable defined in frontmatter, explain how and where it's used in the template>

## Transitions Guide
<General guidance on how sections should flow into each other>

## Tone Map
<Overview of how tone shifts through the article>

## Tips
<Any additional advice for using this template effectively>
```

### Step 4: Review

Display the generated template to the user. Ask: "Does this template look right? You can suggest changes, or say 'save' to keep it as is."

- If the user suggests changes, update the template and show it again.
- If the user approves, confirm the save location.

### Step 5: Confirm

Print:
1. The template path.
2. The template description.
3. The identified structure (section names as a list).
4. The number of variables defined.
5. Suggest: "Use this template with: /write-article <topic> --template <template-name>"
