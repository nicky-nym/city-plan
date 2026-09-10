# city-plan

Tools for designing and scoring city-block geometries. A city is described
as one repeating tile of "solids" (footprint x stories x daylight mix),
scored per square foot of land under swappable cost/value assumptions.
Started as a design exploration of "Plan-B City", a stairless, carless
platonic grid; growing into a workbench that compares candidate designs
against real cities, visualises them in 3D, and searches for better ones.
README.md states the long-term goals and the four-layer architecture.

## Read first

- `README.md` - vision and architecture (design source -> compiled
  geometry -> scorers + assumptions -> results -> viewer / search).
- `next-steps.md` - current state, headline findings, prioritized roadmap,
  open decisions. Update it at the end of any session that changes
  findings, priorities, or decisions.
- `plan-b-city-spec.md` - the Phase 1 design record and the Section 4
  scorecard that the calculator must reproduce.
- `README_for_file_formats.md` - the `city-plan/0.1` JSON format.

## Layout

```
cities/*.json                 one file per city (exact or statistical)
assumptions/*.json            cost and value models, separate from geometry
schema/city-plan.schema.json  JSON Schema for city files
tools/far_calculator.py       the only scorer so far; stdlib only, no deps
results/scorecard*.md         generated, one per assumptions file; regenerate, never hand-edit
```

Planned, per README.md: `geometry/` (compiled 2.5D geometry), more scorers
under `tools/`, JSON results under `results/`, `viewer/index.html`, and one
document per design.

## Commands

Score all cities and check regression targets (exit 1 on failure):

```bash
python3 tools/far_calculator.py cities/*.json -a assumptions/platonic-default.json
```

Add `--markdown results/scorecard.md` to regenerate the scorecard. The
`/score` skill does both, and also scores under `assumptions/realistic-2026.json`
into `results/scorecard-realistic-2026.md`. There is no separate test suite;
the `expected_results` block in each city file is the regression baseline.

To score a design variant without touching the repo, copy the city file to
the scratchpad, edit it, drop `expected_results`, and pass the copy to the
calculator.

## Architecture rules

- Designs are parametric templates plus a parameter vector, not fixed
  instances. When a design choice could be a knob (gallery width, court
  size, helix spacing), make it a parameter rather than a hard-coded number.
- Once the compiler exists, scorers and the viewer read compiled geometry
  only, never design-source files. Until then, v0.1 files declare by hand
  the fractions a compiler will later derive; every such declaration carries
  a derivation string that becomes a compiler regression test.
- Scorers are small, independent, fast (well under a second per tile) and
  write machine-readable results. The viewer and search loop read results
  files and never call scorers directly.
- The viewer is a single HTML file loading three.js from a CDN. No Node, no
  build step. Polish is not a goal.
- Search optimises a Pareto front (net value, commute time, daylight,
  carbon, trees, and more), never a single scalar.
- Scorers stay Python standard library only. numpy or shapely are allowed
  in geometry tools only where the work would be badly hobbled without them,
  and must be isolated to those tools.
- New cost or value models go in a new file under `assumptions/`, with a
  new `cost_model.type` handled in `marginal_floor_cost()`. City files
  should not need to change to be re-scored.
- Units are feet, square feet, and dollars per square foot throughout.

## Regression and data rules

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
- Circulation is two per-solid fields. `circulation_fraction` (transport
  circulation built as floorspace: gen 4 arcades and ramp lanes) is always
  charged. `internal_circulation_fraction` (corridors, cores, galleries) is
  charged only when the assumptions file's `internal_circulation.type` is
  `declared`; platonic-default sets `none` because the spec never charged
  it, and that is what keeps the Section 4 table reproducible. Do not fold
  internal circulation into `circulation_fraction` or the spec check breaks.
- Monte Carlo uses the fixed seed and sample count in the calculator. Do not
  change them casually; results in docs depend on them.
- Design decisions that change a spec'd city (such as the gen 4 gallery
  layout) belong to the author. Score the alternatives, record them in
  next-steps.md, recommend one, and leave the city file alone until the
  author decides.
