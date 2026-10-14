"""The homepage's bounded previews, shared expansion and card geometry in Chromium.

Real rendered pages and their assets are served through request routes in memory, so
the fixture writes no site output. One desktop and one mobile session exercise the
keyboard, canonical Atlas tiles, shared triangle animation and a case link.
"""

from __future__ import annotations

import mimetypes
import os
import re
from collections.abc import Iterator
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlsplit

import pytest

from devtools import (
    news_highlights,
    overview_sections,
    render_changelog,
    render_overview,
    site_assets,
)
from devtools.render_n11_lower_bounds_explainer import COMPOSITE_ASSETS
from sqpack.probes import probe
from tests import site_browser, site_renders

PROBES = Path(__file__).with_name("probes")
STATE = probe(PROBES, "site_homepage/state")
GEOMETRY = probe(PROBES, "site_homepage/geometry")
MEDIA_IMAGES = probe(PROBES, "site_homepage/media_images")
THEME = probe(PROBES, "site_homepage/theme")
FILM = probe(PROBES, "site_homepage/film")
TRANSITION = probe(PROBES, "site_homepage/transition")
INITIAL_LAYOUT = probe(PROBES, "site_atlas_views/initial")
HERO = probe(PROBES, "site_homepage/hero")
DOWNLOAD_ACTION = probe(PROBES, "site_homepage/download_action")
NEWS = probe(PROBES, "site_homepage/news")
NEWS_SETTLED = probe(PROBES, "site_homepage/news-settled")
NEWS_FILTERS = probe(PROBES, "site_homepage/news-filters")
ORIGIN = "http://homepage.test/"
TOGGLE = "[data-homepage-atlas-toggle]"
CELLS = "#homepage-atlas-cells"
TILES = f"{CELLS} .site-atlas-cell:visible"
GRAPHIC = "known-best-1-324.svg"
STATUS = "[data-homepage-atlas-status]"
EXPLORE = '.site-homepage-atlas-actions a[href="atlas.html"]'
WIDTHS = (1280, 390)
NAV_WIDTHS = (*WIDTHS, 320)


@pytest.fixture(scope="module")
def payloads() -> dict[str, bytes]:
    """The real destination pages and exercised cases, with every browser dependency."""
    documents = {
        name: site_renders.html(name)
        for name in ("index.html", "news.html", "atlas.html", "about.html", "results.html")
    }
    documents.update(
        {
            f"cases/{n}.html": site_renders.case_records((18, 36, 53, 291, 306, 324))[
                f"cases/{n}.html"
            ]
            for n in (18, 36, 53, 291, 306, 324)
        }
    )
    assets = site_assets.shared().assets.referenced(documents.values())
    media = {hero for _, hero, *_ in overview_sections.ATLAS_CARDS}
    return {
        **{name: html.encode("utf-8") for name, html in documents.items()},
        **{f"assets/{name}": data for name, data in assets.items()},
        **render_overview.support_files(),
        **{path.name: path.read_bytes() for path in COMPOSITE_ASSETS if path.name in media},
    }


@pytest.fixture(scope="module")
def browser() -> Iterator[Any]:
    with site_browser.api().sync_playwright() as driver:
        launched = site_browser.launch(driver)
        yield launched
        launched.close()


def _serve(page: Any, payloads: dict[str, bytes]) -> None:
    """Fulfill this page's own site requests from prepared renderer output."""

    def answer(route: Any) -> None:
        path = urlsplit(route.request.url).path.lstrip("/") or "index.html"
        body = payloads.get(path)
        if body is None:
            route.fulfill(status=404, body="Missing fixture file")
            return
        content_type = mimetypes.guess_type(path)[0] or "application/octet-stream"
        route.fulfill(body=body, content_type=content_type)

    page.route(f"{ORIGIN}**", answer)


def _requests(page: Any) -> list[str]:
    requests: list[str] = []
    page.on("request", lambda request: requests.append(request.url))
    return requests


@pytest.fixture(scope="module")
def film_payloads() -> dict[str, bytes]:
    """Only the homepage and local poster assets, without rendering the case records."""
    html = site_renders.html("index.html")
    files = site_assets.shared().assets.referenced([html])
    posters = {hero for _, hero, *_ in overview_sections.ATLAS_CARDS}
    return {
        "index.html": html.encode("utf-8"),
        **{f"assets/{name}": data for name, data in files.items()},
        **render_overview.support_files(),
        **{path.name: path.read_bytes() for path in COMPOSITE_ASSETS if path.name in posters},
    }


@pytest.mark.parametrize("width", WIDTHS)
def test_native_homepage_film_waits_for_click_and_main_headings_share_spacing(
    browser: Any, request: pytest.FixtureRequest, width: int
) -> None:
    requests = []
    page = browser.new_page(viewport={"width": width, "height": 900})
    live = os.environ.get("SQPACK_SITE_PREVIEW_URL")
    origin = f"{live.rstrip('/')}/" if live else ORIGIN
    if not live:
        _serve(page, request.getfixturevalue("film_payloads"))

    def intercept(route: Any) -> None:
        requests.append(route.request.url)
        route.abort()

    page.route(render_overview.FILM_URL, intercept)
    try:
        page.goto(f"{origin}index.html", wait_until="load")
        film = page.locator(".site-homepage-film video")
        film.scroll_into_view_if_needed()
        state = page.evaluate(FILM)
        assert requests == [], "preload=none must wait for the reader"
        assert state["controls"]
        assert state["inline"]
        assert state["preload"] == "none"
        assert not state["autoplay"]
        assert not state["marked_autoplay"]
        assert state["paused"]
        assert state["play_icon"]["content"] == '""'
        assert state["play_icon"]["width"] > 0
        assert state["play_icon"]["half_height"] > 0
        assert state["play_icon"]["color"] != "rgba(0, 0, 0, 0)"
        assert not state["play_icon"]["text"]
        assert state["ready"] == state["time"] == 0
        assert state["source"] == render_overview.FILM_URL
        assert state["poster"] == "ascent-n1-324-poster.png"
        assert state["label"]
        assert state["codec"] == "probably"
        assert abs(state["center_offset"]) <= 1
        assert state["width"] <= state["max_width"] + 1
        assert state["left"] >= 0
        assert state["right"] <= width
        assert state["overflow"] <= 0
        assert state["width"] / state["height"] == pytest.approx(16 / 9, abs=0.01)
        assert len(state["headings"]) == 9
        for heading in state["headings"]:
            assert heading["above"] == pytest.approx(state["title_above"], abs=0.01)
            assert heading["below"] == pytest.approx(state["title_below"], abs=0.01)
        overlay = page.get_by_role("button", name="Play video", exact=True)
        with page.expect_request(render_overview.FILM_URL, timeout=5000):
            overlay.click()
        assert requests == [render_overview.FILM_URL]
        state = page.evaluate(FILM, {"mockPlayback": True})
        assert state["overlay_visible"]
        button_box = overlay.bounding_box()
        video_box = film.bounding_box()
        assert button_box is not None
        assert video_box is not None
        assert (
            video_box["y"] + video_box["height"] - button_box["y"] - button_box["height"] >= 47
        )
        overlay.click(position={"x": 24, "y": 24})
        state = page.evaluate(FILM)
        assert state["mock_play_calls"] == 1
        assert not state["paused"]
        assert not state["overlay_visible"]
        assert page.evaluate(FILM, {"mediaEvent": "pause"})["overlay_visible"]
        overlay.focus()
        page.keyboard.press("Enter")
        state = page.evaluate(FILM)
        assert state["mock_play_calls"] == 2
        assert not state["overlay_visible"]
        assert page.evaluate(FILM, {"mediaEvent": "ended"})["overlay_visible"]
        overlay.focus()
        page.keyboard.press("Space")
        state = page.evaluate(FILM)
        assert state["mock_play_calls"] == 3
        assert not state["overlay_visible"]
        assert page.evaluate(FILM, {"mediaEvent": "pause"})["overlay_visible"]
        assert requests == [render_overview.FILM_URL], "mocked controls must not download media"
    finally:
        page.close()


