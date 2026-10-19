"""Recover owned sets once, then make one simultaneous closed-row coverage pass."""

from __future__ import annotations

import argparse
import copy
import math
import sys
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, cast

from devtools import check_n17_regional_row_coverage as regional
from devtools import check_n17_strict_core_regional_transfer as transfer
from devtools.provenance import provenance
from sqpack import retained_json

collective = transfer.collective
parent, finite, cases, guard = (
    collective.parent,
    collective.finite,
    collective.cases,
    collective.guard,
)
type Point = tuple[Q, Q]
require, tick, checked = collective.require, collective.tick, collective.checked
IncompleteError = collective.IncompleteError
OWNERS = collective.OWNERS
SCHEMA = "n17-one-round-owned-domain-propagation/v1"
DESCRIPTOR_SCHEMA = "n17-one-round-owned-domain-propagation-context/v1"
POINT_ROLES = transfer.ROLES
REGIONAL_ROLES = (
    *POINT_ROLES,
    "transfer_descriptor",
    "transfer_certificate",
    "transfer_replay",
)
DIRECT_ROLES = ("regional_descriptor", "regional_certificate", "regional_replay")
DIRECT_TARGET_INDICES = (*range(19, 24), *range(35, 52))
OUTPUT_LIMIT = 64 << 20
INTERSECTION_PRODUCTS = 2000000
payload = collective.payload


def validate_direct_collective(prior: dict[str, Any]) -> None:
    """Bind the complete 22-row component without promoting the SAME25 hypothesis."""
    require(
        prior["all_foreign_rows_accounted"] == 992
        and [entry["owner"] for entry in prior["owners"]] == list(OWNERS[1:])
        and prior["changed_owners"] == [18]
        and prior["complete_empty_owners"] == []
        and prior["original_owned_sets_unchanged"] is True
        and prior["simultaneous_original_groups_only"] is True,
        "direct regional complete component differs",
    )
    for entry in prior["owners"]:
        removed = [
            row["row_index"]
            for row in entry["rows"]
            if row["covered"] and row["inherited_domain_nonempty"]
        ]
        require(
            removed == (list(DIRECT_TARGET_INDICES) if entry["owner"] == 18 else []),
            "direct regional 22-row exclusion roster differs",
        )
        if entry["owner"] == 18:
            require(
                entry["old_closed_interval_union"] == [["0", "1"]]
                and entry["lost_length"] == "11/32"
                and entry["new_closed_interval_union"]
                == [["0", "19/64"], ["3/8", "35/64"], ["13/16", "1"]],
                "direct regional baseline union differs",
            )


def prune_prior(
    rows: dict[int, list[dict[str, Any]]],
    prior: dict[str, Any],
    deadline: float,
    *,
    direct_regional: bool = False,
) -> tuple[dict[int, list[dict[str, Any]]], list[dict[str, Any]]]:
    """Join every old decision before applying its complete whole-row exclusion."""
    if direct_regional:
        validate_direct_collective(prior)
    else:
        transfer.requested_rows(prior)
    effective = copy.deepcopy(rows)
    roster = []
    require(set(rows) == set(OWNERS[1:]), "original propagation owner roster differs")
    for owner, entry in zip(OWNERS[1:], prior["owners"], strict=True):
        tick(deadline)
        original = rows[owner]
        count = 32 if owner == 12 else 64
        require(
            entry["owner"] == owner and len(original) == len(entry["rows"]) == count,
            "complete prior row roster differs",
        )
        flags = []
        for index, (row, decision) in enumerate(zip(original, entry["rows"], strict=True)):
            tick(deadline)
            require(
                decision["row_index"] == index
                and decision["reference"] == row["reference"]
                and decision["interval"] == row["interval"]
                and type(decision["covered"]) is bool
                and decision["inherited_domain_nonempty"] is bool(row["domain"])
                and decision["domain_retained_unchanged"]
                is (bool(row["domain"]) and not decision["covered"]),
                "prior row identity/nonempty decision differs",
            )
            if decision["covered"]:
                effective[owner][index]["domain"] = []
            flags.append(
                {
                    "row_index": index,
                    "reference": copy.deepcopy(row["reference"]),
                    "interval": list(row["interval"]),
                    "prior_covered": decision["covered"],
                    "original_domain_nonempty": bool(row["domain"]),
                    "effective_domain_nonempty": bool(effective[owner][index]["domain"]),
                }
            )
        intervals = collective.union_intervals(
            [
                tuple(map(finite.rational, r["interval"]))
                for r in effective[owner]
                if r["domain"]
            ]
        )
        baseline = [list(map(str, interval)) for interval in intervals]
        require(bool(intervals), "already-empty input owner is a prior contradiction")
        require(baseline == entry["new_closed_interval_union"], "prior surviving union differs")
        roster.append(
            {"owner": owner, "rows": flags, "baseline_closed_interval_union": baseline}
        )
    require(sum(len(r) for r in effective.values()) == 992, "full992 prior roster required")
    return effective, roster


