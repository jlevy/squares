"""Finite owned-core guard identities; conditional transport is an inherited hand proof."""

from __future__ import annotations

import argparse
import copy
import math
import sys
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, cast

from devtools import check_n17_two_child_collective_propagation as prior
from devtools.provenance import provenance
from sqpack import retained_json

finite, parent, guard = prior.finite, prior.parent, prior.guard
require, tick, checked = prior.require, prior.tick, prior.checked
IncompleteError = prior.IncompleteError
SCHEMA = "n17-owned-core-guarded-clause/v1"
DESCRIPTOR_SCHEMA = "n17-owned-core-guarded-clause-context/v1"
ROLES = ("cases_descriptor", "cases_certificate", "cases_replay")
RECEIPT_LIMIT = 64 << 20
OUTPUT_LIMIT = 1 << 20
RESERVE = Q(1, 2**21)
REACH = Q(1, 2) - RESERVE
MONOMIALS = (
    (0, 0, 0),
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (1, 0, 1),
    (0, 1, 1),
    (0, 0, 2),
    (1, 0, 2),
    (0, 1, 2),
)
payload = prior.payload


def scope() -> dict[str, bool]:
    return dict.fromkeys(
        (
            "capture_proved",
            "global_bound_proved",
            "global_optimality_proved",
            "ordinary_assignment_exclusion_proved",
            "census_admission_proved",
            "complement_exclusion_proved",
            "physical_packing_exists_proved",
            "additional_parameter_loss_proved",
            "owner0_target_rows_transported",
            "old_propagation_replayed",
            "root_proof_replayed",
        ),
        False,
    )


def polynomial(point: tuple[Q, Q], axis: str, sign: int) -> list[Q]:
    """Coefficients of the frozen nine monomials in centre x, centre y, and t."""
    require(axis in ("u", "v") and type(sign) is int and sign in (-1, 1), "axis/sign differs")
    x, y = map(checked, point)
    s = Q(sign)
    values = (
        (REACH - s * x, s, Q(0), -2 * s * y, Q(0), 2 * s, REACH + s * x, -s, Q(0))
        if axis == "u"
        else (REACH - s * y, Q(0), s, 2 * s * x, -2 * s, Q(0), REACH + s * y, Q(0), -s)
    )
    return list(map(checked, values))


def at_centre(coefficients: list[Q], centre: tuple[Q, Q]) -> tuple[Q, Q, Q]:
    x, y = map(checked, centre)
    require(len(coefficients) == len(MONOMIALS), "polynomial coefficient roster")
    result = [Q(0)] * 3
    for coefficient, (i, j, k) in zip(coefficients, MONOMIALS, strict=True):
        result[k] = checked(result[k] + coefficient * x**i * y**j)
    return cast(tuple[Q, Q, Q], tuple(result))


def finite_packet(
    points: list[tuple[Q, Q]], old_guard: dict[str, Any], *, deadline: float
) -> dict[str, Any]:
    tick(deadline)
    require(3 <= len(points) <= guard.OWNER0_LIMIT, "nonempty bounded Q0 required")
    points = [(checked(x), checked(y)) for x, y in points]
    require(
        prior.cases.bounded_hull(points, guard.OWNER0_LIMIT, deadline) == points,
        "canonical Q0 hull differs",
    )
    require(
        checked(guard.standing.area2(points)) > 0,
        "positive-area Q0 required",
    )
    lo, hi = map(finite.rational, old_guard["angle_interval"])
    require(
        [lo, hi] == [Q(211, 512), Q(213, 512)] and old_guard["half_width"] == "1/512",
        "old closed angle box differs",
    )
    boxes = [list(map(finite.rational, b)) for b in old_guard["centre_box"]]
    require(
        len(boxes) == 2 and all(len(b) == 2 and b[1] - b[0] == Q(1, 256) for b in boxes),
        "old centre box differs",
    )
    records, minima = [], []
    for index, point in enumerate(points):
        for axis in ("u", "v"):
            for sign in (-1, 1):
                coefficients = polynomial(point, axis, sign)
                records.append(
                    {
                        "q_index": index,
                        "axis": axis,
                        "sign": sign,
                        "coefficients": list(map(str, coefficients)),
                    }
                )
                for corner in ((x, y) for x in boxes[0] for y in boxes[1]):
                    tick(deadline)
                    value, t = guard.sat.minimum(at_centre(coefficients, corner), lo, hi)
                    value, t = checked(value), checked(t)
                    require(value >= 0, "old box inclusion calibration fails")
                    minima.append(
                        {
                            "q_index": index,
                            "axis": axis,
                            "sign": sign,
                            "corner": list(map(str, corner)),
                            "minimum": str(value),
                            "argmin": str(t),
                        }
                    )
    spans = [checked(max(p[i] for p in points) - min(p[i] for p in points)) for i in (0, 1)]
    return {
        "Q0": finite.serial(points),
        "reserve": str(RESERVE),
        "projection_reach": str(REACH),
        "centre_variables": ["cx", "cy"],
        "centre_domain_premise": "original-parent owner0 physical pose domain",
        "same_container_hypothesis_required": True,
        "angle_variable": "t",
        "closed_angle_domain": ["0", "1"],
        "inequality_relation": ">=0",
        "monomial_exponents_cx_cy_t": [list(m) for m in MONOMIALS],
        "maximum_total_degree": 3,
        "polynomials": records,
        "old_box": copy.deepcopy(old_guard),
        "old_box_corner_minima": minima,
        "old_box_inclusion_verified": True,
        "positive_ambient_width_inherited": True,
        "axis_spans": list(map(str, spans)),
        "endpoint_axis_aligned_family_disjoint": max(spans) > 1,
        "quadratic_checks": len(minima),
    }