def _pointer_cases(page: Any, cases: tuple[int, ...]) -> list[dict[str, Any]]:
    """Click the native graphic's last-column links after scrolling them into view."""
    readings = []
    for n in cases:
        link = page.locator(f'{TILES}[data-case="{n}"]')
        link.scroll_into_view_if_needed()
        reading = page.evaluate(GEOMETRY, n)
        link.click()
        article = page.locator(f'#pop-case article.site-case[data-case="{n}"]')
        article.wait_for(state="visible")
        reading["opened"] = article.get_attribute("data-case")
        page.keyboard.press("Escape")
        readings.append(reading)
    return readings


def _themes(page: Any) -> list[dict[str, Any]]:
    """Switch the actual theme controls and OS scheme through all three SVG states."""
    sync_api = site_browser.api()
    readings = []
    for phase, count in (("preview", 100), ("expanded", 324), ("collapsed", 100)):
        while page.locator(TILES).count() != count:
            page.locator(TOGGLE).click()
            page.evaluate(TRANSITION, {"install": False, "settle": True})
        sync_api.expect(page.locator(TILES)).to_have_count(count)
        for mode, scheme in (
            ("system", "light"),
            ("system", "dark"),
            ("light", "dark"),
            ("dark", "light"),
        ):
            page.emulate_media(color_scheme=scheme)
            page.evaluate(THEME, {"scroll_top": True})
            page.locator(".site-theme-button").click()
            page.locator(f'[data-theme-choice="{mode}"]').click()
            resolved = scheme if mode == "system" else mode
            sync_api.expect(page.locator("html")).to_have_attribute(
                "data-kpress-resolved-theme", resolved
            )
            readings.append(
                {
                    "phase": phase,
                    "expected": resolved,
                    **page.evaluate(THEME, {"scroll_top": False}),
                }
            )
    return readings


@pytest.fixture(scope="module")
def seen(toggle_seen: dict[int, dict[str, Any]]) -> dict[int, dict[str, Any]]:
    """Share the retained interaction session with the geometry and content checks."""
    return toggle_seen


