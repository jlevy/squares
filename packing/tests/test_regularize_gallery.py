"""The reviewer's gallery of a regularization run, drawn by the house renderer.

`devtools.regularize_gallery` reads a run directory in the driver's layout and writes one
page. Here a synthetic run is built in a scratch directory from the atlas's n = 26 witness
and the current layer's n = 26 view, which is a same-side view of it, with a hand-written
report in the driver's shape. The page is held to the published-page contract (a title
and stylesheet first, no document skeleton, no script, every colour a token with both dark
blocks), to its anchors and panels, and to its measurements, which are checked against the
renderer's own colour assignment rather than against the page's reading of it. The
report's fields are shown as recorded, and a report that disagrees with the drawings is
flagged. The matching that outlines moved squares is checked on a two-square packing, and
the current-layer mode and the page-size refusal on the real layer.
"""

from __future__ import annotations

import gzip
import json
import re
from pathlib import Path
from typing import Any

import pytest

from devtools import regularize_gallery as gallery
from devtools.build_known_best_atlas import frame_from_witness
from devtools.regularize_axis_components import histogram
from sqpack.render import render_packing_svg
from sqpack.render.color import assign_square_colors
from sqpack.render.model import RenderSpec

REPO = Path(__file__).resolve().parents[2]
SOURCE = "packing/witnesses/known-best/n-026.yaml"
LAYER_VIEW = REPO / "packing/atlas/known-best/regularized/n-026-regularized.yaml.gz"
INDEX = REPO / "packing/atlas/known-best/regularized/index.json"
SPEC = RenderSpec(overlays=frozenset())
LEVEL_TEXT = "only free squares touched"
REASON = "same side, one to one, every move within 1/2, no regression"


def _witness(path: Path) -> dict[str, Any]:
    return gallery.read_witness(path)


def _colours(witness: dict[str, Any]) -> list[Any]:
    """The renderer's own colour assignment, read independently of the page."""
    return list(assign_square_colors(frame_from_witness(witness), SPEC).values())


def _measures(witness: dict[str, Any]) -> tuple[int, int, list[int]]:
    colours = _colours(witness)
    contacts = [colour.contact_sides for colour in colours]
    classes = len({colour.angle_class for colour in colours})
    return classes, contacts.count(4), histogram(contacts)


def _report(**changes: Any) -> dict[str, Any]:
    """A report in the driver's shape whose measurements agree with the drawings."""
    _, _, before = _measures(_witness(REPO / SOURCE))
    _, _, after = _measures(_witness(LAYER_VIEW))
    report: dict[str, Any] = {
        "n": 26,
        "source": {
            "path": SOURCE,
            "kind": "decimal",
            "s_W": "5.62132034355964257320253308632",
        },
        "verified_upper_bound": "5.62132034355964257320253308632",
        "generator": {
            "name": "evand-regularize",
            "pin": "675a5ea",
            "patches": [],
            "variant": "conservative",
            "style": "coincide",
            "orient": 0,
        },
        "solve": {"status": "certified", "cert_valid": True, "free": [8], "seconds": 0.4},
        "regularize": {
            "level": 1,
            "level_text": LEVEL_TEXT,
            "moved": [8],
            "max_move": 0.3107,
            "symmetry": [],
            "groups_before": 2,
            "groups_after": 2,
            "merged": [],
            "angle_changes": [],
            "seconds": 0.8,
        },
        "outputs": {
            "solved": None,
            "same": {
                "path": "view-same.yaml",
                "side": "5.62132034355964257320253308632",
                "relation": "same",
                "routes": {"exact_verify": True, "independent": True},
            },
            "same_refusal": None,
        },
        "identity": {
            "basis": "measured",
            "measured_in": "devtools.check_half_angle_area.arrangement_gap",
            "of": "same",
            "one_to_one": True,
            "moved": 1,
            "max_move": "3.107e-01",
            "max_turn_deg": "0",
            "symmetry": 0,
        },
        "shades": {
            "of": "same",
            "house": {"before": before, "after": after},
            "stage": {"before": before, "after": after},
            "regressions": [],
        },
        "decision": {
            "row": 10,
            "decision": "admit",
            "index_record": "regularized",
            "reason": REASON,
        },
        "status": "ok",
        "error": None,
    }
    return report | changes


def _run(tmp_path: Path, report: dict[str, Any], *, view: bool = True) -> Path:
    """A run directory holding one count, n = 26, as the driver lays it out."""
    run = tmp_path / "run"
    count = run / "n-026"
    count.mkdir(parents=True)
    (count / "report.json").write_text(json.dumps(report), encoding="utf-8")
    if view:
        (count / "view-same.yaml").write_bytes(gzip.decompress(LAYER_VIEW.read_bytes()))
    receipt = {
        "generator": {"name": "evand-regularize", "pin": "675a5ea", "patches": []},
        "cost": {"cpu_seconds": 1.2, "wall_seconds": 1.4},
    }
    (run / "receipt.json").write_text(json.dumps(receipt), encoding="utf-8")
    return run


