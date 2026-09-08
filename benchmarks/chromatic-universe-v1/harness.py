from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any

from environment import ChromaticEnvironment

BENCHMARK_ID = "chromatic-universe-v1"
HARNESS_VERSION = "0.0.1"
PROTOCOL_VERSION = "0.0.1"
MAX_ACTIONS = 64


def canonical_json_bytes(record: dict[str, Any]) -> bytes:
    return (json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode("utf-8")


def _send(proc: subprocess.Popen[str], payload: dict[str, Any]) -> None:
    if proc.stdin is None:
        raise RuntimeError("KEY stdin unavailable")
    proc.stdin.write(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n")
    proc.stdin.flush()


def _read_action(proc: subprocess.Popen[str]) -> dict[str, Any]:
    if proc.stdout is None:
        raise RuntimeError("KEY stdout unavailable")
    line = proc.stdout.readline()
    if not line:
        stderr = proc.stderr.read() if proc.stderr else ""
        raise RuntimeError(f"KEY terminated before CLAIM; stderr={stderr!r}")
    try:
        action = json.loads(line)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"KEY emitted non-JSON protocol line: {line!r}") from exc
    if not isinstance(action, dict):
        raise RuntimeError("KEY action must be a JSON object")
    return action


def _key_env(deny_network: bool) -> dict[str, str]:
    env = os.environ.copy()
    env.pop("KUP_SEED", None)
    env.pop("KUP_HIDDEN_RULE", None)
    env["KUP_NETWORK_MODE"] = "DENIED" if deny_network else "UNRESTRICTED"
    return env


def _key_command(key_path: Path, deny_network: bool, benchmark_dir: Path) -> list[str]:
    if not deny_network:
        return [sys.executable, str(key_path)]
    guard_dir = str(benchmark_dir / "network_guard")
    wrapper = (
        "import runpy,sys; "
        f"sys.path.insert(0,{guard_dir!r}); "
        "from guard import install; install(); "
        "runpy.run_path(sys.argv[1], run_name='__main__')"
    )
    return [sys.executable, "-c", wrapper, str(key_path)]


def run_benchmark(seed: int, key_path: Path, output_path: Path, deny_network: bool) -> dict[str, Any]:
    benchmark_dir = Path(__file__).resolve().parent

    if deny_network:
        sys.path.insert(0, str(benchmark_dir / "network_guard"))
        from guard import install
        install()

    environment = ChromaticEnvironment(seed)
    key_command = _key_command(key_path, deny_network, benchmark_dir)
    proc = subprocess.Popen(
        key_command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        env=_key_env(deny_network),
    )

    start_payload = {
        "type": "START",
        "protocolVersion": PROTOCOL_VERSION,
        "benchmarkId": BENCHMARK_ID,
        "palette": list(environment.palette),
        "claimContract": {
            "ruleType": "single-special-combination",
            "commutative": True,
            "defaultOutcome": "NO_REACTION",
            "inputsMustBeSorted": True,
        },
    }
    _send(proc, start_payload)

    evidence_trail: list[dict[str, Any]] = []
    final_claim: dict[str, Any] | None = None
    sequence = 0
    observe_count = 0
    test_count = 0

    try:
        for _ in range(MAX_ACTIONS):
            action = _read_action(proc)
            action_type = action.get("type")
            sequence += 1

            if action_type == "OBSERVE":
                observe_count += 1
                response = {
                    "type": "OBSERVATION",
                    "palette": list(environment.palette),
                    "observeIndex": observe_count,
                }
                evidence_trail.append({
                    "sequence": sequence,
                    "phase": "OBSERVE",
                    "request": {"type": "OBSERVE"},
                    "response": response,
                })
                _send(proc, response)

            elif action_type == "HYPOTHESIZE":
                hypothesis = action.get("hypothesis")
                if not isinstance(hypothesis, dict):
                    raise RuntimeError("HYPOTHESIZE requires an object field 'hypothesis'")
                evidence_trail.append({
                    "sequence": sequence,
                    "phase": "HYPOTHESIZE",
                    "request": {"type": "HYPOTHESIZE", "hypothesis": hypothesis},
                })

            elif action_type == "TEST":
                left = action.get("left")
                right = action.get("right")
                if not isinstance(left, str) or not isinstance(right, str):
                    raise RuntimeError("TEST requires string fields 'left' and 'right'")
                outcome = environment.combine(left, right)
                test_count += 1
                evidence_ref = f"evidence-{test_count:04d}"
                response = {
                    "type": "MEASUREMENT",
                    "left": left,
                    "right": right,
                    "outcome": outcome,
                    "evidenceRef": evidence_ref,
                    "testIndex": test_count,
                }
                evidence_trail.append({
                    "sequence": sequence,
                    "phase": "TEST",
                    "request": {"type": "TEST", "left": left, "right": right},
                    "response": response,
                    "evidenceRef": evidence_ref,
                })
                _send(proc, response)

            elif action_type == "REVISE":
                revision = action.get("revision")
                evidence_refs = action.get("evidenceRefs")
                if not isinstance(revision, dict):
                    raise RuntimeError("REVISE requires an object field 'revision'")
                if not isinstance(evidence_refs, list) or not all(isinstance(x, str) for x in evidence_refs):
                    raise RuntimeError("REVISE requires string array field 'evidenceRefs'")
                evidence_trail.append({
                    "sequence": sequence,
                    "phase": "REVISE",
                    "request": {
                        "type": "REVISE",
                        "revision": revision,
                        "evidenceRefs": evidence_refs,
                    },
                })

            elif action_type == "CLAIM":
                claim = action.get("rule")
                if not isinstance(claim, dict):
                    raise RuntimeError("CLAIM requires object field 'rule'")
                final_claim = claim
                evidence_trail.append({
                    "sequence": sequence,
                    "phase": "CLAIM",
                    "request": {"type": "CLAIM", "rule": final_claim},
                })
                break

            else:
                raise RuntimeError(f"unknown KEY action type: {action_type!r}")
        else:
            raise RuntimeError(f"KEY exceeded MAX_ACTIONS={MAX_ACTIONS} without CLAIM")
    finally:
        if proc.stdin:
            proc.stdin.close()

    try:
        return_code = proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait(timeout=5)
        raise RuntimeError("KEY did not terminate after CLAIM")

    if return_code != 0:
        stderr = proc.stderr.read() if proc.stderr else ""
        raise RuntimeError(f"KEY exited with code {return_code}; stderr={stderr!r}")
    if final_claim is None:
        raise RuntimeError("KEY never submitted a final claim")

    ground_truth = environment.ground_truth_record()
    exact_match = final_claim == ground_truth

    record = {
        "schemaVersion": "0.0.1",
        "benchmarkId": BENCHMARK_ID,
        "harnessVersion": HARNESS_VERSION,
        "seed": seed,
        "key": {
            "name": "kup-0.0.1-conformance-key",
            "description": "Deterministic exhaustive protocol fixture; not a reference architecture or leaderboard entrant.",
            "sourceRef": "keys/conformance_key.py",
        },
        "execution": {
            "networkMode": "DENIED" if deny_network else "UNRESTRICTED",
            "observeCount": observe_count,
            "testCount": test_count,
        },
        "finalClaimedRule": final_claim,
        "groundTruthRule": ground_truth,
        "comparison": {"exactMatch": exact_match},
        "passed": exact_match,
        "evidenceTrail": evidence_trail,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(canonical_json_bytes(record))
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description="KUP 0.0.1 chromatic-universe harness")
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument(
        "--key",
        type=Path,
        default=Path(__file__).resolve().parent / "keys" / "conformance_key.py",
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--deny-network", action="store_true")
    args = parser.parse_args()

    run_benchmark(args.seed, args.key.resolve(), args.output.resolve(), args.deny_network)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
