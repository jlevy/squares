"""Exact closed convex-polygon union discovery with endpoint-chain certificates.

The caller supplies an already validated real NumberField and the full source
rectangle/polygon wire data. This module constructs no fields and loads no scientific
source. Discovery partitions x at every supporting-line crossing, including those
outside the rectangle's y-range. Endpoint checks, not discovery counts, justify each
published closed slab: a fixed polygon chain connects the bottom and top, with every
adjacent pair intersecting on both endpoint fibers. Convexity extends those pair
intersections across the slab. Closed tangencies therefore count as cover.

A finite closed convex-polygon cover admits these certificates under a sufficiently
fine event partition. Resource exhaustion or failure to find a chain is unresolved,
not a counterexample to an application using this sufficient cover. Independent
verification must bind all source data and recheck every endpoint condition.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from dataclasses import field as dataclass_field
from fractions import Fraction
from itertools import combinations, pairwise
from time import monotonic
from typing import Any

from sqpack.field import FieldElement, NumberField

KIND = "closed-convex-polygon-cover/v1"
MAX_POLYGONS = 32
MAX_VERTICES = 96
MAX_LINES = MAX_VERTICES + 4
MAX_EVENTS = 5000
MAX_SLABS = 5000
MAX_INPUT_BITS = 128
MAX_INPUT_CHARS = 80
MAX_DERIVED_BITS = 4096
MAX_DERIVED_CHARS = 2600
Point = tuple[FieldElement, FieldElement]
Line = tuple[FieldElement, FieldElement, FieldElement]


class CoverError(ValueError):
    """Malformed or unsupported caller-bound source or operational limit."""


class _StoppedError(Exception):
    pass


@dataclass(frozen=True)
class Polygon:
    """A validated positive-area CCW convex polygon with inward edge forms."""

    identifier: str
    vertices: tuple[Point, ...]
    edges: tuple[Line, ...]


@dataclass(frozen=True)
class Source:
    """One validated source identity; the reciprocal cache changes no geometry."""

    field: NumberField
    rectangle: tuple[Point, Point]
    polygons: tuple[Polygon, ...]
    descriptor: dict[str, Any]
    inverses: dict[FieldElement, FieldElement] = dataclass_field(default_factory=dict)


def parse_rational(raw: Any) -> Fraction:
    """Reject lexical expansion tricks before invoking Fraction conversion."""
    if type(raw) is not str or len(raw) > MAX_INPUT_CHARS:
        raise CoverError("a bounded canonical rational string is required")
    if re.fullmatch(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?", raw) is None:
        raise CoverError("rational syntax must be ASCII integer or ratio")
    value = Fraction(raw)
    if (
        str(value) != raw
        or max(value.numerator.bit_length(), value.denominator.bit_length()) > MAX_INPUT_BITS
    ):
        raise CoverError("rational is noncanonical or exceeds the input bit cap")
    return value


def _scalar(raw: Any, field: NumberField) -> FieldElement:
    if type(raw) is not list or len(raw) != field.degree:
        raise CoverError("scalar must contain exactly one coefficient per field degree")
    return field.element([parse_rational(value) for value in raw])


def _point(raw: Any, field: NumberField) -> Point:
    if type(raw) is not list or len(raw) != 2:
        raise CoverError("point must contain exactly two scalars")
    return _scalar(raw[0], field), _scalar(raw[1], field)


def _descriptor(field: NumberField) -> dict[str, Any]:
    if type(field) is not NumberField or not 1 <= field.degree <= 4:
        raise CoverError(
            "caller must supply a validated degree-one through degree-four NumberField"
        )
    certificate = field.precondition_certificate()
    polynomial = certificate["normalized_minimal_polynomial"]
    interval = certificate["declared_isolating_interval"]
    if (
        type(polynomial) is not list
        or len(polynomial) != field.degree + 1
        or type(interval) is not list
        or len(interval) != 2
        or certificate["irreducible_over_q"] is not True
        or certificate["root_count_in_open_interval"] != 1
        or certificate["endpoints_are_not_roots"] is not True
    ):
        raise CoverError("field preconditions are not established")
    for coefficient in [*polynomial, *interval]:
        parse_rational(coefficient)
    return {"minimal_polynomial": list(polynomial), "isolating_interval": list(interval)}


def validate_source(field: NumberField, rectangle: Any, polygons: Any) -> Source:
    """Validate the full source without constructing a field or accepting floats."""
    descriptor = _descriptor(field)
    if type(rectangle) is not list or len(rectangle) != 2:
        raise CoverError("rectangle must contain its lower and upper corners")
    lower, upper = (_point(point, field) for point in rectangle)
    if not lower[0] < upper[0] or not lower[1] < upper[1]:
        raise CoverError("rectangle must be nondegenerate")
    if type(polygons) is not list or len(polygons) > MAX_POLYGONS:
        raise CoverError("polygon inventory exceeds its cap")
    # Count the whole inventory before parsing any polygon's coordinates.
    total = 0
    for raw in polygons:
        if type(raw) is not dict or len(raw) != 2 or set(raw) != {"id", "vertices"}:
            raise CoverError("polygon requires exactly id and vertices")
        if type(raw["vertices"]) is not list or not 3 <= len(raw["vertices"]) <= MAX_VERTICES:
            raise CoverError("polygon vertex inventory is malformed")
        total += len(raw["vertices"])
    if total > MAX_VERTICES:
        raise CoverError("total vertex inventory exceeds its cap")
    identifiers: set[str] = set()
    validated: list[Polygon] = []
    for raw in polygons:
        identifier = raw["id"]
        if (
            type(identifier) is not str
            or re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,63}", identifier) is None
        ):
            raise CoverError("polygon identifier must be bounded ASCII")
        if identifier in identifiers:
            raise CoverError("polygon identifiers must be unique")
        identifiers.add(identifier)
        vertices = tuple(_point(point, field) for point in raw["vertices"])
        if len(set(vertices)) != len(vertices):
            raise CoverError("polygon vertices must be distinct")
        edges: list[Line] = []
        area = field.zero
        for (x, y), (next_x, next_y) in pairwise((*vertices, vertices[0])):
            dx, dy = next_x - x, next_y - y
            if dx.is_zero() and dy.is_zero():
                raise CoverError("polygon has a zero edge")
            edges.append((-dy, dx, dy * x - dx * y))
            area += x * next_y - y * next_x
        if area.sign() <= 0 or any(
            (a * x + b * y + c).sign() < 0 for a, b, c in edges for x, y in vertices
        ):
            raise CoverError("polygon must be positive-area CCW and convex")
        validated.append(Polygon(identifier, vertices, tuple(edges)))
    return Source(field, (lower, upper), tuple(validated), descriptor)


def _bounded(value: FieldElement) -> FieldElement:
    if any(
        max(coefficient.numerator.bit_length(), coefficient.denominator.bit_length())
        > MAX_DERIVED_BITS
        for coefficient in value.coeffs
    ):
        raise _StoppedError("arithmetic_error")
    return value


def _inverse(source: Source, value: FieldElement) -> FieldElement:
    if value not in source.inverses:
        source.inverses[value] = _bounded(source.field.one / value)
    return source.inverses[value]


def _deadline(deadline: float | None) -> None:
    if deadline is not None and monotonic() >= deadline:
        raise _StoppedError("deadline")


def _limit(value: int, maximum: int, minimum: int) -> None:
    if type(value) is not int or not minimum <= value <= maximum:
        raise CoverError("operational limit is outside its fixed admission cap")


def sweep_events(
    source: Source, *, event_limit: int = MAX_EVENTS, deadline: float | None = None
) -> tuple[FieldElement, ...]:
    """Reconstruct every conservative x-event; caps never truncate the inventory."""
    _limit(event_limit, MAX_EVENTS, 2)
    (left, bottom), (right, top) = source.rectangle
    zero, one = source.field.zero, source.field.one
    raw_lines = [
        (one, zero, -left),
        (one, zero, -right),
        (zero, one, -bottom),
        (zero, one, -top),
    ]
    raw_lines.extend(edge for polygon in source.polygons for edge in polygon.edges)
    lines: dict[Line, None] = {}
    for a, b, c in raw_lines:
        _deadline(deadline)
        reciprocal = _inverse(source, a if not a.is_zero() else b)
        lines[
            (_bounded(a * reciprocal), _bounded(b * reciprocal), _bounded(c * reciprocal))
        ] = None
    if len(lines) > MAX_LINES:
        raise _StoppedError("event_limit")
    events = {left, right}

    def add(value: FieldElement) -> None:
        _bounded(value)
        if left <= value <= right:
            events.add(value)
            if len(events) > event_limit:
                raise _StoppedError("event_limit")

    for a, b, c in lines:
        if b.is_zero():
            add(-c * _inverse(source, a))
    for (a, b, c), (other_a, other_b, other_c) in combinations(lines, 2):
        _deadline(deadline)
        determinant = _bounded(a * other_b - other_a * b)
        if not determinant.is_zero():
            # The y-coordinate is deliberately not filtered: this is an overpartition.
            add((b * other_c - other_b * c) * _inverse(source, determinant))
    result = tuple(sorted(events))
    _deadline(deadline)
    return result


def _section(
    source: Source, polygon: Polygon, x: FieldElement
) -> tuple[FieldElement, FieldElement] | None:
    lower, upper = source.rectangle[0][1], source.rectangle[1][1]
    for a, b, c in polygon.edges:
        constant = _bounded(a * x + c)
        direction = b.sign()
        if direction == 0:
            if constant.sign() < 0:
                return None
        else:
            ordinate = _bounded(-constant * _inverse(source, b))
            if direction > 0:
                lower = max(lower, ordinate)
            else:
                upper = min(upper, ordinate)
    return (lower, upper) if lower <= upper else None


def _discover_chain(source: Source, x: FieldElement) -> tuple[int, ...] | None:
    sections = tuple(_section(source, polygon, x) for polygon in source.polygons)
    current, top = source.rectangle[0][1], source.rectangle[1][1]
    chain: list[int] = []
    while current < top:
        best: int | None = None
        farthest = current
        for index, section in enumerate(sections):
            if section is not None and section[0] <= current and section[1] > farthest:
                best, farthest = index, section[1]
        if best is None:
            return None
        chain.append(best)
        current = farthest
    return tuple(chain)


def _endpoint_chain(
    source: Source, left: FieldElement, right: FieldElement, chain: tuple[int, ...]
) -> bool:
    if not chain or len(set(chain)) != len(chain):
        return False
    for x in (left, right):
        sections = []
        for index in chain:
            section = _section(source, source.polygons[index], x)
            if section is None:
                return False
            sections.append(section)
        if sections[0][0] > source.rectangle[0][1] or sections[-1][1] < source.rectangle[1][1]:
            return False
        if any(
            max(first[0], second[0]) > min(first[1], second[1])
            for first, second in pairwise(sections)
        ):
            return False
    return True


def _wire_scalar(value: FieldElement) -> list[str]:
    _bounded(value)
    result = [str(coefficient) for coefficient in value.coeffs]
    if any(len(coefficient) > MAX_DERIVED_CHARS for coefficient in result):
        raise _StoppedError("arithmetic_error")
    return result


def _wire_point(point: Point) -> list[list[str]]:
    return [_wire_scalar(value) for value in point]


def _packet(source: Source, slabs: list[dict[str, Any]], reason: str) -> dict[str, Any]:
    return {
        "kind": KIND,
        "status": "covered" if reason == "complete" else "unresolved",
        "field": {key: list(value) for key, value in source.descriptor.items()},
        "rectangle": [_wire_point(point) for point in source.rectangle],
        "polygons": [
            {
                "id": polygon.identifier,
                "vertices": [_wire_point(point) for point in polygon.vertices],
            }
            for polygon in source.polygons
        ],
        "slabs": slabs if reason == "complete" else [],
        "stop_reason": reason,
    }


def produce_cover(
    field: NumberField,
    rectangle: Any,
    polygons: Any,
    *,
    event_limit: int = MAX_EVENTS,
    slab_limit: int = MAX_SLABS,
    deadline: float | None = None,
) -> dict[str, Any]:
    """Return a complete endpoint-chain cover or an empty unresolved receipt.

    Limits bound discovered events and processed slabs before merging. ``deadline``
    is an optional absolute monotonic time; an external whole-process cap is still
    required for operational isolation. Invalid source/limits raise CoverError.
    """
    _limit(event_limit, MAX_EVENTS, 2)
    _limit(slab_limit, MAX_SLABS, 1)
    if deadline is not None and (type(deadline) is not float or not math.isfinite(deadline)):
        raise CoverError("deadline must be a finite monotonic float")
    source = validate_source(field, rectangle, polygons)
    slabs: list[dict[str, Any]] = []
    try:
        events = sweep_events(source, event_limit=event_limit, deadline=deadline)
        for index, (left, right) in enumerate(pairwise(events)):
            _deadline(deadline)
            if index >= slab_limit:
                return _packet(source, [], "slab_limit")
            chain = _discover_chain(source, _bounded((left + right) / 2))
            if chain is None or not _endpoint_chain(source, left, right, chain):
                return _packet(source, [], "no_chain")
            identifiers = [source.polygons[item].identifier for item in chain]
            if slabs and slabs[-1]["chain"] == identifiers:
                slabs[-1]["right"] = _wire_scalar(right)
            else:
                slabs.append(
                    {
                        "left": _wire_scalar(left),
                        "right": _wire_scalar(right),
                        "chain": identifiers,
                    }
                )
        if not slabs:
            return _packet(source, [], "no_chain")
        _deadline(deadline)
        return _packet(source, slabs, "complete")
    except _StoppedError as stopped:
        return _packet(source, [], str(stopped))
    except ArithmeticError:
        return _packet(source, [], "arithmetic_error")
