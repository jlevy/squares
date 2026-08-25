"""Frits Göbel's ten-square construction over the certified field Q(sqrt(2))."""

from __future__ import annotations

from sqpack.field import NumberField


def build():
    """Return exact corners, side, and the degree-two field for the construction."""
    # x^2 - 2 is irreducible over Q by the rational-root theorem. Its derivative is
    # positive on (1, 2), and its endpoint signs differ, so this interval contains the
    # unique positive root. These are the field preconditions the generic constructor
    # does not yet enforce for arbitrary caller input.
    field = NumberField((1, 0, -2), (1, 2))
    root_two = field.alpha
    rational = field.rational
    half = rational(1) / rational(2)
    quarter_root = root_two / rational(4)
    side = rational(3) + root_two / rational(2)

    centers = [
        (half, half),
        (rational(3) / rational(2), half),
        (half, rational(3) / rational(2)),
        (side - half, half),
        (side - half, side - half),
        (side - rational(3) / rational(2), side - half),
        (side - half, side - rational(3) / rational(2)),
        (half, side - half),
    ]

    def axis_aligned(center):
        x, y = center
        return [
            (x - half, y - half),
            (x + half, y - half),
            (x + half, y + half),
            (x - half, y + half),
        ]

    def diagonal(center):
        x, y = center
        return [
            (x, y - root_two / rational(2)),
            (x + root_two / rational(2), y),
            (x, y + root_two / rational(2)),
            (x - root_two / rational(2), y),
        ]

    squares = [axis_aligned(center) for center in centers]
    middle = rational(3) / rational(2)
    radius = root_two / rational(2)
    squares.extend(
        [
            diagonal((middle + radius, middle)),
            diagonal((middle, middle + radius)),
        ]
    )
    assert quarter_root * quarter_root == rational(1) / rational(8)
    assert rational(2) * side * side - rational(12) * side + rational(17) == field.zero
    return squares, side, field
