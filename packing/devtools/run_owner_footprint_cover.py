#!/usr/bin/env python3
"""Matched exploratory covering LPs for one generic owner-footprint class.

The four arms share one available site set, singleton weight variables, and one
nine-orientation subset.  Owner footprints are always derived from the full 361
orientation manifest.  This is an exploratory finite-direction instrument: its float
objectives do not certify a packing bound, and no arm is silently promoted to an
all-direction result.
"""

from __future__ import annotations

import argparse
import json
import time
from dataclasses import asdict, dataclass, field
from fractions import Fraction
from math import lcm
from pathlib import Path

import numpy as np
from scipy.optimize import linprog
from strif import atomic_write_text

from devtools.owner_footprints import (
    CORE_SIDE,
    OUTER_SIDE,
    OwnerBranchManifest,
    OwnerClass,
    Point,
    Polygon,
    StrictResidualDomain,
    centre_in_strict_residual_domain,
    container_centre_polygon,
    full_owner_direction_manifest,
    owner_branch_manifest,
    owner_class_footprints,
    point_in_closed_convex_polygon,
    point_in_open_convex_polygon,
    polygon_area_twice,
    strict_residual_domain,
)
from devtools.run_residual_cover_pilot import (
    _dense_mass_grid,  # pyright: ignore[reportPrivateUsage]
    _exact_geometry_mass_grid,  # pyright: ignore[reportPrivateUsage]
    _exact_witness_for_cell,  # pyright: ignore[reportPrivateUsage]
    _float_pieces,  # pyright: ignore[reportPrivateUsage]
    _ranked_cells,  # pyright: ignore[reportPrivateUsage]
    _witness_for_cell,  # pyright: ignore[reportPrivateUsage]
    reachable_spans,
)
from sqpack.fractional.colgen import SiteSet, d4_orbit, rationalise_sites
from sqpack.fractional.generate import LP_FEASIBILITY, build_site_grid
from sqpack.fractional.model import Atom, Direction, require_nonnegative_atom_weights

DEFAULT_FOLDED_INDICES = (0, 45, 90, 135, 180)
ARM_ORDER = ("unrestricted", "point", "triangle", "endpoint")


@dataclass(frozen=True, slots=True)
class Arm:
    """One matched domain and its independent singleton support."""

    label: str
    footprint: Polygon | None
    sites: SiteSet
    removed_sites: tuple[Point, ...]
    pieces_by_direction: tuple[tuple[Polygon, ...], ...]
    domains_by_direction: tuple[StrictResidualDomain | None, ...]


@dataclass(frozen=True, slots=True)
class Complexity:
    """Dense-grid upper counts before zero-weight event coarsening."""

    per_direction: tuple[int, ...]

    @property
    def maximum(self) -> int:
        return max(self.per_direction, default=0)

    @property
    def total(self) -> int:
        return sum(self.per_direction)


@dataclass(frozen=True, slots=True)
class ExactMinimum:
    """An exact minimum over positive-area event cells in explicit pieces."""

    mass: Fraction
    reachable_cells: int


@dataclass(slots=True)
class RoundRecord:
    index: int
    rows_held: int
    rows_added: int
    violated: int
    objective: float | None
    least_covered: float
    dense_cells: int
    seconds: float


@dataclass(slots=True)
class ProgramSolution:
    weights: np.ndarray
    stopped: str
    objective: float | None = None
    least_covered: float | None = None
    rows: int = 0
    rounds: list[RoundRecord] = field(default_factory=list)
    seconds: float = 0.0

    @property
    def converged(self) -> bool:
        return self.stopped.startswith("converged")


def singleton_site_set(
    outer_side: Fraction = OUTER_SIDE,
    *,
    grid_count: int = 19,
    inset: Fraction = Fraction(1, 2),
    mark: Point | None = None,
) -> SiteSet:
    """Build the common grid-plus-full-mark-orbit support with independent weights."""

    if grid_count < 2:
        raise ValueError("grid_count must be at least two")
    selected_mark = mark or owner_branch_manifest().classes[0].mark
    points = set(build_site_grid(outer_side, grid_count, inset).positions())
    points.update(d4_orbit(selected_mark[0], selected_mark[1], outer_side))
    return SiteSet(outer_side, tuple((point,) for point in sorted(points)))


