"""Lane L180 method A: separating axes in Python integers, from centres and edge directions.

Written for the blind stage 4 review of issue #996 as a clean-room implementation.
It imports nothing from this repository or the source, and reuses no code of any
earlier review. It reads the JSON form only: centre (x, y) and unit edge direction
(c, s) of each square, never corners.

Each square is put over two integer denominators of its own: the centre as (X, Y)/E
and the direction as (a, b)/r. It is a unit square exactly when r > 0 and
a^2 + b^2 = r^2. With u = (a, b)/r and v = (-b, a)/r, the square is
{C + p u + q v : |p|, |q| <= 1/2}.

For a pair (i, j), on each of the four unit normals u_i, v_i, u_j, v_j, square i
projects to an interval of half-length 1/2 about its centre and square j to one of
half-length (|cos D| + |sin D|)/2, D the angle between them: the same on all four. The
gap on a normal w is |d . w| - 1/2 - (|cos D| + |sin D|)/2 with d = C_j - C_i, an exact
distance along w. The four gaps share the denominator 2 E_i E_j r_i r_j, so their
maximum, the margin, is decided on integer numerators: positive is apart, zero is
contact with disjoint interiors, negative is overlap (two convex polygons with disjoint
interiors are weakly separated by a line parallel to an edge of one of them).

A wall's clearance is the signed distance from the square's extreme corner to it, from
the half-extent (|a| + |b|)/(2r), the same in x and in y.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import lcm

APART, TOUCH, OVERLAP = "apart", "touch", "overlap"
INSIDE, CROSS = "inside", "cross"
WALLS = ("left", "bottom", "right", "top")


@dataclass(frozen=True)
class IntSquare:
    X: int
    Y: int
    E: int
    a: int
    b: int
    r: int


def to_ints(x: Fraction, y: Fraction, c: Fraction, s: Fraction) -> IntSquare:
    E = lcm(x.denominator, y.denominator)
    r = lcm(c.denominator, s.denominator)
    return IntSquare(
        X=x.numerator * (E // x.denominator),
        Y=y.numerator * (E // y.denominator),
        E=E,
        a=c.numerator * (r // c.denominator),
        b=s.numerator * (r // s.denominator),
        r=r,
    )


def is_unit(q: IntSquare) -> bool:
    return q.r > 0 and q.a * q.a + q.b * q.b == q.r * q.r


def pair_gaps(p: IntSquare, q: IntSquare) -> tuple[list[int], int]:
    """The four gap numerators (on u_p, v_p, u_q, v_q) and their common denominator."""
    dX = q.X * p.E - p.X * q.E
    dY = q.Y * p.E - p.Y * q.E
    EE = p.E * q.E
    rr = p.r * q.r
    cosn = p.a * q.a + p.b * q.b
    sinn = p.a * q.b - p.b * q.a
    base = EE * rr + EE * (abs(cosn) + abs(sinn))
    gaps = [
        2 * q.r * abs(dX * p.a + dY * p.b) - base,
        2 * q.r * abs(dY * p.a - dX * p.b) - base,
        2 * p.r * abs(dX * q.a + dY * q.b) - base,
        2 * p.r * abs(dY * q.a - dX * q.b) - base,
    ]
    return gaps, 2 * EE * rr


def pair_margin(p: IntSquare, q: IntSquare) -> tuple[Fraction, int]:
    """The exact margin and the number of normals on which it is attained."""
    gaps, den = pair_gaps(p, q)
    top = max(gaps)
    return Fraction(top, den), sum(1 for g in gaps if g == top)


def pair_class(m: Fraction) -> str:
    return APART if m > 0 else TOUCH if m == 0 else OVERLAP


def wall_clearances(q: IntSquare, side: Fraction) -> dict[str, Fraction]:
    """Signed clearances to the left, bottom, right and top walls of [0, side]^2."""
    P, Q = side.numerator, side.denominator
    ext = q.E * (abs(q.a) + abs(q.b))
    den_lo = 2 * q.E * q.r
    den_hi = 2 * Q * q.E * q.r
    return {
        "left": Fraction(2 * q.r * q.X - ext, den_lo),
        "bottom": Fraction(2 * q.r * q.Y - ext, den_lo),
        "right": Fraction(2 * P * q.E * q.r - 2 * Q * q.r * q.X - Q * ext, den_hi),
        "top": Fraction(2 * P * q.E * q.r - 2 * Q * q.r * q.Y - Q * ext, den_hi),
    }


def wall_class(c: Fraction) -> str:
    return INSIDE if c > 0 else TOUCH if c == 0 else CROSS
