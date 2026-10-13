---
name: debate
description: "This skill orchestrates research-backed multi-agent adversarial debate where domain-expert personas gather current evidence, critique and stress-test an implementation plan, then recommend a solution through structured rounds until consensus emerges. This skill should be used when the user asks to \"debate a plan\", \"stress-test a plan\", \"red team this plan\", \"challenge this plan\", \"poke holes in this plan\", \"devil's advocate review\", \"adversarial review\", \"consensus review\", \"get multiple perspectives on a plan\", \"argue about the best approach\", \"critique this plan\", \"recommend a solution\", or \"what could go wrong with this plan\"."
argument-hint: "[path/to/plan.md] — optional, auto-discovers from bo-planner and deep-plan output when omitted"
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash", "Agent", "WebSearch", "WebFetch"]
---

# Research-Backed Adversarial Consensus Debate

Orchestrate a structured multi-agent debate where domain-expert personas first gather current evidence, independently critique a plan, then argue their positions until consensus emerges. The output is a battle-tested recommendation and plan incorporating the strongest evidence from each perspective.

This skill is not just a critique engine. When the plan involves technology choices, product decisions, security posture, APIs, vendors, laws, standards, pricing, platform capabilities, or anything else that may have changed recently, the debate MUST begin with current research and MUST cite the evidence used for the recommendation.

## Workflow Overview

```
Discover Plan → Select Personas → Research Briefs (parallel) → Evidence Ledger → Position Papers (parallel) → Moderator Synthesis → Debate Rounds → Final Recommendation
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
- **DECISION_QUESTIONS**: The concrete questions the debate must answer. Extract these from the plan and user request. If the user asks for a recommendation, include "What solution should we choose and why?"

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

Present the selected personas to the user with a brief rationale for each selection. Include a cost estimate: "This debate will use approximately N agent calls (N persona research briefs + N persona papers + moderator + up to 3 debate rounds)." Ask for confirmation before proceeding. The user may add, remove, or swap personas.

## Step 3: Generate Research Briefs (Parallel)

Spawn one Agent per persona **in parallel** using a single message with multiple Agent tool calls. Each persona must research before taking a position.

Research is mandatory when any of the following are true:
- The plan compares technologies, vendors, platforms, frameworks, APIs, models, or libraries
- The user asks for the "best", "right", "current", "latest", "recommended", or "most recent" solution
- The decision depends on external facts, pricing, product capabilities, laws, standards, benchmarks, platform support, or release status
- There is more than a 10% chance that a relevant fact has changed since the plan was written

If research-capable tools are available, the persona must use them. If they are not available, the persona must explicitly state that current external research was unavailable and must not present a final recommendation as proven.

Each persona researches from their domain angle and produces a Research Brief:

```
You are a {PERSONA_TITLE} with 15+ years of experience. You are evaluating a plan
that requires a current, evidence-backed recommendation.

## Your Perspective
{PERSONA_PERSPECTIVE_BIAS}

## Decision Questions
{DECISION_QUESTIONS}

## Research Requirements
Research the current state before recommending anything.

Minimum evidence standard:
1. Use primary sources first: official docs, platform docs, standards, release notes, API references, source repos, benchmark repos, vendor security/privacy docs, or authoritative specifications.
2. Use secondary sources only to fill gaps or compare real-world experience. Label them as secondary.
3. Prefer sources from the last 18 months for fast-moving technologies. If an older source is still controlling, explain why.
4. Capture publication or last-updated dates when available.
5. For each material claim, cite the source URL or file path.
6. Separate verified facts from inferences.

Write a Research Brief with:

1. **Evidence Summary**: The 5-10 facts that matter most, each with citation and date when available
2. **Option Matrix**: The credible options, with current support status, constraints, risks, and fit
3. **Unknowns / Proof Gaps**: Facts you could not verify and what would settle them
4. **Recommended Spike or Test**: The smallest experiment needed if the evidence is insufficient
5. **Preliminary Recommendation**: Choose a direction only if the evidence supports it; otherwise state what research is missing

Do not rely on memory alone. Do not assume the plan's existing conclusion is current.

## The Plan
{FULL_PLAN_CONTENT}
```

Wait for all persona agents to complete. Collect all research briefs.

## Step 4: Build Evidence Ledger

Before generating position papers, synthesize the research briefs into an **Evidence Ledger**. This can be done by the main agent or the `debate-moderator` agent.

The ledger must contain:
- **Decision questions**: The concrete questions being answered
- **Sources reviewed**: URL/path, title, type (primary/secondary), date or last-updated if available, and which persona used it
- **Verified facts**: Claim, source, and relevance
- **Contradictions**: Conflicting claims and what would resolve them
- **Proof gaps**: Missing evidence that blocks a confident recommendation
- **Evidence grade**: `STRONG`, `ADEQUATE`, or `INSUFFICIENT`

If the evidence grade is `INSUFFICIENT` for the main decision, stop the debate path and produce an evidence ledger plus a spike/research plan. Do not proceed to a confident recommendation.

## Step 5: Generate Position Papers (Parallel)

Spawn one Agent per persona **in parallel** using a single message with multiple Agent tool calls. For each selected persona, look up their Perspective Bias from the personas reference and substitute it into the prompt. Each Agent call uses:

- **subagent_type**: `general-purpose`
- **model**: `opus`
- **prompt**: Constructed from the template below, with placeholders filled per persona:

```
You are a {PERSONA_TITLE} with 15+ years of experience. You have been asked to
review the following implementation plan and provide your expert critique and recommendation.

## Your Perspective
{PERSONA_PERSPECTIVE_BIAS}

## Shared Evidence Ledger
{EVIDENCE_LEDGER}

