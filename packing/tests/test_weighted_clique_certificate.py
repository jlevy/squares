"""Source-free controls for rational graph certificates, without geometry imports."""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
from itertools import combinations
from typing import Any
from unittest.mock import patch

import pytest

from devtools import weighted_clique_certificate as producer
from devtools.weighted_clique_certificate import GraphError, produce


@pytest.mark.parametrize("raw", ["1e100000000", "1.0", "+1", "1_0", "\u0661", "1/0"])
def test_noncanonical_syntax_is_rejected_before_fraction_conversion(
    monkeypatch: pytest.MonkeyPatch, raw: str
) -> None:
    threshold = Fraction(1)

    def forbidden_conversion(*_args: object, **_kwargs: object) -> Fraction:
        raise AssertionError("noncanonical syntax reached Fraction conversion")

    monkeypatch.setattr(producer.Fraction, "__new__", forbidden_conversion)
    with pytest.raises(GraphError, match="canonical"):
        produce(
            {"vertex_count": 1, "vertices": [{"id": 0, "weight": raw}], "edges": []},
            threshold=threshold,
            node_limit=1,
        )


def graph(weights: tuple[Fraction, ...], edges: tuple[tuple[int, int], ...]) -> dict[str, Any]:
    return {
        "vertex_count": len(weights),
        "vertices": [{"id": i, "weight": str(w)} for i, w in enumerate(weights)],
        "edges": [list(edge) for edge in edges],
    }


def test_four_light_vertices_can_be_an_overweight_clique() -> None:
    raw = graph((Fraction(3, 10),) * 4, tuple(combinations(range(4), 2)))
    result = produce(raw, threshold=Fraction(1), node_limit=15)
    assert result["status"] == "overweight_clique"
    assert result["clique"] == {"vertices": [0, 1, 2, 3], "weight": "6/5"}
    assert result["proof"] is None
    assert "no geometric" in result["scope"]


def test_exact_sum_leaf_retains_zero_weight_vertices() -> None:
    raw = graph((Fraction(1, 3), Fraction(0), Fraction(2, 3)), ((0, 1), (0, 2), (1, 2)))
    result = produce(raw, threshold=Fraction(1), node_limit=1)
    assert result == {
        "version": 1,
        "kind": "rational-weighted-clique-bound",
        "graph": raw,
        "threshold": "1",
        "node_limit": 1,
        "nodes_visited": 1,
        "status": "proved_upper_bound",
        "proof": {"root": 0, "nodes": [{"kind": "sum"}]},
        "clique": None,
        "stop_reason": "complete",
        "scope": "Weighted graph only; no geometric intersection or packing claim.",
    }


def test_independent_class_proves_bound_without_branching() -> None:
    raw = graph((Fraction(4, 5), Fraction(7, 10), Fraction(3, 5)), ())
    result = produce(raw, threshold=Fraction(4, 5), node_limit=1)
    assert result["status"] == "proved_upper_bound"
    assert result["proof"] == {
        "root": 0,
        "nodes": [{"kind": "coloring", "classes": [[0, 1, 2]]}],
    }


def cycle_five() -> dict[str, Any]:
    return graph((Fraction(1, 2),) * 5, ((0, 1), (0, 4), (1, 2), (2, 3), (3, 4)))


def test_both_branches_are_present_in_a_complete_tree() -> None:
    result = produce(cycle_five(), threshold=Fraction(1), node_limit=3)
    assert result["status"] == "proved_upper_bound"
    assert result["nodes_visited"] == 3
    assert result["proof"] == {
        "root": 0,
        "nodes": [
            {"kind": "branch", "vertex": 0, "include": 1, "exclude": 2},
            {"kind": "coloring", "classes": [[1, 4]]},
            {"kind": "coloring", "classes": [[1, 3], [2, 4]]},
        ],
    }
    assert produce(cycle_five(), threshold=Fraction(1), node_limit=3) == result


@pytest.mark.parametrize("limit", [1, 2])
def test_exhausted_branch_is_unresolved_and_discards_partial_tree(limit: int) -> None:
    result = produce(cycle_five(), threshold=Fraction(1), node_limit=limit)
    assert result["status"] == "unresolved"
    assert result["stop_reason"] == "node_limit"
    assert result["nodes_visited"] == limit
    assert result["proof"] is None
    assert result["clique"] is None


def test_empty_graph_and_negative_threshold_have_explicit_empty_clique_semantics() -> None:
    raw = graph((), ())
    result = produce(raw, threshold=Fraction(0), node_limit=1)
    assert result["status"] == "proved_upper_bound"
    assert result["proof"] == {"root": 0, "nodes": [{"kind": "sum"}]}
    negative = produce(raw, threshold=Fraction(-1, 3), node_limit=1)
    assert negative["status"] == "overweight_clique"
    assert negative["nodes_visited"] == 1
    assert negative["clique"] == {"vertices": [], "weight": "0"}
    assert negative["proof"] is None


def test_derived_clique_sum_is_not_truncated_to_the_input_rational_cap() -> None:
    numerator = (1 << 126) - 1
    weights = (
        Fraction(numerator, (1 << 127) - 1),
        Fraction(numerator, (1 << 127) - 3),
    )
    result = produce(graph(weights, ((0, 1),)), threshold=Fraction(3, 4), node_limit=3)
    exact_weight = sum(weights, Fraction(0))
    assert exact_weight.denominator.bit_length() > 128
    assert result["status"] == "overweight_clique"
    assert result["clique"] == {"vertices": [0, 1], "weight": str(exact_weight)}


