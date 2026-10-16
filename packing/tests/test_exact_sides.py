"""Exact sides and their order: `devtools.exact_sides`, which `select_houses` orders every
candidate and every ceiling by, so that no comparison of two sides is left to a person."""

from __future__ import annotations

import itertools
from decimal import Decimal, localcontext
from fractions import Fraction

import pytest

from devtools import exact_sides as exact
from devtools import regularize_evand
from sqpack.field import NumberField

ONE, TWO = Fraction(1), Fraction(2)
SQRT2 = exact.algebraic([1, 0, -2], (ONE, TWO))
CBRT3 = exact.algebraic([1, 0, 0, -3], (ONE, TWO))


def _decimal(side: exact.Side, digits: int = 50) -> Decimal:
    """The side to `digits` places, from an enclosure far tighter, for ordering checks."""
    _low, high = exact.enclosure(side, Fraction(1, 10 ** (digits + 5)))
    with localcontext() as context:
        context.prec = digits + 10
        return Decimal(high.numerator) / Decimal(high.denominator)


def test_a_side_is_held_to_an_isolated_irreducible_root() -> None:
    assert isinstance(SQRT2, exact.Algebraic)
    assert SQRT2.degree == 2
    # The polynomial is made primitive, its leading coefficient positive.
    assert exact.algebraic([-4, 0, 8], (ONE, TWO)) == SQRT2
    halved = exact.algebraic([Fraction(1, 2), 0, -1], (ONE, TWO))
    assert isinstance(halved, exact.Algebraic)
    assert halved.polynomial == (1, 0, -2)
    # A degree-one polynomial is its rational root, inside the interval or refused.
    assert exact.algebraic([3, -5], (ONE, TWO)) == Fraction(5, 3)
    with pytest.raises(exact.ExactSideError, match="does not hold"):
        exact.algebraic([3, -5], (TWO, Fraction(3)))
    with pytest.raises(exact.ExactSideError, match="irreducible"):
        exact.algebraic([1, 0, -4], (ONE, Fraction(3)))  # (x - 2)(x + 2)
    with pytest.raises(exact.ExactSideError, match="irreducible"):
        exact.algebraic([1, 0, -2], (Fraction(-2), TWO))  # two roots
    with pytest.raises(exact.ExactSideError, match="irreducible"):
        exact.algebraic([1, 0, -2], (Fraction(3), Fraction(4)))  # none
    with pytest.raises(exact.ExactSideError, match="nonempty"):
        exact.algebraic([1, 0, -2], (TWO, ONE))
    with pytest.raises(exact.ExactSideError, match="zero polynomial"):
        exact.algebraic([0, 0], (ONE, TWO))


def test_a_rational_is_ordered_against_a_root_exactly_and_is_never_equal_to_it() -> None:
    nearest = Fraction(Decimal("1.41421356237309504880168872420969807856967187537694"))
    for value, order in ((ONE, -1), (TWO, 1), (Fraction(141, 100), -1), (Fraction(3, 2), 1)):
        assert exact.compare(value, SQRT2) == order
        assert exact.compare(SQRT2, value) == -order
    assert nearest < SQRT2 < nearest + Fraction(1, 10**50)
    assert nearest != SQRT2
    assert SQRT2 != 1
    assert SQRT2 > 1


def test_two_roots_of_one_polynomial_are_one_number_where_their_intervals_meet() -> None:
    narrow = exact.algebraic([1, 0, -2], (Fraction(14, 10), Fraction(15, 10)))
    assert narrow == SQRT2
    assert hash(narrow) == hash(SQRT2)
    assert len({narrow, SQRT2}) == 1
    negative = exact.algebraic([1, 0, -2], (Fraction(-2), Fraction(-1)))
    assert negative < SQRT2
    assert exact.compare(SQRT2, negative) == 1


def test_roots_of_different_polynomials_are_ordered_by_narrowing() -> None:
    assert SQRT2 < CBRT3
    assert exact.compare(CBRT3, SQRT2) == 1
    # sqrt(2) + 10^-30 is a root of a different polynomial, 10^-30 away.
    shift = Fraction(1, 10**30)
    near = exact.algebraic([1, -2 * shift, shift**2 - 2], (ONE, TWO))
    assert near > SQRT2
    assert exact.compare(near, SQRT2) == 1
    assert near != SQRT2


