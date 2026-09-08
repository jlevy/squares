"""Known observations that the browser loading guard must refuse."""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import pytest
from nodejs_wheel import node

from devtools import check_math_faces
from devtools.check_math_loading import (
    ACTIVE_MATH_VARIANT,
    EARLY_EVENTS,
    EXPOSED,
    FIRST_PAINT_SCRIPT,
    FONT_LOAD_OBSERVER,
    HOLD_FONTS_SCRIPT,
    READOUTS,
    REQUIRED_FONTS,
    LoadingReport,
    Readout,
    loading_findings,
    no_javascript_findings,
    page_url,
    readout_findings,
)


def run_node(script: str) -> None:
    completed = node(
        ["-"], return_completed_process=True, input=script, capture_output=True, text=True
    )
    assert completed.returncode == 0, completed.stderr


def test_saved_font_variants_do_not_discard_hidden_certificates_or_bad_metadata() -> None:
    script = dedent("""
        const assert = require('node:assert/strict');
        const document = {documentElement: {dataset: {}}};
        const plain = {hidden: true, closest: () => null};
        const variant = (contexts, parent = plain) => ({
          dataset: {squaresMathContexts: contexts}, parentElement: parent,
          closest() { return this; }
        });
    """)
    script += f"const active = {ACTIVE_MATH_VARIANT};\n"
    script += dedent("""
        for (const fontSet of ['custom', 'system']) for (const proseFont of ['serif', 'sans']) {
          document.documentElement.dataset = {
            kpressFontSet: fontSet, kpressProseFont: proseFont};
          const key = `${fontSet}-${proseFont}`;
          const choices = ['custom-serif', 'custom-sans', 'system-serif', 'system-sans'];
          for (const context of choices) {
            assert.equal(active(variant(context)), context === key);
          }
          assert.equal(active(variant(choices.join(' '))), true);
          assert.equal(active(plain), true, 'hidden certificates remain intended math');
        }
        for (const contexts of ['', undefined, 'custom-mono', 'system-serif unknown']) {
          assert.throws(() => active(variant(contexts)), /malformed saved-font math variant/);
        }
        document.documentElement.dataset = {
          kpressFontSet: 'invalid', kpressProseFont: 'invalid'};
        assert.equal(active(variant('custom-serif')), true, 'invalid settings use defaults');
    """)
    run_node(script)


def test_first_exposure_discovery_never_requests_dormant_variant_fonts() -> None:
    script = dedent("""
        const assert = require('node:assert/strict');
        const checked = [];
        const variant = contexts => ({
          dataset: {squaresMathContexts: contexts}, parentElement: null});
        const formula = (id, contexts) => ({id,
          closest: () => contexts ? variant(contexts) : null,
          checkVisibility() { throw new Error('discovery must preserve hidden staging'); }});
        const maths = [formula('plain-hidden-certificate'), formula('selected', 'custom-serif'),
          formula('dormant', 'custom-sans')];
        const document = {documentElement: {dataset: {}}, querySelectorAll: () => maths};
        const MutationObserver = class { observe() {} };
        const requestAnimationFrame = () => {};
    """)
    script += FIRST_PAINT_SCRIPT.replace(
        REQUIRED_FONTS, "math => { checked.push(math.id); return []; }"
    )
    script += "assert.deepEqual(checked, ['plain-hidden-certificate', 'selected']);\n"
    run_node(script)


