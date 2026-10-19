"""Finite-angle LP reconnaissance; floating-point diagnostics are not certificates.

Every inequality is recorded as ``A x <= b``. Variables are unrestricted and
domain bounds are explicit rows, so the dual has no hidden bound multipliers.
"""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import argparse
import itertools
import json
import math
import time
from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from scipy.optimize import linprog
from strif import atomic_write_text

from devtools.check_n17_contact_chart import CONTACTS
from devtools.check_n17_endpoint_feasibility import (
    REPO,
    _layout,
)
from devtools.check_n17_endpoint_features import option_manifest
from devtools.provenance import provenance, repository_path
from sqpack import retained_json

type Point = tuple[float, float]
type Basis = tuple[Point, Point]

LABELS = tuple(label for label in range(1, 18) if label != 6)
SIDE_COLUMN = 2 * len(LABELS)
WIDTH = SIDE_COLUMN + 1
ROOT_CERTIFICATE = (
    REPO / "packing/campaign/series/series-000-smoke-and-calibration/results/"
    "exp-237-n17-polynomial-root/run-001/certificate.json"
)
ENDPOINT_AUDIT = (
    REPO / "packing/campaign/series/series-000-smoke-and-calibration/results/"
    "exp-238-n17-endpoint-feasibility/audit/independent-receipt.json"
)
PROFILES = ("bounded_tube", "drop_sliders", "free_positions", "fully_relaxed")
SCHEMA = "n17-widened-finite-angle-lp/v1"


@dataclass(frozen=True)
class Row:
    """One finite-angle inequality, with a stable geometric identity."""

    name: str
    coefficients: tuple[float, ...]
    upper: float


@dataclass(frozen=True)
class Endpoint:
    """Nominal geometry from the accepted root midpoint, not a new exact witness."""

    side: float
    centres: tuple[Point, ...]
    angles: tuple[float, ...]
    bases: tuple[Basis, ...]
    u: Point
    v: Point
    parameters: tuple[Fraction, Fraction]


@dataclass(frozen=True)
class Feature:
    """A pair-order separating option; owners remain distinct before row construction."""

    left: int
    right: int
    owner: int
    axis: int
    sign: int

    @property
    def name(self) -> str:
        return (
            f"pair:{self.left}:{self.right}:owner:{self.owner}:"
            f"axis:{self.axis}:sign:{self.sign}"
        )


def endpoint_at(t: Fraction, beta: Fraction) -> Endpoint:
    """Convert the retained rational endpoint layout to numerical reconnaissance inputs."""
    side, auxiliary, centres = _layout(t, beta, Fraction(1, 2))
    theta_angle = 2 * math.atan(float(t))
    beta_angle = -2 * math.atan(float(beta))
    nominal_bases: list[Basis] = []
    for label in range(1, 18):
        names = ("u", "v") if 9 <= label <= 14 else ("p", "q") if label == 16 else ("ex", "ey")
        first, second = (auxiliary[name] for name in names)
        nominal_bases.append(
            ((float(first[0]), float(first[1])), (float(second[0]), float(second[1])))
        )
    return Endpoint(
        float(side),
        tuple((float(x), float(y)) for x, y in centres),
        tuple(
            theta_angle if 9 <= label <= 14 else beta_angle if label == 16 else 0.0
            for label in range(1, 18)
        ),
        tuple(nominal_bases),
        (float(auxiliary["u"][0]), float(auxiliary["u"][1])),
        (float(auxiliary["v"][0]), float(auxiliary["v"][1])),
        (t, beta),
    )


def load_endpoint(path: Path = ROOT_CERTIFICATE) -> Endpoint:
    """Read the accepted root's midpoint; the existing exact root proof remains a premise."""
    document = json.loads(path.read_text())
    if (
        document.get("schema") != "n17-root-certificate/v1"
        or document.get("criterion_passed") is not True
        or document.get("failures") != []
    ):
        raise ValueError("accepted n17 root certificate required")
    t, beta = (Fraction(value) for value in document["box"]["midpoint"])
    return endpoint_at(t, beta)


