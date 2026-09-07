"""Synthetic square/graph controls; no adapter producer or scientific source access."""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
from itertools import combinations
from typing import Any
from unittest.mock import patch

import pytest

from devtools import check_geometric_graph_certificate as reader
from sqpack.field import NumberField


@pytest.fixture
def field() -> NumberField:
    return NumberField([1, 0, -2], (1, 2))


def point(x: Fraction | int, y: Fraction | int) -> list[list[str]]:
    return [[str(Fraction(x)), "0"], [str(Fraction(y)), "0"]]


def square(identity: str, x: Fraction | int, y: Fraction | int, weight: str) -> dict[str, Any]:
    return {
        "id": identity,
        "vertices": [point(x, y), point(x + 1, y), point(x + 1, y + 1), point(x, y + 1)],
        "weight": weight,
    }


def source(*entries: dict[str, Any]) -> dict[str, Any]:
    return {
        "field": {"minimal_polynomial": ["1", "0", "-2"], "isolating_interval": ["1", "2"]},
        "squares": list(entries),
    }


def packet(
    raw_source: dict[str, Any],
    *,
    nonedges: list[dict[str, Any]] | None = None,
    leaf: dict[str, Any] | None = None,
    threshold: str = "1",
) -> dict[str, Any]:
    retained = [
        i for i, entry in enumerate(raw_source["squares"]) if Fraction(entry["weight"]) > 0
    ]
    nonedges = nonedges or []
    removed = {tuple(entry["pair"]) for entry in nonedges}
    graph = {
        "vertex_count": len(retained),
        "vertices": [
            {"id": i, "weight": raw_source["squares"][j]["weight"]}
            for i, j in enumerate(retained)
        ],
        "edges": [
            list(pair) for pair in combinations(range(len(retained)), 2) if pair not in removed
        ],
    }
    return {
        "version": 1,
        "kind": reader.KIND,
        "source": deepcopy(raw_source),
        "retained_ids": retained,
        "pairs_tested": len(retained) * (len(retained) - 1) // 2,
        "nonedges": nonedges,
        "unknown_pairs": [],
        "graph_certificate": {
            "version": 1,
            "kind": "rational-weighted-clique-bound",
            "graph": graph,
            "threshold": threshold,
            "node_limit": 10,
            "nodes_visited": 1,
            "status": "proved_upper_bound",
            "proof": {"root": 0, "nodes": [leaf or {"kind": "sum"}]},
            "clique": None,
            "stop_reason": "complete",
            "scope": "Weighted graph only; no geometric intersection or packing claim.",
        },
        "status": "proved_graph_bound",
        "scope": reader.SCOPE,
    }


def separated_packet(offset: Fraction | int = 1) -> tuple[dict[str, Any], dict[str, Any]]:
    raw_source = source(square("left", 0, 0, "1"), square("right", offset, 0, "1"))
    raw = packet(
        raw_source,
        nonedges=[{"pair": [0, 1], "axis": point(1, 0)}],
        leaf={"kind": "coloring", "classes": [[0, 1]]},
    )
    return raw_source, raw


@pytest.mark.parametrize("offset", [1, 2, Fraction(17, 16)])
def test_contact_and_strict_separation_prove_plane_depth(
    field: NumberField, offset: Fraction | int
) -> None:
    raw_source, raw = separated_packet(offset)
    result = reader.check_packet(
        raw, expected_source=raw_source, field=field, threshold=Fraction(1)
    )
    assert result["status"] == "verified_depth_bound"
    assert result["bound_proved"] is True
    assert result["projection_comparisons_checked"] == 16
    assert result["pairs_accounted_for"] == 1
    assert result["nonedges_verified"] == 1
    assert result["scope"] == reader.SCOPE


def test_all_sixteen_cross_projections_are_independently_checked(
    field: NumberField, monkeypatch: pytest.MonkeyPatch
) -> None:
    raw_source, raw = separated_packet()
    original = field.sign
    calls = []

    def counted(value):
        calls.append(value)
        return original(value)

    monkeypatch.setattr(field, "sign", counted)
    reader.check_packet(raw, expected_source=raw_source, field=field, threshold=Fraction(1))
    assert len(calls) == 16


