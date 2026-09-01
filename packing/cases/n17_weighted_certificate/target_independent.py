"""Target geometry adapter around the hash-frozen direct Cartesian accumulator."""

from __future__ import annotations

from fractions import Fraction

from cases.n17_weighted_certificate.geometry import reduce_event_cells
from cases.n17_weighted_certificate.independent import accumulate_direction
from cases.n17_weighted_certificate.model import (
    Atom,
    Direction,
    DirectionManifest,
    Fixture,
    TranslationDomain,
    canonical_hash,
)


def accumulate_target_independent(
    atoms: tuple[Atom, ...],
    direction: Direction,
    outer_side: Fraction,
    square_side: Fraction,
) -> DirectionManifest:
    """Directly sum atoms in every frozen event cell without range accumulation."""

    reduction = reduce_event_cells(atoms, direction, outer_side, square_side)
    best: Fraction | None = None
    witness: tuple[Fraction, Fraction] | None = None
    for i, j in reduction.cells:
        center = (
            (reduction.u_events[i] + reduction.u_events[i + 1]) / 2,
            (reduction.v_events[j] + reduction.v_events[j + 1]) / 2,
        )
        lower_left = (center[0] - square_side / 2, center[1] - square_side / 2)
        fixed = Fixture(
            atoms=atoms,
            directions=(direction,),
            window_side=square_side,
            domain=TranslationDomain(
                lower_left[0], lower_left[0], lower_left[1], lower_left[1]
            ),
        )
        score = accumulate_direction(fixed, direction).minimum
        if (
            best is None
            or witness is None
            or score < best
            or (score == best and center < witness)
        ):
            best = score
            witness = center
    if best is None or witness is None:
        raise ValueError("independent reduction produced no score")
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
