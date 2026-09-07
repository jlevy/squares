"""Unrelated exact clipping controls; both scientific source factories stay forbidden."""

from __future__ import annotations

import importlib
from copy import deepcopy
from fractions import Fraction
from typing import Any
from unittest.mock import patch

import pytest

from devtools import h124_collision_source as source
from devtools import h124_cover_source as old_source
from sqpack.field import FieldElement, NumberField


@pytest.fixture(autouse=True)
def forbid_scientific_factories(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*_args: Any, **_kwargs: Any) -> Any:
        raise AssertionError("scientific construction is forbidden in these controls")

    monkeypatch.setattr(source, "cover_source", forbidden)
    monkeypatch.setattr(old_source, "cover_source", forbidden)
    monkeypatch.setattr(old_source, "point_sets", forbidden)


@pytest.fixture
def field() -> NumberField:
    return NumberField((1, 0), (-1, 1))


def point(field: NumberField, x: int | Fraction, y: int | Fraction) -> source.Point:
    return field.rational(x), field.rational(y)


def box_planes(field: NumberField, width: int = 2) -> list[source.HalfPlane]:
    q = field.rational
    return [
        (q(1), q(0), q(width)),
        (q(-1), q(0), q(0)),
        (q(0), q(1), q(width)),
        (q(0), q(-1), q(0)),
    ]


def test_axis_bounds_give_canonical_closed_rectangle(field: NumberField) -> None:
    result = source.axis_bounded_intersection(box_planes(field))
    assert result == tuple(point(field, x, y) for x, y in ((0, 0), (2, 0), (2, 2), (0, 2)))


def test_diagonal_clip_has_exact_crossings_and_closed_endpoints(field: NumberField) -> None:
    q = field.rational
    result = source.axis_bounded_intersection([*box_planes(field), (q(1), q(1), q(3))])
    assert result == tuple(
        point(field, x, y) for x, y in ((0, 0), (2, 0), (2, 1), (1, 2), (0, 2))
    )


def test_four_diagonal_clips_produce_eight_distinct_ccw_vertices(field: NumberField) -> None:
    q = field.rational
    planes = [
        *box_planes(field),
        (q(1), q(1), q(Fraction(7, 2))),
        (q(-1), q(-1), q(Fraction(-1, 2))),
        (q(1), q(-1), q(Fraction(3, 2))),
        (q(-1), q(1), q(Fraction(3, 2))),
    ]
    half = Fraction(1, 2)
    expected = tuple(
        point(field, x, y)
        for x, y in (
            (0, half),
            (half, 0),
            (2 - half, 0),
            (2, half),
            (2, 2 - half),
            (2 - half, 2),
            (half, 2),
            (0, 2 - half),
        )
    )
    assert source.axis_bounded_intersection(planes) == expected
    assert source.axis_bounded_intersection(planes[:4] + list(reversed(planes[4:]))) == expected


def test_redundant_parallel_and_vertex_touching_constraints_do_not_duplicate(
    field: NumberField,
) -> None:
    q = field.rational
    planes = [*box_planes(field), (q(2), q(0), q(4)), (q(1), q(1), q(4))]
    assert source.axis_bounded_intersection(planes) == source.axis_bounded_intersection(
        box_planes(field)
    )


@pytest.mark.parametrize("bound", [-1, 0])
def test_empty_and_single_point_intersections_refuse(field: NumberField, bound: int) -> None:
    q = field.rational
    with pytest.raises(source.SourceError, match="positive area"):
        source.axis_bounded_intersection([*box_planes(field), (q(1), q(1), q(bound))])


def test_segment_intersection_refuses_instead_of_being_dropped(field: NumberField) -> None:
    q = field.rational
    with pytest.raises(source.SourceError, match="positive area"):
        source.axis_bounded_intersection([*box_planes(field), (q(1), q(0), q(0))])


def test_exact_thin_positive_area_is_retained(field: NumberField) -> None:
    q = field.rational
    tiny = Fraction(1, 2**100)
    result = source.axis_bounded_intersection([*box_planes(field), (q(1), q(0), q(tiny))])
    assert result == tuple(
        point(field, x, y) for x, y in ((0, 0), (tiny, 0), (tiny, 2), (0, 2))
    )


def test_nonrational_sqrt3_cut_and_full_coefficient_wire() -> None:
    field = NumberField((1, 0, -3), (1, 2))
    q, root = field.rational, field.alpha
    result = source.axis_bounded_intersection([*box_planes(field), (root, q(1), root)])
    assert result == ((q(0), q(0)), (q(1), q(0)), (q(0), root))
    assert source.wire_point(result[-1]) == [["0", "0"], ["0", "1"]]


