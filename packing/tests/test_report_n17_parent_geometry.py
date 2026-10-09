"""Synthetic structural counts and bounded accepted-parent audit custody."""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import pytest
from test_check_n17_partner_pose_coupling import synthetic_state, write_fixture

from devtools import report_n17_parent_geometry as tool


def deadline() -> float:
    return time.monotonic() + 30


def test_more_than64_pieces_counted_without_coupling_predicates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    cells, roles, _roster, _centre = synthetic_state()
    cells["1"][0]["residual_polygons"] = [[["1", "1"]]] * 100 + [[]]

    def forbidden(*_args: Any, **_kwargs: Any) -> Any:
        raise AssertionError("structural audit must not clip or couple geometry")

    monkeypatch.setattr(tool.parent, "wall_clip", forbidden)
    monkeypatch.setattr(tool.parent, "row_planes", forbidden)
    result = tool.inspect(cells, roles, deadline=deadline())
    assert result["all_rows_checked"] == 1056
    assert result["foreign_rows_checked"] == 992
    assert result["largest_row_by_piece_count"]["pieces"] == 101
    assert result["largest_row_by_piece_count"]["owner"] == 1
    assert result["empty_residual_pieces"] == 1
    assert result["total_residual_pieces"] == 180
    assert result["total_residual_vertices"] == 179
    assert not result["row_piece_limit_applied"]
    assert not result["prospective_mathematical_comparisons"]["all_rows_within64_pieces"]
    assert result["prospective_mathematical_comparisons"]["all_rows_within4096_pieces"]


@pytest.mark.parametrize("token", ["1e999999999", "2/4", "-0", "1/1", "\u0661"])
def test_canonical_scalar_grammar_before_bounded_int_parse(token: str) -> None:
    with pytest.raises(ValueError, match=r"ASCII|canonical|grammar"):
        tool.scalar_bits(token)
    assert tool.scalar_bits("3/8") == 4


@pytest.mark.parametrize("kind", ["vertices", "characters", "deadline", "rows", "reference"])
def test_limits_and_structural_refusals(kind: str, monkeypatch: pytest.MonkeyPatch) -> None:
    cells, roles, _roster, _centre = synthetic_state()
    if kind == "vertices":
        monkeypatch.setattr(tool, "SCAN_VERTEX_LIMIT", 1)
    elif kind == "characters":
        monkeypatch.setattr(tool, "COORDINATE_CHAR_LIMIT", 2)
        cells["1"][0]["residual_polygons"] = [[["100", "1"]]]
    elif kind == "rows":
        cells["1"].pop()
    elif kind == "reference":
        cells["1"][0]["reference"]["owner"] = 2
    exception = ValueError if kind in ("rows", "reference") else tool.IncompleteError
    with pytest.raises(exception):
        tool.inspect(
            cells, roles, deadline=time.monotonic() - 1 if kind == "deadline" else deadline()
        )


def test_coordinate_above_math_bit_budget_is_measured_not_refused() -> None:
    cells, roles, _roster, _centre = synthetic_state()
    # More than CPython's global decimal-to-int digit limit; source parses chunks.
    token = "1" + "0" * 5000
    cells["1"][0]["residual_polygons"] = [[[token, "1"]]]
    result = tool.inspect(cells, roles, deadline=deadline())
    assert result["status"] == "complete"
    assert result["largest_coordinate_bits"] > 16384
    assert not result["prospective_mathematical_comparisons"]["all_coordinates_within4096_bits"]


def test_full_accepted_intake_sizes_and_no_scientific_claim(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    document = write_fixture(tmp_path, monkeypatch) | {"schema": tool.DESCRIPTOR_SCHEMA}
    result = tool.generate(document, deadline=deadline())
    assert result["status"] == "complete"
    assert result["all_rows_checked"] == 1056
    assert result["accepted_matched_pose_premise_freshly_checked"]
    assert all(result[key] is False for key in tool.scope())
    document["centered_receipt_sha256"] = "f" * 64
    with pytest.raises(ValueError, match="identity"):
        tool.generate(document, deadline=deadline())


def test_fresh_clean_cli_and_output_wall_caps(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    document = write_fixture(tmp_path, monkeypatch) | {"schema": tool.DESCRIPTOR_SCHEMA}
    descriptor = tmp_path / "audit.json"
    descriptor.write_text(json.dumps(document))
    output = tmp_path / "sizes.json"
    code = (
        "from pathlib import Path; import sys; "
        "from devtools import report_n17_parent_geometry as t; "
        "t.finite.REPO=Path(sys.argv[1]); raise SystemExit(t.main(sys.argv[2:]))"
    )
    command = [
        sys.executable,
        "-c",
        code,
        str(tmp_path),
        "--descriptor",
        str(descriptor),
        "--max-seconds",
        "30",
        "--output",
        str(output),
    ]
    completed = subprocess.run(command, capture_output=True, text=True, timeout=40, check=False)
    assert completed.returncode == 0, completed.stderr
    assert json.loads(output.read_bytes())["status"] == "complete"
    monkeypatch.setattr(tool, "OUTPUT_LIMIT", 1)
    assert tool.main(["--descriptor", str(descriptor), "--output", str(output)]) == 1
    assert json.loads(output.read_bytes())["status"] == "incomplete"
