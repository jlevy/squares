"""Method A of the review of jlevy/squares#1031: separating axes on poses, exactly.

Written for this review; imports nothing from this repository or the source.

A pose is ``(cx, cy, ux, uy)`` in ``fractions.Fraction`` with ``ux**2 + uy**2 == 1``;
the square is ``{c + a u + b v : |a|, |b| <= 1/2}``, ``v = (-uy, ux)``.  The method reads
poses and never a corner.

For a pair ``(i, j)`` with centre difference ``d`` the projections on any of the four
unit normals ``u_i, v_i, u_j, v_j`` have half-lengths adding to the same
``H = 1/2 + (|cos D| + |sin D|)/2``, ``cos D = u_i . u_j`` and ``sin D = u_i x u_j``.
The separation on a normal ``w`` is ``|d . w| - H``, an exact distance, and the margin is
the largest of the four.  Two convex polygons have disjoint interiors exactly when a line
parallel to an edge of one of them weakly separates them, and are disjoint exactly when
one separates them strictly, so the sign of the margin is the class: positive apart,
zero contact (disjoint interiors), negative overlap.

A wall clearance is the signed distance from the square's extreme corner to the wall,
from the half-extent ``h = (|ux| + |uy|)/2`` (the same in x and y).
"""

from __future__ import annotations

from fractions import Fraction

HALF = Fraction(1, 2)

Pose = tuple[Fraction, Fraction, Fraction, Fraction]


def pair_terms(p: Pose, q: Pose) -> tuple[Fraction, Fraction, int]:
    """``(M, H, axis)``: the largest ``|d . w|`` over the four normals, ``H``, and which normal.

    The axis index is 0 for ``u_i``, 1 for ``v_i``, 2 for ``u_j``, 3 for ``v_j``.
    """
    cxi, cyi, uxi, uyi = p
    cxj, cyj, uxj, uyj = q
    dx = cxj - cxi
    dy = cyj - cyi
    cos_d = uxi * uxj + uyi * uyj
    sin_d = uxi * uyj - uyi * uxj
    h = HALF + (abs(cos_d) + abs(sin_d)) * HALF
    vals = (
        abs(dx * uxi + dy * uyi),
        abs(-dx * uyi + dy * uxi),
        abs(dx * uxj + dy * uyj),
        abs(-dx * uyj + dy * uxj),
    )
    best = 0
    for k in range(1, 4):
        if vals[k] > vals[best]:
            best = k
    return vals[best], h, best


def pair_margin(p: Pose, q: Pose) -> Fraction:
    m, h, _ = pair_terms(p, q)
    return m - h


def klass(margin: Fraction) -> str:
    if margin > 0:
        return "apart"
    if margin == 0:
        return "contact"
    return "overlap"


def half_extent(p: Pose) -> Fraction:
    return (abs(p[2]) + abs(p[3])) * HALF


def clearances(p: Pose, side: Fraction) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    """(left, bottom, right, top) signed clearances in the box [0, side]^2."""
    h = half_extent(p)
    return p[0] - h, p[1] - h, side - p[0] - h, side - p[1] - h


def wall_class(c: Fraction) -> str:
    if c > 0:
        return "clear"
    if c == 0:
        return "contact"
    return "cross"


def all_margins(poses: list[Pose], pairs: list[tuple[int, int]] | None = None) -> dict[tuple[int, int], Fraction]:
    """Exact margins of every pair (0-based indices), or of the pairs given."""
    out: dict[tuple[int, int], Fraction] = {}
    if pairs is None:
        n = len(poses)
        for i in range(n):
            pi = poses[i]
            for j in range(i + 1, n):
                out[(i, j)] = pair_margin(pi, poses[j])
    else:
        for i, j in pairs:
            out[(i, j)] = pair_margin(poses[i], poses[j])
    return out


def all_clearances(poses: list[Pose], side: Fraction) -> list[tuple[Fraction, Fraction, Fraction, Fraction]]:
    return [clearances(p, side) for p in poses]


def corner_projection_margin(ci: list[tuple[Fraction, Fraction]], cj: list[tuple[Fraction, Fraction]]) -> Fraction:
    """A third formulation, from corners alone: project the eight corners on the four edge
    directions (each a unit vector for a unit square) and take the largest gap."""
    best: Fraction | None = None
    for cs in (ci, cj):
        for k in (0, 1):
            ax, ay = cs[k]
            bx, by = cs[k + 1]
            wx, wy = bx - ax, by - ay
            pi = [x * wx + y * wy for x, y in ci]
            pj = [x * wx + y * wy for x, y in cj]
            gap = max(min(pj) - max(pi), min(pi) - max(pj))
            if best is None or gap > best:
                best = gap
    assert best is not None
    return best
