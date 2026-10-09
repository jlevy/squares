"""Replay one conditional punctured n17 cone using exact homogeneous gap weights.

The endpoint r=0 is retained. The certificate covers the stated cone times six free
angle coordinates, never a complete annulus or a capture tree. Import reads no targets.
"""

from __future__ import annotations

import argparse
import copy
import json
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path
from typing import Any

import sympy as sp

from devtools import audit_n17_endpoint_receipt as exact
from devtools import check_n17_core_stress as core
from devtools import check_n17_endpoint_feasibility as endpoint
from devtools import check_n17_widened_features as forcing
from devtools.check_n17_core_stress import Dyadic
from devtools.check_n17_endpoint_feasibility import (
    _layout,  # pyright: ignore[reportPrivateUsage]
)
from devtools.provenance import provenance
from sqpack import retained_json

SCHEMA = "n17-widened-continuous-cone/v1"
LABELS = tuple(label for label in range(1, 18) if label != 6)
SMALL = (1, 2, 3, 9, 10, 13, 14, 15, 17)
FREE = (4, 5, 7, 8, 11, 12)
CONSTANTS = {
    "radial_upper": "1/200",
    "epsilon": "1/2048",
    "position_radius": "1/100",
    "distance_upper": "4/3",
    "sqrt2_upper": "99/70",
    "pair_change_upper": "24/5",
    "K_upper": "-1/50",
    "M_upper": "50",
    "gamma": "638375/40961024",
}
DOMAIN = {
    "radial_interval_checked": ["0", "1/200"],
    "excluded_radial_domain": "0 < r <= 1/200",
    "q16": "-r",
    "small_labels": list(SMALL),
    "small_half_angle_bound": "r/2048",
    "free_labels": list(FREE),
    "free_half_angle_interval": ["-1/200", "1/200"],
    "endpoint_excluded": False,
}
SCOPE = (
    "conditional cone times six free angle coordinates in the fixed root-side container; "
    "r=0 retained; no annulus coverage, outer capture or side lower bound"
)
WALLS = ((1, "left"), (1, "bottom"), (2, "bottom"), (9, "left"), (15, "top"), (17, "right"))
PAIRS = (
    (1, 2),
    (1, 3),
    (2, 13),
    (3, 9),
    (9, 10),
    (10, 15),
    (13, 14),
    (14, 17),
    (15, 16),
    (16, 17),
)


def selected_options() -> tuple[dict[str, Any], ...]:
    options = tuple(
        option
        for option in forcing.features.expected_options()
        if option["kind"] == "identity"
        and (option["left"], option["right"]) not in forcing.DROPPED
    )
    counts = {}
    for option in options:
        pair = option["left"], option["right"]
        counts[pair] = counts.get(pair, 0) + 1
    exact.require(
        len(options) == 27 and sorted(counts.values()) == [1] * 11 + [2] * 8,
        "changed selected-feature roster",
    )
    exact.require(set(PAIRS) <= set(counts), "missing weighted pair")
    for option in options:
        if (option["left"], option["right"]) in {(15, 16), (16, 17)}:
            exact.require(option["owner"] == 16, "weighted beta pair must be owned by 16")
    return options


def weights(c: Any, s: Any, dr: Any, er: Any) -> dict[str, Any]:
    wall_values = (er * c / s, dr * s / c, er, dr, er + dr * s / c, dr + er * c / s)
    pair_values = (
        er * c / s,
        dr * s / c,
        er / s,
        dr * s / c,
        dr / c,
        dr / c,
        er / s,
        er / s,
        1,
        1,
    )
    return {
        **{
            f"wall:{label}:{wall}": value
            for (label, wall), value in zip(WALLS, wall_values, strict=True)
        },
        **{
            f"pair:{left}:{right}": value
            for (left, right), value in zip(PAIRS, pair_values, strict=True)
        },
    }


