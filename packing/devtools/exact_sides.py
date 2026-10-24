"""Exact sides, rational or algebraic, and their exact order.

The house at a count is the smallest packing whose certificate has passed stage 4
(packing/campaign/result-import.md, "The House Rule"), and which of two sides is smaller
is decided by exact arithmetic. A comparison is never left to a person, and never to a
print: where this module cannot order two sides, that is a defect of this module to fix.

A side is a `Fraction`, or an `Algebraic`: the one real root of an irreducible integer
polynomial of degree two or more in an open rational interval. `algebraic` builds one and
holds it to that: `sqpack.field.NumberField` decides the polynomial irreducible over Q and
counts exactly one root in the interval, with neither endpoint a root, before any order
is read from it. Every order is then decided by the sign of an integer polynomial at a
rational point:

- a rational side is never an irrational one, and stands below it where it lies at or
  below the interval, above it at or above, and inside it on the side of the root its
  polynomial's sign there gives;
- two algebraic sides with one polynomial are one number when either lies in the other's
  interval, since each interval holds that polynomial's only root there;
- two with different polynomials are different numbers, irreducible polynomials sharing no
  root, and bisecting one interval until the other side falls outside it orders them.

A case record writes an algebraic side as `form` gives it, `root(p, low, high)`: `p` its
minimal polynomial in `s`, highest degree first, as the register writes a
`minimal_polynomial` (`polynomial_text`), and `low` and `high` the side cut and rounded up
at forty places, a rational interval in which it is `p`'s one root. `read_form` reads it
back exactly, holding it to that as `algebraic` does, so the house writer's exact form of
an algebraic house is what `select_houses` and the regularized layer order it by
(`regularize_evand.verified_bound`). A `root(` form that names its polynomial instead, as n
= 11's `root(P_trump11, ...)` does, is not this form, and `read_form` leaves it unread.

`of_field_element` reads an element of a number field, as an algebraic witness states its
side, by its minimal polynomial: the square-free part of its characteristic polynomial.
That polynomial is irreducible by construction, the field's own having been decided so, and
only its root count in the element's enclosure is checked: `sqpack.field`'s irreducibility
search cannot certify every minimal polynomial (review B3 of #660, at the non-integral
elements of a biquadratic field). `of_bound` reads a case record's verified ceiling as
`regularize_evand.verified_bound` holds it, a fraction or a closed form isolated exactly;
a form whose polynomial that search cannot certify is refused, and the selection reads its
count as unordered rather than guessing.

Every narrowing is bounded (`MAX_BISECTIONS`): two different irreducible polynomials share
no root, so a comparison that has not separated them by then was handed sides this module
did not build, and it says so rather than looping (review B4 of #660).
"""

from __future__ import annotations

import copy
import itertools
import math
import re
from collections.abc import Sequence
from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction
from functools import cache
from typing import TYPE_CHECKING

from sqpack.field import FieldElement, FieldPreconditionError, NumberField

if TYPE_CHECKING:
    from devtools.regularize_evand import VerifiedBound


class ExactSideError(ValueError):
    """A side that is not what an exact side must be, or that this module cannot hold."""


#: How many times a comparison or a rounding halves an interval before it gives up: about
#: 3,000 decimal places, where the record's closest distinct sides differ by about 1e-99.
#: A refusal here is an `ExactSideError`, which the selection reads as unordered, never as
#: an order.
MAX_BISECTIONS = 10_000


