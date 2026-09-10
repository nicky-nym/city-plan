# city-plan

Tools for designing and scoring city-block geometries. A city is described
as one repeating tile of building "solids", compiled into explicit geometry,
and scored per square foot of land under swappable assumptions about cost,
value, daylight, travel time and carbon. The project began as a design
exploration of "Plan-B City", a stairless, carless platonic grid, and is
growing into a workbench for comparing candidate city designs against
statistical and real cities.

## Where this is going

The long-term goal, set on 2026-09-09, is:

1. **A library of city files.** About six real cities (Manhattan first) and
   six candidate designs, all in one format.
2. **3D visualisation** of every design.
3. **An interactive page** that lists the cities, compares two or three side
   by side, and lets a viewer explore one design.
4. **A suite of estimators.** Daylight, travel time, rental value,
   construction cost, carbon footprint, trees and greenspace, and more.
5. **A search workflow.** Claude brainstorms new designs as parameter changes
   to existing templates, scores them, and hill-climbs toward a Pareto front
   over the metrics above, which the page then shows.

The city format is what holds it together, and it is expected to grow more
detailed over time.

## Architecture

Four layers, each a directory of files with a documented format. Arrows are
tools; boxes are files.

```
 design source        compiled geometry        scorers            results
 cities/*.json  --->  geometry/*.json   --->   tools/*.py  --->   results/*.json
 parametric           explicit 2.5D            read assumptions/  one per city x
 templates            floor polygons +         *.json             assumptions set
                      circulation paths                                |
                                                                       v
                                                     viewer/index.html (three.js via CDN)
                                                     search loop (mutate, compile, score)
```

- **Design source** (`cities/`). A design is a template plus a parameter
  vector (band depth, court width, stories, gallery width, and so on), not a
  fixed instance. Statistical real cities give distributions instead of
  exact numbers. This is the layer Claude edits when brainstorming and the
  layer the search loop mutates.
- **Compiled geometry** (planned). One deterministic compiler expands a
  design into explicit floor polygons, circulation paths and openings.
  Every scorer and the viewer read this layer and only this layer, so a new
  massing idea needs one compiler extension and every tool then works on it.
- **Scorers** (`tools/`). Small, fast, independent estimators. Each reads
  compiled geometry and an assumptions file and writes a results file. Fast
  matters: the search loop scores thousands of candidates.
- **Assumptions** (`assumptions/`). Cost, value, carbon factors, travel
  speeds. Separate from geometry so any city can be re-scored under any
  model.
- **Results** (`results/`). Machine-readable scorecards plus generated
  Markdown. The viewer and the search loop read these and never call the
  scorers directly.
- **Viewer** (planned). A single HTML file loading three.js from a CDN, no
  build step, usable from a static site.

**Status (2026-09-09).** Only the first two layers of the diagram exist, and
the compiler is not built yet: `cities/` holds v0.1 files where fractions
that a compiler will later derive are declared by hand, and the one scorer,
`tools/far_calculator.py`, reads them directly. Six cities are encoded and
scored under two assumptions files. See `next-steps.md` for the roadmap.

## Layout

```
cities/*.json                 one file per city (exact or statistical)
assumptions/*.json            cost and value models, separate from geometry
schema/city-plan.schema.json  JSON Schema for city files
tools/far_calculator.py       FAR / value / cost scorer; stdlib only
results/scorecard*.md         generated, one per assumptions file
plan-b-city-spec.md           Phase 1 design record and regression baseline
README_for_file_formats.md    the city-plan/0.1 JSON format
next-steps.md                 project state, findings, roadmap
```

## Run

Score every city and check regression targets:

```bash
python3 tools/far_calculator.py cities/*.json -a assumptions/platonic-default.json --markdown results/scorecard.md
```

Requires Python 3 only. The scorers stay dependency-free; geometry tools may
use numpy or shapely if they would be badly hobbled without them.

## Read more

- [next-steps.md](next-steps.md) - project state, headline findings, roadmap
- [plan-b-city-spec.md](plan-b-city-spec.md) - the Plan-B City design record this started from
- [README_for_file_formats.md](README_for_file_formats.md) - the JSON file format
- [results/scorecard.md](results/scorecard.md) - current scores under the spec's toy assumptions
- [results/scorecard-realistic-2026.md](results/scorecard-realistic-2026.md) - current scores under realistic costs
