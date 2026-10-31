"""Pose-by-pose identity of two packings, for credit; decides nothing about any bound.

Written for the stage 4 review of Couzo's #843, #844 and a5a5d76 certificates
(bold-ritchie-rv-couzo, 2026-10-31). Reads half-angle certificates ("n S" then "x y t")
and Witness/v2 YAML (center + basis). For each of the eight symmetries of the square
about the box centres it pairs the squares by the assignment of least summed squared
centre distance and keeps the cheapest symmetry; it reports moves, turns modulo 90
degrees, one-to-one by nearest centres, and the bottleneck assignment's largest move.

Usage: identity.py --n N A=PATH B=PATH [C=PATH ...]   (every pair is compared)
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import sys
from fractions import Fraction as F

import numpy as np
import yaml
from scipy.optimize import linear_sum_assignment
from scipy.spatial import cKDTree


def read(path):
    if path.endswith((".yaml", ".yml")):
        d = yaml.safe_load(open(path, encoding="utf-8"))["witness"]
        side = F(str(d["side"]))
        pts = []
        for s in d["squares"]:
            x, y = (float(F(str(c))) for c in s["center"])
            bx, by = (float(F(str(c))) for c in s["basis"])
            pts.append((x, y, math.degrees(math.atan2(by, bx))))
        return side, np.array(pts)
    lines = [ln for ln in open(path, encoding="utf-8").read().splitlines() if ln.strip() and not ln.startswith("#")]
    n, s = lines[0].split()
    side = F(s)
    pts = []
    for ln in lines[1 : 1 + int(n)]:
        x, y, t = (F(z) for z in ln.split())
        pts.append((float(x), float(y), math.degrees(2 * math.atan(float(t)))))
    return side, np.array(pts)


SYMS = [
    (lambda x, y: (x, y), +1, "identity"),
    (lambda x, y: (-y, x), +1, "rot90"),
    (lambda x, y: (-x, -y), +1, "rot180"),
    (lambda x, y: (y, -x), +1, "rot270"),
    (lambda x, y: (-x, y), -1, "mirror x"),
    (lambda x, y: (x, -y), -1, "mirror y"),
    (lambda x, y: (y, x), -1, "diagonal"),
    (lambda x, y: (-y, -x), -1, "antidiagonal"),
]


def tilt(theta):
    r = theta % 90.0
    return min(r, 90.0 - r)


def turn(a, b):
    d = (a - b) % 90.0
    return min(d, 90.0 - d)


def compare(A, sA, B, sB):
    ca = A[:, :2] - float(sA) / 2
    cb = B[:, :2] - float(sB) / 2
    best = None
    for f, orient, name in SYMS:
        mx, my = f(ca[:, 0], ca[:, 1])
        m = np.stack([mx, my], axis=1)
        cost = ((m[:, None, :] - cb[None, :, :]) ** 2).sum(axis=2)
        r, c = linear_sum_assignment(cost)
        tot = cost[r, c].sum()
        if best is None or tot < best[0]:
            best = (tot, name, orient, m, r, c, cost)
    tot, name, orient, m, r, c, cost = best
    moves = np.sqrt(cost[r, c])
    th_a = A[r, 2] * orient
    turns = np.array([turn(a, b) for a, b in zip(th_a, B[c, 2])])
    tree = cKDTree(cb)
    _, nn = tree.query(m)
    one_to_one = len(set(nn.tolist())) == len(nn)
    # bottleneck: least largest move over assignments, by bisection on the threshold
    d = np.sqrt(cost)
    lo, hi = 0.0, float(moves.max())
    for _ in range(40):
        mid = (lo + hi) / 2
        big = np.where(d <= mid, 0.0, 1.0)
        rr, cc = linear_sum_assignment(big)
        if big[rr, cc].sum() == 0:
            hi = mid
        else:
            lo = mid
    return {
        "symmetry": name,
        "one_to_one_nearest": bool(one_to_one),
        "beyond_0.1": int((moves > 0.1).sum()),
        "beyond_0.01": int((moves > 0.01).sum()),
        "beyond_1e-3": int((moves > 1e-3).sum()),
        "beyond_1e-9": int((moves > 1e-9).sum()),
        "largest_move": float(moves.max()),
        "median_move": float(np.median(moves)),
        "bottleneck": hi,
        "turned_beyond_1deg": int((turns > 1.0).sum()),
        "largest_turn_deg": float(turns.max()),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("items", nargs="+")
    ap.add_argument("--out")
    ns = ap.parse_args()
    P = {}
    for it in ns.items:
        k, p = it.split("=", 1)
        s, pts = read(p)
        assert len(pts) == ns.n, (k, len(pts))
        P[k] = (s, pts)
        print(f"{k}: side {float(s):.15f}  tilted beyond 1 deg: {int(sum(tilt(t) > 1.0 for t in pts[:, 2]))}")
    out = []
    for a, b in itertools.combinations(P, 2):
        r = compare(P[a][1], P[a][0], P[b][1], P[b][0])
        r.update({"a": a, "b": b, "side_b_minus_a": float(P[b][0] - P[a][0])})
        out.append(r)
        print(json.dumps(r))
    if ns.out:
        json.dump(out, open(ns.out, "w"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