def basis(
    label: int, c: Any, s: Any, dr: Any, er: Any
) -> tuple[tuple[Any, Any], tuple[Any, Any]]:
    if label == 16:
        return (dr, -er), (er, dr)
    if 9 <= label <= 14:
        return (c, s), (-s, c)
    return (1, 0), (0, 1)


def symbolic_support(label: int, normal: tuple[Any, Any], symbols: tuple[Any, ...]) -> Any:
    """Resolve every absolute projection from positive components and unit identities."""
    c, s, dr, er = symbols
    ideal = sp.groebner((c * c + s * s - 1, dr * dr + er * er - 1), c, s, dr, er)
    values = []
    for axis in basis(label, c, s, dr, er):
        projection = ideal.reduce(sp.expand(normal[0] * axis[0] + normal[1] * axis[1]))[1]
        for positive in (0, 1, c, s, dr, er):
            if sp.expand(projection - positive) == 0 or sp.expand(projection + positive) == 0:
                values.append(positive)
                break
        else:
            raise exact.AuditError("unsupported absolute-projection sign identity")
    return sum(values) / sp.Integer(2)


def symbolic_rows(options: tuple[dict[str, Any], ...]) -> tuple[dict[str, Any], ...]:
    """Gap rows in 32 centre columns followed by the absolute container side."""
    c, s, dr, er = sp.symbols("c s d_r e_r", positive=True)
    symbols = c, s, dr, er
    rows = []
    for label, wall in WALLS:
        axis = 0 if wall in {"left", "right"} else 1
        direction = 1 if wall in {"left", "bottom"} else -1
        coefficients: list[Any] = [sp.Integer(0)] * 33
        coefficients[2 * LABELS.index(label) + axis] = direction
        coefficients[32] = int(direction == -1)
        normal = (1, 0) if axis == 0 else (0, 1)
        rows.append(
            {
                "name": f"wall:{label}:{wall}",
                "coefficients": coefficients,
                "rhs": symbolic_support(label, normal, symbols),
                "labels": [label],
            }
        )
    for left, right in PAIRS:
        variants = [o for o in options if (o["left"], o["right"]) == (left, right)]
        first = None
        for option in variants:
            names = forcing.features.basis_names(option["owner"])
            normal = tuple(
                option["sign"] * x
                for x in basis(option["owner"], *symbols)[names.index(option["axis"])]
            )
            coefficients = [sp.Integer(0)] * 33
            for axis in (0, 1):
                coefficients[2 * LABELS.index(left) + axis] = -normal[axis]
                coefficients[2 * LABELS.index(right) + axis] = normal[axis]
            rhs = symbolic_support(left, normal, symbols) + symbolic_support(
                right, normal, symbols
            )
            item = {
                "name": f"pair:{left}:{right}",
                "coefficients": coefficients,
                "rhs": rhs,
                "labels": [left, right],
            }
            if first is None:
                first = item
            else:
                exact.require(
                    all(
                        sp.cancel(a - b) == 0
                        for a, b in zip(coefficients, first["coefficients"], strict=True)
                    )
                    and sp.cancel(rhs - first["rhs"]) == 0,
                    "alternative owner baseline row differs",
                )
        exact.require(first is not None, "missing weighted pair row")
        rows.append(first)
    return tuple(rows)


