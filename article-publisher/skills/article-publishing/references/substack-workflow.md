# Substack Publishing Workflow

Detailed browser automation steps for publishing to readbo.substack.com.

## Prerequisites

* Chrome open with `bo.bergstrom@gmail.com` profile

* Logged into Substack (session should persist)

## Step-by-Step Process

### 1. Navigate to Editor

Navigate to `https://readbo.substack.com/publish/post` to open the Substack post editor.

If redirected to login, the session has expired — flag to the user.

### 2. Set Title

Click the title field (typically a large input at the top of the editor). Type or paste the article title.

### 3. Set Subtitle

Click the subtitle field (below the title). Type or paste the subtitle. If the article has no subtitle in frontmatter, generate a compelling one-line summary.

### 4. Paste Body Content

Click the main body editor area. Paste the article content.

**Formatting considerations:**

* Substack's editor accepts rich text — paste formatted content

* If pasting Markdown directly, it may not render correctly. Consider using the Substack editor's formatting tools

* Headings: Use the editor's heading buttons (H2, H3)

* Bold/Italic: Standard formatting should transfer

* Code blocks: Use the code block formatting option

* Images: If the article references local images, they need to be uploaded separately

* Links: Ensure all links are properly formatted

### 5. Add Tags/Topics

Look for a "Topics" or "Tags" section in the sidebar or settings area.

* Click to add topics

* Type each tag and select from suggestions or create new

* Add 3-5 relevant tags

### 6. Set Section (if applicable)

If the article specifies a section in frontmatter:

* Look for "Section" dropdown in post settings

* Select the appropriate section

### 7. Save as Draft

Before publishing:

* Click "Save draft" or the equivalent button

* Wait for the save confirmation

* The draft URL will be visible in the browser

### 8. Preview and Screenshot

* Click "Preview" or navigate to the draft preview URL

* Take a full-page screenshot

* Analyze for formatting issues:

  * Are headings properly sized?

  * Are paragraphs properly spaced?

  * Are code blocks formatted correctly?

  * Are images loading?

  * Is the overall layout clean?

### 9. Fix Formatting Issues

If issues are found:

* Return to the editor

* Fix the specific issues

* Save draft again

* Take another screenshot to verify

### 10. Publish

When formatting is verified:

* Click the "Publish" button

* Confirm any publication dialogs

* Wait for the post to be published

* The published URL will appear in the browser address bar

### 11. Capture URL

Copy the published post URL from the browser. It will follow the pattern:
`https://readbo.substack.com/p/article-slug`

## Common Issues

### Editor Not Loading

* Refresh the page

* Check if ad blockers are interfering

* Verify Chrome profile is correct

### Formatting Loss

* Try pasting without formatting first, then apply formatting in editor

* Use keyboard shortcuts (Ctrl+B for bold, etc.)

* For code blocks, use the editor's code block tool

### Image Upload

* Substack requires images to be uploaded, not linked

* Drag and drop images into the editor

* Wait for upload confirmation before proceeding

### Draft Not Saving

* Check internet connection

* Try saving again after a brief pause

* Look for error messages in the editor