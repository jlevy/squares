"""Full angular comparison domain and adversarial error-budget controls."""

from __future__ import annotations

from typing import TypedDict

import mpmath
import pytest

from cases.asymptotic.ryu_k2_minus_c_float_gap import MAX_MULTIPLE, MAX_STEPS, check_float_gap


class Overrides(TypedDict, total=False):
    gap_floor: str
    roundoff_cap: str
    separation_deficit: str
    closing_slack: str
    separation_hex: str


def test_full_domain_and_current_binary_constants_are_certified() -> None:
    audit = check_float_gap()
    assert audit.passed
    # The published full grid, declared loop bounds and actual enumeration must agree.
    assert audit.comparisons == MAX_STEPS * (MAX_MULTIPLE + 1) == 25929
    assert audit.closest == (8, 1325)
    assert set(audit.binary_constants) == {
        "pi",
        "dphi",
        "g0_safe",
        "cell_slack",
        "closing_slack",
    }
    assert all(float.fromhex(value) > 0 for value in audit.binary_constants.values())


@pytest.mark.parametrize(
    ("overrides", "refusal"),
    [
        ({"gap_floor": "0.00005"}, "every finite angular difference exceeds gap floor"),
        (
            {"roundoff_cap": "0.0001"},
            "combined error and slacks are below every comparison gap",
        ),
        ({"roundoff_cap": "1e-20"}, "all endpoint and basic-operation errors fit roundoff cap"),
        (
            {"separation_deficit": "0.00001"},
            "combined error and slacks are below every comparison gap",
        ),
        (
            {"closing_slack": "0.0001"},
            "combined error and slacks are below every comparison gap",
        ),
        (
            {"separation_hex": "0x1p+0"},
            "binary separation is conservative and within 1e-15 of gamma minus deficit",
        ),
    ],
)
def test_unjustified_gap_or_error_assumptions_are_refused(
    overrides: Overrides, refusal: str
) -> None:
    audit = check_float_gap(**overrides)
    assert not audit.passed
    assert refusal in {check.name for check in audit.checks if not check.holds}


@pytest.mark.parametrize(
    "overrides",
    [
        {"gap_floor": "0"},
        {"roundoff_cap": "-1"},
        {"separation_deficit": "0"},
        {"closing_slack": "-1"},
        {"separation_hex": "nan"},
    ],
)
def test_invalid_arithmetic_domains_are_refused(overrides: Overrides) -> None:
    with pytest.raises(ValueError, match="positive"):
        check_float_gap(**overrides)


def test_ambient_precision_does_not_change_the_decision_or_leak() -> None:
    original_mp, original_iv = mpmath.mp.dps, mpmath.iv.dps
    expected = check_float_gap()
    try:
        mpmath.mp.dps, mpmath.iv.dps = 5, 6
        assert check_float_gap() == expected
        assert (mpmath.mp.dps, mpmath.iv.dps) == (5, 6)
    finally:
        mpmath.mp.dps, mpmath.iv.dps = original_mp, original_iv