def verify_rows(
    rows: tuple[dict[str, Any], ...], multipliers: dict[str, Any]
) -> dict[str, Any]:
    c, s, dr, er = sp.symbols("c s d_r e_r", positive=True)
    exact.require(
        len(rows) == 16 and len({row["name"] for row in rows}) == 16,
        "wrong weighted row roster",
    )
    exact.require(
        {row["name"] for row in rows} == set(weights(c, s, dr, er)) == set(multipliers),
        "weighted row identities differ",
    )
    coefficients = [
        sp.cancel(sum(multipliers[row["name"]] * row["coefficients"][j] for row in rows))
        for j in range(33)
    ]
    exact.require(
        all(value == 0 for value in coefficients[:32]), "centre coefficients do not cancel"
    )
    side_weight = (c + s) * (dr / c + er / s)
    exact.require(sp.cancel(coefficients[32] - side_weight) == 0, "side coefficient differs")
    # Use the independently reconstructed endpoint chart X/Y to verify the constant.
    t, beta, radial = sp.symbols("t beta r", real=True)
    side, aux, _ = _layout(t, beta, sp.Rational(1, 2))
    d_radial = (aux["d"] * (1 - radial**2) - 2 * aux["e"] * radial) / (1 + radial**2)
    e_radial = (aux["e"] * (1 - radial**2) + 2 * aux["d"] * radial) / (1 + radial**2)
    replacement = {c: aux["c"], s: aux["s"], dr: d_radial, er: e_radial}
    constant = sum(multipliers[row["name"]] * row["rhs"] for row in rows)
    a, b = side - aux["X"] - sp.Rational(3, 2), side - aux["Y"] - sp.Rational(3, 2)
    exact.require(
        sp.cancel(
            (side_weight * side - constant).subs(replacement)
            - (d_radial * a + e_radial * b - 1)
        )
        == 0,
        "weighted gap constant identity failed",
    )
    return {
        "centre_coefficients": ["0"] * 32,
        "side_coefficient": str(sp.cancel(side_weight)),
        "weighted_gap": "d_r*A+e_r*B-1",
        "alternative_owners_equal": True,
    }


@lru_cache(maxsize=1)
def _symbolic_packet() -> dict[str, Any]:
    options = selected_options()
    c, s, dr, er = sp.symbols("c s d_r e_r", positive=True)
    rows = symbolic_rows(options)
    multipliers = weights(c, s, dr, er)
    identities = verify_rows(rows, multipliers)
    wall_mass = 2 * (c + s) * (dr / c + er / s)
    pair_mass = er * c / s + 2 * dr * s / c + 3 * er / s + 2 * dr / c
    exact.require(
        sp.cancel(sum(multipliers[f"wall:{label}:{wall}"] for label, wall in WALLS) - wall_mass)
        == 0,
        "wall perturbation mass differs",
    )
    exact.require(
        sp.cancel(
            sum(
                multipliers[f"pair:{left}:{right}"]
                for left, right in PAIRS
                if 16 not in (left, right)
            )
            - pair_mass
        )
        == 0,
        "pair perturbation mass differs",
    )
    labels = sorted({label for row in rows for label in row["labels"]})
    exact.require(
        labels == sorted((*SMALL, 16)) and set(labels).isdisjoint(FREE),
        "weighted row depends on a free label",
    )
    t, beta, radial = sp.symbols("t beta r", real=True)
    side, aux, _ = _layout(t, beta, sp.Rational(1, 2))
    a, b = side - aux["X"] - sp.Rational(3, 2), side - aux["Y"] - sp.Rational(3, 2)
    f2 = aux["d"] * a + aux["e"] * b - 1
    k = -aux["e"] * a + aux["d"] * b
    d_radial = (aux["d"] * (1 - radial**2) - 2 * aux["e"] * radial) / (1 + radial**2)
    e_radial = (aux["e"] * (1 - radial**2) + 2 * aux["d"] * radial) / (1 + radial**2)
    pi2 = sum(
        coefficient * t**i * beta**j
        for (i, j), coefficient in forcing.root.n17_polynomials()[0].items()
    )
    denominator = t * (1 + t) * (1 + t * t) * (1 + beta * beta)
    exact.require(sp.cancel(f2 - pi2 / denominator) == 0, "F2 polynomial normalization differs")
    exact.require(
        sp.cancel(
            d_radial * a
            + e_radial * b
            - 1
            - ((1 - radial**2) * f2 + 2 * radial * (k - radial)) / (1 + radial**2)
        )
        == 0,
        "homogeneous radial identity differs",
    )
    exact.require(
        sp.cancel(d_radial * d_radial + e_radial * e_radial - 1) == 0,
        "turned owner basis is not unit",
    )
    exact.require(sp.cancel(aux["c"] ** 2 + aux["s"] ** 2 - 1) == 0, "theta basis is not unit")
    return {
        "selected_options": list(options),
        "raw_branches": 256,
        "weighted_labels": labels,
        "weighted_rows": [
            {
                "name": row["name"],
                "weight": str(sp.cancel(multipliers[row["name"]])),
                "labels": row["labels"],
                "rhs": str(row["rhs"]),
            }
            for row in rows
        ],
        "identities": identities,
        "F2_polynomial": str(sp.expand(pi2)),
        "F2_denominator": str(denominator),
        "F2_exact_root_join": "Pi2=0 from freshly accepted root certificate",
        "radial_identity": "((1-r^2)*F2+2*r*(K-r))/(1+r^2)",
        "constant_residual_used": False,
        "wall_mass": str(sp.cancel(wall_mass)),
        "non16_pair_mass": str(sp.cancel(pair_mass)),
    }


