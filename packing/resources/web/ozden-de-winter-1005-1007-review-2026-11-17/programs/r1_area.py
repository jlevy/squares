"""Method B: the exact intersection of two squares, in GMP rationals.

Lane R1, stage 4 review of #1005, #1006 and #1007.  Clean-room.

Method B is handed points and nothing else.

Four points are a unit square in cyclic order exactly when its four sides have
squared length 1 and both diagonals squared length 2 (four equal sides make a
rhombus or a folded one; a diagonal of squared length 2 excludes the fold and the
other diagonal then makes the rhombus a square).  The shoelace sum, +2 or -2, is
the sense of the listing; a clockwise listing is reversed.

The intersection of two convex polygons P and Q is the convex hull of three kinds
of points: the vertices of P that lie in Q, the vertices of Q that lie in P, and
the points where an edge of P meets a non-parallel edge of Q.  (An extreme point
of the intersection that is a vertex of neither lies inside an edge of each; were
those edges parallel the point would lie inside a segment of the intersection.)
All three are computed with closed tests, so points of contact are kept.  The hull
is built by a monotone chain and measured by the shoelace sum:

    no point        -> the squares are apart
    area exactly 0  -> they touch, with disjoint interiors
    area above 0    -> their interiors meet, by that area

since the interior of an intersection of convex sets is the intersection of their
interiors.  A wall is classed the same way, by intersecting the square with the
closed half-plane outside it, and containment is decided apart: a unit square lies
in the box exactly when its intersection with the box has area exactly 1.

This is vertex enumeration, not successive clipping.
"""

from __future__ import annotations

from gmpy2 import mpq

ZERO = mpq(0)
ONE = mpq(1)
TWO = mpq(2)


def points_from_corners(corners):
    return [(mpq(x.numerator, x.denominator), mpq(y.numerator, y.denominator)) for x, y in corners]


def points_from_centre(cx, cy, ux, uy):
    """Corners from the half-diagonals p = (u + v)/2 and q = (u - v)/2, v = (-uy, ux)."""
    cx, cy = mpq(cx.numerator, cx.denominator), mpq(cy.numerator, cy.denominator)
    ux, uy = mpq(ux.numerator, ux.denominator), mpq(uy.numerator, uy.denominator)
    px, py = (ux - uy) / 2, (uy + ux) / 2
    qx, qy = (ux + uy) / 2, (uy - ux) / 2
    return [(cx - px, cy - py), (cx + qx, cy + qy), (cx + px, cy + py), (cx - qx, cy - qy)]


def of_packing(packing):
    if packing.form == "corners":
        return [points_from_corners(c) for c in packing.squares]
    return [points_from_centre(*c) for c in packing.squares]


def _d2(a, b):
    dx, dy = a[0] - b[0], a[1] - b[1]
    return dx * dx + dy * dy


def shoelace(points):
    """Twice the signed area of a polygon listed in order."""
    total = ZERO
    count = len(points)
    for k in range(count):
        ax, ay = points[k]
        bx, by = points[(k + 1) % count]
        total += ax * by - bx * ay
    return total


def unit_square(points):
    """(is a unit square in cyclic order, sense of the listing)."""
    if len(points) != 4:
        return False, 0
    sides = all(_d2(points[k], points[(k + 1) % 4]) == ONE for k in range(4))
    diagonals = _d2(points[0], points[2]) == TWO and _d2(points[1], points[3]) == TWO
    twice = shoelace(points)
    sense = (twice > 0) - (twice < 0)
    return sides and diagonals, sense


def counterclockwise(points):
    return list(points) if shoelace(points) > 0 else list(reversed(points))


def _inside_closed(p, poly):
    """p lies in the closed convex polygon poly, listed counterclockwise."""
    px, py = p
    count = len(poly)
    for k in range(count):
        ax, ay = poly[k]
        bx, by = poly[(k + 1) % count]
        if (bx - ax) * (py - ay) - (by - ay) * (px - ax) < 0:
            return False
    return True


def _hull_twice_area(points):
    """Twice the area of the convex hull of a finite set of points."""
    pts = sorted(set(points))
    if len(pts) < 3:
        return ZERO

    def turn(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower = []
    for p in pts:
        while len(lower) >= 2 and turn(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and turn(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    hull = lower[:-1] + upper[:-1]
    if len(hull) < 3:
        return ZERO
    return shoelace(hull)


def _classify(candidates, apart_word):
    if not candidates:
        return apart_word, ZERO
    twice = _hull_twice_area(candidates)
    if twice == 0:
        return "touching", ZERO
    return "overlapping", twice / 2


def pair(P, Q):
    """(class, area) of two convex polygons listed counterclockwise."""
    candidates = [p for p in P if _inside_closed(p, Q)]
    candidates += [q for q in Q if _inside_closed(q, P)]
    np, nq = len(P), len(Q)
    for k in range(np):
        ax, ay = P[k]
        bx, by = P[(k + 1) % np]
        rx, ry = bx - ax, by - ay
        for m in range(nq):
            cx, cy = Q[m]
            dx, dy = Q[(m + 1) % nq]
            sx, sy = dx - cx, dy - cy
            den = rx * sy - ry * sx
            if den == 0:
                continue
            wx, wy = cx - ax, cy - ay
            t = (wx * sy - wy * sx) / den
            if t < 0 or t > 1:
                continue
            u = (wx * ry - wy * rx) / den
            if u < 0 or u > 1:
                continue
            candidates.append((ax + t * rx, ay + t * ry))
    return _classify(candidates, "apart")


def beyond(P, a, b, c):
    """(class, area) of polygon P against the closed half-plane a*x + b*y + c >= 0."""
    values = [a * x + b * y + c for x, y in P]
    candidates = [p for p, f in zip(P, values) if f >= 0]
    count = len(P)
    for k in range(count):
        f0, f1 = values[k], values[(k + 1) % count]
        if (f0 < 0 < f1) or (f1 < 0 < f0):
            t = f0 / (f0 - f1)
            ax, ay = P[k]
            bx, by = P[(k + 1) % count]
            candidates.append((ax + t * (bx - ax), ay + t * (by - ay)))
    return _classify(candidates, "apart")


def walls(P, side):
    """Each wall's (class, area outside) in the order left, bottom, right, top."""
    s = mpq(side.numerator, side.denominator)
    return (
        beyond(P, -ONE, ZERO, ZERO),  # x <= 0
        beyond(P, ZERO, -ONE, ZERO),  # y <= 0
        beyond(P, ONE, ZERO, -s),  # x >= side
        beyond(P, ZERO, ONE, -s),  # y >= side
    )


def area_inside_box(P, side):
    """The area of the square's part inside the closed box [0, side]^2."""
    s = mpq(side.numerator, side.denominator)
    box = [(ZERO, ZERO), (s, ZERO), (s, s), (ZERO, s)]
    return pair(P, box)[1]
