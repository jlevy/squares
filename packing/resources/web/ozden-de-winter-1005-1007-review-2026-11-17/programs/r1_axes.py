"""Method A: separating axes in Python integers.

Lane R1, stage 4 review of #1005, #1006 and #1007.  Clean-room.

A square is held as four integer points Q[k] over one positive denominator D (its
corners are Q[k]/D) with its edge vectors E[k] = Q[k+1] - Q[k].  It is a unit square
listed in cyclic order exactly when

    E0.E0 = D^2,  E1.E1 = D^2,  E0.E1 = 0,  E2 = -E0,  E3 = -E1,

and then E0/D and E1/D are unit vectors, the square's two edge directions.

Two convex polygons have disjoint interiors exactly when some line parallel to an
edge of one of them weakly separates them.  For two unit squares that is four
directions.  On a unit direction w the two squares project to intervals, and

    sep_w = max(min_j - max_i, min_i - max_j)

is the signed distance between the intervals (negative when they overlap).  The
margin of the pair is the greatest of the four sep_w: positive, the squares are
apart; zero, they touch with disjoint interiors; negative, their interiors meet.
All of it is decided in integers and returned as an exact fraction.

For a file that gives a centre c and a direction u = (cos, sin), the direction is
first required to be a unit vector on the file's own numbers, and the corners are
c + (-u - v)/2, c + (u - v)/2, c + (u + v)/2, c + (-u + v)/2 with v = (-sin, cos).
"""

from __future__ import annotations

from fractions import Fraction
from math import lcm


class SquareA:
    __slots__ = ("D", "Q", "E0", "E1", "unit", "sense", "why")


def _build(D, Q):
    sq = SquareA()
    sq.D, sq.Q = D, Q
    E = [(Q[(k + 1) % 4][0] - Q[k][0], Q[(k + 1) % 4][1] - Q[k][1]) for k in range(4)]
    sq.E0, sq.E1 = E[0], E[1]
    dd = D * D
    problems = []
    if E[0][0] * E[0][0] + E[0][1] * E[0][1] != dd:
        problems.append("first edge is not of length 1")
    if E[1][0] * E[1][0] + E[1][1] * E[1][1] != dd:
        problems.append("second edge is not of length 1")
    if E[0][0] * E[1][0] + E[0][1] * E[1][1] != 0:
        problems.append("first two edges are not perpendicular")
    if E[2] != (-E[0][0], -E[0][1]):
        problems.append("third edge is not the first reversed")
    if E[3] != (-E[1][0], -E[1][1]):
        problems.append("fourth edge is not the second reversed")
    cross = E[0][0] * E[1][1] - E[0][1] * E[1][0]
    sq.sense = (cross > 0) - (cross < 0)
    sq.unit = not problems
    sq.why = problems
    return sq


def from_corners(corners):
    """corners: four (Fraction, Fraction) in the order the file lists them."""
    D = 1
    for x, y in corners:
        D = lcm(D, x.denominator, y.denominator)
    Q = [
        (x.numerator * (D // x.denominator), y.numerator * (D // y.denominator))
        for x, y in corners
    ]
    return _build(D, Q)


def from_centre(cx, cy, ux, uy):
    """A centre and a direction, as the file gives them (Fractions)."""
    a, b = ux.numerator, ux.denominator
    c, d = uy.numerator, uy.denominator
    direction_is_unit = a * a * d * d + c * c * b * b == b * b * d * d
    hx, hy = ux / 2, uy / 2
    corners = [
        (cx - hx + hy, cy - hy - hx),
        (cx + hx + hy, cy + hy - hx),
        (cx + hx - hy, cy + hy + hx),
        (cx - hx - hy, cy - hy + hx),
    ]
    sq = from_corners(corners)
    if not direction_is_unit:
        sq.unit = False
        sq.why = ["direction is not a unit vector"] + sq.why
    return sq


def of_packing(packing):
    if packing.form == "corners":
        return [from_corners(c) for c in packing.squares]
    return [from_centre(*c) for c in packing.squares]


def clearances(sq, side):
    """(left, bottom, right, top): signed distances of the square inside each wall."""
    xs = [p[0] for p in sq.Q]
    ys = [p[1] for p in sq.Q]
    D = sq.D
    return (
        Fraction(min(xs), D),
        Fraction(min(ys), D),
        side - Fraction(max(xs), D),
        side - Fraction(max(ys), D),
    )


def margin(si, sj):
    """The exact margin of a pair of unit squares: the greatest of four separations."""
    best = None
    Di, Dj = si.D, sj.D
    for owner in (si, sj):
        Dk = owner.D
        den = Di * Dj * Dk
        for ex, ey in (owner.E0, owner.E1):
            pi = [(qx * ex + qy * ey) * Dj for qx, qy in si.Q]
            pj = [(qx * ex + qy * ey) * Di for qx, qy in sj.Q]
            num = max(min(pj) - max(pi), min(pi) - max(pj))
            sep = Fraction(num, den)
            if best is None or sep > best:
                best = sep
    return best


def classify(value):
    """The class of a margin or of a clearance."""
    if value > 0:
        return "apart"
    if value == 0:
        return "touching"
    return "overlapping"
