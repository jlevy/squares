"""A Triangle reached from the top of either Atlas page follows the scroll (think-apqd).

`overview/atlas-view.js` lays the triangle out once, at Large, on a stage the height of
the window that the browser pins while the block's runway scrolls past, and zooms and
pans it as one picture: one smooth curve of zoom from Large down to the least zoom, the
middle of the window a third of the way along the reader's row while that row's left end
stays in view, and at the end a smooth turn from moving up to sliding to the triangle's
left edge. The page's own scroll is never touched, so scrolling back up retraces it.
A sideways wheel pans the triangle while the page scrolls, and fades back at the top; the
small sideways wobble of a swipe down pans nothing. Until the programs frame it the
triangle is out of sight, so the first paint never shows it anywhere else.
A size or view tab ends the following, and so does a fragment or a tile reached from the
keyboard off the stage; the block then takes the size its tabs show, or the one pressed,
with the reader's row where it stood, and the following's listeners go. An address that
names a size, a view, a fragment or an embedding never starts it, and nor does a reader
who asks for reduced motion. A new width lays the triangle out again as a page opened
at that width lays it out; a phone's toolbar showing or hiding moves nothing. The rows
are drawn into one compositor layer.

This reads all of that in Chromium a frame at a time, with the page scrolled as a wheel
scrolls it, and the layers and listeners over the DevTools protocol.
`tests/node/overview_atlas_view` holds the arithmetic; the browser is what says the page
draws it.
"""

from __future__ import annotations

import os
import re
from collections.abc import Iterator
from itertools import pairwise
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

import pytest

from devtools import check_site_rendering, preview_site
from sqpack.probes import probe
from tests import site_browser, site_renders

PROBES = Path(__file__).resolve().parent / "probes"
STATE = probe(PROBES, "site_atlas_follow/state")
STEP = probe(PROBES, "site_atlas_follow/step")
WHEEL = probe(PROBES, "site_atlas_follow/wheel")
PREPAINT = probe(PROBES, "site_atlas_follow/prepaint")
QUIET = probe(PROBES, "site_atlas_follow/quiet")
FRAMES = probe(PROBES, "site_atlas_follow/frames")
UNVEIL = probe(PROBES, "site_atlas_follow/unveil")
ROWS = probe(PROBES, "site_atlas_follow/rows")
SEEK = probe(PROBES, "site_atlas_follow/seek")
FOCUS = probe(PROBES, "site_atlas_follow/focus")
FOCUSED = probe(PROBES, "site_atlas_follow/focused")
JUMP = probe(PROBES, "site_atlas_follow/jump")
PRESS = probe(PROBES, "site_atlas_follow/press")
MIDDLE = probe(PROBES, "site_atlas_follow/middle")
WHOLE = probe(PROBES, "site_atlas_follow/whole")

DESKTOP = {"width": 1280, "height": 900}
PHONE = {"width": 390, "height": 844}
#: The cases at the triangle's top whose records the site serves, so a pressed tile
#: opens its case in the popover rather than going to a page that is not there.
PRESSED = tuple(range(1, 10))
#: One turn of a reader's wheel, in pixels.
TURN = 24
#: Where the middle of the window stands along the reader's row (site.css).
ACROSS = 0.333
#: The least size a case number is drawn at while zoomed, 0.65rem.
LEGIBLE = 10.4
SIZES = ("small", "medium", "large", "xlarge")


@pytest.fixture(scope="module")
def browser() -> Iterator[Any]:
    with site_browser.api().sync_playwright() as driver:
        launched = site_browser.launch(driver)
        try:
            yield launched
        finally:
            launched.close()


@pytest.fixture(scope="module")
def served(tmp_path_factory: pytest.TempPathFactory) -> Iterator[tuple[str, Path | None]]:
    """Both Atlas pages served with their real assets, and where they are written, if
    here."""
    address = os.environ.get("SQPACK_SITE_PREVIEW_URL")
    if address:
        yield address.rstrip("/") + "/", None
        return
    root = Path(tmp_path_factory.mktemp("site"))
    site_renders.write(root, "atlas.html", "index.html")
    server = preview_site.serve(root, 0)
    try:
        yield f"http://127.0.0.1:{server.server_port}/", root
    finally:
        server.shutdown()
        server.server_close()


@pytest.fixture(scope="module")
def site(served: tuple[str, Path | None]) -> str:
    return served[0]


