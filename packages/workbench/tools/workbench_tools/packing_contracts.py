"""The workbench's one validity contract for unit-square pose records, in Python.

This is the Python side of `PACKING_VALIDITY` in `src/core/runtime-contracts.ts`: the same
clauses, in the same order, with the same constants and the same separating-axis measure. Both
test runners read the shared boundary fixture `tests/fixtures/packing-validity.json`, and
each must reach its verdict and first failing clause on every case
(`tests/test_packing_validity.py`).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import StrEnum
from numbers import Integral, Real
from typing import Protocol, cast

import numpy as np
from numpy.typing import NDArray

#: The contract identity, shared with `PACKING_VALIDITY.contract`.
VALIDITY_CONTRACT = "packing.squares:PackingValidity/v1"

#: The side of every square in a packing the workbench ranks or reports.
UNIT_SQUARE_SIDE = 1.0

#: The largest pair or wall penetration that still counts as contact (`PACKING_VALIDITY`).
DEFAULT_VALIDITY_TOLERANCE = 1e-9

#: The one declared exception: frames at the catalogue's stored precision
#: (`CATALOGUE_PRECISION`). The builder rounds centres to 1e-6 and angles to 1e-4 degrees, which
#: moves a pair's measured penetration by at most 3.9e-6 and a wall's by 1.2e-6. For displaying
#: records only; nothing that admits or ranks a result may pass it.
#: `tests/test_catalogue_precision.py` re-measures every stored frame against it.
CATALOGUE_PRECISION_TOLERANCE = 4e-6

#: The only tolerances a caller may name. Any other value is a contract error, never a looser
#: check.
DECLARED_TOLERANCES = (DEFAULT_VALIDITY_TOLERANCE, CATALOGUE_PRECISION_TOLERANCE)

#: The contract's clauses in the order an assessment reports the first failure.
CONTRACT_CLAUSES = (
    "count",
    "nonfinite",
    "dimensions",
    "pair-overlap",
    "wall-overlap",
    "area-bound",
    "magnitude",
    "unit-size",
)

#: The largest centre, container origin, container side or square side the float64 measure is
#: trusted at (`PACKING_VALIDITY.coordinateLimit`). Rounding at 2^17 stays under a tenth of the
#: contract tolerance; near 2^52 a centre plus or minus half a side rounds away entirely.
COORDINATE_LIMIT = float(2**16)


class PackingContractError(ValueError):
    """The checker itself was called with an invalid contract."""


class GeometryIssue(StrEnum):
    """Why a supplied pose record is not an admissible packing snapshot.

    `SHAPE` is Python's alone: a record that is not numeric triples cannot reach the typed
    TypeScript assessment. Every other value is the TypeScript clause name.
    """

    SHAPE = "shape"
    COUNT = "count"
    NONFINITE = "nonfinite"
    DIMENSIONS = "dimensions"
    PAIR_OVERLAP = "pair-overlap"
    WALL_ESCAPE = "wall-overlap"
    AREA_BOUND = "area-bound"
    MAGNITUDE = "magnitude"
    UNIT_SIZE = "unit-size"


_MALFORMED = frozenset(
    {
        GeometryIssue.SHAPE,
        GeometryIssue.COUNT,
        GeometryIssue.NONFINITE,
        GeometryIssue.DIMENSIONS,
    }
)


@dataclass(frozen=True, slots=True)
class GeometryCheck:
    """The contract's count, finite, dimension, pair, wall and unit-size check of one record."""

    expected_count: int
    actual_count: int | None
    shape_valid: bool
    finite: bool
    pair_failures: int | None
    wall_failures: int | None
    tolerance: float
    issues: tuple[GeometryIssue, ...]
    square_side: float = UNIT_SQUARE_SIDE
    max_pair_overlap: float | None = None
    max_wall_overlap: float | None = None
    required_side: float | None = None

    @property
    def passed(self) -> bool:
        """Whether every clause holds: a tolerance-qualified packing of unit squares."""
        return not self.issues

    @property
    def geometry_valid(self) -> bool:
        """Whether the pair and wall clauses hold on a well-formed record, whatever the size."""
        return not any(issue is not GeometryIssue.UNIT_SIZE for issue in self.issues)

    @property
    def reason(self) -> str | None:
        """The first failing clause, which is what the TypeScript assessment reports."""
        return self.issues[0].value if self.issues else None


FloatArray = NDArray[np.float64]


class _SupportsFloat(Protocol):
    def __float__(self) -> float: ...


