# city-plan — Project State & Next Steps

*Handoff document. A fresh chat should read this plus `plan-b-city-spec.md`
and be fully oriented. Last updated: 2026-09-09.*

## Where the project stands

**Phase 1 (design exploration) is summarized in `plan-b-city-spec.md`:**
four generations of plan-b-city geometry, scored by net value per sf of land
under fixed toy assumptions, culminating in Gen 4 "ramp city"
(net $5,766/sf land, ~25-min commutes, no stairs/elevators/cars).

**Phase 2 (tooling) has begun.** We built:

- **`city-plan/0.1` JSON format** — describes any city as a repeating tile of
  "solids" (footprint × stories × daylight mix), works for exact periodic
  designs and statistical real cities alike. Numeric fields accept scalars or
  distributions (seeded Monte Carlo). Documented in `README_for_file_formats.md`;
  structural validation in `schema/city-plan.schema.json`.
- **Economic assumptions live separately** in `assumptions/` so any city can
  be re-scored under any cost/value model without touching geometry files.
  Two files so far: `platonic-default.json` (the spec's toy model; the
  regression baseline) and `realistic-2026.json` (stepped height-class
  costs, blended Manhattan-class values; see "Realistic cost model" below).
- **Six encoded cities** in `cities/`: plan-b1-waffle, plan-b2-pavilions,
  plan-b3-penthouses, plan-b3-traditional-streets, plan-b4-ramp-city (all exact), and
  manhattan-generic (statistical: 900×324 tile, 5–10 buildings, lognormal
  stories 4–30 median 8, 90% lot coverage, 15% core factor).
- **`tools/far_calculator.py`** — computes saleable FAR, ground coverage,
  gross value, cost, and net value per sf land. Two cost model types:
  `marginal-linear` (spec) and `marginal-bands` (stepped lookup by floor
  number). Run:
  `python3 tools/far_calculator.py cities/*.json -a assumptions/platonic-default.json`
  (or `/score`, which runs both assumptions files and writes
  `results/scorecard.md` and `results/scorecard-realistic-2026.md`).

## Regression baseline (must keep passing)

The calculator reproduces the spec's Section 4 scorecard exactly; each city
file carries its targets in `expected_results` (tagged
`"assumptions": "platonic-default"`) and the tool checks them when run under
that file (exit code 1 on failure; other assumptions files score without
checking). One known wrinkle: gen4 computes gross $13,614 /
net $5,774 vs the spec table's $13,606 / $5,766 — a 0.06% artifact of "~4.8%"
circulation having been rounded in the original derivation. Tolerance is set
to accept this; do not "fix" it silently in either direction.

## Headline findings

### Realistic cost model (2026-09-09)

`assumptions/realistic-2026.json`: all-in development cost (hard + soft,
excluding land) for a high-cost US metro, stepped by height class as the
marginal $/sf of floor k — $500 (floors 1–3), $600 (4–7), $750 (8–12),
$900 (13–20), $1,100 (21–30), $1,350 (31–40), $1,650 (41+). Implied
whole-building averages: 7 stories $557, 12 stories $638, 20 stories $743,
40 stories $984. Values: windowed $1,800, skylit $1,500, dark $900 (blended
2026 Manhattan condo/office capitalized value, not the spec's $3,000 luxury
ceiling; dark at ~50% because interior floorplate is sold as part of units).
The numbers are order-of-magnitude estimates from published 2025–26 cost
guides and Manhattan market reports, **not licensed RSMeans data** — the file
says so; replace band-by-band when better sources arrive.

Results (net $/sf land, platonic-default → realistic-2026):

| City | platonic | realistic | rank change |
|---|---|---|---|
| plan-b3-penthouses | 6,460 | 5,850 | still 1st |
| plan-b2-pavilions | 6,250 | 5,482 | still 2nd |
| plan-b4-ramp-city | 5,774 | 5,438 | 4th → 3rd |
| plan-b1-waffle | 5,949 | 5,281 | 3rd → 4th |
| plan-b3-traditional-streets | 4,522 | 4,095 | still 5th |
| manhattan-generic | −2,092 | +3,421 | last, but positive |

Answers to the three questions posed last session:

