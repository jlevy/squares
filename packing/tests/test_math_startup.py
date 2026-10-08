"""Natural startup observations must preserve behavior and reject missing coverage."""

from __future__ import annotations

import math
from pathlib import Path

import pytest
from nodejs_wheel import node

from devtools import check_math_startup
from devtools.check_math_startup import (
    JsonRecord,
    delay_findings,
    run_measurements,
    startup_findings,
    summarize,
)

NODE = Path(__file__).resolve().parent / "node" / "math_startup"

#: `parameters_ready_ms` and `runtime_available_ms` of each control in the full-mode
#: self-test of Pages run 37898417552 (typography job 113716869137), in launch order.
#: The first two launches carry launch cost; every later undelayed load is about 15 ms.
RECORDED_SELF_TEST = {
    "control": (173, 162),
    "no-warmup": (125.10000000000582, 123.10000000000582),
    "delayed": (317, 9),
    "variants": (16.60000000000582, 11.30000000000291),
    "wrong-active-variant": (None, 9.5),
    "missing-math": (None, 9.099999999991269),
    "missing-counters": (14.19999999999709, 9.5),
    "late-target": (14.5, 9.700000000011642),
    "width-change": (324.8000000000029, 10.099999999991269),
    "missing-anchors": (15, 9.69999999999709),
}


def self_test_observations(**overrides: tuple[float | None, float | None]) -> JsonRecord:
    return {
        control: {"metrics": {"parameters_ready_ms": ready, "runtime_available_ms": runtime}}
        for control, (ready, runtime) in (RECORDED_SELF_TEST | overrides).items()
    }


def clean_report() -> JsonRecord:
    snapshot = {
        "width": 1280,
        "height": 720,
        "scroll_x": 0,
        "scroll_y": 0,
        "document_scroll_x": 0,
        "document_scroll_y": 0,
        "visibility": "visible",
        "focused": True,
        "active_certificates": ["test"],
    }
    return {
        "metrics": dict.fromkeys(
            (
                "instrumentation_installed_ms",
                "first_ready_call_ms",
                "initial_ready_end_ms",
                "first_prose_math_ms",
                "first_caption_math_ms",
                "parameters_ready_ms",
                "math_ready_marker_ms",
            ),
            1,
        ),
        "counters": {
            "frames": 1,
            "font_hooks": 2,
            "katex_hooks": 1,
            "runtime_hooks": 2,
            "ready_calls": 1,
            "render_calls": 1,
            "anchor_samples": 3,
        },
        "targets": [
            {"id": f"target-{index}", "correct": True, "exposed": True} for index in range(14)
        ],
        "anchors": [
            {"category": category, "samples": 1}
            for category in ("prose", "caption", "parameter")
        ],
        "snapshots": [snapshot, snapshot.copy()],
        "errors": [],
        "findings": [],
    }


def test_complete_first_frame_is_valid_without_a_movement_or_latency_verdict() -> None:
    report = clean_report()
    report["pre_reveal_frame_observed"] = False
    report["metrics"].update(anchor_max_displacement_px=200, parameters_ready_ms=3000)
    assert startup_findings(report, width=1280, height=720) == []


def test_parameter_mode_requires_math_but_explicitly_omits_all_page_geometry() -> None:
    report = clean_report()
    report["mode"] = "parameters"
    report["anchors"] = []
    report["counters"]["anchor_samples"] = 0
    report["metrics"].pop("first_prose_math_ms")
    report["metrics"].pop("first_caption_math_ms")
    assert startup_findings(report, width=1280, height=720) == []
    report["targets"][0]["exposed"] = False
    assert any(
        "incorrect parameter math: target-0" in finding
        for finding in startup_findings(report, width=1280, height=720)
    )


@pytest.mark.parametrize("mode", ["full", "parameters"])
def test_a_late_additional_target_invalidates_an_otherwise_complete_run(mode: str) -> None:
    report = clean_report()
    report["mode"] = mode
    report["targets"].append({"id": "late-target", "correct": True, "exposed": True})
    assert "expected 14 active parameter targets, found 15" in startup_findings(
        report, width=1280, height=720
    )


