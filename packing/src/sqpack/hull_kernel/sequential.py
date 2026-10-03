"""The sequential mode-A grammar: refinement, owner revisits, both closures and stalls.

Lifted from the frozen sequential generic checker
(`packing/devtools/check_n11_generic_sequential.py`) and its refinement helper
(`packing/devtools/n11_nonfield_refinement.py`), with n11's constants read from the
frame. Against the fresh grammar of `node`, a step here

* may revisit an owner, and its rows may refine the owner's accepted rows: each new row
  cites one accepted predecessor whose interval contains it, and together the new rows
  partition `[0, 1]` (`complete_refinement`);
* may carry self-hull cuts on a row, each admitted as necessary for every pose;
* states its input domain as any convex polygon containing the required legal domain;
* closes an empty legal row with empty outputs, and covers a point or segment domain by
  the closed degenerate cover.

What the frozen checker has and this module refuses: partner pose covers, collision
regions, centre-plane constraints and incomplete steps.

Closure is derived here, after every complete step, never read from the producer:
`all_parent_poses_forbidden` when the stepping owner's rows all have empty residuals, and
`owned_hulls_intersect` when its owned hull meets another owner's (a common point lies
strictly inside both squares in every surviving pose). The node's declared
`contradiction` must equal the derived one, or be absent with `closed` false; a node
that never closes is a stall, reported with every owner's residual extents.
"""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from sqpack.hull_kernel.collision import (
    FacetCache,
    PreparedRow,
    as_prepared,
    cached_universal_collision,
    prepare_rows,
    self_hull_cuts,
)
from sqpack.hull_kernel.covers import (
    closed_degenerate_cover,
    convex_halfplanes,
    fast_union_cover,
    indexed_union_cover,
)
from sqpack.hull_kernel.frame import Frame
from sqpack.hull_kernel.geometry import Budget, Polygon, area2, intersect, require
from sqpack.hull_kernel.induction import (
    common_core_planes,
    convex,
    encode,
    forbidden_regions,
    hull,
    same,
    strict_core,
    wall_lines,
)
from sqpack.hull_kernel.node import (
    Row,
    RowResult,
    Seed,
    admit_final_state,
    admit_header,
    compressed,
    compression_points,
    node_mask,
    points,
    remaining,
)
from sqpack.hull_kernel.rational import Q
from sqpack.hull_kernel.sweep import exact_union_cover

COVERS = {
    "reference": exact_union_cover,
    "fast": fast_union_cover,
    "indexed": indexed_union_cover,
}
# The replay's memo of collision facets by pair of cores is emptied at a step's start once
# it holds more pairs than this. Uniform rows give at most `bins` squared pairs, which a
# node keeps throughout; adaptive rows give many more, and the memo then holds at most this
# many and one step's. The facets are a pure function of the two cores, so emptying the
# memo recomputes them and changes no check.
FACET_MEMO_PAIRS = 1 << 15


def _key(value: object) -> str:
    require(isinstance(value, dict), "pose row reference")
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def complete_refinement(
    proposed: Sequence[Mapping[str, Any]],
    accepted: Sequence[Mapping[str, Any]],
    *,
    max_rows: int,
) -> list[Mapping[str, Any]]:
    """Return each proposed row's exact accepted predecessor or refuse the partition."""
    require(type(max_rows) is int and max_rows > 0, "refinement row ceiling")
    require(0 < len(proposed) <= max_rows and bool(accepted), "refinement row inventory")
    by_ref = {_key(row["reference"]): row for row in accepted}
    require(len(by_ref) == len(accepted), "duplicate accepted row reference")
    cursor = Q()
    predecessors: list[Mapping[str, Any]] = []
    for row in proposed:
        lo, hi = (Q(value) for value in row["interval"])
        require(cursor == lo and lo < hi <= 1, "refinement angular gap or overlap")
        cursor = hi
        prior = by_ref.get(_key(row["prior_reference"]))
        require(prior is not None, "refinement predecessor is not accepted")
        assert prior is not None
        old_lo, old_hi = (Q(value) for value in prior["interval"])
        require(old_lo <= lo and hi <= old_hi, "refinement crossed predecessor interval")
        predecessors.append(prior)
    require(cursor == 1, "refinement angular cover incomplete")
    return predecessors