def symbolic_packet() -> dict[str, Any]:
    """Independent mutable receipt, never an alias of the checker's cached expectation."""
    return copy.deepcopy(_symbolic_packet())


def analytic_gamma(constants: dict[str, Any]) -> Q:
    exact.require(exact.exact_structure(constants, CONSTANTS), "changed frozen constants")
    rho, distance, sqrt2 = (
        exact.rational(constants[name])
        for name in ("position_radius", "distance_upper", "sqrt2_upper")
    )
    exact.require(
        sqrt2 * sqrt2 > 2 and 2 * (distance + 2 * sqrt2 * rho + 1) < Q(24, 5),
        "invalid pair-change bound",
    )
    radial = exact.rational(constants["radial_upper"])
    gamma = -2 * exact.rational(constants["K_upper"]) / (1 + radial * radial) - exact.rational(
        constants["epsilon"]
    ) * exact.rational(constants["M_upper"])
    exact.require(gamma == Q(constants["gamma"]) and gamma > 0, "nonpositive or wrong gamma")
    return gamma


def interval_packet(layout: exact.Layout) -> dict[str, list[str]]:
    def box(value: exact.Interval) -> Dyadic:
        return Dyadic.enclose(*value)

    c, s = (box(value) for value in layout.axes["u"])
    d, minus_e = (box(value) for value in layout.axes["p"])
    e = -minus_e
    radial = Dyadic.enclose(Q(0), Q(1, 200))
    radial_squared = radial * radial
    dr = (d * (1 - radial_squared) - 2 * e * radial) / (1 + radial_squared)
    er = (e * (1 - radial_squared) + 2 * d * radial) / (1 + radial_squared)
    a = box(layout.side) - box(layout.centres[15][0]) - Q(3, 2)
    b = box(layout.side) - box(layout.centres[17][1]) - Q(3, 2)
    k = -e * a + d * b
    w = 2 * (c + s) * (dr / c + er / s)
    p = er * c / s + 2 * dr * s / c + 3 * er / s + 2 * dr / c
    mass = w + Q(24, 5) * p + 2
    t = s / (1 + c)
    beta = e / (1 + d)
    f2_denominator = t * (1 + t) * (1 + t * t) * (1 + beta * beta)
    intervals = {
        "c": c,
        "s": s,
        "d_r": dr,
        "e_r": er,
        "A": a,
        "B": b,
        "K": k,
        "W": w,
        "P": p,
        "M": mass,
        "F2_denominator": f2_denominator,
    }
    intervals.update(
        {f"lambda:{name}": Dyadic.cast(value) for name, value in weights(c, s, dr, er).items()}
    )
    return {name: [str(value.lo), str(value.hi)] for name, value in intervals.items()}


def load_inputs(feature_path: Path) -> tuple[dict[str, Any], exact.Layout]:
    feature = exact.decode(exact.read_bytes(feature_path))
    checked = forcing.check(feature)
    exact.require(checked["verification_passed"] is True, "feature prerequisite refused")
    inputs, layout, _ = forcing.load_root()
    # The same accepted inclusion root carries Pi2=Pi3=0; no midpoint residual is used.
    return {
        "root": inputs,
        "features": str(feature_path.resolve().relative_to(exact.REPO)),
        "feature_check": checked,
        "slider_box": [[str(lo), str(hi)] for lo, hi in forcing.DOMAIN],
        "fixed_container": "[0,S*]^2",
    }, layout


