"""Certify a frozen numeric capture cap against the fresh full accepted root.

This root-only instrument proves a side/cap join, not endpoint containment in
cells, capture, exclusion or global coverage. Existing None/U objects retain
their original frame; this receipt does not relabel them with the new cap.
"""

from __future__ import annotations

import argparse
import copy
import inspect
import json
import sys
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path
from typing import Any

import sympy as sp

from devtools import audit_n17_endpoint_receipt as exact
from devtools import check_n17_endpoint_feasibility as endpoint
from devtools import check_n17_widened_features as root_loader
from devtools.check_n17_endpoint_feasibility import (
    _layout,  # pyright: ignore[reportPrivateUsage]
)
from devtools.provenance import provenance
from sqpack import retained_json

SCHEMA = "n17-capture-cap-root-join/v1"
CAP = Q(935106018721, 200000000000)
OUTER_CAP = Q(1169, 250)
EPSILON = Q(1, 10**12)
CONSTANTS = {
    "numeric_capture_cap": str(CAP),
    "outer_cover_cap": str(OUTER_CAP),
    "maximum_all_root_excess": str(EPSILON),
}
FALSE_FLAGS = {
    "capture_proved": False,
    "leaf_predicate_checked": False,
    "endpoint_cell_containment_proved": False,
    "exclusion_proved": False,
    "global_coverage_proved": False,
    "existing_objects_relabelled": False,
    "producer_run": False,
    "H278_required": False,
}
SCOPE = (
    "root/side/numeric-cap join only; fresh numeric-cap producer and saved replay are separate"
)


def formula(t: Q) -> Q:
    return (6 + 4 * t) / (1 + 2 * t - t * t)


@lru_cache(maxsize=1)
def _symbolic_packet() -> dict[str, Any]:
    t, beta = sp.symbols("t beta", real=True)
    side, _, _ = _layout(t, beta, sp.Rational(1, 2))
    expected = (6 + 4 * t) / (1 + 2 * t - t * t)
    derivative = 4 * (t * t + 3 * t - 2) / (1 + 2 * t - t * t) ** 2
    exact.require(sp.cancel(side - expected) == 0, "endpoint side formula differs")
    exact.require(sp.cancel(sp.diff(expected, t) - derivative) == 0, "side derivative differs")
    exact.require(sp.diff(side, beta) == 0, "side unexpectedly depends on beta")
    return {
        "F": "(6+4*t)/(1+2*t-t^2)",
        "F_prime": "4*(t^2+3*t-2)/(1+2*t-t^2)^2",
        "endpoint_layout_side_identity": True,
        "beta_independent": True,
        "monotone_box": "[F(t_hi),F(t_lo)]",
        "all_root_upper_excess": "cap-side.lo",
        "interval_overlap_used_as_identity": False,
    }


def symbolic_packet() -> dict[str, Any]:
    return copy.deepcopy(_symbolic_packet())


