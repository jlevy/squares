"""Persisted reader choices select matching static glyphs and KaTeX geometry."""

from __future__ import annotations

import re
from collections.abc import Iterator
from pathlib import Path
from typing import TYPE_CHECKING, Any
from unittest.mock import patch
from urllib.parse import urljoin

import pytest
from kpress.format.markdown import parse_markdown

from devtools import (
    check_site_rendering,
    overview_data,
    overview_sections,
    preview_site,
    render_overview,
    site_assets,
    site_math,
    site_urls,
)
from sqpack.probes import applied, probe
from tests import site_browser

if TYPE_CHECKING:
    from playwright.sync_api import Browser

_READ = probe(Path(__file__).parent / "probes", "site_math_preferences/read")
_CHOICES = (("serif", "custom"), ("sans", "custom"), ("sans", "system"))


@pytest.fixture(scope="module")
def browser() -> Iterator[Browser]:
    with site_browser.api().sync_playwright() as playwright:
        driver = site_browser.launch(playwright)
        yield driver
        driver.close()


def test_prepared_math_ignores_empty_runtime_style_attribute_order(browser: Browser) -> None:
    """Font visibility cleanup leaves empty style at timing-dependent attribute positions."""
    measure = applied(
        probe(
            render_overview.PACKING / "devtools/probes",
            "prepare_n11_lower_bounds_explainer_math/measure_math",
        )
    )
    data = 'data-kpress-math-source="n" data-kpress-math-display="inline"'
    styled = 'style="color: rgb(1, 2, 3); --publication-note: keep"'
    attributes = (data, f'style="" {data}', f'{data} style=""', f'style="  " {data}')
    page = browser.new_page()
    try:
        fragments = []
        for attrs in (*attributes, f"{data} {styled}"):
            page.set_content(
                "<style>.base {display:inline-block;font-size:20px;"
                "text-rendering:geometricPrecision}</style>"
                '<span class="kpress-math" data-squares-math-key="0">'
                f'<span class="kpress-math-render" aria-hidden="true" {attrs}>'
                '<span class="katex"><span class="katex-html"><span class="base">'
                '<span class="strut" style="display:inline-block;height:1em"></span>n'
                "</span></span></span></span><math><mi>n</mi></math></span>"
            )
            live = page.locator(".kpress-math-render")
            live_style = live.get_attribute("style")
            prepared = page.evaluate(
                measure,
                [
                    "data-kpress-math-source",
                    "data-kpress-math-display",
                    "data-kpress-math-prepared",
                ],
            )
            assert len(prepared) == 1
            fragments.append(prepared[0]["html"])
            assert live.get_attribute("style") == live_style
        assert all(fragment == fragments[0] for fragment in fragments[1:-1])
        assert styled in fragments[-1]
        assert all("<math><mi>n</mi></math>" in fragment for fragment in fragments)
        assert all('class="squares-math-box" style="' in fragment for fragment in fragments)
        assert 'data-kpress-math-source="n"' in fragments[0]
    finally:
        page.close()


def _native_reference(raw: str, *, prose: str, fonts: str) -> str:
    """Independent raw KaTeX output is the geometry reference, without shared classes."""
    formulas = site_math.formula_sources(raw)
    changes = []
    keys = []
    for formula in formulas:
        profile = (
            "katex"
            if fonts == "system" or formula.choice == "katex"
            else "sans"
            if formula.choice == "sans" or (formula.choice == "prose" and prose == "sans")
            else "prose"
        )
        key: site_math.MathKey = (formula.source, formula.display, profile, False)
        keys.append((formula, key))
    native = site_math.native_math(list(dict.fromkeys(key for _, key in keys)))
    for formula, key in keys:
        opening = raw[formula.start : formula.content]
        opening = (
            opening[:-1]
            + f' data-site-math="{formula.choice}" data-kpress-math-face="{key[2]}"'
            + ' data-kpress-math-prepared="true">'
        )
        changes.append((formula.start, formula.end, opening + native[key]))
        assert formula.host_start is not None
        assert formula.host_content is not None
        host = raw[formula.host_start : formula.host_content]
        changes.append(
            (
                formula.host_start,
                formula.host_content,
                host[:-1] + ' data-kpress-math-rendered="true">',
            )
        )
    pieces = []
    cursor = 0
    for start, end, replacement in sorted(changes):
        pieces.extend((raw[cursor:start], replacement))
        cursor = end
    pieces.append(raw[cursor:])
    reference = "".join(pieces)
    css = site_assets.shared().assets.stylesheet_file(
        render_overview.TEMPLATES / "site-math.css"
    )
    return reference.replace(
        "</head>", site_assets.stylesheet_tag(css, "index.html") + "</head>"
    )