def shared_intersection(
    groups: dict[int, list[Point]], work: dict[str, int], deadline: float
) -> dict[str, Any] | None:
    """Enforce the cumulative input-product limit before each exact pair test."""
    require(set(groups) == set(OWNERS), "complete recovered owner roster differs")
    for index, owner in enumerate(OWNERS):
        for other in OWNERS[index + 1 :]:
            tick(deadline)
            if max(len(groups[owner]), len(groups[other])) > guard.OWNED_LIMIT:
                raise IncompleteError("propagation intersection input vertex ceiling")
            work["intersection_vertex_pairs"] += len(groups[owner]) * len(groups[other])
            if work["intersection_vertex_pairs"] > INTERSECTION_PRODUCTS:
                raise IncompleteError("propagation cumulative intersection product ceiling")
            overlap = cases.conditional.intersection(groups[owner], groups[other])
            tick(deadline)
            if len(overlap) > guard.INTERSECTION_LIMIT:
                raise IncompleteError("propagation intersection output vertex ceiling")
            overlap = [(checked(x), checked(y)) for x, y in overlap]
            if overlap:
                return {
                    "kind": "shared_strictly_owned_point",
                    "owners": [owner, other],
                    "intersection": finite.serial(overlap),
                }
    return None


def scope(mode: str, *, progress: bool = False, contradiction: bool = False) -> dict[str, bool]:
    regional = mode != "point"
    return {
        **guard.scope(),
        "point_guard_necessary_domain_restriction_proved": progress and not regional,
        "regional_necessary_domain_restriction_proved": progress and regional,
        "point_guard_exclusion_proved": contradiction and not regional,
        "point_contradiction_proved": contradiction and not regional,
        "declared_guard_exclusion_proved": contradiction and regional,
        "regional_guard_exclusion_proved": contradiction and regional,
    }


