"""A summary audit preserves cohort flags and cannot manufacture disjoint blocks."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from workbench_tools.historical_summary_audit import audit


def test_retained_n17_level8_cells_are_unresolved_and_deep_level8_is_n11_only() -> None:
    repo = Path(__file__).resolve().parents[3]
    result = audit(
        json.loads((repo / "packing/campaign/results/annealing/summaries.json").read_text())
    )
    assert result["largest_recorded_n"] == 29
    cells = result["cells"]
    assert isinstance(cells, list)
    disputed = [
        cell
        for cell in cells
        if cell["n"] == 17 and cell["parameter_overrides"].get("anneal") == 8
    ]
    assert len(disputed) == 5
    assert {cell["recorded_rows"] for cell in disputed} == {2000}
    assert {cell["resolved_flag"] for cell in disputed} == {False}
    deep = [cell for cell in cells if cell["artifact"] == "a8-deep.jsonl"]
    assert [(cell["n"], cell["recorded_rows"]) for cell in deep] == [(11, 16319)]


def test_reconstruction_keeps_absolute_and_normalized_metrics_distinct() -> None:
    result = audit(
        {
            "control.jsonl": {
                "5": {
                    "trials": 2,
                    "resolved": False,
                    "record": 2.5,
                    "grid": 3,
                    "closed_median": -0.5,
                    "params": {},
                    "best_of": {"1": 0.25},
                }
            }
        }
    )
    cells = result["cells"]
    assert isinstance(cells, list)
    assert cells[0]["reconstructed_median_absolute_excess"] == 0.75
    assert cells[0]["reconstructed_median_relative_excess_pct"] == 30.0
    assert cells[0]["median_grid_gap_closed"] == -0.5
    assert cells[0]["prefix_observations"] == {"1": 0.25}
    assert "blocks" not in cells[0]
    assert (
        result["evidence"] == "historical summaries; raw geometry and seed blocks unavailable"
    )


def test_unretained_metadata_is_not_filled_with_invented_defaults() -> None:
    with pytest.raises(ValueError, match="trial counts"):
        audit({"bad.jsonl": {"5": {"resolved": True}}})
