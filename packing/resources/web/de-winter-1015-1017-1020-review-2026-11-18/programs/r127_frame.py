"""The closed form by centres and directions: a third formulation of the margins and
clearances, used for the controls' moves and the contraction measurement.

Lane r127-1118.  Written for this review; imports nothing from the repository.

A unit square with centre c and unit edge direction u = (a, b) has v = (-b, a) and
half-extent (|w.u| + |w.v|)/2 on a unit direction w.  On its own two edge directions it
is 1/2; on the other square's it is (|cos D| + |sin D|)/2, where cos D = u_i.u_j and
sin D = u_i x u_j.  So on all four candidate axes of a pair the two half-extents sum to
the same T = (1 + |u_i.u_j| + |u_i x u_j|)/2, and the pair's margin is
max_w |w.d| - T over the four edge directions, d the centre difference.  Scaling d by a
factor tau scales every |w.d| by tau: the margin is tau M - T with M = max_w |w.d|.
The wall clearances are c_x - h_x, c_y - h_y, S - c_x - h_x and S - c_y - h_y with
h_x = (|a| + |b|)/2 = h_y.
"""

from __future__ import annotations

from fractions import Fraction


def frame_of_corners(pts):
    """Centre and edge direction of a square given by four corners in cyclic order."""
    (x0, y0), (x1, y1), (x2, y2), _ = pts
    c = ((x0 + x2) / 2, (y0 + y2) / 2)
    u = (x1 - x0, y1 - y0)
    return c, u


def frames(packing):
    if packing.centres is not None:
        return list(packing.centres), list(packing.directions)
    cs, us = [], []
    for pts in packing.corners:
        c, u = frame_of_corners(pts)
        cs.append(c)
        us.append(u)
    return cs, us


def T_of(ui, uj) -> Fraction:
    cosd = ui[0] * uj[0] + ui[1] * uj[1]
    sind = ui[0] * uj[1] - ui[1] * uj[0]
    return (1 + abs(cosd) + abs(sind)) / 2


def M_of(ui, uj, d) -> Fraction:
    best = None
    for a, b in (ui, uj):
        for wx, wy in ((a, b), (-b, a)):
            p = abs(wx * d[0] + wy * d[1])
            if best is None or p > best:
                best = p
    assert best is not None
    return best


def pair_margin(ci, ui, cj, uj) -> Fraction:
    d = (cj[0] - ci[0], cj[1] - ci[1])
    return M_of(ui, uj, d) - T_of(ui, uj)


def half_extent(u) -> Fraction:
    return (abs(u[0]) + abs(u[1])) / 2


def clearances(c, u, side):
    h = half_extent(u)
    return (c[0] - h, c[1] - h, side - c[0] - h, side - c[1] - h)


def extents(cs, us):
    """(min x, max x, min y, max y) of the packing's squares."""
    hs = [half_extent(u) for u in us]
    xs_lo = min(c[0] - h for c, h in zip(cs, hs, strict=True))
    xs_hi = max(c[0] + h for c, h in zip(cs, hs, strict=True))
    ys_lo = min(c[1] - h for c, h in zip(cs, hs, strict=True))
    ys_hi = max(c[1] + h for c, h in zip(cs, hs, strict=True))
    return xs_lo, xs_hi, ys_lo, ys_hi
