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
├── plan-gaps.md             # Audit of implemented code vs. plan (Phase 13 output)
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

The canonical per-phase completion checklists live in `${CLAUDE_PLUGIN_ROOT}/done-means-done/` (one file per phase, plus a README index). When starting a phase, copy its **Hard Gates** verbatim into that phase's `Verification` section. When closing a phase, walk the checklist top-to-bottom and attach evidence to every gate. `/done` and `implement-bo-plan` both consult these checklists as the final gate before declaring completion.

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

Use the 14-phase pattern (customize phase names to the task):

1. **Requirements & Discovery** — Understand intent, capture constraints, environment snapshot
2. **Pain Point Research** — Web research into real user complaints, competitor friction, and unmet needs in the problem space. Output: `findings.md` (Pain Point Research section). See "Pain Point Research" below.
3. **Data Map** — **Kickoff research first** (see "Phase Kickoff Research" below). Then map data entities, relationships, flows, access patterns, storage requirements. Output: `data-map.md`
4. **User Stories** — Derive user stories with acceptance criteria, priorities, and phase mapping. Must reference pain point findings. Output: `user-stories.md`
5. **Architecture** — **Kickoff research first.** Then system design, component boundaries, API surface, infrastructure decisions. Output: `architecture.md`. **Then invoke `agents-argue:debate` on `architecture.md`** to stress-test decisions through adversarial consensus before proceeding.
6. **Tech Guide** — **Kickoff research first — this is the highest-value research step, targeting latest stable versions and breaking changes.** Then tech stack selection, dependency versions, coding conventions, dev environment setup. Output: `tech-guide.md`. **Then invoke `agents-argue:debate` on `tech-guide.md`** to validate stack choices through adversarial consensus before proceeding.
7. **UX Planning** — **Kickoff research first.** Then user flows, interaction patterns, accessibility, error handling, dark pattern audit _(skip for backend-only/library projects)_. Output: `ux-plan.md`
8. **UI Planning** — **Kickoff research first.** Then visual design system, typography, color palette, component inventory, layout _(skip for non-visual projects)_. Output: `ui-plan.md`
9. **Implementation** — Build it, using subagents for independent work
10. **E2E Test Generation** — **Kickoff research first.** Then generate Playwright CLI tests from user stories and UX flows _(skip if no testable UI/CLI)_. Output: `e2e-tests.md` + test files
11. **Testing & Verification** — Run all tests (including generated Playwright tests), verify requirements met. Consider `test-everything:test-full-suite` for comprehensive coverage.
12. **Delivery** — Final review, user verification, cleanup
13. **Plan Gap Audit** — Diff the implemented code against every planning artifact (`user-stories.md`, `architecture.md`, `tech-guide.md`, `ux-plan.md`, `ui-plan.md`, `e2e-tests.md`, each `phase-#-plan.md`). Record every missing, partial, or deviated item. Output: `plan-gaps.md`. Present gaps to user for severity confirmation before Phase 14.
14. **Fix All Gaps** — Work through `plan-gaps.md` in severity order (`blocker` → `major` → `minor` → `nit`). For each gap: implement the fix, re-run relevant tests, flip status to `fixed`. Phase is complete only when every non-`wont_fix` row is `fixed` and `plan-gaps.md` shows zero open items.

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

The `agents-argue:debate` skill is **not optional** for volatile, high-leverage decisions. Phases 5 (Architecture) and 6 (Tech Guide) have mandatory full-artifact debates. **In addition**, an automatic fast-path debate is required any time a decision in the "Volatile Decision Categories" list below is made or changed — no matter which phase it happens in.

### Volatile Decision Categories — Automatic Trigger

Any decision in any of these categories triggers `agents-argue:debate` automatically, even outside Phases 5 and 6. Each decision must be debated **at the time it is made or changed**, not deferred.

