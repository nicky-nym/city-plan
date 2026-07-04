#!/usr/bin/env python3
"""far_calculator.py -- v0.1 analysis tool for city-plan JSON files.

Computes, per sf of tile land:
  saleable FAR, ground coverage, gross floorspace value,
  construction cost, and net value ("land utility").

Exact files (all scalars) are computed deterministically.
Files containing distribution objects are resolved by seeded Monte Carlo,
so results are reproducible run-to-run.

Usage:
  python3 far_calculator.py cities/*.json -a assumptions/platonic-default.json
  python3 far_calculator.py cities/*.json -a ... --markdown results/scorecard.md
"""

import argparse
import json
import math
import random
import sys
from pathlib import Path

MC_SAMPLES = 20000
SEED = 20260703  # fixed for reproducibility

GRADES = ("windowed", "skylit", "dark")


# ---------------------------------------------------------------- sampling

def is_dist(x):
    return isinstance(x, dict) and "dist" in x


def sample(spec, rng):
    """Resolve a scalar-or-distribution field to a number."""
    if not is_dist(spec):
        return spec
    d = spec["dist"]
    if d == "uniform-int":
        return rng.randint(spec["min"], spec["max"])
    if d == "lognormal":
        lo = spec.get("min", 0.0)
        hi = spec.get("max", math.inf)
        mu = math.log(spec["median"])
        sigma = spec["sigma"]
        for _ in range(10000):
            x = rng.lognormvariate(mu, sigma)
            if lo <= x <= hi:
                return x
        raise RuntimeError(f"truncated lognormal rejection failed: {spec}")
    raise ValueError(f"unknown distribution type: {d!r}")


def solid_is_exact(solid):
    return not any(
        is_dist(solid.get(k))
        for k in ("count_per_tile", "footprint_sf", "total_footprint_sf", "stories")
    )


# ---------------------------------------------------------------- economics

def marginal_floor_cost(k, cost_model):
    """$/sf construction cost of floor number k (ground = 1)."""
    if cost_model["type"] == "marginal-linear":
        return cost_model["base_per_sf"] + cost_model["slope_per_floor_per_sf"] * k
    raise ValueError(f"unknown cost model: {cost_model['type']!r}")


def building_cost(footprint, base_floor, stories, cost_model):
    """Total $ cost of one building: footprint x sum of marginal floor costs.

    Cost is charged by absolute floor NUMBER, so a base_floor=8 penthouse
    pays floor-8 cost -- stacked solids price like one taller building.
    """
    return footprint * sum(
        marginal_floor_cost(k, cost_model)
        for k in range(base_floor, base_floor + stories)
    )


def measure_building(footprint, base_floor, stories, solid, assumptions):
    """Return (floorspace, saleable, value, cost, ground_footprint) for one
    building instance with concrete numbers."""
    stories = max(1, int(round(stories)))
    lf = solid.get("light_fractions", {})
    circ = solid.get("circulation_fraction", 0.0)
    values = assumptions["value_per_sf"]

    floorspace = footprint * stories
    saleable = floorspace * (1.0 - circ)
    value = saleable * sum(lf.get(g, 0.0) * values[g] for g in GRADES)
    cost = building_cost(footprint, base_floor, stories, assumptions["cost_model"])
    ground = footprint if base_floor == 1 else 0.0
    return floorspace, saleable, value, cost, ground


def measure_solid_once(solid, assumptions, rng):
    """One Monte Carlo realization (or the exact value) of a solid's totals."""
    base = solid.get("base_floor", 1)
    count = int(round(sample(solid.get("count_per_tile", 1), rng)))

    if "total_footprint_sf" in solid:
        per_building = sample(solid["total_footprint_sf"], rng) / count
    else:
        per_building = None  # sampled per building below

    totals = [0.0] * 5
    for _ in range(count):
        fp = per_building if per_building is not None else sample(solid["footprint_sf"], rng)
        stories = sample(solid["stories"], rng)
        for i, v in enumerate(measure_building(fp, base, stories, solid, assumptions)):
            totals[i] += v
    return totals


# ---------------------------------------------------------------- scoring

