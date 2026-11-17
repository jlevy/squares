"""Lane L180 closed forms in fractions: margins by corner projections, and moves.

Written for the blind stage 4 review of issue #996 as a clean-room implementation.
It imports nothing from this repository or the source, and reuses no code of any
earlier review. It decides nothing about a certificate: the self-test holds the two
methods to it, and the controls plan states its outcomes from it.

- **Margin.** For a pair, every corner of both squares is projected on each of the four
  unit edge normals, and the gap on a normal is the larger of (least projection of one
  square less greatest of the other) both ways round; the margin is the largest gap.
  This is a third formulation, apart from method A's half-extents and method B's
  clipping.
- **Clearance.** The least corner coordinate, and the side less the greatest.
- **Closing a pair.** Square j moves toward square i along d = C_j - C_i, C_j(t) =
  C_j - t d. On a normal w the gap falls as g_w - t |d . w| while the projection keeps
  its sign, so the least t at which the margin is m* is max over the normals with a rate
  of (g_w - m*) / |d . w|, and there the margin is exactly m*.
- **Rotations.** By t = tan(phi / 2), (cos phi, sin phi) = ((1 - t^2), 2t) / (1 + t^2),
  exact and unit for every rational t.
"""

from __future__ import annotations

from fractions import Fraction

from l180_reader import Point, Pose, json_corners


def normals(p: Pose) -> list[Point]:
    return [(p.c, p.s), (-p.s, p.c)]


def _proj(cs: tuple[Point, ...], w: Point) -> tuple[Fraction, Fraction]:
    vals = [x * w[0] + y * w[1] for x, y in cs]
    return min(vals), max(vals)


def gaps(p: Pose, q: Pose) -> list[tuple[Fraction, Point]]:
    """The gap on each of the four normals (p's two, then q's two), with the normal."""
    cp = json_corners(p)
    cq = json_corners(q)
    out: list[tuple[Fraction, Point]] = []
    for w in normals(p) + normals(q):
        lo_p, hi_p = _proj(cp, w)
        lo_q, hi_q = _proj(cq, w)
        out.append((max(lo_q - hi_p, lo_p - hi_q), w))
    return out


def margin(p: Pose, q: Pose) -> Fraction:
    return max(g for g, _ in gaps(p, q))


def clearances(p: Pose, side: Fraction) -> dict[str, Fraction]:
    cs = json_corners(p)
    xs = [x for x, _ in cs]
    ys = [y for _, y in cs]
    return {"left": min(xs), "bottom": min(ys), "right": side - max(xs), "top": side - max(ys)}


def closing_time(p: Pose, q: Pose, target: Fraction) -> Fraction:
    """The least t at which q moved by -t (C_q - C_p) has margin ``target`` with p."""
    dx, dy = q.x - p.x, q.y - p.y
    best: Fraction | None = None
    for g, w in gaps(p, q):
        rate = abs(dx * w[0] + dy * w[1])
        if rate == 0:
            continue
        t = (g - target) / rate
        if best is None or t > best:
            best = t
    if best is None:
        raise ValueError("no normal closes")
    return best


def moved(q: Pose, dx: Fraction, dy: Fraction) -> Pose:
    return Pose(q.x + dx, q.y + dy, q.c, q.s)


def close_pair(p: Pose, q: Pose, target: Fraction) -> tuple[Pose, Fraction]:
    t = closing_time(p, q, target)
    return moved(q, -t * (q.x - p.x), -t * (q.y - p.y)), t


def rotation(t: Fraction) -> tuple[Fraction, Fraction]:
    den = 1 + t * t
    return (1 - t * t) / den, 2 * t / den


def rotated(q: Pose, t: Fraction) -> Pose:
    """q turned about its centre by the angle whose half-angle tangent is t (counterclockwise)."""
    co, si = rotation(t)
    return Pose(q.x, q.y, q.c * co - q.s * si, q.s * co + q.c * si)


def move_to_wall(q: Pose, wall: str, by: Fraction) -> Pose:
    """q moved toward ``wall`` by ``by`` (positive is toward the wall)."""
    step = {"left": (-by, Fraction(0)), "bottom": (Fraction(0), -by), "right": (by, Fraction(0)), "top": (Fraction(0), by)}
    dx, dy = step[wall]
    return moved(q, dx, dy)
