#!/usr/bin/env python3
"""Exact cover test for fixed tuple (0, 0, 0, 7) and D plus the exp149 escape."""

from __future__ import annotations

import argparse
import json
import math
import time
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Literal

from cases.n11_five_dot_cover.independent_union import (
    AuditError,
    DeadlineError,
    FrozenInput,
    UnionMeasure,
    collision_polygon,
    container_rectangle,
    core_offsets,
    load_frozen_input,
    measure_direction,
)
from devtools.owner_footprints import CORE_SIDE, OUTER_SIDE, Point, Polygon
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
    strict_dot_free,
)
from devtools.wall_owner_selected_cover import (
    SELECTED_TUPLE,
    DirectionResult,
    SelectedCoverError,
    SelectedCoverEvidence,
    SelectedEscape,
    load_selected_cover_evidence,
    replay_selected_cover_evidence,
    select_four_footprints,
)

ORIGINAL_DOT_COUNT = 5
SIX_DOT_COUNT = 6
EXPECTED_OBSTACLES = 10
MAX_SUBSETS = 1023


class SixDotCoverError(ValueError):
    """A fixed-six-dot source, geometry, or execution guard failed."""


@dataclass(frozen=True, slots=True)
class SixDotCoverResult:
    status: Literal["complete", "partial"]
    outcome: Literal["covered", "uncovered", "incomplete"]
    directions: tuple[DirectionResult, ...]
    escape: SelectedEscape | None
    selected_footprints: tuple[Polygon, ...]
    dots: tuple[Point, ...]
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


def augment_with_selected_escape(
    source: FrozenInput,
    wall: WallInput,
    evidence: SelectedCoverEvidence,
) -> FrozenInput:
    """Return the fixed six-dot input after checking ordering and source geometry."""

    selected = select_four_footprints(source, wall)
    if evidence.selected_footprints != selected:
        raise SixDotCoverError("selected evidence changes the four wall footprints")
    if len(source.dots) != ORIGINAL_DOT_COUNT or len(set(source.dots)) != len(source.dots):
        raise SixDotCoverError("source does not contain the five distinct frozen dots")
    added = evidence.escape.centre
    dots = (*source.dots, added)
    if dots[:ORIGINAL_DOT_COUNT] != source.dots or len(dots) != SIX_DOT_COUNT:
        raise SixDotCoverError("six-dot construction changes the original dot ordering")
    if len(set(dots)) != SIX_DOT_COUNT:
        raise SixDotCoverError("saved escape is not a distinct sixth site")
    return replace(source, footprints=selected, dots=dots)


def is_strict_six_dot_escape(
    centre: Point,
    source: FrozenInput,
    direction_index: int,
) -> bool:
    """Replay strict containment and all ten closed-obstacle avoidances."""

    if len(source.footprints) != len(CORNERS) or len(source.dots) != SIX_DOT_COUNT:
        raise SixDotCoverError("six-dot replay requires four patches and six sites")
    if not 0 <= direction_index < len(source.directions):
        raise SixDotCoverError("six-dot replay direction is outside the manifest")
    direction = source.directions[direction_index]
    return strict_dot_free(
        centre,
        direction,
        outer_side=source.outer_side,
        core_side=source.core_side,
        dots=source.dots,
    ) and all(
        core_disjoint_from_polygon(centre, direction, source.core_side, polygon)
        for polygon in source.footprints
    )


def replay_six_dot_escape(
    escape: SelectedEscape,
    source: FrozenInput,
    *,
    deadline: float,
) -> None:
    """Independently reject a stored witness touching any sixth-input obstacle."""

    if time.perf_counter() >= deadline:
        raise DeadlineError("deadline reached before six-dot escape replay")
    if (
        not 0 <= escape.orientation_index < len(source.directions)
        or source.directions[escape.orientation_index].label != escape.orientation_label
        or not is_strict_six_dot_escape(escape.centre, source, escape.orientation_index)
    ):
        raise SixDotCoverError("six-dot escape fails strict physical replay")
    if time.perf_counter() >= deadline:
        raise DeadlineError("deadline reached after six-dot escape replay")


