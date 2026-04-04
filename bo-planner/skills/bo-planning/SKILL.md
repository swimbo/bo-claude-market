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
├── data-map.md              # Data entities, relationships, flows, access patterns
├── user-stories.md          # User stories derived from requirements
├── architecture.md          # System design, component boundaries, API surface
├── tech-guide.md            # Tech stack, dependency versions, conventions, dev setup
├── ux-plan.md               # UX: user flows, interaction patterns, accessibility
├── ui-plan.md               # UI: visual design system, typography, colors, components
├── e2e-tests.md             # Playwright test plan and generated test inventory
├── findings.md              # Research discoveries, external content
└── progress.md              # Session log, test results, errors
```

## Quick Start

Before any complex task:

1. **Snapshot environment** — `git status`, check what exists, note running services
2. **Define scope** — IN/OUT scope fence, confirmed with user
3. **Create** **`docs/planning/`** **directory** — `mkdir -p docs/planning`
4. **Create** **`phased-plan.md`** — High-level phases, scope fence, environment snapshot
5. **Create** **`findings.md`** — Initialize with empty Pain Point Research table (populated during Phase 2)
6. **Run pain point research** — WebSearch for user complaints, competitor friction, unmet needs. Populate `findings.md`.
7. **Create** **`data-map.md`** — Data entities, relationships, flows, access patterns, storage
8. **Create** **`user-stories.md`** — User stories from requirements AND pain point findings
9. **Create** **`architecture.md`** — System design, component boundaries, API surface
10. **Create** **`tech-guide.md`** — Tech stack, dependency versions, conventions, dev environment setup
11. **Create** **`ux-plan.md`** — User flows, interaction patterns, accessibility, error handling _(if project has user-facing components)_
12. **Create** **`ui-plan.md`** — Visual design system, typography, colors, component inventory _(if project has visual interfaces)_
13. **Create** **`e2e-tests.md`** — Playwright test plan derived from user stories and UX flows _(if project has testable UI or CLI)_
14. **Create** **`phase-#-plan.md`** — One detailed plan per phase
15. **Create** **`progress.md`** — Session log, test results, errors
16. **Get approval** — Present plan to user before starting

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

Use the 12-phase pattern (customize phase names to the task):

1. **Requirements & Discovery** — Understand intent, capture constraints, environment snapshot
2. **Pain Point Research** — Web research into real user complaints, competitor friction, and unmet needs in the problem space. Output: `findings.md` (Pain Point Research section). See "Pain Point Research" below.
3. **Data Map** — Map data entities, relationships, flows, access patterns, storage requirements. Output: `data-map.md`
4. **User Stories** — Derive user stories with acceptance criteria, priorities, and phase mapping. Must reference pain point findings. Output: `user-stories.md`
5. **Architecture** — System design, component boundaries, API surface, infrastructure decisions. Output: `architecture.md`. **Then invoke `agents-argue:debate` on `architecture.md`** to stress-test decisions through adversarial consensus before proceeding.
6. **Tech Guide** — Tech stack selection, dependency versions, coding conventions, dev environment setup. Output: `tech-guide.md`. **Then invoke `agents-argue:debate` on `tech-guide.md`** to validate stack choices through adversarial consensus before proceeding.
7. **UX Planning** — User flows, interaction patterns, accessibility, error handling, dark pattern audit _(skip for backend-only/library projects)_. Output: `ux-plan.md`
8. **UI Planning** — Visual design system, typography, color palette, component inventory, layout _(skip for non-visual projects)_. Output: `ui-plan.md`
9. **Implementation** — Build it, using subagents for independent work
10. **E2E Test Generation** — Generate Playwright CLI tests from user stories and UX flows _(skip if no testable UI/CLI)_. Output: `e2e-tests.md` + test files
11. **Testing & Verification** — Run all tests (including generated Playwright tests), verify requirements met. Consider `test-everything:test-full-suite` for comprehensive coverage.
12. **Delivery** — Final review, user verification, cleanup

Phase 2 may be skipped ONLY for internal tooling with no external users, when the user provides their own research, or for bug fixes/refactors with no new user-facing behavior. Record skip reason in `findings.md`.
Phases 7-8 apply when the project has user-facing components (web apps, CLI tools, plugins, IDE extensions).
Phase 10 applies when the project has testable UI or CLI interfaces.
For backend-only or pure library projects, skip conditional phases and renumber.

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

### When to include conditional phases

| Project Type | UX Plan | UI Plan | E2E Tests (Playwright) |
| ------------ | ------- | ------- | ---------------------- |
| Web application | Yes | Yes | Yes |
| CLI tool | Yes | Yes (TUI composition) | Yes (CLI tests) |
| IDE plugin/extension | Yes | Yes (container mapping) | Yes |
| API / backend service | No | No | Partial (API integration tests) |
| Library / SDK | Partial (API ergonomics) | No | No |
| MCP server | Partial (tool descriptions for LLM "users") | No | No |

