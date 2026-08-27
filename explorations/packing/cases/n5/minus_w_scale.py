"""Retain exact owner-3 scale proof data for the n=5 obstruction instrument.

This module routes the five preregistered scale regimes through the accepted production
stress. It returns proof data only: no route is called obstructed or feasible, and no
H-023 or pure ``-W`` disposition is made here.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass

from cases.n5 import minus_w_stress, tangent_cones, tangent_inventory
from sqpack.field import FieldElement, NumberField

OWNER3 = "owner3:a+"
BOUNDED_BETA_NEGATIVE = "bounded_beta_negative"
BOUNDED_BETA_ZERO = "bounded_beta_zero"
BOUNDED_BETA_POSITIVE = "bounded_beta_positive"
UNBOUNDED_DELTA_NEGATIVE = "unbounded_delta_negative"
UNBOUNDED_DELTA_POSITIVE = "unbounded_delta_positive"
SCALE_KEYS = (
    BOUNDED_BETA_NEGATIVE,
    BOUNDED_BETA_ZERO,
    BOUNDED_BETA_POSITIVE,
    UNBOUNDED_DELTA_NEGATIVE,
    UNBOUNDED_DELTA_POSITIVE,
)
EXPECTED_SCALE_KEYS = frozenset(SCALE_KEYS)
TIED_PLUS_LABEL = "contact:3-4:owner3:a+:square4-feature+1"
TIED_MINUS_LABEL = "contact:3-4:owner3:a+:square4-feature-1"
NORMALIZED_REMAINDER_LIMITS = (
    "t^2/abs(delta)->0",
    "t*abs(delta)/abs(delta)->0",
    "delta^2/abs(delta)->0",
)


@dataclass(frozen=True)
class FormalBoundedAffine:
    """The formal-real bounded polynomial, with beta never sampled in the field."""

    constant: FieldElement
    correction_coefficients: tuple[FieldElement, ...]
    beta_symbol: str
    beta_direction: tuple[FieldElement, ...]
    beta_coefficient: FieldElement


@dataclass(frozen=True)
class UnboundedCuspData:
    """Source-derived cusp coefficients and normalized remainder obligations."""

    transverse_projection: FieldElement
    tied_labels: tuple[str, str]
    tied_gradients: tuple[tuple[FieldElement, ...], tuple[FieldElement, ...]]
    b_plus: FieldElement
    b_minus: FieldElement
    h: FieldElement
    kappa_positive: FieldElement
    kappa_negative: FieldElement
    nuisance_coefficients: tuple[FieldElement, ...]
    normalized_remainder_limits: tuple[str, str, str]


@dataclass(frozen=True)
class ScaleRouteSpec:
    """One routing partition, separate from its shared exact proof data."""

    family: str
    beta_sign: int | None
    delta_sign: int | None
    decisive_tied_labels: tuple[str, ...]


@dataclass(frozen=True)
class ScaleRecord:
    """One of five scale records for one source stratum."""

    stratum: str
    key: str
    route: ScaleRouteSpec
    stress: minus_w_stress.StressEvaluation
    bounded_affine: FormalBoundedAffine
    unbounded_cusp: UnboundedCuspData


type ScaleHandler = Callable[[], ScaleRouteSpec]


def _bounded_negative() -> ScaleRouteSpec:
    return ScaleRouteSpec("bounded", -1, None, (TIED_MINUS_LABEL,))


def _bounded_zero() -> ScaleRouteSpec:
    return ScaleRouteSpec("bounded", 0, None, (TIED_PLUS_LABEL, TIED_MINUS_LABEL))


def _bounded_positive() -> ScaleRouteSpec:
    return ScaleRouteSpec("bounded", 1, None, (TIED_PLUS_LABEL,))


def _unbounded_negative() -> ScaleRouteSpec:
    return ScaleRouteSpec("unbounded", None, -1, (TIED_MINUS_LABEL,))


def _unbounded_positive() -> ScaleRouteSpec:
    return ScaleRouteSpec("unbounded", None, 1, (TIED_PLUS_LABEL,))


SCALE_HANDLERS: Mapping[str, ScaleHandler] = {
    BOUNDED_BETA_NEGATIVE: _bounded_negative,
    BOUNDED_BETA_ZERO: _bounded_zero,
    BOUNDED_BETA_POSITIVE: _bounded_positive,
    UNBOUNDED_DELTA_NEGATIVE: _unbounded_negative,
    UNBOUNDED_DELTA_POSITIVE: _unbounded_positive,
}


def _validated_handlers(handlers: Mapping[str, ScaleHandler]) -> Mapping[str, ScaleHandler]:
    actual = set(handlers)
    if actual != EXPECTED_SCALE_KEYS:
        missing = sorted(EXPECTED_SCALE_KEYS - actual)
        extra = sorted(actual - EXPECTED_SCALE_KEYS)
        raise ValueError(f"scale handler inventory drifted; missing={missing}, extra={extra}")
    return handlers


def _bounded_affine(
    field: NumberField, stress: minus_w_stress.StressEvaluation
) -> FormalBoundedAffine:
    coefficients = stress.combined_jet.gradient
    beta_direction = tuple(
        field.one if index == tangent_cones.theta(3) else field.zero
        for index in range(tangent_cones.VARIABLE_COUNT)
    )
    beta_coefficient = sum(
        (
            coefficient * direction
            for coefficient, direction in zip(coefficients, beta_direction, strict=True)
        ),
        field.zero,
    )
    if len(coefficients) != tangent_cones.VARIABLE_COUNT:
        raise ValueError("bounded affine correction inventory drifted")
    if any(not coefficient.is_zero() for coefficient in coefficients):
        raise ValueError("bounded affine correction coefficient did not cancel")
    if not beta_coefficient.is_zero():
        raise ValueError("formal beta coefficient did not cancel")
    return FormalBoundedAffine(
        constant=stress.total_weighted_curvature,
        correction_coefficients=coefficients,
        beta_symbol="beta",
        beta_direction=beta_direction,
        beta_coefficient=beta_coefficient,
    )


def _unbounded_cusp(
    field: NumberField, stress: minus_w_stress.StressEvaluation
) -> UnboundedCuspData:
    tied = {row.label: row for row in stress.rows if row.label.startswith("contact:3-4:")}
    if set(tied) != {TIED_PLUS_LABEL, TIED_MINUS_LABEL}:
        raise ValueError("owner-3 tied-row inventory drifted")
    plus = tied[TIED_PLUS_LABEL]
    minus = tied[TIED_MINUS_LABEL]
    b_plus = plus.jet.gradient[tangent_cones.theta(3)]
    b_minus = minus.jet.gradient[tangent_cones.theta(3)]
    h = (b_minus - b_plus) / 2
    tau = stress.transverse_projection
    kappa_positive = b_plus
    kappa_negative = -b_minus
    if b_plus != -(h + tau) or -b_minus != -(h - tau):
        raise ValueError("source-derived cusp identity drifted")
    if kappa_positive.sign() >= 0 or kappa_negative.sign() >= 0:
        raise ValueError("source-derived cusp coefficient is not strictly negative")
    nuisance = stress.combined_jet.gradient
    if any(not coefficient.is_zero() for coefficient in nuisance):
        raise ValueError("unbounded nuisance coefficient did not cancel")
    return UnboundedCuspData(
        transverse_projection=tau,
        tied_labels=(TIED_PLUS_LABEL, TIED_MINUS_LABEL),
        tied_gradients=(plus.jet.gradient, minus.jet.gradient),
        b_plus=b_plus,
        b_minus=b_minus,
        h=h,
        kappa_positive=kappa_positive,
        kappa_negative=kappa_negative,
        nuisance_coefficients=nuisance,
        normalized_remainder_limits=NORMALIZED_REMAINDER_LIMITS,
    )


def scale_records(
    field: NumberField,
    stratum: str,
    velocity: Sequence[FieldElement],
    correction: Sequence[FieldElement],
    *,
    handlers: Mapping[str, ScaleHandler] = SCALE_HANDLERS,
) -> tuple[ScaleRecord, ...]:
    """Build the exact five-route owner-3 record for one registered stratum."""
    selected_handlers = _validated_handlers(handlers)
    if stratum not in tangent_cones.STRATA:
        raise ValueError(f"unknown source stratum {stratum}")
    stress = minus_w_stress.evaluate_stress(field, stratum, OWNER3, velocity, correction)
    bounded = _bounded_affine(field, stress)
    unbounded = _unbounded_cusp(field, stress)
    return tuple(
        ScaleRecord(
            stratum=stratum,
            key=key,
            route=selected_handlers[key](),
            stress=stress,
            bounded_affine=bounded,
            unbounded_cusp=unbounded,
        )
        for key in SCALE_KEYS
    )


def positive_w_control_records(
    field: NumberField,
    *,
    handlers: Mapping[str, ScaleHandler] = SCALE_HANDLERS,
) -> tuple[ScaleRecord, ...]:
    """Exercise all fifteen scale records on exp-036's accepted positive-W control."""
    selected_handlers = _validated_handlers(handlers)
    correction = tuple(field.zero for _ in range(tangent_cones.VARIABLE_COUNT))
    records = tuple(
        record
        for stratum in tangent_cones.STRATA
        for record in scale_records(
            field,
            stratum,
            tuple(tangent_inventory.geometry_vectors(field, stratum)[0]["W"]),
            correction,
            handlers=selected_handlers,
        )
    )
    expected = {
        (stratum, key) for stratum in tangent_cones.STRATA for key in EXPECTED_SCALE_KEYS
    }
    if {(record.stratum, record.key) for record in records} != expected or len(records) != 15:
        raise ValueError("three-stratum scale record inventory drifted")
    if any(record.bounded_affine.constant.sign() >= 0 for record in records):
        raise ValueError("positive-W control lost its strict production curvature")
    return records
