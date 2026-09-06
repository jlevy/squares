"""The retained-family replay reproduces a record from its bytes and refuses a wrong one."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import pytest

from devtools import replay_ceiling_family as replay
from sqpack.fractional.ceiling import (
    CeilingCertificate,
    arrangement_lines,
    container_vertices,
    maximum_depth,
)

# Two upright unit squares overlapping on [1/2, 1]^2 inside side 2: depth two there.
FAMILY = {
    "n": 2,
    "outer_side": "2",
    "square_side": "1",
    "half_tangents": ["0", "207107/500000"],
    "placements": [["0", "1/2", "1/2", "1", "1"], ["0", "1", "1", "1", "1"]],
    "total_weight": "2",
    "total_weight_float": 2.0,
}


def genuine_numbers() -> tuple[int, Fraction]:
    certificate = CeilingCertificate.from_record(FAMILY)
    vertices = container_vertices(certificate, arrangement_lines(certificate))
    worst, _, _ = maximum_depth(certificate, vertices)
    return len(vertices), worst


def write(path: Path, record: dict) -> Path:
    path.write_text(json.dumps(record))
    return path


def test_a_frozen_family_replays_to_its_own_provenance(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    vertices, worst = genuine_numbers()
    assert worst == 2
    record = {
        **FAMILY,
        "provenance": {"verify_ceiling": {"vertices": vertices, "max_depth": str(worst)}},
    }
    path = write(tmp_path / "family.json", record)
    assert replay.main(["--check", str(path)]) == 0
    line = json.loads(capsys.readouterr().out)
    assert line["check"] == "reproduced"
    assert line["placements"] == 2
    assert line["max_depth"] == "2"
    assert line["scaled_total"] == "1"
    assert line["vertices"] == vertices
    assert not line["proved"]


def test_a_record_claiming_a_lower_depth_is_refused(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    vertices, _ = genuine_numbers()
    record = {
        **FAMILY,
        "provenance": {"verify_ceiling": {"vertices": vertices, "max_depth": "1"}},
    }
    path = write(tmp_path / "family.json", record)
    assert replay.main(["--check", str(path)]) == 1
    line = json.loads(capsys.readouterr().out)
    assert line["check"] == ["max_depth: replayed 2, recorded 1"]


def test_a_state_file_is_checked_against_its_scaled_total(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    state = {"best_family": FAMILY, "best_scaled_total": "1"}
    path = write(tmp_path / "state.json", state)
    assert replay.main(["--check", str(path)]) == 0
    assert json.loads(capsys.readouterr().out)["check"] == "reproduced"
    wrong = {"best_family": FAMILY, "best_scaled_total": 1.5}
    path = write(tmp_path / "wrong.json", wrong)
    assert replay.main(["--check", str(path)]) == 1
    assert json.loads(capsys.readouterr().out)["check"] == [
        "scaled_total: replayed 1, recorded 3/2"
    ]


def test_a_record_with_nothing_to_check_cannot_pass_the_check(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = write(tmp_path / "bare.json", FAMILY)
    assert replay.main([str(path)]) == 0
    assert "check" not in json.loads(capsys.readouterr().out)
    assert replay.main(["--check", str(path)]) == 1
    assert json.loads(capsys.readouterr().out)["check"] == [
        "the record carries nothing to check against"
    ]