def clean_report() -> LoadingReport:
    return {
        "held_loads": 3,
        "sliders": 1,
        "early_targets": [{"id": "phi-example", "value": "2"}],
        "frames": 2,
        "math_font_checks": 1,
        "first_paint": {
            "faces": [
                {"family": "KaTeX_Main", "style": "normal", "weight": "400", "status": "loaded"}
            ],
            "required": [{"spec": "16px KaTeX_Main", "text": "x", "ready": True}],
        },
        "unready_math": [],
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
    assert report["first_paint"] is not None
    report["first_paint"]["required"] = [
        {"spec": "16px KaTeX_Size2", "text": "∑", "ready": False}
    ]
    assert any("KaTeX_Size2" in message for message in loading_findings(report))


def test_unused_registered_faces_are_not_part_of_the_visible_formula() -> None:
    report = clean_report()
    assert report["first_paint"] is not None
    report["first_paint"]["faces"] = [
        {"family": "KaTeX_Size2", "style": "normal", "weight": "400", "status": "unloaded"}
    ]
    assert loading_findings(report) == []


def test_readiness_is_checked_for_later_first_exposures_too() -> None:
    report = clean_report()
    report["unready_math"] = ["late sum: 16px KaTeX_Size2 [∑]"]
    assert any("unavailable required faces" in message for message in loading_findings(report))


def test_an_unobserved_first_visible_formula_cannot_pass() -> None:
    report = clean_report()
    assert report["first_paint"] is not None
    report["first_paint"]["required"] = []
    assert any("no observed glyph closure" in message for message in loading_findings(report))


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
          load(...args) {
            calls.push(['set', ...args]);
            return Promise.resolve(args[0].includes('excluded') ? [] : ['matched face']);
          }
          check(spec, text) { return spec === '16px test' && text === 'x'; }
        }};
        assert.equal(typeof FontFaceSet, 'undefined');
    """)
    script += HOLD_FONTS_SCRIPT
    script += dedent("""
        (async () => {
        let matchedDone = false, emptyDone = false;
        const requests = [new FontFace().load('face argument'),
          document.fonts.load('12px test').then(() => { matchedDone = true; }),
          document.fonts.load('12px excluded').then(() => { emptyDone = true; })];
        assert.equal(document.fonts.check('16px test', 'x'), true);
        assert.deepEqual(await __mathLoadControl.nativeLoad('16px test'), ['matched face'],
          'the independent observer bypasses the test gate');
        await Promise.resolve();
        assert.equal(__mathLoadControl.heldLoads, 2);
        assert.equal(matchedDone, false);
        assert.equal(emptyDone, true, 'excluded Unicode/system families must not be held');
        assert.equal(calls.some(([kind]) => kind === 'face'), false);
        __mathLoadControl.release();
        await Promise.all(requests);
        assert.equal(matchedDone, true);
        assert.equal(document.fonts.check('16px missing', 'x'), false);
        assert.deepEqual(calls, [['set', '12px test'], ['set', '12px excluded'],
          ['set', '16px test'], ['face', 'face argument']]);
        })().catch(error => { console.error(error); process.exitCode = 1; });
    """)
    run_node(script)


def test_required_fonts_split_families_and_include_hidden_staging() -> None:
    script = dedent("""
        const assert = require('node:assert/strict');
        const NodeFilter = {SHOW_TEXT: 4};
        const parent = family => ({
          style: {fontStyle: 'normal', fontWeight: '400', fontSize: '16px', fontFamily: family},
          checkVisibility: () => false,
        });
        const composite = '"KPress Math, Text Sans",KaTeX_Main,serif';
        const nodes = [
          {textContent: 'x1', parentElement: parent(composite)},
          {textContent: '1≈', parentElement: parent(composite)},
          {textContent: '∑', parentElement: parent('KaTeX_Size2')},
        ];
        const getComputedStyle = node => node.style;
        const html = {};
        const document = {createTreeWalker(node) {
          assert.equal(node, html);
          let index = -1;
          return {nextNode() { return ++index < nodes.length; },
            get currentNode() { return nodes[index]; }};
        }};
        const math = {querySelector: selector => {
          assert.equal(selector, '.katex-html'); return html;
        }};
        const checked = [];
        const observe = (spec, text) => {
          checked.push({spec, text}); return {ready: !spec.includes('KaTeX_Main')};
        };
    """)
    script += f"const result = ({REQUIRED_FONTS})(math, observe);\n"
    script += dedent("""
        assert.deepEqual(checked, [
          {spec: 'normal 400 16px "KPress Math, Text Sans"', text: 'x1≈'},
          {spec: 'normal 400 16px KaTeX_Main', text: 'x1≈'},
          {spec: 'normal 400 16px serif', text: 'x1≈'},
          {spec: 'normal 400 16px KaTeX_Size2', text: '∑'},
        ]);
        assert.equal(result[0].ready, true);
        assert.equal(result[1].ready, false,
          'a loaded first family cannot hide a pending later relation face');
        assert.equal(result[2].ready, true);
        assert.equal(result[3].ready, true);
    """)
    run_node(script)


def test_the_font_oracle_observes_promises_instead_of_a_lying_check_api() -> None:
    script = dedent("""
        const assert = require('node:assert/strict');
        const requests = [];
        const load = (spec, text) => new Promise((resolve, reject) => {
          requests.push({spec, text, resolve, reject});
        });
        const document = {fonts: {check: () => true}};
        const face = {family: 'KaTeX_Main', style: 'normal', weight: '400',
          unicodeRange: 'U+2265', status: 'error'};
    """)
    script += f"const observe = ({FONT_LOAD_OBSERVER})(load);\n"
    script += dedent("""
        (async () => {
        const spec = 'normal 400 16px "KaTeX_Main"';
        assert.equal(observe(spec, '≥').ready, false);
        assert.equal(observe(spec, '≥').outcome, 'pending');
        assert.equal(requests.length, 1, 'identical descriptions share an observed promise');
        assert.equal(document.fonts.check(spec, '≥'), true,
          'the WebKit false-positive must not make the oracle ready');
        requests[0].resolve([face]);
        await Promise.resolve();
        assert.equal(observe(spec, '≥').ready, false,
          'a resolved promise with an error face is still unavailable');
        assert.equal(observe(spec, '≥').faces[0].status, 'error');
        face.status = 'loaded';
        assert.equal(observe(spec, '≥').ready, true);

        assert.equal(observe('normal 400 16px serif', '≥').ready, false);
        requests[1].resolve([]);
        await Promise.resolve();
        assert.equal(observe('normal 400 16px serif', '≥').ready, true,
          'a system family or excluded Unicode range needs no declared face');

        observe(spec, '≈');
        requests[2].reject(new Error('required face failed'));
        await Promise.resolve();
        assert.equal(observe(spec, '≈').ready, false);
        assert.equal(observe(spec, '≈').outcome, 'rejected');
        assert.match(observe(spec, '≈').error, /required face failed/);
        observe('italic 400 16px "KaTeX_Main"', '≥');
        observe('normal 700 16px "KaTeX_Main"', '≥');
        observe('normal 400 18px "KaTeX_Main"', '≥');
        observe('normal 400 16px "KaTeX_AMS"', '≥');
        assert.equal(requests.length, 7, 'style, weight, size, family, and text key the cache');
        })().catch(error => { console.error(error); process.exitCode = 1; });
    """)
    run_node(script)


@pytest.mark.parametrize("kind", ["raw_tex", "native_math", "prepared_math"])
def test_no_javascript_accepts_each_complete_readable_representation(kind: str) -> None:
    assert no_javascript_findings({"math_wrappers": 1, "unreadable_math": 0, kind: 1}) == []


def test_one_visible_fallback_does_not_cover_another_clipped_formula() -> None:
    findings = no_javascript_findings(
        {"math_wrappers": 2, "unreadable_math": 1, "prepared_math": 1}
    )
    assert findings == ["no JavaScript: 1 formulas have no readable fallback"]
    assert no_javascript_findings({})


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
        const sans = {closest: selector => selector.includes('kpress-math-face') ? {} : null};
        const dormant = {dataset: {squaresMathContexts: 'system-sans'}, parentElement: null};
        const output = text => ({querySelectorAll: selector => selector === '.katex'
          ? [{closest: () => dormant}, sans]
          : [{textContent: 'stale dormant source', closest: () => dormant},
            {textContent: text, closest: () => null}]});
        const elements = {
          'phi-example': {value: '196'},
          'kslider-example': {value: '123', getAttribute: () => 'Direction 123 of 448'},
          's-phi-example': output('19.600^{\\circ}'),
          'kval-example': output('k = 123')
        };
        const document = {getElementById: id => elements[id], documentElement: {dataset: {}}};
        const targets = [{id: 'phi-example', value: '412'},
          {id: 'kslider-example', value: '7'}];
    """)
    script += f"const readouts = ({READOUTS})(targets);\n"
    script += dedent(r"""
        assert.equal(readouts[0].expected_source, '41.200^{\\circ}');
        assert.equal(readouts[0].actual_value, '196');
        assert.equal(readouts[0].source, '19.600^{\\circ}');
        assert.equal(readouts[1].expected_source, 'k = 7');
        assert.equal(readouts[1].actual_value, '123');
        assert.equal(readouts[1].source, 'k = 123');
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