def _contract_values(expected_count: int, tolerance: float) -> tuple[int, float]:
    if (
        isinstance(expected_count, bool)
        or not isinstance(expected_count, Integral)
        or expected_count < 1
    ):
        raise PackingContractError("expected square count must be a positive integer")
    if isinstance(tolerance, bool) or not isinstance(tolerance, Real):
        raise PackingContractError("packing tolerance must be a declared contract tolerance")
    try:
        tolerance_value = float(tolerance)
    except (OverflowError, TypeError, ValueError) as error:
        raise PackingContractError(
            "packing tolerance must be a declared contract tolerance"
        ) from error
    if tolerance_value not in DECLARED_TOLERANCES:
        raise PackingContractError(
            f"packing tolerance {tolerance_value!r} is not a declared contract tolerance "
            f"{DECLARED_TOLERANCES}"
        )
    return int(expected_count), tolerance_value


def _pose_matrix(
    poses: object,
) -> tuple[FloatArray | None, int | None]:
    """Return a strict numeric ``(n, 3)`` matrix and the observable outer count."""
    try:
        raw = np.asarray(poses, dtype=object)
    except TypeError, ValueError:
        return None, None
    actual_count = int(raw.shape[0]) if raw.ndim >= 1 else None
    if raw.ndim != 2 or raw.shape[1] != 3:
        return None, actual_count
    values = raw.reshape(-1).tolist()
    if any(isinstance(value, bool) or not isinstance(value, Real) for value in values):
        return None, actual_count
    try:
        return np.asarray(raw, dtype=np.float64), actual_count
    except OverflowError, TypeError, ValueError:
        return None, actual_count


def _real(value: object) -> float | None:
    if isinstance(value, bool) or not isinstance(value, Real):
        return None
    try:
        return float(cast(_SupportsFloat, value))
    except OverflowError, TypeError, ValueError:
        return math.nan


def _radius_on_axis(
    axis_x: FloatArray, axis_y: FloatArray, cosine: FloatArray, sine: FloatArray, half: float
) -> FloatArray:
    """`squareRadiusOnAxis` in `src/core/geometry.ts`, term for term."""
    return half * (
        np.abs(axis_x * cosine + axis_y * sine) + np.abs(-axis_x * sine + axis_y * cosine)
    )


def pair_penetrations(matrix: FloatArray, square_side: float) -> FloatArray:
    """Separating-axis penetration of each pair that can overlap, as `pairPenetration` measures.

    Pairs whose centres are at least `sqrt(2)` sides apart cannot overlap and are skipped, as
    the TypeScript broad phase skips them. The four face normals of the two squares are the
    only axes.
    """
    count = matrix.shape[0]
    if count < 2:
        return np.zeros(0, dtype=np.float64)
    left, right = np.triu_indices(count, 1)
    dx = matrix[right, 0] - matrix[left, 0]
    dy = matrix[right, 1] - matrix[left, 1]
    near = dx * dx + dy * dy < 2 * square_side * square_side
    left, right, dx, dy = left[near], right[near], dx[near], dy[near]
    left_cosine = np.cos(matrix[left, 2])
    left_sine = np.sin(matrix[left, 2])
    right_cosine = np.cos(matrix[right, 2])
    right_sine = np.sin(matrix[right, 2])
    half = square_side / 2
    penetration = np.full(dx.shape, np.inf)
    separated = np.zeros(dx.shape, dtype=bool)
    for axis_x, axis_y in (
        (left_cosine, left_sine),
        (-left_sine, left_cosine),
        (right_cosine, right_sine),
        (-right_sine, right_cosine),
    ):
        overlap = (
            _radius_on_axis(axis_x, axis_y, left_cosine, left_sine, half)
            + _radius_on_axis(axis_x, axis_y, right_cosine, right_sine, half)
            - np.abs(dx * axis_x + dy * axis_y)
        )
        separated |= overlap <= 0
        penetration = np.minimum(penetration, overlap)
    return np.where(separated, 0.0, penetration)


def wall_penetrations(
    matrix: FloatArray, square_side: float, origin: tuple[float, float], side: float
) -> FloatArray:
    """How far each square reaches outside the container, as `wallPenetration` measures it."""
    x, y, angle = matrix[:, 0], matrix[:, 1], matrix[:, 2]
    radius = square_side / 2 * (np.abs(np.cos(angle)) + np.abs(np.sin(angle)))
    origin_x, origin_y = origin
    return np.maximum.reduce(
        [
            np.zeros_like(x),
            origin_x - (x - radius),
            x + radius - (origin_x + side),
            origin_y - (y - radius),
            y + radius - (origin_y + side),
        ]
    )


