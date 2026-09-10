#!/usr/bin/env python3
"""Exact derived-domain adapter for unit-parent owner compatibility.

This module is a source candidate. It constructs and replays only necessary
unit-parent centre restrictions. It does not load target receipts or run a scientific
target.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass
from fractions import Fraction
from typing import Literal

from devtools.owner_footprints import (
    CORE_SIDE,
    HALF_CORE,
    OUTER_SIDE,
    DirectionSource,
    OwnerClass,
    OwnerDirectionManifest,
    Point,
    Polygon,
    convex_hull,
    convex_polygon_intersection,
    convex_polygons_strictly_disjoint,
    owner_branch_manifest,
    point_in_closed_convex_polygon,
)
from devtools.wall_owner_containment import AffineMap
from devtools.wall_owner_escape_compatibility import (
    AxisExtremum,
    FrameExtremum,
    transform_owner_frame,
)
from devtools.wall_owner_footprints import (
    OwnerFrameFootprint,
    RetainedOwnerFrame,
    centre_set_dimension,
    closed_centre_set,
    retained_owner_frames,
    support_rectangle,
    validate_owner_manifest,
)

GLOBAL_TANGENT_BOUND = Fraction(207107, 90000000)
GLOBAL_SELECTION_RULE = "nearest retained direction before owner routing"
GLOBAL_SOURCE_CONTRACTS = (
    "packing/cases/n11_five_dot_cover/unit-parent-centre-contract.md",
    (
        "packing/campaign/series/series-000-smoke-and-calibration/results/agenda-032/"
        "proofs/fixed-cover-transfer-review.md"
    ),
)
SIGNED_AXIS_LABELS = (
    "+owner-u",
    "-owner-u",
    "+owner-v",
    "-owner-v",
    "+residual-u",
    "-residual-u",
    "+residual-v",
    "-residual-v",
)

Clock = Callable[[], float]


class ParentCompatibilityError(ValueError):
    """An exact input, provenance, domain, or replay guard refused the adapter."""


class ParentCompatibilityDeadlineError(ParentCompatibilityError):
    """The shared compatibility deadline expired."""


@dataclass(frozen=True, slots=True)
class ParentCentreRule:
    """The admitted global nearest-frame unit-parent rule."""

    mode: Literal["global-D"] = "global-D"
    outer_side: Fraction = OUTER_SIDE
    core_side: Fraction = CORE_SIDE
    tangent_bound: Fraction = GLOBAL_TANGENT_BOUND
    selection_rule: str = GLOBAL_SELECTION_RULE
    source_contracts: tuple[str, ...] = GLOBAL_SOURCE_CONTRACTS


GLOBAL_PARENT_RULE = ParentCentreRule()


@dataclass(frozen=True, slots=True)
class DerivedOwnerFrame:
    """One bound exp146 frame and its freshly restricted derived geometry."""

    original: OwnerFrameFootprint
    restricted: OwnerFrameFootprint
    extent: Fraction
    parent_box: Polygon


@dataclass(frozen=True, slots=True)
class ParentClassCompatibility:
    """An individual witness, exhaustive negative, impossibility, or unresolved row."""

    status: Literal["compatible", "incompatible", "impossible", "unresolved"]
    expected_frames: int
    derived_frames: tuple[DerivedOwnerFrame, ...]
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
class ResidualParentCheck:
    """A separate necessary parent-box disposition for one residual core centre."""

    status: Literal["inside-parent-box", "outside-parent-box"]
    centre: Point
    ray: Point
    sources: tuple[DirectionSource, ...]
    extent: Fraction
    parent_box: Polygon


def _fraction(value: object, label: str) -> Fraction:
    if type(value) is not Fraction:
        raise ParentCompatibilityError(f"{label} must be an exact Fraction")
    return value


def _point(value: object, label: str) -> Point:
    if not isinstance(value, tuple) or len(value) != 2:
        raise ParentCompatibilityError(f"{label} must be a two-coordinate tuple")
    return _fraction(value[0], f"{label}.x"), _fraction(value[1], f"{label}.y")


def _dot(left: Point, right: Point) -> Fraction:
    return left[0] * right[0] + left[1] * right[1]


def _turn(point: Point) -> Point:
    return -point[1], point[0]


def _negate(point: Point) -> Point:
    return -point[0], -point[1]


def _subtract(left: Point, right: Point) -> Point:
    return left[0] - right[0], left[1] - right[1]


def _require_unit_ray(ray: object) -> Point:
    checked = _point(ray, "ray")
    if _dot(checked, checked) != 1:
        raise ParentCompatibilityError("ray must be an exact nonzero unit vector")
    return checked


def _require_time(deadline: float, clock: Clock, message: str) -> None:
    if clock() >= deadline:
        raise ParentCompatibilityDeadlineError(message)


def validate_global_rule(rule: ParentCentreRule) -> None:
    """Reject local cells, arbitrary mismatch bounds, and changed frozen scale."""

    for label, value in (
        ("outer_side", rule.outer_side),
        ("core_side", rule.core_side),
        ("tangent_bound", rule.tangent_bound),
    ):
        _fraction(value, label)
    if rule != GLOBAL_PARENT_RULE:
        raise ParentCompatibilityError(
            "parent rule must equal the admitted global-D rule; local or arbitrary "
            "bounds are unsupported"
        )


def angular_extent_lower(ray: object, tangent_bound: object) -> Fraction:
    """Return the exact rational angular lower bound `(S-T*d)/(2+d*d)`."""

    checked = _require_unit_ray(ray)
    d = _fraction(tangent_bound, "tangent_bound")
    if d < 0 or d >= 1:
        raise ParentCompatibilityError("tangent_bound must satisfy 0 <= d < 1")
    s = abs(checked[0]) + abs(checked[1])
    t = abs(abs(checked[0]) - abs(checked[1]))
    return (s - t * d) / (2 + d * d)


def unit_parent_extent_lower(
    ray: object,
    tangent_bound: object,
    *,
    half: object = HALF_CORE,
) -> Fraction:
    """Return `max(h*S, 1/2, (S-T*d)/(2+d*d))` exactly."""

    checked = _require_unit_ray(ray)
    checked_half = _fraction(half, "half")
    if checked_half <= 0:
        raise ParentCompatibilityError("half must be positive")
    s = abs(checked[0]) + abs(checked[1])
    return max(
        checked_half * s,
        Fraction(1, 2),
        angular_extent_lower(checked, tangent_bound),
    )


def closed_parent_box(outer_side: object, extent: object) -> Polygon:
    """Represent a closed square as a polygon, singleton, or exact empty set."""

    q = _fraction(outer_side, "outer_side")
    e = _fraction(extent, "extent")
    if q <= 0 or e < 0:
        raise ParentCompatibilityError("outer_side must be positive and extent nonnegative")
    high = q - e
    if e > high:
        return ()
    if e == high:
        return ((e, e),)
    return ((e, e), (high, e), (high, high), (e, high))


def intersect_parent_box(centre_set: Polygon, parent_box: Polygon) -> Polygon:
    """Intersect a closed centre set with a square, singleton, or empty parent box."""

    if not centre_set or not parent_box:
        return ()
    if len(parent_box) == 1:
        return parent_box if point_in_closed_convex_polygon(parent_box[0], centre_set) else ()
    return convex_hull(convex_polygon_intersection(centre_set, parent_box))


def _validate_original_frame(
    frame: OwnerFrameFootprint,
    *,
    owner_mark: Point,
    rule: ParentCentreRule,
) -> Polygon:
    """Rebuild `Z_B` and reject stale geometry or support fields."""

    ray = _require_unit_ray(frame.frame.ray)
    rebuilt = closed_centre_set(
        owner_mark,
        ray,
        outer_side=rule.outer_side,
        half=rule.core_side / 2,
    )
    dimension = centre_set_dimension(rebuilt)
    if frame.centre_set != rebuilt or frame.centre_dimension != dimension:
        raise ParentCompatibilityError("bound frame differs from reconstructed original Z_B")
    if dimension == -1:
        if (
            frame.disposition != "empty"
            or frame.support_r is not None
            or frame.support_jr is not None
            or frame.common_rectangle is not None
        ):
            raise ParentCompatibilityError("empty original frame has stale derived fields")
        return rebuilt
    rectangle, support_r, support_jr = support_rectangle(
        rebuilt,
        ray,
        half=rule.core_side / 2,
    )
    if (
        frame.disposition != "allowed"
        or frame.support_r != support_r
        or frame.support_jr != support_jr
        or frame.common_rectangle != rectangle
    ):
        raise ParentCompatibilityError("original frame has stale support or rectangle fields")
    return rebuilt


def restrict_owner_centres(
    frame: OwnerFrameFootprint,
    *,
    owner_mark: object,
    rule: ParentCentreRule = GLOBAL_PARENT_RULE,
) -> DerivedOwnerFrame:
    """Rebuild `Z_B`, intersect the closed parent box, and recompute every support."""

    validate_global_rule(rule)
    mark = _point(owner_mark, "owner_mark")
    original = _validate_original_frame(frame, owner_mark=mark, rule=rule)
    ray = frame.frame.ray
    extent = unit_parent_extent_lower(
        ray,
        rule.tangent_bound,
        half=rule.core_side / 2,
    )
    parent_box = closed_parent_box(rule.outer_side, extent)
    restricted = intersect_parent_box(original, parent_box)
    dimension = centre_set_dimension(restricted)
    if dimension == -1:
        derived = OwnerFrameFootprint(frame.frame, (), -1, None, None, None, "empty")
    else:
        rectangle, support_r, support_jr = support_rectangle(
            restricted,
            ray,
            half=rule.core_side / 2,
        )
        if not point_in_closed_convex_polygon(mark, rectangle):
            raise ParentCompatibilityError("derived common rectangle lost the owner mark")
        derived = OwnerFrameFootprint(
            frame.frame,
            restricted,
            dimension,
            support_r,
            support_jr,
            rectangle,
            "allowed",
        )
    return DerivedOwnerFrame(frame, derived, extent, parent_box)


def bound_expected_owner_frames(
    owner_class: OwnerClass,
    manifest: OwnerDirectionManifest,
) -> tuple[RetainedOwnerFrame, ...]:
    """Reconstruct one complete signed-frame source manifest from the frozen net."""

    branch = owner_branch_manifest(manifest)
    validate_owner_manifest(manifest, branch)
    by_id = {item.class_id: item for item in branch.classes}
    if by_id.get(owner_class.class_id) != owner_class:
        raise ParentCompatibilityError("owner class differs from the frozen branch")
    return retained_owner_frames(owner_class, manifest)


def validate_bound_frames(
    frames: tuple[OwnerFrameFootprint, ...],
    expected: tuple[RetainedOwnerFrame, ...],
) -> None:
    """Bind exact ordered rays, selectors, and full folded/reflection source tuples."""

    if not expected or len(frames) != len(expected):
        raise ParentCompatibilityError("frame manifest is missing or has extra frames")
    if len(set(expected)) != len(expected):
        raise ParentCompatibilityError("expected frame manifest contains a duplicate")
    for index, (frame, expected_frame) in enumerate(zip(frames, expected, strict=True)):
        if frame.frame != expected_frame:
            raise ParentCompatibilityError(
                f"frame {index} ray, selector, orientation, or source provenance differs"
            )


def _axis_rows(
    owner_u: Point,
    owner_v: Point,
    residual_u: Point,
) -> tuple[tuple[str, Point], ...]:
    residual_v = _turn(residual_u)
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


def parent_frame_extremum(
    frame: OwnerFrameFootprint,
    *,
    frame_index: int,
    transform: AffineMap,
    residual_centre: object,
    residual_u: object,
    half: object,
    deadline: float,
    clock: Clock = time.perf_counter,
) -> FrameExtremum:
    """Maximize exact slack over all eight signed SAT axes of one derived frame."""

    if frame.disposition != "allowed" or not frame.centre_set:
        raise ParentCompatibilityError("extremum requires one nonempty derived frame")
    centre = _point(residual_centre, "residual_centre")
    residual_ray = _require_unit_ray(residual_u)
    checked_half = _fraction(half, "half")
    if checked_half <= 0:
        raise ParentCompatibilityError("half must be positive")
    transformed = transform_owner_frame(frame, transform)
    rows: list[AxisExtremum] = []
    for label, axis in _axis_rows(
        transformed.owner_u,
        transformed.owner_v,
        residual_ray,
    ):
        _require_time(deadline, clock, "parent compatibility deadline reached within a frame")
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
        owner_radius = checked_half * (
            abs(_dot(axis, transformed.owner_u)) + abs(_dot(axis, transformed.owner_v))
        )
        residual_v = _turn(residual_ray)
        residual_radius = checked_half * (
            abs(_dot(axis, residual_ray)) + abs(_dot(axis, residual_v))
        )
        rows.append(
            AxisExtremum(
                label,
                axis,
                minimum,
                owner_radius,
                residual_radius,
                _dot(axis, centre) - minimum - owner_radius - residual_radius,
                canonical_centre,
                owner_centre,
            )
        )
    if tuple(row.label for row in rows) != SIGNED_AXIS_LABELS:
        raise ParentCompatibilityError("signed SAT axis enumeration changed")
    return FrameExtremum(
        frame_index,
        frame,
        transformed.owner_u,
        transformed.owner_v,
        max(rows, key=lambda row: row.slack),
        len(rows),
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


def literal_frame_signed_slacks(
    frame: OwnerFrameFootprint,
    *,
    transform: AffineMap,
    residual_centre: object,
    residual_u: object,
    half: object,
) -> tuple[tuple[str, Fraction], ...]:
    """Replay each signed gap from literal vertices of both closed squares."""

    if frame.disposition != "allowed" or not frame.centre_set:
        raise ParentCompatibilityError("literal replay requires a nonempty derived frame")
    centre = _point(residual_centre, "residual_centre")
    residual_ray = _require_unit_ray(residual_u)
    checked_half = _fraction(half, "half")
    if checked_half <= 0:
        raise ParentCompatibilityError("half must be positive")
    transformed = transform_owner_frame(frame, transform)
    residual = _square(centre, residual_ray, _turn(residual_ray), checked_half)
    replayed: list[tuple[str, Fraction]] = []
    for label, axis in _axis_rows(
        transformed.owner_u,
        transformed.owner_v,
        residual_ray,
    ):
        residual_minimum = min(_dot(axis, point) for point in residual)
        gaps = []
        for owner_centre in transformed.centre_set:
            owner = _square(
                owner_centre,
                transformed.owner_u,
                transformed.owner_v,
                checked_half,
            )
            gaps.append(residual_minimum - max(_dot(axis, point) for point in owner))
        replayed.append((label, max(gaps)))
    if tuple(label for label, _ in replayed) != SIGNED_AXIS_LABELS:
        raise ParentCompatibilityError("literal replay omitted a signed SAT axis")
    return tuple(replayed)


def replay_positive_parent_witness(
    row: FrameExtremum,
    *,
    original: OwnerFrameFootprint,
    owner_mark: object,
    transform: AffineMap,
    residual_centre: object,
    residual_u: object,
    rule: ParentCentreRule = GLOBAL_PARENT_RULE,
) -> None:
    """Rebuild the derived domain and replay one individual positive core witness."""

    if row.maximum.slack <= 0:
        raise ParentCompatibilityError("positive replay received nonpositive slack")
    derived = restrict_owner_centres(original, owner_mark=owner_mark, rule=rule)
    if derived.restricted != row.source:
        raise ParentCompatibilityError("positive replay did not reconstruct the derived domain")
    canonical = row.maximum.canonical_owner_centre
    if not point_in_closed_convex_polygon(canonical, derived.restricted.centre_set):
        raise ParentCompatibilityError("positive witness leaves its derived centre domain")
    mark = _point(owner_mark, "owner_mark")
    ray = original.frame.ray
    displacement = _subtract(canonical, mark)
    half = rule.core_side / 2
    if not (
        0 <= _dot(displacement, ray) <= half and 0 <= _dot(displacement, _turn(ray)) <= half
    ):
        raise ParentCompatibilityError("positive witness leaves the owner displacement box")
    transformed = transform_owner_frame(derived.restricted, transform)
    if (
        row.owner_u != transformed.owner_u
        or row.owner_v != transformed.owner_v
        or row.maximum.owner_centre != transform.point(canonical)
    ):
        raise ParentCompatibilityError("positive witness has inconsistent physical transport")
    owner = _square(
        row.maximum.owner_centre,
        transformed.owner_u,
        transformed.owner_v,
        half,
    )
    residual_ray = _require_unit_ray(residual_u)
    residual = _square(
        _point(residual_centre, "residual_centre"),
        residual_ray,
        _turn(residual_ray),
        half,
    )
    if not point_in_closed_convex_polygon(transform.point(mark), owner):
        raise ParentCompatibilityError("positive witness owner core lost the selected mark")
    if any(
        not (0 <= coordinate <= rule.outer_side) for vertex in owner for coordinate in vertex
    ):
        raise ParentCompatibilityError("positive witness owner core leaves the container")
    if not convex_polygons_strictly_disjoint(owner, residual):
        raise ParentCompatibilityError("positive witness fails literal square SAT")
    slacks = literal_frame_signed_slacks(
        derived.restricted,
        transform=transform,
        residual_centre=residual_centre,
        residual_u=residual_u,
        half=half,
    )
    if max(value for _, value in slacks) != row.maximum.slack:
        raise ParentCompatibilityError("positive literal replay disagrees with the extremum")


def replay_parent_universal(
    result: ParentClassCompatibility,
    *,
    owner_mark: object,
    transform: AffineMap,
    residual_centre: object,
    residual_u: object,
    rule: ParentCentreRule,
    deadline: float,
    clock: Clock = time.perf_counter,
) -> None:
    """Rebuild every disposition and replay an exhaustive nonpositive class maximum."""

    if result.status != "incompatible" or len(result.derived_frames) != result.expected_frames:
        raise ParentCompatibilityError("universal replay requires one exhausted class")
    rebuilt_frames: list[DerivedOwnerFrame] = []
    nonempty_indices: set[int] = set()
    for index, derived in enumerate(result.derived_frames):
        _require_time(deadline, clock, "deadline reached during parent universal replay")
        rebuilt = restrict_owner_centres(
            derived.original,
            owner_mark=owner_mark,
            rule=rule,
        )
        if rebuilt != derived:
            raise ParentCompatibilityError(
                "universal replay did not reconstruct a derived frame"
            )
        rebuilt_frames.append(rebuilt)
        if rebuilt.restricted.disposition != "empty":
            nonempty_indices.add(index)

    extremum_indices = tuple(row.frame_index for row in result.frame_extrema)
    if len(set(extremum_indices)) != len(extremum_indices):
        raise ParentCompatibilityError("universal extremum indices contain a duplicate")
    if set(extremum_indices) != nonempty_indices:
        raise ParentCompatibilityError(
            "universal extremum indices differ from the nonempty derived frames"
        )
    extrema = {row.frame_index: row for row in result.frame_extrema}
    replayed: list[Fraction] = []
    for index, rebuilt in enumerate(rebuilt_frames):
        if rebuilt.restricted.disposition == "empty":
            continue
        row = extrema[index]
        reconstructed = parent_frame_extremum(
            rebuilt.restricted,
            frame_index=index,
            transform=transform,
            residual_centre=residual_centre,
            residual_u=residual_u,
            half=rule.core_side / 2,
            deadline=deadline,
            clock=clock,
        )
        if row != reconstructed:
            raise ParentCompatibilityError(
                "universal extremum differs from independently reconstructed evidence"
            )
        slacks = literal_frame_signed_slacks(
            rebuilt.restricted,
            transform=transform,
            residual_centre=residual_centre,
            residual_u=residual_u,
            half=rule.core_side / 2,
        )
        maximum = max(value for _, value in slacks)
        if maximum != row.maximum.slack or maximum > 0:
            raise ParentCompatibilityError("universal literal replay disagrees with slack")
        replayed.append(maximum)
    _require_time(deadline, clock, "deadline reached after final parent universal replay")
    if not replayed or max(replayed) != result.global_maximum_slack:
        raise ParentCompatibilityError("universal class maximum fails final replay")


def evaluate_parent_class(
    frames: tuple[OwnerFrameFootprint, ...],
    expected_frames: tuple[RetainedOwnerFrame, ...],
    *,
    owner_mark: object,
    transform: AffineMap,
    residual_centre: object,
    residual_u: object,
    rule: ParentCentreRule = GLOBAL_PARENT_RULE,
    deadline: float,
    clock: Clock = time.perf_counter,
) -> ParentClassCompatibility:
    """Evaluate a complete manifest; positive status claims only one feasible core."""

    derived_rows: list[DerivedOwnerFrame] = []
    extrema: list[FrameExtremum] = []
    try:
        validate_global_rule(rule)
        validate_bound_frames(frames, expected_frames)
        for frame in frames:
            _require_time(deadline, clock, "deadline reached while deriving parent domains")
            derived_rows.append(restrict_owner_centres(frame, owner_mark=owner_mark, rule=rule))
        _require_time(deadline, clock, "deadline reached after parent-domain derivation")
        nonempty = tuple(
            (index, row)
            for index, row in enumerate(derived_rows)
            if row.restricted.disposition == "allowed"
        )
        if not nonempty:
            _require_time(deadline, clock, "deadline reached before all-empty disposition")
            return ParentClassCompatibility(
                "impossible",
                len(expected_frames),
                tuple(derived_rows),
                (),
                None,
                None,
            )
        for index, derived in nonempty:
            row = parent_frame_extremum(
                derived.restricted,
                frame_index=index,
                transform=transform,
                residual_centre=residual_centre,
                residual_u=residual_u,
                half=rule.core_side / 2,
                deadline=deadline,
                clock=clock,
            )
            extrema.append(row)
            if row.maximum.slack > 0:
                replay_positive_parent_witness(
                    row,
                    original=derived.original,
                    owner_mark=owner_mark,
                    transform=transform,
                    residual_centre=residual_centre,
                    residual_u=residual_u,
                    rule=rule,
                )
                _require_time(deadline, clock, "deadline reached after positive parent replay")
                return ParentClassCompatibility(
                    "compatible",
                    len(expected_frames),
                    tuple(derived_rows),
                    tuple(extrema),
                    max(item.maximum.slack for item in extrema),
                    None,
                )
        maximum = max(row.maximum.slack for row in extrema)
        candidate = ParentClassCompatibility(
            "incompatible",
            len(expected_frames),
            tuple(derived_rows),
            tuple(extrema),
            maximum,
            maximum,
        )
        replay_parent_universal(
            candidate,
            owner_mark=owner_mark,
            transform=transform,
            residual_centre=residual_centre,
            residual_u=residual_u,
            rule=rule,
            deadline=deadline,
            clock=clock,
        )
        _require_time(deadline, clock, "deadline reached after universal acceptance replay")
    except (ParentCompatibilityDeadlineError, ParentCompatibilityError) as error:
        observed = max(
            (row.maximum.slack for row in extrema),
            default=None,
        )
        return ParentClassCompatibility(
            "unresolved",
            len(expected_frames),
            tuple(derived_rows),
            tuple(extrema),
            observed,
            None,
            str(error),
        )
    else:
        return candidate


def check_residual_parent_centre(
    centre: object,
    ray: object,
    sources: tuple[DirectionSource, ...],
    expected_sources: tuple[DirectionSource, ...],
    *,
    rule: ParentCentreRule = GLOBAL_PARENT_RULE,
) -> ResidualParentCheck:
    """Check a residual parent box without adding an owner mark or displacement box."""

    validate_global_rule(rule)
    checked_centre = _point(centre, "residual_centre")
    checked_ray = _require_unit_ray(ray)
    if not expected_sources or sources != expected_sources:
        raise ParentCompatibilityError("residual source provenance is incomplete or changed")
    extent = unit_parent_extent_lower(
        checked_ray,
        rule.tangent_bound,
        half=rule.core_side / 2,
    )
    box = closed_parent_box(rule.outer_side, extent)
    inside = bool(box) and point_in_closed_convex_polygon(checked_centre, box)
    return ResidualParentCheck(
        "inside-parent-box" if inside else "outside-parent-box",
        checked_centre,
        checked_ray,
        sources,
        extent,
        box,
    )
