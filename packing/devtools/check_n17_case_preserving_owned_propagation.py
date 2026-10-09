"""One simultaneous owned recovery/pass within each accepted closed centre case."""

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

previous = prior.previous
collective, guard, parent, finite, cases = (
    prior.collective,
    prior.guard,
    prior.parent,
    prior.finite,
    prior.cases,
)
require, tick, checked = prior.require, prior.tick, prior.checked
IncompleteError = prior.IncompleteError
type Point = tuple[Q, Q]
type Plane = tuple[Q, Q, Q]
OWNERS = prior.OWNERS
SCHEMA = "n17-case-preserving-owned-propagation/v1"
DESCRIPTOR_SCHEMA = "n17-case-preserving-owned-propagation-context/v1"
ROLES = ("cases_descriptor", "cases_certificate", "cases_replay")
OUTPUT_LIMIT = 64 << 20
CLIP_VERTICES = prior.CLIP_VERTICES
INTERSECTION_PRODUCTS = 4000000
RECOVERY_SUPPORT_LIMIT = 32000000
STRICT_PAIR_LIMIT = 4000000
STRICT_CHECK_LIMIT = 16000000
MARGIN = guard.MARGIN
OWNED_LIMIT = guard.OWNED_LIMIT
sat = guard.sat
payload = prior.payload
scope = prior.scope


def ownership_planes(
    centres: list[Point], lo: Q, hi: Q, work: dict[str, int], deadline: float
) -> list[Plane]:
    require(bool(centres) and 0 <= lo <= hi <= 1, "nonempty ownership domain required")
    cl, sl = finite.trig(lo)
    ch, sh = finite.trig(hi)
    result = []
    for c in (ch, cl):
        for s in (sl, sh):
            for sign in (-1, 1):
                for normal in ((sign * c, sign * s), (-sign * s, sign * c)):
                    tick(deadline)
                    work["minimum_support_products"] += len(centres)
                    if work["minimum_support_products"] > RECOVERY_SUPPORT_LIMIT:
                        raise IncompleteError("guard-owned recovery MIN-support ceiling")
                    minimum = min(finite.dot(point, normal) for point in centres)
                    result.append((normal[0], normal[1], checked(Q(1, 2) - MARGIN + minimum)))
    return result


def strictly_owned(  # noqa: PLR0917
    points: list[Point],
    centres: list[Point],
    lo: Q,
    hi: Q,
    work: dict[str, int],
    deadline: float,
) -> bool:
    """Fresh strict closed-arc checks for every point/centre product vertex."""
    require(0 <= lo <= hi <= 1, "strict ownership closed interval differs")
    for point in points:
        for centre in centres:
            work["strict_vertex_pairs"] += 1
            if work["strict_vertex_pairs"] > STRICT_PAIR_LIMIT:
                raise IncompleteError("guard-owned strict vertex-pair ceiling")
            x, y = cases.subtract(point, centre)
            for sign in (-1, 1):
                polynomials = (
                    (
                        checked(Q(1, 2) - sign * x),
                        checked(-2 * sign * y),
                        checked(Q(1, 2) + sign * x),
                    ),
                    (
                        checked(Q(1, 2) - sign * y),
                        checked(2 * sign * x),
                        checked(Q(1, 2) + sign * y),
                    ),
                )
                for polynomial in polynomials:
                    tick(deadline)
                    work["strict_quadratic_checks"] += 1
                    if work["strict_quadratic_checks"] > STRICT_CHECK_LIMIT:
                        raise IncompleteError("guard-owned strict quadratic check ceiling")
                    if sat.minimum(polynomial, lo, hi)[0] <= 0:
                        return False
    tick(deadline)
    return True


