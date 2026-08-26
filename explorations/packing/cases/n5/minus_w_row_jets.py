"""Build exact second-order wall and SAT row jets for the n=5 source poses.

This module owns only the case-level geometry-to-jet translation.  It validates the
result against the authoritative first-order inventories, but does not choose stress
weights, substitute a research direction, route asymptotic scales, or decide an
obstruction.
"""

from __future__ import annotations

import itertools

from cases.n5 import equal_side_face as face
from cases.n5 import tangent_cones, tangent_inventory
from sqpack.field import FieldElement, NumberField
from sqpack.research.exact_jets import SecondOrderJet, sat_gap, wall_gap

type JetVector = tuple[SecondOrderJet, ...]
type RowJetMap = dict[str, SecondOrderJet]


def _dot(left: JetVector, right: JetVector) -> SecondOrderJet:
    if len(left) != len(right) or not left:
        raise ValueError("jet vectors must have the same positive dimension")
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
        elif any(not value.is_zero() for value in projection.gradient) or any(
            not value.is_zero() for row in projection.hessian for value in row
        ):
            choices = tuple(
                (sign, f"square{square_index}-feature{sign:+d}") for sign in (-1, 1)
            )
        else:
            choices = ((1, None),)
        options = [
            ((*signs, sign), suffixes if suffix is None else (*suffixes, suffix))
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


def _insert(rows: RowJetMap, label: str, jet: SecondOrderJet) -> None:
    if label in rows:
        raise ValueError(f"duplicate generated row label {label}")
    rows[label] = jet


def active_row_jets(field: NumberField, stratum: str) -> RowJetMap:
    """Construct every active wall and SAT row at one registered source stratum."""
    if stratum not in tangent_cones.STRATA:
        raise ValueError(f"unknown source stratum {stratum}")
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
    generated: RowJetMap = {}
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
                        raise ValueError("an active tied wall has no angle derivative")
                    label = f"{label}:{'+' if angle_sign > 0 else '-'}"
                _insert(generated, label, gap)

    for first, second in itertools.combinations(range(5), 2):
        for owner in (first, second):
            for axis, axis_name in zip(frames[owner], frame_names[owner], strict=True):
                displacement = tuple(
                    right - left
                    for left, right in zip(center_jets[first], center_jets[second], strict=True)
                )
                separation_sign = _dot(axis, displacement).value.sign()
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
                    _insert(generated, label, gap)
    return generated


def owner_row_jets(field: NumberField, stratum: str, owner: str) -> RowJetMap:
    """Return one owner's complete rows after exact source-key and gradient validation."""
    if owner not in tangent_cones.EXPECTED_CONTACT_BRANCHES:
        raise ValueError(f"unknown source owner {owner}")
    generated = active_row_jets(field, stratum)
    selected = {
        label: jet for label, jet in generated.items() if not label.startswith("contact:3-4:")
    }
    selected.update(
        {
            label: jet
            for label, jet in generated.items()
            if label.startswith(f"contact:3-4:{owner}:")
        }
    )
    source_rows = tangent_inventory.matrix(field, stratum, owner)
    expected = {row.label: row.coefficients for row in source_rows}
    if selected.keys() != expected.keys():
        missing = sorted(expected.keys() - selected.keys())
        extra = sorted(selected.keys() - expected.keys())
        raise ValueError(f"generated owner-row keys drifted; missing={missing}, extra={extra}")
    if {label: jet.gradient for label, jet in selected.items()} != expected:
        raise ValueError("generated owner-row gradients drifted from the source matrix")
    return {row.label: selected[row.label] for row in source_rows}
