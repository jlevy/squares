"""No wide block of a site page is cut off by an ancestor that clips, in a browser.

A wide block (a table with its filter bar and count, a row of cards, the atlas grid,
the film) is wider than the reading column, and a narrow page clips at the document's
edge. A block sized from the window ran under that clip: the window counts a scrollbar
the layout does not, so the first letters of the filter labels and the last of the count
were cut. `preview_site.clipped` finds any such block, and this holds the site's pages to
none, at the widths a tablet and a phone have, with and without a scrollbar's width
taken from the layout (`templates/paper-design.md`, Spacing).

The same browser holds Videos and the Workbench to the header every page has: the bar,
the rule under it, the trail, the content. They are separate destinations in the Learn
menu, and neither carries the Film | Workbench switcher it once had under the bar
(`templates/paper-design.md`, Videos and Workbench). The controls put the switcher back,
through the header slot `render_overview.kpress_page` still offers (`tabs`), to show the
header's report would find it and `preview_site.tabs_problems` would name tabs standing
over the rule.

It also holds the header's type to the body's, by relation and not by pixel value: a
link in the bar is one step under the prose, section tabs apply the shared button-label
scale, and the site's name is no smaller than the prose (`preview_site.type_problems`,
`templates/paper-design.md`, Navigation bar).

And it holds the header's labels to their baselines, measured and not read from a
box: the site's name stands on the baseline of the bar's links
(`preview_site.baseline_problems`).

Every page that may be the film's is opened as for a reader who asks for reduced motion
(`preview_site.REDUCED_MOTION`), so its film stands at its poster and no test starts the
film's download.

Skipped where no Chromium can be launched; `SQPACK_CHROMIUM` names one the environment
supplies, as the other browser tools read it.
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from functools import partial
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest

from devtools import render_overview
from devtools.preview_site import (
    BASELINE_TOLERANCE,
    BASELINES,
    CLIP_WIDTHS,
    CLIPPED,
    HEADER,
    REDUCED_MOTION,
    SCROLLBAR_PX,
    baseline_problems,
    clipped,
    tabs_problems,
    type_problems,
)
from devtools.render_n11_lower_bounds_explainer_pdf import BROWSER_OVERRIDE
from tests import site_renders

PAGES = (
    "index.html",
    "results.html",
    "atlas.html",
    "papers.html",
    "visualize.html",
    "tutorial.html",
    "tutorial-advanced.html",
)
WIDTHS = (*CLIP_WIDTHS, 390)
#: The rule the wide track had: its room measured from the window, a rem a side.
FROM_THE_WINDOW = ".site-page .site-wide { --site-wide-room: calc(100vw - 2rem) !important; }"
#: The rule the header had: its own lower border, under the tabs it holds.
RULE_UNDER_THE_TABS = (
    ".kpress-site-header:has(> .site-tabs) { border-block-end: 1px solid !important; }"
)
#: The Film | Workbench switcher Videos and the Workbench carried under the bar, as the
#: retired `render_overview.visualize_tabs` wrote it on the film's page; the controls put
#: it back.
SWITCHER = (
    '<nav class="site-tabs" aria-label="Visuals">'
    '<a data-tab="film" aria-current="page" href="visualize.html">Film</a>'
    '<a data-tab="workbench" href="workbench/">Workbench</a></nav>'
)
#: A root em in CSS pixels, and the trail's spaces, in rem: under the rule and over a
#: page's first block (`.site-breadcrumbs`, `margin-block`, in `site-nav.css`).
REM = 16
TRAIL_ABOVE, TRAIL_BELOW = 1, 2.5
#: The sizes the bar had before its type was tied to the body's: 16px links and name,
#: 14.4px tabs, under 18px prose.
OLD_BAR_TYPE = (
    ".site-nav, .site-nav .site-name { font-size: 1rem !important; }"
    " .site-tabs { font-size: 0.9rem !important; }"
)
#: A name displaced above the other links, as a control for the baseline check.
NAME_ABOVE_LINKS = ".site-nav .site-name { transform: translateY(-4px) !important; }"
#: Desktop, tablet and phone widths exercise both navigation presentations.
BAR_WIDTHS = (1280, 768, 390)


@pytest.fixture(scope="module")
def browser() -> Iterator[Any]:
    sync_api = pytest.importorskip("playwright.sync_api")
    with sync_api.sync_playwright() as driver:
        try:
            launched = driver.chromium.launch(executable_path=os.environ.get(BROWSER_OVERRIDE))
        except sync_api.Error as error:
            pytest.skip(f"no Chromium to launch: {error.message.splitlines()[0]}")
        yield launched
        launched.close()


@pytest.fixture(scope="module")
def pages(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Path]:
    return site_renders.write(tmp_path_factory.mktemp("site"), *PAGES)


@pytest.mark.parametrize("name", PAGES)
def test_no_wide_block_runs_past_an_ancestor_that_clips_it(
    browser: Any, pages: dict[str, Path], name: str
) -> None:
    for width in WIDTHS:
        page = browser.new_page(
            viewport={"width": width, "height": 900}, reduced_motion=REDUCED_MOTION
        )
        try:
            page.goto(pages[name].as_uri(), wait_until="load")
            assert clipped(page) == [], f"{name} at {width}"
        finally:
            page.close()


def test_a_block_sized_from_the_window_is_caught(browser: Any, pages: dict[str, Path]) -> None:
    """The control: with the wide track sized from the window again, the results table,
    its filter bar and its count run past the document's clip on a tablet, further still
    once a scrollbar takes its width from the layout, and the check names each."""
    page = browser.new_page(viewport={"width": 768, "height": 900})
    try:
        page.goto(pages["results.html"].as_uri(), wait_until="load")
        page.add_style_tag(content=FROM_THE_WINDOW)
        plain = page.evaluate(CLIPPED, {"scrollbar": 0})
        frame = page.locator("article.kpress").bounding_box()
        assert frame is not None
        plain_past = (768 - 2 * REM - frame["width"]) / 2
        page.add_style_tag(content=f"html {{ inline-size: calc(100vw - {SCROLLBAR_PX}px); }}")
        narrowed = page.evaluate(CLIPPED, {"scrollbar": SCROLLBAR_PX})
        frame = page.locator("article.kpress").bounding_box()
        assert frame is not None
        narrowed_past = (768 - 2 * REM - frame["width"]) / 2
    finally:
        page.close()
    for found, past in ((plain, plain_past), (narrowed, narrowed_past)):
        assert past > 0
        by_block = {row["block"]: row for row in found}
        for block in ("div.site-table-tools.site-result-filters", "div.site-table-wrap"):
            assert (by_block[block]["left"], by_block[block]["right"]) == (past, past), block
        assert by_block["span.site-count"]["right"] == past
        assert {row["frame"] for row in found} == {"article.kpress"}


def _workbench_shell(path: Path) -> Path:
    """The workbench's shell, written at `path`: its template with its own stylesheet and
    no program, which is all of that page the header's place needs."""
    from workbench_tools import build_site  # noqa: PLC0415

    assets = build_site.WORKBENCH_PACKAGE / "assets"
    shell = build_site.with_nav((assets / "template.html").read_text(encoding="utf-8"))
    styles = (assets / "workbench.css").read_text(encoding="utf-8")
    assert shell.count("__WORKBENCH_CSS__") == 1
    path.write_text(shell.replace("__WORKBENCH_CSS__", styles), encoding="utf-8")
    return path


