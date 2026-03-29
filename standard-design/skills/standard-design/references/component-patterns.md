# Standard Component Patterns

## MUI Component Overrides (28 total)

All overrides are applied via `createStandardTheme(mode)` which returns a complete MUI theme.

### MuiCssBaseline
- Custom scrollbar: 8px wide, `steel` track, `textMuted` thumb, `accent` hover
- Selection: `accent` background with `void` text
- Body: dark mode adds two radial gradient overlays (ellipse at top + circle at center-right)
- Smooth scrolling enabled

### MuiButton
- **Contained primary**: gradient background `linear-gradient(135deg, accent, accentDim)`, white text
- **Hover**: glow shadow `0 0 20px rgba(accent, 0.3)`, lift `translateY(-1px)`
- **Outlined**: `accent` border, `accent` text, `accentGlow` background on hover
- **Text**: `accent` text, `accentGlow` background on hover
- All: `borderRadius: 8px`, no text transform, 600 weight, 0.2s transition

### MuiCard
- Background: `charcoal`
- Border: `1px solid steel`
- Top border: `3px solid accent` (gradient effect)
- Border radius: 12px
- Transition: 0.2s ease on all properties

### MuiChip
- **Default**: `slate` background, `textSecondary` color, `steel` border
- **Success**: `successGlow` background, `success` color, `success` border
- **Warning**: `warningGlow` background, `warning` color, `warning` border
- **Error**: `dangerGlow` background, `danger` color, `danger` border
- **Info/Primary**: `accentGlow` background, `accent` color, `accent` border
- All: border radius 6px, font size 0.75rem, height 24px

### MuiDialog
- Paper: `charcoal` background, `steel` border, border radius 12px
- Backdrop: `rgba(0,0,0,0.7)` (dark), `rgba(0,0,0,0.3)` (light)

### MuiDialogTitle
- Font: Outfit, 600 weight
- Border bottom: `1px solid steel`
- Padding bottom: 16px

### MuiTextField
- Input: `abyss` background, `textPrimary` color
- Border: `steel`, changes to `accent` on focus
- Focus: `accent` border with `accentGlow` box-shadow ring
- Border radius: 8px
- Label: `textSecondary`, `accent` when focused

### MuiSelect
- Same styling as TextField inputs
- Dropdown icon: `textSecondary` color

### MuiMenu
- Paper: `charcoal` background, `steel` border
- Border radius: 8px
- Shadow: elevated

### MuiMenuItem
- Hover: `accentGlow` background, `accent` text
- Selected: slightly stronger `accentGlow` background
- Font size: 0.875rem

### MuiDrawer
- Paper: `abyss` background, no border radius
- Right border: `1px solid steel`
- Width: 260px (constant `DRAWER_WIDTH`)

### MuiAppBar
- Background: transparent with `backdrop-filter: blur(12px)` (glassmorphism)
- Border bottom: `1px solid steel`
- Box shadow: none
- Position: fixed
- Z-index: above drawer

### MuiTabs
- Indicator: `accent` color, 3px height, border radius 3px
- Glow shadow on indicator: `0 0 10px accentGlow`

### MuiTab
- Font: Outfit, 500 weight
- Color: `textSecondary` default, `accent` when selected
- Text transform: none
- Min height: 48px

### MuiLinearProgress
- Background: `slate`
- Bar: `accent` color
- Border radius: 4px
- Height: 6px

### MuiTooltip
- Background: `charcoal` (dark) / `slate` (light)
- Border: `1px solid steel`
- Font size: 0.75rem
- Border radius: 6px
- Shadow: elevated

### MuiIconButton
- Color: `textSecondary`
- Hover: `accent` color, `accentGlow` background
- Transition: 0.2s

### MuiSwitch
- Track: `steel` default, `accent` when checked
- Thumb: `textSecondary` default, white when checked
- Size: slightly larger than MUI default

### MuiPaper
- Background: `charcoal`
- No background image (removes MUI default elevation overlay)

### MuiAlert
- **Success**: `successGlow` background, `success` icon/border
- **Warning**: `warningGlow` background, `warning` icon/border
- **Error**: `dangerGlow` background, `danger` icon/border
- **Info**: `accentGlow` background, `accent` icon/border
- All: left border 4px, border radius 8px

