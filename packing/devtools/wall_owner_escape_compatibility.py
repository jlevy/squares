#!/usr/bin/env python3
"""Test one saved residual core against its four selected snapped-owner classes."""

from __future__ import annotations

import argparse
import json
import math
import time
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Literal

from cases.n11_five_dot_cover.independent_union import (
    DeadlineError,
    FrozenInput,
    load_frozen_input,
)
from devtools.owner_footprints import (
    CORE_SIDE,
    OUTER_SIDE,
    DirectionSource,
    Point,
    Polygon,
    convex_hull,
    convex_polygons_strictly_disjoint,
    full_owner_direction_manifest,
    owner_branch_manifest,
    point_in_closed_convex_polygon,
)
from devtools.wall_owner_containment import (
    CLASS_IDS,
    CORNERS,
    AffineMap,
    ContainmentError,
    WallClass,
    WallInput,
    atomic_write_json,
    load_wall_input,
    physical_corner_maps,
    validate_output_path,
    validate_own_revision,
)
from devtools.wall_owner_footprints import OwnerFrameFootprint, closed_centre_set
from devtools.wall_owner_selected_cover import (
    SELECTED_TUPLE,
    SelectedCoverError,
    SelectedCoverEvidence,
    load_selected_cover_evidence,
    replay_selected_cover_evidence,
)

EXPECTED_FRAMES_PER_CLASS = 181
EXPECTED_AXES_PER_FRAME = 8
EVALUATION_CORNER_INDICES = (3, 0, 1, 2)  # TR, BL, BR, TL


class EscapeCompatibilityError(ValueError):
    """An input, geometry, replay, or execution guard refused the test."""


@dataclass(frozen=True, slots=True)
class TransformedOwnerFrame:
    """One exp146 frame transported into its selected physical corner."""

    source: OwnerFrameFootprint
    centre_set: Polygon
    owner_u: Point
    owner_v: Point


@dataclass(frozen=True, slots=True)
class AxisExtremum:
    """The best owner-centre separation on one signed SAT axis."""

    label: str
    axis: Point
    minimum_owner_projection: Fraction
    owner_radius: Fraction
    residual_radius: Fraction
    slack: Fraction
    canonical_owner_centre: Point
    owner_centre: Point


@dataclass(frozen=True, slots=True)
class FrameExtremum:
    """The exact maximum over all eight signed axes for one owner frame."""

    frame_index: int
    source: OwnerFrameFootprint
    owner_u: Point
    owner_v: Point
    maximum: AxisExtremum
    axes_checked: int = EXPECTED_AXES_PER_FRAME


@dataclass(frozen=True, slots=True)
class ClassCompatibility:
    """A compatible prefix, exhaustive incompatibility, or partial class row."""

    corner_index: int
    class_index: int
    corner_map: AffineMap
    status: Literal["compatible", "incompatible", "partial"]
    expected_frames: int
    frame_extrema: tuple[FrameExtremum, ...]
    observed_maximum_slack: Fraction | None
    global_maximum_slack: Fraction | None
    error: str | None = None

    @property
    def positive_witness(self) -> FrameExtremum | None:
        if self.status != "compatible":
            return None
        return next(
            (row for row in self.frame_extrema if row.maximum.slack > 0),
            None,
        )


@dataclass(frozen=True, slots=True)
class EscapeCompatibilityResult:
    """The bounded result across the fixed TR, BL, BR, TL order."""

    status: Literal["complete", "partial"]
    outcome: Literal["incompatible-class", "all-selected-classes-compatible", "incomplete"]
    classes: tuple[ClassCompatibility, ...]
    wall_seconds: float
    error: str | None = None


def _dot(left: Point, right: Point) -> Fraction:
    return left[0] * right[0] + left[1] * right[1]


def _subtract(left: Point, right: Point) -> Point:
    return left[0] - right[0], left[1] - right[1]


def _turn(point: Point) -> Point:
    return -point[1], point[0]


def _negate(point: Point) -> Point:
    return -point[0], -point[1]


def _deadline(deadline: float, message: str) -> None:
    if time.perf_counter() >= deadline:
        raise DeadlineError(message)


