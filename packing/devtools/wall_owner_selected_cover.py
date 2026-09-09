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
from typing import Literal, cast

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
    bind_clean_git_blob,
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


@dataclass(frozen=True, slots=True)
class SelectedCoverEvidence:
    """One source-bound, parsed exp149 strict escape."""

    source_path: str
    git_commit: str
    git_blob: str
    implementation_revision: str
    direction: DirectionResult
    escape: SelectedEscape
    selected_footprints: tuple[Polygon, ...]


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


def _mapping(value: object, label: str) -> dict[str, object]:
    if type(value) is not dict:
        raise SelectedCoverError(f"{label} must be an object")
    return cast(dict[str, object], value)


def _sequence(value: object, label: str) -> list[object]:
    if type(value) is not list:
        raise SelectedCoverError(f"{label} must be an array")
    return cast(list[object], value)


def _keys(value: dict[str, object], expected: set[str], label: str) -> None:
    if set(value) != expected:
        raise SelectedCoverError(f"{label} has missing or unexpected fields")


def _integer(value: object, label: str) -> int:
    if type(value) is not int:
        raise SelectedCoverError(f"{label} must be an integer")
    return cast(int, value)


def _fraction(value: object, label: str) -> Fraction:
    if not isinstance(value, (str, int)) or isinstance(value, bool):
        raise SelectedCoverError(f"{label} must be an exact rational")
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as error:
        raise SelectedCoverError(f"{label} is not an exact rational") from error


def _point(value: object, label: str) -> Point:
    raw = _sequence(value, label)
    if len(raw) != 2:
        raise SelectedCoverError(f"{label} must have two coordinates")
    return _fraction(raw[0], f"{label}.x"), _fraction(raw[1], f"{label}.y")


def _polygon(value: object, label: str) -> Polygon:
    raw = _sequence(value, label)
    polygon = tuple(_point(item, f"{label}[{index}]") for index, item in enumerate(raw))
    if len(polygon) < 3 or len(set(polygon)) != len(polygon):
        raise SelectedCoverError(f"{label} must be a nondegenerate polygon")
    return polygon


def _elapsed(value: object, label: str) -> float:
    if (
        not isinstance(value, (int, float))
        or isinstance(value, bool)
        or not math.isfinite(value)
        or value < 0
    ):
        raise SelectedCoverError(f"{label} must be a finite nonnegative duration")
    return float(value)


