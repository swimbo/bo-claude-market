# Standard Design

A Claude Code plugin for building React + MUI admin interfaces using the Standard Design System. Provides design tokens, component patterns, theme configuration, and automated compliance review.

## Features

- **Apply theme** — Install and configure the Standard theme in any React + MUI project
- **Review compliance** — Audit components against Standard design system rules (colors, typography, spacing, effects)
- **Scaffold pages** — Generate dashboard, list, detail, and form pages following Standard layout patterns
- **Design tokens** — Complete color palettes (dark/light), typography scale, spacing, and shadow reference

## Commands

| Command | Description |
|---------|-------------|
| `/standard-design:apply` | Apply Standard theme to an existing React + MUI project |
| `/standard-design:review` | Review components for design system compliance |
| `/standard-design:scaffold` | Scaffold pages and components following Standard patterns |

## Agents

| Agent | Description |
|-------|-------------|
| `design-reviewer` | Reviews code against Standard design system rules — colors, typography, spacing, effects, and component usage |

## Skills

| Skill | Description |
|-------|-------------|
| `standard-design` | Core Standard design system knowledge — tokens, patterns, component overrides, theming architecture |

## Design System Overview

The Standard Design System is a React 18 + MUI v6 admin UI system with:

- **Dual-mode theming** — Dark (industrial/cyber) and Light (clean/professional) modes
- **3 font families** — Outfit (display), DM Sans (body), JetBrains Mono (code/data)
- **28 MUI component overrides** — Buttons, Cards, Dialogs, Tables, AppBar, etc.
- **3 custom components** — Layout, Sidebar, DataTable
- **4 page patterns** — Dashboard, List, Detail, Form
- **Special effects** — Gradient buttons, glow hovers, glassmorphism AppBar, pulse animations

## Installation

```bash
claude plugin install standard-design --marketplace bo-marketplace
```
