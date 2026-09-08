# roadmap/

Directional, not a committed schedule. Each phase adds one axis of real-world difficulty back into the benchmark, deliberately, one at a time — see [RESEARCH.md](../RESEARCH.md) for why the first phase strips all of them out.

## Phase 0 — synthetic ground truth (current)

`benchmarks/chromatic-universe-v1/`. Exact ground truth, no sensor noise, no actuation error. Measures research behavior in isolation: hypothesis quality, evidence discipline, query efficiency, revision correctness.

## Phase 1 — noisy synthetic

Same environment class, but observations carry realistic measurement noise and the harness no longer reveals a clean signal. Tests whether an entrant's evidence discipline holds up when "what did I actually measure" becomes a real question, not a given.

## Phase 2 — sensors and electronics

Real hardware in the loop: real sensors with real noise floors, real actuators with real latency and failure modes. LORE now includes hardware-specific calibration history, not just abstract observations.

## Phase 3 — materials / agriculture

Systems with slow feedback loops (hours to weeks, not milliseconds) and irreversible actions — an experiment run wrong can't simply be re-run with different parameters a second later. Tests planning under evidence that arrives slowly and actions that can't be undone.

## Phase 4 — complete physical systems, matched constraints

The long-term direction named in the project's public announcement: several autonomous systems given the same resource budget (area, water, energy, time) and the same task, each bringing its own KEY, sensors, and control strategy. Scored on verified physical outcome, not benchmark score.

## What triggers moving to the next phase

Not a date. A phase advances when: (a) the current phase's harness and scoring are stable enough that entrant results are reproducible and comparable, and (b) at least one real entrant has posted a result worth trying to beat. Moving to Phase 1 before Phase 0 has real registered entrants would just be adding difficulty to a benchmark no one has actually run yet.
