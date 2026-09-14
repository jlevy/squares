"""Exact controls for threshold-atom orbit admission against ceiling families."""

from __future__ import annotations

import json
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import admit_threshold_atom_orbits as admission
from sqpack.fractional.threshold import WEIGHTED_VARIANT, ThresholdAtom


def family(
    weight: str = "1",
    *,
    outer_side: str = "2",
    centre: tuple[str, str] = ("1", "1"),
    side: str = "1",
) -> dict[str, Any]:
    return {
        "n": 1,
        "outer_side": outer_side,
        "square_side": "1",
        "half_tangents": ["0", "1/2"],
        "placements": [["0", centre[0], centre[1], weight, side]],
        "total_weight": weight,
    }


def atom_input(
    points: list[list[str]],
    threshold: int,
    *,
    outer_side: str = "2",
) -> dict[str, Any]:
    atom = ThresholdAtom(
        tuple((Fraction(x), Fraction(y)) for x, y in points), threshold, Fraction(1)
    )
    return {
        "outer_side": outer_side,
        "square_side": "1",
        "atoms": [
            {
                "points": points,
                "threshold": threshold,
                "orbit_size": len(atom.orbit(Fraction(outer_side))),
            }
        ],
    }


def test_wrong_side_and_wrong_orbit_size_are_refused() -> None:
    atoms = atom_input([["1", "1"]], 1)
    wrong_side = deepcopy(atoms)
    wrong_side["outer_side"] = "3"
    with pytest.raises(admission.AdmissionError, match="outer_side 3 does not match"):
        admission.admit_records(family(), wrong_side)

    wrong_orbit = deepcopy(atoms)
    wrong_orbit["atoms"][0]["orbit_size"] = 8
    with pytest.raises(admission.AdmissionError, match="exact D4 reconstruction has 1"):
        admission.admit_records(family(), wrong_orbit)


def test_negative_family_weight_and_false_total_are_refused() -> None:
    atoms = atom_input([["1", "1"]], 1)
    with pytest.raises(admission.AdmissionError, match="non-negative"):
        admission.admit_records(family("-1"), atoms)
    false_total = family()
    false_total["total_weight"] = "2"
    with pytest.raises(admission.AdmissionError, match="does not match its placements"):
        admission.admit_records(false_total, atoms)


@pytest.mark.parametrize(
    ("weight", "admitted", "charge", "slack"),
    [("1", True, "1", "0"), ("3/2", False, "3/2", "-1/2")],
)
def test_valid_and_violated_atom_rows_are_distinguished(
    *, weight: str, admitted: bool, charge: str, slack: str
) -> None:
    receipt = admission.admit_records(family(weight), atom_input([["1", "1"]], 1))
    result = receipt["atom_admission"]
    assert result["admitted"] is admitted
    assert result["orbits"][0]["charge"] == charge
    assert result["orbits"][0]["slack"] == slack
    assert bool(result["violations"]) is not admitted


def test_closed_boundary_memberships_are_charged() -> None:
    # The four D4 images are the midpoints of the centred unit square's closed edges.
    receipt = admission.admit_records(family(), atom_input([["1/2", "1"]], 1))
    result = receipt["atom_admission"]
    assert result["distinct_sites"] == 4
    assert result["orbits"][0]["image_charges"] == ["1", "1", "1", "1"]
    assert result["orbits"][0]["charge"] == "4"
    assert result["orbits"][0]["budget"] == "4"
    assert result["admitted"] is True


def test_three_of_five_uses_the_actual_support_size_and_budget_one_per_image() -> None:
    points = [
        ["1/4", "1/3"],
        ["1/2", "1/3"],
        ["3/4", "1/3"],
        ["1/4", "2/3"],
        ["1/2", "2/3"],
    ]
    receipt = admission.admit_records(
        family("0", outer_side="4", centre=("2", "2")),
        atom_input(points, 3, outer_side="4"),
    )
    row = receipt["atom_admission"]["orbits"][0]
    assert row["support_size"] == 5
    assert row["per_image_budget"] == "1"
    assert row["budget"] == str(row["orbit_size"])


def test_charge_sums_every_orbit_image_and_uses_placement_weights() -> None:
    record = family("1/2", centre=("1/2", "1/2"), side="1/4")
    record["placements"].append(["0", "3/2", "3/2", "3/4", "1/4"])
    record["total_weight"] = "5/4"
    receipt = admission.admit_records(record, atom_input([["1/2", "1/2"]], 1))
    row = receipt["atom_admission"]["orbits"][0]
    assert row["image_charges"] == ["1/2", "0", "0", "3/4"]
    assert row["charge"] == "5/4"
    assert row["budget"] == "4"
    assert receipt["atom_admission"]["worst"]["charge_to_budget"] == "5/16"


