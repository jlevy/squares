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


def test_a_non_integral_element_of_a_biquadratic_field_is_read_without_a_search() -> None:
    """Review B3 of #660: (sqrt(2) + sqrt(3)) / 2 has minimal polynomial 16x^4 - 40x^2 + 1,
    which `sqpack.field`'s irreducibility search cannot certify; the reader retried for
    minutes and raised, and left the shared field refined to thousands of digits. The
    polynomial is irreducible by construction, so only its root count is checked, on a
    copy of the field."""
    field = NumberField([1, 0, -10, 0, 1], (Fraction(3), Fraction(4)))  # sqrt(2) + sqrt(3)
    alpha = field.alpha
    half = exact.of_field_element(alpha / 2)
    assert isinstance(half, exact.Algebraic)
    assert half.polynomial == (16, 0, -40, 0, 1)
    assert Fraction(157, 100) < half < Fraction(158, 100)
    third = exact.of_field_element((alpha + 1) / 3)
    assert isinstance(third, exact.Algebraic)
    assert third.polynomial == (81, -108, -36, 48, -8)
    assert field.refinements == 0
    shifted = exact.of_field_element(alpha + 3)
    assert len(exact.literal(shifted)) < 200


def test_a_side_this_module_did_not_build_is_refused_rather_than_looped(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Review B4 of #660: (x - 2)(x^2 - 2) shares sqrt(2) with x^2 - 2, so bisection never
    separated them. Every narrowing is bounded, and an unseparated pair is refused."""
    monkeypatch.setattr(exact, "MAX_BISECTIONS", 200)
    shared = exact.Algebraic((1, -2, -2, 4), ONE, TWO)
    with pytest.raises(exact.ExactSideError, match="did not separate"):
        exact.compare(shared, SQRT2)
    whole = exact.Algebraic((1, -1), Fraction(1, 2), Fraction(3, 2))  # the root 1
    with pytest.raises(exact.ExactSideError, match="did not round"):
        exact.ceiling(whole, 0)


def test_a_near_tie_never_prints_a_negative_gap() -> None:
    """Review B5 of #660: at sixty digits the gap of sqrt(2) + 10^-90 over sqrt(2) came out
    as -6.2e-61. Where one side is above the other the bound is narrowed until it is
    positive, and it stays a lower bound."""
    tiny = Fraction(1, 10**90)
    near = exact.algebraic([1, -2 * tiny, tiny**2 - 2], (ONE, TWO))
    gap = exact.lower_gap(near, SQRT2)
    assert Fraction(0) < gap <= tiny
    assert tiny - gap < Fraction(1, 10**100)
    assert exact.lower_gap(SQRT2, SQRT2) <= 0


def test_a_closed_form_no_route_here_certifies_is_refused() -> None:
    """Review B3 of #660: sqrt(2) + sqrt(3) + sqrt(5) is a root of a degree-eight
    polynomial reducible modulo every prime, which `sqpack.field` cannot decide
    irreducible; the reader refuses it, and the selection reads its count as unordered."""
    bound = regularize_evand.verified_bound(
        {"verified_upper_bound": "5.3823323", "exact_form": "sqrt(2) + sqrt(3) + sqrt(5)"}
    )
    assert bound is not None
    with pytest.raises(exact.ExactSideError):
        exact.of_bound(bound)


def test_an_algebraic_side_is_written_as_its_root_form_and_read_back_exactly() -> None:
    """think-ot5c (#660 review A1): the house writer states an algebraic house in both lanes
    as `form` writes it, its minimal polynomial in `s` as the register writes one and an
    interval cut at forty places in which it is the one root; `read_form`, the selection's
    `parse_case` and the layer's `verified_bound` read it back as that side."""
    assert exact.polynomial_text((9, -96, 206)) == "9s^2-96s+206"
    assert exact.polynomial_text((1, 0, -2)) == "s^2-2"
    assert exact.polynomial_text((-1, 0, 2)) == "-s^2+2"
    long = (4775, -190430, *([0] * 9), 1, -1)
    assert exact.polynomial_text(long) == "4775s^{12}-190430s^{11}+s-1"
    assert exact.read_polynomial("4775s^{12}-190430s^{11}+s-1=0") == long
    assert exact.read_polynomial("s^8 - 20s^7 + 178s^6") == (1, -20, 178, 0, 0, 0, 0, 0, 0)
    root = exact.algebraic([9, -96, 206], (Fraction(7), Fraction(8)))  # (16 + 5 sqrt 2)/3
    assert isinstance(root, exact.Algebraic)
    form = exact.form(root)
    assert form == (
        "root(9s^2-96s+206, 7.6903559372884917480028145403494967976161, "
        "7.6903559372884917480028145403494967976162)"
    )
    assert exact.read_form(form) == root
    bound = regularize_evand.verified_bound(
        {"verified_upper_bound": exact.ceiling(root, 16), "exact_form": form}
    )
    assert bound is not None
    assert bound.unread is None
    assert bound.polynomial == (9, -96, 206)
    assert exact.of_bound(bound) == root
    assert bound.compare(Fraction(769, 100)) == -1
    assert bound.compare(Fraction(77, 10)) == 1
    # Another `root(` form, as n = 11's names its polynomial, is not this one, and stays
    # unread as before.
    assert exact.read_form("root(P_trump11, 3.877)") is None
    assert exact.read_form("3 + 4 sqrt(2)") is None


def test_a_root_form_that_states_no_isolated_irreducible_root_is_refused() -> None:
    """A written form whose polynomial is reducible, whose interval holds no root or two,
    or that states a rational, is no exact side: the reader refuses it and the layer reads
    the bound as unread, so no comparison rests on it."""
    for form in (
        "root(s^2-4, 1, 3)",  # (s - 2)(s + 2)
        "root(s^2-2, 2, 3)",  # no root there
        "root(s^2-3s+1, 0, 3)",  # two
        "root(2s-3, 1, 2)",  # the rational 3/2
    ):
        with pytest.raises(exact.ExactSideError):
            exact.read_form(form)
        bound = regularize_evand.verified_bound(
            {"verified_upper_bound": "1.5", "exact_form": form}
        )
        assert bound is not None
        assert bound.unread is not None, form
        assert exact.of_bound(bound) is None


@pytest.mark.parametrize(
    ("written", "message"),
    [
        ("5s3", "not a polynomial in s"),  # read as 5s+3 before review A8 of #756
        ("s^2s", "not a polynomial in s"),  # as s^2+s
        ("2 3s", "a space inside a term"),  # as 23s
        ("9 s^2-96s+206", "a space inside a term"),
        ("s^{12-1", "not a polynomial in s"),  # a half-braced exponent
        ("s^2+s^2-2", "written twice"),
        ("9s^2-96s+206=1", "equated to 0"),
    ],
)
def test_a_polynomial_written_otherwise_than_the_register_writes_one_is_refused(
    written: str, message: str
) -> None:
    """The reader is strict (review A8 of #756): every term after the first opens with its
    sign, no space sits inside a term, an exponent is braced whole or bare, no degree is
    written twice, and a closing equation is `=0`. Spaces about the signs stay allowed, as
    n = 11's register entry writes its polynomial."""
    with pytest.raises(exact.ExactSideError, match=message):
        exact.read_polynomial(written)
    if "=" not in written:
        # A root form names no equation, so its reader refuses the same polynomials.
        with pytest.raises(exact.ExactSideError):
            exact.read_form(f"root({written}, 7, 8)")
    assert exact.read_polynomial(" 9s^2 - 96s + 206 = 0 ") == (9, -96, 206)
