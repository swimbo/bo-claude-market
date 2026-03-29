# Standard Page Patterns

4 standard page compositions used across Standard admin interfaces. All pages are rendered inside the `Layout` component wrapper.

---

## 1. Dashboard Page

Overview page with stat cards, progress indicators, status summaries, and recent activity.

### Structure

```tsx
<Layout ...>
  {/* Page Header */}
  <Box sx={{ mb: 4 }}>
    <Typography variant="h1">Dashboard</Typography>
    <Typography variant="body2" color="textSecondary">
      System overview and key metrics
    </Typography>
  </Box>

  {/* Stat Cards Row */}
  <Grid container spacing={3} sx={{ mb: 4 }}>
    <Grid item xs={12} sm={6} md={3}>
      <Card>
        <CardContent>
          <Typography variant="overline" color="textSecondary">Total Users</Typography>
          <Typography variant="h4">12,847</Typography>
          <Chip label="+12.5%" color="success" size="small" />
        </CardContent>
      </Card>
    </Grid>
    {/* Repeat for 3 more stat cards */}
  </Grid>

  {/* Progress Section */}
  <Card sx={{ mb: 3 }}>
    <CardContent>
      <Typography variant="h5" sx={{ mb: 2 }}>System Health</Typography>
      <Box sx={{ mb: 2 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
          <Typography variant="body2">CPU Usage</Typography>
          <Typography variant="overline">67%</Typography>
        </Box>
        <LinearProgress variant="determinate" value={67} />
      </Box>
    </CardContent>
  </Card>

  {/* Recent Activity Table */}
  <Card>
    <CardContent>
      <Typography variant="h5" sx={{ mb: 2 }}>Recent Activity</Typography>
      <DataTable rows={recentActivity} columns={activityColumns} pageSize={5} />
    </CardContent>
  </Card>
</Layout>
```

### Key Conventions
- Stat cards: 4-column grid on desktop, 2 on tablet, 1 on mobile
- Each stat card has: overline label, h4 value, Chip for trend
- Progress bars use `LinearProgress` with overline percentage labels
- Activity tables use `DataTable` with small page size (5)

---

## 2. List Page

Data-heavy page with filters, search, DataTable, and bulk actions.

### Structure

```tsx
<Layout ...>
  {/* Page Header with Actions */}
  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
    <Box>
      <Typography variant="h1">Users</Typography>
      <Typography variant="body2" color="textSecondary">
        Manage user accounts and permissions
      </Typography>
    </Box>
    <Button variant="contained" startIcon={<AddIcon />}>
      Add User
    </Button>
  </Box>

  {/* Filter Bar */}
  <Card sx={{ mb: 3 }}>
    <CardContent sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
      <TextField placeholder="Search users..." size="small" sx={{ flex: 1 }} />
      <Select size="small" value={roleFilter}>
        <MenuItem value="all">All Roles</MenuItem>
        <MenuItem value="admin">Admin</MenuItem>
        <MenuItem value="user">User</MenuItem>
      </Select>
      <Select size="small" value={statusFilter}>
        <MenuItem value="all">All Status</MenuItem>
        <MenuItem value="active">Active</MenuItem>
        <MenuItem value="inactive">Inactive</MenuItem>
      </Select>
    </CardContent>
  </Card>

  {/* Data Table */}
  <Card>
    <DataTable
      rows={users}
      columns={userColumns}
      pageSize={10}
      onRowClick={(row) => navigate(`/users/${row.id}`)}
      toolbar
    />
  </Card>
</Layout>
```

### Key Conventions
- Header row: title + description on left, primary action button on right
- Filter bar in a Card above the data table
- Filters use `size="small"` TextField and Select components
- DataTable inside a Card with toolbar enabled
- Row click navigates to detail page

---

## 3. Detail Page

Single-entity view with header, tabbed sections, and related data.

### Structure

