"""The mode-A node grammar: a wall seed, sequential owner updates and a terminal node.

Copies of the seed, header, row, compression and replay functions of the frozen
fresh-wall generic checker (`packing/devtools/check_n11_generic_fresh.py`) with n11's
mask, bins, step count, owner order and contradiction lifted out as arguments or left
to the caller to pin. The JSON grammar is n11's published one:

* a seed `generic_wall_seed_v1` holds, per owner, owned points (`groups`) and `bins`
  uniform rows, each the owner's cell clipped by the row's legal box with that domain as
  its only residual;
* a node `exact_generic_owned_hull_v1` holds `initial`, `steps[]` and `final_state`; a
  step updates one owner once, every row citing the predecessor row on the same
  interval, then promotes `common_owned_kernel` by exact convex-combination compression;
* a node closes by `all_parent_poses_forbidden` when its contradiction owner's rows all
  have empty residuals.

What this checker refuses rather than reads: a parent or constraints (branch
predicates), a guard, partner pose covers, collision regions, a restricted angle domain,
an owner revisited, and rows that are not the seed's uniform partition. Those are the
parts of the grammar that case 2095 does not use.
"""

from __future__ import annotations

import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from sqpack.hull_kernel.frame import Frame
from sqpack.hull_kernel.geometry import (
    Budget,
    Halfplane,
    IncompleteError,
    Point,
    Polygon,
    area2,
    intersect,
    require,
)
from sqpack.hull_kernel.induction import (
    common_core_planes,
    convex,
    convex_combination,
    encode,
    forbidden_regions,
    hull,
    same,
    strict_core,
    wall_lines,
)
from sqpack.hull_kernel.ownership import ownership
from sqpack.hull_kernel.rational import Q
from sqpack.hull_kernel.sweep import exact_union_cover

type Row = dict[str, Any]
type RowResult = tuple[dict[str, int], Polygon, list[Halfplane], Row]


def remaining(budget: Budget) -> None:
    if time.monotonic() >= budget.deadline:
        raise IncompleteError("generic pilot wall ceiling expired")


def parse_point(value: Any) -> Point:
    require(isinstance(value, list) and len(value) == 2, "expected a two-coordinate point")
    return Q(value[0]), Q(value[1])


def points(value: Any) -> Polygon:
    require(isinstance(value, list), "polygon must be a list")
    return [parse_point(point) for point in value]


def node_mask(
    frame: Frame, *, mask_index: int | None = None, mask: Sequence[int] | None = None
) -> list[int]:
    """A node's owner cells: a frame state by index, explicit cells, or both agreeing.

    n11's nodes name a canonical state (`mask_index`); an n17 sub-pattern names its cells
    and has no index (`mask_index` None), since it is a partial mask.
    """
    if mask is None:
        require(mask_index is not None, "a node needs a mask or a mask index")
        assert mask_index is not None
        return list(frame.representatives[mask_index])
    cells = list(mask)
    require(
        bool(cells)
        and cells == sorted(set(cells))
        and all(0 <= cell < len(frame.cells) for cell in cells),
        "a mask is a sorted list of distinct cells",
    )
    require(
        mask_index is None or list(frame.representatives[mask_index]) == cells,
        "the mask differs from the indexed state",
    )
    return cells


def _same_index(value: object, mask_index: int | None) -> bool:
    return value == mask_index and (mask_index is None or type(value) is int)


@dataclass
class Seed:
    """The proved starting state: owned hulls, normalised rows and the ownership proofs."""

    groups: dict[int, Polygon]
    rows: dict[int, list[Row]]
    proofs: list[dict[str, Any]] = field(default_factory=list)


