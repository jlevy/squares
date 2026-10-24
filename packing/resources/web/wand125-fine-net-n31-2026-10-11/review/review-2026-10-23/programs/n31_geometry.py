"""Exact integer geometry for the capture check of review-2026-10-23 (mixed_n31_L59775).

Everything here is integer arithmetic on a fixed grid, with no division, written from
the mathematics for this review and sharing nothing with any other checker.

Frame. A direction has cos = C/E and sin = S/E (integers, C^2 + S^2 = E^2, C > 0,
S >= 0). Points are on a grid of step 1/G. The rotated, E-scaled coordinates of a grid
point (X, Y) are sigma = C X + S Y and omega = -S X + C Y: E times the coordinates along
u = (cos, sin) and v = (-sin, cos), in grid units. A core (a square of side B at the
direction's angle) or a kernel (a smaller rotated rectangle) is the box
[Slo, Shi] x [Wlo, Whi] in that frame; an axis-parallel rectangle of the measure is the
parallelogram with the four rotated corners.

Area. With A = alpha - u.q and B = beta - v.q, the region
{x >= qx, y >= qy, u.p <= alpha, v.p <= beta} is bounded for 0 <= theta <= pi/4 and has
area h(A, B):

    0                               if A <= 0 or sA + cB <= 0
    (sA + cB)^2 / (2cs)             if B <= 0 < sA + cB
    (sA^2 + 2cAB - sB^2) / (2c)     if 0 < B and cA - sB > 0
    A^2 / (2cs)                     if 0 < B and cA - sB <= 0

and for theta = 0, h = AB when A, B > 0. Inclusion-exclusion over the four corners of
the rectangle and the four corners of the box gives the exact area of their
intersection from sixteen values of h. area16 returns 2 C S E^2 G^2 times that area
(G^2 times it at theta = 0), an integer.

Chord. chord_sigma and chord_omega return C S E G times the length of a segment of a
line sigma = T (omega in [Wlo, Whi]) or omega = T (sigma in [Slo, Shi]) inside a
rectangle (G times it at theta = 0), an integer.
"""

from __future__ import annotations


def h_scaled(a: int, b: int, c: int, s: int, e2: int) -> int:
    """2 C S E^2 G^2 h(A, B) for S > 0, with a = E G A and b = E G B."""
    if a <= 0:
        return 0
    t1 = s * a + c * b
    if t1 <= 0:
        return 0
    if b <= 0:
        return t1 * t1
    if c * a - s * b <= 0:
        return e2 * a * a
    return s * (s * a * a + 2 * c * a * b - s * b * b)


def area16(corners, slo: int, shi: int, wlo: int, whi: int, c: int, s: int,
           e2: int) -> int:
    """Scaled area of (rectangle) intersect (box), from the rectangle's rotated corners.

    corners = ((s00, w00), (s10, w10), (s01, w01), (s11, w11)), the rotated
    coordinates of (x0, y0), (x1, y0), (x0, y1), (x1, y1).
    """
    (s00, w00), (s10, w10), (s01, w01), (s11, w11) = corners
    total = 0
    if s == 0:
        for sq, wq, sign in ((s00, w00, 1), (s10, w10, -1), (s01, w01, -1),
                             (s11, w11, 1)):
            part = 0
            for sv, ss in ((shi, 1), (slo, -1)):
                aa = sv - sq
                if aa <= 0:
                    continue
                for wv, ws in ((whi, 1), (wlo, -1)):
                    bb = wv - wq
                    if bb > 0:
                        part += ss * ws * aa * bb
            total += sign * part
        return total
    for sq, wq, sign in ((s00, w00, 1), (s10, w10, -1), (s01, w01, -1), (s11, w11, 1)):
        part = (h_scaled(shi - sq, whi - wq, c, s, e2)
                - h_scaled(slo - sq, whi - wq, c, s, e2)
                - h_scaled(shi - sq, wlo - wq, c, s, e2)
                + h_scaled(slo - sq, wlo - wq, c, s, e2))
        total += sign * part
    return total


def chord_sigma(t: int, wlo: int, whi: int, x0: int, x1: int, y0: int, y1: int,
                c: int, s: int, e2: int) -> int:
    """C S E G times the length of {sigma = t, wlo <= omega <= whi} inside the rectangle."""
    if s == 0:
        if not x0 <= t <= x1:
            return 0
        lo, hi = max(y0, wlo), min(y1, whi)
        return hi - lo if hi > lo else 0
    lo = max(c * (t * c - e2 * x1), s * (e2 * y0 - t * s), c * s * wlo)
    hi = min(c * (t * c - e2 * x0), s * (e2 * y1 - t * s), c * s * whi)
    return hi - lo if hi > lo else 0


def chord_omega(t: int, slo: int, shi: int, x0: int, x1: int, y0: int, y1: int,
                c: int, s: int, e2: int) -> int:
    """C S E G times the length of {omega = t, slo <= sigma <= shi} inside the rectangle."""
    if s == 0:
        if not y0 <= t <= y1:
            return 0
        lo, hi = max(x0, slo), min(x1, shi)
        return hi - lo if hi > lo else 0
    lo = max(s * (e2 * x0 + t * s), c * (e2 * y0 - t * c), c * s * slo)
    hi = min(s * (e2 * x1 + t * s), c * (e2 * y1 - t * c), c * s * shi)
    return hi - lo if hi > lo else 0
