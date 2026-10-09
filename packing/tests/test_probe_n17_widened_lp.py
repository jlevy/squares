"""Independent geometry and dual-sign controls for finite-angle reconnaissance."""

from __future__ import annotations

import json
import math
from dataclasses import replace
from fractions import Fraction
from itertools import product
from pathlib import Path
from typing import Any

import pytest

from devtools import probe_n17_widened_lp as probe


def test_finite_support_matches_independent_rotated_corners() -> None:
    angle, direction = 0.37, 0.61
    normal = (math.cos(direction), math.sin(direction))
    values = []
    for x, y in ((-0.5, -0.5), (-0.5, 0.5), (0.5, -0.5), (0.5, 0.5)):
        rotated = (
            x * math.cos(angle) - y * math.sin(angle),
            x * math.sin(angle) + y * math.cos(angle),
        )
        values.append(normal[0] * rotated[0] + normal[1] * rotated[1])
    assert abs(probe.support(angle, normal) - max(values)) < 1e-14
    assert abs(probe.support(angle + math.pi / 2, normal) - max(values)) < 1e-14
    assert probe.support(0.0, (1.0, 0.0)) == 0.5
    assert probe.support(math.pi / 4, (1.0, 0.0)) > 0.7


def test_solver_dual_convention_and_sign_mutation() -> None:
    rows = [probe.Row("lower", (-1.0,), -2.0), probe.Row("upper", (1.0,), 3.0)]
    result = probe.solve_rows(rows, [1.0])
    assert result["status"] == "numerically_optimal"
    assert result["diagnostics"]["primal_value"] == 2.0
    assert result["diagnostics"]["dual_candidate_value"] == 2.0
    flipped = probe.diagnostics(rows, [1.0], [2.0], [-1.0, 0.0])
    assert flipped["dual_sign_violation"] == 1.0
    assert flipped["stationarity_residual"] == 2.0
    altered = probe.diagnostics(rows, [1.0], [2.0], [0.9, 0.0])
    assert altered["stationarity_residual"] > 0.09


def test_infeasible_and_unbounded_remain_numerical_outcomes() -> None:
    infeasible = [probe.Row("lower", (-1.0,), -2.0), probe.Row("upper", (1.0,), 1.0)]
    assert probe.solve_rows(infeasible, [1.0])["status"] == "numerically_infeasible"
    assert (
        probe.solve_rows([probe.Row("upper", (1.0,), 3.0)], [1.0])["status"]
        == "numerically_unbounded"
    )


def test_all_owner_branches_and_independent_signed_sat_row() -> None:
    groups = probe.feature_groups()
    assert len(list(product(*groups))) == 256
    owner_sets = {
        (group[0].left, group[0].right): {item.owner for item in group} for group in groups
    }
    assert (9, 11) not in owner_sets
    assert (2, 3) not in owner_sets
    assert owner_sets[1, 2] == {1, 2}
    assert owner_sets[8, 16] == {16}
    bases = (probe.axes(0.0),) * 17
    feature = probe.Feature(1, 2, 2, 0, 1)
    row = probe.separation_row(feature, bases)
    point = [0.0] * probe.WIDTH
    point[probe.centre_column(2, 0)] = 1.2
    gap = row.upper - sum(a * x for a, x in zip(row.coefficients, point, strict=True))
    assert abs(gap - 0.2) < 1e-14
    reverse = probe.separation_row(replace(feature, sign=-1), bases)
    reverse_gap = reverse.upper - sum(
        a * x for a, x in zip(reverse.coefficients, point, strict=True)
    )
    assert reverse_gap < -2.1


def test_half_angle_turns_and_nested_slider_domains() -> None:
    endpoint = probe.endpoint_at(Fraction(1, 3), Fraction(1, 5))
    turns = [Fraction(0)] * 16
    turns[probe.LABELS.index(9)] = Fraction(1, 100)
    turned = probe.turned_bases(endpoint, turns)
    delta = 2 * math.atan(0.01)
    assert abs(turned[8][0][0] - math.cos(endpoint.angles[8] + delta)) < 1e-14
    assert delta != 0.01
    bounded = probe.domain_rows(endpoint, 0.01, "bounded_tube")
    drop_sliders = probe.domain_rows(endpoint, 0.01, "drop_sliders")
    free_positions = probe.domain_rows(endpoint, 0.01, "free_positions")
    assert len(bounded) == 64
    assert len(drop_sliders) == 58
    assert len(free_positions) == 6
    assert set(bounded) == set(drop_sliders) | set(free_positions)
    assert not probe.domain_rows(endpoint, 0.01, "fully_relaxed")
    point = [coordinate for label in probe.LABELS for coordinate in endpoint.centres[label - 1]]
    point.append(endpoint.side)
    assert (
        min(
            row.upper - sum(a * x for a, x in zip(row.coefficients, point, strict=True))
            for row in bounded
        )
        >= -1e-14
    )
    point[probe.centre_column(5, 0)] -= 0.3
    assert any(
        row.upper - sum(a * x for a, x in zip(row.coefficients, point, strict=True)) < -0.04
        for row in free_positions
    )
    assert all(
        row.upper - sum(a * x for a, x in zip(row.coefficients, point, strict=True)) >= -1e-14
        for row in drop_sliders
    )


