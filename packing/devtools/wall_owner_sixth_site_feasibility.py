#!/usr/bin/env python3
"""Solve the fixed-D sixth-site region by exact complete-domain supports."""

from __future__ import annotations

import argparse
import json
import math
import time
from collections.abc import Callable
from dataclasses import dataclass, replace
from fractions import Fraction
from pathlib import Path
from typing import Literal

from cases.n11_five_dot_cover.independent_union import (
    AuditError,
    DeadlineError,
    Direction,
    FrozenInput,
    UnionMeasure,
    collision_polygon,
    container_rectangle,
    core_offsets,
    load_frozen_input,
    measure_direction,
)
from devtools.multi_owner_domains import vertical_decompose
from devtools.owner_footprints import (
    CORE_SIDE,
    OUTER_SIDE,
    Point,
    Polygon,
    convex_hull,
    convex_polygon_intersection,
    point_in_closed_convex_polygon,
)
from devtools.wall_owner_containment import (
    EXPECTED_ORIENTATIONS,
    ContainmentError,
    WallInput,
    atomic_write_json,
    load_wall_input,
    validate_output_path,
    validate_own_revision,
)
from devtools.wall_owner_fixed_pattern import RETAINED_ENDPOINT_BLOB, FixedPatternError
from devtools.wall_owner_selected_cover import (
    SELECTED_TUPLE,
    DirectionResult,
    SelectedCoverError,
    SelectedCoverEvidence,
    SelectedEscape,
    load_selected_cover_evidence,
    replay_selected_cover_evidence,
)
from devtools.wall_owner_six_dot_cover import (
    MAX_SUBSETS,
    SixDotCoverError,
    augment_with_selected_escape,
    extract_six_dot_escape,
    replay_six_dot_escape,
)
from devtools.wall_owner_sixth_site_screen import (
    SixDotEscapeEvidence,
    SixthSiteScreenError,
    escape_core,
    load_six_dot_escape_evidence,
)


class SixthSiteFeasibilityError(ValueError):
    """A source, exact-geometry, or decision guard failed."""


@dataclass(frozen=True, slots=True)
class HalfPlane:
    """One exact closed inequality ``a*x + b*y <= bound``."""

    name: Literal["u-lower", "u-upper", "v-lower", "v-upper"]
    a: Fraction
    b: Fraction
    bound: Fraction

    def value(self, point: Point) -> Fraction:
        return self.a * point[0] + self.b * point[1]


@dataclass(frozen=True, slots=True)
class SupportAttainer:
    """A closure vertex attaining one exact centre projection."""

    component_index: int
    vertex_index: int
    vertex: Point
    value: Fraction


@dataclass(frozen=True, slots=True)
class DirectionSupport:
    """The complete-domain supports and resulting feasible-site prefix."""

    index: int
    label: str
    u: Point
    v: Point
    component_count: int
    u_min: SupportAttainer | None
    u_max: SupportAttainer | None
    v_min: SupportAttainer | None
    v_max: SupportAttainer | None
    constraints: tuple[HalfPlane, ...]
    region: Polygon


@dataclass(frozen=True, slots=True)
class SixthSiteFeasibilityResult:
    """One bounded exact support pass and optional independent confirmation."""

    status: Literal["complete", "partial", "invalid"]
    outcome: Literal["covered", "empty", "incomplete", "inconsistent"]
    initial_region: Polygon | None
    supports: tuple[DirectionSupport, ...]
    final_region: Polygon | None
    candidate: Point | None
    confirmation: tuple[DirectionResult, ...]
    conflicting_escape: SelectedEscape | None
    decomposition_seconds: float
    projection_seconds: float
    confirmation_seconds: float
    wall_seconds: float
    error: str | None = None


Checkpoint = Callable[[SixthSiteFeasibilityResult], None]


def _elapsed(started: float) -> float:
    return max(0.0, time.perf_counter() - started)