@pytest.mark.parametrize("mutation", ["missing", "duplicate", "reordered", "extra"])
def test_vertex_inventory_is_closed_and_ordered(mutation: str) -> None:
    raw = graph((Fraction(1, 3), Fraction(1, 2)), ((0, 1),))
    if mutation == "missing":
        raw["vertices"].pop()
    elif mutation == "duplicate":
        raw["vertices"][1]["id"] = 0
    elif mutation == "reordered":
        raw["vertices"].reverse()
    else:
        raw["vertices"].append({"id": 2, "weight": "0"})
    with pytest.raises(GraphError):
        produce(raw, threshold=Fraction(1), node_limit=1)


@pytest.mark.parametrize("value", [True, -1, 65, 1.0, "2"])
def test_vertex_count_is_a_bounded_exact_integer(value: Any) -> None:
    raw = graph((Fraction(0),), ())
    raw["vertex_count"] = value
    with pytest.raises(GraphError):
        produce(raw, threshold=Fraction(1), node_limit=1)


@pytest.mark.parametrize(
    "edges",
    [
        [[0, 0]],
        [[1, 0]],
        [[0, 3]],
        [[False, 1]],
        [[0, 1], [0, 1]],
        [[1, 2], [0, 1]],
        [[0]],
        [(0, 1)],
        "0,1",
    ],
)
def test_edge_inventory_refuses_noncanonical_or_unknown_edges(edges: Any) -> None:
    raw = graph((Fraction(1, 3),) * 3, ())
    raw["edges"] = edges
    with pytest.raises(GraphError):
        produce(raw, threshold=Fraction(1), node_limit=1)


@pytest.mark.parametrize(
    "value",
    ["-1/2", "2/4", "1.0", "1e0", "nan", "1/0", " 1", "0" * 129, str(2**128), 1, True],
)
def test_weights_are_bounded_canonical_nonnegative_rationals(value: Any) -> None:
    raw = graph((Fraction(0),), ())
    raw["vertices"][0]["weight"] = value
    with pytest.raises(GraphError):
        produce(raw, threshold=Fraction(1), node_limit=1)


@pytest.mark.parametrize("value", [0, 1.0, True, "1", Fraction(2**128), Fraction(1, 2**128)])
def test_threshold_requires_an_admitted_exact_fraction(value: Any) -> None:
    with pytest.raises(GraphError):
        produce(graph((), ()), threshold=value, node_limit=1)


@pytest.mark.parametrize("value", [0, -1, 100_001, True, 1.0, "1"])
def test_node_limit_requires_a_positive_admitted_integer(value: Any) -> None:
    with pytest.raises(GraphError):
        produce(graph((), ()), threshold=Fraction(0), node_limit=value)


def test_missing_budget_is_not_silently_defaulted() -> None:
    with pytest.raises(TypeError, match="node_limit"):
        produce(graph((), ()), threshold=Fraction(0))  # type: ignore[call-arg]


@pytest.mark.parametrize("field", ["source", "target", "geometry", "hypothesis"])
def test_graph_has_no_implicit_scientific_input_channel(field: str) -> None:
    raw = graph((Fraction(1),), ())
    raw[field] = "not an admitted field"
    with pytest.raises(GraphError):
        produce(raw, threshold=Fraction(1), node_limit=1)


def test_graph_and_vertex_dictionaries_have_exact_fields() -> None:
    raw = graph((Fraction(1),), ())
    raw["vertices"][0]["extra"] = "unrecognized"
    with pytest.raises(GraphError):
        produce(raw, threshold=Fraction(1), node_limit=1)
    del raw["edges"]
    with pytest.raises(GraphError):
        produce(raw, threshold=Fraction(1), node_limit=1)
    raw = graph((Fraction(1),), ())
    raw["vertices"][0]["id"] = False
    with pytest.raises(GraphError):
        produce(raw, threshold=Fraction(1), node_limit=1)


def test_producer_does_not_read_files_or_mutate_its_input() -> None:
    raw = cycle_five()
    initial = deepcopy(raw)
    with (
        patch("builtins.open", side_effect=AssertionError("file access forbidden")),
        patch("io.open", side_effect=AssertionError("file access forbidden")),
    ):
        result = produce(raw, threshold=Fraction(1), node_limit=3)
    assert result["status"] == "proved_upper_bound"
    assert raw == initial
    result["graph"]["vertices"][0]["weight"] = "0"
    assert raw == initial


def test_all_four_vertex_toy_graphs_against_direct_clique_enumeration() -> None:
    weights = (Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(3, 4))
    pairs = tuple(combinations(range(4), 2))
    subsets = tuple(tuple(v for v in range(4) if mask & (1 << v)) for mask in range(16))
    for mask in range(1 << len(pairs)):
        edges = tuple(pair for index, pair in enumerate(pairs) if mask & (1 << index))
        edge_set = set(edges)
        maximum = max(
            sum((weights[v] for v in subset), Fraction(0))
            for subset in subsets
            if all(pair in edge_set for pair in combinations(subset, 2))
        )
        for threshold in (Fraction(0), Fraction(1, 2), Fraction(1)):
            result = produce(graph(weights, edges), threshold=threshold, node_limit=31)
            if maximum <= threshold:
                assert result["status"] == "proved_upper_bound"
                assert result["proof"] is not None
                assert result["clique"] is None
            else:
                assert result["status"] == "overweight_clique"
                witness = result["clique"]["vertices"]
                assert all(pair in edge_set for pair in combinations(witness, 2))
                exact_weight = sum((weights[v] for v in witness), Fraction(0))
                assert exact_weight > threshold
                assert result["clique"]["weight"] == str(exact_weight)
                assert result["proof"] is None
