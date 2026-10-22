"""Shared popover headers preserve full-page destinations and native close behavior."""

from collections.abc import Iterator
from dataclasses import replace
from pathlib import Path
from typing import Any

import pytest

from devtools import overview_sections, preview_site, render_contributors, render_overview
from sqpack.contributor_occurrences import load_occurrences
from sqpack.contributors import load_contributors
from sqpack.probes import probe
from tests import site_browser

LAYOUT = probe(Path(__file__).with_name("probes"), "popover_controls/layout")


@pytest.mark.parametrize("action", [None, ("#local", "Go to local section")])
def test_overlays_without_a_full_page_have_only_the_close_control(
    action: tuple[str, str] | None,
) -> None:
    detail = overview_sections.row_detail(
        "pop-local",
        name="Local",
        trigger="Local",
        label="Local",
        title="Local",
        body="<p>Local detail</p>",
        action=action,
    )
    assert "site-popover-expand" not in detail.popover
    assert 'class="site-popover-close"' in detail.popover


def test_full_page_header_and_footer_share_the_escaped_destination() -> None:
    detail = overview_sections.row_detail(
        "pop-result",
        name="Result",
        trigger="Result",
        label="Result",
        title="Result",
        body="<p>Detail</p>",
        action=("result/test.html?x=1&y=2", "Open Result Record"),
    )
    assert 'class="site-popover-expand"' in detail.popover
    assert detail.popover.count('href="result/test.html?x=1&amp;y=2"') == 2
    assert '<path d="M15 3h6v6"/>' in detail.popover
    assert '<path d="m3 21 7-7"/>' in detail.popover
    assert '<use href="#kpress-icon-x">' in detail.popover
    assert detail.popover.index('class="site-popover-expand"') < detail.popover.index(
        'class="site-popover-close"'
    )


@pytest.fixture(scope="module")
def browser() -> Iterator[Any]:
    with site_browser.api().sync_playwright() as driver:
        launched = site_browser.launch(driver)
        yield launched
        launched.close()


@pytest.fixture(scope="module")
def served(tmp_path_factory: pytest.TempPathFactory) -> Iterator[str]:
    result = overview_sections.row_detail(
        "pop-result",
        name="Result",
        trigger="Result",
        label="Result",
        title="Result",
        body="<p>Full record</p>",
        source="result/test.html",
        action=("result/test.html", "Open Result Record"),
    )
    plain = overview_sections.row_detail(
        "pop-local",
        name="Local",
        trigger="Local",
        label="Local",
        title="Local",
        body="<p>Local detail</p>",
    )
    card = overview_sections.card(
        "pop-document",
        "Document",
        "Document",
        "Read the full document.",
        href="reader.html",
        action="Expand document",
    )
    body = (
        '<h1>Header controls</h1><a id="case-link" href="cases/11.html" data-case="11">Case</a>'
        '<a id="profile-link" href="profiles/walter-stromquist.html">Profile</a>'
        '<table><tbody><tr id="result-row" '
        + result.attributes
        + "><td>"
        + result.trigger
        + '</td></tr><tr id="local-row" '
        + plain.attributes
        + "><td>"
        + plain.trigger
        + "</td></tr></tbody></table>"
        + result.popover
        + plain.popover
        + card
    )
    host = render_overview.kpress_page(
        body,
        name="index.html",
        title="Controls",
        description="Popover controls.",
        current="",
        toc=False,
        page_scripts=(render_overview.ROW_POPOVER_SCRIPT,),
    )
    case = (
        '<article class="site-case" data-case="11"><nav class="site-case-steps">'
        '<a href="cases/10.html" data-case-step="10" rel="prev">Previous case</a>'
        '<a href="cases/12.html" data-case-step="12" rel="next">Next case</a></nav>'
        "<h1>Case 11</h1>" + "<p>Retained case detail.</p>" * 100 + "</article>"
    )
    contributor = replace(
        load_contributors().by_id["walter-stromquist"],
        display_name="Walter Stromquist with a Long Contributor Display Name",
    )
    profile = render_contributors.contributor_article(
        contributor, load_occurrences().occurrences
    )
    articles = {
        "result/test.html": '<article class="site-result" data-result-overview="test">'
        "<h1>Result</h1><p>Full result record.</p>"
        '<a class="github-dynamic-check" href="https://github.com/owner/repo/blob/main/README.md">'
        "Source document</a></article>",
        "cases/11.html": case,
        "cases/12.html": case.replace('data-case="11"', 'data-case="12"'),
        "profiles/walter-stromquist.html": profile,
        "reader.html": "<article><h1>Document</h1><p>Complete document.</p></article>",
    }
    pages = [host]
    for name, article in articles.items():
        pages.append(
            render_overview.static_content_page(
                article,
                meta=render_overview.PageMeta("Record", "Record fixture.", name),
                current="",
            )
        )
    root = tmp_path_factory.mktemp("popover-controls")
    render_overview.write_site(root, pages)
    server = preview_site.serve(root, 0)
    try:
        yield f"http://127.0.0.1:{server.server_port}/"
    finally:
        server.shutdown()
        server.server_close()


