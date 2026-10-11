"""The results page's weekly overview: every result at S3 and above from the last four
weeks, by week, crediting its finder, read from the register at render time.

The overview sits above the table and leaves it whole (`think-2z22`). Each check here
reads the rendered page against the register, never against a list kept beside it, so a
result registered tomorrow is checked the same way as one registered today.
"""

from __future__ import annotations

import dataclasses
import html
import re
from collections import Counter
from datetime import date, timedelta

import pytest

from devtools import overview_data, overview_sections, render_overview
from devtools.overview_data import EN_DASH
from devtools.overview_sections import (
    ROLLUP_FLOOR,
    ROLLUP_WEEKS,
    ROLLUP_WEEKS_WORD,
    credit_finder,
    rollup_order,
    rollup_weeks,
    week_label,
)
from tests import site_renders

#: One week's disclosure in the rendered overview: its Monday, whether it starts open,
#: and its body.
WEEK = re.compile(
    r'<details data-week="(\d{4}-\d{2}-\d{2})"( open)?>(.*?)</details>', re.DOTALL
)
#: One finder's line: the project its name links to, if any, the name, and the rest.
LINE = re.compile(
    r'<li><span class="site-rollup-who">(?:<a href="([^"]+)"[^>]*>)?([^<]+)(?:</a>)?</span>'
    r"(.*?)</li>",
    re.DOTALL,
)
#: One result's link in a line, with its attributes.
ID_LINK = re.compile(
    r'<a href="#(t-\d{3})"([^>]*)>(T-\d{3})</a>(<span class="site-rollup-s">'
    r"S(\d)</span>)?"
)
#: The most bytes the overview may weigh. It measured 11,605 bytes on 11 October 2026 with
#: 91 results in the four weeks to that day; this is about twice that.
#: Past it the overview is becoming a second table, and the remedy is a shorter line,
#: not a higher number: the page's own ceiling (`test_overview.PAGE_CEILINGS`) is shared
#: with every row of the table.
ROLLUP_BYTES = 24_000


@pytest.fixture(scope="module")
def results() -> str:
    return site_renders.html(render_overview.RESULTS_PAGE)


@pytest.fixture(scope="module")
def overview() -> overview_data.Overview:
    return site_renders.overview()


@pytest.fixture(scope="module")
def rollup(results: str) -> str:
    """The overview's block, cut from the rendered page."""
    start = results.index('<div class="site-rollup">')
    end = results.index("</details></div>", start) + len("</details></div>")
    return results[start:end]


def _shown_day(record: dict) -> date:
    """The day a register entry's row shows, read from the register directly: its
    publication for a result by others, else its establishment, else its registration;
    a year or a month is its first day."""
    attribution = record.get("attribution")
    shown = str(
        attribution["published"]
        if attribution
        else record.get("established") or record.get("registered")
    )
    return date.fromisoformat(shown + "-01-01"[max(len(shown) - 4, 0) :])


def test_the_overview_sits_above_the_table_and_leaves_it_whole(
    results: str, overview: overview_data.Overview
) -> None:
    """One overview, under its own heading, before the table and its first row; the
    table still carries one row for every register entry."""
    assert results.count('<div class="site-rollup">') == 1
    heading = results.index('<h2 id="recent-results-by-week">')
    assert (
        heading < results.index('<div class="site-rollup">') < results.index("data-site-table")
    )
    assert results.index('<div class="site-rollup">') < results.index('<h1 id="all-results">')
    rows = re.findall(r'<tr id="(t-\d{3})"', results)
    assert sorted(rows) == sorted(result.id.lower() for result in overview.results)


def test_the_introduction_states_the_floor_and_the_window_from_the_code(results: str) -> None:
    """The template types neither the floor nor the window: both are filled in."""
    words = ROLLUP_WEEKS_WORD[ROLLUP_WEEKS]
    assert f"Results at S{ROLLUP_FLOOR} and above from the last {words}," in results


