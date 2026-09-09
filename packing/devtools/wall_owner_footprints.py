#!/usr/bin/env python3
"""Exact wall-aware common footprints for coarse corner-owner classes.

This module constructs geometry and receipts.  It does not run a covering experiment,
test target containments, or claim a packing bound.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import tempfile
import time
from dataclasses import dataclass
from fractions import Fraction
from functools import cmp_to_key
from pathlib import Path
from typing import Literal

from devtools.owner_footprints import (
    ANGLE_LIMIT,
    CORE_SIDE,
    DIRECTION_STEPS,
    HALF_CORE,
    OUTER_SIDE,
    DirectionSource,
    OwnerBranchManifest,
    OwnerClass,
    OwnerDirectionManifest,
    Point,
    Polygon,
    anchored_quarter,
    convex_hull,
    convex_polygon_contains_polygon,
    convex_polygon_intersection,
    endpoint_footprint,
    full_owner_direction_manifest,
    owner_branch_manifest,
    point_in_closed_convex_polygon,
    polygon_area_twice,
    sector_endpoint_rays,
    signed_axis_rays,
)

EXPECTED_ORIENTATIONS = 361
EXPECTED_SIGNED_RAYS = 1444
EXPECTED_CLASSES = 16
EXPECTED_FOLDED_DIRECTIONS = 181


class WallFootprintError(ValueError):
    """An input, geometry, or execution guard refused the construction."""


class WallFootprintDeadlineError(WallFootprintError):
    """The declared construction deadline expired."""


@dataclass(frozen=True, slots=True)
class RetainedOwnerFrame:
    """One signed owner frame with its unabridged net provenance."""

    ray: Point
    orientation_index: int
    quarter_turn: int
    sources: tuple[DirectionSource, ...]


@dataclass(frozen=True, slots=True)
class OwnerFrameFootprint:
    """The legal centres and common rectangle for one signed owner frame."""

    frame: RetainedOwnerFrame
    centre_set: Polygon
    centre_dimension: Literal[-1, 0, 1, 2]
    support_r: tuple[Fraction, Fraction] | None
    support_jr: tuple[Fraction, Fraction] | None
    common_rectangle: Polygon | None
    disposition: Literal["allowed", "empty"]


@dataclass(frozen=True, slots=True)
class WallOwnerFootprint:
    """One completed possible or impossible coarse owner class."""

    owner_class: OwnerClass
    frames: tuple[OwnerFrameFootprint, ...]
    old_endpoint: Polygon
    polygon: Polygon | None
    disposition: Literal["possible", "impossible"]
    proper_inclusion: bool | None


@dataclass(frozen=True, slots=True)
class WallOwnerManifest:
    """A complete, partial, or invalid ordered sixteen-class construction."""

    status: Literal["complete", "partial", "invalid"]
    classes: tuple[WallOwnerFootprint, ...]
    expected_classes: int
    source_revision: str
    wall_seconds: float
    error: str | None = None


def _subtract(left: Point, right: Point) -> Point:
    return left[0] - right[0], left[1] - right[1]


def _cross(left: Point, right: Point) -> Fraction:
    return left[0] * right[1] - left[1] * right[0]


def _dot(left: Point, right: Point) -> Fraction:
    return left[0] * right[0] + left[1] * right[1]


def _quarter_turn(ray: Point) -> Point:
    return -ray[1], ray[0]


def _signed_rotations(ray: Point) -> tuple[Point, Point, Point, Point]:
    turned = _quarter_turn(ray)
    return ray, turned, (-ray[0], -ray[1]), (ray[1], -ray[0])


def _ray_compare(left: RetainedOwnerFrame, right: RetainedOwnerFrame) -> int:
    cross = _cross(left.ray, right.ray)
    if cross > 0:
        return -1
    if cross < 0:
        return 1
    return (left.ray > right.ray) - (left.ray < right.ray)


def centre_set_dimension(polygon: Polygon) -> Literal[-1, 0, 1, 2]:
    """Classify a normalized closed convex set without dropping degeneracies."""

    normalized = convex_hull(polygon)
    if not normalized:
        return -1
    if len(normalized) == 1:
        return 0
    if len(normalized) == 2:
        return 1
    if polygon_area_twice(normalized) <= 0:
        raise WallFootprintError("closed centre polygon is not positive and counterclockwise")
    return 2


def validate_owner_manifest(
    manifest: OwnerDirectionManifest, branch: OwnerBranchManifest
) -> None:
    """Validate the complete frozen direction and sixteen-class manifests."""

    expected = full_owner_direction_manifest(
        angle_limit=ANGLE_LIMIT, direction_steps=DIRECTION_STEPS
    )
    if manifest != expected:
        raise WallFootprintError("owner direction manifest differs from the frozen generator")
    if (
        manifest.angle_limit != ANGLE_LIMIT
        or manifest.direction_steps != DIRECTION_STEPS
        or manifest.folded_count != EXPECTED_FOLDED_DIRECTIONS
        or manifest.full_count != EXPECTED_ORIENTATIONS
    ):
        raise WallFootprintError("owner direction manifest has wrong frozen cardinalities")
    if tuple(item.index for item in manifest.orientations) != tuple(
        range(EXPECTED_ORIENTATIONS)
    ):
        raise WallFootprintError("owner orientation indices are not complete and ordered")
    provenance: dict[Point, tuple[int, int, tuple[DirectionSource, ...]]] = {}
    for item in manifest.orientations:
        direction = item.direction
        if (
            direction.ux * direction.ux + direction.uy * direction.uy != 1
            or (direction.vx, direction.vy) != (-direction.uy, direction.ux)
            or not item.sources
            or len(set(item.sources)) != len(item.sources)
            or any(
                source.folded_index < 0 or source.folded_index >= manifest.folded_count
                for source in item.sources
            )
        ):
            raise WallFootprintError("owner orientation geometry or provenance is invalid")
        for selector, ray in enumerate(_signed_rotations((direction.ux, direction.uy))):
            if ray in provenance:
                raise WallFootprintError("canonical orientations share a signed ray")
            provenance[ray] = item.index, selector, item.sources
    if len(provenance) != EXPECTED_SIGNED_RAYS or set(provenance) != set(
        signed_axis_rays(manifest.directions)
    ):
        raise WallFootprintError("signed-ray manifest is incomplete or duplicated")
    expected_branch = owner_branch_manifest(manifest)
    if branch != expected_branch or len(branch.classes) != EXPECTED_CLASSES:
        raise WallFootprintError("owner class manifest differs from the frozen branch")
    if tuple(item.class_id for item in branch.classes) != tuple(
        f"bottom-left:{mark}:j{sector}" for mark in ("m1", "m2") for sector in range(8)
    ):
        raise WallFootprintError("owner class identifiers or order are invalid")


def retained_owner_frames(
    owner_class: OwnerClass, manifest: OwnerDirectionManifest
) -> tuple[RetainedOwnerFrame, ...]:
    """Return every exact signed frame in one closed owner sector."""

    first, last = sector_endpoint_rays(owner_class.sector, manifest.directions)
    by_ray: dict[Point, RetainedOwnerFrame] = {}
    for item in manifest.orientations:
        direction = item.direction
        for selector, ray in enumerate(_signed_rotations((direction.ux, direction.uy))):
            if ray in by_ray:
                raise WallFootprintError("duplicate signed ray would hide manifest provenance")
            by_ray[ray] = RetainedOwnerFrame(ray, item.index, selector, item.sources)
    all_rays = set(signed_axis_rays(manifest.directions))
    if set(by_ray) != all_rays:
        raise WallFootprintError("signed frame construction disagrees with source ray set")
    selected = {ray for ray in all_rays if _cross(first, ray) >= 0 and _cross(ray, last) >= 0}
    if not selected:
        raise WallFootprintError("owner class has no retained signed frames")
    frames = tuple(sorted((by_ray[ray] for ray in selected), key=cmp_to_key(_ray_compare)))
    if {frame.ray for frame in frames} != selected:
        raise WallFootprintError("owner sector selection lost a signed frame")
    return frames


def physical_container_centres(ray: Point, *, outer_side: Fraction, half: Fraction) -> Polygon:
    """Return the physical closed rectangle of contained owner centres."""

    if outer_side <= 0 or half <= 0 or _dot(ray, ray) != 1:
        raise WallFootprintError("container dimensions and owner ray must be valid")
    extent = half * (abs(ray[0]) + abs(ray[1]))
    low, high = extent, outer_side - extent
    if low >= high:
        raise WallFootprintError("owner has no full-dimensional contained-centre rectangle")
    return ((low, low), (high, low), (high, high), (low, high))


def closed_centre_set(
    mark: Point, ray: Point, *, outer_side: Fraction, half: Fraction
) -> Polygon:
    """Intersect the physical container rectangle with one owner displacement box."""

    container = physical_container_centres(ray, outer_side=outer_side, half=half)
    displacement = anchored_quarter(mark, ray, half=half)
    result = convex_hull(convex_polygon_intersection(container, displacement))
    centre_set_dimension(result)
    return result


def literal_support_interval(
    centre_set: Polygon, axis: Point, *, half: Fraction
) -> tuple[Fraction, Fraction]:
    """Return the intersection of owner support intervals from literal vertices."""

    if not centre_set or half <= 0 or _dot(axis, axis) != 1:
        raise WallFootprintError("support extrema require a nonempty centre set and unit axis")
    projections = tuple(_dot(axis, point) for point in centre_set)
    bounds = max(projections) - half, min(projections) + half
    if bounds[0] > bounds[1]:
        raise WallFootprintError("owner centre width exceeds one half-side on an owner axis")
    return bounds


def support_rectangle(
    centre_set: Polygon, ray: Point, *, half: Fraction
) -> tuple[Polygon, tuple[Fraction, Fraction], tuple[Fraction, Fraction]]:
    """Build the common owner rectangle and its exact support intervals."""

    turned = _quarter_turn(ray)
    support_r = literal_support_interval(centre_set, ray, half=half)
    support_jr = literal_support_interval(centre_set, turned, half=half)

    def world(first: Fraction, second: Fraction) -> Point:
        return (
            first * ray[0] + second * turned[0],
            first * ray[1] + second * turned[1],
        )

    rectangle = convex_hull(
        (
            world(support_r[0], support_jr[0]),
            world(support_r[1], support_jr[0]),
            world(support_r[1], support_jr[1]),
            world(support_r[0], support_jr[1]),
        )
    )
    if len(rectangle) < 3 or polygon_area_twice(rectangle) <= 0:
        raise WallFootprintError("common owner rectangle is not positive-area")
    return rectangle, support_r, support_jr


def combine_frame_footprints(
    owner_class: OwnerClass,
    frames: tuple[OwnerFrameFootprint, ...],
    old_endpoint: Polygon,
) -> WallOwnerFootprint:
    """Complete one class from already constructed frame dispositions."""

    if not frames:
        raise WallFootprintError("an empty retained-frame list is an instrument error")
    rectangles = tuple(
        frame.common_rectangle
        for frame in frames
        if frame.disposition == "allowed" and frame.common_rectangle is not None
    )
    if not rectangles:
        if any(frame.disposition != "empty" for frame in frames):
            raise WallFootprintError("frame disposition is inconsistent with its rectangle")
        return WallOwnerFootprint(owner_class, frames, old_endpoint, None, "impossible", None)
    result = rectangles[0]
    for rectangle in rectangles[1:]:
        result = convex_polygon_intersection(result, rectangle)
        if not result:
            raise WallFootprintError("nonempty owner frame rectangles have empty intersection")
    if (
        centre_set_dimension(result) != 2
        or polygon_area_twice(old_endpoint) <= 0
        or not convex_polygon_contains_polygon(result, old_endpoint)
        or not point_in_closed_convex_polygon(owner_class.mark, result)
    ):
        raise WallFootprintError("wall footprint lost positivity, nesting, or the owned mark")
    old_area_twice = polygon_area_twice(old_endpoint)
    new_area_twice = polygon_area_twice(result)
    if new_area_twice < old_area_twice:
        raise WallFootprintError("wall footprint has negative exact area gain")
    return WallOwnerFootprint(
        owner_class,
        frames,
        old_endpoint,
        result,
        "possible",
        new_area_twice > old_area_twice,
    )


def wall_owner_footprint(
    owner_class: OwnerClass,
    manifest: OwnerDirectionManifest,
    *,
    outer_side: Fraction = OUTER_SIDE,
    half: Fraction = HALF_CORE,
    deadline: float | None = None,
) -> WallOwnerFootprint:
    """Construct one complete wall-aware coarse-class footprint."""

    frame_records: list[OwnerFrameFootprint] = []
    for frame in retained_owner_frames(owner_class, manifest):
        if deadline is not None and time.perf_counter() >= deadline:
            raise WallFootprintDeadlineError("wall-footprint deadline reached within a class")
        centre_set = closed_centre_set(
            owner_class.mark, frame.ray, outer_side=outer_side, half=half
        )
        dimension = centre_set_dimension(centre_set)
        if dimension == -1:
            frame_records.append(OwnerFrameFootprint(frame, (), -1, None, None, None, "empty"))
            continue
        rectangle, support_r, support_jr = support_rectangle(centre_set, frame.ray, half=half)
        literal_r = tuple(_dot(frame.ray, point) for point in centre_set)
        turned = _quarter_turn(frame.ray)
        literal_jr = tuple(_dot(turned, point) for point in centre_set)
        if support_r != (max(literal_r) - half, min(literal_r) + half) or support_jr != (
            max(literal_jr) - half,
            min(literal_jr) + half,
        ):
            raise WallFootprintError("reported supports disagree with literal centre vertices")
        if not point_in_closed_convex_polygon(owner_class.mark, rectangle):
            raise WallFootprintError("owner frame rectangle does not contain the owned mark")
        frame_records.append(
            OwnerFrameFootprint(
                frame,
                centre_set,
                dimension,
                support_r,
                support_jr,
                rectangle,
                "allowed",
            )
        )
    old = endpoint_footprint(
        owner_class.mark,
        owner_class.sector,
        manifest.directions,
        half=half,
    )
    return combine_frame_footprints(owner_class, tuple(frame_records), old)


def build_wall_owner_manifest(
    *,
    source_revision: str,
    deadline_seconds: float,
    directions: OwnerDirectionManifest | None = None,
    branch: OwnerBranchManifest | None = None,
) -> WallOwnerManifest:
    """Build the ordered sixteen-class manifest with conservative partial states."""

    started = time.perf_counter()
    classes: list[WallOwnerFootprint] = []
    manifest = directions or full_owner_direction_manifest()
    owner_classes = branch or owner_branch_manifest(manifest)
    if not math.isfinite(deadline_seconds) or deadline_seconds <= 0:
        return WallOwnerManifest(
            "invalid",
            (),
            len(owner_classes.classes),
            source_revision,
            time.perf_counter() - started,
            "deadline must be finite and positive",
        )

    def require_time(deadline: float) -> None:
        if time.perf_counter() >= deadline:
            raise WallFootprintDeadlineError("wall-footprint deadline reached between classes")

    try:
        validate_owner_manifest(manifest, owner_classes)
        deadline = started + deadline_seconds
        for owner_class in owner_classes.classes:
            require_time(deadline)
            classes.append(wall_owner_footprint(owner_class, manifest, deadline=deadline))
    except WallFootprintDeadlineError as error:
        return WallOwnerManifest(
            "partial",
            tuple(classes),
            len(owner_classes.classes),
            source_revision,
            time.perf_counter() - started,
            str(error),
        )
    except (WallFootprintError, ValueError) as error:
        return WallOwnerManifest(
            "invalid",
            tuple(classes),
            len(owner_classes.classes),
            source_revision,
            time.perf_counter() - started,
            str(error),
        )
    return WallOwnerManifest(
        "complete",
        tuple(classes),
        len(owner_classes.classes),
        source_revision,
        time.perf_counter() - started,
    )


def _point_record(point: Point) -> list[str]:
    return [str(point[0]), str(point[1])]


def _polygon_record(polygon: Polygon | None) -> list[list[str]] | None:
    return None if polygon is None else [_point_record(point) for point in polygon]


def _frame_record(frame: OwnerFrameFootprint) -> dict[str, object]:
    return {
        "ray": _point_record(frame.frame.ray),
        "orientation_index": frame.frame.orientation_index,
        "quarter_turn": frame.frame.quarter_turn,
        "sources": [
            {"folded_index": source.folded_index, "reflected": source.reflected}
            for source in frame.frame.sources
        ],
        "centre_dimension": frame.centre_dimension,
        "centre_set": _polygon_record(frame.centre_set),
        "disposition": frame.disposition,
        "support_r": None
        if frame.support_r is None
        else [str(value) for value in frame.support_r],
        "support_jr": None
        if frame.support_jr is None
        else [str(value) for value in frame.support_jr],
        "common_rectangle": _polygon_record(frame.common_rectangle),
    }


def manifest_receipt(manifest: WallOwnerManifest) -> dict[str, object]:
    """Serialize a constructor result without adding a packing interpretation."""

    classes: list[dict[str, object]] = []
    for item in manifest.classes:
        dimensions = [frame.centre_dimension for frame in item.frames]
        classes.append(
            {
                "class_id": item.owner_class.class_id,
                "mark": _point_record(item.owner_class.mark),
                "sector": item.owner_class.sector,
                "old_endpoint": _polygon_record(item.old_endpoint),
                "disposition": item.disposition,
                "frames": [_frame_record(frame) for frame in item.frames],
                "nonempty_frame_count": sum(value >= 0 for value in dimensions),
                "empty_frame_count": dimensions.count(-1),
                "point_frame_count": dimensions.count(0),
                "segment_frame_count": dimensions.count(1),
                "wall_footprint": _polygon_record(item.polygon),
                "old_endpoint_contained": item.polygon is not None
                and convex_polygon_contains_polygon(item.polygon, item.old_endpoint),
                "proper_inclusion": item.proper_inclusion,
            }
        )
    return {
        "schema": "wall-owner-footprints/v1",
        "status": manifest.status,
        "evidence_tier": "exact geometry construction; no target cover or packing bound",
        "source": {
            "git_commit": manifest.source_revision,
            "owner_module": "packing/devtools/owner_footprints.py",
        },
        "settings": {
            "outer_side": str(OUTER_SIDE),
            "core_side": str(CORE_SIDE),
            "half_core": str(HALF_CORE),
            "angle_limit": str(ANGLE_LIMIT),
            "direction_steps": DIRECTION_STEPS,
            "orientation_count": EXPECTED_ORIENTATIONS,
            "signed_ray_count": EXPECTED_SIGNED_RAYS,
            "class_count": EXPECTED_CLASSES,
            "boundary_policy": "retain nonempty point and segment centre sets",
        },
        "classes": classes,
        "summary": {
            "completed_classes": len(classes),
            "expected_classes": manifest.expected_classes,
            "possible_classes": sum(row["disposition"] == "possible" for row in classes),
            "impossible_classes": sum(row["disposition"] == "impossible" for row in classes),
            "enlarged_classes": sum(row["proper_inclusion"] is True for row in classes),
            "equal_classes": sum(row["proper_inclusion"] is False for row in classes),
            "wall_seconds": manifest.wall_seconds,
        },
        "error": manifest.error,
    }


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ("git", *args), cwd=root, check=False, capture_output=True, text=True
    )
    if result.returncode != 0:
        raise WallFootprintError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout.strip()


def validate_source_revision(expected: str) -> tuple[Path, str]:
    """Bind the constructor to a clean tracked source at one full Git revision."""

    if len(expected) != 40 or any(char not in "0123456789abcdef" for char in expected):
        raise WallFootprintError("expected Git revision must be 40 lowercase hex digits")
    root = Path(_git(Path.cwd(), "rev-parse", "--show-toplevel")).resolve()
    head = _git(root, "rev-parse", "HEAD")
    if head != expected:
        raise WallFootprintError("current Git revision differs from the frozen source")
    if _git(root, "status", "--porcelain"):
        raise WallFootprintError("source worktree must be clean at the frozen revision")
    protected = (
        "packing/devtools/owner_footprints.py",
        "packing/devtools/wall_owner_footprints.py",
    )
    for relative in protected:
        _git(root, "ls-files", "--error-unmatch", "--", relative)
        if _git(root, "status", "--porcelain", "--", relative):
            raise WallFootprintError(f"source file is modified or staged: {relative}")
    return root, head


def validate_output_path(output: Path, repository: Path) -> Path:
    """Require a fresh JSON output outside code and test directories."""

    resolved = output.resolve()
    if resolved.exists() or resolved.suffix != ".json":
        raise WallFootprintError("output must be a fresh JSON path")
    for relative in ("packing/devtools", "packing/tests", "packing/cases", "packing/src"):
        if resolved.is_relative_to(repository / relative):
            raise WallFootprintError("output may not be created inside project code or tests")
    return resolved


def atomic_write_json(path: Path, document: dict[str, object]) -> None:
    """Write one receipt atomically."""

    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(document, stream, indent=1)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        Path(temporary).replace(path)
    except BaseException:
        Path(temporary).unlink(missing_ok=True)
        raise


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expect-git-revision", required=True)
    parser.add_argument("--deadline-seconds", type=float, default=300)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    started = time.perf_counter()
    output: Path | None = None
    try:
        if not math.isfinite(args.deadline_seconds) or args.deadline_seconds <= 0:
            raise WallFootprintError("deadline must be finite and positive")  # noqa: TRY301
        repository, revision = validate_source_revision(args.expect_git_revision)
        output = validate_output_path(args.output, repository)
        result = build_wall_owner_manifest(
            source_revision=revision, deadline_seconds=args.deadline_seconds
        )
        receipt = manifest_receipt(result)
        atomic_write_json(output, receipt)
    except (WallFootprintError, OSError) as error:
        receipt = {
            "schema": "wall-owner-footprints/v1",
            "status": "invalid",
            "evidence_tier": "exact geometry construction; no target cover or packing bound",
            "error": str(error),
            "wall_seconds": time.perf_counter() - started,
        }
        if output is not None:
            atomic_write_json(output, receipt)
    print(json.dumps(receipt, indent=1), flush=True)
    return 0 if receipt.get("status") == "complete" else 2


if __name__ == "__main__":
    raise SystemExit(main())
