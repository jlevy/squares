"""Read frozen H-277 numerical evidence; this is not an exact LP proof verifier.

The reader checks receipt accounting, recorded residuals and registered numerical
criteria independently of the probe's aggregate fields. It does not certify row
geometry, root rounding, numerical infeasibility or a physical packing.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_write_text

from sqpack import retained_json
from sqpack.yamlio import load_yaml

LABELS = tuple(label for label in range(1, 18) if label != 6)
TOLERANCE = 1e-8
MARGIN = 1e-6
ROOT_PATH = (
    Path(__file__).resolve().parents[2]
    / "packing/campaign/series/series-000-smoke-and-calibration/results/"
    "exp-237-n17-polynomial-root/run-001/certificate.json"
)
SCHEMA = "n17-widened-lp-reading/v1"
PROBE_SCHEMA = "n17-widened-finite-angle-lp/v1"
RESIDUALS = (
    "primal_violation",
    "dual_sign_violation",
    "stationarity_residual",
    "complementarity_residual",
)
CONTROL_NAMES = {
    "controls": {
        "finite_support",
        "quarter_turn_support",
        "primal_dual_sign",
        "negative_dual_refused",
    },
    "endpoint_controls": {
        "endpoint_reproduced",
        "nominal_centroid_rows",
        "all_raw_branches_accounted",
        "relaxed_slider_monotonicity",
        "fully_relaxed_monotonicity",
        "omission_refuses_complete_point",
        "domain_roster",
    },
    "geometry_controls": {
        "family_slider_recovery",
        "all_29_family_transverse_errors_zero",
        "all_eight_slider_vertices_inside_domain",
        "all_32_signed_turns_label_mapping",
        "label16_positive_turn_decreases_beta",
        "pair_reversal_and_normal_negation_invariant",
    },
}


class RefusedError(ValueError):
    """Receipt or registration contradicts the declared interpretation contract."""


def require(condition: object, message: str) -> None:
    if not condition:
        raise RefusedError(message)


def finite(value: Any, name: str) -> float:
    require(type(value) in (int, float) and math.isfinite(value), f"nonfinite {name}")
    return float(value)


def expected_ids() -> tuple[set[str], set[str]]:
    targets = {
        f"target:outer:coordinate:{label}:{sign}" for label in LABELS for sign in (-1, 1)
    }
    targets |= {
        f"target:{scale}:{name}:{sign}"
        for scale in ("outer", "inner")
        for name in ("Fsplit", "Fcommon", "Bsplit", "Bcommon")
        for sign in (-1, 1)
    }
    matched = {
        f"control:drop_sliders:target:outer:{name}:{sign}"
        for name in ("Fsplit", "coordinate:11", "coordinate:14", "coordinate:16")
        for sign in (-1, 1)
    }
    return targets, matched


def frozen_points(
    registration: dict[str, Any], roster: dict[str, Any]
) -> dict[str, dict[str, Any]]:
    experiment = registration["experiment"]
    require(
        experiment["id"] == "exp-260" and experiment["hypotheses"] == ["H-277"],
        "wrong registration",
    )
    require(experiment["tier"] == "exploratory", "registration promotes exploratory evidence")
    require(experiment["subject"]["method"] == "numerical-f64", "wrong numerical method")
    require(
        roster["hypothesis"] == "H-277" and roster["labels"] == list(LABELS),
        "wrong roster labels",
    )
    require(Fraction(roster["rho_position"]) == Fraction(1, 100), "position radius drift")
    points = {point["id"]: point for point in roster["points"]}
    targets, matched = expected_ids()
    require(
        len(points) == len(roster["points"]) == 56 and set(points) == targets | matched,
        "frozen 48-target/8-control IDs drifted",
    )
    for name, point in points.items():
        q = point["q"]
        require(
            len(q) == 16 and all(type(value) is str for value in q), "invalid rational q vector"
        )
        turns = tuple(Fraction(value) for value in q)
        direction = point["direction"]
        require(
            len(direction) == 16
            and all(type(value) is int for value in direction)
            and any(direction),
            "invalid direction vector",
        )
        radius = Fraction(point["radius"])
        require(
            radius == (Fraction(1, 2000) if ":inner:" in name else Fraction(1, 200)),
            "radius drift",
        )
        scale = max(map(abs, direction))
        require(
            turns == tuple(radius * value / scale for value in direction),
            "q/direction mismatch",
        )
        require(
            point["role"] == ("target" if name in targets else "matched_control"),
            "point role drift",
        )
        require(
            point["profile"] == ("bounded_tube" if name in targets else "drop_sliders"),
            "profile drift",
        )
        if name in matched:
            target = point["matched_target_id"]
            require(
                target in targets and name == f"control:drop_sliders:{target}",
                "matched target drift",
            )
            require(
                turns == tuple(Fraction(value) for value in points[target]["q"]),
                "matched q drift",
            )
    return points


def point_reading(
    receipt: dict[str, Any], source: dict[str, Any], nominal: float
) -> dict[str, Any]:
    require(receipt["profile"] == source["profile"], "receipt profile drift")
    turns = tuple(Fraction(value) for value in source["q"])
    require(
        tuple(Fraction(value) for value in receipt["half_angle_turns"]) == turns,
        "receipt q drift",
    )
    require(receipt["bound_coverage_certified"] is False, "certified-bound promotion")
    require(
        abs(finite(receipt["rho_position"], "position radius") - 0.01) < 1e-15,
        "receipt radius drift",
    )
    branches, outcomes = receipt["branches"], receipt["outcomes"]
    ids = [branch["branch_id"] for branch in branches]
    require(
        all(type(value) is int and 0 <= value < 256 for value in ids)
        and len(set(ids)) == len(ids),
        "duplicate or invalid raw branch ID",
    )
    accounting_complete = set(ids) == set(range(256)) and receipt["raw_branches"] == 256
    statuses = Counter(branch["status"] for branch in branches)
    primal, dual = [], []
    used: set[int] = set()
    for branch in branches:
        index = branch["outcome_index"]
        if index is None:
            require(branch["status"].startswith("omitted_"), "unbound solver branch")
            continue
        require(
            type(index) is int and 0 <= index < len(outcomes), "invalid branch outcome index"
        )
        outcome = outcomes[index]
        require(outcome["status"] == branch["status"], "branch/outcome status disagreement")
        if index in used:
            continue
        used.add(index)
        if outcome["status"] != "numerically_optimal":
            continue
        diagnostics = outcome["diagnostics"]
        require(
            all(0 <= finite(diagnostics[key], key) <= TOLERANCE for key in RESIDUALS),
            "invalid recorded residual",
        )
        require(
            abs(finite(diagnostics["duality_gap"], "duality gap")) <= TOLERANCE,
            "invalid primal/dual gap",
        )
        p, d = (
            finite(diagnostics["primal_value"], "primal optimum"),
            finite(diagnostics["dual_candidate_value"], "dual candidate"),
        )
        require(
            abs(p - d - diagnostics["duality_gap"]) <= TOLERANCE, "objective/gap disagreement"
        )
        require(
            len(outcome["point"]) == 33
            and abs(finite(outcome["point"][-1], "side coordinate") - p) <= TOLERANCE,
            "primal coordinate/objective disagreement",
        )
        require(
            all(
                math.isfinite(finite(value, "primal coordinate")) for value in outcome["point"]
            ),
            "invalid primal vector",
        )
        row_count = 147 if source["profile"] == "bounded_tube" else 141
        require(
            len(outcome["row_ids"]) == len(outcome["multipliers"]) == row_count
            and len(set(outcome["row_ids"])) == row_count,
            "row/multiplier identities missing",
        )
        require(
            all(
                finite(value, "dual multiplier") >= -TOLERANCE
                for value in outcome["multipliers"]
            ),
            "negative multiplier",
        )
        primal.append(p)
        dual.append(d)
    complete = accounting_complete and all(
        status in {"numerically_optimal", "numerically_infeasible"} for status in statuses
    )
    p_min, d_min = min(primal, default=None), min(dual, default=None)
    radius = 2 * math.atan(float(max(map(abs, turns))))
    gap = None if p_min is None else p_min - nominal
    return {
        "id": source["id"],
        "profile": source["profile"],
        "complete": complete,
        "accounting_complete": accounting_complete,
        "branch_status_counts": dict(statuses),
        "finite_optima": len(primal),
        "observed_primal_minimum": p_min,
        "observed_dual_candidate_minimum": d_min,
        "primal_gap": gap,
        "dual_candidate_gap": None if d_min is None else d_min - nominal,
        "angular_infinity_radius": radius,
        "linear_gap_slope": None if gap is None or radius == 0 else gap / radius,
        "quadratic_gap_ratio": None if gap is None or radius == 0 else gap / (radius * radius),
        "ratio_definitions": {"linear": "(S_LP-S0)/r_a", "quadratic": "(S_LP-S0)/r_a^2"},
    }


def interpret(
    registration: dict[str, Any], roster: dict[str, Any], run: dict[str, Any]
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "schema": SCHEMA,
        "bound_coverage_certified": False,
        "assurance": (
            "recorded f64 residual/accounting review; "
            "no exact certificate or physical counterexample"
        ),
        "hypothesis": "H-277",
        "experiment": "exp-260",
    }
    try:
        expected = frozen_points(registration, roster)
        require(
            run["status"]
            in {"complete_numerical", "inconclusive", "in_progress", "controls_passed"},
            "probe failed controls or has unknown run status",
        )
        require(
            run.get("bound_coverage_certified", False) is False,
            "top-level certified-bound promotion",
        )
        require(
            run["schema"] == PROBE_SCHEMA and run["retained_labels"] == list(LABELS),
            "wrong probe schema/labels",
        )
        require(run["rho_position_exact"] == "1/100", "run position radius drift")
        settings = run["solver_settings"]
        require(
            settings["method"] == "highs"
            and settings["tolerance"] == TOLERANCE
            and settings["branch_limit"] == 256
            and settings["per_point_wall_seconds"] == 15
            and settings["per_branch_solver_seconds"] == 1
            and settings["total_wall_seconds"] == 540,
            "registered settings drift",
        )
        control_settings = run["endpoint_controls"]["settings"]
        require(
            control_settings["per_point_wall_seconds"] == 15
            and control_settings["per_branch_solver_seconds"] == 1
            and control_settings["baseline_branch_limit"] == 256
            and control_settings["omission_control_branch_limit"] == 1,
            "control settings differ from registration",
        )
        for section, names in CONTROL_NAMES.items():
            container = run[section]
            checks = container if section == "controls" else container["checks"]
            require(
                names <= checks.keys() and all(checks[name] is True for name in names),
                f"{section} failed or missing",
            )
            if section != "controls":
                require(container["passed"] is True, f"{section} refused")
        require(
            0
            <= finite(
                run["endpoint_controls"]["nominal_centroid_max_violation"],
                "nominal centroid residual",
            )
            <= TOLERANCE,
            "nominal centroid residual failed",
        )
        nominal = finite(run["nominal_side"], "nominal side")
        root = json.loads(ROOT_PATH.read_text())
        t, beta = map(Fraction, root["box"]["midpoint"])
        require(
            run["nominal_root_midpoint"]
            == {"t": str(t), "beta": str(beta), "root_box_radius": root["box"]["radius"]},
            "accepted midpoint representation drift",
        )
        require(
            abs(nominal - float((6 + 4 * t) / (1 + 2 * t - t * t))) <= 1e-14,
            "nominal side disagrees with frozen root",
        )
        aliases = run.get("point_aliases", [])
        names = [alias["id"] for alias in aliases]
        require(
            len(set(names)) == len(names) and set(names) <= expected.keys(),
            "duplicate/unregistered alias",
        )
        readings = {}
        for alias in aliases:
            source = expected[alias["id"]]
            require(alias["input"] == source, "frozen point input drift")
            index = alias["outcome_index"]
            require(
                type(index) is int and 0 <= index < len(run["points"]),
                "invalid point alias index",
            )
            readings[source["id"]] = point_reading(run["points"][index], source, nominal)
        missing = sorted(set(expected) - set(readings))
        require(
            set(run.get("unstarted_point_ids", [])) <= set(missing),
            "unstarted accounting contradicts evaluated aliases",
        )
        targets = [readings[name] for name in readings if expected[name]["role"] == "target"]
        candidate = any(
            point["primal_gap"] is not None and point["primal_gap"] < -MARGIN
            for point in targets
        )
        matched = []
        for name, relaxed in readings.items():
            source = expected[name]
            if (
                source["role"] != "matched_control"
                or source["matched_target_id"] not in readings
            ):
                continue
            bounded = readings[source["matched_target_id"]]
            passed = None
            if (
                relaxed["complete"]
                and bounded["complete"]
                and relaxed["finite_optima"]
                and bounded["finite_optima"]
            ):
                passed = (
                    relaxed["observed_primal_minimum"]
                    <= bounded["observed_primal_minimum"] + TOLERANCE
                )
                require(passed, "matched relaxation monotonicity failed")
            matched.append(
                {"control": name, "target": source["matched_target_id"], "passed": passed}
            )
        unfinished = bool(missing) or any(not point["complete"] for point in readings.values())
        positive = (
            not unfinished
            and len(targets) == 48
            and len(matched) == 8
            and all(item["passed"] is True for item in matched)
        )
        positive &= all(
            point["finite_optima"]
            and point["primal_gap"] > MARGIN
            and point["dual_candidate_gap"] > MARGIN
            for point in targets
        )
        status = (
            "incomplete"
            if unfinished
            else "relaxation_counterexample_candidate"
            if candidate
            else "positive_numerical_evidence"
            if positive
            else "inconclusive"
        )
        result.update(
            status=status,
            missing_point_ids=missing,
            points=list(readings.values()),
            matched_controls=matched,
            execution_complete=not unfinished,
            positive_margin=MARGIN,
            numerical_tolerance=TOLERANCE,
            negative_branch_candidate=candidate,
            counterexample_threshold=(
                "finite bounded_tube primal gap < -1e-6; conditional relaxation only"
            ),
        )
    except (
        KeyError,
        TypeError,
        ValueError,
        IndexError,
        OverflowError,
        ZeroDivisionError,
        OSError,
    ) as error:
        result.update(status="refused", reason=str(error))
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registration", type=Path, required=True)
    parser.add_argument("--points", type=Path, required=True)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    text = args.registration.read_text()
    registration = load_yaml(text.split("---", 2)[1])
    result = interpret(
        registration, json.loads(args.points.read_text()), json.loads(args.run.read_text())
    )
    atomic_write_text(
        args.output, retained_json.dumps(result, allow_nan=False), make_parents=True
    )
    print(json.dumps({"status": result["status"], "output": str(args.output)}))
    return 1 if result["status"] == "refused" else 0


if __name__ == "__main__":
    raise SystemExit(main())
