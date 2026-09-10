#!/usr/bin/env python3
"""Test one frozen two-attainer strict-core obstruction for fixed D."""

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
    AuditError,
    FrozenInput,
    collision_polygon,
    container_rectangle,
    core_offsets,
    load_frozen_input,
)
from devtools.multi_owner_domains import vertical_decompose
from devtools.owner_footprints import CORE_SIDE, OUTER_SIDE, Point, Polygon, polygon_area_twice
from devtools.wall_owner_containment import (
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
    core_disjoint_from_polygon,
    strict_dot_free,
)
from devtools.wall_owner_selected_cover import (
    SELECTED_TUPLE,
    SelectedEscape,
    select_four_footprints,
)
from devtools.wall_owner_sixth_site_feasibility import support_constraints
from devtools.wall_owner_sixth_site_screen import (
    SixthSiteScreenError,
    StrictSeparator,
    escape_core,
    strict_separator,
)

RIGHT_DIRECTION = 0
RIGHT_EXTREMUM = "u_max"
RIGHT_COMPONENT = 0
RIGHT_VERTEX = 1
LEFT_DIRECTION = 187
LEFT_EXTREMUM = "u_min"
LEFT_COMPONENT = 0
LEFT_VERTEX = 0
EXPECTED_SUPPORT_COUNT = LEFT_DIRECTION + 1
RETAINED_SELECTED_PATH = (
    "packing/campaign/series/series-000-smoke-and-calibration/results/agenda-033/"
    "exp-149-selected-wall-tuple-cover.json"
)
RETAINED_SELECTED_BLOB = "83ec897738d6d1b228623c3ac4c10cd9170d5940"
RETAINED_SELECTED_SOURCE = "5600c0fb4eccf9e9dcdf82b02506d3d4340651cb"
RETAINED_SIX_DOT_PATH = (
    "packing/campaign/series/series-000-smoke-and-calibration/results/agenda-033/"
    "exp-151-selected-six-dot-cover.json"
)
RETAINED_SIX_DOT_BLOB = "46d34b1e295d9f5178379b02780a8c598c1a73e5"
RETAINED_SIX_DOT_SOURCE = "c8cd38dad502c78840144bcae42df4294ba7f3d0"


class TwoAttainerError(ValueError):
    """A source, fixed-construction, or exact replay guard failed."""


@dataclass(frozen=True, slots=True)
class FixedAttainer:
    direction_index: int
    direction_label: str
    extremum: Literal["u_min", "u_max"]
    component_count: int
    component_index: int
    vertex_index: int
    vertex: Point
    value: Fraction


@dataclass(frozen=True, slots=True)
class FeasibilityEvidence:
    source_path: str
    git_commit: str
    git_blob: str
    implementation_revision: str
    support_count: int
    right: FixedAttainer
    left: FixedAttainer


@dataclass(frozen=True, slots=True)
class Witness:
    direction_index: int
    direction_label: str
    closure_attainer: Point
    component_mean: Point
    centre: Point


@dataclass(frozen=True, slots=True)
class TwoAttainerResult:
    status: Literal["complete", "partial", "invalid"]
    outcome: Literal["strict-obstruction", "no-positive-closure-x-gap", "incomplete", "invalid"]
    closure_x_gap: Fraction | None
    movement_bound: Fraction | None
    perturbation_coefficient: Fraction | None
    right: Witness | None
    left: Witness | None
    strict_x_gap: Fraction | None
    separator: StrictSeparator | None
    wall_seconds: float
    error: str | None = None


def _mapping(value: object, label: str) -> dict[str, object]:
    if type(value) is not dict:
        raise TwoAttainerError(f"{label} must be an object")
    return cast(dict[str, object], value)


def _sequence(value: object, label: str) -> list[object]:
    if type(value) is not list:
        raise TwoAttainerError(f"{label} must be an array")
    return cast(list[object], value)


def _integer(value: object, label: str) -> int:
    if type(value) is not int:
        raise TwoAttainerError(f"{label} must be an integer")
    return cast(int, value)


