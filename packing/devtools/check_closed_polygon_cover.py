"""Independent endpoint-chain certificates for closed convex-polygon coverage.

Every slab uses one fixed polygon chain. The first polygon contains both bottom
corners, the last both top corners, and each adjacent pair has intersecting vertical
sections at both endpoints. Convexity of the pair intersection supplies a point at
every intermediate x. The vertical sections are intervals, so the chain connects
the bottom to the top throughout the slab. Endpoint contact is sufficient.

The caller binds an already validated exact field, rectangle and complete polygon
inventory. This reader neither imports a producer nor reconstructs its supporting-
line events. It performs no I/O or scientific construction. A caller must impose
external input/process limits; an exception or unfinished invocation is not a proof.
"""

from __future__ import annotations

import re
from fractions import Fraction
from itertools import pairwise
from typing import Any

from sqpack.field import FieldElement, NumberField

type Point = tuple[FieldElement, FieldElement]
type Polygon = tuple[Point, ...]

KIND = "closed-convex-polygon-cover/v1"
SCOPE = "Caller-bound rectangle and convex polygons only; no packing or continuous-angle claim."
MAX_POLYGONS = 32
MAX_VERTICES = 96
"""Total vertices across the complete source polygon inventory."""
MAX_SLABS = 5000
MAX_DEGREE = 4
INPUT_BITS, INPUT_CHARS = 128, 80
DERIVED_BITS, DERIVED_CHARS = 4096, 2600
UNRESOLVED_REASONS = frozenset(
    {"event_limit", "slab_limit", "no_chain", "deadline", "arithmetic_error"}
)


class GuardError(ValueError):
    """The packet has not proved its caller-bound closed cover."""


def _keys(raw: Any, keys: set[str], label: str) -> None:
    if type(raw) is not dict or set(raw) != keys:
        raise GuardError(f"{label} must have exactly its declared keys")


def _fraction(raw: Any, *, derived: bool = False) -> Fraction:
    bits, chars = (DERIVED_BITS, DERIVED_CHARS) if derived else (INPUT_BITS, INPUT_CHARS)
    if (
        type(raw) is not str
        or len(raw) > chars
        or re.fullmatch(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?", raw) is None
    ):
        raise GuardError("rational requires bounded canonical ASCII syntax")
    value = Fraction(raw)
    if (
        str(value) != raw
        or max(value.numerator.bit_length(), value.denominator.bit_length()) > bits
    ):
        raise GuardError("rational is noncanonical or exceeds its bit cap")
    return value


def _element(raw: Any, field: NumberField, *, derived: bool = False) -> FieldElement:
    if type(raw) is not list or len(raw) != field.degree:
        raise GuardError("scalar requires exactly the field-degree coefficients")
    return field.element([_fraction(value, derived=derived) for value in raw])


def _point(raw: Any, field: NumberField) -> Point:
    if type(raw) is not list or len(raw) != 2:
        raise GuardError("point requires exactly two coordinates")
    return _element(raw[0], field), _element(raw[1], field)


def _field_descriptor(raw: Any, field: NumberField) -> None:
    if type(field) is not NumberField or not 1 <= field.degree <= MAX_DEGREE:
        raise GuardError("caller must supply a validated field of admitted degree")
    _keys(raw, {"minimal_polynomial", "isolating_interval"}, "field descriptor")
    for key, size in (("minimal_polynomial", field.degree + 1), ("isolating_interval", 2)):
        values = raw[key]
        if type(values) is not list or len(values) != size:
            raise GuardError("field descriptor has an incorrect rational inventory")
        for value in values:
            _fraction(value)
    descriptor = field.precondition_certificate()
    if (
        raw["minimal_polynomial"] != descriptor["normalized_minimal_polynomial"]
        or raw["isolating_interval"] != descriptor["declared_isolating_interval"]
    ):
        raise GuardError("field descriptor differs from the caller-bound real embedding")


def _cross(a: Point, b: Point) -> FieldElement:
    return a[0] * b[1] - a[1] * b[0]


def _subtract(a: Point, b: Point) -> Point:
    return a[0] - b[0], a[1] - b[1]


def _edges(polygon: Polygon) -> tuple[tuple[Point, Point], ...]:
    return tuple(zip(polygon, (*polygon[1:], polygon[0]), strict=True))


def _contains(polygon: Polygon, point: Point) -> bool:
    return all(_cross(_subtract(b, a), _subtract(point, a)) >= 0 for a, b in _edges(polygon))


def _convex_polygon(raw: Any, field: NumberField) -> Polygon:
    if type(raw) is not list or not 3 <= len(raw) <= MAX_VERTICES:
        raise GuardError("polygon needs a bounded nondegenerate vertex inventory")
    polygon = tuple(_point(vertex, field) for vertex in raw)
    if len(set(polygon)) != len(polygon):
        raise GuardError("polygon vertices must be distinct; closing vertex is implicit")
    area_twice = sum((_cross(a, b) for a, b in _edges(polygon)), field.zero)
    if area_twice <= 0:
        raise GuardError("polygon must have positive area and counterclockwise orientation")
    if any(not _contains(polygon, vertex) for vertex in polygon):
        raise GuardError("polygon is not a convex counterclockwise boundary")
    return polygon


def _source(
    rectangle: Any, polygons: Any, field: NumberField
) -> tuple[Point, Point, dict[str, Polygon]]:
    if type(rectangle) is not list or len(rectangle) != 2:
        raise GuardError("rectangle needs lower and upper corners")
    lower, upper = (_point(point, field) for point in rectangle)
    if lower[0] >= upper[0] or lower[1] >= upper[1]:
        raise GuardError("rectangle must have positive width and height")
    if type(polygons) is not list or len(polygons) > MAX_POLYGONS:
        raise GuardError("polygon inventory exceeds its admission cap")
    parsed: dict[str, Polygon] = {}
    total_vertices = 0
    for entry in polygons:
        _keys(entry, {"id", "vertices"}, "source polygon")
        identity = entry["id"]
        if (
            type(identity) is not str
            or re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,63}", identity) is None
            or identity in parsed
        ):
            raise GuardError("polygon ids must be unique bounded ASCII names")
        vertices = entry["vertices"]
        if type(vertices) is not list:
            raise GuardError("polygon vertices must be a list")
        total_vertices += len(vertices)
        if total_vertices > MAX_VERTICES:
            raise GuardError("total source vertices exceed their admission cap")
        parsed[identity] = _convex_polygon(vertices, field)
    return lower, upper, parsed


