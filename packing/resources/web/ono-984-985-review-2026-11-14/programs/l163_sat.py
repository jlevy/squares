"""Lane L163 method A: separating axes in Python integers, from centres and half-angles.

Square i has centre (X_i, Y_i) / E_i over one denominator and t_i = p/q, so its edge
direction is u_i = (a_i, b_i) / r_i with a = q^2 - p^2, b = 2pq, r = p^2 + q^2, and
v_i = (-b_i, a_i) / r_i. The square is {C + x u + y v : |x|, |y| <= 1/2}.

On a unit normal w of square i, square i projects to an interval of half-length 1/2
and square j to one of half-length (|u_j . w| + |v_j . w|) / 2, which for either normal
of i is (|cos D| + |sin D|) / 2 with D the angle between them. The gap along w is the
centre separation along w less both half-lengths, an exact distance. All four gaps of
a pair share the denominator 2 E_i E_j r_i r_j, so the margin, their maximum, is
decided on integers: positive apart, zero touching, negative overlapping.

Two convex polygons with disjoint interiors are weakly separated by a line parallel to
an edge of one of them, so those three signs are exactly the three classes.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import lcm


@dataclass(frozen=True)
class Sq:
    """One square as integers: centre over E, edge direction over r."""

    X: int
    Y: int
    E: int
    a: int
    b: int
    r: int


def prepare(row: tuple[int, int, int, int, int, int]) -> Sq:
    xn, xd, yn, yd, tn, td = row
    if xd <= 0 or yd <= 0 or td <= 0:
        raise ValueError("denominator not positive")
    e = lcm(xd, yd)
    return Sq(xn * (e // xd), yn * (e // yd), e, td * td - tn * tn, 2 * tn * td, tn * tn + td * td)


def is_unit(s: Sq) -> bool:
    """The edge direction is an exact unit vector."""
    return s.r > 0 and s.a * s.a + s.b * s.b == s.r * s.r


def margin_parts(si: Sq, sj: Sq) -> tuple[list[int], int]:
    """The four gap numerators (normals u_i, v_i, u_j, v_j) and their common denominator."""
    dx = sj.X * si.E - si.X * sj.E
    dy = sj.Y * si.E - si.Y * sj.E
    ee = si.E * sj.E
    k = ee * (si.r * sj.r + abs(si.a * sj.a + si.b * sj.b) + abs(si.a * sj.b - si.b * sj.a))
    g = [
        2 * sj.r * abs(dx * si.a + dy * si.b) - k,
        2 * sj.r * abs(-dx * si.b + dy * si.a) - k,
        2 * si.r * abs(dx * sj.a + dy * sj.b) - k,
        2 * si.r * abs(-dx * sj.b + dy * sj.a) - k,
    ]
    return g, 2 * ee * si.r * sj.r


def margin(si: Sq, sj: Sq) -> Fraction:
    """The pair's separating-axis margin, exactly."""
    g, den = margin_parts(si, sj)
    return Fraction(max(g), den)


def classify(m: Fraction) -> str:
    """A pair margin's class."""
    return "apart" if m > 0 else ("touch" if m == 0 else "overlap")


def wall_class(c: Fraction) -> str:
    """A wall clearance's class."""
    return "apart" if c > 0 else ("contact" if c == 0 else "crossing")


def clearances(s: Sq, side: tuple[int, int]) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    """Signed clearances to the left, bottom, right and top walls of [0, S]^2."""
    p, q = side
    ext = abs(s.a) + abs(s.b)  # twice the half-extent, times r
    den = 2 * s.E * s.r
    left = Fraction(2 * s.r * s.X - s.E * ext, den)
    bottom = Fraction(2 * s.r * s.Y - s.E * ext, den)
    right = Fraction(2 * s.r * (p * s.E - q * s.X) - q * s.E * ext, q * den)
    top = Fraction(2 * s.r * (p * s.E - q * s.Y) - q * s.E * ext, q * den)
    return left, bottom, right, top