## Your Research Brief
{THIS_PERSONA_RESEARCH_BRIEF}

## Your Task
Write a Position Paper (800-1500 words) that:

1. **Recommendation**: State the solution you recommend and the evidence grade behind it
2. **Executive Assessment**: One paragraph — is this plan sound, risky, or flawed?
3. **Evidence-Backed Rationale**: Cite the facts that drive your position
4. **Strengths**: What does this plan get right? (3-5 points with reasoning)
5. **Concerns**: What worries you? (3-7 points, ranked by severity)
   - For each concern: state the risk, explain why it matters, suggest an alternative
6. **Missing Considerations**: What has been overlooked from your domain expertise?
7. **Recommended Changes**: Concrete, specific modifications (not vague suggestions)
8. **Hard Stance Items**: 1-3 points you would NOT compromise on — the hills you'd die on

Be specific and opinionated. Reference specific sections of the plan and cite evidence from the ledger. Avoid generic advice.
Do NOT be polite about real problems — this is adversarial review.
Do NOT make uncited factual claims about current technology, platform capabilities, pricing, legal status, security posture, or vendor behavior.

## The Plan
{FULL_PLAN_CONTENT}
```

Wait for all persona agents to complete. Collect all position papers.

## Step 6: Moderator Synthesis (Round 1)

Use the Agent tool to invoke the `debate-moderator` agent (set `subagent_type` to `agents-argue:debate-moderator`). Pass it all position papers:

```
Here are position papers from {N} domain experts reviewing an implementation plan.
Synthesize these into a Disagreement Brief following your standard process.
Use the Evidence Ledger to separate evidence-backed findings from unsupported opinions.

## Evidence Ledger
{EVIDENCE_LEDGER}

## Position Papers
{ALL_POSITION_PAPERS}

## Original Plan (for reference)
{FULL_PLAN_CONTENT}
```

The moderator produces a **Disagreement Brief** identifying consensus points, contested decisions, and blind spots.

## Step 7: Debate Rounds (Max 3)

For each round, spawn persona agents **in parallel** again. Each persona receives:

```
You are {PERSONA_TITLE}. You previously reviewed an implementation plan and wrote
a position paper. A moderator has synthesized all position papers and identified
key disagreements.

## Your Previous Position Paper
{THIS_PERSONA_POSITION_PAPER}

## Moderator's Disagreement Brief
{DISAGREEMENT_BRIEF}

## Shared Evidence Ledger
{EVIDENCE_LEDGER}

## Your Task
Respond to the disagreements that involve your expertise (400-800 words):

1. For each disagreement where you hold a position:
   - **Maintain** your stance with new evidence, OR
   - **Concede** to the opposing position with explanation of what convinced you
2. Address any questions the moderator directed at you specifically
3. Respond to counter-arguments from other personas — engage with their reasoning
4. State clearly: "I concede on X" or "I maintain my position on X because..."

Do NOT hedge or be diplomatic. Take clear positions.
Do NOT introduce new factual claims unless you cite sources or explicitly label them as assumptions.
```

After each round, feed responses back to the `debate-moderator` agent (via Agent tool with `subagent_type: agents-argue:debate-moderator`):

```
Round {N} responses from all personas. Update disagreement status.
Determine which disagreements are RESOLVED, MAJORITY, or still CONTESTED.
Reject any resolution that depends on uncited claims or unverified current facts.
If all major disagreements are resolved, indicate CONSENSUS_REACHED.
If not, produce targeted questions for the next round.

## Round {N} Responses
{ALL_RESPONSES}
```

**Termination conditions:**
- Moderator indicates `CONSENSUS_REACHED` → proceed to final synthesis
- Round 3 completed → proceed to final synthesis regardless
- All remaining disagreements are LOW impact → proceed to final synthesis

## Step 8: Final Recommendation Output

Send the `debate-moderator` agent (via Agent tool) the final synthesis request. Set PLAN_DIRECTORY to the parent directory of PLAN_PATH resolved in Step 1:

```
Produce the final research-backed consensus output. Write three files:

1. consensus-plan.md — The revised plan incorporating all resolved decisions
2. evidence-ledger.md — Source list, verified facts, contradictions, and proof gaps
3. debate-transcript.md — Full record of the debate process

## All Debate Material
{POSITION_PAPERS + ALL_ROUND_RESPONSES + DISAGREEMENT_BRIEFS}

## Evidence Ledger
{EVIDENCE_LEDGER}

## Original Plan
{FULL_PLAN_CONTENT}

Write all three files to: {PLAN_DIRECTORY}
```

After the moderator writes the files, present a summary to the user:
- Number of personas, rounds completed
- Sources reviewed and evidence grade
- Recommendation made, including why the selected solution beats alternatives
- Key decisions made (resolved items)
- Any unresolved items requiring human decision
- File paths for the consensus plan, evidence ledger, and transcript

## Error Handling

- If a persona agent fails, continue with remaining personas (minimum 2 required)
- If the moderator agent fails, fall back to manual synthesis: present all position papers to the user
- If plan discovery finds nothing, clearly ask the user for a file path
- If the plan is too short (<100 words), warn the user that debate value may be limited
- If research tools are unavailable, state that limitation before the debate and ask the user whether to continue with an offline critique
- If research completes but evidence is insufficient for the main decision, do not manufacture consensus; produce the evidence ledger and a spike plan instead

## Additional Resources

### Reference Files
- **`references/personas.md`** — Full persona catalog with 170 personas across 16 domains, keyword triggers, and selection algorithm

### Scripts
- **`${CLAUDE_PLUGIN_ROOT}/scripts/find-plans.sh`** — Auto-discovers plan files from bo-planner and deep-plan output locations
