#!/usr/bin/env python3
"""
verify_certificate.py -- exact (rational) verifier for "n unit squares inside a square of side s"
upper-bound certificates.  Standard library only; all comparisons in fractions.Fraction /
int arithmetic; no floating point anywhere in the logic.

Two certificate formats are accepted (auto-detected):

(A) centre/tilt format  ("format": "centre-tilt")
    {"side": "p/q",
     "squares": [{"cx": "p/q", "cy": "p/q", "t": "p/q"}, ...]}
    t = tan(theta/2) is rational, hence cos = (1-t^2)/(1+t^2), sin = 2t/(1+t^2) are exactly
    rational and cos^2 + sin^2 = 1 holds identically.  Corners: c + R(theta)(+-1/2, +-1/2).

(B) integer-corner format  ("format": "integer-corners")
    {"D": <int>, "side_D": <int>,
     "squares": [{"corners": [[x0,y0],[x1,y1],[x2,y2],[x3,y3]]}, ...]}
    all corner coordinates are integers meaning x/D; the container is [0, side_D/D]^2.
    Each square is checked to be a genuine unit square: with e = P1-P0, f = P2-P1 we require
    f = rot90(e), P3 = P0 + f, and |e|^2 = D^2 exactly.

Checks (both formats):
  1. every corner strictly inside the open container (0 < x < s, 0 < y < s);
  2. for every pair of squares there is a separating axis among the edge normals of the two
     squares (4 candidate axes) whose projections are strictly disjoint.
Prints the minimum containment margin and minimum separation margin (exact rationals, plus a
float rendering for humans) and exits 0 on success, 1 on failure.

Mathematical basis (the only thing taken on trust): two convex polygons whose projections
onto some line are disjoint intervals are disjoint sets, and the projection of a polygon is
the interval spanned by its vertices' projections.  Hence a passing certificate proves
s(n) <= side.

Usage:  python verify_certificate.py certificate.json
"""
import json
import sys
from fractions import Fraction as F
from itertools import combinations


def frac(x):
    """Parse an int / 'p/q' string / int-valued JSON number exactly (floats are rejected)."""
    if isinstance(x, bool):
        raise ValueError('bad number')
    if isinstance(x, int):
        return F(x)
    if isinstance(x, str):
        return F(x)          # Fraction('p/q') or Fraction('123') -- exact
    raise ValueError('floating point numbers are not allowed in certificates: %r' % (x,))


HALF = [(F(-1, 2), F(-1, 2)), (F(1, 2), F(-1, 2)), (F(1, 2), F(1, 2)), (F(-1, 2), F(1, 2))]


def squares_from_centre_tilt(cert):
    side = frac(cert['side'])
    sq = []
    for q in cert['squares']:
        cx, cy, t = frac(q['cx']), frac(q['cy']), frac(q['t'])
        den = 1 + t * t
        c, s = (1 - t * t) / den, 2 * t / den
        assert c * c + s * s == 1
        corners = [(cx + c * hx - s * hy, cy + s * hx + c * hy) for hx, hy in HALF]
        sq.append(corners)
    return side, sq


def squares_from_integer_corners(cert):
    D = int(cert['D'])
    side = F(int(cert['side_D']), D)
    sq = []
    for q in cert['squares']:
        P = [(F(int(x), D), F(int(y), D)) for x, y in q['corners']]
        if len(P) != 4:
            raise ValueError('need 4 corners')
        ex, ey = P[1][0] - P[0][0], P[1][1] - P[0][1]
        fx, fy = P[2][0] - P[1][0], P[2][1] - P[1][1]
        if (fx, fy) != (-ey, ex):
            raise ValueError('corners do not form a square (f != rot90 e)')
        if (P[3][0], P[3][1]) != (P[0][0] + fx, P[0][1] + fy):
            raise ValueError('corners do not form a square (P3)')
        if ex * ex + ey * ey != 1:
            raise ValueError('not a unit square: |e|^2 = %s' % (ex * ex + ey * ey))
        sq.append(P)
    return side, sq


def edge_normals(P):
    """Two (non-normalised) edge normals of the square with corners P."""
    ex, ey = P[1][0] - P[0][0], P[1][1] - P[0][1]
    return [(ex, ey), (-ey, ex)]


def verify(cert, verbose=True):
    fmt = cert.get('format', 'centre-tilt')
    if fmt == 'integer-corners':
        side, sq = squares_from_integer_corners(cert)
    else:
        side, sq = squares_from_centre_tilt(cert)
    n = len(sq)
    ok = True
    # 1. containment
    min_margin = None
    for i, P in enumerate(sq):
        for (x, y) in P:
            m = min(x, y, side - x, side - y)
            if min_margin is None or m < min_margin:
                min_margin = m
            if not (0 < x < side and 0 < y < side):
                ok = False
                if verbose:
                    print('FAIL: square %d corner (%s, %s) not strictly inside [0, %s]^2' % (i, x, y, side))
    # 2. pairwise separation
    min_sep = None
    for i, j in combinations(range(n), 2):
        A, B = sq[i], sq[j]
        best = None
        for (ax, ay) in edge_normals(A) + edge_normals(B):
            # normalise the margin by the axis length only for reporting; the sign test is exact
            pa = [ax * x + ay * y for x, y in A]
            pb = [ax * x + ay * y for x, y in B]
            gap = max(min(pb) - max(pa), min(pa) - max(pb))
            # the axis is not unit length; margins are compared as gap/sqrt(L2) exactly (_cmp)
            L2 = ax * ax + ay * ay
            val = (gap, L2)
            if best is None or _cmp(val, best) > 0:
                best = val
        gap, L2 = best
        if gap <= 0:
            ok = False
            if verbose:
                print('FAIL: squares %d and %d have no separating axis (best gap %s)' % (i, j, gap))
        # exact squared margin (as a rational) = gap^2 / L2, keep the smallest positive one
        m2 = (gap * gap / L2) if gap > 0 else F(0)
        if min_sep is None or (gap > 0 and m2 < min_sep) or gap <= 0:
            min_sep = m2 if gap > 0 else F(0)
    if verbose:
        print('squares: %d   side: %s  (= %.15g)' % (n, side, float(side)))
        print('min containment margin: %s  (= %.6e)' % (min_margin, float(min_margin)))
        print('min pair separation^2 : %s' % (min_sep,))
        print('min pair separation   = %.6e (float rendering of sqrt)' % (float(min_sep) ** 0.5))
        print('RESULT:', 'PASS -- s(%d) <= %s' % (n, side) if ok else 'FAIL')
    return ok


def _cmp(a, b):
    """compare margins a=(gap_a, L2_a), b=(gap_b, L2_b) as gap/sqrt(L2), exactly."""
    ga, la = a
    gb, lb = b
    if ga <= 0 and gb <= 0:
        return 0
    if ga > 0 and gb <= 0:
        return 1
    if ga <= 0 and gb > 0:
        return -1
    x = ga * ga * lb
    y = gb * gb * la
    return (x > y) - (x < y)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    with open(sys.argv[1]) as f:
        cert = json.load(f)
    sys.exit(0 if verify(cert) else 1)