def test_corner_contact_and_reversed_signed_axis(field: NumberField) -> None:
    raw_source = source(square("north-east", 1, 1, "1"), square("origin", 0, 0, "1"))
    raw = packet(
        raw_source,
        nonedges=[{"pair": [0, 1], "axis": point(-1, 0)}],
        leaf={"kind": "coloring", "classes": [[0, 1]]},
    )
    assert reader.check_packet(
        raw, expected_source=raw_source, field=field, threshold=Fraction(1)
    )["bound_proved"]


@pytest.mark.parametrize("offset", [0, Fraction(15, 16)])
def test_overlap_never_justifies_a_nonedge(field: NumberField, offset: Fraction | int) -> None:
    raw_source, raw = separated_packet(offset)
    with pytest.raises(reader.GuardError, match="projection"):
        reader.check_packet(raw, expected_source=raw_source, field=field, threshold=Fraction(1))


@pytest.mark.parametrize("axis", [point(0, 0), point(-1, 0), point(0, 1)])
def test_zero_and_wrong_axes_refuse(field: NumberField, axis: list[list[str]]) -> None:
    raw_source, raw = separated_packet()
    raw["nonedges"][0]["axis"] = axis
    with pytest.raises(reader.GuardError, match="axis"):
        reader.check_packet(raw, expected_source=raw_source, field=field, threshold=Fraction(1))


def test_zero_weight_source_is_bound_before_omission_and_never_deduplicated(
    field: NumberField,
) -> None:
    raw_source = source(
        square("first", 0, 0, "1/2"), square("zero", 4, 4, "0"), square("copy", 0, 0, "1/2")
    )
    raw = packet(raw_source)
    result = reader.check_packet(
        raw, expected_source=raw_source, field=field, threshold=Fraction(1)
    )
    assert result["source_squares_checked"] == 3
    assert result["retained_ids"] == [0, 2]
    assert result["pairs_accounted_for"] == 1
    changed = deepcopy(raw)
    changed["source"]["squares"][1]["vertices"] = square("ignored", 5, 5, "0")["vertices"]
    with pytest.raises(reader.GuardError, match="full caller-bound"):
        reader.check_packet(
            changed, expected_source=raw_source, field=field, threshold=Fraction(1)
        )
    changed = deepcopy(raw)
    changed["retained_ids"] = [0]
    with pytest.raises(reader.GuardError, match="retained ids"):
        reader.check_packet(
            changed, expected_source=raw_source, field=field, threshold=Fraction(1)
        )


@pytest.mark.parametrize("mutation", ["id", "weight", "vertices", "field", "missing", "order"])
def test_entire_caller_source_identity_is_required(field: NumberField, mutation: str) -> None:
    raw_source, raw = separated_packet()
    if mutation == "field":
        raw["source"]["field"]["isolating_interval"][0] = "0"
    elif mutation == "missing":
        raw["source"]["squares"].pop()
    elif mutation == "order":
        raw["source"]["squares"].reverse()
    elif mutation == "vertices":
        raw["source"]["squares"][0][mutation][0] = point(-1, 0)
    else:
        raw["source"]["squares"][0][mutation] = "changed"
    with pytest.raises(reader.GuardError, match="full caller-bound"):
        reader.check_packet(raw, expected_source=raw_source, field=field, threshold=Fraction(1))


@pytest.mark.parametrize("mutation", ["nonunit", "backtrack", "bowtie", "zero-degenerate"])
def test_shapes_are_checked_including_omitted_zero_weights(
    field: NumberField, mutation: str
) -> None:
    entry = square("shape", 0, 0, "0" if mutation == "zero-degenerate" else "1")
    if mutation == "nonunit":
        entry["vertices"][1] = point(2, 0)
    elif mutation in {"backtrack", "zero-degenerate"}:
        entry["vertices"][2] = point(0, 0)
    else:
        entry["vertices"][1], entry["vertices"][2] = entry["vertices"][2], entry["vertices"][1]
    raw_source = source(entry)
    with pytest.raises(reader.GuardError, match="source polygon"):
        reader.check_packet(
            packet(raw_source), expected_source=raw_source, field=field, threshold=Fraction(1)
        )