def extract_six_dot_escape(
    source: FrozenInput, direction_index: int, *, deadline: float
) -> SelectedEscape:
    """Extract one rational component witness and replay all ten obstacles."""

    direction = source.directions[direction_index]
    offsets = core_offsets(source.core_side, direction)
    obstacles = tuple(
        collision_polygon(polygon, offsets) for polygon in source.footprints
    ) + tuple(collision_polygon((dot,), offsets) for dot in source.dots)
    if len(obstacles) != EXPECTED_OBSTACLES:
        raise SixDotCoverError("escape extraction requires four owners and six dots")
    container = container_rectangle(source.outer_side, source.core_side, direction)
    centres = component_means(container, obstacles)
    if time.perf_counter() >= deadline:
        raise DeadlineError("deadline reached during six-dot escape extraction")
    for centre in centres:
        if time.perf_counter() >= deadline:
            raise DeadlineError("deadline reached during six-dot escape extraction")
        escape = SelectedEscape(direction_index, direction.label, centre)
        if is_strict_six_dot_escape(centre, source, direction_index):
            return escape
    raise SixDotCoverError("positive exact deficit lacks a replayable strict escape")


def _partial(  # noqa: PLR0917
    rows: list[DirectionResult],
    selected: tuple[Polygon, ...],
    dots: tuple[Point, ...],
    started: float,
    error: str,
    escape: SelectedEscape | None = None,
) -> SixDotCoverResult:
    return SixDotCoverResult(
        "partial",
        "incomplete",
        tuple(rows),
        escape,
        selected,
        dots,
        time.perf_counter() - started,
        error,
    )


def run_six_dot_cover(  # noqa: PLR0911
    source: FrozenInput,
    wall: WallInput,
    evidence: SelectedCoverEvidence,
    *,
    deadline_seconds: float = 240,
) -> SixDotCoverResult:
    """Check the one fixed six-dot input in full-manifest order."""

    if not math.isfinite(deadline_seconds) or deadline_seconds <= 0:
        raise SixDotCoverError("internal deadline must be finite and positive")
    if (source.outer_side, source.core_side) != (OUTER_SIDE, CORE_SIDE):
        raise SixDotCoverError("source changes the frozen outer or core side")
    if len(source.directions) != EXPECTED_ORIENTATIONS:
        raise SixDotCoverError("source lacks the complete 361-direction manifest")
    started = time.perf_counter()
    deadline = started + deadline_seconds
    augmented = augment_with_selected_escape(source, wall, evidence)
    selected = augmented.footprints
    rows: list[DirectionResult] = []

    try:
        # This authority replay intentionally uses the original five-dot source.
        replay_selected_cover_evidence(evidence, source=source, deadline=deadline)
    except DeadlineError:
        return _partial(
            rows,
            selected,
            augmented.dots,
            started,
            "six-dot deadline reached during selected-escape authority replay",
        )

    for index, direction in enumerate(augmented.directions):
        if time.perf_counter() >= deadline:
            return _partial(rows, selected, augmented.dots, started, "six-dot deadline reached")
        try:
            measure = measure_direction(
                augmented, direction, max_subsets=MAX_SUBSETS, deadline=deadline
            )
        except DeadlineError:
            return _partial(rows, selected, augmented.dots, started, "six-dot deadline reached")
        if measure.uncovered_area < 0:
            raise SixDotCoverError("independent union returned negative uncovered area")
        rows.append(_direction_result(index, direction.label, measure))
        if measure.uncovered_area > 0:
            if time.perf_counter() >= deadline:
                return _partial(
                    rows,
                    selected,
                    augmented.dots,
                    started,
                    "deadline reached before six-dot escape extraction",
                )
            escape: SelectedEscape | None = None
            try:
                escape = extract_six_dot_escape(augmented, index, deadline=deadline)
                replay_six_dot_escape(escape, augmented, deadline=deadline)
            except DeadlineError as error:
                return _partial(
                    rows,
                    selected,
                    augmented.dots,
                    started,
                    str(error),
                    escape,
                )
            if escape is None:
                raise SixDotCoverError("six-dot escape extraction returned no witness")
            return SixDotCoverResult(
                "complete",
                "uncovered",
                tuple(rows),
                escape,
                selected,
                augmented.dots,
                time.perf_counter() - started,
            )

    if len(rows) != EXPECTED_ORIENTATIONS:
        raise SixDotCoverError("six-dot check did not visit all 361 directions")
    if time.perf_counter() >= deadline:
        return _partial(
            rows,
            selected,
            augmented.dots,
            started,
            "six-dot deadline reached after the final direction",
        )
    return SixDotCoverResult(
        "complete",
        "covered",
        tuple(rows),
        None,
        selected,
        augmented.dots,
        time.perf_counter() - started,
    )


