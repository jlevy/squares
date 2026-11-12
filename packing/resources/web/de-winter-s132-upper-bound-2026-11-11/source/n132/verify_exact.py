"""Exact checker for a packing of unit squares in a square. Python 3.10 or later, standard library only.

Usage: python3 -B verify_exact.py [file.json]   (default: the *_exact.json file in this folder)

Checks, in rational arithmetic:
  1. every square has an exact unit edge direction (cos^2 + sin^2 = 1);
  2. every square lies inside [0, side] x [0, side];
  3. no two squares share interior points (separating-axis test on all pairs).
"""
import glob
import json
import os
import sys
from fractions import Fraction as F
from itertools import combinations

HALF = F(1, 2)


def corners(q):
    cx, cy, c, s = q
    return [(cx + a * c * HALF - b * s * HALF, cy + a * s * HALF + b * c * HALF)
            for a, b in ((1, 1), (-1, 1), (-1, -1), (1, -1))]


def separated(qa, ca, qb, cb):
    for (cx, cy, c, s), other in ((qa, cb), (qb, ca)):
        for ax, ay in ((c, s), (-s, c)):
            centre = cx * ax + cy * ay
            proj = [x * ax + y * ay for x, y in other]
            if min(proj) >= centre + HALF or max(proj) <= centre - HALF:
                return True
    return False


def main(path=None):
    if path is None:
        here = os.path.dirname(os.path.abspath(__file__))
        path = sorted(glob.glob(os.path.join(here, "*_exact.json")))[0]
    data = json.load(open(path))
    side = F(data["side"])
    squares = [tuple(F(v) for v in q) for q in data["squares"]]
    n = data["n"]
    assert len(squares) == n, "wrong number of squares"
    cs = [corners(q) for q in squares]
    for i, q in enumerate(squares):
        assert q[2] ** 2 + q[3] ** 2 == 1, f"square {i}: direction is not a unit vector"
        assert all(0 <= x <= side and 0 <= y <= side for x, y in cs[i]), f"square {i}: outside the container"
    pairs = 0
    for i, j in combinations(range(n), 2):
        dx = squares[i][0] - squares[j][0]
        dy = squares[i][1] - squares[j][1]
        if dx * dx + dy * dy >= 2:      # centres at least sqrt(2) apart: unit squares cannot overlap
            continue
        pairs += 1
        assert separated(squares[i], cs[i], squares[j], cs[j]), f"squares {i} and {j} overlap"
    digits = str(side.numerator * 10 ** 40 // side.denominator)
    print(f"OK: {n} unit squares, pairwise interior-disjoint ({pairs} close pairs tested), inside a square of side")
    print(f"    {digits[:-40]}.{digits[-40:]}... (exact rational in the file)")


if __name__ == "__main__":
    main(*sys.argv[1:])
