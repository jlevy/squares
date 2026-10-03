"""Ownership: a field point lies strictly inside the square for every pose its cell allows.

A copy of `ownership` from the frozen n11 mask-0 checker with the frame's cap, field
side and scale in place of n11's module constants. The square's centre ranges over the
closed cell and its half-angle `t` over `[0, 1]`.

The disk bound accepts when every cell vertex lies within distance `1/2` of the point
(in physical units), since the square holds the open disc of radius `1/2` about its
centre and the cell is convex. Otherwise the angle interval is bisected: on `[lo, hi]`
the centre is confined to the cell clipped by the frame's centred legal box for the
half-extent `h = min(c + s)/2` over the endpoints (`[h, U - h]^2` without a capture
cap), and for each legal vertex the point's two body coordinates are bounded by
interval products over the endpoint cosines and sines; a positive margin below `1/2` on
both proves strict containment over the whole sub-interval, by convexity in the centre.
"""

from __future__ import annotations

import time
from typing import Any

from sqpack.hull_kernel.frame import Frame
from sqpack.hull_kernel.geometry import (
    Budget,
    IncompleteError,
    Point,
    clip,
    projection_range,
    require,
    trig,
)
from sqpack.hull_kernel.rational import Q


def ownership(
    frame: Frame, cell: int, field_point: Point, *, budget: Budget, max_depth: int = 20
) -> dict[str, Any]:
    """Prove strict capture over all legal centers and the full angle interval."""
    polygon = frame.cell(cell)
    scale = frame.scale
    unit = field_point[0] / scale, field_point[1] / scale
    require(all(0 <= x <= frame.length for x in field_point), "field point outside container")
    max_distance2 = max((unit[0] - v[0]) ** 2 + (unit[1] - v[1]) ** 2 for v in polygon)
    if max_distance2 < Q(1, 4):
        return {
            "method": "strict_disk_vertex_bound",
            "maximum_vertex_distance_squared": str(max_distance2),
            "nodes": 0,
            "leaves": 1,
            "empty_leaves": 0,
            "strict_squared_distance_slack": str(Q(1, 4) - max_distance2),
        }
    stack = [(Q(0), Q(1), 0)]
    nodes = leaves = empty = 0
    margin = Q(1, 2)
    deepest = 0
    while stack:
        if time.monotonic() >= budget.deadline or nodes >= budget.max_nodes:
            raise IncompleteError(f"ownership ceiling: nodes={nodes}, pending={len(stack)}")
        lo, hi, depth = stack.pop()
        nodes += 1
        clo, slo = trig(lo)
        chi, shi = trig(hi)
        low, high = frame.centre_bounds(min(clo + slo, chi + shi) / 2)
        legal = polygon
        for axis in (0, 1):
            normal = (Q(1), Q(0)) if axis == 0 else (Q(0), Q(1))
            legal = clip(legal, (-normal[0], -normal[1], -low))
            legal = clip(legal, (normal[0], normal[1], high))
        deepest = max(deepest, depth)
        if not legal:
            leaves += 1
            empty += 1
            continue
        local = Q(1, 2)
        for x, y in legal:
            dx, dy = unit[0] - x, unit[1] - y
            for a, d in ((dx, dy), (dy, -dx)):
                lower, upper = projection_range((a, d), (chi, clo), (slo, shi))
                local = min(local, Q(1, 2) - max(-lower, upper))
        if local > 0:
            margin = min(margin, local)
            leaves += 1
        elif depth < max_depth:
            mid = (lo + hi) / 2
            stack.append((mid, hi, depth + 1))
            stack.append((lo, mid, depth + 1))
        else:
            raise IncompleteError(
                f"ownership depth ceiling: interval=({lo},{hi}), nodes={nodes}"
            )
    return {
        "method": "strict_wall_interval_bound",
        "maximum_vertex_distance_squared": str(max_distance2),
        "nodes": nodes,
        "leaves": leaves,
        "empty_leaves": empty,
        "minimum_margin": str(margin),
        "deepest": deepest,
    }
