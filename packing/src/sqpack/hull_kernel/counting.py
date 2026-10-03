"""The counting (majority-feature) mode: one packet's rows, ownership and transfer.

A packet names required owners `O` with owned field points, rational sites, one
majority feature over `2m - 1` sites with threshold `m` and weight one, per-cell
thresholds `q_i` and a budget `b`. For each positive cell (`q_i > 0`) and each row of a
closed partition of the half-angle chart `[0, 1]`, the row check proves that every legal
centre lies in the feature's median strip region (the square's strict core captures the
feature) or in a capture box around an owned point of another owner (an interior
overlap, so impossible). The capture resource has capacity one, so a state containing
`O` whose positive thresholds sum above `b` is impossible; transfer extends that to
every orbit representative some symmetry image of which is such a state.

The functions are copies of `row_envelope`, `true_halfplanes`, `row_geometry`,
`proposed_rows`, `transferred_cases` and `all_geometry` from the frozen n11 mask-0
checker with n11's constants read from the frame and the packet. Only the
single-feature, unit-weight packet is lifted: it is the one whose plain union cover is
the proof obligation. Weighted packets need the weighted cover of the n11 field runner,
and a packet that is not unit-weight is refused here rather than checked unsoundly.
"""

from __future__ import annotations

import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from itertools import pairwise
from typing import Any

from sqpack.hull_kernel.frame import Frame
from sqpack.hull_kernel.geometry import (
    Budget,
    Halfplane,
    IncompleteError,
    Point,
    area2,
    box_halfplanes,
    intersect,
    primitive_normal,
    quadratic_nonnegative,
    require,
    trig,
)
from sqpack.hull_kernel.ownership import ownership
from sqpack.hull_kernel.rational import Q
from sqpack.hull_kernel.sweep import exact_union_cover

type Row = tuple[int, int, tuple[Q, Q]]


@dataclass(frozen=True)
class MajorityFeature:
    sites: tuple[int, ...]
    threshold: int
    weight: int


@dataclass(frozen=True)
class CountingPacket:
    """A counting certificate on a frame; every coordinate is a field coordinate."""

    owners: tuple[int, ...]
    owned_points: Mapping[int, tuple[Point, ...]]
    sites: tuple[Point, ...]
    feature: MajorityFeature
    thresholds: tuple[int, ...]
    budget: int

    @property
    def positive_cells(self) -> tuple[int, ...]:
        return tuple(cell for cell, value in enumerate(self.thresholds) if value > 0)


def admit_packet(frame: Frame, packet: CountingPacket) -> None:
    """Refuse a packet the unit-weight union cover does not prove."""
    cells = len(frame.cells)
    require(len(packet.thresholds) == cells, "one threshold per cell is required")
    require(all(value in (0, 1) for value in packet.thresholds), "thresholds must be 0 or 1")
    require(packet.budget == packet.feature.weight == 1, "only a unit-weight packet is lifted")
    feature = packet.feature
    require(
        len(feature.sites) == 2 * feature.threshold - 1 == len(set(feature.sites)),
        "a majority feature needs 2m - 1 distinct sites",
    )
    require(
        tuple(feature.sites) == tuple(range(len(packet.sites))),
        "the feature must use every site in order",
    )
    require(len(set(packet.sites)) == len(packet.sites), "duplicate field site")
    require(
        all(0 <= x <= frame.length and 0 <= y <= frame.length for x, y in packet.sites),
        "field site outside the container",
    )
    require(
        len(set(packet.owners)) == len(packet.owners)
        and all(0 <= owner < cells for owner in packet.owners),
        "owners must be distinct cells",
    )
    require(
        set(packet.owned_points) == set(packet.owners), "owned points must name every owner"
    )
    require(bool(packet.positive_cells), "a packet needs a positive cell")