def _clip_closed_half_plane(region: Polygon, constraint: HalfPlane) -> Polygon:
    """Clip an exact convex region while preserving points and segments."""

    if not region:
        return ()

    def signed(point: Point) -> Fraction:
        return constraint.value(point) - constraint.bound

    if len(region) == 1:
        return region if signed(region[0]) <= 0 else ()
    if len(region) == 2:
        first, second = region
        first_value, second_value = signed(first), signed(second)
        first_inside, second_inside = first_value <= 0, second_value <= 0
        if first_inside and second_inside:
            return region
        if not first_inside and not second_inside:
            return ()
        factor = first_value / (first_value - second_value)
        crossing = (
            first[0] + factor * (second[0] - first[0]),
            first[1] + factor * (second[1] - first[1]),
        )
        return convex_hull((first, crossing) if first_inside else (crossing, second))

    output: list[Point] = []
    previous = region[-1]
    previous_value = signed(previous)
    previous_inside = previous_value <= 0
    for current in region:
        current_value = signed(current)
        current_inside = current_value <= 0
        if current_inside != previous_inside:
            factor = previous_value / (previous_value - current_value)
            output.append(
                (
                    previous[0] + factor * (current[0] - previous[0]),
                    previous[1] + factor * (current[1] - previous[1]),
                )
            )
        if current_inside:
            output.append(current)
        previous, previous_value, previous_inside = current, current_value, current_inside
    return convex_hull(tuple(output))


def _projection_attainers(
    components: tuple[Polygon, ...], axis: Point
) -> tuple[SupportAttainer, SupportAttainer]:
    samples = tuple(
        SupportAttainer(
            component_index,
            vertex_index,
            vertex,
            axis[0] * vertex[0] + axis[1] * vertex[1],
        )
        for component_index, component in enumerate(components)
        for vertex_index, vertex in enumerate(component)
    )
    if not samples:
        raise SixthSiteFeasibilityError("a nonempty domain has no closure vertices")
    minimum = min(
        samples,
        key=lambda item: (item.value, item.component_index, item.vertex_index),
    )
    maximum_value = max(item.value for item in samples)
    maximum = min(
        (item for item in samples if item.value == maximum_value),
        key=lambda item: (item.component_index, item.vertex_index),
    )
    return minimum, maximum


def support_constraints(
    components: tuple[Polygon, ...], direction: Direction, half: Fraction
) -> tuple[
    tuple[HalfPlane, ...],
    SupportAttainer | None,
    SupportAttainer | None,
    SupportAttainer | None,
    SupportAttainer | None,
]:
    """Return the four exact common-core constraints for one closure cover."""

    if half <= 0:
        raise SixthSiteFeasibilityError("core half-side must be positive")
    if not components:
        return (), None, None, None, None
    u = (direction.cosine, direction.sine)
    v = (-direction.sine, direction.cosine)
    u_min, u_max = _projection_attainers(components, u)
    v_min, v_max = _projection_attainers(components, v)
    constraints = (
        HalfPlane("u-lower", -u[0], -u[1], half - u_max.value),
        HalfPlane("u-upper", u[0], u[1], u_min.value + half),
        HalfPlane("v-lower", -v[0], -v[1], half - v_max.value),
        HalfPlane("v-upper", v[0], v[1], v_min.value + half),
    )
    return constraints, u_min, u_max, v_min, v_max


def clip_constraints(region: Polygon, constraints: tuple[HalfPlane, ...]) -> Polygon:
    """Apply exact closed half-planes to an area, segment, or point."""

    result = region
    for constraint in constraints:
        result = _clip_closed_half_plane(result, constraint)
        if not result:
            break
    return result


def _direction_result(index: int, label: str, measure: UnionMeasure) -> DirectionResult:
    return DirectionResult(
        index,
        label,
        measure.container_area,
        measure.covered_area,
        measure.uncovered_area,
        measure.nonempty_subsets,
    )


