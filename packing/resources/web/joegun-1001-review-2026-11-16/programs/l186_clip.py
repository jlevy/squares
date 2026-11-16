"""Lane L186, method B: exact convex clipping in GMP rationals, from the corners.

It is handed four corners per square and nothing else.

A square is accepted as a unit square in cyclic order when its four sides have
squared length exactly 1 and both diagonals squared length exactly 2 (a rhombus
with equal diagonals is a square); the shoelace sum, +2 or -2, gives the sense,
and a clockwise listing is reversed before clipping.

A pair is decided by clipping one square against the four closed half-planes to
the left of the other's counterclockwise edges (Sutherland-Hodgman, keeping
points on the line), which gives their intersection exactly; it is done both
ways round and the two results must agree in class and area. Empty is apart;
non-empty with zero area is contact (the interior of an intersection of convex
sets is the intersection of their interiors); positive area is overlap, by that
area.

A wall is classed the same way, by clipping the square against the closed
half-plane outside it; containment is the area of the square's intersection
with the box, which is exactly 1 when the square lies inside.
"""

from __future__ import annotations

from typing import Any

import gmpy2
from gmpy2 import mpq

from l186_reader import Square

Q = Any  # an mpq
Pt = tuple[Q, Q]


def to_mpq(sq: Square) -> list[Pt]:
    return [(mpq(x.numerator, x.denominator), mpq(y.numerator, y.denominator)) for x, y in sq]


def _d2(a: Pt, b: Pt) -> Q:
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return dx * dx + dy * dy


def shoelace2(poly: list[Pt]) -> Q:
    s = mpq(0)
    m = len(poly)
    for k in range(m):
        x0, y0 = poly[k]
        x1, y1 = poly[(k + 1) % m]
        s += x0 * y1 - x1 * y0
    return s


def unit_square(pts: list[Pt]) -> tuple[bool, int]:
    sides_ok = all(_d2(pts[k], pts[(k + 1) % 4]) == 1 for k in range(4))
    diag_ok = _d2(pts[0], pts[2]) == 2 and _d2(pts[1], pts[3]) == 2
    s2 = shoelace2(pts)
    sense = 1 if s2 > 0 else (-1 if s2 < 0 else 0)
    ok = sides_ok and diag_ok and s2 in (mpq(2), mpq(-2))
    return ok, sense


def ccw(pts: list[Pt]) -> list[Pt]:
    return pts if shoelace2(pts) > 0 else list(reversed(pts))


def clip_halfplane(poly: list[Pt], a: Q, b: Q, c: Q) -> list[Pt]:
    """Keep the part of a convex polygon (vertex list) where a*x + b*y + c >= 0."""
    m = len(poly)
    if m == 0:
        return []
    vals = [a * p[0] + b * p[1] + c for p in poly]
    out: list[Pt] = []
    for k in range(m):
        p, fp = poly[k], vals[k]
        r, fr = poly[(k + 1) % m], vals[(k + 1) % m]
        if fp >= 0:
            out.append(p)
        if (fp > 0 and fr < 0) or (fp < 0 and fr > 0):
            t = fp / (fp - fr)
            out.append((p[0] + (r[0] - p[0]) * t, p[1] + (r[1] - p[1]) * t))
    return out


def clip_by_square(poly: list[Pt], sq_ccw: list[Pt]) -> list[Pt]:
    """Intersect poly with the closed square sq_ccw (counterclockwise)."""
    res = poly
    for k in range(4):
        ax, ay = sq_ccw[k]
        bx, by = sq_ccw[(k + 1) % 4]
        # left of a->b: (bx-ax)*(y-ay) - (by-ay)*(x-ax) >= 0
        a = -(by - ay)
        b = bx - ax
        c = (by - ay) * ax - (bx - ax) * ay
        res = clip_halfplane(res, a, b, c)
        if not res:
            return []
    return res


def classify(poly: list[Pt]) -> tuple[str, Q]:
    if not poly:
        return "apart", mpq(0)
    area = abs(shoelace2(poly)) / 2
    return ("touch" if area == 0 else "overlap"), area


def pair_class(a_ccw: list[Pt], b_ccw: list[Pt]) -> tuple[str, Q, bool]:
    """Class and area of a pair, clipped both ways; the flag says the two agree."""
    c1, ar1 = classify(clip_by_square(a_ccw, b_ccw))
    c2, ar2 = classify(clip_by_square(b_ccw, a_ccw))
    return c1, ar1, (c1 == c2 and ar1 == ar2)


def wall_classes(pts_ccw: list[Pt], side: Q) -> tuple[list[str], Q]:
    """Classes at the left, bottom, right and top walls, and the area inside the box."""
    outside = [
        (mpq(-1), mpq(0), mpq(0)),  # x <= 0
        (mpq(0), mpq(-1), mpq(0)),  # y <= 0
        (mpq(1), mpq(0), -side),  # x >= S
        (mpq(0), mpq(1), -side),  # y >= S
    ]
    classes: list[str] = []
    for a, b, c in outside:
        cls, _ = classify(clip_halfplane(pts_ccw, a, b, c))
        classes.append({"apart": "apart", "touch": "touch", "overlap": "cross"}[cls])
    inside = pts_ccw
    for a, b, c in (
        (mpq(1), mpq(0), mpq(0)),
        (mpq(0), mpq(1), mpq(0)),
        (mpq(-1), mpq(0), side),
        (mpq(0), mpq(-1), side),
    ):
        inside = clip_halfplane(inside, a, b, c)
    area_in = abs(shoelace2(inside)) / 2 if inside else mpq(0)
    return classes, area_in


def version() -> str:
    return f"gmpy2 {gmpy2.version()}, {gmpy2.mp_version()}"
