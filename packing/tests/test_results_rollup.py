"""The results page's overview above its table, read from the register at render time.

Two sections (`think-2z22`). "Added in the Last Seven Days" lists every result the
register took in over its newest day and the seven before it, one block a day by
`registered`, at every significance; the owner asked on 12 October 2026 to see easily
what was imported in the last day. Under it, the weekly rollup of S3 and above by
publication, for the four weeks before those days, which the owner asked for on 11
October. The table stays whole and gains one filter on the same date, Added
(`?added-age=1`, `?added=2026-10-12`).

Each check reads the rendered page against the register, never against a list kept
beside it, so a result registered tomorrow is checked the same way as one registered
today.
"""

from __future__ import annotations

import dataclasses
import html
import re
from collections import Counter
from datetime import date, timedelta
from html.parser import HTMLParser

import pytest

from devtools import overview_data, overview_sections, profile_links, render_overview
from devtools.overview_data import EN_DASH
from devtools.overview_sections import (
    ADDED_DAYS,
    ADDED_DAYS_WORD,
    ADDED_OPEN,
    ROLLUP_FLOOR,
    ROLLUP_WEEKS,
    ROLLUP_WEEKS_WORD,
    added_days,
    credit_finder,
    rollup_order,
    rollup_weeks,
    span_label,
    week_label,
)
from tests import site_renders

#: One week's disclosure in the rendered rollup: its Monday, whether it starts open,
#: and the rest.
WEEK = re.compile(
    r'<details data-week="(\d{4}-\d{2}-\d{2})"( open)?>(.*?)</details>', re.DOTALL
)
#: One day's disclosure in the seven days: its date, whether it starts open, the rest.
DAY = re.compile(r'<details data-day="(\d{4}-\d{2}-\d{2})"( open)?>(.*?)</details>', re.DOTALL)
#: One finder's line: the project its name links to, if any, the name, and the rest.
LINE = re.compile(r'<li><span class="site-rollup-who">()(.*?)</span> (.*?)</li>', re.DOTALL)

#: One result's link in a line, with its attributes, and what it says to a screen
#: reader past its id when it has been superseded.
ID_LINK = re.compile(
    r'<a href="#(t-\d{3})"([^>]*)>(T-\d{3})'
    r'(<span class="site-visually-hidden"> \(superseded\)</span>)?</a>'
    r'(<span class="site-rollup-s">S(\d)</span>)?'
)
#: One result in a day: whether it is muted, its row, the title of its id, its id, its
#: headline, its cases, its V and C rungs, its S score (bold above the floor), the
#: project its credit links to if any, the credit's name, and the word that says it has
#: been superseded.
ENTRY = re.compile(
    r'<li( class="site-rollup-superseded")?><a href="#(t-\d{3})"( title="Superseded")?>'
    r"(T-\d{3})</a> (.*?)<small>([^<]*) · (V\d) (C\d) (<b>S\d</b>|S\d) · "
    r"()(.*?)( · superseded)?</small></li>",
    re.DOTALL,
)

#: A day's link to its own rows: the day it filters on and how many it says it shows.
DAY_LINK = re.compile(
    r'<p><a href="results\.html\?added=(\d{4}-\d{2}-\d{2})#all-results">'
    r"Show (it|these (\d+)) in the table</a></p>"
)
#: The most bytes the overview, both sections, may weigh. The weekly prototype measured
#: 11,605 bytes on 11 October 2026 and was held to 24,000. On 12 October the two
#: sections measured 28,187: 20,013 for the 65 results added over 5-12 October, about
#: 308 bytes a result with its headline, cases, rungs and linked credit, which the owner
#: asked for, and 8,174 for the 55 S3+ results of the four weeks before. The busiest
#: eight days so far, to 6 October, registered 76 results, about 23,400 bytes at that
#: rate, and the four-week rollup has held 91 (11,605), so this is about 1.4 times the
#: largest the record has given. Grouped by the day each result reached the site
#: (`landed`), on the register at the merge with `main` on 14 October (`37e6757ed`), the
#: two measured 25,891: 15,452 for the 48 results that arrived over 7-14 October and
#: 10,439 for 68 in the weeks before. At 217 results on 19 October they measure 37,858,
#: 79% of the ceiling: 22,157 for the 71 results that arrived over 12-19 October, about
#: 312 bytes each, and 15,701 for 97 in the four weeks before. So a window holding about
#: 32 more arrivals than that one fails this test, and single days have brought 30 (14
#: October) and 23 (19 October). The page's own ceiling binds first, at about 9 results,
#: but the intake that moves it (`think-v1qe`) may carry more than 32, and then meets this
#: limit too (#514's review D, finding D3).
#: Past it the overview is becoming a second table, and the remedy is a shorter entry,
#: not a higher number: the page's own ceiling (`test_overview.PAGE_CEILINGS`) is shared
#: with every row of the table.
ROLLUP_BYTES = 48_000


