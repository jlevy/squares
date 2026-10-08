"""Each result's derived standing agrees with the bounds its own words state.

`render_recent_results.standing` derives a standing from evidence ids and never compares
a number. `devtools.check_standing` reads the bounds an entry states and holds them
against the case records, so an entry that is no longer the best is superseded and one
that still stands is not (think-nr0y). These hold the register to that, the reader to
the headlines it must read, and the check to refusing each kind of mismatch.
"""

from __future__ import annotations

from collections.abc import Mapping
from fractions import Fraction
from typing import Any

import pytest

from devtools import check_standing
from devtools import render_recent_results as view
from devtools.check_results import BOUND_KINDS
from devtools.check_standing import BEATEN, EQUAL, EXCEEDS, LOWER, UPPER, Stated

EXACT = Fraction(0)


@pytest.fixture(scope="module")
def records() -> view.Records:
    return view.load_records()


def test_every_standing_in_the_register_agrees_with_the_bounds_its_entry_states(
    records: view.Records, capsys: pytest.CaptureFixture[str]
) -> None:
    """No entry is superseded while a bound it states still stands, and none stands
    while every bound it states is beaten. The command says the same."""
    for record in records.register.results:
        standing = view.standing(record, records)
        assert check_standing.problems(record, standing, records) == [], record["id"]
    assert check_standing.main([]) == 0
    quiet = capsys.readouterr().out
    assert quiet.startswith(f"OK: {len(records.register.results)} results")
    assert len(quiet.splitlines()) == 1
    assert check_standing.main(["--list"]) == 0
    listed = capsys.readouterr().out.splitlines()
    assert len(listed) == len(records.register.results) + 1
    assert all(line.startswith("T-") for line in listed[:-1])


def test_the_check_reads_the_bound_of_nearly_every_entry_that_claims_one(
    records: view.Records,
) -> None:
    """The comparison is of numbers, so it is only as wide as the headlines it reads.
    Every entry with no standing states none; of the entries that are superseded, at
    most a fifth state a bound in a form this does not read, and those are held to the
    structural rule instead."""
    unread = []
    superseded = []
    for record in records.register.results:
        standing = view.standing(record, records)
        stated = check_standing.stated_bounds(record)
        if standing == view.NO_STANDING:
            assert record["kind"] not in BOUND_KINDS, record["id"]
            assert not stated, record["id"]
        if standing == view.SUPERSEDED:
            superseded.append(record["id"])
            if not stated:
                unread.append(record["id"])
    assert superseded
    assert len(unread) * 5 <= len(superseded), unread


