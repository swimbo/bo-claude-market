---
name: whitepaper-authoring
description: >
  This skill should be used when the user is writing, planning, outlining, drafting,
  reviewing, or revising a technical whitepaper. It should also be used when the user
  mentions "whitepaper", "white paper", "technical paper", "thought leadership paper",
  "problem/solution paper", or asks about whitepaper structure, sections, citation styles,
  or formatting conventions.
version: 1.0.0
---

# Technical Whitepaper Authoring

Apply this knowledge when assisting with any whitepaper authoring task.

## Whitepaper Types

There are six recognized types. The type determines structure, tone, depth, and audience.

1. **Pure Technical** — Deep dive into technology/implementation for engineers and architects. Includes code snippets, architecture diagrams, benchmarks. Structure: business case > architecture > implementation > benchmarks > case studies.

2. **Problem/Solution** — Identifies a pain point, builds evidence, presents solution as logical conclusion. For decision-makers. Structure: problem > amplification > solution framework > validation > CTA.

3. **Backgrounder/Product** — Technical evaluation of a product for bottom-of-funnel buyers. Includes competitive comparisons handled carefully. Structure: problem > product overview > features > benefits > proof points > next steps.

4. **Thought Leadership** — Establishes authority on an industry topic. Requires original perspective. Usually by-lined to a senior executive. Structure: issue intro > current state > new framing > implications > recommendations.

5. **Market Research** — Presents original research findings with heavy data visualization. Structure: research overview > methodology > findings > analysis > implications > conclusion.

6. **Visionary** — Forward-looking narrative about the future of an industry. Uses storytelling grounded in facts. Structure: scene-setting > landscape > forces of change > future scenarios > vision > CTA.

See `references/whitepaper-types.md` for full details on each type.

## Standard Section Order

All whitepapers follow this general structure (sections may be omitted based on type):

1. Cover Page (title, subtitle, author, org, date, version)
2. Abstract (technical audiences, 150-250 words) OR Executive Summary (business audiences, max 1 page)
3. Table of Contents (required if >6 pages)
4. Introduction / Problem Statement
5. Background / Context
6. Methodology (research-based papers only)
7. Body / Analysis / Solution
8. Results / Findings (can merge with Body)
9. Conclusion
10. Call to Action (commercially-oriented papers)
11. References / Bibliography
12. Appendices / Glossary

See `references/section-structure.md` for detailed guidance on each section.

## Pre-Writing Questions

Ask these questions before starting any whitepaper. Organize by category:

**Audience:** Who reads this? Knowledge level? Pain points? Multiple audiences?
**Purpose:** Goal? Buyer journey stage? Key message? Desired action? Success metrics?
**Content/Scope:** Specific question answered? Original data/perspective? What is out of scope?
**Technical Depth:** How technical (1-10)? Code/diagrams? Reproducible implementation?
**Logistics:** SMEs to interview? Deadline? Gated or ungated? Output formats? Distribution plan?

## Writing Standards

* Third-person voice for formal/technical papers

* Sentences under 14 words improve comprehension by \~90%

* Eliminate buzzwords: "leveraging," "best-in-class," "industry-leading," "synergies"

* Every claim must be backed by data, benchmarks, citations, or peer-reviewed sources

* Product mentions only near the end, after establishing credibility

* Acknowledge limitations — this increases credibility

## Citation Conventions

| Field                     | Style   | In-text                   |
| ------------------------- | ------- | ------------------------- |
| Engineering, CS           | IEEE    | Numbered \[1]             |
| Business, social sciences | APA     | Author-date (Smith, 2023) |
| Humanities                | MLA     | Author-page (Smith 45)    |
| Law, government, policy   | Chicago | Footnotes                 |

Default to IEEE for technical whitepapers. See `references/citation-styles.md`.

## Visual Element Rules

* Figure captions: placed BELOW the figure

* Table captions: placed ABOVE the table

* Reference all visuals by number ("see Figure 3"), never by position ("the chart below")

* Every visual needs: numbered caption, descriptive title, labeled axes/legends, source attribution

* Use diagrams for architecture/process flows, tables for comparisons, charts for trends

See `references/visual-conventions.md`.

## Quality Differentiation

Great whitepapers: answer one specific question, present original data, quantify concretely ("reduced by 67%"), serve reader first, acknowledge limitations, have clear narrative arc.

Mediocre whitepapers: start with solution before problem, sound like sales brochures, make vague claims, use company jargon, cite secondary sources, mention product too early.

The critical reframe: frame around what the READER gets, not what the company wants to announce.

See `references/quality-checklist.md`.

## PDF Generation

The plugin includes a PDF generation script at `$CLAUDE_PLUGIN_ROOT/scripts/generate-pdf.sh`. It uses pandoc with a LaTeX engine. Check pandoc availability before attempting PDF output.

## Author History

Check `~/.claude/whitepaper-history.json` for previously used author names and organizations. Offer these as quick-select options when asking for author info. After the user provides new info, update the history file.