# Done Means Done

Canonical per-phase completion checklists for the 14-phase `bo-planning` workflow.

A phase is **not done** until every **Hard Gate** in its checklist is satisfied. Soft checks are warnings, not blockers — a phase may complete with soft checks open if the user accepts the risk, but each open soft check must be logged in `docs/planning/progress.md`.

## How to use

- **When starting a phase**: Read the matching checklist and copy the **Hard Gates** into the `Verification` section of `docs/planning/phase-#-plan.md`. Do not paraphrase — copy verbatim so audits are trivial.
- **When closing a phase**: Walk the checklist top-to-bottom. Mark each gate with the evidence that satisfies it (command output, file path + line, artifact link). "It should work" is not evidence.
- **When running `/done`**: The completion-verification protocol cross-references these checklists against `docs/planning/phased-plan.md` and each `phase-#-plan.md`. Any missing Hard Gate blocks completion.

## Index

| Phase | Checklist |
| ----- | --------- |
| 1. Requirements & Discovery | [phase-01-requirements.md](phase-01-requirements.md) |
| 2. Pain Point Research | [phase-02-pain-point-research.md](phase-02-pain-point-research.md) |
| 3. Data Map | [phase-03-data-map.md](phase-03-data-map.md) |
| 4. User Stories | [phase-04-user-stories.md](phase-04-user-stories.md) |
| 5. Architecture | [phase-05-architecture.md](phase-05-architecture.md) |
| 6. Tech Guide | [phase-06-tech-guide.md](phase-06-tech-guide.md) |
| 7. UX Planning | [phase-07-ux-planning.md](phase-07-ux-planning.md) |
| 8. UI Planning | [phase-08-ui-planning.md](phase-08-ui-planning.md) |
| 9. Implementation | [phase-09-implementation.md](phase-09-implementation.md) |
| 10. E2E Test Generation | [phase-10-e2e-test-generation.md](phase-10-e2e-test-generation.md) |
| 11. Testing & Verification | [phase-11-testing-verification.md](phase-11-testing-verification.md) |
| 12. Delivery | [phase-12-delivery.md](phase-12-delivery.md) |
| 13. Plan Gap Audit | [phase-13-plan-gap-audit.md](phase-13-plan-gap-audit.md) |
| 14. Fix All Gaps | [phase-14-fix-all-gaps.md](phase-14-fix-all-gaps.md) |

## Skippable phases

Some phases are conditional (see `SKILL.md` > "Phase Planning"). If a phase is skipped, record the reason in `findings.md` and mark the phase `skipped` in `phased-plan.md` — do **not** mark it `complete`.

| Phase | Skippable when |
| ----- | -------------- |
| 2. Pain Point Research | Internal tooling with no external users; user-supplied research; bug fix/refactor with no new behavior |
| 7. UX Planning | Backend-only or pure-library project |
| 8. UI Planning | Non-visual project (backend, library, MCP server) |
| 10. E2E Test Generation | No testable UI or CLI |

Phases 1, 3–6, 9, 11–14 are **never** skippable.

## Conventions used in every checklist

- **Artifacts**: Files that must exist and be non-empty in `docs/planning/`.
- **Hard Gates**: Blocking checks. Every one must be satisfied before the phase is marked `complete`.
- **Soft Checks**: Advisory. Any open soft check must be logged in `progress.md` with a reason.
- **Evidence**: What proves a gate is satisfied (command + output, file + line, screenshot, test-run ID).
- **Exit Signal**: One sentence describing what the next phase can now safely assume.
