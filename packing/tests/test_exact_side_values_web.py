"""The web report preserves exact values at readable phone and desktop widths."""

from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path
from typing import Literal

import pytest
from playwright.sync_api import Page, sync_playwright

from devtools import render_exact_side_values as paper
from tests import site_browser
from tests.test_render_exact_side_values import REVISION, small_document

NUMERATOR = "879879523721828390257668096702139408352101903022787926324037"
DENOMINATOR = "100000000000000000000000000000000000000000000000000000000000"
LONG_COEFFICIENT = "7" * 724


@pytest.fixture
def page() -> Iterator[Page]:
    with sync_playwright() as driver:
        browser = site_browser.launch(driver)
        try:
            yield browser.new_page()
        finally:
            browser.close()


@pytest.fixture(scope="module")
def complete_report() -> str:
    register = small_document()["register"]
    register["entries"][1]["exact_form_latex"] = rf"\tfrac{{{NUMERATOR}}}{{{DENOMINATOR}}}"
    register["entries"][2]["polynomial"]["coefficients"] = ["1", LONG_COEFFICIENT, "0"]
    html, _markdown = paper.render(
        paper.ARTICLE.read_text(), register=register, revision=REVISION
    )
    return html


@pytest.mark.parametrize("width", [390, 1280])
@pytest.mark.parametrize("scheme", ["light", "dark"])
def test_complete_web_report_preserves_long_fractions_and_coefficients(
    page: Page, complete_report: str, width: int, scheme: Literal["light", "dark"]
) -> None:
    page.set_viewport_size({"width": width, "height": 844})
    page.emulate_media(color_scheme=scheme)
    page.set_content(complete_report, wait_until="networkidle")
    layout = page.evaluate(paper.WEB_LAYOUT)
    assert layout["pageOverflow"] == 0
    assert layout["theme"] == scheme
    assert not paper.web_findings(layout), layout["lostInk"]
    assert layout["fractions"][0]["numerator"] == NUMERATOR
    assert layout["fractions"][0]["denominator"] == DENOMINATOR
    assert layout["fractions"][0]["fontPx"] >= 14
    assert page.locator("td code", has_text=LONG_COEFFICIENT).text_content() == LONG_COEFFICIENT
    assert layout["currentPolynomials"] == 4
    assert layout["historicalPolynomials"] == 1
    assert page.locator("#current-n3").count() == 1
    assert page.locator("#historical-n6-occurrence1").count() == 1
    assert page.locator("a[href$='.pdf']").count() == 0


def test_complete_report_remains_readable_without_javascript(
    page: Page, complete_report: str
) -> None:
    browser = page.context.browser
    assert browser is not None
    context = browser.new_context(
        java_script_enabled=False, viewport={"width": 390, "height": 844}
    )
    try:
        fallback = context.new_page()
        fallback.set_content(complete_report, wait_until="networkidle")
        layout = fallback.evaluate(paper.WEB_LAYOUT, {"settle": False})
        assert not paper.web_findings(layout), layout["lostInk"]
        assert layout["nativeMath"] > 0
        assert layout["coefficients"] == 3
        assert layout["fractions"][0]["numerator"] == NUMERATOR
    finally:
        context.close()


@pytest.mark.parametrize("accessible", [True, False])
def test_web_check_requires_keyboard_access_to_full_wide_table_content(
    page: Page, *, accessible: bool
) -> None:
    overflow = "auto" if accessible else "hidden"
    keyboard = ' tabindex="0"' if accessible else ""
    page.set_viewport_size({"width": 300, "height": 500})
    page.set_content(
        "<style>html,body{margin:0;} .kpress-table-wrap{width:300px;"
        f"overflow-x:{overflow};}} table{{width:600px;}}</style>"
        f'<div class="kpress-table-wrap"{keyboard}>'
        "<table><tbody><tr><td>Preserved full source content</td></tr></tbody></table></div>"
    )
    layout = page.evaluate(paper.WEB_LAYOUT)
    assert layout["pageOverflow"] == 0
    assert bool(paper.web_findings(layout)) is not accessible


def test_web_check_reads_existing_reports_without_regenerating_outputs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    site = tmp_path / "site"
    site.mkdir()
    stored = site / "report.html"
    stored.write_text("preserved publication")
    report = {"runs": [], "findings": ["document overflows"]}
    monkeypatch.setattr(paper, "check_web", lambda _site, **_kwargs: report)

    def forbidden_register() -> None:
        pytest.fail("read-only web check tried to regenerate the register")

    monkeypatch.setattr(paper, "load_register", forbidden_register)
    output = tmp_path / "web.json"
    assert paper.main(["--site", str(site), "--check-web", "--web-report", str(output)]) == 1
    assert json.loads(output.read_text()) == report
    assert json.loads(capsys.readouterr().out) == report
    assert stored.read_text() == "preserved publication"


