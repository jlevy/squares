"""Linear closed-core coverage on a frozen U025 orbit-weight vector.

Once every point coordinate, threshold triple, D4 image, shrink, and direction net is
held fixed, Condition 5' is linear in the orbit weights. At one net direction the event
grid is the arrangement of the frozen sites; a zero-weight orbit still makes events and
no charge. On each reachable open cell the covering pattern of the frozen atoms is a
constant 0/1 (point) or ``[m >= k]`` (threshold) vector, so the cell charge is
``A_cell · w``. D4 tying is the choice of one weight per source orbit.

Omitting an inactive orbit from a decompressed certificate coarsens that arrangement.
Charge depends only on the remaining positive weights, so the minimum over the frozen
cells equals the minimum over the omitted-atom cells. Encoding ``A w >= 1`` on the frozen
Pareto-minimal rows is therefore equivalent to least-charge ``>= 1`` for every Route S
family member, including sparse ones.

This module enumerates that system. It does not solve it, does not run a coverage
verifier on a decompressed candidate, and does not treat a coverage-free cardinality MIP
as an H-163 result.
"""

from __future__ import annotations

import hashlib
from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Literal

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

from sqpack.fractional.model import Atom, Direction, rotation_from_half_tangent
from sqpack.fractional.sweep import reduce_to_spans
from sqpack.fractional.threshold_compression import OrbitInventory

type SearchSolveStatus = Literal[
    "not_run",
    "feasible_unverified",
    "float_infeasible_unresolved",
    "timeout_unresolved",
    "solver_error_unresolved",
]


@dataclass(frozen=True, slots=True)
class _ThresholdMemberPaint:
    """One frozen threshold-orbit image, as event-atom indices and token counts."""

    threshold: int
    sites: tuple[tuple[int, int], ...]


@dataclass(frozen=True, slots=True)
class FrozenCoverageGeometry:
    """Event-making atoms for the frozen U025 sites, indexed per orbit."""

    event_atoms: tuple[Atom, ...]
    point_orbits: tuple[tuple[int, ...], ...]
    threshold_orbits: tuple[tuple[_ThresholdMemberPaint, ...], ...]


@dataclass(frozen=True, slots=True)
class FrozenCoverageEncoding:
    """Pareto-reduced ``A w >= 1`` system on frozen orbit weights."""

    orbit_count: int
    direction_count: int
    reachable_cells: int
    direction_unique_rows: int
    pareto_rows: np.ndarray
    budget_coefficients: tuple[int, ...]
    rows_sha256: str

    @property
    def pareto_row_count(self) -> int:
        return int(self.pareto_rows.shape[0])


@dataclass(frozen=True, slots=True)
class CoverageMipOutcome:
    """Float HiGHS feasibility of the encoded MIP; never an H-163 verdict."""

    status: SearchSolveStatus
    n_plus: int | None
    weights: tuple[float, ...] | None
    objective: float | None
    message: str


_EVENT_ONLY = Fraction(0)
_WEIGHT_UPPER = 11.0
_BUDGET_UPPER = 11.0 - 1e-9


def frozen_coverage_geometry(inventory: OrbitInventory) -> FrozenCoverageGeometry:
    """Build zero-weight event atoms for every frozen U025 site, in orbit order."""

    events: list[Atom] = []
    point_orbits: list[tuple[int, ...]] = []
    for orbit_index, orbit in enumerate(inventory.point_orbits):
        members: list[int] = []
        for member_index, (x, y) in enumerate(orbit.members):
            members.append(len(events))
            events.append(Atom(f"p{orbit_index}:{member_index}", x, y, _EVENT_ONLY))
        point_orbits.append(tuple(members))

    threshold_orbits: list[tuple[_ThresholdMemberPaint, ...]] = []
    for orbit_index, orbit in enumerate(inventory.threshold_orbits):
        members_paint: list[_ThresholdMemberPaint] = []
        for member_index, key in enumerate(orbit.members):
            sites, threshold = key
            painted: list[tuple[int, int]] = []
            for site_index, (x, y, count) in enumerate(sites):
                painted.append((len(events), count))
                events.append(
                    Atom(f"t{orbit_index}:{member_index}:{site_index}", x, y, _EVENT_ONLY)
                )
            members_paint.append(_ThresholdMemberPaint(threshold, tuple(painted)))
        threshold_orbits.append(tuple(members_paint))

    return FrozenCoverageGeometry(tuple(events), tuple(point_orbits), tuple(threshold_orbits))


