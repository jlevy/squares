"""Method A: unit squares, wall clearances and pair margins by separating axes.

Lane L108, blind stage 4 review of jlevy/squares#959. Arithmetic: GMP rationals through
gmpy2.mpq. Input: the integers the reader hands over. Shares nothing with method B.

A listed square p0 p1 p2 p3 is a unit square when u = p1 - p0 has u.u = 1, the vector
w = p3 - p0 is u turned a quarter either way, and p2 = p0 + u + w. Its edge normals are
then u and w, exact rational unit vectors, so a projection gap along them is a true
distance. A pair's margin is the largest projection gap over the four normals of the
two squares: positive means the closed squares are apart, zero that they touch with
disjoint interiors, negative that their interiors meet (two convex polygons with
disjoint interiors are weakly separated by a line parallel to one of their edges).
"""

from __future__ import annotations

from dataclasses import dataclass

from gmpy2 import mpq

QPoint = tuple[mpq, mpq]


@dataclass(frozen=True)
class SquareA:
    corners: tuple[QPoint, QPoint, QPoint, QPoint]
    axes: tuple[QPoint, QPoint]
    own: tuple[tuple[mpq, mpq], tuple[mpq, mpq]]  # own projection interval on each axis
    turn: int  # +1 when w is u turned counterclockwise, -1 when clockwise


def _q(r: tuple[int, int]) -> mpq:
    return mpq(r[0], r[1])


def _dot(a: QPoint, b: QPoint) -> mpq:
    return a[0] * b[0] + a[1] * b[1]


def _project(corners: tuple[QPoint, ...], axis: QPoint) -> tuple[mpq, mpq]:
    values = [_dot(axis, c) for c in corners]
    return (min(values), max(values))


def build(raw: tuple[tuple[tuple[int, int], tuple[int, int]], ...]) -> SquareA | None:
    """The square from four integer corners, or None when it is not a unit square."""
    c = tuple((_q(x), _q(y)) for x, y in raw)
    p0, p1, p2, p3 = c
    u = (p1[0] - p0[0], p1[1] - p0[1])
    w = (p3[0] - p0[0], p3[1] - p0[1])
    if _dot(u, u) != 1:
        return None
    if w == (-u[1], u[0]):
        turn = 1
    elif w == (u[1], -u[0]):
        turn = -1
    else:
        return None
    if p2 != (p0[0] + u[0] + w[0], p0[1] + u[1] + w[1]):
        return None
    corners = (p0, p1, p2, p3)
    return SquareA(corners=corners, axes=(u, w), own=(_project(corners, u), _project(corners, w)), turn=turn)


def margin(a: SquareA, b: SquareA) -> mpq:
    """The largest projection gap over the four edge normals of the pair."""
    best: mpq | None = None
    for sq, other in ((a, b), (b, a)):
        for axis, (lo, hi) in zip(sq.axes, sq.own, strict=True):
            olo, ohi = _project(other.corners, axis)
            gap = max(olo - hi, lo - ohi)
            if best is None or gap > best:
                best = gap
    assert best is not None
    return best


def walls(sq: SquareA, side: mpq) -> dict[str, mpq]:
    """Each wall's clearance: the least distance from a corner to that wall, signed."""
    xs = [c[0] for c in sq.corners]
    ys = [c[1] for c in sq.corners]
    return {"left": min(xs), "bottom": min(ys), "right": side - max(xs), "top": side - max(ys)}


def classify(value: mpq) -> str:
    if value > 0:
        return "clear"
    if value == 0:
        return "contact"
    return "overlap"


def side_q(side: tuple[int, int]) -> mpq:
    return _q(side)
