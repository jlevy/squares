"""Frits Göbel's forty-square construction over the certified field Q(sqrt(2)).

Göbel's family, as Friedman's survey states it: if integers `a` and `b` satisfy
`a - 1 < b/sqrt(2) < a + 1`, then `2a^2 + 2a + b^2` unit squares pack into a square of side
`a + 1 + b/sqrt(2)`, by placing a `b` by `b` block of squares at forty-five degrees in the
centre. At `a = 3, b = 4` that is `2*9 + 6 + 16 = 40` squares in side `4 + 2 sqrt(2)`, and
`2 < 2.828... < 4` holds.

**Why this exists.** `BC-049` recorded, correctly at the time, that `n = 40` had no exact
construction retained and that producing one was the price of extending `X-007`'s rigidity
machinery to it. That was true of the repository and not of the mathematics: the
construction is published, it is in a source this project has transcribed, and the retained
decimal witness is a materialisation of it. Every one of that witness's eighty coordinates
fits `p + q sqrt(2)` with half-integer `p` and `q`, its angles are exactly `0` and `45`, and
the only error anywhere is a single `6.04e-31` truncation of the side inherited by the one
coordinate computed from it.

**The frame is derived, not transcribed.** The twenty-four axis-aligned squares are not a
table of positions read off the witness. Their centres can sit at three offsets from each
wall -- `1/2, 3/2, 5/2` and the same from the far side -- which is thirty-six positions, and
the construction is the twelve of those the diagonal block occupies removed. That removal is
computed here, exactly, by the same separating-axis test the verifier uses. Reading the
positions off the witness would have made this file a copy of the thing it is supposed to
check.

The retained witness is then the check rather than the source, and `sqpack.verify` is what
turns the result into a certificate.
"""

from __future__ import annotations

from sqpack.field import FieldElement, NumberField

SOURCE = "[Friedman DS7] section 2, Goebel's centred diagonal block family, a = 3, b = 4"
SOURCE_URL = "https://kingbird.myphotos.cc/packing/square-40.svg"

BLOCK = 4
"""`b`: the diagonal block is `b` by `b`."""

FRAME_OFFSETS = 3
"""`a`: how many unit squares deep the axis-aligned frame is against each wall."""


def _corners(centre, half_x, half_y):
    """The four corners of a unit square from its centre and two half-edge vectors."""
    cx, cy = centre
    ax, ay = half_x
    bx, by = half_y
    return [
        (cx - ax - bx, cy - ay - by),
        (cx + ax - bx, cy + ay - by),
        (cx + ax + bx, cy + ay + by),
        (cx - ax + bx, cy - ay + by),
    ]


def _overlaps(left, right) -> bool:
    """Do these two unit squares overlap in area? Exact separating-axis test.

    Only the four edge normals of the two squares need testing, and here only two are
    distinct up to sign per square. A shared boundary is not an overlap, which is the whole
    point in a tight packing: the test is strict.
    """
    for square in (left, right):
        for index in range(2):
            (px, py), (qx, qy) = square[index], square[(index + 1) % 4]
            axis = (qy - py, px - qx)
            spans = []
            for corners in (left, right):
                values = [x * axis[0] + y * axis[1] for x, y in corners]
                spans.append((min(values, key=_key), max(values, key=_key)))
            if (spans[0][0] - spans[1][1]).sign() >= 0 or (
                spans[1][0] - spans[0][1]
            ).sign() >= 0:
                return False
    return True


def _key(value: FieldElement):
    """Order field elements by sign of the difference, which is exact."""
    return _Comparable(value)


class _Comparable:
    """A total order on field elements, for `min` and `max` without floats."""

    __slots__ = ("value",)

    def __init__(self, value: FieldElement) -> None:
        self.value = value

    def __lt__(self, other: _Comparable) -> bool:
        return (self.value - other.value).sign() < 0


def build():
    """Return exact corners, side, and the degree-two field for the construction."""
    field = NumberField((1, 0, -2), (1, 2))
    root_two = field.alpha
    rational = field.rational
    one = rational(1)
    half = one / rational(2)
    # The forty-five degree half-edge vectors: an edge of length one turned an eighth turn.
    diagonal = root_two / rational(4)
    side = rational(FRAME_OFFSETS + 1) + rational(BLOCK) * root_two / rational(2)

    # The diagonal block. Its cell (u, v) sits at the centre plus (u + v) and (v - u) steps
    # of half a diagonal, which is what a b by b lattice rotated an eighth turn is.
    tilted = []
    for u in range(BLOCK):
        for v in range(BLOCK):
            # One step along a block row is (1/2, -1/2) turned an eighth turn, whose
            # length is one: adjacent cells of the block touch, as they must.
            cx = rational(2) + (rational(u + v) / rational(2) - half) * root_two
            cy = rational(2) + (rational(v - u) / rational(2) + one) * root_two
            tilted.append(_corners((cx, cy), (diagonal, diagonal), (-diagonal, diagonal)))

    # The frame lattice: three offsets from each wall, in both coordinates.
    offsets = [rational(2 * k + 1) / rational(2) for k in range(FRAME_OFFSETS)]
    offsets += [side - value for value in offsets]

    axis = []
    for cx in offsets:
        for cy in offsets:
            square = _corners((cx, cy), (half, rational(0)), (rational(0), half))
            if not any(_overlaps(square, block) for block in tilted):
                axis.append(square)

    squares = axis + tilted
    assert len(tilted) == BLOCK * BLOCK, len(tilted)
    assert len(axis) == 2 * FRAME_OFFSETS * FRAME_OFFSETS + 2 * FRAME_OFFSETS, len(axis)
    assert len(squares) == 2 * FRAME_OFFSETS**2 + 2 * FRAME_OFFSETS + BLOCK**2
    # s = 4 + 2 sqrt 2 satisfies s^2 - 8s + 8 = 0.
    assert side * side - rational(8) * side + rational(8) == field.zero
    return squares, side, field