@pytest.mark.parametrize("width", WIDTHS)
def test_keyboard_expansion_uses_the_shared_triangle_without_click_time_preparation(
    toggle_seen: dict[int, dict[str, Any]], width: int
) -> None:
    report = toggle_seen[width]
    initial = report["initial"]
    assert initial["h1_spacing"]
    assert report["about"]["h1_spacing"]
    h1_space = initial["h1_spacing"][0]["above"]
    assert h1_space > 0
    for heading in (*initial["h1_spacing"], *report["about"]["h1_spacing"]):
        assert heading["above"] == pytest.approx(h1_space, abs=0.01)
    hero = report["hero"]
    assert [drawing["n"] for drawing in hero["drawings"]] == [53]
    assert hero["captions"] == ["Best known packing for 53 identical squares"]
    assert hero["drawings"][0]["href"] == "cases/53.html"
    assert hero["drawings"][0]["width"] == pytest.approx(hero["drawings"][0]["height"], abs=0.5)
    assert hero["width"] <= 288.5
    assert abs(hero["center_offset"]) <= 0.5
    assert hero["overflow"] == 0
    assert hero["popovers"] == 1
    assert report["hero_case"]["case"] == "53"
    assert [
        f"{urlsplit(href).path.lstrip('/')}"
        f"{'#' + urlsplit(href).fragment if urlsplit(href).fragment else ''}"
        for href in report["hero_case"]["actions"]
    ] == [
        "cases/53.html",
        "atlas.html#n-53",
        "atlas.html#atlas-n-53",
    ]
    assert report["static_hero"]["drawings"][0]["href"] == "cases/53.html"
    assert initial["cases"] == list(range(1, 101))
    assert initial["visible_cases"] == 100
    assert initial["drawings"]["cards"] == 100
    assert initial["drawings"]["rows"] == list(range(1, 11))
    assert initial["drawings"]["size"] == ("medium" if width >= 1200 else "small")
    assert initial["drawings"]["scale"] == "row"
    assert initial["stage"] == 100
    assert initial["view"] == "triangle"
    assert initial["toggle"]["name"] == "Show more: all 324 cases"
    assert initial["prepared_cases"] == 324
    assert initial["images"] == {"decoded": 324, "loaded": 324, "failed": 0}
    assert initial["control_groups"] == [
        "Atlas layout",
        "Atlas tile size",
        "Atlas drawing scale",
        "Atlas drawings",
    ]
    assert initial["atlas_legend"]
    for control in initial["control_type"]:
        assert 0.75 <= control["size"] / control["base"] <= 0.9
    assert initial["cells_role"] == "tabpanel"
    assert initial["toggle"]["expanded"] == "false"
    assert initial["toggle"]["label"] == "Show More"
    assert initial["toggle"]["arrow"] == "double-down"
    assert initial["toggle"]["controls"] == "homepage-atlas-cells"
    for name in ("expanded", "cached"):
        state = report[name]
        assert state["cases"] == list(range(1, 325)), name
        assert state["visible_cases"] == 324, name
        assert state["toggle"]["expanded"] == "true", name
        assert state["toggle"]["label"] == "Show Less", name
        assert state["toggle"]["name"] == "Show less: the first 100"
        assert state["toggle"]["arrow"] == "double-up", name
        assert not state["toggle"]["disabled"], name
        assert state["busy"] is None, name
        assert state["drawings"]["cards"] == 324
        assert state["drawings"]["rows"] == list(range(1, 19))
        assert state["view"] == "triangle"
    collapsed = report["collapsed"]
    assert collapsed["cases"] == initial["cases"]
    assert collapsed["drawings"] == initial["drawings"]
    assert collapsed["toggle"]["expanded"] == "false"
    assert collapsed["toggle"]["label"] == "Show More"
    assert collapsed["toggle"]["arrow"] == "double-down"
    assert collapsed["toggle"]["focused"]
    assert collapsed["prepared_cases"] == 324
    assert collapsed["view"] == "triangle"
    for name in ("initial", "expanded", "collapsed", "cached", "static_labels"):
        center = report[name]["centering"]
        assert center["page_overflow"] == 0, name
        if center["fits"]:
            assert abs(center["offset"]) <= 0.5, (name, center)
    for name in ("initial", "expanded", "collapsed", "cached"):
        state = report[name]
        assert state["label_errors"] == [], name
        assert state["mark_errors"] == [], name
        assert state["number_fonts"] == [state["sans_family"]], name
        for n in state["cases"]:
            assert state["case_names"][str(n)].startswith(f"n = {n}, "), name

        assert report[name]["raw_markup"] == 0, name
        assert state["star_cases"] == [], name
    assert report["atlas_requests"] == 0
    for name in ("initial", "expanded", "collapsed", "cached"):
        assert report[name]["toggle"]["arrow_hidden"] == "true"
        assert report[name]["toggle"]["arrow_mask"] != "none"
        assert report[name]["toggle"]["arrow_width"] > 0
    for name, count in (
        ("expanded_move", 324),
        ("cached_move", 324),
    ):
        transition = report[name]
        response = transition["input"]
        assert response["view"] == "triangle"
        assert response["count"] == count
        assert response["same_nodes"]
        assert response["scroll_delta"] == 0
        assert transition["placement_errors"] == []
        assert transition["drawing_errors"] == []
        assert transition["row_alignment_errors"] == []
        assert transition["duration"] == 360
        if name == "expanded_move" and initial["centering"]["fits"]:
            # Growing the centered visible canvas moves retained tiles horizontally.
            assert any(
                abs(float(animation["first_transform"].split("(", 1)[1].split("px", 1)[0]))
                > 0.5
                for animation in response["animations"]
            )
        if response["layout_changed"]:
            assert response["animations"]
        for animation in response["animations"]:
            assert animation["duration"] == transition["duration"]
            assert animation["delay"] == 0
            assert animation["easing"] == transition["easing"]
        assert transition["address"] == report["address"]
        assert transition["root_view"] == report["root_view"]
        assert transition["root_size"] == report["root_size"]
        assert transition["panel_id"] == "homepage-atlas-cells"
        assert transition["panel_role"] == "tabpanel"
        assert all(aspect == pytest.approx(1, abs=0.002) for aspect in transition["aspects"])
    assert report["collapsed_move"]["input"]["same_nodes"]
    assert report["collapsed_move"]["toggle_in_view"]
    reduced = report["reduced_move"]
    assert reduced["input"]["count"] == 324
    assert reduced["input"]["same_nodes"]
    assert reduced["input"]["animations"] == []
    assert reduced["duration"] == 0
    assert reduced["placement_errors"] == []
    assert report["reduced_collapsed"]["input"]["count"] == 100
    assert report["reduced_collapsed"]["input"]["same_nodes"]
    assert report["reduced_collapsed"]["input"]["animations"] == []
    assert report["reduced_collapsed"]["toggle_in_view"]
    assert report["rapid"]["counts"][-4:] == [324, 100, 324, 100]
    assert report["rapid"]["input"]["same_nodes"]
    assert report["rapid"]["placement_errors"] == []
    assert report["rapid"]["toggle_in_view"]
    assert report["static"]["page_overflow"] == 0
    static = report["static"]["tiles"]
    assert report["static_labels"]["raw_markup"] == 0
    assert report["static_labels"]["label_errors"] == []
    assert report["static_labels"]["star_cases"] == []
    assert [tile["n"] for tile in static] == list(range(1, 101))
    for index, tile in enumerate(static):
        assert tile["left"] >= report["static"]["canvas"]["left"] - 0.5
        assert tile["right"] <= report["static"]["canvas"]["right"] + 0.5
        for other in static[index + 1 :]:
            assert (
                tile["right"] <= other["left"] + 0.5
                or other["right"] <= tile["left"] + 0.5
                or tile["top"] + tile["height"] <= other["top"] + 0.5
                or other["top"] + other["height"] <= tile["top"] + 0.5
            ), (tile["n"], other["n"])
    assert [themed["cases"] for themed in report["staged_themes"]] == [100, 324, 100]
    for themed in report["staged_themes"]:
        assert themed["resolved"] == themed["expected"]
        assert themed["background"] == themed["page_background"]
        assert themed["palette_unchanged"]
        assert themed["label_contrast"] >= 4.5
    assert urlsplit(report["late_case"]).path.lstrip("/") == "cases/291.html"
    controls = report["controls"]
    assert [state["view"] for state in controls] == ["grid"] * 5 + ["triangle"]
    assert controls[1]["drawings"]["size"] == "large"
    assert controls[2]["drawings"]["scale"] == "row"
    assert controls[-1]["drawings"]["size"] == "small"
    assert controls[-1]["drawings"]["scale"] == "fixed"
    for state in controls:
        address = urlsplit(state["address"])
        assert address.path == urlsplit(report["address"]).path
        assert set(parse_qs(address.query)) <= {"atlas", "size", "scale"}
        assert state["centering"]["page_overflow"] == 0
        if state["centering"]["fits"]:
            assert abs(state["centering"]["offset"]) <= 0.5


