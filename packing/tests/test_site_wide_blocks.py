"""No wide block of a site page is cut off by an ancestor that clips, in a browser.

A wide block (a table with its filter bar and count, a row of cards, the atlas grid,
the film) is wider than the reading column, and a narrow page clips at the document's
edge. A block sized from the window ran under that clip: the window counts a scrollbar
the layout does not, so the first letters of the filter labels and the last of the count
were cut. `preview_site.clipped` finds any such block, and this holds the site's pages to
none, at the widths a tablet and a phone have, with and without a scrollbar's width
taken from the layout (`templates/paper-design.md`, Spacing).

The same browser holds the Visualize section's tabs to their place on both its pages:
under the rule that runs under the navigation bar, never over it, with the content the
shared space under them (`preview_site.tabs_problems`, `templates/paper-design.md`,
Section tabs).

It also holds the header's type to the body's, by relation and not by pixel value: a
link in the bar and a section tab are one step under the prose on the paper's scale and
no more, and the site's name is no smaller than the prose (`preview_site.type_problems`,
`templates/paper-design.md`, Navigation bar).

And it holds the header's labels to their baselines, measured and not read from a
box: the site's name stands on the baseline of the bar's links, and the tabs on one of
their own (`preview_site.baseline_problems`).

Every page that may be the film's is opened as for a reader who asks for reduced motion
(`preview_site.REDUCED_MOTION`), so its film stands at its poster and no test starts the
film's download.

Skipped where no Chromium can be launched; `SQPACK_CHROMIUM` names one the environment
supplies, as the other browser tools read it.
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

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

PAGES = ("index.html", "all-results.html", "atlas.html", "visualize.html", "tutorial.html")
WIDTHS = (*CLIP_WIDTHS, 390)
#: The rule the wide track had: its room measured from the window, a rem a side.
FROM_THE_WINDOW = ".site-page .site-wide { --site-wide-room: calc(100vw - 2rem) !important; }"
#: The rule the header had: its own lower border, under the tabs it holds.
RULE_UNDER_THE_TABS = (
    ".kpress-site-header:has(> .site-tabs) { border-block-end: 1px solid !important; }"
)
#: A root em in CSS pixels, and the two spaces the tabs stand in, in rem: under the rule
#: (`--site-tabs-space`) and over a page's first block (`--site-page-top`).
REM = 16
TABS_SPACE, PAGE_TOP = 0.7, 4
#: The sizes the bar had before its type was tied to the body's: 16px links and name,
#: 14.4px tabs, under 18px prose.
OLD_BAR_TYPE = (
    ".site-nav, .site-nav .site-name { font-size: 1rem !important; }"
    " .site-tabs { font-size: 0.9rem !important; }"
)
#: The bar's baseline as it was: the name's row aligned by its first item, the mark.
NAME_ALIGNED_BY_ITS_MARK = ".site-nav .site-name-text { align-self: auto !important; }"
#: The widths the bar is measured at, and how many lines its links may take at each: one
#: on a desktop and a tablet, two on a phone.
BAR_WIDTHS = {1280: 1, 768: 1, 390: 2}


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
        page.goto(pages["all-results.html"].as_uri(), wait_until="load")
        page.add_style_tag(content=FROM_THE_WINDOW)
        plain = page.evaluate(CLIPPED, {"scrollbar": 0})
        narrowed = page.evaluate(CLIPPED, {"scrollbar": SCROLLBAR_PX})
    finally:
        page.close()
    for found, past in ((plain, 16), (narrowed, 16 + SCROLLBAR_PX / 2)):
        by_block = {row["block"]: row for row in found}
        for block in ("div.site-table-tools.site-result-filters", "div.site-table-wrap"):
            assert (by_block[block]["left"], by_block[block]["right"]) == (past, past), block
        assert by_block["span.site-count"]["right"] == past
        assert {row["frame"] for row in found} == {"article.kpress"}


@pytest.fixture(scope="module")
def section_pages(pages: dict[str, Path]) -> dict[str, tuple[Path, str, float]]:
    """The Visualize section's two pages, each with its current tab and the space its
    content starts under the tabs, in rem: the film's page as the site renders it, and
    the workbench's shell on its template with its own stylesheet and no program, which
    is all of that page the header's place needs."""
    from workbench_tools import build_site  # noqa: PLC0415

    assets = build_site.WORKBENCH_PACKAGE / "assets"
    shell = build_site.with_nav((assets / "template.html").read_text(encoding="utf-8"))
    styles = (assets / "workbench.css").read_text(encoding="utf-8")
    assert shell.count("__WORKBENCH_CSS__") == 1
    workbench = pages["visualize.html"].with_name("workbench.html")
    workbench.write_text(shell.replace("__WORKBENCH_CSS__", styles), encoding="utf-8")
    return {
        "visualize.html": (pages["visualize.html"], "Film", PAGE_TOP),
        "workbench/": (workbench, "Workbench", TABS_SPACE),
    }


