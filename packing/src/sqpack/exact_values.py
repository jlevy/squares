"""The algebraic facts a frontier record holds about its side, and where each came from.

A record's `reported_upper_bound` carries up to three exact facts about the side `s` of
the best known packing: a closed form (`exact_form`), the degree of `s` over the
rationals (`algebraic_degree`) and its minimal polynomial (`minimal_polynomial`).
The catalogue prints either a radical or a degree with its polynomial, never both, so
for a radical this repository computes the other two. `algebraic_source` says which
happened, because transcribing a source's claim and computing one here are different
acts (think-18mu, think-kj6n):

- `catalogue`: the source prints the degree, and the polynomial where it gives one;
- `derived-from-exact-form`: computed here from the source's closed form;
- `contact-system`: computed here from an exact contact system, with evidence cited.

The polynomial is stored in the catalogue's own notation, `2s^2 - 28s + 97 = 0`, with
primitive integer coefficients and a positive leading coefficient, so a derived record
reads like a transcribed one and `kingbird_catalogue.normalized_polynomial` reads both.

SymPy is an optional dependency and is imported where it is used.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

CATALOGUE = "catalogue"
DERIVED_FROM_EXACT_FORM = "derived-from-exact-form"
CONTACT_SYSTEM = "contact-system"

#: The schema's `algebraic_source` vocabulary, in the order a reader meets it.
ALGEBRAIC_SOURCES = (CATALOGUE, DERIVED_FROM_EXACT_FORM, CONTACT_SYSTEM)

SIDE_SYMBOL = "s"


@dataclass(frozen=True)
class AlgebraicFacts:
    """A side's degree and minimal polynomial, as primitive integer coefficients."""

    coefficients: tuple[int, ...]
    """Highest degree first, primitive, with a positive leading coefficient."""

    @property
    def degree(self) -> int:
        return len(self.coefficients) - 1

    @property
    def text(self) -> str:
        return format_polynomial(self.coefficients)


def format_polynomial(coefficients: tuple[int, ...] | list[int]) -> str:
    """Print integer coefficients, highest first, as `2s^2 - 28s + 97 = 0`.

    Exponents of ten or more are braced, `s^{10}`, as the catalogue prints them.
    """
    if not coefficients or coefficients[0] == 0:
        raise ValueError(f"not a polynomial with a nonzero leading term: {coefficients!r}")
    degree = len(coefficients) - 1
    terms: list[str] = []
    for index, coefficient in enumerate(coefficients):
        if coefficient == 0:
            continue
        power = degree - index
        magnitude = abs(coefficient)
        if power == 0:
            body = str(magnitude)
        else:
            monomial = SIDE_SYMBOL if power == 1 else f"{SIDE_SYMBOL}^{_exponent(power)}"
            body = monomial if magnitude == 1 else f"{magnitude}{monomial}"
        if not terms:
            terms.append(body if coefficient > 0 else f"-{body}")
        else:
            terms.append(f"+ {body}" if coefficient > 0 else f"- {body}")
    return " ".join(terms) + " = 0"


def _exponent(power: int) -> str:
    return str(power) if power < 10 else f"{{{power}}}"


def derive_from_exact_form(exact_form: str) -> AlgebraicFacts:
    """The minimal polynomial over the rationals of the number a closed form denotes."""
    try:
        rational = Fraction(exact_form)
    except ValueError:
        pass
    else:
        return AlgebraicFacts((rational.denominator, -rational.numerator))

    import sympy as sp  # noqa: PLC0415 - optional dependency, imported where it is used
    from sympy.parsing.sympy_parser import (  # noqa: PLC0415
        implicit_multiplication_application,
        parse_expr,
        standard_transformations,
    )

    transformations = (*standard_transformations, implicit_multiplication_application)
    value = parse_expr(exact_form, transformations=transformations)
    if value.free_symbols:
        raise ValueError(f"exact form is not a number: {exact_form!r}")
    side = sp.Symbol(SIDE_SYMBOL)
    polynomial = sp.Poly(sp.minimal_polynomial(value, side), side)
    return AlgebraicFacts(primitive(tuple(int(c) for c in polynomial.all_coeffs())))


def primitive(coefficients: tuple[int, ...]) -> tuple[int, ...]:
    """Divide out the content and make the leading coefficient positive."""
    from math import gcd  # noqa: PLC0415

    content = 0
    for coefficient in coefficients:
        content = gcd(content, coefficient)
    if content == 0:
        raise ValueError("the zero polynomial has no primitive form")
    sign = -1 if coefficients[0] < 0 else 1
    return tuple(sign * coefficient // content for coefficient in coefficients)


def algebraic_fields(
    exact_form: str | None, degree: int | None, polynomial: str | None
) -> dict[str, object]:
    """The record's `algebraic_degree`, `minimal_polynomial` and `algebraic_source`.

    A degree the source prints is kept as transcribed, with its polynomial where it gives
    one. A rational closed form supplies an omitted degree-one polynomial; otherwise a
    closed form fixes both, and they are derived from it. Neither leaves
    all three null: no exact fact is on hand.
    """
    if degree == 1 and polynomial is None and exact_form is not None:
        facts = derive_from_exact_form(exact_form)
        if facts.degree != degree:
            raise ValueError(f"degree {degree} disagrees with exact form {exact_form!r}")
        return {
            "algebraic_degree": facts.degree,
            "minimal_polynomial": facts.text,
            "algebraic_source": DERIVED_FROM_EXACT_FORM,
        }
    if degree is not None:
        return {
            "algebraic_degree": degree,
            "minimal_polynomial": polynomial,
            "algebraic_source": CATALOGUE,
        }
    if exact_form is not None:
        facts = derive_from_exact_form(exact_form)
        return {
            "algebraic_degree": facts.degree,
            "minimal_polynomial": facts.text,
            "algebraic_source": DERIVED_FROM_EXACT_FORM,
        }
    return {"algebraic_degree": None, "minimal_polynomial": None, "algebraic_source": None}