## Integration with Existing Skills

This planning system works alongside:

* **brainstorming** — Use BEFORE planning for creative/design work

* **agents-argue:debate** — **MANDATORY** during Architecture (Phase 4) and Tech Guide (Phase 5). See "Adversarial Debate Gates" below.

* **frontend-design** — Use during UI Planning phase for production-grade interfaces

* **test-driven-development** — Use during Implementation phase

* **playwright-cli** — Use during E2E Test Generation phase to scaffold and run Playwright tests

* **webapp-testing** — Use during E2E Test Generation and Testing & Verification phases

* **verification-before-completion** — Use during Delivery phase

* **test-everything:test-full-suite** — Use for comprehensive test coverage

* **test-everything:test-audit** — Use to validate test gaps

* **dispatching-parallel-agents** — Use when 3+ independent tasks need delegation

## Adversarial Debate Gates

Phases 5 (Architecture) and 6 (Tech Guide) each have a mandatory debate gate. The phase is NOT complete until the debate has run and the consensus output has been incorporated.

### How it works

For each of these phases:

1. **Draft the artifact** — Write `architecture.md` or `tech-guide.md` as normal using the template.
2. **Invoke the debate** — Use the Skill tool: `Skill("agents-argue:debate", args: "<path to artifact>")`. This launches multi-agent adversarial debate with domain-expert personas who critique and stress-test the decisions.
3. **Incorporate consensus** — The debate produces `consensus-plan.md` and `debate-transcript.md` in `docs/planning/`. Update the original artifact (`architecture.md` or `tech-guide.md`) to incorporate resolved decisions from the consensus output.
4. **Log unresolved items** — Any disagreements the debate could not resolve go into `findings.md` with a `NEEDS_HUMAN_DECISION` tag for the user to resolve before Implementation begins.
5. **Mark phase complete** — Only after the artifact reflects the post-debate consensus.

### Why this is mandatory

Architecture and tech stack decisions are the highest-leverage choices in a project. Mistakes here compound through every downstream phase. The adversarial debate surfaces blind spots, challenges assumptions, and produces stronger decisions than a single perspective can.

### Sequencing

The two debates run **sequentially**, not in parallel — the Tech Guide debate may reference architecture decisions, so Architecture must be debated and finalized first.

## Pain Point Research (Phase 2)

Phase 2 is a dedicated research phase that grounds the entire project in real user pain. Without it, user stories are based solely on the requester's assumptions. This phase ensures we build for actual problems, not imagined ones.

### How it works

After Phase 1 establishes intent and constraints:

1. **Identify the problem space** — What domain is this project in? What existing tools/products address the same need?
2. **Search for user complaints** — Use WebSearch to find forum posts, GitHub issues, Reddit threads, reviews, and support tickets where real users describe frustrations in this space. Target 5+ distinct sources across at least 2 platforms.
3. **Analyze competitor friction** — Look at how existing solutions handle the same problem. Where do users report friction, confusion, or missing features?
4. **Synthesize patterns** — Group complaints into themes. Distinguish one-off gripes from recurring pain patterns.
5. **Capture findings** — Write all discoveries to `findings.md` under the `## Pain Point Research` section with:
   - Source URL
   - Key complaint/pain point
   - Frequency signal (one person vs. recurring theme)
   - Relevance to our project scope
6. **Present to user** — Summarize the top pain points and ask: "Do any of these change your priorities or scope?"

### What to search for

- `"[domain/product] frustrating"`, `"[domain/product] wish it could"`, `"[domain/product] missing feature"`
- GitHub issues with high reaction counts in competing/related projects
- Reddit/HN threads complaining about the problem space
- App store or product reviews mentioning friction
- Stack Overflow questions indicating common confusion or workarounds

### Verification

Phase 2 is complete when:
- `findings.md` has a populated Pain Point Research table with 5+ entries
- At least 2 different source platforms are represented
- Findings have been presented to the user
- User has confirmed whether findings affect scope

### When to skip

Phase 2 may be skipped ONLY when:
- The project is purely internal tooling with no external users
- The user explicitly says they've already done this research and provides their findings
- The project is a bug fix or refactor with no new user-facing behavior

Record the skip reason in `findings.md` if skipped.



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

* [templates/data-map.md](templates/data-map.md)

* [templates/user-stories.md](templates/user-stories.md)

* [templates/architecture.md](templates/architecture.md)

* [templates/tech-guide.md](templates/tech-guide.md)

* [templates/ux-plan.md](templates/ux-plan.md)

* [templates/ui-plan.md](templates/ui-plan.md)

* [templates/e2e-tests.md](templates/e2e-tests.md)

* [templates/findings.md](templates/findings.md)

* [templates/progress.md](templates/progress.md)