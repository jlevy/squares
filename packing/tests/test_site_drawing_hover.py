"""Packing links preserve their artwork under hover, keyboard focus and press.

Atlas cells load standalone SVGs with fixed dark ink and a white canvas in both page
themes. The homepage hero remains inline, using the page's ink. Both must preserve
their frame and square outlines when KPress changes a hovered link's text colour;
the atlas cell's only visual response is the wash behind it (think-8eb4).

Chromium decodes the actual asset and the probe reads its fetched SVG content,
geometry and styles in an isolated shadow root. Screenshot pixels on the frame and
canvas hold contrast and unchanged ink; pixels in the cell's padding hold its wash.
Each screenshot uses two device pixels per CSS pixel, so the frame covers a whole
pixel. The inline hero retains its original checks against the page's own ink.
"""

from __future__ import annotations

import io
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

import pytest
from PIL import Image, ImageColor

from devtools import check_site_rendering, preview_site, render_overview
from sqpack.probes import probe
from tests import site_browser, site_renders

PROBES = Path(__file__).resolve().parent / "probes"
DRAWING = probe(PROBES, "site_drawing_hover/drawing")

#: The case whose cell is read, and the cell before it, which keyboard focus leaves.
CASE = 11
CELL = f'.site-atlas-cell[data-atlas-n="{CASE}"]'
BEFORE = f'.site-atlas-cell[data-atlas-n="{CASE - 1}"]'
HERO = ".site-hero-figure a"
SCHEMES = ("light", "dark")
#: The states a cell is washed in, and the pseudo-classes each must be in.
WASHED = {
    "hover": {"hover": True, "focus_visible": False, "active": False},
    "focus": {"hover": False, "focus_visible": True, "active": False},
    "pressed": {"hover": True, "active": True},
}
#: Longer than `--site-hover-duration` (150ms at most), so a wash has finished.
SETTLE_MS = 400
#: A point of the page no drawing is under: the window's corner, in the bar's margin.
AWAY = (1, 1)
#: How far apart, summed over the three channels, a line and what it is drawn on must be
#: for the line to read. The cached SVG's fixed ink is 668 from its white canvas;
#: the inline hero's page ink is 594 or more from its ground in either theme. The
#: hovered link's teal failed this floor in the original regression.
READABLE = 540

type Pixel = tuple[int, int, int]
#: Every reading of the overview's drawings, by theme and then by state.
type Readings = dict[str, dict[str, Painted]]


@dataclass(frozen=True)
class Painted:
    """The probe's source/style reading, an actual frame-edge pixel, the holder's
    padding pixel, and the artwork's canvas pixel. Cached artwork requires an exact
    ink match; the inline hero selects the edge most distinct from its page ground."""

    state: dict[str, Any]
    ink: Pixel
    ground: Pixel
    canvas: Pixel


def _apart(one: Pixel, other: Pixel) -> int:
    return sum(abs(a - b) for a, b in zip(one, other, strict=True))


def _read(page: Any, holder: str) -> Painted:
    page.wait_for_timeout(SETTLE_MS)
    state = page.evaluate(DRAWING, {"holder": holder})
    assert state is not None, holder
    box, edge = state["box"], state["edge"]
    shot = Image.open(io.BytesIO(page.screenshot(clip=box))).convert("RGB")
    scale = shot.width / box["width"]

    def pixel(x: float, y: float) -> Pixel:
        found = shot.getpixel((round((x - box["x"]) * scale), round((y - box["y"]) * scale)))
        assert isinstance(found, tuple)
        red, green, blue = found
        return int(red), int(green), int(blue)

    ground = pixel(box["x"] + 2, box["y"] + 2)
    image = state["image_box"]
    canvas = ground
    if image:
        color = ImageColor.getrgb(state["frame_fill"])
        assert len(color) == 3
        expected = (color[0], color[1], color[2])
        area = shot.crop(
            (
                round((image["x"] - box["x"]) * scale),
                round((image["y"] - box["y"]) * scale),
                round((image["x"] + image["width"] - box["x"]) * scale),
                round((image["y"] + image["height"] - box["y"]) * scale),
            )
        )
        # Both images are RGB, so every sampled pixel has exactly three channels.
        samples = cast(list[Pixel], list(area.get_flattened_data()))
        canvas = min(samples, key=lambda found: _apart(found, expected))
        assert canvas == expected, (canvas, expected)
    across = [pixel(edge["x"] + step / scale, edge["y"]) for step in range(-6, 7)]
    if image:
        color = ImageColor.getrgb(state["frame_stroke"])
        assert len(color) == 3
        expected = (color[0], color[1], color[2])
        # A dark page can be darker than the SVG's fixed ink. Select actual ink,
        # never an outer background pixel, and require an exact rendered match.
        ink = min(across, key=lambda found: _apart(found, expected))
        assert ink == expected, (ink, expected)
    else:
        ink = max(across, key=lambda found: _apart(found, canvas))
    return Painted(state, ink, ground, canvas)


