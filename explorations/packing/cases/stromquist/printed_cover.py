#!/usr/bin/env python3
"""Replay the printed mechanism of Stromquist's Theorem 2 exactly.

This checker does *not* certify the theorem.  It reconstructs the finite data in
Figures 13 and 14, checks the valid parts of the conditional counting mechanism,
and then terminates with an exact counterexample to the printed Figure 14
unavoidability claim.  In particular, it must never turn search saturation into a
covering proof.

The decisive witness is an open square (a "box" in the paper) of side 10001/10000
inside the claimed container.  All coordinates lie in Q(sqrt(5), sqrt(829)); every
container and point-avoidance decision is therefore an exact algebraic sign test.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
import time
from collections.abc import Callable
from fractions import Fraction
from pathlib import Path

import sympy as sp

from sqpack.field import FieldElement, NumberField
from sqpack.verify import exact_sign, verify_packing

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_VERSION = 1
PAPER = ROOT / "resources/papers/stromquist-2003-packing-10-or-11-unit-squares.pdf"
RAW_TEXT = ROOT / "resources/papers/stromquist-2003-packing-10-or-11-unit-squares.raw.md"
EXPECTED_SOURCE_HASHES = {
    "paper_sha256": "146ac14a015910a95d0c25bf986f6073bcccd21a29ee754a45dcc0d4224d5e0b",
    "raw_text_sha256": "5808f3152c2d3a409c54d1f6ebb2636b7500eb22d489ccf9908435007d8a1d6b",
}

ExactPoint = tuple[FieldElement, FieldElement]
ExactEdge = tuple[ExactPoint, ExactPoint]
RationalEndpoint = int | Fraction


def sha256(path: Path) -> str:
    """Return the byte-level source identity used by this transcription."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fraction_text(value: Fraction) -> str:
    """Serialize a rational without losing its denominator."""
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def exact_value(value: FieldElement) -> dict[str, object]:
    """Serialize a field element in its exact power-basis representation."""
    return {
        "coefficients_low_to_high": [fraction_text(c) for c in value.coeffs],
        "decimal_for_display_only": format(float(value), ".16g"),
    }


def exact_abs(value: FieldElement) -> FieldElement:
    return value if value.sign() >= 0 else -value


def exact_max(left: FieldElement, right: FieldElement) -> tuple[FieldElement, str]:
    if (left - right).sign() >= 0:
        return left, "u"
    return right, "v"


def exact_min(
    labelled: list[tuple[str, FieldElement]],
) -> tuple[str, FieldElement]:
    if not labelled:
        raise ValueError("cannot take the minimum of an empty exact list")
    label, value = labelled[0]
    for candidate_label, candidate in labelled[1:]:
        if (candidate - value).sign() < 0:
            label, value = candidate_label, candidate
    return label, value


def object_dict(value: object, label: str) -> dict[str, object]:
    """Narrow a nested evidence object without making the record dynamically typed."""
    if not isinstance(value, dict):
        raise TypeError(f"{label} evidence is not a mapping")
    return value


def checked_number_field(
    min_poly: tuple[int, ...],
    isolating: tuple[RationalEndpoint, RationalEndpoint],
) -> tuple[NumberField, dict[str, bool]]:
    """Construct a field only after replaying its exact metadata contract."""
    variable = sp.Symbol("x")
    polynomial = sp.Poly.from_list(list(min_poly), gens=variable, domain=sp.QQ)
    lower = sp.Rational(isolating[0].numerator, isolating[0].denominator)
    upper = sp.Rational(isolating[1].numerator, isolating[1].denominator)
    checks = {
        "minimal_polynomial_irreducible_over_Q": bool(polynomial.is_irreducible),
        "minimal_polynomial_squarefree": bool(polynomial.gcd(polynomial.diff()).degree() == 0),
        "isolating_interval_contains_exactly_one_root": bool(
            polynomial.count_roots(lower, upper) == 1
        ),
    }
    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise ValueError(f"algebraic field metadata failed: {failed}")
    return NumberField(min_poly, isolating), checks


