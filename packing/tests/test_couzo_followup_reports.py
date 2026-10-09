"""Derived custody, exact replay and negative controls for Couzo's 2d32a6e follow-up."""

from __future__ import annotations

import json
import shutil
import subprocess
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import couzo_followup_reports as reports
from devtools import couzo_refinement_reports as earlier
from devtools import evand_arrangement_reports as kernel
from sqpack.yamlio import load_yaml


@pytest.fixture
def private_packet(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A private copy of the packet that a mutation cannot reach back from."""
    repo = tmp_path / "private"
    packet = repo / reports.PACKET.relative_to(reports.REPO)
    shutil.copytree(reports.PACKET, packet)
    monkeypatch.setattr(reports, "REPO", repo)
    monkeypatch.setattr(reports, "PACKET", packet)
    monkeypatch.setattr(kernel, "REPO", repo)
    return packet


def _record(packet: Path) -> dict[str, Any]:
    return json.loads((packet / "acquisition/sources.json").read_text())


def _write_record(packet: Path, value: dict[str, Any]) -> None:
    (packet / "acquisition/sources.json").write_text(json.dumps(value, indent=2) + "\n")


def test_derived_packet_rebuilds_every_pinned_certificate_without_raw_bytes() -> None:
    certificates = reports.read_facts()
    assert tuple(certificates) == reports.NUMBERS
    assert sum(len(c.poses) for c in certificates.values()) == 720
    source = reports.read_record(reports.sources_path())
    assert source["raw_asset_retained"] is False
    assert source["licence"] is None
    leaves = source["custody"]["tree"]
    assert len(leaves) == 136
    assert sum(leaves[reports.certificate_path(n)]["size"] for n in reports.NUMBERS) == 119049
    for n, certificate in certificates.items():
        text = reports.render(certificate)
        assert text.startswith(reports.LAYOUT_HEADER)
        assert len(text.encode()) == leaves[reports.certificate_path(n)]["size"]
    retained = {p.name for p in reports.PACKET.rglob("*") if p.is_file()}
    assert not retained & {"n84.cert", "n84.txt", "n84.svg", "README.md.orig"}
    assert not any(name.endswith((".cert", ".txt", ".svg", ".gz")) for name in retained)
    assert certificates[270].side == Fraction(
        169367230228761834072968722597, 10000000000000000000000000000
    )


def test_every_new_side_is_strictly_below_its_frozen_comparisons() -> None:
    certificates = reports.read_facts()
    cases = {row["n"]: row for row in reports.read_record(reports.sources_path())["cases"]}
    for n, certificate in certificates.items():
        prior = cases[n]["prior"]
        assert certificate.side < Fraction(prior["selected_exact"])
        assert certificate.side < Fraction(prior["verified_exact"])
    assert cases[270]["prior"]["selected_source_key"] == "[Daniel new arrangements 2026-10-07]"
    assert cases[105]["prior"]["earlier_couzo_451_exact"] == reports.legacy.literal(
        earlier.read_facts()[105].side
    )
    assert certificates[105].side < earlier.read_facts()[105].side


def test_seven_unchanged_certificates_match_the_issue451_originals() -> None:
    source = reports.read_record(reports.sources_path())
    leaves = source["custody"]["tree"]
    pins = earlier.source_pins()
    assert [row["n"] for row in source["unchanged"]] == list(reports.UNCHANGED)
    for n in reports.UNCHANGED:
        assert leaves[f"certificates/n{n}.cert"]["sha"] == pins[n]["certificate"]["git_blob"]
        assert leaves[f"n{n}.txt"]["sha"] == pins[n]["decimal_pose"]["git_blob"]
    assert leaves["certificates/n105.cert"]["sha"] != pins[105]["certificate"]["git_blob"]


@pytest.mark.parametrize(
    "mutation",
    [
        "centre",
        "noncanonical",
        "basis",
        "missing-square",
        "side",
        "limitations",
    ],
)
def test_late_fact_mutations_refuse(private_packet: Path, mutation: str) -> None:
    assert tuple(reports.read_facts()) == reports.NUMBERS
    path = private_packet / "facts/n-270.yaml"
    original = path.read_text()
    document = load_yaml(original)
    witness = document["witness"]
    if mutation == "centre":
        x = Fraction(witness["squares"][-1]["center"][0])
        witness["squares"][-1]["center"][0] = reports.legacy.literal(x + Fraction(1, 10**30))
    elif mutation == "noncanonical":
        witness["squares"][0]["center"][0] = "2/4"
    elif mutation == "basis":
        witness["squares"][0]["basis"] = ["3/5", "3/5"]
    elif mutation == "missing-square":
        witness["squares"].pop()
    elif mutation == "side":
        witness["side"] = reports.legacy.literal(
            Fraction(witness["side"]) - Fraction(1, 10**12)
        )
    else:
        witness["claim"]["limitations"] = "Global optimality is proved."
    path.write_text(reports.witness_document(witness, schema=reports.SCHEMA))
    with pytest.raises(reports.ReportError):
        reports.read_facts()
    path.write_text(original)
    assert tuple(reports.read_facts()) == reports.NUMBERS


@pytest.mark.parametrize(
    "mutation",
    ["raw-retained", "tree-leaf", "unchanged", "prior", "scope", "licence", "outside"],
)
def test_acquisition_record_mutations_refuse(private_packet: Path, mutation: str) -> None:
    original = _record(private_packet)
    value = deepcopy(original)
    source = value["sources"][0]
    if mutation == "raw-retained":
        source["raw_asset_retained"] = True
    elif mutation == "tree-leaf":
        leaf = source["custody"]["tree"]["n84.svg"]
        leaf["sha"] = source["custody"]["tree"]["n86.svg"]["sha"]
        leaf["url"] = leaf["url"].rsplit("/", 1)[0] + "/" + leaf["sha"]
    elif mutation == "unchanged":
        source["unchanged"][0]["certificate_blob"] = "0" * 40
    elif mutation == "prior":
        source["cases"][0]["prior"]["selected_exact"] = source["cases"][0]["side"]
    elif mutation == "scope":
        source["subtree_scope"].append("n84.txt")
    elif mutation == "licence":
        source["licence"] = "MIT"
    else:
        source["outside_horizon"][0]["blob"] = source["outside_horizon"][1]["blob"]
    _write_record(private_packet, value)
    with pytest.raises(reports.ReportError):
        reports.read_facts()
    _write_record(private_packet, original)
    assert tuple(reports.read_facts()) == reports.NUMBERS


@pytest.mark.parametrize("name", ["certificates/n84.cert", "n84.txt", "facts/n-084.yaml.bak"])
def test_extra_or_raw_packet_file_refuses(private_packet: Path, name: str) -> None:
    extra = private_packet / name
    extra.parent.mkdir(parents=True, exist_ok=True)
    extra.write_text("84 1\n")
    with pytest.raises(reports.ReportError, match="unexpected or missing"):
        reports.read_facts()
    extra.unlink()
    assert tuple(reports.read_facts()) == reports.NUMBERS


def test_linked_fact_refuses(private_packet: Path, tmp_path: Path) -> None:
    path = private_packet / "facts/n-084.yaml"
    outside = tmp_path / "outside.yaml"
    outside.write_bytes(path.read_bytes())
    path.unlink()
    path.symlink_to(outside)
    with pytest.raises(reports.ReportError):
        reports.read_facts()


def test_receipt_admits_all_fifteen_jobs_with_both_routes() -> None:
    positives = reports.check_certification()
    assert tuple(positives) == reports.NUMBERS
    record = kernel.read_xz(reports.receipt_path())
    assert [(row["n"], row["control"]) for row in record["cases"]] == [
        (n, control) for n in reports.NUMBERS for control in reports.JOBS
    ]
    for row in record["cases"]:
        passed = row["control"] == "positive"
        for route in reports.ROUTES:
            assert row[route]["verification_passed"] is passed
            assert row[route]["pairs_tested"] == row["n"] * (row["n"] - 1) // 2
    assert sum(row["exact_verify"]["pairs_tested"] for row in record["cases"]) == 192423


@pytest.mark.parametrize("kind", ["verdict", "limitations", "input", "order", "format"])
def test_receipt_mutations_refuse_then_restore(private_packet: Path, kind: str) -> None:
    target = private_packet / "receipts/exact-certification.json.xz"
    original = target.read_bytes()
    value = deepcopy(kernel.read_xz(target))
    row = value["cases"][-1]
    if kind == "verdict":
        assert row["exact_verify"]["verification_passed"] is False
        row["exact_verify"]["verification_passed"] = True
    elif kind == "limitations":
        row["independent"]["limitations"] = "Global optimality is proved."
    elif kind == "input":
        x = row["checker_input"]["poses"][-1][0]
        row["checker_input"]["poses"][-1][0] = str(Fraction(x) + 1)
    elif kind == "order":
        value["cases"][0], value["cases"][-1] = value["cases"][-1], value["cases"][0]
    else:
        value["format"] = earlier.RECEIPT_FORMAT
    kernel.save_xz(target, value)
    with pytest.raises(kernel.ReportError):
        reports.check_certification()
    target.write_bytes(original)
    assert tuple(reports.check_certification()) == reports.NUMBERS


def test_replay_selection_refuses_unknown_and_repeated_counts() -> None:
    for selection in ([], [84, 84], [108]):
        with pytest.raises(reports.ReportError, match="replay selection"):
            reports.check_certification(selection)


def test_native_driver_retains_stdout_stderr_and_deadline(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    output = tmp_path / "n84-positive.json"
    actual = {"n": 84, "control": "positive", "complete": "unchanged native object"}

    def run(command: list[str], **options: Any) -> subprocess.CompletedProcess[bytes]:
        assert command[2] == "devtools.couzo_followup_reports"
        assert command[command.index("--n") + 1] == "84"
        assert command[command.index("--control") + 1] == "positive"
        assert command[-1] == str(output)
        assert options["timeout"] == 45
        assert options["capture_output"] is True
        output.write_text(json.dumps(actual))
        return subprocess.CompletedProcess(command, 0, b"native stdout", b"native stderr")

    monkeypatch.setattr(subprocess, "run", run)
    assert reports.run_child((84, "positive"), tmp_path, 45) == actual
    assert output.with_suffix(".stdout.log").read_bytes() == b"native stdout"
    assert output.with_suffix(".stderr.log").read_bytes() == b"native stderr"
    with pytest.raises(reports.ReportError, match="overwrite"):
        reports.run_child((84, "positive"), tmp_path, 45)


def test_timeout_preserves_partial_native_output(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def timeout(command: list[str], **_options: Any) -> subprocess.CompletedProcess[bytes]:
        raise subprocess.TimeoutExpired(
            command, 45, output=b"partial out", stderr=b"partial err"
        )

    monkeypatch.setattr(subprocess, "run", timeout)
    with pytest.raises(reports.ReportError, match="exceeded 45s"):
        reports.run_child((270, "positive"), tmp_path, 45)
    assert (tmp_path / "n270-positive.stdout.log").read_bytes() == b"partial out"
    assert (tmp_path / "n270-positive.stderr.log").read_bytes() == b"partial err"


@pytest.mark.parametrize("payload", [b'{"n":84,"n":86}', b"[]"])
def test_driver_refuses_duplicate_keys_and_nonobject_results(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, payload: bytes
) -> None:
    def run(command: list[str], **_options: Any) -> subprocess.CompletedProcess[bytes]:
        Path(command[-1]).write_bytes(payload)
        return subprocess.CompletedProcess(command, 0, b"", b"")

    monkeypatch.setattr(subprocess, "run", run)
    with pytest.raises(reports.ReportError, match=r"strict JSON|object required"):
        reports.run_child((84, "positive"), tmp_path, 45)


def test_certify_refuses_invalid_allocation_and_reused_directory(tmp_path: Path) -> None:
    for workers, timeout in ((3, 45), (True, 45), (2, reports.JOB_TIMEOUT + 1), (2, 0)):
        with pytest.raises(reports.ReportError, match="worker/deadline"):
            reports.certify(tmp_path / "jobs", workers=workers, timeout=timeout)
    (tmp_path / "used").mkdir()
    with pytest.raises(reports.ReportError, match="fresh attempt"):
        reports.certify(tmp_path / "used")
    for job in ((108, "positive"), (84, "unknown")):
        with pytest.raises(reports.ReportError, match="roster"):
            reports.run_child(job, tmp_path, 45)


def _fake_git(objects: dict[tuple[str, ...], bytes]):
    def git(_git_dir: Path, *arguments: str) -> bytes:
        return objects[arguments]

    return git


def test_acquisition_refuses_a_substituted_commit_or_blob(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    commit = (
        f"tree {reports.TREE}\nparent {reports.PARENT}\n"
        "author A <a@example.com> 1791497547 +0000\n"
        "committer A <a@example.com> 1791497547 +0000\n\nmessage\n"
    ).encode()
    monkeypatch.setattr(
        reports, "git", _fake_git({("cat-file", "commit", reports.REVISION): commit})
    )
    with pytest.raises(reports.ReportError, match="pinned identity"):
        reports.read_commit(Path("unused"))
    leaf = reports.read_record(reports.sources_path())["custody"]["tree"][
        "certificates/n84.cert"
    ]
    monkeypatch.setattr(
        reports,
        "git",
        _fake_git({("cat-file", "blob", leaf["sha"]): b"84 1\n" + b" " * (leaf["size"] - 5)}),
    )
    with pytest.raises(reports.ReportError, match="differ from the pinned tree"):
        reports.read_blob(Path("unused"), leaf)


def test_acquisition_refuses_an_existing_packet(tmp_path: Path) -> None:
    with pytest.raises(reports.ReportError, match="fresh derived packet"):
        reports.acquire(tmp_path / "unused.git")


def test_certificate_layout_refuses_any_byte_it_cannot_rebuild() -> None:
    certificate = reports.read_facts()[84]
    text = reports.render(certificate)
    assert reports.admit_certificate(text, 84) == certificate
    for changed in (
        text.replace("\n", "\r\n", 1),
        text + "# trailing comment\n",
        text.replace(" ", "  ", 1),
        text.replace(reports.LAYOUT_HEADER, ""),
    ):
        with pytest.raises(reports.ReportError):
            reports.admit_certificate(changed, 84)
    with pytest.raises(reports.ReportError):
        reports.admit_certificate(text, 86)
