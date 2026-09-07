"""Independent, lazy source reconstruction for the H124 collision augmentation.

Only ``cover_source`` constructs scientific inputs. It retains the accepted
independent axis-frame source and appends one closed collision polygon. The new
polygon is reconstructed from every pair of its eight supporting lines, followed
by all eight closed half-plane tests. Empty or lower-dimensional results refuse.

Shared components are exact NumberField arithmetic, the accepted old independent
source and its Jarvis hull, and the independent endpoint-chain cover reader. No
source producer, polygon clipper or scientific point factory is imported. A source
construction alone makes no coverage or packing claim; external execution limits
and a separately authorized scientific protocol remain necessary.
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from copy import deepcopy
from fractions import Fraction
from itertools import combinations
from typing import Any

from devtools import check_h124_cover_source as old_reader
from devtools.check_closed_polygon_cover import check_packet as check_closed_cover
from sqpack.field import FieldElement, NumberField

type Point = tuple[FieldElement, FieldElement]
type Polygon = tuple[Point, ...]
type Plane = tuple[int, int, FieldElement]

NORMALS = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1))
BASE_IDS = (
    "obstacle",
    "B",
    "C0",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "corner-B",
    "corner-D",
    "corner-F",
)
MAX_NOMINAL_VERTICES = 32
MAX_COLLISION_VERTICES = 8
MAX_TOTAL_VERTICES = 68
INPUT_BITS, INPUT_CHARS, DERIVED_BITS = 128, 80, 4096


class SourceError(ValueError):
    """The bounded exact source contract could not be reconstructed."""


def _scalar(raw: Any, field: NumberField, *, bits: int = INPUT_BITS) -> FieldElement:
    if (
        not isinstance(raw, FieldElement)
        or raw.field is not field
        or len(raw.coeffs) != field.degree
        or any(
            max(value.numerator.bit_length(), value.denominator.bit_length()) > bits
            for value in raw.coeffs
        )
    ):
        raise SourceError("coordinate must be a bounded element of the same exact field")
    return raw


def _points(raw: Any, *, limit: int = MAX_NOMINAL_VERTICES) -> Polygon:
    if not isinstance(raw, (tuple, list)) or not 1 <= len(raw) <= limit:
        raise SourceError("point inventory must be nonempty and bounded")
    result: list[Point] = []
    field: NumberField | None = None
    for point in raw:
        if not isinstance(point, (tuple, list)) or len(point) != 2:
            raise SourceError("point needs two exact coordinates")
        if not isinstance(point[0], FieldElement):
            raise SourceError("point needs exact field coordinates")
        if field is None:
            field = point[0].field
            if type(field) is not NumberField or not 1 <= field.degree <= 2:
                raise SourceError("generic geometry admits validated degree-one or two fields")
        result.append((_scalar(point[0], field), _scalar(point[1], field)))
    return tuple(result)


def support_planes(
    nominal: Sequence[Point],
    *,
    half_width: FieldElement,
    diagonal_scale: FieldElement,
    displacement: FieldElement,
) -> tuple[Plane, ...]:
    """Form all eight bounds with signed minima and an l1 displacement penalty.

    The generic support template is a*||n||1 + a*d*||n||infinity. Its scientific
    specialization supplies d=sqrt(2); unrelated fields and positive d are useful
    controls without constructing that source.
    """
    vertices = _points(nominal)
    field = vertices[0][0].field
    a = _scalar(half_width, field)
    d = _scalar(diagonal_scale, field)
    epsilon = _scalar(displacement, field)
    if a <= 0 or d <= 0 or epsilon < 0:
        raise SourceError("support widths must be positive and displacement nonnegative")
    result: list[Plane] = []
    for nx, ny in NORMALS:
        l1, linfinity = abs(nx) + abs(ny), max(abs(nx), abs(ny))
        bound = (
            a * l1
            + a * d * linfinity
            + min(nx * x + ny * y for x, y in vertices)
            - epsilon * l1
        )
        result.append((nx, ny, _scalar(bound, field)))
    return tuple(result)


def _planes(raw: Any) -> tuple[Plane, ...]:
    if not isinstance(raw, (tuple, list)) or len(raw) != len(NORMALS):
        raise SourceError("all eight supporting half-planes are required")
    result: dict[tuple[int, int], FieldElement] = {}
    field: NumberField | None = None
    for plane in raw:
        if not isinstance(plane, (tuple, list)) or len(plane) != 3:
            raise SourceError("half-plane needs an integer normal and exact bound")
        nx, ny, bound = plane
        if type(nx) is not int or type(ny) is not int or (nx, ny) not in NORMALS:
            raise SourceError("normal must be one of the eight signed axes and diagonals")
        if (nx, ny) in result:
            raise SourceError("duplicate supporting normal")
        if not isinstance(bound, FieldElement):
            raise SourceError("half-plane bound must be exact")
        if field is None:
            field = bound.field
            if type(field) is not NumberField or not 1 <= field.degree <= 2:
                raise SourceError("generic geometry admits validated degree-one or two fields")
        result[nx, ny] = _scalar(bound, field)
    return tuple((nx, ny, result[nx, ny]) for nx, ny in NORMALS)


def _positive_hull(vertices: Sequence[Point]) -> Polygon:
    hull = old_reader.convex_hull(vertices)
    if len(hull) < 3:
        raise SourceError("collision intersection must have positive area")
    field = hull[0][0].field
    area_twice = sum(
        (a[0] * b[1] - a[1] * b[0] for a, b in zip(hull, (*hull[1:], hull[0]), strict=True)),
        field.zero,
    )
    if area_twice <= 0:
        raise SourceError("collision intersection must have positive area")
    return hull


def intersect_halfplanes(planes: Sequence[Plane]) -> Polygon:
    """Enumerate all line pairs and retain only points in every closed half-plane.

    Complete opposite axis normals make the intersection bounded. Every vertex of
    a positive-area bounded polygon occurs at an independent supporting-line pair;
    parallel pairs can therefore be skipped without losing any extreme point.
    """
    complete = _planes(planes)
    field = complete[0][2].field
    vertices: set[Point] = set()
    for (a, b, first), (c, d, second) in combinations(complete, 2):
        determinant = a * d - b * c
        if determinant == 0:
            continue
        x = _scalar((first * d - b * second) / determinant, field, bits=DERIVED_BITS)
        y = _scalar((a * second - first * c) / determinant, field, bits=DERIVED_BITS)
        if all(nx * x + ny * y <= bound for nx, ny, bound in complete):
            vertices.add((x, y))
    hull = _positive_hull(tuple(vertices))
    if len(hull) > MAX_COLLISION_VERTICES:
        raise SourceError("collision polygon exceeds the eight-vertex contract")
    return hull


def _wire_scalar(raw: Any, field: NumberField) -> FieldElement:
    if type(raw) is not list or len(raw) != field.degree:
        raise SourceError("wire coefficient inventory must equal the field degree")
    coefficients: list[Fraction] = []
    for text in raw:
        if (
            type(text) is not str
            or len(text) > INPUT_CHARS
            or re.fullmatch(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?", text) is None
        ):
            raise SourceError("wire rational needs bounded canonical ASCII syntax")
        value = Fraction(text)
        if (
            str(value) != text
            or max(value.numerator.bit_length(), value.denominator.bit_length()) > INPUT_BITS
        ):
            raise SourceError("wire rational is noncanonical or exceeds its bit cap")
        coefficients.append(value)
    return field.element(coefficients)


def _wire_polygon(raw: Any, field: NumberField) -> Polygon:
    if type(raw) is not list or not 3 <= len(raw) <= MAX_TOTAL_VERTICES:
        raise SourceError("source polygon needs a bounded positive-area boundary")
    vertices: list[Point] = []
    for point in raw:
        if type(point) is not list or len(point) != 2:
            raise SourceError("wire point needs two coordinates")
        vertices.append((_wire_scalar(point[0], field), _wire_scalar(point[1], field)))
    if tuple(vertices) != _positive_hull(vertices):
        raise SourceError("source boundary must be strict CCW with its lexicographic start")
    return tuple(vertices)


def append_collision(polygons: Any, collision: Sequence[Point]) -> list[dict[str, Any]]:
    """Preserve all thirteen named inputs and append a canonical positive-area region."""
    vertices = _positive_hull(_points(collision, limit=MAX_COLLISION_VERTICES))
    field = vertices[0][0].field
    if type(polygons) is not list or len(polygons) != len(BASE_IDS):
        raise SourceError("all thirteen unchanged source regions are required")
    total = len(vertices)
    for expected, entry in zip(BASE_IDS, polygons, strict=True):
        if (
            type(entry) is not dict
            or set(entry) != {"id", "vertices"}
            or entry["id"] != expected
        ):
            raise SourceError("source region identity or ordering differs from the old source")
        raw_vertices = entry["vertices"]
        if type(raw_vertices) is not list:
            raise SourceError("source vertices must be a list")
        total += len(raw_vertices)
        if total > MAX_TOTAL_VERTICES:
            raise SourceError("augmented source exceeds its 68-vertex admission cap")
        _wire_polygon(raw_vertices, field)
    result = deepcopy(polygons)
    result.append(
        {
            "id": "collision",
            "vertices": [
                [
                    [str(coefficient) for coefficient in _scalar(value, field).coeffs]
                    for value in point
                ]
                for point in vertices
            ],
        }
    )
    return result


def cover_source() -> tuple[NumberField, list, list]:
    """SCIENTIFIC: reconstruct the fixed axis-frame 14-region source, only on demand."""
    field, rectangle, polygons = old_reader.cover_source("axis")
    declaration = field.precondition_certificate()
    if (
        field.degree != 2
        or declaration["normalized_minimal_polynomial"] != ["1", "0", "-2"]
        or declaration["declared_isolating_interval"] != ["1", "2"]
    ):
        raise SourceError("old source must retain its declared positive sqrt(2) field")
    one = field.one
    q = field.rational("1939/500")
    m, r = q / 2, field.alpha / 2
    k = (one + m) / 2
    nominal = ((k, k - r), (2 * r, r), (m + one - 2 * r, r))
    endpoint = field.rational("110880/50803079")
    half_width = (one + endpoint**2) / (2 * (one + 2 * endpoint - endpoint**2))
    planes = support_planes(
        nominal,
        half_width=half_width,
        diagonal_scale=field.alpha,
        displacement=field.rational("1/500"),
    )
    collision = intersect_halfplanes(planes)
    return field, rectangle, append_collision(polygons, collision)


def check_packet(raw: Any) -> dict[str, Any]:
    """SCIENTIFIC: bind the independently reconstructed source before endpoint replay."""
    field, rectangle, polygons = cover_source()
    return check_closed_cover(raw, field=field, rectangle=rectangle, polygons=polygons)
