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
    from playwright.sync_api import Browser, CDPSession, Page, Route

_SHIFT = applied(probe(Path(__file__).parent / "probes", "site_rendering/shift"))
_FONT_INITIATORS = probe(Path(__file__).parent / "probes", "site_rendering/font_initiators")
_LOCAL_FACE = probe(Path(__file__).parent / "probes", "site_rendering/local_face")


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


def test_frontier_preloads_every_pt_serif_face_it_draws(
    browser: Browser, frontier_native_site: str
) -> None:
    """Italic and bold are first-screen text: the opening paragraphs set both.

    A face left to the layout that discovers it is requested only after that layout,
    so it arrives after the first paint, and the visible paragraph around its
    invisible run rewraps when it does. The hosted runner measured that as CLS 0.134
    and 0.209 at 1280px (frontier.html), above the unchanged 0.1 limit."""
    context = browser.new_context(viewport={"width": 1280, "height": 900})
    try:
        page = context.new_page()
        page.goto(frontier_native_site, wait_until="load")
        check_site_rendering.wait_for_fonts(page)
        fetched = page.evaluate(_FONT_INITIATORS)
    finally:
        context.close()
    serif = {
        re.sub(r"\.[0-9a-f]{16}\.woff2$", ".woff2", row["file"]): row["initiator"]
        for row in fetched
        if row["file"].startswith("pt-serif-")
    }
    assert {
        "pt-serif-latin-400-normal.woff2",
        "pt-serif-latin-400-italic.woff2",
        "pt-serif-latin-700-normal.woff2",
    } <= set(serif), fetched
    assert set(serif) <= set(site_assets.PRELOADED_FACES), fetched
    assert set(serif.values()) == {"link"}, fetched


def _navigation_reading(page: Page) -> tuple[list[dict[str, float]], list[dict[str, Any]]]:
    """The bar's link boxes and the faces Chromium actually draws their labels in."""
    boxes = []
    for link in page.locator(".site-nav-inner > a").all():
        box = link.bounding_box()
        assert box is not None
        boxes.append(dict(box))
    assert len(boxes) > 3
    session = page.context.new_cdp_session(page)
    try:
        session.send("DOM.enable")
        session.send("CSS.enable")
        document = session.send("DOM.getDocument")
        links = session.send(
            "DOM.querySelectorAll",
            {"nodeId": document["root"]["nodeId"], "selector": ".site-nav-inner > a"},
        )
        fonts = [
            face
            for node in links["nodeIds"]
            for face in session.send("CSS.getPlatformFontsForNode", {"nodeId": node})["fonts"]
        ]
        return boxes, fonts
    finally:
        session.detach()


def _unresolved_sans_alias_sources(browser: Browser) -> list[str]:
    """Each `src` of `paper-type.css`'s "Site Sans Arial" faces that names no face the
    browser can load from this machine."""
    css = render_overview.PAPER_TYPE_CSS.read_text(encoding="utf-8")
    sources = re.findall(r'font-family: "Site Sans Arial";\s*src: ([^;]+);', css)
    assert len(sources) == 2, sources
    context = browser.new_context()
    try:
        page = context.new_page()
        return [source for source in sources if not page.evaluate(_LOCAL_FACE, source)]
    finally:
        context.close()