def _primitive(coefficients: Sequence[Fraction | int]) -> tuple[int, ...]:
    """Integer coefficients, highest degree first, coprime, the leading one positive."""
    values = [Fraction(value) for value in coefficients]
    while values and values[0] == 0:
        values.pop(0)
    if not values:
        raise ExactSideError("the zero polynomial has no roots to isolate")
    denominator = math.lcm(*(value.denominator for value in values))
    integers = [int(value * denominator) for value in values]
    content = math.gcd(*integers)
    integers = [value // content for value in integers]
    return tuple(-value for value in integers) if integers[0] < 0 else tuple(integers)


def _sign(polynomial: Sequence[int], point: Fraction) -> int:
    """The sign of the polynomial at a rational point, in integers: b^d p(a/b)."""
    a, b = point.numerator, point.denominator
    degree = len(polynomial) - 1
    total = sum(
        coefficient * a ** (degree - index) * b**index
        for index, coefficient in enumerate(polynomial)
    )
    return (total > 0) - (total < 0)


def _root_count(polynomial: Sequence[int], low: Fraction, high: Fraction) -> int:
    """How many distinct real roots the square-free polynomial has in (low, high], by
    Sturm's theorem, in exact rational arithmetic."""
    first = [Fraction(value) for value in polynomial]
    degree = len(first) - 1
    sequence = [first, [value * (degree - index) for index, value in enumerate(first[:-1])]]
    while len(sequence[-1]) > 1 or (sequence[-1] and sequence[-1][0] != 0):
        _quotient, remainder = _polynomial_divmod(sequence[-2], sequence[-1])
        if not remainder:
            break
        sequence.append([-value for value in remainder])

    def variations(point: Fraction) -> int:
        signs = []
        for row in sequence:
            total = Fraction(0)
            for value in row:
                total = total * point + value
            if total:
                signs.append(total > 0)
        return sum(left != right for left, right in itertools.pairwise(signs))

    return variations(low) - variations(high)


def _isolated(polynomial: tuple[int, ...], low: Fraction, high: Fraction) -> bool:
    """Whether the polynomial has exactly one root in (low, high) and none at either end."""
    return (
        _sign(polynomial, low) != 0
        and _sign(polynomial, high) != 0
        and _root_count(polynomial, low, high) == 1
    )


@cache
def _validated(polynomial: tuple[int, ...], low: Fraction, high: Fraction) -> None:
    """Refuse a polynomial `sqpack.field` does not decide irreducible, or an interval in
    which it does not count exactly one root; cached, since a degree-41 polynomial takes
    seconds and each house is read many times."""
    if len(polynomial) < 3:
        raise ExactSideError("an algebraic side needs a polynomial of degree two or more")
    try:
        NumberField(polynomial, (low, high))
    except FieldPreconditionError as error:
        raise ExactSideError(f"not an isolated irreducible root: {error}") from error


@dataclass(frozen=True, eq=False)
class Algebraic:
    """The one real root of `polynomial` in the open interval (`low`, `high`).

    `polynomial` is primitive, its leading coefficient positive, highest degree first, and
    irreducible over Q of degree two or more, so it is the root's minimal polynomial and
    the root is irrational. Build one with `algebraic`, which holds it to that; this
    constructor itself checks nothing, so that a narrowing (`bisected`) costs one sign.
    Compared with a `Fraction`, an `int` or another `Algebraic` exactly; equal numbers
    hash alike, since they share a minimal polynomial.
    """

    polynomial: tuple[int, ...]
    low: Fraction
    high: Fraction

    @property
    def degree(self) -> int:
        return len(self.polynomial) - 1

    def bisected(self) -> Algebraic:
        """The same number in the half of its interval that holds it."""
        middle = (self.low + self.high) / 2
        if _sign(self.polynomial, middle) == _sign(self.polynomial, self.low):
            return Algebraic(self.polynomial, middle, self.high)
        return Algebraic(self.polynomial, self.low, middle)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, int | Fraction | Algebraic):
            return compare(self, other) == 0
        return NotImplemented

    def __hash__(self) -> int:
        return hash(("algebraic", self.polynomial))

    def __lt__(self, other: object) -> bool:
        if isinstance(other, int | Fraction | Algebraic):
            return compare(self, other) < 0
        return NotImplemented

    def __le__(self, other: object) -> bool:
        if isinstance(other, int | Fraction | Algebraic):
            return compare(self, other) <= 0
        return NotImplemented

    def __gt__(self, other: object) -> bool:
        if isinstance(other, int | Fraction | Algebraic):
            return compare(self, other) > 0
        return NotImplemented

    def __ge__(self, other: object) -> bool:
        if isinstance(other, int | Fraction | Algebraic):
            return compare(self, other) >= 0
        return NotImplemented

    def __repr__(self) -> str:
        return f"Algebraic({literal(self)})"


