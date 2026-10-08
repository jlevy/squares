"""The homepage's atlas in its two views, the grid and the triangle, at its three sizes
of tile, and the marks its tiles carry, in a browser.

The atlas is one set of tiles under two tabs (`templates/paper-design.md`, Atlas views).
The grid is the stylesheet's alone. The triangle sets row k as the 2k - 1 cases a square
of side k holds, starting at the left edge and ending at k squared, and wraps a row too
long for the page: `overview/atlas-view.js` says where each tile stands and moves the
tiles between the views. `tests/node/overview_atlas_view` holds the script's arithmetic;
what a reader
gets is the browser's to say, so this opens the rendered overview in Chromium and reads
it: where every tile stands in each view at a desktop width and on a phone, what a press
of a tab starts, what the keyboard does, what the address says, and what a reader who
asks for reduced motion sees. The size tabs beside the view tabs make every tile
smaller or larger in either view (think-ht8t): the fixture reads that a change of size
moves the tiles as a change of view does, sets the sizes in order, follows the keyboard
and the address, and holds every layout to the same rules. A tile carries the
new-result star after its number where its case has a new result (think-wwtt), and the
regularized badge before it where it is drawn from its regularized view, the atlas's
one drawing of such a case since the House and Regularized tabs went (think-k8x9); the
fixture reads both against the records, with the key that names them.

One fixture drives the page through all of it and keeps what it read, so no test waits
on a browser in its own time. The layouts are read with the measuring tool's probe and
judged by its `layout_problems`, which `tests/test_measure_atlas_views.py` holds to the
shapes it must refuse.

Chromium is launched through `tests.site_browser`, with unhinted text for consistent
pixels across macOS and Linux. A missing browser skips locally and fails where the
frontend gate sets `SQPACK_REQUIRE_CHROMIUM`.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import Any, TypedDict

import pytest

from devtools import measure_atlas_views as atlas
from sqpack.probes import applied, probe
from tests import site_browser, site_renders

PROBES = Path(__file__).resolve().parent / "probes"
PRESSED = probe(PROBES, "site_atlas_views/pressed")
INTERRUPTED = probe(PROBES, "site_atlas_views/interrupted")
WATCH = probe(PROBES, "site_atlas_views/watch")
SEEN = probe(PROBES, "site_atlas_views/seen")
ACTIONS = probe(PROBES, "site_atlas_views/actions")
DRAWING = probe(PROBES, "site_atlas_views/drawing")
INITIAL = probe(PROBES, "site_atlas_views/initial")

GRID, TRIANGLE = atlas.tab("grid"), atlas.tab("triangle")
SMALL, MEDIUM, LARGE = (atlas.size_tab(size) for size in atlas.SIZES)
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
    "default": "triangle",
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
    "sizes, medium": "grid",
    "grid, large": "grid",
    "grid, small": "grid",
    "triangle, small": "triangle",
    "triangle, large": "triangle",
    "triangle, large, every case": "triangle",
    "triangle, medium, every case": "triangle",
    "phone, large": "triangle",
    "phone, small grid": "grid",
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
    seen["default"] = atlas.layout(page)
    page.locator(GRID).click()
    atlas.settle(page)
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
    for _ in range(4):
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
        probe(PROBES, "site_atlas_views/arranged"), arg={"per_line": 4}, timeout=5000
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
    page = atlas.open_atlas(browser, address, view="grid", reduced_motion="reduce", **DESKTOP)
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


def _sizes(browser: Any, address: str) -> Readings:
    """A desktop reader who changes the size: to Large and to Small in the grid, to the
    triangle at Small, to Large there, every case shown, by the keyboard, and back to
    Medium."""
    seen: Readings = {}
    page = atlas.open_atlas(browser, address, **DESKTOP)
    page.locator(GRID).click()
    atlas.settle(page)
    atlas.top(page)
    seen["sizes, medium"] = atlas.layout(page)
    seen["press large"] = page.evaluate(PRESSED, {"press": LARGE})
    atlas.settle(page)
    seen["grid, large"] = atlas.layout(page)
    atlas.top(page)
    seen["press small"] = page.evaluate(PRESSED, {"press": SMALL})
    atlas.settle(page)
    seen["grid, small"] = atlas.layout(page)
    page.locator(TRIANGLE).click()
    atlas.settle(page)
    seen["triangle, small"] = atlas.layout(page)
    seen["press large, triangle"] = page.evaluate(PRESSED, {"press": LARGE})
    atlas.settle(page)
    seen["triangle, large"] = atlas.layout(page)
    page.locator(atlas.EXPANDER).scroll_into_view_if_needed()
    atlas.expand(page)
    seen["triangle, large, every case"] = atlas.layout(page)

    page.locator(LARGE).focus()
    for key in ("ArrowLeft", "ArrowRight", "Home", "End", "ArrowRight"):
        page.keyboard.press(key)
        atlas.settle(page)
        seen.setdefault("size keys", []).append((key, atlas.layout(page)))
    page.locator(MEDIUM).click()
    atlas.settle(page)
    seen["triangle, medium, every case"] = atlas.layout(page)
    page.close()
    return seen


def _phone_sizes(browser: Any, address: str) -> Readings:
    """A phone opened on an address that names the triangle at Large, and then the grid
    at Small."""
    seen: Readings = {}
    page = atlas.open_atlas(
        browser, address, view="triangle", size="large", init_script=applied(WATCH), **PHONE
    )
    seen["phone, large, first placed"] = page.evaluate(SEEN)
    seen["phone, large"] = atlas.layout(page)
    page.locator(GRID).click()
    atlas.settle(page)
    page.locator(SMALL).click()
    atlas.settle(page)
    seen["phone, small grid"] = atlas.layout(page)
    page.close()
    return seen


@pytest.fixture(scope="module")
def seen(tmp_path_factory: pytest.TempPathFactory) -> Iterator[Readings]:
    """Everything the sessions read, by name."""
    sync_api = site_browser.api()
    root = Path(tmp_path_factory.mktemp("site"))
    path = site_renders.write(root, "index.html")["index.html"]
    from devtools import render_overview, site_assets  # noqa: PLC0415

    for name, data in render_overview.support_files().items():
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    static = path.read_text(encoding="utf-8")
    for script in (render_overview.ATLAS_VIEW_SCRIPT, render_overview.ATLAS_GRID_SCRIPT):
        tag = site_assets.script_tag(
            site_assets.shared().assets.script_file(script), "index.html"
        )
        static = static.replace(tag, "")
    initial = root / "initial.html"
    initial.write_text(static, encoding="utf-8")
    address = path.as_uri()
    with sync_api.sync_playwright() as driver:
        browser = site_browser.launch(driver)
        found: Readings = {}
        for session in (_desktop, _phone, _reduced, _linked, _sizes, _phone_sizes):
            found.update(session(browser, address))
        for view in atlas.VIEWS:
            for size in ("medium", "large"):
                page = browser.new_page(viewport=PHONE)
                page.goto(initial.as_uri() + atlas.query_for(view, size), wait_until="load")
                found[f"initial CSS, {view}, {size}"] = page.evaluate(INITIAL)
                page.close()
        browser.close()
        yield found


def test_a_plain_address_opens_medium_triangle_under_its_two_tabs(seen: Readings) -> None:
    """With no parameter the atlas is Medium Triangle: its tab is selected and is the
    one stop in the tab order, both tabs show, in the section tabs' type, side by side, and the
    box of tiles is the panel they control, named by the selected tab."""
    triangle = seen["default"]
    assert triangle["view"] == "triangle"
    assert (triangle["size"], triangle["search"]) == ("medium", "")
    tabs = _tabs(triangle)
    assert list(tabs) == ["grid", "triangle"]
    assert [tab["label"] for tab in tabs.values()] == ["Grid", "Triangle"]
    assert (tabs["triangle"]["selected"], tabs["triangle"]["tabindex"]) == ("true", 0)
    assert (tabs["grid"]["selected"], tabs["grid"]["tabindex"]) == ("false", -1)
    assert all(
        tab["shown"] and tab["controls"] == triangle["panel"]["id"] for tab in tabs.values()
    )
    assert triangle["panel"] == {
        "id": "atlas-cells",
        "role": "tabpanel",
        "labelledby": tabs["triangle"]["id"],
    }
    # The strip's type is the bar's and the section tabs': the note step, 17.48px.
    assert {tab["font_px"] for tab in tabs.values()} == {17.48}
    assert tabs["grid"]["box"]["top"] == tabs["triangle"]["box"]["top"]
    assert tabs["grid"]["box"]["right"] <= tabs["triangle"]["box"]["left"] + 1
    assert len(triangle["tiles"]) == 100


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


def test_the_triangle_sets_row_k_as_2k_minus_1_tiles_starting_at_the_left_edge(
    seen: Readings,
) -> None:
    """At a desktop width a line holds ten Grid-sized tiles; rows 6 to 10 wrap and
    every line starts at the block's left edge, including each short last line."""
    triangle = seen["triangle"]
    assert triangle["view"] == "triangle"
    assert triangle["per_line"] == 10
    assert _same_places(triangle, seen["default"])
    assert _drawing_width(triangle) == pytest.approx(_drawing_width(seen["grid"]), abs=0.5)
    tiles = {tile["n"]: tile for tile in triangle["tiles"]}
    assert sorted(tiles) == list(range(1, 101))
    left = triangle["cells"]["left"]
    for k in range(1, 11):
        row = [tiles[n] for n in range((k - 1) ** 2 + 1, k * k + 1)]
        tops = sorted({tile["top"] for tile in row})
        sizes = tuple(sum(tile["top"] == top for tile in row) for top in tops)
        assert sizes == atlas.row_lines(k, 10)
        for top in tops:
            line = [tile for tile in row if tile["top"] == top]
            assert abs(min(tile["left"] for tile in line) - left) <= atlas.EDGE, k
        reading = [
            tile["n"] for tile in sorted(row, key=lambda tile: (tile["top"], tile["left"]))
        ]
        assert reading == [tile["n"] for tile in row]
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
    assert after["search"] == "?atlas=grid"
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
    """From the view tabs, in the triangle, Tab goes to the size tabs' one stop, Medium,
    then to the key's link, and then to n = 1 and n = 2: the tiles keep the order of the
    cases whichever way they are set."""
    assert seen["tab order"] == ["atlas-size-medium", "regularized view", "1", "2"]


