"""Constructions and closed forms for the self-test and the controls. Decides nothing.

Lane L127, clean room.

A placed unit square is (cx, cy, c, s): centre (cx, cy), axes u = (c, s) and
w = (-s, c), with c^2 + s^2 = 1, all Fractions. Its projection on a unit axis a is the
interval centred at (cx, cy).a of half-width h(a) = (|a.u| + |a.w|) / 2, so the
projection gap of two squares on a is |(c2 - c1).a| - h1(a) - h2(a). The closed-form
margin is the largest of those gaps over the four axes u1, w1, u2, w2; it uses centres
and half-widths only, never corners.

Moving square 2 towards square 1 along their centre line, c2(t) = c2 - t (c2 - c1), the
gap on axis a is |d.a| (1 - t) - H(a) with d = c2 - c1, which is zero at
t_a = 1 - H(a) / |d.a|; the margin is zero at t* = max over axes of t_a, and the axes
attaining it are the binding ones.
"""

from __future__ import annotations

from fractions import Fraction as F
from typing import NamedTuple


class Placed(NamedTuple):
    cx: F
    cy: F
    c: F
    s: F


def pythagorean(m: int, n: int) -> tuple[F, F]:
    """(c, s) = ((m^2 - n^2), 2mn) / (m^2 + n^2)."""
    r = m * m + n * n
    return F(m * m - n * n, r), F(2 * m * n, r)


def corners(sq: Placed, *, ccw: bool = True, start: int = 0) -> list[tuple[F, F]]:
    """The four corners in cyclic order, starting at `start` of the ccw list."""
    half = F(1, 2)
    local = [(-half, -half), (half, -half), (half, half), (-half, half)]
    pts = [(sq.cx + sq.c * x - sq.s * y, sq.cy + sq.s * x + sq.c * y) for x, y in local]
    if not ccw:
        pts = [pts[0], pts[3], pts[2], pts[1]]
    return pts[start:] + pts[:start]


def to_reader(pts: list[tuple[F, F]]) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    return [((x.numerator, x.denominator), (y.numerator, y.denominator)) for x, y in pts]


def axes(sq: Placed) -> list[tuple[F, F]]:
    return [(sq.c, sq.s), (-sq.s, sq.c)]


def half_width(sq: Placed, a: tuple[F, F]) -> F:
    u, w = axes(sq)
    return (abs(a[0] * u[0] + a[1] * u[1]) + abs(a[0] * w[0] + a[1] * w[1])) / 2


def closed_margin(p: Placed, q: Placed) -> F:
    dx, dy = q.cx - p.cx, q.cy - p.cy
    best: F | None = None
    for a in axes(p) + axes(q):
        g = abs(dx * a[0] + dy * a[1]) - half_width(p, a) - half_width(q, a)
        if best is None or g > best:
            best = g
    assert best is not None
    return best


class Closing(NamedTuple):
    t_star: F  # contact time
    binding_rates: list[F]  # |d.a| for the binding axes
    other_slack: F  # least |gap_a(t*)| over the non-binding axes (or 1 if none)


def closing(p: Placed, q: Placed) -> Closing:
    """Contact time moving q towards p along the centre line."""
    dx, dy = q.cx - p.cx, q.cy - p.cy
    ts: list[tuple[F, F, F]] = []  # (t_a, rate, H)
    for a in axes(p) + axes(q):
        rate = abs(dx * a[0] + dy * a[1])
        h = half_width(p, a) + half_width(q, a)
        if rate == 0:
            continue
        ts.append((1 - h / rate, rate, h))
    t_star = max(t for t, _, _ in ts)
    binding = [r for t, r, _ in ts if t == t_star]
    slack = [abs(r * (1 - t_star) - h) for t, r, h in ts if t != t_star]
    return Closing(t_star, binding, min(slack) if slack else F(1))


def moved(q: Placed, p: Placed, t: F) -> Placed:
    """q moved towards p by fraction t of their centre separation."""
    return Placed(q.cx - t * (q.cx - p.cx), q.cy - t * (q.cy - p.cy), q.c, q.s)
