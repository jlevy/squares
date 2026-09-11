"""The publication pass changes math slots, preserving the rest of the source."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import asyncio
import base64
import json
import re
from io import BytesIO
from pathlib import Path
from textwrap import dedent
from typing import TYPE_CHECKING, Any, cast

import pytest
from nodejs_wheel import node

if TYPE_CHECKING:
    from playwright.async_api import Route

from devtools import prepare_explainer_math, render_explainer
from devtools.prepare_explainer_math import (
    GeometryBox,
    GeometryReport,
    MathCoverage,
    PreparedFragment,
    QueueWatchdogReport,
    carrier_font_css,
    coverage_findings,
    font_preference_html,
    geometry_findings,
    held_math_fonts,
    math_slots,
    prepared_html,
)


def test_math_slots_preserve_nested_semantics_and_ignore_script_examples() -> None:
    source = dedent("""
        <html><head><script>const example = '<span class="tex">x</span>';</script></head>
        <body><p>Before <span class="tex">x &lt; 2</span> after.</p>
        <span class="kpress-math"><span class="kpress-math-render">\\(y\\)</span>
        <span class="kpress-math-semantic"><math><mi>y</mi></math></span></span>
        <dd id="s-phi-19-5"></dd><div id="kval-381-100"></div></body></html>
    """)
    slots = math_slots(source)
    assert len(slots) == 4
    fragments: list[PreparedFragment] = [
        {"key": index, "html": f"reserved {index}", "attributes": {}}
        for index in range(len(slots))
    ]
    result = prepared_html(source, slots, fragments)
    assert "<script>const example = '<span class=\"tex\">x</span>';</script>" in result
    assert '<p>Before <span class="tex">reserved 0</span> after.</p>' in result
    assert '<span class="kpress-math">reserved 1</span>' in result
    assert '<dd id="s-phi-19-5">reserved 2</dd>' in result
    assert '<div id="kval-381-100">reserved 3</div>' in result


def test_preparation_must_return_every_slot_and_only_math_attributes() -> None:
    source = '<p><span class="tex">x</span><span class="tex">y</span></p>'
    slots = math_slots(source)
    with pytest.raises(ValueError, match="exactly once"):
        prepared_html(source, slots, [{"key": 0, "html": "x", "attributes": {}}])
    with pytest.raises(ValueError, match="non-math attribute"):
        prepared_html(
            source,
            slots,
            [
                {"key": 0, "html": "x", "attributes": {"onclick": "bad()"}},
                {"key": 1, "html": "y", "attributes": {}},
            ],
        )


def test_prepared_source_attributes_are_escaped_without_rewriting_the_container() -> None:
    source = "<p><span class='tex' title='keep this'>x</span></p>"
    slots = math_slots(source)
    result = prepared_html(
        source,
        slots,
        [
            {
                "key": 0,
                "html": '<span class="katex">x</span>',
                "attributes": {
                    "data-kpress-math-source": 'x < "2" & y',
                    "data-kpress-math-prepared": "true",
                },
            }
        ],
    )
    assert "class='tex' title='keep this'" in result
    assert 'data-kpress-math-source="x &lt; &quot;2&quot; &amp; y"' in result
    assert '<span class="katex">x</span></span></p>' in result


def test_cli_prepares_before_comparing_or_writing_the_publication_artifact(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    page = tmp_path / "index.html"
    page.write_text("<p>prepared</p>")
    (tmp_path / render_explainer.MARKDOWN_OUTPUT.name).write_text("the Markdown edition")
    monkeypatch.setattr(
        render_explainer,
        "render",
        lambda *_args, **_kwargs: render_explainer.Render(
            page="<p>raw</p>", markdown="the Markdown edition"
        ),
    )

    def prepare(source: str) -> str:
        assert source == "<p>raw</p>"
        return "<p>prepared</p>"

    monkeypatch.setattr("devtools.prepare_explainer_math.prepare_math_html", prepare)
    assert render_explainer.main(["--output", str(page), "--prepare-math", "--check"]) == 0
    assert render_explainer.main(["--output", str(page), "--check"]) == 1
    monkeypatch.setattr(render_explainer, "COMPOSITE_ASSETS", ())
    page.write_text("stale")
    assert render_explainer.main(["--output", str(page), "--prepare-math"]) == 0
    assert page.read_text() == "<p>prepared</p>"
    assert (page.parent / render_explainer.MARKDOWN_OUTPUT.name).read_text() == (
        "the Markdown edition"
    )


def test_the_exposure_rule_reads_the_observation_its_exemptions_came_from() -> None:
    """A box the probe's own substitution reveals is not an exposed box (D-491).

    `early_ready` can only name a box the font evidence saw, and that evidence is gathered
    before the carrier face and the `.katex` substitution go in. Judging exposure against
    `before`, which is measured after them, condemns every box those styles reveal. PR
    149's webkit job failed that way twice on `--prose-font sans` at 1280: no box was
    visible when the evidence was taken, eighteen were visible in `before`, and all
    eighteen moved 0.0000px across font arrival.
    """
    held: list[GeometryBox] = [
        {
            "key": key,
            "group": 0,
            "x": 12,
            "y": 24,
            "width": 30,
            "height": 20,
            "baseline": 40,
            "intrinsic_width": 30,
            "hidden": hidden,
        }
        for key, hidden in ((0, True), (1, False))
    ]
    arrived: list[GeometryBox] = [{**box, "hidden": False} for box in held]

    # Key 1 is visible in `before` only because the substitution revealed it: the evidence
    # saw nothing, so nothing was exposed while its requests were held.
    assert geometry_findings(held, arrived, exposed_early=frozenset()) == []

    # The rule keeps its teeth. A box the evidence did see visible, and could not admit,
    # is still an exposed box -- whether or not `before` agrees that it was visible.
    assert any(
        "exposed while its font requests were held" in message
        for message in geometry_findings(held, arrived, exposed_early=frozenset({1}))
    )
    assert (
        geometry_findings(
            held, arrived, exposed_early=frozenset({1}), early_ready=frozenset({1})
        )
        == []
    )

    # Omitted, the rule falls back to `before`'s own flags, which is what every caller
    # without the evidence still gets.
    assert any(
        "exposed while its font requests were held" in message
        for message in geometry_findings(held, arrived)
    )


def test_geometry_oracle_requires_hidden_then_visible_unchanged_boxes_and_line_breaks() -> None:
    before: list[GeometryBox] = [
        {
            "key": 0,
            "group": 0,
            "x": 12,
            "y": 24,
            "width": 30,
            "height": 20,
            "baseline": 40,
            "intrinsic_width": 50,
            "hidden": True,
        },
        {
            "key": 1,
            "group": 0,
            "x": 42,
            "y": 24,
            "width": 25,
            "height": 20,
            "baseline": 40,
            "intrinsic_width": 37,
            "hidden": True,
        },
    ]
    after: list[GeometryBox] = [
        {**box, "hidden": False, "intrinsic_width": box["width"]} for box in before
    ]
    assert geometry_findings(before, after) == []
    after[1] = {**after[1], "y": 50, "baseline": 66}
    findings = geometry_findings(before, after)
    assert any("moved 26.000px" in finding for finding in findings)
    assert any("line wrapping changed" in finding for finding in findings)
    assert geometry_findings(before, [])
    assert geometry_findings(before, before)
    assert geometry_findings(after, after)
    before[0] = {**before[0], "hidden": False}
    after = [{**box, "hidden": False, "intrinsic_width": box["width"]} for box in before]
    assert geometry_findings(before, after)
    assert geometry_findings(before, after, early_ready=frozenset({0})) == []
    assert geometry_findings(after, after, early_ready=frozenset({0, 1}))
    before[0] = {**before[0], "width": 42, "hidden": True}
    after[0] = {**after[0], "width": 42}
    assert any(
        "reserved width differs" in message for message in geometry_findings(before, after)
    )
    after[0] = {**after[0], "text_rendering": "auto"}
    assert any(
        "linear glyph metrics" in message for message in geometry_findings(before, after)
    )
    after[0] = {**after[0], "native_linear_metrics": True}
    assert not any(
        "linear glyph metrics" in message for message in geometry_findings(before, after)
    )


def test_font_hold_rewrites_actual_math_transfers_and_leaves_reading_faces_embedded() -> None:
    source = """<style>
