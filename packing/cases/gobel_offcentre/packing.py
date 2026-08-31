"""Friedman's off-centre variant of Goebel's family, plus its column, for any `(a, b)`.

`[Friedman DS7]` section 3: "We can generalize the packings in Figure 3 by placing the
central square a little off center. We can pack `2a^2+2a+b^2` squares in a rectangle with
sides `a+1/2+b/sqrt(2)` and `a+3/2+b/sqrt(2)`. Adding a column of squares to the side of
this, we get a packing of `2a^2+4a+b^2+1` squares in a square of side `a+3/2+b/sqrt(2)`.
This gives the best known packings for 26 and 85 squares."

The layout is derived from that sentence and nothing else. The rectangle is the centred
family's container squeezed half a unit in one direction and stretched half a unit in the
other, with the `b` by `b` tilted block centred **in the rectangle** -- which is what makes
it off-centre in the final square once the column of `2a+1` unit squares stands against the
rectangle's tall side. The frame is the same derived lattice as `cases/gobel_family`: `a`
offsets from each wall in each direction, minus the cells the block occupies, computed by
the exact separating-axis test. The tighter container narrows Goebel's admissibility
condition by the half unit it took away: `a - 1/2 < b/sqrt(2) < a + 1/2`, which both
published instances satisfy.

A wrong `(a, b)` produces a wrong count rather than a plausible picture, exactly as in the
parent family, and the assertion at the end is what turns that into a stop.

Nothing here claims optimality.
"""

from __future__ import annotations

import math

from cases.gobel40.packing import corners, overlaps
from sqpack.field import FieldElement, NumberField

SOURCE = "[Friedman DS7] section 3, the off-centre family with its column"
SOURCE_URL = "https://kingbird.myphotos.cc/packing/"


def admits(a: int, b: int) -> bool:
    """Does `(a, b)` satisfy the narrowed condition `a - 1/2 < b/sqrt(2) < a + 1/2`?

    Checked in floating point for the same reason as the parent family: the bounds are
    half-integers and `b/sqrt(2)` is irrational, so no boundary case exists for a float
    to get wrong.
    """
    return a >= 1 and b >= 1 and a - 0.5 < b / math.sqrt(2) < a + 0.5


def count(a: int, b: int) -> int:
    """How many squares the construction places."""
    return 2 * a * a + 4 * a + b * b + 1


def column_height(a: int) -> int:
    """Unit squares in the added column: 2a + 1."""
    return 2 * a + 1


def build(
    a: int, b: int
) -> tuple[list[list[tuple[FieldElement, FieldElement]]], FieldElement, NumberField]:
    """Exact corners, side, and the degree-two field for the construction at `(a, b)`."""
    if not admits(a, b):
        raise ValueError(f"a={a}, b={b} does not satisfy a - 1/2 < b/sqrt(2) < a + 1/2")

    field = NumberField((1, 0, -2), (1, 2))
    root = field.alpha
    q = field.rational
    half = q(1) / q(2)
    diagonal = root / q(4)
    width = q(a) + half + q(b) * root / q(2)
    side = width + q(1)
    centre_x = width / q(2)
    centre_y = side / q(2)

    tilted = []
    for u in range(b):
        for v in range(b):
            cx = centre_x + q(2 * (u + v) - 2 * (b - 1)) * root / q(4)
            cy = centre_y + q(2 * (v - u)) * root / q(4)
            tilted.append(corners((cx, cy), (diagonal, diagonal), (-diagonal, diagonal)))

    xs = [q(2 * k + 1) / q(2) for k in range(a)]
    xs += [width - value for value in xs[:a]]
    ys = [q(2 * k + 1) / q(2) for k in range(a)]
    ys += [side - value for value in ys[:a]]
    axis = [
        square
        for cx in xs
        for cy in ys
        for square in [corners((cx, cy), (half, q(0)), (q(0), half))]
        if not any(overlaps(square, block) for block in tilted)
    ]

    column = [
        corners((width + half, q(2 * k + 1) / q(2)), (half, q(0)), (q(0), half))
        for k in range(column_height(a))
    ]

    squares = axis + tilted + column
    assert len(tilted) == b * b, len(tilted)
    assert len(axis) == 2 * a * a + 2 * a, (len(axis), a)
    assert len(column) == column_height(a), len(column)
    assert len(squares) == count(a, b), (len(squares), count(a, b))
    # s = a + 3/2 + b/sqrt(2) satisfies (s - (a + 3/2))^2 = b^2/2.
    offset = side - q(2 * a + 3) / q(2)
    assert offset * offset - q(b * b) / q(2) == field.zero, (
        "the side does not satisfy its own defining relation"
    )
    return squares, side, field


def extra_column_square(a: int, side: FieldElement, field: NumberField):
    """One more column square than fits: its top would stand above the container."""
    q = field.rational
    half = q(1) / q(2)
    return corners(
        (side - half, q(2 * column_height(a) + 1) / q(2)), (half, q(0)), (q(0), half)
    )
