"""Bind exact unit squares to a conservative weighted overlap graph.

Only a nonzero exact separating axis removes an edge. Projection equality proves
interior disjointness, not closed disjointness. An undecided pair remains an edge.
Every original square, including zero-weight entries, is validated and retained in
the source receipt. Coincident positive-weight entries are never deduplicated.

The caller supplies an already validated NumberField; its declared polynomial and
root interval are bound explicitly. No scientific source, container or candidate is
loaded. A later independent reader must bind the full source and replay every omitted
edge plus the complete graph certificate. A graph clique is not a common-interior
witness. Container containment and external source identity are separate obligations.
"""

from __future__ import annotations

import re
from copy import deepcopy
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
from typing import Any

from devtools.weighted_clique_certificate import (
    MAX_NODE_LIMIT,
    MAX_RATIONAL_BITS,
    MAX_RATIONAL_CHARS,
    MAX_VERTICES,
)
from devtools.weighted_clique_certificate import (
    produce as graph_produce,
)
from sqpack.field import FieldElement, NumberField
from sqpack.verify import check_unit_squares, edge_axes, exact_sign, project

type Point = tuple[FieldElement, FieldElement]
type Quad = tuple[Point, Point, Point, Point]

VERSION = 1
KIND = "algebraic-unit-square-overlap-graph"
SCOPE = "Supplied square family only; no packing or source-candidate claim."
MAX_FIELD_DEGREE = 8
"""Admission limit, not permission to construct or evaluate a scientific field."""


class AdapterError(ValueError):
    """Malformed source identity, exact geometry, or prospective graph budget."""


@dataclass(frozen=True)
class _Entry:
    vertices: Quad
    weight: Fraction


def _object(raw: Any, keys: set[str]) -> dict[str, Any]:
    if type(raw) is not dict or set(raw) != keys:
        raise AdapterError("object fields do not match the closed source contract")
    return raw


def _fraction(raw: Any) -> Fraction:
    if (
        type(raw) is not str
        or len(raw) > MAX_RATIONAL_CHARS
        or re.fullmatch(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?", raw) is None
    ):
        raise AdapterError("rational must have bounded canonical ASCII syntax")
    value = Fraction(raw)
    if (
        str(value) != raw
        or max(value.numerator.bit_length(), value.denominator.bit_length()) > MAX_RATIONAL_BITS
    ):
        raise AdapterError("rational is noncanonical or exceeds the input bit cap")
    return value


def _element(raw: Any, field: NumberField) -> FieldElement:
    if type(raw) is not list or len(raw) != field.degree:
        raise AdapterError("coordinate must contain exactly the field-degree coefficients")
    return field.element([_fraction(value) for value in raw])


def _point(raw: Any, field: NumberField) -> Point:
    if type(raw) is not list or len(raw) != 2:
        raise AdapterError("point must contain exactly two exact coordinates")
    return _element(raw[0], field), _element(raw[1], field)


def _descriptor(raw: Any, field: NumberField) -> None:
    descriptor = _object(raw, {"minimal_polynomial", "isolating_interval"})
    for key, length in (
        ("minimal_polynomial", field.degree + 1),
        ("isolating_interval", 2),
    ):
        values = descriptor[key]
        if type(values) is not list or len(values) != length:
            raise AdapterError("field declaration has the wrong coefficient inventory")
        for value in values:
            _fraction(value)
    declared = field.precondition_certificate()
    if descriptor != {
        "minimal_polynomial": declared["normalized_minimal_polynomial"],
        "isolating_interval": declared["declared_isolating_interval"],
    }:
        raise AdapterError("source field declaration does not match the caller's exact field")


def _entries(source: Any, field: NumberField) -> tuple[_Entry, ...]:
    raw = _object(source, {"field", "squares"})
    _descriptor(raw["field"], field)
    squares = raw["squares"]
    if type(squares) is not list or len(squares) > MAX_VERTICES:
        raise AdapterError("complete source roster must be a list within the vertex cap")
    names: set[str] = set()
    entries = []
    for item in squares:
        square = _object(item, {"id", "vertices", "weight"})
        name = square["id"]
        if (
            type(name) is not str
            or re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,63}", name) is None
            or name in names
        ):
            raise AdapterError("source names must be unique bounded ASCII identifiers")
        names.add(name)
        weight = _fraction(square["weight"])
        if weight < 0:
            raise AdapterError("source weights must be nonnegative")
        corners = square["vertices"]
        if type(corners) is not list or len(corners) != 4:
            raise AdapterError("every source square must declare four cyclic vertices")
        parsed = [_point(corner, field) for corner in corners]
        vertices: Quad = parsed[0], parsed[1], parsed[2], parsed[3]
        if check_unit_squares((vertices,), exact_sign):
            raise AdapterError("source member is not a cyclic convex unit square")
        entries.append(_Entry(vertices, weight))
    return tuple(entries)


