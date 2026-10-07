"""Exact two-closed-centre-child reconstruction from an accepted point context.

Accepted guarded geometry is an explicit premise. Only new child geometry is
reconstructed here; the regional branch freshly rebuilds the original context.
"""

from __future__ import annotations

import argparse
import copy
import math
import sys
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, cast

from devtools import check_n17_guard_conditioned_ownership as guard
from devtools.provenance import provenance
from sqpack import retained_json

parent, finite, cases = guard.parent, guard.finite, guard.cases
require, tick, checked = guard.require, guard.tick, guard.checked
IncompleteError = guard.IncompleteError
type Point = tuple[Q, Q]
SCHEMA = "n17-two-center-children/v1"
DESCRIPTOR_SCHEMA = "n17-two-center-children-context/v1"
ROLES = ("guard_descriptor", "guard_certificate", "guard_replay")
CANDIDATES = (5, 7, 8, 9, 11, 12, 13, 14, 18, 21)
OWNERS = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 18, 20, 21)
GENERATED_LIMIT = 2097152
INTERSECTION_PAIRS = 2000000
OUTPUT_LIMIT = 64 << 20


def payload(value: dict[str, Any]) -> dict[str, Any]:
    return {
        k: copy.deepcopy(v)
        for k, v in value.items()
        if k not in {"verification_passed", "provenance", "invocation"}
    }


def parse_polygon(raw: Any, counter: list[int], deadline: float, limit: int) -> list[Point]:
    tick(deadline)
    finite.opaque_polygon(raw)
    if len(raw) > limit:
        raise IncompleteError("two-child polygon vertex ceiling")
    counter[0] += len(raw)
    if counter[0] > parent.INPUT_VERTICES:
        raise IncompleteError("two-child inherited geometry vertex ceiling")
    return finite.polygon(raw)


def context_geometry(
    context: dict[str, Any], reference: dict[str, Any], deadline: float
) -> tuple[dict[int, list[dict[str, Any]]], dict[int, list[Point]]]:
    require(
        context["all_original_rows_checked"] == 1056
        and context["all_foreign_rows_conditioned"] == 992,
        "full row counts differ",
    )
    require(
        set(context["owned_groups"]) == set(map(str, OWNERS))
        and set(context["conditional_rows"]) == set(map(str, OWNERS[1:])),
        "owner roster differs",
    )
    counter = [0]
    groups = {
        o: parse_polygon(context["owned_groups"][str(o)], counter, deadline, guard.OWNED_LIMIT)
        for o in OWNERS
    }
    rows = {}
    for owner in OWNERS[1:]:
        raw = context["conditional_rows"][str(owner)]
        parent.closed_rows(
            [{**row, "outer_domain": [], "residual_polygons": []} for row in raw],
            owner,
            32 if owner == 12 else 64,
            reference,
        )
        rows[owner] = [
            {
                "reference": copy.deepcopy(row["reference"]),
                "interval": list(row["interval"]),
                "domain": parse_polygon(row["domain"], counter, deadline, guard.DOMAIN_LIMIT),
            }
            for row in raw
        ]
        require(any(row["domain"] for row in rows[owner]), "inherited foreign owner empty")
    require(
        bool(groups[0]) and parent.area2(groups[0]) > 0, "positive owner0 strict core required"
    )
    return rows, groups


def box(points: list[Point]) -> tuple[Q, Q, Q, Q]:
    require(bool(points), "nonempty aggregate domain required")
    return (
        min(p[0] for p in points),
        max(p[0] for p in points),
        min(p[1] for p in points),
        max(p[1] for p in points),
    )


def diagonal(points: list[Point]) -> Q:
    if not points:
        return Q(0)
    lo, hi, bottom, top = box(points)
    return checked(checked((hi - lo) ** 2) + checked((top - bottom) ** 2))


def closed_clip(  # noqa: PLR0917
    points: list[Point],
    axis: int,
    midpoint: Q,
    side: int,
    work: dict[str, int],
    deadline: float,
) -> list[Point]:
    require(axis in (0, 1) and side in (-1, 1), "closed child axis/side differs")
    # side=-1 is the closed lower half; side=+1 is the closed upper half.
    sign = -side
    a, b = (Q(sign), Q(0)) if axis == 0 else (Q(0), Q(sign))
    result = cases.clip(points, a, b, checked(sign * midpoint), guard.DOMAIN_LIMIT, deadline)
    work["generated_clip_vertices"] += len(result)
    if work["generated_clip_vertices"] > GENERATED_LIMIT:
        raise IncompleteError("two-child generated clip vertex ceiling")
    return result


