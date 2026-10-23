"""A Triangle reached from the top of either Atlas page follows the scroll (think-apqd).

`overview/atlas-view.js` lays the triangle out once, at Large, and zooms it as one
picture as the reader scrolls down: the middle of the window stays a third of the way
along the reader's row while that row's left end stays in view, the page scrolls to keep
that row under the focus line, and the scroller pans along the triangle's left side.
Scrolling back up retraces it. A pan by hand or a size or view tab ends the following
and leaves the reader's atlas as it stands; an address that names a size, a view, a
fragment or an embedding never starts it.

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
PAN = probe(PROBES, "site_atlas_follow/pan")
PREPAINT = probe(PROBES, "site_atlas_follow/prepaint")
QUIET = probe(PROBES, "site_atlas_follow/quiet")

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
    """Turn the wheel `by` pixels a turn, reading each turn, until the page reaches its
    end, or its top, or the atlas has passed above the window. The last reading is the
    one at which the turn stopped short or the atlas went."""
    readings = []
    for _ in range(limit):
        where = page.evaluate(STEP, {"by": by})
        readings.append(_read(page))
        if where["past"] or (where["end"] if by > 0 else where["top"]):
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
def test_scrolling_down_zooms_out_then_pans_along_the_left_side(
    browser: Any, site: str, name: str, window: dict[str, int]
) -> None:
    page = _open(browser, site + name, window)
    try:
        start = _read(page)
        down = _scroll(page, TURN)
    finally:
        page.close()
    assert (start["scale"], start["pan"], start["shown"]) == (1, 0, "large")
    following = [reading for reading in down if reading["follow"] == "scroll"]
    assert len(following) == len(down), "a plain scroll never takes the atlas over"
    # The zoom only shrinks going down, to its floor, where the numbers still read.
    for one, other in pairwise(down):
        assert other["scale"] <= one["scale"] + 1e-6
        assert other["pan"] <= one["pan"] + 0.5
    least = min(reading["scale"] for reading in down)
    assert least < 0.6
    assert all(reading["number"] >= LEGIBLE - 0.1 for reading in down)
    # The tabs show each size in turn as the zoom passes it.
    shown = [SIZES.index(reading["shown"]) for reading in down]
    assert shown == sorted(shown, reverse=True)
    assert set(shown) == {0, 1, 2}
    assert down[-1]["pan"] < -100
    # The zoom keeps the reader's row under the focus line: a turn moves the reading by
    # the turn and by what the focus line moved, at the zoom the turn began at, and by
    # nothing that the change of zoom adds.
    for one, other in pairwise(down[:-1]):
        expected = (TURN + other["line"] - one["line"]) / one["scale"]
        assert other["point"] - one["point"] == pytest.approx(expected, abs=2 / one["scale"])
    # The framing: the row's left end never leaves the block, and once the scroller has
    # left its start, the middle stands a third along the row until the left end reaches
    # the edge.
    for reading in down:
        assert reading["leftEnd"] >= -0.003
        if reading["pan"] < -1 and reading["leftEnd"] > 0.003:
            assert reading["across"] == pytest.approx(ACROSS, abs=0.01)
    # The page's own scroll to keep the reader's row is not the reader's: once the header
    # has hidden on the way down it stays hidden.
    hidden = [reading["headerHidden"] for reading in down]
    if True in hidden:
        assert all(hidden[hidden.index(True) :])


def test_scrolling_back_up_retraces_the_zoom_and_the_pan(browser: Any, site: str) -> None:
    page = _open(browser, site + "atlas.html", DESKTOP)
    try:
        down = _scroll(page, TURN)
        up = _scroll(page, -TURN)
        end = _read(page)
    finally:
        page.close()
    for one, other in pairwise(up):
        assert other["scale"] >= one["scale"] - 1e-6
        assert other["pan"] >= one["pan"] - 0.5
    assert (end["scrollY"], end["scale"]) == (0, 1)
    assert (end["shown"], end["follow"]) == ("large", "scroll")
    assert abs(end["pan"]) < 0.5
    # The zoom is a function of where the reader is in the rows, the same both ways.
    points = sorted((reading["point"], reading["scale"]) for reading in down)
    for reading in up:
        nearest = min(points, key=lambda each: abs(each[0] - reading["point"]))
        if abs(nearest[0] - reading["point"]) < 2:
            assert reading["scale"] == pytest.approx(nearest[1], abs=0.01)


def test_a_pan_by_hand_or_a_pressed_tab_keeps_the_readers_atlas(
    browser: Any, site: str
) -> None:
    page = _open(browser, site + "atlas.html", DESKTOP)
    try:
        for _ in range(45):
            page.evaluate(STEP, {"by": TURN})
        zoomed = _read(page)
        assert zoomed["follow"] == "scroll"
        assert zoomed["scale"] < 1
        assert page.evaluate(PAN, {"by": 150})
        held = _read(page)
        for _ in range(10):
            page.evaluate(STEP, {"by": TURN})
        later = _read(page)
        page.locator('[data-atlas-size-tab="medium"]').click()
        pressed = _read(page)
        page.wait_for_function(QUIET)
        settled = _read(page)
        query = urlsplit(page.url).query
    finally:
        page.close()
    assert held["follow"] == "held"
    assert held["pan"] == pytest.approx(zoomed["pan"] + 150, abs=1)
    assert later["scale"] == held["scale"]
    assert later["pan"] == pytest.approx(held["pan"], abs=0.5)
    assert pressed["moving"] > 0, "the tab moves the tiles to their size"
    assert (settled["zoomed"], settled["scale"], settled["size"]) == (False, 1, "medium")
    assert settled["explicit"]
    assert settled["shown"] == "medium"
    assert query == "size=medium"

    page = _open(browser, site + "atlas.html", DESKTOP)
    try:
        for _ in range(45):
            page.evaluate(STEP, {"by": TURN})
        page.locator('[data-atlas-tab="grid"]').click()
        page.wait_for_function(QUIET)
        grid = _read(page)
    finally:
        page.close()
    assert (grid["follow"], grid["zoomed"], grid["view"], grid["scale"]) == (
        "held",
        False,
        "grid",
        1,
    )


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