def construct(
    rows: dict[int, list[dict[str, Any]]],
    groups: dict[int, list[Point]],
    prior: dict[str, Any],
    *,
    mode: str,
    deadline: float,
) -> dict[str, Any]:
    require(
        mode in ("point", "fixed_core_regional", "direct_regional"), "propagation mode differs"
    )
    require(set(groups) == set(OWNERS), "complete inherited groups required")
    require(
        bool(groups[0])
        and len(groups[0]) <= guard.OWNER0_LIMIT
        and parent.area2(groups[0]) > 0,
        "positive bounded unchanged owner0 core required",
    )
    effective, roster = prune_prior(
        rows, prior, deadline, direct_regional=mode == "direct_regional"
    )
    frozen_rows = copy.deepcopy(effective)
    recovered = {0: list(groups[0])}
    work = guard.new_work()
    for owner in OWNERS[1:]:
        recovered[owner] = guard.common_owned(effective[owner], work, deadline)
        if len(recovered[owner]) > guard.OWNED_LIMIT:
            raise IncompleteError("propagation recovered vertex ceiling")
        for x, y in recovered[owner]:
            checked(x)
            checked(y)
    require(effective == frozen_rows, "recovery changed the effective row snapshot")
    closure = shared_intersection(recovered, work, deadline)
    new_collective = None
    additional = []
    changed = []
    if closure is None:
        frozen_groups = copy.deepcopy(recovered)
        new_collective = collective.construct(effective, recovered, deadline=deadline)
        require(
            new_collective["all_foreign_rows_accounted"] == 992
            and effective == frozen_rows
            and recovered == frozen_groups,
            "simultaneous collective snapshot changed",
        )
        for old, new in zip(roster, new_collective["owners"], strict=True):
            tick(deadline)
            require(
                new["owner"] == old["owner"]
                and new["old_closed_interval_union"] == old["baseline_closed_interval_union"],
                "new pass baseline union differs",
            )
            removed = [
                r["row_index"]
                for r in new["rows"]
                if r["inherited_domain_nonempty"] and r["covered"]
            ]
            baseline = [
                tuple(map(finite.rational, i)) for i in old["baseline_closed_interval_union"]
            ]
            surviving = [
                tuple(map(finite.rational, i)) for i in new["new_closed_interval_union"]
            ]
            require(
                all(any(a <= lo <= hi <= b for a, b in baseline) for lo, hi in surviving),
                "new interval union escaped baseline",
            )
            lost = checked(collective.length(baseline) - collective.length(surviving))
            require(
                lost >= 0 and str(lost) == new["lost_length"], "additional union length differs"
            )
            if lost > 0:
                changed.append(new["owner"])
            additional.append(
                {
                    "owner": new["owner"],
                    "newly_excluded_rows": removed,
                    "baseline_closed_interval_union": copy.deepcopy(
                        old["baseline_closed_interval_union"]
                    ),
                    "new_closed_interval_union": copy.deepcopy(
                        new["new_closed_interval_union"]
                    ),
                    "additional_lost_length": str(lost),
                }
            )
        if new_collective["complete_empty_owners"]:
            closure = {
                "kind": "collective_owner_cover_empty",
                "owners": list(new_collective["complete_empty_owners"]),
                "closed_cover_accounted": 992,
            }
        # Reused labels describe its local snapshot, after the complete recovery.
        for key in (
            "point_guard_necessary_domain_restriction_proved",
            "point_contradiction_proved",
            "original_owned_sets_unchanged",
            "simultaneous_original_groups_only",
        ):
            new_collective.pop(key)
        new_collective["recovered_groups_frozen_during_collective_pass"] = True
    tick(deadline)
    return {
        "status": "context_excluded"
        if closure
        else "additional_angle_union_restricted"
        if changed
        else "criterion_missed",
        "criterion_met": bool(closure or changed),
        **scope(mode, progress=bool(changed), contradiction=bool(closure)),
        "prior_row_restriction": roster,
        "prior_effective_rows_accounted": 992,
        "recovered_owned_groups": {str(o): finite.serial(recovered[o]) for o in OWNERS},
        "recovered_group_vertex_counts": {str(o): len(recovered[o]) for o in OWNERS},
        "owner0_core_unchanged": recovered[0] == groups[0],
        "all_foreign_recoveries_and_strict_checks_completed": True,
        "groups_recovered_from_prior_surviving_cover": True,
        "recovery_work": work,
        "closure": closure,
        "new_collective": new_collective,
        "new_collective_rows_accounted": 992 if new_collective is not None else 0,
        "additional_restrictions": additional,
        "changed_owners": changed,
        "new_live_row_deletions": sum(len(r["newly_excluded_rows"]) for r in additional),
        "no_sequential_feedback": True,
        "one_recovery_and_at_most_one_collective_pass": True,
    }


def hold_file(
    token: str, sha: str, ceiling: int, held: dict[Path, tuple[str, int]], deadline: float
) -> None:
    path = finite.retained_path(token)
    if path in held:
        require(held[path][0] == sha, "conflicting propagation input aliases")
        ceiling = min(ceiling, held[path][1])
    require(
        finite.digest(path, ceiling, deadline) == sha, "propagation dependency bytes differ"
    )
    held[path] = (sha, ceiling)


def read_bound(
    role: str,
    document: dict[str, Any],
    held: dict[Path, tuple[str, int]],
    deadline: float,
    ceiling: int,
) -> dict[str, Any]:
    path = finite.retained_path(document[role])
    if path in held:
        require(
            held[path][0] == document[role + "_sha256"], "conflicting propagation input aliases"
        )
        ceiling = min(ceiling, held[path][1])
    return transfer.read_bound(role, document, held, deadline, ceiling)


