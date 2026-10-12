"""The lazy catalogue preserves its publication subset without eager polynomial bytes."""

from __future__ import annotations

import json
from collections.abc import Mapping
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from devtools import exact_catalogue
from devtools import render_exact_side_values as paper
from tests.exact_side_values_fixture import adopted_current


def _metadata_url(row: Mapping[str, Any]) -> str:
    return f"{exact_catalogue.DATA_DIRECTORY}/metadata/{row['id']}.json"


def _coefficients_url(row: Mapping[str, Any]) -> str:
    return f"{exact_catalogue.DATA_DIRECTORY}/coefficients/{row['id']}.json"


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
    assert index["schema_version"] == 2
    assert all("metadata_url" not in row and "coefficients_url" not in row for row in rows)
    published = exact_catalogue.publication_register(register)
    originals = [*published["entries"], *published["historical_entries"]]
    assert len(rows) == len(originals)
    assert len({row["id"] for row in rows}) == len(rows)
    for row, original in zip(rows, originals, strict=True):
        metadata = json.loads(files[tmp_path / _metadata_url(row)])
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
        assert '"coefficients":' not in files[tmp_path / _metadata_url(row)]
        assert '"latex":' not in files[tmp_path / _metadata_url(row)]
        if row["kind"] == "polynomial":
            coefficients = json.loads(files[tmp_path / _coefficients_url(row)])
            assert coefficients["coefficients"] == original["polynomial"]["coefficients"]
    assert all(row["section"] == "current" for row in rows[:324])
    assert all(row["section"] == "historical" for row in rows[324:])
    n83 = next(row for row in rows if row["id"] == "current-n83")
    assert n83["degree"] == 672
    assert n83["legacy_anchor"] == "current-polynomial-for--79"
    assert len(json.loads(files[tmp_path / _coefficients_url(n83)])["coefficients"]) == 673
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
    assert not any(
        record.get("source_certificate") for record in published["historical_entries"]
    )
    adopted = [record for record in published["entries"] if record.get("source_certificate")]
    assert len(adopted) == 49
    latest_sources = {
        result: sorted(
            record["n"]
            for record in adopted
            if record["source_certificate"]["result"] == result
        )
        for result in ("T-151", "T-152")
    }
    assert latest_sources == {
        "T-151": [176, 181, 238, 239, 270, 271, 272],
        "T-152": [304, 305],
    }
    n105_sources = [
        (section, record)
        for section in ("entries", "historical_entries")
        for record in register[section]
        if record["n"] == 105 and record.get("source_certificate")
    ]
    assert len(n105_sources) == 5
    assert {
        (
            section,
            record["source_certificate"]["result"],
            record["source_certificate"]["source_key"],
        )
        for section, record in n105_sources
    } == {
        ("entries", "T-130", "[Couzo follow-up refinements 2026-10-08]"),
        ("historical_entries", "T-138", "[Mishapolk decimal poses 2026-10-09]"),
        ("historical_entries", "T-128", "[Couzo exact refinements 2026-10-08]"),
        ("historical_entries", "T-125", "[ry-xu square packing 2026]"),
        ("historical_entries", "T-129", "[Daniel dated certificates 105 and 130 2026-10-07]"),
    }
    assert all(
        record["source_certificate"]["adoption"]
        == ("adopted" if section == "entries" else "not-selected")
        for section, record in n105_sources
    )
    assert all(
        record["status"] == "open" if section == "entries" else record["kind"] == "superseded"
        for section, record in n105_sources
    )
    for record in adopted:
        certificate = record["source_certificate"]
        assert certificate["adoption"] == "adopted"
        assert certificate["geometry_replay"] == "native-replay-retained"
        assert certificate["verification"] == "V3"
        assert certificate["confirmation"] == "C3"
        assert "adopted-current" in record["source_statuses"]
    (n155,) = [row for row in rows if row["n"] == 155]
    assert n155["id"] == "current-n155"
    metadata155 = json.loads(files[tmp_path / _metadata_url(n155)])
    assert metadata155["record"]["source_certificate"]["result"] == "T-149"
    assert (
        metadata155["record"]["source_certificate"]["source_key"]
        == "[Ostashev records 2026-10-11]"
    )
    # The two old equal-side native occurrences remain independently recoverable in raw history.
    n155_records = [
        record
        for record in register["historical_entries"]
        if record["n"] == 155 and record.get("source_certificate", {}).get("result") == "T-128"
    ]
    assert len(n155_records) == 2
    assert all(record["kind"] == "superseded" for record in n155_records)
    assert n155_records[0]["side"] == n155_records[1]["side"]
    assert {record["source_certificate"]["source_key"] for record in n155_records} == {
        "[Couzo exact refinements 2026-10-08]",
        "[Daniel record hunt 2026-10-09]",
    }
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
        *(tmp_path / _metadata_url(row) for row in rows),
        *(tmp_path / _coefficients_url(row) for row in rows),
    }
    for row, record in zip(rows, [current, *historical[1:], *source_roots], strict=True):
        metadata = json.loads(files[tmp_path / _metadata_url(row)])
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
        metadata = json.loads(files[tmp_path / _metadata_url(row)])
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
    metadata = json.loads(files[tmp_path / _metadata_url(row)])
    assert _restore(metadata["record"], files, tmp_path) == original
    assert "pending (V0/C0)" in metadata["claim"]
    assert "Native geometry replay is retained" in metadata["claim"]
    assert "not been replayed" not in metadata["claim"]
    rendered = paper.source_certificate_markdown(original)
    for value in certificate.values():
        assert f"<code>{value}</code>" in rendered