@pytest.fixture(scope="module")
def toggle_seen(browser: Any, request: pytest.FixtureRequest) -> dict[int, dict[str, Any]]:
    """One shared session keeps every keyboard, pointer, theme and fallback reading."""
    sync_api = site_browser.api()
    reports = {}
    live = os.environ.get("SQPACK_SITE_PREVIEW_URL")
    origin = f"{live.rstrip('/')}/" if live else ORIGIN
    files = request.getfixturevalue("payloads") if not live else None
    for width in WIDTHS:
        page = browser.new_page(viewport={"width": width, "height": 900})
        if files is not None:
            _serve(page, files)
        requests = _requests(page)
        try:
            page.goto(f"{origin}index.html", wait_until="load")
            sync_api.expect(page.locator(TOGGLE)).to_be_visible()
            # The ordinary reader expansion reuses already decoded, authored images.
            sync_api.expect(page.locator("[data-atlas-preview]")).to_have_attribute(
                "data-atlas-images-ready", "324", timeout=15000
            )
            report = {"initial": page.evaluate(STATE)}
            report["origin"] = origin
            report["download"] = page.evaluate(DOWNLOAD_ACTION)
            results_screenshot = os.environ.get("SQPACK_HOMEPAGE_RESULTS_SCREENSHOT")
            if width == WIDTHS[0] and results_screenshot:
                recent = page.locator('h2[id="recent-results"]').bounding_box()
                actions = (
                    page.locator(".site-action-row")
                    .filter(has=page.locator("a[data-all-results]"))
                    .bounding_box()
                )
                assert recent is not None
                assert actions is not None
                page.screenshot(
                    path=results_screenshot,
                    full_page=True,
                    clip={
                        "x": 0,
                        "y": recent["y"] - 12,
                        "width": width,
                        "height": actions["y"] + actions["height"] - recent["y"] + 36,
                    },
                )
            screenshot = os.environ.get("SQPACK_HOMEPAGE_MEDIA_SCREENSHOT")
            if width == WIDTHS[0] and screenshot:
                scroll_y = page.evaluate(MEDIA_IMAGES)
                pdfs = page.locator('h1[id="visuals"]').bounding_box()
                video = page.locator(".site-homepage-film").bounding_box()
                assert pdfs is not None
                assert video is not None
                page.screenshot(
                    path=screenshot,
                    full_page=True,
                    clip={
                        "x": 0,
                        "y": pdfs["y"] + scroll_y - 12,
                        "width": width,
                        "height": video["y"] + video["height"] - pdfs["y"] + 80,
                    },
                )
            report["preview_pointer"] = _pointer_cases(page, (18, 36))
            report["hero"] = page.evaluate(HERO)
            hero = page.locator('.site-hero-figure a[data-case="53"]')
            hero.click()
            sync_api.expect(page.locator('#pop-case article[data-case="53"]')).to_be_visible()
            report["hero_case"] = {
                "case": page.locator("#pop-case article[data-case]").get_attribute("data-case"),
                "actions": [
                    link.get_attribute("href")
                    for link in page.locator("#pop-case a.site-popover-action").all()
                ],
            }
            page.keyboard.press("Escape")
            sync_api.expect(hero).to_be_focused()
            report["address"] = page.url
            screenshot_dir = os.environ.get("SQPACK_HOME_ATLAS_SCREENSHOT_DIR")
            if screenshot_dir:
                page.locator(".site-hero-figure").screenshot(
                    path=str(Path(screenshot_dir) / f"homepage-hero-53-{width}.png")
                )
                page.locator("[data-atlas-preview]").screenshot(
                    path=str(Path(screenshot_dir) / f"homepage-triangle-100-{width}.png")
                )
            baseline = page.evaluate(TRANSITION, {"install": True, "settle": False})
            report["root_view"] = baseline["root_view"]
            report["root_size"] = baseline["root_size"]
            toggle = page.locator(TOGGLE)
            toggle.focus()
            page.evaluate(TRANSITION, {"install": False, "settle": True, "position": True})
            page.keyboard.press("Enter")
            report["expanded_move"] = page.evaluate(
                TRANSITION, {"install": False, "settle": True}
            )
            sync_api.expect(page.locator(TILES)).to_have_count(324)
            sync_api.expect(toggle).to_be_enabled()
            report["expanded"] = page.evaluate(STATE)
            if screenshot_dir:
                page.locator("[data-atlas-preview]").screenshot(
                    path=str(Path(screenshot_dir) / f"homepage-triangle-324-{width}.png")
                )
            toggle.focus()
            page.keyboard.press("Space")
            report["collapsed_move"] = page.evaluate(
                TRANSITION, {"install": False, "settle": True}
            )
            sync_api.expect(page.locator(TILES)).to_have_count(100)
            report["collapsed"] = page.evaluate(STATE)
            page.evaluate(TRANSITION, {"install": False, "settle": True, "position": True})
            page.keyboard.press("Enter")
            report["cached_move"] = page.evaluate(
                TRANSITION, {"install": False, "settle": True}
            )
            sync_api.expect(page.locator(TILES)).to_have_count(324)
            report["cached"] = page.evaluate(STATE)
            page.emulate_media(reduced_motion="reduce")
            page.keyboard.press("Space")
            page.evaluate(TRANSITION, {"install": False, "settle": True})
            page.keyboard.press("Enter")
            report["reduced_move"] = page.evaluate(
                TRANSITION, {"install": False, "settle": True}
            )
            page.keyboard.press("Space")
            report["reduced_collapsed"] = page.evaluate(
                TRANSITION, {"install": False, "settle": True}
            )
            page.emulate_media(reduced_motion="no-preference")
            report["rapid"] = page.evaluate(
                TRANSITION, {"install": False, "settle": True, "rapid": True}
            )
            report["staged_themes"] = []
            for stage, mode, scheme in (
                (100, "system", "dark"),
                (324, "light", "dark"),
                (100, "dark", "light"),
            ):
                if page.locator(TILES).count() != stage:
                    toggle.click()
                    page.evaluate(TRANSITION, {"install": False, "settle": True})
                sync_api.expect(page.locator(TILES)).to_have_count(stage)
                page.emulate_media(color_scheme=scheme)
                page.evaluate(THEME, {"scroll_top": True})
                page.locator(".site-theme-button").click()
                page.locator(f'[data-theme-choice="{mode}"]').click()
                report["staged_themes"].append(
                    {
                        **page.evaluate(THEME, {"scroll_top": False}),
                        "expected": scheme if mode == "system" else mode,
                    }
                )
            toggle.click()
            page.evaluate(TRANSITION, {"install": False, "settle": True})
            report["expanded_pointer"] = _pointer_cases(page, (306, 324))
            late = page.locator(f'{TILES}[data-case="291"]')
            late.focus()
            page.keyboard.press("Enter")
            article = page.locator('#pop-case article[data-case="291"]')
            sync_api.expect(article).to_be_visible()
            report["late_case"] = page.locator("#pop-case [data-case-open]").get_attribute(
                "href"
            )
            report["case"] = {
                "shown": article.get_attribute("data-case"),
                "action": report["late_case"],
                "address": page.url,
                "math_errors": article.locator("[data-kpress-math-error]").count(),
                "unprepared": article.locator(
                    '.kpress-math:not([data-kpress-math-rendered="true"])'
                ).count(),
            }
            page.keyboard.press("Escape")
            sync_api.expect(late).to_be_focused()
            report["case_closed"] = not page.locator("#pop-case").is_visible()
            report["themes"] = _themes(page)
            report["atlas_requests"] = requests.count(f"{origin}{GRAPHIC}")
            static_page = browser.new_page(
                viewport={"width": width, "height": 900}, java_script_enabled=False
            )
            if files is not None:
                _serve(static_page, files)
            try:
                static_page.goto(f"{origin}index.html", wait_until="load")
                sync_api.expect(static_page.locator(TOGGLE)).to_be_hidden()
                sync_api.expect(static_page.locator(TILES)).to_have_count(100)
                sync_api.expect(static_page.locator(EXPLORE)).to_be_visible()
                report["static"] = static_page.evaluate(INITIAL_LAYOUT)
                report["static_labels"] = static_page.evaluate(STATE)
                report["static_hero"] = static_page.evaluate(HERO)
            finally:
                static_page.close()
            report["controls"] = []
            for selector in (
                '[data-atlas-tab="grid"]',
                '[data-atlas-size-tab="large"]',
                '[data-atlas-scale-tab="row"]',
                '[data-atlas-scale-tab="fixed"]',
                '[data-atlas-size-tab="small"]',
                '[data-atlas-tab="triangle"]',
            ):
                page.locator(selector).click()
                page.evaluate(TRANSITION, {"install": False, "settle": True})
                report["controls"].append({"address": page.url, **page.evaluate(STATE)})
            page.goto(f"{origin}about.html", wait_until="load")
            report["about"] = page.evaluate(STATE)
            reports[width] = report
        finally:
            page.close()
    return reports


