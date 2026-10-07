---
name: test-differential
description: Divergence testing — run old vs new implementations (or oracle vs implementation) over an input corpus and diff outputs. Every divergence gets a ruling: bug or intended behavior change. Nothing is ignored.
argument-hint: "<old-ref> <new-ref> e.g. 'main' 'HEAD' — for refactors/migrations/rewrites"
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "Agent"]
---

# Differential Testing (Old vs New, Oracle vs Impl)

Two implementations and a comparator. Use during refactors, migrations, rewrites, and optimizations; or whenever a slow-but-obviously-correct oracle exists.

## Instructions

### Mode A: Old-vs-New (refactor / migration / rewrite)

1. **Build an input corpus**: production traces/samples, existing fixtures, property-generated inputs (`/test-property`), hand-picked edges.
2. **Run BOTH implementations** over the corpus — shim the new one behind the old interface.
3. **Diff outputs** (plus timing/memory deltas for optimization claims).
4. **Rule on every divergence**:
   - **bug** → fix the new code, add a regression test with the diverging input, or
   - **intended behavior change** → document it, update consumers.
   No divergence is ignored, and the old code is not deleted until every divergence has a ruling.
5. **Golden-master variant**: capture old outputs as fixtures first, then assert new == golden. This decouples the new code's CI from the old code's continued existence.

### Mode B: Oracle-vs-Impl

When a slow-but-obviously-correct oracle exists (brute force, reference implementation, spec pseudocode): assert `impl(x) == oracle(x)` over generated inputs.

When no oracle exists, do NOT invent a fake one — fall back to invariants and metamorphic relations (`/test-property`).

### Output: Divergence Report

```
| Input | Old output | New output | Ruling (bug / intended) | Ticket |
|-------|-----------|-----------|------------------------|-------|
```

Details: `skills/test-strategy/references/enhancement-capabilities.md` §11.