@pytest.mark.parametrize(
    "defect",
    [
        "numerator",
        "denominator",
        "coefficient",
        "cell",
        "ancestor",
        "clip",
        "math-clip",
        "math-leaf",
    ],
)
def test_web_check_refuses_lost_exact_digits_and_clipped_math(page: Page, defect: str) -> None:
    selector = {
        "numerator": ".exact-numerator",
        "denominator": ".exact-denominator",
        "coefficient": "code",
        "cell": "td",
        "ancestor": ".source",
        "math-leaf": "math mn:first-child",
    }.get(defect)
    style = f"{selector} {{display:none;}}" if selector else ""
    if defect == "clip":
        style = "code {display:block;width:10px;white-space:nowrap;overflow:hidden;}"
    elif defect == "math-clip":
        style = ".kpress-math-display {height:2px;overflow:hidden;}"
    page.set_content(
        "<style>table{table-layout:fixed;width:100px;}" + style + "</style>"
        '<div class="source"><table><tbody><tr><td><code>123456789</code></td></tr>'
        "</tbody></table>"
        '<span class="exact-rational"><span class="exact-numerator">123</span>'
        '<span class="exact-denominator">789</span></span></div>'
        '<div class="kpress-math-display"><span class="kpress-math-semantic">'
        "<math><mfrac><mn>12345</mn><mn>67890</mn></mfrac></math></span></div>"
    )
    layout = page.evaluate(paper.WEB_LAYOUT)
    assert layout["pageOverflow"] == 0
    assert layout["lostInkCount"] > 0
    if defect in {"clip", "math-clip"}:
        assert any(run["clipped"] for run in layout["lostInk"])
    else:
        assert any(run["hidden"] for run in layout["lostInk"])
    assert paper.web_findings(layout)


def test_historical_native_equation_keeps_its_source_identity(page: Page) -> None:
    from playwright.sync_api import expect  # noqa: PLC0415

    from tests.test_exact_side_values_browser import Catalogue  # noqa: PLC0415

    catalogue = Catalogue(page)
    row = next(row for row in catalogue.entries if row["section"] == "historical")
    row["component"] = "H_7,1"
    metadata = catalogue.data[f"/data/{row['id']}.json"]
    metadata["claim"] = "V0/C0; polynomial checked; geometry awaits verification"
    catalogue.open("#" + row["id"])
    expect(page.locator("#detail-content")).to_be_visible()
    expect(page.locator("#entry-equation math mi").first).to_have_text("H")
    expect(page.locator("#entry-equation math")).to_have_attribute(
        "aria-label", "Historical polynomial H_7,1, degree 15"
    )
    assert page.locator("#entry-claim").text_content() == metadata["claim"]


@pytest.mark.parametrize("body", [None, "<p>Empty archive</p>"])
def test_web_diagnostics_preserve_missing_or_empty_archive_refusals(
    tmp_path: Path, body: str | None
) -> None:
    papers = tmp_path / "papers"
    index = papers / paper.exact_catalogue.INDEX_PATH
    index.parent.mkdir(parents=True)
    index.write_text(
        json.dumps(
            {
                "entries": [
                    {
                        "id": "current-n83",
                        "n": 83,
                        "section": "current",
                        "kind": "polynomial",
                        "degree": 672,
                    }
                ]
            }
        )
    )
    if body is not None:
        (tmp_path / paper.COMPLETE_PATH).write_text(body)
    report = paper.check_web(tmp_path)
    assert report["findings"]
    assert len(report["runs"]) == 8
    complete = [run for run in report["runs"] if run["path"] == paper.COMPLETE_PATH]
    assert all(run["phase"] in {"load", "content"} and run["error"] for run in complete)
    assert all("layout" not in run for run in complete)


def test_markdown_keeps_long_rational_math_without_requiring_report_css() -> None:
    register = small_document()["register"]
    source = rf"\tfrac{{{NUMERATOR}}}{{{DENOMINATOR}}}"
    register["entries"][1]["exact_form_latex"] = source
    register["historical_entries"][0]["attribution"]["source_text"] = [f"${source}$"]
    html, markdown = paper.render(
        paper.ARTICLE.read_text(), register=register, revision=REVISION
    )
    assert f"${source}$" in markdown
    assert "exact-numerator" not in markdown
    assert f'class="exact-numerator">{NUMERATOR}</span>' in html
    assert f'class="exact-denominator">{DENOMINATOR}</span>' in html
    assert f"<code>${source}$</code>" in html
