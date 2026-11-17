"""Lane L180, after the freeze: the new packing square by square against T-303.

Written for the blind stage 4 review of issue #996. It decides nothing about the bound.
It pairs the squares of the certificate with those of T-303's house witness by the
optimal assignment of least total squared centre displacement (scipy's
``linear_sum_assignment`` on binary64 distances, the lower-left frames aligned, no
symmetry), the pairing ``devtools.measure_identity`` reports as symmetry 0, and lists
for each pair the move and the turn. It tests the issue's lineage statements: T-303's
49 leaning squares against 37, seven squares in the upper left with a new angle, and
five squares along the left wall made axis-aligned.

Usage: l180_lineage.py JSON HOUSE_WITNESS OUT
"""

from __future__ import annotations

import json
import math
import os
import sys
from fractions import Fraction as F
from typing import Any

import numpy as np
import yaml
from scipy.optimize import linear_sum_assignment

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import l180_reader as R  # noqa: E402


def tilt(c: float, s: float) -> float:
    a = math.degrees(math.atan2(s, c))
    while a > 45:
        a -= 90
    while a <= -45:
        a += 90
    return a


def house_poses(path: str) -> tuple[F, list[tuple[F, F, F, F]]]:
    with open(path, encoding="utf-8") as fh:
        doc = yaml.safe_load(fh)
    w = doc["witness"]
    if w["representation"] != "center-basis" or w["coordinates"]["origin"] != "lower-left":
        raise SystemExit("not a lower-left center-basis witness")
    out = []
    for k, sq in enumerate(w["squares"], start=1):
        if sq["id"] != k:
            raise SystemExit("ids not 1..n in order")
        x, y = (R.scalar(str(v)) for v in sq["center"])
        c, s = (R.scalar(str(v)) for v in sq["basis"])
        if c * c + s * s != 1:
            raise SystemExit(f"house square {k} is not unit")
        out.append((x, y, c, s))
    return R.scalar(str(w["side"])), out


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print(__doc__)
        return 2
    r = R.read_json(argv[1])
    hside, house = house_poses(argv[2])
    new = [(float(p.x), float(p.y), tilt(float(p.c), float(p.s))) for p in r.poses]
    old = [(float(x), float(y), tilt(float(c), float(s))) for x, y, c, s in house]
    a = np.array([[x, y] for x, y, _ in new])
    b = np.array([[x, y] for x, y, _ in old])
    cost = ((a[:, None, :] - b[None, :, :]) ** 2).sum(axis=2)
    rows, cols = linear_sum_assignment(cost)
    pairs: list[dict[str, Any]] = []
    for i, j in zip(rows.tolist(), cols.tolist(), strict=True):
        move = math.dist(new[i][:2], old[j][:2])
        turn = new[i][2] - old[j][2]
        while turn > 45:
            turn -= 90
        while turn <= -45:
            turn += 90
        pairs.append(
            {
                "new": i + 1,
                "t303": j + 1,
                "new_centre": [round(new[i][0], 4), round(new[i][1], 4)],
                "t303_centre": [round(old[j][0], 4), round(old[j][1], 4)],
                "move": round(move, 6),
                "t303_tilt": round(old[j][2], 6),
                "new_tilt": round(new[i][2], 6),
                "turn": round(turn, 6),
            }
        )
    total = float(sum(cost[i, j] for i, j in zip(rows, cols, strict=True)))

    def leaning(t: float, cut: float) -> bool:
        return abs(t) > cut

    counts = {}
    for name, cut in (("exactly_upright_excluded", 0.0), ("beyond_1e-9_degrees", 1e-9), ("beyond_1e-3_degrees", 1e-3), ("beyond_1_degree", 1.0)):
        counts[name] = {
            "t303": sum(1 for _, _, t in old if leaning(t, cut)) if cut else sum(1 for x, y, c, s in house if s != 0 and c != 0),
            "new": sum(1 for _, _, t in new if leaning(t, cut)) if cut else sum(1 for p in r.poses if p.s != 0 and p.c != 0),
        }
    to_upright = [p for p in pairs if abs(p["t303_tilt"]) > 1 and abs(p["new_tilt"]) <= 1]
    to_tilted = [p for p in pairs if abs(p["t303_tilt"]) <= 1 and abs(p["new_tilt"]) > 1]
    new_angle = [p for p in pairs if abs(p["t303_tilt"]) > 1 and abs(p["new_tilt"]) > 1 and abs(p["turn"]) > 1]
    small_old = [p for p in pairs if 0 < abs(p["t303_tilt"]) <= 1]
    moved = sorted((p for p in pairs if p["move"] > 0.1), key=lambda p: -p["move"])
    out = {
        "program": "l180_lineage.py",
        "lane": "L180",
        "house_side": str(hside),
        "assignment_total_squared": round(total, 6),
        "leaning_counts": counts,
        "t303_tilted_now_upright": to_upright,
        "t303_upright_now_tilted": to_tilted,
        "tilted_in_both_turned_beyond_1_degree": new_angle,
        "t303_near_upright_squares": small_old,
        "moved_beyond_0.1": moved,
        "moved_beyond": {str(t): sum(1 for p in pairs if p["move"] > t) for t in (1e-3, 1e-2, 1e-1, 0.3)},
        "turned_beyond_1_degree": sum(1 for p in pairs if abs(p["turn"]) > 1),
        "pairs": pairs,
    }
    with open(argv[3], "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    print(
        f"total squared {total:.5f}; leaning {counts}; tilted->upright {len(to_upright)}, upright->tilted {len(to_tilted)}, "
        f"new angle {len(new_angle)}; moved beyond 0.1: {len(moved)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
