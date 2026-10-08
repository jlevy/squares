"""The column tool reports actual scroll extremes and preserves table geometry."""

from pathlib import Path

import pytest

from devtools.measure_site_pages import measure_columns
from tests import site_browser


def test_scroll_check_measures_both_extremes_and_restores_the_layout(tmp_path: Path) -> None:
    site_browser.api()
    page = tmp_path / "columns.html"
    page.write_text(
        """<html><head><style>
body { margin:0; font-family:sans-serif }
.site-table-wrap { overflow:auto; width:100% }
table { width:700px; table-layout:fixed; border-collapse:collapse }
footer { height:2000px }
</style></head><body><div class="site-table-wrap">
<table class="site-table"><thead><tr><th>A</th><th>B</th></tr></thead>
<tbody><tr id="first"><td>One</td><td>Two</td></tr></tbody></table>
</div><footer></footer></body></html>"""
    )
    report = measure_columns(tmp_path.as_uri(), [page.name], widths=(390,), scroll_check=True)
    (table,) = report
    assert table["shown_ids"] == ["first"]
    assert table["page_scrolls"] == 0
    assert all(column["body_font"]["family"] == "sans-serif" for column in table["columns"])
    states = table["scroll_geometry"]
    assert states["initial"]["window_scroll_y"] == 0
    assert states["vertical_end"]["window_scroll_y"] > 0
    assert states["horizontal_end"]["frame_scroll_left"] > 0
    assert states["restored"]["window_scroll_y"] == 0
    assert states["restored"]["frame_scroll_left"] == 0
    for measured in states.values():
        assert measured["table_width"] == pytest.approx(700, abs=0.5)
        assert measured["column_widths"] == states["initial"]["column_widths"]
        assert measured["frame_width"] == 390
        assert measured["page_scrolls"] == 0


def test_card_groups_read_the_first_matching_cell_across_visible_rows(
    tmp_path: Path,
) -> None:
    site_browser.api()
    (tmp_path / "later.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16">'
        '<rect width="16" height="16"/></svg>'
    )
    page = tmp_path / "cards.html"
    page.write_text(
        """<html><head><style>
body { margin:0 }
thead { display:none }
table, tbody, tr, td { display:block }
.site-n-wraps { font-family:monospace; font-size:19px; font-weight:700 }
tr[hidden] { display:none }
</style></head><body><table class="site-table">
<thead><tr><th>Cases</th></tr></thead><tbody>
<tr id="hidden" hidden><td class="site-n-wraps">Hidden</td></tr>
<tr id="first"><td class="site-n-nowrap">One</td></tr>
<tr id="later"><td class="site-n-wraps">Many <img src="later.svg"></td></tr>
</tbody></table></body></html>"""
    )
    (table,) = measure_columns(tmp_path.as_uri(), [page.name], widths=(390,))
    assert table["layout"] == "cards"
    assert table["shown_ids"] == ["first", "later"]
    groups = {column["column"]: column for column in table["columns"]}
    later = groups["site-n-wraps"]
    assert later["body_font"] == {
        "family": "monospace",
        "size": "19px",
        "weight": "700",
        "line_height": "normal",
    }
    assert later["first_image"]["src"] == "later.svg"
    assert later["first_image"]["complete"]
    assert later["first_image"]["natural_width"] == 16
    assert later["first_image"]["natural_height"] == 16
    assert groups["site-n-nowrap"]["body_font"] is not None
    assert groups["site-n-nowrap"]["first_image"] is None
