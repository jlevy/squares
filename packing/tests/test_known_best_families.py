#!/usr/bin/env python3
"""Checks for the known-best family census: its detectors on fixtures, and its record.

The full census takes about nine seconds, well past the quick lane's two-second marking
threshold, so the retained-record test recomputes a subset of entries geometrically and
rebuilds every summary and the detector from the retained entries. The whole document is
compared byte for byte by `python -m devtools.classify_known_best_families --check`.
"""

from __future__ import annotations

import itertools
import json
import math
from fractions import Fraction
from typing import Any

import pytest

from devtools import classify_known_best_families as families
from devtools.classify_known_best_families import Geometry, Pose, json_differences

HALF_ROOT_TWO = math.sqrt(2.0) / 2


def _grid(columns: int, rows: int) -> tuple[Pose, ...]:
    return tuple(Pose(x + 0.5, y + 0.5, 0.0) for y in range(rows) for x in range(columns))


def _round_trip(value: Any) -> Any:
    return json.loads(json.dumps(value, sort_keys=True))


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (24, {"m": 4, "r": 8, "k": 5, "d": -1, "ceil_sqrt": 5}),
        (25, {"m": 5, "r": 0, "k": 5, "d": 0, "ceil_sqrt": 5}),
        (26, {"m": 5, "r": 1, "k": 5, "d": 1, "ceil_sqrt": 6}),
        (20, {"m": 4, "r": 4, "k": 4, "d": 4, "ceil_sqrt": 5}),
        (21, {"m": 4, "r": 5, "k": 5, "d": -4, "ceil_sqrt": 5}),
    ],
)
def test_square_indices_report_floor_and_nearest_conventions(
    n: int, expected: dict[str, int]
) -> None:
    assert families.square_indices(n) == expected


def test_small_library_is_unambiguous_at_the_side_tolerance() -> None:
    values = [form[0] for form in families.closed_form_library()]
    assert len(values) == 45 * 45
    assert min(b - a for a, b in itertools.pairwise(values)) > 1e-6


def test_closed_forms_cover_both_tiers_and_refuse_a_generic_side() -> None:
    goebel = families.closed_form_record(2 + HALF_ROOT_TWO, 2)
    assert goebel is not None
    assert (goebel["tier"], goebel["kind"], goebel["a"], goebel["b"]) == (
        "small",
        "sqrt2",
        "0",
        "1/2",
    )
    assert goebel["side_expression"] == "2 + 1/2*sqrt(2)"

    integer = families.closed_form_record(3.0, 2)
    assert integer is not None
    assert (integer["tier"], integer["kind"], integer["side_expression"]) == (
        "small",
        "integer",
        "3",
    )

    three_four_five = families.closed_form_record(53 / 7, 7)
    assert three_four_five is not None
    assert (three_four_five["tier"], three_four_five["kind"]) == ("wide", "rational")
    assert three_four_five["side_expression"] == "53/7"

    diamond = families.closed_form_record(8 + 11 * HALF_ROOT_TWO, 15)
    assert diamond is not None
    assert (diamond["tier"], diamond["side_expression"]) == ("wide", "8 + 11/2*sqrt(2)")
    assert (diamond["a"], diamond["b"]) == ("-7", "11/2")

    assert families.closed_form_record(3.877083590022810, 3) is None


def test_two_by_two_grid_is_one_filled_corner_lattice_with_full_symmetry() -> None:
    grid = Geometry(4, 2.0, _grid(2, 2))
    structure = families.axis_structure(grid)
    assert structure["largest_component"] == {
        "size": 4,
        "rows": 2,
        "columns": 2,
        "filled_rectangle": True,
    }
    assert structure["component_count"] == 1
    assert structure["corner_lattice"]["any"] == 4
    assert structure["corner_lattice"]["best"] == 4
    assert families.symmetry(grid, 1e-6, 1e-6)["group"] == "D4"
    profile = families.angle_profile(grid.poses)
    assert profile["axis_aligned"] == {"tight": 4, "loose": 4}
    assert profile["class_count"] == {"tight": 1, "loose": 1}


