"""Behavior tests for exact second-order packing-feature jets."""

from __future__ import annotations

import itertools

import pytest

from cases.n5 import equal_side_face as face
from cases.n5 import tangent_cones, tangent_inventory
from sqpack.field import FieldElement, NumberField
from sqpack.research.exact_jets import (
    SecondOrderJet,
    Taylor2,
    linear_combination,
    sat_gap,
    signed_support,
    wall_gap,
)

type JetVector = tuple[SecondOrderJet, ...]


def _dot(left: JetVector, right: JetVector) -> SecondOrderJet:
    result = left[0] * right[0]
    for left_value, right_value in zip(left[1:], right[1:], strict=True):
        result += left_value * right_value
    return result


def _constant_vector(values: tuple[FieldElement, FieldElement], dimension: int) -> JetVector:
    return tuple(SecondOrderJet.constant(value, dimension) for value in values)


def _support_sign_options(
    axis: JetVector,
    generators: tuple[JetVector, ...],
    square_index: int,
) -> tuple[tuple[tuple[int, ...], tuple[str, ...]], ...]:
    options: list[tuple[tuple[int, ...], tuple[str, ...]]] = [((), ())]
    for generator in generators:
        projection = _dot(axis, generator)
        base_sign = projection.value.sign()
        if base_sign != 0:
            choices: tuple[tuple[int, str | None], ...] = ((base_sign, None),)
        elif any(not value.is_zero() for value in projection.gradient):
            choices = tuple(
                (sign, f"square{square_index}-feature{sign:+d}") for sign in (-1, 1)
            )
        else:
            choices = ((1, None),)
        options = [
            (
                (*signs, sign),
                suffixes if suffix is None else (*suffixes, suffix),
            )
            for signs, suffixes in options
            for sign, suffix in choices
        ]
    return tuple(options)


def _pose_jets(
    field: NumberField, stratum: str
) -> tuple[
    list[JetVector],
    list[tuple[JetVector, ...]],
    list[tuple[str, ...]],
]:
    dimension = tangent_cones.VARIABLE_COUNT
    centers = tangent_cones.centres_for_stratum(field, stratum)
    center_jets = [
        (
            SecondOrderJet.variable(center[0], dimension, tangent_cones.x(index)),
            SecondOrderJet.variable(center[1], dimension, tangent_cones.y(index)),
        )
        for index, center in enumerate(centers)
    ]
    frames: list[tuple[JetVector, ...]] = []
    frame_names: list[tuple[str, ...]] = []
    for index, axes in enumerate(tangent_cones.orientation_axes(field)):
        angle_increment = SecondOrderJet.variable(
            field.zero, dimension, tangent_cones.theta(index)
        )
        frames.append(
            tuple(
                SecondOrderJet.rotation((axis_x, axis_y), angle_increment)
                for axis_x, axis_y, _axis_name in axes
            )
        )
        frame_names.append(tuple(axis_name for _axis_x, _axis_y, axis_name in axes))
    return center_jets, frames, frame_names


def _generated_n5_rows(field: NumberField, stratum: str) -> dict[str, SecondOrderJet]:
    dimension = tangent_cones.VARIABLE_COUNT
    center_jets, frames, frame_names = _pose_jets(field, stratum)
    side = face.exact_data(field)["side"]
    if not isinstance(side, FieldElement):
        raise TypeError("the exact n=5 side is not a field element")
    q = field.rational
    wall_specs = (
        ("x-lower", q(0), (q(-1), q(0))),
        ("x-upper", side, (q(1), q(0))),
        ("y-lower", q(0), (q(0), q(-1))),
        ("y-upper", side, (q(0), q(1))),
    )
    generated: dict[str, SecondOrderJet] = {}
    for square_index in range(5):
        for wall_name, offset_value, normal_value in wall_specs:
            normal = _constant_vector(normal_value, dimension)
            offset = SecondOrderJet.constant(offset_value, dimension)
            options = _support_sign_options(normal, frames[square_index], square_index)
            for feature_signs, _suffixes in options:
                gap = wall_gap(
                    offset,
                    normal,
                    center_jets[square_index],
                    frames[square_index],
                    feature_signs,
                )
                if not gap.value.is_zero():
                    continue
                label = f"wall:{square_index}:{wall_name}"
                if len(options) > 1:
                    angle_sign = gap.gradient[tangent_cones.theta(square_index)].sign()
                    if angle_sign == 0:
                        raise AssertionError("an active tied wall has no angle derivative")
                    label = f"{label}:{'+' if angle_sign > 0 else '-'}"
                generated[label] = gap

    for first, second in itertools.combinations(range(5), 2):
        for owner in (first, second):
            for axis, axis_name in zip(frames[owner], frame_names[owner], strict=True):
                separation = _dot(
                    axis,
                    tuple(
                        right - left
                        for left, right in zip(
                            center_jets[first], center_jets[second], strict=True
                        )
                    ),
                )
                separation_sign = separation.value.sign()
                if separation_sign == 0:
                    continue
                first_options = _support_sign_options(axis, frames[first], first)
                second_options = _support_sign_options(axis, frames[second], second)
                for (first_signs, first_suffixes), (
                    second_signs,
                    second_suffixes,
                ) in itertools.product(first_options, second_options):
                    gap = sat_gap(
                        axis,
                        first_center=center_jets[first],
                        second_center=center_jets[second],
                        first_generators=frames[first],
                        second_generators=frames[second],
                        separation_sign=separation_sign,
                        first_feature_signs=first_signs,
                        second_feature_signs=second_signs,
                    )
                    if not gap.value.is_zero():
                        continue
                    label = f"contact:{first}-{second}:owner{owner}:{axis_name}"
                    suffixes = (*first_suffixes, *second_suffixes)
                    if suffixes:
                        label = f"{label}:{':'.join(suffixes)}"
                    generated[label] = gap
    return generated