def transform_owner_frame(
    frame: OwnerFrameFootprint, transform: AffineMap
) -> TransformedOwnerFrame:
    """Transport a centre set and its ordered owner axes into world coordinates."""

    ray = frame.frame.ray
    turned = _turn(ray)
    if transform.determinant == 1:
        owner_u = transform.linear(ray)
        owner_v = transform.linear(turned)
    elif transform.determinant == -1:
        owner_u = transform.linear(turned)
        owner_v = transform.linear(ray)
    else:
        raise EscapeCompatibilityError("corner map must preserve exact Euclidean scale")
    if owner_v != _turn(owner_u) or _dot(owner_u, owner_u) != 1:
        raise EscapeCompatibilityError("corner transport lost a right-handed unit frame")
    return TransformedOwnerFrame(
        frame,
        tuple(transform.point(point) for point in frame.centre_set),
        owner_u,
        owner_v,
    )


def _axis_rows(owner_u: Point, owner_v: Point, residual_u: Point, residual_v: Point):
    return (
        ("+owner-u", owner_u),
        ("-owner-u", _negate(owner_u)),
        ("+owner-v", owner_v),
        ("-owner-v", _negate(owner_v)),
        ("+residual-u", residual_u),
        ("-residual-u", _negate(residual_u)),
        ("+residual-v", residual_v),
        ("-residual-v", _negate(residual_v)),
    )


def frame_separation_extremum(
    frame: OwnerFrameFootprint,
    *,
    frame_index: int,
    transform: AffineMap,
    residual_centre: Point,
    residual_u: Point,
    half: Fraction,
    deadline: float | None = None,
) -> FrameExtremum:
    """Maximize the exact strict-separation slack over one retained frame."""

    if frame.disposition != "allowed" or not frame.centre_set:
        raise EscapeCompatibilityError("a selected compatibility frame must be allowed")
    if half <= 0 or _dot(residual_u, residual_u) != 1:
        raise EscapeCompatibilityError("compatibility requires positive size and unit axes")
    transformed = transform_owner_frame(frame, transform)
    residual_v = _turn(residual_u)
    rows: list[AxisExtremum] = []
    for label, axis in _axis_rows(
        transformed.owner_u,
        transformed.owner_v,
        residual_u,
        residual_v,
    ):
        if deadline is not None:
            _deadline(deadline, "compatibility deadline reached within a frame")
        projections = tuple(_dot(axis, point) for point in transformed.centre_set)
        minimum = min(projections)
        minimizers = tuple(
            (canonical, world)
            for canonical, world, projection in zip(
                frame.centre_set,
                transformed.centre_set,
                projections,
                strict=True,
            )
            if projection == minimum
        )
        canonical_centre, owner_centre = min(minimizers, key=lambda item: item[1])
        owner_radius = half * (
            abs(_dot(axis, transformed.owner_u)) + abs(_dot(axis, transformed.owner_v))
        )
        residual_radius = half * (abs(_dot(axis, residual_u)) + abs(_dot(axis, residual_v)))
        rows.append(
            AxisExtremum(
                label,
                axis,
                minimum,
                owner_radius,
                residual_radius,
                _dot(axis, residual_centre) - minimum - owner_radius - residual_radius,
                canonical_centre,
                owner_centre,
            )
        )
    maximum = max(rows, key=lambda row: row.slack)
    return FrameExtremum(
        frame_index,
        frame,
        transformed.owner_u,
        transformed.owner_v,
        maximum,
    )


def _square(centre: Point, first: Point, second: Point, half: Fraction) -> Polygon:
    return convex_hull(
        tuple(
            (
                centre[0] + half * (first_sign * first[0] + second_sign * second[0]),
                centre[1] + half * (first_sign * first[1] + second_sign * second[1]),
            )
            for first_sign in (-1, 1)
            for second_sign in (-1, 1)
        )
    )


