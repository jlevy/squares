"""The pre-navigation observer catches an early shift and static missing content."""

from __future__ import annotations

import io
import json
import math
import re
from collections.abc import Callable, Iterator
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast
from unittest.mock import Mock
from urllib.parse import urlsplit

import pytest
from kpress.format.markdown import parse_markdown
from PIL import Image

from devtools import check_site_rendering, preview_site, render_overview, site_assets
from sqpack.probes import applied, probe
from tests import site_browser, site_renders

if TYPE_CHECKING:
    from playwright.sync_api import Browser, Page, Route

_SHIFT = applied(probe(Path(__file__).parent / "probes", "site_rendering/shift"))


@pytest.fixture(scope="module")
def frontier_math_counts() -> tuple[int, int]:
    return site_renders.frontier_math_counts()


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
        font_events = report["fontEvents"]
        started = [event["startTime"] for event in font_events if event["type"] == "loading"]
        completed = [
            event["startTime"] for event in font_events if event["type"] == "loadingdone"
        ]
        assert started, font_events
        assert completed, font_events
        assert completed[-1] >= started[-1] > 0, font_events
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


def test_native_trace_retains_full_events_and_marks_diagnostic_overhead(tmp_path: Path) -> None:
    page = Mock()
    page.url = "http://127.0.0.1/papers/n11-threshold-bound-review.html"
    session = page.context.new_cdp_session.return_value
    callbacks: dict[str, Callable[[dict[str, Any]], None]] = {}

    def on(name: str, callback: Callable[[dict[str, Any]], None]) -> None:
        callbacks[name] = callback

    session.on.side_effect = on
    session.send.return_value = {"product": "test Chromium"}
    destination = tmp_path / "native.json"
    stop = check_site_rendering.record_native_trace(cast("Page", page), destination)
    events = [
        {"name": "UpdateLayoutTree", "ph": "X", "dur": 351000, "args": {"data": {"nodeId": 7}}},
        {"name": "Paint", "ph": "X", "dur": 8000, "args": {"frame": "initial"}},
    ]
    callbacks["Tracing.dataCollected"]({"value": events[:1]})
    callbacks["Tracing.dataCollected"]({"value": events[1:]})
    callbacks["Tracing.tracingComplete"]({"dataLossOccurred": False})
    stop()
    payload = json.loads(destination.read_text())
    assert payload["traceEvents"] == events
    assert payload["diagnostic"]["url"] == page.url
    assert payload["diagnostic"]["tracingComplete"] == {"dataLossOccurred": False}
    assert "no gate timing credit" in payload["diagnostic"]["overhead"]
    session.detach.assert_called_once()
    assert check_site_rendering.LONGEST_TASK_LIMIT_MS == 300


def test_native_trace_refuses_to_overwrite_unique_evidence(tmp_path: Path) -> None:
    destination = tmp_path / "native.json"
    destination.write_text("retained actual receipt")
    page = Mock()
    with pytest.raises(FileExistsError, match="already exists"):
        check_site_rendering.record_native_trace(cast("Page", page), destination)
    assert destination.read_text() == "retained actual receipt"
    page.context.new_cdp_session.assert_not_called()