### MuiDivider
- Color: `steel`

### MuiTableCell
- Header: uppercase, `overline` typography (JetBrains Mono), `textSecondary` color
- Body: `textPrimary` color
- Border bottom: `1px solid slate`

---

## Custom Components

### Layout Component

```typescript
import { Layout } from '../components/Layout';
import DashboardIcon from '@mui/icons-material/Dashboard';
import PeopleIcon from '@mui/icons-material/People';

const navItems = [
  { path: '/', label: 'Dashboard', icon: <DashboardIcon />, section: 'Main' },
  { path: '/users', label: 'Users', icon: <PeopleIcon />, section: 'Management' },
];

<Layout
  user={{ name: 'John Doe', email: 'john@example.com' }}
  navItems={navItems}
  activePath={currentPath}
  onNavigate={(path) => router.push(path)}
  onLogout={() => signOut()}
>
  {children}
</Layout>
```

**Internal structure:**
- Fixed `AppBar` with blur backdrop, 64px height
- Theme toggle button (sun/moon icon with rotation animation)
- Notifications `IconButton`
- User avatar with gradient background and initials
- Profile dropdown `Menu` (Profile, Sign out)
- `Sidebar` component (permanent drawer, 260px)
- Main content area with grid background pattern, fade-in animation
- Content padded to account for AppBar height and Sidebar width

### Sidebar Component

```typescript
import { Sidebar, NavItem } from '../components/Sidebar';

const items: NavItem[] = [
  { path: '/', label: 'Dashboard', icon: <DashboardIcon />, section: 'Overview' },
  { path: '/analytics', label: 'Analytics', icon: <AnalyticsIcon />, section: 'Overview' },
  { path: '/users', label: 'Users', icon: <PeopleIcon />, section: 'Management' },
];

<Sidebar
  navItems={items}
  activePath="/"
  onNavigate={handleNavigate}
  title="STANDARD"
  subtitle="Command Center"
/>
```

**Internal structure:**
- Logo area: gradient icon + brand name (Outfit, bold) + subtitle (overline)
- Sections: grouped by `section` field with uppercase headers
- Active state: left `accent` bar (3px) with glow shadow, `accentGlow` background
- Bottom: pulsing status indicator ("System Online")
- Scrollable with custom scrollbar

### DataTable Component

```typescript
import { DataTable } from '../components/DataTable';
import { GridColDef } from '@mui/x-data-grid';

const columns: GridColDef[] = [
  { field: 'id', headerName: 'ID', width: 90 },
  { field: 'name', headerName: 'Name', flex: 1 },
  { field: 'status', headerName: 'Status', width: 120 },
];

<DataTable
  rows={data}
  columns={columns}
  loading={isLoading}
  pageSize={10}
  onRowClick={(row) => navigate(`/users/${row.id}`)}
  toolbar
/>
```

**Internal structure:**
- MUI `DataGrid` wrapped with Standard theming
- Built-in `GridToolbarQuickFilter` when `toolbar` is true
- Custom header: uppercase, monospace font
- Row hover: `accentGlow` background
- Selection: `accent` checkbox
- Top border gradient line (3px)

---

## Compliance Rules

When reviewing components for Standard compliance, check for:

1. **No raw hex colors** — Must use `useColors()` or theme palette tokens
2. **Correct font family per context** — Outfit for headings/buttons, DM Sans for body, JetBrains Mono for data
3. **Proper status color mapping** — success/warning/danger/info via Chip/Alert variants, not custom colors
4. **Border radius consistency** — 8px default, 12px for cards/dialogs, 6px for chips/tooltips
5. **Transition timing** — Always 0.2s ease, never instant or long transitions
6. **Glow effects on hover** — Interactive elements should have `accentGlow` box-shadow on hover
7. **No text transform on buttons** — `textTransform: 'none'` is enforced
8. **AppBar glassmorphism** — Must use `backdrop-filter: blur(12px)`, never opaque
9. **Table headers** — Must use uppercase overline typography
10. **Grid background** — Main content area should have the 40px grid pattern overlay
