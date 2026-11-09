"""Method A (lane L72, bead think-qqyg): separating axes in fractions.Fraction.

Written from the mathematics alone; imports nothing from the squares repository.

- A listed polygon p0, p1, p2, p3 is a unit square when, with u = p1 - p0 and
  f = p3 - p0, u.u = 1, f = +-perp(u) and p2 = p0 + u + f. Its edge directions are then
  u and perp(u), both exact rational unit vectors.
- A convex polygon lies in [0, S]^2 exactly when its corners do; the clearance to each
  wall is the least distance of a corner to it, which is negative when a corner is past it.
- Two convex polygons have disjoint interiors exactly when, on one of the edge normals of
  the two, their projections overlap in at most a point. On a unit axis the gap between the
  projections is an exact Euclidean length; the pair margin is the largest gap over the four
  axes. Margin > 0: strictly apart; margin = 0: touching; margin < 0: interiors overlap.
"""

from fractions import Fraction

WALLS = ("left", "right", "bottom", "top")


def corners_frac(raw):
    """raw: four (xn, xd, yn, yd) integer tuples -> four Fraction points."""
    return [(Fraction(xn, xd), Fraction(yn, yd)) for (xn, xd, yn, yd) in raw]


def square(P):
    """Unit-square test. Returns (ok, orientation, axes, reason).

    orientation is +1 when f = perp(u) (listed counterclockwise), -1 when f = -perp(u).
    axes are (u, perp(u)) for an accepted square.
    """
    p0, p1, p2, p3 = P
    u = (p1[0] - p0[0], p1[1] - p0[1])
    f = (p3[0] - p0[0], p3[1] - p0[1])
    if u[0] * u[0] + u[1] * u[1] != 1:
        return False, 0, None, "|p1 - p0| != 1"
    perp = (-u[1], u[0])
    if f == perp:
        orient = 1
    elif f == (u[1], -u[0]):
        orient = -1
    else:
        return False, 0, None, "p3 - p0 is not +-perp(p1 - p0)"
    if p2 != (p0[0] + u[0] + f[0], p0[1] + u[1] + f[1]):
        return False, 0, None, "p2 != p0 + u + f"
    return True, orient, (u, perp), ""


def wall_clearances(P, S):
    """Exact clearances to the left, right, bottom and top walls of [0, S]^2."""
    xs = [p[0] for p in P]
    ys = [p[1] for p in P]
    return (min(xs), S - max(xs), min(ys), S - max(ys))


def proj_range(P, a):
    vals = [p[0] * a[0] + p[1] * a[1] for p in P]
    return min(vals), max(vals)


def own_ranges(P, axes):
    """The projections of a square on its own two axes (cached per square)."""
    return (proj_range(P, axes[0]), proj_range(P, axes[1]))


def pair_margin(Pi, axes_i, own_i, Pj, axes_j, own_j):
    """Exact pair margin and the index (0..3) of the axis that attains it.

    Axes 0, 1 are u_i and perp(u_i); axes 2, 3 are u_j and perp(u_j).
    """
    best = None
    best_k = -1
    for k in range(4):
        if k < 2:
            a = axes_i[k]
            lo_i, hi_i = own_i[k]
            lo_j, hi_j = proj_range(Pj, a)
        else:
            a = axes_j[k - 2]
            lo_j, hi_j = own_j[k - 2]
            lo_i, hi_i = proj_range(Pi, a)
        gap = lo_j - hi_i
        other = lo_i - hi_j
        if other > gap:
            gap = other
        if best is None or gap > best:
            best = gap
            best_k = k
    return best, best_k


def classify(x):
    if x > 0:
        return "apart"
    if x == 0:
        return "touching"
    return "overlapping"


def wall_class(c):
    if c > 0:
        return "clear"
    if c == 0:
        return "contact"
    return "outside"
