"""Replay a conditional positive-16 punctured cone with exact finite gap weights.

The endpoint r=0 is retained. This separate cone times six free angle coordinates
does not certify a full annulus, capture tree or global bound. Import reads no targets.
"""

from __future__ import annotations

import argparse
import copy
import json
import sys
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path
from typing import Any

import sympy as sp

from devtools import audit_n17_endpoint_receipt as exact
from devtools import check_n17_core_stress as core
from devtools import check_n17_endpoint_feasibility as endpoint
from devtools import check_n17_widened_cone as negative
from devtools import check_n17_widened_features as forcing
from devtools.check_n17_core_stress import Dyadic
from devtools.check_n17_endpoint_feasibility import (
    _layout,  # pyright: ignore[reportPrivateUsage]
)
from devtools.provenance import provenance
from sqpack import retained_json

SCHEMA = "n17-widened-positive-continuous-cone/v1"
LABELS = negative.LABELS
SMALL = (1, 2, 3, 8, 11, 12, 13, 14, 17)
FREE = (4, 5, 7, 9, 10, 15)
WALLS = (
    (1, "left"),
    (1, "bottom"),
    (2, "bottom"),
    (3, "left"),
    (8, "right"),
    (8, "top"),
    (17, "right"),
)
PAIRS = (
    (1, 2),
    (1, 3),
    (2, 13),
    (3, 11),
    (8, 16),
    (11, 12),
    (12, 16),
    (13, 14),
    (14, 17),
    (16, 17),
)
CONSTANTS = {
    "radial_upper": "1/200",
    "epsilon": "1/128",
    "position_radius": "1/100",
    "distance_upper": "4/3",
    "sqrt2_upper": "99/70",
    "ordinary_pair_change_upper": "24/5",
    "owner12_pair_change_upper": "19/5",
    "H_upper": "-1/2",
    "M_upper": "50",
    "margin_gamma": "11197999975/102405120064",
}
DOMAIN = {
    "radial_interval_checked": ["0", "1/200"],
    "excluded_radial_domain": "0 < r <= 1/200",
    "q16": "+r",
    "small_labels": list(SMALL),
    "small_half_angle_bound": "r/128",
    "free_labels": list(FREE),
    "free_half_angle_interval": ["-1/200", "1/200"],
    "endpoint_excluded": False,
}
SCOPE = (
    "conditional positive-16 cone times six free angle coordinates in the fixed root-side "
    "container; r=0 retained; no full annulus, outer capture or global side lower bound"
)


def weights(c: Any, s: Any, dr: Any, er: Any) -> dict[str, Any]:
    alpha, gamma = c * dr - s * er, c * er + s * dr
    wall = (c * er * alpha / s, s, er * alpha, c, er * gamma, dr * gamma, alpha * gamma / s)
    pairs = (
        c * er * alpha / s,
        s,
        er * alpha / s,
        1,
        gamma,
        1,
        1,
        er * alpha / s,
        er * alpha / s,
        alpha,
    )
    return {
        **{
            f"wall:{label}:{face}": value
            for (label, face), value in zip(WALLS, wall, strict=True)
        },
        **{
            f"pair:{left}:{right}": value
            for (left, right), value in zip(PAIRS, pairs, strict=True)
        },
    }


def unit_reduce(value: Any, symbols: tuple[Any, ...]) -> Any:
    c, s, dr, er = symbols
    numerator, _ = sp.fraction(sp.cancel(value))
    ideal = sp.groebner((c * c + s * s - 1, dr * dr + er * er - 1), c, s, dr, er)
    return sp.expand(ideal.reduce(sp.expand(numerator))[1])


def support(label: int, normal: tuple[Any, Any], symbols: tuple[Any, ...]) -> Any:
    """Absolute projections use only separately certified positive expressions."""
    c, s, dr, er = symbols
    positive = (0, 1, c, s, dr, er, c * dr - s * er, c * er + s * dr)
    components = []
    for axis in negative.basis(label, *symbols):
        projection = normal[0] * axis[0] + normal[1] * axis[1]
        for candidate in positive:
            if (
                unit_reduce(projection - candidate, symbols) == 0
                or unit_reduce(projection + candidate, symbols) == 0
            ):
                components.append(candidate)
                break
        else:
            raise exact.AuditError("unsupported positive-cone support sign")
    return sum(components) / sp.Integer(2)