def test_frontier_sans_arrival_keeps_the_navigation_in_place(
    browser: Browser, frontier_native_site: str
) -> None:
    """Source Sans 3 arriving after the first layout moves nothing at 390px.

    Its preload can lose that race, and the face it holds invisible is laid out in the
    next family of the stack. The hosted runner's was DejaVu Sans, about a quarter
    wider: a link wrapped to the bar's second line and the hero's summary took two more
    lines, and the face's arrival measured CLS 0.251 (run 37875117402); this page
    measured 0.232 the same way. The metric-adjusted Arial alias in `paper-type.css`
    (Liberation Sans on Linux) is what stands in now, so every link stays on its line
    and the published bar is unchanged once the face is in."""
    unresolved = _unresolved_sans_alias_sources(browser)
    assert not unresolved, (
        "this machine has neither Arial nor Liberation Sans for the sans alias in "
        f"paper-type.css, so there is no fallback to measure ({unresolved}); install "
        "Liberation Sans (fonts-liberation on Debian and Ubuntu)"
    )
    reference = browser.new_context(viewport={"width": 390, "height": 900})
    try:
        view = reference.new_page()
        view.goto(frontier_native_site, wait_until="load")
        check_site_rendering.wait_for_fonts(view)
        view.wait_for_timeout(check_site_rendering.SETTLE_MS)
        expected, _ = _navigation_reading(view)
    finally:
        reference.close()

    context = browser.new_context(viewport={"width": 390, "height": 900})
    held: list[Route] = []
    try:
        check_site_rendering.install_observer(context)

        def hold_font(route: Route) -> None:
            held.append(route)

        context.route("**/assets/fonts/source-sans-3-latin-wght-normal.*.woff2", hold_font)
        page = context.new_page()
        page.goto(frontier_native_site, wait_until="domcontentloaded")
        page.wait_for_timeout(check_site_rendering.SETTLE_MS)
        assert len(held) == 1
        temporary, standing = _navigation_reading(page)
        assert standing
        assert all(
            any(name in face["postScriptName"] for name in ("Arial", "LiberationSans"))
            for face in standing
        ), standing
        for request in held:
            request.continue_()
        page.wait_for_load_state("load")
        check_site_rendering.wait_for_fonts(page)
        page.wait_for_timeout(check_site_rendering.SETTLE_MS)
        actual, final = _navigation_reading(page)
        assert all(
            "SourceSans3" in face["postScriptName"] and face["isCustomFont"] for face in final
        ), final
        # Once the face is in, the alias draws nothing it covers: the published bar is
        # unchanged.
        for before, after in zip(expected, actual, strict=True):
            assert after == pytest.approx(before, abs=0.04)
        # And every link stood on the line it ends on while the face was held.
        assert [box["y"] for box in temporary] == pytest.approx(
            [box["y"] for box in actual], abs=0.5
        )
        report = check_site_rendering.read_report(page)
        assert report["supported"], report
        assert report["unreadableMath"] == 0
        assert report["cls"] <= check_site_rendering.CLS_LIMIT, report
    finally:
        context.close()


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


#: The paper's own nesting of the diagnostic's declared targets (review B3 on #468): a
#: home link whose words are hidden at 390 px beside its logo, a flex `.doc-links` row of
#: `a.chip` links, and a `.hero` whose title carries nested math and whose credit lines
#: are spans in a `.credits` block. `CSS.getPlatformFontsForNode` asked about those
#: containers found no face for the chips and only the title's words in the hero.
PAPER_NESTING = (
    "<style>@font-face{font-family:PinnedSans;src:url(font.woff2);font-display:swap}"
    "body{font-family:serif;font-size:24px} .doc-links{display:flex}"
    " .chip{display:inline-flex} .site-name-text{display:none}"
    " .site-nav-inner a,.chip,.credits,.katex{font-family:PinnedSans,sans-serif}</style>"
    '<nav class="site-nav-inner"><a class="site-name" href="/" aria-label="Home">'
    '<svg width="20" height="20"></svg><span class="site-name-text">Home</span></a>'
    '<a href="/">Nav link</a></nav>'
    '<div class="doc-links"><a class="chip" href="a.md">MD</a>'
    '<a class="chip" href="a.pdf">PDF</a></div>'
    '<div class="hero"><h1>Title <span class="kpress-math"><span class="katex">'
    '<span class="katex-html"><span class="base"><span class="mord">x</span></span>'
    '</span></span></span></h1><div class="credits"><span>From the original proof by '
    "<strong>Someone</strong></span><span>Agents and a long credit line</span></div></div>"
)


