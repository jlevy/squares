"""Exact rational certificate for Bui Section 4.2 Lemmas 3-5."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


class InequalityControlError(ValueError):
    """A typed refusal at the local analytic proof boundary."""

    def __init__(self, kind: str, detail: str):
        super().__init__(detail)
        self.kind = kind


@dataclass(frozen=True)
class LocalInequalityCertificate:
    """Exact margins for the three source inequalities."""

    angle_upper: Fraction
    lower_endpoint_open: bool
    cosine_lower: Fraction
    lemma3_margin: Fraction
    lemma4_difference_coefficients: tuple[Fraction, ...]
    lemma4_factor_coefficients: tuple[Fraction, ...]
    lemma4_cleared_coefficients: tuple[Fraction, ...]
    lemma4_cleared_factor_coefficients: tuple[Fraction, ...]
    lemma5_constant: Fraction
    lemma5_cleared_coefficients: tuple[Fraction, ...]
    lemma5_cleared_factor_coefficients: tuple[Fraction, ...]
    lemma5_derivative_lower: Fraction
    lemma5_margin: Fraction


def _multiply_polynomials(
    left: tuple[Fraction, ...], right: tuple[Fraction, ...]
) -> tuple[Fraction, ...]:
    result = [Fraction(0)] * (len(left) + len(right) - 1)
    for left_power, left_coefficient in enumerate(left):
        for right_power, right_coefficient in enumerate(right):
            result[left_power + right_power] += left_coefficient * right_coefficient
    return tuple(result)


def _subtract_polynomials(
    left: tuple[Fraction, ...], right: tuple[Fraction, ...]
) -> tuple[Fraction, ...]:
    size = max(len(left), len(right))
    return tuple(
        (left[power] if power < len(left) else Fraction(0))
        - (right[power] if power < len(right) else Fraction(0))
        for power in range(size)
    )


def _scale_polynomial(
    polynomial: tuple[Fraction, ...], scalar: Fraction
) -> tuple[Fraction, ...]:
    return tuple(scalar * coefficient for coefficient in polynomial)


def prove_local_inequalities(
    *,
    angle_upper: Fraction = Fraction(1, 8),
    lemma5_constant: Fraction = Fraction(49, 100),
    include_zero: bool = False,
) -> LocalInequalityCertificate:
    """Return exact sufficient margins, or a typed failure for a mutated packet."""
    if type(angle_upper) is not Fraction or type(lemma5_constant) is not Fraction:
        raise InequalityControlError(
            "exact-input-required", "angle and coefficient inputs must be Fractions"
        )
    if type(include_zero) is not bool:
        raise InequalityControlError(
            "parameter-domain", "include_zero must be an explicit boolean"
        )
    if include_zero:
        raise InequalityControlError(
            "open-domain",
            "zero is excluded because all three source inequalities are strict",
        )
    if angle_upper <= 0:
        raise InequalityControlError("parameter-domain", "angle upper bound must be positive")
    if lemma5_constant <= 0:
        raise InequalityControlError("parameter-domain", "Lemma 5 constant must be positive")

    cosine_lower = 1 - angle_upper * angle_upper / 2
    lemma3_margin = cosine_lower - Fraction(100, 101)
    if lemma3_margin <= 0:
        raise InequalityControlError(
            "lemma-3-margin", "the rational cosine lower bound does not prove sec(z)<1.01"
        )

    difference = (Fraction(1), Fraction(2), Fraction(1), Fraction(-4))
    factored = _multiply_polynomials(
        (Fraction(1), Fraction(-1)),
        (Fraction(1), Fraction(3), Fraction(4)),
    )
    if difference != factored:
        raise AssertionError("Lemma 4 polynomial factorization is not exact")

    one_minus_c = (Fraction(1), Fraction(-1))
    one_minus_c_squared = _multiply_polynomials(one_minus_c, one_minus_c)
    one_minus_c2 = (Fraction(1), Fraction(0), Fraction(-1))
    c3 = (Fraction(0), Fraction(0), Fraction(0), Fraction(1))
    lemma4_cleared = _subtract_polynomials(
        _multiply_polynomials(one_minus_c2, one_minus_c2),
        _scale_polynomial(_multiply_polynomials(c3, one_minus_c_squared), Fraction(4)),
    )
    lemma4_cleared_factor = _multiply_polynomials(one_minus_c_squared, difference)
    if lemma4_cleared != lemma4_cleared_factor:
        raise AssertionError("Lemma 4 cleared-denominator identity is not exact")

    c2_one_minus_c = (Fraction(0), Fraction(0), Fraction(1), Fraction(-1))
    lemma5_cleared = _subtract_polynomials(
        c2_one_minus_c,
        _scale_polynomial(one_minus_c2, lemma5_constant),
    )
    lemma5_reduced = (
        -lemma5_constant,
        -lemma5_constant,
        Fraction(1),
    )
    lemma5_cleared_factor = _multiply_polynomials(one_minus_c, lemma5_reduced)
    if lemma5_cleared != lemma5_cleared_factor:
        raise AssertionError("Lemma 5 cleared-denominator identity is not exact")

    derivative_lower = 2 * cosine_lower - lemma5_constant
    lemma5_margin = cosine_lower * cosine_lower - lemma5_constant * (1 + cosine_lower)
    if derivative_lower <= 0:
        raise InequalityControlError(
            "lemma-5-monotonicity", "the reduced Lemma 5 polynomial is not increasing"
        )
    if lemma5_margin <= 0:
        raise InequalityControlError(
            "lemma-5-margin", "the rational cosine lower bound does not prove Lemma 5"
        )

    return LocalInequalityCertificate(
        angle_upper=angle_upper,
        lower_endpoint_open=True,
        cosine_lower=cosine_lower,
        lemma3_margin=lemma3_margin,
        lemma4_difference_coefficients=difference,
        lemma4_factor_coefficients=factored,
        lemma4_cleared_coefficients=lemma4_cleared,
        lemma4_cleared_factor_coefficients=lemma4_cleared_factor,
        lemma5_constant=lemma5_constant,
        lemma5_cleared_coefficients=lemma5_cleared,
        lemma5_cleared_factor_coefficients=lemma5_cleared_factor,
        lemma5_derivative_lower=derivative_lower,
        lemma5_margin=lemma5_margin,
    )
