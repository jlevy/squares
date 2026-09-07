"""Independent graph-only fixtures; no producer, geometry or scientific data imports."""

from __future__ import annotations

import copy
import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path
from typing import Any

import pytest

from devtools import check_weighted_clique_certificate as reader


@pytest.mark.parametrize("raw", ["1e100000000", "1.0", "+1", "1_0", "\u0661", "1/0"])
def test_noncanonical_syntax_is_rejected_before_fraction_conversion(
    monkeypatch: pytest.MonkeyPatch, raw: str
) -> None:
    def forbidden_conversion(_value: object) -> Fraction:
        raise AssertionError("noncanonical syntax reached Fraction conversion")

    monkeypatch.setattr(reader, "Fraction", forbidden_conversion)
    with pytest.raises(reader.GuardError, match="canonical"):
        reader.parse_graph(graph([raw]))


def graph(weights: list[str], edges: list[list[int]] | None = None) -> dict[str, Any]:
    return {
        "vertex_count": len(weights),
        "vertices": [{"id": index, "weight": weight} for index, weight in enumerate(weights)],
        "edges": edges or [],
    }


def receipt(
    raw_graph: dict[str, Any], nodes: list[dict[str, Any]], threshold: str = "1"
) -> dict[str, Any]:
    return {
        "version": 1,
        "kind": "rational-weighted-clique-bound",
        "graph": raw_graph,
        "threshold": threshold,
        "node_limit": 100,
        "nodes_visited": len(nodes),
        "status": "proved_upper_bound",
        "proof": {"root": 0, "nodes": nodes},
        "clique": None,
        "stop_reason": "complete",
        "scope": "Weighted graph only; no geometric intersection or packing claim.",
    }


def test_both_include_exclude_branches_independently_cover_all_cliques() -> None:
    raw_graph = graph(["3/4", "3/4"])
    raw = receipt(
        raw_graph,
        [
            {"kind": "branch", "vertex": 0, "include": 1, "exclude": 2},
            {"kind": "sum"},
            {"kind": "sum"},
        ],
    )
    result = reader.check_packet(raw, expected_graph=raw_graph, threshold=Fraction(1))
    assert result["status"] == "verified_upper_bound"
    assert result["bound_proved"] is True
    assert result["nodes_verified"] == 3


def test_coloring_leaf_certifies_a_nonsum_bound() -> None:
    raw_graph = graph(["3/5"] * 4, [[0, 1], [0, 3], [1, 2], [2, 3]])
    raw = receipt(raw_graph, [{"kind": "coloring", "classes": [[0, 2], [1, 3]]}], "6/5")
    result = reader.check_packet(raw, expected_graph=raw_graph, threshold=Fraction(6, 5))
    assert result["bound_proved"] is True
    assert result["nodes_verified"] == 1
    raw["proof"]["nodes"] = [{"kind": "sum"}]
    with pytest.raises(reader.GuardError, match="sum leaf"):
        reader.check_packet(raw, expected_graph=raw_graph, threshold=Fraction(6, 5))


def test_selected_weight_is_included_in_sum_and_coloring_leaf_bounds() -> None:
    nodes = [
        {"kind": "branch", "vertex": 0, "include": 1, "exclude": 2},
        {"kind": "sum"},
        {"kind": "sum"},
    ]
    complete = graph(["3/4", "3/4"], [[0, 1]])
    with pytest.raises(reader.GuardError, match="sum leaf"):
        reader.check_packet(
            receipt(complete, nodes), expected_graph=complete, threshold=Fraction(1)
        )
    colored = [
        nodes[0],
        {"kind": "coloring", "classes": [[1, 2]]},
        {"kind": "coloring", "classes": [[1, 2]]},
    ]
    star = graph(["3/5"] * 3, [[0, 1], [0, 2]])
    with pytest.raises(reader.GuardError, match="coloring leaf"):
        reader.check_packet(receipt(star, colored), expected_graph=star, threshold=Fraction(1))
    star["vertices"][0]["weight"] = "2/5"
    assert (
        reader.check_packet(receipt(star, colored), expected_graph=star, threshold=Fraction(1))[
            "bound_proved"
        ]
        is True
    )


