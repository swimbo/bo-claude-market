# Research-Backed Adversarial Consensus

A Claude Code plugin that researches and stress-tests implementation plans through structured multi-agent debate. Domain-expert personas gather current evidence, independently critique a plan, argue their positions across multiple rounds, and converge on a battle-tested recommendation.

## How It Works

Invoke by asking Claude to debate your plan:

```
"debate the plan at docs/planning/phased-plan.md"
"stress-test this plan"
"red team the implementation plan"
"poke holes in this plan"
```

Or use the skill directly: `/agents-argue:debate [path/to/plan.md]`

1. **Discover** — Finds the plan (auto-discovers from bo-planner and deep-plan output, or accepts a path)
2. **Analyze** — Reads the plan, identifies relevant domains, selects 3-5 expert personas
3. **Research** — Each persona gathers current evidence from primary sources where possible and records citations
4. **Evidence Ledger** — The moderator grades the evidence, tracks verified facts, and flags proof gaps
5. **Position Papers** — Each persona writes an evidence-backed critique and recommendation
6. **Synthesize** — A moderator agent identifies evidence-backed consensus points, contested decisions, and blind spots
7. **Debate** — Personas argue specific disagreements across up to 3 rounds
8. **Recommendation** — Final output: a revised plan, evidence ledger, and full debate transcript

For decisions involving current technology, platform capabilities, vendors, APIs, security/privacy behavior, pricing, standards, laws, or other facts that can drift, research is mandatory. The plugin must not present a confident recommendation unless the evidence ledger supports it. If proof is missing, the output becomes a spike or research plan with the exact facts needed to decide.

## Output

Three files written to the same directory as the input plan:

- **`consensus-plan.md`** — The revised plan with all resolved changes applied, unresolved items flagged, and dissenting opinions preserved
- **`evidence-ledger.md`** — Sources reviewed, verified facts, option matrix, contradictions, proof gaps, and evidence grade
- **`debate-transcript.md`** — Full record: position papers, disagreement maps, round-by-round evolution, final resolution table

## Persona Pool

170 curated personas across 16 domains:

- Architecture & Systems Design
- Backend / Frontend / Fullstack / Mobile Engineering
- DevOps / SRE / Platform Engineering
- Security
- Database & Data Engineering
- AI / ML / Data Science
- QA & Testing
- Product & Design
- Program Management & Leadership
- Compliance, Governance & Risk
- Cost & Business
- Developer Experience
- Enterprise IT & Legacy Systems
- Networking & Infrastructure

Personas are auto-selected based on plan content. You can override the selection before the debate begins.

## Plan Auto-Discovery

When invoked without a path, the plugin searches for:

| Source | Location | Detection |
|--------|----------|-----------|
| bo-planner | `docs/planning/phased-plan.md` | File existence |
| deep-plan | Per `deep_plan_config.json` | Config file parsing |
| Fallback | `PLAN.md`, `plan.md`, etc. | Common patterns |

## Installation

```bash
claude --plugin-dir /path/to/agents-argue
```

## Requirements

- Claude Code with Agent tool support
- Python 3 (used by `find-plans.sh` to parse `deep_plan_config.json`)
- Opus model recommended for deepest persona reasoning

## Cost Estimate

A full debate spawns multiple Opus-level agent calls:
- **Simple plan** (3 personas, 1-2 rounds): ~11-15 agent calls
- **Complex plan** (5 personas, 3 rounds): ~23-28 agent calls

The skill displays an estimate and asks for confirmation before starting.
