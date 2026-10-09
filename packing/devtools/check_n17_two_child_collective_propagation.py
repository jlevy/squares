"""Two exhaustive closed centre cases on an inherited complete regional proof."""

from __future__ import annotations

import argparse
import copy
import math
import sys
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, cast

from devtools import check_n17_one_round_owned_domain_propagation as previous
from devtools.provenance import provenance
from sqpack import retained_json

collective, guard, parent, finite, cases = (
    previous.collective,
    previous.guard,
    previous.parent,
    previous.finite,
    previous.cases,
)
selection_tool = collective.prior
require, tick, checked = previous.require, previous.tick, previous.checked
IncompleteError = previous.IncompleteError
type Point = tuple[Q, Q]
OWNERS = previous.OWNERS
SCHEMA = "n17-two-child-collective-propagation/v1"
DESCRIPTOR_SCHEMA = "n17-two-child-collective-propagation-context/v1"
ROLES = (
    "propagation_descriptor",
    "propagation_certificate",
    "propagation_replay",
    "selection_certificate",
    "selection_replay",
)
SELECTED_OWNER = 18
AXIS = 0
MIDPOINT = Q(471, 250)
OUTPUT_LIMIT = 64 << 20
CLIP_VERTICES = 2097152
INTERSECTION_PRODUCTS = 2000000
payload = previous.payload


def scope(*, progress: bool = False, contradiction: bool = False) -> dict[str, bool]:
    return {
        **guard.scope(),
        "regional_necessary_domain_restriction_proved": progress,
        "regional_guard_exclusion_proved": contradiction,
        "declared_guard_exclusion_proved": contradiction,
        "point_guard_exclusion_proved": False,
        "point_contradiction_proved": False,
        "point_guard_necessary_domain_restriction_proved": False,
    }


def apply_decisions(
    rows: dict[int, list[dict[str, Any]]], prior: dict[str, Any], deadline: float
) -> dict[int, list[dict[str, Any]]]:
    """Join the complete saved pass; do not repeat its accepted arithmetic proof."""
    require(
        prior["all_foreign_rows_accounted"] == 992
        and prior["changed_owners"] == []
        and prior["complete_empty_owners"] == []
        and prior["recovered_groups_frozen_during_collective_pass"] is True,
        "complete unchanged prior collective premise required",
    )
    effective = copy.deepcopy(rows)
    require(len(prior["owners"]) == 16, "prior collective owner roster differs")
    for owner, entry in zip(OWNERS[1:], prior["owners"], strict=True):
        original = rows[owner]
        require(
            entry["owner"] == owner
            and len(entry["rows"]) == len(original)
            and entry["lost_length"] == "0",
            "prior collective row count or loss differs",
        )
        for index, (row, decision) in enumerate(zip(original, entry["rows"], strict=True)):
            tick(deadline)
            require(
                type(decision["row_index"]) is int
                and decision["row_index"] == index
                and decision["reference"] == row["reference"]
                and decision["interval"] == row["interval"]
                and type(decision["covered"]) is bool
                and decision["inherited_domain_nonempty"] is bool(row["domain"])
                and decision["domain_retained_unchanged"]
                is (bool(row["domain"]) and not decision["covered"])
                and not (row["domain"] and decision["covered"]),
                "prior effective row identity or new deletion differs",
            )
            if decision["covered"]:
                effective[owner][index]["domain"] = []
        union = interval_union(effective[owner])
        require(
            union == entry["old_closed_interval_union"] == entry["new_closed_interval_union"],
            "accepted base closed union differs",
        )
    return effective


def interval_union(rows: list[dict[str, Any]]) -> list[list[str]]:
    return [
        list(map(str, interval))
        for interval in collective.union_intervals(
            [tuple(map(finite.rational, row["interval"])) for row in rows if row["domain"]]
        )
    ]


