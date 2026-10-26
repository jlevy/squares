"""Complete Gupta original-source admission and live mutation refusal."""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

import pytest

from devtools import gupta_refinement_reports as reports


@pytest.fixture
def packet(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    original = reports.PACKET
    monkeypatch.setattr(reports, "REPO", tmp_path)
    monkeypatch.setattr(reports, "PACKET", tmp_path / "packet")
    for relative in (
        "acquisition/case-inputs.json",
        "facts/complete-certificates-and-comparators.json.xz",
    ):
        target = reports.PACKET / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((original / relative).read_bytes())
    facts = reports.kernel.read_xz(reports.fact_path())
    assert len(reports.read_facts()) == 17
    return facts


def test_all_originals_comparators_and_control_inputs_are_complete(
    packet: dict[str, Any],
) -> None:
    facts = reports.read_facts()
    assert tuple(facts) == reports.NUMBERS
    assert sum(len(c.poses) for c in facts.values()) == 3017
    for n, certificate in facts.items():
        pin = reports.source_pins()[n]
        assert str(certificate.side) == pin["side_exact"]
        for control in reports.JOBS:
            actual = reports.kernel.job_input(certificate, control)
            deciding = reports.kernel.checker_input(actual)
            assert deciding["n"] == n
            assert len(deciding["poses"]) == n
            assert (
                deciding["poses"][-1] == reports.kernel.checker_input(certificate)["poses"][-1]
            )
    assert len(packet["cases"]) == 17


@pytest.mark.parametrize(
    "mutation",
    ["certificate", "comparator", "drop-last", "repeat-last", "bool-count", "extra-key"],
)
def test_late_original_mutations_refuse_before_any_native_decision(
    packet: dict[str, Any], mutation: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    changed = copy.deepcopy(packet)
    row = changed["cases"][-1]
    if mutation == "certificate":
        row["source_certificate"] += "\n"
    elif mutation == "comparator":
        row["source_comparator"] += "\n"
    elif mutation == "drop-last":
        changed["cases"].pop()
    elif mutation == "repeat-last":
        changed["cases"][-1] = copy.deepcopy(changed["cases"][-2])
    elif mutation == "bool-count":
        row["n"] = True
    else:
        row["extra"] = "unadmitted"
    reports.save_xz(reports.fact_path(), changed)
    monkeypatch.setattr(
        reports.kernel, "run_case", lambda *_a, **_kw: pytest.fail("native geometry called")
    )
    with pytest.raises(reports.kernel.ReportError):
        reports.read_fact(reports.NUMBERS[0])
    reports.save_xz(reports.fact_path(), packet)
    assert reports.read_fact(reports.NUMBERS[0]).n == reports.NUMBERS[0]


@pytest.mark.usefixtures("packet")
def test_trusted_acquisition_roster_is_checked_before_parsing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    path = reports.PACKET / "acquisition/case-inputs.json"
    raw = path.read_bytes()
    path.write_bytes(raw + b"\n")
    monkeypatch.setattr(
        reports.legacy, "parse", lambda *_a, **_kw: pytest.fail("unbound original parsed")
    )
    with pytest.raises(reports.kernel.ReportError, match="acquisition roster"):
        reports.read_facts()
    path.write_bytes(raw)


@pytest.mark.usefixtures("packet")
def test_linked_input_and_output_cannot_escape_private_repository(tmp_path: Path) -> None:
    outside = tmp_path.parent / (tmp_path.name + "-outside")
    outside.mkdir()
    original = reports.fact_path().read_bytes()
    target = outside / "complete.json.xz"
    target.write_bytes(original)
    reports.fact_path().unlink()
    reports.fact_path().symlink_to(target)
    with pytest.raises(reports.kernel.ReportError, match="private repository"):
        reports.read_facts()
    with pytest.raises(reports.kernel.ReportError, match="private repository"):
        reports.save_xz(reports.fact_path(), {})
    assert target.read_bytes() == original


@pytest.mark.parametrize("selection", [[], [88, 88], [True], [87]])
def test_replay_selection_refuses_empty_repeated_or_unknown_counts(
    selection: list[int], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        reports, "read_facts", lambda: pytest.fail("facts read before the selection")
    )
    with pytest.raises(reports.kernel.ReportError, match="replay selection"):
        reports.check_certification(selection, replay=True)


@pytest.fixture
def receipt(packet: dict[str, Any]) -> dict[str, Any]:
    """The packet fixture with the retained receipt beside its facts."""
    del packet
    original = (
        Path(reports.__file__).resolve().parents[1]
        / "resources/web/gupta-square-packing-refinements-2026-10-08"
        / "receipts/exact-certification.json.xz"
    )
    reports.receipt_path().parent.mkdir(parents=True, exist_ok=True)
    reports.receipt_path().write_bytes(original.read_bytes())
    return reports.kernel.read_xz(reports.receipt_path())


def test_a_replay_holds_fresh_jobs_to_the_retained_rows_and_writes_nothing(
    receipt: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    rows = {(row["n"], row["control"]): row for row in receipt["cases"]}
    decided: list[tuple[int, str]] = []

    def fresh(certificate: Any, control: str, **_kw: Any) -> dict[str, Any]:
        decided.append((certificate.n, control))
        # Measured times are not reproducible, and a replay does not compare them.
        return {**copy.deepcopy(rows[certificate.n, control]), "wall_seconds": 0.0}

    monkeypatch.setattr(reports.kernel, "run_case", fresh)
    before = reports.receipt_path().read_bytes()
    reports.check_certification([88, 239], replay=True)
    assert decided == [(n, control) for n in (88, 239) for control in reports.JOBS]
    assert reports.receipt_path().read_bytes() == before

    def moved(certificate: Any, control: str, **_kw: Any) -> dict[str, Any]:
        row = copy.deepcopy(rows[certificate.n, control])
        row["exact_verify"]["pairs_tested"] += 1
        return row

    monkeypatch.setattr(reports.kernel, "run_case", moved)
    with pytest.raises(reports.kernel.ReportError, match="differs from retained"):
        reports.check_certification([88], replay=True)
    assert reports.receipt_path().read_bytes() == before