@pytest.fixture(scope="module")
def results() -> str:
    return site_renders.html(render_overview.RESULTS_PAGE)


@pytest.fixture(scope="module")
def overview() -> overview_data.Overview:
    return site_renders.overview()


def _cut(page: str, start: str) -> str:
    """A section's block, from its opening tag to the end of its last disclosure."""
    begin = page.index(start)
    end = page.index("</details></div>", begin) + len("</details></div>")
    return page[begin:end]


@pytest.fixture(scope="module")
def added(results: str) -> str:
    """The seven days' block, cut from the rendered page."""
    return _cut(results, '<div class="site-rollup site-added">')


@pytest.fixture(scope="module")
def rollup(results: str) -> str:
    """The weekly rollup's block, cut from the rendered page."""
    return _cut(results, '<div class="site-rollup">')


def _registered(record: dict) -> date:
    return date.fromisoformat(str(record["registered"]))


def _landed(record: dict) -> date:
    """The day an entry reached the site, read from the register directly: its `landed`,
    or for an entry a branch adds and no merge has stamped yet, its `registered`."""
    return date.fromisoformat(str(record.get("landed") or record["registered"]))


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


def _window(overview: overview_data.Overview) -> tuple[date, date]:
    """The seven days' first and last day, read from the register: the newest day an
    entry reached the site and the seven days before it."""
    newest = max(_landed(result.record) for result in overview.results)
    return newest - timedelta(days=ADDED_DAYS), newest


def test_the_overview_sits_above_the_table_and_leaves_it_whole(
    results: str, overview: overview_data.Overview
) -> None:
    """Two sections, each under its own heading, the seven days first, both before the
    table and its first row; the table still carries one row for every register entry."""
    assert results.count('<div class="site-rollup site-added">') == 1
    assert results.count('<div class="site-rollup">') == 1
    order = [
        results.index('<h2 id="added-in-the-last-seven-days">'),
        results.index('<div class="site-rollup site-added">'),
        results.index('<h2 id="earlier-results-by-week-published">'),
        results.index('<div class="site-rollup">'),
        results.index('<h1 id="all-results">'),
        results.index("data-site-table"),
    ]
    assert order == sorted(order)
    rows = re.findall(r'<tr id="(t-\d{3})"', results)
    assert sorted(rows) == sorted(result.id.lower() for result in overview.results)


def test_the_introductions_state_the_window_and_the_floor_from_the_code(
    results: str, overview: overview_data.Overview
) -> None:
    """The template types neither the days, the floor nor the weeks: all are filled in.
    The seven days' heading opens the table on the section's own days, from its first,
    `?added-since=`, so it lists the same results on any later day (#514's review A,
    finding A3); the introduction links the last day's arrivals by the reader's day."""
    first, last = _window(overview)
    days = ADDED_DAYS_WORD[ADDED_DAYS]
    assert (
        '<h2 id="added-in-the-last-seven-days"><a href="results.html?added-since='
        f'{first.isoformat()}#all-results">Added in the Last {days.capitalize()} Days</a></h2>'
    ) in results
    prose = " ".join(results.split())
    assert f"reached this site over {span_label(first, last)} (its newest day and the" in prose
    last_day = '<a href="results.html?added-age=1#all-results">what arrived in the last day</a>'
    assert last_day in prose
    words = ROLLUP_WEEKS_WORD[ROLLUP_WEEKS]
    shown = overview_sections.day_label(first)
    assert f"Results at S{ROLLUP_FLOOR} and above from the {words} before {shown}," in prose


