"""Check the Linux certificate runner without executing the screened classes."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from devtools import run_n17_native_certificate as runner


@pytest.mark.parametrize("failure", [None, "search", "verification", "sample"])
def test_runner_requires_full_pass(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, failure: str | None
) -> None:
    output = tmp_path / "run"
    commands: list[list[str]] = []

    def step(command: list[str], log: Path) -> dict[str, Any]:
        commands.append(command)
        stage = log.stem
        if stage == "verification":
            # The search receipt must survive before the expensive verification.
            assert "search" in json.loads((output / "run.json").read_text())
            _ = (output / "verification.json").write_text(
                json.dumps(
                    {
                        "status": "PASS",
                        "mode": "sample" if failure == "sample" else "full",
                        "certificate": {"manifest_sha256": "test-manifest"},
                    }
                )
            )
        return {"returncode": int(stage == failure), "command": command}

    monkeypatch.setattr(runner, "_step", step)
    assert runner.run("C1", tmp_path / "native", output, 86400.0) == int(failure is not None)
    receipt = json.loads((output / "run.json").read_text())
    assert (receipt["status"] == "PASS") == (failure is None)
    assert receipt["wall_seconds"] >= 0
    assert "--save-certificate" in commands[0]
    assert "--native-dir" in commands[0]
    assert runner.CLASSES["C1"] in commands[0]
    if failure == "search":
        assert len(commands) == 1
    else:
        assert len(commands) == 2
        assert "--sample" not in commands[1]
        assert "--trig-sample" not in commands[1]
    with pytest.raises(FileExistsError):
        runner.run("C1", tmp_path / "native", output, 86400.0)
