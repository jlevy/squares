"""One exact square consistent with accepted pooled strict-owned point facts.

The accepted union miss is a premise. This instrument reconstructs a fixed
candidate and its pose tests; it proves no packing, exclusion or admission.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import math
import sys
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, cast

from devtools import probe_n17_pooled_forbidden_cover as union
from devtools.provenance import provenance
from sqpack import retained_json

cases, finite, standing = union.cases, union.finite, union.standing
type Point = tuple[Q, Q]
require, tick, checked = union.require, union.tick, union.checked
IncompleteError = union.IncompleteError
SCHEMA = "n17-pooled-relaxation-witness/v1"
DESCRIPTOR_SCHEMA = "n17-pooled-relaxation-witness-context/v1"
TAU = Q(53, 128)
JSON_LIMIT = 10 << 20
OUTPUT_LIMIT = 64 << 20
POOL_LIMIT, PIECE_LIMIT, REGION_LIMIT, INTERSECTION_LIMIT = 128, 256, 384, 132
INPUTS = ("union_descriptor", "union_certificate", "union_replay")


def scope() -> dict[str, bool]:
    return dict.fromkeys(
        (
            "parent_geometry_replayed",
            "union_geometry_replayed_now",
            "root_checked_now",
            "seventeen_square_packing_proved",
            "conditional_I_exclusion_proved",
            "unconditional_exclusion_proved",
            "census_admission_proved",
            "global_optimality_proved",
            "capture_proved",
        ),
        False,
    )


def payload(document: dict[str, Any]) -> dict[str, Any]:
    return {
        k: v
        for k, v in document.items()
        if k not in {"provenance", "invocation", "verification_passed"}
    }


def polygon(raw: Any, limit: int, deadline: float) -> list[Point]:
    finite.opaque_polygon(raw)
    if len(raw) > limit:
        raise IncompleteError("relaxation-witness input polygon vertex ceiling")
    points = [(finite.rational(x), finite.rational(y)) for x, y in raw]
    result = cases.bounded_hull(points, limit, deadline)
    require(finite.serial(result) == raw, "noncanonical retained polygon")
    return result


def first_gap(lo: Q, hi: Q, spans: list[tuple[Q, Q]]) -> tuple[Q, Q] | None:
    """First positive complement interval; closed touching spans leave no gap."""
    require(lo <= hi and all(a <= b for a, b in spans), "invalid closed section")
    spans = sorted((max(lo, a), min(hi, b)) for a, b in spans if b >= lo and a <= hi)
    if lo == hi:
        return None if any(a <= lo <= b for a, b in spans) else (lo, hi)
    cursor = lo
    for a, b in spans:
        if a > cursor:
            return cursor, a
        cursor = max(cursor, b)
    return (cursor, hi) if cursor < hi else None


def parameter_span(
    region: list[Point], a: Point, b: Point, deadline: float
) -> tuple[Q, Q] | None:
    if not region:
        return None
    dx, dy = cases.subtract(b, a)
    lo, hi = Q(0), Q(1)
    for nx, ny, rhs in standing.closed_planes(region):
        tick(deadline)
        for value in (nx, ny, rhs):
            checked(value)
        value = checked(finite.dot(a, (nx, ny)) - rhs)
        rate = finite.dot((dx, dy), (nx, ny))
        if rate == 0:
            if value > 0:
                return None
        elif rate > 0:
            hi = min(hi, checked(-value / rate))
        else:
            lo = max(lo, checked(-value / rate))
        if lo > hi:
            return None
    return lo, hi


def sweep(
    domain: list[Point], regions: list[list[Point]], deadline: float
) -> tuple[bool, Q | None]:
    edges = sum(len(cases.edges(p)) for p in [domain, *regions])
    if edges > union.EDGE_LIMIT or edges * (edges - 1) // 2 > union.EDGE_PAIR_LIMIT:
        raise IncompleteError("relaxation-witness sweep edge/pair ceiling")
    tick(deadline)
    result, probe = standing.covered_by_sweep(domain, regions)
    tick(deadline)
    if probe is not None:
        checked(probe)
    return result, probe


def choose_center(
    domain: list[Point], regions: list[list[Point]], recorded_probe: Any, deadline: float
) -> dict[str, Any]:
    tick(deadline)
    require(bool(domain), "uncovered empty piece")
    if len(domain) >= 3:
        require(type(recorded_probe) is str, "missing positive-area sweep probe")
        expected = finite.rational(recorded_probe)
        covered, probe = sweep(domain, regions, deadline)
        require(
            not covered and probe == expected,
            "first sweep probe differs from accepted union miss",
        )
        ylo, yhi = min(y for _, y in domain), max(y for _, y in domain)
        a, b = (expected, ylo), (expected, yhi)
        section = parameter_span(domain, a, b, deadline)
        require(section is not None, "uncovered probe has no target section")
        section = cast(tuple[Q, Q], section)
        spans = [
            part for p in regions if (part := parameter_span(p, a, b, deadline)) is not None
        ]
        gap = first_gap(*section, spans)
        dimension = "vertical_section"
    else:
        require(recorded_probe is None, "degenerate piece must have null sweep probe")
        a, b = min(domain), max(domain)
        spans = [
            part for p in regions if (part := parameter_span(p, a, b, deadline)) is not None
        ]
        gap = first_gap(Q(0), Q(1), spans)
        dimension = "point" if a == b else "segment"
    require(gap is not None, "accepted noncoverage has no uncovered gap")
    gap = cast(tuple[Q, Q], gap)
    t = checked((gap[0] + gap[1]) / 2)
    dx, dy = cases.subtract(b, a)
    center = (checked(a[0] + checked(t * dx)), checked(a[1] + checked(t * dy)))
    require(
        cases.contains(domain, center) and all(not cases.contains(p, center) for p in regions),
        "candidate not in exact uncovered complement",
    )
    tick(deadline)
    return {
        "center": list(map(str, center)),
        "selection_dimension": dimension,
        "parameter_segment": finite.serial([a, b]),
        "first_gap": list(map(str, gap)),
        "parameter": str(t),
    }


def body(point: Point, center: Point) -> tuple[Q, Q]:
    c, s = finite.trig(TAU)
    delta = cases.subtract(point, center)
    return finite.dot(delta, (c, s)), finite.dot(delta, (-s, c))


def strict(point: Point, center: Point) -> bool:
    x, y = body(point, center)
    return abs(x) < Q(1, 2) and abs(y) < Q(1, 2)


def square(center: Point, deadline: float) -> list[Point]:
    c, s = finite.trig(TAU)
    corners = [
        (
            checked(center[0] + checked((e * c - f * s) / 2)),
            checked(center[1] + checked((e * s + f * c) / 2)),
        )
        for e in (-1, 1)
        for f in (-1, 1)
    ]
    return cases.bounded_hull(corners, 4, deadline)


def pose(
    center: Point, pools: dict[int, list[Point]], selected: list[Point], deadline: float
) -> dict[str, Any]:
    require(
        len(pools) == 17 and 0 in pools and len(selected) == 5 and len(set(selected)) == 5,
        "complete pool/five-point roster",
    )
    shape = square(center, deadline)
    conditional = cases.bounded_hull(pools[0] + selected, POOL_LIMIT, deadline)
    own_tests = [
        {
            "point": list(map(str, p)),
            "body_coordinates": list(map(str, body(p, center))),
            "strict": strict(p, center),
        }
        for p in conditional
    ]
    wall = all(cases.OFFSET <= value <= cases.U - cases.OFFSET for p in shape for value in p)
    foreign = {}
    for owner in sorted(pools):
        if owner == 0:
            continue
        tick(deadline)
        common = cases.intersection(shape, pools[owner], deadline)
        if len(common) > INTERSECTION_LIMIT:
            raise IncompleteError("relaxation-witness square intersection vertex ceiling")
        totals = [Q(0), Q(0)]
        for point in common:
            tick(deadline)
            totals = [checked(a + b) for a, b in zip(totals, point, strict=True)]
        mean = (
            (checked(totals[0] / len(common)), checked(totals[1] / len(common)))
            if common
            else None
        )
        meets_open = mean is not None and strict(mean, center)
        foreign[str(owner)] = {
            "intersection": finite.serial(common),
            "mean": list(map(str, mean)) if mean is not None else None,
            "mean_body_coordinates": list(map(str, body(mean, center)))
            if mean is not None
            else None,
            "meets_open_square": meets_open,
            "avoidance_passed": not meets_open,
        }
    own = all(test["strict"] is True for test in own_tests)
    avoid = all(test["avoidance_passed"] is True for test in foreign.values())
    success = wall and own and avoid
    return {
        "square": finite.serial(shape),
        "conditional_owner0_hull": finite.serial(conditional),
        "container_passed": wall,
        "owner0_tests": own_tests,
        "all_owner0_strict": own,
        "foreign_tests": foreign,
        "all_foreign_open_avoidance": avoid,
        "criterion_met": success,
        "status": "owned_point_relaxation_witness" if success else "criterion_missed",
    }


def union_contract(
    source: dict[str, Any], certificate: dict[str, Any], replay: dict[str, Any]
) -> None:
    require(
        set(source)
        == {
            "schema",
            "base_kind",
            "proof_pool",
            "initialization_descriptor",
            "initialization_descriptor_sha256",
        }
        and source["schema"] == cases.DESCRIPTOR_SCHEMA
        and source["base_kind"] == cases.BASE_INITIAL
        and source["proof_pool"] == "accepted_original_parent_kernels",
        "frozen union initialization context",
    )
    require(
        replay.get("verification_passed") is True and payload(certificate) == payload(replay),
        "accepted union fresh payload differs",
    )
    require(
        certificate["schema"] == union.SCHEMA
        and certificate["status"] == "criterion_missed"
        and certificate["criterion_met"] is False
        and certificate["pooled_coverage"] is False
        and certificate["conditional_I_exclusion_proved"] is False,
        "complete accepted union miss required",
    )
    require(
        certificate["guard"] == cases.GUARD
        and certificate["container"] == standing.CenteredContainer(cases.U, cases.V).record(),
        "union guard/container differs",
    )
    custody = certificate["custody"]
    require(
        custody["base_kind"] == cases.BASE_INITIAL
        and custody["initialization_freshly_reconstructed"] is True
        and custody["parent_geometry_replayed"] is False
        and custody["child_geometry_replayed_now"] is False
        and custody["initialization_descriptor"] == source["initialization_descriptor"]
        and custody["initialization_descriptor_sha256"]
        == source["initialization_descriptor_sha256"],
        "union parent/initialization custody differs",
    )
    pool = custody["proof_pool"]
    require(
        pool["original_final_contained"] is True
        and pool["unconditional_parent_pools_disjoint"] is True
        and pool["parent_geometry_replayed"] is False,
        "accepted original pool calibration required",
    )
    require(
        pool["node_sha256"] == custody["parent"]["node_sha256"]
        and pool["seed_sha256"] == custody["parent"]["seed_sha256"],
        "pool canonical parent identities differ",
    )
    require(
        pool["selected_five"] == custody["guard_source"]["point_origins"]["selected"]
        and custody["guard_source"]["guard"] == cases.GUARD,
        "five-point guard identity differs",
    )
    mask = certificate["mask"]
    require(
        type(mask) is list
        and len(mask) == 17
        and all(type(i) is int and 0 <= i < 24 for i in mask)
        and mask == sorted(set(mask))
        and 0 in mask
        and 12 in mask
        and set(pool["pools"]) == set(map(str, mask)),
        "full native owner/mask roster",
    )
    constants = {
        "margin": str(cases.MARGIN),
        "core_vertices": union.CORE_LIMIT,
        "minkowski_vertices": union.MINKOWSKI_LIMIT,
        "clipped_vertices": union.CLIPPED_LIMIT,
        "center_vertices": cases.CENTER_LIMIT,
        "necessary_pieces": union.PIECE_LIMIT,
        "generated_pairs_per_row_both_controls": union.PAIR_LIMIT,
        "polygon_edges": union.EDGE_LIMIT,
        "prospective_edge_pairs": union.EDGE_PAIR_LIMIT,
        "input_vertices": cases.INPUT_VERTICES,
        "normalized_rational_bits": finite.BIT_LIMIT,
    }
    require(certificate["constants"] == constants, "union finite constants differ")


def construct(certificate: dict[str, Any], *, deadline: float) -> dict[str, Any]:
    rows: list[dict[str, Any]] = certificate["rows"]
    require(
        type(rows) is list
        and len(rows) == 3
        and [r["row_index"] for r in rows] == [25, 26, 27]
        and [r["interval"] for r in rows]
        == [
            [str(cases.INTERVAL[0])] * 2,
            list(map(str, cases.INTERVAL)),
            [str(cases.INTERVAL[1])] * 2,
        ],
        "complete closed guard row roster",
    )
    row = rows[1]
    pieces: list[dict[str, Any]] = row["pieces"]
    require(
        type(pieces) is list and [p["piece_index"] for p in pieces] == list(range(len(pieces))),
        "retained piece order",
    )
    for piece in pieces:
        require(type(piece["pooled"]["covered"]) is bool, "pooled coverage status")
    eligible = next((p for p in pieces if p["pooled"]["covered"] is False), None)
    if eligible is None:
        tick(deadline)
        return {
            "applicable": False,
            "reason": "row26 has no pooled-uncovered piece",
            "criterion_met": False,
            "status": "criterion_missed",
        }
    domain = polygon(eligible["domain"], PIECE_LIMIT, deadline)
    mask = certificate["mask"]
    raw_regions = eligible["pooled"]["regions"]
    require(
        set(raw_regions) == set(map(str, set(mask) - {0})),
        "complete retained foreign region roster",
    )
    regions = {int(o): polygon(p, REGION_LIMIT, deadline) for o, p in raw_regions.items()}
    pool = certificate["custody"]["proof_pool"]
    pools = {int(o): polygon(p, POOL_LIMIT, deadline) for o, p in pool["pools"].items()}
    selected = polygon(pool["selected_five"], 5, deadline)
    chosen = choose_center(
        domain, list(regions.values()), eligible["pooled"]["uncovered_probe"], deadline
    )
    center = tuple(finite.rational(value) for value in chosen["center"])
    return {
        "applicable": True,
        "row_index": 26,
        "row_reference": copy.deepcopy(row["reference"]),
        "piece_index": eligible["piece_index"],
        "selection": chosen,
        **pose(cast(Point, center), pools, selected, deadline),
    }


def generate(document: dict[str, Any], *, deadline: float) -> dict[str, Any]:
    require(
        set(document) == {"schema", *(k for name in INPUTS for k in (name, name + "_sha256"))}
        and document["schema"] == DESCRIPTOR_SCHEMA,
        "relaxation-witness descriptor fields/schema",
    )
    frozen = finite.canonical(document)
    held: dict[Path, bytes] = {}
    data = []
    for name in INPUTS:
        path = finite.retained_path(document[name])
        raw, value = finite.read_json(path, JSON_LIMIT)
        require(
            hashlib.sha256(raw).hexdigest() == document[name + "_sha256"],
            "union input byte identity differs",
        )
        require(path not in held, "duplicate union input paths")
        held[path] = raw
        data.append(value)
        tick(deadline)
    source, certificate, replay = data
    union_contract(source, certificate, replay)
    result = construct(certificate, deadline=deadline)
    for path, raw in held.items():
        require(
            finite.read_json(path, JSON_LIMIT)[0] == raw, "accepted union input bytes changed"
        )
        tick(deadline)
    require(finite.canonical(document) == frozen, "witness descriptor changed")
    return {
        "schema": SCHEMA,
        "tau": str(TAU),
        "guard": copy.deepcopy(cases.GUARD),
        "container": certificate["container"],
        "mask": certificate["mask"],
        "accepted_union_inputs": copy.deepcopy(document),
        "parent": copy.deepcopy(certificate["custody"]["parent"]),
        "constants": {
            "input_bytes_each": JSON_LIMIT,
            "output_bytes": OUTPUT_LIMIT,
            "normalized_rational_bits": finite.BIT_LIMIT,
            "pool_vertices": POOL_LIMIT,
            "piece_vertices": PIECE_LIMIT,
            "clipped_region_vertices": REGION_LIMIT,
            "square_vertices": 4,
            "intersection_vertices": INTERSECTION_LIMIT,
            "polygon_edges": union.EDGE_LIMIT,
            "prospective_edge_pairs": union.EDGE_PAIR_LIMIT,
        },
        "sweep_resource_assurance": {
            "unreduced_integer_product_bit_cap": False,
            "internal_event_probe_caps_available": False,
            "required": "edge/pair preflight, outer wall and sampled current RSS per process",
        },
        **scope(),
        "hand_implication": (
            "Astra hand derivation; not independently mathematically reviewed "
            "or machine-checked"
        ),
        **result,
    }


def check(
    document: dict[str, Any], certificate: dict[str, Any], *, deadline: float
) -> dict[str, Any]:
    result = payload(certificate)
    require(
        result == generate(document, deadline=deadline),
        "fresh relaxation-witness reconstruction differs",
    )
    return copy.deepcopy(result) | {"verification_passed": True}


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
            "producer/kernel/root import in witness checker",
        )
        raw, document = finite.read_json(args.descriptor)
        if args.certificate:
            saved, certificate = finite.read_json(args.certificate, OUTPUT_LIMIT)
            result = check(document, certificate, deadline=deadline)
            require(
                finite.read_json(args.certificate, OUTPUT_LIMIT)[0] == saved,
                "witness certificate bytes changed",
            )
        else:
            result = generate(document, deadline=deadline)
        require(finite.read_json(args.descriptor)[0] == raw, "witness descriptor bytes changed")
    except IncompleteError as exc:
        result = {
            "schema": SCHEMA,
            "status": "incomplete",
            "error": str(exc),
            "criterion_met": False,
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
            "criterion_met": False,
        }
    result.update(scope())
    result.update(
        provenance=provenance(
            Path(__file__),
            Path(union.__file__),
            Path(cast(str, cases.__file__)),
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
            "error": "witness output byte or wall ceiling",
            "criterion_met": False,
            **scope(),
        }
        text = retained_json.dumps(result, sort_keys=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text)
    return (
        0 if result["status"] in ("owned_point_relaxation_witness", "criterion_missed") else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
