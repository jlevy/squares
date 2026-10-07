"""Recompute a conditional, exact n17 omitted-feature forcing certificate.

One fixed corner upper-bounds each omitted support gap. Every slider vertex is
checked across the entire accepted root interval. No capture or side-bound claim is
made. Importing this module reads no scientific inputs.
"""

from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, cast

from devtools import audit_n17_endpoint_features as features
from devtools import audit_n17_endpoint_receipt as exact
from devtools import check_n17_core_stress as core
from devtools import check_n17_root_certificate as root
from devtools.check_n17_core_stress import Dyadic
from devtools.provenance import provenance
from sqpack import retained_json

SCHEMA = "n17-widened-feature-certificate/v1"
CONVENTION = "owner-other displacement; sign flips when owner is right endpoint"
DOMAIN = ((Q(0), Q(1, 4)), (Q(-1, 2500), Q(1, 12)), (Q(-1, 8), Q(1, 16)))
CORNERS = ((1, 1), (1, -1), (-1, 1), (-1, -1))
DROPPED = {(2, 3), (9, 11)}
ROOT_PATH = exact.REPO / exact.ROOT_RUN / "certificate.json"
CONSTANTS = {
    "position_radius": "1/100",
    "half_angle_radius": "1/200",
    "angle_upper": "1/100",
    "distance_upper": "4/3",
    "nominal_gap_upper": "-11/200",
    "sqrt2_upper": "99/70",
}
SCOPE = (
    "conditional omitted-feature forcing only; "
    "capture, slider coverage and side lower bound unproved"
)


def roster() -> tuple[dict[str, Any], ...]:
    """All 125 omitted identities, derived independently of the LP allowed list."""
    options = tuple(
        option
        for option in features.expected_options()
        if option["kind"] != "identity" and (option["left"], option["right"]) not in DROPPED
    )
    exact.require(len(options) == 125, "omitted feature roster differs")
    return options


def vertices() -> tuple[tuple[Q, Q, Q], ...]:
    return tuple(itertools.product(*DOMAIN))


def shifted(layout: exact.Layout, vertex: tuple[Q, Q, Q]) -> dict[int, exact.Vector]:
    """Independent tuple-interval transcription of the retained slider family."""
    a, b, z = vertex
    centres = dict(layout.centres)
    centres[5] = (exact.subtract(centres[5][0], exact.point(a)), centres[5][1])
    for label, slide in ((11, -b), (13, z)):
        moved = tuple(
            exact.add(coordinate, exact.multiply(exact.point(slide), axis))
            for coordinate, axis in zip(centres[label], layout.axes["v"], strict=True)
        )
        centres[label] = moved[0], moved[1]
    return centres


def corner_gap(
    layout: exact.Layout,
    centres: dict[int, exact.Vector],
    option: dict[str, Any],
    corner: tuple[int, int],
) -> exact.Interval:
    """Fixed-corner upper bound of the full owner-axis separation gap."""
    left, right, owner = (option[name] for name in ("left", "right", "owner"))
    other = right if owner == left else left
    sign = option["sign"] if owner == left else -option["sign"]
    first, second = (layout.axes[name] for name in features.basis_names(other))
    offset = tuple(
        exact.divide(
            exact.add(
                exact.multiply(exact.point(corner[0]), first[axis]),
                exact.multiply(exact.point(corner[1]), second[axis]),
            ),
            exact.point(2),
        )
        for axis in (0, 1)
    )
    displacement = tuple(
        exact.add(value, delta)
        for value, delta in zip(
            exact.difference(centres[other], centres[owner]), offset, strict=True
        )
    )
    return exact.subtract(
        exact.multiply(
            exact.point(sign),
            exact.dot(layout.axes[option["axis"]], (displacement[0], displacement[1])),
        ),
        exact.point(Q(1, 2)),
    )


def distance_squared(centres: dict[int, exact.Vector], pair: tuple[int, int]) -> exact.Interval:
    displacement = exact.difference(centres[pair[1]], centres[pair[0]])
    return exact.add(*(root.power(value, 2) for value in displacement))