def common_owned(
    rows: list[dict[str, Any]], work: dict[str, int], deadline: float
) -> list[Point]:
    """Intersect ownership implications across every surviving closed row."""
    result = [(Q(0), Q(0)), (cases.U, Q(0)), (cases.U, cases.U), (Q(0), cases.U)]
    live = 0
    for row in rows:
        tick(deadline)
        if not row["domain"]:
            continue
        live += 1
        lo, hi = map(finite.rational, row["interval"])
        for a, b, rhs in ownership_planes(row["domain"], lo, hi, work, deadline):
            result = cases.clip(result, a, b, rhs, OWNED_LIMIT, deadline)
    require(live > 0, "empty owner cover requires a distinct conditional closure")
    for row in rows:
        if row["domain"]:
            lo, hi = map(finite.rational, row["interval"])
            require(
                strictly_owned(result, row["domain"], lo, hi, work, deadline),
                "fresh recovered common strict ownership fails",
            )
    return result


def apply_case_decisions(
    rows: dict[int, list[dict[str, Any]]], coverage: dict[str, Any], deadline: float
) -> dict[int, list[dict[str, Any]]]:
    require(
        coverage["all_foreign_rows_accounted"] == 992 and len(coverage["owners"]) == 16,
        "full992 accepted case roster required",
    )
    result = copy.deepcopy(rows)
    for owner, entry in zip(OWNERS[1:], coverage["owners"], strict=True):
        require(
            entry["owner"] == owner and len(entry["rows"]) == len(rows[owner]),
            "case owner/row roster differs",
        )
        for i, (row, decision) in enumerate(zip(rows[owner], entry["rows"], strict=True)):
            tick(deadline)
            require(
                type(decision["row_index"]) is int
                and decision["row_index"] == i
                and decision["reference"] == row["reference"]
                and decision["interval"] == row["interval"]
                and type(decision["covered"]) is bool
                and decision["inherited_domain_nonempty"] is bool(row["domain"])
                and decision["domain_retained_unchanged"]
                is (bool(row["domain"]) and not decision["covered"]),
                "case decision identity differs",
            )
            if decision["covered"]:
                result[owner][i]["domain"] = []
        require(
            prior.interval_union(rows[owner]) == entry["old_closed_interval_union"]
            and prior.interval_union(result[owner]) == entry["new_closed_interval_union"],
            "case decision closed union differs",
        )
        before = [tuple(map(finite.rational, x)) for x in entry["old_closed_interval_union"]]
        after = [tuple(map(finite.rational, x)) for x in entry["new_closed_interval_union"]]
        require(
            str(checked(collective.length(before) - collective.length(after)))
            == entry["lost_length"],
            "case decision loss differs",
        )
    return result


def flags(rows: dict[int, list[dict[str, Any]]], side: int, *, closed: bool) -> dict[str, Any]:
    return {
        "side": side,
        "closed": closed,
        "surviving_rows": {
            str(o): [
                {
                    "row_index": i,
                    "reference": copy.deepcopy(r["reference"]),
                    "interval": list(r["interval"]),
                    "live": bool(r["domain"]) and not closed,
                }
                for i, r in enumerate(rows[o])
            ]
            for o in OWNERS[1:]
        },
    }


