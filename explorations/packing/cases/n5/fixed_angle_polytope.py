#!/usr/bin/env python3
"""Certify the exact fixed-angle n=5 optimal-position polytope from exp-039.

The result is deliberately cell-local.  It proves an LP-optimal five-dimensional
position face and first-order stresses on twelve named paths, not global optimality,
local minimality, or a maximal stationary component.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass, replace
from pathlib import Path
from typing import cast

from strif import atomic_output_file

from cases.n5 import angle_sheet, tangent_cones, tangent_inventory
from cases.n5 import equal_side_face as face
from sqpack.field import FieldElement, NumberField

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_VERSION = 1
RESULTS = ROOT / "campaign/series/series-000-smoke-and-calibration/results"
EXP033 = RESULTS / "exp-033-h-023-n5-equal-side-face.json"
EXP034 = RESULTS / "exp-034-h-023-n5-angle-sheet.json"
EXP038 = RESULTS / "exp-038-h-023-n5-tangent-inventory.json"
CLASSES = ("R1", "R2", "R3", "R6")
STRATA = ("A", "interior", "B")
OWNERS = ("owner3:a+", "owner4:a+")
REDUCED_VARIABLES = ("x0", "y0", "x1", "y1", "a")
REFUSED_CLAIMS = (
    "global_optimality",
    "second_order_local_minimum",
    "quench_terminal",
    "maximal_stationary_component",
    "R4_continuation",
    "R5_continuation",
    "minus_W_continuation",
    "mixed_angle_continuation",
    "basin_mass",
    "census_completeness",
    "unequal_side_clearance",
)


@dataclass(frozen=True)
class ProofInputs:
    """Every value changed by a preregistered negative control."""

    add_a_slide: bool = True
    add_b_slide: bool = False
    r6_dx4_numerator: int = -1
    interior_interval_multiplier: int = 1
    dropped_inequality: str | None = None
    dual_pair_24_numerator: int = -1
    owner3_wplus_shift_numerator: int = 0
    owners: tuple[str, ...] = OWNERS
    extra_zero_axis: str | None = None
    promoted_claim: str | None = None


@dataclass(frozen=True)
class AffineRow:
    label: str
    constant: FieldElement
    coefficients: tuple[FieldElement, ...]


def require_dict(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise TypeError(f"{label} must be an object")
    return cast(dict[str, object], value)


def require_list(value: object, label: str) -> list[object]:
    if not isinstance(value, list):
        raise TypeError(f"{label} must be a list")
    return value


def encode(value: FieldElement) -> list[str]:
    return tangent_cones.encode(value)


def encode_affine(row: AffineRow) -> dict[str, object]:
    return {
        "label": row.label,
        "sense": "constant + coefficients dot variables >= 0",
        "variables": list(REDUCED_VARIABLES),
        "constant_low_degree_first": encode(row.constant),
        "coefficients_low_degree_first": [encode(value) for value in row.coefficients],
    }


def affine_value(
    row: AffineRow, values: list[FieldElement], field: NumberField
) -> FieldElement:
    return row.constant + sum(
        (
            coefficient * value
            for coefficient, value in zip(row.coefficients, values, strict=True)
        ),
        field.zero,
    )


def affine_scaled(row: AffineRow, scale: FieldElement, label: str) -> AffineRow:
    return AffineRow(
        label,
        scale * row.constant,
        tuple(scale * value for value in row.coefficients),
    )


def affine_plus_constant(row: AffineRow, constant: FieldElement, label: str) -> AffineRow:
    return AffineRow(label, row.constant + constant, row.coefficients)


def same_affine(left: AffineRow, right: AffineRow) -> bool:
    return left.constant == right.constant and left.coefficients == right.coefficients


def declared_rows(field: NumberField, inputs: ProofInputs) -> list[AffineRow]:
    q = field.rational
    r = field.alpha

    def row(label: str, constant: FieldElement, *coefficients: FieldElement) -> AffineRow:
        return AffineRow(label, constant, tuple(coefficients))

    z = q(0)
    one = q(1)
    rows = [
        row("x0_lower", -q(1) / 2, one, z, z, z, z),
        row("x0_upper", q(1) / 2 + r / 4, -one, z, z, z, z),
        row("y0_lower", -q(3) / 2, z, one, z, z, z),
        row("y0_upper", q(1) / 2 + 5 * r / 4, z, -one, z, z, z),
        row("x1_lower", -q(3) / 2, z, z, one, z, z),
        row("x1_upper", q(1) / 2 + 5 * r / 4, z, z, -one, z, z),
        row("y1_lower", -q(1) / 2, z, z, z, one, z),
        row("y1_upper", q(1) / 2 + r / 4, z, z, z, -one, z),
        row("a_lower", -r / 2, z, z, z, z, one),
        row("a_upper", q(2), z, z, z, z, -one),
        row("pair_0_1", -one, -one, z, one, z, z),
        row("pair_0_4", -q(3) - r, -one, one, z, z, q(2)),
        row("pair_1_4", one, z, z, one, -one, -q(2)),
    ]
    return [row_value for row_value in rows if row_value.label != inputs.dropped_inequality]


def fixed_position(field: NumberField, reduced: list[FieldElement]) -> list[FieldElement]:
    """Map (x0,y0,x1,y1,a) to (S,x0..x4,y0..y4)."""
    q = field.rational
    r = field.alpha
    x0, y0, x1, y1, a = reduced
    return [
        q(1) + 5 * r / 4,
        x0,
        x1,
        q(1) / 2,
        q(1) + 3 * r / 4,
        a,
        y0,
        y1,
        q(1) / 2,
        q(1) + 3 * r / 4,
        q(2) + r / 2 - a,
    ]


def substituted_cell_rows(field: NumberField) -> list[AffineRow]:
    labels, rows, rhs = face.cell_system(field)
    zero = field.zero
    base = fixed_position(field, [zero, zero, zero, zero, zero])
    columns = (1, 6, 2, 7, 5)
    result: list[AffineRow] = []
    for label, source_row, bound in zip(labels, rows, rhs, strict=True):
        constant = bound - face.dot(source_row, base, field)
        coefficients = [-source_row[index] for index in columns]
        # y4 = 2+r/2-a contributes the second a coefficient.
        coefficients[4] += source_row[10]
        result.append(AffineRow(label, constant, tuple(coefficients)))
    return result


def reduced_base(field: NumberField) -> list[FieldElement]:
    centres = tangent_cones.centres_for_stratum(field, "interior")
    return [centres[0][0], centres[0][1], centres[1][0], centres[1][1], centres[4][0]]


def canonical_vectors(field: NumberField) -> dict[str, list[FieldElement]]:
    q = field.rational
    return {
        "s": tangent_inventory.exact_vector(
            field, {tangent_cones.x(0): q(1), tangent_cones.y(0): q(1)}
        ),
        "R1": tangent_inventory.exact_vector(
            field,
            {
                tangent_cones.x(0): -q(1),
                tangent_cones.x(4): -q(1) / 2,
                tangent_cones.y(4): q(1) / 2,
            },
        ),
        "R2": tangent_inventory.exact_vector(field, {tangent_cones.x(0): -q(1)}),
        "R3": tangent_inventory.exact_vector(
            field,
            {
                tangent_cones.x(0): -q(1),
                tangent_cones.y(1): q(1),
                tangent_cones.x(4): -q(1) / 2,
                tangent_cones.y(4): q(1) / 2,
            },
        ),
        "R6": tangent_inventory.exact_vector(
            field,
            {
                tangent_cones.x(0): -q(1),
                tangent_cones.x(1): -q(1),
                tangent_cones.x(4): -q(1) / 2,
                tangent_cones.y(4): q(1) / 2,
            },
        ),
    }


def path_direction(
    field: NumberField, stratum: str, name: str, inputs: ProofInputs
) -> list[FieldElement]:
    vectors = canonical_vectors(field)
    result = list(vectors[name])
    if name == "R6":
        result[tangent_cones.x(4)] = field.rational(inputs.r6_dx4_numerator) / 2
        result[tangent_cones.y(4)] = -result[tangent_cones.x(4)]
    add_slide = (stratum == "A" and inputs.add_a_slide) or (
        stratum == "B" and inputs.add_b_slide
    )
    if add_slide:
        result = tangent_inventory.add_vectors(field, result, vectors["s"])
    return result


def reduced_direction(vector: list[FieldElement]) -> list[FieldElement]:
    return [
        vector[tangent_cones.x(0)],
        vector[tangent_cones.y(0)],
        vector[tangent_cones.x(1)],
        vector[tangent_cones.y(1)],
        vector[tangent_cones.x(4)],
    ]


def exact_rank(vectors: list[list[FieldElement]], field: NumberField) -> int:
    return tangent_inventory.coefficient_rank(vectors, field)


def domain_certificate(field: NumberField, inputs: ProofInputs) -> dict[str, object]:
    q = field.rational
    r = field.alpha
    rows = declared_rows(field, inputs)
    by_name = {row.label: row for row in rows}
    expected = {
        "x0_lower",
        "x0_upper",
        "y0_lower",
        "y0_upper",
        "x1_lower",
        "x1_upper",
        "y1_lower",
        "y1_upper",
        "a_lower",
        "a_upper",
        "pair_0_1",
        "pair_0_4",
        "pair_1_4",
    }
    if set(by_name) != expected:
        if inputs.dropped_inequality == "x0_lower":
            ray = [-q(1), q(0), q(0), q(0), q(0)]
            if not all(
                sum(
                    (
                        coefficient * value
                        for coefficient, value in zip(row.coefficients, ray, strict=True)
                    ),
                    field.zero,
                ).sign()
                >= 0
                for row in rows
            ):
                raise ValueError("the x0-lower removal did not expose its unbounded ray")
            raise ValueError("removing x0>=1/2 makes the eliminated domain unbounded")
        raise ValueError("the declared thirteen-row eliminated domain drifted")
    for lower, upper in (
        (q(1) / 2, q(1) / 2 + r / 4),
        (q(3) / 2, q(1) / 2 + 5 * r / 4),
        (q(3) / 2, q(1) / 2 + 5 * r / 4),
        (q(1) / 2, q(1) / 2 + r / 4),
        (r / 2, q(2)),
    ):
        if (upper - lower).sign() <= 0:
            raise ValueError("a declared coordinate interval is empty")

    original = {row.label: row for row in substituted_cell_rows(field)}
    decompositions: dict[str, tuple[str | None, FieldElement, FieldElement]] = {
        "0x-lower": ("x0_lower", q(1), q(0)),
        "0x-upper": ("x0_upper", q(1), r),
        "0y-lower": ("y0_lower", q(1), q(1)),
        "0y-upper": ("y0_upper", q(1), q(0)),
        "1x-lower": ("x1_lower", q(1), q(1)),
        "1x-upper": ("x1_upper", q(1), q(0)),
        "1y-lower": ("y1_lower", q(1), q(0)),
        "1y-upper": ("y1_upper", q(1), r),
        "2x-lower": (None, q(0), q(0)),
        "2x-upper": (None, q(0), 5 * r / 4),
        "2y-lower": (None, q(0), q(0)),
        "2y-upper": (None, q(0), 5 * r / 4),
        "3x-lower": (None, q(0), q(1) + r / 4),
        "3x-upper": (None, q(0), q(0)),
        "3y-lower": (None, q(0), q(1) + r / 4),
        "3y-upper": (None, q(0), q(0)),
        "4x-lower": ("a_lower", q(1), q(0)),
        "4x-upper": ("a_upper", q(1), -q(1) + 3 * r / 4),
        "4y-lower": ("a_upper", q(1), q(0)),
        "4y-upper": ("a_lower", q(1), -q(1) + 3 * r / 4),
        "pair-0-1": ("pair_0_1", q(1), q(0)),
        "pair-0-2": ("y0_lower", q(1), q(0)),
        "pair-0-3": ("x0_upper", q(1), q(0)),
        "pair-0-4": ("pair_0_4", r / 2, q(0)),
        "pair-1-2": ("x1_lower", q(1), q(0)),
        "pair-1-3": ("y1_upper", q(1), q(0)),
        "pair-1-4": ("pair_1_4", r / 2, q(0)),
        "pair-2-3": (None, q(0), q(1)),
        "pair-2-4": (None, q(0), q(0)),
        "pair-3-4": (None, q(0), q(0)),
    }
    if set(original) != set(decompositions) or len(original) != 30:
        raise ValueError("the exp-033 common-cell row inventory drifted")
    proof_rows: list[dict[str, object]] = []
    for label, (source_label, scale, constant) in decompositions.items():
        if constant.sign() < 0 or scale.sign() < 0:
            raise ValueError("a common-cell implication uses a negative multiplier")
        if source_label is None:
            candidate = AffineRow(label, constant, (q(0),) * 5)
        else:
            candidate = affine_plus_constant(
                affine_scaled(by_name[source_label], scale, label), constant, label
            )
        if not same_affine(original[label], candidate):
            raise ValueError(f"common-cell decomposition failed for {label}")
        proof_rows.append(
            {
                "common_cell_row": label,
                "eliminated_row": source_label,
                "nonnegative_scale": encode(scale),
                "nonnegative_constant": encode(constant),
            }
        )

    reverse_map = {
        "x0_lower": ("0x-lower", q(1)),
        "x0_upper": ("pair-0-3", q(1)),
        "y0_lower": ("pair-0-2", q(1)),
        "y0_upper": ("0y-upper", q(1)),
        "x1_lower": ("pair-1-2", q(1)),
        "x1_upper": ("1x-upper", q(1)),
        "y1_lower": ("1y-lower", q(1)),
        "y1_upper": ("pair-1-3", q(1)),
        "a_lower": ("4x-lower", q(1)),
        "a_upper": ("4y-lower", q(1)),
        "pair_0_1": ("pair-0-1", q(1)),
        "pair_0_4": ("pair-0-4", r),
        "pair_1_4": ("pair-1-4", r),
    }
    for label, (source_label, scale) in reverse_map.items():
        if not same_affine(by_name[label], affine_scaled(original[source_label], scale, label)):
            raise ValueError(f"reverse common-cell implication failed for {label}")

    base = reduced_base(field)
    eta = q(1) / 1000
    canonical = canonical_vectors(field)
    witness_directions = [canonical[name] for name in ("s", *CLASSES)]
    witnesses = [base]
    for direction in witness_directions:
        reduced = reduced_direction(direction)
        witnesses.append(
            [value + eta * step for value, step in zip(base, reduced, strict=True)]
        )
    if (
        exact_rank(
            [
                [right - left for right, left in zip(witness, base, strict=True)]
                for witness in witnesses[1:]
            ],
            field,
        )
        != 5
    ):
        raise ValueError("the six feasible points are not affinely independent")
    all_original = substituted_cell_rows(field)
    for witness in witnesses:
        if any(affine_value(row, witness, field).sign() < 0 for row in rows):
            raise ValueError("a proposed affine witness leaves the eliminated domain")
        if any(affine_value(row, witness, field).sign() < 0 for row in all_original):
            raise ValueError("a proposed affine witness leaves the 30-row common cell")

    return {
        "fixed_equalities": {
            "side": "1+5*sqrt(2)/4",
            "x2_equals_y2": "1/2",
            "x3_equals_y3": "1+3*sqrt(2)/4",
            "x4_plus_y4": "2+sqrt(2)/2",
        },
        "eliminated_variables": list(REDUCED_VARIABLES),
        "eliminated_inequalities": [encode_affine(row) for row in rows],
        "common_cell_row_count": len(original),
        "bidirectional_equivalence": True,
        "forward_nonnegative_decompositions": proof_rows,
        "reverse_exact_source_rows": {
            label: {
                "common_cell_row": source_label,
                "positive_scale": encode(scale),
            }
            for label, (source_label, scale) in reverse_map.items()
        },
        "bounded_by_coordinate_intervals": True,
        "affine_dimension": 5,
        "affinely_independent_feasible_point_count": len(witnesses),
        "witness_step": "1/1000",
        "witness_directions": ["base", "s", *CLASSES],
    }


def source_bindings(field: NumberField, inputs: ProofInputs) -> dict[str, object]:
    retained_033 = require_dict(json.loads(EXP033.read_text(encoding="utf-8")), "exp-033")
    face.require_same_result(retained_033, face.build_result())
    retained_034 = require_dict(json.loads(EXP034.read_text(encoding="utf-8")), "exp-034")
    angle_sheet.require_same_result(retained_034, angle_sheet.build_result())
    retained_038 = require_dict(json.loads(EXP038.read_text(encoding="utf-8")), "exp-038")
    tangent_inventory.require_same(retained_038, tangent_inventory.build_result())
    centres_a = tangent_cones.centres_for_stratum(field, "A")
    centres_b = tangent_cones.centres_for_stratum(field, "B")
    centres_i = tangent_cones.centres_for_stratum(field, "interior")
    if centres_i != [
        ((left[0] + right[0]) / 2, (left[1] + right[1]) / 2)
        for left, right in zip(centres_a, centres_b, strict=True)
    ]:
        raise ValueError("C_I is not the exact midpoint (C_A+C_B)/2")
    normalization = canonical_binding(field, inputs)
    return {
        "exp_033": str(EXP033.relative_to(ROOT)),
        "exp_034": str(EXP034.relative_to(ROOT)),
        "exp_038": str(EXP038.relative_to(ROOT)),
        "exact_regeneration_matches": True,
        "C_I_equals_exact_midpoint_of_C_A_and_C_B": True,
        "canonical_normalization": normalization,
    }


def canonical_binding(field: NumberField, inputs: ProofInputs) -> dict[str, object]:
    q = field.rational
    r = field.alpha
    canonical = canonical_vectors(field)
    for stratum in STRATA:
        _lineality, _sheet, stored, _kind = tangent_inventory.geometry_vectors(field, stratum)
        for name in CLASSES:
            expected = path_direction(field, stratum, name, inputs)
            if name in {"R1", "R2"}:
                expected = [r * value for value in expected]
            if stored[name] != expected:
                raise ValueError(
                    f"exp-038 canonical normalization drifted for {stratum} {name}"
                )
    if any(
        canonical["R6"][index] != value
        for index, value in {
            tangent_cones.x(0): -q(1),
            tangent_cones.x(1): -q(1),
            tangent_cones.x(4): -q(1) / 2,
            tangent_cones.y(4): q(1) / 2,
        }.items()
    ):
        raise ValueError("the canonical R6 coordinates drifted")
    return {
        "canonical_vectors": {
            name: tangent_inventory.encode_vector(vector) for name, vector in canonical.items()
        },
        "R1_R2_source_scale": "sqrt(2)",
        "A_slide_correction": "sqrt(2)*s for stored R1/R2; s for stored R3/R6",
        "interior_and_B_slide_correction": "none",
        "matches_exp_038": True,
    }


def dual_certificate(field: NumberField, inputs: ProofInputs) -> dict[str, object]:
    labels, rows, rhs = face.cell_system(field)
    q = field.rational
    r = field.alpha
    weights = [q(0) for _ in rows]
    for label in ("2x-lower", "2y-lower", "3x-upper", "3y-upper"):
        weights[labels.index(label)] = -q(1) / 2
    weights[labels.index("pair-2-4")] = q(inputs.dual_pair_24_numerator) * r / 2
    weights[labels.index("pair-3-4")] = -r / 2
    support_rows = [rows[index] for index, weight in enumerate(weights) if not weight.is_zero()]
    if len(support_rows) != 6 or face.exact_rank(support_rows) != 6:
        raise ValueError("the six dual-support rows lost exact rank six")
    objective = [q(1), *[q(0) for _ in range(face.VARIABLE_COUNT - 1)]]
    lhs = [
        sum((row[column] * weight for row, weight in zip(rows, weights, strict=True)), q(0))
        for column in range(face.VARIABLE_COUNT)
    ]
    value = sum((bound * weight for bound, weight in zip(rhs, weights, strict=True)), q(0))
    side = cast(FieldElement, face.exact_data(field)["side"])
    if lhs != objective or value != side or any(weight.sign() > 0 for weight in weights):
        raise ValueError("the fixed-angle LP dual identity failed")
    return {
        "support": [
            label for label, weight in zip(labels, weights, strict=True) if not weight.is_zero()
        ],
        "support_rank_in_eleven_variables": 6,
        "side_row_in_support_span": True,
        "identity": "A^T y=e_side, y<=0, b^T y=1+5*sqrt(2)/4",
        "optimal_side": "1+5*sqrt(2)/4",
        "scope": "one fixed-orientation labelled separating cell",
    }


def centres_along(
    field: NumberField, stratum: str, direction: list[FieldElement], epsilon: FieldElement
) -> list[tuple[FieldElement, FieldElement]]:
    centres = tangent_cones.centres_for_stratum(field, stratum)
    return [
        (
            centre[0] + epsilon * direction[tangent_cones.x(index)],
            centre[1] + epsilon * direction[tangent_cones.y(index)],
        )
        for index, centre in enumerate(centres)
    ]


def cell_slacks(
    field: NumberField, centres: list[tuple[FieldElement, FieldElement]]
) -> dict[str, FieldElement]:
    labels, rows, rhs = face.cell_system(field)
    side = cast(FieldElement, face.exact_data(field)["side"])
    values = face.vector(side, centres)
    return {
        label: bound - face.dot(row, values, field)
        for label, row, bound in zip(labels, rows, rhs, strict=True)
    }


def sat_projection_and_support(
    field: NumberField,
    centres: list[tuple[FieldElement, FieldElement]],
    *,
    first: int,
    second: int,
    owner: int,
    axis_name: str,
) -> tuple[FieldElement, FieldElement]:
    axes = tangent_cones.orientation_axes(field)
    axis_entry = next(item for item in axes[owner] if item[2] == axis_name)
    axis = (axis_entry[0], axis_entry[1])
    displacement = (
        centres[second][0] - centres[first][0],
        centres[second][1] - centres[first][1],
    )
    projection = tangent_cones.dot2(displacement, axis)
    support = field.zero
    for index in (first, second):
        for bx, by, _name in axes[index]:
            support += tangent_cones.abs_exact(tangent_cones.dot2(axis, (bx, by))) / 2
    return projection, support


def active_axis_certificate(
    field: NumberField,
    start: list[tuple[FieldElement, FieldElement]],
    end: list[tuple[FieldElement, FieldElement]],
    inputs: ProofInputs,
) -> dict[str, object]:
    expected = {
        "2-4:owner4:a+",
        "3-4:owner3:a+",
        "3-4:owner4:a+",
    }
    if inputs.extra_zero_axis is not None:
        expected.add(inputs.extra_zero_axis)
    actual: set[str] = set()
    endpoint_data: dict[str, dict[str, object]] = {}
    for first, second in ((2, 4), (3, 4)):
        for owner in (first, second):
            for _ax, _ay, axis_name in tangent_cones.orientation_axes(field)[owner]:
                label = f"{first}-{second}:owner{owner}:{axis_name}"
                values = [
                    sat_projection_and_support(
                        field,
                        centres,
                        first=first,
                        second=second,
                        owner=owner,
                        axis_name=axis_name,
                    )
                    for centres in (start, end)
                ]
                projections = [value[0] for value in values]
                supports = [value[1] for value in values]
                if supports[0] != supports[1]:
                    raise ValueError("fixed orientations changed an owner-axis support")
                gaps = [
                    tangent_cones.abs_exact(projection) - support
                    for projection, support in values
                ]
                endpoint_data[label] = {
                    "signed_projections": [encode(value) for value in projections],
                    "support": encode(supports[0]),
                    "gaps": [encode(value) for value in gaps],
                }
                if label in expected:
                    if (
                        any(projection.sign() == 0 for projection in projections)
                        or projections[0].sign() != projections[1].sign()
                        or any(not gap.is_zero() for gap in gaps)
                    ):
                        raise ValueError(
                            "an expected zero axis lacks a fixed strict projection sign "
                            "or zero endpoint gaps"
                        )
                    actual.add(label)
                elif any(gap.sign() >= 0 for gap in gaps):
                    raise ValueError(
                        "an unlisted owner axis is not strictly negative at both endpoints"
                    )
    if actual != expected:
        raise ValueError("the zero separating-axis exhaustion claim failed")
    return {
        "zero_axes": sorted(actual),
        "scope": "owner axes of contacts (2,4) and (3,4) only",
        "zero_axis_proof": (
            "each zero axis has strict same-sign endpoint projections and zero endpoint "
            "gaps, so its absolute affine projection and gap are affine and identically zero"
        ),
        "all_other_owner_axes_strictly_negative_at_both_interval_endpoints": True,
        "other_axis_proof": (
            "for every other owner axis, |affine projection|-constant support is convex; "
            "its strict-negative endpoint maximum bounds the full segment, even if the "
            "signed projection crosses zero"
        ),
        "endpoint_data": endpoint_data,
    }


def stress_at(
    field: NumberField,
    centres: list[tuple[FieldElement, FieldElement]],
    *,
    name: str,
    epsilon: FieldElement,
    owner: str,
    inputs: ProofInputs,
) -> dict[str, object]:
    q = field.rational
    r = field.alpha
    selected_walls = [
        row
        for row in tangent_cones.wall_rows(field, "interior")
        if row.label.startswith("wall:2:") or row.label.startswith("wall:3:")
    ]
    contact_24 = list(
        tangent_cones.contact_axis_rows(
            field, centres, first=2, second=4, owner=4, axis_name="a+"
        )
    )
    owner_index = 3 if owner == "owner3:a+" else 4
    contact_34 = list(
        tangent_cones.contact_axis_rows(
            field, centres, first=3, second=4, owner=owner_index, axis_name="a+"
        )
    )
    if len(selected_walls) != 6 or len(contact_24) != 1 or len(contact_34) != 2:
        raise ValueError("an active stress row or tied feature row is missing")
    rows = [*selected_walls, *contact_24, *contact_34]
    weights = [r / 4 if row.label.startswith("wall:2:") else r / 2 for row in selected_walls]
    weights.append(q(1))
    path_q = q(0) if name == "R2" else epsilon
    if owner == "owner3:a+":
        weights.extend(
            (
                q(5) / 4
                - r * (q(1) + path_q) / 2
                + q(inputs.owner3_wplus_shift_numerator) / 1000,
                -q(1) / 4 + r * (q(1) + path_q) / 2,
            )
        )
    elif owner == "owner4:a+":
        weights.extend((q(1) / 2, q(1) / 2))
    else:
        raise ValueError("an unknown owner branch was requested")
    if any(weight.sign() <= 0 for weight in weights):
        raise ValueError("a branchwise stress multiplier is not strictly positive")
    lower_bound = r / 2 - q(1) / 4
    if owner == "owner3:a+" and any(
        (weight - lower_bound).sign() < 0 for weight in weights[-2:]
    ):
        raise ValueError("an owner-3 multiplier fell below the exact uniform bound")
    pose_sum = [
        sum(
            (
                weight * row.coefficients[index]
                for weight, row in zip(weights, rows, strict=True)
            ),
            q(0),
        )
        for index in range(tangent_cones.VARIABLE_COUNT)
    ]
    if any(not value.is_zero() for value in pose_sum):
        raise ValueError("the branchwise stress pose-column sum is not zero")
    side_coefficient = sum(
        (
            weight
            for weight, row in zip(weights, rows, strict=True)
            if row.label.startswith("wall:3:")
        ),
        q(0),
    )
    if side_coefficient != r:
        raise ValueError("the stress identity does not equal sqrt(2) dL")
    return {
        "owner": owner,
        "epsilon": encode(epsilon),
        "row_labels": [row.label for row in rows],
        "weights": [encode(weight) for weight in weights],
        "pose_columns_sum_to_zero": True,
        "side_coefficient": encode(side_coefficient),
    }


def stress_polynomial_certificate(  # noqa: PLR0917 -- mirrors the frozen path inputs
    field: NumberField,
    stratum: str,
    direction: list[FieldElement],
    name: str,
    end: FieldElement,
    owner: str,
    inputs: ProofInputs,
) -> dict[str, object]:
    """Build and annihilate the stress polynomial, rather than infer its degree."""
    q = field.rational
    r = field.alpha
    owner_index = 3 if owner == "owner3:a+" else 4
    if owner not in OWNERS:
        raise ValueError("an unknown owner branch was requested")

    def system(
        epsilon: FieldElement,
    ) -> tuple[list[tangent_cones.LinearRow], list[FieldElement]]:
        centres = centres_along(field, stratum, direction, epsilon)
        walls = [
            row
            for row in tangent_cones.wall_rows(field, "interior")
            if row.label.startswith("wall:2:") or row.label.startswith("wall:3:")
        ]
        contact_24 = list(
            tangent_cones.contact_axis_rows(
                field, centres, first=2, second=4, owner=4, axis_name="a+"
            )
        )
        contact_34 = list(
            tangent_cones.contact_axis_rows(
                field,
                centres,
                first=3,
                second=4,
                owner=owner_index,
                axis_name="a+",
            )
        )
        rows = [*walls, *contact_24, *contact_34]
        weights = [r / 4 if row.label.startswith("wall:2:") else r / 2 for row in walls]
        weights.append(q(1))
        path_q = q(0) if name == "R2" else epsilon
        if owner == "owner3:a+":
            weights.extend(
                (
                    q(5) / 4
                    - r * (q(1) + path_q) / 2
                    + q(inputs.owner3_wplus_shift_numerator) / 1000,
                    -q(1) / 4 + r * (q(1) + path_q) / 2,
                )
            )
        else:
            weights.extend((q(1) / 2, q(1) / 2))
        return rows, weights

    start_centres = centres_along(field, stratum, direction, q(0))
    middle_centres = centres_along(field, stratum, direction, end / 2)
    end_centres = centres_along(field, stratum, direction, end)
    if middle_centres != [
        ((left[0] + right[0]) / 2, (left[1] + right[1]) / 2)
        for left, right in zip(start_centres, end_centres, strict=True)
    ]:
        raise ValueError("the path centres are not exactly affine in epsilon")

    contact_specs = ((2, 4, 4), (3, 4, owner_index))
    projection_signs: dict[str, int] = {}
    for first, second, axis_owner in contact_specs:
        endpoint_values = [
            sat_projection_and_support(
                field,
                centres,
                first=first,
                second=second,
                owner=axis_owner,
                axis_name="a+",
            )
            for centres in (start_centres, end_centres)
        ]
        projections = [value[0] for value in endpoint_values]
        if (
            any(value.sign() == 0 for value in projections)
            or projections[0].sign() != projections[1].sign()
        ):
            raise ValueError("a selected stress axis lacks a fixed strict projection sign")
        projection_signs[f"{first}-{second}:owner{axis_owner}:a+"] = projections[0].sign()

    rows_0, weights_0 = system(q(0))
    rows_m, weights_m = system(end / 2)
    rows_e, weights_e = system(end)
    labels = [row.label for row in rows_0]
    if [row.label for row in rows_m] != labels or [row.label for row in rows_e] != labels:
        raise ValueError("the tied source-row label inventory changes along a path")
    row_polynomials: list[list[tuple[FieldElement, FieldElement]]] = []
    for row_0, row_m, row_e in zip(rows_0, rows_m, rows_e, strict=True):
        structural_slopes = [q(0) for _ in range(tangent_cones.VARIABLE_COUNT)]
        if row_0.label.startswith("contact:2-4:owner4:a+"):
            first, second, axis_owner = 2, 4, 4
        elif row_0.label.startswith(f"contact:3-4:owner{owner_index}:a+"):
            first, second, axis_owner = 3, 4, owner_index
        elif row_0.label.startswith("wall:"):
            first = second = axis_owner = -1
        else:
            raise ValueError("an unknown row entered the stress support")
        if axis_owner >= 0:
            axis_entry = next(
                item
                for item in tangent_cones.orientation_axes(field)[axis_owner]
                if item[2] == "a+"
            )
            axis = (axis_entry[0], axis_entry[1])
            velocity = (
                direction[tangent_cones.x(second)] - direction[tangent_cones.x(first)],
                direction[tangent_cones.y(second)] - direction[tangent_cones.y(first)],
            )
            key = f"{first}-{second}:owner{axis_owner}:a+"
            structural_slopes[tangent_cones.theta(axis_owner)] = q(
                projection_signs[key]
            ) * tangent_cones.dot2(velocity, tangent_cones.perpendicular(axis))
        coefficients: list[tuple[FieldElement, FieldElement]] = []
        for value_0, value_m, value_e, slope in zip(
            row_0.coefficients,
            row_m.coefficients,
            row_e.coefficients,
            structural_slopes,
            strict=True,
        ):
            if value_m != value_0 + slope * end / 2 or value_e != value_0 + slope * end:
                raise ValueError(
                    "a rebuilt source row disagrees with its structural affine form"
                )
            coefficients.append((value_0, slope))
        row_polynomials.append(coefficients)
    weight_polynomials: list[tuple[FieldElement, FieldElement]] = []
    weight_slopes = [q(0) for _ in weights_0]
    if owner == "owner3:a+" and name != "R2":
        weight_slopes[-2:] = [-r / 2, r / 2]
    for value_0, value_m, value_e, slope in zip(
        weights_0, weights_m, weights_e, weight_slopes, strict=True
    ):
        if value_m != value_0 + slope * end / 2 or value_e != value_0 + slope * end:
            raise ValueError("a stress weight disagrees with its declared affine formula")
        weight_polynomials.append((value_0, slope))

    coefficient_polynomials: list[list[FieldElement]] = []
    for index in range(tangent_cones.VARIABLE_COUNT):
        polynomial = [q(0), q(0), q(0)]
        for row_poly, weight_poly in zip(row_polynomials, weight_polynomials, strict=True):
            row_0, row_1 = row_poly[index]
            weight_0, weight_1 = weight_poly
            polynomial[0] += row_0 * weight_0
            polynomial[1] += row_0 * weight_1 + row_1 * weight_0
            polynomial[2] += row_1 * weight_1
        if any(not value.is_zero() for value in polynomial):
            raise ValueError("a pose-column stress polynomial is not identically zero")
        coefficient_polynomials.append(polynomial)
    side_polynomial = [
        sum(
            (
                weight_polynomials[index][degree]
                for index, row in enumerate(rows_0)
                if row.label.startswith("wall:3:")
            ),
            q(0),
        )
        for degree in (0, 1)
    ]
    if side_polynomial != [r, q(0)]:
        raise ValueError("the side-column stress polynomial is not exactly sqrt(2)")
    return {
        "affine_centres_checked": True,
        "selected_axis_strict_projection_signs": projection_signs,
        "stable_tied_row_labels": labels,
        "source_row_coefficients_affine_checked": True,
        "stress_weights_affine_checked": True,
        "pose_polynomial_coefficients": [
            [encode(value) for value in polynomial] for polynomial in coefficient_polynomials
        ],
        "side_polynomial_coefficients": [encode(value) for value in side_polynomial],
        "degree_at_most_two_derived": True,
        "all_coefficients_match_sqrt2_dL_identity": True,
    }


def path_certificates(field: NumberField, inputs: ProofInputs) -> list[dict[str, object]]:
    q = field.rational
    r = field.alpha
    delta = 3 * r / 2 - 2
    if set(inputs.owners) != set(OWNERS) or len(inputs.owners) != 2:
        raise ValueError("both owner branches are required")
    lower_bound = r / 2 - q(1) / 4
    if lower_bound.sign() <= 0:
        raise ValueError("the owner-3 uniform stress bound is not positive")
    if -q(1) / 4 + r / 2 != lower_bound or q(5) / 4 - r * (q(1) + delta) / 2 != lower_bound:
        raise ValueError("the two endpoint formulas do not give the uniform stress bound")
    records: list[dict[str, object]] = []
    for stratum in STRATA:
        nominal_end = delta / 2 if stratum == "interior" else delta
        if stratum == "interior":
            nominal_end *= inputs.interior_interval_multiplier
        limiting_label = "0y-upper" if stratum == "A" else "0x-lower"
        for name in CLASSES:
            direction = path_direction(field, stratum, name, inputs)
            start_centres = tangent_cones.centres_for_stratum(field, stratum)
            end_centres = centres_along(field, stratum, direction, nominal_end)
            start_slacks = cell_slacks(field, start_centres)
            end_slacks = cell_slacks(field, end_centres)
            if any(value.sign() < 0 for value in start_slacks.values()):
                raise ValueError("a declared path starts outside the common cell")
            if any(value.sign() < 0 for value in end_slacks.values()):
                raise ValueError("a declared path endpoint leaves the common cell")
            newly_tight = {
                label
                for label in start_slacks
                if start_slacks[label].sign() > 0 and end_slacks[label].is_zero()
            }
            if newly_tight != {limiting_label}:
                raise ValueError("the sharp interval does not have its unique limiting row")
            slope = (end_slacks[limiting_label] - start_slacks[limiting_label]) / nominal_end
            if slope.sign() >= 0:
                raise ValueError("the limiting row does not decrease along the path")
            beyond = nominal_end + q(1) / 1000
            beyond_slack = start_slacks[limiting_label] + beyond * slope
            if beyond_slack.sign() >= 0:
                raise ValueError("the named limiting row is not violated beyond the endpoint")

            fixtures: list[dict[str, object]] = []
            for fixture_name, epsilon in (
                ("strict-interior", nominal_end / 2),
                ("endpoint", nominal_end),
            ):
                centres = centres_along(field, stratum, direction, epsilon)
                report = face.exact_packing_valid(
                    field, centres, cast(FieldElement, face.exact_data(field)["side"])
                )
                if report["valid"] is not True:
                    raise ValueError("a separately checked exact path packing is invalid")
                fixtures.append({"name": fixture_name, "epsilon": encode(epsilon), **report})

            axes = active_axis_certificate(field, start_centres, end_centres, inputs)
            stress_polynomials = [
                stress_polynomial_certificate(
                    field,
                    stratum,
                    direction,
                    name,
                    nominal_end,
                    owner,
                    inputs,
                )
                for owner in inputs.owners
            ]
            stress_samples: list[dict[str, object]] = []
            for epsilon in (q(0), nominal_end / 2, nominal_end):
                centres = centres_along(field, stratum, direction, epsilon)
                stress_samples.extend(
                    stress_at(
                        field,
                        centres,
                        name=name,
                        epsilon=epsilon,
                        owner=owner,
                        inputs=inputs,
                    )
                    for owner in inputs.owners
                )
            records.append(
                {
                    "stratum": stratum,
                    "class": name,
                    "direction": tangent_inventory.encode_vector(direction),
                    "sharp_interval": {"lower": encode(q(0)), "upper": encode(nominal_end)},
                    "unique_limiting_row": limiting_label,
                    "limiting_row_violated_beyond_endpoint": True,
                    "exact_packing_fixtures": fixtures,
                    "active_axis_exhaustion": axes,
                    "stress_identity": {
                        "polynomial_degree_bound_in_epsilon": 2,
                        "coefficient_certificates": stress_polynomials,
                        "three_exact_samples_are_fixtures_only": True,
                        "sample_fixtures": stress_samples,
                    },
                }
            )
    if len(records) != 12:
        raise ValueError("the path inventory does not contain exactly twelve paths")
    return records


def proof_core(field: NumberField, inputs: ProofInputs) -> dict[str, object]:
    if inputs.promoted_claim is not None:
        raise ValueError("the requested promoted claim lies outside the frozen scope")
    canonical_binding(field, inputs)
    return {
        "domain": domain_certificate(field, inputs),
        "dual": dual_certificate(field, inputs),
        "paths": path_certificates(field, inputs),
        "stress_uniform_bound": {
            "owner3_exact_lower_bound": encode(field.alpha / 2 - field.rational(1) / 4),
            "strictly_positive": True,
            "identity": "sum_j w_j z_j = sqrt(2) dL",
            "scope": "the twelve declared path segments only",
        },
    }


def validate_result(result: dict[str, object]) -> None:
    sources = require_dict(result.get("sources"), "sources")
    if sources.get("exact_regeneration_matches") is not True:
        raise ValueError("the exact predecessor binding is missing")
    certificate = require_dict(result.get("certificate"), "certificate")
    domain = require_dict(certificate.get("domain"), "domain")
    if (
        domain.get("common_cell_row_count") != 30
        or domain.get("bidirectional_equivalence") is not True
        or domain.get("bounded_by_coordinate_intervals") is not True
        or domain.get("affine_dimension") != 5
        or domain.get("affinely_independent_feasible_point_count") != 6
    ):
        raise ValueError("the five-dimensional domain certificate is incomplete")
    dual = require_dict(certificate.get("dual"), "dual")
    if (
        dual.get("support_rank_in_eleven_variables") != 6
        or dual.get("side_row_in_support_span") is not True
    ):
        raise ValueError("the exact dual certificate is incomplete")
    paths = require_list(certificate.get("paths"), "paths")
    if len(paths) != 12:
        raise ValueError("the exact twelve-path inventory is incomplete")
    if any(
        len(require_list(require_dict(path, "path").get("exact_packing_fixtures"), "fixtures"))
        != 2
        for path in paths
    ):
        raise ValueError("a path lacks separately checked exact packing fixtures")
    scope = require_dict(result.get("scope_refusals"), "scope refusals")
    if (
        set(require_list(scope.get("refused_claims"), "refused claims")) != set(REFUSED_CLAIMS)
        or scope.get("all_refused") is not True
    ):
        raise ValueError("the frozen refusal boundary drifted")
    determination = require_dict(result.get("determination"), "determination")
    if determination.get("outcome") != "criterion_met":
        raise ValueError("the exp-039 criterion was not met")


def mutation_rejected(field: NumberField, inputs: ProofInputs) -> bool:
    try:
        proof_core(field, inputs)
    except TypeError, ValueError:
        return True
    return False


def controls(field: NumberField) -> dict[str, bool]:
    base = ProofInputs()
    mutations = {
        "omitted_A_slide_correction_rejected": replace(base, add_a_slide=False),
        "added_B_slide_correction_rejected": replace(base, add_b_slide=True),
        "R6_without_dx4_rejected": replace(base, r6_dx4_numerator=0),
        "overlong_interior_path_rejected": replace(base, interior_interval_multiplier=2),
        "removed_nonredundant_inequality_rejected": replace(
            base, dropped_inequality="x0_lower"
        ),
        "perturbed_LP_dual_coefficient_rejected": replace(base, dual_pair_24_numerator=-2),
        "perturbed_owner3_stress_multiplier_rejected": replace(
            base, owner3_wplus_shift_numerator=1
        ),
        "missing_owner_branch_rejected": replace(base, owners=("owner3:a+",)),
        "false_zero_axis_claim_rejected": replace(base, extra_zero_axis="2-4:owner2:x"),
        "scope_promotion_rejected": replace(base, promoted_claim="second_order_local_minimum"),
    }
    return {name: mutation_rejected(field, mutation) for name, mutation in mutations.items()}


def build_result() -> dict[str, object]:
    field = face.make_field()
    inputs = ProofInputs()
    result: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "contract": "packing.squares:N5FixedAnglePolytope/v1",
        "field": "Q(sqrt(2)), sqrt(2) in (1,2)",
        "sources": source_bindings(field, inputs),
        "certificate": proof_core(field, inputs),
        "scope_refusals": {
            "refused_claims": list(REFUSED_CLAIMS),
            "all_refused": True,
            "statement": (
                "cell-local LP optimality and pathwise first-order stationarity only; "
                "the listed global, second-order, terminal, continuation, basin, census, "
                "and unequal-side claims remain unresolved"
            ),
        },
        "determination": {
            "outcome": "criterion_met",
            "claim": (
                "R1, R2, R3, and R6 lie in one connected five-dimensional common-cell "
                "LP-optimal position polytope, with positive first-order stresses on "
                "their twelve declared sharp path segments"
            ),
            "scope": (
                "one fixed-orientation labelled separating cell; no global optimality, "
                "second-order local-minimum, terminality, or maximal-component claim"
            ),
        },
    }
    validate_result(result)
    result["controls"] = controls(field)
    control_values = require_dict(result["controls"], "controls")
    if len(control_values) != 10 or not all(control_values.values()):
        raise ValueError(f"a preregistered control survived: {control_values}")
    return result


def write_json_atomic(path: Path, value: dict[str, object]) -> None:
    with atomic_output_file(path, make_parents=True) as temporary:
        temporary.write_text(
            json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )


def require_same(retained: object, regenerated: dict[str, object]) -> None:
    if retained != regenerated:
        raise ValueError("retained exp-039 record differs from exact regeneration")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--record", type=Path)
    mode.add_argument("--replay", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    started = time.monotonic()
    try:
        result = build_result()
        if args.record is not None:
            write_json_atomic(args.record, result)
        else:
            retained = json.loads(args.replay.read_text(encoding="utf-8"))
            require_same(retained, result)
        summary = {
            "record_written": args.record is not None,
            "record_replayed": args.replay is not None,
            "determination_outcome": require_dict(result["determination"], "determination")[
                "outcome"
            ],
            "affine_dimension": require_dict(
                require_dict(result["certificate"], "certificate")["domain"], "domain"
            )["affine_dimension"],
            "path_count": len(
                require_list(
                    require_dict(result["certificate"], "certificate")["paths"], "paths"
                )
            ),
            "controls": result["controls"],
            "elapsed_seconds": round(time.monotonic() - started, 6),
        }
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
