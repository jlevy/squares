"""Badge explanations share KPress placement, keyboard semantics and fetched DOM support."""

from __future__ import annotations

import mimetypes
import re
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

from devtools import (
    overview_sections,
    render_case_pages,
    render_overview,
    result_overview,
    site_assets,
)
from devtools.render_n11_lower_bounds_explainer import (
    kpress_client_js,
    kpress_css,
    kpress_static,
)
from sqpack.probes import probe
from tests import site_browser

ORIGIN = "http://ratings.test/"
READ = probe(Path(__file__).with_name("probes"), "site_rating_tooltips/read")
EDGE = probe(Path(__file__).with_name("probes"), "site_rating_tooltips/edge")
VENDOR_EDGE = probe(Path(__file__).with_name("probes"), "site_rating_tooltips/vendor_edge")
TIP = ".site-rating-tooltip.kpress-tooltip-visible"
PROPERTY_MEANINGS = (
    ("O", "optimal", "optimal packing"),
    ("=", "exact", "exact algebraic representation"),
    ("R", "rigid", "rigid packing"),
    ("≈", "numerical", "numerical representation"),
)
MARKS = "".join(
    result_overview.badge_glyph(glyph, style, meaning, named=True)
    for glyph, style, meaning in PROPERTY_MEANINGS
)
RATINGS = overview_sections.rung_legend(here=False, heading="Legend")
BODY = (
    f'<h1>Rating explanations</h1><p id="properties">{MARKS}</p>{RATINGS}'
    '<p><a id="fetch-case" href="cases/11.html" data-case="11">Open case 11</a></p>'
    f"{render_case_pages.case_popover()}"
    '<div style="height: 1500px"></div><table id="edge-table"><tbody><tr><td>'
    f"{overview_sections.significance_mark(5, overview_sections.rung_meanings()['S5'])}"
    '</td></tr></tbody></table><div style="height: 1000px"></div>'
)


@pytest.fixture(scope="module")
def browser() -> Iterator[Any]:
    with site_browser.api().sync_playwright() as driver:
        launched = site_browser.launch(driver)
        yield launched
        launched.close()


@pytest.fixture(scope="module")
def payloads() -> dict[str, bytes]:
    """Minimal actual shells and one fetched article, with no full case/site render."""
    ordinary = render_overview.kpress_page(
        BODY,
        name="ordinary.html",
        current="atlas",
        title="Ratings",
        description="Rating explanations.",
        toc=False,
        prepare_math=False,
        page_scripts=(render_overview.CASE_POPOVER_SCRIPT,),
    )
    static = render_overview.static_content_page(
        BODY,
        meta=render_overview.PageMeta("Ratings", "Rating explanations.", "static.html"),
        current="atlas",
    )
    documents = {"ordinary.html": ordinary.html, "static.html": static.html}
    shell = render_overview.nav_shell("visualize", root="")
    documents["workbench.html"] = (
        "<!doctype html><html data-kpress-viewport><head>"
        f'{shell.head}</head><body>{shell.header}<main class="kpress">{BODY}</main>'
        f"{shell.script}</body></html>"
    )
    for paper in (
        "n11-lower-bounds-explainer",
        "n11-optimality-review",
        "n11-threshold-bound-review",
        "packing-methods",
    ):
        template = (render_overview.TEMPLATES / f"{paper}-shell.html").read_text()
        values = {
            "KPRESS_CSS": kpress_css(kpress_static()),
            "SITE_NAV_CSS": render_overview.SITE_NAV_CSS.read_text(),
            "PAPER_TYPE_CSS": render_overview.PAPER_TYPE_CSS.read_text(),
            "SITE_NAV": render_overview.nav_html("papers"),
            "SITE_THEME": render_overview.THEME_SCRIPT.read_text(),
            "BODY_HTML": BODY,
            "KPRESS_CLIENT_SCRIPT": render_overview.kpress_client_script(),
            "SITE_KPRESS_CLIENT": render_overview.kpress_client_script(),
            "SITE_TOOLTIPS": render_overview.TOOLTIP_SCRIPT.read_text(),
        }
        if paper == "n11-lower-bounds-explainer":
            values["KPRESS_CLIENT_SCRIPT"] = kpress_client_js(kpress_static())
            values["BODY_HTML"] += (
                '<p><sup class="kpress-footnote-ref"><a id="footnote-ref" '
                'href="#fn-1">1</a></sup></p>'
                '<ol><li id="fn-1">Explainer footnote</li></ol>'
                '<pre class="kpress-code"><code>certificate = True</code></pre>'
            )
        documents[f"{paper}.html"] = re.sub(
            r"\{\{([A-Z_]+)\}\}",
            lambda match, values=values: values.get(match[1], ""),
            template,
        )
    article = (
        '<article class="site-case" data-case="11">'
        f'<h1 id="n-11">Case 11</h1><p id="fetched-properties">{MARKS}</p>{RATINGS}'
        "</article>"
    )
    documents["cases/11.html"] = render_overview.static_content_page(
        article,
        meta=render_overview.PageMeta("Case 11", "Fetched ratings.", "cases/11.html"),
        current="atlas",
    ).html
    files = site_assets.shared().assets.referenced(documents.values())
    return {
        **{name: html.encode() for name, html in documents.items()},
        **{f"assets/{name}": body for name, body in files.items()},
    }


