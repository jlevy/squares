"""The lazy catalogue preserves the register without eagerly shipping its polynomials."""

from __future__ import annotations

import json
from collections.abc import Mapping
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


def test_lazy_payloads_round_trip_every_record_and_original_coefficient(tmp_path: Path) -> None:
    register = paper.load_register()
    files = exact_catalogue.output_files(register, papers=tmp_path)
    index = json.loads(files[tmp_path / exact_catalogue.INDEX_PATH])
    rows = index["entries"]
    originals = [*register["entries"], *register["historical_entries"]]
    assert len(rows) == len(originals)
    assert len({row["id"] for row in rows}) == len(rows)
    for row, original in zip(rows, originals, strict=True):
        metadata = json.loads(files[tmp_path / row["metadata_url"]])
        if row["section"] == "historical" and original.get("reported_source"):
            assurance = original["assurance"]
            level = f"{assurance['verification']}/{assurance['confirmation']}"
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
    assert '"coefficients":' not in files[tmp_path / exact_catalogue.INDEX_PATH]
    assert len(files[tmp_path / exact_catalogue.INDEX_PATH]) < 350_000


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
