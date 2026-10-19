"""Exercise the native acceptance verdict against incomplete and false-green reports."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from devtools.check_darwin_memory_results import EXPECTED_CASES, main
from sqpack.yamlio import safe_load


def _complete_report() -> ET.Element:
    root = ET.Element("testsuites")
    suite = ET.SubElement(root, "testsuite", tests="4", failures="0", errors="0", skipped="0")
    for name in EXPECTED_CASES:
        ET.SubElement(suite, "testcase", classname="tests.test_process_memory", name=name)
    return root


def test_complete_native_report_passes(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "native.xml"
    ET.ElementTree(_complete_report()).write(path)
    assert main([str(path)]) == 0
    assert "4 passed, zero skips" in capsys.readouterr().out


@pytest.mark.parametrize("report", ["missing", "empty", "no-suites", "no-cases"])
def test_absent_native_evidence_refuses(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], report: str
) -> None:
    path = tmp_path / "native.xml"
    if report == "empty":
        path.write_text("", encoding="utf-8")
    elif report == "no-suites":
        path.write_text("<testsuites/>", encoding="utf-8")
    elif report == "no-cases":
        path.write_text(
            '<testsuite tests="0" failures="0" errors="0" skipped="0"/>', encoding="utf-8"
        )
    assert main([str(path)]) == 1
    assert "Darwin memory acceptance failed:" in capsys.readouterr().err


@pytest.mark.parametrize("outcome", ["skipped", "failure", "error"])
@pytest.mark.parametrize("honest_totals", [False, True])
def test_nonpassing_native_case_refuses_even_with_false_green_totals(
    tmp_path: Path, outcome: str, *, honest_totals: bool
) -> None:
    root = _complete_report()
    case = next(root.iter("testcase"))
    ET.SubElement(case, outcome)
    if honest_totals:
        next(root.iter("testsuite")).set(
            {"failure": "failures", "error": "errors"}.get(outcome, outcome), "1"
        )
    path = tmp_path / "native.xml"
    ET.ElementTree(root).write(path)
    assert main([str(path)]) == 1


@pytest.mark.parametrize("identity", ["missing", "duplicate", "unexpected", "wrong-module"])
def test_native_case_identities_must_match(tmp_path: Path, identity: str) -> None:
    root = _complete_report()
    suite = next(root.iter("testsuite"))
    case = next(root.iter("testcase"))
    if identity == "missing":
        suite.remove(case)
    elif identity == "duplicate":
        case.set("name", EXPECTED_CASES[1])
    elif identity == "unexpected":
        case.set("name", "test_unrelated_positive_case")
    else:
        case.set("classname", "other.test_process_memory")
    path = tmp_path / "native.xml"
    ET.ElementTree(root).write(path)
    assert main([str(path)]) == 1


@pytest.mark.parametrize("counter", [None, "-1", "invalid", "3"])
def test_native_counters_are_required_and_exact(tmp_path: Path, counter: str | None) -> None:
    root = _complete_report()
    suite = next(root.iter("testsuite"))
    if counter is None:
        del suite.attrib["tests"]
    else:
        suite.set("tests", counter)
    path = tmp_path / "native.xml"
    ET.ElementTree(root).write(path)
    assert main([str(path)]) == 1


def test_macos_native_memory_step_selects_four_real_cases_and_preserves_bounds() -> None:
    path = Path(__file__).resolve().parents[2] / ".github/workflows/packing-validation.yml"
    jobs = safe_load(path.read_text(encoding="utf-8"))["jobs"]
    job = jobs["macos-portability"]
    assert job["timeout-minutes"] == 5
    assert job["if"] == "github.event_name != 'pull_request' || github.base_ref == 'main'"
    assert "macos-portability" not in jobs["packing-required"]["needs"]
    step = next(
        item
        for item in job["steps"]
        if item["name"] == "Native Darwin current memory and system SDK layout"
    )
    assert step["timeout-minutes"] == 1
    selected = [
        line.strip().removesuffix(" \\")
        for line in step["run"].splitlines()
        if line.strip().startswith("tests/test_process_memory.py::")
    ]
    assert selected == [f"tests/test_process_memory.py::{name}" for name in EXPECTED_CASES]
    assert "python -m devtools.check_darwin_memory_results" in step["run"]
    assert "$PACKING_VALIDATION_ARTIFACT_DIR/darwin-current-memory.xml" in step["run"]
