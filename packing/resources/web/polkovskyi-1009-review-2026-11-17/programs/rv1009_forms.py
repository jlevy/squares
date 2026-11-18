"""The two forms of a square, and whether two listings are the same square.

Lane c-review-1009-1117, stage 4 blind review of issue #1009. Clean-room.

Form P gives a row ``x y t``; form C gives four corners. This module writes each in the
other's terms, in ``fractions.Fraction``, so that each method can be run on the form it
does not read natively, and so that the two files of one count can be compared square by
square. It decides nothing about a packing.
"""

from __future__ import annotations

import math
from fractions import Fraction

Corner = tuple[Fraction, Fraction]


def fraction(pair: tuple[int, int]) -> Fraction:
    return Fraction(pair[0], pair[1])


def corners_from_xyt(
    x: tuple[int, int], y: tuple[int, int], t: tuple[int, int]
) -> tuple[Corner, ...]:
    """The four corners, counterclockwise, of the unit square with centre ``(x, y)`` and
    an edge at angle ``2*atan(t)`` counterclockwise from the x-axis."""
    cx, cy, tt = fraction(x), fraction(y), fraction(t)
    den = 1 + tt * tt
    c = (1 - tt * tt) / den
    s = 2 * tt / den
    # half-edge vectors u/2 = (c, s)/2 and v/2 = (-s, c)/2
    px, py = (c + s) / 2, (s - c) / 2  # (u - v)/2
    qx, qy = (c - s) / 2, (s + c) / 2  # (u + v)/2
    return (
        (cx - qx, cy - qy),
        (cx + px, cy + py),
        (cx + qx, cy + qy),
        (cx - px, cy - py),
    )


def pose_from_corners(quad: object) -> tuple[tuple[int, int, int, int, int, int], int]:
    """The pose ``(X, Y, E, a, b, r)`` of four corners that are a unit square, and the
    sense of their listing (+1 counterclockwise, -1 clockwise).

    Raises ValueError unless the corners are exactly ``C -/+ u/2 -/+ v/2`` in cyclic
    order for a unit vector ``u`` and ``v`` its quarter turn either way.
    """
    pts = [(fraction(p[0]), fraction(p[1])) for p in quad]  # type: ignore[union-attr]
    if len(pts) != 4:
        msg = "not four corners"
        raise ValueError(msg)
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = pts
    ux, uy = x1 - x0, y1 - y0
    if ux * ux + uy * uy != 1:
        msg = "first edge is not of length 1"
        raise ValueError(msg)
    wx, wy = x3 - x0, y3 - y0
    if (wx, wy) == (-uy, ux):
        sense = 1
    elif (wx, wy) == (uy, -ux):
        sense = -1
    else:
        msg = "fourth corner is not a quarter turn of the first edge"
        raise ValueError(msg)
    if (x2, y2) != (x1 + wx, y1 + wy):
        msg = "third corner does not close the square"
        raise ValueError(msg)
    cx, cy = (x0 + x2) / 2, (y0 + y2) / 2
    e = cx.denominator * cy.denominator // math.gcd(cx.denominator, cy.denominator)
    r = ux.denominator * uy.denominator // math.gcd(ux.denominator, uy.denominator)
    pose = (
        cx.numerator * (e // cx.denominator),
        cy.numerator * (e // cy.denominator),
        e,
        ux.numerator * (r // ux.denominator),
        uy.numerator * (r // uy.denominator),
        r,
    )
    return pose, sense


def same_square(one: object, two: object) -> tuple[int, int] | None:
    """Whether two listings of four corners are one square: the offset and sense
    ``(k, s)`` with ``two[m] == one[(k + s*m) % 4]`` for all m, or None."""
    a = [(fraction(p[0]), fraction(p[1])) for p in one]  # type: ignore[union-attr]
    b = [(fraction(p[0]), fraction(p[1])) for p in two]  # type: ignore[union-attr]
    if len(a) != 4 or len(b) != 4:
        return None
    for sense in (1, -1):
        for k in range(4):
            if all(b[m] == a[(k + sense * m) % 4] for m in range(4)):
                return k, sense
    return None


def pairs_of(corners: tuple[Corner, ...]) -> tuple[tuple[tuple[int, int], tuple[int, int]], ...]:
    """Fractions back to ``(numerator, denominator)`` pairs, as the readers give them."""
    return tuple(
        ((p[0].numerator, p[0].denominator), (p[1].numerator, p[1].denominator)) for p in corners
    )