def feature_groups() -> tuple[tuple[Feature, ...], ...]:
    """The declared 19-pair subsystem: 11 singleton and 8 double-owner choices."""
    retained = {(min(i, j), max(i, j)) for i, j, _, _ in CONTACTS if (i, j) != (9, 11)}
    by_pair: dict[tuple[int, int], list[Feature]] = {pair: [] for pair in sorted(retained)}
    for option in option_manifest():
        pair = int(option["left"]), int(option["right"])
        if pair not in retained or option["kind"] != "identity":
            continue
        axis = 0 if option["axis"] in {"ex", "u", "p"} else 1
        by_pair[pair].append(Feature(*pair, int(option["owner"]), axis, int(option["sign"])))
    groups = tuple(
        tuple(sorted(group, key=lambda item: item.owner)) for group in by_pair.values()
    )
    if len(groups) != 19 or sorted(map(len, groups)) != [1] * 11 + [2] * 8:
        raise ValueError("declared finite-angle owner roster drifted")
    return groups


def _linear_row(name: str, entries: dict[int, float], upper: float) -> Row:
    return Row(name, tuple(entries.get(column, 0.0) for column in range(WIDTH)), upper)


def centre_column(label: int, coordinate: int) -> int:
    return 2 * LABELS.index(label) + coordinate


def turned_bases(endpoint: Endpoint, turns: Sequence[Fraction]) -> tuple[Basis, ...]:
    """Canonical half-angle turns rotate each owner's nominal basis independently."""
    if len(turns) != len(LABELS) or any(type(turn) is not Fraction for turn in turns):
        raise ValueError("sixteen exact half-angle turns required in retained-label order")
    result = list(endpoint.bases)
    for label, turn in zip(LABELS, turns, strict=True):
        denominator = 1 + turn * turn
        cosine, sine = float((1 - turn * turn) / denominator), float(2 * turn / denominator)
        u, v = endpoint.bases[label - 1]
        result[label - 1] = (
            (cosine * u[0] + sine * v[0], cosine * u[1] + sine * v[1]),
            (-sine * u[0] + cosine * v[0], -sine * u[1] + cosine * v[1]),
        )
    return tuple(result)


def basis_support(basis: Basis, normal: Point) -> float:
    return sum(abs(normal[0] * axis[0] + normal[1] * axis[1]) for axis in basis) / 2


def separation_row(feature: Feature, bases: Sequence[Basis]) -> Row:
    """The actual owner-axis SAT inequality, negated into ``A z <= b``."""
    nx, ny = bases[feature.owner - 1][feature.axis]
    normal = feature.sign * nx, feature.sign * ny
    entries: dict[int, float] = {}
    for coordinate, value in enumerate(normal):
        entries[centre_column(feature.left, coordinate)] = value
        entries[centre_column(feature.right, coordinate)] = -value
    upper = -basis_support(bases[feature.left - 1], normal) - basis_support(
        bases[feature.right - 1], normal
    )
    return _linear_row(feature.name, entries, upper)


def containment_rows(bases: Sequence[Basis]) -> list[Row]:
    """All four finite support constraints for each of the 16 retained squares."""
    rows = []
    for label in LABELS:
        for coordinate, normal in enumerate(((1.0, 0.0), (0.0, 1.0))):
            column = centre_column(label, coordinate)
            extent = basis_support(bases[label - 1], normal)
            rows.extend(
                (
                    _linear_row(f"wall:{label}:{coordinate}:lower", {column: -1.0}, -extent),
                    _linear_row(
                        f"wall:{label}:{coordinate}:upper",
                        {column: 1.0, SIDE_COLUMN: -1.0},
                        -extent,
                    ),
                )
            )
    return rows


def domain_rows(endpoint: Endpoint, rho_position: float, profile: str) -> list[Row]:
    """The packet's 6 slider and 58 transverse/position tube rows, with nested controls."""
    if profile not in PROFILES or not math.isfinite(rho_position) or rho_position <= 0:
        raise ValueError("declared domain profile and positive position radius required")
    rows: list[Row] = []

    def interval(label: int, normal: Point, low: float, high: float, name: str) -> None:
        x, y = endpoint.centres[label - 1]
        origin = normal[0] * x + normal[1] * y
        entries = {
            centre_column(label, coordinate): value for coordinate, value in enumerate(normal)
        }
        rows.append(_linear_row(f"{name}:upper", entries, origin + high))
        rows.append(
            _linear_row(
                f"{name}:lower",
                {column: -value for column, value in entries.items()},
                -origin - low,
            )
        )

    if profile in {"bounded_tube", "free_positions"}:
        interval(5, (-1.0, 0.0), 0.0, 1 / 4, "slider:a")
        interval(11, (-endpoint.v[0], -endpoint.v[1]), -1 / 2500, 1 / 12, "slider:b")
        interval(13, endpoint.v, -1 / 8, 1 / 16, "slider:z")
    if profile in {"bounded_tube", "drop_sliders"}:
        interval(5, (0.0, 1.0), -rho_position, rho_position, "tube:5:y")
        interval(11, endpoint.u, -rho_position, rho_position, "tube:11:u")
        interval(13, endpoint.u, -rho_position, rho_position, "tube:13:u")
        for label in LABELS:
            if label in {5, 11, 13}:
                continue
            interval(label, (1.0, 0.0), -rho_position, rho_position, f"tube:{label}:x")
            interval(label, (0.0, 1.0), -rho_position, rho_position, f"tube:{label}:y")
    return rows