def test_each_day_lists_exactly_the_entries_that_arrived_on_it(
    added: str, overview: overview_data.Overview
) -> None:
    """The blocks are the days from the window's first to the newest on which any result
    reached the site (`landed`), newest first, each once; each lists every entry that
    arrived that day, at any significance, each once, and its count says how many. The
    two newest start open, the rest closed."""
    first, last = _window(overview)
    records = [result.record for result in overview.results]
    taken = Counter(_landed(record) for record in records if _landed(record) >= first)
    days = DAY.findall(added)
    assert [date.fromisoformat(day) for day, _, _ in days] == sorted(taken, reverse=True)
    assert date.fromisoformat(days[0][0]) == last
    assert [bool(state) for _, state, _ in days] == [
        index < ADDED_OPEN for index in range(len(days))
    ]
    for day, _, body in days:
        expected = sorted(
            str(record["id"]).lower()
            for record in records
            if _landed(record) == date.fromisoformat(day)
        )
        shown = [entry[1] for entry in ENTRY.findall(body)]
        assert sorted(shown) == expected, day
        assert len(shown) == len(set(shown)) == body.count("<li"), day
        count = len(expected)
        assert f"· {count} result{'' if count == 1 else 's'}</span>" in body, day


class _CreditHTML(HTMLParser):
    """Keep credit text, element order and exact attributes while ignoring quotes."""

    def __init__(self, markup: str) -> None:
        super().__init__(convert_charrefs=True)
        self.events: list[tuple[str, object]] = []
        self.parts: list[str] = []
        self.links: list[dict[str, str | None]] = []
        self.feed(markup)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.events.append(("start", (tag, sorted(attrs))))
        if tag == "a":
            self.links.append(dict(attrs))

    def handle_endtag(self, tag: str) -> None:
        self.events.append(("end", tag))

    def handle_data(self, data: str) -> None:
        self.events.append(("text", data))
        self.parts.append(data)


def _assert_finder(
    markup: str, own: list[overview_data.Result] | tuple[overview_data.Result, ...]
) -> None:
    """Retain the reviewed joins; a conflicting grouping must not choose one identity."""
    finders = {credit_finder(result.credit) for result in own}
    assert len(finders) == 1
    finder = next(iter(finders))
    reviewed = {
        credit_finder(result.credit_html or html.escape(result.credit)) for result in own
    }
    actual = _CreditHTML(markup)
    if len(reviewed) != 1:
        assert actual.events == _CreditHTML(html.escape(finder)).events
        return
    expected = next(iter(reviewed))
    if any(
        (link.get("href") or "").startswith("profiles/") for link in _CreditHTML(expected).links
    ):
        assert (
            actual.events
            == _CreditHTML(f"<span data-contributor-plain>{expected}</span>").events
        )
        assert all(link.get("target") != "_blank" for link in actual.links)
        return
    assert "".join(actual.parts) == finder
    held = Counter(slug for result in own for slug in overview_sections.result_projects(result))
    links = [link.get("href") for link in actual.links]
    if not held:
        assert not links
    else:
        addresses = {
            overview_sections.project_slug(url): url for url in overview_sections.project_urls()
        }
        most = max(held.values())
        assert len(links) == 1
        assert links[0] in {addresses[slug] for slug, count in held.items() if count == most}


def test_a_day_entry_says_what_the_row_says(
    added: str, results: str, overview: overview_data.Overview
) -> None:
    """Each entry's id leads to its own row; its headline is the register's, its cases
    the row's (or how many and the ends of a long list), its rungs and score the
    register's, an S4 or S5 in bold; its credit is the credit line's finder, linked to
    the first listed project the record attributes the result to, plainly named where
    none does; and it is muted and its id titled exactly where it is superseded. The
    entries of a day run from the highest S rung, then by id."""
    by_id = {result.id.lower(): result for result in overview.results}
    for _, _, body in DAY.findall(added):
        entries = ENTRY.findall(body)
        keys = []
        for (
            muted,
            anchor,
            title,
            label,
            headline,
            cases,
            v,
            c,
            score,
            href,
            name,
            note,
        ) in entries:
            result = by_id[anchor]
            record = result.record
            assert label.lower() == anchor
            assert f'<tr id="{anchor}"' in results
            expected_headline = profile_links.link_prose(
                html.escape(overview_sections.plain_text(result.summary), quote=False)
            )
            assert _CreditHTML(headline).events == _CreditHTML(expected_headline).events
            if len(result.scope) <= overview_sections.ADDED_CASES:
                assert html.unescape(cases) == f"n = {result.scope}", anchor
            else:
                assert re.fullmatch(r"\d+ counts from \d+ to \d+", cases), anchor
            assert (v, c) == (record["verification"], record["confirmation"])
            level = overview_sections.significance(result)
            bold = level > ROLLUP_FLOOR
            assert score == (f"<b>S{level}</b>" if bold else f"S{level}"), anchor
            _assert_finder(name, (result,))
            assert not href
            superseded = overview_sections.is_superseded(result)
            assert bool(muted) == bool(title) == bool(note) == superseded, anchor
            keys.append((-level, result.id))
        assert keys == sorted(keys)


