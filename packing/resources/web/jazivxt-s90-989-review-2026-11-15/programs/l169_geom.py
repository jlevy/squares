"""Lane L169 closed form: margins and clearances by projecting corners, in `fractions`.

A third formulation, apart from both methods: a square is (cx, cy, c, s) with (c, s) a
rational unit vector, its corners are C +- u/2 +- v/2, and on each of the four edge
normals of a pair the gap is the larger of (min of j's corner projections - max of i's)
and (min of i's - max of j's); the margin is the largest of the four gaps. A wall
clearance is the distance from the extreme corner coordinate to the wall.

It decides nothing about the certificate. The self-test holds the methods to it, and the
plan states its outcomes from it, with the closing moves below.
"""

from __future__ import annotations

from fractions import Fraction as F

Sq = tuple[F, F, F, F]  # cx, cy, cos, sin


def cs_of_t(t: F) -> tuple[F, F]:
    d = 1 + t * t
    return (1 - t * t) / d, 2 * t / d


def sq_of(cx: F, cy: F, t: F) -> Sq:
    c, s = cs_of_t(t)
    return (F(cx), F(cy), c, s)


def corners(q: Sq) -> list[tuple[F, F]]:
    cx, cy, c, s = q
    h = F(1, 2)
    ux, uy, vx, vy = c * h, s * h, -s * h, c * h
    return [
        (cx - ux - vx, cy - uy - vy),
        (cx + ux - vx, cy + uy - vy),
        (cx + ux + vx, cy + uy + vy),
        (cx - ux + vx, cy - uy + vy),
    ]


def axes(qi: Sq, qj: Sq) -> list[tuple[F, F]]:
    return [(qi[2], qi[3]), (-qi[3], qi[2]), (qj[2], qj[3]), (-qj[3], qj[2])]


def gaps(qi: Sq, qj: Sq) -> list[F]:
    ci, cj = corners(qi), corners(qj)
    out = []
    for nx, ny in axes(qi, qj):
        pi = [nx * x + ny * y for x, y in ci]
        pj = [nx * x + ny * y for x, y in cj]
        out.append(max(min(pj) - max(pi), min(pi) - max(pj)))
    return out


def margin(qi: Sq, qj: Sq) -> F:
    return max(gaps(qi, qj))


def clearances(q: Sq, side: F) -> dict[str, F]:
    cs = corners(q)
    xs = [x for x, _ in cs]
    ys = [y for _, y in cs]
    return {"left": min(xs), "right": side - max(xs), "bottom": min(ys), "top": side - max(ys)}


def close_time(qi: Sq, qj: Sq, target: F) -> F:
    """The time tau at which moving C_j by -tau (C_j - C_i) makes the pair's margin
    exactly `target`: tau = max over the normals n with n.d != 0 of (g_n - target) / |n.d|,
    where g_n is the gap on n now and d = C_j - C_i (each gap falls at rate |n.d|)."""
    dx, dy = qj[0] - qi[0], qj[1] - qi[1]
    g = gaps(qi, qj)
    best = None
    for (nx, ny), gn in zip(axes(qi, qj), g, strict=True):
        rate = abs(nx * dx + ny * dy)
        if rate == 0:
            if gn > target:
                raise ValueError("a normal with no rate cannot reach the target")
            continue
        tau = (gn - target) / rate
        best = tau if best is None else max(best, tau)
    if best is None or best >= 1:
        raise ValueError("no closing time below 1")
    return best


def moved_toward(qi: Sq, qj: Sq, tau: F) -> Sq:
    dx, dy = qj[0] - qi[0], qj[1] - qi[1]
    return (qj[0] - tau * dx, qj[1] - tau * dy, qj[2], qj[3])


def move_dist2(qi: Sq, qj: Sq, tau: F) -> F:
    dx, dy = qj[0] - qi[0], qj[1] - qi[1]
    return tau * tau * (dx * dx + dy * dy)


def moved_to_wall(q: Sq, wall: str, by: F) -> Sq:
    cx, cy, c, s = q
    if wall == "left":
        return (cx - by, cy, c, s)
    if wall == "right":
        return (cx + by, cy, c, s)
    if wall == "bottom":
        return (cx, cy - by, c, s)
    return (cx, cy + by, c, s)


def t_equivalents(t: F) -> list[F]:
    """t itself and the half-angle tangents of theta + 90, + 180 and - 90 degrees, where
    defined: (t + 1)/(1 - t), -1/t, (t - 1)/(1 + t)."""
    out = [t]
    if t != 1:
        out.append((t + 1) / (1 - t))
    if t != 0:
        out.append(-1 / t)
    if t != -1:
        out.append((t - 1) / (1 + t))
    return out
