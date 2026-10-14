"""The drawing-regularity census on fixtures whose shading is known by hand.

A 2 x 2 grid filling a side-2 box draws four dark squares. The same squares in a box
`0.1` wider, staggered, leave light squares whose open faces are slack or misalignment,
which the census counts as uneven. A square turned a fifth of a degree is a near-axis
square, its own hue. On a scratch tree the census draws a count from the layer's view
where the index says `regularized` and from the witness otherwise, and the comparison
ranks the worst first. One real record (n = 10) checks the counts add up.
"""

from __future__ import annotations

import gzip
import json
from pathlib import Path
from typing import Any

from devtools import census_drawing_regularity as census
from devtools import regularize_axis_components as axis
from sqpack.witness import witness_document

UNIT = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]


def _square(index: int, x: float, y: float) -> dict[str, Any]:
    return {"id": index, "corners": [[str(x + a), str(y + b)] for a, b in UNIT]}


def _decimal(
    squares: list[dict[str, Any]], side: str, *, name: str = "fixture"
) -> dict[str, Any]:
    """A decimal corners witness, numerically checked by fiat."""
    return {
        "id": f"W-{name}",
        "n": len(squares),
        "side": side,
        "square_size": "1",
        "representation": "corners",
        "scalar": {"kind": "decimal"},
        "coordinates": {
            "origin": "lower-left",
            "axes": "x-right-y-up",
            "angle_unit": "not-applicable",
        },
        "squares": squares,
        "claim": {
            "coordinate_provenance": "numerically-checked",
            "method": "numerical-multiprecision",
            "precision": {"decimal_digits": 120, "rounding": "nearest"},
            "tolerance": "1e-8",
            "limitations": "synthetic fixture",
        },
        "source": {"path": "tests/synthetic", "url": "https://example.invalid/fixture"},
        "certificate": {"kind": "synthetic", "result": {"check_passed": True}},
    }


def _centre_angle(rows: list[tuple[str, str, str]], side: str) -> dict[str, Any]:
    witness = _decimal([], side, name="tilt")
    witness["representation"] = "center-angle"
    witness["coordinates"]["angle_unit"] = "degrees"
    witness["squares"] = [
        {"id": index, "center": [x, y], "angle": angle}
        for index, (x, y, angle) in enumerate(rows, start=1)
    ]
    witness["n"] = len(rows)
    return witness


def grid() -> dict[str, Any]:
    return _decimal(
        [_square(1, 0, 0), _square(2, 1, 0), _square(3, 0, 1), _square(4, 1, 1)], "2"
    )


def staggered() -> dict[str, Any]:
    """Bottom row flush left, top row flush right: every vertical side misses by 0.1."""
    return _decimal(
        [_square(1, 0, 0), _square(2, 1, 0), _square(3, 0.1, 1.1), _square(4, 1.1, 1.1)],
        "2.1",
    )


def test_a_full_grid_is_dark_and_even() -> None:
    measured = census.regularity(grid())
    assert measured["axis"] == 4
    assert measured["axis_sides"] == [0, 0, 0, 0, 4]
    assert measured["light_axis"] == 0
    assert measured["uneven_axis"] == 0
    assert measured["near_axis"] == 0
    assert measured["variation"] == 0
    assert measured["classes"] == 1


def test_slack_and_misalignment_are_uneven_and_light() -> None:
    measured = census.regularity(staggered())
    # Squares 1 and 4 keep two walls and their row partner; 2 and 3 keep one wall each
    # and their row partner: no vertical side is shared whole.
    assert measured["axis_sides"] == [0, 0, 2, 2, 0]
    assert measured["light_axis"] == 0
    assert measured["uneven_axis"] == 4
    # The rows' vertical faces miss by 0.1 across and along: slack or a staggered row,
    # never a cause the grid could not remove by moving.
    assert set(measured["open_faces"]) <= census.SOFT
    assert sum(measured["open_faces"].values()) == 6
    lone = _decimal([_square(1, 0.4, 0.5)], "2", name="lone")
    alone = census.regularity(lone)
    assert alone["light_axis"] == 1
    # Its right face is 0.6 from the wall: more than half a side, an open region.
    assert alone["light_faces"] == {"hole-or-open": 1, "slack": 3}
    assert alone["uneven_axis"] == 1