def test_endpoint_controls_and_omitted_branch_refusal() -> None:
    controlled = probe.endpoint_controls(probe.load_endpoint(), 0.01)
    assert controlled["passed"]
    bounded = controlled["bounded"]
    assert len(bounded["branches"]) == 256
    assert bounded["unique_lp_solves"] == 1
    assert all(branch["outcome_index"] == 0 for branch in bounded["branches"])
    assert not bounded["bound_coverage_certified"]
    assert not controlled["omitted"]["execution_complete"]
    assert bounded["branches"][0]["features"][0].startswith("pair:1:2:owner:1:")
    assert bounded["branches"][128]["features"][0].startswith("pair:1:2:owner:2:")


def test_reproducible_direction_roster_retains_both_signs() -> None:
    points = probe.coordinate_points(Fraction(1, 1000))
    assert len(points) == 32
    assert len({tuple(point["q"]) for point in points}) == 32
    for label in probe.LABELS:
        pair = [point for point in points if point["id"].startswith(f"coordinate:{label}:")]
        assert len(pair) == 2
        assert all(sum(value != "0" for value in point["q"]) == 1 for point in pair)
    mixed = [0] * 16
    mixed[probe.LABELS.index(9)], mixed[probe.LABELS.index(16)] = 2, -1
    point = probe.direction_point(mixed, Fraction(1, 1000), "mixed")
    assert point["stratum"] == "backbone_mixed"
    assert point["q"][probe.LABELS.index(9)] == "1/1000"
    assert point["q"][probe.LABELS.index(16)] == "-1/2000"


@pytest.mark.parametrize("value", [0.0, -1.0, float("nan"), float("inf")])
def test_invalid_budget_refused_before_solver(value: float) -> None:
    endpoint = probe.endpoint_at(Fraction(1, 3), Fraction(1, 5))
    for name in ("wall_seconds", "solver_seconds"):
        budgets: dict[str, Any] = {name: value}
        with pytest.raises(ValueError, match="finite and positive"):
            probe.evaluate_point(
                endpoint,
                (Fraction(0),) * 16,
                rho_position=0.01,
                profile="bounded_tube",
                **budgets,
            )


