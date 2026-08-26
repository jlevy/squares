#!/usr/bin/env python3
"""Certify the six exact rotating R4/R5 release paths from exp-040."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, replace
from itertools import pairwise
from math import comb
from pathlib import Path
from typing import cast

from strif import atomic_output_file

from cases.n5 import equal_side_face as face
from cases.n5 import fixed_angle_polytope, tangent_cones, tangent_inventory
from sqpack.field import FieldElement, NumberField
from sqpack.verify import exact_sign, verify_packing

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "campaign/series/series-000-smoke-and-calibration/results"
EXP033 = RESULTS / "exp-033-h-023-n5-equal-side-face.json"
EXP038 = RESULTS / "exp-038-h-023-n5-tangent-inventory.json"
EXP039 = RESULTS / "exp-039-h-023-n5-fixed-angle-polytope.json"
SCHEMA_VERSION = 1
SIGNS = (("R4", -1), ("R5", 1))
STRATA = ("A", "interior", "B")
OWNERS = ("owner3:a+", "owner4:a+")
DENOMINATOR = (4, 0, 1)
MAX_BERNSTEIN_DEPTH = 8
REFUSED_CLAIMS = (
    "A_to_B_stationary_connection",
    "whole_polytope_classification",
    "terminal_or_second_order_local_minimum",
    "maximal_stationary_component",
    "minus_W_or_mixed_direction",
    "quench_selection_or_basin_mass",
    "census_completeness",
    "unequal_side_clearance",
)
CONTROL_KEYS = frozenset(
    {
        "non_unit_orientation_rejected",
        "sign_label_swap_rejected",
        "missing_A_slide_rejected",
        "added_B_slide_rejected",
        "changed_square1_displacement_rejected",
        "changed_square4_displacement_rejected",
        "false_midpoint_identity_rejected",
        "missing_R4_rejected",
        "missing_R5_rejected",
        "missing_stratum_rejected",
        "missing_owner_rejected",
        "missing_tied_feature_rejected",
        "sampled_only_rejected",
        "perturbed_numerator_rejected",
        "perturbed_stress_rejected",
        "false_active_slack_rejected",
        "overlong_interior_interval_rejected",
        "missing_zero_axis_rejected",
        "extra_zero_axis_rejected",
        "scope_promotion_rejected",
    }
)
BASE_ZERO_AXES = frozenset(
    {
        "0-4:owner4:a-",
        "1-4:owner4:a-",
        "2-4:owner4:a+",
        "3-4:owner3:a+",
        "3-4:owner4:a+",
    }
)
PATH_ZERO_AXES = BASE_ZERO_AXES - {"1-4:owner4:a-"}


@dataclass(frozen=True)
class ProofInputs:
    """Values changed by the preregistered controls."""

    signs: tuple[tuple[str, int], ...] = SIGNS
    strata: tuple[str, ...] = STRATA
    owners: tuple[str, ...] = OWNERS
    include_all_tied_features: bool = True
    sign_label_swap: bool = False
    add_a_slide: bool = True
    add_b_slide: bool = False
    dx4_numerator: int = -1
    dx1_numerator: int = -1
    midpoint_shift_numerator: int = 0
    orientation_unit_shift: int = 0
    bad_sign_probe: bool = False
    numerator_shift: int = 0
    stress_shift: int = 0
    false_active_slack: bool = False
    interior_interval_multiplier: int = 1
    removed_base_zero_axis: str | None = None
    added_path_zero_axis: str | None = None
    promoted_claim: str | None = None


Poly = tuple[FieldElement, ...]


def require_dict(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise TypeError(f"{label} must be an object")
    return cast(dict[str, object], value)


def encode(value: FieldElement) -> list[str]:
    return tangent_cones.encode(value)


def trim(poly: Poly) -> Poly:
    values = list(poly)
    while len(values) > 1 and values[-1].is_zero():
        values.pop()
    return tuple(values)


def poly_add(field: NumberField, *polys: Poly) -> Poly:
    width = max(len(poly) for poly in polys)
    return trim(
        tuple(
            sum((poly[index] for poly in polys if index < len(poly)), field.zero)
            for index in range(width)
        )
    )


def poly_scale(poly: Poly, scale: FieldElement) -> Poly:
    return trim(tuple(scale * value for value in poly))


def poly_mul(field: NumberField, left: Poly, right: Poly) -> Poly:
    result = [field.zero for _ in range(len(left) + len(right) - 1)]
    for i, left_value in enumerate(left):
        for j, right_value in enumerate(right):
            result[i + j] += left_value * right_value
    return trim(tuple(result))


def poly_value(field: NumberField, poly: Poly, value: FieldElement) -> FieldElement:
    result = field.zero
    for coefficient in reversed(poly):
        result = result * value + coefficient
    return result


def exact_absolute_poly(field: NumberField, poly: Poly, interval_end: FieldElement) -> Poly:
    if all(value.is_zero() for value in poly):
        return poly
    midpoint_value = poly_value(field, poly, interval_end / 2)
    if midpoint_value.is_zero():
        raise ValueError("an absolute-value branch is undecided at the interval midpoint")
    signed = poly_scale(poly, field.rational(midpoint_value.sign()))
    certify_nonnegative(bernstein_coefficients(field, signed, interval_end), field)
    return signed


def affine_numerator(field: NumberField, base: FieldElement, speed: FieldElement) -> Poly:
    return poly_mul(field, (base, speed), tuple(field.rational(value) for value in DENOMINATOR))


def bernstein_coefficients(
    field: NumberField, poly: Poly, interval_end: FieldElement
) -> list[FieldElement]:
    degree = len(poly) - 1
    powers = [field.one]
    for _ in range(degree):
        powers.append(powers[-1] * interval_end)
    scaled = [coefficient * powers[index] for index, coefficient in enumerate(poly)]
    return [
        sum(
            (
                scaled[index] * field.rational(comb(k, index)) / comb(degree, index)
                for index in range(k + 1)
            ),
            field.zero,
        )
        for k in range(degree + 1)
    ]


def subdivide_bernstein(
    coefficients: list[FieldElement], field: NumberField
) -> tuple[list[FieldElement], list[FieldElement]]:
    levels = [coefficients]
    while len(levels[-1]) > 1:
        previous = levels[-1]
        levels.append([(left + right) / 2 for left, right in pairwise(previous)])
    return [level[0] for level in levels], [level[-1] for level in reversed(levels)]


def certify_nonnegative(
    coefficients: list[FieldElement], field: NumberField, depth: int = 0
) -> int:
    if all(value.sign() >= 0 for value in coefficients):
        return 1
    if depth >= MAX_BERNSTEIN_DEPTH:
        raise ValueError("an exact numerator remains uncertified at the subdivision limit")
    left, right = subdivide_bernstein(coefficients, field)
    return certify_nonnegative(left, field, depth + 1) + certify_nonnegative(
        right, field, depth + 1
    )


def minimum_exact(values: list[FieldElement]) -> FieldElement:
    result = values[0]
    for value in values[1:]:
        if (value - result).sign() < 0:
            result = value
    return result


def certify_strict_positive(
    coefficients: list[FieldElement], field: NumberField, depth: int = 0
) -> tuple[int, FieldElement]:
    if all(value.sign() > 0 for value in coefficients):
        return 1, minimum_exact(coefficients)
    if depth >= MAX_BERNSTEIN_DEPTH:
        raise ValueError("a strict residual remains uncertified at the subdivision limit")
    left, right = subdivide_bernstein(coefficients, field)
    left_count, left_bound = certify_strict_positive(left, field, depth + 1)
    right_count, right_bound = certify_strict_positive(right, field, depth + 1)
    return left_count + right_count, minimum_exact([left_bound, right_bound])


def strict_polynomial_certificate(
    field: NumberField, polynomial: Poly, interval_end: FieldElement
) -> dict[str, object]:
    coefficients = bernstein_coefficients(field, polynomial, interval_end)
    pieces, lower_bound = certify_strict_positive(coefficients, field)
    return {
        "coefficients_low_degree_first": [encode(value) for value in polynomial],
        "bernstein_subinterval_count": pieces,
        "bernstein_lower_bound": encode(lower_bound),
        "strictly_positive_on_closed_interval": True,
    }


def denominator_certificate(
    field: NumberField, interval_end: FieldElement
) -> dict[str, object]:
    q = field.rational
    denominator = (q(4), q(0), q(1))
    excess = poly_add(field, denominator, (q(-4),))
    certify_nonnegative(bernstein_coefficients(field, excess, interval_end), field)
    return {
        "polynomial": "4+u^2",
        "coefficients_low_degree_first": [encode(value) for value in denominator],
        "exact_lower_bound": encode(q(4)),
        "excess_over_lower_bound_nonnegative": True,
        "strictly_positive_on_closed_interval": True,
    }


def position_direction(
    field: NumberField, stratum: str, inputs: ProofInputs
) -> list[FieldElement]:
    lineality, _sheet, rays, _kind = tangent_inventory.geometry_vectors(field, stratum)
    del lineality
    result = [(left + right) / 2 for left, right in zip(rays["R3"], rays["R6"], strict=True)]
    result[tangent_cones.x(4)] = field.rational(inputs.dx4_numerator) / 2
    result[tangent_cones.y(4)] = -result[tangent_cones.x(4)]
    result[tangent_cones.x(1)] = field.rational(inputs.dx1_numerator) / 2
    result[tangent_cones.x(2)] += field.rational(inputs.midpoint_shift_numerator) / 1000
    if stratum == "A" and not inputs.add_a_slide:
        result[tangent_cones.x(0)] -= field.one
        result[tangent_cones.y(0)] -= field.one
    if stratum == "B" and inputs.add_b_slide:
        result[tangent_cones.x(0)] += field.one
        result[tangent_cones.y(0)] += field.one
    return result


def centres_at(
    field: NumberField, stratum: str, direction: list[FieldElement], u: FieldElement
) -> list[tuple[FieldElement, FieldElement]]:
    start = tangent_cones.centres_for_stratum(field, stratum)
    return [
        (
            point[0] + u * direction[tangent_cones.x(index)],
            point[1] + u * direction[tangent_cones.y(index)],
        )
        for index, point in enumerate(start)
    ]


def source_bindings(field: NumberField) -> dict[str, object]:
    regenerated = {
        "exp_033": face.build_result(),
        "exp_038": tangent_inventory.build_result(),
        "exp_039": fixed_angle_polytope.build_result(),
    }
    paths = {"exp_033": EXP033, "exp_038": EXP038, "exp_039": EXP039}
    for name, path in paths.items():
        retained = json.loads(path.read_text(encoding="utf-8"))
        if retained != regenerated[name]:
            raise ValueError(f"{name} exact source regeneration drifted")
    result: dict[str, object] = {
        name: str(path.relative_to(ROOT)) for name, path in paths.items()
    }
    result["exact_regeneration_matches"] = True
    return result


def fixed_axes(
    field: NumberField,
) -> tuple[tuple[tuple[FieldElement, FieldElement], ...], ...]:
    q = field.rational
    r = field.alpha
    aligned = ((q(1), q(0)), (q(0), q(1)))
    diagonal = ((r / 2, r / 2), (-r / 2, r / 2))
    return (aligned, aligned, aligned, diagonal, diagonal)


def constant_support(
    field: NumberField, square_index: int, axis: tuple[FieldElement, FieldElement]
) -> FieldElement:
    axes = fixed_axes(field)[square_index]
    return sum(
        (tangent_cones.abs_exact(tangent_cones.dot2(axis, basis)) / 2 for basis in axes),
        field.zero,
    )


def square1_support_numerator(
    field: NumberField, axis: tuple[FieldElement, FieldElement]
) -> Poly:
    q = field.rational
    r = field.alpha
    if axis in ((q(1), q(0)), (q(0), q(1))):
        return (q(2), q(2), -q(1) / 2)
    if axis in ((r / 2, r / 2), (-r / 2, r / 2)):
        return (q(2) * r, q(0), -r / 2)
    raise ValueError("the common cell contains an unknown square-1 support axis")


def square1_wall_feature_certificate(  # noqa: PLR0917 -- frozen case inputs
    field: NumberField,
    stratum: str,
    direction: list[FieldElement],
    sigma: int,
    interval_end: FieldElement,
    inputs: ProofInputs,
) -> dict[str, object]:
    q = field.rational
    starts = tangent_cones.centres_for_stratum(field, stratum)
    denominator = tuple(q(value) for value in DENOMINATOR)
    centre_x = affine_numerator(field, starts[1][0], direction[tangent_cones.x(1)])
    centre_y = affine_numerator(field, starts[1][1], direction[tangent_cones.y(1)])
    side = cast(FieldElement, face.exact_data(field)["side"])
    cosine = (q(4), q(0), -q(1))
    sine = (q(0), q(4 * sigma))
    records: list[dict[str, object]] = []
    derived_small_labels: list[str] = []
    for wall, clearance in (
        (
            "x-upper",
            poly_add(field, poly_scale(denominator, side), poly_scale(centre_x, -q(1))),
        ),
        ("y-lower", centre_y),
    ):
        wall_records: list[tuple[int, Poly]] = []
        for label_sign in (-1, 1):
            feature_support = poly_scale(
                poly_add(field, cosine, poly_scale(sine, q(-label_sign))), q(1) / 2
            )
            numerator = poly_add(field, clearance, poly_scale(feature_support, -q(1)))
            first_nonzero = next(
                index
                for index, coefficient in enumerate(numerator)
                if not coefficient.is_zero()
            )
            residual = numerator[first_nonzero:]
            strict = strict_polynomial_certificate(field, residual, interval_end)
            wall_records.append((label_sign, numerator))
            records.append(
                {
                    "label": f"wall:1:{wall}:{'+' if label_sign > 0 else '-'}",
                    "numerator_coefficients_low_degree_first": [
                        encode(value) for value in numerator
                    ],
                    "maximal_base_factor_power": first_nonzero,
                    "residual": strict,
                }
            )
        selected_sign, selected = max(
            wall_records,
            key=lambda item: next(
                index for index, coefficient in enumerate(item[1]) if not coefficient.is_zero()
            ),
        )
        declared_sigma = -sigma if inputs.sign_label_swap else sigma
        if selected_sign != -declared_sigma:
            raise ValueError("the derived R4/R5 tied wall-feature label map drifted")
        selected_residual = selected[2:]
        if poly_scale(selected_residual, q(2)) != (q(2), q(1)):
            raise ValueError("the selected wall feature lacks primitive residual u+2")
        other = next(numerator for label, numerator in wall_records if label != selected_sign)
        if poly_add(field, other, poly_scale(selected, -q(1))) != (q(0), q(4)):
            raise ValueError("the other tied wall feature does not add exact 4u slack")
        derived_small_labels.append(f"wall:1:{wall}:{'+' if selected_sign > 0 else '-'}")
    return {
        "derived_features": records,
        "derived_small_slack_labels": derived_small_labels,
        "selected_primitive_residual": "u+2",
        "other_feature_additional_slack": "4u/(4+u^2)",
        "strict_only_for_u_positive": True,
    }


def universal_sign_table(
    field: NumberField,
    stratum: str,
    direction: list[FieldElement],
    interval_end: FieldElement,
    inputs: ProofInputs,
) -> list[dict[str, object]]:
    q = field.rational
    side = cast(FieldElement, face.exact_data(field)["side"])
    starts = tangent_cones.centres_for_stratum(field, stratum)
    denominator = tuple(q(value) for value in DENOMINATOR)
    centres = [
        (
            affine_numerator(field, point[0], direction[tangent_cones.x(index)]),
            affine_numerator(field, point[1], direction[tangent_cones.y(index)]),
        )
        for index, point in enumerate(starts)
    ]
    records: list[dict[str, object]] = []

    def retain(label: str, numerator: Poly) -> None:
        if label == "wall:1:x-upper" and inputs.numerator_shift:
            numerator = poly_add(field, numerator, (q(inputs.numerator_shift) / 1000,))
        coefficients = bernstein_coefficients(field, numerator, interval_end)
        pieces = certify_nonnegative(coefficients, field)
        records.append(
            {
                "label": label,
                "numerator_coefficients_low_degree_first": [
                    encode(value) for value in numerator
                ],
                "denominator": "4+u^2",
                "bernstein_subinterval_count": pieces,
                "nonnegative_on_full_interval": True,
                "identically_zero": all(value.is_zero() for value in numerator),
            }
        )

    for index, (x_numerator, y_numerator) in enumerate(centres):
        if index == 1:
            support_x = support_y = square1_support_numerator(field, (q(1), q(0)))
        else:
            support = constant_support(field, index, (q(1), q(0)))
            support_x = support_y = poly_scale(denominator, support)
        retain(
            f"wall:{index}:x-lower", poly_add(field, x_numerator, poly_scale(support_x, -q(1)))
        )
        retain(
            f"wall:{index}:x-upper",
            poly_add(
                field,
                poly_scale(denominator, side),
                poly_scale(x_numerator, -q(1)),
                poly_scale(support_x, -q(1)),
            ),
        )
        retain(
            f"wall:{index}:y-lower", poly_add(field, y_numerator, poly_scale(support_y, -q(1)))
        )
        retain(
            f"wall:{index}:y-upper",
            poly_add(
                field,
                poly_scale(denominator, side),
                poly_scale(y_numerator, -q(1)),
                poly_scale(support_y, -q(1)),
            ),
        )

    h = (q(1) + field.alpha) / 2
    pair_specs = (
        (0, 1, q(1), q(0), -1),
        (0, 2, q(0), q(1), 1),
        (0, 3, q(1), q(0), -1),
        (0, 4, -field.alpha / 2, field.alpha / 2, 1),
        (1, 2, q(1), q(0), 1),
        (1, 3, q(0), q(1), -1),
        (1, 4, -field.alpha / 2, field.alpha / 2, -1),
        (2, 3, field.alpha / 2, field.alpha / 2, -1),
        (2, 4, field.alpha / 2, field.alpha / 2, -1),
        (3, 4, field.alpha / 2, field.alpha / 2, 1),
    )
    del h
    for first, second, ax, ay, cell_sign in pair_specs:
        axis = (ax, ay)
        displacement = poly_add(
            field,
            poly_scale(centres[second][0], ax),
            poly_scale(centres[second][1], ay),
            poly_scale(centres[first][0], -ax),
            poly_scale(centres[first][1], -ay),
        )
        separation = poly_scale(displacement, q(-cell_sign))
        supports: list[Poly] = []
        for square_index in (first, second):
            if square_index == 1:
                supports.append(square1_support_numerator(field, axis))
            else:
                supports.append(
                    poly_scale(denominator, constant_support(field, square_index, axis))
                )
        retain(
            f"pair:{first}-{second}",
            poly_add(field, separation, *(poly_scale(value, -q(1)) for value in supports)),
        )
    if inputs.bad_sign_probe:
        bad = poly_mul(
            field,
            (-interval_end / 2, q(1)),
            (-interval_end, q(1)),
        )
        samples = [
            poly_value(field, bad, value)
            for value in (q(0), interval_end / 2, interval_end)
        ]
        if any(value.sign() < 0 for value in samples):
            raise ValueError("the anti-sampling probe does not pass its declared samples")
        retain("control:p_bad", bad)
    if len(records) != 30:
        raise ValueError("the universal table does not contain twenty walls and ten pairs")
    return records


def rotating_squares(
    field: NumberField,
    centres: list[tuple[FieldElement, FieldElement]],
    sigma: int,
    u: FieldElement,
) -> list[tuple[tuple[FieldElement, FieldElement], ...]]:
    q = field.rational
    denominator = q(4) + u * u
    c = (q(4) - u * u) / denominator
    s = q(sigma) * q(4) * u / denominator
    r = field.alpha
    axes = (
        ((q(1), q(0)), (q(0), q(1))),
        ((c, s), (-s, c)),
        ((q(1), q(0)), (q(0), q(1))),
        ((r / 2, r / 2), (-r / 2, r / 2)),
        ((r / 2, r / 2), (-r / 2, r / 2)),
    )
    return [
        tuple(
            (
                centre[0] + sx * first[0] / 2 + sy * second[0] / 2,
                centre[1] + sx * first[1] / 2 + sy * second[1] / 2,
            )
            for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))
        )
        for centre, (first, second) in zip(centres, axes, strict=True)
    ]


def axis_numerators(
    field: NumberField, square_index: int, sigma: int
) -> tuple[tuple[Poly, Poly, str], ...]:
    q = field.rational
    denominator = tuple(q(value) for value in DENOMINATOR)
    if square_index == 1:
        cosine = (q(4), q(0), -q(1))
        sine = (q(0), q(4 * sigma))
        return (
            (cosine, sine, "x"),
            (poly_scale(sine, -q(1)), cosine, "y"),
        )
    return tuple(
        (poly_scale(denominator, x), poly_scale(denominator, y), name)
        for x, y, name in tangent_cones.orientation_axes(field)[square_index]
    )


def zero_axis_exhaustion(  # noqa: PLR0917 -- mirrors the frozen case inputs
    field: NumberField,
    stratum: str,
    direction: list[FieldElement],
    sigma: int,
    interval_end: FieldElement,
    inputs: ProofInputs,
) -> dict[str, object]:
    q = field.rational
    starts = tangent_cones.centres_for_stratum(field, stratum)
    centres = [
        (
            affine_numerator(field, point[0], direction[tangent_cones.x(index)]),
            affine_numerator(field, point[1], direction[tangent_cones.y(index)]),
        )
        for index, point in enumerate(starts)
    ]
    axes = [axis_numerators(field, index, sigma) for index in range(5)]
    gaps: list[dict[str, object]] = []
    base_zero_axes: set[str] = set()
    path_zero_axes: set[str] = set()
    for first in range(5):
        for second in range(first + 1, 5):
            displacement = (
                poly_add(field, centres[second][0], poly_scale(centres[first][0], -q(1))),
                poly_add(field, centres[second][1], poly_scale(centres[first][1], -q(1))),
            )
            for owner in (first, second):
                for axis_x, axis_y, axis_name in axes[owner]:
                    projection = poly_add(
                        field,
                        poly_mul(field, displacement[0], axis_x),
                        poly_mul(field, displacement[1], axis_y),
                    )
                    separation = exact_absolute_poly(field, projection, interval_end)
                    support_poly: Poly = (field.zero,)
                    for square_index in (first, second):
                        for basis_x, basis_y, _basis_name in axes[square_index]:
                            dot = poly_add(
                                field,
                                poly_mul(field, axis_x, basis_x),
                                poly_mul(field, axis_y, basis_y),
                            )
                            support_poly = poly_add(
                                field,
                                support_poly,
                                poly_scale(
                                    exact_absolute_poly(field, dot, interval_end), q(1) / 2
                                ),
                            )
                    gap = poly_add(field, separation, poly_scale(support_poly, -q(1)))
                    label = f"{first}-{second}:owner{owner}:{axis_name}"
                    is_zero = all(value.is_zero() for value in gap)
                    base_zero = gap[0].is_zero()
                    residual_sign: int | None = None
                    if base_zero:
                        base_zero_axes.add(label)
                    if is_zero:
                        path_zero_axes.add(label)
                        first_nonzero: int | None = None
                        residual_certificate: dict[str, object] | None = None
                    else:
                        first_nonzero = next(
                            index
                            for index, coefficient in enumerate(gap)
                            if not coefficient.is_zero()
                        )
                        residual = gap[first_nonzero:]
                        residual_sign = residual[0].sign()
                        if residual_sign == 0:
                            raise ValueError("a maximal base factor left a zero residual")
                        signed_residual = poly_scale(residual, q(residual_sign))
                        try:
                            residual_certificate = strict_polynomial_certificate(
                                field, signed_residual, interval_end
                            )
                        except ValueError as error:
                            raise ValueError(
                                f"owner-axis {label} lacks a strict residual certificate: "
                                f"{[encode(value) for value in residual]}"
                            ) from error
                    gaps.append(
                        {
                            "label": label,
                            "gap_numerator_coefficients_low_degree_first": [
                                encode(value) for value in gap
                            ],
                            "zero_at_base": base_zero,
                            "identically_zero": is_zero,
                            "maximal_base_factor_power": first_nonzero,
                            "residual_sign": residual_sign,
                            "strict_residual": residual_certificate,
                        }
                    )
    declared_base = set(BASE_ZERO_AXES)
    declared_path = set(PATH_ZERO_AXES)
    if inputs.removed_base_zero_axis is not None:
        declared_base.remove(inputs.removed_base_zero_axis)
    if inputs.added_path_zero_axis is not None:
        declared_path.add(inputs.added_path_zero_axis)
    if base_zero_axes != declared_base:
        raise ValueError("the exact base-point zero-axis inventory drifted")
    if path_zero_axes != declared_path:
        raise ValueError("the exact pathwise zero-axis inventory drifted")
    if len(gaps) != 40:
        raise ValueError("the owner-axis inventory is not the expected forty cases")
    return {
        "declared_base_zero_axes": sorted(declared_base),
        "exact_base_zero_axes": sorted(base_zero_axes),
        "declared_pathwise_zero_axes": sorted(declared_path),
        "exact_pathwise_zero_axes": sorted(path_zero_axes),
        "all_forty_owner_axes": gaps,
        "exhausted": True,
    }


def exact_fixture(
    field: NumberField,
    stratum: str,
    direction: list[FieldElement],
    sigma: int,
    u: FieldElement,
) -> dict[str, object]:
    centres = centres_at(field, stratum, direction, u)
    report = verify_packing(
        rotating_squares(field, centres, sigma, u),
        cast(FieldElement, face.exact_data(field)["side"]),
        sign=exact_sign,
    )
    if not report.valid:
        raise ValueError("an independent rotating exact fixture is invalid")
    return {
        "u": encode(u),
        "valid": True,
        "pairs_tested": report.pairs_tested,
        "touching_pairs": report.touching_pairs,
        "strict_pairs": report.strict_pairs,
        "container_contacts": report.container_contacts,
    }


def branch_stresses(
    field: NumberField,
    stratum: str,
    direction: list[FieldElement],
    interval_end: FieldElement,
    inputs: ProofInputs,
) -> list[dict[str, object]]:
    if set(inputs.owners) != set(OWNERS) or len(inputs.owners) != 2:
        raise ValueError("both owner branches are required")
    if not inputs.include_all_tied_features:
        raise ValueError("each owner branch requires both tied support features")
    stress_inputs = fixed_angle_polytope.ProofInputs(
        owner3_wplus_shift_numerator=inputs.stress_shift,
        owners=inputs.owners,
    )
    identities = [
        fixed_angle_polytope.stress_polynomial_certificate(
            field,
            stratum,
            direction,
            "R3",
            interval_end,
            owner,
            stress_inputs,
        )
        for owner in inputs.owners
    ]
    q = field.rational
    r = field.alpha
    for identity in identities:
        labels = cast(list[str], identity["stable_tied_row_labels"])
        owner = labels[-1].split(":")[2]
        owner_name = "owner3:a+" if owner == "owner3" else "owner4:a+"
        weight_polynomials: list[Poly] = []
        for label in labels:
            if label.startswith("wall:2:"):
                weight_polynomials.append((r / 4,))
            elif label.startswith("wall:3:"):
                weight_polynomials.append((r / 2,))
            elif label.startswith("contact:2-4:"):
                weight_polynomials.append((q(1),))
            elif owner_name == "owner3:a+" and label.endswith("feature+1"):
                weight_polynomials.append(
                    (q(5) / 4 - r / 2 + q(inputs.stress_shift) / 1000, -r / 2)
                )
            elif owner_name == "owner3:a+":
                weight_polynomials.append((-q(1) / 4 + r / 2, r / 2))
            else:
                weight_polynomials.append((q(1) / 2,))
        bounds: list[dict[str, object]] = []
        for label, polynomial in zip(
            labels, weight_polynomials, strict=True
        ):
            start = poly_value(field, polynomial, q(0))
            end = poly_value(field, polynomial, interval_end)
            lower = start if (start - end).sign() <= 0 else end
            if lower.sign() <= 0:
                raise ValueError(
                    "a full-interval stress multiplier lower bound is not positive"
                )
            excess = poly_add(field, polynomial, (-lower,))
            certify_nonnegative(bernstein_coefficients(field, excess, interval_end), field)
            bounds.append(
                {
                    "row_label": label,
                    "affine_coefficients_low_degree_first": [
                        encode(value) for value in polynomial
                    ],
                    "exact_full_interval_lower_bound": encode(lower),
                    "strictly_positive_on_full_interval": True,
                }
            )
        identity["multiplier_lower_bounds"] = bounds
        identity["all_multipliers_strictly_positive_on_full_interval"] = True
    return identities


def sign_guards(field: NumberField, interval_end: FieldElement) -> dict[str, dict[str, object]]:
    q = field.rational
    guards = {
        "4-u^2": (q(4), q(0), -q(1)),
        "4-4u-u^2": (q(4), -q(4), -q(1)),
    }
    result: dict[str, dict[str, object]] = {}
    for label, polynomial in guards.items():
        coefficients = bernstein_coefficients(field, polynomial, interval_end)
        result[label] = {
            "coefficients_low_degree_first": [encode(value) for value in polynomial],
            "bernstein_subinterval_count": certify_nonnegative(coefficients, field),
            "strictly_positive_on_interval": all(value.sign() > 0 for value in coefficients),
        }
        if result[label]["strictly_positive_on_interval"] is not True:
            raise ValueError("a rational half-angle feature-sign guard is not strict")
    return result


def positive_path_controls(field: NumberField) -> list[dict[str, object]]:
    delta = 3 * field.alpha / 2 - 2
    inputs = fixed_angle_polytope.ProofInputs()
    records: list[dict[str, object]] = []
    for stratum in STRATA:
        interval_end = delta / 2 if stratum == "interior" else delta
        for name in ("R3", "R6"):
            direction = fixed_angle_polytope.path_direction(field, stratum, name, inputs)
            centres = centres_at(field, stratum, direction, interval_end)
            report = face.exact_packing_valid(
                field, centres, cast(FieldElement, face.exact_data(field)["side"])
            )
            if report["valid"] is not True:
                raise ValueError("an exp-039 positive path control is invalid")
            records.append(
                {
                    "stratum": stratum,
                    "class": name,
                    "u": encode(interval_end),
                    **report,
                }
            )
    return records


def feasibility_case_certificate(
    field: NumberField,
    class_name: str,
    sigma: int,
    stratum: str,
    inputs: ProofInputs,
) -> dict[str, object]:
    q = field.rational
    delta = 3 * field.alpha / 2 - 2
    interval_end = delta / 2
    if stratum == "interior":
        interval_end *= inputs.interior_interval_multiplier
    direction = position_direction(field, stratum, inputs)
    _lineality, _sheet, rays, _kind = tangent_inventory.geometry_vectors(field, stratum)
    expected_name = "R5" if inputs.sign_label_swap and class_name == "R4" else class_name
    expected = rays[expected_name]
    derivative = list(direction)
    derivative[tangent_cones.theta(1)] = q(sigma)
    if derivative != expected:
        raise ValueError("the rotating derivative does not match its exp-038 representative")
    midpoint = [(left + right) / 2 for left, right in zip(rays["R3"], rays["R6"], strict=True)]
    if direction != midpoint:
        raise ValueError("the center path is not the exp-039 R3/R6 midpoint")
    denominator = (q(4), q(0), q(1))
    cosine = (q(4), q(0), -q(1))
    sine = (q(0), q(4 * sigma + inputs.orientation_unit_shift))
    unit_identity = poly_add(
        field,
        poly_mul(field, cosine, cosine),
        poly_mul(field, sine, sine),
        poly_scale(poly_mul(field, denominator, denominator), -q(1)),
    )
    if any(not value.is_zero() for value in unit_identity):
        raise ValueError("the rational half-angle orientation is not exactly unit")
    table = universal_sign_table(field, stratum, direction, interval_end, inputs)
    zero_axes = zero_axis_exhaustion(field, stratum, direction, sigma, interval_end, inputs)
    if inputs.false_active_slack:
        claimed_path_axes = set(cast(list[str], zero_axes["exact_pathwise_zero_axes"]))
        claimed_path_axes.add("1-4:owner4:a-")
        if claimed_path_axes != PATH_ZERO_AXES:
            raise ValueError("the base-only contact was falsely claimed pathwise active")
    return {
        "class": class_name,
        "sigma": sigma,
        "stratum": stratum,
        "interval": {"lower": encode(q(0)), "upper": encode(interval_end)},
        "derivative": tangent_inventory.encode_vector(derivative),
        "center_path_is_R3_R6_midpoint": True,
        "denominator_certificate": denominator_certificate(field, interval_end),
        "half_angle_sign_guards": sign_guards(field, interval_end),
        "unit_orientation_identity": {
            "identity": "(4-u^2)^2+(4u)^2=(4+u^2)^2",
            "numerator_coefficients_low_degree_first": [
                encode(value) for value in unit_identity
            ],
        },
        "universal_sign_table": table,
        "fixtures": [
            exact_fixture(field, stratum, direction, sigma, interval_end / 2),
            exact_fixture(field, stratum, direction, sigma, interval_end),
        ],
        "owner_feature_branches": {
            "owner3:a+": ["square4-feature+1", "square4-feature-1"],
            "owner4:a+": ["square3-feature+1", "square3-feature-1"],
        },
        "zero_axis_exhaustion": zero_axes,
        "derived_wall_features": square1_wall_feature_certificate(
            field, stratum, direction, sigma, interval_end, inputs
        ),
    }


def proof_core(field: NumberField, inputs: ProofInputs) -> dict[str, object]:
    if set(inputs.signs) != set(SIGNS) or len(inputs.signs) != 2:
        raise ValueError("both rotating signs are required")
    if set(inputs.strata) != set(STRATA) or len(inputs.strata) != 3:
        raise ValueError("all three strata are required")
    if inputs.promoted_claim is not None:
        raise ValueError("the requested claim lies outside the frozen scope")
    feasibility_cases = [
        feasibility_case_certificate(field, class_name, sigma, stratum, inputs)
        for class_name, sigma in inputs.signs
        for stratum in inputs.strata
    ]
    if len(feasibility_cases) != 6:
        raise ValueError("the rotating path inventory is not exactly six cases")
    stress_cases = []
    for class_name, sigma in inputs.signs:
        for stratum in inputs.strata:
            direction = position_direction(field, stratum, inputs)
            interval_end = (3 * field.alpha / 2 - 2) / 2
            if stratum == "interior":
                interval_end *= inputs.interior_interval_multiplier
            stress_cases.append(
                {
                    "class": class_name,
                    "sigma": sigma,
                    "stratum": stratum,
                    "owner_identities": branch_stresses(
                        field, stratum, direction, interval_end, inputs
                    ),
                }
            )
    return {
        "feasibility": {"cases": feasibility_cases, "case_count": 6, "criterion_met": True},
        "stress": {"cases": stress_cases, "case_count": 6, "criterion_met": True},
    }


def mutation_rejected(field: NumberField, inputs: ProofInputs) -> bool:
    try:
        proof_core(field, inputs)
    except TypeError, ValueError:
        return True
    return False


def controls(field: NumberField) -> dict[str, bool]:
    base = ProofInputs()
    mutations = {
        "non_unit_orientation_rejected": replace(base, orientation_unit_shift=1),
        "sign_label_swap_rejected": replace(base, sign_label_swap=True),
        "missing_A_slide_rejected": replace(base, add_a_slide=False),
        "added_B_slide_rejected": replace(base, add_b_slide=True),
        "changed_square1_displacement_rejected": replace(base, dx1_numerator=0),
        "changed_square4_displacement_rejected": replace(base, dx4_numerator=0),
        "false_midpoint_identity_rejected": replace(base, midpoint_shift_numerator=1),
        "missing_R4_rejected": replace(base, signs=(SIGNS[1],)),
        "missing_R5_rejected": replace(base, signs=(SIGNS[0],)),
        "missing_stratum_rejected": replace(base, strata=STRATA[:2]),
        "missing_owner_rejected": replace(base, owners=(OWNERS[0],)),
        "missing_tied_feature_rejected": replace(base, include_all_tied_features=False),
        "sampled_only_rejected": replace(base, bad_sign_probe=True),
        "perturbed_numerator_rejected": replace(base, numerator_shift=-1),
        "perturbed_stress_rejected": replace(base, stress_shift=1),
        "false_active_slack_rejected": replace(base, false_active_slack=True),
        "overlong_interior_interval_rejected": replace(base, interior_interval_multiplier=2),
        "missing_zero_axis_rejected": replace(
            base, removed_base_zero_axis="0-4:owner4:a-"
        ),
        "extra_zero_axis_rejected": replace(
            base, added_path_zero_axis="1-4:owner4:a-"
        ),
        "scope_promotion_rejected": replace(base, promoted_claim="terminal"),
    }
    if set(mutations) != CONTROL_KEYS or len(mutations) != 20:
        raise ValueError("the exact twenty-key semantic control contract drifted")
    result = {name: mutation_rejected(field, mutation) for name, mutation in mutations.items()}
    if set(result) != CONTROL_KEYS:
        raise ValueError("the executed semantic control keys drifted")
    return result


def build_result() -> dict[str, object]:
    field = face.make_field()
    result: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "contract": "packing.squares:N5RotatingReleasePaths/v1",
        "field": "Q(sqrt(2)), sqrt(2) in (1,2)",
        "sources": source_bindings(field),
        "certificates": proof_core(field, ProofInputs()),
        "positive_controls": positive_path_controls(field),
        "scope_refusals": {"refused_claims": list(REFUSED_CLAIMS), "all_refused": True},
        "determinations": {
            "feasibility": {
                "outcome": "criterion_met",
                "claim": "six explicit R4/R5 paths are feasible Bouligand tangents",
            },
            "stress": {
                "outcome": "criterion_met",
                "claim": "both owner branches have positive pathwise first-order stresses",
            },
            "round": {
                "outcome": "criterion_met",
                "scope": "six pathwise Bouligand tangents and first-order no descent only",
            },
        },
    }
    result["controls"] = controls(field)
    control_values = require_dict(result["controls"], "controls")
    if not all(control_values.values()):
        raise ValueError(f"a preregistered control survived: {control_values}")
    return result


def write_json_atomic(path: Path, value: dict[str, object]) -> None:
    with atomic_output_file(path, make_parents=True) as temporary:
        temporary.write_text(
            json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )


def require_same(retained: object, regenerated: dict[str, object]) -> None:
    if retained != regenerated:
        raise ValueError("retained rotating-release result differs from exact regeneration")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--record", type=Path)
    group.add_argument("--replay", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result = build_result()
        if args.record is not None:
            write_json_atomic(args.record, result)
        else:
            retained = json.loads(args.replay.read_text(encoding="utf-8"))
            require_same(retained, result)
        control_values = require_dict(result["controls"], "controls")
        print(json.dumps({"status": "PASS", "cases": 6, "controls": len(control_values)}))
    except (OSError, TypeError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    else:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
