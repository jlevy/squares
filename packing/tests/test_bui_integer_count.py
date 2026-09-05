"""Exact controls for Bui's Section 3.1 replacement-grid count."""

from __future__ import annotations

from fractions import Fraction

import pytest

from cases.asymptotic.bui_integer_count import CountControlError, replay_count


def test_source_count_and_named_final_deletion() -> None:
    receipt = replay_count(7, Fraction(5, 3))

    assert receipt.thresholds == tuple(sorted(receipt.thresholds))
    assert receipt.before_final_deletion == receipt.m * receipt.rows
    assert receipt.after_final_deletion == receipt.m * receipt.rows - 1
    assert receipt.retained_s + receipt.retained_t == receipt.before_final_deletion
    assert receipt.replacement_j_range == (2, receipt.m)
    assert receipt.retained_t == sum(
        receipt.rows - threshold + 1 for threshold in receipt.thresholds[1:]
    )
    assert receipt.deleted_coordinate == (receipt.rows, receipt.m)
    assert receipt.deleted_label == "S"


def test_coincident_thresholds_still_partition_distinct_columns() -> None:
    receipt = replay_count(8, Fraction(1, 5))

    assert receipt.thresholds == (1, 2, 2, 2, 2, 2, 3, 3)
    assert receipt.before_final_deletion == 8 * receipt.thresholds[-1]
    assert receipt.retained_t > 0


def test_two_column_boundary_replaces_only_the_first_column() -> None:
    receipt = replay_count(2, Fraction(3, 2))

    assert receipt.thresholds == (1, 3)
    assert receipt.rows == 3
    assert receipt.retained_t == 1
    assert receipt.retained_s == 5
    assert receipt.before_final_deletion == 6
    assert receipt.after_final_deletion == 5


def test_exact_rational_grid_sweep() -> None:
    for m in range(2, 26):
        for numerator in range(1, 21):
            for denominator in range(1, 21):
                receipt = replay_count(m, Fraction(numerator, denominator))
                assert receipt.before_final_deletion == m * receipt.rows
                assert receipt.after_final_deletion == m * receipt.rows - 1


@pytest.mark.parametrize(
    ("m", "c"),
    [(1, Fraction(1)), (2, Fraction(0)), (2, Fraction(-1, 3))],
)
def test_parameter_domain_mutations_reject(m: int, c: Fraction) -> None:
    with pytest.raises(CountControlError) as caught:
        replay_count(m, c)
    assert caught.value.kind == "parameter-domain"


def test_unbounded_j_wording_cannot_extend_past_the_m_columns() -> None:
    with pytest.raises(CountControlError, match=r"replacement range 2\.\.m") as caught:
        replay_count(5, Fraction(2, 3), replacement_last_j=6)
    assert caught.value.kind == "source-index-range"
