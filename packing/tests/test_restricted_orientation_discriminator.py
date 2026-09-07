"""Source/toy readiness controls; target dispatch is always mocked."""

from __future__ import annotations

import json
import subprocess
import sys
from copy import deepcopy
from typing import Any, cast

import pytest

from cases.stromquist.restricted_orientation import (
    point_sets,
    replay_point_sets,
    source_field,
    source_points,
)
from devtools import run_restricted_orientation_discriminator as runner


def test_shared_replay_preserves_the_original_source_inventory_and_results() -> None:
    side, ten, twelve = source_points(source_field())
    assert point_sets(side) == (ten, twelve)
    progress: list[dict[str, object]] = []
    result = replay_point_sets(side, ten, twelve, on_angle_complete=progress.append)
    assert result["obstructions"] == []
    assert result["obligations"] == {
        "axis_ten_cover": True,
        "localization": True,
        "forced_A1": True,
        "forced_A2": True,
        "forced_A3": True,
        "twelve_cover_0": True,
        "twelve_cover_45": True,
    }
    assert result["cases"] == [
        {
            "angle_degrees": 0,
            "reachable_event_strata_by_dimension": [280, 526, 247],
            "ten_avoiding_strata": 0,
            "canonical_ten_avoiding_strata": 0,
        },
        {
            "angle_degrees": 45,
            "reachable_event_strata_by_dimension": [406, 841, 444],
            "ten_avoiding_strata": 6,
            "canonical_ten_avoiding_strata": 1,
        },
    ]
    assert [item["angle_degrees"] for item in progress] == [0, 45]
    assert progress[0]["obligations"] == {"axis_ten_cover": True, "twelve_cover_0": True}
    assert set(cast(dict[str, bool], progress[1]["obligations"])) == {
        "localization",
        "forced_A1",
        "forced_A2",
        "forced_A3",
        "twelve_cover_45",
    }


def test_mode_and_cap_refusals_happen_before_dispatch(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*_args, **_kwargs):
        raise AssertionError("refused input dispatched geometry")

    monkeypatch.setattr(runner.subprocess, "run", forbidden)
    for arguments in (
        [],
        ["--source-control", "--target-fixed-side"],
        ["--source-control", "--side", "1939/500"],
        ["--source-control", "--angle", "0.25"],
        ["--target-fixed-side", "--timeout-seconds", "0"],
        ["--target-fixed-side", "--timeout-seconds", "11"],
        ["--target-fixed-side", "--timeout-seconds", "1.5"],
        ["--target-fixed-side", "--worker", "--timeout-seconds", "11"],
    ):
        with pytest.raises(SystemExit) as error:
            runner.main(arguments)
        assert error.value.code == 2


def _wire_control(mode: str = "source-control") -> list[dict[str, Any]]:
    """Protocol fixture only: target-mode tests never construct target geometry."""
    return [
        {
            "kind": "input",
            "mode": mode,
            "container_side_power_basis": runner.SIDE_TEXT[mode],
            "ten_points_power_basis": [None] * 10,
            "twelve_points_power_basis": [None] * 12,
        },
        *[
            {
                "kind": "angle_complete",
                "angle_degrees": angle,
                "case": {
                    "angle_degrees": angle,
                    "reachable_event_strata_by_dimension": [1, 0, 0],
                },
                "obligations": dict.fromkeys(names, True),
                "obstructions": [],
            }
            for angle, names in runner.ANGLE_OBLIGATIONS.items()
        ],
        {"kind": "finished", "worker_wall_seconds": 0, "worker_cpu_seconds": 0},
    ]


def _lines(rows: list[dict[str, Any]]) -> str:
    return "".join(json.dumps(row) + "\n" for row in rows)


def test_partial_receipts_keep_exact_checked_and_unchecked_remainder() -> None:
    rows = _wire_control()
    partial = _lines(rows[:2]) + '{"kind":"angle_com'
    result = runner.collect_receipts(
        partial, "source-control", worker_succeeded=False, interrupted=True
    )
    assert result["complete"] is False
    assert result["checked_obligations"] == ["axis_ten_cover", "twelve_cover_0"]
    assert result["unchecked_obligations"] == [
        "localization",
        "forced_A1",
        "forced_A2",
        "forced_A3",
        "twelve_cover_45",
    ]
    assert result["h036_outcome"] == "unresolved"
    empty = runner.collect_receipts("", "source-control", worker_succeeded=False)
    assert empty["checked_obligations"] == []
    assert empty["unchecked_obligations"] == list(runner.OBLIGATIONS)


def test_missing_duplicate_vacuous_and_inconsistent_receipts_refuse() -> None:
    rows = _wire_control()
    mutations = [rows[:-1], [rows[0], rows[2], rows[1], rows[3]], [*rows[:2], *rows[1:]]]
    for key, value in (
        ("obligations", {"axis_ten_cover": True}),
        ("obligations", {"axis_ten_cover": False, "twelve_cover_0": True}),
        ("obligations", {"axis_ten_cover": 1, "twelve_cover_0": True}),
        ("case", {"angle_degrees": 0, "reachable_event_strata_by_dimension": [0, 0, 0]}),
    ):
        changed = deepcopy(rows)
        changed[1][key] = value
        mutations.append(changed)
    for changed in mutations:
        with pytest.raises(ValueError, match=r"receipt|angle|obligation|escape"):
            runner.collect_receipts(_lines(changed), "source-control", worker_succeeded=True)


