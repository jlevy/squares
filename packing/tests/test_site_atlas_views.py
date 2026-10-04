"""The homepage's atlas in its two views, the grid and the triangle, and its two
drawings, house and regularized, in a browser.

The atlas is one set of tiles under two tabs (`templates/paper-design.md`, Atlas views).
The grid is the stylesheet's alone. The triangle sets row k as the 2k - 1 cases a square
of side k holds, ending at k squared on the right edge, and wraps a row too long for the
page: `overview/atlas-view.js` says where each tile stands and moves the tiles between
the views. `tests/node/overview_atlas_view` holds the script's arithmetic; what a reader
gets is the browser's to say, so this opens the rendered overview in Chromium and reads
it: where every tile stands in each view at a desktop width and on a phone, what a press
of a tab starts, what the keyboard does, what the address says, and what a reader who
asks for reduced motion sees. The drawing tabs beside the view tabs swap each case that
has a regularized view for that drawing, badged, in place (`overview/atlas-layer.js`):
the fixture reads that the swap moves nothing, holds through a change of view and the
expander, follows the keyboard and the address, and that a regularized tile is the link
to its case's record, as the house tile is.

One fixture drives the page through all of it and keeps what it read, so no test waits
on a browser in its own time. The layouts are read with the measuring tool's probe and
judged by its `layout_problems`, which `tests/test_measure_atlas_views.py` holds to the
shapes it must refuse.

Skipped where no Chromium can be launched; `SQPACK_CHROMIUM` names one the environment
supplies, as the other browser tools read it.
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from pathlib import Path
from typing import Any, TypedDict

import pytest

from devtools import measure_atlas_views as atlas
from devtools.render_n11_lower_bounds_explainer_pdf import BROWSER_OVERRIDE
from sqpack.probes import applied, probe
from tests import site_renders

PROBES = Path(__file__).resolve().parent / "probes"
PRESSED = probe(PROBES, "site_atlas_views/pressed")
INTERRUPTED = probe(PROBES, "site_atlas_views/interrupted")
WATCH = probe(PROBES, "site_atlas_views/watch")
SEEN = probe(PROBES, "site_atlas_views/seen")
ACTIONS = probe(PROBES, "site_atlas_views/actions")
DRAWING = probe(PROBES, "site_drawing_hover/drawing")

GRID, TRIANGLE = atlas.tab("grid"), atlas.tab("triangle")
HOUSE, REGULARIZED = atlas.layer_tab("house"), atlas.layer_tab("regularized")
#: The case whose tile is hovered and pressed.
CELL = '.site-atlas-cell[data-atlas-n="11"]'


class Window(TypedDict):
    """A window's size, as `atlas.open_atlas` and Playwright's viewport take it."""

    width: int
    height: int


#: A desktop window and a phone's.
DESKTOP: Window = {"width": 1280, "height": 900}
PHONE: Window = {"width": 390, "height": 844}
#: How far into a move the second press of an interrupted one comes, in milliseconds.
MID_MOVE = 120
#: Longer than `--site-hover-duration`, so a wash has finished.
SETTLE_MS = 400
#: The settled layouts the fixture reads, each in the view named.
LAYOUTS = {
    "grid": "grid",
    "triangle": "triangle",
    "grid again": "grid",
    "grid after a second press": "grid",
    "triangle, every case": "triangle",
    "triangle, collapsed": "triangle",
    "resized to a phone": "triangle",
    "phone": "triangle",
    "phone, every case": "triangle",
    "phone, grid": "grid",
    "reduced motion": "triangle",
    "linked": "triangle",
    "drawings, house": "grid",
    "drawings, regularized": "grid",
    "drawings, regularized triangle": "triangle",
    "drawings, house triangle": "triangle",
    "drawings, regularized every case": "triangle",
    "phone, regularized": "triangle",
}

type Readings = dict[str, Any]


def _places(report: dict[str, Any]) -> dict[int, tuple[float, float, float, float]]:
    """Every tile's box as it stands in the block: left and top from the block's own
    corner, so a page that has scrolled reads the same."""
    cells = report["cells"]
    return {
        tile["n"]: (
            round(tile["left"] - cells["left"], 1),
            round(tile["top"] - cells["top"], 1),
            round(tile["width"], 1),
            round(tile["height"], 1),
        )
        for tile in report["tiles"]
    }


def _same_places(one: dict[str, Any], other: dict[str, Any]) -> bool:
    """Whether two layouts set the same tiles in the same places, to a third of a pixel:
    a box is read from the window's corner, which rounds differently once the page has
    scrolled."""
    here, there = _places(one), _places(other)
    return sorted(here) == sorted(there) and all(
        abs(a - b) <= 0.3 for n in here for a, b in zip(here[n], there[n], strict=True)
    )


def _tabs(report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {tab["key"]: tab for tab in report["tabs"]}


def _desktop(browser: Any, address: str) -> Readings:
    """A desktop reader's session: to the triangle and back, a change of mind mid-move,
    the keyboard, a tile hovered and pressed, the expander, and a window made narrow."""
    seen: Readings = {}
    page = atlas.open_atlas(browser, address, **DESKTOP)
    atlas.top(page)
    seen["grid"] = atlas.layout(page)
    seen["actions"] = page.evaluate(ACTIONS)
    seen["press triangle"] = page.evaluate(PRESSED, {"press": TRIANGLE})
    atlas.settle(page)
    seen["triangle"] = atlas.layout(page)
    seen["press grid"] = page.evaluate(PRESSED, {"press": GRID})
    atlas.settle(page)
    seen["grid again"] = atlas.layout(page)
    seen["second press"] = page.evaluate(
        INTERRUPTED, {"first": TRIANGLE, "second": GRID, "wait": MID_MOVE}
    )
    atlas.settle(page)
    seen["grid after a second press"] = atlas.layout(page)

    page.locator(GRID).focus()
    for key in ("ArrowRight", "ArrowRight", "End", "Home", "ArrowLeft"):
        page.keyboard.press(key)
        atlas.settle(page)
        seen.setdefault("keys", []).append((key, atlas.layout(page)))
    order = []
    for _ in range(3):
        page.keyboard.press("Tab")
        order.append(atlas.layout(page)["focus"])
    seen["tab order"] = order

    cell = page.locator(CELL)
    page.mouse.move(1, 1)
    page.wait_for_timeout(SETTLE_MS)
    seen["tile at rest"] = page.evaluate(DRAWING, {"holder": CELL})
    cell.hover()
    page.wait_for_timeout(SETTLE_MS)
    seen["tile hovered"] = page.evaluate(DRAWING, {"holder": CELL})
    # A tile opens its case's record in the case popover, which fetches the record, so
    # that is held where the records are served (`test_site_case_records`); from a file,
    # a tile is the link to that record the popover opens.
    seen["tile link"] = {
        "href": cell.get_attribute("href"),
        "case": cell.get_attribute("data-case"),
    }

    # The expander is under the triangle, below the window: brought into it, as a reader
    # who presses it has it, so what follows the tiles is seen to move with them.
    page.locator(atlas.EXPANDER).scroll_into_view_if_needed()
    seen["press expander"] = page.evaluate(PRESSED, {"press": atlas.EXPANDER})
    atlas.settle(page)
    seen["triangle, every case"] = atlas.layout(page)
    seen["actions, expanded"] = page.evaluate(ACTIONS)
    atlas.expand(page)
    seen["triangle, collapsed"] = atlas.layout(page)

    page.set_viewport_size(PHONE)
    page.wait_for_function(
        probe(PROBES, "site_atlas_views/arranged"), arg={"per_line": 8}, timeout=5000
    )
    seen["resized to a phone"] = atlas.layout(page)
    page.close()
    return seen


def _phone(browser: Any, address: str) -> Readings:
    """A phone opened on the triangle's own address, then every case, then the grid."""
    seen: Readings = {}
    page = atlas.open_atlas(
        browser, address, view="triangle", init_script=applied(WATCH), **PHONE
    )
    seen["phone, first placed"] = page.evaluate(SEEN)
    seen["phone"] = atlas.layout(page)
    seen["phone actions"] = page.evaluate(ACTIONS)
    atlas.expand(page)
    seen["phone, every case"] = atlas.layout(page)
    page.locator(GRID).click()
    atlas.settle(page)
    seen["phone, grid"] = atlas.layout(page)
    page.close()
    return seen


