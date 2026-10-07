"""Complete closed partner-pose collision constraints on an accepted n17 parent.

Parent geometry is an explicit accepted premise. This instrument reconstructs
finite strict cores and all-row collision constraints without producer imports.
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

from devtools import probe_n17_conditional_center_cases as cases
from devtools import probe_n17_pooled_feasible_center as feasible
from devtools import probe_n17_pooled_forbidden_cover as union
from devtools.provenance import provenance
from sqpack import retained_json

finite, standing = cases.finite, cases.conditional.standing
require, tick, checked = cases.require, cases.tick, cases.checked
IncompleteError = cases.IncompleteError
type Point = tuple[Q, Q]
SCHEMA = "n17-partner-pose-coupling/v1"
DESCRIPTOR_SCHEMA = "n17-partner-pose-coupling-context/v1"
TAU = Q(53, 128)
LADDER = (Q(1, 128), Q(1, 512), Q(1, 2048), Q(1, 8192))
MARGIN = Q(1, 2**20)
CORE_LIMIT = 32
CENTER_LIMIT = 256
CLIPPED_LIMIT = 384
DOMAIN_LIMIT = 1024
REGION_LIMIT = 256
INPUT_VERTICES = 1048576
ROW_PIECE_LIMIT = 1024
TARGET_PIECE_LIMIT = 1024
FACET_LIMIT = 64
TOTAL_FACETS = 500000
SUPPORT_PRODUCTS = 16000000
EDGE_LIMIT = 4096
EDGE_PAIR_LIMIT = 8400000
JSON_LIMIT = 10 << 20
OUTPUT_LIMIT = 64 << 20
ENDPOINT_INPUT_BITS = 16384
ENDPOINT_ARITHMETIC_BITS = 32768
INPUTS = (
    "parent_descriptor",
    "centered_receipt",
    "feasible_descriptor",
    "feasible_certificate",
    "feasible_replay",
)


def area2(points: list[Point]) -> Q:
    return checked(
        sum(
            (cases.cross(a, b) for a, b in cases.edges(points)),
            Q(0),
        )
    )


def quadratic_nonnegative(a: Q, b: Q, c: Q, lo: Q, hi: Q) -> bool:
    """Check a+bt+ct² >=0 on a complete closed rational interval."""
    values = [checked(a + b * t + c * t * t) for t in (lo, hi)]
    if c > 0:
        vertex = checked(-b / (2 * c))
        if lo < vertex < hi:
            values.append(checked(a + b * vertex + c * vertex * vertex))
    return min(values) >= 0


def core_closed(points: list[Point], lo: Q, hi: Q) -> bool:
    for x, y in points:
        for sign in (-1, 1):
            if not quadratic_nonnegative(
                Q(1, 2) - sign * x, -2 * sign * y, Q(1, 2) + sign * x, lo, hi
            ) or not quadratic_nonnegative(
                Q(1, 2) - sign * y, 2 * sign * x, Q(1, 2) + sign * y, lo, hi
            ):
                return False
    return True


def core(lo: Q, hi: Q, *, strict: bool, deadline: float) -> list[Point]:
    require(0 <= lo <= hi <= 1, "core closed chart interval differs")
    cl, sl = finite.trig(lo)
    ch, sh = finite.trig(hi)
    rhs = Q(1, 2) - MARGIN if strict else Q(1, 2)
    result = [(Q(-1), Q(-1)), (Q(1), Q(-1)), (Q(1), Q(1)), (Q(-1), Q(1))]
    for c in (ch, cl):
        for s in (sl, sh):
            for sign in (-1, 1):
                for a, b in ((sign * c, sign * s), (-sign * s, sign * c)):
                    result = cases.clip(result, a, b, rhs, CORE_LIMIT, deadline)
    require(len(result) >= 3 and area2(result) > 0, "positive-area common core required")
    require(
        standing.core_strict(result, lo, hi) if strict else core_closed(result, lo, hi),
        "fresh exact closed-arc core check failed",
    )
    tick(deadline)
    return result


def wall_clip(points: list[Point], lo: Q, hi: Q, deadline: float) -> list[Point]:
    require(0 <= lo <= hi <= 1, "wall closed chart interval differs")
    cl, sl = finite.trig(lo)
    ch, sh = finite.trig(hi)
    reach = checked(min(cl + sl, ch + sh) / 2)
    lower, upper = checked(cases.OFFSET + reach), checked(cases.U - cases.OFFSET - reach)
    if lower > upper:
        return []
    for a, b, rhs in (
        (Q(-1), Q(0), -lower),
        (Q(1), Q(0), upper),
        (Q(0), Q(-1), -lower),
        (Q(0), Q(1), upper),
    ):
        points = cases.clip(points, a, b, rhs, CLIPPED_LIMIT, deadline)
    return points


def closed_rows(
    raw: Any, owner: int, count: int, reference_context: dict[str, Any] | None = None
) -> None:
    require(type(raw) is list and len(raw) == count, "complete closed row roster differs")
    cursor = Q(0)
    for index, row in enumerate(raw):
        cases.opaque_row(row)
        lo, hi = map(finite.rational, row["interval"])
        require(lo == cursor and lo < hi <= 1, "complete closed row partition differs")
        ref = row["reference"]
        require(ref["row"] == index, "typed reference row differs")
        if ref["kind"] == "wall_seed":
            require(ref["owner"] == owner, "typed reference owner differs")
        elif reference_context is not None:
            require(
                ref["node"] == reference_context["node_id"]
                and 0 <= ref["step"] < len(reference_context["step_owners"])
                and reference_context["step_owners"][ref["step"]] == owner,
                "typed phase3 node/step owner differs",
            )
        cursor = hi
    require(cursor == 1, "closed rows do not cover full chart")


def row_domain(
    row: dict[str, Any],
    counter: list[int],
    deadline: float,
    core_cache: dict[tuple[Q, Q], list[Point]] | None = None,
) -> dict[str, Any]:
    lo, hi = map(finite.rational, row["interval"])
    if len(row["residual_polygons"]) > ROW_PIECE_LIMIT:
        raise IncompleteError("coupling per-row residual piece ceiling")
    pieces = []
    for index, raw in enumerate(row["residual_polygons"]):
        points = parse_polygon(raw, counter, deadline)
        clipped = wall_clip(points, lo, hi, deadline)
        pieces.append({"piece_index": index, "necessary_domain": finite.serial(clipped)})
    all_vertices = [
        (finite.rational(x), finite.rational(y))
        for item in pieces
        for x, y in item["necessary_domain"]
    ]
    domain = cases.bounded_hull(all_vertices, DOMAIN_LIMIT, deadline)
    row_core = []
    if domain:
        core_cache = {} if core_cache is None else core_cache
        if (lo, hi) not in core_cache:
            core_cache[lo, hi] = core(lo, hi, strict=True, deadline=deadline)
        row_core = list(core_cache[lo, hi])
    return {
        "reference": row["reference"].copy(),
        "interval": row["interval"].copy(),
        "pieces": pieces,
        "domain": domain,
        "core": row_core,
    }


def parse_polygon(raw: Any, counter: list[int], deadline: float) -> list[Point]:
    finite.opaque_polygon(raw)
    if len(raw) > CENTER_LIMIT:
        raise IncompleteError("coupling input piece vertex ceiling")
    counter[0] += len(raw)
    if counter[0] > INPUT_VERTICES:
        raise IncompleteError("coupling used input vertex ceiling")
    points = [(finite.rational(x), finite.rational(y)) for x, y in raw]
    return cases.bounded_hull(points, CENTER_LIMIT, deadline)


def row_planes(
    domain: list[Point],
    partner_core: list[Point],
    own_core: list[Point],
    work: dict[str, Any] | None = None,
) -> Any:
    require(bool(domain), "empty row has no collision constraint")
    work = new_work() if work is None else work
    key = tuple(partner_core), tuple(own_core)
    if key not in work["facets"]:
        work["facets"][key] = standing.difference_facets(
            [standing.homogeneous(p) for p in partner_core],
            [standing.homogeneous(p) for p in own_core],
        )
        work["generated_facets"] += len(work["facets"][key])
    facets = work["facets"][key]
    require(len(facets) >= 3, "degenerate collision difference")
    if len(facets) > FACET_LIMIT:
        raise IncompleteError("coupling row facet ceiling")
    work["facet_instances_checked"] += len(facets)
    if work["facet_instances_checked"] > TOTAL_FACETS:
        raise IncompleteError("coupling overall generated facet ceiling")
    for nx, ny, hn, hd in facets:
        a, b = checked(Q(nx)), checked(Q(ny))
        support_key = tuple(domain), nx, ny
        if support_key not in work["minimum"]:
            work["support_vertex_products"] += len(domain)
            if work["support_vertex_products"] > SUPPORT_PRODUCTS:
                raise IncompleteError("coupling MIN-support vertex product ceiling")
            work["minimum"][support_key] = min(finite.dot(p, (a, b)) for p in domain)
        minimum = work["minimum"][support_key]
        yield a, b, checked(checked(Q(hn, hd)) + minimum)


def new_work() -> dict[str, Any]:
    return {
        "facets": {},
        "minimum": {},
        "generated_facets": 0,
        "facet_instances_checked": 0,
        "support_vertex_products": 0,
    }


def collision_region(
    rows: list[dict[str, Any]],
    own_core: list[Point],
    deadline: float,
    work: dict[str, Any] | None = None,
    box: list[Point] | None = None,
) -> list[Point]:
    """Intersect every live row's necessary collision constraints for one partner."""
    result = (
        list(box)
        if box is not None
        else [(Q(0), Q(0)), (cases.U, Q(0)), (cases.U, cases.U), (Q(0), cases.U)]
    )
    for row in rows:
        tick(deadline)
        if not row["domain"]:
            continue
        for a, b, rhs in row_planes(row["domain"], row["core"], own_core, work):
            result = cases.clip(result, a, b, rhs, REGION_LIMIT, deadline)
    tick(deadline)
    return result


