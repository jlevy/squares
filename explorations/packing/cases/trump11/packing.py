"""Walter Trump's 1979 packing of 11 unit squares, exactly.

This is the best known packing for `n = 11`, the smallest case where `s(n)`
is unknown, and the smallest where the optimal packing is believed to need a
tilt that is neither 0 nor 45 degrees.

The layout is reconstructed from David Ellsworth's SVG on the *Squares in
Squares* record page: six axis-aligned squares plus a block of five rotated
by `a`, where the block's offsets `x0, r1, u1, v1, v2` are the closed forms
given there.

Everything is expressed in `Q(u)` with `u = tan(a/2)`, so `cos a` and
`sin a` are rational in `u` and no transcendental function appears.  The
minimal polynomial of `u` is derived in `derive_field.py`; the container side
is then `s = (6u + 4) / (-u^2 + 2u + 1)`, whose minimal polynomial is the
published degree-8

    s^8 - 20s^7 + 178s^6 - 842s^5 + 1923s^4 - 496s^3 - 6754s^2 + 12420s - 6865
"""

from __future__ import annotations

from sqpack.field import NumberField

# Minimal polynomial of u = tan(a/2), highest degree first, and an isolating
# interval containing the intended root (a is about 40.18 degrees).
U_MIN_POLY = (5, -10, -2, 14, 12, -6, 2, 2, -1)
U_INTERVAL = ("36/100", "37/100")

# Minimal polynomial of the container side, as published.
S_MIN_POLY = (1, -20, 178, -842, 1923, -496, -6754, 12420, -6865)


def build():
    """Return ``(squares, side, field)`` for Trump's packing.

    ``squares`` is a list of 11 squares, each a list of four corners in
    order; every coordinate is a :class:`~sqpack.field.FieldElement`.
    """
    field = NumberField(U_MIN_POLY, U_INTERVAL)
    u = field.alpha
    K = field.rational

    one_plus_u2 = K(1) + u * u
    cos_a = (K(1) - u * u) / one_plus_u2
    sin_a = (K(2) * u) / one_plus_u2
    assert (cos_a * cos_a + sin_a * sin_a - K(1)).is_zero()

    # s = 2 + (2 + sin a) / (cos a + sin a), rationalised in u.
    side = (K(6) * u + K(4)) / (K(1) + K(2) * u - u * u)

    r1 = K(1) - (side - K(3)) * cos_a
    u1 = ((K(1) + r1) * cos_a - K(1)) / sin_a
    v1 = cos_a - sin_a
    v2 = (side - K(1)) / sin_a - r1 - (K(3) + u1) * (cos_a / sin_a)
    x0 = K(1) + K(2) / cos_a - (side - K(2)) * (sin_a / cos_a)

    def axis_aligned(x, y):
        return [(x, y), (x + K(1), y), (x + K(1), y + K(1)), (x, y + K(1))]

    def tilted(ox, oy):
        # The block transform is translate(1,1) . rotate(a) . translate(0,-r1)
        corners = []
        for dx, dy in ((K(0), K(0)), (K(1), K(0)), (K(1), K(1)), (K(0), K(1))):
            px, py = ox + dx, oy + dy - r1
            corners.append((K(1) + cos_a * px - sin_a * py, K(1) + sin_a * px + cos_a * py))
        return corners

    squares = [
        axis_aligned(K(0), K(0)),
        axis_aligned(side - K(1), K(0)),
        axis_aligned(x0, side - K(1)),
        axis_aligned(K(0), side - K(1)),
        axis_aligned(K(1), side - K(1)),
        axis_aligned(K(0), side - K(2)),
        tilted(K(0), K(0)),
        tilted(u1, -K(1)),
        tilted(K(1), v1),
        tilted(u1 + K(1), v1 - K(1)),
        tilted(u1 + K(2), -v2),
    ]
    assert len(squares) == 11
    return squares, side, field


def side_satisfies_published_polynomial(side, field) -> bool:
    """Check ``P(side) == 0`` exactly for the published degree-8 polynomial."""
    acc = field.zero
    for c in S_MIN_POLY:
        acc = acc * side + field.rational(c)
    return acc.is_zero()
