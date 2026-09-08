# KUP 0.0.1 acceptance commands

Install the test-only schema validator once:

```bash
python -m pip install -r benchmarks/chromatic-universe-v1/requirements-dev.txt
```

Then run the four acceptance criteria independently from the repository root:

```bash
python benchmarks/chromatic-universe-v1/tests/test_local_only.py
python benchmarks/chromatic-universe-v1/tests/test_deterministic_seed.py
python benchmarks/chromatic-universe-v1/tests/test_hidden_rule.py
python benchmarks/chromatic-universe-v1/tests/test_result_schema.py
```

All four must exit `0` in the same revision. These are executable checks, not PR-description assertions.

To generate a result directly:

```bash
python benchmarks/chromatic-universe-v1/harness.py \
  --seed 17 \
  --key benchmarks/chromatic-universe-v1/keys/conformance_key.py \
  --deny-network \
  --output benchmarks/chromatic-universe-v1/runs/example-seed-17.json
```

`conformance_key.py` exists only to prove the harness contract can execute. It is not a reference KEY architecture and is not a leaderboard entrant.
