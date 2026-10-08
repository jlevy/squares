"""The pre-navigation observer catches an early shift and static missing content."""

from __future__ import annotations

import re
from collections.abc import Iterator
from pathlib import Path
from typing import TYPE_CHECKING, Any
from urllib.parse import urlsplit

import pytest
from kpress.format.markdown import parse_markdown

from devtools import check_site_rendering, preview_site, render_overview, site_assets
from sqpack.probes import applied, probe
from tests import site_browser

if TYPE_CHECKING:
    from playwright.sync_api import Browser, Page, Route

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
        '<!doctype html><html><body style="margin:0"><main>'
        '<h1>Static content</h1><p style="font-size:40px">A readable paragraph whose '
        "movement is large enough "
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
            sources = [source for shift in bad["layoutShifts"] for source in shift["sources"]]
            moved = next(
                (source for source in sources if source["node"] == "html > body"), None
            )
            assert moved is not None, sources
            # Chromium attributes this inserted gap to the body's changed box.
            assert moved["currentRect"]["height"] - moved["previousRect"]["height"] >= 500
            assert moved["previousRect"]["width"] > 0
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


@pytest.mark.parametrize("override", [False, True], ids=["hidden", "visible-override"])
def test_generic_hidden_math_wrapper_remains_in_the_readability_sample(
    browser: Browser, tmp_path: Path, *, override: bool
) -> None:
    style = ' style="display:block"' if override else ""
    (tmp_path / "index.html").write_text(
        "<main><h1>A visible page title</h1><p>A complete paragraph remains visible "
        "and readable while the formula's wrapper is checked separately.</p>"
        f'<p hidden{style}><span class="kpress-math">'
        '<span class="katex-html">x</span></span></p></main>'
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
        assert report["shownMath"] == 1
        assert report["unreadableMath"] == (0 if override else 1)
        found = check_site_rendering.problems(report, javascript=False)
        assert found == ([] if override else ["visual mathematics missing"])
    finally:
        server.shutdown()
        server.server_close()


@pytest.mark.parametrize(
    ("opening", "closing"),
    [
        ('<div class="site-atlas-rest" data-atlas-rest hidden>', "</div>"),
        ('<table class="site-table"><tbody><tr hidden><td>', "</td></tr></tbody></table>"),
        ('<div class="site-table-tools" hidden>', "</div>"),
        ('<div class="site-table-tools"><label hidden>', "</label></div>"),
        ('<div class="cert-figure" data-cert="alternate" hidden>', "</div>"),
    ],
    ids=["atlas-rest", "filtered-row", "filter-tools", "preset-control", "certificate"],
)
@pytest.mark.parametrize("override", [False, True], ids=["collapsed", "visible-override"])
def test_optional_hidden_math_is_exempt_only_while_its_wrapper_is_collapsed(
    browser: Browser,
    tmp_path: Path,
    opening: str,
    closing: str,
    *,
    override: bool,
) -> None:
    if override:
        opening = opening.replace(" hidden", ' hidden style="display:block"')
    (tmp_path / "index.html").write_text(
        "<main><h1>A visible page title</h1><p>A complete paragraph remains visible "
        "and readable while optional interface content is checked separately.</p>"
        f'{opening}<span class="kpress-math">x</span>{closing}</main>'
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
        assert report["shownMath"] == (1 if override else 0)
        assert report["unreadableMath"] == (1 if override else 0)
        found = check_site_rendering.problems(report, javascript=False)
        assert found == (["visual mathematics missing"] if override else [])
    finally:
        server.shutdown()
        server.server_close()


@pytest.mark.parametrize(
    ("opening", "closing"),
    [
        ("<div popover>", "</div>"),
        ("<details><summary>More formulas</summary>", "</details>"),
    ],
    ids=["closed-popover", "closed-details"],
)
def test_native_closed_optional_math_is_outside_the_initial_readability_sample(
    browser: Browser, tmp_path: Path, opening: str, closing: str
) -> None:
    (tmp_path / "index.html").write_text(
        "<main><h1>A visible page title</h1><p>A complete paragraph remains visible "
        "and readable before the reader opens optional interface content.</p>"
        f'{opening}<span class="kpress-math">x</span>{closing}</main>'
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
        assert report["shownMath"] == 0
        assert report["unreadableMath"] == 0
        assert not check_site_rendering.problems(report, javascript=False)
    finally:
        server.shutdown()
        server.server_close()


@pytest.fixture(scope="module")
def results_font_site(tmp_path_factory: pytest.TempPathFactory) -> Iterator[str]:
    """One actual results page and its asset closure, without other producer trees."""
    from devtools.render_frontier_page import packing_svg  # noqa: PLC0415

    root = tmp_path_factory.mktemp("results-font-layout")
    rendered = render_overview.results_page()
    (root / rendered.name).write_text(rendered.html, encoding="utf-8")
    assets = render_overview.asset_files([rendered])
    assert sum(map(len, assets.values())) + len(rendered.html.encode()) < 3 * 1024 * 1024
    site_assets.write_assets(root, assets)
    icon = packing_svg(11, units=200, ink="#17202a", paper="#ffffff", frame_px=48)
    (root / "favicon.svg").write_text(
        icon.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
    )
    for name in render_overview.FAVICON_FILES[1:]:
        (root / name).write_bytes((render_overview.BROWSER / name).read_bytes())
    server = preview_site.serve(root, 0, as_pages=True)
    try:
        yield f"http://127.0.0.1:{server.server_port}/{rendered.name}"
    finally:
        server.shutdown()
        server.server_close()


def _prose_font_reading(page: Page) -> tuple[list[dict[str, float]], list[dict[str, Any]]]:
    """Actual opening-paragraph boxes and Chromium's font attribution, not CSS names."""
    paragraphs = page.locator(".site-page > p")
    boxes = []
    for paragraph in paragraphs.all()[:3]:
        box = paragraph.bounding_box()
        assert box is not None
        boxes.append(dict(box))
    assert len(boxes) == 3
    session = page.context.new_cdp_session(page)
    try:
        session.send("DOM.enable")
        session.send("CSS.enable")
        document = session.send("DOM.getDocument")
        selected = session.send(
            "DOM.querySelector",
            {"nodeId": document["root"]["nodeId"], "selector": ".site-page > p"},
        )
        fonts = session.send("CSS.getPlatformFontsForNode", {"nodeId": selected["nodeId"]})
        return boxes, fonts["fonts"]
    finally:
        session.detach()


@pytest.mark.parametrize("fallback", ["platform", "times", "unadjusted"])
def test_results_prose_font_arrival_retains_layout(
    browser: Browser, results_font_site: str, fallback: str
) -> None:
    # The reference is the same real page with its final font, so a fallback fix
    # cannot quietly change the published paragraph geometry or typeface.
    reference = browser.new_context(viewport={"width": 390, "height": 900})
    try:
        view = reference.new_page()
        view.goto(results_font_site, wait_until="load")
        check_site_rendering.wait_for_fonts(view)
        view.wait_for_timeout(check_site_rendering.SETTLE_MS)
        expected, _ = _prose_font_reading(view)
    finally:
        reference.close()

    context = browser.new_context(viewport={"width": 390, "height": 900})
    held: list[Route] = []
    try:
        check_site_rendering.install_observer(context)

        def hold_font(route: Route) -> None:
            held.append(route)

        context.route("**/assets/fonts/pt-serif-latin-400-normal.*.woff2", hold_font)
        if fallback != "platform":

            def select_fallback(route: Route) -> None:
                response = route.fetch()
                css = re.sub(r'"Site Prose Georgia"\s*,\s*', "", response.text())
                if fallback == "unadjusted":
                    css = re.sub(r'"Site Prose Times"\s*,\s*', "", css)
                route.fulfill(response=response, body=css)

            context.route("**/assets/css/site.*.css", select_fallback)
        page = context.new_page()
        page.goto(results_font_site, wait_until="domcontentloaded")
        page.wait_for_timeout(check_site_rendering.SETTLE_MS)
        assert len(held) == 1
        _, temporary = _prose_font_reading(page)
        assert any(
            any(
                name in face["postScriptName"]
                for name in ("Georgia", "TimesNewRoman", "LiberationSerif")
            )
            for face in temporary
        )
        assert not any(face["postScriptName"] == "PTSerif-Regular" for face in temporary)
        if fallback == "times":
            assert all(face["familyName"] != "Georgia" for face in temporary)
        for request in held:
            request.continue_()
        page.wait_for_load_state("load")
        check_site_rendering.wait_for_fonts(page)
        page.wait_for_timeout(check_site_rendering.SETTLE_MS)
        actual, final = _prose_font_reading(page)
        assert any(
            face["postScriptName"] == "PTSerif-Regular" and face["isCustomFont"]
            for face in final
        )
        for before, after in zip(expected, actual, strict=True):
            assert after == pytest.approx(before, abs=0.04)
        report = check_site_rendering.read_report(page)
        assert report["shownMath"] > 0
        assert report["unreadableMath"] == 0
        assert report["supported"], report
        assert report["lcpMs"] > 0, report
        # Holding a font, substituting CSS and inspecting fonts through CDP is
        # not the production load protocol. Keep readability and native CLS here;
        # The production CLI enforces LCP, task and blocking budgets on normal loads.
        assert not check_site_rendering.problems(report, javascript=False), report
        if fallback == "unadjusted":
            # The original fallback is a real negative control: exposing a
            # first paint before PT Serif arrives must still trip the .1 guard.
            assert report["cls"] > check_site_rendering.CLS_LIMIT, report
        else:
            assert report["cls"] <= check_site_rendering.CLS_LIMIT, report
    finally:
        context.close()


@pytest.mark.parametrize(
    ("prose", "fonts"),
    [("serif", "custom"), ("sans", "custom"), ("serif", "system"), ("sans", "system")],
)
def test_results_prose_fallback_preserves_reader_choices(
    browser: Browser, results_font_site: str, prose: str, fonts: str
) -> None:
    parsed = urlsplit(results_font_site)
    origin = f"{parsed.scheme}://{parsed.netloc}"
    context = browser.new_context(
        viewport={"width": 390, "height": 900},
        storage_state={
            "cookies": [],
            "origins": [
                {
                    "origin": origin,
                    "localStorage": [
                        {"name": "kpress.proseFont", "value": prose},
                        {"name": "kpress.fontSet", "value": fonts},
                    ],
                }
            ],
        },
    )
    try:
        page = context.new_page()
        page.goto(results_font_site, wait_until="load")
        check_site_rendering.wait_for_fonts(page)
        _, used = _prose_font_reading(page)
        if fonts == "system":
            assert all(not face["isCustomFont"] for face in used), used
        elif prose == "sans":
            assert all("SourceSans" in face["postScriptName"] for face in used), used
        else:
            assert any(face["postScriptName"] == "PTSerif-Regular" for face in used), used
        assert check_site_rendering.read_report(page)["unreadableMath"] == 0
    finally:
        context.close()