def test_legacy_heading_anchors_follow_polynomial_order_across_numeric_gaps(
    tmp_path: Path,
) -> None:
    register = {
        "entries": [
            {"n": 1, "degree": 1, "polynomial": {"coefficients": ["1", "-1"]}},
            {"n": 2, "degree": 1, "polynomial": {"coefficients": ["1", "-2"]}},
            {"n": 3},
            {"n": 4, "degree": 1, "polynomial": {"coefficients": ["1", "-4"]}},
        ]
    }
    index = json.loads(
        exact_catalogue.output_files(register, papers=tmp_path)[
            tmp_path / exact_catalogue.INDEX_PATH
        ]
    )
    assert [row["legacy_anchor"] for row in index["entries"]] == [
        "current-polynomial-for-",
        "current-polynomial-for--1",
        None,
        "current-polynomial-for--2",
    ]


@pytest.mark.parametrize("position", [0, 1, 2])
def test_distinct_inserted_side_preserves_existing_source_payload_ids(tmp_path, position):
    first = {
        "n": 155,
        "side": "12.5",
        "degree": 1,
        "kind": "unreconciled-source",
        "polynomial": {"coefficients": ["2", "-25"]},
        "source_certificate": {
            "source_key": "original finder",
            "verification": "V3",
            "confirmation": "C3",
            "adoption": "pending",
            "geometry_replay": "native-replay-retained",
            "facts": "packing/first.json",
            "receipt": "packing/first-replay.json",
        },
    }
    second = deepcopy(first)
    second["source_certificate"].update(
        source_key="independent retainer",
        facts="packing/second.json",
        receipt="packing/second-replay.json",
    )
    old = {"entries": [], "historical_entries": [first, second]}
    before = exact_catalogue.output_files(old, papers=tmp_path)
    old_rows = json.loads(before[tmp_path / exact_catalogue.INDEX_PATH])["entries"]
    assert old_rows[1]["id"] == old_rows[0]["id"] + "-occurrence2"
    inserted = deepcopy(first)
    inserted.update(side="12.4", polynomial={"coefficients": ["5", "-62"]})
    inserted["source_certificate"]["source_key"] = "new distinct construction"
    new = deepcopy(old)
    new["historical_entries"].insert(position, inserted)
    after = exact_catalogue.output_files(new, papers=tmp_path)
    for path, payload in before.items():
        if path != tmp_path / exact_catalogue.INDEX_PATH:
            assert after[path] == payload
    rows = json.loads(after[tmp_path / exact_catalogue.INDEX_PATH])["entries"]
    assert {row["id"] for row in old_rows} < {row["id"] for row in rows}
    for old_row, original in zip(old_rows, (first, second), strict=True):
        metadata = json.loads(after[tmp_path / _metadata_url(old_row)])
        assert _restore(metadata["record"], after, tmp_path) == original
    assert [row["component"] for row in rows] == ["H_155,1", "H_155,2", "H_155,3"]


def test_inserted_invalid_source_is_refused_instead_of_skipped_for_stable_ids(tmp_path):
    first = {
        "n": 155,
        "side": "12.5",
        "degree": 1,
        "kind": "unreconciled-source",
        "polynomial": {"coefficients": ["2", "-25"]},
    }
    inserted = deepcopy(first)
    inserted.update(side="12.4", polynomial={"coefficients": ["0", "-62"]})
    with pytest.raises(exact_catalogue.ExactCatalogueError, match="nonzero lead"):
        exact_catalogue.output_files(
            {"entries": [], "historical_entries": [first, inserted, first]}, papers=tmp_path
        )
    assert list(tmp_path.iterdir()) == []


def test_adopted_current_custody_round_trips_and_claims_only_the_finite_bound(tmp_path):
    original = adopted_current()
    files = exact_catalogue.output_files({"entries": [original]}, papers=tmp_path)
    index = json.loads(files[tmp_path / exact_catalogue.INDEX_PATH])
    assert index["schema_version"] == 2
    (row,) = index["entries"]
    assert row["id"] == "current-n155"
    metadata = json.loads(files[tmp_path / _metadata_url(row)])
    assert metadata["schema_version"] == 1
    assert _restore(metadata["record"], files, tmp_path) == _without_polynomial_representations(
        original
    )
    assert "adopted (V3/C3)" in metadata["claim"]
    assert "Global optimality remains open" in metadata["claim"]
    assert "T-149" in row["search_text"]
    assert "scoped-finite-feasibility-confirmed" in row["search_text"]


@pytest.mark.parametrize("adoption", ["pending", "not-selected", "unknown", None, [], {}])
def test_current_certificate_refuses_a_nonadopted_or_unknown_disposition(tmp_path, adoption):
    original = adopted_current()
    original["source_certificate"]["adoption"] = adoption
    with pytest.raises(exact_catalogue.ExactCatalogueError, match="adoption"):
        exact_catalogue.output_files({"entries": [original]}, papers=tmp_path)


def test_historical_certificate_refuses_adopted_current_disposition(tmp_path):
    record = adopted_current()
    record.update(kind="unreconciled-source", side=record["side"]["value"])
    with pytest.raises(exact_catalogue.ExactCatalogueError, match=r"historical.*adoption"):
        exact_catalogue.output_files(
            {"entries": [], "historical_entries": [record]}, papers=tmp_path
        )
