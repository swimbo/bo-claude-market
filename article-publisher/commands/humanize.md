---
name: humanize
description: Remove signs of AI-generated writing from an article
argument-hint: "<article-filename>"
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Agent"]
---

Humanize a Markdown article from `/Users/bo/code/articles/` by detecting and removing signs of AI-generated writing.

The user provides the article filename (e.g., `my-article.md`). If no filename is given, list `.md` files in `/Users/bo/code/articles/` and ask the user to pick one.

## Process

### 1. Read the Article

Read the article from `/Users/bo/code/articles/{filename}`.

### 2. Run the Humanizer

Dispatch the `article-publisher:humanizer` agent with the article file path. The agent will:

1. Analyze the article for AI writing patterns
2. Rewrite the body to eliminate those patterns
3. Save the updated article
4. Report what changed

### 3. Show the Diff

After the humanizer agent finishes, run `git diff` on the article file to show the user exactly what changed.

### 4. Ask for Approval

Ask the user to review the changes. If they want to revert, run `git checkout` on the file. If they want further adjustments, take their feedback and make targeted edits.
