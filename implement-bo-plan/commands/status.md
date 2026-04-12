---
name: status
description: "One-screen implementation status. Shows current phase, last gate results, open plan gaps, and overrides in effect."
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
---

Produce a single-screen status snapshot. Do not modify any files.

## Data Sources

Read (each may be absent — handle gracefully):

- `docs/planning/phased-plan.md` — phase status table
- `docs/planning/progress.md` — last entry, override log
- `docs/planning/design-compliance.md` — last design gate result
- `docs/planning/enterprise-assessment.md` — last enterprise grade
- `docs/planning/plan-gaps.md` — gap counts by severity and status

## Output Format

```
Implementation status — {project name / cwd}

Current phase:       {N — name}                    (status: {in_progress|blocked|complete})
Last activity:       {timestamp from progress.md}   {one-line summary}

Gate results
  Tests:             {pass}/{total} passing         ({coverage}% coverage, if available)
  Design:            {critical} critical, {major} major                (Phase 11.5)
  Enterprise:        Grade {X} ({pct}%) — {posture}  (Phase 11.6)

Plan gaps (Phase 13/14)
  Blocker:           {open}/{total}
  Major:             {open}/{total}
  Minor:             {open}/{total}
  Nit:               {open}/{total}
  Accepted wont_fix: {count}

Overrides in effect: {list or "none"}
Next action:         {what /resume or /phase would do}
```

If no planning directory exists, print:
```
No bo-planner plan found. Run /bo-planner:plan first.
```

If planning exists but implementation hasn't started:
```
Plan found. Preflight status: {ready|blocked on phases 1-8}.
Run /implement-bo-plan:implement to begin.
```

## Rules

- Read-only. No writes, no skill invocations, no subagent dispatches.
- If a file is missing, show `—` for its fields, don't error.
- Keep to the format above so the output stays parseable.
