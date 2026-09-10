#!/usr/bin/env python3
"""Exact two-escape intersection screen for one replacement sixth site."""

from __future__ import annotations

import argparse
import json
import math
import time
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Literal, cast

from cases.n11_five_dot_cover.independent_union import (
    AuditError,
    DeadlineError,
    FrozenInput,
    core_offsets,
    load_frozen_input,
)
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
    SIX_DOT_COUNT,
    SixDotCoverError,
    augment_with_selected_escape,
    replay_six_dot_escape,
)


class SixthSiteScreenError(ValueError):
    """A two-escape source, geometry, or execution guard failed."""


@dataclass(frozen=True, slots=True)
class SixDotEscapeEvidence:
    source_path: str
    git_commit: str
    git_blob: str
    implementation_revision: str
    direction: DirectionResult
    escape: SelectedEscape


@dataclass(frozen=True, slots=True)
class StrictSeparator:
    axis: Point
    first_max: Fraction
    second_min: Fraction
    gap: Fraction
    order: Literal["first-before-second", "second-before-first"]


@dataclass(frozen=True, slots=True)
class SixthSiteScreenResult:
    status: Literal["complete", "partial"]
    outcome: Literal["nonempty", "empty", "incomplete"]
    first_core: Polygon | None
    second_core: Polygon | None
    intersection: Polygon | None
    dimension: int | None
    candidate: Point | None
    separator: StrictSeparator | None
    wall_seconds: float
    error: str | None = None


def _mapping(value: object, label: str) -> dict[str, object]:
    if type(value) is not dict:
        raise SixthSiteScreenError(f"{label} must be an object")
    return cast(dict[str, object], value)


def _sequence(value: object, label: str) -> list[object]:
    if type(value) is not list:
        raise SixthSiteScreenError(f"{label} must be an array")
    return cast(list[object], value)


def _keys(value: dict[str, object], expected: set[str], label: str) -> None:
    if set(value) != expected:
        raise SixthSiteScreenError(f"{label} has missing or unexpected fields")


def _integer(value: object, label: str) -> int:
    if type(value) is not int:
        raise SixthSiteScreenError(f"{label} must be an integer")
    return cast(int, value)


def _fraction(value: object, label: str) -> Fraction:
    if not isinstance(value, (str, int)) or isinstance(value, bool):
        raise SixthSiteScreenError(f"{label} must be an exact rational")
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as error:
        raise SixthSiteScreenError(f"{label} is not an exact rational") from error


def _point(value: object, label: str) -> Point:
    raw = _sequence(value, label)
    if len(raw) != 2:
        raise SixthSiteScreenError(f"{label} must have two coordinates")
    return _fraction(raw[0], f"{label}.x"), _fraction(raw[1], f"{label}.y")


def _polygon(value: object, label: str) -> Polygon:
    raw = _sequence(value, label)
    polygon = tuple(_point(item, f"{label}[{index}]") for index, item in enumerate(raw))
    if len(polygon) < 3 or len(set(polygon)) != len(polygon):
        raise SixthSiteScreenError(f"{label} must be a nondegenerate polygon")
    return polygon


def _elapsed(value: object, label: str) -> float:
    if (
        not isinstance(value, (int, float))
        or isinstance(value, bool)
        or not math.isfinite(value)
        or value < 0
    ):
        raise SixthSiteScreenError(f"{label} must be a finite nonnegative duration")
    return float(value)


