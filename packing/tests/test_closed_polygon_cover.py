"""Unrelated exact polygon controls; no scientific constructor or source is loaded."""

from __future__ import annotations

from collections.abc import Sequence
from copy import deepcopy
from fractions import Fraction
from typing import Any

import pytest

from devtools import closed_polygon_cover as cover
from sqpack.field import NumberField


def scalar(value: str | int) -> list[str]:
    return [str(value)]


def point(x: str | int, y: str | int) -> list[list[str]]:
    return [scalar(x), scalar(y)]


def polygon(name: str, vertices: Sequence[tuple[str | int, str | int]]) -> dict[str, Any]:
    return {"id": name, "vertices": [point(x, y) for x, y in vertices]}


def box(name: str, left: str | int, bottom: str | int, right: str | int, top: str | int):
    return polygon(name, [(left, bottom), (right, bottom), (right, top), (left, top)])


def test_diagonal_contact_and_singleton_endpoint_sections_prove_cover() -> None:
    field = NumberField((1, 0), ("-1", "1"))
    rectangle = [point(0, 0), point(1, 1)]
    polygons = [
        polygon("lower", [(0, 0), (1, 0), (1, 1)]),
        polygon("upper", [(0, 0), (1, 1), (0, 1)]),
    ]
    result = cover.produce_cover(field, rectangle, polygons)
    assert result["status"] == "covered"
    assert result["slabs"] == [{"left": ["0"], "right": ["1"], "chain": ["lower", "upper"]}]
    assert result["rectangle"] == rectangle
    assert result["polygons"] == polygons


def test_vertical_seam_and_redundant_events_merge_identical_chains() -> None:
    field = NumberField((1, 0), ("-1", "1"))
    rectangle = [point(0, 0), point(2, 1)]
    result = cover.produce_cover(
        field, rectangle, [box("left", 0, 0, 1, 1), box("right", 1, 0, 2, 1)]
    )
    assert result["status"] == "covered"
    assert [slab["chain"] for slab in result["slabs"]] == [["left"], ["right"]]
    redundant = [box("all", 0, 0, 2, 1), box("inside", "1/3", "1/4", "5/3", "3/4")]
    merged = cover.produce_cover(field, rectangle, redundant)
    assert merged["slabs"] == [{"left": ["0"], "right": ["2"], "chain": ["all"]}]


def test_thin_gap_empty_family_and_different_endpoint_covers_are_unresolved() -> None:
    field = NumberField((1, 0), ("-1", "1"))
    rectangle = [point(0, 0), point(1, 1)]
    width = Fraction(1, 10**25)
    for polygons in (
        [],
        [box("left", 0, 0, "1/2", 1), box("right", str(Fraction(1, 2) + width), 0, 1, 1)],
        [box("left", 0, 0, "1/4", 1), box("right", "3/4", 0, 1, 1)],
    ):
        result = cover.produce_cover(field, rectangle, polygons)
        assert result["status"] == "unresolved"
        assert result["stop_reason"] != "complete"


def test_events_include_outside_y_crossings_and_group_parallel_lines() -> None:
    field = NumberField((1, 0), ("-1", "1"))
    rectangle = [point(0, 0), point(3, 3)]
    polygons = [
        box("cover", 0, 0, 3, 3),
        polygon("first", [(1, 1), ("8/5", "9/5"), ("4/5", "12/5"), ("1/5", "8/5")]),
        polygon("second", [(2, "3/2"), ("13/5", "23/10"), ("9/5", "29/10"), ("6/5", "21/10")]),
    ]
    source = cover.validate_source(field, rectangle, polygons)
    events = cover.sweep_events(source)
    assert field.rational("7/5") in events
    assert events == tuple(sorted(set(events)))
    assert cover.produce_cover(field, rectangle, polygons)["status"] == "covered"


