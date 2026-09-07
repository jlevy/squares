"""Generic geometry and mocked binding only; the H124 constructor is forbidden."""

from __future__ import annotations

import runpy
from copy import deepcopy
from typing import Any

import pytest

from devtools import check_h124_cover_source as source_reader
from devtools.check_closed_polygon_cover import GuardError
from sqpack.field import NumberField


@pytest.fixture(autouse=True)
def forbid_scientific_constructor(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*_args: Any, **_kwargs: Any) -> Any:
        raise AssertionError("scientific source construction is not authorized")

    monkeypatch.setattr(source_reader, "cover_source", forbidden)


def points(field: NumberField, values: list[tuple[int | str, int | str]]) -> tuple:
    return tuple((field.rational(x), field.rational(y)) for x, y in values)


def test_hull_canonicalizes_clockwise_duplicates_collinear_and_interior_points() -> None:
    field = NumberField((1, 0), (-1, 1))
    cloud = points(field, [(0, 2), (3, 2), (3, 0), (0, 0), (1, 0), (1, 1), (0, 0)])
    assert source_reader.convex_hull(cloud) == points(field, [(0, 0), (3, 0), (3, 2), (0, 2)])
    assert source_reader.convex_hull(tuple(reversed(cloud))) == source_reader.convex_hull(cloud)
    assert source_reader.convex_hull(points(field, [(2, 1), (0, 1), (1, 1)])) == points(
        field, [(0, 1), (2, 1)]
    )
    assert source_reader.convex_hull(points(field, [(1, 2), (1, 2)])) == points(field, [(1, 2)])
    assert source_reader.convex_hull(()) == ()


def test_unrelated_quadratic_hull_uses_real_lexicographic_order() -> None:
    field = NumberField((1, 0, -3), (1, 2))
    low, high = 2 - field.alpha, field.alpha - 1
    cloud = ((high, field.one), (low, field.zero), (high, field.zero), (low, field.one))
    result = source_reader.convex_hull(cloud)
    assert result == (
        (low, field.zero),
        (high, field.zero),
        (high, field.one),
        (low, field.one),
    )
    assert result[0][0].coeffs > result[1][0].coeffs


def test_minkowski_hull_and_translation_are_exact() -> None:
    field = NumberField((1, 0), (-1, 1))
    triangle = points(field, [(0, 0), (2, 0), (0, 2)])
    box = points(field, [(-1, -1), (1, -1), (1, 1), (-1, 1)])
    assert source_reader.minkowski_sum(triangle, box) == points(
        field, [(-1, -1), (3, -1), (3, 1), (1, 3), (-1, 3)]
    )
    assert source_reader.minkowski_sum(triangle, points(field, [(5, -2)])) == points(
        field, [(5, -2), (7, -2), (5, 0)]
    )
    assert source_reader.minkowski_sum(triangle, ()) == ()


def test_closed_clipping_preserves_segments_singletons_and_empty_results() -> None:
    field = NumberField((1, 0), (-1, 1))
    zero, one = field.zero, field.one
    box = points(field, [(0, 0), (2, 0), (2, 2), (0, 2)])
    assert source_reader.clip_halfplane(box, (one, one, field.rational(2))) == points(
        field, [(0, 0), (2, 0), (0, 2)]
    )
    assert source_reader.clip_halfplane(box, (one, zero, zero)) == points(
        field, [(0, 0), (0, 2)]
    )
    assert source_reader.clip_halfplane(box, (one, one, zero)) == points(field, [(0, 0)])
    assert source_reader.clip_halfplane(box, (one, zero, -one)) == ()
    assert source_reader.clip_halfplane((), (one, zero, zero)) == ()