@pytest.mark.parametrize("width", WIDTHS)
def test_native_svg_case_links_align_with_drawings_and_open_by_pointer_after_scroll(
    seen: dict[int, dict[str, Any]], width: int
) -> None:
    for phase, cases in (("preview_pointer", (18, 36)), ("expanded_pointer", (306, 324))):
        readings = seen[width][phase]
        assert [reading["n"] for reading in readings] == list(cases)
        for reading in readings:
            assert reading["opened"] == str(reading["n"])
            assert reading["drawing_width"] > 0
            assert reading["drawing_width"] == pytest.approx(reading["drawing_height"], abs=0.1)
            assert reading["row"] == int((reading["n"] - 1) ** 0.5) + 1
            assert reading["segment"] in ("grid", "non-grid")
            assert reading["source"].endswith(f"/n-{reading['n']}.svg")
            assert 0 <= reading["center_x"] <= reading["viewport_width"]
            assert reading["contained"]
            assert reading["page_overflow"] == 0, (phase, reading)


@pytest.mark.parametrize("width", WIDTHS)
def test_a_newly_inserted_case_opens_its_prepared_record_in_the_existing_popover(
    seen: dict[int, dict[str, Any]], width: int
) -> None:
    case = seen[width]["case"]
    assert case["shown"] == "291"
    assert case["action"] == f"{seen[width]['origin']}cases/291.html"
    assert case["address"] == f"{seen[width]['origin']}index.html"
    assert case["math_errors"] == case["unprepared"] == 0
    assert seen[width]["case_closed"]


@pytest.mark.parametrize("width", WIDTHS)
def test_homepage_order_chrome_and_single_card_rows_keep_the_shared_design(
    seen: dict[int, dict[str, Any]], width: int
) -> None:
    home = seen[width]["initial"]
    assert home["headings"] == [
        "the-atlas-of-square-packings",
        "news",
        "recent-results",
        "report-your-results",
        "papers",
    ]
    assert home["main_titles"] == [
        "the-problem",
        "visuals",
        "squares-project-documentation",
        "more-resources",
    ]
    assert len(home["section_title_styles"]) == 8
    selected = news_highlights.highlights(site_renders.overview())
    assert [heading["entry"] for heading in home["news_headings"]] == [
        result.id for result in selected
    ]
    assert len(home["news_headings"]) == 3
    assert all(heading["title"] for heading in home["news_headings"])
    assert home["other_lower_headings"] == []
    assert all(style == home["main_title_style"] for style in home["section_title_styles"])
    assert home["recent_title"] == "Recent Major Results"
    assert home["media"] == {
        "visuals": ["square-packings-324-20261008.pdf"],
    }
    assert home["legacy_pdf_anchor"]
    assert not home["scope_present"]
    assert home["actions"]
    for action in home["actions"]:
        assert action["transform"] == "uppercase", action
    download = seen[width]["download"]
    assert download["order"] == ["Download PDF", "Explore the atlas"]
    assert download["href"] == overview_sections.PDF_CARD_SPECS[1][0]
    assert download["download"]
    assert download["uppercase"] == "uppercase"
    assert download["icon"].startswith("url(")
    assert download["icon_hidden"] == "true"
    assert download["left"] >= 0
    assert download["right"] <= width
    assert home["solo_cards"]
    for card in home["solo_cards"]:
        assert abs(card["center_offset"]) <= 1, card
    assert "squares-project-documentation" in seen[width]["about"]["main_titles"]


@pytest.fixture(scope="module")
def results_navigation_seen(browser: Any) -> dict[int, dict[str, Any]]:
    """Use the two real Results actions without repeating Atlas interactions."""
    sync_api = site_browser.api()
    readings = {}
    live = os.environ.get("SQPACK_SITE_PREVIEW_URL")
    origin = f"{live.rstrip('/')}/" if live else ORIGIN
    files = None
    if not live:
        documents = {name: site_renders.html(name) for name in ("index.html", "results.html")}
        files = {
            **{name: html.encode() for name, html in documents.items()},
            **{
                f"assets/{name}": data
                for name, data in site_assets.shared()
                .assets.referenced(documents.values())
                .items()
            },
            **render_overview.support_files(),
        }
    for width in NAV_WIDTHS:
        page = browser.new_page(viewport={"width": width, "height": 900})
        if files is not None:
            _serve(page, files)
        try:
            page.goto(f"{origin}index.html?s=4", wait_until="load")
            initial = page.evaluate(STATE)
            verification = page.get_by_role(
                "link", name=re.compile("^About Result Verification$", re.IGNORECASE)
            )
            bounds = verification.bounding_box()
            assert bounds is not None
            assert bounds["x"] >= 0
            assert bounds["x"] + bounds["width"] <= width
            verification.focus()
            with page.expect_navigation(wait_until="load"):
                page.keyboard.press("Enter")
            destination = f"{origin}results.html#verification-ladders"
            sync_api.expect(page).to_have_url(destination)
            sync_api.expect(page.locator("#verification-ladders")).to_be_in_viewport()
            sync_api.expect(page.locator("div.site-rung-legend[role=note]")).to_have_count(0)
            keyboard_destination = page.url
            page.goto(f"{origin}index.html?s=4", wait_until="load")
            all_results = page.get_by_role(
                "link", name=re.compile("^All Results$", re.IGNORECASE)
            )
            bounds = all_results.bounding_box()
            assert bounds is not None
            assert bounds["x"] >= 0
            assert bounds["x"] + bounds["width"] <= width
            with page.expect_navigation(wait_until="load"):
                all_results.click()
            sync_api.expect(page).to_have_url(f"{origin}results.html?s=4#all-results")
            sync_api.expect(page.locator("#all-results")).to_be_in_viewport()
            readings[width] = {
                "initial": initial,
                "keyboard_destination": keyboard_destination,
                "pointer_destination": page.url,
                "destination": destination,
            }
        finally:
            page.close()
    return readings