def diagnostic_decimal(value: float) -> str:
    """Round non-decisive libm diagnostics before retaining them."""
    return format(value, ".12g")


def figure13_model() -> dict[str, object]:
    """Reconstruct Figure 13 under its actual K4 reflection symmetry."""
    field, field_checks = checked_number_field((1, 0, -5), (2, 3))
    rational = field.rational
    sqrt5 = field.alpha
    a = rational(2) / sqrt5  # sqrt(4/5)
    side = rational(2) + rational(2) * a

    seeds = (
        (rational(1), rational(1)),
        (side / 2, rational(1)),
        (rational(Fraction(3, 2)) - side / 4, side / 2),
        (rational(Fraction(1, 2)) + side / 4, side / 2),
    )

    def k4_orbit(point: tuple[FieldElement, FieldElement]):
        x, y = point
        return {(x, y), (side - x, y), (x, side - y), (side - x, side - y)}

    points: set[tuple[FieldElement, FieldElement]] = set()
    for seed in seeds:
        points.update(k4_orbit(seed))

    if len(points) != 10:
        raise ValueError(f"Figure 13 K4 orbit has {len(points)} points, expected 10")
    if any(k4_orbit(point) - points for point in points):
        raise ValueError("Figure 13 point set is not K4-invariant")

    # A quarter-turn would be available under D4, but it is not a source symmetry.
    quarter_turn = {(side - y, x) for x, y in points}
    quarter_turn_is_symmetry = quarter_turn == points
    if quarter_turn_is_symmetry:
        raise ValueError("negative control failed: Figure 13 unexpectedly has D4 symmetry")

    bottom = (rational(1), rational(1) + a, rational(1) + rational(2) * a)
    middle = (
        rational(1) - a / 2,
        rational(1) + a / 2,
        rational(1) + rational(Fraction(3, 2)) * a,
        rational(1) + rational(Fraction(5, 2)) * a,
    )
    sloping_edges: list[ExactEdge] = []
    for row_y in (rational(1), side - rational(1)):
        for index, x in enumerate(bottom):
            sloping_edges.extend(
                (
                    ((x, row_y), (middle[index], side / 2)),
                    ((x, row_y), (middle[index + 1], side / 2)),
                )
            )
    squared_lengths = []
    for (x1, y1), (x2, y2) in sloping_edges:
        squared = (x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1)
        squared_lengths.append(squared)
    all_sloping_edges_exactly_one = all(
        (value - rational(1)).is_zero() for value in squared_lengths
    )
    if not all_sloping_edges_exactly_one:
        raise ValueError("Figure 13 sloping-edge transcription is not exact")

    return {
        "source_seed_formulas": [
            "(1,1)",
            "(s/2,1)",
            "(3/2-s/4,s/2)",
            "(1/2+s/4,s/2)",
        ],
        "symmetry_group": "K4: x -> s-x and y -> s-y",
        "point_count": len(points),
        "sloping_edge_count": len(squared_lengths),
        "all_sloping_edges_squared_length_one": all_sloping_edges_exactly_one,
        "quarter_turn_is_symmetry": quarter_turn_is_symmetry,
        "quarter_turn_negative_control_passed": not quarter_turn_is_symmetry,
        "container_side": exact_value(side),
        "field_metadata": field_checks,
    }


