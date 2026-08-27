"""Exact local controls for El Moumni Theorem 1, Case 1."""

from __future__ import annotations

from fractions import Fraction

import pytest

from cases.small_n.el_moumni7 import (
    ElMoumniSourceControlError,
    prove_case1_minimum_repair,
    transcribe_printed_figure4_length,
)


def test_case1_repair_keeps_both_proposition_2_branches_exact() -> None:
    certificate = prove_case1_minimum_repair()

    assert certificate.epsilon_upper == (Fraction(1, 3), Fraction(-1, 6))
    assert certificate.minimum_branch_threshold == (Fraction(3, 2), Fraction(-1))
    assert certificate.threshold_gap == (Fraction(-7, 6), Fraction(5, 6))
    assert certificate.threshold_gap_sign == 1
    assert certificate.low_branch_contradiction_margin == (Fraction(-8), Fraction(6))
    assert certificate.low_branch_contradiction_sign == 1
    assert certificate.high_branch_required_length == 3
    assert certificate.high_branch_available_strict_upper == 2
    assert certificate.conclusion == "case-1-repair-only"


def test_unbranched_source_substitution_rejects() -> None:
    with pytest.raises(ElMoumniSourceControlError) as caught:
        prove_case1_minimum_repair(preserve_minimum=False)
    assert caught.value.kind == "proposition-2-minimum-dropped"


def test_deleted_third_contribution_rejects() -> None:
    with pytest.raises(ElMoumniSourceControlError) as caught:
        prove_case1_minimum_repair(required_contributions=2)
    assert caught.value.kind == "case-1-contribution-count"


def test_printed_figure4_length_is_typed_source_blocker() -> None:
    with pytest.raises(ElMoumniSourceControlError) as caught:
        transcribe_printed_figure4_length()
    assert caught.value.kind == "negative-source-length"
    assert caught.value.exact_value == (Fraction(-4), Fraction(2))


@pytest.mark.parametrize(
    ("preserve_minimum", "required_contributions"),
    ((1, 3), (True, True), (True, 3.0)),
)
def test_inexact_or_boolean_control_inputs_reject(
    preserve_minimum: object, required_contributions: object
) -> None:
    with pytest.raises(ElMoumniSourceControlError) as caught:
        prove_case1_minimum_repair(
            preserve_minimum=preserve_minimum,  # pyright: ignore[reportArgumentType]
            required_contributions=required_contributions,  # pyright: ignore[reportArgumentType]
        )
    assert caught.value.kind == "exact-control-input-required"