def parse_selected_cover_evidence(
    document: object,
    *,
    source_path: str,
    git_commit: str,
    git_blob: str,
    expected_source: str,
    source: FrozenInput,
    wall: WallInput,
) -> SelectedCoverEvidence:
    """Parse a complete exp149 refutation against already validated inputs."""

    receipt = _mapping(document, "selected receipt")
    _keys(
        receipt,
        {
            "schema",
            "status",
            "outcome",
            "claim_limit",
            "sources",
            "settings",
            "selected_footprints",
            "directions",
            "escape",
            "summary",
            "error",
        },
        "selected receipt",
    )
    if (
        receipt["schema"] != "wall-owner-selected-cover/v1"
        or receipt["status"] != "complete"
        or receipt["outcome"] != "refute-selected-cover"
        or receipt["claim_limit"] != "the explicit tuple (0,0,0,7) under fixed D only"
        or receipt["error"] is not None
    ):
        raise SelectedCoverError("selected receipt is not the complete frozen refutation")

    sources = _mapping(receipt["sources"], "selected sources")
    _keys(sources, {"implementation", "endpoint", "wall"}, "selected sources")
    implementation = _mapping(sources["implementation"], "selected implementation")
    endpoint = _mapping(sources["endpoint"], "selected endpoint source")
    wall_source = _mapping(sources["wall"], "selected wall source")
    _keys(implementation, {"git_commit", "module"}, "selected implementation")
    _keys(endpoint, {"path", "git_commit", "git_blob"}, "selected endpoint source")
    _keys(
        wall_source,
        {"path", "git_commit", "git_blob", "constructor_revision"},
        "selected wall source",
    )
    if implementation != {
        "git_commit": expected_source,
        "module": "packing/devtools/wall_owner_selected_cover.py",
    }:
        raise SelectedCoverError("selected receipt changes its implementation source")
    if endpoint != {
        "path": source.source_path,
        "git_commit": expected_source,
        "git_blob": source.git_blob,
    }:
        raise SelectedCoverError("selected receipt changes its endpoint source")
    if wall_source != {
        "path": wall.source_path,
        "git_commit": expected_source,
        "git_blob": wall.git_blob,
        "constructor_revision": wall.constructor_revision,
    }:
        raise SelectedCoverError("selected receipt changes its wall source")

    settings = _mapping(receipt["settings"], "selected settings")
    expected_settings: dict[str, object] = {
        "outer_side": str(source.outer_side),
        "core_side": str(source.core_side),
        "orientation_count": EXPECTED_ORIENTATIONS,
        "candidate": list(SELECTED_TUPLE),
        "selected_classes": [CLASS_IDS[index] for index in SELECTED_TUPLE],
        "corner_order": list(CORNERS),
        "max_subsets": 511,
        "candidate_limit": 1,
    }
    if settings != expected_settings:
        raise SelectedCoverError("selected receipt changes the frozen settings")

    expected_footprints = select_four_footprints(source, wall)
    raw_footprints = _sequence(receipt["selected_footprints"], "selected footprints")
    if len(raw_footprints) != len(CORNERS):
        raise SelectedCoverError("selected receipt does not contain four footprints")
    parsed_footprints: list[Polygon] = []
    for index, (value, expected_polygon) in enumerate(
        zip(raw_footprints, expected_footprints, strict=True)
    ):
        row = _mapping(value, f"selected footprints[{index}]")
        _keys(row, {"corner", "class", "polygon"}, f"selected footprints[{index}]")
        polygon = _polygon(row["polygon"], f"selected footprints[{index}].polygon")
        if (
            row["corner"] != CORNERS[index]
            or row["class"] != CLASS_IDS[SELECTED_TUPLE[index]]
            or polygon != expected_polygon
        ):
            raise SelectedCoverError("selected receipt changes a selected footprint")
        parsed_footprints.append(polygon)

    directions = _sequence(receipt["directions"], "selected directions")
    if len(directions) != 1:
        raise SelectedCoverError("selected refutation must stop at its first direction")
    raw_direction = _mapping(directions[0], "selected directions[0]")
    _keys(
        raw_direction,
        {
            "index",
            "label",
            "container_area",
            "covered_area",
            "uncovered_area",
            "nonempty_subsets",
        },
        "selected directions[0]",
    )
    index = _integer(raw_direction["index"], "selected direction index")
    container_area = _fraction(raw_direction["container_area"], "selected container area")
    covered_area = _fraction(raw_direction["covered_area"], "selected covered area")
    uncovered_area = _fraction(raw_direction["uncovered_area"], "selected uncovered area")
    nonempty_subsets = _integer(raw_direction["nonempty_subsets"], "selected nonempty subsets")
    if (
        index != 0
        or raw_direction["label"] != source.directions[index].label
        or uncovered_area <= 0
        or covered_area < 0
        or container_area != covered_area + uncovered_area
        or nonempty_subsets != 41
    ):
        raise SelectedCoverError("selected direction does not retain the exact first deficit")
    direction = DirectionResult(
        index,
        cast(str, raw_direction["label"]),
        container_area,
        covered_area,
        uncovered_area,
        nonempty_subsets,
    )

    raw_escape = _mapping(receipt["escape"], "selected escape")
    _keys(
        raw_escape,
        {"orientation_index", "orientation_label", "centre", "replay"},
        "selected escape",
    )
    escape = SelectedEscape(
        _integer(raw_escape["orientation_index"], "selected escape orientation"),
        cast(str, raw_escape["orientation_label"]),
        _point(raw_escape["centre"], "selected escape centre"),
    )
    if (
        escape.orientation_index != direction.index
        or escape.orientation_label != direction.label
        or raw_escape["replay"]
        != "open container; closed five-dot and four-selected-owner avoidance"
    ):
        raise SelectedCoverError("selected escape disagrees with the first deficit")

    summary = _mapping(receipt["summary"], "selected summary")
    _keys(
        summary,
        {
            "checked_directions",
            "expected_directions",
            "all_covered",
            "first_positive_deficit",
            "wall_seconds",
            "process_seconds",
        },
        "selected summary",
    )
    _elapsed(summary["wall_seconds"], "selected geometric duration")
    _elapsed(summary["process_seconds"], "selected process duration")
    if summary | {"wall_seconds": None, "process_seconds": None} != {
        "checked_directions": 1,
        "expected_directions": EXPECTED_ORIENTATIONS,
        "all_covered": False,
        "first_positive_deficit": 0,
        "wall_seconds": None,
        "process_seconds": None,
    }:
        raise SelectedCoverError("selected summary disagrees with the first deficit")
    return SelectedCoverEvidence(
        source_path,
        git_commit,
        git_blob,
        expected_source,
        direction,
        escape,
        tuple(parsed_footprints),
    )


def load_selected_cover_evidence(
    path: Path,
    expected_blob: str,
    *,
    expected_source: str,
    source: FrozenInput,
    wall: WallInput,
) -> SelectedCoverEvidence:
    """Bind and parse one clean tracked exp149 selected-cover refutation."""

    if len(expected_source) != 40 or any(
        character not in "0123456789abcdef" for character in expected_source
    ):
        raise SelectedCoverError("expected selected source must be 40 lowercase hex digits")
    _, relative, commit, blob = bind_clean_git_blob(
        path, expected_blob, label="selected receipt"
    )
    try:
        document = cast(object, json.loads(path.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError) as error:
        raise SelectedCoverError(f"could not read selected receipt: {error}") from error
    return parse_selected_cover_evidence(
        document,
        source_path=relative,
        git_commit=commit,
        git_blob=blob,
        expected_source=expected_source,
        source=source,
        wall=wall,
    )


def replay_selected_cover_evidence(
    evidence: SelectedCoverEvidence,
    *,
    source: FrozenInput,
    deadline: float,
) -> None:
    """Replay the saved centre's strict physical semantics without a union search."""

    if time.perf_counter() >= deadline:
        raise DeadlineError("deadline reached before selected escape replay")
    direction = source.directions[evidence.escape.orientation_index]
    centre = evidence.escape.centre
    if not strict_dot_free(
        centre,
        direction,
        outer_side=source.outer_side,
        core_side=source.core_side,
        dots=source.dots,
    ) or not all(
        core_disjoint_from_polygon(centre, direction, source.core_side, polygon)
        for polygon in evidence.selected_footprints
    ):
        raise SelectedCoverError("saved selected escape fails strict physical replay")
    if time.perf_counter() >= deadline:
        raise DeadlineError("deadline reached after selected escape replay")


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
