#!/usr/bin/env python3
"""Exact BC318 containment transfer from retained five-dot evidence.

The adapter validates already published inputs and evaluates exactly 128 logical
component slots.  It does not construct wall footprints or run a covering search.
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
from itertools import pairwise, product
from pathlib import Path
from typing import Literal, cast

from cases.n11_five_dot_cover.independent_union import (
    FrozenInput,
    load_frozen_input,
)
from devtools.owner_footprints import (
    ANGLE_LIMIT,
    CORE_SIDE,
    DIRECTION_STEPS,
    HALF_CORE,
    OUTER_SIDE,
    DirectionSource,
    OwnerDirectionManifest,
    Point,
    Polygon,
    endpoint_footprint,
    full_owner_direction_manifest,
    owner_branch_manifest,
    polygon_area_twice,
)
from devtools.wall_owner_footprints import (
    RetainedOwnerFrame,
    centre_set_dimension,
    retained_owner_frames,
    support_rectangle,
    validate_owner_manifest,
)

EXPECTED_CLASSES = 16
EXPECTED_CORNERS = 4
EXPECTED_FAMILIES = 2
EXPECTED_LOGICAL_SLOTS = 128
EXPECTED_ORIENTATIONS = 361
EXPECTED_SIGNED_RAYS = 1444
EXPECTED_FOLDED_DIRECTIONS = 181
RAW_TUPLE_UNIVERSE = EXPECTED_CLASSES**EXPECTED_CORNERS
RETAINED_ENDPOINT_BLOB = "cc66f06ddd3f7cc52d8a06d30a3920ba8e992c19"
CLASS_IDS = tuple(
    f"bottom-left:{mark}:j{sector}" for mark in ("m1", "m2") for sector in range(8)
)
CORNERS = ("BL", "BR", "TL", "TR")


class ContainmentError(ValueError):
    """A source, geometry, counting, or execution guard refused the adapter."""


class ContainmentDeadlineError(ContainmentError):
    """The declared adapter deadline expired."""


@dataclass(frozen=True, slots=True)
class WallClass:
    class_id: str
    old_endpoint: Polygon
    disposition: Literal["possible", "impossible"]
    wall_footprint: Polygon | None


@dataclass(frozen=True, slots=True)
class WallInput:
    source_path: str
    git_commit: str
    git_blob: str
    constructor_revision: str
    classes: tuple[WallClass, ...]


@dataclass(frozen=True, slots=True)
class ContainmentResult:
    contained: bool
    failure_vertex: Point | None = None
    failure_edge: tuple[Point, Point] | None = None
    failure_cross: Fraction | None = None


@dataclass(frozen=True, slots=True)
class TupleCounts:
    impossible: int
    covered: int
    unresolved: int
    family_products: tuple[int, int]
    overlap: int
    covered_baselines: int
    new_covered: int
    first_new_tuple: tuple[int, int, int, int] | None
    first_new_family: int | None


@dataclass(frozen=True, slots=True)
class AffineMap:
    name: str
    xx: int
    xy: int
    yx: int
    yy: int
    tx: Fraction
    ty: Fraction
    target_family: int
    corner_permutation: tuple[int, int, int, int]

    @property
    def determinant(self) -> int:
        return self.xx * self.yy - self.xy * self.yx

    def linear(self, point: Point) -> Point:
        x, y = point
        return self.xx * x + self.xy * y, self.yx * x + self.yy * y

    def point(self, point: Point) -> Point:
        x, y = self.linear(point)
        return x + self.tx, y + self.ty


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ("git", *args), cwd=root, check=False, capture_output=True, text=True
    )
    if result.returncode != 0:
        raise ContainmentError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout.strip()


def _mapping(value: object, label: str) -> dict[str, object]:
    if type(value) is not dict:
        raise ContainmentError(f"{label} must be an object")
    return cast(dict[str, object], value)


def _sequence(value: object, label: str) -> list[object]:
    if type(value) is not list:
        raise ContainmentError(f"{label} must be an array")
    return cast(list[object], value)


def _keys(record: dict[str, object], expected: set[str], label: str) -> None:
    if set(record) != expected:
        raise ContainmentError(f"{label} has missing or unexpected fields")


def _integer(value: object, label: str) -> int:
    if type(value) is not int:
        raise ContainmentError(f"{label} must be an integer")
    return cast(int, value)


def _fraction(value: object, label: str) -> Fraction:
    if not isinstance(value, (str, int)) or isinstance(value, bool):
        raise ContainmentError(f"{label} must be an exact rational")
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as error:
        raise ContainmentError(f"{label} is not an exact rational") from error


def _point(value: object, label: str) -> Point:
    raw = _sequence(value, label)
    if len(raw) != 2:
        raise ContainmentError(f"{label} must have two coordinates")
    return _fraction(raw[0], f"{label}.x"), _fraction(raw[1], f"{label}.y")


def _cross(left: Point, right: Point) -> Fraction:
    return left[0] * right[1] - left[1] * right[0]


def _subtract(left: Point, right: Point) -> Point:
    return left[0] - right[0], left[1] - right[1]


def normalise_convex_polygon(polygon: Polygon) -> Polygon:
    """Normalize cyclic start and winding while refusing malformed convex input."""

    if len(polygon) < 3 or len(set(polygon)) != len(polygon):
        raise ContainmentError("polygon must have at least three distinct vertices")
    area = polygon_area_twice(polygon)
    if area == 0:
        raise ContainmentError("polygon must have positive area")
    ordered = polygon if area > 0 else tuple(reversed(polygon))
    edges = tuple(pairwise((*ordered, ordered[0])))
    turns = tuple(
        _cross(_subtract(second, first), _subtract(third, second))
        for (first, second), (_, third) in pairwise((*edges, edges[0]))
    )
    if any(turn < 0 for turn in turns) or not any(turn > 0 for turn in turns):
        raise ContainmentError("polygon must be a convex boundary, not a hull request")
    if any(
        _cross(_subtract(end, start), _subtract(vertex, start)) < 0
        for start, end in edges
        for vertex in ordered
    ):
        raise ContainmentError("polygon must lie in every directed edge's closed half-plane")
    start = min(range(len(ordered)), key=ordered.__getitem__)
    return ordered[start:] + ordered[:start]


def _polygon(value: object, label: str, *, optional: bool = False) -> Polygon | None:
    if value is None and optional:
        return None
    raw = _sequence(value, label)
    polygon = tuple(_point(item, f"{label}[{index}]") for index, item in enumerate(raw))
    return normalise_convex_polygon(polygon)


def exact_containment(container: Polygon, contained: Polygon) -> ContainmentResult:
    """Test `contained` inside `container` by exact closed half-planes."""

    wall = normalise_convex_polygon(container)
    old = normalise_convex_polygon(contained)
    for vertex in old:
        for edge in pairwise((*wall, wall[0])):
            cross = _cross(_subtract(edge[1], edge[0]), _subtract(vertex, edge[0]))
            if cross < 0:
                return ContainmentResult(
                    contained=False,
                    failure_vertex=vertex,
                    failure_edge=edge,
                    failure_cross=cross,
                )
    return ContainmentResult(contained=True)


def _point_record(point: Point) -> list[str]:
    return [str(point[0]), str(point[1])]


def _polygon_record(polygon: Polygon) -> list[list[str]]:
    return [_point_record(point) for point in polygon]


def _source_records(sources: tuple[DirectionSource, ...]) -> list[dict[str, object]]:
    return [
        {"folded_index": source.folded_index, "reflected": source.reflected}
        for source in sources
    ]


def bind_clean_git_blob(
    path: Path, expected_blob: str, *, label: str
) -> tuple[Path, str, str, str]:
    """Bind one tracked working file to its exact Git blob."""

    if len(expected_blob) != 40 or any(
        char not in "0123456789abcdef" for char in expected_blob
    ):
        raise ContainmentError(f"expected {label} blob must be 40 lowercase hex digits")
    root = Path(_git(Path.cwd(), "rev-parse", "--show-toplevel")).resolve()
    resolved = path.resolve()
    try:
        relative = resolved.relative_to(root).as_posix()
    except ValueError as error:
        raise ContainmentError(f"{label} is outside the Git repository") from error
    _git(root, "ls-files", "--error-unmatch", "--", relative)
    if _git(root, "status", "--porcelain", "--", relative):
        raise ContainmentError(f"{label} has modified or staged bytes")
    blob = _git(root, "hash-object", "--", relative)
    if blob != expected_blob:
        raise ContainmentError(f"{label} blob {blob} does not match expected {expected_blob}")
    return root, relative, _git(root, "rev-parse", "HEAD"), blob


def validate_own_revision(expected: str) -> tuple[Path, str]:
    """Bind the adapter and all target inputs to one clean published revision."""

    if len(expected) != 40 or any(char not in "0123456789abcdef" for char in expected):
        raise ContainmentError(
            "expected implementation revision must be 40 lowercase hex digits"
        )
    root = Path(_git(Path.cwd(), "rev-parse", "--show-toplevel")).resolve()
    head = _git(root, "rev-parse", "HEAD")
    if head != expected:
        raise ContainmentError("current Git revision differs from the frozen implementation")
    if _git(root, "status", "--porcelain"):
        raise ContainmentError("target worktree must be clean at the frozen implementation")
    for relative in (
        "packing/devtools/owner_footprints.py",
        "packing/devtools/wall_owner_footprints.py",
        "packing/devtools/wall_owner_containment.py",
        "packing/cases/n11_five_dot_cover/independent_union.py",
    ):
        _git(root, "ls-files", "--error-unmatch", "--", relative)
    return root, head


def _read_bound_json(
    path: Path, expected_blob: str, *, label: str
) -> tuple[dict[str, object], str, str, str]:
    _, relative, commit, blob = bind_clean_git_blob(path, expected_blob, label=label)
    try:
        document = _mapping(json.loads(path.read_text(encoding="utf-8")), label)
    except (OSError, json.JSONDecodeError) as error:
        raise ContainmentError(f"could not read {label}: {error}") from error
    return document, relative, commit, blob


def validate_certificate_receipt(
    path: Path,
    expected_blob: str,
    *,
    kind: Literal["replay", "coverage"],
) -> dict[str, object]:
    """Bind and validate one adopted exp144/exp145 certificate receipt."""

    document, relative, commit, blob = _read_bound_json(
        path, expected_blob, label=f"{kind} receipt"
    )
    source = _mapping(document.get("source"), f"{kind} source")
    if source.get("git_blob") != RETAINED_ENDPOINT_BLOB:
        raise ContainmentError(f"{kind} receipt does not bind the retained exp143 blob")
    if kind == "replay":
        summary = _mapping(document.get("summary"), "replay summary")
        if (
            document.get("schema") != "owner-footprint-exact-replay/v1"
            or document.get("status") != "complete"
            or summary.get("minimum_covered_mass") != "1000001/1000000"
            or summary.get("normalised_total_mass") != "5"
            or summary.get("conditional_threshold") != "7"
            or summary.get("normalised_mass_below_threshold") is not True
        ):
            raise ContainmentError("replay receipt lacks the completed retained evidence")
    else:
        settings = _mapping(document.get("settings"), "coverage settings")
        summary = _mapping(document.get("summary"), "coverage summary")
        if (
            document.get("schema") != "independent-five-dot-union/v1"
            or document.get("status") != "complete"
            or document.get("outcome") != "covered"
            or settings.get("outer_side") != str(OUTER_SIDE)
            or settings.get("core_side") != str(CORE_SIDE)
            or settings.get("angle_limit") != str(ANGLE_LIMIT)
            or settings.get("direction_steps") != DIRECTION_STEPS
            or settings.get("direction_count") != EXPECTED_ORIENTATIONS
            or settings.get("owner_footprints") != 4
            or settings.get("dots") != 5
            or summary.get("checked_directions") != EXPECTED_ORIENTATIONS
            or summary.get("expected_directions") != EXPECTED_ORIENTATIONS
            or summary.get("all_covered") is not True
        ):
            raise ContainmentError("coverage receipt lacks complete frozen-net coverage")
    return {"path": relative, "git_commit": commit, "git_blob": blob}


def validate_frame_record(
    raw_value: object,
    expected: object,
    *,
    label: str,
) -> Literal["allowed", "empty"]:
    if not isinstance(expected, RetainedOwnerFrame):
        raise ContainmentError("internal expected-frame type is invalid")
    raw = _mapping(raw_value, label)
    _keys(
        raw,
        {
            "ray",
            "orientation_index",
            "quarter_turn",
            "sources",
            "centre_dimension",
            "centre_set",
            "disposition",
            "support_r",
            "support_jr",
            "common_rectangle",
        },
        label,
    )
    ray = _point(raw["ray"], f"{label}.ray")
    sources = _sequence(raw["sources"], f"{label}.sources")
    for index, item in enumerate(sources):
        _keys(
            _mapping(item, f"{label}.sources[{index}]"),
            {"folded_index", "reflected"},
            f"{label}.sources[{index}]",
        )
    if (
        ray != expected.ray
        or _integer(raw["orientation_index"], f"{label}.orientation_index")
        != expected.orientation_index
        or _integer(raw["quarter_turn"], f"{label}.quarter_turn") != expected.quarter_turn
        or sources != _source_records(expected.sources)
    ):
        raise ContainmentError(f"{label} disagrees with generated frame provenance")
    disposition = raw["disposition"]
    dimension = _integer(raw["centre_dimension"], f"{label}.centre_dimension")
    if disposition == "empty":
        if (
            dimension != -1
            or raw["centre_set"] != []
            or raw["support_r"] is not None
            or raw["support_jr"] is not None
            or raw["common_rectangle"] is not None
        ):
            raise ContainmentError(f"{label} has inconsistent empty-frame data")
        return "empty"
    if disposition != "allowed":
        raise ContainmentError(f"{label} has invalid frame disposition")
    centre_raw = _sequence(raw["centre_set"], f"{label}.centre_set")
    centre_set = tuple(
        _point(item, f"{label}.centre_set[{index}]") for index, item in enumerate(centre_raw)
    )
    if dimension not in (0, 1, 2) or centre_set_dimension(centre_set) != dimension:
        raise ContainmentError(f"{label} has inconsistent centre-set dimension")
    support_r = tuple(
        _fraction(item, f"{label}.support_r")
        for item in _sequence(raw["support_r"], f"{label}.support_r")
    )
    support_jr = tuple(
        _fraction(item, f"{label}.support_jr")
        for item in _sequence(raw["support_jr"], f"{label}.support_jr")
    )
    if len(support_r) != 2 or len(support_jr) != 2:
        raise ContainmentError(f"{label} support intervals must have two endpoints")
    rectangle, expected_r, expected_jr = support_rectangle(centre_set, ray, half=HALF_CORE)
    stored_rectangle = _polygon(raw["common_rectangle"], f"{label}.common_rectangle")
    if (
        support_r != expected_r
        or support_jr != expected_jr
        or stored_rectangle != normalise_convex_polygon(rectangle)
    ):
        raise ContainmentError(f"{label} support receipt is inconsistent")
    return "allowed"


def load_wall_input(path: Path, expected_blob: str, *, expected_source: str) -> WallInput:
    """Load a complete wall receipt and validate all frozen frame provenance."""

    if len(expected_source) != 40 or any(
        char not in "0123456789abcdef" for char in expected_source
    ):
        raise ContainmentError("expected wall source must be 40 lowercase hex digits")
    document, relative, commit, blob = _read_bound_json(
        path, expected_blob, label="wall receipt"
    )
    _keys(
        document,
        {
            "schema",
            "status",
            "evidence_tier",
            "source",
            "settings",
            "classes",
            "summary",
            "error",
        },
        "wall receipt",
    )
    if document["schema"] != "wall-owner-footprints/v1" or document["status"] != "complete":
        raise ContainmentError("wall receipt must be complete wall-owner-footprints/v1")
    if document["error"] is not None:
        raise ContainmentError("complete wall receipt may not retain an error")
    source = _mapping(document["source"], "wall source")
    _keys(source, {"git_commit", "owner_module"}, "wall source")
    if source != {
        "git_commit": expected_source,
        "owner_module": "packing/devtools/owner_footprints.py",
    }:
        raise ContainmentError("wall receipt source differs from the frozen constructor")
    settings = _mapping(document["settings"], "wall settings")
    expected_settings: dict[str, object] = {
        "outer_side": str(OUTER_SIDE),
        "core_side": str(CORE_SIDE),
        "half_core": str(HALF_CORE),
        "angle_limit": str(ANGLE_LIMIT),
        "direction_steps": DIRECTION_STEPS,
        "orientation_count": EXPECTED_ORIENTATIONS,
        "signed_ray_count": EXPECTED_SIGNED_RAYS,
        "class_count": EXPECTED_CLASSES,
        "boundary_policy": "retain nonempty point and segment centre sets",
    }
    if settings != expected_settings:
        raise ContainmentError("wall receipt changes frozen settings or boundary policy")
    manifest = full_owner_direction_manifest()
    branch = owner_branch_manifest(manifest)
    validate_owner_manifest(manifest, branch)
    raw_classes = _sequence(document["classes"], "wall classes")
    if len(raw_classes) != EXPECTED_CLASSES:
        raise ContainmentError("wall receipt must contain all sixteen classes")
    classes: list[WallClass] = []
    possible = impossible = enlarged = equal = 0
    for index, (raw_value, expected_class) in enumerate(
        zip(raw_classes, branch.classes, strict=True)
    ):
        label = f"wall classes[{index}]"
        raw = _mapping(raw_value, label)
        _keys(
            raw,
            {
                "class_id",
                "mark",
                "sector",
                "old_endpoint",
                "disposition",
                "frames",
                "nonempty_frame_count",
                "empty_frame_count",
                "point_frame_count",
                "segment_frame_count",
                "wall_footprint",
                "old_endpoint_contained",
                "proper_inclusion",
            },
            label,
        )
        if (
            raw["class_id"] != expected_class.class_id
            or raw["class_id"] != CLASS_IDS[index]
            or _point(raw["mark"], f"{label}.mark") != expected_class.mark
            or _integer(raw["sector"], f"{label}.sector") != expected_class.sector
        ):
            raise ContainmentError(f"{label} changes class identity or order")
        expected_frames = retained_owner_frames(expected_class, manifest)
        frames = _sequence(raw["frames"], f"{label}.frames")
        if len(frames) != len(expected_frames):
            raise ContainmentError(f"{label} has a partial frame list")
        frame_dispositions = tuple(
            validate_frame_record(item, expected_frame, label=f"{label}.frames[{frame_index}]")
            for frame_index, (item, expected_frame) in enumerate(
                zip(frames, expected_frames, strict=True)
            )
        )
        dimensions = tuple(
            _integer(_mapping(item, "frame")["centre_dimension"], "frame dimension")
            for item in frames
        )
        counts = (
            sum(value >= 0 for value in dimensions),
            dimensions.count(-1),
            dimensions.count(0),
            dimensions.count(1),
        )
        serialized_counts = tuple(
            _integer(raw[name], f"{label}.{name}")
            for name in (
                "nonempty_frame_count",
                "empty_frame_count",
                "point_frame_count",
                "segment_frame_count",
            )
        )
        if counts != serialized_counts:
            raise ContainmentError(f"{label} frame summary is inconsistent")
        old = cast(
            Polygon,
            _polygon(raw["old_endpoint"], f"{label}.old_endpoint"),
        )
        expected_old = normalise_convex_polygon(
            endpoint_footprint(
                expected_class.mark,
                expected_class.sector,
                manifest.directions,
                half=HALF_CORE,
            )
        )
        if old != expected_old:
            raise ContainmentError(f"{label} changes the certified old endpoint")
        disposition = raw["disposition"]
        wall = _polygon(raw["wall_footprint"], f"{label}.wall_footprint", optional=True)
        if disposition == "possible":
            if wall is None or not any(value == "allowed" for value in frame_dispositions):
                raise ContainmentError(f"{label} possible disposition lacks a wall polygon")
            relation = exact_containment(wall, old)
            proper = polygon_area_twice(wall) > polygon_area_twice(old)
            if (
                not relation.contained
                or raw["old_endpoint_contained"] is not True
                or raw["proper_inclusion"] is not proper
            ):
                raise ContainmentError(f"{label} fails its same-class nesting receipt")
            possible += 1
            enlarged += int(proper)
            equal += int(not proper)
            parsed_disposition: Literal["possible", "impossible"] = "possible"
        elif disposition == "impossible":
            if (
                wall is not None
                or any(value != "empty" for value in frame_dispositions)
                or raw["old_endpoint_contained"] is not False
                or raw["proper_inclusion"] is not None
            ):
                raise ContainmentError(
                    f"{label} lacks complete all-empty impossibility evidence"
                )
            impossible += 1
            parsed_disposition = "impossible"
        else:
            raise ContainmentError(f"{label} has invalid class disposition")
        classes.append(WallClass(expected_class.class_id, old, parsed_disposition, wall))
    summary = _mapping(document["summary"], "wall summary")
    seconds = summary.get("wall_seconds")
    if (
        not isinstance(seconds, (int, float))
        or isinstance(seconds, bool)
        or not math.isfinite(seconds)
        or seconds < 0
    ):
        raise ContainmentError("wall summary has invalid elapsed time")
    expected_summary = {
        "completed_classes": EXPECTED_CLASSES,
        "expected_classes": EXPECTED_CLASSES,
        "possible_classes": possible,
        "impossible_classes": impossible,
        "enlarged_classes": enlarged,
        "equal_classes": equal,
        "wall_seconds": seconds,
    }
    if summary != expected_summary:
        raise ContainmentError("wall summary disagrees with complete class evidence")
    return WallInput(relative, commit, blob, expected_source, tuple(classes))


def _corner_maps() -> tuple[AffineMap, AffineMap, AffineMap, AffineMap]:
    q = OUTER_SIDE
    return (
        AffineMap("I", 1, 0, 0, 1, Fraction(0), Fraction(0), 0, (0, 1, 2, 3)),
        AffineMap("H", -1, 0, 0, 1, q, Fraction(0), 0, (1, 0, 3, 2)),
        AffineMap("V", 1, 0, 0, -1, Fraction(0), q, 0, (2, 3, 0, 1)),
        AffineMap("R", -1, 0, 0, -1, q, q, 0, (3, 2, 1, 0)),
    )


def _certificate_maps() -> tuple[AffineMap, AffineMap, AffineMap, AffineMap]:
    q = OUTER_SIDE
    return (
        _corner_maps()[0],
        _corner_maps()[1],
        AffineMap("S", 0, 1, 1, 0, Fraction(0), Fraction(0), 1, (0, 2, 1, 3)),
        AffineMap("S_after_H", 0, 1, -1, 0, Fraction(0), q, 1, (2, 0, 3, 1)),
    )


def transform_polygon(polygon: Polygon, transform: AffineMap) -> Polygon:
    return normalise_convex_polygon(tuple(transform.point(point) for point in polygon))


def _swap_polygon(polygon: Polygon) -> Polygon:
    return normalise_convex_polygon(tuple((y, x) for x, y in polygon))


def occupied_families(source: FrozenInput) -> tuple[tuple[Polygon, ...], tuple[Polygon, ...]]:
    """Build the two four-component families from the retained base patch."""

    if len(source.footprints) != EXPECTED_CORNERS:
        raise ContainmentError("retained source must contain four endpoint components")
    base = normalise_convex_polygon(source.footprints[0])
    family_zero = tuple(transform_polygon(base, transform) for transform in _corner_maps())
    if tuple(map(normalise_convex_polygon, source.footprints)) != family_zero:
        raise ContainmentError("retained endpoint components disagree with corner transport")
    swapped = _swap_polygon(base)
    family_one = tuple(transform_polygon(swapped, transform) for transform in _corner_maps())
    return family_zero, family_one


def _canonical_axis(point: Point) -> Point:
    x, y = point
    matches = tuple(
        candidate
        for candidate in ((x, y), (-y, x), (-x, -y), (y, -x))
        if candidate[0] > 0 and candidate[1] >= 0
    )
    if len(matches) != 1:
        raise ContainmentError("could not resolve transformed orientation modulo quarter turns")
    return matches[0]


def orientation_transport(
    transform: AffineMap, manifest: OwnerDirectionManifest
) -> list[dict[str, object]]:
    """Resolve every transported ordered frame against the full manifest."""

    by_axis = {(item.direction.ux, item.direction.uy): item for item in manifest.orientations}
    rows: list[dict[str, object]] = []
    targets: list[int] = []
    for item in manifest.orientations:
        ray = (item.direction.ux, item.direction.uy)
        ordered = (
            transform.linear(ray)
            if transform.determinant == 1
            else transform.linear((-ray[1], ray[0]))
        )
        target = by_axis.get(_canonical_axis(ordered))
        if target is None:
            raise ContainmentError(f"{transform.name} orientation has no manifest target")
        targets.append(target.index)
        rows.append(
            {
                "source_index": item.index,
                "target_index": target.index,
                "target_sources": _source_records(target.sources),
            }
        )
    if len(rows) != EXPECTED_ORIENTATIONS or set(targets) != set(range(EXPECTED_ORIENTATIONS)):
        raise ContainmentError(f"{transform.name} orientation transport is not a bijection")
    return rows


def _compose(first: AffineMap, second: AffineMap, point: Point) -> Point:
    return first.point(second.point(point))


def validate_transport(
    source: FrozenInput,
    wall: WallInput,
    manifest: OwnerDirectionManifest,
) -> dict[str, object]:
    """Validate whole-certificate, wall-class, and ordered-frame transport."""

    families = occupied_families(source)
    if families[0][0] != wall.classes[0].old_endpoint:
        raise ContainmentError("retained base E differs from the wall receipt's old endpoint")
    if families[1][0] != wall.classes[15].old_endpoint:
        raise ContainmentError("retained S(E) differs from the wall receipt's old endpoint")
    expected_dots = (
        (Fraction(73, 75), Fraction(187, 90)),
        (Fraction(793, 450), Fraction(43, 15)),
        (Fraction(48, 25), Fraction(48, 25)),
        (Fraction(187, 90), Fraction(73, 75)),
        (Fraction(43, 15), Fraction(793, 450)),
    )
    if source.dots != expected_dots:
        raise ContainmentError("retained source changes the five certified dots")
    d0 = frozenset(source.dots)
    h = _certificate_maps()[1]
    d1 = frozenset(h.point(point) for point in source.dots)
    transport_rows: list[dict[str, object]] = []
    for transform in _certificate_maps():
        expected_dot_set = d0 if transform.name in ("I", "S") else d1
        if frozenset(transform.point(point) for point in source.dots) != expected_dot_set:
            raise ContainmentError(f"{transform.name} does not transport the complete dot set")
        for corner, polygon in enumerate(families[0]):
            target_corner = transform.corner_permutation[corner]
            if (
                transform_polygon(polygon, transform)
                != families[transform.target_family][target_corner]
            ):
                raise ContainmentError(
                    f"{transform.name} does not transport the complete patch family"
                )
        orientation_rows = orientation_transport(transform, manifest)
        transport_rows.append(
            {
                "map": transform.name,
                "target_family": transform.target_family,
                "corner_permutation": [
                    CORNERS[index] for index in transform.corner_permutation
                ],
                "dot_pattern": "D0" if expected_dot_set == d0 else "D1",
                "orientation_bijection": orientation_rows,
            }
        )
    points = ((Fraction(1, 7), Fraction(2, 9)), (Fraction(3, 8), Fraction(5, 11)))
    identity, horizontal, vertical, _ = _corner_maps()
    swap = _certificate_maps()[2]
    for point in points:
        if (
            _compose(horizontal, horizontal, point) != identity.point(point)
            or _compose(swap, swap, point) != identity.point(point)
            or _compose(swap, _compose_map(horizontal, swap), point) != vertical.point(point)
        ):
            raise ContainmentError("container reflection identities failed")
    tau: list[int] = []
    for index, item in enumerate(wall.classes):
        target_index = (8 if index < 8 else 0) + (7 - index % 8)
        tau.append(target_index)
        target = wall.classes[target_index]
        if (
            item.disposition != target.disposition
            or _swap_polygon(item.old_endpoint) != target.old_endpoint
        ):
            raise ContainmentError("S-induced old-class permutation failed")
        if item.wall_footprint is not None and (
            target.wall_footprint is None
            or _swap_polygon(item.wall_footprint) != target.wall_footprint
        ):
            raise ContainmentError("S-induced wall-class permutation failed")
    return {
        "certificate_transports": transport_rows,
        "class_permutation_tau": tau,
        "same_class_nesting_relations": sum(
            item.disposition == "possible" for item in wall.classes
        ),
    }


def _compose_map(first: AffineMap, second: AffineMap) -> AffineMap:
    """Compose two maps for exact transport controls."""

    origin = first.point(second.point((Fraction(0), Fraction(0))))
    ex = first.point(second.point((Fraction(1), Fraction(0))))
    ey = first.point(second.point((Fraction(0), Fraction(1))))
    return AffineMap(
        f"{first.name}_after_{second.name}",
        int(ex[0] - origin[0]),
        int(ey[0] - origin[0]),
        int(ex[1] - origin[1]),
        int(ey[1] - origin[1]),
        origin[0],
        origin[1],
        first.target_family,
        (0, 1, 2, 3),
    )


def count_tuple_dispositions(
    possible: tuple[frozenset[int], ...],
    accepted: tuple[tuple[frozenset[int], ...], tuple[frozenset[int], ...]],
    *,
    universe_size: int,
    baselines: tuple[tuple[int, int, int, int], ...] = (),
) -> TupleCounts:
    """Count the exact union of two four-coordinate Cartesian products."""

    if len(possible) != EXPECTED_CORNERS:
        raise ContainmentError("tuple count requires four possible-coordinate rows")
    if universe_size < 1 or any(
        value < 0 or value >= universe_size for values in possible for value in values
    ):
        raise ContainmentError("possible labels leave the declared tuple universe")
    if len(accepted) != EXPECTED_FAMILIES or any(
        len(family) != EXPECTED_CORNERS for family in accepted
    ):
        raise ContainmentError("tuple count requires two complete four-coordinate families")
    if any(
        not accepted[family][corner] <= possible[corner]
        for family in range(EXPECTED_FAMILIES)
        for corner in range(EXPECTED_CORNERS)
    ):
        raise ContainmentError("an accepted row contains an impossible label")
    products = tuple(
        math.prod(len(accepted[family][corner]) for corner in range(EXPECTED_CORNERS))
        for family in range(EXPECTED_FAMILIES)
    )
    overlap = math.prod(
        len(accepted[0][corner] & accepted[1][corner]) for corner in range(EXPECTED_CORNERS)
    )
    covered = products[0] + products[1] - overlap
    possible_count = math.prod(len(values) for values in possible)
    impossible = universe_size**EXPECTED_CORNERS - possible_count
    unresolved = possible_count - covered
    baseline_set = set(baselines)
    covered_baselines = sum(
        tuple_ in baseline_set
        and any(
            all(
                tuple_[corner] in accepted[family][corner] for corner in range(EXPECTED_CORNERS)
            )
            for family in range(EXPECTED_FAMILIES)
        )
        and all(tuple_[corner] in possible[corner] for corner in range(EXPECTED_CORNERS))
        for tuple_ in baseline_set
    )
    first_new: tuple[int, int, int, int] | None = None
    first_family: int | None = None
    for raw_tuple in product(*(sorted(values) for values in possible)):
        tuple_ = cast(tuple[int, int, int, int], raw_tuple)
        if tuple_ in baseline_set:
            continue
        for family in range(EXPECTED_FAMILIES):
            if all(
                tuple_[corner] in accepted[family][corner] for corner in range(EXPECTED_CORNERS)
            ):
                first_new, first_family = tuple_, family
                break
        if first_new is not None:
            break
    return TupleCounts(
        impossible,
        covered,
        unresolved,
        cast(tuple[int, int], products),
        overlap,
        covered_baselines,
        covered - covered_baselines,
        first_new,
        first_family,
    )


def _rotate(point: Point) -> Point:
    return (
        Fraction(3, 5) * point[0] - Fraction(4, 5) * point[1],
        Fraction(4, 5) * point[0] + Fraction(3, 5) * point[1],
    )


def run_controls(manifest: OwnerDirectionManifest) -> list[str]:
    """Run the prospective target-blind containment, transport, and counting controls."""

    square = (
        (Fraction(0), Fraction(0)),
        (Fraction(3), Fraction(0)),
        (Fraction(3), Fraction(3)),
        (Fraction(0), Fraction(3)),
    )
    inner = (
        (Fraction(0), Fraction(0)),
        (Fraction(2), Fraction(0)),
        (Fraction(2), Fraction(2)),
        (Fraction(0), Fraction(2)),
    )
    translated = tuple((x + 2, y + 2) for x, y in inner)
    checks = (
        exact_containment(square, square).contained,
        exact_containment(square, inner).contained,
        exact_containment(square, tuple(reversed(inner))).contained,
        not exact_containment(inner, square).contained,
        not exact_containment(square, translated).contained,
        exact_containment(tuple(map(_rotate, square)), tuple(map(_rotate, inner))).contained,
        not exact_containment(
            tuple(map(_rotate, inner)), tuple(map(_rotate, square))
        ).contained,
    )
    if not all(checks):
        raise ContainmentError("containment direction, boundary, or oblique control failed")
    nonconvex = (
        (Fraction(0), Fraction(0)),
        (Fraction(2), Fraction(0)),
        (Fraction(1), Fraction(1)),
        (Fraction(2), Fraction(2)),
        (Fraction(0), Fraction(2)),
    )
    try:
        normalise_convex_polygon(nonconvex)
    except ContainmentError:
        pass
    else:
        raise ContainmentError("nonconvex control was silently replaced by a hull")
    swap = _certificate_maps()[2]
    ray = (Fraction(3, 5), Fraction(4, 5))
    correct = swap.linear((-ray[1], ray[0]))
    wrong = swap.linear(ray)
    if correct != (Fraction(3, 5), Fraction(-4, 5)) or correct == wrong:
        raise ContainmentError("oblique reflected ordered-frame control failed")
    if len(orientation_transport(swap, manifest)) != EXPECTED_ORIENTATIONS:
        raise ContainmentError("full-manifest transport control failed")
    toy_possible = (frozenset({0, 1, 2}),) * 4
    toy_accepted = (
        (frozenset({0, 1}),) * 4,
        (frozenset({1, 2}),) * 4,
    )
    toy = count_tuple_dispositions(toy_possible, toy_accepted, universe_size=4)
    if (toy.impossible, toy.covered, toy.unresolved, toy.family_products, toy.overlap) != (
        175,
        31,
        50,
        (16, 16),
        1,
    ):
        raise ContainmentError("Cartesian-product union control failed")
    return [
        "exact containment direction, boundary, reversal, translation, and oblique rotation",
        "malformed nonconvex polygon refusal",
        "ordered-frame reflection and full 361-orientation bijection",
        "four-coordinate Cartesian-product union counts 175/31/50",
    ]


def _relation_record(
    family: int,
    corner: int,
    class_index: int,
    result: ContainmentResult | None,
) -> dict[str, object]:
    if result is None:
        disposition = "impossible-class"
        witness = None
    elif result.contained:
        disposition = "contained"
        witness = None
    else:
        disposition = "not-contained"
        assert result.failure_vertex is not None
        assert result.failure_edge is not None
        assert result.failure_cross is not None
        witness = {
            "old_vertex": _point_record(result.failure_vertex),
            "wall_edge": [_point_record(point) for point in result.failure_edge],
            "cross": str(result.failure_cross),
        }
    return {
        "family": family,
        "corner": CORNERS[corner],
        "class_index": class_index,
        "class_id": CLASS_IDS[class_index],
        "disposition": disposition,
        "failure": witness,
    }


def evaluate_relations(
    source: FrozenInput, wall: WallInput, *, deadline: float
) -> tuple[list[dict[str, object]], int]:
    """Evaluate all 128 slots directly, skipping only proved impossible classes."""

    families = occupied_families(source)
    corner_maps = _corner_maps()
    rows: list[dict[str, object]] = []
    polygon_tests = 0
    for family in range(EXPECTED_FAMILIES):
        for corner in range(EXPECTED_CORNERS):
            for class_index, wall_class in enumerate(wall.classes):
                if time.perf_counter() >= deadline:
                    raise ContainmentDeadlineError(
                        "containment deadline reached before all 128 slots"
                    )
                if wall_class.disposition == "impossible":
                    rows.append(_relation_record(family, corner, class_index, None))
                    continue
                assert wall_class.wall_footprint is not None
                container = transform_polygon(wall_class.wall_footprint, corner_maps[corner])
                result = exact_containment(container, families[family][corner])
                polygon_tests += 1
                rows.append(_relation_record(family, corner, class_index, result))
    if len(rows) != EXPECTED_LOGICAL_SLOTS or polygon_tests > EXPECTED_LOGICAL_SLOTS:
        raise ContainmentError("relation driver did not execute exactly 128 logical slots")
    return rows, polygon_tests


def relation_sets(
    rows: list[dict[str, object]], wall: WallInput
) -> tuple[
    tuple[frozenset[int], ...],
    tuple[tuple[frozenset[int], ...], tuple[frozenset[int], ...]],
]:
    possible_row = frozenset(
        index for index, item in enumerate(wall.classes) if item.disposition == "possible"
    )
    possible = (possible_row,) * EXPECTED_CORNERS
    accepted_list: list[tuple[frozenset[int], ...]] = []
    for family in range(EXPECTED_FAMILIES):
        corner_sets: list[frozenset[int]] = []
        for corner in range(EXPECTED_CORNERS):
            selected = frozenset(
                cast(int, row["class_index"])
                for row in rows
                if row["family"] == family
                and row["corner"] == CORNERS[corner]
                and row["disposition"] == "contained"
            )
            corner_sets.append(selected)
        accepted_list.append(tuple(corner_sets))
    accepted = cast(
        tuple[tuple[frozenset[int], ...], tuple[frozenset[int], ...]],
        tuple(accepted_list),
    )
    for family in range(EXPECTED_FAMILIES):
        if any(accepted[family][corner] != accepted[family][0] for corner in range(1, 4)):
            raise ContainmentError("corner transport rows disagree")
    for index in range(EXPECTED_CLASSES):
        tau = (8 if index < 8 else 0) + (7 - index % 8)
        if (index in accepted[0][0]) != (tau in accepted[1][0]):
            raise ContainmentError("S-induced containment rows disagree")
    return possible, accepted


def run_target(
    source: FrozenInput,
    wall: WallInput,
    *,
    implementation_revision: str,
    replay_source: dict[str, object],
    coverage_source: dict[str, object],
    deadline_seconds: float,
) -> dict[str, object]:
    """Validate transports and execute the frozen BC318 relation matrix."""

    if not math.isfinite(deadline_seconds) or deadline_seconds <= 0:
        raise ContainmentError("deadline must be finite and positive")
    started = time.perf_counter()
    deadline = started + deadline_seconds
    manifest = full_owner_direction_manifest()
    validate_owner_manifest(manifest, owner_branch_manifest(manifest))
    controls = run_controls(manifest)
    transports = validate_transport(source, wall, manifest)
    if time.perf_counter() >= deadline:
        raise ContainmentDeadlineError("containment deadline reached before relation slots")
    rows, polygon_tests = evaluate_relations(source, wall, deadline=deadline)
    possible, accepted = relation_sets(rows, wall)
    baselines = ((0, 0, 0, 0), (15, 15, 15, 15))
    counts = count_tuple_dispositions(
        possible, accepted, universe_size=EXPECTED_CLASSES, baselines=baselines
    )
    first_witness: dict[str, object] | None = None
    if counts.first_new_tuple is not None and counts.first_new_family is not None:
        first_witness = {
            "tuple": [CLASS_IDS[index] for index in counts.first_new_tuple],
            "family": counts.first_new_family,
            "relations": [
                {
                    "corner": CORNERS[corner],
                    "class_id": CLASS_IDS[counts.first_new_tuple[corner]],
                    "slot": (
                        counts.first_new_family * EXPECTED_CORNERS * EXPECTED_CLASSES
                        + corner * EXPECTED_CLASSES
                        + counts.first_new_tuple[corner]
                    ),
                    "disposition": "contained",
                }
                for corner in range(EXPECTED_CORNERS)
            ],
        }
    if time.perf_counter() >= deadline:
        raise ContainmentDeadlineError("containment deadline reached before completing receipt")
    return {
        "schema": "wall-owner-containment/v1",
        "status": "complete",
        "verdict": "accept-containment-expansion"
        if counts.new_covered
        else "refute-containment-expansion",
        "evidence_tier": (
            "exact finite containment transfer under retained certificate premises"
        ),
        "claim_limit": (
            "labelled sufficient conditions only; no exhaustiveness or global n11 claim"
        ),
        "sources": {
            "implementation": {
                "git_commit": implementation_revision,
                "module": "packing/devtools/wall_owner_containment.py",
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
            "exact_replay": replay_source,
            "completed_coverage": coverage_source,
        },
        "settings": {
            "outer_side": str(OUTER_SIDE),
            "core_side": str(CORE_SIDE),
            "half_core": str(HALF_CORE),
            "angle_limit": str(ANGLE_LIMIT),
            "direction_steps": DIRECTION_STEPS,
            "orientation_count": EXPECTED_ORIENTATIONS,
            "class_order": list(CLASS_IDS),
            "family_order": [0, 1],
            "corner_order": list(CORNERS),
            "logical_slot_order": "family, corner, class",
            "relation": "certified old component is a subset of the admitted wall footprint",
            "no_adaptive_retry": True,
        },
        "controls": controls,
        "transport": transports,
        "relations": rows,
        "masks": [
            [
                sum(1 << index for index in sorted(accepted[family][corner]))
                for corner in range(4)
            ]
            for family in range(2)
        ],
        "counts": {
            "raw_label_universe": RAW_TUPLE_UNIVERSE,
            "impossible": counts.impossible,
            "covered": counts.covered,
            "unresolved": counts.unresolved,
            "family_products": list(counts.family_products),
            "family_overlap": counts.overlap,
            "covered_baselines": counts.covered_baselines,
            "new_covered": counts.new_covered,
        },
        "first_new_tuple_witness": first_witness,
        "summary": {
            "logical_slots": len(rows),
            "polygon_containment_tests": polygon_tests,
            "impossible_class_skips": len(rows) - polygon_tests,
            "contained_relations": sum(row["disposition"] == "contained" for row in rows),
            "not_contained_relations": sum(
                row["disposition"] == "not-contained" for row in rows
            ),
            "unresolved_relations": 0,
            "wall_seconds": time.perf_counter() - started,
        },
        "error": None,
    }


def validate_output_path(output: Path, repository: Path, inputs: tuple[Path, ...]) -> Path:
    """Require one fresh JSON output outside source and test trees."""

    resolved = output.resolve()
    if any(resolved == path.resolve() for path in inputs):
        raise ContainmentError("output may not overwrite an input receipt")
    if resolved.exists() or resolved.suffix != ".json":
        raise ContainmentError("output must be a fresh JSON path")
    for relative in ("packing/devtools", "packing/tests", "packing/cases", "packing/src"):
        if resolved.is_relative_to(repository / relative):
            raise ContainmentError("output may not be created inside project code or tests")
    return resolved


def atomic_write_json(path: Path, document: dict[str, object]) -> None:
    """Publish one complete receipt atomically."""

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
    parser.add_argument("endpoint_receipt", type=Path)
    parser.add_argument("wall_receipt", type=Path)
    parser.add_argument("--replay-receipt", type=Path, required=True)
    parser.add_argument("--coverage-receipt", type=Path, required=True)
    parser.add_argument("--expect-endpoint-blob", required=True)
    parser.add_argument("--expect-wall-blob", required=True)
    parser.add_argument("--expect-wall-source", required=True)
    parser.add_argument("--expect-replay-blob", required=True)
    parser.add_argument("--expect-coverage-blob", required=True)
    parser.add_argument("--expect-git-revision", required=True)
    parser.add_argument("--deadline-seconds", type=float, default=60)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    started = time.perf_counter()
    output: Path | None = None
    try:
        repository = Path(_git(Path.cwd(), "rev-parse", "--show-toplevel")).resolve()
        inputs = (
            args.endpoint_receipt,
            args.wall_receipt,
            args.replay_receipt,
            args.coverage_receipt,
        )
        output = validate_output_path(args.output, repository, inputs)
        if args.expect_endpoint_blob != RETAINED_ENDPOINT_BLOB:
            raise ContainmentError("endpoint blob differs from the retained exp143 authority")  # noqa: TRY301
        _, revision = validate_own_revision(args.expect_git_revision)
        source = load_frozen_input(args.endpoint_receipt, args.expect_endpoint_blob)
        wall = load_wall_input(
            args.wall_receipt,
            args.expect_wall_blob,
            expected_source=args.expect_wall_source,
        )
        replay = validate_certificate_receipt(
            args.replay_receipt, args.expect_replay_blob, kind="replay"
        )
        coverage = validate_certificate_receipt(
            args.coverage_receipt, args.expect_coverage_blob, kind="coverage"
        )
        result = run_target(
            source,
            wall,
            implementation_revision=revision,
            replay_source=replay,
            coverage_source=coverage,
            deadline_seconds=args.deadline_seconds,
        )
        atomic_write_json(output, result)
    except ContainmentDeadlineError as error:
        result = {
            "schema": "wall-owner-containment/v1",
            "status": "partial",
            "verdict": "incomplete",
            "error": str(error),
            "wall_seconds": time.perf_counter() - started,
        }
        if output is not None:
            atomic_write_json(output, result)
    except (ContainmentError, OSError, json.JSONDecodeError) as error:
        result = {
            "schema": "wall-owner-containment/v1",
            "status": "invalid",
            "verdict": "invalid",
            "error": str(error),
            "wall_seconds": time.perf_counter() - started,
        }
        if output is not None:
            atomic_write_json(output, result)
    print(json.dumps(result, indent=1), flush=True)
    return 0 if result.get("status") == "complete" else 2


if __name__ == "__main__":
    raise SystemExit(main())
