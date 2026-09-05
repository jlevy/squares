#!/usr/bin/env python3
"""Classify the active first-order cones along exp-033's exact n=5 face.

The checker keeps the distinction that matters for this slice: an exact nonzero vector
in every active linearized inequality is first-order evidence, not a nonlinear motion.
It derives the wall/contact inventory from the exact Q(sqrt(2)) poses, enumerates both
owner-axis branches at pair (3,4), retains the tied support rows as a conjunction inside
each branch, and replays explicit endpoint/interior witnesses.
"""

from __future__ import annotations

import argparse
import copy
import itertools
import json
import sys
import time
from pathlib import Path
from typing import cast

from strif import atomic_output_file

from cases.n5 import equal_side_face as face
from sqpack.exact_lp import LinearRow
from sqpack.field import FieldElement, NumberField

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_VERSION = 1
VARIABLE_COUNT = 15
EXP034 = (
    ROOT / "campaign/series/series-000-smoke-and-calibration/results/"
    "exp-034-h-023-n5-angle-sheet.json"
)
STRATA = ("A", "interior", "B")
EXPECTED_WALL_LABELS = {
    "A": {
        "wall:0:x-lower:-",
        "wall:0:x-lower:+",
        "wall:1:x-upper:-",
        "wall:1:x-upper:+",
        "wall:1:y-lower:-",
        "wall:1:y-lower:+",
        "wall:2:x-lower:-",
        "wall:2:x-lower:+",
        "wall:2:y-lower:-",
        "wall:2:y-lower:+",
        "wall:3:x-upper",
        "wall:3:y-upper",
    },
    "interior": {
        "wall:1:x-upper:-",
        "wall:1:x-upper:+",
        "wall:1:y-lower:-",
        "wall:1:y-lower:+",
        "wall:2:x-lower:-",
        "wall:2:x-lower:+",
        "wall:2:y-lower:-",
        "wall:2:y-lower:+",
        "wall:3:x-upper",
        "wall:3:y-upper",
    },
    "B": {
        "wall:0:y-upper:-",
        "wall:0:y-upper:+",
        "wall:1:x-upper:-",
        "wall:1:x-upper:+",
        "wall:1:y-lower:-",
        "wall:1:y-lower:+",
        "wall:2:x-lower:-",
        "wall:2:x-lower:+",
        "wall:2:y-lower:-",
        "wall:2:y-lower:+",
        "wall:3:x-upper",
        "wall:3:y-upper",
    },
}
EXPECTED_ZERO_AXES = {
    "0-4:owner4:a-",
    "1-4:owner4:a-",
    "2-4:owner4:a+",
    "3-4:owner3:a+",
    "3-4:owner4:a+",
}
EXPECTED_CONTACT_BRANCHES = ("owner3:a+", "owner4:a+")


