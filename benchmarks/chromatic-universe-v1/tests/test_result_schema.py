from __future__ import annotations

import json
import unittest

from jsonschema import Draft202012Validator

from _helpers import SCHEMA, run_harness


class ResultSchemaAcceptanceTest(unittest.TestCase):
    def test_result_record_validates_against_committed_schema(self) -> None:
        _raw, result = run_harness(seed=17, deny_network=True)
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(result)
        self.assertEqual(result["comparison"]["exactMatch"], result["passed"])
        self.assertTrue(result["evidenceTrail"])


if __name__ == "__main__":
    unittest.main()
