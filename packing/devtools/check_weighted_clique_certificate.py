"""Independent exact weighted-clique reader, with no geometric interpretation.

The caller supplies the graph and threshold independently of the certificate.
Only the Python standard library is used; no producer or geometry code is imported.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

MAX_VERTICES = 64
MAX_INPUT_BITS = 128
MAX_SUM_BITS = MAX_VERTICES * MAX_INPUT_BITS + MAX_VERTICES.bit_length()
MAX_NODES = 100000
MAX_PACKET_BYTES = 16 * 1024 * 1024
SCOPE = "Weighted graph only; no geometric intersection or packing claim."


class GuardError(ValueError):
    """The supplied receipt has not established its claimed graph result."""


@dataclass(frozen=True)
class Graph:
    weights: tuple[Fraction, ...]
    edges: tuple[tuple[int, int], ...]
    neighbors: tuple[frozenset[int], ...]


def _keys(raw: Any, expected: set[str], label: str) -> None:
    if not isinstance(raw, dict) or set(raw) != expected:
        raise GuardError(f"{label} requires exactly its declared object keys")


def _integer(raw: Any, low: int, high: int, label: str) -> int:
    if type(raw) is not int or not low <= raw <= high:
        raise GuardError(f"{label} must be an integer from {low} to {high}")
    return raw


def _bounded_fraction(value: Fraction, bits: int) -> None:
    if type(value) is not Fraction:
        raise GuardError("caller threshold must be an exact Fraction")
    if max(value.numerator.bit_length(), value.denominator.bit_length()) > bits:
        raise GuardError("rational exceeds its declared bit cap")


def _rational(raw: Any, *, bits: int = MAX_INPUT_BITS) -> Fraction:
    max_digits = bits * 30103 // 100000 + 1
    if not isinstance(raw, str) or not raw or len(raw) > 2 * max_digits + 2:
        raise GuardError("rational must be a bounded canonical string")
    if re.fullmatch(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?", raw) is None:
        raise GuardError("rational must use canonical ASCII integer or ratio syntax")
    try:
        value = Fraction(raw)
    except (ValueError, ZeroDivisionError) as exc:
        raise GuardError("invalid rational string") from exc
    if str(value) != raw:
        raise GuardError("noncanonical rational string")
    _bounded_fraction(value, bits)
    return value


def parse_graph(raw: Any) -> Graph:
    """Validate canonical ordered vertices, nonnegative weights and simple graph edges."""
    _keys(raw, {"vertex_count", "vertices", "edges"}, "graph")
    count = _integer(raw["vertex_count"], 0, MAX_VERTICES, "vertex_count")
    if not isinstance(raw["vertices"], list) or len(raw["vertices"]) != count:
        raise GuardError("graph must contain exactly the declared vertices")
    weights: list[Fraction] = []
    for identity, vertex in enumerate(raw["vertices"]):
        _keys(vertex, {"id", "weight"}, "vertex")
        _integer(vertex["id"], identity, identity, "ordered vertex id")
        weight = _rational(vertex["weight"])
        if weight < 0:
            raise GuardError("vertex weights must be nonnegative")
        weights.append(weight)
    if not isinstance(raw["edges"], list) or len(raw["edges"]) > count * (count - 1) // 2:
        raise GuardError("graph edges must be a bounded list")
    edges: list[tuple[int, int]] = []
    adjacent: list[set[int]] = [set() for _ in range(count)]
    for edge in raw["edges"]:
        if not isinstance(edge, list) or len(edge) != 2:
            raise GuardError("an edge must have exactly two ordered endpoints")
        left = _integer(edge[0], 0, count - 1, "edge endpoint")
        right = _integer(edge[1], 0, count - 1, "edge endpoint")
        pair = left, right
        if left >= right or (edges and pair <= edges[-1]):
            raise GuardError("edges must be unique and lexicographically ordered with u < v")
        edges.append(pair)
        adjacent[left].add(right)
        adjacent[right].add(left)
    return Graph(tuple(weights), tuple(edges), tuple(frozenset(row) for row in adjacent))


def graph_packet(graph: Graph) -> dict[str, Any]:
    return {
        "vertex_count": len(graph.weights),
        "vertices": [
            {"id": index, "weight": str(weight)} for index, weight in enumerate(graph.weights)
        ],
        "edges": [list(edge) for edge in graph.edges],
    }


def _vertices(raw: Any, count: int, label: str) -> tuple[int, ...]:
    if not isinstance(raw, list) or len(raw) > count:
        raise GuardError(f"{label} must be a bounded vertex list")
    values = tuple(_integer(value, 0, count - 1, label) for value in raw)
    if values != tuple(sorted(set(values))):
        raise GuardError(f"{label} must contain sorted unique vertex ids")
    return values


def _color_bound(raw: Any, remaining: tuple[int, ...], graph: Graph) -> Fraction:
    if not isinstance(raw, list) or len(raw) > len(remaining):
        raise GuardError("color classes must form a bounded partition")
    used: set[int] = set()
    available = set(remaining)
    previous = -1
    bound = Fraction(0)
    for entry in raw:
        color = _vertices(entry, len(graph.weights), "color class")
        if not color or color[0] <= previous:
            raise GuardError("nonempty color classes must be ordered by their first ids")
        previous = color[0]
        for vertex in color:
            if vertex not in available or vertex in used:
                raise GuardError("coloring repeats or includes a nonremaining vertex")
            if any(neighbor in graph.neighbors[vertex] for neighbor in color):
                raise GuardError("a color class is not independent")
            used.add(vertex)
        bound += max(graph.weights[vertex] for vertex in color)
    if used != available:
        raise GuardError("coloring omits a remaining vertex")
    return bound


def _verify_tree(raw: Any, graph: Graph, threshold: Fraction, nodes_visited: int) -> int:
    _keys(raw, {"root", "nodes"}, "proof")
    _integer(raw["root"], 0, 0, "proof root")
    nodes = raw["nodes"]
    if not isinstance(nodes, list) or len(nodes) != nodes_visited:
        raise GuardError("proof node inventory disagrees with nodes_visited")

    def visit(index: int, selected: tuple[int, ...], remaining: tuple[int, ...]) -> int:
        if not 0 <= index < len(nodes):
            raise GuardError("proof is missing a required child")
        node = nodes[index]
        if not isinstance(node, dict):
            raise GuardError("proof node must be an object")
        selected_weight = sum((graph.weights[v] for v in selected), Fraction(0))
        total = selected_weight + sum((graph.weights[v] for v in remaining), Fraction(0))
        kind = node.get("kind")
        if kind == "sum":
            _keys(node, {"kind"}, "sum leaf")
            if total > threshold:
                raise GuardError("sum leaf does not prove its reconstructed state")
            return index + 1
        if kind == "coloring":
            _keys(node, {"kind", "classes"}, "coloring leaf")
            if selected_weight + _color_bound(node["classes"], remaining, graph) > threshold:
                raise GuardError("coloring leaf does not prove its reconstructed state")
            return index + 1
        if kind != "branch":
            raise GuardError("unknown proof-node kind")
        _keys(node, {"kind", "vertex", "include", "exclude"}, "branch")
        if not remaining or not selected_weight <= threshold < total:
            raise GuardError("branch violates the selected-weight and remaining-state guards")
        vertex = _integer(node["vertex"], remaining[0], remaining[0], "branch vertex")
        _integer(node["include"], index + 1, index + 1, "include-first preorder index")
        tail = remaining[1:]
        included = tuple(v for v in tail if v in graph.neighbors[vertex])
        next_index = visit(index + 1, (*selected, vertex), included)
        _integer(node["exclude"], next_index, next_index, "exclude preorder index")
        return visit(next_index, selected, tail)

    end = visit(0, (), tuple(range(len(graph.weights))))
    if end != len(nodes):
        raise GuardError("proof contains unreachable orphan nodes")
    return end


def _verify_clique(
    raw: Any, graph: Graph, threshold: Fraction
) -> tuple[tuple[int, ...], Fraction]:
    _keys(raw, {"vertices", "weight"}, "clique")
    vertices = _vertices(raw["vertices"], len(graph.weights), "clique vertices")
    for index, vertex in enumerate(vertices):
        if any(other not in graph.neighbors[vertex] for other in vertices[index + 1 :]):
            raise GuardError("overweight vertex set is not a clique")
    weight = sum((graph.weights[vertex] for vertex in vertices), Fraction(0))
    if _rational(raw["weight"], bits=MAX_SUM_BITS) != weight or weight <= threshold:
        raise GuardError("clique weight is incorrect or not strictly overweight")
    return vertices, weight


def check_packet(raw: Any, *, expected_graph: Any, threshold: Fraction) -> dict[str, Any]:
    """Verify against caller-bound data; a graph clique is never a geometric witness."""
    graph = parse_graph(expected_graph)
    _bounded_fraction(threshold, MAX_INPUT_BITS)
    _keys(
        raw,
        {
            "version",
            "kind",
            "graph",
            "threshold",
            "node_limit",
            "nodes_visited",
            "status",
            "proof",
            "clique",
            "stop_reason",
            "scope",
        },
        "certificate",
    )
    _integer(raw["version"], 1, 1, "certificate version")
    if raw["kind"] != "rational-weighted-clique-bound" or raw["scope"] != SCOPE:
        raise GuardError("foreign certificate kind or geometric scope escalation")
    if parse_graph(raw["graph"]) != graph or _rational(raw["threshold"]) != threshold:
        raise GuardError("certificate differs from the caller-bound graph or threshold")
    node_limit = _integer(raw["node_limit"], 1, MAX_NODES, "node_limit")
    visited = _integer(raw["nodes_visited"], 1, node_limit, "nodes_visited")
    result: dict[str, Any] = {
        "kind": "rational-weighted-clique-check/v1",
        "status": "unresolved",
        "bound_proved": False,
        "graph": graph_packet(graph),
        "threshold": str(threshold),
        "nodes_verified": 0,
        "clique": None,
        "scope": SCOPE,
    }
    if raw["status"] == "proved_upper_bound":
        if raw["clique"] is not None or raw["stop_reason"] != "complete":
            raise GuardError("upper-bound status requires only a complete proof")
        result["nodes_verified"] = _verify_tree(raw["proof"], graph, threshold, visited)
        result["status"] = "verified_upper_bound"
        result["bound_proved"] = True
    elif raw["status"] == "overweight_clique":
        if raw["proof"] is not None or raw["stop_reason"] != "overweight_clique":
            raise GuardError("overweight status cannot carry an upper-bound proof")
        vertices, weight = _verify_clique(raw["clique"], graph, threshold)
        result["status"] = "verified_overweight_clique"
        result["clique"] = {"vertices": list(vertices), "weight": str(weight)}
    elif raw["status"] == "unresolved":
        if (
            raw["proof"] is not None
            or raw["clique"] is not None
            or raw["stop_reason"] != "node_limit"
            or visited != node_limit
        ):
            raise GuardError("unresolved status must retain only exact node-limit exhaustion")
    else:
        raise GuardError("unknown certificate status")
    return result


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise GuardError("duplicate JSON object key")
        result[key] = value
    return result


def _refuse_float(_raw: str) -> Any:
    raise GuardError("floating or nonfinite JSON numbers are forbidden")


def read_json(path: Path) -> Any:
    """Bound input bytes before parsing; duplicate keys and approximate numbers refuse."""
    with path.open("rb") as stream:
        data = stream.read(MAX_PACKET_BYTES + 1)
    if len(data) > MAX_PACKET_BYTES:
        raise GuardError("input exceeds the JSON byte cap")
    return json.loads(
        data,
        object_pairs_hook=_unique_object,
        parse_float=_refuse_float,
        parse_constant=_refuse_float,
    )


def main(argv: list[str] | None = None) -> int:
    """Exit zero means verified graph evidence, not necessarily a proved upper bound."""
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--graph", type=Path, required=True)
    parser.add_argument("--threshold", required=True)
    args = parser.parse_args(argv)
    try:
        result = check_packet(
            read_json(args.input),
            expected_graph=read_json(args.graph),
            threshold=_rational(args.threshold),
        )
    except (OSError, ValueError, RecursionError) as exc:
        print(
            json.dumps(
                {
                    "status": "refused",
                    "bound_proved": False,
                    "reason": str(exc),
                    "scope": SCOPE,
                },
                sort_keys=True,
            )
        )
        print(f"clique certificate refused: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True))
    return 2 if result["status"] == "unresolved" else 0


if __name__ == "__main__":
    raise SystemExit(main())
