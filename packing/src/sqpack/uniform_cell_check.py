"""Independent geometry and Farkas replay for a rational uniform square cell.

Only the public receipt types are shared with the producer. Corners, normals, every
physical row, error allowance, and variable bound are reconstructed here without its
builder or the selected-cell assembler. The reader certifies the attached descriptor;
a parent-cover reader must separately bind that descriptor to the intended root.
"""

from __future__ import annotations

from collections.abc import Sequence
from fractions import Fraction

from sqpack.exact_lp import ExactLP, ExactLPError, LinearRow
from sqpack.uniform_cell import (
    PairChoice,
    PoseBox,
    RationalInterval,
    UniformCell,
    UniformCellDescriptor,
)

type Point = tuple[Fraction, Fraction]


def _interval(value: object) -> RationalInterval:
    if type(value) is not RationalInterval:
        raise ExactLPError(
            "bad-descriptor", "each interval must have the declared receipt type"
        )
    lower, upper = getattr(value, "lower", None), getattr(value, "upper", None)
    if type(lower) is not Fraction or type(upper) is not Fraction:
        raise ExactLPError("bad-descriptor", "stored interval endpoints must be Fractions")
    if lower > upper:
        raise ExactLPError("bad-descriptor", "a closed interval has reversed endpoints")
    return value


def _descriptor(value: object) -> UniformCellDescriptor:
    if type(value) is not UniformCellDescriptor:
        raise ExactLPError("bad-descriptor", "missing or invalid uniform-cell descriptor")
    poses, choices = getattr(value, "poses", None), getattr(value, "choices", None)
    side = _interval(getattr(value, "side", None))
    if side.lower <= 0:
        raise ExactLPError("bad-descriptor", "the side interval must be strictly positive")
    if type(poses) is not tuple or len(poses) < 2:
        raise ExactLPError("bad-descriptor", "at least two ordered pose boxes are required")
    for pose in poses:
        if type(pose) is not PoseBox:
            raise ExactLPError(
                "bad-descriptor", "each pose must have the declared receipt type"
            )
        _interval(getattr(pose, "half_angle", None))
        for name in ("x", "y"):
            coordinate = _interval(getattr(pose, name, None))
            if coordinate.lower < 0 or coordinate.upper > side.upper:
                raise ExactLPError("bad-descriptor", "center bounds exceed the side envelope")
    if type(choices) is not tuple:
        raise ExactLPError("bad-descriptor", "pair inventory must be a tuple")
    expected = [(i, j) for i in range(len(poses)) for j in range(i + 1, len(poses))]
    if len(choices) != len(expected):
        raise ExactLPError(
            "bad-descriptor", "the complete pair inventory is missing or repeated"
        )
    for choice, pair in zip(choices, expected, strict=True):
        if type(choice) is not PairChoice:
            raise ExactLPError(
                "bad-descriptor", "each pair choice needs its declared receipt type"
            )
        fields = tuple(
            getattr(choice, name, None)
            for name in ("first", "second", "axis_position", "orientation")
        )
        if any(type(item) is not int for item in fields):
            raise ExactLPError(
                "bad-descriptor", "pair indices and directions must be strict ints"
            )
        if fields[:2] != pair or fields[2] not in range(4) or fields[3] not in (-1, 1):
            raise ExactLPError("bad-descriptor", "invalid or unordered directed pair inventory")
    return value


def _fractions(value: object, count: int, label: str) -> tuple[Fraction, ...]:
    if (
        type(value) is not tuple
        or len(value) != count
        or any(type(item) is not Fraction for item in value)
    ):
        raise ExactLPError("bad-cell", f"{label} must be a tuple of {count} exact Fractions")
    return value


