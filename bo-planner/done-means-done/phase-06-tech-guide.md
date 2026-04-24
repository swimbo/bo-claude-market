# Phase 6 — Tech Guide: Done Means Done

## Objective recap

Commit to a concrete tech stack with current versions, conventions, and dev environment so Implementation starts from a fixed foundation. Stress-test those choices via adversarial debate — this is the **highest-value** research step.

## Artifacts (must exist and be non-empty)

- `docs/planning/tech-guide.md` — populated from the template.
- `docs/planning/findings.md` — contains `## Phase 6 Kickoff Research`.
- `docs/planning/consensus-plan.md` — appended or updated by the Phase 6 debate.
- `docs/planning/debate-transcript.md` — updated or appended with the Phase 6 debate.

## Hard Gates

- [ ] **Kickoff research done — and substantive**: `findings.md > ## Phase 6 Kickoff Research` captures current stable versions, breaking changes since last-known version, and deprecations. This is the highest-priority research step — skimpy output blocks the phase.
- [ ] **Language & runtime**: `tech-guide.md > ## Language & Runtime` pins language versions (e.g. `Node 22.x`, `Rust 1.83+`, `Python 3.12+`).
- [ ] **Framework selection**: `tech-guide.md > ## Frameworks` lists chosen frameworks with explicit versions and a one-line rationale referencing research findings.
- [ ] **Dependency list**: `tech-guide.md > ## Dependencies` pins every non-trivial dependency to a version known-stable as of kickoff research.
- [ ] **Coding conventions**: `tech-guide.md > ## Conventions` states formatting tool, linter, typing strictness, import style, naming.
- [ ] **Testing stack**: unit, integration, and e2e tooling chosen with versions.
- [ ] **Dev environment**: `tech-guide.md > ## Dev Environment` documents required local services, setup commands, and env-var contract.
- [ ] **Build & run commands**: canonical `build`, `test`, `lint`, `dev`, `start` commands recorded verbatim.
- [ ] **CI shape**: a sketch of CI stages (even if CI is out of scope for v1, the shape is captured).
- [ ] **Alignment with Architecture**: every component in `architecture.md > ## Components` has a clearly-mapped stack choice here. No orphans, no mismatches.
- [ ] **Adversarial debate invoked**: `Skill("agents-argue:debate", args: "<path to tech-guide.md>")` run. Evidence: debate artifacts exist referencing current `tech-guide.md`. Debate runs **after** Architecture debate.
- [ ] **Consensus incorporated**: `tech-guide.md` updated to reflect the debate consensus. `## Debate Outcomes` section summarizes what changed.
- [ ] **Unresolved items escalated**: open disagreements tagged `NEEDS_HUMAN_DECISION` in `findings.md` and resolved by the user before phase close.

## Soft Checks

- [ ] Compatibility matrix across dependencies verified (no known incompat combos).
- [ ] License audit for any GPL/AGPL/restrictive dependencies.
- [ ] Upgrade path for pinned majors noted ("v5 expected 2026 Q3, migration will affect X").

## Blocking condition

Phase 6 is **never** complete without a completed debate. Skipping requires explicit user override logged in `progress.md`; phase then marked `complete_with_override`.

## Exit Signal

> "The stack is chosen, pinned, conventionally documented, aligned with architecture, and debate-hardened."

After this phase, Phase 9 (Implementation) can scaffold without re-litigating stack decisions.