#: A side: rational, or the isolated root of an irreducible polynomial.
type Side = Fraction | Algebraic


def algebraic(coefficients: Sequence[Fraction | int], interval: Sequence[Fraction]) -> Side:
    """The side that is the one root of the polynomial (highest degree first) in the open
    interval: a `Fraction` where the polynomial is of degree one, else an `Algebraic`."""
    polynomial = _primitive(coefficients)
    low, high = (Fraction(end) for end in interval)
    if not low < high:
        raise ExactSideError("an isolating interval must be nonempty")
    if len(polynomial) == 2:
        root = Fraction(-polynomial[1], polynomial[0])
        if not low < root < high:
            raise ExactSideError("the interval does not hold the polynomial's root")
        return root
    _validated(polynomial, low, high)
    return Algebraic(polynomial, low, high)


def _rational_against(value: Fraction, side: Algebraic) -> int:
    """-1, 1 as the rational is below or above the algebraic side; never equal."""
    if value <= side.low:
        return -1
    if value >= side.high:
        return 1
    # The side is the only root in (low, high), and a simple one, so the polynomial keeps
    # the sign it has at `low` up to the root and changes it there.
    return -1 if _sign(side.polynomial, value) == _sign(side.polynomial, side.low) else 1


def _algebraic_order(first: Algebraic, second: Algebraic) -> int:
    if first.polynomial == second.polynomial:
        # One polynomial: `first` is one of its roots, and `second`'s interval holds only
        # one, so `first` lies in that interval exactly where it is `second`.
        if _rational_against(second.high, first) < 0:
            return 1
        if _rational_against(second.low, first) > 0:
            return -1
        return 0
    # Different irreducible polynomials share no root: narrow `second` until `first` lies
    # outside its interval, which it must once the interval is narrower than their gap.
    narrowed = second
    for _step in range(MAX_BISECTIONS):
        if _rational_against(narrowed.low, first) > 0:
            return -1
        if _rational_against(narrowed.high, first) < 0:
            return 1
        narrowed = narrowed.bisected()
    raise ExactSideError(
        f"{literal(first)} and {literal(second)} did not separate: one of them is not "
        "the isolated root of an irreducible polynomial (build sides with `algebraic`)"
    )


def compare(first: Side | int, second: Side | int) -> int:
    """-1, 0 or 1 as `first` is below, equal to or above `second`, decided exactly."""
    if isinstance(first, Algebraic):
        if isinstance(second, Algebraic):
            return _algebraic_order(first, second)
        return -_rational_against(Fraction(second), first)
    if isinstance(second, Algebraic):
        return _rational_against(Fraction(first), second)
    a, b = Fraction(first), Fraction(second)
    return (a > b) - (a < b)


def enclosure(side: Side, width: Fraction) -> tuple[Fraction, Fraction]:
    """Rationals `low <= side <= high` with `high - low <= width`; the side twice if it is
    rational."""
    if not isinstance(side, Algebraic):
        return side, side
    narrowed = side
    while narrowed.high - narrowed.low > width:
        narrowed = narrowed.bisected()
    return narrowed.low, narrowed.high