def test_product_keeps_center_angle_cross_term_and_scales_quadratically() -> None:
    field = NumberField((1, 0, -2), (1, 2))
    q = field.rational
    center_coordinate = SecondOrderJet.variable(q(0), 2, 0)
    angle_increment = SecondOrderJet.variable(q(0), 2, 1)
    _, rotating_axis_y = SecondOrderJet.rotation((q(1), q(0)), angle_increment)
    center_axis_projection = center_coordinate * rotating_axis_y

    zero_correction = (q(0), q(0))
    baseline = center_axis_projection.substitute((q(2), q(3)), zero_correction)
    scaled = center_axis_projection.substitute((q(4), q(6)), zero_correction)

    assert baseline == Taylor2(q(0), q(0), q(6))
    assert scaled.quadratic == 4 * baseline.quadratic
    assert center_coordinate.product(rotating_axis_y) == center_axis_projection
    assert center_axis_projection + center_axis_projection - center_axis_projection == (
        center_axis_projection
    )
    assert -center_axis_projection == center_axis_projection.scale(q(-1))


def test_rotation_preserves_unit_length_and_path_coefficient_convention() -> None:
    field = NumberField((1, 0, -2), (1, 2))
    q = field.rational
    angle_increment = SecondOrderJet.variable(q(0), 1, 0)
    axis_x, axis_y = SecondOrderJet.rotation((q(1), q(0)), angle_increment)

    unit_length = axis_x * axis_x + axis_y * axis_y
    assert unit_length == SecondOrderJet.constant(q(1), 1)

    velocity = (q(3),)
    quadratic_correction = (q(5),)
    assert axis_x.substitute(velocity, quadratic_correction) == Taylor2(q(1), q(0), -q(9) / 2)
    assert axis_y.substitute(velocity, quadratic_correction) == Taylor2(q(0), q(3), q(5))

    coordinate = SecondOrderJet.variable(q(7), 1, 0)
    assert coordinate.substitute(velocity, quadratic_correction) == Taylor2(q(7), q(3), q(5))
    assert (coordinate * coordinate).substitute(velocity, quadratic_correction).quadratic == q(
        79
    )


def test_support_requires_explicit_valid_signs_and_caller_emits_tied_alternatives() -> None:
    field = NumberField((1, 0, -2), (1, 2))
    q = field.rational
    angle_increment = SecondOrderJet.variable(q(0), 1, 0)
    axis = SecondOrderJet.rotation((q(1), q(0)), angle_increment)
    zero = SecondOrderJet.constant(q(0), 1)
    one = SecondOrderJet.constant(q(1), 1)
    tied_generator = ((zero, one),)

    alternatives = tuple(
        signed_support(axis, tied_generator, (feature_sign,)) for feature_sign in (-1, 1)
    )
    negative = alternatives[0].substitute((q(1),), (q(0),))
    positive = alternatives[1].substitute((q(1),), (q(0),))

    assert len(alternatives) == 2
    assert negative.linear == -q(1) / 2
    assert positive.linear == q(1) / 2
    assert isinstance(signed_support(axis, tied_generator, (1,)), SecondOrderJet)

    with pytest.raises(ValueError, match="exactly -1 or \\+1"):
        signed_support(axis, tied_generator, (0,))
    with pytest.raises(ValueError, match="one explicit feature sign"):
        signed_support(axis, tied_generator, ())


