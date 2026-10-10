"""Complete canonical case pages and fetched overlays behave as the published site.

Frontier rows and atlas cells open the same prepared article in a popover, with
stepping and focus restoration. Each case URL serves its full article before scripts
run; ordinary links navigate between canonical pages, including without JavaScript.
Legacy case selectors resolve known records and unknown counts leave the index safe.
"""

from __future__ import annotations

import contextlib
import os
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
LAYOUT = probe(PROBES, "case_layout/read")
NAVIGATION = probe(PROBES, "case_navigation/read")
EXERCISED_CASES = (5, 10, 11, 12, 13, 14, 15, 16, 17, 29, 32, 53, 291, 324)


def _free_port() -> int:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return int(probe.getsockname()[1])


@pytest.fixture(scope="module")
def served(tmp_path_factory: pytest.TempPathFactory) -> Iterator[str]:
    """Use a live local preview, or publish only the case files these tests exercise."""
    if live := os.environ.get("SQPACK_SITE_PREVIEW_URL"):
        yield live.rstrip("/") + "/"
        return
    root = Path(tmp_path_factory.mktemp("cases"))
    files = [
        site_renders.page("index.html"),
        site_renders.page("atlas.html"),
        *(
            render_overview.Page(
                render_case_pages.case_url(n),
                site_renders.case_records(EXERCISED_CASES)[render_case_pages.case_url(n)],
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


def _case_actions(popover: Any, served: str, n: int) -> None:
    assert popover.locator("[data-case-open]").get_attribute("href") == (
        f"{served}cases/{n}.html"
    )
    assert popover.locator("[data-case-frontier]").get_attribute("href") == (
        f"{served}atlas.html#n-{n}"
    )
    assert popover.locator("[data-case-atlas]").get_attribute("href") == (
        f"{served}atlas.html#atlas-n-{n}"
    )


def _revealed_diagram(page: Any, n: int, *, scripts: bool = True) -> None:
    site_browser.api().expect(page.locator(f"#atlas-n-{n}")).to_be_in_viewport()
    state = page.evaluate(NAVIGATION, n)
    assert state["shown"] == 324, state
    assert 0 <= state["top"] < state["bottom"] <= state["viewportHeight"], state
    assert state["outlineWidth"] == "2px", state
    assert state["targeted"], state
    if scripts:
        assert state["expanded"] == "true", state
        assert state["focused"], state


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
        page.goto(f"{served}atlas.html", wait_until="load")
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
        _case_actions(popover, served, 12)
        # The record's links were written from its own directory and are rebased here.
        frontier_link = popover.locator('.site-case-links a:has-text("In the frontier")')
        assert (frontier_link.get_attribute("href") or "").endswith("atlas.html#n-12")
        page.keyboard.press("ArrowRight")
        popover.locator('[data-case-body] article.site-case[data-case="13"]').wait_for()
        _case_actions(popover, served, 13)
        assert row.get_attribute("aria-expanded") == "false"
        assert page.locator("#n-13").get_attribute("aria-expanded") == "true"
        popover.locator('[data-case-body] a[data-case-step="14"]').click()
        popover.locator('[data-case-body] article.site-case[data-case="14"]').wait_for()
        _case_actions(popover, served, 14)
        page.keyboard.press("ArrowLeft")
        popover.locator('[data-case-body] article.site-case[data-case="13"]').wait_for()
        _case_actions(popover, served, 13)
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
        page.goto(f"{served}atlas.html", wait_until="load")
        page.locator("#n-13 td.site-col-n a").click()
        popover = page.locator("#pop-case")
        popover.locator('[data-case-body] article.site-case[data-case="13"]').wait_for()
        prose = popover.locator('[data-case-body] .site-case-prose a[data-case="32"]').first
        prose.scroll_into_view_if_needed()
        prose.click()
        popover.locator('[data-case-body] article.site-case[data-case="32"]').wait_for()
        assert page.url == f"{served}atlas.html"


def test_an_atlas_cell_opens_the_same_record(browser: Any, served: str) -> None:
    """A tile opens the case popover on its record; Escape closes it and focus is back
    on the tile."""
    sync_api = site_browser.api()
    with _page(browser) as page:
        page.goto(f"{served}atlas.html", wait_until="load")
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


@pytest.mark.parametrize("scripts", [True, False])
def test_the_homepage_hero_opens_its_case_with_a_canonical_fallback(
    browser: Any, served: str, *, scripts: bool
) -> None:
    with _page(browser, scripts=scripts, width=390) as page:
        page.goto(served, wait_until="load")
        page.locator('.site-hero-figure a[data-case="53"]').click()
        if not scripts:
            page.wait_for_url(f"{served}cases/53.html", wait_until="load")
            _canonical_case(page, 53)
            return
        popover = page.locator("#pop-case")
        popover.locator('[data-case-body] article.site-case[data-case="53"]').wait_for()
        _case_actions(popover, served, 53)
        popover.locator("[data-case-atlas]").click()
        page.wait_for_url(f"{served}atlas.html#atlas-n-53", wait_until="load")
        _revealed_diagram(page, 53)


def test_case_page_survey_links_resolve_from_the_site_root_and_distinguish_rows_from_tiles(
    browser: Any, served: str
) -> None:
    with _page(browser) as page:
        page.goto(f"{served}cases/13.html", wait_until="load")
        link = page.locator('.site-case-links a:has-text("In the frontier survey")')
        assert link.get_attribute("href") == "../atlas.html#n-13"
        link.click()
        page.wait_for_url(f"{served}atlas.html#n-13", wait_until="load")
        site_browser.api().expect(page.locator("#n-13")).to_be_in_viewport()
        assert page.locator("[data-atlas-toggle]").get_attribute("aria-expanded") == "false"
        page.locator("#n-13 td.site-col-n a").click()
        popover = page.locator("#pop-case")
        popover.locator('[data-case-body] article.site-case[data-case="13"]').wait_for()
        _case_actions(popover, served, 13)
        popover.locator("[data-case-atlas]").click()
        page.wait_for_url(f"{served}atlas.html#atlas-n-13")
        _revealed_diagram(page, 13)


@pytest.mark.parametrize("n", [53, 291, 324])
@pytest.mark.parametrize("scripts", [True, False])
def test_atlas_diagram_fragments_reveal_the_complete_atlas(
    browser: Any, served: str, n: int, *, scripts: bool
) -> None:
    with _page(browser, scripts=scripts, width=390) as page:
        page.goto(f"{served}atlas.html#atlas-n-{n}", wait_until="load")
        _revealed_diagram(page, n, scripts=scripts)


def test_atlas_diagram_fragments_survive_same_fragment_clicks_and_history(
    browser: Any, served: str
) -> None:
    with _page(browser, width=390) as page:
        page.goto(f"{served}atlas.html#atlas-n-53", wait_until="load")
        _revealed_diagram(page, 53)
        page.locator("[data-atlas-toggle]").click()
        assert page.locator("[data-atlas-toggle]").get_attribute("aria-expanded") == "false"
        page.locator("#atlas-n-53").click()
        popover = page.locator("#pop-case")
        popover.locator('[data-case-body] article.site-case[data-case="53"]').wait_for()
        popover.locator("[data-case-atlas]").click()
        assert not popover.is_visible()
        assert page.url == f"{served}atlas.html#atlas-n-53"
        _revealed_diagram(page, 53)

        # A different same-page action updates the browser's :target, not just the URL.
        page.locator("#n-12 td.site-col-n a").click()
        popover.locator('[data-case-body] article.site-case[data-case="12"]').wait_for()
        popover.locator("[data-case-atlas]").click()
        page.wait_for_url(f"{served}atlas.html#atlas-n-12")
        _revealed_diagram(page, 12)

        page.goto(
            f"{served}atlas.html?atlas=triangle&size=large#atlas-n-291", wait_until="load"
        )
        _revealed_diagram(page, 291)
        page.goto(
            f"{served}atlas.html?atlas=triangle&size=large#atlas-n-324", wait_until="load"
        )
        _revealed_diagram(page, 324)
        page.locator("[data-atlas-toggle]").click()
        page.go_back(wait_until="load")
        page.wait_for_url(f"{served}atlas.html?atlas=triangle&size=large#atlas-n-291")
        _revealed_diagram(page, 291)
        page.go_forward(wait_until="load")
        page.wait_for_url(f"{served}atlas.html?atlas=triangle&size=large#atlas-n-324")
        _revealed_diagram(page, 324)


@pytest.mark.parametrize("width", [1280, 390])
@pytest.mark.parametrize("opener", ["frontier", "atlas"])
def test_the_popovers_compact_drawing_keeps_its_own_line_weight(
    browser: Any, served: str, opener: str, width: int
) -> None:
    """Canonical and fetched records share a compact square drawing. Its frame and
    outlines retain their non-scaling strokes, and the caption's radical stays visible.
    """
    with _page(browser, width=width) as page:
        if opener == "frontier":
            page.goto(f"{served}atlas.html", wait_until="load")
            row = page.locator("#n-10")
            row.scroll_into_view_if_needed()
            row.locator("td.site-thumb img").click()
        else:
            page.goto(f"{served}atlas.html", wait_until="load")
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
        limit = 20 if width == 1280 else 18
        assert drawn["width"] == pytest.approx(min(drawn["body"], limit * drawn["rem"]), abs=1)
        assert drawn["height"] == pytest.approx(drawn["width"], abs=0.5), drawn
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
        page.goto(f"{served}atlas.html", wait_until="load")
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
        assert head["cross_width"] == head["cross_height"] >= 44, head
        assert head["hit"], head
        popover.hover()
        page.mouse.wheel(0, 1200)
        site_browser.api().expect(popover.locator(".site-case-steps")).not_to_be_in_viewport()
        scrolled = page.evaluate(CROSS)
        assert scrolled["scroll_top"] > 0, scrolled
        assert scrolled["panel_top"] <= scrolled["cross_top"], scrolled
        assert scrolled["cross_bottom"] <= scrolled["panel_bottom"], scrolled
        assert scrolled["hit"], scrolled
        popover.locator(".site-popover-close").click()
        assert not popover.is_visible()
        site_browser.api().expect(row).to_be_focused()


def _canonical_case(page: Any, n: int) -> None:
    """The complete article, prepared math and identity at a case's own URL."""
    article = page.locator(f'article.site-case[data-case="{n}"]')
    article.wait_for(state="visible")
    assert page.locator("h1").count() == 1
    assert (
        article.locator("h1#case-title .kpress-math-semantic math").text_content() == f"n={n}"
    )
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
    """Canonical articles are present in the initial response; next/back/Atlas
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
        assert page.locator("article.site-case a[data-case-index]").count() == 0
        page.locator('.site-case-links a:has-text("In the frontier survey")').click()
        page.wait_for_url(f"{served}atlas.html#n-11", wait_until="load")
        assert page.locator(".site-atlas-cell[data-case]").count() == 324
        assert page.locator('link[rel="canonical"]').get_attribute("href") == (
            render_overview.canonical_url("atlas.html")
        )


def test_the_old_one_page_address_arrives_at_the_atlas_row(browser: Any, served: str) -> None:
    with _page(browser) as page:
        page.goto(f"{served}cases.html#n-17", wait_until="load")
        page.wait_for_url(f"{served}atlas.html#n-17", wait_until="load")
        site_browser.api().expect(page.locator("#n-17")).to_be_in_viewport()


@pytest.mark.parametrize("scripts", [True, False])
def test_unknown_cases_leave_a_readable_atlas_or_404_and_do_not_trap_back(
    browser: Any, served: str, *, scripts: bool
) -> None:
    """An unknown selector forwards to Atlas; a missing record returns
    HTTP 404 at its own address. Both preserve ordinary Back navigation."""
    with _page(browser, scripts=scripts) as page:
        page.goto(f"{served}atlas.html", wait_until="load")
        unknown = f"{served}cases/?n=999"
        response = page.goto(unknown, wait_until="load")
        assert response is not None
        assert response.status == 200
        destination = f"{served}atlas.html" + ("?n=999" if scripts else "")
        page.wait_for_url(destination, wait_until="load")
        assert page.locator(".site-atlas-cell[data-case]").count() == 324
        assert page.locator("article.site-case").count() == 0
        page.go_back(wait_until="load")
        assert page.url == f"{served}atlas.html"
        missing = f"{served}cases/999.html"
        response = page.goto(missing, wait_until="load")
        assert response is not None
        assert response.status == 404
        assert page.url == missing
        page.go_back(wait_until="load")
        assert page.url == f"{served}atlas.html"


def test_without_scripts_a_record_file_is_read_where_it_is(browser: Any, served: str) -> None:
    with _page(browser, scripts=False) as page:
        response = page.goto(f"{served}cases/29.html", wait_until="load")
        assert response is not None
        assert response.status == 200
        assert re.search(r'<article\b[^>]*\bdata-case="29"', response.text())
        assert page.url == f"{served}cases/29.html"
        _canonical_case(page, 29)
        assert page.locator("article.site-case figure svg").count() == 1


def _centered_case_bounds(layout: dict[str, Any]) -> None:
    """The five bound panels form one or two columns, with the last panel centred."""
    bounds = layout["bounds"]
    assert bounds["count"] == 5, layout
    columns = 2 if layout["articleWidth"] >= 35 * layout["rem"] else 1
    assert bounds["columns"] == columns, layout
    assert bounds["lastWidth"] == pytest.approx(bounds["firstWidth"], abs=0.1), layout
    assert bounds["lastCenter"] == pytest.approx(bounds["center"], abs=0.1), layout
    assert bounds["lastTop"] > bounds["precedingTop"], layout


@pytest.mark.parametrize("width", [1280, 390, 320])
@pytest.mark.parametrize("theme", ["light", "dark"])
def test_case_headers_keep_the_prominent_math_count_and_shared_action_arrows(
    browser: Any, served: str, tmp_path: Path, width: int, theme: str
) -> None:
    """The same coherent header stack opens from every directory entry point."""
    context = browser.new_context(
        viewport={"width": width, "height": 900},
        color_scheme=theme,
        reduced_motion="reduce",
    )
    try:
        page = context.new_page()
        for n in (15, 53, 291, 324):
            page.goto(f"{served}cases/{n}.html", wait_until="load")
            direct = page.evaluate(LAYOUT)
            assert page.locator("article.site-case [data-case-index]").count() == 0
            page.goto(f"{served}atlas.html", wait_until="load")
            page.locator(f"#n-{n} td.site-col-n a").click()
            popover = page.locator("#pop-case")
            popover.locator(f'article.site-case[data-case="{n}"]').wait_for(state="visible")
            fetched = page.evaluate(LAYOUT)
            if n == 15 and theme == "light":
                page.screenshot(path=tmp_path / f"n15-popover-{width}.png")
            _case_actions(popover, served, n)
            for layout in (direct, fetched):
                assert layout["titleMathText"] == f"n={n}", layout
                assert layout["titlePrepared"] == 1, layout
                assert "KPress Math Text" in layout["titleMathFamily"], layout
                assert "Sans" not in layout["titleMathFamily"], layout
                assert layout["titleSize"] == pytest.approx(
                    layout["sansBase"] * layout["titleScale"], abs=0.01
                ), layout
                assert layout["titleMathSize"] >= layout["sansBase"] * 1.5, layout
                assert layout["eyebrow"]["text"] == "Case record", layout
                assert layout["eyebrow"]["center"] == pytest.approx(
                    layout["titleCenter"], abs=1
                ), layout
                assert layout["eyebrow"]["bottom"] < layout["titleTop"], layout
                assert layout["titleBottom"] < layout["statusTop"], layout
                assert layout["statusClasses"][0] == "site-case-badges", layout
                assert layout["statusClasses"][-1] == "site-chip", layout
                assert layout["pageWidth"] <= width, layout
                assert layout["articleScrollWidth"] <= layout["articleWidth"] + 1, layout
                assert not layout["gapValuesOverlap"], layout
                assert layout["errors"] == layout["unprepared"] == 0, layout
            assert direct["semantics"] == fetched["semantics"]
            assert fetched["articleCenter"] == pytest.approx(fetched["panelCenter"], abs=1), (
                fetched
            )
            assert fetched["titleCenter"] == pytest.approx(fetched["panelCenter"], abs=1), (
                fetched
            )
            assert len(fetched["actions"]) == 3, fetched
            assert all(action == fetched["actions"][0] for action in fetched["actions"]), (
                fetched
            )
            assert fetched["actions"][0]["destination"] == "page", fetched
            assert fetched["actions"][0]["content"] == '""', fetched
            assert fetched["actions"][0]["mask"] != "none", fetched
            if n == 15 and width == 1280 and theme == "light":
                for key, following in (
                    ("ArrowRight", 16),
                    ("ArrowLeft", 15),
                    ("ArrowLeft", 14),
                ):
                    page.keyboard.press(key)
                    popover.locator(f'article.site-case[data-case="{following}"]').wait_for()
                    assert page.evaluate(LAYOUT)["titleMathText"] == f"n={following}"
                    _case_actions(popover, served, following)
            page.keyboard.press("Escape")
    finally:
        context.close()


def _case_bounds_at_the_two_column_boundary(page: Any) -> None:
    """Exercise the actual case width on either side of the inclusive 35rem query."""
    page.set_viewport_size({"width": 600, "height": 900})
    layout = page.evaluate(LAYOUT)
    boundary = 35 * layout["rem"]
    viewport = 600 + round(boundary - layout["articleWidth"])
    for offset in (-1, 0, 1):
        page.set_viewport_size({"width": viewport + offset, "height": 900})
        measured = page.evaluate(LAYOUT)
        # KPress's reduced-motion transition still completes on the next paint.
        site_browser.api().expect(page.locator(".site-case-bounds > :last-child")).to_have_css(
            "inline-size", f"{measured['bounds']['firstWidth']:g}px"
        )
        measured = page.evaluate(LAYOUT)
        assert measured["articleWidth"] == pytest.approx(boundary + offset, abs=0.01)
        _centered_case_bounds(measured)


@pytest.mark.parametrize("width", [1280, 390])
def test_the_case_diagram_precedes_its_number_line_with_balanced_footer_padding(
    browser: Any, served: str, tmp_path: Path, width: int
) -> None:
    """The diagram and number line use the same vertical layout in both readers."""
    with _page(browser, width=width) as page:
        for n in (15, 291):
            page.goto(f"{served}cases/{n}.html", wait_until="load")
            direct = page.evaluate(LAYOUT)
            page.goto(f"{served}atlas.html", wait_until="load")
            page.locator(f"#n-{n} td.site-col-n a").click()
            popover = page.locator("#pop-case")
            popover.locator(f'article.site-case[data-case="{n}"]').wait_for(state="visible")
            fetched = page.evaluate(LAYOUT)
            page.screenshot(path=tmp_path / f"n{n}-vertical-popover-{width}.png")
            for layout in (direct, fetched):
                assert layout["figureBottom"] < layout["gapTop"], layout
                assert layout["drawingCenter"] == pytest.approx(layout["articleCenter"], abs=1)
                assert layout["pageWidth"] <= width, layout
                assert not layout["gapValuesOverlap"], layout
            assert fetched["footerPadding"]["top"] == fetched["footerPadding"]["bottom"]
            assert fetched["footerPadding"]["top"] != "0px"
            assert fetched["articleCenter"] == pytest.approx(fetched["panelCenter"], abs=1)
            assert fetched["semantics"] == direct["semantics"]
            page.keyboard.press("Escape")


@pytest.mark.parametrize("width", [1280, 390, 320])
@pytest.mark.parametrize("theme", ["light", "dark"])
def test_case_summaries_keep_math_and_layout_when_fetched(
    browser: Any, served: str, tmp_path: Path, width: int, theme: str
) -> None:
    """Long exact intervals stay readable in their own scroll line; fetching the same
    article preserves its math and drawing with the prominent case heading scale on
    both themes and widths. A final unpaired bound card stays centred.
    """
    context = browser.new_context(
        viewport={"width": width, "height": 900},
        color_scheme=theme,
        reduced_motion="reduce",
    )
    try:
        page = context.new_page()
        for n in (291, 5, 11, 17, 324):
            page.goto(f"{served}cases/{n}.html", wait_until="load")
            page.locator(f'article.site-case[data-case="{n}"]').wait_for(state="visible")
            if n == 291 and width == 1280 and theme == "light":
                _case_bounds_at_the_two_column_boundary(page)
                page.set_viewport_size({"width": width, "height": 900})
            direct = page.evaluate(LAYOUT)
            if n == 291:
                page.screenshot(path=tmp_path / f"n291-direct-{width}-{theme}.png")
            page.goto(f"{served}atlas.html", wait_until="load")
            opener = page.locator(f"#n-{n} td.site-col-n a")
            opener.click()
            popover = page.locator("#pop-case")
            popover.locator(f'article.site-case[data-case="{n}"]').wait_for(state="visible")
            fetched = page.evaluate(LAYOUT)
            if n == 291:
                page.screenshot(path=tmp_path / f"n291-popover-{width}-{theme}.png")
            for layout in (direct, fetched):
                assert layout["pageWidth"] <= width, (n, layout)
                assert layout["articleScrollWidth"] <= layout["articleWidth"] + 1, (n, layout)
                assert layout["articleLeft"] >= 0, (n, layout)
                assert layout["articleRight"] <= width + 1, (n, layout)
                assert layout["errors"] == layout["unprepared"] == 0, (n, layout)
                assert layout["formulas"] > 0, (n, layout)
                assert layout["drawingWidth"] <= 20 * layout["rem"] + 1, (n, layout)
                assert layout["drawingHeight"] == pytest.approx(layout["drawingWidth"], abs=1)
                assert not layout["gapValuesOverlap"], (n, layout)
                assert layout["figureBottom"] < layout["gapTop"] < layout["provenTop"], (
                    n,
                    layout,
                )
                assert layout["glyphTop"] >= layout["intervalTop"] - 1, (n, layout)
                assert layout["glyphBottom"] <= layout["intervalBottom"] + 1, (n, layout)
                _centered_case_bounds(layout)
            assert fetched["panelScrollWidth"] <= fetched["panelWidth"] + 1, (n, fetched)
            assert fetched["semantics"] == direct["semantics"], n
            assert fetched["titleFamily"] == direct["titleFamily"], n
            for layout in (direct, fetched):
                assert layout["titleSize"] == pytest.approx(
                    layout["titleScale"] * layout["sansBase"], abs=0.01
                ), n
            if width == 1280:
                assert fetched["articleWidth"] == pytest.approx(direct["articleWidth"], abs=1)
                assert fetched["drawingWidth"] == pytest.approx(direct["drawingWidth"], abs=1)
            if n == 291:
                assert "data-kpress-math-rendered" in direct["generalBound"]
                assert "sqrt(" not in direct["generalBound"]
                assert fetched["generalBound"] == direct["generalBound"]
                if width <= 390:
                    assert direct["intervalScrollWidth"] > direct["intervalWidth"]
                    assert fetched["intervalScrollWidth"] > fetched["intervalWidth"]
                    assert direct["intervalOverflow"] == fetched["intervalOverflow"] == "auto"
            assert (popover.locator("[data-case-open]").get_attribute("href") or "").endswith(
                f"cases/{n}.html"
            )
            page.keyboard.press("Escape")
            site_browser.api().expect(opener).to_be_focused()
    finally:
        context.close()
