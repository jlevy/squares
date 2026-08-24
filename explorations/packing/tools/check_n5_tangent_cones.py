#!/usr/bin/env python3
"""Classify the active first-order cones along exp-033's exact n=5 face.

The checker keeps the distinction that matters for this slice: an exact nonzero vector
in every active linearized inequality is first-order evidence, not a nonlinear motion.
It derives the wall/contact inventory from the exact Q(sqrt(2)) poses, enumerates every
owner/support branch at pair (3,4), and replays explicit endpoint/interior witnesses.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import cast

from strif import atomic_output_file

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from sqpack.field import FieldElement, NumberField
from tools import check_n5_equal_side_face as face

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


@dataclass(frozen=True)
class LinearRow:
    label: str
    coefficients: tuple[FieldElement, ...]


def require_dict(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise TypeError(f"{label} must be an object")
    return cast(dict[str, object], value)


def require_list(value: object, label: str) -> list[object]:
    if not isinstance(value, list):
        raise TypeError(f"{label} must be a list")
    return value


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def contact_rows(
    field: NumberField,
) -> tuple[tuple[LinearRow, ...], tuple[LinearRow, ...]]:
    q0 = field.rational
    r = field.alpha
    q = r / 2 - q0(3) / 4
    am = (-r / 2, r / 2)
    ap = (r / 2, r / 2)
    fixed = (
        row(
            field,
            "contact:0-4:owner4:a-",
            {
                x(4): am[0],
                x(0): -am[0],
                y(4): am[1],
                y(0): -am[1],
                theta(4): q,
            },
        ),
        row(
            field,
            "contact:1-4:owner4:a-",
            {
                x(4): -am[0],
                x(1): am[0],
                y(4): -am[1],
                y(1): am[1],
                theta(4): q,
            },
        ),
        row(
            field,
            "contact:2-4:owner4:a+",
            {
                x(4): -ap[0],
                x(2): ap[0],
                y(4): -ap[1],
                y(2): ap[1],
                theta(4): -q,
            },
        ),
    )
    alternatives: list[LinearRow] = []
    for owner in (3, 4):
        other = 7 - owner
        for feature_sign in (-1, 1):
            values = {
                x(4): ap[0],
                x(3): -ap[0],
                y(4): ap[1],
                y(3): -ap[1],
                theta(owner): q + q0(feature_sign) / 2,
                theta(other): -q0(feature_sign) / 2,
            }
            alternatives.append(
                row(
                    field,
                    f"contact:3-4:owner{owner}:a+:feature{feature_sign:+d}",
                    values,
                )
            )
    return fixed, tuple(alternatives)


def abs_exact(value: FieldElement) -> FieldElement:
    return -value if value.sign() < 0 else value


def dot2(
    left: tuple[FieldElement, FieldElement], right: tuple[FieldElement, FieldElement]
) -> FieldElement:
    return left[0] * right[0] + left[1] * right[1]


def geometry_inventory(field: NumberField) -> dict[str, object]:
    """Derive active walls and owner axes from the exact source poses."""
    q = field.rational
    r = field.alpha
    data = face.exact_data(field)
    side = cast(FieldElement, data["side"])
    endpoint_a = cast(list[tuple[FieldElement, FieldElement]], data["a"])
    endpoint_b = cast(list[tuple[FieldElement, FieldElement]], data["b"])
    midpoint = [
        ((left[0] + right[0]) / 2, (left[1] + right[1]) / 2)
        for left, right in zip(endpoint_a, endpoint_b, strict=True)
    ]
    axes = [
        ((q(1), q(0), "x"), (q(0), q(1), "y")),
        ((q(1), q(0), "x"), (q(0), q(1), "y")),
        ((q(1), q(0), "x"), (q(0), q(1), "y")),
        ((r / 2, r / 2, "a+"), (-r / 2, r / 2, "a-")),
        ((r / 2, r / 2, "a+"), (-r / 2, r / 2, "a-")),
    ]

    def support(index: int, axis: tuple[FieldElement, FieldElement]) -> FieldElement:
        first, second = axes[index]
        u = (first[0], first[1])
        v = (second[0], second[1])
        return (abs_exact(dot2(axis, u)) + abs_exact(dot2(axis, v))) / 2

    zero_axes: set[str] = set()
    for first, second in itertools.combinations(range(5), 2):
        displacement = (
            midpoint[second][0] - midpoint[first][0],
            midpoint[second][1] - midpoint[first][1],
        )
        for owner in (first, second):
            for axis_x, axis_y, axis_name in axes[owner]:
                axis = (axis_x, axis_y)
                separation = abs_exact(dot2(displacement, axis))
                gap = separation - support(first, axis) - support(second, axis)
                if gap.is_zero():
                    zero_axes.add(f"{first}-{second}:owner{owner}:{axis_name}")
    if zero_axes != EXPECTED_ZERO_AXES:
        raise ValueError(f"unexpected exact zero-axis inventory: {sorted(zero_axes)}")

    wall_tables: dict[str, list[str]] = {}
    for name, centres in (("A", endpoint_a), ("interior", midpoint), ("B", endpoint_b)):
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
    return {"wall_labels": wall_tables, "zero_owner_axes": sorted(zero_axes)}


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


def exact_rank(rows: tuple[LinearRow, ...], field: NumberField) -> int:
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


def matrix_digest(rows: tuple[LinearRow, ...]) -> str:
    payload = [
        {"label": item.label, "coefficients": [encode(value) for value in item.coefficients]}
        for item in rows
    ]
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def witness(field: NumberField, stratum: str) -> list[FieldElement]:
    q = field.rational
    delta = 3 * field.alpha / 2 - 2
    values = zero_row(field)
    values[x(4)] = delta / 2
    values[theta(3)] = q(1)
    values[theta(4)] = q(1)
    if stratum == "A":
        values[y(0)] = -delta
    elif stratum in {"interior", "B"}:
        values[x(0)] = delta
    else:
        raise ValueError(f"unknown stratum {stratum}")
    return values


def build_stratum(field: NumberField, stratum: str) -> dict[str, object]:
    walls = wall_rows(field, stratum)
    fixed, alternatives = contact_rows(field)
    direction = witness(field, stratum)
    all_active = (*walls, *fixed, *alternatives)
    derivatives = {item.label: exact_dot(item, direction, field) for item in all_active}
    if any(value.sign() < 0 for value in derivatives.values()):
        raise ValueError(f"the {stratum} witness violates an active inequality")
    if any(not value.is_zero() for value in derivatives.values()):
        raise ValueError(f"the {stratum} witness should maintain every active feature")
    if direction[theta(3)].is_zero() or direction[theta(4)].is_zero():
        raise ValueError("the non-sheet witness lost its diagonal angle motion")
    expected_rank = 12 if stratum == "interior" else 14
    branches: list[dict[str, object]] = []
    for alternative in alternatives:
        rows = (*walls, *fixed, alternative)
        rank = exact_rank(rows, field)
        if rank != expected_rank:
            raise ValueError(f"unexpected {stratum} branch rank {rank}")
        branches.append(
            {
                "selected_contact_3_4": alternative.label,
                "row_count": len(rows),
                "exact_equality_rank": rank,
                "equality_kernel_nullity": VARIABLE_COUNT - rank,
                "matrix_sha256": matrix_digest(rows),
            }
        )
    if len({branch["matrix_sha256"] for branch in branches}) != 4:
        raise ValueError("the four contact branches are not one-to-one")
    return {
        "name": stratum,
        "wall_row_count": len(walls),
        "fixed_contact_row_count": len(fixed),
        "contact_3_4_branch_count": len(alternatives),
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
    if (
        set(require_list(inventory.get("zero_owner_axes"), "zero owner axes"))
        != EXPECTED_ZERO_AXES
    ):
        raise ValueError("the retained zero-owner-axis inventory is incomplete")
    strata = require_list(result.get("strata"), "strata")
    if len(strata) != 3:
        raise ValueError("the retained result does not cover all three strata")
    for expected_name, item in zip(STRATA, strata, strict=True):
        record = require_dict(item, "stratum")
        if record.get("name") != expected_name:
            raise ValueError("stratum order or identity drifted")
        branches = require_list(record.get("branches"), "branches")
        if len(branches) != 4:
            raise ValueError("a stratum does not retain all four SAT branches")
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
            "exp_034_sha256": sha256_file(EXP034),
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
                "every exact endpoint/interior stratum has a complete active-branch "
                "inventory and an exact non-sheet first-order feasible direction"
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
    false_continuation = copy.deepcopy(result)
    require_dict(false_continuation["nonlinear_continuation"], "continuation")["status"] = (
        "proved"
    )
    tampered_source = copy.deepcopy(result)
    require_dict(tampered_source["source"], "source")["exp_034_sha256"] = "0" * 64
    wrong = witness(field, "interior")
    wrong[theta(4)] = -field.one
    wrong_direction_rejected = any(
        exact_dot(item, wrong, field).sign() < 0
        for item in (
            *wall_rows(field, "interior"),
            *contact_rows(field)[0],
            *contact_rows(field)[1],
        )
    )
    selftests = {
        "missing_sat_branch_is_rejected": False,
        "first_order_evidence_cannot_claim_continuation": False,
        "source_digest_tamper_is_rejected": False,
        "wrong_angle_sign_violates_an_active_row": wrong_direction_rejected,
        "non_sheet_direction_has_diagonal_angle_motion": True,
    }
    try:
        validate_result(missing_branch)
    except ValueError:
        selftests["missing_sat_branch_is_rejected"] = True
    try:
        validate_result(false_continuation)
    except ValueError:
        selftests["first_order_evidence_cannot_claim_continuation"] = True
    try:
        require_same_result(tampered_source, result)
    except ValueError:
        selftests["source_digest_tamper_is_rejected"] = True
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
            "sat_branches_per_stratum": 4,
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
    sys.exit(main())
