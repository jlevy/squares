"""The faster exact covers and the closed point-or-segment cover.

Verbatim copies, error types aside, of three frozen n11 modules:

* `n11_fast_exact_cover.py` (`eb21b1ac...`): the reference sweep's events and probes,
  with each polygon's edges compiled once and kept active across increasing probes;
* `n11_indexed_exact_cover.py` (`68580e32...`): the same, with edge pairs tested for a
  crossing only when their closed x projections overlap;
* `check_n11_closed_degenerate_cover.py` (`858c61c3...`): a point or segment domain
  covered by exact parameter intervals.

The first two prove exactly what `sweep.exact_union_cover` proves and report the same
events, probes and edge count; only the work differs. None of them knows a frame.
"""

from __future__ import annotations

import heapq
import time
from dataclasses import dataclass, field
from itertools import pairwise

from sqpack.hull_kernel.geometry import (
    Budget,
    Halfplane,
    IncompleteError,
    Polygon,
    RefusalError,
    area2,
    require,
)
from sqpack.hull_kernel.rational import Q

type Line = tuple[Q, Q, Q, Q]


@dataclass(slots=True)
class PolygonSweep:
    x_min: Q | None
    x_max: Q | None
    edges: list[Line]
    starts: list[tuple[Q, int]]
    ends: list[tuple[Q, int]]
    verticals: dict[Q, tuple[Q, Q]]
    active: set[int] = field(default_factory=set)
    start_cursor: int = 0
    end_cursor: int = 0

    def interval(self, x: Q) -> tuple[Q, Q] | None:
        """Match the reference's closed extrema over all edges crossing `x`."""
        x_min, x_max = self.x_min, self.x_max
        if x_min is None or x_max is None or x < x_min or x > x_max:
            return None
        while self.start_cursor < len(self.starts) and self.starts[self.start_cursor][0] <= x:
            self.active.add(self.starts[self.start_cursor][1])
            self.start_cursor += 1
        while self.end_cursor < len(self.ends) and self.ends[self.end_cursor][0] < x:
            self.active.remove(self.ends[self.end_cursor][1])
            self.end_cursor += 1
        vertical = self.verticals.get(x)
        low, high = vertical if vertical is not None else (None, None)
        for index in self.active:
            _, _, slope, intercept = self.edges[index]
            ordinate = slope * x + intercept
            if low is None or ordinate < low:
                low = ordinate
            if high is None or ordinate > high:
                high = ordinate
        return (low, high) if low is not None and high is not None else None


def compile_polygon(poly: Polygon) -> PolygonSweep:
    if not poly:
        return PolygonSweep(None, None, [], [], [], {})
    edges: list[Line] = []
    starts: list[tuple[Q, int]] = []
    ends: list[tuple[Q, int]] = []
    verticals: dict[Q, tuple[Q, Q]] = {}
    for p, q in zip(poly, poly[1:] + poly[:1], strict=True):
        if p[0] == q[0]:
            x = p[0]
            lo, hi = min(p[1], q[1]), max(p[1], q[1])
            previous = verticals.get(x)
            verticals[x] = (
                (min(lo, previous[0]), max(hi, previous[1])) if previous else (lo, hi)
            )
            continue
        left, right = min(p[0], q[0]), max(p[0], q[0])
        slope = (q[1] - p[1]) / (q[0] - p[0])
        edges.append((left, right, slope, p[1] - slope * p[0]))
        starts.append((left, len(edges) - 1))
        ends.append((right, len(edges) - 1))
    starts.sort()
    ends.sort()
    return PolygonSweep(
        min(point[0] for point in poly),
        max(point[0] for point in poly),
        edges,
        starts,
        ends,
        verticals,
    )


def covers_vertical_compiled(domain: PolygonSweep, regions: list[PolygonSweep], x: Q) -> bool:
    target = domain.interval(x)
    if target is None:
        raise RefusalError("coverage probe outside domain")
    spans = [span for poly in regions if (span := poly.interval(x)) is not None]
    spans.sort()
    cursor = target[0]
    for low, high in spans:
        if high < cursor:
            continue
        if low > cursor:
            return False
        cursor = max(cursor, high)
        if cursor >= target[1]:
            return True
    return False


