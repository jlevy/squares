"""The News page measuring tool's arithmetic and its projection, with no browser.

`devtools.measure_news_page` is what a raise of `news.html`'s byte budget is set on
(`think-3oxz`), so its `bytes` figures and its projected page are held here on fixture
pages built from the renderer's own card writer, and its card reading on the page the
site renders.
"""

from __future__ import annotations

import collections
import gzip
import re
from datetime import date
from pathlib import Path

import brotli
import pytest

from devtools import measure_news_page as news
from devtools import render_changelog, site_urls
from tests import site_renders

SHELL_HEAD = (
    "<!doctype html><html><head><title>News</title></head><body><main><article>"
    '<h1 id="news">News</h1><div class="site-news" data-news data-contributor-plain>\n'
)
SHELL_TAIL = "</div></article></main></body></html>\n"
LIMITS = news.Limits(budget=60_000, trip=40_000)


def card(identifier: str, day: str, words: int, *, score: int = 4) -> str:
    """One card as `render_changelog.render_news` writes it, `words` long."""
    anchor = render_changelog.entry_anchor(identifier)
    body = (
        f'<div id="changelog-date-{day}"></div>'
        f'<article class="site-news-item" data-news-entry="{identifier}">'
        f'<h2 id="{anchor}-title">{identifier}</h2><p>{"word " * words}</p>'
        f'<a href="#{anchor}">This story</a></article>'
    )
    text = render_changelog.news_card(anchor, day, body).replace(
        "data-news-day=",
        f'data-news-score="{score}" data-news-topics="project" data-news-day=',
        1,
    )
    if score < 4:
        text = text.replace(
            '<section class="site-news-day"', '<section hidden class="site-news-day"', 1
        )
    return text


def page(*cards: str) -> str:
    return SHELL_HEAD + "\n".join(cards) + "\n" + SHELL_TAIL


def fixture() -> str:
    return page(
        card("newest", "2026-10-20", 400),
        card("routine", "2026-10-12", 150, score=3),
        card("older", "2026-10-01", 900, score=5),
        card("before-the-window", "2026-09-01", 2_000),
    )


def test_bytes_reports_the_sizes_the_compressors_give_and_the_shares() -> None:
    text = fixture()
    data = text.encode()
    report = news.byte_report(text, name="fixture", as_of=date(2026, 10, 24), limits=LIMITS)
    assert report["raw_bytes"] == len(data)
    assert report["gzip_bytes"] == len(gzip.compress(data, compresslevel=6, mtime=0))
    assert report["brotli_bytes"] == len(brotli.compress(data, quality=11))
    sizes = sorted(found.bytes for found in news.cards(text))
    assert report["stories"] == 4
    assert report["story_bytes"] == sum(sizes)
    assert report["row_bytes"] == 0
    assert report["shell_bytes"] == len(data) - sum(sizes)
    assert report["story_p90_bytes"] == sizes[3]
    assert (report["trip_bytes"], report["budget_bytes"]) == (40_000, 60_000)


def test_the_days_of_room_follow_from_the_last_28_days_pace() -> None:
    text = fixture()
    size = len(text.encode())
    found = {item.day.isoformat(): item.bytes for item in news.cards(text)}
    # The 28 days ending on 24 October start on 27 September: the first story of
    # September is outside them, and the other three set the pace.
    pace = (found["2026-10-20"] + found["2026-10-12"] + found["2026-10-01"]) / 28
    room = news.room(text, as_of=date(2026, 10, 24), limits=LIMITS)
    assert (room.stories, room.pace_stories) == (4, 3)
    assert room.bytes_per_day == pytest.approx(pace)
    assert room.days_to_trip == pytest.approx((40_000 - size) / pace)
    assert room.days_to_budget == pytest.approx((60_000 - size) / pace)
    line = news.room_line(text, as_of=date(2026, 10, 24), limits=LIMITS)
    assert line.startswith(f"{size:,} bytes over 4 stories; trip point 40,000, budget 60,000;")
    assert f"about {(40_000 - size) / pace:.0f} days of room before the trip point" in line
    # A page at or past a limit has no room left before it.
    full = news.room(text, as_of=date(2026, 10, 24), limits=news.Limits(size, size))
    assert (full.days_to_trip, full.days_to_budget) == (0.0, 0.0)
    # With no story in the window there is no pace, and no count of days.
    quiet = news.room(text, as_of=date(2027, 1, 1), limits=LIMITS)
    assert (quiet.pace_stories, quiet.days_to_trip) == (0, None)
    assert "no pace to project" in news.room_line(text, as_of=date(2027, 1, 1), limits=LIMITS)


