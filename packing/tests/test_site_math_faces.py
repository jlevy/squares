"""Prepared formulas use the face required by their actual browser text context.

Serif prose uses serif mathematics; sans text uses sans mathematics, while a
headline consisting only of mathematics is serif. The walk checks complete canonical
pages and fetched case articles using their prepared visual trees and retained MathML,
with a controlled wrong-profile mutation proving that a face mismatch is detected.
The shared browser launcher fails when an installed-browser gate cannot launch it.
"""

from __future__ import annotations

import html
import re
import socket
from collections.abc import Iterator, Sequence
from pathlib import Path
from typing import Any

import pytest

from devtools import render_case_pages, render_overview
from devtools.measure_site_pages import MATH_FACES
from devtools.preview_site import MATH_FACE, press, serve, settle_math
from tests import site_browser, site_renders

SANS_TEXT = "Source Sans 3 Variable"
SERIF_MATH, SANS_MATH = "KPress Math Text", "KPress Math Text Sans"
#: The cases whose records are walked: the settled case, with a closed form in every
#: panel, and an open one.
CASES = (11, 29)
#: A result row's popover headline on the results page, as `row_detail` writes one that
#: is not mathematics alone (so unmarked): the popover's id and the headline's HTML.
#: These are the popovers whose headlines have words and a formula; the page and paper
#: cards navigate and open none.
ROW_HEADLINE = re.compile(
    r'<p class="site-popover-value" id="(pop-result-t-\d+)-title">(.*?)</p>', re.DOTALL
)
#: One actual semantic MathML tree retained beside a statically prepared formula.
FORMULA = re.compile(
    r'<span class="kpress-math-semantic">(<math\b.*?</math>)</span>', re.DOTALL
)

#: A walk's findings: the formulas set in the wrong face, and every formula counted by
#: (surface, text face, math face).
Walk = tuple[list[str], dict[tuple[str, str, str], dict[str, Any]]]


@pytest.fixture(scope="module")
def frontier_math_counts() -> tuple[int, int]:
    return site_renders.frontier_math_counts()


@pytest.fixture(scope="module")
def browser() -> Iterator[Any]:
    sync_api = site_browser.api()
    with sync_api.sync_playwright() as driver:
        launched = site_browser.launch(driver)
        yield launched
        launched.close()


@pytest.fixture(scope="module")
def root(tmp_path_factory: pytest.TempPathFactory) -> Path:
    return tmp_path_factory.mktemp("site")


def walk(
    browser: Any,
    address: str,
    *,
    presses: Sequence[str],
    whole: bool,
    ready: str = "",
    shown_popover: str = "",
) -> Walk:
    """Open the actual page and walk its prepared formulas after each interaction.
    The whole-page scroll also places lazy drawings; ready names a fetched or
    canonical article whose content must be visible before the walk."""
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    try:
        page.goto(address, wait_until="load")
        if ready:
            page.locator(ready).wait_for()
        if whole:
            assert settle_math(page) == 0, "math left untypeset"
        for selector in presses:
            press(page, selector)
            if shown_popover:
                assert page.locator(shown_popover).is_visible()
            page.keyboard.press("Escape")
        found: list[dict[str, Any]] = page.evaluate(MATH_FACES)
        rows = {(row["surface"], row["text"], row["math"]): row for row in found}
        return page.evaluate(MATH_FACE), rows
    finally:
        page.close()


@pytest.fixture(scope="module")
def overview(browser: Any, root: Path) -> Walk:
    path = site_renders.write(root, "index.html")["index.html"]
    return walk(browser, path.as_uri(), presses=(), whole=True)


@pytest.fixture(scope="module")
def results(browser: Any, root: Path) -> Walk:
    path = site_renders.write(root, render_overview.RESULTS_PAGE)[render_overview.RESULTS_PAGE]
    return walk(browser, path.as_uri(), presses=(), whole=True)


@pytest.fixture(scope="module")
def frontier_atlas(browser: Any, root: Path) -> Walk:
    path = site_renders.write(root, "frontier.html")["frontier.html"]
    return walk(browser, path.as_uri(), presses=(), whole=False)


@pytest.fixture(scope="module")
def served(root: Path) -> Iterator[str]:
    """The real frontier, index and two complete records, served for fetch overlays."""
    files = [
        site_renders.page("frontier.html"),
        site_renders.page(render_case_pages.CASES_PAGE),
        *(
            render_overview.Page(
                render_case_pages.case_url(n),
                site_renders.case_records()[render_case_pages.case_url(n)],
            )
            for n in CASES
        ),
    ]
    directory = root / "served"
    render_overview.write_site(directory, files)
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = int(probe.getsockname()[1])
    server = serve(directory, port)
    try:
        yield f"http://127.0.0.1:{port}/"
    finally:
        server.shutdown()
        server.server_close()


@pytest.fixture(scope="module")
def case_records(browser: Any, served: str) -> dict[int, Walk]:
    """Each complete canonical case page, without a dynamic reader wrapper."""
    return {
        n: walk(
            browser,
            f"{served}{render_case_pages.case_url(n)}",
            presses=(),
            whole=True,
            ready=f'article.site-case[data-case="{n}"]',
        )
        for n in CASES
    }


@pytest.fixture(scope="module")
def frontier_popover(browser: Any, served: str) -> Walk:
    """The frontier page with case 11's row pressed: its record in the case popover."""
    return walk(
        browser, f"{served}frontier.html", presses=("#n-11 td.site-thumb img",), whole=False
    )