def _section(page: str, n: int) -> str:
    start = page.index(f'<section class="count" id="n-{n:03d}"')
    return page[start : page.index("</section>", start)]


def _pair(witness_id: str, lefts: tuple[str, str]) -> dict[str, Any]:
    """A decimal record of two unit squares on the floor of a 2.1 box."""
    return {
        "id": witness_id,
        "n": 2,
        "side": "2.1",
        "square_size": "1",
        "representation": "corners",
        "scalar": {"kind": "decimal"},
        "coordinates": {
            "origin": "lower-left",
            "axes": "x-right-y-up",
            "angle_unit": "not-applicable",
        },
        "squares": [
            {
                "id": index,
                "corners": [
                    [left, "0"],
                    [str(float(left) + 1), "0"],
                    [str(float(left) + 1), "1"],
                    [left, "1"],
                ],
            }
            for index, left in enumerate(lefts, start=1)
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


def test_run_page_keeps_the_published_page_contract(tmp_path: Path) -> None:
    run = _run(tmp_path, _report())
    output = tmp_path / "gallery.html"
    code = gallery.main(
        ["--run-dir", str(run), "--output", str(output), "--with-current-layer"]
    )
    assert code == 0
    page = output.read_text(encoding="utf-8")
    assert page.startswith(f"<title>{gallery.DEFAULT_TITLE}</title>\n<style>")
    assert re.search(r"<(?:!doctype|html|head|body)\b", page, re.IGNORECASE) is None
    assert "<script" not in page.lower()
    assert "@media (prefers-color-scheme: dark)" in page
    assert ':root:not([data-theme="light"])' in page
    assert ':root[data-theme="dark"]' in page
    assert "background: var(--bg)" in page
    assert "font-variant-numeric: tabular-nums" in page
    assert 'href="#n-026"' in page
    assert len(page.encode("utf-8")) < gallery.PAGE_LIMIT


def test_run_page_draws_three_panels_and_its_measurements(tmp_path: Path) -> None:
    run = _run(tmp_path, _report())
    output = tmp_path / "gallery.html"
    gallery.main(["--run-dir", str(run), "--output", str(output), "--with-current-layer"])
    page = output.read_text(encoding="utf-8")
    section = _section(page, 26)
    assert section.count('<svg class="drawing"') == 3
    for heading in ("Source", "Regularized, same", "Current layer"):
        assert f'<span class="role">{heading}</span>' in section

    before_classes, before_dark, before_houses = _measures(_witness(REPO / SOURCE))
    after_classes, after_dark, after_houses = _measures(_witness(LAYER_VIEW))
    summary = page[page.index('<table class="summary">') : page.index("</table>")]
    assert f"{before_classes} → {after_classes}" in summary
    assert f"{before_dark} → {after_dark}" in summary
    assert '<td class="num">1</td>' in summary
    for counts in (before_houses, after_houses):
        cells = "".join(f"<span>{count}</span>" for count in counts)
        assert cells in section

    entry = next(
        entry
        for entry in json.loads(INDEX.read_text(encoding="utf-8"))["entries"]
        if entry["n"] == 26
    )
    # The axis tool's record of the count: the entry itself, or under a v2 entry whose
    # view another generator made, its `reference`.
    largest = (entry.get("moves") or entry["reference"]["moves"])["largest_move_decimal"]
    assert f"1 moved, 0 turned; largest {largest}, 0°; symmetry 0" in section
    assert f"s {gallery.MINUS} s_W = 0" in section
    assert section.count('<path class="mark"') == 3
    assert "chip-admit" in section
    assert "row 10" in section
    assert LEVEL_TEXT in section
    assert REASON in section
    assert "evand-regularize at 675a5ea" in section
    assert "agrees" in section
    assert 'class="flag"' not in section


def test_a_report_that_disagrees_with_the_drawings_is_flagged(tmp_path: Path) -> None:
    report = _report()
    report["source"]["s_W"] = "5.62"
    report["identity"] |= {"moved": 3, "symmetry": 2}
    report["shades"]["house"]["after"] = [0, 0, 0, 0, 26]
    run = _run(tmp_path, report)
    case = gallery.run_case(run / "n-026", None)
    section = _section(gallery.render_page([case], title="Gallery", source="run"), 26)
    assert "has changed since the run" in section
    assert "The drawings disagree on moved (1 measured here), symmetry (0 measured here)" in (
        section
    )
    assert "house histograms differ from the drawings" in section


def test_a_failed_count_draws_its_source_alone(tmp_path: Path) -> None:
    decision = {"row": 1, "decision": "no-view", "index_record": None, "reason": "timeout"}
    run = _run(tmp_path, _report(status="timeout", decision=decision), view=False)
    case = gallery.run_case(run / "n-026", None)
    page = gallery.render_page([case], title="Gallery", source="run")
    section = _section(page, 26)
    assert section.count('<svg class="drawing"') == 1
    # A count with no view is neutral, never red: nothing was refused (owner, 11 October).
    assert '<span class="chip chip-unchanged">no view</span>' in section
    assert "chip-refuse" not in section
    assert "no view drawn" in section


def test_a_view_the_report_does_not_name_is_an_earlier_runs_and_is_not_drawn(
    tmp_path: Path,
) -> None:
    decision = {"row": 1, "decision": "no-view", "index_record": None, "reason": "timeout"}
    outputs = {"solved": None, "same": None, "same_refusal": None}
    report = _report(status="timeout", decision=decision, outputs=outputs)
    run = _run(tmp_path, report)
    case = gallery.run_case(run / "n-026", None)
    section = _section(gallery.render_page([case], title="Gallery", source="run"), 26)
    assert section.count('<svg class="drawing"') == 1
    assert '<span class="chip chip-unchanged">no view</span>' in section
    assert "no view drawn" in section
    assert "view-same.yaml is on disk but the report records no same output" in section


def test_a_same_side_view_set_aside_above_the_bound_is_named_as_this_runs(
    tmp_path: Path,
) -> None:
    """`yield_to_bound` keeps the same-side view's file and its block under
    `same_above_bound`: it is this run's view, set aside, not an earlier run's (#580
    review A5)."""
    same = _report()["outputs"]["same"]
    outputs = {"solved": None, "same": None, "same_above_bound": same, "same_refusal": None}
    run = _run(tmp_path, _report(outputs=outputs))
    case = gallery.run_case(run / "n-026", None)
    named = (
        "view-same.yaml is this run's same-side view, set aside: the witness's side is "
        "above U, so the view at the bound is decided and drawn."
    )
    assert [note for note in case.notes if "view-same.yaml" in note] == [named]
    section = _section(gallery.render_page([case], title="Gallery", source="run"), 26)
    assert section.count('<svg class="drawing"') == 1
    assert "set aside: the witness" in section
    assert "earlier run" not in section


@pytest.mark.parametrize(
    ("decision", "text", "tone"),
    [
        ("admit", "admitted", "admit"),
        ("no-change", "no change", "unchanged"),
        ("held", "held", "candidate"),
        ("refuse", "refused", "refuse"),
        ("candidate", "held", "candidate"),
        ("unchanged", "no change", "unchanged"),
    ],
)
def test_each_reported_decision_reads_as_its_chip(decision: str, text: str, tone: str) -> None:
    assert gallery.DECISION_CHIPS[decision] == (text, tone)


def test_moves_are_matched_under_the_best_box_symmetry() -> None:
    source = frame_from_witness(_pair("W-pair", ("0", "1.05")))
    slid = frame_from_witness(_pair("W-pair-slid", ("0", "1")))
    motion = gallery.square_motions(source, slid)
    assert motion is not None
    assert motion.symmetry == 0
    assert motion.partner == (0, 1)
    assert motion.moved() == [1]
    assert motion.move[1] == pytest.approx(0.05)
    assert motion.turned() == []

    mirrored = frame_from_witness(_pair("W-pair-mirrored", ("0.05", "1.1")))
    motion = gallery.square_motions(source, mirrored)
    assert motion is not None
    assert motion.symmetry == 4
    assert motion.partner == (1, 0)
    assert motion.moved() == []


def test_the_reduced_drawing_keeps_the_renderers_fills() -> None:
    witness = _witness(REPO / SOURCE)
    drawing = gallery.read_house_svg(render_packing_svg(frame_from_witness(witness), spec=SPEC))
    fills = [colour.fill for colour in _colours(witness)]
    assert [square.fill for square in drawing.squares] == fills
    fine = gallery.drawing_svg(drawing, ident="t", label="test", decimals=2)
    coarse = gallery.drawing_svg(
        drawing, ident="t", label="test", decimals=1, marked=["square-009"]
    )
    assert fine.count("Z") == 26
    assert len(coarse) < len(fine) + 200
    assert re.search(r"\d\.\d\d\d", fine) is None
    assert coarse.count('class="mark"') == 1
    assert sorted(set(re.findall(r'fill="(#[0-9a-f]{6})"', fine))) == sorted(
        set(fills) | {drawing.paper}
    )


def test_the_current_layer_mode_draws_source_against_layer(tmp_path: Path) -> None:
    output = tmp_path / "layer.html"
    code = gallery.main(["--current-layer", "--n", "26", "--output", str(output)])
    assert code == 0
    page = output.read_text(encoding="utf-8")
    section = _section(page, 26)
    assert section.count('<svg class="drawing"') == 2
    assert '<span class="chip chip-admit">in layer</span>' in section
    assert "<td>same</td>" in page


def test_a_page_over_the_limit_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(gallery, "PAGE_LIMIT", 1000)
    output = tmp_path / "layer.html"
    code = gallery.main(["--current-layer", "--n", "26", "--output", str(output)])
    assert code == 2
    assert not output.exists()
