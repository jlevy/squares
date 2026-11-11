"""Exact checker for the .cert files in this folder. Python 3.10 or later, standard library only.

File format: comment lines start with '#'. First data line: n and the side. Then n lines: x y t,
with (x, y) the centre of a unit square and t = tan(theta/2) for its rotation angle theta.
All numbers are exact rationals. The checker tests, in rational arithmetic, that every square
lies inside [0, side] x [0, side] and that no two squares share interior points.

Usage: python3 -B verify_cert.py            (checks every n*.cert in the folder)
       python3 -B verify_cert.py n0810.cert
"""
import glob
import sys
from fractions import Fraction as F

HALF = F(1, 2)


def load(path):
    rows = [l.split() for l in open(path) if l.strip() and not l.startswith("#")]
    n, side = int(rows[0][0]), F(rows[0][1])
    squares = []
    for x, y, t in rows[1:]:
        t = F(t)
        squares.append((F(x), F(y), (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)))
    assert len(squares) == n, "wrong number of squares"
    return n, side, squares


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


def check(path):
    n, side, squares = load(path)
    cs = [corners(q) for q in squares]
    for i in range(n):
        assert all(0 <= x <= side and 0 <= y <= side for x, y in cs[i]), f"square {i}: outside the container"
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
            if dx * dx + dy * dy >= 2:   # centres at least sqrt(2) apart: unit squares cannot overlap
                continue
            pairs += 1
            assert separated(squares[i], cs[i], squares[j], cs[j]), f"squares {i} and {j} overlap"
    digits = str(side.numerator * 10 ** 20 // side.denominator + 1)
    print(f"OK {path}: n = {n}, side <= {digits[:-20]}.{digits[-20:]} ({pairs} close pairs tested)")


if __name__ == "__main__":
    for p in (sys.argv[1:] or sorted(glob.glob("n*.cert"))):
        check(p)
