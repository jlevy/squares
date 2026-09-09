"""Natural startup observations must preserve behavior and reject missing coverage."""

from __future__ import annotations

import math
from pathlib import Path
from textwrap import dedent

import pytest
from nodejs_wheel import node

from devtools import check_math_startup
from devtools.check_math_startup import (
    STARTUP_SCRIPT,
    JsonRecord,
    run_measurements,
    startup_findings,
    summarize,
)


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
    script = dedent("""
        const assert = require('node:assert/strict');
        let resolveFace, resolveSet, resolveReady, resolveRender;
        const facePromise = new Promise(resolve => { resolveFace = resolve; });
        const setPromise = new Promise(resolve => { resolveSet = resolve; });
        const readyPromise = new Promise(resolve => { resolveReady = resolve; });
        const renderPromise = new Promise(resolve => { resolveRender = resolve; });
        globalThis.FontFace = class {
          family = 'probe'; style = 'normal'; weight = '400';
          load() { assert.equal(this.family, 'probe'); return facePromise; }
        };
        globalThis.document = {fonts: new class {
          load(value) { assert.equal(value, '16px probe'); return setPromise; }
          addEventListener() {}
        }, addEventListener() {}};
        globalThis.window = globalThis;
        globalThis.addEventListener = () => {};
        globalThis.requestAnimationFrame = () => {};
        globalThis.MutationObserver = class { observe() {} };
        assert.equal(typeof FontFaceSet, 'undefined');
    """)
    script += STARTUP_SCRIPT
    script += dedent("""
        const katexResult = Symbol('katex result');
        globalThis.katex = {render(source, target) {
          assert.equal(source, 'x'); assert.equal(target.id, 'math'); return katexResult;
        }};
        globalThis.kpressMathText = {
          ready() { return readyPromise; }, render() { return renderPromise; },
          hydrate() { return renderPromise; }
        };
        const target = {id: 'math'};
        assert.equal(new FontFace().load(), facePromise);
        assert.equal(document.fonts.load('16px probe'), setPromise);
        assert.equal(kpressMathText.ready(), readyPromise);
        assert.equal(kpressMathText.render('x', target), renderPromise);
        assert.equal(kpressMathText.hydrate('x', target), renderPromise);
        assert.equal(katex.render('x', target), katexResult);
        assert.equal(__mathStartup.counters.font_hooks, 2);
        assert.equal(__mathStartup.counters.runtime_hooks, 2);
        assert.equal(__mathStartup.counters.hydrate_hooks, 1);
        assert.equal(__mathStartup.counters.hydrate_calls, 1);
        assert.equal(__mathStartup.counters.katex_calls, 1);
        assert.ok(__mathStartup.katex[0].duration_ms >= 0);
        assert.equal(__mathStartup.fonts[0].outcome, 'pending');
        resolveFace(); resolveSet(); resolveReady(); resolveRender();
        Promise.resolve().then(() => {
          assert.ok(__mathStartup.fonts.every(record => record.outcome === 'resolved'));
          assert.equal(__mathStartup.ready[0].outcome, 'resolved');
          assert.equal(__mathStartup.renders[0].outcome, 'resolved');
          assert.equal(__mathStartup.hydrates[0].outcome, 'resolved');
          assert.ok(__mathStartup.fonts.every(record => record.end_ms >= record.start_ms));
        });
    """)
    completed = node(
        ["-"], return_completed_process=True, input=script, capture_output=True, text=True
    )
    assert completed.returncode == 0, completed.stderr


def test_cli_requires_complete_pairs_and_positive_run_counts() -> None:
    for args in (["--control", "control.html"], ["--runs", "0"], ["--width", "0"]):
        with pytest.raises(SystemExit) as error:
            check_math_startup.main(args)
        assert error.value.code == 2
