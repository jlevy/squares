"""Unrelated synthetic geometry only; no scientific source or candidate loading."""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
from typing import Any
from unittest.mock import patch

import pytest

from devtools import geometric_graph_certificate as adapter
from devtools.geometric_graph_certificate import AdapterError, produce
from sqpack.field import NumberField


def square(field: NumberField, x: Fraction, y: Fraction) -> tuple:
    a, b = field.rational(x), field.rational(y)
    return ((a, b), (a + 1, b), (a + 1, b + 1), (a, b + 1))


def source(field: NumberField, entries: list[tuple[str, tuple, Fraction]]) -> dict[str, Any]:
    descriptor = field.precondition_certificate()
    return {
        "field": {
            "minimal_polynomial": descriptor["normalized_minimal_polynomial"],
            "isolating_interval": descriptor["declared_isolating_interval"],
        },
        "squares": [
            {
                "id": name,
                "vertices": [
                    [[str(c) for c in coordinate.coeffs] for coordinate in point]
                    for point in vertices
                ],
                "weight": str(weight),
            }
            for name, vertices, weight in entries
        ],
    }


def test_exact_tangency_is_a_certified_nonedge() -> None:
    field = NumberField((1, 0), (-1, 1))
    raw = source(
        field,
        [
            ("left", square(field, Fraction(0), Fraction(0)), Fraction(3, 4)),
            ("right", square(field, Fraction(1), Fraction(0)), Fraction(3, 4)),
        ],
    )
    result = produce(raw, field=field, threshold=Fraction(1), node_limit=1)
    assert result["status"] == "proved_graph_bound"
    assert result["pairs_tested"] == 1
    assert result["nonedges"] == [{"pair": [0, 1], "axis": [["1"], ["0"]]}]
    assert result["graph_certificate"]["graph"]["edges"] == []


def test_true_interior_overlap_remains_an_edge() -> None:
    field = NumberField((1, 0), (-1, 1))
    raw = source(
        field,
        [
            ("first", square(field, Fraction(0), Fraction(0)), Fraction(3, 4)),
            ("second", square(field, Fraction(1, 2), Fraction(0)), Fraction(3, 4)),
        ],
    )
    result = produce(raw, field=field, threshold=Fraction(1), node_limit=3)
    assert result["status"] == "unresolved"
    assert result["nonedges"] == []
    assert result["graph_certificate"]["status"] == "overweight_clique"
    assert result["graph_certificate"]["graph"]["edges"] == [[0, 1]]


def test_every_positive_pair_is_tested_even_when_no_pair_is_overweight() -> None:
    field = NumberField((1, 0), (-1, 1))
    raw = source(
        field,
        [
            (f"toy-{i}", square(field, Fraction(i), Fraction(0)), Fraction(1, 4))
            for i in range(3)
        ],
    )
    result = produce(raw, field=field, threshold=Fraction(1), node_limit=1)
    assert result["pairs_tested"] == 3
    assert [entry["pair"] for entry in result["nonedges"]] == [[0, 1], [0, 2], [1, 2]]
    assert result["graph_certificate"]["proof"] == {"root": 0, "nodes": [{"kind": "sum"}]}


def test_zero_omission_preserves_the_complete_original_source() -> None:
    field = NumberField((1, 0), (-1, 1))
    raw = source(
        field,
        [
            ("left", square(field, Fraction(0), Fraction(0)), Fraction(3, 4)),
            ("zero", square(field, Fraction(0), Fraction(0)), Fraction(0)),
            ("right", square(field, Fraction(1), Fraction(0)), Fraction(3, 4)),
        ],
    )
    original = deepcopy(raw)
    result = produce(raw, field=field, threshold=Fraction(1), node_limit=1)
    assert result["source"] == original
    assert raw == original
    assert result["retained_ids"] == [0, 2]
    assert result["pairs_tested"] == 1
    assert result["nonedges"][0]["pair"] == [0, 1]
    result["source"]["squares"][1]["weight"] = "1"
    assert raw == original


def test_coincident_positive_squares_are_not_deduplicated() -> None:
    field = NumberField((1, 0), (-1, 1))
    corners = square(field, Fraction(0), Fraction(0))
    raw = source(
        field, [("first", corners, Fraction(3, 4)), ("second", corners, Fraction(3, 4))]
    )
    result = produce(raw, field=field, threshold=Fraction(1), node_limit=3)
    assert result["retained_ids"] == [0, 1]
    assert result["graph_certificate"]["clique"] == {"vertices": [0, 1], "weight": "3/2"}
    assert result["status"] == "unresolved"


