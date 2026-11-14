"""Lane L163 method B: exact convex clipping of corners in GMP rationals.

Each square is turned into its four corners from its centre and t = tan(theta/2),
with cos = (1 - t^2) / (1 + t^2) and sin = 2t / (1 + t^2), as
C + x (cos, sin) + y (-sin, cos) for (x, y) = (-1/2, -1/2), (1/2, -1/2), (1/2, 1/2),
(-1/2, 1/2), and from then on only the corners are used.

Four points are a unit square in cyclic order when all four sides have squared length
1 and both diagonals squared length 2. A pair is decided by clipping one square
against the four closed half-planes to the left of the other's directed edges
(Sutherland-Hodgman, keeping boundary points), which gives their intersection exactly:
empty is apart, non-empty with zero area is touching, positive area is overlapping.
A wall is classed the same way by clipping against the closed half-plane outside it,
and containment by the area of the intersection with the box, which is 1 exactly when
the square lies inside.
"""

from __future__ import annotations

from typing import Callable

import gmpy2
from gmpy2 import mpq

Point = tuple[mpq, mpq]
HALF = mpq(1, 2)


def corners(row: tuple[int, int, int, int, int, int]) -> list[Point]:
    xn, xd, yn, yd, tn, td = row
    cx, cy, t = mpq(xn, xd), mpq(yn, yd), mpq(tn, td)
    one_t2 = 1 + t * t
    c = (1 - t * t) / one_t2
    s = 2 * t / one_t2
    out: list[Point] = []
    for x, y in ((-HALF, -HALF), (HALF, -HALF), (HALF, HALF), (-HALF, HALF)):
        out.append((cx + x * c - y * s, cy + x * s + y * c))
    return out


def _d2(p: Point, q: Point) -> mpq:
    dx, dy = p[0] - q[0], p[1] - q[1]
    return dx * dx + dy * dy


def is_unit_square(pts: list[Point]) -> bool:
    if len(pts) != 4:
        return False
    sides = all(_d2(pts[k], pts[(k + 1) % 4]) == 1 for k in range(4))
    return sides and _d2(pts[0], pts[2]) == 2 and _d2(pts[1], pts[3]) == 2


def twice_signed_area(pts: list[Point]) -> mpq:
    acc = mpq(0)
    m = len(pts)
    for k in range(m):
        x0, y0 = pts[k]
        x1, y1 = pts[(k + 1) % m]
        acc += x0 * y1 - x1 * y0
    return acc


def area(pts: list[Point]) -> mpq:
    return abs(twice_signed_area(pts)) / 2 if len(pts) >= 3 else mpq(0)


def clip(poly: list[Point], side: Callable[[Point], mpq]) -> list[Point]:
    """Keep the part of `poly` where side(p) >= 0, boundary included; side is affine."""
    out: list[Point] = []
    m = len(poly)
    if m == 0:
        return out
    for k in range(m):
        cur = poly[k]
        prev = poly[k - 1]
        fc, fp = side(cur), side(prev)
        if fc >= 0:
            if fp < 0 and fc > 0:
                out.append(_cross(prev, cur, fp, fc))
            # fc == 0 and fp < 0: cur itself is the crossing point
            out.append(cur)
        elif fp >= 0:
            if fp > 0:
                out.append(_cross(prev, cur, fp, fc))
            # fp == 0: prev is already kept and is the crossing point
    return out


def _cross(p: Point, q: Point, fp: mpq, fq: mpq) -> Point:
    lam = fp / (fp - fq)
    return (p[0] + lam * (q[0] - p[0]), p[1] + lam * (q[1] - p[1]))


def _edge_fn(a: Point, b: Point) -> Callable[[Point], mpq]:
    ex, ey = b[0] - a[0], b[1] - a[1]
    ax, ay = a

    def f(p: Point) -> mpq:
        return ex * (p[1] - ay) - ey * (p[0] - ax)

    return f


def intersect(pi: list[Point], pj: list[Point]) -> list[Point]:
    """The intersection of convex polygon pj with counterclockwise convex polygon pi."""
    poly = list(pj)
    m = len(pi)
    for k in range(m):
        poly = clip(poly, _edge_fn(pi[k], pi[(k + 1) % m]))
        if not poly:
            break
    return poly


def pair_class(pi: list[Point], pj: list[Point]) -> tuple[str, mpq]:
    """'apart', 'touch' or 'overlap', with the overlap area."""
    inter = intersect(pi, pj)
    if not inter:
        return "apart", mpq(0)
    a = area(inter)
    return ("touch" if a == 0 else "overlap"), a


def wall_classes(pts: list[Point], side: mpq) -> tuple[list[str], mpq]:
    """Classes against the left, bottom, right and top walls, and the area inside the box."""
    outside: list[Callable[[Point], mpq]] = [
        lambda p: -p[0],
        lambda p: -p[1],
        lambda p: p[0] - side,
        lambda p: p[1] - side,
    ]
    classes: list[str] = []
    for f in outside:
        part = clip(pts, f)
        if not part:
            classes.append("apart")
        else:
            classes.append("contact" if area(part) == 0 else "crossing")
    inside = pts
    for f in outside:
        inside = clip(inside, lambda p, f=f: -f(p))
    return classes, area(inside)


def versions() -> dict[str, str]:
    return {"gmpy2": str(gmpy2.version()), "gmp": str(gmpy2.mp_version())}
