"""The home page's Recently Added, read from the record at render time.

The owner, 22 October 2026: "It should be clear if you come to the site and see all the
things that have recently merged now." The section covers the days the results page's
"Added in the Last Seven Days" covers, one disclosure a day: every result that reached
the site, at any significance; each count whose house best packing an adoption pass
moved (`upper_bound_houses`); and the dated beyond-horizon rows the coverage register
recorded (`source-coverage.yaml`). Every check reads the rendered page against those
records, never against a list kept beside them.
"""

from __future__ import annotations

import re
from collections import Counter
from datetime import date

import pytest

from devtools import news_highlights, overview_data, overview_sections, render_changelog
from devtools import render_recent_results as standing
from devtools import upper_bound_houses as houses
from devtools.overview_data import EN_DASH
from devtools.overview_sections import (
    RECENT_OPEN,
    BeyondRows,
    HouseMove,
    RecentDay,
    added_since,
    beyond_rows,
    house_moves,
    landed_day,
    recent_tally,
)
from tests import site_renders

#: One day's disclosure: its date, whether it starts open, the rest.
DAY = re.compile(r'<details data-day="(\d{4}-\d{2}-\d{2})"( open)?>(.*?)</details>', re.DOTALL)
#: One result in a day, as the results page's seven days write it, linked to its row
#: there: its id, its V, C and S rungs.
ENTRY = re.compile(
    r'<li(?: class="site-rollup-superseded")?><a href="results\.html#(t-\d{3})"'
    r'(?: title="Superseded")?>(T-\d{3})</a> .*?<small>[^<]* · (V\d) (C\d) (?:<b>)?(S\d)'
)
#: One house move: the result and the rest of the line, its counts' case links.
HOUSE = re.compile(
    r'<li><a href="results\.html#(t-\d{3})">(T-\d{3})</a> is now the house best packing at '
    r"(.*?)</li>"
)
#: One source's rows: the packet's address, the claims, the counts' span and the credit.
ROWS = re.compile(
    r'<li><a href="([^"]+)" target="_blank" rel="noopener noreferrer">([^<]+)</a> '
    rf"beyond n = (\d+)<small>n = ([0-9{EN_DASH}]+) · (.*?)</small></li>"
)
#: The most bytes the section may weigh. On 22 October 2026, over 15-22 October, it
#: measured 23,651 bytes: 45 results, 61 counts' house best packings on seven days and 11
#: sources' 876 rows. The results page's seven days have held 71 results, about 22,000
#: bytes alone. Past this the section is becoming a second results table; the remedy is a
#: shorter entry, not a higher number.
RECENT_BYTES = 40_000
#: The most bytes the News box may weigh: the newest three News articles of each level,
#: nine cards of 3 to 6 KB, measured at 42,550 bytes on 22 October 2026.
NEWS_BOX_BYTES = 64_000


@pytest.fixture(scope="module")
def home() -> str:
    return site_renders.html("index.html")


@pytest.fixture(scope="module")
def overview() -> overview_data.Overview:
    return site_renders.overview()


@pytest.fixture(scope="module")
def section(home: str) -> str:
    """The section, from its heading to the end of its last disclosure."""
    begin = home.index('id="recently-added"')
    end = home.index("</details></div>", begin) + len("</details></div>")
    return home[begin:end]


@pytest.fixture(scope="module")
def days(section: str) -> dict[str, tuple[bool, str]]:
    return {day: (bool(state), body) for day, state, body in DAY.findall(section)}


def test_every_result_of_the_seven_days_is_listed_on_its_day_with_its_rungs(
    overview: overview_data.Overview, days: dict[str, tuple[bool, str]]
) -> None:
    since = added_since(overview)
    expected = {r.id: r for r in overview.results if landed_day(r) >= since}
    assert expected, "the newest arrival is always inside its own seven days"
    seen: Counter[str] = Counter()
    for day, (_, body) in days.items():
        for anchor, result_id, verification, confirmation, score in ENTRY.findall(body):
            result = expected[result_id]
            assert anchor == result_id.lower()
            assert landed_day(result).isoformat() == day
            assert verification == result.record["verification"]
            assert confirmation == result.record["confirmation"]
            assert score == f"S{overview_sections.significance(result)}"
            seen[result_id] += 1
    assert seen == Counter(set(expected))