def point_collision(
    rows: list[dict[str, Any]],
    own_core: list[Point],
    centre: Point,
    work: dict[str, Any],
    deadline: float,
) -> dict[str, Any]:
    first_failed = None
    facets_checked = 0
    for row_index, row in enumerate(rows):
        tick(deadline)
        if not row["domain"]:
            continue
        for facet_index, (a, b, rhs) in enumerate(
            row_planes(row["domain"], row["core"], own_core, work)
        ):
            tick(deadline)
            lhs = finite.dot(centre, (a, b))
            facets_checked += 1
            if lhs > rhs and first_failed is None:
                first_failed = {
                    "row_index": row_index,
                    "reference": copy.deepcopy(row["reference"]),
                    "facet_index": facet_index,
                    "normal": [str(a), str(b)],
                    "rhs": str(rhs),
                    "lhs": str(lhs),
                }
    tick(deadline)
    return {
        "excluded": first_failed is None,
        "first_failed_facet": first_failed,
        "facets_checked": facets_checked,
        "complete_rows_checked": len(rows),
    }


def endpoint_rational(token: Any) -> Q:
    """Bound syntax before allocation, including integers above CPython's digit guard."""
    require(
        type(token) is str and token.isascii(), "endpoint ASCII exact rational string required"
    )
    if len(token) > 10000:
        raise IncompleteError("endpoint input rational string ceiling")
    finite.rational_grammar(token)

    def integer(part: str) -> int:
        negative = part.startswith("-")
        digits = part[1:] if negative else part
        value = 0
        for start in range(0, len(digits), 1000):
            chunk = digits[start : start + 1000]
            value = value * 10 ** len(chunk) + int(chunk)
        return -value if negative else value

    numerator, separator, denominator = token.partition("/")
    n, d = integer(numerator), integer(denominator) if separator else 1
    if max(abs(n).bit_length(), d.bit_length()) > ENDPOINT_INPUT_BITS:
        raise IncompleteError("endpoint input rational bit ceiling")
    require(token != "-0" and (not separator or d > 1), "noncanonical endpoint rational")
    result = Q(n, d)
    require(result.numerator == n and result.denominator == d, "noncanonical endpoint rational")
    return result