def test_rectangle_clip_and_non_axis_parallelogram() -> None:
    field = NumberField((1, 0, -3), (1, 2))
    box = points(field, [(-2, -2), (2, -2), (2, 2), (-2, 2)])
    rectangle = points(field, [(-1, 0), (1, 3)])
    assert source_reader.clip_rectangle(box, rectangle) == points(
        field, [(-1, 0), (1, 0), (1, 2), (-1, 2)]
    )
    u, v = (field.alpha, field.one), (-field.one, field.alpha)
    kernel = source_reader.centered_parallelogram(u, v)
    assert len(kernel) == 4
    assert set(kernel) == {
        (sx * u[0] + sy * v[0], sx * u[1] + sy * v[1])
        for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))
    }
    assert set(kernel) == {(-x, -y) for x, y in kernel}


def toy_source() -> tuple[NumberField, list, list]:
    field = NumberField((1, 0), (-1, 1))
    rectangle = points(field, [(-1, -1), (1, 1)])
    obstacle = points(field, [(-1, -1), (1, -1), (1, 1), (-1, 1)])
    kernel = obstacle
    marks = tuple((identity, (field.zero, field.zero)) for identity in source_reader.MARK_IDS)
    windows = tuple(
        (identity, points(field, [(-4, -4), (4, 4)])) for identity in source_reader.CORNER_IDS
    )
    rectangle_wire, polygons_wire = source_reader.assemble_source(
        rectangle, obstacle, kernel, marks, windows
    )
    return field, rectangle_wire, polygons_wire


def toy_packet(field: NumberField, rectangle: list, polygons: list) -> dict[str, Any]:
    descriptor = field.precondition_certificate()
    return {
        "kind": "closed-convex-polygon-cover/v1",
        "status": "covered",
        "field": {
            "minimal_polynomial": descriptor["normalized_minimal_polynomial"],
            "isolating_interval": descriptor["declared_isolating_interval"],
        },
        "rectangle": deepcopy(rectangle),
        "polygons": deepcopy(polygons),
        "slabs": [{"left": ["-1"], "right": ["1"], "chain": ["obstacle"]}],
        "stop_reason": "complete",
    }


def test_full_source_assembly_keeps_all_thirteen_ids_and_clips_only_corner_windows() -> None:
    _, rectangle, polygons = toy_source()
    assert [polygon["id"] for polygon in polygons] == [
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
    ]
    assert rectangle == [[["-1"], ["-1"]], [["1"], ["1"]]]
    assert polygons[0]["vertices"] == [
        [["-2"], ["-2"]],
        [["2"], ["-2"]],
        [["2"], ["2"]],
        [["-2"], ["2"]],
    ]
    expected_patch = [[["-1"], ["-1"]], [["1"], ["-1"]], [["1"], ["1"]], [["-1"], ["1"]]]
    assert all(polygon["vertices"] == expected_patch for polygon in polygons[-3:])


def test_assembly_refuses_missing_reordered_or_degenerate_regions() -> None:
    field = NumberField((1, 0), (-1, 1))
    rectangle = points(field, [(-1, -1), (1, 1)])
    box = points(field, [(-1, -1), (1, -1), (1, 1), (-1, 1)])
    marks = tuple((identity, (field.zero, field.zero)) for identity in source_reader.MARK_IDS)
    windows = tuple((identity, rectangle) for identity in source_reader.CORNER_IDS)
    for wrong_marks in (marks[:-1], tuple(reversed(marks))):
        with pytest.raises(source_reader.SourceError, match="inventory"):
            source_reader.assemble_source(rectangle, box, box, wrong_marks, windows)
    with pytest.raises(source_reader.SourceError, match="inventory"):
        source_reader.assemble_source(rectangle, box, box, marks, windows[:-1])
    empty_window = (source_reader.CORNER_IDS[0], points(field, [(5, 5), (6, 6)]))
    with pytest.raises(source_reader.SourceError, match="area"):
        source_reader.assemble_source(rectangle, box, box, marks, (empty_window, *windows[1:]))


