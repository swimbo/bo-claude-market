---
name: Research Methodology
description: This skill should be used when conducting research for articles, gathering sources, fact-checking claims, or synthesizing information from multiple sources. It applies when the user mentions "research", "sources", "fact-check", "find information", "deep research", "verify claims", or discusses research depth, source quality, or information synthesis.
version: 1.0.0
---

# Research Methodology

## Overview

Research is the foundation of credible article writing. This skill defines how to gather, evaluate, synthesize, and document information at four depth levels. All research output feeds into Stage 1 of the article pipeline and is stored for traceability and citation.

## Research Depth Levels

### Basic (3-5 queries)

Use for familiar topics, opinion pieces, or short-form content where the writer already has domain knowledge.

1. Formulate 3-5 targeted WebSearch queries based on the topic and angle.
2. Review the top 3-5 results for each query.
3. Extract key facts, statistics, and relevant quotes.
4. Summarize findings in a concise research document.
5. List all source URLs.

Expected output: 500-1,000 words. Turnaround: fast. Suitable for opinion pieces, short blog posts, and topics where the writer has existing domain expertise.

### Light (8-12 queries)

Use for standard articles where moderate depth is needed. This is the default level.

1. Formulate 8-12 targeted queries, varying search terms to capture different facets of the topic.
2. Review the top 5-7 results for each query.
3. Cross-reference key claims across multiple sources. Flag any contradictions.
4. Identify and extract expert opinions with attribution.
5. Locate relevant statistics with their original sources.
6. Use Perplexity Sonar Deep API for synthesizing findings across sources into a coherent research narrative.
7. Document all sources with URLs and access dates.

Expected output: 1,000-2,000 words. Turnaround: moderate. Suitable for standard blog posts, newsletter features, and general-audience articles.

### Medium (15-20 queries)

Use for thought leadership, in-depth analysis, and pieces that need to demonstrate comprehensive understanding.

1. Formulate 15-20 queries spanning the topic's core, adjacent areas, historical context, and current developments.
2. Review the top 7-10 results for each query.
3. Extensively cross-reference claims. Identify consensus positions and areas of disagreement.
4. Seek out primary sources (original research papers, official reports, firsthand accounts) rather than relying solely on secondary reporting.
5. Actively search for contrarian viewpoints and alternative perspectives. Dedicate 3-4 queries specifically to finding opposing arguments.
6. Collect statistics and data points, tracing each to its original publication.
7. Use Gemini 3.1 Pro for deep synthesis, pattern identification, and gap analysis across the collected research.
8. Document all sources with URLs, access dates, and credibility notes.

Expected output: 2,000-3,500 words. Turnaround: slower. Suitable for thought leadership pieces, industry analysis, and articles intended to establish authority on a topic.

### Deep (25+ queries)

Use for definitive, authoritative pieces intended to be comprehensive references on a topic.

1. Formulate 25+ queries covering the topic exhaustively: core concepts, history, current state, future trends, adjacent fields, key players, controversies, data, methodology, and implications.
2. Review the top 10+ results for each query.
3. Seek academic sources, research papers, and institutional reports. Use targeted queries for Google Scholar, arXiv, and domain-specific databases.
4. Collect expert quotes from multiple perspectives, ensuring balanced representation.
5. Build a comprehensive historical timeline of the topic's development.
6. Perform data analysis on collected statistics: identify trends, outliers, and patterns.
7. Dedicate 5+ queries to contrarian viewpoints, criticisms, and failure cases.
8. Research future implications, forecasts, and emerging developments.
9. Use Opus 4.6 for comprehensive synthesis, identifying meta-patterns, constructing frameworks, and producing an integrated research narrative.
10. Document all sources with full bibliographic information, access dates, and credibility assessments.

Expected output: 3,500-6,000 words. Turnaround: significant. Reserve this level for definitive reference pieces, comprehensive guides, and articles where thoroughness is a key value proposition.

## Research Output Structure

Regardless of depth level, structure the research document with these sections:

### Executive Summary
A 2-3 paragraph synthesis of the most important findings. Highlight the dominant narrative, key tensions, and the most compelling data points. Write this last, after all research is complete.

### Key Facts and Statistics
A bulleted list of verified facts and data points. Each entry must include the source URL. Organize by subtopic or chronologically, whichever aids comprehension.

### Expert Opinions
Attributed quotes and paraphrased positions from identified experts. Include the expert's credentials and affiliation. Note areas of agreement and disagreement among experts.

### Contrarian Viewpoints
Deliberately collected alternative perspectives, criticisms, and counterarguments. Present these fairly, not dismissively. Note the strength of evidence behind each contrarian position.

### Sources
A numbered list of all sources consulted, with:
- Title
- Author (if identifiable)
- Publication/site name
- URL
- Date accessed
- Brief credibility note (e.g., "peer-reviewed journal", "industry blog", "official government report")

