"""One simultaneous whole-row collective union restriction under an accepted point guard."""

from __future__ import annotations

import argparse
import copy
import math
import sys
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, cast

from devtools import check_n17_two_center_children as prior
from devtools.provenance import provenance
from sqpack import retained_json

parent, finite, cases, guard = prior.parent, prior.finite, prior.cases, prior.guard
require, tick, checked = prior.require, prior.tick, prior.checked
IncompleteError = prior.IncompleteError
Point = prior.Point
SCHEMA = "n17-collective-row-coverage/v1"
DESCRIPTOR_SCHEMA = "n17-collective-row-coverage-context/v1"
ROLES = (*prior.ROLES, "two_child_certificate", "two_child_replay")
OWNERS = prior.OWNERS
OUTPUT_LIMIT = 64 << 20
MINK_LIMIT = 1048576
REGION_LIMIT = 4096
POINT_PRODUCTS = 16000000
EDGE_LIMIT = 8192
EDGE_PAIRS = 8000000
payload = prior.payload
context_geometry = prior.context_geometry


def union_intervals(intervals: list[tuple[Q, Q]]) -> list[tuple[Q, Q]]:
    """Exact union of closed intervals, including zero-width seams."""
    result: list[tuple[Q, Q]] = []
    for lo, hi in sorted(intervals):
        require(lo <= hi, "ordered closed interval required")
        if result and lo <= result[-1][1]:
            result[-1] = (result[-1][0], max(result[-1][1], hi))
        else:
            result.append((lo, hi))
    return result


def length(intervals: list[tuple[Q, Q]]) -> Q:
    total = Q(0)
    for lo, hi in union_intervals(intervals):
        total = checked(total + checked(hi - lo))
    return total


def new_work() -> dict[str, int]:
    return dict.fromkeys(
        (
            "minkowski_vertex_products",
            "region_cache_hits",
            "region_cache_misses",
            "point_in_union_facet_products",
            "sweep_prospective_edge_pairs",
            "sweep_rows",
            "vertex_negative_rows",
            "generated_clipped_vertices",
        ),
        0,
    )


def regions_for(  # noqa: PLR0917
    owner: int,
    lo: Q,
    hi: Q,
    groups: dict[int, list[Point]],
    cache: dict[Any, tuple[int, list[Point]]],
    cores: dict[Any, list[Point]],
    saved: list[dict[str, Any]],
    work: dict[str, int],
    deadline: float,
) -> list[tuple[int, int, list[Point]]]:
    interval = (lo, hi)
    if interval not in cores:
        cores[interval] = parent.core(lo, hi, strict=True, deadline=deadline)
    core = cores[interval]
    result = []
    for other in sorted(groups):
        if other == owner or not groups[other]:
            continue
        key = (interval, tuple(groups[other]))
        if key in cache:
            work["region_cache_hits"] += 1
            index, region = cache[key]
        else:
            tick(deadline)
            work["region_cache_misses"] += 1
            work["minkowski_vertex_products"] += len(groups[other]) * len(core)
            if work["minkowski_vertex_products"] > MINK_LIMIT:
                raise IncompleteError("collective Minkowski vertex product ceiling")
            region = cases.bounded_hull(
                [cases.subtract(p, q) for p in groups[other] for q in core],
                REGION_LIMIT,
                deadline,
            )
            index = len(saved)
            cache[key] = (index, region)
            saved.append(
                {
                    "interval": list(map(str, interval)),
                    "owned_polygon": finite.serial(groups[other]),
                    "strict_core": finite.serial(core),
                    "core_strict_checked": True,
                    "region": finite.serial(region),
                    "source_owner_aliases": [],
                }
            )
        if other not in saved[index]["source_owner_aliases"]:
            saved[index]["source_owner_aliases"].append(other)
        result.append((other, index, region))
    return result