def _reduced(browser: Any, address: str) -> Readings:
    """A reader who asks for reduced motion presses Triangle."""
    seen: Readings = {}
    page = atlas.open_atlas(browser, address, reduced_motion="reduce", **DESKTOP)
    seen["reduced press"] = page.evaluate(PRESSED, {"press": TRIANGLE})
    seen["reduced motion"] = atlas.layout(page)
    page.close()
    return seen


def _linked(browser: Any, address: str) -> Readings:
    """An address that names the triangle among other things: a filter of the recent
    table and the section's fragment."""
    seen: Readings = {}
    page = atlas.open_atlas(
        browser, address, query="?age=180&atlas=triangle#the-atlas", **DESKTOP
    )
    seen["linked"] = atlas.layout(page)
    page.locator(GRID).click()
    atlas.settle(page)
    seen["linked, to grid"] = atlas.layout(page)
    page.locator(TRIANGLE).click()
    atlas.settle(page)
    seen["linked, back"] = atlas.layout(page)
    page.close()
    return seen


def _drawings(browser: Any, address: str) -> Readings:
    """A desktop reader who changes the drawing: to Regularized and back in the grid and
    in the triangle, with every case shown, by the keyboard, and who presses a
    regularized tile and then a house one."""
    seen: Readings = {}
    page = atlas.open_atlas(browser, address, **DESKTOP)
    atlas.top(page)
    seen["drawings, house"] = atlas.layout(page)
    seen["press regularized"] = page.evaluate(PRESSED, {"press": REGULARIZED})
    atlas.settle(page)
    seen["drawings, regularized"] = atlas.layout(page)
    page.locator(TRIANGLE).click()
    atlas.settle(page)
    seen["drawings, regularized triangle"] = atlas.layout(page)
    seen["press house"] = page.evaluate(PRESSED, {"press": HOUSE})
    atlas.settle(page)
    seen["drawings, house triangle"] = atlas.layout(page)
    page.locator(REGULARIZED).click()
    page.locator(atlas.EXPANDER).scroll_into_view_if_needed()
    atlas.expand(page)
    seen["drawings, regularized every case"] = atlas.layout(page)

    page.locator(REGULARIZED).focus()
    for key in ("ArrowLeft", "ArrowRight", "Home", "End"):
        page.keyboard.press(key)
        atlas.settle(page)
        seen.setdefault("drawing keys", []).append((key, atlas.layout(page)))

    # A regularized tile is the link to its case's record, as a house tile is (above).
    first = min(seen["drawings, regularized"]["regularized"])
    tile = page.locator(f'.site-atlas-cell[data-atlas-n="{first}"]')
    seen["regularized tile link"] = {
        "n": first,
        "href": tile.get_attribute("href"),
        "case": tile.get_attribute("data-case"),
        "layer": tile.get_attribute("data-atlas-layer"),
    }
    page.close()
    return seen