def test_house_moves_follow_the_adoption_record_and_the_case_records(
    overview: overview_data.Overview, days: dict[str, tuple[bool, str]]
) -> None:
    """Each count an adoption pass moved inside the seven days is listed once, on the
    pass's day, under the result that holds it now; and that result is the one the
    case record's verified upper bound rests on, as the case page says."""
    since = added_since(overview)
    expected = {
        n: (houses.adopted_on(n), houses.ADOPTED[n])
        for n in houses.NUMBERS
        if date.fromisoformat(houses.adopted_on(n)) >= since
    }
    records = standing.load_records()
    seen: dict[int, tuple[str, str]] = {}
    for day, (_, body) in days.items():
        for anchor, result_id, counts in HOUSE.findall(body):
            assert anchor == result_id.lower()
            for n in map(int, re.findall(r'href="cases/(\d+)\.html" data-case="\1"', counts)):
                assert n not in seen
                seen[n] = (day, result_id)
                held = standing.lane_holders(n, records, "upper", ["verified"])
                assert result_id in held, (n, result_id, held)
    assert seen == expected


def test_each_recent_source_of_beyond_horizon_rows_has_one_line_on_its_day(
    overview: overview_data.Overview, days: dict[str, tuple[bool, str]]
) -> None:
    since = added_since(overview)
    expected = {found.source["id"]: found for found in beyond_rows(since)}
    corpus = overview_sections.corpus_end()
    lines = [(day, line) for day, (_, body) in days.items() for line in ROWS.findall(body)]
    assert len(lines) == len(expected)
    by_readme = {
        overview_sections.source_readme(found.source): found for found in expected.values()
    }
    for day, (href, claims, end, span, _credit) in lines:
        found = by_readme[href.replace("&amp;", "&")]
        counts = [int(row["n"]) for row in found.rows]
        assert day == found.day.isoformat()
        assert int(end) == corpus
        assert claims == overview_sections.claims_phrase(found.rows)
        assert span == f"{min(counts)}{EN_DASH}{max(counts)}" or span == str(counts[0])
        # The packet's README where the register names it, else the packet itself.
        assert re.fullmatch(
            rf"https://github\.com/jlevy/squares/(blob/main/packing/.*/README\.md|"
            rf"tree/main/packing/{re.escape(str(found.source['local']).rstrip('/'))})",
            href,
        ), href
        assert all(int(row["n"]) > corpus for row in found.rows)


def test_the_newest_day_starts_open_and_each_day_tallies_what_it_holds(
    overview: overview_data.Overview, days: dict[str, tuple[bool, str]]
) -> None:
    ordered = list(days)
    assert ordered == sorted(ordered, reverse=True)
    assert [opened for opened, _ in days.values()] == [
        index < RECENT_OPEN for index in range(len(days))
    ]
    for recent in overview_sections.recent_days(overview):
        _, body = days[recent.day.isoformat()]
        counts = " ".join(
            f'<span class="site-rollup-count">· {part}</span>' for part in recent_tally(recent)
        )
        assert f"{counts}</span></summary>" in body


def test_a_tally_counts_results_house_best_packings_and_rows_where_a_day_has_them() -> None:
    day = date(2026, 10, 22)
    move = HouseMove(day, "T-225", (204, 227, 229, 260))
    rows = BeyondRows(day, {"id": "s"}, tuple({"n": 330 + i} for i in range(111)))
    corpus = overview_sections.corpus_end()
    assert recent_tally(RecentDay(day, (), (move,), (rows,))) == (
        "4 house best packings",
        f"111 bounds beyond {corpus}",
    )
    assert recent_tally(RecentDay(day, (), (HouseMove(day, "T-1", (5,)),), ())) == (
        "1 house best packing",
    )


def test_house_moves_list_each_count_on_its_last_pass_alone() -> None:
    moves = house_moves(date(2026, 10, 1))
    counts = [n for move in moves for n in move.counts]
    assert len(counts) == len(set(counts))
    for move in moves:
        for n in move.counts:
            assert houses.adopted_on(n) == move.day.isoformat()
            assert houses.ADOPTED[n] == move.result


def test_the_section_links_the_seven_days_and_news(
    section: str, overview: overview_data.Overview
) -> None:
    assert 'href="results.html#added-in-the-last-seven-days"' in section
    assert 'href="news.html"' in section
    results = site_renders.html("results.html")
    assert 'id="added-in-the-last-seven-days"' in results
    span = overview_sections.span_label(
        overview_sections.added_since(overview), overview_sections.added_reference(overview)
    )
    assert span in section


def test_the_home_page_additions_stay_brief(section: str) -> None:
    news = news_highlights.render(render_changelog.load())
    weight, box = len(section.encode("utf-8")), len(news.encode("utf-8"))
    print(
        f"recently added: {weight:,} / {RECENT_BYTES:,}; news box: {box:,} / {NEWS_BOX_BYTES:,}"
    )
    assert weight < RECENT_BYTES
    assert box < NEWS_BOX_BYTES
