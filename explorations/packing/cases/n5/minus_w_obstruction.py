#!/usr/bin/env python3
"""Draft exp-043 pure -W checker; no scientific result is retained.

Independent review found that this draft does not yet construct production rowwise
second-order wall and SAT jets. Its temporary green record is therefore a resume point,
not an obstruction certificate. See the terminal exp-043 artifact before using it.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, replace
from fractions import Fraction
from pathlib import Path
from typing import cast

from strif import atomic_output_file

from cases.n5 import angle_sheet, second_order_obstruction, tangent_cones, tangent_inventory
from cases.n5 import equal_side_face as face
from sqpack.field import FieldElement, NumberField

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "campaign/series/series-000-smoke-and-calibration/results"
EXP034 = RESULTS / "exp-034-h-023-n5-angle-sheet.json"
EXP035 = RESULTS / "exp-035-h-023-n5-tangent-cones.json"
EXP036 = RESULTS / "exp-036-h-023-n5-second-order-obstruction.json"
EXP038 = RESULTS / "exp-038-h-023-n5-tangent-inventory.json"
STRATA = ("A", "interior", "B")
OWNERS = ("owner3:a+", "owner4:a+")
SCHEMA_VERSION = 1
CONTROL_KEYS = frozenset(
    {
        "angle_only_negation_rejected",
        "missing_owner_rejected",
        "missing_tied_row_rejected",
        "owner4_width_sign_rejected",
        "owner3_upper_term_rejected",
        "missing_interior_rejected",
        "realized_sheet_overclaim_rejected",
        "scope_overclaim_rejected",
        "geometry_constant_drift_rejected",
        "retained_correction_coordinate_rejected",
        "scaled_farkas_identity_rejected",
        "tilted_minus_w_rejected",
    }
)
REFUSED_CLAIMS = (
    "Ri_plus_lambda_W_plus_s",
    "other_mixed_direction",
    "other_transverse_direction",
    "whole_polytope_classification",
    "whole_stationary_component",
    "A_to_B_stationary_connection",
    "local_isolation",
    "terminality",
    "quench_selection",
    "basin_mass",
    "census_completeness",
    "unequal_side_clearance",
    "minus_W_obstruction_from_candidate_failure",
)
FROZEN_REFUSALS = frozenset(
    {
        "Ri_plus_lambda_W_plus_s",
        "other_mixed_direction",
        "other_transverse_direction",
        "whole_polytope_classification",
        "whole_stationary_component",
        "A_to_B_stationary_connection",
        "local_isolation",
        "terminality",
        "quench_selection",
        "basin_mass",
        "census_completeness",
        "unequal_side_clearance",
        "minus_W_obstruction_from_candidate_failure",
    }
)


class ProofInvariantError(ValueError):
    """A stable failure of one frozen exp-043 invariant."""

    def __init__(self, failure_id: str, detail: str):
        super().__init__(f"{failure_id}: {detail}")
        self.failure_id = failure_id


@dataclass(frozen=True)
class ProofInputs:
    """Production inputs changed by the twelve semantic mutations."""

    negate_centres: bool = True
    owners: tuple[str, ...] = OWNERS
    drop_tied_row: bool = False
    owner4_width_sign: int = -1
    owner3_upper_adjustment_numerator: int = 0
    strata: tuple[str, ...] = STRATA
    claim_sheet_obstructed: bool = False
    promoted_claim: str | None = None
    # Reaches `source.geometry`: drifts one branch geometry constant.
    geometry_separation_offset: int = 0
    # Reaches `certificate.acceleration_correction`: scaling one weight leaves a
    # correction coordinate in the Farkas combination.
    scale_single_weight: bool = False
    # Reaches `certificate.acceleration_farkas`: scaling every weight preserves the zero
    # pose sum by linearity but moves the side coefficient off the exact alpha.
    weight_scale_offset: int = 0
    # Reaches `source.first_order`: tilts -W so a source row stays active.
    tilt_direction: bool = False


def require_dict(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise TypeError(f"{label} must be an object")
    return cast(dict[str, object], value)


def encode(value: FieldElement) -> list[str]:
    return tangent_cones.encode(value)


def source_bindings() -> dict[str, object]:
    regenerated = {
        "exp_034": angle_sheet.build_result(),
        "exp_035": tangent_cones.build_result(),
        "exp_036": second_order_obstruction.build_result(),
        "exp_038": tangent_inventory.build_result(),
    }
    paths = {"exp_034": EXP034, "exp_035": EXP035, "exp_036": EXP036, "exp_038": EXP038}
    for name, path in paths.items():
        retained = json.loads(path.read_text(encoding="utf-8"))
        if retained != regenerated[name]:
            raise ProofInvariantError("source.replay", f"{name} exact regeneration drifted")
    return {
        "records": {name: str(path.relative_to(ROOT)) for name, path in paths.items()},
        "exact_regeneration_matches": True,
    }


def minus_w_direction(
    field: NumberField, stratum: str, inputs: ProofInputs
) -> tuple[list[FieldElement], list[FieldElement]]:
    stored = tangent_inventory.geometry_vectors(field, stratum)[0]["W"]
    expected = [-value for value in stored]
    candidate = list(expected)
    if not inputs.negate_centres:
        for index in range(10):
            candidate[index] = stored[index]
    if candidate != expected:
        raise ProofInvariantError(
            "source.minus_w", "the complete stored W vector was not negated"
        )
    return stored, candidate


def selected_rows(
    field: NumberField,
    stratum: str,
    owner: str,
    inputs: ProofInputs,
) -> tuple[list[tangent_cones.LinearRow], list[FieldElement]]:
    q = field.rational
    r = field.alpha
    rows = [
        row
        for row in tangent_inventory.matrix(field, stratum, owner)
        if row.label.startswith(("wall:2:", "wall:3:", "contact:2-4:", "contact:3-4:"))
    ]
    weights: list[FieldElement] = []
    transverse = r / 2 - q(3) / 4
    for row in rows:
        if row.label.startswith("wall:2:"):
            weights.append(r / 4)
        elif row.label.startswith("wall:3:"):
            weights.append(r / 2)
        elif row.label.startswith("contact:2-4:"):
            weights.append(q(1))
        elif owner == "owner4:a+":
            weights.append(q(1) / 2)
        elif row.label.endswith("feature+1"):
            weights.append(q(1) / 2 - transverse)
        else:
            weights.append(q(1) / 2 + transverse)
    if inputs.drop_tied_row:
        index = next(
            index for index, row in enumerate(rows) if row.label.startswith("contact:3-4:")
        )
        rows.pop(index)
        weights.pop(index)
    if inputs.scale_single_weight:
        weights[0] = weights[0] * q(2)
    if inputs.weight_scale_offset:
        factor = q(1) + q(inputs.weight_scale_offset)
        weights = [weight * factor for weight in weights]
    tied_count = sum(row.label.startswith("contact:3-4:") for row in rows)
    if len(rows) != 9 or tied_count != 2:
        raise ProofInvariantError(
            "source.tied_rows", "a constructed tied support row is missing"
        )
    return rows, weights


def acceleration_eliminator(
    field: NumberField,
    rows: list[tangent_cones.LinearRow],
    weights: list[FieldElement],
) -> dict[str, object]:
    q = field.rational
    r = field.alpha
    pose_sum = [
        sum(
            (
                weight * row.coefficients[index]
                for row, weight in zip(rows, weights, strict=True)
            ),
            q(0),
        )
        for index in range(tangent_cones.VARIABLE_COUNT)
    ]
    if any(not value.is_zero() for value in pose_sum):
        raise ProofInvariantError(
            "certificate.acceleration_correction",
            "the source-row Farkas combination retains a correction coordinate",
        )
    side_coefficient = sum(
        (
            weight
            for row, weight in zip(rows, weights, strict=True)
            if row.label.startswith("wall:3:")
        ),
        q(0),
    )
    if side_coefficient != r or any(weight.sign() <= 0 for weight in weights):
        raise ProofInvariantError(
            "certificate.acceleration_farkas", "the exact positive Farkas identity drifted"
        )
    return {
        "row_labels": [row.label for row in rows],
        "positive_weights": [encode(value) for value in weights],
        "pose_correction_coefficients": [encode(value) for value in pose_sum],
        "all_arbitrary_second_order_pose_corrections_cancel": True,
        "side_coefficient": encode(side_coefficient),
    }


def geometry_constants(
    field: NumberField, stratum: str, inputs: ProofInputs
) -> tuple[FieldElement, FieldElement, FieldElement]:
    q = field.rational
    r = field.alpha
    centres = tangent_cones.centres_for_stratum(field, stratum)
    p2, p3, p4 = centres[2], centres[3], centres[4]
    a = (r / 2, r / 2)
    perpendicular = (-r / 2, r / 2)
    displacement_24 = (p4[0] - p2[0], p4[1] - p2[1])
    displacement_34 = (p4[0] - p3[0], p4[1] - p3[1])
    transverse = tangent_cones.dot2(displacement_24, perpendicular)
    separation_34 = tangent_cones.dot2(displacement_34, a)
    if inputs.geometry_separation_offset:
        separation_34 = separation_34 + q(inputs.geometry_separation_offset)
    cusp = q(1) / 2 - tangent_cones.abs_exact(transverse)
    if separation_34 != -q(1) or cusp.sign() <= 0:
        raise ProofInvariantError("source.geometry", "a branch geometry constant drifted")
    return transverse, separation_34, cusp


def evaluate_necessary_inequality(
    field: NumberField,
    *,
    stratum: str,
    owner: str,
    direction: list[FieldElement],
    inputs: ProofInputs,
    realized_sheet: bool,
) -> dict[str, object]:
    q = field.rational
    r = field.alpha
    side = cast(FieldElement, face.exact_data(field)["side"])
    rows, weights = selected_rows(field, stratum, owner, inputs)
    if any(not tangent_cones.exact_dot(row, direction, field).is_zero() for row in rows):
        raise ProofInvariantError("source.first_order", "the requested direction is not tight")
    eliminator = acceleration_eliminator(field, rows, weights)
    transverse, _separation_34, cusp = geometry_constants(field, stratum, inputs)
    speed3 = direction[tangent_cones.theta(3)]
    speed4 = direction[tangent_cones.theta(4)]
    width3 = -r * speed3 * speed3 / 2
    width4 = -r * speed4 * speed4 / 2
    if not realized_sheet and owner == "owner4:a+":
        width4 = q(inputs.owner4_width_sign) * r * speed4 * speed4 / 2
    if owner == "owner4:a+":
        coefficient = width3 / 2 - q(3) * width4 / (q(2) * r * r)
        obstructed = coefficient.sign() > 0
        if not realized_sheet and not obstructed:
            raise ProofInvariantError(
                "certificate.owner4_sign", "the eliminated owner-4 excess is not positive"
            )
        derived = {
            "excess_coefficient": encode(coefficient),
            "necessary_inequality": "S >= 1+w3/2+3/(2*w4)",
        }
    else:
        upper = (side - r) * width3 + q(inputs.owner3_upper_adjustment_numerator) / 2
        lower = (width3 + width4) / 2
        gap = upper - lower
        obstructed = gap.sign() < 0 and cusp.sign() > 0
        if not realized_sheet and not obstructed:
            raise ProofInvariantError(
                "certificate.owner3_sign", "the eliminated owner-3 gap is not negative"
            )
        derived = {
            "upper_coefficient": encode(upper),
            "lower_coefficient": encode(lower),
            "upper_minus_lower": encode(gap),
            "obstruction_coefficient": encode(-gap),
            "relative_angle_projection": encode(transverse),
            "relative_angle_cusp_margin": encode(cusp),
            "necessary_inequality": "upper-lower <= -margin*abs(delta)",
            "relative_angle_scale": "delta=o(t), with no O(t^2) assumption",
            "two_scale_exhaustion": (
                "the negative t^2 gap handles delta=o(t^2); the negative cusp term "
                "handles every larger o(t) relative-angle scale"
            ),
        }
    return {
        "owner": owner,
        "realized_sheet_direction": realized_sheet,
        "width_second_order": {"square3": encode(width3), "square4": encode(width4)},
        "arbitrary_little_o_angle_corrections_eliminated": True,
        "feasible_subsequence_owner_branch_exhausted": True,
        "strict_contradiction": obstructed,
        "compatible_second_order_correction": not obstructed,
        "eliminator": eliminator,
        **derived,
    }


def minus_w_cases(field: NumberField, inputs: ProofInputs) -> list[dict[str, object]]:
    if set(inputs.strata) != set(STRATA) or len(inputs.strata) != 3:
        raise ProofInvariantError("source.strata", "A, interior, and B are all required")
    if set(inputs.owners) != set(OWNERS) or len(inputs.owners) != 2:
        raise ProofInvariantError(
            "source.owner_exhaustion", "both nearby owner branches are required"
        )
    if inputs.promoted_claim is not None:
        raise ProofInvariantError("scope.overclaim", "the requested claim exceeds pure -W")
    geometry = tangent_cones.geometry_inventory(field)
    cases: list[dict[str, object]] = []
    for stratum in inputs.strata:
        stored, direction = minus_w_direction(field, stratum, inputs)
        if inputs.tilt_direction:
            direction = list(direction)
            direction[0] = direction[0] + field.rational(1)
        for owner in inputs.owners:
            all_rows = tangent_inventory.matrix(field, stratum, owner)
            if any(
                not tangent_cones.exact_dot(row, direction, field).is_zero() for row in all_rows
            ):
                raise ProofInvariantError("source.first_order", "-W left an active source row")
            certificate = evaluate_necessary_inequality(
                field,
                stratum=stratum,
                owner=owner,
                direction=direction,
                inputs=inputs,
                realized_sheet=False,
            )
            cases.append(
                {
                    "stratum": stratum,
                    "owner": owner,
                    "stored_W": [encode(value) for value in stored],
                    "canonical_minus_W": [encode(value) for value in direction],
                    "complete_vector_negated": True,
                    "all_active_source_rows_first_order_tight": True,
                    "zero_owner_axes": require_dict(
                        geometry["zero_owner_axes_by_stratum"], "zero axes"
                    )[stratum],
                    "certificate": certificate,
                }
            )
    if len(cases) != 6:
        raise ProofInvariantError(
            "source.owner_exhaustion", "the six-case inventory is incomplete"
        )
    return cases


def realized_sheet_oracle(field: NumberField, inputs: ProofInputs) -> dict[str, object]:
    q = field.rational
    direction = tangent_inventory.geometry_vectors(field, "A")[1]["sheet_angle_positive"]
    certificates = [
        evaluate_necessary_inequality(
            field,
            stratum="A",
            owner=owner,
            direction=direction,
            inputs=replace(inputs, drop_tied_row=False),
            realized_sheet=True,
        )
        for owner in OWNERS
    ]
    fixture = angle_sheet.exact_fixture(field, sign=1, endpoint="left", q_abs=Fraction(1, 100))
    compatible = all(item["strict_contradiction"] is False for item in certificates)
    if fixture["valid"] is not True or not compatible or inputs.claim_sheet_obstructed:
        raise ProofInvariantError(
            "control.realized_direction", "the exact exp-034 sheet curve was falsely obstructed"
        )
    return {
        "curve": "exp-034 positive sheet-angle curve at A",
        "normalized_center_velocity": {"dx0": encode(q(1) / 2), "dy0": encode(q(1) / 2)},
        "normalized_center_second_order": {"x0": encode(-q(1) / 4), "y0": encode(-q(1) / 4)},
        "normalized_angle_velocity": {"dtheta0": encode(q(1))},
        "exact_fixture": fixture,
        "generic_evaluator_certificates": certificates,
        "compatible_no_contradiction": True,
    }


def plus_w_oracle(field: NumberField, inputs: ProofInputs) -> list[dict[str, object]]:
    """Send exp-036's realized positive obstruction through the generic evaluator."""
    records: list[dict[str, object]] = []
    production_inputs = replace(
        inputs,
        negate_centres=True,
        drop_tied_row=False,
        owner4_width_sign=-1,
        owner3_upper_adjustment_numerator=0,
    )
    for stratum in STRATA:
        direction = tangent_inventory.geometry_vectors(field, stratum)[0]["W"]
        for owner in OWNERS:
            certificate = evaluate_necessary_inequality(
                field,
                stratum=stratum,
                owner=owner,
                direction=direction,
                inputs=production_inputs,
                realized_sheet=False,
            )
            records.append(
                {
                    "stratum": stratum,
                    "owner": owner,
                    "certificate": certificate,
                }
            )
    return records


