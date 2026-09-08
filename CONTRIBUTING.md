# CONTRIBUTING

You do not have to use any particular architecture. There is no reference implementation in this repository to extend or improve on — see [ARCHITECTURE.md](ARCHITECTURE.md). Contributions here fall into two different categories; read the right one.

## Bringing a competing entrant (KEY)

Your entrant's source does not need to live in this repository, and does not need to be public at all. What's required to register a result is that the harness can independently re-check it:

1. Fork or clone `benchmarks/<benchmark-id>/`.
2. Implement the KEY interface described in that benchmark's `README.md` against your own architecture — anywhere you like, in any language, open or closed.
3. Run the benchmark harness locally against your KEY. It produces a signed result record containing: which BASE/LORE state you ran against, what your KEY claimed, and the evidence trail the harness independently verified.
4. Open a PR adding your result record under `competitors/` (see `competitors/README.md` for the exact format) — this registers your entrant on the public leaderboard for that benchmark. The PR needs only your result record and a pointer (a name, a link if you have one, or nothing beyond a label) to your entrant — not your source code.

If you disagree with how a benchmark is scored, or believe it has a gap that lets a weak KEY look strong (or a strong KEY look weak), open an issue. Benchmark rule changes are versioned (`chromatic-universe-v1`, `v2`, ...) so past results stay comparable within their own version.

## Contributing to the protocol itself

This includes: benchmark environments, the BASE/LORE/KEY schemas, the evidence-verification harness, documentation, and the roadmap toward physical benchmarks.

1. Open an issue describing the gap or proposal before a large PR — this project is early enough that direction changes are cheap now and expensive later.
2. Any change to an existing benchmark's scoring rules requires a version bump (`v1` → `v2`), not an in-place edit — past entrant results must remain valid against the version they were run under.
3. Schema/contract changes need a migration note for anything that already has recorded results against the old shape.

## What we're not looking for

- PRs that add a specific architecture's implementation into this repository, framed as "the" way to do KUP. Put it in `competitors/` as an entrant instead.
- Claims of a benchmark result without a re-checkable evidence trail. See [MANIFESTO.md](MANIFESTO.md): the model may propose, evidence decides what gets remembered.
- Scope creep toward a general LMS, certificate system, or anything that turns this into a syllabus rather than a benchmark.

## Code of conduct

Disagree with the benchmark design, the scoring, or another entrant's approach as much as you want — that's the point. Don't misrepresent your own results, don't misrepresent someone else's, and don't submit a result you can't reproduce if asked.