def test_a_mixed_list_sorts_as_its_decimals_do() -> None:
    sides: list[exact.Side] = [
        Fraction(3, 2),
        CBRT3,
        SQRT2,
        exact.algebraic([1, 0, -3], (ONE, TWO)),  # sqrt(3)
        Fraction(17, 12),  # 1.41666..., just above sqrt(2)
        exact.algebraic([1, -1, -1], (ONE, TWO)),  # the golden ratio
    ]
    ranked = sorted(sides)
    assert ranked == sorted(sides, key=_decimal)
    for first, second in itertools.pairwise(ranked):
        assert exact.compare(first, second) == -1
        assert first < second
        assert second > first


def test_the_ceiling_rounds_up_and_the_gap_is_a_lower_bound() -> None:
    assert exact.ceiling(SQRT2, 16) == "1.4142135623730951"
    assert exact.ceiling(SQRT2, 0) == "2"
    assert exact.ceiling(Fraction(1, 3), 4) == "0.3334"
    assert exact.ceiling(Fraction(18), 3) == "18.000"
    gap = exact.lower_gap(CBRT3, SQRT2)
    width = Fraction(1, 10**70)
    (cube_low, cube_high), (root_low, root_high) = (
        exact.enclosure(CBRT3, width),
        exact.enclosure(SQRT2, width),
    )
    # The true gap lies between these; the lower bound is under it and within 2e-60.
    assert Fraction(0) < gap <= cube_high - root_low
    assert (cube_low - root_high) - gap < Fraction(3, 10**60)
    assert exact.lower_gap(TWO, ONE) == 1
    low, high = exact.enclosure(SQRT2, Fraction(1, 10**40))
    assert low < SQRT2 < high
    assert high - low <= Fraction(1, 10**40)
    assert exact.enclosure(TWO, Fraction(1, 10)) == (TWO, TWO)
    assert exact.literal(SQRT2) == "root of [1, 0, -2] in (1, 2)"
    assert exact.literal(Fraction(5, 3)) == "5/3"


def test_a_field_element_is_read_by_its_minimal_polynomial() -> None:
    field = NumberField([1, 0, -2], (1, 2))
    root = field.alpha
    # 3 + 4 sqrt(2), the root of x^2 - 6x - 23 near 8.66.
    side = exact.of_field_element(field.rational(3) + root * 4)
    assert isinstance(side, exact.Algebraic)
    assert side.polynomial == (1, -6, -23)
    assert side == exact.algebraic([1, -6, -23], (Fraction(8), Fraction(9)))
    assert exact.of_field_element(field.rational(Fraction(7, 2))) == Fraction(7, 2)
    # In a field of degree four, an element of degree two keeps its own polynomial.
    quartic = NumberField([1, 0, -10, 0, 1], (Fraction(3), Fraction(4)))  # sqrt(2) + sqrt(3)
    alpha = quartic.alpha
    sqrt2 = (alpha**3 - alpha * 9) / 2
    assert exact.of_field_element(sqrt2) == SQRT2


def test_a_closed_form_ceiling_is_read_as_the_layer_reads_its_bound() -> None:
    bound = regularize_evand.verified_bound(
        {"verified_upper_bound": "8.6568542494923801952", "exact_form": "3 + 4 sqrt(2)"}
    )
    assert bound is not None
    side = exact.of_bound(bound)
    assert side == exact.algebraic([1, -6, -23], (Fraction(8), Fraction(9)))
    rational = regularize_evand.verified_bound(
        {"verified_upper_bound": "2.5", "exact_form": "5/2"}
    )
    assert rational is not None
    assert exact.of_bound(rational) == Fraction(5, 2)
    unread = regularize_evand.verified_bound(
        {"verified_upper_bound": "3.877", "exact_form": "root(P_trump11, 3.877)"}
    )
    assert unread is not None
    assert exact.of_bound(unread) is None