def cover_row(
    domain: list[Point],
    regions: list[tuple[int, int, list[Point]]],
    work: dict[str, int],
    deadline: float,
) -> dict[str, Any]:
    if not domain:
        return {
            "covered": True,
            "primitive": "inherited_empty_domain",
            "negative_vertex": None,
            "sweep_probe": None,
        }
    for point in sorted(domain):
        in_union = False
        for _owner, _index, region in regions:
            tick(deadline)
            work["point_in_union_facet_products"] += max(1, len(cases.edges(region)))
            if work["point_in_union_facet_products"] > POINT_PRODUCTS:
                raise IncompleteError("collective point-in-union facet product ceiling")
            if cases.contains(region, point):
                in_union = True
                break
        if not in_union:
            work["vertex_negative_rows"] += 1
            return {
                "covered": False,
                "primitive": "exact_vertex_outside_closed_union",
                "negative_vertex": list(map(str, point)),
                "sweep_probe": None,
            }
    polygons = [r for _o, _i, r in regions if r]
    edges = sum(len(cases.edges(p)) for p in [domain, *polygons])
    comparisons = edges * (edges - 1) // 2
    work["sweep_prospective_edge_pairs"] += comparisons
    if edges > EDGE_LIMIT or work["sweep_prospective_edge_pairs"] > EDGE_PAIRS:
        raise IncompleteError("collective union sweep edge/pair ceiling")
    work["sweep_rows"] += 1
    tick(deadline)
    if len(domain) <= 2:
        covered = guard.standing.degenerate_covered(domain, polygons)
        primitive, probe = "degenerate_covered", None
    else:
        covered, probe = guard.standing.covered_by_sweep(domain, polygons)
        primitive = "covered_by_sweep"
    tick(deadline)
    if probe is not None:
        checked(probe)
    return {
        "covered": covered,
        "primitive": primitive,
        "negative_vertex": None,
        "sweep_probe": str(probe) if probe is not None else None,
        "polygon_edges": edges,
        "prospective_edge_pairs": comparisons,
    }


def construct(
    rows: dict[int, list[dict[str, Any]]], groups: dict[int, list[Point]], *, deadline: float
) -> dict[str, Any]:
    require(
        set(rows) == set(OWNERS[1:]) and set(groups) == set(OWNERS),
        "complete collective owner roster differs",
    )
    work = new_work()
    cache: dict[Any, tuple[int, list[Point]]] = {}
    cores: dict[Any, list[Point]] = {}
    saved: list[dict[str, Any]] = []
    owners = []
    changed = []
    whole_empty = []
    for owner in sorted(rows):
        result = []
        before = []
        after = []
        for index, row in enumerate(rows[owner]):
            tick(deadline)
            lo, hi = map(finite.rational, row["interval"])
            domain = row["domain"]
            regions = (
                regions_for(owner, lo, hi, groups, cache, cores, saved, work, deadline)
                if domain
                else []
            )
            decision = cover_row(domain, regions, work, deadline)
            if domain:
                before.append((lo, hi))
                if not decision["covered"]:
                    after.append((lo, hi))
            result.append(
                {
                    "row_index": index,
                    "reference": copy.deepcopy(row["reference"]),
                    "interval": list(row["interval"]),
                    "inherited_domain_nonempty": bool(domain),
                    "forbidden_regions": [
                        {"owner": o, "cache_index": i} for o, i, _r in regions
                    ],
                    "domain_retained_unchanged": bool(domain) and not decision["covered"],
                    **decision,
                }
            )
        old, new = union_intervals(before), union_intervals(after)
        lost = checked(length(old) - length(new))
        require(lost >= 0, "collective interval union grew")
        if lost > 0:
            changed.append(owner)
        if not new:
            whole_empty.append(owner)
        owners.append(
            {
                "owner": owner,
                "rows": result,
                "old_closed_interval_union": [list(map(str, p)) for p in old],
                "new_closed_interval_union": [list(map(str, p)) for p in new],
                "lost_length": str(lost),
            }
        )
    tick(deadline)
    return {
        "status": "angle_union_restricted" if changed else "criterion_missed",
        "criterion_met": bool(changed),
        "point_guard_necessary_domain_restriction_proved": bool(changed),
        "point_contradiction_proved": bool(whole_empty),
        "changed_owners": changed,
        "complete_empty_owners": whole_empty,
        "owners": owners,
        "forbidden_region_cache": saved,
        "work": work,
        "all_foreign_rows_accounted": sum(len(r) for r in rows.values()),
        "original_owned_sets_unchanged": True,
        "simultaneous_original_groups_only": True,
        "resource_assurance": {
            "regions_clipped": False,
            "generated_clipped_vertices": 0,
            "point_product_counts": (
                "conservative full-region edge charge for each queried membership"
            ),
            "sweep_edges_include_target_and_all_forbidden_regions": True,
            "sweep_internal_event_probe_caps_enforced": False,
            "unreduced_homogeneous_integer_bit_cap_enforced": False,
            "outer_supervision_required": True,
        },
    }


