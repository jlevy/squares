"""Uncertified pilot for the fractional piercing value tau* of unit-square poses.

The H-034 family of diagnostics: for the family `U_t` of open unit-square poses
inside `[0, t]^2`, `tau*(U_t)` is the minimum total mass of a point measure giving
every pose at least unit mass. `tau*(U_t) > k` rules out a k-point pure unavoidable
set at side `t`; weak duality against disjoint boxes gives `tau* >= nu` (the
packing number), so for `t > s(11)` the value is already at least 11 and the
informative window for an eleven-point set at `n = 12` is
`(2 + 4/sqrt 5, s(11)) = (3.7889, 3.8771)`.

Everything here is float and restricted, and is typed accordingly:

- the LP restricts points to a grid and poses to a position-angle grid, so its
  value is neither an upper nor a lower bound on `tau*` by itself;
- the weighted escape sweep evaluates the LP optimum against a denser pose grid
  and reports the minimum mass any swept pose collects -- dividing the LP value by
  that minimum gives the value of a measure feasible for the swept family, an
  indicative (still uncertified) upper-side companion;
- the certified two-sided instrument H-034 registered (interval bounds covering
  every omitted continuous point and pose) is exactly what this pilot is not.

Usage, from `packing/`:
    uv run --frozen python -m devtools.pierce_pilot --side 3.83
    uv run --frozen python -m devtools.pierce_pilot --ladder
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass

import numpy as np
from scipy.optimize import linprog

#: The pose side used for the open-box limit; slightly above one, as the boxes are.
BOX_SIDE = 1.0000001


@dataclass(frozen=True)
class PilotResult:
    side: float
    point_grid: int
    pose_positions: int
    pose_angles: int
    lp_value: float
    sweep_min_mass: float
    indicative_upper: float


def poses(side: float, positions: int, angles: int) -> list[tuple[float, float, float]]:
    """Centre-and-angle grid of poses whose boxes fit inside the container."""
    half = BOX_SIDE / 2.0
    out: list[tuple[float, float, float]] = []
    for angle_index in range(angles):
        theta = (math.pi / 2) * angle_index / angles
        cos, sin = math.cos(theta), math.sin(theta)
        reach = half * (abs(cos) + abs(sin))
        low, high = reach, side - reach
        if high <= low:
            continue
        for i in range(positions):
            x = low + (high - low) * i / (positions - 1)
            for j in range(positions):
                y = low + (high - low) * j / (positions - 1)
                out.append((x, y, theta))
    return out


def covers(pose: tuple[float, float, float], px: float, py: float) -> bool:
    x, y, theta = pose
    cos, sin = math.cos(theta), math.sin(theta)
    dx, dy = px - x, py - y
    u = dx * cos + dy * sin
    v = -dx * sin + dy * cos
    half = BOX_SIDE / 2.0
    return abs(u) < half and abs(v) < half


def run_pilot(
    side: float, point_grid: int, pose_positions: int, pose_angles: int
) -> PilotResult:
    margin = 0.02
    points = [
        (
            margin + (side - 2 * margin) * i / (point_grid - 1),
            margin + (side - 2 * margin) * j / (point_grid - 1),
        )
        for i in range(point_grid)
        for j in range(point_grid)
    ]
    pose_list = poses(side, pose_positions, pose_angles)
    rows = np.zeros((len(pose_list), len(points)))
    for row, pose in enumerate(pose_list):
        for col, (px, py) in enumerate(points):
            if covers(pose, px, py):
                rows[row, col] = 1.0
    keep = rows.sum(axis=1) > 0
    if not bool(keep.all()):
        raise SystemExit(
            f"{int((~keep).sum())} poses cover no grid point at side {side}; "
            "refine the point grid"
        )
    result = linprog(
        c=np.ones(len(points)),
        A_ub=-rows,
        b_ub=-np.ones(len(pose_list)),
        bounds=(0, None),
        method="highs",
    )
    if not result.success:
        raise SystemExit(f"LP failed at side {side}: {result.message}")
    weights = result.x
    sweep = poses(side, pose_positions * 2, pose_angles * 3)
    min_mass = math.inf
    for pose in sweep:
        mass = 0.0
        for col, (px, py) in enumerate(points):
            if weights[col] > 1e-12 and covers(pose, px, py):
                mass += weights[col]
        min_mass = min(min_mass, mass)
    lp_value = float(result.fun)
    return PilotResult(
        side=side,
        point_grid=point_grid,
        pose_positions=pose_positions,
        pose_angles=pose_angles,
        lp_value=lp_value,
        sweep_min_mass=min_mass,
        indicative_upper=lp_value / min_mass if min_mass > 0 else math.inf,
    )


def report(result: PilotResult) -> None:
    print(
        f"side {result.side:.4f}  points {result.point_grid}^2  "
        f"poses {result.pose_positions}^2 x {result.pose_angles}: "
        f"LP {result.lp_value:.4f}  sweep min mass {result.sweep_min_mass:.4f}  "
        f"indicative upper {result.indicative_upper:.4f}"
    )


def main(arguments: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--side", type=float, default=None)
    parser.add_argument("--points", type=int, default=26)
    parser.add_argument("--positions", type=int, default=22)
    parser.add_argument("--angles", type=int, default=6)
    parser.add_argument("--ladder", action="store_true")
    options = parser.parse_args(arguments)
    print("UNCERTIFIED PILOT: restricted grids, float LP; not a bound in either direction")
    if options.ladder:
        for side in (3.80, 3.83, 3.86, 3.90):
            report(run_pilot(side, options.points, options.positions, options.angles))
    else:
        side = options.side if options.side is not None else 3.83
        report(run_pilot(side, options.points, options.positions, options.angles))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