def _paint(
    target: np.ndarray,
    u_index: dict[Fraction, int],
    v_index: dict[Fraction, int],
    rectangle: tuple[Fraction, ...],
    value: int,
) -> None:
    u1, u2, v1, v2 = rectangle[:4]
    target[u_index[u1], v_index[v1]] += value
    target[u_index[u2], v_index[v1]] -= value
    target[u_index[u1], v_index[v2]] -= value
    target[u_index[u2], v_index[v2]] += value


def _reachable_cells(spans: tuple[tuple[int, int, int], ...]) -> tuple[np.ndarray, np.ndarray]:
    count = sum(j1 - j0 + 1 for _, j0, j1 in spans)
    cell_i = np.empty(count, dtype=np.int32)
    cell_j = np.empty(count, dtype=np.int32)
    offset = 0
    for i, j0, j1 in spans:
        width = j1 - j0 + 1
        cell_i[offset : offset + width] = i
        cell_j[offset : offset + width] = np.arange(j0, j1 + 1, dtype=np.int32)
        offset += width
    return cell_i, cell_j


def unique_rows(rows: np.ndarray) -> np.ndarray:
    """Lexicographically stable unique rows of a C-contiguous integer matrix."""

    if rows.size == 0:
        return np.zeros((0, rows.shape[1]), dtype=rows.dtype)
    flat = np.ascontiguousarray(rows)
    keys = flat.view(np.dtype((np.void, flat.shape[1] * flat.dtype.itemsize)))
    _, index = np.unique(keys, return_index=True)
    return rows[np.sort(index)]


def pareto_minimal_rows(rows: np.ndarray) -> np.ndarray:
    """Rows not componentwise greater-or-equal to another distinct row.

    For ``w >= 0``, ``b · w >= 1`` implies ``a · w >= 1`` whenever ``b <= a``
    coordinatewise, so dominated covering vectors are redundant inequalities.
    """

    unique = unique_rows(rows)
    if unique.shape[0] <= 1:
        return unique
    order = np.argsort(unique.sum(axis=1), kind="stable")
    ordered = unique[order]
    kept: list[int] = []
    for index, row in enumerate(ordered):
        if any(np.all(ordered[held] <= row) for held in kept):
            continue
        kept.append(index)
    return np.ascontiguousarray(ordered[np.array(kept, dtype=np.intp)])


def _rows_sha256(rows: np.ndarray) -> str:
    if rows.size == 0:
        return hashlib.sha256(b"").hexdigest()
    columns = tuple(rows[:, column] for column in range(rows.shape[1] - 1, -1, -1))
    ordered = np.ascontiguousarray(rows[np.lexsort(columns)])
    return hashlib.sha256(ordered.tobytes()).hexdigest()


def direction_coverage_rows(
    inventory: OrbitInventory,
    geometry: FrozenCoverageGeometry,
    direction: Direction,
) -> tuple[np.ndarray, int]:
    """Unique integer covering rows of one frozen-arrangement direction."""

    reduction = reduce_to_spans(
        geometry.event_atoms, direction, inventory.outer_side, inventory.square_side
    )
    u_index = {value: index for index, value in enumerate(reduction.u_events)}
    v_index = {value: index for index, value in enumerate(reduction.v_events)}
    width, height = len(reduction.u_events), len(reduction.v_events)
    cell_i, cell_j = _reachable_cells(reduction.spans)
    n_cells = int(cell_i.size)
    rows = np.zeros((n_cells, inventory.orbit_count), dtype=np.uint8)
    orbit_index = 0
    for members in geometry.point_orbits:
        grid = np.zeros((width, height), dtype=np.int32)
        for event_index in members:
            _paint(grid, u_index, v_index, reduction.rectangles[event_index], 1)
        np.cumsum(grid, axis=1, out=grid)
        np.cumsum(grid, axis=0, out=grid)
        column = grid[cell_i, cell_j]
        if int(column.max(initial=0)) > 255:
            raise ValueError("point-orbit coverage coefficient exceeds uint8")
        rows[:, orbit_index] = column
        orbit_index += 1
    for members in geometry.threshold_orbits:
        grid = np.zeros((width, height), dtype=np.int32)
        for member in members:
            counts = np.zeros((width, height), dtype=np.int32)
            for event_index, multiplicity in member.sites:
                _paint(
                    counts,
                    u_index,
                    v_index,
                    reduction.rectangles[event_index],
                    multiplicity,
                )
            np.cumsum(counts, axis=1, out=counts)
            np.cumsum(counts, axis=0, out=counts)
            grid += counts >= member.threshold
        column = grid[cell_i, cell_j]
        if int(column.max(initial=0)) > 255:
            raise ValueError("threshold-orbit coverage coefficient exceeds uint8")
        rows[:, orbit_index] = column
        orbit_index += 1
    return unique_rows(rows), n_cells


