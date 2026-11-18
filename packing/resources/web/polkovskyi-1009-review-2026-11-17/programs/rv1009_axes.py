"""Method A: separating axes in Python integers, from poses.

Lane c-review-1009-1117, stage 4 blind review of issue #1009. Clean-room.

A pose is six integers ``(X, Y, E, a, b, r)``: the centre is ``(X/E, Y/E)`` with
``E > 0``, and one edge direction is the unit vector ``u = (a/r, b/r)`` with ``r > 0``
and ``a*a + b*b == r*r``. The square is ``{C + s*u + t*v : |s|, |t| <= 1/2}`` with
``v = (-b/r, a/r)``.

Its projection on any unit vector ``w`` is an interval about ``C.w`` of half-length
``(|u.w| + |v.w|)/2``. On an edge normal of its own that is ``1/2``; on an edge normal of
another square turned by ``D`` from it, ``(|cos D| + |sin D|)/2``. For a pair the sum of
the two half-lengths is therefore the same number ``H`` on all four edge normals, and the
separation on the normal ``w`` is ``|d.w| - H`` with ``d`` the centre difference. The
margin is the greatest of the four separations: positive is apart, zero is contact with
disjoint interiors, negative is overlap, since two convex polygons have disjoint
interiors exactly when a line parallel to an edge of one of them weakly separates them.

Everything is decided on integers; a margin or clearance is returned as an exact
``fractions.Fraction``.
"""

from __future__ import annotations

import math
from fractions import Fraction

Pose = tuple[int, int, int, int, int, int]


def pose_from_xyt(x: tuple[int, int], y: tuple[int, int], t: tuple[int, int]) -> Pose:
    """The pose of a row ``x y t`` of form P, read as centre and half-angle tangent.

    With ``t = p/q`` the edge direction is ``((q*q - p*p)/(q*q + p*p), 2*p*q/(q*q + p*p))``,
    the point of the unit circle at angle ``2*atan(t)`` counterclockwise from the x-axis.
    """
    (xn, xd), (yn, yd), (p, q) = x, y, t
    if xd <= 0 or yd <= 0 or q <= 0:
        msg = "non-positive denominator"
        raise ValueError(msg)
    e = xd * yd // math.gcd(xd, yd)
    return (xn * (e // xd), yn * (e // yd), e, q * q - p * p, 2 * p * q, q * q + p * p)


def is_unit_pose(pose: Pose) -> bool:
    """Whether the six integers are a pose: positive scales and a unit direction."""
    _x, _y, e, a, b, r = pose
    return e > 0 and r > 0 and a * a + b * b == r * r


def wall_clearances(pose: Pose, side: tuple[int, int]) -> tuple[Fraction, ...]:
    """Signed distances (left, bottom, right, top) from the square to the walls of
    ``[0, S]^2``: positive inside, zero touching, negative crossing."""
    x, y, e, a, b, r = pose
    sn, sd = side
    # half-extent on either coordinate axis: (|a| + |b|) / (2r)
    hn = abs(a) + abs(b)
    den = 2 * e * r * sd
    left = 2 * x * r * sd - hn * e * sd
    bottom = 2 * y * r * sd - hn * e * sd
    right = 2 * sn * e * r - 2 * x * r * sd - hn * e * sd
    top = 2 * sn * e * r - 2 * y * r * sd - hn * e * sd
    return (
        Fraction(left, den),
        Fraction(bottom, den),
        Fraction(right, den),
        Fraction(top, den),
    )


def pair_numbers(pi: Pose, pj: Pose) -> tuple[tuple[int, int, int, int], int, int]:
    """The integers behind a pair's margin.

    Returns ``(proj, k, den)``: the four separations are ``(proj[m] - k) / den`` for the
    edge normals ``u_i, v_i, u_j, v_j`` in that order, ``den > 0``.
    """
    xi, yi, ei, ai, bi, ri = pi
    xj, yj, ej, aj, bj, rj = pj
    dx = xj * ei - xi * ej
    dy = yj * ei - yi * ej
    ee = ei * ej
    cosn = ai * aj + bi * bj
    sinn = ai * bj - bi * aj
    k = ee * (ri * rj + abs(cosn) + abs(sinn))
    proj = (
        2 * rj * abs(dx * ai + dy * bi),
        2 * rj * abs(dy * ai - dx * bi),
        2 * ri * abs(dx * aj + dy * bj),
        2 * ri * abs(dy * aj - dx * bj),
    )
    return proj, k, 2 * ee * ri * rj


def pair_margin(pi: Pose, pj: Pose) -> Fraction:
    """The margin of a pair: the greatest of its four separations, exactly."""
    proj, k, den = pair_numbers(pi, pj)
    return Fraction(max(proj) - k, den)


def pair_sign(pi: Pose, pj: Pose) -> int:
    """The sign of the margin: 1 apart, 0 contact, -1 overlap."""
    proj, k, _den = pair_numbers(pi, pj)
    top = max(proj) - k
    return (top > 0) - (top < 0)
