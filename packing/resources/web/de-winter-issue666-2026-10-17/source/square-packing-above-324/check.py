"""Exact check of a square-packing certificate (Python standard library only).

Usage: python3 check.py n0509.cert [more.cert ...]

Certificate format: line 1 'n side'; then one line 'x y t' per unit square, with centre
(x, y) and t = tan(theta/2), all rational (integers, decimals or p/q). Lines starting with
'#' are comments. With cos = (1 - t^2)/(1 + t^2) and sin = 2t/(1 + t^2) every corner is
rational, so the test is exact: every corner lies strictly inside [0, side]^2, and every
pair of squares with centres closer than sqrt(2) is strictly separated along one of the
four edge normals of the two squares.
"""
import sys
from fractions import Fraction as F

H = F(1, 2)
OFFSETS = ((-H, -H), (H, -H), (H, H), (-H, H))


def check(path):
    rows = [line.split() for line in open(path) if line.strip() and not line.startswith('#')]
    n, side = int(rows[0][0]), F(rows[0][1])
    squares = []
    for x, y, t in rows[1:]:
        x, y, t = F(x), F(y), F(t)
        c, s = (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)
        squares.append((x, y, c, s, [(x + a * c - b * s, y + a * s + b * c) for a, b in OFFSETS]))
    if len(squares) != n:
        return False, f'{path}: header says {n} squares, file has {len(squares)}'
    wall = min(min(px, py, side - px, side - py) for q in squares for px, py in q[4])
    fx = [float(q[0]) for q in squares]
    fy = [float(q[1]) for q in squares]
    gap = None
    for i in range(n):
        for j in range(i + 1, n):
            if (fx[i] - fx[j]) ** 2 + (fy[i] - fy[j]) ** 2 >= 2.0000001:
                continue  # centres at least sqrt(2) apart: the squares are disjoint
            best = None
            for c, s in ((squares[i][2], squares[i][3]), (squares[j][2], squares[j][3])):
                for ux, uy in ((c, s), (-s, c)):
                    pa = [px * ux + py * uy for px, py in squares[i][4]]
                    pb = [px * ux + py * uy for px, py in squares[j][4]]
                    g = max(min(pb) - max(pa), min(pa) - max(pb))
                    best = g if best is None or g > best else best
            gap = best if gap is None or best < gap else gap
    ok = wall > 0 and (gap is None or gap > 0)
    return ok, (f'{path}: n = {n}, side = {float(side):.12f}, '
                f'least wall clearance {float(wall):.1e}, least pair gap {float(gap):.1e}, '
                f'{"valid" if ok else "INVALID"}')


if __name__ == '__main__':
    results = [check(p) for p in sys.argv[1:]]
    for ok, msg in results:
        print(msg)
    sys.exit(0 if results and all(ok for ok, _ in results) else 1)
