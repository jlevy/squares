"""Exact, source-distinct controls for El Moumni Theorem 1, Case 1.

This module does not encode Proposition 1, the Figure 4 incidences, Cases 2 and 3, or
the complete published ``s(7) = 3`` proof. It checks the two branches needed to repair
Case 1's dropped ``min``, refuses the printed negative segment length, and separately
replays the source-defined coordinates plus a separately tagged source-distinct
candidate for the scan's undefined ``i``.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import cast

from sqpack.field import FieldElement, NumberField

Quadratic = tuple[Fraction, Fraction]


class ElMoumniSourceControlError(ValueError):
    """A typed refusal at the boundary between transcription and repair."""

    def __init__(
        self,
        kind: str,
        detail: str,
        *,
        exact_value: Quadratic | None = None,
    ):
        super().__init__(detail)
        self.kind = kind
        self.exact_value = exact_value


@dataclass(frozen=True)
class Case1MinimumCertificate:
    """Exact algebra for the two source-distinct Proposition 2 branches."""

    epsilon_upper: Quadratic
    minimum_branch_threshold: Quadratic
    threshold_gap: Quadratic
    threshold_gap_sign: int
    low_branch_contradiction_margin: Quadratic
    low_branch_contradiction_sign: int
    high_branch_required_length: int
    high_branch_available_strict_upper: int
    conclusion: str


@dataclass(frozen=True)
class ExactPoint:
    """One immutable point in ``Q(sqrt(2))^2``."""

    x: Quadratic
    y: Quadratic


@dataclass(frozen=True)
class Figure4CoordinatePacket:
    """Exact coordinates only; no packed-square incidence or geometry claim."""

    contract: str
    evidence_role: str
    promotion_boundary: str
    epsilon: Quadratic
    epsilon_upper: Quadratic
    h: Quadratic
    delta: Quadratic
    k: Quadratic
    points: tuple[tuple[str, ExactPoint], ...]
    p_prime_parameter: Quadratic
    corrected_pr_length: Quadratic
    pr_length_squared: Quadratic
    diagonal_delta: ExactPoint
    diagonal_length_squared: Quadratic
    midpoint_i_candidate: ExactPoint
    midpoint_residual: ExactPoint
    radius_symmetry_residual: Quadratic
    radius_squared_margin: Quadratic
    conclusion: str


FIGURE4_CONTRACT = "packing.squares:ElMoumniFigure4Coordinates/v1"
FIGURE4_EVIDENCE_ROLE = (
    "source-defined Figure 4 coordinates plus a separately tagged source-distinct "
    "midpoint candidate for undefined i only; no t/u or center coordinates, triangle/"
    "polygon incidence, square geometry, Cases 2 and 3, packing feasibility or "
    "optimality, theorem, or n=11 claim"
)
FIGURE4_PROMOTION_BOUNDARY = (
    "passing advances only the Figure 4 coordinate prerequisite under think-trkj; "
    "Proposition 1, t/u, centers, triangle/polygon incidence, packed-square geometry, "
    "Cases 2 and 3, packing feasibility and optimality, the complete s(7)=3 proof, "
    "and any n=11 transfer remain closed"
)
FIGURE4_CONCLUSION = "figure-4-coordinate-prerequisite-only"


def _sqrt2_field() -> NumberField:
    return NumberField((1, 0, -2), (1, 2))


def _sign(field: NumberField, value: Quadratic) -> int:
    return field.element(value).sign()


def _freeze(value: FieldElement) -> Quadratic:
    if len(value.coeffs) != 2:
        raise AssertionError("the Figure 4 packet requires Q(sqrt(2))")
    return (value.coeffs[0], value.coeffs[1])


def _point(x: FieldElement, y: FieldElement) -> ExactPoint:
    return ExactPoint(_freeze(x), _freeze(y))


def _is_quadratic(value: object) -> bool:
    return (
        type(value) is tuple
        and len(value) == 2
        and all(type(coefficient) is Fraction for coefficient in value)
    )


def _require_quadratic(value: object) -> Quadratic:
    if not _is_quadratic(value):
        raise ElMoumniSourceControlError(
            "exact-control-input-required",
            "epsilon must be a two-Fraction Q(sqrt(2)) coefficient tuple",
        )
    return cast(Quadratic, value)


def prove_case1_minimum_repair(
    *,
    preserve_minimum: bool = True,
    required_contributions: int = 3,
) -> Case1MinimumCertificate:
    """Prove the repaired Case 1 split exactly in ``Q(sqrt(2))``.

    Proposition 2 supplies ``min(B, 1)`` for
    ``B = 2 sqrt(2) - 2 + 2 epsilon``. The source's epsilon domain crosses the
    threshold ``B = 1``, so the minimum must remain explicit.
    """
    if type(preserve_minimum) is not bool or type(required_contributions) is not int:
        raise ElMoumniSourceControlError(
            "exact-control-input-required",
            "the minimum flag must be boolean and the contribution count must be integer",
        )
    if not preserve_minimum:
        raise ElMoumniSourceControlError(
            "proposition-2-minimum-dropped",
            "Theorem 1's epsilon domain crosses B=1, so Proposition 2's minimum is active",
        )
    if required_contributions != 3:
        raise ElMoumniSourceControlError(
            "case-1-contribution-count",
            "Case 1 needs the C₁ term, C₃ term, and the two-line C₂ sum",
        )

    field = _sqrt2_field()
    epsilon_upper = (Fraction(1, 3), Fraction(-1, 6))
    minimum_branch_threshold = (Fraction(3, 2), Fraction(-1))
    threshold_gap = (Fraction(-7, 6), Fraction(5, 6))
    low_branch_contradiction_margin = (Fraction(-8), Fraction(6))

    if _sign(field, epsilon_upper) != 1:
        raise AssertionError("the source epsilon upper bound is not positive")
    if _sign(field, minimum_branch_threshold) != 1:
        raise AssertionError("the B=1 threshold is not positive")
    threshold_gap_sign = _sign(field, threshold_gap)
    if threshold_gap_sign != 1:
        raise AssertionError("the source domain does not cross the B=1 threshold")
    low_branch_sign = _sign(field, low_branch_contradiction_margin)
    if low_branch_sign != 1:
        raise AssertionError("6 sqrt(2) - 8 does not contradict the low branch")
    if required_contributions <= 2:
        raise AssertionError("the high branch does not exceed the available line length")

    return Case1MinimumCertificate(
        epsilon_upper=epsilon_upper,
        minimum_branch_threshold=minimum_branch_threshold,
        threshold_gap=threshold_gap,
        threshold_gap_sign=threshold_gap_sign,
        low_branch_contradiction_margin=low_branch_contradiction_margin,
        low_branch_contradiction_sign=low_branch_sign,
        high_branch_required_length=required_contributions,
        high_branch_available_strict_upper=2,
        conclusion="case-1-repair-only",
    )


def transcribe_printed_figure4_length() -> None:
    """Refuse the printed ``|pr|`` value before any Figure 4 route is encoded."""
    field = _sqrt2_field()
    printed_at_zero = (Fraction(-4), Fraction(2))
    if _sign(field, printed_at_zero) < 0:
        raise ElMoumniSourceControlError(
            "negative-source-length",
            "printed |pr| is already negative at epsilon=0 and decreases for epsilon>0",
            exact_value=printed_at_zero,
        )
    raise AssertionError("the retained printed formula unexpectedly passed its sign control")


def transcribe_printed_figure4_line_center() -> None:
    """Refuse printed ``o1`` before any source-figure ``C₄`` chord is encoded."""
    raise ElMoumniSourceControlError(
        "wrong-source-center",
        "printed Delta passes through o1 although its distance premises concern o4",
    )


def derive_figure4_coordinate_packet(
    epsilon: Quadratic,
) -> Figure4CoordinatePacket:
    """Derive source-defined coordinates and the tagged candidate for undefined ``i``.

    The coordinate origin is ``a'`` with x right and y up. The source leaves ``t``,
    ``u``, every packed-square center and orientation, and the surrounding containment
    assertions unspecified; none is inferred here. Point ``i`` is recorded only as the
    source-distinct midpoint interpretation that reproduces the printed distance
    display.
    """
    epsilon = _require_quadratic(epsilon)
    field = _sqrt2_field()
    zero = field.rational(0)
    one = field.rational(1)
    two = field.rational(2)
    sqrt2 = field.element((Fraction(0), Fraction(1)))
    epsilon_value = field.element(epsilon)
    epsilon_upper = field.element((Fraction(1, 3), Fraction(-1, 6)))
    if epsilon_value.sign() <= 0 or (epsilon_upper - epsilon_value).sign() < 0:
        raise ElMoumniSourceControlError(
            "figure4-epsilon-domain",
            "Figure 4 requires 0 < epsilon <= (2-sqrt(2))/6",
            exact_value=epsilon,
        )

    h = one - epsilon_value
    delta = two * sqrt2 - two
    k = h - delta
    if k.sign() <= 0:
        raise AssertionError("the printed epsilon domain must keep p and r ordered")

    inverse_sqrt2 = one / sqrt2
    p_prime_parameter = (h - inverse_sqrt2) / delta
    if p_prime_parameter.sign() <= 0 or (one - p_prime_parameter).sign() <= 0:
        raise AssertionError("the p-prime and r-prime parameter must be interior")

    a = _point(-h, h)
    a1 = _point(zero, h)
    a2 = _point(-h, zero)
    a_prime = _point(zero, zero)
    b_prime = _point(h, zero)
    f_prime = _point(zero, -h)
    p = _point(k, zero)
    q = _point(delta, zero)
    r = _point(zero, -k)
    s = _point(zero, -delta)
    p_prime_x = p_prime_parameter * k
    p_prime_y = h * (one - p_prime_parameter)
    r_prime_x = -p_prime_y
    r_prime_y = -p_prime_x
    p_prime = _point(p_prime_x, p_prime_y)
    r_prime = _point(r_prime_x, r_prime_y)
    midpoint_i_candidate = _point(-h / two, h / two)

    diagonal_dx = p_prime_x - r_prime_x
    diagonal_dy = p_prime_y - r_prime_y
    diagonal_length_squared = diagonal_dx * diagonal_dx + diagonal_dy * diagonal_dy
    if diagonal_dx != inverse_sqrt2 or diagonal_dy != inverse_sqrt2:
        raise AssertionError("the source-distinct p-prime/r-prime diagonal is not parallel")
    if diagonal_length_squared != one:
        raise AssertionError("the source-distinct p-prime/r-prime diagonal is not unit")

    i_x = field.element(midpoint_i_candidate.x)
    i_y = field.element(midpoint_i_candidate.y)
    midpoint_residual_x = i_x - (field.element(a1.x) + field.element(a2.x)) / two
    midpoint_residual_y = i_y - (field.element(a1.y) + field.element(a2.y)) / two
    ip_x = p_prime_x - i_x
    ip_y = p_prime_y - i_y
    ir_x = r_prime_x - i_x
    ir_y = r_prime_y - i_y
    ip_squared = ip_x * ip_x + ip_y * ip_y
    ir_squared = ir_x * ir_x + ir_y * ir_y
    radius_symmetry_residual = ip_squared - ir_squared
    if not midpoint_residual_x.is_zero() or not midpoint_residual_y.is_zero():
        raise AssertionError("undefined i's midpoint candidate did not replay")
    if not radius_symmetry_residual.is_zero():
        raise AssertionError(
            "the equal-radius display under the source-distinct i candidate did not replay"
        )
    radius_squared_margin = one / two - ip_squared
    if radius_squared_margin.sign() <= 0:
        raise AssertionError("the source-distinct midpoint radius bound did not pass")

    corrected_pr_length = sqrt2 * k
    pr_length_squared = two * k * k
    if corrected_pr_length.sign() <= 0 or (one - corrected_pr_length).sign() <= 0:
        raise AssertionError("the corrected local segment length must lie in (0,1)")
    if corrected_pr_length * corrected_pr_length != pr_length_squared:
        raise AssertionError("the corrected local segment identity did not replay")

    return Figure4CoordinatePacket(
        contract=FIGURE4_CONTRACT,
        evidence_role=FIGURE4_EVIDENCE_ROLE,
        promotion_boundary=FIGURE4_PROMOTION_BOUNDARY,
        epsilon=epsilon,
        epsilon_upper=_freeze(epsilon_upper),
        h=_freeze(h),
        delta=_freeze(delta),
        k=_freeze(k),
        points=(
            ("a", a),
            ("a1", a1),
            ("a2", a2),
            ("a_prime", a_prime),
            ("b_prime", b_prime),
            ("f_prime", f_prime),
            ("p", p),
            ("q", q),
            ("r", r),
            ("s", s),
            ("p_prime", p_prime),
            ("r_prime", r_prime),
            ("i_candidate", midpoint_i_candidate),
        ),
        p_prime_parameter=_freeze(p_prime_parameter),
        corrected_pr_length=_freeze(corrected_pr_length),
        pr_length_squared=_freeze(pr_length_squared),
        diagonal_delta=_point(diagonal_dx, diagonal_dy),
        diagonal_length_squared=_freeze(diagonal_length_squared),
        midpoint_i_candidate=midpoint_i_candidate,
        midpoint_residual=_point(midpoint_residual_x, midpoint_residual_y),
        radius_symmetry_residual=_freeze(radius_symmetry_residual),
        radius_squared_margin=_freeze(radius_squared_margin),
        conclusion=FIGURE4_CONCLUSION,
    )


def replay_figure4_coordinate_packet(packet: Figure4CoordinatePacket) -> None:
    """Reject any mutation of the bounded Figure 4 coordinate record."""
    if type(packet) is not Figure4CoordinatePacket:
        raise ElMoumniSourceControlError(
            "exact-control-input-required",
            "Figure 4 replay requires a Figure4CoordinatePacket",
        )
    expected = derive_figure4_coordinate_packet(packet.epsilon)
    if (
        packet.contract != expected.contract
        or packet.evidence_role != expected.evidence_role
        or packet.promotion_boundary != expected.promotion_boundary
        or packet.conclusion != expected.conclusion
    ):
        raise ElMoumniSourceControlError(
            "figure4-claim-boundary",
            "the coordinate-only contract or promotion boundary changed",
        )
    if (
        packet.epsilon_upper != expected.epsilon_upper
        or packet.h != expected.h
        or packet.delta != expected.delta
        or packet.k != expected.k
    ):
        raise ElMoumniSourceControlError(
            "figure4-domain-record",
            "the Figure 4 grid or epsilon-domain record changed",
        )

    if type(packet.points) is not tuple or any(
        type(entry) is not tuple
        or len(entry) != 2
        or type(entry[0]) is not str
        or type(entry[1]) is not ExactPoint
        or not _is_quadratic(entry[1].x)
        or not _is_quadratic(entry[1].y)
        for entry in packet.points
    ):
        raise ElMoumniSourceControlError(
            "figure4-source-point",
            "the Figure 4 point record must be an exact tuple of labeled exact points",
        )
    expected_points = dict(expected.points)
    packet_points = dict(packet.points)
    if len(packet.points) != len(packet_points) or tuple(packet_points) != tuple(
        expected_points
    ):
        raise ElMoumniSourceControlError(
            "figure4-source-point",
            "the Figure 4 point labels are missing, duplicated, or reordered",
        )
    if any(packet_points[label] != expected_points[label] for label in ("p_prime", "r_prime")):
        raise ElMoumniSourceControlError(
            "figure4-diagonal-construction",
            "the p-prime/r-prime construction changed",
        )
    if packet_points["i_candidate"] != expected_points["i_candidate"]:
        raise ElMoumniSourceControlError(
            "figure4-midpoint-role",
            "the separately tagged midpoint candidate for undefined i changed",
        )
    if any(
        packet_points[label] != expected_points[label]
        for label in expected_points
        if label not in {"p_prime", "r_prime", "i_candidate"}
    ):
        raise ElMoumniSourceControlError(
            "figure4-source-point",
            "a source-fixed Figure 4 point changed",
        )
    if (
        packet.p_prime_parameter != expected.p_prime_parameter
        or packet.diagonal_delta != expected.diagonal_delta
        or packet.diagonal_length_squared != expected.diagonal_length_squared
    ):
        raise ElMoumniSourceControlError(
            "figure4-diagonal-construction",
            "the source-distinct unit diagonal construction changed",
        )
    if (
        packet.corrected_pr_length != expected.corrected_pr_length
        or packet.pr_length_squared != expected.pr_length_squared
    ):
        raise ElMoumniSourceControlError(
            "figure4-segment-identity",
            "the source-distinct corrected segment identity changed",
        )
    if (
        packet.midpoint_i_candidate != expected.midpoint_i_candidate
        or packet.midpoint_residual != expected.midpoint_residual
        or packet.radius_symmetry_residual != expected.radius_symmetry_residual
        or packet.radius_squared_margin != expected.radius_squared_margin
    ):
        raise ElMoumniSourceControlError(
            "figure4-midpoint-role",
            "the source-distinct midpoint or radius calculation changed",
        )
