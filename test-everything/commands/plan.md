---
name: plan
description: Generate a phased testing strategy and implementation plan tailored to the current project
argument-hint: "[path-to-project]"
allowed-tools: ["Read", "Glob", "Grep", "Bash", "Agent"]
---

# Testing Strategy Plan Generator

Generate a comprehensive, phased testing implementation plan tailored to the project.

## Instructions

Analyze the project and produce an actionable testing strategy with prioritized phases.

### Step 1: Assess Current State

If a `/test-everything:audit` was recently run, use those results. Otherwise, perform a quick assessment:

* Detect project type, languages, frameworks

* Inventory existing test infrastructure

* Identify major gaps

### Step 2: Select Testing Architecture Model

Based on project type, recommend:

| Project Type          | Model             | Rationale                     |
| --------------------- | ----------------- | ----------------------------- |
| Library / utility     | Pyramid           | Unit tests ARE the product    |
| API / backend service | Pyramid           | Business logic-heavy          |
| Frontend SPA          | Trophy            | Integration + static analysis |
| Full-stack web app    | Diamond           | Integration-heavy with E2E    |
| Microservices         | Diamond/Honeycomb | Service interaction focus     |

### Step 3: Define Target State

For each testing layer, specify:

* Target tool (from preferred stack: Vitest, Rust `#[test]`, Playwright, k6, etc.)

* Target coverage or scope

* Priority (P0 = must have, P1 = should have, P2 = nice to have)

### Step 4: Generate Phased Plan

Create an implementation plan organized in 2-week phases:

**Phase 1 (Foundation)**: Static analysis + unit testing framework
**Phase 2 (Integration)**: Integration tests + test database setup
**Phase 3 (E2E)**: Playwright setup + critical user journey tests
**Phase 4 (Security + Performance)**: SAST in CI + k6 load tests
**Phase 5 (Polish)**: Accessibility + cross-browser + documentation

For each phase, provide:

* Specific files to create or modify

* Tool installation commands

* Configuration snippets

* Estimated effort (hours/days)

* Dependencies on previous phases

### Step 5: Define Quality Gates

Specify what must pass at each pipeline stage:

* Pre-commit hooks

* PR/MR checks

* Staging deployment gates

* Release criteria

### Step 6: Output the Plan

Format as a structured, actionable document:

```
## Testing Strategy Plan for [Project Name]

### Current State
[Summary of existing test infrastructure]

### Target Architecture: [Model Name]

### Implementation Phases

#### Phase 1: Foundation (Week 1-2)
Priority: P0
- [ ] Task 1 — [specific action with file paths]
- [ ] Task 2 — [specific action]
Install: `[exact install command]`
Config: [what to configure]

#### Phase 2: Integration (Week 3-4)
...

### Quality Gates
[Table of gates with specific pass criteria]

### Tool Stack
| Purpose | Tool | Install |
|---------|------|---------|
| Unit (frontend) | Vitest | `pnpm add -D vitest` |
| ... | ... | ... |

### Estimated Total Effort
[Rough estimate per phase]
```

### Tips

* Make every task specific and actionable — include file paths and commands

* Don't recommend tools outside the preferred stack unless there's a strong reason

* Phase 1 should be achievable in a single sprint

* Include "quick wins" in Phase 1 to build momentum

* Reference the testing-strategy skill for deeper guidance on any testing type