def replay_positive_witness(
    row: FrameExtremum,
    *,
    owner_mark: Point,
    transform: AffineMap,
    residual_centre: Point,
    residual_u: Point,
    outer_side: Fraction,
    half: Fraction,
) -> None:
    """Independently replay class membership, containment, and polygon SAT."""

    if row.maximum.slack <= 0:
        raise EscapeCompatibilityError("positive witness replay received nonpositive slack")
    frame = row.source
    ray = frame.frame.ray
    rebuilt = closed_centre_set(owner_mark, ray, outer_side=outer_side, half=half)
    if rebuilt != frame.centre_set:
        raise EscapeCompatibilityError("positive witness centre set fails reconstruction")
    canonical_centre = row.maximum.canonical_owner_centre
    if not point_in_closed_convex_polygon(canonical_centre, rebuilt):
        raise EscapeCompatibilityError("positive witness leaves its canonical centre set")
    displacement = _subtract(canonical_centre, owner_mark)
    turned = _turn(ray)
    if not (0 <= _dot(displacement, ray) <= half and 0 <= _dot(displacement, turned) <= half):
        raise EscapeCompatibilityError("positive witness leaves its class displacement box")
    transformed = transform_owner_frame(frame, transform)
    if (
        row.owner_u != transformed.owner_u
        or row.owner_v != transformed.owner_v
        or row.maximum.owner_centre != transform.point(canonical_centre)
        or not point_in_closed_convex_polygon(row.maximum.owner_centre, transformed.centre_set)
    ):
        raise EscapeCompatibilityError("positive witness corner transport is inconsistent")
    owner = _square(
        row.maximum.owner_centre,
        transformed.owner_u,
        transformed.owner_v,
        half,
    )
    residual_v = _turn(residual_u)
    residual = _square(residual_centre, residual_u, residual_v, half)
    transformed_mark = transform.point(owner_mark)
    if not point_in_closed_convex_polygon(transformed_mark, owner):
        raise EscapeCompatibilityError("positive witness owner core loses its mark")
    if any(not (0 <= coordinate <= outer_side) for vertex in owner for coordinate in vertex):
        raise EscapeCompatibilityError("positive witness owner core leaves the container")
    if not convex_polygons_strictly_disjoint(owner, residual):
        raise EscapeCompatibilityError("positive witness fails independent polygon SAT")


def _explicit_frame_maximum(
    frame: OwnerFrameFootprint,
    *,
    transform: AffineMap,
    residual_centre: Point,
    residual_u: Point,
    half: Fraction,
) -> Fraction:
    """Replay a frame maximum from explicit square-vertex projection intervals."""

    transformed = transform_owner_frame(frame, transform)
    residual_v = _turn(residual_u)
    residual = _square(residual_centre, residual_u, residual_v, half)
    best: Fraction | None = None
    for owner_centre in transformed.centre_set:
        owner = _square(
            owner_centre,
            transformed.owner_u,
            transformed.owner_v,
            half,
        )
        for axis in (
            transformed.owner_u,
            transformed.owner_v,
            residual_u,
            residual_v,
        ):
            owner_projection = tuple(_dot(axis, point) for point in owner)
            residual_projection = tuple(_dot(axis, point) for point in residual)
            for gap in (
                min(residual_projection) - max(owner_projection),
                min(owner_projection) - max(residual_projection),
            ):
                if best is None or gap > best:
                    best = gap
    if best is None:
        raise EscapeCompatibilityError("explicit replay received an empty centre set")
    return best


def replay_incompatible_class(
    result: ClassCompatibility,
    *,
    owner_mark: Point,
    residual_centre: Point,
    residual_u: Point,
    outer_side: Fraction,
    half: Fraction,
    deadline: float,
) -> None:
    """Rebuild every centre set and independently replay one universal maximum."""

    if result.status != "incompatible" or len(result.frame_extrema) != result.expected_frames:
        raise EscapeCompatibilityError("universal replay requires one exhausted class")
    replayed: list[Fraction] = []
    for row in result.frame_extrema:
        _deadline(deadline, "compatibility deadline reached during universal replay")
        rebuilt = closed_centre_set(
            owner_mark,
            row.source.frame.ray,
            outer_side=outer_side,
            half=half,
        )
        if rebuilt != row.source.centre_set:
            raise EscapeCompatibilityError("universal replay centre set differs from source")
        maximum = _explicit_frame_maximum(
            row.source,
            transform=result.corner_map,
            residual_centre=residual_centre,
            residual_u=residual_u,
            half=half,
        )
        if maximum != row.maximum.slack or maximum > 0:
            raise EscapeCompatibilityError("universal explicit replay disagrees with slack")
        replayed.append(maximum)
    if not replayed or max(replayed) != result.global_maximum_slack:
        raise EscapeCompatibilityError("universal class maximum fails independent replay")


