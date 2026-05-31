import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from promptbeat_lite.cli import evaluate_case, format_junit, main, run_suite


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
        self.assertEqual(summary["pass_rate"], 0)

    def test_eval_case_miner_fixture_shape_is_supported(self):
        result = evaluate_case({"id": "mined", "actual": "The answer cites source A.", "expected": "source A"})

        self.assertTrue(result["passed"])

    def test_junit_output_contains_failures(self):
        summary = {"total": 1, "passed": 0, "failed": 1, "pass_rate": 0, "results": [{"id": "x", "passed": False, "failures": ["missing: citation"]}]}

        output = format_junit(summary)

        self.assertIn("<testsuite", output)
        self.assertIn("<failure", output)

    def test_fail_under_returns_two(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "cases.json"
            path.write_text(json.dumps({"cases": [{"id": "bad", "output": "secret", "must_not_contain": ["secret"]}]}), encoding="utf-8")

            with redirect_stdout(StringIO()):
                code = main([str(path), "--fail-under", "100"])

        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
