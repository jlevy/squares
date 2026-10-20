#!/usr/bin/env python3
"""Second, independent exact verifier for packing certificates (same format as verify_cert.py).

Method differs on purpose: no separating axes.  Squares are exact rational polygons (corners from the centre and the rational
rotation (c, s) = ((1-t^2)/(1+t^2), 2t/(1+t^2))).  Two closed convex polygons are disjoint iff (a) no vertex of either lies in
the closed other polygon and (b) no edge of one meets an edge of the other (closed segments).  Containment: every corner
strictly inside (0, S)^2.  All arithmetic in fractions.Fraction.  Pairs with centre distance^2 > 2 are disjoint (circumdiscs).

  verify_cert2.py cert.txt   -> exit 0 iff valid
"""
import sys
from fractions import Fraction as F


def corners(x, y, c, s):
    h = F(1, 2)
    return [(x + c * a - s * b, y + s * a + c * b) for a, b in ((h, h), (-h, h), (-h, -h), (h, -h))]  # counter-clockwise


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def in_closed(p, P):
    """p in closed convex CCW polygon P."""
    return all(cross(P[k], P[(k + 1) % 4], p) >= 0 for k in range(4))


def seg_meet(p1, p2, q1, q2):
    """Closed segments p1p2 and q1q2 intersect (including touching / collinear overlap)."""
    d1, d2 = cross(q1, q2, p1), cross(q1, q2, p2)
    d3, d4 = cross(p1, p2, q1), cross(p1, p2, q2)
    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        return True

    def on(a, b, p):
        return min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])
    return (d1 == 0 and on(q1, q2, p1)) or (d2 == 0 and on(q1, q2, p2)) or (d3 == 0 and on(p1, p2, q1)) or (d4 == 0 and on(p1, p2, q2))


def main(path):
    rows = [l.split() for l in open(path) if l.strip() and not l.lstrip().startswith('#')]
    n, S = int(rows[0][0]), F(rows[0][1])
    sq = []
    for r in rows[1:n + 1]:
        x, y, t = F(r[0]), F(r[1]), F(r[2])
        c, s = (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)
        sq.append(((x, y), corners(x, y, c, s)))
    assert len(sq) == n
    for (_, P) in sq:
        for p in P:
            if not (0 < p[0] < S and 0 < p[1] < S):
                print('INVALID: corner outside the open box'); return 1
    checked = 0
    for i in range(n):
        for j in range(i + 1, n):
            (ci, P), (cj, Q) = sq[i], sq[j]
            if (ci[0] - cj[0]) ** 2 + (ci[1] - cj[1]) ** 2 > 2:
                continue
            checked += 1
            if any(in_closed(p, Q) for p in P) or any(in_closed(q, P) for q in Q):
                print(f'INVALID: vertex containment between #{i} and #{j}'); return 1
            for a in range(4):
                for b in range(4):
                    if seg_meet(P[a], P[(a + 1) % 4], Q[b], Q[(b + 1) % 4]):
                        print(f'INVALID: edges of #{i} and #{j} meet'); return 1
    print(f'VALID: {n} closed unit squares pairwise disjoint inside the open box of side {float(S):.20g} ({checked} close pairs checked)')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
