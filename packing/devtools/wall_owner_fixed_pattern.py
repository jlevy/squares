"""Exact fixed-pattern witness bank and one-candidate discriminator.

This module consumes admitted wall footprints and the retained five-dot source.  It
uses nine fixed seed directions for reusable escape masks, then checks at most one
lexicographically selected tuple on the complete 361-direction manifest.
"""

from __future__ import annotations

import argparse
import json
import math
import time
from dataclasses import dataclass, replace
from fractions import Fraction
from itertools import pairwise, product
from pathlib import Path
from typing import Literal, cast

from cases.n11_five_dot_cover.independent_union import (
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
from devtools.multi_owner_domains import reflect_to_four_corners, vertical_decompose
from devtools.owner_footprints import (
    ANGLE_LIMIT,
    CORE_SIDE,
    DIRECTION_STEPS,
    OUTER_SIDE,
    Point,
    Polygon,
    full_owner_direction_manifest,
    point_in_closed_convex_polygon,
    point_in_open_convex_polygon,
)
from devtools.wall_owner_containment import (
    CLASS_IDS,
    CORNERS,
    EXPECTED_CLASSES,
    EXPECTED_CORNERS,
    EXPECTED_ORIENTATIONS,
    RAW_TUPLE_UNIVERSE,
    ContainmentError,
    WallInput,
    atomic_write_json,
    bind_clean_git_blob,
    load_wall_input,
    normalise_convex_polygon,
    validate_output_path,
    validate_own_revision,
)

SEED_FOLDED_INDICES = frozenset({0, 45, 90, 135, 180})
EXPECTED_SEEDS = 9
EXPECTED_OBSTACLES = 9
RETAINED_ENDPOINT_BLOB = "cc66f06ddd3f7cc52d8a06d30a3920ba8e992c19"
RETAINED_TUPLES = frozenset({(0, 0, 0, 0), (15, 15, 15, 15)})

type LabelTuple = tuple[int, int, int, int]
type Masks = tuple[int, int, int, int]


class FixedPatternError(ValueError):
    """An input, strict-witness, mask, or exact-area guard failed."""


@dataclass(frozen=True, slots=True)
class SourceReferences:
    endpoint_path: str
    endpoint_git_commit: str
    endpoint_blob: str
    wall_path: str
    wall_git_commit: str
    wall_blob: str
    wall_constructor_revision: str


@dataclass(frozen=True, slots=True)
class MaskWitness:
    orientation_index: int
    orientation_label: str
    centre: Point
    masks: Masks
    rejected_count: int
    direction_sources: tuple[tuple[int, bool], ...]
    sources: SourceReferences


@dataclass(frozen=True, slots=True)
class WitnessBank:
    status: Literal["complete", "partial"]
    witnesses: tuple[MaskWitness, ...]
    failure_bits: int
    checked_seed_indices: tuple[int, ...]
    expected_seed_indices: tuple[int, ...]
    all_uncertified_refuted: bool
    wall_seconds: float
    error: str | None = None

    @property
    def rejected_labels(self) -> int:
        return self.failure_bits.bit_count()

    @property
    def failure_bits_hex(self) -> str:
        """Encode the table without using an unbounded decimal conversion."""

        return hex(self.failure_bits)


@dataclass(frozen=True, slots=True)
class DirectionCheck:
    index: int
    label: str
    container_area: Fraction
    covered_area: Fraction
    uncovered_area: Fraction
    nonempty_subsets: int


@dataclass(frozen=True, slots=True)
class CandidateCheck:
    status: Literal["covered", "uncovered", "partial"]
    candidate: LabelTuple
    directions: tuple[DirectionCheck, ...]
    escape: MaskWitness | None
    footprint_source: SourceReferences
    wall_seconds: float
    broadcast_failure_bits: int = 0
    error: str | None = None

    @property
    def broadcast_failure_bits_hex(self) -> str:
        return hex(self.broadcast_failure_bits)


@dataclass(frozen=True, slots=True)
class FixedPatternResult:
    verdict: Literal["accept-expansion", "refute-expansion-by-d", "unresolved"]
    bank: WitnessBank
    candidate: LabelTuple | None
    candidate_check: CandidateCheck | None


def _dot(left: Point, right: Point) -> Fraction:
    return left[0] * right[0] + left[1] * right[1]


def _subtract(left: Point, right: Point) -> Point:
    return left[0] - right[0], left[1] - right[1]


def _direction_axes(direction: Direction) -> tuple[Point, Point]:
    return (
        (direction.cosine, direction.sine),
        (-direction.sine, direction.cosine),
    )


def component_means(container: Polygon, obstacles: tuple[Polygon, ...]) -> tuple[Point, ...]:
    """Return sorted, deduplicated rational means of dot-free component closures."""

    decomposition = vertical_decompose(container, obstacles)
    components = sorted(
        (normalise_convex_polygon(component) for component in decomposition.components),
        key=lambda polygon: polygon,
    )
    centres: list[Point] = []
    seen: set[Point] = set()
    for component in components:
        vertices = tuple(dict.fromkeys(component))
        centre = (
            sum((point[0] for point in vertices), start=Fraction(0)) / len(vertices),
            sum((point[1] for point in vertices), start=Fraction(0)) / len(vertices),
        )
        if centre not in seen:
            seen.add(centre)
            centres.append(centre)
    return tuple(centres)


def strict_dot_free(
    centre: Point,
    direction: Direction,
    *,
    outer_side: Fraction,
    core_side: Fraction,
    dots: tuple[Point, ...],
) -> bool:
    """Replay open-container and closed dot-contact semantics in core coordinates."""

    container = container_rectangle(outer_side, core_side, direction)
    if not point_in_open_convex_polygon(centre, container):
        return False
    first, second = _direction_axes(direction)
    half = core_side / 2
    for dot in dots:
        delta = _subtract(dot, centre)
        if abs(_dot(delta, first)) <= half and abs(_dot(delta, second)) <= half:
            return False
    return True


def core_disjoint_from_polygon(
    centre: Point,
    direction: Direction,
    core_side: Fraction,
    polygon: Polygon,
) -> bool:
    """Use exact separating axes to prove strict separation from a convex polygon."""

    boundary = normalise_convex_polygon(polygon)
    first, second = _direction_axes(direction)
    axes = [first, second]
    for start, end in pairwise((*boundary, boundary[0])):
        edge = _subtract(end, start)
        axes.append((-edge[1], edge[0]))
    half = core_side / 2
    for axis in axes:
        projections = tuple(_dot(axis, point) for point in boundary)
        radius = half * (abs(_dot(axis, first)) + abs(_dot(axis, second)))
        centre_projection = _dot(axis, centre)
        if centre_projection + radius < min(projections) or max(projections) < (
            centre_projection - radius
        ):
            return True
    return False


def tuple_ordinal(values: LabelTuple) -> int:
    """Encode BL, BR, TL, TR labels with the last corner varying fastest."""

    if any(value < 0 or value >= EXPECTED_CLASSES for value in values):
        raise FixedPatternError("tuple label is outside the sixteen-class universe")
    result = 0
    for value in values:
        result = EXPECTED_CLASSES * result + value
    return result


def ordinal_tuple(ordinal: int) -> LabelTuple:
    if ordinal < 0 or ordinal >= RAW_TUPLE_UNIVERSE:
        raise FixedPatternError("tuple ordinal is outside the label universe")
    values: list[int] = []
    remainder = ordinal
    for _ in range(EXPECTED_CORNERS):
        values.append(remainder % EXPECTED_CLASSES)
        remainder //= EXPECTED_CLASSES
    return values[3], values[2], values[1], values[0]


def mask_product_bits(masks: Masks) -> int:
    """Return the exact 65,536-bit Cartesian product represented by four masks."""

    cap = (1 << EXPECTED_CLASSES) - 1
    if any(mask < 0 or mask & ~cap for mask in masks):
        raise FixedPatternError("class mask leaves the sixteen-bit universe")
    if any(mask == 0 for mask in masks):
        return 0
    choices = tuple(
        tuple(index for index in range(EXPECTED_CLASSES) if mask & (1 << index))
        for mask in masks
    )
    result = 0
    for values in product(*choices):
        result |= 1 << tuple_ordinal(cast(LabelTuple, values))
    return result


def merge_mask_product(
    failure_bits: int,
    masks: Masks,
    certified_tuples: frozenset[LabelTuple],
) -> tuple[int, int]:
    """Union one product after rejecting a contradiction with certified tuples."""

    product_bits = mask_product_bits(masks)
    certified_bits = sum(1 << tuple_ordinal(values) for values in certified_tuples)
    if product_bits & certified_bits:
        raise FixedPatternError("escape product contains an already-certified tuple")
    merged = failure_bits | product_bits
    return merged, (merged ^ failure_bits).bit_count()


def fixed_seed_indices(source: FrozenInput) -> tuple[int, ...]:
    """Resolve the frozen five folded indices to nine full-manifest directions."""

    manifest = full_owner_direction_manifest(
        angle_limit=ANGLE_LIMIT, direction_steps=DIRECTION_STEPS
    )
    if len(source.directions) != EXPECTED_ORIENTATIONS or len(manifest.orientations) != len(
        source.directions
    ):
        raise FixedPatternError("source lacks the complete 361-direction manifest")
    indices: list[int] = []
    for item, independent in zip(manifest.orientations, source.directions, strict=True):
        if (item.direction.ux, item.direction.uy) != (
            independent.cosine,
            independent.sine,
        ) or independent.label != f"owner-{item.index:03d}":
            raise FixedPatternError("independent and owner direction manifests disagree")
        if any(source.folded_index in SEED_FOLDED_INDICES for source in item.sources):
            indices.append(item.index)
    if len(indices) != EXPECTED_SEEDS:
        raise FixedPatternError("frozen folded sources do not resolve to nine seeds")
    return tuple(indices)


def _source_references(source: FrozenInput, wall: WallInput) -> SourceReferences:
    return SourceReferences(
        source.source_path,
        source.git_commit,
        source.git_blob,
        wall.source_path,
        wall.git_commit,
        wall.git_blob,
        wall.constructor_revision,
    )


def _mapping(value: object, label: str) -> dict[str, object]:
    if type(value) is not dict:
        raise FixedPatternError(f"{label} must be an object")
    return cast(dict[str, object], value)


def _sequence(value: object, label: str) -> list[object]:
    if type(value) is not list:
        raise FixedPatternError(f"{label} must be an array")
    return cast(list[object], value)


def parse_completed_containment(
    document: object,
    *,
    endpoint_blob: str,
    wall_blob: str,
    containment_revision: str,
) -> frozenset[LabelTuple]:
    """Recover C from a completed, source-bound no-gain BC318 receipt."""

    receipt = _mapping(document, "containment receipt")
    sources = _mapping(receipt.get("sources"), "containment sources")
    implementation = _mapping(sources.get("implementation"), "containment implementation")
    endpoint = _mapping(sources.get("endpoint"), "containment endpoint")
    wall = _mapping(sources.get("wall"), "containment wall")
    settings = _mapping(receipt.get("settings"), "containment settings")
    summary = _mapping(receipt.get("summary"), "containment summary")
    counts = _mapping(receipt.get("counts"), "containment counts")
    if (
        receipt.get("schema") != "wall-owner-containment/v1"
        or receipt.get("status") != "complete"
        or receipt.get("verdict") != "refute-containment-expansion"
        or implementation.get("git_commit") != containment_revision
        or endpoint.get("git_blob") != endpoint_blob
        or wall.get("git_blob") != wall_blob
        or settings.get("orientation_count") != EXPECTED_ORIENTATIONS
        or settings.get("class_order") != list(CLASS_IDS)
        or settings.get("corner_order") != list(CORNERS)
        or summary.get("logical_slots") != 128
        or summary.get("unresolved_relations") != 0
        or counts.get("raw_label_universe") != RAW_TUPLE_UNIVERSE
        or counts.get("impossible") != 0
        or counts.get("new_covered") != 0
        or counts.get("covered") != len(RETAINED_TUPLES)
    ):
        raise FixedPatternError("containment receipt violates the conditional entry")
    raw_families = _sequence(receipt.get("masks"), "containment masks")
    if len(raw_families) != 2:
        raise FixedPatternError("containment masks require two families")
    covered: set[LabelTuple] = set()
    cap = (1 << EXPECTED_CLASSES) - 1
    for family_index, raw_family in enumerate(raw_families):
        family = _sequence(raw_family, f"containment masks[{family_index}]")
        if len(family) != EXPECTED_CORNERS or any(
            type(mask) is not int or mask < 0 or mask & ~cap for mask in family
        ):
            raise FixedPatternError("containment masks leave the four-by-sixteen universe")
        choices = tuple(
            tuple(index for index in range(EXPECTED_CLASSES) if cast(int, mask) & (1 << index))
            for mask in family
        )
        covered.update(cast(LabelTuple, values) for values in product(*choices))
    result = frozenset(covered)
    if result != RETAINED_TUPLES:
        raise FixedPatternError("containment masks do not recover exactly the retained set C")
    return result


def load_completed_containment(
    path: Path,
    expected_blob: str,
    *,
    endpoint_blob: str,
    wall_blob: str,
    containment_revision: str,
) -> tuple[frozenset[LabelTuple], dict[str, str]]:
    """Bind the completed BC318 receipt through Git and recover its certified set."""

    _, relative, git_commit, git_blob = bind_clean_git_blob(
        path, expected_blob, label="containment receipt"
    )
    try:
        document: object = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise FixedPatternError(f"could not read containment receipt: {error}") from error
    certified = parse_completed_containment(
        document,
        endpoint_blob=endpoint_blob,
        wall_blob=wall_blob,
        containment_revision=containment_revision,
    )
    return certified, {
        "path": relative,
        "git_commit": git_commit,
        "git_blob": git_blob,
        "implementation_revision": containment_revision,
    }


def _validate_endpoint_blob(value: str) -> None:
    if value != RETAINED_ENDPOINT_BLOB:
        raise FixedPatternError("endpoint blob differs from the retained exp143 authority")


def _direction_sources(index: int) -> tuple[tuple[int, bool], ...]:
    item = full_owner_direction_manifest().orientations[index]
    return tuple((source.folded_index, source.reflected) for source in item.sources)


def _wall_polygons(wall: WallInput) -> tuple[Polygon, ...]:
    if len(wall.classes) != EXPECTED_CLASSES or any(
        item.disposition != "possible" or item.wall_footprint is None for item in wall.classes
    ):
        raise FixedPatternError("fixed-pattern stage requires sixteen possible wall polygons")
    return tuple(
        item.wall_footprint for item in wall.classes if item.wall_footprint is not None
    )


def witness_masks(
    centre: Point,
    direction: Direction,
    *,
    source: FrozenInput,
    wall: WallInput,
) -> Masks:
    """Build and independently replay four sixteen-bit avoidance masks."""

    footprints = _wall_polygons(wall)
    offsets = core_offsets(source.core_side, direction)
    corner_families = tuple(
        reflect_to_four_corners(polygon, source.outer_side) for polygon in footprints
    )
    masks: list[int] = []
    for corner in range(EXPECTED_CORNERS):
        mask = 0
        for class_index in range(EXPECTED_CLASSES):
            polygon = corner_families[class_index][corner]
            collision = collision_polygon(polygon, offsets)
            minkowski_avoids = not point_in_closed_convex_polygon(centre, collision)
            sat_avoids = core_disjoint_from_polygon(
                centre, direction, source.core_side, polygon
            )
            if minkowski_avoids != sat_avoids:
                raise FixedPatternError(
                    "owner mask disagrees with independent exact SAT replay"
                )
            if sat_avoids:
                mask |= 1 << class_index
        masks.append(mask)
    return masks[0], masks[1], masks[2], masks[3]


def _dot_free_centres(source: FrozenInput, direction: Direction) -> tuple[Point, ...]:
    container = container_rectangle(source.outer_side, source.core_side, direction)
    offsets = core_offsets(source.core_side, direction)
    dot_obstacles = tuple(collision_polygon((dot,), offsets) for dot in source.dots)
    centres = component_means(container, dot_obstacles)
    for centre in centres:
        if not strict_dot_free(
            centre,
            direction,
            outer_side=source.outer_side,
            core_side=source.core_side,
            dots=source.dots,
        ):
            raise FixedPatternError("dot-free component mean failed independent strict replay")
    return centres


def _all_uncertified_refuted(
    failure_bits: int, certified_tuples: frozenset[LabelTuple]
) -> bool:
    universe = (1 << RAW_TUPLE_UNIVERSE) - 1
    certified_bits = sum(1 << tuple_ordinal(values) for values in certified_tuples)
    return failure_bits & (universe ^ certified_bits) == universe ^ certified_bits


def build_witness_bank(
    source: FrozenInput,
    wall: WallInput,
    certified_tuples: frozenset[LabelTuple],
    *,
    seed_deadline: float,
    total_deadline: float,
) -> WitnessBank:
    """Run the nine fixed seed directions and retain useful mask witnesses."""

    started = time.perf_counter()
    indices = fixed_seed_indices(source)
    failure_bits = 0
    witnesses: list[MaskWitness] = []
    seen_masks: set[Masks] = set()
    checked: list[int] = []
    for index in indices:
        if time.perf_counter() >= min(seed_deadline, total_deadline):
            return WitnessBank(
                status="partial",
                witnesses=tuple(witnesses),
                failure_bits=failure_bits,
                checked_seed_indices=tuple(checked),
                expected_seed_indices=indices,
                all_uncertified_refuted=False,
                wall_seconds=time.perf_counter() - started,
                error="seed-stage deadline reached",
            )
        direction = source.directions[index]
        for centre in _dot_free_centres(source, direction):
            if time.perf_counter() >= min(seed_deadline, total_deadline):
                return WitnessBank(
                    status="partial",
                    witnesses=tuple(witnesses),
                    failure_bits=failure_bits,
                    checked_seed_indices=tuple(checked),
                    expected_seed_indices=indices,
                    all_uncertified_refuted=False,
                    wall_seconds=time.perf_counter() - started,
                    error="seed-stage deadline reached",
                )
            masks = witness_masks(centre, direction, source=source, wall=wall)
            if any(mask == 0 for mask in masks) or masks in seen_masks:
                continue
            seen_masks.add(masks)
            product_count = mask_product_bits(masks).bit_count()
            merged, added = merge_mask_product(failure_bits, masks, certified_tuples)
            if added == 0:
                continue
            failure_bits = merged
            witnesses.append(
                MaskWitness(
                    index,
                    direction.label,
                    centre,
                    masks,
                    product_count,
                    _direction_sources(index),
                    _source_references(source, wall),
                )
            )
        if time.perf_counter() >= min(seed_deadline, total_deadline):
            return WitnessBank(
                status="partial",
                witnesses=tuple(witnesses),
                failure_bits=failure_bits,
                checked_seed_indices=tuple(checked),
                expected_seed_indices=indices,
                all_uncertified_refuted=False,
                wall_seconds=time.perf_counter() - started,
                error="seed-stage deadline reached",
            )
        checked.append(index)
        if _all_uncertified_refuted(failure_bits, certified_tuples):
            break
    return WitnessBank(
        status="complete",
        witnesses=tuple(witnesses),
        failure_bits=failure_bits,
        checked_seed_indices=tuple(checked),
        expected_seed_indices=indices,
        all_uncertified_refuted=_all_uncertified_refuted(failure_bits, certified_tuples),
        wall_seconds=time.perf_counter() - started,
    )


def select_first_candidate(
    bank: WitnessBank, certified_tuples: frozenset[LabelTuple]
) -> LabelTuple | None:
    """Select exactly the first tuple outside the certificates and failure table."""

    if bank.status != "complete":
        return None
    certified = {tuple_ordinal(values) for values in certified_tuples}
    for ordinal in range(RAW_TUPLE_UNIVERSE):
        if ordinal not in certified and not bank.failure_bits & (1 << ordinal):
            return ordinal_tuple(ordinal)
    return None


def selected_wall_footprints(
    wall: WallInput, candidate: LabelTuple, *, outer_side: Fraction
) -> tuple[Polygon, ...]:
    """Substitute the candidate's four exp146 wall footprints in physical corners."""

    footprints = _wall_polygons(wall)
    return tuple(
        reflect_to_four_corners(footprints[class_index], outer_side)[corner]
        for corner, class_index in enumerate(candidate)
    )


def _direction_record(index: int, label: str, measure: UnionMeasure) -> DirectionCheck:
    return DirectionCheck(
        index,
        label,
        measure.container_area,
        measure.covered_area,
        measure.uncovered_area,
        measure.nonempty_subsets,
    )


def _extract_escape(
    source: FrozenInput,
    wall: WallInput,
    candidate: LabelTuple,
    direction_index: int,
    certified_tuples: frozenset[LabelTuple],
) -> MaskWitness:
    direction = source.directions[direction_index]
    selected = selected_wall_footprints(wall, candidate, outer_side=source.outer_side)
    offsets = core_offsets(source.core_side, direction)
    obstacles = tuple(collision_polygon(polygon, offsets) for polygon in selected) + tuple(
        collision_polygon((dot,), offsets) for dot in source.dots
    )
    if len(obstacles) != EXPECTED_OBSTACLES:
        raise FixedPatternError("deficit extraction requires exactly nine obstacles")
    container = container_rectangle(source.outer_side, source.core_side, direction)
    for centre in component_means(container, obstacles):
        if not strict_dot_free(
            centre,
            direction,
            outer_side=source.outer_side,
            core_side=source.core_side,
            dots=source.dots,
        ) or not all(
            core_disjoint_from_polygon(centre, direction, source.core_side, polygon)
            for polygon in selected
        ):
            continue
        masks = witness_masks(centre, direction, source=source, wall=wall)
        product_bits = mask_product_bits(masks)
        if not product_bits & (1 << tuple_ordinal(candidate)):
            raise FixedPatternError("deficit witness does not replay against its candidate")
        merge_mask_product(0, masks, certified_tuples)
        return MaskWitness(
            direction_index,
            direction.label,
            centre,
            masks,
            product_bits.bit_count(),
            _direction_sources(direction_index),
            _source_references(source, wall),
        )
    raise FixedPatternError("positive exact deficit lacks a replayable strict escape")


def check_one_candidate(
    source: FrozenInput,
    wall: WallInput,
    bank: WitnessBank,
    candidate: LabelTuple,
    certified_tuples: frozenset[LabelTuple],
    *,
    deadline: float,
) -> CandidateCheck:
    """Check one selected tuple on all directions, stopping at its first deficit."""

    started = time.perf_counter()
    if bank.status != "complete" or select_first_candidate(bank, certified_tuples) != candidate:
        raise FixedPatternError("candidate differs from the deterministic first survivor")
    selected = selected_wall_footprints(wall, candidate, outer_side=source.outer_side)
    substituted = replace(source, footprints=selected)
    footprint_source = _source_references(source, wall)
    rows: list[DirectionCheck] = []
    for index, direction in enumerate(substituted.directions):
        if time.perf_counter() >= deadline:
            return CandidateCheck(
                "partial",
                candidate,
                tuple(rows),
                None,
                footprint_source,
                time.perf_counter() - started,
                error="total deadline reached",
            )
        try:
            measure = measure_direction(
                substituted, direction, max_subsets=511, deadline=deadline
            )
        except DeadlineError:
            return CandidateCheck(
                "partial",
                candidate,
                tuple(rows),
                None,
                footprint_source,
                time.perf_counter() - started,
                error="total deadline reached",
            )
        if measure.uncovered_area < 0:
            raise FixedPatternError("independent union returned negative uncovered area")
        rows.append(_direction_record(index, direction.label, measure))
        if measure.uncovered_area > 0:
            if time.perf_counter() >= deadline:
                return CandidateCheck(
                    "partial",
                    candidate,
                    tuple(rows),
                    None,
                    footprint_source,
                    time.perf_counter() - started,
                    error="total deadline reached before escape extraction",
                )
            escape = _extract_escape(source, wall, candidate, index, certified_tuples)
            broadcast = mask_product_bits(escape.masks)
            if time.perf_counter() >= deadline:
                return CandidateCheck(
                    "partial",
                    candidate,
                    tuple(rows),
                    escape,
                    footprint_source,
                    time.perf_counter() - started,
                    broadcast,
                    "total deadline reached after escape extraction",
                )
            return CandidateCheck(
                "uncovered",
                candidate,
                tuple(rows),
                escape,
                footprint_source,
                time.perf_counter() - started,
                broadcast,
            )
    if len(rows) != EXPECTED_ORIENTATIONS:
        raise FixedPatternError("candidate checker did not complete all 361 directions")
    completed_in_time = time.perf_counter() < deadline
    return CandidateCheck(
        "covered" if completed_in_time else "partial",
        candidate,
        tuple(rows),
        None,
        footprint_source,
        time.perf_counter() - started,
        error=None if completed_in_time else "total deadline reached",
    )


def run_fixed_pattern(
    source: FrozenInput,
    wall: WallInput,
    certified_tuples: frozenset[LabelTuple],
    *,
    total_seconds: float = 240,
    seed_seconds: float = 60,
) -> FixedPatternResult:
    """Compose the fixed witness bank with at most one candidate check."""

    if (
        not math.isfinite(total_seconds)
        or not math.isfinite(seed_seconds)
        or total_seconds <= 0
        or seed_seconds <= 0
        or seed_seconds > total_seconds
    ):
        raise FixedPatternError("internal deadlines must satisfy 0 < seed <= total")
    if (source.outer_side, source.core_side) != (OUTER_SIDE, CORE_SIDE):
        raise FixedPatternError("source changes the frozen outer or core side")
    started = time.perf_counter()
    total_deadline = started + total_seconds
    bank = build_witness_bank(
        source,
        wall,
        certified_tuples,
        seed_deadline=started + seed_seconds,
        total_deadline=total_deadline,
    )
    if bank.status != "complete":
        return FixedPatternResult("unresolved", bank, None, None)
    if bank.all_uncertified_refuted:
        return FixedPatternResult("refute-expansion-by-d", bank, None, None)
    candidate = select_first_candidate(bank, certified_tuples)
    if candidate is None:
        raise FixedPatternError("complete bank has neither a survivor nor a refutation")
    checked = check_one_candidate(
        source,
        wall,
        bank,
        candidate,
        certified_tuples,
        deadline=total_deadline,
    )
    if checked.status == "uncovered" and checked.escape is not None:
        combined = bank.failure_bits | checked.broadcast_failure_bits
        useful = combined != bank.failure_bits
        bank = replace(
            bank,
            witnesses=bank.witnesses + ((checked.escape,) if useful else ()),
            failure_bits=combined,
            all_uncertified_refuted=_all_uncertified_refuted(combined, certified_tuples),
        )
    verdict: Literal["accept-expansion", "refute-expansion-by-d", "unresolved"] = (
        "accept-expansion"
        if checked.status == "covered"
        else "refute-expansion-by-d"
        if bank.all_uncertified_refuted
        else "unresolved"
    )
    return FixedPatternResult(verdict, bank, candidate, checked)


def _point_record(point: Point) -> list[str]:
    return [str(point[0]), str(point[1])]


def _source_record(source: SourceReferences) -> dict[str, object]:
    return {
        "endpoint": {
            "path": source.endpoint_path,
            "git_commit": source.endpoint_git_commit,
            "git_blob": source.endpoint_blob,
        },
        "wall": {
            "path": source.wall_path,
            "git_commit": source.wall_git_commit,
            "git_blob": source.wall_blob,
            "constructor_revision": source.wall_constructor_revision,
        },
    }


def _witness_record(witness: MaskWitness) -> dict[str, object]:
    return {
        "orientation_index": witness.orientation_index,
        "orientation_label": witness.orientation_label,
        "direction_sources": [
            {"folded_index": index, "reflected": reflected}
            for index, reflected in witness.direction_sources
        ],
        "centre": _point_record(witness.centre),
        "masks_hex_16bit": [f"0x{mask:04x}" for mask in witness.masks],
        "product_size": witness.rejected_count,
        "sources": _source_record(witness.sources),
    }


def result_document(
    result: FixedPatternResult,
    *,
    implementation_revision: str,
    containment_source: dict[str, str],
    wall_seconds: float,
) -> dict[str, object]:
    """Serialize replayable evidence without decimalizing the 65,536-bit tables."""

    bank = result.bank
    remaining = RAW_TUPLE_UNIVERSE - len(RETAINED_TUPLES) - bank.rejected_labels
    candidate_record: dict[str, object] | None = None
    if result.candidate_check is not None:
        checked = result.candidate_check
        candidate_record = {
            "status": checked.status,
            "tuple": list(checked.candidate),
            "selected_classes": [CLASS_IDS[index] for index in checked.candidate],
            "footprint_substitution": _source_record(checked.footprint_source),
            "directions": [
                {
                    "index": row.index,
                    "label": row.label,
                    "container_area": str(row.container_area),
                    "covered_area": str(row.covered_area),
                    "uncovered_area": str(row.uncovered_area),
                    "nonempty_subsets": row.nonempty_subsets,
                }
                for row in checked.directions
            ],
            "escape": None if checked.escape is None else _witness_record(checked.escape),
            "broadcast_failure_bits_hex": checked.broadcast_failure_bits_hex,
            "wall_seconds": checked.wall_seconds,
            "error": checked.error,
        }
    status = (
        "partial"
        if bank.status == "partial"
        or (result.candidate_check is not None and result.candidate_check.status == "partial")
        else "complete"
    )
    return {
        "schema": "wall-owner-fixed-pattern/v1",
        "status": status,
        "verdict": result.verdict,
        "claim_limit": (
            "fixed five-dot pattern only; no packing feasibility or exhaustive owner routing"
        ),
        "sources": {
            "implementation": {
                "git_commit": implementation_revision,
                "module": "packing/devtools/wall_owner_fixed_pattern.py",
            },
            "containment": containment_source,
        },
        "settings": {
            "outer_side": str(OUTER_SIDE),
            "core_side": str(CORE_SIDE),
            "orientation_count": EXPECTED_ORIENTATIONS,
            "seed_folded_indices": sorted(SEED_FOLDED_INDICES),
            "expected_seed_count": EXPECTED_SEEDS,
            "corner_order": list(CORNERS),
            "class_order": list(CLASS_IDS),
            "tuple_order": "BL, BR, TL, TR; last corner varies fastest",
            "failure_table_encoding": "hexadecimal integer; bit i is tuple ordinal i",
            "candidate_limit": 1,
        },
        "bank": {
            "status": bank.status,
            "checked_seed_indices": list(bank.checked_seed_indices),
            "expected_seed_indices": list(bank.expected_seed_indices),
            "witnesses": [_witness_record(witness) for witness in bank.witnesses],
            "failure_bits_hex": bank.failure_bits_hex,
            "distinct_rejected_labels": bank.rejected_labels,
            "remaining_uncertified_labels": remaining,
            "all_uncertified_refuted": bank.all_uncertified_refuted,
            "wall_seconds": bank.wall_seconds,
            "error": bank.error,
        },
        "candidate": candidate_record,
        "summary": {
            "certified_labels": len(RETAINED_TUPLES),
            "distinct_rejected_labels": bank.rejected_labels,
            "remaining_uncertified_labels": remaining,
            "selected_candidate": None if result.candidate is None else list(result.candidate),
            "wall_seconds": wall_seconds,
        },
        "error": bank.error
        if bank.status == "partial"
        else (None if result.candidate_check is None else result.candidate_check.error),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("endpoint_receipt", type=Path)
    parser.add_argument("wall_receipt", type=Path)
    parser.add_argument("containment_receipt", type=Path)
    parser.add_argument("--expect-endpoint-blob", required=True)
    parser.add_argument("--expect-wall-blob", required=True)
    parser.add_argument("--expect-wall-source", required=True)
    parser.add_argument("--expect-containment-blob", required=True)
    parser.add_argument("--expect-containment-revision", required=True)
    parser.add_argument("--expect-git-revision", required=True)
    parser.add_argument("--deadline-seconds", type=float, default=240)
    parser.add_argument("--seed-deadline-seconds", type=float, default=60)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    started = time.perf_counter()
    output: Path | None = None
    document: dict[str, object]
    try:
        repository, revision = validate_own_revision(args.expect_git_revision)
        inputs = (args.endpoint_receipt, args.wall_receipt, args.containment_receipt)
        output = validate_output_path(args.output, repository, inputs)
        _validate_endpoint_blob(args.expect_endpoint_blob)
        source = load_frozen_input(args.endpoint_receipt, args.expect_endpoint_blob)
        wall = load_wall_input(
            args.wall_receipt,
            args.expect_wall_blob,
            expected_source=args.expect_wall_source,
        )
        certified, containment_source = load_completed_containment(
            args.containment_receipt,
            args.expect_containment_blob,
            endpoint_blob=args.expect_endpoint_blob,
            wall_blob=args.expect_wall_blob,
            containment_revision=args.expect_containment_revision,
        )
        result = run_fixed_pattern(
            source,
            wall,
            certified,
            total_seconds=args.deadline_seconds,
            seed_seconds=args.seed_deadline_seconds,
        )
        document = result_document(
            result,
            implementation_revision=revision,
            containment_source=containment_source,
            wall_seconds=time.perf_counter() - started,
        )
        atomic_write_json(output, document)
    except (ContainmentError, FixedPatternError, OSError, json.JSONDecodeError) as error:
        document = {
            "schema": "wall-owner-fixed-pattern/v1",
            "status": "invalid",
            "verdict": "invalid",
            "wall_seconds": time.perf_counter() - started,
            "error": str(error),
        }
        if output is not None:
            atomic_write_json(output, document)
    print(json.dumps(document, indent=1), flush=True)
    return 0 if document.get("status") == "complete" else 2


if __name__ == "__main__":
    raise SystemExit(main())
