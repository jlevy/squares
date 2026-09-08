"""The recorded timing verdict refuses missing pairs and changing regimes."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

import pytest

from devtools.report_math_startup import CAMPAIGN, interval, paired_result, render


def samples() -> list[dict[str, Any]]:
    return [
        {
            "pair": pair,
            "label": label,
            "metrics": {"parameters_ready_ms": value},
            "findings": [],
            "environment": {
                "browser": "chromium",
                "browser_version": "pinned",
                "viewport": {"width": 1280, "height": 720},
                "browser_cache": "fresh",
                "os_cache": "uncontrolled",
            },
        }
        for pair in range(1, 13)
        for label, value in (("control", pair * 100), ("candidate", pair * 75))
    ]


RULE = {"metric": "parameters_ready_ms", "minimum_pairs": 12, "maximum_ci95_change_pct": -10}


def test_paired_verdict_is_based_on_relative_changes() -> None:
    result = paired_result(samples(), RULE)
    assert result["change_pct"] == -25
    assert result["ci95"] == (-25, -25)
    assert result["passes"]
    assert interval([-1.0, 0.0, 2.0, 10.0]) == interval([-1.0, 0.0, 2.0, 10.0])


def test_no_change_cannot_pass_the_registered_threshold() -> None:
    runs = samples()
    for pair in range(0, len(runs), 2):
        runs[pair + 1]["metrics"] = deepcopy(runs[pair]["metrics"])
    assert not paired_result(runs, RULE)["passes"]


@pytest.mark.parametrize("defect", ["missing", "duplicate", "regime", "zero", "invalid"])
def test_invalid_measurements_are_not_dropped(defect: str) -> None:
    runs = samples()
    if defect == "missing":
        runs.pop()
    elif defect == "duplicate":
        runs.append(deepcopy(runs[0]))
    elif defect == "regime":
        runs[0]["environment"]["browser_version"] = "different"
    elif defect == "zero":
        runs[0]["metrics"]["parameters_ready_ms"] = 0
    else:
        runs[0]["findings"] = ["incorrect parameter math"]
    expected = {
        "missing": "unmatched",
        "duplicate": "duplicate",
        "regime": "mixes",
        "zero": "nonpositive",
        "invalid": "validity findings",
    }
    with pytest.raises(ValueError, match=expected[defect]):
        paired_result(runs, RULE)


def test_retained_records_validate_and_ledger_is_current() -> None:
    assert (CAMPAIGN / "ledger.md").read_text() == render()
