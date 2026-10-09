"""Reconstruct a regional guard and check the same 25 accepted point-restricted rows."""

from __future__ import annotations

import argparse
import copy
import math
import sys
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, cast

from devtools import check_n17_collective_row_coverage as collective
from devtools.provenance import provenance
from sqpack import retained_json

parent, finite, cases, guard = (
    collective.parent,
    collective.finite,
    collective.cases,
    collective.guard,
)
type Point = tuple[Q, Q]
require, tick = collective.require, collective.tick
IncompleteError = collective.IncompleteError
SCHEMA = "n17-regional-row-coverage/v1"
DESCRIPTOR_SCHEMA = "n17-regional-row-coverage-context/v1"
ROLES = (*parent.INPUTS, "collective_certificate", "collective_replay")
TARGET_OWNER = 18
TARGET_INDICES = (*range(19, 24), *range(33, 53))
HALF_WIDTH = Q(1, 512)
OUTPUT_LIMIT = 64 << 20
CUSTODY_KEYS = (
    "h290_receipt",
    "h290_receipt_sha256",
    "seed_sha256",
    "node_sha256",
    "compressed_sha256",
    "steps",
    "typed_reference_context",
    "accepted_parent_premises",
)
payload = collective.payload


def selected_rows(
    accepted: dict[str, Any], cells: dict[str, Any], reference: dict[str, Any]
) -> list[dict[str, Any]]:
    """Bind the inherited finite selection to every original typed closed row."""
    require(
        accepted["schema"] == collective.SCHEMA
        and accepted["status"] == "angle_union_restricted"
        and accepted["criterion_met"] is True
        and accepted["all_foreign_rows_accounted"] == 992
        and accepted["simultaneous_original_groups_only"] is True
        and accepted["original_owned_sets_unchanged"] is True
        and accepted["changed_owners"] == [TARGET_OWNER]
        and accepted["complete_empty_owners"] == []
        and accepted["point_contradiction_proved"] is False
        and accepted["declared_guard_exclusion_proved"] is False
        and accepted["point_guard_necessary_domain_restriction_proved"] is True
        and accepted["original_rows_inherited"] == 1056
        and accepted["original_endpoint_control"]["all17_retained"] is True
        and accepted["original_endpoint_control"]["family_disjoint"] is True
        and all(accepted.get(k) is False for k in guard.scope()),
        "accepted SAME25 point restriction premise differs",
    )
    owners = accepted["owners"]
    require(
        [entry["owner"] for entry in owners] == list(collective.OWNERS[1:]),
        "accepted collective owner roster differs",
    )
    selected = []
    for entry in owners:
        owner = entry["owner"]
        raw = cells[str(owner)]
        parent.closed_rows(raw, owner, 32 if owner == 12 else 64, reference)
        require(len(entry["rows"]) == len(raw), "accepted collective row count differs")
        removed = []
        for index, (saved, original) in enumerate(zip(entry["rows"], raw, strict=True)):
            require(
                type(saved["row_index"]) is int
                and saved["row_index"] == index
                and saved["reference"] == original["reference"]
                and saved["interval"] == original["interval"]
                and type(saved["covered"]) is bool
                and type(saved["inherited_domain_nonempty"]) is bool,
                "accepted collective original row identity differs",
            )
            if saved["covered"] and saved["inherited_domain_nonempty"]:
                removed.append(index)
                if owner == TARGET_OWNER:
                    selected.append(
                        {
                            "row_index": index,
                            "reference": copy.deepcopy(saved["reference"]),
                            "interval": list(saved["interval"]),
                        }
                    )
        require(
            removed == (list(TARGET_INDICES) if owner == TARGET_OWNER else []),
            "accepted SAME25 removed roster differs",
        )
        require(
            entry["lost_length"] == ("25/64" if owner == TARGET_OWNER else "0"),
            "accepted point interval loss differs",
        )
    return selected


