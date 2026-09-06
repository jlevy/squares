"""Solver-independent BC-254 toy replay using oriented edge determinants.

No target loader or CLI is commissioned. Callers supply the declared toy seeds, not
just a matrix or a claimed support, so omissions and orbit-count mutations are checked.
"""

from __future__ import annotations

from collections.abc import Sequence
from fractions import Fraction

from sqpack.field import FieldElement
from sqpack.full_size_density.support_ceiling import (
    NecessaryRow,
    Square,
    Support,
    SupportError,
    check_upper,
    checked_rational,
)


def _key(square: Square):
    return tuple(sorted((tuple(x.coeffs), tuple(y.coeffs)) for x, y in square))


def _orbit(seed: Square, side: FieldElement):
    # Explicit coordinate maps are separate from the producer's iterative rotations.
    transforms = (
        lambda x, y: (x, y),
        lambda x, y: (side - y, x),
        lambda x, y: (side - x, side - y),
        lambda x, y: (y, side - x),
        lambda x, y: (side - x, y),
        lambda x, y: (side - y, side - x),
        lambda x, y: (x, side - y),
        lambda x, y: (y, x),
    )
    return {_key(tuple(transform(x, y) for x, y in seed)) for transform in transforms}


def replay_upper(
    seeds: Sequence[Square],
    support: Support,
    rows: Sequence[NecessaryRow],
    multipliers: Sequence[object],
) -> Fraction:
    """Regenerate support identity, strict neighborhoods, and the upper inequality."""
    side = support.side
    if side != 2:
        raise SupportError("target-disabled: replay is commissioned only for side-two toys")
    expected = sorted(
        {_key_orbit for seed in seeds for _key_orbit in (tuple(sorted(_orbit(seed, side))),)}
    )
    actual = [tuple(_key(square) for square in orbit) for orbit in support.orbits]
    if actual != expected:
        raise SupportError("support or orbit multiplicities disagree with declared source")
    if not expected:
        raise SupportError("empty source support")
    matrix: list[tuple[int, ...]] = []
    for row in rows:
        if any(type(value) is not int for value in row.coefficients):
            raise SupportError("incidence coefficients require exact integers")
        radius = checked_rational(row.radius)
        if radius <= 0:
            raise SupportError("neighborhood radius must be positive")
        px, py = row.point
        margins = [px, side - px, py, side - py]
        if any((value - 2 * radius).sign() <= 0 for value in margins):
            raise SupportError("neighborhood crosses the container boundary")
        counts: list[int] = []
        for orbit in support.orbits:
            count = 0
            for square in orbit:
                if len(square) != 4:
                    raise SupportError("square has wrong corner count")
                edges = []
                for index, (x, y) in enumerate(square):
                    if x.field is not side.field or y.field is not side.field:
                        raise SupportError("geometry field mismatch")
                    if any(value.sign() < 0 or (side - value).sign() < 0 for value in (x, y)):
                        raise SupportError("square fails containment")
                    nx, ny = square[(index + 1) % 4]
                    dx, dy = nx - x, ny - y
                    if dx * dx + dy * dy != 1:
                        raise SupportError("square edge is not unit length")
                    edges.append((dx, dy))
                ex, ey = edges[0]
                fx, fy = edges[1]
                if (
                    not (ex * fx + ey * fy).is_zero()
                    or edges[2] != (-ex, -ey)
                    or edges[3] != (-fx, -fy)
                ):
                    raise SupportError("corners are not a cyclic unit square")
                orientation = (ex * fy - ey * fx).sign()
                if orientation == 0:
                    raise SupportError("degenerate square")
                signs = []
                for (x, y), (dx, dy) in zip(square, edges, strict=True):
                    value = orientation * (dx * (py - y) - dy * (px - x))
                    sign = value.sign()
                    absolute = value if sign > 0 else -value
                    if sign == 0 or (absolute - 2 * radius).sign() <= 0:
                        raise SupportError("boundary or uncertified neighborhood")
                    signs.append(sign)
                count += int(all(sign > 0 for sign in signs))
            counts.append(count)
        if tuple(counts) != row.coefficients:
            raise SupportError("claimed incidence disagrees with determinant replay")
        matrix.append(tuple(counts))
    return check_upper(matrix, support.sizes, multipliers)