def evaluate_class(
    wall_class: WallClass,
    *,
    owner_mark: Point,
    corner_index: int,
    class_index: int,
    transform: AffineMap,
    residual_centre: Point,
    residual_u: Point,
    expected_frames: int,
    outer_side: Fraction,
    half: Fraction,
    deadline: float,
) -> ClassCompatibility:
    """Evaluate one selected class, permitting early exit only on a witness."""

    if wall_class.disposition != "possible" or wall_class.wall_footprint is None:
        raise EscapeCompatibilityError("selected class is not a possible exp146 class")
    if len(wall_class.frames) != expected_frames or not wall_class.frames:
        raise EscapeCompatibilityError("selected class does not have its complete frame list")
    if any(
        frame.disposition != "allowed" or not frame.centre_set for frame in wall_class.frames
    ):
        raise EscapeCompatibilityError("selected class has an empty or unresolved frame")

    rows: list[FrameExtremum] = []
    try:
        for frame_index, frame in enumerate(wall_class.frames):
            _deadline(deadline, "compatibility deadline reached between frames")
            row = frame_separation_extremum(
                frame,
                frame_index=frame_index,
                transform=transform,
                residual_centre=residual_centre,
                residual_u=residual_u,
                half=half,
                deadline=deadline,
            )
            rows.append(row)
            if row.maximum.slack > 0:
                replay_positive_witness(
                    row,
                    owner_mark=owner_mark,
                    transform=transform,
                    residual_centre=residual_centre,
                    residual_u=residual_u,
                    outer_side=outer_side,
                    half=half,
                )
                _deadline(deadline, "compatibility deadline reached after witness replay")
                return ClassCompatibility(
                    corner_index,
                    class_index,
                    transform,
                    "compatible",
                    expected_frames,
                    tuple(rows),
                    max(item.maximum.slack for item in rows),
                    None,
                )
    except DeadlineError as error:
        return ClassCompatibility(
            corner_index,
            class_index,
            transform,
            "partial",
            expected_frames,
            tuple(rows),
            max((item.maximum.slack for item in rows), default=None),
            None,
            str(error),
        )

    maximum = max(row.maximum.slack for row in rows)
    result = ClassCompatibility(
        corner_index,
        class_index,
        transform,
        "incompatible",
        expected_frames,
        tuple(rows),
        maximum,
        maximum,
    )
    try:
        replay_incompatible_class(
            result,
            owner_mark=owner_mark,
            residual_centre=residual_centre,
            residual_u=residual_u,
            outer_side=outer_side,
            half=half,
            deadline=deadline,
        )
        _deadline(deadline, "compatibility deadline reached after universal replay")
    except DeadlineError as error:
        return ClassCompatibility(
            corner_index,
            class_index,
            transform,
            "partial",
            expected_frames,
            tuple(rows),
            maximum,
            None,
            str(error),
        )
    return result


