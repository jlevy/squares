"""Unrelated exact geometry only; both scientific source factories are forbidden."""

from __future__ import annotations

import runpy
from copy import deepcopy
from typing import Any, cast

import pytest

from devtools import check_h124_collision_source as reader
from devtools import check_h124_cover_source as old_reader
from devtools.check_closed_polygon_cover import GuardError
from sqpack.field import NumberField


@pytest.fixture(autouse=True)
def forbid_scientific_factories(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*_args: Any, **_kwargs: Any) -> Any:
        raise AssertionError("scientific source construction is not authorized")

    monkeypatch.setattr(reader, "cover_source", forbidden)
    monkeypatch.setattr(old_reader, "cover_source", forbidden)


def points(field: NumberField, values: list[tuple[int | str, int | str]]) -> tuple:
    return tuple((field.rational(x), field.rational(y)) for x, y in values)


def box_planes(field: NumberField, *, bound: int = 1) -> tuple:
    return tuple((x, y, field.rational(bound * (abs(x) + abs(y)))) for x, y in reader.NORMALS)


def test_line_intersections_keep_closed_corners_and_canonical_orientation() -> None:
    field = NumberField((1, 0), (-1, 1))
    expected = points(field, [(-1, -1), (1, -1), (1, 1), (-1, 1)])
    assert reader.intersect_halfplanes(box_planes(field)) == expected
    assert reader.intersect_halfplanes(tuple(reversed(box_planes(field)))) == expected


def test_all_eight_constraints_cut_an_octagon() -> None:
    field = NumberField((1, 0), (-1, 1))
    planes = tuple((x, y, field.rational(3 if x and y else 2)) for x, y in reader.NORMALS)
    assert reader.intersect_halfplanes(planes) == points(
        field, [(-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1)]
    )


def test_unrelated_quadratic_bounds_use_the_declared_real_order() -> None:
    field = NumberField((1, 0, -3), (1, 2))
    low, high = 2 - field.alpha, field.alpha - 1
    planes = tuple((x, y, x * (high if x > 0 else low) + abs(y)) for x, y in reader.NORMALS)
    assert reader.intersect_halfplanes(planes) == (
        (low, -field.one),
        (high, -field.one),
        (high, field.one),
        (low, field.one),
    )


def test_support_bounds_use_minimum_signed_dot_and_l1_displacement() -> None:
    field = NumberField((1, 0, -3), (1, 2))
    nominal = points(field, [(-2, 1), (1, -1), (3, 2)])
    width, epsilon = field.rational("3/2"), field.rational("1/7")
    planes = reader.support_planes(
        nominal, half_width=width, diagonal_scale=field.alpha, displacement=epsilon
    )
    bounds = {(x, y): value for x, y, value in planes}
    assert bounds[1, 0] == width * (1 + field.alpha) - 2 - epsilon
    assert bounds[-1, 0] == width * (1 + field.alpha) - 3 - epsilon
    assert bounds[0, 1] == width * (1 + field.alpha) - 1 - epsilon
    assert bounds[0, -1] == width * (1 + field.alpha) - 2 - epsilon
    assert bounds[1, 1] == width * (2 + field.alpha) - 1 - 2 * epsilon
    assert bounds[-1, -1] == width * (2 + field.alpha) - 5 - 2 * epsilon
    assert bounds[1, -1] == width * (2 + field.alpha) - 3 - 2 * epsilon
    assert bounds[-1, 1] == width * (2 + field.alpha) - 2 - 2 * epsilon
    assert len(bounds) == 8


def test_support_translation_covariance() -> None:
    field = NumberField((1, 0), (-1, 1))
    nominal = points(field, [(0, 0), (1, 0), (0, 1)])
    options = {
        "half_width": field.one,
        "diagonal_scale": field.rational(2),
        "displacement": field.zero,
    }
    before = reader.support_planes(nominal, **options)
    after = reader.support_planes(tuple((x + 4, y - 3) for x, y in nominal), **options)
    assert after == tuple((x, y, value + 4 * x - 3 * y) for x, y, value in before)


