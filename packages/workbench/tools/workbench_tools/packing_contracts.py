"""Fail-closed Python checks for workbench unit-square pose records."""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import StrEnum
from numbers import Integral, Real
from typing import Protocol, cast

import numpy as np
from numpy.typing import NDArray

from sqpack.verify import corners_from_poses, float_sign, verify_packing

DEFAULT_VALIDITY_TOLERANCE = 1e-9


class PackingContractError(ValueError):
    """The checker itself was called with an invalid contract."""


class GeometryIssue(StrEnum):
    """Why a supplied pose record is not an admissible packing snapshot."""

    SHAPE = "shape"
    COUNT = "count"
    NONFINITE = "nonfinite"
    PAIR_OVERLAP = "pair-overlap"
    WALL_ESCAPE = "wall-escape"


@dataclass(frozen=True, slots=True)
class GeometryCheck:
    """The independent count, finite, pair, and wall check for one exact snapshot."""

    expected_count: int
    actual_count: int | None
    shape_valid: bool
    finite: bool
    pair_failures: int | None
    wall_failures: int | None
    tolerance: float
    issues: tuple[GeometryIssue, ...]

    @property
    def passed(self) -> bool:
        """Whether the supplied snapshot is a tolerance-qualified packing."""
        return not self.issues


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
        raise PackingContractError("packing tolerance must be finite and non-negative")
    try:
        tolerance_value = float(tolerance)
    except (OverflowError, TypeError, ValueError) as error:
        raise PackingContractError(
            "packing tolerance must be finite and non-negative"
        ) from error
    if not math.isfinite(tolerance_value) or tolerance_value < 0:
        raise PackingContractError("packing tolerance must be finite and non-negative")
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


def check_unit_square_packing(
    poses: object,
    *,
    side: object,
    expected_count: int,
    tolerance: float = DEFAULT_VALIDITY_TOLERANCE,
) -> GeometryCheck:
    """Check lower-left, radian centre poses without trusting producer booleans.

    Malformed result data becomes a failed receipt rather than an exception so report and
    replay callers can count the rejection. Invalid checker configuration still raises.
    """
    expected_count, tolerance = _contract_values(expected_count, tolerance)
    matrix, actual_count = _pose_matrix(poses)
    shape_valid = matrix is not None and isinstance(side, Real) and not isinstance(side, bool)
    try:
        side_value = float(cast(_SupportsFloat, side)) if shape_valid else math.nan
    except OverflowError, TypeError, ValueError:
        side_value = math.nan
    finite = bool(
        shape_valid
        and math.isfinite(side_value)
        and side_value > 0
        and matrix is not None
        and np.isfinite(matrix).all()
    )

    issues: list[GeometryIssue] = []
    if not shape_valid:
        issues.append(GeometryIssue.SHAPE)
    if actual_count != expected_count:
        issues.append(GeometryIssue.COUNT)
    if shape_valid and not finite:
        issues.append(GeometryIssue.NONFINITE)
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
        )

    assert matrix is not None
    corners = corners_from_poses(matrix[:, 0], matrix[:, 1], matrix[:, 2])
    report = verify_packing(
        corners,
        side_value,
        sign=float_sign(tolerance),
        check_shapes=False,
    )
    pair_failures = sum(kind == "overlap" for kind, _detail in report.failures)
    wall_failures = sum(kind == "container" for kind, _detail in report.failures)
    if pair_failures:
        issues.append(GeometryIssue.PAIR_OVERLAP)
    if wall_failures:
        issues.append(GeometryIssue.WALL_ESCAPE)
    return GeometryCheck(
        expected_count=expected_count,
        actual_count=actual_count,
        shape_valid=True,
        finite=True,
        pair_failures=pair_failures,
        wall_failures=wall_failures,
        tolerance=tolerance,
        issues=tuple(issues),
    )