def test_each_day_and_the_heading_open_the_table_on_their_rows(
    added: str, results: str
) -> None:
    """A day's link opens the table on that day alone, `?added=2026-10-12`, which the
    bar's preset-only Added on control offers, every day anything reached the site among
    its choices; the heading's opens it from the section's first day, `?added-since=`,
    which the preset-only Added since control takes; and the visible Added within control
    takes an age of arrival, `?added-age=1`."""
    days = DAY.findall(added)
    bar = results.split('<div class="site-table-tools site-result-filters">', 1)[1]
    bar = bar.split("</div>", 1)[0]
    on = re.search(
        r'<label hidden>Added on <select data-filter="added" data-preset>(.*?)</select>', bar
    )
    assert on
    offered = re.findall(r'<option value="([^"]*)"(?: selected)?>([^<]*)</option>', on[1])
    taken = sorted(set(re.findall(r'data-added="([^"]+)"', results)), reverse=True)
    assert offered == [
        ("", "All"),
        *((day, overview_sections.day_label(date.fromisoformat(day))) for day in taken),
    ]
    assert (
        '<label>Added within <input type="number" data-filter="added" data-bound="age" '
        'min="0" placeholder="any"> days</label>'
    ) in bar
    assert (
        '<label hidden>Added since <input type="date" data-filter="added" data-bound="since" '
        "data-preset></label>"
    ) in bar
    for day, _, body in days:
        link = DAY_LINK.search(body)
        assert link, day
        assert link[1] == day
        count = len(ENTRY.findall(body))
        assert link[2] == ("it" if count == 1 else f"these {count}"), day


def test_each_week_lists_exactly_the_entries_at_the_floor_dated_in_it(
    rollup: str, overview: overview_data.Overview
) -> None:
    """The weeks are the four calendar weeks, Monday to Sunday, newest first, before the
    seven days, the newest ending the day before they begin; each lists every entry at S3
    or above whose row's date falls in it, and nothing else, each once. Every week starts
    closed."""
    first, _ = _window(overview)
    last = first - timedelta(days=1)
    records = [result.record for result in overview.results]
    monday = last - timedelta(days=last.weekday())
    mondays = [monday - timedelta(weeks=back) for back in range(ROLLUP_WEEKS)]
    weeks = WEEK.findall(rollup)
    assert [date.fromisoformat(week) for week, _, _ in weeks] == mondays
    assert not any(state for _, state, _ in weeks)
    for week, _, body in weeks:
        start = date.fromisoformat(week)
        end = min(start + timedelta(days=6), last)
        expected = sorted(
            str(record["id"]).lower()
            for record in records
            if int(record["significance"]["score"]) >= ROLLUP_FLOOR
            and start <= _shown_day(record) <= end
        )
        shown = [found[0] for found in ID_LINK.findall(body)]
        assert sorted(shown) == expected, week
        assert len(shown) == len(set(shown)), week
        count = len(expected)
        assert f"<span>{span_label(start, end)} " in body, week
        assert f"· {count} result{'' if count == 1 else 's'}</span>" in body or not count


def test_every_result_at_the_floor_since_the_rollup_begins_is_in_one_section_or_both(
    added: str, rollup: str, overview: overview_data.Overview
) -> None:
    """No gap between the two: a result at S3 or above shown on any day from the
    rollup's first Monday on is in the weekly rollup, the seven days, or both, since no
    row shows a day later than its registration, and none was registered after it reached
    the site. One published before the seven days and arriving in them is in both."""
    first, _ = _window(overview)
    last = first - timedelta(days=1)
    oldest = last - timedelta(days=last.weekday()) - timedelta(weeks=ROLLUP_WEEKS - 1)
    in_days = {entry[1] for entry in ENTRY.findall(added)}
    in_weeks = {found[0] for found in ID_LINK.findall(rollup)}
    for result in overview.results:
        record = result.record
        assert _shown_day(record) <= _registered(record) <= _landed(record), result.id
        if overview_sections.significance(result) >= ROLLUP_FLOOR and (
            _shown_day(record) >= oldest
        ):
            assert result.id.lower() in in_days | in_weeks, result.id