@pytest.fixture(scope="module")
def pages(tmp_path_factory: pytest.TempPathFactory) -> Iterator[str]:
    root = tmp_path_factory.mktemp("reader-fonts")
    fragment = parse_markdown(
        r"Visible $n + x^2 + \frac{1}{2} + \sqrt{5}$ mathematics.", title="Reader fonts"
    ).html
    body = (
        "<main><h1>Reader font compatibility</h1>"
        f'<div data-font-role="prose">{fragment}</div>'
        f'<div class="sans-text" data-font-role="sans">{fragment}</div>'
        '<div class="sans-text"><div data-math-face="serif" data-font-role="serif">'
        f'{fragment}</div></div><div data-kpress-math-text="katex" data-font-role="stock">'
        f'{fragment}</div><button popovertarget="closed">Open prepared formula</button>'
        '<div popover id="closed" class="site-popover" data-font-role="closed">'
        f"{fragment}</div>"
        "</main>"
    )
    with patch.object(site_math, "prepare", side_effect=lambda html: html):
        raw = render_overview.static_content_page(
            body,
            meta=render_overview.PageMeta(
                "Reader fonts", "Saved reading fonts retain matching math.", "index.html"
            ),
            current="atlas",
        ).html
    prepared = site_math.prepare(raw)
    (root / "index.html").write_text(prepared)
    for prose, fonts in _CHOICES:
        reference = _native_reference(raw, prose=prose, fonts=fonts)
        attrs = f' data-kpress-prose-font="{prose}" data-kpress-font-set="{fonts}"'
        suffix = f"{prose}-{fonts}.html"
        (root / f"reference-{suffix}").write_text(reference)
        (root / f"nojs-{suffix}").write_text(prepared.replace("<html", "<html" + attrs, 1))
        (root / f"reference-nojs-{suffix}").write_text(
            reference.replace("<html", "<html" + attrs, 1)
        )
    site_assets.write_assets(root, site_assets.shared().assets.files())
    server = preview_site.serve(root, 0)
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()


def _compare_geometry(actual: dict[str, Any], native: dict[str, Any]) -> None:
    assert len(actual["formulas"]) == len(native["formulas"]) == 5
    for formula, reference in zip(actual["formulas"], native["formulas"], strict=True):
        assert formula["visualCount"] == reference["visualCount"] == 1
        assert formula["semantics"] == reference["semantics"] == 1
        assert formula["family"] == reference["family"]
        for dimension in ("paragraphWidth", "paragraphHeight"):
            assert formula[dimension] == pytest.approx(reference[dimension], abs=0.04)
        assert len(formula["nodes"]) == len(reference["nodes"])
        for node, expected in zip(formula["nodes"], reference["nodes"], strict=True):
            assert node["classes"] == expected["classes"]
            for dimension in ("left", "top", "width", "height"):
                assert node[dimension] == pytest.approx(expected[dimension], abs=0.04), (
                    formula["role"],
                    dimension,
                    node["font"],
                    expected["font"],
                    node["verticalAlign"],
                    expected["verticalAlign"],
                    formula["hostFont"],
                    reference["hostFont"],
                )