def _partial(
    *,
    initial_region: Polygon | None,
    supports: list[DirectionSupport],
    region: Polygon | None,
    candidate: Point | None,
    confirmation: list[DirectionResult],
    conflicting_escape: SelectedEscape | None,
    decomposition_seconds: float,
    projection_seconds: float,
    confirmation_seconds: float,
    started: float,
    error: str,
) -> SixthSiteFeasibilityResult:
    return SixthSiteFeasibilityResult(
        "partial",
        "incomplete",
        initial_region,
        tuple(supports),
        region,
        candidate,
        tuple(confirmation),
        conflicting_escape,
        decomposition_seconds,
        projection_seconds,
        confirmation_seconds,
        _elapsed(started),
        error,
    )


def _progress_result(
    *,
    initial_region: Polygon,
    supports: list[DirectionSupport],
    region: Polygon,
    decomposition_seconds: float,
    projection_seconds: float,
    started: float,
) -> SixthSiteFeasibilityResult:
    return _partial(
        initial_region=initial_region,
        supports=supports,
        region=region,
        candidate=None,
        confirmation=[],
        conflicting_escape=None,
        decomposition_seconds=decomposition_seconds,
        projection_seconds=projection_seconds,
        confirmation_seconds=0.0,
        started=started,
        error="support pass in progress",
    )