def _program(value: object, width: int, count: int, label: str) -> ExactLP:
    if type(value) is not ExactLP:
        raise ExactLPError("bad-cell", f"{label} has the wrong program type")
    _fractions(getattr(value, "objective", None), width, f"{label} objective")
    _fractions(getattr(value, "rhs", None), count, f"{label} right-hand sides")
    zero, one = getattr(value, "zero", None), getattr(value, "one", None)
    if type(zero) is not Fraction or type(one) is not Fraction or zero != 0 or one != 1:
        raise ExactLPError("bad-cell", f"{label} needs exact rational zero and one")
    rows = getattr(value, "rows", None)
    if type(rows) is not tuple or len(rows) != count:
        raise ExactLPError("bad-cell", f"{label} has an incomplete row inventory")
    for row in rows:
        if type(row) is not LinearRow or type(getattr(row, "label", None)) is not str:
            raise ExactLPError("bad-cell", f"{label} has an invalid labelled row")
        _fractions(getattr(row, "coefficients", None), width, f"{label} coefficients")
    return value


def _unit_geometry(angle: RationalInterval) -> tuple[tuple[Point, ...], tuple[Point, ...]]:
    t = (angle.lower + angle.upper) / 2
    denominator = 1 + t * t
    cosine, sine = (1 - t * t) / denominator, 2 * t / denominator
    diagonal, difference = (cosine + sine) / 2, (cosine - sine) / 2
    corners = (
        (-difference, -diagonal),
        (diagonal, -difference),
        (difference, diagonal),
        (-diagonal, difference),
    )
    # For these counterclockwise corners the first normals are v and -u.
    return corners, ((-sine, cosine), (-cosine, -sine))


def _coordinate_gap(first: RationalInterval, second: RationalInterval) -> Fraction:
    return max(
        abs(left - right)
        for left in (first.lower, first.upper)
        for right in (second.lower, second.upper)
    )


