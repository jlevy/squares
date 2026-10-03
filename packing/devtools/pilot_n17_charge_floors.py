"""Go/no-go pilot for H-262's per-cell charge-floor engine on the H259 grid.

H-262 proposes excluding H260 occupancy patterns on the H259 grid (cap ``U = 1169/250``,
centre box ``[1/2, U - 1/2]^2``, cell side ``919/1250``, 5 x 5 cells) by per-cell floors
of an R068-type charge: a pattern dies when the sum over its cells of occupancy times the
cell's floor exceeds the budget ``M``. This pilot measures those floors from above by
sampling, before anyone builds the exact six-sweep instrument.

**The charge at U.** R068's certificate fixes sites, rules and integer weights in the
``L = 4613/1000`` container and proves, with strict cores over 4,991 half-angle intervals,
that every legal parent of side ``A = L / 4.66044`` captures at least ``Gamma``. The same
sites, rules and weights define a valid charge for any parent side: for pairwise disjoint
regions the sum of their charges is at most ``M``, because every budget term counts how
many disjoint regions can fire an image. Seventeen unit squares in ``[0, U]^2`` scale to
seventeen squares of side ``A_U = L / U`` in ``[0, L]^2`` whose open interiors are
pairwise disjoint, so the charge used here is the charge of the *open* ``A_U``-parent at
each pose. It is a true charge (no core is needed, since open parents are already
disjoint) and it dominates any strict-core charge the exact instrument would use, because
every core lies inside its parent and the rules are monotone. A floor sampled from it is
therefore at least the floor the exact instrument could prove, and a survivor count made
with sampled floors is a lower bound on the instrument's survivor count.

**The floors.** For each D4 class of cells the tool sweeps, at each sampled angle, the
exact arrangement of the signed Möbius atoms' capture rectangles over the closed cell
intersected with the legal centre envelope, evaluating the charge at every arrangement
cell's midpoint. That is exact in position at the sampled angle; the angle grid is
coarse-to-fine. Every reported floor is the charge of an actual legal pose in the cell,
so it is an upper estimate of the true floor.

**The counts.** Survivors are counted by vectorised enumeration over the 2^16 boundary
and 3^9 interior occupancy vectors, under the two subcontainer cuts (at most five centres
in any 2 x 2 block, at most nine in any 3 x 3 block), the floor test, and both, with
D4 orbits by Burnside. The cut-only count reproduces the X048 route census.

Usage (from ``packing/``)::

    uv run --frozen --all-extras --group dev python -m devtools.pilot_n17_charge_floors \\
        --output OUT.json [--workers 2] [--coarse-step 1.0]
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from dataclasses import dataclass
from fractions import Fraction
from multiprocessing import Pool
from pathlib import Path
from typing import Any

import numpy as np
import numpy.typing as npt

from devtools.audit_guzhou_r068 import RELEASES, load_json

FloatArray = npt.NDArray[np.float64]
IntArray = npt.NDArray[np.int64]
BoolArray = npt.NDArray[np.bool_]

N = 17
#: H259 cap, cell side and grid size, in unit-square units.
CAP_U = Fraction(1169, 250)
CELL_SIDE = Fraction(919, 1250)
GRID = 5
CENTRE_LOW = Fraction(1, 2)
#: Representative cells (x-index, y-index) of the six D4 classes of the 5 x 5 grid.
CLASS_REPRESENTATIVES: dict[str, tuple[int, int]] = {
    "corner": (0, 0),
    "edge-near-corner": (0, 1),
    "edge-middle": (0, 2),
    "interior-corner": (1, 1),
    "interior-edge": (1, 2),
    "centre": (2, 2),
}
#: The endpoint's occupancy cells (x-index, y-index), from the X048 endpoint receipt.
ENDPOINT_CELLS: tuple[tuple[int, int], ...] = (
    (0, 0),
    (1, 0),
    (0, 1),
    (0, 4),
    (4, 0),
    (3, 0),
    (4, 1),
    (4, 4),
    (0, 2),
    (1, 3),
    (1, 2),
    (2, 3),
    (2, 1),
    (3, 2),
    (2, 4),
    (3, 3),
    (4, 2),
)
#: The endpoint's seventeen poses (centre x, centre y, angle in degrees), unit frame,
#: as the X048 endpoint receipt prints them (five decimals).
ENDPOINT_POSES: tuple[tuple[float, float, float], ...] = (
    (0.50000, 0.50000, 0.0),
    (1.50000, 0.50000, 0.0),
    (0.50000, 1.50000, 0.0),
    (0.50000, 4.17553, 0.0),
    (4.17553, 0.50000, 0.0),
    (3.13845, 0.50000, 0.0),
    (4.17553, 1.50000, 0.0),
    (4.17553, 4.17553, 0.0),
    (0.70420, 2.70420, 39.805),
    (1.43604, 3.38804, 39.805),
    (1.55674, 2.11294, 39.805),
    (2.28858, 2.79678, 39.805),
    (2.31048, 1.40845, 39.805),
    (3.02713, 2.11052, 39.805),
    (2.34732, 4.17553, 0.0),
    (3.24507, 3.37249, -36.624),
    (4.17553, 2.61346, 0.0),
)
MAX_RULE_SITES = 10
#: Pose perturbations (container units, container units, degrees) that must leave a
#: witness's charge unchanged, so that float containment cannot be what set its value.
PERTURBATIONS: tuple[tuple[float, float, float], ...] = tuple(
    (dx, dy, dt)
    for dx in (-1e-9, 0.0, 1e-9)
    for dy in (-1e-9, 0.0, 1e-9)
    for dt in (-1e-9, 0.0, 1e-9)
    if (dx, dy, dt) != (0.0, 0.0, 0.0)
)
SLAB_BLOCK = 128
CUT_2X2 = 5
CUT_3X3 = 9


@dataclass(frozen=True, slots=True)
class Charge:
    """R068's sites and signed capture atoms in the L container, as floats."""

    container: Fraction
    parent_side_r068: Fraction
    budget: int
    site_x: FloatArray
    site_y: FloatArray
    atom_sites: IntArray
    atom_pad: BoolArray
    atom_weight: FloatArray
    atom_count: int
    site_count: int


