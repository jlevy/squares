"""Measure the #703 (270) certificate pose by pose against the packings its credit names.

Written for the stage 4 review of 21 October 2026 (PR #708, T-224). A measurement for
credit; it decides nothing. The certificate is read by the review checker's own reader;
the register's packings at 270 through `devtools.check_half_angle_area`'s import
readers: T-174 (the house best packing, PingYou's #574 refinement of #500's packing)
and T-151 (Chaoweeraprasit's #500, the start the issue names).

For each pair it reports `arrangement_gap` and `unmoved` (that module's: nearest-centre
matching under each of the eight box symmetries, one to one or not), an optimal
assignment (least total squared centre displacement, scipy in binary64, under each
symmetry, the least kept) with its largest move and counts beyond each bound, the turns,
and the tilt groups of each packing folded into [0, 45] degrees.

Usage, from packing/ with the project interpreter:
    python -I lineage_708.py REVIEW_DIR CERT OUT.json
"""

from __future__ import annotations

import json
import math
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))

import numpy as np  # noqa: E402
from scipy.optimize import linear_sum_assignment  # noqa: E402

from devtools import check_half_angle_area as area  # noqa: E402

BOUNDS = {"1e-4": 1e-4, "1e-3": 1e-3, "1e-2": 1e-2, "1e-1": 1e-1}
Packing = tuple[Fraction, tuple[tuple[Fraction, Fraction, Fraction, Fraction], ...]]


def fold(c: Fraction, s: Fraction) -> float:
    theta = math.degrees(math.atan2(float(s), float(c))) % 90.0
    return min(theta, 90.0 - theta)


def tilt(packing: Packing) -> dict[str, object]:
    angles = sorted(fold(c, s) for _x, _y, c, s in packing[1])
    tilted = [a for a in angles if a > 1e-6]
    groups: list[list[float]] = []
    for a in tilted:
        if groups and a - groups[-1][-1] <= 0.05:
            groups[-1].append(a)
        else:
            groups.append([a])
    return {
        "tilted": len(tilted),
        "groups": [{"count": len(g), "from": round(g[0], 4), "to": round(g[-1], 4)} for g in groups],
    }


def assignment(first: Packing, second: Packing) -> dict[str, object]:
    _side, left = first
    other_side, right = second
    a = np.array([[float(x), float(y)] for x, y, _c, _s in left])
    best = None
    for k in range(8):
        mapped = [area.symmetric(other_side, square, k) for square in right]
        b = np.array([[float(u), float(v)] for u, v, _p, _q in mapped])
        cost = ((a[:, None, :] - b[None, :, :]) ** 2).sum(axis=2)
        rows, cols = linear_sum_assignment(cost)
        total = float(cost[rows, cols].sum())
        if best is None or total < best[0]:
            best = (total, k, rows, cols, mapped, cost)
    assert best is not None
    total, k, rows, cols, mapped, cost = best
    moves = np.sqrt(cost[rows, cols])
    turns = []
    for i, j in zip(rows, cols, strict=True):
        _x, _y, c, s = left[i]
        _u, _v, p, q = mapped[j]
        turns.append(float(min(abs(c * q - s * p), abs(c * p + s * q))))
    return {
        "symmetry": k,
        "total_squared": f"{total:.6e}",
        "largest_move": f"{float(moves.max()):.6g}",
        "moved_beyond": {label: int((moves > bound).sum()) for label, bound in BOUNDS.items()},
        "within_0.1": int((moves <= 0.1).sum()),
        "largest_turn_degrees": f"{math.degrees(math.asin(min(1.0, max(turns)))):.4g}",
        "turned_beyond_0.01_degree": sum(1 for t in turns if t > math.sin(math.radians(0.01))),
    }


def measure(first: Packing, second: Packing) -> dict[str, object]:
    gap = area.arrangement_gap(first, second)
    stay = area.unmoved(first, second)
    return {"arrangement_gap": gap, "unmoved": stay, "assignment": assignment(first, second)}


def main(argv: list[str]) -> int:
    review, cert, out = Path(argv[1]), Path(argv[2]), Path(argv[3])
    sys.path.insert(0, str(review))
    import review_708_check as rc  # noqa: E402

    side, squares, _t = rc.read(cert, 270)
    this: Packing = (side, tuple(squares))
    t174 = area.import_packing("#574")(270)
    t151 = area.import_packing("#500")(270)
    result = {
        "sides": {"#703": str(side), "T-174": str(t174[0]), "T-151": str(t151[0])},
        "#703 vs T-174 (house best packing)": measure(this, t174),
        "#703 vs T-151 (#500, the start)": measure(this, t151),
        "T-174 vs T-151 (the house refines #500)": measure(t174, t151),
        "tilts": {"#703": tilt(this), "T-174": tilt(t174), "T-151": tilt(t151)},
    }
    out.write_text(json.dumps(result, indent=1), encoding="utf-8")
    print(json.dumps(result, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
