"""Failure-path contracts for repository-bound campaign applications."""

from __future__ import annotations

from pathlib import Path

import pytest

from cases.campaign_smoke import baseline_sweep
from sqpack.campaign import runner


def test_gate_refusal_has_a_specific_type_and_recovery_message(tmp_path: Path) -> None:
    marker = tmp_path / ".gate-running"
    marker.touch()

    with pytest.raises(runner.GateRunningError, match=r"delete \.gate-running if a crash"):
        runner.refuse_if_gate_running(marker)


def test_git_failure_reports_the_command_and_stderr() -> None:
    with pytest.raises(runner.RefusalError, match=r"git rev-parse --verify") as raised:
        runner.git("rev-parse", "--verify", "definitely-not-a-revision")

    assert "fatal:" in str(raised.value)


def test_campaign_artifacts_use_the_stable_module_entry_point() -> None:
    assert runner.CAMPAIGN_ENTRY_POINT == "sqpack.campaign.runner:main"


@pytest.mark.parametrize(
    ("axis", "value", "message"),
    [("--instances", "0", "each instance"), ("--seeds", "0", "each seed")],
)
def test_baseline_rejects_invalid_axes_before_work_or_output(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    axis: str,
    value: str,
    message: str,
) -> None:
    engine = tmp_path / "sqsearch"
    engine.touch()
    output = tmp_path / "result.jsonl"

    with pytest.raises(SystemExit) as raised:
        baseline_sweep.main(
            [str(output), "--engine", str(engine), axis, value, "--budget-moves", "1"]
        )

    assert raised.value.code == 2
    assert message in capsys.readouterr().err
    assert not output.exists()
