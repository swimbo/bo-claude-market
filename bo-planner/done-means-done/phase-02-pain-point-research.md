# Phase 2 — Pain Point Research: Done Means Done

## Objective recap

Ground the project in real user pain — forum posts, GitHub issues, reviews, support threads — so user stories in Phase 4 are rooted in actual problems rather than assumed ones.

## Artifacts (must exist and be non-empty)

- `docs/planning/findings.md` — populated `## Pain Point Research` section with a table or structured list of entries.

## Hard Gates

- [ ] **Problem-space framing**: `findings.md > ## Pain Point Research > ### Problem Space` describes the domain and lists existing tools/products addressing the same need.
- [ ] **Minimum source coverage**: at least **5 distinct entries** in the Pain Point Research table.
- [ ] **Platform diversity**: entries span **at least 2 different source platforms** (e.g. GitHub issues + Reddit, forum + Stack Overflow, App Store reviews + HN).
- [ ] **Per-entry fields**: every entry records Source URL, complaint summary, frequency signal (one-off vs. recurring theme), and relevance to our project scope.
- [ ] **Pattern synthesis**: a `### Themes` subsection groups recurring complaints into named patterns, distinguishing recurring themes from one-off gripes.
- [ ] **Competitor friction analysis**: `### Competitor Friction` summarises where users report friction with at least 2 existing solutions in this space.
- [ ] **User review**: top findings have been presented to the user and the user has answered "do any of these change your priorities or scope?" — answer recorded in `progress.md`.
- [ ] **Scope reconciliation**: if the user's answer changes scope, `phased-plan.md > ## Scope` has been updated and the change is linked from `progress.md`.

## Soft Checks

- [ ] Links captured include publication date or recency signal (helps judge if the pain is still current).
- [ ] At least one source is from the last 12 months.
- [ ] Pain points tagged by severity or user impact where inferable.

## Skip condition

Phase 2 may be skipped ONLY when:
- Purely internal tooling, no external users, **or**
- User has supplied their own research and it has been attached/linked in `findings.md`, **or**
- Bug fix or refactor with no new user-facing behavior.

**If skipped**: record the skip reason as a paragraph in `findings.md > ## Pain Point Research > ### Skipped`, and mark the phase `skipped` (not `complete`) in `phased-plan.md`.

## Evidence format

Each entry in the research table links to a concrete URL. Claim that "users are frustrated with X" is never acceptable without a linked source.

## Exit Signal

> "The top real-world pain points in this problem space are documented, the user has seen them, and scope reflects what we learned."

After this phase, Phase 4 (User Stories) can reference specific findings instead of inventing motivations.