def mobius_expansion(
    coefficients: list[int], threshold: int, masks: list[int]
) -> list[tuple[int, int]]:
    """Signed all-subset-capture terms of one monotone rule, as the checkers build them."""
    n = len(coefficients)
    size = 1 << n
    all_masks = np.arange(size)
    if masks:
        fires = np.zeros(size, dtype=np.int64)
        for winning in masks:
            fires |= (all_masks & winning) == winning
    else:
        captured = ((all_masks[:, None] >> np.arange(n)) & 1) * np.asarray(coefficients)
        fires = (captured.sum(axis=1) >= threshold).astype(np.int64)
    values = fires.copy()
    for j in range(n):
        with_bit = all_masks[(all_masks >> j) & 1 == 1]
        values[with_bit] -= values[with_bit ^ (1 << j)]
    return [(int(mask), int(values[mask])) for mask in range(1, size) if values[mask]]


def load_charge() -> Charge:
    """Read R068's certificate at its pinned digest and expand it into atoms."""
    release = RELEASES["R068"]
    data = load_json(release.certificate, release.sha256)
    container = Fraction(data["L"])
    parent = Fraction(data["A"])
    scale = int(data["coordinate_denominator"])
    side_units = container * scale
    if side_units.denominator != 1:
        raise ValueError("container side is not a whole number of coordinate units")
    side = side_units.numerator
    sites: list[tuple[int, int]] = []
    site_weights: list[int] = []
    for x, y, weight in data["point_orbits"]:
        images: dict[tuple[int, int], None] = {}
        for u, v in ((x, y), (y, x)):
            for a in (u, side - u):
                for b in (v, side - v):
                    images.setdefault((a, b), None)
        ordered = sorted(images)
        sites.extend(ordered)
        site_weights.extend([int(weight)] * len(ordered))
    if len(set(sites)) != len(sites):
        raise ValueError("physical sites are not distinct")
    atoms: list[tuple[tuple[int, ...], int]] = [
        ((index,), weight) for index, weight in enumerate(site_weights) if weight
    ]
    budget = sum(site_weights)
    for orbit in data["threshold_orbits"]:
        weight = int(orbit["weight"])
        threshold = int(orbit["threshold"])
        sets = [[int(site) for site in image] for image in orbit["sets"]]
        n = len(sets[0])
        coefficients = [int(c) for c in orbit.get("coefficients", [1] * n)]
        masks = [int(m) for m in orbit.get("winning_masks", [])]
        if n > MAX_RULE_SITES:
            raise ValueError("a rule has more sites than the atom table holds")
        per_image = 1 if masks else sum(coefficients) // threshold
        budget += weight * len(sets) * per_image
        expansion = mobius_expansion(coefficients, threshold, masks)
        for image in sets:
            for mask, coefficient in expansion:
                chosen = tuple(image[j] for j in range(n) if (mask >> j) & 1)
                atoms.append((chosen, weight * coefficient))
    if budget != int(data["budget_units"]):
        raise ValueError("reconstructed budget differs from the certificate's")
    atom_sites = np.full((len(atoms), MAX_RULE_SITES), -1, dtype=np.int64)
    for row, (chosen, _) in enumerate(atoms):
        atom_sites[row, : len(chosen)] = chosen
    atom_pad = atom_sites < 0
    atom_sites[atom_pad] = 0
    return Charge(
        container=container,
        parent_side_r068=parent,
        budget=budget,
        site_x=np.asarray([x / scale for x, _ in sites], dtype=np.float64),
        site_y=np.asarray([y / scale for _, y in sites], dtype=np.float64),
        atom_sites=atom_sites,
        atom_pad=atom_pad,
        atom_weight=np.asarray([w for _, w in atoms], dtype=np.float64),
        atom_count=len(atoms),
        site_count=len(sites),
    )


