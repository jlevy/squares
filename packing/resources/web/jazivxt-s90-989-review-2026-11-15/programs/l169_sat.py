"""Lane L169 method A: separating axes in Python integers, from centres and half-angles.

Square k has centre (X_k, Y_k) / E_k over one denominator, and from t_k = p/q the edge
direction u_k = (a_k, b_k) / r_k with a = q^2 - p^2, b = 2pq, r = p^2 + q^2, and normal
v_k = (-b_k, a_k) / r_k. The square is {C + x u + y v : |x|, |y| <= 1/2}; it is accepted
as a unit square when a^2 + b^2 = r^2 and r > 0.

On a unit normal n of square i, square i projects to an interval of half-length 1/2 and
square j to one of half-length (|cos D| + |sin D|) / 2, D the angle between them; the
same holds on a normal of j with the roles exchanged. The gap on n is |n . (C_j - C_i)|
less both half-lengths, an exact signed distance. The margin of a pair is the largest of
its four gaps, all four over the one denominator 2 E_i E_j r_i r_j: positive is apart,
zero is contact with disjoint interiors, negative is overlap (two convex polygons have
disjoint interiors exactly when a line parallel to an edge of one of them weakly
separates them).

A wall's clearance is the signed distance from the square's extreme corner to it: the
half-extent in x and in y is (|a| + |b|) / (2 r).
"""

from __future__ import annotations

from fractions import Fraction
from math import lcm


class Square:
    __slots__ = ("E", "X", "Y", "a", "b", "r", "ext")

    def __init__(self, x: tuple[int, int], y: tuple[int, int], t: tuple[int, int]) -> None:
        e = lcm(x[1], y[1])
        self.E = e
        self.X = x[0] * (e // x[1])
        self.Y = y[0] * (e // y[1])
        p, q = t
        self.a = q * q - p * p
        self.b = 2 * p * q
        self.r = p * p + q * q
        self.ext = abs(self.a) + abs(self.b)

    def is_unit(self) -> bool:
        return self.r > 0 and self.a * self.a + self.b * self.b == self.r * self.r


def pair_gaps(si: Square, sj: Square) -> tuple[list[int], int]:
    """The four gaps' numerators (u_i, v_i, u_j, v_j) over the common denominator."""
    dx = sj.X * si.E - si.X * sj.E
    dy = sj.Y * si.E - si.Y * sj.E
    cdn = si.a * sj.a + si.b * sj.b
    sdn = si.a * sj.b - si.b * sj.a
    k = si.E * sj.E * (si.r * sj.r + abs(cdn) + abs(sdn))
    g = [
        2 * sj.r * abs(si.a * dx + si.b * dy) - k,
        2 * sj.r * abs(-si.b * dx + si.a * dy) - k,
        2 * si.r * abs(sj.a * dx + sj.b * dy) - k,
        2 * si.r * abs(-sj.b * dx + sj.a * dy) - k,
    ]
    den = 2 * si.E * sj.E * si.r * sj.r
    return g, den


def pair_margin(si: Square, sj: Square) -> Fraction:
    g, den = pair_gaps(si, sj)
    return Fraction(max(g), den)


def binding_axes(si: Square, sj: Square) -> int:
    """How many of the four axes attain the margin."""
    g, _ = pair_gaps(si, sj)
    m = max(g)
    return sum(1 for x in g if x == m)


def clearances(sq: Square, side: tuple[int, int]) -> dict[str, Fraction]:
    """Signed clearances to the four walls of [0, S]^2."""
    s = Fraction(side[0], side[1])
    h = Fraction(sq.ext, 2 * sq.r)
    x = Fraction(sq.X, sq.E)
    y = Fraction(sq.Y, sq.E)
    return {"left": x - h, "right": s - x - h, "bottom": y - h, "top": s - y - h}


def classify(m: Fraction) -> str:
    if m > 0:
        return "apart"
    if m == 0:
        return "contact"
    return "overlap"