| Category | Examples | Why it's volatile |
| -------- | -------- | ----------------- |
| **LLM model / provider** | Claude Opus/Sonnet/Haiku version, GPT-4/5, Gemini, open-weights (Llama, Mistral), embedding models | Model family, capability, pricing, context window, and deprecation schedules shift every few months |
| **AI SDK / framework** | Anthropic SDK, OpenAI SDK, LangChain, LlamaIndex, MCP server libraries, Agent SDK, Vercel AI SDK | APIs and abstractions churn constantly; yesterday's recommended pattern becomes an anti-pattern |
| **Third-party API / service** | Auth provider (Clerk, Auth0, Supabase Auth), payments (Stripe, Lemon Squeezy), analytics, email, file storage, CDN, monitoring (Sentry, Datadog), vector DB, feature flags | Pricing, limits, TOS, and feature sets change; lock-in risk compounds |
| **Primary datastore** | Postgres vs. MySQL vs. SQLite vs. MongoDB vs. DynamoDB vs. cloud-native variants; hosted vs. self-hosted | High switching cost; downstream decisions depend on it |
| **Hosting / runtime** | AWS vs. GCP vs. Cloudflare vs. Fly vs. Render; Lambda vs. containers vs. edge; Vercel/Netlify vs. self-host | Cost model, cold-start, region, feature availability shift |
| **Core framework / language version** | React 18 → 19, Node 20 → 22, Rust edition, Python version, Axum/Express/Hono, Vite/Next/Nuxt | Breaking changes per major; ecosystem compatibility follows |
| **Pinned dependency majors** | ORM (Prisma vs. Drizzle vs. SQLx), test framework (Vitest vs. Jest), styling (Tailwind 3 vs. 4), auth libs, state libs | Majors break APIs; picking the wrong one costs a migration later |
| **Architectural pattern choice** | Monolith vs. services vs. serverless; REST vs. GraphQL vs. tRPC; event-driven vs. request/response; multi-tenant strategy; sync vs. async boundary | Each choice compounds across every downstream component |
| **Auth / session / token strategy** | JWT vs. sessions; access/refresh rotation; OAuth provider selection; permission model (RBAC vs. ABAC vs. ReBAC) | Security-critical, hard to reverse, vendor- and fashion-driven |
| **Data contract / schema choice** | Primary-key strategy (UUID v4 vs. v7 vs. ULID vs. sequential); soft-delete vs. hard; event schema format | Irreversible once data exists |
| **Deployment / CI pattern** | Docker vs. native builds, CI provider, rollout strategy, migration strategy | Provider feature sets and best practices shift |
| **Observability stack** | Logging (pino, tracing, OTel), metrics backend, tracing backend, error tracking | Cost and feature parity move quickly |

If a decision does not obviously fit this table but (a) a web search would return materially different answers than 12 months ago, or (b) the choice is hard to reverse, **default to debating it**. The cost of an unnecessary debate is minutes; the cost of a missed one is compounding tech debt.

### Two Debate Modes

**Mode A — Full-artifact debate (formal gate)**

Applies to Phases 5 and 6. Debate the whole artifact.

1. **Draft the artifact** — Write `architecture.md` or `tech-guide.md` using the template.
2. **Invoke the debate** — `Skill("agents-argue:debate", args: "<path to artifact>")`.
3. **Incorporate consensus** — The debate produces `consensus-plan.md` and `debate-transcript.md` in `docs/planning/`. Update the source artifact to reflect resolved decisions; add a `## Debate Outcomes` section.
4. **Log unresolved items** — Tag unresolved disagreements `NEEDS_HUMAN_DECISION` in `findings.md`.
5. **Mark phase complete** — Only after the artifact reflects the post-debate consensus.

**Mode B — Decision-level debate (fast path)**

Applies any time a single volatile decision is made or changed, in any phase. Do **not** wait for the next formal artifact review.

1. **Write a one-page decision brief** in `docs/planning/decisions/<ISO-date>-<slug>.md` with: the decision being made, 2–3 candidate options, constraints, and the proposed choice. Create `docs/planning/decisions/` if it does not exist.
2. **Invoke the debate** — `Skill("agents-argue:debate", args: "<path to brief>")`.
3. **Record outcome** in the brief: chosen option, rejected options with rationale, unresolved concerns.
4. **Fold the outcome** back into the correct downstream artifact (`architecture.md`, `tech-guide.md`, the relevant `phase-#-plan.md`, `data-map.md`, etc.).
5. **Log unresolved concerns** in `findings.md` tagged `NEEDS_HUMAN_DECISION`.
6. **Index the brief** — append a one-line entry to `docs/planning/decisions/INDEX.md`: `<ISO-date> | <slug> | <category> | <chosen option> | <artifact updated>`.

### Triggers during every phase

At the **start** of each phase, identify any volatile decision the phase is about to make. At the **end** of each phase, re-check whether any were made implicitly without a debate. If yes, run Mode B before closing the phase.

| Phase | Likely volatile decisions | Action |
| ----- | ------------------------- | ------ |
| 1. Requirements | Rarely — but flag any pre-committed vendor in the constraints | Debate if constraint is questionable |
| 3. Data Map | Primary datastore, key strategy, multi-tenant shape | Mode B per decision |
| 5. Architecture | All — formal artifact debate | Mode A |
| 6. Tech Guide | All — formal artifact debate; LLM/SDK choices if applicable | Mode A; Mode B for any LLM-specific choice not captured by the full debate |
| 7. UX / 8. UI | Component library, styling system if not pinned earlier | Mode B |
| 9. Implementation | Any unplanned tradeoff (library swap, new service, model change) | Mode B — **required**, not "if time permits" |
| 10. E2E Tests | Test framework if not already fixed | Mode B |
| 11 / 11.5 / 11.6 | Observability or reporting tool additions | Mode B |
| 13. Plan Gap Audit | New service/model surfaced as drift | Mode B before marking it "fixed" |
| 14. Fix All Gaps | Any replacement library or service used to close a gap | Mode B |

