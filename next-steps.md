# city-plan — Project State & Next Steps

*Handoff document. A fresh chat should read this plus `plan-b-city-spec.md`
and be fully oriented. Last updated: 2026-07-03.*

## Where the project stands

**Phase 1 (design exploration) is summarized in `plan-b-city-spec.md`:**
four generations of plan-b-city geometry, scored by net value per sf of land
under fixed toy assumptions, culminating in Gen 4 "ramp city"
(net $5,766/sf land, ~25-min commutes, no stairs/elevators/cars).

**Phase 2 (tooling) has begun.** We built:

- **`city-plan/0.1` JSON format** — describes any city as a repeating tile of
  "solids" (footprint × stories × daylight mix), works for exact periodic
  designs and statistical real cities alike. Numeric fields accept scalars or
  distributions (seeded Monte Carlo). Documented in `city-plan-format-spec.md`
  (the repo README); structural validation in `schema/city-plan.schema.json`.
- **Economic assumptions live separately** in `assumptions/platonic-default.json`
  so any city can be re-scored under any cost/value model without touching
  geometry files.
- **Six encoded cities** in `cities/`: plan-b1-waffle, plan-b2-pavilions,
  plan-b3-penthouses, plan-b3-traditional-streets, plan-b4-ramp-city (all exact), and
  manhattan-generic (statistical: 900×324 tile, 5–10 buildings, lognormal
  stories 4–30 median 8, 90% lot coverage, 15% core factor).
- **`tools/far_calculator.py`** — computes saleable FAR, ground coverage,
  gross value, cost, and net value per sf land. Run:
  `python3 tools/far_calculator.py cities/*.json -a assumptions/platonic-default.json`

## Regression baseline (must keep passing)

The calculator reproduces the spec's Section 4 scorecard exactly; each city
file carries its targets in `expected_results` and the tool checks them
(exit code 1 on failure). One known wrinkle: gen4 computes gross $13,614 /
net $5,774 vs the spec table's $13,606 / $5,766 — a 0.06% artifact of "~4.8%"
circulation having been rounded in the original derivation. Tolerance is set
to accept this; do not "fix" it silently in either direction.

## Headline finding so far

Under platonic-default assumptions, **manhattan-generic scores net −$2,092/sf
of land** — it loses money. Three causes, in order of importance:

1. The linear cost schedule ($800 + $200k per floor k) makes windowed floors
   unprofitable above floor 11, skylit above 8. Towers hemorrhage value.
   Real high-rise costs are nothing like this — this is the model's weakest
   assumption, now demonstrated concretely.
2. ~45% of deep-floorplate space is dark ($800/sf value, higher cost).
3. Manhattan is charged a 15% core/corridor/elevator factor that platonic
   gens 1–3 charge at 0% (the spec's own Section 5 fairness caveat, now
   quantified). Cross-family comparisons are NOT apples-to-apples until
   platonic files charge internal circulation too.

## Next steps, in priority order

1. **Realistic cost model.** Create `assumptions/realistic-2026.json` with a
   new `cost_model.type` (e.g. per-height-class $/sf lookup, RSMeans-flavored)
   plus matching realistic value tiers ($/sf rents or prices by daylight
   grade). Re-run everything. Key questions: does the Gen 1→4 ranking hold?
   Does taller-than-8-stories become optimal? Does Manhattan go positive?
   (Requires adding the new cost model type to `marginal_floor_cost()` in
   far_calculator.py — small change, marked by the ValueError.)
2. **Charge internal circulation everywhere.** Add realistic
   `circulation_fraction` to gens 1–4 (corridors within 50-ft floorplates,
   the ramp galleries) so the Manhattan comparison becomes fair. Expect all
   platonic net values to drop several percent; document the restated
   scorecard as the new baseline.
3. **Daylight scorer.** Derive `light_fractions` from geometry + the 45° rule
   instead of declaring them. Needs the v0.2 "compiler" step: expand solids
   into explicit 2.5D footprint polygons. Replaces the hand-waved 55/45
   Manhattan split; enables solar-orientation studies later.
4. **Travel-time tool.** Consume `circulation_graph` (currently inert but
   populated in gen4 and manhattan files): graph search over lanes / ramps /
   elevators to verify the ~25-min Gen 4 commute claim and compute
   Manhattan's equivalent under identical trip distributions.
5. **More cities.** phoenix-generic (low-rise sprawl), paris-haussmann,
   barcelona-eixample (the spec notes Gen 1 independently reproduced this —
   encoding it is a satisfying check), hong-kong-tower-podium.

## Workflow notes

- Monte Carlo uses seed 20260703, 20k samples — results are reproducible.
- Format conventions worth remembering: cost is charged by absolute floor
  NUMBER (a base_floor-8 penthouse pays floor-8 cost); `total_footprint_sf`
  splits evenly across `count_per_tile`; tiles may be given as width×depth
  or as bare `area_sf` (used by the traditional-streets counterfactual).
