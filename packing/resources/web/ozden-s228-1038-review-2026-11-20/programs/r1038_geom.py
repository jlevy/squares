"""A third formulation, for the self-test and the controls; it decides nothing alone.

- `corner_margin` and `corner_clearances` recompute method A's margins and clearances from
  the corners, by projecting all eight corners of a pair on each of the four unit normals,
  in `fractions.Fraction`. Control C0 holds them equal to method A everywhere.
- `close_pair` moves square j along the line of centres to make the pair's margin exactly
  m*: with d the centre difference and H_w the two half-widths on normal w, the margin
  after square j moves to c_i + (1 - t) d is max_w ((1 - t)|d . w| - H_w), and
  t* = max over the normals with d . w != 0 of 1 - (m* + H_w)/|d . w| makes it m*.
- `to_wall` moves a square along one axis to a stated clearance from one wall.
"""

from __future__ import annotations

from fractions import Fraction

Vec = tuple[Fraction, Fraction]
HALF = Fraction(1, 2)


def corners(center: Vec, basis: Vec) -> list[Vec]:
    """The four corners c +- u/2 +- v/2, v = (-b, a)."""
    (cx, cy), (a, b) = center, basis
    out: list[Vec] = []
    for s, t in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        out.append((cx + HALF * (s * a - t * b), cy + HALF * (s * b + t * a)))
    return out


def normals(basis: Vec) -> list[Vec]:
    """The square's two unit edge normals."""
    a, b = basis
    return [(a, b), (-b, a)]


def _project(points: list[Vec], w: Vec) -> tuple[Fraction, Fraction]:
    values = [p[0] * w[0] + p[1] * w[1] for p in points]
    return min(values), max(values)


def corner_margin(ci: Vec, bi: Vec, cj: Vec, bj: Vec) -> Fraction:
    """The greatest separation of the two corner projections over the four normals."""
    pi, pj = corners(ci, bi), corners(cj, bj)
    best: Fraction | None = None
    for w in normals(bi) + normals(bj):
        lo_i, hi_i = _project(pi, w)
        lo_j, hi_j = _project(pj, w)
        gap = max(lo_j - hi_i, lo_i - hi_j)
        if best is None or gap > best:
            best = gap
    assert best is not None
    return best


def corner_clearances(center: Vec, basis: Vec, side: Fraction) -> list[Fraction]:
    """Left, bottom, right and top clearances from the corners."""
    points = corners(center, basis)
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return [min(xs), min(ys), side - max(xs), side - max(ys)]


def half_width(basis: Vec, w: Vec) -> Fraction:
    """The square's half-width on the unit direction w."""
    u, v = normals(basis)
    return (abs(u[0] * w[0] + u[1] * w[1]) + abs(v[0] * w[0] + v[1] * w[1])) / 2


def close_pair(ci: Vec, bi: Vec, cj: Vec, bj: Vec, target: Fraction) -> Vec:
    """Square j's new centre on the line of centres, making the pair's margin `target`."""
    d = (cj[0] - ci[0], cj[1] - ci[1])
    best: Fraction | None = None
    for w in normals(bi) + normals(bj):
        along = abs(d[0] * w[0] + d[1] * w[1])
        if along == 0:
            continue
        t = 1 - (target + half_width(bi, w) + half_width(bj, w)) / along
        if best is None or t > best:
            best = t
    assert best is not None
    keep = 1 - best
    return (ci[0] + keep * d[0], ci[1] + keep * d[1])


def to_wall(center: Vec, basis: Vec, side: Fraction, wall: int, clearance: Fraction) -> Vec:
    """The centre moved along one axis so its clearance at `wall` (0 L, 1 B, 2 R, 3 T) is `clearance`."""
    reach = (abs(basis[0]) + abs(basis[1])) / 2
    cx, cy = center
    if wall == 0:
        return (clearance + reach, cy)
    if wall == 1:
        return (cx, clearance + reach)
    if wall == 2:
        return (side - clearance - reach, cy)
    return (cx, side - clearance - reach)