def test_nominal_support_minima_include_ties_and_l1_margin(field: NumberField) -> None:
    q = field.rational
    nominal = [point(field, 0, 0), point(field, 1, 0), point(field, 0, 1)]
    supports = [q(4)] * 8
    planes = source.support_halfplanes(nominal, supports, Fraction(1, 4))
    expected = [
        Fraction(15, 4),
        Fraction(11, 4),
        Fraction(15, 4),
        Fraction(11, 4),
        Fraction(7, 2),
        Fraction(5, 2),
        Fraction(5, 2),
        Fraction(5, 2),
    ]
    assert [c for _, _, c in planes] == [q(value) for value in expected]
    assert [(a, b) for a, b, _ in planes] == [(q(x), q(y)) for x, y in source.NORMALS]
    assert source.support_halfplanes([*nominal, nominal[0]], supports, Fraction(1, 4)) == planes


def test_nonrational_nominal_minima_use_real_order_not_coefficient_order() -> None:
    field = NumberField((1, 0, -3), (1, 2))
    root, zero = field.alpha, field.zero
    nominal = [(root, zero), (field.one, zero)]
    planes = source.support_halfplanes(nominal, [field.rational(5)] * 8, Fraction(0))
    assert planes[0][2] == 6
    assert planes[1][2] == 5 - root


@pytest.mark.parametrize("margin", [Fraction(-1), 0.1, True, "1/4", Fraction(1, 2**129)])
def test_margin_requires_bounded_nonnegative_fraction(field: NumberField, margin: Any) -> None:
    with pytest.raises(source.SourceError):
        source.support_halfplanes([point(field, 0, 0)], [field.one] * 8, margin)


@pytest.mark.parametrize("count", [0, 7, 9])
def test_support_inventory_is_exactly_eight(field: NumberField, count: int) -> None:
    with pytest.raises(source.SourceError, match="eight"):
        source.support_halfplanes([point(field, 0, 0)], [field.one] * count, Fraction(0))


def test_bounded_shapes_and_foreign_fields_refuse_before_geometry(field: NumberField) -> None:
    foreign = NumberField((1, 0), (-1, 1))
    q = field.rational
    malformed: list[Any] = [
        [],
        box_planes(field)[:3],
        box_planes(field) * 3,
        [*box_planes(field), (0.5, q(0), q(1))],
        [*box_planes(field), (q(0), q(0), q(1))],
        [*box_planes(field), (foreign.one, q(0), q(1))],
        [*box_planes(field), (q(1), q(0))],
        [*box_planes(field), (q(1), q(0), q(2**128))],
    ]
    for planes in malformed:
        with pytest.raises(source.SourceError):
            source.axis_bounded_intersection(planes)
    with pytest.raises(source.SourceError):
        source.support_halfplanes([point(field, 0, 0)] * 17, [q(1)] * 8, Fraction(0))
    with pytest.raises(source.SourceError):
        source.support_halfplanes([(foreign.one, q(0))], [q(1)] * 8, Fraction(0))


def test_missing_or_reversed_axis_bounds_refuse(field: NumberField) -> None:
    planes = box_planes(field)
    planes[0], planes[1] = planes[1], planes[0]
    with pytest.raises(source.SourceError, match="axis"):
        source.axis_bounded_intersection(planes)
    planes = box_planes(field)
    planes[0] = field.one, field.zero, -field.one
    with pytest.raises(source.SourceError, match="positive area"):
        source.axis_bounded_intersection(planes)


def test_generic_output_passes_complete_source_validator(field: NumberField) -> None:
    polygon = source.axis_bounded_intersection(box_planes(field))
    rectangle = [source.wire_point(point(field, 0, 0)), source.wire_point(point(field, 2, 2))]
    regions = [{"id": "unrelated", "vertices": [source.wire_point(p) for p in polygon]}]
    assert len(source.validate_source(field, rectangle, regions).polygons) == 1


def test_generic_operations_neither_construct_fields_nor_access_files(
    field: NumberField,
) -> None:
    planes = box_planes(field)
    with (
        patch.object(NumberField, "__init__", side_effect=AssertionError("field factory")),
        patch("builtins.open", side_effect=AssertionError("file access")),
        patch("io.open", side_effect=AssertionError("file access")),
    ):
        assert len(source.axis_bounded_intersection(planes)) == 4


