"""Shared exact geometry definitions and event-cell reduction."""

from __future__ import annotations

from bisect import bisect_left, bisect_right
from dataclasses import dataclass
from fractions import Fraction
from itertools import pairwise

from cases.n17_weighted_certificate.model import Atom, Direction


@dataclass(frozen=True, slots=True)
class EventReduction:
    u_events: tuple[Fraction, ...]
    v_events: tuple[Fraction, ...]
    rectangles: tuple[tuple[Fraction, Fraction, Fraction, Fraction, Fraction], ...]
    cells: tuple[tuple[int, int], ...]


def _clip_u(
    polygon: tuple[tuple[Fraction, Fraction], ...],
    bound: Fraction,
    *,
    keep_greater: bool,
) -> tuple[tuple[Fraction, Fraction], ...]:
    if not polygon:
        return ()
    output: list[tuple[Fraction, Fraction]] = []

    def inside(point: tuple[Fraction, Fraction]) -> bool:
        return point[0] >= bound if keep_greater else point[0] <= bound

    previous = polygon[-1]
    previous_inside = inside(previous)
    for current in polygon:
        current_inside = inside(current)
        if current_inside != previous_inside:
            u1, v1 = previous
            u2, v2 = current
            factor = Fraction(0) if u2 == u1 else (bound - u1) / (u2 - u1)
            output.append((bound, v1 + factor * (v2 - v1)))
        if current_inside:
            output.append(current)
        previous = current
        previous_inside = current_inside
    return tuple(output)


def center_domain(
    outer_side: Fraction,
    square_side: Fraction,
    direction: Direction,
) -> tuple[tuple[Fraction, Fraction], ...]:
    cosine, sine = direction.ux, direction.uy
    half_extent = square_side * (cosine + sine) / 2
    low, high = half_extent, outer_side - half_extent
    corners = ((low, low), (high, low), (high, high), (low, high))
    return tuple((cosine * x + sine * y, -sine * x + cosine * y) for x, y in corners)


def reduce_event_cells(
    atoms: tuple[Atom, ...],
    direction: Direction,
    outer_side: Fraction,
    square_side: Fraction,
) -> EventReduction:
    """Apply the frozen conservative convex-domain event-cell reduction exactly."""

    half = square_side / 2
    domain = center_domain(outer_side, square_side, direction)
    u_domain_min = min(u for u, _ in domain)
    u_domain_max = max(u for u, _ in domain)
    v_domain_min = min(v for _, v in domain)
    v_domain_max = max(v for _, v in domain)
    rectangles: list[tuple[Fraction, Fraction, Fraction, Fraction, Fraction]] = []
    u_events = {u_domain_min, u_domain_max}
    v_events = {v_domain_min, v_domain_max}
    for atom in atoms:
        projected_u = direction.ux * atom.x + direction.uy * atom.y
        projected_v = direction.vx * atom.x + direction.vy * atom.y
        rectangle = (
            projected_u - half,
            projected_u + half,
            projected_v - half,
            projected_v + half,
            atom.weight,
        )
        rectangles.append(rectangle)
        u_events.update(rectangle[:2])
        v_events.update(rectangle[2:4])

    ordered_u = tuple(sorted(u_events))
    ordered_v = tuple(sorted(v_events))
    cells: list[tuple[int, int]] = []
    for i, (u0, u1) in enumerate(pairwise(ordered_u)):
        if u1 <= u_domain_min or u0 >= u_domain_max:
            continue
        slab = _clip_u(domain, u0, keep_greater=True)
        slab = _clip_u(slab, u1, keep_greater=False)
        if not slab:
            continue
        vertical_low = min(v for _, v in slab)
        vertical_high = max(v for _, v in slab)
        if vertical_high <= vertical_low:
            continue
        j0 = max(0, bisect_right(ordered_v, vertical_low) - 1)
        j1 = min(len(ordered_v) - 2, bisect_left(ordered_v, vertical_high) - 1)
        cells.extend((i, j) for j in range(j0, j1 + 1))
    if not cells:
        raise ValueError("center domain produced no event cells")
    return EventReduction(ordered_u, ordered_v, tuple(rectangles), tuple(cells))