def selected_reflected_directions(
    manifest: OwnerBranchManifest,
    folded_indices: tuple[int, ...] = DEFAULT_FOLDED_INDICES,
) -> tuple[Direction, ...]:
    """Select canonical orientations with a declared base or reflected source index."""

    selected = set(folded_indices)
    if not selected or min(selected) < 0 or max(selected) >= manifest.directions.folded_count:
        raise ValueError("folded direction indices lie outside the source net")
    return tuple(
        entry.direction
        for entry in manifest.directions.orientations
        if any(source.folded_index in selected for source in entry.sources)
    )


def _singleton_subset(
    sites: SiteSet, footprint: Polygon | None
) -> tuple[SiteSet, tuple[Point, ...]]:
    if any(len(orbit) != 1 for orbit in sites.orbits):
        raise ValueError("owner-footprint arms require independent singleton variables")
    if footprint is None:
        return sites, ()
    removed = tuple(
        orbit[0]
        for orbit in sites.orbits
        if point_in_closed_convex_polygon(orbit[0], footprint)
    )
    removed_set = set(removed)
    retained = tuple(orbit for orbit in sites.orbits if orbit[0] not in removed_set)
    if not retained:
        raise ValueError("footprint removes the entire candidate support")
    return SiteSet(sites.outer_side, retained), removed


def build_arms(
    owner_class: OwnerClass,
    sites: SiteSet,
    directions: tuple[Direction, ...],
    *,
    square_side: Fraction = CORE_SIDE,
    direction_manifest: OwnerBranchManifest | None = None,
) -> tuple[Arm, ...]:
    """Build the four domains while deriving footprints from the full owner net."""

    manifest = direction_manifest or owner_branch_manifest()
    footprints = owner_class_footprints(owner_class, manifest.directions.directions)
    arm_footprints: dict[str, Polygon | None] = {
        "unrestricted": None,
        "point": footprints["point"],
        "triangle": footprints["triangle"],
        "endpoint": footprints["endpoint"],
    }
    arms: list[Arm] = []
    for label in ARM_ORDER:
        footprint = arm_footprints[label]
        arm_sites, removed = _singleton_subset(sites, footprint)
        pieces: list[tuple[Polygon, ...]] = []
        domains: list[StrictResidualDomain | None] = []
        for direction in directions:
            if footprint is None:
                direction_pieces = (
                    container_centre_polygon(sites.outer_side, square_side, direction),
                )
                domain = None
            else:
                domain = strict_residual_domain(
                    sites.outer_side, square_side, direction, footprint
                )
                direction_pieces = domain.components
            if not direction_pieces:
                raise ValueError(f"{label} has an empty residual domain at {direction.label}")
            pieces.append(direction_pieces)
            domains.append(domain)
        arms.append(Arm(label, footprint, arm_sites, removed, tuple(pieces), tuple(domains)))
    return tuple(arms)


def estimate_complexity(
    arm: Arm, square_side: Fraction, directions: tuple[Direction, ...]
) -> Complexity:
    """Count each arm's dense event rectangle without allocating it."""

    half = square_side / 2
    estimates: list[int] = []
    for direction, pieces in zip(directions, arm.pieces_by_direction, strict=True):
        projected = tuple(
            (
                direction.ux * x + direction.uy * y,
                direction.vx * x + direction.vy * y,
            )
            for x, y in arm.sites.positions()
        )
        u_events = {
            coordinate + offset for coordinate, _ in projected for offset in (-half, half)
        } | {u for polygon in pieces for u, _ in polygon}
        v_events = {
            coordinate + offset for _, coordinate in projected for offset in (-half, half)
        } | {v for polygon in pieces for _, v in polygon}
        estimates.append((len(u_events) - 1) * (len(v_events) - 1))
    return Complexity(tuple(estimates))


