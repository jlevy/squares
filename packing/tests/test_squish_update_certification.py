"""Revision-bound complete SQUISH replay custody and meaningful private mutations."""

from __future__ import annotations

import gzip
import json
import lzma
import shutil
from pathlib import Path

import pytest

from devtools import squish_followup_packets as packet
from sqpack.witness import witness_document


@pytest.fixture
def private_packet(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    retained = tmp_path / packet.PACKET.relative_to(packet.REPO)
    proofs = tmp_path / packet.WITNESSES.relative_to(packet.REPO)
    shutil.copytree(packet.PACKET, retained)
    shutil.copytree(packet.WITNESSES, proofs)
    prior = tmp_path / packet.original.PACKET.relative_to(packet.REPO)
    shutil.copytree(packet.original.PACKET / "facts", prior / "facts")
    monkeypatch.setattr(packet.original, "REPO", tmp_path)
    monkeypatch.setattr(packet.original, "PACKET", prior)
    monkeypatch.setattr(packet, "REPO", tmp_path)
    monkeypatch.setattr(packet, "PACKET", retained)
    monkeypatch.setattr(packet, "WITNESSES", proofs)
    return retained


def save_receipt(path: Path, value: object) -> None:
    path.write_bytes(lzma.compress(packet.json_bytes(value)))


def link_private_proofs() -> Path:
    """Link only private proof copies outside the private consumer repository."""
    source = packet.REPO.with_name(packet.REPO.name + "-linked-proofs")
    shutil.move(packet.WITNESSES, source)
    packet.WITNESSES.symlink_to(source, target_is_directory=True)
    return source


@pytest.mark.usefixtures("private_packet")
def test_linked_proof_read_admission_is_exact_and_keeps_other_escapes_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from devtools import check_results  # noqa: PLC0415

    source = link_private_proofs()
    monkeypatch.setattr(check_results, "REPO", packet.REPO)
    before = {path.name: path.read_bytes() for path in source.iterdir()}
    relatives = [
        packet.certificate_path(n).relative_to(packet.REPO).as_posix()
        for n in packet.RESULT_NUMBERS
    ]
    assert check_results.repository_file_problems(relatives) == dict.fromkeys(relatives)
    assert check_results.repository_file_problem(relatives[0]) is None
    for relative in relatives:
        assert packet.linked_certificate_problem(relative, repository=source) == (
            "resolves outside the repository"
        )
    unrelated = packet.REPO / "unrelated.yaml.gz"
    unrelated.symlink_to(source / "n-123-rational.yaml.gz")
    assert check_results.repository_file_problem("unrelated.yaml.gz") == (
        "resolves outside the repository"
    )
    assert (
        check_results.repository_file_problem(
            "packing/witnesses/squish-401-update-2026/n-153-rational.yaml.gz"
        )
        == "resolves outside the repository"
    )
    assert check_results.repository_file_problem("../unrelated.yaml.gz") == (
        "must be a normalized repository-relative path"
    )
    assert {path.name: path.read_bytes() for path in source.iterdir()} == before


@pytest.mark.parametrize("mutation", ["receipt", "proof"])
def test_linked_proof_read_admission_refuses_complete_custody_corruption(
    private_packet: Path, monkeypatch: pytest.MonkeyPatch, mutation: str
) -> None:
    from devtools import check_results  # noqa: PLC0415

    source = link_private_proofs()
    monkeypatch.setattr(check_results, "REPO", packet.REPO)
    path = (
        private_packet / "receipts/certification.json.xz"
        if mutation == "receipt"
        else source / "n-123-rational.yaml.gz"
    )
    original = path.read_bytes()
    if mutation == "receipt":
        receipt = packet.read_xz_receipt(path)
        receipt["cases"][0]["checker_input"]["squares"][0]["corners"][0][0] = "99"
        save_receipt(path, receipt)
    else:
        (source / "n-123-rational.yaml.gz").unlink()
    relative = packet.certificate_path(123).relative_to(packet.REPO).as_posix()
    problem = check_results.repository_file_problem(relative)
    assert problem is not None
    assert problem.startswith("linked reviewed proof custody mismatch:")
    sibling = packet.certificate_path(126).relative_to(packet.REPO).as_posix()
    problems = check_results.repository_file_problems([relative, sibling])
    assert problems[relative] is not None
    if mutation == "receipt":
        assert problems[sibling] is not None
    else:
        assert problems[sibling] is None
    path.write_bytes(original)
    assert check_results.repository_file_problems([relative, sibling]) == {
        relative: None,
        sibling: None,
    }


@pytest.mark.usefixtures("private_packet")
def test_individual_external_proof_symlinks_do_not_gain_read_admission(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from devtools import check_results  # noqa: PLC0415

    monkeypatch.setattr(check_results, "REPO", packet.REPO)
    path = packet.certificate_path(123)
    source = packet.REPO.with_name(packet.REPO.name + "-external-proof.yaml.gz")
    source.write_bytes(path.read_bytes())
    path.unlink()
    path.symlink_to(source)
    assert not packet.WITNESSES.is_symlink()
    assert check_results.repository_file_problem(path.relative_to(packet.REPO).as_posix()) == (
        "resolves outside the repository"
    )


@pytest.mark.usefixtures("private_packet")
def test_linked_directory_does_not_admit_a_valid_external_leaf_symlink(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from devtools import check_results  # noqa: PLC0415

    source = link_private_proofs()
    monkeypatch.setattr(check_results, "REPO", packet.REPO)
    leaf = source / "n-123-rational.yaml.gz"
    external = source.with_name(source.name + "-leaf.yaml.gz")
    external.write_bytes(leaf.read_bytes())
    leaf.unlink()
    leaf.symlink_to(external)
    assert packet.certificate_path(123).is_symlink()
    # The geometry itself remains valid; the additional link is still inadmissible.
    packet.check_certification([123])
    assert (
        check_results.repository_file_problem(
            packet.certificate_path(123).relative_to(packet.REPO).as_posix()
        )
        == "resolves outside the repository"
    )


def test_all_complete_proofs_and_reused_timing_are_bound(private_packet: Path) -> None:
    rows = packet.check_certification()
    assert tuple(rows) == packet.RESULT_NUMBERS
    assert 153 not in rows
    assert sum(rows) == 2309
    assert sum(row["independent"]["pairs_tested"] for row in rows.values()) == 237025
    summary = packet.read_review_json(private_packet / "receipts/replay-summary.json")
    assert summary["original_batch"]["counts"] == list(packet.NUMBERS)
    assert summary["original_batch"]["positive_wall_seconds"] == pytest.approx(108.597829942)
    assert summary["scoped_positive_wall_seconds"] == pytest.approx(104.001347867)
    assert packet.confirmed_bound(126)["evidence"] == [packet.EXACT_EVIDENCE]


@pytest.mark.parametrize(
    "mutation",
    ["side", "corner", "source", "roster", "pair-type", "verdict", "ceiling", "control"],
)
def test_private_semantic_mutations_refuse_reused_success(
    private_packet: Path, mutation: str
) -> None:
    path = private_packet / "receipts/certification.json.xz"
    receipt = packet.read_xz_receipt(path)
    row = receipt["cases"][0]
    if mutation == "side":
        row["checker_input"]["side"] = "12"
    elif mutation == "corner":
        row["checker_input"]["squares"][0]["corners"][0][0] = "99"
    elif mutation == "source":
        receipt["source_commit"] = "a different revision"
    elif mutation == "roster":
        receipt["cases"].append(row)
    elif mutation == "pair-type":
        row["independent"]["pairs_tested"] = float(row["independent"]["pairs_tested"])
    elif mutation == "verdict":
        row["exact_verify"]["verification_passed"] = 1
    elif mutation == "ceiling":
        row["verified_value"] = "11.6009077785163405"
    else:
        path = private_packet / "receipts/negative-controls.json.xz"
        receipt = packet.read_xz_receipt(path)
        receipt["controls"][0]["checker_input"]["squares"][1]["corners"][0][0] = "99"
    save_receipt(path, receipt)
    with pytest.raises(
        ValueError, match=r"semantic mismatch|provenance mismatch|replay count|coverage"
    ):
        packet.check_certification([123])


@pytest.mark.usefixtures("private_packet")
@pytest.mark.parametrize("field", ["id", "source", "certificate"])
def test_non_geometric_witness_revision_metadata_is_checked(field: str) -> None:
    witness = packet.read_certificate(123)
    if field == "id":
        witness[field] = "W-squish-401-n123"
    elif field == "source":
        witness[field] = {
            "path": "packing/resources/web/squish-401-2026-10-07/facts/n-123.json.gz"
        }
    else:
        witness[field]["replay"] = "python -m devtools.squish_upper_bound_packets check"
    packet.certificate_path(123).write_bytes(
        gzip.compress(witness_document(witness).encode(), mtime=0)
    )
    with pytest.raises(ValueError, match="revision-specific witness metadata/input mismatch"):
        packet.check_certification([123])


@pytest.mark.parametrize(
    "kind", ["truncated", "trailing", "concatenated", "duplicate", "memory"]
)
def test_xz_reader_refuses_ambiguous_or_unbounded_payloads(tmp_path: Path, kind: str) -> None:
    encoded = lzma.compress(b'{"n": 123}')
    if kind == "truncated":
        encoded = encoded[:-1]
    elif kind == "trailing":
        encoded += b"unadmitted bytes"
    elif kind == "concatenated":
        encoded += encoded
    elif kind == "duplicate":
        encoded = lzma.compress(b'{"n": 123, "n": 126}')
    else:
        encoded = lzma.compress(b"{}", preset=9)
    path = tmp_path / "receipt.xz"
    path.write_bytes(encoded)
    with pytest.raises(ValueError, match=r"XZ receipt|duplicate JSON"):
        packet.read_xz_receipt(path)


def test_xz_compressed_and_decoded_caps(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "receipt.xz"
    monkeypatch.setattr(packet, "MAX_RECEIPT_BYTES", 128)
    path.write_bytes(b"x" * 129)
    with pytest.raises(ValueError, match="compressed receipt exceeds"):
        packet.read_xz_receipt(path)
    path.write_bytes(lzma.compress(json.dumps("x" * 129).encode()))
    with pytest.raises(ValueError, match="uncompressed receipt exceeds"):
        packet.read_xz_receipt(path)


def test_linked_producer_output_refuses_before_any_write(
    private_packet: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    original_proof = packet.certificate_path(123).read_bytes()
    linked = tmp_path / "outside" / "proofs"
    linked.parent.mkdir()
    linked.symlink_to(packet.WITNESSES)
    monkeypatch.setattr(packet, "WITNESSES", linked)
    monkeypatch.setattr(packet, "REPO", private_packet)
    with pytest.raises(ValueError, match="escapes the private checkout"):
        packet.save_certificate(packet.certificate_path(123), b"invalid")
    assert packet.certificate_path(123).read_bytes() == original_proof


def test_offline_recovery_is_identical_and_linked_preflight_is_atomic(
    private_packet: Path, tmp_path: Path
) -> None:
    expected = {n: packet.certificate_path(n).read_bytes() for n in packet.RESULT_NUMBERS}
    for n in packet.RESULT_NUMBERS:
        packet.certificate_path(n).unlink()
    packet.restore_witnesses()
    assert {n: packet.certificate_path(n).read_bytes() for n in expected} == expected
    packet.check_certification()
    outside = tmp_path.parent / f"{tmp_path.name}-outside-proof.yaml.gz"
    outside.write_bytes(b"external source proof")
    first = packet.certificate_path(123)
    first.write_bytes(b"private sentinel before preflight")
    target = packet.certificate_path(126)
    target.unlink()
    target.symlink_to(outside)
    with pytest.raises(ValueError, match="escapes the private checkout"):
        packet.restore_witnesses()
    assert first.read_bytes() == b"private sentinel before preflight"
    assert outside.read_bytes() == b"external source proof"
    assert private_packet.is_dir()
