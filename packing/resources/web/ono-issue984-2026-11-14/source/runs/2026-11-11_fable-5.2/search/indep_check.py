#!/usr/bin/env python3
"""Independent exact re-check of a certificate (shares no code with the frozen verifier).

It does NOT replace the frozen judge; it is one of the "try to break it" steps of AGENTS.md rule 7.
Method: exact rational arithmetic (fractions.Fraction); every square is rebuilt as a polygon from
(cx, cy, t); the intersection of every pair is computed by Sutherland-Hodgman clipping and its
area (shoelace) must be exactly 0; every vertex must lie in [0, S]^2; all edges must have squared
length exactly 1 and adjacent edges must be perpendicular.

Usage: indep_check.py certificate.json
"""
import json
import sys
from fractions import Fraction as F


def square(cx, cy, t):
    d = 1 + t * t
    c, s = (1 - t * t) / d, 2 * t / d
    h = F(1, 2)
    pts = []
    for a, b in ((h, h), (-h, h), (-h, -h), (h, -h)):          # counter-clockwise
        pts.append((cx + a * c - b * s, cy + a * s + b * c))
    return pts


def area(poly):
    a = F(0)
    for i in range(len(poly)):
        x1, y1 = poly[i]; x2, y2 = poly[(i + 1) % len(poly)]
        a += x1 * y2 - x2 * y1
    return a / 2


def clip(subject, clipper):
    """Sutherland-Hodgman: subject polygon clipped by convex CCW clipper; exact."""
    out = subject
    for i in range(len(clipper)):
        ax, ay = clipper[i]; bx, by = clipper[(i + 1) % len(clipper)]
        inp = out
        out = []
        if not inp:
            break

        def side(p):
            return (bx - ax) * (p[1] - ay) - (by - ay) * (p[0] - ax)      # > 0 : left of a->b (inside)
        for j in range(len(inp)):
            p = inp[j]; q = inp[(j + 1) % len(inp)]
            sp, sq = side(p), side(q)
            if sp >= 0:
                out.append(p)
            if (sp > 0 and sq < 0) or (sp < 0 and sq > 0):
                tpar = sp / (sp - sq)
                out.append((p[0] + tpar * (q[0] - p[0]), p[1] + tpar * (q[1] - p[1])))
    return out


def main(path):
    cert = json.load(open(path))
    n = cert["n"]
    S = F(cert["side"])
    sq = []
    for q in cert["squares"]:
        assert isinstance(q["cx"], str) and isinstance(q["cy"], str) and isinstance(q.get("t", "0"), str)
        sq.append(square(F(q["cx"]), F(q["cy"]), F(q.get("t", "0"))))
    assert len(sq) == n, "wrong number of squares"
    for k, P in enumerate(sq):
        for i in range(4):
            x1, y1 = P[i]; x2, y2 = P[(i + 1) % 4]; x3, y3 = P[(i + 2) % 4]
            assert (x2 - x1) ** 2 + (y2 - y1) ** 2 == 1, f"square {k}: edge length != 1"
            assert (x2 - x1) * (x3 - x2) + (y2 - y1) * (y3 - y2) == 0, f"square {k}: not a right angle"
            assert 0 <= x1 <= S and 0 <= y1 <= S, f"square {k}: vertex outside container"
        assert area(P) == 1
    worst = F(0)
    pairs = 0
    cen = [(sum(p[0] for p in P) / 4, sum(p[1] for p in P) / 4) for P in sq]
    for i in range(n):
        for j in range(i + 1, n):
            dx = cen[i][0] - cen[j][0]; dy = cen[i][1] - cen[j][1]
            if dx * dx + dy * dy >= 2:
                continue
            pairs += 1
            inter = clip(sq[i], sq[j])
            a = area(inter) if len(inter) >= 3 else F(0)
            if a > worst:
                worst = a
            assert a == 0, f"squares {i} and {j} overlap with area {float(a):.3e}"
    xs = [p[0] for P in sq for p in P]; ys = [p[1] for P in sq for p in P]
    print(f"INDEPENDENT CHECK PASSED: n={n}, {pairs} close pairs clipped exactly, max intersection area = {worst}, "
          f"all vertices inside [0,S]^2, S = {float(S):.15f}, bounding box = [{float(min(xs)):.3g},{float(max(xs)):.12f}] x [{float(min(ys)):.3g},{float(max(ys)):.12f}]")


if __name__ == "__main__":
    main(sys.argv[1])