def test_algebraically_rotated_tangent_squares() -> None:
    field = NumberField((1, 0, -2), (1, 2))
    zero, r = field.zero, field.alpha / 2
    first = ((zero, zero), (r, r), (zero, 2 * r), (-r, r))
    second = tuple((x + r, y + r) for x, y in first)
    raw = source(
        field,
        [("rotated-first", first, Fraction(3, 4)), ("rotated-second", second, Fraction(3, 4))],
    )
    result = produce(raw, field=field, threshold=Fraction(1), node_limit=1)
    assert result["nonedges"] == [{"pair": [0, 1], "axis": [["0", "1/2"], ["0", "1/2"]]}]
    assert result["status"] == "proved_graph_bound"


def test_clockwise_cyclic_unit_vertices_are_valid() -> None:
    field = NumberField((1, 0), (-1, 1))
    corners = tuple(reversed(square(field, Fraction(0), Fraction(0))))
    raw = source(field, [("clockwise", corners, Fraction(1))])
    assert (
        produce(raw, field=field, threshold=Fraction(1), node_limit=1)["status"]
        == "proved_graph_bound"
    )


def test_arithmetic_uncertainty_retains_every_edge(monkeypatch: pytest.MonkeyPatch) -> None:
    field = NumberField((1, 0), (-1, 1))
    raw = source(
        field,
        [
            (f"toy-{i}", square(field, Fraction(i), Fraction(0)), Fraction(3, 4))
            for i in range(3)
        ],
    )

    def uncertain(*_args: object) -> Any:
        raise ArithmeticError("toy sign decision unavailable")

    monkeypatch.setattr(adapter, "_sat_axis", uncertain)
    result = produce(raw, field=field, threshold=Fraction(1), node_limit=4)
    assert result["pairs_tested"] == 3
    assert result["unknown_pairs"] == [[0, 1], [0, 2], [1, 2]]
    assert result["nonedges"] == []
    assert result["graph_certificate"]["graph"]["edges"] == result["unknown_pairs"]
    assert result["status"] == "unresolved"


@pytest.mark.parametrize("zero_axis", [True, False])
def test_invalid_separator_cannot_remove_an_edge(
    monkeypatch: pytest.MonkeyPatch, *, zero_axis: bool
) -> None:
    field = NumberField((1, 0), (-1, 1))
    raw = source(
        field,
        [
            (f"toy-{i}", square(field, Fraction(i), Fraction(0)), Fraction(3, 4))
            for i in range(2)
        ],
    )
    axis = (field.zero, field.zero if zero_axis else field.one)
    monkeypatch.setattr(adapter, "_sat_axis", lambda *_args: axis)
    result = produce(raw, field=field, threshold=Fraction(1), node_limit=3)
    assert result["unknown_pairs"] == [[0, 1]]
    assert result["nonedges"] == []
    assert result["graph_certificate"]["graph"]["edges"] == [[0, 1]]


def test_graph_node_exhaustion_does_not_truncate_pair_receipts() -> None:
    field = NumberField((1, 0), (-1, 1))
    raw = source(
        field,
        [
            (f"toy-{i}", square(field, Fraction(0), Fraction(0)), Fraction(3, 4))
            for i in range(2)
        ],
    )
    result = produce(raw, field=field, threshold=Fraction(1), node_limit=1)
    assert result["pairs_tested"] == 1
    assert result["status"] == "unresolved"
    assert result["graph_certificate"]["stop_reason"] == "node_limit"
    assert result["graph_certificate"]["proof"] is None


@pytest.mark.parametrize(
    "mutation", ["weight", "vertices", "duplicate", "field", "extra", "name"]
)
def test_malformed_source_is_refused_before_zero_omission(mutation: str) -> None:
    field = NumberField((1, 0), (-1, 1))
    raw = source(
        field,
        [
            ("positive", square(field, Fraction(0), Fraction(0)), Fraction(1)),
            ("zero", square(field, Fraction(2), Fraction(0)), Fraction(0)),
        ],
    )
    if mutation == "weight":
        raw["squares"][1]["weight"] = "-1"
    elif mutation == "vertices":
        raw["squares"][1]["vertices"][2] = raw["squares"][1]["vertices"][0]
    elif mutation == "duplicate":
        raw["squares"][1]["id"] = "positive"
    elif mutation == "field":
        raw["field"]["isolating_interval"] = ["-2", "2"]
    elif mutation == "extra":
        raw["squares"][1]["source"] = "not an admitted field"
    else:
        raw["squares"][1]["id"] = "../source"
    with pytest.raises(AdapterError):
        produce(raw, field=field, threshold=Fraction(1), node_limit=1)


