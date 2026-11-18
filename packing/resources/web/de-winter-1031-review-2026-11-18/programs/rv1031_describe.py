"""Describe a packing's structure for the review of jlevy/squares#1031 (decides nothing).

Written after the checker's freeze; imports nothing from this repository or the source.

    python -I -B rv1031_describe.py --kind json --file n299_exact.json --out describe.json

Exact, from the file's rationals: the upright squares, the distinct directions, the pairs
whose centres are less than sqrt 2 apart (the issue's "close pairs"), the near pairs
(margin below 1e-30) and each one's contact factor ``1 - H/M``, the clearances, and the
scalar lengths.  In binary64, for reading only: each tilt in degrees, the counts turned
at least 15 degrees either way, and where the tilted squares lie along the two diagonals
(``x + y`` and ``x - y``).
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from collections import Counter
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # this packet's own modules, under python -I

import rv1031_axes as A
import rv1031_decide as D
import rv1031_reader as R


def tilt_deg(ux: F, uy: F) -> float:
    a = math.degrees(math.atan2(float(uy), float(ux))) % 90.0
    return a - 90.0 if a > 45.0 else a


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--kind", required=True)
    ap.add_argument("--file", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    doc = R.read_any(args.file, args.kind, require_claim=False)
    poses = doc["poses"]
    side = doc["side"]
    n = doc["n"]
    upright = [k for k, p in enumerate(poses) if p[2] * p[3] == 0]
    tilts = [tilt_deg(p[2], p[3]) for p in poses]
    dirs = Counter((abs(p[2]), abs(p[3])) if abs(p[2]) >= abs(p[3]) else (abs(p[3]), abs(p[2])) for p in poses)
    signed_dirs = Counter(round(t, 9) for t in tilts)
    pos15 = [k + 1 for k, t in enumerate(tilts) if t >= 15.0]
    neg15 = [k + 1 for k, t in enumerate(tilts) if t <= -15.0]
    close = 0
    near = []
    factors = []
    for i in range(n):
        for j in range(i + 1, n):
            dx = poses[j][0] - poses[i][0]
            dy = poses[j][1] - poses[i][1]
            if dx * dx + dy * dy < 2:
                close += 1
            m, h, _ = A.pair_terms(poses[i], poses[j])
            if m - h < F(1, 10**30):
                near.append((i, j, m - h))
                factors.append(1 - h / m)
    near_close = 0
    for i, j, _ in near:
        dx = poses[j][0] - poses[i][0]
        dy = poses[j][1] - poses[i][1]
        if dx * dx + dy * dy < 2:
            near_close += 1
    clear = A.all_clearances(poses, side)
    tilted = [k for k in range(n) if k not in set(upright)]

    def band(ks: list[int], f) -> dict:
        vals = sorted(f(poses[k]) for k in ks)
        return {"min": vals[0], "max": vals[-1]} if vals else {}

    groups = {}
    for name, ks in (("tilted_positive", [k for k in tilted if tilts[k] > 0]), ("tilted_negative", [k for k in tilted if tilts[k] < 0])):
        groups[name] = {
            "count": len(ks),
            "x_plus_y": band(ks, lambda p: float(p[0] + p[1])),
            "x_minus_y": band(ks, lambda p: float(p[0] - p[1])),
            "x": band(ks, lambda p: float(p[0])),
            "y": band(ks, lambda p: float(p[1])),
            "tilt_deg_range": [min(tilts[k] for k in ks), max(tilts[k] for k in ks)] if ks else [],
            "squares": [k + 1 for k in ks],
        }
    hist_xpy = Counter(int(float(poses[k][0] + poses[k][1]) // 1) for k in tilted)
    hist_xmy = Counter(int(float(poses[k][0] - poses[k][1]) // 1) for k in tilted)
    rec = {
        "program": "rv1031_describe.py",
        "file": args.file,
        "n": n,
        "side": D.short(side, 20),
        "upright": len(upright),
        "tilted": len(tilted),
        "tilted_at_least_15_deg_positive": len(pos15),
        "tilted_at_least_15_deg_negative": len(neg15),
        "tilt_abs_max_deg": max(abs(t) for t in tilts),
        "tilt_abs_min_nonzero_deg": min((abs(t) for t in tilts if t != 0), default=None),
        "distinct_directions_unsigned": len(dirs),
        "distinct_tilts_signed_1e-9_deg": len(signed_dirs),
        "close_pairs_centres_below_sqrt2": close,
        "near_pairs_margin_below_1e-30": len(near),
        "near_pairs_also_close": near_close,
        "near_margin_range": [D.short(min(m for _, _, m in near)), D.short(max(m for _, _, m in near))] if near else [],
        "near_one_less_contact_factor_range": [D.short(min(factors)), D.short(max(factors))] if factors else [],
        "near_one_less_contact_factor_distinct_12_figures": len({D.short(f) for f in factors}),
        "near_one_less_contact_factor_commonest": Counter(D.short(f, 6) for f in factors).most_common(5),
        "clearances_left_bottom_zero": sum(1 for c in clear for w in (0, 1) if c[w] == 0),
        "clearances_right_top_least": D.short(min(min(c[2], c[3]) for c in clear)),
        "clearances_right_top_below_1e-60": sum(1 for c in clear for w in (2, 3) if c[w] < F(1, 10**60)),
        "clearances_left_bottom_positive_below_1e-60": sum(1 for c in clear for w in (0, 1) if 0 < c[w] < F(1, 10**60)),
        "groups": groups,
        "tilted_by_x_plus_y_unit_bins": dict(sorted(hist_xpy.items())),
        "tilted_by_x_minus_y_unit_bins": dict(sorted(hist_xmy.items())),
        "denominator_digits_max": max(len(str(v.denominator)) for p in poses for v in p),
        "tilts_deg": [round(t, 6) for t in tilts],
    }
    with open(args.out, "w") as fh:
        json.dump(rec, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(json.dumps({k: rec[k] for k in rec if k not in ("groups", "tilts_deg", "tilted_by_x_plus_y_unit_bins", "tilted_by_x_minus_y_unit_bins")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