def intake(document: dict[str, Any], *, deadline: float) -> tuple[Any, ...]:
    require(
        type(document) is dict
        and document.get("schema") == DESCRIPTOR_SCHEMA
        and set(document) == {"schema", *(k for r in ROLES for k in (r, r + "_sha256"))},
        "regional descriptor differs",
    )
    frozen = finite.canonical(document)
    held: dict[Path, tuple[str, int]] = {}
    pairs = []
    for role in ROLES[-2:]:
        path = finite.retained_path(document[role])
        raw, value = finite.read_json(path, OUTPUT_LIMIT)
        require(
            finite.digest(path, OUTPUT_LIMIT, deadline) == document[role + "_sha256"]
            and raw == finite.read_json(path, OUTPUT_LIMIT)[0],
            "regional collective input byte custody differs",
        )
        held[path] = (document[role + "_sha256"], OUTPUT_LIMIT)
        pairs.append(value)
    accepted, replay = pairs
    require(
        type(accepted) is dict
        and type(replay) is dict
        and replay.get("verification_passed") is True
        and payload(accepted) == payload(replay),
        "accepted collective fresh payload differs",
    )
    accepted = cast(dict[str, Any], accepted)
    base = {"schema": parent.DESCRIPTOR_SCHEMA}
    base.update({k: document[k] for r in parent.INPUTS for k in (r, r + "_sha256")})
    final, custody, roster, centre = parent.intake(base, held, deadline)
    parent_custody = {k: copy.deepcopy(custody[k]) for k in CUSTODY_KEYS}
    require(accepted["parent_custody"] == parent_custody, "regional parent custody differs")
    inherited = accepted["accepted_inputs"]
    require(inherited["schema"] == collective.DESCRIPTOR_SCHEMA, "collective context differs")
    path = finite.retained_path(inherited["guard_descriptor"])
    raw, historical = finite.read_json(path, parent.JSON_LIMIT)
    require(
        finite.digest(path, parent.JSON_LIMIT, deadline) == inherited["guard_descriptor_sha256"]
        and raw == finite.read_json(path, parent.JSON_LIMIT)[0],
        "accepted point descriptor byte custody differs",
    )
    held[path] = (inherited["guard_descriptor_sha256"], parent.JSON_LIMIT)
    require(
        historical == {**base, "schema": guard.DESCRIPTOR_SCHEMA},
        "regional seven-role original input identities differ",
    )
    gate = finite.read_json(finite.retained_path(base["parent_descriptor"]), parent.JSON_LIMIT)[
        1
    ]
    selected = selected_rows(accepted, final["cells"], custody["typed_reference_context"])
    return final, gate["label_to_owner"], roster, centre, parent_custody, selected, held, frozen