@pytest.mark.parametrize(
    ("text", "scope", "expected"),
    [
        (
            "`s(17) ≥ 4426213/1000000 = 4.426213`, from a sixteen-point unavoidable set",
            [17],
            {(17, LOWER): Stated(Fraction(4426213, 1000000), EXACT)},
        ),
        ("`s(11) > 31/8 = 3.875`", [11], {(11, LOWER): Stated(Fraction(31, 8), EXACT)}),
        (
            "`s(13) = 4`",
            [13],
            {(13, LOWER): Stated(Fraction(4), EXACT), (13, UPPER): Stated(Fraction(4), EXACT)},
        ),
        # Cut decimals stand for every number that starts so.
        (
            "`s(29) ≤ 5.933833…`, by a Krawczyk interval certificate",
            [29],
            {(29, UPPER): Stated(Fraction("5.933833"), Fraction(1, 10**6))},
        ),
        # A closed form is read by the decimals after it.
        (
            "`s(11) ≥ 38100√(8100042893309449)/899996306539 = 3.8100257…`",
            [11],
            {(11, LOWER): Stated(Fraction("3.8100257"), Fraction(1, 10**7))},
        ),
        # A closed form with no decimals is not read as its first number.
        ("`s(11) ≥ 2 + 4/√5`, by a repair of Stromquist 2003's Figure 14", [11], {}),
        ("s(11) >= 2 + 4/sqrt(5), by a source-distinct repair", [11], {}),
        ("`s(n) ≥ min(⌈√n⌉, √(n - 2⌊√n⌋ + 1) + 1)` for `4 ≤ n ≤ 100`", [4, 5], {}),
        # `s(n)` is for the cases named after it, or for the whole scope.
        (
            "`s(n) ≥ 24/5 = 4.80` for `n = 19, 20, 21`",
            [19, 20, 21, 22],
            {(n, LOWER): Stated(Fraction(24, 5), EXACT) for n in (19, 20, 21)},
        ),
        (
            (
                "`s(11) ≥ 381/100`; `s(n) ≥ 1377/250` for `n = 26…28`; "
                "`s(n) ≥ 571/100` for `n = 29…31`"
            ),
            [11, 26, 27, 28, 29, 30, 31],
            {
                (11, LOWER): Stated(Fraction(381, 100), EXACT),
                **{(n, LOWER): Stated(Fraction(1377, 250), EXACT) for n in (26, 27, 28)},
                **{(n, LOWER): Stated(Fraction(571, 100), EXACT) for n in (29, 30, 31)},
            },
        ),
        (
            "`s(n) ≥ 22529/5000`, by monotonicity",
            [18, 19],
            {(n, LOWER): Stated(Fraction(22529, 5000), EXACT) for n in (18, 19)},
        ),
        (
            "`s(27), s(28) ≥ 28/5`, `s(31) ≥ 148/25` and `s(32) ≥ 119/20`",
            [27, 28, 31, 32],
            {
                (27, LOWER): Stated(Fraction(28, 5), EXACT),
                (28, LOWER): Stated(Fraction(28, 5), EXACT),
                (31, LOWER): Stated(Fraction(148, 25), EXACT),
                (32, LOWER): Stated(Fraction(119, 20), EXACT),
            },
        ),
        # The strongest of two statements about one case, and a claim's plain relations,
        # a value at the end of a sentence among them.
        (
            "`s(17) ≥ 461300/99999 = 4.61304613…`, and beneath it Mira's `s(17) ≥ 4613/1000`",
            [17],
            {(17, LOWER): Stated(Fraction(461300, 99999), EXACT)},
        ),
        (
            "prove s(26) >= 109/20, s(29) >= 557/100 and s(72) >= 861/100. Four more",
            [26, 29, 72],
            {
                (26, LOWER): Stated(Fraction(109, 20), EXACT),
                (29, LOWER): Stated(Fraction(557, 100), EXACT),
                (72, LOWER): Stated(Fraction(861, 100), EXACT),
            },
        ),
        (
            "`s(211) ≤ 14.99796070496771500150 < 15`, the first packing below the grid",
            [211],
            {(211, UPPER): Stated(Fraction("14.99796070496771500150"), EXACT)},
        ),
        # A case outside the entry's scope is another entry's bound, quoted.
        (
            "`s(18) ≥ 467/100`, above `s(17) ≥ 459/100`",
            [18],
            {(18, LOWER): Stated(Fraction(467, 100), EXACT)},
        ),
        ("Goebel's `n = 5` packing is second-order rigid at fixed side", [5], {}),
    ],
)
def test_the_bounds_a_headline_states_are_read(
    text: str, scope: list[int], expected: dict[tuple[int, str], Stated]
) -> None:
    assert check_standing.statements(text, scope) == expected


def test_the_claim_is_read_only_where_the_headline_states_no_bound() -> None:
    record = {
        "headline": "`s(17) ≥ 4613/1000`",
        "claim": "s(17) >= 4613/1000, below Bidwell's s(17) <= 4.6756.",
        "scope": {"n_values": [17]},
    }
    assert check_standing.stated_bounds(record) == {
        (17, LOWER): Stated(Fraction(4613, 1000), EXACT)
    }
    record["headline"] = "Weighted point lower bounds for one count"
    assert set(check_standing.stated_bounds(record)) == {(17, LOWER), (17, UPPER)}


