"""The shared header's scroll, focus and geometry contract across its four shells."""

from __future__ import annotations

import json
import re
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

from devtools import check_site_rendering, render_overview, site_assets
from devtools.render_n11_lower_bounds_explainer import kpress_css, kpress_static
from sqpack.probes import probe
from tests import site_browser

PROBES = Path(__file__).with_name("probes")
STATE = probe(PROBES, "site_headroom/state")
SCROLL = probe(PROBES, "site_headroom/scroll")
ANCHOR = probe(PROBES, "site_headroom/anchor")
NAVIGATION = probe(PROBES, "site_headroom/navigation")
BODY = (
    "<h1>Header test</h1><p>Scroll to the target.</p>"
    '<div style="height: 1600px"></div><h2 id="header-target">Target</h2>'
    '<div style="height: 1600px"></div>'
)


@pytest.fixture(scope="module")
def browser() -> Iterator[Any]:
    sync_api = site_browser.api()
    with sync_api.sync_playwright() as driver:
        launched = site_browser.launch(driver)
        yield launched
        launched.close()


@pytest.fixture(scope="module")
def shells(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Path]:
    """Minimal documents through the real page builders and each paper's actual shell."""
    from workbench_tools import build_site  # noqa: PLC0415

    root = tmp_path_factory.mktemp("headroom")
    ordinary = render_overview.kpress_page(
        BODY,
        name="header.html",
        current="visualize",
        title="Header test",
        description="Header behavior fixture.",
        toc=False,
        tabs=render_overview.visualize_tabs("film"),
        prepare_math=False,
    )
    static = render_overview.static_content_page(
        BODY,
        meta=render_overview.PageMeta("Header test", "Header fixture.", "header-static.html"),
        current="atlas",
    )
    documents = {
        "ordinary": site_assets.shared().assets.inlined(ordinary.html),
        "static": site_assets.shared().assets.inlined(static.html),
    }
    for paper in (
        "n11-lower-bounds-explainer",
        "n11-optimality-review",
        "n11-threshold-bound-review",
        "packing-methods",
    ):
        template = (render_overview.TEMPLATES / f"{paper}-shell.html").read_text()
        values = {
            "KPRESS_CSS": kpress_css(kpress_static()),
            "SITE_NAV_CSS": render_overview.SITE_NAV_CSS.read_text(),
            "PUBLICATION_CSS": (
                render_overview.TEMPLATES / "paper-publication.css"
            ).read_text(),
            "PAPER_TYPE_CSS": render_overview.PAPER_TYPE_CSS.read_text(),
            "SITE_NAV": render_overview.nav_html("papers"),
            "SITE_THEME": render_overview.THEME_SCRIPT.read_text(),
            "SITE_HEADROOM": render_overview.HEADROOM_SCRIPT.read_text(),
            "BODY_HTML": BODY,
        }
        documents[paper] = re.sub(
            r"\{\{([A-Z_]+)\}\}", lambda m, values=values: values.get(m[1], ""), template
        )
    assets = build_site.WORKBENCH_PACKAGE / "assets"
    workbench = build_site.with_nav((assets / "template.html").read_text())
    documents["workbench"] = (
        workbench.replace("__WORKBENCH_CSS__", (assets / "workbench.css").read_text())
        .replace("__FONT_CSS__", "")
        .replace("__KATEX_CSS__", "")
    )
    paths = {}
    for name, html in documents.items():
        path = root / f"{name}.html"
        path.write_text(html)
        paths[name] = path
    return paths


@pytest.mark.parametrize("width", [1280, 768, 390, 320])
def test_header_hides_down_and_returns_on_first_upward_scroll(
    browser: Any, shells: dict[str, Path], width: int
) -> None:
    for name, path in shells.items():
        if name == "workbench":
            continue
        page = browser.new_page(
            viewport={"width": width, "height": 700}, reduced_motion="reduce"
        )
        try:
            page.goto(path.as_uri(), wait_until="load")
            page.locator(".site-headroom").wait_for(state="attached")
            before = page.evaluate(STATE)
            assert before["enhanced"], name
            assert before["top"] >= 0, name
            assert before["overflow"] == 0, name
            page.evaluate(SCROLL, 600)
            down = page.evaluate(STATE)
            assert down["hidden"], name
            assert down["bottom"] <= 0.5, name
            assert down["targetPosition"] == pytest.approx(before["targetPosition"]), name
            page.evaluate(SCROLL, 597)
            up = page.evaluate(STATE)
            assert not up["hidden"], name
            assert up["top"] == pytest.approx(0, abs=0.5), name
            assert up["targetPosition"] == pytest.approx(before["targetPosition"]), name
            assert up["offset"] >= up["height"], name
            assert up["transition"] == "0s", name
            page.evaluate(SCROLL, 0)
            assert not page.evaluate(STATE)["hidden"], name
            if name == "ordinary":
                assert before["tabsInside"]
        finally:
            page.close()


