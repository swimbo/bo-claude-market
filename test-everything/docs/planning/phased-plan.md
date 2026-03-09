# Interaction Verification Improvements — Phased Plan

**Date:** 2026-03-08
**Project:** test-everything plugin
**Design Doc:** `research/2026-03-08-interaction-verification-design.md`

## Environment

- **Branch:** main (up to date with origin)
- **Plugin version:** 0.4.0 → target 0.5.0
- **Plugin type:** Claude Code plugin (markdown templates, not executable code)
- **Files to modify:** 8 existing files across commands/, agents/, skills/
- **No new files** except planning artifacts

### Current Plugin Structure

```
test-everything/
├── .claude-plugin/plugin.json        # manifest (version bump)
├── commands/
│   ├── test-scaffold.md              # MODIFY (P1-P3, P4-P7)
│   ├── test-full-suite.md            # MODIFY (P1-P3, P5-P7)
│   ├── test-audit.md                 # MODIFY (P4)
│   └── test-plan.md                  # NO CHANGE
├── agents/
│   ├── test-gap-analyzer.md          # NO CHANGE
│   └── test-quality-reviewer.md      # MODIFY (P4)
├── skills/
│   └── test-strategy/
│       ├── SKILL.md                  # MODIFY (principles)
│       └── references/
│           ├── testing-types-detail.md    # MODIFY (E2E section)
│           └── implementation-roadmap.md  # MODIFY (Phase 3)
└── research/                         # design doc (already written)
```

## Scope Fence

### IN SCOPE

1. **test-scaffold.md** — Add interaction verification patterns, fixtures, selectors, walkthrough, visual regression to e2e layer
2. **test-full-suite.md** — Add verification rules (Phase 3), browser health (Phase 4), coverage report (Phase 6)
3. **test-audit.md** — Add interaction verification and selector quality checks
4. **test-quality-reviewer.md** — Add fire-and-forget and selector anti-patterns
5. **SKILL.md** — Add interaction verification principles
6. **testing-types-detail.md** — Expand E2E section with verification patterns + fixtures
7. **implementation-roadmap.md** — Add interaction verification to Phase 3
8. **plugin.json** — Bump version 0.4.0 → 0.5.0

### OUT OF SCOPE

- No new commands or agents
- No actual test code (plugin generates templates)
- No changes to unit/integration/perf/security layers
- No test-plan.md changes
- No test-gap-analyzer.md changes

## Phase Overview

| Phase | Focus | Files | Priority |
|-------|-------|-------|----------|
| **1** | Core Verification Patterns | test-scaffold.md, test-full-suite.md, testing-types-detail.md | P1-P3 |
| **2** | Quality & Audit Enhancements | test-audit.md, test-quality-reviewer.md, test-scaffold.md (selectors) | P4 |
| **3** | Advanced Features | test-scaffold.md (walkthrough, visual), test-full-suite.md (coverage report) | P5-P7 |
| **4** | Documentation & Finalization | SKILL.md, implementation-roadmap.md, plugin.json | All |

## Delegations

- Phases 1-4 can be executed sequentially by a single implementer
- No external dependencies or blocking factors
- All changes are additive (no breaking changes to existing behavior)
