"""Method B for lane L64: unit squares, walls and pairs by exact clipped areas, in mpq.

Written clean room on 2026-11-09 from the definitions alone. It shares only the reader
with method A (`l64_sat.py`) and none of its reductions.

A quadrilateral with four edges of length 1, all turns of one sign and area 1 is a unit
square: four equal edges make a rhombus, turns of one sign make it convex, and a rhombus
of side 1 has area sin(angle), which is 1 only at a right angle.

A convex polygon Q lies in the closed box B exactly when Q clipped to B keeps Q's area.
Two convex polygons have disjoint interiors exactly when their intersection has area 0,
since a convex set with an interior point has positive area. Sutherland-Hodgman clipping
by closed half-planes, in exact rationals, yields the intersection itself: empty when
the closed squares are apart, a point or segment of area 0 when they touch, and a
polygon of positive area when they overlap.
"""

from __future__ import annotations

from gmpy2 import mpq

ZERO = mpq(0)


class ShapeErrorB(Exception):
    pass


def area2(poly: list[tuple[mpq, mpq]]) -> mpq:
    """Twice the signed shoelace area."""
    s = mpq(0)
    m = len(poly)
    for i in range(m):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % m]
        s += x0 * y1 - x1 * y0
    return s


class SquareB:
    __slots__ = ("id", "poly", "sense")

    def __init__(
        self, sid: int, corners: list[tuple[int, int, int, int]], unit: bool = True
    ) -> None:
        """unit=False decides only a square of some positive side (enlargement controls)."""
        self.id = sid
        pts = [(mpq(xn, xd), mpq(yn, yd)) for (xn, xd, yn, yd) in corners]
        edges = []
        length2 = None
        for k in range(4):
            x0, y0 = pts[k]
            x1, y1 = pts[(k + 1) % 4]
            dx, dy = x1 - x0, y1 - y0
            l2 = dx * dx + dy * dy
            if length2 is None:
                length2 = l2 if not unit else mpq(1)
            if l2 != length2 or l2 == 0:
                raise ShapeErrorB(f"edge {k} is not of length {'1' if unit else 'edge 0'}")
            edges.append((dx, dy))
        turns = [
            edges[k][0] * edges[(k + 1) % 4][1] - edges[k][1] * edges[(k + 1) % 4][0]
            for k in range(4)
        ]
        if not (all(t > 0 for t in turns) or all(t < 0 for t in turns)):
            raise ShapeErrorB("turns are not all of one sign")
        a2 = area2(pts)
        if a2 not in (2 * length2, -2 * length2):
            raise ShapeErrorB("area is not the square of the edge")
        self.sense = 1 if a2 > 0 else -1
        self.poly = pts if a2 > 0 else pts[::-1]


def clip(subject: list[tuple[mpq, mpq]], clipper: list[tuple[mpq, mpq]]) -> list:
    """Sutherland-Hodgman: subject clipped by the closed left half-planes of a CCW clipper."""
    out = list(subject)
    m = len(clipper)
    for k in range(m):
        if not out:
            return out
        ax, ay = clipper[k]
        bx, by = clipper[(k + 1) % m]
        ex, ey = bx - ax, by - ay
        inp = out
        d = [ex * (y - ay) - ey * (x - ax) for x, y in inp]
        out = []
        size = len(inp)
        for i in range(size):
            dp = d[i]
            dq = d[(i + 1) % size]
            px, py = inp[i]
            if dp >= 0:
                out.append((px, py))
            if (dp > 0 and dq < 0) or (dp < 0 and dq > 0):
                qx, qy = inp[(i + 1) % size]
                t = dp / (dp - dq)
                out.append((px + t * (qx - px), py + t * (qy - py)))
    return out


def pair_class(a: SquareB, b: SquareB) -> tuple[str, mpq]:
    """The class of a pair by its exact intersection, and the intersection's area."""
    r = clip(a.poly, b.poly)
    if not r:
        return "separated", ZERO
    a2 = area2(r)
    if a2 > 0:
        return "overlapping", a2 / 2
    if a2 == 0:
        return "touching", ZERO
    raise AssertionError("negative clipped area from CCW polygons")


def box(side: mpq) -> list[tuple[mpq, mpq]]:
    return [(mpq(0), mpq(0)), (side, mpq(0)), (side, side), (mpq(0), side)]


def contained(a: SquareB, side: mpq) -> tuple[bool, mpq]:
    """Whether the square lies in [0, side]^2, and the area it keeps when clipped there."""
    r = clip(a.poly, box(side))
    kept = area2(r) / 2 if r else ZERO
    return kept == area2(a.poly) / 2, kept


def corners_on_walls(a: SquareB, side: mpq) -> int:
    """How many of the square's corners lie on a wall line (x or y equal to 0 or side)."""
    return sum(1 for x, y in a.poly if x == 0 or y == 0 or x == side or y == side)