def regional_decision(
    context: dict[str, Any],
    selected: list[dict[str, Any]],
    *,
    deadline: float,
    reference_context: dict[str, Any],
) -> dict[str, Any]:
    require(
        [r["row_index"] for r in selected] == list(TARGET_INDICES),
        "regional SAME25 requested roster differs",
    )
    require(
        context["all_original_rows_checked"] == 1056
        and context["all_foreign_rows_conditioned"] == 992
        and context["context_nonzero"] is True,
        "complete regional conditioning differs",
    )
    if context["closure"] is not None:
        return {
            "status": "regional_guard_excluded",
            "criterion_met": True,
            "declared_guard_exclusion_proved": True,
            "regional_necessary_domain_restriction_proved": True,
            "same25_rows_excluded": True,
            "same25_coverage_checks_performed": 0,
            "requested_row_disposition": (
                "logical_consequence_of_checked_regional_contradiction"
            ),
            "requested_rows": copy.deepcopy(selected),
            "collective": None,
            "regional_closure": copy.deepcopy(context["closure"]),
        }
    rows, groups = collective.context_geometry(context, reference_context, deadline)
    finite_result = collective.construct(rows, groups, deadline=deadline)
    require(finite_result["all_foreign_rows_accounted"] == 992, "regional coverage incomplete")
    owner = next(r for r in finite_result["owners"] if r["owner"] == TARGET_OWNER)
    decisions = []
    for requested in selected:
        row = owner["rows"][requested["row_index"]]
        require(
            row["reference"] == requested["reference"]
            and row["interval"] == requested["interval"],
            "regional SAME25 row identity differs",
        )
        decisions.append({**copy.deepcopy(requested), "covered": row["covered"]})
    success = all(row["covered"] for row in decisions)
    empty_owners = finite_result["complete_empty_owners"]
    collective_closure = None
    if empty_owners:
        emptied = next(r for r in finite_result["owners"] if r["owner"] == min(empty_owners))
        require(
            emptied["new_closed_interval_union"] == [], "empty regional owner has live seam"
        )
        collective_closure = {
            "kind": "collective_owner_cover_empty",
            "owner": emptied["owner"],
            "rows": [
                {k: copy.deepcopy(r[k]) for k in ("row_index", "reference", "interval")}
                for r in emptied["rows"]
            ],
            "new_closed_interval_union": [],
        }
    # The reused finite routine's point-only proof labels do not describe this context.
    finite_result = {
        k: v
        for k, v in finite_result.items()
        if k
        not in {
            "criterion_met",
            "status",
            "point_guard_necessary_domain_restriction_proved",
            "point_contradiction_proved",
        }
    }
    return {
        "status": "regional_guard_excluded"
        if collective_closure
        else "same25_regional_rows_restricted"
        if success
        else "criterion_missed",
        "criterion_met": success or bool(collective_closure),
        "declared_guard_exclusion_proved": bool(collective_closure),
        "regional_necessary_domain_restriction_proved": success or bool(collective_closure),
        "same25_rows_excluded": success or bool(collective_closure),
        "collective_closure": collective_closure,
        "regional_closure": collective_closure,
        "same25_coverage_checks_performed": len(decisions),
        "requested_row_disposition": (
            "logical_consequence_of_checked_regional_contradiction"
            if collective_closure
            else "fresh_complete_regional_union_coverage"
        ),
        "requested_rows": decisions,
        "collective": finite_result,
    }


def construct(
    cells: dict[str, Any],
    roles: dict[str, int],
    roster: Any,
    centre: Point,
    selected: list[dict[str, Any]],
    *,
    deadline: float,
    reference_context: dict[str, Any],
) -> dict[str, Any]:
    require(
        set(roles) == set(map(str, range(1, 18)))
        and roles["1"] == 0
        and roles["6"] == 12
        and roles["11"] == 18
        and set(roles.values()) == set(collective.OWNERS)
        and all(type(owner) is int for owner in roles.values())
        and set(cells) == set(map(str, roles.values())),
        "regional original label/owner roster differs",
    )
    require(
        [r["row_index"] for r in selected] == list(TARGET_INDICES),
        "regional SAME25 requested roster differs",
    )
    require(
        all(
            r["reference"] == cells["18"][r["row_index"]]["reference"]
            and r["interval"] == cells["18"][r["row_index"]]["interval"]
            for r in selected
        ),
        "regional SAME25 original identities differ",
    )
    counter = [0]
    original = {}
    core_cache: dict[Any, list[Point]] = {}
    for owner in sorted(roles.values()):
        raw = cells[str(owner)]
        parent.closed_rows(raw, owner, 32 if owner == 12 else 64, reference_context)
        original[owner] = [parent.row_domain(r, counter, deadline, core_cache) for r in raw]
        require(any(r["domain"] for r in original[owner]), "original endpoint all-empty owner")
    endpoint = parent.endpoint_control(roster, original, roles, deadline)
    work = guard.new_work()
    context = guard.condition_context(
        cells, original, centre, counter, work, deadline, half_width=HALF_WIDTH
    )
    expected_guard = {
        "half_width": str(HALF_WIDTH),
        "centre_box": [
            [str(finite.checked(x - HALF_WIDTH)), str(finite.checked(x + HALF_WIDTH))]
            for x in centre
        ],
        "angle_interval": [str(guard.TAU - HALF_WIDTH), str(guard.TAU + HALF_WIDTH)],
    }
    require(context["guard"] == expected_guard, "fixed regional witness guard differs")
    decision = regional_decision(
        context, selected, deadline=deadline, reference_context=reference_context
    )
    tick(deadline)
    return {
        **decision,
        "regional_context": context,
        "guard_work": dict(work),
        "original_rows_reconstructed": 1056,
        "regional_foreign_rows_conditioned": 992,
        "regional_contexts_constructed": 1,
        "point_context_constructed": False,
        "original_endpoint_control": {
            "all17_retained": True,
            "witnesses": endpoint,
            "family_disjoint": True,
            "conditional_endpoint_retention_required": False,
        },
    }


