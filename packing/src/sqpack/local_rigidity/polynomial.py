"""Sparse multivariate polynomials whose coefficients live in an exact number field.

The half-angle chart turns every packing constraint into a polynomial in fifteen chart
variables with coefficients in `Q(sqrt 2)`, and the whole point of `H-060` is that those
polynomials are decided by exact sign rather than by tolerance. So the arithmetic here is
`FieldElement` arithmetic throughout: there is no float anywhere in this module, not even
for ordering or for a heuristic, and `sqpack.field.FieldElement.sign` is the only decision
procedure used.

A polynomial is a mapping from exponent tuples to nonzero field coefficients. Sparsity is
not an optimisation here so much as a normal form: two polynomials are equal exactly when
their term dictionaries agree, because a coefficient that reduces to zero is dropped at
construction, and `FieldElement.is_zero` is exact.

Three operations carry the instrument:

- `evaluate` gives an exact base margin, which is what the neighborhood argument rests on;
- `derivative` gives the exact chart gradient, which is what binds to `T-012`'s `A`;
- `restrict_to_line` gives the exact univariate jet along a chart direction, whose
  order-two coefficient is what binds to `T-012`'s `q`.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from itertools import zip_longest

from sqpack.field import FieldElement, NumberField

Exponents = tuple[int, ...]


class ArityError(ValueError):
    """Two polynomials from different chart dimensions were combined.

    Raised rather than broadcast. A silent zero-pad would let a fourteen-variable
    constraint be added to a fifteen-variable one and produce a polynomial that is not the
    constraint either factor describes -- and the sum would still evaluate, still have a
    sign, and still look like evidence.
    """


@dataclass(frozen=True, slots=True)
class Poly:
    """A polynomial in `arity` variables over one `NumberField`.

    Construct through `Poly.constant`, `Poly.variable` or `Poly.from_terms`; the
    constructor itself does not normalise, and an unnormalised term dictionary breaks the
    equality normal form.
    """

    field: NumberField
    arity: int
    terms: Mapping[Exponents, FieldElement]

    # -- construction ------------------------------------------------------

    @staticmethod
    def from_terms(
        field: NumberField, arity: int, terms: Mapping[Exponents, FieldElement]
    ) -> Poly:
        """Normalise a term mapping: drop exactly-zero coefficients, check every key."""
        kept: dict[Exponents, FieldElement] = {}
        for exponents, coefficient in terms.items():
            if len(exponents) != arity:
                raise ArityError(
                    f"exponent tuple {exponents} has length {len(exponents)}, not {arity}"
                )
            if any(power < 0 for power in exponents):
                raise ValueError(f"negative exponent in {exponents}")
            if not coefficient.is_zero():
                kept[exponents] = coefficient
        return Poly(field, arity, kept)

    @staticmethod
    def constant(field: NumberField, arity: int, value: FieldElement) -> Poly:
        return Poly.from_terms(field, arity, {(0,) * arity: value})

    @staticmethod
    def zero(field: NumberField, arity: int) -> Poly:
        return Poly(field, arity, {})

    @staticmethod
    def variable(field: NumberField, arity: int, index: int) -> Poly:
        if not 0 <= index < arity:
            raise IndexError(f"variable {index} is outside 0..{arity - 1}")
        exponents = tuple(1 if position == index else 0 for position in range(arity))
        return Poly.from_terms(field, arity, {exponents: field.one})

    # -- structure ---------------------------------------------------------

    def _check(self, other: Poly) -> None:
        if other.field is not self.field:
            raise ArityError("polynomials come from different number fields")
        if other.arity != self.arity:
            raise ArityError(
                f"polynomials have different arities: {self.arity} and {other.arity}"
            )

    def is_zero(self) -> bool:
        return not self.terms

    def degree(self) -> int:
        """Total degree, with the zero polynomial reported as -1."""
        if not self.terms:
            return -1
        return max(sum(exponents) for exponents in self.terms)

    def support(self) -> tuple[int, ...]:
        """The variables this polynomial actually mentions, ascending."""
        used = {
            index for exponents in self.terms for index, power in enumerate(exponents) if power
        }
        return tuple(sorted(used))

    # -- arithmetic --------------------------------------------------------

    def __add__(self, other: Poly) -> Poly:
        self._check(other)
        combined = dict(self.terms)
        for exponents, coefficient in other.terms.items():
            combined[exponents] = (
                combined[exponents] + coefficient if exponents in combined else coefficient
            )
        return Poly.from_terms(self.field, self.arity, combined)

    def __neg__(self) -> Poly:
        return Poly(
            self.field,
            self.arity,
            {exponents: -value for exponents, value in self.terms.items()},
        )

    def __sub__(self, other: Poly) -> Poly:
        return self + (-other)

    def __mul__(self, other: Poly) -> Poly:
        self._check(other)
        product: dict[Exponents, FieldElement] = {}
        for left_exponents, left in self.terms.items():
            for right_exponents, right in other.terms.items():
                key = tuple(a + b for a, b in zip(left_exponents, right_exponents, strict=True))
                value = left * right
                product[key] = product[key] + value if key in product else value
        return Poly.from_terms(self.field, self.arity, product)

    def scale(self, factor: FieldElement) -> Poly:
        """Multiply by one field element, which is the row scaling the binding needs."""
        return Poly.from_terms(
            self.field,
            self.arity,
            {exponents: value * factor for exponents, value in self.terms.items()},
        )

    def __eq__(self, other: object) -> bool:
        """Exact equality of the normal form, decided by `FieldElement.is_zero`."""
        if not isinstance(other, Poly):
            return NotImplemented
        if other.field is not self.field or other.arity != self.arity:
            return False
        return (self - other).is_zero()

    def __hash__(self) -> int:  # pragma: no cover - polynomials are not keys here
        raise TypeError("Poly is not hashable")

    # -- calculus and evaluation -------------------------------------------

    def evaluate(self, point: Sequence[FieldElement]) -> FieldElement:
        """Exact value at one chart point."""
        if len(point) != self.arity:
            raise ArityError(f"point has {len(point)} coordinates, not {self.arity}")
        total = self.field.zero
        for exponents, coefficient in self.terms.items():
            term = coefficient
            for index, power in enumerate(exponents):
                if power:
                    term = term * (point[index] ** power)
            total = total + term
        return total

    def derivative(self, index: int) -> Poly:
        """Exact partial derivative in one chart variable."""
        if not 0 <= index < self.arity:
            raise IndexError(f"variable {index} is outside 0..{self.arity - 1}")
        derived: dict[Exponents, FieldElement] = {}
        for exponents, coefficient in self.terms.items():
            power = exponents[index]
            if not power:
                continue
            key = tuple(
                value - 1 if position == index else value
                for position, value in enumerate(exponents)
            )
            value = coefficient * self.field.rational(power)
            derived[key] = derived[key] + value if key in derived else value
        return Poly.from_terms(self.field, self.arity, derived)

    def gradient(self) -> list[FieldElement]:
        """The exact gradient at the chart origin, one entry per variable.

        Evaluated at the origin rather than returned as polynomials because that is what
        binds to `T-012`: the constraint rows are the first-order data *at the pose*.
        """
        origin = [self.field.zero] * self.arity
        return [self.derivative(index).evaluate(origin) for index in range(self.arity)]

    def restrict_to_line(self, direction: Sequence[FieldElement]) -> list[FieldElement]:
        """Coefficients of `t -> self(t * direction)`, ascending in `t`.

        The chart origin is the pose, so this is the exact jet of the constraint along a
        straight chart ray. Entry `d` is the coefficient of `t**d`; the second derivative
        at `t = 0` is twice entry two, which is the convention `T-012`'s `q` uses.
        """
        if len(direction) != self.arity:
            raise ArityError(f"direction has {len(direction)} entries, not {self.arity}")
        by_degree: dict[int, FieldElement] = {}
        for exponents, coefficient in self.terms.items():
            term = coefficient
            for index, power in enumerate(exponents):
                if power:
                    term = term * (direction[index] ** power)
            total_degree = sum(exponents)
            by_degree[total_degree] = (
                by_degree[total_degree] + term if total_degree in by_degree else term
            )
        if not by_degree:
            return []
        highest = max(by_degree)
        return [by_degree.get(degree, self.field.zero) for degree in range(highest + 1)]

    def second_derivative_along(self, direction: Sequence[FieldElement]) -> FieldElement:
        """`d^2/dt^2` of `t -> self(t * direction)` at `t = 0`, exactly."""
        jet = self.restrict_to_line(direction)
        if len(jet) < 3:
            return self.field.zero
        return jet[2] * self.field.rational(2)

    def text(self) -> str:
        """Deterministic serialisation, sorted by exponent tuple.

        Byte-stable across runs and across `-O`, because the ordering is on integer
        tuples and the coefficients print through `FieldElement.text`.
        """
        parts = [
            f"{'*'.join(str(power) for power in exponents)}:{value.text()}"
            for exponents, value in sorted(self.terms.items())
        ]
        return "poly{" + ";".join(parts) + "}"


def dot(left: Sequence[Poly], right: Sequence[Poly]) -> Poly:
    """Exact inner product of two equal-length vectors of polynomials."""
    if len(left) != len(right):
        raise ArityError(f"vectors have lengths {len(left)} and {len(right)}")
    if not left:
        raise ArityError("inner product of empty vectors is not defined here")
    total = left[0] * right[0]
    for a, b in zip(left[1:], right[1:], strict=True):
        total = total + a * b
    return total


def as_polynomials(
    field: NumberField, arity: int, values: Iterable[FieldElement]
) -> list[Poly]:
    """Lift field constants into constant polynomials of the chart's arity."""
    return [Poly.constant(field, arity, value) for value in values]


def jets_agree(left: Sequence[FieldElement], right: Sequence[FieldElement]) -> bool:
    """Exactly: do two jets agree coefficient by coefficient, padding with zeros?"""
    for a, b in zip_longest(left, right):
        if a is None:
            if b is not None and not b.is_zero():
                return False
        elif b is None:
            if not a.is_zero():
                return False
        elif not (a - b).is_zero():
            return False
    return True
