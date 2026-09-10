# city-plan — Project State & Next Steps

*Handoff document. A fresh chat should read `README.md` (vision and
architecture), this file, and `plan-b-city-spec.md`, and be fully oriented.
Last updated: 2026-09-09 (night, after the roadmap session).*

## Where the project is going

See README.md "Where this is going" for the five long-term goals: a library
of real and candidate cities in one format, 3D visualisation, an interactive
comparison page, a suite of estimators, and a search workflow that finds
high-performing designs. Decisions taken on 2026-09-09 that shape all later
work:

- **Two-layer format.** Designs are parametric templates (`cities/`); a
  compiler expands them into explicit 2.5D geometry (floor polygons plus
  sloped circulation paths); every scorer and the viewer read the compiled
  layer only. Hand-derived fractions in today's v0.1 files become regression
  tests for the compiler.
- **Viewer early.** A single HTML file with three.js from a CDN, no Node
  build. Audience is the author plus a dozen viewers; polish is not a goal.
  Seeing geometry catches spec ambiguities faster than any scorer (the gen 4
  gallery question took a session of arithmetic to find).
- **Real cities: simplest first.** Statistical tiles (as manhattan-generic
  today) remain the method for now. Tracing representative blocks from open
  data (NYC PLUTO, Paris, Barcelona) is a later item.
- **Search objective is a Pareto front**, not a scalar: net value per sf
  land, commute time, daylight, carbon, tree count, and more as scorers
  arrive. The viewer shows the front.
- **Dependencies.** Scorers stay standard-library Python so they are fast
  and portable; numpy or shapely are allowed in geometry tools only where
  the work would be badly hobbled without them.
- **Documents.** README.md is the project overview; plan-b-city-spec.md is
  the Phase 1 record and stays the platonic-default regression baseline;
  each design will get its own document, generated partly from its JSON.

## Roadmap, in agreed order

0. **Gallery default for gen 4.** Decision pending from the author (see
   "Open decision" below). In the parametric format the gallery layout
   becomes a parameter the search explores, so this only fixes the default
   the spec describes.
1. **Define the v0.2 formats.** Two documents: the design-source format
   (template + parameter vector; keep distributions for statistical
   cities) and the compiled-geometry format (per-floor polygons in tile
   coordinates, light-grade regions, circulation paths with slopes and
   widths, openings). Write these before code.
2. **Build the compiler.** Regression suite: the five plan-b files. It must
   reproduce their footprints, coverage, and every hand-derived circulation
   fraction (14.4% corridors gens 1–3, 27.0% galleries gen 4, 10%
   pavilion corridor) from parameters alone. The FAR calculator then reads
   compiled geometry, and platonic-default must still reproduce the Section 4
   table.
3. **Viewer.** `viewer/index.html`: city list, side-by-side of two or three
   cities, single-design explore mode with floors toggled. Reads compiled
   geometry and results JSON from the repo.
4. **Daylight scorer.** 45° rule on compiled geometry, replacing declared
   `light_fractions`. First job: the 50×50 band intersections (22.9% of a
   waffle module-floor) are valued windowed but the spec itself calls them
   dark; charging them dark costs gen 3 roughly $1,000/sf land under
   realistic-2026 and nearly closes its lead over Manhattan. Second job:
   Manhattan's hand-waved 55/45 split. Later: continuous sky-angle value.
5. **Travel-time scorer.** Graph search over compiled circulation paths
   (lanes, ramps, helices, elevators) to verify the ~25-min gen 4 commute and
   compute Manhattan's equivalent under identical trip distributions. Also
   the place to check whether narrower or shared galleries hurt the commute.
6. **Results format.** One JSON per city per assumptions set, all metrics,
   consumed by the viewer and the search loop. Markdown scorecards become a
   rendering of it. Move `expected_results` to one block per assumptions
   file so realistic-2026 gets a regression check (gen 1 hand values: FAR
   3.6364, value $6,546, cost $2,367, net $4,178).
7. **More scorers.** Carbon (embodied, by structure class and floor area),
   trees and greenspace (courts, moats, roofs, terraces vs benchmarks),
   water and stormwater under 81% coverage, rental value with a per-floor
   gradient. Each is a small tool with its own assumptions file.
8. **More cities.** phoenix-generic, paris-haussmann, barcelona-eixample
   (the spec notes gen 1 independently reproduces it), hong-kong-tower-podium;
   then traced real blocks. Each needs a stated basis for its internal
   circulation and light fractions until the scorers derive them.
9. **Search loop.** Mutate template parameters, compile, score, keep the
   Pareto front; a skill that lets Claude brainstorm a candidate, run it,
   and report where it lands. Needs every scorer to run in well under a
   second per tile.

