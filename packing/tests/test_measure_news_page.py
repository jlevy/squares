"""The News page measuring tool's arithmetic and its projection, with no browser.

`devtools.measure_news_page` is what a raise of `news.html`'s byte budget is set on
(`think-3oxz`), so its `bytes` figures and its projected page are held here on fixture
pages built from the renderer's own card writer, and its card reading on the page the
site renders.
"""

from __future__ import annotations

import collections
import gzip
import json
import re
from contextlib import nullcontext
from datetime import date
from pathlib import Path
from typing import Any
from unittest.mock import Mock

import brotli
import pytest

from devtools import check_site_rendering, preview_site, render_changelog, site_urls
from devtools import measure_news_page as news
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
    assert "brotli_withheld" not in report


def test_a_projected_page_reports_gzip_and_withholds_brotli() -> None:
    # Brotli's window reaches across a projection's repeated cards, so its size there
    # measures the repetition; gzip's 32 KB window does not, so its size stands.
    grown = news.project_page(fixture(), 100_000).page
    assert news.projected(grown)
    assert not news.projected(fixture())
    report = news.byte_report(grown, name="grown", as_of=date(2026, 10, 24), limits=LIMITS)
    assert report["gzip_bytes"] == len(gzip.compress(grown.encode(), compresslevel=6, mtime=0))
    assert report["brotli_bytes"] is None
    assert "repeated cards" in report["brotli_withheld"]


def test_the_90th_percentile_story_is_by_nearest_rank() -> None:
    # Nearest rank: the smallest size at or above 90% of them, the 45th of 50 and the
    # 9th of 10, not the next one up.
    assert news.nearest_rank(range(1, 51), 0.9) == 45
    assert news.nearest_rank([10, 9, 8, 7, 6, 5, 4, 3, 2, 1], 0.9) == 9
    assert news.nearest_rank([7], 0.9) == 7
    with pytest.raises(ValueError, match="no size"):
        news.nearest_rank([], 0.9)


def test_the_days_of_room_follow_from_the_last_28_days_pace() -> None:
    text = fixture()
    size = len(text.encode())
    found = {item.day.isoformat(): item.bytes for item in news.cards(text)}
    # The 28 days ending on 24 October start on 27 September: the first story of
    # September is outside them, and the other three set the pace.
    pace = (found["2026-10-20"] + found["2026-10-12"] + found["2026-10-01"]) / 28
    room = news.room(text, as_of=date(2026, 10, 24), limits=LIMITS)
    assert (room.stories, room.pace_days, room.pace_stories) == (4, 28, 3)
    assert room.earliest == date(2026, 10, 1)
    assert room.bytes_per_day == pytest.approx(pace)
    assert room.days_to_trip == pytest.approx((40_000 - size) / pace)
    assert room.days_to_budget == pytest.approx((60_000 - size) / pace)
    line = news.room_line(text, as_of=date(2026, 10, 24), limits=LIMITS)
    assert line.startswith(f"{size:,} bytes over 4 stories; trip point 40,000, budget 60,000;")
    assert f"about {(40_000 - size) / pace:.0f} days of room before the trip point" in line
    assert "(3 stories, the earliest dated 2026-10-01," in line
    # A shorter window reads the pace of the stories inside it alone, over its own days:
    # the 14 days ending on 24 October start on 11 October.
    recent = (found["2026-10-20"] + found["2026-10-12"]) / 14
    short = news.room(text, as_of=date(2026, 10, 24), limits=LIMITS, pace_days=14)
    assert (short.pace_days, short.pace_stories, short.earliest) == (14, 2, date(2026, 10, 12))
    assert short.bytes_per_day == pytest.approx(recent)
    assert short.days_to_budget == pytest.approx((60_000 - size) / recent)
    report = news.byte_report(
        text, name="fixture", as_of=date(2026, 10, 24), limits=LIMITS, pace_days=14
    )
    assert (report["pace_days"], report["pace_earliest_story"]) == (14, "2026-10-12")
    with pytest.raises(ValueError, match="at least one day"):
        news.room(text, as_of=date(2026, 10, 24), limits=LIMITS, pace_days=0)
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


def test_a_control_leaves_out_one_named_script_and_nothing_else() -> None:
    scripts = (
        '<script src="assets/js/news-cards.a05a2d7bcb2a122b.js"></script>\n'
        '<script src="assets/js/filter-menu.4ff10cd5ef7ce93a.js"></script>\n'
        '<script src="assets/js/news-filters.80875a7f24c0dc24.js"></script>\n'
    )
    text = fixture().replace(SHELL_TAIL, scripts + SHELL_TAIL)
    assert news.without_scripts(text, []) == text
    control = news.without_scripts(text, ["news-cards.js"])
    assert control == text.replace(scripts.splitlines(keepends=True)[0], "")
    both = news.without_scripts(text, ["news-cards.js", "news-filters.js"])
    assert re.findall(r"assets/js/([a-z-]+)\.", both) == ["filter-menu"]
    # A script the page does not name, or names twice, is refused rather than skipped.
    with pytest.raises(ValueError, match=r"0 elements for the script news-views\.js"):
        news.without_scripts(text, ["news-views.js"])
    with pytest.raises(ValueError, match="2 elements"):
        news.without_scripts(text + scripts, ["news-cards.js"])


