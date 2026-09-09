# city-plan

Tools for scoring the economics of repeating city-block geometries. A city is
described as one representative tile of "solids" (footprint x stories x
daylight mix), scored per square foot of land under swappable cost/value
assumptions. Started as a design exploration of "Plan-B City", a stairless,
carless platonic grid; now compares those designs against statistical models
of real cities.

## Read first

- `next-steps.md` - current state, headline findings, prioritized roadmap.
  Update it at the end of any session that changes findings or priorities.
- `plan-b-city-spec.md` - the design spec and the Section 4 scorecard that
  the calculator must reproduce.
- `README_for_file_formats.md` - the `city-plan/0.1` JSON format.

## Layout

```
cities/*.json                 one file per city (exact or statistical)
assumptions/*.json            cost and value models, separate from geometry
schema/city-plan.schema.json  JSON Schema for city files
tools/far_calculator.py       the only tool so far; stdlib only, no deps
results/scorecard*.md         generated, one per assumptions file; regenerate, never hand-edit
```

## Commands

Score all cities and check regression targets (exit 1 on failure):

```bash
python3 tools/far_calculator.py cities/*.json -a assumptions/platonic-default.json
```

Add `--markdown results/scorecard.md` to regenerate the scorecard. The
`/score` skill does both, and also scores under `assumptions/realistic-2026.json`
into `results/scorecard-realistic-2026.md`. There is no separate test suite;
the `expected_results` block in each city file is the regression baseline.

## Rules

- Every city file must carry an `expected_results` block. When adding a
  city, derive the targets by hand from the spec or a cited source, then
  confirm the calculator matches; never paste the calculator's own output in
  as the target. The block's `assumptions` key names the assumptions file
  the targets belong to (platonic-default if absent); under any other
  assumptions file the city is scored but not checked.
- Never loosen `CHECK_TOLERANCE` or edit an `expected_results` target to make
  a check pass without saying so explicitly and explaining why.
- plan-b4-ramp-city deliberately computes 0.06% above the spec table
  (rounded "~4.8%" circulation). Leave it; do not "fix" either side.
- Cost is charged by absolute floor number, not by floors counted from a
  solid's base. This is what makes stacked solids price like one building.
- Monte Carlo uses the fixed seed and sample count in the calculator. Do not
  change them casually; results in docs depend on them.
- New cost or value models go in a new file under `assumptions/`, with a new
  `cost_model.type` handled in `marginal_floor_cost()`. City files should not
  need to change to be re-scored.
- Keep the calculator dependency-free (Python standard library only).
- Units are feet, square feet, and dollars per square foot throughout.