def _fraction(value: object, label: str) -> Fraction:
    if not isinstance(value, (str, int)) or isinstance(value, bool):
        raise TwoAttainerError(f"{label} must be an exact rational")
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as error:
        raise TwoAttainerError(f"{label} is not an exact rational") from error


def _point(value: object, label: str) -> Point:
    raw = _sequence(value, label)
    if len(raw) != 2:
        raise TwoAttainerError(f"{label} must have two coordinates")
    return _fraction(raw[0], f"{label}.x"), _fraction(raw[1], f"{label}.y")


def _parse_attainer(
    row: dict[str, object],
    *,
    source: FrozenInput,
    index: int,
    extremum: Literal["u_min", "u_max"],
    component_index: int,
    vertex_index: int,
) -> FixedAttainer:
    if _integer(row.get("index"), "support index") != index:
        raise TwoAttainerError("fixed support row has the wrong index")
    label = row.get("label")
    if label != source.directions[index].label:
        raise TwoAttainerError("fixed support row changes its manifest label")
    component_count = _integer(row.get("component_count"), "component count")
    extrema = _mapping(row.get("extrema"), "support extrema")
    record = _mapping(extrema.get(extremum), f"support {extremum}")
    if (
        _integer(record.get("component_index"), "attainer component") != component_index
        or _integer(record.get("vertex_index"), "attainer vertex") != vertex_index
        or record.get("semantics") != "positive-area component closure vertex"
    ):
        raise TwoAttainerError("fixed attainer identity changed")
    vertex = _point(record.get("vertex"), "attainer vertex")
    value = _fraction(record.get("value"), "attainer value")
    direction = source.directions[index]
    if _point(row.get("u"), "support u") != (direction.cosine, direction.sine) or _point(
        row.get("v"), "support v"
    ) != (-direction.sine, direction.cosine):
        raise TwoAttainerError("fixed support row changes its exact axes")
    projection = direction.cosine * vertex[0] + direction.sine * vertex[1]
    if value != projection:
        raise TwoAttainerError("fixed attainer value disagrees with its vertex")
    return FixedAttainer(
        index,
        cast(str, label),
        extremum,
        component_count,
        component_index,
        vertex_index,
        vertex,
        value,
    )


