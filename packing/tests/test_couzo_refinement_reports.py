"""Complete-source and bounded replay protocol controls for issue #451."""

from __future__ import annotations

import json
import subprocess
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import couzo_refinement_reports as reports
from devtools import evand_arrangement_reports as kernel
from devtools.retained_data import read_retained_bytes


def test_all_eight_sources_keep_complete_exact_poses_and_decimal_context() -> None:
    pins = reports.source_pins()
    certificates = reports.read_facts()
    assert list(certificates) == list(pins)
    assert sum(len(certificate.poses) for certificate in certificates.values()) == 1340
    for n, certificate in certificates.items():
        raw = read_retained_bytes(
            reports.PACKET / "source" / pins[n]["certificate"]["path"],
            limit=reports.MAX_SOURCE_BYTES,
        )
        assert certificate == reports.legacy.parse(raw.decode(), expected_n=n)
        for control in reports.JOBS:
            deciding = kernel.checker_input(kernel.job_input(certificate, control))
            assert deciding["n"] == n
            assert len(deciding["poses"]) == n
    assert certificates[306].side == Fraction(
        8981716858745712869796920037761, 500000000000000000000000000000
    )


@pytest.mark.parametrize("field", ["source_certificate", "decimal_pose"])
def test_late_complete_original_mutations_refuse(
    monkeypatch: pytest.MonkeyPatch, field: str
) -> None:
    original = kernel.read_xz(reports.fact_path())
    changed = deepcopy(original)
    changed["cases"][-1][field] += "\n# changed original bytes\n"
    monkeypatch.setattr(kernel, "read_xz", lambda _path: changed)
    with pytest.raises(kernel.ReportError, match="complete original bytes"):
        reports.read_facts()
    monkeypatch.setattr(kernel, "read_xz", lambda _path: original)
    assert len(reports.read_facts()[306].poses) == 306


