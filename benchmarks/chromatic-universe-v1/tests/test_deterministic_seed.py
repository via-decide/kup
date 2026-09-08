from __future__ import annotations

import unittest

from _helpers import run_harness


class DeterministicSeedAcceptanceTest(unittest.TestCase):
    def test_same_seed_produces_byte_identical_result_record(self) -> None:
        first, _ = run_harness(seed=1701, deny_network=True)
        second, _ = run_harness(seed=1701, deny_network=True)
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
