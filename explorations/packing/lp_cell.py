"""The fixed-angle cell of the configuration space is a linear program.

Fix every square's angle, and fix for each pair *which* of the four candidate
axes separates it.  What is left is a linear program in the centres and the
side: corners are affine in the centre, the separating-axis condition is a
conjunction of linear inequalities, containment is linear, and `min s` is
linear.  All of this problem's nonconvexity lives in the angles and in the
combinatorial choice of cell.

This script is the check.  It reads the cell off `sqpack`'s exact certificate
for Trump's packing -- eleven angles and fifty-five axis choices, and nothing
else -- rebuilds the LP from scratch, and asks whether solving it returns the
packing.  The centres are never given to the solver; they are what it has to
reconstruct.

It then holds the cell fixed and sweeps the one free angle, which turns the
34-dimensional problem into a one-dimensional one and shows where its minimum
sits and what shape it has.

    uv run python lp_cell.py

Everything printed is asserted, so this doubles as a gate.
"""

from __future__ import annotations

import math
import sys

from scipy.optimize import linprog

from sqpack.packings.trump11 import build
from sqpack.verify import edge_axes, exact_sign, project

# Trump's tilt, as the frontier corpus records it.
A_STAR_DEG = 40.181937290329714

# Decimal digits taken from the exact field before dropping to f64.  Well past
# f64's 17, so nothing here is limited by the conversion.
FIELD_DIGITS = 40


def unit_square_offsets(theta: float) -> list[tuple[float, float]]:
    """The four corner offsets from the centre of a unit square at angle `theta`.

    A function of the angle alone, which is the whole point: once the angles
    are fixed these are constants, and the corners become affine in the centre.
    """
    c, s = math.cos(theta), math.sin(theta)
    return [
        (c * dx - s * dy, s * dx + c * dy)
        for dx, dy in ((-0.5, -0.5), (0.5, -0.5), (0.5, 0.5), (-0.5, 0.5))
    ]


def edge_normals(theta: float) -> list[tuple[float, float]]:
    """The two distinct edge normals of a unit square at angle `theta`."""
    c, s = math.cos(theta), math.sin(theta)
    return [(-s, c), (-c, -s)]


def read_cell(squares, to_float):
    """Read the cell off the exact certificate.

    Returns the eleven angles and, for each pair, which of its four candidate
    axes separates it and in which order.  This is the *combinatorial* content
    of the packing -- what an annealer would have to discover, and what the LP
    takes as given.
    """
    angles = []
    for sq in squares:
        (px, py), (qx, qy) = sq[0], sq[1]
        angles.append(math.atan2(to_float(qy) - to_float(py), to_float(qx) - to_float(px)))

    axis_of = {}
    for i in range(len(squares)):
        for j in range(i + 1, len(squares)):
            a, b = squares[i], squares[j]
            for k, axis in enumerate(edge_axes(a) + edge_axes(b)):
                alo, ahi = project(a, axis, exact_sign)
                blo, bhi = project(b, axis, exact_sign)
                if exact_sign(blo - ahi) >= 0:  # i at or before j
                    axis_of[(i, j)] = (k, +1)
                    break
                if exact_sign(alo - bhi) >= 0:  # j at or before i
                    axis_of[(i, j)] = (k, -1)
                    break
            else:
                raise AssertionError(f"pair {(i, j)} has no separating axis")
    return angles, axis_of


def cell_lp(angles: list[float], axis_of: dict):
    """Assemble the cell's LP as `(c, A_ub, b_ub)`.

    Variables are `x_0..x_{n-1}, y_0..y_{n-1}, s`; the objective is `min s`.
    Two constraint families, both 16 rows wide:

    - **containment**, per square: each of 4 corners against each of the 4
      container edges;
    - **separation**, per pair: each of 4 corners of the earlier square at or
      before each of 4 corners of the later one, along the pair's fixed axis.

    So `16 * (n + C(n, 2))` rows in total -- 1,056 at `n = 11`.
    """
    n = len(angles)
    offs = [unit_square_offsets(t) for t in angles]
    nv, s_col = 2 * n + 1, 2 * n
    a_ub: list[list[float]] = []
    b_ub: list[float] = []

    def add(rhs: float) -> list[float]:
        """Append a fresh all-zero row with right-hand side `rhs`, and return it."""
        r = [0.0] * nv
        a_ub.append(r)
        b_ub.append(rhs)
        return r

    for i in range(n):
        for ox, oy in offs[i]:
            add(ox)[i] = -1.0  # 0 <= x_i + ox
            add(oy)[n + i] = -1.0  # 0 <= y_i + oy
            r = add(-ox)  # x_i + ox <= s
            r[i], r[s_col] = 1.0, -1.0
            r = add(-oy)  # y_i + oy <= s
            r[n + i], r[s_col] = 1.0, -1.0

    for (i, j), (k, orient) in axis_of.items():
        nx, ny = (edge_normals(angles[i]) + edge_normals(angles[j]))[k]
        lo, hi = (i, j) if orient > 0 else (j, i)
        for ox, oy in offs[lo]:
            for px, py in offs[hi]:
                r = add((nx * px + ny * py) - (nx * ox + ny * oy))
                r[lo] += nx
                r[n + lo] += ny
                r[hi] -= nx
                r[n + hi] -= ny

    c = [0.0] * nv
    c[s_col] = 1.0
    return c, a_ub, b_ub


