import json
import tempfile
import unittest
from pathlib import Path

from promptbeat_lite.cli import evaluate_case, run_suite


class PromptbeatLiteTests(unittest.TestCase):
    def test_evaluates_case_rules(self):
        result = evaluate_case({"id": "a", "output": "hello source", "must_contain": ["source"], "must_not_contain": ["secret"]})
        self.assertTrue(result["passed"])

    def test_suite_counts_failures(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "cases.json"
            path.write_text(json.dumps({"cases": [{"id": "bad", "output": "secret", "must_not_contain": ["secret"]}]}), encoding="utf-8")
            summary = run_suite(str(path))
        self.assertEqual(summary["failed"], 1)


if __name__ == "__main__":
    unittest.main()