def test_the_address_names_grid_and_keeps_what_else_it_holds(seen: Readings) -> None:
    """Grid is `?atlas=grid` and the default Triangle has no parameter; a press writes it
    without a new history entry's worth of change to anything else in the address."""
    assert seen["triangle"]["search"] == ""
    assert seen["grid again"]["search"] == "?atlas=grid"
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
        "?age=180&atlas=grid",
        "#the-atlas",
    )
    back = seen["linked, back"]
    assert (back["view"], back["search"], back["hash"]) == (
        "triangle",
        "?age=180",
        "#the-atlas",
    )
    assert _same_places(back, linked)


def test_a_linked_triangle_is_the_triangle_before_a_tile_is_drawn(seen: Readings) -> None:
    """Opened on the triangle's address, the block is in the triangle, with every tile
    arranged and nothing in a move, at the moment its tiles are first put in the page:
    the grid is never shown first."""
    assert seen["phone, first placed"] == [
        {"view": "triangle", "size": "medium", "per_line": "4", "tiles": 100, "moving": 0}
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


def test_a_phone_wraps_the_long_rows_and_starts_every_line_at_the_left_edge(
    seen: Readings,
) -> None:
    """At 390 pixels a line holds four Grid-sized tiles. Rows 1 and 2 fit; row
    10, nineteen tiles, is lines of 4, 4, 4, 4 and 3 in reading order. No tile runs past the
    block or the page, and every line starts at the block's left edge, including a
    wrapped row's short last line."""
    phone = seen["phone"]
    assert phone["per_line"] == 4
    assert phone["overflow"] == 0
    cells = phone["cells"]
    tiles = {tile["n"]: tile for tile in phone["tiles"]}
    assert _drawing_width(phone) == pytest.approx(_drawing_width(seen["phone, grid"]), abs=0.5)
    for tile in tiles.values():
        assert tile["left"] >= cells["left"] - atlas.EDGE, tile["n"]
        assert tile["right"] <= cells["right"] + atlas.EDGE, tile["n"]
    for k in range(1, 11):
        row = [tiles[n] for n in range((k - 1) ** 2 + 1, k * k + 1)]
        tops = sorted({tile["top"] for tile in row})
        sizes = tuple(sum(tile["top"] == top for tile in row) for top in tops)
        assert sizes == atlas.row_lines(k, 4), k
        for top in tops:
            line = [tile for tile in row if tile["top"] == top]
            assert abs(min(tile["left"] for tile in line) - cells["left"]) <= atlas.EDGE, k
        # The cases read on in order along each line and down the lines.
        assert [tile["n"] for tile in sorted(row, key=lambda t: (t["top"], t["left"]))] == [
            tile["n"] for tile in row
        ]
    assert atlas.row_lines(10, 4) == (4, 4, 4, 4, 3)
    assert [k for k in range(1, 11) if len(atlas.row_lines(k, 4)) == 1] == [1, 2]


def test_the_space_over_a_row_is_larger_than_between_the_lines_of_one(seen: Readings) -> None:
    """Where rows wrap, a new row starts further below the line above it than a wrapped
    row's own lines stand apart, so the lines of a row read as one group."""
    tiles = {tile["n"]: tile for tile in seen["phone"]["tiles"]}
    # Row 10 at four a line: 82 to 85, 86 to 89, and three further lines.
    within = tiles[86]["top"] - tiles[82]["bottom"]
    between = tiles[82]["top"] - tiles[81]["bottom"]
    assert within == pytest.approx(tiles[90]["top"] - tiles[86]["bottom"], abs=0.5)
    assert between > within + 10, (between, within)


def test_the_expander_works_in_the_triangle(seen: Readings) -> None:
    """Showing every case keeps the hundred at their readable size and extends the
    wrapped triangle through row 18; collapsing restores the hundred. A phone keeps
    four tiles to a line even when all 324 show."""
    assert seen["press expander"]["moving"] > 0
    every = seen["triangle, every case"]
    assert (every["view"], every["expanded"], every["per_line"]) == ("triangle", "true", 10)
    assert sorted(tile["n"] for tile in every["tiles"]) == list(range(1, 325))
    collapsed = seen["triangle, collapsed"]
    assert (collapsed["expanded"], collapsed["per_line"]) == ("false", 10)
    assert _same_places(collapsed, seen["triangle"])
    phone = seen["phone, every case"]
    assert (phone["per_line"], len(phone["tiles"])) == (4, 324)
    assert len(seen["phone, grid"]["tiles"]) == 324


def test_a_narrower_window_rearranges_the_triangle_without_a_move(seen: Readings) -> None:
    """Made a phone's width, the desktop's triangle is the phone's: the same tiles to a
    line and every tile where a phone opened on the triangle has it, with no move."""
    resized = seen["resized to a phone"]
    assert resized["per_line"] == 4
    assert resized["moving"] == 0
    assert _same_places(resized, seen["phone"])


@pytest.mark.parametrize("name", LAYOUTS)
def test_no_layout_runs_past_the_page_or_sets_a_tile_over_another(
    seen: Readings, name: str
) -> None:
    """Every settled layout, in either view and at either width: nothing in a move, no
    tile outside the block or over another, the cases in order, and in the triangle
    every line at the left edge and every row cut as `row_lines` gives."""
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
    assert hovered["source"] == rest["source"]
    assert hovered["filter"] == rest["filter"] == "none"
    assert hovered["opacity"] == rest["opacity"] == "1"
    assert hovered["natural_width"] == rest["natural_width"] > 0


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


def _size_tabs(report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {tab["key"]: tab for tab in report["sizes"]}


def _width(report: dict[str, Any]) -> float:
    """The width most of a layout's tiles have."""
    widths = sorted(tile["width"] for tile in report["tiles"])
    return widths[len(widths) // 2]


def _drawing_width(report: dict[str, Any]) -> float:
    """The visible drawing width most of a layout's tiles have, after padding."""
    widths = sorted(tile["drawing"]["width"] for tile in report["tiles"])
    return widths[len(widths) // 2]


def test_the_size_tabs_stand_beside_the_view_tabs_and_open_on_medium(seen: Readings) -> None:
    """A plain address is at Medium, under a second strip on the view tabs' line, in
    their type and at their height: Small, Medium and Large, Medium selected and the
    strip's one stop in the tab order, each controlling the box of tiles. The key to a
    tile's marks stands under both strips and over the tiles."""
    medium = seen["default"]
    assert (medium["size"], medium["search"]) == ("medium", "")
    sizes = _size_tabs(medium)
    assert list(sizes) == ["small", "medium", "large"]
    assert [tab["label"] for tab in sizes.values()] == ["Small", "Medium", "Large"]
    assert (sizes["medium"]["selected"], sizes["medium"]["tabindex"]) == ("true", 0)
    for key in ("small", "large"):
        assert (sizes[key]["selected"], sizes[key]["tabindex"]) == ("false", -1), key
    assert all(tab["shown"] and tab["controls"] == "atlas-cells" for tab in sizes.values())
    views = _tabs(medium)
    assert {tab["font_px"] for tab in sizes.values()} == {views["grid"]["font_px"]}
    assert sizes["small"]["box"]["top"] == views["grid"]["box"]["top"]
    assert sizes["small"]["box"]["height"] == views["grid"]["box"]["height"]
    assert sizes["small"]["box"]["left"] > views["triangle"]["box"]["right"]
    legend = medium["legend"]
    assert legend["shown"]
    assert legend["text"] == "★ new result regularized view"
    # The note step, as the tables' legend is set, which is the tabs' step too.
    assert legend["font_px"] == 17.48
    assert legend["box"]["top"] >= views["grid"]["box"]["bottom"]
    assert legend["box"]["bottom"] <= medium["cells"]["top"]
    assert _same_places(medium, seen["triangle"])


def test_a_change_of_size_moves_the_tiles_as_a_change_of_view_does(seen: Readings) -> None:
    """A press of a size tab, in either view, starts one move a tile in the window, each
    an animation of `transform` and nothing else, timed by the same tokens, and leaves
    the view as it was."""
    for press, view, size in (
        ("press large", "grid", "large"),
        ("press small", "grid", "small"),
        ("press large, triangle", "triangle", "large"),
    ):
        started = seen[press]
        assert (started["view"], started["size"]) == (view, size), press
        assert 0 < started["moving"] <= 100, press
        assert started["properties"] == ["transform"], press
        assert started["duration"] == 360, press
        assert started["easing"] == "cubic-bezier(0.2, 0, 0, 1)", press


def test_the_grid_holds_more_and_smaller_tiles_at_small_and_fewer_and_larger_at_large(
    seen: Readings,
) -> None:
    """At 1280 pixels the grid holds fifteen tiles to a line at Small, ten at Medium and
    seven at Large, each size's tiles larger than the last; on a phone, six at Small and
    four at Medium. The address names the size, and Medium has no parameter."""
    names = ("grid, small", "sizes, medium", "grid, large")
    assert [atlas.summary(seen[name])["per_line"] for name in names] == [15, 10, 7]
    widths = [_width(seen[name]) for name in names]
    assert widths == sorted(widths)
    assert len(set(widths)) == 3
    assert [seen[name]["search"] for name in names] == [
        "?atlas=grid&size=small",
        "?atlas=grid",
        "?atlas=grid&size=large",
    ]
    assert atlas.summary(seen["phone, grid"])["per_line"] == 4
    small = seen["phone, small grid"]
    assert (small["size"], small["search"]) == ("small", "?size=small&atlas=grid")
    assert atlas.summary(small)["per_line"] == 6


def test_the_triangle_matches_grid_sizes_and_wraps_its_long_rows(seen: Readings) -> None:
    """At each size Triangle uses Grid's readable width and fits the same number of
    tiles. Expanding preserves that width; returning to Medium restores its layout."""
    small, medium, large = seen["triangle, small"], seen["triangle"], seen["triangle, large"]
    assert (small["per_line"], medium["per_line"], large["per_line"]) == (15, 10, 7)
    assert _width(small) < _width(medium) < _width(large)
    for triangle, grid in ((small, seen["grid, small"]), (large, seen["grid, large"])):
        assert _drawing_width(triangle) == pytest.approx(_drawing_width(grid), abs=0.5)
    assert atlas.summary(small)["wrapped"] == [9, 10]
    assert atlas.summary(large)["wrapped"] == [5, 6, 7, 8, 9, 10]
    assert small["search"] == "?size=small"
    assert large["search"] == "?size=large"
    every = seen["triangle, large, every case"]
    assert (every["per_line"], len(every["tiles"])) == (7, 324)
    assert _width(every) == pytest.approx(_width(large), abs=0.5)
    back = seen["triangle, medium, every case"]
    assert (back["size"], back["search"], back["per_line"]) == ("medium", "", 10)
    assert _same_places(back, seen["triangle, every case"])


def test_the_arrow_keys_move_between_the_size_tabs_and_select_the_one_focused(
    seen: Readings,
) -> None:
    """The size tabs' keys are the view tabs': Right and Left to the next and the last,
    wrapping, Home and End to the ends, and the tab the focus lands on is selected."""
    keys = [(key, report["size"]) for key, report in seen["size keys"]]
    assert keys == [
        ("ArrowLeft", "medium"),
        ("ArrowRight", "large"),
        ("Home", "small"),
        ("End", "large"),
        ("ArrowRight", "small"),
    ]
    for key, report in seen["size keys"]:
        sizes = _size_tabs(report)
        current = sizes.pop(report["size"])
        assert current["focused"], key
        assert (current["selected"], current["tabindex"]) == ("true", 0), key
        for other in sizes.values():
            assert (other["selected"], other["tabindex"], other["focused"]) == (
                "false",
                -1,
                False,
            ), key
        assert report["focus"] == current["id"]


def test_a_linked_size_is_that_size_before_a_tile_is_drawn(seen: Readings) -> None:
    """Opened on an address that names the triangle at Large, the block is at Large, its
    tiles arranged three to a line on a phone, at the moment they are first put in the
    page; the phone's layout is larger than at Medium and runs past nothing, with the size
    tabs beside the view tabs or under them."""
    assert seen["phone, large, first placed"] == [
        {"view": "triangle", "size": "large", "per_line": "3", "tiles": 100, "moving": 0}
    ]
    phone = seen["phone, large"]
    assert phone["overflow"] == 0
    assert _width(phone) > _width(seen["phone"])
    views, sizes = _tabs(phone), _size_tabs(phone)
    beside = sizes["small"]["box"]["left"] >= views["triangle"]["box"]["right"]
    under = sizes["small"]["box"]["top"] >= views["grid"]["box"]["bottom"]
    assert beside or under
    assert phone["legend"]["box"]["right"] <= phone["block"]["right"] + atlas.EDGE


@pytest.mark.parametrize(
    "name", ["triangle, large, every case", "triangle, medium, every case", "phone, large"]
)
def test_a_tile_carries_the_star_of_a_new_result_and_the_badge_of_its_regularized_view(
    seen: Readings, name: str
) -> None:
    """A case whose verified lower bound is a new result, the frontier table's rule,
    carries the star after its number, and its tile's name ends "new result"; a case
    drawn from its regularized view, the atlas's one drawing of it, carries the badge
    before its number, and its name says so; no other tile carries either. Where each
    stands is `mark_problems`', which every layout is held to above."""
    from devtools import overview_sections, render_frontier_page  # noqa: PLC0415

    new = {n for n, recent in render_frontier_page.recent_lower_bounds().items() if recent}
    regularized = set(overview_sections.atlas_regularized())
    assert new
    assert regularized
    tiles = seen[name]["tiles"]
    for tile in tiles:
        n = tile["n"]
        assert (tile["star"] is not None) == (n in new), n
        assert tile["name"].endswith(", new result") == (n in new), n
        assert (tile["mark"] is not None) == (n in regularized), n
        assert ("regularized view" in tile["name"]) == (n in regularized), n
    shown = {tile["n"] for tile in tiles}
    assert shown & new
    if len(tiles) == 324:
        assert shown & regularized == regularized


@pytest.mark.parametrize(
    ("view", "size", "columns"),
    [
        ("triangle", "medium", 4),
        ("triangle", "large", 3),
        ("grid", "medium", 4),
        ("grid", "large", 3),
    ],
)
def test_direct_mobile_queries_fit_before_atlas_programs_run(
    seen: Readings, view: str, size: str, columns: int
) -> None:
    """Responsive container geometry works without initialization or a resize event."""
    report = seen[f"initial CSS, {view}, {size}"]
    assert report is not None
    assert all(report["supported"].values())
    assert (report["view"], report["size"], report["columns"]) == (view, size, columns)
    assert report["overflow"] == 0
    assert [tile["n"] for tile in report["tiles"]] == list(range(1, 101))
    for tile in report["tiles"]:
        assert tile["left"] >= -0.5, tile["n"]
        assert tile["right"] <= report["width"] + 0.5, tile["n"]
    if view == "triangle":
        tops = {tile["top"] for tile in report["tiles"]}
        for top in tops:
            line = [tile for tile in report["tiles"] if tile["top"] == top]
            assert min(tile["left"] for tile in line) == pytest.approx(0, abs=0.5)
