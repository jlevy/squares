"""Toy and mocked controls; actual original-source execution is never a fixture."""

from __future__ import annotations

import json
import subprocess
from fractions import Fraction
from pathlib import Path

import pytest

from devtools import angle_grid_source_control as grid


def test_toy_control_emits_the_exact_frozen_grid_wire_contract(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    points = tuple((Fraction(3, 4) + Fraction(i, 1000), Fraction(3, 4)) for i in range(10))
    monkeypatch.setattr(grid, "source_input", lambda: (Fraction(3, 2), points))
    result = grid.run_source()
    assert set(result) == {
        "version",
        "kind",
        "grid",
        "angle_slab",
        "assignments",
        "status",
        "inequalities_checked",
        "unresolved",
    }
    assert result["version"] == 1
    assert result["kind"] == "original-source-axis-ten-cover-grid"
    assert result["grid"] == [6, 3]
    assert result["angle_slab"] == ["0", "0"]
    assert result["assignments"] == [
        [1, 1, 4, 4, 7, 7],
        [0, 3, 3, 6, 6, 9],
        [2, 2, 5, 5, 8, 8],
    ]
    assert result["status"] == "proved"
    assert result["inequalities_checked"] == 432
    assert result["unresolved"] == []
    assert grid.parse_worker(json.dumps(result)) == result


def test_alarm_retains_only_completed_canonical_prefix(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(grid, "source_input", lambda: (Fraction(2), ()))

    def interrupted(*_args):
        yield (0, 0, 0, 0, 0), True
        yield (0, 0, 0, 0, 1), False
        raise TimeoutError("toy interrupted third obligation")

    monkeypatch.setattr(grid, "grid_obligations", interrupted)
    result = grid.run_source()
    assert result["status"] == "unresolved"
    assert result["inequalities_checked"] == 2
    assert result["unresolved"] == [[0, 0, 0, 0, 1]]
    assert grid.parse_worker(json.dumps(result)) == result


def test_failed_toy_assignments_do_not_short_circuit_the_complete_inventory(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    points = tuple((Fraction(3, 2) + Fraction(i, 1000), Fraction(3, 2)) for i in range(10))
    monkeypatch.setattr(grid, "source_input", lambda: (Fraction(3), points))
    result = grid.run_source()
    assert result["status"] == "unresolved"
    assert result["inequalities_checked"] == 432
    assert result["unresolved"]
    assert grid.parse_worker(json.dumps(result)) == result


def test_refused_modes_overrides_and_colliding_paths_never_dispatch(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    def forbidden(*_args, **_kwargs):
        raise AssertionError("refusal dispatched or constructed source")

    monkeypatch.setattr(grid, "source_input", forbidden)
    monkeypatch.setattr(grid.subprocess, "run", forbidden)
    for arguments in (
        [],
        ["--target-fixed-side"],
        ["--source-control", "--side", "2"],
        ["--source-control", "--angle", "0"],
        ["--source-control", "--timeout-seconds", "11"],
        ["--source-control", "--grid", "6", "3"],
        ["--source-control", "--worker", "--output", str(tmp_path / "p")],
        ["--source-control", "--output", str(tmp_path / "p"), "--log", str(tmp_path / "p")],
    ):
        with pytest.raises(SystemExit) as error:
            grid.main(arguments)
        assert error.value.code == 2


def test_worker_packet_refuses_scope_counts_booleans_and_nonprefix_failures() -> None:
    original = grid.packet(2, [(0, 0, 0, 0, 1)])
    for change in (
        {"version": True},
        {"grid": [True, 3]},
        {"status": "proved"},
        {"inequalities_checked": True},
        {"inequalities_checked": 433},
        {"assignments": [[True] * 6] * 3},
        {"extra": "unfrozen"},
        {"unresolved": [[0, 0, 0, 0, 2]]},
        {"unresolved": [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1]]},
        {"unresolved": [[0, 0, 0, 0, True]]},
    ):
        with pytest.raises(ValueError, match="worker"):
            grid.parse_worker(json.dumps(original | change))
    with pytest.raises(ValueError, match="256 KiB"):
        grid.parse_worker(" " * (262144 + 1))


def test_worker_installs_and_cancels_its_fixed_alarm_without_source_geometry(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    alarms = []
    monkeypatch.setattr(grid.signal, "alarm", alarms.append)
    monkeypatch.setattr(grid, "run_source", lambda: grid.packet(0, []))
    assert grid.main(["--source-control", "--worker"]) == 1
    assert alarms == [10, 0]
    assert json.loads(capsys.readouterr().out) == grid.packet(0, [])


def test_parent_timeout_invokes_once_and_retains_raw_output(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    calls = []

    def timeout(command, **kwargs):
        calls.append((command, kwargs["timeout"]))
        raise subprocess.TimeoutExpired(command, 10, output=b"{partial", stderr=b"toy cap")

    monkeypatch.setattr(grid.subprocess, "run", timeout)
    output, log = tmp_path / "packet.json", tmp_path / "run.log"
    assert grid.main(["--source-control", "--output", str(output), "--log", str(log)]) == 1
    assert len(calls) == 1
    assert calls[0][1] == 10
    assert json.loads(output.read_text()) == grid.packet(0, [])
    retained = json.loads(log.read_text())
    assert retained["stdout"] == "{partial"
    assert retained["stderr"] == "toy cap"
    assert retained["child_exit_code"] is None
    assert retained["child_wall_cap_seconds"] == 10


def test_malformed_and_nonzero_worker_receipts_preserve_raw_execution_log(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    output, log = tmp_path / "packet.json", tmp_path / "run.log"
    for stdout, child_exit, expected_code in (
        ("{truncated", 2, 2),
        (json.dumps(grid.packet(432, [])), 1, 1),
    ):
        monkeypatch.setattr(
            grid.subprocess,
            "run",
            lambda command, child_exit=child_exit, stdout=stdout, **_kwargs: (
                subprocess.CompletedProcess(command, child_exit, stdout, "toy")
            ),
        )
        assert (
            grid.main(["--source-control", "--output", str(output), "--log", str(log)])
            == expected_code
        )
        assert json.loads(output.read_text())["status"] == "unresolved"
        retained = json.loads(log.read_text())
        assert retained["stdout"] == stdout
        assert retained["stderr"] == "toy"
        assert retained["child_exit_code"] == child_exit
