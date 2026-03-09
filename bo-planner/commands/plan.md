---
name: plan
description: "Start file-based planning. Creates full artifact set in docs/planning/ with scope fences, environment snapshot, phased plans, user stories, and architecture."
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
  - AskUserQuestion
argument-hint: "<task description>"
---

Invoke the bo-planner:bo-planning skill and follow it exactly.

The argument is the task description. If no argument is provided, ask the user what they want to build or accomplish.

## Workflow

1. **Create output directory** — `mkdir -p docs/planning`

2. **Environment snapshot** — Run `git status`, check what exists in cwd, note running services. Capture in the Environment section of `docs/planning/phased-plan.md`.

3. **Scope negotiation** — Present the user with a proposed IN/OUT scope based on the task description. Use AskUserQuestion to confirm. Do NOT proceed until scope is approved.

4. **Create planning artifacts** in `docs/planning/`:

   * `phased-plan.md` — High-level phase overview, scope fence, environment, delegations

   * `user-stories.md` — User stories derived from the requirements

   * `architecture.md` — Tech stack, architecture decisions, project structure. If building a new fullstack app, reference `~/.claude/templates/fullstack/` for the preferred stack.

   * `ux-plan.md` — User flows, interaction patterns, accessibility requirements, error handling strategy, dark pattern audit _(create when project has user-facing components)_

   * `ui-plan.md` — Visual design system, color palette, typography scale, component inventory, layout architecture _(create when project has visual interfaces)_

   * `phase-1-plan.md` through `phase-N-plan.md` — Detailed plan for each phase with task checklist, dependencies, verification criteria

   * `findings.md` — Research, discoveries, technical decisions

   * `progress.md` — Session log, test results, error log

5. **Present the plan** — Show the user the phase breakdown and ask for approval before starting work.

## Rules

* Never start implementation without an approved plan

* Every phase-#-plan.md must have a verification section

* Capture environment state FIRST to avoid "wrong approach" friction

* Scope fence is non-negotiable — if something isn't in IN scope, don't do it

* All planning files go in `docs/planning/`, never in project root