"""Evaluate the exp-034 positive left-boundary path on exact n=5 row jets.

This module is a reusable compatibility control.  It binds one exact source path and
checks its active-row Taylor coefficients, but does not choose stresses, route scales,
or make a tangent-cone or obstruction determination.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from cases.n5 import angle_sheet, minus_w_row_jets, tangent_cones
from sqpack.field import FieldElement, NumberField
from sqpack.research.exact_jets import SecondOrderJet, Taylor2


@dataclass(frozen=True)
class SourceBinding:
    """Exact base data regenerated from the exp-034 rational family."""

    side: FieldElement
    centers: tuple[tuple[FieldElement, FieldElement], ...]
    cosine: FieldElement
    sine: FieldElement


@dataclass(frozen=True)
class SheetPath:
    """Coefficients for ``pose=base+t*velocity+t**2*correction``."""

    velocity: tuple[FieldElement, ...]
    correction: tuple[FieldElement, ...]


@dataclass(frozen=True)
class OwnerEvaluation:
    """All active-row Taylor coefficients for one exact owner inventory."""

    owner: str
    rows: dict[str, Taylor2]
    compatible: bool


@dataclass(frozen=True)
class SheetEvaluation:
    """Lexicographic row compatibility for both A owner inventories."""

    source: SourceBinding
    path: SheetPath
    owners: tuple[OwnerEvaluation, ...]
    compatible: bool


def source_binding(field: NumberField) -> SourceBinding:
    """Regenerate and bind the zero-parameter exp-034 positive left endpoint."""
    q = field.rational
    side, centers, cosine, sine = angle_sheet.parameter_values(
        field, sign=1, endpoint="left", q_abs=Fraction(0)
    )
    expected_centers = tuple(tangent_cones.centres_for_stratum(field, "A"))
    if tuple(centers) != expected_centers:
        raise ValueError("the exp-034 zero-parameter base differs from source stratum A")
    if cosine != q(1) or not sine.is_zero():
        raise ValueError("the exp-034 zero-parameter orientation is not the source pose")
    return SourceBinding(side, tuple(centers), cosine, sine)


def derive_positive_left_boundary_path(
    field: NumberField, *, half_angle_rate: FieldElement
) -> SheetPath:
    """Derive the path from the exp-034 rational formula through exact order two."""
    source = source_binding(field)
    q = field.rational
    time = SecondOrderJet.variable(q(0), 1, 0)
    one = SecondOrderJet.constant(q(1), 1)
    half_angle = time.scale(half_angle_rate)
    half_angle_squared = half_angle.product(half_angle)
    denominator = one + half_angle_squared
    reciprocal = one - half_angle_squared
    if denominator.product(reciprocal) != one:
        raise ValueError("the order-two reciprocal identity failed")

    cosine = (one - half_angle_squared).product(reciprocal)
    sine = half_angle.scale(q(2)).product(reciprocal)
    shrink = half_angle.product(one - half_angle).product(reciprocal)
    physical_angle = half_angle.scale(q(2))
    if cosine.product(cosine) + sine.product(sine) != one:
        raise ValueError("the order-two unit-circle identity failed")

    zero_path = (q(0),)
    unit_path = (q(1),)
    cosine_taylor = cosine.substitute(unit_path, zero_path)
    sine_taylor = sine.substitute(unit_path, zero_path)
    angle_taylor = physical_angle.substitute(unit_path, zero_path)
    if (cosine_taylor.value, sine_taylor.value) != (source.cosine, source.sine):
        raise ValueError("the rational formula base differs from the exp-034 source")
    if angle_taylor != Taylor2(q(0), q(1), q(0)):
        raise ValueError("the half-angle rate does not normalize the physical angle to t")

    center_x = SecondOrderJet.constant(source.centers[0][0], 1) + shrink
    center_y = SecondOrderJet.constant(source.centers[0][1], 1) + shrink
    center_x_taylor = center_x.substitute(unit_path, zero_path)
    center_y_taylor = center_y.substitute(unit_path, zero_path)
    if (center_x_taylor.value, center_y_taylor.value) != source.centers[0]:
        raise ValueError("the rational center formula differs from the exp-034 source")

    velocity = list(tangent_cones.zero_row(field))
    correction = list(tangent_cones.zero_row(field))
    velocity[tangent_cones.x(0)] = center_x_taylor.linear
    velocity[tangent_cones.y(0)] = center_y_taylor.linear
    velocity[tangent_cones.theta(0)] = angle_taylor.linear
    correction[tangent_cones.x(0)] = center_x_taylor.quadratic
    correction[tangent_cones.y(0)] = center_y_taylor.quadratic
    return SheetPath(tuple(velocity), tuple(correction))


def positive_left_boundary_path(field: NumberField) -> SheetPath:
    """Derive the normalized positive sheet path from the rational half-angle formula."""
    return derive_positive_left_boundary_path(field, half_angle_rate=field.rational(1) / 2)


def bad_left_boundary_path(field: NumberField) -> SheetPath:
    """Return the declared incompatible center-correction control path."""
    q = field.rational
    path = positive_left_boundary_path(field)
    correction = list(path.correction)
    correction[tangent_cones.x(0)] = -q(1) / 2
    correction[tangent_cones.y(0)] = -q(1) / 2
    return SheetPath(path.velocity, tuple(correction))


def row_is_lexicographically_compatible(value: Taylor2) -> bool:
    """Check one active gap through the first decisive Taylor coefficient."""
    if not value.value.is_zero():
        raise ValueError("lexicographic compatibility requires an active base row")
    linear_sign = value.linear.sign()
    return linear_sign > 0 or (linear_sign == 0 and value.quadratic.sign() >= 0)


def evaluate_path(field: NumberField, path: SheetPath) -> SheetEvaluation:
    """Evaluate one supplied path through both complete A owner row inventories."""
    source = source_binding(field)
    owners: list[OwnerEvaluation] = []
    for owner in tangent_cones.EXPECTED_CONTACT_BRANCHES:
        jets = minus_w_row_jets.owner_row_jets(field, "A", owner)
        rows = {
            label: jet.substitute(path.velocity, path.correction) for label, jet in jets.items()
        }
        if len(rows) != 17 or any(not value.value.is_zero() for value in rows.values()):
            raise ValueError("the exp-034 sheet evaluator lost its complete active row set")
        compatible = all(row_is_lexicographically_compatible(value) for value in rows.values())
        owners.append(OwnerEvaluation(owner, rows, compatible))
    return SheetEvaluation(
        source=source,
        path=path,
        owners=tuple(owners),
        compatible=all(owner.compatible for owner in owners),
    )
