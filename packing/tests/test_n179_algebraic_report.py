"""Attachment custody, exact selection and native-house contract for issue 959."""

from __future__ import annotations

import gzip
import json
import lzma
import shutil
from pathlib import Path
from typing import Any

import pytest

from devtools import algebraic_witness_reports as fields
from devtools import exact_sides, retained_data, select_houses
from devtools import n179_algebraic_report as n179
from devtools import upper_bound_houses as houses
from devtools import upper_bound_reports as reports
from sqpack.field import FieldElement
from sqpack.witness import validate_witness_document, witness_document, witness_envelope
from sqpack.yamlio import load_yaml


@pytest.fixture
def packet(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    original = n179.packet_path()
    target = tmp_path / "packing/resources/web" / n179.PACKET_NAME
    relatives = [n179.SOURCE, n179.CUSTODY, Path(str(n179.FACT) + ".gz")]
    relatives.append(fields.receipt_path(original, 179).relative_to(original))
    for relative in relatives:
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(original / relative, destination)
    (target / fields.DECLARATION).write_text(
        json.dumps(n179.declaration(read_on="2026-11-21", read_at_main="test context")),
        encoding="utf-8",
    )
    prior = reports.packet_path
    monkeypatch.setattr(
        reports, "packet_path", lambda name: target if name == n179.PACKET_NAME else prior(name)
    )
    monkeypatch.setattr(houses, "ROOT", tmp_path / "packing")
    monkeypatch.setattr(houses, "REPO", tmp_path)
    monkeypatch.setattr(reports, "REPO", tmp_path)
    houses.clear_caches()
    return target


def test_original_and_retained_fact_agree(packet: Path) -> None:
    actual = fields.read_facts(packet, {179})
    assert actual[179] == n179.build_witness(packet)
    assert len(actual[179]["squares"]) == 179
    assert fields.read_facts(packet, set()) == {}


@pytest.mark.parametrize("count", [70, 178, 180])
def test_undeclared_count_is_refused(packet: Path, count: int) -> None:
    with pytest.raises(fields.ReportError, match="undeclared count"):
        fields.read_facts(packet, {count})
    with pytest.raises(fields.ReportError, match="only n=179"):
        n179.exact_side(count)


def test_changed_source_is_refused(packet: Path) -> None:
    path = packet / n179.SOURCE
    path.write_bytes(path.read_bytes() + b"changed")
    with pytest.raises(fields.ReportError, match="attachment member differs"):
        fields.read_facts(packet)


def test_changed_custody_is_refused(packet: Path) -> None:
    path = packet / n179.CUSTODY
    record = json.loads(path.read_text(encoding="utf-8"))
    record["archive_sha256"] = "0" * 64
    path.write_text(json.dumps(record), encoding="utf-8")
    with pytest.raises(fields.ReportError, match="custody identity differs"):
        fields.read_facts(packet)


def test_changed_fact_is_refused(packet: Path) -> None:
    witness = n179.read_witness(packet, 179)
    witness["side"][0] = "14"
    path = packet / (str(n179.FACT) + ".gz")
    path.write_bytes(
        gzip.compress(witness_document(witness, schema=fields.FACT_SCHEMA).encode())
    )
    with pytest.raises(fields.ReportError, match="does not rebuild"):
        fields.read_facts(packet)


def test_changed_declaration_is_refused(packet: Path) -> None:
    path = packet / fields.DECLARATION
    declaration = json.loads(path.read_text(encoding="utf-8"))
    declaration["witnesses"][0]["degree"] = 4
    path.write_text(json.dumps(declaration), encoding="utf-8")
    with pytest.raises(fields.ReportError, match="accepted source or scope"):
        fields.read_facts(packet)


def test_native_jobs_and_house_contract(packet: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    source = houses.field_source("T-999", n179.PACKET_NAME, (179,))
    witness = n179.read_witness(packet, 179)
    record = json.loads(lzma.decompress(fields.receipt_path(packet, 179).read_bytes()))
    jobs = {row["control"]: row for row in record["cases"]}
    assert set(jobs) == set(fields.JOBS)
    for name, job in jobs.items():
        fields.validate_job(job, witness, name)
        assert job[fields.ROUTE]["pairs_tested"] == 15931
        assert job[fields.ROUTE]["verification_passed"] is (name == "positive")
    monkeypatch.setattr(houses, "source_for", lambda _n: source)
    house = houses.expected_house(179)
    assert house["id"] == "W-known-best-n179"
    assert house["certificate"]["result"]["id"] == house["id"]
    assert house["certificate"]["kind"] == "exact-number-field-sat"
    assert house["source"]["key"] == n179.SOURCE_KEY
    assert all(path.is_file() for path in source.inputs((179,)))
    assert (
        validate_witness_document(
            witness_envelope(house, schema="witness.schema.yaml"),
            path=fields.WITNESS_SCHEMA,
            fallback_schema=fields.WITNESS_SCHEMA,
        )
        == house
    )


def test_native_positive_cannot_be_relabelled(packet: Path) -> None:
    witness = n179.read_witness(packet, 179)
    row: dict[str, Any] = json.loads(
        lzma.decompress(fields.receipt_path(packet, 179).read_bytes())
    )["cases"][0]
    row[fields.ROUTE]["id"] = "W-n179-959-algebraic-reading"
    with pytest.raises(fields.ReportError):
        fields.validate_job(row, witness, "positive")


def test_exact_selection_and_side_identities(packet: Path) -> None:
    assert reports.import_packet(n179.SOURCE_KEY) == packet
    assert select_houses.algebraic_counts(n179.SOURCE_KEY) == frozenset({179})
    side = select_houses.exact_side(n179.SOURCE_KEY, 179)
    assert exact_sides.ceiling(side, 16) == "13.8809603715555796"
    for n, shift in [(70, 5), (207, -1)]:
        path = reports.ROOT / f"witnesses/known-best/n-{n:03d}.yaml"
        witness = validate_witness_document(
            load_yaml(retained_data.read_retained_bytes(path).decode()),
            path=path,
            fallback_schema=fields.WITNESS_SCHEMA,
        )
        value = fields.side_of(witness)
        assert isinstance(value, FieldElement)
        assert exact_sides.compare(side, exact_sides.of_field_element(value + shift)) == 0


def test_registration_id_is_coordinator_supplied(packet: Path) -> None:
    assert n179.registered_result() is None
    path = packet / "acquisition/registration.json"
    path.write_text(
        json.dumps({"result": "T-999", "n": 179, "source_key": n179.SOURCE_KEY}),
        encoding="utf-8",
    )
    assert n179.registered_result() == "T-999"
    assert path in n179.inputs(packet)
    path.write_text(
        json.dumps({"result": "T-999", "n": 180, "source_key": n179.SOURCE_KEY}),
        encoding="utf-8",
    )
    with pytest.raises(fields.ReportError, match="different source"):
        n179.registered_result()


def test_conflicting_plain_fact_is_refused(packet: Path) -> None:
    witness = n179.read_witness(packet, 179)
    witness["side"][0] = "14"
    (packet / n179.FACT).write_text(
        witness_document(witness, schema=fields.FACT_SCHEMA), encoding="utf-8"
    )
    with pytest.raises(ValueError, match="differs from its compressed copy"):
        fields.read_facts(packet)


def test_symlinked_mathematical_source_is_refused(packet: Path) -> None:
    path = packet / n179.SOURCE
    twin = path.with_name("twin.gz")
    shutil.copy2(path, twin)
    path.unlink()
    path.symlink_to(twin)
    with pytest.raises(reports.ReportError, match="private repository file"):
        fields.read_facts(packet)
