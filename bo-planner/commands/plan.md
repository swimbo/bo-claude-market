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

   * `findings.md` — **Populated during Phase 2 (Pain Point Research)** with real user complaints, competitor friction, and unmet needs from web research. Also holds later research discoveries and technical decisions.

   * `data-map.md` — Data entities, relationships, flows, access patterns, storage requirements

   * `user-stories.md` — User stories derived from requirements AND pain point research findings, with acceptance criteria

   * `architecture.md` — System design, component boundaries, API surface, infrastructure decisions. If building a new fullstack app, reference `~/.claude/templates/fullstack/` for the preferred stack. **After drafting, invoke `agents-argue:debate` on this file to stress-test decisions.**

   * `tech-guide.md` — Tech stack selection, dependency versions, coding conventions, dev environment setup. Reference `~/.claude/preferred-tech-stack.md` for defaults. **After drafting, invoke `agents-argue:debate` on this file to validate stack choices.**

   * `ux-plan.md` — User flows, interaction patterns, accessibility requirements, error handling strategy, dark pattern audit _(create when project has user-facing components)_

   * `ui-plan.md` — Visual design system, color palette, typography scale, component inventory, layout architecture _(create when project has visual interfaces)_

   * `e2e-tests.md` — Playwright test plan derived from user stories and UX flows, plus generated test file inventory _(create when project has testable UI or CLI)_

   * `phase-1-plan.md` through `phase-N-plan.md` — Detailed plan for each phase with task checklist, dependencies, verification criteria

   * `progress.md` — Session log, test results, error log

5. **Present the plan** — Show the user the phase breakdown and ask for approval before starting work.

## Rules

* Never start implementation without an approved plan

* Every phase-#-plan.md must have a verification section

* Capture environment state FIRST to avoid "wrong approach" friction

* Scope fence is non-negotiable — if something isn't in IN scope, don't do it

* All planning files go in `docs/planning/`, never in project root

* **Pain point research before user stories** — Phase 2 populates `findings.md` with real user complaints via web research. Phase 4 (User Stories) must reference these findings. Skip only for internal tooling, user-provided research, or bug fixes.

* **Kickoff research at the start of major phases** — Phases 3, 5, 6, 7, 8, and 10 begin with a 3-5 minute WebSearch targeting "latest"/"current" information to counter stale training data. Capture findings in `findings.md`. Highest value is Phase 6 (Tech Guide).

* **Architecture and Tech Guide require adversarial debate** — invoke `agents-argue:debate` on each artifact after drafting. Incorporate consensus before marking the phase complete. Debate Architecture before Tech Guide (sequential, not parallel).