@pytest.mark.parametrize("width", NAV_WIDTHS)
def test_results_actions_reach_verification_and_the_complete_table(
    results_navigation_seen: dict[int, dict[str, Any]], width: int
) -> None:
    reading = results_navigation_seen[width]
    assert not reading["initial"]["scope_present"]
    assert not reading["initial"]["legend_present"]
    assert reading["keyboard_destination"] == reading["destination"]
    parsed = urlsplit(reading["pointer_destination"])
    assert parsed.path == "/results.html"
    assert parsed.query == "s=4"
    assert parsed.fragment == "all-results"


@pytest.mark.parametrize("width", WIDTHS)
def test_native_svg_follows_live_system_light_dark_choices_in_all_cached_states(
    seen: dict[int, dict[str, Any]], width: int
) -> None:
    readings = seen[width]["themes"]
    assert len(readings) == 12
    for state in readings:
        assert state["resolved"] == state["expected"]
        assert state["cases"] == (324 if state["phase"] == "expanded" else 100)
        assert state["background"] == state["page_background"]
        assert state["white_samples"] > 0, state
        assert state["colored_samples"] > 0, state
        assert state["label_contrast"] >= 4.5, state
        assert state["palette_samples"] >= 5
        assert state["palette_unchanged"]
        assert state["filter"] == "none"
    for phase in ("preview", "expanded", "collapsed"):
        colors = {tuple(state["background"]) for state in readings if state["phase"] == phase}
        assert len(colors) == 2, phase
        pixels = {state["palette_signature"] for state in readings if state["phase"] == phase}
        assert len(pixels) == 1, phase


@pytest.mark.parametrize("width", WIDTHS)
def test_missing_shared_engine_keeps_native_preview_and_explore_usable(
    browser: Any, payloads: dict[str, bytes], width: int
) -> None:
    sync_api = site_browser.api()
    page = browser.new_page(viewport={"width": width, "height": 900})
    _serve(page, payloads)
    page.route(f"{ORIGIN}assets/js/atlas-view.*.js", lambda route: route.abort())
    errors = []

    def record_error(error: Any) -> None:
        # Playwright annotates callbacks, which a built-in list method cannot accept.
        errors.append(error)

    page.on("pageerror", record_error)
    try:
        page.goto(f"{ORIGIN}index.html", wait_until="load")
        sync_api.expect(page.locator(STATUS)).to_be_visible()
        sync_api.expect(page.locator(TOGGLE)).to_be_hidden()
        failed = page.evaluate(STATE)
        assert failed["visible_cases"] == 100
        assert failed["toggle"]["expanded"] == "false"
        assert failed["prepared_cases"] == 324
        assert failed["busy"] is None
        assert failed["status"]["role"] == "status"
        assert "Explore the atlas" in failed["status"]["text"]
        assert page.url == f"{ORIGIN}index.html"

        assert errors == []
        page.locator(EXPLORE).click()
        sync_api.expect(page).to_have_url(f"{ORIGIN}atlas.html")
        sync_api.expect(page.locator("[data-atlas-grid]")).to_be_visible()
    finally:
        page.close()


@pytest.mark.parametrize("width", WIDTHS)
def test_explore_stays_usable_without_javascript_and_the_expander_stays_hidden(
    browser: Any, payloads: dict[str, bytes], width: int
) -> None:
    sync_api = site_browser.api()
    page = browser.new_page(viewport={"width": width, "height": 900}, java_script_enabled=False)
    _serve(page, payloads)
    try:
        page.goto(f"{ORIGIN}index.html", wait_until="load")
        sync_api.expect(page.locator(TOGGLE)).to_be_hidden()
        sync_api.expect(page.locator(TILES)).to_have_count(100)
        sync_api.expect(page.locator(EXPLORE)).to_be_visible()
        page.locator(EXPLORE).click()
        sync_api.expect(page).to_have_url(f"{ORIGIN}atlas.html")
        sync_api.expect(page.locator("[data-atlas-grid]")).to_be_visible()
    finally:
        page.close()


