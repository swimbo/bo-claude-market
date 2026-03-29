# Bo's Claude Code Marketplace

Custom plugins for Claude Code.

## Plugins

| Plugin | Description |
|--------|-------------|
| [bo-planner](./bo-planner/) | File-based planning — scope fences, environment snapshots, verification gates, subagent delegation |
| [enterprise-assessment](./enterprise-assessment/) | Enterprise readiness evaluator — 12-category assessment with risk scoring, compliance mapping (NIST, SOC2, ISO 27001) |
| [standard-design](./standard-design/) | Standard Design System — apply, review, and scaffold React + MUI admin interfaces with dual-mode theming |
| [test-everything](./test-everything/) | Comprehensive testing toolkit — audit gaps, plan strategy, scaffold infrastructure, review quality |
| [whitepaper](./whitepaper/) | Technical whitepaper authoring — guided creation, review, and revision workflows |
| [top-10](./top-10/) | Competitive research — top 10 solutions analysis with deep dives and PRD generation |
| [article-writer](./article-writer/) | Article writing — 6-stage pipeline with voice profiles, 42 templates, research depth levels, series support |
| [incident-postmortem](./incident-postmortem/) | Incident postmortem builder — intake artifacts (logs, chat threads, screenshots), produce structured 8-section postmortems |

## Plugin Integration

Four core plugins (bo-planner, standard-design, test-everything, enterprise-assessment) automatically detect and consume each other's artifacts when installed on the same project. This enables a unified lifecycle:

```
Plan → Design → Review → Test → Assess → Deliver
```

See [plugin-integration.md](./plugin-integration.md) for the full integration guide, artifact flow diagrams, and example workflows.

## Installation

```bash
claude plugin install bo-planner --marketplace bo-marketplace
claude plugin install enterprise-assessment --marketplace bo-marketplace
claude plugin install standard-design --marketplace bo-marketplace
claude plugin install test-everything --marketplace bo-marketplace
claude plugin install whitepaper --marketplace bo-marketplace
claude plugin install top-10 --marketplace bo-marketplace
claude plugin install article-writer --marketplace bo-marketplace
claude plugin install incident-postmortem --marketplace bo-marketplace
```