def figure13_escape() -> dict[str, object]:
    """Certify a strict box that realizes Figure 13's advertised escape."""
    # alpha = sqrt(2) + sqrt(5), with both radicals recovered in Q(alpha).
    field, field_checks = checked_number_field(
        (1, 0, -14, 0, 9),
        (Fraction(365, 100), Fraction(366, 100)),
    )
    rational = field.rational
    alpha = field.alpha
    sqrt2 = (alpha - rational(3) / alpha) / 2
    sqrt5 = (alpha + rational(3) / alpha) / 2
    if not (sqrt2 * sqrt2 - rational(2)).is_zero():
        raise ValueError("Figure 13 witness sqrt(2) reconstruction failed")
    if not (sqrt5 * sqrt5 - rational(5)).is_zero():
        raise ValueError("Figure 13 witness sqrt(5) reconstruction failed")
    if sqrt2.sign() <= 0 or sqrt5.sign() <= 0:
        raise ValueError("Figure 13 witness selected a negative radical conjugate")

    a = rational(2) / sqrt5
    side = rational(2) + rational(4) / sqrt5
    length = rational(Fraction(101, 100))
    cosine = rational(1) / sqrt2
    sine = cosine
    center_x = rational(1) + rational(1) / sqrt5
    center_y = rational(Fraction(18, 25))
    half = length / 2
    if (length - rational(1)).sign() <= 0:
        raise ValueError("Figure 13 escape is not a strict box")
    if (cosine * cosine + sine * sine - rational(1)).sign() != 0:
        raise ValueError("Figure 13 escape orientation is not a unit vector")

    corners: list[ExactPoint] = []
    for sign_u, sign_v in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        corners.append(
            (
                center_x + sign_u * half * cosine - sign_v * half * sine,
                center_y + sign_u * half * sine + sign_v * half * cosine,
            )
        )
    verifier = verify_packing(
        [corners], side, sign=exact_sign, check_shapes=False, bucket=False
    )
    if not verifier.valid:
        raise ValueError(f"Figure 13 escape violates the container: {verifier.failures}")

    container_clearances: list[tuple[str, FieldElement]] = []
    for index, (x, y) in enumerate(corners):
        container_clearances.extend(
            (
                (f"corner_{index}_left", x),
                (f"corner_{index}_bottom", y),
                (f"corner_{index}_right", side - x),
                (f"corner_{index}_top", side - y),
            )
        )
    if any(value.sign() <= 0 for _, value in container_clearances):
        raise ValueError("Figure 13 escape is not strictly inside the container")
    min_clearance_label, min_clearance = exact_min(container_clearances)

    figure13_points = [
        ("bottom_left", rational(1), rational(1)),
        ("bottom_center", rational(1) + a, rational(1)),
        ("bottom_right", rational(1) + rational(2) * a, rational(1)),
        ("middle_0", rational(1) - a / 2, side / 2),
        ("middle_1", rational(1) + a / 2, side / 2),
        ("middle_2", rational(1) + rational(Fraction(3, 2)) * a, side / 2),
        ("middle_3", rational(1) + rational(Fraction(5, 2)) * a, side / 2),
        ("top_left", rational(1), side - rational(1)),
        ("top_center", rational(1) + a, side - rational(1)),
        ("top_right", rational(1) + rational(2) * a, side - rational(1)),
    ]
    avoidance: list[tuple[str, FieldElement]] = []
    for label, x, y in figure13_points:
        dx, dy = x - center_x, y - center_y
        local_u = cosine * dx + sine * dy
        local_v = -sine * dx + cosine * dy
        margin_u = exact_abs(local_u) - half
        margin_v = exact_abs(local_v) - half
        margin, _ = exact_max(margin_u, margin_v)
        if margin.sign() <= 0:
            raise ValueError(f"Figure 13 witness does not strictly avoid {label}")
        avoidance.append((label, margin))
    min_avoidance_label, min_avoidance = exact_min(avoidance)

    a_points = [
        ("A1", rational(1), rational(Fraction(9, 10))),
        ("A2", rational(1) + a, rational(Fraction(9, 10))),
        ("A3", rational(1) + a / 2, rational(Fraction(28, 25))),
    ]
    containment: list[tuple[str, FieldElement]] = []
    for label, x, y in a_points:
        dx, dy = x - center_x, y - center_y
        local_u = cosine * dx + sine * dy
        local_v = -sine * dx + cosine * dy
        extent, _ = exact_max(exact_abs(local_u), exact_abs(local_v))
        margin = half - extent
        if margin.sign() <= 0:
            raise ValueError(f"Figure 13 witness does not strictly contain {label}")
        containment.append((label, margin))
    min_containment_label, min_containment = exact_min(containment)

    return {
        "role": "constructive non-unavoidability witness, not a localization proof",
        "field": {
            "generator": "alpha=sqrt(2)+sqrt(5)",
            "minimal_polynomial_high_to_low": [1, 0, -14, 0, 9],
            "rational_isolating_interval": ["365/100", "366/100"],
            "all_decisions": "exact signs in Q(alpha)",
            "metadata_checks": field_checks,
        },
        "box": {
            "side_formula": "101/100",
            "side": exact_value(length),
            "strictly_greater_than_one": True,
            "orientation": "45 degrees; cos=sin=1/sqrt(2)",
            "center_formula": ["1+1/sqrt(5)", "18/25"],
        },
        "independent_verify_packing_valid": verifier.valid,
        "strictly_inside_container": True,
        "minimum_container_clearance_location": min_clearance_label,
        "minimum_container_clearance": exact_value(min_clearance),
        "all_ten_figure13_points_strictly_avoided": True,
        "minimum_avoidance_margin_point": min_avoidance_label,
        "minimum_avoidance_margin": exact_value(min_avoidance),
        "all_three_A_points_strictly_contained": True,
        "minimum_A_containment_margin_point": min_containment_label,
        "minimum_A_containment_margin": exact_value(min_containment),
    }