def unit_to_container(charge: Charge) -> float:
    """The scale from the unit frame ``[0, U]^2`` to the L container; also ``A_U``."""
    return float(charge.container / CAP_U)


def charge_at_pose(charge: Charge, parent: float, x: float, y: float, theta: float) -> int:
    """The open-parent charge of one pose in the L container, summed directly."""
    cosine, sine = math.cos(theta), math.sin(theta)
    du = cosine * (charge.site_x - x) + sine * (charge.site_y - y)
    dv = -sine * (charge.site_x - x) + cosine * (charge.site_y - y)
    half = parent / 2
    captured = (np.abs(du) < half) & (np.abs(dv) < half)
    inside = captured[charge.atom_sites] | charge.atom_pad
    fires = inside.all(axis=1)
    return round(float(charge.atom_weight[fires].sum()))


@dataclass(frozen=True, slots=True)
class SweepResult:
    theta_degrees: float
    minimum: int
    x: float
    y: float
    arrangement_cells: int
    rectangles: int


def _region_in_container(
    charge: Charge, cell: tuple[int, int], parent: float, theta: float
) -> tuple[float, float, float, float]:
    """The closed H259 cell, cut to the legal centre envelope, in container coordinates."""
    scale = unit_to_container(charge)
    i, j = cell
    x_low = float(CENTRE_LOW + i * CELL_SIDE) * scale
    x_high = float(CENTRE_LOW + (i + 1) * CELL_SIDE) * scale
    y_low = float(CENTRE_LOW + j * CELL_SIDE) * scale
    y_high = float(CENTRE_LOW + (j + 1) * CELL_SIDE) * scale
    margin = parent * (abs(math.cos(theta)) + abs(math.sin(theta))) / 2
    side = float(charge.container)
    return (
        max(x_low, margin),
        min(x_high, side - margin),
        max(y_low, margin),
        min(y_high, side - margin),
    )