def test_each_week_lists_exactly_the_entries_at_the_floor_dated_in_it(
    rollup: str, overview: overview_data.Overview
) -> None:
    """The weeks are the last four calendar weeks, Monday to Sunday, newest first, up to
    the week of the register's newest date; each lists every entry at S3 or above whose
    row's date falls in it, and nothing else, each once."""
    records = [result.record for result in overview.results]
    newest = max(
        *(date.fromisoformat(str(record["registered"])) for record in records),
        *(_shown_day(record) for record in records),
    )
    monday = newest - timedelta(days=newest.weekday())
    mondays = [monday - timedelta(weeks=back) for back in range(ROLLUP_WEEKS)]
    weeks = WEEK.findall(rollup)
    assert [date.fromisoformat(week) for week, _, _ in weeks] == mondays
    for week, _, body in weeks:
        start = date.fromisoformat(week)
        expected = sorted(
            str(record["id"]).lower()
            for record in records
            if int(record["significance"]["score"]) >= ROLLUP_FLOOR
            and start <= _shown_day(record) <= start + timedelta(days=6)
        )
        shown = [found[0] for found in ID_LINK.findall(body)]
        assert sorted(shown) == expected, week
        assert len(shown) == len(set(shown)), week
        count = len(expected)
        assert f"· {count} result{'' if count == 1 else 's'}</span>" in body or not count


def test_every_id_leads_to_its_own_row_on_this_page(rollup: str, results: str) -> None:
    """An id's link is the fragment of its row in the table below, and names it."""
    links = ID_LINK.findall(rollup)
    assert links
    for anchor, _, label, _, _ in links:
        assert anchor == label.lower()
        assert f'<tr id="{anchor}"' in results


def test_a_line_credits_its_finder_and_links_the_project_holding_most_of_it(
    rollup: str, overview: overview_data.Overview
) -> None:
    """Every result on a line has that line's finder as its credit's finder, and a
    finder has one line a week. The name links to a listed project the record attributes
    the most of the line's results to, and is plain where no listed project holds any."""
    by_id = {result.id.lower(): result for result in overview.results}
    addresses = {
        overview_sections.project_slug(url): url for url in overview_sections.project_urls()
    }
    for week, _, body in WEEK.findall(rollup):
        lines = LINE.findall(body)
        names = [html.unescape(name) for _, name, _ in lines]
        assert len(names) == len(set(names)), week
        for href, name, rest in lines:
            own = [by_id[anchor] for anchor, *_ in ID_LINK.findall(rest)]
            assert own, (week, name)
            assert {credit_finder(result.credit) for result in own} == {html.unescape(name)}
            held = Counter(
                slug for result in own for slug in overview_sections.result_projects(result)
            )
            if not held:
                assert not href, (week, name)
                continue
            most = max(held.values())
            assert href in {addresses[slug] for slug, count in held.items() if count == most}


def test_superseded_results_are_muted_and_the_most_significant_carry_their_rung(
    rollup: str, overview: overview_data.Overview
) -> None:
    """An id is muted, and titled so, exactly where its result is superseded; a result
    above the floor carries its S rung after its id, and one at the floor does not."""
    by_id = {result.id.lower(): result for result in overview.results}
    for anchor, attributes, _, rung, level in ID_LINK.findall(rollup):
        result = by_id[anchor]
        muted = 'class="site-rollup-superseded"' in attributes
        assert muted == overview_sections.is_superseded(result), anchor
        assert ('title="Superseded"' in attributes) == muted, anchor
        score = overview_sections.significance(result)
        assert bool(rung) == (score > ROLLUP_FLOOR), anchor
        assert not rung or int(level) == score, anchor


def test_only_the_newest_week_with_a_result_starts_open(rollup: str) -> None:
    """The page opens on one week's lines; every other week is one press away."""
    weeks = WEEK.findall(rollup)
    opened = [week for week, state, _ in weeks if state]
    first = next(week for week, _, body in weeks if "<li>" in body)
    assert opened == [first]


def test_lines_run_from_the_most_significant(overview: overview_data.Overview) -> None:
    """A week's lines are in `rollup_order`: the highest S rung first, then more
    results, then the newest, then by name."""
    reference = overview_sections.rollup_reference(overview)
    for week in rollup_weeks(overview.results, reference):
        keys = [rollup_order(credit) for credit in week.credits]
        assert keys == sorted(keys), week.monday


