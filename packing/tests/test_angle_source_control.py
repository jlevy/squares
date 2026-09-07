"""Toy and mocked-dispatch controls; never invoke the original-source builder."""

from __future__ import annotations

import json
import subprocess
from fractions import Fraction
from pathlib import Path

import pytest

from devtools import angle_source_control as source
from devtools.angle_tile_certificate import closed_tiles


def test_unknown_modes_and_cap_overrides_refuse_before_source_construction(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden(*_args, **_kwargs):
        raise AssertionError("refused input constructed or dispatched the original source")

    monkeypatch.setattr(source, "source_input", forbidden)
    monkeypatch.setattr(source.subprocess, "run", forbidden)
    for arguments in (
        [],
        ["--target-fixed-side"],
        ["--source-control", "--side", "2"],
        ["--source-control", "--timeout-seconds", "11"],
        ["--source-control", "--depth", "11"],
        ["--source-control", "--angle", "1"],
    ):
        with pytest.raises(SystemExit) as error:
            source.main(arguments)
        assert error.value.code == 2


def test_toy_builder_uses_first_point_and_complete_closed_root_inventory() -> None:
    result = source.build_cover(
        Fraction(3, 2),
        ((Fraction(3, 4), Fraction(3, 4)), (Fraction(4, 5), Fraction(4, 5))),
    )
    assert result["status"] == "certified"
    assert result["leaves"] == [["0", 0], ["1", 0]]
    assert result["unchecked_paths"] == []
    assert result["point_trials"] == 2


def test_mocked_process_timeout_stays_unresolved_and_never_retries(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    calls = []

    def timeout(command, **kwargs):
        calls.append((command, kwargs["timeout"]))
        raise subprocess.TimeoutExpired(command, 10, output=b"", stderr=b"toy interrupted")

    monkeypatch.setattr(source.subprocess, "run", timeout)
    assert source.main(["--source-control"]) == 1
    result = json.loads(capsys.readouterr().out)
    assert result["status"] == "unresolved"
    assert result["stop_reason"] == "child process cap"
    assert len(calls) == 1
    assert calls[0][1] == 10
    assert result["h036_outcome"] == "unresolved"


def test_bfs_depth_leaf_and_alarm_stops_keep_a_complete_unresolved_partition(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    points = ((Fraction(3, 2), Fraction(3, 2)),)
    monkeypatch.setattr(source, "DEPTH_CAP", 1)
    depth_stop = source.build_cover(Fraction(3), points)
    assert depth_stop["stop_reason"] == "tile depth cap"
    assert depth_stop["stopped_tile"] == "00"
    assert depth_stop["point_trials"] == 3
    assert depth_stop["unchecked_paths"] == ["00", "01", "10", "11"]
    assert len(closed_tiles(tuple(row[0] for row in depth_stop["leaves"]))) == 4
    monkeypatch.setattr(source, "LEAF_CAP", 3)
    leaf_stop = source.build_cover(Fraction(3), points)
    assert leaf_stop["stop_reason"] == "leaf cap"
    assert leaf_stop["stopped_tile"] == "1"
    assert leaf_stop["point_trials"] == 2
    assert leaf_stop["unchecked_paths"] == ["00", "01", "1"]

    def expire(*_args, **_kwargs):
        raise TimeoutError("toy algebra interrupted")

    monkeypatch.setattr(source, "membership_polynomials", expire)
    alarm_stop = source.build_cover(Fraction(3), points)
    assert alarm_stop["stop_reason"] == "worker alarm"
    assert alarm_stop["leaves"] == [["0", None], ["1", None]]


def test_worker_alarm_and_public_raw_output_retention_without_source_geometry(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    alarms = []
    monkeypatch.setattr(source.signal, "alarm", alarms.append)

    def refused_source():
        raise TimeoutError("toy source interrupted before construction")

    monkeypatch.setattr(source, "run_source", refused_source)
    assert source.main(["--source-control", "--worker"]) == 1
    assert alarms == [10, 0]
    assert json.loads(capsys.readouterr().out)["status"] == "unresolved"

    def failed(command, **kwargs):
        assert kwargs["timeout"] == 10
        return subprocess.CompletedProcess(command, 2, "{truncated", "deliberate toy failure")

    monkeypatch.setattr(source.subprocess, "run", failed)
    output, log = tmp_path / "result.json", tmp_path / "run.log"
    assert source.main(["--source-control", "--output", str(output), "--log", str(log)]) == 2
    retained = json.loads(log.read_text())
    assert retained["child_exit_code"] == 2
    assert retained["parent_exit_code"] == 2
    assert retained["stdout"] == "{truncated"
    assert retained["stderr"] == "deliberate toy failure"
    assert json.loads(output.read_text())["status"] == "unresolved"