@pytest.mark.parametrize("width", WIDTHS)
def test_news_cards_expand_only_on_press_and_legacy_bookmarks_forward(
    browser: Any, payloads: dict[str, bytes], width: int
) -> None:
    sync_api = site_browser.api()
    page = browser.new_page(
        viewport={"width": width, "height": 900},
        reduced_motion="reduce",
        has_touch=width == 390,
    )
    _serve(page, payloads)
    try:
        page.goto(ORIGIN, wait_until="load")
        preview = page.evaluate(NEWS)
        assert len(preview["entries"]) == 3
        page.locator('.site-action[href="news.html"]').click()
        page.wait_for_url(f"{ORIGIN}news.html")
        page.locator('[data-news-all="scores"]').click()
        news = page.evaluate(NEWS)
        document = render_changelog.load()
        assert len(news["entries"]) == len(document["entries"])
        assert len(news["days"]) == len(document["entries"])
        assert news["heading"]["transform"] == "uppercase"
        assert news["family"] == news["heading"]["family"]
        assert preview["reference_h3"] == news["reference_h3"]
        for surface in (preview, news):
            assert surface["overflow"] == 0
            for day in surface["days"]:
                assert day["border"] == 1
                assert 0 <= day["left"] < day["right"] <= width
                assert day["family"] == surface["family"]
                assert day["body_family"] == surface["family"]
                assert day["date_transform"] == "none"
                assert day["title_style"] == surface["reference_h3"]
                assert day["title_style"]["color"] == surface["text_color"]
                assert day["title_before_date"]
                assert day["date_before_topics"]
                assert day["metadata_after_date"]
                assert day["meter_count"] == 1
                assert day["meter_label"].startswith("Significance S")
                assert day["meter_tooltip"]
                assert abs(day["meter_right_gap"]) <= 0.5
                assert day["meter_with_topics"]
                assert "Significance" not in day["visible_rating_label"]
                for topic in day["topic_styles"]:
                    assert topic["transform"] == "none"
                    assert topic["caps"] == "normal"
                    assert float(topic["size"].removesuffix("px")) < day["title_size"]
                    assert topic["family"] == day["title_style"]["family"]
        card = page.locator("[data-news-day].is-collapsed").first
        card_id = card.get_attribute("id")
        assert card_id is not None
        card = page.locator(f"#{card_id}")
        button = card.locator(".site-news-expand")

        def reading() -> dict[str, Any]:
            return next(day for day in page.evaluate(NEWS)["days"] if day["id"] == card_id)

        sync_api.expect(button).to_have_attribute("aria-expanded", "false")
        closed = reading()
        assert closed["body_height"] == pytest.approx(10 * closed["line_height"], abs=1)
        assert closed["body_scroll"] > closed["body_height"]
        assert closed["button_top"] >= closed["body_bottom"]
        assert closed["fade"] == "1"
        assert "max-block-size" in closed["height_transition"]
        assert "rotate" in closed["arrow_transition"]
        meter = card.locator(".site-significance[data-site-tooltip]")
        meaning = meter.get_attribute("data-site-tooltip")
        entry_id = card.locator("[data-news-entry]").get_attribute("data-news-entry")
        entry = next(item for item in document["entries"] if item["id"] == entry_id)
        assert meaning is not None
        assert (
            overview_sections.rung_meanings()[f"S{entry['significance']['score']}"] in meaning
        )
        assert entry["significance"]["rationale"] in meaning
        tooltip = page.locator(".site-rating-tooltip.kpress-tooltip-visible")
        for interaction in ("hover", "focus", "press"):
            page.mouse.move(0, 0)
            button.focus()
            if interaction == "hover":
                meter.hover()
            elif interaction == "focus":
                meter.focus()
            elif width == 390:
                meter.tap()
            else:
                meter.click()
            sync_api.expect(tooltip).to_be_visible()
            sync_api.expect(tooltip).to_have_text(meaning)
            sync_api.expect(button).to_have_attribute("aria-expanded", "false")
            assert reading()["height"] == closed["height"]
            assert reading()["body_height"] == closed["body_height"]
            page.keyboard.press("Escape")
            sync_api.expect(tooltip).to_have_count(0)
        page.mouse.move(0, 0)
        button.focus()
        card.hover()
        assert reading()["height"] == closed["height"]
        button.focus()
        assert reading()["height"] == closed["height"]
        button.press("Enter")
        sync_api.expect(button).to_have_attribute("aria-expanded", "true")
        opened = reading()
        assert opened["body_height"] >= opened["body_scroll"] - 1
        assert opened["fade"] == "0"
        page.mouse.move(0, 0)
        assert reading()["height"] == opened["height"]
        button.press("Space")
        sync_api.expect(button).to_have_attribute("aria-expanded", "false")
        link = card.locator('a[href*="/pull/"]').first
        link.focus()
        sync_api.expect(button).to_have_attribute("aria-expanded", "true")
        button.click()
        sync_api.expect(button).to_have_attribute("aria-expanded", "false")
        card.locator("h3").first.click()
        sync_api.expect(button).to_have_attribute("aria-expanded", "true")
        if width == 1280:
            button.click()
            page.emulate_media(reduced_motion="no-preference")
            button.click()
            page.wait_for_function(
                NEWS_SETTLED, arg={"id": card_id, "open": True}, timeout=5000
            )
            assert reading()["inline_height"] == ""
            page.set_viewport_size({"width": 390, "height": 900})
            page.wait_for_function(
                NEWS_SETTLED, arg={"id": card_id, "open": True}, timeout=5000
            )
            page.set_viewport_size({"width": width, "height": 900})
            button.click()
            page.wait_for_function(
                NEWS_SETTLED, arg={"id": card_id, "open": False}, timeout=5000
            )
            # Keep rapid activations on the same focused control as its footer moves.
            button.press("Enter", delay=30)
            button.press("Enter")
            page.wait_for_function(
                NEWS_SETTLED, arg={"id": card_id, "open": False}, timeout=5000
            )
            button.click()
            page.wait_for_function(
                NEWS_SETTLED, arg={"id": card_id, "open": True}, timeout=5000
            )
            page.emulate_media(reduced_motion="reduce")
        link = card.locator('a[href*="/pull/"]').first
        target = link.get_attribute("href")
        assert target is not None
        page.context.route(
            target, lambda route: route.fulfill(body="<p>Ordinary proof link</p>")
        )
        if link.get_attribute("target") == "_blank":
            with page.expect_popup() as opened_link:
                link.click()
            linked_page = opened_link.value
            sync_api.expect(linked_page).to_have_url(target)
            linked_page.close()
        else:
            link.click()
            sync_api.expect(page).to_have_url(target)
        anchor = render_changelog.entry_anchor(
            render_changelog.ordered_entries(document)[0]["id"]
        )
        page.goto(f"{ORIGIN}about.html#{anchor}", wait_until="load")
        page.wait_for_url(f"{ORIGIN}news.html#{anchor}")
        sync_api.expect(page.locator(f"#{anchor}")).to_be_visible()
        owner = page.locator(f"[data-news-day]#{anchor}")
        sync_api.expect(owner.locator(".site-news-expand")).to_have_attribute(
            "aria-expanded", "true"
        )
    finally:
        page.close()
    if width == 390:
        for javascript in (False, True):
            context = browser.new_context(
                viewport={"width": width, "height": 900},
                has_touch=True,
                is_mobile=True,
                java_script_enabled=javascript,
            )
            try:
                touch = context.new_page()
                _serve(touch, payloads)
                touch.goto(f"{ORIGIN}news.html", wait_until="load")
                card = touch.locator(
                    "[data-news-day].is-collapsed" if javascript else "[data-news-day]"
                ).first
                card_id = card.get_attribute("id")
                assert card_id is not None
                card = touch.locator(f"#{card_id}")
                button = card.locator(".site-news-expand")
                if javascript:
                    button.tap()
                    sync_api.expect(button).to_have_attribute("aria-expanded", "true")
                    button.tap()
                    sync_api.expect(button).to_have_attribute("aria-expanded", "false")
                else:
                    sync_api.expect(button).to_be_hidden()
                    full = touch.evaluate(NEWS)["days"][0]
                    assert full["body_height"] >= full["body_scroll"] - 1
            finally:
                context.close()


