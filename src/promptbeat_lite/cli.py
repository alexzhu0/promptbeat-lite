"""Run lightweight prompt regression checks from JSON fixtures."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Sequence


def load_cases(path: str) -> List[Dict[str, Any]]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        payload = payload.get("cases", [])
    return [case for case in payload if isinstance(case, dict)]


def evaluate_case(case: Dict[str, Any]) -> Dict[str, Any]:
    output = str(case.get("output", ""))
    must_contain = [str(item) for item in case.get("must_contain", [])]
    must_not_contain = [str(item) for item in case.get("must_not_contain", [])]
    failures = []
    for item in must_contain:
        if item not in output:
            failures.append(f"missing: {item}")
    for item in must_not_contain:
        if item in output:
            failures.append(f"forbidden: {item}")
    return {"id": case.get("id", "case"), "passed": not failures, "failures": failures}


def run_suite(path: str) -> Dict[str, Any]:
    results = [evaluate_case(case) for case in load_cases(path)]
    passed = sum(1 for result in results if result["passed"])
    return {"total": len(results), "passed": passed, "failed": len(results) - passed, "results": results}


def format_text(summary: Dict[str, Any]) -> str:
    lines = [f"Total: {summary['total']}", f"Passed: {summary['passed']}", f"Failed: {summary['failed']}", ""]
    for result in summary["results"]:
        status = "PASS" if result["passed"] else "FAIL"
        lines.append(f"- {status} {result['id']}: {', '.join(result['failures']) or 'ok'}")
    return "\n".join(lines).rstrip()


def run(input_path: str, output_format: str = "text") -> str:
    summary = run_suite(input_path)
    if output_format == "json":
        return json.dumps(summary, indent=2, sort_keys=True)
    return format_text(summary)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run lightweight prompt regression checks from JSON fixtures.")
    parser.add_argument("input", help="JSON fixtures file")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    print(run(args.input, args.format))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
