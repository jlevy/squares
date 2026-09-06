"""Independent adversarial controls for the exact-angle BC-255 source replay."""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from typing import cast

import pytest

from cases.stromquist import restricted_orientation as source
from sqpack.field import FieldElement, NumberField


def _quadratic_sign(a: Fraction, b: Fraction) -> int:
    """Sign of a + b sqrt(2), using rational squared comparisons, not isolation."""
    if a == 0:
        return (b > 0) - (b < 0)
    if b == 0 or (a > 0) == (b > 0):
        return (a > 0) - (a < 0)
    difference = a * a - 2 * b * b
    sign = (difference > 0) - (difference < 0)
    return sign if a > 0 else -sign


def test_source_field_signs_match_rational_oracle_including_near_cancellation() -> None:
    field = source.source_field()
    for a, b in product((Fraction(-7, 5), Fraction(-1), Fraction(0), Fraction(2, 3)), repeat=2):
        assert field.element((a, b)).sign() == _quadratic_sign(a, b)
    p, q = 1, 0
    for _ in range(25):
        p, q = 3 * p + 4 * q, 2 * p + 3 * q
    assert p * p - 2 * q * q == 1
    small = p - q * field.alpha
    assert small.sign() == 1
    assert (small - Fraction(1, p)).sign() == -1
    assert (field.alpha * field.alpha - 2).sign() == 0


def test_original_coordinates_and_k4_are_not_a_d4_substitution() -> None:
    field = source.source_field()
    side, ten, twelve = source.source_points(field)
    assert side == 2 + Fraction(4, 3) * field.alpha
    assert len(ten) == 10
    assert len(twelve) == 12
    assert twelve[:3] == (
        (field.one, side - 3),
        (side / 2, side - 3),
        (field.rational("3/2"), field.rational("13/10")),
    )
    assert twelve[3:] == tuple(
        (field.element(x), field.element(y))
        for x, y in (
            ((1, Fraction(4, 3)), (1,)),
            ((Fraction(6, 5), Fraction(4, 3)), (1, Fraction(2, 3))),
            ((1, Fraction(4, 3)), (1, Fraction(4, 3))),
            ((1, Fraction(2, 3)), (Fraction(6, 5), Fraction(4, 3))),
            ((1,), (1, Fraction(4, 3))),
            ((Fraction(4, 5),), (0, Fraction(4, 3))),
            ((Fraction(17, 10),), (Fraction(11, 5),)),
            ((Fraction(11, 5),), (Fraction(11, 5),)),
            ((Fraction(11, 5),), (Fraction(17, 10),)),
        )
    )
    assert (side / 2, field.one) in ten
    assert (side - 1, side / 2) not in ten
    for flip_x, flip_y in product((False, True), repeat=2):
        reflected = {(side - x if flip_x else x, side - y if flip_y else y) for x, y in ten}
        assert reflected == set(ten)


def test_domain_vertices_inside_open_event_segments_are_not_dropped() -> None:
    field = source.source_field()
    cells = tuple(source.event_cells(field.rational(2), 45, ()))
    assert len(cells) == 5
    assert sum(cell.dimension == 1 for cell in cells) == 4
    assert sum(cell.dimension == 2 for cell in cells) == 1
    # Each extreme domain point lies inside an event segment, not at an event vertex.
    for cell in cells:
        if cell.dimension == 1:
            assert len(cell.polygon) == 1
            assert cell.witness == cell.polygon[0]
    singleton = tuple(source.event_cells(field.alpha, 45, ()))
    assert len(singleton) == 1
    assert singleton[0].dimension == 0
    assert len(singleton[0].polygon) == 1


