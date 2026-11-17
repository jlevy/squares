"""Decide each house witness and measure its uniform-contraction margin exactly (review L83).

Usage: python -I -B l83_houses.py N KNOWN_BEST_DIR OUT.json

Centres scale by a common lambda <= 1, orientations kept. On each of a pair's four axes
the gap whose slope is positive is |d| lambda - (h_i + h_j), with d the centres'
separation along the axis and h the half-widths, so a pair first touches at
min (h_i + h_j) / |d| over its axes, and the packing at lambda* = the largest of those.
The margin is the house side less the contracted extent; the wall part is the side less
the uncontracted extent. The contracted packing is then decided at lambda* (accepted,
the binding pair touching) and 10^-30 below it (refused), over every square and pair.
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import l83_check as C  # noqa: E402
import l83_geom as G  # noqa: E402
import l83_house as H  # noqa: E402


def half(u, a):
    return (abs(u[0] * a[0] + u[1] * a[1]) + abs(-u[1] * a[0] + u[0] * a[1])) / 2


def extent(cs, us, lam):
    ex = []
    for k in (0, 1):
        axis = (F(1), F(0)) if k == 0 else (F(0), F(1))
        hi = max(lam * c[k] + half(u, axis) for c, u in zip(cs, us))
        lo = min(lam * c[k] - half(u, axis) for c, u in zip(cs, us))
        ex.append((lo, hi))
    return ex


def packing(cs, us, lam, ex):
    lo_x, lo_y = ex[0][0], ex[1][0]
    side = max(ex[0][1] - ex[0][0], ex[1][1] - ex[1][0])
    corners = [G.to_pq(H.corners((lam * c[0] - lo_x, lam * c[1] - lo_y), u)) for c, u in zip(cs, us)]
    return (side.numerator, side.denominator), corners


def main(argv):
    n, kb, out = int(argv[1]), Path(argv[2]), Path(argv[3])
    t0 = time.process_time()
    hn, S, ids, cs, us = H.read_rational(kb / f"n-{n}.yaml")
    corners = [G.to_pq(H.corners(c, u)) for c, u in zip(cs, us)]
    idx = list(range(1, hn + 1))
    base = C.decide(hn, (S.numerator, S.denominator), idx, corners)
    summ = C.summary(base, (S.numerator, S.denominator))
    lam_best, binding = F(0), None
    for i, j in combinations(range(hn), 2):
        lp = None
        for a in (us[i], (-us[i][1], us[i][0]), us[j], (-us[j][1], us[j][0])):
            d = abs((cs[j][0] - cs[i][0]) * a[0] + (cs[j][1] - cs[i][1]) * a[1])
            if d == 0:
                continue
            v = (half(us[i], a) + half(us[j], a)) / d
            if lp is None or v < lp:
                lp = v
        if lp is not None and lp > lam_best:
            lam_best, binding = lp, (ids[i], ids[j])
    ex1 = extent(cs, us, F(1))
    exs = extent(cs, us, lam_best)
    e1 = max(ex1[0][1] - ex1[0][0], ex1[1][1] - ex1[1][0])
    es = max(exs[0][1] - exs[0][0], exs[1][1] - exs[1][0])
    margin = S - es
    side_c, corners_c = packing(cs, us, lam_best, exs)
    at = C.decide(hn, side_c, idx, corners_c)
    lam_past = lam_best - F(1, 10**30)
    exp = extent(cs, us, lam_past)
    side_p, corners_p = packing(cs, us, lam_past, exp)
    past = C.decide(hn, side_p, idx, corners_p)
    doc = {
        "n": n,
        "house_file": f"packing/witnesses/known-best/n-{n}.yaml",
        "house_side": f"{S.numerator}/{S.denominator}",
        "house_check": {k: summ[k] for k in ("verdict", "pairs_decided", "touching_pairs", "overlapping_pairs", "wall_contacts", "least_pair_margin", "least_positive_wall_clearance", "pairs_below_1e-12")},
        "lambda_star": str(lam_best),
        "one_minus_lambda_star": float(1 - lam_best),
        "binding_pair": binding,
        "uncontracted_extent": str(e1),
        "margin": str(margin),
        "margin_float": float(margin),
        "wall_part": float(S - e1),
        "pair_part": float(e1 - es),
        "margin_over_side": float(margin / S),
        "contracted_at_lambda_star": {"verdict": "ACCEPT" if at["accept"] else "REFUSE", "touching": at["touching"], "overlaps": len(at["overlaps"])},
        "contracted_1e-30_below": {"verdict": "ACCEPT" if past["accept"] else "REFUSE", "overlapping_pairs": len(past["overlaps"]), "touching": len(past["touching"])},
        "cpu_seconds": round(time.process_time() - t0, 1),
        "programs": C.program_digests(),
    }
    out.write_text(json.dumps(doc, indent=1) + "\n")
    print(n, doc["house_check"]["verdict"], "lam*", doc["one_minus_lambda_star"], "margin", doc["margin_float"], "wall", doc["wall_part"], "pair", doc["pair_part"], doc["contracted_at_lambda_star"], doc["contracted_1e-30_below"], "cpu", doc["cpu_seconds"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
