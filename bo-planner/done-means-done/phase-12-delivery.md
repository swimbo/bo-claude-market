# Phase 12 — Delivery: Done Means Done

## Objective recap

Final review, cleanup, handoff, and explicit user sign-off.

## Artifacts (must exist and be non-empty)

- `docs/planning/phased-plan.md` — every non-skipped phase shows `Status: complete` (or `complete_with_override`).
- `docs/planning/progress.md` — final delivery entry with timestamp and user sign-off quote/paraphrase.
- Any user-facing delivery artifact: README update, changelog entry, release notes, demo GIF, or equivalent — appropriate to the project type.

## Hard Gates

- [ ] **All earlier phases closed**: every non-skipped phase 1–11 is `complete`. Phases marked `skipped` or `complete_with_override` list a reason in `phased-plan.md`.
- [ ] **README / docs updated**: user-facing documentation reflects what was actually built. Outdated sections edited, not abandoned.
- [ ] **Changelog / release note**: a single entry describing what shipped, in the project's conventional format (CHANGELOG.md, release description, PR body).
- [ ] **Demo evidence** *(where applicable)*: for UI / CLI features, a screenshot, terminal recording, or short GIF exists and is linked from `progress.md`.
- [ ] **Cleanup**: dead code, commented-out code, temporary scripts, and scratch files removed. Dependencies added during exploration but unused are removed.
- [ ] **Dependency audit**: `npm audit` / `pip-audit` / `cargo audit` (whichever applies) reviewed. High/critical issues either fixed or accepted with a logged rationale.
- [ ] **Secrets & config**: no live secrets in the repo; `.env.example` updated if env-var contract changed; rotation recorded if any secret was exposed during work.
- [ ] **`verification-before-completion` applied**: the `superpowers:verification-before-completion` discipline — run the commands, show the output — has been followed for the final sign-off run.
- [ ] **User sign-off**: the user has explicitly confirmed the work is acceptable. Evidence: timestamped line in `progress.md`: `User signed off on delivery <date>: <quote or paraphrase>`.

## Soft Checks

- [ ] Follow-up / next-step list distilled into `findings.md > ## Follow-ups`.
- [ ] Any `TODO` or `FIXME` introduced during work is either resolved or tracked externally.
- [ ] Post-mortem notes (what went well / what was painful) captured if the project had notable incidents.

## Exit Signal

> "The work is built, verified, documented, cleaned up, and explicitly accepted by the user."

After this phase, Phases 13–14 close the loop by auditing the implementation against the plan and fixing any drift.
