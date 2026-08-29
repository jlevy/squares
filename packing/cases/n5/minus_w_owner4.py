"""Retain target-free owner-4 proof data for the n=5 obstruction instrument.

This module exhausts the three registered source strata through the accepted production
stress on the positive-W control. It returns proof data only: no pure ``-W`` target,
obstruction, feasibility, or H-023 disposition is constructed here.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from cases.n5 import minus_w_row_jets, minus_w_stress, tangent_cones, tangent_inventory
from sqpack.field import FieldElement, NumberField
from sqpack.research.exact_jets import SecondOrderJet

OWNER4 = "owner4:a+"
EXPECTED_TIED_LABELS = frozenset(
    {
        "contact:3-4:owner4:a+:square3-feature+1",
        "contact:3-4:owner4:a+:square3-feature-1",
    }
)


@dataclass(frozen=True)
class Owner4Record:
    """Exact owner-4 stress and its retained correction cancellation."""

    stratum: str
    velocity: tuple[FieldElement, ...]
    correction: tuple[FieldElement, ...]
    stress: minus_w_stress.StressEvaluation
    correction_coefficients: tuple[FieldElement, ...]
    constant: FieldElement


def owner4_record(
    field: NumberField,
    stratum: str,
    velocity: Sequence[FieldElement],
    correction: Sequence[FieldElement],
    *,
    active_rows: Mapping[str, SecondOrderJet] | None = None,
) -> Owner4Record:
    """Build one source-derived owner-4 record without assigning an outcome."""
    if stratum not in tangent_cones.STRATA:
        raise ValueError(f"unknown source stratum {stratum}")
    retained_velocity = tuple(velocity)
    retained_correction = tuple(correction)
    stress = minus_w_stress.evaluate_stress(
        field,
        stratum,
        OWNER4,
        retained_velocity,
        retained_correction,
        active_rows=active_rows,
    )
    if stress.owner != "owner4:a+":
        raise ValueError("owner-4 production branch drifted")
    tied_labels = {row.label for row in stress.rows if row.label.startswith("contact:3-4:")}
    if tied_labels != EXPECTED_TIED_LABELS:
        raise ValueError("owner-4 tied-row inventory drifted")
    if any(
        not row.taylor.value.is_zero() or not row.taylor.linear.is_zero() for row in stress.rows
    ):
        raise ValueError("owner-4 source path is not first-order tight")
    coefficients = stress.combined_jet.gradient
    if len(coefficients) != tangent_cones.VARIABLE_COUNT:
        raise ValueError("owner-4 correction inventory drifted")
    if any(not coefficient.is_zero() for coefficient in coefficients):
        raise ValueError("owner-4 correction coefficient did not cancel")
    constant = stress.total_weighted_curvature
    if stress.combined_taylor.quadratic != constant:
        raise ValueError("owner-4 stress constant drifted from production curvature")
    return Owner4Record(
        stratum=stratum,
        velocity=retained_velocity,
        correction=retained_correction,
        stress=stress,
        correction_coefficients=coefficients,
        constant=constant,
    )


def positive_w_control_records(
    field: NumberField,
    *,
    row_inventory: minus_w_row_jets.RowJetInventory | None = None,
) -> tuple[Owner4Record, ...]:
    """Exercise one exact owner-4 record per stratum on exp-036's positive W."""
    correction = tuple(
        field.rational(index - 7) for index in range(tangent_cones.VARIABLE_COUNT)
    )
    records: list[Owner4Record] = []
    for stratum in tangent_cones.STRATA:
        active_rows = (
            None if row_inventory is None else row_inventory.active_rows(field, stratum)
        )
        record = owner4_record(
            field,
            stratum,
            tuple(tangent_inventory.geometry_vectors(field, stratum)[0]["W"]),
            correction,
            active_rows=active_rows,
        )
        if record.constant.sign() >= 0:
            raise ValueError("positive-W owner-4 control lost its strict production curvature")
        records.append(record)
    if len(records) != 3 or {record.stratum for record in records} != set(tangent_cones.STRATA):
        raise ValueError("three-stratum owner-4 record inventory drifted")
    return tuple(records)
