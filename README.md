# Bo's Claude Code Marketplace

Custom plugins for Claude Code.

## Plugins

| Plugin | Description |
|--------|-------------|
| [bo-planner](./bo-planner/) | File-based planning — 14-phase model with scope fences, environment snapshots, verification gates, adversarial debate gates, plan gap audit |
| [implement-bo-plan](./implement-bo-plan/) | Enterprise-grade plan executor — orchestrates agents-argue, standard-design, test-everything, and enterprise-assessment to drive phases 9–14 with quality gates and gap auditing |
| [agents-argue](./agents-argue/) | Multi-agent adversarial debate — 170 domain-expert personas stress-test plans through structured rounds until consensus. Used as a gate by bo-planner phases 5 and 6 |
| [enterprise-assessment](./enterprise-assessment/) | Enterprise readiness evaluator — 12-category assessment with risk scoring, compliance mapping (NIST, SOC2, ISO 27001) |
| [standard-design](./standard-design/) | Standard Design System — apply, review, and scaffold React + MUI admin interfaces with dual-mode theming |
| [test-everything](./test-everything/) | Comprehensive testing toolkit — audit gaps, plan strategy, scaffold infrastructure, review quality, contract enforcement |
| [whitepaper](./whitepaper/) | Technical whitepaper authoring — guided creation, review, and revision workflows |
| [top-10](./top-10/) | Competitive research — top 10 solutions analysis with deep dives and PRD generation |
| [article-writer](./article-writer/) | Article writing — 6-stage pipeline with voice profiles (analyze or interview), templates, research depth levels, series support |
| [article-publisher](./article-publisher/) | Publish articles to Substack, Reddit, and LinkedIn with browser automation, screenshot verification, and auto-formatting fixes |
| [incident-postmortem](./incident-postmortem/) | Incident postmortem builder — intake artifacts (logs, chat threads, screenshots), produce structured 8-section postmortems |

## Plugin Integration

The core plugins (bo-planner, implement-bo-plan, agents-argue, standard-design, test-everything, enterprise-assessment) automatically detect and consume each other's artifacts when installed on the same project. This enables a unified lifecycle:

```
Plan (bo-planner phases 1–8)
  ↳ debate gates via agents-argue (phases 5, 6)
Execute (implement-bo-plan phases 9–14)
  ↳ standard-design scaffold + review
  ↳ test-everything plan, scaffold, full-suite, contract
  ↳ enterprise-assessment gate (grade ≥ B)
  ↳ plan-gaps.md audit + fix loop
Deliver (bo-planner :done)
```

See [plugin-integration.md](./plugin-integration.md) for the full integration guide, artifact flow diagrams, and example workflows.

## Installation

```bash
claude plugin install bo-planner --marketplace bo-marketplace
claude plugin install implement-bo-plan --marketplace bo-marketplace
claude plugin install agents-argue --marketplace bo-marketplace
claude plugin install enterprise-assessment --marketplace bo-marketplace
claude plugin install standard-design --marketplace bo-marketplace
claude plugin install test-everything --marketplace bo-marketplace
claude plugin install whitepaper --marketplace bo-marketplace
claude plugin install top-10 --marketplace bo-marketplace
claude plugin install article-writer --marketplace bo-marketplace
claude plugin install article-publisher --marketplace bo-marketplace
claude plugin install incident-postmortem --marketplace bo-marketplace
```
