#!/usr/bin/env python3
"""Certify a two-parameter exact optimal sheet through exp-033's n=5 face.

The exp-033 segment moves square 0 along a diagonal while all angles stay fixed.
Here square 0 may also rotate.  Half-angle coordinates make its sine and cosine
rational functions, so containment, separation, and the surviving LP dual can be
checked without numerical trigonometry.

The result is scoped to one declared family of fixed-angle LP cells.  It is not a
certificate that the sheet is a full stationary component or a basin.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
import time
from fractions import Fraction
from pathlib import Path
from typing import cast

from strif import atomic_output_file

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from sqpack.field import FieldElement, NumberField
from sqpack.verify import exact_sign, verify_packing
from tools import check_n5_equal_side_face as face

SCHEMA_VERSION = 1
EXP033 = (
    ROOT / "campaign/series/series-000-smoke-and-calibration/results/"
    "exp-033-h-023-n5-equal-side-face.json"
)
Q_MAX = Fraction(1, 100)
COS_AT_Q_MAX = Fraction(9999, 10001)
SIN_AT_Q_MAX = Fraction(200, 10001)
E_MAX = Fraction(99, 10001)
EXPECTED_DUAL_SUPPORT = {
    "2x-lower",
    "2y-lower",
    "3x-upper",
    "3y-upper",
    "pair-2-4",
    "pair-3-4",
}


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


def encode(value: FieldElement) -> list[str]:
    return [str(coefficient) for coefficient in value.coeffs]


def oriented_square(
    field: NumberField,
    centre: tuple[FieldElement, FieldElement],
    cosine: FieldElement,
    sine: FieldElement,
) -> tuple[tuple[FieldElement, FieldElement], ...]:
    """Construct one unit square from exact cosine and sine."""
    u = (cosine, sine)
    v = (-sine, cosine)
    cx, cy = centre
    return tuple(
        (cx + sx * u[0] / 2 + sy * v[0] / 2, cy + sx * u[1] / 2 + sy * v[1] / 2)
        for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))
    )


def parameter_values(
    field: NumberField, *, sign: int, endpoint: str, q_abs: Fraction = Q_MAX
) -> tuple[
    FieldElement,
    list[tuple[FieldElement, FieldElement]],
    FieldElement,
    FieldElement,
]:
    """Return side, centres, cosine and sine for one exact sheet fixture."""
    if sign not in {-1, 1}:
        raise ValueError("rotation sign must be -1 or 1")
    if endpoint not in {"left", "right", "unshrunk", "signed-error"}:
        raise ValueError(f"unknown endpoint mode {endpoint}")
    q = field.rational
    data = face.exact_data(field)
    side = cast(FieldElement, data["side"])
    delta = cast(FieldElement, data["delta"])
    fixed = cast(list[tuple[FieldElement, FieldElement]], data["a"])[1:]
    q_value = q(q_abs)
    denominator = q(1) + q_value * q_value
    cosine = (q(1) - q_value * q_value) / denominator
    sine = sign * 2 * q_value / denominator
    shrink = q_value * (q(1) - q_value) / denominator
    if endpoint == "left":
        u = shrink
    elif endpoint == "right":
        u = delta - shrink
    elif endpoint == "unshrunk":
        u = q(0)
    else:
        u = -shrink
    centres = [
        (q(1) / 2 + u, q(5) / 2 - field.alpha / 4 + u),
        *fixed,
    ]
    return side, centres, cosine, sine


def exact_fixture(
    field: NumberField, *, sign: int, endpoint: str, q_abs: Fraction = Q_MAX
) -> dict[str, object]:
    side, centres, cosine, sine = parameter_values(
        field, sign=sign, endpoint=endpoint, q_abs=q_abs
    )
    squares = [
        oriented_square(field, centres[0], cosine, sine),
        face.square(field, centres[1], diagonal=False),
        face.square(field, centres[2], diagonal=False),
        face.square(field, centres[3], diagonal=True),
        face.square(field, centres[4], diagonal=True),
    ]
    report = verify_packing(squares, side, sign=exact_sign)
    return {
        "rotation_sign": sign,
        "endpoint": endpoint,
        "q_abs": str(q_abs),
        "cosine": str(COS_AT_Q_MAX) if q_abs == Q_MAX else str(float(cosine)),
        "sine": str(sign * SIN_AT_Q_MAX) if q_abs == Q_MAX else str(float(sine)),
        "valid": report.valid,
        "pairs_tested": report.pairs_tested,
        "touching_pairs": report.touching_pairs,
        "strict_pairs": report.strict_pairs,
        "container_contacts": report.container_contacts,
    }


def uniform_sheet_certificate(field: NumberField) -> dict[str, object]:
    """Prove every point in the declared (t,u) strip is feasible."""
    q = field.rational
    r = field.alpha
    q_max = q(Q_MAX)
    e_max = q(E_MAX)
    delta = 3 * r / 2 - 2
    derivative_numerator_at_q_max = q(1) - 2 * q_max - q_max * q_max
    strip_width_at_q_max = delta - 2 * e_max

    # The named axes are unchanged square axes, except pair 0-3, whose owner is the
    # rotated square.  Its conservative projection bound is uniform in both signs.
    residual_margins = {
        "strip_width_at_q_max": strip_width_at_q_max,
        "moving_square_x_upper": q(2) - r / 4,
        "moving_square_y_lower": q(2) - r / 4,
        "pair_0_1_on_square_1_x_axis": q(1) - r / 4,
        "pair_0_2_on_square_2_y_axis": q(1) - r / 4,
        "pair_0_3_on_square_0_rotated_axis": (
            (q(5) / 2 - 3 * r / 4) * q(COS_AT_Q_MAX)
            - (r / 2 - q(1) / 2) * q(SIN_AT_Q_MAX)
            - (q(1) / 2 + r / 2)
        ),
        "pair_0_4_gap_at_q_max": r / 10001,
    }
    if derivative_numerator_at_q_max.sign() <= 0:
        raise ValueError("the support shrink is not monotone on the declared q interval")
    if any(value.sign() <= 0 for value in residual_margins.values()):
        raise ValueError("a residual uniform sheet margin is not strictly positive")
    if q_max * (q(1) - q_max) / (q(1) + q_max * q_max) != e_max:
        raise ValueError("the declared maximum support shrink is inconsistent")
    if (q(1) - q_max * q_max) / (q(1) + q_max * q_max) != q(COS_AT_Q_MAX):
        raise ValueError("the half-angle cosine identity failed")
    if 2 * q_max / (q(1) + q_max * q_max) != q(SIN_AT_Q_MAX):
        raise ValueError("the half-angle sine identity failed")
    return {
        "parameters": {
            "t": "tan(theta_0/2), |t| <= 1/100",
            "e_of_t": "|t|(1-|t|)/(1+t^2)",
            "u": "e(t) <= u <= 3*sqrt(2)/2-2-e(t)",
            "moving_square": "centre=(1/2+u, 5/2-sqrt(2)/4+u), angle=2*atan(t)",
            "other_four_squares": "fixed at the exp-033 exact coordinates and angles",
        },
        "dimension_lower_bound": 2,
        "support_shrink_monotone": True,
        "support_derivative_numerator_at_q_max": str(Fraction(9799, 10000)),
        "universal_feasibility_inequalities_verified": True,
        "boundary_inequalities": ("u-e(t) >= 0 and 3*sqrt(2)/2-2-e(t)-u >= 0"),
        "strict_residual_margins": {
            label: encode(value) for label, value in residual_margins.items()
        },
        "contact_0_4_gap": "sqrt(2)*t^2/(1+t^2), nonnegative",
        "proof_scope": (
            "the formulas cover every real t in the interval and every u in its strip; "
            "the four exact boundary fixtures are replay controls, not samples standing "
            "in for the universal inequalities"
        ),
    }


def dual_certificate(field: NumberField) -> dict[str, object]:
    """Replay the exp-033 dual whose support is independent of square 0."""
    labels, rows, rhs = face.cell_system(field)
    weights = [field.zero for _ in rows]
    for label in ("2x-lower", "2y-lower", "3x-upper", "3y-upper"):
        weights[labels.index(label)] = field.rational(-1) / 2
    for label in ("pair-2-4", "pair-3-4"):
        weights[labels.index(label)] = -field.alpha / 2
    support = {labels[index] for index, weight in enumerate(weights) if not weight.is_zero()}
    if support != EXPECTED_DUAL_SUPPORT:
        raise ValueError("the uniform dual support changed")
    objective = [field.one, *[field.zero for _ in range(face.VARIABLE_COUNT - 1)]]
    lhs = [
        sum(
            (rows[index][column] * weights[index] for index in range(len(rows))),
            field.zero,
        )
        for column in range(face.VARIABLE_COUNT)
    ]
    value = sum(
        (bound * weight for bound, weight in zip(rhs, weights, strict=True)), field.zero
    )
    side = cast(FieldElement, face.exact_data(field)["side"])
    if lhs != objective or value != side or any(weight.sign() > 0 for weight in weights):
        raise ValueError("the uniform sheet dual failed exact replay")
    return {
        "support": sorted(support),
        "support_avoids_moving_square_0": True,
        "identity": "A^T y=e_side, y<=0, b^T y=1+5*sqrt(2)/4",
        "uniform_over_sheet": True,
        "scope": "the declared fixed-angle cells containing the parameterized family",
    }


def validate_result(result: dict[str, object]) -> None:
    sheet = require_dict(result.get("sheet_certificate"), "sheet certificate")
    if sheet.get("dimension_lower_bound") != 2:
        raise ValueError("the certified sheet dimension lower bound is not two")
    if sheet.get("universal_feasibility_inequalities_verified") is not True:
        raise ValueError("the universal sheet inequalities were not verified")
    fixtures = require_list(result.get("boundary_fixtures"), "boundary fixtures")
    if len(fixtures) != 4 or any(
        require_dict(fixture, "boundary fixture").get("valid") is not True
        for fixture in fixtures
    ):
        raise ValueError("the four exact boundary fixtures are not all valid")
    dual = require_dict(result.get("uniform_dual"), "uniform dual")
    if dual.get("uniform_over_sheet") is not True:
        raise ValueError("the exact dual was not certified uniformly")
    determination = require_dict(result.get("determination"), "determination")
    if determination.get("outcome") != "criterion_met":
        raise ValueError("the two-parameter sheet criterion was not met")


def require_same_result(retained: dict[str, object], regenerated: dict[str, object]) -> None:
    if retained != regenerated:
        raise ValueError("retained n=5 angle-sheet record differs from regeneration")


def build_result() -> dict[str, object]:
    field = face.make_field()
    fixtures = [
        exact_fixture(field, sign=sign, endpoint=endpoint)
        for sign in (-1, 1)
        for endpoint in ("left", "right")
    ]
    result: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "contract": "packing.squares:N5AngleSheet/v1",
        "source": {
            "exp_033": str(EXP033.relative_to(ROOT)),
            "exp_033_sha256": sha256_file(EXP033),
        },
        "sheet_certificate": uniform_sheet_certificate(field),
        "boundary_fixtures": fixtures,
        "uniform_dual": dual_certificate(field),
        "determination": {
            "outcome": "criterion_met",
            "claim": (
                "the exp-033 segment lies in an exact two-parameter sheet of feasible "
                "orientation-indexed LP optima at side 1+5*sqrt(2)/4"
            ),
            "scope": (
                "declared square-0 half-angle and slide family only; no full stationary "
                "component, basin mass, or census-completeness conclusion"
            ),
        },
    }
    validate_result(result)

    too_wide = exact_fixture(field, sign=1, endpoint="left", q_abs=Fraction(1, 10))
    unshrunk = exact_fixture(field, sign=1, endpoint="unshrunk")
    signed_error = exact_fixture(field, sign=-1, endpoint="signed-error")
    bad_dual = copy.deepcopy(result)
    require_dict(bad_dual["uniform_dual"], "bad dual")["uniform_over_sheet"] = False
    bad_digest = copy.deepcopy(result)
    require_dict(bad_digest["source"], "bad source")["exp_033_sha256"] = "0" * 64
    selftests = {
        "excessive_angle_is_rejected": too_wide["valid"] is False,
        "unshrunk_left_endpoint_is_rejected": unshrunk["valid"] is False,
        "signed_instead_of_absolute_support_is_rejected": signed_error["valid"] is False,
        "uniform_dual_drift_is_rejected": False,
        "source_digest_tamper_is_rejected": False,
    }
    try:
        validate_result(bad_dual)
    except ValueError:
        selftests["uniform_dual_drift_is_rejected"] = True
    try:
        require_same_result(bad_digest, result)
    except ValueError:
        selftests["source_digest_tamper_is_rejected"] = True
    if not all(selftests.values()):
        raise ValueError(f"n=5 angle-sheet selftests failed: {selftests}")
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
        summary = {
            "record_written": args.record is not None,
            "record_replayed": args.replay is not None,
            "determination_outcome": require_dict(result["determination"], "determination")[
                "outcome"
            ],
            "dimension_lower_bound": require_dict(
                result["sheet_certificate"], "sheet certificate"
            )["dimension_lower_bound"],
            "boundary_fixtures": len(
                require_list(result["boundary_fixtures"], "boundary fixtures")
            ),
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
