# Phase 8 — UI Planning: Done Means Done

## Objective recap

Commit to a visual design system — typography, color, spacing, components — so Implementation produces a coherent UI, not ad-hoc styling.

## Artifacts (must exist and be non-empty)

- `docs/planning/ui-plan.md` — populated from the template.
- `docs/planning/findings.md` — contains `## Phase 8 Kickoff Research`.

## Hard Gates

- [ ] **Kickoff research done**: current component-library state, CSS feature maturity, and design trends captured in `findings.md > ## Phase 8 Kickoff Research`.
- [ ] **Design tokens defined**: `ui-plan.md > ## Tokens` declares colors (semantic + raw), typography (family, scale, weights, line-heights), spacing scale, radii, shadows, motion durations/easings.
- [ ] **Color contrast verified**: every foreground/background pair used for text meets WCAG AA (4.5:1 body, 3:1 large). Contrast ratios listed or linked.
- [ ] **Dark mode stance**: dark-mode is either fully specified or explicitly marked out-of-scope with a note.
- [ ] **Typography applied**: monospaced typography adjustments made where relevant (code blocks, CLI output panels).
- [ ] **Component inventory**: `ui-plan.md > ## Components` lists every UI primitive the app needs (Button, Input, Card, Dialog, Table, …) with states (default/hover/active/focus/disabled/error/loading).
- [ ] **Layout system**: grid/flex primitives, breakpoints, container widths declared.
- [ ] **Iconography**: icon set chosen with rationale; sizes and usage conventions recorded.
- [ ] **Motion**: reduced-motion handling declared; transition durations within an accessibility-safe range.
- [ ] **Brand stance**: `ui-plan.md > ## Brand` states whether the product uses a distinct brand palette or a neutral one; Anthropic-brand palette referenced only if explicitly requested.
- [ ] **Alignment with UX**: every flow in `ux-plan.md` can be composed from components in this inventory. No orphan flows.
- [ ] **Anti-pattern audit**: `ui-plan.md > ## Anti-Pattern Audit` confirms we are not committing the visual AI-slop failure modes (gradient soup, generic card grids, inconsistent rhythm, decorative-only shadows).
- [ ] **Cross-reference to research**: `research/ui-design.md` cited where applicable.

## Soft Checks

- [ ] Sample `cn()` utility usage shown (if Tailwind + shadcn-style stack).
- [ ] Figma / design-file pointer or equivalent source-of-truth listed.
- [ ] Empty-state and skeleton-loader visuals specified.

## Skip condition

Phase 8 may be skipped for non-visual projects (pure backend, library, MCP server). CLI / TUI projects must still complete this phase, adapting "UI" to terminal composition.

**If skipped**: record skip reason in `ui-plan.md` (stub file fine), mark phase `skipped` in `phased-plan.md`.

## Exit Signal

> "There is a design token system, a component inventory, and every UX flow is buildable from it."

After this phase, Implementation can compose screens from a fixed kit.
