"""A search for the least capture at a stratified sample of rotated directions.

Usage: python -I direction_sample.py --release DIR --receipts FILE --out FILE
       [--strata 24] [--grid 33] [--only N]

The sample is fixed before any direction runs: directions 1 to 2072 in equal strata,
one drawn from each by a generator seeded from the candidate's SHA-256 (its first 16
hex digits), and named directions: 1, 2, 1036, 2071, 2072, the source's two least
certified, and the two whose least-bound centre had the least exact capture in
receipts_check.py. At each direction a grid over the quadrant [L/2, U_j]^2 is
evaluated in binary64, and a compass search runs from the ten best grid points; one
more search starts at the source's least-bound centre and is reported apart. Every end
point is then evaluated exactly. This decides nothing between the points it evaluates:
it can only find a capture below 1 (a counterexample) or below the source's certified
bound (a contradiction of the source's run). At each end point it also records whether
the 99/100 mutant's exact capture is below 1.
"""

from __future__ import annotations

import argparse
import gzip
import json
import random
import sys
import time
from fractions import Fraction
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import fnlib as F  # noqa: E402

NAMES = ("mixed_n28_L57425", "mixed_n30_L58925")


def plan(sha: str, run_rows: dict, receipts: dict, strata: int) -> dict[int, str]:
    rng = random.Random(int(sha[:16], 16))
    chosen: dict[int, str] = {}
    edges = [1 + round(k * 2072 / strata) for k in range(strata + 1)]
    for k in range(strata):
        chosen.setdefault(rng.randrange(edges[k], edges[k + 1]), "drawn")
    named = {1: "smallest angle", 2: "second angle", 1036: "middle", 2071: "next to last", 2072: "last"}
    by_bound = sorted(range(1, 2073), key=lambda j: run_rows[j]["min_certified_lower_bound"])
    for j in by_bound[:2]:
        named.setdefault(j, "source's least certified")
    for t in receipts["least_bound_centres"]["least_exact_margins"][:2]:
        named.setdefault(t["r"], "least exact at a least-bound centre")
    for j, why in named.items():
        chosen[j] = why if chosen.get(j) != "drawn" else f"{why}, also drawn"
    return dict(sorted(chosen.items()))


def compass(f, x: float, y: float, lo: float, hi: float, h: float, tol: float = 1e-7):
    best = f(x, y)
    evals = 1
    while h > tol:
        moved = False
        for dx, dy in ((h, 0.0), (-h, 0.0), (0.0, h), (0.0, -h)):
            nx, ny = min(max(x + dx, lo), hi), min(max(y + dy, lo), hi)
            v = f(nx, ny)
            evals += 1
            if v < best:
                best, x, y, moved = v, nx, ny, True
                break
        if not moved:
            h /= 2
    return best, x, y, evals


