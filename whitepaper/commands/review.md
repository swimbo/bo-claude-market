---
name: review
description: Review an existing whitepaper draft against best practices and quality standards
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
  - WebSearch
argument-hint: "<path-to-whitepaper-draft> [path-to-requirements-doc]"
---

# Review Whitepaper

Analyze an existing whitepaper draft and produce a structured quality review report.

## Step 1: Load the Draft

Read the whitepaper draft from the provided path. If a requirements document path is also provided, read that too.

If a requirements document is provided, launch the `requirements-extractor` agent to parse it first.

## Step 2: Identify Whitepaper Type

Analyze the draft to determine which of the 6 whitepaper types it most closely matches:

1. Pure Technical
2. Problem/Solution
3. Backgrounder/Product
4. Thought Leadership
5. Market Research
6. Visionary

If unclear, ask the user which type was intended.

## Step 3: Run Review

Launch the `whitepaper-reviewer` agent (via Task tool) with:

* The full draft content

* The identified whitepaper type

* The requirements document (if provided)

The reviewer will evaluate against the quality checklist from `references/quality-checklist.md`.

## Step 4: Present Review Report

Organize the review findings into a structured report:

### Report Structure

**Overall Assessment:** Brief 2-3 sentence summary of the draft quality.

**Score:** Rate each category on a 1-5 scale:

* Structure and Organization: X/5

* Evidence and Credibility: X/5

* Writing Quality: X/5

* Visual Elements: X/5

* Citations and References: X/5

* Type-Specific Requirements: X/5

* Requirements Compliance: X/5 (only if requirements doc was provided)

**Critical Issues:** Problems that must be fixed. Each item includes:

* What the issue is

* Where it occurs (section and approximate location)

* Why it matters

* Suggested fix

**Improvements:** Recommended but not critical changes. Same format as critical issues.

**Strengths:** What the draft does well. Important for encouraging the author.

**Compliance Report** (if requirements document was provided):

* Checklist of each requirement with pass/fail status

* Details on any failed requirements

## Step 5: Ask About Next Steps

After presenting the review, ask the user:
"Would you like me to help revise this whitepaper to address the issues found? You can use `/whitepaper:revise` with the draft path to start revisions."