def _sat_axis(first: Quad, second: Quad) -> Point | None:
    """Search exact square edge normals; no floating-point broad phase."""
    for axis in edge_axes(first) + edge_axes(second):
        if axis[0].is_zero() and axis[1].is_zero():
            raise ArithmeticError("zero candidate axis")
        low_a, high_a = project(first, axis, exact_sign)
        low_b, high_b = project(second, axis, exact_sign)
        if (low_b - high_a).sign() >= 0:
            return axis
        if (low_a - high_b).sign() >= 0:
            return -axis[0], -axis[1]
    return None


def _axis_proves_nonedge(first: Quad, second: Quad, axis: Point) -> bool:
    """Recheck the emitted orientation on every cross-projection, including equality."""
    if (
        len(axis) != 2
        or any(
            not isinstance(value, FieldElement) or value.field is not first[0][0].field
            for value in axis
        )
        or all(value.is_zero() for value in axis)
    ):
        return False
    return all(
        (axis[0] * (q[0] - p[0]) + axis[1] * (q[1] - p[1])).sign() >= 0
        for p in first
        for q in second
    )


def _axis_packet(axis: Point) -> list[list[str]]:
    return [[str(coefficient) for coefficient in coordinate.coeffs] for coordinate in axis]


def _confirmed_axis(first: Quad, second: Quad) -> Point | None:
    axis = _sat_axis(first, second)
    if axis is not None and not _axis_proves_nonedge(first, second, axis):
        raise ArithmeticError("proposed separating axis failed its exact replay")
    return axis


def produce(
    source: Any, *, field: NumberField, threshold: Fraction, node_limit: int
) -> dict[str, Any]:
    """Visit every positive-weight pair, then produce a finite graph certificate.

    At most 64 source squares yield at most 2016 retained pairs and four candidate
    SAT axes per pair. A failed sign operation retains its edge and is recorded in
    unknown_pairs. An interrupted invocation yields no complete receipt; a caller
    must impose its own external wall cap. The graph node limit is mandatory.
    """
    if not isinstance(field, NumberField) or not 1 <= field.degree <= MAX_FIELD_DEGREE:
        raise AdapterError("caller must supply a validated field of admitted degree")
    if (
        type(threshold) is not Fraction
        or max(threshold.numerator.bit_length(), threshold.denominator.bit_length())
        > MAX_RATIONAL_BITS
    ):
        raise AdapterError("threshold must be an admitted exact Fraction")
    if type(node_limit) is not int or not 1 <= node_limit <= MAX_NODE_LIMIT:
        raise AdapterError("node_limit must be an admitted positive integer")
    entries = _entries(source, field)
    retained = [index for index, entry in enumerate(entries) if entry.weight > 0]
    edges: list[list[int]] = []
    nonedges: list[dict[str, Any]] = []
    unknown: list[list[int]] = []
    tested = 0
    for i, j in combinations(range(len(retained)), 2):
        tested += 1
        first, second = entries[retained[i]].vertices, entries[retained[j]].vertices
        try:
            axis = _confirmed_axis(first, second)
        except ArithmeticError, RuntimeError:
            axis = None
            unknown.append([i, j])
        if axis is None:
            edges.append([i, j])
        else:
            nonedges.append({"pair": [i, j], "axis": _axis_packet(axis)})
    graph = {
        "vertex_count": len(retained),
        "vertices": [
            {"id": local, "weight": str(entries[original].weight)}
            for local, original in enumerate(retained)
        ],
        "edges": edges,
    }
    certificate = graph_produce(graph, threshold=threshold, node_limit=node_limit)
    return {
        "version": VERSION,
        "kind": KIND,
        "source": deepcopy(source),
        "retained_ids": retained,
        "pairs_tested": tested,
        "nonedges": nonedges,
        "unknown_pairs": unknown,
        "graph_certificate": certificate,
        "status": (
            "proved_graph_bound"
            if certificate["status"] == "proved_upper_bound"
            else "unresolved"
        ),
        "scope": SCOPE,
    }
