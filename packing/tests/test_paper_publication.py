"""Published paper metadata and no-script reading retain the offline renderer contract."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

import pytest

from devtools import render_n11_lower_bounds_explainer as lower
from devtools import render_n11_optimality_review as optimality
from devtools import render_n11_threshold_bound_review as threshold
from devtools import render_overview, site_assets, site_math
from tests import test_render_n11_optimality_review as optimality_fixture
from tests import test_render_n11_threshold_bound_review as threshold_fixture


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


@pytest.mark.skipif(
    os.environ.get("SQPACK_N11_OPTIMALITY_REVIEW_BROWSER") != "1",
    reason="paper publication browser lane",
)
@pytest.mark.parametrize("fixture", [optimality_fixture, threshold_fixture])
def test_linked_paper_math_is_visible_without_javascript(fixture, tmp_path: Path) -> None:
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    paper = fixture.paper
    html, _ = paper.render(
        fixture.SOURCE,
        figures=fixture.FIGURES,
        revision=fixture.REVISION,
        article=fixture.ARTICLE,
    )
    lower.assert_self_contained(html)
    prepared = site_math.prepare(html)
    linked, assets = site_assets.link_inline_assets(prepared, paper.SITE_PATH)
    assert len(linked.encode()) < 800_000
    site_assets.write_assets(tmp_path, assets)
    output = tmp_path / paper.SITE_PATH
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(linked, encoding="utf-8")
    restored = site_assets.read_inline_page(output)
    lower.assert_self_contained(restored)
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