def row_envelope(frame: Frame, interval: tuple[Q, Q]) -> tuple[Q, Q, Q, Q]:
    """Strict core side, legal centre half-width and midpoint `(c, s)` of one row."""
    scale = frame.scale
    left, right = interval
    require(0 <= left < right <= 1, "row interval outside closed angle domain")
    mid = (left + right) / 2
    c, s = trig(mid)
    endpoint = [trig(t) for t in interval]
    factors = [c * cz + s * sz + abs(c * sz - s * cz) for cz, sz in endpoint]
    factor = max(factors)
    min_width = min(cz + sz for cz, sz in endpoint)
    core = (scale - frame.core_slack) / factor
    low, high = frame.field_centre_bounds(min_width / 2)
    halfwidth = (high - low) / 2
    require(0 < core < scale and core * factor < scale, "strict inner core fails")
    require(
        quadratic_nonnegative(factor - c - s, 2 * (c - s), factor + c + s, left, mid)
        and quadratic_nonnegative(factor - c + s, -2 * (c + s), factor + c - s, mid, right),
        "full-angle core envelope fails",
    )
    require(
        quadratic_nonnegative(1 - min_width, Q(2), -1 - min_width, left, right),
        "full-angle legal-wall envelope fails",
    )
    return core, halfwidth, c, s


def majority_halfplanes(sites: list[Point], radius: Q, threshold: int) -> list[Halfplane]:
    """Median-strip TRUE region; between these normal events its supports are affine."""
    require(len(sites) == 2 * threshold - 1, "a majority feature needs 2m - 1 sites")
    normals = {(Q(1), Q(0)), (Q(0), Q(1))}
    for number, p in enumerate(sites):
        for q in sites[number + 1 :]:
            dx, dy = q[1] - p[1], p[0] - q[0]
            if dx or dy:
                normals.add(primitive_normal(dx, dy))
    rows: list[Halfplane] = []
    for a, b in sorted(normals):
        median = sorted(a * x + b * y for x, y in sites)[threshold - 1]
        margin = radius * (abs(a) + abs(b))
        rows.extend(((a, b, median + margin), (-a, -b, -median + margin)))
    return rows


def counting_row(
    frame: Frame,
    packet: CountingPacket,
    cell: int,
    interval: tuple[Q, Q],
    *,
    budget: Budget,
) -> dict[str, Any]:
    """One row of one positive cell: every legal centre is charged or impossible."""
    require(cell in packet.positive_cells, "row outside positive cells")
    core, h, c, s = row_envelope(frame, interval)
    low, high = frame.field_centre_bounds(min(sum(trig(t), Q()) for t in interval) / 2)
    legal = intersect(
        frame.world(cell),
        [
            (Q(1), Q(0), high),
            (Q(-1), Q(0), -low),
            (Q(0), Q(1), high),
            (Q(0), Q(-1), -low),
        ],
    )
    require(area2(legal) > 0, "degenerate row domain needs a separate proof")
    domain = [frame.rotate(p, c, s) for p in legal]
    sites = [frame.rotate(packet.sites[index], c, s) for index in packet.feature.sites]
    radius = core / 2
    true_region = intersect(
        domain, majority_halfplanes(sites, radius, packet.feature.threshold)
    )
    regions = [true_region] if area2(true_region) > 0 else []
    for owner in packet.owners:
        if owner == cell:
            continue
        for value in packet.owned_points[owner]:
            captured = intersect(domain, box_halfplanes(frame.rotate(value, c, s), radius))
            if area2(captured) > 0:
                regions.append(captured)
    proof = exact_union_cover(domain, regions, budget=budget)
    return {
        "cell": cell,
        "interval": [str(interval[0]), str(interval[1])],
        "core_side": str(core),
        "parent_center_halfwidth": str(h),
        "domain_area_twice": str(area2(domain)),
        "eligible_regions": len(regions),
        **proof,
    }


def partition_rows(
    proposals: Sequence[tuple[int, tuple[Q, Q]]], positive_cells: Sequence[int]
) -> list[Row]:
    """Order proposed `(cell, interval)` rows; each cell's must partition `[0, 1]`."""
    by_cell: dict[int, list[tuple[Q, Q]]] = {cell: [] for cell in positive_cells}
    for cell, interval in proposals:
        require(cell in by_cell, "row proposal outside positive cells")
        by_cell[cell].append(interval)
    ordered: list[Row] = []
    for cell in positive_cells:
        intervals = sorted(by_cell[cell])
        require(bool(intervals), f"cell {cell}: no rows")
        require(
            intervals[0][0] == 0 and intervals[-1][1] == 1,
            f"cell {cell}: angle endpoints missing",
        )
        require(len(set(intervals)) == len(intervals), f"cell {cell}: duplicate row interval")
        for left, right in intervals:
            require(0 <= left < right <= 1, f"cell {cell}: malformed row interval")
        for (_, end), (start, _) in pairwise(intervals):
            require(end == start, f"cell {cell}: row gap or overlap")
        ordered.extend((cell, index, interval) for index, interval in enumerate(intervals))
    return ordered