def _sweep_probes(
    compiled: list[PolygonSweep], positions: list[Q], left: Q, right: Q, *, budget: Budget
) -> int:
    require(positions[0] == left and positions[-1] == right, "row domain endpoint missing")
    probes = [positions[0]]
    for a, b in pairwise(positions):
        probes.extend(((a + b) / 2, b))
    if len(probes) > budget.max_nodes:
        raise IncompleteError(f"row probe ceiling: probes={len(probes)}")
    for number, x in enumerate(probes):
        if time.monotonic() >= budget.deadline:
            raise IncompleteError(f"row sweep timeout: checked={number}, total={len(probes)}")
        require(
            covers_vertical_compiled(compiled[0], compiled[1:], x),
            f"row uncovered at exact x={x}",
        )
    return len(probes)


def fast_union_cover(
    domain: Polygon, regions: list[Polygon], *, budget: Budget
) -> dict[str, int]:
    """The reference sweep's events and probes over compiled, persistent edge state."""
    require(area2(domain) > 0, "degenerate row domain needs a separate proof")
    require(bool(regions), "no eligible charge regions")
    polygons = [domain, *regions]
    left, right = min(p[0] for p in domain), max(p[0] for p in domain)
    events = {p[0] for poly in polygons for p in poly if left <= p[0] <= right}
    compiled = [compile_polygon(poly) for poly in polygons]
    lines = [line for poly in compiled for line in poly.edges]
    for number, (a0, a1, m, b) in enumerate(lines):
        if time.monotonic() >= budget.deadline:
            raise IncompleteError(f"row event construction timed out after {number} edges")
        for z0, z1, n, d in lines[number + 1 :]:
            if m == n:
                continue
            start, stop = max(a0, z0, left), min(a1, z1, right)
            if start <= stop:
                crossing = (d - b) / (m - n)
                if start <= crossing <= stop:
                    events.add(crossing)
        if len(events) > budget.max_nodes:
            raise IncompleteError(f"row event ceiling: events={len(events)}")
    positions = sorted(events)
    probes = _sweep_probes(compiled, positions, left, right, budget=budget)
    return {"events": len(positions), "probes": probes, "edge_segments": len(lines)}


def event_positions(
    polygons: list[Polygon], lines: list[Line], left: Q, right: Q, *, budget: Budget
) -> list[Q]:
    """The reference's complete vertex and crossing abscissae, pairs indexed by x overlap."""
    events = {
        point[0] for polygon in polygons for point in polygon if left <= point[0] <= right
    }
    if len(events) > budget.max_nodes:
        raise IncompleteError(f"row event ceiling: events={len(events)}")
    active: dict[int, None] = {}
    ending: list[tuple[Q, int]] = []
    pairs = 0
    order = sorted(range(len(lines)), key=lambda item: (lines[item][0], item))
    for number, index in enumerate(order):
        if time.monotonic() >= budget.deadline:
            raise IncompleteError(f"indexed event construction timed out after {number} edges")
        a0, a1, m, b = lines[index]
        if a1 < left or a0 > right:
            continue
        while ending and ending[0][0] < a0:
            _, expired = heapq.heappop(ending)
            active.pop(expired, None)
        for other in active:
            pairs += 1
            if pairs % 1024 == 0 and time.monotonic() >= budget.deadline:
                raise IncompleteError(
                    f"indexed event construction timed out after {pairs} candidate pairs"
                )
            z0, z1, n, d = lines[other]
            if m == n:
                continue
            start, stop = max(a0, z0, left), min(a1, z1, right)
            if start <= stop:
                crossing = (d - b) / (m - n)
                if start <= crossing <= stop:
                    events.add(crossing)
                    if len(events) > budget.max_nodes:
                        raise IncompleteError(f"row event ceiling: events={len(events)}")
        active[index] = None
        heapq.heappush(ending, (a1, index))
    return sorted(events)