def test_strict_region_feasibility_uses_the_whole_clipped_polygon() -> None:
    field = source.source_field()
    zero, one = field.zero, field.one
    square = ((zero, zero), (one, zero), (one, one), (zero, one))
    interval = source.Stratum(zero, one)
    cell = source.Cell(interval, interval, square, (one / 2, one / 2), 0)
    constraints = (
        ((-one, zero, -Fraction(3, 4) * one), True),
        ((zero, -one, -Fraction(3, 4) * one), True),
    )
    witness = source.region_witness(cell, constraints)
    assert witness is not None
    assert Fraction(3, 4) < witness[0] < 1
    assert Fraction(3, 4) < witness[1] < 1
    # Closure touches x=1, but neither the open event cell nor x>1 is reached.
    assert source.region_witness(cell, (((-one, zero, -one), True),)) is None
    edge = source.Cell(
        source.Stratum(one, one), interval, ((one, zero), (one, one)), (one, one / 2), 0
    )
    assert source.region_witness(edge, (((-one, zero, -one), False),)) == (one, one / 2)
    assert source.region_witness(edge, (((-one, zero, -one), True),)) is None


def test_forced_triple_has_an_explicit_nonvacuous_strict_source_box() -> None:
    field = source.source_field()
    side, ten, twelve = source.source_points(field)
    center = (1 + field.alpha / 3, field.rational("3/4"))
    assert 1 < center[0] < side / 2
    assert 0 < center[1] < 1
    assert source.direct_membership(side, 45, center, ten) == 0
    assert source.direct_membership(side, 45, center, twelve) & 7 == 7
    # This is also a source box: open, side > 1, contained, and still P10-avoiding.
    assert (
        source.direct_membership(
            side, 45, center, ten, square_side=Fraction(101, 100), closed=False
        )
        == 0
    )
    assert (
        source.direct_membership(
            side, 45, center, twelve, square_side=Fraction(101, 100), closed=False
        )
        & 7
        == 7
    )


def test_all_seven_source_conclusions_and_nonvacuous_counts_are_reported() -> None:
    result = source.source_replay()
    assert result["obligations"] == {
        "axis_ten_cover": True,
        "localization": True,
        "forced_A1": True,
        "forced_A2": True,
        "forced_A3": True,
        "twelve_cover_0": True,
        "twelve_cover_45": True,
    }
    assert result["complete"] is True
    assert result["theorem_acceptance"] is False
    assert result["obstructions"] == []
    cases = cast(list[dict[str, object]], result["cases"])
    assert cases[0]["reachable_event_strata_by_dimension"] == [280, 526, 247]
    assert cases[1]["reachable_event_strata_by_dimension"] == [406, 841, 444]
    assert cases[1]["ten_avoiding_strata"] == 6
    assert cases[1]["canonical_ten_avoiding_strata"] == 1


@pytest.mark.parametrize("index", [0, 1, 2])
def test_each_individual_failed_a_point_is_a_checked_obstruction(
    index: int, monkeypatch: pytest.MonkeyPatch
) -> None:
    original = source.source_points

    def changed_points(
        field: NumberField,
    ) -> tuple[FieldElement, tuple[source.Point, ...], tuple[source.Point, ...]]:
        side, ten, twelve = original(field)
        changed = list(twelve)
        changed[index] = (side - Fraction(1, 2), side - Fraction(1, 2))
        return side, ten, tuple(changed)

    monkeypatch.setattr(source, "source_points", changed_points)
    result = source.source_replay()
    obligations = cast(dict[str, bool], result["obligations"])
    assert not obligations[f"forced_A{index + 1}"]
    for other in range(3):
        if other != index:
            assert obligations[f"forced_A{other + 1}"]
    obstructions = cast(list[dict[str, object]], result["obstructions"])
    matched = [row for row in obstructions if row["obligation"] == f"forced_A{index + 1}"]
    assert len(matched) == 1
    assert matched[0]["direct_corner_and_determinant_check"] is True
    assert matched[0]["strict_box_counterexample_established"] is False
    assert result["status"] == "obstruction_retained"
    assert result["complete"] is True
    assert result["theorem_acceptance"] is False
