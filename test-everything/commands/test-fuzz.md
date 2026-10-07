---
name: test-fuzz
description: LLM-crafted adversarial seed corpora fed into deterministic fuzzing engines (go-fuzz, atheris, jazzer, cargo-fuzz). Every crash/timeout/OOM becomes a minimized, deterministic regression test.
argument-hint: "[parser-or-decoder-target]"
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "Agent", "WebSearch"]
---

# Fuzz Testing (LLM Adversarial Inputs, Deterministic Engines)

Division of labor: **the LLM invents adversarial input CLASSES and seed corpora; the fuzzing engine executes deterministically.**

## Instructions

### Step 1: Identify the Boundary

Parsers, deserializers, protocol decoders, file importers — anywhere untrusted bytes become structures.

### Step 2: Write the Harness

The harness is a deterministic artifact, reviewed like production code:

| Stack | Tool |
|---|---|
| Go | `go-fuzz` build artifact or native `FuzzXxx` with seed corpus in `testdata/fuzz` |
| Python | `atheris` (`atheris.instrument_all(); atheris.Fuzz().Fuzz(my_func)`) |
| JVM | Jazzer (`com.code_intelligence.jazzer.api.FuzzTest`) |
| Rust | `cargo fuzz init` / `cargo fuzz target` libFuzzer harnesses |

Use WebSearch to confirm current harness APIs if unsure.

### Step 3: Seed with LLM-Crafted Adversarial Classes

The LLM writes the seed generator; the engine mutates from there. Seed classes:

- **Unicode edge cases**: combining chars, RTL, astral planes
- **Deep nesting**
- **Integer boundaries**: INT_MAX/MIN, off-by-one lengths
- **Malformed encodings**: truncated UTF-8, lone surrogates
- **Protocol confusion**: HTTP in TLS, ZIP-in-ZIP
- **Oversized inputs**, empty/short truncations, hostile-but-valid headers

### Step 4: Run a Bounded Campaign

Fixed time or execution budget in CI **nightly** (not the PR gate) — e.g. 10–30 min per target.

### Step 5: File Findings as Minimized Regressions

Every crash / timeout / OOM / leak gets a **minimized input checked into the regular suite** as a deterministic regression test. **Fuzz findings must reproduce deterministically or they are not filed.**

### Step 6: Track

Corpus growth, unique crashers, coverage-over-time per target.

Details: `skills/test-strategy/references/enhancement-capabilities.md` §12.
