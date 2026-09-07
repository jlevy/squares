"""Rational toys and mocked dispatch only; never construct the fixed-side target."""

from __future__ import annotations

import json
import subprocess
from fractions import Fraction
from pathlib import Path

import pytest

from devtools import angle_near_axis_control as near


@pytest.fixture(autouse=True)
def refuse_real_target(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*_args, **_kwargs):
        raise AssertionError("a control attempted to construct the actual target")

    monkeypatch.setattr(near, "target_input", forbidden)
    monkeypatch.setattr(subprocess, "run", forbidden)


def test_toy_source_formulas_are_evaluated_directly_and_sorted() -> None:
    q = Fraction
    assert near.ten_set(q(3)) == (
        (q(3, 4), q(3, 2)),
        (q(1), q(1)),
        (q(1), q(2)),
        (q(5, 4), q(3, 2)),
        (q(3, 2), q(1)),
        (q(3, 2), q(2)),
        (q(7, 4), q(3, 2)),
        (q(2), q(1)),
        (q(2), q(2)),
        (q(9, 4), q(3, 2)),
    )
    with pytest.raises(ValueError, match="Fraction"):
        near.ten_set(3.0)  # pyright: ignore[reportArgumentType]
    with pytest.raises(ValueError, match="ten"):
        near.ten_set(q(2))


