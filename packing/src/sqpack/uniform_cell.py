"""Rational outer LPs for one explicitly selected square-packing cell.

The descriptor defines a closed restricted domain, not a complete packing cover. Its
centers are absolute coordinates in ``[0, L]^2`` and its angles are actual rational
half-angle charts, ``theta = 2 atan(t)``. Angle boxes are independent; using them for
shared-angle squares is a conservative relaxation that forgets those equalities.

Every midpoint physical row is relaxed outward using the uniform error proved in the
BC-260 direct hybrid contract. The returned descriptor, midpoint rows and aligned error
vector let an independent reader reconstruct the geometry without trusting a solver.
No infeasibility status, complete case cover or scientific verdict is produced here.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations

from sqpack.exact_lp import ExactLP, ExactLPError, LinearRow, cell_lp_for_axes

type RationalPoint = tuple[Fraction, Fraction]


def _rational(value: object, label: str) -> Fraction:
    if type(value) is int:
        return Fraction(value)
    if type(value) is Fraction:
        return value
    raise ExactLPError("bad-descriptor", f"{label} must be an int or Fraction")


@dataclass(frozen=True, init=False)
class RationalInterval:
    """A finite closed chart or coordinate interval with no floating conversion."""

    lower: Fraction
    upper: Fraction

    def __init__(self, lower: int | Fraction, upper: int | Fraction) -> None:
        low = _rational(lower, "lower endpoint")
        high = _rational(upper, "upper endpoint")
        if low > high:
            raise ExactLPError("bad-descriptor", "interval endpoints are reversed")
        object.__setattr__(self, "lower", low)
        object.__setattr__(self, "upper", high)

    @property
    def midpoint(self) -> Fraction:
        """The exact reference used when reconstructing physical rows."""
        return (self.lower + self.upper) / 2

    @property
    def radius(self) -> Fraction:
        """Half-angle or coordinate radius, without a conversion to radians."""
        return (self.upper - self.lower) / 2


@dataclass(frozen=True)
class PoseBox:
    """Declared center restrictions and actual half-angle bounds for one unit square."""

    x: RationalInterval
    y: RationalInterval
    half_angle: RationalInterval

    def __post_init__(self) -> None:
        if any(
            type(interval) is not RationalInterval
            for interval in (self.x, self.y, self.half_angle)
        ):
            raise ExactLPError("bad-descriptor", "pose bounds must be RationalInterval objects")


@dataclass(frozen=True)
class PairChoice:
    """One directed SAT alternative in ``edge_axes(first) + edge_axes(second)`` order."""

    first: int
    second: int
    axis_position: int
    orientation: int

    def __post_init__(self) -> None:
        values = (self.first, self.second, self.axis_position, self.orientation)
        if any(type(value) is not int for value in values):
            raise ExactLPError(
                "bad-descriptor", "pair choices require integers, excluding bool"
            )
        if not 0 <= self.first < self.second:
            raise ExactLPError("bad-descriptor", "pair labels must satisfy 0 <= first < second")
        if self.axis_position not in range(4) or self.orientation not in (-1, 1):
            raise ExactLPError("bad-descriptor", "invalid directed separating-axis alternative")


@dataclass(frozen=True)
class UniformCellDescriptor:
    """An immutable cell with all pair choices and bounds on every LP variable.

    Center boxes must lie inside the container's outer coordinate envelope. They are
    restrictions defining this cell; a consumer must separately prove they cover its
    intended parent. Square labels are the positions in ``poses``. Choices must list
    every canonical pair once in lexicographic order. All squares have side one.
    """

    poses: tuple[PoseBox, ...]
    side: RationalInterval
    choices: tuple[PairChoice, ...]

    def __post_init__(self) -> None:
        if type(self.poses) is not tuple or len(self.poses) < 2:
            raise ExactLPError("bad-descriptor", "poses must be a tuple of at least two boxes")
        if any(type(pose) is not PoseBox for pose in self.poses):
            raise ExactLPError("bad-descriptor", "poses must contain PoseBox objects")
        if type(self.side) is not RationalInterval or self.side.lower <= 0:
            raise ExactLPError("bad-descriptor", "side must be a strictly positive interval")
        if type(self.choices) is not tuple or any(
            type(choice) is not PairChoice for choice in self.choices
        ):
            raise ExactLPError(
                "bad-descriptor", "choices must be a tuple of PairChoice objects"
            )
        expected = tuple(combinations(range(len(self.poses)), 2))
        actual = tuple((choice.first, choice.second) for choice in self.choices)
        if actual != expected:
            raise ExactLPError("bad-descriptor", "choices must cover every canonical pair once")
        for pose in self.poses:
            for interval in (pose.x, pose.y):
                if interval.lower < 0 or interval.upper > self.side.upper:
                    raise ExactLPError(
                        "bad-descriptor", "center bounds exceed the side envelope"
                    )


@dataclass(frozen=True)
class UniformCell:
    """A descriptor-bound outer LP; ``row_errors`` aligns with every row of ``lp``.

    ``midpoint_lp`` contains only physical geometry. ``lp`` also contains exact
    variable bounds, whose errors are zero. A verifier should reconstruct this object
    from the descriptor before checking any attached infeasibility multipliers.
    """

    descriptor: UniformCellDescriptor
    midpoint_lp: ExactLP
    lp: ExactLP
    row_errors: tuple[Fraction, ...]


def _unit_corners(half_angle: Fraction) -> tuple[RationalPoint, ...]:
    denominator = 1 + half_angle * half_angle
    cosine = (1 - half_angle * half_angle) / denominator
    sine = 2 * half_angle / denominator
    # Counterclockwise order makes edge_axes return (v, -u), both unit normals.
    return tuple(
        ((cosine * x - sine * y) / 2, (sine * x + cosine * y) / 2)
        for x, y in ((-1, -1), (1, -1), (1, 1), (-1, 1))
    )


def _difference_bound(first: RationalInterval, second: RationalInterval) -> Fraction:
    return max(abs(first.lower - second.upper), abs(first.upper - second.lower))


def _physical_errors(descriptor: UniformCellDescriptor) -> dict[str, Fraction]:
    """Bound whole row residuals, including products of changing normals and corners."""
    errors: dict[str, Fraction] = {}
    for index, pose in enumerate(descriptor.poses):
        for corner in range(4):
            for wall in ("left", "bottom", "right", "top"):
                errors[f"wall:{index}:{wall}:{corner}"] = 2 * pose.half_angle.radius
    for choice in descriptor.choices:
        first = descriptor.poses[choice.first]
        second = descriptor.poses[choice.second]
        owner = first if choice.axis_position < 2 else second
        delta = owner.half_angle.radius
        distance = _difference_bound(first.x, second.x) + _difference_bound(first.y, second.y)
        error = (
            2 * delta * distance
            + 8 * delta
            + 4 * first.half_angle.radius
            + 4 * second.half_angle.radius
        )
        for first_corner in range(4):
            for second_corner in range(4):
                label = (
                    f"pair:{choice.first}:{choice.second}:axis{choice.axis_position}:"
                    f"{first_corner}-{second_corner}"
                )
                errors[label] = error
    return errors


def build_uniform_cell(descriptor: UniformCellDescriptor) -> UniformCell:
    """Assemble necessary ``A z <= b + error`` rows on the entire declared box.

    The variable order is all x centers, all y centers, then L. The global derivative
    bounds ``|c'(t)|, |s'(t)| <= 2`` give the corner and axis errors, and every
    uncancelled center coordinate has an explicit descriptor bound. This function does
    not infer a complete SAT cover from its one selected alternative per pair.
    """
    if type(descriptor) is not UniformCellDescriptor:
        raise ExactLPError("bad-descriptor", "expected a UniformCellDescriptor")
    squares = tuple(_unit_corners(pose.half_angle.midpoint) for pose in descriptor.poses)
    choices = {
        (choice.first, choice.second): (choice.axis_position, choice.orientation)
        for choice in descriptor.choices
    }
    midpoint = cell_lp_for_axes(squares, choices, zero=Fraction(0), one=Fraction(1))
    errors = _physical_errors(descriptor)
    if (
        len(midpoint.rows) != len(errors)
        or {row.label for row in midpoint.rows} != errors.keys()
    ):
        raise ExactLPError("geometry-rows", "physical row labels do not match the descriptor")
    rows = list(midpoint.rows)
    row_errors = [errors[row.label] for row in rows]
    rhs = [bound + error for bound, error in zip(midpoint.rhs, row_errors, strict=True)]
    variables = (
        *((f"x:{index}", pose.x) for index, pose in enumerate(descriptor.poses)),
        *((f"y:{index}", pose.y) for index, pose in enumerate(descriptor.poses)),
        ("side", descriptor.side),
    )
    for column, (label, interval) in enumerate(variables):
        for direction, endpoint, suffix in (
            (-1, -interval.lower, "lower"),
            (1, interval.upper, "upper"),
        ):
            coefficients = [Fraction(0)] * midpoint.width
            coefficients[column] = Fraction(direction)
            rows.append(LinearRow(f"bound:{label}:{suffix}", tuple(coefficients)))
            rhs.append(endpoint)
            row_errors.append(Fraction(0))
    outer = ExactLP(
        objective=midpoint.objective,
        rows=tuple(rows),
        rhs=tuple(rhs),
        zero=Fraction(0),
        one=Fraction(1),
    )
    return UniformCell(descriptor, midpoint, outer, tuple(row_errors))