def ceiling(side: Side, places: int) -> str:
    """The side rounded up at `places` decimals, as a case record prints an exact side."""
    scale = 10**places
    if isinstance(side, Algebraic):
        narrowed = side
        # An irrational side is no multiple of 1/scale, so its interval shrinks to one
        # that holds none, and every number in it rounds up alike.
        for _step in range(MAX_BISECTIONS):
            if math.floor(narrowed.low * scale) == math.floor(narrowed.high * scale):
                break
            narrowed = narrowed.bisected()
        else:
            raise ExactSideError(f"{literal(side)} did not round: it is not irrational")
        whole = math.floor(narrowed.high * scale) + 1
    else:
        scaled = side * scale
        whole = -(-scaled.numerator // scaled.denominator)
    if places == 0:
        return str(whole)
    text = str(whole).rjust(places + 1, "0")
    return f"{text[:-places]}.{text[-places:]}"


def lower_gap(high: Side, low: Side, digits: int = 60) -> Fraction:
    """A rational at most `high - low`: the difference itself where both are rational,
    else within 2 * 10**-digits of it, narrowed further where `high` is above `low` until
    the bound is positive, so a near tie never prints as a negative gap (review B5 of
    #660). It is for prose and tables and decides nothing."""
    if not isinstance(high, Algebraic) and not isinstance(low, Algebraic):
        return high - low
    above = compare(high, low) > 0
    while True:
        width = Fraction(1, 10**digits)
        gap = enclosure(high, width)[0] - enclosure(low, width)[1]
        if gap > 0 or not above:
            return gap
        digits *= 2


def literal(side: Side) -> str:
    """A side as text a reader can parse back: the fraction, or the polynomial (highest
    degree first) with the interval its root is the only one in."""
    if not isinstance(side, Algebraic):
        return str(side)
    coefficients = ", ".join(str(value) for value in side.polynomial)
    return f"root of [{coefficients}] in ({side.low}, {side.high})"


#: The places an algebraic side's written interval is cut at: forty, as the register prints
#: such a side (T-193's claim), doubled wherever forty do not isolate the root.
FORM_PLACES = 40
#: One monomial of a polynomial in `s` as the register writes it: `4775s^{18}`, `-96s`,
#: `+206` (`devtools.intake_ledger.polynomial` reads the same), its exponent in braces or
#: bare, never half-braced.
_MONOMIAL = re.compile(r"([+-]?)([0-9]*)(s(?:\^(?:\{([0-9]+)\}|([0-9]+)))?)?")
#: Spaces a written polynomial may hold: about the signs between its terms, and at its ends.
_SIGN_SPACES = re.compile(r"\s*([+-])\s*")
_DECIMAL = r"[0-9]+(?:\.[0-9]+)?"
#: `form`'s text: the polynomial, then the interval's two ends as decimals.
_ROOT_FORM = re.compile(
    rf"root\((?P<polynomial>[0-9s^{{}}+\- ]+),\s*(?P<low>{_DECIMAL}),\s*(?P<high>{_DECIMAL})\)"
)


def polynomial_text(polynomial: Sequence[int]) -> str:
    """An integer polynomial, highest degree first, as the register writes a minimal
    polynomial in `s`: ``9s^2-96s+206``, an exponent of two digits or more in braces,
    ``4775s^{18}``."""
    degree = len(polynomial) - 1
    terms = []
    for index, coefficient in enumerate(polynomial):
        if coefficient == 0:
            continue
        power = degree - index
        sign = "-" if coefficient < 0 else ("+" if terms else "")
        magnitude = "" if abs(coefficient) == 1 and power else str(abs(coefficient))
        variable = "" if power == 0 else "s" if power == 1 else f"s^{power}"
        if power >= 10:
            variable = f"s^{{{power}}}"
        terms.append(f"{sign}{magnitude}{variable}")
    if not terms:
        raise ExactSideError("the zero polynomial has no written form")
    return "".join(terms)


def read_polynomial(text: str) -> tuple[int, ...]:
    """The integer coefficients, highest degree first, of a polynomial `polynomial_text`
    writes, with or without spaces about the signs between its terms and a closing ``=0``.

    Read strictly (review A8 of #756): every term but the first opens with its sign, so
    ``5s3`` and ``s^2s`` are refused rather than read as ``5s+3`` and ``s^2+s``; a space
    inside a term, as in ``2 3s``, is refused rather than read as ``23s``; so are a
    right-hand side other than ``0``, a half-braced exponent and a degree written twice."""
    left, equals, right = text.partition("=")
    if equals and right.strip() != "0":
        raise ExactSideError(f"not a polynomial in s equated to 0: {text!r}")
    written = _SIGN_SPACES.sub(r"\1", left.strip())
    if any(character.isspace() for character in written):
        raise ExactSideError(f"a space inside a term of {text!r}")
    coefficients: dict[int, int] = {}
    position = 0
    while position < len(written):
        match = _MONOMIAL.match(written, position)
        if match is None or match.end() == position or (position and not match.group(1)):
            raise ExactSideError(f"not a polynomial in s: {text!r}")
        sign = -1 if match.group(1) == "-" else 1
        if match.group(3):
            exponent = match.group(4) or match.group(5)
            power, coefficient = int(exponent or 1), int(match.group(2) or 1)
        elif match.group(2):
            power, coefficient = 0, int(match.group(2))
        else:
            raise ExactSideError(f"not a polynomial in s: {text!r}")
        if power in coefficients:
            raise ExactSideError(f"s^{power} is written twice in {text!r}")
        coefficients[power] = sign * coefficient
        position = match.end()
    if not coefficients:
        raise ExactSideError(f"not a polynomial in s: {text!r}")
    return tuple(coefficients.get(power, 0) for power in range(max(coefficients), -1, -1))


def _cut(value: Fraction, places: int, *, up: bool) -> str:
    """A rational cut down, or rounded up, at `places` decimals."""
    scaled = value * 10**places
    whole = -(-scaled.numerator // scaled.denominator) if up else math.floor(scaled)
    text = str(whole).rjust(places + 1, "0")
    return f"{text[:-places]}.{text[-places:]}"


def form(side: Algebraic) -> str:
    """The side as a case record writes it exactly: ``root(p, low, high)``, its minimal
    polynomial in `s` and the side cut and rounded up at `FORM_PLACES` decimals, an interval
    in which it is the polynomial's one root, with more places where forty do not isolate
    it. `read_form` reads it back as this side."""
    places = FORM_PLACES
    for _step in range(8):
        low, high = enclosure(side, Fraction(1, 10 ** (places + 2)))
        below, above = _cut(low, places, up=False), _cut(high, places, up=True)
        ends = Fraction(Decimal(below)), Fraction(Decimal(above))
        if ends[0] < ends[1] and _isolated(side.polynomial, *ends):
            return f"root({polynomial_text(side.polynomial)}, {below}, {above})"
        places *= 2
    raise ExactSideError(f"no decimal interval isolates {literal(side)}")


def read_form(text: str) -> Side | None:
    """The side a `form` text states, held as `algebraic` holds one: an irreducible
    polynomial with exactly one root in the interval. None where the text is not that form,
    such as a closed form or a `root(` form that names its polynomial; a text of the form
    that does not state such a root is refused (`ExactSideError`)."""
    match = _ROOT_FORM.fullmatch(text.strip())
    if match is None:
        return None
    polynomial = read_polynomial(match.group("polynomial"))
    low, high = (Fraction(Decimal(match.group(end))) for end in ("low", "high"))
    side = algebraic(polynomial, (low, high))
    if not isinstance(side, Algebraic):
        raise ExactSideError(f"{text!r} states a rational side, which is written as a fraction")
    return side


def _polynomial_divmod(
    numerator: list[Fraction], denominator: list[Fraction]
) -> tuple[list[Fraction], list[Fraction]]:
    """Long division of polynomials over Q, highest degree first."""
    remainder = list(numerator)
    quotient: list[Fraction] = []
    while len(remainder) >= len(denominator):
        factor = remainder[0] / denominator[0]
        quotient.append(factor)
        for index, value in enumerate(denominator):
            remainder[index] -= factor * value
        remainder.pop(0)
    while remainder and remainder[0] == 0:
        remainder.pop(0)
    return quotient, remainder


def _gcd(first: list[Fraction], second: list[Fraction]) -> list[Fraction]:
    a, b = first, second
    while b:
        a, b = b, _polynomial_divmod(a, b)[1]
    return [value / a[0] for value in a]


def _characteristic(matrix: list[list[Fraction]]) -> list[Fraction]:
    """The characteristic polynomial det(x I - M), highest degree first, by Faddeev and
    LeVerrier's recursion over Q."""
    size = len(matrix)
    identity = [[Fraction(int(i == j)) for j in range(size)] for i in range(size)]
    coefficients = [Fraction(1)]
    power = [[Fraction(0)] * size for _ in range(size)]
    for k in range(1, size + 1):
        power = [
            [
                sum((matrix[i][m] * power[m][j] for m in range(size)), Fraction(0))
                + coefficients[-1] * identity[i][j]
                for j in range(size)
            ]
            for i in range(size)
        ]
        trace = sum(
            (sum((matrix[i][m] * power[m][i] for m in range(size)), Fraction(0)))
            for i in range(size)
        )
        coefficients.append(-Fraction(trace) / k)
    return coefficients


def _enclosed(element: FieldElement, digits: int) -> tuple[Fraction, Fraction]:
    """The element's enclosure at `digits` places, rounded outward to them: narrowed on a
    copy of its field, so the narrowing never reaches the field the element belongs to,
    and rounded, so neither does how far that field was refined before (review B3 of
    #660, where an interval of thousands of digits outran `literal`)."""
    field = copy.copy(element.field)
    field.refine_to(digits)
    low, high = (Fraction(end) for end in field.enclose(element))
    scale = 10**digits
    return (
        Fraction(math.floor(low * scale), scale),
        Fraction(math.ceil(high * scale), scale),
    )


def of_field_element(element: FieldElement, digits: int = 30) -> Side:
    """The exact side an element of a number field is, by its minimal polynomial.

    Multiplication by the element is a linear map on the field's power basis; its
    characteristic polynomial is a power of the minimal polynomial, so the square-free
    part is that polynomial, irreducible since the field's own polynomial was decided
    irreducible. The element's enclosure, narrowed until it holds exactly one root of it,
    isolates the right one; only that root count is checked (`_isolated`).
    """
    field = element.field
    basis = [field.alpha**j for j in range(field.degree)]
    columns = [(element * power).coeffs for power in basis]
    size = field.degree
    matrix = [[Fraction(columns[j][i]) for j in range(size)] for i in range(size)]
    characteristic = _characteristic(matrix)
    derivative = [
        value * (len(characteristic) - 1 - index)
        for index, value in enumerate(characteristic[:-1])
    ]
    common = _gcd(characteristic, derivative) if derivative else [Fraction(1)]
    minimal, remainder = _polynomial_divmod(characteristic, common)
    if remainder:
        raise ExactSideError("the characteristic polynomial did not divide exactly")
    polynomial = _primitive(minimal)
    if len(polynomial) == 2:
        return Fraction(-polynomial[1], polynomial[0])
    while True:
        low, high = _enclosed(element, digits)
        if low < high and _isolated(polynomial, low, high):
            return Algebraic(polynomial, low, high)
        if digits > 4000:
            raise ExactSideError(
                f"no enclosure up to {digits} digits isolates the element's root of "
                f"{list(polynomial)}"
            )
        digits *= 2


def of_bound(bound: VerifiedBound) -> Side | None:
    """A case's verified ceiling as `regularize_evand.verified_bound` holds it exactly: its
    fraction, or its closed form's isolated root; None where that driver could not read the
    form (`VerifiedBound.unread`), which no comparison may then rest on."""
    if bound.rational is not None:
        return bound.rational
    if bound.interval is None:
        return None
    return algebraic(bound.polynomial, bound.interval)