@pytest.fixture(scope="module")
def cases(served: tuple[str, Path | None]) -> str:
    """The same site with the records of the cases `PRESSED`, written only for the test
    that opens one, since rendering them takes tens of seconds."""
    address, root = served
    if root is not None:
        from devtools import site_assets  # noqa: PLC0415

        records = site_renders.case_records(PRESSED)
        for name, record in records.items():
            (root / name).parent.mkdir(exist_ok=True)
            (root / name).write_text(record, encoding="utf-8")
        site_assets.write_assets(root, site_assets.shared().assets.referenced(records.values()))
    return address


def _open(browser: Any, address: str, window: dict[str, int]) -> Any:
    page = browser.new_page(viewport=window)
    page.goto(address, wait_until="load")
    check_site_rendering.wait_for_fonts(page)
    page.wait_for_selector("[data-atlas-grid][data-atlas-ready]")
    return page


def _read(page: Any) -> dict[str, Any]:
    reading = page.evaluate(STATE)
    assert reading is not None
    return reading


def _layers(page: Any) -> list[dict[str, Any]]:
    """The compositor's layers that draw content, as it reports them over the DevTools
    protocol (`LayerTree`) after a small scroll and five frames."""
    session = page.context.new_cdp_session(page)
    trees: list[dict[str, Any]] = []

    # A function of its own: Playwright marks the handler, which a bound method refuses.
    def changed(event: dict[str, Any]) -> None:
        trees.append(event)

    session.on("LayerTree.layerTreeDidChange", changed)
    session.send("LayerTree.enable")
    page.evaluate(STEP, {"by": 2})
    page.evaluate(FRAMES, {"count": 5})
    session.detach()
    layers = trees[-1].get("layers", []) if trees else []
    return [layer for layer in layers if layer.get("drawsContent")]


def _listeners(page: Any, selector: str) -> list[str]:
    """The kinds of event the element `selector` names is listened to for, one a listener,
    as the DevTools protocol lists them (`DOMDebugger.getEventListeners`)."""
    session = page.context.new_cdp_session(page)
    root = session.send("DOM.getDocument", {"depth": 0})["root"]["nodeId"]
    node = session.send("DOM.querySelector", {"nodeId": root, "selector": selector})["nodeId"]
    remote = session.send("DOM.resolveNode", {"nodeId": node})["object"]["objectId"]
    found = session.send("DOMDebugger.getEventListeners", {"objectId": remote})["listeners"]
    session.detach()
    return sorted(listener["type"] for listener in found)


def _scroll(page: Any, by: int, *, limit: int = 400) -> list[dict[str, Any]]:
    """Turn the wheel `by` pixels a turn, reading each turn: down until the page reaches
    its end or the atlas has passed above the window, up until the page's top."""
    readings = []
    for _ in range(limit):
        where = page.evaluate(STEP, {"by": by})
        readings.append(_read(page))
        if (where["past"] or where["end"]) if by > 0 else where["top"]:
            break
    return readings


@pytest.mark.parametrize("name", ["atlas.html", "index.html"])
def test_the_triangle_opens_at_large_and_mounting_moves_nothing(
    browser: Any, site: str, name: str
) -> None:
    programs = re.compile(r"/assets/js/atlas-(view|grid)\.")
    page = browser.new_page(viewport=DESKTOP)
    try:
        page.route(programs, lambda route: route.abort())
        page.goto(site + name, wait_until="load")
        check_site_rendering.wait_for_fonts(page)
        before = page.evaluate(PREPAINT)
        hidden = page.evaluate(UNVEIL)
        page.unroute(programs)
        page.reload(wait_until="load")
        check_site_rendering.wait_for_fonts(page)
        page.wait_for_selector("[data-atlas-grid][data-atlas-ready]")
        after = page.evaluate(PREPAINT)
        shown = page.evaluate(UNVEIL)
        state = _read(page)
    finally:
        page.close()
    assert before["armed"]
    assert before["follow"] is None
    assert not before["zoomed"]
    assert before["scale"] == 2.25
    assert before["number"] == pytest.approx(2.4 * 16, abs=0.01)
    assert after["tile"] == pytest.approx(before["tile"], abs=0.03)
    assert after["number"] == pytest.approx(before["number"], abs=0.01)
    assert (after["follow"], after["zoomed"], after["size"]) == ("scroll", True, "xlarge")
    assert (state["scale"], state["shown"]) == (1, "xlarge")
    assert not state["explicit"]
    # The browser paints before the programs run; until they frame it the stage is out of
    # sight, so it never stands at its right end first. Without them it shows after 2s;
    # framed, it fades in where it stands.
    assert hidden == {"delay": 2000, "length": 0, "start": 0, "end": 1}
    assert shown == {"delay": 0, "length": 250, "start": 0, "end": 1}


