"""Version 1.2 numerical consequences and falsifiable source-threshold controls."""

from fractions import Fraction
from typing import TypedDict

import pytest

from cases.asymptotic.ryu_k2_minus_c_constants import Check, check_constants_v12


class Overrides(TypedDict, total=False):
    q_star: str
    cutoff: str
    gamma_bound: str
    bracket_bound: str
    lead_bound: str
    shift_bound: str
    room_bound: str
    kappa: str
    conditional_kappa: str


def failed(checks: tuple[Check, ...]) -> set[str]:
    return {check.name for check in checks if not check.holds}


@pytest.mark.parametrize("overlap", [9, 13])
def test_primary_arithmetic_holds_separately_for_both_overlap_routes(overlap: int) -> None:
    checks = check_constants_v12(overlap)
    assert not failed(checks)
    conditional = [check for check in checks if "conditional" in check.name]
    assert bool(conditional) == (overlap == 9)


@pytest.mark.parametrize(
    ("overrides", "refusal"),
    [
        ({"q_star": "0.31"}, "overlap-derived A < stated A"),
        ({"cutoff": "235000"}, "column inclination <= 2.119e-6"),
        ({"gamma_bound": "1.60e-5"}, "integrated excess Gamma < stated cap"),
        ({"bracket_bound": "30.4179"}, "full bracket < stated bracket"),
        ({"lead_bound": "1.99955"}, "twice (1 - omega0) h0 >= stated lead"),
        ({"shift_bound": "13.0667"}, "full height shift < stated shift"),
        ({"room_bound": "0.49998"}, "remaining room > g0"),
        ({"kappa": "0.0354"}, "max(1,F)/log k supports all-k coefficient"),
        ({"conditional_kappa": "0.0542"}, "conditional max(4,F)/log k supports 0.0541"),
    ],
)
def test_a_stricter_new_source_bound_is_refused(overrides: Overrides, refusal: str) -> None:
    assert refusal in failed(check_constants_v12(**overrides))


def test_analytic_all_k_coefficient_does_not_inherit_computer_assisted_value() -> None:
    assert "max(1,F)/log k supports all-k coefficient" in failed(
        check_constants_v12(13, kappa="0.0353")
    )


def test_a_tenth_rectangle_refuses_the_nine_rectangle_derived_constant() -> None:
    assert "overlap-derived A < stated A" in failed(check_constants_v12(10))


def test_source_transition_and_exact_all_k_lower_envelopes() -> None:
    lead, bracket, shift = map(Fraction, ("1.99954", "30.418", "13.06675"))
    transition = shift + 4 * bracket / lead
    assert Fraction("73.91674") < transition < Fraction("73.91675")
    all_k = lead / (bracket + lead * shift)
    conditional = 4 / transition
    assert Fraction("0.0353") < all_k < Fraction("0.0354")
    assert Fraction("0.0541") < conditional < Fraction("0.0542")


@pytest.mark.parametrize(
    "overrides",
    [
        {"room_bound": "-1"},
        {"room_bound": "0"},
        {"bracket_bound": "-1"},
        {"lead_bound": "0"},
        {"shift_bound": "-1"},
        {"cutoff": "235999.5"},
    ],
)
def test_invalid_arithmetic_domains_are_refused(overrides: Overrides) -> None:
    with pytest.raises(ValueError, match=r"positive|integer"):
        check_constants_v12(**overrides)
