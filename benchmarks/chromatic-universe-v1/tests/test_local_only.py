from __future__ import annotations

import subprocess
import unittest

from _helpers import network_probe_command, run_harness


class LocalOnlyAcceptanceTest(unittest.TestCase):
    def test_network_guard_blocks_socket_and_benchmark_still_completes(self) -> None:
        probe = subprocess.run(
            network_probe_command(),
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(probe.returncode, 0, "network guard did not block socket creation")

        _raw, result = run_harness(seed=17, deny_network=True)
        self.assertEqual(result["execution"]["networkMode"], "DENIED")
        self.assertTrue(result["passed"])


if __name__ == "__main__":
    unittest.main()
