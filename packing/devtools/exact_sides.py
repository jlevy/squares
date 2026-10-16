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

`of_field_element` reads an element of a number field, as an algebraic witness states its
side, by its minimal polynomial: the square-free part of its characteristic polynomial.
`of_bound` reads a case record's verified ceiling as `regularize_evand.verified_bound`
holds it, a fraction or a closed form isolated exactly.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction
from functools import cache
from typing import TYPE_CHECKING

from sqpack.field import FieldElement, FieldPreconditionError, NumberField

if TYPE_CHECKING:
    from devtools.regularize_evand import VerifiedBound


class ExactSideError(ValueError):
    """A side that is not what an exact side must be, or that this module cannot hold."""


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
    while True:
        if _rational_against(narrowed.low, first) > 0:
            return -1
        if _rational_against(narrowed.high, first) < 0:
            return 1
        narrowed = narrowed.bisected()


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
        while math.floor(narrowed.low * scale) != math.floor(narrowed.high * scale):
            narrowed = narrowed.bisected()
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
    else within 2 * 10**-digits of it. It is for prose and tables and decides nothing."""
    if not isinstance(high, Algebraic) and not isinstance(low, Algebraic):
        return high - low
    width = Fraction(1, 10**digits)
    return enclosure(high, width)[0] - enclosure(low, width)[1]


def literal(side: Side) -> str:
    """A side as text a reader can parse back: the fraction, or the polynomial (highest
    degree first) with the interval its root is the only one in."""
    if not isinstance(side, Algebraic):
        return str(side)
    coefficients = ", ".join(str(value) for value in side.polynomial)
    return f"root of [{coefficients}] in ({side.low}, {side.high})"


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


def of_field_element(element: FieldElement, digits: int = 30) -> Side:
    """The exact side an element of a number field is, by its minimal polynomial.

    Multiplication by the element is a linear map on the field's power basis; its
    characteristic polynomial is a power of the minimal polynomial, so the square-free
    part is that polynomial. The element's enclosure, narrowed until it holds one root,
    isolates the right one.
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
        field.refine_to(digits)
        low, high = field.enclose(element)
        try:
            return algebraic(polynomial, (Fraction(low), Fraction(high)))
        except ExactSideError:
            if digits > 4000:
                raise
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
