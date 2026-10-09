"""The source catalogue is metadata, not a geometry or formalization verdict."""

from __future__ import annotations

import copy
import json

import pytest

from devtools import evand_report_catalogue as reports
from devtools.retained_data import read_retained_text


def rows() -> list[dict]:
    return json.loads(
        read_retained_text(reports.PACKET / "source/s12/search/exact/exact_forms.json.gz")
    )


def test_source_rosters_remain_reports_and_do_not_infer_a_band() -> None:
    result = reports.catalogue(rows())
    assert result["assurance"] == "reported"
    assert result["independent_geometry_replay"] == "not-attempted"
    assert result["independent_lean_replay"] == "not-attempted"
    assert result["polynomial_minimality"].startswith("source-claimed")
    assert result["special_local_minimum_claims"] == {
        11: "grade A (N11L)",
        28: "grade A (N28L)",
    }
    assert 83 in result["open_counts"]
    assert not {110, 132, 156, 182, 210, 211, 240, 241, 272, 273, 306, 307} & set(
        result["band_local_minimum_claims"]
    )
    assert result["new_form_claims"][106]["degree"] == 32
    assert result["new_form_claims"][152]["degree"] == 40


def test_missing_or_duplicate_count_is_not_another_claim() -> None:
    original = rows()
    with pytest.raises(ValueError, match="exactly one row"):
        reports.catalogue(original[:-1])
    duplicate = copy.deepcopy(original)
    duplicate[-1]["n"] = duplicate[0]["n"]
    with pytest.raises(ValueError, match="duplicated"):
        reports.catalogue(duplicate)


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("S_degree", 9, "degree/coefficients"),
        ("S_interval", ["2", "1"], "invalid positive"),
        ("verify_exact", "true", "booleans"),
        ("lean_local_min", "global optimum", "unknown local"),
        ("data", "minpoly/data/n-999.minpoly.json.gz", "does not match"),
        ("new", "false", "must be boolean"),
        ("status", "confirmed", "unknown source status"),
    ],
)
def test_source_metadata_mutants_are_refused(field: str, value: object, message: str) -> None:
    modified = rows()
    modified[101][field] = value
    with pytest.raises(ValueError, match=message):
        reports.catalogue(modified)


def test_retained_catalogue_is_current_in_ci() -> None:
    retained = json.loads((reports.PACKET / "reported-catalogue.json").read_text())
    assert retained == json.loads(json.dumps(reports.catalogue(rows())))
