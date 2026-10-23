"""Repository document pages share real GitHub and raw Markdown source actions."""

import re
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

from devtools import paper_front, render_overview, repo_links, site_documents
from tests import site_browser, site_renders


@pytest.fixture(scope="module")
def documents() -> dict[str, render_overview.Page]:
    return site_documents.site_documents()


def source_row(page: str) -> str:
    rows = re.findall(r'<div class="doc-links screen-only">(.*?)</div>', page, re.DOTALL)
    assert len(rows) == 1
    return rows[0]


def test_every_repository_document_and_synopsis_chapter_links_its_actual_source(
    documents: dict[str, render_overview.Page],
) -> None:
    sources = {document.name: document.source for document in site_documents.DOCUMENTS}
    sources.update(
        dict.fromkeys(site_documents.chapter_names(), repo_links.REPO / repo_links.SYNOPSIS)
    )
    assert set(sources) == set(documents)
    for name, source in sources.items():
        assert source.is_file(), name
        row = source_row(documents[name].html)
        assert re.findall(r'href="([^"]+)"', row) == [
            repo_links.repo_url(source),
            repo_links.repo_url(source, kind="raw"),
        ], name
        assert row.count("<svg") == 1, name
        assert "GITHUB</a>" in row, name
        assert ">MD</a>" in row, name
        assert ".pdf" not in row, name
    assert Path(paper_front.__file__) in render_overview.inputs()


@pytest.fixture(scope="module")
def source_browser() -> Iterator[Any]:
    with site_browser.api().sync_playwright() as driver:
        browser = site_browser.launch(driver)
        yield browser
        browser.close()


@pytest.mark.parametrize("width", [1280, 390])
def test_source_actions_remain_visible_within_the_document_viewport(
    source_browser: Any, tmp_path: Path, width: int
) -> None:
    path = site_renders.write(tmp_path, "epistemics.html")["epistemics.html"]
    page = source_browser.new_page(viewport={"width": width, "height": 900})
    try:
        page.goto(path.as_uri(), wait_until="load")
        source_browser_api = site_browser.api()
        row = page.locator(".doc-links")
        source_browser_api.expect(row).to_be_visible()
        source_browser_api.expect(
            row.get_by_role("link", name="GITHUB", exact=True)
        ).to_be_visible()
        source_browser_api.expect(
            row.get_by_role("link", name="MD", exact=True)
        ).to_be_visible()
        assert row.locator("svg").count() == 1
        box = row.bounding_box()
        assert box is not None
        assert box["x"] >= 0
        assert box["x"] + box["width"] <= width
        title = page.locator("h1").first.bounding_box()
        assert title is not None
        # Source controls are not a preceding content section. The first title
        # keeps the page's normal top edge rather than the 100px section gap.
        assert abs(title["y"] - box["y"]) < 16
    finally:
        page.close()
