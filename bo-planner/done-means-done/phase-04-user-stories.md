# Phase 4 — User Stories: Done Means Done

## Objective recap

Translate requirements and Phase 2 pain findings into user stories with acceptance criteria, priorities, and phase mapping — so Implementation has a testable, prioritized backlog.

## Artifacts (must exist and be non-empty)

- `docs/planning/user-stories.md` — populated from the template.

## Hard Gates

- [ ] **Pain reference**: every story links to at least one entry in `findings.md > ## Pain Point Research` OR is explicitly flagged `source: user request` / `source: internal`. No story may have an empty source.
- [ ] **Canonical shape**: each story uses the form `As a <role>, I want <capability>, so that <outcome>`.
- [ ] **Acceptance criteria**: each story has **≥ 2 acceptance criteria** written in `Given / When / Then` (or equivalent) form. Criteria are testable, not aspirational.
- [ ] **Priority assigned**: every story is tagged `P0`, `P1`, `P2`, or `P3` (or equivalent) with a one-line rationale.
- [ ] **Phase mapping**: every story is mapped to one or more of Phases 9–12. Unmapped stories are rejected or deferred, not left floating.
- [ ] **Scope alignment**: every story is reconciled against `phased-plan.md > ## Scope`. Stories outside IN scope are either moved to a "Deferred" section or Scope is renegotiated with the user.
- [ ] **Coverage sanity check**: for each IN-scope deliverable in `phased-plan.md`, at least one story exists that exercises it.
- [ ] **User review**: the story list has been presented to the user and confirmed. Confirmation noted in `progress.md`.

## Soft Checks

- [ ] Non-functional stories captured (performance, accessibility, observability, security).
- [ ] Edge-case and failure-mode stories exist, not just happy paths.
- [ ] Personas defined if the system has multiple user roles.

## Evidence format

Each story carries an ID (e.g. `US-001`) that will be reused by `e2e-tests.md`, phase plans, and `plan-gaps.md`. IDs are non-negotiable for downstream traceability.

## Exit Signal

> "Every in-scope outcome has at least one testable story, prioritized, mapped to a phase, and traceable back to real user pain or an explicit user request."

After this phase, Architecture can size the system against a fixed backlog.
