"""Complete #399 input custody, native decisions, controls and bounded evidence."""

from __future__ import annotations

import copy
import hashlib
import json
import lzma
import subprocess
from pathlib import Path
from typing import Any

import pytest

from devtools import evand_arrangement_reports as reports
from devtools import evand_exact_certificates as legacy


@pytest.fixture
def packet(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    """Three small complete inputs, decided by both real native routes."""
    numbers = (3, 4, 5)
    monkeypatch.setattr(reports, "REPO", tmp_path)
    monkeypatch.setattr(reports, "PACKET", tmp_path / "packet")
    monkeypatch.setattr(reports, "NUMBERS", numbers)
    monkeypatch.setattr(reports, "SOURCE_NAMES", {n: f"n-{n}.cert" for n in numbers})
    sources: dict[int, bytes] = {}
    for n in numbers:
        text = f"{n} 10\n" + "".join(f"{index + 1}/1 1 0\n" for index in range(n))
        sources[n] = text.encode()
        path = reports.PACKET / "source" / reports.source_path(n)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(sources[n])
    monkeypatch.setattr(
        reports,
        "SOURCE_SHA256",
        {n: hashlib.sha256(raw).hexdigest() for n, raw in sources.items()},
    )
    reports.import_facts()
    facts = reports.read_facts()
    rows = [reports.run_case(facts[n], control) for n in numbers for control in reports.JOBS]
    record = {"format": reports.RECEIPT_FORMAT, "routes": list(reports.ROUTES), "cases": rows}
    reports.save_xz(reports.receipt_path(), record)
    assert reports.check_certification() == {
        n: rows[index * 3] for index, n in enumerate(numbers)
    }
    return record


def test_actual_routes_accept_positive_and_refuse_both_full_roster_controls(
    packet: dict[str, Any],
) -> None:
    for row in packet["cases"]:
        n = row["n"]
        assert len(row["checker_input"]["poses"]) == n
        for route in reports.ROUTES:
            assert row[route]["pairs_tested"] == n * (n - 1) // 2
            assert row[route]["verification_passed"] is (row["control"] == "positive")
    assert reports.check_certification(replay=True)


@pytest.mark.parametrize(
    "mutation",
    [
        "drop-last-pose",
        "change-last-pose",
        "wrong-side",
        "bool-count",
        "drop-control",
        "duplicate-job",
        "extra-job",
        "wrong-control-input",
        "partial-pair-count",
        "bool-pair-count",
        "missing-route",
        "numeric-verdict",
        "missing-native-key",
        "wrong-field",
        "wrong-limitations",
        "wrong-route-id",
        "forged-positive-failure",
        "forged-control-success",
        "non-rational-minimum",
        "negative-time",
        "nan-time",
    ],
)
def test_whole_inputs_and_full_native_results_are_required(
    packet: dict[str, Any], mutation: str
) -> None:
    changed = copy.deepcopy(packet)
    row = changed["cases"][0]
    route = row["exact_verify"]
    if mutation == "drop-last-pose":
        row["checker_input"]["poses"].pop()
    elif mutation == "change-last-pose":
        row["checker_input"]["poses"][-1][0] = "9"
    elif mutation == "wrong-side":
        row["checker_input"]["side"] = "11"
    elif mutation == "bool-count":
        row["n"] = True
    elif mutation == "drop-control":
        changed["cases"].pop()
    elif mutation == "duplicate-job":
        changed["cases"][1] = copy.deepcopy(row)
    elif mutation == "extra-job":
        changed["cases"].append(copy.deepcopy(row))
    elif mutation == "wrong-control-input":
        changed["cases"][1]["checker_input"] = copy.deepcopy(row["checker_input"])
    elif mutation == "partial-pair-count":
        route["pairs_tested"] -= 1
    elif mutation == "bool-pair-count":
        route["pairs_tested"] = True
    elif mutation == "missing-route":
        row.pop("independent")
    elif mutation == "numeric-verdict":
        route["verification_passed"] = 1
    elif mutation == "missing-native-key":
        route.pop("minimum_best_pair_gap")
    elif mutation == "wrong-field":
        route["field_certificate"]["field"] = "float"
    elif mutation == "wrong-limitations":
        route["limitations"] = "Globally optimal."
    elif mutation == "wrong-route-id":
        route["id"] = "W-evand-exact-n003"
    elif mutation == "forged-positive-failure":
        route["failures"] = ["failure"]
    elif mutation == "forged-control-success":
        changed["cases"][1]["independent"]["verification_passed"] = True
    elif mutation == "non-rational-minimum":
        route["minimum_containment_clearance"] = "0.0"
    elif mutation == "negative-time":
        row["wall_seconds"] = -1
    else:
        # The writer also rejects NaN; inject it at the read boundary to test admission.
        row["wall_seconds"] = float("nan")
        reports.receipt_path().write_bytes(lzma.compress(json.dumps(changed).encode()))
        with pytest.raises(reports.ReportError):
            reports.check_certification()
        return
    reports.save_xz(reports.receipt_path(), changed)
    with pytest.raises(reports.ReportError):
        reports.check_certification()


def test_each_call_rereads_receipt_and_source_facts(packet: dict[str, Any]) -> None:
    assert reports.check_certification()
    changed = copy.deepcopy(packet)
    changed["cases"][-1]["checker_input"]["poses"][-1][2] = "1/3"
    reports.save_xz(reports.receipt_path(), changed)
    with pytest.raises(reports.ReportError, match="full native deciding input"):
        reports.check_certification([reports.NUMBERS[0]])
    reports.save_xz(reports.receipt_path(), packet)
    assert reports.check_certification()
    facts = reports.read_xz(reports.fact_path())
    facts["cases"][-1]["source_certificate"] += "\n1 1 0\n"
    reports.save_xz(reports.fact_path(), facts)
    with pytest.raises(reports.ReportError, match="acquired certificate"):
        reports.check_certification([reports.NUMBERS[0]])


@pytest.mark.usefixtures("packet")
@pytest.mark.parametrize("selection", [[], [3, 3], [True], [3, 99]])
def test_scope_must_be_explicit_complete_valid_counts(selection: list[int]) -> None:
    with pytest.raises(reports.ReportError):
        reports.check_certification(selection)


def test_bound_is_exact_rational_ceiling_not_a_source_decimal(packet: dict[str, Any]) -> None:
    assert packet["cases"][0]["checker_input"]["side"] == "10"
    assert reports.confirmed_bound(3) == {
        "value": "10.0000000000000000",
        "exact_form": "10",
        "evidence": [reports.EXACT_EVIDENCE],
    }


def test_tangent_conversion_uses_all_rows_and_rational_orientation() -> None:
    certificate = legacy.parse("2 5\n1 1 1/3\n3 3 -7/5\n")
    witness = reports.to_witness(certificate)
    assert witness["squares"] == legacy.basis_witness(certificate)["squares"]
    assert witness["squares"][-1]["basis"] == ["-12/37", "-35/37"]
    assert "global optimality" in witness["claim"]["limitations"]
    assert reports.job_input(certificate, "positive") == certificate


@pytest.mark.parametrize("corruption", ["duplicate-key", "trailing-stream", "truncated"])
def test_bounded_xz_reader_rejects_ambiguous_or_incomplete_data(
    tmp_path: Path, corruption: str
) -> None:
    data = lzma.compress(b'{"cases": [], "cases": []}')
    if corruption == "trailing-stream":
        data = lzma.compress(b"{}") + lzma.compress(b"{}")
    elif corruption == "truncated":
        data = lzma.compress(b"{}")[:-4]
    path = tmp_path / "input.xz"
    path.write_bytes(data)
    with pytest.raises(reports.ReportError):
        reports.read_xz(path)


def test_bound_applies_before_and_after_decompression(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(reports, "MAX_BYTES", 200)
    path = tmp_path / "input.xz"
    path.write_bytes(b"x" * 201)
    with pytest.raises(reports.ReportError, match="compressed evidence"):
        reports.read_xz(path)
    path.write_bytes(lzma.compress(json.dumps({"poses": "x" * 1000}).encode()))
    with pytest.raises(reports.ReportError, match="oversized"):
        reports.read_xz(path)


def test_retained_producer_refuses_external_linked_leaf(
    packet: dict[str, Any], tmp_path: Path
) -> None:
    outside = tmp_path.parent / f"{tmp_path.name}-outside.xz"
    outside.write_bytes(b"must survive")
    reports.receipt_path().unlink()
    reports.receipt_path().symlink_to(outside)
    with pytest.raises(reports.ReportError, match="inside the repository"):
        reports.save_xz(reports.receipt_path(), packet)
    assert outside.read_bytes() == b"must survive"
    outside.unlink()


def test_native_child_timeout_is_bounded_and_never_becomes_a_success_receipt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def hung(command: list[str], **kwargs: Any) -> subprocess.CompletedProcess[bytes]:
        assert kwargs["timeout"] == 1
        raise subprocess.TimeoutExpired(command, 1, output=b"partial", stderr=b"diagnostic")

    monkeypatch.setattr(reports.subprocess, "run", hung)
    with pytest.raises(reports.ReportError, match="exceeded 1s"):
        reports.run_child((266, "positive"), tmp_path, 1)
    assert (tmp_path / "n266-positive.stdout.log").read_bytes() == b"partial"
    assert (tmp_path / "n266-positive.stderr.log").read_bytes() == b"diagnostic"
    assert (
        json.loads((tmp_path / "n266-positive.failure.json").read_text())["status"] == "timeout"
    )


def test_real_retained_three_packing_roster_is_complete() -> None:
    facts = reports.read_facts()
    assert tuple(facts) == (266, 270, 272)
    assert all(len(certificate.poses) == n for n, certificate in facts.items())


def test_real_retained_native_verdicts_bind_all_three_sources_and_all_controls() -> None:
    positives = reports.check_certification()
    assert tuple(positives) == reports.NUMBERS
    for n, positive in positives.items():
        assert positive["checker_input"] == reports.checker_input(reports.read_fact(n))
        assert all(positive[route]["verification_passed"] for route in reports.ROUTES)


@pytest.mark.parametrize("control", reports.JOBS)
def test_explicit_profile_keeps_native_routes_and_binds_namespace(control: str) -> None:
    certificate = legacy.parse("2 5\n1 1 0\n3 3 0\n")
    profile = {
        "witness_prefix": "W-ryxu-432-n",
        "claim_limitations": "Complete rational input; feasibility only.",
    }
    witness = reports.to_witness(certificate, **profile)
    assert witness["id"] == "W-ryxu-432-n002"
    assert witness["claim"]["limitations"] == profile["claim_limitations"]
    row = reports.run_case(certificate, control, **profile)
    reports.validate_job(row, certificate, control, **profile)
    with pytest.raises(reports.ReportError, match="identity"):
        reports.validate_job(row, certificate, control)
    default = reports.run_case(certificate, control)
    assert default["exact_verify"]["id"] == "W-evand-399-n002"
    alternate = copy.deepcopy(row)
    alternate["exact_verify"]["id"] = default["exact_verify"]["id"]
    timing = {"cpu_seconds", "wall_seconds"}
    assert {key: value for key, value in alternate.items() if key not in timing} == {
        key: value for key, value in default.items() if key not in timing
    }


@pytest.mark.parametrize(
    ("key", "value"),
    [
        ("witness_prefix", ""),
        ("witness_prefix", "W-UPPER-n"),
        ("witness_prefix", "W-ryxu-432-n/"),
        ("witness_prefix", "W-ryxu--432-n"),
        ("witness_prefix", "W-" + "a" * 128 + "-n"),
        ("witness_prefix", 42),
        ("claim_limitations", ""),
        ("claim_limitations", "  "),
        ("claim_limitations", "x" * 4001),
        ("claim_limitations", None),
    ],
)
def test_profile_is_strict_and_bounded(key: str, value: Any) -> None:
    certificate = legacy.parse("2 5\n1 1 0\n3 3 0\n")
    profile = {key: value}
    with pytest.raises(reports.ReportError):
        reports.to_witness(certificate, **profile)
    with pytest.raises(reports.ReportError):
        reports.run_case(certificate, "positive", **profile)
    with pytest.raises(reports.ReportError):
        reports.validate_job({}, certificate, "positive", **profile)
