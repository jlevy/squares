"""`devtools.measure_core`: a smaller packing placed in a larger box, square by square."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

from devtools import measure_core as core

PACKET = "ozden-s179-issue959-2026-11-11"
CORE = core.reports.ROOT / "witnesses/known-best/n-070.yaml"


def _placed(side: float, rows: list[tuple[float, float, float]]) -> core.Placed:
    return core.Placed(
        side, np.array([[x, y] for x, y, _t in rows]), np.array([t for _x, _y, t in rows])
    )


def test_fold_takes_angles_modulo_a_quarter_turn_to_the_half_open_interval() -> None:
    folded = core.fold(np.array([0.0, 45.0, 46.0, -40.0, 90.0, 130.0]))
    assert folded.tolist() == [0.0, 45.0, -44.0, -40.0, 0.0, 40.0]


def test_the_eight_symmetries_keep_the_box_and_reflections_turn_the_tilt_over() -> None:
    packing = _placed(3.0, [(0.5, 0.5, 10.0), (2.5, 1.5, -20.0)])
    images = {name: core.transform(packing, name) for name in core.SYMMETRIES}
    assert len({tuple(image.xy.ravel()) for image in images.values()}) == 8
    for name, image in images.items():
        assert np.all((image.xy > 0) & (image.xy < 3))
        flipped = name.startswith("reflect")
        expected = [-10.0, 20.0] if flipped else [10.0, -20.0]
        assert image.tilt.tolist() == expected


def test_a_border_by_l_steps_adds_its_width_times_twice_the_floor_plus_the_width() -> None:
    assert core.l_border(Fraction(8880960371555579595, 10**18), 1) == 17
    assert core.l_border(Fraction(8880960371555579595, 10**18), 5) == 105
    assert core.l_border(Fraction(3), 2) == 16


def test_a_core_laid_at_both_ends_of_the_diagonal_matches_every_square_of_its_copy() -> None:
    small = _placed(2.0, [(0.5, 0.5, 0.0), (1.5, 1.5, 30.0)])
    view = _placed(4.0, [(0.5, 0.5, 0.0), (1.5, 1.5, 30.0), (2.5, 2.5, 0.0), (3.5, 3.5, 30.0)])
    diagonal = core.diagonal_matches(view, small, tilted=False)
    assert diagonal["best_symmetry"] == "identity"
    assert diagonal["symmetries"][0]["matched"]["1e-9"] == 4
    band = core.diagonal_matches(view, small, tilted=True)
    assert (band["view_squares"], band["core_squares"]) == (2, 1)
    assert band["by_shift"]["0"]["1e-9"] == 1
    assert band["by_shift"]["2"]["1e-9"] == 1
    corners = core.core_matches(view, small)
    assert corners["best"]["1e-9"] == 2


def test_the_receipt_of_959_against_the_70_places_the_band_ends_exactly() -> None:
    record = core.receipt(f"#959=packet:{PACKET}", 179, CORE, 70)
    assert record["inputs"]["core"]["scalar"] == "algebraic-number-field"
    assert record["side"]["plus"][5]["excess"].startswith("2.645")
    assert record["band"]["best_symmetry"] == "identity"
    assert record["band"]["symmetries"][0]["matched"]["1e-9"] == 15
    retained = core.reports.packet_path(PACKET) / "measure/core-n070.json"
    assert retained.exists()
    assert json.loads(retained.read_text(encoding="utf-8")) == record


def test_a_core_at_least_as_large_as_the_view_is_refused(tmp_path: Path) -> None:
    with pytest.raises(core.CoreError):
        core.receipt(f"packet:{PACKET}", 179, CORE, 179)
    with pytest.raises(core.CoreError):
        core.read_core(tmp_path / "missing.yaml", 70)