def test_branch_neighbor_restriction_and_zero_weight_vertices_are_exact() -> None:
    raw_graph = graph(["0", "3/5", "3/5"], [[0, 1]])
    nodes = [
        {"kind": "branch", "vertex": 0, "include": 1, "exclude": 2},
        {"kind": "sum"},
        {"kind": "coloring", "classes": [[1, 2]]},
    ]
    result = reader.check_packet(
        receipt(raw_graph, nodes), expected_graph=raw_graph, threshold=Fraction(1)
    )
    assert result["bound_proved"] is True
    assert result["nodes_verified"] == 3


def test_missing_repeated_cyclic_or_orphan_nodes_cannot_cover_the_tree() -> None:
    raw_graph = graph(["3/4", "3/4"])
    base = receipt(
        raw_graph,
        [
            {"kind": "branch", "vertex": 0, "include": 1, "exclude": 2},
            {"kind": "sum"},
            {"kind": "sum"},
        ],
    )
    changes: list[dict[str, Any]] = []
    for key, value in (
        ("vertex", 1),
        ("vertex", True),
        ("include", 0),
        ("include", 2),
        ("exclude", 0),
        ("exclude", 1),
        ("exclude", 3),
        ("exclude", True),
    ):
        raw = copy.deepcopy(base)
        raw["proof"]["nodes"][0][key] = value
        changes.append(raw)
    raw = copy.deepcopy(base)
    raw["proof"]["nodes"].pop()
    raw["nodes_visited"] = 2
    changes.append(raw)
    raw = copy.deepcopy(base)
    raw["proof"]["nodes"].append({"kind": "sum"})
    raw["nodes_visited"] = 4
    changes.append(raw)
    raw = copy.deepcopy(base)
    raw["proof"]["root"] = True
    changes.append(raw)
    raw = copy.deepcopy(base)
    del raw["proof"]["nodes"][0]["exclude"]
    changes.append(raw)
    for raw in changes:
        with pytest.raises(reader.GuardError):
            reader.check_packet(raw, expected_graph=raw_graph, threshold=Fraction(1))


def test_coloring_partition_must_cover_each_remaining_vertex_once_independently() -> None:
    raw_graph = graph(["1/4"] * 4, [[0, 1]])
    invalid = (
        [],
        [[0, 2], [1]],
        [[0, 2], [1, 2, 3]],
        [[0, 1], [2, 3]],
        [[2, 0], [1, 3]],
        [[1, 3], [0, 2]],
        [[], [0, 2], [1, 3]],
        [[0, 2], [1, 4]],
        [[False, 2], [1, 3]],
    )
    for classes in invalid:
        raw = receipt(raw_graph, [{"kind": "coloring", "classes": classes}])
        with pytest.raises(reader.GuardError):
            reader.check_packet(raw, expected_graph=raw_graph, threshold=Fraction(1))


def overweight(raw_graph: dict[str, Any], vertices: list[int], weight: str) -> dict[str, Any]:
    raw = receipt(raw_graph, [])
    raw.update(
        status="overweight_clique",
        proof=None,
        clique={"vertices": vertices, "weight": weight},
        nodes_visited=1,
        stop_reason="overweight_clique",
    )
    return raw


def test_four_three_tenths_vertices_defeat_any_triple_only_bound() -> None:
    raw_graph = graph(["3/10"] * 4, [list(edge) for edge in combinations(range(4), 2)])
    result = reader.check_packet(
        overweight(raw_graph, [0, 1, 2, 3], "6/5"),
        expected_graph=raw_graph,
        threshold=Fraction(1),
    )
    assert result["status"] == "verified_overweight_clique"
    assert result["bound_proved"] is False
    assert result["scope"] == "Weighted graph only; no geometric intersection or packing claim."
    for vertices in combinations(range(4), 3):
        with pytest.raises(reader.GuardError, match="strictly overweight"):
            reader.check_packet(
                overweight(raw_graph, list(vertices), "9/10"),
                expected_graph=raw_graph,
                threshold=Fraction(1),
            )
    with pytest.raises(reader.GuardError, match="sum leaf"):
        reader.check_packet(
            receipt(raw_graph, [{"kind": "sum"}]),
            expected_graph=raw_graph,
            threshold=Fraction(1),
        )