def _section(polygon: Polygon, x: FieldElement) -> tuple[FieldElement, FieldElement] | None:
    """Intersect every closed edge with a vertical line, retaining vertical segments."""
    heights: list[FieldElement] = []
    for a, b in _edges(polygon):
        dx = b[0] - a[0]
        if dx.is_zero():
            if x == a[0]:
                heights.extend((a[1], b[1]))
        elif min(a[0], b[0]) <= x <= max(a[0], b[0]):
            heights.append(a[1] + (x - a[0]) * (b[1] - a[1]) / dx)
    return (min(heights), max(heights)) if heights else None


def _chain(
    raw: Any,
    *,
    left: FieldElement,
    right: FieldElement,
    lower_y: FieldElement,
    upper_y: FieldElement,
    polygons: dict[str, Polygon],
) -> int:
    if (
        type(raw) is not list
        or not 1 <= len(raw) <= len(polygons)
        or any(type(identity) is not str or identity not in polygons for identity in raw)
        or len(set(raw)) != len(raw)
    ):
        raise GuardError("slab requires one nonempty chain of distinct source polygon ids")
    first, last = polygons[raw[0]], polygons[raw[-1]]
    for x in (left, right):
        if not _contains(first, (x, lower_y)) or not _contains(last, (x, upper_y)):
            raise GuardError("chain endpoints do not contain both bottom and top slab corners")
        sections = [_section(polygons[identity], x) for identity in raw]
        for a, b in pairwise(sections):
            if a is None or b is None or max(a[0], b[0]) > min(a[1], b[1]):
                raise GuardError("fixed chain has a gap in an endpoint vertical section")
    return 2 * (len(raw) - 1)


def check_packet(
    raw: Any, *, field: NumberField, rectangle: Any, polygons: Any
) -> dict[str, Any]:
    """Prove exactly the caller-bound rectangle cover, never an inferred packing claim."""
    _keys(
        raw,
        {"kind", "status", "field", "rectangle", "polygons", "slabs", "stop_reason"},
        "cover packet",
    )
    if raw["kind"] != KIND:
        raise GuardError("foreign cover packet kind")
    _field_descriptor(raw["field"], field)
    if raw["rectangle"] != rectangle or raw["polygons"] != polygons:
        raise GuardError("packet differs from the complete caller-bound rectangle or polygons")
    lower, upper, parsed = _source(raw["rectangle"], raw["polygons"], field)
    slabs = raw["slabs"]
    if type(slabs) is not list or len(slabs) > MAX_SLABS:
        raise GuardError("slab inventory exceeds its admission cap")
    if raw["status"] == "unresolved":
        if (
            slabs
            or type(raw["stop_reason"]) is not str
            or raw["stop_reason"] not in UNRESOLVED_REASONS
        ):
            raise GuardError("unresolved packet must have no proof and a declared stop reason")
        return _result(proved=False, slabs=0, polygons=len(parsed), checks=0)
    if raw["status"] != "covered" or raw["stop_reason"] != "complete" or not slabs:
        raise GuardError("positive cover requires complete status and a nonempty partition")
    cursor = lower[0]
    checks = 0
    for entry in slabs:
        _keys(entry, {"left", "right", "chain"}, "slab")
        left = _element(entry["left"], field, derived=True)
        right = _element(entry["right"], field, derived=True)
        if left != cursor or right <= left or right > upper[0]:
            raise GuardError(
                "slabs must form a contiguous increasing partition within the rectangle"
            )
        checks += _chain(
            entry["chain"],
            left=left,
            right=right,
            lower_y=lower[1],
            upper_y=upper[1],
            polygons=parsed,
        )
        cursor = right
    if cursor != upper[0]:
        raise GuardError("slab partition omits the right boundary or a final interval")
    return _result(proved=True, slabs=len(slabs), polygons=len(parsed), checks=checks)


def _result(*, proved: bool, slabs: int, polygons: int, checks: int) -> dict[str, Any]:
    return {
        "kind": "closed-polygon-cover-check/v1",
        "status": "verified_cover" if proved else "unresolved",
        "cover_proved": proved,
        "slabs_checked": slabs,
        "polygons_checked": polygons,
        "endpoint_pair_checks": checks,
        "scope": SCOPE,
    }
