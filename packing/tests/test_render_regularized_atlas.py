"""The regularized views drawn by the house renderer, for the homepage's second layer.

`devtools.render_regularized_atlas` draws each view the layer's index lists to
`atlas/known-best/regularized/rendering/`. On a scratch tree of two records, one with a
view and one without, it is held to its contract: it draws what the index asks for and
nothing else, shades by the house rule on the view's pose, states the record's evidence
and not the view's, refuses a view or a witness the index's digests do not name, and its
check names a missing, stale or unexpected drawing. On the real tree the cheap halves
run here: the drawings kept are the index's set, and the smallest is what the renderer
draws now. The whole comparison is `--check`, a few seconds of rendering.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import re
from pathlib import Path
from typing import Any

import pytest

from devtools import render_frontier_page
from devtools import render_regularized_atlas as drawings
from devtools.build_known_best_atlas import frame_from_witness
from devtools.regularize_axis_components import ATLAS_CONTRACT
from sqpack.render import render_packing_svg
from sqpack.render.model import RenderSpec
from sqpack.witness import witness_document

UNIT = [("0", "0"), ("1", "0"), ("1", "1"), ("0", "1")]


def _moved(corners: list[tuple[str, str]], dx: str) -> list[tuple[str, str]]:
    return [(str(float(x) + float(dx)), y) for x, y in corners]


def _source() -> dict[str, Any]:
    """A decimal record of two squares on the floor of a 2.1 box, the second 0.05 clear
    of the first: four sides in contact between them, house rule."""
    return {
        "id": "W-pair",
        "n": 2,
        "side": "2.1",
        "square_size": "1",
        "representation": "corners",
        "scalar": {"kind": "decimal"},
        "coordinates": {"origin": "lower-left", "axes": "x-right-y-up"},
        "squares": [
            {"id": 1, "corners": [list(point) for point in UNIT]},
            {"id": 2, "corners": [list(point) for point in _moved(UNIT, "1.05")]},
        ],
        "claim": {
            "coordinate_provenance": "numerically-checked",
            "method": "numerical-multiprecision",
            "precision": {"decimal_digits": 120, "rounding": "nearest"},
            "tolerance": "1e-8",
            "limitations": "synthetic fixture",
        },
        "source": {"path": "tests/synthetic", "url": "https://example.invalid/pair"},
        "certificate": {"kind": "synthetic", "result": {"check_passed": True}},
    }


def _view() -> dict[str, Any]:
    """The record's regularized view: the second square slid into exact contact with the
    first, exactly, at the same side."""
    unit = [[x, y] for x, y in UNIT]
    return {
        "id": "W-pair-regularized",
        "n": 2,
        "side": "21/10",
        "square_size": "1",
        "representation": "corners",
        "scalar": {"kind": "rational"},
        "coordinates": {"origin": "lower-left", "axes": "x-right-y-up"},
        "squares": [
            {"id": 1, "corners": unit},
            {"id": 2, "corners": [[str(int(x) + 1), y] for x, y in unit]},
        ],
        "claim": {
            "coordinate_provenance": "verified",
            "method": "exact-algebraic",
            "limitations": "A regularized derived view for drawing, not the source witness.",
        },
        "certificate": {
            "kind": "regularized-view",
            "label": "regularized",
            "derived_from": "W-pair",
        },
    }


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def scratch(tmp_path: Path) -> drawings.Layout:
    """A record with a view (n = 2) and one the layer left unchanged (n = 3)."""
    packing = tmp_path / "packing"
    (packing / "w").mkdir(parents=True)
    regularized = packing / "regularized"
    regularized.mkdir()
    source = witness_document(_source()).encode()
    (packing / "w/n-002.yaml").write_bytes(source)
    view = witness_document(_view()).encode()
    (regularized / "n-002-regularized.yaml.gz").write_bytes(gzip.compress(view, mtime=0))
    index = {
        "contract": ATLAS_CONTRACT,
        "label": "regularized",
        "entries": [
            {
                "n": 2,
                "status": "regularized",
                "source": {
                    "witness": "packing/w/n-002.yaml",
                    "id": "W-pair",
                    "sha256": _digest(source),
                },
                "view": {
                    "path": "packing/regularized/n-002-regularized.yaml.gz",
                    "sha256": _digest(view),
                },
                "exact_verification": {"passed": True},
            },
            {"n": 3, "status": "unchanged"},
        ],
    }
    (regularized / "index.json").write_text(json.dumps(index), encoding="utf-8")
    return drawings.Layout(tmp_path, regularized / "index.json", regularized / "rendering")


def _contacts(svg: str) -> list[int]:
    return [int(count) for count in re.findall(r'data-contact-sides="(\d+)"', svg)]


def _metadata(svg: str, name: str) -> str:
    found = re.search(rf'<sqpack:value name="{name}">([^<]*)</sqpack:value>', svg)
    assert found is not None, name
    return found.group(1)


def test_it_draws_what_the_index_asks_for_and_checks_it(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    layout = scratch(tmp_path)
    assert drawings.main(["--update", "--workers", "1"], layout=layout) == 0
    assert sorted(path.name for path in layout.render_root.iterdir()) == ["n-002.svg"]
    assert drawings.main(["--check", "--workers", "1"], layout=layout) == 0
    assert "check passed: 1 regularized views drawn by the house renderer" in (
        capsys.readouterr().out
    )

    drawn = layout.rendering(2).read_text(encoding="utf-8")
    # The house rule on the view's pose: the slid square now shares a whole side with
    # its neighbour, so each counts one contact more than in the record's own pose.
    record = render_packing_svg(
        frame_from_witness(_source()), spec=RenderSpec(overlays=frozenset())
    )
    assert _contacts(record) == [2, 1]
    assert _contacts(drawn) == [3, 2]
    # It says what it is, and promotes nothing: the evidence is the record's.
    assert "Known-best packing of 2 unit squares, regularized</title>" in drawn
    assert "never the source witness" in drawn
    assert _metadata(drawn, "evidence") == "numerically-checked"
    assert _metadata(drawn, "evidence") == _metadata(record, "evidence")
    assert _metadata(drawn, "check-kind") == "numerical"
    assert _metadata(drawn, "source-id") == "W-pair-regularized"
    assert _metadata(drawn, "source-url") == "https://example.invalid/pair"


def test_its_check_names_a_missing_stale_or_unexpected_drawing(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    layout = scratch(tmp_path)
    assert drawings.problems(layout) == ["packing/regularized/rendering/n-002.svg is missing"]
    assert drawings.main(["--check", "--workers", "1"], layout=layout) == 1
    assert "regularized renderings drift" in capsys.readouterr().out

    drawings.update(layout)
    target = layout.rendering(2)
    target.write_text(target.read_text(encoding="utf-8") + " ", encoding="utf-8")
    (layout.render_root / "n-003.svg").write_text("", encoding="utf-8")
    assert drawings.problems(layout) == [
        "packing/regularized/rendering/n-002.svg is stale",
        "unexpected packing/regularized/rendering/n-003.svg",
    ]
    drawings.update(layout)
    assert drawings.problems(layout) == []
    assert sorted(path.name for path in layout.render_root.iterdir()) == ["n-002.svg"]


def test_it_refuses_a_view_the_index_does_not_vouch_for(tmp_path: Path) -> None:
    """The index's digests say which witness a view came from and which bytes its verdict
    is for, so a changed witness, a changed view, or an index under another label is
    refused rather than drawn."""
    layout = scratch(tmp_path)
    index = json.loads(layout.index.read_text(encoding="utf-8"))

    view = layout.repo / index["entries"][0]["view"]["path"]
    retained = view.read_bytes()
    edited = gzip.decompress(retained).replace(b"W-pair-regularized", b"W-pair-tidied")
    view.write_bytes(gzip.compress(edited, mtime=0))
    with pytest.raises(SystemExit, match="differs from the view its verdict is for"):
        drawings.update(layout)
    view.write_bytes(retained)

    source = layout.repo / index["entries"][0]["source"]["witness"]
    source.write_text(source.read_text(encoding="utf-8") + "# touched\n", encoding="utf-8")
    with pytest.raises(SystemExit, match=r"changed since its view was derived \(stale\)"):
        drawings.update(layout)

    layout.index.write_text(json.dumps({**index, "label": "tidied"}), encoding="utf-8")
    with pytest.raises(SystemExit, match="labels its drawings 'tidied'"):
        drawings.regularized_entries(layout)
    assert not layout.render_root.exists()


def test_the_homepage_reads_the_drawings_where_this_writes_them() -> None:
    assert drawings.INDEX == render_frontier_page.REGULARIZED_INDEX
    assert drawings.RENDER_ROOT == render_frontier_page.REGULARIZED_RENDERINGS


def test_the_committed_drawings_are_the_index_set_and_the_smallest_is_current() -> None:
    """The cheap halves of `--check` on the real tree: the drawings kept are exactly the
    ones the index asks for, and the smallest is byte for byte what the renderer draws
    now, with the record's evidence beside its house drawing's."""
    entries = drawings.regularized_entries()
    assert entries, "the layer has no regularized view"
    kept = sorted(path.name for path in drawings.RENDER_ROOT.iterdir())
    assert kept == [f"n-{entry['n']:03d}.svg" for entry in entries]
    smallest = min(entries, key=lambda entry: entry["n"])
    n = smallest["n"]
    drawn = drawings.render(smallest)
    assert drawings.RENDER_ROOT.joinpath(f"n-{n:03d}.svg").read_text(encoding="utf-8") == drawn
    house = render_frontier_page.RENDERINGS.joinpath(f"n-{n:03d}.svg").read_text(
        encoding="utf-8"
    )
    assert _metadata(drawn, "evidence") == _metadata(house, "evidence")
    assert drawn != house
