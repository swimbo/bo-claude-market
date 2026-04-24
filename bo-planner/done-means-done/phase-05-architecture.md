# Phase 5 — Architecture: Done Means Done

## Objective recap

Design the system: component boundaries, API surface, integration points, infrastructure. Stress-test those decisions via adversarial debate before handing to Tech Guide.

## Artifacts (must exist and be non-empty)

- `docs/planning/architecture.md` — populated from the template.
- `docs/planning/findings.md` — contains `## Phase 5 Kickoff Research`.
- `docs/planning/consensus-plan.md` — produced by `agents-argue:debate`.
- `docs/planning/debate-transcript.md` — produced by `agents-argue:debate`.

## Hard Gates

- [ ] **Kickoff research done**: `findings.md > ## Phase 5 Kickoff Research` captures 2–4 queries on current architectural patterns and reference architectures for this domain, with deltas vs. training-data assumptions.
- [ ] **Component boundaries**: `architecture.md > ## Components` names every service/module with responsibility, owned data, and public interface.
- [ ] **API surface**: `architecture.md > ## API Surface` lists routes/operations/tools with method, shape, auth requirement, idempotency, and error semantics.
- [ ] **Data ownership**: every entity from `data-map.md` has exactly one owning component — no ambiguous ownership.
- [ ] **Integration points**: `architecture.md > ## Integrations` lists external services, auth, rate limits, and failure-mode handling.
- [ ] **Infrastructure**: `architecture.md > ## Infrastructure` states deployment topology, environments, persistence, and secrets strategy.
- [ ] **Non-functional requirements**: performance, scalability, availability, and observability targets recorded.
- [ ] **Adversarial debate invoked**: `Skill("agents-argue:debate", args: "<path to architecture.md>")` has been run. Evidence: `consensus-plan.md` and `debate-transcript.md` exist and reference the current `architecture.md`.
- [ ] **Consensus incorporated**: `architecture.md` has been updated to reflect resolved decisions from `consensus-plan.md`. A `## Debate Outcomes` section summarizes what changed.
- [ ] **Unresolved items escalated**: any disagreements the debate could not resolve are logged in `findings.md` tagged `NEEDS_HUMAN_DECISION`.
- [ ] **User resolution**: every `NEEDS_HUMAN_DECISION` item from this phase is resolved by the user before the phase is marked `complete`. Resolutions recorded in `progress.md`.

## Soft Checks

- [ ] Alternatives considered and explicitly rejected are listed, with rationale.
- [ ] Security boundaries diagram or description present.
- [ ] Failure-domain and blast-radius analysis for the top 3 risk points.

## Blocking condition

Phase 5 is **never** complete without a completed debate. Skipping the debate requires explicit user override logged in `progress.md` with a reason — and even then, the phase is marked `complete_with_override`, not `complete`.

## Exit Signal

> "Components, APIs, and infrastructure are chosen, written down, stress-tested by adversarial debate, and reconciled by the user."

After this phase, Phase 6 can pick a concrete stack to realize these components.