def test_clockwise_order_and_algebraic_unit_square_are_valid(field: NumberField) -> None:
    c = field.alpha / 2
    p = field.rational(3), field.rational(5)
    u, v = (c, c), (-c, c)
    points = [
        p,
        (p[0] + u[0], p[1] + u[1]),
        (p[0] + u[0] + v[0], p[1] + u[1] + v[1]),
        (p[0] + v[0], p[1] + v[1]),
    ]
    entry = {
        "id": "algebraic",
        "weight": "1",
        "vertices": [
            [[str(coefficient) for coefficient in coordinate.coeffs] for coordinate in vertex]
            for vertex in reversed(points)
        ],
    }
    raw_source = source(entry)
    assert reader.check_packet(
        packet(raw_source), expected_source=raw_source, field=field, threshold=Fraction(1)
    )["bound_proved"]


@pytest.mark.parametrize(
    "mutation", ["missing-receipt", "extra-edge", "weight", "positive-omission"]
)
def test_graph_must_equal_all_pairs_except_verified_nonedges(
    field: NumberField, mutation: str
) -> None:
    raw_source, raw = separated_packet()
    graph = raw["graph_certificate"]["graph"]
    if mutation == "missing-receipt":
        raw["nonedges"] = []
    elif mutation == "extra-edge":
        graph["edges"] = [[0, 1]]
    elif mutation == "weight":
        graph["vertices"][0]["weight"] = "0"
    else:
        raw["retained_ids"] = [0]
    with pytest.raises(reader.GuardError):
        reader.check_packet(raw, expected_source=raw_source, field=field, threshold=Fraction(1))


@pytest.mark.parametrize(
    "mutation", ["duplicate", "dangling", "reversed", "bool", "unknown-nonedge", "count"]
)
def test_pair_inventories_are_closed_and_exact(field: NumberField, mutation: str) -> None:
    raw_source, raw = separated_packet()
    if mutation == "duplicate":
        raw["nonedges"].append(deepcopy(raw["nonedges"][0]))
    elif mutation == "unknown-nonedge":
        raw["unknown_pairs"] = [[0, 1]]
    elif mutation == "count":
        raw["pairs_tested"] = True
    else:
        raw["nonedges"][0]["pair"] = {
            "dangling": [0, 2],
            "reversed": [1, 0],
            "bool": [False, 1],
        }[mutation]
    with pytest.raises(reader.GuardError):
        reader.check_packet(raw, expected_source=raw_source, field=field, threshold=Fraction(1))


def test_unknown_pairs_stay_edges_and_can_still_have_a_complete_bound(
    field: NumberField,
) -> None:
    raw_source = source(square("one", 0, 0, "1/3"), square("two", 0, 0, "1/3"))
    raw = packet(raw_source)
    raw["unknown_pairs"] = [[0, 1]]
    result = reader.check_packet(
        raw, expected_source=raw_source, field=field, threshold=Fraction(1)
    )
    assert result["bound_proved"] is True
    assert result["nonedges_verified"] == 0
    assert result["graph_verification"]["graph"]["edges"] == [[0, 1]]


@pytest.mark.parametrize("status", ["overweight_clique", "unresolved"])
def test_graph_nonsuccess_never_becomes_depth_or_geometric_witness(
    field: NumberField, status: str
) -> None:
    raw_source = source(square("one", 0, 0, "3/5"), square("two", 0, 0, "3/5"))
    raw = packet(raw_source)
    graph = raw["graph_certificate"]
    graph["status"] = status
    graph["proof"] = None
    graph["stop_reason"] = status if status == "overweight_clique" else "node_limit"
    graph["node_limit"] = 1
    graph["clique"] = (
        {"vertices": [0, 1], "weight": "6/5"} if status == "overweight_clique" else None
    )
    raw["status"] = "unresolved"
    result = reader.check_packet(
        raw, expected_source=raw_source, field=field, threshold=Fraction(1)
    )
    assert result["status"] == "unresolved"
    assert result["bound_proved"] is False
    raw["status"] = "proved_graph_bound"
    with pytest.raises(reader.GuardError, match="adapter status"):
        reader.check_packet(raw, expected_source=raw_source, field=field, threshold=Fraction(1))