def axes(angle: float) -> tuple[Point, Point]:
    """Actual square axes at the supplied angle, in radians."""
    if not math.isfinite(angle):
        raise ValueError("angle must be finite")
    cosine, sine = math.cos(angle), math.sin(angle)
    return (cosine, sine), (-sine, cosine)


def support(angle: float, normal: Point) -> float:
    """Unit-square support at a finite angle, retaining the absolute-value kinks."""
    first, second = axes(angle)
    return (
        abs(normal[0] * first[0] + normal[1] * first[1])
        + abs(normal[0] * second[0] + normal[1] * second[1])
    ) / 2


def diagnostics(
    rows: Sequence[Row],
    objective: Sequence[float],
    point: Sequence[float],
    multipliers: Sequence[float],
) -> dict[str, float]:
    """Primal and dual residuals in the recorded inequality convention.

    With ``lambda >= 0``, stationarity is ``c + A.T lambda = 0`` and the
    candidate dual value is ``-lambda @ b``. Residuals are diagnostic only;
    no floating tolerance turns them into a sound lower bound.
    """
    if len(point) != len(objective) or len(rows) != len(multipliers):
        raise ValueError("LP diagnostic dimensions differ")
    if any(len(row.coefficients) != len(point) for row in rows):
        raise ValueError("LP row width differs")
    values = (*point, *multipliers, *objective)
    if not all(math.isfinite(value) for value in values):
        raise ValueError("nonfinite LP diagnostic input")
    slacks = [
        row.upper - sum(a * x for a, x in zip(row.coefficients, point, strict=True))
        for row in rows
    ]
    primal = sum(c * x for c, x in zip(objective, point, strict=True))
    dual = -sum(y * row.upper for y, row in zip(multipliers, rows, strict=True))
    stationarity = [
        c + sum(y * row.coefficients[j] for y, row in zip(multipliers, rows, strict=True))
        for j, c in enumerate(objective)
    ]
    return {
        "primal_violation": max((max(0.0, -slack) for slack in slacks), default=0.0),
        "dual_sign_violation": max((max(0.0, -y) for y in multipliers), default=0.0),
        "stationarity_residual": max(map(abs, stationarity), default=0.0),
        "complementarity_residual": max(
            (abs(y * slack) for y, slack in zip(multipliers, slacks, strict=True)),
            default=0.0,
        ),
        "primal_value": primal,
        "dual_candidate_value": dual,
        "duality_gap": primal - dual,
    }


def solve_rows(
    rows: Sequence[Row],
    objective: Sequence[float],
    *,
    tolerance: float = 1e-8,
    time_limit: float = 5.0,
) -> dict[str, Any]:
    """Solve one branch and retain failed/inconclusive numerical outcomes."""
    if not rows or not objective or len({row.name for row in rows}) != len(rows):
        raise ValueError("LP needs nonempty rows/objective and unique row identities")
    if (
        not math.isfinite(tolerance)
        or tolerance <= 0
        or not math.isfinite(time_limit)
        or time_limit <= 0
    ):
        raise ValueError("LP tolerances and time limit must be positive")
    if any(len(row.coefficients) != len(objective) for row in rows):
        raise ValueError("LP row width differs")
    if not all(
        math.isfinite(value)
        for value in (
            *objective,
            *(value for row in rows for value in (*row.coefficients, row.upper)),
        )
    ):
        raise ValueError("LP coefficients must be finite")
    wall_start, cpu_start = time.monotonic(), time.process_time()
    result = linprog(
        list(objective),
        A_ub=[list(row.coefficients) for row in rows],
        b_ub=[row.upper for row in rows],
        bounds=[(None, None)] * len(objective),
        method="highs",
        options={
            "time_limit": time_limit,
            "primal_feasibility_tolerance": tolerance,
            "dual_feasibility_tolerance": tolerance,
        },
    )
    outcome: dict[str, Any] = {
        "status": "numerically_unresolved",
        "solver_status": int(result.status),
        "solver_message": str(result.message),
        "wall_seconds": time.monotonic() - wall_start,
        "cpu_seconds": time.process_time() - cpu_start,
        "row_ids": [row.name for row in rows],
        "assurance": "floating-point reconnaissance; no certified bound or exclusion",
    }
    if result.status != 0:
        outcome["status"] = {
            1: "solver_limit",
            2: "numerically_infeasible",
            3: "numerically_unbounded",
        }.get(int(result.status), "solver_failure")
        return outcome
    point = [float(value) for value in result.x]
    multipliers = [-float(value) for value in result.ineqlin.marginals]
    checks = diagnostics(rows, objective, point, multipliers)
    valid = (
        all(
            checks[name] <= tolerance
            for name in (
                "primal_violation",
                "dual_sign_violation",
                "stationarity_residual",
                "complementarity_residual",
            )
        )
        and abs(checks["duality_gap"]) <= tolerance
    )
    outcome.update(
        {
            "status": "numerically_optimal" if valid else "residual_failure",
            "point": point,
            "multipliers": multipliers,
            "diagnostics": checks,
            "positive_dual_rows": [
                row.name
                for row, weight in zip(rows, multipliers, strict=True)
                if weight > tolerance
            ],
        }
    )
    return outcome


