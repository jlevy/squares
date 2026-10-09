"""The atlas measuring tool's own arithmetic and judgement, with no browser.

`devtools.measure_atlas_views` reads the homepage's atlas in a browser and says what is
wrong with a layout (`layout_problems`). The browser tests (`test_site_atlas_views`) rely
on that judgement, so this holds it: the triangle's complete right-aligned rows,
written here independently of the page's script, and each fault a layout may
have, planted in a layout that is otherwise right and required to be named. The same
goes for the marks a tile carries (`mark_problems`): a new-result star or a regularized
badge over its number or out of its tile, and a number pushed off its tile's centre.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from devtools import measure_atlas_views as atlas

#: A block 400 pixels wide starting 20 from the window's edge.
LEFT, WIDTH = 20.0, 400.0


def _tile(n: int, left: float, top: float, size: float) -> dict[str, Any]:
    return {
        "n": n,
        "left": left,
        "top": top,
        "right": left + size,
        "bottom": top + size + 12,
        "width": size,
        "height": size + 12,
        "drawing": {"left": left + 2, "top": top + 2, "width": size - 4},
        "number_px": 9.0,
    }


def _report(view: str, per: int | None, tiles: list[dict[str, Any]]) -> dict[str, Any]:
    bottom = max(tile["bottom"] for tile in tiles)
    return {
        "view": view,
        "per_line": per,
        "cells": {
            "left": LEFT,
            "top": 0.0,
            "right": LEFT + WIDTH,
            "bottom": bottom,
            "width": WIDTH,
            "height": bottom,
        },
        "moving": 0,
        "overflow": 0,
        "tiles": tiles,
    }


def _triangle(last: int, per: int) -> dict[str, Any]:
    """Complete rows, right aligned on a canvas that keeps the viewport tile scale."""
    size = WIDTH / per
    canvas_width = max(WIDTH, (2 * atlas.row_of(last) - 1) * size)
    tiles: list[dict[str, Any]] = []
    for k in range(1, atlas.row_of(last) + 1):
        count = 2 * k - 1
        for index, n in enumerate(range((k - 1) ** 2 + 1, k * k + 1)):
            tiles.append(
                _tile(
                    n,
                    LEFT + canvas_width - count * size + index * size,
                    (k - 1) * (size + 18),
                    size,
                )
            )
    report = _report("triangle", per, [tile for tile in tiles if tile["n"] <= last])
    report["canvas"] = {**report["cells"], "right": LEFT + canvas_width, "width": canvas_width}
    return report


def _grid(last: int, per: int) -> dict[str, Any]:
    size = WIDTH / per
    tiles = [
        _tile(n, LEFT + ((n - 1) % per) * size, ((n - 1) // per) * (size + 12), size)
        for n in range(1, last + 1)
    ]
    return _report("grid", None, tiles)


def _moved(report: dict[str, Any], n: int, *, by: float = 0.0, down: float = 0.0) -> dict:
    """`report` with case `n`'s tile moved `by` pixels right and `down` pixels down."""
    tiles = [
        {
            **tile,
            "left": tile["left"] + by,
            "right": tile["right"] + by,
            "top": tile["top"] + down,
            "bottom": tile["bottom"] + down,
        }
        if tile["n"] == n
        else tile
        for tile in report["tiles"]
    ]
    return {**report, "tiles": tiles}


def test_a_case_is_in_the_row_of_the_next_perfect_square() -> None:
    known = {1: 1, 2: 2, 4: 2, 5: 3, 9: 3, 10: 4, 100: 10, 101: 11, 324: 18}
    assert {n: atlas.row_of(n) for n in known} == known
    for n in range(1, 2000):
        k = atlas.row_of(n)
        assert (k - 1) ** 2 < n <= k * k
    assert [n for n in range(1, 30) if atlas.is_square(n)] == [1, 4, 9, 16, 25]
    assert not atlas.is_square(0)
    with pytest.raises(ValueError, match="no case"):
        atlas.row_of(0)


