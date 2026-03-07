---
name: status
description: "Show current planning status — phases, scope, delegated agents, and verification state."
---

<span data-proof="suggestion" data-id="m1772856365027_4" data-by="ai:external-agent" data-kind="replace">Read task_plan.md from the current project directory and display a compact status summary.</span>

## What to Show

1. **Goal**: One-line goal from the plan
2. **Scope**: IN scope items (abbreviated)
3. **Current Phase**: Which phase is active
4. **Phase Progress**: Count with status icons
5. **Delegated Work**: Any subagent tasks and their status
6. **Verification**: Whether current phase verification is documented
7. **<span data-proof="suggestion" data-id="m1772856365015_3" data-by="ai:external-agent" data-kind="replace">Errors</span>**<span data-proof="suggestion" data-id="m1772856365015_3" data-by="ai:external-agent" data-kind="replace">: Count of logged errors</span>

## Status Icons

* pending: (pending)

* in\_progress: (active)

* complete: (done)

* blocked: (blocked)

## Output Format

```
Planning Status

Goal: [goal statement]
Scope: [abbreviated IN items]
Current: Phase {N} of {total} ({percent}%)

  [icon] Phase 1: {name}
  [icon] Phase 2: {name} <- you are here
  [icon] Phase 3: {name}

Delegated: {count} subagent tasks ({completed}/{total})
Verification: {current phase verified? yes/no}
Files: task_plan.md {y|n} | findings.md {y|n} | progress.md {y|n}
Errors logged: {count}
```

## If No Planning Files Exist

```
No planning files found.
Run /plan to start a new planning session.
```

<!-- PROOF
{
  "version": 2,
  "marks": {
    "m1772856365027_4": {
      "kind": "replace",
      "by": "ai:external-agent",
      "createdAt": "2026-03-07T04:06:05.027Z",
      "range": {
        "from": 126,
        "to": 216
      },
      "content": "Read docs/planning/phased-plan.md from the current project directory and display a compact status summary.",
      "status": "pending"
    },
    "m1772856365015_3": {
      "kind": "replace",
      "by": "ai:external-agent",
      "createdAt": "2026-03-07T04:06:05.015Z",
      "range": {
        "from": 514,
        "to": 544
      },
      "content": "Errors: Count of logged errors from docs/planning/progress.md",
      "status": "pending"
    },
    "m1772856365004_2": {
      "kind": "replace",
      "by": "ai:external-agent",
      "createdAt": "2026-03-07T04:06:05.004Z",
      "range": {
        "from": 977,
        "to": 1042
      },
      "content": "Files: phased-plan {y|n} | architecture {y|n} | user-stories {y|n} | findings {y|n} | progress {y|n}\nPhase plans: phase-1 {y|n} | phase-2 {y|n} | ...",
      "status": "pending"
    },
    "m1772856364985_1": {
      "kind": "replace",
      "by": "ai:external-agent",
      "createdAt": "2026-03-07T04:06:04.985Z",
      "range": {
        "from": 1095,
        "to": 1119
      },
      "content": "No planning files found in docs/planning/.",
      "status": "pending"
    }
  }
}
-->

<!-- PROOF:END -->