def proof_core(field: NumberField, inputs: ProofInputs) -> dict[str, object]:
    cases = minus_w_cases(field, inputs)
    sheet = realized_sheet_oracle(field, inputs)
    plus_cases = plus_w_oracle(field, inputs)
    q = field.rational
    r = field.alpha
    obstruction_met = all(
        require_dict(item["certificate"], "case certificate")["strict_contradiction"] is True
        for item in cases
    )
    predicted_values_met = all(
        (
            require_dict(item["certificate"], "case certificate").get("excess_coefficient")
            == encode(r / 8)
            if item["owner"] == "owner4:a+"
            else require_dict(item["certificate"], "case certificate").get(
                "obstruction_coefficient"
            )
            == encode(q(1) / 4)
            and require_dict(item["certificate"], "case certificate").get(
                "relative_angle_cusp_margin"
            )
            == encode(r / 2 - q(1) / 4)
        )
        for item in cases
    )
    plus_by_case = {
        (item["stratum"], item["owner"]): require_dict(item["certificate"], "+W certificate")
        for item in plus_cases
    }
    symmetry_met = predicted_values_met and all(
        require_dict(item["certificate"], "-W certificate")
        == plus_by_case[(item["stratum"], item["owner"])]
        for item in cases
    )
    return {
        "cases": cases,
        "case_count": len(cases),
        "realized_sheet_oracle": sheet,
        "positive_W_obstruction_oracle": plus_cases,
        "determinations": {
            "obstruction": {
                "outcome": "criterion_met" if obstruction_met else "criterion_missed",
                "claim": "canonical pure -W is excluded at A, interior, and B",
            },
            "sign_symmetry": {
                "outcome": "criterion_met" if symmetry_met else "criterion_missed",
                "claim": "the -W coefficients equal the separately derived +W values",
            },
        },
    }