def test_incomplete_graph_proof_and_wrong_threshold_refuse(field: NumberField) -> None:
    raw_source, raw = separated_packet()
    raw["graph_certificate"]["proof"]["nodes"] = []
    with pytest.raises(reader.GuardError, match="graph certificate"):
        reader.check_packet(raw, expected_source=raw_source, field=field, threshold=Fraction(1))
    raw_source, raw = separated_packet()
    with pytest.raises(reader.GuardError, match="graph certificate"):
        reader.check_packet(raw, expected_source=raw_source, field=field, threshold=Fraction(2))


@pytest.mark.parametrize("raw", ["1e100000000", "1.0", "+1", "1_0", "\u0661", "1/0"])
def test_noncanonical_rationals_never_reach_conversion(
    field: NumberField, monkeypatch: pytest.MonkeyPatch, raw: str
) -> None:
    raw_source, certificate = separated_packet()
    raw_source["field"]["minimal_polynomial"][0] = raw
    certificate["source"] = deepcopy(raw_source)
    threshold = Fraction(1)

    def forbidden(*_args: object, **_kwargs: object) -> Fraction:
        raise AssertionError("forbidden conversion")

    monkeypatch.setattr(reader.Fraction, "__new__", forbidden)
    with pytest.raises(reader.GuardError, match="canonical"):
        reader.check_packet(
            certificate, expected_source=raw_source, field=field, threshold=threshold
        )


@pytest.mark.parametrize(
    "value", [True, 1.0, "2/4", "1" * 129, str(2**128), str(Fraction(1, 2**128))]
)
def test_coordinate_admission_is_exact_and_bounded(field: NumberField, value: Any) -> None:
    raw_source = source(square("one", 0, 0, "1"))
    raw_source["squares"][0]["vertices"][0][0][0] = value
    with pytest.raises(reader.GuardError, match="rational"):
        reader.check_packet(
            packet(raw_source), expected_source=raw_source, field=field, threshold=Fraction(1)
        )


@pytest.mark.parametrize(
    "mutation",
    [
        "coordinate-length",
        "negative-weight",
        "duplicate-id",
        "bad-id",
        "embedding",
        "extra-key",
    ],
)
def test_source_admission_guards(field: NumberField, mutation: str) -> None:
    raw_source, raw = separated_packet()
    if mutation == "coordinate-length":
        raw_source["squares"][0]["vertices"][0][0] = ["0"]
    elif mutation == "negative-weight":
        raw_source["squares"][0]["weight"] = "-1"
    elif mutation == "duplicate-id":
        raw_source["squares"][1]["id"] = "left"
    elif mutation == "bad-id":
        raw_source["squares"][0]["id"] = "not an admitted id"
    elif mutation == "embedding":
        raw_source["field"]["isolating_interval"] = ["-2", "-1"]
    else:
        raw_source["squares"][0]["target"] = "forbidden"
    raw["source"] = deepcopy(raw_source)
    with pytest.raises(reader.GuardError):
        reader.check_packet(raw, expected_source=raw_source, field=field, threshold=Fraction(1))


@pytest.mark.parametrize("value", [str(2**257), "1" * 201, True, "1e100000000"])
def test_axis_coefficients_are_bounded_before_arithmetic(
    field: NumberField, value: Any
) -> None:
    raw_source, raw = separated_packet()
    raw["nonedges"][0]["axis"][0][0] = value
    with pytest.raises(reader.GuardError, match="rational"):
        reader.check_packet(raw, expected_source=raw_source, field=field, threshold=Fraction(1))


@pytest.mark.parametrize(
    "claim",
    [
        {"status": "verified_upper_bound", "bound_proved": False},
        {"status": "verified_overweight_clique", "bound_proved": True},
    ],
)
def test_untrusted_graph_status_alone_is_not_accepted(
    field: NumberField, monkeypatch: pytest.MonkeyPatch, claim: dict[str, Any]
) -> None:
    raw_source, raw = separated_packet()

    def misleading(*_args: object, **_kwargs: object) -> dict[str, Any]:
        return claim

    monkeypatch.setattr(reader.graph_reader, "check_packet", misleading)
    with pytest.raises(reader.GuardError, match="adapter status"):
        reader.check_packet(raw, expected_source=raw_source, field=field, threshold=Fraction(1))


