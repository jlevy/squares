"""Synthetic receipt controls; no scientific point is solved or selected here."""

from __future__ import annotations

import copy
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest
import yaml

from devtools import read_n17_widened_lp as reader

REPO = Path(__file__).resolve().parents[2]
REGISTRATION = (
    REPO
    / "packing/campaign/series/series-000-smoke-and-calibration/experiments"
    / "exp-260-h277-widened-lp-reconnaissance.md"
)
ROSTER = (
    REPO
    / "packing/campaign/series/series-000-smoke-and-calibration/results"
    / "exp-260-widened-lp-reconnaissance/points.json"
)


@pytest.fixture
def packet() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    registration = yaml.safe_load(REGISTRATION.read_text().split("---", 2)[1])
    roster = json.loads(ROSTER.read_text())
    root = json.loads(reader.ROOT_PATH.read_text())
    t, beta = map(Fraction, root["box"]["midpoint"])
    nominal = float((6 + 4 * t) / (1 + 2 * t - t * t))
    run: dict[str, Any] = {
        "status": "complete_numerical",
        "schema": reader.PROBE_SCHEMA,
        "retained_labels": list(reader.LABELS),
        "rho_position_exact": "1/100",
        "nominal_side": nominal,
        "nominal_root_midpoint": {
            "t": str(t),
            "beta": str(beta),
            "root_box_radius": root["box"]["radius"],
        },
        "solver_settings": {
            "method": "highs",
            "tolerance": 1e-8,
            "branch_limit": 256,
            "per_point_wall_seconds": 15,
            "per_branch_solver_seconds": 1,
            "total_wall_seconds": 540,
        },
        "points": [],
        "point_aliases": [],
        "unstarted_point_ids": [],
    }
    for section, names in reader.CONTROL_NAMES.items():
        checks = dict.fromkeys(names, True)
        run[section] = checks if section == "controls" else {"checks": checks, "passed": True}
    run["endpoint_controls"].update(
        {
            "nominal_centroid_max_violation": 1e-15,
            "settings": {
                "per_point_wall_seconds": 15,
                "per_branch_solver_seconds": 1,
                "baseline_branch_limit": 256,
                "omission_control_branch_limit": 1,
            },
        }
    )
    for index, point in enumerate(roster["points"]):
        value = nominal + 2e-6
        rows = 147 if point["profile"] == "bounded_tube" else 141
        outcome = {
            "status": "numerically_optimal",
            "diagnostics": {
                **dict.fromkeys(reader.RESIDUALS, 0.0),
                "duality_gap": 0.0,
                "primal_value": value,
                "dual_candidate_value": value,
            },
            "point": [0.0] * 32 + [value],
            "row_ids": [f"synthetic:{i}" for i in range(rows)],
            "multipliers": [1.0] + [0.0] * (rows - 1),
        }
        run["points"].append(
            {
                "profile": point["profile"],
                "half_angle_turns": point["q"],
                "rho_position": 0.01,
                "bound_coverage_certified": False,
                "raw_branches": 256,
                "branches": [
                    {"branch_id": i, "outcome_index": 0, "status": "numerically_optimal"}
                    for i in range(256)
                ],
                "outcomes": [outcome],
                # Deliberately false aggregate fields: the reader must derive its own.
                "heuristic_point_minimum": -1000.0,
                "execution_complete": False,
            }
        )
        run["point_aliases"].append(
            {"id": point["id"], "outcome_index": index, "input": copy.deepcopy(point)}
        )
    return registration, roster, run


def test_positive_rederived_and_radius_ratio_units(
    packet: tuple[dict[str, Any], dict[str, Any], dict[str, Any]],
) -> None:
    result = reader.interpret(*packet)
    assert result["status"] == "positive_numerical_evidence"
    assert not result["bound_coverage_certified"]
    point = result["points"][0]
    assert 0.00999 < point["angular_infinity_radius"] < 0.01001
    assert (
        abs(point["linear_gap_slope"] * point["angular_infinity_radius"] - point["primal_gap"])
        < 1e-15
    )
    assert (
        abs(
            point["quadratic_gap_ratio"] * point["angular_infinity_radius"] ** 2
            - point["primal_gap"]
        )
        < 1e-15
    )


def test_omitted_branch_preserves_ancillary_negative_without_positive(
    packet: tuple[dict[str, Any], dict[str, Any], dict[str, Any]],
) -> None:
    registration, roster, run = packet
    point = run["points"][0]
    value = run["nominal_side"] - 2e-6
    outcome = point["outcomes"][0]
    outcome["diagnostics"].update(primal_value=value, dual_candidate_value=value)
    outcome["point"][-1] = value
    point["branches"][-1].update(status="omitted_by_wall_limit", outcome_index=None)
    # Preserve monotonicity for its matched control.
    matched = run["points"][1]["outcomes"][0]
    matched["diagnostics"].update(primal_value=value, dual_candidate_value=value)
    matched["point"][-1] = value
    result = reader.interpret(registration, roster, run)
    assert result["status"] == "incomplete"
    assert result["negative_branch_candidate"]
    assert result["points"][0]["observed_primal_minimum"] == value