Carried forward from the earlier roadmap, to slot in as the scorers mature:
a height-dependent core factor (bands by story count, per sampled building,
mostly affecting Manhattan's tall tail); hardening realistic-2026 with cited
cost bands.

## Open decision: the gen 4 gallery design

The 8-ft cloister on both faces of every band (27.0% of waffle floorspace)
is the single number that decides whether ramp city beats Manhattan under
realistic-2026. It is a faithful reading of the spec text: "each courtyard's
perimeter gallery", 8 ft wide, tilted into a continuous helix, so every face
of every band carries a gallery at every level, and a cloister is
conventionally inside the building envelope. Variants scored 2026-09-09
(net $/sf land, realistic-2026; gen 3 = $4,717, Manhattan = $3,421):

| Design | Gallery share of band | Net |
|---|---|---|
| As written: 8 ft, both faces, every court | 27.0% | 3,342 |
| 6 ft, both faces, every court | 19.8% | 3,892 |
| 8 ft, helix in every other court | 13.5% | 4,375 |
| 6 ft, every other court | 9.9% | 4,650 |
| 8 ft cantilevered into the moat, every court | 0% in band | 4,880 |
| 8 ft cantilevered, every other court | 0% in band | 5,144 |

What the variants showed:

- **The penalty is lost sale value, not construction cost.** Cost is $2,731
  for every inside-band variant; a gallery costs what the room it displaces
  would have. The $2,066 gap between as-written and gallery-free is forgone
  windowed floorspace at $1,800. A cheaper cost grade for open cloisters
  would save only about $320, so it is a refinement, not a fix.
- **Every other court is the cleanest revision.** Each band carries one
  gallery and 42-ft through-rooms lit from both ends; 8 ft, 1:30, the 12-ft
  moat and the 45° rule are untouched. Costs: pavilions in helix-free courts
  lose their bridge to a level-2 gallery (need a passage through the band,
  or become private roof gardens), and the longest walk to a ramp grows by
  about one band length. The remaining $342 gap to gen 3 is then the honest
  price of vertical circulation, which gen 3 never specified.
- **The cantilever is a different building.** Ring inside the 84-ft court is
  76 ft on centre, a 304-ft lap, so the helix steepens to 3.9% or the court
  grows; the moat drops to 4 ft; coverage rises to 94%; opposite galleries
  cut a few degrees into the 45° plane from ground sills. It beats gen 3 only
  because the model charges a cantilevered walkway at ordinary floor cost.
- **6 ft makes the helix single-track for trikes** (a cargo trike is about
  3 ft wide and the helix is two-way).

Recommendation: 8-ft helix in every other court as the spec default, with
gallery width and helix spacing as search parameters. Questions for the
author: were the galleries pictured inside the 50-ft band or hanging into the
court; is two-way trike passing a hard requirement; are half the pavilion
roofs losing their bridge acceptable?

## Where the project stands

**Phase 1 (design exploration)** is recorded in `plan-b-city-spec.md`: four
generations of plan-b-city geometry scored by net value per sf of land under
fixed toy assumptions, culminating in gen 4 "ramp city" (net $5,766/sf
land, ~25-min commutes, no stairs, elevators or cars).

**Phase 2 (tooling)** so far:

- **`city-plan/0.1` JSON format**: one representative tile of "solids"
  (footprint × stories × daylight mix); numeric fields accept scalars or
  distributions (seeded Monte Carlo). Documented in
  `README_for_file_formats.md`; structural validation in
  `schema/city-plan.schema.json`. Fractions a compiler will later derive
  (light, circulation) are declared by hand with derivation strings.
- **Assumptions files** in `assumptions/`: `platonic-default.json` (the
  spec's toy model, the regression baseline, internal circulation not
  charged) and `realistic-2026.json` (stepped height-class costs, blended
  Manhattan-class values, internal circulation charged).
- **Circulation is two per-solid fields.** `circulation_fraction` is
  transport circulation built as floorspace (gen 4's arcades and ramp
  lanes), always charged. `internal_circulation_fraction` is corridors,
  cores and galleries, charged only when the assumptions file's
  `internal_circulation.type` is `declared`.
- **Six cities** in `cities/`: plan-b1-waffle, plan-b2-pavilions,
  plan-b3-penthouses, plan-b3-traditional-streets, plan-b4-ramp-city (exact),
  and manhattan-generic (statistical: 900×324 tile, 5–10 buildings,
  lognormal stories 4–30 median 8, 90% lot coverage, 15% core factor).
- **`tools/far_calculator.py`**: saleable FAR, ground coverage, gross value,
  cost and net value per sf land. Cost models `marginal-linear` (spec) and
  `marginal-bands` (stepped by floor number). `/score` runs both assumptions
  files and writes both scorecards.

## Regression baseline (must keep passing)

Under platonic-default the calculator reproduces the spec's Section 4
scorecard; each city file's `expected_results` (tagged
`"assumptions": "platonic-default"`) is checked, exit 1 on failure. Known
wrinkle: gen 4 computes gross $13,614 / net $5,774 vs the table's $13,606 /
$5,766, a 0.06% artifact of "~4.8%" circulation having been rounded in the
original derivation. Tolerance accepts it; do not "fix" either side.

