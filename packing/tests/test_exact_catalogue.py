"""The lazy catalogue preserves its publication subset without eager polynomial bytes."""

from __future__ import annotations

import json
from collections.abc import Mapping
from copy import deepcopy
from pathlib import Path
from typing import Any

from devtools import exact_catalogue
from devtools import render_exact_side_values as paper


def _restore(value: Any, files: Mapping[Path, str], papers: Path) -> Any:
    if isinstance(value, list):
        return [_restore(item, files, papers) for item in value]
    if not isinstance(value, dict):
        return value
    omitted = {"coefficients_url", "order"} if "coefficients_url" in value else set()
    restored = {
        key: _restore(item, files, papers) for key, item in value.items() if key not in omitted
    }
    if "coefficients_url" in value:
        payload = json.loads(files[papers / value["coefficients_url"]])
        assert payload["order"] == "descending"
        restored["coefficients"] = payload["coefficients"]
    return restored


def _without_polynomial_representations(value: Any) -> Any:
    if isinstance(value, list):
        return [_without_polynomial_representations(item) for item in value]
    if not isinstance(value, dict):
        return value
    omitted = {"latex", "text"} if "coefficients" in value else set()
    return {
        key: _without_polynomial_representations(item)
        for key, item in value.items()
        if key not in omitted
    }


def test_lazy_payloads_round_trip_published_records_and_original_coefficients(
    tmp_path: Path,
) -> None:
    register = paper.load_register()
    files = exact_catalogue.output_files(register, papers=tmp_path)
    index = json.loads(files[tmp_path / exact_catalogue.INDEX_PATH])
    rows = index["entries"]
    published = exact_catalogue.publication_register(register)
    originals = [*published["entries"], *published["historical_entries"]]
    assert len(rows) == len(originals)
    assert len({row["id"] for row in rows}) == len(rows)
    for row, original in zip(rows, originals, strict=True):
        metadata = json.loads(files[tmp_path / row["metadata_url"]])
        if row["section"] == "historical" and original.get("reported_source"):
            assurance = original["assurance"]
            level = f"{assurance['verification']}/{assurance['confirmation']}"
            assert level in metadata["claim"]
        if original.get("source_certificate"):
            certificate = original["source_certificate"]
            level = f"{certificate['verification']}/{certificate['confirmation']}"
            assert level in metadata["claim"]
        assert _restore(metadata["record"], files, tmp_path) == (
            _without_polynomial_representations(original)
        )
        assert '"coefficients":' not in files[tmp_path / row["metadata_url"]]
        assert '"latex":' not in files[tmp_path / row["metadata_url"]]
        if row["coefficients_url"] is not None:
            coefficients = json.loads(files[tmp_path / row["coefficients_url"]])
            assert coefficients["coefficients"] == original["polynomial"]["coefficients"]
    assert all(row["section"] == "current" for row in rows[:324])
    assert all(row["section"] == "historical" for row in rows[324:])
    n83 = next(row for row in rows if row["id"] == "current-n83")
    assert n83["degree"] == 672
    assert n83["legacy_anchor"] == "current-polynomial-for--83"
    assert len(json.loads(files[tmp_path / n83["coefficients_url"]])["coefficients"]) == 673
    assert {record["kind"] for record in published["historical_entries"]} == {
        "outside-frontier",
        "source-invalid",
        "unreconciled-source",
    }
    source_roots = [
        record for record in published["historical_entries"] if record.get("reported_source")
    ]
    assert [record["n"] for record in source_roots] == [106, 152, 177]
    assert all(record["assurance"]["verification"] == "V0" for record in source_roots)
    assert all(record["assurance"]["confirmation"] == "C0" for record in source_roots)
    pending = [
        record for record in published["historical_entries"] if record.get("source_certificate")
    ]
    assert len(pending) == 15
    assert sum(record["n"] == 105 for record in pending) == 2
    n155 = [row for row in rows if row["section"] == "historical" and row["n"] == 155]
    assert len(n155) == 2
    assert n155[0]["id"] + "-occurrence2" == n155[1]["id"]
    assert "[Daniel record hunt 2026-10-09]" in n155[1]["title"]
    n155_records = [record for record in pending if record["n"] == 155]
    assert n155_records[0]["side"] == n155_records[1]["side"]
    assert {record["source_certificate"]["source_key"] for record in n155_records} == {
        "[Couzo exact refinements 2026-10-08]",
        "[Daniel record hunt 2026-10-09]",
    }
    for record in pending:
        certificate = record["source_certificate"]
        assert certificate["adoption"] == "pending"
        assert certificate["geometry_replay"] == "native-replay-retained"
        assert certificate["verification"] == "V0"
        assert certificate["confirmation"] == "C0"
    (superseded_daniel,) = [
        record
        for record in register["historical_entries"]
        if record["n"] == 102 and record.get("reported_source")
    ]
    assert superseded_daniel["kind"] == "superseded"
    assert superseded_daniel["assurance"]["verification"] == "V0"
    assert superseded_daniel["assurance"]["confirmation"] == "C0"
    assert '"coefficients":' not in files[tmp_path / exact_catalogue.INDEX_PATH]
    assert len(files[tmp_path / exact_catalogue.INDEX_PATH]) < 350_000


