"""Check a noncircular conditional physical-pair lower slider bound.

The coarse domain does not assume BW' or H278. Only the fresh accepted-root loader
is reused. This instrument checks a root guard and finite identities/envelopes, not
an actual capture leaf or global coverage. Importing it reads no scientific inputs.
"""

from __future__ import annotations

import argparse
import copy
import itertools
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
from devtools import check_n17_widened_features as root_loader
from devtools.check_n17_core_stress import Dyadic
from devtools.check_n17_endpoint_feasibility import (
    _layout,  # pyright: ignore[reportPrivateUsage]
)
from devtools.provenance import provenance
from sqpack import retained_json

SCHEMA = "n17-independent-coarse-slider-floor/v1"
CONVENTION = "all SAT normals directed against Delta=x9-x11; +v survives"
CONSTANTS = {
    "root_tau_lower": "-1/3",
    "root_tau_upper": "-1/8",
    "coordinate_radius9": "1/100",
    "eta_radius11": "1/100",
    "v_projection_radius9": "1/5000",
    "sqrt2_upper": "99/70",
    "U_absolute_upper": "9/25",
    "universal_pair_support_lower": "1",
    "desired_b_floor": "-1/2500",
    "floor": "-14333333/41666665000",
    "headroom": "2333333/41666665000",
}
DOMAIN = {
    "e9_x": ["-1/100", "1/100"],
    "e9_y": ["-1/100", "1/100"],
    "eta11": ["-1/100", "1/100"],
    "v_dot_e9": ["-1/5000", "1/5000"],
    "b_independent_coarse": ["-1/2", "1/12"],
    "q9": ["-1/200", "1/5000"],
    "q11": ["-1/200", "1/5000"],
    "closed": True,
    "physical_pair_non_overlap": [9, 11],
    "H278_required": False,
    "BW_prime_required": False,
}
SCOPE = (
    "conditional physical 9/11 pair lemma on the independent closed coarse domain; "
    "no actual leaf acceptance, BW' assumption, LP-relaxation consequence or global coverage"
)


def sat_options() -> list[dict[str, Any]]:
    return [
        {"id": f"{owner}:{axis}:{sign}", "owner": owner, "axis": axis, "sign": sign}
        for owner, axis, sign in itertools.product((9, 11), ("u", "v"), (-1, 1))
    ]


@lru_cache(maxsize=1)
def _symbolic_packet() -> dict[str, Any]:
    t, beta, q = sp.symbols("t beta q", real=True)
    _, aux, centres = _layout(t, beta, sp.Rational(1, 2))
    c, s = aux["c"], aux["s"]
    tau = c * (s - 1)
    displacement = tuple(centres[8][axis] - centres[10][axis] for axis in (0, 1))
    nominal = (tau * c - s, tau * s + c)
    exact.require(
        all(sp.cancel(a - b) == 0 for a, b in zip(displacement, nominal, strict=True)),
        "coarse nominal displacement identity differs",
    )
    exact.require(sp.cancel(c * c + s * s - 1) == 0, "coarse root axes are not unit")
    ex, ey, eta, b = sp.symbols("e9_x e9_y eta11 b", real=True)
    delta = nominal[0] + ex - eta * c - b * s, nominal[1] + ey - eta * s + b * c
    u_projection, v_projection = c * delta[0] + s * delta[1], -s * delta[0] + c * delta[1]
    exact.require(
        sp.cancel(u_projection - (tau + c * ex + s * ey - eta)) == 0,
        "coarse U projection sign differs",
    )
    exact.require(
        sp.cancel(v_projection - (1 + b - s * ex + c * ey)) == 0,
        "coarse V projection sign differs",
    )
    cosine, sine = (1 - q * q) / (1 + q * q), 2 * q / (1 + q * q)
    tangent, secant = 2 * q / (1 - q * q), (1 + q * q) / (1 - q * q)
    exact.require(
        sp.cancel(cosine**2 + sine**2 - 1) == 0
        and sp.cancel(tangent * cosine - sine) == 0
        and sp.cancel(secant * cosine - 1) == 0,
        "coarse half-angle identities differ",
    )
    u_projection_symbol, ev = sp.symbols("U v_dot_e9", real=True)
    exact.require(
        sp.cancel(
            cosine * (1 + b + ev)
            - sine * u_projection_symbol
            - 1
            - cosine * (b - (secant - 1 + tangent * u_projection_symbol - ev))
        )
        == 0,
        "coarse surviving-row rearrangement differs",
    )
    return {
        "nominal_displacement": "x9*-x11*=tau0*u+v",
        "tau0": "c*(s-1)",
        "u": ["c", "s"],
        "v": ["-s", "c"],
        "root_axis_unit_identity": "c^2+s^2=1 from exact half-angle chart",
        "b_definition": "b=-v dot (x11-x11*)",
        "eta11_definition": "eta11=u dot (x11-x11*)",
        "U": "tau0+u dot e9-eta11",
        "V": "1+b+v dot e9",
        "positive_v_projection": "cos(delta_i)*V-sin(delta_i)*U",
        "half_angle_cosine": str(cosine),
        "half_angle_sine": str(sine),
        "half_angle_tangent": str(tangent),
        "half_angle_secant": str(secant),
        "surviving_row_rearrangement": "cos(delta)*(b-(sec(delta)-1+tan(delta)*U-v dot e9))>=0",
        "support_lemma": "own support1/2; other support>=1/2 by unit l1>=unit l2",
        "SAT_lemma": (
            "physical interior non-overlap leaves at least one of eight signed owner-axis rows"
        ),
        "nominal_corner_witness_used": False,
        "interval_division_by_zero": False,
    }