@pytest.mark.parametrize(
    ("stated", "current", "direction", "expected"),
    [
        (Stated(Fraction(459, 100), EXACT), "4.66044", LOWER, BEATEN),
        (Stated(Fraction(116511, 25000), EXACT), "4.66044", LOWER, EQUAL),
        (Stated(Fraction(37, 5), EXACT), "7.1", LOWER, EXCEEDS),
        (Stated(Fraction(6), EXACT), "5.9", UPPER, BEATEN),
        (Stated(Fraction(6), EXACT), "6", UPPER, EQUAL),
        (Stated(Fraction("5.9"), EXACT), "6", UPPER, EXCEEDS),
        # Cut decimals equal a bound that starts with them, and no other.
        (Stated(Fraction("5.933833"), Fraction(1, 10**6)), "5.93383346267692", UPPER, EQUAL),
        (Stated(Fraction("3.8100257"), Fraction(1, 10**7)), "3.8100258", LOWER, BEATEN),
        (Stated(Fraction("5.933833"), Fraction(1, 10**6)), "5.933834", UPPER, EXCEEDS),
        (Stated(Fraction("5.933833"), Fraction(1, 10**6)), "5.9338", UPPER, BEATEN),
        (Stated(Fraction("3.8100257"), Fraction(1, 10**7)), "3.81002575", LOWER, EQUAL),
        (Stated(Fraction("3.8100257"), Fraction(1, 10**7)), "3.81", LOWER, EXCEEDS),
    ],
)
def test_a_stated_bound_is_beaten_by_equal_to_or_more_than_the_record(
    stated: Stated, current: str, direction: str, expected: str
) -> None:
    bound = {"value": current, "exact_form": None}
    assert check_standing.relation(stated, bound, direction) == expected
    assert check_standing.relation(stated, None, direction) is None


def _entry(records: view.Records, entry: str, **changed: Any) -> Mapping[str, Any]:
    return {**records.results[entry], **changed}


def test_a_superseded_entry_whose_bound_still_stands_is_refused(records: view.Records) -> None:
    """The mismatch one way: marked superseded, and still the best on record. T-093
    holds the verified bound at n = 17 (T-043 until 2026-10-05), and T-048's 37/5 is the
    verified bound at n = 50 since its replay was recorded on 2026-10-02. The reported
    lane is held too: n = 11's record reports the proved value as the source rounds it,
    below the verified one."""
    assert view.standing(records.results["T-093"], records) == view.HOLDS
    for entry, n in (("T-093", 17), ("T-048", 50)):
        (verified,) = check_standing.problems(records.results[entry], view.SUPERSEDED, records)
        assert f"{entry} is superseded, yet at n = {n}" in verified
        assert "no worse than the verified one" in verified
    rounded = _entry(records, "T-018", headline="`s(11) ≥ 3.87708359002281`")
    (reported,) = check_standing.problems(rounded, view.SUPERSEDED, records)
    assert "T-018 is superseded, yet at n = 11" in reported
    assert "no worse than the reported one" in reported
    # A tie is not superseded either: the same value under another entry's citation.
    tied = _entry(records, "T-001", headline="`s(17) ≥ 18641771/4000000`")
    assert check_standing.problems(tied, view.SUPERSEDED, records)


def test_a_superseded_report_is_held_to_the_reported_lane_alone(records: view.Records) -> None:
    """T-046 reports wand125's rectangle certificates at C0. Its replays (T-045, T-070)
    held verified bounds equal to some of its values, the last at n = 52 until T-082's
    certificate was decided there on 6 October, and every one is beaten in the reported
    lane, so it is superseded without a problem. The rule is held on the same entry
    stating n = 96's verified 997/100, below the reported 10 there: superseded as a
    report, and refused at a replayed rung."""
    record = records.results["T-046"]
    assert record["confirmation"] in check_standing.UNREPLAYED
    assert view.standing(record, records) == view.SUPERSEDED
    assert check_standing.problems(record, view.SUPERSEDED, records) == []
    assert "beaten at n = 18" in check_standing.summary(record, view.SUPERSEDED, records)
    tied = _entry(records, "T-046", headline="`s(96) ≥ 997/100`", scope={"n_values": [96]})
    assert check_standing.problems(tied, view.SUPERSEDED, records) == []
    assert "equals the verified bound at n = 96" in check_standing.summary(
        tied, view.SUPERSEDED, records
    )
    replayed = {**tied, "confirmation": "C3"}
    (problem,) = check_standing.problems(replayed, view.SUPERSEDED, records)
    assert "no worse than the verified one" in problem


