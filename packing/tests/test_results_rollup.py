"""The retired Recent Results page keeps one canonical All Results destination."""

from __future__ import annotations

import pytest

from devtools import paper_structure, render_overview
from tests import site_renders


@pytest.fixture(scope="module")
def results() -> str:
    return site_renders.html(render_overview.RESULTS_PAGE)


def test_recent_results_is_a_compatibility_route_not_a_second_collection() -> None:
    assert "recent-results.html" not in render_overview.PAGES
    assert "recent-results.html" not in render_overview.SITE_PAGES
    assert not hasattr(render_overview, "recent_results_page")
    assert dict(render_overview.MOVED_PAGES)["recent-results.html"] == "results.html"
    alias = next(
        page for page in render_overview.forwarder_pages() if page.name == "recent-results.html"
    )
    assert 'data-moved-to="results.html"' in alias.html
    assert 'rel="canonical" href="https://squaremath.org/results.html"' in alias.html
    assert "data-recent-results" not in alias.html


def test_all_results_keeps_every_record_once_with_shared_metadata(results: str) -> None:
    document = paper_structure.parse(results)
    tables = [node for node in document.walk() if node.tag == "table"]
    assert len(tables) == 1
    rows = [
        node for node in tables[0].walk() if node.tag == "tr" and "data-added" in node.attrs
    ]
    expected = {result.id.lower(): result for result in site_renders.overview().results}
    identifiers = [row.attrs["id"] for row in rows]
    assert len(identifiers) == len(set(identifiers)) == len(expected)
    assert set(identifiers) == set(expected)
    assert "data-site-table" in results
    assert "data-recent-toggle" not in results
    for row in rows:
        result = expected[row.attrs["id"]]
        assert row.attrs["data-v"] == result.record["verification"][1:]
        assert row.attrs["data-c"] == result.record["confirmation"][1:]
        assert row.attrs["data-kind"] == result.record["kind"]
        assert row.attrs["data-status"] == result.status
        assert "hidden" not in row.attrs
