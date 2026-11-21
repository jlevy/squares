"""Method A of lane r1052: separating axes on poses, in Python integers.

A square is held as a pose: its centre c and the unit direction u of one edge, with v the
quarter turn of u; the square is c + alpha u + beta v with |alpha|, |beta| <= 1/2. Each
pose is written over one integer denominator D: c = (X, Y)/D, u = (A, B)/D. It is a
unit square exactly when A^2 + B^2 = D^2.

For two unit squares i and j with centre difference d, the projections on any of the four
unit normals u_i, v_i, u_j, v_j have half-lengths adding to the same
H = 1/2 + (|cos t| + |sin t|)/2, t the angle between the squares, so the separation on a
normal w is |d . w| - H, an exact signed distance. The margin is the largest of the four.
Two convex polygons have disjoint interiors exactly when a line parallel to an edge of one
of them weakly separates them, and are disjoint exactly when one separates them strictly,
so the margin's sign is the class: positive apart, zero contact, negative overlap.

A wall's clearance is the signed distance from the square's extreme point to the wall:
the half-extent of a pose along either axis is (|cos| + |sin|)/2.

Method A shares the reader with method B and nothing else. Given corners instead of
poses, it makes its own pose: with E = P1 - P0 and F = P2 - P1 it requires P3 - P2 = -E,
P0 - P3 = -F, E.E = F.F = 1 and E.F = 0, and takes c = P0 + (E + F)/2, u = E.
"""

from __future__ import annotations

from fractions import Fraction
from math import lcm
from typing import Any

Pose = tuple[int, int, int, int, int]  # X, Y, A, B, D


def integer_pose(x: Fraction, y: Fraction, a: Fraction, b: Fraction) -> Pose:
    d = lcm(x.denominator, y.denominator, a.denominator, b.denominator)
    return (
        x.numerator * (d // x.denominator),
        y.numerator * (d // y.denominator),
        a.numerator * (d // a.denominator),
        b.numerator * (d // b.denominator),
        d,
    )


def is_unit(p: Pose) -> bool:
    return p[2] * p[2] + p[3] * p[3] == p[4] * p[4]


def pose_from_corners(
    corners: list[tuple[Fraction, Fraction]],
) -> tuple[bool, tuple[Fraction, Fraction, Fraction, Fraction] | None]:
    """Method A's own reading of four corners as a pose, or (False, None)."""
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = corners
    ex, ey = x1 - x0, y1 - y0
    fx, fy = x2 - x1, y2 - y1
    closes = (x3 - x2, y3 - y2) == (-ex, -ey) and (x0 - x3, y0 - y3) == (-fx, -fy)
    unit = ex * ex + ey * ey == 1 and fx * fx + fy * fy == 1 and ex * fx + ey * fy == 0
    if not (closes and unit):
        return False, None
    return True, (x0 + (ex + fx) / 2, y0 + (ey + fy) / 2, ex, ey)


def clearances(side: Fraction, p: Pose) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    """(left, bottom, right, top): signed distances from the square to the four walls."""
    x, y, a, b, d = p
    w = abs(a) + abs(b)
    return (
        Fraction(2 * x - w, 2 * d),
        Fraction(2 * y - w, 2 * d),
        side - Fraction(2 * x + w, 2 * d),
        side - Fraction(2 * y + w, 2 * d),
    )


def margin(p: Pose, q: Pose) -> Fraction:
    """The largest separation of two unit squares over their four edge normals."""
    xi, yi, ai, bi, di = p
    xj, yj, aj, bj, dj = q
    dx = xj * di - xi * dj  # d = (dx, dy) / (di dj)
    dy = yj * di - yi * dj
    k = di * dj + abs(ai * aj + bi * bj) + abs(ai * bj - bi * aj)  # 2 H di dj
    on_i = 2 * max(abs(dx * ai + dy * bi), abs(dy * ai - dx * bi)) - di * k  # / (2 di^2 dj)
    on_j = 2 * max(abs(dx * aj + dy * bj), abs(dy * aj - dx * bj)) - dj * k  # / (2 di dj^2)
    return Fraction(max(on_i * dj, on_j * di), 2 * di * di * dj * dj)


def classify(value: Fraction) -> str:
    return "apart" if value > 0 else ("contact" if value == 0 else "overlap")


def wall_class(value: Fraction) -> str:
    return "apart" if value > 0 else ("contact" if value == 0 else "crossing")


def run(
    side: Fraction,
    *,
    poses: list[tuple[Fraction, Fraction, Fraction, Fraction]] | None = None,
    corners: list[list[tuple[Fraction, Fraction]]] | None = None,
) -> dict[str, Any]:
    """Decide every square, wall and pair. No pair is skipped and nothing is rounded."""
    if (poses is None) == (corners is None):
        raise ValueError("give poses or corners")
    if corners is not None:
        made = [pose_from_corners(c) for c in corners]
        unit = [ok for ok, _ in made]
        raw = [pose for _, pose in made]
    else:
        assert poses is not None
        raw = list(poses)
        unit = [True] * len(raw)
    ints: list[Pose | None] = []
    for k, pose in enumerate(raw):
        if pose is None:
            ints.append(None)
            continue
        ip = integer_pose(*pose)
        if not is_unit(ip):
            unit[k] = False
        ints.append(ip if unit[k] else None)
    walls: list[tuple[Fraction, ...] | None] = []
    for ip in ints:
        walls.append(None if ip is None else clearances(side, ip))
    n = len(ints)
    margins: dict[tuple[int, int], Fraction] = {}
    for i in range(n):
        pi = ints[i]
        if pi is None:
            continue
        for j in range(i + 1, n):
            pj = ints[j]
            if pj is None:
                continue
            margins[(i, j)] = margin(pi, pj)
    return {"unit": unit, "walls": walls, "margins": margins, "n": n}