def test_rejected_maximal_clique_cannot_discharge_potential_overweight_subcliques() -> None:
    raw_graph = graph(["3/10"] * 4 + ["0"], [list(edge) for edge in combinations(range(5), 2)])
    raw = receipt(raw_graph, [{"kind": "rejected_maximal_clique", "vertices": list(range(5))}])
    with pytest.raises(reader.GuardError, match="unknown proof-node"):
        reader.check_packet(raw, expected_graph=raw_graph, threshold=Fraction(1))
    result = reader.check_packet(
        overweight(raw_graph, [0, 1, 2, 3], "6/5"),
        expected_graph=raw_graph,
        threshold=Fraction(1),
    )
    assert result["bound_proved"] is False
    assert result["status"] == "verified_overweight_clique"


def test_overweight_receipt_requires_actual_edges_correct_sum_and_unique_ids() -> None:
    raw_graph = graph(["3/4", "3/4"])
    with pytest.raises(reader.GuardError, match="not a clique"):
        reader.check_packet(
            overweight(raw_graph, [0, 1], "3/2"),
            expected_graph=raw_graph,
            threshold=Fraction(1),
        )
    raw_graph["edges"] = [[0, 1]]
    for vertices, weight in (
        ([0, 1], "2"),
        ([0, 0], "3/2"),
        ([1, 0], "3/2"),
        ([0, 2], "3/2"),
        ([0, 1], "1"),
        ([0, 1], "1.5"),
    ):
        with pytest.raises(reader.GuardError):
            reader.check_packet(
                overweight(raw_graph, vertices, weight),
                expected_graph=raw_graph,
                threshold=Fraction(1),
            )


def test_derived_sum_may_exceed_the_individual_rational_bit_cap() -> None:
    left, right = Fraction(1, (1 << 127) - 1), Fraction(1, (1 << 126) - 1)
    raw_graph = graph([str(left), str(right)], [[0, 1]])
    total = left + right
    assert total.denominator.bit_length() > 128
    raw = overweight(raw_graph, [0, 1], str(total))
    raw["threshold"] = "0"
    result = reader.check_packet(raw, expected_graph=raw_graph, threshold=Fraction(0))
    assert result["clique"] == {"vertices": [0, 1], "weight": str(total)}


def test_empty_graph_zero_weights_and_negative_threshold_include_empty_clique() -> None:
    for raw_graph in (graph([]), graph(["0", "0"])):
        raw = receipt(raw_graph, [{"kind": "sum"}], "0")
        assert (
            reader.check_packet(raw, expected_graph=raw_graph, threshold=Fraction(0))[
                "bound_proved"
            ]
            is True
        )
    empty = graph([])
    raw = overweight(empty, [], "0")
    raw["threshold"] = "-1"
    assert (
        reader.check_packet(raw, expected_graph=empty, threshold=Fraction(-1))["status"]
        == "verified_overweight_clique"
    )
    with pytest.raises(reader.GuardError, match="sum leaf"):
        reader.check_packet(
            receipt(empty, [{"kind": "sum"}], "-1"),
            expected_graph=empty,
            threshold=Fraction(-1),
        )


def test_graph_and_threshold_are_bound_to_the_caller_not_self_description() -> None:
    raw_graph = graph(["1/4", "1/4"])
    raw = receipt(raw_graph, [{"kind": "sum"}])
    for expected in (graph(["1/4", "1/4"], [[0, 1]]), graph(["1/4", "1/3"]), graph(["1/4"])):
        with pytest.raises(reader.GuardError, match="caller-bound"):
            reader.check_packet(raw, expected_graph=expected, threshold=Fraction(1))
    with pytest.raises(reader.GuardError, match="caller-bound"):
        reader.check_packet(raw, expected_graph=raw_graph, threshold=Fraction(2))


def test_malformed_graphs_and_nonexact_or_oversized_rationals_refuse() -> None:
    base = graph(["1/4", "1/4"])
    cases: list[Any] = [None, [], {}, {**base, "extra": 0}, graph(["0"] * 65)]
    for weight in ("-1", "1.0", "2/2", "1/0", "NaN", 0.25, True, str(1 << 128)):
        raw = copy.deepcopy(base)
        raw["vertices"][0]["weight"] = weight
        cases.append(raw)
    cases.extend(
        {**base, "edges": edges}
        for edges in ([[0, 0]], [[1, 0]], [[0, 2]], [[False, 1]], [[0, 1], [0, 1]])
    )
    raw = copy.deepcopy(base)
    raw["vertices"][0]["id"] = False
    cases.append(raw)
    cases.append({**base, "vertex_count": True})
    for raw in cases:
        with pytest.raises(reader.GuardError):
            reader.parse_graph(raw)


