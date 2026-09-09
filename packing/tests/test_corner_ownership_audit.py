"""Independent checks for the adjacent-corner ownership audit."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import replace
from fractions import Fraction
from itertools import combinations
from pathlib import Path
from typing import cast

import pytest

from devtools import corner_ownership_audit as audit


def _checks(report: dict[str, object]) -> dict[str, dict[str, object]]:
    return cast("dict[str, dict[str, object]]", report["checks"])


def _independent_sat(left: audit.Diamond, right: audit.Diamond, side: Fraction) -> bool:
    dx, dy = left.center[0] - right.center[0], left.center[1] - right.center[1]
    return any(value * value >= 2 * side * side for value in (dx + dy, dx - dy))


def test_exact_target_refutes_the_named_claim() -> None:
    family = audit.reference_family()
    report = audit.audit_family(family)
    checks = _checks(report)

    assert report["valid_n11_counterexample"] is True
    assert report["claim_refuted"] is True
    assert all(check["holds"] is True for check in checks.values())
    assert checks["unit_containment"]["minimum_margin"] == "71/100"
    assert Fraction(71, 100) ** 2 > Fraction(1, 2)
    distances = {
        Fraction(value) for value in cast("list[str]", checks["core_ownership"]["l1_distances"])
    }
    assert distances == {Fraction(2959, 12700), Fraction(4337, 6350)}
    assert checks["core_ownership"]["all_distances_below_7/10"] is True
    assert checks["core_ownership"]["7/10_inside_core_radius"] is True
    pairs = checks["pair_interior_disjointness"]
    assert pairs["minimum_l1_distance"] == "143/100"
    assert pairs["l1_sat_agree"] is True
    identity = cast("dict[str, bool]", report["target_identity"])
    assert all(identity.values())
    reflection = cast("dict[str, object]", report["horizontal_reflection_extension"])
    assert reflection == {"l1_distance": "27/50", "interiors_disjoint": False}


def test_l1_and_independent_sat_agree_for_source_and_controls() -> None:
    for control in (None, *audit.CONTROL_NAMES):
        family = audit.reference_family() if control is None else audit.control_family(control)
        rows = cast(
            "list[dict[str, object]]",
            _checks(audit.audit_family(family))["pair_interior_disjointness"]["pairs"],
        )
        reported = {
            tuple(cast("list[str]", row["diamonds"])): row["l1_disjoint"] for row in rows
        }
        expected = {
            (left.name, right.name): _independent_sat(left, right, family.diamond_side)
            for left, right in combinations(family.diamonds, 2)
        }
        assert reported == expected


def test_each_control_breaks_only_its_named_geometry_check() -> None:
    expected = {
        "overlap": "pair_interior_disjointness",
        "containment": "unit_containment",
        "core-ownership": "core_ownership",
    }
    for control, failed_name in expected.items():
        report = audit.audit_family(audit.control_family(control))
        checks = _checks(report)
        assert {name for name, check in checks.items() if check["holds"] is False} == {
            failed_name
        }
        assert checks["pair_interior_disjointness"]["l1_sat_agree"] is True
        assert report["valid_n11_counterexample"] is False


def test_valid_generic_geometry_does_not_refute_the_n11_target() -> None:
    family = replace(audit.reference_family(), container_side=Fraction(4))
    geometry = audit.audit_geometry(family)
    report = audit.audit_family(family)

    assert geometry["geometry_holds"] is True
    assert report["target_identity"]["parameters"] is False
    assert report["valid_n11_counterexample"] is False
    assert report["claim_refuted"] is False


def test_guards_and_boundary_semantics() -> None:
    family = audit.reference_family()
    invalid = (
        replace(family, geometry="axis-squares"),
        replace(family, container_side=Fraction(0)),
        replace(family, diamond_side=Fraction(-1)),
        replace(family, core_side=Fraction(0)),
        replace(family, diamonds=(family.diamonds[0], family.diamonds[0])),
        replace(family, marks=(replace(family.marks[0], owner="missing"), *family.marks[1:])),
    )
    for candidate in invalid:
        with pytest.raises(audit.GuardError):
            audit.audit_geometry(candidate)

    assert audit.interiors_disjoint(Fraction(2), Fraction(2))
    assert not audit.strictly_contained(Fraction(1, 2), Fraction(1, 2))
    assert not audit.strictly_owned(Fraction(1, 2), Fraction(1, 2))


def test_cli_json_and_control_exit_contract() -> None:
    module_root = Path(audit.__file__).resolve().parents[1]
    environment = os.environ.copy()
    environment["PYTHONPATH"] = os.pathsep.join(
        (str(module_root), environment.get("PYTHONPATH", ""))
    )
    command = [sys.executable, "-m", "devtools.corner_ownership_audit"]
    positive = subprocess.run(
        command, check=False, capture_output=True, text=True, env=environment
    )
    assert positive.returncode == 0
    assert json.loads(positive.stdout)["valid_n11_counterexample"] is True
    for control in audit.CONTROL_NAMES:
        completed = subprocess.run(
            [*command, "--control", control],
            check=False,
            capture_output=True,
            text=True,
            env=environment,
        )
        assert completed.returncode == 0
        assert json.loads(completed.stdout)["control_expectation_met"] is True
    unexpected = subprocess.run(
        [*command, "--control", "unknown"],
        check=False,
        capture_output=True,
        text=True,
        env=environment,
    )
    assert unexpected.returncode != 0
    assert "invalid choice" in unexpected.stderr