def generate(feature_path: Path) -> dict[str, Any]:
    inputs, layout = load_inputs(feature_path)
    return {
        "schema": SCHEMA,
        "scope": SCOPE,
        "inputs": inputs,
        "constants": dict(CONSTANTS),
        "domain": copy.deepcopy(DOMAIN),
        "symbolic": symbolic_packet(),
        "intervals": interval_packet(layout),
        "gamma": str(analytic_gamma(CONSTANTS)),
    }


def check(packet: dict[str, Any], feature_path: Path) -> dict[str, Any]:
    exact.require(
        packet["schema"] == SCHEMA and packet["scope"] == SCOPE, "wrong cone contract"
    )
    exact.require(
        exact.exact_structure(packet["domain"], DOMAIN), "changed radial or angle domain"
    )
    gamma = analytic_gamma(packet["constants"])
    exact.require(exact.rational(packet["gamma"]) == gamma, "changed gamma")
    inputs, layout = load_inputs(feature_path)
    exact.require(exact.exact_structure(packet["inputs"], inputs), "changed accepted premises")
    exact.require(
        exact.exact_structure(packet["symbolic"], symbolic_packet()),
        "changed symbolic weights or identities",
    )
    actual = interval_packet(layout)
    exact.require(set(packet["intervals"]) == set(actual), "missing interval checks")
    for name, values in actual.items():
        low, high = exact.read_interval(packet["intervals"][name])
        exact.require(
            low <= Q(values[0]) <= Q(values[1]) <= high,
            "reported interval does not enclose reconstruction",
        )
    signs = all(
        Q(packet["intervals"][name][0]) > 0
        for name in ("c", "s", "d_r", "e_r", "F2_denominator")
    )
    nonnegative = all(
        Q(values[0]) >= 0
        for name, values in packet["intervals"].items()
        if name.startswith("lambda:")
    )
    k_pass = Q(packet["intervals"]["K"][1]) <= Q(-1, 50)
    mass_pass = Q(packet["intervals"]["M"][1]) <= 50
    certified = signs and nonnegative and k_pass and mass_pass
    return {
        "schema": "n17-widened-continuous-cone-check/v1",
        "verification_passed": True,
        "cone_certified": certified,
        "status": "conditional_cone_certified" if certified else "inconclusive",
        "strict_signs": signs,
        "nonnegative_weights": nonnegative,
        "K_bound_passed": k_pass,
        "M_bound_passed": mass_pass,
        "gamma": str(gamma),
        "weighted_rows": 16,
        "raw_branches": 256,
        "endpoint_excluded": False,
        "global_coverage_certified": False,
        "scope": SCOPE,
        "hand_implication": "Astra's uniform gap perturbation remains a reviewed hand premise",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--features", required=True, type=Path)
    parser.add_argument("--certificate", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        packet = (
            generate(args.features)
            if args.certificate is None
            else exact.decode(exact.read_bytes(args.certificate))
        )
        result = check(packet, args.features)
        packet["checker"] = result
        packet["provenance"] = provenance(
            Path(__file__),
            Path(forcing.__file__),
            Path(exact.__file__),
            Path(forcing.root.__file__),
            Path(forcing.features.__file__),
            Path(endpoint.__file__),
            Path(core.__file__),
        )
    except (ValueError, OSError, KeyError, TypeError) as error:
        packet = {
            "schema": SCHEMA,
            "verification_passed": False,
            "status": "refused",
            "error": str(error),
        }
        result = packet
    if args.output is not None:
        args.output.write_text(retained_json.dumps(packet))
    print(json.dumps(result))
    return 0 if result.get("cone_certified") is True else 1


if __name__ == "__main__":
    raise SystemExit(main())