def symbolic_packet() -> dict[str, Any]:
    return copy.deepcopy(_symbolic_packet())


def finite_packet() -> dict[str, Any]:
    exact.require(
        DOMAIN["q9"] == DOMAIN["q11"] == ["-1/200", "1/5000"],
        "both owners require the same asymmetric half-angle domain",
    )
    sqrt2 = exact.rational(CONSTANTS["sqrt2_upper"])
    rho9 = exact.rational(CONSTANTS["coordinate_radius9"])
    eta11 = exact.rational(CONSTANTS["eta_radius11"])
    projection9 = exact.rational(CONSTANTS["v_projection_radius9"])
    tau_lo, tau_hi = (
        exact.rational(CONSTANTS["root_tau_lower"]),
        exact.rational(CONSTANTS["root_tau_upper"]),
    )
    u_abs = exact.rational(CONSTANTS["U_absolute_upper"])
    u_lo, u_hi = tau_lo - sqrt2 * rho9 - eta11, tau_hi + sqrt2 * rho9 + eta11
    b_lo, b_hi = (exact.rational(value) for value in DOMAIN["b_independent_coarse"])
    v_lo, v_hi = 1 + b_lo - projection9, 1 + b_hi + projection9
    q_lo, q_hi = (exact.rational(value) for value in DOMAIN["q9"])
    q0 = max(abs(q_lo), abs(q_hi))
    c0, s0 = (1 - q0 * q0) / (1 + q0 * q0), 2 * q0 / (1 + q0 * q0)
    exact.require(
        sqrt2 * sqrt2 > 2
        and -u_abs < u_lo <= u_hi < 0
        and v_lo > 0
        and 0 <= q_hi < q0 < 1
        and c0 > 0,
        "invalid independent coarse envelope",
    )
    tangent = 2 * q_hi / (1 - q_hi * q_hi)
    floor = -projection9 - u_abs * tangent
    headroom = floor - exact.rational(CONSTANTS["desired_b_floor"])
    exact.require(
        floor == exact.rational(CONSTANTS["floor"]) == -Q(1, 5000) - Q(3600, 24999999)
        and headroom == exact.rational(CONSTANTS["headroom"]) > 0,
        "wrong coarse floor or strict headroom",
    )
    options = sat_options()
    keys = [(option["owner"], option["axis"], option["sign"]) for option in options]
    exact.require(
        len(keys) == len(set(keys)) == 8
        and set(keys) == set(itertools.product((9, 11), ("u", "v"), (-1, 1)))
        and all(
            option["id"] == f"{option['owner']}:{option['axis']}:{option['sign']}"
            for option in options
        ),
        "coarse SAT roster is not exactly eight unique owner-axis-sign options",
    )
    omitted, survivors = [], []
    for option in options:
        if option["axis"] == "v" and option["sign"] == 1:
            survivors.append(option)
            continue
        projection = u_abs + s0 * v_hi if option["axis"] == "u" else s0 * u_abs - c0 * v_lo
        gap_upper = projection - exact.rational(CONSTANTS["universal_pair_support_lower"])
        exact.require(gap_upper < 0, "coarse omitted SAT row not strict")
        omitted.append(
            {
                **option,
                "projection_upper": str(projection),
                "gap_upper": str(gap_upper),
                "witness": "whole-coarse-domain rational envelope; universal support>=1",
            }
        )
    exact.require(len(omitted) == 6 and len(survivors) == 2, "wrong coarse SAT partition")
    return {
        "U_derived_bounds": [str(u_lo), str(u_hi)],
        "U_strict_outer_bounds": [str(-u_abs), "0"],
        "V_closed_bounds": [str(v_lo), str(v_hi)],
        "cosine_lower": str(c0),
        "absolute_sine_upper": str(s0),
        "positive_tangent_upper": str(tangent),
        "positive_q_upper": str(q_hi),
        "omitted": omitted,
        "survivors": survivors,
        "floor": str(floor),
        "desired_b_floor": CONSTANTS["desired_b_floor"],
        "strict_headroom": str(headroom),
        "floor_implication": (
            "sec(delta)-1>=0; tan(delta)*U>=0 for delta<=0; "
            "otherwise tan(delta)<=positive_tangent_upper and U>=-9/25"
        ),
        "closes_BW_prime": False,
        "leaf_predicate_checked": False,
    }