def transferred_states(frame: Frame, packet: CountingPacket) -> dict[str, list[int]]:
    """Representative indices excluded directly, and through any symmetry image."""
    support = set(packet.owners)

    def applicable(state: Sequence[int]) -> bool:
        return (
            support.issubset(state)
            and sum(packet.thresholds[cell] for cell in state) > packet.budget
        )

    representatives = frame.representatives
    direct = [index for index, state in enumerate(representatives) if applicable(state)]
    transferred = [
        index
        for index, state in enumerate(representatives)
        if any(applicable(frame.image(action, state)) for action in frame.actions)
    ]
    return {"direct_case_ids": direct, "transferred_case_ids": transferred}


def _partitions(rows: Sequence[Row], packet: CountingPacket) -> bool:
    """Whether the rows partition `[0, 1]` for every positive cell, and nothing else."""
    by_cell: dict[int, list[tuple[Q, Q]]] = {cell: [] for cell in packet.positive_cells}
    for cell, _, interval in rows:
        if cell not in by_cell:
            return False
        by_cell[cell].append(interval)
    for intervals in by_cell.values():
        ordered = sorted(intervals)
        if not ordered or ordered[0][0] != 0 or ordered[-1][1] != 1:
            return False
        if any(first[1] != second[0] for first, second in pairwise(ordered)):
            return False
    return True


def _check_global_budget(budget: Budget, work: int, phase: str) -> None:
    if time.monotonic() >= budget.deadline or work >= budget.max_nodes:
        raise IncompleteError(f"global ceiling before next {phase}")


def replay_counting_packet(
    frame: Frame,
    packet: CountingPacket,
    rows: Sequence[Row],
    *,
    budget: Budget,
    points: Sequence[tuple[int, int]] | None = None,
    transfer: bool = True,
) -> dict[str, Any]:
    """Check ownership points, then rows, then transfer, under one shared budget.

    `points` and `rows` may be subsets for a partial replay; a partial replay, like an
    incomplete one, reports `geometry_verified: False` and excludes nothing.
    """
    admit_packet(frame, packet)
    every_point = [
        (owner, index)
        for owner in packet.owners
        for index in range(len(packet.owned_points[owner]))
    ]
    owner_keys = every_point if points is None else list(points)
    require(all(key in every_point for key in owner_keys), "point outside the packet")
    checked_points: list[dict[str, Any]] = []
    checked_rows: list[dict[str, Any]] = []
    transfer_result: dict[str, list[int]] | None = None
    work = 0
    try:
        for owner, index in owner_keys:
            _check_global_budget(budget, work, "owned point")
            proof = ownership(
                frame,
                owner,
                packet.owned_points[owner][index],
                budget=Budget(budget.deadline, budget.max_nodes - work),
            )
            work += proof["nodes"]
            checked_points.append({"owner": owner, "point_index": index, **proof})
        for cell, index, interval in rows:
            _check_global_budget(budget, work, "row")
            proof = counting_row(
                frame,
                packet,
                cell,
                interval,
                budget=Budget(budget.deadline, budget.max_nodes - work),
            )
            work += proof["events"] + proof["probes"]
            checked_rows.append({"row_index": index, **proof})
        if transfer:
            _check_global_budget(budget, work, "transfer audit")
            transfer_result = transferred_states(frame, packet)
        _check_global_budget(budget, work, "PASS return")
    except IncompleteError as error:
        return {
            "status": "INCOMPLETE",
            "reason": str(error),
            "ownership_checked": checked_points,
            "rows_checked": checked_rows,
            "work_units": work,
            "canonical_cases_excluded": 0,
            "geometry_verified": False,
        }
    complete = points is None and transfer_result is not None and _partitions(rows, packet)
    return {
        "status": "PASS_COUNTING_PACKET" if complete else "PASS_PARTIAL_REPLAY",
        "frame": frame.name,
        "ownership_checked": checked_points,
        "rows_checked": checked_rows,
        "work_units": work,
        "ownership_points": len(checked_points),
        "positive_cell_rows": len(checked_rows),
        "canonical_cases_excluded": (
            len(transfer_result["transferred_case_ids"]) if complete and transfer_result else 0
        ),
        "geometry_verified": complete,
        "transfer": transfer_result,
    }