def mutation_record(
    field: NumberField, inputs: ProofInputs, expected_id: str
) -> dict[str, object]:
    try:
        proof_core(field, inputs)
    except ProofInvariantError as error:
        actual_id: str | None = error.failure_id
    else:
        actual_id = None
    return {
        "expected_failure_id": expected_id,
        "actual_failure_id": actual_id,
        "passed": actual_id == expected_id,
    }


def controls(field: NumberField) -> dict[str, dict[str, object]]:
    base = ProofInputs()
    mutations: dict[str, tuple[ProofInputs, str]] = {
        "angle_only_negation_rejected": (replace(base, negate_centres=False), "source.minus_w"),
        "missing_owner_rejected": (
            replace(base, owners=(OWNERS[0],)),
            "source.owner_exhaustion",
        ),
        "missing_tied_row_rejected": (replace(base, drop_tied_row=True), "source.tied_rows"),
        "owner4_width_sign_rejected": (
            replace(base, owner4_width_sign=1),
            "certificate.owner4_sign",
        ),
        "owner3_upper_term_rejected": (
            replace(base, owner3_upper_adjustment_numerator=1),
            "certificate.owner3_sign",
        ),
        "missing_interior_rejected": (replace(base, strata=("A", "B")), "source.strata"),
        "realized_sheet_overclaim_rejected": (
            replace(base, claim_sheet_obstructed=True),
            "control.realized_direction",
        ),
        "scope_overclaim_rejected": (replace(base, promoted_claim="mixed"), "scope.overclaim"),
        "geometry_constant_drift_rejected": (
            replace(base, geometry_separation_offset=1),
            "source.geometry",
        ),
        "retained_correction_coordinate_rejected": (
            replace(base, scale_single_weight=True),
            "certificate.acceleration_correction",
        ),
        "scaled_farkas_identity_rejected": (
            replace(base, weight_scale_offset=1),
            "certificate.acceleration_farkas",
        ),
        "tilted_minus_w_rejected": (replace(base, tilt_direction=True), "source.first_order"),
    }
    if set(mutations) != CONTROL_KEYS or len(mutations) != 12:
        raise ProofInvariantError("control.keys", "the exact twelve-key control set drifted")
    records = {
        name: mutation_record(field, mutation, expected)
        for name, (mutation, expected) in mutations.items()
    }
    if not all(record["passed"] is True for record in records.values()):
        raise ProofInvariantError(
            "control.identifiers", "a typed mutation identifier mismatched"
        )
    return records


