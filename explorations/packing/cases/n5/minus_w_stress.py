"""Evaluate the exact weighted nine-row stress for n=5 source poses.

The evaluator derives weights from source geometry and retains rowwise and combined
Taylor data.  It does not choose a direction, route relative-angle scales, compare
signs, or decide whether any curvature is an obstruction.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from cases.n5 import minus_w_row_jets, tangent_cones
from sqpack.field import FieldElement, NumberField
from sqpack.research.exact_jets import (
    SecondOrderJet,
    Taylor2,
    linear_combination,
)

COMMON_STRESS_LABELS = frozenset(
    {
        "wall:2:x-lower:+",
        "wall:2:x-lower:-",
        "wall:2:y-lower:+",
        "wall:2:y-lower:-",
        "wall:3:x-upper",
        "wall:3:y-upper",
        "contact:2-4:owner4:a+",
    }
)


@dataclass(frozen=True)
class WeightedRowEvaluation:
    """One production row and its exact path and weighted-curvature data."""

    label: str
    jet: SecondOrderJet
    weight: FieldElement
    taylor: Taylor2
    correction_coefficients: tuple[FieldElement, ...]
    velocity_curvature: FieldElement
    weighted_curvature: FieldElement


@dataclass(frozen=True)
class StressEvaluation:
    """The validated nine-row stress evaluation, without scientific disposition."""

    stratum: str
    owner: str
    transverse_projection: FieldElement
    rows: tuple[WeightedRowEvaluation, ...]
    combined_jet: SecondOrderJet
    combined_taylor: Taylor2
    total_weighted_curvature: FieldElement


def _transverse_projection(field: NumberField, stratum: str) -> FieldElement:
    centers = tangent_cones.centres_for_stratum(field, stratum)
    p2 = centers[2]
    p4 = centers[4]
    perpendicular = (-field.alpha / 2, field.alpha / 2)
    displacement = (p4[0] - p2[0], p4[1] - p2[1])
    return displacement[0] * perpendicular[0] + displacement[1] * perpendicular[1]


def _expected_labels(owner: str) -> frozenset[str]:
    tied_square = 4 if owner == "owner3:a+" else 3
    return COMMON_STRESS_LABELS | {
        f"contact:3-4:{owner}:square{tied_square}-feature+1",
        f"contact:3-4:{owner}:square{tied_square}-feature-1",
    }


def _production_weights(
    field: NumberField,
    owner: str,
    labels: Sequence[str],
    transverse: FieldElement,
) -> dict[str, FieldElement]:
    q = field.rational
    weights: dict[str, FieldElement] = {}
    for label in labels:
        if label.startswith("wall:2:"):
            weight = field.alpha / 4
        elif label.startswith("wall:3:"):
            weight = field.alpha / 2
        elif label == "contact:2-4:owner4:a+":
            weight = q(1)
        elif owner == "owner4:a+":
            weight = q(1) / 2
        elif label.endswith("feature+1"):
            weight = q(1) / 2 - transverse
        else:
            weight = q(1) / 2 + transverse
        weights[label] = weight
    return weights


def _validate_weight_contract(
    field: NumberField,
    owner: str,
    weights: Mapping[str, FieldElement],
    transverse: FieldElement,
) -> None:
    q = field.rational
    wall2 = {label for label in weights if label.startswith("wall:2:")}
    wall3 = {label for label in weights if label.startswith("wall:3:")}
    tied = {label for label in weights if label.startswith("contact:3-4:")}
    valid = (
        weights["contact:2-4:owner4:a+"] == q(1)
        and len(wall2) == 4
        and all(weights[label] == field.alpha / 4 for label in wall2)
        and len(wall3) == 2
        and all(weights[label] == field.alpha / 2 for label in wall3)
        and sum((weights[label] for label in wall3), field.zero) == field.alpha
        and len(tied) == 2
    )
    if owner == "owner4:a+":
        valid = valid and all(weights[label] == q(1) / 2 for label in tied)
    else:
        valid = valid and all(
            weights[label]
            == (q(1) / 2 - transverse if label.endswith("feature+1") else q(1) / 2 + transverse)
            for label in tied
        )
    if not valid:
        raise ValueError("stress weight normalization or source identity drifted")


def evaluate_stress(
    field: NumberField,
    stratum: str,
    owner: str,
    velocity: Sequence[FieldElement],
    correction: Sequence[FieldElement],
    *,
    weight_adjustments: Mapping[str, FieldElement] | None = None,
) -> StressEvaluation:
    """Evaluate and validate the source-derived positive nine-row stress."""
    owner_rows = minus_w_row_jets.owner_row_jets(field, stratum, owner)
    expected = _expected_labels(owner)
    selected = {label: jet for label, jet in owner_rows.items() if label in expected}
    if set(selected) != expected or len(selected) != 9:
        missing = sorted(expected - selected.keys())
        extra = sorted(selected.keys() - expected)
        raise ValueError(f"stress row inventory drifted; missing={missing}, extra={extra}")

    transverse = _transverse_projection(field, stratum)
    weights = _production_weights(field, owner, tuple(selected), transverse)
    for label, adjustment in (weight_adjustments or {}).items():
        if label not in weights:
            raise ValueError(f"weight adjustment names a non-stress row {label}")
        if adjustment.field is not field:
            raise ValueError("weight adjustment comes from a different number field")
        weights[label] = weights[label] + adjustment
    if any(weight.sign() <= 0 for weight in weights.values()):
        raise ValueError("every stress weight must remain exactly positive")

    zero_correction = tuple(field.zero for _ in range(tangent_cones.VARIABLE_COUNT))
    evaluated_rows = tuple(
        WeightedRowEvaluation(
            label=label,
            jet=jet,
            weight=weights[label],
            taylor=jet.substitute(velocity, correction),
            correction_coefficients=jet.gradient,
            velocity_curvature=jet.substitute(velocity, zero_correction).quadratic,
            weighted_curvature=(
                weights[label] * jet.substitute(velocity, zero_correction).quadratic
            ),
        )
        for label, jet in selected.items()
    )
    combined_jet = linear_combination(
        tuple(row.weight for row in evaluated_rows),
        tuple(row.jet for row in evaluated_rows),
    )
    if any(not coefficient.is_zero() for coefficient in combined_jet.gradient):
        raise ValueError("combined stress gradient does not cancel")
    _validate_weight_contract(field, owner, weights, transverse)
    combined_taylor = combined_jet.substitute(velocity, correction)
    total_weighted_curvature = sum(
        (row.weighted_curvature for row in evaluated_rows), field.zero
    )
    combined_velocity_curvature = combined_jet.substitute(velocity, zero_correction).quadratic
    if combined_velocity_curvature != total_weighted_curvature:
        raise ValueError("combined curvature differs from weighted row curvatures")
    if combined_taylor.quadratic != total_weighted_curvature:
        raise ValueError("a quadratic correction survived the cancelled stress")
    return StressEvaluation(
        stratum=stratum,
        owner=owner,
        transverse_projection=transverse,
        rows=evaluated_rows,
        combined_jet=combined_jet,
        combined_taylor=combined_taylor,
        total_weighted_curvature=total_weighted_curvature,
    )