def _placement_cells(
    arm: Arm,
    direction: Direction,
    direction_index: int,
    site_weights: np.ndarray,
    square_side: Fraction,
    *,
    keep: int,
    max_event_cells: int,
) -> tuple[list[tuple[float, float, float, np.ndarray]], int]:
    pieces = arm.pieces_by_direction[direction_index]
    points = arm.sites.points()
    float_pieces = _float_pieces(pieces)
    u, v, u_events, v_events, mass = _dense_mass_grid(
        points, site_weights, direction, float(square_side), float_pieces
    )
    dense_cells = int(mass.size)
    if dense_cells > max_event_cells:
        raise ValueError(
            f"direction {direction.label} needs {dense_cells:,} dense cells, "
            f"above guard {max_event_cells:,}"
        )
    spans = reachable_spans(tuple(u_events), tuple(v_events), float_pieces)
    if not spans:
        return _placement_cells_exact_geometry(
            arm,
            direction,
            direction_index,
            site_weights,
            square_side,
            keep=keep,
            max_event_cells=max_event_cells,
        )
    ranked, survey = _ranked_cells(mass, spans, keep)
    half = float(square_side) / 2
    found: list[tuple[float, float, float, np.ndarray]] = []
    for event_mass, i, j in ranked[: max(survey, keep)]:
        try:
            cu, cv = _witness_for_cell(
                float_pieces,
                float(u_events[i]),
                float(u_events[i + 1]),
                float(v_events[j]),
                float(v_events[j + 1]),
            )
        except ValueError:
            return _placement_cells_exact_geometry(
                arm,
                direction,
                direction_index,
                site_weights,
                square_side,
                keep=keep,
                max_event_cells=max_event_cells,
            )
        if not _exact_witness_is_admissible(
            arm, direction, direction_index, (Fraction(cu), Fraction(cv)), square_side
        ):
            return _placement_cells_exact_geometry(
                arm,
                direction,
                direction_index,
                site_weights,
                square_side,
                keep=keep,
                max_event_cells=max_event_cells,
            )
        covers = (np.abs(u - cu) <= half) & (np.abs(v - cv) <= half)
        direct_mass = float(site_weights[covers].sum())
        if abs(direct_mass - event_mass) > 1e-8:
            return _placement_cells_exact_geometry(
                arm,
                direction,
                direction_index,
                site_weights,
                square_side,
                keep=keep,
                max_event_cells=max_event_cells,
            )
        found.append((direct_mass, cu, cv, covers))
        if len(found) >= keep:
            break
    if not found:
        raise ValueError("no interior witness was found for the least event cells")
    return found, dense_cells


def _exact_witness_is_admissible(
    arm: Arm,
    direction: Direction,
    direction_index: int,
    centre: Point,
    square_side: Fraction,
) -> bool:
    domain = arm.domains_by_direction[direction_index]
    if domain is not None:
        return centre_in_strict_residual_domain(centre, domain)
    container = container_centre_polygon(arm.sites.outer_side, square_side, direction)
    return point_in_open_convex_polygon(centre, container)


def _placement_cells_exact_geometry(
    arm: Arm,
    direction: Direction,
    direction_index: int,
    site_weights: np.ndarray,
    square_side: Fraction,
    *,
    keep: int,
    max_event_cells: int,
) -> tuple[list[tuple[float, float, float, np.ndarray]], int]:
    """Reconstruct ambiguous cells from rational sites and generic domain pieces."""

    pieces = arm.pieces_by_direction[direction_index]
    points = arm.sites.positions()
    projected, u_events, v_events, mass = _exact_geometry_mass_grid(
        points, site_weights, direction, square_side, pieces
    )
    dense_cells = int(mass.size)
    if dense_cells > max_event_cells:
        raise ValueError(
            f"exact fallback for direction {direction.label} needs {dense_cells:,} dense "
            f"cells, above guard {max_event_cells:,}"
        )
    spans = reachable_spans(u_events, v_events, pieces)
    if not spans:
        raise ValueError("exact domain reaches no positive-area event cell")
    ranked, survey = _ranked_cells(mass, spans, keep)
    half = square_side / 2
    found: list[tuple[float, float, float, np.ndarray]] = []
    for event_mass, i, j in ranked[: max(survey, keep)]:
        centre = _exact_witness_for_cell(
            pieces, u_events[i], u_events[i + 1], v_events[j], v_events[j + 1]
        )
        if not _exact_witness_is_admissible(
            arm, direction, direction_index, centre, square_side
        ):
            raise ValueError("exact-event witness failed generic domain admissibility")
        cu, cv = centre
        covers = np.array(
            [abs(u - cu) <= half and abs(v - cv) <= half for u, v in projected],
            dtype=bool,
        )
        direct_mass = float(site_weights[covers].sum())
        if abs(direct_mass - event_mass) > 1e-8:
            raise ValueError("exact-event mass disagrees with its rational-cell witness")
        found.append((direct_mass, float(cu), float(cv), covers))
        if len(found) >= keep:
            break
    if not found:
        raise ValueError("exact event fallback found no least-cell witness")
    return found, dense_cells


