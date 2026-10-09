"""The recent rows, their counts and each entry's standing are what the record says.

`devtools.render_recent_results` reads them for the site's overview and `RESULTS.md`
(README's three generated results tables moved to the site). These are the properties
that make them mean something: the rows are exactly the cases the record calls recent,
the verified bounds the atlas stars and the reported bounds the register's coverage gate
must hold; the counts are the rows; and standing is derived from the case records.
"""

from __future__ import annotations

import re
from fractions import Fraction

import pytest

from devtools import check_results
from devtools import render_recent_results as view
from devtools.build_bound_citations import PROJECT_NAME, load_case, recent_lower_bounds
from devtools.check_results import recent_evidence

ELLIPSIS = "…"


@pytest.fixture(scope="module")
def records() -> view.Records:
    return view.load_records()


@pytest.fixture(scope="module")
def rows(records: view.Records) -> list[view.Row]:
    return view.recent_rows(records)


def test_the_rows_are_the_recent_cases(records: view.Records, rows: list[view.Row]) -> None:
    """The row set is the atlas's stars plus the reported bounds the register must hold."""
    starred = {n for n in recent_lower_bounds() if n <= view.HUNDRED}
    reported = {
        n
        for n in range(1, view.HUNDRED + 1)
        if any(
            recent_evidence(records.register.evidence[item], records.sources)
            for item in load_case(n)["reported_lower_bound"]["evidence"]
        )
    }
    assert {row.n for row in rows} == starred | reported
    assert {row.n for row in rows if row.verified.recent} == starred
    assert [row.n for row in rows] == sorted(row.n for row in rows)


def test_every_recent_lane_names_its_holder_entry_lineage_and_date(
    records: view.Records, rows: list[view.Row]
) -> None:
    """Credit is the bibliography's, and the coverage gate gives each a register entry."""
    credited = {source.credited for source in records.register.sources.values()}
    for row in rows:
        for lane in (row.verified, row.reported):
            if not lane.recent:
                continue
            assert lane.holder in credited | {PROJECT_NAME}, (row.n, lane.holder)
            assert lane.results.startswith("T-"), (row.n, lane.results)
            assert lane.lineage, row.n
            assert lane.published, row.n


def test_the_counts_are_the_rows(rows: list[view.Row]) -> None:
    counts = view.recent_counts(rows)
    verified = [row for row in rows if row.verified.recent]
    assert counts.cases == len(rows)
    assert counts.verified == len(verified)
    assert counts.ours == sum(row.verified.holder == PROJECT_NAME for row in verified)
    assert counts.exact == sum(row.exact for row in verified)


@pytest.mark.parametrize(
    ("value", "shown"),
    [
        (Fraction(31, 8), "3.875"),
        (Fraction(15680, 3951), f"3.9686{ELLIPSIS}"),
        (Fraction(116511, 25000), "4.66044"),
        (Fraction(5), "5"),
        (Fraction(2, 3), f"0.6666{ELLIPSIS}"),
    ],
)
def test_decimals_are_exact_or_cut_never_rounded_up(value: Fraction, shown: str) -> None:
    assert view.digits(value) == shown


def test_standing_is_one_of_the_derived_words(records: view.Records) -> None:
    for record in records.register.results:
        standing = view.standing(record, records)
        assert standing in (*view.STANDINGS, view.NO_STANDING), record["id"]


def test_an_entry_that_claims_no_bound_has_no_standing(records: view.Records) -> None:
    """Standing is about bounds. An entry whose evidence claims none has no standing, and
    its kind is never one of the three bounds; no standing says only what an entry is
    not."""
    without = {}
    for record in records.register.results:
        if view.standing(record, records) == view.NO_STANDING:
            assert record["kind"] not in check_results.BOUND_KINDS, record["id"]
            without[record["id"]] = record["kind"]
    assert view.NO_STANDING not in view.STANDINGS
    assert not any("bound" in standing for standing in view.STANDINGS)
    assert set(without.values()) == {
        "uniqueness",
        "rigidity",
        "case-exclusion",
        "restricted-optimality",
        "method-limit",
        "audit",
        # T-085, from 2026-10-02: the correction of Nagamochi's Lemma 1 cites the exact
        # recomputation of its counterexample, which claims no bound.
        "correction",
    }
    # T-112, from 2026-10-06: the uniqueness of the optimal packing of eleven squares
    # cites only its derived-structure entry, which claims no bound.
    # T-124 reports local minima of source configurations, without a global bound.
    assert without["T-124"] == "restricted-optimality"
    assert len(without) == 12


def test_standing_agrees_with_the_recent_rows(
    records: view.Records, rows: list[view.Row]
) -> None:
    """An entry a recent row names as a bound's holder holds a bound by `standing` too."""
    for row in rows:
        for entry in re.findall(r"T-\d{3}", row.verified.results):
            assert view.standing(records.results[entry], records) == view.HOLDS, (row.n, entry)
        if row.shows_reported and row.reported.recent:
            for entry in re.findall(r"T-\d{3}", row.reported.results):
                assert view.standing(records.results[entry], records) in {
                    view.HOLDS,
                    view.HOLDS_REPORTED,
                }, (row.n, entry)