def check_row(
    frame: Frame,
    source: Mapping[str, Any],
    step: Mapping[str, Any],
    row_index: int,
    *,
    prior: Mapping[int, Polygon],
    predecessor: Mapping[str, Any],
    budget: Budget,
    cover: str = "reference",
    partners: Mapping[int, Sequence[PreparedRow | tuple[Polygon, Polygon]]] | None = None,
    facets: FacetCache | None = None,
) -> RowResult:
    """One closed row of the sequential grammar, from its accepted predecessor.

    A collision region names an admitted partner; it is accepted only if every vertex lies
    in the row's legal domain and, for every live row `(D_r, Q_r)` of that partner's
    complete pose cover, in every facet `n.p <= h + min over D_r of n.y` of `Q_r - Q_i`
    (`cached_universal_collision`, the memoised form of `integer_universal_collision`):
    square `i` centred there overlaps the partner in every pose the partner can still
    take. `facets` is the node's memo of facets by pair of cores; a fresh one is used
    when none is given.
    """
    row = step["rows"][row_index]
    owner = step["owner"]
    require(row["prior_reference"] == predecessor["reference"], "row predecessor reference")
    lo, hi = (Q(value) for value in row["interval"])
    old_lo, old_hi = (Q(value) for value in predecessor["interval"])
    require(old_lo <= lo < hi <= old_hi, "row interval escaped predecessor")
    supplied = [
        (Q(item["normal"][0]), Q(item["normal"][1]), Q(item["upper"]))
        for item in row.get("self_hull_cuts", [])
    ]
    cuts = self_hull_cuts(frame, supplied, prior[owner], lo, hi) if supplied else []
    required = intersect(
        hull(points(predecessor["outer_domain"])), wall_lines(frame, lo, hi) + cuts
    )
    reference = {
        "kind": "phase3",
        "node": source["node_id"],
        "step": step["index"],
        "row": row_index,
    }
    require(row["reference"] == reference, "row reference")
    empty_row: Row = {
        "interval": [str(lo), str(hi)],
        "reference": reference,
        "outer_domain": [],
        "residual_polygons": [],
    }
    if not required:
        require(
            row["residual_polygons"] == []
            and row["collision_regions"] == []
            and row["common_core_halfplanes"] == []
            and row["outer_bounds"] == []
            and row["outer_domain"] == [],
            "empty legal row has an unsupported output",
        )
        remaining(budget)
        return {"events": 0, "probes": 0, "edge_segments": 0}, [], [], empty_row
    proposal = convex(points(row["input_domain"]))
    require(hull(required + proposal) == proposal, "row input domain excludes a legal pose")
    domain = required
    core = convex(points(row["core_vertices"]))
    strict_core(frame, core, lo, hi)
    collisions: list[Polygon] = []
    collision_checks = 0
    memo: FacetCache = {} if facets is None else facets
    for item in row["collision_regions"]:
        partner = item["partner"]
        require(partners is not None and partner in partners, "collision partner not admitted")
        assert partners is not None
        region = convex(points(item["vertices"]))
        collision_checks += cached_universal_collision(
            core, domain, as_prepared(partners[partner]), region, budget=budget, facets=memo
        )
        collisions.append(region)
    forbidden = [region for region in forbidden_regions(prior, owner, core) if region]
    residual = [convex(points(poly)) for poly in row["residual_polygons"]]
    regions = forbidden + collisions + residual
    coverage = (
        COVERS[cover](domain, regions, budget=budget)
        if area2(domain) > 0
        else closed_degenerate_cover(domain, regions, budget=budget)
    )
    coverage = {
        **coverage,
        "collision_regions": len(collisions),
        "collision_checks": collision_checks,
    }
    vertices = [point for poly in residual for point in poly]
    expected = common_core_planes(core, vertices)
    actual = [
        (Q(item["normal"][0]), Q(item["normal"][1]), Q(item["upper"]))
        for item in row["common_core_halfplanes"]
    ]
    require(set(actual) == set(expected), "common owned-core facets")
    support = [
        (Q(item["normal"][0]), Q(item["normal"][1]), Q(item["upper"]))
        for item in row["outer_bounds"]
    ]
    require(
        all(nx * x + ny * y <= upper for x, y in vertices for nx, ny, upper in support),
        "support bound excludes residual vertex",
    )
    if vertices:
        trusted_outer = hull(intersect(frame.world(owner), support))
        require(same(trusted_outer, points(row["outer_domain"])), "row outer")
    else:
        require(not support and not row["outer_domain"], "empty residual has support")
        trusted_outer = []
    remaining(budget)
    accepted = {
        "interval": [str(lo), str(hi)],
        "reference": reference,
        "outer_domain": encode(trusted_outer),
        "residual_polygons": [encode(poly) for poly in residual],
    }
    return coverage, vertices, actual, accepted