def evaluate_point(
    endpoint: Endpoint,
    turns: Sequence[Fraction],
    *,
    rho_position: float,
    profile: str,
    branch_limit: int = 256,
    wall_seconds: float = 60.0,
    solver_seconds: float = 5.0,
    global_deadline: float | None = None,
) -> dict[str, Any]:
    """Account for every raw branch, retaining aliases only for equal numerical rows.

    The aggregate is exploratory. A numeric infeasibility report is not a Farkas
    certificate, and no omitted branch receives an implicit infinite value.
    """
    if type(branch_limit) is not int or not 1 <= branch_limit <= 256:
        raise ValueError("branch limit must be an integer in 1..256")
    if any(not math.isfinite(value) or value <= 0 for value in (wall_seconds, solver_seconds)):
        raise ValueError("wall and solver ceilings must be finite and positive")
    start = time.monotonic()
    deadline = start + wall_seconds
    if global_deadline is not None:
        if not math.isfinite(global_deadline):
            raise ValueError("global deadline must be finite")
        deadline = min(deadline, global_deadline)
    bases = turned_bases(endpoint, turns)
    common = containment_rows(bases) + domain_rows(endpoint, rho_position, profile)
    objective = [0.0] * WIDTH
    objective[SIDE_COLUMN] = 1.0
    groups = feature_groups()
    solved: dict[tuple[tuple[tuple[float, ...], float], ...], int] = {}
    outcomes: list[dict[str, Any]] = []
    branches: list[dict[str, Any]] = []
    for branch_id, features in enumerate(itertools.product(*groups)):
        rows = common + [separation_row(feature, bases) for feature in features]
        row_key = tuple((row.coefficients, row.upper) for row in rows)
        entry: dict[str, Any] = {
            "branch_id": branch_id,
            "features": [feature.name for feature in features],
            "outcome_index": None,
            "status": "omitted_by_branch_limit",
        }
        if branch_id < branch_limit:
            if row_key in solved:
                index = solved[row_key]
                entry.update(outcome_index=index, status=outcomes[index]["status"])
            else:
                remaining = deadline - time.monotonic()
                if remaining > 0:
                    outcome = solve_rows(
                        rows, objective, time_limit=min(solver_seconds, remaining)
                    )
                    index = len(outcomes)
                    solved[row_key] = index
                    outcomes.append({"representative_branch": branch_id, **outcome})
                    entry.update(outcome_index=index, status=outcome["status"])
                else:
                    entry["status"] = "omitted_by_wall_limit"
        branches.append(entry)
    optimum_indices = [
        index
        for index, outcome in enumerate(outcomes)
        if outcome["status"] == "numerically_optimal"
    ]
    minimizer = min(
        optimum_indices,
        key=lambda index: outcomes[index]["diagnostics"]["primal_value"],
        default=None,
    )
    observed = None if minimizer is None else outcomes[minimizer]["diagnostics"]["primal_value"]
    observed_dual = min(
        (outcomes[index]["diagnostics"]["dual_candidate_value"] for index in optimum_indices),
        default=None,
    )
    angular_radius = max((abs(2 * math.atan(float(turn))) for turn in turns), default=0.0)
    terminal = {"numerically_optimal", "numerically_infeasible"}
    execution_complete = all(branch["status"] in terminal for branch in branches)
    finite_heuristic = execution_complete and all(
        branch["status"] in {"numerically_optimal", "numerically_infeasible"}
        for branch in branches
    )
    return {
        "status": "complete_numerical"
        if finite_heuristic and observed is not None
        else "inconclusive",
        "half_angle_turns": [str(turn) for turn in turns],
        "display_delta_radians": [2 * math.atan(float(turn)) for turn in turns],
        "profile": profile,
        "rho_position": rho_position,
        "raw_branches": len(branches),
        "branch_encoding": {
            "binary_pairs": [
                [group[0].left, group[0].right] for group in groups if len(group) == 2
            ],
            "bit_order": "lexicographic pair order, first pair is most significant bit",
            "owner_bits": "0 selects lower owner label; 1 selects higher owner label",
            "row_alias_assurance": (
                "identical floating rows only; no algebraic equality certificate"
            ),
        },
        "unique_lp_solves": len(outcomes),
        "distinct_positive_dual_signatures": len(
            {
                tuple(outcome["positive_dual_rows"])
                for outcome in outcomes
                if outcome["status"] == "numerically_optimal"
            }
        ),
        "execution_complete": execution_complete,
        "branch_status_counts": {
            status: sum(branch["status"] == status for branch in branches)
            for status in sorted({branch["status"] for branch in branches})
        },
        "bound_coverage_certified": False,
        "observed_branch_minimum": observed,
        "observed_dual_candidate_minimum": observed_dual,
        "heuristic_point_minimum": observed if finite_heuristic else None,
        "heuristic_point_dual_minimum": observed_dual if finite_heuristic else None,
        "nominal_gap": None if observed is None else observed - endpoint.side,
        "angular_infinity_radius": angular_radius,
        "sampled_gap_slope": (
            (observed - endpoint.side) / angular_radius
            if observed is not None and angular_radius > 0
            else None
        ),
        "minimizer_outcome": minimizer,
        "branches": branches,
        "outcomes": outcomes,
        "wall_seconds": time.monotonic() - start,
        "basis_forecast": (
            "unknown; sampled dual-support signatures are not basis or patch coverage"
        ),
        "interpretation": (
            "conditional 19-pair subsystem without square 6; "
            "no physical counterexample or theorem claim"
        ),
    }


