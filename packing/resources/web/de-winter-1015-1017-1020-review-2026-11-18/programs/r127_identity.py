"""Describe packings and measure how far two of them differ, square by square.  It
decides nothing: its numbers are binary64 reads of exact files, for description.

Lane r127-1118.  Written for this review; imports only its own modules, numpy and
scipy.

    python -I -B r127_identity.py LABEL=FILE [LABEL=FILE ...] --out OUT.json

For each packing: the tilt of each square (the angle of its edge direction, reduced to
(-45, 45] degrees), how many are exactly upright (an edge direction with a zero
component, exactly), turned below 1e-6 degrees, below 1 degree, and beyond; and the
number of distinct exact orientations.

For each earlier-later pair (in the order given): under each of the eight symmetries of
the box, the later packing's centres are mapped about its box centre onto the earlier's
box centre, and the squares are paired by an optimal assignment of Euclidean distance
(scipy's linear_sum_assignment).  Reported for the symmetry with the least largest
move: whether nearest centres pair the squares one to one, the largest move, the number
of squares moved beyond 1e-9, 1e-6, 1e-3 and 1e-1, and the largest tilt change of a
paired square.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I drops the script dir

import argparse
import json
import math
import sys

import numpy as np
from scipy.optimize import linear_sum_assignment

import r127_frame as F
import r127_read as R

SYMS = [
    ("identity", lambda x, y: (x, y)),
    ("rot90", lambda x, y: (-y, x)),
    ("rot180", lambda x, y: (-x, -y)),
    ("rot270", lambda x, y: (y, -x)),
    ("mirror-x", lambda x, y: (-x, y)),
    ("mirror-y", lambda x, y: (x, -y)),
    ("transpose", lambda x, y: (y, x)),
    ("antitranspose", lambda x, y: (-y, -x)),
]


def tilt_deg(u) -> float:
    a = math.degrees(math.atan2(float(u[1]), float(u[0])))
    a = (a + 45.0) % 90.0 - 45.0
    return a


def describe(p) -> dict:
    cs, us = F.frames(p)
    tilts = [tilt_deg(u) for u in us]
    upright = sum(1 for u in us if u[0] == 0 or u[1] == 0)
    ab = [abs(t) for t in tilts]
    orient = set()
    for u in us:
        a, b = u
        # reduce the exact direction to its class under quarter turns: the representative
        # with a > 0 and b >= 0
        for _ in range(4):
            if a > 0 and b >= 0:
                break
            a, b = -b, a
        orient.add((a, b))
    beyond = sorted(t for t in tilts if abs(t) > 1.0)
    return {
        "n": p.n,
        "exactly_upright": upright,
        "turned_below_1e-6_deg": sum(1 for t, u in zip(ab, us, strict=True)
                                      if t < 1e-6 and not (u[0] == 0 or u[1] == 0)),
        "turned_1e-6_to_1_deg": sum(1 for t in ab if 1e-6 <= t <= 1.0),
        "turned_beyond_1_deg": len(beyond),
        "beyond_1_deg_range": [beyond[0], beyond[-1]] if beyond else None,
        "beyond_1_deg_positive": sum(1 for t in beyond if t > 0),
        "beyond_1_deg_negative": sum(1 for t in beyond if t < 0),
        "distinct_orientations": len(orient),
        "max_denominator_digits_direction": max(len(str(u[0].denominator)) for u in us),
        "max_denominator_digits_centre": max(max(len(str(c[0].denominator)), len(str(c[1].denominator))) for c in cs),
    }


def compare(p, q) -> dict:
    cp, up = F.frames(p)
    cq, uq = F.frames(q)
    hp, hq = float(p.side) / 2, float(q.side) / 2
    P = np.array([[float(x) - hp, float(y) - hp] for x, y in cp])
    tp = np.array([tilt_deg(u) for u in up])
    best = None
    for name, g in SYMS:
        Qm = np.array([g(float(x) - hq, float(y) - hq) for x, y in cq])
        uq_g = [g(float(a), float(b)) for a, b in uq]
        tq = np.array([((math.degrees(math.atan2(b, a)) + 45.0) % 90.0 - 45.0) for a, b in uq_g])
        dist = np.sqrt(((P[:, None, :] - Qm[None, :, :]) ** 2).sum(axis=2))
        rows, cols = linear_sum_assignment(dist)
        moves = dist[rows, cols]
        nearest_q = dist.argmin(axis=1)
        nearest_p = dist.argmin(axis=0)
        one_to_one = len(set(nearest_q.tolist())) == len(P) and all(
            nearest_p[nearest_q[i]] == i for i in range(len(P)))
        dt = np.abs(((tp[rows] - tq[cols]) + 45.0) % 90.0 - 45.0)
        rec = {
            "symmetry": name,
            "nearest_centres_one_to_one": bool(one_to_one),
            "assignment_is_file_order": bool((cols == np.arange(len(P))).all()),
            "largest_move": float(moves.max()),
            "largest_move_square": int(rows[moves.argmax()]) + 1,
            "moved_beyond": {k: int((moves > 10.0 ** -e).sum()) for k, e in
                             (("1e-9", 9), ("1e-6", 6), ("1e-3", 3), ("1e-1", 1))},
            "largest_tilt_change_deg": float(dt.max()),
            "tilt_changes_beyond_1e-3_deg": int((dt > 1e-3).sum()),
        }
        if best is None or rec["largest_move"] < best["largest_move"]:
            best = rec
    assert best is not None
    return best


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    labels, packs = [], []
    for spec in a.inputs:
        label, path = spec.split("=", 1)
        labels.append(label)
        packs.append(R.read_path(path))
    out: dict = {"program": "r127_identity.py", "decides": "nothing",
                 "describe": {lab: describe(p) for lab, p in zip(labels, packs, strict=True)},
                 "pairs": []}
    for lab, d in out["describe"].items():
        print(f"{lab}: {d}")
    for i in range(len(packs)):
        for j in range(i + 1, len(packs)):
            r = compare(packs[i], packs[j])
            r = {"earlier": labels[i], "later": labels[j], **r}
            out["pairs"].append(r)
            print(f"{labels[i]} vs {labels[j]}: {r}")
    json.dump(out, open(a.out, "w"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