def test_the_overviews_sans_surfaces_set_sans_math_and_its_math_headline_serif(
    overview: Walk,
) -> None:
    """The overview's cards, notes, popovers and tables are sans text with sans math; a
    popover headline that is mathematics alone is serif, each result row's whose summary
    is one bound; and nothing is set wrongly."""
    wrong, rows = overview
    assert wrong == []
    for surface in ("card headline", "card note", "popover headline", "table cell"):
        assert rows[(surface, SANS_TEXT, SANS_MATH)]["count"] > 0, surface
        assert rows[(surface, SANS_TEXT, SANS_MATH)]["alone"] == 0, surface
    headline = rows[("popover headline", SANS_TEXT, SERIF_MATH)]
    assert headline["count"] == headline["alone"] >= 1
    assert ("card headline", SANS_TEXT, SERIF_MATH) not in rows


def test_the_results_table_sets_sans_math(results: Walk) -> None:
    """The results table's cells and its row popovers are sans text with sans math, and
    the only serif math in sans text is a popover headline that is mathematics alone."""
    wrong, rows = results
    assert wrong == []
    assert rows[("table cell", SANS_TEXT, SANS_MATH)]["count"] > 0
    serif = {key[0]: row for key, row in rows.items() if key[1:] == (SANS_TEXT, SERIF_MATH)}
    assert set(serif) <= {"popover headline"}
    assert all(row["count"] == row["alone"] for row in serif.values())


def test_the_frontier_table_sets_sans_math(
    frontier_atlas: Walk, frontier_math_counts: tuple[int, int]
) -> None:
    """The frontier atlas's table is sans math. The page has no subtitle: its range of
    cases, set as sans math under the title, went on 2026-10-02 (the owner,
    `think-wz9d`). Its case popover, which fetches a record, is walked where the
    records are served (`frontier_popover`)."""
    wrong, rows = frontier_atlas
    assert wrong == []
    native = rows[("table cell", SANS_TEXT, SANS_TEXT)]
    assert native["count"] == frontier_math_counts[0]
    assert native["backend"] == "native-mathml"
    assert not [key for key in rows if key[0] == "subtitle"]


def test_the_case_popover_sets_its_records_math_sans(frontier_popover: Walk) -> None:
    """A case's record in the frontier's case popover is set as on its own page: its
    head, panels and visual summary are sans text with sans math, the case file's prose
    serif with serif math, and nothing is set wrongly. In the popover the probe counts
    the record's head and panels under the popover's surface."""
    wrong, rows = frontier_popover
    assert wrong == []
    assert rows[("popover", SANS_TEXT, SANS_MATH)]["count"] > 0
    assert rows[("visual summary", SANS_TEXT, SANS_MATH)]["count"] > 0
    for surface, text, face in rows:
        if surface in {"popover", "visual summary"}:
            assert (text == SANS_TEXT) == (face == SANS_MATH), (surface, text, face)


@pytest.mark.parametrize("n", CASES)
def test_a_case_records_panels_set_sans_math(case_records: dict[int, Walk], n: int) -> None:
    wrong, rows = case_records[n]
    assert wrong == []
    for surface in ("case head", "case bounds", "visual summary"):
        assert rows[(surface, SANS_TEXT, SANS_MATH)]["count"] > 0, surface
    assert not [key for key in rows if key[0].startswith("case") and key[2] != SANS_MATH]


def test_the_walk_catches_serif_math_in_a_sans_headline(browser: Any, root: Path) -> None:
    """The control changes one prepared formula in a worded sans headline to the
    serif profile. The clean baseline passes and the same walk names the wrong face,
    from its actual semantic MathML, after its real row trigger opens it."""
    results = site_renders.html(render_overview.RESULTS_PAGE)
    target, headline, semantic = next(
        (target, headline, FORMULA.findall(headline)[0])
        for target, headline in ROW_HEADLINE.findall(results)
        if len(FORMULA.findall(headline)) == 1 and re.match(r"\s*\w", headline)
    )
    plain = f'<p class="site-popover-value" id="{target}-title">{headline}</p>'
    assert results.count(plain) == 1
    assert 'data-site-math="sans"' in headline
    # Change the prepared profile, preserving the real visual tree and MathML.
    damaged = plain.replace('data-site-math="sans"', 'data-site-math="serif"', 1)
    baseline = site_renders.write(root, render_overview.RESULTS_PAGE)[
        render_overview.RESULTS_PAGE
    ]
    trigger = f'tr[aria-controls="{target}"] td.site-col-date'
    clean, _ = walk(
        browser,
        baseline.as_uri(),
        presses=(trigger,),
        whole=False,
        shown_popover=f"#{target}",
    )
    assert clean == []
    marked = root / "marked.html"
    marked.write_text(results.replace(plain, damaged, 1), encoding="utf-8")
    wrong, _ = walk(
        browser,
        marked.as_uri(),
        presses=(trigger,),
        whole=False,
        shown_popover=f"#{target}",
    )
    where = f"p.site-popover-value in #{target}-title"
    example = html.unescape(re.sub(r"<[^>]+>", "", semantic))[:40]
    assert example
    assert wrong == [f"serif math in sans text: {where}: {example}"]


def test_frontier_native_math_wrong_face_is_reported(
    browser: Any,
    frontier_math_counts: tuple[int, int],
    tmp_path: Path,
) -> None:
    path = site_renders.write(tmp_path, "frontier.html")["frontier.html"]
    source = path.read_text()
    source = source.replace(
        "</head>",
        '<style>.site-frontier [data-site-native-math="frontier"] :is(mi,mn,mtext,ms) '
        '{font-family:"Times New Roman";}</style></head>',
        1,
    )
    path.write_text(source)
    wrong, rows = walk(browser, path.as_uri(), presses=(), whole=False)
    assert any("native frontier math" in finding for finding in wrong)
    mutant = rows[("table cell", SANS_TEXT, "Times New Roman")]
    assert mutant["count"] == frontier_math_counts[0]
    assert mutant["backend"] == "native-mathml"
