"""Exact controls for the robust outer-corner arithmetic replay."""

from fractions import Fraction

from devtools.check_robust_outer_corner_incompatibility import (
    algebra_checks,
    arithmetic_checks,
)


def test_fixed_draft_arithmetic_and_algebra_are_exact() -> None:
    assert all(arithmetic_checks().values())
    assert all(algebra_checks().values())


def test_perturbation_guard_rejects_an_out_of_scope_epsilon() -> None:
    checks = arithmetic_checks(Fraction(1, 10))
    assert not checks["left_case_H"]
    assert not checks["r_lower_equivalent"]
    assert not checks["beta_upper"]
