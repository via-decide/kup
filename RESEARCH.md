# RESEARCH

This document states what is actually being investigated — not what KUP hopes to eventually claim.

## The core research loop

```
BASE + LORE + KEY
      ↓
LOCAL RESEARCH SYSTEM
      ↓
  OBSERVE
      ↓
  HYPOTHESIZE
      ↓
  TEST
      ↓
  MEASURE
      ↓
  REVISE
      ↓
  NEW LORE
```

Every entrant, regardless of architecture, is evaluated on this loop — not on a single answer to a single question.

## The three primitives

```
KUP
├── BASE   what exists locally: datasets, tools, models, sensors, experiments, and available resources
├── LORE   what previous experiments taught: evidence, failures, recoveries, contradictions, and provenance
└── KEY    how a particular intelligence interprets, tests, and acts on that world
```

Different entrants can share the same BASE and the same accumulated LORE (subject to the benchmark rules for a given run) while bringing entirely different KEYs. This is the point: the benchmark exists to compare KEYs under identical conditions, not to compare who has the most data.

## What is being measured

For a given research loop, KUP tracks — per architecture, per run:

- how it forms hypotheses given partial observation
- how it chooses what to test next (does it reduce genuine uncertainty, or just confirm what it already believes?)
- whether its measured evidence actually supports what it claims to have learned
- whether prior LORE gets revised correctly when new evidence contradicts it, or whether contradictions get silently dropped
- how it behaves when a hidden variable makes its current model wrong

None of this is measured by asking the system to self-report confidence. It is measured against exact ground truth in the benchmark environment (see `benchmarks/chromatic-universe-v1/`).

## The first environment

The first benchmark uses a fully synthetic, fully known universe: controlled color states, combinations, transitions, hidden variables, and exact ground truth. This is deliberate — a synthetic environment is the only place research behavior can be scored with zero ambiguity about what the "correct" answer actually was.

## Where this goes

Later phases move the same research contracts (the same OBSERVE → HYPOTHESIZE → TEST → MEASURE → REVISE loop, the same evidence requirements) into physical systems: sensors, electronics, materials, and eventually autonomous physical experiments (see [roadmap/](roadmap/)). A system that only performs well in the synthetic environment has not yet demonstrated anything about physical competence — that gap is itself part of what KUP is trying to measure.

## What KUP is explicitly not investigating (yet)

- General-purpose AGI claims
- Whether any specific architecture (including any built by KUP's maintainers) is "the" solution
- Anything requiring continuous access to an external, more-capable model during execution — see [ARCHITECTURE.md](ARCHITECTURE.md) on why local execution is part of the test, not an implementation detail
