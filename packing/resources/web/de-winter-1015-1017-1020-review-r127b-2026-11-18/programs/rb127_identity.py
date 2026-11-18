"""Measure one packing against another, square by square (lane r127b-1118).

Decides nothing about a bound. For each of the eight symmetries of the square box it
maps the first packing onto the second, in two frames: the lower-left frame (both boxes
with their corner at the origin, the symmetry acting on the first box) and the
box-centred frame (each packing's box centre at the origin). In each it reports:

- whether the nearest-centre map from the second packing's squares to the first's is
  one to one;
- the optimal assignment by the sum of squared centre moves (chosen in binary64, which
  only chooses; every reported move is computed exactly from the rationals);
- how many squares move beyond 1e-9, 1e-6, 1e-3, 1e-2 and 1e-1, decided exactly on the
  squared distances; the largest move; the squares whose orientation (the direction
  modulo a quarter turn) is exactly kept; and the largest turn, printed only.

The symmetry with the least assignment cost is the nearest.
"""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Any

import numpy as np
from scipy.optimize import linear_sum_assignment

import rb127_fmt as F

Q = tuple[int, int]
# (name, matrix): x' = m00 x + m01 y + t0, y' = m10 x + m11 y + t1, t chosen to keep the box.
SYMS = [
    ("identity", ((1, 0), (0, 1))),
    ("mirror x -> S - x", ((-1, 0), (0, 1))),
    ("mirror y -> S - y", ((1, 0), (0, -1))),
    ("half turn", ((-1, 0), (0, -1))),
    ("transpose", ((0, 1), (1, 0))),
    ("quarter turn counterclockwise", ((0, -1), (1, 0))),
    ("quarter turn clockwise", ((0, 1), (-1, 0))),
    ("antitranspose", ((0, -1), (-1, 0))),
]
THRESHOLDS = [Fraction(1, 10**9), Fraction(1, 10**6), Fraction(1, 10**3), Fraction(1, 100), Fraction(1, 10)]


def _f(v: Q) -> Fraction:
    return Fraction(v[0], v[1])


def poses(rows: list[tuple[Q, Q, Q, Q]]) -> list[tuple[Fraction, Fraction, Fraction, Fraction]]:
    return [(_f(r[0]), _f(r[1]), _f(r[2]), _f(r[3])) for r in rows]


def _apply(m: tuple[tuple[int, int], tuple[int, int]], x: Fraction, y: Fraction) -> tuple[Fraction, Fraction]:
    return m[0][0] * x + m[0][1] * y, m[1][0] * x + m[1][1] * y


def _map(P: list, SA: Fraction, m, frame: str) -> list:
    out = []
    for x, y, c, s in P:
        if frame == "lower-left":
            cx, cy = x - SA / 2, y - SA / 2
            nx, ny = _apply(m, cx, cy)
            nx, ny = nx + SA / 2, ny + SA / 2
        else:
            nx, ny = _apply(m, x - SA / 2, y - SA / 2)
        nc, ns = _apply(m, c, s)
        out.append((nx, ny, nc, ns))
    return out


def _orientation(uA: tuple[Fraction, Fraction], uB: tuple[Fraction, Fraction]) -> tuple[bool, float]:
    c, s = uA
    reps = [(c, s), (-s, c), (-c, -s), (s, -c)]
    best = max(reps, key=lambda r: r[0] * uB[0] + r[1] * uB[1])
    dot = best[0] * uB[0] + best[1] * uB[1]
    cross = best[0] * uB[1] - best[1] * uB[0]
    same = uB in reps
    return same, math.degrees(math.atan2(float(cross), float(dot)))


def _sqrt_print(d2: Fraction) -> str:
    """The square root of an exact squared distance, to 8 figures, from integers."""
    if d2 == 0:
        return "0"
    scale = 40
    root = math.isqrt(d2.numerator * 10 ** (2 * scale) // d2.denominator)
    return F.sci(Fraction(root, 10**scale), 8)


def compare(PA: list, SA: Fraction, PB: list, SB: Fraction, m, frame: str) -> dict[str, Any]:
    MA = _map(PA, SA, m, frame)
    if frame == "lower-left":
        TB = PB
    else:
        TB = [(x - SB / 2, y - SB / 2, c, s) for x, y, c, s in PB]
    n = len(TB)
    ax = np.array([[float(p[0]), float(p[1])] for p in MA])
    bx = np.array([[float(p[0]), float(p[1])] for p in TB])
    cost = ((bx[:, None, :] - ax[None, :, :]) ** 2).sum(axis=2)
    nn = cost.argmin(axis=1)
    nn_one_to_one = len(set(nn.tolist())) == n
    rows, cols = linear_sum_assignment(cost)
    moves = []
    same_orient = 0
    max_turn = 0.0
    for b, a in zip(rows.tolist(), cols.tolist(), strict=True):
        dx = TB[b][0] - MA[a][0]
        dy = TB[b][1] - MA[a][1]
        d2 = dx * dx + dy * dy
        moves.append((d2, b + 1, a + 1))
        same, turn = _orientation((MA[a][2], MA[a][3]), (TB[b][2], TB[b][3]))
        same_orient += same
        max_turn = max(max_turn, abs(turn))
    beyond = {F.sci(t, 1): sum(1 for d2, _, _ in moves if d2 > t * t) for t in THRESHOLDS}
    moves.sort(key=lambda t: (-t[0], t[1]))
    total = sum((d2 for d2, _, _ in moves), Fraction(0))
    largest = moves[0]
    assignment_is_identity_labels = all(b == a for _, b, a in moves)
    return {
        "frame": frame,
        "nearest_centre_one_to_one": nn_one_to_one,
        "assignment_cost_float": float(total),
        "assignment_keeps_labels": assignment_is_identity_labels,
        "moved_beyond": beyond,
        "largest_move": _sqrt_print(largest[0]),
        "largest_move_square_second": largest[1],
        "largest_move_square_first": largest[2],
        "largest_moves": [
            {"second": b, "first": a, "move": _sqrt_print(d2)} for d2, b, a in moves[:8]
        ],
        "orientation_kept_exactly": same_orient,
        "largest_turn_degrees": f"{max_turn:.6e}",
        "_moves": moves,
    }


def measure(rowsA: list, sideA: Q, rowsB: list, sideB: Q) -> dict[str, Any]:
    PA, PB = poses(rowsA), poses(rowsB)
    SA, SB = _f(sideA), _f(sideB)
    results = []
    for name, m in SYMS:
        for frame in ("lower-left", "box-centred"):
            r = compare(PA, SA, PB, SB, m, frame)
            r["symmetry"] = name
            results.append(r)
    best = {}
    for frame in ("lower-left", "box-centred"):
        cand = [r for r in results if r["frame"] == frame]
        cand.sort(key=lambda r: r["assignment_cost_float"])
        best[frame] = cand[0]["symmetry"]
    for r in results:
        r.pop("_moves")
    return {"nearest_symmetry": best, "by_symmetry": results}
