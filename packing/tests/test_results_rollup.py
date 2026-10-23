"""Recent Results is one complete arrival-ordered table, with an older-row disclosure."""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from devtools import overview_data, overview_sections, paper_structure, render_overview
from tests import site_renders


@pytest.fixture(scope="module")
def overview() -> overview_data.Overview:
    return site_renders.overview()


@pytest.fixture(scope="module")
def recent_page() -> str:
    return site_renders.html(render_overview.RECENT_RESULTS_PAGE)


@pytest.fixture(scope="module")
def table(recent_page: str) -> paper_structure.Node:
    document = paper_structure.parse(recent_page)
    tables = [node for node in document.walk() if node.tag == "table"]
    assert len(tables) == 1
    assert "data-recent-results" in tables[0].attrs
    return tables[0]


def _rows(node: paper_structure.Node) -> list[paper_structure.Node]:
    return [part for part in node.walk() if part.tag == "tr" and "data-result" in part.attrs]


def _arrival(result: overview_data.Result) -> date:
    return date.fromisoformat(str(result.record.get("landed") or result.record["registered"]))


def test_recent_table_keeps_every_result_once_in_arrival_order(
    table: paper_structure.Node, overview: overview_data.Overview
) -> None:
    """Ordering and completeness come from retained arrival dates, not publication
    dates or significance; results formerly repeated in two lists appear once."""
    expected = sorted(
        overview.results, key=lambda result: (-_arrival(result).toordinal(), result.id)
    )
    rows = _rows(table)
    identifiers = [row.attrs["data-result"] for row in rows]
    assert identifiers == [result.id.lower() for result in expected]
    assert len(identifiers) == len(set(identifiers)) == len(overview.results)
    assert all("hidden" not in row.attrs for row in rows)
    for row, result in zip(rows, expected, strict=True):
        cells = [child for child in row.children if isinstance(child, paper_structure.Node)]
        assert len(cells) == 8
        assert cells[0].attrs["data-value"] == _arrival(result).isoformat()
        assert cells[0].text().startswith(_arrival(result).isoformat())
        assert "added" in cells[0].text()
        assert row.attrs["data-added"] == _arrival(result).isoformat()


def test_seven_calendar_dates_are_current_and_every_older_row_shares_the_table(
    table: paper_structure.Node, overview: overview_data.Overview
) -> None:
    """The newest arrival day and six preceding dates start open; all older rows
    remain in a second tbody of the same table and are available without scripts."""
    bodies = [
        child
        for child in table.children
        if isinstance(child, paper_structure.Node) and child.tag == "tbody"
    ]
    assert len(bodies) == 2
    cutoff = max(_arrival(result) for result in overview.results) - timedelta(days=6)
    assert table.attrs["data-recent-cutoff"] == cutoff.isoformat()
    current, older = bodies
    by_id = {result.id.lower(): result for result in overview.results}
    assert {row.attrs["data-result"] for row in _rows(current)} == {
        identifier for identifier, result in by_id.items() if _arrival(result) >= cutoff
    }
    assert {row.attrs["data-result"] for row in _rows(older)} == {
        identifier for identifier, result in by_id.items() if _arrival(result) < cutoff
    }
    assert older.attrs["id"] == "recent-results-older"
    assert "data-recent-older" in older.attrs
    assert "hidden" not in older.attrs
    controls = [node for node in current.walk() if "data-recent-toggle" in node.attrs]
    assert len(controls) == 1
    assert controls[0].tag == "button"
    assert controls[0].attrs["aria-controls"] == older.attrs["id"]
    assert controls[0].attrs["aria-expanded"] == "false"
    assert controls[0].text() == "Earlier results"
    assert not any("data-sort" in node.attrs for node in table.walk())


def test_recent_rows_keep_shared_metadata_and_canonical_record_links(
    table: paper_structure.Node, overview: overview_data.Overview
) -> None:
    """The consolidated view retains the shared claim, credit, ratings, status and
    case metadata, with each result's full record one ordinary link away."""
    by_id = {result.id.lower(): result for result in overview.results}
    for row in _rows(table):
        result = by_id[row.attrs["data-result"]]
        assert row.attrs["data-v"] == result.record["verification"][1:]
        assert row.attrs["data-c"] == result.record["confirmation"][1:]
        assert row.attrs["data-kind"] == result.record["kind"]
        assert row.attrs["data-status"] == result.status
        cells = [node for node in row.walk() if node.tag == "td"]
        assert cells[4].attrs["data-value"] == result.credit
        links = [node.attrs.get("href") for node in row.walk() if node.tag == "a"]
        assert overview_sections.result_fragment(result.id) in links
        assert cells[7].text() == result.id


def test_recent_page_has_only_its_title_before_the_table_and_retains_legacy_ids(
    recent_page: str, table: paper_structure.Node
) -> None:
    """The lists' legacy anchors now land on the one table or its older-row boundary;
    extra introductions, local navigation and filter bars do not precede it."""
    before = recent_page.split("<article", 1)[1].split("<table", 1)[0]
    assert '<h1 id="recent-results">Recent Results</h1>' in before
    for extra in ("<p", "<nav", "<h2", "site-table-tools", "site-rollup"):
        assert extra not in before
    for identifier in (
        "recent-arrivals",
        "added-in-the-last-seven-days",
        "earlier-results-by-week-published",
    ):
        assert recent_page.count(f'id="{identifier}"') == 1
    assert table.attrs["id"] == "added-in-the-last-seven-days"