def selected_options() -> tuple[dict[str, Any], ...]:
    options = negative.selected_options()
    required = {(8, 16): (16, "q", -1), (12, 16): (12, "u", 1), (16, 17): (16, "p", 1)}
    for pair, witness in required.items():
        variants = [option for option in options if (option["left"], option["right"]) == pair]
        exact.require(
            len(variants) == 1
            and (variants[0]["owner"], variants[0]["axis"], variants[0]["sign"]) == witness,
            "changed positive-cone distinguished owner/axis/sign",
        )
    exact.require(
        set(PAIRS) <= {(o["left"], o["right"]) for o in options}, "missing weighted pair"
    )
    return options


def symbolic_rows(options: tuple[dict[str, Any], ...]) -> tuple[dict[str, Any], ...]:
    symbols = sp.symbols("c s d_r e_r", positive=True)
    rows = []
    for label, face in WALLS:
        axis = 0 if face in {"left", "right"} else 1
        sign = 1 if face in {"left", "bottom"} else -1
        coefficients: list[Any] = [sp.Integer(0)] * 33
        coefficients[2 * LABELS.index(label) + axis], coefficients[32] = sign, int(sign < 0)
        normal = (1, 0) if axis == 0 else (0, 1)
        rows.append(
            {
                "name": f"wall:{label}:{face}",
                "coefficients": coefficients,
                "rhs": support(label, normal, symbols),
                "labels": [label],
            }
        )
    for left, right in PAIRS:
        variants = [o for o in options if (o["left"], o["right"]) == (left, right)]
        first = None
        for option in variants:
            names = forcing.features.basis_names(option["owner"])
            normal = tuple(
                option["sign"] * value
                for value in negative.basis(option["owner"], *symbols)[
                    names.index(option["axis"])
                ]
            )
            coefficients = [sp.Integer(0)] * 33
            for axis in (0, 1):
                coefficients[2 * LABELS.index(left) + axis] = -normal[axis]
                coefficients[2 * LABELS.index(right) + axis] = normal[axis]
            item = {
                "name": f"pair:{left}:{right}",
                "coefficients": coefficients,
                "rhs": support(left, normal, symbols) + support(right, normal, symbols),
                "labels": [left, right],
            }
            if first is None:
                first = item
            else:
                exact.require(
                    all(
                        unit_reduce(a - b, symbols) == 0
                        for a, b in zip(coefficients, first["coefficients"], strict=True)
                    )
                    and unit_reduce(item["rhs"] - first["rhs"], symbols) == 0,
                    "alternative positive-cone owner baseline differs",
                )
        exact.require(first is not None, "missing positive-cone pair row")
        rows.append(first)
    return tuple(rows)


def gap(c: Any, s: Any, dr: Any, er: Any, side: Any, *, y17: Any) -> Any:
    alpha, gamma = c * dr - s * er, c * er + s * dr
    cc = dr * (side - 1) - er * (y17 + sp.Rational(1, 2)) - sp.Rational(1, 2)
    bb = (dr + er) * (side - 1) - sp.Rational(1, 2)
    return alpha * (cc - sp.Rational(1, 2)) + gamma * (bb - sp.Rational(1, 2)) - (c + 2 * s + 2)


def h_coefficients(c: Any, s: Any, d: Any, e: Any, side: Any, *, y17: Any) -> tuple[Any, ...]:
    tt, zz = side - 1, y17 + Q(1, 2)
    a2, b2, c2 = (c + s) * tt, c * (tt - zz), s * zz + c * tt
    q0 = a2 * d * d + b2 * d * e + c2 * e * e
    q90 = a2 * e * e - b2 * d * e + c2 * d * d
    qcross = 2 * d * e * (a2 - c2) + b2 * (e * e - d * d)
    l0, lcross = (c + s) * d + (c - s) * e, (c + s) * e - (c - s) * d
    return 2 * (qcross - lcross), 4 * (q90 - q0) + 2 * l0, -2 * (qcross + lcross), 2 * l0


