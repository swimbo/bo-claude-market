---
name: bo-planning
description: >
  File-based planning with scope fences, environment snapshots, verification gates,
  and subagent delegation. Use when asked to plan, break down, or organize any
  multi-step task requiring >5 tool calls. Creates a full planning artifact set in
  docs/planning/. Supports session recovery after /clear.
user-invocable: true
allowed-tools: "Read, Write, Edit, Bash, Glob, Grep, Task, AskUserQuestion"
hooks:
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "echo '[bo-planner] File updated. If this completes a phase, update phased-plan.md and verify before marking complete.'"
  Stop:
    - hooks:
        - type: command
          command: "sh \"${CLAUDE_PLUGIN_ROOT}/scripts/check-complete.sh\""
metadata:
  version: "0.2.0"
---

# Bo Planner

Persistent markdown files as working memory. Explore first, plan second, code third.

## Session Recovery

Before starting work, check for a previous session:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/session-catchup.py "$(pwd)"
```

If catchup shows unsynced context:

1. Run `git diff --stat`
2. Read current planning files in `docs/planning/`
3. Update planning files based on catchup + git diff
4. Then proceed

## File Locations

| Location                                    | Contents                       |
| ------------------------------------------- | ------------------------------ |
| Plugin directory (`${CLAUDE_PLUGIN_ROOT}/`) | Templates, scripts, references |
| `docs/planning/` in project                 | All planning artifacts         |

## Output Structure

All planning files are written to `docs/planning/` in the project directory:

```
docs/planning/
├── phased-plan.md           # High-level phase overview, scope fence, environment
├── phase-1-plan.md          # Detailed plan for Phase 1
├── phase-2-plan.md          # Detailed plan for Phase 2
├── phase-N-plan.md          # ...one per phase
├── user-stories.md          # User stories derived from requirements
├── architecture.md          # Architecture decisions, tech stack, diagrams
├── ux-plan.md               # UX: user flows, interaction patterns, accessibility
├── ui-plan.md               # UI: visual design system, typography, colors, components
├── findings.md              # Research discoveries, external content
└── progress.md              # Session log, test results, errors
```

## Quick Start

Before any complex task:

1. **Snapshot environment** — `git status`, check what exists, note running services
2. **Define scope** — IN/OUT scope fence, confirmed with user
3. **Create** **`docs/planning/`** **directory** — `mkdir -p docs/planning`
4. **Create** **`phased-plan.md`** — High-level phases, scope fence, environment snapshot
5. **Create** **`user-stories.md`** — User stories from requirements
6. **Create** **`architecture.md`** — Tech stack, architecture decisions
7. **Create** **`ux-plan.md`** — User flows, interaction patterns, accessibility, error handling _(if project has user-facing components)_
8. **Create** **`ui-plan.md`** — Visual design system, typography, colors, component inventory _(if project has visual interfaces)_
9. **Create** **`phase-#-plan.md`** — One detailed plan per phase
10. **Create** **`findings.md`** — Research, decisions, resources
11. **Create** **`progress.md`** — Session log, test results, errors
12. **Get approval** — Present plan to user before starting

Use templates from `${CLAUDE_PLUGIN_ROOT}/templates/` as starting points.

## Architecture Reference

For new fullstack projects, reference the preferred architecture at:
`~/.claude/templates/fullstack/`

Key patterns from that template:

* **Frontend**: React 19 + Vite 6 + Tailwind 4 + shadcn/ui + TanStack Query

* **Backend**: Rust/Axum + SQLx + PostgreSQL

* **Agents**: TypeScript + Express + Claude Agent SDK

* **Infra**: Docker Compose orchestration

* **Auth**: JWT access/refresh tokens + RBAC

Capture relevant patterns in `architecture.md` when starting a new project.

## The Core Pattern

```
Context Window = RAM (volatile, limited)
Filesystem = Disk (persistent, unlimited)
Anything important gets written to disk.
```

## Critical Rules

### 1. Scope Fence is Non-Negotiable

Every plan has explicit IN and OUT sections in `phased-plan.md`. If it's not IN scope, don't do it. If scope needs to change, negotiate with the user first.

### 2. Environment Before Plan

Capture what already exists (repos, services, tools, files) BEFORE planning. This prevents the #1 source of wasted time: Claude misreading what's already set up.

### 3. Verification Gates

Every phase plan (`phase-#-plan.md`) has a `Verification` section. A phase cannot be marked `complete` without documented verification. "It should work" is not verification.

### 4. Subagents for Independent Work

When a phase has 2+ independent tasks, delegate to parallel subagents. Track delegations in `phased-plan.md`. This is not optional.

### 5. The 2-Action Rule

After every 2 view/browser/search operations, save key findings to `findings.md`. Visual/multimodal content doesn't persist.

### 6. Read Before Decide