def _phone_drawings(browser: Any, address: str) -> Readings:
    """A phone opened on an address that names the triangle and the regularized drawing."""
    seen: Readings = {}
    page = atlas.open_atlas(
        browser,
        address,
        view="triangle",
        layer="regularized",
        init_script=applied(WATCH),
        **PHONE,
    )
    seen["phone, regularized, first placed"] = page.evaluate(SEEN)
    seen["phone, regularized"] = atlas.layout(page)
    page.close()
    return seen


@pytest.fixture(scope="module")
def seen(tmp_path_factory: pytest.TempPathFactory) -> Iterator[Readings]:
    """Everything the four sessions read, by name."""
    sync_api = pytest.importorskip("playwright.sync_api")
    path = Path(tmp_path_factory.mktemp("site")) / "index.html"
    path.write_text(site_renders.html("index.html"), encoding="utf-8")
    address = path.as_uri()
    with sync_api.sync_playwright() as driver:
        try:
            browser = driver.chromium.launch(executable_path=os.environ.get(BROWSER_OVERRIDE))
        except sync_api.Error as error:
            pytest.skip(f"no Chromium to launch: {error.message.splitlines()[0]}")
        found: Readings = {}
        for session in (_desktop, _phone, _reduced, _linked, _drawings, _phone_drawings):
            found.update(session(browser, address))
        browser.close()
        yield found