def _point_record(point: Point) -> list[str]:
    return [str(point[0]), str(point[1])]


def _polygon_record(polygon: Polygon) -> list[list[str]]:
    return [_point_record(point) for point in polygon]


def _validate_endpoint_blob(value: str) -> None:
    if value != RETAINED_ENDPOINT_BLOB:
        raise SixDotCoverError("endpoint differs from the retained exp143 authority")


def result_document(
    result: SixDotCoverResult,
    *,
    source: FrozenInput,
    wall: WallInput,
    selected: SelectedCoverEvidence,
    implementation_revision: str,
    process_seconds: float,
) -> dict[str, object]:
    """Serialize the fixed-six-dot decision and all bound source identities."""

    outcome = (
        "accept-six-dot-cover"
        if result.outcome == "covered"
        else "refute-six-dot-cover"
        if result.outcome == "uncovered"
        else "incomplete"
    )
    return {
        "schema": "wall-owner-six-dot-cover/v1",
        "status": result.status,
        "outcome": outcome,
        "claim_limit": "the explicit tuple (0,0,0,7) under fixed D plus x149 only",
        "sources": {
            "implementation": {
                "git_commit": implementation_revision,
                "module": "packing/devtools/wall_owner_six_dot_cover.py",
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
        },
        "settings": {
            "outer_side": str(source.outer_side),
            "core_side": str(source.core_side),
            "orientation_count": EXPECTED_ORIENTATIONS,
            "candidate": list(SELECTED_TUPLE),
            "selected_classes": [CLASS_IDS[index] for index in SELECTED_TUPLE],
            "corner_order": list(CORNERS),
            "max_subsets": MAX_SUBSETS,
            "candidate_limit": 1,
            "dot_count": SIX_DOT_COUNT,
        },
        "sites": {
            "original": [_point_record(point) for point in source.dots],
            "added": _point_record(selected.escape.centre),
            "augmented": [_point_record(point) for point in result.dots],
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
            "replay": "open container; closed six-dot and four-selected-owner avoidance",
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
    parser.add_argument("selected_receipt", type=Path)
    parser.add_argument("--expect-endpoint-blob", required=True)
    parser.add_argument("--expect-wall-blob", required=True)
    parser.add_argument("--expect-wall-source", required=True)
    parser.add_argument("--expect-selected-blob", required=True)
    parser.add_argument("--expect-selected-source", required=True)
    parser.add_argument("--expect-git-revision", required=True)
    parser.add_argument("--deadline-seconds", type=float, default=240)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    started = time.perf_counter()
    output: Path | None = None
    document: dict[str, object]
    try:
        repository, revision = validate_own_revision(args.expect_git_revision)
        inputs = (args.endpoint_receipt, args.wall_receipt, args.selected_receipt)
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
        result = run_six_dot_cover(
            source, wall, selected, deadline_seconds=args.deadline_seconds
        )
        document = result_document(
            result,
            source=source,
            wall=wall,
            selected=selected,
            implementation_revision=revision,
            process_seconds=time.perf_counter() - started,
        )
        atomic_write_json(output, document)
    except (
        AuditError,
        ContainmentError,
        FixedPatternError,
        SelectedCoverError,
        SixDotCoverError,
        OSError,
        json.JSONDecodeError,
    ) as error:
        document = {
            "schema": "wall-owner-six-dot-cover/v1",
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