def hulls_meet(first: Polygon, second: Polygon) -> Polygon:
    """A common point of two closed convex hulls (points and segments allowed), or []."""
    if not first or not second:
        return []
    common = intersect(list(first), convex_halfplanes(second))
    if not common:
        return []
    witness = common[0]
    for nx, ny, upper in convex_halfplanes(first) + convex_halfplanes(second):
        require(nx * witness[0] + ny * witness[1] <= upper, "hull meeting witness escapes")
    return [witness]


def owner_extents(
    frame: Frame, owner: int, rows: Sequence[Row], group: Polygon
) -> dict[str, Any]:
    """Live rows, live angle width, the residual's physical box and the owned hull."""
    live = [row for row in rows if row["residual_polygons"]]
    vertices = [
        (Q(x) / frame.scale, Q(y) / frame.scale)
        for row in live
        for polygon in row["residual_polygons"]
        for x, y in polygon
    ]
    width = sum((Q(row["interval"][1]) - Q(row["interval"][0]) for row in live), Q())
    box = (
        None
        if not vertices
        else [
            [str(min(x for x, _ in vertices)), str(max(x for x, _ in vertices))],
            [str(min(y for _, y in vertices)), str(max(y for _, y in vertices))],
        ]
    )
    return {
        "owner": owner,
        "cell": frame.cell_names[owner],
        "rows": len(rows),
        "live_rows": len(live),
        "live_half_angle_width": str(width),
        "residual_box_physical": box,
        "residual_box_extent": (
            None
            if box is None
            else [
                str(Q(box[0][1]) - Q(box[0][0])),
                str(Q(box[1][1]) - Q(box[1][0])),
            ]
        ),
        "owned_hull_vertices": len(group),
        "owned_hull_area2_physical": str(area2(group) / frame.scale**2),
    }


def admit_partner_covers(
    frame: Frame,
    step: Mapping[str, Any],
    rows: Mapping[int, list[Row]],
    *,
    mask: Sequence[int],
) -> dict[int, list[tuple[Polygon, Polygon]]]:
    """Each named partner's complete pose cover, row for row from its accepted state.

    A cover row cites the partner's accepted row by reference and interval; its domain is
    the hull of that row's residual vertices, which holds every centre the partner can
    take at those angles; its core is proved strictly inside the partner's square at every
    angle of the row. Rows with no residual are empty (no pose there). A partner with no
    live row would be a closure already, so an empty cover is refused, never quantified.
    """
    covers = step["prior_partner_pose_covers"]
    require(isinstance(covers, dict), "partner covers must be a mapping")
    admitted: dict[int, list[tuple[Polygon, Polygon]]] = {}
    for key, given in covers.items():
        partner = int(key)
        require(
            str(partner) == key and partner in mask and partner != step["owner"],
            "partner cover names no other owner",
        )
        accepted = rows[partner]
        require(isinstance(given, list) and len(given) == len(accepted), "partner cover rows")
        live: list[tuple[Polygon, Polygon]] = []
        for item, row in zip(given, accepted, strict=True):
            require(
                item["reference"] == row["reference"] and item["interval"] == row["interval"],
                "partner cover row differs from the accepted row",
            )
            vertices = [
                vertex for polygon in row["residual_polygons"] for vertex in points(polygon)
            ]
            if not vertices:
                require(
                    item["domain"] == [] and item["core"] == [], "empty partner row has a pose"
                )
                continue
            domain = hull(vertices)
            require(same(points(item["domain"]), domain), "partner cover domain differs")
            lo, hi = (Q(value) for value in row["interval"])
            core = convex(points(item["core"]))
            strict_core(frame, core, lo, hi)
            live.append((domain, core))
        require(bool(live), "an empty partner cover is a closure, not a quantifier")
        admitted[partner] = live
    return admitted


@dataclass
class SequentialTrace:
    """What the replay accepted: per-step coverage, the state, closure or stall extents."""

    steps: list[dict[str, Any]] = field(default_factory=list)
    groups: dict[int, Polygon] = field(default_factory=dict)
    rows: dict[int, list[Row]] = field(default_factory=dict)
    closure: dict[str, Any] | None = None
    extents: list[dict[str, Any]] = field(default_factory=list)


