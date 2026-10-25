"""The deficiency family's comparison: the recorded assessment, its tail and its freshness."""

from __future__ import annotations

import copy

import pytest

from cases.asymptotic import deficiency_family as family
from cases.asymptotic import fang_excess_inventory as fang
from cases.asymptotic import fang_theorem_a


def fang_row(ledger: dict) -> dict:
    return next(row for row in ledger[family.SECTION] if row.get("record_scope"))


def test_the_recorded_assessment_is_what_the_family_recomputes() -> None:
    """The gate's freshness check: `devtools.profile_records` reads the recorded
    assessment, so this is what holds it to every statement of the family."""
    assert family.main([]) == 0
    ledger, dated = family.load()
    ((result, recorded, recomputed),) = family.recorded_assessments(ledger, dated)
    assert result == "T-163"
    assert family.stale(recorded, recomputed) == []
    assert recomputed["smallest"] == [[15, 34], [36, 39]]
    assert recomputed["tied"] == [[34, 34], [39, 39]]


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


def test_a_stale_assessment_fails_the_comparison() -> None:
    ledger, dated = family.load()
    fang_row(ledger)["record_scope"]["assessment"]["smallest"] = [[15, 78]]
    ((_, recorded, recomputed),) = family.recorded_assessments(ledger, dated)
    assert family.stale(recorded, recomputed) == ["smallest"]
    for row in ledger[family.SECTION]:
        if row.get("record_scope"):
            del row["record_scope"]["assessment"]
    assert family.recorded_assessments(ledger, dated) == []


def test_a_tie_stays_with_the_earlier_report() -> None:
    """T-163 ties Daniel's bound, reported on 18 October, at 34 and 39: the ties are T-163's.
    Dated before T-163, Daniel's report would take them."""
    ledger, dated = family.load()
    row = fang_row(ledger)
    assert family.assess(ledger, row, dated)["smallest"] == [[15, 34], [36, 39]]
    earlier = {**dated, family.DANIEL: "2026-10-12"}
    assert family.assess(ledger, row, earlier)["smallest"] == [[15, 33], [36, 38]]


def test_without_the_two_sqrt_k_rows_the_earlier_window_returns() -> None:
    """The window before Daniel's and Fang's rows, with Ryu's earlier ties at 69 and 76."""
    ledger, dated = family.load()
    ledger[family.SECTION] = [
        row
        for row in ledger[family.SECTION]
        if row["source_key"] not in {family.DANIEL, family.FANG_A}
    ]
    found = family.assess(ledger, fang_row(ledger), dated)
    assert found["smallest"] == [[15, 68], [70, 75]]
    assert found["tied"] == [[69, 69], [76, 76]]
    later = {**dated, family.RYU: "2026-10-30"}
    assert family.assess(ledger, fang_row(ledger), later)["smallest"] == [[15, 76]]


def test_the_two_sqrt_k_statements_are_their_integer_bounds() -> None:
    for k in range(7, 400):
        b = fang_theorem_a.ceil_sqrt(2 * k - 7)
        assert (b - 1) ** 2 < 2 * k - 7 <= b * b
        assert family.daniel_layers(k) == 4 * b - 1
        a = fang_theorem_a.theorem_a(k)
        assert (a - 1) ** 2 < 32 * k <= a * a
    with pytest.raises(ValueError, match="k >= 7"):
        family.daniel_layers(6)
    with pytest.raises(ValueError, match="k >= 6"):
        fang_theorem_a.theorem_a(5)


@pytest.mark.parametrize(
    ("key", "date"),
    [
        (family.FANG, ""),
        (family.FANG, None),
        (family.DANIEL, ""),
        (family.DANIEL, None),
        (family.DANIEL, "None"),
        (family.DANIEL, "2026-10"),
    ],
)
def test_an_undated_source_orders_no_tie(key: str, date: str | None) -> None:
    """Review A4 on #770: a tie is ordered by the bibliography's dates compared as days,
    so the assessed row's key, or the key of a statement it ties, with no day-precision
    date refuses the assessment instead of winning every tie. Daniel's key is the one
    T-163 ties, at k = 34 and 39."""
    ledger, dated = family.load()
    with pytest.raises(family.FamilyError, match="no day-precision date"):
        family.assess(ledger, fang_row(ledger), {**dated, key: date})


def test_dates_are_compared_as_days() -> None:
    ledger, dated = family.load()
    row = fang_row(ledger)
    # As strings "2026-9-30" would sort after "2026-10-13"; it is no date the gate reads.
    with pytest.raises(family.FamilyError, match="no day-precision date"):
        family.assess(ledger, row, {**dated, family.DANIEL: "2026-9-30"})
    earlier = {**dated, family.DANIEL: "2026-10-12"}
    assert family.assess(ledger, row, earlier)["smallest"] == [[15, 33], [36, 38]]
    same_day = {**dated, family.DANIEL: dated[family.FANG]}
    assert family.assess(ledger, row, same_day)["smallest"] == [[15, 33], [36, 38]]


def _rows(ledger: dict) -> list[tuple[int, str]]:
    return [
        (index, field)
        for index, row in enumerate(ledger[family.SECTION])
        for field in family.STATED
        if row.get(field) is not None
    ]


def test_a_row_restated_in_place_refuses_the_assessment() -> None:
    """Review A5 on #770: a row whose bound is rewritten under the same key, kernel and
    side condition is a new statement of the family, so it is compared again before any
    assessment stands. The review's probe: Ryu's row restated as 4 ceil(sqrt(k - 4)) - 1."""
    ledger, dated = family.load()
    probe = copy.deepcopy(ledger)
    ryu_row = next(
        row for row in probe[family.SECTION] if str(row.get("kernel", "")).startswith("sqrt k")
    )
    ryu_row["bound"] = "c*(k) <= 4 ceil(sqrt(k - 4)) - 1"
    ryu_row["constant"] = "4"
    with pytest.raises(family.FamilyError, match="restated"):
        family.assess(probe, fang_row(probe), dated)
    assert _rows(ledger)
    for index, field in _rows(ledger):
        edited = copy.deepcopy(ledger)
        edited[family.SECTION][index][field] = f"{edited[family.SECTION][index][field]} x"
        with pytest.raises(family.FamilyError, match=f"restated: its {field}"):
            family.assess(edited, fang_row(edited), dated)


def test_reflowing_a_row_is_not_a_restatement() -> None:
    ledger, dated = family.load()
    for row in ledger[family.SECTION]:
        for field in family.STATED:
            if isinstance(row.get(field), str):
                row[field] = "\n  ".join(row[field].split())
    assert family.assess(ledger, fang_row(ledger), dated)["smallest"] == [[15, 34], [36, 39]]
