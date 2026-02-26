---
name: create
description: Create a new technical whitepaper from scratch through a guided workflow
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
  - WebSearch
  - WebFetch
argument-hint: "[topic or title]"
---

# Create Technical Whitepaper

Guide the user through the full whitepaper creation lifecycle: discovery, outline, research, drafting, review, revision, and finalization.

## Step 1: Author History

Check if `~/.claude/whitepaper-history.json` exists. If it does, read it and present previous author entries as quick-select options. If the user selects a previous entry, use that. Otherwise, ask for:

* Author name(s)

* Organization name

* Author credentials/title

After collecting author info, save or update `~/.claude/whitepaper-history.json` with the new entry. The file format is:

```json
{
  "authors": [
    {"name": "Jane Smith", "org": "Acme Corp", "credentials": "VP Engineering", "lastUsed": "2026-02-26"}
  ]
}
```

## Step 2: Discovery Questions

Ask these questions in organized groups. Wait for answers before proceeding.

**Whitepaper Type** — Present the 6 types and ask the user to select one:

1. Pure Technical — deep dive into technology/implementation
2. Problem/Solution — pain point identification with evidence-backed solution
3. Backgrounder/Product — product evaluation for buyers
4. Thought Leadership — original perspective on industry topic
5. Market Research — presentation of original research findings
6. Visionary — forward-looking narrative about industry future

**Audience:**

* Who specifically will read this?

* What is their existing knowledge level on this topic?

* What problem keeps them up at night that this paper addresses?

**Purpose:**

* What is the single most important message the reader should leave with?

* What action should the reader take after reading?

**Content and Scope:**

* What specific question does this paper answer?

* What original data or perspective makes this worth reading?

* What is explicitly out of scope?

**Technical Depth:**

* How technical should this be? (1-10 scale)

* Will it include code, architecture diagrams, or implementation steps?

**Format Preferences:**

* Preferred citation style? (IEEE for tech, APA for business, or other)

* Target length? (6-10 pages executive, 10-15 technical, 15-25 research)

* Output format? (markdown, PDF, or both)

**Drafting preference:**

* Ask the user: "Would you like me to generate each section one at a time for your review, or generate the full draft at once?"

* Respect the user's choice throughout the workflow.

## Step 3: Generate Outline

Based on the whitepaper type selected and answers provided, generate a detailed outline following the type-specific structure from the whitepaper-authoring skill.

The outline must include:

* All applicable sections for the chosen type

* Subsection headings within each section

* Brief notes on what each section/subsection will cover

* Estimated word count per section

* Placeholder notes for where visuals should appear

**Present the outline to the user and ask for approval.** Do not proceed to drafting until the user approves or requests changes.

## Step 4: Research

Use the `whitepaper-researcher` agent (via Task tool) to gather data, statistics, and citations for the whitepaper topic. The researcher should use WebSearch to find:

* Industry statistics and data points

* Peer-reviewed sources and authoritative references

* Case studies and real-world examples

* Competitive landscape data (if applicable)

Present the research findings to the user. Ask if additional research is needed before drafting.

## Step 5: Draft

Write the whitepaper section by section following the approved outline.

If the user chose section-by-section mode:

* Write one section at a time

* Present each section to the user for review

* Wait for approval or revision requests before moving to the next section

* Incorporate feedback immediately

If the user chose full-draft mode:

* Write all sections sequentially

* Present the complete draft for review

For all drafting:

* Follow the writing standards from the whitepaper-authoring skill

* Use third-person voice for formal/technical papers

* Back every claim with a citation from the research phase

* Include visual element placeholders with descriptions (e.g., "\[Figure 1: Architecture diagram showing X]")

* Use the chosen citation style consistently

* Write section files to the working directory as `whitepaper-draft.md` or a user-specified filename

## Step 6: Review

Launch the `whitepaper-reviewer` agent (via Task tool) to review the complete draft against the quality checklist. Present the review findings to the user.

## Step 7: Revise

Address all issues identified in the review:

* Fix structural problems

* Strengthen weak evidence

* Correct citation formatting

* Improve reader-first framing

* Add missing visual elements

Present the revised draft and ask if further revisions are needed.

## Step 8: Finalize

When the user approves the final draft:

1. Generate the final markdown file with proper formatting
2. If the user requested PDF output, use the PDF generation script:

   ```
   bash $CLAUDE_PLUGIN_ROOT/scripts/generate-pdf.sh <input.md> <output.pdf>
   ```
3. If pandoc is not installed, inform the user and provide installation instructions
4. Present the final file paths to the user

## Important Rules

* Never skip the outline approval step

* Never generate a section without research backing

* Always maintain the chosen citation style consistently

* Always frame content around reader value, never company announcements

* Keep sentences concise (target under 14 words average)

* Eliminate buzzwords: "leveraging," "best-in-class," "industry-leading," "synergies"