def tile_land_area(tile):
    if "area_sf" in tile:
        return tile["area_sf"]
    return tile["width"] * tile["depth"]


def score_city(city, assumptions):
    land = tile_land_area(city["tile"])
    exact = all(solid_is_exact(s) for s in city["solids"])
    n_runs = 1 if exact else MC_SAMPLES
    rng = random.Random(SEED)

    acc = [0.0] * 5
    for _ in range(n_runs):
        for solid in city["solids"]:
            for i, v in enumerate(measure_solid_once(solid, assumptions, rng)):
                acc[i] += v
    floorspace, saleable, value, cost, ground = (a / n_runs for a in acc)

    return {
        "name": city["name"],
        "exact": exact,
        "saleable_far": saleable / land,
        "ground_coverage": ground / land,
        "gross_value_per_sf_land": value / land,
        "cost_per_sf_land": cost / land,
        "net_value_per_sf_land": (value - cost) / land,
    }


# ---------------------------------------------------------------- regression

CHECK_TOLERANCE = {
    "saleable_far": 0.01,             # table shows 2 decimals
    "ground_coverage": 0.01,          # table shows whole percent
    "gross_value_per_sf_land": 10.0,  # dollars; allows spec's own rounding
    "cost_per_sf_land": 10.0,
    "net_value_per_sf_land": 10.0,
}


def regression_check(result, expected):
    """Compare against a city file's expected_results block. Returns list of
    (metric, got, want, ok)."""
    rows = []
    for metric, tol in CHECK_TOLERANCE.items():
        if expected is None or metric not in expected:
            continue
        got, want = result[metric], expected[metric]
        rows.append((metric, got, want, abs(got - want) <= tol))
    return rows


# ---------------------------------------------------------------- output

COLUMNS = [
    ("Saleable FAR", "saleable_far", "{:.2f}"),
    ("Ground coverage", "ground_coverage", "{:.0%}"),
    ("Gross value", "gross_value_per_sf_land", "${:,.0f}"),
    ("Construction cost", "cost_per_sf_land", "${:,.0f}"),
    ("Net value (land utility)", "net_value_per_sf_land", "${:,.0f}"),
]


def render_markdown(results):
    lines = []
    header = "| Metric (per sf of land) | " + " | ".join(r["name"] for r in results) + " |"
    sep = "|" + "---|" * (len(results) + 1)
    lines += [header, sep]
    for label, key, fmt in COLUMNS:
        cells = [fmt.format(r[key]) for r in results]
        lines.append(f"| {label} | " + " | ".join(cells) + " |")
    mc = [r["name"] for r in results if not r["exact"]]
    if mc:
        lines.append("")
        lines.append(f"*Monte Carlo ({MC_SAMPLES:,} samples, seed {SEED}): {', '.join(mc)}*")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("cities", nargs="+", help="city-plan JSON files")
    ap.add_argument("-a", "--assumptions", required=True)
    ap.add_argument("--markdown", help="also write a markdown scorecard here")
    args = ap.parse_args(argv)

    assumptions = json.loads(Path(args.assumptions).read_text())

    results, failures = [], 0
    for path in args.cities:
        city = json.loads(Path(path).read_text())
        res = score_city(city, assumptions)
        results.append(res)

        checks = regression_check(res, city.get("expected_results"))
        status = ""
        if checks:
            bad = [c for c in checks if not c[3]]
            failures += len(bad)
            status = "PASS" if not bad else "FAIL " + ", ".join(
                f"{m} got {g:,.1f} want {w:,.1f}" for m, g, w, _ in bad)
        mode = "exact" if res["exact"] else "monte-carlo"
        print(f"{res['name']:28s} [{mode:11s}] "
              f"FAR {res['saleable_far']:5.2f}  cover {res['ground_coverage']:4.0%}  "
              f"value ${res['gross_value_per_sf_land']:8,.0f}  "
              f"cost ${res['cost_per_sf_land']:8,.0f}  "
              f"net ${res['net_value_per_sf_land']:8,.0f}  {status}")

    if args.markdown:
        Path(args.markdown).write_text(render_markdown(results) + "\n")
        print(f"\nwrote {args.markdown}")

    if failures:
        print(f"\n{failures} regression check(s) FAILED", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
