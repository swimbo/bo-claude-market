---
name: revise
description: Revise a whitepaper draft based on review feedback or specific instructions
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
argument-hint: "<path-to-whitepaper-draft>"
---

# Revise Whitepaper

Revise an existing whitepaper draft based on review feedback, user instructions, or both.

## Step 1: Load the Draft

Read the whitepaper draft from the provided path.

## Step 2: Gather Revision Instructions

Ask the user how they want to approach revision:

**Option A: Address review feedback**

* Ask the user to paste or describe the review feedback

* Or check if a recent `/whitepaper:review` was run and reference those findings

**Option B: Specific revisions**

* Ask the user what specific changes they want made

* Examples: "strengthen the evidence in section 3," "rewrite the introduction," "add more technical depth"

**Option C: Full re-review and fix**

* Launch the `whitepaper-reviewer` agent to identify all issues

* Then systematically address each one

## Step 3: Plan Revisions

Present a revision plan to the user before making changes:

For each revision:

* What section is affected

* What the current issue is

* What the planned change is

* Whether new research is needed

Ask for approval before proceeding.

## Step 4: Execute Revisions

Work through revisions section by section.

Ask the user: "Would you like me to revise each section one at a time for your review, or revise the full draft at once?"

If section-by-section:

* Make the revision to one section

* Show the before/after diff or the revised section

* Wait for approval before moving to the next

If full revision:

* Apply all planned revisions

* Present the complete revised draft

For all revisions:

* If new research is needed, launch the `whitepaper-researcher` agent

* Maintain consistent citation style throughout

* Preserve the author's voice where possible — do not rewrite sections that are already strong

* Keep a revision log noting what changed and why

## Step 5: Verify Revisions

After all revisions are applied:

* Run a quick quality check against the most critical checklist items

* Verify citation consistency

* Check that no new issues were introduced

Present a summary:

* Number of sections revised

* Key changes made

* Any remaining issues or suggestions for future revisions

## Step 6: Finalize

Ask the user if they want to:

1. Generate the final output (markdown and/or PDF)
2. Run another review cycle
3. Make additional specific changes

If generating final output:

* Write the final markdown file

* If PDF requested, run: `bash $CLAUDE_PLUGIN_ROOT/scripts/generate-pdf.sh <input.md> <output.pdf>`

* Present the final file paths