def intake(document: Any, deadline: float) -> tuple[Any, ...]:
    require(
        type(document) is dict
        and document.get("schema") == DESCRIPTOR_SCHEMA
        and set(document) == {"schema", *(k for r in ROLES for k in (r, r + "_sha256"))},
        "two-case descriptor differs",
    )
    held: dict[Path, tuple[str, int]] = {}
    values = {
        role: previous.read_bound(
            role,
            document,
            held,
            deadline,
            parent.JSON_LIMIT if role.endswith("descriptor") else OUTPUT_LIMIT,
        )
        for role in ROLES
    }
    descriptor = values["propagation_descriptor"]
    accepted, replay = values["propagation_certificate"], values["propagation_replay"]
    require(
        descriptor["schema"] == previous.DESCRIPTOR_SCHEMA
        and descriptor["mode"] == "direct_regional"
        and set(descriptor)
        == {"schema", "mode", *(k for r in previous.DIRECT_ROLES for k in (r, r + "_sha256"))}
        and accepted["schema"] == previous.SCHEMA
        and accepted["accepted_inputs"] == descriptor
        and accepted["mode"] == "direct_regional"
        and accepted["status"] == "criterion_missed"
        and accepted["criterion_met"] is False
        and replay.get("verification_passed") is True
        and payload(accepted) == payload(replay)
        and accepted["closure"] is None
        and accepted["changed_owners"] == []
        and accepted["new_live_row_deletions"] == 0
        and accepted["original_rows_inherited"] == 1056
        and accepted["prior_effective_rows_accounted"] == 992
        and accepted["new_collective_rows_accounted"] == 992
        and accepted["all_foreign_recoveries_and_strict_checks_completed"] is True
        and accepted["owner0_core_unchanged"] is True
        and accepted["no_sequential_feedback"] is True
        and accepted["one_recovery_and_at_most_one_collective_pass"] is True
        and accepted["accepted_regional_conditioning_inherited"] is True
        and accepted["regional_conditioning_reconstructed"] is False
        and accepted["prior_regional_collective_finite_reconstructions"] == 1
        and accepted["prior_primary_same25_criterion_met"] is False
        and accepted["prior_component_parameter_loss"] == "11/32"
        and all(accepted.get(k) is False for k in scope()),
        "accepted wider complete fixed-point premise differs",
    )
    regional_values = {
        role: previous.read_bound(
            role,
            descriptor,
            held,
            deadline,
            parent.JSON_LIMIT if role.endswith("descriptor") else OUTPUT_LIMIT,
        )
        for role in previous.DIRECT_ROLES
    }
    original = regional_values["regional_certificate"]
    require(
        original["accepted_inputs"] == regional_values["regional_descriptor"]
        and payload(original) == payload(regional_values["regional_replay"])
        and regional_values["regional_replay"].get("verification_passed") is True
        and original["parent_custody"] == accepted["parent_custody"]
        and original["container"] == accepted["container"]
        and original["original_endpoint_control"] == accepted["original_endpoint_control"]
        and original["regional_context"]["guard"] == accepted["guard"]
        and accepted["container"]
        == guard.standing.CenteredContainer(cases.U, cases.V).record(),
        "inherited regional context ancestry differs",
    )
    witness = original["matched_owned_point_witness"]
    centre = list(map(finite.rational, witness["centre"]))
    require(len(centre) == 2 and witness["tau"] == str(guard.TAU), "matched pose differs")
    h = previous.regional.HALF_WIDTH
    require(
        accepted["guard"]
        == {
            "half_width": str(h),
            "angle_interval": [str(guard.TAU - h), str(guard.TAU + h)],
            "centre_box": [[str(checked(x - h)), str(checked(x + h))] for x in centre],
        },
        "nonzero wider guard differs",
    )
    endpoint = accepted["original_endpoint_control"]
    require(
        endpoint["all17_retained"] is True
        and endpoint["family_disjoint"] is True
        and [w["label"] for w in endpoint["witnesses"]] == list(range(1, 18))
        and {w["owner"] for w in endpoint["witnesses"]} == set(OWNERS)
        and endpoint["witnesses"][0]["owner"] == 0
        and endpoint["witnesses"][5]["owner"] == 12
        and endpoint["witnesses"][10]["owner"] == 18,
        "inherited full endpoint/family control differs",
    )
    previous.direct_dependencies(
        regional_values["regional_descriptor"], original, held, deadline
    )
    reference = accepted["parent_custody"]["typed_reference_context"]
    rows, old_groups = collective.context_geometry(
        original["regional_context"], reference, deadline
    )
    effective, roster = previous.prune_prior(
        rows, original["collective"], deadline, direct_regional=True
    )
    require(
        roster == accepted["prior_row_restriction"], "accepted prior restriction roster differs"
    )
    effective = apply_decisions(effective, accepted["new_collective"], deadline)
    raw_groups = accepted["recovered_owned_groups"]
    require(set(raw_groups) == set(map(str, OWNERS)), "accepted recovered owner roster differs")
    counter = [
        sum(len(row["domain"]) for entries in rows.values() for row in entries)
        + sum(map(len, old_groups.values()))
    ]
    groups = {
        o: selection_tool.parse_polygon(
            raw_groups[str(o)],
            counter,
            deadline,
            guard.OWNER0_LIMIT if o == 0 else guard.OWNED_LIMIT,
        )
        for o in OWNERS
    }
    require(
        groups[0] == old_groups[0]
        and accepted["recovered_group_vertex_counts"]
        == {str(o): len(groups[o]) for o in OWNERS},
        "accepted recovered group/core identity differs",
    )
    selection, selected_replay = values["selection_certificate"], values["selection_replay"]
    require(
        selection["schema"] == selection_tool.SCHEMA
        and selection["status"] == "criterion_missed"
        and selection["criterion_met"] is False
        and selected_replay.get("verification_passed") is True
        and payload(selection) == payload(selected_replay)
        and selection["selection"]["owner"] == SELECTED_OWNER
        and type(selection["selection"]["owner"]) is int
        and selection["selection"]["axis"] == AXIS
        and type(selection["selection"]["axis"]) is int
        and selection["selection"]["midpoint"] == str(MIDPOINT)
        and all(
            selection["parent_custody"][k] == accepted["parent_custody"][k]
            for k in (
                "seed_sha256",
                "node_sha256",
                "compressed_sha256",
                "h290_receipt",
                "h290_receipt_sha256",
                "typed_reference_context",
            )
        ),
        "historical cut or same-parent selection premise differs",
    )
    return effective, groups, accepted, held