def figure14_points(
    field: NumberField, a: FieldElement
) -> list[tuple[str, FieldElement, FieldElement]]:
    """Return the twelve printed points, preserving source labels."""
    rational = field.rational
    return [
        ("A1", rational(1), rational(Fraction(9, 10))),
        ("A2", rational(1) + a, rational(Fraction(9, 10))),
        ("A3", rational(1) + a / 2, rational(Fraction(28, 25))),
        ("B", rational(1) + rational(2) * a, rational(1)),
        (
            "C",
            rational(Fraction(11, 10)) + rational(2) * a,
            rational(1) + a,
        ),
        ("D", rational(1) + rational(2) * a, rational(1) + rational(2) * a),
        (
            "E",
            rational(1) + a,
            rational(Fraction(11, 10)) + rational(2) * a,
        ),
        ("F", rational(1), rational(1) + rational(2) * a),
        ("G", rational(Fraction(4, 5)), rational(Fraction(37, 20))),
        ("H", rational(Fraction(3, 2)), rational(Fraction(21, 10))),
        ("I", rational(Fraction(21, 10)), rational(Fraction(21, 10))),
        ("J", rational(Fraction(21, 10)), rational(Fraction(3, 2))),
    ]


def printed_figure14_escape() -> dict[str, object]:
    """Certify the strict box that avoids every printed Figure 14 point."""
    # alpha = sqrt(5) + sqrt(829).  Its minimal polynomial is
    # x^4 - 1668*x^2 + 678976, and the intended root is the unique root in (31,32).
    field, field_checks = checked_number_field((1, 0, -1668, 0, 678976), (31, 32))
    rational = field.rational
    alpha = field.alpha
    sqrt829 = (alpha + rational(824) / alpha) / 2
    sqrt5 = (alpha - rational(824) / alpha) / 2
    if not (sqrt829 * sqrt829 - rational(829)).is_zero():
        raise ValueError("sqrt(829) reconstruction failed")
    if not (sqrt5 * sqrt5 - rational(5)).is_zero():
        raise ValueError("sqrt(5) reconstruction failed")
    if sqrt829.sign() <= 0 or sqrt5.sign() <= 0:
        raise ValueError("radical reconstruction selected a negative conjugate")

    a = rational(2) / sqrt5
    side = rational(2) + rational(4) / sqrt5
    length = rational(Fraction(10001, 10000))
    cosine = rational(10) / sqrt829
    sine = rational(27) / sqrt829
    center_x = rational(37) * length / (rational(2) * sqrt829)
    center_y = rational(Fraction(11, 8))
    half = length / 2

    if (cosine * cosine + sine * sine - rational(1)).sign() != 0:
        raise ValueError("witness orientation is not a unit vector")
    if (length - rational(1)).sign() <= 0:
        raise ValueError("witness is not a box: its side must be strictly greater than one")

    # Ordered corners use edge vectors L(cos,sin) and L(-sin,cos).
    corners: list[ExactPoint] = []
    for sign_u, sign_v in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        corners.append(
            (
                center_x + sign_u * half * cosine - sign_v * half * sine,
                center_y + sign_u * half * sine + sign_v * half * cosine,
            )
        )

    edge_squared = []
    corner_dots = []
    for index in range(4):
        x1, y1 = corners[index]
        x2, y2 = corners[(index + 1) % 4]
        x0, y0 = corners[(index - 1) % 4]
        edge_squared.append((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))
        corner_dots.append((x0 - x1) * (x2 - x1) + (y0 - y1) * (y2 - y1))
    if not all((value - length * length).is_zero() for value in edge_squared):
        raise ValueError("witness corners do not have the declared exact side length")
    if not all(value.is_zero() for value in corner_dots):
        raise ValueError("witness corners are not exact right angles")

    # Reuse the packing verifier only for its independently implemented container
    # checks.  Shape checking there is unit-specific, whereas a box has L > 1.
    verifier = verify_packing(
        [corners], side, sign=exact_sign, check_shapes=False, bucket=False
    )
    if not verifier.valid:
        raise ValueError(
            f"independent container verifier rejected witness: {verifier.failures}"
        )

    left_shift = rational(Fraction(1, 10000))
    shifted_corners = [(x - left_shift, y) for x, y in corners]
    shifted_verifier = verify_packing(
        [shifted_corners], side, sign=exact_sign, check_shapes=False, bucket=False
    )
    if shifted_verifier.valid:
        raise ValueError("left-shift mutation was not rejected by the container verifier")

    clearances: list[tuple[str, FieldElement]] = []
    for index, (x, y) in enumerate(corners):
        clearances.extend(
            (
                (f"corner_{index}_left", x),
                (f"corner_{index}_bottom", y),
                (f"corner_{index}_right", side - x),
                (f"corner_{index}_top", side - y),
            )
        )
    if any(value.sign() < 0 for _, value in clearances):
        raise ValueError("witness has a negative exact container clearance")
    contacts = [label for label, value in clearances if value.sign() == 0]
    positive_clearances = [(label, value) for label, value in clearances if value.sign() > 0]
    min_clearance_label, min_positive_clearance = exact_min(positive_clearances)

    point_records = []
    avoidance_margins: list[tuple[str, FieldElement]] = []
    for label, x, y in figure14_points(field, a):
        dx, dy = x - center_x, y - center_y
        local_u = cosine * dx + sine * dy
        local_v = -sine * dx + cosine * dy
        margin_u = exact_abs(local_u) - half
        margin_v = exact_abs(local_v) - half
        margin, active_axis = exact_max(margin_u, margin_v)
        if margin.sign() <= 0:
            raise ValueError(f"witness does not strictly avoid printed point {label}")
        avoidance_margins.append((label, margin))
        point_records.append(
            {
                "label": label,
                "active_local_axis": active_axis,
                "strictly_outside_open_box": True,
                "exact_margin": exact_value(margin),
            }
        )
    min_point_label, min_avoidance_margin = exact_min(avoidance_margins)

    if contacts != ["corner_3_left"]:
        raise ValueError(f"unexpected witness contact pattern: {contacts}")
    if min_point_label != "G":
        raise ValueError(f"unexpected closest printed point: {min_point_label}")

    return {
        "field": {
            "generator": "alpha=sqrt(5)+sqrt(829)",
            "minimal_polynomial_high_to_low": [1, 0, -1668, 0, 678976],
            "rational_isolating_interval": ["31", "32"],
            "all_decisions": "exact signs in Q(alpha)",
            "metadata_checks": field_checks,
        },
        "box": {
            "side_formula": "10001/10000",
            "side": exact_value(length),
            "strictly_greater_than_one": True,
            "cosine_formula": "10/sqrt(829)",
            "sine_formula": "27/sqrt(829)",
            "center_formula": ["37L/(2sqrt(829))", "11/8"],
            "center": [exact_value(center_x), exact_value(center_y)],
            "exact_square_shape": True,
        },
        "container": {
            "side_formula": "2+4/sqrt(5)",
            "side": exact_value(side),
            "independent_verify_packing_valid": verifier.valid,
            "exact_boundary_contacts": contacts,
            "all_other_clearances_strictly_positive": True,
            "minimum_positive_clearance_location": min_clearance_label,
            "minimum_positive_clearance": exact_value(min_positive_clearance),
        },
        "printed_points": point_records,
        "all_twelve_strictly_avoided": True,
        "minimum_avoidance_margin_point": min_point_label,
        "minimum_avoidance_margin": exact_value(min_avoidance_margin),
        "mutations": {
            "left_shift_by_1_over_10000_rejected_by_container": not shifted_verifier.valid,
        },
    }