def test_a_bound_row_is_complete_at_every_viewport_capacity() -> None:
    for per in range(1, 41):
        for k in range(1, 19):
            assert atlas.row_lines(k, per) == (2 * k - 1,)
    assert atlas.row_lines(10, 8) == (19,)
    assert atlas.row_lines(18, 26) == (35,)
    with pytest.raises(ValueError, match="no row"):
        atlas.row_lines(3, 0)


@pytest.mark.parametrize(("last", "per"), [(100, 19), (324, 35), (100, 8), (324, 8), (324, 26)])
def test_a_complete_right_aligned_triangle_has_no_problem(last: int, per: int) -> None:
    report = _triangle(last, per)
    assert atlas.layout_problems(report) == []
    found = atlas.summary(report)
    assert (found["view"], found["shown"], found["per_line"]) == ("triangle", last, per)
    assert found["wrapped"] == [
        k for k in range(1, atlas.row_of(last) + 1) if len(atlas.row_lines(k, per)) > 1
    ]


def test_a_right_grid_has_no_problem_and_reports_the_tiles_on_its_first_line() -> None:
    report = _grid(100, 10)
    assert atlas.layout_problems(report) == []
    found = atlas.summary(report)
    assert (found["per_line"], found["lines"], found["wrapped"]) == (10, 10, [])


def test_each_fault_of_a_layout_is_named() -> None:
    """Planted one at a time in a triangle that is otherwise right."""
    right = _triangle(100, 8)

    def problems(report: dict[str, Any]) -> str:
        return "; ".join(atlas.layout_problems(report))

    assert "past the window" in problems({**right, "overflow": 12})
    assert "still in a move" in problems({**right, "moving": 3})
    assert "outside the block: [100]" in problems(_moved(right, 100, by=300))
    assert "n = 99 runs over n = 100" in problems(_moved(right, 99, by=20))
    assert "row 9's line of n = 65 misses the right edge" in problems(_moved(right, 81, by=-4))
    assert "row 1's line of n = 1 misses the right edge" in problems(_moved(right, 1, by=4))
    # A whole logical row overlaps the one above it.
    over = right
    for n in range(82, 101):
        over = _moved(over, n, down=-30)
    assert "runs over the next" in problems(over)
    # A complete row is indented away from its common right endpoint.
    shifted = right
    for n in range(82, 101):
        shifted = _moved(shifted, n, by=-25)
    assert "row 10's line of n = 82 misses the right edge" in problems(shifted)
    # A row broken into a continuation violates the complete-row contract.
    broken = right
    for n in (98, 99, 100):
        broken = _moved(broken, n, down=100)
    assert "row 10 is set (16, 3), not (19,)" in problems(broken)
    swapped = [{**tile, "n": {5: 6, 6: 5}.get(tile["n"], tile["n"])} for tile in right["tiles"]]
    assert "out of order" in problems({**right, "tiles": swapped})
    assert atlas.layout_problems({**right, "tiles": []}) == ["no tile shows"]
    assert "no tiles to a line" in problems({**right, "per_line": None})


def test_a_grid_is_held_to_order_and_room_and_not_to_the_triangle() -> None:
    """The grid's squares are wherever its lines put them, which is no fault; a tile
    over another or outside the block is."""
    grid = _grid(100, 10)
    assert atlas.layout_problems(grid) == []
    assert "n = 4 runs over n = 5" in "; ".join(atlas.layout_problems(_moved(grid, 4, by=10)))
    assert "outside the block" in "; ".join(atlas.layout_problems(_moved(grid, 1, by=-30)))


