"""Fast contracts for the reusable exact-arithmetic and verification boundary."""

from __future__ import annotations

from fractions import Fraction

from sqpack.field import NumberField
from sqpack.verify import verify_packing


def _fraction_sign(value: Fraction) -> int:
    return (value > 0) - (value < 0)


def test_number_field_reduces_equal_elements_and_decides_sign() -> None:
    field = NumberField([1, 0, -2], (Fraction(7, 5), Fraction(3, 2)))
    alpha = field.alpha

    assert alpha * alpha - 2 == field.zero
    assert field.sign(alpha - Fraction(7, 5)) > 0
    assert field.sign(alpha - Fraction(3, 2)) < 0


def test_exact_verifier_distinguishes_contact_from_rational_overlap() -> None:
    first = [
        (Fraction(0), Fraction(0)),
        (Fraction(1), Fraction(0)),
        (Fraction(1), Fraction(1)),
        (Fraction(0), Fraction(1)),
    ]
    touching = [
        (Fraction(1), Fraction(0)),
        (Fraction(2), Fraction(0)),
        (Fraction(2), Fraction(1)),
        (Fraction(1), Fraction(1)),
    ]
    overlapping = [
        (Fraction(99, 100), Fraction(0)),
        (Fraction(199, 100), Fraction(0)),
        (Fraction(199, 100), Fraction(1)),
        (Fraction(99, 100), Fraction(1)),
    ]

    valid = verify_packing([first, touching], Fraction(2), _fraction_sign)
    invalid = verify_packing([first, overlapping], Fraction(2), _fraction_sign)

    assert valid.valid
    assert valid.touching_pairs == 1
    assert invalid.valid is False
    assert invalid.failures == [("overlap", "squares 0 and 1 overlap")]
