"""The frontier atlas's table as a reader has it, in a browser.

Each row leads with the drawing of its best known packing in a column of its own, under
no heading; then the case number, bold; then the star of a recent bound; then the status,
the four bounds, the gap and the records (`templates/paper-design.md`, Frontier table).
Every cell is centred on its row's height, a closed form has its decimal under it, and
the ten columns fit the 1200 pixels a 1280-pixel window gives the table.

Where a column ends, which rule centres a cell and how tall a row comes out are the
browser's to say, from the faces, the typeset formulas and the rules `site.css` gives
the table. So this opens the rendered page in Chromium, its math typeset, and reads the
table through one probe at 1280, 1024 and 768 pixels and at 390, where the same table
scrolls sideways in its wrap (the frontier has no card layout). It then uses the table
as a reader does: sorts it, filters it, opens a row's popover from its drawing and a
case's record from its number.

The browser is launched as `tests.site_browser` launches it: the pinned Chromium, or the
one `SQPACK_CHROMIUM` names, with its text unhinted so that the pixels pinned here read
the same on Linux as on macOS, where they were measured; skipped where none can be
launched, unless the run requires one.
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools.preview_site import settle_math
from devtools.render_frontier_page import recent_lower_bounds
from sqpack.probes import probe
from tests import site_browser, site_renders
from tests.test_frontier_page import COLUMNS, column

PROBES = Path(__file__).resolve().parent / "probes"
LAYOUT = probe(PROBES, "site_frontier_table/layout")

#: The widths the table is read at: the one its track is sized for, two it scrolls
#: sideways at, and a phone.
WIDTHS = (1280, 1024, 768, 390)
#: The rows read: a row of whole numbers (the shortest a row can be), a radical with its
#: credit, the proved case with a root shown as a decimal and the longest credited name,
#: a fraction that is a recent bound, a verified bound printed beside the reported one,
#: and a three-digit case with a rational upper bound. The fraction was n = 18's until
#: 2026-10-02, when its verified bound rose to the reported one, and then n = 19's until
#: the same happened there later that day; n = 12's has terminated since 5 October. The
#: verified bound beside the reported one was n = 51's, 37/5 and from the morning of 6
#: October 2977/400 (T-070), until sqverify-fast decided its own certificate (T-090) later
#: that day, and is n = 96's since.
CASES = (1, 5, 11, 12, 51, 70, 96, 108, 230)
ROWS = [f"n-{n}" for n in CASES]
#: The drawing's side before it had a column: 2.6rem.
OLD_THUMB = 41.6
#: The site's bold in a sans table, `--site-font-weight-sans-bold`.
BOLD = "680"
#: A cell's padding above and below, 0.55rem, in pixels.
PADDING = 8.8
#: How far two middles may sit apart and still read as level: a pixel, and the half
#: pixel a box lands off the grid.
LEVEL = 1.5


@pytest.fixture(scope="module")
def page(tmp_path_factory: pytest.TempPathFactory) -> Iterator[Any]:
    """The rendered Atlas, or SQPACK_SITE_PREVIEW_URL's existing local build."""
    sync_api = site_browser.api()
    live = os.environ.get("SQPACK_SITE_PREVIEW_URL")
    if live:
        address = f"{live.rstrip('/')}/atlas.html"
    else:
        root = Path(tmp_path_factory.mktemp("site"))
        address = site_renders.write(root, "atlas.html")["atlas.html"].as_uri()
    with sync_api.sync_playwright() as driver:
        browser = site_browser.launch(driver)
        opened = browser.new_page(viewport={"width": WIDTHS[0], "height": 900})
        opened.goto(address, wait_until="load")
        settle_math(opened)
        yield opened
        browser.close()


