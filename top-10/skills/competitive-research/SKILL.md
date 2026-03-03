---
name: Competitive Research
description: >
  This skill should be used when the user asks to "research competitors",
  "analyze a market", "find top solutions", "competitive analysis",
  "compare products in a category", "market landscape", or mentions
  researching existing solutions before building a product. Provides
  methodology for systematic competitive research and report generation.
---

# Competitive Research Methodology

Systematic approach to researching, analyzing, and synthesizing competitive landscapes in any solution area.

## Core Workflow

The competitive research process follows six sequential phases. Each phase produces a deliverable file.

### Phase 1: Solution Discovery

Identify the top 10 solutions in the target area.

1. Run multiple web searches with varied queries:

   * `"best {area} software 2026"`

   * `"top {area} tools"`

   * `"G2 best {area}"`

   * `"{area} market leaders"`

   * `"alternatives to [known leader in space]"`
2. Cross-reference results across sources (G2, Capterra, Gartner, industry blogs, Reddit)
3. Rank by frequency of appearance, market share data, and review volume
4. Present the top 10 list to the user for approval before proceeding
5. Write `top-10-{area}-report.md` with the ranked list including a brief description of each

### Phase 2: Individual Solution Deep Dives

For each approved solution, launch a `solution-researcher` agent (via Task tool) to produce a comprehensive report.

* Launch all 10 agents in parallel for speed

* Each agent writes `{solution-name}-report.md` to the current directory

* Each report covers: features, pricing, user loves, user hates, market position

* Wait for all agents to complete before proceeding

### Phase 3: Trend Analysis

Read all 10 individual reports and identify patterns.

Analyze across these dimensions:

* **Common features**: What do most/all solutions offer?

* **Common strengths**: What do users consistently love across the category?

* **Common pain points**: What frustrations appear repeatedly?

* **Pricing patterns**: How do pricing models compare?

* **Architecture patterns**: Shared technical approaches (cloud-native, API-first, etc.)

* **Market convergence**: Features that were once differentiating but are now table stakes

Write `{area}-trends.md` with findings organized by dimension.

### Phase 4: Unique Features Analysis

Read all 10 individual reports and identify standout features.

For each solution, extract features that:

* Are unique to that solution (not found in most competitors)

* Are specifically called out as loved by users

* Represent innovative approaches to common problems

Write `{area}-unique-features.md` organized by solution, with context on why each feature matters.

### Phase 5: Recommended Pricing

Read all 10 individual reports (focusing on their Pricing sections) and the trends report (Pricing Patterns section). Synthesize a recommended pricing strategy.

Analyze across these dimensions:

* **Market pricing landscape**: Aggregate all competitors' tiers, models, and price points into a comparison

* **Pricing model analysis**: Which models dominate and how users feel about each

* **Price sensitivity insights**: What pricing-related praise and complaints appear in reviews

* **Free tier strategy**: Whether to offer a free plan, with what limits, based on competitive evidence

* **Recommended pricing structure**: Concrete tiers with price ranges and feature allocation

* **Pricing pitfalls to avoid**: Common mistakes identified from user backlash

Write `{area}-recommended-pricing.md` with the complete pricing recommendation.

### Phase 6: PRD Generation

Synthesize the trends and unique features into a product requirements document.

Structure the PRD as:

1. **Problem Statement**: Derived from common pain points found across solutions
2. **Target Users**: Identified from the user bases of researched solutions
3. **Product Vision**: How to build something better based on the research
4. **Feature Requirements**:

   * **Must-have** (P0): Features every competitor has — table stakes

   * **Should-have** (P1): Common strengths users love — competitive parity

   * **Nice-to-have** (P2): Unique features worth adopting — differentiation

   * **Innovative** (P3): Gaps identified from user complaints — blue ocean
5. **Success Metrics**: Based on what users measure competitors against
6. **Competitive Positioning**: Where the new product fits in the landscape

Write `{area}-prd.md` with the complete PRD.

## File Naming Convention

Slugify all file names: lowercase, hyphens for spaces, strip special characters.

* Area "Task Management" → `task-management`

* Solution "Monday.com" → `monday-com`

* Solution "ClickUp" → `clickup`

## Quality Standards

* Every claim traced to a source

* Prefer data from the last 2 years

* Minimum 5 sources per individual report

* Present user quotes when available

* Distinguish fact from opinion

* Note when data is limited or conflicting

## Additional Resources

### Reference Files

For detailed guidance on specific phases, consult:

* **`references/report-templates.md`** — Markdown templates for all report types
