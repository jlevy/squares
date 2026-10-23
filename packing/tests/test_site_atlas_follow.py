"""A Triangle reached from the top of either Atlas page follows the scroll (think-apqd).

`overview/atlas-view.js` lays the triangle out once, at Large, on a stage the height of
the window that the browser pins while the block's runway scrolls past, and zooms and
pans it as one picture: one smooth curve of zoom from Large down to the least zoom, the
middle of the window a third of the way along the reader's row while that row's left end
stays in view, and at the end a smooth turn from moving up to sliding to the triangle's
left edge. The page's own scroll is never touched, so scrolling back up retraces it.
A sideways wheel pans the triangle while the page scrolls, and fades back at the top.
A size or view tab ends the following; an address that names a size, a view, a fragment
or an embedding never starts it.

This reads all of that in Chromium a frame at a time, with the page scrolled as a wheel
scrolls it. `tests/node/overview_atlas_view` holds the arithmetic; the browser is what
says the page draws it.
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

DESKTOP = {"width": 1280, "height": 900}
PHONE = {"width": 390, "height": 844}
#: One turn of a reader's wheel, in pixels.
TURN = 24
#: Where the middle of the window stands along the reader's row (site.css).
ACROSS = 0.333
#: The least size a case number is drawn at while zoomed, 0.65rem.
LEGIBLE = 10.4
SIZES = ("small", "medium", "large")


@pytest.fixture(scope="module")
def browser() -> Iterator[Any]:
    with site_browser.api().sync_playwright() as driver:
        launched = site_browser.launch(driver)
        try:
            yield launched
        finally:
            launched.close()


@pytest.fixture(scope="module")
def site(tmp_path_factory: pytest.TempPathFactory) -> Iterator[str]:
    """Both Atlas pages served with their real assets."""
    address = os.environ.get("SQPACK_SITE_PREVIEW_URL")
    if address:
        yield address.rstrip("/") + "/"
        return
    root = Path(tmp_path_factory.mktemp("site"))
    site_renders.write(root, "atlas.html", "index.html")
    server = preview_site.serve(root, 0)
    try:
        yield f"http://127.0.0.1:{server.server_port}/"
    finally:
        server.shutdown()
        server.server_close()


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
        page.unroute(programs)
        page.reload(wait_until="load")
        check_site_rendering.wait_for_fonts(page)
        page.wait_for_selector("[data-atlas-grid][data-atlas-ready]")
        after = page.evaluate(PREPAINT)
        state = _read(page)
    finally:
        page.close()
    assert before["armed"]
    assert before["follow"] is None
    assert not before["zoomed"]
    assert before["scale"] == 1.5
    assert before["number"] == pytest.approx(1.45 * 16, abs=0.01)
    assert after["tile"] == pytest.approx(before["tile"], abs=0.03)
    assert after["number"] == pytest.approx(before["number"], abs=0.01)
    assert (after["follow"], after["zoomed"], after["size"]) == ("scroll", True, "large")
    assert (state["scale"], state["pan"], state["shown"]) == (1, 0, "large")
    assert not state["explicit"]


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
    assert (start["scale"], start["shown"], start["follow"]) == (1, "large", "scroll")
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
    assert set(shown) == {0, 1, 2}
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
    # Nothing scrolls the page but the reader, so a header hidden on the way down stays
    # hidden.
    hidden = [reading["headerHidden"] for reading in down]
    if True in hidden:
        assert all(hidden[hidden.index(True) :])


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
        "large",
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
        # A diagonal gesture: each turn moves the page down and the triangle sideways.
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
    assert diagonal["nudge"] == pytest.approx(-160, abs=1)
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

    page = _open(browser, site + "atlas.html", DESKTOP)
    try:
        for _ in range(10):
            page.evaluate(STEP, {"by": TURN})
        page.locator('[data-atlas-tab="grid"]').click()
        page.wait_for_function(QUIET)
        grid = _read(page)
    finally:
        page.close()
    assert (grid["follow"], grid["zoomed"], grid["view"]) == ("held", False, "grid")


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