def intake(document: Any, deadline: float) -> tuple[Any, ...]:
    require(
        type(document) is dict
        and document.get("schema") == DESCRIPTOR_SCHEMA
        and set(document) == {"schema", *(k for r in ROLES for k in (r, r + "_sha256"))},
        "guarded-clause descriptor differs",
    )
    held: dict[Path, tuple[str, int]] = {}
    values = {
        r: prior.previous.read_bound(
            r,
            document,
            held,
            deadline,
            parent.JSON_LIMIT if r.endswith("descriptor") else RECEIPT_LIMIT,
        )
        for r in ROLES
    }
    accepted, replay = values["cases_certificate"], values["cases_replay"]
    require(
        accepted["schema"] == prior.SCHEMA
        and accepted["accepted_inputs"] == values["cases_descriptor"]
        and accepted["status"] == "additional_angle_union_restricted"
        and accepted["criterion_met"] is True
        and replay.get("verification_passed") is True
        and payload(accepted) == payload(replay)
        and accepted["closed_case_count"] == 0
        and accepted["both_children_closed"] is False
        and accepted["base_foreign_rows_accounted"] == 992
        and accepted["original_rows_inherited"] == 1056
        and accepted["survivors_unioned_across_cases"] is True
        and accepted["no_sequential_feedback"] is True
        and accepted["regional_necessary_domain_restriction_proved"] is True
        and all(
            accepted.get(k) is False
            for k in prior.scope()
            if k != "regional_necessary_domain_restriction_proved"
        ),
        "accepted302 complete positive premise differs",
    )
    rows, groups, original, transitive = prior.intake(values["cases_descriptor"], deadline)
    for path, (sha, source_limit) in transitive.items():
        limit = source_limit
        if path in held:
            require(held[path][0] == sha, "conflicting custody alias")
            limit = min(limit, held[path][1])
        held[path] = sha, limit
    require(
        all(
            accepted[k] == original[k]
            for k in ("guard", "container", "parent_custody", "original_endpoint_control")
        ),
        "accepted core/context ancestry differs",
    )
    children = accepted["children"]
    require(
        accepted["fixed_selection"] == {"owner": 18, "axis": 0, "midpoint": str(prior.MIDPOINT)}
        and all(
            c["halfplane"]
            == {
                "axis": 0,
                "relation": "<=" if c["side"] == -1 else ">=",
                "midpoint": str(prior.MIDPOINT),
            }
            for c in children
        ),
        "frozen accepted closed case cover differs",
    )
    require(
        [c["side"] for c in children] == [-1, 1]
        and all(
            c["closed"] is False
            and c["closure"] is None
            and c["collective_rows_accounted"] == 992
            and c["collective"]["all_foreign_rows_accounted"] == 992
            and c["other_owned_groups_unchanged"] is True
            for c in children
        ),
        "both full open case premises required",
    )
    combined = prior.combine(rows, children, deadline)
    require(combined == accepted["combined_restrictions"], "accepted combined clauses differ")
    by_owner = {entry["owner"]: entry for entry in combined}
    require(
        by_owner[6]["combined_surviving_closed_interval_union"] == [["1/16", "19/32"]]
        and by_owner[6]["additional_lost_length"] == "15/32"
        and by_owner[18]["combined_surviving_closed_interval_union"]
        == [["0", "19/64"], ["3/8", "35/64"], ["13/16", "1"]],
        "frozen302 owner6/18 clauses differ",
    )
    endpoint = accepted["original_endpoint_control"]
    require(
        endpoint["all17_retained"] is True
        and [w["label"] for w in endpoint["witnesses"]] == list(range(1, 18))
        and endpoint["witnesses"][0]["owner"] == 0,
        "inherited original17 endpoint premise differs",
    )
    path = finite.retained_path(accepted["parent_custody"]["h290_receipt"])
    require(
        path in held and held[path][0] == accepted["parent_custody"]["h290_receipt_sha256"],
        "accepted endpoint receipt custody missing",
    )
    _, h290 = finite.read_json(path, held[path][1])
    roster = h290["custody"]["input_control"]["endpoint_roster"]
    require(
        [p["label"] for p in roster] == list(range(1, 18))
        and roster[0]["owner"] == 0
        and roster[0]["charts"] == [["0", "0"], ["1", "1"]],
        "endpoint exact axis-aligned alternatives differ",
    )
    return groups[0], accepted, held, combined