def test_cli_serializes_exact_receipt_and_keeps_ceiling_proof_separate(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    family_path = tmp_path / "family.json"
    atoms_path = tmp_path / "atoms.json"
    family_path.write_text(json.dumps(family("3/2")))
    atoms_path.write_text(json.dumps(atom_input([["1", "1"]], 1)))
    assert admission.main([str(family_path), str(atoms_path)]) == 1
    receipt = json.loads(capsys.readouterr().out)
    assert receipt["atom_admission"]["worst"] == {
        "budget": "1",
        "charge": "3/2",
        "charge_to_budget": "3/2",
        "index": 0,
    }
    assert receipt["ceiling_proof"]["checked"] is False
    assert "K0--K3" in receipt["ceiling_proof"]["obligation"]


def test_a_declared_input_kind_is_checked_rather_than_ignored() -> None:
    """The receipt stamped its own kind from the start but read no declared one.

    A record of another shape whose field names happen to line up was admitted without
    complaint, which is an admission receipt attesting to an object nobody chose. The
    sibling `devtools.admit_fixed_support_dual` has always checked.
    """

    atoms = atom_input([["1", "1"]], 1)
    atoms["kind"] = "something-else/v9"
    with pytest.raises(admission.AdmissionError, match="does not accept"):
        admission.admit_records(family(), atoms)
    # An undeclared kind stays readable: the retained inputs carry none.
    assert "kind" not in atom_input([["1", "1"]], 1)


def test_the_per_image_budget_is_a_token_budget() -> None:
    """Five sites floor to one; their eight tokens must instead give budget two."""
    points = [["1", "1"], ["1", "13/10"], ["13/10", "1"], ["7/10", "1"], ["1", "7/10"]]
    atom = ThresholdAtom(
        tuple((Fraction(x), Fraction(y)) for x, y in points), 4, Fraction(1), (2, 2, 2, 1, 1)
    )
    atoms = {
        "outer_side": "2",
        "atoms": [atom.to_record() | {"orbit_size": len(atom.orbit(Fraction(2)))}],
    }
    receipt = admission.admit_records(family(), atoms)
    row = receipt["atom_admission"]["orbits"][0]
    assert row["support_size"] == 5
    assert row["token_count"] == 8
    # The receipt stringifies every rational figure; this one is an integer budget.
    assert row["per_image_budget"] == "2"
    assert row["budget"] == str(2 * row["orbit_size"])


def test_token_counts_without_their_variant_are_refused_by_the_admitter() -> None:
    atoms = atom_input([["1", "1"], ["1", "13/10"]], 2)
    atoms["atoms"][0]["multiplicities"] = [2, 1]
    with pytest.raises(admission.AdmissionError, match="multiplicities"):
        admission.admit_records(family(), atoms)


@pytest.mark.parametrize(
    ("weight", "admitted", "charge", "slack"),
    [("1", True, "4", "0"), ("3/2", False, "6", "-2")],
)
def test_a_heavy_site_alone_reaches_the_threshold_in_every_orbit_image(
    *, weight: str, admitted: bool, charge: str, slack: str
) -> None:
    atom = ThresholdAtom(
        ((Fraction(1), Fraction(1)), (Fraction(1), Fraction(17, 10))),
        2,
        Fraction(1),
        (2, 1),
    )
    images = atom.orbit(Fraction(2))
    assert len(images) == 4
    atoms = {
        "outer_side": "2",
        "atoms": [atom.to_record() | {"orbit_size": len(images)}],
    }
    result = admission.admit_records(family(weight), atoms)["atom_admission"]
    row = result["orbits"][0]
    assert row["image_charges"] == [weight] * 4
    assert row["charge"] == charge
    assert row["budget"] == "4"
    assert row["slack"] == slack
    assert result["admitted"] is admitted


@pytest.mark.parametrize(
    "entry",
    [
        {"variant": WEIGHTED_VARIANT, "weighted_points": []},
        {"variant": None, "points": [["1", "1"]]},
        {"variant": WEIGHTED_VARIANT, "points": [["1", "1"]], "multiplicities": []},
        {"variant": WEIGHTED_VARIANT, "weighted_points": [["1", "1", True]]},
        {"variant": WEIGHTED_VARIANT, "weighted_points": [["1", "1", 2.0]]},
        {"variant": WEIGHTED_VARIANT, "weighted_points": [["1", "1", 2]], "points": []},
        {"weighted_points": [["1", "1", 2]]},
    ],
)
def test_malformed_weighted_sites_refuse_with_an_indexed_reader_error(
    entry: dict[str, Any], tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    atoms = {"outer_side": "2", "atoms": [entry | {"threshold": 1, "orbit_size": 1}]}
    with pytest.raises(admission.AdmissionError, match="invalid atom 0"):
        admission.admit_records(family(), atoms)
    family_path, atoms_path = tmp_path / "family.json", tmp_path / "atoms.json"
    family_path.write_text(json.dumps(family()), encoding="utf-8")
    atoms_path.write_text(json.dumps(atoms), encoding="utf-8")
    assert admission.main([str(family_path), str(atoms_path)]) == 2
    receipt = json.loads(capsys.readouterr().out)
    assert receipt["atom_admission"]["admitted"] is False
    assert "invalid atom 0" in receipt["error"]
