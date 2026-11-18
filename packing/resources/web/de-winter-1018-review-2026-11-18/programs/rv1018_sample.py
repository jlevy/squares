"""A seeded search for the least capture at a fixed sample of rotated directions.

Lane r108-1118, blind review of jlevy/squares#1018. The sample is fixed by rules written
before any program ran on the certificate:

- named: r = 1, 2, 3, 100, 200, 300, 399 and 400 (400 is the net's last index, whose bin
  holds no folded angle);
- from the source's runs, as rv1018_runs.py reads them: the rotated direction with the least
  certified bound, and the one with the most nodes;
- from rv1018_poses.py: the rotated direction whose least-bound centre has the least exact
  capture;
- seeded: one index in each of the eight strata [1, 50], ..., [351, 400], drawn by Python's
  random.Random seeded with the first 16 hex digits of the decompressed measure's SHA-256.

At each, a 41 x 41 float grid over the quadrant [L/2, U_r]^2, then a compass search from the
eight best grid points and from the source's least-bound centre, clipped to the quadrant;
every end point is evaluated exactly. This decides nothing between the points it
evaluates: it can find a capture below 1, or show where a 99/100 mutant has an exact
witness below 1.

Imports nothing from jlevy/squares or the source.

Usage: python -I rv1018_sample.py --measure M.json.gz --runs RUNS.json --poses POSES.json
         --out OUT.json
"""

from __future__ import annotations

import argparse
import json
import random
import sys
import time
from fractions import Fraction
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import rv1018_common as cm  # noqa: E402

NAMED = [1, 2, 3, 100, 200, 300, 399, 400]


def sample_directions(runs: dict, poses: dict, sha: str, last: int = 400) -> dict[str, list[int]]:
    rot = [t for t in runs["directions"] if t["r"] >= 1]
    least_bound = min(rot, key=lambda t: Fraction(t["bound"]))["r"]
    most_nodes = max(rot, key=lambda t: t["nodes"])["r"]
    least_pose = poses["least_exact_at_least_bound_centre"]["r"]
    rng = random.Random(int(sha[:16], 16))
    width = last // 8
    seeded = [rng.randint(1 + k * width, (k + 1) * width) for k in range(8)]
    out = {
        "named": NAMED,
        "least_certified_bound": [least_bound],
        "most_nodes": [most_nodes],
        "least_exact_pose": [least_pose],
        "seeded": seeded,
    }
    allr = sorted({r for v in out.values() for r in v})
    out["all"] = allr
    return out


def compass(fm: cm.FloatMeasure, c: float, s: float, h: float, lo: float, hi: float,
            x: float, y: float) -> tuple[float, float, float]:
    best = fm.capture(c, s, h, x, y)
    stp = 0.02
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    while stp > 1e-7:
        moved = False
        for dx, dy in dirs:
            nx = min(hi, max(lo, x + dx * stp))
            ny = min(hi, max(lo, y + dy * stp))
            v = fm.capture(c, s, h, nx, ny)
            if v < best:
                best, x, y, moved = v, nx, ny, True
                break
        if not moved:
            stp /= 2
    return best, x, y


def search_direction(fm, rects_q, r, step, side_b, side, start=None) -> dict:
    c, s = cm.cos_sin(r * step)
    cf, sf, h = float(c), float(s), float(side_b) / 2
    lo, hi = float(side) / 2, float(cm.domain_upper(r, step, side))
    lo_q, hi_q = side / 2, cm.domain_upper(r, step, side)
    g = np.linspace(lo, hi, 41)
    grid = sorted((fm.capture(cf, sf, h, x, y), x, y) for x in g for y in g)
    starts = [(x, y) for _v, x, y in grid[:8]]
    if start is not None:
        starts.append(start)
    ends = []
    for k, (x, y) in enumerate(starts):
        v, ex, ey = compass(fm, cf, sf, h, lo, hi, x, y)
        px = min(hi_q, max(lo_q, Fraction(ex)))
        py = min(hi_q, max(lo_q, Fraction(ey)))
        val = cm.capture_exact(rects_q, r, step, side_b, px, py)
        ends.append((Fraction(val.numerator, val.denominator), float(px), float(py), k >= 8))
    from_source = [e[0] for e in ends if e[3]]
    ends.sort()
    best = ends[0]
    return {
        "r": r,
        "grid_least": grid[0][0],
        "least_exact": float(best[0]),
        "least_exact_digits": cm.mpq_to_float_str(cm._q(best[0]), 17),
        "at": [best[1], best[2]],
        "end_points": len(ends),
        "at_least_one": best[0] >= 1,
        "witness_99_100": best[0] * Fraction(99, 100) < 1,
        "least_from_grid_starts": float(min(e[0] for e in ends if not e[3])),
        "from_source_start": float(from_source[0]) if from_source else None,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--measure", required=True)
    ap.add_argument("--runs", required=True)
    ap.add_argument("--poses", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    t0 = time.process_time()
    meas = cm.read_measure(args.measure)
    runs = json.loads(Path(args.runs).read_text())
    poses = json.loads(Path(args.poses).read_text())
    sample = sample_directions(runs, poses, meas["json_sha256"], meas["last"])
    rects = cm.expand(meas["rows"], meas["L"])
    rects_q = cm.to_mpq_rects(rects)
    fm = cm.FloatMeasure(rects)
    boxes = {t["r"]: t for t in runs["directions"]}
    rows = []
    for r in sample["all"]:
        st = (float(boxes[r]["box"][0]), float(boxes[r]["box"][1])) if r in boxes else None
        row = search_direction(fm, rects_q, r, meas["step"], meas["B"], meas["L"], st)
        rows.append(row)
        print(r, row["least_exact_digits"], row["at"], flush=True)
    fails = [f"capture below 1 at r = {x['r']}" for x in rows if not x["at_least_one"]]
    least = min(rows, key=lambda x: x["least_exact"])
    res = {
        "program": "rv1018_sample.py",
        "verdict": "NO_COUNTEREXAMPLE_IN_SAMPLE" if not fails else "COUNTEREXAMPLE_FOUND",
        "failures": fails,
        "sample": sample,
        "least": least,
        "median_least": sorted(x["least_exact"] for x in rows)[len(rows) // 2],
        "witness_99_100_at": sum(1 for x in rows if x["witness_99_100"]),
        "directions": len(rows),
        "cpu_seconds": round(time.process_time() - t0, 1),
        "rows": rows,
    }
    Path(args.out).write_text(json.dumps(res, indent=1) + "\n")
    print(res["verdict"], "least", least["least_exact_digits"], "at r =", least["r"])
    return 0 if not fails else 1


if __name__ == "__main__":
    raise SystemExit(main())
