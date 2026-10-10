"""Replay one exact all-owner n17 angle patch from a retained numerical dual seed.

No LP solver is called. A positive strict interval margin certifies only the declared
closed patch on the fixed root-side container and stated slider/position domain.
The five failed patch attempts remain unresolved, never feasible-packing evidence.
Importing this module reads no scientific inputs.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections.abc import Mapping
from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from devtools import audit_n17_endpoint_receipt as exact
from devtools import check_n17_widened_apex as apex
from devtools import check_n17_widened_features as forcing
from devtools import probe_n17_widened_lp as probe
from devtools.check_n17_core_stress import Dyadic
from devtools.check_n17_endpoint_feasibility import Box
from devtools.provenance import provenance
from sqpack import retained_json

SCHEMA = "n17-widened-annulus-patch/v1"
LABELS = tuple(label for label in range(1, 18) if label != 6)
RHO, OUTER = Q(1, 100), Q(1, 200)
BITS = 44
LADDER = (20, 22, 24, 26, 28)
SEED_ID = "target:outer:coordinate:16:-1"
SEED_RUN = exact.REPO / exact.RESULTS / "exp-260-widened-lp-reconnaissance/run.json"
MAX_SEED_BYTES = 32 * 1024 * 1024
SCOPE = (
    "one closed 16-angle patch, all 256 selected owner branches; "
    "no complete annulus or global claim"
)

type Vector = tuple[Box, Box]


@dataclass(frozen=True)
class Row:
    name: str
    coefficients: tuple[Box, ...]
    rhs: Box
    options: tuple[str, ...] = ()


def point(value: int | Q) -> Dyadic:
    return Dyadic.point(value)


def dot(left: Vector, right: Vector) -> Box:
    return left[0] * right[0] + left[1] * right[1]


def square(value: Dyadic) -> Dyadic:
    lower = Q(0) if value.lo <= 0 <= value.hi else min(value.lo**2, value.hi**2)
    return Dyadic.enclose(lower, max(value.lo**2, value.hi**2))


def rotate(basis: tuple[Vector, Vector], turn: Dyadic) -> tuple[Vector, Vector]:
    denominator = 1 + square(turn)
    cosine, sine = (1 - square(turn)) / denominator, 2 * turn / denominator
    u, v = basis
    return (
        (cosine * u[0] + sine * v[0], cosine * u[1] + sine * v[1]),
        (-sine * u[0] + cosine * v[0], -sine * u[1] + cosine * v[1]),
    )


def support(basis: tuple[Vector, Vector], normal: Vector) -> Box:
    return (dot(normal, basis[0]).absolute() + dot(normal, basis[1]).absolute()) / 2


def hull(values: list[Box]) -> Dyadic:
    exact.require(values, "empty owner hull")
    return Dyadic.enclose(min(value.lo for value in values), max(value.hi for value in values))


def hull_rows(rows: list[Row], name: str) -> Row:
    exact.require(
        rows and all(len(row.coefficients) == 32 for row in rows), "wrong pair hull width"
    )
    return Row(
        name,
        tuple(hull([row.coefficients[j] for row in rows]) for j in range(32)),
        hull([row.rhs for row in rows]),
        tuple(row.name for row in rows),
    )


def column(label: int, axis: int) -> int:
    return 2 * LABELS.index(label) + axis


def row(name: str, entries: dict[int, Box], rhs: Box, options: tuple[str, ...] = ()) -> Row:
    return Row(name, tuple(entries.get(j, point(0)) for j in range(32)), rhs, options)


def nominal(layout: exact.Layout, label: int) -> tuple[Vector, Vector]:
    axes = tuple(
        (Dyadic.enclose(*layout.axes[name][0]), Dyadic.enclose(*layout.axes[name][1]))
        for name in forcing.features.basis_names(label)
    )
    return axes[0], axes[1]


def pair_row(feature: probe.Feature, bases: Mapping[int, tuple[Vector, Vector]]) -> Row:
    normal = tuple(feature.sign * value for value in bases[feature.owner][feature.axis])
    entries = {column(feature.left, j): -value for j, value in enumerate(normal)}
    entries.update({column(feature.right, j): value for j, value in enumerate(normal)})
    direction = normal[0], normal[1]
    return row(
        feature.name,
        entries,
        support(bases[feature.left], direction) + support(bases[feature.right], direction),
    )


def build_rows(layout: exact.Layout, box: tuple[exact.Interval, ...]) -> tuple[Row, ...]:
    exact.require(len(box) == 16, "wrong angle label count")
    bases = {
        label: rotate(nominal(layout, label), Dyadic.enclose(*turn))
        for label, turn in zip(LABELS, box, strict=True)
    }
    side = Dyadic.enclose(*layout.side)
    centres = {
        label: (Dyadic.enclose(*xy[0]), Dyadic.enclose(*xy[1]))
        for label, xy in layout.centres.items()
    }
    u, v = nominal(layout, 11)
    rows = []
    for label in LABELS:
        for coordinate, normal in enumerate(((point(1), point(0)), (point(0), point(1)))):
            extent = support(bases[label], normal)
            rows.extend(
                (
                    row(
                        f"wall:{label}:{coordinate}:lower",
                        {column(label, coordinate): point(1)},
                        extent,
                    ),
                    row(
                        f"wall:{label}:{coordinate}:upper",
                        {column(label, coordinate): point(-1)},
                        extent - side,
                    ),
                )
            )

    def interval(label: int, normal: Vector, low: Q, high: Q, name: str) -> None:
        origin = dot(normal, centres[label])
        entries = {column(label, j): value for j, value in enumerate(normal)}
        rows.extend(
            (
                row(
                    f"{name}:upper", {j: -value for j, value in entries.items()}, -origin - high
                ),
                row(f"{name}:lower", entries, origin + low),
            )
        )

    interval(5, (point(-1), point(0)), Q(0), Q(1, 4), "slider:a")
    interval(11, (-v[0], -v[1]), Q(-1, 2500), Q(1, 12), "slider:b")
    interval(13, v, Q(-1, 8), Q(1, 16), "slider:z")
    interval(5, (point(0), point(1)), -RHO, RHO, "tube:5:y")
    interval(11, u, -RHO, RHO, "tube:11:u")
    interval(13, u, -RHO, RHO, "tube:13:u")
    for label in LABELS:
        if label not in {5, 11, 13}:
            interval(label, (point(1), point(0)), -RHO, RHO, f"tube:{label}:x")
            interval(label, (point(0), point(1)), -RHO, RHO, f"tube:{label}:y")
    for group in probe.feature_groups():
        options = [pair_row(feature, bases) for feature in group]
        rows.append(hull_rows(options, f"pair:{group[0].left}:{group[0].right}"))
    exact.require(
        len(rows) == 147 and len({item.name for item in rows}) == 147,
        "wrong physical row roster",
    )
    return tuple(rows)


def round_weight(value: Q) -> Q:
    exact.require(type(value) is Q and value >= 0, "negative or inexact seed multiplier")
    scaled = value * 2**BITS + Q(1, 2)
    return Q(scaled.numerator // scaled.denominator, 2**BITS)


def decimal_rational(value: Any) -> Q:
    """Bound decimal expansion before constructing arbitrary-size rational integers."""
    exact.require(type(value) in (Decimal, int), "seed number must preserve decimal token")
    if type(value) is int:
        exact.require(
            value.bit_length() <= exact.MAX_DIGITS * 3,
            "oversized seed integer",
        )
        return Q(value)
    exact.require(value.is_finite(), "nonfinite seed decimal")
    _, digits, exponent = value.as_tuple()
    exact.require(
        type(exponent) is int
        and len(digits) <= exact.MAX_DIGITS
        and exponent > -exact.MAX_DIGITS
        and exponent + len(digits) <= exact.MAX_DIGITS,
        "oversized seed decimal expansion",
    )
    return Q(value)


def seed_from_receipt(packet: dict[str, Any]) -> dict[str, Any]:
    matches = [alias for alias in packet["point_aliases"] if alias["id"] == SEED_ID]
    exact.require(len(matches) == 1, "missing or duplicate seed point")
    alias = matches[0]
    exact.require(
        type(alias["outcome_index"]) is int
        and 0 <= alias["outcome_index"] < len(packet["points"]),
        "invalid seed point outcome index",
    )
    result = packet["points"][alias["outcome_index"]]
    exact.require(
        result["profile"] == "bounded_tube"
        and result["execution_complete"] is True
        and result["status"] == "complete_numerical",
        "seed numerical execution incomplete",
    )
    expected_turns = [Q(-OUTER) if label == 16 else Q(0) for label in LABELS]
    exact.require(
        [exact.rational(value) for value in result["half_angle_turns"]] == expected_turns,
        "wrong seed turn vector",
    )
    branches = result["branches"]
    exact.require(
        all(type(branch["branch_id"]) is int for branch in branches)
        and len(branches) == 256
        and {branch["branch_id"] for branch in branches} == set(range(256)),
        "seed raw branch coverage differs",
    )
    candidates = []
    for branch in branches:
        exact.require(
            branch["status"] in {"numerically_optimal", "numerically_infeasible"},
            "nonterminal seed branch",
        )
        if branch["status"] == "numerically_optimal":
            exact.require(
                type(branch["outcome_index"]) is int
                and 0 <= branch["outcome_index"] < len(result["outcomes"]),
                "invalid seed branch outcome index",
            )
            outcome = result["outcomes"][branch["outcome_index"]]
            exact.require(
                outcome["status"] == "numerically_optimal", "seed branch outcome mismatch"
            )
            token = outcome["diagnostics"]["primal_value"]
            value = decimal_rational(token)
            candidates.append((value, branch["branch_id"], outcome))
    exact.require(candidates, "seed has no optimal numerical branch")
    _, branch_id, outcome = min(candidates, key=lambda item: (item[0], item[1]))
    combinations = tuple(itertools.product(*probe.feature_groups()))
    choices = combinations[branch_id]
    common_ids = [
        f"wall:{label}:{coordinate}:{suffix}"
        for label in LABELS
        for coordinate in (0, 1)
        for suffix in ("lower", "upper")
    ]
    common_ids.extend(
        f"slider:{name}:{suffix}" for name in ("a", "b", "z") for suffix in ("upper", "lower")
    )
    tubes = ["tube:5:y", "tube:11:u", "tube:13:u"] + [
        f"tube:{label}:{axis}"
        for label in LABELS
        if label not in {5, 11, 13}
        for axis in ("x", "y")
    ]
    common_ids.extend(f"{name}:{suffix}" for name in tubes for suffix in ("upper", "lower"))
    expected_ids = common_ids + [feature.name for feature in choices]
    # An aliased solve may have another owner's row IDs. Bind to the representative's
    # actual owner choices before retaining its weights; coverage uses fresh owner hulls.
    representative = outcome["representative_branch"]
    exact.require(
        type(representative) is int and 0 <= representative < 256,
        "invalid representative branch",
    )
    representative_ids = common_ids + [feature.name for feature in combinations[representative]]
    exact.require(outcome["row_ids"] == representative_ids, "seed row order differs")
    weights = tuple(round_weight(decimal_rational(value)) for value in outcome["multipliers"])
    exact.require(len(weights) == 147, "seed multiplier count differs")
    return {
        "point_id": SEED_ID,
        "selected_raw_branch": branch_id,
        "representative_branch": representative,
        "selected_raw_row_ids": expected_ids,
        "seed_row_ids": representative_ids,
        "primal_value_decimal": str(outcome["diagnostics"]["primal_value"]),
        "weights": [str(value) for value in weights],
        "half_angle_turns": [str(value) for value in expected_turns],
        "rounding": "nearest nonnegative 2^-44, ties upward from exact recorded decimal tokens",
    }


def patch_box(seed: list[Q], bits: int) -> tuple[exact.Interval, ...]:
    exact.require(bits in LADDER and len(seed) == 16, "changed patch ladder or labels")
    width = Q(1, 2**bits)
    return tuple((max(-OUTER, value - width), min(OUTER, value + width)) for value in seed)


def evaluate(
    rows: tuple[Row, ...], weights: tuple[Q, ...], layout: exact.Layout
) -> dict[str, Any]:
    exact.require(
        len(rows) == len(weights) and all(weight >= 0 for weight in weights),
        "bad patch multipliers",
    )
    a = tuple(
        sum(
            (
                weight * item.coefficients[j]
                for weight, item in zip(weights, rows, strict=True)
                if weight
            ),
            point(0),
        )
        for j in range(32)
    )
    d = sum(
        (weight * item.rhs for weight, item in zip(weights, rows, strict=True) if weight),
        point(0),
    )
    vertices = []
    for vertex in forcing.vertices():
        centres = forcing.shifted(layout, vertex)
        flat = tuple(
            Dyadic.enclose(*interval) for label in LABELS for interval in centres[label]
        )
        value = d - sum(
            (coefficient * coordinate for coefficient, coordinate in zip(a, flat, strict=True)),
            point(0),
        )
        vertices.append(
            {
                "vertex": [str(value) for value in vertex],
                "interval": [str(value.lo), str(value.hi)],
            }
        )
    u = nominal(layout, 11)[0]
    residuals = []
    for name in apex.position_names():
        kind, label_text = name.rstrip("0123456789"), name[len(name.rstrip("0123456789")) :]
        label = int(label_text)
        value = (
            dot((a[column(label, 0)], a[column(label, 1)]), u)
            if kind == "u"
            else a[column(label, 0 if kind == "xi" else 1)]
        )
        residuals.append([str(value.lo), str(value.hi)])
    penalty = RHO * sum((max(abs(Q(lo)), abs(Q(hi))) for lo, hi in residuals), Q(0))
    eta = min(Q(item["interval"][0]) for item in vertices) - penalty
    return {
        "weighted_A": [[str(value.lo), str(value.hi)] for value in a],
        "weighted_b": [str(d.lo), str(d.hi)],
        "slider_vertices": vertices,
        "position_residual_intervals": residuals,
        "residual_penalty": str(penalty),
        "eta": str(eta),
        "passed": eta > 0,
    }


def load_inputs(
    feature_path: Path, apex_path: Path
) -> tuple[dict[str, Any], exact.Layout, dict[str, Any], Q]:
    feature_packet = exact.decode(exact.read_bytes(feature_path))
    forcing.check(feature_packet)
    apex_packet = exact.decode(exact.read_bytes(apex_path))
    apex.check(apex_packet, feature_path)
    inputs, layout, _ = forcing.load_root()
    with SEED_RUN.open("rb") as stream:
        raw = stream.read(MAX_SEED_BYTES + 1)
    exact.require(len(raw) <= MAX_SEED_BYTES, "seed receipt exceeds 32 MiB")
    receipt = json.loads(
        raw,
        parse_float=Decimal,
        parse_int=exact.json_integer,
        parse_constant=exact.reject_constant,
        object_pairs_hook=exact.duplicate_refusal,
    )
    exact.require(
        receipt["root_input"] == str(forcing.ROOT_PATH.relative_to(exact.REPO)),
        "seed root path differs",
    )
    exact.require(
        receipt["nominal_root_midpoint"]["t"] == inputs["root_search_box"]["midpoint"][0]
        and receipt["nominal_root_midpoint"]["beta"]
        == inputs["root_search_box"]["midpoint"][1],
        "seed root midpoint differs",
    )
    return (
        {
            "root": inputs,
            "features": str(feature_path.resolve().relative_to(exact.REPO)),
            "apex": str(apex_path.resolve().relative_to(exact.REPO)),
            "seed_receipt": str(SEED_RUN.relative_to(exact.REPO)),
            "rho": str(RHO),
            "outer_half_angle_radius": str(OUTER),
            "slider_box": [[str(lo), str(hi)] for lo, hi in forcing.DOMAIN],
            "labels": list(LABELS),
            "position_columns": list(apex.position_names()),
            "branch_coverage": 256,
        },
        layout,
        seed_from_receipt(receipt),
        Q(apex_packet["q0"]),
    )


def generate(feature_path: Path, apex_path: Path) -> dict[str, Any]:
    inputs, layout, seed, q0 = load_inputs(feature_path, apex_path)
    centre = [Q(value) for value in seed["half_angle_turns"]]
    weights = tuple(Q(value) for value in seed["weights"])
    attempts = []
    for bits in LADDER:
        box = patch_box(centre, bits)
        exact.require(
            all(-OUTER <= lo < hi <= OUTER for lo, hi in box), "patch outside outer cube"
        )
        distance = max(Q(0) if lo <= 0 <= hi else min(abs(lo), abs(hi)) for lo, hi in box)
        exact.require(distance >= q0, "patch intersects unexcluded apex interior")
        rows = build_rows(layout, box)
        result = evaluate(rows, weights, layout)
        attempts.append(
            {
                "h_bits": bits,
                "angle_box": [[str(lo), str(hi)] for lo, hi in box],
                "pair_options": [list(item.options) for item in rows[-19:]],
                "row_ids": [item.name for item in rows],
                **result,
            }
        )
        if result["passed"]:
            break
    return {
        "schema": SCHEMA,
        "inputs": inputs,
        "seed": seed,
        "apex_q0": str(q0),
        "ladder": list(LADDER),
        "attempts": attempts,
        "status": "certified_patch" if attempts[-1]["passed"] else "inconclusive",
        "scope": SCOPE,
    }


def check(packet: dict[str, Any], feature_path: Path, apex_path: Path) -> dict[str, Any]:
    expected = generate(feature_path, apex_path)
    exact.require(
        exact.exact_structure({name: packet[name] for name in expected}, expected),
        "patch certificate differs from exact replay",
    )
    return {
        "schema": "n17-widened-annulus-patch-check/v1",
        "verification_passed": True,
        "status": expected["status"],
        "positive_patch_certified": expected["status"] == "certified_patch",
        "eta": expected["attempts"][-1]["eta"],
        "scope": SCOPE,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--features", type=Path, required=True)
    parser.add_argument("--apex", type=Path, required=True)
    parser.add_argument("--certificate", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        packet = (
            generate(args.features, args.apex)
            if args.certificate is None
            else exact.decode(exact.read_bytes(args.certificate))
        )
        result = check(packet, args.features, args.apex)
        packet["checker"] = result
        packet["provenance"] = provenance(
            Path(__file__),
            Path(forcing.__file__),
            Path(apex.__file__),
            Path(probe.__file__),
            Path(exact.__file__),
            Path(apex.local.__file__),
            Path(apex.endpoint.__file__),
            Path(forcing.core.__file__),
            Path(forcing.root.__file__),
            Path(forcing.features.__file__),
        )
    except (ValueError, OSError, KeyError, TypeError) as error:
        packet = {"schema": SCHEMA, "verification_passed": False, "error": str(error)}
        result = packet
    if args.output is not None:
        args.output.write_text(retained_json.dumps(packet))
    print(json.dumps(result))
    return 0 if result.get("verification_passed") is True else 1


if __name__ == "__main__":
    raise SystemExit(main())