def clip_rows(
    rows: list[dict[str, Any]], side: int, work: dict[str, int], deadline: float
) -> list[dict[str, Any]]:
    require(side in (-1, 1), "closed case side differs")
    result = copy.deepcopy(rows)
    sign = -side
    for row in result:
        row["domain"] = cases.clip(
            row["domain"], Q(sign), Q(0), checked(sign * MIDPOINT), guard.DOMAIN_LIMIT, deadline
        )
        work["generated_clip_vertices"] += len(row["domain"])
        if work["generated_clip_vertices"] > CLIP_VERTICES:
            raise IncompleteError("two-case cumulative clip vertex ceiling")
    return result


def selected_intersection(
    groups: dict[int, list[Point]], work: dict[str, int], deadline: float
) -> dict[str, Any] | None:
    for other in OWNERS:
        if other == SELECTED_OWNER or not groups[SELECTED_OWNER] or not groups[other]:
            continue
        tick(deadline)
        work["intersection_vertex_pairs"] += len(groups[SELECTED_OWNER]) * len(groups[other])
        if work["intersection_vertex_pairs"] > INTERSECTION_PRODUCTS:
            raise IncompleteError("two-case cumulative intersection product ceiling")
        overlap = cases.conditional.intersection(groups[SELECTED_OWNER], groups[other])
        tick(deadline)
        if len(overlap) > guard.INTERSECTION_LIMIT:
            raise IncompleteError("two-case intersection output ceiling")
        if overlap:
            return {
                "kind": "shared_strictly_owned_point",
                "owners": [SELECTED_OWNER, other],
                "intersection": finite.serial([(checked(x), checked(y)) for x, y in overlap]),
            }
    return None


