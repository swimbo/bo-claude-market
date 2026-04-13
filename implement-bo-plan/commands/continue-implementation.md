---
name: continue-implementation
description: "Continue an interrupted implementation. Reads progress.md and phased-plan.md to determine where to restart. (Named continue-implementation because /resume is reserved by Claude Code for resuming conversations.)"
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
  - Task
  - AskUserQuestion
  - Skill
---

Continue an in-flight `/implement` run that was interrupted.

## Steps

1. **Read state.**
   - `docs/planning/phased-plan.md` — find the first non-`complete` phase.
   - `docs/planning/progress.md` — find the most recent entry.
   - If any gate was marked failed in the last entry, treat that gate as the
     restart point, not the first non-`complete` phase.

2. **Classify restart point.**
   - Mid-task in phase 9 → find the next unchecked task in `phase-9-plan.md`.
   - Phase 11 test failure → restart at `test-everything:test-contract`.
   - Phase 11.5 blocked on critical design issues → restart at phase 9 for
     those fixes, then re-run phase 11 → 11.5.
   - Phase 11.6 blocked on grade → restart at phase 9 for the Critical/High
     findings, then re-run phase 11 → 11.6.
   - Phase 13 partially audited → find which artifact audits are incomplete,
     dispatch parallel subagents only for the missing ones.
   - Phase 14 has open gaps → continue from highest open severity.

3. **Confirm with user.**
   Use `AskUserQuestion` to confirm:
   > "Resuming from: Phase {N} — {restart reason}. Proceed?"

4. **Execute.**
   Invoke `Skill("implement-bo-plan:enterprise-implementation")` and run from
   the confirmed restart point through phase 14.

## Rules

- Never assume state — read the files every time.
- If `progress.md` is missing or empty, treat the run as fresh and suggest
  `/implement` instead.
- If the user disagrees with the proposed restart point, accept their choice
  and log the correction.