def bisect_sign_change(function: Callable[[float], float], low: float, high: float) -> float:
    """Deterministically bisect a bracket; used only for a reported diagnostic."""
    f_low = function(low)
    f_high = function(high)
    if f_low == 0:
        return low
    if f_high == 0:
        return high
    if f_low * f_high >= 0:
        raise ValueError("numeric diagnostic was not given a sign-changing bracket")
    for _ in range(80):
        middle = (low + high) / 2
        f_middle = function(middle)
        if f_low * f_middle <= 0:
            high, f_high = middle, f_middle
        else:
            low, f_low = middle, f_middle
    return (low + high) / 2


def lemma4_diagnostic() -> dict[str, object]:
    """Expose the paper's squared-root error and the failing Figure 14 face."""

    def cubic(theta: float, a: float) -> float:
        cosine = math.cos(theta)
        return (
            2 * cosine**3 - (2 * a + 2) * cosine**2 + (a * a - 2 * a + 3) * cosine - (1 - a * a)
        )

    def derivative(theta: float, a: float) -> float:
        cosine, sine = math.cos(theta), math.sin(theta)
        return -sine / (1 + cosine) ** 2 + (a - cosine) / sine**2

    def threshold(theta: float, a: float) -> float:
        cosine, sine = math.cos(theta), math.sin(theta)
        return cosine / (1 + cosine) + (1 - a * cosine) / sine

    a_middle = math.sqrt(4 / 5)
    extraneous = bisect_sign_change(
        lambda theta: cubic(theta, a_middle), math.radians(24), math.radians(25)
    )
    true_stationary = bisect_sign_change(
        lambda theta: derivative(theta, a_middle), math.radians(31), math.radians(32)
    )
    face_stationary = bisect_sign_change(
        lambda theta: derivative(theta, 0.95), math.radians(20), math.radians(21)
    )
    middle_threshold = threshold(true_stationary, a_middle)
    face_threshold = threshold(face_stationary, 0.95)

    # This exact certificate does not rely on the floating root diagnostic.  At
    # tan(theta)=3/8, b*(theta) is already below 4/5.  Since f(.95) is the minimum
    # of b*, this one exact evaluation disproves the required 4/5 <= f(.95).
    exact_field, exact_field_checks = checked_number_field((1, 0, -73), (8, 9))
    exact_rational = exact_field.rational
    sqrt73 = exact_field.alpha
    exact_cosine = exact_rational(8) / sqrt73
    exact_sine = exact_rational(3) / sqrt73
    exact_a = exact_rational(Fraction(19, 20))
    exact_candidate = (
        exact_cosine / (exact_rational(1) + exact_cosine)
        + (exact_rational(1) - exact_a * exact_cosine) / exact_sine
    )
    exact_gap = exact_rational(Fraction(4, 5)) - exact_candidate
    if exact_gap.sign() <= 0:
        raise ValueError("exact G-A1 Lemma 4 counterexample failed")

    checks = {
        "paper_cubic_root_violates_unsquared_sign": math.cos(extraneous) > a_middle,
        "paper_cubic_root_is_not_stationary": derivative(extraneous, a_middle) < -0.2,
        "corrected_root_satisfies_unsquared_sign": math.cos(true_stationary) < a_middle,
        "corrected_middle_application_b_0_9_passes": middle_threshold > 0.9,
        "figure14_G_A1_application_b_0_8_fails": face_threshold < 0.8,
        "figure14_G_A1_failure_has_exact_upper_bound": exact_gap.sign() > 0,
    }
    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise ValueError(f"Lemma 4 diagnostic controls failed: {failed}")
    return {
        "role": "floating-point diagnostic only; the terminal witness uses exact signs",
        "unsquared_stationarity_sign_condition": "cos(theta) <= a",
        "middle_table": {
            "role": "rounded display diagnostics; no verdict depends on these strings",
            "a": diagnostic_decimal(a_middle),
            "extraneous_cubic_root_degrees": diagnostic_decimal(math.degrees(extraneous)),
            "derivative_at_extraneous_root": diagnostic_decimal(
                derivative(extraneous, a_middle)
            ),
            "corrected_root_degrees": diagnostic_decimal(math.degrees(true_stationary)),
            "corrected_f_a": diagnostic_decimal(middle_threshold),
        },
        "failed_figure14_face": {
            "name": "outer G-A1 Lemma 4 cell",
            "a": "0.95",
            "claimed_b": "0.8",
            "true_f_a_display_only": diagnostic_decimal(face_threshold),
            "inequality_b_le_f_a": False,
            "exact_upper_bound_certificate": {
                "field_metadata": exact_field_checks,
                "test_orientation": "tan(theta)=3/8; cos=8/sqrt(73); sin=3/sqrt(73)",
                "b_star_at_test_orientation": exact_value(exact_candidate),
                "strict_gap_4_over_5_minus_b_star": exact_value(exact_gap),
                "conclusion": "f(19/20) <= b_star(theta) < 4/5",
            },
        },
        "checks": checks,
    }