def case_result(  # noqa: PLR0917
    rows: dict[int, list[dict[str, Any]]],
    groups: dict[int, list[Point]],
    side: int,
    work: dict[str, int],
    recovery: dict[str, int],
    deadline: float,
) -> dict[str, Any]:
    child = copy.deepcopy(rows)
    child[SELECTED_OWNER] = clip_rows(child[SELECTED_OWNER], side, work, deadline)
    snapshot = copy.deepcopy(child)
    inherited = copy.deepcopy(groups)
    closure = None
    if not any(row["domain"] for row in child[SELECTED_OWNER]):
        closure = {
            "kind": "selected_owner_cover_empty",
            "owner": SELECTED_OWNER,
            "row_count": len(child[SELECTED_OWNER]),
        }
    else:
        inherited[SELECTED_OWNER] = guard.common_owned(
            child[SELECTED_OWNER], recovery, deadline
        )
        closure = selected_intersection(inherited, work, deadline)
    require(
        child == snapshot
        and all(inherited[o] == groups[o] for o in OWNERS if o != SELECTED_OWNER),
        "case recovery changed frozen domains or other groups",
    )
    coverage = None
    surviving = copy.deepcopy(child)
    if closure is None:
        frozen = copy.deepcopy(inherited)
        coverage = collective.construct(child, inherited, deadline=deadline)
        require(
            coverage["all_foreign_rows_accounted"] == 992
            and inherited == frozen
            and child == snapshot,
            "complete immutable case collective pass required",
        )
        for owner, entry in zip(OWNERS[1:], coverage["owners"], strict=True):
            require(
                entry["owner"] == owner and len(entry["rows"]) == len(child[owner]),
                "case coverage row roster differs",
            )
            for index, decision in enumerate(entry["rows"]):
                row = child[owner][index]
                require(
                    decision["row_index"] == index
                    and decision["reference"] == row["reference"]
                    and decision["interval"] == row["interval"]
                    and decision["inherited_domain_nonempty"] is bool(row["domain"]),
                    "case collective decision identity differs",
                )
                if decision["covered"]:
                    surviving[owner][index]["domain"] = []
        if coverage["complete_empty_owners"]:
            closure = {
                "kind": "collective_owner_cover_empty",
                "owners": list(coverage["complete_empty_owners"]),
                "closed_cover_accounted": 992,
            }
        for key in (
            "point_guard_necessary_domain_restriction_proved",
            "point_contradiction_proved",
            "original_owned_sets_unchanged",
            "simultaneous_original_groups_only",
        ):
            coverage.pop(key)
        coverage["case_groups_frozen_during_collective_pass"] = True
    tick(deadline)
    return {
        "side": side,
        "halfplane": {
            "axis": AXIS,
            "relation": "<=" if side == -1 else ">=",
            "midpoint": str(MIDPOINT),
        },
        "closed": closure is not None,
        "closure": closure,
        "selected_owner_clipped_rows": [
            {
                "row_index": i,
                "reference": copy.deepcopy(row["reference"]),
                "interval": list(row["interval"]),
                "domain": finite.serial(row["domain"]),
            }
            for i, row in enumerate(child[SELECTED_OWNER])
        ],
        "selected_owned_group": finite.serial(inherited[SELECTED_OWNER]),
        "other_owned_groups_unchanged": True,
        "collective": coverage,
        "collective_rows_accounted": 992 if coverage is not None else 0,
        "surviving_rows": {
            str(o): [
                {
                    "row_index": i,
                    "reference": copy.deepcopy(r["reference"]),
                    "interval": list(r["interval"]),
                    "live": bool(r["domain"]) and closure is None,
                }
                for i, r in enumerate(surviving[o])
            ]
            for o in OWNERS[1:]
        },
    }


