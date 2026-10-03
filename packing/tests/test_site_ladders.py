"""The rating ladders hold their rows at every width, in a browser.

Verification Ladders is one diagram of three ladders (`templates/paper-design.md`,
Rating ladders): every rung is the same height, a chip and a description that is a box of
exactly two lines its words never run past, with no tally of results and no rule between
the rows. Whether a text takes two lines is the browser's to say, from the face and the
cell's width, so this opens the rendered results page in Chromium (the diagram was the
overview's until 2026-10-02) and measures the diagram
with the probe `devtools.measure_site_pages ladders` reports from, at the widths the
design is shot at and at the ones where a description is narrowest: 716 pixels, the least
window that sets three columns, and 715, where the ladders stack; 768, where the page's
margin widens and the wide track is 4 pixels more than at 716; 973, the least that sets
a rung's description beside its chip in three columns, and 972, the widest that sets it
under; and on a phone 360, 320 and 318, the least that sets it beside, with 317 under. At
each the diagram also stands inside whatever clips the page sideways, with the wide
track's gutter either side.

The page is rendered and loaded once, in a module fixture, and resized for each width.
Skipped where no Chromium can be launched; `SQPACK_CHROMIUM` names one the environment
supplies, as the other browser tools read it.
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

from devtools import overview_sections
from devtools.measure_site_pages import LADDERS
from devtools.render_n11_lower_bounds_explainer_pdf import BROWSER_OVERRIDE
from tests import site_renders

#: Each width measured, and how many columns the rungs stand in there.
WIDTHS = {
    1280: 3,
    1024: 3,
    973: 3,
    972: 3,
    768: 3,
    716: 3,
    715: 1,
    390: 1,
    360: 1,
    320: 1,
    318: 1,
    317: 1,
}
#: The widths at which a cell has 17.85rem, the widest rail's, significance's, with the
#: gap and the least description, so a rung's description stands beside its chip; at
#: the others it lies under the chip, across the cell. The cells turned at 16.5rem, the
#: chips' rail's, from a 908-pixel window and on a phone from 296, until significance
#: took marks in a wider rail (2026-10-03).
BESIDE = frozenset({1280, 1024, 973, 715, 390, 360, 320, 318})
#: A rung's height in pixels where its description stands beside its chip, and where it
#: lies under it: the two lines, or the chip's line and the two, and 0.4rem
#: (`--site-ladders-row-space`) above and below, which is all that parts the rows.
RUNG_HEIGHT = {True: 64.1, False: 91.8}
#: The diagram's one rule, under each column's head, in pixels.
HEAD_RULE = 1
#: `--site-ladders-meaning-min`, 13.5rem, in pixels: the narrowest a description is set.
MEANING_MIN = 216
#: How much narrower a significance description is than the others where it stands
#: beside its rail: its rail, `--site-ladders-significance-rail`, 3.6rem, over the chips',
#: `--site-ladders-rail`, 2.25rem, in pixels.
SIGNIFICANCE_RAIL_MORE = 21.6
#: `--site-wide-gutter`, 0.5rem, in pixels: the least room either side of a wide block.
GUTTER = 8


@pytest.fixture(scope="module")
def diagrams(tmp_path_factory: pytest.TempPathFactory) -> Iterator[dict[int, dict[str, Any]]]:
    """The overview's one ladder diagram as laid out at each of `WIDTHS`."""
    sync_api = pytest.importorskip("playwright.sync_api")
    # The diagram is the results page's since 2026-10-02, under its table.
    path = Path(tmp_path_factory.mktemp("site")) / "all-results.html"
    path.write_text(site_renders.html("all-results.html"), encoding="utf-8")
    with sync_api.sync_playwright() as driver:
        try:
            browser = driver.chromium.launch(executable_path=os.environ.get(BROWSER_OVERRIDE))
        except sync_api.Error as error:
            pytest.skip(f"no Chromium to launch: {error.message.splitlines()[0]}")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto(path.as_uri(), wait_until="load")
        page.wait_for_timeout(300)
        found: dict[int, dict[str, Any]] = {}
        for width in WIDTHS:
            page.set_viewport_size({"width": width, "height": 900})
            page.wait_for_timeout(100)
            (found[width],) = page.evaluate(LADDERS)
        browser.close()
        yield found


