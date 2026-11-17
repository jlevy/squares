"""Method B: exact clipped areas in GMP rationals (gmpy2.mpq).

A polygon is a unit square when its four edges have squared length 1, its four turns
have one strict sign, and its signed area is +/-1. (A convex quadrilateral with four
unit sides is a rhombus, and a rhombus of area 1 is the unit square.)

A pair is the first square clipped (Sutherland-Hodgman, closed half-planes) by the
other's four edge half-planes. In exact arithmetic that is the closed intersection:
empty means apart, nonempty with area 0 means contact, positive area means the
interiors meet. A wall is the square clipped by the wall's closed outer half-plane,
read the same three ways; containment is clipping to the box and keeping area 1.

It shares nothing with Method A except the integers the reader hands it.
"""

from __future__ import annotations

from dataclasses import dataclass

from gmpy2 import mpq

PointQ = tuple[mpq, mpq]
HalfPlane = tuple[mpq, mpq, mpq]  # a*x + b*y + c >= 0


@dataclass(frozen=True)
class SquareB:
    corners: tuple[PointQ, ...]
    sense: int
    halfplanes: tuple[HalfPlane, ...]


def _cross(ax: mpq, ay: mpq, bx: mpq, by: mpq) -> mpq:
    return ax * by - ay * bx


def twice_area(poly: list[PointQ] | tuple[PointQ, ...]) -> mpq:
    total = mpq(0)
    count = len(poly)
    for k in range(count):
        x0, y0 = poly[k]
        x1, y1 = poly[(k + 1) % count]
        total += x0 * y1 - x1 * y0
    return total


def make_square(points: list[tuple[tuple[int, int], tuple[int, int]]]) -> SquareB | str:
    q = tuple((mpq(*x), mpq(*y)) for x, y in points)
    edges = [(q[(k + 1) % 4][0] - q[k][0], q[(k + 1) % 4][1] - q[k][1]) for k in range(4)]
    for ex, ey in edges:
        if ex * ex + ey * ey != 1:
            return "an edge is not of squared length 1"
    turns = [_cross(*edges[k], *edges[(k + 1) % 4]) for k in range(4)]
    if not (all(t > 0 for t in turns) or all(t < 0 for t in turns)):
        return "turns are not of one strict sign"
    area2 = twice_area(q)
    if abs(area2) != 2:
        return "area is not 1"
    sense = 1 if area2 > 0 else -1
    planes = []
    for k in range(4):
        ex, ey = edges[k]
        # Inside of a counterclockwise edge is its left: cross(e, X - q_k) >= 0.
        a, b = -ey * sense, ex * sense
        c = -(a * q[k][0] + b * q[k][1])
        planes.append((a, b, c))
    return SquareB(corners=q, sense=sense, halfplanes=tuple(planes))


def clip(poly: list[PointQ], plane: HalfPlane) -> list[PointQ]:
    a, b, c = plane
    out: list[PointQ] = []
    count = len(poly)
    for k in range(count):
        s = poly[k - 1] if count > 1 else poly[0]
        e = poly[k]
        ds = a * s[0] + b * s[1] + c
        de = a * e[0] + b * e[1] + c
        if de >= 0:
            if ds < 0:
                t = ds / (ds - de)
                out.append((s[0] + t * (e[0] - s[0]), s[1] + t * (e[1] - s[1])))
            out.append(e)
        elif ds >= 0:
            t = ds / (ds - de)
            out.append((s[0] + t * (e[0] - s[0]), s[1] + t * (e[1] - s[1])))
    return out


def clip_all(poly: list[PointQ], planes: tuple[HalfPlane, ...] | list[HalfPlane]) -> list[PointQ]:
    for plane in planes:
        poly = clip(poly, plane)
        if not poly:
            return poly
    return poly


def pair(a: SquareB, b: SquareB) -> tuple[str, mpq]:
    """Class ('clear', 'contact', 'overlap') and the exact intersection area."""
    region = clip_all(list(a.corners), b.halfplanes)
    if not region:
        return "clear", mpq(0)
    area = abs(twice_area(region)) / 2
    return ("overlap" if area > 0 else "contact"), area


def outer_planes(side: mpq) -> dict[str, HalfPlane]:
    return {
        "left": (mpq(-1), mpq(0), mpq(0)),
        "bottom": (mpq(0), mpq(-1), mpq(0)),
        "right": (mpq(1), mpq(0), -side),
        "top": (mpq(0), mpq(1), -side),
    }


def inner_planes(side: mpq) -> list[HalfPlane]:
    return [
        (mpq(1), mpq(0), mpq(0)),
        (mpq(0), mpq(1), mpq(0)),
        (mpq(-1), mpq(0), side),
        (mpq(0), mpq(-1), side),
    ]


def wall(sq: SquareB, plane: HalfPlane) -> tuple[str, mpq]:
    """Class ('clear', 'contact', 'outside') against one wall, and the area outside."""
    region = clip_all(list(sq.corners), [plane])
    if not region:
        return "clear", mpq(0)
    area = abs(twice_area(region)) / 2
    return ("outside" if area > 0 else "contact"), area


def inside_area(sq: SquareB, side: mpq) -> mpq:
    region = clip_all(list(sq.corners), inner_planes(side))
    return abs(twice_area(region)) / 2 if region else mpq(0)