def test_the_control_is_built_from_the_page_the_site_renders(rendered: str) -> None:
    for script in ("news-cards.js", "news-filters.js"):
        control = news.without_scripts(rendered, [script])
        assert script.removesuffix(".js") + "." not in control
        assert len(news.cards(control)) == len(news.cards(rendered))


class _Server:
    server_port = 0

    def shutdown(self) -> None:
        pass

    def server_close(self) -> None:
        pass


def checker_report(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    samples: dict[tuple[int, str, bool], dict[str, Any]],
) -> dict[str, Any]:
    """`check_site_rendering`'s own report on `news.html`, its browser and server
    stubbed and each scenario's sample given, so the verdict reads the checker's real
    failure text rather than a copy of it that could drift."""
    (tmp_path / news.PAGE).write_text("<main>News</main>", encoding="utf-8")
    passing = {
        "heading": "News",
        "contentChars": 400,
        "supported": True,
        "cls": 0.0,
        "lcpMs": 400,
        "longestTaskMs": 120,
        "blockingMs": 40,
        "unreadableMath": 0,
        "errors": [],
    }

    def measure(_browser: object, _url: str, **options: Any) -> dict[str, Any]:
        key = (options["width"], options["scheme"], options.get("javascript", True))
        return passing | samples.get(key, {})

    monkeypatch.setattr("playwright.sync_api.sync_playwright", lambda: nullcontext(Mock()))
    monkeypatch.setattr(preview_site, "launch_chromium", lambda _driver: Mock())
    monkeypatch.setattr(preview_site, "serve", lambda *_args, **_options: _Server())
    monkeypatch.setattr(check_site_rendering, "measure", measure)
    capsys.readouterr()
    check_site_rendering.main([str(tmp_path), "--page", news.PAGE, "--runs", "3"])
    return json.loads(capsys.readouterr().out)


def test_the_verdict_is_the_four_limits_on_the_medians_and_the_no_js_page(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    def report(samples: dict[tuple[int, str, bool], dict[str, Any]]) -> dict[str, Any]:
        return checker_report(monkeypatch, tmp_path, capsys, samples)

    # Formulas hidden with scripts on are listed and do not decide the verdict.
    hidden = report({(1280, "light", True): {"unreadableMath": 3}})
    found = news.verdict(hidden)
    assert found["passes"]
    assert found["other_findings"] == ["news.html 1280px light: visual mathematics missing"]
    assert found["limit_failures"] == found["no_js_failures"] == found["run_failures"] == []
    # Each limit, read on the median, decides it, and so does an unreadable page
    # without scripts.
    failing = report(
        {
            (390, "dark", True): {"cls": 0.4, "longestTaskMs": 310},
            (1280, "dark", False): {"heading": None},
        }
    )
    found = news.verdict(failing)
    assert not found["passes"]
    assert found["limit_failures"] == [
        "news.html 390px dark: cls 0.400 exceeds 0.1",
        "news.html 390px dark: longestTaskMs 310.000 exceeds 300",
    ]
    assert found["no_js_failures"] == [
        "news.html no-JS 1280px dark: primary heading/prose missing"
    ]
    assert found["worst_medians"] == {
        "cls": 0.4,
        "lcpMs": 400,
        "longestTaskMs": 310,
        "blockingMs": 40,
    }


@pytest.mark.parametrize(
    ("sample", "problem"),
    [
        ({"supported": False, "lcpMs": 0}, "required native load timing is unavailable"),
        (
            {"errors": ["HTTP 404: assets/js/news-cards.js"]},
            "HTTP 404: assets/js/news-cards.js",
        ),
        ({"errors": ["TypeError: card is null"]}, "TypeError: card is null"),
    ],
)
def test_a_run_that_was_not_timed_or_raised_an_error_fails_the_verdict(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    sample: dict[str, Any],
    problem: str,
) -> None:
    # Every limit is within bounds on the medians, but one scenario's runs were not all
    # measured, so the limits were not, and the verdict does not pass.
    found = news.verdict(
        checker_report(monkeypatch, tmp_path, capsys, {(390, "light", True): sample})
    )
    assert not found["passes"]
    assert found["limit_failures"] == found["no_js_failures"] == []
    assert found["run_failures"] == [f"news.html 390px light: {problem}"]


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
