"""Second exact checker for a packing of unit squares in a square. Python 3.10 or later, standard library only.

Usage: python3 -B check_area.py [file.json]   (default: the *_exact.json file in this folder)

This script shares no code with verify_exact.py. For every pair of squares with centres closer than sqrt(2), it clips
one square against the other in rational arithmetic and requires the intersection polygon to have area exactly 0.
It also checks that every square is a unit square inside [0, side] x [0, side].
"""
import glob
import json
import os
import sys
from fractions import Fraction as F

HALF = F(1, 2)


def polygon(q):
    cx, cy, c, s = q
    return [(cx + a * c * HALF - b * s * HALF, cy + a * s * HALF + b * c * HALF)
            for a, b in ((1, 1), (-1, 1), (-1, -1), (1, -1))]          # counter-clockwise


def area(p):
    return sum(p[i][0] * p[(i + 1) % len(p)][1] - p[(i + 1) % len(p)][0] * p[i][1] for i in range(len(p))) / 2


def clip(subject, clipper):
    """Sutherland-Hodgman clipping of a convex polygon against a convex counter-clockwise polygon."""
    out = subject
    for i in range(len(clipper)):
        a, b = clipper[i], clipper[(i + 1) % len(clipper)]
        ex, ey = b[0] - a[0], b[1] - a[1]

        def left_of(p):
            return ex * (p[1] - a[1]) - ey * (p[0] - a[0])              # > 0: strictly inside this edge

        inp, out = out, []
        for j in range(len(inp)):
            p, q = inp[j], inp[(j + 1) % len(inp)]
            sp, sq = left_of(p), left_of(q)
            if sp >= 0:
                out.append(p)
            if (sp > 0 and sq < 0) or (sp < 0 and sq > 0):
                t = sp / (sp - sq)
                out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
        if not out:
            return []
    return out


def main(path=None):
    if path is None:
        here = os.path.dirname(os.path.abspath(__file__))
        path = sorted(glob.glob(os.path.join(here, "*_exact.json")))[0]
    data = json.load(open(path))
    n = data["n"]
    side = F(data["side"])
    squares = [tuple(F(v) for v in q) for q in data["squares"]]
    assert len(squares) == n, "wrong number of squares"
    polys = [polygon(q) for q in squares]
    for i, q in enumerate(squares):
        assert q[2] ** 2 + q[3] ** 2 == 1, f"square {i}: direction is not a unit vector"
        assert area(polys[i]) == 1, f"square {i}: area is not 1"
        assert all(0 <= x <= side and 0 <= y <= side for x, y in polys[i]), f"square {i}: outside the container"
    order = sorted(range(n), key=lambda i: squares[i][0])
    pairs = 0
    for a in range(n):
        i = order[a]
        for b in range(a + 1, n):
            j = order[b]
            dx = squares[j][0] - squares[i][0]
            if dx * dx >= 2:
                break
            dy = squares[j][1] - squares[i][1]
            if dx * dx + dy * dy >= 2:      # centres at least sqrt(2) apart: unit squares cannot overlap
                continue
            pairs += 1
            common = clip(polys[i], polys[j])
            assert len(common) < 3 or area(common) == 0, f"squares {i} and {j} overlap"
    print(f"OK: {n} unit squares inside a square of side {float(side):.15f}; "
          f"{pairs} close pairs, every intersection has area exactly 0")


if __name__ == "__main__":
    main(*sys.argv[1:])