@pytest.mark.parametrize(
    ("entry", "expected"),
    [
        # A rung of the n = 18 ladder shares its interval decision with the rung that
        # holds the bound; a shared checker does not make it hold.
        ("T-027", view.SUPERSEDED),
        # A rigidity theorem claims no bound on s(n), so it has no standing.
        ("T-014", view.NO_STANDING),
        ("T-036", view.NO_STANDING),
        ("T-059", view.NO_STANDING),
        # A second proof of s(45) = 7, whose bound Evan Daniel's cover holds.
        ("T-054", view.SECOND_CERTIFICATE),
        # A second, point-only route to s(21) = 5, reported until its complete replay here
        # was recorded on 2026-10-02.
        ("T-055", view.SECOND_CERTIFICATE),
        # Couzo's eight rational certificates of 8 October report sides below every
        # ceiling their cases hold, and the case records have not taken them in yet.
        ("T-128", view.PENDING_ADOPTION),
    ],
)
def test_standing_is_read_from_the_case_records(
    records: view.Records, entry: str, expected: str
) -> None:
    assert view.standing(records.results[entry], records) == expected


def test_the_recent_rows_date_this_projects_bounds_by_establishment(
    records: view.Records, rows: list[view.Row]
) -> None:
    for row in rows:
        if row.verified.ours:
            entry = re.findall(r"T-\d{3}", row.verified.results)[0]
            assert row.verified.published == records.results[entry]["established"], row.n


def test_every_recent_result_by_others_has_a_relation(records: view.Records) -> None:
    for record in records.register.results:
        if view.is_recent_by_others(record):
            assert view.relation(record, records) in view.LINEAGES.values(), record["id"]


def test_a_rounded_report_of_the_verified_result_is_not_awaiting_replay(
    rows: list[view.Row],
) -> None:
    """think-pd2g. n = 11's record reports T as the source's rounded display,
    `3.87708359002281`, below the 32-place verified value; both lanes carry T-060.
    Compared as numbers they differed, so T-060 was listed as awaiting its own replay,
    with a reported value below the verified one. The source's value stays as reported."""
    case = load_case(11)
    assert case["reported_lower_bound"]["value"] == "3.87708359002281"
    eleven = next(row for row in rows if row.n == 11)
    assert eleven.reported.value < eleven.verified.value
    assert eleven.reported.results == eleven.verified.results == "T-060 `V3/C3`"
    assert not eleven.shows_reported
    assert eleven.described == [eleven.verified]
    # Each clause decides n = 11 by itself: the same entry, and the same value printed.
    assert eleven.reported.same_value(eleven.verified)


def _lane(value: str, exact_form: str | None, holder: str, results: str) -> view.Lane:
    bound = {"value": value, "exact_form": exact_form}
    return view.Lane(
        view.magnitude(bound),
        view.shown(bound),
        holder,
        results,
        recent=True,
        ours=False,
        lineage="independent",
        published="2026-09-01",
        bound=bound,
    )


T = "3.87708359002281417730789706010096"


@pytest.mark.parametrize(
    ("reported", "verified", "shows"),
    [
        # One result carried by both lanes is one lane, whatever each prints.
        (
            _lane("3.8", None, "A", "T-900 `V4/C3`"),
            _lane("3.9", "39/10", "A", "T-900 `V4/C3`"),
            False,
        ),
        # The same holder's rounded display of the verified closed form.
        (
            _lane("3.87708359002281", None, "A", "T-901 `V0/C0`"),
            _lane(T, f"root(P, {T})", "A", "T-900 `V4/C3`"),
            False,
        ),
        # A display agrees within half a unit of the coarser printed place, and no further.
        (
            _lane("4.68", None, "A", "T-901 `V0/C0`"),
            _lane("4.675", "187/40", "A", "T-900 `V4/C3`"),
            False,
        ),
        (
            _lane("4.68", None, "A", "T-901 `V0/C0`"),
            _lane("4.6749", "46749/10000", "A", "T-900 `V4/C3`"),
            True,
        ),
        # Two exact forms agree only where they are one number.
        (
            _lane("4.68", "117/25", "A", "T-901 `V0/C0`"),
            _lane("4.6789", "46789/10000", "A", "T-900 `V4/C3`"),
            True,
        ),
        (
            _lane("4.68", "117/25", "A", "T-901 `V0/C0`"),
            _lane("4.68", "468/100", "A", "T-900 `V4/C3`"),
            False,
        ),
        # Another holder's report is its own entry however close the value.
        (
            _lane("4.68", None, "B", "T-901 `V0/C0`"),
            _lane("4.68", "117/25", "A", "T-900 `V4/C3`"),
            True,
        ),
    ],
)
def test_a_reported_lane_is_its_own_entry_only_where_it_says_something_else(
    reported: view.Lane, verified: view.Lane, *, shows: bool
) -> None:
    row = view.Row(18, exact=False, verified=verified, reported=reported)
    assert row.shows_reported is shows
