---
name: debate
description: "This skill orchestrates multi-agent adversarial debate where domain-expert personas critique and stress-test an implementation plan through structured rounds until consensus emerges. This skill should be used when the user asks to \"debate a plan\", \"stress-test a plan\", \"red team this plan\", \"challenge this plan\", \"poke holes in this plan\", \"devil's advocate review\", \"adversarial review\", \"consensus review\", \"get multiple perspectives on a plan\", \"argue about the best approach\", \"critique this plan\", or \"what could go wrong with this plan\"."
argument-hint: "[path/to/plan.md] — optional, auto-discovers from bo-planner and deep-plan output when omitted"
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash", "Agent"]
---

# Adversarial Consensus Debate

Orchestrate a structured multi-agent debate where domain-expert personas independently critique a plan, then argue their positions until consensus emerges. The output is a battle-tested plan incorporating the strongest arguments from each perspective.

## Workflow Overview

```
Discover Plan → Select Personas → Position Papers (parallel) → Moderator Synthesis → Debate Rounds → Final Consensus
```

## Step 1: Discover the Plan

If a path argument is provided, read that file directly.

If no argument is provided, auto-discover plans by running:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/scripts/find-plans.sh "$(pwd)"
```

If multiple plans are found, present them to the user and ask which to debate. If a single plan is found, confirm it with the user before proceeding. If no plans are found, ask the user to provide a path.

Read the full plan content into context. For multi-file plans (bo-planner phase files, deep-plan sections), read and concatenate all files to form the complete plan.

After resolving the plan, establish these variables for use throughout the workflow:
- **PLAN_PATH**: Absolute path to the primary plan file
- **PLAN_DIRECTORY**: Parent directory of PLAN_PATH (output files are written here)
- **FULL_PLAN_CONTENT**: The complete plan text (concatenated if multi-file)

## Step 2: Analyze Domain & Select Personas

Analyze the plan content to determine relevant domains:

1. Read `${CLAUDE_PLUGIN_ROOT}/skills/debate/references/personas.md`
2. Extract keywords from the plan (section titles, technology mentions, domain terms)
3. Score each domain by keyword matches
4. Apply the complexity heuristic:
   - **Simple** (3 personas): Single-phase, single-domain, <500 words
   - **Medium** (4 personas): Multi-phase OR multi-domain, 500-2000 words
   - **Complex** (5 personas): Multi-phase AND multi-domain, >2000 words
5. Select top personas following the selection algorithm in the personas reference
6. Always include one **contrarian persona** from outside the plan's primary domain

Present the selected personas to the user with a brief rationale for each selection. Include a cost estimate: "This debate will use approximately N agent calls (N persona papers + moderator + up to 3 debate rounds)." Ask for confirmation before proceeding. The user may add, remove, or swap personas.

## Step 3: Generate Position Papers (Parallel)

Spawn one Agent per persona **in parallel** using a single message with multiple Agent tool calls. For each selected persona, look up their Perspective Bias from the personas reference and substitute it into the prompt. Each Agent call uses:

- **subagent_type**: `general-purpose`
- **model**: `opus`
- **prompt**: Constructed from the template below, with placeholders filled per persona:

```
You are a {PERSONA_TITLE} with 15+ years of experience. You have been asked to
review the following implementation plan and provide your expert critique.

## Your Perspective
{PERSONA_PERSPECTIVE_BIAS}

## Your Task
Write a Position Paper (800-1500 words) that:

1. **Executive Assessment**: One paragraph — is this plan sound, risky, or flawed?
2. **Strengths**: What does this plan get right? (3-5 points with reasoning)
3. **Concerns**: What worries you? (3-7 points, ranked by severity)
   - For each concern: state the risk, explain why it matters, suggest an alternative
4. **Missing Considerations**: What has been overlooked from your domain expertise?
5. **Recommended Changes**: Concrete, specific modifications (not vague suggestions)
6. **Hard Stance Items**: 1-3 points you would NOT compromise on — the hills you'd die on