def test_solver_timeout_does_not_complete_aliased_point(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def limited(*_args: Any, **_kwargs: Any) -> dict[str, Any]:
        return {"status": "solver_limit"}

    monkeypatch.setattr(probe, "solve_rows", limited)
    endpoint = probe.endpoint_at(Fraction(1, 3), Fraction(1, 5))
    result = probe.evaluate_point(
        endpoint, (Fraction(0),) * 16, rho_position=0.01, profile="bounded_tube"
    )
    assert result["unique_lp_solves"] == 1
    assert all(branch["status"] == "solver_limit" for branch in result["branches"])
    assert not result["execution_complete"]
    assert result["heuristic_point_minimum"] is None


def test_elapsed_budget_retains_partial_witness(monkeypatch: pytest.MonkeyPatch) -> None:
    times = iter((0.0, 0.5))
    monkeypatch.setattr(probe.time, "monotonic", lambda: next(times, 2.0))
    limits: list[float] = []

    def solved(*_args: Any, **kwargs: Any) -> dict[str, Any]:
        limits.append(kwargs["time_limit"])
        return {
            "status": "numerically_optimal",
            "diagnostics": {"primal_value": 2.0, "dual_candidate_value": 2.0},
            "positive_dual_rows": [],
        }

    monkeypatch.setattr(probe, "solve_rows", solved)
    endpoint = probe.endpoint_at(Fraction(1, 3), Fraction(1, 5))
    turns = [Fraction(0)] * 16
    turns[0] = Fraction(1, 100)
    result = probe.evaluate_point(
        endpoint,
        turns,
        rho_position=0.01,
        profile="bounded_tube",
        wall_seconds=1.0,
        solver_seconds=0.8,
    )
    assert limits == [0.5]
    assert any(branch["status"] == "omitted_by_wall_limit" for branch in result["branches"])
    assert result["observed_branch_minimum"] == 2.0
    assert result["heuristic_point_minimum"] is None
    assert not result["execution_complete"]


def test_endpoint_controls_use_declared_budgets(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[dict[str, Any]] = []
    endpoint = probe.load_endpoint()

    def evaluated(*_args: Any, **kwargs: Any) -> dict[str, Any]:
        calls.append(kwargs)
        omitted = kwargs.get("branch_limit") == 1
        return {
            "heuristic_point_minimum": None if omitted else endpoint.side,
            "raw_branches": 256,
            "execution_complete": not omitted,
        }

    monkeypatch.setattr(probe, "evaluate_point", evaluated)
    result = probe.endpoint_controls(endpoint, 0.01, wall_seconds=1.25, solver_seconds=0.75)
    assert result["passed"]
    assert len(calls) == 4
    assert all(call["wall_seconds"] == 1.25 for call in calls)
    assert all(call["solver_seconds"] == 0.75 for call in calls)
    assert result["settings"]["per_point_wall_seconds"] == 1.25


def test_family_and_signed_geometry_controls() -> None:
    controlled = probe.geometry_controls(probe.load_endpoint(), 0.01)
    assert controlled["passed"]
    assert controlled["max_transverse_error"] < 1e-14


def test_expired_global_budget_omits_without_solver(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*_args: Any, **_kwargs: Any) -> dict[str, Any]:
        raise AssertionError("expired global budget must not invoke solver")

    monkeypatch.setattr(probe, "solve_rows", forbidden)
    endpoint = probe.load_endpoint()
    result = probe.evaluate_point(
        endpoint,
        (Fraction(0),) * 16,
        rho_position=0.01,
        profile="bounded_tube",
        global_deadline=0.0,
    )
    assert result["unique_lp_solves"] == 0
    assert result["branch_status_counts"] == {"omitted_by_wall_limit": 256}
    assert not result["execution_complete"]


@pytest.mark.parametrize(
    "status", ["numerically_infeasible", "numerically_unbounded", "residual_failure"]
)
def test_no_finite_optimum_stays_inconclusive(
    monkeypatch: pytest.MonkeyPatch, status: str
) -> None:
    monkeypatch.setattr(probe, "solve_rows", lambda *_args, **_kwargs: {"status": status})
    result = probe.evaluate_point(
        probe.load_endpoint(), (Fraction(0),) * 16, rho_position=0.01, profile="bounded_tube"
    )
    assert result["status"] == "inconclusive"
    assert result["execution_complete"] == (status == "numerically_infeasible")
    assert result["heuristic_point_minimum"] is None
    assert not result["bound_coverage_certified"]


@pytest.mark.parametrize("expire", [False, True])
def test_profile_identity_and_incremental_receipt(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, *, expire: bool
) -> None:
    points = tmp_path / "points.json"
    output = tmp_path / "receipt.json"
    points.write_text(
        json.dumps(
            {
                "points": [
                    {"id": "bounded", "q": ["0"] * 16, "profile": "bounded_tube"},
                    {"id": "relaxed", "q": ["0"] * 16, "profile": "drop_sliders"},
                    {"id": "alias", "q": ["0"] * 16, "profile": "bounded_tube"},
                ]
            }
        )
    )
    monkeypatch.setattr(probe, "synthetic_controls", lambda **_kwargs: {"mocked": True})
    monkeypatch.setattr(probe, "endpoint_controls", lambda *_args, **_kwargs: {"passed": True})
    monkeypatch.setattr(probe, "geometry_controls", lambda *_args: {"passed": True})
    if expire:
        times = iter((0.0, 0.25, 0.5))
        monkeypatch.setattr(probe.time, "monotonic", lambda: next(times, 1000.0))
    calls: list[str] = []

    def evaluated(*_args: Any, **kwargs: Any) -> dict[str, Any]:
        if calls:
            previous = json.loads(output.read_text())
            assert previous["status"] == "in_progress"
            assert len(previous["points"]) == 1
        calls.append(kwargs["profile"])
        assert math.isfinite(kwargs["global_deadline"])
        return {"status": "complete_numerical", "profile": kwargs["profile"]}

    monkeypatch.setattr(probe, "evaluate_point", evaluated)
    exit_code = probe.main(
        ["--points", str(points), "--rho-position", "1/100", "--output", str(output)]
    )
    receipt = json.loads(output.read_text())
    if expire:
        assert exit_code == 1
        assert calls == ["bounded_tube"]
        assert receipt["status"] == "inconclusive"
        assert len(receipt["points"]) == 1
        assert receipt["unstarted_point_ids"] == ["relaxed", "alias"]
        assert receipt["unstarted_point_count"] == 2
    else:
        assert exit_code == 0
        assert calls == ["bounded_tube", "drop_sliders"]
        assert [alias["outcome_index"] for alias in receipt["point_aliases"]] == [0, 1, 0]
        assert receipt["status"] == "complete_numerical"
