"""The pre-navigation observer catches an early shift and static missing content."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from devtools import check_site_rendering, preview_site
from sqpack.probes import applied, probe
from tests import site_browser

if TYPE_CHECKING:
    from playwright.sync_api import Browser

_SHIFT = applied(probe(Path(__file__).parent / "probes", "site_rendering_shift"))


@pytest.fixture(scope="module")
def browser() -> Iterator[Browser]:
    with site_browser.api().sync_playwright() as playwright:
        driver = site_browser.launch(playwright)
        yield driver
        driver.close()


def test_early_shift_is_measured_and_missing_static_math_fails(
    browser: Browser, tmp_path: Path
) -> None:
    page = tmp_path / "index.html"
    page.write_text(
        '<!doctype html><html><body style="margin:0"><main><h1>Static content</h1>'
        '<p style="font-size:40px">A readable paragraph whose movement is large enough '
        "to fail the declared layout budget.</p></main></body></html>"
    )
    server = preview_site.serve(tmp_path, 0)
    url = f"http://127.0.0.1:{server.server_port}/index.html"
    try:
        good = check_site_rendering.measure(browser, url, width=390, scheme="light")
        assert not check_site_rendering.problems(good)
        context = browser.new_context(viewport={"width": 390, "height": 900})
        try:
            context.add_init_script(check_site_rendering.INSTRUMENT)
            context.add_init_script(_SHIFT)
            shifted = context.new_page()
            shifted.goto(url, wait_until="load")
            shifted.wait_for_timeout(450)
            bad = shifted.evaluate(check_site_rendering.REPORT)
            assert bad["cls"] > check_site_rendering.CLS_LIMIT
            assert any(
                problem.startswith("cls ") for problem in check_site_rendering.problems(bad)
            )
        finally:
            context.close()
        page.write_text(
            "<!doctype html><main><h1>Missing math</h1><p>A readable paragraph "
            "with an equation absent until a browser script runs.</p>"
            '<span class="kpress-math">x^2</span></main>'
        )
        static = check_site_rendering.measure(
            browser, url, width=390, scheme="light", javascript=False
        )
        assert "visual mathematics missing" in check_site_rendering.problems(
            static, javascript=False
        )
    finally:
        server.shutdown()
        server.server_close()