@pytest.fixture(scope="module")
def laid(page: Any) -> dict[int, dict[str, Any]]:
    """The table as laid out at each width, read before any test sorts or filters it."""
    found: dict[int, dict[str, Any]] = {}
    for width in WIDTHS:
        page.set_viewport_size({"width": width, "height": 900})
        page.wait_for_timeout(150)
        found[width] = page.evaluate(LAYOUT, {"rows": ROWS})
    page.set_viewport_size({"width": WIDTHS[0], "height": 900})
    page.wait_for_timeout(150)
    return found


@pytest.mark.parametrize("width", WIDTHS)
def test_the_drawing_has_the_first_column_under_no_heading(
    laid: dict[int, dict[str, Any]], width: int
) -> None:
    """The columns are the ten in their order. The first shows no heading and is named
    "Packing" for a screen reader; each row's first cell is the drawing and nothing
    else, a square larger than the 41.6 pixels it was under the number, and its column
    is the drawing and the row's start padding, with no room to spare."""
    table = laid[width]
    head = table["head"]
    assert [cell["words"] for cell in head] == COLUMNS
    assert head[0]["label"] == "Packing"
    assert head[0]["sorts"] is None
    assert all(cell["label"] is None for cell in head[1:])
    sides = set()
    for row in table["rows"]:
        thumb = row["thumb"]
        assert thumb["index"] == 0, row["id"]
        assert thumb["alone"], row["id"]
        assert thumb["width"] == thumb["height"], row["id"]
        sides.add(thumb["width"])
        # The number starts after the drawing, in the next column.
        assert row["n"]["left"] > thumb["left"] + thumb["width"], row["id"]
    (side,) = sides
    assert OLD_THUMB + 4 < side < OLD_THUMB * 1.3
    assert side < head[0]["width"] <= side + 10


@pytest.mark.parametrize("width", WIDTHS)
def test_the_drawing_makes_no_row_taller_than_its_text(
    laid: dict[int, dict[str, Any]], width: int
) -> None:
    """The drawing is two lines of the table's text high, and every row has two lines
    at least, the case file's link over the link to the case's record. So in the
    shortest row, one of whole numbers, the drawing and the Records cell's two lines
    each fill the cell's height between its padding, and the row is no taller than those
    two lines need."""
    shortest = laid[width]["rows"][ROWS.index("n-1")]
    thumb, records = shortest["cells"][0], shortest["cells"][column("Records")]
    assert shortest["height"] == min(row["height"] for row in laid[width]["rows"])
    assert shortest["height"] == pytest.approx(shortest["thumb"]["height"] + 2 * PADDING, abs=1)
    for cell in (thumb, records):
        assert cell["above"] == pytest.approx(0, abs=1)
        assert cell["below"] == pytest.approx(0, abs=1)


@pytest.mark.parametrize("width", WIDTHS)
def test_the_case_number_is_bold_and_level_with_the_drawing(
    laid: dict[int, dict[str, Any]], width: int
) -> None:
    """A row's `n` is the number alone, in the site's bold, and the middle of its text
    is the middle of the drawing beside it, in a short row and in a tall one."""
    for row, n in zip(laid[width]["rows"], CASES, strict=True):
        assert row["n"]["words"] == str(n)
        assert row["n"]["weight"] == BOLD, row["id"]
        assert row["n"]["middle"] == pytest.approx(row["thumb"]["middle"], abs=LEVEL), row["id"]


@pytest.mark.parametrize("width", WIDTHS)
def test_every_cell_is_centred_on_its_row(laid: dict[int, dict[str, Any]], width: int) -> None:
    """Every body cell is set to the middle of its row, and the cells of plain text and
    the drawing show it: what each holds has the same room above it as below. (A typeset
    formula's own box reaches past its line, so a cell of math is held to the rule and
    not to the measurement.) The header keeps the foot of its cell and still sticks."""
    table = laid[width]
    for cell in table["head"]:
        assert cell["vertical_align"] == "bottom"
        assert cell["position"] == "sticky"
    assert len({cell["top"] for cell in table["head"]}) == 1
    plain = [column(label) for label in ("", "n", "Status", "Records")]
    for row in table["rows"]:
        assert [cell["vertical_align"] for cell in row["cells"]] == ["middle"] * len(COLUMNS)
        for index in plain:
            cell = row["cells"][index]
            assert cell["above"] == pytest.approx(cell["below"], abs=2), (row["id"], index)
    # A tall row: the status chip of n = 12 sits well clear of the top of its cell.
    tall = table["rows"][ROWS.index("n-12")]
    assert tall["height"] > table["rows"][ROWS.index("n-1")]["height"] + 20
    assert tall["cells"][column("Status")]["above"] > 20


