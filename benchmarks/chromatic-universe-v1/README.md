# chromatic-universe-v1

The first KUP benchmark. A fully synthetic universe with exact, harness-known ground truth — chosen specifically so research *behavior* can be scored with zero ambiguity about what the correct answer actually was, before anyone brings the same architecture to a physical experiment.

**Status: executable 0.0.1 kernel; richer v1 environment/scoring remains draft.** Issue #1 implements the minimum OBSERVE → HYPOTHESIZE → TEST → MEASURE → REVISE loop with one seeded hidden combination rule, one conformance KEY fixture, and one schema-valid result record. Hidden variables, contradictory observations, weighted scoring, multi-entrant comparison, and leaderboard population remain out of scope for 0.0.1.

## 0.0.1 executable kernel

The 0.0.1 harness is intentionally smaller than the full benchmark described below.

```text
seed
↓
harness-owned hidden combination rule
↓
JSONL KEY protocol in a separate process
↓
OBSERVE / HYPOTHESIZE / TEST / MEASURE / REVISE
↓
final CLAIM
↓
post-claim evaluator reads ground truth
↓
canonical JSON result record + evidence trail
```

The KEY-facing protocol receives the palette and measurement outcomes, not the seed or hidden ground-truth rule. The harness reads ground truth only after the KEY has submitted its final claim and terminated. This is an interface boundary, not an adversarial OS sandbox.

`keys/conformance_key.py` is a deterministic exhaustive protocol fixture used only to prove that the harness works end to end. It is **not** a reference architecture and is **not** a leaderboard entrant; `ARCHITECTURE.md` remains authoritative that KUP does not prescribe a reference KEY.

Run the four executable acceptance checks in [`ACCEPTANCE.md`](ACCEPTANCE.md). A generated seed-17 result is committed under `runs/` as a concrete evidence artifact for this revision.

## The environment

A world of discrete color states with:

- **base states** — a fixed palette of primitive colors
- **combination rules** — how states combine into new states (not all pairs are valid; not all valid combinations are obvious)
- **transitions** — how a state changes over time or in response to an action, including transitions that only apply under conditions the entrant hasn't observed yet
- **hidden variables** — rules that affect outcomes but are never directly observable, only inferable from repeated experiment
- **contradictory-looking observations** — states that appear to violate an entrant's current model until a hidden variable is accounted for

The harness knows the true rule set. The entrant does not, and is not shown it under any circumstances during a run.

## The loop an entrant is scored on

```
OBSERVE   -- query the environment's current state (bounded query budget per run)
HYPOTHESIZE -- propose a rule explaining observed behavior
TEST      -- request a specific experiment (e.g. "combine X and Y under condition Z")
MEASURE   -- receive the real outcome from the harness
REVISE    -- update or discard the hypothesis; write evidence-backed claims to LORE
```

This repeats for a fixed budget (queries, experiments, or wall-clock time — declared per run). At the end, the entrant's final claimed rule set is checked against the harness's true rule set.

## Scoring (draft -- not final)

- **Accuracy**: how much of the entrant's final claimed rule set matches ground truth.
- **Evidence discipline**: what fraction of claims written to LORE during the run were actually supported by the measurement that accompanied them, vs. asserted without a matching test.
- **Query efficiency**: ground-truth accuracy achieved per unit of OBSERVE/TEST budget spent — rewards hypotheses that target real uncertainty, not confirmation of what's already believed.
- **Revision correctness**: when a new measurement contradicts an existing LORE entry, was that entry actually revised, or silently left standing alongside the contradiction?

Exact scoring weights and the query-budget schedule are not final — see CONTRIBUTING.md for how to propose changes before v1 results start being recorded, since scoring changes after that require a version bump.

## What this benchmark does not claim to measure

Performance here says nothing about physical competence — sensor noise, actuation error, and real-world confounds don't exist in a synthetic universe. `chromatic-universe-v1` measures research behavior in isolation from physical execution risk; see `roadmap/` for how later benchmark versions add that back in deliberately, one axis at a time.

## Interfaces (draft)

- `KEY` interface: 0.0.1 uses a JSONL subprocess protocol with `OBSERVE`, `HYPOTHESIZE`, `TEST`, `REVISE`, and final `CLAIM`. Richer v1 signatures remain draft until later benchmark versions require them.
- Result record format: 0.0.1 is defined by `schema/result-record.schema.json`; leaderboard records remain governed by `competitors/README.md` when multi-entrant scoring lands.
