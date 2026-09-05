"""Smoke tests for the documented Python command surfaces."""

from __future__ import annotations

import subprocess
import sys
from importlib.metadata import version

import pytest

CONSOLE_SCRIPTS = [
    "sqpack.campaign.runner",
    "sqpack.campaign.ledger",
    "sqpack.cli.validate",
    "sqpack.cli.witness",
]
"""The four `[project.scripts]` entry points, by module, so the test needs no install."""


def _run(module: str, flag: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", module, flag],
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.mark.parametrize(
    "module",
    [
        "cases.campaign_smoke.baseline_sweep",
        "cases.campaign_smoke.basin_entry_experiment",
        "cases.campaign_smoke.quench_experiment",
        *CONSOLE_SCRIPTS,
    ],
)
def test_help_is_read_only_and_self_documenting(module: str) -> None:
    completed = _run(module, "--help")

    assert completed.returncode == 0, completed.stderr
    assert "usage:" in completed.stdout
    assert "Traceback" not in completed.stderr


@pytest.mark.parametrize("module", CONSOLE_SCRIPTS)
def test_console_scripts_report_the_installed_version(module: str) -> None:
    """`--version` answers from the distribution metadata, on stdout, with exit 0."""
    completed = _run(module, "--version")

    assert completed.returncode == 0, completed.stderr
    assert completed.stdout.rstrip().endswith(version("sqpack"))
    assert completed.stderr == ""