@pytest.mark.parametrize("width", WIDTHS)
def test_news_facets_history_bookmarks_and_shared_meters(
    browser: Any, payloads: dict[str, bytes], width: int, request: pytest.FixtureRequest
) -> None:
    document = render_changelog.load()
    page = browser.new_page(
        viewport={"width": width, "height": 900},
        reduced_motion="reduce",
        has_touch=width == 390,
    )
    _serve(page, payloads)

    def state() -> dict[str, Any]:
        return page.evaluate(NEWS_FILTERS)

    def expected(scores: set[int], topics: set[str] | None = None) -> set[str]:
        return {
            render_changelog.entry_anchor(entry["id"])
            for entry in document["entries"]
            if entry["significance"]["score"] in scores
            and (topics is None or topics.intersection(entry.get("topics", [])))
        }

    def check(scores: set[int], topics: set[str] | None = None) -> dict[str, Any]:
        seen = state()
        visible = {card["id"] for card in seen["cards"] if card["visible"]}
        assert visible == expected(scores, topics)
        assert seen["count"] == f"{len(visible)} of {len(document['entries'])} news items"
        assert seen["empty"] is (not visible)
        assert parse_qs(urlsplit(page.url).query)["reader"] == ["kept"]
        assert seen["overflow"] == 0
        return seen

    def shared_chooser_contract() -> None:
        for scheme in ("light", "dark"):
            page.emulate_media(color_scheme=scheme)
            appearances = {}
            for name, surface, group, chosen, other in (
                (
                    "home",
                    "index.html",
                    ".site-atlas-views",
                    '[aria-selected="true"]',
                    '[aria-selected="false"]',
                ),
                (
                    "scores",
                    "news.html",
                    '[aria-labelledby="news-significance-label"]',
                    '[data-news-score="4"]',
                    '[data-news-score="1"]',
                ),
                (
                    "topics",
                    "news.html",
                    '[aria-labelledby="news-topics-label"]',
                    '[data-news-topic][aria-pressed="true"]',
                    '[data-news-topic][aria-pressed="false"]',
                ),
            ):
                page.goto(f"{ORIGIN}{surface}", wait_until="load")
                if name == "topics":
                    page.locator(group).locator("[data-news-topic]").first.click()
                samples = {}
                for selection, choice in (("selected", chosen), ("unselected", other)):
                    control = page.locator(group).locator(choice).first
                    for interaction in ("normal", "hover", "focus"):
                        page.locator("h1").first.click()
                        page.mouse.move(0, 0)
                        if interaction == "hover":
                            control.hover()
                        elif interaction == "focus":
                            page.keyboard.press("Tab")
                            control.focus()
                        sample = page.evaluate(
                            NEWS_FILTERS, {"chooser": group, "choice": choice}
                        )["chooser"]
                        assert sample is not None
                        if interaction == "focus":
                            assert sample["focus_visible"]
                        samples[selection, interaction] = {
                            key: sample[key]
                            for key in ("appearance", "border", "gap", "height")
                        }
                appearances[name] = samples
            assert appearances["scores"] == appearances["home"], scheme
            assert appearances["topics"] == appearances["home"], scheme
            request.node.user_properties.append(
                (f"chooser-{scheme}", str(appearances["home"]["selected", "normal"]))
            )
            seen = state()
            assert seen["groups"] == [
                {"name": "Significance", "hidden_legend": True, "tabs": 0},
                {"name": "Topics", "hidden_legend": True, "tabs": 0},
            ]
            assert abs(seen["count_right_gap"]) <= 0.5
            assert abs(seen["count_card_right_gap"]) <= 0.5
            assert seen["count_above_cards"]
            news_count = seen["count_style"]
            broken = page.evaluate(
                NEWS_FILTERS,
                {
                    "chooser": '[aria-labelledby="news-significance-label"]',
                    "choice": '[data-news-score="4"]',
                    "overrideChooser": True,
                },
            )["chooser"]
            assert (
                broken["appearance"]["font-size"]
                != appearances["home"]["selected", "normal"]["appearance"]["font-size"]
            ), "the contract must reject a page-specific chooser override"
            page.goto(f"{ORIGIN}results.html", wait_until="load")
            results_count = state()["count_style"]
            for key in ("font-family", "font-size", "font-weight", "line-height", "color"):
                assert news_count[key] == results_count[key], (scheme, key)
        page.emulate_media(color_scheme="light")

    try:
        shared_chooser_contract()
        page.goto(f"{ORIGIN}news.html?reader=kept", wait_until="load")
        seen = check({4, 5})
        assert seen["scores"] == ["4", "5"]
        used_topics = {
            topic for entry in document["entries"] for topic in entry.get("topics", [])
        }
        assert set(seen["topics"]) == used_topics
        page.locator('button[data-news-score="3"]').focus()
        page.keyboard.press("Space")
        check({3, 4, 5})
        for topic in used_topics:
            if topic != "optimality":
                page.locator(f'button[data-news-topic="{topic}"]').click()
        check({3, 4, 5}, {"optimality"})
        page.locator('button[data-news-topic="verification"]').click()
        check({3, 4, 5}, {"optimality", "verification"})
        page.locator("[data-news-reset]").click()
        check({4, 5})
        for score in (4, 5):
            button = page.locator(f'button[data-news-score="{score}"]')
            button.tap() if width == 390 else button.click()
        check(set())
        assert parse_qs(urlsplit(page.url).query)["news-s"] == ["none"]
        page.locator('[data-news-all="scores"]').click()
        check({1, 2, 3, 4, 5})
        page.locator("[data-news-reset]").click()
        check({4, 5})
        page.go_back(wait_until="load")
        check({1, 2, 3, 4, 5})
        page.go_forward(wait_until="load")
        check({4, 5})
        low = max(
            (entry for entry in document["entries"] if entry["significance"]["score"] < 4),
            key=lambda entry: len(entry["summary"]) + len(entry.get("details", "")),
        )
        anchor = render_changelog.entry_anchor(low["id"])
        # Begin with a hidden card, so a prior plain bookmark cannot mask a
        # failure to expand the equivalent percent-encoded bookmark.
        encoded = f"%{ord(anchor[0]):02X}{anchor[1:]}"
        page.goto(f"{ORIGIN}news.html?reader=kept#{encoded}", wait_until="load")
        assert urlsplit(page.url).fragment == encoded
        seen = check({4, 5, low["significance"]["score"]})
        target = next(card for card in seen["cards"] if card["id"] == anchor)
        assert target["expanded"] == "true"
        assert not target["button_hidden"]
        assert abs(target["center_offset"]) <= 0.5
        button = page.locator(f"#{anchor} .site-news-expand")
        button.click()
        assert (
            next(card for card in state()["cards"] if card["id"] == anchor)["expanded"]
            == "false"
        )
        button.click()
        assert (
            next(card for card in state()["cards"] if card["id"] == anchor)["expanded"]
            == "true"
        )
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.goto(f"{ORIGIN}news.html?reader=kept#%E0%A4%A", wait_until="load")
        check({4, 5})
        assert errors == [], "a malformed bookmark must not break either enhancement"
        specimens = "".join(
            overview_sections.significance_mark(level, "Importance only.")
            for level in range(overview_sections.SIGNIFICANCE_TOP + 1)
        )
        samples = page.evaluate(NEWS_FILTERS, {"meters": specimens})["samples"]
        assert len(samples) == 6
        assert (
            max(item["width"] for item in samples) - min(item["width"] for item in samples)
            <= 0.1
        )
        for item in samples:
            assert item["filled"] == item["level"]
            assert item["border"] == 1
            assert len(item["bars"]) == 5
            for bar in item["bars"]:
                assert bar["border"] == 1
                assert bar["height"] > 0.5 * item["font"]
                assert bar["width"] > 0.4 * item["font"]
                assert (bar["fill"] == "rgba(0, 0, 0, 0)") is (not bar["filled"])
        static = browser.new_page(
            viewport={"width": width, "height": 900}, java_script_enabled=False
        )
        _serve(static, payloads)
        try:
            static.goto(f"{ORIGIN}news.html?news-s=none", wait_until="load")
            complete = static.evaluate(NEWS_FILTERS)
            assert complete["controls_hidden"]
            assert all(
                card["visible"] and card["full"] and card["button_hidden"]
                for card in complete["cards"]
            )
        finally:
            static.close()
    finally:
        page.close()