def test_the_views_and_their_controls_are_named_one_way() -> None:
    assert atlas.query_for("grid") == "?atlas=grid"
    assert atlas.query_for("triangle") == ""
    assert atlas.query_for("grid", "large") == "?atlas=grid&size=large"
    assert atlas.query_for("triangle", "small") == ""
    assert atlas.query_for("triangle", "medium") == "?size=medium"
    assert atlas.query_for("triangle", "small", "row") == "?scale=row"
    assert atlas.query_for("grid", "large", "global") == "?atlas=grid&size=large&scale=global"
    with pytest.raises(ValueError, match="no scale"):
        atlas.query_for("grid", "small", "invalid")
    assert atlas.tab("triangle") == '[data-atlas-tab="triangle"]'
    assert atlas.size_tab("large") == '[data-atlas-size-tab="large"]'
    assert atlas.SIZES == ("small", "medium", "large")
    assert atlas.DEFAULT_SIZE in atlas.SIZES
    assert not hasattr(atlas, "LAYERS")
    for name in (atlas.query_for, atlas.tab):
        with pytest.raises(ValueError, match="no view"):
            name("pyramid")
    with pytest.raises(ValueError, match="no size"):
        atlas.size_tab("huge")
    with pytest.raises(ValueError, match="no size"):
        atlas.query_for("grid", "huge")
    # Every change `move` times is one a reader makes, and each is named once; a change
    # of size is timed in both views, and the page is put back at Medium after each.
    named = [change for change, _, _ in atlas.CHANGES if change is not None]
    assert len({(change, shown) for change, shown, _ in atlas.CHANGES if change}) == len(named)
    assert {shown for _, shown, _ in atlas.CHANGES} == {100, 324}
    sized = [change for change, _, press in atlas.CHANGES if change and "size-tab" in press]
    assert sized == [
        "grid, medium to large",
        "grid, large to small",
        "triangle, medium to large",
        "triangle, large to small",
    ]
    for index, (change, _, _) in enumerate(atlas.CHANGES):
        if change is not None and change.endswith("large to small"):
            assert atlas.CHANGES[index + 1] == (
                None,
                atlas.CHANGES[index][1],
                atlas.size_tab("medium"),
            )


def test_runs_are_reported_as_their_median_and_their_most_long_tasks() -> None:
    rows = [
        {"width": 1280, "change": "grid to triangle", "shown": 100, "run": run, **numbers}
        for run, numbers in enumerate(
            (
                {"handler_ms": 5.0, "frames": 22, "long_tasks": []},
                {"handler_ms": 9.0, "frames": 20, "long_tasks": [{"start": 1, "duration": 60}]},
                {"handler_ms": 6.0, "frames": 23, "long_tasks": []},
            )
        )
    ]
    assert atlas.medians(rows) == [
        {
            "width": 1280,
            "change": "grid to triangle",
            "shown": 100,
            "runs": 3,
            "handler_ms": 6.0,
            "frames": 22,
            "long_tasks": 1,
        }
    ]
    (least,) = atlas.medians(rows, best=True)
    assert (least["handler_ms"], least["frames"], least["long_tasks"]) == (5.0, 20, 1)
    table = atlas.markdown_table(atlas.medians(rows))
    assert table.splitlines()[0].startswith("| width | change | shown | runs | handler_ms |")
    assert "| 1280 | grid to triangle | 100 | 3 | 6.0 | 22 | 1 |" in table
    assert atlas.markdown_table([]) == ""
    assert "| none |" in atlas.markdown_table([{"wrapped": [], "problems": ["a", "b"]}])


def test_a_page_that_is_not_built_is_refused(tmp_path: Path) -> None:
    with pytest.raises(SystemExit, match="no built overview"):
        atlas.page_address(tmp_path, render=False)
    built = tmp_path / "index.html"
    built.write_text("<!doctype html>", encoding="utf-8")
    assert atlas.page_address(tmp_path, render=False) == built.resolve().as_uri()
    assert atlas.page_address(built, render=False) == built.resolve().as_uri()


#: The cases that carry a star, and the ones that carry the badge, in the planted layouts.
STARRED, BADGED = [5, 6, 7], [5, 8]


def _marked(report: dict[str, Any]) -> dict[str, Any]:
    """`report` with each tile's number centred under its drawing, a star just past the
    number of each starred case and a badge just before the number of each badged one."""
    tiles = []
    for tile in report["tiles"]:
        centre = (tile["left"] + tile["right"]) / 2
        number = {"left": centre - 6, "right": centre + 6, "top": tile["bottom"] - 10}
        number["bottom"] = tile["bottom"] - 2
        star = (
            {
                "left": number["right"] + 1,
                "right": number["right"] + 7,
                "top": tile["bottom"] - 9,
                "bottom": tile["bottom"] - 3,
                "width": 6,
                "height": 6,
            }
            if tile["n"] in STARRED
            else None
        )
        mark = (
            {
                "left": number["left"] - 6,
                "right": number["left"] - 2,
                "top": tile["bottom"] - 8,
                "bottom": tile["bottom"] - 4,
                "width": 4,
                "height": 4,
            }
            if tile["n"] in BADGED
            else None
        )
        tiles.append({**tile, "number_box": number, "star": star, "mark": mark})
    return {**report, "size": "medium", "tiles": tiles}


