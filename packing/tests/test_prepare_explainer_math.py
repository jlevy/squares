"""The publication pass changes math slots, preserving the rest of the source."""

from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent

import pytest

from devtools import prepare_explainer_math, render_explainer
from devtools.prepare_explainer_math import (
    GeometryBox,
    GeometryReport,
    MathCoverage,
    PreparedFragment,
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


def test_cli_retains_raw_control_reports_and_automatic_provenance(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """The JSON transport retains observations, not only the guard's verdict."""
    source = tmp_path / "input.html"
    source.write_text("<html>prepared fixture</html>")
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

    monkeypatch.setattr(prepare_explainer_math, "check_geometry", check)
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
    assert "missing_reservation" in report["controls"]
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
