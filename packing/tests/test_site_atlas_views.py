"""The homepage's atlas in its two views, the grid and the triangle, at its three sizes
of tile, and the marks its tiles carry, in a browser.

The atlas is one set of tiles under two tabs (`templates/paper-design.md`, Atlas views).
The grid is the stylesheet's alone. The triangle sets row k as the 2k - 1 cases a square
of side k holds, ending at k squared at the common right edge. Complete rows pan
without shrinking on a narrow screen: `overview/atlas-view.js` says where each tile
stands and moves the
tiles between the views. `tests/node/overview_atlas_view` holds the script's arithmetic;
what a reader
gets is the browser's to say, so this opens the rendered overview in Chromium and reads
it: where every tile stands in each view at a desktop width and on a phone, what a press
of a tab starts, what the keyboard does, what the address says, and what a reader who
asks for reduced motion sees. The size tabs beside the view tabs make every tile
smaller or larger in either view (think-ht8t): the fixture reads that a change of size
moves the tiles as a change of view does, sets the sizes in order, follows the keyboard
and the address, and holds every layout to the same rules. A tile carries the
new-result star after its number where its case has a new result (think-wwtt), and
accessible first-grid wording at the retained grid boundary in each row. Selected
derived drawings are shown directly, without layer labels or badges.

One fixture drives the page through all of it and keeps what it read, so no test waits
on a browser in its own time. The layouts are read with the measuring tool's probe and
judged by its `layout_problems`, which `tests/test_measure_atlas_views.py` holds to the
shapes it must refuse.

Chromium is launched through `tests.site_browser`, with unhinted text for consistent
pixels across macOS and Linux. A missing browser skips locally and fails where the
frontend gate sets `SQPACK_REQUIRE_CHROMIUM`.
"""

from __future__ import annotations

import json
from itertools import pairwise
from pathlib import Path
from typing import Any, TypedDict
from urllib.parse import unquote, urlsplit

import pytest

from devtools import check_site_rendering
from devtools import measure_atlas_views as atlas
from devtools.measure_atlas_views import LAYOUT
from sqpack.known_best import grid_transitions
from sqpack.probes import applied, probe
from tests import site_browser, site_renders

MANIFEST = Path(__file__).resolve().parents[1] / "atlas/known-best/manifest.json"
FIRST_GRIDS = {
    transition.row: transition.first_grid_n
    for transition in grid_transitions(json.loads(MANIFEST.read_text())["atlas"]["entries"])
}

PROBES = Path(__file__).resolve().parent / "probes"
PRESSED = probe(PROBES, "site_atlas_views/pressed")
INTERRUPTED = probe(PROBES, "site_atlas_views/interrupted")
WATCH = probe(PROBES, "site_atlas_views/watch")
SEEN = probe(PROBES, "site_atlas_views/seen")
ACTIONS = probe(PROBES, "site_atlas_views/actions")
DRAWING = probe(PROBES, "site_atlas_views/drawing")
INITIAL = probe(PROBES, "site_atlas_views/initial")
SUBSET = probe(PROBES, "site_atlas_views/subset")
REFERENCE = probe(PROBES, "site_atlas_views/reference")
CONTRIBUTIONS = probe(PROBES, "site_atlas_views/contributions")
PREPARE_SHOT = probe(PROBES, "site_atlas_views/prepare-shot")
CONTROLS = probe(PROBES, "site_atlas_views/controls")

GRID, TRIANGLE = atlas.tab("grid"), atlas.tab("triangle")
SMALL, MEDIUM, LARGE = (atlas.size_tab(size) for size in atlas.SIZES)
FIXED, ROW, GLOBAL = (f'[data-atlas-scale-tab="{scale}"]' for scale in atlas.SCALES)
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
    "medium": "triangle",
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
    "phone, small, every case": "triangle",
    "wide, small": "triangle",
    "wide, small grid": "grid",
}

type Readings = dict[str, Any]


def _places(report: dict[str, Any]) -> dict[int, tuple[float, float, float, float]]:
    """Every tile's box as it stands in the block: left and top from the block's own
    corner, so a page that has scrolled reads the same."""
    cells = report.get("canvas", report["cells"])
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


def _assert_line_edge(
    line: list[dict[str, Any]], k: int, per: int, left: float, right: float
) -> None:
    assert per >= 1
    assert {atlas.row_of(tile["n"]) for tile in line} == {k}
    assert min(tile["left"] for tile in line) >= left - atlas.EDGE
    assert max(tile["right"] for tile in line) == pytest.approx(right, abs=atlas.EDGE)


def _save_artifact(page: Any, address: str, name: str) -> None:
    root = Path(unquote(urlsplit(address).path)).parent
    assert page.evaluate(PREPARE_SHOT) == [], "every shown drawing must decode for the artifact"
    page.locator(atlas.BLOCK).screenshot(path=root / f"{name}.png", animations="disabled")
    (root / f"{name}.json").write_text(json.dumps(atlas.layout(page), indent=2))


def _desktop(browser: Any, address: str) -> Readings:
    """A desktop reader's session: to the triangle and back, a change of mind mid-move,
    the keyboard, a tile hovered and pressed, the expander, and a window made narrow."""
    seen: Readings = {}
    page = atlas.open_atlas(browser, address, init_script=applied(WATCH), **DESKTOP)
    atlas.top(page)
    seen["default"] = atlas.layout(page)
    seen["default, first placed"] = page.evaluate(SEEN)
    _save_artifact(page, address, "desktop-small-default")
    page.locator(MEDIUM).click()
    atlas.settle(page)
    seen["medium"] = atlas.layout(page)
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
    for _ in range(5):
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
        browser, address, view="triangle", size="medium", init_script=applied(WATCH), **PHONE
    )
    seen["phone, first placed"] = page.evaluate(SEEN)
    seen["phone"] = atlas.layout(page)
    seen["phone, panned start"] = page.evaluate(LAYOUT, {"pan": "start"})
    seen["phone, panned end"] = page.evaluate(LAYOUT, {"pan": "end"})
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
    page = atlas.open_atlas(
        browser, address, view="grid", size="medium", reduced_motion="reduce", **DESKTOP
    )
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
    page = atlas.open_atlas(browser, address, size="medium", **DESKTOP)
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
    page.locator(TRIANGLE).click()
    atlas.settle(page)
    atlas.expand(page)
    seen["phone, small, every case"] = atlas.layout(page)
    _save_artifact(page, address, "phone-small-all324")
    page.close()
    return seen