def run_sixth_site_feasibility(  # noqa: PLR0911
    source: FrozenInput,
    wall: WallInput,
    selected: SelectedCoverEvidence,
    six_dot: SixDotEscapeEvidence,
    *,
    deadline_seconds: float = 240,
    checkpoint: Checkpoint | None = None,
) -> SixthSiteFeasibilityResult:
    """Compute the exact feasible site set and independently confirm one candidate."""

    if not math.isfinite(deadline_seconds) or deadline_seconds <= 0:
        raise SixthSiteFeasibilityError("internal deadline must be finite and positive")
    if (source.outer_side, source.core_side) != (OUTER_SIDE, CORE_SIDE):
        raise SixthSiteFeasibilityError("source changes the frozen outer or core side")
    if len(source.directions) != EXPECTED_ORIENTATIONS:
        raise SixthSiteFeasibilityError("source lacks the complete 361-direction manifest")

    started = time.perf_counter()
    deadline = started + deadline_seconds
    augmented = augment_with_selected_escape(source, wall, selected)
    original = replace(augmented, dots=source.dots)
    supports: list[DirectionSupport] = []
    confirmation: list[DirectionResult] = []
    decomposition_seconds = 0.0
    projection_seconds = 0.0
    confirmation_seconds = 0.0
    initial_region: Polygon | None = None
    region: Polygon | None = None
    candidate: Point | None = None

    try:
        replay_selected_cover_evidence(selected, source=source, deadline=deadline)
        replay_six_dot_escape(six_dot.escape, augmented, deadline=deadline)
    except DeadlineError as error:
        return _partial(
            initial_region=None,
            supports=supports,
            region=None,
            candidate=None,
            confirmation=confirmation,
            conflicting_escape=None,
            decomposition_seconds=0.0,
            projection_seconds=0.0,
            confirmation_seconds=0.0,
            started=started,
            error=str(error),
        )

    first_core = escape_core(source, selected.escape)
    second_core = escape_core(source, six_dot.escape)
    initial_region = convex_hull(convex_polygon_intersection(first_core, second_core))
    if not initial_region:
        raise SixthSiteFeasibilityError("the admitted two-core intersection is empty")
    region = initial_region

    for index, direction in enumerate(original.directions):
        if time.perf_counter() >= deadline:
            return _partial(
                initial_region=initial_region,
                supports=supports,
                region=region,
                candidate=None,
                confirmation=confirmation,
                conflicting_escape=None,
                decomposition_seconds=decomposition_seconds,
                projection_seconds=projection_seconds,
                confirmation_seconds=confirmation_seconds,
                started=started,
                error="sixth-site feasibility deadline reached before decomposition",
            )
        offsets = core_offsets(original.core_side, direction)
        obstacles = tuple(
            collision_polygon(footprint, offsets) for footprint in original.footprints
        ) + tuple(collision_polygon((dot,), offsets) for dot in original.dots)
        stage_started = time.perf_counter()
        decomposition = vertical_decompose(
            container_rectangle(original.outer_side, original.core_side, direction), obstacles
        )
        decomposition_seconds += _elapsed(stage_started)
        if time.perf_counter() >= deadline:
            return _partial(
                initial_region=initial_region,
                supports=supports,
                region=region,
                candidate=None,
                confirmation=confirmation,
                conflicting_escape=None,
                decomposition_seconds=decomposition_seconds,
                projection_seconds=projection_seconds,
                confirmation_seconds=confirmation_seconds,
                started=started,
                error="sixth-site feasibility deadline reached after decomposition",
            )
        stage_started = time.perf_counter()
        constraints, u_min, u_max, v_min, v_max = support_constraints(
            decomposition.components, direction, original.core_side / 2
        )
        region = clip_constraints(region, constraints)
        projection_seconds += _elapsed(stage_started)
        row = DirectionSupport(
            index,
            direction.label,
            (direction.cosine, direction.sine),
            (-direction.sine, direction.cosine),
            len(decomposition.components),
            u_min,
            u_max,
            v_min,
            v_max,
            constraints,
            region,
        )
        supports.append(row)
        if checkpoint is not None:
            checkpoint(
                _progress_result(
                    initial_region=initial_region,
                    supports=supports,
                    region=region,
                    decomposition_seconds=decomposition_seconds,
                    projection_seconds=projection_seconds,
                    started=started,
                )
            )
        if not region:
            if time.perf_counter() >= deadline:
                return _partial(
                    initial_region=initial_region,
                    supports=supports,
                    region=region,
                    candidate=None,
                    confirmation=confirmation,
                    conflicting_escape=None,
                    decomposition_seconds=decomposition_seconds,
                    projection_seconds=projection_seconds,
                    confirmation_seconds=confirmation_seconds,
                    started=started,
                    error="sixth-site feasibility deadline reached after empty prefix",
                )
            return SixthSiteFeasibilityResult(
                "complete",
                "empty",
                initial_region,
                tuple(supports),
                region,
                None,
                (),
                None,
                decomposition_seconds,
                projection_seconds,
                0.0,
                _elapsed(started),
            )

    if len(supports) != EXPECTED_ORIENTATIONS or region is None or not region:
        raise SixthSiteFeasibilityError("support pass ended in an impossible state")
    candidate = (
        sum((x for x, _ in region), start=Fraction(0)) / len(region),
        sum((y for _, y in region), start=Fraction(0)) / len(region),
    )
    if not point_in_closed_convex_polygon(candidate, initial_region) or any(
        constraint.value(candidate) > constraint.bound
        for support in supports
        for constraint in support.constraints
    ):
        raise SixthSiteFeasibilityError("canonical candidate fails an exact support constraint")

    candidate_source = replace(original, dots=(*original.dots, candidate))
    conflicting_escape: SelectedEscape | None = None
    confirmation_started = time.perf_counter()
    for index, direction in enumerate(candidate_source.directions):
        if time.perf_counter() >= deadline:
            confirmation_seconds += _elapsed(confirmation_started)
            return _partial(
                initial_region=initial_region,
                supports=supports,
                region=region,
                candidate=candidate,
                confirmation=confirmation,
                conflicting_escape=None,
                decomposition_seconds=decomposition_seconds,
                projection_seconds=projection_seconds,
                confirmation_seconds=confirmation_seconds,
                started=started,
                error="sixth-site feasibility deadline reached during confirmation",
            )
        try:
            measure = measure_direction(
                candidate_source, direction, max_subsets=MAX_SUBSETS, deadline=deadline
            )
        except DeadlineError as error:
            confirmation_seconds += _elapsed(confirmation_started)
            return _partial(
                initial_region=initial_region,
                supports=supports,
                region=region,
                candidate=candidate,
                confirmation=confirmation,
                conflicting_escape=None,
                decomposition_seconds=decomposition_seconds,
                projection_seconds=projection_seconds,
                confirmation_seconds=confirmation_seconds,
                started=started,
                error=str(error),
            )
        row = _direction_result(index, direction.label, measure)
        confirmation.append(row)
        if measure.uncovered_area > 0:
            try:
                conflicting_escape = extract_six_dot_escape(
                    candidate_source, index, deadline=deadline
                )
                replay_six_dot_escape(conflicting_escape, candidate_source, deadline=deadline)
            except DeadlineError as error:
                confirmation_seconds += _elapsed(confirmation_started)
                return _partial(
                    initial_region=initial_region,
                    supports=supports,
                    region=region,
                    candidate=candidate,
                    confirmation=confirmation,
                    conflicting_escape=conflicting_escape,
                    decomposition_seconds=decomposition_seconds,
                    projection_seconds=projection_seconds,
                    confirmation_seconds=confirmation_seconds,
                    started=started,
                    error=str(error),
                )
            except SixDotCoverError as error:
                confirmation_seconds += _elapsed(confirmation_started)
                return SixthSiteFeasibilityResult(
                    "invalid",
                    "inconsistent",
                    initial_region,
                    tuple(supports),
                    region,
                    candidate,
                    tuple(confirmation),
                    None,
                    decomposition_seconds,
                    projection_seconds,
                    confirmation_seconds,
                    _elapsed(started),
                    f"positive confirmation deficit could not be replayed: {error}",
                )
            confirmation_seconds += _elapsed(confirmation_started)
            return SixthSiteFeasibilityResult(
                "invalid",
                "inconsistent",
                initial_region,
                tuple(supports),
                region,
                candidate,
                tuple(confirmation),
                conflicting_escape,
                decomposition_seconds,
                projection_seconds,
                confirmation_seconds,
                _elapsed(started),
                "completed support constraints disagree with independent union replay",
            )
    confirmation_seconds += _elapsed(confirmation_started)
    if len(confirmation) != EXPECTED_ORIENTATIONS:
        raise SixthSiteFeasibilityError("confirmation did not visit all 361 directions")
    if time.perf_counter() >= deadline:
        return _partial(
            initial_region=initial_region,
            supports=supports,
            region=region,
            candidate=candidate,
            confirmation=confirmation,
            conflicting_escape=None,
            decomposition_seconds=decomposition_seconds,
            projection_seconds=projection_seconds,
            confirmation_seconds=confirmation_seconds,
            started=started,
            error="sixth-site feasibility deadline reached after confirmation",
        )
    return SixthSiteFeasibilityResult(
        "complete",
        "covered",
        initial_region,
        tuple(supports),
        region,
        candidate,
        tuple(confirmation),
        None,
        decomposition_seconds,
        projection_seconds,
        confirmation_seconds,
        _elapsed(started),
    )