def test_limits_and_deadline_never_publish_complete_cover(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    field = NumberField((1, 0), ("-1", "1"))
    rectangle = [point(0, 0), point(2, 1)]
    polygons = [box("left", 0, 0, 1, 1), box("right", 1, 0, 2, 1)]
    options_list: list[dict[str, Any]] = [
        {"event_limit": 2},
        {"slab_limit": 1},
        {"deadline": 0.0},
    ]
    for options in options_list:
        result = cover.produce_cover(field, rectangle, polygons, **options)
        assert result["status"] == "unresolved"
    monkeypatch.setattr(
        cover, "sweep_events", lambda *_args, **_kwargs: (field.zero, field.rational(2))
    )
    omitted = cover.produce_cover(field, rectangle, polygons)
    assert omitted["status"] == "unresolved"
    assert omitted["stop_reason"] == "no_chain"


def test_input_validation_refuses_nonconvex_degenerate_duplicate_and_noncanonical() -> None:
    field = NumberField((1, 0), ("-1", "1"))
    rectangle = [point(0, 0), point(1, 1)]
    valid = box("one", 0, 0, 1, 1)
    for polygons in (
        [polygon("bad", [(0, 0), (1, 1), (1, 0), (0, 1)])],
        [polygon("bad", [(0, 0), (1, 0), ("1/2", "1/4"), (1, 1), (0, 1)])],
        [polygon("bad", [(0, 0), (1, 0), (2, 0)])],
        [valid, valid],
        [polygon("bad", [(0, 0), (1, 0), (1, 1), (0, 0)])],
    ):
        with pytest.raises(cover.CoverError):
            cover.produce_cover(field, rectangle, polygons)
    with pytest.raises(cover.CoverError):
        cover.produce_cover(field, [point(0, 0), point(0, 1)], [valid])
    altered = deepcopy(rectangle)
    altered[0][0] = ["0/1"]
    with pytest.raises(cover.CoverError):
        cover.produce_cover(field, altered, [valid])


@pytest.mark.parametrize(
    "raw", ["1e100000000", "1_0", "1.0", "+1", "\u0661", "1/0", "9" * 1000, 0.5, True]
)
def test_bad_lexical_input_is_refused_before_fraction(
    raw: Any, monkeypatch: pytest.MonkeyPatch
) -> None:
    def forbidden(*_args: Any, **_kwargs: Any) -> Fraction:
        raise AssertionError("Fraction conversion must not run")

    monkeypatch.setattr(cover, "Fraction", forbidden)
    with pytest.raises(cover.CoverError):
        cover.parse_rational(raw)


def test_quadratic_field_uses_real_order_and_does_not_construct_fields(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    field = NumberField((1, 0, -2), ("1", "2"))

    def qpoint(x: list[str], y: list[str]) -> list[list[str]]:
        return [x, y]

    zero, one, root = ["0", "0"], ["1", "0"], ["0", "1"]
    rectangle = [qpoint(zero, zero), qpoint(root, one)]
    vertices = [qpoint(zero, zero), qpoint(root, zero), qpoint(root, one), qpoint(zero, one)]

    def forbidden(*_args: Any, **_kwargs: Any) -> None:
        raise AssertionError("producer cannot construct a NumberField")

    monkeypatch.setattr(NumberField, "__init__", forbidden)
    result = cover.produce_cover(field, rectangle, [{"id": "quadratic", "vertices": vertices}])
    assert result["status"] == "covered"
    assert result["slabs"][-1]["right"] == root


def test_cubic_and_quartic_caller_fields_and_collinear_boundary_vertices() -> None:
    for minimal in ((1, 0, 0, -2), (1, 0, 0, 0, -2)):
        field = NumberField(minimal, ("1", "2"))

        def padded(value: int, degree: int = field.degree) -> list[str]:
            return [str(value), *(["0"] * (degree - 1))]

        def vertex(x: int, y: int) -> list[list[str]]:
            return [padded(x), padded(y)]

        rectangle = [vertex(0, 0), vertex(2, 2)]
        polygons = [
            {
                "id": "boundary",
                "vertices": [
                    vertex(0, 0),
                    vertex(1, 0),
                    vertex(2, 0),
                    vertex(2, 2),
                    vertex(0, 2),
                ],
            }
        ]
        result = cover.produce_cover(field, rectangle, polygons)
        assert result["status"] == "covered"
        assert len(result["slabs"]) == 1


def test_source_and_budget_admission_is_bounded_before_geometry(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    field = NumberField((1, 0), ("-1", "1"))
    rectangle = [point(0, 0), point(1, 1)]
    valid = box("one", 0, 0, 1, 1)
    options_list: list[dict[str, Any]] = [
        {"event_limit": True},
        {"event_limit": cover.MAX_EVENTS + 1},
        {"slab_limit": 0},
        {"deadline": float("nan")},
        {"deadline": True},
    ]
    for options in options_list:
        with pytest.raises(cover.CoverError):
            cover.produce_cover(field, rectangle, [valid], **options)
    for polygons in (
        [valid] * (cover.MAX_POLYGONS + 1),
        [{"id": str(index), "vertices": valid["vertices"]} for index in range(25)],
        [{"id": "bad:id", "vertices": valid["vertices"]}],
        [{"id": "bad", "vertices": [point(0, 0)] * (cover.MAX_VERTICES + 1)}],
    ):
        with pytest.raises(cover.CoverError):
            cover.produce_cover(field, rectangle, polygons)
    with pytest.raises(cover.CoverError):
        cover.parse_rational(str(2**cover.MAX_INPUT_BITS))
    monkeypatch.setattr(field, "degree", 5)
    with pytest.raises(cover.CoverError, match="degree"):
        cover.produce_cover(field, rectangle, [valid])


def test_arithmetic_failure_drops_any_partial_slabs(monkeypatch: pytest.MonkeyPatch) -> None:
    field = NumberField((1, 0), ("-1", "1"))
    rectangle = [point(0, 0), point(2, 1)]
    polygons = [box("left", 0, 0, 1, 1), box("right", 1, 0, 2, 1)]
    count = 0

    def interrupted(_source: cover.Source, _x: Any) -> tuple[int, ...]:
        nonlocal count
        count += 1
        if count == 2:
            raise ArithmeticError("injected arithmetic failure")
        # The first slab really is covered by polygon zero; fail only after it closes.
        return (0,)

    monkeypatch.setattr(cover, "_discover_chain", interrupted)
    result = cover.produce_cover(field, rectangle, polygons)
    assert count == 2
    assert result["status"] == "unresolved"
    assert result["stop_reason"] == "arithmetic_error"
    assert result["slabs"] == []


def test_three_way_event_and_distinct_polygon_aliases_keep_full_identity() -> None:
    field = NumberField((1, 0), ("-1", "1"))
    rectangle = [point(0, 0), point(2, 2)]
    polygons = [
        box("all", 0, 0, 2, 2),
        polygon("up", [(0, 0), (2, 0), (1, 1)]),
        polygon("down", [(0, 2), (1, 1), (2, 2)]),
        box("vertical", 1, 0, 2, 2),
        box("alias", 0, 0, 2, 2),
    ]
    events = cover.sweep_events(cover.validate_source(field, rectangle, polygons))
    assert events.count(field.one) == 1
    result = cover.produce_cover(field, rectangle, polygons)
    assert result["status"] == "covered"
    assert result["polygons"] == polygons
    assert result["slabs"] == [{"left": ["0"], "right": ["2"], "chain": ["all"]}]
    polygons[0]["vertices"][0][0][0] = "99"
    assert result["polygons"][0]["vertices"][0][0][0] == "0"


def test_thirteen_polygon_unrelated_oblique_control() -> None:
    field = NumberField((1, 0), ("-1", "1"))
    rectangle = [point(-4, -4), point(4, 4)]
    polygons = [box("whole", -4, -4, 4, 4)]
    for index in range(1, 13):
        t = Fraction(index, 37)
        cosine, sine = (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)
        center_x, center_y = Fraction(index, 19), Fraction(index, 23)
        vertices = [
            (str(center_x + sx * cosine - sy * sine), str(center_y + sx * sine + sy * cosine))
            for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))
        ]
        polygons.append(polygon(f"oblique-{index}", vertices))
    result = cover.produce_cover(field, rectangle, polygons)
    assert result["status"] == "covered"
    assert result["slabs"] == [{"left": ["-4"], "right": ["4"], "chain": ["whole"]}]