def direct_dependencies(
    document: dict[str, Any],
    accepted: dict[str, Any],
    held: dict[Path, tuple[str, int]],
    deadline: float,
) -> None:
    """Hold only the named accepted dependency chain; do not traverse arbitrary JSON."""
    values = {
        role: read_bound(
            role,
            document,
            held,
            deadline,
            OUTPUT_LIMIT if role.startswith("collective_") else parent.JSON_LIMIT,
        )
        for role in regional.ROLES
    }
    gate = values["parent_descriptor"]
    custody = accepted["parent_custody"]
    require(
        all(
            gate[k] == custody[k]
            for k in (
                "seed_sha256",
                "node_sha256",
                "compressed_sha256",
                "h290_receipt",
                "h290_receipt_sha256",
            )
        )
        and custody["steps"] == 16
        and len(custody["typed_reference_context"]["step_owners"]) == 16
        and set(custody["typed_reference_context"]["step_owners"]) == set(OWNERS) - {12},
        "direct accepted parent identities differ",
    )
    for token, sha in custody["compressed_sha256"].items():
        ceiling = (
            finite.SEED_LIMIT if Path(token).name.startswith("seed-") else finite.NODE_LIMIT
        )
        hold_file(token, sha, ceiling, held, deadline)
    hold_file(
        custody["h290_receipt"],
        custody["h290_receipt_sha256"],
        parent.JSON_LIMIT,
        held,
        deadline,
    )
    descriptor = values["feasible_descriptor"]
    for role in parent.feasible.INPUTS:
        hold_file(
            descriptor[role], descriptor[role + "_sha256"], parent.JSON_LIMIT, held, deadline
        )
    prior_inputs = values["collective_certificate"]["accepted_inputs"]
    historical = {
        role: read_bound(
            role,
            prior_inputs,
            held,
            deadline,
            parent.JSON_LIMIT if role == collective.ROLES[0] else OUTPUT_LIMIT,
        )
        for role in collective.ROLES
    }
    require(
        historical["guard_descriptor"]
        == {
            "schema": guard.DESCRIPTOR_SCHEMA,
            **{k: document[k] for r in parent.INPUTS for k in (r, r + "_sha256")},
        },
        "direct original five-role ancestry differs",
    )


