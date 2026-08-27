"""Exact, source-distinct controls for El Moumni Theorem 1, Case 1.

This module does not encode Proposition 1, the Figure 4 incidences, Cases 2 and 3, or
the complete published ``s(7) = 3`` proof. It only checks the two branches needed to
repair Case 1's dropped ``min`` and refuses the printed negative segment length.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from sqpack.field import NumberField

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


def _sqrt2_field() -> NumberField:
    return NumberField((1, 0, -2), (1, 2))


def _sign(field: NumberField, value: Quadratic) -> int:
    return field.element(value).sign()


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
            "Case 1 needs the C1 term, C3 term, and the two-line C2 sum",
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
