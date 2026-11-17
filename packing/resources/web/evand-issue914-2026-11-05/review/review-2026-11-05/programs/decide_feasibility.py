"""Decide one certificate exactly: every wall and every pair, by method A and by method B.

Usage (from packing/, Python 3.14):
  python -I decide_feasibility.py CERT OUT.json [--sense -1] [--label NAME]

Method A: separating axes in fractions.Fraction (exact_geometry.pair_gap_a, wall_clearance_a).
Method B: exact clipped areas in gmpy2.mpq (exact_geometry.pair_area_b, wall_deficit_b).
No distance filter: all n(n-1)/2 pairs and all 4n wall constraints are decided by each.

Each pair is classified three ways by each method and the classes must agree:
  A: gap > 0 (closed squares disjoint), gap = 0 (touching), gap < 0 (interiors meet);
  B: clipped polygon empty, non-empty with area 0, area > 0.
The receipt records the verdicts, the agreement, the least wall clearance and least pair
gap exactly (with the square indices, 1-based, and file lines), counts by gap decade,
and the CPU seconds of each method.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import exact_geometry as eg  # noqa: E402
from cert_reader import read_cert  # noqa: E402


def fstr(v) -> str:
    v = Fraction(int(v.numerator), int(v.denominator))
    return f"{v.numerator}/{v.denominator}" if v.denominator != 1 else str(v.numerator)


def ffloat(v) -> float:
    v = Fraction(int(v.numerator), int(v.denominator))
    return float(v)


def decade(v: Fraction) -> str:
    if v < 0:
        return "negative"
    if v == 0:
        return "zero"
    e = math.floor(math.log10(float(v))) if float(v) > 0 else -400
    return f"1e{e}"


def decide(path: str, sense: int = 1) -> dict:
    cert = read_cert(path)
    n, side, squares = cert["n"], cert["S"], cert["squares"]
    lines = cert["line_of_square"]
    out: dict = {
        "path": path,
        "sha256": cert["sha256"],
        "bytes": cert["bytes"],
        "n": n,
        "side": fstr(side),
        "side_float": float(side),
        "sense": sense,
        "pairs_expected": n * (n - 1) // 2,
    }

    # ---------------- method A
    t0 = time.process_time()
    sq_a = [eg.square_a(x, y, t, sense=sense) for (x, y, t) in squares]
    clear = [eg.wall_clearance_a(s, side) for s in sq_a]
    walls_bad_a = [i + 1 for i, c in enumerate(clear) if c < 0]
    kmin = min(range(n), key=lambda i: clear[i])
    which = []
    for (px, py) in sq_a[kmin][0]:
        for name, v in (("left", px), ("right", side - px), ("bottom", py), ("top", side - py)):
            if v == clear[kmin]:
                which.append(name)
    # every square's least clearance, and how many squares sit at the least value
    at_min = sum(1 for c in clear if c == clear[kmin])
    gap_min = None
    gap_arg = None
    gap_axis = None
    classes_a = {"separated": 0, "touching": 0, "overlapping": 0}
    bad_a = set()
    touch_a = set()
    decades: dict[str, int] = {}
    pairs_a = 0
    for i in range(n):
        si = sq_a[i]
        for j in range(i + 1, n):
            g, k = eg.pair_gap_a(si, sq_a[j])
            pairs_a += 1
            if g > 0:
                classes_a["separated"] += 1
            elif g == 0:
                classes_a["touching"] += 1
                touch_a.add((i, j))
            else:
                classes_a["overlapping"] += 1
                bad_a.add((i, j))
            if gap_min is None or g < gap_min:
                gap_min, gap_arg, gap_axis = g, (i, j), k
            if g < Fraction(1, 10**6):
                d = decade(g)
                decades[d] = decades.get(d, 0) + 1
    cpu_a = time.process_time() - t0
    out["method_a"] = {
        "name": "separating axes, fractions.Fraction",
        "walls_decided": 4 * n,
        "squares_outside": walls_bad_a,
        "least_wall_clearance": fstr(clear[kmin]),
        "least_wall_clearance_float": ffloat(clear[kmin]),
        "least_wall_square": kmin + 1,
        "least_wall_square_line": lines[kmin],
        "least_wall_walls": sorted(set(which)),
        "squares_at_least_wall_clearance": at_min,
        "pairs_decided": pairs_a,
        "classes": classes_a,
        "least_pair_gap": fstr(gap_min),
        "least_pair_gap_float": ffloat(gap_min),
        "least_pair": [gap_arg[0] + 1, gap_arg[1] + 1],
        "least_pair_lines": [lines[gap_arg[0]], lines[gap_arg[1]]],
        "least_pair_axis": ["u_i", "v_i", "u_j", "v_j"][gap_axis],
        "pairs_below_1e-6_by_decade": dict(sorted(decades.items())),
        "verdict": "accept" if not walls_bad_a and not bad_a else "refuse",
        "cpu_seconds": round(cpu_a, 3),
    }

    # ---------------- method B
    t1 = time.process_time()
    sq_b = [eg.square_b(x, y, t, sense=sense) for (x, y, t) in squares]
    unit_area_ok = all(eg.area_b(p) == 1 for p in sq_b) if sense in (1, -1) else None
    deficits = [eg.wall_deficit_b(p, side) for p in sq_b]
    walls_bad_b = [i + 1 for i, d in enumerate(deficits) if d != 0]
    classes_b = {"empty": 0, "touching": 0, "overlapping": 0}
    bad_b = set()
    touch_b = set()
    pairs_b = 0
    max_area = 0
    for i in range(n):
        pi = sq_b[i]
        for j in range(i + 1, n):
            pairs_b += 1
            # clip, keeping the polygon to classify empty / zero-area / positive-area
            poly = list(pi)
            pj = sq_b[j]
            for k in range(4):
                ax, ay = pj[k]
                bx, by = pj[(k + 1) % 4]
                poly = eg._clip(poly, ax, ay, bx, by)
                if not poly:
                    break
            if not poly:
                classes_b["empty"] += 1
                continue
            a = eg.area_b(poly)
            if a < 0:
                raise AssertionError("negative area")
            if a == 0:
                classes_b["touching"] += 1
                touch_b.add((i, j))
            else:
                classes_b["overlapping"] += 1
                bad_b.add((i, j))
                if a > max_area:
                    max_area = a
    cpu_b = time.process_time() - t1
    out["method_b"] = {
        "name": "exact clipped areas, gmpy2.mpq " + eg.GMPY2_VERSION,
        "every_square_area_exactly_1": unit_area_ok,
        "walls_decided": n,
        "squares_outside": walls_bad_b,
        "pairs_decided": pairs_b,
        "classes": classes_b,
        "largest_overlap_area": fstr(Fraction(int(max_area.numerator), int(max_area.denominator)))
        if max_area
        else "0",
        "verdict": "accept" if not walls_bad_b and not bad_b else "refuse",
        "cpu_seconds": round(cpu_b, 3),
    }
    agree = (
        walls_bad_a == walls_bad_b
        and bad_a == bad_b
        and touch_a == touch_b
        and classes_a["separated"] == classes_b["empty"]
    )
    out["methods_agree_pair_by_pair"] = agree
    out["verdict"] = (
        "accept"
        if agree and out["method_a"]["verdict"] == "accept" == out["method_b"]["verdict"]
        else ("refuse" if agree else "METHODS DISAGREE")
    )
    if bad_a:
        out["overlapping_pairs_first_10"] = sorted([i + 1, j + 1] for (i, j) in bad_a)[:10]
        out["overlapping_pairs_count"] = len(bad_a)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cert")
    ap.add_argument("out")
    ap.add_argument("--sense", type=int, default=1, choices=(1, -1))
    ap.add_argument("--label", default="")
    a = ap.parse_args()
    t = time.process_time()
    r = decide(a.cert, a.sense)
    r["label"] = a.label
    r["cpu_seconds_total"] = round(time.process_time() - t, 3)
    Path(a.out).write_text(json.dumps(r, indent=1) + "\n")
    print(
        a.label or a.cert,
        r["verdict"],
        "A",
        r["method_a"]["verdict"],
        r["method_a"]["classes"],
        "B",
        r["method_b"]["verdict"],
        r["method_b"]["classes"],
        "minwall",
        r["method_a"]["least_wall_clearance_float"],
        "mingap",
        r["method_a"]["least_pair_gap_float"],
        "cpu",
        r["cpu_seconds_total"],
    )


if __name__ == "__main__":
    main()