def indexed_union_cover(
    domain: Polygon, regions: list[Polygon], *, budget: Budget
) -> dict[str, int]:
    """Prove the same closed convex-region union as the all-pairs reference."""
    require(area2(domain) > 0, "degenerate row domain needs a separate proof")
    require(bool(regions), "no eligible charge regions")
    polygons = [domain, *regions]
    left, right = min(point[0] for point in domain), max(point[0] for point in domain)
    compiled = [compile_polygon(polygon) for polygon in polygons]
    lines = [line for polygon in compiled for line in polygon.edges]
    positions = event_positions(polygons, lines, left, right, budget=budget)
    probes = _sweep_probes(compiled, positions, left, right, budget=budget)
    return {"events": len(positions), "probes": probes, "edge_segments": len(lines)}


def _cross(p: tuple[Q, Q], q: tuple[Q, Q], r: tuple[Q, Q]) -> Q:
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def closed_convex_hull(region: Polygon) -> Polygon:
    """Hull normal form of a closed convex region, point or segment; refuses nonconvex."""
    require(bool(region), "empty coverage region")
    if len(region) >= 3:
        turns = [
            _cross(p, q, r)
            for p, q, r in zip(
                region, region[1:] + region[:1], region[2:] + region[:2], strict=True
            )
        ]
        require(
            all(turn >= 0 for turn in turns) or all(turn <= 0 for turn in turns),
            "nonconvex coverage region",
        )
    ordered = sorted(set(region))
    if len(ordered) <= 2:
        return ordered
    lower: Polygon = []
    upper: Polygon = []
    for point in ordered:
        while len(lower) >= 2 and _cross(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)
    for point in reversed(ordered):
        while len(upper) >= 2 and _cross(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    result = lower[:-1] + upper[:-1]
    require(area2(region) == area2(result), "region differs from convex hull")
    return result


def convex_halfplanes(region: Polygon) -> list[Halfplane]:
    """Represent a closed convex area, segment, or point by halfplanes."""
    poly = closed_convex_hull(region)
    if len(poly) == 1:
        x, y = poly[0]
        return [
            (Q(1), Q(), x),
            (Q(-1), Q(), -x),
            (Q(), Q(1), y),
            (Q(), Q(-1), -y),
        ]
    if len(poly) == 2:
        (x0, y0), (x1, y1) = poly
        dx, dy = x1 - x0, y1 - y0
        line = (dy, -dx, dy * x0 - dx * y0)
        return [
            (Q(1), Q(), max(x0, x1)),
            (Q(-1), Q(), -min(x0, x1)),
            (Q(), Q(1), max(y0, y1)),
            (Q(), Q(-1), -min(y0, y1)),
            line,
            (-line[0], -line[1], -line[2]),
        ]
    return [
        (q[1] - p[1], p[0] - q[0], (q[1] - p[1]) * p[0] - (q[0] - p[0]) * p[1])
        for p, q in zip(poly, poly[1:] + poly[:1], strict=True)
    ]


def closed_degenerate_cover(
    legal: Polygon, regions: list[Polygon], *, budget: Budget
) -> dict[str, int]:
    """Cover a closed point or segment by exact parameter intervals in [0,1]."""
    domain = closed_convex_hull(legal)
    require(len(domain) <= 2, "expected point or segment domain")
    require(bool(regions), "no eligible charge regions")
    start, end = domain[0], domain[-1]
    dx, dy = end[0] - start[0], end[1] - start[1]
    intervals: list[tuple[Q, Q]] = []
    constraints = 0
    for region in regions:
        lower, upper = Q(), Q(1)
        for a, b, c in convex_halfplanes(region):
            constraints += 1
            if constraints > budget.max_nodes or time.monotonic() >= budget.deadline:
                raise IncompleteError("degenerate coverage event ceiling")
            base = a * start[0] + b * start[1] - c
            slope = a * dx + b * dy
            if slope > 0:
                upper = min(upper, -base / slope)
            elif slope < 0:
                lower = max(lower, -base / slope)
            elif base > 0:
                lower, upper = Q(1), Q()
                break
            if lower > upper:
                break
        if lower <= upper:
            intervals.append((lower, upper))
    intervals.sort()
    cursor = Q()
    for lower, upper in intervals:
        require(lower <= cursor, "uncovered degenerate legal domain")
        cursor = max(cursor, upper)
        if cursor >= 1:
            return {"events": constraints, "probes": len(intervals)}
    require(cursor >= 1, "uncovered degenerate legal domain")
    return {"events": constraints, "probes": len(intervals)}
