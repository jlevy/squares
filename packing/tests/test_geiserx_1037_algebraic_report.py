"""Attachment-to-fact custody and native house admission for the two quadratic cases."""

from __future__ import annotations

import gzip
import json
import lzma
import shutil
from collections.abc import Iterator
from pathlib import Path

import pytest

from devtools import algebraic_witness_reports as fields
from devtools import exact_sides, retained_data, select_houses
from devtools import geiserx_1037_algebraic_report as source
from devtools import upper_bound_houses as houses
from devtools import upper_bound_reports as reports
from sqpack.witness import validate_witness_document, witness_document, witness_envelope


@pytest.fixture
def packet(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[Path]:
    original = source.packet_path()
    target = tmp_path / "packing/resources/web" / source.PACKET_NAME
    for path in source.inputs(original):
        destination = target / path.relative_to(original)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)
    prior = reports.packet_path
    monkeypatch.setattr(
        reports,
        "packet_path",
        lambda name: target if name == source.PACKET_NAME else prior(name),
    )
    monkeypatch.setattr(houses, "ROOT", tmp_path / "packing")
    monkeypatch.setattr(houses, "REPO", tmp_path)
    monkeypatch.setattr(reports, "REPO", tmp_path)
    houses.clear_caches()
    select_houses.algebraic_counts.cache_clear()
    try:
        yield target
    finally:
        houses.clear_caches()
        select_houses.algebraic_counts.cache_clear()


def test_original_geometry_native_rows_and_house_agree(
    packet: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    held = fields.read_facts(packet)
    house_source = houses.field_source("test-only", source.PACKET_NAME, source.COUNTS)
    monkeypatch.setattr(houses, "source_for", lambda _n: house_source)
    expected_forms = {202: "(1417-19*sqrt(3))/94", 263: "(1605-19*sqrt(3))/94"}
    for n, witness in held.items():
        assert witness == source.build_witness(packet, n)
        assert len(witness["squares"]) == n
        side = source.exact_side(n)
        assert isinstance(side, exact_sides.Algebraic)
        assert exact_sides.form(side) == expected_forms[n]
        positive = fields.check(packet, [n])[n]
        assert positive["pairs_tested"] == n * (n - 1) // 2
        house = houses.expected_house(n)
        assert house["id"] == f"W-known-best-n{n}"
        assert house["certificate"]["result"]["id"] == house["id"]
        assert house["certificate"]["kind"] == "exact-number-field-sat"
        assert house["source"]["revision"] == f"attachment-sha256:{source.ARCHIVE_SHA256}"
        origin = house_source.origin(n)
        assert origin.raw_asset_retained
        assert origin.path == retained_data.compressed_path(packet / source.fact_path(n))
        assert (
            validate_witness_document(
                witness_envelope(house, schema="witness.schema.yaml"),
                path=fields.WITNESS_SCHEMA,
                fallback_schema=fields.WITNESS_SCHEMA,
            )
            == house
        )
    assert reports.import_packet(source.SOURCE_KEY) == packet
    assert select_houses.algebraic_counts(source.SOURCE_KEY) == frozenset(source.COUNTS)
    assert fields.read_facts(packet, set()) == {}


def test_changed_member_and_custody_are_refused(packet: Path) -> None:
    path = packet / source.source_path(202)
    original = path.read_bytes()
    path.write_bytes(gzip.compress(gzip.decompress(original).replace(b"1303/94", b"1304/94")))
    with pytest.raises(fields.ReportError, match="attachment member differs"):
        source.checked_source(packet, 202)
    path.write_bytes(original)
    custody = packet / source.CUSTODY
    record = json.loads(custody.read_text())
    record["attachment"]["sha256"] = "0" * 64
    custody.write_text(json.dumps(record))
    with pytest.raises(fields.ReportError, match="custody identity differs"):
        source.checked_source(packet, 202)


def test_changed_fact_is_refused(packet: Path) -> None:
    witness = source.read_witness(packet, 202)
    witness["squares"][0]["center"][0] = "1"
    path = retained_data.compressed_path(packet / source.fact_path(202))
    path.write_bytes(
        gzip.compress(witness_document(witness, schema=fields.FACT_SCHEMA).encode())
    )
    with pytest.raises(fields.ReportError, match="does not rebuild"):
        fields.read_facts(packet, {202})


def test_changed_receipt_copy_is_refused(packet: Path) -> None:
    path = fields.receipt_path(packet, 263)
    record = json.loads(lzma.decompress(path.read_bytes()))
    record["cases"][0]["exact_verify"]["id"] = "W-other-n263-positive"
    path.write_bytes(lzma.compress(json.dumps(record).encode(), preset=0))
    with pytest.raises(fields.ReportError, match="wrapped native receipt differs"):
        fields.read_facts(packet, {263})


def test_changed_scope_is_refused(packet: Path) -> None:
    with pytest.raises(fields.ReportError, match="only 202 and 263"):
        fields.read_facts(packet, {204})
    path = packet / fields.DECLARATION
    record = json.loads(path.read_text())
    record["witnesses"][0]["degree"] = 3
    path.write_text(json.dumps(record))
    with pytest.raises(fields.ReportError, match="accepted source or scope"):
        fields.read_facts(packet, {202})


def test_registration_is_explicit_and_scope_bound(packet: Path) -> None:
    path = packet / source.REGISTRATION
    path.unlink(missing_ok=True)
    assert source.registered_result() is None
    record = {"result": "T-999", "n_values": [202, 263], "source_key": source.SOURCE_KEY}
    path.write_text(json.dumps(record))
    assert source.registered_result() == "T-999"
    assert path in source.inputs(packet)
    record["n_values"] = [202, 204]
    path.write_text(json.dumps(record))
    with pytest.raises(fields.ReportError, match="different source or scope"):
        source.registered_result()