def admit_seed(
    frame: Frame,
    seed: Mapping[str, Any],
    *,
    mask_index: int | None = None,
    mask: Sequence[int] | None = None,
    bins: int,
    budget: Budget,
    owners: Sequence[int] | None = None,
    allow_empty_groups: bool = False,
) -> Seed:
    """Prove every seed point owned and every seed row the owner's whole legal domain.

    `owners` restricts the check to some owners, for a partial replay. With
    `allow_empty_groups` an owner may start owning nothing (n17's axis interior cells,
    whose least enclosing radius exceeds one half, own no point from the cell alone);
    n11's grammar keeps the frozen requirement of at least one point.
    """
    mask = node_mask(frame, mask_index=mask_index, mask=mask)
    require(seed.get("schema") == "generic_wall_seed_v1", "wrong seed schema")
    require(_same_index(seed.get("mask_index"), mask_index), "seed ID")
    require(seed.get("mask") == mask, "seed mask changed")
    require(Q(seed["U"]) == frame.cap and Q(seed["B"]) == frame.scale, "seed U/B")
    require(type(seed.get("bins")) is int and seed["bins"] == bins > 0, "seed bins")
    require(set(seed["groups"]) == set(map(str, mask)), "seed group inventory")
    require(set(seed["cells"]) == set(map(str, mask)), "seed row-owner inventory")
    world = [frame.world(cell) for cell in range(len(frame.cells))]
    require(len(seed["world"]) == len(world), "seed world inventory")
    require(
        all(
            same(points(given), actual)
            for given, actual in zip(seed["world"], world, strict=True)
        ),
        "seed world differs from the frame's cells",
    )
    result = Seed({}, {})
    for owner in mask if owners is None else owners:
        require(owner in mask, "owner outside the seed mask")
        group = points(seed["groups"][str(owner)])
        require(
            (group or allow_empty_groups) and len(set(group)) == len(group),
            "seed group has duplicate/empty points",
        )
        for index, point in enumerate(group):
            remaining(budget)
            proof = ownership(frame, owner, point, budget=budget)
            result.proofs.append({"owner": owner, "point_index": index, **proof})
        result.groups[owner] = hull(group)
        owner_rows = seed["cells"][str(owner)]
        require(len(owner_rows) == bins, "seed angular inventory changed")
        normalized: list[Row] = []
        for index, row in enumerate(owner_rows):
            remaining(budget)
            lo, hi = (Q(t) for t in row["interval"])
            require((lo, hi) == (Q(index, bins), Q(index + 1, bins)), "seed row gap/overlap")
            domain = intersect(world[owner], wall_lines(frame, lo, hi))
            require(same(points(row["outer_domain"]), domain), "seed legal domain differs")
            require(row["outer_bounds"] == [], "unexpected seed support restriction")
            expected = [domain] if domain else []
            actual = [points(value) for value in row["residual_polygons"]]
            require(
                len(actual) == len(expected)
                and all(same(a, e) for a, e in zip(actual, expected, strict=True)),
                "seed residual differs from complete legal domain",
            )
            require(
                row["reference"] == {"kind": "wall_seed", "owner": owner, "row": index},
                "seed row reference changed",
            )
            normalized.append(
                {
                    "interval": [str(lo), str(hi)],
                    "reference": row["reference"],
                    "outer_domain": encode(domain),
                    "residual_polygons": [encode(poly) for poly in expected],
                }
            )
        result.rows[owner] = normalized
    return result


def admit_header(
    frame: Frame,
    source: Mapping[str, Any],
    seed: Seed,
    *,
    mask_index: int | None = None,
    mask: Sequence[int] | None = None,
    seed_sha256: str,
) -> None:
    """The node's premises: no ancestry, constraints or guard, and the proved seed."""
    mask = node_mask(frame, mask_index=mask_index, mask=mask)
    require(source.get("schema") == "exact_generic_owned_hull_v1", "wrong terminal schema")
    require(
        source.get("parent") is None and source.get("constraints") == [], "unsupported ancestry"
    )
    require(source.get("guard_source") is None, "guarded source unsupported")
    require(_same_index(source.get("mask_index"), mask_index), "source ID")
    require(source.get("mask") == mask, "source mask changed")
    require(Q(source["U"]) == frame.cap and Q(source["B"]) == frame.scale, "source U/B")
    require(source["source"]["sha256"] == seed_sha256, "terminal seed binding")
    require(source["initial"]["groups"] and source["steps"], "missing initial state/steps")
    require(
        set(source["initial"]["groups"]) == set(map(str, mask))
        and set(source["initial"]["cell_references"]) == set(map(str, mask)),
        "source initial owner inventory changed",
    )
    require(
        all(
            same(points(source["initial"]["groups"][str(owner)]), seed.groups[owner])
            for owner in mask
        ),
        "source initial owner state differs from proved seed",
    )
    require(
        all(
            source["initial"]["cell_references"][str(owner)]
            == [row["reference"] for row in seed.rows[owner]]
            for owner in mask
        ),
        "source initial row references differ from proved seed",
    )