def test_pair_order_and_unknown_duplicates_refuse_within_length_cap(field: NumberField) -> None:
    raw_source = source(*(square(f"s{i}", i * 2, 0, "1/4") for i in range(3)))
    raw = packet(raw_source)
    for unknown in ([[0, 1], [0, 1]], [[1, 2], [0, 1]], [[0, 3]]):
        raw["unknown_pairs"] = unknown
        with pytest.raises(reader.GuardError):
            reader.check_packet(
                raw, expected_source=raw_source, field=field, threshold=Fraction(1)
            )
    raw["unknown_pairs"] = []
    for pairs in ([[0, 1], [0, 1]], [[1, 2], [0, 1]]):
        raw["nonedges"] = [{"pair": pair, "axis": point(1, 0)} for pair in pairs]
        with pytest.raises(reader.GuardError, match="lexicographically"):
            reader.check_packet(
                raw, expected_source=raw_source, field=field, threshold=Fraction(1)
            )


def test_four_light_coincident_squares_do_not_get_a_depth_bound(field: NumberField) -> None:
    raw_source = source(*(square(f"light{i}", 0, 0, "3/10") for i in range(4)))
    raw = packet(raw_source)
    graph = raw["graph_certificate"]
    graph.update(
        status="overweight_clique",
        proof=None,
        clique={"vertices": [0, 1, 2, 3], "weight": "6/5"},
        stop_reason="overweight_clique",
    )
    raw["status"] = "unresolved"
    result = reader.check_packet(
        raw, expected_source=raw_source, field=field, threshold=Fraction(1)
    )
    assert result["bound_proved"] is False
    assert result["pairs_accounted_for"] == 6
    assert result["status"] == "unresolved"


def test_largest_admitted_axis_bit_width_is_exact(field: NumberField) -> None:
    raw_source, raw = separated_packet()
    raw["nonedges"][0]["axis"] = point(2**256, 0)
    assert reader.check_packet(
        raw, expected_source=raw_source, field=field, threshold=Fraction(1)
    )["bound_proved"]


def test_degree_one_field_and_source_count_guard() -> None:
    field = NumberField([1, 0], (-1, 1))
    entry = square("rational", 0, 0, "1")
    entry["vertices"] = [
        [coordinate[:1] for coordinate in vertex] for vertex in entry["vertices"]
    ]
    raw_source = {
        "field": {"minimal_polynomial": ["1", "0"], "isolating_interval": ["-1", "1"]},
        "squares": [entry],
    }
    assert reader.check_packet(
        packet(raw_source), expected_source=raw_source, field=field, threshold=Fraction(1)
    )["bound_proved"]
    raw_source["squares"] = [entry] * 65
    with pytest.raises(reader.GuardError, match="inventory exceeds"):
        reader.check_packet(
            packet(raw_source), expected_source=raw_source, field=field, threshold=Fraction(1)
        )


def test_no_file_access_or_new_field_construction(field: NumberField) -> None:
    raw_source, raw = separated_packet()
    with (
        patch("builtins.open", side_effect=AssertionError("file access forbidden")),
        patch.object(
            NumberField, "__init__", side_effect=AssertionError("field construction forbidden")
        ),
    ):
        assert reader.check_packet(
            raw, expected_source=raw_source, field=field, threshold=Fraction(1)
        )["bound_proved"]


def test_arithmetic_failure_cannot_return_a_bound(
    field: NumberField, monkeypatch: pytest.MonkeyPatch
) -> None:
    raw_source, raw = separated_packet()

    def failed(_value: object) -> int:
        raise TimeoutError("toy exact-sign budget")

    monkeypatch.setattr(field, "sign", failed)
    with pytest.raises(TimeoutError):
        reader.check_packet(raw, expected_source=raw_source, field=field, threshold=Fraction(1))


def test_empty_family_is_supported_without_containment_claim(field: NumberField) -> None:
    raw_source = source()
    result = reader.check_packet(
        packet(raw_source), expected_source=raw_source, field=field, threshold=Fraction(1)
    )
    assert result["bound_proved"] is True
    assert result["source_squares_checked"] == 0
    assert "packing" in result["scope"]