def test_a_plain_address_opens_the_grid_under_its_two_tabs(seen: Readings) -> None:
    """With no parameter the atlas is the grid: its tab is selected and is the one stop
    in the tab order, both tabs show, in the section tabs' type, side by side, and the
    box of tiles is the panel they control, named by the selected tab."""
    grid = seen["grid"]
    assert grid["view"] == "grid"
    assert grid["search"] == ""
    tabs = _tabs(grid)
    assert list(tabs) == ["grid", "triangle"]
    assert [tab["label"] for tab in tabs.values()] == ["Grid", "Triangle"]
    assert (tabs["grid"]["selected"], tabs["grid"]["tabindex"]) == ("true", 0)
    assert (tabs["triangle"]["selected"], tabs["triangle"]["tabindex"]) == ("false", -1)
    assert all(tab["shown"] and tab["controls"] == grid["panel"]["id"] for tab in tabs.values())
    assert grid["panel"] == {
        "id": "atlas-cells",
        "role": "tabpanel",
        "labelledby": tabs["grid"]["id"],
    }
    # The strip's type is the bar's and the section tabs': the note step, 17.48px.
    assert {tab["font_px"] for tab in tabs.values()} == {17.48}
    assert tabs["grid"]["box"]["top"] == tabs["triangle"]["box"]["top"]
    assert tabs["grid"]["box"]["right"] <= tabs["triangle"]["box"]["left"] + 1
    assert len(grid["tiles"]) == 100


def test_pressing_triangle_moves_every_tile_on_its_transform_alone(seen: Readings) -> None:
    """A press starts one move a tile that is in the window, each an animation of
    `transform` and nothing else, for the duration and with the easing the tokens name.
    Nothing is animated that lays the page out. What follows the tiles moves with them
    where it is in the window, as the expander's row is when it is pressed."""
    for press, view in (("press triangle", "triangle"), ("press grid", "grid")):
        started = seen[press]
        assert started["view"] == view
        assert 0 < started["moving"] <= 100, press
        assert started["properties"] == ["transform"], press
        assert started["duration"] == 360
        assert started["easing"] == "cubic-bezier(0.2, 0, 0, 1)"
    assert seen["press expander"]["followers"] > 0


def test_the_triangle_sets_row_k_as_2k_minus_1_tiles_ending_at_the_right_edge(
    seen: Readings,
) -> None:
    """At a desktop width no row wraps: ten rows of 1, 3, 5, ... 19 tiles, each a line,
    and every perfect square's tile ends at the block's right edge."""
    triangle = seen["triangle"]
    assert triangle["view"] == "triangle"
    assert triangle["per_line"] == 19
    tiles = {tile["n"]: tile for tile in triangle["tiles"]}
    assert sorted(tiles) == list(range(1, 101))
    right = triangle["cells"]["right"]
    for k in range(1, 11):
        row = [tiles[n] for n in range((k - 1) ** 2 + 1, k * k + 1)]
        assert len(row) == 2 * k - 1
        assert len({tile["top"] for tile in row}) == 1, f"row {k} is not one line"
        assert abs(tiles[k * k]["right"] - right) <= atlas.EDGE, f"{k * k} is off the edge"
        lefts = [tile["left"] for tile in row]
        assert lefts == sorted(lefts)
    tops = [tiles[k * k]["top"] for k in range(1, 11)]
    assert tops == sorted(tops)
    assert len(set(tops)) == 10
    assert _tabs(triangle)["triangle"]["selected"] == "true"
    assert triangle["panel"]["labelledby"] == _tabs(triangle)["triangle"]["id"]


def test_toggling_back_puts_every_tile_where_the_grid_had_it(seen: Readings) -> None:
    assert _same_places(seen["grid again"], seen["grid"])
    assert seen["grid again"]["view"] == "grid"
    assert not _same_places(seen["triangle"], seen["grid"])


def test_a_second_press_mid_move_starts_from_where_the_tiles_are(seen: Readings) -> None:
    """Pressing Grid while the tiles are on their way to the triangle turns them round
    where they are: no drawing in the window jumps across the press, the tiles are
    moving after it, and they settle in the grid exactly, with the focus still on the
    tab pressed and the address the grid's."""
    second = seen["second press"]
    assert second["moving_before"] > 0
    assert second["moving_after"] > 0
    assert second["watched"] > 20
    assert second["jump"] < 1.5, second
    after = seen["grid after a second press"]
    assert after["view"] == "grid"
    assert after["moving"] == 0
    assert _same_places(after, seen["grid"])
    assert after["search"] == ""
    assert _tabs(after)["grid"]["focused"]


