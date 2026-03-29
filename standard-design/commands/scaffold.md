---
name: scaffold
description: Scaffold new pages and components following Standard Design System patterns — Dashboard, List, Detail, and Form pages
argument-hint: "<page-type> <entity-name> [--path <output-dir>]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
---

# Scaffold Standard Pages

Generate pages and components following Standard Design System patterns.

**Arguments:**
- `<page-type>`: One of `dashboard`, `list`, `detail`, `form`, or `layout`
- `<entity-name>`: The entity the page is for (e.g., `user`, `project`, `order`)
- `--path <dir>`: Output directory (defaults to `src/pages/`)

If no arguments provided, ask the user what they want to scaffold using AskUserQuestion.

## Page Types

### `dashboard`

Generate a dashboard page with:
- Page header (h1 + description)
- 4 stat cards in a responsive grid (overline label, h4 value, Chip trend)
- System health / progress section with LinearProgress bars
- Recent activity section with DataTable (pageSize: 5)

Read `references/page-patterns.md` — Dashboard section for the exact structure.

File output: `{path}/{entity}Dashboard.tsx`

### `list`

Generate a list page with:
- Page header with primary action button (Add {Entity})
- Filter bar Card with search TextField + 2 Select filters
- DataTable with entity columns, row click navigation, toolbar

Read `references/page-patterns.md` — List section for the exact structure.

Ask the user what columns the entity has. Generate `GridColDef[]` from their response.

File output: `{path}/{entity}List.tsx`

### `detail`

Generate a detail page with:
- Entity header Card (Avatar + name + metadata + status Chip + Edit/Delete buttons)
- Tabs component (Overview, Activity, Settings)
- Overview tab: 2-column grid (8/4) with detail fields (overline labels) and sidebar stats
- Placeholder content for other tabs

Read `references/page-patterns.md` — Detail section for the exact structure.

Ask the user what fields the entity has. Generate detail field sections from their response.

File output: `{path}/{entity}Detail.tsx`

### `form`

Generate a form page with:
- Page header (Create/Edit {Entity})
- Field groups in separate Cards with h6 section titles
- 2-column grid for related fields, full-width for standalone
- Validation error states on required fields
- Cancel (outlined) + Submit (contained) action buttons

Read `references/page-patterns.md` — Form section for the exact structure.

Ask the user what fields the entity has and which are required. Generate form fields from their response.

File output: `{path}/{entity}Form.tsx`

### `layout`

Generate the full Layout setup with:
- Layout component wrapping content
- Navigation items array with icons and sections
- Sample route structure

Ask the user what navigation items they want. Generate the nav items array.

File output: `{path}/AppLayout.tsx`

## Step 1: Validate Theme Exists

Check that the Standard theme is installed in the project:

```
Glob: src/theme/ThemeModeProvider.tsx
```

If not found, warn the user:
```
Standard theme not found in this project. Run /standard-design:apply first to install the theme.
Proceeding anyway — the generated code will reference Standard theme imports.
```

## Step 2: Determine Output Location

If `--path` is provided, use that directory. Otherwise:
- Check if `src/pages/` exists — use it
- Check if `src/app/` exists (Next.js) — use it
- Check if `src/views/` exists — use it
- Default to `src/pages/` and create it

## Step 3: Generate the Page

Read the corresponding section from `references/page-patterns.md` for the exact component structure.

Follow these rules when generating:
1. Import `useColors` from the theme — use tokens for any inline styles
2. Import all MUI components used (Typography, Card, CardContent, Grid, etc.)
3. Import custom Standard components (Layout, DataTable, Sidebar) as needed
4. Use TypeScript with proper typing for props and state
5. Include TODO comments for data fetching placeholders
6. Follow Standard naming: PascalCase components, camelCase variables

## Step 4: Generate Types (if needed)

If the entity has fields, create a types file:

```typescript
// {path}/types/{entity}.ts
export interface {Entity} {
  id: string;
  // ... fields from user input
  createdAt: string;
  updatedAt: string;
}
```

## Step 5: Summary

Present what was generated:
```
Scaffolded {page-type} page for {entity}:
- {path}/{EntityPageType}.tsx
- {path}/types/{entity}.ts (if applicable)

The page uses:
- Layout wrapper with navigation
- Standard color tokens via useColors()
- MUI components with Standard theme overrides
- TypeScript types for {entity}

Next: Wire up data fetching (marked with TODO comments) and add routing.
```

## Important Rules

- Always use Standard theme imports — never raw hex colors or inline font families
- Generated components must be fully typed with TypeScript
- Include prop interfaces for all components
- Use MUI `sx` prop for styling, not inline styles or CSS modules
- Follow the exact page structures from `references/page-patterns.md`
- Do not generate routing configuration — just the page components
- Ask for entity fields before generating list/detail/form pages
