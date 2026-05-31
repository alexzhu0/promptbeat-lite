"""Run lightweight prompt regression checks from JSON fixtures."""

from __future__ import annotations

import argparse
import json
import xml.sax.saxutils as xml_escape
from pathlib import Path
from typing import Any, Dict, List, Sequence


def load_cases(path: str) -> List[Dict[str, Any]]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        payload = payload.get("cases", [])
    return [case for case in payload if isinstance(case, dict)]


def evaluate_case(case: Dict[str, Any]) -> Dict[str, Any]:
    output = str(case.get("output", case.get("actual", "")))
    must_contain = [str(item) for item in case.get("must_contain", [])]
    if case.get("expected") and not must_contain:
        must_contain.append(str(case["expected"]))
    must_not_contain = [str(item) for item in case.get("must_not_contain", [])]
    must_equal = case.get("must_equal")
    failures = []
    if must_equal is not None and output != str(must_equal):
        failures.append("not equal to expected golden output")
    for item in must_contain:
        if item not in output:
            failures.append(f"missing: {item}")
    for item in must_not_contain:
        if item in output:
            failures.append(f"forbidden: {item}")
    return {
        "id": case.get("id", "case"),
        "passed": not failures,
        "failures": failures,
        "tags": case.get("tags", []),
    }


def run_suite(path: str) -> Dict[str, Any]:
    results = [evaluate_case(case) for case in load_cases(path)]
    passed = sum(1 for result in results if result["passed"])
    total = len(results)
    pass_rate = round((passed / total) * 100, 2) if total else 100.0
    return {
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "pass_rate": pass_rate,
        "results": results,
    }


def format_text(summary: Dict[str, Any]) -> str:
    lines = [
        f"Total: {summary['total']}",
        f"Passed: {summary['passed']}",
        f"Failed: {summary['failed']}",
        f"Pass rate: {summary['pass_rate']}%",
        "",
    ]
    for result in summary["results"]:
        status = "PASS" if result["passed"] else "FAIL"
        lines.append(f"- {status} {result['id']}: {', '.join(result['failures']) or 'ok'}")
    return "\n".join(lines).rstrip()


def format_junit(summary: Dict[str, Any]) -> str:
    lines = [
        f'<testsuite name="promptbeat-lite" tests="{summary["total"]}" failures="{summary["failed"]}">'
    ]
    for result in summary["results"]:
        case_id = xml_escape.escape(str(result["id"]))
        lines.append(f'  <testcase name="{case_id}">')
        if not result["passed"]:
            failure_text = xml_escape.escape("; ".join(result["failures"]))
            lines.append(f'    <failure message="{failure_text}">{failure_text}</failure>')
        lines.append("  </testcase>")
    lines.append("</testsuite>")
    return "\n".join(lines)


def run(input_path: str, output_format: str = "text") -> str:
    summary = run_suite(input_path)
    if output_format == "json":
        return json.dumps(summary, indent=2, sort_keys=True)
    if output_format == "junit":
        return format_junit(summary)
    return format_text(summary)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run lightweight prompt regression checks from JSON fixtures.")
    parser.add_argument("input", help="JSON fixtures file")
    parser.add_argument("--format", choices=["text", "json", "junit"], default="text")
    parser.add_argument(
        "--fail-under",
        type=float,
        default=None,
        metavar="PERCENT",
        help="Exit with code 2 when pass rate is below this percentage",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    summary = run_suite(args.input)
    if args.format == "json":
        print(json.dumps(summary, indent=2, sort_keys=True))
    elif args.format == "junit":
        print(format_junit(summary))
    else:
        print(format_text(summary))
    if args.fail_under is not None and summary["pass_rate"] < args.fail_under:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