def _scales(browser: Any, address: str) -> Readings:
    """Scale changes, shown-set references, keyboard control and a real smaller instance."""
    found: Readings = {}
    page = atlas.open_atlas(browser, address, **DESKTOP)
    found["scale, triangle, fixed"] = atlas.layout(page)
    found["reference, triangle, fixed"] = page.evaluate(REFERENCE)
    for mode, selector in (("row", ROW), ("global", GLOBAL)):
        page.locator(selector).click()
        atlas.settle(page)
        found[f"scale, triangle, {mode}"] = atlas.layout(page)
        found[f"reference, triangle, {mode}"] = page.evaluate(REFERENCE)
        _save_artifact(page, address, f"desktop-small-scale-{mode}")
    atlas.expand(page)
    found["scale, global, expanded"] = atlas.layout(page)
    _save_artifact(page, address, "desktop-small-scale-global-all324")
    atlas.expand(page)
    found["scale, global, collapsed"] = atlas.layout(page)
    page.locator(GRID).click()
    atlas.settle(page)
    found["scale, grid, global"] = atlas.layout(page)
    found["reference, grid, global"] = page.evaluate(REFERENCE)
    page.locator(ROW).click()
    atlas.settle(page)
    found["scale, grid, row"] = atlas.layout(page)
    found["reference, grid, row"] = page.evaluate(REFERENCE)
    page.locator(FIXED).click()
    atlas.settle(page)
    found["scale, grid, fixed"] = atlas.layout(page)
    found["reference, grid, fixed"] = page.evaluate(REFERENCE)
    page.locator(FIXED).focus()
    for key in ("ArrowRight", "ArrowRight", "Home", "End", "ArrowRight", "ArrowLeft"):
        page.keyboard.press(key)
        atlas.settle(page)
        found.setdefault("scale keys", []).append((key, atlas.layout(page)))
    page.locator(MEDIUM).click()
    atlas.settle(page)
    found["scale, size changed"] = atlas.layout(page)
    page.locator(TRIANGLE).click()
    atlas.settle(page)
    found["scale, layout changed"] = atlas.layout(page)
    page.close()
    page = atlas.open_atlas(browser, address, scale="global", **PHONE)
    page.evaluate(SUBSET, {"keep": [1, 5, 11]})
    page.locator(LARGE).click()
    atlas.settle(page)
    found["scale, actual subset"] = atlas.layout(page)
    page.close()
    page = atlas.open_atlas(browser, address, scale="row", scheme="dark", **DESKTOP)
    found["reference, dark"] = page.evaluate(REFERENCE)
    _save_artifact(page, address, "desktop-small-row-reference-dark")
    page.close()
    return found


@pytest.fixture(scope="module")
def seen(tmp_path_factory: pytest.TempPathFactory) -> Readings:
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
    fallback = root / "fallback.html"
    bootstrap = render_overview.EMBED_SCRIPT.read_text(encoding="utf-8")
    rendered = path.read_text(encoding="utf-8")
    assert bootstrap in rendered
    fallback.write_text(rendered.replace(bootstrap, ""), encoding="utf-8")
    address = path.as_uri()
    with sync_api.sync_playwright() as driver:
        browser = site_browser.launch(driver)
        found: Readings = {}
        for session in (_desktop, _phone, _reduced, _linked, _sizes, _phone_sizes, _scales):
            found.update(session(browser, address))
        page = atlas.open_atlas(browser, address, size="small", width=3200, height=1200)
        found["wide, small"] = atlas.layout(page)
        from devtools import result_overview  # noqa: PLC0415

        facts = result_overview.film_facts()
        for n in (1, 11, 17, 211):
            fragment = (
                result_overview.film_bound(facts[n])
                + result_overview.gap_bar(facts[n])
                + result_overview.film_facts_html(facts[n])
                + result_overview.case_badges(n)
            )
            found[f"contributions, {n}"] = page.evaluate(CONTRIBUTIONS, {"html": fragment})
        _save_artifact(page, address, "wide-small-mounted")
        page.locator(GRID).click()
        atlas.settle(page)
        found["wide, small grid"] = atlas.layout(page)
        page.close()
        page = browser.new_page(viewport={"width": 3200, "height": 1200})
        page.goto(initial.as_uri() + atlas.query_for("triangle", "small"), wait_until="load")
        found["initial CSS, wide"] = page.evaluate(INITIAL)
        page.locator(atlas.BLOCK).screenshot(
            path=root / "wide-small-initial.png", animations="disabled"
        )
        (root / "wide-small-initial.json").write_text(
            json.dumps(found["initial CSS, wide"], indent=2)
        )
        page.close()
        for view in atlas.VIEWS:
            for size in atlas.SIZES:
                page = browser.new_page(viewport=PHONE)
                page.goto(initial.as_uri() + atlas.query_for(view, size), wait_until="load")
                found[f"initial CSS, {view}, {size}"] = page.evaluate(INITIAL)
                if size == "small":
                    found[f"initial reference, {view}, fixed"] = page.evaluate(REFERENCE)
                page.close()
        for size in atlas.SIZES:
            page = atlas.open_atlas(browser, fallback.as_uri(), size=size, **PHONE)
            found[f"without bootstrap, {size}"] = atlas.layout(page)
            page.close()
        for view, scale in (
            ("triangle", "row"),
            ("triangle", "global"),
            ("grid", "row"),
            ("grid", "global"),
        ):
            page = browser.new_page(viewport=PHONE)
            page.goto(
                initial.as_uri() + atlas.query_for(view, "small", scale), wait_until="load"
            )
            found[f"initial scale, {view}, {scale}"] = page.evaluate(INITIAL)
            found[f"initial reference, {view}, {scale}"] = page.evaluate(REFERENCE)
            page.close()
            page = atlas.open_atlas(browser, address, view=view, scale=scale, **PHONE)
            found[f"mounted scale, {view}, {scale}"] = atlas.layout(page)
            found[f"mounted reference, {view}, {scale}"] = page.evaluate(REFERENCE)
            if view == "triangle":
                _save_artifact(page, address, f"phone-small-scale-{scale}")
            page.close()
        for scale in ("row", "global", "invalid"):
            page = atlas.open_atlas(
                browser, fallback.as_uri(), query=f"?scale={scale}", **PHONE
            )
            found[f"scale without bootstrap, {scale}"] = atlas.layout(page)
            found[f"reference without bootstrap, {scale}"] = page.evaluate(REFERENCE)
            page.close()
        context = browser.new_context(java_script_enabled=False, viewport=PHONE)
        page = context.new_page()
        page.goto(address, wait_until="load")
        found["no JavaScript"] = page.evaluate(INITIAL)
        found["reference, no JavaScript"] = page.evaluate(REFERENCE)
        page.locator(atlas.BLOCK).screenshot(path=root / "phone-small-no-javascript.png")
        (root / "phone-small-no-javascript.json").write_text(
            json.dumps(found["no JavaScript"], indent=2)
        )
        context.close()
        browser.close()
        (root / "all-readings.json").write_text(json.dumps(found, indent=2))
    return found


