"""Route A: exact separating axes over every pair, and walls by support function.

Decides, over Q with Fractions, that n unit squares lie in [0, side]^2 with pairwise
disjoint interiors:

- unit: a^2 + b^2 = 1 exactly for every basis (a, b);
- walls: with h = (|a| + |b|)/2 the half-extent of a square along x and along y,
  h <= cx <= side - h and h <= cy <= side - h;
- pairs: for squares i, j with D = theta_j - theta_i, cos D = ai aj + bi bj and
  sin D = ai bj - bi aj, each square's half-width on any of the four edge normals of the
  pair is 1/2 for its own and (|cos D| + |sin D|)/2 for the other's, so the one threshold
  T = (1 + |cos D| + |sin D|)/2 serves all four; the interiors are disjoint iff some edge
  normal u has |u . (cj - ci)| >= T (the separating axis theorem for convex polygons,
  closed projections allowed to touch).

Every pair i < j is decided; nothing is pruned. Reports the least pair slack
max_u |u . d| - T and the least wall clearance, each with where it occurs.
"""

from __future__ import annotations

from fractions import Fraction

from qio import Square


def pair_slack(p: Square, q: Square) -> tuple[Fraction, int]:
    cxi, cyi, ai, bi = p
    cxj, cyj, aj, bj = q
    dx, dy = cxj - cxi, cyj - cyi
    cos_d = ai * aj + bi * bj
    sin_d = ai * bj - bi * aj
    t = (1 + abs(cos_d) + abs(sin_d)) / 2
    projs = (
        abs(ai * dx + bi * dy),
        abs(-bi * dx + ai * dy),
        abs(aj * dx + bj * dy),
        abs(-bj * dx + aj * dy),
    )
    k = max(range(4), key=lambda m: projs[m])
    return projs[k] - t, k


def axis_of(p: Square, q: Square, k: int) -> tuple[Fraction, Fraction]:
    _, _, ai, bi = p
    _, _, aj, bj = q
    return ((ai, bi), (-bi, ai), (aj, bj), (-bj, aj))[k]


def half_extent(sq: Square) -> Fraction:
    return (abs(sq[2]) + abs(sq[3])) / 2


def check(side: Fraction, squares: list[Square]) -> dict[str, object]:
    n = len(squares)
    non_unit = [i for i, s in enumerate(squares) if s[2] * s[2] + s[3] * s[3] != 1]
    wall_best: tuple[Fraction, int, str] | None = None
    wall_fail: list[tuple[int, str]] = []
    extent_hi = Fraction(0)
    extent_lo: Fraction | None = None
    for i, s in enumerate(squares):
        h = half_extent(s)
        for name, v in (("left", s[0] - h), ("bottom", s[1] - h), ("right", side - s[0] - h), ("top", side - s[1] - h)):
            if v < 0:
                wall_fail.append((i, name))
            if wall_best is None or v < wall_best[0]:
                wall_best = (v, i, name)
        extent_hi = max(extent_hi, s[0] + h, s[1] + h)
        lo = min(s[0] - h, s[1] - h)
        extent_lo = lo if extent_lo is None else min(extent_lo, lo)
    pair_best: tuple[Fraction, int, int, int] | None = None
    overlaps: list[tuple[int, int]] = []
    pairs = 0
    for i in range(n):
        p = squares[i]
        for j in range(i + 1, n):
            slack, k = pair_slack(p, squares[j])
            pairs += 1
            if slack < 0:
                overlaps.append((i, j))
            if pair_best is None or slack < pair_best[0]:
                pair_best = (slack, i, j, k)
    assert wall_best is not None and pair_best is not None and extent_lo is not None
    ok = not non_unit and not wall_fail and not overlaps
    return {
        "route": "A: separating axes over all pairs, walls by support function",
        "n": n,
        "side": side,
        "accepted": ok,
        "pairs_decided": pairs,
        "non_unit": non_unit,
        "wall_failures": wall_fail[:10],
        "wall_failure_count": len(wall_fail),
        "overlap_count": len(overlaps),
        "overlaps": overlaps[:10],
        "least_wall_clearance": wall_best,
        "least_pair_slack": pair_best,
        "extent_hi": extent_hi,
        "extent_lo": extent_lo,
    }