def test_a_square_a_fifth_of_a_degree_off_is_near_axis() -> None:
    witness = _centre_angle(
        [("0.5", "0.5", "0"), ("1.5", "0.5", "0"), ("1.5", "1.6", "0.2")], "2.2"
    )
    measured = census.regularity(witness)
    assert measured["axis"] == 2
    assert measured["near_axis"] == 1
    assert measured["near_axis_degrees"] == [0.2]
    assert measured["near_axis_classes"] == 1
    assert measured["classes"] == 2
    assert measured["variation"] >= 1


def scratch_tree(tmp_path: Path) -> Path:
    """n = 4 drawn from a view the index lists; n = 1 from its witness."""
    known = tmp_path / "packing/witnesses/known-best"
    known.mkdir(parents=True)
    (known / "n-004.yaml").write_text(witness_document(staggered()), encoding="utf-8")
    one = _decimal([_square(1, 0, 0)], "1", name="one")
    (known / "n-001.yaml").write_text(witness_document(one), encoding="utf-8")
    layer = tmp_path / "packing/atlas/known-best/regularized"
    layer.mkdir(parents=True)
    view = witness_document(grid() | {"side": "2"}).encode()
    (layer / "n-004-regularized.yaml.gz").write_bytes(gzip.compress(view, mtime=0))
    index = {
        "entries": [
            {"n": 1, "status": "unchanged"},
            {
                "n": 4,
                "status": "regularized",
                "generator": axis.EVAND_GENERATOR,
                "view": {
                    "path": "packing/atlas/known-best/regularized/n-004-regularized.yaml.gz"
                },
            },
        ]
    }
    (layer / "index.json").write_text(json.dumps(index), encoding="utf-8")
    return tmp_path


def test_the_tree_decides_what_is_drawn(tmp_path: Path) -> None:
    tree = scratch_tree(tmp_path)
    document = census.census(tree, [1, 4])
    first, fourth = document["counts"]
    assert first["drawing"]["kind"] == "witness"
    assert first["drawing"]["path"] == "packing/witnesses/known-best/n-001.yaml"
    assert fourth["drawing"]["kind"] == "regularized-view"
    assert fourth["uneven_axis"] == 0
    assert document["totals"]["drawn_from_views"] == 1
    assert document["totals"]["axis_sides"] == [0, 0, 0, 0, 5]
    bare = tmp_path / "bare"
    (bare / "packing/witnesses").mkdir(parents=True)
    (bare / "packing/witnesses/known-best").symlink_to(
        tmp_path / "packing/witnesses/known-best"
    )
    before = census.census(bare, [1, 4])
    assert before["counts"][1]["drawing"]["kind"] == "witness"
    assert before["counts"][1]["uneven_axis"] == 4
    rows = census.compare(before, document)
    assert [row["n"] for row in rows] == [4, 1] or [row["n"] for row in rows] == [1, 4]
    assert next(row for row in rows if row["n"] == 4)["change"] == -4
    table = census.ranking_markdown(rows, top=5)
    assert "| 4 | witness | 0 / 4 / 4 | 0 | Evan view | 0 / 0 / 4 | 0 | 0 | -4 |" in table


def test_a_view_is_labelled_by_its_generator() -> None:
    def drawn(generator: str | None) -> dict[str, Any]:
        return {"kind": "regularized-view", "generator": generator}

    assert census.source_label({"kind": "witness"}) == "witness"
    assert census.source_label(drawn(axis.EVAND_GENERATOR)) == "Evan view"
    for grid in axis.GRID_GENERATORS:
        assert census.source_label(drawn(grid)) == "grid view"
    assert census.source_label(drawn(axis.ALGORITHM)) == "axis view"
    assert census.source_label(drawn(None)) == "axis view"
    # An older tree's index, and a census written from one, name the driver's command.
    assert census.source_label(drawn("python -m devtools.regularize_evand run")) == "Evan view"
    assert (
        census.source_label(drawn("devtools.regularize_grid_slack (prototype)")) == "grid view"
    )


def test_the_cli_writes_its_census(tmp_path: Path) -> None:
    tree = scratch_tree(tmp_path)
    output = tmp_path / "out/census.json"
    assert census.main(["--tree", str(tree), "--n", "4", "--output", str(output)]) == 0
    written = json.loads(output.read_text(encoding="utf-8"))
    assert written["format"] == census.FORMAT
    assert written["counts"][0]["n"] == 4


def test_a_real_record_adds_up() -> None:
    document = census.census(census.REPO, [10])
    row = document["counts"][0]
    assert row["squares"] == 10
    assert sum(row["axis_sides"]) == row["axis"]
    assert row["light_axis"] <= row["axis"]
    assert row["uneven_axis"] <= row["axis"]
