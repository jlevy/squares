"""Lane L105's construction helpers for the self-test and the controls.

Decides nothing. Builds squares as the reader's integer pairs from Fractions,
computes the exact centre-line move that brings a pair's separating-axis margin
to a target value, and the exact wall move that brings a clearance to a target.

The closing move: square j moves to c_i + (1 - lam) d, d = c_j - c_i. Along each
edge normal a with D_a = |a.d| > 0 the gap is D_a (1 - lam) - H_a, a decreasing
line in lam, H_a the two half-extents. The margin, their maximum, equals t first
at lam(t) = max_a (1 - (H_a + t) / D_a); axes with D_a = 0 have gap -H_a <= -1/2.
"""

from __future__ import annotations

from fractions import Fraction

Rat = tuple[int, int]
Sq = tuple[Rat, Rat, Rat, Rat]


def rat(v: Fraction) -> Rat:
    v = Fraction(v)
    return (v.numerator, v.denominator)


def fr(r: Rat) -> Fraction:
    return Fraction(r[0], r[1])


def sq(x: Fraction, y: Fraction, c: Fraction, s: Fraction) -> Sq:
    return (rat(x), rat(y), rat(c), rat(s))


def unpack(s: Sq) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    return fr(s[0]), fr(s[1]), fr(s[2]), fr(s[3])


def _half(c: Fraction, s: Fraction, ax: Fraction, ay: Fraction) -> Fraction:
    return (abs(ax * c + ay * s) + abs(-ax * s + ay * c)) / 2


def closing_lambda(si: Sq, sj: Sq, t: Fraction) -> Fraction:
    xi, yi, ci, s_i = unpack(si)
    xj, yj, cj, s_j = unpack(sj)
    dx, dy = xj - xi, yj - yi
    best: Fraction | None = None
    for ax, ay in ((ci, s_i), (-s_i, ci), (cj, s_j), (-s_j, cj)):
        D = abs(ax * dx + ay * dy)
        if D == 0:
            continue
        H = _half(ci, s_i, ax, ay) + _half(cj, s_j, ax, ay)
        lam = 1 - (H + t) / D
        if best is None or lam > best:
            best = lam
    assert best is not None
    return best


def close_pair(si: Sq, sj: Sq, t: Fraction) -> Sq:
    """Square j moved along the centre line so that the pair's margin is t."""
    lam = closing_lambda(si, sj, t)
    assert lam < 1, lam  # negative lam moves the pair apart
    xi, yi, _, _ = unpack(si)
    xj, yj, cj, s_j = unpack(sj)
    return sq(xi + (1 - lam) * (xj - xi), yi + (1 - lam) * (yj - yi), cj, s_j)


def half_extent_xy(s: Sq) -> Fraction:
    _, _, c, si = unpack(s)
    return (abs(c) + abs(si)) / 2


def move_to_wall(s: Sq, wall: str, side: Fraction, target: Fraction) -> Sq:
    """Square moved normal to `wall` so that its clearance there is `target`."""
    x, y, c, si = unpack(s)
    h = half_extent_xy(s)
    if wall == "left":
        x = target + h
    elif wall == "bottom":
        y = target + h
    elif wall == "right":
        x = side - h - target
    elif wall == "top":
        y = side - h - target
    else:
        raise ValueError(wall)
    return sq(x, y, c, si)


def pythagorean(m: int, n: int) -> tuple[Fraction, Fraction]:
    r = m * m + n * n
    return Fraction(m * m - n * n, r), Fraction(2 * m * n, r)
