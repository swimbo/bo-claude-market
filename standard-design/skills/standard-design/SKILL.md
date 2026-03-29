---
name: standard-design
description: >
  This skill should be used when building, reviewing, or scaffolding React + MUI admin interfaces
  using the Standard Design System. It applies when the user asks to "apply Standard theme", "review design
  compliance", "scaffold a page", "use Standard colors", "set up dark mode", "create an admin layout",
  or references Standard design tokens, component patterns, or theming. Also applies when working with
  MUI component overrides, ThemeModeProvider, or the Standard color palette.
version: 1.0.0
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "Agent"]
---

# Standard Design System

The Standard Design System is a React 18 + MUI v6 admin UI design system with dual-mode theming (dark/light), 28 MUI component overrides, 3 custom layout components, and 4 page patterns.

## Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| UI Framework | React | 18.x |
| Component Library | MUI (Material-UI) | 6.x |
| CSS-in-JS | Emotion | 11.x |
| Icons | MUI Icons Material | 6.x |
| Data Grid | MUI X Data Grid | 7.x |
| Build Tool | Vite | 6.x |
| Documentation | Storybook | 8.x |
| Language | TypeScript | 5.x |

## Architecture

```
src/
├── theme/
│   ├── index.ts              # Central export
│   ├── colors.ts             # Dark/light color palettes
│   ├── typography.ts         # Font families + scale
│   ├── theme.ts              # MUI theme factory + 28 overrides
│   └── ThemeModeProvider.tsx  # React context for theme switching
├── components/
│   ├── Layout.tsx            # Full admin layout (AppBar + Sidebar + content)
│   ├── Sidebar.tsx           # Navigation drawer with sections
│   └── DataTable.tsx         # Themed MUI DataGrid wrapper
└── stories/                  # Storybook stories (26 total)
```

## Core Principles

1. **Semantic color naming** — Always use palette tokens (`colors.accent`, `colors.steel`), never raw hex values
2. **Theme-aware components** — All components adapt to dark/light mode via `useThemeMode()` hook
3. **Decoupled from routing/auth** — Custom components accept state as props, no hooks for auth or routing
4. **MUI-first** — Extend MUI components via theme overrides, don't rebuild from scratch
5. **Type-safe tokens** — All design tokens exported with TypeScript types

## Theme Modes

### Dark Mode — Industrial/Cyber Aesthetic
- Electric cyan accent (#00d4ff)
- Radial gradient backgrounds
- Glow effects on interactive elements
- Custom scrollbars with accent hover

### Light Mode — Clean/Professional
- Professional blue accent (#0969da)
- White/gray backgrounds, no gradients
- Subtle transparent glows
- Standard RGBA shadows

## Font Families

| Family | Usage | Import |
|--------|-------|--------|
| **Outfit** | Display — headings, buttons, navigation | Google Fonts |
| **DM Sans** | Body — content, descriptions, form text | Google Fonts |
| **JetBrains Mono** | Code — data labels, IDs, timestamps, metrics | Google Fonts |

Google Fonts URL:
```
https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Outfit:wght@400;500;600;700;800&display=swap
```

## Special Effects

| Effect | Where | Implementation |
|--------|-------|---------------|
| Gradient buttons | Primary buttons | `linear-gradient(135deg, accent, accentDim)` |
| Glow hover | Buttons, chips, tabs | `box-shadow: 0 0 20px rgba(accent, 0.3)` |
| Lift effect | Button hover | `transform: translateY(-1px)` |
| Glassmorphism | AppBar | `backdrop-filter: blur(12px)` + transparent bg |
| Pulse animation | Status indicator | `@keyframes pulse` 2s infinite |
| Fade-in content | Main content area | `@keyframes fadeInUp` 0.4s ease-out |
| Top border gradient | Cards | `borderTop: 3px solid` with gradient |
| Active nav indicator | Sidebar items | Left accent bar with glow shadow |

## Component Overrides (28 total)

See `references/component-patterns.md` for the full list with implementation details.

## Custom Components

### Layout
Full admin layout wrapper — fixed AppBar with blur backdrop, theme toggle, notifications, user profile menu, collapsible Sidebar, grid background pattern.

**Props:**
- `children: ReactNode`
- `user?: { name?, email? }`
- `navItems: NavItem[]`
- `activePath?: string`
- `onNavigate?: (path: string) => void`
- `onLogout?: () => void`

### Sidebar
Navigation drawer with sections, icons, active state indicator.

**Props:**
- `navItems: NavItem[]`
- `activePath?: string`
- `onNavigate?: (path: string) => void`
- `title?: string` (default: 'STANDARD')
- `subtitle?: string` (default: 'Command Center')

**NavItem type:** `{ path: string, label: string, icon: ReactNode, section?: string }`

### DataTable
Themed MUI DataGrid wrapper with toolbar, quick filter, custom header styling.

**Props:**
- `rows: GridRowsProp`
- `columns: GridColDef[]`
- `loading?: boolean`
- `pageSize?: number` (default: 10)
- `onRowClick?: (row) => void`
- `toolbar?: boolean` (default: true)

## Page Patterns

4 standard page compositions — see `references/page-patterns.md`:

1. **Dashboard** — Stat cards, progress bars, status summaries, recent activity
2. **List** — DataTable with filters, search, bulk actions
3. **Detail** — Header with actions, tabbed content sections, related data
4. **Form** — Grouped fields, validation states, save/cancel actions

## Reference Files

- **`references/color-tokens.md`** — Complete dark/light color palettes with hex values and usage
- **`references/typography-tokens.md`** — All 11 typography variants with size, weight, family
- **`references/component-patterns.md`** — All 28 MUI component overrides with implementation
- **`references/page-patterns.md`** — 4 page compositions with component structure
