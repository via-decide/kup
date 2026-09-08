from __future__ import annotations

from itertools import combinations
import json
import sys
from typing import Any


def send(payload: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n")
    sys.stdout.flush()


def receive() -> dict[str, Any]:
    line = sys.stdin.readline()
    if not line:
        raise RuntimeError("harness closed protocol stream")
    payload = json.loads(line)
    if not isinstance(payload, dict):
        raise RuntimeError("protocol payload must be an object")
    return payload


def main() -> int:
    start = receive()
    if set(start) != {"type", "protocolVersion", "benchmarkId", "palette", "claimContract"}:
        raise RuntimeError("unexpected START interface fields")
    if start["type"] != "START":
        raise RuntimeError("expected START")

    palette = start["palette"]
    if not isinstance(palette, list) or not all(isinstance(x, str) for x in palette):
        raise RuntimeError("invalid palette")

    send({"type": "OBSERVE"})
    observation = receive()
    if observation.get("type") != "OBSERVATION":
        raise RuntimeError("expected OBSERVATION")

    pairs = [tuple(pair) for pair in combinations(palette, 2)]
    send({
        "type": "HYPOTHESIZE",
        "hypothesis": {
            "statement": "Exactly one unordered pair produces a non-default outcome; test every pair.",
            "candidateCount": len(pairs),
        },
    })

    discovered_pair: tuple[str, str] | None = None
    discovered_output: str | None = None
    evidence_refs: list[str] = []

    for index, (left, right) in enumerate(pairs, start=1):
        send({"type": "TEST", "left": left, "right": right})
        measurement = receive()
        if measurement.get("type") != "MEASUREMENT":
            raise RuntimeError("expected MEASUREMENT")
        evidence_ref = measurement.get("evidenceRef")
        if not isinstance(evidence_ref, str):
            raise RuntimeError("measurement missing evidenceRef")
        evidence_refs.append(evidence_ref)
        outcome = measurement.get("outcome")
        if outcome != "NO_REACTION":
            discovered_pair = tuple(sorted((left, right)))
            discovered_output = str(outcome)

        send({
            "type": "REVISE",
            "revision": {
                "testsCompleted": index,
                "specialPairFound": discovered_pair is not None,
            },
            "evidenceRefs": list(evidence_refs),
        })

    if discovered_pair is None or discovered_output is None:
        raise RuntimeError("conformance KEY did not find the single special combination")

    send({
        "type": "CLAIM",
        "rule": {
            "ruleType": "single-special-combination",
            "inputs": list(discovered_pair),
            "output": discovered_output,
            "defaultOutcome": "NO_REACTION",
            "commutative": True,
        },
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
