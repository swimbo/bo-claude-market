# Article Publisher

A Claude Code plugin to publish Markdown articles from your local directory to Substack, Reddit, and LinkedIn — with screenshot verification and auto-formatting fixes.

## Features

* **AI writing humanizer**: Detects and removes signs of LLM-generated writing before publishing — banned words, uniform sentence length, formulaic openings, excessive hedging, and more

* **Multi-platform publishing**: Substack → Reddit → LinkedIn in one command

* **Screenshot verification**: Takes screenshots before posting to catch formatting issues

* **Auto-fix formatting**: Detects and fixes obvious formatting problems

* **Smart subreddit discovery**: Automatically finds the best subreddit for your article

* **Publication tracking**: Logs all published URLs in your article file and a central `published.md`

* **Single-platform retry**: Publish to individual platforms with `/article-publisher:publish-to`

## Prerequisites

* Google Chrome with profile `bo.bergstrom@gmail.com`

* Logged into Substack (readbo.substack.com), Reddit (u/bberg2020), and LinkedIn

* Playwright MCP server configured in Claude Code

* Articles as `.md` files in `/Users/bo/code/articles/`

## Commands

### `/article-publisher:publish <filename>`

Full pipeline: reads article → humanizes → publishes to Substack (draft first) → Reddit → LinkedIn.

```
/article-publisher:publish my-article.md
```

### `/article-publisher:humanize <filename>`

Standalone humanizer: analyzes an article for AI writing patterns and rewrites to sound naturally human. Shows a diff for approval.

```
/article-publisher:humanize my-article.md
```

### `/article-publisher:publish-to <platform> <filename>`

Publish to a single platform. Runs the humanizer first for Substack. Useful for retrying or publishing individually.

```
/article-publisher:publish-to substack my-article.md
/article-publisher:publish-to reddit my-article.md
/article-publisher:publish-to linkedin my-article.md --substack-url https://readbo.substack.com/p/my-article
```

## Article Format

Articles should be Markdown files with optional YAML frontmatter:

```markdown
---
title: My Article Title
subtitle: A compelling subtitle
tags: [technology, AI, writing]
section: Essays
---

Article content here...
```

If frontmatter fields are missing, they'll be inferred from the content.

## Publishing Order

1. **Humanize** — Scans for AI writing patterns and rewrites the article body. Shows diff for user approval.
2. **Substack** — Creates draft, verifies formatting via screenshot, publishes. Captures URL.
3. **Reddit** — Finds best subreddit via AI agent, posts summary with Substack link.
4. **LinkedIn** — Posts summary with Substack link and relevant hashtags.

## Components

| Type    | Name                 | Purpose                                        |
| ------- | -------------------- | ---------------------------------------------- |
| Command | `publish`            | Full multi-platform publishing pipeline        |
| Command | `publish-to`         | Single-platform publishing                     |
| Command | `humanize`           | Standalone AI writing pattern removal          |
| Agent   | `humanizer`          | Detects and rewrites AI-sounding prose         |
| Agent   | `subreddit-finder`   | Discovers the best subreddit for an article    |
| Skill   | `article-publishing` | Platform-specific browser automation knowledge |
| Script  | `launch-chrome.sh`   | Launches Chrome with the correct profile       |

## Post-Publishing

After publishing, the plugin:

1. Appends a `## Published` section to the article file with all URLs and the date
2. Updates `/Users/bo/code/articles/published.md` with the entry

## Installation

Add to your Claude Code plugins or use directly:

```bash
claude --plugin-dir /path/to/article-publisher
```