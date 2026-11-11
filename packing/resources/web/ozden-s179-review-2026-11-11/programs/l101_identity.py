"""Measure the certificate pose by pose against the house at 179. Decides nothing.

Usage: python -I -B l101_identity.py SOURCE_DIR HOUSE.yaml OUT.json

In binary64. The house's squares are mapped by each of the eight symmetries of its box,
anchored at each corner of the box (the corner of the same name meeting) or, apart, at the box centres, and matched to the new
squares by nearest centre and by SciPy's optimal assignment of least summed move and of
least summed squared move. A turn is the change of edge direction modulo 90 degrees,
folded to [0, 45]; a square is tilted when its own direction modulo 90 is beyond 0.5
degrees from upright.
"""

from __future__ import annotations

import json
import math
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.set_int_max_str_digits(0)

import numpy as np  # noqa: E402
import yaml  # noqa: E402
from scipy.optimize import linear_sum_assignment  # noqa: E402

import l101_geom as geom  # noqa: E402
import l101_reader as reader  # noqa: E402
from l101_check import sha256_file  # noqa: E402

ANCHORS = ("lower-left", "lower-right", "upper-left", "upper-right", "centred")
SYMS = ("identity", "flip-x", "flip-y", "half-turn", "transpose", "rot+90", "rot-90", "antitranspose")


def fold(deg: float) -> float:
    """Direction modulo 90 degrees, in (-45, 45]."""
    r = math.fmod(deg, 90.0)
    if r > 45:
        r -= 90
    if r <= -45:
        r += 90
    return r


def turn(a: float, b: float) -> float:
    return abs(fold(a - b))


def apply(sym: str, x: float, y: float, side: float, ang: float) -> tuple[float, float, float]:
    h = side
    return {
        "identity": (x, y, ang),
        "flip-x": (h - x, y, -ang),
        "flip-y": (x, h - y, -ang),
        "half-turn": (h - x, h - y, ang),
        "transpose": (y, x, -ang),
        "rot+90": (h - y, x, ang),
        "rot-90": (y, h - x, ang),
        "antitranspose": (h - y, h - x, -ang),
    }[sym]


def load_new(src: Path) -> tuple[float, np.ndarray, np.ndarray]:
    w = reader.read_files(src / "n-179-candidate.yaml", src / "n179-witness.json", 179)
    cs, angs = [], []
    for sq in w.squares:
        c = geom.centre(sq)
        p = geom.to_fracs(sq)
        u = (p[1][0] - p[0][0], p[1][1] - p[0][1])
        cs.append((float(c[0]), float(c[1])))
        angs.append(math.degrees(math.atan2(float(u[1]), float(u[0]))))
    return float(F(*w.side)), np.array(cs), np.array(angs)


def load_house(path: Path) -> tuple[float, np.ndarray, np.ndarray]:
    w = yaml.safe_load(path.read_text(encoding="utf-8"))["witness"]
    cs, angs = [], []
    for sq in w["squares"]:
        cx, cy = (float(F(str(v))) for v in sq["center"])
        c, s = (float(F(str(v))) for v in sq["basis"])
        cs.append((cx, cy))
        angs.append(math.degrees(math.atan2(s, c)))
    return float(F(str(w["side"]))), np.array(cs), np.array(angs)


def measure(new_c, new_a, house_c, house_a, house_side, new_side, sym, anchor, cost):
    hc = np.array([apply(sym, x, y, house_side, 0.0)[:2] for x, y in house_c])
    ha = np.array([apply(sym, 0.0, 0.0, house_side, a)[2] for a in house_a])
    nc = new_c.copy()
    if anchor == "centred":
        hc = hc - house_side / 2
        nc = nc - new_side / 2
    else:
        # Anchored at a corner of the box: the house's image is translated so that its
        # box's corner of that name meets the new box's.
        delta = new_side - house_side
        shift = {"lower-left": (0.0, 0.0), "lower-right": (delta, 0.0),
                 "upper-left": (0.0, delta), "upper-right": (delta, delta)}[anchor]
        hc = hc + np.array(shift)
    d = np.linalg.norm(nc[:, None, :] - hc[None, :, :], axis=2)
    nearest = d.argmin(axis=1)
    rows, cols = linear_sum_assignment(d if cost == "sum" else d**2)
    moves = d[rows, cols]
    turns = np.array([turn(new_a[r], ha[c]) for r, c in zip(rows, cols, strict=True)])
    return {
        "symmetry": sym,
        "anchor": anchor,
        "cost": cost,
        "total_cost": float(moves.sum() if cost == "sum" else (moves**2).sum()),
        "nearest_distinct": len(set(nearest.tolist())),
        "one_to_one_by_nearest": len(set(nearest.tolist())) == len(nearest),
        "moved_beyond": {k: int((moves > v).sum()) for k, v in
                         (("1e-9", 1e-9), ("1e-6", 1e-6), ("1e-3", 1e-3), ("0.05", 0.05), ("0.1", 0.1))},
        "within_0.05": int((moves <= 0.05).sum()),
        "largest_move": float(moves.max()),
        "turned_beyond_1deg": int((turns > 1).sum()),
        "turned_beyond_1e-6_rad": int((turns > math.degrees(1e-6)).sum()),
        "largest_turn_deg": float(turns.max()),
    }


def main() -> int:
    src, house_path, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    new_side, new_c, new_a = load_new(src)
    house_side, house_c, house_a = load_house(house_path)
    runs = [measure(new_c, new_a, house_c, house_a, house_side, new_side, sym, anchor, cost)
            for anchor in ANCHORS for cost in ("sum", "squared") for sym in SYMS]
    best = {}
    for anchor in ANCHORS:
        for cost in ("sum", "squared"):
            cands = [r for r in runs if r["anchor"] == anchor and r["cost"] == cost]
            best[f"{anchor}/{cost}"] = min(cands, key=lambda r: r["total_cost"])
    tilt_new = [fold(a) for a in new_a]
    tilt_house = [fold(a) for a in house_a]
    receipt = {
        "program": "l101_identity.py",
        "certificate_sha256": sha256_file(src / "n-179-candidate.yaml"),
        "house_sha256": sha256_file(house_path),
        "tilted_beyond_0.5deg": {"new": sum(1 for t in tilt_new if abs(t) > 0.5),
                                 "house": sum(1 for t in tilt_house if abs(t) > 0.5)},
        "tilted_beyond_1deg": {"new": sum(1 for t in tilt_new if abs(t) > 1),
                               "house": sum(1 for t in tilt_house if abs(t) > 1)},
        "best": best,
        "runs": runs,
    }
    out.write_text(json.dumps(receipt, indent=1) + "\n", encoding="utf-8")
    print("tilted", receipt["tilted_beyond_0.5deg"])
    for key, r in best.items():
        print(key, r["symmetry"], round(r["total_cost"], 4), r["moved_beyond"], round(r["largest_move"], 4),
              r["turned_beyond_1deg"], round(r["largest_turn_deg"], 3), "nearest", r["nearest_distinct"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