def endpoint_checked(value: Q) -> Q:
    if (
        max(abs(value.numerator).bit_length(), value.denominator.bit_length())
        > ENDPOINT_ARITHMETIC_BITS
    ):
        raise IncompleteError("endpoint containment arithmetic ceiling")
    return value


def endpoint_contains(polygon: list[Point], point: Point) -> bool:
    if not polygon:
        return False
    if len(polygon) == 1:
        return point == polygon[0]
    for a, b in cases.edges(polygon):
        dx, dy = cases.subtract(b, a)
        px = endpoint_checked(point[0] - a[0])
        py = endpoint_checked(point[1] - a[1])
        value = endpoint_checked(endpoint_checked(dx * py) - endpoint_checked(dy * px))
        if (len(polygon) == 2 and value != 0) or (len(polygon) >= 3 and value < 0):
            return False
    return len(polygon) != 2 or all(
        min(a, b) <= x <= max(a, b)
        for a, b, x in zip(polygon[0], polygon[1], point, strict=True)
    )


def endpoint_control(
    roster: Any,
    domains: dict[int, list[dict[str, Any]]],
    roles: dict[str, int],
    deadline: float,
) -> list[dict[str, Any]]:
    require(type(roster) is list, "endpoint roster list required")
    roster = cast(list[dict[str, Any]], roster)
    require(
        [p["label"] for p in roster] == list(range(1, 18))
        and {str(p["label"]): p["owner"] for p in roster} == roles,
        "full17 endpoint role roster differs",
    )
    witnesses = []
    for pose in roster:
        tick(deadline)
        require(
            type(pose["centre"]) is list and len(pose["centre"]) == 2,
            "endpoint two-axis centre required",
        )
        centre = []
        for box in pose["centre"]:
            require(type(box) is list and len(box) == 2, "endpoint centre interval shape")
            lo, hi = map(endpoint_rational, box)
            require(lo <= hi, "endpoint centre interval order")
            centre.append((lo, hi))
        corners = [(x, y) for x in centre[0] for y in centre[1]]
        require(type(pose["charts"]) is list and pose["charts"], "endpoint chart alternatives")
        charts = []
        for box in pose["charts"]:
            require(type(box) is list and len(box) == 2, "endpoint chart interval shape")
            lo, hi = map(endpoint_rational, box)
            require(0 <= lo <= hi <= 1, "endpoint chart interval order")
            charts.append((lo, hi))
        found = []
        for index, row in enumerate(domains[pose["owner"]]):
            lo, hi = map(finite.rational, row["interval"])
            if any(lo <= a <= b <= hi for a, b in charts) and all(
                endpoint_contains(row["domain"], p) for p in corners
            ):
                found.append(index)
        require(bool(found), f"endpoint calibration lost label {pose['label']}")
        if pose["label"] == 1:
            require(
                charts == [(Q(0), Q(0)), (Q(1), Q(1))], "fixed label1 endpoint charts differ"
            )
            require(
                all(not (TAU - h <= b and a <= TAU + h) for h in LADDER for a, b in charts),
                "regional angle ladder meets endpoint family",
            )
        witnesses.append({"label": pose["label"], "owner": pose["owner"], "row_indices": found})
    return witnesses