def _serve(page: Any, payloads: dict[str, bytes]) -> None:
    page.set_default_timeout(6000)

    def answer(route: Any) -> None:
        path = route.request.url.removeprefix(ORIGIN)
        body = payloads.get(path)
        if body is None:
            route.fulfill(status=404, body="Missing fixture")
        else:
            media = mimetypes.guess_type(path)[0] or "application/octet-stream"
            route.fulfill(status=200, body=body, content_type=media)

    page.route(f"{ORIGIN}**", answer)


def _assert_tooltip(page: Any, selector: str, *, reduced: bool = True) -> dict[str, Any]:
    page.locator(TIP).wait_for(state="visible")
    seen = page.evaluate(READ, selector)
    assert seen["title"] is None
    assert seen["role"] == "img"
    assert seen["tab"] == "0"
    assert seen["described"]
    assert seen["active"] == 1
    assert seen["top_layer"]
    assert seen["unclipped"], seen
    assert seen["left"] >= 0
    assert seen["right"] <= seen["width"]
    assert seen["top"] >= 0
    assert seen["bottom"] <= seen["height"]
    assert seen["background"] != "rgba(0, 0, 0, 0)"
    assert seen["native_titles"] == 0
    assert all(seen["names"])
    if reduced:
        assert seen["transition"] == "0s"
    return seen


@pytest.mark.parametrize("width", [1280, 390])
def test_meaningful_keyboard_tooltips_work_in_every_shared_shell(
    browser: Any, payloads: dict[str, bytes], width: int
) -> None:
    for path in payloads:
        if not path.endswith(".html") or path.startswith("cases/"):
            continue
        page = browser.new_page(
            viewport={"width": width, "height": 900}, reduced_motion="reduce"
        )
        _serve(page, payloads)
        try:
            page.goto(f"{ORIGIN}{path}", wait_until="load")
            selector = '#properties [data-style="optimal"]'
            for _, style, meaning in PROPERTY_MEANINGS:
                selector = f'#properties [data-style="{style}"]'
                page.locator(selector).focus()
                seen = _assert_tooltip(page, selector)
                assert seen["text"] == meaning
            for label, meaning in overview_sections.rung_meanings().items():
                selector = (
                    f'.site-rung-legend .site-significance[data-level="{label[1:]}"]'
                    if label.startswith("S")
                    else f'.site-rung-fill[data-rung="{label[0]}"][data-level="{label[1:]}"]'
                )
                page.locator(selector).focus()
                seen = _assert_tooltip(page, selector)
                assert seen["text"].endswith(meaning)
                assert label in seen["name"]
            page.keyboard.press("Escape")
            page.locator(TIP).wait_for(state="hidden")
            assert page.locator(selector).get_attribute("aria-describedby") is None
            assert page.locator(selector).get_attribute("tabindex") == "0"
        finally:
            page.close()


@pytest.mark.parametrize("width", [1280, 390])
def test_fetched_case_tooltip_sits_above_the_popover_and_escape_keeps_the_case_open(
    browser: Any, payloads: dict[str, bytes], width: int
) -> None:
    page = browser.new_page(viewport={"width": width, "height": 900}, reduced_motion="reduce")
    _serve(page, payloads)
    try:
        page.goto(f"{ORIGIN}ordinary.html", wait_until="load")
        page.locator("#fetch-case").click()
        popup = page.locator("[data-case-popover]")
        badge = popup.locator('[data-style="numerical"]')
        badge.wait_for(state="visible")
        badge.focus()
        seen = _assert_tooltip(page, '[data-case-popover] [data-style="numerical"]')
        assert seen["text"] == "numerical representation"
        page.keyboard.press("Escape")
        assert popup.is_visible()
        assert badge.get_attribute("aria-describedby") is None
        page.keyboard.press("Escape")
        popup.wait_for(state="hidden")
    finally:
        page.close()


