"""Method A of lane r127b-1118: separating axes in Python integers, from poses.

A pose is a centre and the unit direction of one edge, ``(cx, cy, c, s)``, each a
rational ``(p, q)`` as the reader hands it. The square is the set
``C + alpha*u + beta*v`` with ``|alpha|, |beta| <= 1/2``, ``u = (c, s)`` and
``v = (-s, c)``; the square is the same whichever of its four edge directions is given.

Each pose is written over integers: the centre as ``(X, Y) / E`` and the direction as
``(a, b) / r``, and it is a unit square exactly when ``a*a + b*b == r*r``.

For a pair, every one of the four edge normals ``w`` (two of each square) gives an
exact separation ``|d . w| - H``, ``d`` the centre difference, where
``H = 1/2 + (|cos D| + |sin D|)/2`` is the sum of the two squares' half-widths on any of
the four normals (``D`` the angle between the squares). The margin is the largest of the
four separations: positive is apart, zero is contact with disjoint interiors, negative
is overlap. Two convex polygons have disjoint interiors exactly when a line parallel to
an edge of one of them weakly separates them, and are disjoint exactly when one does so
strictly, so the three signs are exactly those three classes.

All four separations and ``H`` share the denominator ``L = 2 E_i E_j r_i r_j``, so the
margin is decided on one integer numerator and kept as an exact fraction. The pair's
contact factor, the scale of the centre difference at which the margin is zero, is
``H / max_w |d . w|``, also exact.

A wall's clearance is the signed distance from the square's extreme point to the wall,
from the half-extent ``(|a| + |b|) / (2 r)``, the same on both axes.

The module reads no corner and imports nothing from this repository or the source.
"""

from __future__ import annotations

from fractions import Fraction
from math import lcm
from typing import NamedTuple

Q = tuple[int, int]


class IPose(NamedTuple):
    X: int
    Y: int
    E: int
    a: int
    b: int
    r: int


def to_ipose(cx: Q, cy: Q, c: Q, s: Q) -> IPose:
    """Write a pose over integers. Denominators are positive by the reader."""
    E = lcm(cx[1], cy[1])
    X = cx[0] * (E // cx[1])
    Y = cy[0] * (E // cy[1])
    r = lcm(c[1], s[1])
    a = c[0] * (r // c[1])
    b = s[0] * (r // s[1])
    return IPose(X, Y, E, a, b, r)


def is_unit(p: IPose) -> bool:
    return p.a * p.a + p.b * p.b == p.r * p.r


def pair_numbers(pi: IPose, pj: IPose) -> tuple[int, int, int]:
    """Return ``(M, Hn, L)``: the margin is ``(M - Hn) / L`` and the factor ``Hn / M``.

    ``M`` is the numerator of ``max_w |d . w|`` and ``Hn`` that of ``H``, both over ``L``.
    """
    Ei, Ej = pi.E, pj.E
    dx = pj.X * Ei - pi.X * Ej
    dy = pj.Y * Ei - pi.Y * Ej
    ai, bi, ri = pi.a, pi.b, pi.r
    aj, bj, rj = pj.a, pj.b, pj.r
    pu_i = abs(dx * ai + dy * bi) * 2 * rj
    pv_i = abs(-dx * bi + dy * ai) * 2 * rj
    pu_j = abs(dx * aj + dy * bj) * 2 * ri
    pv_j = abs(-dx * bj + dy * aj) * 2 * ri
    M = max(pu_i, pv_i, pu_j, pv_j)
    cosn = abs(ai * aj + bi * bj)
    sinn = abs(ai * bj - bi * aj)
    Hn = (ri * rj + cosn + sinn) * Ei * Ej
    L = 2 * Ei * Ej * ri * rj
    return M, Hn, L


def margin(pi: IPose, pj: IPose) -> Fraction:
    M, Hn, L = pair_numbers(pi, pj)
    return Fraction(M - Hn, L)


def margin_sign(pi: IPose, pj: IPose) -> int:
    M, Hn, _ = pair_numbers(pi, pj)
    return (M > Hn) - (M < Hn)


def contact_factor(pi: IPose, pj: IPose) -> Fraction | None:
    """The scale of ``d`` at which the pair touches; ``None`` if the centres coincide."""
    M, Hn, _ = pair_numbers(pi, pj)
    if M == 0:
        return None
    return Fraction(Hn, M)


def half_extent(p: IPose) -> Fraction:
    return Fraction(abs(p.a) + abs(p.b), 2 * p.r)


def clearances(p: IPose, side: Q) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    """Left, bottom, right and top clearances in the box ``[0, side]^2``."""
    S = Fraction(side[0], side[1])
    h = half_extent(p)
    x = Fraction(p.X, p.E)
    y = Fraction(p.Y, p.E)
    return (x - h, y - h, S - x - h, S - y - h)


def centre(p: IPose) -> tuple[Fraction, Fraction]:
    return Fraction(p.X, p.E), Fraction(p.Y, p.E)


def direction(p: IPose) -> tuple[Fraction, Fraction]:
    return Fraction(p.a, p.r), Fraction(p.b, p.r)