def cover_piece(
    domain: list[Point], regions: dict[int, list[Point]], deadline: float
) -> dict[str, Any]:
    clipped = {}
    for owner, region in regions.items():
        polygon = domain
        if not region:
            polygon = []
        else:
            for a, b, rhs in standing.closed_planes(region):
                polygon = cases.clip(polygon, a, b, rhs, CLIPPED_LIMIT, deadline)
        clipped[owner] = polygon
    edges = sum(len(cases.edges(p)) for p in [domain, *clipped.values()])
    comparisons = edges * (edges - 1) // 2
    if edges > EDGE_LIMIT or comparisons > EDGE_PAIR_LIMIT:
        raise IncompleteError("coupling sweep edge/pair ceiling")
    tick(deadline)
    if not domain:
        covered, probe, primitive = True, None, "empty_piece"
    elif len(domain) <= 2:
        covered, probe = standing.degenerate_covered(domain, list(clipped.values())), None
        primitive = "degenerate_covered"
    else:
        covered, probe = standing.covered_by_sweep(domain, list(clipped.values()))
        primitive = "covered_by_sweep"
    tick(deadline)
    if probe is not None:
        checked(probe)
    return {
        "covered": covered,
        "primitive": primitive,
        "uncovered_probe": str(probe) if probe is not None else None,
        "clipped_regions": {str(o): finite.serial(p) for o, p in clipped.items()},
        "edges": edges,
        "prospective_edge_pairs": comparisons,
        "internal_events": None,
        "internal_probes": None,
    }