def direction(m: F.Measure, fm: F.FloatMeasure, L: Fraction, j: int, box: dict, bound: float, grid: int,
              axis_argmin: tuple[float, float]) -> dict:
    c, s = F.cos_sin(j)
    b = F.CORE / 2
    fc, fs, fb = float(c), float(s), float(b)
    lo, hi = float(L / 2), float(F.upper_end(j, L))
    # Keep every float pose inside the exact quadrant.
    lo_q, hi_q = Fraction(lo), Fraction(hi)
    if lo_q < L / 2:
        lo = float(np.nextafter(lo, np.inf))
    if hi_q > F.upper_end(j, L):
        hi = float(np.nextafter(hi, -np.inf))

    def f(x: float, y: float) -> float:
        return F.fcapture(fm, fc, fs, fb, x, y)

    xs = np.linspace(lo, hi, grid)
    vals = [(f(x, y), x, y) for x in xs for y in xs]
    vals.sort()
    starts = vals[:10]
    h0 = (hi - lo) / (grid - 1)
    evals = len(vals)
    ends = []
    for _, x, y in starts:
        v, x2, y2, e = compass(f, x, y, lo, hi, h0)
        evals += e
        ends.append((x2, y2, "independent"))
    bx = min(max(box["x"], lo), hi)
    by = min(max(box["y"], lo), hi)
    v, x2, y2, e = compass(f, bx, by, lo, hi, max(box["dx"], box["dy"], 1e-6))
    evals += e
    ends.append((x2, y2, "from the source's box"))
    for ax, ay in (axis_argmin, axis_argmin[::-1]):
        v, x2, y2, e = compass(f, min(max(ax, lo), hi), min(max(ay, lo), hi), lo, hi, h0)
        evals += e
        ends.append((x2, y2, "from the axis argmin"))
    exact = []
    for x, y, kind in ends:
        val = F.capture(m, j, Fraction(x), Fraction(y))
        exact.append((val, x, y, kind))
    exact.sort(key=lambda t: t[0])
    least = exact[0]
    least_ind = min((t for t in exact if t[3] == "independent"), key=lambda t: t[0])
    bound_q = Fraction(bound)
    return {
        "r": j,
        "float_evaluations": evals,
        "least_exact": float(least[0]),
        "least_exact_minus_1": float(least[0] - 1),
        "least_at": [least[1], least[2]],
        "least_kind": least[3],
        "least_independent": float(least_ind[0]),
        "source_bound": bound,
        "all_ends_at_least_1": all(t[0] >= 1 for t in exact),
        "all_ends_at_least_source_bound": all(t[0] >= bound_q for t in exact),
        "mutant_99_100_witness": Fraction(99, 100) * least[0] < 1,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--release", required=True)
    ap.add_argument("--receipts", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--strata", type=int, default=24)
    ap.add_argument("--grid", type=int, default=65)
    ap.add_argument("--only", type=int, default=0, help="run only the first N directions (a trial)")
    args = ap.parse_args()
    rec = json.loads(Path(args.receipts).read_text())["certificates"]
    res = {}
    for name in NAMES:
        t0 = time.process_time()
        cdir = Path(args.release) / name
        cert = F.read_candidate(cdir / "candidate.json.gz")
        m = F.Measure(F.expand(cert.rows, cert.L))
        fm = F.FloatMeasure(m)
        with gzip.open(cdir / "check2" / "run.jsonl.gz", "rt") as fh:
            rows = {r["r"]: r for r in (json.loads(x) for x in fh) if "r" in r}
        chosen = plan(cert.sha256, rows, rec[name], args.strata)
        items = list(chosen.items())[: args.only or None]
        dirs = []
        for j, why in items:
            axis = tuple(float(F.rat(v)) for v in rows[0]["argmin"])
            d = direction(m, fm, cert.L, j, rows[j]["least_bound_box"], rows[j]["min_certified_lower_bound"],
                          args.grid, axis)
            d["why"] = why
            dirs.append(d)
            print(name, j, why, f"{d['least_exact']:.7f}", d["least_kind"], flush=True)
        least = min(dirs, key=lambda d: d["least_exact"])
        res[name] = {
            "directions": len(dirs),
            "plan": chosen,
            "least_found": {"r": least["r"], "value": least["least_exact"], "at": least["least_at"]},
            "median_least": sorted(d["least_exact"] for d in dirs)[len(dirs) // 2],
            "every_end_at_least_1_and_the_source_bound": all(
                d["all_ends_at_least_1"] and d["all_ends_at_least_source_bound"] for d in dirs),
            "mutant_witness_at_every_direction": all(d["mutant_99_100_witness"] for d in dirs),
            "float_evaluations": sum(d["float_evaluations"] for d in dirs),
            "cpu_seconds": round(time.process_time() - t0, 1),
            "per_direction": dirs,
        }
    ok = all(r["every_end_at_least_1_and_the_source_bound"] for r in res.values())
    status = "NO_COUNTEREXAMPLE_IN_SAMPLE" if ok else "CAPTURE_BELOW_BOUND_FOUND"
    F.write_json(args.out, {"program": "direction_sample.py", "status": status, "certificates": res})
    print(status)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