def select(
    rows: dict[int, list[dict[str, Any]]],
    groups: dict[int, list[Point]],
    work: dict[str, int],
    deadline: float,
) -> dict[str, Any]:
    require(
        tuple(o for o in OWNERS[1:] if not groups[o]) == CANDIDATES,
        "accepted ten empty-owned candidates differ",
    )
    choices = []
    for owner in CANDIDATES:
        aggregate = [p for row in rows[owner] for p in row["domain"]]
        bounds = box(aggregate)
        for axis in (0, 1):
            midpoint = checked((bounds[2 * axis] + bounds[2 * axis + 1]) / 2)
            child_scores = []
            for side in (-1, 1):
                points = [
                    p
                    for row in rows[owner]
                    for p in closed_clip(row["domain"], axis, midpoint, side, work, deadline)
                ]
                child_scores.append(diagonal(points))
            choices.append((max(child_scores), owner, axis, midpoint, child_scores))
    score, owner, axis, midpoint, children = min(choices, key=lambda x: x[:3])
    return {
        "owner": owner,
        "axis": axis,
        "midpoint": str(midpoint),
        "worst_child_squared_diagonal": str(score),
        "child_squared_diagonals": list(map(str, children)),
        "tie_order": "score,owner,axis(x_before_y)",
        "candidate_count": len(choices),
    }


def children(  # noqa: PLR0917
    rows: dict[int, list[dict[str, Any]]],
    groups: dict[int, list[Point]],
    selection: dict[str, Any],
    work: dict[str, int],
    recovery: dict[str, int],
    deadline: float,
) -> dict[str, Any]:
    owner, axis = selection["owner"], selection["axis"]
    midpoint = finite.rational(selection["midpoint"])
    results = []
    for side in (-1, 1):
        child_rows = [
            {
                **copy.deepcopy(row),
                "domain": closed_clip(row["domain"], axis, midpoint, side, work, deadline),
            }
            for row in rows[owner]
        ]
        aggregate = [p for row in child_rows for p in row["domain"]]
        intrinsic = diagonal(aggregate) < 1 if aggregate else False
        if not aggregate:
            owned = []
            closure = {"kind": "complete_child_owner_empty", "owner": owner}
        else:
            owned = guard.common_owned(child_rows, recovery, deadline)
            closure = None
            for other in sorted(groups):
                if other == owner:
                    continue
                tick(deadline)
                work["intersection_vertex_pairs"] += len(owned) * len(groups[other])
                if work["intersection_vertex_pairs"] > INTERSECTION_PAIRS:
                    raise IncompleteError("two-child intersection vertex-product ceiling")
                overlap = cases.conditional.intersection(owned, groups[other])
                tick(deadline)
                if len(overlap) > guard.INTERSECTION_LIMIT:
                    raise IncompleteError("two-child intersection output ceiling")
                overlap = [(checked(x), checked(y)) for x, y in overlap]
                if overlap:
                    closure = {
                        "kind": "shared_strictly_owned_point",
                        "owners": [owner, other],
                        "intersection": finite.serial(overlap),
                    }
                    break
        results.append(
            {
                "side": side,
                "closed": closure is not None,
                "closure": closure,
                "owned": finite.serial(owned),
                "intrinsic_diagonal_below_one": intrinsic,
                "row_count": len(child_rows),
                "empty_rows": sum(not r["domain"] for r in child_rows),
                "rows": [{**r, "domain": finite.serial(r["domain"])} for r in child_rows],
            }
        )
    return {"both_children_closed": all(r["closed"] for r in results), "children": results}


def regional(
    document: dict[str, Any],
    accepted: dict[str, Any],
    held: dict[Path, tuple[str, int]],
    deadline: float,
) -> dict[str, Any]:
    final, custody, roster, centre = parent.intake(
        copy.deepcopy(document) | {"schema": parent.DESCRIPTOR_SCHEMA}, held, deadline
    )
    require(
        custody["node_sha256"] == accepted["parent_custody"]["node_sha256"]
        and custody["seed_sha256"] == accepted["parent_custody"]["seed_sha256"]
        and custody["compressed_sha256"] == accepted["parent_custody"]["compressed_sha256"],
        "regional original parent identity differs",
    )
    require(
        list(map(str, centre)) == accepted["matched_owned_point_witness"]["centre"],
        "regional fixed witness differs",
    )
    gate = finite.read_json(
        finite.retained_path(document["parent_descriptor"]), parent.JSON_LIMIT
    )[1]
    roles = gate["label_to_owner"]
    counter, original, cache = [0], {}, {}
    for owner in OWNERS:
        raw = final["cells"][str(owner)]
        parent.closed_rows(
            raw, owner, 32 if owner == 12 else 64, custody["typed_reference_context"]
        )
        original[owner] = [parent.row_domain(row, counter, deadline, cache) for row in raw]
        require(any(r["domain"] for r in original[owner]), "original owner empty")
    endpoint = parent.endpoint_control(roster, original, roles, deadline)
    require(len(endpoint) == 17, "all17 regional original endpoint controls required")
    result = guard.condition_context(
        final["cells"],
        original,
        centre,
        counter,
        guard.new_work(),
        deadline,
        half_width=guard.HALF_WIDTH,
    )
    require(result["closure"] is None, "unexpected pre-split regional closure calibration")
    return result


