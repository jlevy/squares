"""Goebel's `n = 65` family pose with one L of seventeen: the published `n = 82` record.

`[Friedman DS7]` section 2 states both rules. The centred-diagonal-block family gives the
best known `n = 65` at side `5 + (5/2)/sqrt(2) * 2` -- built here by
`cases.gobel_family.build(4, 5)` -- and "adding an 'L' around the packing of 65 squares
gives the best known packing of 82 squares", at side one larger. (The Kingbird catalogue's
`n = 82` annotation says "two L's"; two L's would add two to the side and its own arithmetic
says one, which is also what DS7 says. One L is what verifies.)

The L is derived rather than transcribed: the new container is exactly one wider, so a
column of unit squares stands flush against the new right wall and a row lies flush under
the new top wall. Nine fit in the column and eight in the row -- `floor(6 + (5/2)sqrt(2))`
is nine, and the row loses one to the column's top square -- and a tenth column square is
refused by the container, which `verify_exact` keeps as a control.

The retained decimal witness carries this side exactly, correctly rounded up at its
thirty-two digits, but **not this layout**: its centre set matches none of this
construction's eight dihedral images (all gaps exceed `6.8`). So the evidence this package
supports is about the construction -- `s(82) <= 6 + (5/2)sqrt(2)` -- and deliberately not an
identification of the witness's geometry, unlike `cases/gobel_family` at `n = 65`.

Nothing here claims optimality.
"""

from __future__ import annotations

from cases.gobel40.packing import corners
from cases.gobel_family.packing import build as build_family
from sqpack.field import FieldElement, NumberField

SOURCE = "[Friedman DS7] section 2, Goebel's family plus the L extension"
SOURCE_URL = "https://kingbird.myphotos.cc/packing/"

COLUMN = 9
"""Unit squares against the new right wall: floor(6 + (5/2)sqrt(2)) = 9."""

ROW = 8
"""Unit squares under the new top wall, stopping short of the column's top square."""


def count() -> int:
    return 65 + COLUMN + ROW


def build() -> tuple[list[list[tuple[FieldElement, FieldElement]]], FieldElement, NumberField]:
    """Exact corners, side, and the degree-two field for the `n = 82` construction."""
    inner, inner_side, field = build_family(4, 5)
    q = field.rational
    half = q(1) / q(2)
    side = inner_side + q(1)

    column = [
        corners((side - half, q(2 * k + 1) / q(2)), (half, q(0)), (q(0), half))
        for k in range(COLUMN)
    ]
    row = [
        corners((q(2 * k + 1) / q(2), side - half), (half, q(0)), (q(0), half))
        for k in range(ROW)
    ]

    squares = inner + column + row
    assert len(squares) == count(), (len(squares), count())
    # s = 7 + (5/2) sqrt(2) - 1 satisfies (s - 6)^2 = 25/2.
    residual = (side - q(6)) * (side - q(6)) - q(25) / q(2)
    assert residual == field.zero, "the side does not satisfy its own defining relation"
    return squares, side, field