def generate(document: dict[str, Any], *, deadline: float) -> dict[str, Any]:
    final, roles, roster, centre, custody, selected, held, frozen = intake(
        document, deadline=deadline
    )
    result = construct(
        final["cells"],
        roles,
        roster,
        centre,
        selected,
        deadline=deadline,
        reference_context=custody["typed_reference_context"],
    )
    for path, (digest, ceiling) in held.items():
        require(finite.digest(path, ceiling, deadline) == digest, "regional inputs changed")
    require(finite.canonical(document) == frozen, "regional descriptor changed")
    tick(deadline)
    return {
        "schema": SCHEMA,
        **guard.scope(),
        **result,
        "accepted_inputs": copy.deepcopy(document),
        "parent_custody": custody,
        "container": guard.standing.CenteredContainer(cases.U, cases.V).record(),
        "matched_owned_point_witness": {
            "centre": list(map(str, centre)),
            "tau": str(guard.TAU),
            "freshly_checked": True,
        },
        "accepted_point_selection_inherited": True,
        "accepted_point_domains_used_as_regional_domains": False,
        "original_parent_proof_replayed": False,
        "point_guard_exclusion_proved": False,
        "point_guard_necessary_domain_restriction_proved": False,
        "mathematical_assurance": (
            "sole-Astra hand composition; fresh exact finite reconstruction"
        ),
        "limits": {
            "half_width": str(HALF_WIDTH),
            "tau": str(guard.TAU),
            "target_owner": TARGET_OWNER,
            "target_indices": list(TARGET_INDICES),
            "guard": guard.constants(),
            "collective": {
                "minkowski_products_cache_misses": collective.MINK_LIMIT,
                "point_in_union_facet_products": collective.POINT_PRODUCTS,
                "per_row_sweep_edges": collective.EDGE_LIMIT,
                "cumulative_sweep_edge_pairs": collective.EDGE_PAIRS,
                "region_vertices": collective.REGION_LIMIT,
            },
            "guard_and_collective_work_counters_separate": True,
            "input_json_bytes": parent.JSON_LIMIT,
            "accepted_collective_bytes": OUTPUT_LIMIT,
            "output_bytes": OUTPUT_LIMIT,
        },
    }


def check(
    document: dict[str, Any], certificate: dict[str, Any], *, deadline: float
) -> dict[str, Any]:
    expected = generate(document, deadline=deadline)
    require(payload(certificate) == expected, "fresh regional reconstruction differs")
    tick(deadline)
    return copy.deepcopy(expected) | {"verification_passed": True}


def failure(exc: Exception) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "status": "incomplete" if isinstance(exc, IncompleteError) else "refused",
        "error": str(exc),
        "criterion_met": False,
        "verification_passed": False,
        "same25_rows_excluded": False,
        "declared_guard_exclusion_proved": False,
        "regional_necessary_domain_restriction_proved": False,
        "point_guard_exclusion_proved": False,
        "point_guard_necessary_domain_restriction_proved": False,
        **guard.scope(),
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
            "producer/kernel/root import in regional checker",
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
        provenance=provenance(
            *(
                Path(cast(str, module.__file__))
                for module in (
                    sys.modules[__name__],
                    collective,
                    collective.prior,
                    guard,
                    parent,
                    finite,
                    cases,
                    guard.standing,
                )
            )
        ),
        invocation={
            "argv": argv if argv is not None else sys.argv[1:],
            "executable": sys.executable,
        },
    )
    text = retained_json.dumps(result, sort_keys=True)
    if len(text.encode()) > OUTPUT_LIMIT or time.monotonic() >= deadline:
        result = failure(IncompleteError("regional output byte or wall ceiling"))
        text = retained_json.dumps(result, sort_keys=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text)
    return (
        0
        if result["status"]
        in ("same25_regional_rows_restricted", "regional_guard_excluded", "criterion_missed")
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