@pytest.mark.parametrize(
    "coefficient", ["1e100000000", "1/0", "2/4", "\uff11", str(2**128), 0.5, True]
)
def test_bad_coordinate_rationals_are_refused(coefficient: Any) -> None:
    field = NumberField((1, 0), (-1, 1))
    raw = source(field, [("toy", square(field, Fraction(0), Fraction(0)), Fraction(1))])
    raw["squares"][0]["vertices"][0][0][0] = coefficient
    with pytest.raises(AdapterError):
        produce(raw, field=field, threshold=Fraction(1), node_limit=1)


def test_no_file_access_or_field_construction_inside_adapter() -> None:
    field = NumberField((1, 0), (-1, 1))
    raw = source(field, [("toy", square(field, Fraction(-3), Fraction(5)), Fraction(1))])
    with (
        patch("builtins.open", side_effect=AssertionError("source file access forbidden")),
        patch("io.open", side_effect=AssertionError("source file access forbidden")),
        patch.object(
            NumberField, "__init__", side_effect=AssertionError("field construction forbidden")
        ),
    ):
        result = produce(raw, field=field, threshold=Fraction(1), node_limit=1)
    assert result["status"] == "proved_graph_bound"
    assert (
        result["scope"] == "Supplied square family only; no packing or source-candidate claim."
    )


def test_empty_and_all_zero_sources_have_exact_empty_graph_semantics() -> None:
    field = NumberField((1, 0), (-1, 1))
    for entries in ([], [("zero", square(field, Fraction(0), Fraction(0)), Fraction(0))]):
        result = produce(
            source(field, entries), field=field, threshold=Fraction(0), node_limit=1
        )
        assert result["retained_ids"] == []
        assert result["pairs_tested"] == 0
        assert result["graph_certificate"]["graph"] == {
            "vertex_count": 0,
            "vertices": [],
            "edges": [],
        }


@pytest.mark.parametrize("mutation", ["bowtie", "corner-count", "dimension", "point-size"])
def test_malformed_vertex_inventory_and_nonsquares_are_refused(mutation: str) -> None:
    field = NumberField((1, 0), (-1, 1))
    raw = source(field, [("toy", square(field, Fraction(0), Fraction(0)), Fraction(1))])
    corners = raw["squares"][0]["vertices"]
    if mutation == "bowtie":
        corners[1], corners[2] = corners[2], corners[1]
    elif mutation == "corner-count":
        corners.pop()
    elif mutation == "dimension":
        corners[0][0].append("0")
    else:
        corners[0].append(["0"])
    with pytest.raises(AdapterError):
        produce(raw, field=field, threshold=Fraction(1), node_limit=1)


@pytest.mark.parametrize("limit", [0, -1, 100_001, True, 1.0])
def test_invalid_graph_budgets_are_refused_without_geometry(limit: Any) -> None:
    field = NumberField((1, 0), (-1, 1))
    with (
        patch.object(adapter, "_entries", side_effect=AssertionError("geometry forbidden")),
        pytest.raises(AdapterError),
    ):
        produce({}, field=field, threshold=Fraction(1), node_limit=limit)


def test_original_roster_cap_counts_zero_weights_too() -> None:
    field = NumberField((1, 0), (-1, 1))
    raw = source(field, [])
    raw["squares"] = [{}] * 65
    with pytest.raises(AdapterError, match="roster"):
        produce(raw, field=field, threshold=Fraction(1), node_limit=1)


def test_noncanonical_coordinate_syntax_is_rejected_before_fraction_conversion(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    field = NumberField((1, 0), (-1, 1))
    raw = source(field, [("toy", square(field, Fraction(0), Fraction(0)), Fraction(1))])
    raw["squares"][0]["vertices"][0][0][0] = "1e100000000"
    threshold = Fraction(1)
    original_new = Fraction.__new__

    def guarded_new(cls: type[Fraction], *args: Any, **kwargs: Any) -> Fraction:
        if args and args[0] == "1e100000000":
            raise AssertionError("noncanonical exponent reached rational conversion")
        return original_new(cls, *args, **kwargs)

    monkeypatch.setattr(Fraction, "__new__", guarded_new)
    with pytest.raises(AdapterError, match="ASCII"):
        produce(raw, field=field, threshold=threshold, node_limit=1)