@pytest.fixture(scope="module")
def control_readings(tmp_path_factory: pytest.TempPathFactory) -> Readings:
    """Read the actual homepage across chooser wrap points, with and without scripts."""
    root = Path(tmp_path_factory.mktemp("atlas-controls"))
    address = site_renders.write(root, "index.html")["index.html"].as_uri()
    found: Readings = {}
    with site_browser.api().sync_playwright() as driver:
        browser = site_browser.launch(driver)
        for javascript in (False, True):
            context = browser.new_context(java_script_enabled=javascript)
            page = context.new_page()
            page.goto(address, wait_until="load")
            check_site_rendering.wait_for_fonts(page)
            for width in (320, 390, 640, 820, 1280, 3200):
                page.set_viewport_size({"width": width, "height": 900})
                name = f"{width}px, scripts {javascript}"
                found[name] = page.evaluate(CONTROLS)
                if javascript and width in (390, 1280):
                    page.locator("[data-atlas-controls]").screenshot(
                        path=root / f"controls-{width}.png", animations="disabled"
                    )
            context.close()
        browser.close()
    (root / "controls.json").write_text(json.dumps(found, indent=2), encoding="utf-8")
    return found


def test_choosers_and_the_color_legend_share_the_content_center(
    control_readings: Readings,
) -> None:
    for name, reading in control_readings.items():
        content = reading["controls"]
        center = (content["left"] + content["right"]) / 2
        lines: dict[float, list[dict[str, float]]] = {}
        assert len(reading["choosers"]) == 3, name
        for chooser in reading["choosers"]:
            lines.setdefault(round(chooser["top"], 1), []).append(chooser)
        for line in lines.values():
            left = min(box["left"] for box in line)
            right = max(box["right"] for box in line)
            assert (left + right) / 2 == pytest.approx(center, abs=1), name
            assert left >= content["left"] - 1, name
            assert right <= content["right"] + 1, name
        columns = reading["columns"]
        assert len(columns) == 2, name
        assert [len(column["items"]) for column in columns] == [1, 1], name
        items = [item for column in columns for item in column["items"]]
        left = min(item["box"]["left"] for item in items)
        right = max(item["box"]["right"] for item in items)
        assert (left + right) / 2 == pytest.approx(center, abs=1), name
        assert left >= content["left"] - 1, name
        assert right <= content["right"] + 1, name
        for column in columns:
            for item in column["items"]:
                assert item["box"]["left"] == pytest.approx(column["box"]["left"], abs=1), name
                assert item["textAlign"] in ("start", "left"), name


def test_a_plain_address_opens_small_triangle_under_its_two_tabs(seen: Readings) -> None:
    """With no parameter the atlas is Small Triangle: its tab is selected and is the
    one stop in the tab order, both tabs show, in the section tabs' type, side by side, and the
    box of tiles is the panel they control, named by the selected tab."""
    triangle = seen["default"]
    assert triangle["view"] == "triangle"
    assert (triangle["size"], triangle["search"]) == ("small", "")
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


