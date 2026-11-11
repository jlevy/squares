"""Lane L109's geometry helper: builds squares and moves for the self-test and controls.

It decides nothing. It makes unit squares from a centre and a rational rotation, moves
squares, and computes, for two squares, the exact time at which one of them, moved
along the line of their centres, first touches the other, and the time at which it is
a given distance past that contact. Both times are exact rationals: each projection gap
of the pair is linear in the time, and the contact time is the largest root among the
gaps that close.

All arithmetic is ``fractions.Fraction``. Imports nothing from the repository.
"""

from __future__ import annotations

from fractions import Fraction as Q

Pt = tuple[Q, Q]


def square(cx: Q, cy: Q, c: Q, s: Q, ccw: bool = True, start: int = 0) -> list[Pt]:
    """A unit square centred at (cx, cy), turned by the rotation (c, s), c^2 + s^2 = 1."""
    assert c * c + s * s == 1
    h = Q(1, 2)
    local = [(-h, -h), (h, -h), (h, h), (-h, h)]
    if not ccw:
        local = [local[0], local[3], local[2], local[1]]
    pts = [(cx + c * x - s * y, cy + s * x + c * y) for x, y in local]
    return pts[start:] + pts[:start]


def translate(pts: list[Pt], dx: Q, dy: Q) -> list[Pt]:
    return [(x + dx, y + dy) for x, y in pts]


def centre(pts: list[Pt]) -> Pt:
    return (sum((p[0] for p in pts), Q(0)) / 4, sum((p[1] for p in pts), Q(0)) / 4)


def _dirs(pts: list[Pt]) -> list[Pt]:
    u = (pts[1][0] - pts[0][0], pts[1][1] - pts[0][1])
    return [u, (-u[1], u[0])]


def _proj(pts: list[Pt], ax: Pt) -> tuple[Q, Q]:
    v = [ax[0] * p[0] + ax[1] * p[1] for p in pts]
    return min(v), max(v)


def gap_lines(a: list[Pt], b: list[Pt], d: Pt) -> list[tuple[Q, Q]]:
    """Each projection gap of (a, b + t d) as (value at t = 0, slope in t)."""
    lines = []
    for ax in _dirs(a) + _dirs(b):
        lo_a, hi_a = _proj(a, ax)
        lo_b, hi_b = _proj(b, ax)
        sl = ax[0] * d[0] + ax[1] * d[1]
        lines.append((lo_b - hi_a, sl))
        lines.append((lo_a - hi_b, -sl))
    return lines


def close_along_centres(a: list[Pt], b: list[Pt], past: Q = Q(0)) -> dict[str, object]:
    """Move b toward a along the centre line: exact contact time, and the time `past` beyond it.

    Returns the direction d = centre(a) - centre(b), the contact time t0, the time t1
    at which the largest gap is exactly -past (t1 = t0 when past is 0), the slope of the
    binding gap, and the Euclidean length of the move to t0 as its exact square.
    """
    ca, cb = centre(a), centre(b)
    d = (ca[0] - cb[0], ca[1] - cb[1])
    lines = gap_lines(a, b, d)
    m0 = max(g for g, _ in lines)
    if m0 <= 0:
        raise ValueError("the pair is not apart")
    roots = [-g / s for g, s in lines if s < 0]
    t0 = max(roots)
    at0 = [g + s * t0 for g, s in lines]
    if max(at0) != 0:
        raise ValueError("no exact contact on the centre line")
    binding = [s for (g, s), v in zip(lines, at0, strict=True) if v == 0]
    slope = max(binding)  # the binding gap that falls slowest
    t1 = t0 if past == 0 else t0 + past / (-slope)
    m1 = max(g + s * t1 for g, s in lines)
    return {
        "d": d,
        "t0": t0,
        "t1": t1,
        "margin_at_t1": m1,
        "slope": slope,
        "len2_t0": t0 * t0 * (d[0] * d[0] + d[1] * d[1]),
        "len2_t1": t1 * t1 * (d[0] * d[0] + d[1] * d[1]),
    }


def moved(b: list[Pt], d: Pt, t: Q) -> list[Pt]:
    return translate(b, d[0] * t, d[1] * t)


def to_wall(pts: list[Pt], wall: str, clearance: Q, past: Q = Q(0)) -> list[Pt]:
    """Move a square toward a wall by its clearance plus `past`."""
    m = clearance + past
    if wall == "left":
        return translate(pts, -m, Q(0))
    if wall == "right":
        return translate(pts, m, Q(0))
    if wall == "bottom":
        return translate(pts, Q(0), -m)
    if wall == "top":
        return translate(pts, Q(0), m)
    raise ValueError(wall)
