"""Exact overweight-pair separation; a no-hit result is never a depth certificate."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction

from sqpack.field import FieldElement
from sqpack.full_size_density.support_ceiling import (
    Point,
    Square,
    SquareKey,
    SupportError,
    square_key,
)
from sqpack.verify import edge_axes, exact_sign, project, separated, verify_packing

PAIR_CAP = 134
PLACEMENT_CAP = 60


@dataclass(frozen=True)
class WeightedSquare:
    key: SquareKey
    square: Square
    weight: Fraction


@dataclass(frozen=True)
class PairFamily:
    side: FieldElement
    placements: tuple[WeightedSquare, ...]


@dataclass(frozen=True)
class Separation:
    pair: tuple[int, int]
    axis: Point


@dataclass(frozen=True)
class PairWitness:
    pair: tuple[int, int]
    point: Point
    radius: Fraction
    excess: Fraction


@dataclass(frozen=True)
class PairResult:
    eligible: int
    separations: tuple[Separation, ...]
    witness: PairWitness | None


def make_family(
    squares: Sequence[Square], side: FieldElement, weights: Sequence[Fraction]
) -> PairFamily:
    """Validate exact contained unit geometry and deduplicate, without summing duplicates."""
    if not 1 <= len(squares) <= PLACEMENT_CAP or len(squares) != len(weights):
        raise SupportError("pair family dimensions or placement cap violated")
    if not isinstance(side, FieldElement) or side.sign() <= 0:
        raise SupportError("pair family needs a positive exact side")
    entries: dict[SquareKey, WeightedSquare] = {}
    for square, weight in zip(squares, weights, strict=True):
        if type(weight) not in (int, Fraction) or weight < 0:
            raise SupportError("pair weights must be nonnegative exact rationals")
        if len(square) != 4 or any(
            len(point) != 2
            or any(
                not isinstance(value, FieldElement) or value.field is not side.field
                for value in point
            )
            for point in square
        ):
            raise SupportError("pair geometry requires four corners in one exact field")
        if not verify_packing((square,), side, sign=exact_sign).valid:
            raise SupportError("pair member is not a contained unit square")
        key = square_key(square)
        if key in entries and entries[key].weight != weight:
            raise SupportError("duplicate placement has inconsistent weights")
        entries.setdefault(key, WeightedSquare(key, tuple(square), Fraction(weight)))
    return PairFamily(side, tuple(entries[key] for key in sorted(entries)))


def eligible_pairs(family: PairFamily) -> tuple[tuple[int, int], ...]:
    """Only a strict rational overweight can support a pair obstruction."""
    pairs = tuple(
        (i, j)
        for i, first in enumerate(family.placements)
        for j in range(i + 1, len(family.placements))
        if first.weight + family.placements[j].weight > 1
    )
    if len(pairs) > PAIR_CAP:
        raise SupportError("eligible-pair cap exceeded")
    return pairs


def _cross(first: Point, second: Point) -> FieldElement:
    return first[0] * second[1] - first[1] * second[0]


def _subtract(first: Point, second: Point) -> Point:
    return first[0] - second[0], first[1] - second[1]


def _forms(square: Square, point: Point) -> tuple[FieldElement, ...]:
    e = _subtract(square[1], square[0])
    f = _subtract(square[3], square[0])
    displacement = _subtract(point, square[0])
    u = displacement[0] * e[0] + displacement[1] * e[1]
    v = displacement[0] * f[0] + displacement[1] * f[1]
    return u, 1 - u, v, 1 - v


def _intersection_center(first: Square, second: Square) -> Point:
    points = {
        point
        for source, other in ((first, second), (second, first))
        for point in source
        if all(value.sign() >= 0 for value in _forms(other, point))
    }
    for i, p in enumerate(first):
        r = _subtract(first[(i + 1) % 4], p)
        for j, q in enumerate(second):
            s = _subtract(second[(j + 1) % 4], q)
            denominator = _cross(r, s)
            if denominator.is_zero():
                # Collinear segment endpoints are already included by closed membership.
                continue
            difference = _subtract(q, p)
            t, u = _cross(difference, s) / denominator, _cross(difference, r) / denominator
            if 0 <= t <= 1 and 0 <= u <= 1:
                points.add((p[0] + t * r[0], p[1] + t * r[1]))
    if not points:
        raise SupportError("strict SAT overlap has no reconstructed intersection vertices")
    zero = first[0][0].field.zero
    return (
        sum((point[0] for point in points), zero) / len(points),
        sum((point[1] for point in points), zero) / len(points),
    )


def _witness(family: PairFamily, pair: tuple[int, int]) -> PairWitness:
    first, second = (family.placements[index] for index in pair)
    point = _intersection_center(first.square, second.square)
    x, y = point
    forms = (
        *_forms(first.square, point),
        *_forms(second.square, point),
        x,
        y,
        family.side - x,
        family.side - y,
    )
    lower_bounds = []
    for value in forms:
        if value.sign() <= 0:
            raise SupportError("intersection average is not a strict common-interior point")
        lower, _ = family.side.field.enclose(value)
        if lower <= 0:
            raise SupportError("positive rational witness margin was not established")
        lower_bounds.append(lower)
    return PairWitness(pair, point, min(lower_bounds) / 4, first.weight + second.weight - 1)


def _separation(first: Square, second: Square, pair: tuple[int, int]) -> Separation:
    for axis in edge_axes(first) + edge_axes(second):
        alo, ahi = project(first, axis, exact_sign)
        blo, bhi = project(second, axis, exact_sign)
        if (blo - ahi).sign() >= 0:
            return Separation(pair, axis)
        if (alo - bhi).sign() >= 0:
            return Separation(pair, (-axis[0], -axis[1]))
    raise SupportError("SAT separation has no exact axis certificate")


def separate(family: PairFamily) -> PairResult:
    """Stop at the first interior-overlapping overweight pair, retaining preceding axes."""
    pairs = eligible_pairs(family)
    certificates = []
    for pair in pairs:
        first, second = (family.placements[index].square for index in pair)
        # Zero is contact, not overlap; a truthiness check here would be unsound.
        if separated(first, second, exact_sign) is None:
            return PairResult(len(pairs), tuple(certificates), _witness(family, pair))
        certificates.append(_separation(first, second, pair))
    return PairResult(len(pairs), tuple(certificates), None)
