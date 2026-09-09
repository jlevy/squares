"""Opt-in full-checks workload for the maintained validation timing instrument.

This lives outside the ordinary test suite: selecting it measures the real gate,
including engine setup, and must never make that gate invoke itself recursively.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
EXPECTED = ROOT / "benchmarks/validation-efficiency/VE-003-checks.json"


def test_complete_checks_workload(capsys: pytest.CaptureFixture[str]) -> None:
    """Retain the complete CLI result before refusing failed or changed coverage."""
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "sqpack.cli.validate",
            "--checks",
            "--jobs",
            "3",
            "--inner-jobs",
            "1",
            "--format",
            "json",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=600,
        check=False,
    )
    with capsys.disabled():
        print(completed.stdout, end="")
        print(completed.stderr, end="", file=sys.stderr)
    assert completed.returncode == 0
    summary = json.loads(completed.stdout)
    expected = json.loads(EXPECTED.read_text())
    assert summary["selected_count"] == len(summary["results"]) == len(expected) == 48
    assert sorted(row["name"] for row in summary["results"]) == expected
    assert all(row["status"] == "passed" for row in summary["results"])
