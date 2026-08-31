"""Goebel's diagonal-strip family, for any `a >= 2`.

`[Friedman DS7]` section 2, Figure 1: a unit-width strip of forty-five-degree squares
crosses the container corner to corner, staircases of axis-aligned squares fill the two
triangles beside it, and one axis-aligned square sits in each of the two corners the strip
runs toward. The side is `a + 1 + sqrt(2)/2` and the count is
`a^2 + a + 3 + floor((a-1) sqrt(2))`, which lands on the best known records at
`n = 27, 38, 52, 67, 84` for `a = 4..8` -- five open cases whose retained ceilings were the
integer grid until this module.

The layout is derived, not transcribed, and every piece of it is forced once three exact
facts are in hand:

- **The strip is the band `a + 1 <= x + y <= a + 1 + sqrt(2)`.** A forty-five-degree unit
  square spans exactly `sqrt(2)` in `x + y`, so the tilted squares fill the band's width
  with equality, and the staircase squares -- integer cells `[i, i+1] x [j, j+1]` with
  `i + j <= a - 1`, and their images under the half-turn -- touch the band's boundary lines
  corner to corner.
- **The tilted centres sit on `x + y = s`, one apart.** Adjacent diamonds meet edge to
  edge, so with `d = x - y` their centres are `sqrt(2)` apart in `d`, symmetric about
  `d = 0`.
- **The corner squares bound the row at exactly Goebel's count.** The extreme diamond
  clears the corner square `[s-1, s] x [0, 1]` by passing over its inner corner
  `(s-1, 1)`, whose `d` is `s - 2 = a - 1 + sqrt(2)/2`; the diamond's largest `d` is
  `d_max + sqrt(2)/2` with `d_max = floor((a-1) sqrt(2)) * sqrt(2)/2 <= a - 1`, so the
  clearance is `a - 1 - d_max >= 0` **because** `floor((a-1) sqrt(2)) <= (a-1) sqrt(2)` --
  and one more diamond in the row violates it, which `verify_exact` keeps as a control.

The row has translation slack of `(a-1) sqrt(2) - floor((a-1) sqrt(2))` along the strip;
this module takes the symmetric position. The retained witnesses take other slack choices
(and other corners), so they share this construction's side and angle census but not its
coordinates -- the evidence is about the construction, exactly as at `n = 82`.

Nothing here claims optimality. `a = 3` is `n = 17`, where the strip is beaten by Bidwell;
the five sizes above are where the family is the best known this repository retains.
"""

from __future__ import annotations

from math import isqrt

from cases.gobel40.packing import corners
from sqpack.field import FieldElement, NumberField

SOURCE = "[Friedman DS7] section 2, Goebel's diagonal-strip family, Figure 1"
SOURCE_URL = "https://kingbird.myphotos.cc/packing/"


def diamonds(a: int) -> int:
    """How many forty-five-degree squares the strip holds: floor((a-1) sqrt(2)) + 1."""
    return isqrt(2 * (a - 1) * (a - 1)) + 1


def count(a: int) -> int:
    """How many squares the construction places."""
    return a * a + a + 2 + diamonds(a)


def build(
    a: int,
) -> tuple[list[list[tuple[FieldElement, FieldElement]]], FieldElement, NumberField]:
    """Exact corners, side, and the degree-two field for the strip at `a`."""
    if a < 2:
        raise ValueError(f"a={a}: the strip needs at least one staircase row")

    field = NumberField((1, 0, -2), (1, 2))
    root = field.alpha
    q = field.rational
    half = q(1) / q(2)
    side = q(a + 1) + root / q(2)

    low = [
        corners((q(2 * i + 1) / q(2), q(2 * j + 1) / q(2)), (half, q(0)), (q(0), half))
        for i in range(a)
        for j in range(a - i)
    ]
    high = [
        corners(
            (side - q(2 * i + 1) / q(2), side - q(2 * j + 1) / q(2)),
            (half, q(0)),
            (q(0), half),
        )
        for i in range(a)
        for j in range(a - i)
    ]
    corner_squares = [
        corners((side - half, half), (half, q(0)), (q(0), half)),
        corners((half, side - half), (half, q(0)), (q(0), half)),
    ]

    m = diamonds(a)
    diagonal = root / q(4)
    tilted = []
    for k in range(m):
        d = q(2 * k - (m - 1)) * root / q(2)
        cx = (side + d) / q(2)
        cy = (side - d) / q(2)
        tilted.append(corners((cx, cy), (diagonal, diagonal), (-diagonal, diagonal)))

    squares = low + high + corner_squares + tilted
    assert len(low) == len(high) == a * (a + 1) // 2, (len(low), a)
    assert len(tilted) == m, (len(tilted), m)
    assert len(squares) == count(a), (len(squares), count(a))
    # s = a + 1 + sqrt(2)/2 satisfies (s - (a+1))^2 = 1/2.
    residual = (side - q(a + 1)) * (side - q(a + 1)) - half
    assert residual == field.zero, "the side does not satisfy its own defining relation"
    return squares, side, field


def extra_diamond(a: int, side: FieldElement, field: NumberField):
    """One more diamond past the row's end: the square Goebel's count says cannot fit.

    Takes `build`'s own side and field, because field elements refuse arithmetic across
    two `NumberField` instances even when the polynomials agree -- which is the guard
    working, not a nuisance to route around.
    """
    root = field.alpha
    q = field.rational
    m = diamonds(a)
    diagonal = root / q(4)
    d = q(m + 1) * root / q(2)
    cx = (side + d) / q(2)
    cy = (side - d) / q(2)
    return corners((cx, cy), (diagonal, diagonal), (-diagonal, diagonal))