def test_the_table_fits_its_track_at_1280_and_scrolls_in_its_wrap_below(
    laid: dict[int, dict[str, Any]],
) -> None:
    """At a 1280-pixel window the ten columns fit the table's track, so nothing scrolls
    sideways; before the drawing had its column the table ran 82 pixels past it. Below
    that the table keeps its width and scrolls inside its wrap, and at no width does the
    page itself scroll sideways. The star's column is as narrow as its heading, and `n`
    narrower still."""
    wide = laid[1280]
    assert wide["scrolls"] == 0, wide["table_width"]
    assert wide["table_width"] <= wide["frame_width"]
    widths = {cell["words"]: cell["width"] for cell in wide["head"]}
    assert widths["n"] < 50
    assert widths["Recent"] < 96
    # At 1280 the table is stretched to its track; below it keeps its own width, the same
    # at every narrower window: 1192 pixels since the table has no frame (2026-10-02,
    # think-wadm), 1194 before, and 1180 since 3 October 2026, when an exact gap with a
    # numerator or denominator of more than eight digits became its decimal (n = 68's
    # 4512425581603/15625000000000 was the widest gap; GAP_DIGITS), and 1165 since 6
    # October 2026, when Evan Daniel's exact optima (T-098) put the upper lane of 48
    # counts, n = 68 among them, at their certified sides and narrowed the gap column.
    own = laid[WIDTHS[1]]["table_width"]
    assert own <= wide["table_width"]
    assert own == pytest.approx(1165, abs=10)
    for width in WIDTHS[1:]:
        assert laid[width]["scrolls"] > 0, width
        assert laid[width]["table_width"] == pytest.approx(own, abs=1), width
    assert [laid[width]["page_scrolls"] for width in WIDTHS] == [0] * len(WIDTHS)


def test_a_fraction_shows_its_decimal_and_a_name_stays_whole(
    laid: dict[int, dict[str, Any]],
) -> None:
    """The best known packing of n = 230 is `15 + (28/41)`, and the cell prints its decimal
    under it: the value cut after eight places. The example was n = 12's reported lower
    bound, `31360/7901`, then its verified one, `15680000/3949423`, until T-095's
    terminating `7943/2000` took both of n = 12's lower cells on 5 October 2026. A
    credit's longest name, in the row above n = 12, is set on one line."""
    rows = {row["id"]: row for row in laid[1280]["rows"]}
    upper = rows["n-230"]["cells"][column("Best known packing")]["approx"]
    assert upper == ["≈ 15.68292682…"]
    exact, shown = Fraction(643, 41), Fraction(upper[0][2:-1])
    assert 0 < exact - shown < Fraction(1, 10**8)
    # n = 12 since 5 October 2026: one lower bound in both lower cells, so the verified
    # cell repeats no decimal, and the gap 57/2000; both decimals terminate.
    assert rows["n-12"]["cells"][column("Reported lower")]["approx"] == ["= 3.9715"]
    assert rows["n-12"]["cells"][column("Gap")]["approx"] == ["= 0.0285"]
    assert [cell["approx"] for cell in rows["n-12"]["cells"]].count([]) == len(COLUMNS) - 2
    # A terminating fraction shows its exact decimal in either column: n = 12's above in
    # the reported one, and in the verified one a bound printed beside a different
    # reported one. That example was n = 18 until 2026-10-02, when T-045's replay raised
    # its verified bound to the reported 939/200 and the cell became "same", and then
    # n = 19 until T-074's did the same there later that day; then n = 51, 37/5 from
    # n = 50's replayed mixed certificate below its own reported mixed certificate,
    # 747/100 (T-090; 373/50, T-082, until 5 October), and from the morning of 6 October
    # its own replayed rectangle certificate, 2977/400 (T-070), until sqverify-fast
    # decided T-090's certificates later that day. Since then it is n = 96, 1993/200 by
    # mass from n = 95 (T-090) below the reported s(96) = 10 (T-081), and from later that
    # day its own certificate's 997/100 (T-082), decided here by sqverify-fast.
    assert rows["n-96"]["cells"][column("Verified lower")]["approx"] == ["= 9.97"]
    assert all(cell["approx"] == [] for cell in rows["n-1"]["cells"])
    assert rows["n-11"]["cells"][column("Reported lower")]["broken"] == []


