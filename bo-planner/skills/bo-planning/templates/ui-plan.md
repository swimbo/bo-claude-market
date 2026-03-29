# UI Plan: \[Feature/Project Name]

## Objective

\[What visual design problem this plan addresses]

## Design System

### Standard Design System Integration

<!-- If the project uses the Standard Design System (React + MUI), the tokens below are pre-filled.
     Run `/standard-design:apply` to install the theme, or `/standard-design:review` to check compliance.
     If NOT using Standard Design, replace these with your project's brand tokens. -->

**Design system in use:** Standard Design System / Custom (choose one)

If using Standard Design System, the following tokens are pre-defined and should NOT be overridden:
- Fonts: Outfit (display), DM Sans (body), JetBrains Mono (code)
- Dark accent: #00d4ff (electric cyan) / Light accent: #0969da (professional blue)
- 28 MUI component overrides applied via theme
- See `/standard-design` skill for full token reference

### Brand Alignment

<!-- If aligning to a specific brand or overriding Standard Design defaults, map tokens here -->

| Role | Hex | Usage |
| ---- | --- | ----- |
| Primary | \[#hex or Standard: textPrimary] | Primary text, high-contrast backgrounds |
| Surface | \[#hex or Standard: charcoal] | Page/container backgrounds |
| Accent | \[#hex or Standard: accent] | Interactive elements, CTAs |
| Secondary Accent | \[#hex or Standard: accentDim] | Informational highlights |
| Muted | \[#hex or Standard: textMuted] | Borders, disabled states, secondary text |
| Success | \[#hex or Standard: success] | Success states, confirmations |
| Warning | \[#hex or Standard: warning] | Warnings, caution states |
| Destructive | \[#hex or Standard: danger] | Errors, destructive actions |

### Color Contrast Verification

| Pairing | Ratio | WCAG AA | WCAG AAA |
| ------- | ----- | ------- | -------- |
| Primary text on Surface | \[ratio]:1 | Pass/Fail | Pass/Fail |
| Accent on Surface | \[ratio]:1 | Pass/Fail | Pass/Fail |
| Muted text on Surface | \[ratio]:1 | Pass/Fail | Pass/Fail |

Minimum requirements: 4.5:1 for body text, 3:1 for large text (18pt+ or 14pt bold).

## Typography

### Scale

<!-- Limit to 2-3 font families. If using Standard Design, these are pre-defined. -->

| Role | Font | Size | Weight | Usage |
| ---- | ---- | ---- | ------ | ----- |
| Display | \[Font or Outfit] | \[size or 2.25rem] | \[weight or 700] | Hero text, large numbers |
| Heading | \[Font or Outfit] | \[size or 1.75rem] | \[weight or 600] | Section headers |
| Subheading | \[Font or Outfit] | \[size or 1.25rem] | \[weight or 600] | Subsection headers |
| Body | \[Font or DM Sans] | \[size or 0.9375rem] | \[weight or 400] | Primary content |
| Label | \[Font or DM Sans] | \[size or 0.75rem] | \[weight or 400] | Form labels, captions |
| Code | \[Monospace or JetBrains Mono] | \[size or 0.6875rem] | \[weight or 500] | Code blocks, data labels |

### Monospaced Adjustments (if applicable)

* Large headings (20px+): Tighten letter-spacing to prevent visual looseness
* Small body (12px-): Slightly increase letter-spacing for character separation
* Limit size variation — extreme size jumps feel unnatural in monospaced contexts

### Font Fallbacks

| Primary | Fallback |
| ------- | -------- |
| \[Primary sans] | Arial, Helvetica, sans-serif |
| \[Primary serif] | Georgia, Times New Roman, serif |
| \[Primary mono] | Consolas, Monaco, monospace |

## Layout & Spacing

### Grid System

* Base unit: 8px
* Spacing scale: 4, 8, 12, 16, 24, 32, 48, 64
* Max content width: \[value]
* Column system: \[columns and gutters]

### Responsive Breakpoints

| Breakpoint | Width | Layout Adjustments |
| ---------- | ----- | ------------------ |
| Mobile | < 640px | \[changes] |
| Tablet | 640-1024px | \[changes] |
| Desktop | > 1024px | \[changes] |

## Component Inventory

### Interactive Components

| Component | States | Visual Spec |
| --------- | ------ | ----------- |
| Primary Button | Default, Hover, Active, Disabled, Focus | \[border-radius, padding, colors per state] |
| Secondary Button | Default, Hover, Active, Disabled, Focus | \[specs] |
| Text Input | Default, Focus, Error, Disabled | \[specs] |
| Dropdown | Closed, Open, Item Hover, Disabled | \[specs] |

### Consistency Rules

* All buttons: same border-radius, same padding scale
* All inputs: same height, same border treatment
* All focus states: consistent outline style (e.g., 2px solid accent)
* All disabled states: same opacity or muted treatment

## Layout Architecture

### Container Map

<!-- Where content lives in the target environment -->

| Container | Content | Constraints |
| --------- | ------- | ----------- |
| \[Container name] | \[What goes here] | \[Size limits, scrolling, resize behavior] |

### IDE Integration (if applicable)

| VS Code Container | Usage | Constraints |
| ------------------ | ----- | ----------- |
| Activity Bar | Navigation icon | Outline-style, match native aesthetic |
| Sidebar | \[View type] | Match File Explorer spacing/indentation |
| Editor | \[Custom editor?] | Respect theme tokens, tab lifecycle |
| Panel | \[Output/data] | Horizontal reflow, collapsible |
| Status Bar | \[Status text] | Terse text, no custom colors unless critical |

### CLI/TUI Composition (if applicable)

* Borders: \[Box-drawing style — rounded, double, single, none]
* Color strategy: ANSI 16 / ANSI 256 / True Color / Monochrome
* Visual hierarchy: Bold, dim, reverse video, color
* Layout: \[How information is spatially organized in the terminal grid]

## Visual Hierarchy

```
[Sketch the Z-pattern or F-pattern reading order]

┌─────────────────────────────┐
│  [Highest visual weight]     │
├─────────────────────────────┤
│  [Secondary content area]    │
│                              │
│  [Supporting content]        │
├─────────────────────────────┤
│  [Actions / footer]          │
└─────────────────────────────┘
```

## Whitespace Strategy

* Use whitespace as an active structural element, not empty filler
* Group related elements with tight spacing (8-12px)
* Separate distinct sections with generous spacing (24-48px)
* Isolate primary CTAs with surrounding whitespace to increase salience

## Anti-Pattern Checklist

<!-- Verify NONE of these exist in the design -->

* [ ] No visual clutter — every element has clear purpose
* [ ] No inconsistent components — buttons, inputs, colors are uniform
* [ ] No low-contrast text — all pairings meet WCAG minimums
* [ ] No color-only meaning — redundant indicators for all states
* [ ] No truncated/clipped content at any viewport size
* [ ] No more than 2-3 typefaces on any single screen
* [ ] No arbitrary decoration — Rams' "as little design as possible"
* [ ] No Frankenstein layouts — all components from same design system
* [ ] No hardcoded colors in IDE extensions (use theme tokens)
* [ ] No Webviews where native IDE components suffice

## Verification

* [ ] Color palette defined with semantic roles
* [ ] All text pairings meet WCAG AA contrast minimums
* [ ] Typography scale defined with fallbacks
* [ ] Spacing follows consistent grid system
* [ ] All interactive components have defined states (default, hover, active, disabled, focus)
* [ ] Layout adapts to target environment constraints
* [ ] Anti-pattern checklist passes (all items checked)
* [ ] Visual hierarchy guides eye to primary content first

## Status

**Status:** pending
**Started:** —
**Completed:** —