def test_the_overview_stays_brief(rollup: str) -> None:
    """The overview is a few lines a week, not a second table (`ROLLUP_BYTES`)."""
    size = len(rollup.encode("utf-8"))
    print(f"weekly overview: {size:,} bytes / {ROLLUP_BYTES:,}")
    assert size < ROLLUP_BYTES


def _entry(
    base: overview_data.Result,
    result_id: str,
    day: str,
    score: int,
    *,
    credit: str,
    kind: str = "lower-bound",
) -> overview_data.Result:
    """A register entry made from `base`: its id, the day it was published, its S rung,
    its credit line and its kind, attributed to no listed project."""
    record = {
        **base.record,
        "id": result_id,
        "kind": kind,
        "significance": {**base.record["significance"], "score": score},
        "attribution": {"published": day, "source_keys": []},
    }
    return dataclasses.replace(base, record=record, credit=credit)


def test_weeks_group_by_the_shown_day_and_drop_what_is_below_or_outside(
    overview: overview_data.Overview,
) -> None:
    """The rules on entries made for the purpose: a week runs Monday to Sunday; an entry
    below the floor, or dated before the window, is in no week; a week with nothing at
    the floor has no line; a finder's results share one line, oldest first, whatever
    follows "after" in their credits; and the lines run from the most significant."""
    base = overview.results[0]
    entries = [
        _entry(base, "T-901", "2026-10-05", 3, credit="Alpha after Beta"),
        _entry(base, "T-902", "2026-10-11", 3, credit="Alpha after Gamma", kind="upper-bound"),
        _entry(base, "T-903", "2026-10-12", 3, credit="Alpha"),
        _entry(base, "T-904", "2026-10-08", 2, credit="Delta"),
        _entry(base, "T-905", "2026-10-06", 4, credit="Epsilon"),
        _entry(base, "T-906", "2026-09-14", 5, credit="Zeta"),
        _entry(base, "T-907", "2026", 5, credit="Eta"),
    ]
    weeks = rollup_weeks(entries, date(2026, 10, 14), weeks=3)
    assert [week.monday for week in weeks] == [
        date(2026, 10, 12),
        date(2026, 10, 5),
        date(2026, 9, 28),
    ]
    newest, middle, oldest = weeks
    assert [(c.finder, [r.id for r in c.results]) for c in newest.credits] == [
        ("Alpha", ["T-903"])
    ]
    assert [(c.finder, [r.id for r in c.results]) for c in middle.credits] == [
        ("Epsilon", ["T-905"]),
        ("Alpha", ["T-901", "T-902"]),
    ]
    assert middle.total == 3
    assert oldest.credits == ()
    assert all(credit.projects == () for week in weeks for credit in week.credits)
    assert overview_sections.kind_phrase(middle.credits[1].results) == (
        "1 lower bound and 1 upper bound"
    )


def test_a_week_is_named_monday_to_sunday() -> None:
    """Within a month, across two months, and across a new year."""
    assert week_label(date(2026, 10, 5)) == f"5{EN_DASH}11 October 2026"
    assert week_label(date(2026, 9, 28)) == f"28 September {EN_DASH} 4 October 2026"
    assert week_label(date(2025, 12, 29)) == f"29 December 2025 {EN_DASH} 4 January 2026"


def test_a_kind_is_counted_in_words() -> None:
    """Bounds are nouns of their own; every other kind is a result of its kind."""
    base = site_renders.overview().results[0]
    made = [
        _entry(base, "T-911", "2026-10-05", 3, credit="A", kind="optimality"),
        _entry(base, "T-912", "2026-10-05", 3, credit="A", kind="optimality"),
        _entry(base, "T-913", "2026-10-05", 3, credit="A", kind="case-exclusion"),
        _entry(base, "T-914", "2026-10-05", 3, credit="A", kind="lower-bound"),
    ]
    assert overview_sections.kind_phrase(made) == (
        "1 lower bound, 2 optimality results and 1 case exclusion result"
    )