def test_missing_duplicate_zero_and_foreign_normals_are_refused() -> None:
    field = NumberField((1, 0), (-1, 1))
    planes = box_planes(field)
    malformed = (
        planes[:-1],
        (*planes[:-1], planes[0]),
        (*planes[:-1], (0, 0, field.one)),
        (*planes[:-1], (2, 1, field.one)),
        (*planes[:-1], (True, 1, field.one)),
        (*planes[:-1], (1.0, 1, field.one)),
    )
    for bad in malformed:
        with pytest.raises(reader.SourceError):
            reader.intersect_halfplanes(cast(Any, bad))


def test_empty_segment_and_singleton_intersections_are_refused() -> None:
    field = NumberField((1, 0), (-1, 1))
    for case in ("empty", "segment", "point"):
        planes = []
        for x, y, original_bound in box_planes(field):
            bound = original_bound
            if x and not y:
                bound = field.rational(-1 if case == "empty" else 0)
            if y and not x and case == "point":
                bound = field.zero
            planes.append((x, y, bound))
        with pytest.raises(reader.SourceError, match="positive area"):
            reader.intersect_halfplanes(planes)


def test_mixed_fields_nonexact_and_oversized_bounds_are_refused() -> None:
    field = NumberField((1, 0, -3), (1, 2))
    foreign = NumberField((1, 0, -3), (-2, -1))
    planes = box_planes(field)
    for bound in (foreign.one, 1, 1.0, field.rational(2**129)):
        bad = (*planes[:-1], (*planes[-1][:2], bound))
        with pytest.raises(reader.SourceError):
            reader.intersect_halfplanes(cast(Any, bad))


def test_invalid_support_inputs_are_refused() -> None:
    field = NumberField((1, 0), (-1, 1))
    foreign = NumberField((1, 0), (-1, 1))
    nominal = points(field, [(0, 0), (1, 0), (0, 1)])
    options = {
        "half_width": field.one,
        "diagonal_scale": field.one,
        "displacement": field.zero,
    }
    for key, value in (
        ("half_width", field.zero),
        ("diagonal_scale", -field.one),
        ("displacement", -field.one),
        ("half_width", foreign.one),
        ("displacement", 0.0),
    ):
        with pytest.raises(reader.SourceError):
            reader.support_planes(nominal, **cast(Any, options | {key: value}))
    for cloud in ((), ((field.zero, foreign.zero),), ((0, 0),), nominal * 12):
        with pytest.raises(reader.SourceError):
            reader.support_planes(cast(Any, cloud), **options)


def toy_source() -> tuple[NumberField, list, list]:
    field = NumberField((1, 0), (-1, 1))
    rectangle = [[["-1"], ["-1"]], [["1"], ["1"]]]
    square = [[["-1"], ["-1"]], [["1"], ["-1"]], [["1"], ["1"]], [["-1"], ["1"]]]
    polygons = [{"id": identity, "vertices": deepcopy(square)} for identity in reader.BASE_IDS]
    return field, rectangle, polygons


def test_append_preserves_all_original_regions_and_full_coefficient_width() -> None:
    field = NumberField((1, 0, -3), (1, 2))
    _, _, polygons = toy_source()
    for entry in polygons:
        for vertex in entry["vertices"]:
            for coordinate in vertex:
                coordinate.append("0")
    original = deepcopy(polygons)
    collision = reader.intersect_halfplanes(box_planes(field))
    result = reader.append_collision(polygons, collision)
    assert result[:-1] == original == polygons
    assert result[-1]["id"] == "collision"
    assert result[-1]["vertices"][0] == [["-1", "0"], ["-1", "0"]]
    result[0]["vertices"][0][0][0] = "999"
    assert polygons == original


def test_append_refuses_incomplete_inventory_and_degenerate_collision() -> None:
    field, _, polygons = toy_source()
    collision = reader.intersect_halfplanes(box_planes(field))
    for bad in (polygons[:-1], list(reversed(polygons)), [*polygons, polygons[0]]):
        with pytest.raises(reader.SourceError):
            reader.append_collision(bad, collision)
    with pytest.raises(reader.SourceError, match="positive area"):
        reader.append_collision(polygons, points(field, [(0, 0), (1, 0)]))