def check_row(
    frame: Frame,
    source: Mapping[str, Any],
    step: Mapping[str, Any],
    row: Mapping[str, Any],
    *,
    row_index: int,
    owner: int,
    bins: int,
    prior: Mapping[int, Polygon],
    predecessor: Mapping[str, Any],
    budget: Budget,
) -> RowResult:
    """One closed row: inherited domain, strict core, cover, planes and support domain."""
    require(row["prior_reference"] == predecessor["reference"], "wrong predecessor row")
    lo, hi = (Q(t) for t in row["interval"])
    require(
        (lo, hi) == (Q(row_index, bins), Q(row_index + 1, bins)),
        "row interval gap/overlap",
    )
    require([lo, hi] == [Q(t) for t in predecessor["interval"]], "row predecessor interval")
    domain = intersect(hull(points(predecessor["outer_domain"])), wall_lines(frame, lo, hi))
    require(same(points(row["input_domain"]), domain), "row input domain differs")
    require(area2(domain) > 0, "degenerate generic domain needs separate proof")
    core = convex(points(row["core_vertices"]))
    strict_core(frame, core, lo, hi)
    require(row["collision_regions"] == [], "unsupported collision region")
    forbidden = forbidden_regions(prior, owner, core)
    residual = [convex(points(value)) for value in row["residual_polygons"]]
    coverage = exact_union_cover(domain, forbidden + residual, budget=budget)
    require(
        row["reference"]
        == {
            "kind": "phase3",
            "node": source["node_id"],
            "step": step["index"],
            "row": row_index,
        },
        "row reference changed",
    )
    vertices = [point for polygon in residual for point in polygon]
    expected_planes = common_core_planes(core, vertices)
    actual_planes = [
        (Q(item["normal"][0]), Q(item["normal"][1]), Q(item["upper"]))
        for item in row["common_core_halfplanes"]
    ]
    require(set(actual_planes) == set(expected_planes), "common owned-core facets differ")
    support = [
        (Q(item["normal"][0]), Q(item["normal"][1]), Q(item["upper"]))
        for item in row["outer_bounds"]
    ]
    require(
        all(nx * x + ny * y <= upper for x, y in vertices for nx, ny, upper in support),
        "support bound excludes a residual vertex",
    )
    trusted_outer: Polygon = []
    if vertices:
        trusted_outer = hull(intersect(frame.world(owner), support))
        require(same(trusted_outer, points(row["outer_domain"])), "row support domain differs")
    else:
        require(not support and not row["outer_domain"], "empty residual has a support domain")
    remaining(budget)
    accepted = {
        "interval": [str(lo), str(hi)],
        "reference": row["reference"],
        "outer_domain": encode(trusted_outer),
        "residual_polygons": [encode(polygon) for polygon in residual],
    }
    return coverage, vertices, actual_planes, accepted


def compressed(step: Mapping[str, Any], prior: Polygon, kernel: Polygon) -> Polygon:
    """The owner's new hull: the prior hull and grid points proved convex combinations."""
    return hull(prior + compression_points(step, prior, kernel))


def compression_points(step: Mapping[str, Any], prior: Polygon, kernel: Polygon) -> Polygon:
    """The step's grid points, each proved an exact convex combination of at most three
    vertices of the hull of the prior hull and the promoted kernel."""
    original = hull(prior + kernel)
    require(
        same(points(step["compression_source_hull"]), original),
        "compression source differs from independently accepted owner hull",
    )
    receipt = step["inner_grid_compression"]
    new_points = points(receipt["vertices"])
    witnesses = receipt["witnesses"]
    denominator = receipt["denominator"]
    require(
        type(denominator) is int and denominator > 0 and len(new_points) == len(witnesses) > 0,
        "compression inventory or grid denominator changed",
    )
    require(
        receipt["original_vertices"] == len(original)
        and receipt["retained_vertices"] == len(new_points),
        "compression counts changed",
    )
    for point, witness in zip(new_points, witnesses, strict=True):
        combination = convex_combination(
            original, witness["indices"], [Q(value) for value in witness["weights"]]
        )
        require(combination is not None, "invalid convex-combination witness")
        require(
            all((coordinate * denominator).denominator == 1 for coordinate in point)
            and parse_point(witness["point"]) == point
            and point == combination,
            "compressed point is not a proved convex combination",
        )
    return new_points


@dataclass
class StepTrace:
    owner: int
    rows: list[RowResult]
    group: Polygon


@dataclass
class NodeTrace:
    """Everything the replay accepted, in order, for comparison with another checker."""

    steps: list[StepTrace] = field(default_factory=list)
    groups: dict[int, Polygon] = field(default_factory=dict)
    rows: dict[int, list[Row]] = field(default_factory=dict)
    contradiction: dict[str, Any] = field(default_factory=dict)


