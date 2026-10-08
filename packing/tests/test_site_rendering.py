"""The pre-navigation observer catches an early shift and static missing content."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from kpress.format.markdown import parse_markdown

from devtools import check_site_rendering, preview_site, render_overview, site_assets
from sqpack.probes import applied, probe
from tests import site_browser

if TYPE_CHECKING:
    from playwright.sync_api import Browser

_SHIFT = applied(probe(Path(__file__).parent / "probes", "site_rendering/shift"))


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
            check_site_rendering.install_observer(context)
            context.add_init_script(_SHIFT)
            shifted = context.new_page()
            shifted.goto(url, wait_until="load")
            shifted.wait_for_timeout(450)
            bad = check_site_rendering.read_report(shifted)
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


def test_prepared_record_math_matches_the_surrounding_sans_face(
    browser: Browser, tmp_path: Path
) -> None:
    fragment = parse_markdown("Visible $x^2$ mathematics.", title="Font consistency").html
    body = (
        '<main><h1>Font consistency</h1><div class="site-result">'
        f'{fragment}<div data-math-face="serif">{fragment}</div></div>'
        f'<div class="site-case-bound">{fragment}</div></main>'
    )
    page = render_overview.static_content_page(
        body,
        meta=render_overview.PageMeta(
            "Font consistency",
            "Prepared math matches each surrounding text face.",
            "index.html",
        ),
        current="frontier",
    )
    render_overview.write_site(tmp_path, [page])
    site_assets.write_assets(tmp_path, site_assets.shared().assets.files())
    server = preview_site.serve(tmp_path, 0)
    context = browser.new_context(java_script_enabled=False)
    try:
        view = context.new_page()
        view.goto(f"http://127.0.0.1:{server.server_port}/index.html", wait_until="load")
        check_site_rendering.wait_for_fonts(view)
        readings = view.evaluate(
            probe(Path(__file__).parent / "probes", "site_rendering/math_profile"),
            ".kpress-math-render",
        )
        assert [row["profile"] for row in readings] == ["sans", "prose", "sans"]
        for row in (readings[0], readings[2]):
            assert "Source Sans" in row["surroundingFont"]
            assert "Sans" in row["glyphFont"]
        assert "Sans" not in readings[1]["glyphFont"]
    finally:
        context.close()
        server.shutdown()
        server.server_close()


@pytest.mark.parametrize("hidden", ["main", "h1", "math"])
def test_static_readability_refuses_hidden_primary_content(
    browser: Browser, tmp_path: Path, hidden: str
) -> None:
    style = ' style="display:none"'
    page = tmp_path / "index.html"
    page.write_text(
        f"<main{style if hidden == 'main' else ''}>"
        f"<h1{style if hidden == 'h1' else ''}>The visible page title</h1>"
        "<p>A complete paragraph is visible from the start, "
        "even when scripting is disabled.</p>"
        f'<span class="kpress-math"{style if hidden == "math" else ""}>'
        '<span class="katex-html">x</span></span></main>'
    )
    server = preview_site.serve(tmp_path, 0)
    try:
        report = check_site_rendering.measure(
            browser,
            f"http://127.0.0.1:{server.server_port}/index.html",
            width=390,
            scheme="light",
            javascript=False,
        )
        assert check_site_rendering.problems(report, javascript=False)
    finally:
        server.shutdown()
        server.server_close()