def analytic_margin(constants: dict[str, Any]) -> Q:
    """Astra's rational Lipschitz bound; 2 atan(q) <= 2 q supplies the angle bound."""
    exact.require(set(constants) == set(CONSTANTS), "wrong analytic constants")
    rho, half_angle, angle, distance, gap, sqrt2 = (
        exact.rational(constants[name])
        for name in (
            "position_radius",
            "half_angle_radius",
            "angle_upper",
            "distance_upper",
            "nominal_gap_upper",
            "sqrt2_upper",
        )
    )
    exact.require(rho > 0 and half_angle > 0 and distance > 0, "nonpositive radius or distance")
    exact.require(angle >= 2 * half_angle, "angle bound does not enclose half-angle turns")
    exact.require(sqrt2 > 0 and sqrt2 * sqrt2 > 2, "invalid square-root bound")
    return gap + 2 * sqrt2 * rho + (distance + 1) * angle


def rounded_layout(layout: exact.Layout) -> exact.Layout:
    """Outward grid enclosure keeps retained rational bounds small and replayable."""

    def rounded(value: exact.Interval) -> exact.Interval:
        interval = Dyadic.enclose(*value)
        return interval.lo, interval.hi

    def vector(value: exact.Vector) -> exact.Vector:
        return rounded(value[0]), rounded(value[1])

    return exact.Layout(
        {label: vector(value) for label, value in layout.centres.items()},
        {name: vector(value) for name, value in layout.axes.items()},
        layout.guards,
        layout.sliders,
        rounded(layout.side),
    )


def load_root(path: Path = ROOT_PATH) -> tuple[dict[str, Any], exact.Layout, exact.Layout]:
    """Verify H255 afresh, then enclose its certified inclusion box on the 2^-256 grid."""
    document = exact.decode(exact.read_bytes(path))
    checked = root.check(document, exact.read_bytes(exact.REPO / root.SOURCE_PATH))
    exact.require(checked["verification_passed"] is True, "root certificate not accepted")
    midpoint = tuple(root.rational(value) for value in document["box"]["midpoint"])
    radii = tuple(root.rational(value) for value in checked["inclusion_bounds"])
    intervals = tuple(
        Dyadic.enclose(value - radius, value + radius)
        for value, radius in zip(midpoint, radii, strict=True)
    )
    layout = rounded_layout(exact.reconstruct(*((value.lo, value.hi) for value in intervals)))
    nominal = exact.reconstruct(*(exact.point(value) for value in midpoint))
    inputs = {
        "root_path": str(path.resolve().relative_to(exact.REPO)),
        "root_reference": exact.ROOT_REF,
        "root_search_box": document["box"],
        "root_inclusion_box_used": [[str(value.lo), str(value.hi)] for value in intervals],
        "root_verification_passed": True,
    }
    return inputs, layout, nominal


def encode(interval: exact.Interval) -> list[str]:
    return [str(value) for value in interval]


def generate(path: Path = ROOT_PATH) -> dict[str, Any]:
    inputs, layout, nominal = load_root(path)
    options = roster()
    pairs = sorted({(option["left"], option["right"]) for option in options})
    scenes = [shifted(layout, vertex) for vertex in vertices()]
    origin = shifted(nominal, (Q(0), Q(0), Q(0)))
    distances = [
        {
            "pair": list(pair),
            "vertices": [
                {
                    "vertex": [str(x) for x in vertex],
                    "squared_interval": encode(distance_squared(scene, pair)),
                }
                for vertex, scene in zip(vertices(), scenes, strict=True)
            ],
        }
        for pair in pairs
    ]
    rows = []
    for option in options:
        corner = min(CORNERS, key=lambda choice: corner_gap(nominal, origin, option, choice)[1])
        rows.append(
            {
                "option": option,
                "corner": list(corner),
                "vertices": [
                    {
                        "vertex": [str(x) for x in vertex],
                        "gap_interval": encode(corner_gap(layout, scene, option, corner)),
                    }
                    for vertex, scene in zip(vertices(), scenes, strict=True)
                ],
            }
        )
    return {
        "schema": SCHEMA,
        "convention": CONVENTION,
        "inputs": inputs,
        "slider_box": [[str(lo), str(hi)] for lo, hi in DOMAIN],
        "constants": dict(CONSTANTS),
        "final_margin": str(analytic_margin(CONSTANTS)),
        "distances": distances,
        "features": rows,
        "scope": SCOPE,
    }


def match_vertices(rows: Any, field: str) -> dict[tuple[Q, Q, Q], exact.Interval]:
    exact.require(type(rows) is list and len(rows) == 8, "missing or extra slider vertex")
    result = {}
    for row in cast(list[dict[str, Any]], rows):
        exact.require(
            type(row) is dict and set(row) == {"vertex", field}, "wrong vertex fields"
        )
        values = tuple(exact.rational(value) for value in row["vertex"])
        exact.require(len(values) == 3, "wrong vertex dimension")
        vertex = values[0], values[1], values[2]
        exact.require(
            vertex in vertices() and vertex not in result, "invalid or duplicate vertex"
        )
        result[vertex] = exact.read_interval(row[field])
    return result


