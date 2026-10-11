"""Exact union coverage by pooled foreign owned hulls in a closed chart guard.

Full original-parent replay is an accepted premise. This producer-free finite
instrument reconstructs strict cores and forbidden-region unions, and proves
only the declared conditional closed-angle exclusion when every piece is covered.
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

from devtools import probe_n17_conditional_center_cases as cases
from devtools.provenance import provenance
from sqpack import retained_json

SCHEMA = "n17-pooled-forbidden-cover/v1"
CORE_LIMIT = 32
MINKOWSKI_LIMIT = 256
CLIPPED_LIMIT = 384
PIECE_LIMIT = 256
PAIR_LIMIT = 65536
EDGE_LIMIT = 2048
EDGE_PAIR_LIMIT = 2100000
OUTPUT_LIMIT = 64 << 20
Point = cases.Point
IncompleteError = cases.IncompleteError
require, tick, checked = cases.require, cases.tick, cases.checked
standing, finite = cases.conditional.standing, cases.finite


def core(lo: Q, hi: Q, deadline: float) -> list[Point]:
    require(
        cases.INTERVAL[0] <= lo <= hi <= cases.INTERVAL[1], "closed core interval escapes guard"
    )
    rows = [{"interval": (lo, hi), "pieces": [[(Q(0), Q(0))]]}]
    planes = list(cases.ownership_planes(rows, deadline))
    polygon = [(Q(-1), Q(-1)), (Q(1), Q(-1)), (Q(1), Q(1)), (Q(-1), Q(1))]
    for a, b, rhs in planes:
        polygon = cases.clip(polygon, a, b, rhs, CORE_LIMIT, deadline)
    require(
        len(polygon) >= 3
        and cases.contains(polygon, (Q(0), Q(0)))
        and all(finite.dot(p, (a, b)) <= rhs for p in polygon for a, b, rhs in planes),
        "strict core construction failed",
    )
    require(standing.core_strict(polygon, lo, hi), "independent closed-arc core check failed")
    tick(deadline)
    return polygon


def foreign_regions(
    groups: dict[int, list[Point]],
    square_core: list[Point],
    counter: list[int],
    deadline: float,
) -> dict[int, list[Point]]:
    regions = {}
    for owner in sorted(groups):
        if owner == 0:
            continue
        count = len(groups[owner]) * len(square_core)
        counter[0] += count
        if counter[0] > PAIR_LIMIT:
            raise IncompleteError("forbidden-cover generated pair ceiling")
        points = []
        for point in groups[owner]:
            for body in square_core:
                tick(deadline)
                points.append(cases.subtract(point, body))
        regions[owner] = cases.bounded_hull(points, MINKOWSKI_LIMIT, deadline)
    return regions


def cover_piece(
    domain: list[Point], regions: dict[int, list[Point]], deadline: float
) -> dict[str, Any]:
    clipped = {}
    for owner, region in regions.items():
        polygon = cases.intersection(domain, region, deadline)
        if len(polygon) > CLIPPED_LIMIT:
            raise IncompleteError("forbidden-cover clipped region ceiling")
        clipped[owner] = polygon
    every = list(clipped.values())
    edges = sum(len(cases.edges(p)) for p in [domain, *every])
    comparisons = edges * (edges - 1) // 2
    if edges > EDGE_LIMIT or comparisons > EDGE_PAIR_LIMIT:
        raise IncompleteError("forbidden-cover sweep edge/pair ceiling")
    tick(deadline)
    probe = None
    if not domain:
        covered, primitive = True, "empty_piece"
    elif len(domain) <= 2:
        covered, primitive = standing.degenerate_covered(domain, every), "degenerate_covered"
    else:
        covered, probe = standing.covered_by_sweep(domain, every)
        primitive = "covered_by_sweep"
    tick(deadline)
    if probe is not None:
        checked(probe)
    return {
        "covered": covered,
        "primitive": primitive,
        "uncovered_probe": str(probe) if probe is not None else None,
        "regions": {str(o): finite.serial(p) for o, p in clipped.items()},
        "polygon_edges": edges,
        "prospective_edge_pairs": comparisons,
        "internal_events": None,
        "internal_probes": None,
        "event_probe_caps_enforced": False,
    }


def construct(
    rows: list[Any],
    raw_pools: dict[str, Any],
    raw_ordinary: dict[str, Any],
    *,
    deadline: float,
    input_vertex_offset: int = 0,
) -> dict[str, Any]:
    require(
        len(raw_pools) == 17 and set(raw_pools) == set(raw_ordinary) and "0" in raw_pools,
        "complete matched foreign owner roster",
    )
    counter = [input_vertex_offset]
    pools = {int(o): cases.parse_polygon(p, counter, deadline) for o, p in raw_pools.items()}
    ordinary = {
        int(o): cases.parse_polygon(p, counter, deadline) for o, p in raw_ordinary.items()
    }
    for owner, pool in pools.items():
        require(
            all(cases.contains(pool, point) for point in ordinary[owner]),
            "ordinary final hull not contained in pool",
        )
    pieces = cases.necessary_pieces(rows, deadline, counter)
    nonempty = sum(len(r["pieces"]) for r in pieces)
    if nonempty > PIECE_LIMIT:
        raise IncompleteError("forbidden-cover necessary piece ceiling")
    results = []
    pooled_all = ordinary_all = True
    for row in pieces:
        if not row["pieces"]:
            results.append(
                {
                    "row_index": row["row_index"],
                    "reference": row["reference"],
                    "interval": list(map(str, row["interval"])),
                    "strict_core": [],
                    "core_strict_checked": None,
                    "generated_pairs_both_controls": 0,
                    "pieces": [],
                    "status": "empty_necessary_row",
                }
            )
            continue
        lo, hi = row["interval"]
        square_core = core(lo, hi, deadline)
        pair_count = [0]
        old_regions = foreign_regions(ordinary, square_core, pair_count, deadline)
        pooled_regions = foreign_regions(pools, square_core, pair_count, deadline)
        found = []
        for index, domain in enumerate(row["pieces"]):
            old = cover_piece(domain, old_regions, deadline)
            new = cover_piece(domain, pooled_regions, deadline)
            require(
                not old["covered"] or new["covered"],
                "ordinary-covered pooled-uncovered calibration",
            )
            ordinary_all = ordinary_all and old["covered"]
            pooled_all = pooled_all and new["covered"]
            found.append(
                {
                    "piece_index": index,
                    "domain": finite.serial(domain),
                    "ordinary": old,
                    "pooled": new,
                }
            )
        results.append(
            {
                "row_index": row["row_index"],
                "reference": row["reference"],
                "interval": list(map(str, row["interval"])),
                "strict_core": finite.serial(square_core),
                "core_strict_checked": True,
                "generated_pairs_both_controls": pair_count[0],
                "pieces": found,
            }
        )
    tick(deadline)
    return {
        "rows": results,
        "ordinary_final_coverage": ordinary_all,
        "pooled_coverage": pooled_all,
        "compression_information_recovered": pooled_all and not ordinary_all,
        "conditional_I_exclusion_proved": pooled_all,
        "criterion_met": pooled_all,
        "status": "closed_I_exclusion" if pooled_all else "criterion_missed",
        "input_vertices": counter[0],
        "nonempty_necessary_pieces": nonempty,
        "relaxation_gap_is_feasible_packing": False,
    }


def generate(document: dict[str, Any], *, deadline: float) -> dict[str, Any]:
    frozen = finite.canonical(document)
    held: dict[Path, tuple[str, int]] = {}
    state, custody, offset, _selected = cases.intake(document, held, deadline)
    pool = custody["proof_pool"]
    result = construct(
        state["cells"]["0"],
        state["groups"],
        pool["unpooled_conditional_groups"],
        deadline=deadline,
        input_vertex_offset=offset,
    )
    for path, (expected, ceiling) in held.items():
        require(
            finite.digest(path, ceiling, deadline) == expected, "forbidden-cover inputs changed"
        )
    require(finite.canonical(document) == frozen, "forbidden-cover descriptor changed")
    return {
        "schema": SCHEMA,
        "guard": copy.deepcopy(cases.GUARD),
        "container": standing.CenteredContainer(cases.U, cases.V).record(),
        "custody": custody,
        "mask": state["mask"],
        "constants": {
            "margin": str(cases.MARGIN),
            "core_vertices": CORE_LIMIT,
            "minkowski_vertices": MINKOWSKI_LIMIT,
            "clipped_vertices": CLIPPED_LIMIT,
            "center_vertices": cases.CENTER_LIMIT,
            "necessary_pieces": PIECE_LIMIT,
            "generated_pairs_per_row_both_controls": PAIR_LIMIT,
            "polygon_edges": EDGE_LIMIT,
            "prospective_edge_pairs": EDGE_PAIR_LIMIT,
            "input_vertices": cases.INPUT_VERTICES,
            "normalized_rational_bits": finite.BIT_LIMIT,
        },
        "sweep_resource_assurance": {
            "internal_event_probe_caps_available": False,
            "unreduced_integer_product_bit_cap": False,
            "required": "finite edge/pair preflight, outer wall/RSS supervisor",
        },
        "unconditional_exclusion_proved": False,
        "census_admission_proved": False,
        "global_optimality_proved": False,
        "mask_exclusion_proved": False,
        "existing_U_census_admission": False,
        "new_target_admission_proved": False,
        "dominance_over_center_cases_proved": False,
        "parent_geometry_replayed": False,
        "root_checked_now": False,
        "hand_implication": (
            "Astra hand derivation; not independently mathematically reviewed "
            "or machine-checked"
        ),
        **result,
    }


def check(
    document: dict[str, Any], certificate: dict[str, Any], *, deadline: float
) -> dict[str, Any]:
    core_result = {
        k: v for k, v in certificate.items() if k not in {"provenance", "invocation"}
    }
    require(
        core_result == generate(document, deadline=deadline),
        "fresh forbidden-cover reconstruction differs",
    )
    return copy.deepcopy(core_result) | {"verification_passed": True}


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
                name == prefix or name.startswith(prefix + ".")
                for name in sys.modules
                for prefix in (*finite.FORBIDDEN, "devtools.produce_n17_conditional_owned_hull")
            ),
            "producer/kernel/root import in finite checker",
        )
        raw, document = finite.read_json(args.descriptor)
        if args.certificate:
            certificate_raw, certificate = finite.read_json(args.certificate, OUTPUT_LIMIT)
            result = check(document, certificate, deadline=deadline)
            require(
                finite.read_json(args.certificate, OUTPUT_LIMIT)[0] == certificate_raw,
                "certificate changed during reconstruction",
            )
        else:
            result = generate(document, deadline=deadline)
        require(finite.read_json(args.descriptor)[0] == raw, "descriptor bytes changed")
    except IncompleteError as exc:
        result = {
            "schema": SCHEMA,
            "status": "incomplete",
            "error": str(exc),
            "conditional_I_exclusion_proved": False,
        }
    except (
        ValueError,
        KeyError,
        TypeError,
        OSError,
        EOFError,
        standing.VerificationError,
    ) as exc:
        result = {
            "schema": SCHEMA,
            "status": "refused",
            "error": str(exc),
            "conditional_I_exclusion_proved": False,
        }
    result.update(
        provenance=provenance(
            Path(__file__),
            Path(cases.__file__),
            Path(cast(str, finite.__file__)),
            Path(cases.conditional.__file__),
            Path(cast(str, standing.__file__)),
        ),
        invocation={
            "argv": argv if argv is not None else sys.argv[1:],
            "executable": sys.executable,
        },
    )
    text = retained_json.dumps(result, sort_keys=True)
    if len(text.encode()) > OUTPUT_LIMIT or time.monotonic() >= deadline:
        result = {
            "schema": SCHEMA,
            "status": "incomplete",
            "error": "forbidden-cover output byte or wall ceiling",
            "conditional_I_exclusion_proved": False,
        }
        text = retained_json.dumps(result, sort_keys=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text)
    return 0 if result["status"] in ("closed_I_exclusion", "criterion_missed") else 1


if __name__ == "__main__":
    raise SystemExit(main())
