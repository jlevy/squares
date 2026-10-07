"""Exact primitives for a prospective guard-conditioned ownership round.

The original accepted parent and matched witness are inherited premises.
The guard does not contain the certified endpoint family's owner-0 orientations.
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

from devtools import check_n17_full_square_partner_coupling as sat
from devtools import check_n17_partner_pose_coupling as parent
from devtools.provenance import provenance
from sqpack import retained_json

finite, cases, standing = parent.finite, parent.cases, parent.standing
require, tick, checked = parent.require, parent.tick, parent.checked
IncompleteError = parent.IncompleteError
type Point = tuple[Q, Q]
type Plane = tuple[Q, Q, Q]
TAU = Q(53, 128)
HALF_WIDTH = Q(1, 512)
MARGIN = Q(1, 2**20)
# These are the frozen prospective guard-round allocations. Scientific use
# still requires a clean-source registration and fresh reconstruction.
OWNED_LIMIT = 2048
OWNER0_LIMIT = 32
INTERSECTION_LIMIT = 4096
CLIPPED_LIMIT = 384
FACET_LIMIT = 64
BRANCH_LIMIT = 64
STRICT_CHECK_LIMIT = 8000000
STRICT_PAIR_LIMIT = 2000000
RECOVERY_SUPPORT_LIMIT = 16000000
FAST_SUPPORT_LIMIT = 16000000
CONDITIONAL_ROW_LIMIT = 8192
CONDITIONAL_PIECE_LIMIT = 131072
GENERATED_VERTEX_LIMIT = 2097152
DOMAIN_LIMIT = 1024
MINKOWSKI_PRODUCT_LIMIT = 131072
OUTPUT_LIMIT = 64 << 20
SCHEMA = "n17-guard-conditioned-ownership/v1"
DESCRIPTOR_SCHEMA = "n17-guard-conditioned-ownership-context/v1"


class ContextIncompleteError(IncompleteError):
    def __init__(self, message: str, observations: dict[str, Any]) -> None:
        super().__init__(message)
        self.observations: dict[str, Any] = dict(observations) | {
            "completed_contexts_are_candidates_only": True,
            "verification_passed": False,
        }


def new_work() -> dict[str, int]:
    return {
        "minimum_support_products": 0,
        "strict_quadratic_checks": 0,
        "subtraction_branches": 0,
        "intersection_vertex_pairs": 0,
        "strict_vertex_pairs": 0,
        "fastpath_support_products": 0,
        "retained_conditional_pieces": 0,
        "generated_clip_output_vertices": 0,
        "raw_minkowski_vertex_products": 0,
        "context_piece_baseline": 0,
    }


def centre_box(centre: Point, half_width: Q = HALF_WIDTH) -> list[Point]:
    require(
        type(half_width) is Q and half_width in (0, HALF_WIDTH), "frozen half-width differs"
    )
    return [
        (checked(centre[0] + sx * half_width), checked(centre[1] + sy * half_width))
        for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))
    ]


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


def guard_owned(
    centre: Point, work: dict[str, int], deadline: float, *, half_width: Q = HALF_WIDTH
) -> list[Point]:
    corners = centre_box(centre, half_width)
    lo, hi = TAU - half_width, TAU + half_width
    result = [(Q(0), Q(0)), (cases.U, Q(0)), (cases.U, cases.U), (Q(0), cases.U)]
    for a, b, rhs in ownership_planes(corners, lo, hi, work, deadline):
        result = cases.clip(result, a, b, rhs, OWNER0_LIMIT, deadline)
    require(
        len(result) >= 3 and parent.area2(result) > 0,
        "guard owner0 strict core must have positive area",
    )
    seed_radius = checked((Q(1, 2) - MARGIN) / 2 - half_width)
    require(
        half_width != HALF_WIDTH or seed_radius == Q(520191, 2097152),
        "guaranteed guard seed radius differs",
    )
    seed = [
        (checked(centre[0] + sx * seed_radius), checked(centre[1] + sy * seed_radius))
        for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))
    ]
    require(
        all(cases.contains(result, point) for point in seed),
        "guaranteed positive guard seed box is not retained",
    )
    require(
        strictly_owned(result, corners, lo, hi, work, deadline),
        "fresh guard strict ownership fails",
    )
    require(
        strictly_owned(result, [centre], TAU, TAU, work, deadline),
        "matched fixed square fails guard ownership control",
    )
    return result


def forbidden_planes(
    owner_owned: list[Point], partner_core: list[Point], deadline: float
) -> list[Plane]:
    require(
        len(owner_owned) >= 3 and len(partner_core) >= 3,
        "positive-area forbidden operands required",
    )
    tick(deadline)
    facets = standing.difference_facets(
        [standing.homogeneous(p) for p in owner_owned],
        [standing.homogeneous(p) for p in partner_core],
    )
    if len(facets) > FACET_LIMIT:
        raise IncompleteError("guard-owned forbidden facet ceiling")
    require(len(facets) >= 3, "forbidden polygon facets missing")
    return [(checked(Q(a)), checked(Q(b)), checked(Q(hn, hd))) for a, b, hn, hd in facets]


def subtract_piece(
    piece: list[Point], planes: list[Plane], work: dict[str, int], deadline: float
) -> dict[str, Any]:
    """Closed union outside each facet; all forbidden boundaries are retained."""
    require(len(planes) >= 3, "complete forbidden facets required")
    if len(planes) > BRANCH_LIMIT:
        raise IncompleteError("guard-owned per-piece subtraction branch ceiling")
    if piece:
        for index, (a, b, rhs) in enumerate(planes):
            tick(deadline)
            work["fastpath_support_products"] += len(piece)
            if work["fastpath_support_products"] > FAST_SUPPORT_LIMIT:
                raise IncompleteError("guard-owned outside-fastpath support ceiling")
            minimum = min(finite.dot(point, (a, b)) for point in piece)
            if minimum >= rhs:
                return {
                    "pieces": [list(piece)],
                    "branches": [],
                    "empty": False,
                    "boundary_retained": True,
                    "identical_closed_piece_dedup_only": True,
                    "fastpath": {
                        "kind": "whole_piece_in_closed_outside_halfplane",
                        "facet_index": index,
                        "normal": [str(a), str(b)],
                        "rhs": str(rhs),
                        "minimum": str(minimum),
                    },
                }
    branches = []
    unique: dict[tuple[Point, ...], int] = {}
    pieces = []
    for index, (a, b, rhs) in enumerate(planes):
        tick(deadline)
        work["subtraction_branches"] += 1
        output = cases.clip(piece, -a, -b, -rhs, CLIPPED_LIMIT, deadline)
        work["generated_clip_output_vertices"] += len(output)
        if work["generated_clip_output_vertices"] > GENERATED_VERTEX_LIMIT:
            raise IncompleteError("guard-owned generated clip-output vertex ceiling")
        key = tuple(output)
        alias = None
        if output:
            if key not in unique:
                unique[key] = len(pieces)
                pieces.append(output)
            alias = unique[key]
        branches.append(
            {
                "facet_index": index,
                "outside_closed_plane": [str(-a), str(-b), str(-rhs)],
                "piece_alias": alias,
                "empty": not output,
            }
        )
    tick(deadline)
    return {
        "pieces": pieces,
        "branches": branches,
        "empty": not pieces,
        "boundary_retained": True,
        "identical_closed_piece_dedup_only": True,
        "fastpath": None,
    }


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


def shared_owned(
    groups: dict[int, list[Point]], work: dict[str, int], deadline: float
) -> dict[str, Any] | None:
    owners = sorted(groups)
    for index, owner in enumerate(owners):
        for other in owners[index + 1 :]:
            tick(deadline)
            if max(len(groups[owner]), len(groups[other])) > OWNED_LIMIT:
                raise IncompleteError("guard-owned intersection input vertex ceiling")
            products = len(groups[owner]) * len(groups[other])
            work["intersection_vertex_pairs"] += products
            overlap = cases.conditional.intersection(groups[owner], groups[other])
            tick(deadline)
            if len(overlap) > INTERSECTION_LIMIT:
                raise IncompleteError("guard-owned intersection output vertex ceiling")
            overlap = [(checked(x), checked(y)) for x, y in overlap]
            if overlap:
                return {
                    "kind": "shared_strictly_owned_point",
                    "owners": [owner, other],
                    "intersection": finite.serial(overlap),
                    "conditional_only": True,
                }
    return None


def guard_wall_clip(
    points: list[Point], lo: Q, hi: Q, work: dict[str, int], deadline: float
) -> list[Point]:
    """Count the restricted-angle wall clips as conditional-cover outputs."""
    require(0 <= lo <= hi <= 1, "guard wall interval differs")
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
        work["generated_clip_output_vertices"] += len(points)
        if work["generated_clip_output_vertices"] > GENERATED_VERTEX_LIMIT:
            raise IncompleteError("guard-owned generated clip-output vertex ceiling")
    return points


def guarded_owner0(
    rows: list[dict[str, Any]],
    centre: Point,
    counter: list[int],
    work: dict[str, int],
    deadline: float,
    *,
    half_width: Q = HALF_WIDTH,
) -> list[dict[str, Any]]:
    centre_box(centre, half_width)
    result = []
    lo_guard, hi_guard = TAU - half_width, TAU + half_width
    for index, row in enumerate(rows):
        lo, hi = map(finite.rational, row["interval"])
        lo, hi = max(lo, lo_guard), min(hi, hi_guard)
        if lo > hi:
            continue
        pieces = []
        for piece_index, raw in enumerate(row["residual_polygons"]):
            points = parent.parse_polygon(raw, counter, deadline)
            points = guard_wall_clip(points, lo, hi, work, deadline)
            for a, b, rhs in (
                (Q(-1), Q(0), -centre[0] + half_width),
                (Q(1), Q(0), centre[0] + half_width),
                (Q(0), Q(-1), -centre[1] + half_width),
                (Q(0), Q(1), centre[1] + half_width),
            ):
                points = cases.clip(points, a, b, checked(rhs), CLIPPED_LIMIT, deadline)
                work["generated_clip_output_vertices"] += len(points)
                if work["generated_clip_output_vertices"] > GENERATED_VERTEX_LIMIT:
                    raise IncompleteError("guard-owned generated clip-output vertex ceiling")
            if points:
                pieces.append(
                    {"source_piece_index": piece_index, "domain": finite.serial(points)}
                )
        if len(pieces) > CONDITIONAL_ROW_LIMIT:
            raise IncompleteError("guard-owned owner0 per-row conditional piece ceiling")
        work["retained_conditional_pieces"] += len(pieces)
        if (
            work["retained_conditional_pieces"] - work["context_piece_baseline"]
            > CONDITIONAL_PIECE_LIMIT
        ):
            raise IncompleteError("guard-owned global conditional piece ceiling")
        result.append(
            {
                "row_index": index,
                "reference": copy.deepcopy(row["reference"]),
                "interval": [str(lo), str(hi)],
                "original_piece_count": len(row["residual_polygons"]),
                "pieces": pieces,
            }
        )
    require(
        any(
            finite.rational(row["interval"][0]) <= TAU <= finite.rational(row["interval"][1])
            and any(
                cases.contains(
                    [(finite.rational(x), finite.rational(y)) for x, y in p["domain"]], centre
                )
                for p in row["pieces"]
            )
            for row in result
        ),
        "fixed witness absent from actual guard target piece",
    )
    return result


def condition_row(
    row: dict[str, Any],
    q0: list[Point],
    cache: dict[Any, Any],
    work: dict[str, int],
    deadline: float,
) -> dict[str, Any]:
    if row["domain"]:
        key = tuple(row["core"])
        if key not in cache:
            work["raw_minkowski_vertex_products"] += len(q0) * len(row["core"])
            if work["raw_minkowski_vertex_products"] > MINKOWSKI_PRODUCT_LIMIT:
                raise IncompleteError("guard-owned raw Minkowski vertex-product ceiling")
            cache[key] = forbidden_planes(q0, row["core"], deadline)
        planes = cache[key]
    else:
        planes = []
    pieces: list[list[Point]] = []
    aliases: dict[tuple[Point, ...], int] = {}
    sources = []
    for original in row["pieces"]:
        polygon = [
            (finite.rational(x), finite.rational(y)) for x, y in original["necessary_domain"]
        ]
        if polygon:
            subtraction = subtract_piece(polygon, planes, work, deadline)
        else:
            subtraction = {
                "pieces": [],
                "branches": [],
                "empty": True,
                "fastpath": None,
                "boundary_retained": True,
                "identical_closed_piece_dedup_only": True,
            }
        local_to_row = []
        for output in subtraction["pieces"]:
            key = tuple(output)
            if key not in aliases:
                if len(pieces) >= CONDITIONAL_ROW_LIMIT:
                    raise IncompleteError("guard-owned per-row conditional piece ceiling")
                aliases[key] = len(pieces)
                pieces.append(output)
                work["retained_conditional_pieces"] += 1
                if (
                    work["retained_conditional_pieces"] - work["context_piece_baseline"]
                    > CONDITIONAL_PIECE_LIMIT
                ):
                    raise IncompleteError("guard-owned global conditional piece ceiling")
            local_to_row.append(aliases[key])
        # Geometry is transient: the fresh checker rebuilds every original
        # piece/closed disjunct. Arrays retain all source and face aliases.
        fast = subtraction["fastpath"]
        sources.append(
            [
                original["piece_index"],
                fast["facet_index"] if fast else None,
                local_to_row,
                [branch["piece_alias"] for branch in subtraction["branches"]],
            ]
        )
    domain = cases.bounded_hull(
        [point for polygon in pieces for point in polygon], DOMAIN_LIMIT, deadline
    )
    return {
        "reference": copy.deepcopy(row["reference"]),
        "interval": list(row["interval"]),
        "pieces": pieces,
        "source_pieces": sources,
        "domain": domain,
        "forbidden_planes": [list(map(str, plane)) for plane in planes],
        "original_piece_count": len(row["pieces"]),
        "conditional_piece_count": len(pieces),
        "all_closed_complement_boundaries_retained": True,
    }


def condition_context(  # noqa: PLR0917
    cells: dict[str, Any],
    original: dict[int, list[dict[str, Any]]],
    centre: Point,
    counter: list[int],
    work: dict[str, int],
    deadline: float,
    *,
    half_width: Q,
) -> dict[str, Any]:
    work["context_piece_baseline"] = work["retained_conditional_pieces"]
    target = guarded_owner0(cells["0"], centre, counter, work, deadline, half_width=half_width)
    q0 = guard_owned(centre, work, deadline, half_width=half_width)
    conditional = {}
    cache: dict[Any, Any] = {}
    for owner, rows in original.items():
        if owner != 0:
            conditional[owner] = [condition_row(row, q0, cache, work, deadline) for row in rows]
    empty = [
        owner for owner, rows in conditional.items() if all(not row["domain"] for row in rows)
    ]
    groups = {0: q0}
    if empty:
        selected = min(empty)
        closure = {
            "kind": "conditional_owner_cover_empty",
            "owner": selected,
            "row_indices": list(range(len(conditional[selected]))),
            "conditional_only": True,
        }
        recovery = "not_required_after_complete_conditional_owner_empty"
    else:
        for owner, rows in conditional.items():
            groups[owner] = common_owned(rows, work, deadline)
        closure = shared_owned(groups, work, deadline)
        recovery = "all_surviving_closed_rows_reconstructed"
    tick(deadline)
    return {
        "status": "closed_guard_exclusion"
        if closure and half_width > 0
        else "point_guard_exclusion"
        if closure
        else "criterion_missed",
        "criterion_met": closure is not None and half_width > 0,
        "declared_guard_exclusion_proved": closure is not None and half_width > 0,
        "point_guard_exclusion_proved": closure is not None and half_width == 0,
        "context_nonzero": half_width > 0,
        "closure": closure,
        "guard": {
            "half_width": str(half_width),
            "centre_box": [
                [str(checked(x - half_width)), str(checked(x + half_width))] for x in centre
            ],
            "angle_interval": [str(TAU - half_width), str(TAU + half_width)],
        },
        "owner0_target_rows": target,
        "owner0_owned": finite.serial(q0),
        "all_original_rows_checked": sum(len(rows) for rows in original.values()),
        "all_foreign_rows_conditioned": sum(len(rows) for rows in conditional.values()),
        "input_vertices_parsed": counter[0],
        "work": dict(work),
        "context_retained_pieces": work["retained_conditional_pieces"]
        - work["context_piece_baseline"],
        "recovery": recovery,
        "owned_groups": {str(o): finite.serial(group) for o, group in groups.items()},
        "conditional_geometry_assurance": {
            "intermediate_polygons_serialized": False,
            "every_source_piece_accounted": True,
            "all_required_clips_or_exact_whole_piece_fastpaths_reconstructed": True,
            "source_piece_array_fields": [
                "source_piece_index",
                "whole_piece_outside_facet_or_null",
                "local_to_row_aliases",
                "facet_to_local_aliases_or_null",
            ],
            "all_facet_indices_implicit_in_array_order": True,
            "geometry_hash_used_instead_of_arithmetic": False,
        },
        "conditional_rows": {
            str(o): [
                {
                    **{k: v for k, v in row.items() if k != "pieces"},
                    "domain": finite.serial(row["domain"]),
                    "conditional_polygon_coordinates_serialized": False,
                }
                for row in rows
            ]
            for o, rows in conditional.items()
        },
    }


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
        "complete frozen label/owner roster differs",
    )
    counter = [0]
    original = {}
    core_cache: dict[tuple[Q, Q], list[Point]] = {}
    for owner in sorted(roles.values()):
        raw = cells[str(owner)]
        parent.closed_rows(raw, owner, 32 if owner == 12 else 64, reference_context)
        original[owner] = [parent.row_domain(row, counter, deadline, core_cache) for row in raw]
        require(
            any(r["domain"] for r in original[owner]),
            "original endpoint calibration all-empty owner",
        )
    endpoint = parent.endpoint_control(roster, original, roles, deadline)
    work = new_work()
    contexts: list[dict[str, Any]] = []
    for half_width in (Q(0), HALF_WIDTH):
        try:
            context = condition_context(
                cells, original, centre, counter, work, deadline, half_width=half_width
            )
        except IncompleteError as exc:
            raise ContextIncompleteError(
                str(exc),
                {
                    "completed_contexts": contexts,
                    "unfinished_context_half_width": str(half_width),
                    "point_guard_exclusion_candidate": bool(
                        contexts and contexts[0]["closure"]
                    ),
                    "partial_custody_recheck_complete": False,
                    "work": dict(work),
                },
            ) from exc
        contexts.append(context)
        if half_width == 0 and context["closure"] is None:
            break
    regional = len(contexts) == 2 and contexts[1]["closure"] is not None
    point = contexts[0]["closure"] is not None
    try:
        tick(deadline)
    except IncompleteError as exc:
        raise ContextIncompleteError(
            str(exc),
            {
                "completed_contexts": contexts,
                "point_guard_exclusion_candidate": point,
                "partial_custody_recheck_complete": False,
                "work": dict(work),
            },
        ) from exc
    selected = contexts[-1]
    return {
        **{
            key: value
            for key, value in selected.items()
            if key
            not in {
                "status",
                "criterion_met",
                "declared_guard_exclusion_proved",
                "closure",
                "point_guard_exclusion_proved",
                "work",
            }
        },
        "status": "closed_guard_exclusion"
        if regional
        else "fixed_witness_only"
        if point
        else "criterion_missed",
        "criterion_met": regional,
        "declared_guard_exclusion_proved": regional,
        "closure": contexts[1]["closure"] if regional else None,
        "point_guard_excluded": point,
        "point_guard_exclusion_proved": point,
        "declared_primary_guard": {
            "half_width": str(HALF_WIDTH),
            "centre_box": [
                [str(checked(x - HALF_WIDTH)), str(checked(x + HALF_WIDTH))] for x in centre
            ],
            "angle_interval": [str(TAU - HALF_WIDTH), str(TAU + HALF_WIDTH)],
        },
        "point_closure": contexts[0]["closure"],
        "contexts": contexts,
        "regional_context_started": len(contexts) == 2,
        "regional_skip_reason": "complete_point_miss_monotonic_inclusion"
        if not point
        else None,
        "original_reconstruction_shared": True,
        "original_endpoint_control": {
            "all17_retained": True,
            "witnesses": endpoint,
            "family_disjoint": True,
            "conditional_endpoint_retention_required": False,
        },
        "work": dict(work),
    }


def constants() -> dict[str, Any]:
    return {
        "primary_half_width": str(HALF_WIDTH),
        "context_half_widths": ["0", str(HALF_WIDTH)],
        "work_counters_cumulative_across_contexts": True,
        "retained_piece_cap_scope": "per_context",
        "tau": str(TAU),
        "margin": str(MARGIN),
        "guaranteed_seed_radius": "520191/2097152",
        "original_row_pieces": parent.ROW_PIECE_LIMIT,
        "original_vertices": parent.INPUT_VERTICES,
        "geometry_bits": finite.BIT_LIMIT,
        "endpoint_input_bits": parent.ENDPOINT_INPUT_BITS,
        "endpoint_arithmetic_bits": parent.ENDPOINT_ARITHMETIC_BITS,
        "row_conditional_pieces": CONDITIONAL_ROW_LIMIT,
        "conditional_pieces_per_context": CONDITIONAL_PIECE_LIMIT,
        "maximum_contexts": 2,
        "generated_clip_output_vertices": GENERATED_VERTEX_LIMIT,
        "conditional_domain_vertices": DOMAIN_LIMIT,
        "owner0_partner_core_vertices": OWNER0_LIMIT,
        "common_owned_vertices": OWNED_LIMIT,
        "forbidden_facets": FACET_LIMIT,
        "raw_minkowski_vertex_products": MINKOWSKI_PRODUCT_LIMIT,
        "recovery_MIN_support_products": RECOVERY_SUPPORT_LIMIT,
        "outside_fastpath_MIN_support_products": FAST_SUPPORT_LIMIT,
        "strict_verification_vertex_pairs": STRICT_PAIR_LIMIT,
        "strict_quadratic_checks": STRICT_CHECK_LIMIT,
        "intersection_output_vertices": INTERSECTION_LIMIT,
        "output_bytes": OUTPUT_LIMIT,
    }


def scope() -> dict[str, bool]:
    return {
        **parent.scope(),
        "new_producer_run": False,
        "conditional_endpoint_retention_proved": False,
    }


def generate(document: dict[str, Any], *, deadline: float) -> dict[str, Any]:
    require(document["schema"] == DESCRIPTOR_SCHEMA, "guard-owned descriptor schema differs")
    frozen = finite.canonical(document)
    held: dict[Path, tuple[str, int]] = {}
    final, custody, roster, centre = parent.intake(
        copy.deepcopy(document) | {"schema": parent.DESCRIPTOR_SCHEMA}, held, deadline
    )
    gate = finite.read_json(
        finite.retained_path(document["parent_descriptor"]), parent.JSON_LIMIT
    )[1]
    result = construct(
        final["cells"],
        gate["label_to_owner"],
        roster,
        centre,
        deadline=deadline,
        reference_context=custody["typed_reference_context"],
    )
    try:
        for path, (expected, ceiling) in held.items():
            require(
                finite.digest(path, ceiling, deadline) == expected, "guard-owned inputs changed"
            )
        require(finite.canonical(document) == frozen, "guard-owned descriptor changed")
        tick(deadline)
    except IncompleteError as exc:
        raise ContextIncompleteError(
            str(exc),
            {
                "completed_contexts": result["contexts"],
                "point_guard_exclusion_candidate": result["point_guard_excluded"],
                "partial_custody_recheck_complete": False,
                "work": result["work"],
            },
        ) from exc
    return {
        "schema": SCHEMA,
        "accepted_inputs": copy.deepcopy(document),
        "container": standing.CenteredContainer(cases.U, cases.V).record(),
        "parent_custody": {
            k: copy.deepcopy(custody[k])
            for k in (
                "h290_receipt",
                "h290_receipt_sha256",
                "seed_sha256",
                "node_sha256",
                "compressed_sha256",
                "steps",
                "typed_reference_context",
                "accepted_parent_premises",
            )
        },
        "matched_owned_point_witness": {
            "centre": list(map(str, centre)),
            "tau": str(TAU),
            "freshly_checked": True,
        },
        "constants": constants(),
        "mathematical_assurance": (
            "finite exact reconstruction; guard-conditioned composition is a sole-Astra hand "
            "implication, not independently mathematically reviewed or machine-formalized"
        ),
        "resource_assurance": {
            "conditional_cover_clip_counter_scope": [
                "owner0_restricted_angle_wall",
                "owner0_position_box",
                "foreign_outside_facets",
            ],
            "conditional_cover_clip_counter_excludes": [
                "unconditional_original_wall_preflight",
                "Q0_clips",
                "common_K_clips",
            ],
            "trusted_intersection_internal_operations_capped": False,
            "unreduced_integer_product_bit_cap": False,
            "required": "outer wall ceiling and sampled current RSS per live owned process",
        },
        **scope(),
        **result,
    }


def check(
    document: dict[str, Any], certificate: dict[str, Any], *, deadline: float
) -> dict[str, Any]:
    expected = parent.feasible.witness.payload(certificate)
    require(
        expected == generate(document, deadline=deadline),
        "fresh guard-owned reconstruction differs",
    )
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
                name == prefix or name.startswith(prefix + ".")
                for name in sys.modules
                for prefix in (*finite.FORBIDDEN, "devtools.produce_n17_conditional_owned_hull")
            ),
            "producer/kernel/root import in guard-owned checker",
        )
        raw, document = finite.read_json(args.descriptor, parent.JSON_LIMIT)
        if args.certificate:
            saved, certificate = finite.read_json(args.certificate, OUTPUT_LIMIT)
            result = check(document, certificate, deadline=deadline)
            require(
                finite.read_json(args.certificate, OUTPUT_LIMIT)[0] == saved,
                "guard-owned certificate bytes changed",
            )
        else:
            result = generate(document, deadline=deadline)
        require(
            finite.read_json(args.descriptor, parent.JSON_LIMIT)[0] == raw,
            "guard-owned descriptor bytes changed",
        )
    except IncompleteError as exc:
        result = {
            **(exc.observations if isinstance(exc, ContextIncompleteError) else {}),
            "schema": SCHEMA,
            "status": "incomplete",
            "error": str(exc),
            "criterion_met": False,
            "declared_guard_exclusion_proved": False,
            "point_guard_exclusion_proved": False,
            "verification_passed": False,
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
            "declared_guard_exclusion_proved": False,
            "point_guard_exclusion_proved": False,
            "verification_passed": False,
        }
    result.update(scope())
    result.update(
        provenance=provenance(
            Path(__file__),
            Path(parent.__file__),
            Path(sat.__file__),
            Path(cast(str, cases.__file__)),
            Path(cast(str, finite.__file__)),
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
            "point_guard_exclusion_candidate": result.get(
                "point_guard_excluded", result.get("point_guard_exclusion_candidate", False)
            ),
            "completed_context_half_widths": [
                c["guard"]["half_width"]
                for c in result.get("contexts", result.get("completed_contexts", []))
            ],
            "schema": SCHEMA,
            "status": "incomplete",
            "error": "guard-owned output byte or wall ceiling",
            "criterion_met": False,
            "declared_guard_exclusion_proved": False,
            "point_guard_exclusion_proved": False,
            "verification_passed": False,
            **scope(),
        }
        text = retained_json.dumps(result, sort_keys=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text)
    return (
        0
        if result["status"]
        in ("closed_guard_exclusion", "criterion_missed", "fixed_witness_only")
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