def orbit_weights(inventory: OrbitInventory) -> tuple[Fraction, ...]:
    """Source orbit weights in the catalog's mixed point-then-threshold order."""

    return tuple(
        orbit.weight for orbit in (*inventory.point_orbits, *inventory.threshold_orbits)
    )


def budget_coefficients(inventory: OrbitInventory) -> tuple[int, ...]:
    """Condition 2' coefficients of the frozen orbits."""

    return tuple(
        orbit.budget_coefficient
        for orbit in (*inventory.point_orbits, *inventory.threshold_orbits)
    )


def _solver_bound(values: np.ndarray) -> Any:
    """scipy's stubs type constraint bounds as scalars; HiGHS takes arrays."""

    return values


def minimum_encoded_charge(rows: np.ndarray, weights: Sequence[Fraction]) -> Fraction:
    """Exact ``min A_cell · w`` over the supplied integer rows."""

    if rows.size == 0:
        raise ValueError("coverage encoding has no rows")
    if rows.shape[1] != len(weights):
        raise ValueError("row width does not match the orbit-weight vector")
    best: Fraction | None = None
    for row in rows:
        charge = sum(
            (
                int(coefficient) * weight
                for coefficient, weight in zip(row, weights, strict=True)
            ),
            start=Fraction(0),
        )
        if best is None or charge < best:
            best = charge
    if best is None:
        raise ValueError("coverage encoding has no rows")
    return best


def encode_frozen_coverage(
    inventory: OrbitInventory,
    *,
    direction_indices: tuple[int, ...] | None = None,
) -> FrozenCoverageEncoding:
    """Enumerate Pareto-minimal frozen covering rows over the requested net directions."""

    if inventory.orbit_count < 1:
        raise ValueError("coverage encoding requires at least one orbit")
    geometry = frozen_coverage_geometry(inventory)
    if direction_indices is None:
        indices = tuple(range(len(inventory.half_tangents)))
    else:
        indices = direction_indices
        for index in indices:
            if index < 0 or index >= len(inventory.half_tangents):
                raise ValueError(f"direction index {index} is outside the frozen net")
    pareto = np.zeros((0, inventory.orbit_count), dtype=np.uint8)
    reachable = 0
    unique_sum = 0
    for index in indices:
        direction = rotation_from_half_tangent(str(index), inventory.half_tangents[index])
        rows, n_cells = direction_coverage_rows(inventory, geometry, direction)
        reachable += n_cells
        unique_sum += int(rows.shape[0])
        stacked = rows if pareto.shape[0] == 0 else np.vstack((pareto, rows))
        pareto = pareto_minimal_rows(stacked)
    if pareto.shape[0] == 0:
        raise ValueError("frozen coverage encoding produced no reachable cells")
    return FrozenCoverageEncoding(
        orbit_count=inventory.orbit_count,
        direction_count=len(indices),
        reachable_cells=reachable,
        direction_unique_rows=unique_sum,
        pareto_rows=pareto,
        budget_coefficients=budget_coefficients(inventory),
        rows_sha256=_rows_sha256(pareto),
    )


