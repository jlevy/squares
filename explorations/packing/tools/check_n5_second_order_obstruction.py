#!/usr/bin/env python3
"""Certify a second-order obstruction to exp-035's displayed n=5 direction.

The certificate is deliberately narrower than a local-rigidity result.  It proves that
the one exact direction retained by exp-035 is in the branchwise linearized systems but
not in the Bouligand tangent cone of fixed-side feasible packings.  It does not classify
the other first-order directions or the full stationary component.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
import time
from collections.abc import Callable
from pathlib import Path
from typing import cast

from strif import atomic_output_file

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from sqpack.field import FieldElement, NumberField
from tools import check_n5_equal_side_face as face

SCHEMA_VERSION = 1
EXP035 = (
    ROOT / "campaign/series/series-000-smoke-and-calibration/results/"
    "exp-035-h-023-n5-tangent-cones.json"
)
STRATA = ("A", "interior", "B")
OWNER_BRANCHES = ("owner3:a+", "owner4:a+")
EXPECTED_ZERO_AXES = {
    "0-4:owner4:a-",
    "1-4:owner4:a-",
    "2-4:owner4:a+",
    "3-4:owner3:a+",
    "3-4:owner4:a+",
}
REQUIRED_COMMON_ROWS = {
    "wall:2:x-lower:+",
    "wall:2:x-lower:-",
    "wall:2:y-lower:+",
    "wall:2:y-lower:-",
    "wall:3:x-upper",
    "wall:3:y-upper",
    "contact:2-4:owner4:a+",
}
SCOPE = (
    "only the displayed exp-035 direction at strata A/interior/B; other non-sheet "
    "directions, local isolation, component identity, basin mass, census completeness, "
    "and unequal-side clearance remain unresolved"
)


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


def abs_exact(value: FieldElement) -> FieldElement:
    return -value if value.sign() < 0 else value


def dot2(
    left: tuple[FieldElement, FieldElement],
    right: tuple[FieldElement, FieldElement],
) -> FieldElement:
    return left[0] * right[0] + left[1] * right[1]


def load_exp035() -> dict[str, object]:
    return require_dict(json.loads(EXP035.read_text(encoding="utf-8")), "exp-035")


def row_labels(branch: dict[str, object]) -> set[str]:
    labels: set[str] = set()
    for item in require_list(branch.get("inequalities"), "branch inequalities"):
        row = require_dict(item, "branch inequality")
        label = row.get("label")
        if not isinstance(label, str):
            raise TypeError("branch inequality label must be a string")
        labels.add(label)
    return labels


def validate_exp035_source(source: dict[str, object]) -> list[dict[str, object]]:
    """Check every exp-035 datum on which the asymptotic argument depends."""
    determination = require_dict(source.get("determination"), "source determination")
    if determination.get("outcome") != "criterion_met":
        raise ValueError("exp-035 did not retain its first-order criterion")
    continuation = require_dict(
        source.get("nonlinear_continuation"), "source nonlinear continuation"
    )
    if continuation.get("status") != "unresolved":
        raise ValueError("exp-035 continuation status drifted")

    inventory = require_dict(source.get("active_inventory"), "source inventory")
    axis_tables = require_dict(
        inventory.get("zero_owner_axes_by_stratum"), "source zero-axis tables"
    )
    strata = [
        require_dict(item, "source stratum")
        for item in require_list(source.get("strata"), "source strata")
    ]
    if [item.get("name") for item in strata] != list(STRATA):
        raise ValueError("exp-035 stratum identity or order drifted")

    for stratum, name in zip(strata, STRATA, strict=True):
        axes = set(require_list(axis_tables.get(name), f"{name} zero axes"))
        if axes != EXPECTED_ZERO_AXES:
            raise ValueError(f"exp-035 {name} zero-axis inventory drifted")
        direction = require_dict(stratum.get("non_sheet_direction"), "source direction")
        variables = require_list(direction.get("variables"), "source variables")
        coordinates = require_list(
            direction.get("coordinates_low_degree_first"), "source coordinates"
        )
        if len(coordinates) != 15 or variables[13:] != ["dtheta3", "dtheta4"]:
            raise ValueError(f"exp-035 {name} direction coordinates drifted")
        if coordinates[13] != ["1", "0"] or coordinates[14] != ["1", "0"]:
            raise ValueError(f"exp-035 {name} direction lost its common angle speed")
        if direction.get("all_active_derivatives_exactly_zero") is not True:
            raise ValueError(f"exp-035 {name} direction is no longer first-order tight")

        branches = [
            require_dict(item, "source owner branch")
            for item in require_list(stratum.get("branches"), "source branches")
        ]
        if [item.get("selected_contact_3_4_owner_axis") for item in branches] != list(
            OWNER_BRANCHES
        ):
            raise ValueError(f"exp-035 {name} owner-axis branches drifted")
        for branch, owner in zip(branches, OWNER_BRANCHES, strict=True):
            if branch.get("tied_support_row_count") != 2:
                raise ValueError(f"exp-035 {name} lost a tied support row")
            labels = row_labels(branch)
            if not REQUIRED_COMMON_ROWS.issubset(labels):
                raise ValueError(f"exp-035 {name} lost a wall or pair-24 row")
            owner_prefix = f"contact:3-4:{owner}:"
            if sum(label.startswith(owner_prefix) for label in labels) != 2:
                raise ValueError(f"exp-035 {name} {owner} support rows drifted")
    return strata


def exact_certificate(field: NumberField) -> dict[str, object]:
    """Derive the Q(sqrt(2)) constants in the two branch contradictions."""
    q = field.rational
    r = field.alpha
    data = face.exact_data(field)
    side = cast(FieldElement, data["side"])
    centres = cast(list[tuple[FieldElement, FieldElement]], data["a"])
    p2, p3, p4 = centres[2], centres[3], centres[4]
    a = (r / 2, r / 2)
    a_perp = (-r / 2, r / 2)
    displacement_24 = (p4[0] - p2[0], p4[1] - p2[1])
    displacement_34 = (p4[0] - p3[0], p4[1] - p3[1])
    transverse_24 = dot2(displacement_24, a_perp)
    separation_24 = dot2(displacement_24, a)
    separation_34 = dot2(displacement_34, a)
    relative_angle_margin = q(1) / 2 - abs_exact(transverse_24)
    width_second_order = -r / 2
    owner4_excess = width_second_order / 2 - (3 * width_second_order / (2 * r * r))
    owner3_upper = (side - r) * width_second_order
    owner3_lower = width_second_order
    owner3_gap = owner3_upper - owner3_lower
    owner3_obstruction = -owner3_gap

    expected = {
        "side": q(1) + 5 * r / 4,
        "p2_lower_wall_x": q(1) / 2,
        "p2_lower_wall_y": q(1) / 2,
        "p3_upper_wall_x": side - r / 2,
        "p3_upper_wall_y": side - r / 2,
        "pair_2_4_axis_separation": (r + q(1)) / 2,
        "pair_2_4_transverse_projection": r / 2 - q(3) / 4,
        "pair_3_4_axis_projection": -q(1),
        "relative_angle_margin": r / 2 - q(1) / 4,
        "width_second_order": -r / 2,
        "owner4_excess_second_order": r / 8,
        "owner3_upper_second_order": -r / 2 - q(1) / 4,
        "owner3_lower_second_order": -r / 2,
        "owner3_gap_second_order": -q(1) / 4,
        "owner3_obstruction_margin": q(1) / 4,
    }
    actual = {
        "side": side,
        "p2_lower_wall_x": p2[0],
        "p2_lower_wall_y": p2[1],
        "p3_upper_wall_x": p3[0],
        "p3_upper_wall_y": p3[1],
        "pair_2_4_axis_separation": separation_24,
        "pair_2_4_transverse_projection": transverse_24,
        "pair_3_4_axis_projection": separation_34,
        "relative_angle_margin": relative_angle_margin,
        "width_second_order": width_second_order,
        "owner4_excess_second_order": owner4_excess,
        "owner3_upper_second_order": owner3_upper,
        "owner3_lower_second_order": owner3_lower,
        "owner3_gap_second_order": owner3_gap,
        "owner3_obstruction_margin": owner3_obstruction,
    }
    if actual != expected:
        raise ValueError("the exact n=5 obstruction constants drifted")
    if owner4_excess.sign() <= 0:
        raise ValueError("the owner-4 second-order excess is not positive")
    if owner3_gap.sign() >= 0 or owner3_obstruction.sign() <= 0:
        raise ValueError("the owner-3 second-order gap is not obstructed")
    if relative_angle_margin.sign() <= 0:
        raise ValueError("the owner-3 relative-angle cusp has no positive margin")

    return {
        "constants_low_degree_first": {name: encode(value) for name, value in actual.items()},
        "asymptotic_normalization": {
            "parameter": "t -> 0+",
            "theta_3": "pi/4 + t + o(t)",
            "theta_4": "pi/4 + t + o(t)",
            "w_i": "cos(theta_i)+sin(theta_i)=sqrt(2)-(sqrt(2)/2)t^2+o(t^2)",
            "delta": "theta_3-theta_4=o(t)",
        },
        "owner4_branch": {
            "necessary_inequality": ("S >= 1+w3/2+(1+(cos(delta)+abs(sin(delta)))/2)/w4"),
            "weaker_nearby_inequality": "S >= 1+w3/2+3/(2*w4)",
            "right_minus_left": "(sqrt(2)/8)t^2+o(t^2)",
            "common_angle_factorization": ("1+w/2+3/(2*w)-S=(w-sqrt(2))*(w-3*sqrt(2)/2)/(2*w)"),
            "contradiction": True,
        },
        "owner3_branch": {
            "necessary_upper_bound": "p3.a3 <= (S-w3/2)*w3",
            "necessary_lower_chain": (
                "p3.a3 >= w3/2+cos(delta)*(w4+1)/2+sin(delta)*(q+O(t))"
                "+1/2+(cos(delta)+abs(sin(delta)))/2"
            ),
            "relative_cusp": "q*delta+abs(delta)/2 >= margin*abs(delta)",
            "upper_minus_lower": "-(1/4)t^2+o(t^2)-margin*abs(delta)",
            "contradiction": True,
        },
        "branch_exhaustion": {
            "pair_2_4": (
                "owner4:a+ is its only zero SAT axis at the base, so continuity forces "
                "that separating axis nearby"
            ),
            "pair_3_4": (
                "only owner3:a+ and owner4:a+ are zero at the base; every feasible "
                "sequence has a subsequence using one of those two axes"
            ),
        },
    }


def validate_result(result: dict[str, object]) -> None:
    if result.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("obstruction schema version drifted")
    source = require_dict(result.get("source"), "source")
    if source.get("exp_035_sha256") != sha256_file(EXP035):
        raise ValueError("exp-035 source digest is stale")
    if source.get("exp_035") != str(EXP035.relative_to(ROOT)):
        raise ValueError("exp-035 source path drifted")

    field = face.make_field()
    expected_certificate = exact_certificate(field)
    if result.get("certificate") != expected_certificate:
        raise ValueError("the retained exact obstruction certificate drifted")
    certificate = require_dict(result.get("certificate"), "certificate")
    constants = require_dict(
        certificate.get("constants_low_degree_first"), "certificate constants"
    )
    if constants.get("owner4_excess_second_order") != encode(field.alpha / 8):
        raise ValueError("the owner-4 obstruction coefficient is not positive and exact")
    if constants.get("relative_angle_margin") != encode(
        field.alpha / 2 - field.rational(1) / 4
    ):
        raise ValueError("the relative-angle margin is not positive and exact")
    if constants.get("owner3_gap_second_order") != encode(-field.rational(1) / 4):
        raise ValueError("the owner-3 second-order gap is not negative and exact")

    determination = require_dict(result.get("determination"), "determination")
    if determination.get("outcome") != "criterion_met":
        raise ValueError("the second-order obstruction criterion was not met")
    if determination.get("scope") != SCOPE:
        raise ValueError("the determination overstates or changes its scope")


def require_same_result(retained: dict[str, object], regenerated: dict[str, object]) -> None:
    if retained != regenerated:
        raise ValueError("retained n=5 second-order record differs from regeneration")


def mutation_rejected(
    result: dict[str, object], mutate: Callable[[dict[str, object]], None]
) -> bool:
    candidate = copy.deepcopy(result)
    mutate(candidate)
    try:
        validate_result(candidate)
    except (TypeError, ValueError):
        return True
    return False


def build_result() -> dict[str, object]:
    source = load_exp035()
    source_strata = validate_exp035_source(source)
    field = face.make_field()
    result: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "contract": "packing.squares:N5SecondOrderObstruction/v1",
        "source": {
            "exp_035": str(EXP035.relative_to(ROOT)),
            "exp_035_sha256": sha256_file(EXP035),
            "validated_strata": [item["name"] for item in source_strata],
            "validated_owner_branches": list(OWNER_BRANCHES),
            "field": "Q(sqrt(2)), sqrt(2) in (1,2)",
        },
        "certificate": exact_certificate(field),
        "determination": {
            "outcome": "criterion_met",
            "claim": (
                "the displayed exp-035 common-angle direction is not a Bouligand "
                "tangent of the fixed-side feasible set at A, the interior, or B"
            ),
            "interpretation": (
                "the branchwise linearized cone strictly contains the true tangent "
                "cone in this direction; this is an Abadie-type equality failure for "
                "the retained disjunctive local model"
            ),
            "scope": SCOPE,
        },
    }
    validate_result(result)

    def tamper_source(candidate: dict[str, object]) -> None:
        require_dict(candidate["source"], "source")["exp_035_sha256"] = "0" * 64

    def tamper_owner4(candidate: dict[str, object]) -> None:
        constants = require_dict(
            require_dict(candidate["certificate"], "certificate")["constants_low_degree_first"],
            "constants",
        )
        constants["owner4_excess_second_order"] = ["0", "0"]

    def tamper_margin(candidate: dict[str, object]) -> None:
        constants = require_dict(
            require_dict(candidate["certificate"], "certificate")["constants_low_degree_first"],
            "constants",
        )
        constants["relative_angle_margin"] = ["0", "0"]

    def overclaim(candidate: dict[str, object]) -> None:
        require_dict(candidate["determination"], "determination")["scope"] = (
            "the full n=5 component is locally isolated"
        )

    source_missing_branch = copy.deepcopy(source)
    first_stratum = require_dict(
        require_list(source_missing_branch["strata"], "strata")[0], "first stratum"
    )
    require_list(first_stratum["branches"], "branches").pop()
    source_wrong_direction = copy.deepcopy(source)
    middle_stratum = require_dict(
        require_list(source_wrong_direction["strata"], "strata")[1], "middle stratum"
    )
    coordinates = require_list(
        require_dict(middle_stratum["non_sheet_direction"], "direction")[
            "coordinates_low_degree_first"
        ],
        "coordinates",
    )
    coordinates[14] = ["0", "0"]
    source_missing_pair24 = copy.deepcopy(source)
    middle_stratum = require_dict(
        require_list(source_missing_pair24["strata"], "strata")[1], "middle stratum"
    )
    first_branch = require_dict(
        require_list(middle_stratum["branches"], "branches")[0], "first branch"
    )
    rows = require_list(first_branch["inequalities"], "inequalities")
    first_branch["inequalities"] = [
        row for row in rows if require_dict(row, "row").get("label") != "contact:2-4:owner4:a+"
    ]

    def source_mutation_rejected(candidate: dict[str, object]) -> bool:
        try:
            validate_exp035_source(candidate)
        except (TypeError, ValueError):
            return True
        return False

    selftests = {
        "source_digest_tamper_is_rejected": mutation_rejected(result, tamper_source),
        "wrong_common_angle_direction_is_rejected": source_mutation_rejected(
            source_wrong_direction
        ),
        "missing_pair_2_4_row_is_rejected": source_mutation_rejected(source_missing_pair24),
        "missing_owner_branch_is_rejected": source_mutation_rejected(source_missing_branch),
        "nonpositive_owner4_coefficient_is_rejected": mutation_rejected(result, tamper_owner4),
        "nonpositive_relative_margin_is_rejected": mutation_rejected(result, tamper_margin),
        "component_isolation_overclaim_is_rejected": mutation_rejected(result, overclaim),
    }
    if not all(selftests.values()):
        raise ValueError(f"n=5 second-order selftests failed: {selftests}")
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
            "strata": len(STRATA),
            "obstructed_owner_branches": len(OWNER_BRANCHES),
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