def diagnose_font_fixture(browser: Browser, site: Path, body: str) -> dict[str, Any]:
    """Serve `body` with the pinned Source Sans face beside it, and diagnose it."""
    font = (
        Path(__file__).parents[2]
        / "vendor/kpress/src/kpress/format/static/fonts"
        / "source-sans-3-latin-wght-normal.woff2"
    )
    (site / "font.woff2").write_bytes(font.read_bytes())
    (site / "index.html").write_text(f'<!doctype html><meta charset="utf-8">{body}')
    server = preview_site.serve(site, 0)
    try:
        return check_site_rendering.diagnose_font_delivery(
            browser,
            f"http://127.0.0.1:{server.server_port}/index.html",
            site / "font-diagnostic.json",
            width=390,
            scheme="light",
        )
    finally:
        server.shutdown()
        server.server_close()


def test_font_diagnostic_observes_physical_fallback_then_pinned_face(
    browser: Browser, tmp_path: Path
) -> None:
    result = diagnose_font_fixture(browser, tmp_path, PAPER_NESTING)
    assert result == json.loads((tmp_path / "font-diagnostic.json").read_text())
    assert result["complete"] is True
    assert result["gate_credit"] is False
    assert result["failed_fonts"] == []
    assert len(result["held_fonts"]) == 1
    assert [row["phase"] for row in result["snapshots"]] == ["fonts-held", "fonts-settled"]
    before, after = (row["nodes"] for row in result["snapshots"])
    # What the container reads missed: any face at all for the chips, and the pinned face
    # of the hero's credit lines (their 61 characters) rather than only the title's.
    assert before[2]["fonts"]
    assert after[2]["fonts"]
    assert sum(face["glyphCount"] for face in after[3]["fonts"] if face["isCustomFont"]) > 61
    assert all(row["problems"] == [] for row in result["snapshots"])
    assert [row["selector"] for row in after] == [
        ".site-nav-inner > a",
        ".site-nav-inner > a",
        ".doc-links",
        ".hero",
    ]
    for fallback, custom in zip(before, after, strict=True):
        assert fallback["backendNodeId"] == custom["backendNodeId"]
        assert fallback["html"] == custom["html"]
        assert fallback["complete"] is custom["complete"] is True
        assert fallback["box"]["width"] > 0
        assert custom["box"]["width"] > 0
        assert [text["backendNodeId"] for text in fallback["text"]] == [
            text["backendNodeId"] for text in custom["text"]
        ]
        for row in (fallback, custom):
            assert sum(face["glyphCount"] for face in row["fonts"]) == sum(
                face["glyphCount"] for text in row["text"] for face in text["fonts"]
            )
        for held, settled in zip(fallback["text"], custom["text"], strict=True):
            assert held["typography"] == settled["typography"]
            assert held["fonts"]
            assert settled["fonts"]
            assert not any(face["isCustomFont"] for face in held["fonts"])
            pinned = any(
                face["isCustomFont"] and face["familyName"].startswith("Source Sans")
                for face in settled["fonts"]
            )
            assert pinned is held["typography"]["font-family"].startswith("PinnedSans")
    home, link, documents, hero = after
    # The home link renders only its logo at this width; its words are kept, unrendered.
    assert home["text"] == []
    assert [(text["element"], text["text"]) for text in home["unrendered_text"]] == [
        ("span.site-name-text", "Home")
    ]
    assert [text["text"] for text in link["text"]] == ["Nav link"]
    # The chips' own text, face and family: not the container's serif, and not nothing.
    assert [(text["element"], text["text"]) for text in documents["text"]] == [
        ("a.chip", "MD"),
        ("a.chip", "PDF"),
    ]
    assert documents["typographies"][0]["font-family"] == "PinnedSans, sans-serif"
    assert [
        face["glyphCount"]
        for face in documents["fonts"]
        if face["isCustomFont"] and face["familyName"].startswith("Source Sans")
    ] == [5]
    # The hero's title, its nested math and every credit line.
    assert [(text["element"], text["text"]) for text in hero["text"]] == [
        ("h1", "Title "),
        ("span.mord", "x"),
        ("span", "From the original proof by "),
        ("strong", "Someone"),
        ("span", "Agents and a long credit line"),
    ]
    assert [text["typography"]["font-family"] for text in hero["text"]] == [
        "serif",
        *["PinnedSans, sans-serif"] * 4,
    ]
    # The title, its math at the title's size, the credit lines, and the bold name.
    assert len(hero["typographies"]) == 4