def test_append_rejects_malformed_wire_before_unbounded_rational_parsing() -> None:
    field, _, polygons = toy_source()
    collision = reader.intersect_halfplanes(box_planes(field))
    for coefficient in ("01", "1/0", "2/2", "1e2", "9" * 81, str(2**129), 1.0):
        bad = deepcopy(polygons)
        bad[0]["vertices"][0][0] = [coefficient]
        with pytest.raises(reader.SourceError):
            reader.append_collision(bad, collision)
    bad = deepcopy(polygons)
    bad[0]["vertices"][0][0] = ["-1", "0"]
    with pytest.raises(reader.SourceError, match="degree"):
        reader.append_collision(bad, collision)


def test_append_rejects_noncanonical_old_boundaries_and_total_inventory_overflow() -> None:
    field, _, polygons = toy_source()
    collision = reader.intersect_halfplanes(box_planes(field))
    for boundary in (
        list(reversed(polygons[0]["vertices"])),
        polygons[0]["vertices"][1:] + polygons[0]["vertices"][:1],
        [*polygons[0]["vertices"], polygons[0]["vertices"][0]],
    ):
        bad = deepcopy(polygons)
        bad[0]["vertices"] = boundary
        with pytest.raises(reader.SourceError, match="strict CCW"):
            reader.append_collision(bad, collision)
    bad = deepcopy(polygons)
    bad[0]["vertices"] *= 18
    with pytest.raises(reader.SourceError, match="68-vertex"):
        reader.append_collision(bad, collision)


def test_endpoint_reader_refuses_incomplete_or_omitted_collision_binding(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    field, rectangle, old_polygons = toy_source()
    polygons = reader.append_collision(
        old_polygons, reader.intersect_halfplanes(box_planes(field))
    )
    monkeypatch.setattr(reader, "cover_source", lambda: (field, rectangle, polygons))
    raw = packet(field, rectangle, polygons)
    raw["slabs"][0]["right"] = ["0"]
    with pytest.raises(GuardError, match="omits"):
        reader.check_packet(raw)
    raw = packet(field, rectangle, polygons)
    raw["polygons"].pop()
    with pytest.raises(GuardError, match="caller-bound"):
        reader.check_packet(raw)


def packet(field: NumberField, rectangle: list, polygons: list) -> dict[str, Any]:
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
        "slabs": [{"left": ["-1"], "right": ["1"], "chain": ["collision"]}],
        "stop_reason": "complete",
    }


def test_mocked_source_binding_replays_complete_inventory_and_refuses_tampering(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    field, rectangle, old_polygons = toy_source()
    polygons = reader.append_collision(
        old_polygons, reader.intersect_halfplanes(box_planes(field))
    )
    monkeypatch.setattr(reader, "cover_source", lambda: (field, rectangle, polygons))
    raw = packet(field, rectangle, polygons)
    result = reader.check_packet(raw)
    assert result["cover_proved"] is True
    assert result["polygons_checked"] == 14
    for index in (0, 13):
        changed = deepcopy(raw)
        changed["polygons"][index]["vertices"][0][0][0] = "-2"
        with pytest.raises(GuardError, match="caller-bound"):
            reader.check_packet(changed)
    changed = deepcopy(raw)
    changed["field"]["isolating_interval"] = ["-2", "2"]
    with pytest.raises(GuardError, match="embedding"):
        reader.check_packet(changed)
    raw.update(status="unresolved", slabs=[], stop_reason="no_chain")
    assert reader.check_packet(raw)["cover_proved"] is False


def test_import_constructs_no_field_or_scientific_source(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden(*_args: Any, **_kwargs: Any) -> Any:
        raise AssertionError("import-time field construction is forbidden")

    monkeypatch.setattr(NumberField, "__init__", forbidden)
    loaded = runpy.run_path(reader.__file__)
    assert callable(loaded["cover_source"])