def _readings(page: Any, hero_address: str) -> dict[str, Painted]:
    """The cell at rest and in each washed state, then the hero's link at rest and under
    the pointer. The press is last and is never released, so nothing is followed."""
    page.locator("[data-atlas-grid]").scroll_into_view_if_needed()
    cell = page.locator(CELL)
    cell.wait_for()
    cell.scroll_into_view_if_needed()
    page.mouse.move(*AWAY)
    found = {"rest": _read(page, CELL)}
    cell.hover()
    found["hover"] = _read(page, CELL)
    page.mouse.move(*AWAY)
    page.locator(BEFORE).focus()
    page.keyboard.press("Tab")
    found["focus"] = _read(page, CELL)
    atlas_address = page.url
    page.goto(hero_address, wait_until="load")
    check_site_rendering.wait_for_fonts(page)
    hero = page.locator(HERO)
    hero.scroll_into_view_if_needed()
    page.mouse.move(*AWAY)
    found["hero rest"] = _read(page, HERO)
    hero.hover()
    found["hero hover"] = _read(page, HERO)
    page.goto(atlas_address, wait_until="load")
    check_site_rendering.wait_for_fonts(page)
    cell.scroll_into_view_if_needed()
    cell.hover()
    page.mouse.down()
    found["pressed"] = _read(page, CELL)
    return found


@pytest.fixture(scope="module")
def painted(tmp_path_factory: pytest.TempPathFactory) -> Iterator[Readings]:
    """Every reading of the overview's drawings, by theme and then by state."""
    root = Path(tmp_path_factory.mktemp("site"))
    site_renders.write(root, "index.html", "atlas.html")
    server = preview_site.serve(root, 0)
    try:
        with site_browser.api().sync_playwright() as driver:
            browser = site_browser.launch(driver)
            found: Readings = {}
            try:
                for scheme in SCHEMES:
                    page = browser.new_page(
                        viewport={"width": 1280, "height": 900},
                        device_scale_factor=2,
                        color_scheme=scheme,
                    )
                    response = page.goto(
                        f"http://127.0.0.1:{server.server_port}/atlas.html?atlas=grid",
                        wait_until="load",
                    )
                    assert response is not None
                    assert response.ok
                    assert (
                        page.locator("html").get_attribute("data-kpress-resolved-theme")
                        == scheme
                    )
                    check_site_rendering.wait_for_fonts(page)
                    found[scheme] = _readings(
                        page, f"http://127.0.0.1:{server.server_port}/index.html"
                    )
                    page.close()
            finally:
                browser.close()
        yield found
    finally:
        server.shutdown()
        server.server_close()


@pytest.mark.parametrize("scheme", SCHEMES)
def test_a_cell_at_rest_is_drawn_in_its_fixed_ink_on_its_white_canvas(
    painted: Readings, scheme: str
) -> None:
    """The cached SVG uses its declared dark ink and white canvas in both page themes;
    the cell itself has no wash until input, and every drawing line reads."""
    rest = painted[scheme]["rest"]
    assert rest.state["background"] == "rgba(0, 0, 0, 0)"
    assert not any(rest.state[name] for name in ("hover", "focus_visible", "active"))
    assert rest.state["frame_stroke"] == rest.state["outline_stroke"] == "rgb(23, 32, 42)"
    assert rest.state["frame_fill"] == "rgb(255, 255, 255)"
    assert rest.canvas == (255, 255, 255)
    assert _apart(rest.ink, rest.canvas) > READABLE, rest