def test_font_diagnostic_fails_a_declared_target_that_renders_no_text(
    browser: Browser, tmp_path: Path
) -> None:
    body = PAPER_NESTING.replace('<a class="chip" href="a.pdf">PDF</a>', "").replace(
        '<a class="chip" href="a.md">', '<a class="chip" href="a.md" style="display:none">'
    )
    with pytest.raises(
        ValueError, match=r"rows are incomplete: .*\.doc-links: renders no text"
    ):
        diagnose_font_fixture(browser, tmp_path, body)
    result = json.loads((tmp_path / "font-diagnostic.json").read_text())
    assert result["complete"] is False
    assert [snapshot["problems"] for snapshot in result["snapshots"]] == [
        [".doc-links: renders no text"],
        [".doc-links: renders no text"],
    ]
    documents = next(
        row for row in result["snapshots"][1]["nodes"] if row["selector"] == ".doc-links"
    )
    assert documents["text"] == []
    assert [text["text"] for text in documents["unrendered_text"]] == ["MD"]


class FacelessSession:
    """A CDP session over a page whose `.doc-links` text shapes with no face."""

    def __init__(self) -> None:
        def element(node: int, name: str, children: list[dict[str, Any]]) -> dict[str, Any]:
            return {
                "nodeId": node,
                "backendNodeId": node,
                "nodeType": 1,
                "nodeName": name.upper(),
                "localName": name,
                "attributes": [],
                "children": children,
            }

        def text(node: int, value: str) -> dict[str, Any]:
            return {"nodeId": node, "backendNodeId": node, "nodeType": 3, "nodeValue": value}

        self.selectors = {".site-nav-inner > a": [3], ".doc-links": [5], ".hero": [7]}
        self.root = element(
            1,
            "body",
            [
                element(2, "nav", [element(3, "a", [text(4, "Nav")])]),
                element(5, "div", [element(10, "span", [text(6, "Formats")])]),
                element(7, "div", [text(8, "Title"), text(9, "\n  ")]),
            ],
        )

    def send(self, method: str, parameters: dict[str, Any] | None = None) -> dict[str, Any]:
        node = (parameters or {}).get("nodeId")
        face = {"familyName": "Sans", "postScriptName": "Sans", "isCustomFont": False}
        replies: dict[str, Callable[[], dict[str, Any]]] = {
            "DOM.getDocument": lambda: {"root": self.root},
            "DOM.querySelectorAll": lambda: {
                "nodeIds": self.selectors[(parameters or {})["selector"]]
            },
            "DOM.getContentQuads": lambda: {"quads": [[0, 0, 1, 0, 1, 1, 0, 1]]},
            "CSS.getComputedStyleForNode": lambda: {
                "computedStyle": [{"name": "font-family", "value": "Sans"}]
            },
            "CSS.getPlatformFontsForNode": lambda: {
                "fonts": [] if node == 6 else [{**face, "glyphCount": 3}]
            },
            "DOM.getOuterHTML": lambda: {"outerHTML": "<div></div>"},
            "DOM.getBoxModel": lambda: {"model": {"width": 1, "height": 1}},
        }
        return replies[method]()


