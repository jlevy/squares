"""Known observations that the browser loading guard must refuse."""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import pytest
from nodejs_wheel import node

from devtools import check_math_faces
from devtools.check_math_loading import (
    EARLY_EVENTS,
    EXPOSED,
    HOLD_FONTS_SCRIPT,
    READOUTS,
    LoadingReport,
    Readout,
    loading_findings,
    page_url,
    readout_findings,
)


def run_node(script: str) -> None:
    completed = node(
        ["-"], return_completed_process=True, input=script, capture_output=True, text=True
    )
    assert completed.returncode == 0, completed.stderr


def clean_report() -> LoadingReport:
    return {
        "held_loads": 3,
        "sliders": 1,
        "early_targets": [{"id": "phi-example", "value": "2"}],
        "frames": 2,
        "first_paint": {
            "faces": [
                {"family": "KaTeX_Main", "style": "normal", "weight": "400", "status": "loaded"}
            ]
        },
        "early_math": None,
        "fallback": None,
        "readouts": [],
        "no_javascript": {},
        "findings": [],
    }


@pytest.mark.parametrize(
    "url",
    [
        "https://jlevy.github.io/squares/",
        "https://jlevy.github.io/squares/?review=fonts#381-100",
        "http://127.0.0.1:8000/index.html",
    ],
)
def test_live_page_urls_are_preserved(url: str) -> None:
    assert page_url(url) == url


def test_local_pages_resolve_from_paths_and_strings(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    page = tmp_path / "page with spaces.html"
    monkeypatch.chdir(tmp_path)
    for value in (page, str(page), Path(page.name), page.name):
        assert page_url(value) == page.as_uri()


def test_math_faces_cli_preserves_the_live_url(monkeypatch: pytest.MonkeyPatch) -> None:
    url = "https://jlevy.github.io/squares/"

    def check(path: Path | str, *, width: int) -> check_math_faces.Report:
        assert path == url
        assert width == 390
        return {"nodes": 0, "marked": 0, "tables": [], "findings": []}

    monkeypatch.setattr(check_math_faces, "check", check)
    assert check_math_faces.main([url, "--width", "390"]) == 0


def test_construct_faces_are_part_of_first_visible_paint() -> None:
    report = clean_report()
    report["first_paint"] = {
        "faces": [
            {"family": "KaTeX_Size2", "style": "normal", "weight": "400", "status": "loading"}
        ]
    }
    assert any("KaTeX_Size2" in message for message in loading_findings(report))


def test_early_event_render_and_semantic_fallback_are_independent_failures() -> None:
    report = clean_report()
    report["early_math"] = "x = 1"
    report["fallback"] = "y = 2"
    findings = loading_findings(report)
    assert any("before font readiness" in message for message in findings)
    assert any("native MathML" in message for message in findings)


def test_a_vacuous_or_incomplete_probe_cannot_pass() -> None:
    report = clean_report()
    report["held_loads"] = 0
    report["frames"] = 0
    report["first_paint"] = None
    assert len(loading_findings(report)) == 3


def test_font_hold_intercepts_both_apis_without_a_fontfaceset_global() -> None:
    script = dedent("""
        const assert = require('node:assert/strict');
        const calls = [];
        globalThis.FontFace = class {
          load(...args) { calls.push(['face', ...args]); return Promise.resolve(this); }
        };
        const document = {fonts: new class {
          load(...args) { calls.push(['set', ...args]); return Promise.resolve([]); }
        }};
        assert.equal(typeof FontFaceSet, 'undefined');
    """)
    script += HOLD_FONTS_SCRIPT
    script += dedent("""
        const requests = [new FontFace().load('face argument'),
          document.fonts.load('12px test')];
        assert.equal(__mathLoadControl.heldLoads, 2);
        assert.deepEqual(calls, [], 'the real loaders must also be delayed');
        __mathLoadControl.release();
        Promise.all(requests).then(() => {
          assert.deepEqual(calls, [['face', 'face argument'], ['set', '12px test']]);
        });
    """)
    run_node(script)


def test_early_targets_survive_boot_resets_and_end_at_distinct_values() -> None:
    script = dedent("""
        const assert = require('node:assert/strict');
        const sliders = ['kslider-one', 'phi-one', 'kslider-two', 'phi-two'].map(id => ({
          id, min: '0', max: '450', step: '1', value: id.startsWith('phi-') ? '196' : '0',
          events: [], dispatchEvent() { this.events.push(this.value); }
        }));
        const initial = sliders.map(slider => slider.value);
        const document = {querySelectorAll: () => sliders};
        const window = {dispatchEvent() {
          sliders.forEach((slider, i) => { slider.value = initial[i]; });
        }};
    """)
    script += f"const targets = ({EARLY_EVENTS})();\n"
    script += dedent("""
        assert.equal(Object.isFrozen(targets), true);
        assert.equal(new Set(targets.map(target => target.value)).size, sliders.length);
        for (const [i, target] of targets.entries()) {
          assert.equal(Object.isFrozen(target), true);
          assert.notEqual(target.value, initial[i], 'dropping all input must change output');
          assert.notEqual(target.value, sliders[i].value,
            'boot resets cannot revise expectations');
          assert.equal(sliders[i].events.length, 2);
          assert.notEqual(sliders[i].events[0], sliders[i].events[1]);
          assert.equal(sliders[i].events[1], target.value);
        }
    """)
    run_node(script)


def test_readout_probe_uses_frozen_values_for_angles_and_directions() -> None:
    script = dedent(r"""
        const assert = require('node:assert/strict');
        const sans = {dataset: {kpressMathFace: 'sans'}};
        const elements = {
          'phi-example': {value: '196'},
          'kslider-example': {value: '123', getAttribute: () => 'Direction 123 of 448'},
          's-phi-example': {...sans, querySelector: () => ({textContent: '19.600^{\\circ}'})},
          'kval-example': {children: [sans], querySelector: () => ({textContent: 'k = 123'})}
        };
        const document = {getElementById: id => elements[id]};
        const targets = [{id: 'phi-example', value: '412'},
          {id: 'kslider-example', value: '7'}];
    """)
    script += f"const readouts = ({READOUTS})(targets);\n"
    script += dedent(r"""
        assert.equal(readouts[0].expected_source, '41.200^{\\circ}');
        assert.equal(readouts[0].actual_value, '196');
        assert.equal(readouts[1].expected_source, 'k = 7');
        assert.equal(readouts[1].actual_value, '123');
        assert.equal(readouts[1].state_matches, false);
        assert.ok(readouts.every(readout => readout.sans && readout.supported));
    """)
    run_node(script)


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("actual_value", "123", "slider value changed"),
        ("source", "k = 70", "stale readout"),
        ("state_matches", False, "accessible direction state"),
        ("sans", False, "lost sans math"),
    ],
)
def test_each_readout_contract_is_checked(field: str, value: object, message: str) -> None:
    readout: Readout = {
        "id": "kslider-example",
        "expected_value": "7",
        "actual_value": "7",
        "expected_source": "k = 7",
        "source": "k = 7",
        "sans": True,
        "state_matches": True,
        "supported": True,
    }
    assert readout_findings([readout]) == []
    changed: Readout = {**readout, field: value}  # pyright: ignore[reportAssignmentType]
    findings = readout_findings([changed])
    assert len(findings) == 1
    assert message in findings[0]


