"""Independent conservative-graph reader for a caller-bound family of unit squares.

The complete source, including zero-weight entries, is bound before omission. A
nonedge needs a nonzero exact axis with all sixteen cross-projections nonnegative;
equality excludes common interior and is sufficient. Every other pair stays an
edge. Only an independently verified complete clique upper bound establishes the
almost-everywhere depth bound for this finite family.

The caller supplies an already validated NumberField. No field/source constructor,
producer, file loader or floating geometry is used. Containment and scientific
source identity are NOT inferred: a later packing adapter must validate them
separately. Arithmetic errors and external time-limit termination are not proofs.
"""

from __future__ import annotations

import re
from fractions import Fraction
from itertools import combinations
from typing import Any

from devtools import check_weighted_clique_certificate as graph_reader
from sqpack.field import FieldElement, NumberField

SCOPE = "Supplied square family only; no packing or source-candidate claim."
KIND = "algebraic-unit-square-overlap-graph"
MAX_SQUARES = 64
Point = tuple[FieldElement, FieldElement]
Square = tuple[Point, ...]


class GuardError(ValueError):
    """The packet has not established its claimed family-depth bound."""


def _keys(raw: Any, expected: set[str], label: str) -> None:
    if type(raw) is not dict or set(raw) != expected:
        raise GuardError(f"{label} must have exactly its declared keys")


def _integer(raw: Any, low: int, high: int, label: str) -> int:
    if type(raw) is not int or not low <= raw <= high:
        raise GuardError(f"{label} is not an admitted exact integer")
    return raw


def _fraction(raw: Any, *, bits: int = 128, chars: int = 128) -> Fraction:
    if type(raw) is not str or len(raw) > chars:
        raise GuardError("rational must be a bounded canonical string")
    if re.fullmatch(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?", raw) is None:
        raise GuardError("rational must use canonical ASCII integer or ratio syntax")
    value = Fraction(raw)
    if (
        str(value) != raw
        or max(value.numerator.bit_length(), value.denominator.bit_length()) > bits
    ):
        raise GuardError("rational is noncanonical or exceeds its bit cap")
    return value


def _element(raw: Any, field: NumberField, *, axis: bool = False) -> FieldElement:
    if type(raw) is not list or len(raw) != field.degree:
        raise GuardError("field coefficient vector must have exactly the declared degree")
    bits, chars = (257, 200) if axis else (128, 128)
    return field.element([_fraction(value, bits=bits, chars=chars) for value in raw])


def _point(raw: Any, field: NumberField, *, axis: bool = False) -> Point:
    if type(raw) is not list or len(raw) != 2:
        raise GuardError("point or axis must have exactly two coordinates")
    return _element(raw[0], field, axis=axis), _element(raw[1], field, axis=axis)


def _difference(left: Point, right: Point) -> Point:
    return left[0] - right[0], left[1] - right[1]


def _dot(left: Point, right: Point) -> FieldElement:
    return left[0] * right[0] + left[1] * right[1]


def _unit_square(square: Square) -> None:
    """Two perpendicular unit edges and parallelogram closure, either cyclic order."""
    p, q, r, s = square
    u, v = _difference(q, p), _difference(s, p)
    if not (_dot(u, u) - 1).is_zero() or not (_dot(v, v) - 1).is_zero():
        raise GuardError("source polygon has nonunit adjacent edges")
    if not _dot(u, v).is_zero():
        raise GuardError("source polygon has nonorthogonal adjacent edges")
    if not (r[0] - q[0] - s[0] + p[0]).is_zero() or not (r[1] - q[1] - s[1] + p[1]).is_zero():
        raise GuardError("source polygon is not a cyclic parallelogram")
    if (u[0] * v[1] - u[1] * v[0]).is_zero():
        raise GuardError("source polygon is degenerate")


def _field_descriptor(raw: Any, field: NumberField) -> None:
    _keys(raw, {"minimal_polynomial", "isolating_interval"}, "field descriptor")
    polynomial, interval = raw["minimal_polynomial"], raw["isolating_interval"]
    if type(polynomial) is not list or len(polynomial) != field.degree + 1:
        raise GuardError("field polynomial inventory disagrees with its degree")
    if type(interval) is not list or len(interval) != 2:
        raise GuardError("field isolating interval needs two endpoints")
    for value in [*polynomial, *interval]:
        _fraction(value)
    certificate = field.precondition_certificate()
    if (
        polynomial != certificate["normalized_minimal_polynomial"]
        or interval != certificate["declared_isolating_interval"]
    ):
        raise GuardError("source field differs from the caller-bound real embedding")


def _source(raw: Any, field: NumberField) -> tuple[list[Square], list[Fraction]]:
    _keys(raw, {"field", "squares"}, "source")
    if type(field) is not NumberField or not 1 <= field.degree <= 4:
        raise GuardError("caller must supply an admitted validated NumberField")
    _field_descriptor(raw["field"], field)
    entries = raw["squares"]
    if type(entries) is not list or len(entries) > MAX_SQUARES:
        raise GuardError("source square inventory exceeds its cap")
    squares: list[Square] = []
    weights: list[Fraction] = []
    identities: set[str] = set()
    for entry in entries:
        _keys(entry, {"id", "vertices", "weight"}, "source square")
        identity = entry["id"]
        if (
            type(identity) is not str
            or re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,63}", identity) is None
            or identity in identities
        ):
            raise GuardError("source square ids must be unique bounded ASCII names")
        identities.add(identity)
        vertices = entry["vertices"]
        if type(vertices) is not list or len(vertices) != 4:
            raise GuardError("source square needs exactly four cyclic vertices")
        square = tuple(_point(vertex, field) for vertex in vertices)
        _unit_square(square)
        weight = _fraction(entry["weight"])
        if weight < 0:
            raise GuardError("source weights must be nonnegative")
        squares.append(square)
        weights.append(weight)
    return squares, weights


