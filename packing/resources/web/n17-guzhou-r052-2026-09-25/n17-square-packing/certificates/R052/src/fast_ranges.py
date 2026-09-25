"""Exact integer projection of a convex legal polygon onto event y-cells.

The event x-grid includes every polygon vertex x.  Thus, within each open
x-slab, its top and bottom edges do not change.  A y-cell intersects the
positive-area legal slab exactly when its open interval meets the interior
of the slab's y projection.  No midpoint-feasibility claim is made.
"""
from __future__ import annotations

from bisect import bisect_left, bisect_right


def _less(a: tuple[int, int], b: tuple[int, int]) -> bool:
    return a[0]*b[1] < b[0]*a[1]


def feasible_y_ranges_fast(grid: dict) -> tuple[list[int], list[int]]:
    xe, ye, poly = grid['x_events'], grid['y_events'], grid['polygon']
    edges = []
    for (x0, y0), (x1, y1) in zip(poly, poly[1:]+poly[:1]):
        if x0 == x1:
            continue
        if x1 < x0:
            x0, y0, x1, y1 = x1, y1, x0, y0
        dx = x1-x0
        dy = y1-y0
        edges.append((x0, x1, dy, y0*dx-x0*dy, dx))
    pleft = min(x for x, _ in poly)
    pright = max(x for x, _ in poly)
    first, last = [], []
    for a, b in zip(xe, xe[1:]):
        if a < pleft or b > pright:
            first.append(-1)
            last.append(-1)
            continue
        values = []
        for left, right, slope, intercept, den in edges:
            if left <= a and b <= right:
                values.append((slope*a+intercept, den))
                values.append((slope*b+intercept, den))
        if len(values) != 4:
            raise ValueError(f"expected two legal edges over slab [{a},{b}], got {len(values)//2}")
        bottom = top = values[0]
        for value in values[1:]:
            if _less(value, bottom):
                bottom = value
            if _less(top, value):
                top = value
        if not _less(bottom, top):
            raise ValueError("legal slab has zero y extent")
        bottom_floor = bottom[0]//bottom[1]
        top_ceil = -((-top[0])//top[1])
        lo = bisect_right(ye, bottom_floor)-1
        hi = bisect_left(ye, top_ceil)
        if not (0 <= lo < hi <= len(ye)-1):
            raise ValueError(f"invalid y range at slab [{a},{b}]: {lo},{hi}")
        first.append(lo)
        last.append(hi)
    if not any(x >= 0 for x in first):
        raise ValueError("no legal open event cell")
    return first, last
