"""Method A: separating axes on centres and unit bases, in Python integers.

A square is its centre c and its basis u = (a, b), with v = (-b, a): the set
{c + s u + t v : |s| <= 1/2, |t| <= 1/2}. Each square's four scalars are written over
their least common denominator D, so c = (X, Y)/D and u = (A, B)/D with integers.

- Unit square: A^2 + B^2 = D^2 exactly, so u and v are unit vectors and the set is a unit
  square.
- Pair margin: on each of the four normals u_i, v_i, u_j, v_j (all exactly unit), the
  separation of the two projections is |d . w| - h_i(w) - h_j(w), with d the centre
  difference and h_k(w) = (|u_k . w| + |v_k . w|)/2 the half-width of square k on w.
  The margin is the greatest of the four, an exact fraction with a positive integer
  denominator: positive is apart, zero is contact with disjoint interiors, negative is
  overlap. Two convex polygons have disjoint interiors exactly when a line parallel to an
  edge of one of them weakly separates them, so the three signs are exactly those classes.
- Wall clearance: the signed distance from the square's extreme point to the wall, its
  half-width on an axis being (|a| + |b|)/2.

This module imports nothing outside the standard library and shares nothing with method B
but the reader's output.
"""

from __future__ import annotations

from fractions import Fraction
from math import lcm
from typing import NamedTuple


class IntSquare(NamedTuple):
    """A square's centre (X, Y)/D and basis (A, B)/D over one positive denominator."""

    X: int
    Y: int
    A: int
    B: int
    D: int


Ratio = tuple[int, int]  # numerator, positive denominator


def integer_square(cx: Fraction, cy: Fraction, a: Fraction, b: Fraction) -> IntSquare:
    """Write one square over the least common denominator of its four scalars."""
    d = lcm(cx.denominator, cy.denominator, a.denominator, b.denominator)
    return IntSquare(
        cx.numerator * (d // cx.denominator),
        cy.numerator * (d // cy.denominator),
        a.numerator * (d // a.denominator),
        b.numerator * (d // b.denominator),
        d,
    )


def is_unit(square: IntSquare) -> bool:
    """Whether the basis is exactly a unit vector."""
    return square.A * square.A + square.B * square.B == square.D * square.D


def greater(left: Ratio, right: Ratio) -> bool:
    """left > right for two ratios with positive denominators."""
    return left[0] * right[1] > right[0] * left[1]


def margin(si: IntSquare, sj: IntSquare) -> Ratio:
    """The greatest separation over the four normals, as (numerator, denominator)."""
    ex = sj.X * si.D - si.X * sj.D
    ey = sj.Y * si.D - si.Y * sj.D
    dot = si.A * sj.A + si.B * sj.B
    cross = si.A * sj.B - si.B * sj.A
    spread = abs(dot) + abs(cross)
    # The normals of square i, over 2 D_i^2 D_j.
    den_i = 2 * si.D * si.D * sj.D
    base_i = si.D * si.D * sj.D + si.D * spread
    on_ui = 2 * abs(ex * si.A + ey * si.B) - base_i
    on_vi = 2 * abs(ey * si.A - ex * si.B) - base_i
    # The normals of square j, over 2 D_j^2 D_i.
    den_j = 2 * sj.D * sj.D * si.D
    base_j = sj.D * sj.D * si.D + sj.D * spread
    on_uj = 2 * abs(ex * sj.A + ey * sj.B) - base_j
    on_vj = 2 * abs(ey * sj.A - ex * sj.B) - base_j
    best: Ratio = (max(on_ui, on_vi), den_i)
    other: Ratio = (max(on_uj, on_vj), den_j)
    if greater(other, best):
        best = other
    return best


def clearances(square: IntSquare, side: Fraction) -> tuple[Ratio, Ratio, Ratio, Ratio]:
    """Signed clearances to the left, bottom, right and top walls of [0, side]^2."""
    width = abs(square.A) + abs(square.B)  # over 2D, twice the half-width
    den = 2 * square.D
    left = (2 * square.X - width, den)
    bottom = (2 * square.Y - width, den)
    sn, sd = side.numerator, side.denominator
    den_far = 2 * square.D * sd
    right = (2 * sn * square.D - sd * (2 * square.X + width), den_far)
    top = (2 * sn * square.D - sd * (2 * square.Y + width), den_far)
    return left, bottom, right, top


def sign(value: Ratio) -> int:
    """The sign of a ratio with a positive denominator."""
    return (value[0] > 0) - (value[0] < 0)


def as_fraction(value: Ratio) -> Fraction:
    """The ratio as a reduced fraction, for reporting and for the controls' rules."""
    return Fraction(value[0], value[1])
