"""Controls for the W5 wave-efficiency renderer.

The numbers it prints are field lookups over retained records, so the controls check
that it looks the right fields up, refuses when the records cannot support a row, and
prints the same figures under normal and optimized Python.
"""

from __future__ import annotations

import json
import subprocess
import sys

import pytest

from devtools.render_wave_efficiency import RefusalError, baseline, lane_row, render_markdown


def test_lane_row_is_a_lookup_over_the_declared_receipt() -> None:
    row = lane_row("session-075")

    assert row["status"] == "completed"
    assert row["cells"] == 7
    assert row["receipt"] == "packing/campaign/resource-usage/codex-task-tree-session-075.yaml"
    assert row["lower_bound"] is False
    assert row["agent_active_seconds"] == 5093.446
    assert row["tool_seconds"]["command"] == 804.037
    assert row["model_response_count"] == 212
    assert row["outputs"] == 8
    # The session record itself and the resource receipt are not substantive outputs.
    assert row["substantive_outputs"] == 6


def test_coordinator_is_shown_beside_the_lanes_and_never_summed() -> None:
    result = baseline(["session-073", "session-074", "session-075"], "session-072")

    totals = result["lane_totals"]
    assert totals["cells"] == 22
    assert totals["agent_active_seconds"] == 17294.963
    assert totals["lower_bound"] is True
    assert result["coordinator"]["session"] == "session-072"
    assert result["coordinator_residual_agent_active_seconds"] == round(
        25451.681 - 17294.963, 3
    )
    rendered = render_markdown(result)
    assert "| **Lane total** | **22 cells** |" in rendered
    assert "session-072 (coordinator, contains the lanes)" in rendered


def test_non_terminal_or_receiptless_sessions_are_refused() -> None:
    with pytest.raises(RefusalError, match="expected exactly one session record"):
        lane_row("session-999")
    with pytest.raises(RefusalError, match="expected one Codex receipt"):
        # session-071 declares only its own receipt under a different name pattern? No:
        # it declares codex-task-tree-session-071.yaml, so pick a Claude-only session.
        lane_row("session-047")


def test_cli_agrees_under_optimization() -> None:
    base = [
        "-m",
        "devtools.render_wave_efficiency",
        "--lanes",
        "session-073",
        "session-074",
        "session-075",
        "--coordinator",
        "session-072",
        "--format",
        "json",
    ]
    normal = subprocess.run([sys.executable, *base], check=True, capture_output=True, text=True)
    optimized = subprocess.run(
        [sys.executable, "-O", *base], check=True, capture_output=True, text=True
    )
    assert json.loads(normal.stdout) == json.loads(optimized.stdout)
