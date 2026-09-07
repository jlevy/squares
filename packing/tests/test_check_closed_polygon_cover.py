"""Synthetic closed-cover controls, independent of producer and scientific inputs."""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
from typing import Any

import pytest

from devtools import check_closed_polygon_cover as reader
from devtools.check_closed_polygon_cover import GuardError, check_packet
from sqpack.field import NumberField


def scalar(value: int | Fraction) -> list[str]:
    return [str(Fraction(value))]


def point(x: int | Fraction, y: int | Fraction) -> list[list[str]]:
    return [scalar(x), scalar(y)]


def polygon(identity: str, vertices: list[tuple]) -> dict[str, Any]:
    return {"id": identity, "vertices": [point(x, y) for x, y in vertices]}


def packet(rectangle: list, polygons: list, slabs: list) -> dict[str, Any]:
    return {
        "kind": "closed-convex-polygon-cover/v1",
        "status": "covered",
        "field": {"minimal_polynomial": ["1", "0"], "isolating_interval": ["-1", "1"]},
        "rectangle": deepcopy(rectangle),
        "polygons": deepcopy(polygons),
        "slabs": deepcopy(slabs),
        "stop_reason": "complete",
    }


def slab(left: int | Fraction, right: int | Fraction, *chain: str) -> dict[str, Any]:
    return {"left": scalar(left), "right": scalar(right), "chain": list(chain)}


def test_diagonal_closed_seam_and_singleton_endpoint_contact() -> None:
    field = NumberField((1, 0), (-1, 1))
    rectangle = [point(0, 0), point(1, 1)]
    polygons = [
        polygon("lower", [(0, 0), (1, 0), (1, 1)]),
        polygon("upper", [(0, 0), (1, 1), (0, 1)]),
    ]
    result = check_packet(
        packet(rectangle, polygons, [slab(0, 1, "lower", "upper")]),
        field=field,
        rectangle=rectangle,
        polygons=polygons,
    )
    assert result["status"] == "verified_cover"
    assert result["cover_proved"] is True
    assert result["endpoint_pair_checks"] == 2


def simple_fixture() -> tuple[NumberField, list, list, dict[str, Any]]:
    field = NumberField((1, 0), (-1, 1))
    rectangle = [point(0, 0), point(1, 1)]
    polygons = [polygon("box", [(0, 0), (1, 0), (1, 1), (0, 1)])]
    return field, rectangle, polygons, packet(rectangle, polygons, [slab(0, 1, "box")])


def test_vertical_closed_partition_seam() -> None:
    field = NumberField((1, 0), (-1, 1))
    rectangle = [point(0, 0), point(2, 1)]
    polygons = [
        polygon("left", [(0, 0), (1, 0), (1, 1), (0, 1)]),
        polygon("right", [(1, 0), (2, 0), (2, 1), (1, 1)]),
    ]
    result = check_packet(
        packet(rectangle, polygons, [slab(0, 1, "left"), slab(1, 2, "right")]),
        field=field,
        rectangle=rectangle,
        polygons=polygons,
    )
    assert result["cover_proved"] is True
    assert result["slabs_checked"] == 2


def test_exact_thin_gap_is_not_contact() -> None:
    field = NumberField((1, 0), (-1, 1))
    rectangle = [point(0, 0), point(1, 1)]
    half = Fraction(1, 2)
    below = half - Fraction(1, 2**80)
    polygons = [
        polygon("lower", [(0, 0), (1, 0), (1, below), (0, below)]),
        polygon("upper", [(0, half), (1, half), (1, 1), (0, 1)]),
    ]
    with pytest.raises(GuardError, match="gap"):
        check_packet(
            packet(rectangle, polygons, [slab(0, 1, "lower", "upper")]),
            field=field,
            rectangle=rectangle,
            polygons=polygons,
        )


