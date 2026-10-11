"""Actual stored #451 outcomes bind complete source and native inputs without decisions."""

from __future__ import annotations

import copy
from fractions import Fraction
from pathlib import Path

import pytest

from devtools import couzo_refinement_reports as reports
from devtools import run_negative_controls as controls


@pytest.fixture
def private_inputs(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    original_repo, packet = reports.REPO, reports.PACKET
    repo = tmp_path / "private"
    for original in reports.private_input_paths():
        landing = repo / original.relative_to(original_repo)
        landing.parent.mkdir(parents=True, exist_ok=True)
        landing.write_bytes(original.read_bytes())
    monkeypatch.setattr(reports, "REPO", repo)
    monkeypatch.setattr(reports.kernel, "REPO", repo)
    monkeypatch.setattr(reports, "PACKET", repo / packet.relative_to(original_repo))

    def forbidden(*_args, **_kwargs):
        pytest.fail("source custody ran a geometric decision")

    monkeypatch.setattr(reports.kernel, "run_case", forbidden)
    monkeypatch.setattr(reports.legacy, "exact_verify", forbidden)
    monkeypatch.setattr(reports.legacy.independent, "check_squares", forbidden)


@pytest.mark.parametrize(
    "kind", ["verdict", "limitations", "input", "source", "decimal", "map"]
)
@pytest.mark.usefixtures("private_inputs")
def test_last_complete_private_input_mutation_refuses_then_restores(kind: str) -> None:
    assert tuple(reports.check_certification()) == reports.NUMBERS
    target = (
        reports.receipt_path()
        if kind in {"verdict", "limitations", "input"}
        else reports.fact_path()
    )
    if kind == "map":
        target = reports.private_input_paths()[0]
    original = target.read_bytes()
    try:
        if kind == "map":
            target.write_bytes(original + b"\n")
        else:
            value = copy.deepcopy(reports.kernel.read_xz(target))
            row = value["cases"][-1]
            if kind == "verdict":
                assert row["exact_verify"]["verification_passed"] is False
                row["exact_verify"]["verification_passed"] = True
            elif kind == "limitations":
                row["independent"]["limitations"] = "Global optimality is proved."
            elif kind == "input":
                x = row["checker_input"]["poses"][-1][0]
                row["checker_input"]["poses"][-1][0] = str(Fraction(x) + 1)
            elif kind == "source":
                row["source_certificate"] += "\n"
            else:
                row["decimal_pose"] += "\n"
            reports.kernel.save_xz(target, value)
        with pytest.raises(reports.kernel.ReportError):
            reports.check_certification()
    finally:
        target.write_bytes(original)
    assert tuple(reports.check_certification()) == reports.NUMBERS
    assert target.read_bytes() == original


def test_production_private_roster_carries_all_three_complete_inputs() -> None:
    assert len(reports.private_input_paths()) == 3
    assert set(reports.private_input_paths()) <= set(controls.COPY_SEPARATELY)


@pytest.mark.parametrize("output", ["facts", "receipt"])
@pytest.mark.usefixtures("private_inputs")
def test_linked_producer_output_refuses_before_any_source_read_or_child(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, output: str
) -> None:
    target = reports.fact_path() if output == "facts" else reports.receipt_path()
    external = tmp_path / "external-output"
    original = target.read_bytes()
    external.write_bytes(original)
    target.unlink()
    target.symlink_to(external)

    def forbidden(*_args, **_kwargs):
        pytest.fail("producer did work before checking its private output")

    monkeypatch.setattr(reports, "source_pins", forbidden)
    monkeypatch.setattr(reports, "read_facts", forbidden)
    monkeypatch.setattr(reports, "run_child", forbidden)
    producer = (
        reports.import_facts
        if output == "facts"
        else lambda: reports.certify(tmp_path / "must-not-exist")
    )
    with pytest.raises(reports.kernel.ReportError, match="must remain private"):
        producer()
    assert external.read_bytes() == original
    assert not (tmp_path / "must-not-exist").exists()
