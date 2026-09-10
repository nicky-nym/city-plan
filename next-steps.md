# city-plan — Project State & Next Steps

*Handoff document. A fresh chat should read this plus `plan-b-city-spec.md`
and be fully oriented. Last updated: 2026-09-09 (evening, after the circulation restatement).*

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
  regression baseline; internal circulation *not* charged, as in the spec)
  and `realistic-2026.json` (stepped height-class costs, blended
  Manhattan-class values, internal circulation charged; see "Realistic cost
  model" and "Internal circulation" below).
- **Circulation is two per-solid fields.** `circulation_fraction` is
  transport circulation built as floorspace (gen 4's arcades and ramp
  lanes) and is always charged. `internal_circulation_fraction` is ordinary
  corridors/cores/galleries, with a hand `internal_circulation_derivation`
  in every file, and is charged only when the assumptions file's
  `internal_circulation.type` is `declared`. Under either file every city
  is treated alike.
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

### Internal circulation charged everywhere (2026-09-09, later session)

Roadmap item 1 done. Every plan-b file now declares an
`internal_circulation_fraction` derived from its geometry, and Manhattan's
15% moved from `circulation_fraction` to the same field, so under
realistic-2026 (which charges it) all six cities pay for corridors and cores
and under platonic-default (which does not, matching the spec) none do.
Platonic-default still reproduces the spec's Section 4 table exactly; only
Manhattan's platonic number moved (−$2,092 → −$231) because it is no longer
the one city paying a core factor.

Derivations (sf per module-floor):

| Solid | Internal share | Geometry |
|---|---|---|
| waffle bands, gens 1–3 | 14.4% | 6-ft double-loaded corridor on both band centrelines, crossing once: 6×134×2 − 36 = 1,572 of 10,900 |
| waffle bands, gen 4 | 27.0% | 8-ft helical cloister rings each 84×84 court on every floor, replacing the corridor: 100² − 84² = 2,944 of 10,900 |
| court pavilion | 10% | one 6×60 corridor, 360 of 3,600 |
| penthouse | 0% | 26-ft band opens onto 12-ft terraces both sides; terrace is the walkway |
| manhattan-generic | 15% | typical mid-rise core + corridor factor (unchanged, relocated) |

Gens 1–3 charge corridors only. They never specified vertical circulation
(the no-stairs premise rules out stair cores; ramps arrive in gen 4), so
their numbers are a floor and **gen 4 is the only complete design to set
against Manhattan.**

Realistic-2026 results, before → after (net $/sf land):

| City | before | after | rank |
|---|---|---|---|
| plan-b3-penthouses | 5,850 | 4,717 | 1st |
| plan-b2-pavilions | 5,482 | 4,349 | 2nd |
| plan-b1-waffle | 5,281 | 4,178 | 3rd |
| manhattan-generic | 3,421 | 3,421 | 4th (was last) |
| plan-b4-ramp-city | 5,438 | 3,342 | 5th (was 3rd) |
| plan-b3-traditional-streets | 4,095 | 3,302 | 6th |

Two findings:

1. **The ramp galleries are the whole story for gen 4.** The spec's "1.5%
   ramp allowance" covered the vehicle ramp lanes, not the 8-ft pedestrian
   cloister, which by the spec's own dimensions is 27% of every waffle
   floor. Charged, it costs gen 4 about $2,100/sf of land and drops it
   below generic Manhattan by $79/sf, within the noise of either model.
   Sensitivity: each foot of gallery width is worth ≈$280/sf land of net
   value (5-ft galleries → $4,158; 6-ft → $3,892; 7-ft → $3,619; 8-ft →
   $3,342), so gen 4 beats Manhattan at any width under ~7.7 ft. The
   spec's 8 ft was chosen so cargo trikes can pass; that choice now has a
   price tag. Alternatives worth scoring: a single helix serving two courts
   (galleries on one face of each band, ~13.5%), narrower galleries, or
   galleries cantilevered into the moat if a relaxed 45° rule allows it.
   Also note the galleries are charged at full enclosed-space cost; an open
   cloister is cheaper, but the cost model has no such grade (the spec's
   Section 5 makes the same caveat about arcade structure).
2. **Gen 3 keeps a real lead over Manhattan, but it is an incomplete
   design.** With corridors charged, gen 3 leads Manhattan by $1,296/sf
   (was $2,429), close to the ~$1,100 predicted last session. Whatever
   vertical circulation gen 3 eventually gets will cost part of that.
   Under platonic-default, where nobody pays for internal circulation, the
   plan-b files keep their spec numbers and Manhattan is essentially
   break-even (−$231), so the platonic loss is now entirely the linear cost
   schedule and the 45% dark share, not the core factor.

The gen 1 derivation is easy to check by hand and could seed the
realistic-2026 regression block once `expected_results` supports one block
per assumptions file (item 4b): saleable FAR 76,300 × (1 − 0.1442) / 17,956
= 3.6364; value × $1,800 = $6,546; cost unchanged at $2,367; net $4,178.

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

Results at the time (net $/sf land, platonic-default → realistic-2026;
superseded for realistic-2026 by the circulation restatement above, which
also moved Manhattan's platonic number to −$231):

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
   ~$2,400. *(Confirmed by the restatement above: Gen 3 at 14.4% corridors
   nets $4,717, a $1,296 margin.)*

### Under platonic-default (2026-07-03)

**manhattan-generic scores net −$2,092/sf of land** — it loses money.
Three causes, in order of importance:

1. The linear cost schedule ($800 + $200k per floor k) makes windowed floors
   unprofitable above floor 11, skylit above 8. Towers hemorrhage value.
   Real high-rise costs are nothing like this — this is the model's weakest
   assumption, now demonstrated concretely. (Addressed by realistic-2026
   above; the platonic file is kept as the regression baseline.)
2. ~45% of deep-floorplate space is dark ($800/sf value, higher cost).
3. Manhattan was charged a 15% core/corridor/elevator factor that platonic
   gens 1–3 charged at 0% (the spec's own Section 5 fairness caveat).
   Resolved 2026-09-09: platonic-default now charges nobody for internal
   circulation and Manhattan scores −$231 under it; realistic-2026 charges
   everybody.

## Next steps, in priority order

1. **Decide the gen 4 gallery design, then rescore.** The 8-ft cloister on
   both faces of every band (27% of waffle floorspace) is the single number
   that decides whether ramp city beats Manhattan. Confirm it is the
   intended reading of the spec (gallery inside the 50-ft band, both faces,
   all seven floors), or revise the spec: narrower galleries, one helix per
   two courts, or a cantilever into the moat. Each is a one-line change to
   `internal_circulation_fraction` in plan-b4-ramp-city.json plus a new
   derivation string. Also consider a cheaper cost grade for open galleries
   and arcades (a `cost_multiplier` per circulation component) since they
   are now a third of gen 4's cost base at full price.
2. **Daylight scorer.** Derive `light_fractions` from geometry + the 45° rule
   instead of declaring them. Needs the v0.2 "compiler" step: expand solids
   into explicit 2.5D footprint polygons. Replaces the hand-waved 55/45
   Manhattan split; enables solar-orientation studies later. Under realistic
   costs the daylight rule is the *only* thing keeping the optimal waffle at
   7 stories, and it is currently declared, not computed, so "7 stories" is
   an input, not a finding. Noticed while deriving corridors: the 50×50
   band intersections, which the spec itself calls "naturally dark" and
   assigns to service cores, are 2,500 of the 10,900 sf per module-floor
   (22.9%) and are valued as windowed in every plan-b file. Charging them
   as dark would cost gen 3 roughly $1,000/sf land under realistic-2026
   (≈ 0.229 × 4.17 FAR × ($1,800 − $900) ≈ $860 net of the corridor already
   inside them) and would nearly close its lead over Manhattan. This is the
   daylight scorer's first job and probably the biggest remaining
   distortion in the platonic family's favour.
3. **Height-dependent core factor.** A third `internal_circulation.type`
   (bands by story count, like the cost bands: ~12% at 8 stories, ~25% at
   40) applied per sampled building. Mostly affects Manhattan's 20–30 story
   tail, pushing its net down; with cost no longer capping height, core
   growth and daylight are the only things stopping towers in the model.
   Needs a source per band, same discipline as the cost bands.
4. **Harden realistic-2026.** (a) Replace the estimated bands with cited
   figures (RSMeans or a Turner/Rider Levett Bucknall-class index) and
   record the source per band. (b) Hand-derive realistic-2026 targets for at
   least plan-b1-waffle (worked above: FAR 3.6364, value $6,546, cost
   $2,367, net $4,178) so the second assumptions file also has a regression
   check — this needs `expected_results` to hold one block per assumptions
   file, a small format change. (c) Consider a per-floor value gradient
   (upper-floor view premium, ~0.5–1%/floor residential) as a value-model
   option, since real markets reward height on the value side while costs
   punish it.
5. **Travel-time tool.** Consume `circulation_graph` (currently inert but
   populated in gen4 and manhattan files): graph search over lanes / ramps /
   elevators to verify the ~25-min Gen 4 commute claim and compute
   Manhattan's equivalent under identical trip distributions. Now also the
   place to test whether narrower or shared galleries (item 1) hurt the
   commute claim.
6. **More cities.** phoenix-generic (low-rise sprawl), paris-haussmann,
   barcelona-eixample (the spec notes Gen 1 independently reproduced this —
   encoding it is a satisfying check), hong-kong-tower-podium. Each needs an
   `internal_circulation_fraction` with a stated basis.

## Workflow notes

- Monte Carlo uses seed 20260703, 20k samples — results are reproducible.
- Format conventions worth remembering: cost is charged by absolute floor
  NUMBER (a base_floor-8 penthouse pays floor-8 cost); `total_footprint_sf`
  splits evenly across `count_per_tile`; tiles may be given as width×depth
  or as bare `area_sf` (used by the traditional-streets counterfactual);
  `circulation_fraction` and `internal_circulation_fraction` add, and only
  the second is switchable from the assumptions file (`internal_circulation`:
  `none` in platonic-default, `declared` in realistic-2026).
- To reproduce the spec's Section 4 table, score under platonic-default;
  the plan-b `expected_results` blocks are still the spec's numbers and
  must stay that way. Any restated baseline belongs in a realistic-2026
  block (item 4b), not in the platonic one.
