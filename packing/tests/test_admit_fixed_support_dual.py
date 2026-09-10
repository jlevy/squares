"""Exact positive and negative controls for fixed-support dual admission."""

from __future__ import annotations

import json
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import admit_fixed_support_dual as reader
from sqpack.fractional import ceiling

PACKING = Path(ceiling.__file__).resolve().parents[3]
RESULTS = (
    PACKING
    / "campaign"
    / "series"
    / "series-000-smoke-and-calibration"
    / "results"
    / "agenda-034"
)
CERTIFICATE = RESULTS / "lane-a6-dual-bracket-10-42.json"
SUPPORT = RESULTS / "lane-a3-family-153-40-sites-round1-exact25.json"


def records() -> tuple[dict[str, Any], dict[str, Any]]:
    return (
        dict(reader.load_record(CERTIFICATE, "dual certificate")),
        dict(reader.load_record(SUPPORT, "support family")),
    )


def test_the_retained_seven_rows_rebuild_the_exact_upper_bound() -> None:
    certificate, support = records()
    receipt = reader.admit_records(certificate, support)
    assert receipt["admitted"] is True
    assert receipt["support"] == {
        "certificate_representatives_match_every_source_orbit_once": True,
        "objective_orbit_costs_match_sizes": True,
        "orbit_sizes": [8] * 35,
        "source_d4_closure_placements": 280,
        "source_d4_orbits": 35,
        "source_is_exactly_d4_closed": True,
        "source_positive_placements": 280,
    }
    assert receipt["priced_rows"]["depth_rows"] == 6
    assert receipt["priced_rows"]["threshold_atom_rows"] == 1
    assert receipt["priced_rows"]["rows"][-1]["row"] == 142090
    assert receipt["priced_rows"]["rows"][-1]["budget"] == "8"
    assert receipt["dual"]["bound"] == "2605263163/250000000"
    assert receipt["dual"]["minimum_column_slack"] == "3/500000000"
    assert receipt["scope"]["selected_row_lower"] == {
        "checked": False,
        "declared": "325657893/31250000",
        "note": (
            "the reader did not check the candidate family or the other program rows; "
            "the retained max-depth verdict is 105263157/100000000, above one"
        ),
    }


def test_a_saved_row_coefficient_is_checked_against_exact_members_itself() -> None:
    certificate, support = records()
    certificate = deepcopy(certificate)
    certificate["dual"]["priced_rows"][0]["bounds_support_orbits"][0][1] = "1"
    with pytest.raises(reader.AdmissionError, match="stored coefficients differ"):
        reader.admit_records(certificate, support)


@pytest.mark.parametrize("multiplier", ["-1/2", 0.5, "1/0"])
def test_a_negative_or_malformed_multiplier_is_refused(multiplier: object) -> None:
    certificate, support = records()
    certificate = deepcopy(certificate)
    certificate["dual"]["priced_rows"][0]["multiplier"] = multiplier
    with pytest.raises(reader.AdmissionError, match="multiplier"):
        reader.admit_records(certificate, support)


def test_the_three_of_five_budget_uses_the_floor() -> None:
    certificate, support = records()
    certificate = deepcopy(certificate)
    threshold_row = certificate["dual"]["priced_rows"][-1]
    assert len(threshold_row["identity"]["points"]) == 5
    assert threshold_row["identity"]["threshold"] == 3
    assert threshold_row["identity"]["orbit_size"] == 8
    threshold_row["budget"] = "40/3"
    with pytest.raises(reader.AdmissionError, match="exact row budget is 8"):
        reader.admit_records(certificate, support)


def test_wrong_bound_support_count_and_side_are_each_refused() -> None:
    certificate, support = records()
    wrong_bound = deepcopy(certificate)
    wrong_bound["dual"]["bound"] = "2605263164/250000000"
    with pytest.raises(reader.AdmissionError, match="recomputed bound"):
        reader.admit_records(wrong_bound, support)

    wrong_support = deepcopy(certificate)
    wrong_support["support"]["placements"] = 279
    with pytest.raises(reader.AdmissionError, match="exact source has 280"):
        reader.admit_records(wrong_support, support)

    wrong_side = deepcopy(certificate)
    wrong_side["square_side"] = "1"
    with pytest.raises(reader.AdmissionError, match="does not match support"):
        reader.admit_records(wrong_side, support)


