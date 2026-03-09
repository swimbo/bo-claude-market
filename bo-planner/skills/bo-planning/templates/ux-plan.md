# UX Plan: \[Feature/Project Name]

## Objective

\[What user experience problem this plan addresses]

## Target Users

<!-- Link to user-stories.md for detailed personas -->

| User Type | Context | Primary Goal | Technical Literacy |
| --------- | ------- | ------------ | ------------------ |
| \[Role]   | \[How they encounter this tool] | \[What they need to accomplish] | Low/Medium/High |

## User Flows

### Flow 1: \[Primary Flow Name]

```
[Step 1] → [Step 2] → [Step 3] → [Outcome]
```

* Happy path: \[Expected progression]
* Error path: \[What happens when things go wrong]
* Recovery: \[How the user gets back on track]

### Flow 2: \[Secondary Flow Name]

```
[Step 1] → [Step 2] → [Outcome]
```

## Information Architecture

<!-- How content and navigation are organized -->

```
[Top-level structure]
├── [Section 1]
│   ├── [Subsection]
│   └── [Subsection]
├── [Section 2]
└── [Section 3]
```

## Interaction Patterns

<!-- Which modality fits each interaction? -->

| Interaction | Pattern | Rationale |
| ----------- | ------- | --------- |
| \[Action]   | Inline / Sidebar / Modal / CLI / Panel | \[Why this pattern] |

### CLI/Terminal Interactions (if applicable)

* Command structure: `tool [noun] [verb]` or custom
* Output format: Table / JSON / Plain text
* Progress indication: Spinner / Progress bar / Step log
* Streams: stdout for data, stderr for status/errors
* Interactive prompts: Yes/No (always bypassable with flags)

### IDE Integration (if applicable)

* Surface: Activity Bar / Sidebar / Panel / Status Bar / Editor
* Native components vs Webview: \[Decision]
* Theme compatibility: \[How it adapts to user themes]

## Accessibility Requirements

| Requirement | Implementation |
| ----------- | -------------- |
| Color contrast | Minimum 4.5:1 body text, 3:1 large text (WCAG AA) |
| Color independence | Never use color alone to convey meaning |
| Keyboard navigation | All actions reachable without mouse |
| Screen reader support | \[Specific accommodations] |
| Reduced motion | Respect `prefers-reduced-motion` / provide `--no-animation` flag |
| Text scaling | UI accommodates 200% text zoom without breaking |

### CLI Accessibility (if applicable)

* [ ] `--no-animation` flag disables cursor-moving spinners
* [ ] `--simple` flag strips ASCII art and box-drawing characters
* [ ] Output uses blank lines to separate logical blocks
* [ ] Tabular data repeats context per row (grep-parseable)

## Error Handling Strategy

<!-- Following Nielsen's heuristic: help users recognize, diagnose, recover -->

| Error Type | User Sees | Recovery Action |
| ---------- | --------- | --------------- |
| \[Category] | \[Plain-language message + error code] | \[Specific next step] |

Principles:
* Validate inputs in real-time where possible
* Provide "dry-run" or preview for destructive actions
* Error messages include: what happened, why, and how to fix it
* Never expose raw stack traces or HTTP codes without translation

## Feedback & System Status

| User Action | Immediate Feedback | Completion Signal |
| ----------- | ------------------ | ----------------- |
| \[Action]   | \[What they see instantly] | \[How they know it's done] |

* Long operations: Show progress with cancel option
* Background tasks: Notify on completion
* Silent failures: Prohibited — every action must produce visible feedback

## AI/Agent Interactions (if applicable)

<!-- Following Microsoft HAX guidelines -->

| Phase | Guideline | Implementation |
| ----- | --------- | -------------- |
| Initial | Set clear capability expectations | \[How you communicate what the AI can/can't do] |
| During | Respect user flow state | \[When and how AI intervenes] |
| When Wrong | Support efficient correction | \[Undo, dismiss, diff-view mechanisms] |
| Over Time | Learn from user behavior | \[Context memory, personalization controls] |

* Confidence communication: \[How uncertainty is shown]
* Chain-of-thought: \[Whether reasoning is displayed before actions]
* Human-in-the-loop: \[Where user approval is required]

## Dark Pattern Audit

<!-- Verify NONE of these exist in the design -->

* [ ] No trick questions or confusing double-negatives
* [ ] No sneaked additions (unsolicited items, telemetry)
* [ ] No roach motels (hard to exit/cancel/unsubscribe)
* [ ] No confirmshaming (guilt-tripping opt-out language)
* [ ] No hidden costs or surprise dependencies
* [ ] No misdirection via visual hierarchy manipulation
* [ ] No disguised ads or upsells masquerading as features
* [ ] No bad defaults (settings optimize for user, not data harvesting)
* [ ] No forced continuity without clear notification

## Verification

* [ ] All user flows documented with happy + error paths
* [ ] Accessibility requirements defined and achievable
* [ ] Error handling covers all failure modes with recovery steps
* [ ] Every user action has defined feedback
* [ ] Dark pattern audit passes (all items checked)
* [ ] AI interactions have human-in-the-loop safeguards (if applicable)

## Status

**Status:** pending
**Started:** —
**Completed:** —
