# Test-Everything Plugin — Debate Transcript

## Metadata

| Field | Value |
|---|---|
| Date | 2026-04-01 |
| Format | Adversarial consensus (position papers → moderator synthesis → debate round → final consensus) |
| Rounds | 2 |
| Personas | Senior QA Architect, Senior E2E Test Engineer, Senior Design Systems Engineer (contrarian), Senior DX Engineer |
| Source Plan | docs/planning/phased-plan.md |
| Plugin | agents-argue v0.1.0 |

## Position Paper Summaries

### Senior QA Architect
- **Assessment:** Structurally sound but strategically timid
- **Top concern:** No validation that templates change agent behavior (CRITICAL)
- **Hard stances:** Walkthrough needs test.step(), "verified interaction" needs formal definition, version bump requires before/after proof

### Senior E2E Test Engineer (Playwright Specialist)
- **Assessment:** Strategically misaligned — ignores timing, parallelism, CI integration
- **Top concern:** No timing/waiting strategy (CRITICAL)
- **Hard stances:** Kill walkthrough mega-test, mandatory timing strategy, browser health must capture traces

### Senior Design Systems Engineer (Contrarian)
- **Assessment:** Architecturally misaligned — pushes component defects to E2E layer
- **Top concern:** "Accessible selectors" misnomer creates false accessibility confidence (CRITICAL)
- **Hard stances:** Rename to semantic locators, component defects belong in component tests, browser health needs allowlist

### Senior DX Engineer
- **Assessment:** Under-specified prompt engineering problem
- **Top concern:** No generated output examples — LLMs follow examples more than rules (CRITICAL)
- **Hard stances:** Every template needs output examples, walkthrough must not be monolithic, selector hierarchy must be enforced in code

## Disagreement Map (Pre-Debate)

| Topic | QA Arch | E2E Eng | DSE | DX Eng |
|-------|---------|---------|-----|--------|
| Walkthrough | test.step() fix | Kill entirely | Cross-flow suite | Transition tests |
| Test pyramid | Silent | Silent | 10:1 ratio mandate | Silent |
| Terminology | Silent | Neutral | Rename to semantic | Neutral |
| Timing | Silent | CRITICAL | Silent | LOW |
| Coverage report | Cut entirely | No data source | No mechanism | No data source |
| Output examples | Implied | Implied | Silent | CRITICAL |
| Allowlist | Needed | Default + override | Needed | Silent |

## Round 2 — Key Shifts

| Expert | Conceded On | Shifted To | Why |
|--------|------------|-----------|-----|
| QA Architect | Walkthrough | Independent specs + smoke | Accepted mega-test is anti-pattern |
| QA Architect | Test pyramid | Component assertions out of E2E | Design Systems Engineer's argument convinced |
| QA Architect | Terminology | "Semantic locators" | Agreed "accessible" is misleading |
| E2E Engineer | CI/CD scope | Checklist in template | Pipeline config is separate deliverable |
| E2E Engineer | Test pyramid | Push to component, keep E2E for DOM | Qualified concession |
| E2E Engineer | Terminology | "Semantic locators" | Accepted |
| Design Systems Eng | Component gate | Diagnostic, not blocker | Unrealistic as prerequisite |
| Design Systems Eng | Coverage report | Checklist | More pragmatic than cut or spike |
| DX Engineer | Audit grep | Concrete commands | Tightened from free-form to specific patterns |
| DX Engineer | Terminology | "Semantic locators" | Clearer for DX audience |

**Positions held firm:**
- QA Architect: Timing mandatory, coverage report should be cut
- E2E Engineer: Kill walkthrough entirely, timing is critical, trace capture required
- Design Systems Engineer: 10:1 ratio in Phase 2, cross-flow smoke suite
- DX Engineer: Output examples non-negotiable, timing is low priority

## Final Resolution Table

| # | Topic | Status | Vote | Decision |
|---|-------|--------|------|----------|
| 1 | Terminology | RESOLVED | 4:0 | "Semantic locators" |
| 2 | Coverage report | RESOLVED | 3:1 | Checklist (QA wanted cut — both eliminate heavy report) |
| 3 | Selector allowlist | RESOLVED | 3:0 | Default set + per-project override |
| 4 | Component prerequisite | RESOLVED | 4:0 | Diagnostic, not gate |
| 5 | Output examples | RESOLVED | 4:0 | 2 per section, inline |
| 6 | Audit commands | RESOLVED | 4:0 | Concrete grep commands |
| 7 | Walkthrough | MAJORITY | 3:1 | Cross-flow transition tests (E2E Eng dissents) |
| 8 | Test pyramid | MAJORITY | 3:1 | Distribution Check in Phase 5 (DSE dissents) |
| 9 | Timing strategy | MAJORITY | 2:1:1 | Mandatory section (DX Eng rates low) |

## Action Recommendations

1. **Monitor transition test drift** — After 30 days, audit for action count, duration, and state isolation
2. **Consider strict mode** — If E2E-heavy generation persists, promote DSE's ratio constraint as opt-in
3. **Review timing section length** — If template adoption suffers, timing is first candidate for extraction to appendix