def test_the_arrow_keys_move_between_the_tabs_and_select_the_one_focused(
    seen: Readings,
) -> None:
    """The tablist's keys: Right and Left move to the next tab and the last wraps to the
    first, Home and End go to the ends, and the tab the focus lands on is selected, so
    the focus is never left behind on a tab that is not."""
    expected = {
        "ArrowRight": "triangle",
        "End": "triangle",
        "Home": "grid",
        "ArrowLeft": "triangle",
    }
    views = [(key, report["view"]) for key, report in seen["keys"]]
    assert views == [
        ("ArrowRight", "triangle"),
        ("ArrowRight", "grid"),
        ("End", expected["End"]),
        ("Home", expected["Home"]),
        ("ArrowLeft", expected["ArrowLeft"]),
    ]
    for key, report in seen["keys"]:
        tabs = _tabs(report)
        current = tabs[report["view"]]
        assert current["focused"], key
        assert (current["selected"], current["tabindex"]) == ("true", 0), key
        other = tabs["grid" if report["view"] == "triangle" else "triangle"]
        assert (other["selected"], other["tabindex"], other["focused"]) == ("false", -1, False)
        assert report["focus"] == current["id"]


def test_the_tiles_follow_the_tabs_in_the_tab_order_in_case_order(seen: Readings) -> None:
    """From the view tabs, in the triangle, Tab goes to the drawing tabs' one stop, House,
    and then to n = 1 and n = 2: the tiles keep the order of the cases whichever way
    they are set."""
    assert seen["tab order"] == ["atlas-layer-house", "1", "2"]


def test_the_address_names_the_triangle_and_keeps_what_else_it_holds(seen: Readings) -> None:
    """The triangle is `?atlas=triangle` and the grid no parameter; a press writes it
    without a new history entry's worth of change to anything else in the address."""
    assert seen["triangle"]["search"] == "?atlas=triangle"
    assert seen["grid again"]["search"] == ""
    linked = seen["linked"]
    assert (linked["view"], linked["search"], linked["hash"]) == (
        "triangle",
        "?age=180&atlas=triangle",
        "#the-atlas",
    )
    assert _tabs(linked)["triangle"]["selected"] == "true"
    to_grid = seen["linked, to grid"]
    assert (to_grid["view"], to_grid["search"], to_grid["hash"]) == (
        "grid",
        "?age=180",
        "#the-atlas",
    )
    back = seen["linked, back"]
    assert (back["view"], back["search"], back["hash"]) == (
        "triangle",
        "?age=180&atlas=triangle",
        "#the-atlas",
    )
    assert _same_places(back, linked)


def test_a_linked_triangle_is_the_triangle_before_a_tile_is_drawn(seen: Readings) -> None:
    """Opened on the triangle's address, the block is in the triangle, with every tile
    arranged and nothing in a move, at the moment its tiles are first put in the page:
    the grid is never shown first."""
    assert seen["phone, first placed"] == [
        {
            "view": "triangle",
            "layer": "house",
            "per_line": "8",
            "tiles": 100,
            "regularized": 0,
            "moving": 0,
        }
    ]


def test_reduced_motion_switches_at_once(seen: Readings) -> None:
    """For a reader who asks for reduced motion a press starts no move at all, of a tile
    or of anything after the tiles, and the triangle is complete as the press returns."""
    press = seen["reduced press"]
    assert (press["view"], press["moving"], press["followers"]) == ("triangle", 0, 0)
    reduced = seen["reduced motion"]
    assert reduced["view"] == "triangle"
    assert reduced["moving"] == 0
    assert _same_places(reduced, seen["triangle"])


