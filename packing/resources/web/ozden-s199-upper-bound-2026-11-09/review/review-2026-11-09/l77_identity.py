"""#938 against the 199 house (T-127's witness on main) and T-282 against T-257; decides nothing.

Pose by pose in binary64: for each of the eight symmetries of the reference box, anchored
at the lower-left corner, nearest-centre pairing and SciPy's optimal assignment of least
summed squared move. A turn is the change of edge direction modulo 90 degrees. Also counts
the house's own axis-aligned squares in the band of width 1 along each wall.

Run: python -I -B l77_identity.py CANDIDATE.yaml MAIN_N199.yaml OUT.json
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import sys
from fractions import Fraction as F

import numpy as np
import yaml
from scipy.optimize import linear_sum_assignment

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import l77_checker as C  # noqa: E402


def from_corners(cs: list) -> tuple[float, float, float]:
    sq = C.SquareA(cs)
    cx = float((sq.pts[0][0] + sq.pts[2][0]) / 2)
    cy = float((sq.pts[0][1] + sq.pts[2][1]) / 2)
    ux, uy = sq.axes[0]
    return cx, cy, math.degrees(math.atan2(float(uy), float(ux)))


def read_cb(path: str) -> tuple[F, list[tuple[float, float, float]], list]:
    w = yaml.safe_load(open(path))["witness"]
    side = F(*C.parse_scalar(str(w["side"])))
    out = []
    exact = []
    for e in w["squares"]:
        c = [F(*C.parse_scalar(str(v))) for v in e["center"]]
        b = [F(*C.parse_scalar(str(v))) for v in e["basis"]]
        out.append((float(c[0]), float(c[1]), math.degrees(math.atan2(float(b[1]), float(b[0])))))
        exact.append((c, b))
    return side, out, exact


def turn(a: float, b: float) -> float:
    d = (a - b) % 90.0
    return min(d, 90.0 - d)


def sym(p: tuple[float, float, float], k: int, s: float) -> tuple[float, float, float]:
    x, y, a = p
    for _ in range(k % 4):
        x, y, a = s - y, x, a + 90.0
    if k >= 4:
        x, a = s - x, -a
    return x, y, a


def compare(new: list, ref: list, s_ref: float) -> dict:
    best = None
    for k in range(8):
        m = [sym(p, k, s_ref) for p in new]
        A = np.array([[p[0], p[1]] for p in m])
        B = np.array([[p[0], p[1]] for p in ref])
        D = ((A[:, None, :] - B[None, :, :]) ** 2).sum(-1)
        nearest = D.argmin(1)
        r, c = linear_sum_assignment(D)
        moves = np.sqrt(D[r, c])
        turns = np.array([turn(m[i][2], ref[j][2]) for i, j in zip(r, c)])
        rec = {"symmetry": k, "nearest_distinct": int(len(set(nearest.tolist()))),
               "moved_beyond": {t: 0 for t in ("1e-9", "1e-3", "0.05", "0.1", "0.5")},
               "largest_move": float(moves.max()), "turned_beyond_1deg": int((turns > 1).sum()),
               "largest_turn_deg": float(turns.max()), "same_id": int(sum(1 for i, j in zip(r, c) if i == j)),
               "sum_sq": float((moves ** 2).sum())}
        rec["moved_beyond"] = {k2: int((moves > float(k2)).sum()) for k2 in rec["moved_beyond"]}
        if best is None or rec["sum_sq"] < best["sum_sq"]:
            best = rec
            best["moved_list"] = [[int(i) + 1, int(j) + 1, round(float(mv), 4)] for i, j, mv in zip(r, c, moves) if mv > 0.1][:60]
    return best


def main() -> int:
    cand, house, out = sys.argv[1:4]
    w = C.read_witness(cand)
    new = [from_corners(cs) for cs in w["corners"]]
    s_h, ref, exact = read_cb(house)
    res: dict = {"program": "l77_identity.py", "program_sha256": hashlib.sha256(open(__file__, "rb").read()).hexdigest(),
                 "house_sha256": hashlib.sha256(open(house, "rb").read()).hexdigest(), "house_side": float(s_h)}
    # the house's axis-aligned squares wholly inside the band of width 1 along each wall
    band = {"left": [], "right": [], "bottom": [], "top": []}
    tol = F(1, 10**9)  # the house certificate is padded, so a wall square sits a hair off its wall
    for i, (c, b) in enumerate(exact):
        if b[0] * b[1] != 0:
            continue
        lo_x, hi_x, lo_y, hi_y = c[0] - F(1, 2), c[0] + F(1, 2), c[1] - F(1, 2), c[1] + F(1, 2)
        if hi_x <= 1 + tol:
            band["left"].append(i + 1)
        if lo_x >= s_h - 1 - tol:
            band["right"].append(i + 1)
        if hi_y <= 1 + tol:
            band["bottom"].append(i + 1)
        if lo_y >= s_h - 1 - tol:
            band["top"].append(i + 1)
    res["house_band_ids"] = band
    res["house_axis_aligned"] = sum(1 for c, b in exact if b[0] * b[1] == 0)
    res["house_band_counts"] = {k: len(v) for k, v in band.items()}
    res["house_L_top_right"] = len(set(band["top"]) | set(band["right"]))
    res["new_vs_house"] = compare(new, ref, float(s_h))
    res["new_tilted_beyond_0.5deg"] = sum(1 for p in new if turn(p[2], 0) > 0.5)
    res["house_tilted_beyond_0.5deg"] = sum(1 for p in ref if turn(p[2], 0) > 0.5)
    with open(out, "w") as fh:
        json.dump(res, fh, indent=1)
        fh.write("\n")
    print(json.dumps({k: v for k, v in res.items()}, indent=1)[:4000])
    return 0


if __name__ == "__main__":
    sys.exit(main())
