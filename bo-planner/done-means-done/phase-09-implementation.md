# Phase 9 — Implementation: Done Means Done

## Objective recap

Build the system against the plan using subagents for independent work.

## Artifacts (must exist and be non-empty)

- Each `docs/planning/phase-#-plan.md` that participates in Implementation has a populated `Tasks` checklist with every task checked, a populated `Verification` section, and `Status: complete`.
- `docs/planning/progress.md` — per-session log with timestamps, commands run, errors, and mutations to approach.
- Working source code matching the IN scope items in `phased-plan.md`.

## Hard Gates

- [ ] **Scope fidelity**: every IN-scope deliverable in `phased-plan.md` is represented by at least one merged/committed change. Nothing OUT-of-scope was implemented.
- [ ] **User-story coverage**: every P0 story from `user-stories.md` has a code path that fulfils its acceptance criteria. Evidence: story ID referenced in commit messages, code comments, or `progress.md`.
- [ ] **Architecture adherence**: implemented component boundaries match `architecture.md > ## Components`. Deviations were negotiated and recorded in `progress.md`.
- [ ] **Tech-guide adherence**: versions, conventions, and dev-env commands match `tech-guide.md`. Deviations recorded with rationale.
- [ ] **Subagent delegation used where required**: any phase with 2+ independent tasks dispatched parallel agents; delegation table in `phased-plan.md > ## Delegated Work` shows statuses and results.
- [ ] **Error log is clean**: `progress.md > ## Errors` has no open errors. Every entry is either `resolved` with resolution, or tagged `accepted_risk` with a user sign-off line.
- [ ] **3-strike protocol respected**: no task shows 3+ repeated identical failing attempts. Every failure has a mutation entry.
- [ ] **Mid-phase volatile decisions debated**: every decision made during Implementation that falls into a Volatile Decision Category (LLM/model, AI SDK, third-party API/service, datastore swap, framework version bump, dependency major, architectural pattern change, auth strategy, data contract, deploy/CI pattern, observability) has a Mode B decision brief in `docs/planning/decisions/`, an `agents-argue:debate` outcome recorded in the brief, and an entry in `docs/planning/decisions/INDEX.md`. No silent adoption.
- [ ] **Secrets hygiene**: no secrets in code, commits, or planning files. `.env` present in `.gitignore` if used.
- [ ] **Build succeeds**: canonical build command from `tech-guide.md` runs to success locally. Output pasted or linked in `progress.md`.
- [ ] **Lint clean**: canonical lint command runs clean. Output linked.
- [ ] **Type-check clean** *(typed languages)*: type-check runs clean.

## Soft Checks

- [ ] Commit messages reference user-story IDs or phase plan tasks.
- [ ] TODOs left in code are logged in `progress.md` with intended resolution phase.
- [ ] Performance-sensitive paths have a baseline benchmark noted.

## Anti-patterns that block completion

- Silent scope expansion — OUT-of-scope work merged without negotiating scope. Block until rolled back or scope updated.
- Phase marked complete with empty `Verification` section.
- Independent tasks done sequentially when subagents were available — repeat for the remaining work.

## Exit Signal

> "Every IN-scope outcome has running code, built and linted clean, matching architecture and tech guide, with a clean error log."

After this phase, Phases 10–11 can exercise the system end-to-end.
