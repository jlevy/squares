"""Method B for the L70 review: exact clipped areas in ``gmpy2.mpq``.

Clean room, sharing only the reader with method A. A square is a quadrilateral of
four corners computed here, in GMP rationals.

* Unit square: four edges of squared length 1, four turns of one sign and
  shoelace area 1. A convex quadrilateral with four unit edges is a rhombus, and a
  rhombus of side 1 and area 1 has a right angle, so it is a unit square.
* Containment: clip the square to ``[0, S]^2`` (Sutherland-Hodgman, closed
  half-planes, exact). It lies in the box exactly when it keeps area 1.
* Pairs: clip one square by the four closed half-planes of the other. The result is
  their intersection. Empty: apart. Nonempty with area 0: touching (a point or a
  segment). Positive area: the interiors meet, since a convex set has positive area
  exactly when its interior is nonempty.
"""

from __future__ import annotations

from typing import Any

import gmpy2
from gmpy2 import mpq

Point = tuple[Any, Any]


def corners_from_cert_row(row: tuple[int, ...]) -> list[Point]:
    xn, xd, yn, yd, tn, td = row
    x = mpq(xn, xd)
    y = mpq(yn, yd)
    t = mpq(tn, td)
    tt = t * t
    one = mpq(1)
    d = one + tt
    c = (one - tt) / d
    s = (2 * t) / d
    half = mpq(1, 2)
    # u = (c, s), v = (-s, c); corners x +- u/2 +- v/2 in the order (-,-), (+,-), (+,+), (-,+)
    ax, ay = half * c, half * s
    bx, by = -half * s, half * c
    return [
        (x - ax - bx, y - ay - by),
        (x + ax - bx, y + ay - by),
        (x + ax + bx, y + ay + by),
        (x - ax + bx, y - ay + by),
    ]


def corners_from_corner_row(row: tuple[int, ...]) -> list[Point]:
    return [(mpq(row[4 * k], row[4 * k + 1]), mpq(row[4 * k + 2], row[4 * k + 3])) for k in range(4)]


def area2(poly: list[Point]) -> Any:
    """Twice the signed shoelace area."""
    m = len(poly)
    if m < 3:
        return mpq(0)
    acc = mpq(0)
    for k in range(m):
        x1, y1 = poly[k]
        x2, y2 = poly[(k + 1) % m]
        acc += x1 * y2 - x2 * y1
    return acc


def is_unit_square(poly: list[Point]) -> bool:
    if len(poly) != 4:
        return False
    signs = set()
    for k in range(4):
        x0, y0 = poly[k]
        x1, y1 = poly[(k + 1) % 4]
        x2, y2 = poly[(k + 2) % 4]
        ex, ey = x1 - x0, y1 - y0
        if ex * ex + ey * ey != 1:
            return False
        fx, fy = x2 - x1, y2 - y1
        cr = ex * fy - ey * fx
        if cr == 0:
            return False
        signs.add(cr > 0)
    if len(signs) != 1:
        return False
    a2 = area2(poly)
    return a2 == 2 or a2 == -2


def ccw(poly: list[Point]) -> list[Point]:
    return poly if area2(poly) > 0 else list(reversed(poly))


def _clip(poly: list[Point], ax: Any, ay: Any, bx: Any, by: Any) -> list[Point]:
    """Keep the part of ``poly`` on the closed left side of the directed line a->b."""
    if not poly:
        return poly
    dx, dy = bx - ax, by - ay
    out: list[Point] = []
    m = len(poly)
    prev = poly[-1]
    fp = dx * (prev[1] - ay) - dy * (prev[0] - ax)
    for k in range(m):
        cur = poly[k]
        fc = dx * (cur[1] - ay) - dy * (cur[0] - ax)
        if fc >= 0:
            if fp < 0 and fc > 0:
                r = fp / (fp - fc)
                out.append((prev[0] + (cur[0] - prev[0]) * r, prev[1] + (cur[1] - prev[1]) * r))
            out.append(cur)
        elif fp > 0:
            r = fp / (fp - fc)
            out.append((prev[0] + (cur[0] - prev[0]) * r, prev[1] + (cur[1] - prev[1]) * r))
        prev, fp = cur, fc
    return out


def clip_convex(subject: list[Point], clipper_ccw: list[Point]) -> list[Point]:
    poly = list(subject)
    m = len(clipper_ccw)
    for k in range(m):
        a = clipper_ccw[k]
        b = clipper_ccw[(k + 1) % m]
        poly = _clip(poly, a[0], a[1], b[0], b[1])
        if not poly:
            break
    return poly


def box(side: Any) -> list[Point]:
    z = mpq(0)
    return [(z, z), (side, z), (side, side), (z, side)]


class ClipSquare:
    __slots__ = ("poly", "unit", "minx", "maxx", "miny", "maxy")

    def __init__(self, poly: list[Point]) -> None:
        self.unit = is_unit_square(poly)
        self.poly = ccw(poly)
        xs = [q[0] for q in poly]
        ys = [q[1] for q in poly]
        self.minx, self.maxx = min(xs), max(xs)
        self.miny, self.maxy = min(ys), max(ys)


def build(packing: Any) -> list[ClipSquare]:
    if packing.kind == "cert":
        return [ClipSquare(corners_from_cert_row(r)) for r in packing.squares]
    if packing.kind == "corners":
        return [ClipSquare(corners_from_corner_row(r)) for r in packing.squares]
    raise ValueError(f"unknown kind {packing.kind!r}")


def inside_box(sq: ClipSquare, side: Any) -> bool:
    clipped = clip_convex(sq.poly, box(side))
    return abs(area2(clipped)) == 2


def wall_touches(sq: ClipSquare, side: Any) -> tuple[bool, bool, bool, bool]:
    """(left, bottom, right, top): does a corner lie exactly on that wall line."""
    return (sq.minx == 0, sq.miny == 0, sq.maxx == side, sq.maxy == side)


def pair_class(a: ClipSquare, b: ClipSquare) -> tuple[str, Any]:
    """('apart' | 'touch' | 'overlap', intersection area)."""
    inter = clip_convex(b.poly, a.poly)
    if not inter:
        return "apart", mpq(0)
    a2 = abs(area2(inter))
    if a2 == 0:
        return "touch", mpq(0)
    return "overlap", a2 / 2


def version() -> str:
    return str(gmpy2.version())