Before major decisions, read `phased-plan.md`. This keeps goals in your attention window after many tool calls.

### 7. Log ALL Errors

Every error goes in `progress.md`. Track attempts and mutate approach — never repeat the same failing action.

### 8. 3-Strike Protocol

```
Attempt 1: Diagnose and fix (targeted)
Attempt 2: Alternative approach (different method)
Attempt 3: Broader rethink (question assumptions)
After 3 failures: Escalate to user with what you tried
```

## Phase Planning

Use the 7-phase pattern (customize phase names to the task):

1. **Requirements & Discovery** — Understand intent, capture constraints, environment snapshot
2. **Planning & Structure** — Technical approach, architecture decisions, scope confirmation
3. **UX Planning** — User flows, interaction patterns, accessibility, error handling, dark pattern audit _(skip for backend-only/library projects)_
4. **UI Planning** — Visual design system, typography, color palette, component inventory, layout _(skip for non-visual projects)_
5. **Implementation** — Build it, using subagents for independent work
6. **Testing & Verification** — Run tests, verify requirements met. Consider `test-everything:test-full-suite` for comprehensive coverage.
7. **Delivery** — Final review, user verification, cleanup

Phases 3-4 apply when the project has user-facing components (web apps, CLI tools, plugins, IDE extensions). For backend-only or pure library projects, skip and renumber to 5 phases.

`phased-plan.md` contains the high-level overview of all phases with status tracking.
Each phase gets its own `phase-#-plan.md` with:

* Detailed task checklist

* Dependencies and prerequisites

* Subagent delegation plan (if applicable)

* Verification criteria (what proves this phase is done)

* Acceptance criteria

## Subagent Delegation

When delegating to subagents, track in `phased-plan.md`:

```markdown
## Delegated Work
| Task | Agent Type | Status | Result |
|------|-----------|--------|--------|
| Research competitor X | general-purpose | complete | See findings.md |
| Write unit tests for auth | general-purpose | in_progress | — |
```

Launch independent agents in a single message for parallel execution.

## UX & UI Planning Reference

When creating UX or UI plans, reference the research documents in the plugin's `research/` directory:

* **`research/ux-design.md`** — Nielsen's heuristics, Shneiderman's rules, dark patterns taxonomy, CLI usability (12-Factor CLI, Heroku standards), IDE plugin architecture, Microsoft HAX guidelines for AI interaction, MCP tool design, accessibility standards
* **`research/ui-design.md`** — Dieter Rams' principles, Gestalt composition, color theory with WCAG contrast ratios, monospaced typography adjustments, VS Code extension containers, JetBrains UI paradigms, CLI/TUI aesthetics (Ratatui, Charmbracelet), Anthropic brand color palette, visual anti-patterns

### When to include UX/UI phases

| Project Type | UX Plan | UI Plan |
| ------------ | ------- | ------- |
| Web application | Yes | Yes |
| CLI tool | Yes | Yes (TUI composition) |
| IDE plugin/extension | Yes | Yes (container mapping) |
| API / backend service | No | No |
| Library / SDK | Partial (API ergonomics) | No |
| MCP server | Partial (tool descriptions for LLM "users") | No |

## Integration with Existing Skills

This planning system works alongside:

* **brainstorming** — Use BEFORE planning for creative/design work

* **frontend-design** — Use during UI Planning phase for production-grade interfaces

* **test-driven-development** — Use during Implementation phase

* **verification-before-completion** — Use during Delivery phase

* **test-everything:test-full-suite** — Use for comprehensive test coverage

* **test-everything:test-audit** — Use to validate test gaps

* **dispatching-parallel-agents** — Use when 3+ independent tasks need delegation

## Anti-Patterns

| Don't                                              | Do Instead                                 |
| -------------------------------------------------- | ------------------------------------------ |
| Start implementing without a plan                  | Create docs/planning/ artifacts FIRST      |
| Assume what exists in the environment              | Run git status, check directories          |
| Declare phases complete without verification       | Document what you verified                 |
| Do independent tasks sequentially                  | Delegate to parallel subagents             |
| Expand scope silently                              | Negotiate scope changes with user          |
| Repeat failed actions                              | Track attempts, mutate approach            |
| Write external/untrusted content to phased-plan.md | Write external content to findings.md only |
| Stuff everything in context                        | Store large content in files               |

## Templates

* [templates/phased-plan.md](templates/phased-plan.md)

* [templates/phase-plan.md](templates/phase-plan.md)

* [templates/user-stories.md](templates/user-stories.md)

* [templates/architecture.md](templates/architecture.md)

* [templates/ux-plan.md](templates/ux-plan.md)

* [templates/ui-plan.md](templates/ui-plan.md)

* [templates/findings.md](templates/findings.md)

* [templates/progress.md](templates/progress.md)