---
name: csv-analyzer-workspace
description: >-
  Manage a workspace for evaluating and benchmarking CSV analysis quality.
  Use when the user wants to set up eval harnesses, compare analysis outputs
  with and without skills, grade CSV analysis results, or track analysis
  accuracy over time.
---

# CSV Analyzer Workspace

Set up and manage a workspace for evaluating CSV analysis quality, running
benchmarks, and tracking improvements.

## Workspace Structure

Create the workspace with this layout:

```
csv-analyzer-workspace/
├── evalsets/          # Gold-standard question-answer pairs
├── datasets/          # Sample CSV files for evaluation
├── results/           # Eval run outputs
├── scripts/           # Automation helpers
└── config.yaml        # Workspace configuration
```

## Quick Start

1. **Initialise**: Create the workspace structure above.
2. **Add datasets**: Place sample CSV files in `datasets/`.
3. **Write evalsets**: Create JSON files in `evalsets/` (see format below).
4. **Run evals**: Execute the grading script against analysis outputs.
5. **Compare**: Review results in `results/` to measure skill impact.

## Evalset Format

Each evalset is a JSON array of test cases:

```json
[
  {
    "id": "sales-q1",
    "dataset": "datasets/sales_2024.csv",
    "question": "What is the total revenue for Q1?",
    "expected": "Total Q1 revenue is $1,234,567.89",
    "rubric": ["correct_total", "includes_currency", "specifies_quarter"]
  },
  {
    "id": "missing-vals",
    "dataset": "datasets/survey_responses.csv",
    "question": "How many missing values are in the age column?",
    "expected": "There are 42 missing values in the age column.",
    "rubric": ["correct_count", "names_column"]
  }
]
```

### Rubric Keys

| Key                | Meaning                                    |
|--------------------|--------------------------------------------|
| `correct_total`    | Numeric answer matches expected value      |
| `correct_count`    | Count matches expected value               |
| `includes_currency`| Output includes proper currency formatting |
| `names_column`     | Output explicitly names the column         |
| `specifies_quarter`| Output identifies the time period          |
| `lists_steps`      | Output shows analytical steps taken        |

## config.yaml

```yaml
workspace: csv-analyzer-workspace
datasets_dir: datasets
evalsets_dir: evalsets
results_dir: results
grading:
  model: gpt-4o-mini          # LLM judge for open-ended rubrics
  strict_match_keys:           # rubric keys that require exact match
    - correct_total
    - correct_count
  fuzzy_match_keys:            # rubric keys graded by LLM judge
    - includes_currency
    - names_column
    - specifies_quarter
    - lists_steps
  pass_threshold: 0.8          # minimum score to pass a test case
```

## Running Evaluations

### Baseline (no skill)

```bash
python scripts/run_eval.py \
  --evalset evalsets/sales_questions.json \
  --output results/baseline_$(date +%Y%m%d).json
```

### With skill active

```bash
python scripts/run_eval.py \
  --evalset evalsets/sales_questions.json \
  --skill analyze-csv-files \
  --output results/with_skill_$(date +%Y%m%d).json
```

### Compare runs

```bash
python scripts/compare_runs.py \
  results/baseline_20250101.json \
  results/with_skill_20250101.json
```

Output:

```
Test Cases:  12
Baseline:    7/12 (58.3%)
With Skill: 11/12 (91.7%)
Delta:      +33.4%

Regressions: 0
New Passes:  sales-q3, survey-median, outlier-detect, grouped-avg
```

## Grading Script

Use `scripts/run_eval.py` to automate evaluation:

```python
#!/usr/bin/env python3
"""Run an evalset against the current agent and grade results."""
import argparse
import json
from pathlib import Path

def load_evalset(path: str) -> list[dict]:
    return json.loads(Path(path).read_text())

def grade_case(case: dict, actual: str, config: dict) -> dict:
    score = 0
    total = len(case["rubric"])
    details = {}
    for key in case["rubric"]:
        if key in config["grading"]["strict_match_keys"]:
            passed = check_strict(case["expected"], actual, key)
        else:
            passed = check_fuzzy(case["expected"], actual, key)
        details[key] = passed
        score += int(passed)
    return {
        "id": case["id"],
        "score": score / total if total else 0,
        "passed": (score / total) >= config["grading"]["pass_threshold"],
        "details": details,
    }

def check_strict(expected: str, actual: str, key: str) -> bool:
    # Extract numbers and compare
    import re
    expected_nums = re.findall(r"[\d,]+\.?\d*", expected)
    actual_nums = re.findall(r"[\d,]+\.?\d*", actual)
    return bool(set(expected_nums) & set(actual_nums))

def check_fuzzy(expected: str, actual: str, key: str) -> bool:
    # Simple keyword overlap — replace with LLM judge for production
    expected_words = set(expected.lower().split())
    actual_words = set(actual.lower().split())
    overlap = len(expected_words & actual_words) / len(expected_words)
    return overlap > 0.5
```

## Gotchas

- **Eval drift**: Re-run baselines when you update datasets; stale baselines
  give misleading deltas.
- **Rubric granularity**: Broad rubric keys (e.g. "correct") hide failure modes.
  Prefer specific keys like `correct_total`, `names_column`.
- **Date-sensitive data**: If CSVs contain relative dates ("last quarter"),
  evals break over time. Pin dates or use synthetic data.
- **Large CSVs**: Keep eval datasets under 10 MB. Larger files slow eval runs
  and can hit token limits.
- **LLM judge variance**: Fuzzy-match grading varies between runs. Pin the
  judge model version and temperature (0.0) for reproducibility.

## Validation

After workspace setup, confirm:

1. `ls datasets/` shows at least one `.csv` file.
2. `python -c "import json; json.load(open('evalsets/<file>.json'))"` parses
   without error.
3. `python scripts/run_eval.py --evalset evalsets/<file>.json --output /dev/null`
   completes without exceptions.