def test_every_id_leads_to_its_own_row_on_this_page(rollup: str, results: str) -> None:
    """An id's link is the fragment of its row in the table below, and names it."""
    links = ID_LINK.findall(rollup)
    assert links
    for anchor, _, label, _, _, _ in links:
        assert anchor == label.lower()
        assert f'<tr id="{anchor}"' in results


def test_a_line_credits_its_finder_and_links_the_project_holding_most_of_it(
    rollup: str, overview: overview_data.Overview
) -> None:
    """Every result on a line has that line's finder as its credit's finder, and a
    finder has one line a week. The name links to a listed project the record attributes
    the most of the line's results to, and is plain where no listed project holds any."""
    by_id = {result.id.lower(): result for result in overview.results}
    for week, _, body in WEEK.findall(rollup):
        lines = LINE.findall(body)
        names = [html.unescape(re.sub(r"<[^>]*>", "", name)) for _, name, _ in lines]
        assert len(names) == len(set(names)), week
        for href, name, rest in lines:
            own = [by_id[anchor] for anchor, *_ in ID_LINK.findall(rest)]
            assert own, (week, name)
            _assert_finder(name, own)
            assert not href


def test_superseded_results_are_muted_and_the_most_significant_carry_their_rung(
    rollup: str, overview: overview_data.Overview
) -> None:
    """An id is muted, titled so and says so to a screen reader exactly where its result
    is superseded (#514's review A, finding A4); a result above the floor carries its S
    rung after its id, and one at the floor does not."""
    by_id = {result.id.lower(): result for result in overview.results}
    for anchor, attributes, _, spoken, rung, level in ID_LINK.findall(rollup):
        result = by_id[anchor]
        muted = 'class="site-rollup-superseded"' in attributes
        assert muted == overview_sections.is_superseded(result), anchor
        assert ('title="Superseded"' in attributes) == bool(spoken) == muted, anchor
        score = overview_sections.significance(result)
        assert bool(rung) == (score > ROLLUP_FLOOR), anchor
        assert not rung or int(level) == score, anchor


def test_lines_run_from_the_most_significant(overview: overview_data.Overview) -> None:
    """A week's lines are in `rollup_order`: the highest S rung first, then more
    results, then the newest, then by name."""
    last = overview_sections.added_since(overview) - timedelta(days=1)
    for week in rollup_weeks(overview.results, last):
        keys = [rollup_order(credit) for credit in week.credits]
        assert keys == sorted(keys), week.monday


def test_the_overview_stays_brief(added: str, rollup: str) -> None:
    """The overview is a line or two a result, not a second table (`ROLLUP_BYTES`)."""
    days, weeks = len(added.encode("utf-8")), len(rollup.encode("utf-8"))
    print(f"overview: {days:,} + {weeks:,} = {days + weeks:,} bytes / {ROLLUP_BYTES:,}")
    assert days + weeks < ROLLUP_BYTES


def _entry(
    base: overview_data.Result,
    result_id: str,
    day: str,
    score: int,
    *,
    credit: str,
    kind: str = "lower-bound",
    registered: str | None = None,
    landed: str | None = None,
) -> overview_data.Result:
    """A register entry made from `base`: its id, the day it was published, its S rung,
    its credit line, its kind, the day it was registered, the day it was published
    unless given, and the day it reached the site, the day it was registered unless given,
    or none when `landed` is empty, which the schema no longer allows; attributed to no listed
    project."""
    record = {
        **base.record,
        "id": result_id,
        "kind": kind,
        "registered": registered or day,
        "landed": landed if landed is not None else registered or day,
        "significance": {**base.record["significance"], "score": score},
        "attribution": {"published": day, "source_keys": []},
    }
    if not record["landed"]:
        del record["landed"]
    return dataclasses.replace(base, record=record, credit=credit, credit_html="")