def _point_record(point: Point) -> list[str]:
    return [str(point[0]), str(point[1])]


def _polygon_record(polygon: Polygon) -> list[list[str]]:
    return [_point_record(point) for point in polygon]


def _attainer_record(attainer: SupportAttainer | None) -> dict[str, object] | None:
    if attainer is None:
        return None
    return {
        "component_index": attainer.component_index,
        "vertex_index": attainer.vertex_index,
        "vertex": _point_record(attainer.vertex),
        "value": str(attainer.value),
        "semantics": "positive-area component closure vertex",
    }


def _constraint_record(constraint: HalfPlane) -> dict[str, object]:
    return {
        "name": constraint.name,
        "a": str(constraint.a),
        "b": str(constraint.b),
        "bound": str(constraint.bound),
        "relation": "a*x+b*y<=bound",
    }


def _direction_record(row: DirectionResult) -> dict[str, object]:
    return {
        "index": row.index,
        "label": row.label,
        "container_area": str(row.container_area),
        "covered_area": str(row.covered_area),
        "uncovered_area": str(row.uncovered_area),
        "nonempty_subsets": row.nonempty_subsets,
    }


def result_document(
    result: SixthSiteFeasibilityResult,
    *,
    source: FrozenInput,
    wall: WallInput,
    selected: SelectedCoverEvidence,
    six_dot: SixDotEscapeEvidence,
    implementation_revision: str,
    process_seconds: float,
) -> dict[str, object]:
    """Serialize exact support evidence and the complete source chain."""

    outcome = {
        "covered": "accept-fixed-D-sixth-site",
        "empty": "refute-fixed-D-plus-one-site-family",
        "incomplete": "incomplete",
        "inconsistent": "invalid-support-union-disagreement",
    }[result.outcome]
    return {
        "schema": "wall-owner-sixth-site-feasibility/v1",
        "status": result.status,
        "outcome": outcome,
        "claim_limit": "the explicit tuple (0,0,0,7) under fixed D plus one site only",
        "sources": {
            "implementation": {
                "git_commit": implementation_revision,
                "module": "packing/devtools/wall_owner_sixth_site_feasibility.py",
            },
            "endpoint": {
                "path": source.source_path,
                "git_commit": source.git_commit,
                "git_blob": source.git_blob,
            },
            "wall": {
                "path": wall.source_path,
                "git_commit": wall.git_commit,
                "git_blob": wall.git_blob,
                "constructor_revision": wall.constructor_revision,
            },
            "selected_cover": {
                "path": selected.source_path,
                "git_commit": selected.git_commit,
                "git_blob": selected.git_blob,
                "implementation_revision": selected.implementation_revision,
            },
            "six_dot_cover": {
                "path": six_dot.source_path,
                "git_commit": six_dot.git_commit,
                "git_blob": six_dot.git_blob,
                "implementation_revision": six_dot.implementation_revision,
            },
        },
        "settings": {
            "outer_side": str(source.outer_side),
            "core_side": str(source.core_side),
            "candidate": list(SELECTED_TUPLE),
            "orientation_count": EXPECTED_ORIENTATIONS,
            "original_dot_count": len(source.dots),
            "support_obstacle_count": len(selected.selected_footprints) + len(source.dots),
            "confirmation_obstacle_count": len(selected.selected_footprints)
            + len(source.dots)
            + 1,
            "max_subsets": MAX_SUBSETS,
            "candidate_limit": 1,
        },
        "initial_region": None
        if result.initial_region is None
        else _polygon_record(result.initial_region),
        "supports": [
            {
                "index": row.index,
                "label": row.label,
                "u": _point_record(row.u),
                "v": _point_record(row.v),
                "component_count": row.component_count,
                "extrema": {
                    "u_min": _attainer_record(row.u_min),
                    "u_max": _attainer_record(row.u_max),
                    "v_min": _attainer_record(row.v_min),
                    "v_max": _attainer_record(row.v_max),
                },
                "constraints": [_constraint_record(item) for item in row.constraints],
                "resulting_region": _polygon_record(row.region),
            }
            for row in result.supports
        ],
        "final_region": None
        if result.final_region is None
        else {
            "dimension": None
            if not result.final_region
            else 0
            if len(result.final_region) == 1
            else 1
            if len(result.final_region) == 2
            else 2,
            "vertices": _polygon_record(result.final_region),
        },
        "canonical_site": None if result.candidate is None else _point_record(result.candidate),
        "confirmation": [_direction_record(row) for row in result.confirmation],
        "conflicting_escape": None
        if result.conflicting_escape is None
        else {
            "orientation_index": result.conflicting_escape.orientation_index,
            "orientation_label": result.conflicting_escape.orientation_label,
            "centre": _point_record(result.conflicting_escape.centre),
            "replay": "open container; closed candidate-site and four-selected-owner avoidance",
        },
        "summary": {
            "support_directions_complete": len(result.supports),
            "confirmation_directions_complete": len(result.confirmation),
            "decomposition_seconds": result.decomposition_seconds,
            "projection_seconds": result.projection_seconds,
            "confirmation_seconds": result.confirmation_seconds,
            "wall_seconds": result.wall_seconds,
            "process_seconds": process_seconds,
        },
        "error": result.error,
    }


