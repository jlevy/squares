"""Lane r1052's third formulation: centres and half-widths in Python fractions.

It decides nothing. The controls use it to construct moved squares and to predict, as
exact fractions, the margins and clearances the two methods must then find; the check
uses it to recompute every margin and clearance a second way (control C0).

A pose is (cx, cy, ux, uy) with u a unit vector; v is its quarter turn.
"""

from __future__ import annotations

from fractions import Fraction

Pose = tuple[Fraction, Fraction, Fraction, Fraction]


def half_sum(p: Pose, r: Pose) -> Fraction:
    """H: the two projections' half-lengths added, the same on all four edge normals."""
    cos = p[2] * r[2] + p[3] * r[3]
    sin = p[2] * r[3] - p[3] * r[2]
    return Fraction(1, 2) + (abs(cos) + abs(sin)) / 2


def normals(p: Pose, r: Pose) -> list[tuple[Fraction, Fraction]]:
    return [(p[2], p[3]), (-p[3], p[2]), (r[2], r[3]), (-r[3], r[2])]


def margin(p: Pose, r: Pose) -> Fraction:
    dx, dy = r[0] - p[0], r[1] - p[1]
    h = half_sum(p, r)
    return max(abs(dx * wx + dy * wy) - h for wx, wy in normals(p, r))


def clearances(side: Fraction, p: Pose) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    h = (abs(p[2]) + abs(p[3])) / 2
    return (p[0] - h, p[1] - h, side - p[0] - h, side - p[1] - h)


def close_toward(p: Pose, r: Pose, target: Fraction) -> Pose:
    """Move r along the line of centres toward p until the margin is exactly ``target``.

    With d the centre difference, r moves to c_r - t d; on a normal w with d.w != 0 the
    separation is (1 - t)|d.w| - H, so the margin, the largest of them, first reaches
    the target at t = max over those normals of 1 - (target + H)/|d.w|.
    """
    dx, dy = r[0] - p[0], r[1] - p[1]
    h = half_sum(p, r)
    ts = []
    for wx, wy in normals(p, r):
        s = abs(dx * wx + dy * wy)
        if s != 0:
            ts.append(1 - (target + h) / s)
    t = max(ts)
    return (r[0] - t * dx, r[1] - t * dy, r[2], r[3])


def to_wall(side: Fraction, p: Pose, wall: int, beyond: Fraction) -> Pose:
    """Move p perpendicular to a wall (0 left, 1 bottom, 2 right, 3 top) until its
    clearance there is exactly ``-beyond``."""
    c = clearances(side, p)[wall]
    step = c + beyond
    x, y = p[0], p[1]
    if wall == 0:
        x -= step
    elif wall == 1:
        y -= step
    elif wall == 2:
        x += step
    else:
        y += step
    return (x, y, p[2], p[3])


def corners(p: Pose) -> list[tuple[Fraction, Fraction]]:
    """The corners c - u/2 - v/2, c + u/2 - v/2, c + u/2 + v/2, c - u/2 + v/2."""
    ux, uy = p[2] / 2, p[3] / 2
    vx, vy = -uy, ux
    cx, cy = p[0], p[1]
    return [
        (cx - ux - vx, cy - uy - vy),
        (cx + ux - vx, cy + uy - vy),
        (cx + ux + vx, cy + uy + vy),
        (cx - ux + vx, cy - uy + vy),
    ]


def seg_dist2(
    pt: tuple[Fraction, Fraction], a: tuple[Fraction, Fraction], b: tuple[Fraction, Fraction]
) -> Fraction:
    abx, aby = b[0] - a[0], b[1] - a[1]
    apx, apy = pt[0] - a[0], pt[1] - a[1]
    t = (apx * abx + apy * aby) / (abx * abx + aby * aby)
    t = min(max(t, Fraction(0)), Fraction(1))
    dx, dy = apx - t * abx, apy - t * aby
    return dx * dx + dy * dy