def finite_bounds(
    t: exact.Interval,
    consumer_side: exact.Interval,
    *,
    cap: Q = CAP,
    outer_cap: Q = OUTER_CAP,
    epsilon: Q = EPSILON,
) -> dict[str, Any]:
    """General exact arithmetic helper; certificate acceptance freezes its constants."""
    lo, hi = t
    side_lo, side_hi = consumer_side
    exact.require(lo <= hi and side_lo <= side_hi, "unordered root or consumer interval")
    exact.require(epsilon > 0, "nonpositive excess allowance")
    square = exact.multiply(t, t)
    denominator = exact.add(
        exact.point(1), exact.multiply(exact.point(2), t), exact.negate(square)
    )
    derivative_numerator = exact.multiply(
        exact.point(4), exact.add(square, exact.multiply(exact.point(3), t), exact.point(-2))
    )
    guards = {
        "positive_ordered_root_below_one": 0 < lo <= hi < 1,
        "denominator_positive": denominator[0] > 0,
        "derivative_numerator_strictly_negative": derivative_numerator[1] < 0,
        "cap_within_outer_cover": 0 < cap <= outer_cap,
    }
    result: dict[str, Any] = {
        "t": [str(lo), str(hi)],
        "denominator_enclosure": [str(value) for value in denominator],
        "derivative_numerator_enclosure": [str(value) for value in derivative_numerator],
        "consumer_side_enclosure": [str(side_lo), str(side_hi)],
        "monotone_side_enclosure": None,
        "excess": None,
        "guards": guards,
        "cap_certified": False,
    }
    if not all(guards.values()):
        return result
    lower, upper = formula(hi), formula(lo)
    exact.require(lower <= upper, "monotone side bracket differs")
    # Preserve the actual outward consumer enclosure; do not replace it with
    # the tighter monotone box or accept mere overlap between the two.
    guards["consumer_encloses_monotone_box"] = side_lo <= lower <= upper <= side_hi
    gaps = {
        "monotone_minimum_excess": cap - upper,
        "monotone_maximum_excess": cap - lower,
        "consumer_minimum_excess": cap - side_hi,
        "consumer_maximum_excess": cap - side_lo,
    }
    guards["strictly_above_both_side_upper_endpoints"] = (
        gaps["monotone_minimum_excess"] > 0 and gaps["consumer_minimum_excess"] > 0
    )
    guards["both_all_root_excesses_within_allowance"] = (
        gaps["monotone_maximum_excess"] <= epsilon
        and gaps["consumer_maximum_excess"] <= epsilon
    )
    result["monotone_side_enclosure"] = [str(lower), str(upper)]
    result["excess"] = {name: str(value) for name, value in gaps.items()}
    result["cap_certified"] = all(guards.values())
    return result


def load_inputs(path: Path) -> tuple[dict[str, Any], exact.Interval]:
    inputs, layout, _ = root_loader.load_root(path)
    exact.require(inputs["root_verification_passed"] is True, "root prerequisite refused")
    return inputs, layout.side


def generate(path: Path = root_loader.ROOT_PATH) -> dict[str, Any]:
    inputs, side = load_inputs(path)
    t = exact.read_interval(inputs["root_inclusion_box_used"][0])
    return {
        "schema": SCHEMA,
        "inputs": copy.deepcopy(inputs),
        "constants": dict(CONSTANTS),
        "symbolic": symbolic_packet(),
        "finite": finite_bounds(t, side),
        "scope": SCOPE,
        **FALSE_FLAGS,
    }


def check(document: dict[str, Any], path: Path = root_loader.ROOT_PATH) -> dict[str, Any]:
    expected = generate(path)
    payload = {
        key: value
        for key, value in document.items()
        if key not in {"checker", "provenance", "execution"}
    }
    exact.require(
        exact.exact_structure(payload, expected), "cap certificate or root custody differs"
    )
    certified = expected["finite"]["cap_certified"]
    return {
        "schema": SCHEMA,
        "verification_passed": True,
        "cap_certified": certified,
        "status": "numeric_capture_cap_certified" if certified else "inconclusive",
        "scope": SCOPE,
        **FALSE_FLAGS,
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
        packet["execution"] = {
            "argv": list(argv) if argv is not None else sys.argv[1:],
            "python": sys.version,
            "sympy": sp.__version__,
        }
        packet["provenance"] = provenance(
            Path(__file__),
            Path(root_loader.__file__),
            Path(root_loader.root.__file__),
            Path(exact.__file__),
            Path(endpoint.__file__),
            Path(inspect.getfile(root_loader.Dyadic)),
        )
    except (ValueError, OSError, KeyError, TypeError, IndexError) as error:
        packet = {
            "schema": SCHEMA,
            "status": "refused",
            "verification_passed": False,
            "cap_certified": False,
            "error": str(error),
            "scope": SCOPE,
            **FALSE_FLAGS,
        }
        result = packet
    if args.output is not None:
        args.output.write_text(retained_json.dumps(packet))
    print(json.dumps(result))
    return 0 if result["cap_certified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