def generate_direct(document: dict[str, Any], *, deadline: float) -> dict[str, Any]:
    require(
        set(document)
        == {"schema", "mode", *(k for r in DIRECT_ROLES for k in (r, r + "_sha256"))},
        "direct regional propagation roles differ",
    )
    frozen = finite.canonical(document)
    held: dict[Path, tuple[str, int]] = {}
    inputs = {
        role: read_bound(
            role,
            document,
            held,
            deadline,
            parent.JSON_LIMIT if role.endswith("descriptor") else OUTPUT_LIMIT,
        )
        for role in DIRECT_ROLES
    }
    descriptor = inputs["regional_descriptor"]
    accepted, replay = inputs["regional_certificate"], inputs["regional_replay"]
    require(
        accepted["schema"] == regional.SCHEMA
        and accepted["accepted_inputs"] == descriptor
        and descriptor["schema"] == regional.DESCRIPTOR_SCHEMA
        and set(descriptor)
        == {"schema", *(k for r in regional.ROLES for k in (r, r + "_sha256"))}
        and replay.get("verification_passed") is True
        and payload(accepted) == payload(replay)
        and accepted["status"] == "criterion_missed"
        and accepted["criterion_met"] is False
        and accepted["same25_rows_excluded"] is False
        and accepted["declared_guard_exclusion_proved"] is False
        and accepted["regional_necessary_domain_restriction_proved"] is False
        and accepted["point_guard_exclusion_proved"] is False
        and accepted["point_guard_necessary_domain_restriction_proved"] is False
        and accepted["regional_closure"] is None
        and accepted["point_context_constructed"] is False
        and accepted["accepted_point_domains_used_as_regional_domains"] is False
        and accepted["original_rows_reconstructed"] == 1056
        and accepted["regional_foreign_rows_conditioned"] == 992
        and accepted["regional_contexts_constructed"] == 1
        and all(accepted.get(k) is False for k in guard.scope()),
        "accepted direct regional completed-miss premise differs",
    )
    context = accepted["regional_context"]
    witness = accepted["matched_owned_point_witness"]
    require(
        witness["tau"] == str(guard.TAU) and len(witness["centre"]) == 2,
        "direct matched witness differs",
    )
    centre = list(map(finite.rational, witness["centre"]))
    expected_guard = {
        "half_width": str(regional.HALF_WIDTH),
        "angle_interval": [
            str(guard.TAU - regional.HALF_WIDTH),
            str(guard.TAU + regional.HALF_WIDTH),
        ],
        "centre_box": [
            [str(checked(x - regional.HALF_WIDTH)), str(checked(x + regional.HALF_WIDTH))]
            for x in centre
        ],
    }
    endpoint = accepted["original_endpoint_control"]
    require(
        context["guard"] == expected_guard
        and context["context_nonzero"] is True
        and context["closure"] is None
        and context["owner0_owned"] == context["owned_groups"]["0"]
        and accepted["container"] == guard.standing.CenteredContainer(cases.U, cases.V).record()
        and endpoint["all17_retained"] is True
        and endpoint["family_disjoint"] is True
        and [w["label"] for w in endpoint["witnesses"]] == list(range(1, 18))
        and {w["owner"] for w in endpoint["witnesses"]} == set(OWNERS)
        and endpoint["witnesses"][0]["owner"] == 0
        and endpoint["witnesses"][5]["owner"] == 12
        and endpoint["witnesses"][10]["owner"] == 18,
        "direct guard/core/container/endpoint premise differs",
    )
    direct_dependencies(descriptor, accepted, held, deadline)
    selected = [
        {k: copy.deepcopy(row[k]) for k in ("row_index", "reference", "interval")}
        for row in accepted["requested_rows"]
    ]
    require(
        accepted["same25_coverage_checks_performed"] == 25
        and [row["row_index"] for row in selected] == list(regional.TARGET_INDICES)
        and all(type(row["row_index"]) is int for row in selected),
        "direct original requested25 roster differs",
    )
    reference = accepted["parent_custody"]["typed_reference_context"]
    # Reconstruct only the finite collective implication. Conditioning remains inherited.
    prior_decision = regional.regional_decision(
        context, selected, deadline=deadline, reference_context=reference
    )
    require(
        all(accepted[k] == value for k, value in prior_decision.items()),
        "direct prior complete finite reconstruction differs",
    )
    prior = prior_decision["collective"]
    require(type(prior) is dict, "direct nonclosed collective component required")
    validate_direct_collective(prior)
    rows, groups = collective.context_geometry(context, reference, deadline)
    result = construct(rows, groups, prior, mode="direct_regional", deadline=deadline)
    for path, (sha, ceiling) in held.items():
        require(finite.digest(path, ceiling, deadline) == sha, "propagation premise changed")
    require(finite.canonical(document) == frozen, "propagation descriptor changed")
    tick(deadline)
    return {
        "schema": SCHEMA,
        "mode": "direct_regional",
        **result,
        "accepted_inputs": copy.deepcopy(document),
        "guard": copy.deepcopy(expected_guard),
        "parent_custody": copy.deepcopy(accepted["parent_custody"]),
        "container": copy.deepcopy(accepted["container"]),
        "original_endpoint_control": copy.deepcopy(endpoint),
        "original_rows_inherited": 1056,
        "original_parent_proof_replayed": False,
        "root_proof_replayed": False,
        "point_conditioning_reconstructed": False,
        "regional_conditioning_reconstructed": False,
        "accepted_regional_conditioning_inherited": True,
        "original17_endpoint_retention_inherited": True,
        "old_owner0_target_rows_transferred": False,
        "prior_regional_collective_finite_reconstructions": 1,
        "prior_collective_work": copy.deepcopy(prior["work"]),
        "prior_primary_same25_criterion_met": False,
        "prior_component_excluded_row_indices": list(DIRECT_TARGET_INDICES),
        "prior_component_parameter_loss": "11/32",
        "regional_conditioning_source": {
            "path": document["regional_certificate"],
            "sha256": document["regional_certificate_sha256"],
            "json_path": "$.regional_context",
        },
        "mathematical_assurance": (
            "sole-Astra one-round hand composition plus fresh finite reconstruction"
        ),
        "limits": {
            "output_bytes": OUTPUT_LIMIT,
            "geometry_bits": finite.BIT_LIMIT,
            "recovered_vertices": guard.OWNED_LIMIT,
            "owner0_vertices": guard.OWNER0_LIMIT,
            "recovery_support_products": guard.RECOVERY_SUPPORT_LIMIT,
            "strict_vertex_pairs": guard.STRICT_PAIR_LIMIT,
            "strict_quadratic_checks": guard.STRICT_CHECK_LIMIT,
            "intersection_input_products": INTERSECTION_PRODUCTS,
            "intersection_output_vertices": guard.INTERSECTION_LIMIT,
            "prior_and_new_collective_caps_unchanged_and_separate": True,
        },
        "resource_assurance": {
            "intersection_products_precharged": True,
            "trusted_unreduced_integer_products_individually_bounded": False,
            "sweep_internal_event_caps_enforced": False,
            "outer_supervision_required": True,
        },
    }