def test_days_group_by_arrival_and_not_by_registration_or_publication(
    overview: overview_data.Overview,
) -> None:
    """The rules on entries made for the purpose: a result is placed by the day it reached
    the site (`landed`), so one published in 2018, registered on 10 October and landing on
    11 October is in that day's block and in no recent week, and so is one registered on
    9 October that waited two days to merge (#514's review A, finding A1); results
    arriving on different days are in different blocks, newest first; one that arrived
    before the window is in none; a record with no `landed`, which the schema no longer
    allows in the register, is placed by its registration; every significance counts, the
    highest first within a day; and a
    day nothing arrived on has no block."""
    base = overview.results[0]
    entries = [
        _entry(
            base, "T-921", "2018", 2, credit="Old", registered="2026-10-10", landed="2026-10-11"
        ),
        _entry(base, "T-922", "2026-10-12", 4, credit="New"),
        _entry(base, "T-923", "2026-10-03", 5, credit="Before"),
        _entry(base, "T-924", "2026-10-09", 3, credit="Late", landed="2026-10-11"),
        _entry(base, "T-925", "2026-10-07", 1, credit="Low"),
        _entry(base, "T-926", "2026-10-12", 1, credit="Unstamped", landed=""),
    ]
    days = added_days(entries, date(2026, 10, 5))
    assert [(day.day, [result.id for result in day.results]) for day in days] == [
        (date(2026, 10, 12), ["T-922", "T-926"]),
        (date(2026, 10, 11), ["T-924", "T-921"]),
        (date(2026, 10, 7), ["T-925"]),
    ]
    assert 'data-added="2026-10-11"' in overview_sections.result_facets(entries[3])
    assert 'data-added="2026-10-12"' in overview_sections.result_facets(entries[5])
    # An entry says its own rungs whatever its day: an S4 or S5 in bold, below that plain.
    assert "<b>S4</b> · " in overview_sections.added_entry(entries[1])
    assert " S2 · " in overview_sections.added_entry(entries[0])
    assert "<b>" not in overview_sections.added_entry(entries[0])
    weeks = rollup_weeks(entries, date(2026, 10, 4), weeks=4, floor=1)
    assert [
        result.id for week in weeks for line in week.credits for result in line.results
    ] == ["T-923"]


def test_the_seven_days_start_from_the_registers_newest_arrival(
    overview: overview_data.Overview,
) -> None:
    """The window is the register's, never the clock's: the newest day an entry reached
    the site and the seven days before it, as `?added-age=7` reaches back on that day
    (`age_cutoff`). It is no earlier than the newest registration, which runs ahead of
    arrival."""
    reference = overview_sections.added_reference(overview)
    assert reference == max(_landed(result.record) for result in overview.results)
    assert reference >= overview_sections.reference_date(overview)
    since = overview_sections.added_since(overview)
    assert since == reference - timedelta(days=ADDED_DAYS)
    assert since.isoformat() == overview_sections.age_cutoff(reference, ADDED_DAYS)