def solve(angles, axis_of) -> tuple[float, list[tuple[float, float]]] | None:
    """Return `(s, centres)` at the cell's optimum, or `None` if infeasible."""
    n = len(angles)
    c, a_ub, b_ub = cell_lp(angles, axis_of)
    res = linprog(c, A_ub=a_ub, b_ub=b_ub, bounds=[(None, None)] * len(c), method="highs")
    if res.status != 0:
        return None
    return res.x[2 * n], [(res.x[i], res.x[n + i]) for i in range(n)]


def main() -> int:
    squares, side, field = build()
    n = len(squares)
    field.refine_to(60)

    def to_float(e):
        return float(field.decimal(e, FIELD_DIGITS))

    s_exact = to_float(side)
    centres_exact = [
        (sum(to_float(p[0]) for p in sq) / 4.0, sum(to_float(p[1]) for p in sq) / 4.0)
        for sq in squares
    ]

    angles, axis_of = read_cell(squares, to_float)
    distinct = sorted({round(math.degrees(a), 9) for a in angles})
    tilted = [i for i, a in enumerate(angles) if abs(a) > 1e-9]

    print("The cell, read off the exact certificate")
    print(f"  distinct angles:  {distinct} deg")
    print(f"  tilted squares:   {tilted}")
    print(f"  axis choices:     {len(axis_of)} pairs")

    c, a_ub, _ = cell_lp(angles, axis_of)
    print(
        f"  LP shape:         {len(c)} variables, {len(a_ub)} constraints"
        f"  (= 16 x ({n} + {n * (n - 1) // 2}))"
    )
    assert len(c) == 2 * n + 1
    assert len(a_ub) == 16 * (n + n * (n - 1) // 2) == 1056

    solved = solve(angles, axis_of)
    assert solved is not None, "the certificate's own cell must be feasible"
    s_lp, centres_lp = solved
    worst = max(
        max(
            abs(centres_lp[i][0] - centres_exact[i][0]),
            abs(centres_lp[i][1] - centres_exact[i][1]),
        )
        for i in range(n)
    )

    print("\nSolving it, without telling the solver where the squares go")
    print(f"  LP optimum        s = {s_lp:.16f}")
    print(f"  exact value       s = {s_exact:.16f}")
    print(f"  |difference|        = {abs(s_lp - s_exact):.3e}")
    print(f"  worst centre error  = {worst:.3e}")
    assert abs(s_lp - s_exact) < 1e-12, s_lp
    assert worst < 1e-12, worst

    # Hold the cell fixed and vary the one free angle.  phi(a) is then the whole
    # problem, restricted to this cell, as a function of a single variable.
    def phi(a_deg: float) -> float:
        a = math.radians(a_deg)
        out = solve([a if i in tilted else 0.0 for i in range(n)], axis_of)
        return float("inf") if out is None else out[0]

    print("\nThe cell as a function of its one free angle")
    print("      a (deg)         phi(a)        phi(a) - s*")
    for a_deg in (39.0, 39.5, 40.0, 40.1, A_STAR_DEG, 40.3, 40.5, 41.0, 42.0):
        v = phi(a_deg)
        mark = "  <- Trump" if a_deg == A_STAR_DEG else ""
        print(f"  {a_deg:>11.6f}   {v:.12f}   {v - s_exact:+.3e}{mark}")

    grid = [38.0 + 4.0 * k / 2000 for k in range(2001)]
    best_v, best_a = min((phi(a), a) for a in grid)
    print(f"\n  argmin over [38, 42] deg, 2001 samples: a = {best_a:.6f} deg")
    print(f"  Trump's angle:                          a = {A_STAR_DEG:.6f} deg")
    assert abs(best_a - A_STAR_DEG) <= 4.0 / 2000, best_a
    assert best_v >= s_exact - 1e-12, best_v

    # The minimum is a corner, not a smooth stationary point: the one-sided slopes
    # are stable under refinement and differ by a factor of about 2.2.  Reported in
    # radians as well, because that is the unit H-019 and exp-010 are recorded in and
    # this script exists to reproduce them through unrelated constraint rows.
    print("\nShape of the minimum: one-sided slopes")
    print("        h (deg)       left /deg      right /deg     left /rad    right /rad")
    slopes = []
    per_rad = 180.0 / math.pi
    for h in (1e-2, 1e-3, 1e-4, 1e-5):
        left = (phi(A_STAR_DEG - h) - s_exact) / h
        right = (phi(A_STAR_DEG + h) - s_exact) / h
        slopes.append((left, right))
        print(
            f"  {h:>13.0e}   {left:.6e}   {right:.6e}"
            f"      {left * per_rad:.4f}       {right * per_rad:.4f}"
        )
    for left, right in slopes:
        assert 0.0 < left < right, (left, right)
    assert abs(slopes[-1][0] / slopes[0][0] - 1.0) < 1e-3, "left slope not stable"
    assert abs(slopes[-1][1] / slopes[0][1] - 1.0) < 1e-3, "right slope not stable"

    # H-019's registered values, measured by sqpack.quench through a different
    # formulation (one row per pair, not sixteen). Agreement to three decimals is the
    # cross-check; divergence would mean one of the two constraint sets is wrong.
    left_rad, right_rad = slopes[-1][0] * per_rad, slopes[-1][1] * per_rad
    print(f"\n  ratio right/left = {right_rad / left_rad:.4f}")
    print("  H-019 / exp-010, via sqpack.quench: 0.1747, 0.3841, ratio 2.198")
    assert abs(left_rad - 0.1747) < 5e-4, left_rad
    assert abs(right_rad - 0.3841) < 5e-4, right_rad

    print("\nALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