def test_the_room_is_read_against_the_registered_budget() -> None:
    [row] = [row for row in site_urls.load_registry() if row.path == news.PAGE]
    budget = site_urls.page_budget(row)
    assert news.registered_limits() == news.Limits(budget, budget - news.TRIP_MARGIN)
    assert news.TRIP_MARGIN == 150_000


@pytest.mark.parametrize("target", [30_000, 47_123, 100_000])
def test_project_reaches_its_target_within_one_story_from_the_pages_own_cards(
    target: int,
) -> None:
    text = fixture()
    original = news.cards(text)
    projection = news.project_page(text, target)
    grown = projection.page
    size = len(grown.encode())
    # It reaches the target and passes it by less than one story.
    assert target <= size < target + max(item.bytes for item in original)
    found = news.cards(grown)
    assert len(found) == len(original) + projection.stories_added
    # The page's own cards and nothing else: each copy, its ids' suffix taken off, is
    # one of the page's cards, and they repeat in the page's order, ahead of the first.
    bodies = [grown[item.start : item.end] for item in found]
    sources = [text[item.start : item.end] for item in original]
    plain = [re.sub(r"--projected-\d+", "", body) for body in bodies]
    added = projection.stories_added
    assert plain[:added] == [sources[index % len(sources)] for index in range(added)]
    assert bodies[added:] == sources
    assert grown.startswith(text[: original[0].start])
    assert grown.endswith(text[original[-1].end :])
    # Every id and anchor is unique, and every reference names an id on the page.
    ids = re.findall(r'\sid="([^"]+)"', grown)
    assert [name for name, count in collections.Counter(ids).items() if count > 1] == []
    entries = re.findall(r'data-news-entry="([^"]+)"', grown)
    assert len(entries) == len(set(entries)) == len(found)
    references = re.findall(r'(?:aria-controls="|href="#)([^"]+)"', grown)
    assert references
    assert set(references) <= set(ids)


def test_a_page_already_at_its_target_is_projected_unchanged() -> None:
    text = fixture()
    assert news.project_page(text, len(text.encode())) == (text, 0, 0)
    assert news.project_page(text, 0) == (text, 0, 0)
    with pytest.raises(ValueError, match="no News card"):
        news.project_page(SHELL_HEAD + SHELL_TAIL, 100_000)


def test_project_writes_a_directory_of_its_own(tmp_path: Path) -> None:
    (tmp_path / "index.html").write_text("another build's", encoding="utf-8")
    with pytest.raises(ValueError, match="is not empty"):
        news.write_projection(fixture(), tmp_path)


def test_the_verdict_is_the_four_limits_on_the_medians_and_the_no_js_page() -> None:
    def scenario(width: int, scheme: str, cls: float, task: float) -> dict:
        return {
            "width": width,
            "scheme": scheme,
            "cls": cls,
            "lcpMs": 400,
            "longestTaskMs": task,
            "blockingMs": 100,
        }

    report = {
        "pages": [scenario(1280, "light", 0.02, 120), scenario(390, "dark", 0.4, 310)],
        "failures": [
            "news.html 1280px light: visual mathematics missing",
            "news.html 390px dark: cls 0.400 exceeds 0.1",
            "news.html 390px dark: longestTaskMs 310.000 exceeds 300",
        ],
    }
    found = news.verdict(report)
    assert not found["passes"]
    assert found["limit_failures"] == report["failures"][1:]
    assert found["other_findings"] == report["failures"][:1]
    assert found["worst_medians"] == {
        "cls": 0.4,
        "lcpMs": 400,
        "longestTaskMs": 310,
        "blockingMs": 100,
    }
    # A finding outside the limits is listed and does not decide the verdict; an
    # unreadable page without scripts does.
    assert news.verdict(report | {"failures": report["failures"][:1]})["passes"]
    unreadable = ["news.html no-JS 390px dark: primary heading/prose missing"]
    assert not news.verdict(report | {"failures": unreadable})["passes"]


@pytest.fixture(scope="module")
def rendered() -> str:
    return site_renders.html(news.PAGE)


def test_the_tool_reads_one_card_for_each_story_the_site_renders(rendered: str) -> None:
    shown = render_changelog.news_entries(render_changelog.load())
    found = news.cards(rendered)
    first_ids = [
        re.findall(r'\sid="([^"]+)"', rendered[item.start : item.end])[0] for item in found
    ]
    assert first_ids == [render_changelog.entry_anchor(entry["id"]) for entry in shown]
    assert [item.day.isoformat() for item in found] == [entry["date"] for entry in shown]
    assert news.row_bytes(rendered) == 0