def test_a_standing_entry_whose_every_bound_is_beaten_is_refused(records: view.Records) -> None:
    """The mismatch the other way: not marked superseded, and no longer the best at any
    case. T-001's 4.426213 is below the verified and the reported bound at n = 17."""
    assert view.standing(records.results["T-001"], records) == view.SUPERSEDED
    for standing in (view.HOLDS, view.HOLDS_REPORTED):
        (problem,) = check_standing.problems(records.results["T-001"], standing, records)
        assert "reads as superseded" in problem
    (second,) = check_standing.problems(
        records.results["T-001"], view.SECOND_CERTIFICATE, records
    )
    assert "does not state the verified value" in second


def test_an_entry_that_holds_one_case_of_several_stands(records: view.Records) -> None:
    """T-069 is beaten at n = 66, 90 and 92 and holds n = 37 and 65. It still holds a
    case bound, so it is not superseded, and the summary names both. The example was T-047
    until 2026-10-02, when the rectangle replays raised n = 26, 29 and 30, the last three
    it held; then T-044 until the replays of 1 October's certificates (T-074) raised n =
    56, the last count it held, later that day; then T-045 until 2026-10-05, when the
    replay of T-096's certificate on a declared net raised n = 18; then, briefly, T-071,
    until T-094's n = 84 certificate, decided here the same day, raised its last count.
    T-097's n = 66 certificate and T-091's n = 90, decided here on 2026-10-06, took two of
    T-069's counts."""
    record = records.results["T-069"]
    assert view.standing(record, records) == view.HOLDS
    assert check_standing.problems(record, view.HOLDS, records) == []
    line = check_standing.summary(record, view.HOLDS, records)
    assert "equals the verified bound at n = 37, 65 " in line
    assert "beaten at n = 66, 90, 92" in line
    assert check_standing.problems(record, view.SUPERSEDED, records)


def test_an_entry_may_not_state_more_than_its_case_record_carries(
    records: view.Records,
) -> None:
    over = _entry(records, "T-093", headline="`s(17) > 4.67`")
    (problem,) = check_standing.problems(over, view.HOLDS, records)
    assert "T-093 states more than the verified bound its case record carries" in problem


def test_an_entry_with_no_standing_states_no_bound(records: view.Records) -> None:
    """A rigidity, an exclusion or a method limit claims no bound, so no better bound
    supersedes it and it has no standing; one that stated a bound would be a bound."""
    record = records.results["T-014"]
    assert view.standing(record, records) == view.NO_STANDING
    assert check_standing.problems(record, view.NO_STANDING, records) == []
    stating = _entry(records, "T-014", headline="`s(5) ≥ 2`")
    (problem,) = check_standing.problems(stating, view.NO_STANDING, records)
    assert "T-014 has no standing, yet states a bound at n = 5" in problem


def test_a_superseded_entry_this_cannot_read_needs_another_holder(
    records: view.Records,
) -> None:
    """T-010's `2 + 4/√5` is a closed form with no decimals, so its supersession is
    held to the structure: T-060 holds the verified bound at n = 11. Were it the only
    entry at a case, as T-051 is at n = 32, nothing would have superseded it."""
    record = records.results["T-010"]
    assert check_standing.stated_bounds(record) == {}
    assert check_standing.problems(record, view.SUPERSEDED, records) == []
    alone = _entry(records, "T-010", id="T-051", scope={"n_values": [32]})
    (problem,) = check_standing.problems(alone, view.SUPERSEDED, records)
    assert "no other entry holds a verified bound" in problem


def test_the_command_fails_on_a_mismatch(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(view, "standing", lambda *_: view.SUPERSEDED)
    assert check_standing.main(["--cases"]) == 1
    printed = capsys.readouterr()
    assert "FAIL  T-093 is superseded, yet at n = 17" in printed.err
    assert "n = 17 lower 18641771/4000000: verified equal, reported equal" in printed.out
    assert "n = 17 lower 116511/25000: verified beaten, reported beaten" in printed.out
