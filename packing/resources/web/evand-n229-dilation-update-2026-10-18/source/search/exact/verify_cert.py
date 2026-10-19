#!/usr/bin/env python3
"""Exact (rational-arithmetic) verifier of a square-packing certificate.  Standalone: Python standard library only.

Certificate format (lines starting with '#' are comments):
    n  S                      S = container side, a rational p/q (or integer / decimal)
    x  y  t                   one line per unit square: centre (x, y), rotation (c, s) = ((1-t^2)/(1+t^2), 2t/(1+t^2))
All numbers rational, so c^2 + s^2 = 1 exactly and every quantity below is an exact rational.

Checks, all with strict inequalities:
  * each square lies in the open box (0, S)^2:  x - e > 0, x + e < S (same for y), e = (|c| + |s|)/2;
  * each pair (i, j) has disjoint closed squares: either |c_i - c_j|^2 > 2 (circumscribed discs disjoint), or some of
    the 4 face normals n of i and j is a separating axis:  |n.(c_j - c_i)| > h_i(n) + h_j(n), h(n) = (|n.u| + |n.v|)/2.
If every check passes, the n closed unit squares are pairwise disjoint inside [0, S]^2, so s(n) <= S.

  verify_cert.py cert.txt        -> prints the verdict and the smallest exact margins; exit status 0 iff valid
"""
import sys
from fractions import Fraction as Fr

HALF = Fr(1, 2)


def parse(path):
    rows = [l.split() for l in open(path) if l.strip() and not l.lstrip().startswith('#')]
    n, S = int(rows[0][0]), Fr(rows[0][1])
    sq = []
    for r in rows[1:n + 1]:
        x, y, t = Fr(r[0]), Fr(r[1]), Fr(r[2])
        d = 1 + t * t
        sq.append((x, y, (1 - t * t) / d, 2 * t / d))
    assert len(sq) == n, 'wrong number of squares'
    return n, S, sq


def verify(n, S, sq, verbose=True):
    for (x, y, c, s) in sq:
        assert c * c + s * s == 1
    wall = None                                    # (margin, square)
    for i, (x, y, c, s) in enumerate(sq):
        e = HALF * (abs(c) + abs(s))
        m = min(x - e, S - x - e, y - e, S - y - e)
        if wall is None or m < wall[0]:
            wall = (m, i)
    pair = None                                    # (best separating margin, i, j) minimised over close pairs
    nclose = 0
    for i in range(n):
        xi, yi, ci, si = sq[i]
        for j in range(i + 1, n):
            xj, yj, cj, sj = sq[j]
            dx, dy = xj - xi, yj - yi
            if dx * dx + dy * dy > 2:
                continue
            nclose += 1
            best = None
            for (nx, ny) in ((ci, si), (-si, ci), (cj, sj), (-sj, cj)):
                hi = HALF * (abs(nx * ci + ny * si) + abs(-nx * si + ny * ci))
                hj = HALF * (abs(nx * cj + ny * sj) + abs(-nx * sj + ny * cj))
                g = abs(nx * dx + ny * dy) - hi - hj
                if best is None or g > best:
                    best = g
            if pair is None or best < pair[0]:
                pair = (best, i, j)
    ok = wall[0] > 0 and (pair is None or pair[0] > 0)
    if verbose:
        print(f'n = {n}, S = {S} (~{float(S):.20g})')
        print(f'  min wall clearance  = {float(wall[0]):.3e}  (square #{wall[1]})')
        if pair:
            print(f'  min pair separation = {float(pair[0]):.3e}  (squares #{pair[1]}, #{pair[2]}; {nclose} pairs with '
                  f'|dc|^2 <= 2 checked by separating axes, the rest by disc separation)')
        print('  VALID: s(n) <= S' if ok else '  INVALID')
    return ok, wall, pair


if __name__ == '__main__':
    n, S, sq = parse(sys.argv[1])
    ok, _, _ = verify(n, S, sq)
    sys.exit(0 if ok else 1)
