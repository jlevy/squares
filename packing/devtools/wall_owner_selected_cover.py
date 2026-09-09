#!/usr/bin/env python3
"""Exact 361-direction cover test for the fixed tuple (0, 0, 0, 7)."""

from __future__ import annotations

import argparse
import json
import math
import time
from dataclasses import dataclass, replace
from fractions import Fraction
from pathlib import Path
from typing import Literal

from cases.n11_five_dot_cover.independent_union import (
    DeadlineError,
    FrozenInput,
    UnionMeasure,
    collision_polygon,
    container_rectangle,
    core_offsets,
    load_frozen_input,
    measure_direction,
)
from devtools.owner_footprints import (
    CORE_SIDE,
    OUTER_SIDE,
    Point,
    Polygon,
)
from devtools.wall_owner_containment import (
    CLASS_IDS,
    CORNERS,
    EXPECTED_ORIENTATIONS,
    ContainmentError,
    WallInput,
    atomic_write_json,
    load_wall_input,
    validate_output_path,
    validate_own_revision,
)
from devtools.wall_owner_fixed_pattern import (
    RETAINED_ENDPOINT_BLOB,
    FixedPatternError,
    component_means,
    core_disjoint_from_polygon,
    selected_wall_footprints,
    strict_dot_free,
)

SELECTED_TUPLE = (0, 0, 0, 7)
EXPECTED_OBSTACLES = 9
EXPECTED_PATCH_VERTICES = 4


class SelectedCoverError(ValueError):
    """A selected-cover input, geometry, or execution guard failed."""


@dataclass(frozen=True, slots=True)
class DirectionResult:
    index: int
    label: str
    container_area: Fraction
    covered_area: Fraction
    uncovered_area: Fraction
    nonempty_subsets: int


@dataclass(frozen=True, slots=True)
class SelectedEscape:
    orientation_index: int
    orientation_label: str
    centre: Point


@dataclass(frozen=True, slots=True)
class SelectedCoverResult:
    status: Literal["complete", "partial"]
    outcome: Literal["covered", "uncovered", "incomplete"]
    directions: tuple[DirectionResult, ...]
    escape: SelectedEscape | None
    selected_footprints: tuple[Polygon, ...]
    wall_seconds: float
    error: str | None = None


def _direction_result(index: int, label: str, measure: UnionMeasure) -> DirectionResult:
    return DirectionResult(
        index,
        label,
        measure.container_area,
        measure.covered_area,
        measure.uncovered_area,
        measure.nonempty_subsets,
    )


def select_four_footprints(source: FrozenInput, wall: WallInput) -> tuple[Polygon, ...]:
    """Resolve the four explicit wall footprints and reject changed complexity."""

    selected = selected_wall_footprints(wall, SELECTED_TUPLE, outer_side=source.outer_side)
    if len(selected) != len(CORNERS) or any(
        len(polygon) != EXPECTED_PATCH_VERTICES for polygon in selected
    ):
        raise SelectedCoverError("selected tuple no longer has four four-vertex patches")
    return selected


def extract_selected_escape(
    source: FrozenInput,
    selected: tuple[Polygon, ...],
    direction_index: int,
) -> SelectedEscape:
    """Extract and independently replay the first strict nine-obstacle escape."""

    direction = source.directions[direction_index]
    offsets = core_offsets(source.core_side, direction)
    obstacles = tuple(collision_polygon(polygon, offsets) for polygon in selected) + tuple(
        collision_polygon((dot,), offsets) for dot in source.dots
    )
    if len(obstacles) != EXPECTED_OBSTACLES:
        raise SelectedCoverError("escape replay requires four owners and five dots")
    container = container_rectangle(source.outer_side, source.core_side, direction)
    for centre in component_means(container, obstacles):
        if not strict_dot_free(
            centre,
            direction,
            outer_side=source.outer_side,
            core_side=source.core_side,
            dots=source.dots,
        ):
            continue
        if all(
            core_disjoint_from_polygon(centre, direction, source.core_side, polygon)
            for polygon in selected
        ):
            return SelectedEscape(direction_index, direction.label, centre)
    raise SelectedCoverError("positive exact deficit lacks a replayable strict escape")


