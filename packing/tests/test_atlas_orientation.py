"""Atlas isometries preserve the packing and its scientific source record."""

from __future__ import annotations

from copy import deepcopy
from decimal import localcontext
from fractions import Fraction
from pathlib import Path

import pytest

from devtools import build_known_best_atlas as builder
from devtools.atlas_orientation import (
    Reflection,
    orient_atlas_witness,
    reflect_escape_case,
    reflect_x_axis,
    reflect_y_axis,
    source_orientation,
)
from sqpack.witness import exact_verify, load_witness

ROOT = Path(__file__).resolve().parents[1]
SELECTED = ROOT / "witnesses/known-best/n-211.yaml"


def _decimal_pair() -> dict:
    return {
        "id": "W-test-pair",
        "n": 2,
        "side": "3.000000000000000001",
        "square_size": "1",
        "representation": "center-angle",
        "scalar": {"kind": "decimal"},
        "coordinates": {
            "origin": "lower-left",
            "axes": "x-right-y-up",
            "angle_unit": "radians",
        },
        "squares": [
            {"id": 1, "center": ["0.75", "0.75"], "angle": "0.2"},
            {"id": 2, "center": ["2.25", "2.25"], "angle": "0.0"},
        ],
        "claim": {
            "coordinate_provenance": "reported",
            "method": "numerical-multiprecision",
            "precision": {"decimal_digits": 120, "rounding": "nearest"},
            "tolerance": "1e-12",
        },
        "source": {"path": "tests/pair", "retrieved": "2026-09-16"},
    }


@pytest.mark.parametrize("component", [0, 1])
def test_decimal_reflection_is_exact_independent_of_the_decimal_context(component: int) -> None:
    reflect = reflect_y_axis if component == 0 else reflect_x_axis
    source = _decimal_pair()
    before = deepcopy(source)
    with localcontext() as context:
        context.prec = 4
        reflected = reflect(source)
    assert source == before
    assert reflected["side"] == source["side"]
    assert reflected["source"] == source["source"]
    assert reflected["claim"] == source["claim"]
    for original, image in zip(source["squares"], reflected["squares"], strict=True):
        assert image["id"] == original["id"]
        assert image["center"][1 - component] == original["center"][1 - component]
        assert Fraction(image["center"][component]) == Fraction(source["side"]) - Fraction(
            original["center"][component]
        )
        assert Fraction(image["angle"]) == -Fraction(original["angle"])
    assert reflected["squares"][1]["angle"] == "0"
    restored = reflect(reflected)
    for original, image in zip(source["squares"], restored["squares"], strict=True):
        assert [Fraction(value) for value in image["center"]] == [
            Fraction(value) for value in original["center"]
        ]
        assert Fraction(image["angle"]) == Fraction(original["angle"])


@pytest.mark.parametrize("component", [0, 1])
def test_rational_reflection_restores_ccw_winding_and_exact_containment(component: int) -> None:
    reflect = reflect_y_axis if component == 0 else reflect_x_axis
    source = {
        "id": "W-rational-pair",
        "n": 2,
        "side": "2",
        "square_size": "1",
        "representation": "corners",
        "scalar": {"kind": "rational"},
        "coordinates": {
            "origin": "lower-left",
            "axes": "x-right-y-up",
            "angle_unit": "not-applicable",
        },
        "squares": [
            {"id": 1, "corners": [["0", "0"], ["1", "0"], ["1", "1"], ["0", "1"]]},
            {"id": 2, "corners": [["1", "0"], ["2", "0"], ["2", "1"], ["1", "1"]]},
        ],
        "claim": {"coordinate_provenance": "verified", "method": "exact-algebraic"},
    }
    image = reflect(source)
    assert image["squares"][0]["corners"] == (
        [["2", "1"], ["1", "1"], ["1", "0"], ["2", "0"]]
        if component == 0
        else [["0", "1"], ["1", "1"], ["1", "2"], ["0", "2"]]
    )
    verdict, report = exact_verify(image)
    assert report.valid
    assert verdict["verification_passed"]
    assert reflect(image) == source


def test_only_the_registered_atlas_case_is_oriented() -> None:
    source = _decimal_pair()
    assert orient_atlas_witness(source) is source


