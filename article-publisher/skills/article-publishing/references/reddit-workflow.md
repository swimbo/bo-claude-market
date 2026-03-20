# Reddit Publishing Workflow

Detailed browser automation steps for posting to Reddit as u/bberg2020.

## Prerequisites

* Chrome open with `bo.bergstrom@gmail.com` profile

* Logged into Reddit as u/bberg2020 (session should persist)

## Step-by-Step Process

### 1. Determine Target Subreddit

Use the subreddit-finder agent to analyze the article and identify the best subreddit. The agent will return a recommended subreddit name.

### 2. Navigate to Subreddit Submit Page

Navigate to `https://www.reddit.com/r/{subreddit}/submit` to open the submission form.

If the subreddit uses new Reddit, the URL may be:
`https://www.reddit.com/r/{subreddit}/submit`

### 3. Select Post Type

Reddit offers multiple post types. For article sharing, prefer:

* **Link Post** — If the subreddit allows link posts (most common for article sharing)

* **Text Post** — If the subreddit restricts to text-only posts

Check the submission form tabs for available options.

### 4. Fill Post Title

Create a compelling title that:

* Summarizes the article's key point

* Follows the subreddit's title conventions (check sidebar rules)

* Is not clickbaity or misleading

* Is under 300 characters

### 5. Fill Post Content

**For Link Posts:**

* Paste the Substack URL in the URL field

* The title is the main content

**For Text Posts:**

* Write a 2-3 paragraph summary of the article

* Include the key takeaway or thesis

* End with: "Full article: \[Substack URL]"

* Use Reddit Markdown formatting (not HTML)

### 6. Select Flair (if required)

Many subreddits require post flair:

* Look for a "Flair" dropdown or button

* Browse available options

* Select the most appropriate flair for the article topic

* If unsure, choose a general category like "Discussion", "Article", or "Resource"

* Some subreddits won't let you post without flair — always check

### 7. Review Subreddit Rules

Before posting, verify the post complies with subreddit rules:

* Check sidebar rules (usually visible on submit page)

* Verify self-promotion policies

* Ensure post type is allowed

* Check minimum account age/karma requirements

### 8. Screenshot and Verify

Take a screenshot of the filled submission form:

* Verify title is clear and appropriate

* Check content formatting

* Confirm flair is set (if required)

* Ensure the Substack link is correct

### 9. Submit Post

* Click the "Post" or "Submit" button

* Wait for the post to appear

* If an error occurs (e.g., rate limit), wait and retry

### 10. Capture URL

Copy the post URL from the browser. It follows the pattern:
`https://www.reddit.com/r/{subreddit}/comments/{id}/{slug}/`

## Common Issues

### Rate Limiting

Reddit has rate limits for new posts. If rate-limited:

* Wait the specified time before retrying

* Flag to user if the wait is significant

### Flair Required Error

If the subreddit requires flair but none was selected:

* Return to the submission form

* Select appropriate flair

* Resubmit

### Subreddit Restrictions

Some subreddits have:

* Minimum karma requirements

* Approved poster lists

* Restrictions on link posts

* Restrictions on self-promotion

If blocked, suggest an alternative subreddit to the user.

### New vs Old Reddit

The submission form differs between new and old Reddit:

* New Reddit: More graphical, tab-based interface

* Old Reddit: Simpler form-based interface

* Prefer new Reddit for consistency

## Reddit Markdown Quick Reference

```
**bold text**
*italic text*
[link text](url)
> blockquote
- bullet point
1. numbered list
`inline code`

    code block (4 spaces indent)
```