def generate(document: dict[str, Any], *, deadline: float) -> dict[str, Any]:
    require(
        set(document) == {"schema", *(k for role in ROLES for k in (role, role + "_sha256"))}
        and document["schema"] == DESCRIPTOR_SCHEMA,
        "two-child descriptor differs",
    )
    frozen_descriptor = finite.canonical(document)
    held: dict[Path, tuple[str, int]] = {}
    inputs = {}
    for role in ROLES:
        path = finite.retained_path(document[role])
        ceiling = parent.JSON_LIMIT if role == ROLES[0] else OUTPUT_LIMIT
        raw, value = finite.read_json(path, ceiling)
        require(
            finite.digest(path, ceiling, deadline) == document[role + "_sha256"],
            "two-child input byte custody differs",
        )
        held[path] = (document[role + "_sha256"], ceiling)
        require(
            raw == finite.read_json(path, ceiling)[0], "two-child input changed while reading"
        )
        inputs[role] = value
    accepted, replay = inputs["guard_certificate"], inputs["guard_replay"]
    require(
        accepted["schema"] == guard.SCHEMA
        and accepted["status"] == "criterion_missed"
        and replay.get("verification_passed") is True
        and payload(accepted) == payload(replay),
        "accepted guard complete-miss fresh premise differs",
    )
    require(
        accepted["accepted_inputs"] == inputs["guard_descriptor"]
        and accepted["constants"] == guard.constants()
        and accepted["container"] == guard.standing.CenteredContainer(cases.U, cases.V).record()
        and accepted["criterion_met"] is False
        and accepted["point_guard_exclusion_proved"] is False
        and accepted["regional_context_started"] is False
        and len(accepted["contexts"]) == 1
        and accepted["contexts"][0]["guard"]["half_width"] == "0"
        and accepted["closure"] is None
        and accepted["point_closure"] is None,
        "accepted point-only nonclosed premise differs",
    )
    endpoint = accepted["original_endpoint_control"]
    witness = accepted["matched_owned_point_witness"]
    require(
        witness["tau"] == str(guard.TAU) and len(witness["centre"]) == 2,
        "matched point witness shape differs",
    )
    centre = list(map(finite.rational, witness["centre"]))
    expected_guard = {
        "half_width": "0",
        "angle_interval": [str(guard.TAU)] * 2,
        "centre_box": [[str(x), str(x)] for x in centre],
    }
    require(
        accepted["contexts"][0]["guard"] == expected_guard,
        "accepted point context differs from matched witness",
    )
    require(
        endpoint["all17_retained"] is True
        and endpoint["family_disjoint"] is True
        and len(endpoint["witnesses"]) == 17
        and {w["label"] for w in endpoint["witnesses"]} == set(range(1, 18))
        and {w["owner"] for w in endpoint["witnesses"]} == set(OWNERS),
        "original endpoint premise differs",
    )
    reference = accepted["parent_custody"]["typed_reference_context"]
    require(
        accepted["parent_custody"]["steps"] == 16
        and len(reference["step_owners"]) == 16
        and set(reference["step_owners"]) == set(OWNERS) - {12},
        "parent step roster differs",
    )
    rows, groups = context_geometry(accepted["contexts"][0], reference, deadline)
    work = {"generated_clip_vertices": 0, "intersection_vertex_pairs": 0}
    recovery = guard.new_work()
    selection = select(rows, groups, work, deadline)
    point = children(rows, groups, selection, work, recovery, deadline)
    region = None
    try:
        if point["both_children_closed"]:
            context = regional(inputs["guard_descriptor"], accepted, held, deadline)
            region_rows, region_groups = context_geometry(context, reference, deadline)
            region = children(region_rows, region_groups, selection, work, recovery, deadline)
            region["original_conditional_work"] = context["work"]
        for path, (digest, ceiling) in held.items():
            require(
                finite.digest(path, ceiling, deadline) == digest, "two-child inputs changed"
            )
        require(finite.canonical(document) == frozen_descriptor, "two-child descriptor changed")
        tick(deadline)
    except IncompleteError as exc:
        raise guard.ContextIncompleteError(
            str(exc),
            {
                "selection_candidate": selection,
                "completed_point_children_candidate": point,
                "point_guard_exclusion_candidate": point["both_children_closed"],
                "new_child_work": work,
                "new_recovery_work": recovery,
                "partial_custody_recheck_complete": False,
            },
        ) from exc
    proved = bool(region and region["both_children_closed"])
    return {
        "schema": SCHEMA,
        "status": "closed_region_exclusion"
        if proved
        else "fixed_witness_only"
        if point["both_children_closed"]
        else "criterion_missed",
        "criterion_met": proved,
        "declared_guard_exclusion_proved": proved,
        "point_guard_exclusion_proved": point["both_children_closed"],
        "selection": selection,
        "point": point,
        "regional": region,
        "regional_context_started": region is not None,
        "regional_skip_reason": None
        if region
        else "complete_fixed_split_point_miss_monotonic_inclusion",
        "accepted_inputs": copy.deepcopy(document),
        "parent_custody": copy.deepcopy(accepted["parent_custody"]),
        "original_endpoint_control": copy.deepcopy(endpoint),
        "original_rows_inherited": 1056,
        "foreign_rows_reconstructed_from_accepted_domains": 992,
        "new_child_work": work,
        "new_recovery_work": recovery,
        "mathematical_assurance": (
            "sole-Astra hand composition plus fresh finite child reconstruction"
        ),
        "accepted_point_geometry_inherited": True,
        "fresh_point_parent_replay": False,
        **guard.scope(),
        "regional_original_domains_reconstructed": region is not None,
        "limits": {
            "new_generated_clip_vertices": GENERATED_LIMIT,
            "new_intersection_vertex_pairs": INTERSECTION_PAIRS,
            "new_recovery_support_products": guard.RECOVERY_SUPPORT_LIMIT,
            "new_strict_vertex_pairs": guard.STRICT_PAIR_LIMIT,
            "new_strict_quadratic_checks": guard.STRICT_CHECK_LIMIT,
            "inherited_guard_work_separate": guard.constants(),
            "output_bytes": OUTPUT_LIMIT,
        },
    }


