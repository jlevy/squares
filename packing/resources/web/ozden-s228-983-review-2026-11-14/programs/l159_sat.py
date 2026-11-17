"""Lane L159's method A: separating axes in Python integers.

Clean-room code written for the stage 4 review of issue #983. It imports nothing from
this repository or from the source, and reuses no code of any earlier review.

A square's eight coordinates are written over their least common denominator D as
integer points A_k = D * P_k. It is a unit square, listed in cyclic order, exactly when
U = A_1 - A_0 has U.U = D^2, W = A_3 - A_0 is U turned a quarter either way, and
A_2 = A_0 + U + W. Its edge normals are then the exact rational unit vectors U/D and
W/D, and its own projection on each is an interval of length 1.

A pair's margin is the largest gap between the two projections over the four normals
of the two squares, kept as an exact fraction (numerator, positive denominator). Two
convex polygons with disjoint interiors are weakly separated by a line parallel to an
edge of one of them, so the margin is positive when the squares are apart, zero when
they touch with disjoint interiors, and negative when their interiors meet.

A wall clearance is the least signed distance of a corner from the wall, positive
inside the box [0, S]^2.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import lcm

Rational = tuple[int, int]
Point = tuple[Rational, Rational]


@dataclass(frozen=True, slots=True)
class SquareA:
    """A unit square accepted by method A, in integers over its own denominator."""

    D: int
    A: tuple[tuple[int, int], ...]
    U: tuple[int, int]
    W: tuple[int, int]
    sense: int


def prepare(corners: tuple[Point, ...]) -> SquareA | None:
    """Return the square in integers, or None when the corners are not a unit square."""
    d = 1
    for (_, xq), (_, yq) in corners:
        d = lcm(d, xq, yq)
    pts = tuple((xp * (d // xq), yp * (d // yq)) for (xp, xq), (yp, yq) in corners)
    u = (pts[1][0] - pts[0][0], pts[1][1] - pts[0][1])
    w = (pts[3][0] - pts[0][0], pts[3][1] - pts[0][1])
    if u[0] * u[0] + u[1] * u[1] != d * d:
        return None
    if w == (-u[1], u[0]):
        sense = 1
    elif w == (u[1], -u[0]):
        sense = -1
    else:
        return None
    if pts[2] != (pts[0][0] + u[0] + w[0], pts[0][1] + u[1] + w[1]):
        return None
    return SquareA(D=d, A=pts, U=u, W=w, sense=sense)


def _gap_on(own: SquareA, normal: tuple[int, int], other: SquareA) -> tuple[int, int]:
    """The projection gap on own's normal, as (numerator, denominator D_o^2 D_t)."""
    do, dt = own.D, other.D
    lo_own = (normal[0] * own.A[0][0] + normal[1] * own.A[0][1]) * dt
    hi_own = lo_own + do * do * dt
    proj = [(normal[0] * x + normal[1] * y) * do for x, y in other.A]
    lo_other, hi_other = min(proj), max(proj)
    return max(lo_other - hi_own, lo_own - hi_other), do * do * dt


def margin(a: SquareA, b: SquareA) -> tuple[int, int]:
    """The exact pair margin as (numerator, positive denominator)."""
    best = _gap_on(a, a.U, b)
    for own, normal, other in ((a, a.W, b), (b, b.U, a), (b, b.W, a)):
        g, d = _gap_on(own, normal, other)
        if g * best[1] > best[0] * d:
            best = (g, d)
    return best


def margin_class(numerator: int) -> str:
    """Apart, contact (disjoint interiors) or overlap, from the margin's sign."""
    if numerator > 0:
        return "apart"
    if numerator == 0:
        return "contact"
    return "overlap"


def margin_fraction(m: tuple[int, int]) -> Fraction:
    """The margin as a reduced fraction."""
    return Fraction(m[0], m[1])


def clearances(sq: SquareA, side: Rational) -> list[Fraction]:
    """Signed clearances from the left, bottom, right and top walls of [0, S]^2."""
    sp, sq_ = side
    xs = [x for x, _ in sq.A]
    ys = [y for _, y in sq.A]
    d = sq.D
    return [
        Fraction(min(xs), d),
        Fraction(min(ys), d),
        Fraction(sp * d - sq_ * max(xs), sq_ * d),
        Fraction(sp * d - sq_ * max(ys), sq_ * d),
    ]


def clearance_class(value: Fraction) -> str:
    """Inside with room, at the wall, or across it."""
    if value > 0:
        return "apart"
    if value == 0:
        return "contact"
    return "cross"
