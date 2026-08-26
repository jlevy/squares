"""Bounded local realization checks for abstract contact scaffolds.

This module solves only assembly-frame contact equalities and positive tangential
overlap inequalities. It does not check container fit, wall contacts, non-edge
separation, or whole-packing feasibility.
"""

from __future__ import annotations

import math
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Literal

import numpy as np
from scipy.optimize import linprog

from sqpack.contact_assembly import (
    CanonicalScaffold,
    ContactScaffold,
    canonicalize_scaffold,
)

type Point = tuple[float, float]
type LocalOutcome = Literal["locally-feasible", "locally-infeasible", "solver-indeterminate"]


class LocalRealizationError(ValueError):
    """A typed malformed-input or unsupported-slice failure."""

    def __init__(self, kind: str, detail: str):
        super().__init__(detail)
        self.kind = kind


@dataclass(frozen=True)
class LocalWitnessCheck:
    """Direct replay of only the constraints owned by this local prefilter."""

    passed: bool
    maximum_normal_residual: float
    minimum_realized_overlap: float | None
    failed_edges: tuple[int, ...]


@dataclass(frozen=True)
class LocalRealizationReceipt:
    canonical_label: str
    outcome: LocalOutcome
    solver_status: int
    lp_solve_index: int
    coordinates: tuple[Point, ...] | None
    witness_check: LocalWitnessCheck | None


@dataclass(frozen=True)
class LocalRealizationBatch:
    status: Literal["completed", "limit"]
    receipts: tuple[LocalRealizationReceipt, ...]
    encountered_candidates: int
    duplicate_candidates: int
    lp_solves: int
    limit_kind: Literal["lp-solve-cap"] | None
    limit: int | None
    pending_canonical_label: str | None


def _validate_parameters(*, minimum_overlap: float, tolerance: float) -> None:
    if not math.isfinite(minimum_overlap) or not 0 < minimum_overlap <= 1:
        raise LocalRealizationError(
            "malformed-overlap",
            "minimum_overlap must be finite and in the interval (0, 1]",
        )
    if not math.isfinite(tolerance) or tolerance <= 0:
        raise LocalRealizationError(
            "malformed-tolerance", "tolerance must be finite and positive"
        )


def _validate_scaffold(scaffold: ContactScaffold) -> None:
    if any(scaffold.wall_contacts):
        raise LocalRealizationError(
            "unsupported-wall-constraints",
            "the local assembly-frame prefilter cannot enforce container walls",
        )
    if len(set(scaffold.vertex_colors)) != 1:
        raise LocalRealizationError(
            "unsupported-angle-classes",
            "the local assembly-frame prefilter requires one uniform vertex angle class",
        )


def check_local_contact_witness(
    scaffold: ContactScaffold,
    coordinates: tuple[Point, ...],
    *,
    minimum_overlap: float,
    tolerance: float = 1e-9,
) -> LocalWitnessCheck:
    """Replay normal equality and tangential overlap, and nothing more."""
    _validate_parameters(minimum_overlap=minimum_overlap, tolerance=tolerance)
    _validate_scaffold(scaffold)
    if len(coordinates) != len(scaffold.vertex_colors) or any(
        len(point) != 2 or any(not math.isfinite(value) for value in point)
        for point in coordinates
    ):
        raise LocalRealizationError(
            "malformed-coordinates",
            "coordinates must contain one finite assembly-frame point per vertex",
        )

    maximum_residual = 0.0
    overlaps: list[float] = []
    failed: list[int] = []
    for edge_index, edge in enumerate(scaffold.edges):
        left_u, left_v = coordinates[edge.left]
        right_u, right_v = coordinates[edge.right]
        delta_u, delta_v = right_u - left_u, right_v - left_v
        normal_delta = delta_u if edge.normal == "u" else delta_v
        tangential_delta = delta_v if edge.normal == "u" else delta_u
        residual = abs(normal_delta - edge.sign)
        overlap = 1 - abs(tangential_delta)
        maximum_residual = max(maximum_residual, residual)
        overlaps.append(overlap)
        if residual > tolerance or overlap + tolerance < minimum_overlap:
            failed.append(edge_index)
    return LocalWitnessCheck(
        passed=not failed,
        maximum_normal_residual=maximum_residual,
        minimum_realized_overlap=min(overlaps) if overlaps else None,
        failed_edges=tuple(failed),
    )