def parse_feasibility_evidence(
    document: object,
    *,
    source_path: str,
    git_commit: str,
    git_blob: str,
    expected_source: str,
    source: FrozenInput,
    wall: WallInput,
) -> FeasibilityEvidence:
    """Parse the fixed two attainers from a complete source-bound exp153 receipt."""

    receipt = _mapping(document, "feasibility receipt")
    if (
        receipt.get("schema") != "wall-owner-sixth-site-feasibility/v1"
        or receipt.get("status") != "complete"
        or receipt.get("outcome") != "refute-fixed-D-plus-one-site-family"
        or receipt.get("claim_limit")
        != "the explicit tuple (0,0,0,7) under fixed D plus one site only"
        or receipt.get("error") is not None
        or receipt.get("canonical_site") is not None
        or receipt.get("confirmation") != []
        or receipt.get("conflicting_escape") is not None
    ):
        raise TwoAttainerError("feasibility receipt is not the complete frozen refutation")
    sources = _mapping(receipt.get("sources"), "feasibility sources")
    expected_sources = {
        "implementation": {
            "git_commit": expected_source,
            "module": "packing/devtools/wall_owner_sixth_site_feasibility.py",
        },
        "endpoint": {
            "path": source.source_path,
            "git_commit": expected_source,
            "git_blob": source.git_blob,
        },
        "wall": {
            "path": wall.source_path,
            "git_commit": expected_source,
            "git_blob": wall.git_blob,
            "constructor_revision": wall.constructor_revision,
        },
        "selected_cover": {
            "path": RETAINED_SELECTED_PATH,
            "git_commit": expected_source,
            "git_blob": RETAINED_SELECTED_BLOB,
            "implementation_revision": RETAINED_SELECTED_SOURCE,
        },
        "six_dot_cover": {
            "path": RETAINED_SIX_DOT_PATH,
            "git_commit": expected_source,
            "git_blob": RETAINED_SIX_DOT_BLOB,
            "implementation_revision": RETAINED_SIX_DOT_SOURCE,
        },
    }
    if sources != expected_sources:
        raise TwoAttainerError("feasibility receipt changes its authority chain")
    settings = _mapping(receipt.get("settings"), "feasibility settings")
    selected_footprints = select_four_footprints(source, wall)
    if settings != {
        "outer_side": str(source.outer_side),
        "core_side": str(source.core_side),
        "candidate": list(SELECTED_TUPLE),
        "orientation_count": EXPECTED_ORIENTATIONS,
        "original_dot_count": len(source.dots),
        "support_obstacle_count": len(selected_footprints) + len(source.dots),
        "confirmation_obstacle_count": len(selected_footprints) + len(source.dots) + 1,
        "max_subsets": 1023,
        "candidate_limit": 1,
    }:
        raise TwoAttainerError("feasibility receipt changes the frozen settings")
    final_region = _mapping(receipt.get("final_region"), "final region")
    if final_region != {"dimension": None, "vertices": []}:
        raise TwoAttainerError("feasibility receipt does not retain an empty final region")
    supports = _sequence(receipt.get("supports"), "supports")
    if len(supports) != EXPECTED_SUPPORT_COUNT:
        raise TwoAttainerError("feasibility receipt changes the complete support prefix")
    for index, raw in enumerate(supports):
        row = _mapping(raw, f"support[{index}]")
        if row.get("index") != index or row.get("label") != source.directions[index].label:
            raise TwoAttainerError("feasibility support prefix changes manifest order")
        resulting = _sequence(row.get("resulting_region"), "resulting region")
        if (index < LEFT_DIRECTION and not resulting) or (
            index == LEFT_DIRECTION and resulting
        ):
            raise TwoAttainerError("feasibility receipt changes its first empty prefix")
    summary = _mapping(receipt.get("summary"), "feasibility summary")
    if (
        summary.get("support_directions_complete") != EXPECTED_SUPPORT_COUNT
        or summary.get("confirmation_directions_complete") != 0
    ):
        raise TwoAttainerError("feasibility summary changes its terminal prefix")
    right_row = _mapping(supports[RIGHT_DIRECTION], "right support")
    left_row = _mapping(supports[LEFT_DIRECTION], "left support")
    right = _parse_attainer(
        right_row,
        source=source,
        index=RIGHT_DIRECTION,
        extremum=RIGHT_EXTREMUM,
        component_index=RIGHT_COMPONENT,
        vertex_index=RIGHT_VERTEX,
    )
    left = _parse_attainer(
        left_row,
        source=source,
        index=LEFT_DIRECTION,
        extremum=LEFT_EXTREMUM,
        component_index=LEFT_COMPONENT,
        vertex_index=LEFT_VERTEX,
    )
    left_extrema = _mapping(left_row.get("extrema"), "left extrema")
    v_max = _mapping(left_extrema.get("v_max"), "left v_max")
    if (
        _integer(v_max.get("component_index"), "v_max component") != LEFT_COMPONENT
        or _integer(v_max.get("vertex_index"), "v_max vertex") != LEFT_VERTEX
        or _point(v_max.get("vertex"), "v_max vertex") != left.vertex
    ):
        raise TwoAttainerError("fixed left u_min/v_max shared attainer changed")
    return FeasibilityEvidence(
        source_path,
        git_commit,
        git_blob,
        expected_source,
        len(supports),
        right,
        left,
    )


