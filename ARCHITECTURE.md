# ARCHITECTURE

This document defines the interfaces an entrant must implement to run against a KUP benchmark. It does not define, recommend, or ship a reference architecture. **There is no reference implementation in this repository.** See [competitors/README.md](competitors/README.md) for how entrants register themselves.

This separation is deliberate: KUP is the protocol and the benchmark, not any one system's implementation of a solution to it. Keeping this repo free of a specific architecture is what keeps the benchmark neutral.

## The three primitives, as interfaces

### BASE

What an entrant has access to before a run starts: datasets, tools, local models, sensors (in physical-phase benchmarks), and declared resource limits (compute, memory, wall-clock, energy where applicable). BASE is fixed by the benchmark definition, not chosen by the entrant — every entrant in a given run receives the same BASE.

### LORE

The accumulated evidence record: prior observations, prior hypotheses, which were confirmed, which failed, and why. LORE is structured, provenance-tagged evidence — not free-text notes. A benchmark run specifies whether entrants start with empty LORE or a shared prior LORE state; either way, every entrant in that run starts from the same LORE.

### KEY

The entrant's own architecture: however it interprets BASE and LORE, forms hypotheses, selects tests, and decides what to write back into LORE. This is the only primitive that varies between entrants. A KEY can be a GraphRAG system, a symbolic reasoner, a local LLM agent, classical ML, a control algorithm, a hybrid physics/AI system, or something that doesn't resemble any current category.

## The evidence contract

A KEY may write a claim into LORE only alongside the evidence that produced it: what was tested, what was measured, and how the measurement was obtained. A benchmark harness must be able to independently re-check that evidence against the environment's ground truth (synthetic phase) or a defined measurement procedure (physical phase). Claims without a re-checkable evidence trail are rejected by the harness before they reach the entrant's score — they never need to be argued about, because they never entered LORE.

## Why local execution is architecturally required

An entrant's KEY must be able to complete a full OBSERVE → HYPOTHESIZE → TEST → MEASURE → REVISE cycle without a live query to a more-capable external system during the timed portion of a run. This is not a deployment preference — it is what the benchmark is measuring. A KEY that depends on an external system's live reasoning during execution is being scored on that external system's capability, not its own preparation. Retrieval from an entrant's own pre-loaded local knowledge (its own BASE/LORE) is not an external dependency; a live API call to a third-party model during the timed run is.

## Registering an entrant

See [CONTRIBUTING.md](CONTRIBUTING.md). An entrant's source does not need to live in this repository — `competitors/README.md` explains the registration format (a pointer to your own repo, a declared BASE/LORE/KEY mapping, and the benchmark results it has produced), so no one is required to open-source their own KEY to participate in the comparison, only to make its claims re-checkable by the harness.
