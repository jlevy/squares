"""Method B: unit squares, walls and pairs by exact clipping of closed polygons.

Lane L108, blind stage 4 review of jlevy/squares#959. Arithmetic: CPython's
fractions.Fraction. Input: the integers the reader hands over. Shares nothing with
method A.

A listed quadrilateral is a unit square when its four sides have squared length 1 and
both diagonals squared length 2 (a rhombus with equal diagonals is a square), and its
shoelace area is 1 in absolute value. A pair is decided by clipping the first square to
the second's four closed half-planes: an empty result means the closed squares are
apart, a non-empty result of area 0 that they touch with disjoint interiors, and a
positive area that their interiors meet. For two convex bodies the interior of the
intersection is the intersection of the interiors, so the area decides. A wall is
decided the same way with the wall's closed outer half-plane, and containment by
clipping the square to the box and keeping area 1.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

FPoint = tuple[Fraction, Fraction]


@dataclass(frozen=True)
class SquareB:
    corners: tuple[FPoint, FPoint, FPoint, FPoint]
    orientation: int  # sign of the shoelace area: +1 counterclockwise, -1 clockwise


def _f(r: tuple[int, int]) -> Fraction:
    return Fraction(r[0], r[1])


def _sq_len(a: FPoint, b: FPoint) -> Fraction:
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    return dx * dx + dy * dy


def twice_area(poly: list[FPoint] | tuple[FPoint, ...]) -> Fraction:
    """Twice the signed shoelace area."""
    total = Fraction(0)
    m = len(poly)
    for k in range(m):
        x0, y0 = poly[k]
        x1, y1 = poly[(k + 1) % m]
        total += x0 * y1 - x1 * y0
    return total


def build(raw: tuple[tuple[tuple[int, int], tuple[int, int]], ...]) -> SquareB | None:
    """The square from four integer corners, or None when it is not a unit square."""
    c = tuple((_f(x), _f(y)) for x, y in raw)
    sides = [_sq_len(c[k], c[(k + 1) % 4]) for k in range(4)]
    diagonals = [_sq_len(c[0], c[2]), _sq_len(c[1], c[3])]
    if any(s != 1 for s in sides) or any(d != 2 for d in diagonals):
        return None
    area2 = twice_area(c)
    if abs(area2) != 2:
        return None
    return SquareB(corners=(c[0], c[1], c[2], c[3]), orientation=1 if area2 > 0 else -1)


# A closed half-plane {p : a*x + b*y + c >= 0}.
HalfPlane = tuple[Fraction, Fraction, Fraction]


def _value(h: HalfPlane, p: FPoint) -> Fraction:
    return h[0] * p[0] + h[1] * p[1] + h[2]


def clip(poly: list[FPoint], h: HalfPlane) -> list[FPoint]:
    """Sutherland-Hodgman against one closed half-plane; boundary points are kept."""
    out: list[FPoint] = []
    m = len(poly)
    for k in range(m):
        p = poly[k]
        q = poly[(k + 1) % m]
        vp = _value(h, p)
        vq = _value(h, q)
        if vp >= 0:
            out.append(p)
        if (vp > 0 > vq) or (vp < 0 < vq):
            t = vp / (vp - vq)
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return out


def inner_half_planes(sq: SquareB) -> list[HalfPlane]:
    """The four closed half-planes whose intersection is the square."""
    out: list[HalfPlane] = []
    c = sq.corners
    for k in range(4):
        (x0, y0), (x1, y1) = c[k], c[(k + 1) % 4]
        ex, ey = x1 - x0, y1 - y0
        # orientation * cross(e, p - c_k) >= 0 is the inner side of edge k.
        s = sq.orientation
        out.append((-s * ey, s * ex, s * (ey * x0 - ex * y0)))
    return out


def classify_poly(poly: list[FPoint]) -> tuple[str, Fraction]:
    if not poly:
        return ("clear", Fraction(0))
    area = abs(twice_area(poly)) / 2
    return ("contact" if area == 0 else "overlap", area)


def pair(a: SquareB, b_planes: list[HalfPlane]) -> tuple[str, Fraction]:
    poly: list[FPoint] = list(a.corners)
    for h in b_planes:
        poly = clip(poly, h)
        if not poly:
            break
    return classify_poly(poly)


def wall_planes(side: Fraction) -> dict[str, HalfPlane]:
    """Each wall's closed outer half-plane."""
    zero, one = Fraction(0), Fraction(1)
    return {
        "left": (-one, zero, zero),  # x <= 0
        "bottom": (zero, -one, zero),  # y <= 0
        "right": (one, zero, -side),  # x >= side
        "top": (zero, one, -side),  # y >= side
    }


def wall(sq: SquareB, outer: HalfPlane) -> tuple[str, Fraction]:
    return classify_poly(clip(list(sq.corners), outer))


def area_in_box(sq: SquareB, side: Fraction) -> Fraction:
    zero, one = Fraction(0), Fraction(1)
    poly: list[FPoint] = list(sq.corners)
    for h in ((one, zero, zero), (zero, one, zero), (-one, zero, side), (zero, -one, side)):
        poly = clip(poly, h)
        if not poly:
            return Fraction(0)
    return abs(twice_area(poly)) / 2


def side_f(side: tuple[int, int]) -> Fraction:
    return _f(side)