def combine(
    rows: dict[int, list[dict[str, Any]]], children: list[dict[str, Any]], deadline: float
) -> list[dict[str, Any]]:
    require([c["side"] for c in children] == [-1, 1], "both closed halfspace cases required")
    result = []
    for owner in OWNERS[1:]:
        baseline = interval_union(rows[owner])
        live = []
        for index, row in enumerate(rows[owner]):
            tick(deadline)
            flags = []
            for child in children:
                roster = child["surviving_rows"][str(owner)]
                require(len(roster) == len(rows[owner]), "case surviving roster differs")
                record = roster[index]
                require(
                    record["row_index"] == index
                    and record["reference"] == row["reference"]
                    and record["interval"] == row["interval"]
                    and type(record["live"]) is bool
                    and not (record["live"] and not row["domain"])
                    and not (record["live"] and child["closed"]),
                    "case surviving row identity differs",
                )
                flags.append(record["live"])
            if any(flags):
                live.append(tuple(map(finite.rational, row["interval"])))
        union = collective.union_intervals(live)
        old = [tuple(map(finite.rational, interval)) for interval in baseline]
        require(
            all(any(a <= lo <= hi <= b for a, b in old) for lo, hi in union),
            "combined union escaped base",
        )
        lost = checked(collective.length(old) - collective.length(union))
        require(lost >= 0, "combined closed union grew")
        result.append(
            {
                "owner": owner,
                "baseline_closed_interval_union": baseline,
                "combined_surviving_closed_interval_union": [list(map(str, p)) for p in union],
                "additional_lost_length": str(lost),
            }
        )
    return result


def construct(
    rows: dict[int, list[dict[str, Any]]], groups: dict[int, list[Point]], *, deadline: float
) -> dict[str, Any]:
    require(
        set(rows) == set(OWNERS[1:])
        and sum(map(len, rows.values())) == 992
        and set(groups) == set(OWNERS),
        "full two-case base roster required",
    )
    work = {"generated_clip_vertices": 0, "intersection_vertex_pairs": 0}
    recovery = guard.new_work()
    children = []
    try:
        for side in (-1, 1):
            # Preserve the complete prefix if the following case exceeds a ceiling.
            children.append(case_result(rows, groups, side, work, recovery, deadline))  # noqa: PERF401
        unions = combine(rows, children, deadline)
    except IncompleteError as exc:
        raise guard.ContextIncompleteError(
            str(exc),
            {
                "finished_children_candidates": children,
                "child_work": work,
                "recovery_work": recovery,
            },
        ) from exc
    changed = [r["owner"] for r in unions if finite.rational(r["additional_lost_length"]) > 0]
    both_closed = all(c["closed"] for c in children)
    cumulative = {
        key: sum(c["collective"]["work"][key] for c in children if c["collective"] is not None)
        for key in collective.new_work()
    }
    tick(deadline)
    return {
        "status": "regional_guard_excluded"
        if both_closed
        else "additional_angle_union_restricted"
        if changed
        else "criterion_missed",
        "criterion_met": bool(both_closed or changed),
        **scope(progress=bool(changed), contradiction=both_closed),
        "both_children_closed": both_closed,
        "closed_case_count": sum(c["closed"] for c in children),
        "children": children,
        "combined_restrictions": unions,
        "changed_owners": changed,
        "child_work": work,
        "recovery_work": recovery,
        "cumulative_collective_work": cumulative,
        "fixed_selection": {"owner": SELECTED_OWNER, "axis": AXIS, "midpoint": str(MIDPOINT)},
        "survivors_unioned_across_cases": True,
        "other_groups_inherited_and_unchanged": True,
        "one_selected_owner_recovery_per_live_case": True,
        "no_sequential_feedback": True,
        "base_foreign_rows_accounted": 992,
    }