def verify_rows(
    rows: tuple[dict[str, Any], ...], multipliers: dict[str, Any]
) -> dict[str, Any]:
    symbols = sp.symbols("c s d_r e_r", positive=True)
    c, s, dr, er = symbols
    exact.require(
        len(rows) == 17
        and len({row["name"] for row in rows}) == 17
        and {row["name"] for row in rows} == set(weights(*symbols)) == set(multipliers),
        "wrong positive weighted-row roster",
    )
    coefficients = [
        sp.cancel(sum(multipliers[row["name"]] * row["coefficients"][j] for row in rows))
        for j in range(33)
    ]
    exact.require(
        all(unit_reduce(value, symbols) == 0 for value in coefficients[:32]),
        "positive centre coefficients do not cancel",
    )
    alpha, gamma = c * dr - s * er, c * er + s * dr
    side_weight = gamma * (dr + er + alpha / s)
    exact.require(
        unit_reduce(coefficients[32] - side_weight, symbols) == 0,
        "positive side coefficient differs",
    )
    t, beta, radial = sp.symbols("t beta r", real=True)
    side, aux, centres = _layout(t, beta, sp.Rational(1, 2))
    drad = (aux["d"] * (1 - radial**2) + 2 * aux["e"] * radial) / (1 + radial**2)
    erad = (aux["e"] * (1 - radial**2) - 2 * aux["d"] * radial) / (1 + radial**2)
    replacement = {c: aux["c"], s: aux["s"], dr: drad, er: erad}
    rhs = sum(multipliers[row["name"]] * row["rhs"] for row in rows)
    exact.require(
        sp.cancel(
            (side_weight * side - rhs).subs(replacement)
            - gap(aux["c"], aux["s"], drad, erad, side, y17=centres[16][1])
        )
        == 0,
        "positive fixed-container gap identity differs",
    )
    return {
        "centre_coefficients": ["0"] * 32,
        "side_coefficient": str(sp.cancel(side_weight)),
        "fixed_gap": "G(r)=alpha_r*(C_r-1/2)+gamma_r*(B_r-1/2)-(c+2*s+2)",
        "alternative_owners_equal": True,
        "unit_reduction": ["c^2+s^2=1", "d_r^2+e_r^2=1"],
    }


@lru_cache(maxsize=1)
def _symbolic_packet() -> dict[str, Any]:
    c, s, dr, er = sp.symbols("c s d_r e_r", positive=True)
    options = selected_options()
    rows, multipliers = symbolic_rows(options), weights(c, s, dr, er)
    identities = verify_rows(rows, multipliers)
    alpha, gamma = c * dr - s * er, c * er + s * dr
    wall_mass = sum(multipliers[f"wall:{label}:{face}"] for label, face in WALLS)
    pair_mass = c * er * alpha / s + s + 3 * er * alpha / s + 2
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
        "positive ordinary-pair mass differs",
    )
    special = {(12, 16): 1, (8, 16): gamma, (16, 17): alpha}
    exact.require(
        all(
            sp.cancel(multipliers[f"pair:{a}:{b}"] - value) == 0
            for (a, b), value in special.items()
        ),
        "positive special-pair mass differs",
    )
    labels = sorted({label for row in rows for label in row["labels"]})
    exact.require(
        labels == sorted((*SMALL, 16)) and set(labels).isdisjoint(FREE),
        "positive weighted incidence/free labels differ",
    )
    t, beta, radial = sp.symbols("t beta r", real=True)
    side, aux, centres = _layout(t, beta, sp.Rational(1, 2))
    cc, ss, dd, ee = (aux[key] for key in ("c", "s", "d", "e"))
    drad = (dd * (1 - radial**2) + 2 * ee * radial) / (1 + radial**2)
    erad = (ee * (1 - radial**2) - 2 * dd * radial) / (1 + radial**2)
    aa = side - aux["X"] - sp.Rational(3, 2)
    bb = side - aux["Y"] - sp.Rational(3, 2)
    f2 = dd * aa + ee * bb - 1
    f3 = (
        aux["alpha"] * (aux["A"] - sp.Rational(1, 2))
        + aux["gamma"] * (aux["B"] - sp.Rational(1, 2))
        - (cc + 2 * ss + 2)
    )
    polynomials = forcing.root.n17_polynomials()
    pi2, pi3 = (
        sum(value * t**i * beta**j for (i, j), value in polynomial.items())
        for polynomial in polynomials
    )
    den2 = t * (1 + t) * (1 + t * t) * (1 + beta * beta)
    den3 = (1 + t) * (1 + t * t) ** 2 * (1 + beta * beta) ** 2
    exact.require(sp.cancel(f2 - pi2 / den2) == 0, "positive F2 normalization differs")
    exact.require(sp.cancel(f3 - 2 * pi3 / den3) == 0, "positive F3 normalization differs")
    g0 = gap(cc, ss, dd, ee, side, y17=centres[16][1])
    exact.require(
        sp.cancel(g0 - f3 - aux["alpha"] * f2) == 0, "positive zero-root join differs"
    )
    coefficients = h_coefficients(cc, ss, dd, ee, side, y17=centres[16][1])
    polynomial = sum(value * radial**i for i, value in enumerate(coefficients))
    exact.require(
        sp.cancel(
            (1 + radial**2) ** 2 * (gap(cc, ss, drad, erad, side, y17=centres[16][1]) - g0)
            - radial * polynomial
        )
        == 0,
        "positive cubic radial identity differs",
    )
    exact.require(
        sp.cancel(drad**2 + erad**2 - 1) == 0 and sp.cancel(cc**2 + ss**2 - 1) == 0,
        "positive half-angle unit identity differs",
    )
    return {
        "selected_options": list(options),
        "retained_pairs": 19,
        "raw_branches": 256,
        "weighted_labels": labels,
        "weighted_rows": [
            {
                "name": row["name"],
                "weight": str(sp.cancel(multipliers[row["name"]])),
                "labels": row["labels"],
                "coefficients": [str(value) for value in row["coefficients"]],
                "rhs": str(row["rhs"]),
            }
            for row in rows
        ],
        "identities": identities,
        "F2_polynomial": str(sp.expand(pi2)),
        "F3_polynomial": str(sp.expand(pi3)),
        "F2_denominator": str(den2),
        "F3_denominator": str(den3),
        "zero_root_join": "G(0)=F3+alpha_0*F2=0; Pi2=Pi3=0 from fresh accepted root",
        "constant_residual_used": False,
        "cubic_identity": "(1+r^2)^2*(G(r)-G(0))=r*H(r)",
        "cubic_coefficients": [str(sp.cancel(value)) for value in coefficients],
        "cubic_degree": 3,
        "interval_division_by_r": False,
        "wall_mass": str(sp.cancel(wall_mass)),
        "ordinary_pair_mass": str(sp.cancel(pair_mass)),
        "special_pair_weights": {
            f"pair:{a}:{b}": str(value) for (a, b), value in special.items()
        },
    }