@pytest.mark.parametrize("width", [320, 390, 1280])
def test_result_and_document_header_links_keep_native_navigation(
    browser: Any,
    served: str,
    width: int,
) -> None:
    page = browser.new_page(viewport={"width": width, "height": 900})
    page.set_default_timeout(5000)
    page.set_default_navigation_timeout(5000)
    try:
        for opener, panel_id in (
            ("#result-row", "pop-result"),
            ('.site-card[popovertarget="pop-document"]', "pop-document"),
        ):
            page.goto(served)
            if opener == "#result-row":
                page.locator(opener).press("Enter")
            else:
                page.locator(opener).click()
            panel = page.locator(f"#{panel_id}")
            panel.wait_for(state="visible")
            expand = panel.locator(".site-popover-expand")
            expected = panel.locator(".site-popover-actions > a").first.get_attribute("href")
            assert expand.get_attribute("href") == expected
            assert expand.get_attribute("aria-label")
            layout = panel.evaluate(LAYOUT)
            assert layout["expand"]["right"] <= layout["close"]["left"] + 0.5, layout
            assert layout["close"]["width"] == layout["expand"]["width"] >= 44, layout
            assert layout["expandIcon"] == layout["closeIcon"], layout
            assert layout["expandGlyphWidth"] > 0, layout
            assert layout["closeGlyphWidth"] > 0, layout
            assert layout["hitExpand"], layout
            assert layout["hitClose"], layout
            assert layout["pageWidth"] <= width, layout
            page.locator(f"#{panel_id} .site-popover-expand").click()
            site_browser.api().expect(page).to_have_url(served + expected)
    finally:
        page.close()


@pytest.mark.parametrize("width", [320, 390, 1280])
def test_case_and_profile_actions_follow_replacement_and_remain_navigable(
    browser: Any,
    served: str,
    width: int,
) -> None:
    page = browser.new_page(viewport={"width": width, "height": 900})
    page.set_default_timeout(5000)
    page.set_default_navigation_timeout(5000)
    try:
        page.goto(served)
        page.locator("#case-link").click()
        panel = page.locator("#pop-case")
        panel.locator('article[data-case="11"]').wait_for(state="visible")
        for n in (11, 12):
            expected = served + f"cases/{n}.html"
            assert panel.locator(".site-popover-expand").get_attribute("href") == expected
            assert panel.locator("[data-case-open]").get_attribute("href") == expected
            site_browser.api().expect(panel.locator(".site-popover-close")).to_be_focused()
            if n == 11:
                page.keyboard.press("ArrowRight")
                panel.locator('article[data-case="12"]').wait_for(state="visible")
        panel.locator(".site-popover-expand").click()
        site_browser.api().expect(page).to_have_url(served + "cases/12.html")
        page.goto(served)
        page.locator("#profile-link").click()
        panel = page.locator("#pop-contributor")
        panel.locator("article.site-contributor").wait_for(state="visible")
        assert not panel.evaluate(LAYOUT)["titleOverlapsControls"]
        expected = served + "profiles/walter-stromquist.html"
        assert panel.locator(".site-popover-expand").get_attribute("href") == expected
        assert panel.locator("[data-contributor-open]").get_attribute("href") == expected
        site_browser.api().expect(panel.locator(".site-popover-close")).to_be_focused()
        panel.locator(".site-popover-expand").click()
        site_browser.api().expect(page).to_have_url(expected)
        page.goto(served)
        page.locator("#local-row").press("Enter")
        assert page.locator("#pop-local .site-popover-expand").count() == 0
        page.keyboard.press("Escape")
        site_browser.api().expect(page.locator("#local-row")).to_be_focused()
    finally:
        page.close()
