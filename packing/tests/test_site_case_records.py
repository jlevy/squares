"""Complete canonical case pages and fetched overlays behave as the published site.

Frontier rows and atlas cells open the same prepared article in a popover, with
stepping and focus restoration. Each case URL serves its full article before scripts
run; ordinary links navigate between canonical pages, including without JavaScript.
Legacy case selectors resolve known records and unknown counts leave the index safe.
"""

from __future__ import annotations

import contextlib
import re
import socket
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

from devtools import render_case_pages, render_overview
from devtools.preview_site import serve
from sqpack.probes import probe
from tests import site_browser, site_renders

PROBES = Path(__file__).resolve().parent / "probes"
FIGURE = probe(PROBES, "case_popover_figure/figure")
CROSS = probe(PROBES, "case_popover_head/cross")
EXERCISED_CASES = (10, 11, 12, 13, 14, 17, 29, 32)


def _free_port() -> int:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return int(probe.getsockname()[1])


@pytest.fixture(scope="module")
def served(tmp_path_factory: pytest.TempPathFactory) -> Iterator[str]:
    """Publish real pages and only the eight case files these tests exercise."""
    root = Path(tmp_path_factory.mktemp("cases"))
    files = [
        site_renders.page("index.html"),
        site_renders.page("frontier.html"),
        site_renders.page(render_case_pages.CASES_PAGE),
        *(
            render_overview.Page(
                render_case_pages.case_url(n),
                site_renders.case_records()[render_case_pages.case_url(n)],
            )
            for n in EXERCISED_CASES
        ),
        *render_overview.forwarder_pages(),
    ]
    render_overview.write_site(root, files)
    server = serve(root, _free_port())
    try:
        yield f"http://127.0.0.1:{server.server_port}/"
    finally:
        server.shutdown()
        server.server_close()


@pytest.fixture(scope="module")
def browser() -> Iterator[Any]:
    sync_api = site_browser.api()
    with sync_api.sync_playwright() as driver:
        launched = site_browser.launch(driver)
        yield launched
        launched.close()


@contextlib.contextmanager
def _page(browser: Any, *, scripts: bool = True, width: int = 1280) -> Iterator[Any]:
    context = browser.new_context(
        java_script_enabled=scripts, viewport={"width": width, "height": 900}
    )
    try:
        yield context.new_page()
    finally:
        context.close()


def _shown_case(popover: Any) -> str | None:
    """The case the popover's record is, by its article."""
    return popover.locator("[data-case-body] article.site-case").get_attribute("data-case")


def test_a_frontier_row_opens_its_record_and_steps_to_the_next(
    browser: Any, served: str
) -> None:
    """Pressing a row anywhere opens the case popover on its record, the visual summary
    first, with the action to the record's own address; the right arrow key and the
    record's own step move it to the next case in place, and the row of the case shown
    reads as expanded; Escape closes it, every row reads as collapsed, and focus is back
    on the row that opened it. Enter on a row opens it too."""
    sync_api = site_browser.api()
    with _page(browser) as page:
        page.goto(f"{served}frontier.html", wait_until="load")
        row = page.locator("#n-12")
        row.scroll_into_view_if_needed()
        row.locator("td.site-thumb img").click()
        popover = page.locator("#pop-case")
        popover.locator("[data-case-body] article.site-case").wait_for()
        assert popover.is_visible()
        assert (
            popover.locator("[data-case-body]").get_attribute("data-kpress-prose-font")
            == "sans"
        )
        assert _shown_case(popover) == "12"
        assert row.get_attribute("aria-expanded") == "true"
        assert popover.locator(".site-case-summary figure svg").count() == 1
        assert popover.locator(".site-case-summary .site-atlas-gap").count() == 1
        action = popover.locator("[data-case-open]").get_attribute("href") or ""
        assert action.endswith("cases/12.html")
        # The record's links were written from its own directory and are rebased here.
        frontier_link = popover.locator('.site-case-links a:has-text("In the frontier")')
        assert (frontier_link.get_attribute("href") or "").endswith("frontier.html#n-12")
        page.keyboard.press("ArrowRight")
        popover.locator('[data-case-body] article.site-case[data-case="13"]').wait_for()
        assert row.get_attribute("aria-expanded") == "false"
        assert page.locator("#n-13").get_attribute("aria-expanded") == "true"
        popover.locator('[data-case-body] a[data-case-step="14"]').click()
        popover.locator('[data-case-body] article.site-case[data-case="14"]').wait_for()
        assert popover.is_visible()
        page.keyboard.press("Escape")
        assert not popover.is_visible()
        assert page.locator('tr[data-case-row][aria-expanded="true"]').count() == 0
        sync_api.expect(row).to_be_focused()
        page.keyboard.press("Enter")
        popover.locator('[data-case-body] article.site-case[data-case="12"]').wait_for()
        assert popover.is_visible()


