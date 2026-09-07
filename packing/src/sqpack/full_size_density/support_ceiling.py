"""Exact finite-support geometry and LP adapters; no execution at import time."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction
from typing import cast

from sqpack.exact_lp import ExactLP, LinearRow, rational_sign, solve
from sqpack.field import FieldElement

type Point = tuple[FieldElement, FieldElement]
type Square = tuple[Point, ...]
type SquareKey = tuple[tuple[tuple[Fraction, ...], tuple[Fraction, ...]], ...]

CONTROL_SIDE = 2
PIVOT_CAP = 64
QUARTER_TURNS = 4


class SupportError(ValueError):
    """An exact support, row, or certificate precondition was not established."""


class BoundaryPointError(SupportError):
    """An exact supporting-line equality disqualifies this necessary row."""


@dataclass(frozen=True)
class Support:
    side: FieldElement
    orbits: tuple[tuple[Square, ...], ...]

    @property
    def sizes(self) -> tuple[int, ...]:
        return tuple(len(orbit) for orbit in self.orbits)


@dataclass(frozen=True)
class NecessaryRow:
    point: Point
    radius: Fraction
    coefficients: tuple[int, ...]


@dataclass(frozen=True)
class ControlSolution:
    point: tuple[Fraction, ...]
    multipliers: tuple[Fraction, ...]
    bound: Fraction
    pivots: int


def axis_square(x: FieldElement, y: FieldElement) -> Square:
    """Construct a unit control square from its exact center."""
    half = Fraction(1, 2)
    return (
        (x - half, y - half),
        (x + half, y - half),
        (x + half, y + half),
        (x - half, y + half),
    )


def square_key(square: Square) -> SquareKey:
    """Ignore the starting corner and direction of traversal, without rounding."""
    return tuple(sorted((tuple(x.coeffs), tuple(y.coeffs)) for x, y in square))


def _images(square: Square, side: FieldElement) -> tuple[Square, ...]:
    images: list[Square] = []
    for reflected in (False, True):
        current = tuple((side - x if reflected else x, y) for x, y in square)
        for _ in range(QUARTER_TURNS):
            images.append(current)
            current = tuple((side - y, x) for x, y in current)
    return tuple(images)


def _edges(square: Square, side: FieldElement) -> tuple[Point, Point]:
    if len(square) != QUARTER_TURNS:
        raise SupportError("a square requires four cyclic corners")
    for corner in square:
        if any(
            not isinstance(value, FieldElement) or value.field is not side.field
            for value in corner
        ):
            raise SupportError("geometry requires one exact field")
        if any(value.sign() < 0 or (side - value).sign() < 0 for value in corner):
            raise SupportError("square fails containment")
    x, y = square[0]
    e = (square[1][0] - x, square[1][1] - y)
    f = (square[3][0] - x, square[3][1] - y)
    if (
        e[0] * e[0] + e[1] * e[1] != 1
        or f[0] * f[0] + f[1] * f[1] != 1
        or not (e[0] * f[0] + e[1] * f[1]).is_zero()
        or square[2] != (x + e[0] + f[0], y + e[1] + f[1])
    ):
        raise SupportError("corners do not form an ordered unit square")
    return e, f


def build_control_support(seeds: Sequence[Square], side: FieldElement) -> Support:
    """Deduplicate D4 toy supports; the side guard disables the Trump target."""
    if side != CONTROL_SIDE:
        raise SupportError("target-disabled: only side-two controls are commissioned")
    return build_support(seeds, side)


def build_support(seeds: Sequence[Square], side: FieldElement) -> Support:
    """Construct exactly the D4 closure of at most eleven declared unit squares."""
    if not seeds or len(seeds) > 11 or side.sign() <= 0:
        raise SupportError("support requires one to eleven seeds and a positive side")
    placements: dict[SquareKey, Square] = {}
    for seed in seeds:
        _edges(seed, side)
        for square in _images(seed, side):
            placements.setdefault(square_key(square), square)
    remaining = set(placements)
    for square in placements.values():
        _edges(square, side)
    orbits: list[tuple[Square, ...]] = []
    while remaining:
        representative = placements[min(remaining)]
        keys = sorted({square_key(square) for square in _images(representative, side)})
        orbits.append(tuple(placements[key] for key in keys))
        remaining.difference_update(keys)
    return Support(side, tuple(orbits))


def necessary_row(support: Support, point: Point) -> NecessaryRow:
    """Certify a positive-area constant-incidence neighborhood using projections."""
    side = support.side
    if len(point) != 2 or any(
        not isinstance(value, FieldElement) or value.field is not side.field for value in point
    ):
        raise SupportError("row point uses another field")
    forms = [point[0], side - point[0], point[1], side - point[1]]
    if any(value.sign() <= 0 for value in forms):
        raise SupportError("row point is not strictly inside the container")
    coefficients: list[int] = []
    for orbit in support.orbits:
        count = 0
        for square in orbit:
            e, f = _edges(square, side)
            dx, dy = point[0] - square[0][0], point[1] - square[0][1]
            u, v = dx * e[0] + dy * e[1], dx * f[0] + dy * f[1]
            values = (u, 1 - u, v, 1 - v)
            signs = tuple(value.sign() for value in values)
            if 0 in signs:
                raise BoundaryPointError("row point lies on a supporting boundary line")
            count += int(all(sign > 0 for sign in signs))
            forms.extend(values)
        coefficients.append(count)
    lower_bounds = []
    for value in forms:
        positive = value if value.sign() > 0 else -value
        lower, _ = side.field.enclose(positive)
        if lower <= 0:
            raise SupportError("positive rational margin was not established")
        lower_bounds.append(lower)
    return NecessaryRow(point, min(lower_bounds) / 4, tuple(coefficients))


def checked_rational(value: object) -> Fraction:
    """Refuse floats, booleans, and malformed serialized rational numbers."""
    if type(value) not in (int, Fraction, str):
        raise SupportError("certificate requires exact rational values")
    try:
        return Fraction(cast("int | Fraction | str", value))
    except (ValueError, ZeroDivisionError) as error:
        raise SupportError(f"malformed rational: {value!r}") from error


def check_upper(
    matrix: Sequence[Sequence[int]], sizes: Sequence[int], multipliers: Sequence[object]
) -> Fraction:
    """Verify an LP upper witness directly, without calling the optimizer."""
    if not sizes or any(type(size) is not int or size <= 0 for size in sizes):
        raise SupportError("objective requires positive integer multiplicities")
    if len(matrix) != len(multipliers) or any(len(row) != len(sizes) for row in matrix):
        raise SupportError("certificate dimensions disagree")
    if any(
        type(value) is not int or not 0 <= value <= size
        for row in matrix
        for value, size in zip(row, sizes, strict=True)
    ):
        raise SupportError("incidence must count distinct orbit members")
    weights = tuple(checked_rational(value) for value in multipliers)
    if any(value < 0 for value in weights):
        raise SupportError("negative upper multiplier")
    for column, size in enumerate(sizes):
        if (
            sum(
                (weight * row[column] for weight, row in zip(weights, matrix, strict=True)),
                Fraction(),
            )
            < size
        ):
            raise SupportError(f"upper witness fails column {column}")
    return sum(weights, Fraction())


def solve_control_lp(
    matrix: Sequence[Sequence[int]], sizes: Sequence[int], *, pivot_budget: int = PIVOT_CAP
) -> ControlSolution:
    """Use the explicit nonnegativity basis at zero for a bounded toy relaxation."""
    if (
        not sizes
        or any(type(size) is not int or size <= 0 for size in sizes)
        or any(len(row) != len(sizes) for row in matrix)
    ):
        raise SupportError("invalid LP dimensions or multiplicities")
    if any(
        type(value) is not int or not 0 <= value <= size
        for row in matrix
        for value, size in zip(row, sizes, strict=True)
    ):
        raise SupportError("invalid incidence coefficient")
    if any(not any(row[column] > 0 for row in matrix) for column in range(len(sizes))):
        raise SupportError("uncovered column has no finite-bound guard")
    if type(pivot_budget) is not int or not 0 <= pivot_budget <= PIVOT_CAP:
        raise SupportError("pivot cap exceeds the control commission")
    rows = [
        LinearRow(f"point:{index}", tuple(map(Fraction, row)))
        for index, row in enumerate(matrix)
    ]
    start = tuple(range(len(rows), len(rows) + len(sizes)))
    rows.extend(
        LinearRow(
            f"nonnegative:{column}",
            tuple(Fraction(-int(index == column)) for index in range(len(sizes))),
        )
        for column in range(len(sizes))
    )
    lp = ExactLP(
        tuple(-Fraction(size) for size in sizes),
        tuple(rows),
        (Fraction(1),) * len(matrix) + (Fraction(),) * len(sizes),
        Fraction(),
        Fraction(1),
    )
    solution = solve(lp, start, rational_sign, pivot_budget=pivot_budget)
    weights = [Fraction()] * len(matrix)
    for index, value in zip(solution.vertex.active, solution.vertex.multipliers, strict=True):
        if index < len(matrix):
            weights[index] = value
    bound = check_upper(matrix, sizes, weights)
    point = tuple(checked_rational(value) for value in solution.vertex.point)
    if len(point) != len(sizes) or any(value < 0 for value in point):
        raise SupportError("invalid primal control point")
    if any(
        sum(
            (value * coefficient for value, coefficient in zip(point, row, strict=True)),
            Fraction(),
        )
        > 1
        for row in matrix
    ):
        raise SupportError("primal control point violates an incidence row")
    objective = sum(
        (value * size for value, size in zip(point, sizes, strict=True)), Fraction()
    )
    if bound != objective or bound != -solution.vertex.objective_value:
        raise SupportError("primal and independently checked upper values differ")
    return ControlSolution(point, tuple(weights), bound, solution.pivots)