def test_table_badge_at_the_bottom_edge_keeps_its_full_explanation_in_view(
    browser: Any, payloads: dict[str, bytes]
) -> None:
    page = browser.new_page(viewport={"width": 1280, "height": 700}, reduced_motion="reduce")
    _serve(page, payloads)
    try:
        page.goto(f"{ORIGIN}ordinary.html", wait_until="load")
        bottom = page.evaluate(EDGE)
        assert bottom == pytest.approx(688, abs=1)
        _assert_tooltip(page, "#edge-table .site-significance")
        vendor_bottom = page.evaluate(VENDOR_EDGE)
        assert vendor_bottom > 700
        page.keyboard.press("Escape")
        page.evaluate(EDGE)
        seen = _assert_tooltip(page, "#edge-table .site-significance")
        assert seen["text"].endswith(overview_sections.rung_meanings()["S5"])
    finally:
        page.close()


def test_explainer_keeps_its_actual_footnote_preview_and_code_copy_runtime(
    browser: Any, payloads: dict[str, bytes]
) -> None:
    page = browser.new_page(reduced_motion="reduce")
    _serve(page, payloads)
    try:
        page.goto(f"{ORIGIN}n11-lower-bounds-explainer.html", wait_until="load")
        assert page.locator(".kpress-code-copy").count() == 1
        footnote = page.locator("#footnote-ref")
        footnote.focus()
        preview = page.locator(".kpress-tooltip-footnote.kpress-tooltip-visible")
        preview.wait_for(state="visible")
        assert "Explainer footnote" in preview.inner_text()
        selector = '#properties [data-style="optimal"]'
        page.locator(selector).focus()
        _assert_tooltip(page, selector)
        assert page.locator(".kpress-tooltip-footnote.kpress-tooltip-visible").count() == 0
        page.keyboard.press("Escape")
        footnote.focus()
        preview.wait_for(state="visible")
        assert "Explainer footnote" in preview.inner_text()
    finally:
        page.close()


def test_hover_transition_and_touch_badges_keep_the_enclosing_card_destination(
    browser: Any, payloads: dict[str, bytes]
) -> None:
    page = browser.new_page(
        viewport={"width": 1280, "height": 900}, reduced_motion="no-preference"
    )
    _serve(page, payloads)
    try:
        page.goto(f"{ORIGIN}ordinary.html", wait_until="load")
        selector = '#properties [data-style="rigid"]'
        page.locator(selector).hover()
        seen = _assert_tooltip(page, selector, reduced=False)
        assert seen["text"] == "rigid packing"
        assert "0.14s" in seen["transition"]
        page.locator(TIP).hover()
        page.wait_for_timeout(250)
        assert page.locator(TIP).is_visible()
        page.locator("h1").click()
        page.locator(TIP).wait_for(state="hidden")
    finally:
        page.close()
    touch = browser.new_page(viewport={"width": 320, "height": 700}, has_touch=True)
    _serve(touch, payloads)
    try:
        touch.goto(f"{ORIGIN}ordinary.html", wait_until="load")
        selector = '.site-rung-fill[data-rung="V"][data-level="5"]'
        touch.locator(selector).tap()
        seen = _assert_tooltip(touch, selector, reduced=False)
        assert "V5" in seen["text"]
        assert touch.url == f"{ORIGIN}ordinary.html"
        assert touch.locator("a.site-rung-legend").get_attribute("href") == (
            "all-results.html#verification-ladders"
        )
    finally:
        touch.close()


def test_source_titles_and_meanings_survive_without_javascript(
    browser: Any, payloads: dict[str, bytes]
) -> None:
    page = browser.new_page(java_script_enabled=False)
    _serve(page, payloads)
    try:
        page.goto(f"{ORIGIN}ordinary.html", wait_until="load")
        assert (
            page.locator(
                ".site-rung-legend .site-significance[title], "
                ".site-rung-legend .site-rung-fill[title]"
            ).count()
            == 17
        )
        assert page.locator('#properties [title="optimal packing"]').count() == 1
        assert page.locator(".site-rating-tooltip").count() == 0
    finally:
        page.close()
