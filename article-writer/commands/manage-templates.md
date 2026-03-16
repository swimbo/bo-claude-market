---
name: manage-templates
description: List, view, edit, or delete article templates used for structuring articles.
argument-hint: "list | view <name> | edit <name> | delete <name>"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Manage Templates

You are managing article templates. Parse the user's input to extract:

- **action** (required) — one of: `list`, `view`, `edit`, `delete`
- **template name** — required for `view`, `edit`, and `delete`

Templates are stored in two locations:
- **Built-in templates**: `${CLAUDE_PLUGIN_ROOT}/templates/` (read-only, organized by category subfolders)
- **User-created templates**: `~/.claude/article-writer/templates/`

## Actions

### list

1. Use Glob to find all `.md` files in `${CLAUDE_PLUGIN_ROOT}/templates/` recursively.
2. Use Glob to find all `.md` files in `~/.claude/article-writer/templates/`.
3. For each template found, read the YAML frontmatter to extract `name`, `description`, `category`, `estimated_length`, and `difficulty_level`.
4. Group templates by category and display:

```
Article Templates
══════════════════════════════════════════════════════════════

  Technical
  ────────────────────────────────────────────────────────────
  [built-in]  deep-dive        Technical deep-dive analysis    ~2500 words
  [user]      api-tutorial     Step-by-step API tutorial        ~1500 words

  Opinion
  ────────────────────────────────────────────────────────────
  [built-in]  hot-take         Short-form opinion piece         ~800 words
  [user]      editorial        Long-form editorial              ~2000 words

══════════════════════════════════════════════════════════════
```

If no templates exist in either location, print: "No templates found. Create one with: /create-template <template-name>"

### view <name>

1. Search for the template by name in both locations (user-created first, then built-in).
2. If found, read and display the full template content.
3. If found in built-in templates, note: "(built-in template — read-only)"
4. If not found, print: "Template '<name>' not found. Use '/manage-templates list' to see available templates."

### edit <name>

1. Search for the template in `~/.claude/article-writer/templates/` only.
2. If not found there, check if it exists in `${CLAUDE_PLUGIN_ROOT}/templates/`.
   - If found in built-in: "Template '<name>' is a built-in template and cannot be edited directly. Would you like to create a user copy that you can edit?"
     - If yes, copy it to `~/.claude/article-writer/templates/<name>.md` and proceed to edit.
     - If no, abort.
   - If not found anywhere: "Template '<name>' not found."
3. Read and display the current template content.
4. Ask the user what changes they want to make.
5. Apply the changes and write the updated file.
6. Display the updated template for confirmation.

### delete <name>

1. Search for the template in `~/.claude/article-writer/templates/` only.
2. If not found there, check if it exists in `${CLAUDE_PLUGIN_ROOT}/templates/`.
   - If found in built-in: "Template '<name>' is a built-in template and cannot be deleted."
   - If not found anywhere: "Template '<name>' not found."
3. Ask for confirmation: "Are you sure you want to delete the template '<name>'? This cannot be undone."
4. If confirmed:
   - Delete the template file using Bash `rm`.
   - Confirm: "Template '<name>' has been deleted."
5. If not confirmed: "Deletion cancelled."