def run_selected_cover(
    source: FrozenInput,
    wall: WallInput,
    *,
    deadline_seconds: float = 240,
) -> SelectedCoverResult:
    """Check the explicit tuple in manifest order and stop at its first deficit."""

    if not math.isfinite(deadline_seconds) or deadline_seconds <= 0:
        raise SelectedCoverError("internal deadline must be finite and positive")
    if (source.outer_side, source.core_side) != (OUTER_SIDE, CORE_SIDE):
        raise SelectedCoverError("source changes the frozen outer or core side")
    if len(source.directions) != EXPECTED_ORIENTATIONS:
        raise SelectedCoverError("source lacks the complete 361-direction manifest")
    started = time.perf_counter()
    deadline = started + deadline_seconds
    selected = select_four_footprints(source, wall)
    substituted = replace(source, footprints=selected)
    rows: list[DirectionResult] = []
    for index, direction in enumerate(substituted.directions):
        if time.perf_counter() >= deadline:
            return SelectedCoverResult(
                "partial",
                "incomplete",
                tuple(rows),
                None,
                selected,
                time.perf_counter() - started,
                "selected-cover deadline reached",
            )
        try:
            measure = measure_direction(
                substituted, direction, max_subsets=511, deadline=deadline
            )
        except DeadlineError:
            return SelectedCoverResult(
                "partial",
                "incomplete",
                tuple(rows),
                None,
                selected,
                time.perf_counter() - started,
                "selected-cover deadline reached",
            )
        if measure.uncovered_area < 0:
            raise SelectedCoverError("independent union returned negative uncovered area")
        rows.append(_direction_result(index, direction.label, measure))
        if measure.uncovered_area > 0:
            if time.perf_counter() >= deadline:
                return SelectedCoverResult(
                    "partial",
                    "incomplete",
                    tuple(rows),
                    None,
                    selected,
                    time.perf_counter() - started,
                    "deadline reached before escape replay",
                )
            escape = extract_selected_escape(source, selected, index)
            if time.perf_counter() >= deadline:
                return SelectedCoverResult(
                    "partial",
                    "incomplete",
                    tuple(rows),
                    escape,
                    selected,
                    time.perf_counter() - started,
                    "deadline reached after escape replay",
                )
            return SelectedCoverResult(
                "complete",
                "uncovered",
                tuple(rows),
                escape,
                selected,
                time.perf_counter() - started,
            )
    if len(rows) != EXPECTED_ORIENTATIONS:
        raise SelectedCoverError("selected-cover check did not visit all 361 directions")
    completed_in_time = time.perf_counter() < deadline
    return SelectedCoverResult(
        "complete" if completed_in_time else "partial",
        "covered" if completed_in_time else "incomplete",
        tuple(rows),
        None,
        selected,
        time.perf_counter() - started,
        None if completed_in_time else "selected-cover deadline reached",
    )


def _point_record(point: Point) -> list[str]:
    return [str(point[0]), str(point[1])]


def _polygon_record(polygon: Polygon) -> list[list[str]]:
    return [_point_record(point) for point in polygon]


def _validate_endpoint_blob(value: str) -> None:
    if value != RETAINED_ENDPOINT_BLOB:
        raise SelectedCoverError("endpoint differs from the retained exp143 authority")


