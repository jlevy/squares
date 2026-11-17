"""Method A: separating axes in fractions.Fraction (review L83, clean room).

A square is accepted when its listed corners p0..p3 satisfy u = p1 - p0 with u.u = 1,
p3 - p0 = +-perp(u) and p2 = p0 + u + (p3 - p0). Its edge normals u and perp(u) are then
exact rational unit vectors, so every projection gap below is an exact length.

Two squares have disjoint interiors exactly when, on one of the four edge normals of
the pair, their projections overlap in at most a point. The pair margin is the largest
gap over those four axes: positive is clear, zero is contact, negative is overlap.
"""

from __future__ import annotations

from fractions import Fraction

Pt = tuple[Fraction, Fraction]


def frac(pq: tuple[int, int]) -> Fraction:
    return Fraction(pq[0], pq[1])


def points(corners) -> list[Pt]:
    return [(frac(x), frac(y)) for x, y in corners]


class Square:
    __slots__ = ("pts", "sense", "axes", "own")

    def __init__(self, pts: list[Pt]):
        self.pts = pts
        (x0, y0), (x1, y1), (x2, y2), (x3, y3) = pts
        ux, uy = x1 - x0, y1 - y0
        fx, fy = x3 - x0, y3 - y0
        if ux * ux + uy * uy != 1:
            raise ValueError("first edge is not of length 1")
        if (fx, fy) == (-uy, ux):
            self.sense = 1
        elif (fx, fy) == (uy, -ux):
            self.sense = -1
        else:
            raise ValueError("last edge is not the first turned a quarter")
        if (x2, y2) != (x0 + ux + fx, y0 + uy + fy):
            raise ValueError("third corner is not p0 + u + f")
        self.axes = ((ux, uy), (-uy, ux))
        self.own = tuple(interval(pts, a) for a in self.axes)


def interval(pts: list[Pt], a: Pt) -> tuple[Fraction, Fraction]:
    ax, ay = a
    vals = [x * ax + y * ay for x, y in pts]
    return min(vals), max(vals)


def pair_margin(a: Square, b: Square) -> Fraction:
    best = None
    for sq, other in ((a, b), (b, a)):
        for axis, (lo, hi) in zip(sq.axes, sq.own):
            lo2, hi2 = interval(other.pts, axis)
            g = lo2 - hi if lo2 - hi > lo - hi2 else lo - hi2
            if best is None or g > best:
                best = g
    assert best is not None
    return best


def wall_clearances(pts: list[Pt], side: Fraction) -> dict[str, Fraction]:
    xs = [x for x, _ in pts]
    ys = [y for _, y in pts]
    return {"left": min(xs), "bottom": min(ys), "right": side - max(xs), "top": side - max(ys)}


def classify(value: Fraction) -> str:
    return "clear" if value > 0 else ("contact" if value == 0 else "overlap")
