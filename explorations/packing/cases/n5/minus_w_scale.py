"""Retain exact owner-3 scale proof data for the n=5 obstruction instrument.

This module routes the five preregistered scale regimes through the accepted production
stress. It returns proof data only: no route is called obstructed or feasible, and no
H-023 or pure ``-W`` disposition is made here.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from enum import StrEnum

from cases.n5 import minus_w_row_jets, minus_w_stress, tangent_cones, tangent_inventory
from sqpack.field import FieldElement, NumberField
from sqpack.research.exact_jets import SecondOrderJet

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


class RemainderExpression(StrEnum):
    """The closed inventory of normalized remainders."""

    T_SQUARED_OVER_ABS_DELTA = "t^2/abs(delta)->0"
    T_ABS_DELTA_OVER_ABS_DELTA = "t*abs(delta)/abs(delta)->0"
    DELTA_SQUARED_OVER_ABS_DELTA = "delta^2/abs(delta)->0"


class RemainderRule(StrEnum):
    """The exact symbolic reduction used for a zero-limit witness."""

    RECIPROCAL_DIVERGENT_RATIO = "reciprocal_divergent_ratio"
    CANCEL_EVENTUALLY_NONZERO_ABS_DELTA = "cancel_eventually_nonzero_abs_delta"
    ABS_DELTA_FROM_LITTLE_O = "abs_delta_from_little_o"


class ScalePremise(StrEnum):
    """Typed premises that a remainder rule may consume."""

    T_TO_ZERO = "t_to_zero"
    T_EVENTUALLY_POSITIVE = "t_eventually_positive"
    DELTA_LITTLE_O_T = "delta_little_o_t"
    ABS_DELTA_OVER_T_SQUARED_TO_POSITIVE_INFINITY = (
        "abs_delta_over_t_squared_to_positive_infinity"
    )
    DELTA_EVENTUALLY_NONZERO = "delta_eventually_nonzero"
    DELTA_SIGN_STABLE = "delta_sign_stable"


NORMALIZED_REMAINDER_EXPRESSIONS = tuple(RemainderExpression)


@dataclass(frozen=True)
class FormalBoundedAffine:
    """The formal-real bounded polynomial, with beta never sampled in the field."""

    constant: FieldElement
    correction_coefficients: tuple[FieldElement, ...]
    beta_symbol: str
    beta_direction: tuple[FieldElement, ...]
    beta_coefficient: FieldElement


@dataclass(frozen=True)
class UnboundedRoutePremises:
    """Premises declared by one sign-stable unbounded-delta route."""

    t_to_zero: bool
    t_eventually_positive: bool
    delta_little_o_t: bool
    abs_delta_over_t_squared_to_positive_infinity: bool
    delta_eventually_nonzero: bool
    delta_sign_stable: bool
    delta_sign: int


@dataclass(frozen=True)
class AsymptoticLimitWitness:
    """One checked symbolic reduction to a declared zero-limit premise."""

    expression: RemainderExpression
    rule: RemainderRule
    premises: frozenset[ScalePremise]
    delta_sign: int


@dataclass(frozen=True)
class RouteSignEvidence:
    """Production projection and the tied labels selected by either delta sign."""

    projection: SecondOrderJet
    delta_direction: tuple[FieldElement, ...]
    delta_coefficient: FieldElement
    positive_delta_tied_label: str
    negative_delta_tied_label: str


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


@dataclass(frozen=True)
class ScaleRouteSpec:
    """One routing partition, separate from its shared exact proof data."""

    family: str
    beta_sign: int | None
    delta_sign: int | None
    decisive_tied_labels: tuple[str, ...]
    unbounded_premises: UnboundedRoutePremises | None


@dataclass(frozen=True)
class ScaleRecord:
    """One of five scale records for one source stratum."""

    stratum: str
    key: str
    route: ScaleRouteSpec
    route_sign_evidence: RouteSignEvidence
    stress: minus_w_stress.StressEvaluation
    bounded_affine: FormalBoundedAffine
    unbounded_cusp: UnboundedCuspData
    normalized_remainder_limits: tuple[AsymptoticLimitWitness, ...]


type ScaleHandler = Callable[[RouteSignEvidence], ScaleRouteSpec]


def _bounded_negative(evidence: RouteSignEvidence) -> ScaleRouteSpec:
    return ScaleRouteSpec("bounded", -1, None, (evidence.negative_delta_tied_label,), None)


def _bounded_zero(evidence: RouteSignEvidence) -> ScaleRouteSpec:
    return ScaleRouteSpec(
        "bounded",
        0,
        None,
        (evidence.positive_delta_tied_label, evidence.negative_delta_tied_label),
        None,
    )


def _bounded_positive(evidence: RouteSignEvidence) -> ScaleRouteSpec:
    return ScaleRouteSpec("bounded", 1, None, (evidence.positive_delta_tied_label,), None)


def unbounded_route_premises(delta_sign: int) -> UnboundedRoutePremises:
    """Return the closed premise set owned by one unbounded sign route."""
    if delta_sign not in (-1, 1):
        raise ValueError(f"unbounded scale route has invalid delta sign {delta_sign}")
    return UnboundedRoutePremises(
        t_to_zero=True,
        t_eventually_positive=True,
        delta_little_o_t=True,
        abs_delta_over_t_squared_to_positive_infinity=True,
        delta_eventually_nonzero=True,
        delta_sign_stable=True,
        delta_sign=delta_sign,
    )


def _unbounded_negative(evidence: RouteSignEvidence) -> ScaleRouteSpec:
    return ScaleRouteSpec(
        "unbounded",
        None,
        -1,
        (evidence.negative_delta_tied_label,),
        unbounded_route_premises(-1),
    )


def _unbounded_positive(evidence: RouteSignEvidence) -> ScaleRouteSpec:
    return ScaleRouteSpec(
        "unbounded",
        None,
        1,
        (evidence.positive_delta_tied_label,),
        unbounded_route_premises(1),
    )


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


def validated_route_specs(
    handlers: Mapping[str, ScaleHandler], evidence: RouteSignEvidence
) -> Mapping[str, ScaleRouteSpec]:
    """Run every handler and reject semantic drift behind a valid key inventory."""
    selected = _validated_handlers(handlers)
    actual = {key: selected[key](evidence) for key in SCALE_KEYS}
    expected = {
        BOUNDED_BETA_NEGATIVE: _bounded_negative(evidence),
        BOUNDED_BETA_ZERO: _bounded_zero(evidence),
        BOUNDED_BETA_POSITIVE: _bounded_positive(evidence),
        UNBOUNDED_DELTA_NEGATIVE: _unbounded_negative(evidence),
        UNBOUNDED_DELTA_POSITIVE: _unbounded_positive(evidence),
    }
    for key in SCALE_KEYS:
        if actual[key] != expected[key]:
            raise ValueError(f"scale handler semantics drifted; key={key}")
    return actual


def unbounded_remainder_witnesses(
    premises: UnboundedRoutePremises,
    *,
    witness_overrides: Mapping[RemainderExpression, AsymptoticLimitWitness] | None = None,
) -> tuple[AsymptoticLimitWitness, AsymptoticLimitWitness, AsymptoticLimitWitness]:
    """Derive the three normalized zero limits from explicit scale premises."""
    if premises.delta_sign not in (-1, 1):
        raise ValueError(f"unbounded scale route has invalid delta sign {premises.delta_sign}")
    availability = {
        ScalePremise.T_TO_ZERO: premises.t_to_zero,
        ScalePremise.T_EVENTUALLY_POSITIVE: premises.t_eventually_positive,
        ScalePremise.DELTA_LITTLE_O_T: premises.delta_little_o_t,
        ScalePremise.ABS_DELTA_OVER_T_SQUARED_TO_POSITIVE_INFINITY: (
            premises.abs_delta_over_t_squared_to_positive_infinity
        ),
        ScalePremise.DELTA_EVENTUALLY_NONZERO: premises.delta_eventually_nonzero,
        ScalePremise.DELTA_SIGN_STABLE: premises.delta_sign_stable,
    }
    missing = tuple(
        sorted(premise.value for premise, present in availability.items() if not present)
    )
    if missing:
        raise ValueError(f"unbounded scale assumption missing; premises={list(missing)}")
    expected = (
        AsymptoticLimitWitness(
            expression=RemainderExpression.T_SQUARED_OVER_ABS_DELTA,
            rule=RemainderRule.RECIPROCAL_DIVERGENT_RATIO,
            premises=frozenset(
                {
                    ScalePremise.T_EVENTUALLY_POSITIVE,
                    ScalePremise.DELTA_EVENTUALLY_NONZERO,
                    ScalePremise.DELTA_SIGN_STABLE,
                    ScalePremise.ABS_DELTA_OVER_T_SQUARED_TO_POSITIVE_INFINITY,
                }
            ),
            delta_sign=premises.delta_sign,
        ),
        AsymptoticLimitWitness(
            expression=RemainderExpression.T_ABS_DELTA_OVER_ABS_DELTA,
            rule=RemainderRule.CANCEL_EVENTUALLY_NONZERO_ABS_DELTA,
            premises=frozenset(
                {
                    ScalePremise.T_EVENTUALLY_POSITIVE,
                    ScalePremise.DELTA_EVENTUALLY_NONZERO,
                    ScalePremise.DELTA_SIGN_STABLE,
                    ScalePremise.T_TO_ZERO,
                }
            ),
            delta_sign=premises.delta_sign,
        ),
        AsymptoticLimitWitness(
            expression=RemainderExpression.DELTA_SQUARED_OVER_ABS_DELTA,
            rule=RemainderRule.ABS_DELTA_FROM_LITTLE_O,
            premises=frozenset(
                {
                    ScalePremise.T_EVENTUALLY_POSITIVE,
                    ScalePremise.DELTA_EVENTUALLY_NONZERO,
                    ScalePremise.DELTA_SIGN_STABLE,
                    ScalePremise.DELTA_LITTLE_O_T,
                    ScalePremise.T_TO_ZERO,
                }
            ),
            delta_sign=premises.delta_sign,
        ),
    )
    overrides = witness_overrides or {}
    actual = (
        overrides.get(expected[0].expression, expected[0]),
        overrides.get(expected[1].expression, expected[1]),
        overrides.get(expected[2].expression, expected[2]),
    )
    if actual != expected:
        changed = next(
            witness.expression.value
            for witness, wanted in zip(actual, expected, strict=True)
            if witness != wanted
        )
        raise ValueError(f"unbounded remainder witness drifted; expression={changed}")
    return actual


def route_sign_evidence(
    field: NumberField,
    stratum: str,
    stress: minus_w_stress.StressEvaluation,
) -> RouteSignEvidence:
    projection = minus_w_row_jets.owner3_tied_feature_projection(field, stratum)
    delta_direction = tuple(
        field.one if index == tangent_cones.theta(3) else field.zero
        for index in range(tangent_cones.VARIABLE_COUNT)
    )
    delta_coefficient = sum(
        (
            coefficient * direction
            for coefficient, direction in zip(projection.gradient, delta_direction, strict=True)
        ),
        field.zero,
    )
    if delta_coefficient.sign() == 0:
        raise ValueError("owner-3 tied projection has no strict delta sign")
    if projection.gradient[tangent_cones.theta(4)] != -delta_coefficient or any(
        not coefficient.is_zero()
        for index, coefficient in enumerate(projection.gradient)
        if index not in {tangent_cones.theta(3), tangent_cones.theta(4)}
    ):
        raise ValueError("owner-3 tied projection is not a pure delta covector")
    tied_labels = {row.label for row in stress.rows if row.label.startswith("contact:3-4:")}
    positive_sign = delta_coefficient.sign()
    positive_label = TIED_PLUS_LABEL if positive_sign > 0 else TIED_MINUS_LABEL
    negative_label = TIED_MINUS_LABEL if positive_sign > 0 else TIED_PLUS_LABEL
    if {positive_label, negative_label} != tied_labels:
        raise ValueError("derived route labels drifted from production tied rows")
    return RouteSignEvidence(
        projection=projection,
        delta_direction=delta_direction,
        delta_coefficient=delta_coefficient,
        positive_delta_tied_label=positive_label,
        negative_delta_tied_label=negative_label,
    )


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
    sign_evidence = route_sign_evidence(field, stratum, stress)
    routes = validated_route_specs(selected_handlers, sign_evidence)
    records: list[ScaleRecord] = []
    for key in SCALE_KEYS:
        route = routes[key]
        if route.family == "unbounded":
            premises = route.unbounded_premises
            if premises is None or premises.delta_sign != route.delta_sign:
                raise ValueError(f"unbounded route premises drifted; key={key}")
            limits = unbounded_remainder_witnesses(premises)
        elif route.family == "bounded":
            if route.unbounded_premises is not None:
                raise ValueError(f"bounded route acquired unbounded premises; key={key}")
            limits = ()
        else:
            raise ValueError(f"unknown scale route family; key={key}")
        records.append(
            ScaleRecord(
                stratum=stratum,
                key=key,
                route=route,
                route_sign_evidence=sign_evidence,
                stress=stress,
                bounded_affine=bounded,
                unbounded_cusp=unbounded,
                normalized_remainder_limits=limits,
            )
        )
    return tuple(records)


def positive_w_control_records(
    field: NumberField,
    *,
    handlers: Mapping[str, ScaleHandler] = SCALE_HANDLERS,
) -> tuple[ScaleRecord, ...]:
    """Exercise all fifteen scale records on exp-036's accepted positive-W control."""
    selected_handlers = _validated_handlers(handlers)
    correction = tuple(field.zero for _ in range(tangent_cones.VARIABLE_COUNT))
    records: list[ScaleRecord] = []
    for stratum in tangent_cones.STRATA:
        batch = scale_records(
            field,
            stratum,
            tuple(tangent_inventory.geometry_vectors(field, stratum)[0]["W"]),
            correction,
            handlers=selected_handlers,
        )
        if any(record.bounded_affine.constant.sign() >= 0 for record in batch):
            raise ValueError("positive-W control lost its strict production curvature")
        records.extend(batch)
    expected = {
        (stratum, key) for stratum in tangent_cones.STRATA for key in EXPECTED_SCALE_KEYS
    }
    if {(record.stratum, record.key) for record in records} != expected or len(records) != 15:
        raise ValueError("three-stratum scale record inventory drifted")
    return tuple(records)