def test_arithmetic_interruption_propagates_without_partial_polygon(
    field: NumberField,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    planes = box_planes(field)

    def interrupted(*_args: Any, **_kwargs: Any) -> Any:
        raise TimeoutError("unrelated toy interruption")

    monkeypatch.setattr(field, "sign", interrupted)
    with pytest.raises(TimeoutError):
        source.axis_bounded_intersection(planes)


def test_import_has_no_scientific_factory_or_field_construction(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    with patch.object(NumberField, "__init__", side_effect=AssertionError("field factory")):
        importlib.reload(source)

    def forbidden(*_args: Any, **_kwargs: Any) -> Any:
        raise AssertionError("scientific construction remains forbidden after reload")

    monkeypatch.setattr(source, "cover_source", forbidden)
    assert source.SOURCE_FIELD_DEGREE == 2
    assert source.SOURCE_VERTEX_BOUND == 68
    assert (*old_source.POLYGON_IDS, "collision") == source.POLYGON_IDS


def toy_base(field: NumberField, pentagons: int = 0) -> tuple[list, list[dict[str, Any]]]:
    q = field.rational
    square = source.axis_bounded_intersection(box_planes(field))
    pentagon = source.axis_bounded_intersection([*box_planes(field), (q(1), q(1), q(3))])
    rectangle = [source.wire_point(point(field, 0, 0)), source.wire_point(point(field, 2, 2))]
    regions = [
        {
            "id": name,
            "vertices": [source.wire_point(p) for p in (pentagon if i < pentagons else square)],
        }
        for i, name in enumerate(source.POLYGON_IDS[:-1])
    ]
    return rectangle, regions


def test_assembly_preserves_entire_prefix_without_mutation(field: NumberField) -> None:
    rectangle, regions = toy_base(field)
    before = deepcopy((rectangle, regions))
    polygon = source.axis_bounded_intersection(box_planes(field))
    result = source.append_collision_region(field, rectangle, regions, polygon)
    assert len(result) == 14
    assert result[-1]["id"] == "collision"
    assert (rectangle, regions) == before
    assert all(new is old for new, old in zip(result[:-1], regions, strict=True))
    assert result[-1]["vertices"] == [source.wire_point(p) for p in polygon]


def test_exact_declared_total_vertex_limit_is_admitted(field: NumberField) -> None:
    rectangle, regions = toy_base(field, pentagons=8)
    q = field.rational
    planes = [
        *box_planes(field),
        (q(1), q(1), q(Fraction(7, 2))),
        (q(-1), q(-1), q(Fraction(-1, 2))),
        (q(1), q(-1), q(Fraction(3, 2))),
        (q(-1), q(1), q(Fraction(3, 2))),
    ]
    polygon = source.axis_bounded_intersection(planes)
    result = source.append_collision_region(field, rectangle, regions, polygon)
    assert sum(len(entry["vertices"]) for entry in result) == 68


def test_old_vertex_cap_refuses_before_appending(field: NumberField) -> None:
    rectangle, regions = toy_base(field, pentagons=9)
    with pytest.raises(source.SourceError, match="sixty"):
        source.append_collision_region(
            field, rectangle, regions, source.axis_bounded_intersection(box_planes(field))
        )


@pytest.mark.parametrize("mutation", ["missing", "foreign", "reordered", "duplicate"])
def test_full_old_inventory_cannot_be_replaced_or_omitted(
    field: NumberField, mutation: str
) -> None:
    rectangle, regions = toy_base(field)
    if mutation == "missing":
        regions.pop()
    elif mutation == "foreign":
        regions[0]["id"] = "foreign"
    elif mutation == "reordered":
        regions.reverse()
    else:
        regions[-1]["id"] = regions[0]["id"]
    with pytest.raises(ValueError, match=r"inventory|unique"):
        source.append_collision_region(
            field, rectangle, regions, source.axis_bounded_intersection(box_planes(field))
        )


@pytest.mark.parametrize("count", [0, 1, 2, 9])
def test_appended_polygon_vertex_inventory_refuses(field: NumberField, count: int) -> None:
    rectangle, regions = toy_base(field)
    with pytest.raises(source.SourceError, match="three through eight"):
        source.append_collision_region(field, rectangle, regions, [point(field, 0, 0)] * count)


def test_appended_polygon_requires_same_field_and_positive_area(field: NumberField) -> None:
    rectangle, regions = toy_base(field)
    foreign = NumberField((1, 0), (-1, 1))
    with pytest.raises(source.SourceError, match="exact field"):
        source.append_collision_region(
            field, rectangle, regions, source.axis_bounded_intersection(box_planes(foreign))
        )
    with pytest.raises(source.SourceError, match="positive area"):
        source.append_collision_region(
            field, rectangle, regions, [point(field, i, 0) for i in range(3)]
        )


def test_oversized_declared_field_refuses_before_clipping() -> None:
    large = 2**128
    field = NumberField((1, -large), (large - 1, large + 1))
    with pytest.raises(ValueError, match="bit cap"):
        source.axis_bounded_intersection(box_planes(field))


def test_degree_five_field_refuses_before_clipping() -> None:
    field = NumberField((1, 0, 0, 0, 0, -2), (1, 2))
    with pytest.raises(source.SourceError, match="degree"):
        source.axis_bounded_intersection(box_planes(field))


@pytest.mark.parametrize("coefficients", [[Fraction(0)], [0.0, 1.0]])
def test_incomplete_or_approximate_coefficient_vectors_refuse(coefficients: Any) -> None:
    field = NumberField((1, 0, -3), (1, 2))
    malformed = FieldElement(field, coefficients)
    with pytest.raises(source.SourceError, match="coefficient vectors"):
        source.wire_point((malformed, field.zero))