@pytest.mark.parametrize("state", WASHED)
@pytest.mark.parametrize("scheme", SCHEMES)
def test_a_washed_cell_changes_its_background_and_keeps_every_line(
    painted: Readings, scheme: str, state: str
) -> None:
    """Under the pointer, on keyboard focus and while pressed, the cell's background is
    the wash and the drawing is stroked exactly as at rest: the same computed stroke on
    the frame and on the outlines, and the same pixel on the frame's edge."""
    rest, washed = painted[scheme]["rest"], painted[scheme][state]
    assert {name: washed.state[name] for name in WASHED[state]} == WASHED[state]
    assert washed.state["background"] != rest.state["background"]
    assert washed.ground != rest.ground
    assert washed.state["frame_stroke"] == rest.state["frame_stroke"]
    assert washed.state["outline_stroke"] == rest.state["outline_stroke"]
    assert washed.ink == rest.ink, (washed.ink, rest.ink)
    assert washed.canvas == rest.canvas
    assert _apart(washed.ink, washed.canvas) > READABLE, washed


@pytest.mark.parametrize("scheme", SCHEMES)
def test_the_homepage_picture_keeps_its_ink_under_the_pointer(
    painted: Readings, scheme: str
) -> None:
    """The hero is the same drawing in a link, with no wash: hovered, its strokes and the
    pixel on its frame's edge are what they are at rest."""
    rest, over = painted[scheme]["hero rest"], painted[scheme]["hero hover"]
    assert over.state["hover"]
    assert not rest.state["hover"]
    assert over.state["frame_stroke"] == rest.state["frame_stroke"] == rest.state["color"]
    assert over.state["outline_stroke"] == rest.state["outline_stroke"]
    assert over.ink == rest.ink, (over.ink, rest.ink)


@pytest.mark.parametrize("scheme", SCHEMES)
def test_cached_svg_loads_the_complete_declared_artwork(painted: Readings, scheme: str) -> None:
    state = painted[scheme]["rest"].state
    assert state["source_url"].endswith("/atlas/house/n-11.svg")
    assert state["namespace"] == "http://www.w3.org/2000/svg"
    assert state["square_count"] == CASE
    assert state["path_count"] > 0
    assert state["natural_width"] == state["natural_height"] == 1000
    assert state["frame"] == {"x": 0, "y": 0, "width": 1000, "height": 1000}
    assert state["viewbox"] == {"x": -10, "y": -10, "width": 1020, "height": 1020}
    assert painted[scheme]["hero rest"].state["square_count"] == 53


@pytest.mark.parametrize(
    ("source", "refusal"),
    [
        ("missing.svg", "drawing image did not decode"),
        ("drawings/", "drawing image did not decode"),
        ("not-svg.png", "not successful SVG artwork"),
    ],
)
def test_drawing_probe_refuses_missing_and_non_svg_assets(
    tmp_path: Path, source: str, refusal: str
) -> None:
    (tmp_path / "index.html").write_text(
        f'<a id="drawing"><img src="{source}" width="100" height="100"></a>'
    )
    (tmp_path / "drawings").mkdir()
    (tmp_path / "not-svg.png").write_bytes(
        (render_overview.BROWSER / "favicon-48.png").read_bytes()
    )
    server = preview_site.serve(tmp_path, 0)
    try:
        with site_browser.api().sync_playwright() as driver:
            browser = site_browser.launch(driver)
            try:
                page = browser.new_page()
                page.goto(
                    f"http://127.0.0.1:{server.server_port}/index.html", wait_until="load"
                )
                with pytest.raises(site_browser.api().Error, match=refusal):
                    page.evaluate(DRAWING, {"holder": "#drawing"})
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()