def generate(document: dict[str, Any], *, deadline: float) -> dict[str, Any]:
    require(
        type(document) is dict and document.get("schema") == DESCRIPTOR_SCHEMA,
        "propagation descriptor differs",
    )
    if document.get("mode") == "direct_regional":
        return generate_direct(document, deadline=deadline)
    require(
        document.get("mode") in ("point", "fixed_core_regional"), "propagation mode differs"
    )
    mode = cast(str, document["mode"])
    roles = POINT_ROLES if mode == "point" else REGIONAL_ROLES
    require(
        set(document) == {"schema", "mode", *(k for r in roles for k in (r, r + "_sha256"))},
        "propagation input roles differ",
    )
    frozen = finite.canonical(document)
    held: dict[Path, tuple[str, int]] = {}
    inputs = {
        role: read_bound(
            role,
            document,
            held,
            deadline,
            parent.JSON_LIMIT if role.endswith("descriptor") else OUTPUT_LIMIT,
        )
        for role in roles
    }
    old_doc = inputs["collective_descriptor"]
    accepted, replay = inputs["collective_certificate"], inputs["collective_replay"]
    require(
        replay.get("verification_passed") is True and payload(accepted) == payload(replay),
        "accepted prior collective payload differs",
    )
    uniform = None
    if mode == "point":
        fresh = collective.check(old_doc, accepted, deadline=deadline)
    else:
        transfer_doc = inputs["transfer_descriptor"]
        require(
            transfer_doc
            == {
                "schema": transfer.DESCRIPTOR_SCHEMA,
                **{k: document[k] for r in POINT_ROLES for k in (r, r + "_sha256")},
            },
            "transfer refers to a different collective premise",
        )
        require(
            inputs["transfer_replay"].get("verification_passed") is True
            and payload(inputs["transfer_certificate"]) == payload(inputs["transfer_replay"]),
            "accepted transfer fresh payload differs",
        )
        uniform = transfer.check(
            transfer_doc, inputs["transfer_certificate"], deadline=deadline
        )
        require(
            uniform["criterion_met"] is True and uniform["same25_rows_excluded"] is True,
            "uniform transfer incomplete",
        )
        fresh = copy.deepcopy(accepted) | {"verification_passed": True}
    transfer.requested_rows(fresh)
    rows, groups, point, inherited_held, _ = collective.intake(old_doc, deadline=deadline)
    held.update(inherited_held)
    context = point["contexts"][0]
    require(
        context["owner0_owned"] == context["owned_groups"]["0"], "unchanged owner0 core differs"
    )
    if uniform is not None:
        require(
            uniform["parent_custody"] == point["parent_custody"]
            and uniform["container"] == point["container"]
            and uniform["inherited_point_core_source"]["path"] == old_doc["guard_certificate"]
            and uniform["inherited_point_core_source"]["sha256"]
            == old_doc["guard_certificate_sha256"],
            "transferred core/parent identity differs",
        )
    result = construct(rows, groups, fresh, mode=mode, deadline=deadline)
    for path, (sha, ceiling) in held.items():
        require(finite.digest(path, ceiling, deadline) == sha, "propagation premise changed")
    require(finite.canonical(document) == frozen, "propagation descriptor changed")
    tick(deadline)
    return {
        "schema": SCHEMA,
        "mode": mode,
        **result,
        "accepted_inputs": copy.deepcopy(document),
        "guard": copy.deepcopy(uniform["guard"] if uniform is not None else context["guard"]),
        "parent_custody": copy.deepcopy(point["parent_custody"]),
        "container": copy.deepcopy(point["container"]),
        "original_endpoint_control": copy.deepcopy(point["original_endpoint_control"]),
        "original_rows_inherited": 1056,
        "original_parent_proof_replayed": False,
        "root_proof_replayed": False,
        "point_conditioning_reconstructed": False,
        "original17_endpoint_retention_inherited": True,
        "old_owner0_target_rows_transferred": False,
        "prior_collective_finite_reconstructions": 1,
        "prior_collective_work": copy.deepcopy(fresh["work"]),
        "uniform_transfer_rechecked": uniform is not None,
        "mathematical_assurance": (
            "sole-Astra one-round hand composition plus fresh finite reconstruction"
        ),
        "limits": {
            "output_bytes": OUTPUT_LIMIT,
            "geometry_bits": finite.BIT_LIMIT,
            "recovered_vertices": guard.OWNED_LIMIT,
            "owner0_vertices": guard.OWNER0_LIMIT,
            "recovery_support_products": guard.RECOVERY_SUPPORT_LIMIT,
            "strict_vertex_pairs": guard.STRICT_PAIR_LIMIT,
            "strict_quadratic_checks": guard.STRICT_CHECK_LIMIT,
            "intersection_input_products": INTERSECTION_PRODUCTS,
            "intersection_output_vertices": guard.INTERSECTION_LIMIT,
            "prior_and_new_collective_caps_unchanged_and_separate": True,
        },
        "resource_assurance": {
            "intersection_products_precharged": True,
            "trusted_unreduced_integer_products_individually_bounded": False,
            "sweep_internal_event_caps_enforced": False,
            "outer_supervision_required": True,
        },
    }