def solve_program(  # noqa: PLR0911 -- each stop preserves a distinct partial receipt
    arm: Arm,
    square_side: Fraction,
    directions: tuple[Direction, ...],
    *,
    max_rounds: int,
    rows_per_direction: int,
    deadline_seconds: float,
    max_event_cells: int,
) -> ProgramSolution:
    """Run float row generation on one explicit generic residual domain."""

    started = time.perf_counter()
    deadline = started + deadline_seconds
    weights = np.zeros(len(arm.sites.orbits))
    rows: list[np.ndarray] = []
    held: set[bytes] = set()
    objective: float | None = None
    least_covered: float | None = None
    round_records: list[RoundRecord] = []

    def stopped(reason: str) -> ProgramSolution:
        return ProgramSolution(
            weights,
            reason,
            objective,
            least_covered,
            len(rows),
            round_records,
            time.perf_counter() - started,
        )

    for round_index in range(max_rounds):
        if time.perf_counter() >= deadline:
            return stopped(f"deadline {deadline_seconds:g}s reached before round {round_index}")
        round_started = time.perf_counter()
        violated = added = dense_cells = 0
        least = float("inf")
        for direction_index, direction in enumerate(directions):
            if time.perf_counter() >= deadline:
                return stopped(f"deadline {deadline_seconds:g}s reached during separation")
            try:
                placements, cells = _placement_cells(
                    arm,
                    direction,
                    direction_index,
                    weights,
                    square_side,
                    keep=rows_per_direction,
                    max_event_cells=max_event_cells,
                )
            except (MemoryError, ValueError) as error:
                return stopped(f"separation unresolved: {type(error).__name__}: {error}")
            dense_cells += cells
            least = min(least, placements[0][0])
            for mass, _, _, covers in placements:
                if mass >= 1 - 1e-9:
                    break
                row = covers.astype(float)
                if not row.any():
                    return stopped("a placement covers no candidate site")
                violated += 1
                key = row.tobytes()
                if key not in held:
                    held.add(key)
                    rows.append(row)
                    added += 1
        least_covered = least
        if violated == 0 or (added == 0 and 1 - least <= LP_FEASIBILITY):
            objective = float(weights.sum())
            round_records.append(
                RoundRecord(
                    round_index,
                    len(rows),
                    added,
                    violated,
                    objective,
                    least,
                    dense_cells,
                    time.perf_counter() - round_started,
                )
            )
            return stopped("converged: every surveyed placement covers mass 1")
        if added == 0:
            return stopped(f"a held row is violated by {1 - least:.3e}")
        remaining = deadline - time.perf_counter()
        if remaining <= 0:
            return stopped(f"deadline {deadline_seconds:g}s reached before LP solve")
        result = linprog(
            c=np.ones(len(arm.sites.orbits)),
            A_ub=-np.vstack(rows),
            b_ub=-np.ones(len(rows)),
            bounds=[(0.0, None)] * len(arm.sites.orbits),
            method="highs",
            options={"time_limit": remaining},
        )
        if not result.success:
            if result.status == 1 or time.perf_counter() >= deadline:
                return stopped(f"deadline {deadline_seconds:g}s reached during LP solve")
            return stopped(f"linear program refused: {result.message}")
        weights = np.asarray(result.x, dtype=float)
        objective = float(result.fun)
        round_records.append(
            RoundRecord(
                round_index,
                len(rows),
                added,
                violated,
                objective,
                least,
                dense_cells,
                time.perf_counter() - round_started,
            )
        )
    return stopped(f"round limit {max_rounds} reached")