def require_dict(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise TypeError(f"{label} must be an object")
    return cast(dict[str, object], value)


def require_list(value: object, label: str) -> list[object]:
    if not isinstance(value, list):
        raise TypeError(f"{label} must be a list")
    return value


def x(index: int) -> int:
    return index


def y(index: int) -> int:
    return 5 + index


def theta(index: int) -> int:
    return 10 + index


def zero_row(field: NumberField) -> list[FieldElement]:
    return [field.zero for _ in range(VARIABLE_COUNT)]


def row(field: NumberField, label: str, values: dict[int, FieldElement]) -> LinearRow:
    coefficients = zero_row(field)
    for index, value in values.items():
        coefficients[index] = value
    return LinearRow(label, tuple(coefficients))


def wall_rows(field: NumberField, stratum: str) -> tuple[LinearRow, ...]:
    q = field.rational
    rows: list[LinearRow] = []

    def tied(label: str, coordinate: int, coordinate_sign: int, angle: int) -> None:
        for feature_sign, suffix in ((-1, "-"), (1, "+")):
            rows.append(
                row(
                    field,
                    f"{label}:{suffix}",
                    {
                        coordinate: q(coordinate_sign),
                        angle: q(feature_sign) / 2,
                    },
                )
            )

    tied("wall:1:x-upper", x(1), -1, theta(1))
    tied("wall:1:y-lower", y(1), 1, theta(1))
    tied("wall:2:x-lower", x(2), 1, theta(2))
    tied("wall:2:y-lower", y(2), 1, theta(2))
    rows.append(row(field, "wall:3:x-upper", {x(3): q(-1)}))
    rows.append(row(field, "wall:3:y-upper", {y(3): q(-1)}))
    if stratum == "A":
        tied("wall:0:x-lower", x(0), 1, theta(0))
    elif stratum == "B":
        tied("wall:0:y-upper", y(0), -1, theta(0))
    elif stratum != "interior":
        raise ValueError(f"unknown stratum {stratum}")
    return tuple(sorted(rows, key=lambda item: item.label))


def add_coefficient(values: dict[int, FieldElement], index: int, value: FieldElement) -> None:
    updated = values[index] + value if index in values else value
    if updated.is_zero():
        values.pop(index, None)
    else:
        values[index] = updated


def add_form(
    target: dict[int, FieldElement],
    source: dict[int, FieldElement],
    scale: FieldElement,
) -> None:
    for index, value in source.items():
        add_coefficient(target, index, scale * value)


def perpendicular(
    vector: tuple[FieldElement, FieldElement],
) -> tuple[FieldElement, FieldElement]:
    return (-vector[1], vector[0])


def orientation_axes(
    field: NumberField,
) -> tuple[tuple[tuple[FieldElement, FieldElement, str], ...], ...]:
    q = field.rational
    r = field.alpha
    aligned = ((q(1), q(0), "x"), (q(0), q(1), "y"))
    diagonal = ((r / 2, r / 2, "a+"), (-r / 2, r / 2, "a-"))
    return (aligned, aligned, aligned, diagonal, diagonal)


def support_derivative_options(
    field: NumberField,
    axis: tuple[FieldElement, FieldElement],
    *,
    axis_owner: int,
    square_index: int,
) -> tuple[tuple[str, dict[int, FieldElement]], ...]:
    """Return every linear support derivative at one possibly tied feature."""
    q = field.rational
    deterministic: dict[int, FieldElement] = {}
    tied: list[dict[int, FieldElement]] = []
    for basis_x, basis_y, _basis_name in orientation_axes(field)[square_index]:
        basis = (basis_x, basis_y)
        derivative: dict[int, FieldElement] = {}
        add_coefficient(
            derivative,
            theta(axis_owner),
            dot2(perpendicular(axis), basis),
        )
        add_coefficient(
            derivative,
            theta(square_index),
            dot2(axis, perpendicular(basis)),
        )
        projection = dot2(axis, basis)
        if projection.is_zero():
            if derivative:
                tied.append(derivative)
            continue
        add_form(deterministic, derivative, q(projection.sign()) / 2)

    options: list[tuple[str, dict[int, FieldElement]]] = []
    for signs in itertools.product((-1, 1), repeat=len(tied)):
        values = dict(deterministic)
        for sign, derivative in zip(signs, tied, strict=True):
            add_form(values, derivative, q(sign) / 2)
        suffix = ":".join(f"square{square_index}-feature{sign:+d}" for sign in signs)
        options.append((suffix, values))
    return tuple(options)


def contact_axis_rows(
    field: NumberField,
    centres: list[tuple[FieldElement, FieldElement]],
    *,
    first: int,
    second: int,
    owner: int,
    axis_name: str,
) -> tuple[LinearRow, ...]:
    """Differentiate one active SAT owner axis, retaining every tied support row."""
    q = field.rational
    axis_entry = next(
        entry for entry in orientation_axes(field)[owner] if entry[2] == axis_name
    )
    axis = (axis_entry[0], axis_entry[1])
    displacement = (
        centres[second][0] - centres[first][0],
        centres[second][1] - centres[first][1],
    )
    projection = dot2(displacement, axis)
    if projection.is_zero():
        raise ValueError("an active SAT axis has zero centre separation")
    separation_sign = projection.sign()
    support = field.zero
    for square_index in (first, second):
        for basis_x, basis_y, _basis_name in orientation_axes(field)[square_index]:
            support += abs_exact(dot2(axis, (basis_x, basis_y))) / 2
    if abs_exact(projection) != support:
        raise ValueError(f"contact {first}-{second}:owner{owner}:{axis_name} is not exact")

    separation: dict[int, FieldElement] = {}
    for coordinate, axis_value in ((x, axis[0]), (y, axis[1])):
        add_coefficient(separation, coordinate(second), q(separation_sign) * axis_value)
        add_coefficient(separation, coordinate(first), -q(separation_sign) * axis_value)
    add_coefficient(
        separation,
        theta(owner),
        q(separation_sign) * dot2(displacement, perpendicular(axis)),
    )

    first_options = support_derivative_options(
        field, axis, axis_owner=owner, square_index=first
    )
    second_options = support_derivative_options(
        field, axis, axis_owner=owner, square_index=second
    )
    rows: list[LinearRow] = []
    for first_suffix, first_support in first_options:
        for second_suffix, second_support in second_options:
            values = dict(separation)
            add_form(values, first_support, q(-1))
            add_form(values, second_support, q(-1))
            suffix = ":".join(item for item in (first_suffix, second_suffix) if item)
            label = f"contact:{first}-{second}:owner{owner}:{axis_name}"
            if suffix:
                label = f"{label}:{suffix}"
            rows.append(row(field, label, values))
    return tuple(sorted(rows, key=lambda item: item.label))


def contact_rows(
    field: NumberField,
    centres: list[tuple[FieldElement, FieldElement]],
) -> tuple[tuple[LinearRow, ...], dict[str, tuple[LinearRow, ...]]]:
    fixed = (
        *contact_axis_rows(field, centres, first=0, second=4, owner=4, axis_name="a-"),
        *contact_axis_rows(field, centres, first=1, second=4, owner=4, axis_name="a-"),
        *contact_axis_rows(field, centres, first=2, second=4, owner=4, axis_name="a+"),
    )
    branches = {
        f"owner{owner}:a+": contact_axis_rows(
            field,
            centres,
            first=3,
            second=4,
            owner=owner,
            axis_name="a+",
        )
        for owner in (3, 4)
    }
    if len(fixed) != 3 or any(len(rows) != 2 for rows in branches.values()):
        raise ValueError("the exact contact feature topology drifted")
    return fixed, branches


def abs_exact(value: FieldElement) -> FieldElement:
    return -value if value.sign() < 0 else value


def dot2(
    left: tuple[FieldElement, FieldElement], right: tuple[FieldElement, FieldElement]
) -> FieldElement:
    return left[0] * right[0] + left[1] * right[1]


def geometry_inventory(field: NumberField) -> dict[str, object]:
    """Derive active walls and owner axes from the exact source poses."""
    q = field.rational
    data = face.exact_data(field)
    side = cast(FieldElement, data["side"])
    endpoint_a = cast(list[tuple[FieldElement, FieldElement]], data["a"])
    endpoint_b = cast(list[tuple[FieldElement, FieldElement]], data["b"])
    midpoint = [
        ((left[0] + right[0]) / 2, (left[1] + right[1]) / 2)
        for left, right in zip(endpoint_a, endpoint_b, strict=True)
    ]
    axes = orientation_axes(field)

    def support(index: int, axis: tuple[FieldElement, FieldElement]) -> FieldElement:
        first, second = axes[index]
        u = (first[0], first[1])
        v = (second[0], second[1])
        return (abs_exact(dot2(axis, u)) + abs_exact(dot2(axis, v))) / 2

    wall_tables: dict[str, list[str]] = {}
    zero_axis_tables: dict[str, list[str]] = {}
    for name, centres in (("A", endpoint_a), ("interior", midpoint), ("B", endpoint_b)):
        zero_axes: set[str] = set()
        for first, second in itertools.combinations(range(5), 2):
            displacement = (
                centres[second][0] - centres[first][0],
                centres[second][1] - centres[first][1],
            )
            for owner in (first, second):
                for axis_x, axis_y, axis_name in axes[owner]:
                    axis = (axis_x, axis_y)
                    separation = abs_exact(dot2(displacement, axis))
                    gap = separation - support(first, axis) - support(second, axis)
                    if gap.is_zero():
                        zero_axes.add(f"{first}-{second}:owner{owner}:{axis_name}")
        if zero_axes != EXPECTED_ZERO_AXES:
            raise ValueError(
                f"unexpected {name} exact zero-axis inventory: {sorted(zero_axes)}"
            )
        zero_axis_tables[name] = sorted(zero_axes)

        labels: set[str] = set()
        for index, centre in enumerate(centres):
            square = face.square(field, centre, diagonal=index >= 3)
            for coordinate, wall, value in (
                (0, "x-lower", q(0)),
                (0, "x-upper", side),
                (1, "y-lower", q(0)),
                (1, "y-upper", side),
            ):
                active = [vertex for vertex in square if vertex[coordinate] == value]
                if not active:
                    continue
                if len(active) == 1:
                    labels.add(f"wall:{index}:{wall}")
                elif len(active) == 2:
                    labels.update((f"wall:{index}:{wall}:-", f"wall:{index}:{wall}:+"))
                else:
                    raise ValueError("unexpected active wall feature count")
        if labels != EXPECTED_WALL_LABELS[name]:
            raise ValueError(f"unexpected {name} exact wall inventory: {sorted(labels)}")
        wall_tables[name] = sorted(labels)
    return {
        "wall_labels_by_stratum": wall_tables,
        "zero_owner_axes_by_stratum": zero_axis_tables,
    }


def centres_for_stratum(
    field: NumberField, stratum: str
) -> list[tuple[FieldElement, FieldElement]]:
    data = face.exact_data(field)
    endpoint_a = cast(list[tuple[FieldElement, FieldElement]], data["a"])
    endpoint_b = cast(list[tuple[FieldElement, FieldElement]], data["b"])
    if stratum == "A":
        return endpoint_a
    if stratum == "B":
        return endpoint_b
    if stratum == "interior":
        return [
            ((left[0] + right[0]) / 2, (left[1] + right[1]) / 2)
            for left, right in zip(endpoint_a, endpoint_b, strict=True)
        ]
    raise ValueError(f"unknown stratum {stratum}")


def exact_dot(
    row_value: LinearRow, vector: list[FieldElement], field: NumberField
) -> FieldElement:
    return sum(
        (
            coefficient * coordinate
            for coefficient, coordinate in zip(row_value.coefficients, vector, strict=True)
        ),
        field.zero,
    )


def exact_rank(rows: tuple[LinearRow, ...]) -> int:
    work = [list(item.coefficients) for item in rows]
    rank = 0
    for column in range(VARIABLE_COUNT):
        pivot = next(
            (
                candidate
                for candidate in range(rank, len(work))
                if not work[candidate][column].is_zero()
            ),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = work[rank][column].inverse()
        work[rank] = [value * inverse for value in work[rank]]
        for candidate in range(len(work)):
            if candidate == rank:
                continue
            factor = work[candidate][column]
            if factor.is_zero():
                continue
            work[candidate] = [
                left - factor * right
                for left, right in zip(work[candidate], work[rank], strict=True)
            ]
        rank += 1
    return rank


def encode(value: FieldElement) -> list[str]:
    return [str(coefficient) for coefficient in value.coeffs]


def encode_row(item: LinearRow) -> dict[str, object]:
    return {
        "label": item.label,
        "coefficients_low_degree_first": [encode(value) for value in item.coefficients],
        "sense": ">= 0",
    }


def witness(field: NumberField, stratum: str) -> list[FieldElement]:
    q = field.rational
    delta = 3 * field.alpha / 2 - 2
    values = zero_row(field)
    values[x(4)] = delta / 2
    values[theta(3)] = q(1)
    values[theta(4)] = q(1)
    if stratum == "A":
        values[y(0)] = -delta
    elif stratum == "B":
        values[x(0)] = -delta
    elif stratum != "interior":
        raise ValueError(f"unknown stratum {stratum}")
    return values


def build_stratum(field: NumberField, stratum: str) -> dict[str, object]:
    centres = centres_for_stratum(field, stratum)
    walls = wall_rows(field, stratum)
    fixed, alternatives = contact_rows(field, centres)
    direction = witness(field, stratum)
    all_active = (
        *walls,
        *fixed,
        *(item for branch in alternatives.values() for item in branch),
    )
    derivatives = {item.label: exact_dot(item, direction, field) for item in all_active}
    if any(value.sign() < 0 for value in derivatives.values()):
        raise ValueError(f"the {stratum} witness violates an active inequality")
    if any(not value.is_zero() for value in derivatives.values()):
        raise ValueError(f"the {stratum} witness should maintain every active feature")
    if direction[theta(3)].is_zero() or direction[theta(4)].is_zero():
        raise ValueError("the non-sheet witness lost its diagonal angle motion")
    branches: list[dict[str, object]] = []
    for branch_name in EXPECTED_CONTACT_BRANCHES:
        contact_branch = alternatives[branch_name]
        rows = (*walls, *fixed, *contact_branch)
        rank = exact_rank(rows)
        if exact_dot(contact_branch[0], direction, field) != field.zero:
            raise ValueError(f"the {stratum} witness left one tied support row")
        if exact_dot(contact_branch[1], direction, field) != field.zero:
            raise ValueError(f"the {stratum} witness left one tied support row")
        branches.append(
            {
                "selected_contact_3_4_owner_axis": branch_name,
                "tied_support_row_count": len(contact_branch),
                "row_count": len(rows),
                "exact_equality_rank": rank,
                "equality_kernel_nullity": VARIABLE_COUNT - rank,
                "inequalities": [encode_row(item) for item in rows],
            }
        )
    if branches[0]["inequalities"] == branches[1]["inequalities"]:
        raise ValueError("the two owner-axis branches are not one-to-one")
    return {
        "name": stratum,
        "wall_row_count": len(walls),
        "fixed_contact_row_count": len(fixed),
        "contact_3_4_owner_branch_count": len(alternatives),
        "contact_3_4_rows_per_owner_branch": 2,
        "branches": branches,
        "non_sheet_direction": {
            "variables": [f"dx{i}" for i in range(5)]
            + [f"dy{i}" for i in range(5)]
            + [f"dtheta{i}" for i in range(5)],
            "coordinates_low_degree_first": [encode(value) for value in direction],
            "all_active_derivatives_exactly_zero": True,
            "outside_exp_034_sheet": True,
        },
        "all_active_feature_derivatives": {
            label: encode(value) for label, value in sorted(derivatives.items())
        },
    }


def validate_result(result: dict[str, object]) -> None:
    inventory = require_dict(result.get("active_inventory"), "active inventory")
    wall_tables = require_dict(
        inventory.get("wall_labels_by_stratum"), "wall labels by stratum"
    )
    axis_tables = require_dict(
        inventory.get("zero_owner_axes_by_stratum"), "zero owner axes by stratum"
    )
    for name in STRATA:
        retained_walls = set(require_list(wall_tables.get(name), f"{name} wall labels"))
        if retained_walls != EXPECTED_WALL_LABELS[name]:
            raise ValueError(f"the retained {name} wall inventory is incomplete")
        retained_axes = set(require_list(axis_tables.get(name), f"{name} zero owner axes"))
        if retained_axes != EXPECTED_ZERO_AXES:
            raise ValueError(f"the retained {name} zero-axis inventory is incomplete")
    strata = require_list(result.get("strata"), "strata")
    if len(strata) != 3:
        raise ValueError("the retained result does not cover all three strata")
    for expected_name, item in zip(STRATA, strata, strict=True):
        record = require_dict(item, "stratum")
        if record.get("name") != expected_name:
            raise ValueError("stratum order or identity drifted")
        expected_wall_count = len(EXPECTED_WALL_LABELS[expected_name])
        if record.get("wall_row_count") != expected_wall_count:
            raise ValueError(f"the {expected_name} wall-row count drifted")
        if record.get("fixed_contact_row_count") != 3:
            raise ValueError(f"the {expected_name} fixed-contact rows drifted")
        if record.get("contact_3_4_owner_branch_count") != 2:
            raise ValueError(f"the {expected_name} owner-axis branch count drifted")
        if record.get("contact_3_4_rows_per_owner_branch") != 2:
            raise ValueError(f"the {expected_name} tied-support conjunction drifted")
        branches = require_list(record.get("branches"), "branches")
        if len(branches) != len(EXPECTED_CONTACT_BRANCHES):
            raise ValueError("a stratum does not retain both owner-axis branches")
        retained_matrices: list[list[object]] = []
        for expected_branch, branch_item in zip(
            EXPECTED_CONTACT_BRANCHES, branches, strict=True
        ):
            branch = require_dict(branch_item, "branch")
            if branch.get("selected_contact_3_4_owner_axis") != expected_branch:
                raise ValueError("owner-axis branch order or identity drifted")
            if branch.get("tied_support_row_count") != 2:
                raise ValueError("a tied support row was treated as an alternative")
            expected_row_count = expected_wall_count + 5
            if branch.get("row_count") != expected_row_count:
                raise ValueError("an active inequality row is missing")
            inequalities = require_list(branch.get("inequalities"), "inequalities")
            if len(inequalities) != expected_row_count:
                raise ValueError("the retained row count disagrees with the matrix")
            contact_3_4_labels: list[str] = []
            for row_item in inequalities:
                retained_row = require_dict(row_item, "inequality")
                label = retained_row.get("label")
                coefficients = require_list(
                    retained_row.get("coefficients_low_degree_first"), "coefficients"
                )
                if not isinstance(label, str) or len(coefficients) != VARIABLE_COUNT:
                    raise ValueError("a retained inequality row is malformed")
                if retained_row.get("sense") != ">= 0":
                    raise ValueError("a retained inequality has the wrong sense")
                if label.startswith("contact:3-4:"):
                    contact_3_4_labels.append(label)
            if len(contact_3_4_labels) != 2:
                raise ValueError("an owner branch must retain both tied support rows")
            expected_owner = expected_branch.split(":", maxsplit=1)[0]
            if any(f":{expected_owner}:" not in label for label in contact_3_4_labels):
                raise ValueError("a tied support row belongs to the wrong owner axis")
            retained_matrices.append(inequalities)
        if retained_matrices[0] == retained_matrices[1]:
            raise ValueError("the two owner-axis matrices are not one-to-one")
        direction = require_dict(record.get("non_sheet_direction"), "direction")
        if (
            direction.get("all_active_derivatives_exactly_zero") is not True
            or direction.get("outside_exp_034_sheet") is not True
        ):
            raise ValueError("the exact non-sheet direction is not certified")
    continuation = require_dict(result.get("nonlinear_continuation"), "continuation")
    if continuation.get("status") != "unresolved":
        raise ValueError("first-order evidence cannot claim nonlinear continuation")
    determination = require_dict(result.get("determination"), "determination")
    if determination.get("outcome") != "criterion_met":
        raise ValueError("the complete first-order criterion was not met")


def require_same_result(retained: dict[str, object], regenerated: dict[str, object]) -> None:
    if retained != regenerated:
        raise ValueError("retained n=5 tangent-cone record differs from regeneration")


def build_result() -> dict[str, object]:
    field = face.make_field()
    result: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "contract": "packing.squares:N5TangentCones/v1",
        "source": {
            "exp_034": str(EXP034.relative_to(ROOT)),
            "field": "Q(sqrt(2)), sqrt(2) in (1,2)",
        },
        "active_inventory": geometry_inventory(field),
        "strata": [build_stratum(field, name) for name in STRATA],
        "nonlinear_continuation": {
            "status": "unresolved",
            "next_test": (
                "rotate squares 3 and 4 together in half-angle coordinates, solve the "
                "1-4, 2-4, and 0-4 contact equations, then certify every wall and SAT branch"
            ),
            "warning": (
                "a nonzero linearized direction is not a Bouligand motion or a stationary-"
                "component connection until a nonlinear continuation realizes it"
            ),
        },
        "determination": {
            "outcome": "criterion_met",
            "claim": (
                "every exact endpoint/interior stratum has both owner-axis branches, "
                "both tied support rows per branch, and an exact non-sheet first-order "
                "feasible direction"
            ),
            "scope": (
                "linearized active inequalities only; nonlinear realization, component "
                "identity, basin mass, and unequal-side clearance remain unresolved"
            ),
        },
    }
    validate_result(result)

    missing_branch = copy.deepcopy(result)
    require_list(
        require_dict(require_list(missing_branch["strata"], "strata")[1], "stratum")[
            "branches"
        ],
        "branches",
    ).pop()
    missing_tied_row = copy.deepcopy(result)
    interior_branch = require_dict(
        require_list(missing_tied_row["strata"], "strata")[1], "interior stratum"
    )
    first_branch = require_dict(
        require_list(interior_branch["branches"], "branches")[0], "first branch"
    )
    retained_rows = require_list(first_branch["inequalities"], "inequalities")
    retained_rows.pop()
    first_branch["tied_support_row_count"] = 1
    first_branch["row_count"] = len(retained_rows)
    false_continuation = copy.deepcopy(result)
    require_dict(false_continuation["nonlinear_continuation"], "continuation")["status"] = (
        "proved"
    )
    wrong = witness(field, "interior")
    wrong[theta(4)] = -field.one
    interior_centres = centres_for_stratum(field, "interior")
    interior_fixed, interior_branches = contact_rows(field, interior_centres)
    wrong_direction_rejected = any(
        exact_dot(item, wrong, field).sign() < 0
        for item in (
            *wall_rows(field, "interior"),
            *interior_fixed,
            *(item for rows in interior_branches.values() for item in rows),
        )
    )
    endpoint_a_fixed, _endpoint_a_branches = contact_rows(
        field, centres_for_stratum(field, "A")
    )
    stale_a_row_rejected = (
        endpoint_a_fixed[0].coefficients != interior_fixed[0].coefficients
        and not exact_dot(endpoint_a_fixed[0], witness(field, "interior"), field).is_zero()
        and exact_dot(interior_fixed[0], witness(field, "interior"), field).is_zero()
    )
    selftests = {
        "missing_owner_axis_branch_is_rejected": False,
        "missing_tied_support_row_is_rejected": False,
        "stale_endpoint_contact_row_is_rejected": stale_a_row_rejected,
        "first_order_evidence_cannot_claim_continuation": False,
        "wrong_angle_sign_violates_an_active_row": wrong_direction_rejected,
        "non_sheet_direction_has_diagonal_angle_motion": True,
    }
    try:
        validate_result(missing_branch)
    except ValueError:
        selftests["missing_owner_axis_branch_is_rejected"] = True
    try:
        validate_result(missing_tied_row)
    except ValueError:
        selftests["missing_tied_support_row_is_rejected"] = True
    try:
        validate_result(false_continuation)
    except ValueError:
        selftests["first_order_evidence_cannot_claim_continuation"] = True
    if not all(selftests.values()):
        raise ValueError(f"n=5 tangent-cone selftests failed: {selftests}")
    result["selftests"] = selftests
    return result


def write_json_atomic(path: Path, value: dict[str, object]) -> None:
    with atomic_output_file(path, make_parents=True) as temporary:
        temporary.write_text(
            json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )


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
            retained = require_dict(
                json.loads(args.replay.read_text(encoding="utf-8")), "retained result"
            )
            require_same_result(retained, result)
        summary = {
            "record_written": args.record is not None,
            "record_replayed": args.replay is not None,
            "determination_outcome": require_dict(result["determination"], "determination")[
                "outcome"
            ],
            "strata": len(require_list(result["strata"], "strata")),
            "owner_axis_branches_per_stratum": 2,
            "tied_support_rows_per_owner_branch": 2,
            "nonlinear_continuation": require_dict(
                result["nonlinear_continuation"], "continuation"
            )["status"],
            "selftests": result["selftests"],
            "elapsed_seconds": round(time.monotonic() - started, 6),
        }
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
