---
name: test-property
description: Property-based testing where the LLM states invariants and a deterministic engine (Hypothesis, fast-check, proptest, gopter) falsifies them. Every counterexample is a found bug or a wrong invariant.
argument-hint: "[target-file-or-module]"
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "Agent", "WebSearch"]
---

# Property-Based Testing (LLM Proposes, Engine Falsifies)

The LLM's role is to **STATE invariants**; a deterministic property engine **falsifies** them. Never trust a property suite that has never falsified anything.

## Instructions

### Step 1: State Invariants

Read the target code and state 2–5 invariants per unit, in precise English FIRST (precision failures here are caught cheaply by the engine). Standard invariant families:

- **Round-trip**: serialize → parse == identity
- **Idempotence**: f(f(x)) == f(x)
- **Order-independence**: result independent of input ordering
- **Conservation**: sum of parts == total
- **Bounds**: 0 ≤ x < n
- **Monotonicity / metamorphic relations**: if input grows, output never shrinks

### Step 2: Encode + Generate

| Stack | Tool |
|---|---|
| Python | Hypothesis `@given(st.integers(), st.text())` with tailored strategies |
| JS/TS | fast-check `fc.assert(fc.property(fc.integer(), ...))` |
| Rust | proptest / quickcheck |
| Go | gopter table/property blocks |

Write generators for the actual input domain, not just primitives. Use WebSearch to confirm API details if unsure.

### Step 3: Falsify

Run. Every counterexample is one of:

- a **real bug** → fix the code, add the shrunk input as a regression test, or
- a **wrong invariant** → sharpen it, record why it was wrong.

Hypothesis shrinks automatically; fast-check uses `fc.seed` for reproducibility — **always record the seed**.

### Step 4: Prove the Harness Can Fail

Before trusting a new property suite, inject one known-bad implementation once and confirm the property fires. A property suite that has never failed anything is untested machinery.

Details: `skills/test-strategy/references/enhancement-capabilities.md` §5.
