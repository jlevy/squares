"""Lane L169 method B: exact convex clipping of the squares' corners in GMP rationals.

Each square becomes its four corners C - u/2 - v/2, C + u/2 - v/2, C + u/2 + v/2,
C - u/2 + v/2, with cos(theta) = (1 - t^2) / (1 + t^2) and sin(theta) = 2t / (1 + t^2)
computed in gmpy2.mpq; from then on only the corners are used.

Four points are a unit square in cyclic order when the four sides have squared length 1
and both diagonals squared length 2 (the converse of Pythagoras puts right angles at the
second and fourth corners, which are then the two points at distance 1 from the first
and the third). The listing must be counterclockwise: twice the shoelace sum is +2.

A pair is decided by clipping one square against the four closed half-planes to the left
of the other's directed edges (Sutherland-Hodgman, keeping boundary points), which leaves
the intersection exactly. Empty is apart; non-empty with zero area is contact (the
interior of an intersection of convex sets is the intersection of their interiors);
positive area is overlap, by that area. A wall is classed the same way, by clipping the
square against the closed half-plane outside it. Containment is separate: a unit square
lies in the box exactly when its intersection with the box has area exactly 1.
"""

from __future__ import annotations

import gmpy2
from gmpy2 import mpq

Point = tuple[object, object]

HALF = mpq(1, 2)


def corners(x: tuple[int, int], y: tuple[int, int], t: tuple[int, int]) -> list[Point]:
    cx, cy, tt = mpq(*x), mpq(*y), mpq(*t)
    den = 1 + tt * tt
    c = (1 - tt * tt) / den
    s = 2 * tt / den
    ux, uy = c * HALF, s * HALF
    vx, vy = -s * HALF, c * HALF
    return [
        (cx - ux - vx, cy - uy - vy),
        (cx + ux - vx, cy + uy - vy),
        (cx + ux + vx, cy + uy + vy),
        (cx - ux + vx, cy - uy + vy),
    ]


def _d2(p: Point, q: Point):
    dx = p[0] - q[0]
    dy = p[1] - q[1]
    return dx * dx + dy * dy


def twice_area(poly: list[Point]):
    s = mpq(0)
    n = len(poly)
    for k in range(n):
        x1, y1 = poly[k]
        x2, y2 = poly[(k + 1) % n]
        s += x1 * y2 - x2 * y1
    return s


def is_unit_ccw(c: list[Point]) -> tuple[bool, bool]:
    """(the four points are a unit square in cyclic order, listed counterclockwise)."""
    unit = (
        len(c) == 4
        and all(_d2(c[k], c[(k + 1) % 4]) == 1 for k in range(4))
        and _d2(c[0], c[2]) == 2
        and _d2(c[1], c[3]) == 2
    )
    return unit, twice_area(c) == 2


def clip(poly: list[Point], a, b, c, closed: bool = True) -> list[Point]:
    """poly intersected with {a x + b y + c >= 0} (closed) or {> 0} (open, for the
    self-test's broken copy only)."""
    out: list[Point] = []
    n = len(poly)
    if n == 0:
        return out

    def inside(f) -> bool:
        return f >= 0 if closed else f > 0

    for k in range(n):
        p = poly[k]
        q = poly[(k + 1) % n]
        fp = a * p[0] + b * p[1] + c
        fq = a * q[0] + b * q[1] + c
        ip, iq = inside(fp), inside(fq)
        if ip and iq:
            out.append(q)
        elif ip and not iq:
            lam = fp / (fp - fq)
            out.append((p[0] + lam * (q[0] - p[0]), p[1] + lam * (q[1] - p[1])))
        elif not ip and iq:
            lam = fp / (fp - fq)
            out.append((p[0] + lam * (q[0] - p[0]), p[1] + lam * (q[1] - p[1])))
            out.append(q)
    return out


def intersect(ci: list[Point], cj: list[Point], closed: bool = True) -> list[Point]:
    """cj clipped by the half-planes to the left of ci's directed edges."""
    poly = list(cj)
    for k in range(4):
        p = ci[k]
        q = ci[(k + 1) % 4]
        ex, ey = q[0] - p[0], q[1] - p[1]
        # left of p->q: ex (Y - py) - ey (X - px) >= 0
        poly = clip(poly, -ey, ex, ey * p[0] - ex * p[1], closed)
        if not poly:
            break
    return poly


def pair_class(ci: list[Point], cj: list[Point], closed: bool = True) -> tuple[str, object]:
    poly = intersect(ci, cj, closed)
    if not poly:
        return "apart", mpq(0)
    area = abs(twice_area(poly)) / 2
    return ("contact" if area == 0 else "overlap"), area


_OUTSIDE = {
    # wall: (a, b, c) of the closed half-plane a x + b y + c >= 0 outside the wall,
    # as a function of the side S
    "left": lambda s: (mpq(-1), mpq(0), mpq(0)),
    "right": lambda s: (mpq(1), mpq(0), -s),
    "bottom": lambda s: (mpq(0), mpq(-1), mpq(0)),
    "top": lambda s: (mpq(0), mpq(1), -s),
}


def wall_class(c: list[Point], wall: str, side: tuple[int, int], closed: bool = True):
    s = mpq(*side)
    a, b, cc = _OUTSIDE[wall](s)
    poly = clip(list(c), a, b, cc, closed)
    if not poly:
        return "clear", mpq(0)
    area = abs(twice_area(poly)) / 2
    return ("contact" if area == 0 else "crossing"), area


def area_in_box(c: list[Point], side: tuple[int, int]):
    s = mpq(*side)
    poly = list(c)
    for a, b, cc in ((1, 0, 0), (-1, 0, s), (0, 1, 0), (0, -1, s)):
        poly = clip(poly, mpq(a), mpq(b), mpq(cc))
        if not poly:
            return mpq(0)
    return abs(twice_area(poly)) / 2


def gmp_version() -> str:
    return f"gmpy2 {gmpy2.version()}, {gmpy2.mp_version()}"
