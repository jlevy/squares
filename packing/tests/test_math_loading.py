"""Known observations that the browser loading guard must refuse.

The probes are exercised against stand-ins by the Node scripts in `tests/node/math_loading/`,
one per test below; each script loads the probe files it tests.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from nodejs_wheel import node

from devtools import check_math_faces
from devtools.check_math_loading import (
    LoadingReport,
    Readout,
    loading_findings,
    no_javascript_findings,
    page_url,
    readout_findings,
)

NODE = Path(__file__).resolve().parent / "node" / "math_loading"


def run_node(script: str) -> None:
    completed = node(
        [str(NODE / script)], return_completed_process=True, capture_output=True, text=True
    )
    assert completed.returncode == 0, completed.stderr


def test_saved_font_variants_do_not_discard_hidden_certificates_or_bad_metadata() -> None:
    run_node("saved-font-variants.mjs")


def test_first_exposure_discovery_never_requests_dormant_variant_fonts() -> None:
    run_node("first-exposure-discovery.mjs")


def test_mutation_discovery_rescans_only_affected_math_and_global_style_changes() -> None:
    run_node("mutation-discovery.mjs")


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
    run_node("font-hold.mjs")


def test_required_fonts_split_families_and_include_hidden_staging() -> None:
    run_node("required-fonts.mjs")


def test_the_font_oracle_observes_promises_instead_of_a_lying_check_api() -> None:
    run_node("font-oracle.mjs")


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
    run_node("early-targets.mjs")


def test_readout_probe_uses_frozen_values_for_angles_and_directions() -> None:
    run_node("readouts.mjs")


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
    run_node("visibility.mjs")
