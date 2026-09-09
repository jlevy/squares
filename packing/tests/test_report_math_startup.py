"""The recorded timing verdict refuses missing pairs and changing regimes."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from devtools import report_math_startup
from devtools.report_math_startup import (
    CAMPAIGN,
    geometry_result,
    interval,
    paired_result,
    render,
    startup_diagnostics,
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


def diagnostic_samples() -> list[dict[str, Any]]:
    runs = samples()
    for run in runs:
        ready = run["metrics"]["parameters_ready_ms"]
        run["metrics"]["runtime_available_ms"] = 40
        run["counters"] = {"katex_calls": 0, "render_calls": 0, "hydrate_calls": 211}
        run["fonts"] = [
            {"start_ms": 10, "end_ms": 20, "outcome": "resolved"},
            {"start_ms": 15, "end_ms": 45, "outcome": "resolved"},
        ]
        run["targets"] = [
            {
                "id": identifier,
                "slug": "19-5",
                "correct": True,
                "exposed": True,
                "first_visible_ms": ready - 20 if identifier.startswith("s-") else ready,
            }
            for identifier in [
                *(f"figure6-19-5-label-{index}" for index in range(8)),
                *(f"s-{key}-19-5" for key in ("phi", "theta", "d", "D", "B", "prod")),
            ]
        ]
    return runs


def test_startup_diagnostics_derive_promise_durations_and_complete_readout_gap() -> None:
    runs = diagnostic_samples()
    original = deepcopy(runs)
    decision = paired_result(runs, RULE)
    text = "\n".join(startup_diagnostics(runs))
    assert "| Runtime available (ms) | 40.0 (40.0 to 40.0) |" in text
    assert "| Runtime hydrate calls | 211.0 (211.0 to 211.0) |" in text
    assert "| Font load calls | 2.0 (2.0 to 2.0) |" in text
    assert "| Per-run median font promise (ms) | 20.0 (20.0 to 20.0) |" in text
    assert "| Per-run longest font promise (ms) | 30.0 (30.0 to 30.0) |" in text
    assert "| All six dynamic readouts exposed (ms) | 630.0 (80.0 to 1180.0) |" in text
    assert "| Dynamic readouts to all fourteen (ms) | 20.0 (20.0 to 20.0) |" in text
    assert "not isolated font-decoding measurements" in text
    assert runs == original
    assert paired_result(runs, RULE) == decision


def test_startup_diagnostics_are_optional_for_older_reports() -> None:
    assert startup_diagnostics(samples()) == []


@pytest.mark.parametrize("defect", ["missing", "negative", "pending"])
def test_font_diagnostics_do_not_drop_incomplete_or_invalid_requests(defect: str) -> None:
    runs = diagnostic_samples()
    font = runs[0]["fonts"][0]
    if defect == "missing":
        del font["end_ms"]
    elif defect == "negative":
        font["end_ms"] = 0
    else:
        font["outcome"] = "pending"
    text = "\n".join(startup_diagnostics(runs))
    assert "Font load calls" in text
    assert "Per-run median font promise" not in text
    assert "Per-run longest font promise" not in text


@pytest.mark.parametrize("defect", ["missing", "duplicate", "slug", "incorrect", "time"])
def test_readout_diagnostics_require_all_fourteen_mapped_targets(defect: str) -> None:
    runs = diagnostic_samples()
    targets = runs[0]["targets"]
    if defect == "missing":
        targets.pop()
    elif defect == "duplicate":
        targets[-1]["id"] = targets[-2]["id"]
    elif defect == "slug":
        targets[-1]["slug"] = "381-100"
    elif defect == "incorrect":
        targets[-1]["correct"] = False
    else:
        targets[0]["first_visible_ms"] += 1
    text = "\n".join(startup_diagnostics(runs))
    assert "Runtime hydrate calls" in text
    assert "dynamic readouts" not in text
    assert "Dynamic readouts to all fourteen" not in text


def test_parameter_confirmation_refuses_wrong_mode_and_excessive_observer_cost() -> None:
    rule = {**RULE, "required_mode": "parameters", "maximum_sampler_fraction": 0.1}
    runs = samples()
    with pytest.raises(ValueError, match="mode"):
        paired_result(runs, rule)
    for run in runs:
        run["mode"] = "parameters"
        run["metrics"]["sampler_total_ms"] = 1
    assert paired_result(runs, rule)["passes"]
    for run in runs:
        if run["label"] == "candidate":
            run["metrics"]["sampler_total_ms"] = run["metrics"]["parameters_ready_ms"] * 0.2
    with pytest.raises(ValueError, match="sampler overhead"):
        paired_result(runs, rule)


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
    box = {"key": 1, "group": 0, "x": 0, "y": 0, "width": 20, "height": 16, "baseline": 12}
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


FONT_CONTEXTS = ["custom-serif", "custom-sans", "system-serif", "system-sans"]
SAVED_SETTINGS_RULE = {**GEOMETRY_RULE, "font_contexts": FONT_CONTEXTS}


def saved_setting_reports() -> list[dict[str, Any]]:
    reports = []
    for context in FONT_CONTEXTS:
        for report in geometry_reports():
            report["font_set"], report["prose_font"] = context.split("-")
            for stage in ("before", "after"):
                # One formula can legitimately contain several unbreakable bases.
                report[stage].append({**report[stage][0], "key": 2, "x": 20})
                report[f"coverage_{stage}"] = {
                    "targets": 1,
                    "formulas": 1,
                    "bases": 2,
                    "missing": [],
                    "unreserved": [],
                    "variant_errors": [],
                    "duplicate_ids": [],
                }
            report["controls"]["missing_reservation"] = {
                "rejected": True,
                "report": {"findings": ["unreserved base"]},
            }
            reports.append(report)
        printed = deepcopy(reports[-2])
        printed["medium"] = "print"
        printed["browser"] = "chromium"
        reports.append(printed)
    return reports


def test_saved_settings_require_complete_context_matrix_and_formula_coverage() -> None:
    reports = saved_setting_reports()
    assert geometry_result(reports, SAVED_SETTINGS_RULE)[1] == []
    assert any(
        "missing registered" in item
        for item in geometry_result(reports[:-2], SAVED_SETTINGS_RULE)[1]
    )
    reports[0]["coverage_before"]["unreserved"] = ["a surviving formula lost its box"]
    assert any(
        "incomplete before" in item for item in geometry_result(reports, SAVED_SETTINGS_RULE)[1]
    )
    reports[0]["coverage_before"]["unreserved"] = []
    del reports[0]["coverage_after"]
    assert any(
        "incomplete after" in item for item in geometry_result(reports, SAVED_SETTINGS_RULE)[1]
    )
    for report in reports:
        del report["controls"]["missing_reservation"]
    assert any(
        "pre-discovery" in item for item in geometry_result(reports, SAVED_SETTINGS_RULE)[1]
    )


@pytest.mark.parametrize("stage", ["before", "after"])
@pytest.mark.parametrize("defect", ["truncated", "duplicate", "formula_count", "regrouped"])
def test_saved_settings_reconcile_raw_boxes_with_coverage(stage: str, defect: str) -> None:
    reports = saved_setting_reports()
    report = reports[0]
    if defect == "truncated":
        report[f"coverage_{stage}"]["bases"] = 261
    elif defect == "duplicate":
        report[stage].append(deepcopy(report[stage][0]))
    elif defect == "formula_count":
        report[f"coverage_{stage}"]["formulas"] = 2
    else:
        for box in report[stage]:
            box["group"] = 99
    assert geometry_result(reports, SAVED_SETTINGS_RULE)[1]


@pytest.mark.parametrize("named", [["H-001"], ["H-004"], [], ["H-001", "H-004"]])
def test_render_dispatches_the_experiments_registered_geometry_rule(
    named: list[str], monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """The complete renderer must not apply H001's default-only rule to H004."""
    reports = geometry_reports()
    paths = []
    for index, report in enumerate(reports):
        path = tmp_path / f"report-{index}.json"
        path.write_text(json.dumps(report))
        paths.append(path.name)
    fixture: dict[str, dict[str, Any]] = {
        "explorations": {"X-001": {"proposes": ["H-001", "H-004"]}},
        "hypotheses": {
            identity: {**rule, "criterion": "geometry", "derived_from": ["X-001"]}
            for identity, rule in (("H-001", GEOMETRY_RULE), ("H-004", SAVED_SETTINGS_RULE))
        },
        "experiments": {
            "exp-001": {
                "title": "Geometry dispatch regression",
                "kind": "geometry",
                "hypotheses": named,
                "measurements": paths,
                "correctness": "passed",
                "judgment": "Fixture observations cover only default settings.",
            }
        },
    }
    (tmp_path / "ideas.md").write_text("H-001 H-004")
    monkeypatch.setattr(
        report_math_startup, "records", lambda _root, directory: fixture[directory]
    )
    if len(named) != 1:
        with pytest.raises(ValueError, match="exactly one geometry hypothesis"):
            render(tmp_path)
    elif named == ["H-001"]:
        assert "Decision: **accepted**" in render(tmp_path)
    else:
        result = render(tmp_path)
        assert "Decision: **invalid**" in result
        assert "custom-sans" in result
        assert "incomplete before formula coverage" in result
