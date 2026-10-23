"""The homepage's bounded previews, its complete atlas and card geometry in Chromium.

Real rendered pages and their assets are served through request routes in memory, so
the fixture writes no site output. One desktop and one mobile session exercise the
keyboard, canonical Atlas tiles, shared triangle animation and a case link.

Set `SQPACK_NEWS_SCREENSHOT_DIR` to a directory to keep review screenshots of the News
surfaces these tests drive: the first visible card at each width (`news-card-WIDTH.png`)
and the filter controls in each theme (`news-chooser-SCHEME-WIDTH.png`). Nothing reads
them; a pull request that changes the News presentation attaches them for review.
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
    check_site_rendering,
    news_highlights,
    overview_sections,
    preview_site,
    render_changelog,
    render_overview,
    site_assets,
)
from devtools.render_n11_lower_bounds_explainer import COMPOSITE_ASSETS
from devtools.render_n11_lower_bounds_explainer_pdf import BROWSER_OVERRIDE
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
TOOLTIP_WATCH = probe(PROBES, "site_homepage/tooltip-watch")
TOOLTIP_CLEAR = probe(PROBES, "site_homepage/tooltip-clear")
SCROLL_FILTERS = probe(PROBES, "site_homepage/scroll-filters")
CHOOSER_LABELS = probe(PROBES, "site_homepage/chooser-labels")
ORIGIN = "http://homepage.test/"
CELLS = "#homepage-atlas-cells"
TILES = f"{CELLS} .site-atlas-cell:visible"
GRID_TAB, TRIANGLE_TAB = '[data-atlas-tab="grid"]', '[data-atlas-tab="triangle"]'
GRAPHIC = "known-best-1-324.svg"
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
    """Homepage and standalone Videos, without rendering the case records."""
    documents = {name: site_renders.html(name) for name in ("index.html", "visualize.html")}
    files = site_assets.shared().assets.referenced(documents.values())
    posters = {hero for _, hero, *_ in overview_sections.ATLAS_CARDS}
    return {
        **{name: html.encode("utf-8") for name, html in documents.items()},
        **{f"assets/{name}": data for name, data in files.items()},
        **render_overview.support_files(),
        **{path.name: path.read_bytes() for path in COMPOSITE_ASSETS if path.name in posters},
    }


@pytest.mark.parametrize("width", WIDTHS)
def test_homepage_links_to_native_videos_and_reduced_motion_waits_for_click(
    browser: Any, request: pytest.FixtureRequest, width: int
) -> None:
    requests = []
    page = browser.new_page(viewport={"width": width, "height": 900}, reduced_motion="reduce")
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
        assert page.locator("video").count() == 0
        videos = page.locator('a[href="visualize.html"]').filter(has_text="View Videos")
        assert videos.count() == 1
        videos.click()
        film = page.locator(".site-film-frame video")
        film.scroll_into_view_if_needed()
        state = page.evaluate(FILM)
        assert requests == [], "preload=none must wait for the reader"
        assert state["controls"]
        assert state["inline"]
        assert state["preload"] == "none"
        assert not state["autoplay"]
        assert state["marked_autoplay"]
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
        assert state["height"] <= 900
        assert state["left"] >= 0
        assert state["right"] <= width
        assert state["overflow"] <= 0
        assert state["width"] / state["height"] == pytest.approx(16 / 9, abs=0.01)
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
    """Switch the actual theme controls and OS scheme in each view of every case."""
    sync_api = site_browser.api()
    readings = []
    for phase, tab in (("triangle", TRIANGLE_TAB), ("grid", GRID_TAB)):
        page.locator(tab).click()
        page.evaluate(TRANSITION, {"install": False, "settle": True})
        sync_api.expect(page.locator(TILES)).to_have_count(324)
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
    page.locator(TRIANGLE_TAB).click()
    page.evaluate(TRANSITION, {"install": False, "settle": True})
    return readings


@pytest.fixture(scope="module")
def seen(atlas_seen: dict[int, dict[str, Any]]) -> dict[int, dict[str, Any]]:
    """Share the retained interaction session with the geometry and content checks."""
    return atlas_seen


@pytest.mark.parametrize("width", WIDTHS)
def test_the_homepage_atlas_shows_every_case_in_the_shared_triangle(
    atlas_seen: dict[int, dict[str, Any]], width: int
) -> None:
    """The homepage's atlas shows all 324 cases from the first response, as the Atlas
    page does, and its controls move the same tiles with the shared layout and motion
    and no click-time preparation. Its Show More button, which revealed the cases after
    the first hundred, went on 2026-10-22 (the owner)."""
    report = atlas_seen[width]
    initial = report["initial"]
    assert initial["h1_spacing"]
    assert report["about"]["h1_spacing"]
    h1_space = initial["h1_spacing"][0]["above"]
    assert h1_space > 0
    about_headings = report["about"]["h1_spacing"]
    assert about_headings[0]["id"] == "the-squares-project"
    # The page's first block starts at its shared top padding; subsequent sections
    # keep the title-spacing token, as every homepage title below its hero does.
    assert about_headings[0]["above"] == pytest.approx(0, abs=0.01)
    for heading in (*initial["h1_spacing"], *about_headings[1:]):
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
        "frontier.html#n-53",
        "atlas.html#atlas-n-53",
    ]
    assert report["static_hero"]["drawings"][0]["href"] == "cases/53.html"
    assert initial["cases"] == list(range(1, 325))
    assert initial["visible_cases"] == 324
    assert initial["drawings"]["cards"] == 324
    assert initial["drawings"]["rows"] == list(range(1, 19))
    # Opened from the top, the homepage's triangle follows the scroll from XL
    # (`tests/test_site_atlas_follow.py`).
    assert initial["drawings"]["size"] == "xlarge"
    assert initial["drawings"]["scale"] == "row"
    assert initial["view"] == "triangle"
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
    for name, view in (("grid", "grid"), ("triangle", "triangle")):
        state = report[name]
        assert state["cases"] == list(range(1, 325)), name
        assert state["visible_cases"] == 324, name
        assert state["busy"] is None, name
        assert state["drawings"]["cards"] == 324
        assert state["view"] == view
    assert report["triangle"]["drawings"] == initial["drawings"]
    assert report["triangle"]["prepared_cases"] == 324
    for name in ("initial", "grid", "triangle", "static_labels"):
        center = report[name]["centering"]
        assert center["page_overflow"] == 0, name
        if center["fits"]:
            assert abs(center["offset"]) <= 0.5, (name, center)
    for name in ("initial", "grid", "triangle"):
        state = report[name]
        assert state["label_errors"] == [], name
        assert state["mark_errors"] == [], name
        assert state["number_fonts"] == [state["sans_family"]], name
        for n in state["cases"]:
            assert state["case_names"][str(n)].startswith(f"n = {n}, "), name

        assert report[name]["raw_markup"] == 0, name
        assert state["star_cases"] == [], name
    assert report["atlas_requests"] == 0
    for name, view in (("grid_move", "grid"), ("triangle_move", "triangle")):
        transition = report[name]
        response = transition["input"]
        assert response["view"] == view
        assert response["count"] == 324
        assert response["same_nodes"]
        assert response["scroll_delta"] == 0
        assert transition["placement_errors"] == []
        assert transition["drawing_errors"] == []
        assert transition["row_alignment_errors"] == []
        assert transition["duration"] == 360
        assert response["layout_changed"]
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
    for name in ("reduced_move", "reduced_back"):
        reduced = report[name]
        assert reduced["input"]["count"] == 324, name
        assert reduced["input"]["same_nodes"], name
        assert reduced["input"]["animations"] == [], name
        assert reduced["duration"] == 0, name
        assert reduced["placement_errors"] == [], name
    assert report["rapid"]["counts"][-4:] == [324] * 4
    assert report["rapid"]["input"]["view"] == "triangle"
    assert report["rapid"]["input"]["same_nodes"]
    assert report["rapid"]["placement_errors"] == []
    assert report["static"]["page_overflow"] == 0
    static = report["static"]["tiles"]
    assert report["static_labels"]["raw_markup"] == 0
    assert report["static_labels"]["label_errors"] == []
    assert report["static_labels"]["star_cases"] == []
    assert [tile["n"] for tile in static] == list(range(1, 325))
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
    assert [themed["view"] for themed in report["staged_themes"]] == [
        "triangle",
        "grid",
        "triangle",
    ]
    for themed in report["staged_themes"]:
        assert themed["cases"] == 324
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
def atlas_seen(browser: Any, request: pytest.FixtureRequest) -> dict[int, dict[str, Any]]:
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
            sync_api.expect(page.locator(TILES)).to_have_count(324)
            # Every row's authored images are decoded after first paint.
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
            # A reader who chooses a view ends the following, and the triangle takes its
            # own layout, where a tile is clicked where its layout puts it. The homepage
            # writes no view to its address.
            page.locator(GRID_TAB).click()
            page.locator(TRIANGLE_TAB).click()
            sync_api.expect(page.locator("[data-atlas-preview]")).to_have_attribute(
                "data-atlas-follow", "held"
            )
            report["pointer"] = _pointer_cases(page, (18, 36, 306, 324))
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
                    path=str(Path(screenshot_dir) / f"homepage-triangle-324-{width}.png")
                )
            baseline = page.evaluate(TRANSITION, {"install": True, "settle": False})
            report["root_view"] = baseline["root_view"]
            report["root_size"] = baseline["root_size"]
            # The keyboard presses the layout tabs, as a reader does.
            page.locator(GRID_TAB).focus()
            page.evaluate(TRANSITION, {"install": False, "settle": True, "position": True})
            page.keyboard.press("Enter")
            report["grid_move"] = page.evaluate(TRANSITION, {"install": False, "settle": True})
            sync_api.expect(page.locator(TILES)).to_have_count(324)
            report["grid"] = page.evaluate(STATE)
            if screenshot_dir:
                page.locator("[data-atlas-preview]").screenshot(
                    path=str(Path(screenshot_dir) / f"homepage-grid-324-{width}.png")
                )
            page.locator(TRIANGLE_TAB).focus()
            page.evaluate(TRANSITION, {"install": False, "settle": True, "position": True})
            page.keyboard.press("Space")
            report["triangle_move"] = page.evaluate(
                TRANSITION, {"install": False, "settle": True}
            )
            sync_api.expect(page.locator(TILES)).to_have_count(324)
            report["triangle"] = page.evaluate(STATE)
            page.emulate_media(reduced_motion="reduce")
            page.locator(GRID_TAB).focus()
            page.keyboard.press("Enter")
            report["reduced_move"] = page.evaluate(
                TRANSITION, {"install": False, "settle": True}
            )
            page.locator(TRIANGLE_TAB).focus()
            page.keyboard.press("Enter")
            report["reduced_back"] = page.evaluate(
                TRANSITION, {"install": False, "settle": True}
            )
            page.emulate_media(reduced_motion="no-preference")
            report["rapid"] = page.evaluate(
                TRANSITION,
                {
                    "install": False,
                    "settle": True,
                    "rapid": [GRID_TAB, TRIANGLE_TAB, GRID_TAB, TRIANGLE_TAB],
                },
            )
            report["staged_themes"] = []
            for view, mode, scheme in (
                ("triangle", "system", "dark"),
                ("grid", "light", "dark"),
                ("triangle", "dark", "light"),
            ):
                page.locator(f'[data-atlas-tab="{view}"]').click()
                page.evaluate(TRANSITION, {"install": False, "settle": True})
                page.emulate_media(color_scheme=scheme)
                page.evaluate(THEME, {"scroll_top": True})
                page.locator(".site-theme-button").click()
                page.locator(f'[data-theme-choice="{mode}"]').click()
                report["staged_themes"].append(
                    {
                        **page.evaluate(THEME, {"scroll_top": False}),
                        "view": view,
                        "expected": scheme if mode == "system" else mode,
                    }
                )
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
                sync_api.expect(static_page.locator(TILES)).to_have_count(324)
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
    readings = seen[width]["pointer"]
    assert [reading["n"] for reading in readings] == [18, 36, 306, 324]
    for reading in readings:
        assert reading["opened"] == str(reading["n"])
        assert reading["drawing_width"] > 0
        assert reading["drawing_width"] == pytest.approx(reading["drawing_height"], abs=0.1)
        assert reading["row"] == int((reading["n"] - 1) ** 0.5) + 1
        assert reading["segment"] in ("grid", "non-grid")
        assert reading["source"].endswith(f"/n-{reading['n']}.svg")
        assert 0 <= reading["center_x"] <= reading["viewport_width"]
        assert reading["contained"]
        assert reading["page_overflow"] == 0, reading


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
        "papers",
        "report-your-results",
    ]
    assert home["main_titles"] == [
        "the-problem",
        "profiles",
        "visuals",
        "more-resources",
        "about-the-squares-project",
    ]
    assert len(home["section_title_styles"]) == 9
    selected = news_highlights.highlights(render_changelog.load())
    assert [heading["entry"] for heading in home["news_headings"]] == [
        entry["id"] for entry in selected
    ]
    assert len(home["news_headings"]) == len(selected)
    assert all(heading["title"] for heading in home["news_headings"])
    assert [heading["href"] for heading in home["paper_headings"]] == [
        paper.href for paper in (*overview_sections.PAPERS[-2:], overview_sections.PAPERS[0])
    ]
    assert all(heading["title"] for heading in home["paper_headings"])
    assert home["other_lower_headings"] == []
    assert all(style == home["main_title_style"] for style in home["section_title_styles"])
    assert home["recent_title"] == "Results"
    assert home["media"] == {
        "visuals": ["square-packings-324-20261008.pdf"],
    }
    assert home["legacy_pdf_anchor"]
    assert not home["scope_present"]
    assert home["actions"]
    for action in home["actions"]:
        assert action["transform"] == "uppercase", action
    download = seen[width]["download"]
    assert download["order"] == ["Download PDF", "View Visual Atlas"]
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
    assert seen[width]["about"]["main_titles"] == ["the-squares-project"]


@pytest.fixture(scope="module")
def results_navigation_seen(browser: Any) -> dict[int, dict[str, Any]]:
    """Follow the one complete Results action by keyboard and pointer."""
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
            all_results = page.locator("a[data-all-results]")
            sync_api.expect(all_results).to_have_text(
                re.compile("^View All Results$", re.IGNORECASE)
            )
            bounds = all_results.bounding_box()
            assert bounds is not None
            assert bounds["x"] >= 0
            assert bounds["x"] + bounds["width"] <= width
            all_results.focus()
            with page.expect_navigation(wait_until="load"):
                page.keyboard.press("Enter")
            destination = f"{origin}results.html?s=4#all-results"
            sync_api.expect(page).to_have_url(destination)
            sync_api.expect(
                page.get_by_role("heading", name="All Results", exact=True)
            ).to_be_visible()
            sync_api.expect(page.locator("#all-results")).to_be_in_viewport()
            keyboard_destination = page.url
            page.goto(f"{origin}index.html?s=4", wait_until="load")
            all_results = page.locator("a[data-all-results]")
            bounds = all_results.bounding_box()
            assert bounds is not None
            assert bounds["x"] >= 0
            assert bounds["x"] + bounds["width"] <= width
            with page.expect_navigation(wait_until="load"):
                all_results.click()
            sync_api.expect(page).to_have_url(destination)
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
def test_results_action_reaches_complete_archive_by_keyboard_and_pointer(
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
def test_native_svg_follows_live_system_light_dark_choices_in_both_views(
    seen: dict[int, dict[str, Any]], width: int
) -> None:
    readings = seen[width]["themes"]
    assert len(readings) == 8
    for state in readings:
        assert state["resolved"] == state["expected"]
        assert state["cases"] == 324
        assert state["background"] == state["page_background"]
        assert state["white_samples"] > 0, state
        assert state["colored_samples"] > 0, state
        assert state["label_contrast"] >= 4.5, state
        assert state["palette_samples"] >= 5
        assert state["palette_unchanged"]
        assert state["filter"] == "none"
    for phase in ("triangle", "grid"):
        colors = {tuple(state["background"]) for state in readings if state["phase"] == phase}
        assert len(colors) == 2, phase
        pixels = {state["palette_signature"] for state in readings if state["phase"] == phase}
        assert len(pixels) == 1, phase


@pytest.mark.parametrize("width", WIDTHS)
def test_missing_shared_engine_keeps_every_case_and_the_atlas_link_usable(
    browser: Any, payloads: dict[str, bytes], width: int
) -> None:
    """Without the views' script the homepage keeps its static atlas, every case shown
    and each a link, with no error; View Visual Atlas still opens the Atlas page. The
    status line that pointed a reader there, because the cases after the first hundred
    could not be shown, went with the expander on 2026-10-22."""
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
        sync_api.expect(page.locator(TILES)).to_have_count(324)
        failed = page.evaluate(STATE)
        assert failed["visible_cases"] == 324
        assert failed["prepared_cases"] == 324
        assert failed["busy"] is None
        assert page.url == f"{ORIGIN}index.html"

        assert errors == []
        page.locator(EXPLORE).click()
        sync_api.expect(page).to_have_url(f"{ORIGIN}atlas.html")
        sync_api.expect(page.locator("[data-atlas-grid]")).to_be_visible()
    finally:
        page.close()


@pytest.mark.parametrize("width", WIDTHS)
def test_every_case_and_the_atlas_link_stay_usable_without_javascript(
    browser: Any, payloads: dict[str, bytes], width: int
) -> None:
    sync_api = site_browser.api()
    page = browser.new_page(viewport={"width": width, "height": 900}, java_script_enabled=False)
    _serve(page, payloads)
    try:
        page.goto(f"{ORIGIN}index.html", wait_until="load")
        sync_api.expect(page.locator(TILES)).to_have_count(324)
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
        selected = news_highlights.highlights(render_changelog.load())
        assert preview["entries"] == [entry["id"] for entry in selected]
        title_link = page.locator(".site-news-header > h3 > a").first
        anchor = render_changelog.entry_anchor(selected[0]["id"])
        sync_api.expect(title_link).to_have_attribute("href", f"news.html#{anchor}")
        title_link.click()
        page.wait_for_url(f"{ORIGIN}news.html#{anchor}")
        page.locator('button[data-news-score="3"]').click()
        news = page.evaluate(NEWS)
        if screenshot_dir := os.environ.get("SQPACK_NEWS_SCREENSHOT_DIR"):
            page.locator("[data-news-day]:visible").first.screenshot(
                path=str(Path(screenshot_dir) / f"news-card-{width}.png")
            )
        document = render_changelog.load()
        entries = render_changelog.news_entries(document)
        assert len(news["entries"]) == len(entries)
        assert len(news["days"]) == len(entries)
        assert news["heading"]["transform"] == "uppercase"
        assert news["family"] == news["heading"]["family"]
        footer = news["archive_action"]
        assert footer is not None
        assert footer["family"] == news["family"]
        assert footer["arrow"] == "external"
        assert footer["label"] == "Full changelog on GitHub"
        assert footer["href"] == f"{document['repository']}/blob/main/CHANGELOG.md"
        assert preview["reference_article_title"] is not None
        for surface in (preview, news):
            assert surface["reference_prose"] is not None
            assert surface["overflow"] == 0
            for day in surface["days"]:
                assert day["border"] == 1
                assert 0 <= day["left"] < day["right"] <= width
                assert day["family"] == surface["family"]
                assert day["body_family"] == surface["reference_prose"]["family"]
                assert day["body_family"] != surface["family"]
                for role in ("size", "weight", "leading"):
                    assert day["body_style"][role] == surface["reference_prose"][role]
                assert day["metadata_families"]
                assert set(day["metadata_families"]) == {surface["family"]}
                assert day["date_family"] == surface["family"]
                assert set(day["metadata_colors"]) == {day["date_color"]}
                assert day["date_color"] != surface["text_color"]
                assert day["body_style"]["color"] == surface["text_color"]
                if day["prose_records_gap"] is not None:
                    assert 16 <= day["prose_records_gap"] <= 20
                for padding in day["prose_padding"].values():
                    assert 0 < padding <= 6
                assert day["date_transform"] == "none"
                assert day["title_style"] == preview["reference_article_title"]
                assert day["headline_style"] == day["title_style"]
                assert day["title_style"]["color"] == surface["text_color"]
                assert day["title_before_date"]
                assert day["date_before_topics"]
                assert day["metadata_after_date"]
                for gap in ("title_date_gap", "date_metadata_gap"):
                    assert 0 <= day[gap] <= 7, (day["id"], gap, day[gap])
                assert 8 <= day["metadata_body_gap"] <= 12
                if day["paragraph_gap"] is not None:
                    assert 4 <= day["paragraph_gap"] <= 12
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
        archive_days = {day["id"]: day for day in news["days"]}
        for day in preview["days"]:
            assert day["topic_styles"] == archive_days[day["id"]]["topic_styles"]
            assert day["headline_style"] == archive_days[day["id"]]["headline_style"]
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
        entry = next(item for item in entries if item["id"] == entry_id)
        assert meaning is not None
        score = entry["significance"]["score"]
        # A News post's level is described by the rubric that scored it, not the results
        # ladder, and without the post's own rationale (`think-yznf`).
        news_level = render_changelog.news_significance_meanings()[score]
        assert meaning == f"Significance S{score}: {news_level}."
        assert news_level != overview_sections.rung_meanings()[f"S{score}"]
        assert len(meaning) <= 120
        assert entry["significance"]["rationale"] not in meaning
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
        if screenshot_dir := os.environ.get("SQPACK_NEWS_SCREENSHOT_DIR"):
            card.screenshot(path=str(Path(screenshot_dir) / f"news-card-expanded-{width}.png"))
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
        anchor = render_changelog.entry_anchor(entries[0]["id"])
        scores = {4, 5, entries[0]["significance"]["score"]}
        page.goto(f"{ORIGIN}about.html#{anchor}", wait_until="load")
        page.wait_for_url(
            lambda address: (
                urlsplit(address)._replace(query="").geturl() == f"{ORIGIN}news.html#{anchor}"
            )
        )
        query = urlsplit(page.url).query
        if scores == {4, 5}:
            assert query == ""
        else:
            assert parse_qs(query, keep_blank_values=True) == {
                "news-s": [",".join(str(score) for score in sorted(scores))]
            }
        sync_api.expect(page.locator(f"#{anchor}")).to_be_visible()
        owner = page.locator(f"[data-news-day]#{anchor}")
        sync_api.expect(owner.locator(".site-news-expand")).to_have_attribute(
            "aria-expanded", "true"
        )
        forwarded = page.evaluate(NEWS_FILTERS)
        assert {int(score) for score in forwarded["scores"]} == scores
        target_card = next(card for card in forwarded["cards"] if card["id"] == anchor)
        assert target_card["visible"]
        assert target_card["full"]
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


def test_excluded_news_bookmarks_reach_the_retained_changelog(
    browser: Any, payloads: dict[str, bytes]
) -> None:
    sync_api = site_browser.api()
    document = render_changelog.load()
    targets = render_changelog.archived_news_targets(document)
    assert targets
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    _serve(page, payloads)
    page.route(
        f"{document['repository']}/blob/main/CHANGELOG.md",
        lambda route: route.fulfill(body="<p>Retained project changelog</p>"),
    )
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    try:
        for surface in ("about.html", "news.html"):
            for anchor, target in targets.items():
                encoded = f"%{ord(anchor[0]):02X}{anchor[1:]}"
                for fragment in (anchor, encoded):
                    page.goto(f"{ORIGIN}{surface}#{fragment}", wait_until="load")
                    sync_api.expect(page).to_have_url(target)
            malformed = f"{ORIGIN}{surface}#%E0%A4%A"
            page.goto(malformed, wait_until="load")
            sync_api.expect(page).to_have_url(malformed)
        assert errors == []
    finally:
        page.close()


@pytest.mark.parametrize("width", WIDTHS)
def test_news_facets_history_bookmarks_and_shared_meters(
    browser: Any, payloads: dict[str, bytes], width: int, request: pytest.FixtureRequest
) -> None:
    sync_api = site_browser.api()
    document = render_changelog.load()
    entries = render_changelog.news_entries(document)
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
            for entry in entries
            if entry["significance"]["score"] in scores
            and (topics is None or topics.intersection(entry.get("topics", [])))
        }

    def check(scores: set[int], topics: set[str] | None = None) -> dict[str, Any]:
        seen = state()
        visible = {card["id"] for card in seen["cards"] if card["visible"]}
        assert visible == expected(scores, topics)
        assert seen["count"] == f"{len(visible)} of {len(entries)} news items"
        assert seen["empty"] is (not visible)
        scored = [entry for entry in entries if entry["significance"]["score"] in scores]
        for topic, tally in seen["topic_tallies"].items():
            matches = sum(topic in entry.get("topics", []) for entry in scored)
            assert tally["tally"] == f" ({matches})"
            assert tally["name"] == f"{tally['label']} ({matches})"
        assert seen["all_buttons"] == 0
        assert len(seen["resets"]) == 1
        assert seen["resets"][0]["label"] == "Reset filters"
        assert seen["resets"][0]["appearance"]["border-top-width"] == "0px"
        assert seen["resets"][0]["appearance"]["border-bottom-width"] == "0px"
        for score, meaning in seen["score_tooltips"].items():
            description = render_changelog.news_significance_tooltip(int(score))
            assert meaning == f"Significance S{score}: {description}"
        assert parse_qs(urlsplit(page.url).query)["reader"] == ["kept"]
        assert seen["overflow"] == 0
        return seen

    def pressed_under_pointer(button: Any, topic: str, scheme: str) -> None:
        """A topic retains its neutral surface and colored ink when pressed. The
        visible check carries selection without moving the button (`think-slt2`)."""
        choice = {
            "chooser": '[aria-labelledby="news-topics-label"]',
            "choice": f'[data-news-topic="{topic}"]',
        }
        page.mouse.move(0, 0)
        button.hover()
        box = button.bounding_box()
        states = [page.evaluate(NEWS_FILTERS, choice)["chooser"]]
        for _ in range(2):
            button.tap() if width == 390 else button.click()
            states.append(page.evaluate(NEWS_FILTERS, choice)["chooser"])
            assert button.bounding_box() == box, (scheme, topic)
        fills = [state["appearance"]["background-color"] for state in states]
        assert len(set(fills)) == 1, (scheme, topic, fills)
        for state in states:
            pressed = state["pressed"] == "true"
            assert state["check_visible"] is pressed, (scheme, topic, state["pressed"])
            assert (
                state["appearance"]["background-color"] == state["chip"]["background-color"]
            ), (scheme, topic)
            if pressed:
                assert state["check_contrast"] >= 4.5, (scheme, topic, state["check_contrast"])

    def open_topics() -> None:
        trigger = page.locator("[data-site-filter-trigger]")
        if trigger.get_attribute("aria-expanded") != "true":
            trigger.click()

    def score_explanations_leave_the_filters_free() -> None:
        """An S button's explanation never lies over a filter control or the shown
        site header's links: hovered or focused, it opens above the filters and below
        the header, or below the filters where there is no room between, or the phone's
        bottom bar holds it, so the next click reaches the control under the pointer. A
        mouse press explains nothing, not even for a frame, and leaves the toggle to the
        button."""
        tooltip = page.locator(".site-rating-tooltip.kpress-tooltip-visible")
        for score in (3, 4, 5):
            button = page.locator(f'button[data-news-score="{score}"]')
            page.mouse.move(0, 0)
            page.evaluate(TOOLTIP_WATCH, {"watch": True})
            for _ in range(2):
                button.click()
            assert page.evaluate(TOOLTIP_WATCH) is False, score
            page.keyboard.press("Escape")
            page.locator("h1").first.click()
            page.keyboard.press("Tab")
            button.focus()
            sync_api.expect(tooltip).to_be_visible()
            clear = page.evaluate(TOOLTIP_CLEAR)
            assert clear["covers"] == clear["covers_header"] == [], ("focus", score, clear)
            page.keyboard.press("Escape")
            topics = page.locator("[data-site-filter-trigger]").all()
            for topic in topics:
                page.mouse.move(0, 0)
                button.hover()
                sync_api.expect(tooltip).to_be_visible()
                clear = page.evaluate(TOOLTIP_CLEAR)
                assert clear["covers"] == clear["covers_header"] == [], ("hover", score, clear)
                box = topic.bounding_box()
                assert box is not None
                expanded = topic.get_attribute("aria-expanded")
                page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                assert topic.get_attribute("aria-expanded") != expanded, (score, clear)
                topic.click()
                assert topic.get_attribute("aria-expanded") == expanded
        if width != 1280:
            return
        # Scrolled down and then back up, the header shows, and with the filters 120 px
        # from the window's top the only room above them is over the header's links.
        for offset in (-300, -100, 50, 100, 120):
            page.evaluate(SCROLL_FILTERS, offset)
            page.wait_for_timeout(100)
        for score in (3, 4, 5):
            page.mouse.move(0, 0)
            page.keyboard.press("Escape")
            page.locator(f'button[data-news-score="{score}"]').hover()
            sync_api.expect(tooltip).to_be_visible()
            clear = page.evaluate(TOOLTIP_CLEAR)
            assert clear["header_bottom"] > 0, ("the header must show", clear)
            assert clear["covers"] == clear["covers_header"] == [], ("band", score, clear)
        page.mouse.move(0, 0)
        page.keyboard.press("Escape")
        page.evaluate(SCROLL_FILTERS, 10_000)

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
                    '[data-news-score="3"]',
                ),
            ):
                page.goto(f"{ORIGIN}{surface}", wait_until="load")
                samples = {}
                for selection, choice in (("selected", chosen), ("unselected", other)):
                    control = page.locator(group).locator(choice).first
                    for interaction in ("normal", "hover", "focus"):
                        page.keyboard.press("Escape")
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
                            if name == "scores":
                                assert control.get_attribute("role") is None
                                score = int(control.get_attribute("data-news-score") or 0)
                                level = render_changelog.news_significance_tooltip(score)
                                sync_api.expect(
                                    page.locator(".site-rating-tooltip.kpress-tooltip-visible")
                                ).to_have_text(f"Significance S{score}: {level}")
                        samples[selection, interaction] = {
                            key: sample[key]
                            for key in ("appearance", "border", "gap", "height")
                        }
                appearances[name] = samples
            assert appearances["scores"] == appearances["home"], scheme
            request.node.user_properties.append(
                (f"chooser-{scheme}", str(appearances["home"]["selected", "normal"]))
            )
            page.keyboard.press("Escape")
            trigger = page.locator("[data-site-filter-trigger]")
            panel = page.locator("[data-site-filter-options]")
            assert trigger.get_attribute("aria-controls") == panel.get_attribute("id")
            sync_api.expect(panel).to_have_css("transition-duration", "0s")
            sync_api.expect(panel).to_be_hidden()
            assert page.locator("[data-site-filter-summary]").text_content() == "All"
            trigger.focus()
            page.keyboard.press("ArrowDown")
            all_topics = panel.locator("[data-site-filter-all]")
            sync_api.expect(all_topics).to_be_focused()
            page.keyboard.press("End")
            sync_api.expect(panel.locator("button").last).to_be_focused()
            page.keyboard.press("Home")
            sync_api.expect(all_topics).to_be_focused()
            page.keyboard.press("ArrowDown")
            first = panel.locator("button[data-news-topic]").first
            sync_api.expect(first).to_be_focused()
            page.keyboard.press("Space")
            assert first.get_attribute("aria-pressed") == "false"
            assert trigger.get_attribute("aria-expanded") == "true"
            page.keyboard.press("Space")
            assert first.get_attribute("aria-pressed") == "true"
            for button in panel.locator("button[data-news-topic]").all():
                topic = button.get_attribute("data-news-topic")
                assert topic
                pressed_under_pointer(button, topic, scheme)
            panel_box = panel.bounding_box()
            assert panel_box is not None
            assert panel_box["x"] >= 15
            assert panel_box["x"] + panel_box["width"] <= width - 15
            page.keyboard.press("Escape")
            sync_api.expect(panel).to_be_hidden()
            sync_api.expect(trigger).to_be_focused()
            open_topics()
            page.locator("h1").first.click()
            sync_api.expect(panel).to_be_hidden()
            open_topics()
            panel.locator("button").last.focus()
            page.keyboard.press("Tab")
            sync_api.expect(panel).to_be_hidden()
            sync_api.expect(page.locator("[data-news-reset]")).to_be_focused()
            palette = state()["news_topic_palette"]
            assert palette
            assert len({chip["background"] for chip in palette}) == 1
            assert all(chip["contrast"] >= 4.5 for chip in palette), palette
            assert len({chip["color"] for chip in palette}) > 1
            page.goto(f"{ORIGIN}news.html?news-topics=verification", wait_until="load")
            assert page.locator("[data-site-filter-summary]").text_content() == "Verification"
            open_topics()
            panel.locator('button[data-news-topic="optimality"]').click()
            assert page.locator("[data-site-filter-summary]").text_content().endswith("+1")
            assert trigger.get_attribute("aria-expanded") == "true"
            all_topics.click()
            assert page.locator("[data-site-filter-summary]").text_content() == "All"
            assert "news-topics" not in parse_qs(urlsplit(page.url).query)
            page.goto(f"{ORIGIN}news.html?news-topics=none", wait_until="load")
            assert page.locator("[data-site-filter-summary]").text_content() == "None"
            open_topics()
            all_topics.click()
            assert page.locator("[data-site-filter-summary]").text_content() == "All"
            seen = state()
            assert seen["groups"] == [
                {"name": "Significance", "hidden_legend": True, "tabs": 0},
                {"name": "Topics", "hidden_legend": True, "tabs": 0},
            ]
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
            if screenshot_dir := os.environ.get("SQPACK_NEWS_SCREENSHOT_DIR"):
                page.locator(".site-news-filters").screenshot(
                    path=str(Path(screenshot_dir) / f"news-chooser-{scheme}-{width}.png")
                )
            page.goto(f"{ORIGIN}results.html", wait_until="load")
            results_state = state()
            # Results and News topics share a neutral surface with distinct ink hues.
            assert len(set(results_state["topic_palette"].values())) > 1
            for key in ("font-family", "font-size", "font-weight", "line-height", "color"):
                assert news_count[key] == results_state["count_style"][key], (scheme, key)
        page.emulate_media(color_scheme="light")

    try:
        shared_chooser_contract()
        page.goto(f"{ORIGIN}news.html?reader=kept", wait_until="load")
        score_explanations_leave_the_filters_free()
        seen = check({4, 5})
        assert seen["scores"] == ["4", "5"]
        used_topics = {topic for entry in entries for topic in entry.get("topics", [])}
        assert set(seen["topics"]) == used_topics
        page.goto(
            f"{ORIGIN}news.html?reader=kept&news-topics=correction,audit,verification",
            wait_until="load",
        )
        seen = check({4, 5}, {"verification"})
        assert seen["topics"] == ["verification"]
        assert parse_qs(urlsplit(page.url).query)["news-topics"] == ["verification"]
        page.locator("[data-news-reset]").click()
        page.locator('button[data-news-score="3"]').focus()
        page.keyboard.press("Space")
        check({3, 4, 5})
        # A press is the button's own action, so its explanation steps aside rather than
        # cover the topic filters that follow it.
        sync_api.expect(
            page.locator(".site-rating-tooltip.kpress-tooltip-visible")
        ).to_have_count(0)
        open_topics()
        for topic in used_topics:
            if topic != "optimality":
                page.locator(f'button[data-news-topic="{topic}"]').click()
        check({3, 4, 5}, {"optimality"})
        page.locator('button[data-news-topic="verification"]').click()
        check({3, 4, 5}, {"optimality", "verification"})
        page.keyboard.press("Escape")
        sync_api.expect(page.locator("[data-site-filter-options]")).to_be_hidden()
        page.locator("[data-news-reset]").click()
        check({4, 5})
        open_topics()
        for topic in used_topics:
            page.locator(f'button[data-news-topic="{topic}"]').click()
        check({4, 5}, set())
        assert parse_qs(urlsplit(page.url).query)["news-topics"] == ["none"]
        page.locator("[data-news-reset]").click()
        check({4, 5})
        assert "news-topics" not in parse_qs(urlsplit(page.url).query)
        for score in (4, 5):
            button = page.locator(f'button[data-news-score="{score}"]')
            button.tap() if width == 390 else button.click()
        check(set())
        assert parse_qs(urlsplit(page.url).query)["news-s"] == ["none"]
        for score in (3, 4, 5):
            page.locator(f'button[data-news-score="{score}"]').click()
        check({3, 4, 5})
        page.locator("[data-news-reset]").click()
        check({4, 5})
        page.go_back(wait_until="load")
        check({3, 4, 5})
        page.go_forward(wait_until="load")
        check({4, 5})
        low = max(
            (entry for entry in entries if entry["significance"]["score"] < 4),
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


@pytest.mark.parametrize("width", WIDTHS)
def test_significance_meter_spacing_rejects_oversized_boxes(
    browser: Any, payloads: dict[str, bytes], width: int
) -> None:
    page = browser.new_page(viewport={"width": width, "height": 900}, reduced_motion="reduce")
    _serve(page, payloads)
    try:
        page.goto(f"{ORIGIN}news.html", wait_until="load")
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
            assert item["border_color"] == item["color"]
            assert item["side_space"] <= 0.7 * item["font"]
            assert item["fits"], item
            assert item["side_space"] >= 2 * (item["border"] + item["padding"]) - 0.5, item
            assert len(item["bars"]) == 5
            for bar in item["bars"]:
                assert bar["border"] == 1
                assert bar["height"] > 0.5 * item["font"]
                assert bar["width"] > 0.4 * item["font"]
                assert (bar["fill"] == "rgba(0, 0, 0, 0)") is (not bar["filled"])
        oversized = page.evaluate(NEWS_FILTERS, {"meters": specimens, "meterSize": "7em"})[
            "samples"
        ]
        assert all(item["side_space"] > 0.7 * item["font"] for item in oversized), (
            "the spacing probe must reject excessive meter whitespace",
            oversized,
        )
        crowded = page.evaluate(NEWS_FILTERS, {"meters": specimens, "meterSize": "3.6em"})[
            "samples"
        ]
        assert all(
            not item["fits"]
            or item["side_space"] < 2 * (item["border"] + item["padding"]) - 0.5
            for item in crowded
        ), ("the spacing probe must reject a meter its label and bars overflow", crowded)
    finally:
        page.close()


#: Every page that sets a compact chooser, and the kinds of control each must show. The
#: atlases are opened at a named size, which keeps the scroll from resizing their tiles.
CHOOSER_SURFACES = {
    "atlas.html?size=medium": {"tab"},
    "index.html?size=medium": {"tab"},
    "news.html": {"tab", "trigger", "reset"},
    "results.html": {"tab"},
}


@pytest.fixture(scope="module")
def doubled(browser: Any) -> Iterator[Any]:
    """The same Chromium laid out for a 2x screen. `--force-device-scale-factor` lays a
    page out in device pixels, as a Retina display does, so a font's ascent and the
    leading round there as they do for a reader on one; a context's
    `device_scale_factor` draws the 1x layout larger and rounds nothing differently."""
    launched = browser.browser_type.launch(
        executable_path=os.environ.get(BROWSER_OVERRIDE),
        args=[preview_site.FONT_RENDER_HINTING, "--force-device-scale-factor=2"],
    )
    yield launched
    launched.close()


@pytest.mark.parametrize("scale", [1, 2])
def test_every_compact_chooser_centers_its_capitals(
    browser: Any, payloads: dict[str, bytes], scale: int, request: pytest.FixtureRequest
) -> None:
    """Every compact chooser's words stand in the middle of their control, on the Atlas,
    the homepage, News and Results, at both widths and at 1x and 2x. The labels are set
    in capitals, so the middle of the capitals is what reads as the text's middle, and
    it is held to a quarter pixel.

    Set by the leading and the padding, the capitals sat 0.35px high at 1x and 0.86px
    high on a 2x screen, where the browser rounds the font's ascent and the half leading
    in device pixels (the owner, 2026-10-23). Each line is now trimmed to its capitals
    (`text-box`) and centered in a control 24px tall, the floor a tap target needs."""
    chromium = browser if scale == 1 else request.getfixturevalue("doubled")
    page = chromium.new_page(viewport={"width": WIDTHS[0], "height": 900})
    _serve(page, payloads)
    try:
        for path, kinds in CHOOSER_SURFACES.items():
            page.goto(f"{ORIGIN}{path}", wait_until="load")
            check_site_rendering.wait_for_fonts(page)
            for width in WIDTHS:
                page.set_viewport_size({"width": width, "height": 900})
                controls = page.evaluate(CHOOSER_LABELS)
                where = (path, width, scale)
                assert {control["kind"] for control in controls} == kinds, where
                for control in controls:
                    assert control["fontSize"] == pytest.approx(15.2 * 0.875, abs=0.01), where
                    assert control["height"] >= 24 - 0.01, (where, control)
                    assert control["words"], (where, control)
                    for word in control["words"]:
                        assert word["transform"] == "uppercase", (where, control)
                        assert abs(word["offset"]) <= 0.25, (where, control)
    finally:
        page.close()
