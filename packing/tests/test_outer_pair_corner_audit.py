"""Exact acceptance and failure controls for the outer-pair construction."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
from typing import cast

import pytest

from devtools import outer_pair_corner_audit as audit


def _checks(report: dict[str, object]) -> dict[str, dict[str, object]]:
    return cast("dict[str, dict[str, object]]", report["checks"])


def test_exact_four_square_target_refutes_only_the_local_incompatibility() -> None:
    report = audit.audit_family(audit.reference_family())
    checks = _checks(report)

    assert report["claim_refuted"] is True
    assert report["valid_target_counterexample"] is True
    assert report["q"] == "96/25"
    assert report["core_side"] == "9977/10000"
    assert report["eleven_square_packing_claimed"] is False
    assert report["scope"] == "four-square local ownership compatibility"
    identity = cast("dict[str, bool]", report["target_identity"])
    assert all(identity.values())
    squares = cast("list[dict[str, object]]", report["squares"])
    assert [row["name"] for row in squares] == ["A-minus", "A-plus", "C-minus", "C-plus"]
    assert all(row["unit_square"] is True and row["contained"] is True for row in squares)
    assert {row["center"] for row in squares} == {
        ("1/2", "71/50"),
        ("1/2", "121/50"),
        ("531/370", "47/74"),
        ("531/370", "5929/1850"),
    }
    assert all(check["holds"] is True for check in checks.values())


def test_all_six_sat_receipts_and_touching_semantics_are_exact() -> None:
    pairs = cast(
        "list[dict[str, object]]",
        _checks(audit.audit_family(audit.reference_family()))["pair_interior_disjointness"][
            "pairs"
        ],
    )
    receipts = {
        tuple(cast("list[str]", row["squares"])): (row["normal"], row["gap"]) for row in pairs
    }
    assert receipts == {
        ("A-minus", "A-plus"): (["0", "1"], "0"),
        ("A-minus", "C-minus"): (["-35/37", "12/37"], "137/34225"),
        ("A-minus", "C-plus"): (["0", "1"], "601/925"),
        ("A-plus", "C-minus"): (["0", "1"], "601/925"),
        ("A-plus", "C-plus"): (["35/37", "12/37"], "137/34225"),
        ("C-minus", "C-plus"): (["12/37", "35/37"], "8414/6845"),
    }
    assert all(row["interiors_disjoint"] is True for row in pairs)
    touching = next(row for row in pairs if row["gap"] == "0")
    assert touching["interiors_disjoint"] is True
    assert touching["strictly_separated"] is False


def test_core_clearances_and_segment_memberships_are_positive_and_explicit() -> None:
    checks = _checks(audit.audit_family(audit.reference_family()))
    core = checks["core_membership"]
    assert core["minimum_core_clearance"] == "166045951/3477260000"
    rows = cast("list[dict[str, object]]", core["marks"])
    assert {tuple(cast("list[str]", row["local_coordinates"])) for row in rows} == {
        ("212556/4346575", "1963348/4346575")
    }
    assert all(row["strictly_inside_core"] is True for row in rows)
    assert {tuple(cast("list[str]", row["point"])) for row in rows} == {
        ("3152/3175", "2336/3175"),
        ("3152/3175", "9856/3175"),
    }
    segment = checks["segment_membership"]
    assert segment["segment"] == [["49/100", "48/25"], ["59/100", "48/25"]]
    owners = cast("list[dict[str, object]]", segment["owners"])
    assert [row["square"] for row in owners] == ["A-minus", "A-plus"]
    assert all(row["whole_segment_in_closed_square"] is True for row in owners)


def test_three_controls_have_their_independent_expected_outcomes() -> None:
    overlap = audit.audit_family(audit.control_family("overlap"))
    overlap_checks = _checks(overlap)
    assert overlap_checks["pair_interior_disjointness"]["holds"] is False
    assert all(
        overlap_checks[name]["holds"] is True
        for name in ("container_containment", "core_membership", "segment_membership")
    )
    assert overlap["claim_refuted"] is False

    broken = audit.audit_family(audit.control_family("broken-mark"))
    broken_checks = _checks(broken)
    assert broken_checks["core_membership"]["holds"] is False
    assert all(
        broken_checks[name]["holds"] is True
        for name in (
            "container_containment",
            "pair_interior_disjointness",
            "segment_membership",
        )
    )
    assert broken["claim_refuted"] is False

    changed = audit.audit_family(audit.control_family("changed-target"))
    assert changed["geometry_holds"] is True
    assert changed["target_identity"]["fixed_q_and_core"] is False
    assert changed["claim_refuted"] is False


def test_invalid_geometry_raises_explicit_errors() -> None:
    family = audit.reference_family()
    first = family.squares[0]
    malformed = replace(first, vertices=(*first.vertices[:3], (Fraction(2), Fraction(2))))
    invalid = (
        replace(family, geometry="diamonds"),
        replace(family, q=Fraction(0)),
        replace(family, core_side=Fraction(0)),
        replace(family, squares=(malformed, *family.squares[1:])),
        replace(family, core_marks=()),
        replace(family, segment=replace(family.segment, owners=("missing", "A-plus"))),
    )
    for candidate in invalid:
        with pytest.raises(audit.GuardError):
            audit.audit_geometry(candidate)


def test_cli_emits_json_and_controls_return_success_only_when_the_guard_fires() -> None:
    module_root = Path(audit.__file__).resolve().parents[1]
    environment = os.environ.copy()
    environment["PYTHONPATH"] = os.pathsep.join(
        (str(module_root), environment.get("PYTHONPATH", ""))
    )
    command = [sys.executable, "-m", "devtools.outer_pair_corner_audit"]
    positive = subprocess.run(
        command, check=False, capture_output=True, text=True, env=environment
    )
    assert positive.returncode == 0
    assert json.loads(positive.stdout)["valid_target_counterexample"] is True
    for control in audit.CONTROL_NAMES:
        completed = subprocess.run(
            [*command, "--control", control],
            check=False,
            capture_output=True,
            text=True,
            env=environment,
        )
        assert completed.returncode == 0
        control_record = json.loads(completed.stdout)
        assert control_record["control_expectation_met"] is True
        assert control_record["status"] == "control_passed"
    unexpected = subprocess.run(
        [*command, "--control", "unknown"],
        check=False,
        capture_output=True,
        text=True,
        env=environment,
    )
    assert unexpected.returncode != 0
    assert "invalid choice" in unexpected.stderr