def _validate_endpoint_blob(value: str) -> None:
    if value != RETAINED_ENDPOINT_BLOB:
        raise SixthSiteFeasibilityError("endpoint differs from retained exp143 authority")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("endpoint_receipt", type=Path)
    parser.add_argument("wall_receipt", type=Path)
    parser.add_argument("selected_receipt", type=Path)
    parser.add_argument("six_dot_receipt", type=Path)
    parser.add_argument("--expect-endpoint-blob", required=True)
    parser.add_argument("--expect-wall-blob", required=True)
    parser.add_argument("--expect-wall-source", required=True)
    parser.add_argument("--expect-selected-blob", required=True)
    parser.add_argument("--expect-selected-source", required=True)
    parser.add_argument("--expect-six-dot-blob", required=True)
    parser.add_argument("--expect-six-dot-source", required=True)
    parser.add_argument("--expect-git-revision", required=True)
    parser.add_argument("--deadline-seconds", type=float, default=240)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    process_started = time.perf_counter()
    output: Path | None = None
    document: dict[str, object]
    try:
        repository, revision = validate_own_revision(args.expect_git_revision)
        inputs = (
            args.endpoint_receipt,
            args.wall_receipt,
            args.selected_receipt,
            args.six_dot_receipt,
        )
        output = validate_output_path(args.output, repository, inputs)
        _validate_endpoint_blob(args.expect_endpoint_blob)
        source = load_frozen_input(args.endpoint_receipt, args.expect_endpoint_blob)
        wall = load_wall_input(
            args.wall_receipt,
            args.expect_wall_blob,
            expected_source=args.expect_wall_source,
        )
        selected = load_selected_cover_evidence(
            args.selected_receipt,
            args.expect_selected_blob,
            expected_source=args.expect_selected_source,
            source=source,
            wall=wall,
        )
        six_dot = load_six_dot_escape_evidence(
            args.six_dot_receipt,
            args.expect_six_dot_blob,
            expected_source=args.expect_six_dot_source,
            source=source,
            wall=wall,
            selected=selected,
        )

        def checkpoint(result: SixthSiteFeasibilityResult) -> None:
            if output is None:
                raise AssertionError("validated output path unexpectedly missing")
            atomic_write_json(
                output,
                result_document(
                    result,
                    source=source,
                    wall=wall,
                    selected=selected,
                    six_dot=six_dot,
                    implementation_revision=revision,
                    process_seconds=_elapsed(process_started),
                ),
            )

        result = run_sixth_site_feasibility(
            source,
            wall,
            selected,
            six_dot,
            deadline_seconds=args.deadline_seconds,
            checkpoint=checkpoint,
        )
        document = result_document(
            result,
            source=source,
            wall=wall,
            selected=selected,
            six_dot=six_dot,
            implementation_revision=revision,
            process_seconds=_elapsed(process_started),
        )
        atomic_write_json(output, document)
    except (
        AuditError,
        ContainmentError,
        FixedPatternError,
        SelectedCoverError,
        SixDotCoverError,
        SixthSiteScreenError,
        SixthSiteFeasibilityError,
        OSError,
        json.JSONDecodeError,
    ) as error:
        document = {
            "schema": "wall-owner-sixth-site-feasibility/v1",
            "status": "invalid",
            "outcome": "invalid",
            "process_seconds": _elapsed(process_started),
            "error": str(error),
        }
        if output is not None:
            atomic_write_json(output, document)
    print(json.dumps(document, indent=1), flush=True)
    return 0 if document.get("status") == "complete" else 2


if __name__ == "__main__":
    raise SystemExit(main())