@pytest.mark.parametrize(
    ("name", "window"),
    [("atlas.html", DESKTOP), ("index.html", DESKTOP), ("atlas.html", PHONE)],
    ids=["atlas-desktop", "home-desktop", "atlas-phone"],
)
def test_scrolling_down_zooms_out_then_slides_to_the_left_edge(
    browser: Any, site: str, name: str, window: dict[str, int]
) -> None:
    page = _open(browser, site + name, window)
    try:
        start = _read(page)
        down = _scroll(page, TURN)
    finally:
        page.close()
    assert (start["scale"], start["shown"], start["follow"]) == (1, "xlarge", "scroll")
    assert all(reading["follow"] == "scroll" for reading in down)
    # The page's own scroll is never pulled back: each turn moves it on or not at all.
    for one, other in pairwise(down):
        assert other["scrollY"] >= one["scrollY"]
        # The zoom only shrinks going down, to its floor, where the numbers still read.
        assert other["scale"] <= one["scale"] + 1e-9
    least = min(reading["scale"] for reading in down)
    assert least < 0.6
    assert all(reading["number"] >= LEGIBLE - 0.1 for reading in down)
    # The tabs show each size in turn as the zoom passes it.
    shown = [SIZES.index(reading["shown"]) for reading in down]
    assert shown == sorted(shown, reverse=True)
    assert set(shown) == {0, 1, 2, 3}
    # Pinned, the point at the focus line passes it at the page's own speed: a turn
    # moves it by the turn at the zoom the turn began at, until the rows begin to slow.
    end = down[0]["end"]
    stop = min(window["height"] / 4, end / 2)
    for one, other in pairwise(down):
        if one["scrolled"] > 0 and other["scrolled"] < end - stop:
            moved = other["scrolled"] - one["scrolled"]
            assert other["point"] - one["point"] == pytest.approx(
                moved / one["scale"], abs=2 / one["scale"]
            )
    # The framing: the row's left end never leaves the stage, and away from the bends at
    # the right edge and the left, each a quarter of the stage's width, the middle stands
    # a third along the row.
    for reading in down:
        assert reading["leftEnd"] >= -0.003
        framed = reading["pan"] < -0.3 * reading["room"] and reading["leftEnd"] > 0.3
        if framed and reading["scrolled"] < end - stop:
            assert reading["across"] == pytest.approx(ACROSS, abs=0.01)
    # Past the bottom the triangle slides all the way to its left edge.
    assert abs(down[-1]["lastLeft"]) < 0.005
    # Its pan and its zoom change speed a little at a time all the way down, from rest
    # at the top: no turn of the wheel starts, stops or turns them with a jolt.
    for key in ("pan", "scale"):
        values = [reading[key] for reading in [start, *down]]
        speeds = [0, *(other - one for one, other in pairwise(values))]
        typical = max(abs(speed) for speed in speeds)
        jolts = [
            (index, one, other)
            for index, (one, other) in enumerate(pairwise(speeds))
            if abs(other - one) >= 0.3 * typical
        ]
        assert not jolts, (key, typical, jolts[:5])
    # Nothing scrolls the page but the reader, so the header, which hides once the page
    # has scrolled down past it, stays hidden from then on.
    hidden = [reading["headerHidden"] for reading in down]
    assert True in hidden
    assert all(hidden[hidden.index(True) :])