def test_both_closed_slabs_use_the_complete_toy_grid_in_fixed_order(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    points = tuple((Fraction(3, 4) + Fraction(i, 1000), Fraction(3, 4)) for i in range(10))
    monkeypatch.setattr(near, "target_input", lambda: (Fraction(3, 2), points))
    result = near.run_target()
    assert set(result) == {
        "version",
        "kind",
        "side",
        "grid",
        "half_angle_slabs",
        "assignments",
        "status",
        "inequalities_checked",
        "unresolved",
    }
    assert result["half_angle_slabs"] == [
        ["-110880/50803079", "0"],
        ["0", "110880/50803079"],
    ]
    assert result["assignments"] == [
        [1, 1, 4, 4, 7, 7],
        [0, 3, 3, 6, 6, 9],
        [2, 2, 5, 5, 8, 8],
    ]
    assert result["status"] == "proved"
    assert result["inequalities_checked"] == 864
    assert result["unresolved"] == []


def test_cli_refuses_missing_mode_and_all_domain_or_budget_overrides(tmp_path: Path) -> None:
    for arguments in (
        [],
        ["--source-control"],
        ["--target-near-axis", "--side", "3"],
        ["--target-near-axis", "--angle", "0"],
        ["--target-near-axis", "--sign-depth", "1"],
        ["--target-near-axis", "--timeout-seconds", "11"],
        ["--target-near-axis", "--grid", "6", "3"],
        ["--target-near-axis", "--worker", "--output", str(tmp_path / "p")],
        ["--target-near-axis", "--output", str(tmp_path / "p"), "--log", str(tmp_path / "p")],
    ):
        with pytest.raises(SystemExit) as error:
            near.main(arguments)
        assert error.value.code == 2


def test_worker_prefix_stops_in_the_second_slab_without_claiming_completion(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(near, "target_input", lambda: (Fraction(3, 2), ()))
    seen = []

    def interrupted(_side, _points, _assignments, *, low, high):
        seen.append((low, high))
        if low < 0:
            for row in range(3):
                for column in range(6):
                    for triangle in range(2):
                        for vertex in range(3):
                            for axis in range(4):
                                yield (row, column, triangle, vertex, axis), True
        else:
            yield (0, 0, 0, 0, 0), False
            raise TimeoutError("toy second-slab alarm")

    monkeypatch.setattr(near, "grid_obligations", interrupted)
    result = near.run_target()
    assert seen == list(near.SLABS)
    assert result["status"] == "unresolved"
    assert result["inequalities_checked"] == 433
    assert result["unresolved"] == [[1, 0, 0, 0, 0, 0]]
    assert near.parse_worker(json.dumps(result)) == result


def test_failed_toy_labels_keep_all_obligations_in_both_closed_slabs(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    points = tuple((Fraction(3, 2) + Fraction(i, 1000), Fraction(3, 2)) for i in range(10))
    monkeypatch.setattr(near, "target_input", lambda: (Fraction(3), points))
    result = near.run_target()
    assert result["status"] == "unresolved"
    assert result["inequalities_checked"] == 864
    assert {index[0] for index in result["unresolved"]} == {0, 1}
    assert near.parse_worker(json.dumps(result)) == result


def test_packet_binding_refuses_changed_range_labels_counts_or_failure_order() -> None:
    original = near.packet(2, [(0, 0, 0, 0, 0, 1)])
    for change in (
        {"version": True},
        {"kind": "original-source-axis-ten-cover-grid"},
        {"side": "3.878"},
        {"grid": [True, 3]},
        {"status": "proved"},
        {"half_angle_slabs": [["0", "110880/50803079"]]},
        {"half_angle_slabs": [["-1/1000", "0"], ["0", "1/1000"]]},
        {"assignments": [[0] * 6] * 3},
        {"extra": "unfrozen"},
        {"inequalities_checked": True},
        {"inequalities_checked": 865},
        {"unresolved": [[0, 0, 0, 0, 0, 2]]},
        {"unresolved": [[0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0]]},
        {"unresolved": [[0, 0, 0, 0, 0, True]]},
    ):
        with pytest.raises(ValueError, match="packet"):
            near.parse_worker(json.dumps(original | change))
    with pytest.raises(ValueError, match="duplicate"):
        near.parse_worker('{"version": 1, "version": 1}')
    with pytest.raises(ValueError, match="256 KiB"):
        near.parse_worker(" " * 262145)


def test_mocked_alarm_and_one_parent_timeout_retain_honest_output(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    alarms = []
    monkeypatch.setattr(near.signal, "alarm", alarms.append)
    monkeypatch.setattr(near, "run_target", lambda: near.packet(0, []))
    assert near.main(["--target-near-axis", "--worker"]) == 1
    assert alarms == [10, 0]
    assert json.loads(capsys.readouterr().out)["status"] == "unresolved"
    calls = []

    def timeout(command, **kwargs):
        calls.append((command, kwargs["timeout"]))
        raise subprocess.TimeoutExpired(command, 10, output=b"{partial", stderr=b"toy alarm")

    monkeypatch.setattr(subprocess, "run", timeout)
    output, log = tmp_path / "p.json", tmp_path / "p.log"
    assert near.main(["--target-near-axis", "--output", str(output), "--log", str(log)]) == 1
    assert len(calls) == 1
    assert calls[0][1] == 10
    assert json.loads(output.read_text()) == near.packet(0, [])
    retained = json.loads(log.read_text())
    assert retained["child_exit_code"] is None
    assert retained["stdout"] == "{partial"
    assert retained["stderr"] == "toy alarm"


def test_parent_success_requires_a_complete_packet_and_zero_worker_exit(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    output, log = tmp_path / "p.json", tmp_path / "p.log"
    for payload, child_exit, expected_code in (
        (json.dumps(near.packet(864, [])), 0, 0),
        (json.dumps(near.packet(864, [])), 1, 1),
        ("{truncated", 2, 2),
    ):

        def failed(command, payload=payload, child_exit=child_exit, **_kwargs):
            return subprocess.CompletedProcess(command, child_exit, payload, "toy failure")

        monkeypatch.setattr(subprocess, "run", failed)
        arguments = ["--target-near-axis", "--output", str(output), "--log", str(log)]
        assert near.main(arguments) == expected_code
        assert json.loads(output.read_text())["status"] == (
            "proved" if expected_code == 0 else "unresolved"
        )
        retained = json.loads(log.read_text())
        assert retained["stdout"] == payload
        assert retained["stderr"] == "toy failure"
        assert retained["child_exit_code"] == child_exit
