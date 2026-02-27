# Report Templates

Markdown templates for each deliverable in the competitive research workflow.

## Top 10 Report Template

```markdown
# Top 10 {Area} Solutions

> Research conducted: {date}
> Solution area: {area}

## Ranking

| Rank | Solution | Category | Est. Users/Market Share | Key Strength |
|------|----------|----------|------------------------|--------------|
| 1 | [Name] | [Segment] | [Data if available] | [One-liner] |
| 2 | ... | ... | ... | ... |
...

## Selection Methodology

Solutions were identified by cross-referencing:
- [Source 1]
- [Source 2]
- [Source 3]
...

## Brief Descriptions

### 1. {Solution Name}
[2-3 sentence overview: what it is, who it's for, what makes it notable]

### 2. {Solution Name}
...

[Repeat for all 10]
```

## Individual Solution Report Template

```markdown
# {Solution Name} — Deep Dive Report

## Overview
- **Company**: [Company name]
- **Founded**: [Year]
- **Headquarters**: [Location]
- **Target market**: [Who it's for]
- **Pricing**: [Pricing summary with tiers]
- **Website**: [URL]

## Features

### Core Features
- [Feature]: [Brief description]

### Differentiating Features
- [Feature]: [What makes this unique]

### Integration Ecosystem
- [Notable integrations]

## What People Love

### 1. [Theme]
[Evidence from reviews, specific quotes, sources]

### 2. [Theme]
[Evidence]

[Continue for all major positive themes]

## What People Hate

### 1. [Theme]
[Evidence from reviews, specific quotes, sources]

### 2. [Theme]
[Evidence]

[Continue for all major negative themes]

## Market Position
[Competitive positioning, trajectory, target segment]

## Sources
- [Source with URL]
```

## Trends Report Template

```markdown
# {Area} — Market Trends

> Synthesized from deep-dive analysis of 10 leading solutions
> Research date: {date}

## Common Features (Table Stakes)

Features found in 7+ of the 10 solutions analyzed:

| Feature | Present In | Notes |
|---------|-----------|-------|
| [Feature] | 9/10 | [Context] |
...

## Common Strengths (What Users Consistently Love)

### 1. [Theme]
- **Frequency**: Found in [X]/10 solutions
- **Evidence**: [Summarized user sentiment]
- **Best implementation**: [Which solution does this best and why]

### 2. [Theme]
...

## Common Pain Points (What Users Consistently Hate)

### 1. [Theme]
- **Frequency**: Found in [X]/10 solutions
- **Evidence**: [Summarized user frustration]
- **Worst offender**: [Which solution gets the most complaints]

### 2. [Theme]
...

## Pricing Patterns

| Model | Solutions Using It | Price Range |
|-------|-------------------|-------------|
| Freemium | [List] | [Range] |
| Per-seat | [List] | [Range] |
...

## Architecture Patterns
[Technical commonalities: cloud-native, API-first, mobile-first, etc.]

## Market Convergence
[Features that were differentiating 2-3 years ago but are now standard]
```

## Unique Features Report Template

```markdown
# {Area} — Unique Features People Love

> Features that stand out as loved by users and not widely replicated
> Research date: {date}

## {Solution 1 Name}

### [Unique Feature Name]
- **What it does**: [Description]
- **Why users love it**: [Evidence from reviews]
- **Why it's unique**: [How competitors differ]

### [Unique Feature Name]
...

## {Solution 2 Name}
...

[Repeat for each solution that has standout features]

## Summary Table

| Solution | Unique Feature | User Impact | Adoptability |
|----------|---------------|-------------|--------------|
| [Name] | [Feature] | [High/Med/Low] | [Easy/Moderate/Hard] |
...
```

## PRD Template

```markdown
# {Area} — Product Requirements Document

> Generated from competitive analysis of 10 leading solutions
> Research date: {date}

## 1. Problem Statement

### Primary Problem
[Derived from common pain points across all 10 solutions]

### Secondary Problems
- [Problem 2]
- [Problem 3]

### Evidence
[Data from user complaints and reviews supporting these problems]

## 2. Target Users

### Primary Persona
- **Role**: [Who they are]
- **Pain points**: [What frustrates them with current solutions]
- **Goals**: [What they're trying to accomplish]
- **Current solutions**: [What they use today]

### Secondary Persona
...

## 3. Product Vision

[2-3 paragraph vision for how a new product addresses the identified problems
better than existing solutions, informed by the research]

## 4. Feature Requirements

### P0 — Must-Have (Table Stakes)
Features every competitor has. Without these, the product won't be considered.

| Feature | Rationale | Found In |
|---------|-----------|----------|
| [Feature] | [Why it's required] | [X/10 solutions] |
...

### P1 — Should-Have (Competitive Parity)
Common strengths users love. These drive adoption and retention.

| Feature | Rationale | Best Implementation |
|---------|-----------|-------------------|
| [Feature] | [Why users love it] | [Which competitor does it best] |
...

### P2 — Nice-to-Have (Differentiation)
Unique features worth adopting from specific competitors.

| Feature | Source | User Impact |
|---------|--------|-------------|
| [Feature] | [Which competitor] | [Why users love it] |
...

### P3 — Innovative (Blue Ocean)
Features that don't exist yet, derived from user complaints no one has solved.

| Feature | Problem It Solves | Evidence |
|---------|------------------|----------|
| [Feature] | [User complaint] | [Review sources] |
...

## 5. Success Metrics

| Metric | Target | Rationale |
|--------|--------|-----------|
| [Metric] | [Target] | [Based on competitor benchmarks] |
...

## 6. Competitive Positioning

### Positioning Statement
[One paragraph: For [target users] who [need], [product] is a [category]
that [key differentiator]. Unlike [competitors], [product] [unique value].]

### Competitive Matrix

| Capability | Our Product | Competitor A | Competitor B | Competitor C |
|-----------|-------------|-------------|-------------|-------------|
| [Capability] | [Plan] | [Status] | [Status] | [Status] |
...

## 7. Appendix

### Sources
- [All sources referenced in this PRD]

### Related Reports
- `top-10-{area}-report.md` — Initial solution ranking
- Individual solution reports (10 files)
- `{area}-trends.md` — Cross-solution trend analysis
- `{area}-unique-features.md` — Standout features analysis
```