def direction_point(direction: Sequence[int], radius: Fraction, name: str) -> dict[str, Any]:
    """Construct a reproducible rational-turn point from a declared integer direction."""
    if (
        len(direction) != len(LABELS)
        or any(type(value) is not int for value in direction)
        or not any(direction)
        or type(radius) is not Fraction
        or radius <= 0
    ):
        raise ValueError(
            "nonzero integer sixteen-direction and positive rational radius required"
        )
    scale = max(map(abs, direction))
    labels = {label for label, value in zip(LABELS, direction, strict=True) if value}
    stratum = (
        "coordinate"
        if len(labels) == 1
        else "backbone_mixed"
        if labels <= {9, 10, 11, 12, 13, 14, 16}
        else "full_mixed"
    )
    return {
        "id": name,
        "q": [str(radius * value / scale) for value in direction],
        "direction": list(direction),
        "radius": str(radius),
        "stratum": stratum,
    }


def coordinate_points(radius: Fraction) -> list[dict[str, Any]]:
    """All 32 signed coordinate directions, without silently choosing target radii."""
    points = []
    for index, label in enumerate(LABELS):
        for sign in (-1, 1):
            direction = [0] * len(LABELS)
            direction[index] = sign
            points.append(direction_point(direction, radius, f"coordinate:{label}:{sign}"))
    return points


