"""Audit BC-240's retained arithmetic without executing either Trump generator.

The exact field and tangent row inventory are shared primitives. Gradients, rational
caps, row factors, stress constants, and selected primal/dual face checks are computed
here; no isolation-radius helper or tangent replay function is called. Missing radius
face witnesses remain retained premises, even when the selected face checks succeed.
"""

from __future__ import annotations

import argparse
import ast
import json
import math
import subprocess
import time
from dataclasses import dataclass, replace
from fractions import Fraction
from pathlib import Path
from typing import Any, cast

import numpy as np
from scipy.optimize import linprog

from cases.trump11 import packing as trump
from cases.trump11 import tangent_cones as tangent
from sqpack.exact_lp import LinearRow, solve_square_system
from sqpack.field import FieldElement, NumberField

PACKING = Path(__file__).resolve().parents[1]
REPO = PACKING.parent
RESULTS = "packing/campaign/series/series-000-smoke-and-calibration/results/"
TANGENT = RESULTS + "exp-013-h-026-trump-tangent.json"
RADIUS = RESULTS + "bc-199-trump-isolation-radius.json"
THEOREM = RESULTS + "bc-240-trump-local-theorem.json"
REVIEW_REVISION = "f9ba790a2a60b990d20261cc2645595d78740dcc"
ARCHIVE = "01ca830a041a5cc94f8a9c20eaf9f965bf40b88e"
DIMENSION = 33
SQRT_TWO_UP = Fraction(14143, 10000)
WALL_CURVATURE = Fraction(7072, 10000)
type Point = tuple[FieldElement, FieldElement]


class ReviewError(ValueError):
    """A named retained premise or independent arithmetic identity failed."""


def require(condition: object, message: str) -> None:
    if not condition:
        raise ReviewError(message)


def load_records() -> tuple[dict[str, Any], dict[str, Any]]:
    return json.loads((REPO / RADIUS).read_text()), json.loads((REPO / THEOREM).read_text())


def git_content(revision: str, path: str) -> bytes:
    """Read repository evidence at its reviewed Git revision and path."""
    return subprocess.run(
        ["git", "show", f"{revision}:{path}"], cwd=REPO, check=True, capture_output=True
    ).stdout


def pivot_argument_semantics(source: bytes) -> str:
    """Account for the documented removal of an unused pivot-helper argument."""
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "exact_pivot_rows":
            require(
                not any(
                    isinstance(child, ast.Name) and child.id == "field"
                    for statement in node.body
                    for child in ast.walk(statement)
                ),
                "exact_pivot_rows field argument is used",
            )
            node.args.args = [
                argument for argument in node.args.args if argument.arg != "field"
            ]
        elif isinstance(node, ast.Call):
            function = node.func
            name = (
                function.id
                if isinstance(function, ast.Name)
                else (function.attr if isinstance(function, ast.Attribute) else None)
            )
            if (
                name == "exact_pivot_rows"
                and len(node.args) == 2
                and isinstance(node.args[-1], ast.Name)
                and node.args[-1].id == "field"
            ):
                node.args.pop()
    return ast.dump(tree)


def check_source_binding(input_root: Path = REPO) -> dict[str, Any]:
    """Compare full input contents and the two declared source changes against Git."""
    theorem = json.loads(git_content(REVIEW_REVISION, THEOREM))
    paths = list(
        dict.fromkeys(
            (
                TANGENT,
                RADIUS,
                THEOREM,
                theorem["theorem_document"],
                *theorem["inputs"],
            )
        )
    )
    reviewed = {path: git_content(REVIEW_REVISION, path) for path in paths}
    for path, expected in reviewed.items():
        require((input_root / path).read_bytes() == expected, f"input content mismatch: {path}")
    unchanged = [TANGENT, RADIUS, "packing/cases/trump11/packing.py"]
    for path in unchanged:
        require(reviewed[path] == git_content(ARCHIVE, path), f"archived input changed: {path}")
    drift = []
    for path, description in (
        (
            "packing/cases/trump11/tangent_cones.py",
            "Unused exact_pivot_rows field argument and its caller arguments removed.",
        ),
        (
            "packing/cases/trump11/isolation_radius.py",
            "Two caller arguments removed; Archimedes-bound provenance comment expanded.",
        ),
    ):
        archived = git_content(ARCHIVE, path)
        require(
            pivot_argument_semantics(reviewed[path]) == pivot_argument_semantics(archived),
            f"undeclared source drift: {path}",
        )
        drift.append(
            {
                "path": path,
                "content_changed": reviewed[path] != archived,
                "declared_change": description,
                "semantics_match": True,
                "comparison": (
                    "Complete syntax trees after removing the unused pivot-helper argument; "
                    "comments carry no executable syntax."
                ),
            }
        )
    return {
        "review_revision": REVIEW_REVISION,
        "input_paths": paths,
        "comparison": "Complete file contents equal their reviewed Git revision and path.",
        "archive_revision": ARCHIVE,
        "retained_inputs_unchanged_since_archive": unchanged,
        "declared_source_drift": drift,
    }