def test_different_endpoint_chains_cannot_hide_a_middle_gap() -> None:
    field = NumberField((1, 0), (-1, 1))
    rectangle = [point(0, 0), point(2, 1)]
    low, high = Fraction(2, 5), Fraction(3, 5)
    polygons = [
        polygon("bottom", [(0, 0), (2, 0), (2, low), (0, low)]),
        polygon("top", [(0, high), (2, high), (2, 1), (0, 1)]),
        polygon("left", [(0, low), (Fraction(1, 2), low), (Fraction(1, 2), high), (0, high)]),
        polygon("right", [(Fraction(3, 2), low), (2, low), (2, high), (Fraction(3, 2), high)]),
    ]
    for connector in ("left", "right"):
        with pytest.raises(GuardError, match="gap"):
            check_packet(
                packet(rectangle, polygons, [slab(0, 2, "bottom", connector, "top")]),
                field=field,
                rectangle=rectangle,
                polygons=polygons,
            )
    raw = packet(rectangle, polygons, [slab(0, 2, "bottom", "left", "top")])
    raw["slabs"][0]["right_chain"] = ["bottom", "right", "top"]
    with pytest.raises(GuardError, match="declared keys"):
        check_packet(raw, field=field, rectangle=rectangle, polygons=polygons)


@pytest.mark.parametrize(
    "vertices",
    [
        [(0, 0), (1, 0), (Fraction(1, 2), Fraction(1, 2)), (1, 1), (0, 1)],
        [(0, 0), (0, 1), (1, 1), (1, 0)],
        [(0, 0), (1, 1), (0, 1), (1, 0)],
        [(0, 0), (1, 0), (2, 0)],
        [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)],
    ],
)
def test_invalid_polygon_boundaries_refused(vertices: list[tuple]) -> None:
    field, rectangle, _, _ = simple_fixture()
    polygons = [polygon("bad", vertices)]
    with pytest.raises(GuardError):
        check_packet(
            packet(rectangle, polygons, [slab(0, 1, "bad")]),
            field=field,
            rectangle=rectangle,
            polygons=polygons,
        )


def test_redundant_collinear_boundary_vertex_is_valid() -> None:
    field, rectangle, _, _ = simple_fixture()
    polygons = [polygon("box", [(0, 0), (Fraction(1, 2), 0), (1, 0), (1, 1), (0, 1)])]
    result = check_packet(
        packet(rectangle, polygons, [slab(0, 1, "box")]),
        field=field,
        rectangle=rectangle,
        polygons=polygons,
    )
    assert result["cover_proved"] is True


@pytest.mark.parametrize(
    "slabs",
    [
        [],
        [slab(Fraction(1, 2), 1, "box")],
        [slab(0, Fraction(1, 2), "box")],
        [slab(0, Fraction(1, 3), "box"), slab(Fraction(2, 3), 1, "box")],
        [slab(0, Fraction(2, 3), "box"), slab(Fraction(1, 3), 1, "box")],
        [slab(0, 0, "box"), slab(0, 1, "box")],
        [slab(0, 1, "box"), slab(0, 1, "box")],
        [slab(0, 2, "box")],
        [slab(0, 1)],
        [slab(0, 1, "missing")],
        [slab(0, 1, "box", "box")],
    ],
)
def test_incomplete_or_invalid_partitions_refused(slabs: list) -> None:
    field, rectangle, polygons, raw = simple_fixture()
    raw["slabs"] = slabs
    with pytest.raises(GuardError):
        check_packet(raw, field=field, rectangle=rectangle, polygons=polygons)


@pytest.mark.parametrize(
    "reason", ["event_limit", "slab_limit", "no_chain", "deadline", "arithmetic_error"]
)
def test_unresolved_never_proves_cover(reason: str) -> None:
    field, rectangle, polygons, raw = simple_fixture()
    raw.update(status="unresolved", stop_reason=reason, slabs=[])
    result = check_packet(raw, field=field, rectangle=rectangle, polygons=polygons)
    assert result["status"] == "unresolved"
    assert result["cover_proved"] is False
    assert result["slabs_checked"] == 0


