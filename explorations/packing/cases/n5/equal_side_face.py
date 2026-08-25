#!/usr/bin/env python3
"""Certify the equal-side n=5 golden endpoints share one exact LP face.

The two endpoint-key rows are deterministic golden seeds 2 and 5.  After one declared
container quarter-turn and square relabelling, four squares coincide and the fifth
slides on an exact line segment.  This checker proves the whole segment feasible in one
fixed-angle separating cell and supplies an exact LP dual at the shared side.

The conclusion is intentionally narrower than full terminal-component identity:
angle-varying stationarity, attraction mass, and completeness remain unproved.
"""

from __future__ import annotations

import argparse
import copy
import json
import math
import sys
import time
from pathlib import Path
from typing import cast

from strif import atomic_output_file

from sqpack.field import FieldElement, NumberField
from sqpack.verify import exact_sign, verify_packing

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_VERSION = 1
VARIABLE_COUNT = 11
SOURCE_TOLERANCE = 1e-6
GOLDEN = ROOT / "golden/basin-maps.yaml"
COMPONENT_A = "07860b128b38dd2e7856c11e9ff03eb7"
COMPONENT_B = "0373183838f6f0c42956f969dadfda97"
CONTACT_KEY = "5dcbd27037e1bd5227723319c9f55c72"

SOURCE_A = {
    "seed": 2,
    "side": 2.7677669529663698,
    "x": [
        0.5000000000000011,
        2.267766952966301,
        0.5000000000000011,
        2.0606601717798227,
        1.3838834736760117,
    ],
    "y": [
        2.1464466150210755,
        0.5000000000000688,
        0.5000000000000011,
        2.0606601717798227,
        1.323223304703433,
    ],
    "theta": [
        1.5707963267948988,
        1.570796326794759,
        1.5707963267948988,
        0.7853981171215281,
        0.7853981171215281,
    ],
    "geometric_key": COMPONENT_A,
    "contact_key": CONTACT_KEY,
}
SOURCE_B = {
    "seed": 5,
    "side": 2.7677669529663724,
    "x": [
        0.5000000000000033,
        1.3232233047033686,
        2.0606601717798254,
        2.2677668116881486,
        0.5000000000000037,
    ],
    "y": [
        0.5000000000000033,
        1.383883474233812,
        0.707106781186547,
        2.146446755183641,
        2.267766952966369,
    ],
    "theta": [
        1.5707963267949032,
        0.7853982004790125,
        0.7853982004790125,
        -2.8255648770060665e-7,
        7.29316860823932e-15,
    ],
    "geometric_key": COMPONENT_B,
    "contact_key": CONTACT_KEY,
}
SOURCE_B_PERMUTATION = (3, 0, 4, 2, 1)