def geometry_controls(endpoint: Endpoint, rho_position: float) -> dict[str, Any]:
    """Family vertices and signed-label turns checked independently of LP optima."""
    max_recovery, max_transverse, max_domain_violation = 0.0, 0.0, 0.0
    untouched_labels = True
    tube = domain_rows(endpoint, rho_position, "drop_sliders")
    domain = domain_rows(endpoint, rho_position, "bounded_tube")
    for a, b, z in itertools.product((0.0, 0.25), (-1 / 2500, 1 / 12), (-1 / 8, 1 / 16)):
        point = [value for label in LABELS for value in endpoint.centres[label - 1]]
        point.append(endpoint.side)
        point[centre_column(5, 0)] -= a
        for label, shift in ((11, -b), (13, z)):
            for coordinate in (0, 1):
                point[centre_column(label, coordinate)] += shift * endpoint.v[coordinate]

        def displacement(label: int, normal: Point, point: list[float] = point) -> float:
            return sum(
                normal[c] * (point[centre_column(label, c)] - endpoint.centres[label - 1][c])
                for c in (0, 1)
            )

        recovered = (
            -displacement(5, (1.0, 0.0)),
            -displacement(11, endpoint.v),
            displacement(13, endpoint.v),
        )
        max_recovery = max(
            max_recovery, *(abs(x - y) for x, y in zip(recovered, (a, b, z), strict=True))
        )
        for upper in tube[::2]:
            value = sum(c * x for c, x in zip(upper.coefficients, point, strict=True))
            max_transverse = max(max_transverse, abs(value - (upper.upper - rho_position)))
        max_domain_violation = max(
            max_domain_violation,
            *(
                max(
                    0.0,
                    sum(c * x for c, x in zip(row.coefficients, point, strict=True))
                    - row.upper,
                )
                for row in domain
            ),
        )
    max_turn_error = 0.0
    for label in LABELS:
        for sign in (-1, 1):
            turns = [Fraction(0)] * len(LABELS)
            turns[LABELS.index(label)] = Fraction(sign, 100)
            bases = turned_bases(endpoint, turns)
            expected = axes(endpoint.angles[label - 1] + 2 * math.atan(sign / 100))
            max_turn_error = max(
                max_turn_error,
                *(
                    abs(x - y)
                    for actual, want in zip(bases[label - 1], expected, strict=True)
                    for x, y in zip(actual, want, strict=True)
                ),
            )
            untouched_labels &= all(
                bases[other - 1] == endpoint.bases[other - 1]
                for other in LABELS
                if other != label
            )
    turns = [Fraction(0)] * len(LABELS)
    turns[LABELS.index(16)] = Fraction(1, 100)
    u16 = turned_bases(endpoint, turns)[15][0]
    beta_after = -math.atan2(u16[1], u16[0]) / 2
    feature = feature_groups()[0][0]
    reversed_feature = Feature(
        feature.right, feature.left, feature.owner, feature.axis, -feature.sign
    )
    normal_row = separation_row(feature, endpoint.bases)
    reversed_row = separation_row(reversed_feature, endpoint.bases)
    checks = {
        "family_slider_recovery": max_recovery < 1e-14,
        "all_29_family_transverse_errors_zero": max_transverse < 1e-14,
        "all_eight_slider_vertices_inside_domain": max_domain_violation < 1e-14,
        "all_32_signed_turns_label_mapping": max_turn_error < 1e-14 and untouched_labels,
        "label16_positive_turn_decreases_beta": beta_after
        < math.atan(float(endpoint.parameters[1])),
        "pair_reversal_and_normal_negation_invariant": (
            normal_row.coefficients == reversed_row.coefficients
            and normal_row.upper == reversed_row.upper
        ),
    }
    return {
        "checks": checks,
        "passed": all(checks.values()),
        "max_slider_recovery_error": max_recovery,
        "max_transverse_error": max_transverse,
        "max_vertex_domain_violation": max_domain_violation,
        "max_signed_turn_error": max_turn_error,
    }


def synthetic_controls(*, solver_seconds: float = 5.0) -> dict[str, bool]:
    """Quick controls independent of every n17 target input."""
    rows = [Row("lower", (-1.0,), -2.0), Row("upper", (1.0,), 3.0)]
    solved = solve_rows(rows, [1.0], time_limit=solver_seconds)
    sign_flip = diagnostics(rows, [1.0], [2.0], [-1.0, 0.0])
    angle = 0.37
    normal = axes(0.61)[0]
    corners = [
        (
            x * math.cos(angle) - y * math.sin(angle),
            x * math.sin(angle) + y * math.cos(angle),
        )
        for x, y in itertools.product((-0.5, 0.5), repeat=2)
    ]
    direct = max(normal[0] * x + normal[1] * y for x, y in corners)
    return {
        "finite_support": abs(support(angle, normal) - direct) < 1e-14,
        "quarter_turn_support": abs(support(angle + math.pi / 2, normal) - direct) < 1e-14,
        "primal_dual_sign": solved["status"] == "numerically_optimal"
        and solved["diagnostics"]["dual_candidate_value"] == 2.0,
        "negative_dual_refused": sign_flip["dual_sign_violation"] == 1.0
        and sign_flip["stationarity_residual"] == 2.0,
    }