@pytest.mark.parametrize(
    "changes",
    [
        {"status": "unresolved", "stop_reason": "deadline"},
        {"status": "unresolved", "stop_reason": "unknown", "slabs": []},
        {"status": "covered", "stop_reason": "deadline"},
        {"status": "proved"},
        {"kind": "foreign"},
        {"extra": 1},
    ],
)
def test_false_status_and_foreign_packets_refused(changes: dict) -> None:
    field, rectangle, polygons, raw = simple_fixture()
    raw.update(changes)
    with pytest.raises(GuardError):
        check_packet(raw, field=field, rectangle=rectangle, polygons=polygons)


@pytest.mark.parametrize(
    "bad", ["2/4", "-0", "01", "1/0", "1e999999999", "\u0661", "9" * 81, str(2**128), 0.0, True]
)
def test_source_rational_guards(bad: Any) -> None:
    field, rectangle, polygons, _ = simple_fixture()
    polygons[0]["vertices"][0][0] = [bad]
    raw = packet(rectangle, polygons, [slab(0, 1, "box")])
    with pytest.raises(GuardError):
        check_packet(raw, field=field, rectangle=rectangle, polygons=polygons)


@pytest.mark.parametrize("bad", ["9" * 2601, str(2**4096), "2/4"])
def test_derived_rational_guards(bad: str) -> None:
    field, rectangle, polygons, raw = simple_fixture()
    raw["slabs"][0]["right"] = [bad]
    with pytest.raises(GuardError):
        check_packet(raw, field=field, rectangle=rectangle, polygons=polygons)


@pytest.mark.parametrize("part", ["rectangle", "polygons", "field"])
def test_complete_source_and_embedding_binding(part: str) -> None:
    field, rectangle, polygons, raw = simple_fixture()
    if part == "rectangle":
        raw[part][1] = point(2, 1)
    elif part == "polygons":
        raw[part][0]["id"] = "renamed"
    else:
        raw[part]["isolating_interval"] = ["-2", "2"]
    with pytest.raises(GuardError):
        check_packet(raw, field=field, rectangle=rectangle, polygons=polygons)


def test_inventory_caps_and_duplicate_ids() -> None:
    field, rectangle, polygons, raw = simple_fixture()
    raw["slabs"] *= 5001
    with pytest.raises(GuardError, match="cap"):
        check_packet(raw, field=field, rectangle=rectangle, polygons=polygons)
    for inventory in (polygons * 33, polygons * 2):
        raw = packet(rectangle, inventory, [slab(0, 1, "box")])
        with pytest.raises(GuardError):
            check_packet(raw, field=field, rectangle=rectangle, polygons=inventory)
    polygons[0]["vertices"] *= 25
    raw = packet(rectangle, polygons, [slab(0, 1, "box")])
    with pytest.raises(GuardError, match="cap"):
        check_packet(raw, field=field, rectangle=rectangle, polygons=polygons)


@pytest.mark.parametrize("minimal_polynomial", [(1, 0, -2), (1, 0, 0, 0, -2)])
def test_positive_algebraic_embedding(minimal_polynomial: tuple[int, ...]) -> None:
    field = NumberField(minimal_polynomial, (1, 2))
    zero = ["0"] * field.degree
    one = ["1", *(["0"] * (field.degree - 1))]
    alpha = ["0", "1", *(["0"] * (field.degree - 2))]
    rectangle = [[zero, zero], [alpha, one]]
    polygons = [
        {"id": "rootbox", "vertices": [[zero, zero], [alpha, zero], [alpha, one], [zero, one]]}
    ]
    raw = packet(rectangle, polygons, [])
    raw["field"] = {
        "minimal_polynomial": [str(coefficient) for coefficient in minimal_polynomial],
        "isolating_interval": ["1", "2"],
    }
    raw["slabs"] = [{"left": zero, "right": alpha, "chain": ["rootbox"]}]
    assert (
        check_packet(raw, field=field, rectangle=rectangle, polygons=polygons)["cover_proved"]
        is True
    )
    foreign = NumberField(minimal_polynomial, (-2, -1))
    with pytest.raises(GuardError, match="embedding"):
        check_packet(raw, field=foreign, rectangle=rectangle, polygons=polygons)