@font-face { font-family: 'PT Serif'; src: url(data:font/woff2;base64,YWJj); }
@font-face { font-family: 'KPress Math Text'; src: url(data:font/woff2;base64,YWJj); }
@font-face { font-family: KaTeX_Main; src: url(data:font/woff2;base64,ZGVm); }
</style>"""
    output, fonts = held_math_fonts(source)
    assert output.count("data:font/woff2;base64,YWJj") == 1
    assert sorted(fonts.values()) == [b"abc", b"def"]
    assert all(url in output for url in fonts)


def test_held_font_responses_all_start_before_any_waits_for_completion() -> None:
    """Serialized WebKit fulfills can spend the real runtime's entire font timeout."""
    started: set[str] = set()
    payloads: dict[str, bytes] = {}

    async def exercise() -> None:
        all_started = asyncio.Event()

        class Request:
            def __init__(self, url: str) -> None:
                self.url = url

        class HeldResponse:
            def __init__(self, url: str) -> None:
                self.request = Request(url)

            async def fulfill(
                self, *, body: bytes, content_type: str, headers: dict[str, str]
            ) -> None:
                assert content_type == "font/woff2"
                assert headers == {"access-control-allow-origin": "*"}
                started.add(self.request.url)
                if len(started) == 3:
                    all_started.set()
                await all_started.wait()
                payloads[self.request.url] = body

        fonts = {f"font-{index}": bytes([index]) for index in range(3)}
        held = cast("list[Route]", [HeldResponse(url) for url in fonts])
        await asyncio.wait_for(
            prepare_explainer_math.release_held_fonts(held, fonts), timeout=1
        )
        assert payloads == fonts

    asyncio.run(exercise())