def derived_closure(
    owner: int, step_index: int, groups: Mapping[int, Polygon], rows: Mapping[int, list[Row]]
) -> dict[str, Any] | None:
    if all(not row["residual_polygons"] for row in rows[owner]):
        return {"kind": "all_parent_poses_forbidden", "owner": owner, "step": step_index}
    for other, group in sorted(groups.items()):
        if other != owner and (witness := hulls_meet(groups[owner], group)):
            return {
                "kind": "owned_hulls_intersect",
                "owners": sorted((owner, other)),
                "step": step_index,
                "point": [str(witness[0][0]), str(witness[0][1])],
            }
    return None


def replay_sequential(
    frame: Frame,
    source: Mapping[str, Any],
    seed: Seed,
    *,
    mask: Sequence[int] | None = None,
    mask_index: int | None = None,
    seed_sha256: str,
    budget: Budget,
    cover: str = "reference",
) -> SequentialTrace:
    """Replay every step; closure is derived, and a node without one is a reported stall."""
    mask = node_mask(frame, mask_index=mask_index, mask=mask)
    admit_header(frame, source, seed, mask_index=mask_index, mask=mask, seed_sha256=seed_sha256)
    groups, rows = dict(seed.groups), dict(seed.rows)
    trace = SequentialTrace()
    steps = source["steps"]
    facets: FacetCache = {}
    for step_index, step in enumerate(steps):
        require(trace.closure is None, "a step follows the node's closure")
        if len(facets) > FACET_MEMO_PAIRS:
            facets.clear()
        owner = step["owner"]
        require(
            type(step["index"]) is int and step["index"] == step_index and owner in mask,
            "step owner/order",
        )
        require(
            step["allowed_half_angle"] == ["0", "1"] and step["complete"] is True,
            "unsupported angle or incomplete step",
        )
        require(
            set(step["prior_owned_hulls"]) == set(map(str, mask))
            and all(same(points(step["prior_owned_hulls"][str(i)]), groups[i]) for i in mask),
            "step previous accepted state",
        )
        predecessors = complete_refinement(step["rows"], rows[owner], max_rows=budget.max_nodes)
        partners = admit_partner_covers(frame, step, rows, mask=mask)
        prepared = {partner: prepare_rows(live) for partner, live in partners.items()}
        results = [
            check_row(
                frame,
                source,
                step,
                row_index,
                prior=groups,
                predecessor=predecessor,
                budget=budget,
                cover=cover,
                partners=prepared,
                facets=facets,
            )
            for row_index, predecessor in enumerate(predecessors)
        ]
        all_vertices = [point for result in results for point in result[1]]
        all_planes = [plane for result in results for plane in result[2]]
        kernel = points(step["common_owned_kernel"])
        for point in kernel:
            require(
                all(0 <= coordinate <= frame.length for coordinate in point)
                and all(nx * point[0] + ny * point[1] <= upper for nx, ny, upper in all_planes),
                "promoted point lacks full-row ownership proof",
            )
        if all_vertices and (groups[owner] or kernel):
            groups[owner] = (
                hull(compression_points(step, groups[owner], kernel))
                if step["inner_grid_compression"].get("mode") == "replace"
                else compressed(step, groups[owner], kernel)
            )
        else:
            require("inner_grid_compression" not in step, "nothing to promote, yet compression")
        rows[owner] = [result[3] for result in results]
        trace.steps.append(
            {
                "step": step_index,
                "owner": owner,
                "rows": len(results),
                "events": sum(result[0]["events"] for result in results),
                "probes": sum(result[0]["probes"] for result in results),
                "collision_regions": sum(
                    result[0].get("collision_regions", 0) for result in results
                ),
                "partners": sorted(partners),
                "live_rows": sum(1 for result in results if result[3]["residual_polygons"]),
                "owned_hull_vertices": len(groups[owner]),
            }
        )
        trace.closure = derived_closure(owner, step_index, groups, rows)
    admit_final_state(frame, source, groups, rows, mask_index=mask_index, mask=mask)
    require(
        source["contradiction"] == trace.closure
        and source["closed"] is (trace.closure is not None)
        and source["terminal"] is (trace.closure is not None),
        "declared closure differs from the derived one",
    )
    require(
        source["mask_exclusion_proved"] is False
        and source["global_optimality_proved"] is False,
        "source claim fields changed",
    )
    trace.groups, trace.rows = groups, rows
    trace.extents = [owner_extents(frame, owner, rows[owner], groups[owner]) for owner in mask]
    return trace