def test_no_input_access_or_field_construction(monkeypatch: pytest.MonkeyPatch) -> None:
    field, rectangle, polygons, raw = simple_fixture()

    def forbidden(*_args: Any, **_kwargs: Any) -> Any:
        raise AssertionError("reader accessed external input or constructed a field")

    monkeypatch.setattr("builtins.open", forbidden)
    monkeypatch.setattr("io.open", forbidden)
    monkeypatch.setattr(NumberField, "__init__", forbidden)
    assert (
        check_packet(raw, field=field, rectangle=rectangle, polygons=polygons)["cover_proved"]
        is True
    )


def test_interrupted_exact_arithmetic_cannot_accept(monkeypatch: pytest.MonkeyPatch) -> None:
    field, rectangle, polygons, raw = simple_fixture()

    def interrupted(*_args: Any, **_kwargs: Any) -> Any:
        raise TimeoutError("external cap")

    monkeypatch.setattr(NumberField, "sign", interrupted)
    with pytest.raises(TimeoutError):
        check_packet(raw, field=field, rectangle=rectangle, polygons=polygons)


@pytest.mark.parametrize("upper", [(0, 1), (1, 0), (-1, 1), (1, -1)])
def test_nondegenerate_rectangle_required(upper: tuple[int, int]) -> None:
    field, _, polygons, _ = simple_fixture()
    rectangle = [point(0, 0), point(*upper)]
    with pytest.raises(GuardError, match="positive width and height"):
        check_packet(
            packet(rectangle, polygons, [slab(0, 1, "box")]),
            field=field,
            rectangle=rectangle,
            polygons=polygons,
        )


def test_unused_polygon_still_validated_and_bound() -> None:
    field, rectangle, polygons, _ = simple_fixture()
    polygons.append(polygon("unused", [(0, 0), (0, 1), (1, 1), (1, 0)]))
    raw = packet(rectangle, polygons, [slab(0, 1, "box")])
    with pytest.raises(GuardError, match="counterclockwise"):
        check_packet(raw, field=field, rectangle=rectangle, polygons=polygons)
    raw["polygons"].pop()
    with pytest.raises(GuardError, match="caller-bound"):
        check_packet(raw, field=field, rectangle=rectangle, polygons=polygons)


@pytest.mark.parametrize("identity", ["", "a" * 65, "a b", "\u0661", True])
def test_id_lexical_guards(identity: Any) -> None:
    field, rectangle, polygons, _ = simple_fixture()
    polygons[0]["id"] = identity
    raw = packet(rectangle, polygons, [slab(0, 1, "box")])
    with pytest.raises(GuardError, match="ASCII names"):
        check_packet(raw, field=field, rectangle=rectangle, polygons=polygons)


@pytest.mark.parametrize("bad", ["1e999999999", "\u0661", "9" * 81, "1/0", True])
def test_lexical_refusal_precedes_fraction_construction(
    bad: Any, monkeypatch: pytest.MonkeyPatch
) -> None:
    field, rectangle, polygons, raw = simple_fixture()
    raw["field"]["minimal_polynomial"][0] = bad

    def forbidden(*_args: Any, **_kwargs: Any) -> Any:
        raise AssertionError("malformed input reached Fraction")

    monkeypatch.setattr(reader, "Fraction", forbidden)
    with pytest.raises(GuardError):
        check_packet(raw, field=field, rectangle=rectangle, polygons=polygons)


def test_chain_requires_bottom_and_top_corners() -> None:
    field = NumberField((1, 0), (-1, 1))
    rectangle = [point(0, 0), point(1, 1)]
    half = Fraction(1, 2)
    polygons = [
        polygon("lower", [(0, 0), (1, 0), (1, half), (0, half)]),
        polygon("upper", [(0, half), (1, half), (1, 1), (0, 1)]),
    ]
    for chain in (("upper", "lower"), ("lower",), ("upper",)):
        with pytest.raises(GuardError, match="corners"):
            check_packet(
                packet(rectangle, polygons, [slab(0, 1, *chain)]),
                field=field,
                rectangle=rectangle,
                polygons=polygons,
            )