def check(packet: dict[str, Any], path: Path = ROOT_PATH) -> dict[str, Any]:
    """Reconstruct geometry from accepted root data; never trust reported intervals."""
    exact.require(
        packet["schema"] == SCHEMA and packet["convention"] == CONVENTION, "wrong contract"
    )
    exact.require(packet["scope"] == SCOPE, "wrong certificate scope")
    exact.require(
        packet["slider_box"] == [[str(lo), str(hi)] for lo, hi in DOMAIN], "wrong slider domain"
    )
    inputs, layout, _ = load_root(path)
    exact.require(exact.exact_structure(packet["inputs"], inputs), "wrong accepted root input")
    constants = packet["constants"]
    margin = analytic_margin(constants)
    exact.require(
        exact.rational(packet["final_margin"]) == margin and margin < 0,
        "nonnegative or wrong forcing margin",
    )
    exact.require(exact.exact_structure(constants, CONSTANTS), "changed frozen analytic region")
    distance = exact.rational(constants["distance_upper"])
    gap = exact.rational(constants["nominal_gap_upper"])
    expected = {features.pair_key(option): option for option in roster()}
    pairs = {(option["left"], option["right"]) for option in expected.values()}
    scenes = {vertex: shifted(layout, vertex) for vertex in vertices()}
    exact.require(
        type(packet["distances"]) is list and len(packet["distances"]) == 19,
        "wrong distance count",
    )
    seen_pairs = set()
    for row in cast(list[dict[str, Any]], packet["distances"]):
        exact.require(set(row) == {"pair", "vertices"}, "wrong distance fields")
        values = tuple(row["pair"])
        exact.require(
            len(values) == 2 and all(type(x) is int for x in values), "invalid pair labels"
        )
        pair = values[0], values[1]
        exact.require(pair in pairs and pair not in seen_pairs, "invalid or duplicate pair")
        seen_pairs.add(pair)
        for vertex, reported in match_vertices(row["vertices"], "squared_interval").items():
            actual = distance_squared(scenes[vertex], pair)
            exact.require(
                reported[0] <= actual[0] <= actual[1] <= reported[1] <= distance * distance,
                "distance enclosure or bound failed",
            )
    exact.require(
        type(packet["features"]) is list and len(packet["features"]) == 125,
        "wrong feature count",
    )
    seen_options = set()
    for row in cast(list[dict[str, Any]], packet["features"]):
        exact.require(set(row) == {"option", "corner", "vertices"}, "wrong feature fields")
        option = row["option"]
        key = features.pair_key(option)
        exact.require(
            key in expected and key not in seen_options, "invalid or duplicate feature"
        )
        exact.require(exact.exact_structure(option, expected[key]), "feature identity differs")
        seen_options.add(key)
        values = tuple(row["corner"])
        exact.require(
            all(type(x) is int for x in values) and values in CORNERS, "invalid corner"
        )
        corner = values[0], values[1]
        for vertex, reported in match_vertices(row["vertices"], "gap_interval").items():
            actual = corner_gap(layout, scenes[vertex], option, corner)
            exact.require(
                reported[0] <= actual[0] <= actual[1] <= reported[1] <= gap,
                "corner enclosure or nominal bound failed",
            )
    return {
        "schema": "n17-widened-feature-check/v1",
        "verification_passed": True,
        "pairs": 19,
        "features": 125,
        "vertices_per_row": 8,
        "final_margin": str(margin),
        "scope": packet["scope"],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--certificate", type=Path, help="check a retained certificate instead of producing one"
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        packet = (
            generate()
            if args.certificate is None
            else exact.decode(exact.read_bytes(args.certificate))
        )
        result = check(packet)
        packet["checker"] = result
        packet["provenance"] = provenance(
            Path(__file__),
            Path(exact.__file__),
            Path(features.__file__),
            Path(root.__file__),
            Path(core.__file__),
        )
    except (ValueError, OSError, KeyError, TypeError) as error:
        packet = {"schema": SCHEMA, "verification_passed": False, "error": str(error)}
        if args.output is not None:
            args.output.write_text(retained_json.dumps(packet))
        print(json.dumps(packet))
        return 1
    if args.output is not None:
        args.output.write_text(retained_json.dumps(packet))
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