def symbolic_packet() -> dict[str, Any]:
    return copy.deepcopy(_symbolic_packet())


def analytic_margin(constants: dict[str, Any]) -> Q:
    exact.require(
        exact.exact_structure(constants, CONSTANTS), "changed positive-cone constants"
    )
    rho, distance, sqrt2 = (
        exact.rational(constants[key])
        for key in ("position_radius", "distance_upper", "sqrt2_upper")
    )
    exact.require(
        sqrt2 * sqrt2 > 2
        and 2 * (distance + 2 * sqrt2 * rho + 1) < Q(24, 5)
        and 2 * (distance + 2 * sqrt2 * rho) + 1 < Q(19, 5),
        "invalid positive pair Lipschitz bounds",
    )
    upper = exact.rational(constants["radial_upper"])
    margin = -exact.rational(constants["H_upper"]) / (1 + upper * upper) ** 2 - exact.rational(
        constants["M_upper"]
    ) * exact.rational(constants["epsilon"])
    exact.require(
        margin == exact.rational(constants["margin_gamma"]) and margin > 0,
        "nonpositive positive-cone margin",
    )
    return margin


def interval_packet(layout: exact.Layout) -> dict[str, list[str]]:
    def box(value: exact.Interval) -> Dyadic:
        return Dyadic.enclose(*value)

    c, s = (box(value) for value in layout.axes["u"])
    d, minus_e = (box(value) for value in layout.axes["p"])
    e = -minus_e
    radial = Dyadic.enclose(Q(0), Q(1, 200))
    squared = radial * radial
    dr = (d * (1 - squared) + 2 * e * radial) / (1 + squared)
    er = (e * (1 - squared) - 2 * d * radial) / (1 + squared)
    alpha, gamma = c * dr - s * er, c * er + s * dr
    values = weights(c, s, dr, er)
    wall_mass = sum(values[f"wall:{label}:{face}"] for label, face in WALLS)
    pair_mass = c * er * alpha / s + s + 3 * er * alpha / s + 2
    mass = wall_mass + Q(24, 5) * pair_mass + Q(19, 5) + gamma + alpha
    coeffs = h_coefficients(c, s, d, e, box(layout.side), y17=box(layout.centres[17][1]))
    h_value = Dyadic.cast(coeffs[-1])
    for value in reversed(coeffs[:-1]):
        h_value = h_value * radial + value
    t, beta = s / (1 + c), e / (1 + d)
    theta_denominator, beta_denominator = 1 + t * t, 1 + beta * beta
    intervals = {
        "c": c,
        "s": s,
        "d_r": dr,
        "e_r": er,
        "alpha_r": alpha,
        "gamma_r": gamma,
        "F2_denominator": t * (1 + t) * (1 + t * t) * (1 + beta * beta),
        "F3_denominator": (1 + t)
        * theta_denominator
        * theta_denominator
        * beta_denominator
        * beta_denominator,
        "W": Dyadic.cast(wall_mass),
        "P": pair_mass,
        "M": mass,
        "H": h_value,
        **{f"H_coefficient:{i}": Dyadic.cast(value) for i, value in enumerate(coeffs)},
        **{f"lambda:{name}": Dyadic.cast(value) for name, value in values.items()},
    }
    return {key: [str(value.lo), str(value.hi)] for key, value in intervals.items()}


