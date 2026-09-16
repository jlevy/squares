"""The Python adapter reaches the TypeScript contract's verdict on every shared boundary."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import cast

import pytest

from workbench_tools.packing_contracts import (
    CATALOGUE_PRECISION_TOLERANCE,
    CONTRACT_CLAUSES,
    DEFAULT_VALIDITY_TOLERANCE,
    VALIDITY_CONTRACT,
    GeometryIssue,
    PackingContractError,
    check_unit_square_packing,
)

FIXTURE = Path(__file__).parent / "fixtures/packing-validity.json"
SPELLED = {"NaN": math.nan, "Infinity": math.inf, "-Infinity": -math.inf}
TOLERANCES = {
    "contract": DEFAULT_VALIDITY_TOLERANCE,
    "catalogue-precision": CATALOGUE_PRECISION_TOLERANCE,
}


def _number(value: object) -> float:
    if isinstance(value, str):
        return SPELLED[value]
    assert isinstance(value, (int, float))
    assert not isinstance(value, bool)
    return float(value)


def _fixture() -> dict[str, object]:
    loaded: object = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return cast(dict[str, object], loaded)


def _cases() -> list[dict[str, object]]:
    cases = _fixture()["cases"]
    assert isinstance(cases, list)
    return cast(list[dict[str, object]], cases)


def test_fixture_names_the_same_contract_and_declared_tolerances() -> None:
    fixture = _fixture()
    assert fixture["contract"] == VALIDITY_CONTRACT
    assert fixture["tolerances"] == TOLERANCES
    exercised = {case["clause"] for case in _cases()}
    assert set(CONTRACT_CLAUSES) <= exercised


@pytest.mark.parametrize("case", _cases(), ids=lambda case: str(case["id"]))
def test_boundary_case_matches_the_typescript_contract(case: dict[str, object]) -> None:
    snapshot = cast(dict[str, object], case["snapshot"])
    container = cast(dict[str, object], snapshot["container"])
    poses = [
        (_number(pose["x"]), _number(pose["y"]), _number(pose["angle"]))
        for pose in cast(list[dict[str, object]], snapshot["poses"])
    ]
    tolerance = TOLERANCES[cast(str, case["tolerance"])]
    check = check_unit_square_packing(
        poses,
        side=_number(container["side"]),
        expected_count=cast(int, case["expectedCount"]),
        tolerance=tolerance,
        origin=(_number(container["originX"]), _number(container["originY"])),
        square_side=_number(snapshot["squareSide"]),
    )
    assert (check.passed, check.geometry_valid, check.reason) == (
        case["valid"],
        case["geometryValid"],
        case["reason"],
    )
    assert check.tolerance == tolerance


def test_an_undeclared_tolerance_is_a_contract_error() -> None:
    with pytest.raises(PackingContractError, match="declared"):
        check_unit_square_packing([(0.5, 0.5, 0.0)], side=1.0, expected_count=1, tolerance=1e-5)


def test_the_first_issue_is_the_reason_the_contract_reports() -> None:
    overlapping_and_outside = [(0.4, 0.5, 0.0), (0.4, 0.5, 0.0)]
    check = check_unit_square_packing(overlapping_and_outside, side=2.0, expected_count=2)
    assert check.issues == (
        GeometryIssue.PAIR_OVERLAP,
        GeometryIssue.WALL_ESCAPE,
        GeometryIssue.AREA_BOUND,
    )
    assert check.reason == "pair-overlap"
    assert check.max_pair_overlap == pytest.approx(1.0)
