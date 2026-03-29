---
name: apply
description: Apply the Standard Design System theme to an existing React + MUI project — installs dependencies, creates theme files, and configures the provider
argument-hint: "[project-path]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
---

# Apply Standard Theme

Install and configure the Standard Design System in an existing React + MUI project.

**The argument is the project path** (defaults to current directory if omitted).

## Step 1: Verify Project

Check the project has the required foundation:

1. Find `package.json` — confirm it exists
2. Check for React (`react` in dependencies)
3. Check for MUI (`@mui/material` in dependencies)

If React is missing, ask the user if they want to proceed (Standard requires React 18+).

If MUI is missing, tell the user you'll install it. Run:
```bash
npm install @mui/material @emotion/react @emotion/styled @mui/icons-material @mui/x-data-grid
```

## Step 2: Install Google Fonts

Find the project's HTML entry point. Check for:
- `index.html` (Vite, CRA)
- `app/layout.tsx` or `app/layout.js` (Next.js App Router)
- `pages/_document.tsx` or `pages/_document.js` (Next.js Pages Router)

Add the Google Fonts link to the `<head>`:
```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
```

For Next.js projects, prefer `next/font/google` instead:
```typescript
import { Outfit, DM_Sans, JetBrains_Mono } from 'next/font/google';

const outfit = Outfit({ subsets: ['latin'], variable: '--font-outfit' });
const dmSans = DM_Sans({ subsets: ['latin'], variable: '--font-dm-sans' });
const jetbrainsMono = JetBrains_Mono({ subsets: ['latin'], variable: '--font-jetbrains-mono' });
```

## Step 3: Create Theme Files

Create the following files under `src/theme/` (or the project's source directory):

### 3a. `src/theme/colors.ts`

Read `references/color-tokens.md` from this skill for the complete dark and light color palettes. Create the file with:
- `ColorPalette` interface
- `darkColors` object with all dark mode tokens
- `lightColors` object with all light mode tokens

### 3b. `src/theme/typography.ts`

Read `references/typography-tokens.md` from this skill for the full typography scale. Create the file with:
- `FONT_URL` constant (Google Fonts URL)
- `typography` object with all 11 MUI variants configured

### 3c. `src/theme/theme.ts`

Read `references/component-patterns.md` from this skill for all 28 MUI component overrides. Create the file with:
- `createStandardTheme(mode: 'dark' | 'light')` factory function
- All 28 component overrides using color tokens
- Custom shadows array (25 levels)
- Shape configuration (borderRadius: 8)
- Export `darkTheme` and `lightTheme`

### 3d. `src/theme/ThemeModeProvider.tsx`

Create a React context provider that:
- Manages dark/light mode state
- Persists preference to `localStorage` key `standard-theme-mode`
- Detects system preference via `prefers-color-scheme`
- Provides `useThemeMode()` hook returning `{ mode, toggleTheme, setMode, colors }`
- Provides `useColors()` hook returning current color palette
- Wraps children in MUI `ThemeProvider` + `CssBaseline`
- Sets `data-theme` attribute on `document.documentElement`
- Accepts optional `initialMode` prop to override

### 3e. `src/theme/index.ts`

Central export file:
```typescript
export { darkColors, lightColors } from './colors';
export type { ColorPalette } from './colors';
export { typography, FONT_URL } from './typography';
export { darkTheme, lightTheme, createStandardTheme } from './theme';
export { ThemeModeProvider, useThemeMode, useColors } from './ThemeModeProvider';
```

## Step 4: Create Custom Components

Create the 3 custom Standard components. Read `references/component-patterns.md` for full implementation details.

### 4a. `src/components/Layout.tsx`
Full admin layout with AppBar (glassmorphism), theme toggle, user menu, Sidebar, and grid background.

### 4b. `src/components/Sidebar.tsx`
Navigation drawer with sections, active state indicator, and status badge.

### 4c. `src/components/DataTable.tsx`
Themed MUI DataGrid wrapper with toolbar and quick filter.

## Step 5: Wire Up Provider

Find the app's root component (e.g., `App.tsx`, `main.tsx`, `app/layout.tsx`) and wrap it with `ThemeModeProvider`:

```typescript
import { ThemeModeProvider } from './theme';

function App() {
  return (
    <ThemeModeProvider>
      {/* existing app content */}
    </ThemeModeProvider>
  );
}
```

## Step 6: Summary

Present a summary to the user:
```
Standard Design System applied successfully!

Files created:
- src/theme/colors.ts (dark + light color palettes)
- src/theme/typography.ts (font families + 11 variants)
- src/theme/theme.ts (MUI theme factory + 28 overrides)
- src/theme/ThemeModeProvider.tsx (theme context + hooks)
- src/theme/index.ts (central exports)
- src/components/Layout.tsx (admin layout)
- src/components/Sidebar.tsx (navigation drawer)
- src/components/DataTable.tsx (themed data grid)

Next steps:
1. Wrap your app root with <ThemeModeProvider>
2. Use <Layout> for admin pages
3. Access colors via useColors() hook
4. Run `npm run dev` to see the theme in action
```

## Important Rules

- Do not overwrite existing theme files without asking the user first
- If the project already has MUI theme configuration, ask if they want to merge or replace
- Always use the exact color values from the reference files — don't approximate
- For Next.js projects, adapt file paths to the project structure (app/ vs pages/ vs src/)
- Detect the package manager (npm, yarn, pnpm) from lock files and use accordingly
