"""Exact captures at the poses the source's runs name.

Lane r108-1118, blind review of jlevy/squares#1018. For every rotated direction r of the
source's runs, the centre of the least-bound box: the box's certified bound is a lower bound
on the capture at every centre of the box, so the exact capture at its centre must be at
least that bound, and at least 1. At r = 0, the sweep's argmin. Every capture is exact
(GMP rationals, clipping); every 25th direction is evaluated again by the chord method and
must agree exactly. This samples poses; it decides no direction.

Imports nothing from jlevy/squares or the source.

Usage: python -I rv1018_poses.py --measure M.json.gz --runs RUNS.json --out OUT.json
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import rv1018_common as cm  # noqa: E402


def pose_values(
    rects_q: list,
    table: list[dict],
    step: Fraction,
    side_b: Fraction,
    side: Fraction,
    cross_every: int = 25,
) -> list[dict]:
    out = []
    h = cm._q(side_b / 2)
    for t in table:
        r = t["r"]
        if r == 0:
            px, py = (Fraction(v) for v in t["argmin"])
        else:
            px, py = Fraction(float(t["box"][0])), Fraction(float(t["box"][1]))
        val = cm.capture_exact(rects_q, r, step, side_b, px, py)
        bound = Fraction(float(t["bound"]))
        vq = Fraction(val.numerator, val.denominator)
        row = {
            "r": r,
            "exact": cm.mpq_to_float_str(val, 17),
            "logged_bound": t["bound"],
            "exact_minus_bound": float(vq - bound),
            "at_least_bound": vq >= bound,
            "at_least_one": vq >= 1,
            "witness_99_100": vq * Fraction(99, 100) < 1,
            "in_quadrant": side / 2 <= px <= cm.domain_upper(r, step, side)
            and side / 2 <= py <= cm.domain_upper(r, step, side),
        }
        if r >= 1 and cross_every and r % cross_every == 0:
            c, s = cm.cos_sin(r * step)
            alt = cm.capture_exact_chords(rects_q, cm._q(c), cm._q(s), h, cm._q(px), cm._q(py))
            row["chord_method_agrees"] = alt == val
        out.append(row)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--measure", required=True)
    ap.add_argument("--runs", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    t0 = time.process_time()
    meas = cm.read_measure(args.measure)
    runs = json.loads(Path(args.runs).read_text())
    rects_q = cm.to_mpq_rects(cm.expand(meas["rows"], meas["L"]))
    rows = pose_values(rects_q, runs["directions"], meas["step"], meas["B"], meas["L"])
    rot = [x for x in rows if x["r"] >= 1]
    least = min(rot, key=lambda x: Fraction(x["exact"]))
    tight = min(rows, key=lambda x: x["exact_minus_bound"])
    fails = []
    if not all(x["at_least_bound"] for x in rows):
        fails.append("an exact capture below its box's certified bound")
    if not all(x["at_least_one"] for x in rows):
        fails.append("an exact capture below 1")
    if not all(x.get("chord_method_agrees", True) for x in rows):
        fails.append("the two exact methods disagree")
    res = {
        "program": "rv1018_poses.py",
        "verdict": "ALL_POSES_CONSISTENT" if not fails else "POSES_INCONSISTENT",
        "failures": fails,
        "poses": len(rows),
        "least_exact_at_least_bound_centre": least,
        "least_exact_minus_bound": tight,
        "median_exact_rotated": sorted(Fraction(x["exact"]) for x in rot)[len(rot) // 2].__float__(),
        "witnesses_99_100": sum(1 for x in rot if x["witness_99_100"]),
        "outside_quadrant": [x["r"] for x in rows if not x["in_quadrant"]],
        "cross_checked": sum(1 for x in rows if "chord_method_agrees" in x),
        "cpu_seconds": round(time.process_time() - t0, 1),
        "rows": rows,
    }
    Path(args.out).write_text(json.dumps(res, separators=(",", ":")) + "\n")
    print(res["verdict"], fails, "least", least["exact"], "at r =", least["r"])
    return 0 if not fails else 1


if __name__ == "__main__":
    raise SystemExit(main())