@pytest.fixture(scope="module")
def media_pages(pages: dict[str, Path]) -> dict[str, Path]:
    """Videos and the Workbench: the film's page as the site renders it, and the
    workbench's shell (`_workbench_shell`)."""
    film = pages["visualize.html"]
    workbench = _workbench_shell(film.with_name("workbench.html"))
    return {"visualize.html": film, "workbench/": workbench}


@pytest.fixture(scope="module")
def switcher_pages(pages: dict[str, Path]) -> dict[str, Path]:
    """The same two pages with `SWITCHER` put back after the bar, in the header slot each
    still offers: `tabs` of `render_overview.kpress_page`, which renders the film's page,
    and of `render_overview.nav_shell`, which gives the workbench's shell its bar."""
    from workbench_tools import build_site  # noqa: PLC0415

    beside = pages["visualize.html"]
    film = beside.with_name("film-switcher.html")
    with patch.object(
        render_overview, "kpress_page", partial(render_overview.kpress_page, tabs=SWITCHER)
    ):
        film.write_text(render_overview.visualize_page().html, encoding="utf-8")
    with patch.object(
        build_site, "nav_shell", partial(render_overview.nav_shell, tabs=SWITCHER)
    ):
        workbench = _workbench_shell(beside.with_name("workbench-switcher.html"))
    return {"visualize.html": film, "workbench/": workbench}