def generate(document: dict[str, Any], *, deadline: float) -> dict[str, Any]:
    frozen = finite.canonical(document)
    rows, groups, accepted, held = intake(document, deadline)
    result = construct(rows, groups, deadline=deadline)
    for path, (sha, ceiling) in held.items():
        require(finite.digest(path, ceiling, deadline) == sha, "two-case premise changed")
    require(finite.canonical(document) == frozen, "two-case descriptor changed")
    tick(deadline)
    return {
        "schema": SCHEMA,
        **result,
        "accepted_inputs": copy.deepcopy(document),
        "guard": copy.deepcopy(accepted["guard"]),
        "container": copy.deepcopy(accepted["container"]),
        "parent_custody": copy.deepcopy(accepted["parent_custody"]),
        "original_endpoint_control": copy.deepcopy(accepted["original_endpoint_control"]),
        "original_rows_inherited": 1056,
        "base_proof_inherited": True,
        "base_geometry_parsed_once": True,
        "base_collective_arithmetic_replayed": False,
        "original_parent_proof_replayed": False,
        "root_proof_replayed": False,
        "original17_endpoint_retention_inherited": True,
        "selection_recomputed": False,
        "selection_point_geometry_used": False,
        "tiny_guard_geometry_used": False,
        "mathematical_assurance": (
            "sole-Astra hand composition and fresh two-case finite reconstruction"
        ),
        "limits": {
            "output_bytes": OUTPUT_LIMIT,
            "geometry_bits": finite.BIT_LIMIT,
            "inherited_geometry_vertices": parent.INPUT_VERTICES,
            "child_domain_vertices": guard.DOMAIN_LIMIT,
            "generated_clip_vertices": CLIP_VERTICES,
            "recovered_group_vertices": guard.OWNED_LIMIT,
            "intersection_products": INTERSECTION_PRODUCTS,
            "intersection_output_vertices": guard.INTERSECTION_LIMIT,
            "recovery_support_products": guard.RECOVERY_SUPPORT_LIMIT,
            "strict_vertex_pairs": guard.STRICT_PAIR_LIMIT,
            "strict_quadratic_checks": guard.STRICT_CHECK_LIMIT,
            "per_case_collective_minkowski_products": collective.MINK_LIMIT,
            "per_case_collective_point_products": collective.POINT_PRODUCTS,
            "per_case_collective_sweep_pairs": collective.EDGE_PAIRS,
            "cumulative_collective_minkowski_products": 2 * collective.MINK_LIMIT,
            "cumulative_collective_point_products": 2 * collective.POINT_PRODUCTS,
            "cumulative_collective_sweep_pairs": 2 * collective.EDGE_PAIRS,
        },
        "resource_assurance": {
            "per_case_collective_limits_unchanged_and_stricter_than_aggregate": True,
            "clip_recovery_intersection_work_shared": True,
            "sweep_internal_event_caps_enforced": False,
            "unreduced_integer_products_individually_bounded": False,
            "outer_supervision_required": True,
        },
    }


def check(
    document: dict[str, Any], certificate: dict[str, Any], *, deadline: float
) -> dict[str, Any]:
    result = generate(document, deadline=deadline)
    require(payload(certificate) == result, "fresh two-case reconstruction differs")
    return result | {"verification_passed": True}


def failure(exc: Exception) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "status": "incomplete" if isinstance(exc, IncompleteError) else "refused",
        "criterion_met": False,
        "verification_passed": False,
        **scope(),
        "error": str(exc),
        "candidate_observations": getattr(exc, "observations", None),
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
            "producer/kernel/root import in two-case checker",
        )
        raw, document = finite.read_json(args.descriptor, parent.JSON_LIMIT)
        if args.certificate:
            saved, certificate = finite.read_json(args.certificate, OUTPUT_LIMIT)
            result = check(document, certificate, deadline=deadline)
            require(
                saved == finite.read_json(args.certificate, OUTPUT_LIMIT)[0],
                "saved certificate changed",
            )
        else:
            result = generate(document, deadline=deadline)
        require(
            raw == finite.read_json(args.descriptor, parent.JSON_LIMIT)[0],
            "descriptor bytes changed",
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
            Path(previous.__file__),
            Path(cast(str, collective.__file__)),
            Path(cast(str, guard.__file__)),
        ),
        invocation={
            "argv": argv if argv is not None else sys.argv[1:],
            "executable": sys.executable,
        },
    )
    text = retained_json.dumps(result, sort_keys=True)
    if len(text.encode()) > OUTPUT_LIMIT or time.monotonic() >= deadline:
        result = failure(IncompleteError("two-case output byte or wall ceiling"))
        text = retained_json.dumps(result, sort_keys=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text)
    return (
        0
        if result["status"]
        in ("regional_guard_excluded", "additional_angle_union_restricted", "criterion_missed")
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