def capacity_check(*, triple_size: int) -> dict[str, object]:
    """Evaluate the two-stage resource count without hiding its premises."""
    boxes = 11
    figure13_points = 10
    figure14_points = 12
    special_boxes = 1 if boxes > figure13_points else 0
    remaining_boxes = boxes - special_boxes
    remaining_points = figure14_points - triple_size
    contradiction = special_boxes == 1 and remaining_boxes > remaining_points
    return {
        "boxes": boxes,
        "figure13_points": figure13_points,
        "stage_one_forces_an_avoider_if_localization_is_valid": special_boxes == 1,
        "assumed_points_in_special_box": triple_size,
        "remaining_boxes": remaining_boxes,
        "remaining_figure14_points": remaining_points,
        "conditional_capacity_contradiction": contradiction,
    }


def pigeonhole_contradiction(box_count: int, resource_count: int) -> bool:
    """Return whether unit-capacity resources are fewer than boxes."""
    return box_count > resource_count


def build_result() -> dict[str, object]:
    """Build the deterministic terminal H-010 evidence record."""
    source_hashes = {
        "paper_sha256": sha256(PAPER),
        "raw_text_sha256": sha256(RAW_TEXT),
    }
    if source_hashes != EXPECTED_SOURCE_HASHES:
        raise ValueError(
            "archived Stromquist source identity changed; re-audit the finite transcription"
        )

    figure13 = figure13_model()
    stage_one_escape = figure13_escape()
    escape = printed_figure14_escape()
    lemma4 = lemma4_diagnostic()
    capacity = capacity_check(triple_size=3)
    capacity_mutation = capacity_check(triple_size=2)
    standalone_p12_pigeonhole = pigeonhole_contradiction(11, 12)
    escape_box = object_dict(escape["box"], "escape box")
    escape_mutations = object_dict(escape["mutations"], "escape mutations")
    lemma_checks = object_dict(lemma4["checks"], "Lemma 4 checks")
    selftests = {
        "source_hashes_match": source_hashes == EXPECTED_SOURCE_HASHES,
        "figure13_K4_not_D4": bool(figure13["quarter_turn_negative_control_passed"]),
        "figure13_strict_escape_avoids_all_ten": bool(
            stage_one_escape["all_ten_figure13_points_strictly_avoided"]
        ),
        "figure13_escape_contains_A_triple": bool(
            stage_one_escape["all_three_A_points_strictly_contained"]
        ),
        "box_side_is_strictly_greater_than_one": bool(escape_box["strictly_greater_than_one"]),
        "exact_witness_avoids_all_printed_points": bool(escape["all_twelve_strictly_avoided"]),
        "left_shift_witness_mutation_is_rejected": bool(
            escape_mutations["left_shift_by_1_over_10000_rejected_by_container"]
        ),
        "three_point_capacity_closes_conditionally": bool(
            capacity["conditional_capacity_contradiction"]
        ),
        "two_point_capacity_mutation_does_not_close": not bool(
            capacity_mutation["conditional_capacity_contradiction"]
        ),
        "standalone_twelve_point_pigeonhole_does_not_close": not standalone_p12_pigeonhole,
        "lemma4_squared_root_negative_control": bool(
            lemma_checks["paper_cubic_root_is_not_stationary"]
        ),
    }
    if not all(selftests.values()):
        failed = [name for name, passed in selftests.items() if not passed]
        raise ValueError(f"H-010 selftests failed: {failed}")

    return {
        "schema_version": SCHEMA_VERSION,
        "hypothesis_id": "H-010",
        "source": {
            "title": "Packing 10 or 11 Unit Squares in a Square",
            "author": "Walter Stromquist",
            "year": 2003,
            **source_hashes,
        },
        "figure13": {**figure13, "exact_escape": stage_one_escape},
        "figure14": {
            "printed_point_count": 12,
            "claimed_unavoidable": True,
            "source_faithful_cover_certified": False,
            "reason_cover_rejected": (
                "the outer G-A1 Lemma 4 premise fails and an exact strict escape exists"
            ),
            "exact_escape": escape,
        },
        "lemma4": lemma4,
        "conditional_capacity": capacity,
        "mutations": {
            "triple_size_2": capacity_mutation,
            "standalone_figure14_pigeonhole_contradiction": standalone_p12_pigeonhole,
        },
        "selftests": selftests,
        "determination": {
            "outcome": "refuted",
            "claim": "the printed Figure 14 twelve-point set is unavoidable",
            "reason": (
                "an exactly verified open box of side 10001/10000 fits in the claimed "
                "container and strictly avoids all twelve printed points"
            ),
            "scope": (
                "rejects Stromquist's printed Figure 14 cover and hence the proof as "
                "printed; does not refute the numerical lower bound itself"
            ),
        },
    }