def test_unknown_measurement_mode_cannot_silently_skip_coverage() -> None:
    report = clean_report()
    report["mode"] = "unknown"
    assert "unknown startup measurement mode: unknown" in startup_findings(
        report, width=1280, height=720
    )


def test_initially_hidden_figures_remain_measurable_but_final_selection_is_required() -> None:
    report = clean_report()
    report["snapshots"][0].update(active_certificates=[], math_ready=False)
    assert startup_findings(report, width=1280, height=720) == []
    report["snapshots"][-1].update(active_certificates=[], math_ready=True)
    assert "expected exactly one active certificate" in startup_findings(
        report, width=1280, height=720
    )


def test_unused_warmup_is_optional_but_rendering_or_hydration_must_be_observed() -> None:
    report = clean_report()
    report["counters"].update(ready_calls=0, render_calls=0, hydrate_calls=14)
    report["metrics"].pop("first_ready_call_ms")
    report["metrics"]["initial_ready_end_ms"] = None
    assert startup_findings(report, width=1280, height=720) == []
    report["counters"]["hydrate_calls"] = 0
    assert "no observed math rendering or hydration activity" in startup_findings(
        report, width=1280, height=720
    )


@pytest.mark.parametrize(
    ("section", "key", "value", "message"),
    [
        ("counters", "font_hooks", 0, "missing instrumentation: font_hooks"),
        ("counters", "anchor_samples", 0, "missing instrumentation: anchor_samples"),
        (
            "metrics",
            "parameters_ready_ms",
            None,
            "missing startup milestone: parameters_ready_ms",
        ),
        (
            "metrics",
            "first_prose_math_ms",
            math.nan,
            "missing startup milestone: first_prose_math_ms",
        ),
    ],
)
def test_missing_instrumentation_invalidates_the_run(
    section: str, key: str, value: float | None, message: str
) -> None:
    report = clean_report()
    report[section][key] = value
    assert message in startup_findings(report, width=1280, height=720)


def test_a_missing_parameter_and_no_adjacent_caption_text_are_not_fast_success() -> None:
    report = clean_report()
    report["targets"].pop()
    report["targets"][0]["correct"] = False
    report["anchors"] = [
        anchor for anchor in report["anchors"] if anchor["category"] != "caption"
    ]
    findings = startup_findings(report, width=1280, height=720)
    assert any("expected 14" in message for message in findings)
    assert any("incorrect parameter math: target-0" in message for message in findings)
    assert "no readable neighboring text anchors: caption" in findings


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("scroll_y", 10, "startup changed viewport state: scroll_y"),
        ("width", 390, "viewport dimensions changed during startup"),
        ("visibility", "hidden", "page was not visible and focused during startup"),
        ("focused", False, "page was not visible and focused during startup"),
        ("active_certificates", [], "expected exactly one active certificate"),
    ],
)
def test_startup_viewport_changes_are_reported(field: str, value: object, message: str) -> None:
    report = clean_report()
    report["snapshots"][-1][field] = value
    assert message in startup_findings(report, width=1280, height=720)


def test_summaries_retain_missing_values_and_the_full_observed_range() -> None:
    runs = [
        {"metrics": {"parameters_ready_ms": 100, "layout_shift_score": None}},
        {"metrics": {"parameters_ready_ms": 200, "layout_shift_score": None}},
        {"metrics": {"parameters_ready_ms": 150, "layout_shift_score": None}},
        {"metrics": {"parameters_ready_ms": None}},
    ]
    summary = summarize(runs)
    assert summary["parameters_ready_ms"] == {
        "count": 3,
        "missing": 1,
        "median": 150,
        "min": 100,
        "max": 200,
    }
    assert summary["layout_shift_score"] == {
        "count": 0,
        "missing": 4,
        "median": None,
        "min": None,
        "max": None,
    }


def test_launch_cost_on_the_first_controls_cannot_hide_the_injected_delay() -> None:
    # Against the first control alone this run kept only 317 - 173 = 144 ms of the delay.
    assert delay_findings(self_test_observations()) == []


def test_a_delay_the_readiness_milestone_does_not_show_is_still_reported() -> None:
    findings = delay_findings(self_test_observations(delayed=(17, 9)))
    assert len(findings) == 2
    assert all(
        finding.startswith("the delayed control did not record the known 300 ms delay")
        for finding in findings
    )