@pytest.mark.parametrize("width", [1440, 1280, 1239, 768, 390, 320])
def test_gear_aligns_with_the_navigation_labels_visible_ink(
    browser: Any, shells: dict[str, Path], width: int
) -> None:
    for name, path in shells.items():
        page = browser.new_page(viewport={"width": width, "height": 700})
        try:
            page.goto(path.as_uri(), wait_until="load")
            page.locator(".site-headroom").wait_for(state="attached")
            items = page.evaluate(NAVIGATION)
            github = next(item for item in items if item["label"] == "github")
            gear = next(item for item in items if item["label"] == "site-theme")
            assert gear["iconCenter"] == pytest.approx(gear["inkCenter"], abs=0.75), (
                name,
                items,
            )
            # The button can wrap onto its own line at 320px. Its own text baseline
            # still defines the same optical alignment as a label on that line.
            if abs(gear["baseline"] - github["baseline"]) < 0.75:
                assert gear["iconCenter"] == pytest.approx(github["inkCenter"], abs=0.75)
            assert gear["buttonWidth"] >= 24, (name, gear)
            assert gear["buttonHeight"] >= 24, (name, gear)
        finally:
            page.close()


def test_focus_and_open_theme_menu_keep_header_visible(
    browser: Any, shells: dict[str, Path]
) -> None:
    page = browser.new_page(viewport={"width": 390, "height": 700}, reduced_motion="reduce")
    try:
        page.goto(shells["ordinary"].as_uri(), wait_until="load")
        page.locator(".site-headroom").wait_for(state="attached")
        page.evaluate(SCROLL, 600)
        page.locator('.site-nav a[data-page="overview"]').focus()
        assert not page.evaluate(STATE)["hidden"]
        page.evaluate(SCROLL, 700)
        assert not page.evaluate(STATE)["hidden"]
        page.locator(".site-theme-button").click()
        page.evaluate(SCROLL, 800)
        assert not page.evaluate(STATE)["hidden"]
        button = page.locator(".site-theme-button").bounding_box()
        menu = page.locator(".site-theme-menu").bounding_box()
        assert button is not None
        assert menu is not None
        assert menu["y"] == pytest.approx(button["y"] + button["height"] + 4, abs=0.5)
        page.set_viewport_size({"width": 1280, "height": 700})
        page.evaluate(SCROLL, 800)
        state = page.evaluate(STATE)
        assert state["offset"] >= state["height"]
        button = page.locator(".site-theme-button").bounding_box()
        menu = page.locator(".site-theme-menu").bounding_box()
        assert button is not None
        assert menu is not None
        assert menu["y"] == pytest.approx(button["y"] + button["height"] + 4, abs=0.5)
    finally:
        page.close()


def test_anchor_target_clears_the_whole_header(browser: Any, shells: dict[str, Path]) -> None:
    page = browser.new_page(viewport={"width": 390, "height": 700}, reduced_motion="reduce")
    try:
        page.goto(shells["ordinary"].as_uri(), wait_until="load")
        page.locator(".site-headroom").wait_for(state="attached")
        page.evaluate(ANCHOR)
        page.locator('.site-nav a[data-page="overview"]').focus()
        state = page.evaluate(STATE)
        assert state["targetTop"] >= state["bottom"], state
    finally:
        page.close()


def test_initial_fragment_keeps_the_top_region_at_the_headers_document_position(
    browser: Any, shells: dict[str, Path]
) -> None:
    page = browser.new_page(viewport={"width": 390, "height": 700}, reduced_motion="reduce")
    try:
        page.goto(shells["ordinary"].as_uri() + "#header-target", wait_until="load")
        page.locator(".site-headroom").wait_for(state="attached")
        initial = page.evaluate(STATE)
        assert initial["scroll"] > initial["height"]
        assert not initial["hidden"]
        assert initial["targetTop"] >= initial["bottom"], initial
        page.evaluate(SCROLL, initial["scroll"] + 10)
        assert page.evaluate(STATE)["hidden"]
        page.evaluate(SCROLL, initial["scroll"] + 7)
        assert not page.evaluate(STATE)["hidden"]
    finally:
        page.close()