def sweep_cell(
    charge: Charge, parent: float, cell: tuple[int, int], theta_degrees: float
) -> SweepResult:
    """Exact-in-position minimum of the open-parent charge over a cell at one angle.

    Every atom's capture set is an open rectangle in the rotated centre frame. The
    arrangement of those rectangles over the region is swept slab by slab, and the charge
    at the midpoint of every arrangement cell whose midpoint lies in the closed region is
    recorded. The result is the least of them, which is the charge of a legal pose.
    """
    theta = math.radians(theta_degrees)
    cosine, sine = math.cos(theta), math.sin(theta)
    half = parent / 2
    u = cosine * charge.site_x + sine * charge.site_y
    v = -sine * charge.site_x + cosine * charge.site_y
    atom_u = u[charge.atom_sites]
    atom_v = v[charge.atom_sites]
    pad = charge.atom_pad
    u0 = np.where(pad, -np.inf, atom_u).max(axis=1) - half
    u1 = np.where(pad, np.inf, atom_u).min(axis=1) + half
    v0 = np.where(pad, -np.inf, atom_v).max(axis=1) - half
    v1 = np.where(pad, np.inf, atom_v).min(axis=1) + half
    x_low, x_high, y_low, y_high = _region_in_container(charge, cell, parent, theta)
    if x_high <= x_low or y_high <= y_low:
        raise ValueError("the legal part of the cell is empty at this angle")
    corners_x = np.asarray([x_low, x_high, x_high, x_low])
    corners_y = np.asarray([y_low, y_low, y_high, y_high])
    box_u = cosine * corners_x + sine * corners_y
    box_v = -sine * corners_x + cosine * corners_y
    ub0, ub1 = float(box_u.min()), float(box_u.max())
    vb0, vb1 = float(box_v.min()), float(box_v.max())
    keep = (u0 < u1) & (v0 < v1) & (u1 > ub0) & (u0 < ub1) & (v1 > vb0) & (v0 < vb1)
    u0 = np.maximum(u0[keep], ub0)
    u1 = np.minimum(u1[keep], ub1)
    v0 = np.maximum(v0[keep], vb0)
    v1 = np.minimum(v1[keep], vb1)
    weights = charge.atom_weight[keep]
    u_events = np.unique(np.concatenate((u0, u1)))
    v_events = np.unique(np.concatenate((v0, v1)))
    iu0 = np.searchsorted(u_events, u0)
    iu1 = np.searchsorted(u_events, u1)
    iv0 = np.searchsorted(v_events, v0)
    iv1 = np.searchsorted(v_events, v1)
    slab_count = len(u_events) - 1
    v_count = len(v_events) - 1
    width = v_count + 1
    v_mid = (v_events[:-1] + v_events[1:]) / 2
    u_mid = (u_events[:-1] + u_events[1:]) / 2
    order_start = np.argsort(iu0, kind="stable")
    order_end = np.argsort(iu1, kind="stable")
    starts_sorted = iu0[order_start]
    ends_sorted = iu1[order_end]
    profile = np.zeros(width, dtype=np.float64)
    best = math.inf
    best_pose = (math.nan, math.nan)
    counted = 0
    for block_start in range(0, slab_count, SLAB_BLOCK):
        block_end = min(block_start + SLAB_BLOCK, slab_count)
        rows = block_end - block_start
        flat: list[FloatArray] = []
        flat_weights: list[FloatArray] = []
        for sorted_index, order, sign in (
            (starts_sorted, order_start, 1.0),
            (ends_sorted, order_end, -1.0),
        ):
            lo = int(np.searchsorted(sorted_index, block_start, side="left"))
            hi = int(np.searchsorted(sorted_index, block_end, side="left"))
            if hi == lo:
                continue
            chosen = order[lo:hi]
            local = (sorted_index[lo:hi] - block_start).astype(np.float64)
            flat.append(local * width + iv0[chosen])
            flat_weights.append(sign * weights[chosen])
            flat.append(local * width + iv1[chosen])
            flat_weights.append(-sign * weights[chosen])
        if flat:
            delta = np.bincount(
                np.concatenate(flat).astype(np.int64),
                weights=np.concatenate(flat_weights),
                minlength=rows * width,
            ).reshape(rows, width)
            delta = np.cumsum(delta, axis=0)
            delta += profile
        else:
            delta = np.broadcast_to(profile, (rows, width)).copy()
        charges = np.cumsum(delta, axis=1)[:, :v_count]
        profile = delta[-1].copy()
        block_u = u_mid[block_start:block_end]
        x = cosine * block_u[:, None] - sine * v_mid[None, :]
        y = sine * block_u[:, None] + cosine * v_mid[None, :]
        inside = (x >= x_low) & (x <= x_high) & (y >= y_low) & (y <= y_high)
        if not inside.any():
            continue
        counted += int(inside.sum())
        masked = np.where(inside, charges, np.inf)
        position = int(np.argmin(masked))
        value = float(masked.flat[position])
        if value < best:
            best = value
            row, column = divmod(position, v_count)
            best_pose = (float(x[row, column]), float(y[row, column]))
    if not math.isfinite(best):
        raise ValueError("no arrangement cell met the region")
    return SweepResult(
        theta_degrees=theta_degrees,
        minimum=round(best),
        x=best_pose[0],
        y=best_pose[1],
        arrangement_cells=counted,
        rectangles=int(keep.sum()),
    )


def _angle_grid(start: float, stop: float, step: float) -> list[float]:
    count = round((stop - start) / step)
    return [round(start + k * step, 9) for k in range(count + 1)]


def floor_for_class(
    name: str, coarse_step: float, fine_steps: tuple[float, float]
) -> dict[str, Any]:
    """Coarse-to-fine angle scan of one cell class; exact in position at every angle."""
    charge = load_charge()
    parent = unit_to_container(charge)
    cell = CLASS_REPRESENTATIVES[name]
    diagonal = cell[0] == cell[1]
    top = 45.0 if diagonal else 90.0 - coarse_step
    started = time.perf_counter()
    rows: list[SweepResult] = []
    seen: set[float] = set()

    def scan(angles: list[float]) -> None:
        for angle in angles:
            key = round(angle % 90.0, 9)
            if key in seen or (diagonal and key > 45.0):
                continue
            seen.add(key)
            rows.append(sweep_cell(charge, parent, cell, key))

    scan(_angle_grid(0.0, top, coarse_step))
    step_mid, step_fine = fine_steps
    for radius, step, breadth in ((coarse_step, step_mid, 2), (step_mid, step_fine, 1)):
        rows.sort(key=lambda row: row.minimum)
        for row in rows[:breadth]:
            scan(_angle_grid(row.theta_degrees - radius, row.theta_degrees + radius, step))
    rows.sort(key=lambda row: (row.minimum, row.theta_degrees))
    best = rows[0]
    scale = unit_to_container(charge)
    return {
        "class": name,
        "cell": list(cell),
        "angles_swept": len(rows),
        "floor_upper_estimate": best.minimum,
        "witness_pose_unit_frame": {
            "x": best.x / scale,
            "y": best.y / scale,
            "theta_degrees": best.theta_degrees,
        },
        "witness_direct_recount": charge_at_pose(
            charge, parent, best.x, best.y, math.radians(best.theta_degrees)
        ),
        "witness_charge_constant_within_1e-9": all(
            charge_at_pose(
                charge,
                parent,
                best.x + dx,
                best.y + dy,
                math.radians(best.theta_degrees + dt),
            )
            == best.minimum
            for dx, dy, dt in PERTURBATIONS
        ),
        "coarse_minimum_by_angle": [
            [row.theta_degrees, row.minimum]
            for row in sorted(rows, key=lambda row: row.theta_degrees)
            if abs(row.theta_degrees / coarse_step - round(row.theta_degrees / coarse_step))
            < 1e-9
        ],
        "arrangement_cells_per_angle_mean": float(
            np.mean([row.arrangement_cells for row in rows])
        ),
        "rectangles_per_angle_mean": float(np.mean([row.rectangles for row in rows])),
        "seconds": time.perf_counter() - started,
    }


