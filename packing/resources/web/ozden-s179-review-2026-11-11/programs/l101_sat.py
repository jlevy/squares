"""Method A: separating axes in exact rationals (Python's fractions.Fraction).

A square is accepted when u = p1 - p0 has u.u = 1, p3 - p0 = +/- perp(u) and
p2 = p0 + u + (p3 - p0). Its edge normals u and perp(u) are then exact rational unit
vectors, so projections onto them are exact distances.

A pair's margin is the largest projection gap over the four edge normals of the two
squares. For convex polygons it is positive exactly when the closed squares are apart,
zero exactly when they touch with disjoint interiors, and negative exactly when the
interiors meet. A wall clearance is the least corner coordinate's distance to the wall.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

WALLS = ("left", "bottom", "right", "top")


@dataclass(frozen=True)
class SquareA:
    corners: tuple[tuple[Fraction, Fraction], ...]
    axes: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]
    sense: int  # +1 counterclockwise, -1 clockwise


def make_square(points: list[tuple[tuple[int, int], tuple[int, int]]]) -> SquareA | str:
    """The square, or the reason it is not a unit square."""
    p = tuple((Fraction(*x), Fraction(*y)) for x, y in points)
    u = (p[1][0] - p[0][0], p[1][1] - p[0][1])
    if u[0] * u[0] + u[1] * u[1] != 1:
        return "first edge is not of length 1"
    v = (p[3][0] - p[0][0], p[3][1] - p[0][1])
    perp = (-u[1], u[0])
    if v == perp:
        sense = 1
    elif v == (-perp[0], -perp[1]):
        sense = -1
    else:
        return "last edge is not the first turned by a right angle"
    if p[2] != (p[0][0] + u[0] + v[0], p[0][1] + u[1] + v[1]):
        return "third corner is not p0 + u + v"
    return SquareA(corners=p, axes=(u, perp), sense=sense)


def _interval(sq: SquareA, axis: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
    values = [x * axis[0] + y * axis[1] for x, y in sq.corners]
    return min(values), max(values)


def pair_margin(a: SquareA, b: SquareA) -> Fraction:
    best: Fraction | None = None
    for axis in (*a.axes, *b.axes):
        lo_a, hi_a = _interval(a, axis)
        lo_b, hi_b = _interval(b, axis)
        gap = max(lo_b - hi_a, lo_a - hi_b)
        if best is None or gap > best:
            best = gap
    assert best is not None
    return best


def wall_clearances(sq: SquareA, side: Fraction) -> dict[str, Fraction]:
    xs = [x for x, _ in sq.corners]
    ys = [y for _, y in sq.corners]
    return {
        "left": min(xs),
        "bottom": min(ys),
        "right": side - max(xs),
        "top": side - max(ys),
    }


def classify(value: Fraction) -> str:
    """Three-way class of a margin or clearance."""
    if value > 0:
        return "clear"
    if value == 0:
        return "contact"
    return "overlap"


def wall_class(value: Fraction) -> str:
    if value > 0:
        return "clear"
    if value == 0:
        return "contact"
    return "outside"