def test_header_measurement_does_not_restyle_the_native_math_document(
    browser: Any, shells: dict[str, Path], tmp_path: Path
) -> None:
    """Header startup and wrapping must not invalidate the whole paper's styles."""
    expressions = 500
    mathematics = (
        '<math xmlns="http://www.w3.org/1998/Math/MathML">'
        "<mfrac><mrow><mi>s</mi><mo>(</mo><mi>n</mi><mo>)</mo></mrow>"
        "<msqrt><mi>n</mi></msqrt></mfrac></math>"
    ) * expressions
    path = tmp_path / "native-math-header.html"
    path.write_text(
        shells["ordinary"]
        .read_text()
        .replace("<h1>Header test</h1>", f"<h1>Header test</h1><div>{mathematics}</div>")
    )
    trace = tmp_path / "header-native-trace.json"
    page = browser.new_page(viewport={"width": 390, "height": 700}, reduced_motion="reduce")
    stop_trace = check_site_rendering.record_native_trace(page, trace)
    try:
        page.goto(path.as_uri(), wait_until="load")
        assert page.locator("math").count() == expressions
        page.locator(".site-headroom").wait_for(state="attached")
        narrow = page.evaluate(STATE)
        assert narrow["offset"] == pytest.approx(narrow["height"] + 8, abs=0.01)
        page.set_viewport_size({"width": 1280, "height": 700})
        page.evaluate(SCROLL, 0)
        wide = page.evaluate(STATE)
        assert wide["height"] < narrow["height"]
        assert wide["offset"] == pytest.approx(wide["height"] + 8, abs=0.01)
        page.evaluate(ANCHOR)
        page.locator('.site-nav a[data-page="overview"]').focus()
        anchored = page.evaluate(STATE)
        assert anchored["targetTop"] >= anchored["bottom"], anchored
    finally:
        stop_trace()
        page.close()

    events = json.loads(trace.read_text())["traceEvents"]
    measures = [
        event
        for event in events
        if event["name"] == "FunctionCall"
        and event.get("args", {}).get("data", {}).get("functionName") == "measure"
    ]
    assert len(measures) >= 2, measures
    invalidations = []
    for measure in measures:
        task = next(
            event
            for event in events
            if event["name"] == "RunTask"
            and event["tid"] == measure["tid"]
            and event["ts"] <= measure["ts"] < event["ts"] + event.get("dur", 0)
        )
        styles = [
            event.get("args", {}).get("elementCount", 0)
            for event in events
            if event["name"] == "UpdateLayoutTree"
            and event["tid"] == measure["tid"]
            and measure["ts"] + measure["dur"] <= event["ts"] < task["ts"] + task["dur"]
        ]
        invalidations.extend(styles)
    # Native trace counts establish the invalidation's scope without a machine-speed
    # threshold or an assertion about how the scroll clearance is implemented.
    assert max(invalidations, default=0) < expressions, invalidations


def test_nonscrolling_workbench_keeps_header_and_tabs_visible(
    browser: Any, shells: dict[str, Path]
) -> None:
    page = browser.new_page(viewport={"width": 390, "height": 700}, reduced_motion="reduce")
    try:
        page.goto(shells["workbench"].as_uri(), wait_until="load")
        page.locator(".site-headroom").wait_for(state="attached")
        page.mouse.wheel(0, 700)
        header = page.locator(".site-headroom")
        assert header.count() == 1
        assert "site-headroom-hidden" not in (header.get_attribute("class") or "")
        assert header.locator("nav.site-tabs").is_visible()
    finally:
        page.close()


def test_header_is_usable_without_javascript(browser: Any, shells: dict[str, Path]) -> None:
    page = browser.new_page(viewport={"width": 320, "height": 700}, java_script_enabled=False)
    try:
        page.goto(shells["ordinary"].as_uri(), wait_until="load")
        nav = page.locator(".site-nav")
        assert nav.is_visible()
        assert nav.locator('a[data-page="about"]').is_visible()
        assert nav.locator('a[data-page="github"]').is_visible()
    finally:
        page.close()
