# Adversarial Consensus

A Claude Code plugin that stress-tests implementation plans through structured multi-agent debate. Domain-expert personas independently critique a plan, argue their positions across multiple rounds, and converge on a battle-tested consensus.

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
3. **Position Papers** — Each persona independently writes a detailed critique (spawned in parallel)
4. **Synthesize** — A moderator agent identifies consensus points, contested decisions, and blind spots
5. **Debate** — Personas argue specific disagreements across up to 3 rounds
6. **Consensus** — Final output: a revised plan + full debate transcript

## Output

Two files written to the same directory as the input plan:

- **`consensus-plan.md`** — The revised plan with all resolved changes applied, unresolved items flagged, and dissenting opinions preserved
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
- **Simple plan** (3 personas, 1-2 rounds): ~8-12 agent calls
- **Complex plan** (5 personas, 3 rounds): ~18-22 agent calls

The skill displays an estimate and asks for confirmation before starting.
