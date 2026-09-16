"""The annealing summariser reproduces the committed `summaries.json` from rows.

The per-trial rows are not retained, so these fixtures are verbatim copies of a few of
them: the whole of one six-trial file scored before runs were repaired, and the first
100 seeds of `n = 10` from a repaired file. A best-of-first-k value depends only on the
first k seeds, so those 100 rows determine three entries of that cell's ladder.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from workbench_tools import summarize_annealing
from workbench_tools.summarize_annealing import overlaps, render, summarize, summarize_rows

FIXTURES = Path(__file__).parent / "fixtures" / "annealing-rows"
UNREPAIRED = FIXTURES / "20260912T012205-n11-bodies.jsonl"
REPAIRED_PREFIX = FIXTURES / "resolved-5k-a6-n10-first-100-seeds.jsonl"


def _committed() -> dict[str, dict[str, dict[str, object]]]:
    return json.loads(summarize_annealing.SUMMARIES.read_text(encoding="utf-8"))


def _rows(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_a_whole_unrepaired_file_reproduces_its_committed_cell_exactly() -> None:
    assert summarize_rows(_rows(UNREPAIRED)) == _committed()[UNREPAIRED.name]


def test_repaired_rows_reproduce_the_committed_ladder_their_seeds_determine() -> None:
    cell = summarize_rows(_rows(REPAIRED_PREFIX))["10"]
    committed = _committed()["resolved-5k-a6.jsonl"]["10"]

    assert cell["resolved"] is True
    assert committed["resolved"] is True
    ladder = committed["best_of"]
    assert isinstance(ladder, dict)
    assert cell["best_of"] == {k: ladder[k] for k in ("1", "10", "100")}


def test_resolved_means_the_rows_carry_a_repaired_side_not_that_rows_were_filtered() -> None:
    rows = _rows(REPAIRED_PREFIX)
    stripped = [
        {key: value for key, value in row.items() if not key.startswith("resolved_")}
        for row in rows
    ]

    repaired = summarize_rows(rows)["10"]
    raw = summarize_rows(stripped)["10"]

    assert raw["resolved"] is False
    assert repaired["trials"] == raw["trials"] == len(rows)
    assert raw["closed_median"] > repaired["closed_median"]


def test_the_directory_summary_renders_byte_for_byte_like_the_committed_file(
    tmp_path: Path,
) -> None:
    (tmp_path / UNREPAIRED.name).write_bytes(UNREPAIRED.read_bytes())
    (tmp_path / "empty.jsonl").write_text("", encoding="utf-8")

    summary = summarize(tmp_path)

    assert summary == {UNREPAIRED.name: _committed()[UNREPAIRED.name]}
    committed = summarize_annealing.SUMMARIES.read_text(encoding="utf-8")
    assert render(_committed()) == committed


def test_a_cell_whose_record_equals_the_grid_is_refused() -> None:
    row = {"n": 4, "seed": 0, "record": 2.0, "excess": 0.0, "ms": 1.0}

    with pytest.raises(ValueError, match="no gap"):
        summarize_rows([row])


def test_the_overlap_report_counts_distinct_runs_and_what_ended_below_tolerance() -> None:
    rows = _rows(REPAIRED_PREFIX)
    report = overlaps([*rows, *rows[:10]])

    assert report.runs == 100
    assert report.rows == 110
    assert report.at_or_below_tolerance == 0
    assert 0 < report.overlap_min <= report.overlap_median <= report.overlap_max
    assert report.repaired_all_finite
    assert report.repaired_overlap_max <= 1e-9
    assert report.seeds_contiguous


def test_the_overlap_report_refuses_a_run_replayed_with_a_different_overlap() -> None:
    rows = _rows(REPAIRED_PREFIX)
    forged = {**rows[0], "overlap": 0.0}

    with pytest.raises(ValueError, match="disagree"):
        overlaps([*rows, forged])


def test_check_refuses_to_pass_when_no_rows_are_present(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert summarize_annealing.main(["--rows", str(tmp_path), "--check"]) == 1
    assert "no rows" in capsys.readouterr().out


def test_check_compares_the_run_files_present_and_names_how_many(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (tmp_path / UNREPAIRED.name).write_bytes(UNREPAIRED.read_bytes())

    assert summarize_annealing.main(["--rows", str(tmp_path), "--check"]) == 0
    assert f"1 of {len(_committed())} committed run files" in capsys.readouterr().out

    rows = _rows(UNREPAIRED)
    rows[0]["ms"] = 99.0
    (tmp_path / UNREPAIRED.name).write_text(
        "".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8"
    )
    assert summarize_annealing.main(["--rows", str(tmp_path), "--check"]) == 0, "timing only"
    capsys.readouterr()

    rows[0]["excess"] = 0.0
    (tmp_path / UNREPAIRED.name).write_text(
        "".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8"
    )
    assert summarize_annealing.main(["--rows", str(tmp_path), "--check"]) == 1
    assert f"MISMATCH {UNREPAIRED.name}: cells differ" in capsys.readouterr().out
