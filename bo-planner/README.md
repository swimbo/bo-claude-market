# bo-planner

File-based planning for Claude Code with scope fences, environment snapshots, verification gates, and subagent delegation tracking.

Opinionated fork of [planning-with-files](https://github.com/othmanadi/planning-with-files), customized for directive, parallel-first workflows.

## What's Different

| Feature | planning-with-files | bo-planner |
|---------|-------------------|------------|
| Output location | Project root (3 files) | `docs/planning/` (structured artifact set) |
| Scope management | None | Explicit IN/OUT scope fence per plan |
| Environment capture | None | Snapshot of existing state before planning |
| Verification | Optional | Mandatory gate per phase |
| Phase detail | Single file | `phased-plan.md` overview + individual `phase-#-plan.md` |
| User stories | None | Dedicated `user-stories.md` with acceptance criteria |
| Architecture | None | Dedicated `architecture.md` with stack/data model/API |
| Subagent tracking | None | Delegation table in phased-plan.md |
| Hook frequency | PreToolUse on every call | PostToolUse on writes only |
| Templates | Verbose with tutorial comments | Lean, no-noise templates |
| Platform support | 16 IDEs + Windows | macOS + Claude Code |
| Architecture reference | None | Points to ~/.claude/templates/fullstack/ |
| Completion check | Status report only | Full verification protocol with user confirmation |
| Testing integration | None | Integrates with test-everything plugin |

## Commands

| Command | Description |
|---------|-------------|
| `/plan` | Start a planning session with scope negotiation |
| `/status` | Quick status check of current plan |
| `/done` | Verification protocol before declaring complete |

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
├── user-stories.md          # User stories with acceptance criteria
├── architecture.md          # Tech stack, data model, API design, decisions
├── findings.md              # Research discoveries, external content
└── progress.md              # Session log, test results, errors
```

## Philosophy

- Explore first, plan second, code third
- Scope fence is non-negotiable
- Every phase needs documented verification
- Parallel subagents for independent work
- Never repeat a failed action
- User confirms completion, not Claude