def required_side(matrix: FloatArray, square_side: float) -> float:
    """The side of the tight axis-aligned square around all squares, as `packingBounds` fits."""
    x, y, angle = matrix[:, 0], matrix[:, 1], matrix[:, 2]
    radius = square_side / 2 * (np.abs(np.cos(angle)) + np.abs(np.sin(angle)))
    width = float(np.max(x + radius) - np.min(x - radius))
    height = float(np.max(y + radius) - np.min(y - radius))
    return max(width, height)


def check_unit_square_packing(
    poses: object,
    *,
    side: object,
    expected_count: int,
    tolerance: float = DEFAULT_VALIDITY_TOLERANCE,
    origin: tuple[float, float] = (0.0, 0.0),
    square_side: object = UNIT_SQUARE_SIDE,
) -> GeometryCheck:
    """Check centre poses (x, y, radians) against the validity contract, trusting no booleans.

    The container is the axis-aligned square of `side` whose lower-left corner is `origin`.
    Malformed result data becomes a failed receipt rather than an exception so report and
    replay callers can count the rejection. Invalid checker configuration still raises.
    """
    expected_count, tolerance = _contract_values(expected_count, tolerance)
    matrix, actual_count = _pose_matrix(poses)
    side_value = _real(side)
    square_value = _real(square_side)
    origin_values = tuple(_real(value) for value in origin)
    shape_valid = (
        matrix is not None
        and side_value is not None
        and square_value is not None
        and len(origin_values) == 2
        and all(value is not None for value in origin_values)
    )
    numbers = [side_value, square_value, *origin_values]
    finite = bool(
        shape_valid
        and matrix is not None
        and all(value is not None and math.isfinite(value) for value in numbers)
        and np.isfinite(matrix).all()
    )

    issues: list[GeometryIssue] = []
    if not shape_valid:
        issues.append(GeometryIssue.SHAPE)
    if actual_count != expected_count:
        issues.append(GeometryIssue.COUNT)
    if shape_valid and not finite:
        issues.append(GeometryIssue.NONFINITE)
    if finite and not (cast(float, side_value) > 0 and cast(float, square_value) > 0):
        issues.append(GeometryIssue.DIMENSIONS)
    if issues:
        return GeometryCheck(
            expected_count=expected_count,
            actual_count=actual_count,
            shape_valid=shape_valid,
            finite=finite,
            pair_failures=None,
            wall_failures=None,
            tolerance=tolerance,
            issues=tuple(issues),
            square_side=square_value if square_value is not None else math.nan,
        )

    assert matrix is not None
    side_float = cast(float, side_value)
    square_float = cast(float, square_value)
    origin_pair = (cast(float, origin_values[0]), cast(float, origin_values[1]))
    pairs = pair_penetrations(matrix, square_float)
    walls = wall_penetrations(matrix, square_float, origin_pair, side_float)
    pair_failures = int(np.count_nonzero(pairs > tolerance))
    wall_failures = int(np.count_nonzero(walls > tolerance))
    if pair_failures:
        issues.append(GeometryIssue.PAIR_OVERLAP)
    if wall_failures:
        issues.append(GeometryIssue.WALL_ESCAPE)
    fitted_side = required_side(matrix, square_float)
    if fitted_side < area_bound(expected_count, square_float, tolerance):
        issues.append(GeometryIssue.AREA_BOUND)
    lengths = [square_float, side_float, *origin_pair]
    if max(abs(value) for value in lengths) > COORDINATE_LIMIT or (
        float(np.max(np.abs(matrix[:, :2]))) > COORDINATE_LIMIT
    ):
        issues.append(GeometryIssue.MAGNITUDE)
    if square_float != UNIT_SQUARE_SIDE:
        issues.append(GeometryIssue.UNIT_SIZE)
    return GeometryCheck(
        expected_count=expected_count,
        actual_count=actual_count,
        shape_valid=True,
        finite=True,
        pair_failures=pair_failures,
        wall_failures=wall_failures,
        tolerance=tolerance,
        issues=tuple(issues),
        square_side=square_float,
        max_pair_overlap=float(pairs.max()) if pairs.size else 0.0,
        max_wall_overlap=float(walls.max()) if walls.size else 0.0,
        required_side=fitted_side,
    )


def malformed(check: GeometryCheck) -> bool:
    """Whether the record could not be measured: shape, count, finiteness or dimensions."""
    return bool(_MALFORMED.intersection(check.issues))


def area_bound(count: int, square_side: float, tolerance: float) -> float:
    """The smallest side a tolerance-qualified packing of `count` squares can measure.

    Squares whose pairs penetrate by at most `tolerance` still fit without overlap when shrunk
    by twice the tolerance, so their tight side is at least `sqrt(count)` of that; one more
    tolerance allows for rounding. This is `areaBound` in the TypeScript contract.
    """
    return math.sqrt(count) * (square_side - 2 * tolerance) - tolerance
