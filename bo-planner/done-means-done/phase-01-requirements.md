# Phase 1 — Requirements & Discovery: Done Means Done

## Objective recap

Understand intent, capture constraints, and snapshot the starting environment so every downstream phase is grounded in reality.

## Artifacts (must exist and be non-empty)

- `docs/planning/phased-plan.md` — contains Scope Fence (IN / OUT), Environment Snapshot, Phase Overview.
- `docs/planning/findings.md` — initialized, even if empty sections.
- `docs/planning/progress.md` — initialized with session start entry.

## Hard Gates

- [ ] **Intent captured**: `phased-plan.md` has a one-paragraph problem statement written in the user's words, not Claude's paraphrase.
- [ ] **IN scope fence**: `phased-plan.md > ## Scope > IN` lists concrete deliverables. No vague items like "improve X".
- [ ] **OUT scope fence**: `phased-plan.md > ## Scope > OUT` lists explicit non-goals. At least one non-trivial OUT item is present.
- [ ] **Environment snapshot**: `phased-plan.md > ## Environment` records: cwd, `git status` output summary, languages/frameworks detected, running services observed, existing `docs/planning/` state.
- [ ] **Constraints captured**: hard constraints (deadline, stack lock-in, compliance, budget, team) are listed in `phased-plan.md > ## Constraints`. Absence of a constraint is itself recorded ("None reported by user").
- [ ] **Phase overview drafted**: `phased-plan.md > ## Phases` lists which of phases 2–14 apply, which are skipped, and why.
- [ ] **User confirmation**: user has explicitly confirmed the scope fence. Evidence: timestamped line in `progress.md` of the form `User confirmed scope on <date>: <quote or paraphrase>`.

## Soft Checks

- [ ] Glossary of domain terms captured if the project uses jargon.
- [ ] Stakeholders / reviewers identified in `phased-plan.md`.
- [ ] Known unknowns (questions to revisit) logged in `findings.md`.

## Evidence format

Each Hard Gate should be satisfied by a link of the form `phased-plan.md#scope` or a short command output (`git status --short`) pasted into `progress.md`.

## Exit Signal

> "Scope is fenced, the environment is known, and the user has confirmed both."

After this phase, Phase 2 can assume the problem space is agreed and start researching real user pain in that space without re-negotiating scope.
