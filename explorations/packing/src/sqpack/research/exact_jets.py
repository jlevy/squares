"""Case-free exact second-order jets for packing constraint features.

A jet stores the value, gradient, and symmetric Hessian of one scalar expression at
one base point.  Every coefficient belongs to the same :class:`NumberField`; no
floating-point values or implicit absolute-value branch choices enter this module.

These fixed-feature jets do not enumerate branches or feasible subsequences, route
scales other than ``t**2``, or prove an obstruction.  Those obligations remain with
the caller.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Self

from sqpack.field import FieldElement

type JetVector = tuple[SecondOrderJet, ...]


def _require_sign(sign: int, label: str) -> None:
    if sign not in (-1, 1):
        raise ValueError(f"{label} must be exactly -1 or +1")


def _require_same_field(reference: FieldElement, value: FieldElement, label: str) -> None:
    if value.field is not reference.field:
        raise ValueError(f"{label} comes from a different number field")


@dataclass(frozen=True)
class Taylor2:
    """Exact coefficients of ``value + linear*t + quadratic*t**2``."""

    value: FieldElement
    linear: FieldElement
    quadratic: FieldElement

    def __post_init__(self) -> None:
        _require_same_field(self.value, self.linear, "linear coefficient")
        _require_same_field(self.value, self.quadratic, "quadratic coefficient")


@dataclass(frozen=True)
class SecondOrderJet:
    """A scalar value with its exact gradient and symmetric Hessian."""

    value: FieldElement
    gradient: tuple[FieldElement, ...]
    hessian: tuple[tuple[FieldElement, ...], ...]

    def __post_init__(self) -> None:
        dimension = len(self.gradient)
        if len(self.hessian) != dimension:
            raise ValueError("Hessian row count must equal the gradient dimension")
        for index, component in enumerate(self.gradient):
            _require_same_field(self.value, component, f"gradient[{index}]")
        for row_index, row in enumerate(self.hessian):
            if len(row) != dimension:
                raise ValueError("every Hessian row must equal the gradient dimension")
            for column_index, component in enumerate(row):
                _require_same_field(
                    self.value,
                    component,
                    f"hessian[{row_index}][{column_index}]",
                )
        for row_index in range(dimension):
            for column_index in range(row_index):
                if (
                    self.hessian[row_index][column_index]
                    != self.hessian[column_index][row_index]
                ):
                    raise ValueError("Hessian must be symmetric")

    @property
    def dimension(self) -> int:
        """Number of independent coordinates differentiated by this jet."""
        return len(self.gradient)

    @classmethod
    def constant(cls, value: FieldElement, dimension: int) -> Self:
        """Construct a constant scalar jet in ``dimension`` coordinates."""
        if dimension < 0:
            raise ValueError("dimension must be nonnegative")
        zero = value.field.zero
        return cls(
            value,
            tuple(zero for _ in range(dimension)),
            tuple(tuple(zero for _ in range(dimension)) for _ in range(dimension)),
        )

    @classmethod
    def variable(cls, value: FieldElement, dimension: int, index: int) -> Self:
        """Construct coordinate ``index`` with the supplied base-point value."""
        if not 0 <= index < dimension:
            raise ValueError("variable index must lie within the jet dimension")
        zero = value.field.zero
        one = value.field.one
        gradient = tuple(
            one if coordinate == index else zero for coordinate in range(dimension)
        )
        return cls(
            value,
            gradient,
            tuple(tuple(zero for _ in range(dimension)) for _ in range(dimension)),
        )

    @classmethod
    def rotation(
        cls,
        vector: tuple[FieldElement, FieldElement],
        angle_increment: SecondOrderJet,
    ) -> tuple[SecondOrderJet, SecondOrderJet]:
        """Rotate an exact planar vector by an angle-increment jet based at zero."""
        if not angle_increment.value.is_zero():
            raise ValueError("rotation angle increment must have base value zero")
        for index, component in enumerate(vector):
            _require_same_field(angle_increment.value, component, f"vector[{index}]")
        one = angle_increment.value.field.one
        half = angle_increment.value.field.rational(1) / 2
        cosine = cls.constant(one, angle_increment.dimension) - angle_increment.product(
            angle_increment
        ).scale(half)
        sine = angle_increment
        first = cosine.scale(vector[0]) - sine.scale(vector[1])
        second = sine.scale(vector[0]) + cosine.scale(vector[1])
        return first, second

    def _require_compatible(self, other: SecondOrderJet) -> None:
        if self.dimension != other.dimension:
            raise ValueError("jets have different dimensions")
        _require_same_field(self.value, other.value, "jet")

    def add(self, other: SecondOrderJet) -> SecondOrderJet:
        """Add two compatible jets coefficient by coefficient."""
        self._require_compatible(other)
        return SecondOrderJet(
            self.value + other.value,
            tuple(
                left + right for left, right in zip(self.gradient, other.gradient, strict=True)
            ),
            tuple(
                tuple(left + right for left, right in zip(left_row, right_row, strict=True))
                for left_row, right_row in zip(self.hessian, other.hessian, strict=True)
            ),
        )

    def subtract(self, other: SecondOrderJet) -> SecondOrderJet:
        """Subtract one compatible jet from another."""
        return self.add(-other)

    def negate(self) -> SecondOrderJet:
        """Negate every coefficient of this jet."""
        return SecondOrderJet(
            -self.value,
            tuple(-component for component in self.gradient),
            tuple(tuple(-component for component in row) for row in self.hessian),
        )

    def scale(self, scalar: FieldElement) -> SecondOrderJet:
        """Multiply every coefficient by an exact scalar from the same field."""
        _require_same_field(self.value, scalar, "scale")
        return SecondOrderJet(
            scalar * self.value,
            tuple(scalar * component for component in self.gradient),
            tuple(tuple(scalar * component for component in row) for row in self.hessian),
        )

    def product(self, other: SecondOrderJet) -> SecondOrderJet:
        """Return the exact order-two product jet."""
        self._require_compatible(other)
        gradient = tuple(
            self.gradient[index] * other.value + self.value * other.gradient[index]
            for index in range(self.dimension)
        )
        hessian = tuple(
            tuple(
                self.hessian[row][column] * other.value
                + self.gradient[row] * other.gradient[column]
                + self.gradient[column] * other.gradient[row]
                + self.value * other.hessian[row][column]
                for column in range(self.dimension)
            )
            for row in range(self.dimension)
        )
        return SecondOrderJet(self.value * other.value, gradient, hessian)

    def substitute(
        self,
        velocity: Sequence[FieldElement],
        acceleration: Sequence[FieldElement],
    ) -> Taylor2:
        """Substitute ``z=z0+t*velocity+t**2*acceleration`` through order two."""
        if len(velocity) != self.dimension or len(acceleration) != self.dimension:
            raise ValueError("path vectors must equal the jet dimension")
        for index, component in enumerate(velocity):
            _require_same_field(self.value, component, f"velocity[{index}]")
        for index, component in enumerate(acceleration):
            _require_same_field(self.value, component, f"acceleration[{index}]")
        zero = self.value.field.zero
        linear = sum(
            (gradient * path for gradient, path in zip(self.gradient, velocity, strict=True)),
            zero,
        )
        correction = sum(
            (
                gradient * path
                for gradient, path in zip(self.gradient, acceleration, strict=True)
            ),
            zero,
        )
        curvature = sum(
            (
                velocity[row] * self.hessian[row][column] * velocity[column]
                for row in range(self.dimension)
                for column in range(self.dimension)
            ),
            zero,
        )
        quadratic = correction + curvature / 2
        return Taylor2(self.value, linear, quadratic)

    def __add__(self, other: SecondOrderJet) -> SecondOrderJet:
        return self.add(other)

    def __sub__(self, other: SecondOrderJet) -> SecondOrderJet:
        return self.subtract(other)

    def __neg__(self) -> SecondOrderJet:
        return self.negate()

    def __mul__(self, other: SecondOrderJet) -> SecondOrderJet:
        return self.product(other)


def _dot(left: Sequence[SecondOrderJet], right: Sequence[SecondOrderJet]) -> SecondOrderJet:
    if len(left) != len(right) or not left:
        raise ValueError("dot-product vectors must have the same positive dimension")
    return linear_combination(
        tuple(left[index].value.field.one for index in range(len(left))),
        tuple(left[index].product(right[index]) for index in range(len(left))),
    )


def signed_support(
    axis: Sequence[SecondOrderJet],
    generators: Sequence[Sequence[SecondOrderJet]],
    feature_signs: Sequence[int],
) -> SecondOrderJet:
    """Support of a unit square frame for caller-supplied absolute-feature signs."""
    if len(generators) != len(feature_signs) or not generators:
        raise ValueError("every support generator needs one explicit feature sign")
    for index, sign in enumerate(feature_signs):
        _require_sign(sign, f"feature_signs[{index}]")
    projections = tuple(_dot(axis, generator) for generator in generators)
    for index, (projection, sign) in enumerate(zip(projections, feature_signs, strict=True)):
        base_sign = projection.value.sign()
        if base_sign not in (0, sign):
            raise ValueError(
                f"feature_signs[{index}] disagrees with its nonzero base projection"
            )
    field = projections[0].value.field
    half = field.rational(1) / 2
    weights = tuple(field.rational(sign) * half for sign in feature_signs)
    return linear_combination(weights, projections)


def wall_gap(
    offset: SecondOrderJet,
    normal: Sequence[SecondOrderJet],
    center: Sequence[SecondOrderJet],
    generators: Sequence[Sequence[SecondOrderJet]],
    feature_signs: Sequence[int],
) -> SecondOrderJet:
    """Gap to an outward-normal wall: ``offset-normal·center-support``."""
    return offset - _dot(normal, center) - signed_support(normal, generators, feature_signs)


def sat_gap(
    axis: Sequence[SecondOrderJet],
    *,
    first_center: Sequence[SecondOrderJet],
    second_center: Sequence[SecondOrderJet],
    first_generators: Sequence[Sequence[SecondOrderJet]],
    second_generators: Sequence[Sequence[SecondOrderJet]],
    separation_sign: int,
    first_feature_signs: Sequence[int],
    second_feature_signs: Sequence[int],
) -> SecondOrderJet:
    """Signed separating-axis gap with every absolute-value branch explicit."""
    _require_sign(separation_sign, "separation_sign")
    if len(first_center) != len(second_center) or not first_center:
        raise ValueError("center vectors must have the same positive dimension")
    displacement = tuple(
        second - first for first, second in zip(first_center, second_center, strict=True)
    )
    separation_projection = _dot(axis, displacement)
    base_sign = separation_projection.value.sign()
    if base_sign not in (0, separation_sign):
        raise ValueError("separation_sign disagrees with the nonzero base separation")
    separation = separation_projection.scale(
        separation_projection.value.field.rational(separation_sign)
    )
    return (
        separation
        - signed_support(axis, first_generators, first_feature_signs)
        - signed_support(axis, second_generators, second_feature_signs)
    )


def linear_combination(
    weights: Sequence[FieldElement],
    jets: Sequence[SecondOrderJet],
) -> SecondOrderJet:
    """Return a nonempty exact weighted sum of compatible scalar jets."""
    if len(weights) != len(jets) or not jets:
        raise ValueError("a linear combination needs equally many weights and jets")
    result = jets[0].scale(weights[0])
    for weight, jet in zip(weights[1:], jets[1:], strict=True):
        result = result + jet.scale(weight)
    return result