def _floor_task(args: tuple[str, float, tuple[float, float]]) -> dict[str, Any]:
    return floor_for_class(*args)


def cell_class(cell: tuple[int, int]) -> str:
    """The D4 class name of a cell of the 5 x 5 grid."""
    i, j = (min(k, GRID - 1 - k) for k in cell)
    i, j = min(i, j), max(i, j)
    return {
        (0, 0): "corner",
        (0, 1): "edge-near-corner",
        (0, 2): "edge-middle",
        (1, 1): "interior-corner",
        (1, 2): "interior-edge",
        (2, 2): "centre",
    }[(i, j)]


def is_boundary(cell: tuple[int, int]) -> bool:
    return 0 in cell or GRID - 1 in cell


def _d4_permutations() -> list[list[int]]:
    cells = [(i, j) for i in range(GRID) for j in range(GRID)]
    index = {cell: k for k, cell in enumerate(cells)}
    last = GRID - 1
    images = (
        lambda i, j: (i, j),
        lambda i, j: (last - i, j),
        lambda i, j: (i, last - j),
        lambda i, j: (last - i, last - j),
        lambda i, j: (j, i),
        lambda i, j: (last - j, i),
        lambda i, j: (j, last - i),
        lambda i, j: (last - j, last - i),
    )
    return [[index[image(i, j)] for i, j in cells] for image in images]


def _blocks(size: int) -> list[list[int]]:
    return [
        [(i + di) * GRID + (j + dj) for di in range(size) for dj in range(size)]
        for i in range(GRID - size + 1)
        for j in range(GRID - size + 1)
    ]


CLASS_NAMES = tuple(CLASS_REPRESENTATIVES)
#: Mixed radix of the class-count key: corner <= 4, edge-near-corner <= 8, edge-middle <= 4.
BOUNDARY_KEY_RADIX = (1, 5, 45)
BOUNDARY_KEYS = 225
#: Interior-corner <= 8, interior-edge <= 8, centre <= 2.
INTERIOR_KEY_RADIX = (1, 9, 81)
INTERIOR_KEYS = 243


def _class_counts_from_keys(boundary_key: int, interior_key: int) -> tuple[int, ...]:
    corner, rest = boundary_key % 5, boundary_key // 5
    near, middle = rest % 9, rest // 9
    inner_corner, rest = interior_key % 9, interior_key // 9
    inner_edge, centre = rest % 9, rest // 9
    return (corner, near, middle, inner_corner, inner_edge, centre)