@pytest.mark.parametrize("width", WIDTHS)
def test_every_rung_is_one_height_and_its_description_two_lines(
    diagrams: dict[int, dict[str, Any]], width: int
) -> None:
    """At every width each rung's cell is the same height, its description's box is two
    lines tall and at least the least width, and no description takes a third line or
    runs past its box, so nothing has to be clipped. Each ladder's descriptions are one
    width, verification's and confirmation's the same; significance's, beside the wider
    rail its marks take, are that much narrower where they stand beside it, and the same
    where they lie under it."""
    diagram = diagrams[width]
    rungs = diagram["rungs"]
    assert len(rungs) == len(overview_sections.rung_meanings())
    assert diagram["columns"] == WIDTHS[width]
    assert len(diagram["heights"]) == 1, diagram["heights"]
    assert {rung["beside"] for rung in rungs} == {width in BESIDE}
    assert diagram["heights"][0] == pytest.approx(RUNG_HEIGHT[width in BESIDE], abs=0.2)
    widths = {
        ladder: {rung["meaning_width"] for rung in rungs if rung["ladder"] == ladder}
        for ladder in ("S", "V", "C")
    }
    assert all(len(found) == 1 for found in widths.values()), widths
    (significance,), (verification,), (confirmation,) = widths.values()
    assert verification == confirmation
    more = SIGNIFICANCE_RAIL_MORE if width in BESIDE else 0
    assert verification - significance == pytest.approx(more, abs=0.2)
    for rung in rungs:
        assert rung["parts"] == 2, rung
        assert rung["meaning"] == overview_sections.rung_short_meanings()[rung["rung"]]
        assert rung["title"] == overview_sections.rung_meanings()[rung["rung"]]
        assert rung["meaning_height"] == pytest.approx(2 * rung["line_height"], abs=0.2), rung
        assert rung["meaning_width"] >= MEANING_MIN - 0.5, rung
        assert 1 <= rung["lines"] <= 2, rung
        assert rung["overflow"] == 0, rung


@pytest.mark.parametrize("width", WIDTHS)
def test_one_rule_stands_under_the_heads_and_none_between_the_rows(
    diagrams: dict[int, dict[str, Any]], width: int
) -> None:
    """At every width the diagram's only rule is the one under each column's head: no
    cell draws a rule above or below itself, in three columns or stacked, so the rows are
    parted by their space alone."""
    diagram = diagrams[width]
    assert diagram["head_rules"] == [HEAD_RULE]
    assert diagram["row_rules"] == [0]


@pytest.mark.parametrize("width", WIDTHS)
def test_the_rungs_line_up_across_three_columns_and_stack_by_ladder_on_a_phone(
    diagrams: dict[int, dict[str, Any]], width: int
) -> None:
    """In three columns the rungs of one level share a row, significance first and the
    highest level at the top, and the level significance lacks leaves an empty cell as
    tall as its row. On a phone each ladder is a block of its own in the same order, and
    the missing rung takes no room."""
    diagram = diagrams[width]
    rungs = diagram["rungs"]
    assert diagram["heads"] == [name for _, name, _, _ in overview_sections.DIMENSIONS]
    order = [scale for scale, *_ in overview_sections.DIMENSIONS]
    by_place = sorted(rungs, key=lambda rung: (rung["top"], rung["column"]))
    if WIDTHS[width] == 3:
        assert all(rung["column"] == order.index(rung["ladder"]) + 1 for rung in rungs)
        tops = {int(rung["rung"][1]): set[int]() for rung in rungs}
        for rung in rungs:
            tops[int(rung["rung"][1])].add(rung["top"])
        assert all(len(found) == 1 for found in tops.values()), tops
        assert sorted(tops, key=lambda level: min(tops[level])) == [5, 4, 3, 2, 1, 0]
        assert diagram["empty"] == diagram["heights"]
    else:
        ladders = [rung["rung"] for rung in by_place]
        assert ladders == [
            f"{scale}{level}"
            for scale in order
            for level in range(5, -1, -1)
            if f"{scale}{level}" in overview_sections.rung_meanings()
        ]
        assert all(height <= 1 for height in diagram["empty"])


@pytest.mark.parametrize("width", WIDTHS)
def test_the_diagram_stands_inside_what_clips_the_page_with_a_gutter_either_side(
    diagrams: dict[int, dict[str, Any]], width: int
) -> None:
    """At every width the diagram is centred, and it stops at least the wide track's
    gutter short of the nearest ancestor that clips sideways, or of the page's edge where
    none does, so no rule and no letter of it is cut or set flush to the edge."""
    diagram = diagrams[width]
    assert diagram["gutter_left"] >= GUTTER - 0.5, diagram["frame"]
    assert diagram["gutter_right"] >= GUTTER - 0.5, diagram["frame"]
    assert diagram["gutter_left"] == pytest.approx(diagram["gutter_right"], abs=0.5)
