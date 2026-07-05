# city-plan JSON — format specification v0.1

A machine-readable format for describing the repeating geometry of city plans —
both exact periodic designs (Plan-B City generations) and statistical
descriptions of real cities (generic Manhattan) — so that a family of analysis
tools can score them under shared, swappable economic assumptions.

## Design principles

1. **Cities are tiles, not building lists.** Every city file describes one
   representative tile that conceptually repeats across the plain. Exact
   designs give exact numbers; real cities give distributions.
2. **Geometry, circulation, and economics are separate layers.** A city file
   contains geometry (`solids`) and a circulation description
   (`circulation_graph`). Economic parameters (costs, values, story height)
   live in a separate *assumptions* file passed alongside, so any city can be
   scored under any assumptions.
3. **Fields are scalars or distributions.** Anywhere a number is expected, a
   distribution object may appear instead. Tools resolve distributions by
   seeded Monte Carlo, so results are reproducible.
4. **Declared now, derived later.** v0.1 lets files *declare* things that
   future tools should *derive* from geometry (daylight grades, circulation
   fractions, explicit footprint polygons). Each declared field is a stub for
   a smarter tool. See "Roadmap" below.

## City file structure

```jsonc
{
  "format": "city-plan/0.1",
  "name": "short-slug",
  "description": "prose",
  "units": "feet",

  // The repeating tile. Give width/depth, or area_sf directly when the
  // tile is easier to state as an area (e.g. "module plus 30% right-of-way").
  "tile": { "width": 134, "depth": 134 },
  // or:  { "area_sf": 25651.4, "note": "134x134 module / 0.70 buildable" }

  "solids": [ Solid, ... ],
  "circulation_graph": [ CirculationElement, ... ],   // descriptive in v0.1
  "expected_results": { ... }                          // optional regression targets
}
```

### Solid

A solid is a homogeneous block of floorspace: a footprint extruded from a base
floor for some number of stories, with a declared daylight mix.

```jsonc
{
  "id": "waffle-bands",
  "derivation": "134^2 - 84^2 courtyard",   // human-readable audit trail
  "count_per_tile": 1,                       // scalar or distribution
  "footprint_sf": 10900,                     // per instance; scalar or distribution
  // or "total_footprint_sf": splits a total evenly across count_per_tile
  // (used for statistical blocks: "5-10 buildings sharing 190,080 sf")
  "base_floor": 1,                           // 1 = ground; 8 = sits atop 7 stories
  "stories": 7,                              // scalar or distribution
  "light_fractions": { "windowed": 1.0 },    // windowed / skylit / dark, sums to 1
  "circulation_fraction": 0.0,               // share of floorspace built at full
                                             // cost but zero value (arcades, ramps,
                                             // cores, corridors)
  "roof": "terrace"                          // optional annotation
}
```

**Important convention — `base_floor` and cost:** construction cost is charged
per floor *number*, not per floor counted from the solid's own base. A
penthouse with `base_floor: 8` pays the floor-8 marginal cost. This is what
makes stacked solids (waffle + penthouse) price identically to a single
8-story solid.

### Distribution objects

```jsonc
{ "dist": "uniform-int", "min": 5, "max": 10 }
{ "dist": "lognormal", "median": 8, "sigma": 0.5, "min": 4, "max": 30 }  // truncated
```

### CirculationElement (v0.1: descriptive only)

Not yet consumed by any tool; recorded now so files are complete and the
future travel-time tool has a target schema to firm up.

```jsonc
{ "type": "lane",       "level": 0, "axis": "NS", "spacing_ft": 402, "speed_mph": 15 }
{ "type": "ramp-helix", "per": "courtyard", "slope": 0.033, "rise_per_lap_ft": 12,
  "modes": ["walk", "cargo-trike"] }
{ "type": "elevator",   "per": "building", "speed_fpm": 500, "avg_wait_s": 45 }
{ "type": "stair",      "per": "building" }
```

## Assumptions file structure

```jsonc
{
  "format": "city-assumptions/0.1",
  "name": "platonic-default",
  "story_height_ft": 12,
  "cost_model": {
    "type": "marginal-linear",     // cost of floor k = base + slope*k, $/sf
    "base_per_sf": 800,
    "slope_per_floor_per_sf": 200
  },
  "value_per_sf": { "windowed": 3000, "skylit": 2500, "dark": 800 }
}
```

The `marginal-linear` model reproduces the spec's schedule exactly: floor 1
costs $1,000/sf, floor 7 $2,200/sf, floor 8 $2,400/sf; a 7-story building
averages $1,600/sf ("$1,000 at 1 story, +$100/sf per additional story").
Swapping in RSMeans-class real data later means adding a new `cost_model.type`
(e.g. a per-height-class lookup table) — city files don't change.

A useful consequence to keep in mind: under this schedule a **windowed** floor
stops paying for itself above floor 11 (800 + 200k > 3,000), skylit above
floor 8, dark never. This is why tall statistical cities can score badly under
platonic-default assumptions — the model, not the format, is doing that.

## Metrics (v0.1 calculator)

All per sf of tile land, matching the spec's scorecard:

- **Saleable FAR** — floorspace net of circulation fraction ÷ land
- **Ground coverage** — footprints of solids with `base_floor: 1` ÷ land
- **Gross value** — Σ saleable floorspace × light-grade value ÷ land
- **Construction cost** — Σ footprint × Σ marginal floor costs ÷ land
  (circulation space pays full cost, earns nothing)
- **Net value (land utility)** — gross value − cost

## Known v0.1 limitations / roadmap

- `light_fractions` are declared, not derived. Next tool: a daylight scorer
  that computes them from explicit geometry and the 45° rule (needs footprint
  polygons, not just areas — the planned v0.2 "compiler" step that expands
  semantic primitives into 2.5D polygon solids).
- `circulation_fraction` is declared. Platonic gens 1–3 declare 0 (internal
  corridors were never charged in any generation — comparisons are internally
  fair but absolute FARs slightly optimistic, per the spec). Statistical
  cities should declare realistic core/corridor factors (~15%), which makes
  cross-family comparisons **not** apples-to-apples. Flagged in file notes.
- `circulation_graph` is inert. Next tool after daylight: travel-time
  estimator (graph search over lanes/ramps/elevators + tile geometry).
- No solar orientation, wind, fire egress, drainage — same gaps as the spec.

## Repo layout

```
README_for_file_formats.md   this spec
city-plan.schema.json        JSON Schema (structural validation)
assumptions-platonic-default.json
cities/*.json                plan-b1..plan-b4, plan-b3-traditional-streets, manhattan-generic
tools/far_calculator.py      metric calculator + regression checks
results/scorecard.md         generated output
```

Run: `python3 tools/far_calculator.py cities/*.json -a assumptions/platonic-default.json`