Be specific and opinionated. Reference specific sections of the plan. Avoid generic advice.
Do NOT be polite about real problems — this is adversarial review.

## The Plan
{FULL_PLAN_CONTENT}
```

Wait for all persona agents to complete. Collect all position papers.

## Step 4: Moderator Synthesis (Round 1)

Use the Agent tool to invoke the `debate-moderator` agent (set `subagent_type` to `adversarial-consensus:debate-moderator`). Pass it all position papers:

```
Here are position papers from {N} domain experts reviewing an implementation plan.
Synthesize these into a Disagreement Brief following your standard process.

## Position Papers
{ALL_POSITION_PAPERS}

## Original Plan (for reference)
{FULL_PLAN_CONTENT}
```

The moderator produces a **Disagreement Brief** identifying consensus points, contested decisions, and blind spots.

## Step 5: Debate Rounds (Max 3)

For each round, spawn persona agents **in parallel** again. Each persona receives:

```
You are {PERSONA_TITLE}. You previously reviewed an implementation plan and wrote
a position paper. A moderator has synthesized all position papers and identified
key disagreements.

## Your Previous Position Paper
{THIS_PERSONA_POSITION_PAPER}

## Moderator's Disagreement Brief
{DISAGREEMENT_BRIEF}

## Your Task
Respond to the disagreements that involve your expertise (400-800 words):

1. For each disagreement where you hold a position:
   - **Maintain** your stance with new evidence, OR
   - **Concede** to the opposing position with explanation of what convinced you
2. Address any questions the moderator directed at you specifically
3. Respond to counter-arguments from other personas — engage with their reasoning
4. State clearly: "I concede on X" or "I maintain my position on X because..."

Do NOT hedge or be diplomatic. Take clear positions.
```

After each round, feed responses back to the `debate-moderator` agent (via Agent tool with `subagent_type: adversarial-consensus:debate-moderator`):

```
Round {N} responses from all personas. Update disagreement status.
Determine which disagreements are RESOLVED, MAJORITY, or still CONTESTED.
If all major disagreements are resolved, indicate CONSENSUS_REACHED.
If not, produce targeted questions for the next round.

## Round {N} Responses
{ALL_RESPONSES}
```

**Termination conditions:**
- Moderator indicates `CONSENSUS_REACHED` → proceed to final synthesis
- Round 3 completed → proceed to final synthesis regardless
- All remaining disagreements are LOW impact → proceed to final synthesis

## Step 6: Final Consensus Output

Send the `debate-moderator` agent (via Agent tool) the final synthesis request. Set PLAN_DIRECTORY to the parent directory of PLAN_PATH resolved in Step 1:

```
Produce the final consensus output. Write two files:

1. consensus-plan.md — The revised plan incorporating all resolved decisions
2. debate-transcript.md — Full record of the debate process

## All Debate Material
{POSITION_PAPERS + ALL_ROUND_RESPONSES + DISAGREEMENT_BRIEFS}

## Original Plan
{FULL_PLAN_CONTENT}

Write both files to: {PLAN_DIRECTORY}
```

After the moderator writes the files, present a summary to the user:
- Number of personas, rounds completed
- Key decisions made (resolved items)
- Any unresolved items requiring human decision
- File paths for the consensus plan and transcript

## Error Handling

- If a persona agent fails, continue with remaining personas (minimum 2 required)
- If the moderator agent fails, fall back to manual synthesis: present all position papers to the user
- If plan discovery finds nothing, clearly ask the user for a file path
- If the plan is too short (<100 words), warn the user that debate value may be limited

## Additional Resources

### Reference Files
- **`references/personas.md`** — Full persona catalog with 170 personas across 16 domains, keyword triggers, and selection algorithm

### Scripts
- **`${CLAUDE_PLUGIN_ROOT}/scripts/find-plans.sh`** — Auto-discovers plan files from bo-planner and deep-plan output locations