def generate(document: dict[str, Any], *, deadline: float) -> dict[str, Any]:
    frozen = finite.canonical(document)
    points, accepted, held, combined = intake(document, deadline)
    packet = finite_packet(points, accepted["guard"], deadline=deadline)
    met = packet["endpoint_axis_aligned_family_disjoint"]
    for path, (sha, limit) in held.items():
        require(finite.digest(path, limit, deadline) == sha, "guarded-clause premise changed")
    require(finite.canonical(document) == frozen, "guarded-clause descriptor changed")
    tick(deadline)
    return {
        "schema": SCHEMA,
        "status": "guarded_clause_verified" if met else "criterion_missed",
        "criterion_met": met,
        "verification_passed": False,
        **scope(),
        "accepted_inputs": copy.deepcopy(document),
        "container": copy.deepcopy(accepted["container"]),
        "parent_custody": copy.deepcopy(accepted["parent_custody"]),
        "guard_packet": packet,
        "conditional_clauses": [
            {
                "owner": o,
                "closed_interval_union": copy.deepcopy(
                    next(e for e in combined if e["owner"] == o)[
                        "combined_surviving_closed_interval_union"
                    ]
                ),
            }
            for o in (6, 18)
        ],
        "transport_scope": "physical original-parent packings satisfying the SAME Q0 guard",
        "hand_transport_independently_verified": False,
        "hand_dependency": (
            "same-Q0 strict ownership transports accepted302 foreign domains and case cover"
        ),
        "endpoint_original17_retention_inherited": True,
        "endpoint_axis_alignment": {
            "label": 1,
            "owner": 0,
            "charts": [["0", "0"], ["1", "1"]],
            "source_path": accepted["parent_custody"]["h290_receipt"],
            "source_json_path": "custody.input_control.endpoint_roster[0].charts",
        },
        "oldbox_inclusion_is_not_physical_packing_existence": True,
        "parent_geometry_replayed": False,
        "limits": {
            "Q0_vertices": guard.OWNER0_LIMIT,
            "geometry_bits": finite.BIT_LIMIT,
            "maximum_quadratic_checks": 512,
            "output_bytes": OUTPUT_LIMIT,
            "accepted_receipt_bytes": RECEIPT_LIMIT,
            "descriptor_bytes": parent.JSON_LIMIT,
            "cooperative_phase_seconds": 60,
            "outer_supervisor_required": True,
        },
    }


def check(
    document: dict[str, Any], certificate: dict[str, Any], *, deadline: float
) -> dict[str, Any]:
    result = generate(document, deadline=deadline)
    require(
        payload(certificate) == payload(result), "fresh guarded-clause reconstruction differs"
    )
    return result | {"verification_passed": True}


def failure(exc: Exception) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "status": "incomplete" if isinstance(exc, IncompleteError) else "refused",
        "criterion_met": False,
        "verification_passed": False,
        **scope(),
        "error": str(exc),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--descriptor", type=Path, required=True)
    parser.add_argument("--certificate", type=Path)
    parser.add_argument("--max-seconds", type=float, default=60)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    if not math.isfinite(args.max_seconds) or args.max_seconds <= 0:
        parser.error("max-seconds must be finite and positive")
    deadline = time.monotonic() + args.max_seconds
    try:
        require(
            not any(
                n == p or n.startswith(p + ".") for n in sys.modules for p in finite.FORBIDDEN
            ),
            "producer/kernel/root import in guarded-clause checker",
        )
        raw, document = finite.read_json(args.descriptor, parent.JSON_LIMIT)
        if args.certificate:
            saved, certificate = finite.read_json(args.certificate, OUTPUT_LIMIT)
            result = check(document, certificate, deadline=deadline)
            require(
                saved == finite.read_json(args.certificate, OUTPUT_LIMIT)[0],
                "certificate changed",
            )
        else:
            result = generate(document, deadline=deadline)
        require(
            raw == finite.read_json(args.descriptor, parent.JSON_LIMIT)[0], "descriptor changed"
        )
    except (
        IncompleteError,
        ValueError,
        KeyError,
        TypeError,
        OSError,
        EOFError,
        guard.standing.VerificationError,
    ) as exc:
        result = failure(exc)
    result.update(
        provenance=provenance(Path(__file__), Path(prior.__file__)),
        invocation={
            "argv": argv if argv is not None else sys.argv[1:],
            "executable": sys.executable,
        },
    )
    text = retained_json.dumps(result, sort_keys=True)
    if len(text.encode()) > OUTPUT_LIMIT or time.monotonic() >= deadline:
        result = failure(IncompleteError("guarded-clause output byte or wall ceiling"))
        text = retained_json.dumps(result, sort_keys=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as stream:
        stream.write(text)
    return 1 if result["status"] in ("refused", "incomplete") else 0


if __name__ == "__main__":
    raise SystemExit(main())
