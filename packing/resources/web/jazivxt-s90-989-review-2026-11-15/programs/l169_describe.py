"""Lane L169 description: tilts, near pairs, near-wall clearances and extents.

Usage: l169_describe.py CERT CHECK_JSON OUT_JSON

It decides nothing. Exact values come from method A's functions; angles in degrees and
decimal prints are information only.
"""

from __future__ import annotations

import json
import math
import os
import sys
import time
from collections import Counter
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I leaves it off

import l169_decide as dec
import l169_reader as rd
import l169_sat as sat


def main(argv: list[str]) -> int:
    t0 = time.process_time()
    reading = rd.read_file(argv[1])
    check = json.load(open(argv[2]))
    sq = reading["squares"]
    n = len(sq)
    side = reading["side"]
    S = F(*side)
    A = [sat.Square(*r) for r in sq]
    ts = [F(*r[2]) for r in sq]
    deg = [math.degrees(2 * math.atan(float(t))) for t in ts]
    tilt_counts = Counter(round(d, 4) for d in deg)
    distinct_t = Counter(ts)
    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            m = sat.pair_margin(A[i], A[j])
            pairs.append((m, i + 1, j + 1, sat.binding_axes(A[i], A[j])))
    pairs.sort()
    near = [p for p in pairs if p[0] < F(1, 10**3)]
    near_vals = [p[0] for p in near]
    tiny = [p for p in pairs if p[0] < F(1, 10**10)]
    med = tiny[len(tiny) // 2][0] if tiny else None
    gap_after = next((p for p in pairs if p[0] >= F(1, 10**10)), None)
    clear = []
    for k in range(n):
        for w, c in sat.clearances(A[k], side).items():
            clear.append((c, k + 1, w))
    clear.sort()
    xs_lo = min(F(a.X, a.E) - F(a.ext, 2 * a.r) for a in A)
    xs_hi = max(F(a.X, a.E) + F(a.ext, 2 * a.r) for a in A)
    ys_lo = min(F(a.Y, a.E) - F(a.ext, 2 * a.r) for a in A)
    ys_hi = max(F(a.Y, a.E) + F(a.ext, 2 * a.r) for a in A)
    # Clusters of near-pair margins: exact values and how many pairs share each.
    vc = Counter(p[0] for p in tiny)
    out = {
        "program": "l169_describe.py",
        "n": n,
        "squares_t_zero": sum(1 for t in ts if t == 0),
        "squares_within_1e-3_degree_not_zero": sum(1 for t, d in zip(ts, deg, strict=True) if t != 0 and abs(d) < 1e-3),
        "squares_turned_beyond_0.5_degree": sum(1 for d in deg if abs(d) > 0.5),
        "turned_positive": sum(1 for d in deg if d > 0.5),
        "turned_negative": sum(1 for d in deg if d < -0.5),
        "tilt_degrees_counts": sorted([[k, v] for k, v in tilt_counts.items()], key=lambda x: -x[1]),
        "distinct_t": len(distinct_t),
        "t_values": sorted([[dec.frac_str(t), v, round(math.degrees(2 * math.atan(float(t))), 6)] for t, v in distinct_t.items()], key=lambda x: -x[1]),
        "squares_by_t": {dec.frac_str(t): [k + 1 for k in range(n) if ts[k] == t] for t in distinct_t},
        "near_pairs_below_1e-3": len(near),
        "pairs_below_1e-10": len(tiny),
        "pairs_below_1e-10_range": [dec.sci(tiny[0][0]), dec.sci(tiny[-1][0])] if tiny else None,
        "pairs_below_1e-10_median": dec.sci(med) if med is not None else None,
        "pairs_below_1e-10_distinct_margins": len(vc),
        "pairs_below_1e-10_most_common": [[dec.sci(m, 12), c] for m, c in vc.most_common(8)],
        "first_pair_at_or_above_1e-10": None if gap_after is None else {"pair": [gap_after[1], gap_after[2]], "approx": dec.sci(gap_after[0])},
        "near_pairs_listing": [[i, j, dec.sci(m, 8), b] for m, i, j, b in near],
        "binding_axes_below_1e-10": dict(Counter(p[3] for p in tiny)),
        "least_clearances": [[k, w, dec.sci(c, 8)] for c, k, w in clear[:40]],
        "distinct_clearances_below_1e-12": sorted({dec.sci(c, 10) for c, _, _ in clear if c < F(1, 10**12)}),
        "extent_x": [dec.sci(xs_lo, 8), dec.frac_str(S - xs_hi), dec.sci(S - xs_hi, 8)],
        "extent_y": [dec.sci(ys_lo, 8), dec.frac_str(S - ys_hi), dec.sci(S - ys_hi, 8)],
        "width_x": dec.sci(xs_hi - xs_lo, 16),
        "width_y": dec.sci(ys_hi - ys_lo, 16),
        "side_less_widths": [dec.sci(S - (xs_hi - xs_lo), 10), dec.sci(S - (ys_hi - ys_lo), 10)],
        "check_least_margin": check["decision"]["least_margin"]["approx"],
        "cpu_seconds": 0.0,
    }
    out["cpu_seconds"] = round(time.process_time() - t0, 2)
    with open(argv[3], "w") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    for k in ("squares_t_zero", "squares_within_1e-3_degree_not_zero", "squares_turned_beyond_0.5_degree",
              "turned_positive", "turned_negative", "distinct_t", "near_pairs_below_1e-3", "pairs_below_1e-10",
              "pairs_below_1e-10_range", "pairs_below_1e-10_median", "pairs_below_1e-10_distinct_margins",
              "first_pair_at_or_above_1e-10", "binding_axes_below_1e-10", "extent_x", "extent_y", "side_less_widths"):
        print(k, out[k])
    print("t_values", out["t_values"])
    print("most common near margins", out["pairs_below_1e-10_most_common"])
    print("distinct clearances below 1e-12", out["distinct_clearances_below_1e-12"])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
