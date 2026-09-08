from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Any

BENCHMARK_DIR = Path(__file__).resolve().parents[1]
HARNESS = BENCHMARK_DIR / "harness.py"
KEY = BENCHMARK_DIR / "keys" / "conformance_key.py"
SCHEMA = BENCHMARK_DIR / "schema" / "result-record.schema.json"


def run_harness(seed: int = 17, deny_network: bool = True) -> tuple[bytes, dict[str, Any]]:
    with tempfile.TemporaryDirectory() as temp_dir:
        output = Path(temp_dir) / "result.json"
        command = [
            sys.executable,
            str(HARNESS),
            "--seed",
            str(seed),
            "--key",
            str(KEY),
            "--output",
            str(output),
        ]
        if deny_network:
            command.append("--deny-network")
        subprocess.run(command, check=True, cwd=BENCHMARK_DIR)
        raw = output.read_bytes()
        return raw, json.loads(raw)


def network_probe_command() -> list[str]:
    guard_dir = str(BENCHMARK_DIR / "network_guard")
    wrapper = (
        "import sys; "
        f"sys.path.insert(0,{guard_dir!r}); "
        "from guard import install; install(); "
        "import socket; socket.socket()"
    )
    return [sys.executable, "-c", wrapper]