@pytest.mark.parametrize("width", [1280, 390])
def test_videos_and_the_workbench_have_no_tabs_under_the_bars_rule(
    browser: Any, media_pages: dict[str, Path], width: int
) -> None:
    """On the film's page and the workbench, from the top: the bar, the rule under it,
    the trail, the content, as on every page, with no switcher between the rule and the
    trail. The rule is the header slot's, at the bar's foot and as long as the bar; the
    trail starts `TRAIL_ABOVE` under it, and the film or the application `TRAIL_BELOW`
    under the trail."""
    for name, path in media_pages.items():
        page = browser.new_page(
            viewport={"width": width, "height": 900}, reduced_motion=REDUCED_MOTION
        )
        try:
            page.goto(path.as_uri(), wait_until="load")
            found = page.evaluate(HEADER)
        finally:
            page.close()
        where = f"{name} at {width}"
        assert found["tabs"] is None, where
        parts = ("nav", "rule", "breadcrumb", "first")
        nav, rule, trail, first = (found[part] for part in parts)
        assert rule["on"].partition(".")[0] == "header", where
        assert rule["top"] == pytest.approx(nav["bottom"], abs=0.05), where
        assert (rule["left"], rule["right"]) == (nav["left"], nav["right"]), where
        assert trail is not None, where
        above, below = trail["top"] - rule["bottom"], first["top"] - trail["bottom"]
        assert above == pytest.approx(TRAIL_ABOVE * REM, abs=0.05), where
        assert below == pytest.approx(TRAIL_BELOW * REM, abs=0.05), where


def test_inline_visuals_choices_are_not_header_tabs(browser: Any) -> None:
    """A chooser inside the reading column does not constrain the title above it."""
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    try:
        page.set_content(
            '<header class="kpress-site-header"><nav class="site-nav">Site</nav></header>'
            '<article class="kpress-long-text"><h1>Explanations</h1>'
            '<h2>Visuals</h2><nav class="site-tabs" aria-label="Visuals">'
            '<a aria-current="page" href="#film">Film</a>'
            '<a href="#workbench">Workbench</a></nav></article>'
        )
        found = page.evaluate(HEADER)
    finally:
        page.close()
    assert found["tabs"] is None
    assert found["type"]["tab"] is None
    assert tabs_problems(found) == []


def test_baseline_labels_use_visible_text_or_the_icon_links_accessible_name(
    browser: Any,
) -> None:
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    try:
        page.set_content(
            '<nav class="site-nav">'
            '<a data-page="overview" aria-label="Overview page">Overview</a>'
            '<a data-page="github" aria-label="GitHub">'
            '<svg aria-hidden="true" viewBox="0 0 24 24"></svg></a></nav>'
        )
        found = page.evaluate(BASELINES)
    finally:
        page.close()
    assert [link["label"] for link in found["links"]] == ["Overview", "GitHub"]


def test_tabs_over_the_rule_are_caught(browser: Any, switcher_pages: dict[str, Path]) -> None:
    """The control: put the switcher back after the bar, and the header's report finds
    it, with Film current, so the pages above have none for it to miss; give the header
    that holds it its lower border back, as it had while the tabs stood over the rule,
    and the check names the tabs on both pages."""
    for name, path in switcher_pages.items():
        page = browser.new_page(
            viewport={"width": 1280, "height": 900}, reduced_motion=REDUCED_MOTION
        )
        try:
            page.goto(path.as_uri(), wait_until="load")
            if name != "workbench/":
                # ResizeObserver can add site-headroom after load; the workbench
                # fixture deliberately has no program.
                page.locator("header.site-headroom").wait_for(state="attached")
            found = page.evaluate(HEADER)
            page.add_style_tag(content=RULE_UNDER_THE_TABS)
            problems = tabs_problems(page.evaluate(HEADER))
        finally:
            page.close()
        assert found["tabs"] is not None, name
        assert found["tabs"]["current"] == "Film", name
        assert tabs_problems(found) == [], name
        assert len(problems) == 1, name
        assert problems[0].startswith("the section tabs start "), name
        owner = "header" if name == "workbench/" else "header.site-headroom"
        assert problems[0].endswith(f"which is on {owner}"), name


def _header(browser: Any, path: Path, width: int, *, style: str = "") -> dict[str, Any]:
    """The `preview_site/header` report of the page at `path`, `width` pixels wide, with
    `style` added to it first."""
    page = browser.new_page(
        viewport={"width": width, "height": 900}, reduced_motion=REDUCED_MOTION
    )
    try:
        page.goto(path.as_uri(), wait_until="load")
        if style:
            page.add_style_tag(content=style)
        return page.evaluate(HEADER)
    finally:
        page.close()