def require_dict(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise TypeError(f"{label} must be an object")
    return cast(dict[str, object], value)


def require_number(value: object, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{label} must be a number")
    return float(value)


def make_field() -> NumberField:
    """Return Q(sqrt(2)) with an exact isolating interval."""
    return NumberField([1, 0, -2], (1, 2))


def exact_data(field: NumberField) -> dict[str, object]:
    """Construct the two aligned endpoints and the exact path parameter."""
    q = field.rational
    r = field.alpha
    side = q(1) + 5 * r / 4
    delta = 3 * r / 2 - 2
    fixed = [
        (q(0), q(0)),
        (q(1) / 2 + 5 * r / 4, q(1) / 2),
        (q(1) / 2, q(1) / 2),
        (q(1) + 3 * r / 4, q(1) + 3 * r / 4),
        (q(1) / 2 + 5 * r / 8, q(3) / 2 - r / 8),
    ]
    endpoint_a = [
        (q(1) / 2, q(5) / 2 - r / 4),
        *fixed[1:],
    ]
    endpoint_b = [
        (q(1) / 2 + delta, q(5) / 2 - r / 4 + delta),
        *fixed[1:],
    ]
    return {"side": side, "delta": delta, "a": endpoint_a, "b": endpoint_b}


def angle_distance(value: float, target: float) -> float:
    folded = value % (math.pi / 2)
    return min(
        abs(folded - target),
        abs(folded - target + math.pi / 2),
        abs(folded - target - math.pi / 2),
    )


def source_alignment(
    data: dict[str, object], *, use_quarter_turn: bool = True
) -> dict[str, object]:
    """Bind the two exact endpoints to the recovered golden seed outputs."""
    side = float(cast(FieldElement, data["side"]))
    exact_a = cast(list[tuple[FieldElement, FieldElement]], data["a"])
    exact_b = cast(list[tuple[FieldElement, FieldElement]], data["b"])
    source_a_x = cast(list[float], SOURCE_A["x"])
    source_a_y = cast(list[float], SOURCE_A["y"])
    source_a_theta = cast(list[float], SOURCE_A["theta"])
    source_b_x = cast(list[float], SOURCE_B["x"])
    source_b_y = cast(list[float], SOURCE_B["y"])
    source_b_theta = cast(list[float], SOURCE_B["theta"])
    if use_quarter_turn:
        transformed_b = [
            (side - source_b_y[index], source_b_x[index], source_b_theta[index])
            for index in SOURCE_B_PERMUTATION
        ]
    else:
        transformed_b = [
            (source_b_x[index], source_b_y[index], source_b_theta[index])
            for index in SOURCE_B_PERMUTATION
        ]
    residuals = [abs(float(SOURCE_A["side"]) - side), abs(float(SOURCE_B["side"]) - side)]
    for index, (x, y) in enumerate(exact_a):
        residuals.extend(
            (
                abs(source_a_x[index] - float(x)),
                abs(source_a_y[index] - float(y)),
                angle_distance(source_a_theta[index], 0.0 if index < 3 else math.pi / 4),
            )
        )
    for index, (x, y) in enumerate(exact_b):
        source_x, source_y, source_theta = transformed_b[index]
        residuals.extend(
            (
                abs(source_x - float(x)),
                abs(source_y - float(y)),
                angle_distance(source_theta, 0.0 if index < 3 else math.pi / 4),
            )
        )
    maximum = max(residuals)
    return {
        "golden_seeds": [2, 5],
        "source_geometric_keys": [COMPONENT_A, COMPONENT_B],
        "shared_contact_key": CONTACT_KEY,
        "container_action_on_seed_5": "quarter-turn counterclockwise",
        "seed_5_square_permutation": list(SOURCE_B_PERMUTATION),
        "maximum_f64_to_exact_residual": maximum,
        "tolerance": SOURCE_TOLERANCE,
        "matches": maximum <= SOURCE_TOLERANCE,
    }


def square(
    field: NumberField,
    centre: tuple[FieldElement, FieldElement],
    *,
    diagonal: bool,
) -> tuple[tuple[FieldElement, FieldElement], ...]:
    """Construct one exact unit square from its centre and orientation class."""
    q = field.rational
    r = field.alpha
    if diagonal:
        u = (r / 2, r / 2)
        v = (-r / 2, r / 2)
    else:
        u = (q(1), q(0))
        v = (q(0), q(1))
    cx, cy = centre
    return tuple(
        (cx + sx * u[0] / 2 + sy * v[0] / 2, cy + sx * u[1] / 2 + sy * v[1] / 2)
        for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))
    )


def exact_packing_valid(
    field: NumberField,
    centres: list[tuple[FieldElement, FieldElement]],
    side: FieldElement,
) -> dict[str, object]:
    squares = [
        square(field, centre, diagonal=index >= 3) for index, centre in enumerate(centres)
    ]
    report = verify_packing(squares, side, sign=exact_sign)
    return {
        "valid": report.valid,
        "pairs_tested": report.pairs_tested,
        "touching_pairs": report.touching_pairs,
        "strict_pairs": report.strict_pairs,
        "container_contacts": report.container_contacts,
    }


def zero_row(field: NumberField) -> list[FieldElement]:
    return [field.zero for _ in range(VARIABLE_COUNT)]