def test_n211_orientation_keeps_source_dates_bounds_and_feasibility() -> None:
    source = source_orientation(load_witness(SELECTED))
    image = orient_atlas_witness(source)
    assert image["n"] == 211
    for key in ("id", "side", "square_size", "scalar", "coordinates", "source", "claim"):
        assert image[key] == source[key]
    assert image["certificate"]["result"]["check_passed"]
    assert image["certificate"]["result"]["pairs_tested"] == 22155
    transform = image["certificate"]["geometry_transform"]
    assert transform["operation"] == "reflect-y-axis"
    assert transform["reference_n"] == 241
    assert (
        transform["parent"]["path"]
        == "packing/resources/web/de-winter-square-packing-211-2026-09-16/facts/n-211.yaml"
    )
    assert (
        transform["parent"]["atlas_receipt_before_transform"] == source["certificate"]["result"]
    )
    assert orient_atlas_witness(image) is image
    restored = source_orientation(image)
    assert restored["certificate"] == source["certificate"]
    for original, reflected in zip(source["squares"], image["squares"], strict=True):
        assert Fraction(reflected["center"][1]) == Fraction(original["center"][1])
        assert Fraction(reflected["center"][0]) == Fraction(source["side"]) - Fraction(
            original["center"][0]
        )
        assert Fraction(reflected["angle"]) == -Fraction(original["angle"])


def test_correcting_a_legacy_vertical_flip_rebases_on_the_original_parent() -> None:
    source = source_orientation(load_witness(SELECTED))
    corrected = orient_atlas_witness(source)
    legacy = reflect_x_axis(source)
    legacy["certificate"]["geometry_transform"] = deepcopy(
        corrected["certificate"]["geometry_transform"]
    )
    legacy["certificate"]["geometry_transform"].update(
        operation="reflect-x-axis",
        reference_n=182,
        map={"x": "x", "y": "side - y", "angle": "-angle"},
    )
    migrated = orient_atlas_witness(legacy)
    for expected, actual in zip(corrected["squares"], migrated["squares"], strict=True):
        assert expected["id"] == actual["id"]
        assert [Fraction(value) for value in expected["center"]] == [
            Fraction(value) for value in actual["center"]
        ]
        assert Fraction(expected["angle"]) == Fraction(actual["angle"])
    assert migrated["certificate"] == corrected["certificate"]
    assert orient_atlas_witness(migrated) is migrated


@pytest.mark.parametrize(
    ("field", "value"), [("origin", "container-center"), ("axes", "x-right-y-down")]
)
def test_an_unhandled_coordinate_convention_is_refused(field: str, value: str) -> None:
    source = _decimal_pair()
    source["coordinates"][field] = value
    with pytest.raises(ValueError, match=r"lower-left.*y-up"):
        reflect_x_axis(source)


@pytest.mark.parametrize("operation", ["reflect-x-axis", "reflect-y-axis"])
def test_escape_reflection_preserves_ids_order_distances_and_tolerance_groups(
    operation: Reflection,
) -> None:
    case = {
        "n": 211,
        "movable_square_count": 2,
        "movable_squares_by_tolerance": {"1e-12": [2, 7]},
        "movable_squares": [
            {
                "square_index": index,
                "witness_square_id": index + 1,
                "direction": {"x": "0.6", "y": y},
                "slide_distance": "0.025",
                "active_blockers": {"square_indices": [1, 4]},
            }
            for index, y in ((2, "0.8"), (7, "-0.8"))
        ],
    }
    before = deepcopy(case)
    image = reflect_escape_case(case, operation=operation)
    assert case == before
    assert [motion["direction"] for motion in image["movable_squares"]] == (
        [{"x": "0.6", "y": "-0.8"}, {"x": "0.6", "y": "0.8"}]
        if operation == "reflect-x-axis"
        else [{"x": "-0.6", "y": "0.8"}, {"x": "-0.6", "y": "-0.8"}]
    )
    assert reflect_escape_case(image, operation=operation) == case


def test_selected_atlas_cli_dispatches_the_existing_scoped_producer(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = []
    monkeypatch.setattr(builder, "update_selected", lambda ns, jobs: calls.append((ns, jobs)))
    monkeypatch.setattr(
        builder, "update", lambda _jobs: pytest.fail("scoped refresh rebuilt the corpus")
    )
    assert builder.main(["--update", "--n", "211", "--jobs", "1"]) == 0
    assert calls == [([211], 1)]
    with pytest.raises(SystemExit, match="--n narrows --update"):
        builder.main(["--check", "--n", "211", "--jobs", "1"])


@pytest.mark.parametrize("field", ["key", "path"])
def test_n211_source_switch_cannot_inherit_the_registered_packet_lineage(field: str) -> None:
    source = source_orientation(load_witness(SELECTED))
    source["source"][field] = "another-published-parent"
    before = deepcopy(source)
    with pytest.raises(ValueError, match=r"registered atlas orientation.*parent"):
        orient_atlas_witness(source)
    assert source == before