def test_a_record_opens_a_case_its_prose_links_in_place(browser: Any, served: str) -> None:
    """A case file's link to another case file is marked for the case popover
    (`mark_case_links`): in the popover it loads that case in place, and the page stays
    where it is."""
    with _page(browser) as page:
        page.goto(f"{served}frontier.html", wait_until="load")
        page.locator("#n-13 td.site-col-n a").click()
        popover = page.locator("#pop-case")
        popover.locator('[data-case-body] article.site-case[data-case="13"]').wait_for()
        prose = popover.locator('[data-case-body] .site-case-prose a[data-case="32"]').first
        prose.scroll_into_view_if_needed()
        prose.click()
        popover.locator('[data-case-body] article.site-case[data-case="32"]').wait_for()
        assert page.url == f"{served}frontier.html"


def test_an_atlas_cell_opens_the_same_record(browser: Any, served: str) -> None:
    """A tile opens the case popover on its record; Escape closes it and focus is back
    on the tile."""
    sync_api = site_browser.api()
    with _page(browser) as page:
        page.goto(served, wait_until="load")
        page.locator("[data-atlas-grid]").scroll_into_view_if_needed()
        cell = page.locator('.site-atlas-cell[data-case="11"]')
        cell.wait_for()
        cell.click()
        popover = page.locator("#pop-case")
        popover.locator('[data-case-body] article.site-case[data-case="11"]').wait_for()
        assert popover.is_visible()
        assert popover.locator(".site-case-summary figure svg").count() == 1
        page.keyboard.press("Escape")
        assert not popover.is_visible()
        sync_api.expect(cell).to_be_focused()


@pytest.mark.parametrize("width", [1280, 390])
@pytest.mark.parametrize("opener", ["frontier", "atlas"])
def test_the_popovers_drawing_fills_its_width_at_its_own_line_weight(
    browser: Any, served: str, opener: str, width: int
) -> None:
    """Opened from a frontier row or an atlas cell, on a laptop's window and a phone's,
    the case popover's drawing is square and as wide as the panel's body, short of the
    panel's height less 8rem (`think-u214`), and the page is no wider than the window.
    Its frame and outlines are drawn in the page's own units, as heavy as at the
    drawing's own share of its width up to 12rem across and no heavier (`think-pkz0`):
    2.3 and 1.1 pixels in a 700px drawing, not the 8.2 and 4.1 the drawing's own units
    would give them. Case 10's caption, side 3 + ½√2, keeps its radical, which the
    drawing's sizing once collapsed."""
    with _page(browser, width=width) as page:
        if opener == "frontier":
            page.goto(f"{served}frontier.html", wait_until="load")
            row = page.locator("#n-10")
            row.scroll_into_view_if_needed()
            row.locator("td.site-thumb img").click()
        else:
            page.goto(served, wait_until="load")
            page.locator("[data-atlas-grid]").scroll_into_view_if_needed()
            cell = page.locator('.site-atlas-cell[data-case="10"]')
            cell.wait_for()
            cell.scroll_into_view_if_needed()
            cell.click()
        popover = page.locator("#pop-case")
        popover.locator('[data-case-body] article.site-case[data-case="10"]').wait_for()
        popover.locator(".site-case-figure > figcaption .katex svg").first.wait_for()
        drawn = page.evaluate(FIGURE)
        assert drawn is not None
        assert drawn["caption_math"], drawn
        assert min(drawn["caption_math"]) > 0.5 * drawn["rem"], drawn
        tallest = drawn["panel_height"] - 8 * drawn["rem"]
        assert drawn["width"] == pytest.approx(min(drawn["body"], tallest), abs=1), drawn
        assert drawn["height"] == pytest.approx(drawn["width"], abs=0.5), drawn
        if width == 1280:
            assert drawn["width"] == pytest.approx(tallest, abs=1), drawn
            assert drawn["width"] > 1.5 * 24 * drawn["rem"], drawn
        else:
            assert drawn["width"] == pytest.approx(drawn["body"], abs=1), drawn
        assert drawn["frame_effect"] == drawn["outline_effect"] == "non-scaling-stroke"
        lines = min(drawn["width"], 12 * drawn["rem"])
        assert drawn["frame"] == pytest.approx(lines * 1.2 / 102, abs=0.01), drawn
        assert drawn["outline"] == pytest.approx(lines * 0.6 / 102, abs=0.01), drawn
        assert drawn["page_width"] <= drawn["window_width"], drawn
        assert drawn["popover_right"] <= drawn["window_width"], drawn


@pytest.mark.parametrize("width", [1280, 390])
def test_the_popovers_cross_stands_in_its_corner_clear_of_the_steps(
    browser: Any, served: str, width: int
) -> None:
    """On a laptop's window and a phone's, the case popover's close cross stands inside
    the panel at its corner, and the record's steps end before it: the next case's link
    once ended under the cross, which the card's horizontal inset, read by the sticky
    cross as a second limit, had set a padding's width in from the corner
    (`think-0dxa`)."""
    with _page(browser, width=width) as page:
        page.goto(f"{served}frontier.html", wait_until="load")
        row = page.locator("#n-10")
        row.scroll_into_view_if_needed()
        row.locator("td.site-thumb img").click()
        popover = page.locator("#pop-case")
        popover.locator('[data-case-body] article.site-case[data-case="10"]').wait_for()
        head = page.evaluate(CROSS)
        assert head is not None
        assert head["cross_right"] <= head["panel_right"] + 0.5, head
        assert head["panel_right"] - head["cross_right"] <= 16, head
        assert head["next_right"] <= head["cross_left"] + 0.5, head