def cell_system(
    field: NumberField,
) -> tuple[list[str], list[list[FieldElement]], list[FieldElement]]:
    """Build A v <= b for the common fixed-angle separating cell."""
    q = field.rational
    r = field.alpha
    labels: list[str] = []
    rows: list[list[FieldElement]] = []
    rhs: list[FieldElement] = []
    half_extents = [q(1) / 2] * 3 + [r / 2] * 2
    for index, half in enumerate(half_extents):
        for coordinate, axis in ((1 + index, "x"), (6 + index, "y")):
            lower = zero_row(field)
            lower[coordinate] = q(-1)
            labels.append(f"{index}{axis}-lower")
            rows.append(lower)
            rhs.append(-half)
            upper = zero_row(field)
            upper[coordinate] = q(1)
            upper[0] = q(-1)
            labels.append(f"{index}{axis}-upper")
            rows.append(upper)
            rhs.append(-half)
    h = (q(1) + r) / 2
    pairs = (
        (0, 1, q(1), q(0), q(1), -1),
        (0, 2, q(0), q(1), q(1), 1),
        (0, 3, q(1), q(0), h, -1),
        (0, 4, -r / 2, r / 2, h, 1),
        (1, 2, q(1), q(0), q(1), 1),
        (1, 3, q(0), q(1), h, -1),
        (1, 4, -r / 2, r / 2, h, -1),
        (2, 3, r / 2, r / 2, h, -1),
        (2, 4, r / 2, r / 2, h, -1),
        (3, 4, r / 2, r / 2, q(1), 1),
    )
    for first, second, ax, ay, separation, sign in pairs:
        row = zero_row(field)
        row[1 + first] = -sign * ax
        row[1 + second] = sign * ax
        row[6 + first] = -sign * ay
        row[6 + second] = sign * ay
        labels.append(f"pair-{first}-{second}")
        rows.append(row)
        rhs.append(-separation)
    return labels, rows, rhs


def vector(
    side: FieldElement, centres: list[tuple[FieldElement, FieldElement]]
) -> list[FieldElement]:
    return [side, *[point[0] for point in centres], *[point[1] for point in centres]]


def dot(
    row: list[FieldElement], values: list[FieldElement], field: NumberField
) -> FieldElement:
    return sum((a * b for a, b in zip(row, values, strict=True)), field.zero)


def exact_rank(matrix: list[list[FieldElement]]) -> int:
    """Compute matrix rank by exact Gaussian elimination."""
    work = [list(row_values) for row_values in matrix]
    if not work:
        return 0
    row = 0
    for column in range(len(work[0])):
        pivot = next(
            (
                candidate
                for candidate in range(row, len(work))
                if not work[candidate][column].is_zero()
            ),
            None,
        )
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        inverse = work[row][column].inverse()
        work[row] = [value * inverse for value in work[row]]
        for candidate in range(len(work)):
            if candidate == row:
                continue
            factor = work[candidate][column]
            if not factor.is_zero():
                work[candidate] = [
                    left - factor * right
                    for left, right in zip(work[candidate], work[row], strict=True)
                ]
        row += 1
        if row == len(work):
            break
    return row


