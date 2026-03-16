---
name: manage-profiles
description: List, view, set default, or delete voice profiles used for article writing.
argument-hint: "list | view <name> | set-default <name> | delete <name>"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Manage Profiles

You are managing voice profiles. Parse the user's input to extract:

- **action** (required) — one of: `list`, `view`, `set-default`, `delete`
- **profile name** — required for `view`, `set-default`, and `delete`

The profiles directory is `~/.claude/article-writer/profiles/`. Profile files are markdown with `.md` extension.

## Actions

### list

1. Use Glob to find all `.md` files in `~/.claude/article-writer/profiles/`.
2. For each file found, read the YAML frontmatter to extract `name`, `created`, `updated`, and `sample_count`.
3. Read `~/.claude/article-writer.local.md` to check if a `default_profile` is set.
4. Display results in a table format:

```
Voice Profiles
──────────────────────────────────────────────────
  Name            Created      Samples   Default
  ─────────────   ──────────   ───────   ───────
  technical       2026-01-15   5         *
  casual          2026-02-20   3
  academic        2026-03-01   7
──────────────────────────────────────────────────
```

If no profiles exist, print: "No voice profiles found. Create one with: /analyze-voice <profile-name>"

### view <name>

1. Check if `~/.claude/article-writer/profiles/<name>.md` exists.
2. If it exists, read and display the full profile content.
3. If it does not exist, print: "Profile '<name>' not found. Use '/manage-profiles list' to see available profiles."

### set-default <name>

1. Check if `~/.claude/article-writer/profiles/<name>.md` exists. If not, print an error and list available profiles.
2. Read `~/.claude/article-writer.local.md` (create it if it doesn't exist).
3. If the file contains a `default_profile` line, update it to the new value.
4. If it does not contain a `default_profile` line, add one.
5. The line format should be: `default_profile: <name>`
6. Confirm: "Default voice profile set to '<name>'. All future articles will use this profile unless --voice is specified."

### delete <name>

1. Check if `~/.claude/article-writer/profiles/<name>.md` exists. If not, print an error.
2. Check if this profile is currently set as the default in `~/.claude/article-writer.local.md`.
3. Ask for confirmation: "Are you sure you want to delete the voice profile '<name>'?"
   - If it's the default, add: "This is currently your default profile. The default setting will also be removed."
4. If confirmed:
   - Delete the profile file using Bash `rm`.
   - If it was the default, remove the `default_profile` line from `~/.claude/article-writer.local.md`.
   - Confirm: "Profile '<name>' has been deleted."
5. If not confirmed, abort: "Deletion cancelled."