### Recommended Angles
Based on the research, suggest 2-4 potential angles or thesis statements for the article. Note which angles have the strongest evidentiary support and which would be most original. For each angle, briefly note the key evidence that supports it and the potential risks (e.g., "strong data but contrarian view may alienate mainstream audience").

### Research Gaps
Explicitly list any questions that remain unanswered after research. Note areas where available sources are insufficient, contradictory, or outdated. Flag topics that would benefit from additional research or expert consultation. This section helps the outline stage make informed decisions about what to include and what to qualify.

## Source Evaluation

Apply these criteria when assessing source quality:

- **Prefer primary sources** over secondary reporting. An original research paper is more reliable than a blog post summarizing it.
- **Verify recency**. Check publication dates. For fast-moving topics, deprioritize sources older than 12 months unless they provide foundational context.
- **Assess authority**. Prefer sources from recognized institutions, peer-reviewed publications, established domain experts, and official bodies.
- **Check for bias**. Note the source's potential conflicts of interest, funding sources, or ideological positioning. Do not discard biased sources but flag the bias.
- **Cross-reference claims**. A claim appearing in only one source should be flagged as unverified. A claim corroborated by 3+ independent sources can be treated as established.

## Fact-Checking Approach

Apply these practices throughout the research process:

- **Verify statistics at their source**. When a secondary source cites a statistic, trace it back to the original study or dataset. Note any discrepancies in how the statistic has been reported.
- **Check quote accuracy**. When collecting expert quotes, verify them against the original publication. Note whether quotes are from written work, interviews, or social media.
- **Confirm dates and names**. Verify dates of events, correct spellings of names, and accuracy of titles and affiliations.
- **Flag uncertain claims**. Mark any claim that cannot be adequately verified with a confidence indicator: [verified], [likely accurate], [unverified], [disputed].
- **Note contradictions**. When sources contradict each other, document both positions and assess which has stronger evidence.

## Web Tools Usage

### WebSearch
Use for discovering sources and getting an overview of available information on a topic. Formulate specific, targeted queries rather than broad ones. Vary query phrasing to capture different result sets.

### WebFetch
Use to retrieve the full content of specific web pages identified through WebSearch. Prefer fetching primary sources, detailed articles, and pages with data tables or statistics. Extract the relevant content and discard navigation, ads, and boilerplate.

## Attribution

Maintain a running source list throughout the research process. Every fact, statistic, quote, and substantive claim must be linked to its source URL. This source list carries through the entire pipeline so that the final article can include proper citations or a references section.

When recording a source, capture the URL immediately. Do not plan to "find it later" -- URLs become difficult to relocate.

Use a consistent citation format throughout. Each source entry should include a sequential number, the title, the author or organization, the URL, and a one-line relevance note. This format carries through to the final article where citations can be rendered as footnotes, inline links, or a references section depending on the template.

## Query Formulation Strategy

Effective research depends on well-crafted queries. Follow these principles:

- **Start broad, then narrow**. Begin with overview queries to understand the landscape, then drill into specific subtopics.
- **Vary terminology**. Search for the same concept using different terms, synonyms, and related phrases. Industry jargon, academic terminology, and casual language all surface different results.
- **Use operators**. Include site-specific searches (e.g., restricting to .gov, .edu, or specific publications) when seeking authoritative sources.
- **Search for disagreement**. Explicitly query for criticisms, failures, and counterarguments. Queries like "problems with X" or "why X fails" surface perspectives that balanced queries miss.
- **Time-bound when relevant**. For fast-moving topics, restrict searches to recent timeframes to avoid outdated information.

## Handling Conflicting Information

When sources disagree:

1. Document both positions with their respective sources.
2. Assess the credibility and recency of each source.
3. Note whether the disagreement is factual (verifiable) or interpretive (opinion-based).
4. If factual, attempt to trace back to primary data to determine which position is correct.
5. If interpretive, present both perspectives in the research output and let the article writer decide how to handle the tension.
6. Never silently discard the minority position. Contrarian views often make articles more interesting and credible.

## Research for Article Series

When researching for a series of related articles:

1. Consider the full series arc. Identify which research is foundational (relevant to all articles) and which is specific to individual installments.
2. Conduct foundational research once and store it in a shared research directory accessible to all articles in the series.
3. For each individual article, conduct targeted research that builds on the foundation without repeating it.
4. Track which sources have been cited in previous articles to avoid over-relying on the same references.
5. Identify gaps in the series coverage that later articles should address.
6. Store series-level research in a shared directory alongside the individual article directories: `/Users/bo/code/articles/<series-slug>/shared-research/`.

## Research Quality Checklist

Before marking research as complete, verify:

- [ ] All key claims have at least one source URL attached.
- [ ] Statistics have been traced to their original publication, not just a secondary source.
- [ ] At least one contrarian viewpoint has been documented (for medium and deep levels).
- [ ] The executive summary accurately reflects the full body of research.
- [ ] Source credibility has been assessed and noted.
- [ ] The recommended angles are supported by the evidence collected.
- [ ] Research gaps are explicitly documented rather than silently ignored.