def outward(value: Fraction, digits: int, *, upper: bool = False) -> Fraction:
    scaled = value * 10**digits
    units = (
        -((-scaled.numerator) // scaled.denominator)
        if upper
        else scaled.numerator // scaled.denominator
    )
    return Fraction(units, 10**digits)


def check_aggregate(record: dict, theorem: dict) -> dict[str, Any]:
    """Recompute exact minima and outward rounding from retained rational premises."""
    shared = {
        "declared_box": Fraction(record["box_sup_radius"]),
        "gap_to_lipschitz": Fraction(record["gaps"]["cap_rational_lower"]),
        "symmetry_half_distance": Fraction(record["symmetry"]["threshold"]) / 2,
    }
    require(
        shared["symmetry_half_distance"] == Fraction(record["symmetry"]["radius"]),
        "symmetry half-distance",
    )
    require(
        record["symmetry"]["certified_distance_at_least_threshold"] is True,
        "retained symmetry guard",
    )
    for key, value in shared.items():
        require(Fraction(record["rho_0"]["candidates"][key]) == value, f"shared cap {key}")
    uniform_modulus = Fraction(record["modulus"]["two_kappa_over_K_rational_lower"])
    require(
        uniform_modulus == Fraction(record["rho_0"]["candidates"]["modulus_2kappa_over_K"]),
        "uniform modulus cap",
    )
    weighted_modulus = Fraction(record["rho_0_weighted"]["per_row_K_modulus_rational_lower"])
    radii = {}
    for key, cap_name, modulus in (
        ("rho_0", "modulus_2kappa_over_K", uniform_modulus),
        ("rho_0_weighted", "modulus_per_row_K", weighted_modulus),
    ):
        caps = {**shared, cap_name: modulus}
        exact_minimum = min(caps.values())
        require(
            exact_minimum == Fraction(record[key]["rational_lower_bound"]),
            f"{key} aggregate minimum",
        )
        require(record[key]["binding"] == min(caps, key=caps.__getitem__), f"{key} binding cap")
        rounded = outward(exact_minimum, 12)
        require(
            rounded == Fraction(record[key]["rational_lower_bound_short"]),
            f"{key} lower rounding",
        )
        require(
            rounded <= exact_minimum < rounded + Fraction(1, 10**12), f"{key} outward interval"
        )
        radii[key] = str(rounded)
    constants = theorem["constants"]
    require(
        Fraction(radii["rho_0"])
        == Fraction(constants["uniform"]["radius_rational_lower_bound"]),
        "uniform radius",
    )
    require(
        Fraction(radii["rho_0_weighted"])
        == Fraction(constants["per_row_preferred"]["radius_rational_lower_bound"]),
        "preferred radius",
    )
    quadratic = {}
    for key, published in (("uniform_K", "uniform"), ("per_row_K", "per_row_preferred")):
        upper = Fraction(record["C"][key + "_rational_upper"])
        rounded = outward(upper, 9, upper=True)
        require(
            rounded == Fraction(record["C"][key + "_rational_upper_short"]),
            f"{key} upper rounding",
        )
        require(
            rounded
            == Fraction(constants[published]["quadratic_constant_rational_upper_bound"]),
            f"{key} published C",
        )
        require(rounded - Fraction(1, 10**9) < upper <= rounded, f"{key} outward interval")
        quadratic[key] = str(rounded)
    require(
        outward(shared["gap_to_lipschitz"], 12)
        == Fraction(record["gaps"]["cap_rational_lower_short"]),
        "gap cap lower rounding",
    )
    require(
        theorem["chart"]["variables"] == DIMENSION
        and theorem["chart"]["side_fixed"] is True
        and theorem["chart"]["labels_fixed"] is True,
        "fixed-side labelled chart",
    )
    require(
        theorem["claim_boundary"]["retained_bc199_text"] == record["claim_boundary"],
        "local-only claim boundary",
    )
    return {
        "shared_caps": {key: str(value) for key, value in shared.items()},
        "uniform_radius": radii["rho_0"],
        "preferred_radius": radii["rho_0_weighted"],
        "uniform_quadratic_constant": quadratic["uniform_K"],
        "preferred_quadratic_constant": quadratic["per_row_K"],
        "outward_rounding_verified": True,
        "weighted_modulus_premise": (
            "Retained aggregate exact rational; no per-branch algebraic weighted "
            "witnesses are present."
        ),
        "gap_and_symmetry_premises": (
            "Retained geometric guards; their shared-cap arithmetic is checked here, "
            "their full producers are not replayed."
        ),
    }


@dataclass
class Context:
    field: NumberField
    squares: list[list[Point]]
    centres: list[Point]
    side: FieldElement
    branches: list[tuple[LinearRow, ...]]
    certificates: dict[int, dict]


def load_context() -> Context:
    squares, side, field = trump.build()
    walls, _, centres = tangent.wall_rows(squares, side, field)
    contacts = tangent.contact_options(squares, centres, field)
    groups = tangent.enumerate_branch_groups(walls, contacts)
    branches = [group["rows"] for _, group in sorted(groups.items())]
    require(
        len(branches) == 128 and all(len(rows) == 42 for rows in branches), "branch inventory"
    )
    record = json.loads((REPO / TANGENT).read_text())
    certificates = {
        item["branch"]: item["certificate"] for item in record["branches"]["records"]
    }
    require(set(certificates) == set(range(128)), "retained branch IDs")
    field.refine_to(48)
    return Context(field, squares, cast("list[Point]", centres), side, branches, certificates)


def dot(left, right, zero: FieldElement) -> FieldElement:
    return sum((a * b for a, b in zip(left, right, strict=True) if not a.is_zero()), zero)


def row_curvature(context: Context, row: LinearRow) -> Fraction:
    """Differentiate the tied elementary margin independently of tangent row assembly."""
    field = context.field
    parts = row.label.split(":")
    gradient = [field.zero for _ in range(DIMENSION)]
    if parts[0] == "wall":
        square = int(parts[1])
        wall = parts[2]
        corner = int(parts[3].removeprefix("corner-"))
        point = context.squares[square][corner]
        centre = context.centres[square]
        coordinate = int(wall in ("bottom", "top"))
        direction = 1 if wall in ("left", "bottom") else -1
        margin = point[coordinate] if direction == 1 else context.side - point[coordinate]
        gradient[3 * square + coordinate] = field.rational(direction)
        gradient[3 * square + 2] = (
            direction * (point[0] - centre[0])
            if coordinate
            else -direction * (point[1] - centre[1])
        )
        curvature = WALL_CURVATURE
    else:
        first, second = (int(value) for value in parts[1].split("-"))
        owner = int(parts[2].removeprefix("owner-"))
        axis_index = int(parts[3].removeprefix("axis-"))
        other = first + second - owner
        epsilon = 1 if other == (second if parts[4] == "first-before-second" else first) else -1
        corner_map = {
            int(square): int(corner)
            for square, corner in (
                value.split(".") for value in parts[5].removeprefix("vertices-").split("-")
            )
        }
        point = context.squares[other][corner_map[other]]
        owner_corners = context.squares[owner]
        edge = (0, 1) if axis_index == 0 else (1, 2)
        edge_x, edge_y = (
            owner_corners[edge[1]][i] - owner_corners[edge[0]][i] for i in range(2)
        )
        axis = (-edge_y, edge_x)
        require(
            (dot(axis, axis, field.zero) - 1).is_zero(), f"unit separating axis: {row.label}"
        )
        displacement = tuple(point[i] - context.centres[owner][i] for i in range(2))
        radius = tuple(point[i] - context.centres[other][i] for i in range(2))
        margin = epsilon * dot(axis, displacement, field.zero) - Fraction(1, 2)
        for coordinate in range(2):
            gradient[3 * other + coordinate] = epsilon * axis[coordinate]
            gradient[3 * owner + coordinate] = -epsilon * axis[coordinate]
        gradient[3 * other + 2] = epsilon * (-axis[0] * radius[1] + axis[1] * radius[0])
        gradient[3 * owner + 2] = epsilon * (
            -axis[1] * displacement[0] + axis[0] * displacement[1]
        )
        distance = tuple(
            context.centres[other][i] - context.centres[owner][i] for i in range(2)
        )
        _, distance_squared_up = field.enclose(dot(distance, distance, field.zero))
        numerator = distance_squared_up.numerator * 10**18
        denominator = distance_squared_up.denominator
        root = math.isqrt(numerator // denominator)
        root += int(root * root * denominator < numerator)
        distance_up = Fraction(root, 10**9)
        require(distance_up**2 >= distance_squared_up, "exact centre-distance upper bound")
        curvature = distance_up + (Fraction(2, 64) + 6) * SQRT_TWO_UP
    require(margin.is_zero(), f"elementary margin is not tied: {row.label}")
    require(
        all((a - b).is_zero() for a, b in zip(gradient, row.coefficients, strict=True)),
        f"active-row coefficient mismatch: {row.label}",
    )
    return curvature


def check_factor(curvature: Fraction, factor: Fraction) -> None:
    """Check normalization before allowing any radius comparison to use the factor."""
    require(curvature > 0 and factor > 0, "nonpositive norm factor or curvature")
    product = factor * curvature
    require(product == 2, f"norm factor product is {product}, expected 2")


def check_stress(rows, stress: list[FieldElement], field: NumberField) -> None:
    require(
        len(stress) == len(rows) and all(weight.sign() > 0 for weight in stress),
        "stress positivity",
    )
    for coordinate in range(DIMENSION):
        residual = dot([row.coefficients[coordinate] for row in rows], stress, field.zero)
        require(residual.is_zero(), f"retained stress residual at coordinate {coordinate}")


def reconstruct_stress(context: Context, branch: int) -> list[FieldElement]:
    rows, field = context.branches[branch], context.field
    certificate = context.certificates[branch]
    pivots = certificate["pivot_rows"]
    free = {int(key): Fraction(value) for key, value in certificate["free_weights"].items()}
    require(
        len(pivots) == DIMENSION and len(set(pivots)) == DIMENSION,
        f"branch {branch} pivot basis",
    )
    require(
        set(pivots).isdisjoint(free) and set(pivots) | set(free) == set(range(len(rows))),
        f"branch {branch} stress partition",
    )
    matrix = [
        [rows[index].coefficients[column] for index in pivots] for column in range(DIMENSION)
    ]
    rhs = [
        -sum(
            (rows[index].coefficients[column] * weight for index, weight in free.items()),
            field.zero,
        )
        for column in range(DIMENSION)
    ]
    solved = cast("list[FieldElement]", solve_square_system(matrix, rhs, field.one))
    stress = [field.zero for _ in rows]
    for index, value in free.items():
        stress[index] = field.rational(value)
    for index, value in zip(pivots, solved, strict=True):
        stress[index] = value
    check_stress(rows, stress, field)
    return stress


def branch_constants(
    context: Context, branch: int, curvatures: dict
) -> tuple[FieldElement, FieldElement, list[FieldElement]]:
    rows, field = context.branches[branch], context.field
    stress = reconstruct_stress(context, branch)
    far = [
        index
        for index, row in enumerate(rows)
        if row.label.startswith("wall:") and row.label.split(":")[2] in ("right", "top")
    ]
    near = [
        index
        for index, row in enumerate(rows)
        if row.label.startswith("wall:") and index not in far
    ]
    far_stress = sum((stress[index] for index in far), field.zero)
    near_stress = sum((stress[index] for index in near), field.zero)
    require(
        far_stress.sign() > 0 and (near_stress - far_stress).is_zero(),
        f"branch {branch} wall stress",
    )
    uniform = sum(stress, field.zero) * max(curvatures.values()) / (2 * far_stress)
    weighted = sum(
        (
            weight * curvatures[tangent.row_key(row)]
            for row, weight in zip(rows, stress, strict=True)
        ),
        field.zero,
    ) / (2 * far_stress)
    return uniform, weighted, stress


def independent_basis(matrix: list[list[FieldElement]]) -> list[int]:
    echelon: dict[int, list[FieldElement]] = {}
    selected = []
    for index, source_row in enumerate(matrix):
        row = list(source_row)
        for pivot, basis_row in echelon.items():
            if not row[pivot].is_zero():
                factor = row[pivot]
                row = [a - factor * b for a, b in zip(row, basis_row, strict=True)]
        pivot = next((i for i, value in enumerate(row) if not value.is_zero()), None)
        if pivot is not None:
            divisor = row[pivot]
            echelon[pivot] = [value / divisor for value in row]
            selected.append(index)
        if len(selected) == len(source_row):
            break
    return selected


def selected_face(
    context: Context, branch: int, curvatures: dict, record: dict, *, weighted: bool
) -> dict[str, Any]:
    """Audit one declared face by an exact feasible primal and simplex dual equality."""
    field = context.field
    retained = record["branches"][branch]
    face = retained["rho_weighted_argmin_face" if weighted else "kappa_argmin_face"]
    coordinate, sign = face["coordinate"], face["sign"]
    source_rows = context.branches[branch]
    factors = [
        2 / curvatures[tangent.row_key(row)] if weighted else Fraction(1) for row in source_rows
    ]
    if weighted:
        for row, factor in zip(source_rows, factors, strict=True):
            check_factor(curvatures[tangent.row_key(row)], factor)
    rows = [
        [value * factor for value in row.coefficients]
        for row, factor in zip(source_rows, factors, strict=True)
    ]
    matrix = np.array([[float(value) for value in row] for row in rows])
    bounds = [(-1.0, 1.0)] * DIMENSION + [(None, None)]
    bounds[coordinate] = (float(sign), float(sign))
    proposal = linprog(
        np.r_[np.zeros(DIMENSION), 1.0],
        A_ub=np.c_[-matrix, -np.ones(len(rows))],
        b_ub=np.zeros(len(rows)),
        bounds=bounds,
        method="highs",
    )
    if not proposal.success or proposal.x is None:
        raise ReviewError(f"selected face proposal branch {branch}")
    point_float = proposal.x[:DIMENSION]
    fixed = {
        index: field.rational(1 if value > 0 else -1)
        for index, value in enumerate(point_float)
        if index == coordinate or abs(value) > 1 - 1e-7
    }
    fixed[coordinate] = field.rational(sign)
    free = [index for index in range(DIMENSION) if index not in fixed]
    active = [
        index
        for index, residual in enumerate(matrix @ point_float + proposal.x[-1])
        if abs(residual) < 1e-7
    ]
    # A degenerate vertex admits bases with negative dual weights. Preserve the
    # proposed positive dual support first; all subsequent decisions remain exact.
    active.sort(key=lambda index: (proposal.ineqlin.marginals[index] >= -1e-8, index))
    equations = [[*(rows[index][column] for column in free), field.one] for index in active]
    selected = independent_basis(equations)
    require(len(selected) == len(free) + 1, f"selected face exact rank branch {branch}")
    basis = [active[index] for index in selected]
    coefficients = [equations[index] for index in selected]
    rhs = [
        -sum((rows[index][column] * value for column, value in fixed.items()), field.zero)
        for index in basis
    ]
    solution = cast("list[FieldElement]", solve_square_system(coefficients, rhs, field.one))
    point = [fixed.get(index, field.zero) for index in range(DIMENSION)]
    for column, value in zip(free, solution[:-1], strict=True):
        point[column] = value
    require(
        all(value >= -1 and value <= 1 for value in point), f"selected face box branch {branch}"
    )
    require(
        (point[coordinate] - sign).is_zero(), f"selected face normalization branch {branch}"
    )
    upper = max(-dot(row, point, field.zero) for row in rows)
    dual_matrix = [list(column) for column in zip(*coefficients, strict=True)]
    dual = cast(
        "list[FieldElement]",
        solve_square_system(dual_matrix, [field.zero] * len(free) + [field.one], field.one),
    )
    require(
        all(weight.sign() >= 0 for weight in dual) and (sum(dual, field.zero) - 1).is_zero(),
        f"selected face simplex dual branch {branch}, weighted={weighted}",
    )
    products = [
        dot([rows[index][column] for index in basis], dual, field.zero)
        for column in range(DIMENSION)
    ]
    lower = -sign * products[coordinate] - sum(
        (
            value if value.sign() >= 0 else -value
            for index, value in enumerate(products)
            if index != coordinate
        ),
        field.zero,
    )
    require((upper - lower).is_zero(), f"selected face primal-dual gap branch {branch}")
    if not weighted:
        expected = field.element([Fraction(value) for value in retained["kappa_lower"]])
        require(
            (lower - expected).is_zero(),
            f"selected uniform face retained modulus branch {branch}",
        )
    else:
        require(
            lower >= Fraction(record["rho_0_weighted"]["per_row_K_modulus_rational_lower"]),
            f"selected weighted face below retained aggregate branch {branch}",
        )
    return {
        "branch": branch,
        "weighted": weighted,
        "coordinate": coordinate,
        "sign": sign,
        "free_coordinates": free,
        "basis_rows": basis,
        "primal_point_coefficients": [[str(value) for value in item.coeffs] for item in point],
        "dual_on_basis_coefficients": [[str(value) for value in item.coeffs] for item in dual],
        "exact_value_coefficients": [str(value) for value in lower.coeffs],
        "value_decimal": field.decimal(lower, 30),
        "primal_feasible": True,
        "simplex_dual_feasible": True,
        "exact_primal_dual_gap": "0",
        "scope": (
            "This single face only; it does not check the other 65 faces "
            "or certify the all-branch weighted minimum."
        ),
    }


def run_review() -> dict[str, Any]:
    started, cpu_started = time.perf_counter(), time.process_time()
    binding = check_source_binding()
    record, theorem = load_records()
    aggregate = check_aggregate(record, theorem)
    context = load_context()
    field = context.field
    distinct = {tangent.row_key(row): row for rows in context.branches for row in rows}
    curvatures = {key: row_curvature(context, row) for key, row in distinct.items()}
    require(
        max(curvatures.values()) == Fraction(record["curvature"]["K"]),
        "uniform curvature maximum",
    )
    require(Fraction(record["curvature"]["K_wall"]) == WALL_CURVATURE, "wall curvature")
    factors = []
    for key, row in distinct.items():
        curvature = curvatures[key]
        factor = 2 / curvature
        check_factor(curvature, factor)
        factors.append(
            {
                "row": row.label,
                "K_j": str(curvature),
                "factor_j": str(factor),
                "factor_times_K": "2",
            }
        )
    kappas = [
        field.element([Fraction(value) for value in item["kappa_lower"]])
        for item in record["branches"]
    ]
    minimum = min(kappas)
    uniform_radius = minimum * 2 / max(curvatures.values())
    rational_radius = Fraction(record["modulus"]["two_kappa_over_K_rational_lower"])
    require(uniform_radius >= rational_radius, "retained uniform modulus lower enclosure")
    radius_low, radius_high = field.enclose(uniform_radius)
    require(
        outward(radius_low, 12)
        == outward(radius_high, 12)
        == Fraction(record["rho_0"]["rational_lower_bound_short"]),
        "independently rounded uniform radius",
    )
    all_uniform, all_weighted, retained_stress = [], [], None
    for branch in range(128):
        uniform, weighted, stress = branch_constants(context, branch, curvatures)
        all_uniform.append(uniform)
        all_weighted.append(weighted)
        if branch == 0:
            retained_stress = stress
    for key, values in (("uniform_K", all_uniform), ("per_row_K", all_weighted)):
        upper = Fraction(record["C"][key + "_rational_upper"])
        computed = max(values)
        require(computed <= upper, f"{key} retained C upper enclosure")
        computed_low, computed_high = field.enclose(computed)
        require(
            outward(computed_low, 9, upper=True)
            == outward(computed_high, 9, upper=True)
            == Fraction(record["C"][key + "_rational_upper_short"]),
            f"{key} independently rounded quadratic constant",
        )
    rows = context.branches[0]
    if retained_stress is None:
        raise ReviewError("missing branch-zero retained stress")
    mutations = []
    index = next(i for i, row in enumerate(rows) if row.label.startswith("pair:"))
    original = rows[index]
    coefficients = list(original.coefficients)
    changed_column = next(i for i, value in enumerate(coefficients) if not value.is_zero())
    coefficients[changed_column] = coefficients[changed_column] + 1
    changed_row = replace(original, coefficients=tuple(coefficients))
    reversed_rows = list(rows)
    reversed_rows[index] = replace(
        original, coefficients=tuple(-value for value in original.coefficients)
    )
    factor_curvature = curvatures[tangent.row_key(original)]
    checks = (
        ("active_row_coefficient", lambda: row_curvature(context, changed_row)),
        (
            "separating_axis_sign_retaining_stress",
            lambda: check_stress(reversed_rows, retained_stress, field),
        ),
        (
            "per_row_factor_2_over_K_to_1_over_K",
            lambda: check_factor(factor_curvature, 1 / factor_curvature),
        ),
    )
    for name, check in checks:
        try:
            check()
        except ReviewError as error:
            mutations.append(
                {
                    "control": name,
                    "branch": 0,
                    "row_index": index,
                    "row_label": original.label,
                    "rejected": True,
                    "reason": str(error),
                }
            )
        else:
            raise ReviewError(f"falsifying mutation accepted: {name}")
    faces = [
        selected_face(context, branch, curvatures, record, weighted=weighted)
        for branch in (0, 4)
        for weighted in (False, True)
    ]
    return {
        "disposition": "accept_retained_record_dependent_local_scope",
        "source_binding": binding,
        "archived_source_audit": {
            "revision": ARCHIVE,
            "source": "packing/cases/trump11/isolation_radius.py",
            "functions_read": [
                "elementary_functions",
                "identify_rows",
                "face_lp",
                "dual_lower_bound",
                "primal_upper_bound",
                "exact_vertex_refinement",
                "stress_constants",
                "build_result",
            ],
            "independent_formulas": (
                "Differentiated signed support margin and curvature bounds; exact primal "
                "box feasibility and simplex weak duality on four selected faces; "
                "all-branch stress ratios and rational cap/outward-rounding arithmetic."
            ),
            "generator_imported_or_executed": False,
        },
        "aggregate_arithmetic": aggregate,
        "branch_arithmetic": {
            "branches_checked": 128,
            "minimum_kappa_coefficients": [str(value) for value in minimum.coeffs],
            "uniform_modulus_conversion": (
                "2*min(kappa_b)/max(K_j), in the original 33-coordinate sup norm"
            ),
            "uniform_C_formula": "max_b(sum(lambda_b)*K/(2*Lambda_far_b))",
            "per_row_C_formula": "max_b(sum_j(lambda_bj*K_j)/(2*Lambda_far_b))",
            "uniform_C_decimal": field.decimal(max(all_uniform), 30),
            "per_row_C_decimal": field.decimal(max(all_weighted), 30),
            "uniform_C_coefficients": [str(value) for value in max(all_uniform).coeffs],
            "per_row_C_coefficients": [str(value) for value in max(all_weighted).coeffs],
            "published_short_constants_independently_rounded": True,
            "all_stresses_positive_with_exact_zero_residual": True,
            "near_and_far_wall_stresses_equal": True,
        },
        "row_audit": {
            "distinct_rows_checked": len(distinct),
            "all_tied_elementary_gradients_match": True,
            "factors": factors,
        },
        "mutations": mutations,
        "selected_faces": faces,
        "radius_generator_executed": False,
        "tangent_replay_executed_by_this_checker": False,
        "unreviewed_generator_obligations": [
            "Complete 128-by-66 uniform and weighted radius face witnesses are absent.",
            (
                "The retained weighted aggregate rational is not independently recovered "
                "from every weighted face."
            ),
            (
                "Full inactive-gap and symmetry geometry producers are not rerun; "
                "retained guards are exact input premises."
            ),
        ],
        "claim_scope": theorem["claim_boundary"],
        "wall_seconds": round(time.perf_counter() - started, 6),
        "cpu_seconds": round(time.process_time() - cpu_started, 6),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    try:
        result = run_review()
    except ReviewError as error:
        print(json.dumps({"disposition": "refused", "reason": str(error)}, indent=2))
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
