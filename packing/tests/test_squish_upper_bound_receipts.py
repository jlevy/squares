"""Integrity controls for the confirmed SQUISH receipts and derived certificates."""

from __future__ import annotations

import gzip
import json
import shutil
from pathlib import Path

import pytest

from devtools import squish_upper_bound_packets as packet
from sqpack.yamlio import safe_load


@pytest.mark.parametrize("record", ["certification", "acquisition", "controls"])
def test_duplicate_receipt_rosters_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, record: str
) -> None:
    local = tmp_path / "packet"
    original_packet = packet.PACKET
    shutil.copytree(packet.PACKET, local)
    path = (
        local
        / (
            {
                "certification": "receipts/certification.json",
                "acquisition": "acquisition/sources.json",
                "controls": "receipts/negative-controls.json",
            }[record]
        )
    )
    value = json.loads(path.read_text())
    if record == "controls":
        value["controls"][1] = value["controls"][0]
    else:
        value["cases"].append(value["cases"][0])
    path.write_text(json.dumps(value))
    monkeypatch.setattr(packet, "PACKET", local)
    monkeypatch.setattr(
        packet, "fact_path", lambda n: original_packet / "facts" / f"n-{n:03d}.json.gz"
    )
    # Roster refusal precedes certificate rebuilding, whose source.path uses PACKET.
    with pytest.raises(ValueError, match=r"roster|negative.control"):
        packet.check([], replay=False)


def test_committed_packet_rebuilds_deterministically() -> None:
    # Offline gate: all facts and certificates, no expensive exact pairwise replay.
    packet.check(list(packet.NUMBERS), replay=False)


def test_changed_retained_certificate_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    n = packet.NUMBERS[0]
    witness = safe_load(gzip.decompress(packet.certificate_path(n).read_bytes()).decode())[
        "witness"
    ]
    witness["squares"][0]["corners"][0][0] = "-1"
    text = packet.witness_document(witness, schema="../witness.schema.yaml").encode()
    original = packet.certificate_path
    altered = tmp_path / "altered.yaml.gz"
    altered.write_bytes(gzip.compress(text, mtime=0))
    monkeypatch.setattr(
        packet, "certificate_path", lambda count: altered if count == n else original(count)
    )
    with pytest.raises(ValueError, match="mismatch"):
        packet.check([n], replay=False)


def test_changed_facts_and_rebuilt_certificate_cannot_reuse_old_success(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    n = packet.NUMBERS[0]
    fact = packet.read_fact(n)
    fact["squares"][1] = dict(fact["squares"][0])
    text = packet.witness_document(packet.to_witness(fact), schema="../witness.schema.yaml")
    altered = tmp_path / "altered.yaml.gz"
    altered.write_bytes(gzip.compress(text.encode(), mtime=0))
    original_read = packet.read_fact
    original_certificate = packet.certificate_path
    monkeypatch.setattr(
        packet, "read_fact", lambda count: fact if count == n else original_read(count)
    )
    monkeypatch.setattr(
        packet,
        "certificate_path",
        lambda count: altered if count == n else original_certificate(count),
    )
    with pytest.raises(ValueError, match="checker-input semantic mismatch"):
        packet.check([n], replay=False)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("source_commit", "0" * 40),
        ("producer_checker_replayed", True),
        ("raw_asset_retained", True),
        ("retrieved", "2026-10-06"),
    ],
)
def test_forged_source_provenance_refused(
    monkeypatch: pytest.MonkeyPatch, field: str, value: object
) -> None:
    acquisition = json.loads((packet.PACKET / "acquisition/sources.json").read_text())
    acquisition[field] = value
    original_load = packet.read_json
    monkeypatch.setattr(
        packet,
        "read_json",
        lambda path: acquisition if path.name == "sources.json" else original_load(path),
    )
    with pytest.raises(ValueError, match="source provenance mismatch"):
        packet.check([], replay=False)


@pytest.mark.parametrize("checker", ["independent", "exact_verify"])
@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("failures", [["overlap", "squares overlap"]]),
        ("minimum_containment_clearance", "-1"),
    ],
)
def test_inconsistent_success_receipt_refused(
    monkeypatch: pytest.MonkeyPatch, checker: str, field: str, value: object
) -> None:
    receipt = packet.read_json(packet.PACKET / "receipts/certification.json")
    receipt["cases"][0][checker][field] = value
    original_load = packet.read_json
    monkeypatch.setattr(
        packet,
        "read_json",
        lambda path: receipt if path.name == "certification.json" else original_load(path),
    )
    with pytest.raises(ValueError, match="full checker coverage"):
        packet.check([packet.NUMBERS[0]], replay=False)


@pytest.mark.parametrize("checker", ["independent", "exact_verify"])
def test_null_negative_control_verdict_refused(
    monkeypatch: pytest.MonkeyPatch, checker: str
) -> None:
    receipt = packet.read_json(packet.PACKET / "receipts/negative-controls.json")
    receipt["controls"][0][checker]["verification_passed"] = None
    original_load = packet.read_json
    monkeypatch.setattr(
        packet,
        "read_json",
        lambda path: receipt if path.name == "negative-controls.json" else original_load(path),
    )
    with pytest.raises(ValueError, match="negative-control checker coverage"):
        packet.check([], replay=False)