def test_acquisition_mutation_cannot_relabel_source(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    original = reports.PACKET / "acquisition/case-inputs.json"
    value = json.loads(original.read_text())
    value["cases"][-1]["certificate"]["sha256"] = value["cases"][0]["certificate"]["sha256"]
    packet = tmp_path / "packet"
    (packet / "acquisition").mkdir(parents=True)
    (packet / "acquisition/case-inputs.json").write_text(json.dumps(value))
    monkeypatch.setattr(reports, "REPO", tmp_path)
    monkeypatch.setattr(reports, "PACKET", packet)
    with pytest.raises(kernel.ReportError, match="acquisition roster"):
        reports.source_pins()


def test_fact_scope_refuses_missing_reordered_and_extra_originals(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original = kernel.read_xz(reports.fact_path())
    for mutation in ("missing", "reordered", "extra", "boolean-count"):
        changed = deepcopy(original)
        if mutation == "missing":
            changed["cases"].pop()
        elif mutation == "reordered":
            changed["cases"][0], changed["cases"][-1] = (
                changed["cases"][-1],
                changed["cases"][0],
            )
        elif mutation == "extra":
            changed["unexpected"] = True
        else:
            changed["cases"][-1]["n"] = True
        monkeypatch.setattr(kernel, "read_xz", lambda _path, record=changed: record)
        with pytest.raises(kernel.ReportError):
            reports.read_facts()


def test_full_envelope_transfers_all_twenty_four_complete_validator_inputs(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    facts = reports.read_facts()
    seen: list[tuple[int, str]] = []
    rows = [
        {
            "n": n,
            "control": control,
            "checker_input": kernel.checker_input(kernel.job_input(facts[n], control)),
        }
        for n in reports.NUMBERS
        for control in reports.JOBS
    ]

    def admit(
        row: dict[str, Any],
        certificate: reports.legacy.Certificate,
        control: str,
        *,
        witness_prefix: str,
        claim_limitations: str,
    ) -> None:
        expected = kernel.checker_input(kernel.job_input(certificate, control))
        if (
            row["n"] != certificate.n
            or row["control"] != control
            or row["checker_input"] != expected
            or witness_prefix != "W-couzo-451-n"
            or "Finite construction feasibility only" not in claim_limitations
        ):
            raise kernel.ReportError("wrong complete deciding input or finite profile")
        seen.append((certificate.n, control))

    monkeypatch.setattr(kernel, "validate_job", admit)
    envelope = {
        "format": reports.RECEIPT_FORMAT,
        "routes": list(reports.ROUTES),
        "cases": rows,
    }
    positives = reports.validate_certification(envelope, facts)
    assert seen == [(n, control) for n in reports.NUMBERS for control in reports.JOBS]
    assert list(positives) == list(reports.NUMBERS)
    for mutation in (
        "missing",
        "repeated",
        "reordered",
        "swapped-routes",
        "extra",
        "wrong-format",
    ):
        changed = deepcopy(envelope)
        if mutation == "missing":
            changed["cases"].pop()
        elif mutation == "repeated":
            changed["cases"][-1] = changed["cases"][0]
        elif mutation == "reordered":
            changed["cases"][0], changed["cases"][-1] = (
                changed["cases"][-1],
                changed["cases"][0],
            )
        elif mutation == "swapped-routes":
            changed["routes"].reverse()
        elif mutation == "extra":
            changed["extra"] = True
        else:
            changed["format"] = reports.FACT_FORMAT
        with pytest.raises(kernel.ReportError):
            reports.validate_certification(changed, facts)


def test_decimal_context_refuses_missing_row_count_and_nonfinite() -> None:
    pin = reports.source_pins()[306]["decimal_pose"]
    text = read_retained_bytes(
        reports.PACKET / "source" / pin["path"], limit=reports.MAX_SOURCE_BYTES
    ).decode()
    reports.admit_decimal_pose(text, 306)
    for changed in (
        "\n".join(text.splitlines()[:-1]) + "\n",
        text.replace("# n = 306", "# n = 305"),
        text.replace(
            text.splitlines()[-1], "NaN " + " ".join(text.splitlines()[-1].split()[1:])
        ),
    ):
        with pytest.raises(kernel.ReportError):
            reports.admit_decimal_pose(changed, 306)


def test_native_driver_retains_stdout_stderr_and_exact_deadline(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    output = tmp_path / "n306-positive.json"
    actual = {"n": 306, "control": "positive", "complete": "unchanged native object"}

    def run(command: list[str], **options: Any) -> subprocess.CompletedProcess[bytes]:
        assert command[2] == "devtools.couzo_refinement_reports"
        assert command[command.index("--n") + 1] == "306"
        assert command[command.index("--control") + 1] == "positive"
        assert command[-1] == str(output)
        assert options["timeout"] == 45
        assert options["capture_output"] is True
        output.write_text(json.dumps(actual))
        return subprocess.CompletedProcess(command, 0, b"native stdout", b"native stderr")

    monkeypatch.setattr(subprocess, "run", run)
    assert reports.run_child((306, "positive"), tmp_path, 45) == actual
    assert output.with_suffix(".stdout.log").read_bytes() == b"native stdout"
    assert output.with_suffix(".stderr.log").read_bytes() == b"native stderr"
    with pytest.raises(kernel.ReportError, match="overwrite"):
        reports.run_child((306, "positive"), tmp_path, 45)


def test_timeout_preserves_partial_native_output(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def timeout(command: list[str], **_options: Any) -> subprocess.CompletedProcess[bytes]:
        raise subprocess.TimeoutExpired(
            command, 45, output=b"partial stdout", stderr=b"partial stderr"
        )

    monkeypatch.setattr(subprocess, "run", timeout)
    with pytest.raises(kernel.ReportError, match="exceeded 45s"):
        reports.run_child((306, "positive"), tmp_path, 45)
    assert (tmp_path / "n306-positive.stdout.log").read_bytes() == b"partial stdout"
    assert (tmp_path / "n306-positive.stderr.log").read_bytes() == b"partial stderr"


def test_scientific_producer_refuses_external_custody_and_invalid_batch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(reports, "REPO", tmp_path / "private")
    with pytest.raises(kernel.ReportError, match="remain private"):
        reports.ensure_private(tmp_path / "outside.json")
    for workers, timeout in ((3, 45), (True, 45), (2, 46), (2, 0), (2, True)):
        with pytest.raises(kernel.ReportError, match="worker/deadline"):
            reports.certify(tmp_path / "jobs", workers=workers, timeout=timeout)


@pytest.mark.parametrize("payload", [b'{"n":306,"n":105}', b"[]"])
def test_driver_refuses_duplicate_keys_and_nonobject_results(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, payload: bytes
) -> None:
    def run(command: list[str], **_options: Any) -> subprocess.CompletedProcess[bytes]:
        Path(command[-1]).write_bytes(payload)
        return subprocess.CompletedProcess(command, 0, b"", b"")

    monkeypatch.setattr(subprocess, "run", run)
    with pytest.raises(kernel.ReportError):
        reports.run_child((306, "positive"), tmp_path, 45)


def test_import_refuses_compressed_original_link_outside_private_tree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    pin = reports.source_pins()[105]["certificate"]
    packet = tmp_path / "private/packet"
    (packet / "acquisition").mkdir(parents=True)
    (packet / "acquisition/case-inputs.json").write_bytes(
        (reports.PACKET / "acquisition/case-inputs.json").read_bytes()
    )
    target = packet / pin["stored"]
    target.parent.mkdir(parents=True)
    outside = tmp_path / "external.cert.gz"
    outside.write_bytes((reports.PACKET / pin["stored"]).read_bytes())
    target.symlink_to(outside)
    monkeypatch.setattr(reports, "REPO", tmp_path / "private")
    monkeypatch.setattr(reports, "PACKET", packet)
    with pytest.raises(kernel.ReportError, match="remain private"):
        reports.import_facts()
    assert not reports.fact_path().exists()
