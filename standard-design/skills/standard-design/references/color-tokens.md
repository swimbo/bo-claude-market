# Standard Color Tokens

## ColorPalette Type

```typescript
interface ColorPalette {
  // Base
  void: string;
  abyss: string;
  charcoal: string;
  slate: string;
  steel: string;

  // Text
  textPrimary: string;
  textSecondary: string;
  textMuted: string;

  // Accent
  accent: string;
  accentDim: string;
  accentGlow: string;

  // Status
  success: string;
  successGlow: string;
  warning: string;
  warningGlow: string;
  danger: string;
  dangerGlow: string;
  info: string;

  // Backgrounds
  paper: string;
  default: string;
}
```

## Dark Mode Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `void` | `#0a0c10` | Deepest background, body |
| `abyss` | `#0d1117` | Secondary background |
| `charcoal` | `#161b22` | Card backgrounds, paper |
| `slate` | `#21262d` | Borders, dividers |
| `steel` | `#30363d` | Subtle borders, input borders |
| `textPrimary` | `#e6edf3` | Main text color |
| `textSecondary` | `#8b949e` | Secondary text, descriptions |
| `textMuted` | `#484f58` | Disabled text, placeholders |
| `accent` | `#00d4ff` | Primary accent — electric cyan |
| `accentDim` | `#0099cc` | Darker accent for gradients |
| `accentGlow` | `rgba(0, 212, 255, 0.15)` | Glow effects, hover states |
| `success` | `#3fb950` | Success states |
| `successGlow` | `rgba(63, 185, 80, 0.15)` | Success glow |
| `warning` | `#d29922` | Warning states |
| `warningGlow` | `rgba(210, 153, 34, 0.15)` | Warning glow |
| `danger` | `#f85149` | Error/danger states |
| `dangerGlow` | `rgba(248, 81, 73, 0.15)` | Danger glow |
| `info` | `#58a6ff` | Informational elements |
| `paper` | `#161b22` | Paper/card surfaces |
| `default` | `#0a0c10` | Default background |

## Light Mode Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `void` | `#ffffff` | Deepest background, body |
| `abyss` | `#f6f8fa` | Secondary background |
| `charcoal` | `#ffffff` | Card backgrounds, paper |
| `slate` | `#f0f3f6` | Borders, dividers |
| `steel` | `#d1d9e0` | Subtle borders, input borders |
| `textPrimary` | `#1f2328` | Main text color |
| `textSecondary` | `#59636e` | Secondary text, descriptions |
| `textMuted` | `#8b949e` | Disabled text, placeholders |
| `accent` | `#0969da` | Primary accent — professional blue |
| `accentDim` | `#0550ae` | Darker accent for gradients |
| `accentGlow` | `rgba(9, 105, 218, 0.10)` | Glow effects, hover states |
| `success` | `#1a7f37` | Success states |
| `successGlow` | `rgba(26, 127, 55, 0.10)` | Success glow |
| `warning` | `#9a6700` | Warning states |
| `warningGlow` | `rgba(154, 103, 0, 0.10)` | Warning glow |
| `danger` | `#d1242f` | Error/danger states |
| `dangerGlow` | `rgba(209, 36, 47, 0.10)` | Danger glow |
| `info` | `#0969da` | Informational elements |
| `paper` | `#ffffff` | Paper/card surfaces |
| `default` | `#f6f8fa` | Default background |

## Usage Rules

1. **Never use raw hex values** — always reference tokens via `useColors()` hook or theme palette
2. **Glow tokens** are for `box-shadow` and background overlays only, never for text or borders
3. **Status colors** map to MUI severity: `success`, `warning`, `error` (danger), `info`
4. **Dark mode glows** use 15% opacity; **light mode glows** use 10% opacity
5. **Accent gradient** is always `linear-gradient(135deg, accent, accentDim)`

## Accessing Colors in Components

```typescript
import { useColors } from '../theme';

function MyComponent() {
  const colors = useColors();
  return (
    <Box sx={{ color: colors.textPrimary, bgcolor: colors.charcoal }}>
      Content
    </Box>
  );
}
```

Or via MUI theme:

```typescript
import { useTheme } from '@mui/material';

function MyComponent() {
  const theme = useTheme();
  // Access via theme.palette.primary.main (accent)
  // Access via theme.palette.background.paper (charcoal)
}
```
