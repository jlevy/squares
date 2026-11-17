"""Lane L159's method B: exact convex clipping in GMP rationals.

Clean-room code written for the stage 4 review of issue #983. It imports nothing from
this repository or from the source, and reuses no code of any earlier review.

Four points are a unit square in cyclic order when all four sides have squared length 1
and both diagonals squared length 2: by the converse of Pythagoras the angles at P_1 and
P_3 are right, and P_1 and P_3 are then the two distinct points at distance 1 from both
P_0 and P_2. The listing sense is the sign of the shoelace sum, which is then +-2.

A pair is decided by clipping one square against the four closed half-planes of the
other's edges, keeping boundary points (Sutherland-Hodgman, convex against convex), so
the result is the intersection exactly. Empty is apart; non-empty with zero area is
contact, since the interior of an intersection of convex sets is the intersection of
their interiors; positive area is overlap, by that area.

A wall is classed the same way, by clipping the square against the closed half-plane
outside it. Containment is decided on its own: a unit square lies in the box exactly
when its intersection with the box has area 1.
"""

from __future__ import annotations

from collections.abc import Callable

from gmpy2 import mpq

Rational = tuple[int, int]
Point = tuple[Rational, Rational]
QPoint = tuple[object, object]
Affine = Callable[[QPoint], object]


def to_points(corners: tuple[Point, ...]) -> list[QPoint]:
    """The corners as gmpy2 rationals."""
    return [(mpq(xp, xq), mpq(yp, yq)) for (xp, xq), (yp, yq) in corners]


def _d2(a: QPoint, b: QPoint) -> object:
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return dx * dx + dy * dy


def is_unit_square(p: list[QPoint]) -> bool:
    """Four sides of squared length 1 and two diagonals of squared length 2."""
    if len(p) != 4:
        return False
    if any(_d2(p[k], p[(k + 1) % 4]) != 1 for k in range(4)):
        return False
    return _d2(p[0], p[2]) == 2 and _d2(p[1], p[3]) == 2


def twice_area(poly: list[QPoint]) -> object:
    """The signed shoelace sum."""
    total = mpq(0)
    m = len(poly)
    for k in range(m):
        x0, y0 = poly[k]
        x1, y1 = poly[(k + 1) % m]
        total += x0 * y1 - x1 * y0
    return total


def sense(p: list[QPoint]) -> int:
    """+1 for a counterclockwise listing, -1 for clockwise, 0 for neither."""
    s = twice_area(p)
    if s == 2:
        return 1
    if s == -2:
        return -1
    return 0


def inside(value: object) -> bool:
    """The closed half-plane f >= 0 keeps its boundary."""
    return value >= 0


def _crossing(a: QPoint, b: QPoint, fa: object, fb: object) -> QPoint:
    t = fa / (fa - fb)
    return (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))


def clip(poly: list[QPoint], f: Affine) -> list[QPoint]:
    """Clip a convex polygon (possibly degenerate) against the closed half-plane f >= 0."""
    m = len(poly)
    if m == 0:
        return []
    values = [f(v) for v in poly]
    out: list[QPoint] = []
    for k in range(m):
        a, b = poly[k - 1], poly[k]
        fa, fb = values[k - 1], values[k]
        if inside(fb):
            if not inside(fa):
                out.append(_crossing(a, b, fa, fb))
            out.append(b)
        elif inside(fa):
            out.append(_crossing(a, b, fa, fb))
    return out


def edge_half_planes(p: list[QPoint]) -> list[Affine]:
    """The four closed inner half-planes of a unit square's edges."""
    s = sense(p)
    planes: list[Affine] = []
    for k in range(4):
        ax, ay = p[k]
        bx, by = p[(k + 1) % 4]
        ex, ey = bx - ax, by - ay

        def plane(v: QPoint, ax=ax, ay=ay, ex=ex, ey=ey) -> object:
            return s * (ex * (v[1] - ay) - ey * (v[0] - ax))

        planes.append(plane)
    return planes


def classify_area(poly: list[QPoint]) -> tuple[str, object]:
    """Empty, zero area or positive area, with the area."""
    if not poly:
        return "apart", mpq(0)
    area = abs(twice_area(poly)) / 2
    if area == 0:
        return "contact", area
    return "overlap", area


def pair(p: list[QPoint], planes_q: list[Affine]) -> tuple[str, object]:
    """Clip square p against the other square's closed half-planes."""
    poly = list(p)
    for f in planes_q:
        poly = clip(poly, f)
        if not poly:
            return "apart", mpq(0)
    return classify_area(poly)


def wall_planes(side: Rational) -> list[Affine]:
    """The closed half-planes outside the left, bottom, right and top walls."""
    s = mpq(side[0], side[1])
    return [
        lambda v: -v[0],
        lambda v: -v[1],
        lambda v: v[0] - s,
        lambda v: v[1] - s,
    ]


def walls(p: list[QPoint], side: Rational) -> list[str]:
    """Each wall's class: apart, contact, or cross (positive area outside)."""
    out = []
    for f in wall_planes(side):
        cls, _ = classify_area(clip(list(p), f))
        out.append("cross" if cls == "overlap" else cls)
    return out


def contained(p: list[QPoint], side: Rational) -> bool:
    """The square meets the closed box in area exactly 1."""
    s = mpq(side[0], side[1])
    poly = list(p)
    for f in (lambda v: v[0], lambda v: v[1], lambda v: s - v[0], lambda v: s - v[1]):
        poly = clip(poly, f)
    return bool(poly) and abs(twice_area(poly)) == 2
