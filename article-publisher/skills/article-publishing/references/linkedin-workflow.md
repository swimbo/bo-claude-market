# LinkedIn Publishing Workflow

Detailed browser automation steps for posting to LinkedIn.

## Prerequisites

* Chrome open with `bo.bergstrom@gmail.com` profile

* Logged into LinkedIn (session should persist)

## Step-by-Step Process

### 1. Navigate to LinkedIn Feed

Navigate to `https://www.linkedin.com/feed/` to access the main feed.

If redirected to login, the session has expired — flag to the user.

### 2. Open Post Creator

Click the "Start a post" button at the top of the feed. This opens the post composition modal.

Alternative: Navigate directly to `https://www.linkedin.com/feed/?shareActive=true`

### 3. Write Post Content

LinkedIn posts (not Articles) have a 3,000-character limit. Structure the post as:

**Opening hook (1-2 sentences):**

* Start with a compelling statement, question, or insight from the article

* Make it scroll-stopping

**Body (2-3 short paragraphs):**

* Summarize the key points or argument

* Use line breaks between paragraphs for readability

* Include 1-2 specific insights or data points from the article

**Call to action + link:**

* End with a clear CTA: "Read the full article here:"

* Paste the Substack URL on its own line

* LinkedIn will generate a link preview

**Hashtags:**

* Add 3-5 relevant hashtags at the end

* Place each on a new line or space-separated

* Use a mix of broad and niche hashtags

* Example: #Writing #ContentStrategy #Substack #\[TopicSpecific]

### 4. Format the Post

LinkedIn supports limited formatting:

* **Bold**: Use `**text**` or the bold button

* **Italic**: Use `*text*` or the italic button

* **Lists**: Use `-` or `•` characters

* **Line breaks**: Press Enter for new paragraph

* **No headers**: LinkedIn posts don't support headings

Tips:

* Short paragraphs (1-3 sentences each)

* Use line breaks liberally for readability

* Emoji can be used sparingly for visual breaks (optional)

### 5. Verify Link Preview

After pasting the Substack URL:

* LinkedIn should generate a link preview card

* Verify the preview shows:

  * Correct article title

  * Appropriate preview image (if any)

  * Correct domain (readbo.substack.com)

* If preview is missing or incorrect, try removing and re-pasting the URL

### 6. Screenshot and Verify

Take a screenshot of the composed post:

* Check overall formatting and readability

* Verify the link preview is correct

* Ensure hashtags are present

* Confirm the post length is appropriate (not truncated)

### 7. Post

* Click the "Post" button

* Wait for the post to publish

* The post will appear in the feed

### 8. Capture URL

After posting:

* Click on the post timestamp or "..." menu to get the post URL

* The URL follows the pattern: `https://www.linkedin.com/posts/{user-slug}_{post-id}`

* Alternatively, copy from the browser after clicking on the post

## Hashtag Strategy

Select hashtags based on article topic. Common effective hashtags by category:

**Technology:** #Tech #Innovation #AI #MachineLearning #Software #DataScience
**Business:** #Business #Entrepreneurship #Leadership #Strategy #Growth
**Writing:** #Writing #ContentCreation #Blogging #Storytelling #ContentStrategy
**Career:** #Career #ProfessionalDevelopment #Productivity #WorkLife
**Marketing:** #Marketing #DigitalMarketing #ContentMarketing #Branding

Choose 3-5 that are most relevant. Mix one broad hashtag (#Writing) with more specific ones (#ContentStrategy, #SubstackWriters).

## Common Issues

### Post Not Publishing

* Check for content policy violations

* Verify internet connection

* Try refreshing and recomposing

### Link Preview Not Generating

* Wait a few seconds after pasting the URL

* Remove and re-paste the URL

* If still not working, the Substack post may not have proper Open Graph tags

### Character Limit

LinkedIn posts are limited to 3,000 characters. If the summary exceeds this:

* Trim the body paragraphs

* Focus on the most compelling 2-3 points

* Keep the hook and CTA intact

### Modal Closing Unexpectedly

If the post composer closes:

* LinkedIn sometimes auto-saves drafts

* Check for a "Draft" indicator

* Otherwise recompose the post