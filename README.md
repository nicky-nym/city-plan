# city-plan

Tools authored by Claude in 2026 to look at different geometries and "layout
plans" for city blocks, mobility, and circulation.

Each city is described as one repeating tile of building "solids" in a small
JSON format, then scored for floor area ratio, ground coverage, gross value,
construction cost, and net value per square foot of land under a separate,
swappable set of economic assumptions.

## Run

```bash
python3 tools/far_calculator.py cities/*.json -a assumptions/platonic-default.json --markdown results/scorecard.md
```

Requires Python 3 only; no third-party packages.

## Read more

- [plan-b-city-spec.md](plan-b-city-spec.md) - the design spec this started from
- [README_for_file_formats.md](README_for_file_formats.md) - the JSON file format
- [next-steps.md](next-steps.md) - project state and roadmap
- [results/scorecard.md](results/scorecard.md) - current scores