def check(
    document: dict[str, Any], certificate: dict[str, Any], *, deadline: float
) -> dict[str, Any]:
    expected = generate(document, deadline=deadline)
    require(payload(certificate) == expected, "fresh one-round propagation differs")
    tick(deadline)
    return copy.deepcopy(expected) | {"verification_passed": True}


def failure(exc: Exception) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "status": "incomplete" if isinstance(exc, IncompleteError) else "refused",
        "error": str(exc),
        "criterion_met": False,
        "verification_passed": False,
        **scope("point"),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--descriptor", type=Path, required=True)
    parser.add_argument("--certificate", type=Path)
    parser.add_argument("--max-seconds", type=float, default=180)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    if not math.isfinite(args.max_seconds) or args.max_seconds <= 0:
        parser.error("max-seconds must be finite and positive")
    deadline = time.monotonic() + args.max_seconds
    try:
        require(
            not any(
                n == p or n.startswith(p + ".")
                for n in sys.modules
                for p in (*finite.FORBIDDEN, "devtools.produce_n17_conditional_owned_hull")
            ),
            "producer/kernel/root import in propagation checker",
        )
        raw, doc = finite.read_json(args.descriptor, parent.JSON_LIMIT)
        if args.certificate:
            saved, cert = finite.read_json(args.certificate, OUTPUT_LIMIT)
            result = check(doc, cert, deadline=deadline)
            require(
                saved == finite.read_json(args.certificate, OUTPUT_LIMIT)[0],
                "certificate changed",
            )
        else:
            result = generate(doc, deadline=deadline)
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
        provenance=provenance(
            Path(__file__),
            Path(collective.__file__),
            Path(cast(str, transfer.__file__)),
            Path(cast(str, guard.__file__)),
        ),
        invocation={
            "argv": argv if argv is not None else sys.argv[1:],
            "executable": sys.executable,
        },
    )
    text = retained_json.dumps(result, sort_keys=True)
    if len(text.encode()) > OUTPUT_LIMIT or time.monotonic() >= deadline:
        result = failure(IncompleteError("propagation output byte or wall ceiling"))
        text = retained_json.dumps(result, sort_keys=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text)
    return (
        0
        if result["status"]
        in ("context_excluded", "additional_angle_union_restricted", "criterion_missed")
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