def test_visibility_requires_readable_geometry_after_ancestor_clipping() -> None:
    script = dedent("""
        const assert = require('node:assert/strict');
        const getComputedStyle = node => node.style;
        const element = (style = {}, width = 100, height = 20, parent = null) => ({
          style, parentElement: parent,
          checkVisibility(options) {
            assert.equal(options.opacityProperty, true);
            assert.equal(options.visibilityProperty, true);
            return true;
          },
          getBoundingClientRect: () => ({left: 0, top: 0, right: width, bottom: height,
            width, height})
        });
    """)
    script += f"const exposed = {EXPOSED};\n"
    script += dedent("""
        assert.equal(exposed(element()), true);
        assert.equal(exposed(element({}, 1, 1)), false,
          'clipped accessibility text is not visible');
        assert.equal(exposed(element({clipPath: 'inset(50%)'})), false);
        assert.equal(exposed(element({clipPath: 'inset(0px)'})), true);
        assert.equal(exposed(element({clip: 'rect(0px, 0px, 0px, 0px)'})), false);
        assert.equal(exposed(element({}, 100, 20, element({overflowX: 'hidden'}, 1))), false);
        assert.equal(exposed(element({}, 100, 20, element({clipPath: 'inset(50%)'}))), false);
        const frame = element({overflowY: 'hidden'}, 100, 720);
        const scroll = element({overflowY: 'auto'}, 100, 720, frame);
        scroll.scrollHeight = 10000; scroll.clientHeight = 720;
        const belowFold = element({}, 100, 20, scroll);
        belowFold.getBoundingClientRect = () => ({left: 0, top: 1000, right: 100,
          bottom: 1020, width: 100, height: 20});
        assert.equal(exposed(belowFold), true, 'scrolling can expose readable fallback');
    """)
    run_node(script)