def test_a_phone_wraps_the_long_rows_and_keeps_every_square_on_the_right_edge(
    seen: Readings,
) -> None:
    """At 390 pixels a line holds eight tiles of 40 pixels or more. Rows 1 to 4 fit; row
    10, nineteen tiles, is lines of 8, 8 and 3 in reading order. No tile runs past the
    block or the page, every perfect square ends at the block's right edge, and every
    line of a wrapped row but its last starts at the block's left edge."""
    phone = seen["phone"]
    assert phone["per_line"] == 8
    assert phone["overflow"] == 0
    cells = phone["cells"]
    tiles = {tile["n"]: tile for tile in phone["tiles"]}
    assert min(tile["width"] for tile in tiles.values()) >= 40
    for tile in tiles.values():
        assert tile["left"] >= cells["left"] - atlas.EDGE, tile["n"]
        assert tile["right"] <= cells["right"] + atlas.EDGE, tile["n"]
    for k in range(1, 11):
        assert abs(tiles[k * k]["right"] - cells["right"]) <= atlas.EDGE, k
        row = [tiles[n] for n in range((k - 1) ** 2 + 1, k * k + 1)]
        tops = sorted({tile["top"] for tile in row})
        sizes = tuple(sum(tile["top"] == top for tile in row) for top in tops)
        assert sizes == atlas.row_lines(k, 8), k
        for top in tops[:-1]:
            line = [tile for tile in row if tile["top"] == top]
            assert abs(min(tile["left"] for tile in line) - cells["left"]) <= atlas.EDGE, k
        # The cases read on in order along each line and down the lines.
        assert [tile["n"] for tile in sorted(row, key=lambda t: (t["top"], t["left"]))] == [
            tile["n"] for tile in row
        ]
    assert atlas.row_lines(10, 8) == (8, 8, 3)
    assert [k for k in range(1, 11) if len(atlas.row_lines(k, 8)) == 1] == [1, 2, 3, 4]


def test_the_space_over_a_row_is_larger_than_between_the_lines_of_one(seen: Readings) -> None:
    """Where rows wrap, a new row starts further below the line above it than a wrapped
    row's own lines stand apart, so the lines of a row read as one group."""
    tiles = {tile["n"]: tile for tile in seen["phone"]["tiles"]}
    # Row 10 at eight a line: 82 to 89, 90 to 97, 98 to 100. Row 9 ends at 81.
    within = tiles[90]["top"] - tiles[82]["bottom"]
    between = tiles[82]["top"] - tiles[81]["bottom"]
    assert within == pytest.approx(tiles[98]["top"] - tiles[90]["bottom"], abs=0.5)
    assert between > within + 10, (between, within)


def test_the_expander_works_in_the_triangle(seen: Readings) -> None:
    """Showing every case in the triangle moves the hundred into their smaller places
    and sets eighteen rows, the last of 35 tiles; collapsing puts the hundred back where
    they stood. On a phone all 324 wrap at eight a line."""
    assert seen["press expander"]["moving"] > 0
    every = seen["triangle, every case"]
    assert (every["view"], every["expanded"], every["per_line"]) == ("triangle", "true", 35)
    assert sorted(tile["n"] for tile in every["tiles"]) == list(range(1, 325))
    collapsed = seen["triangle, collapsed"]
    assert (collapsed["expanded"], collapsed["per_line"]) == ("false", 19)
    assert _same_places(collapsed, seen["triangle"])
    phone = seen["phone, every case"]
    assert (phone["per_line"], len(phone["tiles"])) == (8, 324)
    assert len(seen["phone, grid"]["tiles"]) == 324


def test_a_narrower_window_rearranges_the_triangle_without_a_move(seen: Readings) -> None:
    """Made a phone's width, the desktop's triangle is the phone's: the same tiles to a
    line and every tile where a phone opened on the triangle has it, with no move."""
    resized = seen["resized to a phone"]
    assert resized["per_line"] == 8
    assert resized["moving"] == 0
    assert _same_places(resized, seen["phone"])


@pytest.mark.parametrize("name", LAYOUTS)
def test_no_layout_runs_past_the_page_or_sets_a_tile_over_another(
    seen: Readings, name: str
) -> None:
    """Every settled layout, in either view and at either width: nothing in a move, no
    tile outside the block or over another, the cases in order, and in the triangle
    every square on the right edge and every row cut as `row_lines` gives."""
    report = seen[name]
    assert report["view"] == LAYOUTS[name]
    assert atlas.layout_problems(report) == []