def intake(document: Any, deadline: float) -> tuple[Any, ...]:
    require(
        type(document) is dict
        and document.get("schema") == DESCRIPTOR_SCHEMA
        and set(document) == {"schema", *(k for r in ROLES for k in (r, r + "_sha256"))},
        "case propagation descriptor differs",
    )
    held: dict[Path, tuple[str, int]] = {}
    values = {
        r: previous.read_bound(
            r,
            document,
            held,
            deadline,
            parent.JSON_LIMIT if r.endswith("descriptor") else OUTPUT_LIMIT,
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
        and accepted["survivors_unioned_across_cases"] is True
        and accepted["no_sequential_feedback"] is True
        and accepted["base_foreign_rows_accounted"] == 992
        and accepted["original_rows_inherited"] == 1056
        and accepted["regional_necessary_domain_restriction_proved"] is True
        and all(
            accepted.get(k) is False
            for k in scope()
            if k != "regional_necessary_domain_restriction_proved"
        ),
        "accepted two-open-case positive premise differs",
    )
    base, groups, original, transitive = prior.intake(values["cases_descriptor"], deadline)
    for path, recorded_identity in transitive.items():
        identity = recorded_identity
        if path in held:
            require(held[path][0] == identity[0], "conflicting case custody aliases")
            identity = (identity[0], min(identity[1], held[path][1]))
        held[path] = identity
    require(
        all(
            accepted[k] == original[k]
            for k in ("guard", "container", "parent_custody", "original_endpoint_control")
        )
        and accepted["fixed_selection"]
        == {"owner": 18, "axis": 0, "midpoint": str(prior.MIDPOINT)},
        "accepted case parent/context differs",
    )
    require(
        [c["side"] for c in accepted["children"]] == [-1, 1], "both accepted sides required"
    )
    effective = []
    work = {"generated_clip_vertices": 0}
    inherited_counter = [
        sum(len(r["domain"]) for entries in base.values() for r in entries)
        + sum(map(len, groups.values()))
    ]
    for child in accepted["children"]:
        require(
            child["closed"] is False
            and child["closure"] is None
            and child["other_owned_groups_unchanged"] is True
            and child["collective_rows_accounted"] == 992
            and child["collective"]["case_groups_frozen_during_collective_pass"] is True,
            "open complete case premise differs",
        )
        side = child["side"]
        require(
            child["halfplane"]
            == {
                "axis": 0,
                "relation": "<=" if side == -1 else ">=",
                "midpoint": str(prior.MIDPOINT),
            },
            "frozen closed cut differs",
        )
        rows = copy.deepcopy(base)
        rows[18] = prior.clip_rows(rows[18], side, work, deadline)
        saved = [
            {
                "row_index": i,
                "reference": copy.deepcopy(r["reference"]),
                "interval": list(r["interval"]),
                "domain": finite.serial(r["domain"]),
            }
            for i, r in enumerate(rows[18])
        ]
        require(
            saved == child["selected_owner_clipped_rows"], "accepted halfspace domains differ"
        )
        prior.selection_tool.parse_polygon(
            child["selected_owned_group"], inherited_counter, deadline, OWNED_LIMIT
        )
        rows = apply_case_decisions(rows, child["collective"], deadline)
        require(
            child["collective"]["complete_empty_owners"] == []
            and all(any(r["domain"] for r in rows[o]) for o in OWNERS[1:]),
            "accepted open case has an empty owner cover",
        )
        require(
            flags(rows, side, closed=False)["surviving_rows"] == child["surviving_rows"],
            "accepted case survivor flags differ",
        )
        effective.append(rows)
    require(
        prior.combine(base, accepted["children"], deadline)
        == accepted["combined_restrictions"],
        "accepted combined baseline differs",
    )
    return base, effective, groups, accepted, held, work


def shared_intersection(
    groups: dict[int, list[Point]], work: dict[str, int], deadline: float
) -> dict[str, Any] | None:
    for i, owner in enumerate(OWNERS):
        for other in OWNERS[i + 1 :]:
            if not groups[owner] or not groups[other]:
                continue
            tick(deadline)
            work["intersection_vertex_pairs"] += len(groups[owner]) * len(groups[other])
            if work["intersection_vertex_pairs"] > INTERSECTION_PRODUCTS:
                raise IncompleteError("shared owned intersection product ceiling")
            overlap = cases.conditional.intersection(groups[owner], groups[other])
            tick(deadline)
            if len(overlap) > guard.INTERSECTION_LIMIT:
                raise IncompleteError("shared owned intersection output ceiling")
            if overlap:
                return {
                    "kind": "shared_strictly_owned_point",
                    "owners": [owner, other],
                    "intersection": finite.serial(
                        [(checked(x), checked(y)) for x, y in overlap]
                    ),
                }
    return None


def case_result(
    rows: dict[int, list[dict[str, Any]]],
    groups: dict[int, list[Point]],
    side: int,
    work: dict[str, int],
    deadline: float,
) -> dict[str, Any]:
    snapshot = copy.deepcopy(rows)
    recovered = {0: list(groups[0])}
    empty = [o for o in OWNERS[1:] if not any(r["domain"] for r in rows[o])]
    closure = {"kind": "accepted_case_owner_cover_empty", "owners": empty} if empty else None
    if closure is None:
        for owner in OWNERS[1:]:
            recovered[owner] = common_owned(rows[owner], work, deadline)
            require(len(recovered[owner]) <= OWNED_LIMIT, "recovered group too large")
        closure = shared_intersection(recovered, work, deadline)
    coverage = None
    surviving = copy.deepcopy(rows)
    if closure is None:
        frozen = copy.deepcopy(recovered)
        coverage = collective.construct(rows, recovered, deadline=deadline)
        require(recovered == frozen and rows == snapshot, "case simultaneous snapshot mutated")
        surviving = apply_case_decisions(rows, coverage, deadline)
        if coverage["complete_empty_owners"]:
            closure = {
                "kind": "collective_owner_cover_empty",
                "owners": list(coverage["complete_empty_owners"]),
                "closed_cover_accounted": 992,
            }
        for k in (
            "point_guard_necessary_domain_restriction_proved",
            "point_contradiction_proved",
            "original_owned_sets_unchanged",
            "simultaneous_original_groups_only",
        ):
            coverage.pop(k)
        coverage["case_groups_frozen_during_collective_pass"] = True
    require(
        rows == snapshot and recovered[0] == groups[0], "case recovery changed frozen rows/core"
    )
    tick(deadline)
    return {
        **flags(surviving, side, closed=closure is not None),
        "closure": closure,
        "recovered_owned_groups": {str(o): finite.serial(p) for o, p in recovered.items()},
        "all16_recoveries_completed": len(recovered) == 17,
        "owner0_core_unchanged": True,
        "collective": coverage,
        "collective_rows_accounted": 992 if coverage is not None else 0,
    }


def compare_combined(
    base: dict[int, list[dict[str, Any]]],
    baseline: list[dict[str, Any]],
    children: list[dict[str, Any]],
    deadline: float,
) -> list[dict[str, Any]]:
    result = prior.combine(base, children, deadline)
    require(
        [r["owner"] for r in baseline] == list(OWNERS[1:]),
        "combined baseline owner roster differs",
    )
    for old, new in zip(baseline, result, strict=True):
        before = [
            tuple(map(finite.rational, p))
            for p in old["combined_surviving_closed_interval_union"]
        ]
        after = [
            tuple(map(finite.rational, p))
            for p in new["combined_surviving_closed_interval_union"]
        ]
        require(
            all(any(a <= lo <= hi <= b for a, b in before) for lo, hi in after),
            "new survivors escaped accepted combined baseline",
        )
        new["baseline_closed_interval_union"] = copy.deepcopy(
            old["combined_surviving_closed_interval_union"]
        )
        new["additional_lost_length"] = str(
            checked(collective.length(before) - collective.length(after))
        )
    return result


def construct(
    base: dict[int, list[dict[str, Any]]],
    effective: list[dict[int, list[dict[str, Any]]]],
    groups: dict[int, list[Point]],
    baseline: list[dict[str, Any]],
    *,
    deadline: float,
) -> dict[str, Any]:
    require(
        len(effective) == 2
        and set(groups) == set(OWNERS)
        and bool(groups[0])
        and len(groups[0]) <= guard.OWNER0_LIMIT
        and parent.area2(groups[0]) > 0
        and all(
            set(rows) == set(OWNERS[1:]) and sum(map(len, rows.values())) == 992
            for rows in effective
        ),
        "complete case geometry/core required",
    )
    work = guard.new_work()
    children = []
    try:
        for side, rows in zip((-1, 1), effective, strict=True):
            children.append(case_result(rows, groups, side, work, deadline))
        unions = compare_combined(base, baseline, children, deadline)
    except IncompleteError as exc:
        raise guard.ContextIncompleteError(
            str(exc), {"finished_children_candidates": children, "recovery_work": work}
        ) from exc
    cumulative = {
        k: sum(c["collective"]["work"][k] for c in children if c["collective"] is not None)
        for k in collective.new_work()
    }
    require(
        cumulative["minkowski_vertex_products"] <= 2 * collective.MINK_LIMIT
        and cumulative["point_in_union_facet_products"] <= 2 * collective.POINT_PRODUCTS
        and cumulative["sweep_prospective_edge_pairs"] <= 2 * collective.EDGE_PAIRS,
        "aggregate collective work exceeded per-case bounds",
    )
    changed = [r["owner"] for r in unions if finite.rational(r["additional_lost_length"]) > 0]
    both = all(c["closed"] for c in children)
    tick(deadline)
    return {
        "status": "regional_guard_excluded"
        if both
        else "additional_angle_union_restricted"
        if changed
        else "criterion_missed",
        "criterion_met": bool(both or changed),
        **scope(progress=bool(changed), contradiction=both),
        "both_children_closed": both,
        "closed_case_count": sum(c["closed"] for c in children),
        "children": children,
        "combined_restrictions": unions,
        "accepted_combined_baseline": copy.deepcopy(baseline),
        "changed_owners": changed,
        "recovery_work": work,
        "cumulative_collective_work": cumulative,
        "survivors_unioned_across_cases": True,
        "all16_recoveries_before_each_collective_pass": True,
        "no_sequential_feedback": True,
        "base_foreign_rows_accounted": 992,
    }


def generate(document: dict[str, Any], *, deadline: float) -> dict[str, Any]:
    frozen = finite.canonical(document)
    base, effective, groups, accepted, held, clip_work = intake(document, deadline)
    result = construct(
        base, effective, groups, accepted["combined_restrictions"], deadline=deadline
    )
    for path, (sha, ceiling) in held.items():
        require(
            finite.digest(path, ceiling, deadline) == sha, "case propagation premise changed"
        )
    require(finite.canonical(document) == frozen, "case propagation descriptor changed")
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
        "base_geometry_parsed_once": True,
        "base_proof_inherited": True,
        "accepted_cases_arithmetic_replayed": False,
        "original_parent_proof_replayed": False,
        "original17_endpoint_retention_inherited": True,
        "selection_point_geometry_used": False,
        "tiny_guard_geometry_used": False,
        "halfspace_reconstruction_work": clip_work,
        "mathematical_assurance": (
            "sole-Astra hand composition and fresh case-preserving finite reconstruction"
        ),
        "limits": {
            "output_bytes": OUTPUT_LIMIT,
            "geometry_bits": finite.BIT_LIMIT,
            "inherited_geometry_vertices": parent.INPUT_VERTICES,
            "row_domain_vertices": guard.DOMAIN_LIMIT,
            "owner0_vertices": guard.OWNER0_LIMIT,
            "recovered_group_vertices": OWNED_LIMIT,
            "recovery_support_products": RECOVERY_SUPPORT_LIMIT,
            "strict_vertex_pairs": STRICT_PAIR_LIMIT,
            "strict_quadratic_checks": STRICT_CHECK_LIMIT,
            "intersection_products": INTERSECTION_PRODUCTS,
            "intersection_output_vertices": guard.INTERSECTION_LIMIT,
            "generated_halfspace_clip_vertices": CLIP_VERTICES,
            "per_case_collective_minkowski_products": collective.MINK_LIMIT,
            "per_case_collective_point_products": collective.POINT_PRODUCTS,
            "per_case_collective_sweep_pairs": collective.EDGE_PAIRS,
            "cumulative_collective_minkowski_products": 2 * collective.MINK_LIMIT,
            "cumulative_collective_point_products": 2 * collective.POINT_PRODUCTS,
            "cumulative_collective_sweep_pairs": 2 * collective.EDGE_PAIRS,
        },
        "resource_assurance": {
            "outer_supervision_required": True,
            "sweep_internal_event_caps_enforced": False,
            "unreduced_integer_products_individually_bounded": False,
        },
    }


def check(
    document: dict[str, Any], certificate: dict[str, Any], *, deadline: float
) -> dict[str, Any]:
    result = generate(document, deadline=deadline)
    require(payload(certificate) == result, "fresh case-preserving reconstruction differs")
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
            "producer/kernel/root import in case-preserving checker",
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
            Path(prior.__file__),
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
        result = failure(IncompleteError("case-preserving output byte or wall ceiling"))
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
