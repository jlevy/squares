"""Lane L109's method B: exact clipping in GMP rationals (``gmpy2.mpq``).

A polygon is a unit square when each of its four edges has squared length 1, each two
consecutive edges have dot product 0, and every turn (the cross product of consecutive
edges) has the same sign. Unit, perpendicular and turning one way, the edges close a
square.

A pair is decided by clipping the first square with the four closed inner half-planes
of the second (Sutherland-Hodgman, exact): an empty result means the closed squares are
disjoint, a non-empty result of area 0 that they touch with disjoint interiors, and a
positive area that their interiors meet. The polygon kept is exactly the intersection,
since each half-plane of a convex polygon keeps a convex polygon whose vertices are the
kept vertices and the crossing points.

A wall is decided by clipping the square with the wall's closed outer half-plane, read
the same three ways (clear, contact, outside); containment is clipping with the four
inner half-planes of the box and keeping area exactly 1.

Shares nothing with method A but the integers the reader hands it.
"""

from __future__ import annotations

from dataclasses import dataclass

import gmpy2
from gmpy2 import mpq

Pt = tuple[mpq, mpq]
Half = tuple[mpq, mpq, mpq]  # a*x + b*y + c >= 0


class NotUnit(Exception):
    pass


@dataclass(frozen=True)
class SquareB:
    pts: tuple[Pt, Pt, Pt, Pt]
    inner: tuple[Half, Half, Half, Half]  # the closed inner half-planes of the edges
    turn: int


def make(pts: list[Pt]) -> SquareB:
    if len(pts) != 4:
        raise NotUnit("not four corners")
    edges = []
    for i in range(4):
        p, q = pts[i], pts[(i + 1) % 4]
        edges.append((q[0] - p[0], q[1] - p[1]))
    turns = set()
    for i in range(4):
        e, f = edges[i], edges[(i + 1) % 4]
        if e[0] * e[0] + e[1] * e[1] != 1:
            raise NotUnit(f"edge {i} squared length is not 1")
        if e[0] * f[0] + e[1] * f[1] != 0:
            raise NotUnit(f"edges {i} and {(i + 1) % 4} are not perpendicular")
        turns.add(e[0] * f[1] - e[1] * f[0])
    if len(turns) != 1:
        raise NotUnit("turns differ in sign")
    s = turns.pop()
    if s not in (1, -1):
        raise NotUnit("turn is not a unit")
    sgn = 1 if s > 0 else -1
    inner = []
    for i in range(4):
        p = pts[i]
        e = edges[i]
        # sgn * cross(e, x - p) >= 0, i.e. a*x + b*y + c >= 0
        a = -e[1] * sgn
        b = e[0] * sgn
        c = (e[1] * p[0] - e[0] * p[1]) * sgn
        inner.append((mpq(a), mpq(b), mpq(c)))
    t = (pts[0], pts[1], pts[2], pts[3])
    return SquareB(pts=t, inner=(inner[0], inner[1], inner[2], inner[3]), turn=sgn)


def clip(poly: list[Pt], h: Half) -> list[Pt]:
    """The polygon cut by the closed half-plane a*x + b*y + c >= 0."""
    a, b, c = h
    if not poly:
        return []
    vals = [a * p[0] + b * p[1] + c for p in poly]
    out: list[Pt] = []
    m = len(poly)
    for i in range(m):
        cur, vc = poly[i], vals[i]
        prv, vp = poly[i - 1], vals[i - 1]
        if (vp > 0 and vc < 0) or (vp < 0 and vc > 0):
            t = vp / (vp - vc)
            out.append((prv[0] + t * (cur[0] - prv[0]), prv[1] + t * (cur[1] - prv[1])))
        if vc >= 0:
            out.append(cur)
    return out


def area(poly: list[Pt]) -> mpq:
    """Absolute area by the shoelace formula."""
    s = mpq(0)
    m = len(poly)
    for i in range(m):
        p, q = poly[i], poly[(i + 1) % m]
        s += p[0] * q[1] - q[0] * p[1]
    return abs(s) / 2


def pair(a: SquareB, b: SquareB) -> tuple[str, mpq]:
    poly = list(a.pts)
    for h in b.inner:
        poly = clip(poly, h)
        if not poly:
            return ("apart", mpq(0))
    ar = area(poly)
    return ("contact" if ar == 0 else "overlap", ar)


def outer_walls(side: mpq) -> dict[str, Half]:
    z, one = mpq(0), mpq(1)
    return {
        "left": (-one, z, z),  # x <= 0
        "bottom": (z, -one, z),  # y <= 0
        "right": (one, z, -side),  # x >= side
        "top": (z, one, -side),  # y >= side
    }


def wall(a: SquareB, h: Half) -> tuple[str, mpq]:
    poly = clip(list(a.pts), h)
    if not poly:
        return ("clear", mpq(0))
    ar = area(poly)
    return ("contact" if ar == 0 else "outside", ar)


def inside(a: SquareB, side: mpq) -> bool:
    z, one = mpq(0), mpq(1)
    poly = list(a.pts)
    for h in ((one, z, z), (z, one, z), (-one, z, side), (z, -one, side)):
        poly = clip(poly, h)
        if not poly:
            return False
    return area(poly) == 1


def as_mpq(r: tuple[int, int]) -> mpq:
    return mpq(gmpy2.mpz(r[0]), gmpy2.mpz(r[1]))
