"""Finite rational weighted-graph upper certificates, without geometric semantics.

An external reader must bind the graph, weights and threshold independently. Edges
in a geometric over-approximation may be removed only with separate geometric
evidence. An overweight graph clique need not have a common geometric interior.

The version-one packet contains graph identity, threshold, node limit and count,
status, proof, clique, stop reason and scope. A proved packet has a flat include-first
preorder tree rooted at zero. Branches name their minimum remaining vertex and both
child indices; sum/coloring leaves carry no trusted numerical bound. The reader
reconstructs selected and remaining vertices from the root and checks every leaf.
Only a complete tree proves an upper bound. Search exhaustion carries no proof.

At a branch, every clique extending the selected vertices either contains the
minimum remaining vertex (and its other vertices are neighbors) or excludes it.
An independent color class contributes at most its maximum vertex weight. These
two facts justify the branch split and coloring leaves; nonnegative weights justify
sum leaves. They concern graph cliques, not common intersections of convex sets.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any

VERSION = 1
KIND = "rational-weighted-clique-bound"
SCOPE = "Weighted graph only; no geometric intersection or packing claim."
MAX_VERTICES = 64
"""Bounds recursive depth and the size of each exact graph operation."""
MAX_NODE_LIMIT = 100_000
"""Admission ceiling; each invocation must still supply its own smaller node limit."""
MAX_RATIONAL_BITS = 128
"""Bounds input arithmetic; sums involve at most MAX_VERTICES such rationals."""
MAX_RATIONAL_CHARS = 128
"""Refuse oversized rational text before parsing its integers."""


class GraphError(ValueError):
    """Malformed graph identity, rational value, or finite search budget."""


@dataclass(frozen=True)
class _Graph:
    weights: tuple[Fraction, ...]
    edges: tuple[tuple[int, int], ...]
    neighbors: tuple[frozenset[int], ...]

    def packet(self) -> dict[str, Any]:
        return {
            "vertex_count": len(self.weights),
            "vertices": [{"id": i, "weight": str(w)} for i, w in enumerate(self.weights)],
            "edges": [list(edge) for edge in self.edges],
        }


def _check_fraction(value: Any) -> Fraction:
    if type(value) is not Fraction:
        raise GraphError("an exact Fraction is required")
    if max(value.numerator.bit_length(), value.denominator.bit_length()) > MAX_RATIONAL_BITS:
        raise GraphError("rational numerator or denominator exceeds the bit cap")
    return value


def _rational(raw: Any) -> Fraction:
    if type(raw) is not str or len(raw) > MAX_RATIONAL_CHARS:
        raise GraphError("rational input must be a bounded canonical string")
    if re.fullmatch(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?", raw) is None:
        raise GraphError("rational must use canonical ASCII integer or ratio syntax")
    try:
        value = Fraction(raw)
    except (ValueError, ZeroDivisionError) as exc:
        raise GraphError("invalid rational string") from exc
    if str(value) != raw:
        raise GraphError("rational string is not canonical")
    return _check_fraction(value)


def _graph(raw: Any) -> _Graph:
    if type(raw) is not dict or set(raw) != {"vertex_count", "vertices", "edges"}:
        raise GraphError("graph must have exactly vertex_count, vertices and edges")
    count = raw["vertex_count"]
    if type(count) is not int or not 0 <= count <= MAX_VERTICES:
        raise GraphError("vertex_count must be an integer within the graph cap")
    vertices = raw["vertices"]
    if type(vertices) is not list or len(vertices) != count:
        raise GraphError("vertex inventory does not match vertex_count")
    weights: list[Fraction] = []
    for index, vertex in enumerate(vertices):
        if type(vertex) is not dict or set(vertex) != {"id", "weight"}:
            raise GraphError("each vertex must contain exactly id and weight")
        if type(vertex["id"]) is not int or vertex["id"] != index:
            raise GraphError("vertex ids must be exactly 0 through vertex_count-1 in order")
        weight = _rational(vertex["weight"])
        if weight < 0:
            raise GraphError("vertex weights must be nonnegative")
        weights.append(weight)
    if type(raw["edges"]) is not list or len(raw["edges"]) > count * (count - 1) // 2:
        raise GraphError("edge inventory is not a bounded list")
    edges: list[tuple[int, int]] = []
    neighbors: list[set[int]] = [set() for _ in range(count)]
    for pair in raw["edges"]:
        if type(pair) is not list or len(pair) != 2:
            raise GraphError("an edge must be a two-element list")
        left, right = pair
        if type(left) is not int or type(right) is not int or not 0 <= left < right < count:
            raise GraphError("edge endpoints must satisfy 0 <= left < right < vertex_count")
        edge = (left, right)
        if edges and edge <= edges[-1]:
            raise GraphError("edges must be unique and strictly lexicographically ordered")
        edges.append(edge)
        neighbors[left].add(right)
        neighbors[right].add(left)
    return _Graph(tuple(weights), tuple(edges), tuple(frozenset(row) for row in neighbors))


def _coloring(graph: _Graph, remaining: tuple[int, ...]) -> list[list[int]]:
    classes: list[list[int]] = []
    for vertex in remaining:
        for color_class in classes:
            if all(other not in graph.neighbors[vertex] for other in color_class):
                color_class.append(vertex)
                break
        else:
            classes.append([vertex])
    return classes


@dataclass
class _Search:
    graph: _Graph
    threshold: Fraction
    node_limit: int
    nodes: list[dict[str, Any]] = field(default_factory=list)
    clique: dict[str, Any] | None = None

    def visit(
        self, selected: tuple[int, ...], remaining: tuple[int, ...], weight: Fraction
    ) -> int | None:
        if len(self.nodes) == self.node_limit:
            return None
        index = len(self.nodes)
        self.nodes.append({"kind": "pending"})
        if weight > self.threshold:
            self.clique = {"vertices": list(selected), "weight": str(weight)}
            return None
        bound = weight + sum((self.graph.weights[v] for v in remaining), Fraction(0))
        if bound <= self.threshold:
            self.nodes[index] = {"kind": "sum"}
            return index
        classes = _coloring(self.graph, remaining)
        bound = weight + sum(
            (max(self.graph.weights[v] for v in color_class) for color_class in classes),
            Fraction(0),
        )
        if bound <= self.threshold:
            self.nodes[index] = {"kind": "coloring", "classes": classes}
            return index
        # Nonnegative weights and the failed sum bound ensure remaining is nonempty.
        vertex, *rest = remaining
        included = tuple(v for v in rest if v in self.graph.neighbors[vertex])
        include_index = self.visit(
            (*selected, vertex), included, weight + self.graph.weights[vertex]
        )
        if include_index is None:
            return None
        exclude_index = self.visit(selected, tuple(rest), weight)
        if exclude_index is not None:
            self.nodes[index] = {
                "kind": "branch",
                "vertex": vertex,
                "include": include_index,
                "exclude": exclude_index,
            }
        return index if exclude_index is not None else None


def produce(raw_graph: Any, *, threshold: Fraction, node_limit: int) -> dict[str, Any]:
    """Prove a graph upper bound or return a graph witness/finite-budget refusal.

    Input ids and weights must be fully declared; no geometry or source identity is
    inferred. Every visited node, including the root and terminal witness, costs one
    budget unit. The empty clique has weight zero, including for negative thresholds.
    Tree depth is at most vertex_count + 1 and nodes_visited never exceeds node_limit.
    The node limit is not a wall-clock guarantee; a caller may impose a separate
    external time cap, whose termination is unresolved without a complete packet.
    """
    graph = _graph(raw_graph)
    threshold = _check_fraction(threshold)
    if type(node_limit) is not int or not 1 <= node_limit <= MAX_NODE_LIMIT:
        raise GraphError("node_limit must be an integer between 1 and the node admission cap")
    search = _Search(graph, threshold, node_limit)
    root = search.visit((), tuple(range(len(graph.weights))), Fraction(0))
    if root is not None:
        status, stop_reason = "proved_upper_bound", "complete"
        proof: dict[str, Any] | None = {"root": root, "nodes": search.nodes}
    elif search.clique is not None:
        status, stop_reason, proof = "overweight_clique", "overweight_clique", None
    else:
        status, stop_reason, proof = "unresolved", "node_limit", None
    return {
        "version": VERSION,
        "kind": KIND,
        "graph": graph.packet(),
        "threshold": str(threshold),
        "node_limit": node_limit,
        "nodes_visited": len(search.nodes),
        "status": status,
        "proof": proof,
        "clique": search.clique,
        "stop_reason": stop_reason,
        "scope": SCOPE,
    }
