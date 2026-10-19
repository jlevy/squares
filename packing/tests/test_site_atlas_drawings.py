"""Both atlas surfaces compare policy-selected drawings with the current originals."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

from devtools import preview_site, render_frontier_page
from sqpack.probes import probe
from tests import site_browser, site_renders

STATE = probe(Path(__file__).parent / "probes", "site_atlas_drawings/state")


@pytest.fixture(scope="module")
def site(tmp_path_factory: pytest.TempPathFactory) -> Iterator[str]:
    root = tmp_path_factory.mktemp("drawing-choice")
    site_renders.write(root, "index.html", "atlas.html")
    server = preview_site.serve(root, 0)
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()


@pytest.fixture(scope="module")
def browser() -> Iterator[Any]:
    with site_browser.api().sync_playwright() as driver:
        instance = site_browser.launch(driver)
        yield instance
        instance.close()


@pytest.mark.parametrize("name", ["index.html", "atlas.html"])
def test_original_round_trip_preserves_tiles_and_uses_current_house_drawings(
    browser: Any, site: str, name: str
) -> None:
    page = browser.new_page(viewport={"width": 1280, "height": 900}, reduced_motion="reduce")
    try:
        page.goto(f"{site}/{name}?size=large&scale=row", wait_until="load")
        before = page.evaluate(STATE)
        assert before["mode"] == "regularized"
        assert [tab["label"] for tab in before["tabs"]] == ["Regularized", "Original"]
        assert [tab["selected"] for tab in before["tabs"]] == ["true", "false"]
        assert len(before["tiles"]) == 324
        regularized = render_frontier_page.drawn_regularized()
        for tile in before["tiles"]:
            assert tile["src"] == render_frontier_page.drawing_path(
                tile["n"], regularized=tile["n"] in regularized
            )
        image = page.locator('[data-atlas-n="88"] img')
        image.scroll_into_view_if_needed()
        regularized_pixels = image.screenshot()
        assert "Regularized" in image.get_attribute("alt")
        assert "Daniel" in image.get_attribute("title")
        address = page.url
        page.get_by_role("tab", name="Original", exact=True).click()
        original = page.evaluate(STATE)
        assert original["mode"] == "original"
        assert page.url == address
        assert [tile["href"] for tile in original["tiles"]] == [
            tile["href"] for tile in before["tiles"]
        ]
        for tile in original["tiles"]:
            assert tile["src"] == render_frontier_page.drawing_path(tile["n"])
            assert tile["alt"].startswith("Original packing")
            assert "Regularized by" not in tile["title"]
        image.scroll_into_view_if_needed()
        assert image.screenshot() != regularized_pixels
        assert (
            page.request.get(f"{site}/{image.get_attribute('src')}").body()
            == (render_frontier_page.drawing_files()["atlas/house/n-88.svg"])
        )
        # The hidden suffix must already have the chosen source when it is expanded.
        page.locator("[data-atlas-toggle]").click()
        later = page.locator('[data-atlas-n="180"] img')
        later.scroll_into_view_if_needed()
        assert later.get_attribute("src") == "atlas/house/n-180.svg"
        page.get_by_role("tab", name="Regularized", exact=True).click()
        after = page.evaluate(STATE)
        assert after["mode"] == "regularized"
        assert [tile["src"] for tile in after["tiles"]] == [
            tile["src"] for tile in before["tiles"]
        ]
        assert [tile["side"] for tile in after["tiles"]] == [
            tile["side"] for tile in before["tiles"]
        ]
        assert len({tile["number_color"] for tile in after["tiles"]}) == 1
        assert after["tiles"][69]["src"] == "atlas/house/n-70.svg"
        assert after["tiles"][69]["alt"].startswith("Original packing")
        # Repeated changes can overtake pending decodes, including a return to the
        # same URL. Only the active generation may mark an image prepared.
        for label in ("Original", "Regularized", "Original", "Regularized"):
            page.get_by_role("tab", name=label, exact=True).click()
        page.locator('[data-atlas-images-ready="324"]').wait_for(state="attached")
        assert page.locator('img[data-atlas-image-state="failed"]').count() == 0
        page.get_by_role("tab", name="Original", exact=True).click()
        page.reload(wait_until="load")
        assert page.evaluate(STATE)["mode"] == "regularized"
    finally:
        page.close()


@pytest.mark.parametrize("name", ["index.html", "atlas.html"])
def test_drawing_chooser_keyboard_and_unscripted_default(
    browser: Any, site: str, name: str
) -> None:
    context = browser.new_context(java_script_enabled=False)
    try:
        page = context.new_page()
        page.goto(f"{site}/{name}", wait_until="load")
        assert page.locator('[data-atlas-n="88"] img').get_attribute("src") == (
            "atlas/regularized/n-88.svg"
        )
        assert not page.locator("[data-atlas-drawings]").is_visible()
    finally:
        context.close()
    page = browser.new_page(reduced_motion="reduce")
    try:
        page.goto(f"{site}/{name}", wait_until="load")
        page.get_by_role("tab", name="Regularized", exact=True).focus()
        for key, selected in (("ArrowRight", 1), ("Home", 0), ("End", 1), ("ArrowRight", 0)):
            page.keyboard.press(key)
            state = page.evaluate(STATE)
            assert state["tabs"][selected]["selected"] == "true"
            assert state["tabs"][selected]["focused"]
            assert state["tabs"][selected]["tabindex"] == "0"
            assert state["tabs"][1 - selected]["tabindex"] == "-1"
            assert page.locator(f"#{state['tabs'][selected]['controls']}").count() == 1
            panel = page.locator(f"#{state['tabs'][selected]['controls']}")
            assert f"atlas-drawing-{'original' if selected else 'regularized'}" in (
                panel.get_attribute("aria-labelledby").split()
            )
    finally:
        page.close()
