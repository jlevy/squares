"""Measure the five certificates pose by pose against the packings their credit names.

Written for the stage 4 review of 19 October 2026. A measurement for credit; it decides
nothing. It reads every packing through `devtools.check_half_angle_area`, the third route
the earlier reviews used for the same measurement, after adding to that module's import
table, in this process only, the keys of the five packets reviewed here and of T-186's
packet (``70a033f``), as the 16 October review's driver did; each read admits its packet
through `upper_bound_reports.read_facts` first. Joost de Winter's #668 witness at 229
(T-196), which no reader there covers, is read here from its retained gzip: ``side`` and
each square's ``center`` and ``basis`` as exact rationals, the basis held to the unit
circle.

For each pair it reports:

- `arrangement_gap` and `unmoved`, as the 16 October review's Credit and Lineage table
  did: each square of the certificate matched to the nearest centre of the other packing
  under each of the eight box symmetries, a symmetry counting only where that matching is
  one to one, and the best kept (the largest move least);
- an optimal assignment, which is how the source compares (its issues: "optimal
  assignment over the eight box symmetries"): under each symmetry, the one-to-one
  matching of least total squared centre displacement (`scipy.optimize.
  linear_sum_assignment`, in binary64), the symmetry of least total kept, with its
  largest move and how many squares move beyond each bound;
- each packing's tilt: every square's angle folded into ``[0, 45]`` degrees, which no
  box symmetry or quarter turn changes, squares above ``1e-6`` degrees counted as tilted
  and grouped where consecutive angles lie within ``0.05`` degrees.

Usage, from ``packing/`` with the project interpreter::

    python -I lineage_1019.py --json OUT.json
"""

from __future__ import annotations

import argparse
import gzip
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))

import numpy as np  # noqa: E402
from scipy.optimize import linear_sum_assignment  # noqa: E402

from devtools import check_half_angle_area as area  # noqa: E402

WEB = Path.cwd() / "resources/web"
KEYS = {
    "#669": "evand-n155-explorer-2026-10-17",
    "#674-opening": "evand-n229-dilation-2026-10-17",
    "#674-update": "evand-n229-dilation-update-2026-10-18",
    "#659": "evand-n236-2026-10-16",
    "#664": "evand-n271-2026-10-17",
    "70a033f": "mishapolk-kkt-refinements-2026-10-14",
}
BOUNDS = {"1e-4": 1e-4, "1e-3": 1e-3, "1e-2": 1e-2, "1e-1": 1e-1}

Packing = tuple[Fraction, tuple[tuple[Fraction, Fraction, Fraction, Fraction], ...]]


def de_winter_229() -> Packing:
    raw = (WEB / "de-winter-upper-bounds-227-229-260-2026-10-17/source/n229/n229_exact.json.gz").read_bytes()
    value = json.loads(gzip.decompress(raw))
    if value["n"] != 229 or len(value["squares"]) != 229:
        raise ValueError("not 229 squares")
    side = Fraction(value["side"])
    placed = []
    for square in value["squares"]:
        x, y = (Fraction(v) for v in square["center"])
        c, s = (Fraction(v) for v in square["basis"])
        if c * c + s * s != 1:
            raise ValueError("basis off the unit circle")
        placed.append((x, y, c, s))
    return side, tuple(placed)


#: Register entries no reader of that module names, by the key added above.
ENTRY_KEYS = {"T-186": "70a033f"}


def reader(label: str, n: int) -> Packing:
    if label == "T-196":
        return de_winter_229()
    if label in ENTRY_KEYS:
        return area.import_packing(ENTRY_KEYS[label])(n)
    if label in area.CREDITED_READERS:
        return area.CREDITED_READERS[label](n)
    return area.import_packing(label)(n)


#: (certificate key, n, packing measured against, why).
PAIRS = (
    ("#669", 155, "T-149", "the start the issue names (Ostashev, #501)"),
    ("#669", 155, "T-174", "the case's house (Ostashev's packing as PingYou padded it)"),
    ("#674-update", 229, "#674-opening", "the opening certificate the update replaces"),
    ("#674-opening", 229, "T-196", "de Winter's #668, which the issue says #672 refines"),
    ("#674-update", 229, "T-196", "de Winter's #668, which the issue says #672 refines"),
    ("#659", 236, "T-136", "SQUISH's #481, whose composition the issue says was rebuilt"),
    ("#659", 236, "T-146", "the case's house (Daniel's regularized view of #481's packing)"),
    ("#659", 236, "T-174", "PR #574's certificate at 236"),
    ("#664", 271, "T-186", "the case's house (Polkovskyi's re-solve of T-161's packing)"),
    ("#664", 271, "T-161", "Couzo's #561, which the issue says it refines"),
    ("#664", 271, "T-151", "SQUISH's #500, which T-161 refines"),
    ("#664", 271, "T-174", "PR #574's certificate at 271"),
)


def fold(c: Fraction, s: Fraction) -> float:
    """The square's angle in degrees folded into [0, 45]: invariant under box symmetries."""
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
        "groups": [
            {"count": len(g), "from": round(g[0], 4), "to": round(g[-1], 4)} for g in groups
        ],
    }


def assignment(first: Packing, second: Packing) -> dict[str, object]:
    """Least total squared displacement over one-to-one matchings, under each symmetry."""
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
        "largest_turn_degrees": f"{math.degrees(math.asin(min(1.0, max(turns)))):.4g}",
        "turned_beyond_0.01_degree": sum(1 for t in turns if t > math.sin(math.radians(0.01))),
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--json", type=Path, required=True)
    args = parser.parse_args(argv)
    area.ALL_IMPORTS.update(KEYS)
    report: dict[str, object] = {"pairs": {}, "tilts": {}}
    pairs = report["pairs"]
    tilts = report["tilts"]
    assert isinstance(pairs, dict) and isinstance(tilts, dict)
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
        nearest = row["nearest"]
        assert isinstance(nearest, dict)
        print(
            f"{key} n={n} vs {against}: side diff {row['side_difference']}; nearest "
            + (
                f"k={nearest['symmetry']} moved {nearest['moved_beyond']} largest {nearest['largest_displacement'][:10]}"
                if "symmetry" in nearest
                else "unmatched"
            )
            + f"; unmoved {row['unmoved']}; assignment {row['assignment']}",
            flush=True,
        )
    for label, value in tilts.items():
        print(label, json.dumps(value))
    args.json.write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