def exact_minimum_covered_mass_on_pieces(
    atoms: tuple[Atom, ...],
    direction: Direction,
    square_side: Fraction,
    pieces: tuple[Polygon, ...],
) -> ExactMinimum:
    """Replay one direction exactly over separate positive-area component closures."""

    require_nonnegative_atom_weights(atoms)
    if not atoms:
        raise ValueError("exact replay needs at least one weighted atom")
    active_pieces = tuple(
        polygon for polygon in pieces if len(polygon) >= 3 and polygon_area_twice(polygon) != 0
    )
    if not active_pieces:
        raise ValueError("exact replay needs at least one positive-area component")
    half = square_side / 2
    projected = tuple(
        (
            direction.ux * atom.x + direction.uy * atom.y,
            direction.vx * atom.x + direction.vy * atom.y,
            atom.weight,
        )
        for atom in atoms
    )
    u_events = tuple(
        sorted(
            {u + offset for u, _, _ in projected for offset in (-half, half)}
            | {u for polygon in active_pieces for u, _ in polygon}
        )
    )
    v_events = tuple(
        sorted(
            {v + offset for _, v, _ in projected for offset in (-half, half)}
            | {v for polygon in active_pieces for _, v in polygon}
        )
    )
    scale = lcm(*(atom.weight.denominator for atom in atoms))
    scaled = tuple(int(atom.weight * scale) for atom in atoms)
    if sum(scaled) >= 2**60:
        raise ValueError("scaled total mass exceeds the exact grid limit")
    grid = np.zeros((len(u_events), len(v_events)), dtype=np.int64)
    u_index = {value: index for index, value in enumerate(u_events)}
    v_index = {value: index for index, value in enumerate(v_events)}
    for (u, v, _), weight in zip(projected, scaled, strict=True):
        left, right = u_index[u - half], u_index[u + half]
        bottom, top = v_index[v - half], v_index[v + half]
        grid[left, bottom] += weight
        grid[right, bottom] -= weight
        grid[left, top] -= weight
        grid[right, top] += weight
    np.cumsum(grid, axis=1, out=grid)
    np.cumsum(grid, axis=0, out=grid)
    spans = reachable_spans(u_events, v_events, active_pieces)
    if not spans:
        raise ValueError("exact residual domain reaches no positive-area event cell")
    best: int | None = None
    count = 0
    for i, j0, j1 in spans:
        score = int(grid[i, j0 : j1 + 1].min())
        best = score if best is None else min(best, score)
        count += j1 - j0 + 1
    if best is None:
        raise ValueError("exact replay found no reachable score")
    return ExactMinimum(Fraction(best, scale), count)


def _fraction_polygon(polygon: Polygon | None) -> list[list[str]] | None:
    if polygon is None:
        return None
    return [[str(x), str(y)] for x, y in polygon]


def _arm_record(arm: Arm, complexity: Complexity) -> dict[str, object]:
    return {
        "footprint": _fraction_polygon(arm.footprint),
        "available_sites": arm.sites.size + len(arm.removed_sites),
        "retained_singleton_variables": arm.sites.size,
        "removed_inside_closed_footprint": [[str(x), str(y)] for x, y in arm.removed_sites],
        "component_counts": [len(pieces) for pieces in arm.pieces_by_direction],
        "complexity": {
            "per_direction": list(complexity.per_direction),
            "maximum": complexity.maximum,
            "total_one_round": complexity.total,
        },
        "proposal": None,
    }