def load_inputs(root_path: Path) -> tuple[dict[str, Any], exact.Layout]:
    # Reuse ONLY root admission. In particular do not call root_loader.check/generate.
    inputs, layout, _ = root_loader.load_root(root_path)
    return {"root": inputs, "root_only_prerequisite": True}, layout


def root_intervals(layout: exact.Layout) -> dict[str, list[str]]:
    c, s = (Dyadic.enclose(*value) for value in layout.axes["u"])
    tau = c * (s - 1)
    return {"tau0": [str(tau.lo), str(tau.hi)]}


def generate(root_path: Path = root_loader.ROOT_PATH) -> dict[str, Any]:
    inputs, layout = load_inputs(root_path)
    return {
        "schema": SCHEMA,
        "scope": SCOPE,
        "convention": CONVENTION,
        "inputs": inputs,
        "constants": dict(CONSTANTS),
        "coarse_domain": copy.deepcopy(DOMAIN),
        "symbolic": symbolic_packet(),
        "finite": finite_packet(),
        "root_intervals": root_intervals(layout),
    }


def check(packet: dict[str, Any], root_path: Path = root_loader.ROOT_PATH) -> dict[str, Any]:
    exact.require(
        packet["schema"] == SCHEMA
        and packet["scope"] == SCOPE
        and packet["convention"] == CONVENTION,
        "wrong independent coarse-floor contract",
    )
    exact.require(
        exact.exact_structure(packet["constants"], CONSTANTS)
        and exact.exact_structure(packet["coarse_domain"], DOMAIN),
        "changed constants or circular coarse domain",
    )
    inputs, layout = load_inputs(root_path)
    exact.require(
        exact.exact_structure(packet["inputs"], inputs), "changed accepted coarse root premises"
    )
    exact.require(
        exact.exact_structure(packet["symbolic"], symbolic_packet()),
        "changed displacement/unit/projection identities",
    )
    expected = finite_packet()
    exact.require(
        exact.exact_structure(packet["finite"], expected),
        "changed SAT inventory/envelopes/floor/headroom",
    )
    actual = root_intervals(layout)
    exact.require(set(packet["root_intervals"]) == set(actual), "missing coarse root guard")
    lo, hi = exact.read_interval(packet["root_intervals"]["tau0"])
    actual_lo, actual_hi = exact.read_interval(actual["tau0"])
    exact.require(
        lo <= actual_lo <= actual_hi <= hi,
        "coarse root interval does not enclose reconstruction",
    )
    guard = (
        exact.rational(CONSTANTS["root_tau_lower"])
        <= lo
        <= hi
        <= exact.rational(CONSTANTS["root_tau_upper"])
    )
    return {
        "schema": "n17-independent-coarse-slider-floor-check/v1",
        "verification_passed": True,
        "floor_certified": guard,
        "status": "conditional_slider_floor_certified" if guard else "inconclusive",
        "root_guard_passed": guard,
        "SAT_options": 8,
        "omitted_options": 6,
        "surviving_options": 2,
        "floor": expected["floor"],
        "strict_headroom": expected["strict_headroom"],
        "physical_pair_non_overlap_required": [9, 11],
        "H278_required": False,
        "BW_prime_required": False,
        "LP_relaxation_consequence": False,
        "leaf_predicate_checked": False,
        "global_coverage_certified": False,
        "scope": SCOPE,
        "hand_implication": (
            "Astra hand derivation; not independently mathematically reviewed "
            "or machine-checked"
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=root_loader.ROOT_PATH)
    parser.add_argument("--certificate", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        packet = (
            generate(args.root)
            if args.certificate is None
            else exact.decode(exact.read_bytes(args.certificate))
        )
        result = check(packet, args.root)
        packet["checker"] = result
        packet["provenance"] = provenance(
            Path(__file__),
            Path(root_loader.__file__),
            Path(root_loader.root.__file__),
            Path(exact.__file__),
            Path(endpoint.__file__),
            Path(core.__file__),
        )
        packet["execution"] = {
            "argv": list(argv) if argv is not None else sys.argv[1:],
            "root": str(args.root),
            "python": sys.version,
            "sympy": sp.__version__,
        }
    except (ValueError, OSError, KeyError, TypeError) as error:
        packet = {
            "schema": SCHEMA,
            "verification_passed": False,
            "floor_certified": False,
            "status": "refused",
            "error": str(error),
            "leaf_predicate_checked": False,
            "global_coverage_certified": False,
        }
        result = packet
    if args.output is not None:
        args.output.write_text(retained_json.dumps(packet))
    print(json.dumps(result))
    return 0 if result.get("floor_certified") is True else 1


if __name__ == "__main__":
    raise SystemExit(main())
