"""Independent adapter controls; target geometry is never evaluated here."""

from __future__ import annotations

import json
import signal
import subprocess
import sys
from fractions import Fraction
from typing import Any

import pytest

from cases.stromquist import restricted_orientation as source
from devtools import run_restricted_orientation_discriminator as runner
from sqpack.field import FieldElement


def _toy_escape(
    name: str,
) -> tuple[FieldElement, tuple[source.Point, ...], tuple[source.Point, ...], dict[str, Any]]:
    field = source.source_field()
    side = field.rational(4)
    ten = tuple(
        (field.rational(3 + Fraction(i, 100)), field.rational("16/5")) for i in range(10)
    )
    twelve = tuple(
        (field.rational(3 + Fraction(i, 100)), field.rational("17/5")) for i in range(12)
    )
    angle = 0 if name in source.ANGLE_OBLIGATIONS[0] else 45
    coordinate = Fraction(1) if angle else Fraction(1, 2)
    if name == "localization":
        coordinate = Fraction(2)
    center = field.rational(coordinate)
    row: dict[str, Any] = {
        "obligation": name,
        "angle_degrees": angle,
        "center_power_basis": [center.text(), center.text()],
        "square_side": "1",
        "square_semantics": "closed",
        "ten_membership_mask": 0,
        "twelve_membership_mask": 0,
        "strict_box_counterexample_established": False,
    }
    return side, ten, twelve, row


@pytest.mark.parametrize("name", source.OBLIGATIONS)
def test_every_obstruction_clause_accepts_a_directly_checkable_toy(name: str) -> None:
    side, ten, twelve, row = _toy_escape(name)
    # All marked points have x>=3; the squares' rightmost corners have x<3.
    # The localization toy lies in the middle strip; forced toys lie on y=1.
    runner.verify_escape(side, ten, twelve, row)
    row["strict_box_counterexample_established"] = True
    with pytest.raises(ValueError, match="strict-box counterexample"):
        runner.verify_escape(side, ten, twelve, row)


def test_escape_replay_retains_a_closed_corner_hit_and_checks_containment() -> None:
    side, ten, twelve, row = _toy_escape("twelve_cover_0")
    twelve = ((side.field.one, side.field.one), *twelve[1:])
    # The square is [0,1]^2. Its corner point counts, even though it is not interior.
    with pytest.raises(ValueError, match="mask disagrees"):
        runner.verify_escape(side, ten, twelve, row)
    row["twelve_membership_mask"] = 1
    with pytest.raises(ValueError, match="does not violate"):
        runner.verify_escape(side, ten, twelve, row)
    row["center_power_basis"] = ["poly[0,0]", "poly[1/2,0]"]
    with pytest.raises(ValueError, match="corner containment"):
        runner.verify_escape(side, ten, twelve, row)


def _partial_source_receipts() -> str:
    """Synthetic child protocol fixture, not a geometric certificate."""
    rows = (
        {
            "kind": "input",
            "mode": "source-control",
            "container_side_power_basis": runner.SIDE_TEXT["source-control"],
            "ten_points_power_basis": [["poly[0,0]", "poly[0,0]"]] * 10,
            "twelve_points_power_basis": [["poly[0,0]", "poly[0,0]"]] * 12,
        },
        {
            "kind": "angle_complete",
            "angle_degrees": 0,
            "case": {
                "angle_degrees": 0,
                "reachable_event_strata_by_dimension": [1, 0, 0],
            },
            "obligations": {"axis_ten_cover": True, "twelve_cover_0": True},
            "obstructions": [],
        },
    )
    return "".join(json.dumps(row) + "\n" for row in rows)


def test_explicit_target_dispatch_is_capped_and_never_falls_back(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    calls: list[tuple[list[str], dict[str, Any]]] = []

    def timeout(command: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        calls.append((command, kwargs))
        raise subprocess.TimeoutExpired(command, kwargs["timeout"], output=b"")

    def forbidden(*_args: Any, **_kwargs: Any) -> None:
        raise AssertionError("mocked target dispatch evaluated geometry")

    monkeypatch.setattr(runner.subprocess, "run", timeout)
    monkeypatch.setattr(runner, "run_geometry", forbidden)
    assert runner.main(["--target-fixed-side"]) == 1
    assert calls == [
        (
            [
                sys.executable,
                "-m",
                "devtools.run_restricted_orientation_discriminator",
                "--target-fixed-side",
                "--worker",
                "--timeout-seconds",
                "10",
            ],
            {"capture_output": True, "text": True, "check": False, "timeout": 10},
        )
    ]
    result = json.loads(capsys.readouterr().out)
    assert result["mode"] == "target-fixed-side"
    assert result["complete"] is False
    assert result["checked_obligations"] == []
    assert set(result["unchecked_obligations"]) == set(source.OBLIGATIONS)
    assert result["process_wall_cap_seconds"] == 10
    assert result["h036_outcome"] == "unresolved"


def test_failed_worker_retains_completed_prefix_before_a_truncated_line(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def failed(command: list[str], **_kwargs: Any) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(
            command,
            1,
            _partial_source_receipts() + '{"kind":"angle_complete",',
            "unresolved: fixed process wall cap expired\n",
        )

    monkeypatch.setattr(runner.subprocess, "run", failed)
    assert runner.main(["--source-control"]) == 1
    result = json.loads(capsys.readouterr().out)
    assert result["complete"] is False
    assert set(result["checked_obligations"]) == set(source.ANGLE_OBLIGATIONS[0])
    assert set(result["unchecked_obligations"]) == set(source.ANGLE_OBLIGATIONS[45])


def test_internal_worker_mode_installs_its_own_cap_and_restores_the_handler(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    alarms: list[int] = []
    previous = signal.getsignal(signal.SIGALRM)

    def alarm(seconds: int) -> int:
        alarms.append(seconds)
        return 0

    def interrupted(mode: str, _emit: Any) -> None:
        assert mode == "target-fixed-side"
        assert alarms == [10]
        handler = signal.getsignal(signal.SIGALRM)
        assert callable(handler)
        handler(signal.SIGALRM, None)

    monkeypatch.setattr(runner.signal, "alarm", alarm)
    monkeypatch.setattr(runner, "run_geometry", interrupted)
    assert runner.main(["--target-fixed-side", "--worker"]) == 1
    assert alarms == [10, 0]
    assert signal.getsignal(signal.SIGALRM) is previous
    assert "fixed process wall cap expired" in capsys.readouterr().err