def test_node_exhaustion_and_mutated_statuses_never_certify_a_bound() -> None:
    raw_graph = graph(["3/4", "3/4"])
    raw = receipt(raw_graph, [])
    raw.update(
        status="unresolved",
        proof=None,
        clique=None,
        stop_reason="node_limit",
        node_limit=1,
        nodes_visited=1,
    )
    result = reader.check_packet(raw, expected_graph=raw_graph, threshold=Fraction(1))
    assert result["status"] == "unresolved"
    assert result["bound_proved"] is False
    for key, value in (
        ("status", "proved_upper_bound"),
        ("nodes_visited", 0),
        ("nodes_visited", 2),
        ("node_limit", True),
        ("node_limit", 100001),
        ("proof", {"root": 0, "nodes": []}),
        ("clique", {"vertices": [], "weight": "0"}),
        ("stop_reason", "complete"),
        ("version", True),
        ("scope", "Positive-area geometric witness"),
    ):
        changed = {**raw, key: value}
        with pytest.raises(reader.GuardError):
            reader.check_packet(changed, expected_graph=raw_graph, threshold=Fraction(1))


def test_cli_binds_a_separate_graph_and_exposes_refusal_and_exhaustion(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    raw_graph = graph(["1/4", "1/4"])
    graph_path, proof_path = tmp_path / "graph.json", tmp_path / "proof.json"
    graph_path.write_text(json.dumps(raw_graph), encoding="utf-8")
    proof_path.write_text(json.dumps(receipt(raw_graph, [{"kind": "sum"}])), encoding="utf-8")
    args = ["--input", str(proof_path), "--graph", str(graph_path), "--threshold", "1"]
    assert reader.main(args) == 0
    output = capsys.readouterr()
    assert json.loads(output.out)["bound_proved"] is True
    assert output.err == ""
    raw = receipt(raw_graph, [])
    raw.update(
        status="unresolved", proof=None, stop_reason="node_limit", node_limit=1, nodes_visited=1
    )
    proof_path.write_text(json.dumps(raw), encoding="utf-8")
    assert reader.main(args) == 2
    assert json.loads(capsys.readouterr().out)["status"] == "unresolved"
    for text in (
        '{"version":1,"version":1}',
        '{"version":1.0}',
        '{"version":NaN}',
        '{"version":',
    ):
        proof_path.write_text(text, encoding="utf-8")
        assert reader.main(args) == 2
        output = capsys.readouterr()
        assert json.loads(output.out)["bound_proved"] is False
        assert "refused" in output.err
    monkeypatch.setattr(reader, "MAX_PACKET_BYTES", 16)
    proof_path.write_text(" " * 17, encoding="utf-8")
    assert reader.main(args) == 2
    assert "byte cap" in capsys.readouterr().out
    with pytest.raises(SystemExit) as refused:
        reader.main(["--input", str(proof_path), "--threshold", "1"])
    assert refused.value.code == 2


def test_cli_clique_success_is_not_an_upper_bound_and_graph_or_file_mismatch_refuses(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    raw_graph = graph(["3/4", "3/4"], [[0, 1]])
    graph_path, proof_path = tmp_path / "graph.json", tmp_path / "clique.json"
    graph_path.write_text(json.dumps(raw_graph), encoding="utf-8")
    proof_path.write_text(json.dumps(overweight(raw_graph, [0, 1], "3/2")), encoding="utf-8")
    args = ["--input", str(proof_path), "--graph", str(graph_path), "--threshold", "1"]
    assert reader.main(args) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["status"] == "verified_overweight_clique"
    assert result["bound_proved"] is False
    graph_path.write_text(json.dumps(graph(["3/4", "3/4"])), encoding="utf-8")
    assert reader.main(args) == 2
    result = json.loads(capsys.readouterr().out)
    assert result["status"] == "refused"
    assert "caller-bound" in result["reason"]
    args[1] = str(tmp_path / "missing.json")
    assert reader.main(args) == 2
    assert json.loads(capsys.readouterr().out)["bound_proved"] is False