@pytest.mark.parametrize(
    ("name", "window"),
    [("atlas.html", DESKTOP), ("index.html", DESKTOP), ("atlas.html", PHONE)],
    ids=["atlas-desktop", "home-desktop", "atlas-phone"],
)
def test_the_pan_sets_off_from_rest_and_gathers_speed_smoothly(
    browser: Any, site: str, name: str, window: dict[str, int]
) -> None:
    """From the page's top the pan starts at no speed, only to the right, and its speed
    changes a little at a time (the owner, 2026-10-23): it once set off at most of its
    speed with the first pixel of scroll."""
    step = 8
    page = _open(browser, site + name, window)
    try:
        readings = [_read(page)]
        for _ in range(2 * window["height"] // step):
            page.evaluate(STEP, {"by": step})
            readings.append(_read(page))
    finally:
        page.close()
    speeds = [one["pan"] - other["pan"] for one, other in pairwise(readings)]
    moving = [index for index, speed in enumerate(speeds) if abs(speed) > 0.01]
    assert moving, speeds
    typical = max(abs(speed) for speed in speeds)
    assert typical > 1, speeds
    first = moving[0]
    assert speeds[first] < 0.05 * typical, speeds[first : first + 8]
    # Over the stretch it takes to come up to speed it moves only one way, to the right.
    launched = first + int(0.6 * window["height"] / step)
    assert all(speed >= -0.01 for speed in speeds[first:launched]), speeds
    for one, other in pairwise(speeds):
        assert abs(other - one) < 0.1 * typical, (one, other, typical)


def test_scrolling_back_up_retraces_the_zoom_and_the_pan(browser: Any, site: str) -> None:
    page = _open(browser, site + "atlas.html", DESKTOP)
    try:
        start = _read(page)
        down = _scroll(page, TURN)
        up = _scroll(page, -TURN)
        page.evaluate(FRAMES, {"count": 10})
        end = _read(page)
    finally:
        page.close()
    for one, other in pairwise(up):
        assert other["scale"] >= one["scale"] - 1e-9
    assert (end["scrollY"], end["scale"], end["shown"], end["follow"]) == (
        0,
        1,
        "xlarge",
        "scroll",
    )
    assert end["pan"] == pytest.approx(start["pan"], abs=0.5)
    # Zoom and pan are a function of the scroll alone, the same both ways.
    going = {round(reading["scrollY"]): reading for reading in down}
    for reading in up:
        same = going.get(round(reading["scrollY"]))
        if same is not None:
            assert reading["scale"] == pytest.approx(same["scale"], abs=1e-6)
            assert reading["pan"] == pytest.approx(same["pan"], abs=0.5)


def test_a_sideways_wheel_pans_while_the_page_scrolls(browser: Any, site: str) -> None:
    page = _open(browser, site + "atlas.html", DESKTOP)
    try:
        for _ in range(60):
            page.evaluate(STEP, {"by": TURN})
        before = _read(page)
        # A swipe down that wobbles a little sideways pans nothing.
        for x in (3, -2, 4, 2, 1, 3):
            page.evaluate(WHEEL, {"x": x, "y": TURN})
        straight = _read(page)
        page.evaluate(FRAMES, {"count": 12})
        # A diagonal gesture: each turn moves the page down and the triangle sideways,
        # past the first 16 pixels of slack, easing back a little as the page scrolls.
        for _ in range(8):
            page.evaluate(WHEEL, {"x": -20, "y": TURN})
        diagonal = _read(page)
        _scroll(page, -TURN)
        page.evaluate(FRAMES, {"count": 60})
        top = _read(page)
    finally:
        page.close()
    assert before["follow"] == diagonal["follow"] == "scroll"
    assert diagonal["scrollY"] > before["scrollY"]
    assert straight["nudge"] == 0
    assert -144 < diagonal["nudge"] < -100
    # Back at the top the reader's own pan has eased away.
    assert (top["nudge"], top["scale"], top["follow"]) == (0, 1, "scroll")


def test_a_pressed_tab_keeps_the_readers_atlas(browser: Any, site: str) -> None:
    page = _open(browser, site + "atlas.html", DESKTOP)
    try:
        for _ in range(10):
            page.evaluate(STEP, {"by": TURN})
        page.locator('[data-atlas-size-tab="medium"]').click()
        pressed = _read(page)
        page.wait_for_function(QUIET)
        settled = _read(page)
        query = urlsplit(page.url).query
        _scroll(page, TURN, limit=40)
        later = _read(page)
    finally:
        page.close()
    assert pressed["moving"] > 0, "the tab moves the tiles to their size"
    assert (settled["zoomed"], settled["size"], settled["follow"]) == (False, "medium", "held")
    assert settled["explicit"]
    assert settled["shown"] == "medium"
    assert query == "size=medium"
    # A chosen size stays chosen as the page scrolls on.
    assert (later["zoomed"], later["size"]) == (False, "medium")

    # Grid, or a tile's fragment, deep in the journey, where the zoom has passed XL: the
    # block takes the size the tabs show, the one the reader was looking at, so the tabs
    # and the tiles agree. They once showed it while Grid opened at XL.
    for act in ("grid", "fragment"):
        page = _open(browser, site + "atlas.html", DESKTOP)
        try:
            page.evaluate(STEP, {"by": 1500})
            deep = _read(page)
            if act == "grid":
                assert page.evaluate(PRESS, {"selector": '[data-atlas-tab="grid"]'})
            else:
                assert page.evaluate(JUMP, {"hash": "#atlas-n-53"}) == "#atlas-n-53"
            page.wait_for_function(QUIET)
            ended = _read(page)
        finally:
            page.close()
        assert (deep["follow"], deep["size"]) == ("scroll", "xlarge")
        assert deep["shown"] != "xlarge", act
        assert (ended["follow"], ended["zoomed"]) == ("held", False), act
        assert ended["view"] == ("grid" if act == "grid" else "triangle")
        assert ended["size"] == ended["shown"] == deep["shown"], act
        assert not ended["explicit"]


@pytest.mark.parametrize(
    ("name", "query", "size"),
    [
        ("atlas.html", "?size=small", "small"),
        ("atlas.html", "?atlas=grid", "medium"),
        ("atlas.html", "#the-atlas", "medium"),
        ("index.html", "#the-atlas", "medium"),
        ("atlas.html", "?view=embed", "medium"),
    ],
)
def test_an_address_naming_a_size_view_fragment_or_embedding_does_not_follow(
    browser: Any, site: str, name: str, query: str, size: str
) -> None:
    page = _open(browser, site + name + query, DESKTOP)
    try:
        start = page.evaluate(PREPAINT)
        for _ in range(20):
            page.evaluate(STEP, {"by": TURN})
        later = page.evaluate(PREPAINT)
    finally:
        page.close()
    assert (start["armed"], start["follow"], start["zoomed"]) == (False, None, False)
    assert start["size"] == size == later["size"]
    assert later["follow"] is None


@pytest.mark.parametrize("name", ["atlas.html", "index.html"])
def test_a_reader_who_asks_for_reduced_motion_is_not_followed(
    browser: Any, site: str, name: str
) -> None:
    """With reduced motion the bootstrap leaves the root unmarked and the programs do not
    follow: the triangle opens at its static default size and stays there."""
    programs = re.compile(r"/assets/js/atlas-(view|grid)\.")
    page = browser.new_page(viewport=DESKTOP, reduced_motion="reduce")
    try:
        page.route(programs, lambda route: route.abort())
        page.goto(site + name, wait_until="load")
        check_site_rendering.wait_for_fonts(page)
        painted = page.evaluate(PREPAINT)
        page.unroute(programs)
        page.reload(wait_until="load")
        check_site_rendering.wait_for_fonts(page)
        page.wait_for_selector("[data-atlas-grid][data-atlas-ready]")
        start = page.evaluate(PREPAINT)
        for _ in range(20):
            page.evaluate(STEP, {"by": TURN})
        later = page.evaluate(PREPAINT)
    finally:
        page.close()
    # Medium's scale, the wide screen's static default, from the first paint.
    assert (painted["armed"], painted["scale"]) == (False, 1)
    for reading in (start, later):
        assert (reading["armed"], reading["follow"], reading["zoomed"]) == (False, None, False)
        assert (reading["size"], reading["scale"]) == ("medium", 1)


@pytest.mark.parametrize(
    ("window", "turned", "scroll"),
    [
        (PHONE, {"width": 844, "height": 390}, 1500),
        (DESKTOP, {"width": 1000, "height": 900}, 1200),
    ],
    ids=["phone-turned", "desktop-narrowed"],
)
def test_a_new_width_lays_the_triangle_out_as_a_page_opened_at_it(
    browser: Any, site: str, window: dict[str, int], turned: dict[str, int], scroll: int
) -> None:
    """A window narrowed or a phone turned mid-journey draws the triangle as a page opened
    at the new size draws it at the same place in the journey, after one new layout. The
    triangle was once laid out a frame before the tiles were, against the tiles the old
    width held: its rows overlapped on a turned phone and stood far apart on a desktop."""
    page = _open(browser, site + "atlas.html", window)
    try:
        page.evaluate(STEP, {"by": scroll})
        before = page.evaluate(ROWS)
        page.set_viewport_size(turned)
        page.evaluate(FRAMES, {"count": 5})
        resized = page.evaluate(ROWS)
    finally:
        page.close()
    page = _open(browser, site + "atlas.html", turned)
    try:
        page.evaluate(SEEK, {"to": resized["reading"]["scrolled"]})
        fresh = page.evaluate(ROWS)
    finally:
        page.close()
    assert resized["follow"] == fresh["follow"] == "scroll"
    assert 0 < resized["reading"]["scrolled"] < resized["reading"]["end"]
    assert fresh["reading"]["scrolled"] == pytest.approx(
        resized["reading"]["scrolled"], abs=0.5
    )
    assert resized["stage"] == fresh["stage"] == turned["height"]
    assert resized["reading"]["end"] == pytest.approx(fresh["reading"]["end"], abs=2)
    assert resized["reading"]["zoom"] == pytest.approx(fresh["reading"]["zoom"], abs=1e-3)
    assert resized["reading"]["point"] == pytest.approx(fresh["reading"]["point"], abs=1)
    assert resized["reading"]["pan"] == pytest.approx(fresh["reading"]["pan"], abs=1)
    assert len(resized["rows"]) == len(fresh["rows"])
    for one, other in zip(resized["rows"], fresh["rows"], strict=True):
        for key in ("top", "left", "right"):
            assert one[key] == pytest.approx(other[key], abs=1), (key, one, other)
    # The ResizeObserver and the window's resize both ask; the triangle is laid out once.
    assert resized["reading"]["lays"] == before["reading"]["lays"] + 1


def test_a_phone_toolbar_leaves_the_rows_where_they_stand(browser: Any, site: str) -> None:
    """A phone's toolbar showing or hiding as the page scrolls changes the window's height
    alone, by a little: the rows stay where they stand and the journey keeps its length,
    where they once jumped some 60 pixels and the page changed its height. A change of
    height past a toolbar's lays the triangle out for it."""
    page = _open(browser, site + "atlas.html", PHONE)
    try:
        # Most of the way through the journey, where the rows have zoomed out.
        end = _read(page)["end"]
        page.evaluate(SEEK, {"to": 0.7 * end})
        before = page.evaluate(ROWS)
        page.set_viewport_size({"width": PHONE["width"], "height": PHONE["height"] - 64})
        page.evaluate(FRAMES, {"count": 5})
        shown = page.evaluate(ROWS)
        page.set_viewport_size(PHONE)
        page.evaluate(FRAMES, {"count": 5})
        hidden = page.evaluate(ROWS)
        page.set_viewport_size({"width": PHONE["width"], "height": 600})
        page.evaluate(FRAMES, {"count": 5})
        shorter = page.evaluate(ROWS)
    finally:
        page.close()
    assert before["follow"] == "scroll"
    assert 0 < before["reading"]["scrolled"] < before["reading"]["end"]
    for after in (shown, hidden):
        for one, other in zip(before["rows"], after["rows"], strict=True):
            assert other["top"] == pytest.approx(one["top"], abs=1)
            assert other["left"] == pytest.approx(one["left"], abs=1)
        assert after["reading"]["end"] == before["reading"]["end"]
        assert (after["stage"], after["page"]) == (before["stage"], before["page"])
        assert after["reading"]["lays"] == before["reading"]["lays"]
    assert shorter["stage"] == 600
    assert shorter["reading"]["lays"] == before["reading"]["lays"] + 1


@pytest.mark.parametrize("scroll", [0, 1200], ids=["top", "journey"])
@pytest.mark.parametrize("name", ["atlas.html", "index.html"])
def test_a_tile_reached_from_the_keyboard_is_drawn_in_view(
    browser: Any, site: str, name: str, scroll: int
) -> None:
    """Tabbing from the size tabs through the tiles: every tile the focus reaches is drawn
    where the window shows it. The stage clips, and once 35 of 43 tiles were focused off
    it; a tile off the stage now ends the following and is brought into view."""
    page = _open(browser, site + name, DESKTOP)
    try:
        if scroll:
            page.evaluate(STEP, {"by": scroll})
        assert page.evaluate(FOCUS)
        focused = []
        for _ in range(45):
            page.keyboard.press("Tab")
            focused.append(page.evaluate(FOCUSED))
        state = _read(page)
    finally:
        page.close()
    tiles = [reading for reading in focused if reading["n"] is not None]
    assert len(tiles) >= 30
    assert all(reading["visible"] for reading in tiles)
    assert [reading["n"] for reading in tiles if not reading["seen"]] == []
    assert (state["follow"], state["zoomed"]) == ("held", False)
    assert state["size"] == state["shown"]


def test_a_pressed_tile_opens_its_case_and_keeps_the_following(
    browser: Any, cases: str
) -> None:
    """A pointer on a tile in view opens its case in the popover, and the triangle keeps
    following, as it did before keyboard focus ended it; Escape puts the focus back on
    the tile, which is in view, so the following holds then too."""
    page = _open(browser, cases + "atlas.html", DESKTOP)
    try:
        target = page.evaluate(WHOLE, {"cases": list(PRESSED)})
        assert target is not None
        page.mouse.click(target["x"], target["y"])
        article = page.locator(f'#pop-case article.site-case[data-case="{target["n"]}"]')
        site_browser.api().expect(article).to_be_visible()
        opened = _read(page)
        page.keyboard.press("Escape")
        back = page.evaluate(FOCUSED)
        closed = _read(page)
    finally:
        page.close()
    assert (opened["follow"], opened["zoomed"]) == ("scroll", True)
    assert (back["n"], back["visible"], back["seen"]) == (str(target["n"]), True, True)
    assert (closed["follow"], closed["zoomed"]) == ("scroll", True)


@pytest.mark.parametrize("step", [-1, 1], ids=["smaller", "larger"])
def test_a_pressed_size_keeps_the_readers_row_in_place(
    browser: Any, site: str, step: int
) -> None:
    """Pressing a size next to the one the tabs show, mid-journey, lays the triangle out at
    that size with the tile at the middle of the stage on the focus line moved across by
    less than a tile. The scroller once took the zoomed pan's pixels as the new layout's,
    and that tile moved three tiles or more."""
    page = _open(browser, site + "atlas.html", DESKTOP)
    try:
        page.evaluate(STEP, {"by": 1500})
        deep = _read(page)
        looked = page.evaluate(MIDDLE, {"n": None})
        pressed = SIZES[SIZES.index(deep["shown"]) + step]
        assert page.evaluate(PRESS, {"selector": f'[data-atlas-size-tab="{pressed}"]'})
        page.wait_for_function(QUIET)
        settled = _read(page)
        kept = page.evaluate(MIDDLE, {"n": looked["n"]})
    finally:
        page.close()
    assert deep["follow"] == "scroll"
    assert deep["shown"] in {"medium", "large"}
    assert abs(looked["offset"]) < looked["width"]
    assert (settled["follow"], settled["zoomed"], settled["size"]) == ("held", False, pressed)
    assert abs(kept["offset"] - looked["offset"]) < kept["width"], (looked, kept)


def test_the_following_triangle_is_drawn_into_one_layer(browser: Any, site: str) -> None:
    """The script wraps a following triangle's rows in one picture and zooms and pans that
    one layer, so following composites no more layers than the same triangle at XL that
    stands still. Each of its 18 rows was once a layer of its own, 22 layers against 5."""
    counts = {}
    for query in ("", "?size=xlarge"):
        page = _open(browser, site + "atlas.html" + query, DESKTOP)
        try:
            page.evaluate(STEP, {"by": 1200})
            counts[query] = len(_layers(page))
            followed = _read(page)["follow"]
        finally:
            page.close()
        assert followed == ("scroll" if query == "" else None)
    assert counts[""] <= counts["?size=xlarge"] + 1, counts


def test_the_following_takes_its_listeners_with_it_when_it_ends(
    browser: Any, site: str
) -> None:
    """The stage's wheel, pointer, scroll and focus listeners are the following's: when a
    tab ends it they go, rather than staying on as handlers that do nothing."""
    stage = "[data-atlas-grid] .site-atlas-cells"
    page = _open(browser, site + "atlas.html", DESKTOP)
    try:
        page.evaluate(STEP, {"by": 600})
        following = _listeners(page, stage)
        assert page.evaluate(PRESS, {"selector": '[data-atlas-size-tab="large"]'})
        page.wait_for_function(QUIET)
        held = _listeners(page, stage)
        state = _read(page)
    finally:
        page.close()
    added = {
        "focusin",
        "pointercancel",
        "pointerdown",
        "pointermove",
        "pointerup",
        "scroll",
        "wheel",
    }
    assert state["follow"] == "held"
    assert not added & set(held), held
    assert added <= set(following), following
