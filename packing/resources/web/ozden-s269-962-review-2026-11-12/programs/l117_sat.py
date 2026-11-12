"""Lane L117, method A: separating axes in plain Python integers.

Clean-room code for the stage 4 review of jlevy/squares#962. Each square's corners are
written over one common positive denominator D (the lcm of its eight), as integer
points P_k, so p_k = P_k / D. With U = P_1 - P_0 and W = P_3 - P_0, the square is a unit
square exactly when U.U = D^2, W is U turned a quarter (either way), and
P_2 = P_0 + U + W. Its edge normals are then u = U/D and w = W/D, exact unit vectors,
and its own projection on u is [u.p_0, u.p_0 + 1], on w [w.p_0, w.p_0 + 1].

A pair's margin is the largest gap over the four normals of the two squares: the
other square's projected interval less this one's. Two convex polygons with disjoint
interiors are weakly separated by a line parallel to an edge of one of them, so a
positive margin is apart, zero is contact with disjoint interiors, and negative is
overlap. Signs are decided on integers; the margin's value is an exact Fraction.

A wall's clearance is the least distance from a corner to it, an exact Fraction.
"""

from __future__ import annotations

import math
from fractions import Fraction

Rat = tuple[int, int]
Corner = tuple[Rat, Rat]


class SquareA:
    """A square over a common denominator, with its unit-square test."""

    __slots__ = ("D", "P", "U", "W", "sense", "pu", "pw")

    def __init__(self, corners: list[Corner]) -> None:
        dens = [c[1] for pt in corners for c in pt]
        D = 1
        for q in dens:
            D = D * q // math.gcd(D, q)
        self.D = D
        self.P = [(x[0] * (D // x[1]), y[0] * (D // y[1])) for x, y in corners]
        p0, p1, p2, p3 = self.P
        self.U = (p1[0] - p0[0], p1[1] - p0[1])
        self.W = (p3[0] - p0[0], p3[1] - p0[1])
        ux, uy = self.U
        self.sense = 0
        if ux * ux + uy * uy == D * D and p2 == (p0[0] + ux + self.W[0], p0[1] + uy + self.W[1]):
            if self.W == (-uy, ux):
                self.sense = 1  # counterclockwise listing
            elif self.W == (uy, -ux):
                self.sense = -1  # clockwise listing
        # own interval lower ends on u and w, scaled by D^2
        self.pu = ux * p0[0] + uy * p0[1]
        self.pw = self.W[0] * p0[0] + self.W[1] * p0[1]

    @property
    def unit(self) -> bool:
        return self.sense != 0


def _gap_on_own_axis(a: SquareA, ax: tuple[int, int], lo_scaled: int, b: SquareA) -> Fraction:
    """Gap along a's unit normal ax/D_a between a's interval and b's projection."""
    Da, Db = a.D, b.D
    projs = [ax[0] * q[0] + ax[1] * q[1] for q in b.P]  # b's corners on ax, scale D_a * D_b
    mn, mx = min(projs), max(projs)
    # common scale D_a^2 * D_b
    above = Da * mn - Db * lo_scaled - Da * Da * Db  # b above a's interval
    below = Db * lo_scaled - Da * mx  # b below a's interval
    return Fraction(max(above, below), Da * Da * Db)


def pair_margin(a: SquareA, b: SquareA) -> Fraction:
    """Exact margin of a unit-square pair: positive apart, zero contact, negative overlap."""
    return max(
        _gap_on_own_axis(a, a.U, a.pu, b),
        _gap_on_own_axis(a, a.W, a.pw, b),
        _gap_on_own_axis(b, b.U, b.pu, a),
        _gap_on_own_axis(b, b.W, b.pw, a),
    )


def pair_class(m: Fraction) -> str:
    return "apart" if m > 0 else ("contact" if m == 0 else "overlap")


def wall_clearances(a: SquareA, side: Fraction) -> dict[str, Fraction]:
    """Least corner distance to each wall of [0, side]^2; negative is outside."""
    xs = [p[0] for p in a.P]
    ys = [p[1] for p in a.P]
    return {
        "left": Fraction(min(xs), a.D),
        "bottom": Fraction(min(ys), a.D),
        "right": side - Fraction(max(xs), a.D),
        "top": side - Fraction(max(ys), a.D),
    }


def wall_class(c: Fraction) -> str:
    return "apart" if c > 0 else ("contact" if c == 0 else "outside")
