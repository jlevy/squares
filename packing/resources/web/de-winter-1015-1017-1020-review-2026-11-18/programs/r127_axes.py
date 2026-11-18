"""Method A: separating axes in Python integers, on corners over one denominator.

Lane r127-1118.  Written for this review; imports nothing from the repository.

Each square's eight coordinates are written over their least common denominator D, so
its corners are integer points Q_k / D and its edges E_k = Q_{k+1} - Q_k integer vectors.
It is a unit square, listed in cyclic order, exactly when E0.E0 = E1.E1 = D^2,
E0.E1 = 0, E2 = -E0 and E3 = -E1 (then the four points are a unit square; the sign of
E0 x E1 is the sense of the listing).

Two convex polygons have disjoint interiors exactly when some line parallel to an edge
of one of them weakly separates them.  For unit squares that means one of the four edge
directions w = E/D of the two squares: the projections of the two squares' corners on
w give two intervals, and their signed separation (positive apart, zero touching,
negative overlapping) is exact.  The pair's margin is the greatest of the four
separations, an exact Fraction: > 0 apart, = 0 contact with disjoint interiors, < 0
overlap.  A wall's clearance is the signed distance from the square's extreme corner to
the wall, for the box [0, S]^2.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import lcm


@dataclass
class SquareA:
    D: int
    Q: list[tuple[int, int]]
    axes: list[tuple[int, int]]
    own: list[tuple[int, int]]  # own projection interval (min, max) of Q.w, per axis
    unit: bool
    sense: int


def prepare(corners: list[tuple[Fraction, Fraction]]) -> SquareA:
    D = 1
    for x, y in corners:
        D = lcm(D, x.denominator, y.denominator)
    Q = [(int(x * D), int(y * D)) for x, y in corners]
    E = [(Q[(k + 1) % 4][0] - Q[k][0], Q[(k + 1) % 4][1] - Q[k][1]) for k in range(4)]
    d2 = D * D
    unit = (
        E[0][0] * E[0][0] + E[0][1] * E[0][1] == d2
        and E[1][0] * E[1][0] + E[1][1] * E[1][1] == d2
        and E[0][0] * E[1][0] + E[0][1] * E[1][1] == 0
        and E[2] == (-E[0][0], -E[0][1])
        and E[3] == (-E[1][0], -E[1][1])
    )
    cross = E[0][0] * E[1][1] - E[0][1] * E[1][0]
    sense = (cross > 0) - (cross < 0)
    axes = [E[0], E[1]]
    own = []
    for w in axes:
        ps = [q[0] * w[0] + q[1] * w[1] for q in Q]
        own.append((min(ps), max(ps)))
    return SquareA(D=D, Q=Q, axes=axes, own=own, unit=unit, sense=sense)


def _sep_on(a: SquareA, k: int, b: SquareA) -> Fraction:
    """Signed separation of a and b along a's k-th edge direction, exactly."""
    w = a.axes[k]
    lo_a, hi_a = a.own[k]
    ps = [q[0] * w[0] + q[1] * w[1] for q in b.Q]
    lo_b, hi_b = min(ps), max(ps)
    # a's projections are Q.w / D_a^2, b's are P.w / (D_a D_b); common denominator D_a^2 D_b.
    lo_a, hi_a = lo_a * b.D, hi_a * b.D
    lo_b, hi_b = lo_b * a.D, hi_b * a.D
    s = max(lo_b - hi_a, lo_a - hi_b)
    return Fraction(s, a.D * a.D * b.D)


def margin(a: SquareA, b: SquareA) -> Fraction:
    return max(_sep_on(a, 0, b), _sep_on(a, 1, b), _sep_on(b, 0, a), _sep_on(b, 1, a))


def walls(a: SquareA, side: Fraction) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    """Clearances (left, bottom, right, top) in the box [0, side]^2."""
    xs = [q[0] for q in a.Q]
    ys = [q[1] for q in a.Q]
    return (
        Fraction(min(xs), a.D),
        Fraction(min(ys), a.D),
        side - Fraction(max(xs), a.D),
        side - Fraction(max(ys), a.D),
    )


def cls(m: Fraction) -> str:
    return "apart" if m > 0 else ("contact" if m == 0 else "overlap")


def decide(corners_list, side: Fraction, pairs=None):
    """Return (units, senses, wall clearances, {pair: margin}) for the given pairs."""
    sq = [prepare(c) for c in corners_list]
    units = [s.unit for s in sq]
    senses = [s.sense for s in sq]
    wl = [walls(s, side) for s in sq]
    n = len(sq)
    if pairs is None:
        pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    mg = {(i, j): margin(sq[i], sq[j]) for i, j in pairs}
    return units, senses, wl, mg