def build_receipt(
    *,
    class_id: str = "bottom-left:m1:j0",
    grid_count: int = 19,
    inset: Fraction = Fraction(1, 2),
    folded_indices: tuple[int, ...] = DEFAULT_FOLDED_INDICES,
) -> tuple[dict[str, object], tuple[Arm, ...], tuple[Direction, ...]]:
    """Build the frozen settings and complexity receipt without solving any arm."""

    manifest = owner_branch_manifest(full_owner_direction_manifest())
    by_id = {entry.class_id: entry for entry in manifest.classes}
    if class_id not in by_id:
        raise ValueError(f"unknown owner class {class_id!r}")
    owner_class = by_id[class_id]
    directions = selected_reflected_directions(manifest, folded_indices)
    sites = singleton_site_set(
        OUTER_SIDE,
        grid_count=grid_count,
        inset=inset,
        mark=owner_class.mark,
    )
    arms = build_arms(
        owner_class,
        sites,
        directions,
        direction_manifest=manifest,
    )
    complexities = {arm.label: estimate_complexity(arm, CORE_SIDE, directions) for arm in arms}
    receipt: dict[str, object] = {
        "schema": "owner-footprint-cover/v1",
        "status": "estimated",
        "evidence_tier": "finite-direction exploratory matched covering LP",
        "scientific_target_run": False,
        "claim_limit": (
            "No packing bound: float proposals require exact replay and nine directions "
            "do not cover the full 361-orientation owner or residual families."
        ),
        "class": {
            "id": owner_class.class_id,
            "mark_id": owner_class.mark_id,
            "mark": [str(value) for value in owner_class.mark],
            "sector": owner_class.sector,
            "reflected_class_id": owner_class.reflected_class_id,
        },
        "settings": {
            "outer_side": str(OUTER_SIDE),
            "square_side": str(CORE_SIDE),
            "grid_count": grid_count,
            "inset": str(inset),
            "variable_grouping": "independent singleton site weights",
            "folded_source_indices": list(folded_indices),
            "selected_canonical_directions": len(directions),
            "full_owner_orientation_count": manifest.directions.full_count,
            "owner_footprints_derived_from_full_manifest": True,
        },
        "direction_provenance": [
            {
                "label": entry.direction.label,
                "ux": str(entry.direction.ux),
                "uy": str(entry.direction.uy),
                "sources": [
                    {"folded_index": source.folded_index, "reflected": source.reflected}
                    for source in entry.sources
                    if source.folded_index in set(folded_indices)
                ],
            }
            for entry in manifest.directions.orientations
            if entry.direction in directions
        ],
        "available_support": {
            "sites": sites.size,
            "all_singletons": all(len(orbit) == 1 for orbit in sites.orbits),
            "coordinates": [[str(x), str(y)] for x, y in sites.positions()],
        },
        "arms": {arm.label: _arm_record(arm, complexities[arm.label]) for arm in arms},
        "comparison": None,
    }
    return receipt, arms, directions


def run_arms(
    receipt: dict[str, object],
    arms: tuple[Arm, ...],
    directions: tuple[Direction, ...],
    *,
    max_rounds: int,
    rows_per_direction: int,
    deadline_seconds: float,
    max_event_cells: int,
    max_round_cells: int,
    scale: int,
    checkpoint: Path | None = None,
) -> dict[str, object]:
    """Run each frozen arm once, refusing complexity over the declared guards."""

    arm_records = receipt["arms"]
    if not isinstance(arm_records, dict):
        raise TypeError("receipt arm map is malformed")
    objectives: dict[str, float] = {}
    receipt["scientific_target_run"] = True
    receipt["status"] = "running"
    settings = receipt["settings"]
    if not isinstance(settings, dict):
        raise TypeError("receipt settings map is malformed")
    settings["execution"] = {
        "max_rounds_per_arm": max_rounds,
        "rows_per_direction": rows_per_direction,
        "deadline_seconds_per_arm": deadline_seconds,
        "max_dense_event_cells_per_direction": max_event_cells,
        "max_dense_event_cells_per_round": max_round_cells,
        "rationalisation_scale": scale,
    }
    if checkpoint is not None:
        atomic_write_text(checkpoint, _json(receipt), make_parents=True)
    for arm in arms:
        complexity = estimate_complexity(arm, CORE_SIDE, directions)
        if complexity.maximum > max_event_cells or complexity.total > max_round_cells:
            raise ValueError(f"{arm.label} complexity exceeds the declared guard")
        solution = solve_program(
            arm,
            CORE_SIDE,
            directions,
            max_rounds=max_rounds,
            rows_per_direction=rows_per_direction,
            deadline_seconds=deadline_seconds,
            max_event_cells=max_event_cells,
        )
        atoms = rationalise_sites(arm.sites, solution.weights, scale=scale)
        record = arm_records[arm.label]
        if not isinstance(record, dict):
            raise TypeError("receipt arm entry is malformed")
        record["proposal"] = {
            "search_arithmetic": "floating point; exploratory",
            "stopped": solution.stopped,
            "converged": solution.converged,
            "seconds": solution.seconds,
            "rows": solution.rows,
            "objective": solution.objective,
            "least_covered": solution.least_covered,
            "rationalisation_scale": scale,
            "rationalised_total_mass": str(
                sum((atom.weight for atom in atoms), start=Fraction(0))
            ),
            "rationalised_atoms": [
                [str(atom.x), str(atom.y), str(atom.weight)] for atom in atoms
            ],
            "exact_validation": None,
            "rounds": [asdict(round_record) for round_record in solution.rounds],
        }
        if checkpoint is not None:
            atomic_write_text(checkpoint, _json(receipt), make_parents=True)
        if not solution.converged or solution.objective is None:
            receipt["status"] = "partial"
            if checkpoint is not None:
                atomic_write_text(checkpoint, _json(receipt), make_parents=True)
            return receipt
        objectives[arm.label] = solution.objective
    receipt["comparison"] = {
        "arithmetic": "floating point; exploratory",
        "M0": objectives["unrestricted"],
        "Mm": objectives["point"],
        "MT": objectives["triangle"],
        "MP": objectives["endpoint"],
        "Mm_minus_MT": objectives["point"] - objectives["triangle"],
        "MT_minus_MP": objectives["triangle"] - objectives["endpoint"],
        "nested_monotonicity_observed": (
            objectives["endpoint"] <= objectives["triangle"] + 1e-7
            and objectives["triangle"] <= objectives["point"] + 1e-7
            and objectives["point"] <= objectives["unrestricted"] + 1e-7
        ),
    }
    receipt["status"] = "complete"
    if checkpoint is not None:
        atomic_write_text(checkpoint, _json(receipt), make_parents=True)
    return receipt


