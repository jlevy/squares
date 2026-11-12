"""Lane L117, after the freeze: the issue's lineage counts against T-290. Decides nothing.

Reads the certificate (frozen reader) and the house witness (center-basis rational,
read as data). Places the house under each of the eight symmetries of its box, anchored
at each corner of the new box and at its centre, and pairs squares by an optimal
assignment of least summed move and of least summed squared move (SciPy). For each it
counts centres moved beyond 1e-3, 0.05 and 0.1, the largest move, the squares turned
beyond 1 degree (modulo a quarter turn) and the largest turn, in binary64.

Usage: python -I -B l117_lineage.py CERT.yaml TWIN.json HOUSE.yaml OUT.json
"""

from __future__ import annotations

import json
import math
import os
import sys
from fractions import Fraction as F

import numpy as np
import yaml
from scipy.optimize import linear_sum_assignment

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import l117_geom as g  # noqa: E402
import l117_reader as rd  # noqa: E402


def wrap(a: float) -> float:
    a = math.fmod(a, 90.0)
    if a > 45:
        a -= 90
    if a <= -45:
        a += 90
    return a


def main(argv: list[str]) -> int:
    ypath, jpath, hpath, opath = argv[1:5]
    rec = rd.read_files(ypath, jpath)
    side = rec["side"]
    sq = rec["squares"]
    assert isinstance(side, tuple) and isinstance(sq, list)
    S = float(F(side[0], side[1]))
    new_c, new_a = [], []
    for c in sq:
        cc, u, _ = g.pose(g.from_rat(c))
        new_c.append((float(cc[0]), float(cc[1])))
        new_a.append(math.degrees(math.atan2(float(u[1]), float(u[0]))))
    with open(hpath, encoding="utf-8") as fh:
        house = yaml.safe_load(fh)["witness"]
    T = float(F(house["side"]))
    h_c = [(float(F(s["center"][0])), float(F(s["center"][1]))) for s in house["squares"]]
    h_a = [math.degrees(math.atan2(float(F(s["basis"][1])), float(F(s["basis"][0])))) for s in house["squares"]]
    N = np.array(new_c)
    na = np.array(new_a)

    syms = {
        0: lambda x, y, a: (x, y, a),
        1: lambda x, y, a: (T - y, x, a),
        2: lambda x, y, a: (T - x, T - y, a),
        3: lambda x, y, a: (y, T - x, a),
        4: lambda x, y, a: (T - x, y, -a),
        5: lambda x, y, a: (x, T - y, -a),
        6: lambda x, y, a: (y, x, -a),
        7: lambda x, y, a: (T - y, T - x, -a),
    }
    names = {0: "identity", 1: "quarter turn", 2: "half turn", 3: "three-quarter turn",
             4: "reflected left to right", 5: "reflected top to bottom", 6: "transposed",
             7: "anti-transposed"}
    d = S - T
    anchors = {"lower-left": (0.0, 0.0), "lower-right": (d, 0.0), "upper-left": (0.0, d),
               "upper-right": (d, d), "centre": (d / 2, d / 2)}
    rows = []
    for k, f in syms.items():
        H = [f(x, y, a) for (x, y), a in zip(h_c, h_a, strict=True)]
        for an, (sx, sy) in anchors.items():
            Hc = np.array([(x + sx, y + sy) for x, y, _ in H])
            ha = np.array([a for _, _, a in H])
            D = np.sqrt(((N[:, None, :] - Hc[None, :, :]) ** 2).sum(axis=2))
            for cost in ("summed", "squared"):
                r, c = linear_sum_assignment(D if cost == "summed" else D * D)
                mv = D[r, c]
                turn = np.array([abs(wrap(na[i] - ha[j])) for i, j in zip(r, c, strict=True)])
                rows.append({
                    "symmetry": names[k], "anchor": an, "assignment": f"least {cost} move",
                    "total": round(float(mv.sum()), 4),
                    "beyond_1e-3": int((mv > 1e-3).sum()), "beyond_0.05": int((mv > 0.05).sum()),
                    "beyond_0.1": int((mv > 0.1).sum()), "largest_move": round(float(mv.max()), 4),
                    "turned_beyond_1_degree": int((turn > 1).sum()),
                    "largest_turn": round(float(turn.max()), 2),
                })
    best = {cost: min((r for r in rows if r["assignment"] == f"least {cost} move"), key=lambda r: r["total"])
            for cost in ("summed", "squared")}
    issue = {"beyond_1e-3": 262, "beyond_0.05": 124, "largest_move": 1.456, "turned_beyond_1_degree": 116,
             "largest_turn": 44.77}
    def agrees(r: dict) -> bool:
        """Equal at the issue's printed precision (3 places for the move, 2 for the turn)."""
        return (r["beyond_1e-3"] == 262 and r["beyond_0.05"] == 124 and round(r["largest_move"], 3) == 1.456
                and r["turned_beyond_1_degree"] == 116 and r["largest_turn"] == 44.77)

    match = [r for r in rows if agrees(r)]
    near = sorted(rows, key=lambda r: abs(r["beyond_1e-3"] - 262) + abs(r["beyond_0.05"] - 124)
                  + 100 * abs(r["largest_move"] - 1.456))[:4]
    hc = np.array(h_c)
    house_tilted = int(sum(1 for a in h_a if abs(wrap(a)) > 0.5))
    out = {
        "program": "l117_lineage.py",
        "new_side_less_house_side": S - T,
        "house_tilted_beyond_0.5": house_tilted,
        "house_centre_span": [float(hc[:, 0].min()), float(hc[:, 0].max())],
        "issue_counts": issue,
        "rows_matching_issue": match,
        "rows_nearest_issue": near,
        "least_total": best,
        "rows": rows,
    }
    with open(opath, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    print("matching", json.dumps(match))
    print("nearest", json.dumps(near, indent=0))
    print("least total", json.dumps(best, indent=0))
    print("house tilted", house_tilted)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
