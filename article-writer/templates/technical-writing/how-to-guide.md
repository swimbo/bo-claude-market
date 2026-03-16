---
name: "How-To Guide Template"
description: "A step-by-step instructional guide for completing a specific task"
category: "technical-writing"
estimated_length: 1200
difficulty_level: "intermediate"
tags: ["how-to", "tutorials", "education"]
variables:
  - name: "task"
    type: "text"
    description: "The specific task or goal the reader will accomplish"
  - name: "difficulty"
    type: "select"
    description: "The difficulty level of the task being taught"
  - name: "time_required"
    type: "text"
    description: "Estimated time to complete the task"
  - name: "tools_needed"
    type: "textarea"
    description: "Tools, software, or materials required to complete the task"
---

## Prerequisites

**Purpose**: Ensure the reader has everything they need before starting
**Target length**: ~150 words

List all prerequisites clearly so the reader can verify readiness before beginning. Include:

- Required tools, software, or materials.
- Prior knowledge or skills assumed.
- Environment setup or configuration needed.
- Any accounts, subscriptions, or access permissions required.

Use a checklist format where possible. If a prerequisite has its own setup process, link to a separate guide rather than explaining it here. State the estimated time to complete the full guide so the reader can plan accordingly.

## Step-by-Step Instructions

**Purpose**: Walk the reader through the task with clear, sequential steps
**Target length**: ~800 words

Number each step and keep them atomic — one action per step. For each step:

1. State the action clearly and directly (use imperative mood: "Click," "Enter," "Navigate to").
2. Explain what happens after the action is taken — what should the reader see or expect?
3. Include screenshots, code snippets, or examples where they add clarity.
4. Note any variations based on operating system, version, or configuration.

Use callout boxes or bold text for warnings and important notes. If a step has sub-steps, use lettered sub-lists (a, b, c). Include verification checkpoints every 3-5 steps so the reader can confirm they are on track. Avoid jargon unless you have defined it in the prerequisites section.

## Troubleshooting

**Purpose**: Address common problems and their solutions
**Target length**: ~150 words

List 3-5 common issues readers may encounter, formatted as problem/solution pairs:

- **Problem**: Describe the symptom or error the reader sees.
- **Cause**: Briefly explain why this happens.
- **Solution**: Provide the fix in 1-3 clear steps.

Focus on the issues that are most frequently reported or most likely to block progress. If a problem requires more extensive debugging, link to additional resources or support channels.

## Conclusion

**Purpose**: Confirm success and point to next steps
**Target length**: ~100 words

Congratulate the reader on completing the task. Summarize what they have accomplished and the result they should see. Suggest logical next steps — advanced configurations, related guides, or ways to extend what they have built. Include a link to community forums, documentation, or support for readers who need further help.