def _parse_indices(value: str) -> tuple[int, ...]:
    try:
        indices = tuple(sorted({int(item) for item in value.split(",")}))
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            "folded indices must be comma-separated integers"
        ) from error
    if not indices:
        raise argparse.ArgumentTypeError("at least one folded index is required")
    return indices


def _json(record: dict[str, object]) -> str:
    return json.dumps(record, indent=1, allow_nan=False) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--class-id", default="bottom-left:m1:j0")
    parser.add_argument("--grid-count", type=int, default=19)
    parser.add_argument("--inset", type=Fraction, default=Fraction(1, 2))
    parser.add_argument("--folded-indices", type=_parse_indices, default=DEFAULT_FOLDED_INDICES)
    parser.add_argument("--rows-per-direction", type=int, default=3)
    parser.add_argument("--max-rounds", type=int, default=60)
    parser.add_argument("--deadline-seconds-per-arm", type=float, default=120)
    parser.add_argument("--max-event-cells", type=int, default=5_000_000)
    parser.add_argument("--max-round-cells", type=int, default=30_000_000)
    parser.add_argument("--scale", type=int, default=4_000_000)
    parser.add_argument("--estimate-only", action="store_true")
    args = parser.parse_args(argv)
    if (
        min(
            args.rows_per_direction,
            args.max_rounds,
            args.max_event_cells,
            args.max_round_cells,
            args.scale,
        )
        < 1
    ):
        parser.error("row, round, cell, and scale guards must be positive")
    if args.deadline_seconds_per_arm <= 0:
        parser.error("deadline-seconds-per-arm must be positive")
    if not args.estimate_only and args.output is None:
        parser.error("a non-estimate run requires --output for incremental receipts")

    receipt, arms, directions = build_receipt(
        class_id=args.class_id,
        grid_count=args.grid_count,
        inset=args.inset,
        folded_indices=args.folded_indices,
    )
    if not args.estimate_only:
        receipt = run_arms(
            receipt,
            arms,
            directions,
            max_rounds=args.max_rounds,
            rows_per_direction=args.rows_per_direction,
            deadline_seconds=args.deadline_seconds_per_arm,
            max_event_cells=args.max_event_cells,
            max_round_cells=args.max_round_cells,
            scale=args.scale,
            checkpoint=args.output,
        )
    rendered = _json(receipt)
    if args.output is not None:
        atomic_write_text(args.output, rendered, make_parents=True)
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
