---
name: Article Publishing
description: This skill should be used when the user asks to "publish an article", "post to substack", "share on linkedin", "post to reddit", "publish my writing", "cross-post article", "distribute my article", "post to all platforms", or needs to publish Markdown articles to Substack, Reddit, and LinkedIn using browser automation.
version: 0.1.0
---

# Article Publishing

Orchestrate publishing articles from local Markdown files to Substack, Reddit, and LinkedIn using browser automation. Articles live in `/Users/bo/code/articles/` as `.md` files with optional frontmatter.

## Publishing Order

Always follow this sequence:
1. **Humanize** — Run the humanizer agent to detect and remove AI writing patterns from the article body. Show the report and diff to the user for approval.
2. **Substack** — Create draft, verify formatting, publish. Capture the published URL.
3. **Reddit** — Find best subreddit, post summary with Substack link.
4. **LinkedIn** — Post summary with Substack link.

## Article Reading

Read the article Markdown file and extract metadata from frontmatter:

```yaml
---
title: "My Article Title"
subtitle: "A compelling subtitle"
tags: [writing, strategy, content]
section: "Essays"
---
```

- **Title** from `title:` field or first `# heading`
- **Subtitle** from `subtitle:` field, or generate a compelling one from the content
- **Tags** from `tags:` field, or infer 3-5 relevant tags from the content
- **Section** from `section:` field if present
- **Body** content (everything after frontmatter)

## Humanizer Stage

Before publishing to any platform, run the humanizer to clean up AI writing patterns:

1. Dispatch the `article-publisher:humanizer` agent with the article file path
2. The agent analyzes the article against `references/humanizer-guide.md` patterns:
   - Banned words and phrases (delve, tapestry, leverage, etc.)
   - Uniform sentence length (low burstiness)
   - Formulaic openings and closings
   - Missing contractions and overly formal tone
   - Excessive hedging, parallel constructions, signposting
   - Vague claims and false depth
3. The agent rewrites the body to eliminate detected patterns
4. Show the humanizer report (AI-ness score + changes) and `git diff` to the user
5. Get user approval before proceeding to publish

The humanizer preserves: frontmatter, `## Published` sections, core arguments, facts, data, and overall structure. It only modifies prose style.

The humanizer also applies when writing summaries for Reddit and LinkedIn — those summaries should follow the same principles (use contractions, vary sentence length, avoid banned words, take positions rather than hedging).

## Chrome Profile

All browser automation uses Chrome profile `bo.bergstrom@gmail.com`. Launch with:

```bash
bash $CLAUDE_PLUGIN_ROOT/scripts/launch-chrome.sh
```

Wait for Chrome to be ready before navigating.

## Platform Workflows

### Substack (readbo.substack.com)

Load `references/substack-workflow.md` for step-by-step browser automation.

Key points:
- Navigate to `https://readbo.substack.com/publish/post`
- Fill title, subtitle, body content
- Set tags/topics and section
- Save as draft first
- Take screenshot of draft preview to verify formatting
- Fix any obvious formatting issues (broken images, misaligned text, missing line breaks)
- Publish when formatting looks correct
- Capture the published post URL from the browser

### Reddit (u/bberg2020)

Load `references/reddit-workflow.md` for step-by-step browser automation.

Key points:
- Use the subreddit-finder agent to identify the best subreddit
- Navigate to subreddit's submit page
- Create a link post or text post with summary + Substack link
- Auto-select flair if the subreddit requires it
- Take screenshot to verify formatting
- Submit the post
- Capture the Reddit post URL

### LinkedIn

Load `references/linkedin-workflow.md` for step-by-step browser automation.

Key points:
- Navigate to LinkedIn feed
- Create a new post (not a LinkedIn Article)
- Write a compelling summary of the article (2-4 paragraphs)
- Include the Substack link
- Add 3-5 relevant hashtags
- Take screenshot to verify formatting
- Publish the post
- Capture the LinkedIn post URL

## Screenshot Verification

After composing content on each platform, before publishing:
1. Take a screenshot of the preview/draft
2. Analyze the screenshot for formatting issues:
   - Broken or missing images
   - Misaligned text or headings
   - Missing line breaks or spacing
   - Truncated content
   - Broken links
3. If issues found, fix them in the editor and re-screenshot
4. Only publish when formatting is correct

## Post-Publishing

After all platforms are published:

1. **Append URLs to article file** — Add a `## Published` section at the end of the article:
   ```markdown
   ## Published

   - **Substack**: [URL]
   - **Reddit**: [URL] (r/subreddit-name)
   - **LinkedIn**: [URL]
   - **Date**: YYYY-MM-DD
   ```

2. **Update published.md** — Append an entry to `/Users/bo/code/articles/published.md`:
   ```markdown
   ## Article Title
   - **Date**: YYYY-MM-DD
   - **Tags**: tag1, tag2, tag3
   - **Substack**: [URL]
   - **Reddit**: [URL] (r/subreddit-name)
   - **LinkedIn**: [URL]
   ```

## Failure Recovery

If publishing fails on any platform mid-sequence:
1. Record which platforms succeeded and capture their URLs
2. Note the error details from the failed platform
3. Report the status to the user with URLs collected so far
4. Append any successful URLs to the article file immediately (don't wait for all three)
5. The user can retry the failed platform with `/article-publisher:publish-to`

## Summary Writing

When creating summaries for Reddit and LinkedIn:
- Capture the key thesis or argument of the article
- Keep it engaging and readable (2-4 short paragraphs)
- End with a clear call-to-action pointing to the full article on Substack
- For LinkedIn, add relevant hashtags based on article topic
- For Reddit, match the tone and conventions of the target subreddit

## Reference Files

- **`references/humanizer-guide.md`** — Banned words, structural fixes, tone adjustments, and specificity rules for removing AI writing patterns
- **`references/substack-workflow.md`** — Substack editor navigation, draft workflow, common issues
- **`references/reddit-workflow.md`** — Reddit submission, flair selection, subreddit rules
- **`references/linkedin-workflow.md`** — LinkedIn post composition, hashtag strategy, link previews
