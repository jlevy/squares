"""Unrelated exact geometry controls; the scientific H124 constructor is forbidden."""

from __future__ import annotations

from fractions import Fraction
from typing import Any
from unittest.mock import patch

import pytest

from devtools import h124_cover_source as source
from sqpack.field import NumberField


@pytest.fixture(autouse=True)
def forbid_scientific_constructor(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*_args: Any, **_kwargs: Any) -> Any:
        raise AssertionError(
            "scientific H124 construction is forbidden in source-free controls"
        )

    monkeypatch.setattr(source, "cover_source", forbidden)
    monkeypatch.setattr(source, "point_sets", forbidden)


def test_hull_removes_duplicates_and_collinear_points_and_starts_lexically() -> None:
    field = NumberField((1, 0), (-1, 1))

    def point(x: int, y: int):
        return field.rational(x), field.rational(y)

    cloud = [point(2, 2), point(0, 0), point(1, 0), point(0, 2), point(2, 0), point(0, 0)]
    assert source.convex_hull(cloud) == (point(0, 0), point(2, 0), point(2, 2), point(0, 2))


@pytest.fixture
def field() -> NumberField:
    return NumberField((1, 0, -2), (1, 2))


def point(field: NumberField, x: int | Fraction, y: int | Fraction) -> source.Point:
    return field.rational(x), field.rational(y)


def test_minkowski_sum_has_hand_computed_pentagon_boundary(field: NumberField) -> None:
    triangle = tuple(point(field, x, y) for x, y in ((0, 0), (2, 0), (0, 1)))
    rectangle = tuple(point(field, x, y) for x, y in ((0, 0), (1, 0), (1, 2), (0, 2)))
    expected = tuple(point(field, x, y) for x, y in ((0, 0), (3, 0), (3, 2), (1, 3), (0, 3)))
    assert source.minkowski_sum(triangle, rectangle) == expected
    assert source.minkowski_sum(rectangle, triangle) == expected


def test_hull_is_independent_of_input_order_and_uses_exact_real_order(
    field: NumberField,
) -> None:
    root = field.alpha
    zero, one = field.zero, field.one
    cloud = [(root, one), (zero, zero), (root, zero), (zero, one), (one, one / 2)]
    expected = ((zero, zero), (root, zero), (root, one), (zero, one))
    assert source.convex_hull(cloud) == expected
    assert source.convex_hull(tuple(reversed(cloud))) == expected
    assert source.convex_hull(cloud[2:] + cloud[:2]) == expected


def test_nonrational_translation_preserves_canonical_boundary(field: NumberField) -> None:
    triangle = tuple(point(field, x, y) for x, y in ((0, 0), (1, 0), (0, 2)))
    shift = field.alpha, -field.alpha
    result = source.translate(triangle, shift)
    assert result == (
        shift,
        (field.alpha + 1, -field.alpha),
        (field.alpha, 2 - field.alpha),
    )
    assert source.translate(result, (-shift[0], -shift[1])) == triangle


def test_centered_axis_and_diagonal_squares_have_known_vertices(field: NumberField) -> None:
    half = Fraction(1, 3)
    assert source.centered_square(field, half, "axis") == tuple(
        point(field, x, y)
        for x, y in ((-half, -half), (half, -half), (half, half), (-half, half))
    )
    height = field.alpha / 3
    zero = field.zero
    assert source.centered_square(field, half, "diagonal") == (
        (-height, zero),
        (zero, -height),
        (height, zero),
        (zero, height),
    )


def test_closed_rectangle_clipping_has_known_boundary(field: NumberField) -> None:
    first = (point(field, 0, 0), point(field, 3, 4))
    second = (point(field, 2, -1), point(field, 4, 2))
    expected = tuple(point(field, x, y) for x, y in ((2, 0), (3, 0), (3, 2), (2, 2)))
    assert source.intersect_rectangles(first, second) == expected
    assert source.intersect_rectangles(second, first) == expected
    assert source.intersect_rectangles(first, first) == source.rectangle_polygon(first)


def test_tiny_positive_area_is_not_collapsed(field: NumberField) -> None:
    tiny = Fraction(1, 2**100)
    expected = (point(field, 0, 0), point(field, tiny, 0), point(field, 0, 1))
    assert source.convex_hull(tuple(reversed(expected))) == expected


@pytest.mark.parametrize("vertices", [[], [(0, 0)], [(0, 0), (1, 1)], [(0, 0), (1, 1), (2, 2)]])
def test_degenerate_hulls_refuse(field: NumberField, vertices: list[tuple[int, int]]) -> None:
    with pytest.raises(source.SourceError):
        source.convex_hull([point(field, x, y) for x, y in vertices])


@pytest.mark.parametrize("frame", ["near45", "axis ", "", False, None])
def test_closed_frame_selector_refuses_foreign_values(field: NumberField, frame: Any) -> None:
    with pytest.raises(source.SourceError, match="exactly axis or diagonal"):
        source.centered_square(field, Fraction(1, 3), frame)