def result_document(
    result: SelectedCoverResult,
    *,
    source: FrozenInput,
    wall: WallInput,
    implementation_revision: str,
    process_seconds: float,
) -> dict[str, object]:
    """Serialize the bounded selected-tuple result and its wall substitution."""

    outcome = (
        "accept-selected-cover"
        if result.outcome == "covered"
        else "refute-selected-cover"
        if result.outcome == "uncovered"
        else "incomplete"
    )
    return {
        "schema": "wall-owner-selected-cover/v1",
        "status": result.status,
        "outcome": outcome,
        "claim_limit": "the explicit tuple (0,0,0,7) under fixed D only",
        "sources": {
            "implementation": {
                "git_commit": implementation_revision,
                "module": "packing/devtools/wall_owner_selected_cover.py",
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
        },
        "settings": {
            "outer_side": str(source.outer_side),
            "core_side": str(source.core_side),
            "orientation_count": EXPECTED_ORIENTATIONS,
            "candidate": list(SELECTED_TUPLE),
            "selected_classes": [CLASS_IDS[index] for index in SELECTED_TUPLE],
            "corner_order": list(CORNERS),
            "max_subsets": 511,
            "candidate_limit": 1,
        },
        "selected_footprints": [
            {
                "corner": CORNERS[index],
                "class": CLASS_IDS[SELECTED_TUPLE[index]],
                "polygon": _polygon_record(polygon),
            }
            for index, polygon in enumerate(result.selected_footprints)
        ],
        "directions": [
            {
                "index": row.index,
                "label": row.label,
                "container_area": str(row.container_area),
                "covered_area": str(row.covered_area),
                "uncovered_area": str(row.uncovered_area),
                "nonempty_subsets": row.nonempty_subsets,
            }
            for row in result.directions
        ],
        "escape": None
        if result.escape is None
        else {
            "orientation_index": result.escape.orientation_index,
            "orientation_label": result.escape.orientation_label,
            "centre": _point_record(result.escape.centre),
            "replay": "open container; closed five-dot and four-selected-owner avoidance",
        },
        "summary": {
            "checked_directions": len(result.directions),
            "expected_directions": EXPECTED_ORIENTATIONS,
            "all_covered": result.outcome == "covered",
            "first_positive_deficit": None
            if result.outcome != "uncovered"
            else result.directions[-1].index,
            "wall_seconds": result.wall_seconds,
            "process_seconds": process_seconds,
        },
        "error": result.error,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("endpoint_receipt", type=Path)
    parser.add_argument("wall_receipt", type=Path)
    parser.add_argument("--expect-endpoint-blob", required=True)
    parser.add_argument("--expect-wall-blob", required=True)
    parser.add_argument("--expect-wall-source", required=True)
    parser.add_argument("--expect-git-revision", required=True)
    parser.add_argument("--deadline-seconds", type=float, default=240)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    started = time.perf_counter()
    output: Path | None = None
    document: dict[str, object]
    try:
        repository, revision = validate_own_revision(args.expect_git_revision)
        inputs = (args.endpoint_receipt, args.wall_receipt)
        output = validate_output_path(args.output, repository, inputs)
        _validate_endpoint_blob(args.expect_endpoint_blob)
        source = load_frozen_input(args.endpoint_receipt, args.expect_endpoint_blob)
        wall = load_wall_input(
            args.wall_receipt,
            args.expect_wall_blob,
            expected_source=args.expect_wall_source,
        )
        result = run_selected_cover(source, wall, deadline_seconds=args.deadline_seconds)
        document = result_document(
            result,
            source=source,
            wall=wall,
            implementation_revision=revision,
            process_seconds=time.perf_counter() - started,
        )
        atomic_write_json(output, document)
    except (
        ContainmentError,
        FixedPatternError,
        SelectedCoverError,
        OSError,
        json.JSONDecodeError,
    ) as error:
        document = {
            "schema": "wall-owner-selected-cover/v1",
            "status": "invalid",
            "outcome": "invalid",
            "process_seconds": time.perf_counter() - started,
            "error": str(error),
        }
        if output is not None:
            atomic_write_json(output, document)
    print(json.dumps(document, indent=1), flush=True)
    return 0 if document.get("status") == "complete" else 2


if __name__ == "__main__":
    raise SystemExit(main())