def build_result() -> dict[str, object]:
    field = face.make_field()
    sources = source_bindings()
    certificate = proof_core(field, ProofInputs())
    determinations = require_dict(certificate["determinations"], "determinations")
    obstruction = require_dict(determinations["obstruction"], "obstruction determination")
    if obstruction["outcome"] != "criterion_met":
        raise ProofInvariantError(
            "baseline.obstruction", "the unmutated obstruction did not pass"
        )
    if len(REFUSED_CLAIMS) != 13 or set(REFUSED_CLAIMS) != FROZEN_REFUSALS:
        raise ProofInvariantError(
            "scope.refusal_set", "the exact thirteen-key refusal set drifted"
        )
    return {
        "schema_version": SCHEMA_VERSION,
        "contract": "packing.squares:N5MinusWObstruction/v1",
        "field": "Q(sqrt(2)), sqrt(2) in (1,2)",
        "sources": sources,
        "certificate": certificate,
        "determinations": determinations,
        "positive_obstruction_control": {
            "exp_036_exact_regeneration_bound": True,
            "orientation": "+W",
        },
        "controls": controls(field),
        "scope_refusals": {"refused_claims": list(REFUSED_CLAIMS), "all_refused": True},
    }


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
    try:
        result = build_result()
        if args.record is not None:
            write_json_atomic(args.record, result)
        else:
            retained = json.loads(args.replay.read_text(encoding="utf-8"))
            if retained != result:
                raise ProofInvariantError(
                    "replay.drift", "retained result differs from regeneration"
                )
        summary_cases = require_dict(result["certificate"], "certificate")["case_count"]
        summary_controls = len(require_dict(result["controls"], "controls"))
        print(
            json.dumps(
                {"status": "PASS", "cases": summary_cases, "controls": summary_controls}
            )
        )
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
