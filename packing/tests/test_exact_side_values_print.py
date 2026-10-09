"""The complete archive refuses clipped print math before writing its PDF."""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from playwright.sync_api import Page, sync_playwright

from devtools.render_exact_side_values import PRINT_CONTENT_WIDTH, PRINT_MATH_FIT
from tests import site_browser


@pytest.fixture
def page() -> Iterator[Page]:
    with sync_playwright() as driver:
        browser = site_browser.launch(driver)
        try:
            yield browser.new_page()
        finally:
            browser.close()


@pytest.mark.parametrize(("formula_width", "overflow_count"), [(220, 0), (380, 1)])
def test_print_preflight_refuses_a_display_beyond_its_column(
    page: Page, formula_width: int, overflow_count: int
) -> None:
    page.emulate_media(media="print")
    page.set_content(
        "<style>.kpress-math-display {width:300px;text-align:center;}"
        ".katex-html,.base {display:inline-block;}"
        f".base {{width:{formula_width}px;}}</style>"
        '<article class="exact-side-values-paper"><div class="kpress-math-display" '
        'data-kpress-math-source="print control"><span class="katex-html">'
        '<span class="base">Complete formula</span></span></div></article>'
    )
    result = page.evaluate(PRINT_MATH_FIT)
    assert result["checked"] == 1
    assert len(result["overflows"]) == overflow_count
    if overflow_count:
        assert result["overflows"][0]["formula_width"] == formula_width
        assert result["overflows"][0]["source"] == "print control"


@pytest.mark.parametrize(("margin", "content_width"), [("1.25in", 576), ("1in", 624)])
def test_print_preflight_uses_the_publication_page_margin(
    page: Page, margin: str, content_width: int
) -> None:
    page.emulate_media(media="print")
    page.set_content(f"<style>:root {{ --kpress-print-page-margin: {margin}; }}</style>")
    assert page.evaluate(PRINT_CONTENT_WIDTH) == content_width