def test_the_triangle_sets_complete_rows_at_a_common_right_edge(
    seen: Readings,
) -> None:
    """Viewport capacity controls drawing scale; complete logical rows align right."""
    triangle = seen["triangle"]
    assert triangle["view"] == "triangle"
    assert triangle["per_line"] == 10
    assert _same_places(triangle, seen["medium"])
    assert _drawing_width(triangle) == pytest.approx(_drawing_width(seen["grid"]), abs=0.5)
    tiles = {tile["n"]: tile for tile in triangle["tiles"]}
    assert sorted(tiles) == list(range(1, 101))
    left = triangle["canvas"]["left"]
    for k in range(1, 11):
        row = [tiles[n] for n in range((k - 1) ** 2 + 1, k * k + 1)]
        tops = sorted({tile["top"] for tile in row})
        sizes = tuple(sum(tile["top"] == top for tile in row) for top in tops)
        assert sizes == atlas.row_lines(k, 10, FIRST_GRIDS[k])
        for top in tops:
            line = [tile for tile in row if tile["top"] == top]
            _assert_line_edge(line, k, 10, left, triangle["canvas"]["right"])
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
    # The shared legend changes how many drawings fit in the viewport. The probe
    # checks every visible drawing, and its jump bound must not be vacuous.
    assert second["watched"] > 0
    assert second["jump"] < 1.5, second
    after = seen["grid after a second press"]
    assert after["view"] == "grid"
    assert after["moving"] == 0
    assert _same_places(after, seen["grid"])
    assert after["search"] == "?size=medium&atlas=grid"
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
    then to n = 1, n = 2 and n = 3: the tiles keep the order of the
    cases whichever way they are set."""
    assert seen["tab order"] == ["atlas-size-medium", "atlas-scale-fixed", "1", "2", "3"]


def test_the_address_names_grid_and_keeps_what_else_it_holds(seen: Readings) -> None:
    """Grid is `?atlas=grid` and the default Triangle has no parameter; a press writes it
    without a new history entry's worth of change to anything else in the address."""
    assert seen["triangle"]["search"] == "?size=medium"
    assert seen["grid again"]["search"] == "?size=medium&atlas=grid"
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
    assert seen["default, first placed"] == [
        {
            "view": "triangle",
            "size": "small",
            "scale": "fixed",
            "per_line": "15",
            "tiles": 100,
            "moving": 0,
        }
    ]
    assert seen["phone, first placed"] == [
        {
            "view": "triangle",
            "size": "medium",
            "scale": "fixed",
            "per_line": "4",
            "tiles": 100,
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


def test_a_phone_pans_complete_readable_rows_at_the_right_edge(
    seen: Readings,
) -> None:
    """The phone retains Grid-sized drawings on complete rows in a local pan frame."""
    phone = seen["phone"]
    assert phone["per_line"] == 4
    assert phone["overflow"] == 0
    cells = phone["canvas"]
    tiles = {tile["n"]: tile for tile in phone["tiles"]}
    assert _drawing_width(phone) == pytest.approx(_drawing_width(seen["phone, grid"]), abs=0.5)
    for tile in tiles.values():
        assert tile["left"] >= cells["left"] - atlas.EDGE, tile["n"]
        assert tile["right"] <= cells["right"] + atlas.EDGE, tile["n"]
    for k in range(1, 11):
        row = [tiles[n] for n in range((k - 1) ** 2 + 1, k * k + 1)]
        tops = sorted({tile["top"] for tile in row})
        sizes = tuple(sum(tile["top"] == top for tile in row) for top in tops)
        assert sizes == atlas.row_lines(k, 4, FIRST_GRIDS[k]), k
        for top in tops:
            line = [tile for tile in row if tile["top"] == top]
            _assert_line_edge(line, k, 4, cells["left"], cells["right"])
        # The cases read on in order along each line and down the lines.
        assert [tile["n"] for tile in sorted(row, key=lambda t: (t["top"], t["left"]))] == [
            tile["n"] for tile in row
        ]
    assert atlas.row_lines(10, 4, FIRST_GRIDS[10]) == (19,)
    start, end = seen["phone, panned start"], seen["phone, panned end"]
    assert start["pan"]["left"] < end["pan"]["left"] == 0
    assert start["canvas"]["left"] == pytest.approx(start["cells"]["left"], abs=atlas.EDGE)
    assert end["canvas"]["right"] == pytest.approx(end["cells"]["right"], abs=atlas.EDGE)
    assert start["pan"]["width"] > start["pan"]["viewport"]
    assert atlas.layout_problems(start) == atlas.layout_problems(end) == []


def _assert_uniform_lines(
    tiles: list[dict[str, Any]], gap: float, top: float, bottom: float
) -> None:
    """Every occupied line reserves the same height and gap, with no blank row space."""
    tops = sorted({tile["top"] for tile in tiles})
    height = tiles[0]["height"]
    assert tops[0] == pytest.approx(top, abs=atlas.EDGE)
    for tile in tiles:
        assert tile["height"] == pytest.approx(height, abs=atlas.EDGE)
    for earlier, later in pairwise(tops):
        assert later - earlier == pytest.approx(height + gap, abs=atlas.EDGE)
    assert bottom - top == pytest.approx(
        len(tops) * height + (len(tops) - 1) * gap, abs=atlas.EDGE
    )


def _assert_frame_extent(report: dict[str, Any]) -> None:
    """Rows fill the actual client area; clientHeight excludes a real scrollbar."""
    canvas, frame = report["canvas"], report["frame"]
    assert canvas["top"] == pytest.approx(frame["top"], abs=atlas.EDGE)
    assert canvas["bottom"] == pytest.approx(frame["bottom"], abs=atlas.EDGE)


def test_frame_extent_rejects_blank_space_even_with_valid_row_pitch() -> None:
    tiles = [{"top": 0, "height": 50}, {"top": 60, "height": 50}]
    _assert_uniform_lines(tiles, 10, 0, 110)
    right = {"canvas": {"top": 0, "bottom": 110}, "frame": {"top": 0, "bottom": 110}}
    _assert_frame_extent(right)
    # Top padding leaves every row and its pitch valid but adds blank frame space.
    with pytest.raises(AssertionError):
        _assert_frame_extent({**right, "frame": {"top": -12, "bottom": 110}})
    # A stale min-height likewise extends the actual frame below the last row.
    with pytest.raises(AssertionError):
        _assert_frame_extent({**right, "frame": {"top": 0, "bottom": 122}})


@pytest.mark.parametrize("name", [name for name, view in LAYOUTS.items() if view == "triangle"])
def test_every_triangle_line_has_uniform_height_and_vertical_pitch(
    seen: Readings, name: str
) -> None:
    """Every complete logical row reserves identical height and vertical spacing."""
    report = seen[name]
    assert report["line_gap_px"] == pytest.approx(report["gap_px"], abs=atlas.EDGE)
    for tile in report["tiles"]:
        drawing = tile["drawing"]
        padding = (tile["width"] - drawing["width"]) / 2
        assert drawing["top"] - tile["top"] == pytest.approx(padding, abs=atlas.EDGE)
        assert tile["height"] == pytest.approx(
            drawing["height"]
            + 2 * padding
            + tile["number_box"]["height"]
            + tile["width"] * 0.04,
            abs=atlas.EDGE,
        )
    _assert_uniform_lines(
        report["tiles"],
        report["line_gap_px"],
        report["canvas"]["top"],
        report["canvas"]["bottom"],
    )
    _assert_frame_extent(report)


def test_the_expander_works_in_the_triangle(seen: Readings) -> None:
    """Showing every case keeps the hundred at their readable size and extends the
    complete triangle through row 18; collapsing restores the hundred. A phone keeps
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
    every logical row complete and aligned to the canvas right edge."""
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


def test_the_size_tabs_stand_beside_the_view_tabs_and_open_on_small(seen: Readings) -> None:
    """A plain address is at Small, under a second strip on the view tabs' line, in
    their type and at their height: Small, Medium and Large, Small selected and the
    strip's one stop in the tab order, each controlling the box of tiles. The key to a
    tile's marks stands under both strips and over the tiles."""
    small = seen["default"]
    assert (small["size"], small["search"]) == ("small", "")
    sizes = _size_tabs(small)
    assert list(sizes) == ["small", "medium", "large"]
    assert [tab["label"] for tab in sizes.values()] == ["Small", "Medium", "Large"]
    assert (sizes["small"]["selected"], sizes["small"]["tabindex"]) == ("true", 0)
    for key in ("medium", "large"):
        assert (sizes[key]["selected"], sizes[key]["tabindex"]) == ("false", -1), key
    assert all(tab["shown"] and tab["controls"] == "atlas-cells" for tab in sizes.values())
    views = _tabs(small)
    assert {tab["font_px"] for tab in sizes.values()} == {views["grid"]["font_px"]}
    assert sizes["small"]["box"]["top"] == views["grid"]["box"]["top"]
    assert sizes["small"]["box"]["height"] == views["grid"]["box"]["height"]
    assert sizes["small"]["box"]["left"] > views["triangle"]["box"]["right"]
    legend = small["legend"]
    assert legend["shown"]
    assert "proved optimal (" in legend["text"]
    assert "recent result, since August, 2026" in legend["text"]
    assert "colors indicate distinct tilt angles" in legend["text"]
    assert "shade indicates number of full-side contacts" in legend["text"]
    assert "half a drawing" not in legend["text"]
    left, right = legend["columns"]
    assert all(item["text"].endswith("/324)") for item in [*left["items"], right["items"][0]])
    assert [item["key"] for item in left["items"]] == ["optimal", "exact", "numerical", "rigid"]
    assert [item["key"] for item in right["items"]] == [
        "recent",
        "angles",
        "contacts",
        "degree",
    ]
    assert right["items"][3]["text"] == "deg is the algebraic degree of that side length"
    assert right["items"][3]["swatches"] == []
    for column in (left, right):
        for item in column["items"]:
            assert item["box"]["left"] == pytest.approx(column["box"]["left"], abs=atlas.EDGE)
    for item, values in zip(
        right["items"][1:3], (["0", "1", "2", "3"], ["4", "3", "2", "1", "0"]), strict=True
    ):
        assert [swatch["value"] for swatch in item["swatches"]] == values
        assert len({swatch["fill"] for swatch in item["swatches"]}) == len(values)
        assert all(swatch["width"] > 0 and swatch["height"] > 0 for swatch in item["swatches"])
    assert [swatch["label"] for swatch in right["items"][1]["swatches"]] == [
        "90\N{DEGREE SIGN}",
        "45\N{DEGREE SIGN}",
        "",
        "",
    ]
    assert [swatch["ink"] for swatch in right["items"][1]["swatches"][:2]] == [
        "rgb(0, 0, 0)"
    ] * 2
    assert [swatch["label"] for swatch in right["items"][2]["swatches"]] == [
        "4",
        "3",
        "2",
        "1",
        "0",
    ]
    # The note step, as the tables' legend is set, which is the tabs' step too.
    assert legend["font_px"] == 17.48
    assert legend["box"]["top"] >= views["grid"]["box"]["bottom"]
    assert legend["box"]["bottom"] <= small["cells"]["top"]
    assert small["view_strip"]["left"] == pytest.approx(small["cells"]["left"], abs=atlas.EDGE)
    assert legend["box"]["left"] == pytest.approx(small["cells"]["left"], abs=atlas.EDGE)
    assert _same_places(small, seen["triangle, small"])


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
    four at Medium. The address names Medium and Large; Small has no parameter."""
    names = ("grid, small", "sizes, medium", "grid, large")
    assert [atlas.summary(seen[name])["per_line"] for name in names] == [15, 10, 7]
    widths = [_width(seen[name]) for name in names]
    assert widths == sorted(widths)
    assert len(set(widths)) == 3
    assert [seen[name]["search"] for name in names] == [
        "?atlas=grid",
        "?size=medium&atlas=grid",
        "?size=large&atlas=grid",
    ]
    assert atlas.summary(seen["phone, grid"])["per_line"] == 4
    small = seen["phone, small grid"]
    assert (small["size"], small["search"]) == ("small", "?atlas=grid")
    assert atlas.summary(small)["per_line"] == 6


def test_the_triangle_matches_grid_sizes_and_keeps_complete_rows(seen: Readings) -> None:
    """At each size Triangle uses Grid's readable width and fits the same number of
    tiles. Expanding preserves that width; returning to Medium restores its layout."""
    small, medium, large = seen["triangle, small"], seen["triangle"], seen["triangle, large"]
    assert (small["per_line"], medium["per_line"], large["per_line"]) == (15, 10, 7)
    assert _width(small) < _width(medium) < _width(large)
    for triangle, grid in ((small, seen["grid, small"]), (large, seen["grid, large"])):
        assert _drawing_width(triangle) == pytest.approx(_drawing_width(grid), abs=0.5)
    assert atlas.summary(small)["wrapped"] == []
    assert atlas.summary(large)["wrapped"] == []
    assert small["search"] == ""
    assert large["search"] == "?size=large"
    every = seen["triangle, large, every case"]
    assert (every["per_line"], len(every["tiles"])) == (7, 324)
    assert _width(every) == pytest.approx(_width(large), abs=0.5)
    back = seen["triangle, medium, every case"]
    assert (back["size"], back["search"], back["per_line"]) == ("medium", "?size=medium", 10)
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
        {
            "view": "triangle",
            "size": "large",
            "scale": "fixed",
            "per_line": "3",
            "tiles": 100,
            "moving": 0,
        }
    ]
    phone = seen["phone, large"]
    assert phone["overflow"] == 0
    assert _width(phone) > _width(seen["phone"])
    views, sizes = _tabs(phone), _size_tabs(phone)
    beside = sizes["small"]["box"]["left"] >= views["triangle"]["box"]["right"]
    under = sizes["small"]["box"]["top"] >= views["grid"]["box"]["bottom"]
    assert beside or under
    assert phone["legend"]["box"]["right"] <= phone["block"]["right"] + atlas.EDGE
    right = phone["legend"]["columns"][1]
    degree = right["items"][3]
    assert degree["text"] == "deg is the algebraic degree of that side length"
    assert degree["box"]["right"] <= right["box"]["right"] + atlas.EDGE
    assert degree["box"]["bottom"] <= phone["cells"]["top"] + atlas.EDGE


@pytest.mark.parametrize(
    "name",
    [
        "triangle, large, every case",
        "triangle, medium, every case",
        "phone, large",
        "phone, small, every case",
    ],
)
def test_tiles_keep_new_result_stars_without_layer_indicators(
    seen: Readings, name: str
) -> None:
    """Selected drawings are shown directly; the only result indicator is the star."""
    from devtools import render_frontier_page  # noqa: PLC0415

    new = {n for n, recent in render_frontier_page.recent_lower_bounds().items() if recent}
    assert new
    tiles = seen[name]["tiles"]
    for tile in tiles:
        n = tile["n"]
        assert (tile["star"] is not None) == (n in new), n
        assert tile["name"].endswith(", new result") == (n in new), n
        assert tile["mark"] is None, n
        assert "regularized" not in tile["name"], n
        assert tile["grid_from"] == (n == FIRST_GRIDS[atlas.row_of(n)]), n
        assert not tile["grid_marker"], n
        assert tile["grid_label"] is None, n
    assert {tile["n"] for tile in tiles} & new


@pytest.mark.parametrize(
    ("view", "size", "columns"),
    [
        ("triangle", "small", 6),
        ("triangle", "medium", 4),
        ("triangle", "large", 3),
        ("grid", "small", 6),
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
    assert report["page_overflow"] == 0
    assert (report["overflow"] > 0) == (view == "triangle")
    assert [tile["n"] for tile in report["tiles"]] == list(range(1, 101))
    for tile in report["tiles"]:
        assert tile["left"] >= report["canvas"]["left"] - 0.5, tile["n"]
        assert tile["right"] <= report["canvas"]["right"] + 0.5, tile["n"]
    if view == "triangle":
        tops = {tile["top"] for tile in report["tiles"]}
        for top in tops:
            line = [tile for tile in report["tiles"] if tile["top"] == top]
            _assert_line_edge(
                line,
                atlas.row_of(line[0]["n"]),
                columns,
                report["canvas"]["left"],
                report["canvas"]["right"],
            )


@pytest.mark.parametrize(
    "name",
    [
        "triangle",
        "phone",
        "triangle, small",
        "triangle, large, every case",
        "phone, small, every case",
    ],
)
def test_extra_gaps_follow_the_retained_suffix_without_web_captions(
    seen: Readings, name: str
) -> None:
    """Inline segments keep the horizontal half-drawing gap; split lines use ordinary pitch."""
    report = seen[name]
    found = {tile["n"]: tile for tile in report["tiles"]}
    crossing = 0
    for n in FIRST_GRIDS.values():
        if n not in found:
            continue
        tile = found[n]
        assert not tile["grid_marker"]
        assert tile["grid_label"] is None
        assert tile["grid_marker_lines"] == []
        assert "first grid packing" in tile["name"]
        previous = found.get(n - 1)
        if (
            previous
            and atlas.row_of(n - 1) == atlas.row_of(n)
            and previous["top"] == tile["top"]
        ):
            crossing += 1
            gap = tile["left"] - previous["right"]
            assert gap == pytest.approx(
                report["gap_px"] + tile["drawing"]["width"] / 2, abs=atlas.EDGE
            )
        else:
            k = atlas.row_of(n)
            line = [
                t
                for t in report["tiles"]
                if atlas.row_of(t["n"]) == k and abs(t["top"] - tile["top"]) <= atlas.EDGE
            ]
            _assert_line_edge(
                line, k, report["per_line"], report["canvas"]["left"], report["canvas"]["right"]
            )
            if previous and atlas.row_of(previous["n"]) == k:
                assert tile["top"] - previous["bottom"] == pytest.approx(
                    report["gap_px"], abs=atlas.EDGE
                )
    if report["per_line"] >= 6:
        assert crossing > 0
    for tile in seen["grid"]["tiles"]:
        assert not tile["grid_marker"]


@pytest.mark.parametrize(("size", "columns"), [("small", 6), ("medium", 4), ("large", 3)])
def test_first_grid_spacing_is_present_without_captions_before_atlas_scripts(
    seen: Readings, size: str, columns: int
) -> None:
    report = seen[f"initial CSS, triangle, {size}"]
    tiles = {tile["n"]: tile for tile in report["tiles"]}
    _assert_uniform_lines(
        report["tiles"],
        report["line_gap_px"],
        report["canvas"]["top"],
        report["canvas"]["bottom"],
    )
    _assert_frame_extent(report)
    for k in range(1, 11):
        row = [tiles[n] for n in range((k - 1) ** 2 + 1, k * k + 1)]
        tops = sorted({tile["top"] for tile in row})
        assert tuple(
            sum(tile["top"] == top for tile in row) for top in tops
        ) == atlas.row_lines(k, columns, FIRST_GRIDS[k])
        first = tiles[FIRST_GRIDS[k]]
        assert not first["grid_marker"]
        assert first["grid_label"] is None
        assert first["grid_marker_lines"] == []
        previous = tiles.get(first["n"] - 1)
        if previous and atlas.row_of(previous["n"]) == k and previous["top"] == first["top"]:
            assert first["left"] - previous["right"] == pytest.approx(
                report["gap_px"] + first["drawing_width"] / 2, abs=atlas.EDGE
            )
        else:
            line = [tile for tile in row if tile["top"] == first["top"]]
            _assert_line_edge(
                line, k, columns, report["canvas"]["left"], report["canvas"]["right"]
            )
            if previous and atlas.row_of(previous["n"]) == k:
                assert first["top"] - previous["bottom"] == pytest.approx(
                    report["gap_px"], abs=atlas.EDGE
                )
    assert all(not tile["grid_marker"] for tile in seen[f"initial CSS, grid, {size}"]["tiles"])


def test_small_triangle_survives_disabled_javascript_and_mounting_without_bootstrap(
    seen: Readings,
) -> None:
    static = seen["no JavaScript"]
    assert (static["view"], static["size"], static["columns"]) == ("triangle", "small", 6)
    assert static["page_overflow"] == 0
    assert all(not tile["grid_marker"] for tile in static["tiles"])
    _assert_uniform_lines(
        static["tiles"],
        static["line_gap_px"],
        static["canvas"]["top"],
        static["canvas"]["bottom"],
    )
    _assert_frame_extent(static)
    for size, columns in (("small", 6), ("medium", 4), ("large", 3)):
        mounted = seen[f"without bootstrap, {size}"]
        assert (mounted["view"], mounted["size"], mounted["per_line"]) == (
            "triangle",
            size,
            columns,
        )
        assert _size_tabs(mounted)[size]["selected"] == "true"
        assert atlas.layout_problems(mounted) == []


def test_wide_triangle_uses_grid_capacity_without_a_row_length_cap(seen: Readings) -> None:
    report = seen["wide, small"]
    assert report["per_line"] > 19
    assert _drawing_width(report) == pytest.approx(
        _drawing_width(seen["wide, small grid"]), abs=0.5
    )
    assert atlas.summary(report)["lines"] == 10
    assert atlas.summary(report)["wrapped"] == []
    initial = seen["initial CSS, wide"]
    _assert_uniform_lines(
        initial["tiles"],
        initial["line_gap_px"],
        initial["canvas"]["top"],
        initial["canvas"]["bottom"],
    )
    _assert_frame_extent(initial)
    assert initial["columns"] == report["per_line"]
    assert len({tile["top"] for tile in initial["tiles"]}) == 10
    assert initial["overflow"] == 0


def test_contribution_accents_paint_independently_and_rigidity_stays_dark(
    seen: Readings,
) -> None:
    seventeen = seen["contributions, 17"]
    assert seventeen["lower_gap_label"] == "4.66"
    assert seventeen["lower_bound_label"] == "4.66044"
    eleven = seen["contributions, 11"]
    assert eleven["upper"] == eleven["colors"]["upper"]
    assert eleven["lower_citation"] == eleven["colors"]["recent"]
    assert eleven["equality_upper"] == eleven["colors"]["neutral"]
    for badge in eleven["badges"]:
        if badge["glyph"] == "O":
            assert badge["background"] == eleven["colors"]["recent"]
        if badge["glyph"] == "R":
            assert badge["style"] == "solid"
            assert badge["background"] == eleven["colors"]["dark"]
    updated_upper = seen["contributions, 211"]
    assert updated_upper["upper"] == updated_upper["colors"]["recent"]
    old_optimal = seen["contributions, 1"]
    assert old_optimal["equality_upper"] == old_optimal["colors"]["neutral"]
    assert all(
        badge["background"] == old_optimal["colors"]["dark"]
        for badge in old_optimal["badges"]
        if badge["glyph"] in ("O", "R")
    )


@pytest.mark.parametrize("view", ["triangle", "grid"])
@pytest.mark.parametrize("scale", ["row", "global"])
def test_scale_changes_real_drawings_without_moving_slots_or_resizing_numbers(
    seen: Readings,
    view: str,
    scale: str,
) -> None:
    fixed = seen[f"scale, {view}, fixed"]
    report = seen[f"scale, {view}, {scale}"]
    assert report["scale"] == scale
    assert _same_places(fixed, report)
    original = {tile["n"]: tile for tile in fixed["tiles"]}
    for tile in report["tiles"]:
        baseline = original[tile["n"]]
        reference = (
            atlas.row_of(tile["n"])
            if scale == "row"
            else max(t["side"] for t in report["tiles"])
        )
        assert tile["drawing"]["width"] == pytest.approx(
            baseline["drawing"]["width"] * tile["side"] / reference, abs=0.02
        )
        assert tile["drawing_slot_width"] == baseline["drawing_slot_width"]
        assert tile["number_px"] == baseline["number_px"]
        assert tile["number_box"]["height"] == baseline["number_box"]["height"]
        assert tile["number_box"]["top"] - tile["top"] == pytest.approx(
            baseline["number_box"]["top"] - baseline["top"], abs=0.02
        )
    assert atlas.layout_problems(report) == []
    assert atlas.mark_problems(report) == []
    row_tiles = {tile["n"]: tile for tile in report["tiles"]}
    assert row_tiles[5]["side"] == pytest.approx(2 + 2**-0.5)
    if scale == "row":
        assert row_tiles[25]["drawing"]["width"] == row_tiles[36]["drawing"]["width"]
        assert row_tiles[5]["drawing"]["width"] < row_tiles[9]["drawing"]["width"]
    else:
        assert row_tiles[25]["drawing"]["width"] / row_tiles[36]["drawing"][
            "width"
        ] == pytest.approx(5 / 6, abs=0.002)


def test_global_reference_follows_expansion_collapse_and_an_actual_case_subset(
    seen: Readings,
) -> None:
    expanded, collapsed = seen["scale, global, expanded"], seen["scale, global, collapsed"]
    assert (len(expanded["tiles"]), expanded["largest_side"]) == (324, 18)
    assert (len(collapsed["tiles"]), collapsed["largest_side"]) == (100, 10)
    for report in (expanded, collapsed, seen["scale, actual subset"]):
        largest = max(tile["side"] for tile in report["tiles"])
        assert report["largest_side"] == largest
        for tile in report["tiles"]:
            assert tile["drawing"]["width"] == pytest.approx(
                tile["drawing_slot_width"] * tile["side"] / largest, abs=0.02
            )
    subset = seen["scale, actual subset"]
    assert [tile["n"] for tile in subset["tiles"]] == [1, 5, 11]
    assert subset["largest_side"] == pytest.approx(3.877083590022814)
    assert _same_places(collapsed, seen["scale, triangle, fixed"])
    assert atlas.layout_problems(expanded) == []


def test_scale_tabs_have_one_tab_stop_descriptions_and_keyboard_url_state(
    seen: Readings,
) -> None:
    report = seen["default"]
    tabs = {tab["key"]: tab for tab in report["scales"]}
    assert list(tabs) == ["fixed", "row", "global"]
    assert report["scale"] == "fixed"
    assert [(tab["selected"], tab["tabindex"]) for tab in tabs.values()] == [
        ("true", 0),
        ("false", -1),
        ("false", -1),
    ]
    assert all(tab["description"] and tab["controls"] == "atlas-cells" for tab in tabs.values())
    expected = ["row", "global", "fixed", "global", "fixed", "global"]
    for (_, reading), mode in zip(seen["scale keys"], expected, strict=True):
        selected = next(tab for tab in reading["scales"] if tab["selected"] == "true")
        assert selected["key"] == mode
        assert selected["focused"]
        assert selected["tabindex"] == 0
        assert reading["scale"] == mode
        assert reading["search"] == f"?atlas=grid{'' if mode == 'fixed' else f'&scale={mode}'}"
    assert seen["scale, size changed"]["search"] == "?atlas=grid&scale=global&size=medium"
    assert seen["scale, layout changed"]["search"] == "?scale=global&size=medium"


@pytest.mark.parametrize("view", ["triangle", "grid"])
@pytest.mark.parametrize("scale", ["row", "global"])
def test_scale_query_has_correct_actual_ratios_before_mount_without_layout_shift(
    seen: Readings,
    view: str,
    scale: str,
) -> None:
    initial = seen[f"initial scale, {view}, {scale}"]
    mounted = seen[f"mounted scale, {view}, {scale}"]
    assert initial["scale"] == mounted["scale"] == scale
    assert initial["height"] == pytest.approx(mounted["cells"]["height"], abs=0.02)
    assert initial["width"] == mounted["cells"]["width"]
    for before, after in zip(initial["tiles"], mounted["tiles"], strict=True):
        assert before["n"] == after["n"]
        reference = (
            atlas.row_of(before["n"])
            if scale == "row"
            else max(tile["side"] for tile in initial["tiles"])
        )
        assert before["drawing_width"] == pytest.approx(
            before["drawing_slot_width"] * before["side"] / reference, abs=0.02
        )
        assert before["drawing_width"] == pytest.approx(after["drawing"]["width"], abs=0.02)
        assert before["width"] == pytest.approx(after["width"], abs=0.02)
        assert before["height"] == after["height"]


@pytest.mark.parametrize("scale", ["row", "global", "invalid"])
def test_scale_defaults_survive_missing_bootstrap_and_disabled_javascript(
    seen: Readings, scale: str
) -> None:
    assert seen["scale without bootstrap, " + scale]["scale"] == (
        scale if scale != "invalid" else "fixed"
    )
    assert seen["no JavaScript"]["scale"] == "fixed"


def _reference_frame() -> tuple[float, float]:
    """Independent expected bounds from the actual normalized enclosing SVG frame."""
    from xml.etree import ElementTree as ET  # noqa: PLC0415

    from devtools.render_frontier_page import packing_svg  # noqa: PLC0415

    svg = ET.fromstring(packing_svg(5, units=1000))
    left, _, extent, _ = map(float, svg.attrib["viewBox"].split())
    frame = svg.find("rect")
    assert frame is not None
    return (float(frame.attrib["x"]) - left) / extent, float(frame.attrib["width"]) / extent


def _assert_row_reference(report: Readings) -> None:
    inset, span = _reference_frame()
    assert report["frame"] == {"inset": inset, "span": span}
    tiles = {tile["n"]: tile for tile in report["tiles"]}
    for n in (5, 11, 18):
        tile = tiles[n]
        reference = tile["reference"]
        assert tile["smaller"]
        assert reference is not None
        assert reference["width"] == pytest.approx(tile["slot_width"] * span, abs=0.03)
        assert reference["height"] == reference["width"]
        assert reference["left"] - tile["tile"]["left"] == pytest.approx(
            tile["padding"] + tile["slot_width"] * inset, abs=0.03
        )
        assert reference["top"] - tile["tile"]["top"] == pytest.approx(
            tile["padding"] + tile["slot_width"] * inset, abs=0.03
        )
        drawing = tile["drawing"]
        assert drawing["left"] + drawing["width"] / 2 == pytest.approx(
            reference["left"] + reference["width"] / 2, abs=0.03
        )
        assert drawing["top"] + drawing["height"] / 2 == pytest.approx(
            reference["top"] + reference["height"] / 2, abs=0.03
        )
        assert drawing["width"] * span < reference["width"]
        assert reference["pointer_events"] == "none"
        assert reference["fill"] == "rgba(0, 0, 0, 0)"
        assert reference["box_sizing"] == "border-box"
        assert reference["border_style"] == "solid"
        assert 0 < reference["border_width"] <= 1
    for n in (1, 2, 3, 4, 6, 9, 12, 16, 25, 36, 100):
        assert not tiles[n]["smaller"]
        assert tiles[n]["reference"] is None


@pytest.mark.parametrize("view", ["triangle", "grid"])
def test_row_reference_outlines_smaller_containers_at_the_fixed_frame(
    seen: Readings, view: str
) -> None:
    _assert_row_reference(seen[f"reference, {view}, row"])
    for scale in ("fixed", "global"):
        assert all(
            tile["reference"] is None for tile in seen[f"reference, {view}, {scale}"]["tiles"]
        )


@pytest.mark.parametrize("view", ["triangle", "grid"])
def test_row_reference_prepaints_on_a_phone_and_keeps_script_fallbacks(
    seen: Readings, view: str
) -> None:
    for state in ("initial", "mounted"):
        _assert_row_reference(seen[f"{state} reference, {view}, row"])
    for scale in ("fixed", "global"):
        assert all(
            tile["reference"] is None
            for tile in seen[f"initial reference, {view}, {scale}"]["tiles"]
        )
    _assert_row_reference(seen["reference without bootstrap, row"])
    for mode in ("global", "invalid"):
        assert all(
            tile["reference"] is None
            for tile in seen[f"reference without bootstrap, {mode}"]["tiles"]
        )
    assert all(tile["reference"] is None for tile in seen["reference, no JavaScript"]["tiles"])


def test_row_reference_uses_neutral_theme_ink_and_has_no_hit_target(seen: Readings) -> None:
    _assert_row_reference(seen["reference, dark"])
    light = seen["reference, triangle, row"]["tiles"]
    dark = seen["reference, dark"]["tiles"]
    light_ink = {tile["reference"]["ink"] for tile in light if tile["reference"]}
    dark_ink = {tile["reference"]["ink"] for tile in dark if tile["reference"]}
    assert len(light_ink) == len(dark_ink) == 1
    assert light_ink != dark_ink
