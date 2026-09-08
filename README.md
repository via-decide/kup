# KUP

**Local research intelligence, tested against reality.**

KUP is an experimental framework for building and comparing intelligence systems that can operate locally, accumulate evidence, form hypotheses, test them, learn from failure, and carry verified knowledge forward.

There is no reference implementation in this repository. This repo defines the protocol, the benchmark, and the invitation — not a specific architecture. See [CONTRIBUTING.md](CONTRIBUTING.md) for how to bring your own.

The long-term goal is to move AI evaluation beyond answers and benchmarks into complete physical loops:

```
OBSERVE → REASON → ACT → MEASURE → LEARN
```

We begin with controlled synthetic research environments where ground truth is exact. We then progressively move toward sensors, electronics, agriculture, materials, and other physical systems.

If your architecture can do this better, bring it.

## Why local?

Local execution is not an aesthetic preference in KUP. It is part of the test.

A deployed system should arrive prepared with the models, knowledge, tools, and reasoning capability required for its task. If a system encounters every difficult state by asking an external intelligence what to do next, the benchmark is measuring access to that external intelligence — not the preparation and capability of the submitted system.

## Bring your own intelligence

You can participate with:

- a GraphRAG architecture
- a symbolic reasoning system
- a local LLM agent
- classical ML
- control algorithms
- hybrid physics/AI systems
- an architecture that does not resemble any of these

The objective is not to make any one approach win. The objective is to discover what actually works.

## Where this is going

Today AI systems are often compared on questions, datasets, and model benchmarks. KUP ultimately wants to compare complete systems operating in the same physical world.

Imagine several autonomous growing systems receiving the same crop, area, water, energy, and time budget. Each team brings its own local intelligence, sensors, control strategy, and engineering stack. The winner is not the system with the highest benchmark score — the winner is the system that produces the strongest verified physical result.

Motorsport helped improve ordinary vehicles by forcing complete engineering systems to compete. KUP wants to explore whether a similar culture can accelerate useful physical AI.

## Status

KUP is not being published as a finished answer. It is being published as a place to test the question.

- [MANIFESTO.md](MANIFESTO.md) — the invariant this whole project is built on
- [RESEARCH.md](RESEARCH.md) — what is actually being investigated
- [ARCHITECTURE.md](ARCHITECTURE.md) — BASE / LORE / KEY, and why no reference implementation ships here
- [CONTRIBUTING.md](CONTRIBUTING.md) — how to bring a competing system
- [benchmarks/chromatic-universe-v1/](benchmarks/chromatic-universe-v1/) — the first benchmark
- [roadmap/](roadmap/) — where this goes after the synthetic benchmark

## Ecosystem

KUP does not try to own every layer of this itself. When a KUP project or entrant is missing a representation it needs — not code, the underlying understanding — that gap is meant to be filled by a dedicated capability graph rather than re-derived ad hoc inside this repo:

- **[via-decide/kup-curriculum](https://github.com/via-decide/kup-curriculum)** — the canonical KUP learning graph. Representation-first, not a syllabus: every concept connects an equation/representation to its physical meaning, a cross-domain bridge, a simulation, a measurement, and an unresolved question. `KUP PROJECT → required capability → missing representation? → kup-curriculum → bounded learning path → new reusable capability → back to project.`

Other repositories in the broader `via-decide` organization support parts of this work but aren't yet reviewed for public linkage from here — this section grows deliberately, not by default.

## Get started

```
git clone <this-repo>
cd kup
cat benchmarks/chromatic-universe-v1/README.md
```

There is a reproducible local benchmark, and anyone can bring another system to attempt it.