def target_rows(
    rows: list[dict[str, Any]],
    centre: Point,
    half_width: Q,
    counter: list[int],
    deadline: float,
) -> list[dict[str, Any]]:
    interval = TAU - half_width, TAU + half_width
    result = []
    total = 0
    for index, row in enumerate(rows):
        lo, hi = map(finite.rational, row["interval"])
        lo, hi = max(lo, interval[0]), min(hi, interval[1])
        if lo > hi:
            continue
        pieces = []
        for piece_index, raw in enumerate(row["residual_polygons"]):
            points = parse_polygon(raw, counter, deadline)
            points = wall_clip(points, lo, hi, deadline)
            for a, b, rhs in (
                (Q(-1), Q(0), -centre[0] + half_width),
                (Q(1), Q(0), centre[0] + half_width),
                (Q(0), Q(-1), -centre[1] + half_width),
                (Q(0), Q(1), centre[1] + half_width),
            ):
                points = cases.clip(points, a, b, checked(rhs), CLIPPED_LIMIT, deadline)
            pieces.append({"piece_index": piece_index, "domain": points})
            total += 1
            if total > TARGET_PIECE_LIMIT:
                raise IncompleteError("coupling target piece/context ceiling")
        result.append(
            {
                "row_index": index,
                "reference": copy.deepcopy(row["reference"]),
                "interval": [str(lo), str(hi)],
                "pieces": pieces,
                "core": core(lo, hi, strict=False, deadline=deadline),
            }
        )
    require(
        any(
            finite.rational(row["interval"][0]) <= TAU <= finite.rational(row["interval"][1])
            and any(cases.contains(p["domain"], centre) for p in row["pieces"])
            for row in result
        ),
        "fixed witness lost from declared regional target",
    )
    tick(deadline)
    return result