def write_record(path: Path, result: dict[str, object]) -> None:
    """Atomically write a retained record using only the standard library."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def replay_record(path: Path) -> dict[str, object]:
    """Regenerate every field and byte-compare its parsed JSON value."""
    retained = json.loads(path.read_text(encoding="utf-8"))
    regenerated = build_result()
    if retained != regenerated:
        raise ValueError("retained H-010 record differs from exact regenerated evidence")
    return regenerated


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--record", type=Path, help="atomically write the JSON evidence record")
    mode.add_argument("--replay", type=Path, help="regenerate and compare a retained record")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    started = time.monotonic()
    try:
        result = replay_record(args.replay) if args.replay is not None else build_result()
        if args.record is not None:
            write_record(args.record, result)
        summary = {
            "schema_version": SCHEMA_VERSION,
            "hypothesis_id": "H-010",
            "record_written": args.record is not None,
            "record_replayed": args.replay is not None,
            "determination_outcome": object_dict(result["determination"], "determination")[
                "outcome"
            ],
            "minimum_avoidance_margin_point": object_dict(
                object_dict(result["figure14"], "Figure 14")["exact_escape"],
                "Figure 14 escape",
            )["minimum_avoidance_margin_point"],
            "selftests": result["selftests"],
            "elapsed_seconds": round(time.monotonic() - started, 6),
        }
        print(json.dumps(summary, indent=2, sort_keys=True))
    except (OSError, TypeError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