def test_corner_lattice_is_measured_from_each_corner_of_a_non_integer_side() -> None:
    side = 2 + HALF_ROOT_TWO
    corners = (
        Pose(0.5, 0.5, 0.0),
        Pose(side - 0.5, 0.5, 0.0),
        Pose(0.5, side - 0.5, 0.0),
        Pose(side - 0.5, side - 0.5, 0.0),
        Pose(side / 2, side / 2, 45.0),
    )
    lattice = families.axis_structure(Geometry(5, side, corners))["corner_lattice"]
    assert lattice == {
        "lower-left": 1,
        "lower-right": 1,
        "upper-left": 1,
        "upper-right": 1,
        "any": 4,
        "best": 1,
    }
    assert families.symmetry(Geometry(5, side, corners), 1e-6, 1e-6)["group"] == "D4"
    assert families.angle_profile(corners)["forty_five"] == {"tight": 1, "loose": 1}


@pytest.mark.parametrize(
    ("angle", "group"),
    [(0.0, "D4"), (45.0, "D4"), (30.0, "C4")],
)
def test_reflections_negate_a_tilt_so_only_rotations_keep_an_oblique_square(
    angle: float, group: str
) -> None:
    lone = Geometry(1, 2.0, (Pose(1.0, 1.0, angle),))
    assert families.symmetry(lone, 1e-6, 1e-6)["group"] == group


def test_an_l_tromino_is_mirror_symmetric_about_the_main_diagonal() -> None:
    tromino = Geometry(3, 2.0, (Pose(0.5, 0.5, 0.0), Pose(1.5, 0.5, 0.0), Pose(0.5, 1.5, 0.0)))
    assert families.symmetry(tromino, 1e-6, 1e-6) == {
        "group": "D1-diagonal",
        "elements": ["identity", "flip-diagonal"],
    }


def test_angle_classes_join_across_the_ninety_degree_seam() -> None:
    poses = tuple(
        Pose(float(index), 0.5, angle)
        for index, angle in enumerate((0.0, 89.9999999, 30.0, 30.2, 60.0))
    )
    profile = families.angle_profile(poses)
    assert profile["class_count"] == {"tight": 4, "loose": 3}
    assert profile["axis_aligned"] == {"tight": 2, "loose": 2}
    assert [item["count"] for item in profile["classes_loose"]] == [2, 2, 1]
    assert [item["angle_degrees"] for item in profile["classes_loose"]] == [0.0, 30.1, 60.0]
    assert families.tilt_signature(profile) == profile["classes_loose"][1:]


def test_shared_structure_finds_an_embedding_and_a_corner_anchor() -> None:
    tromino = Geometry(3, 2.0, (Pose(0.5, 0.5, 0.0), Pose(1.5, 0.5, 0.0), Pose(0.5, 1.5, 0.0)))
    grown = families.shared_structure(tromino, Geometry(4, 2.0, _grid(2, 2)))
    assert (grown["matched"], grown["embeds"]) == (3, True)

    single = Geometry(1, 1.0, (Pose(0.5, 0.5, 0.0),))
    far_corner = Geometry(1, 2.0, (Pose(1.5, 1.5, 0.0),))
    anchored = families.shared_structure(single, far_corner)
    assert (anchored["matched"], anchored["anchor"], anchored["transform"]) == (
        1,
        "upper-right",
        "identity",
    )


def test_tilted_layout_reads_a_diagonal_band() -> None:
    band = tuple(Pose(0.5 + step, 0.5 + step, 30.0) for step in range(6))
    layout = families.tilted_layout(band + _grid(1, 1))
    assert layout["count"] == 6
    assert layout["principal_direction_degrees"] == 45.0
    assert layout["elongation"] is None


def test_l_construction_follows_the_definition_on_synthetic_sides() -> None:
    sides = {
        1: 1.0,
        2: 2.0,
        3: 2.0,
        4: 2.0,
        5: 2 + HALF_ROOT_TWO,
        6: 3.0,
        7: 3.0,
        8: 3.0,
        9: 3.0,
        10: 3 + HALF_ROOT_TWO,
    }
    assert families.l_step(2.9999999999) == 7
    assert families.l_parent(10, sides) == 5
    assert families.l_parent(9, sides) == 4
    assert families.l_chain(9, sides) == (1, 2)
    assert families.l_parent(5, sides) is None
    assert families.l_bound(5, sides) is None
    improved = {**sides, 10: 3.6}
    assert families.l_parent(10, improved) is None
    beaten = families.l_bound(10, improved)
    assert beaten is not None
    assert beaten["from"] == 5
    assert beaten["margin"] == pytest.approx(HALF_ROOT_TWO - 0.6, abs=1e-12)


