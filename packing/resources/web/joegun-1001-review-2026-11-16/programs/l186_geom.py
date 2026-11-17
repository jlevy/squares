"""Lane L186: a closed form by centres and half-extents, in `fractions`.

It decides nothing on its own. The controls use it to compute exact moves
(closing a pair along its centre line, taking a square to a wall) and as a third
formulation of the margins and clearances, checked against method A.

A unit square with corners P0..P3 has centre c = (P0 + P2) / 2 and unit edge
directions u = P1 - P0 and v = P3 - P0. Its projection on a unit vector w is
the interval c.w -+ h(w), with h(w) = (|u.w| + |v.w|) / 2, since a square is
centrally symmetric. The gap of a pair on w is |(c_j - c_i).w| - h_i(w) - h_j(w),
and the margin is the greatest gap over the four normals u_i, v_i, u_j, v_j.

Closing a pair along its centre line: with d = c_j - c_i, moving square j to
c_j - t d makes every gap (1 - t)|d.w| - H_w, a decreasing line in t; the
margin equals a target m (0 or negative, above -1/2) exactly at
t* = max over normals with d.w != 0 of 1 - (m + H_w) / |d.w|.
"""

from __future__ import annotations

from fractions import Fraction

from l186_reader import Point, Square


def centre(sq: Square) -> Point:
    return ((sq[0][0] + sq[2][0]) / 2, (sq[0][1] + sq[2][1]) / 2)


def dirs(sq: Square) -> tuple[Point, Point]:
    u = (sq[1][0] - sq[0][0], sq[1][1] - sq[0][1])
    v = (sq[3][0] - sq[0][0], sq[3][1] - sq[0][1])
    return u, v


def dot(a: Point, b: Point) -> Fraction:
    return a[0] * b[0] + a[1] * b[1]


def half(sq: Square, w: Point) -> Fraction:
    u, v = dirs(sq)
    return (abs(dot(u, w)) + abs(dot(v, w))) / 2


def normals(si: Square, sj: Square) -> list[Point]:
    ui, vi = dirs(si)
    uj, vj = dirs(sj)
    return [ui, vi, uj, vj]


def margin(si: Square, sj: Square) -> Fraction:
    ci, cj = centre(si), centre(sj)
    d = (cj[0] - ci[0], cj[1] - ci[1])
    return max(abs(dot(d, w)) - half(si, w) - half(sj, w) for w in normals(si, sj))


def clearances(sq: Square, side: Fraction) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    c = centre(sq)
    hx = half(sq, (Fraction(1), Fraction(0)))
    hy = half(sq, (Fraction(0), Fraction(1)))
    return (c[0] - hx, c[1] - hy, side - c[0] - hx, side - c[1] - hy)


def closing_time(si: Square, sj: Square, target: Fraction) -> Fraction:
    ci, cj = centre(si), centre(sj)
    d = (cj[0] - ci[0], cj[1] - ci[1])
    best: Fraction | None = None
    for w in normals(si, sj):
        rate = abs(dot(d, w))
        if rate == 0:
            continue
        t = 1 - (target + half(si, w) + half(sj, w)) / rate
        if best is None or t > best:
            best = t
    if best is None:
        raise ValueError("coincident centres")
    return best


def translate(sq: Square, dx: Fraction, dy: Fraction) -> Square:
    p = [(x + dx, y + dy) for x, y in sq]
    return (p[0], p[1], p[2], p[3])


def close_pair(si: Square, sj: Square, target: Fraction) -> tuple[Square, Fraction]:
    """Square j moved toward square i along the centre line; and the move's squared length."""
    t = closing_time(si, sj, target)
    ci, cj = centre(si), centre(sj)
    d = (cj[0] - ci[0], cj[1] - ci[1])
    moved = translate(sj, -t * d[0], -t * d[1])
    return moved, t * t * dot(d, d)


WALL_DIR = {
    "left": (Fraction(-1), Fraction(0)),
    "bottom": (Fraction(0), Fraction(-1)),
    "right": (Fraction(1), Fraction(0)),
    "top": (Fraction(0), Fraction(1)),
}


def to_wall(sq: Square, wall: str, distance: Fraction) -> Square:
    """Square moved toward a wall, perpendicular to it, by a distance."""
    dx, dy = WALL_DIR[wall]
    return translate(sq, dx * distance, dy * distance)