def test_publication_omits_only_superseded_rows_and_notes_without_mutating_source(
    tmp_path: Path,
) -> None:
    current = {
        "n": 83,
        "status": "open",
        "side": {"value": "9.25", "relation": "upper-bound"},
        "degree": 2,
        "polynomial": {"coefficients": ["1", "0", "-0083"]},
        "notes": [
            {
                "kind": "superseded-catalogue-polynomial",
                "degree": 1,
                "polynomial": {"coefficients": ["1", "-0079"]},
            },
            {
                "kind": "retained-source-polynomial",
                "degree": 1,
                "polynomial": {"coefficients": ["0001", "-0090"]},
            },
        ],
    }
    historical = [
        {
            "n": n,
            "kind": kind,
            "side": str(n),
            "degree": 1,
            "polynomial": {"coefficients": ["1", f"-{n}"]},
        }
        for n, kind in ((82, "superseded"), (1850, "outside-frontier"), (1, "source-invalid"))
    ]
    source_roots = [
        {
            "n": n,
            "kind": "unreconciled-source",
            "side": str(n),
            "degree": 1,
            "polynomial": {"coefficients": ["1", f"-{n}"]},
            "reported_source": {"interval_root_count": 1},
            "assurance": {"verification": "V0", "confirmation": "C0"},
        }
        for n in (102, 106, 152, 177)
    ]
    register = {
        "entries": [current],
        "historical_entries": [*historical, *source_roots],
        "sources": {"records": ["canonical source"]},
    }
    original = deepcopy(register)
    expected = deepcopy(register)
    expected["entries"][0]["notes"] = [current["notes"][1]]
    expected["historical_entries"] = [*historical[1:], *source_roots]
    published = exact_catalogue.publication_register(register)
    assert published == expected
    files = exact_catalogue.output_files(register, papers=tmp_path)
    assert register == original
    index = json.loads(files[tmp_path / exact_catalogue.INDEX_PATH])
    rows = index["entries"]
    assert [row["n"] for row in rows] == [83, 1850, 1, 102, 106, 152, 177]
    assert {row["status"] for row in rows[1:]} == {
        "outside-frontier",
        "source-invalid",
        "unreconciled-source",
    }
    assert set(files) == {
        tmp_path / exact_catalogue.INDEX_PATH,
        tmp_path
        / exact_catalogue.DATA_DIRECTORY
        / "coefficients/current-n83-notes-0-polynomial.json",
        *(tmp_path / row["metadata_url"] for row in rows),
        *(tmp_path / row["coefficients_url"] for row in rows),
    }
    for row, record in zip(rows, [current, *historical[1:], *source_roots], strict=True):
        metadata = json.loads(files[tmp_path / row["metadata_url"]])
        expected_record = expected["entries"][0] if row["section"] == "current" else record
        assert _restore(metadata["record"], files, tmp_path) == expected_record
        if record.get("reported_source"):
            assert "V0/C0" in metadata["claim"]
    assert all(
        "superseded" not in content and "-0079" not in content for content in files.values()
    )
    published["sources"]["records"].append("copy-only change")
    assert register == original


def test_empty_collections_and_repeated_historical_sides_are_deterministic(
    tmp_path: Path,
) -> None:
    empty = {"entries": [], "historical_entries": [], "sources": {"records": "source"}}
    files = exact_catalogue.output_files(empty, papers=tmp_path)
    assert set(files) == {tmp_path / exact_catalogue.INDEX_PATH}
    assert json.loads(files[tmp_path / exact_catalogue.INDEX_PATH])["entries"] == []
    record = {
        "n": 1850,
        "side": "52.00001",
        "current_side": None,
        "kind": "outside-frontier",
        "source_statuses": ["best-known"],
        "degree": 1,
        "polynomial": {"coefficients": ["0001", "-0052"], "height_digits": 4},
    }
    register = {"entries": [], "historical_entries": [record, record]}
    files = exact_catalogue.output_files(register, papers=tmp_path)
    assert files == exact_catalogue.output_files(register, papers=tmp_path)
    index = json.loads(files[tmp_path / exact_catalogue.INDEX_PATH])
    assert len({row["id"] for row in index["entries"]}) == 2
    for row in index["entries"]:
        metadata = json.loads(files[tmp_path / row["metadata_url"]])
        assert metadata["record"]["current_side"] is None
        assert _restore(metadata["record"], files, tmp_path) == record


def test_pending_native_certificate_preserves_custody_without_claiming_adoption(
    tmp_path: Path,
) -> None:
    certificate = {
        "result": "T-128",
        "source_key": "couzo-exact-refinements",
        "revision": "source-fixture",
        "facts": "packing/resources/web/fixture/facts.json",
        "original_certificate": "n105.cert",
        "receipt": "packing/resources/web/fixture/replay.json",
        "verification": "V0",
        "confirmation": "C0",
        "algebraic_identity": "independently-checked",
        "geometry_replay": "native-replay-retained",
        "adoption": "pending",
        "global_optimality": "not-established",
    }
    original = {
        "n": 105,
        "kind": "unreconciled-source",
        "side": "10.5",
        "degree": 1,
        "polynomial": {"coefficients": ["2", "-21"]},
        "source_certificate": certificate,
    }
    register = {"entries": [], "historical_entries": [original]}
    files = exact_catalogue.output_files(register, papers=tmp_path)
    row = json.loads(files[tmp_path / exact_catalogue.INDEX_PATH])["entries"][0]
    metadata = json.loads(files[tmp_path / row["metadata_url"]])
    assert _restore(metadata["record"], files, tmp_path) == original
    assert "pending (V0/C0)" in metadata["claim"]
    assert "Native geometry replay is retained" in metadata["claim"]
    assert "not been replayed" not in metadata["claim"]
    rendered = paper.source_certificate_markdown(original)
    for value in certificate.values():
        assert f"<code>{value}</code>" in rendered
