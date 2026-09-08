from __future__ import annotations

import unittest

from _helpers import run_harness


class HiddenRuleAcceptanceTest(unittest.TestCase):
    def test_key_facing_responses_expose_outcomes_not_seed_or_ground_truth(self) -> None:
        _raw, result = run_harness(seed=99, deny_network=True)

        for event in result["evidenceTrail"]:
            response = event.get("response")
            if response is None:
                continue
            self.assertNotIn("seed", response)
            self.assertNotIn("rule", response)
            self.assertNotIn("hiddenRule", response)
            self.assertNotIn("groundTruthRule", response)

        test_events = [e for e in result["evidenceTrail"] if e["phase"] == "TEST"]
        self.assertGreater(len(test_events), 0)
        for event in test_events:
            self.assertIn("outcome", event["response"])
            self.assertIn("evidenceRef", event["response"])

        phases = [event["phase"] for event in result["evidenceTrail"]]
        self.assertIn("OBSERVE", phases)
        self.assertIn("HYPOTHESIZE", phases)
        self.assertIn("TEST", phases)
        self.assertIn("REVISE", phases)
        self.assertEqual(phases[-1], "CLAIM")


if __name__ == "__main__":
    unittest.main()
