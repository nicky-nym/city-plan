---
name: score
description: Score every city file with the FAR calculator, check regression targets, and regenerate results/scorecard.md
---

Run the calculator over all cities and regenerate the scorecard:

```bash
python3 tools/far_calculator.py cities/*.json -a assumptions/platonic-default.json --markdown results/scorecard.md
```

Then:

1. Report each city's PASS/FAIL line. Exit code 1 means at least one
   `expected_results` check failed; do not edit the tolerances or the
   `expected_results` blocks to make it pass without saying so explicitly.
2. If `results/scorecard.md` changed, show the diff and explain which
   change in geometry or assumptions caused it.
3. If a second assumptions file is given as an argument, run it as well
   and present both scorecards side by side.