def test_a_rendered_text_without_a_physical_face_marks_its_row_incomplete() -> None:
    rows = check_site_rendering.physical_font_snapshot(cast("CDPSession", FacelessSession()))
    assert [(row["selector"], row["complete"]) for row in rows] == [
        (".site-nav-inner > a", True),
        (".doc-links", False),
        (".hero", True),
    ]
    documents = rows[1]
    assert [(text["element"], text["text"]) for text in documents["text"]] == [
        ("span", "Formats")
    ]
    assert documents["fonts"] == []
    assert documents["problems"] == [
        ".doc-links: span text 'Formats' resolved no physical face"
    ]
    # Collapsible whitespace is not text; the title's face is summed once.
    assert [text["text"] for text in rows[2]["text"]] == ["Title"]
    assert rows[2]["fonts"] == [
        {"familyName": "Sans", "postScriptName": "Sans", "isCustomFont": False, "glyphCount": 3}
    ]
    assert check_site_rendering.snapshot_problems(rows) == documents["problems"]


@pytest.mark.parametrize("failure", ["no-font", "missing-node", "failed-font"])
def test_font_diagnostic_retains_incomplete_native_observations(
    browser: Browser, tmp_path: Path, failure: str
) -> None:
    styles = (
        "<style>@font-face{font-family:MissingFont;src:url(missing.woff2)}"
        "body{font-family:MissingFont,serif}</style>"
        if failure != "no-font"
        else ""
    )
    hero = ' class="hero"' if failure != "missing-node" else ""
    (tmp_path / "index.html").write_text(
        "<!doctype html>"
        + styles
        + '<nav class="site-nav-inner"><a href="/">Navigation text</a></nav>'
        + '<div class="doc-links">Document formats</div>'
        + f"<main{hero}><h1>Readable title</h1><p>This complete paragraph remains "
        + "readable while a native diagnostic rejects an incomplete observation.</p></main>"
    )
    destination = tmp_path / "incomplete.json"
    messages = {
        "no-font": "no held font requests",
        "missing-node": "selector is absent",
        "failed-font": "failed font loads",
    }
    server = preview_site.serve(tmp_path, 0)
    try:
        with pytest.raises(ValueError, match=messages[failure]):
            check_site_rendering.diagnose_font_delivery(
                browser,
                f"http://127.0.0.1:{server.server_port}/index.html",
                destination,
                width=390,
                scheme="light",
            )
    finally:
        server.shutdown()
        server.server_close()
    result = json.loads(destination.read_text())
    assert result["complete"] is False
    assert result["gate_credit"] is False
    assert result["error"]["type"] == "ValueError"
    assert messages[failure] in result["error"]["message"]
    if failure == "failed-font":
        assert result["failed_fonts"]
        assert len(result["snapshots"]) == 2


def test_font_diagnostic_refuses_overwrite_before_context(tmp_path: Path) -> None:
    destination = tmp_path / "retained.json"
    destination.write_text("retained evidence")
    driver = Mock()
    with pytest.raises(FileExistsError):
        check_site_rendering.diagnose_font_delivery(
            driver, "http://localhost/index.html", destination, width=390, scheme="light"
        )
    driver.new_context.assert_not_called()
    assert destination.read_text() == "retained evidence"


def test_font_diagnostic_retains_context_failure(tmp_path: Path) -> None:
    driver = Mock()
    driver.new_context.side_effect = RuntimeError("native context failed")
    destination = tmp_path / "failed-context.json"
    with pytest.raises(RuntimeError, match="native context failed"):
        check_site_rendering.diagnose_font_delivery(
            driver, "http://localhost/index.html", destination, width=390, scheme="light"
        )
    result = json.loads(destination.read_text())
    assert result["complete"] is False
    assert result["error"] == {"type": "RuntimeError", "message": "native context failed"}


def test_font_diagnostic_cli_refuses_receipt_before_launch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "index.html").write_text("<main>Existing page</main>")
    destination = tmp_path / "retained.json"
    destination.write_text("retained evidence")
    launch = Mock()
    monkeypatch.setattr(preview_site, "launch_chromium", launch)
    with pytest.raises(SystemExit) as error:
        check_site_rendering.main(
            [str(tmp_path), "--page", "index.html", "--font-diagnostic", str(destination)]
        )
    assert error.value.code == 2
    launch.assert_not_called()
    assert destination.read_text() == "retained evidence"