## Headline findings

### Internal circulation charged everywhere (2026-09-09)

Every plan-b file declares an `internal_circulation_fraction` derived from
its geometry; Manhattan's 15% moved to the same field. Under realistic-2026
all six cities pay for corridors and cores; under platonic-default none do,
matching the spec. Only Manhattan's platonic number moved (−$2,092 → −$231).

| Solid | Internal share | Geometry (sf per module-floor) |
|---|---|---|
| waffle bands, gens 1–3 | 14.4% | 6-ft double-loaded corridor on both band centrelines, crossing once: 6×134×2 − 36 = 1,572 of 10,900 |
| waffle bands, gen 4 | 27.0% | 8-ft helical cloister rings each 84×84 court on every floor: 100² − 84² = 2,944 of 10,900 |
| court pavilion | 10% | one 6×60 corridor, 360 of 3,600 |
| penthouse | 0% | 26-ft band opens onto 12-ft terraces; the terrace is the walkway |
| manhattan-generic | 15% | typical mid-rise core + corridor factor |

Gens 1–3 charge corridors only; they never specified vertical circulation
(no stairs allowed, ramps arrive in gen 4), so their numbers are a floor and
**gen 4 is the only complete design to set against Manhattan.**

Realistic-2026, net $/sf land:

| City | net | rank |
|---|---|---|
| plan-b3-penthouses | 4,717 | 1st |
| plan-b2-pavilions | 4,349 | 2nd |
| plan-b1-waffle | 4,178 | 3rd |
| manhattan-generic | 3,421 | 4th |
| plan-b4-ramp-city | 3,342 | 5th |
| plan-b3-traditional-streets | 3,302 | 6th |

Gen 3 leads Manhattan by $1,296 with corridors charged; whatever vertical
circulation it eventually gets will cost part of that. Under platonic-default
Manhattan is essentially break-even (−$231), so its platonic loss is the
linear cost schedule and the 45% dark share, not the core factor.

### Realistic cost model (2026-09-09)

`assumptions/realistic-2026.json`: all-in development cost (hard + soft,
excluding land) for a high-cost US metro, stepped by height class as the
marginal $/sf of floor k: $500 (floors 1–3), $600 (4–7), $750 (8–12), $900
(13–20), $1,100 (21–30), $1,350 (31–40), $1,650 (41+). Values: windowed
$1,800, skylit $1,500, dark $900 (blended 2026 Manhattan capitalised value,
not the spec's $3,000 luxury ceiling). Order-of-magnitude estimates from
published 2025–26 cost guides, **not licensed RSMeans data**; replace
band-by-band when better sources arrive.

Answers to the three questions that motivated it:

1. **Does the gen 1→4 ranking hold?** Mostly; gen 3 stays on top, streets
   counterfactual stays last. Gen 4 dropped to 5th once its galleries were
   charged (above).
2. **Does taller than 8 stories become optimal?** Cost no longer caps
   height at all: a windowed floor pays for itself at every floor number
   (marginal cost tops out at $1,650 < $1,800), skylit through floor 40,
   dark through floor 20. Under platonic-default a windowed slab peaked at
   10 stories; under realistic-2026 it is monotone increasing. **The spec's
   "7 stories optimal" now rests entirely on the 45° daylight rule, which
   the calculator only declares, so "7 stories" is an input, not a finding.**
   This is why the daylight scorer is roadmap item 4 and not later.
3. **Does Manhattan go positive?** Yes, +$3,421, but 27% below gen 3. What
   remains of the gap is not cost: it is 45% dark space at half value, plus
   the corridor share, which gen 3 now also pays.

### Under platonic-default (2026-07-03)

manhattan-generic scores −$231/sf of land (was −$2,092 before circulation
was made symmetric). The linear cost schedule ($800 + $200k per floor k)
makes windowed floors unprofitable above floor 11 and skylit above 8, and
~45% of deep-floorplate space is dark. Real high-rise costs are nothing like
this; the platonic file is kept only as the regression baseline.

## Workflow notes

- Monte Carlo uses seed 20260703, 20k samples; results are reproducible.
- Cost is charged by absolute floor NUMBER (a base_floor-8 penthouse pays
  floor-8 cost); `total_footprint_sf` splits evenly across `count_per_tile`;
  tiles may be width×depth or bare `area_sf`; `circulation_fraction` and
  `internal_circulation_fraction` add, and only the second is switchable
  from the assumptions file.
- To reproduce the spec's Section 4 table, score under platonic-default;
  the plan-b `expected_results` blocks are the spec's numbers and must stay
  that way. Any restated baseline belongs in a realistic-2026 block (item
  6), not the platonic one.
- Scratch scoring of design variants: copy a city file to the scratchpad,
  edit one field, strip `expected_results`, and pass the copy to the
  calculator alongside `-a assumptions/realistic-2026.json`. That is how the
  gallery table above was produced.
