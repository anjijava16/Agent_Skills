#!/usr/bin/env python3
"""Compare two eval run results and report deltas."""
import json
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 3:
        print("Usage: compare_runs.py <baseline.json> <candidate.json>")
        sys.exit(1)

    baseline = json.loads(Path(sys.argv[1]).read_text())
    candidate = json.loads(Path(sys.argv[2]).read_text())

    b_map = {r["id"]: r for r in baseline["results"]}
    c_map = {r["id"]: r for r in candidate["results"]}

    all_ids = sorted(set(b_map) | set(c_map))
    regressions = []
    new_passes = []

    for case_id in all_ids:
        b_passed = b_map.get(case_id, {}).get("passed", False)
        c_passed = c_map.get(case_id, {}).get("passed", False)
        if b_passed and not c_passed:
            regressions.append(case_id)
        elif not b_passed and c_passed:
            new_passes.append(case_id)

    b_rate = baseline.get("pass_rate", 0) * 100
    c_rate = candidate.get("pass_rate", 0) * 100
    delta = c_rate - b_rate

    print(f"Test Cases:  {len(all_ids)}")
    print(f"Baseline:    {baseline['passed']}/{baseline['total']} ({b_rate:.1f}%)")
    print(f"Candidate:   {candidate['passed']}/{candidate['total']} ({c_rate:.1f}%)")
    print(f"Delta:       {'+' if delta >= 0 else ''}{delta:.1f}%")
    print(f"\nRegressions: {len(regressions)}")
    if regressions:
        print(f"  {', '.join(regressions)}")
    print(f"New Passes:  {len(new_passes)}")
    if new_passes:
        print(f"  {', '.join(new_passes)}")


if __name__ == "__main__":
    main()
