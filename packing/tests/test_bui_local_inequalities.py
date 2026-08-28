"""Exact controls for Bui Section 4.2 Lemmas 3-5."""

from __future__ import annotations

from fractions import Fraction
from typing import cast

import pytest

from cases.asymptotic.bui_local_inequalities import (
    InequalityControlError,
    prove_local_inequalities,
)


def test_source_packet_has_exact_positive_margins() -> None:
    certificate = prove_local_inequalities()

    assert certificate.angle_upper == Fraction(1, 8)
    assert certificate.lower_endpoint_open is True
    assert certificate.cosine_lower == Fraction(127, 128)
    assert certificate.lemma3_margin == Fraction(27, 12928)
    assert certificate.lemma4_difference_coefficients == (
        Fraction(1),
        Fraction(2),
        Fraction(1),
        Fraction(-4),
    )
    assert certificate.lemma4_factor_coefficients == (
        Fraction(1),
        Fraction(2),
        Fraction(1),
        Fraction(-4),
    )
    assert certificate.lemma4_cleared_coefficients == (
        Fraction(1),
        Fraction(0),
        Fraction(-2),
        Fraction(-4),
        Fraction(9),
        Fraction(-4),
    )
    assert (
        certificate.lemma4_cleared_factor_coefficients
        == certificate.lemma4_cleared_coefficients
    )
    assert certificate.lemma5_cleared_coefficients == (
        Fraction(-49, 100),
        Fraction(0),
        Fraction(149, 100),
        Fraction(-1),
    )
    assert (
        certificate.lemma5_cleared_factor_coefficients
        == certificate.lemma5_cleared_coefficients
    )
    assert certificate.lemma5_derivative_lower > 0
    assert certificate.lemma5_margin == Fraction(677, 81920)


def test_weaker_angle_bound_does_not_prove_lemma_3() -> None:
    with pytest.raises(InequalityControlError) as caught:
        prove_local_inequalities(angle_upper=Fraction(1))
    assert caught.value.kind == "lemma-3-margin"


def test_strengthened_half_constant_does_not_prove_lemma_5() -> None:
    with pytest.raises(InequalityControlError) as caught:
        prove_local_inequalities(lemma5_constant=Fraction(1, 2))
    assert caught.value.kind == "lemma-5-margin"


@pytest.mark.parametrize(
    ("angle_upper", "constant"),
    ((Fraction(0), Fraction(49, 100)), (Fraction(1, 8), Fraction(0))),
)
def test_nonpositive_domain_mutations_reject(angle_upper: Fraction, constant: Fraction) -> None:
    with pytest.raises(InequalityControlError) as caught:
        prove_local_inequalities(
            angle_upper=angle_upper,
            lemma5_constant=constant,
        )
    assert caught.value.kind == "parameter-domain"


def test_zero_endpoint_inclusion_rejects_strict_claims() -> None:
    with pytest.raises(InequalityControlError) as caught:
        prove_local_inequalities(include_zero=True)
    assert caught.value.kind == "open-domain"


@pytest.mark.parametrize(
    ("angle_upper", "constant"),
    (
        (0.125, Fraction(49, 100)),
        (float("nan"), Fraction(49, 100)),
        (Fraction(1, 8), 0.49),
        (True, Fraction(49, 100)),
    ),
)
def test_inexact_and_boolean_inputs_reject(angle_upper: object, constant: object) -> None:
    with pytest.raises(InequalityControlError) as caught:
        prove_local_inequalities(
            angle_upper=cast(Fraction, angle_upper),
            lemma5_constant=cast(Fraction, constant),
        )
    assert caught.value.kind == "exact-input-required"
