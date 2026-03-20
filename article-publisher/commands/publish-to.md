---
name: publish-to
description: Publish an article to a single platform (substack, reddit, or linkedin)
argument-hint: "<platform> <article-filename> [--substack-url <url>]"
allowed-tools: ["Read", "Write", "Edit", "Bash", "Glob", "Grep", "Agent", "mcp__playwright__*"]
---

Publish a Markdown article from `/Users/bo/code/articles/` to a single specified platform.

**Arguments:**

* `platform`: One of `substack`, `reddit`, or `linkedin`

* `article-filename`: The `.md` file in `/Users/bo/code/articles/`

* `--substack-url <url>` (optional): Required for reddit and linkedin if the article has already been published to Substack. If not provided and the article file has a `## Published` section, extract the Substack URL from there.

If no filename is given, list `.md` files in `/Users/bo/code/articles/` and ask the user to pick one.

## Process

### 1. Read the Article

Read the article from `/Users/bo/code/articles/{filename}`. Extract metadata (title, subtitle, tags, section, body) from frontmatter or content.

If the article has a `## Published` section, check which platforms have already been published to and extract existing URLs.

### 2. Humanize the Article

If the target platform is `substack` (the primary content platform), dispatch the `article-publisher:humanizer` agent with the full article file path to remove AI writing patterns before publishing.

Wait for the agent to finish. Show the humanizer report and `git diff`. Ask the user to confirm changes before proceeding.

Skip this step for `reddit` and `linkedin` since those platforms get summaries written fresh (not the full article body).

### 3. Launch Chrome

Run the Chrome launcher script:

```bash
bash $CLAUDE_PLUGIN_ROOT/scripts/launch-chrome.sh
```

### 4. Publish to the Specified Platform

#### If `substack`:

Follow the full Substack workflow from the article-publishing skill's `references/substack-workflow.md`.

#### If `reddit`:

* A Substack URL is required. Check:

  1. `--substack-url` argument
  2. `## Published` section in the article file
  3. If neither, ask the user for the Substack URL

* Use the `article-publisher:subreddit-finder` agent to find the best subreddit

* Follow the Reddit workflow from `references/reddit-workflow.md`

#### If `linkedin`:

* A Substack URL is required (same resolution as reddit above)

* Follow the LinkedIn workflow from `references/linkedin-workflow.md`

### 5. Record Results

After publishing:

* If the article already has a `## Published` section, append the new platform URL to it

* If not, create the `## Published` section

* Update `/Users/bo/code/articles/published.md` with the new entry

### 6. Report

Report the published URL and any issues encountered.