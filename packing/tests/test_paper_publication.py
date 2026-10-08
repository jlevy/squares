"""Published paper metadata and no-script reading retain the offline renderer contract."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from types import ModuleType

import pytest

from devtools import render_n11_lower_bounds_explainer as lower
from devtools import render_n11_optimality_review as optimality
from devtools import render_n11_threshold_bound_review as threshold
from devtools import render_overview, site_assets, site_math
from sqpack.yamlio import safe_load
from tests import test_render_n11_optimality_review as optimality_fixture
from tests import test_render_n11_threshold_bound_review as threshold_fixture

PAPER_BROWSER_FIXTURES = [
    pytest.param(
        fixture,
        id=fixture.paper.SLUG,
        marks=pytest.mark.skipif(
            os.environ.get(flag) != "1",
            reason=f"{fixture.paper.SLUG} publication browser lane",
        ),
    )
    for fixture, flag in (
        (optimality_fixture, "SQPACK_N11_OPTIMALITY_REVIEW_BROWSER"),
        (threshold_fixture, "SQPACK_N11_THRESHOLD_BOUND_REVIEW_BROWSER"),
    )
]


def _write_linked_page(html: str, page_path: str, root: Path) -> tuple[Path, str]:
    """Publish the fixture at its served depth, with every linked asset present."""
    prepared = site_math.prepare(html, page_path=page_path)
    linked, assets = site_assets.link_inline_assets(prepared, page_path)
    assert len(linked.encode()) < 800_000
    output = root / page_path
    output.parent.mkdir(parents=True, exist_ok=True)
    roots = {
        (output.parent / prefix).resolve()
        for prefix in re.findall(r'(?:href|src)="((?:\.\./)*assets)/', linked)
    }
    assert roots == {(root / site_assets.ASSETS_DIR).resolve()}
    site_assets.write_assets(root, assets)
    output.write_text(linked, encoding="utf-8")
    restored = site_assets.read_inline_page(output)
    lower.assert_self_contained(restored)
    assert site_math.prepare(restored, page_path=page_path) == restored
    return output, restored


@pytest.mark.parametrize(
    ("paper", "flag"),
    [
        (optimality, "SQPACK_N11_OPTIMALITY_REVIEW_BROWSER"),
        (threshold, "SQPACK_N11_THRESHOLD_BOUND_REVIEW_BROWSER"),
    ],
    ids=[optimality.SLUG, threshold.SLUG],
)
def test_each_sparse_paper_producer_runs_its_publication_browser_contract(paper, flag) -> None:
    workflow = safe_load(
        (Path(__file__).resolve().parents[2] / ".github/workflows/pages.yml").read_text()
    )
    checks = [
        step
        for step in workflow["jobs"][paper.SLUG]["steps"]
        if "tests/test_paper_publication.py" in step.get("run", "")
    ]
    assert len(checks) == 1
    assert checks[0]["env"][flag] == "1"
    assert all(
        other not in checks[0]["env"]
        for other in (
            "SQPACK_N11_OPTIMALITY_REVIEW_BROWSER",
            "SQPACK_N11_THRESHOLD_BOUND_REVIEW_BROWSER",
        )
        if other != flag
    )


@pytest.mark.parametrize("page_path", [optimality.SITE_PATH, threshold.SITE_PATH])
def test_prepared_paper_metric_and_page_styles_share_the_served_asset_root(
    page_path: str, tmp_path: Path
) -> None:
    from kpress.format.markdown import parse_markdown  # noqa: PLC0415

    fragment = parse_markdown("A formula $x^2$.", title="Paper").html
    html = (
        "<html><head><title>Paper</title><style>p{color:navy}</style></head>"
        f"<body><main>{fragment}</main></body></html>"
    )
    output, restored = _write_linked_page(html, page_path, tmp_path)
    linked = output.read_text()
    assert '<link data-site-math-styles rel="stylesheet" href="../assets/' in linked
    assert restored.count('class="katex-html"') == restored.count("<math") == 1
    assert "<style data-site-math-styles>" in restored
    assert "p{color:navy}" in restored
    sheets = list((tmp_path / "assets/css").glob("*.css"))
    assert len(sheets) >= 2
    assert sum(path.stat().st_size for path in tmp_path.rglob("*") if path.is_file()) < 50_000

    # A conflicting base is a malformed page, not a reason to weaken the inliner.
    output.write_text(linked.replace('href="../assets/', 'href="assets/', 1))
    with pytest.raises(ValueError, match="multiple asset roots"):
        site_assets.read_inline_page(output)
    output.write_text(linked)
    sheets[0].unlink()
    with pytest.raises(FileNotFoundError):
        site_assets.read_inline_page(output)


@pytest.mark.parametrize(
    "meta", [lower.published_page_meta(), optimality.page_meta(), threshold.page_meta()]
)
def test_paper_metadata_matches_the_published_title_dates_and_downloads(
    meta: render_overview.PageMeta,
) -> None:
    head = render_overview.head_tags(meta)
    records = [
        json.loads(value)
        for value in re.findall(r'<script type="application/ld\+json">(.*?)</script>', head)
    ]
    article, breadcrumb = records
    assert article["@type"] == "ScholarlyArticle"
    assert article["headline"] == meta.name
    assert article["datePublished"] == meta.published
    assert article["dateModified"] == meta.modified
    assert article["author"] == [
        {"@type": "Person", "name": "Joshua Levy", "url": "https://x.com/ojoshe"}
    ]
    url = render_overview.canonical_url(meta.path)
    tags = dict(meta.extra_meta)
    assert tags["citation_title"] == meta.name
    assert tags["citation_author"] == "Joshua Levy"
    assert tags["citation_publication_date"] == meta.published
    assert tags["citation_abstract_html_url"] == article["url"] == url
    assert (
        tags["citation_pdf_url"]
        == article["encoding"]["contentUrl"]
        == url.removesuffix(".html") + ".pdf"
    )
    assert breadcrumb["@type"] == "BreadcrumbList"
    assert [item["name"] for item in breadcrumb["itemListElement"]] == [
        "Home",
        "Papers",
        meta.name,
    ]
    assert f" · {render_overview.PROJECT_NAME}</title>" not in head


@pytest.mark.parametrize("fixture", PAPER_BROWSER_FIXTURES)
def test_linked_paper_math_is_visible_without_javascript(
    fixture: ModuleType, tmp_path: Path
) -> None:
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    paper = fixture.paper
    html, _ = paper.render(
        fixture.SOURCE,
        figures=fixture.FIGURES,
        revision=fixture.REVISION,
        article=fixture.ARTICLE,
    )
    lower.assert_self_contained(html)
    output, _ = _write_linked_page(html, paper.SITE_PATH, tmp_path)
    with sync_playwright() as driver:
        browser = driver.chromium.launch(
            executable_path=os.environ.get("SQUARES_BROWSER_EXECUTABLE")
        )
        try:
            page = browser.new_page(java_script_enabled=False)
            page.goto(output.as_uri(), wait_until="networkidle")
            math = page.locator(".katex-html")
            assert math.count() > 0
            assert all(math.nth(index).is_visible() for index in range(math.count()))
            if 'class="tex"' in paper.FRONT.title:
                assert page.locator(".hero h1 .katex-html").count() > 0
        finally:
            browser.close()