def test_a_triangle_tile_keeps_its_ink_under_the_pointer(seen: Readings) -> None:
    """A tile washes on hover in the triangle as in the grid, and its drawing is stroked
    exactly as at rest (`test_site_drawing_hover` reads the grid's)."""
    rest, hovered = seen["tile at rest"], seen["tile hovered"]
    assert not rest["hover"]
    assert hovered["hover"]
    assert hovered["background"] != rest["background"]
    assert hovered["frame_stroke"] == rest["frame_stroke"] == rest["color"]
    assert hovered["outline_stroke"] == rest["outline_stroke"]


@pytest.mark.parametrize("name", ["actions", "phone actions"])
def test_see_all_results_and_the_expander_are_one_button(seen: Readings, name: str) -> None:
    """The link under the recent table and the button under the atlas are the site's one
    action under a table or grid: the same colours, type, padding, corners and height,
    each centred in its row, with its icon from the one set after its label at the same
    size, the arrow right on the link and the double chevron on the button; at a desktop
    width and on a phone."""
    see_all, expander = seen[name]["see_all"], seen[name]["expander"]
    assert see_all is not None
    assert expander is not None
    for key in ("color", "background", "font_px", "weight", "family", "padding", "radius"):
        assert see_all[key] == expander[key], (name, key)
    assert see_all["box"]["height"] == pytest.approx(expander["box"]["height"], abs=0.5)
    assert abs(see_all["centred"]) <= 1, (name, see_all["centred"])
    assert abs(expander["centred"]) <= 1, (name, expander["centred"])
    assert "site-action" in see_all["classes"]
    assert "site-action" in expander["classes"]
    assert see_all["icon"]["arrow"] == "right"
    assert expander["icon"]["arrow"] == "double-down"
    assert see_all["icon"]["width"] == pytest.approx(expander["icon"]["width"], abs=0.5)
    assert see_all["icon"]["after_text"]
    assert expander["icon"]["after_text"]
    assert see_all["label"] == "See all results"


def test_the_expander_reads_show_more_then_show_less_with_the_chevron_turned(
    seen: Readings,
) -> None:
    """Collapsed, the button reads Show More with the chevron down and is named for all
    the cases it shows; expanded, Show Less with the chevron up, named for the hundred it
    keeps; it says which it is and what it controls either way."""
    closed, opened = seen["actions"]["expander"], seen["actions, expanded"]["expander"]
    assert (closed["label"], closed["expanded"], closed["icon"]["arrow"]) == (
        "Show More",
        "false",
        "double-down",
    )
    assert closed["name"] == "Show more: all 324 cases"
    assert (opened["label"], opened["expanded"], opened["icon"]["arrow"]) == (
        "Show Less",
        "true",
        "double-up",
    )
    assert opened["name"] == "Show less: the first 100"
    assert closed["controls"] == opened["controls"] == "atlas-cells"


def test_a_triangle_tile_is_the_link_to_its_case_record(seen: Readings) -> None:
    assert seen["tile link"] == {"href": "cases/11.html", "case": "11"}


