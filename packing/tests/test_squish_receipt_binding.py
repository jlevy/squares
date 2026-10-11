"""Exact semantic receipt binding with a complete small packet and real deciders."""

from __future__ import annotations

import gzip
import json
from pathlib import Path

import pytest

from devtools import squish_upper_bound_packets as packet
from sqpack.yamlio import safe_load


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value))


@pytest.fixture
def small_packet(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setattr(packet, "REPO", tmp_path)
    monkeypatch.setattr(packet, "PACKET", tmp_path / "packing/resources/web/squish")
    monkeypatch.setattr(packet, "WITNESSES", tmp_path / "packing/witnesses/squish")
    monkeypatch.setattr(packet, "NUMBERS", (2,))
    release = tmp_path / "release"
    _write_json(
        release / "n2/n2.cert.json",
        {
            "n": 2,
            "s_exact": "200001/100000",
            "s_decimal": "2.0000",
            "note": "fixture",
            "squares": [["1/2", "1/2", "0"], ["3/2", "1/2", "0"]],
        },
    )
    packet.acquire(
        release,
        tmp_path / "unused",
        release_url="https://github.com/itsnaka/squish-certs",
        supplement_url=packet.source_url(2),
    )
    row = packet.certify_one(2)
    _write_json(
        packet.PACKET / "receipts/certification.json",
        {
            "format": packet.CERTIFICATION_FORMAT,
            "producer_checker_replayed": False,
            "checkers": [
                "devtools.check_rational_witness_independent",
                "sqpack.witness.exact_verify",
            ],
            "cases": [row],
        },
    )
    _write_json(packet.PACKET / "receipts/negative-controls.json", packet.negative_controls())
    for label, claims in packet.normalized_claims([row]).items():
        _write_json(packet.PACKET / f"acquisition/{label}-normalized-claims.json", claims)
    return packet.PACKET


def test_safe_normalized_claims_and_exact_form_are_replayable(small_packet: Path) -> None:
    packet.check([2], replay=True)
    row = packet.read_json(small_packet / "receipts/certification.json")["cases"][0]
    assert row["verified_value"] == "2.0001"
    assert row["exact_form"] == "200001/100000"
    source = packet.read_json(small_packet / "acquisition/sources.json")["cases"][0]
    assert "facts_sha256" not in source
    assert len(source["source_sha256"]) == 64
    claims = packet.read_json(small_packet / "acquisition/release-normalized-claims.json")
    assert claims["results"] == [
        {
            "n": 2,
            "offered_side": "2.0001",
            "exact_side": "200001/100000",
            "source_display": "2.0000",
        }
    ]


@pytest.mark.usefixtures("small_packet")
def test_rebuilt_infeasible_geometry_cannot_reuse_success() -> None:
    fact = packet.read_fact(2)
    fact["squares"][1] = fact["squares"][0].copy()
    packet.fact_path(2).write_bytes(gzip.compress(json.dumps(fact).encode(), mtime=0))
    text = packet.witness_document(packet.to_witness(fact), schema="../witness.schema.yaml")
    packet.certificate_path(2).write_bytes(gzip.compress(text.encode(), mtime=0))
    with pytest.raises(ValueError, match="checker-input semantic mismatch"):
        packet.check([2], replay=False)


@pytest.mark.usefixtures("small_packet")
def test_metadata_and_equivalent_rational_spelling_reuse_geometry_verdict() -> None:
    path = packet.certificate_path(2)
    witness = safe_load(gzip.decompress(path.read_bytes()).decode())["witness"]
    witness["claim"]["limitations"] = "Updated attribution prose; geometry unchanged."
    witness["source"]["url"] = "https://example.com/attribution"
    witness["certificate"]["replay"] = "a revised replay instruction"
    witness["side"] = "400002/200000"
    witness["squares"][0]["corners"][0][0] = "0/2"
    text = packet.witness_document(witness, schema="../witness.schema.yaml")
    path.write_bytes(gzip.compress((text + "# metadata-only formatting\n").encode(), mtime=0))
    packet.check([2], replay=True)


@pytest.mark.parametrize("mutation", ["unit", "frame", "dispatch", "id", "corner"])
@pytest.mark.usefixtures("small_packet")
def test_changed_certificate_decision_input_is_refused(mutation: str) -> None:
    path = packet.certificate_path(2)
    witness = safe_load(gzip.decompress(path.read_bytes()).decode())["witness"]
    if mutation == "unit":
        witness["square_size"] = "2"
    elif mutation == "frame":
        witness["coordinates"]["origin"] = "container-center"
    elif mutation == "dispatch":
        witness["claim"]["method"] = "interval-certified"
    elif mutation == "id":
        witness["squares"][0]["id"] = 7
    else:
        witness["squares"][0]["corners"][0][0] = "1/1000"
    text = packet.witness_document(witness, schema="../witness.schema.yaml")
    path.write_bytes(gzip.compress(text.encode(), mtime=0))
    with pytest.raises(ValueError, match=r"checker input|mismatch|square_size"):
        packet.check([2], replay=False)


def test_controls_and_normalized_claims_cannot_inherit_stale_data(small_packet: Path) -> None:
    path = small_packet / "receipts/negative-controls.json"
    controls = packet.read_json(path)
    controls["controls"][0]["checker_input"]["squares"][0]["corners"][0][0] = "1/1000"
    _write_json(path, controls)
    with pytest.raises(ValueError, match="negative-control checker-input semantic mismatch"):
        packet.check([], replay=False)
    _write_json(path, packet.negative_controls())
    path = small_packet / "acquisition/release-normalized-claims.json"
    claims = packet.read_json(path)
    claims["results"][0]["offered_side"] = "2.0000"
    _write_json(path, claims)
    with pytest.raises(ValueError, match="normalized claims mismatch"):
        packet.check([], replay=False)


def test_receipt_and_literal_size_ceilings_are_enforced(
    small_packet: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(packet, "MAX_RECEIPT_BYTES", 16)
    with pytest.raises(ValueError, match="byte ceiling"):
        packet.read_json(small_packet / "receipts/certification.json")
    witness = packet.to_witness(packet.read_fact(2))
    witness["squares"][0]["corners"][0][0] = "1" * (packet.MAX_CHECKER_LITERAL_CHARS + 1)
    with pytest.raises(ValueError, match="bounded exact rational"):
        packet.checker_input(witness)
    witness["squares"][0]["corners"][0][0] = "1/0"
    with pytest.raises(ValueError, match="nonzero"):
        packet.checker_input(witness)
