# competitors/

This directory is the public leaderboard. It contains **result records**, not source code — an entrant's KEY does not need to be open-sourced to register a result here (see [ARCHITECTURE.md](../ARCHITECTURE.md) and [CONTRIBUTING.md](../CONTRIBUTING.md)).

## Registering a result

One file per entrant per benchmark version: `competitors/<benchmark-id>/<your-entrant-name>.yaml`.

Draft shape (finalizes alongside the first real harness):

```yaml
entrantName: your-entrant-name
benchmarkId: chromatic-universe-v1
keyDescription: "one paragraph -- architecture family, not implementation detail"
sourceRef: null   # optional: a link, if you're making yours public. Not required.
runDate: 2026-01-01
harnessVersion: "1.0.0"
resultRecord:
  accuracy: null
  evidenceDiscipline: null
  queryEfficiency: null
  revisionCorrectness: null
evidenceTrail: null   # harness-generated, re-checkable, attached automatically by the run
```

A PR adding an entry here must include the harness-generated `evidenceTrail` — a hand-written result record without one will not be merged. This is the same evidence contract every other part of KUP holds itself to (see [MANIFESTO.md](../MANIFESTO.md)): the model may propose, evidence decides what gets remembered, and that includes leaderboard entries.

## No entrant is the reference

Nothing in this repository is the "official" or "default" way to build a KEY. If a maintainer of this repo also registers a result here, it is scored under exactly the same rules as every other entry, with no privileged position.