@pytest.mark.parametrize("half", [Fraction(0), Fraction(-1, 3), 0.5, True])
def test_kernel_width_requires_positive_exact_fraction(field: NumberField, half: Any) -> None:
    with pytest.raises(source.SourceError, match="positive rational"):
        source.centered_square(field, half, "axis")


@pytest.mark.parametrize(
    ("polynomial", "interval"), [((1, 0, -2), (-2, -1)), ((1, 0, -3), (1, 2))]
)
def test_diagonal_requires_the_correct_positive_root(
    polynomial: tuple[int, ...], interval: tuple[int, int]
) -> None:
    wrong = NumberField(polynomial, interval)
    with pytest.raises(source.SourceError, match="positive square root of two"):
        source.centered_square(wrong, Fraction(1, 3), "diagonal")


def test_foreign_fields_cannot_mix_in_any_geometry_operation(field: NumberField) -> None:
    foreign = NumberField((1, 0, -2), (1, 2))
    left = source.centered_square(field, Fraction(1, 3), "axis")
    right = source.centered_square(foreign, Fraction(1, 3), "axis")
    with pytest.raises(source.SourceError, match="same"):
        source.convex_hull([*left, right[0]])
    with pytest.raises(source.SourceError, match="same"):
        source.minkowski_sum(left, right)
    with pytest.raises(source.SourceError, match="exact field"):
        source.translate(left, right[0])
    with pytest.raises(source.SourceError, match="same"):
        source.intersect_rectangles((left[0], left[2]), (right[0], right[2]))


@pytest.mark.parametrize("bounds", [((0, 0), (0, 1)), ((0, 0), (1, 0)), ((1, 0), (0, 1))])
def test_rectangle_must_have_positive_extent(
    field: NumberField, bounds: tuple[tuple[int, int], tuple[int, int]]
) -> None:
    with pytest.raises(source.SourceError, match="positive width and height"):
        source.rectangle_polygon(tuple(point(field, x, y) for x, y in bounds))


@pytest.mark.parametrize("left", [1, 2])
def test_empty_or_boundary_only_rectangle_intersection_refuses(
    field: NumberField, left: int
) -> None:
    first = (point(field, 0, 0), point(field, 1, 1))
    second = (point(field, left, 0), point(field, left + 1, 1))
    with pytest.raises(source.SourceError, match="positive width and height"):
        source.intersect_rectangles(first, second)


def test_geometry_lexical_shapes_and_point_cap_refuse_before_arithmetic(
    field: NumberField,
) -> None:
    malformed: list[Any] = [[], [(1.0, 0.0)], [(field.zero,)], [point(field, 0, 0)] * 257]
    for raw in malformed:
        with pytest.raises(source.SourceError):
            source.convex_hull(raw)


def test_minkowski_enumeration_cap_refuses_without_partial_output(field: NumberField) -> None:
    parabola = tuple(point(field, index, index * index) for index in range(17))
    assert len(source.convex_hull(parabola)) == 17
    with pytest.raises(source.SourceError, match="Minkowski point inventory"):
        source.minkowski_sum(parabola, parabola)


def test_full_length_wire_and_generic_cover_source_admission(field: NumberField) -> None:
    bounds = (point(field, 0, 0), point(field, 2, 1))
    kernel = source.centered_square(field, Fraction(1, 2), "axis")
    polygons = [
        {
            "id": name,
            "vertices": [
                source.wire_point(vertex)
                for vertex in source.translate(kernel, point(field, x, Fraction(1, 2)))
            ],
        }
        for name, x in (("left", Fraction(1, 2)), ("right", Fraction(3, 2)))
    ]
    rectangle = [source.wire_point(vertex) for vertex in bounds]
    validated = source.validate_source(field, rectangle, polygons)
    assert len(validated.polygons) == 2
    assert rectangle == [[["0", "0"], ["0", "0"]], [["2", "0"], ["1", "0"]]]
    assert source.wire_point((field.alpha, field.one)) == [["0", "1"], ["1", "0"]]


def test_generic_helpers_do_not_construct_fields_or_access_inputs(field: NumberField) -> None:
    bounds = (point(field, 0, 0), point(field, 1, 1))
    shift = point(field, -1, 2)
    with (
        patch.object(
            NumberField, "__init__", side_effect=AssertionError("field construction forbidden")
        ),
        patch("builtins.open", side_effect=AssertionError("input access forbidden")),
        patch("io.open", side_effect=AssertionError("input access forbidden")),
    ):
        square = source.rectangle_polygon(bounds)
        result = source.minkowski_sum(square, source.translate(square, shift))
        assert result == tuple(
            point(field, x, y) for x, y in ((-1, 2), (1, 2), (1, 4), (-1, 4))
        )


def test_exact_arithmetic_interruption_does_not_return_a_hull(
    field: NumberField, monkeypatch: pytest.MonkeyPatch
) -> None:
    points = tuple(point(field, x, y) for x, y in ((0, 0), (1, 0), (0, 1)))

    def interrupted(*_args: Any, **_kwargs: Any) -> Any:
        raise TimeoutError("toy arithmetic cap")

    monkeypatch.setattr(field, "sign", interrupted)
    with pytest.raises(TimeoutError):
        source.convex_hull(points)
