"""Regression coverage for the finite n=11 selection-routing controls."""

from __future__ import annotations

import json

import pytest

from devtools.check_n11_selection_routing import main


def test_finite_selection_routing_controls(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main() == 0
    summary = json.loads(capsys.readouterr().out)

    assert summary["relevant_availability_profiles_checked"] == 256
    assert summary["profiles_avoiding_G0"] == 225
    assert summary["maximal_products"] == 16
    assert [len(orbit) for orbit in summary["D4_orbits"]] == [4, 8, 4]
    assert [len(orbit) for orbit in summary["LB_orbits"]] == [1, 2, 2, 2, 2, 1, 2, 1, 2, 1]
    assert summary["incidence_counts"] == {
        "0": [1, 4, 6, 4, 1],
        "1": [8, 24, 24, 8],
    }
    assert summary["joint_four_parent_configurations_checked"] == 81
    assert summary["labels"] == [
        [1, 2, 13, 14],
        [0, 7, 13, 14],
        [1, 2, 8, 15],
    ]
    assert summary["core_containment_margin"] == "87879/2540000"
    assert summary["cross_corner_least_squared_distance"] == "34668544/10080625"
    assert summary["distant_wall_squared_margin"] == "43064/403225"
    assert summary["missing_mark_allowance"] == "517143/4000000"
    assert summary["result"] == (
        "PASS; synthetic exact arithmetic and combinatorics only; no scientific target"
    )