def test_wall_and_sat_gaps_respond_to_path_and_branch_mutations() -> None:
    field = NumberField((1, 0, -2), (1, 2))
    q = field.rational
    zero = SecondOrderJet.constant(q(0), 1)
    one = SecondOrderJet.constant(q(1), 1)
    two = SecondOrderJet.constant(q(2), 1)
    half_edge_x = (one, zero)
    half_edge_y = (zero, one)
    generators = (half_edge_x, half_edge_y)
    normal = (one, zero)
    moving_x = SecondOrderJet.variable(q(1), 1, 0)

    wall = wall_gap(two, normal, (moving_x, zero), generators, (1, 1))
    assert wall.substitute((q(1),), (q(2),)) == Taylor2(q(1) / 2, q(-1), q(-2))

    first_center = (zero, zero)
    second_center = (two, zero)
    separated = sat_gap(
        normal,
        first_center=first_center,
        second_center=second_center,
        first_generators=generators,
        second_generators=generators,
        separation_sign=1,
        first_feature_signs=(1, 1),
        second_feature_signs=(1, 1),
    )
    assert separated.value == q(1)
    with pytest.raises(ValueError, match="nonzero base separation"):
        sat_gap(
            normal,
            first_center=first_center,
            second_center=second_center,
            first_generators=generators,
            second_generators=generators,
            separation_sign=-1,
            first_feature_signs=(1, 1),
            second_feature_signs=(1, 1),
        )
    with pytest.raises(ValueError, match="nonzero base projection"):
        sat_gap(
            normal,
            first_center=first_center,
            second_center=second_center,
            first_generators=generators,
            second_generators=generators,
            separation_sign=1,
            first_feature_signs=(-1, 1),
            second_feature_signs=(-1, 1),
        )
    with pytest.raises(ValueError, match="exactly -1 or \\+1"):
        sat_gap(
            normal,
            first_center=first_center,
            second_center=second_center,
            first_generators=generators,
            second_generators=generators,
            separation_sign=0,
            first_feature_signs=(1, 1),
            second_feature_signs=(1, 1),
        )


def test_linear_combination_cancels_corrections_only_when_gradient_cancels() -> None:
    field = NumberField((1, 0, -2), (1, 2))
    q = field.rational
    coordinate = SecondOrderJet.variable(q(1), 1, 0)
    square = coordinate * coordinate
    negative_linear = coordinate.scale(q(-2))

    eliminated = linear_combination((q(1), q(1)), (square, negative_linear))
    first_correction = eliminated.substitute((q(3),), (q(5),))
    second_correction = eliminated.substitute((q(3),), (q(17),))

    assert eliminated.gradient == (q(0),)
    assert first_correction.quadratic == q(9)
    assert second_correction.quadratic == first_correction.quadratic

    mutated_weight = linear_combination((q(1), q(1) / 2), (square, negative_linear))
    mutated_first = mutated_weight.substitute((q(3),), (q(5),))
    mutated_second = mutated_weight.substitute((q(3),), (q(17),))
    assert mutated_weight.gradient == (q(1),)
    assert mutated_second.quadratic - mutated_first.quadratic == q(12)


def test_n5_wall_and_contact_gradients_match_authoritative_source_rows() -> None:
    field = NumberField((1, 0, -2), (1, 2))
    for stratum in tangent_cones.STRATA:
        generated = _generated_n5_rows(field, stratum)
        walls = {label: jet for label, jet in generated.items() if label.startswith("wall:")}
        contacts = {
            label: jet for label, jet in generated.items() if label.startswith("contact:")
        }
        for owner in tangent_cones.EXPECTED_CONTACT_BRANCHES:
            expected_rows = tangent_inventory.matrix(field, stratum, owner)
            expected = {row.label: row.coefficients for row in expected_rows}
            selected = {
                **walls,
                **{
                    label: jet
                    for label, jet in contacts.items()
                    if not label.startswith("contact:3-4:")
                    or label.startswith(f"contact:3-4:{owner}:")
                },
            }
            assert selected.keys() == expected.keys()
            assert {label: jet.gradient for label, jet in selected.items()} == expected