def _reconstruct(
    descriptor: UniformCellDescriptor,
) -> tuple[ExactLP, ExactLP, tuple[Fraction, ...]]:
    """Rebuild the declared conservative envelopes from the geometric derivatives.

    Each component of the normal changes by at most twice its half-angle radius;
    each corner coordinate has the same derivative bound. In a pair row, the normal
    change against the center displacement costs `2 r_owner (Dx + Dy)`. Against the
    two corner offsets it costs at most `8 r_owner`, since each offset coordinate has
    magnitude at most one. Corner changes against the midpoint unit normal cost
    `4 r_first + 4 r_second`. A wall changes by at most `2 r_square`.
    """
    count = len(descriptor.poses)
    width, side_column = 2 * count + 1, 2 * count
    zero, one = Fraction(0), Fraction(1)
    geometry = tuple(_unit_geometry(pose.half_angle) for pose in descriptor.poses)
    radii = tuple(
        (pose.half_angle.upper - pose.half_angle.lower) / 2 for pose in descriptor.poses
    )
    rows: list[LinearRow] = []
    rhs: list[Fraction] = []
    errors: list[Fraction] = []

    def append(
        label: str,
        entries: tuple[tuple[int, Fraction], ...],
        bound: Fraction,
        error: Fraction,
    ) -> None:
        coefficients = [zero] * width
        for column, coefficient in entries:
            coefficients[column] = coefficient
        rows.append(LinearRow(label, tuple(coefficients)))
        rhs.append(bound)
        errors.append(error)

    for square, (corners, _) in enumerate(geometry):
        error = 2 * radii[square]
        for corner, (x, y) in enumerate(corners):
            append(f"wall:{square}:left:{corner}", ((square, -one),), x, error)
            append(f"wall:{square}:bottom:{corner}", ((count + square, -one),), y, error)
            append(
                f"wall:{square}:right:{corner}", ((square, one), (side_column, -one)), -x, error
            )
            append(
                f"wall:{square}:top:{corner}",
                ((count + square, one), (side_column, -one)),
                -y,
                error,
            )
    for choice in descriptor.choices:
        first, second = choice.first, choice.second
        owner = (first, second)[choice.axis_position // 2]
        nx, ny = geometry[owner][1][choice.axis_position % 2]
        before, after = (first, second) if choice.orientation == 1 else (second, first)
        distance = sum(
            (
                _coordinate_gap(
                    getattr(descriptor.poses[first], coordinate),
                    getattr(descriptor.poses[second], coordinate),
                )
                for coordinate in ("x", "y")
            ),
            zero,
        )
        error = (
            2 * radii[owner] * distance + 8 * radii[owner] + 4 * (radii[first] + radii[second])
        )
        entries = ((before, nx), (count + before, ny), (after, -nx), (count + after, -ny))
        for p, (px, py) in enumerate(geometry[before][0]):
            for q, (qx, qy) in enumerate(geometry[after][0]):
                append(
                    f"pair:{first}:{second}:axis{choice.axis_position}:{p}-{q}",
                    entries,
                    nx * (qx - px) + ny * (qy - py),
                    error,
                )
    objective = (zero,) * side_column + (one,)
    midpoint = ExactLP(objective, tuple(rows), tuple(rhs), zero, one)
    rhs = [bound + error for bound, error in zip(rhs, errors, strict=True)]
    coordinates = [(f"x:{i}", pose.x) for i, pose in enumerate(descriptor.poses)]
    coordinates.extend((f"y:{i}", pose.y) for i, pose in enumerate(descriptor.poses))
    coordinates.append(("side", descriptor.side))
    for column, (name, interval) in enumerate(coordinates):
        append(f"bound:{name}:lower", ((column, -one),), -interval.lower, zero)
        append(f"bound:{name}:upper", ((column, one),), interval.upper, zero)
    outer = ExactLP(objective, tuple(rows), tuple(rhs), zero, one)
    return midpoint, outer, tuple(errors)


def check_uniform_cell(cell: UniformCell, multipliers: Sequence[Fraction]) -> Fraction:
    """Certify this closed descriptor's exclusion with a strictly positive rational gap.

    All stored numeric fields and multipliers must be actual Fractions. Producer
    constructors normalize input integers; this receipt boundary rejects bool, float,
    NaN and substituted scalar objects before comparing or multiplying them. Matrix,
    RHS, labels, bounds and errors are bound to the reconstructed descriptor, including
    orientation even though the pair label itself does not encode that direction.
    """
    if type(cell) is not UniformCell:
        raise ExactLPError("bad-cell", "expected a UniformCell receipt")
    descriptor = _descriptor(getattr(cell, "descriptor", None))
    count = len(descriptor.poses)
    width = 2 * count + 1
    physical_count = 16 * (count + count * (count - 1) // 2)
    full_count = physical_count + 2 * width
    midpoint = _program(getattr(cell, "midpoint_lp", None), width, physical_count, "midpoint")
    outer = _program(getattr(cell, "lp", None), width, full_count, "outer")
    errors = _fractions(getattr(cell, "row_errors", None), full_count, "row errors")
    if not isinstance(multipliers, Sequence):
        raise ExactLPError("invalid-certificate", "dual must be a sequence of exact Fractions")
    dual = tuple(multipliers)
    if len(dual) != full_count or any(type(value) is not Fraction for value in dual):
        raise ExactLPError("invalid-certificate", "dual must give one exact Fraction per row")
    expected_midpoint, expected_outer, expected_errors = _reconstruct(descriptor)
    if midpoint != expected_midpoint or outer != expected_outer or errors != expected_errors:
        raise ExactLPError(
            "bad-cell", "stored geometry, bounds or errors differ from the descriptor"
        )

    totals = [Fraction(0)] * width
    bound = Fraction(0)
    for multiplier, row, rhs in zip(dual, outer.rows, outer.rhs, strict=True):
        if multiplier < 0:
            raise ExactLPError("invalid-certificate", "negative Farkas multiplier")
        for column, coefficient in enumerate(row.coefficients):
            totals[column] += multiplier * coefficient
        bound += multiplier * rhs
    if any(total != 0 for total in totals):
        raise ExactLPError("invalid-certificate", "Farkas coefficients do not cancel exactly")
    if bound >= 0:
        raise ExactLPError(
            "invalid-certificate", "Farkas right-hand side is not strictly negative"
        )
    return -bound