def check(
    document: dict[str, Any], certificate: dict[str, Any], *, deadline: float
) -> dict[str, Any]:
    expected = generate(document, deadline=deadline)
    require(payload(certificate) == expected, "fresh two-child reconstruction differs")
    tick(deadline)
    return copy.deepcopy(expected) | {"verification_passed": True}


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
                n == p or n.startswith(p + ".") for n in sys.modules for p in finite.FORBIDDEN
            ),
            "producer/kernel/root import in two-child checker",
        )
        raw, doc = finite.read_json(args.descriptor, parent.JSON_LIMIT)
        if args.certificate:
            saved, certificate = finite.read_json(args.certificate, OUTPUT_LIMIT)
            result = check(doc, certificate, deadline=deadline)
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
        result = {
            **(exc.observations if isinstance(exc, guard.ContextIncompleteError) else {}),
            "schema": SCHEMA,
            "status": "incomplete" if isinstance(exc, IncompleteError) else "refused",
            "error": str(exc),
            "criterion_met": False,
            "declared_guard_exclusion_proved": False,
            "point_guard_exclusion_proved": False,
            "verification_passed": False,
            **guard.scope(),
        }
    result.update(
        provenance=provenance(
            Path(__file__),
            Path(cast(str, guard.__file__)),
            Path(cast(str, parent.__file__)),
            Path(cast(str, finite.__file__)),
            Path(cast(str, cases.__file__)),
            Path(cast(str, guard.standing.__file__)),
        ),
        invocation={
            "argv": argv if argv is not None else sys.argv[1:],
            "executable": sys.executable,
        },
    )
    text = retained_json.dumps(result, sort_keys=True)
    if len(text.encode()) > OUTPUT_LIMIT or time.monotonic() >= deadline:
        result = {
            "point_guard_exclusion_candidate": result.get(
                "point_guard_exclusion_proved",
                result.get("point_guard_exclusion_candidate", False),
            ),
            "selection_candidate": result.get("selection", result.get("selection_candidate")),
            "schema": SCHEMA,
            "status": "incomplete",
            "criterion_met": False,
            "error": "two-child output byte or wall ceiling",
            "verification_passed": False,
            "declared_guard_exclusion_proved": False,
            "point_guard_exclusion_proved": False,
            **guard.scope(),
        }
        text = retained_json.dumps(result, sort_keys=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text)
    return (
        0
        if result["status"]
        in ("closed_region_exclusion", "criterion_missed", "fixed_witness_only")
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
