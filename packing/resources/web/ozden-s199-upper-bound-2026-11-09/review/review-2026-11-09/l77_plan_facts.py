"""Exact facts the controls plan states its outcomes from; decides no modified file.

Run: python -I -B l77_plan_facts.py CANDIDATE.yaml OUT.json
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import l77_checker as C  # noqa: E402


def main() -> int:
    cand, out = sys.argv[1:3]
    w = C.read_witness(cand)
    S = F(*w["side"])
    S172 = S - 1
    sq = [C.SquareA(cs) for cs in w["corners"]]
    res: dict = {"program": "l77_plan_facts.py",
                 "program_sha256": hashlib.sha256(open(__file__, "rb").read()).hexdigest(),
                 "side_denominator": str(S.denominator)}
    # square 1 clear of x = 0, so square 1 moved by (S, 0) lies wholly beyond the right wall
    res["square1_min_x"] = float(min(p[0] for p in sq[0].pts))
    res["square1_wall_clearances"] = {k: float(v) for k, v in C.walls_a(sq[0], S).items()}
    # 159 against the row: separating axis and exact gap
    s159 = sq[158]
    res["sq159_axes"] = [[C.q_str(a), C.q_str(b)] for a, b in s159.axes]
    top159 = S172 - max(p[1] for p in s159.pts)
    m184, ax184 = C.margin_a(s159, sq[183])
    m185, ax185 = C.margin_a(s159, sq[184])
    res["sq159_top_clearance_to_S172"] = C.q_str(top159)
    res["gap_159_184"] = {"value": C.q_str(m184), "axis_index": ax184, "equals_top_clearance": m184 == top159}
    res["gap_159_185"] = {"value": C.q_str(m185), "axis_index": ax185, "equals_top_clearance": m185 == top159}
    xs159 = sorted(p[0] for p in s159.pts)
    ys159 = sorted(p[1] for p in s159.pts)
    res["sq159_axis_aligned"] = len(set(xs159)) == 2 and len(set(ys159)) == 2
    res["sq159_top_corners"] = [[float(p[0]), float(S172 - p[1])] for p in s159.pts if S172 - p[1] < F(1, 10**12)]
    # 161's corners at x = S172
    s161 = sq[160]
    res["sq161_corners_at_x_S172"] = [[C.q_str(p[1]), float(p[1])] for p in s161.pts if p[0] == S172]
    res["sq161_other_old_corners_exactly_at_x_S172"] = [i + 1 for i in range(172) if i != 160 and any(p[0] == S172 for p in sq[i].pts)]
    res["old_corners_exactly_at_y_S172"] = [i + 1 for i in range(172) if any(p[1] == S172 for p in sq[i].pts)]
    # least margins of grid squares 184 and 199 against everything except their contacts
    def least_others(g: int) -> list:
        ms = []
        for i in range(199):
            if i == g:
                continue
            m, _ = C.margin_a(sq[g], sq[i])
            ms.append((m, i + 1))
        ms.sort()
        return [[i, float(m)] for m, i in ms[:4]]
    res["sq184_least_margins"] = least_others(183)
    res["sq199_least_margins"] = least_others(198)
    # old-grid pairs below 1e-12, for the pair-level closing
    near = []
    for i in range(172):
        for g in range(172, 199):
            m, _ = C.margin_a(sq[i], sq[g])
            if m < F(1, 10**12):
                near.append([i + 1, g + 1])
    res["old_grid_pairs_below_1e-12"] = near
    res["count_old_grid_below_1e-12"] = len(near)
    # least old-grid gap overall, so that every 1e-30 move of a grid square toward the old part stays clear
    least = min(C.margin_a(sq[i], sq[g])[0] for i in range(172) for g in range(172, 199))
    res["least_old_grid_gap"] = float(least)
    res["least_old_grid_gap_exceeds_1e-30"] = least > F(1, 10**30)
    with open(out, "w") as fh:
        json.dump(res, fh, indent=1)
        fh.write("\n")
    print(json.dumps({k: v for k, v in res.items() if k != "old_grid_pairs_below_1e-12"}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