### When to skip a debate

Never skip for a Mode A gate. For Mode B, the only valid skip is when **all** of these hold:

- The user has explicitly pre-committed to this choice in writing (`phased-plan.md > ## Constraints`).
- The choice is trivially reversible (swap is < 1 day of work).
- No downstream artifact needs to change based on the outcome.

Record the skip reason in the decisions index with category `skipped-with-reason`.

### Why this is aggressive

Volatile decisions are where LLM training data goes stale fastest and where one wrong choice rewrites many downstream ones. Claude's default posture — picking the "known good" answer from training — silently commits the project to last year's best practice. Adversarial debate with current web grounding (via kickoff research) is the cheapest way to catch this before it compounds.

### Sequencing

- **Architecture debate (Phase 5) must finish before Tech Guide debate (Phase 6)** — the two formal gates run sequentially, not in parallel.
- **Mode B debates are always serialized against their dependencies** — debate the upstream decision first (e.g. pick the datastore before the ORM; pick the LLM before the prompt/context strategy).
- **Multiple independent Mode B debates may run in parallel** when their outcomes do not depend on each other.

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

## Phase Kickoff Research

LLM training data goes stale fast — framework versions, library APIs, design patterns, and best practices change constantly. Before starting each major phase, run a brief focused web search to ground decisions in current reality rather than memorized knowledge.

### Which phases require kickoff research

| Phase | Why | Priority |
| ----- | --- | -------- |
| 3. Data Map | Privacy regulations, data modeling patterns, storage options evolve | Medium |
| 5. Architecture | Architectural patterns and reference architectures change | High |
| 6. Tech Guide | **Highest value** — library versions, breaking changes, stack recommendations | **Critical** |
| 7. UX Planning | Accessibility standards (WCAG), interaction patterns, AI/agent UX patterns | Medium |
| 8. UI Planning | Design trends, component libraries, CSS features | Medium |
| 10. E2E Test Generation | Playwright API changes, current test patterns | High |

Phases 1, 2, 4, 9, 11, 12, 13, 14 do not require kickoff research — they are either internal, already research-based, derivative, or execution-focused.

### How it works

At the start of each listed phase, before touching the template:

1. **Formulate 2-4 focused queries** — Target "latest" and "current" information. Examples:
   - Phase 6: `"latest stable [framework] version 2026"`, `"[library] breaking changes [current year]"`, `"current recommended [stack type] 2026"`
   - Phase 5: `"current architectural patterns for [domain]"`, `"[system type] reference architecture 2026"`
   - Phase 10: `"Playwright latest API 2026"`, `"current best practices Playwright e2e [current year]"`
2. **Run WebSearch** — Use 3-5 minutes max. This is a grounding check, not a deep dive.
3. **Prefer official sources** — Framework docs, release notes, official guides. Skip low-quality aggregator content.
4. **Capture deltas** — Write findings to `findings.md` under a `## Phase [N] Kickoff Research` subsection. Focus on what changed vs. what you'd have assumed from training data.
5. **Apply findings to the phase artifact** — Let the research shape decisions in `architecture.md`, `tech-guide.md`, etc.

### Query templates

| Topic | Query pattern |
| ----- | ------------- |
| Framework version | `"[framework] latest stable version [current year]"` |
| Breaking changes | `"[library] breaking changes [version] to [version]"` |
| Best practices | `"current best practices [domain] [current year]"` |
| Patterns | `"latest [pattern type] patterns [current year]"` |
| Deprecations | `"[tool] deprecated [current year]"` |
| Reference architectures | `"[system type] reference architecture latest"` |

### Keep it bounded

Kickoff research is a **grounding check**, not a full research phase (that's Phase 2). Time-box it to 3-5 minutes per phase. The goal is to catch stale knowledge, not to produce a literature review.

### When to skip

Kickoff research may be skipped for a phase when:
- The user has explicitly provided current information for that phase
- The phase is trivial for this project (e.g., Data Map for a stateless CLI tool)
- Training data cutoff is recent enough for the specific topic (rare — default to searching)

Log any skips in `findings.md` with a reason.

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

* [templates/data-map.md](templates/data-map.md)

* [templates/user-stories.md](templates/user-stories.md)

* [templates/architecture.md](templates/architecture.md)

* [templates/tech-guide.md](templates/tech-guide.md)

* [templates/ux-plan.md](templates/ux-plan.md)

* [templates/ui-plan.md](templates/ui-plan.md)

* [templates/e2e-tests.md](templates/e2e-tests.md)

* [templates/plan-gaps.md](templates/plan-gaps.md)

* [templates/findings.md](templates/findings.md)

* [templates/progress.md](templates/progress.md)