1. **Does the Gen 1→4 ranking hold?** Mostly. Gen 3 penthouses stays on
   top and the streets counterfactual stays last. The one swap: Gen 4 ramp
   city now beats Gen 1 waffle, because its 4.8% circulation charge is
   cheap when cost is a third of value instead of half. Gen 4 trails Gen 3
   by 7% (was 11%).
2. **Does taller than 8 stories become optimal?** The cost model no longer
   caps height at all. A windowed floor pays for itself at every floor
   number (marginal cost tops out at $1,650 < $1,800), skylit through
   floor 40, dark through floor 20. Under platonic-default a windowed slab
   peaked at 10 stories; under realistic-2026 it is monotone increasing
   (net per sf footprint $8,700 at 7 stories, $21,150 at 20, $32,650 at
   40). So the spec's "7 stories optimal" now rests entirely on the
   daylight constraint (the 45° rule), which the calculator only *declares*
   via `light_fractions`. **Height is capped by daylight geometry and
   circulation growth, not by cost — which makes roadmap items 2 and 3
   the binding work.**
3. **Does Manhattan go positive?** Yes, +$3,421/sf, but still 42% below
   Gen 3. What remains of the gap is no longer cost: Manhattan's cost/sf
   land ($3,897) is only $1,166 above Gen 3's while its gross value is
   $1,262 lower despite 9% more saleable FAR. The gap is 45% dark space at
   half value and the 15% circulation charge that platonic files still
   pay at 0%. If Gen 3 were charged 15% circulation too its net would drop
   to roughly $4,560 — still ahead, but the margin would be ~$1,100, not
   ~$2,400.

### Under platonic-default (2026-07-03)

**manhattan-generic scores net −$2,092/sf of land** — it loses money.
Three causes, in order of importance:

1. The linear cost schedule ($800 + $200k per floor k) makes windowed floors
   unprofitable above floor 11, skylit above 8. Towers hemorrhage value.
   Real high-rise costs are nothing like this — this is the model's weakest
   assumption, now demonstrated concretely. (Addressed by realistic-2026
   above; the platonic file is kept as the regression baseline.)
2. ~45% of deep-floorplate space is dark ($800/sf value, higher cost).
3. Manhattan is charged a 15% core/corridor/elevator factor that platonic
   gens 1–3 charge at 0% (the spec's own Section 5 fairness caveat, now
   quantified). Cross-family comparisons are NOT apples-to-apples until
   platonic files charge internal circulation too.

## Next steps, in priority order

1. **Charge internal circulation everywhere.** Add realistic
   `circulation_fraction` to gens 1–4 (corridors within 50-ft floorplates,
   the ramp galleries) so the Manhattan comparison becomes fair. Now the
   biggest remaining distortion: under realistic-2026 it is worth ~$1,300/sf
   of Gen 3's ~$2,400/sf lead over Manhattan. Expect all platonic net values
   to drop several percent; document the restated scorecard as the new
   baseline. Consider a height-dependent core factor (an 8-story building's
   core is ~12%, a 40-story tower's ~25%) since circulation growth is now
   one of only two things that stop towers in the model.
2. **Daylight scorer.** Derive `light_fractions` from geometry + the 45° rule
   instead of declaring them. Needs the v0.2 "compiler" step: expand solids
   into explicit 2.5D footprint polygons. Replaces the hand-waved 55/45
   Manhattan split; enables solar-orientation studies later. Promoted in
   urgency: under realistic costs the daylight rule is the *only* thing
   keeping the optimal waffle at 7 stories, and it is currently declared,
   not computed — so "7 stories" is an input, not a finding.
3. **Harden realistic-2026.** (a) Replace the estimated bands with cited
   figures (RSMeans or a Turner/Rider Levett Bucknall-class index) and
   record the source per band. (b) Hand-derive realistic-2026 targets for at
   least plan-b1-waffle (saleable FAR 4.2493 × $1,800 = $7,649 value;
   0.60704 coverage × (3×$500 + 4×$600) = $2,367 cost) so the second
   assumptions file also has a regression check — this needs
   `expected_results` to hold one block per assumptions file, a small
   format change. (c) Consider a per-floor value gradient (upper-floor view
   premium, ~0.5–1%/floor residential) as a value-model option, since real
   markets reward height on the value side while costs punish it.
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