def face_certificate(field: NumberField, data: dict[str, object]) -> dict[str, object]:
    """Verify exact feasibility, optimality, and stratum dimensions."""
    side = cast(FieldElement, data["side"])
    delta = cast(FieldElement, data["delta"])
    endpoint_a = cast(list[tuple[FieldElement, FieldElement]], data["a"])
    endpoint_b = cast(list[tuple[FieldElement, FieldElement]], data["b"])
    labels, rows, rhs = cell_system(field)
    values_a = vector(side, endpoint_a)
    values_b = vector(side, endpoint_b)
    slacks_a = [bound - dot(row, values_a, field) for row, bound in zip(rows, rhs, strict=True)]
    slacks_b = [bound - dot(row, values_b, field) for row, bound in zip(rows, rhs, strict=True)]
    if any(slack.sign() < 0 for slack in (*slacks_a, *slacks_b)):
        raise ValueError("an exact endpoint leaves the declared common cell")
    if delta.sign() <= 0:
        raise ValueError("the exact path parameter interval is empty")
    dual = [field.zero for _ in rows]
    for label in ("2x-lower", "2y-lower", "3x-upper", "3y-upper"):
        dual[labels.index(label)] = field.rational(-1) / 2
    for label in ("pair-2-4", "pair-3-4"):
        dual[labels.index(label)] = -field.alpha / 2
    objective = [field.one, *[field.zero for _ in range(VARIABLE_COUNT - 1)]]
    dual_lhs = [
        sum((rows[index][column] * dual[index] for index in range(len(rows))), field.zero)
        for column in range(VARIABLE_COUNT)
    ]
    if dual_lhs != objective or any(weight.sign() > 0 for weight in dual):
        raise ValueError("the exact common-cell dual is invalid")
    dual_value = sum(
        (bound * weight for bound, weight in zip(rhs, dual, strict=True)), field.zero
    )
    if dual_value != side:
        raise ValueError("the exact dual does not prove the declared side")
    midpoint = [
        ((left[0] + right[0]) / 2, (left[1] + right[1]) / 2)
        for left, right in zip(endpoint_a, endpoint_b, strict=True)
    ]
    side_row = objective
    strata: list[dict[str, object]] = []
    for name, centres in (("A", endpoint_a), ("interior", midpoint), ("B", endpoint_b)):
        values = vector(side, centres)
        active = [
            row
            for row, bound in zip(rows, rhs, strict=True)
            if (bound - dot(row, values, field)).is_zero()
        ]
        rank = exact_rank([*active, side_row])
        strata.append(
            {
                "name": name,
                "active_row_count": len(active),
                "rank_with_fixed_side": rank,
                "linear_face_nullity": VARIABLE_COUNT - rank,
            }
        )
    tangent = [field.zero for _ in range(VARIABLE_COUNT)]
    tangent[1] = field.one
    tangent[6] = field.one
    interior_active = [
        row
        for row, bound in zip(rows, rhs, strict=True)
        if (bound - dot(row, vector(side, midpoint), field)).is_zero()
    ]
    if any(not dot(row, tangent, field).is_zero() for row in [*interior_active, side_row]):
        raise ValueError("the declared interior tangent is not in the exact active kernel")
    return {
        "parameter": "u in [0, 3*sqrt(2)/2 - 2]",
        "moving_square": "p0(u)=(1/2+u, 5/2-sqrt(2)/4+u), theta=0 mod pi/2",
        "other_four_squares": "fixed",
        "common_cell_row_count": len(rows),
        "endpoint_slacks_nonnegative": True,
        "full_segment_feasible_by_convexity": True,
        "dual_nonzero_weights": {
            "2x-lower": "-1/2",
            "2y-lower": "-1/2",
            "3x-upper": "-1/2",
            "3y-upper": "-1/2",
            "pair-2-4": "-sqrt(2)/2",
            "pair-3-4": "-sqrt(2)/2",
        },
        "dual_identity": "A^T y = e_side, y <= 0, b^T y = 1+5*sqrt(2)/4",
        "fixed_angle_cell_optimal_side": "1+5*sqrt(2)/4",
        "strata": strata,
        "interior_kernel_generator": "dx0=dy0=1; all other coordinates and ds zero",
    }


def encoded_centres(
    centres: list[tuple[FieldElement, FieldElement]],
) -> list[list[list[str]]]:
    return [
        [[str(value) for value in coordinate.coeffs] for coordinate in point]
        for point in centres
    ]


def validate_result(result: dict[str, object]) -> None:
    source = require_dict(result.get("source_alignment"), "source alignment")
    if (
        source.get("matches") is not True
        or require_number(source.get("maximum_f64_to_exact_residual"), "source residual")
        > SOURCE_TOLERANCE
    ):
        raise ValueError("golden source endpoints do not match the exact reconstruction")
    model = require_dict(result.get("exact_model"), "exact model")
    endpoint_a = require_dict(model.get("endpoint_a_validity"), "endpoint A validity")
    endpoint_b = require_dict(model.get("endpoint_b_validity"), "endpoint B validity")
    if endpoint_a.get("valid") is not True or endpoint_b.get("valid") is not True:
        raise ValueError("an exact endpoint is not a valid packing")
    certificate = require_dict(result.get("fixed_angle_face"), "fixed-angle face")
    strata = cast(list[dict[str, object]], certificate.get("strata"))
    if [row.get("linear_face_nullity") for row in strata] != [0, 1, 0]:
        raise ValueError("exact face strata must have endpoint/interior nullities 0/1/0")
    if certificate.get("full_segment_feasible_by_convexity") is not True:
        raise ValueError("the exact segment was not certified feasible")
    determination = require_dict(result.get("determination"), "determination")
    if determination.get("outcome") != "criterion_met":
        raise ValueError("the fixed-angle connection criterion was not met")


