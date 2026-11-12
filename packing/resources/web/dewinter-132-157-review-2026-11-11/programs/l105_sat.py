"""Lane L105's method A: separating axes in `fractions.Fraction`.

A square is (x, y, c, s): centre (x, y) and the unit direction u = (c, s) of one
edge; the other edge direction is v = (-s, c). It is a unit square exactly when
c*c + s*s == 1, and then u and v are exact rational unit vectors.

- Half-extent of a square along a unit axis a: h(a) = (|a.u| + |a.v|) / 2.
- Wall clearances: left x - h, bottom y - h, right L - x - h, top L - y - h,
  with h = (|c| + |s|) / 2 the half-extent along either coordinate axis.
- Pair margin: the largest of |a.d| - h_i(a) - h_j(a) over the four edge
  normals a in {u_i, v_i, u_j, v_j}, d = centre_j - centre_i. Positive: the
  closed squares are apart; zero: they touch with disjoint interiors; negative:
  their interiors meet (the separating axis theorem for convex polygons, whose
  Minkowski difference has edges parallel to theirs).

Written for this review alone; it imports nothing from this repository or the
source, and shares nothing with method B but the integers the reader hands it.
"""

from __future__ import annotations

from fractions import Fraction

Rat = tuple[int, int]
HALF = Fraction(1, 2)


def frac(r: Rat) -> Fraction:
    return Fraction(r[0], r[1])


class SquareA:
    __slots__ = ("x", "y", "c", "s", "unit", "h")

    def __init__(self, x: Fraction, y: Fraction, c: Fraction, s: Fraction) -> None:
        self.x, self.y, self.c, self.s = x, y, c, s
        self.unit = c * c + s * s == 1
        self.h = (abs(c) + abs(s)) / 2


def build(sq: tuple[Rat, Rat, Rat, Rat]) -> SquareA:
    return SquareA(frac(sq[0]), frac(sq[1]), frac(sq[2]), frac(sq[3]))


def clearances(q: SquareA, side: Fraction) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    """(left, bottom, right, top) clearances, exact."""
    return (q.x - q.h, q.y - q.h, side - q.x - q.h, side - q.y - q.h)


def _half(q: SquareA, ax: Fraction, ay: Fraction) -> Fraction:
    return (abs(ax * q.c + ay * q.s) + abs(-ax * q.s + ay * q.c)) / 2


def margin(a: SquareA, b: SquareA) -> tuple[Fraction, int]:
    """(margin, index of the binding axis: 0 u_a, 1 v_a, 2 u_b, 3 v_b)."""
    dx, dy = b.x - a.x, b.y - a.y
    axes = ((a.c, a.s), (-a.s, a.c), (b.c, b.s), (-b.s, b.c))
    best: Fraction | None = None
    arg = -1
    for k, (ax, ay) in enumerate(axes):
        g = abs(ax * dx + ay * dy) - _half(a, ax, ay) - _half(b, ax, ay)
        if best is None or g > best:
            best, arg = g, k
    assert best is not None
    return best, arg


def classify(m: Fraction) -> str:
    if m > 0:
        return "apart"
    if m == 0:
        return "contact"
    return "overlap"


def wall_class(c: Fraction) -> str:
    if c > 0:
        return "inside"
    if c == 0:
        return "contact"
    return "outside"
