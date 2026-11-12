"""Lane L109's identity measure under five anchorings, written after the findings were frozen.

Usage: python -I -B l109_identity.py CERT.yaml TWIN.json HOUSE.yaml OUT.json

Decides nothing. Reads the certificate with the frozen reader and the house witness at
237 (center-basis, rational) with PyYAML, both in binary64 after exact reading; puts the
house under each of the eight symmetries of its box, anchored at each corner of the new
box (the house's image translated so that the corner of that name meets the new box's)
and at the box centres; and pairs the squares by SciPy's optimal assignment, of least
summed squared move and, apart, of least summed move. It reports, for each anchoring, the best symmetry and its counts:
centres moved beyond 1e-3, 0.05 and 0.1, the largest move, squares turned beyond 1
degree (angles compared modulo 90 degrees), the largest turn, and whether nearest
centres pair one to one. It also counts tilted squares (beyond 0.5 and 1 degree from
upright) and groups the new packing's tilt angles.

The issue's counts are 236 of 237 beyond 1e-3, 78 beyond 0.05, largest 1.202, 73
re-tilted beyond 1 degree, largest 43.77 degrees, 43 tilted beyond 0.5 degree against
the record's 49.
"""

from __future__ import annotations

import json
import math
import os
import sys
from fractions import Fraction as Q

import numpy as np
import yaml
from scipy.optimize import linear_sum_assignment

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import l109_check as C  # noqa: E402
import l109_reader as R  # noqa: E402

PROGRAMS = ["l109_reader.py", "l109_check.py", "l109_identity.py"]


def wrap90(a: float) -> float:
    """An angle in degrees modulo 90, in [-45, 45)."""
    return (a + 45.0) % 90.0 - 45.0


def new_packing(cert: str, twin: str) -> tuple[float, np.ndarray, np.ndarray]:
    rd = R.read_files(cert, twin)
    side = float(Q(*rd.side))
    cs, an = [], []
    for sq in rd.corners:
        pts = [(Q(*x), Q(*y)) for x, y in sq]
        cx = sum((p[0] for p in pts), Q(0)) / 4
        cy = sum((p[1] for p in pts), Q(0)) / 4
        ux, uy = pts[1][0] - pts[0][0], pts[1][1] - pts[0][1]
        cs.append((float(cx), float(cy)))
        an.append(wrap90(math.degrees(math.atan2(float(uy), float(ux)))))
    return side, np.array(cs), np.array(an)


def house_packing(path: str) -> tuple[float, np.ndarray, np.ndarray]:
    with open(path, encoding="utf-8") as f:
        w = yaml.safe_load(f)["witness"]
    assert w["representation"] == "center-basis"
    side = float(Q(w["side"]))
    cs, an = [], []
    for sq in w["squares"]:
        cs.append((float(Q(sq["center"][0])), float(Q(sq["center"][1]))))
        c, s = float(Q(sq["basis"][0])), float(Q(sq["basis"][1]))
        an.append(wrap90(math.degrees(math.atan2(s, c))))
    return side, np.array(cs), np.array(an)


def symmetry(k: int, xy: np.ndarray, ang: np.ndarray, L: float) -> tuple[np.ndarray, np.ndarray]:
    """The k-th symmetry of the box [0, L]^2: rotation by 90 k degrees, then a reflection for k >= 4."""
    x, y = xy[:, 0] - L / 2, xy[:, 1] - L / 2
    a = ang.copy()
    r = k % 4
    for _ in range(r):
        x, y = -y, x
    if k >= 4:  # reflect in the vertical line x = L/2
        x = -x
        a = -a
    return np.stack([x + L / 2, y + L / 2], axis=1), np.array([wrap90(v) for v in a])


def measure(new_xy: np.ndarray, new_a: np.ndarray, h_xy: np.ndarray, h_a: np.ndarray, squared: bool) -> dict[str, object]:
    d2 = ((new_xy[:, None, :] - h_xy[None, :, :]) ** 2).sum(axis=2)
    rows, cols = linear_sum_assignment(d2 if squared else np.sqrt(d2))
    mv = np.sqrt(d2[rows, cols])
    turn = np.abs(np.array([wrap90(new_a[i] - h_a[j]) for i, j in zip(rows, cols, strict=True)]))
    nearest = d2.argmin(axis=1)
    return {
        "cost": float(d2[rows, cols].sum()) if squared else float(np.sqrt(d2[rows, cols]).sum()),
        "beyond_1e-3": int((mv > 1e-3).sum()),
        "beyond_0.05": int((mv > 0.05).sum()),
        "beyond_0.1": int((mv > 0.1).sum()),
        "largest_move": round(float(mv.max()), 4),
        "turned_beyond_1_degree": int((turn > 1).sum()),
        "largest_turn_degrees": round(float(turn.max()), 2),
        "nearest_centres_distinct": len(set(nearest.tolist())),
    }


def main() -> int:
    cert, twin, house_path, out = sys.argv[1:5]
    S, nxy, na = new_packing(cert, twin)
    L, hxy, ha = house_packing(house_path)
    anchors = {
        "lower-left": (0.0, 0.0),
        "lower-right": (S - L, 0.0),
        "upper-left": (0.0, S - L),
        "upper-right": (S - L, S - L),
        "centred": ((S - L) / 2, (S - L) / 2),
    }
    results: dict[str, dict[str, object]] = {}
    for squared in (True, False):
        key = "least_summed_squared_move" if squared else "least_summed_move"
        results[key] = {}
        for name, (dx, dy) in anchors.items():
            best = None
            for k in range(8):
                sxy, sa = symmetry(k, hxy, ha, L)
                sxy = sxy + np.array([dx, dy])
                m = measure(nxy, na, sxy, sa, squared)
                m["symmetry"] = k
                if best is None or m["cost"] < best["cost"]:  # type: ignore[operator]
                    best = m
            results[key][name] = best
    tilt_new = np.abs(na)
    tilt_house = np.abs(ha)
    # group the new packing's tilted angles (beyond 0.5 degree) to within 0.01 degree
    tilted = sorted(float(v) for v in na if abs(v) > 0.5)
    groups: list[list[float]] = []
    for v in tilted:
        if groups and v - groups[-1][-1] <= 0.01:
            groups[-1].append(v)
        else:
            groups.append([v])
    receipt = {
        "program": "l109_identity.py",
        "programs_sha256": C.program_digests(PROGRAMS),
        "decides": "nothing",
        "new_side": S,
        "house_side": L,
        "anchorings": results,
        "tilted": {
            "new_beyond_0.5": int((tilt_new > 0.5).sum()),
            "new_beyond_1": int((tilt_new > 1).sum()),
            "house_beyond_0.5": int((tilt_house > 0.5).sum()),
            "house_beyond_1": int((tilt_house > 1).sum()),
            "new_angle_groups": [
                {"count": len(g), "from": round(g[0], 4), "to": round(g[-1], 4)} for g in groups
            ],
        },
    }
    with open(out, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=1)
        f.write("\n")
    print(json.dumps(receipt, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
