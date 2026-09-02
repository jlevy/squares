"""Clean-room direct Cartesian accumulator for weighted-point certificates.

This module deliberately uses direct membership sums. It contains no source-verifier
imports, difference arrays, prefix sums, or target-specific expected values.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import pairwise

from cases.n17_weighted_certificate.model import (
    Atom,
    CertificateManifest,
    Direction,
    DirectionManifest,
    Fixture,
    canonical_hash,
)


def _events(
    coordinates: tuple[Fraction, ...],
    side: Fraction,
    low: Fraction,
    high: Fraction,
) -> tuple[Fraction, ...]:
    values = {low, high}
    for coordinate in coordinates:
        for event in (coordinate, coordinate - side):
            if low <= event <= high:
                values.add(event)
    return tuple(sorted(values))


def _states(events: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    values = set(events)
    values.update((left + right) / 2 for left, right in pairwise(events))
    return tuple(sorted(values))


def _project(atom: Atom, direction: Direction) -> tuple[Fraction, Fraction]:
    return (
        direction.ux * atom.x + direction.uy * atom.y,
        direction.vx * atom.x + direction.vy * atom.y,
    )


def _inside(
    coordinate: Fraction,
    start: Fraction,
    side: Fraction,
    *,
    upper_inclusive: bool,
) -> bool:
    if coordinate < start:
        return False
    upper = start + side
    return coordinate <= upper if upper_inclusive else coordinate < upper


def accumulate_direction(
    fixture: Fixture,
    direction: Direction,
    *,
    upper_inclusive: bool = True,
) -> DirectionManifest:
    """Enumerate Cartesian event states and directly sum every atom at each state."""

    projected = tuple((atom, *_project(atom, direction)) for atom in fixture.atoms)
    x_events = _events(
        tuple(x for _, x, _ in projected),
        fixture.window_side,
        fixture.domain.x_low,
        fixture.domain.x_high,
    )
    y_events = _events(
        tuple(y for _, _, y in projected),
        fixture.window_side,
        fixture.domain.y_low,
        fixture.domain.y_high,
    )
    x_states = _states(x_events)
    y_states = _states(y_events)

    minimum: Fraction | None = None
    witness: tuple[Fraction, Fraction] | None = None
    for x_start in x_states:
        for y_start in y_states:
            mass = sum(
                (
                    atom.weight
                    for atom, x, y in projected
                    if _inside(
                        x,
                        x_start,
                        fixture.window_side,
                        upper_inclusive=upper_inclusive,
                    )
                    and _inside(
                        y,
                        y_start,
                        fixture.window_side,
                        upper_inclusive=upper_inclusive,
                    )
                ),
                start=Fraction(0),
            )
            candidate = (x_start, y_start)
            if (
                minimum is None
                or witness is None
                or mass < minimum
                or (mass == minimum and candidate < witness)
            ):
                minimum = mass
                witness = candidate

    if minimum is None or witness is None:
        raise ValueError("translation domain produced no Cartesian state")
    return DirectionManifest(
        label=direction.label,
        direction=(direction.ux, direction.uy, direction.vx, direction.vy),
        x_events=x_events,
        y_events=y_events,
        x_event_hash=canonical_hash(x_events),
        y_event_hash=canonical_hash(y_events),
        event_cell_count=max(0, len(x_events) - 1) * max(0, len(y_events) - 1),
        evaluated_state_count=len(x_states) * len(y_states),
        minimum=minimum,
        witness=witness,
    )


def accumulate_fixture(
    fixture: Fixture, *, upper_inclusive: bool = True
) -> CertificateManifest:
    """Build the complete canonical manifest with no target-specific oracle values."""

    rows = tuple(
        accumulate_direction(fixture, direction, upper_inclusive=upper_inclusive)
        for direction in fixture.directions
    )
    return CertificateManifest(
        atom_count=len(fixture.atoms),
        atom_hash=canonical_hash(fixture.atoms),
        total_weight=sum((atom.weight for atom in fixture.atoms), start=Fraction(0)),
        direction_count=len(fixture.directions),
        direction_hash=canonical_hash(fixture.directions),
        rows=rows,
        global_minimum=min(row.minimum for row in rows),
    )