@pytest.mark.parametrize("frame", ["axis", "diagonal"])
def test_binding_wrapper_accepts_mocked_complete_toy_source_only(
    frame: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    field, rectangle, polygons = toy_source()
    requested = []

    def reconstructed(name: str) -> tuple[NumberField, list, list]:
        requested.append(name)
        return field, rectangle, polygons

    monkeypatch.setattr(source_reader, "cover_source", reconstructed)
    raw = toy_packet(field, rectangle, polygons)
    result = source_reader.check_packet(raw, frame=frame)
    assert requested == [frame]
    assert result["status"] == "verified_cover"
    assert result["polygons_checked"] == 13
    raw["status"], raw["slabs"], raw["stop_reason"] = "unresolved", [], "no_chain"
    assert source_reader.check_packet(raw, frame=frame)["cover_proved"] is False


@pytest.mark.parametrize("mutation", ["missing", "mark", "corner", "field"])
def test_binding_wrapper_refuses_source_substitution(
    mutation: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    field, rectangle, polygons = toy_source()
    monkeypatch.setattr(
        source_reader, "cover_source", lambda _frame: (field, rectangle, polygons)
    )
    raw = toy_packet(field, rectangle, polygons)
    if mutation == "missing":
        raw["polygons"].pop()
    elif mutation == "mark":
        raw["polygons"][2]["id"] = "C"
    elif mutation == "corner":
        raw["polygons"][-1]["vertices"][0][0][0] = "0"
    else:
        raw["field"]["isolating_interval"] = ["-2", "2"]
    with pytest.raises(GuardError):
        source_reader.check_packet(raw, frame="axis")


@pytest.mark.parametrize("frame", ["near45", "Axis", "", None, True, 0])
def test_bad_frame_refused_before_scientific_constructor(frame: Any) -> None:
    with pytest.raises(source_reader.SourceError, match="frame"):
        source_reader.check_packet({}, frame=frame)


def test_generic_geometry_refuses_foreign_fields_and_floats() -> None:
    first = NumberField((1, 0), (-1, 1))
    second = NumberField((1, 0), (-1, 1))
    with pytest.raises(source_reader.SourceError, match="field"):
        source_reader.convex_hull(((first.zero, first.one), (second.zero, second.one)))
    malformed: Any = ((0.0, first.one),)
    with pytest.raises(source_reader.SourceError, match="exact"):
        source_reader.convex_hull(malformed)


def test_full_quadratic_coefficient_arrays_bind_an_unrelated_source(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    field = NumberField((1, 0, -3), (1, 2))
    root, one = field.alpha, field.one
    rectangle = ((-root, -one), (root, one))
    obstacle = ((-root, -one), (root, -one), (root, one), (-root, one))
    kernel = points(field, [(-1, -1), (1, -1), (1, 1), (-1, 1)])
    marks = tuple((identity, (field.zero, field.zero)) for identity in source_reader.MARK_IDS)
    windows = tuple((identity, rectangle) for identity in source_reader.CORNER_IDS)
    rectangle_wire, polygons = source_reader.assemble_source(
        rectangle, obstacle, kernel, marks, windows
    )
    assert polygons[0]["vertices"][0] == [["-1", "-1"], ["-2", "0"]]
    assert all(
        len(coordinate) == 2
        for polygon in polygons
        for point in polygon["vertices"]
        for coordinate in point
    )
    monkeypatch.setattr(
        source_reader, "cover_source", lambda _frame: (field, rectangle_wire, polygons)
    )
    raw = toy_packet(field, rectangle_wire, polygons)
    raw["slabs"] = [{"left": ["0", "-1"], "right": ["0", "1"], "chain": ["obstacle"]}]
    checked = source_reader.check_packet(raw, frame="diagonal")
    assert checked["cover_proved"] is True
    assert checked["polygons_checked"] == 13


def test_module_import_cannot_construct_a_field(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*_args: Any, **_kwargs: Any) -> None:
        raise AssertionError("import attempted scientific field construction")

    monkeypatch.setattr(NumberField, "__init__", forbidden)
    runpy.run_path(str(source_reader.__file__))
