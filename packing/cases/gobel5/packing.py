"""Frits Göbel's five-square construction over the certified field Q(sqrt(2))."""

from __future__ import annotations

from sqpack.field import NumberField

SOURCE_URL = "https://kingbird.myphotos.cc/packing/square-5.svg"


def build():
    """Return exact corners, side, and the degree-two field for the construction."""
    # As in the n=10 companion: x^2-2 is irreducible over Q, and monotonicity plus
    # opposite endpoint signs makes (1,2) a unique isolating interval for sqrt(2).
    field = NumberField((1, 0, -2), (1, 2))
    root_two = field.alpha
    rational = field.rational
    one = rational(1)
    half = one / rational(2)
    cosine = root_two / rational(2)
    sine = cosine
    side = rational(2) + root_two / rational(2)

    def axis_aligned(x, y):
        return [(x, y), (x + one, y), (x + one, y + one), (x, y + one)]

    squares = [
        axis_aligned(rational(0), rational(0)),
        axis_aligned(side - one, rational(0)),
        axis_aligned(rational(0), side - one),
        axis_aligned(side - one, side - one),
    ]
    central = []
    for x, y in (
        (rational(0), rational(0)),
        (one, rational(0)),
        (one, one),
        (rational(0), one),
    ):
        shifted_y = y - half
        central.append(
            (one + cosine * x - sine * shifted_y, one + sine * x + cosine * shifted_y)
        )
    squares.append(central)
    assert rational(2) * side * side - rational(8) * side + rational(7) == field.zero
    return squares, side, field
