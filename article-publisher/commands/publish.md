---
name: publish
description: Publish an article to Substack, Reddit, and LinkedIn with screenshot verification
argument-hint: "<article-filename>"
allowed-tools: ["Read", "Write", "Edit", "Bash", "Glob", "Grep", "Agent", "mcp__playwright__*"]
---

Publish a Markdown article from `/Users/bo/code/articles/` to all three platforms in order: Substack → Reddit → LinkedIn.

The user provides the article filename (e.g., `my-article.md`). If no filename is given, list `.md` files in `/Users/bo/code/articles/` and ask the user to pick one.

## Process

### 1. Read the Article

Read the article from `/Users/bo/code/articles/{filename}`. Extract from frontmatter (or infer from content):

* **Title**: from `title:` field or first `# heading`

* **Subtitle**: from `subtitle:` field, or generate a compelling one

* **Tags**: from `tags:` field, or infer 3-5 relevant tags

* **Section**: from `section:` field if present

* **Body**: everything after frontmatter

### 2. Humanize the Article

Dispatch the `article-publisher:humanizer` agent with the full article file path. The agent analyzes the content for AI writing patterns (overused words, uniform sentence length, formulaic openings, excessive hedging, etc.) and rewrites the body to sound naturally human.

Wait for the agent to finish. Show the user the humanizer report (AI-ness score and changes made). Run `git diff` on the article file so the user can see the diff.

Ask the user to confirm the changes before proceeding. If they want to revert, run `git checkout` on the file and skip to step 3 with the original content.

### 3. Launch Chrome

Run the Chrome launcher script:

```bash
bash $CLAUDE_PLUGIN_ROOT/scripts/launch-chrome.sh
```

### 4. Publish to Substack

Load the `references/substack-workflow.md` from the article-publishing skill for detailed steps.

1. Navigate to `https://readbo.substack.com/publish/post`
2. Fill in title, subtitle, and body content
3. Set tags and section
4. Save as draft
5. Take a screenshot of the draft preview
6. Analyze screenshot for formatting issues — fix any found
7. Publish the post
8. **Capture the Substack URL** — this is needed for Reddit and LinkedIn

Report the Substack URL to the user before continuing.

### 5. Publish to Reddit

Use the `article-publisher:subreddit-finder` agent to find the best subreddit for this article. Pass the article title, tags, and a brief summary.

Load `references/reddit-workflow.md` from the article-publishing skill for detailed steps.

1. Navigate to the recommended subreddit's submit page
2. Create a post with:

   * A compelling title (not identical to the Substack title — adapt for Reddit's audience)

   * A brief summary (2-3 paragraphs) of the article

   * The Substack link
3. Auto-select flair if required
4. Take a screenshot and verify formatting
5. Submit the post
6. **Capture the Reddit post URL**

Report the Reddit URL and subreddit to the user before continuing.

### 6. Publish to LinkedIn

Load `references/linkedin-workflow.md` from the article-publishing skill for detailed steps.

1. Navigate to `https://www.linkedin.com/feed/`
2. Click "Start a post"
3. Write the post:

   * Opening hook (1-2 sentences) — the most compelling insight from the article

   * Body (2-3 short paragraphs) summarizing key points

   * Call-to-action with the Substack link

   * 3-5 relevant hashtags
4. Take a screenshot and verify formatting
5. Publish the post
6. **Capture the LinkedIn post URL**

Report the LinkedIn URL to the user.

### 7. Record Results

After all three platforms are published:

**Append to the article file** — add a `## Published` section:

```markdown

## Published

- **Substack**: {substack_url}
- **Reddit**: {reddit_url} (r/{subreddit_name})
- **LinkedIn**: {linkedin_url}
- **Date**: {today's date YYYY-MM-DD}
```

**Append to** **`/Users/bo/code/articles/published.md`**:

```markdown

## {Article Title}
- **Date**: {today's date YYYY-MM-DD}
- **Tags**: {comma-separated tags}
- **Substack**: {substack_url}
- **Reddit**: {reddit_url} (r/{subreddit_name})
- **LinkedIn**: {linkedin_url}
```

Create `published.md` if it doesn't exist yet.

### 8. Summary

Report a final summary:

* Article title

* All three URLs

* Any issues encountered