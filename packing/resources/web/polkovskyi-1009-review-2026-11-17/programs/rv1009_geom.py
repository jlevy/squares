"""Closed forms for the self-test and the controls. Decides nothing.

Lane c-review-1009-1117, stage 4 blind review of issue #1009. Clean-room.

A packing here is a list of rows ``(x, y, t)`` of ``fractions.Fraction``: the centre and
the half-angle tangent of form P. This module moves rows (a pair closed along its centre
line, a square taken to a wall, the whole packing contracted or translated), and it
recomputes a pair's margin a third way, from the projections of the eight corners on the
four edge directions, which neither method uses: method A projects centres and adds
half-lengths, and method B clips.
"""

from __future__ import annotations

from fractions import Fraction

from gmpy2 import mpq

Row = tuple[Fraction, Fraction, Fraction]
PAST = Fraction(1, 10**40)


def direction(t: Fraction) -> tuple[Fraction, Fraction]:
    """(cos, sin) of the angle ``2*atan(t)``."""
    den = 1 + t * t
    return (1 - t * t) / den, 2 * t / den


def half_extent(t: Fraction) -> Fraction:
    """Half the width of the square on either coordinate axis."""
    c, s = direction(t)
    return (abs(c) + abs(s)) / 2


def corners(row: Row) -> tuple[tuple[Fraction, Fraction], ...]:
    """Four corners, counterclockwise, of the square of a row."""
    x, y, t = row
    c, s = direction(t)
    px, py = (c + s) / 2, (s - c) / 2
    qx, qy = (c - s) / 2, (s + c) / 2
    return ((x - qx, y - qy), (x + px, y + py), (x + qx, y + qy), (x - px, y - py))


def clearances(row: Row, side: Fraction) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    """(left, bottom, right, top) by centre and half-extent."""
    x, y, t = row
    h = half_extent(t)
    return x - h, y - h, side - x - h, side - y - h


def pair_terms(ri: Row, rj: Row) -> tuple[list[Fraction], Fraction]:
    """``(projs, H)``: the four ``|d.w|`` on the edge normals of the two squares, and the
    sum ``H`` of the two half-lengths, which is the same on all four."""
    xi, yi, ti = ri
    xj, yj, tj = rj
    ci, si = direction(ti)
    cj, sj = direction(tj)
    dx, dy = xj - xi, yj - yi
    cosd = ci * cj + si * sj
    sind = ci * sj - si * cj
    h = Fraction(1, 2) + (abs(cosd) + abs(sind)) / 2
    projs = [
        abs(dx * ci + dy * si),
        abs(dy * ci - dx * si),
        abs(dx * cj + dy * sj),
        abs(dy * cj - dx * sj),
    ]
    return projs, h


def margin(ri: Row, rj: Row) -> Fraction:
    """The margin by centres and half-lengths, in Fractions."""
    projs, h = pair_terms(ri, rj)
    return max(projs) - h


def corner_margin(qi: object, qj: object) -> Fraction:
    """The margin a third way: on each of the four edge directions of two unit squares
    given by their corners (as Fractions), the gap between the two sets of four
    projections. The sums are taken in GMP rationals, which are exact, for speed."""
    a = [(mpq(p[0].numerator, p[0].denominator), mpq(p[1].numerator, p[1].denominator)) for p in qi]  # type: ignore[union-attr]
    b = [(mpq(p[0].numerator, p[0].denominator), mpq(p[1].numerator, p[1].denominator)) for p in qj]  # type: ignore[union-attr]
    best = None
    for quad in (a, b):
        for k in (0, 1):
            wx = quad[k + 1][0] - quad[k][0]
            wy = quad[k + 1][1] - quad[k][1]
            pa = [p[0] * wx + p[1] * wy for p in a]
            pb = [p[0] * wx + p[1] * wy for p in b]
            gap = max(min(pb) - max(pa), min(pa) - max(pb))
            if best is None or gap > best:
                best = gap
    assert best is not None
    return Fraction(int(best.numerator), int(best.denominator))


def close_pair(ri: Row, rj: Row, target: Fraction) -> tuple[Row, Fraction]:
    """Square j moved along the line of centres until the pair's margin is ``target``.

    With the centre difference scaled by ``s`` every ``|d.w|`` scales by ``s`` and ``H``
    does not change, so the margin is ``max_w(s*|d.w|) - H``, and it equals ``target`` at
    ``s = (target + H) / max_w |d.w|``. Returns the moved row and ``s``.
    """
    projs, h = pair_terms(ri, rj)
    top = max(projs)
    if top == 0:
        msg = "coincident centres"
        raise ValueError(msg)
    if target + h <= 0:
        msg = "target margin below the least possible"
        raise ValueError(msg)
    s = (target + h) / top
    xi, yi, _ti = ri
    xj, yj, tj = rj
    return (xi + s * (xj - xi), yi + s * (yj - yi), tj), s


def contact_scale_pair(ri: Row, rj: Row) -> Fraction:
    """The factor of a uniform contraction about the origin at which the pair first
    touches: its margin at factor ``g`` is ``g*max_w|d.w| - H``."""
    projs, h = pair_terms(ri, rj)
    top = max(projs)
    if top == 0:
        msg = "coincident centres"
        raise ValueError(msg)
    return h / top


def contact_scale_walls(row: Row, side: Fraction) -> tuple[Fraction, ...]:
    """The factors at which the square first touches (left, bottom, right, top) when
    centres and side are scaled together about the origin."""
    x, y, t = row
    h = half_extent(t)
    out = []
    for dist in (x, y, side - x, side - y):
        if dist <= 0:
            msg = "centre on or outside a wall"
            raise ValueError(msg)
        out.append(h / dist)
    return tuple(out)


def scaled(rows: list[Row], factor: Fraction) -> list[Row]:
    return [(x * factor, y * factor, t) for x, y, t in rows]


def translated(rows: list[Row], dx: Fraction, dy: Fraction) -> list[Row]:
    return [(x + dx, y + dy, t) for x, y, t in rows]


def transposed_t(t: Fraction) -> Fraction:
    """The half-angle tangent of the reflected direction ``(sin, cos)``; a square turned
    by 90 degrees less its angle. ``t = -1`` (a square at -90 degrees, which is upright)
    maps to 0."""
    if t == -1:
        return Fraction(0)
    return (1 - t) / (1 + t)
