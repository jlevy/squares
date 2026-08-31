"""The falsifier's known-answer triple (think-yrvm, BC-094).

Three calibrations, none negotiable: the search MUST find the Figure 13 escape at
s = 2 + 4/sqrt(5); it MUST saturate on the repaired twelve-point Figure 14 set; and
every refusal MUST name what defeated the candidate. The exact bridge is calibrated
by replaying the retained Figure 13 escape pose through it over Q(sqrt2 + sqrt5).
"""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Any

import pytest

from sqpack.cover import checked_number_field
from sqpack.falsify import (
    SATURATION_CAVEAT,
    CertificationRefusedError,
    EscapeCandidate,
    SaturationReport,
    certify_escape,
    float_margin,
    search_escape,
)

SQRT5 = math.sqrt(5)
SIDE = 2 + 4 / SQRT5
A = 2 / SQRT5
LENGTH = 1.01

FIGURE13 = [
    ("bottom_left", 1.0, 1.0),
    ("bottom_center", 1 + A, 1.0),
    ("bottom_right", 1 + 2 * A, 1.0),
    ("middle_0", 1 - A / 2, SIDE / 2),
    ("middle_1", 1 + A / 2, SIDE / 2),
    ("middle_2", 1 + 1.5 * A, SIDE / 2),
    ("middle_3", 1 + 2.5 * A, SIDE / 2),
    ("top_left", 1.0, SIDE - 1),
    ("top_center", 1 + A, SIDE - 1),
    ("top_right", 1 + 2 * A, SIDE - 1),
]

# The repaired Figure 14 set with G' = (79/100, 37/20), to float precision; the exact
# set lives in cases.stromquist.repaired_cover and is certified unavoidable by exp-017.
FIGURE14_REPAIRED = [
    ("A1", 1.0, 0.9),
    ("A2", 1 + A, 0.9),
    ("A3", 1 + A / 2, 1.12),
    ("B", SIDE - 1, 1.0),
    ("C", SIDE - 0.9, 1 + A),
    ("D", SIDE - 1, SIDE - 1),
    ("E", 1 + A, SIDE - 0.9),
    ("F", 1.0, SIDE - 1),
    ("G", 0.79, 1.85),
    ("H", 1.5, 2.1),
    ("I", 2.1, 2.1),
    ("J", 2.1, 1.5),
]


def test_search_finds_the_figure13_escape() -> None:
    result = search_escape(FIGURE13, SIDE, LENGTH)
    assert isinstance(result, EscapeCandidate)
    assert result.margin > 5e-3
    # The escape family is the 45-degree one T-4 retained; the search lands in it.
    assert abs(result.theta - math.pi / 4) < 1e-3
    margin, _ = float_margin(result.x, result.y, result.theta, LENGTH / 2, FIGURE13)
    assert margin == pytest.approx(result.margin)


def test_retained_escape_pose_has_positive_float_margin() -> None:
    margin, closest = float_margin(1 + 1 / SQRT5, 18 / 25, math.pi / 4, LENGTH / 2, FIGURE13)
    assert margin > 9e-3
    assert closest == "bottom_left"


def test_search_saturates_on_the_repaired_figure14_set() -> None:
    result = search_escape(FIGURE14_REPAIRED, SIDE, LENGTH)
    assert isinstance(result, SaturationReport)
    assert result.best_margin < 0
    assert result.caveat == SATURATION_CAVEAT
    assert result.defeating_point in {label for label, _, _ in FIGURE14_REPAIRED}
    assert result.candidates_tested > 10_000


def _figure13_exact_context() -> tuple[Any, Any, Any, Any, list[tuple[str, Any]]]:
    field, _ = checked_number_field((1, 0, -14, 0, 9), (Fraction(365, 100), Fraction(366, 100)))
    rational = field.rational
    alpha = field.alpha
    sqrt2 = (alpha - rational(3) / alpha) / 2
    sqrt5 = (alpha + rational(3) / alpha) / 2
    assert (sqrt2 * sqrt2 - rational(2)).is_zero()
    assert (sqrt5 * sqrt5 - rational(5)).is_zero()
    a = rational(2) / sqrt5
    side = rational(2) + rational(4) / sqrt5
    points = [
        ("bottom_left", (rational(1), rational(1))),
        ("bottom_center", (rational(1) + a, rational(1))),
        ("bottom_right", (rational(1) + rational(2) * a, rational(1))),
        ("middle_0", (rational(1) - a / 2, side / 2)),
        ("middle_1", (rational(1) + a / 2, side / 2)),
        ("middle_2", (rational(1) + rational(Fraction(3, 2)) * a, side / 2)),
        ("middle_3", (rational(1) + rational(Fraction(5, 2)) * a, side / 2)),
        ("top_left", (rational(1), side - rational(1))),
        ("top_center", (rational(1) + a, side - rational(1))),
        ("top_right", (rational(1) + rational(2) * a, side - rational(1))),
    ]
    cosine = rational(1) / sqrt2
    return rational, side, sqrt5, cosine, points


def test_exact_bridge_certifies_the_retained_figure13_escape() -> None:
    rational, side, sqrt5, cosine, points = _figure13_exact_context()
    certificate = certify_escape(
        side=side,
        length=rational(Fraction(101, 100)),
        center=(rational(1) + rational(1) / sqrt5, rational(Fraction(18, 25))),
        cosine=cosine,
        sine=cosine,
        points=points,
    )
    assert certificate["all_points_strictly_avoided"] is True
    assert certificate["point_count"] == 10
    assert certificate["minimum_avoidance_margin_sign"] == 1


def test_exact_bridge_refuses_a_pose_on_a_point() -> None:
    rational, side, _sqrt5, cosine, points = _figure13_exact_context()
    with pytest.raises(CertificationRefusedError) as caught:
        certify_escape(
            side=side,
            length=rational(Fraction(101, 100)),
            center=(rational(1), rational(1)),
            cosine=cosine,
            sine=cosine,
            points=points,
        )
    assert caught.value.defeated_by == "bottom_left"


def test_exact_bridge_refuses_a_unit_side_by_type() -> None:
    rational, side, _sqrt5, cosine, points = _figure13_exact_context()
    with pytest.raises(CertificationRefusedError) as caught:
        certify_escape(
            side=side,
            length=rational(1),
            center=(rational(2), rational(2)),
            cosine=cosine,
            sine=cosine,
            points=points,
        )
    assert caught.value.defeated_by == "length"
