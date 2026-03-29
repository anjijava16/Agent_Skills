#!/usr/bin/env python3
"""Run an evalset against CSV analysis outputs and grade results."""
import argparse
import json
import re
import sys
from pathlib import Path

import yaml


def load_config(path: str = "config.yaml") -> dict:
    return yaml.safe_load(Path(path).read_text())


def load_evalset(path: str) -> list[dict]:
    return json.loads(Path(path).read_text())


def check_strict(expected: str, actual: str) -> bool:
    """Compare extracted numbers between expected and actual."""
    expected_nums = set(re.findall(r"[\d,]+\.?\d*", expected))
    actual_nums = set(re.findall(r"[\d,]+\.?\d*", actual))
    if not expected_nums:
        return expected.strip().lower() in actual.lower()
    return bool(expected_nums & actual_nums)


def check_fuzzy(expected: str, actual: str) -> bool:
    """Keyword overlap check — replace with LLM judge for production."""
    expected_words = set(expected.lower().split())
    actual_words = set(actual.lower().split())
    if not expected_words:
        return True
    overlap = len(expected_words & actual_words) / len(expected_words)
    return overlap > 0.5


def grade_case(case: dict, actual: str, config: dict) -> dict:
    strict_keys = set(config.get("grading", {}).get("strict_match_keys", []))
    threshold = config.get("grading", {}).get("pass_threshold", 0.8)
    score = 0
    total = len(case["rubric"])
    details = {}
    for key in case["rubric"]:
        if key in strict_keys:
            passed = check_strict(case["expected"], actual)
        else:
            passed = check_fuzzy(case["expected"], actual)
        details[key] = passed
        score += int(passed)
    pct = score / total if total else 0
    return {
        "id": case["id"],
        "score": round(pct, 4),
        "passed": pct >= threshold,
        "details": details,
    }


def main():
    parser = argparse.ArgumentParser(description="Run CSV analysis eval")
    parser.add_argument("--evalset", required=True, help="Path to evalset JSON")
    parser.add_argument("--answers", required=True, help="Path to answers JSON (id→text)")
    parser.add_argument("--config", default="config.yaml", help="Workspace config")
    parser.add_argument("--output", default=None, help="Output results JSON")
    args = parser.parse_args()

    config = load_config(args.config)
    cases = load_evalset(args.evalset)
    answers = json.loads(Path(args.answers).read_text())

    results = []
    for case in cases:
        actual = answers.get(case["id"], "")
        results.append(grade_case(case, actual, config))

    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    summary = {
        "evalset": args.evalset,
        "total": total,
        "passed": passed,
        "pass_rate": round(passed / total, 4) if total else 0,
        "results": results,
    }

    output_text = json.dumps(summary, indent=2)
    if args.output and args.output != "/dev/null":
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(output_text)
        print(f"Results written to {args.output}")
    else:
        print(output_text)

    print(f"\nPassed: {passed}/{total} ({summary['pass_rate']:.1%})")
    sys.exit(0 if summary["pass_rate"] >= config.get("grading", {}).get("pass_threshold", 0.8) else 1)


if __name__ == "__main__":
    main()
