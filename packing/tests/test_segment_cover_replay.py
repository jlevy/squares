"""The retained exact cover, its known escape, and incomplete-proof refusals."""

from __future__ import annotations

import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

from devtools.segment_cover_replay import (
    DELTA,
    exact_certify_leaf,
    exact_discard_box,
    exact_escape,
    exact_square_segment_dist2,
    replay,
)

PACKING = Path(__file__).resolve().parents[1]


def test_retained_e4_cover_rechecks_every_leaf_and_discard() -> None:
    for sharper in (False, True):
        result = replay(sharper=sharper)
        assert result["status"] == "certified"
        assert result["proved"] is True
        assert result["nodes"] == 24381
        assert result["certified"] == 10960
        assert result["discarded"] == 1231
        assert result["failures"] == 0
        assert result["exact_rejected_leaves"] == 0
        assert result["exact_rejected_discards"] == 0
        assert result["volume"] == "243/128"
        assert result["volume_ok"] is True


def test_exact_geometry_keeps_the_recorded_escape_and_segment_crossing() -> None:
    pose = (Fraction(384507, 1048576), Fraction(156707, 65536), Fraction(46211, 65536))
    escaped, distance_squared = exact_escape(*pose, half_length=Fraction(7, 200))
    assert escaped
    assert distance_squared > DELTA * DELTA
    assert exact_escape(*pose)[0] is False
    # Both endpoints lie outside the square, so endpoint-only distance would be wrong.
    assert (
        exact_square_segment_dist2(
            Fraction(0), Fraction(1), Fraction(1), 0, half_length=Fraction(3, 2)
        )
        == 0
    )
    assert (
        exact_square_segment_dist2(Fraction(0), Fraction(1), Fraction(1501, 1000), 0)
        == Fraction(1, 1000) ** 2
    )
    # A far mark cannot certify the corner pose, and a box containing it is not empty.
    assert not exact_certify_leaf(np.array([0, 0, 0.5, 0.5, 0.5, 0.5, 5, 0, 0, 0]), DELTA)
    assert not exact_discard_box(np.array([0, 0, 0, 2, 0, 2], dtype=float))


def test_cli_refuses_an_incomplete_cover_and_invalid_budget(tmp_path: Path) -> None:
    output = tmp_path / "cover.json"
    command = [
        sys.executable,
        "-m",
        "devtools.segment_cover_replay",
        "--node-budget",
        "1",
        "--output",
        str(output),
    ]
    incomplete = subprocess.run(
        command,
        cwd=PACKING,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert incomplete.returncode == 1
    result = json.loads(incomplete.stdout)
    assert result == json.loads(output.read_text())
    assert result["status"] == "unresolved"
    assert result["proved"] is False
    assert result["failures"] > 0
    assert result["nodes"] <= 1
    assert result["volume_ok"] is True
    invalid = subprocess.run(
        [*command, "--floor", "nan"],
        cwd=PACKING,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert invalid.returncode == 2
    assert json.loads(invalid.stdout)["status"] == "error"
