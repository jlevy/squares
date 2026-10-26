"""Exact scalars of a regularized view: rationals, or elements of a witness's number field.

A regularized view is written in the scalar kind of the witness it is a view of. Over `Q`
a coordinate is a `Fraction`; over a real number field `Q(alpha)`, the field of an
algebraic house (think-mbdw), it is an `sqpack.field.FieldElement`. The regularization
tools hold both kinds through these helpers, so that a side, a centre or a rotation is
parsed, written, compared and approximated one way wherever it is read:

- `field_of` builds a witness's field from its `scalar` block, one field per block, so
  that a view and the witness it is a view of, which state the same block, share it and
  their elements combine (`sqpack.field` refuses elements of two field objects).
- `parse` reads the witness format's literal: a rational string, or the coefficient
  strings of a polynomial in `alpha`, lowest degree first.
- `scalar` writes it back in that format, and `text` as one string for a report or an
  index entry: a rational as `p/q`, a field element as its coefficient list,
  `['2863/164', '155/164', ...]`, the form the default record already gives a
  number-field witness's side. `parse_text` reads that string back.
- `equal` and `compare` decide exactly; `approximate` and `decimal` are for reports and
  binary64 work only, and decide nothing.

The exact decisions are `sqpack.field`'s (the first exact route's arithmetic); the second
route over a number field, `devtools.check_algebraic_witness_independent`, shares none of
this and reads a view from its own text.
"""

from __future__ import annotations

import ast
import functools
from collections.abc import Mapping, Sequence
from decimal import ROUND_HALF_EVEN, Decimal, localcontext
from fractions import Fraction
from typing import Any

from sqpack.field import FieldElement, NumberField

type Scalar = Fraction | FieldElement

NUMBER_FIELD = "algebraic-number-field"


def is_field(value: object) -> bool:
    return isinstance(value, FieldElement)


@functools.cache
def _field(polynomial: tuple[str, ...], interval: tuple[str, str]) -> NumberField:
    return NumberField(
        [Fraction(value) for value in polynomial], tuple(Fraction(v) for v in interval)
    )


def field_of(witness: Mapping[str, Any]) -> NumberField | None:
    """The witness's number field, one object per `scalar` block; None over `Q`."""
    scalar = witness.get("scalar") or {}
    if scalar.get("kind") != NUMBER_FIELD:
        return None
    polynomial = tuple(str(value) for value in scalar["minimal_polynomial"])
    low, high = (str(value) for value in scalar["isolating_interval"])
    return _field(polynomial, (low, high))


def _rational_literal(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def rational_part(value: FieldElement) -> Fraction | None:
    """The element as a rational where it is one, else None."""
    if all(coefficient == 0 for coefficient in value.coeffs[1:]):
        return Fraction(value.coeffs[0]) if value.coeffs else Fraction(0)
    return None


def parse(value: Any, field: NumberField | None) -> Scalar:
    """A witness-format literal, in `field` where there is one."""
    if field is None:
        if isinstance(value, list):
            raise ValueError("a coefficient list outside a number field")
        return Fraction(str(value))
    if isinstance(value, list):
        return field.element([Fraction(str(item)) for item in value])
    return field.rational(Fraction(str(value)))


def scalar(value: Scalar) -> str | list[str]:
    """`value` in the witness format: a rational string or coefficient strings."""
    if isinstance(value, FieldElement):
        rational = rational_part(value)
        if rational is not None:
            return _rational_literal(rational)
        return [_rational_literal(Fraction(c)) for c in value.coeffs]
    return _rational_literal(Fraction(value))


def text(value: Scalar) -> str:
    """`value` as one string: `scalar`'s, a coefficient list written as a Python list."""
    written = scalar(value)
    return written if isinstance(written, str) else str(written)


def parse_text(written: str, field: NumberField | None) -> Scalar:
    """`text`'s string, or a witness's side as `str` writes it, read back."""
    stripped = written.strip()
    if stripped.startswith("["):
        items = ast.literal_eval(stripped)
        if not isinstance(items, list):
            raise ValueError(f"not a coefficient list: {written!r}")
        if field is None:
            raise ValueError(f"a coefficient list outside a number field: {written!r}")
        return parse([str(item) for item in items], field)
    return parse(stripped, field)


def in_field(value: Scalar, field: NumberField) -> FieldElement:
    """`value` as an element of `field`: a rational, or an element of a field object with
    the same polynomial and interval, whose coefficients mean the same there."""
    if isinstance(value, FieldElement):
        if value.field is field:
            return value
        if not same_field(value.field, field):
            raise ValueError("elements of two different number fields")
        return field.element(list(value.coeffs))
    return field.rational(Fraction(value))


def same_field(left: NumberField, right: NumberField) -> bool:
    if left is right:
        return True
    return (
        left.precondition_certificate()["normalized_minimal_polynomial"]
        == right.precondition_certificate()["normalized_minimal_polynomial"]
        and left.precondition_certificate()["declared_isolating_interval"]
        == right.precondition_certificate()["declared_isolating_interval"]
    )


def _common(left: Scalar, right: Scalar) -> tuple[Scalar, Scalar]:
    if isinstance(left, FieldElement):
        return left, in_field(right, left.field)
    if isinstance(right, FieldElement):
        return in_field(left, right.field), right
    return Fraction(left), Fraction(right)


def compare(left: Scalar, right: Scalar) -> int:
    """-1, 0 or 1 as `left` is below, at or above `right`, decided exactly."""
    a, b = _common(left, right)
    if isinstance(a, FieldElement) and isinstance(b, FieldElement):
        return (a - b).sign()
    return (a > b) - (a < b)


def equal(left: Scalar, right: Scalar) -> bool:
    return compare(left, right) == 0


def approximate(value: Scalar, digits: int = 60) -> Fraction:
    """A rational within `10^-digits` of `value`: for reports and binary64 work only."""
    if isinstance(value, FieldElement):
        field = value.field
        field.refine_to(digits + 12)
        low, high = field.enclose(value)
        return (low + high) / 2
    return Fraction(value)


def decimal_text(value: Scalar, digits: int = 40) -> str:
    """`value` to `digits` significant digits, rounded to nearest, in fixed notation."""
    rational = approximate(value, digits + 20)
    with localcontext() as context:
        context.prec = digits
        context.rounding = ROUND_HALF_EVEN
        number = Decimal(rational.numerator) / Decimal(rational.denominator)
    return format(number, "f")


def absolute(value: Scalar) -> Scalar:
    """`|value|`, exactly."""
    if isinstance(value, FieldElement):
        return -value if value.sign() < 0 else value
    return abs(value)


def zero_like(values: Sequence[Scalar]) -> Scalar:
    """Zero in the field of the first field element among `values`, else `Fraction(0)`."""
    for value in values:
        if isinstance(value, FieldElement):
            return value.field.zero
    return Fraction(0)