def _layers(report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {tab["key"]: tab for tab in report["layers"]}


def _drawn(report: dict[str, Any]) -> list[int]:
    """The cases a layout shows in their regularized drawing."""
    return [tile["n"] for tile in report["tiles"] if tile["layer"] == "regularized"]


def test_the_drawing_tabs_stand_beside_the_view_tabs_and_open_on_house(seen: Readings) -> None:
    """A plain address shows the house drawings, under a second strip on the view tabs'
    line and in their type: House selected and the strip's one stop in the tab order,
    Regularized after it, both controlling the box of tiles. The page has regularized
    drawings to offer, and none is shown."""
    house = seen["drawings, house"]
    assert (house["layer"], house["search"]) == ("house", "")
    layers = _layers(house)
    assert list(layers) == ["house", "regularized"]
    assert [tab["label"] for tab in layers.values()] == ["House", "Regularized"]
    assert (layers["house"]["selected"], layers["house"]["tabindex"]) == ("true", 0)
    assert (layers["regularized"]["selected"], layers["regularized"]["tabindex"]) == (
        "false",
        -1,
    )
    assert all(tab["shown"] and tab["controls"] == "atlas-cells" for tab in layers.values())
    views = _tabs(house)
    assert {tab["font_px"] for tab in layers.values()} == {views["grid"]["font_px"]}
    assert layers["house"]["box"]["top"] == views["grid"]["box"]["top"]
    assert layers["house"]["box"]["left"] > views["triangle"]["box"]["right"]
    assert house["regularized"], "the page offers no regularized drawing"
    assert _drawn(house) == []


def test_pressing_regularized_swaps_the_drawings_in_place_and_moves_nothing(
    seen: Readings,
) -> None:
    """A press of Regularized starts no move, of a tile or of anything after the tiles,
    and leaves every tile where it stood. Each shown case with a regularized view now
    shows it, badged, and every other case its house drawing; the address says so."""
    pressed = seen["press regularized"]
    assert (pressed["view"], pressed["moving"], pressed["followers"]) == ("grid", 0, 0)
    regularized = seen["drawings, regularized"]
    assert (regularized["layer"], regularized["search"]) == (
        "regularized",
        "?layer=regularized",
    )
    assert _same_places(regularized, seen["drawings, house"])
    shown = [n for n in regularized["regularized"] if n <= 100]
    assert shown, "no regularized view among the first hundred cases"
    assert _drawn(regularized) == shown
    assert _layers(regularized)["regularized"]["selected"] == "true"
    assert atlas.layout_problems(regularized) == []


def test_the_drawing_holds_through_a_change_of_view_and_house_puts_the_tiles_back(
    seen: Readings,
) -> None:
    """In the triangle the regularized tiles stand where the triangle places their cases,
    and House puts the house tiles back exactly there, with no move; the address keeps
    the view while the drawing comes and goes."""
    triangle = seen["drawings, regularized triangle"]
    assert (triangle["view"], triangle["layer"]) == ("triangle", "regularized")
    assert triangle["search"] == "?layer=regularized&atlas=triangle"
    assert _drawn(triangle) == [n for n in triangle["regularized"] if n <= 100]
    assert seen["press house"]["moving"] == 0
    house = seen["drawings, house triangle"]
    assert (house["layer"], house["search"]) == ("house", "?atlas=triangle")
    assert _drawn(house) == []
    assert _same_places(house, triangle)


def test_tiles_placed_later_take_the_drawing_the_block_is_in(seen: Readings) -> None:
    """The rest of the cases, placed when the expander is first pressed, arrive in the
    regularized drawing when the block is in it: every case with a view shows it."""
    every = seen["drawings, regularized every case"]
    assert (every["layer"], every["expanded"]) == ("regularized", "true")
    assert len(every["tiles"]) == 324
    assert _drawn(every) == sorted(every["regularized"])


def test_the_arrow_keys_move_between_the_drawing_tabs_and_select_the_one_focused(
    seen: Readings,
) -> None:
    keys = [(key, report["layer"]) for key, report in seen["drawing keys"]]
    assert keys == [
        ("ArrowLeft", "house"),
        ("ArrowRight", "regularized"),
        ("Home", "house"),
        ("End", "regularized"),
    ]
    for key, report in seen["drawing keys"]:
        current = _layers(report)[report["layer"]]
        assert current["focused"], key
        assert (current["selected"], current["tabindex"]) == ("true", 0), key


def test_a_regularized_tile_is_the_link_to_the_same_case_record(seen: Readings) -> None:
    """A regularized tile opens the record its house tile opens: the record's drawing is
    the house one, and the regularized layer is only the atlas's view of it."""
    tile = seen["regularized tile link"]
    n = tile["n"]
    assert tile == {"n": n, "href": f"cases/{n}.html", "case": str(n), "layer": "regularized"}


def test_a_linked_regularized_atlas_is_regularized_before_a_tile_is_drawn(
    seen: Readings,
) -> None:
    """Opened on an address that names the regularized drawing, the tiles are already
    the regularized ones when they are first put in the page, and the phone's layout of
    them, badges and all, has nothing wrong with it."""
    phone = seen["phone, regularized"]
    shown = len([n for n in phone["regularized"] if n <= 100])
    assert seen["phone, regularized, first placed"] == [
        {
            "view": "triangle",
            "layer": "regularized",
            "per_line": "8",
            "tiles": 100,
            "regularized": shown,
            "moving": 0,
        }
    ]
    assert phone["overflow"] == 0
    views, layers = _tabs(phone), _layers(phone)
    beside = layers["house"]["box"]["left"] >= views["triangle"]["box"]["right"]
    under = layers["house"]["box"]["top"] >= views["grid"]["box"]["bottom"]
    assert beside or under