def _pair(raw: Any, count: int) -> tuple[int, int]:
    if type(raw) is not list or len(raw) != 2:
        raise GuardError("pair needs exactly two local vertex ids")
    left = _integer(raw[0], 0, count - 1, "pair id")
    right = _integer(raw[1], 0, count - 1, "pair id")
    if left >= right:
        raise GuardError("pair must have increasing distinct local ids")
    return left, right


def _nonedges(raw: Any, squares: list[Square], field: NumberField) -> set[tuple[int, int]]:
    count = len(squares)
    if type(raw) is not list or len(raw) > count * (count - 1) // 2:
        raise GuardError("nonedge inventory exceeds its pair cap")
    removed: set[tuple[int, int]] = set()
    previous = (-1, -1)
    for entry in raw:
        _keys(entry, {"pair", "axis"}, "nonedge receipt")
        pair = _pair(entry["pair"], count)
        if pair <= previous:
            raise GuardError("nonedge receipts must be unique and lexicographically ordered")
        previous = pair
        axis = _point(entry["axis"], field, axis=True)
        if axis[0].is_zero() and axis[1].is_zero():
            raise GuardError("a separating axis must be nonzero")
        # Every vertex of the second square must project at least as far as every
        # vertex of the first. No producer projection extrema are trusted.
        for first in squares[pair[0]]:
            for second in squares[pair[1]]:
                if field.sign(_dot(_difference(second, first), axis)) < 0:
                    raise GuardError("nonedge axis fails a cross-vertex projection comparison")
        removed.add(pair)
    return removed


def _unknown_pairs(raw: Any, count: int, removed: set[tuple[int, int]]) -> None:
    if type(raw) is not list or len(raw) > count * (count - 1) // 2:
        raise GuardError("unknown pair inventory exceeds its cap")
    previous = (-1, -1)
    for entry in raw:
        pair = _pair(entry, count)
        if pair <= previous or pair in removed:
            raise GuardError("unknown pairs must be ordered unique retained graph edges")
        previous = pair


def check_packet(
    raw: Any, *, expected_source: Any, field: NumberField, threshold: Fraction
) -> dict[str, Any]:
    """Return a family-depth proof only after exact geometry and complete graph replay.

    This API performs no I/O and provides no wall-clock guarantee. The caller must
    bind its source independently and impose any scientific process cap externally.
    An unresolved/overweight graph receipt is never a positive-area witness.
    """
    _keys(
        raw,
        {
            "version",
            "kind",
            "source",
            "retained_ids",
            "pairs_tested",
            "nonedges",
            "unknown_pairs",
            "graph_certificate",
            "status",
            "scope",
        },
        "adapter certificate",
    )
    _integer(raw["version"], 1, 1, "version")
    if raw["kind"] != KIND or raw["scope"] != SCOPE:
        raise GuardError("foreign adapter kind or scope escalation")
    _keys(expected_source, {"field", "squares"}, "caller source")
    if raw["source"] != expected_source:
        raise GuardError("certificate differs from the full caller-bound source")
    squares, weights = _source(raw["source"], field)
    retained = [index for index, weight in enumerate(weights) if weight > 0]
    ids = raw["retained_ids"]
    if type(ids) is not list or any(type(value) is not int for value in ids) or ids != retained:
        raise GuardError("retained ids must be exactly the original positive-weight indices")
    count = len(retained)
    pair_count = count * (count - 1) // 2
    _integer(raw["pairs_tested"], pair_count, pair_count, "pairs_tested")
    removed = _nonedges(raw["nonedges"], [squares[index] for index in retained], field)
    _unknown_pairs(raw["unknown_pairs"], count, removed)
    graph = {
        "vertex_count": count,
        "vertices": [
            {"id": local, "weight": str(weights[original])}
            for local, original in enumerate(retained)
        ],
        "edges": [list(pair) for pair in combinations(range(count), 2) if pair not in removed],
    }
    try:
        checked = graph_reader.check_packet(
            raw["graph_certificate"], expected_graph=graph, threshold=threshold
        )
    except graph_reader.GuardError as exc:
        raise GuardError(f"graph certificate refused: {exc}") from exc
    proved = checked["status"] == "verified_upper_bound" and checked["bound_proved"] is True
    if raw["status"] != ("proved_graph_bound" if proved else "unresolved"):
        raise GuardError(
            "adapter status disagrees with the independently verified graph result"
        )
    return {
        "kind": "geometric-graph-check/v1",
        "status": "verified_depth_bound" if proved else "unresolved",
        "bound_proved": proved,
        "threshold": str(threshold),
        "source_squares_checked": len(squares),
        "retained_ids": retained,
        "pairs_accounted_for": pair_count,
        "nonedges_verified": len(removed),
        "projection_comparisons_checked": 16 * len(removed),
        "graph_verification": checked,
        "scope": SCOPE,
    }
