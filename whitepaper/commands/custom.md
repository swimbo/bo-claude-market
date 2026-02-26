---
name: custom
description: Create a whitepaper from a requirements document (RFP, style guide, template)
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
argument-hint: "<path-to-requirements-document>"
---

# Custom Whitepaper from Requirements Document

Create a whitepaper that conforms to format and structure requirements extracted from a provided document.

## Step 1: Load Requirements Document

Read the provided document. Supported formats:
- **Markdown** (.md): Read directly with Read tool
- **PDF** (.pdf): Read with Read tool (it handles PDFs)
- **Word** (.docx): Convert using `pandoc` or `textutil -convert txt` on macOS, then read
- **Plain text** (.txt): Read directly with Read tool

If the file cannot be read, inform the user and suggest converting to a supported format.

## Step 2: Extract Requirements

Launch the `requirements-extractor` agent (via Task tool) with the document content. The agent will parse and return a structured requirements profile covering:

- **Structure requirements**: Required sections, section order, naming conventions
- **Format requirements**: Page limits, word counts, margins, font specifications
- **Content requirements**: Required topics, mandatory data points, specific questions to answer
- **Style requirements**: Voice (first/third person), tone, citation style, terminology rules
- **Visual requirements**: Required diagrams, charts, tables, figure formatting rules
- **Compliance requirements**: Specific evaluation criteria, scoring rubrics, mandatory certifications

Present the extracted requirements to the user and ask for confirmation. Highlight any ambiguities or conflicts found in the document.

## Step 3: Author History

Same as the `create` command — check `~/.claude/whitepaper-history.json` for previous entries, offer as quick-select, collect new info if needed, and save.

## Step 4: Gap-Fill Questions

Based on extracted requirements, identify what information is still needed that the requirements document did not specify. Ask the user only for information not covered by the requirements doc:

- Topic and thesis (if not specified)
- Audience details (if not specified)
- Technical depth (if not specified)
- Any requirement-specific content the user needs to provide (case studies, data, product details)

## Step 5: Generate Outline

Generate an outline that:
- Follows the structure specified in the requirements document
- Uses the section names and ordering from the requirements
- Includes all mandatory sections
- Maps whitepaper best practices onto the required structure
- Notes where requirements conflict with best practices (and explains the trade-off)

**Present the outline to the user and ask for approval.**

## Step 6: Research

Same as the `create` command — launch the `whitepaper-researcher` agent to gather data, statistics, and citations. Focus research on topics required by the requirements document.

## Step 7: Draft

Write the whitepaper section by section following the approved outline.

Ask the user: "Would you like me to generate each section one at a time for your review, or generate the full draft at once?"

For all drafting:
- Follow the structure and format rules from the extracted requirements
- Where requirements are silent on a convention, fall back to whitepaper best practices
- Maintain compliance with all mandatory requirements
- Flag any section where a requirement could not be fully met and explain why

Write the draft to the working directory as `whitepaper-draft.md` or a user-specified filename.

## Step 8: Compliance Check

After drafting, run a compliance check against the extracted requirements:
- Verify all required sections are present
- Check word/page counts against limits
- Verify citation style matches requirements
- Confirm all mandatory topics are addressed
- Check visual element requirements

Present a compliance report showing pass/fail for each requirement.

## Step 9: Review

Launch the `whitepaper-reviewer` agent to review quality. The reviewer should check against BOTH:
1. The extracted requirements (compliance)
2. General whitepaper best practices (quality)

## Step 10: Revise and Finalize

Same as the `create` command — address issues, present revised draft, generate final markdown and/or PDF output.

## Important Rules

- Requirements from the document take precedence over default best practices
- When requirements conflict with best practices, follow the requirements but note the trade-off
- Always present the extracted requirements for user confirmation before proceeding
- Track compliance throughout the workflow, not just at the end
