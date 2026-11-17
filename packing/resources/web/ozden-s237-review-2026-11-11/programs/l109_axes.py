"""Lane L109's method A: separating axes in exact rationals (``fractions.Fraction``).

A square is accepted when u = p1 - p0 has u.u = 1, p3 - p0 = +-perp(u) and
p2 = p0 + u + (p3 - p0); its two edge directions u and perp(u) are then exact rational
unit vectors.

A pair's margin is the largest gap, over the four edge directions of the two squares
and both senses of each, between the projections of the two squares. For two convex
polygons the Minkowski difference has only edges parallel to theirs, so the margin is
positive exactly when the closed squares are disjoint, zero exactly when they touch
with disjoint interiors, and negative exactly when their interiors meet.

A wall clearance is the distance from the square's extreme corner coordinate to the
wall, inward positive.

Imports nothing from the repository or the source.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q

Pt = tuple[Q, Q]


class NotUnit(Exception):
    pass


@dataclass(frozen=True)
class SquareA:
    pts: tuple[Pt, Pt, Pt, Pt]
    axes: tuple[Pt, Pt]  # u, perp(u): exact unit vectors
    own: tuple[tuple[Q, Q], tuple[Q, Q]]  # own projection interval on each own axis
    ccw: bool


def _dot(a: Pt, b: Pt) -> Q:
    return a[0] * b[0] + a[1] * b[1]


def _span(pts: tuple[Pt, ...], ax: Pt) -> tuple[Q, Q]:
    vals = [_dot(p, ax) for p in pts]
    return (min(vals), max(vals))


def make(pts: list[Pt]) -> SquareA:
    if len(pts) != 4:
        raise NotUnit("not four corners")
    p0, p1, p2, p3 = pts
    u = (p1[0] - p0[0], p1[1] - p0[1])
    if _dot(u, u) != 1:
        raise NotUnit("first edge is not of length 1")
    v = (p3[0] - p0[0], p3[1] - p0[1])
    perp = (-u[1], u[0])
    if v == perp:
        ccw = True
    elif v == (u[1], -u[0]):
        ccw = False
    else:
        raise NotUnit("last edge is not the first turned by a right angle")
    if p2 != (p0[0] + u[0] + v[0], p0[1] + u[1] + v[1]):
        raise NotUnit("third corner is not p0 + u + v")
    t = (p0, p1, p2, p3)
    return SquareA(pts=t, axes=(u, perp), own=(_span(t, u), _span(t, perp)), ccw=ccw)


def margin(a: SquareA, b: SquareA) -> Q:
    """Largest projection gap over the four edge directions: >0 apart, 0 touching, <0 overlapping."""
    best: Q | None = None
    for sq, other in ((a, b), (b, a)):
        for k in range(2):
            ax = sq.axes[k]
            lo_s, hi_s = sq.own[k]
            lo_o, hi_o = _span(other.pts, ax)
            g = max(lo_o - hi_s, lo_s - hi_o)
            if best is None or g > best:
                best = g
    assert best is not None
    return best


WALLS = ("left", "bottom", "right", "top")


def walls(a: SquareA, side: Q) -> dict[str, Q]:
    xs = [p[0] for p in a.pts]
    ys = [p[1] for p in a.pts]
    return {"left": min(xs), "bottom": min(ys), "right": side - max(xs), "top": side - max(ys)}


def sign_class(v: Q) -> str:
    return "apart" if v > 0 else ("contact" if v == 0 else "overlap")


def wall_class(v: Q) -> str:
    return "clear" if v > 0 else ("contact" if v == 0 else "outside")