def encoding_record(encoding: FrozenCoverageEncoding) -> dict[str, Any]:
    """JSON-ready summary of an enumerated encoding; omits the dense row matrix."""

    return {
        "orbit_count": encoding.orbit_count,
        "direction_count": encoding.direction_count,
        "reachable_cells": encoding.reachable_cells,
        "direction_unique_rows": encoding.direction_unique_rows,
        "pareto_row_count": encoding.pareto_row_count,
        "rows_sha256": encoding.rows_sha256,
        "budget_coefficients": list(encoding.budget_coefficients),
        "includes_coverage": True,
        "coverage_linear": True,
    }


def solve_feasibility_mip(
    encoding: FrozenCoverageEncoding,
    *,
    max_orbits: int,
    budget_below: int,
    time_limit_s: float | None = None,
) -> CoverageMipOutcome:
    """Float HiGHS feasibility of ``A w >= 1``, budget ``< 11``, ``N+ <= 23``.

    A timeout or float infeasibility is unresolved, never a scientific rejection.
    A feasible float incumbent is not an H-163 result until exact coverage agrees.
    """

    n_orbits = encoding.orbit_count
    if max_orbits < 1:
        raise ValueError("max_orbits must be a positive integer")
    if budget_below != 11:
        raise ValueError("budget_below must remain the frozen H-163 bound 11")
    coverage = encoding.pareto_rows.astype(np.float64, copy=False)
    zeros = np.zeros((coverage.shape[0], n_orbits), dtype=np.float64)
    coverage_block = np.hstack((-coverage, zeros))
    budget = np.concatenate(
        [np.array(encoding.budget_coefficients, dtype=np.float64), np.zeros(n_orbits)]
    )
    cardinality = np.concatenate([np.zeros(n_orbits), np.ones(n_orbits)])
    links = np.zeros((n_orbits, 2 * n_orbits), dtype=np.float64)
    for index in range(n_orbits):
        links[index, index] = 1.0
        links[index, n_orbits + index] = -_WEIGHT_UPPER
    constraints = [
        LinearConstraint(coverage_block, ub=_solver_bound(np.full(coverage.shape[0], -1.0))),
        LinearConstraint(budget, ub=_BUDGET_UPPER),
        LinearConstraint(cardinality, ub=float(max_orbits)),
        LinearConstraint(links, ub=_solver_bound(np.zeros(n_orbits))),
    ]
    bounds = Bounds(
        lb=_solver_bound(np.zeros(2 * n_orbits)),
        ub=_solver_bound(np.concatenate([np.full(n_orbits, _WEIGHT_UPPER), np.ones(n_orbits)])),
    )
    integrality = np.concatenate(
        [np.zeros(n_orbits, dtype=np.int8), np.ones(n_orbits, dtype=np.int8)]
    )
    cost = np.concatenate([np.zeros(n_orbits), np.ones(n_orbits)])
    options: dict[str, Any] = {}
    if time_limit_s is not None:
        options["time_limit"] = time_limit_s
    try:
        result = milp(
            cost,
            constraints=constraints,
            bounds=bounds,
            integrality=integrality,
            options=options or None,
        )
    except (ValueError, TypeError, RuntimeError) as error:
        return CoverageMipOutcome(
            "solver_error_unresolved", None, None, None, f"HiGHS refused: {error}"
        )
    status = int(result.status)
    if status == 1:
        return CoverageMipOutcome(
            "timeout_unresolved",
            None,
            None,
            None,
            "HiGHS reached its time limit; timeout is unresolved, never rejected",
        )
    if not result.success or result.x is None:
        return CoverageMipOutcome(
            "float_infeasible_unresolved",
            None,
            None,
            None,
            "float MIP reported infeasible; this is not an exact infeasibility certificate",
        )
    weights = tuple(float(value) for value in result.x[:n_orbits])
    n_plus = sum(1 for value in result.x[n_orbits:] if float(value) > 0.5)
    return CoverageMipOutcome(
        "feasible_unverified",
        n_plus,
        weights,
        float(result.fun) if result.fun is not None else float(n_plus),
        "float incumbent is not an H-163 result until exact coverage agrees",
    )
