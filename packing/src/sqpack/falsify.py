"""Escaping-pose falsifier for unavoidable point sets.

The certifier half of the instrument (`sqpack.cover`) decides that a declared cover
holds; this module is the other half, built under `BC-094`: given marked points in a
container, it *searches* poses `(x, y, theta)` for a box -- an open square of side
strictly greater than one -- that avoids every point, and certifies a found escape
exactly.  The division of labor is strict and asymmetric:

- the search runs in floating point and proves nothing;
- a found candidate becomes a result only through `certify_escape`, where every
  decision is an exact sign in the caller's field;
- a search that finds nothing yields a `SaturationReport`, and **a saturation is
  never a proof of unavoidability** -- only a cover certificate decides that
  direction.  The report says exactly how hard it looked and what defeated it.

The known-answer triple that calibrates this module (think-yrvm, H-010's history):
the search must find the Figure 13 escape at `s = 2 + 4/sqrt(5)`, must saturate on
the repaired twelve-point Figure 14 set, and every refusal must name the defeating
pose.  Those live in `tests/test_falsify.py`.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from scipy.optimize import minimize

from sqpack.cover import (
    avoidance_margin,
    box_corners,
    corner_clearances,
    exact_min,
    validate_box_shape,
)

#: Fixed wording, retained in every saturation report so a reader can never mistake
#: a tired search for a theorem.
SATURATION_CAVEAT = "search saturation is not a proof of unavoidability"

type FloatPoint = tuple[str, float, float]
type Scalar = Any
type ExactPoint = tuple[Scalar, Scalar]


class CertificationRefusedError(ValueError):
    """An exact check refused the candidate; the message names what defeated it."""

    def __init__(self, reason: str, defeated_by: str):
        super().__init__(f"{reason} (defeated by {defeated_by})")
        self.defeated_by = defeated_by


@dataclass(frozen=True)
class EscapeCandidate:
    """A float pose whose minimum avoidance margin is positive; not yet a result."""

    x: float
    y: float
    theta: float
    margin: float
    closest_point: str


@dataclass(frozen=True)
class SaturationReport:
    """The search exhausted its declared resolution without a positive margin."""

    theta_steps: int
    xy_steps: int
    candidates_tested: int
    refinements: int
    best_margin: float
    best_x: float
    best_y: float
    best_theta: float
    defeating_point: str
    caveat: str = SATURATION_CAVEAT


def float_margin(
    x: float, y: float, theta: float, half: float, points: list[FloatPoint]
) -> tuple[float, str]:
    """Minimum local-frame L-infinity margin over the points; positive means escape."""
    cosine, sine = math.cos(theta), math.sin(theta)
    best = math.inf
    label = ""
    for name, px, py in points:
        dx, dy = px - x, py - y
        local_u = cosine * dx + sine * dy
        local_v = -sine * dx + cosine * dy
        margin = max(abs(local_u) - half, abs(local_v) - half)
        if margin < best:
            best, label = margin, name
    return best, label


def feasible_center_interval(theta: float, side: float, length: float) -> tuple[float, float]:
    """Closed interval each center coordinate must lie in for the box to fit."""
    half_width = (length / 2) * (abs(math.cos(theta)) + abs(math.sin(theta)))
    return half_width, side - half_width


def _clamp(value: float, low: float, high: float) -> float:
    return low if value < low else min(value, high)


def search_escape(
    points: list[FloatPoint],
    side: float,
    length: float,
    *,
    theta_steps: int = 48,
    xy_steps: int = 32,
    refine_top: int = 8,
) -> EscapeCandidate | SaturationReport:
    """Deterministic coarse grid over (x, y, theta), then local refinement.

    Theta ranges over [0, pi/2): a square box is invariant under quarter turns.  The
    grid stays inside the feasible center region for each angle, so container fit is
    a constraint rather than a term of the objective -- the retained escapes touch
    the wall exactly, and a fit term would bias the search away from them.
    """
    half = length / 2
    evaluated: list[tuple[float, float, float, float]] = []
    tested = 0
    for theta_index in range(theta_steps):
        theta = (math.pi / 2) * theta_index / theta_steps
        low, high = feasible_center_interval(theta, side, length)
        if high < low:
            continue
        for x_index in range(xy_steps):
            x = low + (high - low) * x_index / (xy_steps - 1)
            for y_index in range(xy_steps):
                y = low + (high - low) * y_index / (xy_steps - 1)
                margin, _ = float_margin(x, y, theta, half, points)
                tested += 1
                evaluated.append((margin, x, y, theta))
    evaluated.sort(key=lambda item: -item[0])

    best_margin, best_x, best_y, best_theta = evaluated[0]
    refinements = 0
    for _margin, x, y, theta in evaluated[:refine_top]:
        refinements += 1

        def negated(pose: Any) -> float:
            pose_theta = _clamp(pose[2], 0.0, math.pi / 2 * 0.9999)
            low, high = feasible_center_interval(pose_theta, side, length)
            if high < low:
                return math.inf
            pose_x = _clamp(pose[0], low, high)
            pose_y = _clamp(pose[1], low, high)
            value, _ = float_margin(pose_x, pose_y, pose_theta, half, points)
            return -value

        result = minimize(
            negated,
            [x, y, theta],
            method="Nelder-Mead",
            options={"xatol": 1e-12, "fatol": 1e-14},
        )
        refined_theta = _clamp(float(result.x[2]), 0.0, math.pi / 2 * 0.9999)
        low, high = feasible_center_interval(refined_theta, side, length)
        refined_x = _clamp(float(result.x[0]), low, high)
        refined_y = _clamp(float(result.x[1]), low, high)
        refined_margin, _ = float_margin(refined_x, refined_y, refined_theta, half, points)
        if refined_margin > best_margin:
            best_margin, best_x, best_y, best_theta = (
                refined_margin,
                refined_x,
                refined_y,
                refined_theta,
            )

    _, defeating = float_margin(best_x, best_y, best_theta, half, points)
    if best_margin > 0:
        return EscapeCandidate(
            x=best_x, y=best_y, theta=best_theta, margin=best_margin, closest_point=defeating
        )
    return SaturationReport(
        theta_steps=theta_steps,
        xy_steps=xy_steps,
        candidates_tested=tested,
        refinements=refinements,
        best_margin=best_margin,
        best_x=best_x,
        best_y=best_y,
        best_theta=best_theta,
        defeating_point=defeating,
    )


def rationalize_pose(
    candidate: EscapeCandidate, *, max_denominator: int = 10_000
) -> tuple[Fraction, Fraction, Fraction]:
    """Nearby rational (tan theta, x, y) for the exact certification bridge."""
    tangent = Fraction(math.tan(candidate.theta)).limit_denominator(max_denominator)
    x = Fraction(candidate.x).limit_denominator(max_denominator)
    y = Fraction(candidate.y).limit_denominator(max_denominator)
    return tangent, x, y


def certify_escape(
    *,
    side: Scalar,
    length: Scalar,
    center: ExactPoint,
    cosine: Scalar,
    sine: Scalar,
    points: list[tuple[str, ExactPoint]],
) -> dict[str, object]:
    """Exact certificate that the box strictly avoids every point and fits.

    Every input is a scalar in the caller's field; every decision below is an exact
    sign.  Boundary contact with the container is permitted and recorded, exactly as
    the retained escapes permit it; a negative clearance, a wrong shape, a side not
    exceeding one, or any non-positive avoidance margin is a typed refusal naming
    what defeated the candidate.
    """
    one = length / length
    if (length - one).sign() <= 0:
        raise CertificationRefusedError("side must strictly exceed one", "length")
    if (cosine * cosine + sine * sine - one).sign() != 0:
        raise CertificationRefusedError("orientation is not a unit vector", "orientation")
    half = length / 2
    corners = box_corners(center, half, cosine, sine)
    validate_box_shape(corners, length)

    clearances = corner_clearances(corners, side)
    for label, value in clearances:
        if value.sign() < 0:
            raise CertificationRefusedError("box leaves the container", label)
    contacts = [label for label, value in clearances if value.sign() == 0]

    margins: list[tuple[str, Scalar]] = []
    for label, point in points:
        margin, _ = avoidance_margin(point, center, half, cosine, sine)
        if margin.sign() <= 0:
            raise CertificationRefusedError("box does not strictly avoid a point", label)
        margins.append((label, margin))
    closest_label, closest_margin = exact_min(margins)

    return {
        "all_points_strictly_avoided": True,
        "point_count": len(points),
        "exact_boundary_contacts": contacts,
        "minimum_avoidance_margin_point": closest_label,
        "minimum_avoidance_margin_sign": closest_margin.sign(),
        "all_decisions": "exact signs in the caller's field",
    }
