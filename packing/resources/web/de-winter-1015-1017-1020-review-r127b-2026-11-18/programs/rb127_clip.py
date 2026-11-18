"""Method B of lane r127b-1118: exact convex clipping in GMP rationals, from corners.

It is handed four corners per square and nothing else. Four points are a unit square in
the order listed when all four sides have squared length 1 and both diagonals squared
length 2 (a rhombus with equal diagonals is a square). The shoelace sum, which is +2 or
-2 for a unit square, gives the sense; a clockwise listing is reversed before clipping.

A pair is decided by clipping one square against the four closed half-planes to the
left of the other's counterclockwise edges (Sutherland-Hodgman, points on a line kept),
which gives their intersection exactly, and it is clipped both ways round: the two
results must agree in class and in area. Empty is apart; non-empty with zero area is
contact, since the interior of an intersection of convex sets is the intersection of
their interiors; positive area is overlap, by that area.

A wall is classed the same way, by clipping the square against the closed half-plane
outside it, and containment is decided apart: a unit square lies in the box exactly
when its intersection with the box has area exactly 1.

The module uses ``gmpy2.mpq`` throughout and imports nothing from this repository, the
source, or method A.
"""

from __future__ import annotations

from typing import Any

from gmpy2 import mpq

Pt = tuple[Any, Any]


def to_points(corners: tuple[tuple[tuple[int, int], tuple[int, int]], ...]) -> list[Pt]:
    return [(mpq(x[0], x[1]), mpq(y[0], y[1])) for x, y in corners]


def _d2(p: Pt, q: Pt) -> Any:
    dx = q[0] - p[0]
    dy = q[1] - p[1]
    return dx * dx + dy * dy


def shoelace2(poly: list[Pt]) -> Any:
    """Twice the signed area."""
    total = mpq(0)
    m = len(poly)
    for k in range(m):
        x0, y0 = poly[k]
        x1, y1 = poly[(k + 1) % m]
        total += x0 * y1 - x1 * y0
    return total


def unit_square(pts: list[Pt]) -> tuple[bool, int]:
    """Whether four listed points are a unit square in cyclic order, and their sense."""
    if len(pts) != 4:
        return False, 0
    for k in range(4):
        if _d2(pts[k], pts[(k + 1) % 4]) != 1:
            return False, 0
    if _d2(pts[0], pts[2]) != 2 or _d2(pts[1], pts[3]) != 2:
        return False, 0
    s2 = shoelace2(pts)
    if s2 == 2:
        return True, 1
    if s2 == -2:
        return True, -1
    return False, 0


def ccw(pts: list[Pt], sense: int) -> list[Pt]:
    return list(pts) if sense > 0 else list(reversed(pts))


def _side(p: Pt, q: Pt, x: Pt) -> Any:
    return (q[0] - p[0]) * (x[1] - p[1]) - (q[1] - p[1]) * (x[0] - p[0])


def clip_halfplane(poly: list[Pt], p: Pt, q: Pt) -> list[Pt]:
    """Keep the part of ``poly`` on or to the left of the directed line ``p -> q``."""
    out: list[Pt] = []
    m = len(poly)
    if m == 0:
        return out
    for k in range(m):
        cur = poly[k]
        nxt = poly[(k + 1) % m]
        sc = _side(p, q, cur)
        sn = _side(p, q, nxt)
        if sc >= 0:
            out.append(cur)
        if (sc > 0 and sn < 0) or (sc < 0 and sn > 0):
            t = sc / (sc - sn)
            out.append((cur[0] + t * (nxt[0] - cur[0]), cur[1] + t * (nxt[1] - cur[1])))
    return out


def clip_convex(subject: list[Pt], clipper_ccw: list[Pt]) -> list[Pt]:
    poly = list(subject)
    m = len(clipper_ccw)
    for k in range(m):
        poly = clip_halfplane(poly, clipper_ccw[k], clipper_ccw[(k + 1) % m])
        if not poly:
            break
    return poly


def area(poly: list[Pt]) -> Any:
    if len(poly) < 3:
        return mpq(0)
    return abs(shoelace2(poly)) / 2


def classify(poly: list[Pt]) -> tuple[str, Any]:
    if not poly:
        return "apart", mpq(0)
    a = area(poly)
    return ("contact", a) if a == 0 else ("overlap", a)


def pair(sq_i: list[Pt], sq_j: list[Pt]) -> tuple[str, Any, bool]:
    """Class and area of two counterclockwise squares, clipped both ways round."""
    c1, a1 = classify(clip_convex(sq_j, sq_i))
    c2, a2 = classify(clip_convex(sq_i, sq_j))
    return c1, a1, (c1 == c2 and a1 == a2)


def walls(sq: list[Pt], side: Any) -> tuple[list[tuple[str, Any]], Any]:
    """Each wall's class (left, bottom, right, top) and the area inside the box."""
    zero = mpq(0)
    coords = [c for p in sq for c in p]
    # Bounds that contain the square and the box, so that each quadrilateral below holds
    # the whole part of the square on its side of the wall.
    small = min(min(coords), zero) - 1
    big = max(max(coords), side) + 1
    # Closed half-planes outside each wall, written as counterclockwise quadrilaterals.
    outside = [
        [(small, small), (zero, small), (zero, big), (small, big)],
        [(small, small), (big, small), (big, zero), (small, zero)],
        [(side, small), (big, small), (big, big), (side, big)],
        [(small, side), (big, side), (big, big), (small, big)],
    ]
    classes = [classify(clip_convex(sq, region)) for region in outside]
    box = [(zero, zero), (side, zero), (side, side), (zero, side)]
    inside = area(clip_convex(sq, box))
    return [(c, a) for c, a in classes], inside


def projections_margin(sq_i: list[Pt], sq_j: list[Pt]) -> Any:
    """A third formulation: the margin from corner projections on the four edge normals.

    Each edge vector of a unit square has length 1, so the normal of an edge is the
    edge turned by a quarter, a rational unit vector, and every projection is exact.
    """
    best = None
    for sq in (sq_i, sq_j):
        for k in (0, 1):
            ex = sq[k + 1][0] - sq[k][0]
            ey = sq[k + 1][1] - sq[k][1]
            nx, ny = -ey, ex
            pi = [p[0] * nx + p[1] * ny for p in sq_i]
            pj = [p[0] * nx + p[1] * ny for p in sq_j]
            sep = max(min(pj) - max(pi), min(pi) - max(pj))
            best = sep if best is None or sep > best else best
    return best
