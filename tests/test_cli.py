import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from promptbeat_lite.cli import evaluate_case, format_junit, load_cases, main, run_suite


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

    def test_must_equal_detects_golden_mismatch(self):
        result = evaluate_case({"id": "golden", "output": "actual", "must_equal": "expected"})

        self.assertFalse(result["passed"])
        self.assertEqual(result["failures"], ["not equal to expected golden output"])

    def test_empty_suite_has_full_pass_rate(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "cases.json"
            path.write_text(json.dumps({"cases": []}), encoding="utf-8")

            summary = run_suite(str(path))

        self.assertEqual(summary["total"], 0)
        self.assertEqual(summary["pass_rate"], 100.0)

    def test_directory_suite_loads_multiple_fixture_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.json").write_text(json.dumps({"cases": [{"id": "a", "output": "ok", "expected": "ok"}]}), encoding="utf-8")
            (root / "nested").mkdir()
            (root / "nested" / "b.json").write_text(json.dumps({"cases": [{"id": "b", "output": "safe", "must_not_contain": ["secret"]}]}), encoding="utf-8")

            summary = run_suite(str(root))

        self.assertEqual(summary["total"], 2)
        self.assertEqual(summary["passed"], 2)

    def test_golden_file_is_loaded_relative_to_fixture(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "golden.txt").write_text("exact answer\n", encoding="utf-8")
            fixture = root / "cases.json"
            fixture.write_text(json.dumps({"cases": [{"id": "golden", "output": "exact answer", "golden_file": "golden.txt"}]}), encoding="utf-8")

            cases = load_cases(str(fixture))
            result = evaluate_case(cases[0])

        self.assertTrue(result["passed"])

    def test_invalid_case_fails_with_schema_issue(self):
        result = evaluate_case({"id": "invalid", "output": "anything"})

        self.assertFalse(result["passed"])
        self.assertIn("missing expectation rule", result["failures"])


if __name__ == "__main__":
    unittest.main()