def test_launch_cost_on_the_delayed_load_cannot_stand_in_for_the_delay() -> None:
    # Launch cost holds this load's runtime back to 180 ms, so readiness at 190 ms clears
    # the fastest undelayed control by over 150 ms with none of the delay in it.
    assert delay_findings(self_test_observations(delayed=(190, 180))) == [
        (
            "the delayed control did not record the known 300 ms delay:"
            " ready 10 ms after its math runtime arrived"
        )
    ]


@pytest.mark.parametrize(
    "overrides",
    [
        {"delayed": (None, 9)},
        {"delayed": (317, None)},
        {"control": (None, 162), "no-warmup": (None, 123), "variants": (None, 11)},
    ],
)
def test_a_missing_delay_milestone_is_not_a_recorded_delay(
    overrides: dict[str, tuple[float | None, float | None]],
) -> None:
    assert delay_findings(self_test_observations(**overrides))


def test_matched_runs_are_sequential_and_reverse_order_without_discarding_failures(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sources = {"control": "/tmp/control.html", "candidate": "https://example.test/squares/"}
    calls: list[Path | str] = []

    def measure(path: Path | str, **_options: object) -> JsonRecord:
        calls.append(path)
        return {
            "metrics": {"parameters_ready_ms": len(calls)},
            "findings": ["known fault"] if len(calls) == 3 else [],
        }

    monkeypatch.setattr(check_math_startup, "measure_startup", measure)
    report = run_measurements(sources, runs=3)
    assert calls == [
        sources[label]
        for label in ("control", "candidate", "candidate", "control", "control", "candidate")
    ]
    assert [run["pair"] for run in report["runs"]] == [1, 1, 2, 2, 3, 3]
    assert report["findings"] == ["candidate pair 2: known fault"]
    assert report["summary"]["candidate"]["parameters_ready_ms"]["count"] == 3


def test_parameter_mode_is_forwarded_and_retained_in_paired_reports(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    modes: list[object] = []

    def measure(_path: Path | str, **options: object) -> JsonRecord:
        modes.append(options["mode"])
        return {"mode": options["mode"], "metrics": {}, "findings": []}

    monkeypatch.setattr(check_math_startup, "measure_startup", measure)
    report = run_measurements({"page": "/tmp/page.html"}, runs=2, mode="parameters")
    assert modes == ["parameters", "parameters"]
    assert report["mode"] == "parameters"
    assert all(run["mode"] == "parameters" for run in report["runs"])


def test_pass_through_instrumentation_keeps_native_promises_and_return_values() -> None:
    completed = node(
        [str(NODE / "pass-through-instrumentation.mjs")],
        return_completed_process=True,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr


def test_cli_requires_complete_pairs_and_positive_run_counts() -> None:
    for args in (["--control", "control.html"], ["--runs", "0"], ["--width", "0"]):
        with pytest.raises(SystemExit) as error:
            check_math_startup.main(args)
        assert error.value.code == 2


@pytest.mark.parametrize("wait", [300, 0, None, math.nan])
def test_known_delay_uses_its_readiness_wait_even_after_a_slow_navigation(
    monkeypatch: pytest.MonkeyPatch, wait: float | None
) -> None:
    required_findings = {
        "missing-math": "incorrect parameter math",
        "wrong-active-variant": "incorrect parameter math",
        "missing-counters": "missing instrumentation: font_hooks",
        "late-target": "expected 14 active parameter targets, found 15",
    }

    def measure(path: Path, **_options: object) -> JsonRecord:
        control = path.stem
        return {
            "metrics": {
                "finish_validation_ms": 1,
                "parameters_ready_ms": 325.9 if control == "delayed" else 200.9,
                "initial_ready_wait_ms": wait if control == "delayed" else 0,
            },
            "counters": {
                "ready_calls": 0 if control == "no-warmup" else 1,
                "anchor_samples": 0,
            },
            "findings": [required_findings[control]] if control in required_findings else [],
        }

    monkeypatch.setattr(check_math_startup, "measure_startup", measure)
    report = check_math_startup.self_test(mode="parameters")
    expected = (
        [] if wait == 300 else ["the delayed control did not record the known 300 ms delay"]
    )
    assert report["findings"] == expected