def _canonical_case(page: Any, n: int) -> None:
    """The complete article, prepared math and identity at a case's own URL."""
    article = page.locator(f'article.site-case[data-case="{n}"]')
    article.wait_for(state="visible")
    assert page.locator("h1").count() == 1
    assert article.locator("h1#case-title").inner_text().startswith(f"n = {n}")
    assert page.title() == render_overview.page_title(
        f"{n} Unit Squares in a Square: Bounds and Best Packing"
    )
    assert page.locator('link[rel="canonical"]').get_attribute("href") == (
        render_overview.canonical_url(render_case_pages.case_url(n))
    )
    assert article.locator('[data-kpress-math-prepared="true"] .katex-html').count() > 0
    assert article.locator(".kpress-math-semantic math").count() > 0


@pytest.mark.parametrize("scripts", [True, False])
@pytest.mark.parametrize("width", [1280, 390])
def test_a_record_file_serves_its_complete_page_and_navigates_ordinary_links(
    browser: Any, served: str, *, scripts: bool, width: int
) -> None:
    """Canonical articles are present in the initial response; next/back/index
    navigation works on desktop and phone with and without JavaScript."""
    with _page(browser, scripts=scripts, width=width) as page:
        documents: list[str] = []
        page.on(
            "request",
            lambda request: (
                documents.append(request.url) if request.resource_type == "document" else None
            ),
        )
        address = f"{served}cases/11.html"
        response = page.goto(address, wait_until="load")
        assert response is not None
        assert response.status == 200
        initial = response.text()
        assert re.search(r'<article\b[^>]*\bdata-case="11"', initial)
        assert 'data-kpress-math-prepared="true"' in initial
        assert documents == [address]
        assert page.url == address
        _canonical_case(page, 11)
        page.locator('article.site-case a[data-case-step="12"]').click()
        page.wait_for_url(f"{served}cases/12.html", wait_until="load")
        assert documents[-1] == f"{served}cases/12.html"
        _canonical_case(page, 12)
        page.go_back(wait_until="load")
        assert page.url == address
        _canonical_case(page, 11)
        page.locator("article.site-case a[data-case-index]").click()
        page.wait_for_url(f"{served}cases/", wait_until="load")
        assert page.locator("h1#case-records").text_content() == "Case Records"
        assert page.locator("nav[data-case-index] a[data-case]").count() == 324
        assert page.locator('link[rel="canonical"]').get_attribute("href") == (
            render_overview.canonical_url(render_case_pages.CASES_PAGE)
        )


def test_the_old_one_page_address_arrives_at_the_complete_case(
    browser: Any, served: str
) -> None:
    with _page(browser) as page:
        page.goto(f"{served}cases.html#n-17", wait_until="load")
        page.wait_for_url(f"{served}cases/17.html", wait_until="load")
        _canonical_case(page, 17)


@pytest.mark.parametrize("scripts", [True, False])
def test_unknown_cases_leave_a_readable_index_or_404_and_do_not_trap_back(
    browser: Any, served: str, *, scripts: bool
) -> None:
    """An unknown selector stays on the complete index; a missing record returns
    HTTP 404 at its own address. Both preserve ordinary Back navigation."""
    with _page(browser, scripts=scripts) as page:
        page.goto(f"{served}frontier.html", wait_until="load")
        unknown = f"{served}cases/?n=999"
        response = page.goto(unknown, wait_until="load")
        assert response is not None
        assert response.status == 200
        assert page.url == unknown
        assert page.locator("h1#case-records").text_content() == "Case Records"
        assert page.locator("nav[data-case-index] a[data-case]").count() == 324
        assert page.locator("article.site-case").count() == 0
        page.go_back(wait_until="load")
        assert page.url == f"{served}frontier.html"
        missing = f"{served}cases/999.html"
        response = page.goto(missing, wait_until="load")
        assert response is not None
        assert response.status == 404
        assert page.url == missing
        page.go_back(wait_until="load")
        assert page.url == f"{served}frontier.html"


def test_without_scripts_a_record_file_is_read_where_it_is(browser: Any, served: str) -> None:
    with _page(browser, scripts=False) as page:
        response = page.goto(f"{served}cases/29.html", wait_until="load")
        assert response is not None
        assert response.status == 200
        assert re.search(r'<article\b[^>]*\bdata-case="29"', response.text())
        assert page.url == f"{served}cases/29.html"
        _canonical_case(page, 29)
        assert page.locator("article.site-case figure svg").count() == 1
