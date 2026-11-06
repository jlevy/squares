"""Exact scale slack: how far each packing's centres can be scaled about the corner.

Usage (from packing/, Python 3.14):
  python -I scale_slack.py CANDIDATES_DIR HOUSES_DIR OUT.json

Added after the review's findings were frozen, following the 5 November review's measure
of a house's slack. A measurement; it decides nothing about any bound.

Scale every centre and the side by lambda about the corner (0, 0), keeping each square's
orientation and size. A wall constraint of a square with centre c and corner offset o
needs lambda c + o >= 0 and lambda c + o <= lambda S, so lambda >= -o/c where o < 0 and
lambda >= o/(S - c) where o > 0. A pair with centre difference d, along each of its four
edge normals b, has the gap lambda |d.b| - q_b, where q_b is the sum of the two squares'
half-widths along b; the pair stays disjoint while some axis has a non-negative gap, so
lambda >= min_b q_b / |d.b|. The least scale lambda* is the largest of those bounds; the
side then shrinks by S (1 - lambda*), which is exact. Only pairs whose centres lie within
1.8 are evaluated: for d >= 1.8 one axis of the first square lies within 45 degrees of d,
so its bound is at most (1/2 + sqrt(2)/2) sqrt(2) / d < 0.95, below every lambda* here.
"""

from __future__ import annotations

import json
import math
import sys
from fractions import Fraction as F
from pathlib import Path

import mpmath

sys.path.insert(0, str(Path(__file__).resolve().parent))

import exact_geometry as eg  # noqa: E402
from cert_reader import read_cert  # noqa: E402
from house_slack import NAMES, read_witness, square_cs  # noqa: E402

H = F(1, 2)


def least_scale(side: F, poses: list[tuple[F, F, F, F]]) -> dict:
    """poses: (x, y, c, s) with c^2 + s^2 = 1."""
    best = F(0)
    where = None
    sq = [square_cs(*p) for p in poses]
    for k, ((x, y, _, _), (corners, _)) in enumerate(zip(poses, sq)):
        for (px, py) in corners:
            for cen, off in ((x, px - x), (y, py - y)):
                if off < 0:
                    b = -off / cen
                elif off > 0:
                    b = off / (side - cen)
                else:
                    continue
                if b > best:
                    best, where = b, ("wall", k + 1)
    n = len(poses)
    for i in range(n):
        xi, yi = poses[i][0], poses[i][1]
        for j in range(i + 1, n):
            xj, yj = poses[j][0], poses[j][1]
            if math.hypot(float(xi - xj), float(yi - yj)) >= 1.8:
                continue
            dx, dy = xj - xi, yj - yi
            lam = None
            for (bx, by) in sq[i][1] + sq[j][1]:
                p = abs(dx * bx + dy * by)
                if p == 0:
                    continue
                q = F(0)
                for (ux, uy), (vx, vy) in (sq[i][1], sq[j][1]):
                    q += H * (abs(ux * bx + uy * by) + abs(vx * bx + vy * by))
                r = q / p
                lam = r if lam is None or r < lam else lam
            if lam is not None and lam > best:
                best, where = lam, ("pair", i + 1, j + 1)
    slack = side * (1 - best)
    return {
        "least_scale": f"{best.numerator}/{best.denominator}",
        "one_minus_least_scale": mpmath.nstr(mpmath.mpf((1 - best).numerator) / (1 - best).denominator, 8),
        "side_slack": mpmath.nstr(mpmath.mpf(slack.numerator) / slack.denominator, 8),
        "set_by": where,
    }


def cert_poses(path: Path):
    c = read_cert(path)
    out = []
    for (x, y, t) in c["squares"]:
        cc, ss = eg.frame_a(t)
        out.append((x, y, cc, ss))
    return c["S"], out


def main() -> None:
    mpmath.mp.dps = 40
    cand, houses, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    res = {}
    for n, name in NAMES.items():
        w = read_witness(houses / f"W-known-best-n{n}.yaml")
        res[f"house {n}"] = least_scale(w["S"], w["squares"])
        s, p = cert_poses(cand / f"{name}.cert")
        res[f"new {n}"] = least_scale(s, p)
        print(n, "house", res[f"house {n}"], "| new", res[f"new {n}"])
    s, p = cert_poses(houses / "T-257-s260_1028.cert")
    res["T-257 260"] = least_scale(s, p)
    print("T-257 260", res["T-257 260"])
    out.write_text(json.dumps(res, indent=1) + "\n")


if __name__ == "__main__":
    main()