def test_the_bars_type_is_one_step_under_the_bodys(
    browser: Any,
    pages: dict[str, Path],
    media_pages: dict[str, Path],
) -> None:
    """At a desktop, a tablet and a phone width, on a page of prose, on the film's page
    and on the workbench: a link in the bar is smaller than the body's
    prose and no smaller than the first step of the paper's scale under it, and no page
    has a section tab to size. The site's name is at least the body's size.
    Nothing here is a pixel
    value: the body is the prose base the page resolves, which a prose paragraph is set
    at, and the step is read from the same scale. The larger type leaves the bar's links
    reachable at desktop, tablet and phone widths, with no page wider than its window."""
    opened = {"atlas.html": pages["atlas.html"], **media_pages}
    seen: dict[str, set[tuple[float, float | None, float]]] = {name: set() for name in opened}
    for width in BAR_WIDTHS:
        for name, path in opened.items():
            sizes = _header(browser, path, width)["type"]
            where = f"{name} at {width}"
            assert type_problems({"type": sizes}) == [], where
            body, scale = sizes["scale"]["prose"], sizes["scale"]
            below = max(step for step in scale.values() if step < body)
            assert below <= sizes["link"] < body <= sizes["name"], where
            assert sizes["name_shown"] is True, where
            assert sizes["name_label"] == (
                "The Squares Project" if width == 1280 else "Squares"
            )
            assert sizes["links_rows"] >= 1, where
            assert sizes["overflow"] == 0, where
            if name == "atlas.html":
                assert sizes["body"] == body, where
            assert sizes["tab"] is None, where
            seen[name].add((sizes["link"], sizes["tab"], sizes["name"]))
    # One size at every width, and the same bar on every page.
    assert all(len(found) == 1 for found in seen.values()), seen
    assert len({next(iter(found))[::2] for found in seen.values()}) == 1, seen


def test_a_bar_set_smaller_than_one_step_under_the_body_is_caught(
    browser: Any, switcher_pages: dict[str, Path]
) -> None:
    """The control: on the film's page with the switcher put back, give the bar and the
    tabs the sizes they had, in rem and not from the body's scale, and the check names
    the links, the tabs and the name."""
    path = switcher_pages["visualize.html"]
    problems = type_problems(_header(browser, path, 1280, style=OLD_BAR_TYPE))
    assert [problem.split(":")[0] for problem in problems] == [
        "a link in the header is 16px",
        "a tab in the header is 14.4px",
        "the site's name is 16px, under the body's 18px",
    ]


def _baselines(browser: Any, path: Path, width: int, *, style: str = "") -> dict[str, Any]:
    """The `preview_site/baselines` report of the page at `path`, `width` pixels wide,
    with `style` added to it first."""
    page = browser.new_page(
        viewport={"width": width, "height": 900}, reduced_motion=REDUCED_MOTION
    )
    try:
        page.goto(path.as_uri(), wait_until="load")
        if style:
            page.add_style_tag(content=style)
        return page.evaluate(BASELINES)
    finally:
        page.close()


def test_the_name_stands_on_the_links_baseline(
    browser: Any,
    pages: dict[str, Path],
    media_pages: dict[str, Path],
) -> None:
    """At a desktop, a tablet and a phone width, on a page of prose, on the film's page
    and on the workbench: every link on a line of the bar stands on one baseline, and
    the full or compact site name on the links', each within half a pixel, with no
    section tab under the bar. The current link's baseline is as far over the rule
    with the full name as with the compact one."""
    opened = {"atlas.html": pages["atlas.html"], **media_pages}
    over_rule: dict[int, set[float]] = {}
    for width in BAR_WIDTHS:
        for name, path in opened.items():
            found = _baselines(browser, path, width)
            where = f"{name} at {width}"
            assert baseline_problems(found) == [], where
            labels = [link["label"] for link in found["links"]]
            # Overview and News moved into the Project menu on 26 October 2026, so the
            # bar's own row is four categories and the GitHub link.
            assert labels == (
                ["Menu", "GitHub"]
                if width < 768
                else ["Project", "Results", "Learn", "About", "GitHub"]
            ), where
            first = min(found["links"], key=lambda link: link["top"])
            assert abs(found["name"] - first["baseline"]) <= BASELINE_TOLERANCE, where
            assert found["tabs"] == [], where
            if found["current_above_rule"] is not None:
                over_rule.setdefault(width, set()).add(found["current_above_rule"])
    # With the full name (1280) and the compact one (768), on every page: one distance.
    assert len(set().union(*over_rule.values())) == 1, over_rule


def test_a_name_above_the_links_is_caught(browser: Any, pages: dict[str, Path]) -> None:
    """The control: lift the name above the links and require the check to report it."""
    found = _baselines(browser, pages["atlas.html"], 1280, style=NAME_ABOVE_LINKS)
    problems = baseline_problems(found)
    assert len(problems) == 1, problems
    assert problems[0].startswith("the site's name stands -"), problems
    assert problems[0].endswith("px off the baseline of the bar's links"), problems
