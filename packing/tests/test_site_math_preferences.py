"""Persisted reader choices select matching static glyphs and KaTeX geometry."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import TYPE_CHECKING, Any
from unittest.mock import patch

import pytest
from kpress.format.markdown import parse_markdown

from devtools import check_site_rendering, preview_site, render_overview, site_assets, site_math
from sqpack.probes import probe
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
            current="frontier",
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