def replay_node(
    frame: Frame,
    source: Mapping[str, Any],
    seed: Seed,
    *,
    mask_index: int | None = None,
    mask: Sequence[int] | None = None,
    bins: int,
    budget: Budget,
) -> NodeTrace:
    """Replay every sequential step, the final state and the terminal contradiction."""
    mask = node_mask(frame, mask_index=mask_index, mask=mask)
    state_groups = dict(seed.groups)
    state_rows = dict(seed.rows)
    trace = NodeTrace()
    seen: set[int] = set()
    for step_index, step in enumerate(source["steps"]):
        owner = step["owner"]
        require(
            type(step["index"]) is int
            and step["index"] == step_index
            and owner in mask
            and owner not in seen,
            "generic step order or owner inventory changed",
        )
        require(
            step["allowed_half_angle"] == ["0", "1"]
            and step["prior_partner_pose_covers"] == {},
            "unsupported angle or partner premise",
        )
        require(
            set(step["prior_owned_hulls"]) == set(map(str, mask))
            and all(
                same(points(step["prior_owned_hulls"][str(other)]), state_groups[other])
                for other in mask
            ),
            "step prior does not equal completed predecessor state",
        )
        require(len(step["rows"]) == bins, "step lacks a full closed angle partition")
        results: list[RowResult] = []
        for row_index, row in enumerate(step["rows"]):
            remaining(budget)
            results.append(
                check_row(
                    frame,
                    source,
                    step,
                    row,
                    row_index=row_index,
                    owner=owner,
                    bins=bins,
                    prior=state_groups,
                    predecessor=state_rows[owner][row_index],
                    budget=budget,
                )
            )
        all_vertices = [point for result in results for point in result[1]]
        all_planes = [plane for result in results for plane in result[2]]
        require(step["complete"] is True, "source step is not complete")
        kernel = points(step["common_owned_kernel"])
        for point in kernel:
            require(
                all(0 <= coordinate <= frame.length for coordinate in point)
                and all(nx * point[0] + ny * point[1] <= upper for nx, ny, upper in all_planes),
                "promoted kernel point lacks a complete-row ownership proof",
            )
        if all_vertices:
            state_groups[owner] = compressed(step, state_groups[owner], kernel)
        else:
            require("inner_grid_compression" not in step, "empty residual has compression")
        state_rows[owner] = [result[3] for result in results]
        seen.add(owner)
        trace.steps.append(StepTrace(owner, results, state_groups[owner]))
    admit_final_state(frame, source, state_groups, state_rows, mask_index=mask_index, mask=mask)
    trace.groups, trace.rows = state_groups, state_rows
    trace.contradiction = admit_contradiction(source, state_rows)
    return trace


def admit_final_state(
    frame: Frame,
    source: Mapping[str, Any],
    groups: Mapping[int, Polygon],
    rows: Mapping[int, list[Row]],
    *,
    mask_index: int | None = None,
    mask: Sequence[int] | None = None,
) -> None:
    mask = node_mask(frame, mask_index=mask_index, mask=mask)
    final = source["final_state"]
    require(
        final["mask_index"] == mask_index
        and final["mask"] == mask
        and Q(final["U"]) == frame.cap
        and Q(final["B"]) == frame.scale
        and final["constraints"] == []
        and final["guard"] == {}
        and final["guard_source"] is None
        and final["source"] == source["source"],
        "final state premise changed",
    )
    require(
        len(final["world"]) == len(frame.cells)
        and all(
            same(points(final["world"][cell]), frame.world(cell))
            for cell in range(len(frame.cells))
        ),
        "final world differs from the frame's cells",
    )
    require(
        set(final["groups"]) == set(map(str, mask))
        and all(same(points(final["groups"][str(owner)]), groups[owner]) for owner in mask),
        "final owned hulls differ from accepted induction",
    )
    for owner in mask:
        given = final["cells"][str(owner)]
        accepted = rows[owner]
        require(len(given) == len(accepted), "final row count changed")
        for source_row, checked_row in zip(given, accepted, strict=True):
            require(
                source_row["reference"] == checked_row["reference"]
                and [Q(t) for t in source_row["interval"]]
                == [Q(t) for t in checked_row["interval"]]
                and same(
                    points(source_row["outer_domain"]), points(checked_row["outer_domain"])
                )
                and len(source_row["residual_polygons"])
                == len(checked_row["residual_polygons"])
                and all(
                    same(points(got), points(want))
                    for got, want in zip(
                        source_row["residual_polygons"],
                        checked_row["residual_polygons"],
                        strict=True,
                    )
                ),
                "final row differs from accepted induction",
            )


def admit_contradiction(
    source: Mapping[str, Any], rows: Mapping[int, list[Row]]
) -> dict[str, Any]:
    """The declared closure, shown: the named owner's last update left no residual."""
    contradiction = source["contradiction"]
    require(
        isinstance(contradiction, dict)
        and contradiction.get("kind") == "all_parent_poses_forbidden",
        "only the all_parent_poses_forbidden closure is lifted",
    )
    owner, step_index = contradiction.get("owner"), contradiction.get("step")
    steps = source["steps"]
    require(
        type(owner) is int
        and type(step_index) is int
        and 0 <= step_index < len(steps)
        and steps[step_index]["owner"] == owner
        and owner in rows,
        "the contradiction names no updated owner",
    )
    assert isinstance(owner, int)
    require(
        all(not row["residual_polygons"] for row in rows[owner]),
        "complete terminal owner contradiction was not independently shown",
    )
    require(source["terminal"] is True and source["closed"] is True, "source is not terminal")
    require(
        source["mask_exclusion_proved"] is False
        and source["global_optimality_proved"] is False,
        "source claim fields changed",
    )
    return dict(contradiction)