def test_geometry_font_gate_starts_runtime_only_after_before_snapshot() -> None:
    """The geometry probe's own setup cannot consume KPress's timeout budget."""
    trace = prepare_explainer_math._GEOMETRY_FONT_TRACE  # noqa: SLF001
    exercise = dedent("""
        const assert = require('node:assert/strict');
        const starts = [];
        const postReleasePromise = Promise.resolve('post-release');
        const synchronousError = new Error('synchronous failure');
        const rejection = new Error('post-release rejection');
        let rejectedPromise;
        globalThis.kpressMathText = {
          render(source) { starts.push(['render', source, performance.now()]);
            if (source === 'post-release') return postReleasePromise;
            if (source === 'throw') throw synchronousError;
            if (source === 'reject') {
              rejectedPromise = Promise.reject(rejection); return rejectedPromise;
            }
            return Promise.resolve('rendered'); },
          hydrate(source) { starts.push(['hydrate', source, performance.now()]);
            return Promise.resolve('hydrated'); }
        };
        (async () => {
          const rendered = kpressMathText.render('x');
          const hydrated = kpressMathText.hydrate('y');
          await Promise.resolve();
          const beforeSnapshotCompleted = performance.now();
          assert.deepEqual(starts, []);
          assert.equal(__squaresGeometryFontTrace.first_math_request_ms, null);
          assert.equal(__squaresGeometryFontTrace.queued_calls, 2);
          assert.throws(() => __squaresReleaseGeometryFontGate(),
            /released before the before snapshot/);
          assert.deepEqual(starts, []);
          __squaresMarkGeometryBeforeSnapshotComplete();
          __squaresReleaseGeometryFontGate();
          assert.deepEqual(starts.map(call => call.slice(0, 2)),
            [['render', 'x'], ['hydrate', 'y']]);
          assert.ok(starts.every(call => call[2] >= beforeSnapshotCompleted));
          assert.ok(__squaresGeometryFontTrace.first_math_request_ms
            >= beforeSnapshotCompleted);
          assert.deepEqual(await Promise.all([rendered, hydrated]),
            ['rendered', 'hydrated']);
          assert.strictEqual(kpressMathText.render('post-release'), postReleasePromise);
          assert.throws(() => kpressMathText.render('throw'),
            error => error === synchronousError);
          const observedRejection = kpressMathText.render('reject');
          assert.strictEqual(observedRejection, rejectedPromise);
          await assert.rejects(observedRejection, /post-release rejection/);
          assert.deepEqual(__squaresGeometryFontTrace.rejections.map(entry => entry.source),
            ['throw', 'reject']);
          process.stdout.write('complete');
        })().catch(error => { console.error(error); process.exitCode = 1; });
    """)
    completed = node(
        ["-"],
        return_completed_process=True,
        input=trace + exercise,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    assert completed.stdout == "complete"


@pytest.mark.parametrize("font_set", ["custom", "system"])
@pytest.mark.parametrize("prose_font", ["serif", "sans"])
def test_font_preferences_apply_before_bootstrap_and_math(
    font_set: str, prose_font: str
) -> None:
    source = "<html><head><script>bootstrap()</script></head><body>math</body></html>"
    output = font_preference_html(source, prose_font=prose_font, font_set=font_set)
    assert output.index(f'kpressProseFont = "{prose_font}"') < output.index("bootstrap()")
    assert output.index(f'kpressFontSet = "{font_set}"') < output.index("bootstrap()")
    assert output.endswith("<body>math</body></html>")
    with pytest.raises(ValueError, match="unsupported"):
        font_preference_html(source, prose_font="unmeasured", font_set=font_set)


def test_geometry_coverage_rejects_missing_formulas_and_unreserved_bases() -> None:
    coverage: MathCoverage = {
        "targets": 5,
        "formulas": 5,
        "bases": 7,
        "missing": [],
        "unreserved": [],
        "variant_errors": [],
        "duplicate_ids": [],
    }
    assert coverage_findings(coverage) == []
    assert any(
        "lack reservations" in finding
        for finding in coverage_findings({**coverage, "unreserved": ["x + y"]})
    )
    assert any(
        "no prepared formula" in finding
        for finding in coverage_findings({**coverage, "missing": ["x + y"]})
    )
    assert coverage_findings({**coverage, "bases": 0})
    assert coverage_findings({**coverage, "variant_errors": ["x + y"]})
    assert coverage_findings({**coverage, "duplicate_ids": ["formula-1"]})


def test_carrier_font_control_changes_only_line_metrics_of_shipped_glyphs() -> None:
    """The cross-platform control needs different struts, not different mathematics."""
    from fontTools.ttLib import TTFont  # noqa: PLC0415

    path = render_explainer.kpress_static() / "fonts" / "pt-serif-latin-400-normal.woff2"
    original_bytes = path.read_bytes()
    source = (
        '@font-face{font-family:"PT Serif";font-style:normal;'
        "src:url(data:font/woff2;base64,"
        + base64.b64encode(original_bytes).decode("ascii")
        + ")}"
    )
    css = carrier_font_css(source)
    data = re.search(r"base64,([A-Za-z0-9+/=]+)", css)
    assert data is not None
    original = TTFont(BytesIO(original_bytes))
    controlled = TTFont(BytesIO(base64.b64decode(data.group(1))))
    head: Any = original["head"]
    vertical: Any = controlled["hhea"]
    os2: Any = controlled["OS/2"]
    units = int(head.unitsPerEm)
    assert vertical.ascent == round(1.8 * units)
    assert vertical.descent == -round(0.2 * units)
    assert os2.sTypoAscender == vertical.ascent
    assert os2.sTypoDescender == vertical.descent
    assert os2.usWinAscent == vertical.ascent
    assert os2.usWinDescent == -vertical.descent
    assert vertical.lineGap == os2.sTypoLineGap == 0
    assert controlled.getBestCmap() == original.getBestCmap()
    assert controlled.getTableData("glyf") == original.getTableData("glyf")
    assert controlled["hmtx"].metrics == original["hmtx"].metrics
    assert path.read_bytes() == original_bytes
    with pytest.raises(ValueError, match="no shipped prose face"):
        carrier_font_css("<html>no embedded fonts</html>")


def test_cli_retains_raw_control_reports_and_automatic_provenance(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """The JSON transport retains observations, not only the guard's verdict."""
    source = tmp_path / "input.html"
    source.write_text("<html><head></head><body>prepared fixture</body></html>")
    output = tmp_path / "report.json"

    def check(_source: str, **options: object) -> GeometryReport:
        assert options["prose_font"] == "sans"
        assert options["font_set"] == "system"
        findings = []
        if options.get("break_reservation"):
            findings.append("base 0: width moved 12.000px")
        if options.get("wrong_reservation"):
            findings.append("base 0: reserved width differs from glyphs by 12.000px")
        if options.get("missing_reservation"):
            findings.append("visible math bases lack reservations: ['x + y']")
        if "{line-height:1.2!important}" in _source:
            findings.append("base 0: baseline moved 4.000px")
        coverage: MathCoverage = {
            "targets": 1,
            "formulas": 1,
            "bases": 1,
            "missing": [],
            "unreserved": [],
            "variant_errors": [],
            "duplicate_ids": [],
        }
        return {
            "browser": "fixture",
            "width": 1280,
            "medium": "screen",
            "alternate_certificate": False,
            "prose_font": "sans",
            "font_set": "system",
            "held_fonts": 1,
            "font_timing": {
                "first_math_request_ms": 20,
                "first_font_request_ms": 30,
                "release_started_ms": 200,
                "release_completed_ms": 210,
                "held_ms": 170,
                "release_ms": 10,
                "rejections": [],
            },
            "before": [],
            "after": [],
            "early_visible": [],
            "coverage_before": coverage,
            "coverage_after": coverage,
            "environment": {
                "browser": "fixture",
                "browser_version": "1.2.3",
                "viewport": {"width": 1280, "height": 960},
                "media": "screen",
                "recorded_at": "2026-09-08T00:00:00+00:00",
            },
            "source_identity": {
                "title": "Fixture",
                "publication_date": "DRAFT v0.2.4-12345678",
                "revision_url": None,
            },
            "findings": findings,
        }

    def check_queue(_source: str, **options: object) -> QueueWatchdogReport:
        return {
            "before": {
                "delayed_batches": 1,
                "root_pending": False,
                "unsubmitted_formulas": 1,
                "observed_ms": 3020,
                "target_classes": {"tex": 1},
                "exposed": ["x + y"] if options.get("break_queue") else [],
            },
            "held_fonts": 1,
            "queued_remaining": 0,
            "unreadable_after": [],
            "findings": ["math exposed while queued after watchdog: ['x + y']"]
            if options.get("break_queue")
            else [],
            "environment": check(_source, **options)["environment"],
        }

    monkeypatch.setattr(prepare_explainer_math, "check_queue_watchdog", check_queue)
    monkeypatch.setattr(prepare_explainer_math, "check_geometry", check)
    monkeypatch.setattr(
        prepare_explainer_math,
        "check_preparation_metrics",
        lambda **_options: {
            "positive": {"fontSize": 18, "width": 72, "linearWidth": 72},
            "controls": {
                "hinted_metrics": {"error": "math preparation requires geometricPrecision"},
                "nonlinear_scaling": {"error": "math width does not scale linearly"},
            },
        },
    )
    arguments = [
        str(source),
        "--self-test",
        "--prose-font",
        "sans",
        "--font-set",
        "system",
        "--output",
        str(output),
    ]
    assert prepare_explainer_math.main(arguments) == 0
    report = json.loads(output.read_text())
    assert report["requested_source"] == str(source.resolve())
    assert report["source_identity"]["publication_date"] == "DRAFT v0.2.4-12345678"
    assert report["instrument"]["entry_point"] == "devtools.prepare_explainer_math"
    assert report["instrument"]["command_arguments"] == arguments
    assert len(report["instrument"]["git_head"]) == 40
    assert isinstance(report["instrument"]["git_dirty"], bool)
    assert report["instrument"]["browser_versions"] == ["fixture 1.2.3"]
    assert report["font_set"] == "system"
    assert report["prose_font"] == "sans"
    assert report["coverage_after"]["unreserved"] == []
    assert report["font_timing"]["held_ms"] == 170
    assert report["font_timing"]["release_ms"] == 10
    assert report["font_timing"]["rejections"] == []
    assert "missing_reservation" in report["controls"]
    assert "unprotected_queue" in report["controls"]
    assert "unreserved_carrier" in report["controls"]
    assert report["queue_watchdog"]["findings"] == []
    assert report["preparation_metrics"]["positive"]["linearWidth"] == 72
    assert {"hinted_metrics", "nonlinear_scaling"} <= report["controls"].keys()
    for control in report["controls"].values():
        assert control["rejected"] is True
        assert control["report"]["findings"]
        assert control["report"]["environment"]["viewport"] == {"width": 1280, "height": 960}


def test_checker_report_cannot_overwrite_its_input_html(tmp_path: Path) -> None:
    source = tmp_path / "input.html"
    source.write_text("prepared HTML")
    with pytest.raises(SystemExit) as error:
        prepare_explainer_math.main([str(source), "--output", str(source)])
    assert error.value.code == 2
    assert source.read_text() == "prepared HTML"
