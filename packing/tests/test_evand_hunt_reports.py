"""Custody, frozen comparisons and the retained exact replay of Evan Daniel's #465 pair."""

from __future__ import annotations

import json
import shutil
import subprocess
from collections.abc import Callable
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import evand_arrangement_reports as kernel
from devtools import evand_exact_certificates as legacy
from devtools import evand_hunt_reports as reports

#: The source checkers this packet pins against the issue-399 packet's identical copies.
CHECKERS = "packing/resources/web/evand-new-arrangements-2026-10-07/source/s12/search/exact"


@pytest.fixture
def private_packet(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A private copy of the packet, with the two checker copies its record names."""
    repo = tmp_path / "private"
    packet = repo / reports.PACKET.relative_to(reports.REPO)
    shutil.copytree(reports.PACKET, packet)
    shutil.copytree(reports.REPO / CHECKERS, repo / CHECKERS)
    monkeypatch.setattr(reports, "REPO", repo)
    monkeypatch.setattr(reports, "PACKET", packet)
    monkeypatch.setattr(kernel, "REPO", repo)
    return packet


def _receipt() -> dict[str, Any]:
    return kernel.read_xz(reports.receipt_path())


def test_custody_admits_both_certificates_at_the_sides_the_issue_prints() -> None:
    certificates = reports.read_facts()
    assert tuple(certificates) == reports.NUMBERS
    for n, certificate in certificates.items():
        assert len(certificate.poses) == n
        assert certificate.side == Fraction(reports.OFFERED[n])
    assert certificates[132].side == Fraction(
        2397419866449012645435948575487, 200000000000000000000000000000
    )


def test_claims_record_rebuilds_from_the_retained_houses() -> None:
    claims = reports.check_claims()
    rows = {row["n"]: row for row in claims["results"]}
    for row in rows.values():
        side, house = Fraction(row["exact_side"]), Fraction(row["house"]["exact_side"])
        assert side < house
        assert Fraction(row["house"]["below_by"]) == house - side
    assert rows[132]["house"]["result"] == "T-098"
    assert rows[155]["house"]["result"] == "T-115"
    assert 4.22e-3 < float(Fraction(rows[132]["house"]["below_by"])) < 4.23e-3
    assert 4.25e-6 < float(Fraction(rows[155]["house"]["below_by"])) < 4.26e-6
    assert "equal_side" not in rows[132]


def test_n155_matches_t128_bound_and_source_labeled_indices() -> None:
    row = {r["n"]: r for r in reports.check_claims()["results"]}[155]
    equal = row["equal_side"]
    assert equal["result"] == "T-128"
    assert equal["exact_side"] == row["exact_side"]
    assert equal["identical_poses"] == 152
    assert len(equal["differing_here"]) == len(equal["differing_there"]) == 3
    # The differing indices match the source's free/flat labels.
    assert equal["differing_here"] == equal["source_zero_mode_squares"] == [83, 134, 138]
    assert equal["differing_are_zero_modes"] is True


def test_zero_mode_squares_refuse_a_report_without_them(private_packet: Path) -> None:
    path = private_packet / "source" / reports.certificate_path(155).replace(".cert", ".json")
    report = json.loads(path.read_text())
    report["second_order"]["flat_squares"] = [155]
    path.write_text(json.dumps(report))
    with pytest.raises(reports.ReportError, match="free and flat squares"):
        reports.zero_mode_squares(155)


def test_receipt_admits_all_six_jobs_with_both_routes() -> None:
    positives = reports.check_certification()
    assert set(positives) == set(reports.NUMBERS)
    rows = _receipt()["cases"]
    assert [(row["n"], row["control"]) for row in rows] == [
        (n, control) for n in reports.NUMBERS for control in reports.JOBS
    ]
    assert sum(row[route]["pairs_tested"] for row in rows for route in reports.ROUTES) == 123486
    for n, margins in reports.margins(positives).items():
        for field in ("containment_clearance", "best_pair_gap"):
            assert margins[f"exact_verify_{field}"] == margins[f"independent_{field}"]
        assert margins["exact_verify_containment_clearance"] == "1/200000000000000000000"
        gap = Fraction(margins["exact_verify_best_pair_gap"])
        assert Fraction(9, 10**21) < gap < Fraction(1, 10**20), n


@pytest.mark.parametrize("mutation", ["certificate-byte", "extra-pose", "licence"])
def test_custody_refuses_a_changed_retained_file(private_packet: Path, mutation: str) -> None:
    source = private_packet / "source"
    path = source / reports.certificate_path(155)
    if mutation == "certificate-byte":
        text = path.read_text()
        path.write_text(
            text.replace("647624947200700369098292528347", "647624947200700369098292528348", 1)
        )
    elif mutation == "extra-pose":
        path.write_text(path.read_text() + "1/2 1/2 0\n")
    else:
        (source / "LICENSE").write_text("All rights reserved.\n")
    with pytest.raises(reports.ReportError, match="packet custody"):
        reports.read_facts()


@pytest.mark.parametrize("mutation", ["house-side", "identical-poses", "dropped-row"])
def test_claims_refuse_a_tampered_frozen_comparison(
    private_packet: Path, mutation: str
) -> None:
    path = private_packet / "acquisition/claims.json"
    claims = json.loads(path.read_text())
    if mutation == "house-side":
        claims["results"][0]["house"]["exact_side"] = "12"
    elif mutation == "identical-poses":
        claims["results"][1]["equal_side"]["identical_poses"] = 155
    else:
        claims["results"].pop()
    path.write_text(json.dumps(claims, indent=2) + "\n")
    with pytest.raises(reports.ReportError, match="frozen claim record"):
        reports.check_claims()


@pytest.mark.parametrize("kind", ["flipped-control", "moved-input", "reordered", "format"])
def test_receipt_mutations_refuse(private_packet: Path, kind: str) -> None:
    value = _receipt()
    cases = value["cases"]
    if kind == "flipped-control":
        cases[1]["independent"]["verification_passed"] = True
    elif kind == "moved-input":
        cases[0]["checker_input"]["poses"][0][0] = "1/3"
    elif kind == "reordered":
        cases[0], cases[3] = cases[3], cases[0]
    else:
        value["format"] = "evand-399-complete-exact-replay-v1"
    kernel.save_xz(reports.receipt_path(), value)
    assert private_packet in reports.receipt_path().parents
    with pytest.raises(kernel.ReportError):
        reports.check_certification()


@pytest.mark.parametrize("selection", [[], [132, 132], [True], [132, 133]])
def test_replay_selection_refuses_unknown_and_repeated_counts(selection: list[int]) -> None:
    with pytest.raises(reports.ReportError):
        reports.check_certification(selection)


def test_pose_comparison_needs_one_count_and_distinct_poses() -> None:
    first = legacy.parse("2 5\n1 1 0\n3 3 0\n")
    with pytest.raises(reports.ReportError, match="one count"):
        reports.pose_comparison(first, legacy.parse("1 5\n1 1 0\n"))
    with pytest.raises(reports.ReportError, match="repeats a pose"):
        reports.pose_comparison(first, legacy.parse("2 5\n1 1 0\n1 1 0\n"))
    assert reports.pose_comparison(first, legacy.parse("2 5\n3 3 0\n1 2 0\n")) == {
        "identical_poses": 1,
        "differing_here": [0],
        "differing_there": [1],
    }


def test_certify_refuses_an_invalid_allocation_or_a_reused_directory(tmp_path: Path) -> None:
    with pytest.raises(reports.ReportError, match="worker/deadline"):
        reports.certify(tmp_path / "jobs", workers=3)
    with pytest.raises(reports.ReportError, match="fresh attempt"):
        reports.certify(tmp_path)


def _fake_runner(
    monkeypatch: pytest.MonkeyPatch, outcome: Callable[[list[str]], bytes | None]
) -> list[list[str]]:
    """Replace the kernel's child process; ``outcome`` writes the output or times out."""
    commands: list[list[str]] = []

    def run(command: list[str], **options: Any) -> subprocess.CompletedProcess[bytes]:
        commands.append(command)
        assert options["capture_output"] is True
        payload = outcome(command)
        if payload is None:
            raise subprocess.TimeoutExpired(
                command, options["timeout"], output=b"partial out", stderr=b"partial err"
            )
        Path(command[-1]).write_bytes(payload)
        return subprocess.CompletedProcess(command, 0, b"native stdout", b"native stderr")

    monkeypatch.setattr(kernel.subprocess, "run", run)
    return commands


@pytest.mark.usefixtures("private_packet")
def test_driver_runs_this_module_and_keeps_a_timeout_failure_record(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    commands = _fake_runner(monkeypatch, lambda _command: None)
    before = reports.receipt_path().read_bytes()
    with pytest.raises(kernel.ReportError, match="exceeded 45s"):
        reports.certify(tmp_path / "jobs", workers=1, timeout=45)
    command = commands[0]
    assert command[2] == reports.MODULE
    assert command[command.index("--n") + 1] == "132"
    assert command[command.index("--control") + 1] == "positive"
    stem = tmp_path / "jobs" / "n132-positive"
    assert stem.with_suffix(".stdout.log").read_bytes() == b"partial out"
    assert stem.with_suffix(".stderr.log").read_bytes() == b"partial err"
    failure = json.loads(stem.with_suffix(".failure.json").read_text())
    assert failure == {
        "n": 132,
        "control": "positive",
        "status": "timeout",
        "timeout_seconds": 45,
    }
    assert reports.receipt_path().read_bytes() == before


@pytest.mark.usefixtures("private_packet")
@pytest.mark.parametrize("payload", [b'{"n":132,"n":155}', b"[]", b'{"n": 132}'])
def test_driver_refuses_duplicate_keys_and_incomplete_rows(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, payload: bytes
) -> None:
    _fake_runner(monkeypatch, lambda _command: payload)
    before = reports.receipt_path().read_bytes()
    with pytest.raises(kernel.ReportError):
        reports.certify(tmp_path / "jobs", workers=1, timeout=45)
    assert (tmp_path / "jobs" / "n132-positive.stdout.log").read_bytes() == b"native stdout"
    assert reports.receipt_path().read_bytes() == before