def test_target_dispatch_and_timeout_are_mocked_without_target_geometry(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    rows = _wire_control("target-fixed-side")
    commands: list[tuple[list[str], int]] = []

    def completed(command, *, capture_output, text, check, timeout):
        assert capture_output
        assert text
        assert not check
        commands.append((command, timeout))
        return subprocess.CompletedProcess(command, 0, _lines(rows), "")

    monkeypatch.setattr(runner.subprocess, "run", completed)
    assert runner.main(["--target-fixed-side", "--timeout-seconds", "3"]) == 0
    assert commands == [
        (
            [
                sys.executable,
                "-m",
                "devtools.run_restricted_orientation_discriminator",
                "--target-fixed-side",
                "--worker",
                "--timeout-seconds",
                "3",
            ],
            3,
        )
    ]
    result = json.loads(capsys.readouterr().out)
    assert result["complete"] is True
    assert result["theorem_acceptance"] is False
    assert result["h036_outcome"] == "unresolved"

    def timeout(command, **kwargs):
        assert kwargs["timeout"] == 10
        raise subprocess.TimeoutExpired(command, 10, output=(_lines(rows[:2]) + "{").encode())

    monkeypatch.setattr(runner.subprocess, "run", timeout)
    assert runner.main(["--target-fixed-side"]) == 1
    output = capsys.readouterr()
    assert "wall cap expired" in output.err
    result = json.loads(output.out)
    assert result["checked_obligations"] == ["axis_ten_cover", "twelve_cover_0"]
    assert len(result["unchecked_obligations"]) == 5
    assert result["complete"] is False


def test_internal_worker_installs_and_cancels_cap_without_target_geometry(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    alarms: list[int] = []
    monkeypatch.setattr(runner.signal, "alarm", alarms.append)

    def refused_geometry(mode, _emit):
        assert mode == "target-fixed-side"
        raise TimeoutError("toy timeout before geometry")

    monkeypatch.setattr(runner, "run_geometry", refused_geometry)
    assert runner.main(["--target-fixed-side", "--worker", "--timeout-seconds", "2"]) == 1
    assert alarms == [2, 0]
    assert "toy timeout before geometry" in capsys.readouterr().err


def test_returned_toy_escape_replay_keeps_boundary_and_each_forced_point() -> None:
    field = source_field()
    side = field.rational(4)
    half, one = field.rational("1/2"), field.one
    far = (field.rational(3), field.rational(3))
    row: dict[str, Any] = {
        "obligation": "twelve_cover_0",
        "angle_degrees": 0,
        "center_power_basis": [half.text(), half.text()],
        "square_side": "1",
        "square_semantics": "closed",
        "ten_membership_mask": 0,
        "twelve_membership_mask": 0,
        "strict_box_counterexample_established": False,
    }
    runner.verify_escape(side, (far,), (far,), row)
    boundary = (one, one)
    with pytest.raises(ValueError, match="determinant geometry"):
        runner.verify_escape(field.one, (boundary,), (boundary,), row)
    for index in range(3):
        center = (one, field.rational("3/4"))
        near = (center, (one + half / 4, center[1]), (one, center[1] + half / 4))
        twelve = tuple(far if j == index else point for j, point in enumerate(near))
        failed = {
            **row,
            "obligation": f"forced_A{index + 1}",
            "angle_degrees": 45,
            "center_power_basis": [value.text() for value in center],
            "twelve_membership_mask": 7 ^ (1 << index),
        }
        runner.verify_escape(side, (far,), twelve, failed)
        failed["obligation"] = f"forced_A{(index + 1) % 3 + 1}"
        with pytest.raises(ValueError, match="does not violate"):
            runner.verify_escape(side, (far,), twelve, failed)
    for key, value in (
        ("angle_degrees", 0.25),
        ("square_semantics", "open"),
        ("strict_box_counterexample_established", True),
        ("center_power_basis", ["poly[0,0]", "poly[0,0]"]),
    ):
        with pytest.raises(ValueError, match=r"escape|counterexample|containment"):
            runner.verify_escape(side, (far,), (far,), {**row, key: value})


def test_escape_parser_rejects_exponents_before_fraction_construction(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    field = source_field()
    assert runner.parse_coordinate("poly[-1/3,2]", field) == field.element(("-1/3", "2"))

    def forbidden(_value):
        raise AssertionError("invalid lexical input reached Fraction")

    monkeypatch.setattr(runner, "Fraction", forbidden)
    for value in (
        "poly[1e1000000000,0]",
        "poly[+1,0]",
        "poly[01,0]",
        "poly[1.0,0]",
        "poly[\uff11,0]",
        "poly[1,0,0]",
        "poly[" + "1" * 257 + ",0]",
    ):
        with pytest.raises(ValueError, match="coefficient"):
            runner.parse_coordinate(value, field)