```tsx
<Layout ...>
  {/* Entity Header */}
  <Card sx={{ mb: 3 }}>
    <CardContent sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
      <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
        <Avatar sx={{ width: 56, height: 56, bgcolor: 'primary.main' }}>
          {initials}
        </Avatar>
        <Box>
          <Typography variant="h2">{entity.name}</Typography>
          <Typography variant="body2" color="textSecondary">{entity.email}</Typography>
          <Chip label={entity.status} color={statusColor} size="small" sx={{ mt: 0.5 }} />
        </Box>
      </Box>
      <Box sx={{ display: 'flex', gap: 1 }}>
        <Button variant="outlined" startIcon={<EditIcon />}>Edit</Button>
        <Button variant="outlined" color="error" startIcon={<DeleteIcon />}>Delete</Button>
      </Box>
    </CardContent>
  </Card>

  {/* Tabbed Content */}
  <Tabs value={activeTab} onChange={(_, v) => setActiveTab(v)} sx={{ mb: 3 }}>
    <Tab label="Overview" />
    <Tab label="Activity" />
    <Tab label="Settings" />
  </Tabs>

  {/* Tab Panels */}
  {activeTab === 0 && (
    <Grid container spacing={3}>
      <Grid item xs={12} md={8}>
        <Card>
          <CardContent>
            <Typography variant="h5" sx={{ mb: 2 }}>Details</Typography>
            {/* Detail fields as label/value pairs */}
            <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 2 }}>
              <Box>
                <Typography variant="overline" color="textSecondary">Role</Typography>
                <Typography variant="body1">{entity.role}</Typography>
              </Box>
              {/* More fields */}
            </Box>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={12} md={4}>
        <Card>
          <CardContent>
            <Typography variant="h5" sx={{ mb: 2 }}>Quick Stats</Typography>
            {/* Stat items */}
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  )}
</Layout>
```

### Key Conventions
- Entity header: Avatar + name + metadata + status Chip + action buttons
- Tabs below header for content sections
- Overview tab: 2-column grid (8/4 split) with detail fields and sidebar stats
- Detail fields: overline label above body1 value
- Destructive actions use `color="error"` variant

---

## 4. Form Page

Data entry page with grouped fields, validation, and save/cancel actions.

### Structure

```tsx
<Layout ...>
  {/* Page Header */}
  <Box sx={{ mb: 3 }}>
    <Typography variant="h1">Create User</Typography>
    <Typography variant="body2" color="textSecondary">
      Add a new user account to the system
    </Typography>
  </Box>

  <form onSubmit={handleSubmit}>
    {/* Field Group */}
    <Card sx={{ mb: 3 }}>
      <CardContent>
        <Typography variant="h6" sx={{ mb: 2 }}>Personal Information</Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6}>
            <TextField
              label="First Name"
              fullWidth
              required
              error={!!errors.firstName}
              helperText={errors.firstName}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField label="Last Name" fullWidth required />
          </Grid>
          <Grid item xs={12}>
            <TextField label="Email" type="email" fullWidth required />
          </Grid>
        </Grid>
      </CardContent>
    </Card>

    {/* Another Field Group */}
    <Card sx={{ mb: 3 }}>
      <CardContent>
        <Typography variant="h6" sx={{ mb: 2 }}>Role & Permissions</Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6}>
            <Select label="Role" fullWidth>
              <MenuItem value="admin">Administrator</MenuItem>
              <MenuItem value="user">User</MenuItem>
            </Select>
          </Grid>
          <Grid item xs={12}>
            <FormControlLabel control={<Switch />} label="Enable notifications" />
          </Grid>
        </Grid>
      </CardContent>
    </Card>

    {/* Form Actions */}
    <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 2 }}>
      <Button variant="outlined" onClick={() => navigate(-1)}>Cancel</Button>
      <Button variant="contained" type="submit">Create User</Button>
    </Box>
  </form>
</Layout>
```

### Key Conventions
- Field groups in separate Cards with h6 section titles
- 2-column grid for related fields (first/last name), full width for standalone fields
- Validation: `error` prop + `helperText` on TextFields
- Form actions: cancel (outlined) + submit (contained) at bottom-right
- Toggle options use `Switch` with `FormControlLabel`
- All fields use `fullWidth` prop

---

## Layout Spacing Conventions

| Element | Spacing |
|---------|---------|
| Page header to content | `mb: 3` or `mb: 4` |
| Between Cards | `mb: 3` |
| Card content internal | `mb: 2` between sections |
| Grid item gap | `spacing={2}` or `spacing={3}` |
| Form actions to last card | `mt: 0` (immediately below last card) |
| Stat cards grid | `spacing={3}`, 4-col on md+ |