def intake(document: dict[str, Any], *, deadline: float) -> tuple[Any, ...]:
    require(
        set(document) == {"schema", *(k for role in ROLES for k in (role, role + "_sha256"))}
        and document["schema"] == DESCRIPTOR_SCHEMA,
        "collective descriptor differs",
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
            "collective input byte custody differs",
        )
        held[path] = (document[role + "_sha256"], ceiling)
        require(
            raw == finite.read_json(path, ceiling)[0], "collective input changed while reading"
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
    route, route_replay = inputs["two_child_certificate"], inputs["two_child_replay"]
    expected_route_descriptor = {
        "schema": prior.DESCRIPTOR_SCHEMA,
        **{k: document[k] for role in prior.ROLES for k in (role, role + "_sha256")},
    }
    require(
        route["schema"] == prior.SCHEMA
        and route["status"] == "criterion_missed"
        and route_replay.get("verification_passed") is True
        and payload(route) == payload(route_replay),
        "accepted two-child miss prerequisite differs",
    )
    require(
        route["accepted_inputs"] == expected_route_descriptor
        and route["parent_custody"] == accepted["parent_custody"]
        and route["original_endpoint_control"] == endpoint
        and route["criterion_met"] is False
        and route["point"]["both_children_closed"] is False
        and route["regional_context_started"] is False,
        "two-child route-selection premise identity differs",
    )
    return rows, groups, accepted, held, frozen_descriptor


def generate(document: dict[str, Any], *, deadline: float) -> dict[str, Any]:
    rows, groups, accepted, held, frozen = intake(document, deadline=deadline)
    result = construct(rows, groups, deadline=deadline)
    for path, (sha, ceiling) in held.items():
        require(
            finite.digest(path, ceiling, deadline) == sha,
            "collective input changed during reconstruction",
        )
    require(finite.canonical(document) == frozen, "collective descriptor changed")
    tick(deadline)
    return {
        "schema": SCHEMA,
        **result,
        "accepted_inputs": copy.deepcopy(document),
        "parent_custody": copy.deepcopy(accepted["parent_custody"]),
        "original_endpoint_control": copy.deepcopy(accepted["original_endpoint_control"]),
        "accepted_point_geometry_inherited": True,
        "original_rows_inherited": 1056,
        "new_parent_geometry_replay": False,
        "mathematical_assurance": (
            "sole-Astra hand composition plus fresh collective finite reconstruction"
        ),
        "declared_guard_exclusion_proved": False,
        "point_guard_exclusion_proved": result["point_contradiction_proved"],
        **guard.scope(),
        "limits": {
            "minkowski_products_cache_misses": MINK_LIMIT,
            "point_in_union_facet_products": POINT_PRODUCTS,
            "per_row_sweep_edges": EDGE_LIMIT,
            "cumulative_sweep_edge_pairs": EDGE_PAIRS,
            "region_vertices": REGION_LIMIT,
            "generated_clipped_vertices": 2097152,
            "output_bytes": OUTPUT_LIMIT,
        },
    }


def check(
    document: dict[str, Any], certificate: dict[str, Any], *, deadline: float
) -> dict[str, Any]:
    expected = generate(document, deadline=deadline)
    require(payload(certificate) == expected, "fresh collective reconstruction differs")
    tick(deadline)
    return copy.deepcopy(expected) | {"verification_passed": True}


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
            "producer/kernel/root import in collective checker",
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
            "schema": SCHEMA,
            "status": "incomplete" if isinstance(exc, IncompleteError) else "refused",
            "error": str(exc),
            "criterion_met": False,
            "declared_guard_exclusion_proved": False,
            "point_guard_necessary_domain_restriction_proved": False,
            "point_contradiction_proved": False,
            "point_guard_exclusion_proved": False,
            "verification_passed": False,
            **guard.scope(),
        }
    result.update(
        provenance=provenance(
            Path(__file__),
            Path(cast(str, prior.__file__)),
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
            "error": "collective output byte or wall ceiling",
            "verification_passed": False,
            "declared_guard_exclusion_proved": False,
            "point_guard_necessary_domain_restriction_proved": False,
            "point_contradiction_proved": False,
            "point_guard_exclusion_proved": False,
            **guard.scope(),
        }
        text = retained_json.dumps(result, sort_keys=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text)
    return 0 if result["status"] in ("angle_union_restricted", "criterion_missed") else 1


if __name__ == "__main__":
    raise SystemExit(main())
