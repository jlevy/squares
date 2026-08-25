"""Smoke tests for the documented Python command surfaces."""

from __future__ import annotations

import subprocess
import sys

import pytest


@pytest.mark.parametrize(
    "module",
    [
        "cases.campaign_smoke.baseline_sweep",
        "cases.campaign_smoke.basin_entry_experiment",
        "cases.campaign_smoke.quench_experiment",
        "sqpack.campaign.ledger",
    ],
)
def test_help_is_read_only_and_self_documenting(module: str) -> None:
    completed = subprocess.run(
        [sys.executable, "-m", module, "--help"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    assert "usage:" in completed.stdout
    assert "Traceback" not in completed.stderr
