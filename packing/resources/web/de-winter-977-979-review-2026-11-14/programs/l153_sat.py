"""Lane L153 method A: separating axes in Python integers.

Clean-room: written for this review, importing nothing from this repository or the
source, and reusing no code of any earlier review.

A square is read as its centre C and its edge direction u = (c, s); its other edge
direction is v = (-s, c), and its points are C + x u + y v with |x|, |y| <= 1/2.

Per square, the centre is written over one denominator E (C = (X, Y) / E) and the
direction over one denominator r (u = (a, b) / r). The square is a unit square exactly
when a^2 + b^2 = r^2, which makes u and v exact rational unit vectors.

For a pair (i, j) and a unit normal w of square k (k in {i, j}, w in {u_k, v_k}), the
projection of square k on w has half-length 1/2, and that of the other square o has
half-length (|u_o . w| + |v_o . w|) / 2. The gap is |(C_o - C_k) . w| minus both
half-lengths, an exact Euclidean distance along w. All four gaps of a pair share the
denominator 2 E_i E_j r_i r_j, so the margin, their maximum, is decided on integers and
kept as an exact Fraction. Positive is apart, zero is contact with disjoint interiors,
negative is overlap: two convex polygons have disjoint interiors exactly when a line
parallel to an edge of one of them weakly separates them.

A wall clearance is the signed distance from the square's extreme corner to the wall:
the square's half-extent along x and along y is (|a| + |b|) / (2 r).
"""

from __future__ import annotations

from fractions import Fraction
from math import lcm

Pair = tuple[int, int]
Square = tuple[Pair, Pair, Pair, Pair]
Prepared = tuple[int, int, int, int, int, int]

WALLS = ("left", "right", "bottom", "top")


def prepare(square: Square) -> Prepared:
    """(X, Y, E, a, b, r) with C = (X, Y) / E and u = (a, b) / r."""
    (px, qx), (py, qy), (pc, qc), (ps, qs) = square
    e = lcm(qx, qy)
    r = lcm(qc, qs)
    return px * (e // qx), py * (e // qy), e, pc * (r // qc), ps * (r // qs), r


def is_unit(sq: Prepared) -> bool:
    _, _, _, a, b, r = sq
    return a * a + b * b == r * r


def _gap_numerator(k: Prepared, o: Prepared, wa: int, wb: int) -> int:
    """Numerator over 2 E_k E_o r_k r_o of the gap along w = (wa, wb) / r_k."""
    xk, yk, ek, _, _, rk = k
    xo, yo, eo, ao, bo, ro = o
    centre = (xo * ek - xk * eo) * wa + (yo * ek - yk * eo) * wb
    other = abs(ao * wa + bo * wb) + abs(ao * wb - bo * wa)
    return 2 * ro * abs(centre) - ek * eo * (ro * rk + other)


def margin(i: Prepared, j: Prepared) -> Fraction:
    """The pair's exact margin: the largest projection gap over the four normals."""
    _, _, ei, ai, bi, ri = i
    _, _, ej, aj, bj, rj = j
    best = max(
        _gap_numerator(i, j, ai, bi),
        _gap_numerator(i, j, -bi, ai),
        _gap_numerator(j, i, aj, bj),
        _gap_numerator(j, i, -bj, aj),
    )
    return Fraction(best, 2 * ei * ej * ri * rj)


def clearances(sq: Prepared, side: Fraction) -> dict[str, Fraction]:
    """Signed distance from the square's extreme corner to each wall of [0, side]^2."""
    x, y, e, a, b, r = sq
    half = Fraction(abs(a) + abs(b), 2 * r)
    cx = Fraction(x, e)
    cy = Fraction(y, e)
    return {
        "left": cx - half,
        "right": side - cx - half,
        "bottom": cy - half,
        "top": side - cy - half,
    }


def classify(value: Fraction) -> str:
    if value > 0:
        return "apart"
    if value == 0:
        return "contact"
    return "overlap"