@pytest.mark.parametrize(("prose", "fonts"), _CHOICES)
@pytest.mark.parametrize("javascript", [False, True], ids=["no-runtime", "saved-preference"])
def test_saved_reader_faces_match_native_metric_geometry(
    browser: Browser, pages: str, prose: str, fonts: str, *, javascript: bool
) -> None:
    context = browser.new_context(
        java_script_enabled=javascript,
        storage_state={
            "cookies": [],
            "origins": [
                {
                    "origin": pages,
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
        suffix = f"{prose}-{fonts}.html"
        actual = f"{pages}/index.html" if javascript else f"{pages}/nojs-{suffix}"
        reference = f"{pages}/reference-{'nojs-' if not javascript else ''}{suffix}"
        readings = []
        for url in (actual, reference):
            page.goto(url, wait_until="load")
            check_site_rendering.wait_for_fonts(page)
            closed = page.evaluate(_READ)["formulas"][-1]
            assert closed["visualCount"] == 0
            assert closed["semantics"] == 1
            page.locator('[popovertarget="closed"]').click()
            check_site_rendering.wait_for_fonts(page)
            readings.append(page.evaluate(_READ))
        assert (readings[0]["prose"], readings[0]["fonts"]) == (prose, fonts)
        assert readings[0]["mathScripts"] == 0
        _compare_geometry(*readings)
        families = {formula["role"]: formula["family"] for formula in readings[0]["formulas"]}
        if fonts == "system":
            assert all("KPress" not in family for family in families.values())
        else:
            assert "Sans" in families["sans"]
            assert "Sans" in families["closed"]
            assert "Sans" not in families["serif"]
            assert "KPress" not in families["stock"]
            assert ("Sans" in families["prose"]) == (prose == "sans")
    finally:
        context.close()


@pytest.fixture(scope="module")
def amended_result_pages(tmp_path_factory: pytest.TempPathFactory) -> Iterator[str]:
    root = tmp_path_factory.mktemp("result-address-notice")
    records = {
        page.name: page
        for page in render_overview.iter_result_fragments(
            result_ids=frozenset({"T-116", "T-110"})
        )
    }
    for name in ("result/t-116.html", "result/t-110.html"):
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(records[name].html)
    overview = overview_data.load()
    result = next(result for result in overview.results if result.id == "T-116")
    row, popover = overview_sections.result_table_row(result, overview, here=True, shown=True)
    body = (
        "<main><h1>Result address compatibility</h1><table><tbody>"
        f"{row}</tbody></table>{popover}</main>"
    )
    page = render_overview.static_content_page(
        body,
        meta=render_overview.PageMeta(
            "Result address compatibility", "A former result keeps its own page.", "index.html"
        ),
        current="results",
        page_scripts=(render_overview.ROW_POPOVER_SCRIPT,),
    )
    (root / "index.html").write_text(page.html)
    site_assets.write_assets(root, site_assets.shared().assets.files())
    server = preview_site.serve(root, 0)
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()


def test_a_generated_result_overlay_keeps_one_visible_headline(
    browser: Browser, amended_result_pages: str
) -> None:
    """The canonical title replaces the short shell title and names the dialog."""
    context = browser.new_context()
    try:
        page = context.new_page()
        page.goto(f"{amended_result_pages}/index.html", wait_until="load")
        row = page.locator('tr[data-row-popover="pop-result-t-116"]')
        row.focus()
        page.keyboard.press("Enter")
        popover = page.locator("#pop-result-t-116")
        article = popover.locator("article.site-result")
        article.wait_for()
        canonical_title = article.locator(":scope > h1")
        site_browser.api().expect(canonical_title).to_be_visible()
        assert (
            popover.locator(":scope > .site-card-label, :scope > .site-popover-value").count()
            == 0
        )
        assert (canonical_title.get_attribute("id") or "").endswith("-t-116")
        assert popover.get_attribute("aria-labelledby") == canonical_title.get_attribute("id")
        site_browser.api().expect(popover).to_have_accessible_name(re.compile(r"\S"))
        page.keyboard.press("Escape")
        site_browser.api().expect(row).to_be_focused()
        page.goto(f"{amended_result_pages}/result/t-116.html", wait_until="load")
        site_browser.api().expect(page.locator("main article.site-result > h1")).to_be_visible()
    finally:
        context.close()


@pytest.mark.parametrize("javascript", [False, True], ids=["complete-nojs", "fetched-article"])
def test_former_result_notice_survives_complete_page_and_article_fetch(
    browser: Browser, amended_result_pages: str, *, javascript: bool
) -> None:
    amendment = next(
        change
        for row in site_urls.load_registry()
        if row.path == "result/t-116.html"
        for change in row.amendments
        if change.get("historical_target")
    )
    context = browser.new_context(java_script_enabled=javascript)
    try:
        page = context.new_page()
        start = "index.html" if javascript else "result/t-116.html"
        page.goto(f"{amended_result_pages}/{start}", wait_until="load")
        if javascript:
            assert page.locator(".site-result-compatibility").count() == 0
            page.locator("tr[data-row-popover]").focus()
            page.keyboard.press("Enter")
        notice = page.locator("article.site-result .site-result-compatibility")
        notice.wait_for(state="visible")
        assert amendment["historical_title"] in notice.inner_text()
        assert "separate upper bound result" in notice.inner_text()
        target = notice.locator("a")
        expected = f"{amended_result_pages}/{amendment['historical_target']}"
        href = target.get_attribute("href")
        assert href is not None
        assert urljoin(page.url, href) == expected
        target.click()
        page.wait_for_url(expected)
        assert page.locator("main article h1").is_visible()
        assert "T-110" in page.locator("main article h1").inner_text()
    finally:
        context.close()
