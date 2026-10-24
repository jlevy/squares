"""The deficiency family's comparison: the recorded assessment, its tail and its freshness."""

from __future__ import annotations

import copy

import pytest

from cases.asymptotic import deficiency_family as family
from cases.asymptotic import fang_excess_inventory as fang


def fang_row(ledger: dict) -> dict:
    return next(row for row in ledger[family.SECTION] if row.get("record_scope"))


def test_the_recorded_assessment_is_what_the_family_recomputes() -> None:
    assert family.main([]) == 0
    ledger, dated = family.load()
    ((result, recorded, recomputed),) = family.recorded_assessments(ledger, dated)
    assert result == "T-163"
    assert family.stale(recorded, recomputed) == []
    assert recomputed["smallest"] == [[15, 68], [70, 75]]
    assert recomputed["tied"] == [[69, 69], [76, 76]]


def test_the_tail_lemma_starts_where_its_quadratic_turns_positive() -> None:
    assert family.tail_holds(family.TAIL)
    assert not family.tail_holds(family.TAIL - 1)
    for k in range(family.TAIL, 3000):
        # F(k) <= 1 + 2(k - 15)/21, so Theorem 2 >= (19k - 12)/21 > Theorem 1.4.
        assert 21 * (fang.excess(k) - 1) <= 2 * (k - 15)
        assert fang.theorem_two(k) > fang.ryu(k)


def test_theorem_1_4_never_undercuts_theorem_1_3_at_its_best_b() -> None:
    for k in range(15, family.TAIL):
        assert family.ryu_theorem_1_3(k) <= fang.ryu(k)


def test_a_statement_the_comparison_does_not_name_refuses_the_assessment() -> None:
    ledger, dated = family.load()
    unnamed = copy.deepcopy(ledger)
    unnamed[family.SECTION].append(
        {"source_key": "[new 2026]", "kernel": "log k", "side_condition": "k >= 2"}
    )
    with pytest.raises(family.FamilyError, match="no single maintained statement"):
        family.assess(unnamed, fang_row(unnamed), dated)
    explicit = copy.deepcopy(ledger)
    explicit["upper_bounds"][0]["constant"] = "W(x) <= 9 x^{7/11} for x >= 2"
    with pytest.raises(family.FamilyError, match="states a constant"):
        family.assess(explicit, fang_row(explicit), dated)


def test_a_tie_stays_with_the_earlier_report() -> None:
    ledger, dated = family.load()
    row = fang_row(ledger)
    assert family.assess(ledger, row, dated)["smallest"] == [[15, 68], [70, 75]]
    later = {**dated, family.RYU: "2026-10-30"}
    assert family.assess(ledger, row, later)["smallest"] == [[15, 76]]