def _changed(report: dict[str, Any], n: int, **fields: Any) -> dict[str, Any]:
    tiles = [{**tile, **fields} if tile["n"] == n else tile for tile in report["tiles"]]
    return {**report, "tiles": tiles}


def test_each_fault_of_a_tiles_marks_is_named() -> None:
    """A right layout with its marks has no problem, in either view, and a report with
    no number's box is not asked about marks. Each fault is planted alone and must be
    named: a star or a badge with no size, over its number or outside its tile, and a
    number moved off its tile's centre."""
    assert atlas.layout_problems(_marked(_triangle(100, 8))) == []
    assert atlas.layout_problems(_marked(_grid(100, 10))) == []
    assert atlas.mark_problems(_grid(100, 10)) == []
    right = _marked(_grid(100, 10))

    def problems(report: dict[str, Any]) -> list[str]:
        return atlas.mark_problems(report)

    tile = next(tile for tile in right["tiles"] if tile["n"] == 5)
    star, badge, number = tile["star"], tile["mark"], tile["number_box"]
    assert problems(_changed(right, 5, star={**star, "width": 0})) == [
        "n = 5's star has no size"
    ]
    assert problems(_changed(right, 5, mark={**badge, "height": 0})) == [
        "n = 5's badge has no size"
    ]
    over = {**star, "left": star["left"] - 4, "right": star["right"] - 4}
    assert problems(_changed(right, 5, star=over)) == ["n = 5's star runs over its number"]
    over = {**badge, "left": badge["left"] + 4, "right": badge["right"] + 4}
    assert problems(_changed(right, 5, mark=over)) == ["n = 5's badge runs over its number"]
    out = {**star, "left": tile["right"] - 1, "right": tile["right"] + 5}
    assert problems(_changed(right, 5, star=out)) == ["n = 5's star stands outside its tile"]
    out = {**badge, "left": tile["left"] - 3, "right": tile["left"] + 1}
    assert problems(_changed(right, 5, mark=out)) == ["n = 5's badge stands outside its tile"]
    moved = {**number, "left": number["left"] - 4, "right": number["right"] - 4}
    assert problems(_changed(right, 6, number_box=moved)) == [
        "n = 6's number is off its tile's centre"
    ]
    found = atlas.summary(right)
    assert (found["size"], found["starred"], found["badged"]) == ("medium", 3, 2)


def test_complete_transition_rows_keep_the_half_drawing_gap() -> None:
    for per in (1, 2, 4, 6, 35):
        assert atlas.row_lines(3, per, 6) == (5,)
        assert atlas.row_lines(8, per, 56) == (15,)
    size = WIDTH / 6
    half_drawing = (size - 4) / 2
    left = LEFT + WIDTH - 5 * size - half_drawing
    tiles = [
        _tile(n, left + (n - 5) * size + (half_drawing if n >= 6 else 0), 0, size)
        for n in range(5, 10)
    ]
    report = _report("triangle", 6, tiles)
    report["gap_px"] = 0
    tiles[1]["grid_from"] = True
    assert atlas.layout_problems(report) == []
    # Scaling the drawing must not shrink the separator's reserved Fixed width.
    for tile in tiles:
        tile["drawing_slot_width"] = tile["drawing"]["width"]
        tile["drawing"]["width"] /= 3
    assert atlas.layout_problems(report) == []
    faults = atlas.layout_problems(_moved(report, 6, by=-10))
    assert any("gap before n = 6" in problem for problem in faults)


def test_a_panned_complete_grid_row_must_reach_its_canvas_right_edge() -> None:
    report = _triangle(100, 3)
    assert report["canvas"]["width"] > report["cells"]["width"]
    assert atlas.layout_problems(report) == []
    problems = atlas.layout_problems(_moved(report, 100, by=-10))
    assert any("misses the right edge" in problem for problem in problems)