def test_native_trace_detaches_and_refuses_an_incomplete_capture(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    page = Mock()
    session = page.context.new_cdp_session.return_value
    destination = tmp_path / "native.json"
    stop = check_site_rendering.record_native_trace(cast("Page", page), destination)
    times = iter((0, 11))
    monkeypatch.setattr(check_site_rendering.time, "monotonic", lambda: next(times))
    with pytest.raises(TimeoutError, match="did not finish"):
        stop()
    session.detach.assert_called_once()
    assert not destination.exists()


def test_native_trace_summary_reports_inclusive_work_without_changing_events() -> None:
    events = [
        {"name": "Layout", "ph": "X", "dur": 12000},
        {"name": "Layout", "ph": "X", "dur": 4000},
        {"name": "Paint", "ph": "X", "dur": 500},
        {
            "name": "SelectorStats",
            "args": {
                "selector_stats": {
                    "selector_timings": [
                        {
                            "selector": ".actual",
                            "elapsed (us)": 25,
                            "match_attempts": 7,
                            "match_count": 3,
                        }
                    ]
                }
            },
        },
    ]
    preserved = json.dumps(events, sort_keys=True)
    summary = check_site_rendering.native_trace_summary(events)
    assert summary["event_count"] == 4
    assert summary["phases"]["Layout"] == {"count": 2, "inclusive_ms": 16.0, "max_ms": 12.0}
    assert summary["selectors"] == [
        {"selector": ".actual", "elapsed_us": 25, "match_attempts": 7, "match_count": 3}
    ]
    assert "overlap" in summary["interpretation"]
    assert "no gate timing credit" in summary["interpretation"]
    assert json.dumps(events, sort_keys=True) == preserved


@pytest.mark.parametrize(
    ("native", "expected"),
    [
        (
            '<math xmlns="http://www.w3.org/1998/Math/MathML"><mi>x</mi><mo>+</mo><mn>1</mn></math>',
            0,
        ),
        ("wrapper text without math", 1),
        ('<math xmlns="http://www.w3.org/1998/Math/MathML"></math>', 1),
        (
            (
                '<math xmlns="http://www.w3.org/1998/Math/MathML" '
                'style="display:none"><mi>x</mi></math>'
            ),
            1,
        ),
        (
            (
                '<math xmlns="http://www.w3.org/1998/Math/MathML" '
                'style="visibility:hidden"><mi>x</mi></math>'
            ),
            1,
        ),
        (
            (
                '<math xmlns="http://www.w3.org/1998/Math/MathML">'
                '<mi style="visibility:hidden">x</mi></math>'
            ),
            1,
        ),
        ('<span class="katex-html">wrapper fallback</span>', 1),
    ],
    ids=[
        "visible",
        "missing",
        "empty",
        "display-none",
        "hidden",
        "hidden-content",
        "katex-impostor",
    ],
)
def test_native_frontier_readability_requires_visible_nonempty_math(
    browser: Browser,
    tmp_path: Path,
    native: str,
    expected: int,
) -> None:
    (tmp_path / "index.html").write_text(
        "<main><h1>Native frontier math</h1><p>A complete readable paragraph "
        "accompanies a frontier value with its own checked mathematical content.</p>"
        '<table class="site-frontier"><tbody><tr><td>'
        '<span class="kpress-math kpress-math-inline" data-site-native-math="frontier">'
        f"{native}</span></td></tr></tbody></table></main>"
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
        assert report["unreadableMath"] == expected
        assert check_site_rendering.problems(report, javascript=False) == (
            ["visual mathematics missing"] if expected else []
        )
    finally:
        server.shutdown()
        server.server_close()


@pytest.fixture(scope="module")
def frontier_native_site(tmp_path_factory: pytest.TempPathFactory) -> Iterator[str]:
    root = tmp_path_factory.mktemp("frontier-native-layout")
    site_renders.write(root, "frontier.html")
    server = preview_site.serve(root, 0, as_pages=True)
    try:
        yield f"http://127.0.0.1:{server.server_port}/frontier.html"
    finally:
        server.shutdown()
        server.server_close()


@pytest.mark.parametrize(
    ("width", "scheme"), [(390, "light"), (390, "dark"), (1280, "light"), (1280, "dark")]
)
def test_native_frontier_passes_the_unchanged_http_load_and_nojs_budgets(
    browser: Browser,
    frontier_math_counts: tuple[int, int],
    frontier_native_site: str,
    width: int,
    scheme: Any,
) -> None:
    for javascript in (True, False):
        report = check_site_rendering.measure(
            browser,
            frontier_native_site,
            width=width,
            scheme=scheme,
            javascript=javascript,
        )
        assert report["shownMath"] == frontier_math_counts[1]
        assert report["unreadableMath"] == 0
        assert check_site_rendering.problems(report, javascript=javascript) == [], report


@pytest.mark.parametrize(
    ("prose", "fonts"),
    [("serif", "custom"), ("sans", "custom"), ("serif", "system"), ("sans", "system")],
)
def test_frontier_native_math_keeps_actual_reader_and_print_fonts(
    browser: Browser,
    frontier_math_counts: tuple[int, int],
    frontier_native_site: str,
    prose: str,
    fonts: str,
) -> None:
    parsed = urlsplit(frontier_native_site)
    origin = f"{parsed.scheme}://{parsed.netloc}"
    context = browser.new_context(
        viewport={"width": 1280, "height": 900},
        java_script_enabled=True,
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
        page.goto(frontier_native_site, wait_until="load")
        session = context.new_cdp_session(page)
        try:
            session.send("DOM.enable")
            session.send("CSS.enable")
            document = session.send("DOM.getDocument")
            for media in ("screen", "print"):
                page.emulate_media(media=media)
                check_site_rendering.wait_for_fonts(page)
                report = check_site_rendering.read_report(page)
                assert report["shownMath"] == frontier_math_counts[1]
                assert report["unreadableMath"] == 0
                assert (
                    page.locator('.site-frontier [data-site-native-math="frontier"]').count()
                    == frontier_math_counts[0]
                )
                assert page.locator("#frontier-table tbody tr").count() == 324
                nodes = [
                    session.send(
                        "DOM.querySelector",
                        {
                            "nodeId": document["root"]["nodeId"],
                            "selector": selector,
                        },
                    )["nodeId"]
                    for selector in (
                        '.site-frontier [data-site-native-math="frontier"] math mn',
                        '.site-frontier td:has([data-site-native-math="frontier"])',
                        '.site-frontier [data-site-native-math="frontier"] > math',
                    )
                ]
                styles = [
                    session.send("CSS.getComputedStyleForNode", {"nodeId": node})[
                        "computedStyle"
                    ]
                    for node in nodes
                ]
                families = [
                    next(item["value"] for item in style if item["name"] == "font-family")
                    for style in styles
                ]
                assert families[0] == families[1], (prose, fonts, media, families)
                assert families[2] == "math", (prose, fonts, media, families)
                used = session.send("CSS.getPlatformFontsForNode", {"nodeId": nodes[0]})[
                    "fonts"
                ]
                assert used
                if fonts == "system":
                    assert all(not face["isCustomFont"] for face in used), (media, used)
                else:
                    assert any(face["isCustomFont"] for face in used), (media, used)
        finally:
            session.detach()
    finally:
        context.close()


def native_radical_paint(page: Page, screenshot: Path) -> dict[str, int | bool]:
    """Read actual radical hook and overbar ink with its radicand text suppressed.

    Transparent text preserves the real formula's layout and faces, but prevents the
    numeral from passing this painted-construction check. A bar without a hook fails.
    """
    radical = page.locator('#n-5 [data-site-native-math="frontier"] msqrt')
    assert radical.count() == 1
    radicand = radical.locator("mn")
    assert radicand.count() == 1
    box, text_box = radical.bounding_box(), radicand.bounding_box()
    assert box is not None
    assert text_box is not None
    pixels = Image.open(
        io.BytesIO(
            radical.screenshot(
                path=str(screenshot),
                style=(
                    '#n-5 [data-site-native-math="frontier"] msqrt {'
                    "color: #000 !important; background: #fff !important; }"
                    '#n-5 [data-site-native-math="frontier"] msqrt > * {'
                    "color: transparent !important; }"
                ),
            )
        )
    ).convert("RGB")
    scale = pixels.width / box["width"]
    text_left = max(0, min(pixels.width, math.floor((text_box["x"] - box["x"]) * scale)))
    dark = {
        (x, y)
        for y in range(pixels.height)
        for x in range(pixels.width)
        if max(cast("tuple[int, int, int]", pixels.getpixel((x, y)))) < 160
    }
    rows = [
        sum((x, y) in dark for x in range(text_left, pixels.width))
        for y in range(pixels.height)
    ]
    bar_y = max(range(pixels.height), key=rows.__getitem__)
    bar = rows[bar_y] >= max(2, math.ceil((pixels.width - text_left) * 0.6))
    hook = {
        (x, y) for x, y in dark if x < text_left - 1 and y > bar_y + max(2, pixels.height // 8)
    }
    hook_height = max((y for _, y in hook), default=0) - min((y for _, y in hook), default=0)
    return {
        "hook": len(hook) >= 3 and hook_height >= pixels.height * 0.25,
        "bar": bar,
        "hook_pixels": len(hook),
        "bar_pixels": rows[bar_y],
        "hook_height": hook_height,
        "text_left": text_left,
        "width": pixels.width,
        "height": pixels.height,
    }


@pytest.mark.parametrize("media", ["screen", "print"])
def test_frontier_native_radical_paints_hook_and_bar_and_rejects_text_font(
    browser: Browser, frontier_native_site: str, tmp_path: Path, media: Any
) -> None:
    for mutant in (False, True):
        context = browser.new_context(
            viewport={"width": 1280, "height": 900},
            device_scale_factor=2,
            java_script_enabled=False,
        )
        try:
            if mutant:

                def text_font(route: Route) -> None:
                    response = route.fetch()
                    damaged = response.text().replace(
                        "</head>",
                        '<style>.site-frontier [data-site-native-math="frontier"] > math {'
                        "font-family: var(--kpress-font-sans) !important;}</style></head>",
                        1,
                    )
                    route.fulfill(response=response, body=damaged)

                context.route("**/frontier.html", text_font)
            page = context.new_page()
            page.emulate_media(media=media)
            page.goto(frontier_native_site, wait_until="load")
            check_site_rendering.wait_for_fonts(page)
            painted = native_radical_paint(page, tmp_path / f"radical-{media}-{mutant}.png")
            if mutant:
                assert not (painted["hook"] and painted["bar"]), painted
            else:
                assert painted["hook"], painted
                assert painted["bar"], painted
        finally:
            context.close()


@pytest.fixture(scope="module")
def semantic_math_site(tmp_path_factory: pytest.TempPathFactory) -> Iterator[str]:
    """A prepared formula beside native and unrendered MathML, without a site build."""
    root = tmp_path_factory.mktemp("semantic-math")
    fragment = parse_markdown(
        r"Copy $x^2 + \frac{1}{2}$ exactly.", title="Semantic mathematics"
    ).html
    body = (
        '<article class="kpress kpress-doc kpress-prose"><h1>Semantic mathematics</h1>'
        f'<div id="copy-formula">{fragment}</div><div id="fallback-slot"></div>'
        '<div class="site-frontier"><span data-site-native-math="frontier">'
        '<math xmlns="http://www.w3.org/1998/Math/MathML"><mi>n</mi></math>'
        "</span></div></article>"
    )
    page = render_overview.static_content_page(
        body,
        meta=render_overview.PageMeta(
            "Semantic mathematics", "Accessible static mathematical content.", "index.html"
        ),
        current="papers",
    )
    fallback = (
        '<span id="fallback-math" class="kpress-math" data-kpress-math="inline">'
        '<span class="kpress-math-semantic"><math '
        'xmlns="http://www.w3.org/1998/Math/MathML"><mi>z</mi></math></span></span>'
    )
    assert page.html.count('<div id="fallback-slot"></div>') == 1
    output = page.html.replace('<div id="fallback-slot"></div>', fallback)
    (root / "index.html").write_text(output, encoding="utf-8")
    site_assets.write_assets(root, render_overview.asset_files([page]))
    server = preview_site.serve(root, 0)
    try:
        yield f"http://127.0.0.1:{server.server_port}/index.html"
    finally:
        server.shutdown()
        server.server_close()


def semantic_math_state(page: Page, *, javascript: bool) -> dict[str, Any]:
    """Native geometry/accessibility and an intercepted copy, without clipboard writes."""
    copied = page.evaluate(
        probe(Path(__file__).parent / "probes", "site_rendering/math_copy"),
        {"selector": "#copy-formula", "copy": javascript},
    )
    assert copied["mode"] == (
        "native-copy-intercepted" if javascript else "selection-only-nojs"
    )
    assert copied["intercepted"] is javascript
    assert copied["command_succeeded"] is javascript
    assert copied["text"]
    assert "Copy" in copied["text"]
    assert len(copied["mathml"]) == 1
    assert "<msup><mi>x</mi><mn>2</mn></msup>" in copied["mathml"][0]
    assert "<mfrac>" in copied["mathml"][0]
    assert copied["mathml"]
    assert copied["source_html"]
    assert all(
        row["reset"] == row["increment"] == row["set"] == "none"
        and row["before"] in {"none", "normal"}
        and row["after"] in {"none", "normal"}
        for row in copied["semantic_styles"]
    )
    session = page.context.new_cdp_session(page)
    try:
        dom = session.send("DOMSnapshot.captureSnapshot", {"computedStyles": []})
        ax = session.send("Accessibility.getFullAXTree")["nodes"]
    finally:
        session.detach()
    document = dom["documents"][0]["nodes"]
    math_ids = {
        document["backendNodeId"][index]
        for index, name in enumerate(document["nodeName"])
        if dom["strings"][name].lower() == "math"
    }
    nodes = {node["nodeId"]: node for node in ax}

    def subtree(node: dict[str, Any]) -> dict[str, Any]:
        return {key: node.get(key, {}).get("value") for key in ("role", "name", "value")} | {
            "ignored": node.get("ignored"),
            "children": [subtree(nodes[key]) for key in node.get("childIds", [])],
        }

    roots = [node for node in ax if node.get("backendDOMNodeId") in math_ids]
    assert len(math_ids) == len(roots) == 3
    assert not any(node["ignored"] for node in roots)
    boxes = [
        node.bounding_box()
        for node in page.locator(".kpress-math, [data-site-native-math]").all()
    ]
    assert len(boxes) == 3
    assert all(box and box["width"] > 0 and box["height"] > 0 for box in boxes)
    return {"copy": copied, "ax_math": [subtree(node) for node in roots], "boxes": boxes}


@pytest.mark.parametrize("javascript", [True, False])
@pytest.mark.parametrize("width", [390, 1280])
def test_clipped_semantic_math_keeps_print_nojs_accessibility_and_copy(
    browser: Browser, semantic_math_site: str, *, javascript: bool, width: int
) -> None:
    context = browser.new_context(
        viewport={"width": width, "height": 900}, java_script_enabled=javascript
    )
    try:
        page = context.new_page()
        page.goto(semantic_math_site, wait_until="load")
        page.locator("#fallback-math > .kpress-math-semantic").wait_for(state="visible")
        session = context.new_cdp_session(page)
        try:
            session.send("DOM.enable")
            session.send("CSS.enable")

            def containment(selector: str) -> str:
                root = session.send("DOM.getDocument")["root"]["nodeId"]
                node = session.send("DOM.querySelector", {"nodeId": root, "selector": selector})
                styles = session.send("CSS.getComputedStyleForNode", {"nodeId": node["nodeId"]})
                return next(
                    row["value"] for row in styles["computedStyle"] if row["name"] == "contain"
                )

            selector = '.kpress-math[data-kpress-math-rendered="true"] > .kpress-math-semantic'
            frame = session.send("Page.getFrameTree")["frameTree"]["frame"]["id"]
            override = session.send("CSS.createStyleSheet", {"frameId": frame, "force": True})[
                "styleSheetId"
            ]
            for medium in ("screen", "print"):
                page.emulate_media(media=medium)
                check_site_rendering.wait_for_fonts(page)
                assert containment(selector) == "strict"
                assert containment("#fallback-math > .kpress-math-semantic") == "none"
                assert containment('[data-site-native-math="frontier"] > math') == "none"
                original = semantic_math_state(page, javascript=javascript)
                # Inspector styles do not wait for disabled page-script load handlers.
                session.send(
                    "CSS.setStyleSheetText",
                    {
                        "styleSheetId": override,
                        "text": selector + " { contain: none !important; }",
                    },
                )
                try:
                    assert containment(selector) == "none"
                    assert semantic_math_state(page, javascript=javascript) == original
                finally:
                    session.send(
                        "CSS.setStyleSheetText", {"styleSheetId": override, "text": ""}
                    )
                assert containment(selector) == "strict"
                assert semantic_math_state(page, javascript=javascript) == original
        finally:
            session.detach()
    finally:
        context.close()
