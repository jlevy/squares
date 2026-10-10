"""A fetched canonical result gives its dialog one title and one accessible name."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import replace
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest

from devtools import (
    overview_data,
    overview_sections,
    preview_site,
    render_overview,
    repo_links,
    site_assets,
    site_documents,
)
from sqpack.probes import probe
from tests import site_browser, site_renders

RESULT = "T-115"
PATH = "result/t-115.html"
POPOVER = "pop-result-t-115"
DOCUMENT_PATH = "conventions.html"
DOCUMENT_POPOVER = "pop-doc-conventions"
TITLE = probe(Path(__file__).with_name("probes"), "site_result_popover/title")
FOCUSED = probe(Path(__file__).with_name("probes"), "site_result_popover/focused")
HEADINGS = probe(Path(__file__).with_name("probes"), "site_result_popover/headings")


@pytest.fixture(scope="module")
def browser() -> Iterator[Any]:
    with site_browser.api().sync_playwright() as driver:
        launched = site_browser.launch(driver)
        yield launched
        launched.close()


@pytest.fixture(scope="module")
def served(tmp_path_factory: pytest.TempPathFactory) -> Iterator[str]:
    """A real result row and document card, rendering only their two target pages."""
    overview = site_renders.overview()
    result = next(result for result in overview.results if result.id == RESULT)
    detail = overview_sections.result_row(result, trigger=RESULT)
    document = next(doc for doc in site_documents.DOCUMENTS if doc.name == DOCUMENT_PATH)
    card = overview_sections.card(
        DOCUMENT_POPOVER,
        "conventions.md",
        document.title,
        document.description,
        href=document.name,
        action="Expand conventions.md",
    )
    body = (
        '<table><tbody><tr id="t-115" '
        f"{detail.attributes}><td>{detail.trigger}</td><td>Open result</td></tr>"
        f"</tbody></table>{detail.popover}"
        f'<div class="site-cards-frame"><div class="site-cards">{card}</div></div>'
    )
    start = render_overview.static_content_page(
        body,
        meta=render_overview.PageMeta(
            "Result title", "Result dialog title fixture.", "index.html"
        ),
        current="results",
    )
    script = site_assets.script_tag(
        site_assets.shared().assets.script_file(render_overview.ROW_POPOVER_SCRIPT),
        "index.html",
    )
    start = start._replace(html=start.html.replace("</body>", script + "</body>"))
    with patch.object(overview_data, "load", return_value=replace(overview, results=[result])):
        canonical = render_overview.result_fragments()[0]
    reader = site_documents.render_document(
        document, tree=repo_links.repository_tree(), report=site_documents.LinkReport()
    )
    root = tmp_path_factory.mktemp("result-popover")
    render_overview.write_site(root, [start, canonical, reader])
    server = preview_site.serve(root, 0)
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()


@pytest.mark.parametrize("width", [1280, 390])
def test_successful_article_fetch_replaces_outer_titles_and_names_the_dialog(
    browser: Any, served: str, width: int
) -> None:
    page = browser.new_page(viewport={"width": width, "height": 900}, reduced_motion="reduce")
    try:
        page.goto(f"{served}/{PATH}", wait_until="load")
        direct = page.locator("article.site-result > h1")
        direct_text = direct.inner_text()
        direct_math = direct.locator(".kpress-math-semantic mi").all_text_contents()
        assert direct_math == ["s", "n", "S", "n"]
        assert direct.get_attribute("id") == "t-115"
        page.goto(f"{served}/index.html", wait_until="load")
        page.locator("#t-115 td").last.click()
        heading = page.locator(f"#{POPOVER} article.site-result > h1")
        heading.wait_for(state="visible")
        found = page.evaluate(TITLE, POPOVER)
        assert found["outerTitles"] == 0, found
        assert found["titleCount"] == 1, found
        assert heading.inner_text() == direct_text
        assert found["math"] == direct_math
        assert found["mathTransforms"]
        assert set(found["mathTransforms"]) == {"none"}
        assert found["namedBy"] == found["titleID"]
        assert found["namedCount"] == 1
        assert found["namedInside"]
        assert found["duplicateIDs"] == [], found
        assert page.locator("#t-115").count() == 1
        page.keyboard.press("Escape")
        site_browser.api().expect(page.locator("#t-115")).to_have_attribute(
            "aria-expanded", "false"
        )
        assert page.locator("#t-115").evaluate(FOCUSED)
        page.locator("#t-115").press("Enter")
        assert page.evaluate(TITLE, POPOVER)["titleCount"] == 1
    finally:
        page.close()


def test_failed_fetch_keeps_a_meaningful_fallback_and_can_retry(
    browser: Any, served: str
) -> None:
    page = browser.new_page(reduced_motion="reduce")
    try:
        page.route(f"**/{PATH}", lambda route: route.abort())
        page.goto(f"{served}/index.html", wait_until="load")
        page.locator("#t-115 td").last.click()
        fallback = page.locator(f"#{POPOVER} > .site-popover-value")
        assert fallback.is_visible()
        found = page.evaluate(TITLE, POPOVER)
        assert found["namedCount"] == 1
        assert found["namedInside"]
        assert found["namedText"]
        assert found["duplicateIDs"] == []
        assert page.locator(f"#{POPOVER} > .site-card-label").inner_text() == RESULT
        page.locator(f"#{POPOVER} [data-row-pop-loading]").wait_for(state="detached")
        page.keyboard.press("Escape")
        page.unroute(f"**/{PATH}")
        page.locator("#t-115").press("Enter")
        page.locator(f"#{POPOVER} article.site-result > h1").wait_for(state="visible")
        assert page.evaluate(TITLE, POPOVER)["titleCount"] == 1
    finally:
        page.close()


def test_loading_article_retains_fallback_name_until_the_complete_title_arrives(
    browser: Any, served: str
) -> None:
    page = browser.new_page(reduced_motion="reduce")
    pending: list[Any] = []

    def hold(route: Any) -> None:
        pending.append(route)

    try:
        page.route(f"**/{PATH}", hold)
        page.goto(f"{served}/index.html", wait_until="load")
        page.locator("#t-115 td").last.click()
        found = page.evaluate(TITLE, POPOVER)
        assert len(pending) == 1
        assert found["outerTitles"] == 2
        assert found["namedInside"]
        assert found["namedText"]
        assert found["title"] is None
        assert found["duplicateIDs"] == []
        response = pending[0].fetch()
        pending[0].fulfill(response=response)
        page.locator(f"#{POPOVER} article.site-result > h1").wait_for(state="visible")
        assert page.evaluate(TITLE, POPOVER)["titleCount"] == 1
    finally:
        page.close()


def test_direct_result_page_keeps_its_complete_title_without_javascript(
    browser: Any, served: str
) -> None:
    page = browser.new_page(java_script_enabled=False)
    try:
        page.goto(f"{served}/index.html", wait_until="load")
        page.locator("#t-115 .site-row-open").click()
        page.wait_for_url(f"{served}/{PATH}")
        title = page.locator("article.site-result > h1")
        assert title.is_visible()
        assert RESULT in title.inner_text()
        assert title.get_attribute("id") == "t-115"
        assert title.locator(".kpress-math-semantic mi").all_text_contents() == [
            "s",
            "n",
            "S",
            "n",
        ]
    finally:
        page.close()


@pytest.mark.parametrize("width", [1280, 390])
def test_document_iframe_uses_compact_shared_headings_and_preserves_the_full_page(
    browser: Any, served: str, width: int
) -> None:
    page = browser.new_page(viewport={"width": width, "height": 900}, reduced_motion="reduce")
    try:
        page.goto(f"{served}/{DOCUMENT_PATH}", wait_until="load")
        standalone = page.evaluate(HEADINGS)
        assert standalone["view"] is None
        assert standalone["headings"][1]["fontStyle"] == "italic"
        page.goto(f"{served}/index.html", wait_until="load")
        page.locator(f'.site-card[popovertarget="{DOCUMENT_POPOVER}"]').click()
        iframe = page.locator(f"#{DOCUMENT_POPOVER} iframe").element_handle()
        assert iframe is not None
        frame = iframe.content_frame()
        assert frame is not None
        frame.locator(".site-page h1").wait_for(state="visible")
        frame.wait_for_load_state("load")
        embedded = frame.evaluate(HEADINGS)
        assert embedded["view"] == "embed"
        assert not embedded["navigationVisible"]
        assert len(embedded["headings"]) == 3
        for index, scale in enumerate((1.25, 1.1, 1.0)):
            heading = embedded["headings"][index]
            assert heading["text"] == standalone["headings"][index]["text"]
            assert heading["fontSize"] == pytest.approx(heading["parentFontSize"] * scale)
            assert heading["fontFamily"] == embedded["sansFamily"]
            assert heading["fontWeight"] == "550"
            assert heading["fontStyle"] == "normal"
            assert heading["textTransform"] == "none"
            assert heading["letterSpacing"] == "normal"
            assert heading["lineHeight"] == pytest.approx(heading["fontSize"] * 1.15)
        page.goto(f"{served}/{DOCUMENT_PATH}", wait_until="load")
        assert page.evaluate(HEADINGS) == standalone
    finally:
        page.close()