def test_witness_projection_folds_degrees_radians_and_corners() -> None:
    def witness(squares: list[dict[str, Any]], representation: str, unit: str) -> dict:
        return {
            "n": len(squares),
            "side": "2",
            "representation": representation,
            "scalar": {"kind": "decimal"},
            "coordinates": {"origin": "lower-left", "axes": "x-right-y-up", "angle_unit": unit},
            "squares": squares,
        }

    degrees = families.witness_geometry(
        witness([{"id": 1, "center": ["1", "1"], "angle": "120"}], "center-angle", "degrees")
    )
    assert degrees.poses[0].angle == pytest.approx(30.0, abs=1e-12)
    radians = families.witness_geometry(
        witness(
            [{"id": 1, "center": ["1", "1"], "angle": str(-math.pi / 6)}],
            "center-angle",
            "radians",
        )
    )
    assert radians.poses[0].angle == pytest.approx(60.0, abs=1e-9)
    diamond = families.witness_geometry(
        witness(
            [
                {
                    "id": 1,
                    "corners": [
                        ["1", str(1 - HALF_ROOT_TWO)],
                        [str(1 + HALF_ROOT_TWO), "1"],
                        ["1", str(1 + HALF_ROOT_TWO)],
                        [str(1 - HALF_ROOT_TWO), "1"],
                    ],
                }
            ],
            "corners",
            "not-applicable",
        )
    )
    pose = diamond.poses[0]
    assert (pose.x, pose.y) == pytest.approx((1.0, 1.0), abs=1e-12)
    assert pose.angle == pytest.approx(45.0, abs=1e-9)


@pytest.fixture(scope="module")
def retained() -> dict[str, Any]:
    return json.loads(families.OUTPUT.read_text(encoding="utf-8"))


def test_retained_summary_and_detector_rebuild_from_the_retained_entries(
    retained: dict[str, Any],
) -> None:
    assert len(retained["entries"]) == len(families.manifest_entries())
    assert _round_trip(families.expected_document(retained["entries"])) == retained


def test_retained_entries_match_a_recomputed_subset(retained: dict[str, Any]) -> None:
    """Recompute 1, 5, 82 (an L child of 65), 233, and 301 from their witnesses."""
    by_n = {entry["n"]: entry for entry in retained["entries"]}
    for record in families.build_records([1, 5, 82, 233, 301]):
        assert _round_trip(record) == by_n[record["n"]]


def test_row_summary_keeps_the_fields_the_asymptotics_lane_reads(
    retained: dict[str, Any],
) -> None:
    rows = retained["summary"]["rows"]
    assert [row["k"] for row in rows] == list(range(1, 19))
    assert {
        "grid_held_width",
        "grid_held_smallest_n",
        "grid_held_contiguous_to_k_squared",
        "closed_form_count",
        "tilted_n_count",
    } <= set(rows[0])
    assert sum(row["grid_held_width"] for row in rows) == sum(
        entry["integer_side"] for entry in retained["entries"]
    )


@pytest.mark.parametrize(("k", "offset"), [(5, 2), (7, 3), (12, 5), (17, 7)])
def test_goebel_offset_takes_the_floor_exactly(k: int, offset: int) -> None:
    assert families.goebel_offset(k) == offset


def test_small_library_constants_are_what_the_detector_declares() -> None:
    assert families.CLOSED_FORM_DENOMINATORS == (1, 2, 3, 4)
    assert families.CLOSED_FORM_NUMERATOR_BOUND == 8
    assert Fraction(1, 2) in {form[2] for form in families.closed_form_library()}


def test_a_stale_census_names_the_paths_that_moved() -> None:
    retained = {"a": 1, "b": [1, 2], "c": {"d": 0.5}}
    fresh = {"a": 2, "b": [1], "c": {"d": 0.5, "e": True}}
    assert list(json_differences(retained, fresh)) == [
        "$.a: retained 1, fresh 2",
        "$.b: retained 2 items, fresh 1",
        "$.c.e: present only in fresh",
    ]
