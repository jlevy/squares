"""Method A for lane L64: unit squares, walls and pairs by separating axes, in Fraction.

Written clean room on 2026-11-09 from the definitions alone (see the review's "The Claim
and What It Needs"). It shares only the reader with method B (`l64_clip.py`).

A square is four corners p0, p1, p2, p3 in cyclic order. It is a unit square exactly
when u = p1 - p0 has u.u = 1, f = p3 - p0 is u turned by a right angle either way, and
p2 = p0 + u + f. Its two edge directions u and w = (-u_y, u_x) are then exact rational
unit vectors, so every separation measured along them is an exact rational length.

A closed convex polygon lies in [0, S]^2 exactly when its corners do. Two convex
polygons have disjoint interiors exactly when, along one of their edge normals, their
projections overlap in at most a point; for two squares those normals are the four axes
u_i, w_i, u_j, w_j. The pair margin is the largest gap over those four axes: positive
means apart, zero touching, negative overlapping.
"""

from __future__ import annotations

from fractions import Fraction as F

Point = tuple[F, F]


class ShapeError(Exception):
    pass


class SquareA:
    __slots__ = ("id", "p", "u", "w", "orient")

    def __init__(
        self, sid: int, corners: list[tuple[int, int, int, int]], unit: bool = True
    ) -> None:
        self.id = sid
        self.p: list[Point] = [(F(xn, xd), F(yn, yd)) for (xn, xd, yn, yd) in corners]
        self.u, self.w, self.orient = shape(self.p, unit)


def shape(p: list[Point], unit: bool = True) -> tuple[Point, Point, int]:
    """Decide that p0..p3 are a unit square in cyclic order; return u, w and the sense.

    With unit=False it decides only that they are a square of some positive side (used by
    the controls that enlarge one square); its axes are then not unit vectors, which
    scales every gap along them but keeps every sign, so classes stay exact.
    """
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p
    ux, uy = x1 - x0, y1 - y0
    fx, fy = x3 - x0, y3 - y0
    if unit and ux * ux + uy * uy != 1:
        raise ShapeError("edge p0p1 is not of length 1")
    if ux == 0 and uy == 0:
        raise ShapeError("edge p0p1 has length 0")
    if (fx, fy) == (-uy, ux):
        orient = 1
    elif (fx, fy) == (uy, -ux):
        orient = -1
    else:
        raise ShapeError("edge p0p3 is not edge p0p1 turned by a right angle")
    if (x2, y2) != (x0 + ux + fx, y0 + uy + fy):
        raise ShapeError("p2 is not p0 + (p1 - p0) + (p3 - p0)")
    return (ux, uy), (-uy, ux), orient


def wall_clearances(sq: SquareA, side: F) -> dict[str, F]:
    """Exact clearance to each wall: least corner x, y, and side minus largest x, y."""
    xs = [x for x, _ in sq.p]
    ys = [y for _, y in sq.p]
    return {
        "left": min(xs),
        "bottom": min(ys),
        "right": side - max(xs),
        "top": side - max(ys),
    }


def _interval(p: list[Point], ax: Point) -> tuple[F, F]:
    vals = [x * ax[0] + y * ax[1] for x, y in p]
    return min(vals), max(vals)


def pair_margin(a: SquareA, b: SquareA) -> tuple[F, int]:
    """Largest gap over the four edge axes, and the axis (0..3: a.u, a.w, b.u, b.w)."""
    best: F | None = None
    which = -1
    for k, ax in enumerate((a.u, a.w, b.u, b.w)):
        lo_a, hi_a = _interval(a.p, ax)
        lo_b, hi_b = _interval(b.p, ax)
        gap = max(lo_b - hi_a, lo_a - hi_b)
        if best is None or gap > best:
            best, which = gap, k
    assert best is not None
    return best, which


def classify(margin: F) -> str:
    if margin > 0:
        return "separated"
    if margin == 0:
        return "touching"
    return "overlapping"


def _seg_dist2(v: Point, a: Point, b: Point) -> F:
    """Squared distance from v to the unit segment ab (|b - a| = 1 exactly)."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    vx, vy = v[0] - a[0], v[1] - a[1]
    t = vx * dx + vy * dy
    if t <= 0:
        return vx * vx + vy * vy
    if t >= 1:
        wx, wy = v[0] - b[0], v[1] - b[1]
        return wx * wx + wy * wy
    cross = dx * vy - dy * vx
    return cross * cross


def distance2(a: SquareA, b: SquareA) -> F:
    """Exact squared Euclidean distance between two closed squares with disjoint interiors.

    For disjoint convex polygons the least distance is attained between a corner of one
    and an edge of the other; touching squares give 0.
    """
    best: F | None = None
    for s, t in ((a, b), (b, a)):
        for v in s.p:
            for k in range(4):
                d2 = _seg_dist2(v, t.p[k], t.p[(k + 1) % 4])
                if best is None or d2 < best:
                    best = d2
    assert best is not None
    return best