def parse_six_dot_escape_evidence(
    document: object,
    *,
    source_path: str,
    git_commit: str,
    git_blob: str,
    expected_source: str,
    source: FrozenInput,
    wall: WallInput,
    selected: SelectedCoverEvidence,
) -> SixDotEscapeEvidence:
    """Parse the complete source-bound exp151 refutation."""

    receipt = _mapping(document, "six-dot receipt")
    _keys(
        receipt,
        {
            "schema",
            "status",
            "outcome",
            "claim_limit",
            "sources",
            "settings",
            "sites",
            "selected_footprints",
            "directions",
            "escape",
            "summary",
            "error",
        },
        "six-dot receipt",
    )
    if (
        receipt["schema"] != "wall-owner-six-dot-cover/v1"
        or receipt["status"] != "complete"
        or receipt["outcome"] != "refute-six-dot-cover"
        or receipt["claim_limit"] != "the explicit tuple (0,0,0,7) under fixed D plus x149 only"
        or receipt["error"] is not None
    ):
        raise SixthSiteScreenError("six-dot receipt is not the complete frozen refutation")

    sources = _mapping(receipt["sources"], "six-dot sources")
    _keys(sources, {"implementation", "endpoint", "wall", "selected_cover"}, "sources")
    if _mapping(sources["implementation"], "implementation") != {
        "git_commit": expected_source,
        "module": "packing/devtools/wall_owner_six_dot_cover.py",
    }:
        raise SixthSiteScreenError("six-dot receipt changes its implementation source")
    if _mapping(sources["endpoint"], "endpoint") != {
        "path": source.source_path,
        "git_commit": expected_source,
        "git_blob": source.git_blob,
    }:
        raise SixthSiteScreenError("six-dot receipt changes its endpoint source")
    if _mapping(sources["wall"], "wall") != {
        "path": wall.source_path,
        "git_commit": expected_source,
        "git_blob": wall.git_blob,
        "constructor_revision": wall.constructor_revision,
    }:
        raise SixthSiteScreenError("six-dot receipt changes its wall source")
    if _mapping(sources["selected_cover"], "selected cover") != {
        "path": selected.source_path,
        "git_commit": expected_source,
        "git_blob": selected.git_blob,
        "implementation_revision": selected.implementation_revision,
    }:
        raise SixthSiteScreenError("six-dot receipt changes its selected-cover source")

    augmented = augment_with_selected_escape(source, wall, selected)
    settings = _mapping(receipt["settings"], "six-dot settings")
    if settings != {
        "outer_side": str(source.outer_side),
        "core_side": str(source.core_side),
        "orientation_count": EXPECTED_ORIENTATIONS,
        "candidate": list(SELECTED_TUPLE),
        "selected_classes": [CLASS_IDS[index] for index in SELECTED_TUPLE],
        "corner_order": list(CORNERS),
        "max_subsets": MAX_SUBSETS,
        "candidate_limit": 1,
        "dot_count": SIX_DOT_COUNT,
    }:
        raise SixthSiteScreenError("six-dot receipt changes the frozen settings")
    sites = _mapping(receipt["sites"], "six-dot sites")
    expected_sites = {
        "original": [[str(x), str(y)] for x, y in source.dots],
        "added": [str(selected.escape.centre[0]), str(selected.escape.centre[1])],
        "augmented": [[str(x), str(y)] for x, y in augmented.dots],
    }
    if sites != expected_sites:
        raise SixthSiteScreenError("six-dot receipt changes the six fixed sites")

    raw_footprints = _sequence(receipt["selected_footprints"], "selected footprints")
    if len(raw_footprints) != len(CORNERS):
        raise SixthSiteScreenError("six-dot receipt does not contain four footprints")
    for index, (raw, expected_polygon) in enumerate(
        zip(raw_footprints, augmented.footprints, strict=True)
    ):
        row = _mapping(raw, f"footprint[{index}]")
        _keys(row, {"corner", "class", "polygon"}, f"footprint[{index}]")
        if (
            row["corner"] != CORNERS[index]
            or row["class"] != CLASS_IDS[SELECTED_TUPLE[index]]
            or _polygon(row["polygon"], f"footprint[{index}].polygon") != expected_polygon
        ):
            raise SixthSiteScreenError("six-dot receipt changes a selected footprint")

    raw_directions = _sequence(receipt["directions"], "six-dot directions")
    if len(raw_directions) < 2 or len(raw_directions) >= EXPECTED_ORIENTATIONS:
        raise SixthSiteScreenError("six-dot refutation has an invalid direction prefix")
    directions: list[DirectionResult] = []
    for index, raw in enumerate(raw_directions):
        row = _mapping(raw, f"direction[{index}]")
        _keys(
            row,
            {
                "index",
                "label",
                "container_area",
                "covered_area",
                "uncovered_area",
                "nonempty_subsets",
            },
            f"direction[{index}]",
        )
        container = _fraction(row["container_area"], "container area")
        covered = _fraction(row["covered_area"], "covered area")
        uncovered = _fraction(row["uncovered_area"], "uncovered area")
        count = _integer(row["nonempty_subsets"], "nonempty subsets")
        if (
            _integer(row["index"], "direction index") != index
            or row["label"] != source.directions[index].label
            or container != covered + uncovered
            or covered < 0
            or uncovered < 0
            or count < 0
            or count > MAX_SUBSETS
            or (index < len(raw_directions) - 1 and uncovered != 0)
            or (index == len(raw_directions) - 1 and uncovered <= 0)
        ):
            raise SixthSiteScreenError("six-dot direction prefix is inconsistent")
        directions.append(
            DirectionResult(
                index, cast(str, row["label"]), container, covered, uncovered, count
            )
        )

    raw_escape = _mapping(receipt["escape"], "six-dot escape")
    _keys(raw_escape, {"orientation_index", "orientation_label", "centre", "replay"}, "escape")
    escape = SelectedEscape(
        _integer(raw_escape["orientation_index"], "escape orientation"),
        cast(str, raw_escape["orientation_label"]),
        _point(raw_escape["centre"], "escape centre"),
    )
    if (
        escape.orientation_index != directions[-1].index
        or escape.orientation_label != directions[-1].label
        or raw_escape["replay"]
        != "open container; closed six-dot and four-selected-owner avoidance"
    ):
        raise SixthSiteScreenError("six-dot escape disagrees with the first deficit")

    summary = _mapping(receipt["summary"], "six-dot summary")
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
        "summary",
    )
    _elapsed(summary["wall_seconds"], "geometric duration")
    _elapsed(summary["process_seconds"], "process duration")
    if summary | {"wall_seconds": None, "process_seconds": None} != {
        "checked_directions": len(directions),
        "expected_directions": EXPECTED_ORIENTATIONS,
        "all_covered": False,
        "first_positive_deficit": directions[-1].index,
        "wall_seconds": None,
        "process_seconds": None,
    }:
        raise SixthSiteScreenError("six-dot summary disagrees with its deficit")
    return SixDotEscapeEvidence(
        source_path, git_commit, git_blob, expected_source, directions[-1], escape
    )