def run_escape_compatibility(
    source: FrozenInput,
    wall: WallInput,
    evidence: SelectedCoverEvidence,
    *,
    deadline_seconds: float,
    expected_frames: int = EXPECTED_FRAMES_PER_CLASS,
) -> EscapeCompatibilityResult:
    """Run the one-pose discriminator in its frozen corner order."""

    started = time.perf_counter()
    if not math.isfinite(deadline_seconds) or deadline_seconds <= 0 or expected_frames <= 0:
        raise EscapeCompatibilityError("deadline and expected frame count must be positive")
    if (source.outer_side, source.core_side) != (OUTER_SIDE, CORE_SIDE):
        raise EscapeCompatibilityError("compatibility input changes the frozen scale")
    if evidence.escape.orientation_index >= len(source.directions):
        raise EscapeCompatibilityError("saved escape orientation leaves the source manifest")
    deadline = started + deadline_seconds
    try:
        replay_selected_cover_evidence(evidence, source=source, deadline=deadline)
    except DeadlineError as error:
        return EscapeCompatibilityResult(
            "partial", "incomplete", (), time.perf_counter() - started, str(error)
        )

    manifest = full_owner_direction_manifest()
    branch = owner_branch_manifest(manifest)
    maps = physical_corner_maps()
    residual_direction = source.directions[evidence.escape.orientation_index]
    residual_u = residual_direction.cosine, residual_direction.sine
    rows: list[ClassCompatibility] = []
    for corner_index in EVALUATION_CORNER_INDICES:
        class_index = SELECTED_TUPLE[corner_index]
        owner_class = branch.classes[class_index]
        wall_class = wall.classes[class_index]
        if (
            wall_class.class_id != owner_class.class_id
            or wall_class.class_id != CLASS_IDS[class_index]
        ):
            raise EscapeCompatibilityError(
                "selected class identity disagrees with the manifest"
            )
        row = evaluate_class(
            wall_class,
            owner_mark=owner_class.mark,
            corner_index=corner_index,
            class_index=class_index,
            transform=maps[corner_index],
            residual_centre=evidence.escape.centre,
            residual_u=residual_u,
            expected_frames=expected_frames,
            outer_side=source.outer_side,
            half=source.core_side / 2,
            deadline=deadline,
        )
        rows.append(row)
        if row.status == "partial":
            return EscapeCompatibilityResult(
                "partial",
                "incomplete",
                tuple(rows),
                time.perf_counter() - started,
                row.error,
            )
        if row.status == "incompatible":
            try:
                _deadline(deadline, "compatibility deadline reached before acceptance")
            except DeadlineError as error:
                return EscapeCompatibilityResult(
                    "partial",
                    "incomplete",
                    tuple(rows),
                    time.perf_counter() - started,
                    str(error),
                )
            return EscapeCompatibilityResult(
                "complete",
                "incompatible-class",
                tuple(rows),
                time.perf_counter() - started,
            )
    try:
        _deadline(deadline, "compatibility deadline reached before final refutation")
    except DeadlineError as error:
        return EscapeCompatibilityResult(
            "partial",
            "incomplete",
            tuple(rows),
            time.perf_counter() - started,
            str(error),
        )
    if len(rows) != len(EVALUATION_CORNER_INDICES) or any(
        row.status != "compatible" for row in rows
    ):
        raise EscapeCompatibilityError("all-compatible result lacks four witnesses")
    return EscapeCompatibilityResult(
        "complete",
        "all-selected-classes-compatible",
        tuple(rows),
        time.perf_counter() - started,
    )


def _point_record(point: Point) -> list[str]:
    return [str(point[0]), str(point[1])]


def _source_records(sources: tuple[DirectionSource, ...]) -> list[dict[str, object]]:
    return [
        {"folded_index": source.folded_index, "reflected": source.reflected}
        for source in sources
    ]


def _frame_record(row: FrameExtremum) -> dict[str, object]:
    frame = row.source
    maximum = row.maximum
    return {
        "frame_index": row.frame_index,
        "ray": _point_record(frame.frame.ray),
        "orientation_index": frame.frame.orientation_index,
        "quarter_turn": frame.frame.quarter_turn,
        "sources": _source_records(frame.frame.sources),
        "centre_dimension": frame.centre_dimension,
        "owner_u": _point_record(row.owner_u),
        "owner_v": _point_record(row.owner_v),
        "axes_checked": row.axes_checked,
        "maximum_slack": str(maximum.slack),
        "attaining_axis": maximum.label,
        "axis": _point_record(maximum.axis),
        "minimum_owner_projection": str(maximum.minimum_owner_projection),
        "owner_radius": str(maximum.owner_radius),
        "residual_radius": str(maximum.residual_radius),
        "canonical_owner_centre": _point_record(maximum.canonical_owner_centre),
        "owner_centre": _point_record(maximum.owner_centre),
    }


def _class_record(row: ClassCompatibility) -> dict[str, object]:
    witness = row.positive_witness
    return {
        "corner": CORNERS[row.corner_index],
        "corner_index": row.corner_index,
        "class_index": row.class_index,
        "class_id": CLASS_IDS[row.class_index],
        "corner_map": row.corner_map.name,
        "status": row.status,
        "expected_frames": row.expected_frames,
        "checked_frames": len(row.frame_extrema),
        "allowed_frames": len(row.frame_extrema),
        "empty_frames": 0,
        "observed_maximum_slack": None
        if row.observed_maximum_slack is None
        else str(row.observed_maximum_slack),
        "global_maximum_slack": None
        if row.global_maximum_slack is None
        else str(row.global_maximum_slack),
        "positive_witness": None
        if witness is None
        else {
            "frame_index": witness.frame_index,
            "slack": str(witness.maximum.slack),
            "owner_centre": _point_record(witness.maximum.owner_centre),
            "replay": "exact class membership, container, mark, and polygon SAT passed",
        },
        "frame_extrema": [_frame_record(frame) for frame in row.frame_extrema],
        "error": row.error,
    }


