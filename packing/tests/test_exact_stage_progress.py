"""Pure metadata journal controls, with no scientific input or proof work."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from devtools import exact_stage_progress as tool


class Clock:
    def __init__(self) -> None:
        self.value = 0.0

    def __call__(self) -> float:
        return self.value


def journal(tmp_path: Path, *, limit: float = 100) -> tuple[tool.StageProgress, Clock]:
    clock = Clock()
    result = tool.StageProgress(
        tmp_path / "progress.json",
        deadline=limit,
        counter_limits={"rows": 1056, "vertices": 1048576},
        clock=clock,
        cpu_clock=clock,
    )
    return result, clock


def read(value: tool.StageProgress) -> dict[str, Any]:
    return json.loads(value.output.read_bytes())


def test_sequential_stage_wall_cpu_and_cumulative_limits(tmp_path: Path) -> None:
    value, clock = journal(tmp_path)
    value.stage("canonical_extract", location={"context": 1})
    clock.value = 2
    assert value.checkpoint({"rows": 12, "vertices": 60})
    clock.value = 3
    value.end_stage({"rows": 24})
    value.stage("wall_domains", location={"owner": 0, "row": 26})
    clock.value = 7
    value.end_stage({"rows": 1056, "vertices": 350000})
    value.finish("observations_complete")
    result = read(value)
    assert result["status"] == "observations_complete"
    assert result["counter_limits"] == {"rows": 1056, "vertices": 1048576}
    assert result["counters"] == {"rows": 1056, "vertices": 350000}
    assert result["elapsed_wall_seconds"] == result["elapsed_cpu_seconds"] == 7
    assert [stage["name"] for stage in result["completed_stages"]] == [
        "canonical_extract",
        "wall_domains",
    ]
    assert result["current_stage"] is None
    assert not result["scientific_verdict_supplied"]
    assert not result["proof_prefix_admitted"]
    assert not result["timings_in_mathematical_payload"]
    assert result["outer_supervisor_authoritative"]


def test_incomplete_retains_current_stage_and_exceeded_counter(tmp_path: Path) -> None:
    value, clock = journal(tmp_path)
    value.stage("support", location={"owner": 5, "row": 6})
    clock.value = 3
    value.checkpoint({"rows": 1057})
    value.finish("incomplete", reason="row work ceiling")
    result = read(value)
    assert result["status"] == "incomplete"
    assert result["counters"]["rows"] == 1057
    assert result["current_stage"]["location"] == {"owner": 5, "row": 6}
    assert result["completed_stages"] == []


def test_checkpoints_rate_limited_but_stage_boundary_forces_latest_counts(
    tmp_path: Path,
) -> None:
    value, clock = journal(tmp_path)
    value.stage("rows")
    writes = value.writes
    for index in range(20):
        clock.value = index / 100
        assert not value.checkpoint({"rows": index})
    assert value.writes == writes
    assert read(value)["counters"]["rows"] == 0
    value.end_stage({"rows": 20})
    assert read(value)["counters"]["rows"] == 20


def test_existing_evidence_never_overwritten(tmp_path: Path) -> None:
    path = tmp_path / "progress.json"
    path.write_bytes(b"previous evidence")
    with pytest.raises(tool.JournalError, match="I/O failed"):
        journal(tmp_path)
    assert path.read_bytes() == b"previous evidence"


def test_atomic_update_failure_preserves_previous_snapshot(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    value, clock = journal(tmp_path)
    value.stage("rows")
    previous = value.output.read_bytes()

    def fail_replace(_self: Path, _target: Path) -> None:
        raise OSError("simulated atomic replace failure")

    monkeypatch.setattr(Path, "replace", fail_replace)
    clock.value = 2
    with pytest.raises(tool.JournalError, match="I/O failed"):
        value.checkpoint({"rows": 1})
    assert value.failed
    assert value.output.read_bytes() == previous
    assert list(tmp_path.glob(".stage-progress-*")) == []
    with pytest.raises(tool.JournalError, match="failed or finished"):
        value.end_stage({"rows": 1})


@pytest.mark.parametrize("deadline", [float("nan"), float("inf"), True, -1])
def test_invalid_or_expired_initial_clock_refuses_without_claim(
    deadline: Any, tmp_path: Path
) -> None:
    clock = Clock()
    with pytest.raises(tool.JournalError, match=r"finite|wall ceiling"):
        tool.StageProgress(
            tmp_path / "progress.json",
            deadline=deadline,
            counter_limits={},
            clock=clock,
            cpu_clock=clock,
        )
    assert not (tmp_path / "progress.json").exists()


def test_serialization_time_counts_against_caller_deadline(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    value, clock = journal(tmp_path, limit=3)
    original = tool.retained_json.dumps
    previous = value.output.read_bytes()

    def expires(*args: Any, **kwargs: Any) -> str:
        result = original(*args, **kwargs)
        clock.value = 4
        return result

    monkeypatch.setattr(tool.retained_json, "dumps", expires)
    with pytest.raises(tool.JournalIncompleteError, match="wall ceiling"):
        value.stage("wall")
    assert value.failed
    assert value.output.read_bytes() == previous


def test_byte_cap_failure_preserves_evidence_and_fail_closed_policy(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    value, _clock = journal(tmp_path)
    previous = value.output.read_bytes()
    monkeypatch.setattr(tool, "BYTE_LIMIT", 1)
    with pytest.raises(tool.JournalIncompleteError, match="byte ceiling"):
        value.stage("row")
    assert value.failed
    assert value.output.read_bytes() == previous


@pytest.mark.parametrize("kind", ["unknown", "negative", "bool", "decrease", "float"])
def test_invalid_or_decreasing_counters_refuse(kind: str, tmp_path: Path) -> None:
    value, _clock = journal(tmp_path)
    value.stage("rows")
    value.checkpoint({"rows": 1})
    counters = {
        "unknown": {"different": 2},
        "negative": {"rows": -1},
        "bool": {"rows": True},
        "decrease": {"rows": 0},
        "float": {"rows": 1.5},
    }[kind]
    with pytest.raises(tool.JournalError, match="counter"):
        value.checkpoint(counters)


@pytest.mark.parametrize("kind", ["stage_name", "location", "unfinished"])
def test_invalid_stage_or_unfinished_completion_poison_observer(
    kind: str, tmp_path: Path
) -> None:
    value, _clock = journal(tmp_path)

    def operation() -> None:
        if kind == "stage_name":
            value.stage("not geometry λ")
        elif kind == "location":
            value.stage("rows", location={"x": 1})
        else:
            value.stage("rows")
            value.finish("observations_complete")

    with pytest.raises(tool.JournalError, match=r"identifier|location|unfinished"):
        operation()
    assert value.failed
    with pytest.raises(tool.JournalError, match="failed or finished"):
        value.stage("another")


def test_successfully_finished_journal_cannot_resume(tmp_path: Path) -> None:
    value, _clock = journal(tmp_path)
    value.stage("rows")
    value.finish("refused", reason="metadata only")
    with pytest.raises(tool.JournalError, match="finished"):
        value.stage("another")


def test_stage_and_counter_rosters_bounded_and_input_limits_copied(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    value, _clock = journal(tmp_path)
    monkeypatch.setattr(tool, "STAGE_LIMIT", 1)
    value.stage("first")
    value.end_stage({})
    with pytest.raises(tool.JournalIncompleteError, match="stage ceiling"):
        value.stage("second")
    limits = {"rows": 5}
    copy = tool.StageProgress(
        tmp_path / "copy.json",
        deadline=100,
        counter_limits=limits,
        clock=Clock(),
        cpu_clock=Clock(),
    )
    limits["rows"] = 100
    assert read(copy)["counter_limits"]["rows"] == 5
    monkeypatch.setattr(tool, "COUNTER_LIMIT", 0)
    with pytest.raises(tool.JournalError, match="roster"):
        tool.StageProgress(
            tmp_path / "bad.json",
            deadline=100,
            counter_limits={"one": 1},
            clock=Clock(),
            cpu_clock=Clock(),
        )


def test_observer_totals_explicitly_exclude_current_write(tmp_path: Path) -> None:
    value, _clock = journal(tmp_path)
    value.stage("rows")
    result = read(value)["observer_io_through_previous_write"]
    assert result["writes"] == value.writes - 1
    assert result["wall_seconds"] == result["cpu_seconds"] == 0


@pytest.mark.parametrize("clock_value", [float("nan"), float("inf"), -1, True])
def test_bad_clock_observation_refuses_before_initial_claim(
    clock_value: Any,
    tmp_path: Path,
) -> None:
    def invalid_clock() -> float:
        return clock_value

    with pytest.raises(tool.JournalError, match="clock observation"):
        tool.StageProgress(
            tmp_path / "bad.json", deadline=100, counter_limits={}, clock=invalid_clock
        )
    assert not (tmp_path / "bad.json").exists()
