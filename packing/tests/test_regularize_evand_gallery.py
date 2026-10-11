"""The review gallery is built from a run's summary, its drawings and optional notes."""

from __future__ import annotations

import json
from pathlib import Path

from devtools import regularize_evand_gallery as gallery


def _row(n: int, report: str, *, row: int, register: bool = False) -> dict[str, object]:
    return {
        "n": n,
        "scalar_kind": "rational",
        "project_layer": {"status": "unchanged"},
        "timings": {
            "exact_solve": {"wall": 2.0, "cpu": 2.0},
            "regularize_conservative": {"wall": 1.0, "cpu": 1.0},
            "import_conservative": {"wall": 0.5, "cpu": 0.5},
            "render": None,
        },
        "variants": {
            "conservative": {
                "policy": {"report": report, "row": row, "register_candidate": register},
                "identity": {"one_to_one": True, "max_move": 0.25, "max_turn_degrees": 0.0},
                "shades": {"house": {"light_before": 7, "light_after": 5}},
                "same_side": {"status": "same"},
            }
        },
    }


def _summary() -> dict[str, object]:
    return {
        "tool": "devtools.regularize_evand",
        "pin": {"revision": "675a5ea"},
        "rows": [
            _row(30, "no change", row=5),
            _row(12, "admitted", row=10),
            _row(20, "held", row=3, register=True),
        ],
    }


def test_counts_are_grouped_by_reported_decision_in_policy_order(tmp_path: Path) -> None:
    page = gallery.build(_summary(), tmp_path, {})
    admitted, held, flat = (
        page.index(f'id="{key}"') for key in ("admitted", "held", "no-change")
    )
    assert admitted < held < flat
    assert "<b>1</b> admitted" in page
    assert "<b>1</b> held" in page
    assert "675a5ea" in page
    assert "<script" not in page
    assert "{{" not in page


def test_notes_pilot_and_decisions_appear_escaped(tmp_path: Path) -> None:
    notes = {
        "title": "Spikes <3",
        "pilot": [12],
        "decisions": ["Approve n = 12?"],
        "notes": {12: "moves one square & keeps contacts"},
    }
    page = gallery.build(_summary(), tmp_path, notes)
    assert "<title>Spikes &lt;3</title>" in page
    assert "moves one square &amp; keeps contacts" in page
    assert "Approve n = 12?" in page
    assert page.count('class="pilot"') == 2  # the table row and the card


def test_drawings_are_inlined_and_made_scalable(tmp_path: Path) -> None:
    (tmp_path / "n-012-compare.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="300" height="200" '
        'viewBox="0 0 300 200">'
        "<rect width='10' height='10' fill='#000'/></svg>",
        encoding="utf-8",
    )
    page = gallery.build(_summary(), tmp_path, {})
    assert 'viewBox="0 0 300 200"' in page
    assert 'width="300" height="200"' not in page


def test_measured_cost_sums_each_stage(tmp_path: Path) -> None:
    page = gallery.build(_summary(), tmp_path, {"effort": "About 3 h for all counts."})
    assert "About 3 h for all counts." in page
    assert '<td class="num">6 s</td>' in page  # exact solve, 3 counts x 2 s
    assert '<td class="num"><b>10 s</b></td>' in page


def test_the_command_line_writes_the_page(tmp_path: Path) -> None:
    (tmp_path / "summary.json").write_text(json.dumps(_summary()), encoding="utf-8")
    out = tmp_path / "gallery.html"
    assert gallery.main(["--render", str(tmp_path), "--out", str(out)]) == 0
    assert out.read_text(encoding="utf-8").startswith("<title>")
