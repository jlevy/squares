"""Measure the #689 (308) and #694 (154) certificates pose by pose against the packings
their credit names.

Written for the stage 4 review of 20 October 2026. A measurement for credit; it decides
nothing. Every packing is read through `devtools.check_half_angle_area`'s readers, after
adding to that module's import table, in this process only, the keys of the two packets
reviewed here and of T-186's packet (``70a033f``), as the 19 October review's program
did; each read admits its packet through `upper_bound_reports.read_facts` first.

For each pair at one count it reports:

- `arrangement_gap` and `unmoved` (that module's): each square of the certificate matched
  to the nearest centre of the other packing under each of the eight box symmetries, a
  symmetry counting only where that matching is one to one, and the best kept;
- an optimal assignment, as the source compares: under each symmetry the one-to-one
  matching of least total squared centre displacement (`scipy`, binary64), the symmetry
  of least total kept, with its largest move and how many squares move beyond each bound;
- the tilts: every square's angle folded into [0, 45] degrees, squares above 1e-6
  degrees counted as tilted and grouped where consecutive angles lie within 0.05 degrees.

For the two starts at a neighbouring count, #481's 307 packing (one square inserted) and
#501's 156 packing (two removed), it reports, under each symmetry, the one-sided
matching: how many squares of the smaller packing find a square of the larger within
each bound, under the symmetry that keeps most within 0.1, and the assignment of the
smaller into the larger.

Usage, from ``packing/`` with the project interpreter::

    python -I lineage_1020.py --json OUT.json
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))

import numpy as np  # noqa: E402
from scipy.optimize import linear_sum_assignment  # noqa: E402

from devtools import check_half_angle_area as area  # noqa: E402

KEYS = {
    "#689": "evand-n308-2026-10-19",
    "#694": "evand-n154-sweep-2026-10-20",
    "70a033f": "mishapolk-kkt-refinements-2026-10-14",
}
#: Register entries no reader of that module names, by the import key read for them:
#: T-186 through Mishapolk's 70a033f packet, T-135 through Fang's #484 packet.
ENTRY_KEYS = {"T-186": "70a033f", "T-135": "#484", "T-182": "#586"}
BOUNDS = {"1e-4": 1e-4, "1e-3": 1e-3, "1e-2": 1e-2, "1e-1": 1e-1}

Packing = tuple[Fraction, tuple[tuple[Fraction, Fraction, Fraction, Fraction], ...]]


def reader(label: str, n: int) -> Packing:
    if label in ENTRY_KEYS:
        return area.import_packing(ENTRY_KEYS[label])(n)
    if label in area.CREDITED_READERS:
        return area.CREDITED_READERS[label](n)
    return area.import_packing(label)(n)


#: (certificate key, n, packing measured against, why), at one count.
PAIRS = (
    ("#689", 308, "T-174", "the case's house (PingYou's refinement of T-141's packing)"),
    ("#689", 308, "T-141", "Daniel's #489, which the issue says it is not a refinement of"),
    ("#689", 308, "T-135", "Fang's #484, the two-wedge construction"),
    ("#694", 154, "T-186", "the case's house (Polkovskyi's refinement of T-182's packing)"),
    ("#694", 154, "T-182", "Couzo's #586, whose arrangement the issue asks to credit"),
    ("#694", 154, "T-172", "Couzo's #583"),
    ("#694", 154, "T-160", "Daniel's #552, which #586 continues"),
)
#: (certificate key, n, start key, start n, why), across counts.
STARTS = (
    ("#689", 308, "T-136", 307, "Chaoweeraprasit's #481 at 307, the ultimate start the issue names"),
    ("#694", 154, "T-149", 156, "Ostashev's #501 at 156, the start the issue names"),
)


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
    """Least total squared displacement over one-to-one matchings of `first` into
    `second` (which may be larger), under each symmetry of `second`'s box."""
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


def one_sided(small: Packing, large: Packing) -> dict[str, object]:
    """Each square of the smaller packing to its nearest centre in the larger, under the
    symmetry of the larger's box that keeps most within 0.1."""
    _s, left = small
    other_side, right = large
    best = None
    for k in range(8):
        mapped = [area.symmetric(other_side, sq, k) for sq in right]
        b = np.array([[float(u), float(v)] for u, v, _p, _q in mapped])
        counts = {}
        dists = []
        for x, y, _c, _sn in left:
            d = np.sqrt(((b - np.array([float(x), float(y)])) ** 2).sum(axis=1)).min()
            dists.append(d)
        arr = np.array(dists)
        counts = {label: int((arr <= bound).sum()) for label, bound in BOUNDS.items()}
        key = (counts["1e-1"], counts["1e-2"], counts["1e-3"])
        if best is None or key > best[0]:
            best = (key, {"symmetry": k, "within": counts, "largest_nearest": f"{float(arr.max()):.4g}"})
    assert best is not None
    return best[1]


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--json", type=Path, required=True)
    args = parser.parse_args(argv)
    area.ALL_IMPORTS.update(KEYS)
    report: dict[str, object] = {"pairs": {}, "starts": {}, "tilts": {}}
    pairs = report["pairs"]
    starts = report["starts"]
    tilts = report["tilts"]
    assert isinstance(pairs, dict) and isinstance(starts, dict) and isinstance(tilts, dict)
    for key, n, against, why in PAIRS:
        mine = reader(key, n)
        other = reader(against, n)
        row: dict[str, object] = {"why": why, "side_difference": f"{float(mine[0] - other[0]):.6e}"}
        try:
            row["nearest"] = area.arrangement_gap(mine, other)
        except area.AreaRouteError as error:
            row["nearest"] = {"unmatched": str(error)}
        row["unmoved"] = area.unmoved(mine, other)
        row["assignment"] = assignment(mine, other)
        pairs[f"{key} n={n} against {against}"] = row
        for label, packing in ((key, mine), (against, other)):
            tilts.setdefault(f"{label} n={n}", tilt(packing))
        print(f"{key} n={n} vs {against}: {json.dumps(row)}", flush=True)
    for key, n, start, m, why in STARTS:
        mine = reader(key, n)
        other = reader(start, m)
        small, large = (other, mine) if m < n else (mine, other)
        row = {
            "why": why,
            "side_difference": f"{float(mine[0] - other[0]):.6e}",
            "one_sided_nearest": one_sided(small, large),
            "assignment_of_smaller_into_larger": assignment(small, large),
        }
        starts[f"{key} n={n} against {start} n={m}"] = row
        tilts.setdefault(f"{start} n={m}", tilt(other))
        print(f"{key} n={n} vs {start} n={m}: {json.dumps(row)}", flush=True)
    for label, value in tilts.items():
        print(f"tilt {label}: {json.dumps(value)}", flush=True)
    args.json.write_text(json.dumps(report, indent=1) + "\n", "utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
