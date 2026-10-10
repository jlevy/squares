"""The homepage's bounded previews, shared expansion and card geometry in Chromium.

Real rendered pages and their assets are served through request routes in memory, so
the fixture writes no site output. One desktop and one mobile session exercise the
keyboard, prepared native tiles, shared triangle animation and a case link.
"""

from __future__ import annotations

import mimetypes
import os
from collections.abc import Iterator
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

import pytest

from devtools import overview_sections, render_overview, site_assets
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
ORIGIN = "http://homepage.test/"
TOGGLE = "[data-homepage-atlas-toggle]"
CELLS = "#homepage-atlas-cells"
TILES = f"{CELLS} .site-atlas-cell:visible"
GRAPHIC = overview_sections.ATLAS_COMPOSITE.name
STATUS = "[data-homepage-atlas-status]"
EXPLORE = '.site-homepage-atlas-actions a[href="atlas.html"]'
WIDTHS = (1280, 390)
LEGEND_WIDTHS = (*WIDTHS, 320)


@pytest.fixture(scope="module")
def payloads() -> dict[str, bytes]:
    """The actual homepage, complete Atlas, About and case 291 with their dependencies."""
    documents = {
        name: site_renders.html(name)
        for name in ("index.html", "atlas.html", "about.html", "all-results.html")
    }
    documents.update(
        {
            f"cases/{n}.html": site_renders.case_records()[f"cases/{n}.html"]
            for n in (18, 36, 291, 306, 324)
        }
    )
    assets = site_assets.shared().assets.referenced(documents.values())
    media = {hero for _, hero, *_ in overview_sections.ATLAS_CARDS}
    return {
        **{name: html.encode("utf-8") for name, html in documents.items()},
        **{f"assets/{name}": data for name, data in assets.items()},
        **render_overview.support_files(),
        GRAPHIC: overview_sections.ATLAS_COMPOSITE.read_bytes(),
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
def test_native_homepage_film_waits_for_click_and_main_headings_gain_half_a_rem(
    browser: Any, film_payloads: dict[str, bytes], width: int
) -> None:
    requests = []
    page = browser.new_page(viewport={"width": width, "height": 900})
    _serve(page, film_payloads)

    def intercept(route: Any) -> None:
        requests.append(route.request.url)
        route.abort()

    page.route(render_overview.FILM_URL, intercept)
    try:
        page.goto(f"{ORIGIN}index.html", wait_until="networkidle")
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
        assert len(state["headings"]) == 8
        for heading in state["headings"]:
            assert heading["above"] - heading["before"] == pytest.approx(
                state["extra_space"], abs=0.01
            )
        assert state["legend_above"] == 0
        with page.expect_request(render_overview.FILM_URL, timeout=5000):
            film.click(position={"x": 24, "y": state["height"] - 48})
        assert requests == [render_overview.FILM_URL]
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
    for phase, count in (("preview", 36), ("expanded", 324), ("collapsed", 36)):
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
def seen(browser: Any, payloads: dict[str, bytes]) -> dict[int, dict[str, Any]]:
    """Keep every reading from one compact session at each supported window width."""
    sync_api = site_browser.api()
    reports: dict[int, dict[str, Any]] = {}
    for width in WIDTHS:
        page = browser.new_page(viewport={"width": width, "height": 900})
        _serve(page, payloads)
        requests = _requests(page)
        report: dict[str, Any] = {}
        try:
            page.goto(f"{ORIGIN}index.html", wait_until="load")
            sync_api.expect(page.locator(TOGGLE)).to_be_visible()
            report["initial"] = page.evaluate(STATE)
            report["download"] = page.evaluate(DOWNLOAD_ACTION)
            legend_screenshot = os.environ.get("SQPACK_HOMEPAGE_LEGEND_SCREENSHOT")
            if width == WIDTHS[0] and legend_screenshot:
                recent = page.locator('h2[id="recent-results"]').bounding_box()
                legend = page.locator(".site-rung-legend").bounding_box()
                assert recent is not None
                assert legend is not None
                page.screenshot(
                    path=legend_screenshot,
                    full_page=True,
                    clip={
                        "x": 0,
                        "y": recent["y"] - 12,
                        "width": width,
                        "height": legend["y"] + legend["height"] - recent["y"] + 36,
                    },
                )
            screenshot = os.environ.get("SQPACK_HOMEPAGE_MEDIA_SCREENSHOT")
            if width == WIDTHS[0] and screenshot:
                scroll_y = page.evaluate(MEDIA_IMAGES)
                pdfs = page.locator('h2[id="pdfs"]').bounding_box()
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
            toggle = page.locator(TOGGLE)
            toggle.focus()
            page.keyboard.press("Enter")
            page.evaluate(TRANSITION, {"install": False, "settle": True})
            sync_api.expect(page.locator(TILES)).to_have_count(100)
            page.keyboard.press("Enter")
            page.evaluate(TRANSITION, {"install": False, "settle": True})
            sync_api.expect(page.locator(TILES)).to_have_count(324)
            sync_api.expect(toggle).to_be_enabled()
            report["expanded"] = page.evaluate(STATE)

            toggle.focus()
            page.keyboard.press("Space")
            page.evaluate(TRANSITION, {"install": False, "settle": True})
            sync_api.expect(page.locator(TILES)).to_have_count(36)
            report["collapsed"] = page.evaluate(STATE)
            page.keyboard.press("Enter")
            page.evaluate(TRANSITION, {"install": False, "settle": True})
            sync_api.expect(page.locator(TILES)).to_have_count(100)
            page.keyboard.press("Enter")
            page.evaluate(TRANSITION, {"install": False, "settle": True})
            sync_api.expect(page.locator(TILES)).to_have_count(324)
            report["cached"] = page.evaluate(STATE)
            report["atlas_requests"] = requests.count(f"{ORIGIN}{GRAPHIC}")
            report["expanded_pointer"] = _pointer_cases(page, (306, 324))

            tile = page.locator(f'{TILES}[data-case="291"]')
            tile.focus()
            page.keyboard.press("Enter")
            article = page.locator('#pop-case article.site-case[data-case="291"]')
            article.wait_for(state="visible")
            report["case"] = {
                "shown": article.get_attribute("data-case"),
                "action": page.locator("#pop-case [data-case-open]").get_attribute("href"),
                "address": page.url,
                "math_errors": article.locator("[data-kpress-math-error]").count(),
                "unprepared": article.locator(
                    '.kpress-math:not([data-kpress-math-rendered="true"])'
                ).count(),
            }
            page.keyboard.press("Escape")
            sync_api.expect(tile).to_be_focused()
            report["case_closed"] = not page.locator("#pop-case").is_visible()
            report["themes"] = _themes(page)
            page.goto(f"{ORIGIN}about.html", wait_until="load")
            report["about"] = page.evaluate(STATE)
        finally:
            page.close()
        reports[width] = report
    return reports


@pytest.mark.parametrize("width", WIDTHS)
def test_keyboard_expansion_uses_the_shared_triangle_without_click_requests(
    toggle_seen: dict[int, dict[str, Any]], width: int
) -> None:
    report = toggle_seen[width]
    initial = report["initial"]
    hero = report["hero"]
    assert [drawing["n"] for drawing in hero["drawings"]] == [53]
    assert hero["captions"] == [
        (
            "Best known packing for 53 identical squares. Colors indicate angle. "
            "Darker colors mean more common shared faces."
        )
    ]
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
    assert initial["cases"] == list(range(1, 37))
    assert initial["visible_cases"] == 36
    assert initial["svg"] == {"cards": 36, "rows": [0, 1], "viewbox": "60 174 216 252"}
    assert initial["stage"] == 36
    assert initial["view"] == "triangle"
    assert initial["toggle"]["name"] == "Show more: expand from 36 to 100 cases (10 rows)"
    assert initial["prepared_cases"] == 324
    assert initial["cells_role"] is None
    assert initial["toggle"]["expanded"] == "false"
    assert initial["toggle"]["label"] == "Show More"
    assert initial["toggle"]["arrow"] == "double-down"
    assert initial["toggle"]["controls"] == "homepage-atlas-cells"
    intermediate = report["intermediate"]
    assert intermediate["cases"] == list(range(1, 101))
    assert intermediate["stage"] == 100
    assert intermediate["toggle"]["expanded"] == "true"
    assert intermediate["toggle"]["label"] == "Show More"
    assert intermediate["toggle"]["arrow"] == "double-down"
    assert intermediate["toggle"]["name"] == "Show more: expand from 100 to 324 cases (18 rows)"
    for name in ("expanded", "cached"):
        state = report[name]
        assert state["cases"] == list(range(1, 325)), name
        assert state["visible_cases"] == 324, name
        assert state["toggle"]["expanded"] == "true", name
        assert state["toggle"]["label"] == "Show Less", name
        assert state["toggle"]["name"] == "Show less: collapse from 324 to 36 cases (6 rows)"
        assert state["toggle"]["arrow"] == "double-up", name
        assert not state["toggle"]["disabled"], name
        assert state["busy"] is None, name
        assert state["svg"] == {
            "cards": 324,
            "rows": list(range(18)),
            "viewbox": "60 174 216 252",
        }
        assert state["view"] == "triangle"
    collapsed = report["collapsed"]
    assert collapsed["cases"] == initial["cases"]
    assert collapsed["svg"] == initial["svg"]
    assert collapsed["toggle"]["expanded"] == "false"
    assert collapsed["toggle"]["label"] == "Show More"
    assert collapsed["toggle"]["arrow"] == "double-down"
    assert collapsed["toggle"]["focused"]
    assert collapsed["prepared_cases"] == 324
    assert collapsed["view"] == "triangle"
    for name in ("initial", "intermediate", "expanded", "collapsed", "cached"):
        assert report[name]["label_errors"] == [], name
        assert report[name]["raw_markup"] == 0, name
        assert {11, 12, 17, 18, 19, 20, 21}.issubset(report[name]["star_cases"]), name
    assert report["atlas_requests"] == 0
    for name in ("initial", "expanded", "collapsed", "cached"):
        assert report[name]["toggle"]["arrow_hidden"] == "true"
        assert report[name]["toggle"]["arrow_mask"] != "none"
        assert report[name]["toggle"]["arrow_width"] > 0
    for name, count in (
        ("intermediate_move", 100),
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
        assert transition["crop_errors"] == []
        assert transition["duration"] == 360
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
        assert transition["panel_role"] is None
        assert all(
            aspect == pytest.approx(216 / 252, abs=0.002) for aspect in transition["aspects"]
        )
    assert report["collapsed_move"]["input"]["same_nodes"]
    assert report["collapsed_move"]["toggle_in_view"]
    reduced = report["reduced_move"]
    assert reduced["input"]["count"] == 324
    assert reduced["input"]["same_nodes"]
    assert reduced["input"]["animations"] == []
    assert reduced["duration"] == 0
    assert reduced["placement_errors"] == []
    assert report["reduced_collapsed"]["input"]["count"] == 36
    assert report["reduced_collapsed"]["input"]["same_nodes"]
    assert report["reduced_collapsed"]["input"]["animations"] == []
    assert report["reduced_collapsed"]["toggle_in_view"]
    assert report["rapid"]["counts"][-3:] == [100, 324, 36]
    assert report["rapid"]["input"]["same_nodes"]
    assert report["rapid"]["placement_errors"] == []
    assert report["rapid"]["toggle_in_view"]
    assert report["static"]["overflow"] == 0
    static = report["static"]["tiles"]
    assert report["static_labels"]["raw_markup"] == 0
    assert report["static_labels"]["label_errors"] == []
    assert {11, 12, 17, 18, 19, 20, 21}.issubset(report["static_labels"]["star_cases"])
    assert [tile["n"] for tile in static] == list(range(1, 37))
    for index, tile in enumerate(static):
        assert tile["left"] >= -0.5
        assert tile["right"] <= report["static"]["width"] + 0.5
        for other in static[index + 1 :]:
            assert (
                tile["right"] <= other["left"] + 0.5
                or other["right"] <= tile["left"] + 0.5
                or tile["top"] + tile["height"] <= other["top"] + 0.5
                or other["top"] + other["height"] <= tile["top"] + 0.5
            ), (tile["n"], other["n"])
    assert [themed["cases"] for themed in report["staged_themes"]] == [36, 100, 324, 36]
    for themed in report["staged_themes"]:
        assert themed["resolved"] == themed["expected"]
        assert themed["background"] == themed["page_background"]
        assert themed["palette_unchanged"]
        assert themed["label_contrast"] >= 4.5
    assert urlsplit(report["late_case"]).path.lstrip("/") == "cases/291.html"


@pytest.fixture(scope="module")
def toggle_seen(browser: Any, request: pytest.FixtureRequest) -> dict[int, dict[str, Any]]:
    """The existing keyboard transitions without case-page or theme-matrix rendering."""
    sync_api = site_browser.api()
    reports = {}
    live = os.environ.get("SQPACK_SITE_PREVIEW_URL")
    origin = f"{live.rstrip('/')}/" if live else ORIGIN
    files = None
    if not live:
        documents = {
            f"cases/{n}.html": site_renders.case_records()[f"cases/{n}.html"] for n in (53, 291)
        }
        assets = site_assets.shared().assets.referenced(documents.values())
        files = {
            **request.getfixturevalue("film_payloads"),
            **{name: html.encode() for name, html in documents.items()},
            **{f"assets/{name}": data for name, data in assets.items()},
        }
    for width in WIDTHS:
        page = browser.new_page(viewport={"width": width, "height": 900})
        if files is not None:
            _serve(page, files)
        requests = _requests(page)
        try:
            page.goto(f"{origin}index.html", wait_until="load")
            sync_api.expect(page.locator(TOGGLE)).to_be_visible()
            report = {"initial": page.evaluate(STATE)}
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
                    path=str(Path(screenshot_dir) / f"homepage-triangle-36-{width}.png")
                )
            baseline = page.evaluate(TRANSITION, {"install": True, "settle": False})
            report["root_view"] = baseline["root_view"]
            report["root_size"] = baseline["root_size"]
            toggle = page.locator(TOGGLE)
            toggle.focus()
            page.evaluate(TRANSITION, {"install": False, "settle": True, "position": True})
            page.keyboard.press("Enter")
            report["intermediate_move"] = page.evaluate(
                TRANSITION, {"install": False, "settle": True}
            )
            sync_api.expect(page.locator(TILES)).to_have_count(100)
            report["intermediate"] = page.evaluate(STATE)
            if screenshot_dir:
                page.locator("[data-atlas-preview]").screenshot(
                    path=str(Path(screenshot_dir) / f"homepage-triangle-100-{width}.png")
                )
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
            sync_api.expect(page.locator(TILES)).to_have_count(36)
            report["collapsed"] = page.evaluate(STATE)
            page.keyboard.press("Enter")
            page.evaluate(TRANSITION, {"install": False, "settle": True})
            sync_api.expect(page.locator(TILES)).to_have_count(100)
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
                (36, "system", "light"),
                (100, "system", "dark"),
                (324, "light", "dark"),
                (36, "dark", "light"),
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
            toggle.click()
            page.evaluate(TRANSITION, {"install": False, "settle": True})
            late = page.locator(f'{TILES}[data-case="291"]')
            late.click()
            article = page.locator('#pop-case article[data-case="291"]')
            sync_api.expect(article).to_be_visible()
            report["late_case"] = page.locator("#pop-case [data-case-open]").get_attribute(
                "href"
            )
            page.keyboard.press("Escape")
            sync_api.expect(late).to_be_focused()
            report["atlas_requests"] = requests.count(f"{origin}{GRAPHIC}")
            static_page = browser.new_page(
                viewport={"width": width, "height": 900}, java_script_enabled=False
            )
            if files is not None:
                _serve(static_page, files)
            try:
                static_page.goto(f"{origin}index.html", wait_until="load")
                sync_api.expect(static_page.locator(TOGGLE)).to_be_hidden()
                sync_api.expect(static_page.locator(TILES)).to_have_count(36)
                sync_api.expect(static_page.locator(EXPLORE)).to_be_visible()
                report["static"] = static_page.evaluate(INITIAL_LAYOUT)
                report["static_labels"] = static_page.evaluate(STATE)
                report["static_hero"] = static_page.evaluate(HERO)
            finally:
                static_page.close()
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
            for name, expected in (
                ("left_gap", 24),
                ("top_gap", 12),
                ("link_width", 216),
                ("link_height", 252),
                ("drawing_width", 158),
                ("drawing_height", 158),
            ):
                # Compare in CSS pixels: fractional layout rounds the percentage
                # link bounds to subpixels, especially in the scrolled phone view.
                error = abs(reading[name] - expected) * reading["scale"]
                assert error <= 0.1, (phase, reading)
            assert 0 <= reading["center_x"] <= reading["viewport_width"]
            assert reading["contained"]
            assert reading["horizontal_scroll"] == 0, (phase, reading)


@pytest.mark.parametrize("width", WIDTHS)
def test_a_newly_inserted_case_opens_its_prepared_record_in_the_existing_popover(
    seen: dict[int, dict[str, Any]], width: int
) -> None:
    case = seen[width]["case"]
    assert case["shown"] == "291"
    assert case["action"] == f"{ORIGIN}cases/291.html"
    assert case["address"] == f"{ORIGIN}index.html"
    assert case["math_errors"] == case["unprepared"] == 0
    assert seen[width]["case_closed"]


@pytest.mark.parametrize("width", WIDTHS)
def test_homepage_order_chrome_and_single_card_rows_keep_the_shared_design(
    seen: dict[int, dict[str, Any]], width: int
) -> None:
    home = seen[width]["initial"]
    assert home["headings"] == [
        "the-atlas-of-square-packings",
        "recent-results",
        "papers",
        "pdfs",
        "video",
    ]
    assert home["main_titles"] == [
        "the-problem",
        "squares-project-documentation",
        "more-resources",
    ]
    assert len(home["section_title_styles"]) == 7
    assert home["lower_headings"] == 0
    assert all(style == home["main_title_style"] for style in home["section_title_styles"])
    assert home["recent_title"] == "Recent Major Results"
    assert home["media"] == {
        "pdfs": ["known-best-1-100.pdf", "known-best-1-324.pdf"],
        "video": [],
    }
    assert home["legacy_pdf_anchor"]
    assert not home["scope_present"]
    assert home["actions"]
    for action in home["actions"]:
        assert action["transform"] == "uppercase", action
    download = seen[width]["download"]
    assert download["order"] == ["Show More", "Download PDF", "Explore the atlas"]
    assert download["href"] == "known-best-1-324.pdf"
    assert download["download"]
    assert download["uppercase"] == "uppercase"
    assert download["icon"].startswith("url(")
    assert download["icon_hidden"] == "true"
    assert download["left"] >= 0
    assert download["right"] <= width
    assert home["solo_cards"]
    assert any("The Squares Project" in card["label"] for card in home["solo_cards"])
    for card in home["solo_cards"]:
        assert abs(card["center_offset"]) <= 1, card
    assert "squares-project-documentation" in seen[width]["about"]["main_titles"]


@pytest.mark.parametrize("width", LEGEND_WIDTHS)
def test_homepage_legend_is_centered_compact_and_keeps_every_rung(
    legend_seen: dict[int, dict[str, Any]], width: int
) -> None:
    home = legend_seen[width]["initial"]
    legend = home["legend"]
    assert legend is not None
    assert legend["title"] == "Legend"
    assert legend["transform"] == "uppercase"
    assert legend["style"] == "normal"
    assert legend["family"] == home["actions"][0]["family"]
    assert legend["size"] == legend["card_label_size"]
    assert legend["entries"] == [
        *(f"S{level}" for level in range(1, 6)),
        *(f"V{level}" for level in range(6)),
        *(f"C{level}" for level in range(6)),
    ]
    assert legend["paragraphs"] == 4
    assert legend["lines"] == [
        ["Significance"],
        ["Verification"],
        ["Confirmation"],
        ["new result"],
    ]
    assert not legend["helper_text"]
    rows = legend["rows"]
    assert max(row["icon_left"] for row in rows) - min(row["icon_left"] for row in rows) <= 0.5
    assert (
        max(row["label_left"] for row in rows) - min(row["label_left"] for row in rows) <= 0.5
    )
    for row in rows:
        assert row["label_left"] >= row["icon_right"] + 15
        assert abs(row["center_offset"]) <= 1
    assert legend["title_align"] == "center"
    assert abs(legend["title_center_offset"]) <= 1
    assert legend["star"]
    assert legend["detail"] == "all-results.html#verification-ladders"
    assert legend["shared_card"]
    assert legend["destination_kind"] == "page"
    assert legend["nested_links"] == 0
    assert legend["accessible_name"] == (
        "Legend: what the significance, verification and confirmation ratings mean"
    )
    assert abs(legend["center_offset"]) <= 1
    assert legend["width"] <= 52 * legend["rem"] + 1
    if width == WIDTHS[0]:
        assert legend["width"] < legend["table_width"]
    else:
        assert legend["left"] >= 0
        assert legend["right"] <= width
        assert legend["scroll_width"] <= legend["client_width"]


@pytest.fixture(scope="module")
def legend_seen(browser: Any, request: pytest.FixtureRequest) -> dict[int, dict[str, Any]]:
    """Measure the linked legend without repeating the Atlas/theme interaction matrix."""
    sync_api = site_browser.api()
    readings = {}
    live = os.environ.get("SQPACK_SITE_PREVIEW_URL")
    origin = f"{live.rstrip('/')}/" if live else ORIGIN
    payloads = request.getfixturevalue("payloads") if not live else None
    for width in LEGEND_WIDTHS:
        page = browser.new_page(viewport={"width": width, "height": 900})
        if payloads is not None:
            _serve(page, payloads)
        try:
            page.goto(f"{origin}index.html", wait_until="load")
            initial = page.evaluate(STATE)
            screenshot = os.environ.get("SQPACK_HOME_LEGEND_SCREENSHOT_DIR")
            if screenshot:
                page.locator("a.site-rung-legend").screenshot(
                    path=str(Path(screenshot) / f"homepage-legend-{width}.png")
                )
            card = page.get_by_role(
                "link",
                name=(
                    "Legend: what the significance, verification and confirmation ratings mean"
                ),
                exact=True,
            )
            card.focus()
            sync_api.expect(card).to_be_focused()
            with page.expect_navigation(wait_until="load"):
                page.keyboard.press("Enter")
            destination = f"{origin}all-results.html#verification-ladders"
            sync_api.expect(page).to_have_url(destination)
            target = page.locator("#verification-ladders")
            sync_api.expect(target).to_have_text("Verification Ladders")
            sync_api.expect(target).to_be_in_viewport()
            sync_api.expect(page.locator("div.site-rung-legend[role=note]")).to_have_count(1)
            sync_api.expect(page.locator(".site-rung-legend-heading")).to_have_count(0)
            keyboard_destination = page.url
            page.goto(f"{origin}index.html", wait_until="load")
            with page.expect_navigation(wait_until="load"):
                page.locator("a.site-rung-legend > p").last.click()
            sync_api.expect(page).to_have_url(destination)
            sync_api.expect(page.locator("#verification-ladders")).to_be_in_viewport()
            readings[width] = {
                "initial": initial,
                "keyboard_destination": keyboard_destination,
                "pointer_destination": page.url,
                "destination": destination,
            }
        finally:
            page.close()
    return readings


@pytest.mark.parametrize("width", LEGEND_WIDTHS)
def test_whole_legend_card_reaches_the_existing_ladders_with_keyboard_and_pointer(
    legend_seen: dict[int, dict[str, Any]], width: int
) -> None:
    reading = legend_seen[width]
    assert not reading["initial"]["scope_present"]
    destination = reading["destination"]
    assert reading["keyboard_destination"] == destination
    assert reading["pointer_destination"] == destination


@pytest.mark.parametrize("width", WIDTHS)
def test_native_svg_follows_live_system_light_dark_choices_in_all_cached_states(
    seen: dict[int, dict[str, Any]], width: int
) -> None:
    readings = seen[width]["themes"]
    assert len(readings) == 12
    for state in readings:
        assert state["resolved"] == state["expected"]
        assert state["cases"] == (324 if state["phase"] == "expanded" else 36)
        assert state["background"] == state["page_background"]
        assert state["container"] == state["background"]
        assert state["outline"] == state["grid"] == state["label"]
        assert state["label_contrast"] >= 4.5, state
        assert state["palette_samples"] >= 5
        assert state["palette_unchanged"]
        assert state["filter"] == "none"
    for phase in ("preview", "expanded", "collapsed"):
        colors = {tuple(state["background"]) for state in readings if state["phase"] == phase}
        assert len(colors) == 2, phase


@pytest.mark.parametrize("width", WIDTHS)
def test_failed_startup_preparation_keeps_native_preview_and_explore_usable(
    browser: Any, payloads: dict[str, bytes], width: int
) -> None:
    sync_api = site_browser.api()
    page = browser.new_page(viewport={"width": width, "height": 900})
    broken = payloads["index.html"].replace(
        b"<template data-homepage-atlas-gzip>", b"<template data-homepage-atlas-gzip>!"
    )
    _serve(page, {**payloads, "index.html": broken})
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
        assert failed["visible_cases"] == 36
        assert failed["toggle"]["expanded"] == "false"
        assert failed["prepared_cases"] == 36
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
        sync_api.expect(page.locator(TILES)).to_have_count(36)
        sync_api.expect(page.locator(EXPLORE)).to_be_visible()
        page.locator(EXPLORE).click()
        sync_api.expect(page).to_have_url(f"{ORIGIN}atlas.html")
        sync_api.expect(page.locator("[data-atlas-grid]")).to_be_visible()
    finally:
        page.close()
