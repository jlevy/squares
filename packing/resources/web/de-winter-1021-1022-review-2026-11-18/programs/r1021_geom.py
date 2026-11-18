"""Method A of lane r1021-1118: separating axes on poses, in Python integers.

A pose is (x, y, c, s): the centre and the unit direction u = (c, s) of one edge; the
square is C + a u + b v with |a|, |b| <= 1/2 and v = (-s, c).  Method A is handed
poses and never a corner.

For a pair, on each of the four edge normals w in {u_i, v_i, u_j, v_j} the two
half-widths add to the same H = 1/2 + (|cos D| + |sin D|)/2, D the angle between the
squares, and the separation along w is |d . w| - H, d the centre difference.  The
pair's margin is the largest of the four.  Two convex polygons have disjoint
interiors exactly when a line parallel to an edge of one of them weakly separates
them, so margin > 0 is apart, margin = 0 is contact with disjoint interiors, and
margin < 0 is overlap.

Each centre is written (X, Y)/E and each direction (A, B)/R in integers; all four
separations then share the denominator 2 E_i E_j R_i R_j, and the margin's sign is
decided on one integer numerator.  The contact factor of a pair, the scale of the
centre difference at which the pair first touches, is H / max_w |d . w|.
"""

from __future__ import annotations

from fractions import Fraction
from math import lcm


def int_pose(p):
    """(x, y, c, s) as Fractions -> (X, Y, E, A, B, R) in integers."""
    x, y, c, s = p
    e = lcm(x.denominator, y.denominator)
    r = lcm(c.denominator, s.denominator)
    return (
        x.numerator * (e // x.denominator),
        y.numerator * (e // y.denominator),
        e,
        c.numerator * (r // c.denominator),
        s.numerator * (r // s.denominator),
        r,
    )


def is_unit(p) -> bool:
    _x, _y, c, s = p
    return c * c + s * s == 1


def pair_terms(pi, pj):
    """Return (P, Hn, Den) for two integer poses.

    The largest projection |d . w| is 2P / Den, the summed half-width H is Hn / Den,
    so the margin is (2P - Hn) / Den and the contact factor is Hn / (2P).
    """
    xi, yi, ei, ai, bi, ri = pi
    xj, yj, ej, aj, bj, rj = pj
    dx = xj * ei - xi * ej
    dy = yj * ei - yi * ej
    p = max(
        rj * abs(dx * ai + dy * bi),
        rj * abs(dy * ai - dx * bi),
        ri * abs(dx * aj + dy * bj),
        ri * abs(dy * aj - dx * bj),
    )
    hn = ei * ej * (ri * rj + abs(ai * aj + bi * bj) + abs(ai * bj - bi * aj))
    den = 2 * ei * ej * ri * rj
    return p, hn, den


def margin(pi, pj) -> Fraction:
    p, hn, den = pair_terms(pi, pj)
    return Fraction(2 * p - hn, den)


def all_margins(ints):
    """Every pair i < j (0-based) -> exact margin, in lexicographic order."""
    n = len(ints)
    out = []
    for i in range(n):
        pi = ints[i]
        for j in range(i + 1, n):
            p, hn, den = pair_terms(pi, ints[j])
            out.append(Fraction(2 * p - hn, den))
    return out


def half_extent(p) -> Fraction:
    _x, _y, c, s = p
    return (abs(c) + abs(s)) / 2


def clearances(p, side: Fraction):
    """Signed distances (left, bottom, right, top) from the square to the walls of [0, side]^2."""
    x, y, _c, _s = p
    e = half_extent(p)
    return (x - e, y - e, side - x - e, side - y - e)


def corners_of(p):
    """The four corners C + u/2 + v/2, C - u/2 + v/2, C - u/2 - v/2, C + u/2 - v/2 (counterclockwise)."""
    x, y, c, s = p
    ux, uy = c / 2, s / 2
    vx, vy = -s / 2, c / 2
    return (
        (x + ux + vx, y + uy + vy),
        (x - ux + vx, y - uy + vy),
        (x - ux - vx, y - uy - vy),
        (x + ux - vx, y + uy - vy),
    )


def d2(a, b) -> Fraction:
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def pose_of_corners(q):
    """Corners in listed order -> (unit, pose).  unit: four sides of squared length 1, two diagonals of 2."""
    sides = [d2(q[k], q[(k + 1) % 4]) for k in range(4)]
    diags = [d2(q[0], q[2]), d2(q[1], q[3])]
    unit = all(v == 1 for v in sides) and all(v == 2 for v in diags)
    x = (q[0][0] + q[1][0] + q[2][0] + q[3][0]) / 4
    y = (q[0][1] + q[1][1] + q[2][1] + q[3][1]) / 4
    c = q[1][0] - q[0][0]
    s = q[1][1] - q[0][1]
    return unit, (x, y, c, s)


def twin_match(q, p):
    """Is the corner list q the corners of pose p, as a cyclic list in either sense?

    Returns (offset, sense) with sense 'ccw' or 'cw', or None.  The counterclockwise
    list is corners_of(p); offset o means q starts at its corner o.
    """
    e = corners_of(p)
    for o in range(4):
        if all(q[k] == e[(o + k) % 4] for k in range(4)):
            return o, "ccw"
        if all(q[k] == e[(o - k) % 4] for k in range(4)):
            return o, "cw"
    return None


def decide_poses(poses, side: Fraction):
    """Method A on a list of poses in [0, side]^2.

    Returns a dict: unit (indices not unit), clearances, margins (lexicographic pairs).
    """
    not_unit = [k for k, p in enumerate(poses) if not is_unit(p)]
    clear = [clearances(p, side) for p in poses]
    ints = [int_pose(p) for p in poses]
    margins = all_margins(ints)
    return {"not_unit": not_unit, "clearances": clear, "margins": margins, "ints": ints}


def pair_index(n: int):
    """The lexicographic list of pairs (i, j), i < j, 0-based."""
    return [(i, j) for i in range(n) for j in range(i + 1, n)]


def contact_factors(ints):
    """Every pair's contact factor as (num, den) with num/den = Hn/(2P); None for coincident centres."""
    n = len(ints)
    out = []
    for i in range(n):
        pi = ints[i]
        for j in range(i + 1, n):
            p, hn, _den = pair_terms(pi, ints[j])
            out.append((hn, 2 * p) if p else None)
    return out