def _solve_one(
    canonical: CanonicalScaffold,
    *,
    minimum_overlap: float,
    tolerance: float,
    solve_index: int,
) -> LocalRealizationReceipt:
    scaffold = canonical.scaffold
    size = len(scaffold.vertex_colors)
    variable_count = 2 * size
    equalities: list[list[float]] = []
    equality_bounds: list[float] = []
    inequalities: list[list[float]] = []
    inequality_bounds: list[float] = []
    tangential_bound = 1 - minimum_overlap

    for edge in scaffold.edges:
        normal_offset = 0 if edge.normal == "u" else 1
        tangent_offset = 1 - normal_offset
        equality = [0.0] * variable_count
        equality[2 * edge.left + normal_offset] = -1
        equality[2 * edge.right + normal_offset] = 1
        equalities.append(equality)
        equality_bounds.append(float(edge.sign))

        forward = [0.0] * variable_count
        forward[2 * edge.left + tangent_offset] = -1
        forward[2 * edge.right + tangent_offset] = 1
        inequalities.append(forward)
        inequality_bounds.append(tangential_bound)
        inequalities.append([-value for value in forward])
        inequality_bounds.append(tangential_bound)

    result = linprog(
        np.zeros(variable_count),
        A_ub=np.asarray(inequalities) if inequalities else None,
        b_ub=np.asarray(inequality_bounds) if inequality_bounds else None,
        A_eq=np.asarray(equalities) if equalities else None,
        b_eq=np.asarray(equality_bounds) if equality_bounds else None,
        bounds=[(0.0, 0.0), (0.0, 0.0)] + [(None, None)] * (variable_count - 2),
        method="highs",
    )
    if result.success and result.x is not None:
        coordinates = tuple(
            (float(result.x[2 * index]), float(result.x[2 * index + 1]))
            for index in range(size)
        )
        witness_check = check_local_contact_witness(
            scaffold,
            coordinates,
            minimum_overlap=minimum_overlap,
            tolerance=tolerance,
        )
        outcome: LocalOutcome = (
            "locally-feasible" if witness_check.passed else "solver-indeterminate"
        )
        return LocalRealizationReceipt(
            canonical.canonical_label,
            outcome,
            int(result.status),
            solve_index,
            coordinates,
            witness_check,
        )
    outcome = "locally-infeasible" if result.status == 2 else "solver-indeterminate"
    return LocalRealizationReceipt(
        canonical.canonical_label,
        outcome,
        int(result.status),
        solve_index,
        None,
        None,
    )


def realize_local_contact_scaffolds(
    candidates: Iterable[ContactScaffold],
    *,
    minimum_overlap: float,
    maximum_lp_solves: int,
    tolerance: float = 1e-9,
) -> LocalRealizationBatch:
    """Canonicalize, deduplicate, and locally solve a bounded candidate stream."""
    _validate_parameters(minimum_overlap=minimum_overlap, tolerance=tolerance)
    if (
        isinstance(maximum_lp_solves, bool)
        or not isinstance(maximum_lp_solves, int)
        or maximum_lp_solves < 0
    ):
        raise LocalRealizationError(
            "malformed-cap", "maximum_lp_solves must be a nonnegative integer"
        )
    receipts: list[LocalRealizationReceipt] = []
    labels: set[str] = set()
    encountered = 0
    duplicates = 0
    for encountered, scaffold in enumerate(candidates, start=1):
        _validate_scaffold(scaffold)
        canonical = canonicalize_scaffold(scaffold)
        if canonical.status == "limit":
            raise RuntimeError("size-five scaffold exceeded the full 960-image orbit cap")
        if canonical.canonical_label in labels:
            duplicates += 1
            continue
        labels.add(canonical.canonical_label)
        if len(receipts) >= maximum_lp_solves:
            return LocalRealizationBatch(
                "limit",
                tuple(receipts),
                encountered,
                duplicates,
                len(receipts),
                "lp-solve-cap",
                maximum_lp_solves,
                canonical.canonical_label,
            )
        receipts.append(
            _solve_one(
                canonical,
                minimum_overlap=minimum_overlap,
                tolerance=tolerance,
                solve_index=len(receipts) + 1,
            )
        )
    return LocalRealizationBatch(
        "completed",
        tuple(receipts),
        encountered,
        duplicates,
        len(receipts),
        None,
        None,
        None,
    )