def test_unstarted_roster_is_incomplete(
    packet: tuple[dict[str, Any], dict[str, Any], dict[str, Any]],
) -> None:
    registration, roster, run = packet
    omitted = run["point_aliases"].pop()
    run["unstarted_point_ids"] = [omitted["id"]]
    result = reader.interpret(registration, roster, run)
    assert result["status"] == "incomplete"
    assert result["missing_point_ids"] == [omitted["id"]]


@pytest.mark.parametrize(
    "mutation", ["promotion", "residual", "control", "q", "duplicate", "monotonicity"]
)
def test_contract_violations_refused(
    packet: tuple[dict[str, Any], dict[str, Any], dict[str, Any]], mutation: str
) -> None:
    registration, roster, run = packet
    if mutation == "promotion":
        run["points"][0]["bound_coverage_certified"] = True
    elif mutation == "residual":
        run["points"][0]["outcomes"][0]["diagnostics"]["stationarity_residual"] = 1e-6
    elif mutation == "control":
        run["controls"]["primal_dual_sign"] = False
    elif mutation == "q":
        run["points"][0]["half_angle_turns"] = ["0"] * 16
    elif mutation == "duplicate":
        run["points"][0]["branches"][-1]["branch_id"] = 0
    else:
        outcome = run["points"][1]["outcomes"][0]
        value = run["nominal_side"] + 3e-6
        outcome["diagnostics"].update(primal_value=value, dual_candidate_value=value)
        outcome["point"][-1] = value
    assert reader.interpret(registration, roster, run)["status"] == "refused"


def test_numeric_infeasible_does_not_become_exact_infinity(
    packet: tuple[dict[str, Any], dict[str, Any], dict[str, Any]],
) -> None:
    registration, roster, run = packet
    point = run["points"][0]
    point["outcomes"] = [{"status": "numerically_infeasible"}]
    for branch in point["branches"]:
        branch["status"] = "numerically_infeasible"
    result = reader.interpret(registration, roster, run)
    assert result["status"] == "inconclusive"
    assert result["points"][0]["observed_primal_minimum"] is None
    assert result["points"][0]["branch_status_counts"] == {"numerically_infeasible": 256}


def test_complete_negative_batch_and_small_gap_distinguished(
    packet: tuple[dict[str, Any], dict[str, Any], dict[str, Any]],
) -> None:
    registration, roster, run = packet
    for delta, expected in (
        (-2e-6, "relaxation_counterexample_candidate"),
        (-2e-8, "inconclusive"),
    ):
        for index in (0, 1):
            outcome = run["points"][index]["outcomes"][0]
            value = run["nominal_side"] + delta
            outcome["diagnostics"].update(primal_value=value, dual_candidate_value=value)
            outcome["point"][-1] = value
        assert reader.interpret(registration, roster, run)["status"] == expected


@pytest.mark.parametrize(
    "status", ["solver_limit", "solver_failure", "numerically_unbounded", "residual_failure"]
)
def test_nonadmissible_numeric_status_remains_incomplete(
    packet: tuple[dict[str, Any], dict[str, Any], dict[str, Any]], status: str
) -> None:
    registration, roster, run = packet
    point = run["points"][0]
    point["outcomes"] = [{"status": status}]
    for branch in point["branches"]:
        branch["status"] = status
    result = reader.interpret(registration, roster, run)
    assert result["status"] == "incomplete"
    assert result["points"][0]["observed_primal_minimum"] is None


def test_mixed_numeric_infeasibility_keeps_only_heuristic_evidence(
    packet: tuple[dict[str, Any], dict[str, Any], dict[str, Any]],
) -> None:
    registration, roster, run = packet
    point = run["points"][0]
    point["outcomes"].append({"status": "numerically_infeasible"})
    point["branches"][0].update(outcome_index=1, status="numerically_infeasible")
    result = reader.interpret(registration, roster, run)
    assert result["status"] == "positive_numerical_evidence"
    assert result["points"][0]["branch_status_counts"]["numerically_infeasible"] == 1
    assert not result["bound_coverage_certified"]


def test_positive_requires_dual_candidate_margin_independently(
    packet: tuple[dict[str, Any], dict[str, Any], dict[str, Any]],
) -> None:
    registration, roster, run = packet
    outcome = run["points"][0]["outcomes"][0]
    p, d = run["nominal_side"] + 1.001e-6, run["nominal_side"] + 0.999e-6
    outcome["point"][-1] = p
    outcome["diagnostics"].update(primal_value=p, dual_candidate_value=d, duality_gap=p - d)
    # The matched control stays below the changed bounded optimum.
    control = run["points"][1]["outcomes"][0]
    control["point"][-1] = d
    control["diagnostics"].update(primal_value=d, dual_candidate_value=d)
    result = reader.interpret(registration, roster, run)
    assert result["status"] == "inconclusive"
