"""Static records retain their direct addresses and crawlable metadata."""

import json
import re
from unittest.mock import patch

from devtools import overview_data, overview_sections, render_overview, site_documents


def test_head_metadata_contains_breadcrumb_json_and_preview_permission() -> None:
    breadcrumb = render_overview.breadcrumb_data(
        ("Home", "index.html"), ("Cases", "cases/index.html"), ("11 squares", "cases/11.html")
    )
    meta = render_overview.PageMeta(
        "11 squares",
        "Bounds for packing eleven unit squares.",
        "cases/11.html",
        structured_data=(breadcrumb,),
    )
    head = render_overview.head_tags(meta)
    assert 'name="robots" content="max-image-preview:large"' in head
    match = re.search(r'<script type="application/ld\+json">(.*?)</script>', head)
    assert match is not None
    data = json.loads(match[1])
    assert data["@type"] == "BreadcrumbList"
    assert data["itemListElement"][-1]["item"] == render_overview.canonical_url("cases/11.html")


def test_synopsis_historical_anchors_link_to_the_exact_static_section() -> None:
    full = render_overview.Page(
        "synopsis.html",
        '<article><div class="kpress-prose">'
        '<h1 id="synopsis">Synopsis</h1>'
        '<h2 id="first">First</h2><h3 id="detail">Detail</h3>'
        '<p><a href="#second">Next</a></p>'
        '<h2 id="second">Second</h2><p>Full content.</p>'
        "</div></div></article>",
    )
    with patch.object(
        site_documents,
        "chapter_names",
        return_value=("synopsis/first.html", "synopsis/second.html"),
    ):
        index, chapters = site_documents.synopsis_parts(full)
    assert 'id="detail"><a href="synopsis/first.html#detail"' in index.html
    assert 'href="second.html#second"' in chapters[0].html
    assert "Full content." in chapters[1].html
    assert all(page.html.count("<h1") == 1 for page in chapters)


def test_recent_overview_contains_only_the_advertised_subset() -> None:
    overview = overview_data.load()
    table = overview_sections.recent_table(overview)
    reference = overview_sections.reference_date(overview)
    included = [
        result
        for result in overview_sections.recent_results(overview)
        if overview_sections.shown_by_default(
            result, overview_sections.RECENT_DEFAULTS, reference
        )
    ][: overview_sections.RECENT_LIMIT]
    assert table.count("<tr data-result=") == len(included) < len(overview.results)
    assert "data-filter=" not in table
    assert "data-all-results" not in table
    attributes = overview_sections.all_results_link_attributes(overview)
    assert attributes.startswith("data-all-results ")
    assert "data-result-ids=" in attributes
    for result in included:
        assert f'href="result/{result.id.lower()}.html"' in table