def count_survivors(floors_by_cell: list[int], budget: int) -> dict[str, Any]:
    """Exact state and D4-orbit counts under the cuts, the floor test, and both.

    Also returns, for the cut survivors, the exact orbit count of every class-count
    vector (how many centres sit in each of the six D4 cell classes), which is what any
    class-symmetric per-cell floor vector can and cannot separate.
    """
    started = time.perf_counter()
    cells = [(i, j) for i in range(GRID) for j in range(GRID)]
    boundary = [k for k, cell in enumerate(cells) if is_boundary(cell)]
    interior = [k for k, cell in enumerate(cells) if not is_boundary(cell)]
    boundary_position = {k: p for p, k in enumerate(boundary)}
    interior_position = {k: p for p, k in enumerate(interior)}
    boundary_vectors = (
        (np.arange(1 << len(boundary))[:, None] >> np.arange(len(boundary))) & 1
    ).astype(np.int64)
    interior_vectors = (
        (np.arange(3 ** len(interior))[:, None] // (3 ** np.arange(len(interior)))) % 3
    ).astype(np.int64)
    boundary_class = np.asarray(
        [CLASS_NAMES.index(cell_class(cells[k])) for k in boundary], dtype=np.int64
    )
    interior_class = np.asarray(
        [CLASS_NAMES.index(cell_class(cells[k])) - 3 for k in interior], dtype=np.int64
    )
    boundary_key = np.zeros(len(boundary_vectors), dtype=np.int64)
    for c, radix in enumerate(BOUNDARY_KEY_RADIX):
        boundary_key += radix * boundary_vectors[:, boundary_class == c].sum(axis=1)
    interior_key = np.zeros(len(interior_vectors), dtype=np.int64)
    for c, radix in enumerate(INTERIOR_KEY_RADIX):
        interior_key += radix * interior_vectors[:, interior_class == c].sum(axis=1)

    def split(block: list[int]) -> tuple[IntArray, IntArray]:
        b = np.zeros(len(boundary), dtype=np.int64)
        i = np.zeros(len(interior), dtype=np.int64)
        for k in block:
            if k in boundary_position:
                b[boundary_position[k]] = 1
            else:
                i[interior_position[k]] = 1
        return b, i

    def block_sums(size: int) -> tuple[IntArray, IntArray]:
        parts = [split(block) for block in _blocks(size)]
        b = np.stack([part[0] for part in parts], axis=1)
        i = np.stack([part[1] for part in parts], axis=1)
        return boundary_vectors @ b, interior_vectors @ i

    boundary_2x2, interior_2x2 = block_sums(2)
    boundary_3x3, interior_3x3 = block_sums(3)
    floor_boundary = boundary_vectors @ np.asarray([floors_by_cell[k] for k in boundary])
    floor_interior = interior_vectors @ np.asarray([floors_by_cell[k] for k in interior])
    boundary_sum = boundary_vectors.sum(axis=1)
    interior_sum = interior_vectors.sum(axis=1)
    by_sum = [np.flatnonzero(boundary_sum == s) for s in range(len(boundary) + 1)]
    fixed_boundary: list[BoolArray] = []
    fixed_interior: list[BoolArray] = []
    for permutation in _d4_permutations():
        pb = [boundary_position[permutation[k]] for k in boundary]
        pi = [interior_position[permutation[k]] for k in interior]
        fixed_boundary.append((boundary_vectors == boundary_vectors[:, pb]).all(axis=1))
        fixed_interior.append((interior_vectors == interior_vectors[:, pi]).all(axis=1))
    names: tuple[str, ...] = ("all", "cuts", "floors", "both")
    states: dict[str, int] = dict.fromkeys(names, 0)
    fixed = {name: [0] * 8 for name in names}
    class_fixed = np.zeros((8, INTERIOR_KEYS, BOUNDARY_KEYS), dtype=np.int64)
    for row in range(len(interior_vectors)):
        need = N - int(interior_sum[row])
        if need < 0 or need > len(boundary):
            continue
        idx = by_sum[need]
        cuts_ok = ((boundary_2x2[idx] + interior_2x2[row]) <= CUT_2X2).all(axis=1) & (
            (boundary_3x3[idx] + interior_3x3[row]) <= CUT_3X3
        ).all(axis=1)
        floors_ok = (floor_boundary[idx] + floor_interior[row]) <= budget
        masks = {
            "all": np.ones(len(idx), dtype=bool),
            "cuts": cuts_ok,
            "floors": floors_ok,
            "both": cuts_ok & floors_ok,
        }
        for name, mask in masks.items():
            states[name] += int(mask.sum())
            for g in range(8):
                if fixed_interior[g][row]:
                    fixed[name][g] += int((mask & fixed_boundary[g][idx]).sum())
        for g in range(8):
            if fixed_interior[g][row]:
                chosen = cuts_ok & fixed_boundary[g][idx]
                class_fixed[g, interior_key[row]] += np.bincount(
                    boundary_key[idx][chosen], minlength=BOUNDARY_KEYS
                )
    result: dict[str, Any] = {"seconds": time.perf_counter() - started}
    for name in names:
        total = sum(fixed[name])
        if total % 8:
            raise ValueError("Burnside sum is not divisible by the group order")
        result[name] = {
            "states": states[name],
            "orbits": total // 8,
            "fixed_by_symmetry": fixed[name],
        }
    class_total = class_fixed.sum(axis=0)
    if (class_total % 8).any():
        raise ValueError("a class-count Burnside sum is not divisible by eight")
    class_orbits = class_total // 8
    result["cut_orbits_by_class_counts"] = {
        ",".join(map(str, _class_counts_from_keys(b, i))): int(class_orbits[i, b])
        for i in range(INTERIOR_KEYS)
        for b in range(BOUNDARY_KEYS)
        if class_orbits[i, b]
    }
    return result


def class_floor_ceiling(
    orbits_by_class_counts: dict[str, int], endpoint_counts: tuple[int, ...], seed: int
) -> dict[str, Any]:
    """What any class-symmetric per-cell floor vector must leave among the cut survivors.

    A floor vector ``f`` over the six cell classes keeps every class-count vector ``n``
    with ``(n - n*) . f <= 0``, where ``n*`` is the endpoint's own vector, which must
    survive. Two rigorous lower bounds on the survivors of every ``f``: the orbits whose
    class counts equal ``n*`` (never separable), and for every antipodal pair
    ``n* + d``, ``n* - d`` of feasible vectors the smaller of the two counts (one of the
    pair survives). A random search over ``f`` gives an upper bound on the best achievable
    count.
    """
    vectors = {
        tuple(int(part) for part in key.split(",")): count
        for key, count in orbits_by_class_counts.items()
    }
    same = vectors.get(endpoint_counts, 0)
    pair_bound = same
    seen: set[tuple[int, ...]] = set()
    for n, count in vectors.items():
        d = tuple(a - b for a, b in zip(n, endpoint_counts, strict=True))
        if not any(d) or d in seen:
            continue
        mirror = tuple(a - b for a, b in zip(endpoint_counts, d, strict=True))
        if mirror in vectors:
            neg = tuple(-x for x in d)
            seen.add(d)
            seen.add(neg)
            pair_bound += min(count, vectors[mirror])
    keys = np.asarray(list(vectors), dtype=np.float64)
    counts = np.asarray(list(vectors.values()), dtype=np.int64)
    differences = keys - np.asarray(endpoint_counts, dtype=np.float64)
    rng = np.random.default_rng(seed)
    best = int(counts.sum())
    best_direction = [0.0] * len(endpoint_counts)
    for _ in range(20000):
        direction = rng.standard_normal(len(endpoint_counts))
        survivors = int(counts[(differences @ direction) <= 1e-9].sum())
        if survivors < best:
            best = survivors
            best_direction = [float(x) for x in direction]
    return {
        "endpoint_class_counts": list(endpoint_counts),
        "class_count_vectors": len(vectors),
        "orbits_with_endpoint_class_counts": same,
        "antipodal_pair_lower_bound": pair_bound,
        "random_search_best_survivors": best,
        "random_search_best_direction": best_direction,
    }


def orientation_split_summary(
    class_rows: list[dict[str, Any]], threshold: Fraction
) -> dict[str, Any]:
    """What floors split by orientation could do, read off the coarse angle grid.

    For each class: the largest per-angle minimum over the sampled angles (the best an
    orientation-split floor could be at any sampled angle), its excess over ``M / 17``,
    and the share of sampled angles at which the per-angle minimum reaches ``M / 17``.
    Every pattern has at least eight boundary centres (the interior 3 x 3 block holds at
    most nine), so ``9 * max interior excess + 8 * max boundary excess`` bounds the sum of
    excesses of any pattern under any orientation assignment at the sampled angles; a
    negative value means no pattern is excluded even with orientation-split floors.
    """
    summary: dict[str, Any] = {}
    best_boundary = -math.inf
    best_interior = -math.inf
    for row in class_rows:
        minima = [(float(angle), int(value)) for angle, value in row["coarse_minimum_by_angle"]]
        top_angle, top = max(minima, key=lambda item: item[1])
        excess = float(top - threshold)
        name = row["class"]
        summary[name] = {
            "max_per_angle_minimum": top,
            "at_theta_degrees": top_angle,
            "excess_over_budget_over_17": excess,
            "share_of_angles_at_or_above_budget_over_17": sum(
                value >= threshold for _, value in minima
            )
            / len(minima),
            "angles": len(minima),
        }
        if is_boundary(CLASS_REPRESENTATIVES[name]):
            best_boundary = max(best_boundary, excess)
        else:
            best_interior = max(best_interior, excess)
    return {
        "by_class": summary,
        "max_boundary_excess": best_boundary,
        "max_interior_excess": best_interior,
        "pattern_excess_bound": 9 * best_interior + 8 * best_boundary,
        "any_pattern_excludable_at_sampled_angles": 9 * best_interior + 8 * best_boundary > 0,
    }


def endpoint_control(charge: Charge, floors_by_class: dict[str, int]) -> dict[str, Any]:
    """The endpoint's own charges and floor sum, which must not exceed the budget."""
    parent = unit_to_container(charge)
    scale = unit_to_container(charge)
    charges: list[int] = []
    for x, y, degrees in ENDPOINT_POSES:
        charges.append(
            charge_at_pose(charge, parent, x * scale, y * scale, math.radians(degrees))
        )
    classes = [cell_class(cell) for cell in ENDPOINT_CELLS]
    floor_sum = sum(floors_by_class[name] for name in classes)
    below = [
        (k, charges[k], floors_by_class[classes[k]])
        for k in range(N)
        if charges[k] < floors_by_class[classes[k]]
    ]
    return {
        "pose_charges": charges,
        "pose_classes": classes,
        "charge_sum": sum(charges),
        "charge_sum_minus_budget": sum(charges) - charge.budget,
        "floor_sum": floor_sum,
        "floor_sum_minus_budget": floor_sum - charge.budget,
        "survives_floor_test": floor_sum <= charge.budget,
        "poses_below_their_class_floor": below,
        "class_counts": {name: classes.count(name) for name in CLASS_REPRESENTATIVES},
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    _ = parser.add_argument("--output", type=Path, required=True)
    _ = parser.add_argument("--workers", type=int, default=2)
    _ = parser.add_argument("--coarse-step", type=float, default=1.0)
    _ = parser.add_argument("--mid-step", type=float, default=0.05)
    _ = parser.add_argument("--fine-step", type=float, default=0.005)
    _ = parser.add_argument("--seed", type=int, default=20261002)
    _ = parser.add_argument(
        "--classes", nargs="*", default=list(CLASS_REPRESENTATIVES), help="classes to sweep"
    )
    _ = parser.add_argument(
        "--floors-json",
        type=Path,
        default=None,
        help="reuse the floors of an earlier output and only recount",
    )
    args = parser.parse_args(argv)
    started = time.perf_counter()
    charge = load_charge()
    parent = unit_to_container(charge)
    gamma_r068 = 1000026844
    print(
        f"sites {charge.site_count} atoms {charge.atom_count} budget {charge.budget} "
        f"A_R068 {float(charge.parent_side_r068):.9f} A_U {parent:.9f}",
        flush=True,
    )
    if args.floors_json is not None:
        earlier = json.loads(Path(args.floors_json).read_text())
        class_rows: list[dict[str, Any]] = earlier["floors"]
    else:
        tasks = [
            (name, args.coarse_step, (args.mid_step, args.fine_step)) for name in args.classes
        ]
        if args.workers > 1:
            with Pool(args.workers) as pool:
                class_rows = pool.map(_floor_task, tasks)
        else:
            class_rows = [_floor_task(task) for task in tasks]
        for row in class_rows:
            print(
                f"{row['class']:18s} floor<= {row['floor_upper_estimate']} "
                f"at theta={row['witness_pose_unit_frame']['theta_degrees']:.3f} "
                f"({row['angles_swept']} angles, {row['seconds']:.0f} s)",
                flush=True,
            )
    floors_by_class = {row["class"]: int(row["floor_upper_estimate"]) for row in class_rows}
    missing = [name for name in CLASS_REPRESENTATIVES if name not in floors_by_class]
    if missing:
        raise ValueError(f"no floor for classes {missing}")
    cells = [(i, j) for i in range(GRID) for j in range(GRID)]
    floors_by_cell = [floors_by_class[cell_class(cell)] for cell in cells]
    threshold = Fraction(charge.budget, N)
    counts = count_survivors(floors_by_cell, charge.budget)
    control = endpoint_control(charge, floors_by_class)
    endpoint_counts = tuple(control["class_counts"][name] for name in CLASS_NAMES)
    ceiling = class_floor_ceiling(
        counts["cut_orbits_by_class_counts"], endpoint_counts, seed=args.seed
    )
    gamma_u = min(floors_by_class.values())
    result = {
        "schema": "pilot-n17-charge-floors/v1",
        "charge": {
            "source": "R068 certificate 116511/25000, sites, rules and weights unchanged",
            "container_L": str(charge.container),
            "cap_U": str(CAP_U),
            "parent_side_A_U": parent,
            "parent_side_A_R068": float(charge.parent_side_r068),
            "parent_shrink_relative": 1 - parent / float(charge.parent_side_r068),
            "budget_M": charge.budget,
            "budget_over_17": float(threshold),
            "gamma_r068": gamma_r068,
            "seventeen_gamma_minus_M_r068": N * gamma_r068 - charge.budget,
            "sites": charge.site_count,
            "atoms": charge.atom_count,
            "definition": "open A_U-parent capture of R068's sites; pose charge = sum of "
            "signed Mobius atoms whose sites all lie strictly inside the parent",
        },
        "floors": class_rows,
        "floors_by_class": floors_by_class,
        "floor_minus_budget_over_17": {
            name: float(value - threshold) for name, value in floors_by_class.items()
        },
        "gamma_u_upper_estimate": gamma_u,
        "seventeen_gamma_u_minus_M": N * gamma_u - charge.budget,
        "endpoint_control": control,
        "counts": counts,
        "class_floor_ceiling": ceiling,
        "orientation_split": orientation_split_summary(class_rows, threshold),
        "seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=1))
    summary = {k: v for k, v in result.items() if k != "floors"}
    summary["counts"] = {k: v for k, v in counts.items() if k != "cut_orbits_by_class_counts"}
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
