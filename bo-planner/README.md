# bo-planner

File-based planning for Claude Code with scope fences, environment snapshots, verification gates, and subagent delegation tracking.

Opinionated fork of [planning-with-files](https://github.com/othmanadi/planning-with-files), customized for directive, parallel-first workflows.

## What's Different

| Feature                | planning-with-files            | bo-planner                                               |
| ---------------------- | ------------------------------ | -------------------------------------------------------- |
| Output location        | Project root (3 files)         | `docs/planning/` (structured artifact set)               |
| Scope management       | None                           | Explicit IN/OUT scope fence per plan                     |
| Environment capture    | None                           | Snapshot of existing state before planning               |
| Verification           | Optional                       | Mandatory gate per phase                                 |
| Phase detail           | Single file                    | `phased-plan.md` overview + individual `phase-#-plan.md` |
| Pain point research    | None                           | Dedicated phase: web research into real user complaints before stories |
| Data mapping           | None                           | Dedicated `data-map.md` with entities, flows, access patterns |
| User stories           | None                           | Dedicated `user-stories.md` grounded in researched pain points |
| Architecture           | None                           | Dedicated `architecture.md` with adversarial debate gate |
| Tech guide             | None                           | Dedicated `tech-guide.md` with adversarial debate gate   |
| Subagent tracking      | None                           | Delegation table in phased-plan.md                       |
| Hook frequency         | PreToolUse on every call       | PostToolUse on writes only                               |
| Templates              | Verbose with tutorial comments | Lean, no-noise templates                                 |
| Platform support       | 16 IDEs + Windows              | macOS + Claude Code                                      |
| Architecture reference | None                           | Points to \~/.claude/templates/fullstack/                |
| Completion check       | Status report only             | Full verification protocol with user confirmation        |
| UX/UI planning         | None                           | Dedicated UX and UI planning phases with templates       |
| E2E test generation    | None                           | Playwright test plan phase with CLI test support         |
| Adversarial debate     | None                           | Mandatory agents-argue:debate on architecture & tech stack |
| Testing integration    | None                           | Integrates with test-everything plugin                   |

## Commands

| Command   | Description                                     |
| --------- | ----------------------------------------------- |
| `/plan`   | Start a planning session with scope negotiation |
| `/status` | Quick status check of current plan              |
| `/done`   | Verification protocol before declaring complete |

## Install

```bash
claude plugin install bo-planner@bo-planner
```

## Output Structure

All planning artifacts go in `docs/planning/`:

```
docs/planning/
├── phased-plan.md           # High-level phases, scope fence, environment, delegations
├── phase-1-plan.md          # Detailed Phase 1: tasks, deps, verification
├── phase-2-plan.md          # Detailed Phase 2: tasks, deps, verification
├── phase-N-plan.md          # ...one per phase
├── data-map.md              # Data entities, relationships, flows, access patterns
├── user-stories.md          # User stories with acceptance criteria
├── architecture.md          # System design, component boundaries, API surface
├── tech-guide.md            # Tech stack, dependency versions, conventions, dev setup
├── ux-plan.md               # UX: user flows, interaction patterns, accessibility
├── ui-plan.md               # UI: visual design system, typography, colors, components
├── e2e-tests.md             # Playwright test plan and generated test inventory
├── findings.md              # Pain point research, discoveries, external content
└── progress.md              # Session log, test results, errors
```

## Phases

12-phase model (conditional phases skipped when not applicable):

| Phase | Name | Conditional | Quality Gate |
| ----- | ---- | ----------- | ------------ |
| 1 | Requirements & Discovery | | |
| 2 | Pain Point Research | Skip for internal tooling / bug fixes | Web research into real user complaints |
| 3 | Data Map | | |
| 4 | User Stories | | Must reference pain point findings |
| 5 | Architecture | | **Adversarial debate** |
| 6 | Tech Guide | | **Adversarial debate** |
| 7 | UX Planning | User-facing projects only | |
| 8 | UI Planning | Visual interfaces only | |
| 9 | Implementation | | |
| 10 | E2E Test Generation | Testable UI/CLI only | |
| 11 | Testing & Verification | | |
| 12 | Delivery | | |

Phase 2 searches for real user complaints, competitor friction, and unmet needs via web research before user stories are written. Phases 5 and 6 require mandatory `agents-argue:debate` invocation — the artifact is drafted, debated by multi-agent adversarial consensus, then updated with resolved decisions before proceeding. Architecture is debated before Tech Guide (sequential).

## Philosophy

* Explore first, plan second, code third

* Research real pain before writing stories

* Scope fence is non-negotiable

* Every phase needs documented verification

* High-leverage decisions get adversarial debate

* Parallel subagents for independent work

* Never repeat a failed action

* User confirms completion, not Claude