def load_feasibility_evidence(
    path: Path,
    expected_blob: str,
    *,
    expected_source: str,
    source: FrozenInput,
    wall: WallInput,
) -> FeasibilityEvidence:
    """Bind one clean tracked exp153 receipt and parse the frozen attainers."""

    if len(expected_source) != 40 or any(
        character not in "0123456789abcdef" for character in expected_source
    ):
        raise TwoAttainerError("expected feasibility source must be 40 lowercase hex digits")
    _, relative, commit, blob = bind_clean_git_blob(
        path, expected_blob, label="feasibility receipt"
    )
    try:
        document = cast(object, json.loads(path.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError) as error:
        raise TwoAttainerError(f"could not read feasibility receipt: {error}") from error
    return parse_feasibility_evidence(
        document,
        source_path=relative,
        git_commit=commit,
        git_blob=blob,
        expected_source=expected_source,
        source=source,
        wall=wall,
    )


def _mean(polygon: Polygon) -> Point:
    vertices = tuple(dict.fromkeys(polygon))
    if len(vertices) < 3 or polygon_area_twice(vertices) <= 0:
        raise TwoAttainerError("selected decomposition component is not full-dimensional")
    return (
        sum((point[0] for point in vertices), start=Fraction(0)) / len(vertices),
        sum((point[1] for point in vertices), start=Fraction(0)) / len(vertices),
    )


def _interpolate(start: Point, end: Point, coefficient: Fraction) -> Point:
    return (
        start[0] + coefficient * (end[0] - start[0]),
        start[1] + coefficient * (end[1] - start[1]),
    )


def _strict_escape(source: FrozenInput, centre: Point, index: int) -> bool:
    direction = source.directions[index]
    return strict_dot_free(
        centre,
        direction,
        outer_side=source.outer_side,
        core_side=source.core_side,
        dots=source.dots,
    ) and all(
        core_disjoint_from_polygon(centre, direction, source.core_side, footprint)
        for footprint in source.footprints
    )


def _closure_component(source: FrozenInput, attainer: FixedAttainer) -> tuple[Polygon, Point]:
    direction = source.directions[attainer.direction_index]
    offsets = core_offsets(source.core_side, direction)
    obstacles = tuple(
        collision_polygon(footprint, offsets) for footprint in source.footprints
    ) + tuple(collision_polygon((dot,), offsets) for dot in source.dots)
    decomposition = vertical_decompose(
        container_rectangle(source.outer_side, source.core_side, direction), obstacles
    )
    if len(decomposition.components) != attainer.component_count:
        raise TwoAttainerError("reconstructed component count disagrees with exp153")
    if not 0 <= attainer.component_index < len(decomposition.components):
        raise TwoAttainerError("fixed component index is outside the reconstruction")
    component = decomposition.components[attainer.component_index]
    if (
        not 0 <= attainer.vertex_index < len(component)
        or component[attainer.vertex_index] != attainer.vertex
    ):
        raise TwoAttainerError("reconstructed closure vertex disagrees with exp153")
    _, u_min, u_max, _, v_max = support_constraints(
        decomposition.components, direction, source.core_side / 2
    )
    actual = u_max if attainer.extremum == "u_max" else u_min
    if actual is None or (
        actual.component_index,
        actual.vertex_index,
        actual.vertex,
        actual.value,
    ) != (
        attainer.component_index,
        attainer.vertex_index,
        attainer.vertex,
        attainer.value,
    ):
        raise TwoAttainerError("reconstructed projection extremum disagrees with exp153")
    if attainer.direction_index == LEFT_DIRECTION and (
        v_max is None
        or (v_max.component_index, v_max.vertex_index, v_max.vertex)
        != (attainer.component_index, attainer.vertex_index, attainer.vertex)
    ):
        raise TwoAttainerError("reconstructed left u_min/v_max identity changed")
    return component, _mean(component)


def _core(source: FrozenInput, centre: Point, index: int) -> Polygon:
    direction = source.directions[index]
    return escape_core(source, SelectedEscape(index, direction.label, centre))


def _x_gap(left_core: Polygon, right_core: Polygon) -> Fraction:
    return min(point[0] for point in right_core) - max(point[0] for point in left_core)


def _x_radius(source: FrozenInput, index: int) -> Fraction:
    direction = source.directions[index]
    return source.core_side * (abs(direction.cosine) + abs(direction.sine)) / 2


def _partial(
    started: float,
    error: str,
    *,
    closure_gap: Fraction | None = None,
    movement_bound: Fraction | None = None,
    coefficient: Fraction | None = None,
    right: Witness | None = None,
    left: Witness | None = None,
    strict_gap: Fraction | None = None,
    separator: StrictSeparator | None = None,
) -> TwoAttainerResult:
    return TwoAttainerResult(
        "partial",
        "incomplete",
        closure_gap,
        movement_bound,
        coefficient,
        right,
        left,
        strict_gap,
        separator,
        max(0.0, time.perf_counter() - started),
        error,
    )


def run_two_attainer_obstruction(  # noqa: PLR0911
    source: FrozenInput,
    wall: WallInput,
    feasibility: FeasibilityEvidence,
    *,
    deadline_seconds: float = 90,
) -> TwoAttainerResult:
    """Run the one frozen x-axis closure-to-strict obstruction construction."""

    if not math.isfinite(deadline_seconds) or deadline_seconds <= 0:
        raise TwoAttainerError("internal deadline must be finite and positive")
    if (source.outer_side, source.core_side) != (OUTER_SIDE, CORE_SIDE):
        raise TwoAttainerError("source changes the frozen outer or core side")
    if len(source.directions) != EXPECTED_ORIENTATIONS:
        raise TwoAttainerError("source lacks the complete direction manifest")
    started = time.perf_counter()
    deadline = started + deadline_seconds
    original = replace(source, footprints=select_four_footprints(source, wall))
    if time.perf_counter() >= deadline:
        return _partial(started, "deadline reached before domain reconstruction")
    right_component, right_mean = _closure_component(original, feasibility.right)
    if time.perf_counter() >= deadline:
        return _partial(started, "deadline reached after first domain reconstruction")
    left_component, left_mean = _closure_component(original, feasibility.left)
    if time.perf_counter() >= deadline:
        return _partial(started, "deadline reached after second domain reconstruction")
    if (
        feasibility.right.vertex not in right_component
        or feasibility.left.vertex not in left_component
    ):
        raise TwoAttainerError("fixed attainer disappeared from its reconstructed component")

    closure_gap = (
        feasibility.right.vertex[0]
        - _x_radius(original, RIGHT_DIRECTION)
        - feasibility.left.vertex[0]
        - _x_radius(original, LEFT_DIRECTION)
    )
    replayed_closure_gap = _x_gap(
        _core(original, feasibility.left.vertex, LEFT_DIRECTION),
        _core(original, feasibility.right.vertex, RIGHT_DIRECTION),
    )
    if replayed_closure_gap != closure_gap:
        raise TwoAttainerError("fixed x-radius formula disagrees with core reconstruction")
    if closure_gap <= 0:
        if time.perf_counter() >= deadline:
            return _partial(
                started, "deadline reached after closure-gap test", closure_gap=closure_gap
            )
        return TwoAttainerResult(
            "complete",
            "no-positive-closure-x-gap",
            closure_gap,
            None,
            None,
            None,
            None,
            None,
            None,
            max(0.0, time.perf_counter() - started),
        )

    right_dx = right_mean[0] - feasibility.right.vertex[0]
    left_dx = left_mean[0] - feasibility.left.vertex[0]
    possible_loss = abs(right_dx) + abs(left_dx)
    coefficient = (
        Fraction(1, 2)
        if possible_loss == 0
        else min(Fraction(1, 2), closure_gap / (2 * possible_loss))
    )
    if not 0 < coefficient < 1:
        raise TwoAttainerError("perturbation coefficient is not strictly interior")
    right_centre = _interpolate(feasibility.right.vertex, right_mean, coefficient)
    left_centre = _interpolate(feasibility.left.vertex, left_mean, coefficient)
    right = Witness(
        RIGHT_DIRECTION,
        original.directions[RIGHT_DIRECTION].label,
        feasibility.right.vertex,
        right_mean,
        right_centre,
    )
    left = Witness(
        LEFT_DIRECTION,
        original.directions[LEFT_DIRECTION].label,
        feasibility.left.vertex,
        left_mean,
        left_centre,
    )
    if time.perf_counter() >= deadline:
        return _partial(
            started,
            "deadline reached before strict replay",
            closure_gap=closure_gap,
            movement_bound=possible_loss,
            coefficient=coefficient,
            right=right,
            left=left,
        )
    if not _strict_escape(original, right.centre, RIGHT_DIRECTION) or not _strict_escape(
        original, left.centre, LEFT_DIRECTION
    ):
        return TwoAttainerResult(
            "invalid",
            "invalid",
            closure_gap,
            possible_loss,
            coefficient,
            right,
            left,
            None,
            None,
            max(0.0, time.perf_counter() - started),
            "margin-bounded inward perturbation fails independent strict escape replay",
        )
    strict_gap = _x_gap(
        _core(original, left.centre, LEFT_DIRECTION),
        _core(original, right.centre, RIGHT_DIRECTION),
    )
    separator = strict_separator(
        _core(original, left.centre, LEFT_DIRECTION),
        _core(original, right.centre, RIGHT_DIRECTION),
    )
    if strict_gap < closure_gap / 2 or separator is None or separator.gap <= 0:
        return TwoAttainerResult(
            "invalid",
            "invalid",
            closure_gap,
            possible_loss,
            coefficient,
            right,
            left,
            strict_gap,
            separator,
            max(0.0, time.perf_counter() - started),
            "margin-bounded perturbation lost the fixed strict x-axis separator",
        )
    if time.perf_counter() >= deadline:
        return _partial(
            started,
            "deadline reached after strict SAT replay",
            closure_gap=closure_gap,
            movement_bound=possible_loss,
            coefficient=coefficient,
            right=right,
            left=left,
            strict_gap=strict_gap,
            separator=separator,
        )
    return TwoAttainerResult(
        "complete",
        "strict-obstruction",
        closure_gap,
        possible_loss,
        coefficient,
        right,
        left,
        strict_gap,
        separator,
        max(0.0, time.perf_counter() - started),
    )


def _point_record(point: Point) -> list[str]:
    return [str(point[0]), str(point[1])]


def _witness_record(witness: Witness | None, *, verified: bool) -> dict[str, object] | None:
    if witness is None:
        return None
    return {
        "direction_index": witness.direction_index,
        "direction_label": witness.direction_label,
        "closure_attainer": _point_record(witness.closure_attainer),
        "component_vertex_mean": _point_record(witness.component_mean),
        "candidate_centre": _point_record(witness.centre),
        "strict_replay_verified": verified,
        "required_replay": (
            "open container; closed original-five-dot and four-selected-patch avoidance"
        ),
    }


def _separator_record(separator: StrictSeparator | None) -> dict[str, object] | None:
    if separator is None:
        return None
    return {
        "axis": _point_record(separator.axis),
        "first_max": str(separator.first_max),
        "second_min": str(separator.second_min),
        "gap": str(separator.gap),
        "order": separator.order,
    }


def result_document(
    result: TwoAttainerResult,
    *,
    source: FrozenInput,
    wall: WallInput,
    feasibility: FeasibilityEvidence,
    implementation_revision: str,
    process_seconds: float,
) -> dict[str, object]:
    return {
        "schema": "wall-owner-two-attainer-obstruction/v1",
        "status": result.status,
        "outcome": result.outcome,
        "claim_limit": (
            "one fixed x-axis construction from exp153 rows 0 and 187; a positive "
            "result proves only that two original-D-missed cores require distinct "
            "additional unit atoms, for nominal total mass at least 7 in the selected "
            "four-patch relaxation"
        ),
        "banking_condition": (
            "an available-mass conclusion separately requires proof that the five "
            "original sites lie outside the selected occupied patches"
        ),
        "sources": {
            "implementation": {
                "git_commit": implementation_revision,
                "module": "packing/devtools/wall_owner_two_attainer_obstruction.py",
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
            "sixth_site_feasibility": {
                "path": feasibility.source_path,
                "git_commit": feasibility.git_commit,
                "git_blob": feasibility.git_blob,
                "implementation_revision": feasibility.implementation_revision,
            },
        },
        "settings": {
            "outer_side": str(source.outer_side),
            "core_side": str(source.core_side),
            "candidate": list(SELECTED_TUPLE),
            "axis": ["1", "0"],
            "right_seed": [RIGHT_DIRECTION, RIGHT_EXTREMUM, RIGHT_COMPONENT, RIGHT_VERTEX],
            "left_seed": [LEFT_DIRECTION, LEFT_EXTREMUM, LEFT_COMPONENT, LEFT_VERTEX],
            "attempt_limit": 1,
        },
        "closure_x_gap": None if result.closure_x_gap is None else str(result.closure_x_gap),
        "movement_bound": None if result.movement_bound is None else str(result.movement_bound),
        "perturbation_coefficient": None
        if result.perturbation_coefficient is None
        else str(result.perturbation_coefficient),
        "right_witness": _witness_record(
            result.right, verified=result.outcome == "strict-obstruction"
        ),
        "left_witness": _witness_record(
            result.left, verified=result.outcome == "strict-obstruction"
        ),
        "strict_x_gap": None if result.strict_x_gap is None else str(result.strict_x_gap),
        "strict_sat": _separator_record(result.separator),
        "summary": {
            "strict_escape_count": 2 if result.outcome == "strict-obstruction" else 0,
            "strict_pair_disjoint": result.outcome == "strict-obstruction",
            "wall_seconds": result.wall_seconds,
            "process_seconds": process_seconds,
        },
        "error": result.error,
    }


def _validate_endpoint_blob(value: str) -> None:
    if value != RETAINED_ENDPOINT_BLOB:
        raise TwoAttainerError("endpoint differs from the retained exp143 authority")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("endpoint_receipt", type=Path)
    parser.add_argument("wall_receipt", type=Path)
    parser.add_argument("feasibility_receipt", type=Path)
    parser.add_argument("--expect-endpoint-blob", required=True)
    parser.add_argument("--expect-wall-blob", required=True)
    parser.add_argument("--expect-wall-source", required=True)
    parser.add_argument("--expect-feasibility-blob", required=True)
    parser.add_argument("--expect-feasibility-source", required=True)
    parser.add_argument("--expect-git-revision", required=True)
    parser.add_argument("--deadline-seconds", type=float, default=90)
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
            args.feasibility_receipt,
        )
        output = validate_output_path(args.output, repository, inputs)
        _validate_endpoint_blob(args.expect_endpoint_blob)
        source = load_frozen_input(args.endpoint_receipt, args.expect_endpoint_blob)
        wall = load_wall_input(
            args.wall_receipt,
            args.expect_wall_blob,
            expected_source=args.expect_wall_source,
        )
        feasibility = load_feasibility_evidence(
            args.feasibility_receipt,
            args.expect_feasibility_blob,
            expected_source=args.expect_feasibility_source,
            source=source,
            wall=wall,
        )
        result = run_two_attainer_obstruction(
            source,
            wall,
            feasibility,
            deadline_seconds=args.deadline_seconds,
        )
        document = result_document(
            result,
            source=source,
            wall=wall,
            feasibility=feasibility,
            implementation_revision=revision,
            process_seconds=max(0.0, time.perf_counter() - process_started),
        )
        atomic_write_json(output, document)
    except (
        AuditError,
        ContainmentError,
        FixedPatternError,
        SixthSiteScreenError,
        TwoAttainerError,
        OSError,
        json.JSONDecodeError,
    ) as error:
        document = {
            "schema": "wall-owner-two-attainer-obstruction/v1",
            "status": "invalid",
            "outcome": "invalid",
            "process_seconds": max(0.0, time.perf_counter() - process_started),
            "error": str(error),
        }
        if output is not None:
            atomic_write_json(output, document)
    print(json.dumps(document, indent=1), flush=True)
    return 0 if document.get("status") == "complete" else 2


if __name__ == "__main__":
    raise SystemExit(main())