def result_document(
    result: EscapeCompatibilityResult,
    *,
    source: FrozenInput,
    wall: WallInput,
    evidence: SelectedCoverEvidence,
    implementation_revision: str,
    process_seconds: float,
) -> dict[str, object]:
    """Serialize one bounded saved-escape compatibility result."""

    class_rows = [_class_record(row) for row in result.classes]
    return {
        "schema": "wall-owner-escape-compatibility/v1",
        "status": result.status,
        "outcome": result.outcome,
        "claim_limit": (
            "saved exp149 B-core versus one individual snapped B-owner core per "
            "selected class; no joint owners, unit parents, tuple exclusion, or global bound"
        ),
        "sources": {
            "implementation": {
                "git_commit": implementation_revision,
                "module": "packing/devtools/wall_owner_escape_compatibility.py",
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
            "selected": {
                "path": evidence.source_path,
                "git_commit": evidence.git_commit,
                "git_blob": evidence.git_blob,
                "implementation_revision": evidence.implementation_revision,
            },
        },
        "settings": {
            "outer_side": str(source.outer_side),
            "core_side": str(source.core_side),
            "half_core": str(source.core_side / 2),
            "candidate": list(SELECTED_TUPLE),
            "selected_classes": [CLASS_IDS[index] for index in SELECTED_TUPLE],
            "corner_order": [CORNERS[index] for index in EVALUATION_CORNER_INDICES],
            "residual_orientation_index": evidence.escape.orientation_index,
            "residual_orientation_label": evidence.escape.orientation_label,
            "residual_centre": _point_record(evidence.escape.centre),
            "expected_frames_per_class": EXPECTED_FRAMES_PER_CLASS,
            "signed_axes_per_frame": EXPECTED_AXES_PER_FRAME,
            "boundary_policy": "strictly positive separation; zero slack is contact",
            "candidate_limit": 1,
        },
        "classes": class_rows,
        "summary": {
            "checked_classes": len(result.classes),
            "expected_classes": len(EVALUATION_CORNER_INDICES),
            "checked_frames": sum(len(row.frame_extrema) for row in result.classes),
            "expected_frames_if_exhaustive": EXPECTED_FRAMES_PER_CLASS
            * len(EVALUATION_CORNER_INDICES),
            "compatible_classes": sum(row.status == "compatible" for row in result.classes),
            "incompatible_classes": sum(row.status == "incompatible" for row in result.classes),
            "first_incompatible_corner": next(
                (
                    CORNERS[row.corner_index]
                    for row in result.classes
                    if row.status == "incompatible"
                ),
                None,
            ),
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
    parser.add_argument("--deadline-seconds", type=float, default=90)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    process_started = time.perf_counter()
    output: Path | None = None
    document: dict[str, object]
    try:
        repository, revision = validate_own_revision(args.expect_git_revision)
        inputs = (args.endpoint_receipt, args.wall_receipt, args.selected_receipt)
        output = validate_output_path(args.output, repository, inputs)
        source = load_frozen_input(args.endpoint_receipt, args.expect_endpoint_blob)
        wall = load_wall_input(
            args.wall_receipt,
            args.expect_wall_blob,
            expected_source=args.expect_wall_source,
        )
        evidence = load_selected_cover_evidence(
            args.selected_receipt,
            args.expect_selected_blob,
            expected_source=args.expect_selected_source,
            source=source,
            wall=wall,
        )
        result = run_escape_compatibility(
            source,
            wall,
            evidence,
            deadline_seconds=args.deadline_seconds,
        )
        document = result_document(
            result,
            source=source,
            wall=wall,
            evidence=evidence,
            implementation_revision=revision,
            process_seconds=time.perf_counter() - process_started,
        )
        atomic_write_json(output, document)
    except (
        ContainmentError,
        DeadlineError,
        EscapeCompatibilityError,
        SelectedCoverError,
        OSError,
        json.JSONDecodeError,
    ) as error:
        document = {
            "schema": "wall-owner-escape-compatibility/v1",
            "status": "invalid",
            "outcome": "invalid",
            "process_seconds": time.perf_counter() - process_started,
            "error": str(error),
        }
        if output is not None:
            atomic_write_json(output, document)
    print(json.dumps(document, indent=1), flush=True)
    return 0 if document.get("status") == "complete" else 2


if __name__ == "__main__":
    raise SystemExit(main())