@pytest.mark.parametrize("width", [1280, 390])
def test_the_section_tabs_stand_under_the_bars_rule(
    browser: Any, section_pages: dict[str, tuple[Path, str, float]], width: int
) -> None:
    """On the film's page and on the workbench, from the top: the bar, the rule under it,
    the tabs, the content. The rule is the bar's own, at the bar's foot and as long as
    the bar, where it is on every other page; the tabs start `--site-tabs-space` under
    it with their own tab current; the film starts `--site-page-top` under the tabs, and
    the application the tabs' own space under them."""
    for name, (path, current, below) in section_pages.items():
        page = browser.new_page(
            viewport={"width": width, "height": 900}, reduced_motion=REDUCED_MOTION
        )
        try:
            page.goto(path.as_uri(), wait_until="load")
            found = page.evaluate(HEADER)
        finally:
            page.close()
        where = f"{name} at {width}"
        assert tabs_problems(found) == [], where
        nav, rule, tabs, first = (found[part] for part in ("nav", "rule", "tabs", "first"))
        assert rule["on"] == "nav.site-nav", where
        assert rule["bottom"] == nav["bottom"], where
        assert (rule["left"], rule["right"]) == (nav["left"], nav["right"]), where
        assert tabs["current"] == current, where
        assert tabs["top"] - rule["bottom"] == pytest.approx(TABS_SPACE * REM, abs=0.05), where
        assert first["top"] - tabs["bottom"] == pytest.approx(below * REM, abs=0.05), where


def test_tabs_over_the_rule_are_caught(
    browser: Any, section_pages: dict[str, tuple[Path, str, float]]
) -> None:
    """The control: give the header that holds the tabs its lower border back, as it had
    while the tabs stood over the rule, and the check names the tabs on both pages."""
    for name, (path, _, _) in section_pages.items():
        page = browser.new_page(
            viewport={"width": 1280, "height": 900}, reduced_motion=REDUCED_MOTION
        )
        try:
            page.goto(path.as_uri(), wait_until="load")
            page.add_style_tag(content=RULE_UNDER_THE_TABS)
            problems = tabs_problems(page.evaluate(HEADER))
        finally:
            page.close()
        assert len(problems) == 1, name
        assert problems[0].startswith("the section tabs start "), name
        owner = "header.site-headroom" if name == "visualize.html" else "header"
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
    section_pages: dict[str, tuple[Path, str, float]],
) -> None:
    """At a desktop, a tablet and a phone width, on a page of prose, on the film's page
    and on the workbench: a link in the bar and a section tab are smaller than the body's
    prose and no smaller than the first step of the paper's scale under it, the two are
    one size, and the site's name is at least the body's size. Nothing here is a pixel
    value: the body is the prose base the page resolves, which a prose paragraph is set
    at, and the step is read from the same scale. The larger type leaves the bar's links
    on one line on a desktop and a tablet and two on a phone, and no page wider than its
    window."""
    opened = {
        "atlas.html": pages["atlas.html"],
        **{name: path for name, (path, _, _) in section_pages.items()},
    }
    seen: dict[str, set[tuple[float, float | None, float]]] = {name: set() for name in opened}
    for width, rows in BAR_WIDTHS.items():
        for name, path in opened.items():
            sizes = _header(browser, path, width)["type"]
            where = f"{name} at {width}"
            assert type_problems({"type": sizes}) == [], where
            body, scale = sizes["scale"]["prose"], sizes["scale"]
            below = max(step for step in scale.values() if step < body)
            assert below <= sizes["link"] < body <= sizes["name"], where
            assert sizes["name_shown"] is (width == 1280), where
            assert (sizes["links_rows"], sizes["overflow"]) == (rows, 0), where
            if name == "atlas.html":
                assert sizes["body"] == body, where
                assert sizes["tab"] is None, where
            else:
                assert sizes["tab"] == sizes["link"], where
            seen[name].add((sizes["link"], sizes["tab"], sizes["name"]))
    # One size at every width, and the same bar on every page.
    assert all(len(found) == 1 for found in seen.values()), seen
    assert len({next(iter(found))[::2] for found in seen.values()}) == 1, seen