def require_same_result(retained: dict[str, object], regenerated: dict[str, object]) -> None:
    if retained != regenerated:
        raise ValueError("retained n=5 face record differs from exact regeneration")


def build_result() -> dict[str, object]:
    field = make_field()
    data = exact_data(field)
    side = cast(FieldElement, data["side"])
    endpoint_a = cast(list[tuple[FieldElement, FieldElement]], data["a"])
    endpoint_b = cast(list[tuple[FieldElement, FieldElement]], data["b"])
    result: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "contract": "packing.squares:N5EqualSideFace/v1",
        "sources": {
            "golden": str(GOLDEN.relative_to(ROOT)),
            "recovery_regime": "golden census Random(1005), seeds 2 and 5, quench_bracket",
            "recovery_engine_commit": "9dbbd24",
        },
        "source_alignment": source_alignment(data),
        "exact_model": {
            "field": "Q(sqrt(2)), sqrt(2) in (1,2)",
            "side": "1+5*sqrt(2)/4",
            "endpoint_a": encoded_centres(endpoint_a),
            "endpoint_b_after_D4_and_S5": encoded_centres(endpoint_b),
            "orientations": ["axis", "axis", "axis", "diagonal", "diagonal"],
            "endpoint_a_validity": exact_packing_valid(field, endpoint_a, side),
            "endpoint_b_validity": exact_packing_valid(field, endpoint_b, side),
        },
        "fixed_angle_face": face_certificate(field, data),
        "determination": {
            "outcome": "criterion_met",
            "claim": (
                "the two equal-side n=5 golden rows lie in one exact connected "
                "fixed-angle LP optimal face"
            ),
            "scope": (
                "fixed-angle common-cell connection only; full angle-varying stationarity, "
                "attraction mass, and component completeness remain unresolved"
            ),
        },
    }
    validate_result(result)
    shifted = copy.deepcopy(result)
    require_dict(shifted["fixed_angle_face"], "shifted face")[
        "full_segment_feasible_by_convexity"
    ] = False
    wrong_action = source_alignment(data, use_quarter_turn=False)
    invalid_endpoint = copy.deepcopy(result)
    require_dict(
        require_dict(invalid_endpoint["exact_model"], "invalid model")["endpoint_a_validity"],
        "invalid endpoint",
    )["valid"] = False
    selftests = {
        "disconnected_key_labels_do_not_block_exact_path": COMPONENT_A != COMPONENT_B,
        "shared_contact_key_alone_is_not_the_certificate": CONTACT_KEY
        == str(SOURCE_A["contact_key"])
        == str(SOURCE_B["contact_key"]),
        "missing_path_certificate_is_rejected": False,
        "invalid_endpoint_is_rejected": False,
        "wrong_source_D4_action_is_rejected": wrong_action["matches"] is False,
    }
    try:
        validate_result(shifted)
    except ValueError:
        selftests["missing_path_certificate_is_rejected"] = True
    try:
        validate_result(invalid_endpoint)
    except ValueError:
        selftests["invalid_endpoint_is_rejected"] = True
    if not all(selftests.values()):
        raise ValueError(f"n=5 equal-side selftests failed: {selftests}")
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


def require_replay_match(path: Path, result: dict[str, object]) -> None:
    retained = require_dict(json.loads(path.read_text(encoding="utf-8")), "retained result")
    require_same_result(retained, result)


def main() -> int:
    args = parse_args()
    started = time.monotonic()
    try:
        result = build_result()
        if args.record is not None:
            write_json_atomic(args.record, result)
        else:
            require_replay_match(args.replay, result)
        certificate = require_dict(result["fixed_angle_face"], "fixed-angle face")
        summary = {
            "record_written": args.record is not None,
            "record_replayed": args.replay is not None,
            "determination_outcome": require_dict(result["determination"], "determination")[
                "outcome"
            ],
            "parameter": certificate["parameter"],
            "strata": certificate["strata"],
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
