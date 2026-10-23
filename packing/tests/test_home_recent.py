"""The home page's Recently Added, read from the record at render time.

The owner, 22 October 2026: "It should be clear if you come to the site and see all the
things that have recently merged now." The section covers the newest day anything reached
`main` and the seven before it, one disclosure a day: every result that reached the site,
at any significance, by its `landed`; each count whose house best packing changed, and
each source's dated beyond-horizon rows, by the day `main` first held them
(`frontier/landings.yaml`, which `devtools.stamp_landed` writes from the merge; #736's
review A, findings A2 and A3). Every check reads the rendered page against those records,
never against a list kept beside them.
"""

from __future__ import annotations

import re
from collections import Counter
from datetime import date, timedelta

import pytest

from devtools import (
    news_highlights,
    overview_data,
    overview_sections,
    render_changelog,
    stamp_landed,
)
from devtools import render_recent_results as standing
from devtools.overview_data import EN_DASH
from devtools.overview_sections import (
    RECENT_OPEN,
    BeyondRows,
    HouseMove,
    RecentDay,
    arrival_reference,
    beyond_rows,
    house_landings,
    house_moves,
    landed_day,
    recent_tally,
    source_landings,
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


def _window(overview: overview_data.Overview) -> tuple[date, date]:
    """The section's window: the newest arrival of any kind and the seven days before."""
    until = arrival_reference(overview)
    return until - timedelta(days=overview_sections.ADDED_DAYS), until


def test_every_result_of_the_seven_days_is_listed_on_its_day_with_its_rungs(
    overview: overview_data.Overview, days: dict[str, tuple[bool, str]]
) -> None:
    since, until = _window(overview)
    expected = {r.id: r for r in overview.results if since <= landed_day(r) <= until}
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


def test_house_moves_are_listed_on_the_day_main_took_them_in(
    overview: overview_data.Overview, days: dict[str, tuple[bool, str]]
) -> None:
    """Each count whose house best packing reached `main` inside the window is listed
    once, on that day (`landings.yaml`), under the result that holds it now; that result
    is the one the adoption record names and the one the case record's verified upper
    bound rests on, as the case page says."""
    since, until = _window(overview)
    expected = {
        n: (day.isoformat(), result)
        for n, (result, day) in house_landings().items()
        if since <= day <= until
    }
    adopted, _ = stamp_landed.current_landings()
    records = standing.load_records()
    seen: dict[int, tuple[str, str]] = {}
    for day, (_, body) in days.items():
        for anchor, result_id, counts in HOUSE.findall(body):
            assert anchor == result_id.lower()
            for n in map(int, re.findall(r'href="cases/(\d+)\.html" data-case="\1"', counts)):
                assert n not in seen
                seen[n] = (day, result_id)
                assert adopted[n] == result_id
                held = standing.lane_holders(n, records, "upper", ["verified"])
                assert result_id in held, (n, result_id, held)
    assert seen == expected


def test_the_examples_review_a_cited_are_dated_by_their_merges() -> None:
    """The pass of 17 October 2026 reached `main` on the 19th (d167d4b86, f3d5da7bd), so
    its houses land on the 19th, not the day it ran; #631's rows reached `main` with
    #631's results on 16 October; #701's couzo-issue678 rows with T-223 on the 21st. Each
    holds while its house or source is the record's (#736's review A, finding A2)."""
    houses = house_landings()
    for n, result in ((29, "T-195"), (68, "T-174"), (172, "T-174")):
        if houses[n][0] == result:
            assert houses[n][1] == date(2026, 10, 19), n
    rows = source_landings()
    register = {r.id: r for r in site_renders.overview().results}
    for source, result in (
        ("couzo-verified-bounds-2026-10-14", "T-188"),
        ("couzo-certificates-2026-10-14", "T-188"),
        ("couzo-issue678-2026-10-18", "T-223"),
    ):
        assert rows[source] == landed_day(register[result]), source


def test_each_source_of_beyond_horizon_rows_in_the_window_has_one_line_on_its_day(
    overview: overview_data.Overview, days: dict[str, tuple[bool, str]]
) -> None:
    since, until = _window(overview)
    expected = {found.source["id"]: found for found in beyond_rows(since, until)}
    landed = source_landings()
    corpus = overview_sections.corpus_end()
    lines = [(day, line) for day, (_, body) in days.items() for line in ROWS.findall(body)]
    assert len(lines) == len(expected)
    by_readme = {
        overview_sections.source_readme(found.source): found for found in expected.values()
    }
    for day, (href, claims, end, span, _credit) in lines:
        found = by_readme[href.replace("&amp;", "&")]
        counts = [int(row["n"]) for row in found.rows]
        assert day == found.day.isoformat() == landed[found.source["id"]].isoformat()
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


def test_one_window_bounds_every_kind_and_the_introduction_names_what_is_shown(
    overview: overview_data.Overview, section: str, days: dict[str, tuple[bool, str]]
) -> None:
    """Results, houses and rows share one window, from seven days before the newest
    arrival of any kind to it, read from the record and never the clock; the
    introduction's span runs from the oldest day shown to the newest, so no block sits
    outside it (#736's review A, finding A3)."""
    since, until = _window(overview)
    shown = sorted(date.fromisoformat(day) for day in days)
    assert shown
    assert since <= shown[0]
    assert shown[-1] == until
    assert f"over {overview_sections.span_label(shown[0], shown[-1])}," in section
    assert overview_sections.recent_span(overview) == overview_sections.span_label(
        shown[0], shown[-1]
    )
    # Bounded at both ends: a move or a source outside the window is left out.
    early = until - timedelta(days=1)
    assert all(move.day <= early for move in house_moves(since, early))
    assert all(found.day <= early for found in beyond_rows(since, early))
    assert overview_sections.record_reference() == until


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


def test_house_moves_list_each_count_once_under_its_house() -> None:
    moves = house_moves(date(2026, 10, 1), date(2027, 1, 1))
    counts = [n for move in moves for n in move.counts]
    assert len(counts) == len(set(counts))
    houses = house_landings()
    for move in moves:
        for n in move.counts:
            assert houses[n] == (move.result, move.day)


def test_the_section_links_the_seven_days_and_news(section: str) -> None:
    assert 'href="results.html#added-in-the-last-seven-days"' in section
    assert 'href="news.html"' in section
    results = site_renders.html("results.html")
    assert 'id="added-in-the-last-seven-days"' in results


def test_the_home_page_additions_stay_brief(section: str) -> None:
    news = news_highlights.render(render_changelog.load())
    weight, box = len(section.encode("utf-8")), len(news.encode("utf-8"))
    print(
        f"recently added: {weight:,} / {RECENT_BYTES:,}; news box: {box:,} / {NEWS_BOX_BYTES:,}"
    )
    assert weight < RECENT_BYTES
    assert box < NEWS_BOX_BYTES