def test_a_bar_set_smaller_than_one_step_under_the_body_is_caught(
    browser: Any, section_pages: dict[str, tuple[Path, str, float]]
) -> None:
    """The control: give the bar and the tabs the sizes they had, in rem and not from the
    body's scale, and the check names the links, the tabs and the name."""
    path = section_pages["visualize.html"][0]
    problems = type_problems(_header(browser, path, 1280, style=OLD_BAR_TYPE))
    assert [problem.split(":")[0] for problem in problems] == [
        "a link in the header is 16px",
        "a tab in the header is 14.4px",
        "a section tab is 14.4px and a link in the bar 16px",
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
    section_pages: dict[str, tuple[Path, str, float]],
) -> None:
    """At a desktop, a tablet and a phone width, on a page of prose, on the film's page
    and on the workbench: every link on a line of the bar stands on one baseline, the
    section tabs on one of theirs, and the site's name, where its text is shown, on the
    links', each within half a pixel. The name's text is shown only on the desktop; on
    the tablet and the phone the mark alone leads home and there is no name to align.
    The mark is centred on the name's line. Aligning the name moves nothing else: the
    current link's baseline is as far over the rule with the name beside it as without,
    and the current tab's as far over the foot of its strip at every width."""
    opened = {
        "atlas.html": pages["atlas.html"],
        **{name: path for name, (path, _, _) in section_pages.items()},
    }
    over_rule: dict[int, set[float]] = {}
    over_foot: set[float] = set()
    for width, rows in BAR_WIDTHS.items():
        for name, path in opened.items():
            found = _baselines(browser, path, width)
            where = f"{name} at {width}"
            assert baseline_problems(found) == [], where
            lines = {link["top"] for link in found["links"]}
            assert len(lines) == rows, where
            assert len(found["links"]) == 7, where
            first = min(found["links"], key=lambda link: link["top"])
            if width == 1280:
                assert abs(found["name"] - first["baseline"]) <= BASELINE_TOLERANCE, where
            else:
                assert found["name"] is None, where
            assert len(found["tabs"]) == (0 if name == "atlas.html" else 2), where
            if rows == 1:
                over_rule.setdefault(width, set()).add(found["current_above_rule"])
            if found["tabs"]:
                over_foot.add(round(found["current_tab_above_foot"], 1))
    # With the name (1280) and without it (768), on every page: one distance.
    assert len(set().union(*over_rule.values())) == 1, over_rule
    assert len(over_foot) == 1, over_foot


def test_a_name_aligned_by_its_mark_is_caught(browser: Any, pages: dict[str, Path]) -> None:
    """The control: let the name's row take its baseline from its first item again, the
    mark, and the check names the name, some pixels above the links."""
    found = _baselines(browser, pages["atlas.html"], 1280, style=NAME_ALIGNED_BY_ITS_MARK)
    problems = baseline_problems(found)
    assert len(problems) == 1, problems
    assert problems[0].startswith("the site's name stands -"), problems
    assert problems[0].endswith("px off the baseline of the bar's links"), problems
