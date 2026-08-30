"""Goebel's centred-diagonal-block family, for any `(a, b)` it admits.

`cases/gobel40` is this construction at `a = 3, b = 4`, written when `n = 40` was the only
size that needed it. The rule is general, and
`campaign/series/series-000-smoke-and-calibration/results/bc-049-gobel-family-coverage.json`
measures where it lands: twelve sizes below 100, and at four of them the side is *exactly*
the best known this repository retains -- `n = 5`, `40`, `65` and `89`.

The first two have exact constructions here. **This module is why the other two do.**

Goebel's rule, as `[Friedman DS7]` states it: for integers `a, b` with
`a - 1 < b / sqrt(2) < a + 1`, exactly `2a^2 + 2a + b^2` unit squares pack into a square of
side `a + 1 + b / sqrt(2)`, by setting a `b` by `b` block at forty-five degrees in the
middle of a frame `a` squares deep.

**The frame is derived, not transcribed**, exactly as at `n = 40` and for the same reason.
Its centres may sit at `a` offsets from each wall, which is `(2a)^2` positions, and the
construction is that lattice minus the ones the diagonal block occupies -- computed here by
the exact separating-axis test rather than read off a witness. A wrong `(a, b)` therefore
produces a wrong count rather than a plausible picture, and the assertion at the end is
what turns that into a stop.

Nothing here claims optimality. The family being *at* the best known side for four sizes is
a fact about the retained record; that those packings are optimal is not shown, here or
anywhere in this repository.
"""

from __future__ import annotations

import math

from cases.gobel40.packing import corners, overlaps
from sqpack.field import FieldElement, NumberField

SOURCE = "[Friedman DS7] section 2, Goebel's centred diagonal block family"
SOURCE_URL = "https://kingbird.myphotos.cc/packing/"


def admits(a: int, b: int) -> bool:
    """Does `(a, b)` satisfy Goebel's condition?

    Checked in floating point because the condition is a strict inequality on `b / sqrt(2)`
    with integer bounds, and the only way it could be close is `b / sqrt(2)` landing on an
    integer -- which it never does, `sqrt(2)` being irrational. So there is no boundary case
    for a float to get wrong.
    """
    return a >= 1 and b >= 1 and a - 1 < b / math.sqrt(2) < a + 1


def count(a: int, b: int) -> int:
    """How many squares the construction places."""
    return 2 * a * a + 2 * a + b * b


def build(
    a: int, b: int
) -> tuple[list[list[tuple[FieldElement, FieldElement]]], FieldElement, NumberField]:
    """Exact corners, side, and the degree-two field for the construction at `(a, b)`."""
    if not admits(a, b):
        raise ValueError(f"a={a}, b={b} does not satisfy a - 1 < b/sqrt(2) < a + 1")

    field = NumberField((1, 0, -2), (1, 2))
    root = field.alpha
    q = field.rational
    half = q(1) / q(2)
    # A forty-five degree half-edge: an edge of length one turned an eighth turn.
    diagonal = root / q(4)
    side = q(a + 1) + q(b) * root / q(2)
    centre = side / q(2)

    # The block, laid out from its own centre rather than from a corner, so the same
    # expression works for even and odd `b` without a case split.
    tilted = []
    for u in range(b):
        for v in range(b):
            cx = centre + q(2 * (u + v) - 2 * (b - 1)) * root / q(4)
            cy = centre + q(2 * (v - u)) * root / q(4)
            tilted.append(corners((cx, cy), (diagonal, diagonal), (-diagonal, diagonal)))

    offsets = [q(2 * k + 1) / q(2) for k in range(a)]
    offsets += [side - value for value in offsets]
    axis = [
        square
        for cx in offsets
        for cy in offsets
        for square in [corners((cx, cy), (half, q(0)), (q(0), half))]
        if not any(overlaps(square, block) for block in tilted)
    ]

    squares = axis + tilted
    assert len(tilted) == b * b, len(tilted)
    assert len(axis) == 2 * a * a + 2 * a, (len(axis), a)
    assert len(squares) == count(a, b), (len(squares), count(a, b))
    # s = a + 1 + b/sqrt(2) satisfies (s - (a+1))^2 = b^2/2.
    residual = (side - q(a + 1)) * (side - q(a + 1)) - q(b * b) / q(2)
    assert residual == field.zero, "the side does not satisfy its own defining relation"
    return squares, side, field
