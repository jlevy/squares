"""The closed-form constants of Ryu's k^{2/5} and k^{3/8} bounds on c*(k), and refusals."""

from __future__ import annotations

from dataclasses import replace

import pytest

from cases.asymptotic.ryu_upper_constants import (
    TIERS,
    check_all,
    check_theorem_11_v10,
    check_theorem_12,
    check_tiers,
    iv,
    phi_terms,
)


def _failed(checks) -> list[str]:
    return [check.name for check in checks if not check.holds]


def test_every_stated_constant_holds() -> None:
    checks = check_all(subdivisions=40)
    assert _failed(checks) == []
    assert len(checks) == 77


def test_phi_at_b_10_4_is_the_published_enclosure() -> None:
    iv.dps = 50
    phi = phi_terms(iv.mpf(10) ** (iv.mpf(-4) / 3))["Phi"]
    assert 5.0162487 < float(phi.a) <= float(phi.b) < 5.0162488


def test_a_smaller_end_constant_for_theorem_12_is_refused() -> None:
    iv.dps = 50
    assert "Phi(x0) <= C_E = 5.01" in _failed(check_theorem_12(c_e="5.01", subdivisions=4))


def test_a_larger_end_constant_breaks_the_closed_form() -> None:
    iv.dps = 50
    failed = _failed(check_theorem_11_v10(c_e="15.6"))
    assert "(32/5)(5/3)^{3/8} 15.6^{5/8} < 43.06" in failed


def test_a_covering_supremum_above_the_certified_constant_is_refused() -> None:
    iv.dps = 50
    assert any("Psi_sup" in name for name in _failed(check_theorem_11_v10(psi_sup="96.5")))


@pytest.mark.parametrize(
    ("field", "value"),
    [("c", "42.08"), ("k", "2.47e12"), ("a", "0.049"), ("better_from", "2.2e12")],
)
def test_a_tier_stated_below_its_closed_form_is_refused(field: str, value: str) -> None:
    iv.dps = 50
    c3 = next(tier for tier in TIERS if tier.name == "C3")
    assert _failed(check_tiers([replace(c3, **{field: value})]))


def test_the_twelve_tiers_and_the_crossing() -> None:
    iv.dps = 50
    checks = check_tiers()
    assert len(checks) == 12 * 4 + 1
    assert _failed(checks) == []