def construct(
    cells: dict[str, Any],
    roles: dict[str, int],
    roster: Any,
    centre: Point,
    *,
    deadline: float,
    reference_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    require(
        set(roles) == set(map(str, range(1, 18)))
        and roles["1"] == 0
        and roles["6"] == 12
        and len(set(roles.values())) == 17
        and all(type(owner) is int and 0 <= owner < 24 for owner in roles.values())
        and set(cells) == set(map(str, roles.values())),
        "complete frozen label/owner/cell roster differs",
    )
    domains = {}
    counter = [0]
    core_cache: dict[tuple[Q, Q], list[Point]] = {}
    for owner in sorted(roles.values()):
        rows = cells[str(owner)]
        closed_rows(rows, owner, 32 if owner == roles["6"] else 64, reference_context)
        domains[owner] = [row_domain(row, counter, deadline, core_cache) for row in rows]
        require(
            any(r["domain"] for r in domains[owner]), "endpoint calibration all-empty partner"
        )
    witnesses = endpoint_control(roster, domains, roles, deadline)
    point_pieces = []
    for row in cells["0"]:
        lo, hi = map(finite.rational, row["interval"])
        if lo <= TAU <= hi:
            point_pieces.extend(
                wall_clip(parse_polygon(raw, counter, deadline), TAU, TAU, deadline)
                for raw in row["residual_polygons"]
            )
    require(
        any(cases.contains(piece, centre) for piece in point_pieces),
        "fixed witness absent from individual accepted owner0 piece",
    )
    partners = {owner: raw for owner, raw in domains.items() if owner != 0}
    work = new_work()
    own = core(TAU, TAU, strict=False, deadline=deadline)
    point_results = {
        o: point_collision(rows, own, centre, work, deadline) for o, rows in partners.items()
    }
    excluded_by = [o for o, result in point_results.items() if result["excluded"]]
    levels = []
    regional = False
    if excluded_by:
        for width in LADDER:
            target = target_rows(cells["0"], centre, width, counter, deadline)
            box = [
                (centre[0] - width, centre[1] - width),
                (centre[0] + width, centre[1] - width),
                (centre[0] + width, centre[1] + width),
                (centre[0] - width, centre[1] + width),
            ]
            rows_result = []
            covered = True
            for row in target:
                regions_at_row = {
                    o: collision_region(rs, row["core"], deadline, work, box)
                    for o, rs in partners.items()
                }
                pieces = []
                for piece in row["pieces"]:
                    coverage = cover_piece(piece["domain"], regions_at_row, deadline)
                    covered = covered and coverage["covered"]
                    pieces.append(
                        {
                            "piece_index": piece["piece_index"],
                            "domain": finite.serial(piece["domain"]),
                            **coverage,
                        }
                    )
                rows_result.append(
                    {
                        "row_index": row["row_index"],
                        "reference": row["reference"],
                        "interval": row["interval"],
                        "owner_closed_core": finite.serial(row["core"]),
                        "partner_regions": {
                            str(o): finite.serial(p) for o, p in regions_at_row.items()
                        },
                        "pieces": pieces,
                    }
                )
            levels.append(
                {
                    "half_width": str(width),
                    "angle_interval": [str(TAU - width), str(TAU + width)],
                    "centre_box": [[str(v - width), str(v + width)] for v in centre],
                    "all_pieces_covered": covered,
                    "rows": rows_result,
                }
            )
            if covered:
                regional = True
                break
    tick(deadline)
    return {
        "status": "closed_region_exclusion"
        if regional
        else "fixed_witness_only"
        if excluded_by
        else "criterion_missed",
        "criterion_met": regional,
        "closed_region_exclusion_proved": regional,
        "fixed_witness_excluded": bool(excluded_by),
        "point_excluded_by": excluded_by,
        "fixed_point_partners": {str(o): result for o, result in point_results.items()},
        "fixed_point_owner_closed_core": finite.serial(own),
        "endpoint_control": {
            "all17_retained": True,
            "witnesses": witnesses,
            "label1_charts_disjoint_from_ladder": True,
        },
        "levels": levels,
        "unstarted_ladder": [str(h) for h in LADDER[len(levels) :]],
        "foreign_rows_checked": sum(len(rs) for rs in partners.values()),
        "all_rows_checked": sum(len(rs) for rs in domains.values()),
        "input_vertices_parsed": counter[0],
        "generated_facets": work["generated_facets"],
        "facet_instances_checked": work["facet_instances_checked"],
        "MIN_support_vertex_products": work["support_vertex_products"],
        "rows": {
            str(owner): [
                {
                    **row,
                    "domain": finite.serial(row["domain"]),
                    "core": finite.serial(row["core"]),
                }
                for row in rs
            ]
            for owner, rs in domains.items()
        },
    }


def intake(
    document: dict[str, Any], held: dict[Path, tuple[str, int]], deadline: float
) -> tuple[dict[str, Any], dict[str, Any], list[Any], Point]:
    require(
        document["schema"] == DESCRIPTOR_SCHEMA
        and set(document)
        == {"schema", *(k for name in INPUTS for k in (name, name + "_sha256"))},
        "coupling descriptor fields/schema",
    )
    values = {}
    for name in INPUTS:
        path = finite.retained_path(document[name])
        raw, value = finite.read_json(path, JSON_LIMIT)
        require(path not in held, "duplicate coupling input role path")
        digest = hashlib.sha256(raw).hexdigest()
        require(digest == document[name + "_sha256"], "coupling input byte identity differs")
        held[path] = digest, JSON_LIMIT
        values[name] = value
        tick(deadline)
    gate, centered = values["parent_descriptor"], values["centered_receipt"]
    descriptor, certificate, replay = (
        values[name]
        for name in ("feasible_descriptor", "feasible_certificate", "feasible_replay")
    )
    require(
        certificate["schema"] == feasible.SCHEMA
        and certificate["status"] == "owned_point_relaxation_witness"
        and certificate["criterion_met"] is True
        and replay["verification_passed"] is True
        and feasible.witness.payload(certificate) == feasible.witness.payload(replay),
        "accepted matched owned-point witness/replay required",
    )
    # Preserve all small byte-bound inputs actually used by the fresh finite
    # reconstruction throughout the later coupling computation.
    for role in feasible.INPUTS:
        path = finite.retained_path(descriptor[role])
        expected = descriptor[role + "_sha256"]
        digest = finite.digest(path, JSON_LIMIT, deadline)
        require(digest == expected, "matched witness dependency bytes differ")
        require(path not in held or held[path][0] == digest, "input alias identity differs")
        held[path] = digest, JSON_LIMIT
    fresh = feasible.check(descriptor, certificate, deadline=deadline)
    require(
        fresh["criterion_met"] is True
        and fresh["tau"] == str(TAU)
        and fresh["pose"]["container_passed"] is True
        and fresh["pose"]["all_owner0_strict"] is True
        and fresh["pose"]["all_foreign_open_avoidance"] is True
        and fresh["container"] == standing.CenteredContainer(cases.U, cases.V).record(),
        "fresh matched point-only feasibility fails",
    )
    final, custody = finite.extract(gate, deadline)
    raw_receipt, accepted = finite.accepted_receipt(gate)
    # Bind phase3 references to the canonical header's node and actual owners.
    node_path = (
        finite.retained_path(gate["saved_objects"]) / f"node-{gate['node_sha256']}.json.gz"
    )
    stream = finite.BoundedNode(node_path, deadline)
    step_owners = [step["owner"] for step in stream.steps()]
    require(
        stream.sha256 == gate["node_sha256"]
        and step_owners == accepted["custody"]["parent_replay"]["step_owners"]
        and type(stream.header["node_id"]) is str,
        "canonical reference-context node/owner sequence differs",
    )
    custody["typed_reference_context"] = {
        "node_id": stream.header["node_id"],
        "step_owners": step_owners,
    }
    parent = certificate["parent"]
    expected_parent = {
        "schema": "accepted-centered-parent/v1",
        "seed_sha256": gate["seed_sha256"],
        "node_sha256": gate["node_sha256"],
        "compressed_sha256": gate["compressed_sha256"],
        "h290_receipt": gate["h290_receipt"],
        "h290_receipt_sha256": gate["h290_receipt_sha256"],
        "centered_parent_receipt": document["centered_receipt"],
        "centered_parent_receipt_sha256": document["centered_receipt_sha256"],
    }
    result = centered["fresh_standing"]["receipt"]
    require(
        parent == expected_parent
        and centered["schema"] == "n17-centered-cap-standing-context/v1"
        and centered["status"] == "centered_stall_control_checked"
        and centered["readiness_passed"] is True
        and centered["verification_passed"] is True
        and centered["fresh_standing"]["exit_code"] == 0
        and result["schema"] == standing.CENTERED_SCHEMA
        and result["mode"] == "full"
        and result["status"] == "PASS_STALL"
        and result["independent_modules"] is True
        and result["root_cap_join_checked"] is False
        and result["owned_hull_limit"] == 48
        and result["container"] == standing.CenteredContainer(cases.U, cases.V).record()
        and result["certificate"]
        == {"seed_sha256": gate["seed_sha256"], "node_sha256": gate["node_sha256"]}
        and result["compressed_sha256"] == cases.conditional.parent_compressed_roles(gate)
        and result["mask"] == final["mask"] == certificate["mask"]
        and result["counts"]["steps"] == 16
        and result["closed"] is False
        and result["closure"] is None
        and centered["accepted_context"]["accepted_endpoint"]["sha256"]
        == gate["h290_receipt_sha256"],
        "centered full same-object parent/frame premise differs",
    )
    for path_token, expected in gate["compressed_sha256"].items():
        path = finite.retained_path(path_token)
        ceiling = finite.SEED_LIMIT if path.name.startswith("seed-") else finite.NODE_LIMIT
        held[path] = expected, ceiling
    path = finite.retained_path(gate["h290_receipt"])
    require(
        hashlib.sha256(raw_receipt).hexdigest() == gate["h290_receipt_sha256"],
        "H290 bytes differ",
    )
    held[path] = gate["h290_receipt_sha256"], JSON_LIMIT
    selection = fresh["chosen"]["selection"]["center"]
    require(type(selection) is list and len(selection) == 2, "matched fixed centre shape")
    centre = (finite.rational(selection[0]), finite.rational(selection[1]))
    return final, custody, accepted["custody"]["input_control"]["endpoint_roster"], centre


def scope() -> dict[str, bool]:
    return dict.fromkeys(
        (
            "parent_geometry_replayed",
            "root_checked_now",
            "conditional_I_exclusion_proved",
            "parent_exclusion_proved",
            "mask_exclusion_proved",
            "census_admission_proved",
            "global_optimality_proved",
            "capture_proved",
            "seventeen_square_packing_proved",
        ),
        False,
    )


def constants() -> dict[str, Any]:
    return {
        "tau": str(TAU),
        "ladder": list(map(str, LADDER)),
        "margin": str(MARGIN),
        "geometry_bits": finite.BIT_LIMIT,
        "endpoint_input_bits": ENDPOINT_INPUT_BITS,
        "endpoint_arithmetic_bits": ENDPOINT_ARITHMETIC_BITS,
        "row_pieces": ROW_PIECE_LIMIT,
        "input_piece_vertices": CENTER_LIMIT,
        "clipped_piece_vertices": CLIPPED_LIMIT,
        "used_input_vertices": INPUT_VERTICES,
        "row_domain_vertices": DOMAIN_LIMIT,
        "core_vertices": CORE_LIMIT,
        "facets_per_row_context": FACET_LIMIT,
        "checked_facet_instances": TOTAL_FACETS,
        "MIN_support_vertex_products": SUPPORT_PRODUCTS,
        "partner_region_vertices": REGION_LIMIT,
        "target_pieces_per_context": TARGET_PIECE_LIMIT,
        "sweep_edges": EDGE_LIMIT,
        "sweep_prospective_pairs": EDGE_PAIR_LIMIT,
        "input_json_bytes_each": JSON_LIMIT,
        "output_bytes": OUTPUT_LIMIT,
        "seed_bytes": finite.SEED_LIMIT,
        "compressed_node_bytes": finite.NODE_LIMIT,
        "decoded_node_bytes": finite.DECODED_LIMIT,
        "final_slice_bytes": finite.SLICE_LIMIT,
    }


def generate(document: dict[str, Any], *, deadline: float) -> dict[str, Any]:
    frozen = finite.canonical(document)
    held: dict[Path, tuple[str, int]] = {}
    final, custody, roster, centre = intake(document, held, deadline)
    gate = finite.read_json(finite.retained_path(document["parent_descriptor"]), JSON_LIMIT)[1]
    result = construct(
        final["cells"],
        gate["label_to_owner"],
        roster,
        centre,
        deadline=deadline,
        reference_context=custody["typed_reference_context"],
    )
    for path, (expected, ceiling) in held.items():
        require(finite.digest(path, ceiling, deadline) == expected, "coupling inputs changed")
    require(finite.canonical(document) == frozen, "coupling descriptor changed")
    tick(deadline)
    return {
        "schema": SCHEMA,
        "accepted_inputs": copy.deepcopy(document),
        "container": standing.CenteredContainer(cases.U, cases.V).record(),
        "parent_custody": {
            key: copy.deepcopy(custody[key])
            for key in (
                "h290_receipt",
                "h290_receipt_sha256",
                "seed_sha256",
                "node_sha256",
                "compressed_sha256",
                "steps",
                "accepted_parent_premises",
                "typed_reference_context",
            )
        },
        "matched_owned_point_witness": {
            "centre": list(map(str, centre)),
            "tau": str(TAU),
            "freshly_checked": True,
        },
        "constants": constants(),
        "mathematical_assurance": (
            "finite exact reconstruction; one-sided strictness and endpoint-family "
            "angle invariance are sole-Astra hand implications, not independently "
            "mathematically reviewed or machine-checked"
        ),
        "resource_assurance": {
            "internal_sweep_event_probe_cap": False,
            "unreduced_integer_product_bit_cap": False,
            "required": "outer wall ceiling and sampled current RSS per live owned process",
        },
        **scope(),
        **result,
    }


def check(
    document: dict[str, Any], certificate: dict[str, Any], *, deadline: float
) -> dict[str, Any]:
    expected = feasible.witness.payload(certificate)
    require(
        expected == generate(document, deadline=deadline),
        "fresh complete coupling reconstruction differs",
    )
    tick(deadline)
    return copy.deepcopy(expected) | {"verification_passed": True}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--descriptor", type=Path, required=True)
    parser.add_argument("--certificate", type=Path)
    parser.add_argument("--max-seconds", type=float, default=120)
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
            "producer/kernel/root import in coupling checker",
        )
        raw, document = finite.read_json(args.descriptor, JSON_LIMIT)
        if args.certificate:
            saved, certificate = finite.read_json(args.certificate, OUTPUT_LIMIT)
            result = check(document, certificate, deadline=deadline)
            require(
                finite.read_json(args.certificate, OUTPUT_LIMIT)[0] == saved,
                "coupling certificate bytes changed",
            )
        else:
            result = generate(document, deadline=deadline)
        require(
            finite.read_json(args.descriptor, JSON_LIMIT)[0] == raw,
            "coupling descriptor bytes changed",
        )
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
            Path(cast(str, cases.__file__)),
            Path(cast(str, finite.__file__)),
            Path(cast(str, standing.__file__)),
            Path(cast(str, feasible.__file__)),
            Path(cast(str, union.__file__)),
            Path(cast(str, feasible.witness.__file__)),
            Path(cast(str, cases.conditional.__file__)),
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
            "error": "coupling output byte or wall ceiling",
            "criterion_met": False,
            **scope(),
        }
        text = retained_json.dumps(result, sort_keys=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text)
    return (
        0
        if result["status"]
        in ("closed_region_exclusion", "fixed_witness_only", "criterion_missed")
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
