"""The closed form by centres and half-extents, and the moves the controls make.

Lane R1, stage 4 review of #1005, #1006 and #1007.  Clean-room.  It decides no
certificate: it is a third formulation, compared with method A on every pair and
wall (control C0) and used to compute how far a square must move to reach contact.

A unit square is a centre c and two orthogonal unit edge directions u and v.  Its
half-extent along a unit direction w is

    h(w) = (|u.w| + |v.w|) / 2,

so the separation of two squares along w is |d.w| - h_i(w) - h_j(w) with
d = c_j - c_i, and the margin is the greatest separation over w in {u_i, v_i, u_j,
v_j}.  The clearance at a wall is the centre's distance from it less the
half-extent along that wall's normal.

Closing a pair.  Moving square j to c_j - tau*d (toward square i along the centre
line, 0 <= tau < 1) scales every |d.w| by (1 - tau) and leaves every h unchanged, so
sep_w(tau) = (1 - tau)|d.w| - H_w is non-increasing in tau.  With
tau_w = 1 - (m + H_w)/|d.w| on each direction with |d.w| > 0, the time
tau* = max_w tau_w gives sep_w(tau*) <= m on every direction with equality on the
maximising one, so the margin is exactly m (m = 0 is contact, m < 0 an overlap of
that depth), provided m >= -min H_w, which holds for |m| below 1.
"""

from __future__ import annotations

from fractions import Fraction

HALF = Fraction(1, 2)


class Frame:
    __slots__ = ("c", "u", "v")

    def __init__(self, c, u, v):
        self.c, self.u, self.v = c, u, v


def from_corners(corners):
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = corners
    return Frame(((x0 + x2) / 2, (y0 + y2) / 2), (x1 - x0, y1 - y0), (x3 - x0, y3 - y0))


def from_centre(cx, cy, ux, uy):
    return Frame((cx, cy), (ux, uy), (-uy, ux))


def of_packing(packing):
    if packing.form == "corners":
        return [from_corners(c) for c in packing.squares]
    return [from_centre(*c) for c in packing.squares]


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def half_extent(frame, w):
    return (abs(_dot(frame.u, w)) + abs(_dot(frame.v, w))) / 2


def margin(fi, fj):
    d = (fj.c[0] - fi.c[0], fj.c[1] - fi.c[1])
    best = None
    for w in (fi.u, fi.v, fj.u, fj.v):
        sep = abs(_dot(d, w)) - half_extent(fi, w) - half_extent(fj, w)
        if best is None or sep > best:
            best = sep
    return best


def clearances(frame, side):
    hx = (abs(frame.u[0]) + abs(frame.v[0])) / 2
    hy = (abs(frame.u[1]) + abs(frame.v[1])) / 2
    cx, cy = frame.c
    return (cx - hx, cy - hy, side - cx - hx, side - cy - hy)


def closing_time(fi, fj, target):
    """tau* such that square j at c_j - tau*(c_j - c_i) has margin exactly `target`.

    None when the centres coincide.
    """
    d = (fj.c[0] - fi.c[0], fj.c[1] - fi.c[1])
    best = None
    for w in (fi.u, fi.v, fj.u, fj.v):
        rate = abs(_dot(d, w))
        if rate == 0:
            continue
        tau = 1 - (target + half_extent(fi, w) + half_extent(fj, w)) / rate
        if best is None or tau > best:
            best = tau
    return best


def closing_shift(fi, fj, target):
    """The translation of square j that brings the pair's margin to `target`."""
    tau = closing_time(fi, fj, target)
    if tau is None:
        return None
    return (-tau * (fj.c[0] - fi.c[0]), -tau * (fj.c[1] - fi.c[1]))


def translate_square(form, square, shift):
    """A square of the reader's form moved by a rational vector."""
    tx, ty = shift
    if form == "corners":
        return tuple((x + tx, y + ty) for x, y in square)
    cx, cy, ux, uy = square
    return (cx + tx, cy + ty, ux, uy)


WALLS = ("left", "bottom", "right", "top")
WALL_PUSH = {"left": (-1, 0), "bottom": (0, -1), "right": (1, 0), "top": (0, 1)}


def wall_shift(wall, amount):
    """The translation that lowers the clearance at `wall` by `amount`."""
    px, py = WALL_PUSH[wall]
    return (px * amount, py * amount)