def test_the_table_still_sorts_filters_and_opens(page: Any, laid: dict[int, Any]) -> None:
    """The columns moved and the script did not: a heading sorts its own column and the
    filters narrow the rows. A row opens its case's record, which is fetched, so that is
    held where the page is served (`test_site_case_records`); here, from a file, a row is
    one control that names its record."""
    assert laid
    shown = page.locator("#frontier-table tbody tr:not([hidden])")
    recent = page.locator("#frontier-table thead th", has_text="Recent")
    recent.click()
    assert recent.get_attribute("aria-sort") == "ascending"
    assert shown.first.get_attribute("data-recent") == "false"
    recent.click()
    assert recent.get_attribute("aria-sort") == "descending"
    # Which floors are recent is the citation record's to say, not this test's: since
    # 2026-10-02 the open floors rest on Karakus 2026 and s(k^2-2) on a 2026 Lean proof.
    starred = sorted(n for n, is_recent in recent_lower_bounds().items() if is_recent)
    assert shown.first.get_attribute("id") == f"n-{starred[0]}"
    number = page.locator("#frontier-table thead th.site-col-n")
    number.click()
    number.click()
    assert number.get_attribute("aria-sort") == "descending"
    assert shown.first.get_attribute("id") == "n-324"
    number.click()
    assert shown.first.get_attribute("id") == "n-1"
    # The heading with no words sorts nothing and is no tab stop.
    assert page.locator("#frontier-table thead th.site-thumb").get_attribute("tabindex") is None

    # 27 recent cases until 2026-10-02, when the merged rectangle replays (T-045, T-070)
    # and s(59), s(60) and s(61) made 44; the replays recorded later that day (T-048,
    # T-069, T-071, T-074 and s(77), s(78)) made 60; T-064's replay of 3 October, which
    # proved nine k^2 - 3 cases, made 69; T-075's replays the same day took n = 83, 91 and
    # 96 off Nagamochi's bound and made 72; T-080's replayed linear certificate took
    # n = 101 to 105 off it and made 77; T-076's replayed linear certificate took n = 82
    # off it and made 78, the cases `recent_lower_bounds` names. Since the correction of
    # 2 October 2026 was merged with those on 3 October, the corrected floors (Karakus
    # 2026, the Lean s(k^2-2) proof) are recent as well, so the count is read from the
    # citation record rather than pinned here.
    page.get_by_label("recent only").check()
    count = page.locator(".site-table-tools .site-count").inner_text()
    assert count == f"{len(starred)} of 324 cases"
    assert shown.count() == len(starred)
    assert shown.first.get_attribute("id") == f"n-{starred[0]}"
    page.get_by_label("recent only").uncheck()
    assert shown.count() == 324

    row = page.locator("#n-12")
    row.scroll_into_view_if_needed()
    assert row.get_attribute("data-case-href") == "cases/12.html"
    assert row.get_attribute("tabindex") == "0"
    assert row.get_attribute("aria-controls") == "pop-case"
    assert row.locator("td.site-col-n a").get_attribute("href") == "cases/12.html"