def load_inputs(feature_path: Path) -> tuple[dict[str, Any], exact.Layout]:
    return negative.load_inputs(feature_path)


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
        "margin_gamma": str(analytic_margin(CONSTANTS)),
    }


def check(packet: dict[str, Any], feature_path: Path) -> dict[str, Any]:
    exact.require(
        packet["schema"] == SCHEMA and packet["scope"] == SCOPE, "wrong positive-cone contract"
    )
    exact.require(
        exact.exact_structure(packet["domain"], DOMAIN), "changed positive cone domain"
    )
    margin = analytic_margin(packet["constants"])
    exact.require(exact.rational(packet["margin_gamma"]) == margin, "changed positive margin")
    inputs, layout = load_inputs(feature_path)
    exact.require(
        exact.exact_structure(packet["inputs"], inputs), "changed accepted positive premises"
    )
    exact.require(
        exact.exact_structure(packet["symbolic"], symbolic_packet()),
        "changed positive symbolic recipe",
    )
    actual = interval_packet(layout)
    exact.require(set(packet["intervals"]) == set(actual), "missing positive interval checks")
    decoded = {}
    for name, values in actual.items():
        low, high = exact.read_interval(packet["intervals"][name])
        exact.require(
            low <= exact.rational(values[0]) <= exact.rational(values[1]) <= high,
            "positive interval does not enclose reconstruction",
        )
        decoded[name] = low, high
    signs = all(
        decoded[key][0] > 0
        for key in (
            "c",
            "s",
            "d_r",
            "e_r",
            "alpha_r",
            "gamma_r",
            "F2_denominator",
            "F3_denominator",
        )
    )
    nonnegative = all(
        value[0] >= 0 for key, value in decoded.items() if key.startswith("lambda:")
    )
    h_pass, mass_pass = decoded["H"][1] <= Q(-1, 2), decoded["M"][1] <= 50
    certified = signs and nonnegative and h_pass and mass_pass
    return {
        "schema": "n17-widened-positive-cone-check/v1",
        "verification_passed": True,
        "cone_certified": certified,
        "status": "conditional_positive_cone_certified" if certified else "inconclusive",
        "strict_signs": signs,
        "nonnegative_weights": nonnegative,
        "H_bound_passed": h_pass,
        "M_bound_passed": mass_pass,
        "margin_gamma": str(margin),
        "weighted_rows": 17,
        "retained_pairs": 19,
        "raw_branches": 256,
        "endpoint_excluded": False,
        "global_coverage_certified": False,
        "scope": SCOPE,
        "hand_implication": (
            "Astra hand derivation; not independently mathematically reviewed "
            "or machine-checked"
        ),
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
            Path(negative.__file__),
            Path(forcing.__file__),
            Path(exact.__file__),
            Path(forcing.root.__file__),
            Path(forcing.features.__file__),
            Path(endpoint.__file__),
            Path(core.__file__),
        )
        packet["execution"] = {
            "argv": list(argv) if argv is not None else sys.argv[1:],
            "features": str(args.features),
            "certificate": str(args.certificate) if args.certificate else None,
            "python": sys.version,
            "sympy": sp.__version__,
        }
    except (ValueError, OSError, KeyError, TypeError) as error:
        packet = {
            "schema": SCHEMA,
            "verification_passed": False,
            "cone_certified": False,
            "status": "refused",
            "error": str(error),
            "endpoint_excluded": False,
            "global_coverage_certified": False,
        }
        result = packet
    if args.output is not None:
        args.output.write_text(retained_json.dumps(packet))
    print(json.dumps(result))
    return 0 if result.get("cone_certified") is True else 1


if __name__ == "__main__":
    raise SystemExit(main())
