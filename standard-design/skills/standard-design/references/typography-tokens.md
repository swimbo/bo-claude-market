# Standard Typography Tokens

## Font Families

```typescript
const FONT_FAMILIES = {
  display: '"Outfit", sans-serif',    // Headings, buttons, navigation
  body: '"DM Sans", sans-serif',      // Content, descriptions, form text
  mono: '"JetBrains Mono", monospace', // Data labels, IDs, timestamps, metrics, code
};
```

## Google Fonts URL

```
https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Outfit:wght@400;500;600;700;800&display=swap
```

Include this in your HTML `<head>` or load via `@import` in CSS.

## Typography Scale

| Variant | Font Family | Size | Weight | Line Height | Letter Spacing | Usage |
|---------|------------|------|--------|-------------|----------------|-------|
| `h1` | Outfit | 2.25rem (36px) | 700 | 1.2 | -0.02em | Main page headings |
| `h2` | Outfit | 1.75rem (28px) | 600 | 1.3 | -0.01em | Section headings |
| `h3` | Outfit | 1.25rem (20px) | 600 | 1.4 | 0 | Subsection headings |
| `h4` | Outfit | 1.5rem (24px) | 700 | 1.3 | -0.01em | Card titles |
| `h5` | Outfit | 1.125rem (18px) | 600 | 1.4 | 0 | Panel headings |
| `h6` | Outfit | 1rem (16px) | 600 | 1.5 | 0 | Form section labels |
| `body1` | DM Sans | 0.9375rem (15px) | 400 | 1.6 | 0 | Primary body text |
| `body2` | DM Sans | 0.875rem (14px) | 400 | 1.5 | 0 | Secondary body text |
| `button` | Outfit | inherit | 600 | inherit | 0.02em | Button labels |
| `caption` | DM Sans | 0.75rem (12px) | 400 | 1.5 | 0.01em | Small labels, metadata |
| `overline` | JetBrains Mono | 0.6875rem (11px) | 500 | 1.5 | 0.08em | Data labels, section headers, uppercase text |

## MUI Typography Configuration

```typescript
const typography = {
  fontFamily: '"DM Sans", sans-serif', // Default body font
  h1: {
    fontFamily: '"Outfit", sans-serif',
    fontSize: '2.25rem',
    fontWeight: 700,
    lineHeight: 1.2,
    letterSpacing: '-0.02em',
  },
  h2: {
    fontFamily: '"Outfit", sans-serif',
    fontSize: '1.75rem',
    fontWeight: 600,
    lineHeight: 1.3,
    letterSpacing: '-0.01em',
  },
  h3: {
    fontFamily: '"Outfit", sans-serif',
    fontSize: '1.25rem',
    fontWeight: 600,
    lineHeight: 1.4,
  },
  h4: {
    fontFamily: '"Outfit", sans-serif',
    fontSize: '1.5rem',
    fontWeight: 700,
    lineHeight: 1.3,
    letterSpacing: '-0.01em',
  },
  h5: {
    fontFamily: '"Outfit", sans-serif',
    fontSize: '1.125rem',
    fontWeight: 600,
    lineHeight: 1.4,
  },
  h6: {
    fontFamily: '"Outfit", sans-serif',
    fontSize: '1rem',
    fontWeight: 600,
    lineHeight: 1.5,
  },
  body1: {
    fontFamily: '"DM Sans", sans-serif',
    fontSize: '0.9375rem',
    fontWeight: 400,
    lineHeight: 1.6,
  },
  body2: {
    fontFamily: '"DM Sans", sans-serif',
    fontSize: '0.875rem',
    fontWeight: 400,
    lineHeight: 1.5,
  },
  button: {
    fontFamily: '"Outfit", sans-serif',
    fontWeight: 600,
    letterSpacing: '0.02em',
    textTransform: 'none' as const,
  },
  caption: {
    fontFamily: '"DM Sans", sans-serif',
    fontSize: '0.75rem',
    fontWeight: 400,
    lineHeight: 1.5,
    letterSpacing: '0.01em',
  },
  overline: {
    fontFamily: '"JetBrains Mono", monospace',
    fontSize: '0.6875rem',
    fontWeight: 500,
    lineHeight: 1.5,
    letterSpacing: '0.08em',
    textTransform: 'uppercase' as const,
  },
};
```

## Usage Rules

1. **Headings** always use Outfit — never DM Sans or JetBrains Mono for headings
2. **Body text** always uses DM Sans — never Outfit for paragraph content
3. **Data/metrics** use JetBrains Mono via the `overline` variant — timestamps, IDs, status codes, KPIs
4. **Buttons** use Outfit with `textTransform: 'none'` — never uppercase buttons
5. **Table headers** use uppercase + monospace via overline styling
6. **Font weights**: 400 (regular), 500 (medium), 600 (semibold), 700 (bold) — no 300 or 800 in body
