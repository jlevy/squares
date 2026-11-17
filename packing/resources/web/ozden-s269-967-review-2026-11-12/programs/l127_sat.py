"""Method A: unit squares, wall clearances and pair margins by separating axes.

Lane L127, clean room. Plain Python integers only; no floating point, no fractions in
the deciding path.

Each square's eight coordinates are put over one denominator D (the lcm of its eight
denominators) as integer corners P0..P3. The square is a unit square listed in cyclic
order exactly when, with U = P1 - P0 and W = P3 - P0,

    U.U == D*D,   W == rot(U) for a quarter turn either way,   P2 == P0 + U + W.

Its edge normals are then u = U/D and w = W/D, exact unit vectors, and its own
projections on them are [P0.U/D^2, P0.U/D^2 + 1] and [P0.W/D^2, P0.W/D^2 + 1].

A pair's margin is the largest projection gap over the four normals of the two squares.
Two convex polygons with disjoint interiors are weakly separated by a line parallel to an
edge of one of them, so: margin > 0 apart, margin == 0 touching with disjoint
interiors, margin < 0 interiors overlapping.

A wall's clearance is the least signed distance from a corner to that wall, measured
into the box.

Fractions are carried as (numerator, denominator) with denominator > 0.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import lcm

Rat = tuple[int, int]


@dataclass(frozen=True)
class SquareA:
    d: int  # common denominator of the eight coordinates
    pts: tuple[tuple[int, int], ...]  # integer corners, value = pt / d
    u: tuple[int, int]  # edge P1 - P0 (length d)
    w: tuple[int, int]  # edge P3 - P0 (length d)
    sense: int  # +1 counterclockwise listing, -1 clockwise
    lo_u: int  # P0 . U  (own interval on u is [lo_u, lo_u + d^2] / d^2)
    lo_w: int  # P0 . W


class NotUnit(Exception):
    """The four corners are not a unit square in cyclic order."""


def make_square(corners: list[tuple[Rat, Rat]]) -> SquareA:
    d = 1
    for (_, xq), (_, yq) in corners:
        d = lcm(d, xq, yq)
    pts = tuple((xp * (d // xq), yp * (d // yq)) for (xp, xq), (yp, yq) in corners)
    p0, p1, p2, p3 = pts
    u = (p1[0] - p0[0], p1[1] - p0[1])
    w = (p3[0] - p0[0], p3[1] - p0[1])
    if u[0] * u[0] + u[1] * u[1] != d * d:
        msg = "first edge is not of length 1"
        raise NotUnit(msg)
    if w == (-u[1], u[0]):
        sense = 1
    elif w == (u[1], -u[0]):
        sense = -1
    else:
        msg = "fourth corner is not the first edge turned a quarter"
        raise NotUnit(msg)
    if p2 != (p0[0] + u[0] + w[0], p0[1] + u[1] + w[1]):
        msg = "third corner is not opposite the first"
        raise NotUnit(msg)
    lo_u = p0[0] * u[0] + p0[1] * u[1]
    lo_w = p0[0] * w[0] + p0[1] * w[1]
    return SquareA(d=d, pts=pts, u=u, w=w, sense=sense, lo_u=lo_u, lo_w=lo_w)


def _gap_on_axis(a: SquareA, axis: tuple[int, int], lo: int, b: SquareA) -> Rat:
    """Projection gap between square a (owner of the axis) and square b on that axis.

    Everything is over the denominator b.d * a.d^2.
    """
    da, db = a.d, b.d
    projs = [q[0] * axis[0] + q[1] * axis[1] for q in b.pts]  # over db * da
    bmin = min(projs)
    bmax = max(projs)
    hi = lo + da * da  # over da^2
    beyond_hi = bmin * da - hi * db
    beyond_lo = lo * db - bmax * da
    return (max(beyond_hi, beyond_lo), db * da * da)


def _rat_max(x: Rat, y: Rat) -> Rat:
    return x if x[0] * y[1] >= y[0] * x[1] else y


def pair_margin(a: SquareA, b: SquareA) -> Rat:
    """The largest gap over the four edge normals, as (num, den), den > 0."""
    m = _gap_on_axis(a, a.u, a.lo_u, b)
    m = _rat_max(m, _gap_on_axis(a, a.w, a.lo_w, b))
    m = _rat_max(m, _gap_on_axis(b, b.u, b.lo_u, a))
    return _rat_max(m, _gap_on_axis(b, b.w, b.lo_w, a))


def pair_class(margin: Rat) -> str:
    if margin[0] > 0:
        return "apart"
    if margin[0] == 0:
        return "touch"
    return "overlap"


WALLS = ("left", "bottom", "right", "top")


def wall_clearances(sq: SquareA, side: Rat) -> dict[str, Rat]:
    """Signed clearance of the square from each wall of [0, side]^2, positive inside."""
    sp, sq_ = side
    xs = [p[0] for p in sq.pts]
    ys = [p[1] for p in sq.pts]
    d = sq.d
    return {
        "left": (min(xs), d),
        "bottom": (min(ys), d),
        "right": (sp * d - max(xs) * sq_, sq_ * d),
        "top": (sp * d - max(ys) * sq_, sq_ * d),
    }


def wall_class(clearance: Rat) -> str:
    if clearance[0] > 0:
        return "clear"
    if clearance[0] == 0:
        return "touch"
    return "outside"
