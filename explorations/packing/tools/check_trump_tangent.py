#!/usr/bin/env python3
"""Decide the branchwise one-sided linearized cones of Trump's exact packing.

The original feasible set is nonsmooth twice over: square support functions have
absolute-value derivatives when orientations agree, and pairwise non-overlap is a
union over locally active separating features.  This checker derives both structures
from the exact corner witness rather than from a hand-written contact graph.

For each complete feature selection it proves that the resulting cone is ``{0}`` by
exhibiting a strictly positive stress on all inequality rows and a full-rank subset of
33 rows. SciPy proposes positive free stress weights; exact arithmetic in ``Q(u)``
chooses the row basis, re-solves, and verifies the certificate. Floating point never
decides the result.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import sys
import time
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from sqpack.field import FieldElement, NumberField
from sqpack.packings import trump11
from sqpack.verify import edge_axes, exact_sign, separated, verify_packing

VARIABLES_PER_SQUARE = 3
EXPECTED_SQUARES = 11
EXPECTED_VARIABLES = VARIABLES_PER_SQUARE * EXPECTED_SQUARES
EXPECTED_WALL_INCIDENCES = 11
EXPECTED_WALL_ROWS = 20
EXPECTED_CONTACTS = 14
EXPECTED_RAW_FEATURES = 24
EXPECTED_LOCAL_OPTIONS = 22
EXPECTED_RAW_BRANCHES = 512
EXPECTED_REDUCED_BRANCHES = 128
EXPECTED_BRANCH_ROWS = 42
EXPECTED_WALL_TABLE = (
    (0, "left"),
    (0, "bottom"),
    (1, "right"),
    (1, "bottom"),
    (2, "top"),
    (3, "left"),
    (3, "top"),
    (4, "top"),
    (5, "left"),
    (7, "bottom"),
    (10, "right"),
)
EXPECTED_CONTACT_TABLE = (
    (0, 6),
    (1, 9),
    (2, 8),
    (2, 10),
    (3, 4),
    (3, 5),
    (4, 5),
    (4, 8),
    (5, 6),
    (6, 7),
    (6, 8),
    (7, 9),
    (8, 9),
    (9, 10),
)
EXPECTED_RAW_OPTION_COUNTS = (1, 1, 1, 1, 2, 2, 4, 1, 1, 2, 2, 2, 2, 2)
EXPECTED_OPTION_COUNTS = (1, 1, 1, 1, 1, 1, 4, 1, 1, 2, 2, 2, 2, 2)
EXPECTED_INCIDENTAL_ZERO_PAIRS = ((0, 4), (2, 5))
DETERMINATION_SCOPE = (
    "linearized cones overapproximate the true Bouligand tangent; zero for every "
    "complete branch implies true-tangent zero, while a nonzero linearized vector "
    "requires nonlinear continuation"
)


@dataclass(frozen=True)
class LinearRow:
    label: str
    coefficients: tuple[FieldElement, ...]


@dataclass(frozen=True)
class FeatureOption:
    label: str
    aliases: tuple[str, ...]
    rows: tuple[LinearRow, ...]


@dataclass(frozen=True)
class Contact:
    pair: tuple[int, int]
    raw_option_count: int
    options: tuple[FeatureOption, ...]


def rotate_quarter(point):
    return -point[1], point[0]


def dot(left, right):
    return left[0] * right[0] + left[1] * right[1]


def centre(square, zero):
    return (
        sum((point[0] for point in square), zero) / 4,
        sum((point[1] for point in square), zero) / 4,
    )


def zero_row(field: NumberField) -> list[FieldElement]:
    return [field.zero for _ in range(EXPECTED_VARIABLES)]


def add(row: list, square: int, coordinate: int, value) -> None:
    row[VARIABLES_PER_SQUARE * square + coordinate] = (
        row[VARIABLES_PER_SQUARE * square + coordinate] + value
    )


def scalar_key(value) -> tuple[tuple[int, int], ...]:
    return tuple(
        (coefficient.numerator, coefficient.denominator) for coefficient in value.coeffs
    )


def row_key(row: LinearRow) -> tuple:
    return tuple(scalar_key(value) for value in row.coefficients)


def matrix_digest(rows: tuple[LinearRow, ...]) -> str:
    payload = repr(tuple(sorted(row_key(row) for row in rows))).encode()
    return hashlib.sha256(payload).hexdigest()


def ordered_matrix_digest(rows: tuple[LinearRow, ...]) -> str:
    payload = repr(tuple(row_key(row) for row in rows)).encode()
    return hashlib.sha256(payload).hexdigest()


def unique_rows(rows: list[LinearRow]) -> tuple[LinearRow, ...]:
    found: dict[tuple, LinearRow] = {}
    for row in rows:
        found.setdefault(row_key(row), row)
    return tuple(found.values())


def wall_rows(squares, side, field):
    rows: list[LinearRow] = []
    incidences = []
    centres = [centre(square, field.zero) for square in squares]
    walls = (
        ("left", lambda point: point[0], 0, 1),
        ("right", lambda point: side - point[0], 0, -1),
        ("bottom", lambda point: point[1], 1, 1),
        ("top", lambda point: side - point[1], 1, -1),
    )
    for square_index, square in enumerate(squares):
        cx, cy = centres[square_index]
        for wall, margin, coordinate, direction in walls:
            tied = [index for index, point in enumerate(square) if margin(point).is_zero()]
            if not tied:
                continue
            incidence_rows = []
            for corner_index in tied:
                px, py = square[corner_index]
                row = zero_row(field)
                add(row, square_index, coordinate, field.rational(direction))
                if coordinate == 0:
                    angle_coefficient = -direction * (py - cy)
                else:
                    angle_coefficient = direction * (px - cx)
                add(row, square_index, 2, angle_coefficient)
                incidence_rows.append(
                    LinearRow(f"wall:{square_index}:{wall}:corner-{corner_index}", tuple(row))
                )
            incidence_rows = list(unique_rows(incidence_rows))
            rows.extend(incidence_rows)
            incidences.append(
                {
                    "square": square_index,
                    "wall": wall,
                    "support_corners": tied,
                    "tangent_rows": len(incidence_rows),
                }
            )
    return tuple(rows), incidences, centres


def projection_extrema(square, axis):
    values = [dot(axis, point) for point in square]
    low = high = values[0]
    for value in values[1:]:
        if (value - low).sign() < 0:
            low = value
        if (value - high).sign() > 0:
            high = value
    low_vertices = [index for index, value in enumerate(values) if (value - low).is_zero()]
    high_vertices = [index for index, value in enumerate(values) if (value - high).is_zero()]
    return low, high, low_vertices, high_vertices


def feature_rows(
    squares,
    centres,
    field,
    *,
    pair: tuple[int, int],
    owner: int,
    axis_index: int,
    order: str,
) -> tuple[LinearRow, ...] | None:
    first, second = pair
    axis = edge_axes(squares[owner])[axis_index]
    first_low, first_high, first_min, first_max = projection_extrema(squares[first], axis)
    second_low, second_high, second_min, second_max = projection_extrema(squares[second], axis)
    if order == "first-before-second":
        gap = second_low - first_high
        positive, positive_vertices = second, second_min
        negative, negative_vertices = first, first_max
    else:
        gap = first_low - second_high
        positive, positive_vertices = first, first_min
        negative, negative_vertices = second, second_max
    if not gap.is_zero():
        return None

    normal_velocity = rotate_quarter(axis)
    rows = []
    for positive_vertex in positive_vertices:
        for negative_vertex in negative_vertices:
            positive_point = squares[positive][positive_vertex]
            negative_point = squares[negative][negative_vertex]
            positive_radius = (
                positive_point[0] - centres[positive][0],
                positive_point[1] - centres[positive][1],
            )
            negative_radius = (
                negative_point[0] - centres[negative][0],
                negative_point[1] - centres[negative][1],
            )
            row = zero_row(field)
            add(row, positive, 0, axis[0])
            add(row, positive, 1, axis[1])
            add(row, negative, 0, -axis[0])
            add(row, negative, 1, -axis[1])
            add(row, positive, 2, dot(axis, rotate_quarter(positive_radius)))
            add(row, negative, 2, -dot(axis, rotate_quarter(negative_radius)))
            separation = (
                positive_point[0] - negative_point[0],
                positive_point[1] - negative_point[1],
            )
            add(row, owner, 2, dot(normal_velocity, separation))
            rows.append(
                LinearRow(
                    (
                        f"pair:{first}-{second}:owner-{owner}:axis-{axis_index}:"
                        f"{order}:vertices-{negative}.{negative_vertex}-"
                        f"{positive}.{positive_vertex}"
                    ),
                    tuple(row),
                )
            )
    return unique_rows(rows)


def contact_options(squares, centres, field) -> tuple[Contact, ...]:
    contacts = []
    for first in range(len(squares)):
        for second in range(first + 1, len(squares)):
            if separated(squares[first], squares[second], exact_sign) != 0:
                continue
            raw_options = []
            for owner in (first, second):
                for axis_index in (0, 1):
                    for order in ("first-before-second", "second-before-first"):
                        rows = feature_rows(
                            squares,
                            centres,
                            field,
                            pair=(first, second),
                            owner=owner,
                            axis_index=axis_index,
                            order=order,
                        )
                        if rows is not None:
                            raw_options.append(
                                FeatureOption(
                                    f"{first}-{second}/{owner}.{axis_index}/{order}",
                                    (),
                                    rows,
                                )
                            )
            grouped: dict[tuple, FeatureOption] = {}
            aliases: dict[tuple, list[str]] = {}
            for option in raw_options:
                key = tuple(sorted(row_key(row) for row in option.rows))
                aliases.setdefault(key, []).append(option.label)
                grouped.setdefault(key, option)
            options = tuple(
                FeatureOption(option.label, tuple(aliases[key]), option.rows)
                for key, option in grouped.items()
            )
            if not options:
                raise ValueError(f"contact pair {(first, second)} has no zero-gap feature")
            contacts.append(Contact((first, second), len(raw_options), options))
    return tuple(contacts)


def incidental_zero_pairs(squares, centres, field) -> tuple[tuple[int, int], ...]:
    """Return strict pairs that nevertheless have a zero projection feature."""
    pairs = []
    for first in range(len(squares)):
        for second in range(first + 1, len(squares)):
            if separated(squares[first], squares[second], exact_sign) == 0:
                continue
            has_zero_feature = any(
                feature_rows(
                    squares,
                    centres,
                    field,
                    pair=(first, second),
                    owner=owner,
                    axis_index=axis_index,
                    order=order,
                )
                is not None
                for owner in (first, second)
                for axis_index in (0, 1)
                for order in ("first-before-second", "second-before-first")
            )
            if has_zero_feature:
                pairs.append((first, second))
    return tuple(pairs)


def as_float_matrix(rows: tuple[LinearRow, ...]) -> np.ndarray:
    return np.asarray([[float(value) for value in row.coefficients] for row in rows])


def exact_solve(
    matrix: list[list[FieldElement]], rhs: list[FieldElement], field: NumberField
) -> list[FieldElement] | None:
    size = len(matrix)
    augmented = [[*row, rhs[index]] for index, row in enumerate(matrix)]
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if not augmented[row][column].is_zero()),
            None,
        )
        if pivot is None:
            return None
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        inverse = augmented[column][column].inverse()
        augmented[column][column:] = [value * inverse for value in augmented[column][column:]]
        for row in range(column + 1, size):
            factor = augmented[row][column]
            if factor.is_zero():
                continue
            augmented[row][column:] = [
                left - factor * right
                for left, right in zip(
                    augmented[row][column:], augmented[column][column:], strict=True
                )
            ]
    solution = [field.zero for _ in range(size)]
    for row in range(size - 1, -1, -1):
        solution[row] = augmented[row][-1] - sum(
            (augmented[row][column] * solution[column] for column in range(row + 1, size)),
            field.zero,
        )
    return solution


def exact_pivot_rows(rows: tuple[LinearRow, ...], field: NumberField) -> list[int] | None:
    """Select a full-rank row basis deterministically in exact arithmetic."""
    if not rows:
        return None
    variable_count = len(rows[0].coefficients)
    transpose = [
        [row.coefficients[coordinate] for row in rows] for coordinate in range(variable_count)
    ]
    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(len(rows)):
        pivot = next(
            (
                row
                for row in range(pivot_row, variable_count)
                if not transpose[row][column].is_zero()
            ),
            None,
        )
        if pivot is None:
            continue
        transpose[pivot_row], transpose[pivot] = transpose[pivot], transpose[pivot_row]
        inverse = transpose[pivot_row][column].inverse()
        transpose[pivot_row] = [value * inverse for value in transpose[pivot_row]]
        for row in range(variable_count):
            if row == pivot_row:
                continue
            factor = transpose[row][column]
            if factor.is_zero():
                continue
            transpose[row] = [
                left - factor * right
                for left, right in zip(transpose[row], transpose[pivot_row], strict=True)
            ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == variable_count:
            return pivot_columns
    return None


def exact_dot(
    row: tuple[FieldElement, ...], vector: list[FieldElement], field: NumberField
) -> FieldElement:
    return sum((left * right for left, right in zip(row, vector, strict=True)), field.zero)


def positive_stress_certificate(rows: tuple[LinearRow, ...], field: NumberField) -> dict | None:
    matrix = as_float_matrix(rows)
    row_count, variable_count = matrix.shape
    if variable_count != EXPECTED_VARIABLES:
        raise ValueError(f"expected {EXPECTED_VARIABLES} variables, got {variable_count}")
    numeric = linprog(
        np.ones(row_count),
        A_eq=matrix.T,
        b_eq=np.zeros(variable_count),
        bounds=[(1.0, None)] * row_count,
        method="highs-ds",
    )
    if not numeric.success or numeric.x is None:
        return None
    pivot_rows = exact_pivot_rows(rows, field)
    if pivot_rows is None:
        return None
    free_rows = [index for index in range(row_count) if index not in set(pivot_rows)]
    free_weights = {
        index: Fraction(format(float(numeric.x[index]), ".17g")) for index in free_rows
    }
    coefficient_matrix = [[field.zero for _ in pivot_rows] for _ in range(variable_count)]
    for coordinate in range(variable_count):
        for column, pivot in enumerate(pivot_rows):
            coefficient_matrix[coordinate][column] = rows[pivot].coefficients[coordinate]
    rhs = [
        -sum(
            (
                rows[index].coefficients[coordinate] * field.rational(weight)
                for index, weight in free_weights.items()
            ),
            field.zero,
        )
        for coordinate in range(variable_count)
    ]
    pivot_weights = exact_solve(coefficient_matrix, rhs, field)
    if pivot_weights is None or any(weight.sign() <= 0 for weight in pivot_weights):
        return None
    stress = [field.zero for _ in range(row_count)]
    for index, weight in free_weights.items():
        stress[index] = field.rational(weight)
    for index, weight in zip(pivot_rows, pivot_weights, strict=True):
        stress[index] = weight
    residuals = [
        sum(
            (
                rows[index].coefficients[coordinate] * stress[index]
                for index in range(row_count)
            ),
            field.zero,
        )
        for coordinate in range(variable_count)
    ]
    if any(not residual.is_zero() for residual in residuals):
        raise AssertionError("exact stress replay left a nonzero residual")
    if any(weight.sign() <= 0 for weight in stress):
        raise AssertionError("exact stress replay was not strictly positive")
    return {
        "pivot_rows": pivot_rows,
        "free_weights": {str(index): str(weight) for index, weight in free_weights.items()},
        "minimum_weight_approx": min(float(weight) for weight in stress),
        "rank": variable_count,
        "residual_exactly_zero": True,
        "all_weights_strictly_positive": True,
    }


def replay_certificate(
    rows: tuple[LinearRow, ...], certificate: dict, field: NumberField
) -> bool:
    if (
        certificate.get("rank") != EXPECTED_VARIABLES
        or certificate.get("residual_exactly_zero") is not True
        or certificate.get("all_weights_strictly_positive") is not True
    ):
        return False
    pivot_rows = [int(index) for index in certificate["pivot_rows"]]
    free_weights = {
        int(index): Fraction(weight) for index, weight in certificate["free_weights"].items()
    }
    variable_count = len(rows[0].coefficients)
    if len(pivot_rows) != variable_count:
        return False
    coefficient_matrix = [
        [rows[pivot].coefficients[coordinate] for pivot in pivot_rows]
        for coordinate in range(variable_count)
    ]
    rhs = [
        -sum(
            (
                rows[index].coefficients[coordinate] * field.rational(weight)
                for index, weight in free_weights.items()
            ),
            field.zero,
        )
        for coordinate in range(variable_count)
    ]
    pivot_weights = exact_solve(coefficient_matrix, rhs, field)
    if pivot_weights is None or any(weight.sign() <= 0 for weight in pivot_weights):
        return False
    stress = [field.zero for _ in rows]
    for index, weight in free_weights.items():
        stress[index] = field.rational(weight)
    for index, weight in zip(pivot_rows, pivot_weights, strict=True):
        stress[index] = weight
    return all(weight.sign() > 0 for weight in stress) and all(
        exact_dot(tuple(row.coefficients[coordinate] for row in rows), stress, field).is_zero()
        for coordinate in range(variable_count)
    )


def field_element_record(value: FieldElement) -> list[str]:
    return [str(coefficient) for coefficient in value.coeffs]


def exact_nonzero_direction(rows: tuple[LinearRow, ...], field: NumberField) -> dict | None:
    """Propose numerically, then replay exactly, one nonzero cone vector."""
    matrix = as_float_matrix(rows)
    variable_count = matrix.shape[1]
    for coordinate in range(variable_count):
        for sign in (-1, 1):
            objective = np.zeros(variable_count)
            objective[coordinate] = -sign
            result = linprog(
                objective,
                A_ub=-matrix,
                b_ub=np.zeros(len(rows)),
                bounds=[(-1.0, 1.0)] * variable_count,
                method="highs-ds",
            )
            if not result.success or result.x is None:
                continue
            if sign * float(result.x[coordinate]) < 0.5:
                continue

            equations: list[LinearRow] = []
            right_sides: list[FieldElement] = []
            products = matrix @ result.x
            for index, product in enumerate(products):
                if abs(float(product)) <= 1e-7:
                    equations.append(rows[index])
                    right_sides.append(field.zero)
            for index, value in enumerate(result.x):
                if abs(abs(float(value)) - 1.0) > 1e-7:
                    continue
                coefficients = zero_row(field)
                coefficients[index] = field.one
                equations.append(LinearRow(f"bound:{index}", tuple(coefficients)))
                right_sides.append(field.rational(1 if value > 0 else -1))

            equation_tuple = tuple(equations)
            pivot_equations = exact_pivot_rows(equation_tuple, field)
            if pivot_equations is None:
                continue
            system = [list(equations[index].coefficients) for index in pivot_equations]
            rhs = [right_sides[index] for index in pivot_equations]
            direction = exact_solve(system, rhs, field)
            if direction is None or all(value.is_zero() for value in direction):
                continue
            if any(exact_dot(row.coefficients, direction, field).sign() < 0 for row in rows):
                continue
            if direction[coordinate] != field.rational(sign):
                continue
            return {
                "normalizing_coordinate": coordinate,
                "normalizing_sign": sign,
                "coordinates_low_degree_first": [
                    field_element_record(value) for value in direction
                ],
                "all_inequalities_replayed_exactly": True,
            }
    return None


def field_metadata_selftest() -> dict[str, bool]:
    variable = sp.Symbol("u")
    polynomial = sp.Poly.from_list(list(trump11.U_MIN_POLY), gens=variable, domain=sp.QQ)
    lower = sp.Rational(trump11.U_INTERVAL[0])
    upper = sp.Rational(trump11.U_INTERVAL[1])
    irreducible = bool(polynomial.is_irreducible)
    squarefree = bool(polynomial.gcd(polynomial.diff()).degree() == 0)
    unique_root = bool(polynomial.count_roots(lower, upper) == 1)
    if not (irreducible and squarefree and unique_root):
        raise AssertionError("Trump field metadata failed exact polynomial replay")
    return {
        "u_polynomial_irreducible_over_Q": irreducible,
        "u_polynomial_squarefree": squarefree,
        "u_interval_contains_exactly_one_root": unique_root,
    }


def index_complete_records(records: list[dict], branch_groups: dict[str, dict]) -> dict:
    if len(records) != len(branch_groups):
        raise ValueError("record count does not match the derived matrix count")
    records_by_digest: dict[str, dict] = {}
    for branch_record in records:
        digest = branch_record["matrix_sha256"]
        if digest in records_by_digest:
            raise ValueError(f"record duplicates branch matrix: {digest}")
        records_by_digest[digest] = branch_record
    if set(records_by_digest) != set(branch_groups):
        raise ValueError("recorded branch digests are not the complete derived matrix set")
    return records_by_digest


def run_selftests(
    field: NumberField,
    walls: tuple[LinearRow, ...],
    contacts: tuple[Contact, ...],
) -> dict[str, bool]:
    two = 2
    rigid_rows = tuple(
        LinearRow(label, tuple(coefficients))
        for label, coefficients in (
            ("x+", (field.one, field.zero)),
            ("x-", (-field.one, field.zero)),
            ("y+", (field.zero, field.one)),
            ("y-", (field.zero, -field.one)),
        )
    )
    flexible_rows = (LinearRow("x+", (field.one, field.zero)),)

    def toy_certificate(rows):
        matrix = np.asarray([[float(value) for value in row.coefficients] for row in rows])
        result = linprog(
            np.ones(len(rows)),
            A_eq=matrix.T,
            b_eq=np.zeros(two),
            bounds=[(1.0, None)] * len(rows),
            method="highs-ds",
        )
        return result.success

    if not toy_certificate(rigid_rows) or toy_certificate(flexible_rows):
        raise AssertionError("known rigid/flexible cone controls failed")

    omitted_wall_rows = tuple(row for row in walls if not row.label.startswith("wall:0:left:"))
    omission_direction = [field.zero for _ in range(EXPECTED_VARIABLES)]
    omission_direction[0] = -field.one
    remaining_options = tuple(option for contact in contacts for option in contact.options)
    if any(
        exact_dot(row.coefficients, omission_direction, field).sign() < 0
        for row in omitted_wall_rows
    ) or any(
        exact_dot(row.coefficients, omission_direction, field).sign() < 0
        for option in remaining_options
        for row in option.rows
    ):
        raise AssertionError("known flexible wall-omission control failed")
    try:
        index_complete_records(
            [{"matrix_sha256": "a"}, {"matrix_sha256": "a"}],
            {"a": {}, "b": {}},
        )
    except ValueError:
        duplicate_rejected = True
    else:
        duplicate_rejected = False
    if not duplicate_rejected:
        raise AssertionError("duplicate branch-record coverage control failed")
    return {
        "rigid_cone_has_positive_stress": True,
        "flexible_cone_has_no_positive_stress": True,
        "trump_wall_omission_has_exact_nonzero_direction": True,
        "duplicate_branch_records_are_rejected": True,
        **field_metadata_selftest(),
    }


def enumerate_branch_groups(
    walls: tuple[LinearRow, ...], contacts: tuple[Contact, ...]
) -> dict[str, dict]:
    branch_groups: dict[str, dict] = {}
    for selection in itertools.product(*(range(len(contact.options)) for contact in contacts)):
        selected = [
            contact.options[index] for contact, index in zip(contacts, selection, strict=True)
        ]
        rows = tuple(itertools.chain(walls, *(option.rows for option in selected)))
        digest = matrix_digest(rows)
        group = branch_groups.setdefault(
            digest,
            {
                "rows": rows,
                "selections": [],
                "raw_selection_count": 0,
            },
        )
        group["selections"].append(selection)
        group["raw_selection_count"] += math.prod(len(option.aliases) for option in selected)
    return branch_groups


def contact_records(contacts: tuple[Contact, ...]) -> list[dict]:
    return [
        {
            "pair": list(contact.pair),
            "raw_feature_option_count": contact.raw_option_count,
            "feature_option_count": len(contact.options),
            "options": [
                {
                    "label": option.label,
                    "aliases": list(option.aliases),
                    "tangent_rows": len(option.rows),
                }
                for option in contact.options
            ],
        }
        for contact in contacts
    ]


def build_result() -> dict:
    started = time.monotonic()
    squares, side, field = trump11.build()
    verification = verify_packing(squares, side, sign=exact_sign)
    if not verification.valid or verification.n != EXPECTED_SQUARES:
        raise ValueError(f"exact Trump witness failed its prerequisite:\n{verification}")
    walls, incidences, centres = wall_rows(squares, side, field)
    contacts = contact_options(squares, centres, field)
    incidental_pairs = incidental_zero_pairs(squares, centres, field)
    if len(incidences) != EXPECTED_WALL_INCIDENCES or len(walls) != EXPECTED_WALL_ROWS:
        raise ValueError(
            f"active wall inventory drifted: {len(incidences)} incidences, {len(walls)} rows"
        )
    if len(contacts) != EXPECTED_CONTACTS:
        raise ValueError(f"active pair inventory drifted: {len(contacts)} contacts")
    wall_table = tuple((item["square"], item["wall"]) for item in incidences)
    contact_table = tuple(contact.pair for contact in contacts)
    raw_option_counts = tuple(contact.raw_option_count for contact in contacts)
    option_counts = tuple(len(contact.options) for contact in contacts)
    if set(wall_table) != set(EXPECTED_WALL_TABLE):
        raise ValueError(f"active wall table drifted: {wall_table}")
    if contact_table != EXPECTED_CONTACT_TABLE:
        raise ValueError(f"active contact table drifted: {contact_table}")
    if raw_option_counts != EXPECTED_RAW_OPTION_COUNTS:
        raise ValueError(f"raw contact-feature counts drifted: {raw_option_counts}")
    if option_counts != EXPECTED_OPTION_COUNTS:
        raise ValueError(f"linearized contact-option counts drifted: {option_counts}")
    if sum(raw_option_counts) != EXPECTED_RAW_FEATURES:
        raise ValueError(f"expected {EXPECTED_RAW_FEATURES} raw features")
    if sum(option_counts) != EXPECTED_LOCAL_OPTIONS:
        raise ValueError(f"expected {EXPECTED_LOCAL_OPTIONS} local linearized options")
    if incidental_pairs != EXPECTED_INCIDENTAL_ZERO_PAIRS:
        raise ValueError(f"incidental zero-projection pair table drifted: {incidental_pairs}")
    raw_branch_count = 1
    reduced_branch_count = 1
    for contact in contacts:
        raw_branch_count *= contact.raw_option_count
        reduced_branch_count *= len(contact.options)
    if raw_branch_count != EXPECTED_RAW_BRANCHES:
        raise ValueError(
            f"expected {EXPECTED_RAW_BRANCHES} raw branches, got {raw_branch_count}"
        )
    if reduced_branch_count != EXPECTED_REDUCED_BRANCHES:
        raise ValueError(
            f"expected {EXPECTED_REDUCED_BRANCHES} derivative-distinct branches, "
            f"got {reduced_branch_count}"
        )

    branch_groups = enumerate_branch_groups(walls, contacts)

    if len(branch_groups) != EXPECTED_REDUCED_BRANCHES:
        raise ValueError(
            f"expected {EXPECTED_REDUCED_BRANCHES} unique matrices, got {len(branch_groups)}"
        )
    if any(len(group["rows"]) != EXPECTED_BRANCH_ROWS for group in branch_groups.values()):
        raise ValueError(f"a branch did not have exactly {EXPECTED_BRANCH_ROWS} rows")
    if sum(group["raw_selection_count"] for group in branch_groups.values()) != (
        EXPECTED_RAW_BRANCHES
    ):
        raise ValueError("the derivative-to-raw branch multiplicities do not sum to 512")

    branch_records = []
    for branch_index, (digest, group) in enumerate(sorted(branch_groups.items())):
        rows = group["rows"]
        certificate = positive_stress_certificate(rows, field)
        if certificate is None:
            direction = exact_nonzero_direction(rows, field)
            branch_records.append(
                {
                    "branch": branch_index,
                    "matrix_sha256": digest,
                    "ordered_matrix_sha256": ordered_matrix_digest(rows),
                    "row_count": len(rows),
                    "derivative_selection_count": len(group["selections"]),
                    "derivative_selections": [
                        list(selection) for selection in group["selections"]
                    ],
                    "raw_selection_count": group["raw_selection_count"],
                    "certificate": None,
                    "exact_nonzero_direction": direction,
                }
            )
            continue
        if not replay_certificate(rows, certificate, field):
            raise AssertionError(f"branch {branch_index} certificate did not replay")
        branch_records.append(
            {
                "branch": branch_index,
                "matrix_sha256": digest,
                "ordered_matrix_sha256": ordered_matrix_digest(rows),
                "row_count": len(rows),
                "derivative_selection_count": len(group["selections"]),
                "derivative_selections": [list(selection) for selection in group["selections"]],
                "raw_selection_count": group["raw_selection_count"],
                "certificate": certificate,
                "exact_nonzero_direction": None,
            }
        )
    certified = sum(record["certificate"] is not None for record in branch_records)
    witnessed_flexible = sum(
        record["exact_nonzero_direction"] is not None for record in branch_records
    )
    all_certified = certified == len(branch_records)
    if all_certified:
        outcome = "criterion_met"
        claim = "all branchwise fixed-side linearized cones are zero"
    elif witnessed_flexible:
        outcome = "criterion_missed"
        claim = "at least one branchwise linearized cone has an exact nonzero vector"
    else:
        outcome = "invalid"
        claim = "one or more branches lack an exact terminal certificate"
    selftests = run_selftests(field, walls, contacts)
    return {
        "schema_version": 1,
        "subject": {
            "n": EXPECTED_SQUARES,
            "side_minimal_polynomial": list(trump11.S_MIN_POLY),
            "field": "Q(u)",
            "field_degree": field.degree,
            "u_minimal_polynomial": list(trump11.U_MIN_POLY),
            "u_isolating_interval": list(trump11.U_INTERVAL),
            "variables": EXPECTED_VARIABLES,
            "fixed_side": True,
        },
        "active_system": {
            "wall_incidences": incidences,
            "wall_incidence_count": len(incidences),
            "wall_tangent_row_count": len(walls),
            "pair_contact_count": len(contacts),
            "raw_feature_count": sum(raw_option_counts),
            "linearized_local_option_count": sum(option_counts),
            "incidental_zero_projection_noncontacts": [list(pair) for pair in incidental_pairs],
            "contacts": contact_records(contacts),
        },
        "branches": {
            "raw_count": raw_branch_count,
            "derivative_distinct_selection_count": reduced_branch_count,
            "unique_matrix_count": len(branch_groups),
            "certified_zero_cones": certified,
            "exact_nonzero_direction_cones": witnessed_flexible,
            "unresolved_cones": len(branch_records) - certified - witnessed_flexible,
            "all_certified": all_certified,
            "records": branch_records,
        },
        "certificate_logic": {
            "statement": (
                "A full-rank row subset plus lambda > 0 with A^T lambda = 0 "
                "proves {v: A v >= 0} = {0}."
            ),
            "numeric_role": "propose free stress weights or a nonzero direction only",
            "decisive_role": (
                "exact Q(u) basis selection, solve, signs, inequalities, and residual replay"
            ),
        },
        "selftests": selftests,
        "determination": {
            "outcome": outcome,
            "claim": claim,
            "scope": DETERMINATION_SCOPE,
        },
        "elapsed_seconds": round(time.monotonic() - started, 6),
    }


def replay_direction(rows, direction_record, field) -> bool:
    direction = [
        field.element([Fraction(coefficient) for coefficient in value])
        for value in direction_record["coordinates_low_degree_first"]
    ]
    coordinate = direction_record["normalizing_coordinate"]
    sign = direction_record["normalizing_sign"]
    return (
        len(direction) == EXPECTED_VARIABLES
        and type(coordinate) is int
        and 0 <= coordinate < EXPECTED_VARIABLES
        and type(sign) is int
        and sign in (-1, 1)
        and direction[coordinate] == field.rational(sign)
        and direction_record.get("all_inequalities_replayed_exactly") is True
        and any(not value.is_zero() for value in direction)
        and all(exact_dot(row.coefficients, direction, field).sign() >= 0 for row in rows)
    )


def replay_result(record: dict) -> dict:
    started = time.monotonic()
    squares, side, field = trump11.build()
    verification = verify_packing(squares, side, sign=exact_sign)
    if not verification.valid or verification.n != EXPECTED_SQUARES:
        raise ValueError("exact Trump witness failed before certificate replay")
    walls, incidences, centres = wall_rows(squares, side, field)
    contacts = contact_options(squares, centres, field)
    if len(incidences) != EXPECTED_WALL_INCIDENCES or len(walls) != EXPECTED_WALL_ROWS:
        raise ValueError("derived wall inventory failed the replay completeness guard")
    if {(item["square"], item["wall"]) for item in incidences} != set(EXPECTED_WALL_TABLE):
        raise ValueError("derived wall table failed the replay completeness guard")
    if tuple(contact.pair for contact in contacts) != EXPECTED_CONTACT_TABLE:
        raise ValueError("derived contact table failed the replay completeness guard")
    if (
        tuple(contact.raw_option_count for contact in contacts) != (EXPECTED_RAW_OPTION_COUNTS)
        or tuple(len(contact.options) for contact in contacts) != EXPECTED_OPTION_COUNTS
    ):
        raise ValueError("derived contact-option table failed replay")
    branch_groups = enumerate_branch_groups(walls, contacts)
    records = record["branches"]["records"]
    if len(records) != EXPECTED_REDUCED_BRANCHES or len(branch_groups) != len(records):
        raise ValueError("record does not cover all 128 derivative-distinct matrices")
    records_by_digest = index_complete_records(records, branch_groups)
    if record["branches"]["raw_count"] != EXPECTED_RAW_BRANCHES:
        raise ValueError("record does not retain all 512 raw nonlinear branches")
    if (
        record["branches"]["derivative_distinct_selection_count"] != (EXPECTED_REDUCED_BRANCHES)
        or record["branches"]["unique_matrix_count"] != EXPECTED_REDUCED_BRANCHES
    ):
        raise ValueError("recorded derivative-branch counts do not match the exact model")
    subject = record["subject"]
    if (
        subject["n"] != EXPECTED_SQUARES
        or subject["side_minimal_polynomial"] != list(trump11.S_MIN_POLY)
        or subject["field"] != "Q(u)"
        or subject["field_degree"] != field.degree
        or subject["u_minimal_polynomial"] != list(trump11.U_MIN_POLY)
        or subject["u_isolating_interval"] != list(trump11.U_INTERVAL)
        or subject["variables"] != EXPECTED_VARIABLES
        or subject["fixed_side"] is not True
    ):
        raise ValueError("recorded number-field metadata drifted")
    if tuple((item["square"], item["wall"]) for item in incidences) != tuple(
        (item["square"], item["wall"]) for item in record["active_system"]["wall_incidences"]
    ):
        raise ValueError("recorded wall incidence order drifted")
    if record["active_system"]["wall_incidences"] != incidences:
        raise ValueError("recorded wall table does not match the exact witness")
    if record["active_system"]["contacts"] != contact_records(contacts):
        raise ValueError("recorded contact-feature table does not match the exact witness")
    active = record["active_system"]
    if (
        active["wall_incidence_count"] != EXPECTED_WALL_INCIDENCES
        or active["wall_tangent_row_count"] != EXPECTED_WALL_ROWS
        or active["pair_contact_count"] != EXPECTED_CONTACTS
        or active["raw_feature_count"] != EXPECTED_RAW_FEATURES
        or active["linearized_local_option_count"] != EXPECTED_LOCAL_OPTIONS
    ):
        raise ValueError("recorded active-system totals do not match the exact model")
    incidental_pairs = incidental_zero_pairs(squares, centres, field)
    if incidental_pairs != EXPECTED_INCIDENTAL_ZERO_PAIRS:
        raise ValueError("derived incidental-zero table failed replay")
    if record["active_system"]["incidental_zero_projection_noncontacts"] != [
        list(pair) for pair in incidental_pairs
    ]:
        raise ValueError("recorded incidental-zero exclusions do not replay")

    replayed_certificates = 0
    replayed_directions = 0
    replayed_unresolved = 0
    for branch_index, (digest, group) in enumerate(sorted(branch_groups.items())):
        branch_record = records_by_digest[digest]
        rows = group["rows"]
        if branch_record["branch"] != branch_index:
            raise ValueError("recorded branch numbering drifted")
        if branch_record["ordered_matrix_sha256"] != ordered_matrix_digest(rows):
            raise ValueError("certificate row order drifted")
        if len(rows) != EXPECTED_BRANCH_ROWS or branch_record["row_count"] != len(rows):
            raise ValueError("recorded branch row count drifted")
        if branch_record["raw_selection_count"] != group["raw_selection_count"]:
            raise ValueError("recorded raw-branch multiplicity drifted")
        selections = [list(item) for item in group["selections"]]
        if (
            branch_record["derivative_selection_count"] != len(selections)
            or branch_record["derivative_selections"] != selections
        ):
            raise ValueError("recorded derivative-selection mapping drifted")
        certificate = branch_record["certificate"]
        direction = branch_record["exact_nonzero_direction"]
        if certificate is not None:
            if direction is not None or not replay_certificate(rows, certificate, field):
                raise ValueError("an exact zero-cone certificate failed replay")
            replayed_certificates += 1
        elif direction is not None:
            if not replay_direction(rows, direction, field):
                raise ValueError("an exact nonzero direction failed replay")
            replayed_directions += 1
        else:
            replayed_unresolved += 1

    if replayed_certificates == EXPECTED_REDUCED_BRANCHES:
        outcome = "criterion_met"
        claim = "all branchwise fixed-side linearized cones are zero"
    elif replayed_directions > 0:
        outcome = "criterion_missed"
        claim = "at least one branchwise linearized cone has an exact nonzero vector"
    else:
        outcome = "invalid"
        claim = "one or more branches lack an exact terminal certificate"
    branches = record["branches"]
    if (
        branches["certified_zero_cones"] != replayed_certificates
        or branches["exact_nonzero_direction_cones"] != replayed_directions
        or branches["unresolved_cones"] != replayed_unresolved
        or branches["all_certified"] != (replayed_certificates == EXPECTED_REDUCED_BRANCHES)
        or record["determination"]["outcome"] != outcome
        or record["determination"]["claim"] != claim
        or record["determination"]["scope"] != DETERMINATION_SCOPE
    ):
        raise ValueError("recorded determination does not match the replayed witnesses")
    selftests = run_selftests(field, walls, contacts)
    if record["selftests"] != selftests:
        raise ValueError("recorded selftest summary does not match the replayed controls")
    return {
        "schema_version": 1,
        "record_replayed": True,
        "branch_count": len(records),
        "raw_branch_count": sum(
            branch_record["raw_selection_count"] for branch_record in records
        ),
        "exact_zero_certificates": replayed_certificates,
        "exact_nonzero_directions": replayed_directions,
        "unresolved_cones": replayed_unresolved,
        "determination_outcome": outcome,
        "selftests": selftests,
        "elapsed_seconds": round(time.monotonic() - started, 6),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    paths = parser.add_mutually_exclusive_group()
    paths.add_argument("--record", type=Path, help="write the JSON evidence record atomically")
    paths.add_argument("--replay", type=Path, help="replay a retained JSON record exactly")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.replay:
        record = json.loads(args.replay.read_text())
        replay = replay_result(record)
        print(json.dumps(replay, indent=2, sort_keys=True))
        return 0 if replay["determination_outcome"] != "invalid" else 1
    result = build_result()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.record:
        args.record.parent.mkdir(parents=True, exist_ok=True)
        temporary = args.record.with_suffix(args.record.suffix + ".tmp")
        temporary.write_text(rendered)
        temporary.replace(args.record)
    print(rendered, end="")
    return 0 if result["determination"]["outcome"] != "invalid" else 1


if __name__ == "__main__":
    raise SystemExit(main())