def test_weeks_group_by_the_shown_day_and_drop_what_is_below_or_outside(
    overview: overview_data.Overview,
) -> None:
    """The rules on entries made for the purpose: a week runs Monday to Sunday, the
    newest cut at the day before the seven days; an entry below the floor, or dated
    before the window or after its last day, is in no week; a week with nothing at the
    floor has no line; a finder's results share one line, oldest first, whatever follows
    "after" in their credits; and the lines run from the most significant."""
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
    assert [week.last for week in weeks] == [
        date(2026, 10, 14),
        date(2026, 10, 11),
        date(2026, 10, 4),
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
    # Cut at a Wednesday, the newest week ends there and holds nothing after it.
    cut = rollup_weeks(entries, date(2026, 10, 7), weeks=1)
    assert [(week.monday, week.last) for week in cut] == [
        (date(2026, 10, 5), date(2026, 10, 7))
    ]
    assert [r.id for c in cut[0].credits for r in c.results] == ["T-905", "T-901"]


def test_a_run_of_days_is_named_from_its_first_to_its_last() -> None:
    """Within a month, across two months, across a new year, and one day alone."""
    assert week_label(date(2026, 10, 5)) == f"5{EN_DASH}11 October 2026"
    assert week_label(date(2026, 9, 28)) == f"28 September {EN_DASH} 4 October 2026"
    assert week_label(date(2025, 12, 29)) == f"29 December 2025 {EN_DASH} 4 January 2026"
    assert span_label(date(2026, 10, 5), date(2026, 10, 7)) == f"5{EN_DASH}7 October 2026"
    assert span_label(date(2026, 10, 5), date(2026, 10, 5)) == "5 October 2026"


def test_a_long_list_of_cases_is_counted() -> None:
    """A list longer than `ADDED_CASES` characters is how many and its ends."""
    base = site_renders.overview().results[0]
    short = dataclasses.replace(
        base, record={**base.record, "scope": {"n_values": [176, 181, 270, 271, 272]}}
    )
    assert overview_sections.added_cases(short) == f"n = 176, 181, 270{EN_DASH}272"
    wide = dataclasses.replace(
        base, record={**base.record, "scope": {"n_values": list(range(1, 400, 2))}}
    )
    assert overview_sections.added_cases(wide) == "200 counts from 1 to 399"
    ranged = dataclasses.replace(
        base, record={**base.record, "scope": {"n_min": 1, "n_max": 9}}
    )
    assert overview_sections.added_cases(ranged) == f"n = 1{EN_DASH}9"


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


def test_compound_finders_use_reviewed_people_and_conflicting_joins_stay_plain() -> None:
    base = overview_data.Result(
        record={},
        group="",
        credit="Guzhou0806, Mira after Levy",
        ours=False,
        credit_html=(
            '<a href="profiles/guzhou0806.html">Guzhou0806</a>, '
            '<a href="profiles/mira.html">Mira-acc</a> after '
            '<a href="profiles/joshua-levy.html">Levy</a>'
        ),
    )
    shown = overview_sections.credit_link(
        "Guzhou0806, Mira", ("https://example.org/repo",), results=(base,)
    )
    assert "profiles/guzhou0806.html" in shown
    assert "profiles/mira.html" in shown
    assert "joshua-levy" not in shown
    assert "https://example.org/repo" not in shown
    conflicting = dataclasses.replace(base, credit_html="Guzhou0806, Mira after Levy")
    assert (
        overview_sections.credit_link(
            "Guzhou0806, Mira", ("https://example.org/repo",), results=(base, conflicting)
        )
        == "Guzhou0806, Mira"
    )


def test_unresolved_source_credit_does_not_gain_an_alias_identity_in_a_summary() -> None:
    result = overview_data.Result(
        record={}, group="", credit="Mira", ours=False, credit_html="Mira"
    )
    shown = overview_sections.credit_link(
        "Mira", ("https://example.org/work",), results=(result,)
    )
    assert 'href="https://example.org/work"' in shown
    assert ">Mira</a>" in shown
    assert "profiles/" not in shown


@pytest.mark.parametrize("quoted", [False, True])
def test_finder_html_comparison_accepts_equivalent_attribute_serialization(
    *, quoted: bool
) -> None:
    first = '<a href="profiles/francisco-couzo.html">Couzo</a>'
    second = '<a href="profiles/oscar-fitzharding.html">Fitzharding</a>'
    result = overview_data.Result(
        record={},
        group="",
        credit="Couzo, Fitzharding",
        ours=False,
        credit_html=first + ", " + second,
    )
    markup = f"<span data-contributor-plain>{first}, {second}</span>"
    if not quoted:
        markup = re.sub(r'href="([^"]+)"', r"href=\1", markup)
    _assert_finder(markup, (result,))


@pytest.mark.parametrize("mutation", ["name", "url", "duplicate", "order", "new-tab"])
def test_finder_html_comparison_rejects_changed_reviewed_credits(mutation: str) -> None:
    first = '<a href="profiles/francisco-couzo.html">Couzo</a>'
    second = '<a href="profiles/oscar-fitzharding.html">Fitzharding</a>'
    result = overview_data.Result(
        record={},
        group="",
        credit="Couzo, Fitzharding",
        ours=False,
        credit_html=first + ", " + second,
    )
    original = f"<span data-contributor-plain>{first}, {second}</span>"
    changed = {
        "name": original.replace(">Couzo<", ">Other<"),
        "url": original.replace("profiles/francisco-couzo.html", "profiles/other.html"),
        "duplicate": original.replace(first, first + first),
        "order": f"<span data-contributor-plain>{second}, {first}</span>",
        "new-tab": original.replace("<a href=", "<a target=_blank href=", 1),
    }[mutation]
    with pytest.raises(AssertionError):
        _assert_finder(changed, (result,))
