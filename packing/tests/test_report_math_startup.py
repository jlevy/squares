"""The recorded timing verdict refuses missing pairs and changing regimes."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

import pytest

from devtools.report_math_startup import (
    CAMPAIGN,
    geometry_result,
    interval,
    paired_result,
    render,
)


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


def geometry_reports() -> list[dict[str, Any]]:
    box = {"key": 1, "x": 0, "y": 0, "width": 20, "height": 16, "baseline": 12}
    return [
        {
            "browser": browser,
            "width": width,
            "medium": "screen",
            "alternate_certificate": False,
            "held_fonts": 1,
            "before": [{**box, "hidden": True, "intrinsic_width": 25}],
            "after": [{**box, "hidden": False, "intrinsic_width": 20}],
            "findings": [],
            "controls": {
                name: {"rejected": True, "report": {"findings": ["known defect"]}}
                for name in ("removed_width", "stable_wrong_width")
            },
        }
        for browser in ("chromium", "firefox", "webkit")
        for width in (1280, 390)
    ]


GEOMETRY_RULE = {"widths": [1280, 390], "maximum_math_box_displacement_px": 1}


def test_geometry_requires_every_browser_width_and_actual_negative_controls() -> None:
    reports = geometry_reports()
    assert geometry_result(reports, GEOMETRY_RULE)[1] == []
    assert "missing registered" in geometry_result(reports[:-1], GEOMETRY_RULE)[1][0]
    for report in reports:
        report["controls"] = {}
    assert "missing rejected" in geometry_result(reports, GEOMETRY_RULE)[1][0]


@pytest.mark.parametrize("defect", ["movement", "wrong_width", "no_transition"])
def test_geometry_rechecks_measurements_instead_of_trusting_a_verdict(defect: str) -> None:
    reports = geometry_reports()
    if defect == "movement":
        reports[0]["after"][0]["x"] = 2
    elif defect == "wrong_width":
        reports[0]["after"][0]["intrinsic_width"] = 25
    else:
        reports[0]["before"][0]["hidden"] = False
    assert geometry_result(reports, GEOMETRY_RULE)[1]