def test_duplicate_column_orbits_are_refused_before_the_matrix_is_read() -> None:
    certificate, support = records()
    certificate = deepcopy(certificate)
    certificate["dual"]["columns"][1]["representative"] = deepcopy(
        certificate["dual"]["columns"][0]["representative"]
    )
    with pytest.raises(reader.AdmissionError, match="repeats the support orbit"):
        reader.admit_records(certificate, support)


def test_a_source_missing_one_d4_image_is_refused() -> None:
    certificate, support = records()
    support = deepcopy(support)
    removed = support["placements"].pop()
    support["total_weight"] = str(Fraction(support["total_weight"]) - Fraction(removed[3]))
    with pytest.raises(reader.AdmissionError, match="not exactly D4-closed"):
        reader.admit_records(certificate, support)


def test_a_nonpositive_source_weight_is_not_silently_dropped() -> None:
    certificate, support = records()
    support = deepcopy(support)
    previous = Fraction(support["placements"][0][3])
    support["placements"][0][3] = "0"
    support["total_weight"] = str(Fraction(support["total_weight"]) - previous)
    with pytest.raises(reader.AdmissionError, match="must have positive weight"):
        reader.admit_records(certificate, support)


def synthetic_undercovered_dual() -> tuple[dict[str, Any], dict[str, Any]]:
    support = {
        "n": 8,
        "outer_side": "2",
        "square_side": "1/4",
        "half_tangents": ["0", "1"],
        "placements": [
            [tangent, x, y, "1", "1/4"]
            for tangent in ("0", "1")
            for x, y in (
                ("1/2", "1/2"),
                ("1/2", "3/2"),
                ("3/2", "1/2"),
                ("3/2", "3/2"),
            )
        ],
        "total_weight": "8",
    }
    representative = {
        "half_tangent": "0",
        "centre_x": "1/2",
        "centre_y": "1/2",
        "side": "1/4",
    }
    certificate = {
        "kind": "lane-a6/dual-bracket/v1",
        "outer_side": "2",
        "square_side": "1/4",
        "support": {"placements": 8, "d4_orbits": 1},
        "program": {
            "rows_total": 1,
            "depth_rows": 1,
            "atom_rows": 0,
            "seeded_atom_rows": 0,
            "columns": 1,
        },
        "dual": {
            "n_priced_rows": 1,
            "bound": "1",
            "a_transpose_u_ge_cost": False,
            "priced_rows": [
                {
                    "row": 0,
                    "multiplier": "1",
                    "budget": "1",
                    "contribution": "1",
                    "bounds_support_orbits": [],
                    "identity": {"kind": "depth-at-site", "site": ["1", "1"]},
                }
            ],
            "columns": [
                {
                    "orbit": 0,
                    "orbit_size": 8,
                    "cost": "8",
                    "A_transpose_u": "0",
                    "slack": "-8",
                    "holds": False,
                    "representative": representative,
                }
            ],
        },
        "bracket": {"lower_exact": "0", "upper_exact": "1"},
    }
    return certificate, support


def test_exact_column_undercoverage_refuses_a_self_consistent_false_dual() -> None:
    certificate, support = synthetic_undercovered_dual()
    with pytest.raises(reader.AdmissionError, match=r"fails A\^T u >= cost by 8"):
        reader.admit_records(certificate, support)


def test_cli_refuses_a_bad_certificate_without_a_success_receipt(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    certificate, support = records()
    certificate = deepcopy(certificate)
    certificate["dual"]["priced_rows"][0]["multiplier"] = "-1"
    certificate_path = tmp_path / "certificate.json"
    support_path = tmp_path / "support.json"
    certificate_path.write_text(json.dumps(certificate, default=str), encoding="utf-8")
    support_path.write_text(json.dumps(support, default=str), encoding="utf-8")
    assert reader.main([str(certificate_path), str(support_path)]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert '"admitted": false' in captured.err
    assert "Traceback" not in captured.err