def load_six_dot_escape_evidence(
    path: Path,
    expected_blob: str,
    *,
    expected_source: str,
    source: FrozenInput,
    wall: WallInput,
    selected: SelectedCoverEvidence,
) -> SixDotEscapeEvidence:
    """Bind and parse one clean tracked exp151 strict-escape receipt."""

    if len(expected_source) != 40 or any(
        character not in "0123456789abcdef" for character in expected_source
    ):
        raise SixthSiteScreenError("expected six-dot source must be 40 lowercase hex digits")
    _, relative, commit, blob = bind_clean_git_blob(
        path, expected_blob, label="six-dot receipt"
    )
    try:
        document = cast(object, json.loads(path.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError) as error:
        raise SixthSiteScreenError(f"could not read six-dot receipt: {error}") from error
    return parse_six_dot_escape_evidence(
        document,
        source_path=relative,
        git_commit=commit,
        git_blob=blob,
        expected_source=expected_source,
        source=source,
        wall=wall,
        selected=selected,
    )


def escape_core(source: FrozenInput, escape: SelectedEscape) -> Polygon:
    """Construct one exact physical B-core from its saved pose."""

    if not 0 <= escape.orientation_index < len(source.directions):
        raise SixthSiteScreenError("escape direction is outside the manifest")
    direction = source.directions[escape.orientation_index]
    if escape.orientation_label != direction.label:
        raise SixthSiteScreenError("escape label disagrees with the direction manifest")
    return convex_hull(
        tuple(
            (escape.centre[0] + dx, escape.centre[1] + dy)
            for dx, dy in core_offsets(source.core_side, direction)
        )
    )


def strict_separator(first: Polygon, second: Polygon) -> StrictSeparator | None:
    """Return an exact positive SAT separator, if one exists."""

    for polygon in (first, second):
        for start, end in zip(polygon, (*polygon[1:], polygon[0]), strict=True):
            axis = (-(end[1] - start[1]), end[0] - start[0])
            if axis == (0, 0):
                continue
            first_values = tuple(axis[0] * x + axis[1] * y for x, y in first)
            second_values = tuple(axis[0] * x + axis[1] * y for x, y in second)
            if max(first_values) < min(second_values):
                gap = min(second_values) - max(first_values)
                return StrictSeparator(
                    axis, max(first_values), min(second_values), gap, "first-before-second"
                )
            if max(second_values) < min(first_values):
                gap = min(first_values) - max(second_values)
                return StrictSeparator(
                    axis, max(second_values), min(first_values), gap, "second-before-first"
                )
    return None


def run_sixth_site_screen(
    source: FrozenInput,
    wall: WallInput,
    selected: SelectedCoverEvidence,
    six_dot: SixDotEscapeEvidence,
    *,
    deadline_seconds: float = 30,
) -> SixthSiteScreenResult:
    """Replay both escapes and intersect their exact closed cores."""

    if not math.isfinite(deadline_seconds) or deadline_seconds <= 0:
        raise SixthSiteScreenError("internal deadline must be finite and positive")
    if (source.outer_side, source.core_side) != (OUTER_SIDE, CORE_SIDE):
        raise SixthSiteScreenError("source changes the frozen outer or core side")
    if len(source.directions) != EXPECTED_ORIENTATIONS:
        raise SixthSiteScreenError("source lacks the complete 361-direction manifest")
    started = time.perf_counter()
    deadline = started + deadline_seconds
    augmented = augment_with_selected_escape(source, wall, selected)
    try:
        replay_selected_cover_evidence(selected, source=source, deadline=deadline)
        replay_six_dot_escape(six_dot.escape, augmented, deadline=deadline)
    except DeadlineError as error:
        return SixthSiteScreenResult(
            "partial",
            "incomplete",
            None,
            None,
            None,
            None,
            None,
            None,
            time.perf_counter() - started,
            str(error),
        )
    first = escape_core(source, selected.escape)
    second = escape_core(source, six_dot.escape)
    intersection = convex_hull(convex_polygon_intersection(first, second))
    separator: StrictSeparator | None = None
    candidate: Point | None = None
    dimension: int | None
    outcome: Literal["nonempty", "empty"]
    if intersection:
        dimension = 0 if len(intersection) == 1 else 1 if len(intersection) == 2 else 2
        candidate = (
            sum((x for x, _ in intersection), start=Fraction(0)) / len(intersection),
            sum((y for _, y in intersection), start=Fraction(0)) / len(intersection),
        )
        if not point_in_closed_convex_polygon(
            candidate, first
        ) or not point_in_closed_convex_polygon(candidate, second):
            raise SixthSiteScreenError("canonical site fails independent closed membership")
        outcome = "nonempty"
    else:
        dimension = None
        separator = strict_separator(first, second)
        if separator is None or separator.gap <= 0:
            raise SixthSiteScreenError("empty intersection lacks a strict SAT separator")
        outcome = "empty"
    complete = time.perf_counter() < deadline
    return SixthSiteScreenResult(
        "complete" if complete else "partial",
        outcome if complete else "incomplete",
        first,
        second,
        intersection,
        dimension,
        candidate,
        separator,
        time.perf_counter() - started,
        None if complete else "sixth-site screen deadline reached after geometry",
    )


def _point_record(point: Point) -> list[str]:
    return [str(point[0]), str(point[1])]


def _polygon_record(polygon: Polygon) -> list[list[str]]:
    return [_point_record(point) for point in polygon]


def _separator_record(separator: StrictSeparator) -> dict[str, object]:
    return {
        "axis": _point_record(separator.axis),
        "first_max": str(separator.first_max),
        "second_min": str(separator.second_min),
        "gap": str(separator.gap),
        "order": separator.order,
    }


def result_document(
    result: SixthSiteScreenResult,
    *,
    source: FrozenInput,
    wall: WallInput,
    selected: SelectedCoverEvidence,
    six_dot: SixDotEscapeEvidence,
    implementation_revision: str,
    process_seconds: float,
) -> dict[str, object]:
    """Serialize the exact two-core intersection and source receipt chain."""

    outcome = (
        "accept-nonempty-intersection"
        if result.outcome == "nonempty"
        else "refute-empty-intersection"
        if result.outcome == "empty"
        else "incomplete"
    )
    return {
        "schema": "wall-owner-sixth-site-screen/v1",
        "status": result.status,
        "outcome": outcome,
        "claim_limit": "necessary replacement-site screen for fixed D and tuple (0,0,0,7)",
        "sources": {
            "implementation": {
                "git_commit": implementation_revision,
                "module": "packing/devtools/wall_owner_sixth_site_screen.py",
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
            "original_dot_count": len(source.dots),
            "screened_escape_count": 2,
            "candidate_limit": 1,
        },
        "escapes": {
            "exp149": {
                "orientation_index": selected.escape.orientation_index,
                "orientation_label": selected.escape.orientation_label,
                "centre": _point_record(selected.escape.centre),
            },
            "exp151": {
                "orientation_index": six_dot.escape.orientation_index,
                "orientation_label": six_dot.escape.orientation_label,
                "centre": _point_record(six_dot.escape.centre),
            },
        },
        "cores": None
        if result.first_core is None or result.second_core is None
        else {
            "exp149": _polygon_record(result.first_core),
            "exp151": _polygon_record(result.second_core),
        },
        "intersection": None
        if result.intersection is None
        else {
            "dimension": result.dimension,
            "vertices": _polygon_record(result.intersection),
            "canonical_site": None
            if result.candidate is None
            else _point_record(result.candidate),
        },
        "separator": None if result.separator is None else _separator_record(result.separator),
        "replay": {
            "exp149": "open container; closed five-dot and four-selected-owner avoidance",
            "exp151": "open container; closed six-dot and four-selected-owner avoidance",
        },
        "summary": {
            "intersection_nonempty": result.outcome == "nonempty",
            "wall_seconds": result.wall_seconds,
            "process_seconds": process_seconds,
        },
        "error": result.error,
    }


def _validate_endpoint_blob(value: str) -> None:
    if value != RETAINED_ENDPOINT_BLOB:
        raise SixthSiteScreenError("endpoint differs from retained exp143 authority")


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
    parser.add_argument("--deadline-seconds", type=float, default=30)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    started = time.perf_counter()
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
        result = run_sixth_site_screen(
            source, wall, selected, six_dot, deadline_seconds=args.deadline_seconds
        )
        document = result_document(
            result,
            source=source,
            wall=wall,
            selected=selected,
            six_dot=six_dot,
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
        SixthSiteScreenError,
        OSError,
        json.JSONDecodeError,
    ) as error:
        document = {
            "schema": "wall-owner-sixth-site-screen/v1",
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
