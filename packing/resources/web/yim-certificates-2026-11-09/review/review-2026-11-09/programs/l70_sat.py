"""Method A for the L70 review: separating axes in ``fractions.Fraction``.

Clean room. A square is its four corners. It is a unit square when, with
``e1 = p1 - p0`` and ``e2 = p3 - p0``, ``e1.e1 = 1``, ``e2 = +-perp(e1)`` and
``p2 = p0 + e1 + e2``. Then ``e1`` and ``e2`` are its unit edge normals.

* Containment: a convex polygon lies in ``[0, S]^2`` exactly when its corners do.
  The clearance to each wall is exact.
* Pairs: two convex polygons have disjoint interiors exactly when, on one edge
  normal of either, their projections overlap in at most a point. The pair margin
  is the largest projection gap over the four normals; since the normals are unit
  vectors it is a length. Margin > 0: apart; = 0: touching; < 0: interiors meet.

Imports nothing but the standard library; reads only the integers the reader gives.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any

F = Fraction


def corners_from_cert_row(row: tuple[int, ...]) -> list[tuple[Fraction, Fraction]]:
    xn, xd, yn, yd, tn, td = row
    x = F(xn, xd)
    y = F(yn, yd)
    t = F(tn, td)
    t2 = t * t
    den = 1 + t2
    c = (1 - t2) / den
    s = 2 * t / den
    ux, uy = c, s
    vx, vy = -s, c
    hux, huy, hvx, hvy = ux / 2, uy / 2, vx / 2, vy / 2
    return [
        (x - hux - hvx, y - huy - hvy),
        (x + hux - hvx, y + huy - hvy),
        (x + hux + hvx, y + huy + hvy),
        (x - hux + hvx, y - huy + hvy),
    ]


def corners_from_corner_row(row: tuple[int, ...]) -> list[tuple[Fraction, Fraction]]:
    return [(F(row[4 * k], row[4 * k + 1]), F(row[4 * k + 2], row[4 * k + 3])) for k in range(4)]


class SatSquare:
    __slots__ = ("p", "e1", "e2", "own1", "own2", "minx", "maxx", "miny", "maxy", "unit", "sense")

    def __init__(self, p: list[tuple[Fraction, Fraction]]) -> None:
        self.p = p
        p0, p1, p2, p3 = p
        e1 = (p1[0] - p0[0], p1[1] - p0[1])
        e2 = (p3[0] - p0[0], p3[1] - p0[1])
        unit_len = e1[0] * e1[0] + e1[1] * e1[1] == 1
        perp_ccw = e2 == (-e1[1], e1[0])
        perp_cw = e2 == (e1[1], -e1[0])
        closes = p2 == (p0[0] + e1[0] + e2[0], p0[1] + e1[1] + e2[1])
        self.unit = bool(unit_len and (perp_ccw or perp_cw) and closes)
        self.sense = "ccw" if perp_ccw else ("cw" if perp_cw else "none")
        self.e1 = e1
        self.e2 = e2
        pr1 = [e1[0] * q[0] + e1[1] * q[1] for q in p]
        pr2 = [e2[0] * q[0] + e2[1] * q[1] for q in p]
        self.own1 = (min(pr1), max(pr1))
        self.own2 = (min(pr2), max(pr2))
        xs = [q[0] for q in p]
        ys = [q[1] for q in p]
        self.minx, self.maxx = min(xs), max(xs)
        self.miny, self.maxy = min(ys), max(ys)


def build(packing: Any) -> list[SatSquare]:
    if packing.kind == "cert":
        return [SatSquare(corners_from_cert_row(r)) for r in packing.squares]
    if packing.kind == "corners":
        return [SatSquare(corners_from_corner_row(r)) for r in packing.squares]
    raise ValueError(f"unknown kind {packing.kind!r}")


def _proj(w: tuple[Fraction, Fraction], pts: list[tuple[Fraction, Fraction]]) -> tuple[Fraction, Fraction]:
    a = w[0] * pts[0][0] + w[1] * pts[0][1]
    lo = hi = a
    for q in pts[1:]:
        v = w[0] * q[0] + w[1] * q[1]
        if v < lo:
            lo = v
        elif v > hi:
            hi = v
    return lo, hi


def pair_margin(a: SatSquare, b: SatSquare) -> tuple[Fraction, int]:
    """Largest projection gap over the four edge normals, and which normal gives it.

    Normal index: 0 = a.e1, 1 = a.e2, 2 = b.e1, 3 = b.e2.
    """
    best: Fraction | None = None
    arg = -1
    for k, (w, own, other) in enumerate(
        (
            (a.e1, a.own1, b.p),
            (a.e2, a.own2, b.p),
            (b.e1, b.own1, a.p),
            (b.e2, b.own2, a.p),
        )
    ):
        lo, hi = _proj(w, other)
        gap = lo - own[1]
        g2 = own[0] - hi
        if g2 > gap:
            gap = g2
        if best is None or gap > best:
            best = gap
            arg = k
    assert best is not None
    return best, arg


def wall_clearances(sq: SatSquare, side: Fraction) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    """(left, bottom, right, top) clearances of one square, exact."""
    return sq.minx, sq.miny, side - sq.maxx, side - sq.maxy


def classify(margin: Fraction) -> str:
    if margin > 0:
        return "apart"
    if margin == 0:
        return "touch"
    return "overlap"