def endpoint_controls(
    endpoint: Endpoint,
    rho_position: float,
    *,
    wall_seconds: float = 60.0,
    solver_seconds: float = 5.0,
    global_deadline: float | None = None,
) -> dict[str, Any]:
    """Endpoint reproduction, domain relaxation and omission controls before sampling."""
    turns = (Fraction(0),) * len(LABELS)
    budgets: dict[str, Any] = {
        "wall_seconds": wall_seconds,
        "solver_seconds": solver_seconds,
        "global_deadline": global_deadline,
    }
    bounded = evaluate_point(
        endpoint, turns, rho_position=rho_position, profile="bounded_tube", **budgets
    )
    relaxed = evaluate_point(
        endpoint, turns, rho_position=rho_position, profile="drop_sliders", **budgets
    )
    fully_relaxed = evaluate_point(
        endpoint, turns, rho_position=rho_position, profile="fully_relaxed", **budgets
    )
    omitted = evaluate_point(
        endpoint,
        turns,
        rho_position=rho_position,
        profile="bounded_tube",
        branch_limit=1,
        **budgets,
    )
    first, second = bounded["heuristic_point_minimum"], relaxed["heuristic_point_minimum"]
    third = fully_relaxed["heuristic_point_minimum"]
    point = [value for label in LABELS for value in endpoint.centres[label - 1]]
    point.append(endpoint.side)
    nominal_rows = (
        containment_rows(endpoint.bases)
        + domain_rows(endpoint, rho_position, "bounded_tube")
        + [
            separation_row(feature, endpoint.bases)
            for group in feature_groups()
            for feature in group
        ]
    )
    nominal_violation = max(
        max(0.0, sum(a * x for a, x in zip(row.coefficients, point, strict=True)) - row.upper)
        for row in nominal_rows
    )
    checks = {
        "endpoint_reproduced": first is not None and abs(first - endpoint.side) <= 1e-8,
        "nominal_centroid_rows": nominal_violation <= 1e-8,
        "all_raw_branches_accounted": bounded["raw_branches"] == 256
        and bounded["execution_complete"],
        "relaxed_slider_monotonicity": first is not None
        and second is not None
        and second <= first + 1e-8,
        "fully_relaxed_monotonicity": second is not None
        and third is not None
        and third <= second + 1e-8,
        "omission_refuses_complete_point": not omitted["execution_complete"]
        and omitted["heuristic_point_minimum"] is None,
        "domain_roster": len(domain_rows(endpoint, rho_position, "bounded_tube")) == 64
        and len(domain_rows(endpoint, rho_position, "drop_sliders")) == 58,
    }
    return {
        "settings": {
            "per_point_wall_seconds": wall_seconds,
            "per_branch_solver_seconds": solver_seconds,
            "baseline_branch_limit": 256,
            "omission_control_branch_limit": 1,
        },
        "checks": checks,
        "passed": all(checks.values()),
        "nominal_centroid_max_violation": nominal_violation,
        "bounded": bounded,
        "drop_sliders": relaxed,
        "fully_relaxed": fully_relaxed,
        "omitted": omitted,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--controls", action="store_true")
    mode.add_argument(
        "--points",
        type=Path,
        help="frozen JSON object with points [{id,q:[16 rational strings]}]",
    )
    parser.add_argument("--root", type=Path, default=ROOT_CERTIFICATE)
    parser.add_argument("--rho-position", type=Fraction, required=True)
    parser.add_argument("--profile", choices=PROFILES, default="bounded_tube")
    parser.add_argument("--branch-limit", type=int, default=256)
    parser.add_argument("--wall-seconds", type=float, default=60.0, help="per-point ceiling")
    parser.add_argument("--solver-seconds", type=float, default=5.0)
    parser.add_argument(
        "--total-wall-seconds",
        type=float,
        default=540.0,
        help="cooperative whole-run ceiling including controls",
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    if any(
        not math.isfinite(value) or value <= 0
        for value in (args.wall_seconds, args.solver_seconds, args.total_wall_seconds)
    ):
        parser.error("wall and solver ceilings must be finite and positive")
    if not 1 <= args.branch_limit <= 256:
        parser.error("branch limit must be in 1..256")
    if args.rho_position <= 0:
        parser.error("position radius must be positive")
    run_start = time.monotonic()
    global_deadline = run_start + args.total_wall_seconds
    controls = synthetic_controls(
        solver_seconds=min(args.wall_seconds, args.solver_seconds, args.total_wall_seconds)
    )
    if not all(controls.values()):
        atomic_write_text(
            args.output,
            retained_json.dumps(
                {"schema": SCHEMA, "status": "control_failure", "controls": controls}
            ),
            make_parents=True,
        )
        return 1
    endpoint = load_endpoint(args.root)
    root_document = json.loads(args.root.read_text())
    accepted_side = (
        {
            "source": repository_path(ENDPOINT_AUDIT),
            "outward_decimal_enclosure": json.loads(ENDPOINT_AUDIT.read_text())["side"][
                "outward_decimal_enclosure"
            ],
            "assurance": "retained feasibility audit premise, not reverified by this probe",
        }
        if args.root.resolve() == ROOT_CERTIFICATE.resolve()
        else None
    )
    result: dict[str, Any] = {
        "schema": SCHEMA,
        "assurance": "exploratory numerical reconnaissance at rational root midpoint",
        "controls": controls,
        "retained_labels": list(LABELS),
        "root_input": repository_path(args.root),
        "nominal_side": endpoint.side,
        "nominal_root_midpoint": {
            "t": str(endpoint.parameters[0]),
            "beta": str(endpoint.parameters[1]),
            "root_box_radius": root_document["box"]["radius"],
        },
        "accepted_side_enclosure": accepted_side,
        "half_angle_representation": "q=tan(delta/2); delta=2atan(q), not q radians",
        "rho_position_exact": str(args.rho_position),
        "solver_settings": {
            "method": "highs",
            "tolerance": 1e-8,
            "per_point_wall_seconds": args.wall_seconds,
            "per_branch_solver_seconds": args.solver_seconds,
            "branch_limit": args.branch_limit,
            "total_wall_seconds": args.total_wall_seconds,
            "wall_ceiling_kind": "cooperative; solver calls have bounded leases",
        },
        "provenance": provenance(
            Path(__file__),
            REPO / "packing/devtools/check_n17_endpoint_feasibility.py",
            REPO / "packing/devtools/check_n17_endpoint_features.py",
            REPO / "packing/devtools/check_n17_contact_chart.py",
        ),
    }
    result["endpoint_controls"] = endpoint_controls(
        endpoint,
        float(args.rho_position),
        wall_seconds=args.wall_seconds,
        solver_seconds=args.solver_seconds,
        global_deadline=global_deadline,
    )
    result["geometry_controls"] = geometry_controls(endpoint, float(args.rho_position))
    if not result["endpoint_controls"]["passed"] or not result["geometry_controls"]["passed"]:
        result["status"] = "control_failure"
    elif args.controls:
        result["status"] = "controls_passed"
    else:
        document = json.loads(args.points.read_text())
        points = document["points"]
        if not points or len({point["id"] for point in points}) != len(points):
            raise ValueError("nonempty point list with unique IDs required")
        evaluated: dict[tuple[tuple[Fraction, ...], str], int] = {}
        outputs: list[dict[str, Any]] = []
        aliases = []
        result["point_aliases"], result["points"] = aliases, outputs
        result["unstarted_point_ids"] = []
        for point_index, point in enumerate(points):
            if time.monotonic() >= global_deadline:
                result["unstarted_point_ids"] = [item["id"] for item in points[point_index:]]
                result["unstarted_reason"] = "global_wall_limit"
                break
            if len(point["q"]) != 16 or any(type(value) is not str for value in point["q"]):
                raise ValueError("each point needs sixteen rational strings")
            turns = tuple(Fraction(value) for value in point["q"])
            profile = point.get("profile", args.profile)
            if profile not in PROFILES:
                raise ValueError("point profile must name a declared domain profile")
            key = turns, profile
            if key not in evaluated:
                evaluated[key] = len(outputs)
                outputs.append(
                    evaluate_point(
                        endpoint,
                        turns,
                        rho_position=float(args.rho_position),
                        profile=profile,
                        branch_limit=args.branch_limit,
                        wall_seconds=args.wall_seconds,
                        solver_seconds=args.solver_seconds,
                        global_deadline=global_deadline,
                    )
                )
            aliases.append({"id": point["id"], "outcome_index": evaluated[key], "input": point})
            result["status"] = "in_progress"
            result["total_elapsed_seconds"] = time.monotonic() - run_start
            atomic_write_text(
                args.output,
                retained_json.dumps(result, allow_nan=False),
                make_parents=True,
            )
        result["point_aliases"] = aliases
        result["points"] = outputs
        result["status"] = (
            "complete_numerical"
            if not result["unstarted_point_ids"]
            and all(point["status"] == "complete_numerical" for point in outputs)
            else "inconclusive"
        )
        result["unstarted_point_count"] = len(result["unstarted_point_ids"])
    result["total_elapsed_seconds"] = time.monotonic() - run_start
    atomic_write_text(
        args.output, retained_json.dumps(result, allow_nan=False), make_parents=True
    )
    print(json.dumps({"status": result["status"], "output": str(args.output)}))
    return 0 if result["status"] in {"controls_passed", "complete_numerical"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
