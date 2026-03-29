---
name: done
description: "Verify completion before declaring a task done. Checks all phases, runs verification, and asks user to confirm."
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
---

## Completion Verification Protocol

Before declaring ANY task complete, run through this checklist:

### Step 1: Read Planning State

<span data-proof="suggestion" data-id="m1772856376792_6" data-by="ai:external-agent" data-kind="replace">Read task_plan.md, findings.md, and progress.md. Check:</span>

* <span data-proof="suggestion" data-id="m1772856376792_6" data-by="ai:external-agent" data-kind="replace">Are ALL phases marked</span> <span data-proof="suggestion" data-id="m1772856376792_6" data-by="ai:external-agent" data-kind="replace">`complete`?</span>

* <span data-proof="suggestion" data-id="m1772856376792_6" data-by="ai:external-agent" data-kind="replace">Does every phase have a filled-in</span> <span data-proof="suggestion" data-id="m1772856376792_6" data-by="ai:external-agent" data-kind="replace">`Verification`</span> <span data-proof="suggestion" data-id="m1772856376792_6" data-by="ai:external-agent" data-kind="replace">section?</span>

* <span data-proof="suggestion" data-id="m1772856376792_6" data-by="ai:external-agent" data-kind="replace">Are there any unresolved errors in the error log?</span>

### Step 2: Run Project Checks

Based on what the project contains:

* **If tests exist**: Run the test suite. Report pass/fail count.

* **If it's a build project**: Run the build. Confirm it succeeds.

* **If there's a linter configured**: Run lint. Report issues.

* **If it's a web app**: Check that the dev server starts without errors.

### Step 3: Cross-Plugin Quality Gates

Check for artifacts from other plugins and include their results in the completion check:

1. **Enterprise Assessment** — Check for `docs/planning/enterprise-assessment.md` or `enterprise-assessment-report.md`:
   - If found, read the overall grade and risk posture
   - If grade < B (below 75%): **WARN** "Enterprise assessment grade is [grade] ([pct]%) — risk posture is [posture]. Consider remediating Critical/High findings before delivery."
   - List count of Critical and High findings
   - This is a warning, not a blocker — the user decides whether to proceed

2. **Design Compliance** — Check for `docs/planning/design-compliance.md`:
   - If found, read the critical issue count
   - If critical issues > 0: **WARN** "[n] critical design compliance issues remain (raw hex colors, wrong fonts, etc.)"
   - This is a warning, not a blocker

3. **Test Coverage** — Check for test-everything audit results or `.test-results/`:
   - If found, report test pass/fail counts and coverage metrics
   - If tests are failing: **BLOCK** "Tests are failing — must fix before delivery"

Include these results in the Step 5 summary output.

### Step 4: Scope Audit

<span data-proof="suggestion" data-id="m1772856376784_5" data-by="ai:external-agent" data-kind="replace">Compare the IN scope items from task_plan.md against what was actually delivered:</span>

* List each IN scope item and whether it's done

* Flag any OUT scope items that were accidentally included

* Flag any IN scope items that were missed

### <span data-proof="suggestion" data-id="m1772856376777_4" data-by="ai:external-agent" data-kind="replace">Step 5: Ask User</span>

Present the results to the user using AskUserQuestion:

```
Completion check:
- Phases: {completed}/{total}
- User stories: {delivered}/{total} implemented
- Tests: {pass}/{total} passing
- Scope: {delivered}/{in_scope} items delivered
- Unresolved errors: {count}
- Enterprise assessment: {grade} ({pct}%) — {posture} [or "not run"]
- Design compliance: {critical} critical issues [or "not run"]

Ready to mark complete? Or should I address [specific issues]?
```

Do NOT declare success until the user confirms.

### <span data-proof="suggestion" data-id="m1772856376764_2" data-by="ai:external-agent" data-kind="replace">Step 6: Update Files</span>

If user confirms:

* <span data-proof="suggestion" data-id="m1772856376756_1" data-by="ai:external-agent" data-kind="replace">Mark all phases complete in task_plan.md</span>

* <span data-proof="suggestion" data-id="m1772856376756_1" data-by="ai:external-agent" data-kind="replace">Add final session entry to progress.md</span>

* Log completion timestamp

If this is a test-heavy project, consider invoking the `test-everything:test-audit` skill to validate coverage.

<!-- PROOF
{
  "version": 2,
  "marks": {
    "m1772856376792_6": {
      "kind": "replace",
      "by": "ai:external-agent",
      "createdAt": "2026-03-07T04:06:16.792Z",
      "range": {
        "from": 347,
        "to": 549
      },
      "content": "Read all files in docs/planning/. Check:\nAre ALL phases marked complete in phased-plan.md?\nDoes every phase-#-plan.md have a filled-in Verification section?\nAre there any unresolved errors in progress.md?",
      "status": "pending"
    },
    "m1772856376784_5": {
      "kind": "replace",
      "by": "ai:external-agent",
      "createdAt": "2026-03-07T04:06:16.784Z",
      "range": {
        "from": 899,
        "to": 980
      },
      "content": "Compare the IN scope items from docs/planning/phased-plan.md against what was actually delivered:",
      "status": "pending"
    },
    "m1772856376777_4": {
      "kind": "replace",
      "by": "ai:external-agent",
      "createdAt": "2026-03-07T04:06:16.777Z",
      "range": {
        "from": 1137,
        "to": 1153
      },
      "content": "Step 4: User Stories Check\nRead docs/planning/user-stories.md. For each user story, verify:\nIs the story implemented?\nDoes verification exist for it?\nStep 5: Ask User",
      "status": "pending"
    },
    "m1772856376769_3": {
      "kind": "insert",
      "by": "ai:external-agent",
      "createdAt": "2026-03-07T04:06:16.769Z",
      "range": {
        "from": 1258,
        "to": 1306
      },
      "content": "\n- User stories: {delivered}/{total} implemented",
      "status": "pending"
    },
    "m1772856376764_2": {
      "kind": "replace",
      "by": "ai:external-agent",
      "createdAt": "2026-03-07T04:06:16.764Z",
      "range": {
        "from": 1530,
        "to": 1550
      },
      "content": "Step 6: Update Files",
      "status": "pending"
    },
    "m1772856376756_1": {
      "kind": "replace",
      "by": "ai:external-agent",
      "createdAt": "2026-03-07T04:06:16.756Z",
      "range": {
        "from": 1573,
        "to": 1655
      },
      "content": "Mark all phases complete in docs/planning/phased-plan.md\nAdd final session entry to docs/planning/progress.md",
      "status": "pending"
    }
  }
}
-->

<!-- PROOF:END -->
