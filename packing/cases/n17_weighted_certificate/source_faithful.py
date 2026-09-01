"""Source-faithful integer difference-array adapter, isolated from the clean-room path."""

from __future__ import annotations

from fractions import Fraction

from cases.n17_weighted_certificate.geometry import reduce_event_cells
from cases.n17_weighted_certificate.model import (
    Atom,
    Direction,
    DirectionManifest,
    canonical_hash,
)


def accumulate_source_faithful(
    atoms: tuple[Atom, ...],
    direction: Direction,
    outer_side: Fraction,
    square_side: Fraction,
) -> DirectionManifest:
    """Mirror the retained range-addition and two-axis cumulative-sum control flow."""

    reduction = reduce_event_cells(atoms, direction, outer_side, square_side)
    u_index = {value: index for index, value in enumerate(reduction.u_events)}
    v_index = {value: index for index, value in enumerate(reduction.v_events)}
    difference = [[Fraction(0) for _ in reduction.v_events] for _ in reduction.u_events]
    for u1, u2, v1, v2, weight in reduction.rectangles:
        left, right = u_index[u1], u_index[u2]
        bottom, top = v_index[v1], v_index[v2]
        difference[left][bottom] += weight
        difference[right][bottom] -= weight
        difference[left][top] -= weight
        difference[right][top] += weight

    for i in range(len(difference)):
        for j in range(1, len(difference[i])):
            difference[i][j] += difference[i][j - 1]
    for i in range(1, len(difference)):
        for j in range(len(difference[i])):
            difference[i][j] += difference[i - 1][j]

    best: Fraction | None = None
    witness: tuple[Fraction, Fraction] | None = None
    for i, j in reduction.cells:
        score = difference[i][j]
        center = (
            (reduction.u_events[i] + reduction.u_events[i + 1]) / 2,
            (reduction.v_events[j] + reduction.v_events[j + 1]) / 2,
        )
        if (
            best is None
            or witness is None
            or score < best
            or (score == best and center < witness)
        ):
            best = score
            witness = center
    if best is None or witness is None:
        raise ValueError("source-faithful reduction produced no score")
    return DirectionManifest(
        label=direction.label,
        direction=(direction.ux, direction.uy, direction.vx, direction.vy),
        x_events=reduction.u_events,
        y_events=reduction.v_events,
        x_event_hash=canonical_hash(reduction.u_events),
        y_event_hash=canonical_hash(reduction.v_events),
        event_cell_count=len(reduction.cells),
        evaluated_state_count=len(reduction.cells),
        minimum=best,
        witness=witness,
    )
