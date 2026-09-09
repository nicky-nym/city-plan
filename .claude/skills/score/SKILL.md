---
name: score
description: Score every city file with the FAR calculator, check regression targets, and regenerate results/scorecard.md
---

Run the calculator under both assumptions files and regenerate both scorecards:

```bash
python3 tools/far_calculator.py cities/*.json -a assumptions/platonic-default.json --markdown results/scorecard.md
```

```bash
python3 tools/far_calculator.py cities/*.json -a assumptions/realistic-2026.json --markdown results/scorecard-realistic-2026.md
```

Then:

1. Report each city's PASS/FAIL line. Exit code 1 means at least one
   `expected_results` check failed; do not edit the tolerances or the
   `expected_results` blocks to make it pass without saying so explicitly.
   Cities whose targets belong to a different assumptions file print
   `(no targets for ...)` and are scored but not checked; that is expected.
2. If either scorecard changed, show the diff and explain which change in
   geometry or assumptions caused it.
3. If another assumptions file is given as an argument, run it as well,
   writing `results/scorecard-<name>.md`, and present the scorecards side
   by side.
