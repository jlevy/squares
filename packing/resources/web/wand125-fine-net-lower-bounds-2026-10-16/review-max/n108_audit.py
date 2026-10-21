"""Independently recompute n108 input premises and selected exact captures.

This program does not decide universal coverage. It imports no project verifier.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import cast

type Json = bool | int | float | str | list[Json] | dict[str, Json] | None
type Point = tuple[Fraction, Fraction]
type Rectangle = tuple[Fraction, Fraction, Fraction, Fraction]

PACKET = Path("packing/resources/web/wand125-fine-net-lower-bounds-2026-10-16")
CERTIFICATE = "mixed_n108_L1062"


def obj(value: Json) -> dict[str, Json]:
    if not isinstance(value, dict):
        raise TypeError("Expected a JSON object")
    return value


def seq(value: Json) -> list[Json]:
    if not isinstance(value, list):
        raise TypeError("Expected a JSON array")
    return value


def rational(value: Json) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, str | int | float):
        raise TypeError("Expected a rational string or number")
    # Receipt coordinates are binary64 values; Fraction(float) preserves that pose.
    return Fraction(value)


def integer(value: Json) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("Expected an integer")
    return value


def unique_object(pairs: list[tuple[str, Json]]) -> dict[str, Json]:
    result: dict[str, Json] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def decode(data: bytes, *, exact_decimals: bool = False) -> Json:
    return cast(
        Json,
        json.loads(
            data,
            object_pairs_hook=unique_object,
            parse_float=str if exact_decimals else float,
        ),
    )


def read_json(path: Path) -> dict[str, Json]:
    return obj(decode(path.read_bytes()))


def json_lines(path: Path) -> list[dict[str, Json]]:
    return [obj(decode(line)) for line in gzip.decompress(path.read_bytes()).splitlines()]


def polynomial(t: Fraction) -> Fraction:
    return t * t + 2 * t - 1


def wall_radius(t: Fraction) -> Fraction:
    return (1 + 2 * t - t * t) / (2 * (1 + t * t))


def clip(polygon: list[Point], a: Fraction, b: Fraction, bound: Fraction) -> list[Point]:
    """Intersect a convex polygon with one closed rational half-plane."""
    if not polygon:
        return []
    output: list[Point] = []
    previous = polygon[-1]
    old = a * previous[0] + b * previous[1] - bound
    for current in polygon:
        new = a * current[0] + b * current[1] - bound
        if (old <= 0) != (new <= 0):
            fraction = old / (old - new)
            output.append(
                (
                    previous[0] + fraction * (current[0] - previous[0]),
                    previous[1] + fraction * (current[1] - previous[1]),
                )
            )
        if new <= 0:
            output.append(current)
        previous, old = current, new
    return output


def intersection_area(
    rectangle: Rectangle, centre: Point, t: Fraction, side: Fraction
) -> Fraction:
    left, bottom, right, top = rectangle
    x, y = centre
    cosine, sine = (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)
    half = side / 2
    extent = half * (abs(cosine) + abs(sine))
    if right <= x - extent or left >= x + extent or top <= y - extent or bottom >= y + extent:
        return Fraction(0)
    polygon: list[Point] = [(left, bottom), (right, bottom), (right, top), (left, top)]
    for a, b in ((cosine, sine), (-cosine, -sine), (-sine, cosine), (sine, -cosine)):
        polygon = clip(polygon, a, b, half + a * x + b * y)
    if len(polygon) < 3:
        return Fraction(0)
    return (
        abs(
            sum(
                (
                    p[0] * q[1] - q[0] * p[1]
                    for p, q in zip(polygon, [*polygon[1:], polygon[0]], strict=True)
                ),
                Fraction(0),
            )
        )
        / 2
    )


def expand(
    candidate: dict[str, Json], side: Fraction
) -> tuple[dict[Rectangle, Fraction], Fraction]:
    """Average eight images, retaining multiplicity when an orbit has a stabilizer."""
    densities: dict[Rectangle, Fraction] = {}
    mass = Fraction(0)
    for item in seq(candidate["rectangles"]):
        row = obj(item)
        coordinates = [rational(value) for value in seq(row["rectangle"])]
        if len(coordinates) != 4:
            raise ValueError("A rectangle needs four coordinates")
        left, bottom, right, top = coordinates
        weight = rational(row["mass"])
        if not (0 <= left < right <= side and 0 <= bottom < top <= side and weight > 0):
            raise ValueError("Invalid positive rectangle")
        mass += weight
        density = weight / (8 * (right - left) * (top - bottom))
        for swap in (False, True):
            x1, y1, x2, y2 = (bottom, left, top, right) if swap else (left, bottom, right, top)
            for flip_x in (False, True):
                for flip_y in (False, True):
                    lo_x, hi_x = (side - x2, side - x1) if flip_x else (x1, x2)
                    lo_y, hi_y = (side - y2, side - y1) if flip_y else (y1, y2)
                    key = (lo_x, lo_y, hi_x, hi_y)
                    densities[key] = densities.get(key, Fraction(0)) + density
    return densities, mass


def capture(
    densities: dict[Rectangle, Fraction], centre: Point, t: Fraction, side: Fraction
) -> Fraction:
    return sum(
        (
            density * intersection_area(rectangle, centre, t, side)
            for rectangle, density in densities.items()
        ),
        Fraction(0),
    )


def enclosure(value: Fraction) -> dict[str, Json]:
    denominator = 10**18
    floor = value.numerator * denominator // value.denominator
    return {
        "lower": str(Fraction(floor, denominator)),
        "upper": str(Fraction(floor + 1, denominator)),
    }


def geometry_controls() -> None:
    """Analytic areas check a rotated cut, boundary contact, and coincident orbits."""
    unit: Rectangle = (Fraction(0), Fraction(0), Fraction(1), Fraction(1))
    assert intersection_area(
        unit, (Fraction(1, 2), Fraction(1, 2)), Fraction(1, 3), Fraction(1, 2)
    ) == Fraction(1, 4)
    assert intersection_area(
        unit, (Fraction(1), Fraction(1, 2)), Fraction(0), Fraction(1)
    ) == Fraction(1, 2)
    assert (
        intersection_area(unit, (Fraction(3, 2), Fraction(1, 2)), Fraction(0), Fraction(1)) == 0
    )
    symmetric: dict[str, Json] = {"rectangles": [{"rectangle": [0, 0, 1, 1], "mass": "3/2"}]}
    densities, mass = expand(symmetric, Fraction(1))
    assert len(densities) == 1
    assert mass == Fraction(3, 2)
    assert (
        capture(densities, (Fraction(1, 2), Fraction(1, 2)), Fraction(0), Fraction(1)) == mass
    )


def receipt_inventory(rows: list[dict[str, Json]], expected: int) -> dict[str, Json]:
    directions = {integer(row["r"]): row for row in rows if "r" in row}
    summaries = [row for row in rows if row.get("kind") == "sqverify-fast-summary/v1"]
    counts = Counter(str(row["verdict"]) for row in rows if "r" in row)
    complete = (
        len(directions) == expected
        and set(directions) == set(range(expected))
        and sum(counts.values()) == expected
    )
    assert complete
    assert counts == {"verified": expected}
    assert len(summaries) == 1
    summary = summaries[0]
    assert summary["status"] == "VERIFIED"
    assert summary["threshold"] == "1"
    assert summary["fault_injected_at_box"] is None
    assert summary["refused_directions"] == []
    assert integer(summary["nodes"]) == sum(
        integer(row.get("nodes", 0)) for row in directions.values()
    )
    assert all(rational(row["min_certified_lower_bound"]) >= 1 for row in directions.values())
    return {
        "directions": expected,
        "complete_unique_indices": complete,
        "verdict_counts": dict(counts),
        "nodes": summary["nodes"],
        "build": summary["build"],
        "premises": summary["premises"],
        "min_reported_bound": str(
            min(rational(row["min_certified_lower_bound"]) for row in directions.values())
        ),
    }


def run(repo: Path) -> dict[str, Json]:
    geometry_controls()
    packet = repo / PACKET
    source = packet / "release/certificates" / CERTIFICATE
    candidate_path = source / "candidate.json.gz"
    compressed = candidate_path.read_bytes()
    raw = gzip.decompress(compressed)
    candidate = obj(decode(raw, exact_decimals=True))
    n, side, core = integer(candidate["n"]), rational(candidate["L"]), rational(candidate["B"])
    net = obj(candidate["proof_net"])
    step, last = rational(net["step"]), integer(net["last"])
    assert n == 108
    assert side == Fraction(531, 50)
    assert not seq(candidate["points"])
    assert not candidate.get("segments", [])
    densities, mass = expand(candidate, side)
    assert mass == rational(candidate["total_mass"])
    assert 0 < mass < n
    expanded_mass = sum(
        (
            density * (right - left) * (top - bottom)
            for (left, bottom, right, top), density in densities.items()
        ),
        Fraction(0),
    )
    assert expanded_mass == mass
    assert max(densities.values()) <= 2**96
    end = last * step
    last_lower = end - step / 2
    assert 0 < core < 1
    assert step > 0
    assert 1 <= last < 2**16
    assert end <= Fraction(1, 2)
    assert core * (1 + step) < 1
    assert polynomial(end) > 0
    assert polynomial(last_lower) < 0
    assert core * (1 + step / (1 - step * step / 4)) < 1
    assert side <= 1000
    assert side * side >= 2 * core * core
    domains = [
        wall_radius(max(Fraction(0), index * step - step / 2)) for index in range(last + 1)
    ]
    assert all(radius < side / 2 for radius in domains)
    census_dir = repo / "packing/benchmarks/measure-verifier/census-mixed"
    native_log = census_dir / packet.name / f"{CERTIFICATE}.jsonl.gz"
    source_rows = json_lines(source / "check2/run.jsonl.gz")
    native_rows = json_lines(native_log)
    source_inventory = receipt_inventory(source_rows, last + 1)
    native_inventory = receipt_inventory(native_rows, last + 1)
    raw_digest = hashlib.sha256(raw).hexdigest()
    compressed_digest = hashlib.sha256(compressed).hexdigest()
    assert obj(source_inventory["premises"])["input_sha256"] == raw_digest
    assert obj(native_inventory["premises"])["input_sha256"] == compressed_digest
    source_by_r = {integer(row["r"]): row for row in source_rows if "r" in row}
    native_by_r = {integer(row["r"]): row for row in native_rows if "r" in row}
    matching_nodes = sum(
        source_by_r[r].get("nodes", 0) == native_by_r[r].get("nodes", 0) for r in source_by_r
    )
    controls = read_json(census_dir / packet.name / f"{CERTIFICATE}.control.json")
    sweeps = [
        row for item in seq(controls["runs"]) if (row := obj(item))["name"] == "scaled-99-100"
    ]
    sweep = obj(sweeps[0]["sweep"])
    samples: list[Json] = []
    for item in seq(sweep["refused"]):
        row = obj(item)
        index = integer(row["r"])
        if index not in (1, 100, 157, 200):
            continue
        pose = seq(row["pose"])
        centre = (rational(pose[0]), rational(pose[1]))
        value = capture(densities, centre, index * step, core)
        scaled = value * Fraction(99, 100)
        in_domain = all(
            domains[index] <= coordinate <= side - domains[index] for coordinate in centre
        )
        assert in_domain
        assert value >= 1
        assert scaled < 1
        assert scaled == rational(row["capture"])
        samples.append(
            {
                "index": index,
                "pose_binary64_as_rationals": [str(part) for part in centre],
                "in_domain": in_domain,
                "original_capture_interval": enclosure(value),
                "scaled_capture_interval": enclosure(scaled),
                "agrees_exactly_with_retained_capture": True,
            }
        )
    assert len(samples) == 4
    source_controls = json_lines(source / "check2/control-197_200.jsonl.gz")
    axis_row = next(row for row in source_controls if row.get("r") == 0)
    axis_pose = seq(axis_row["argmin"])
    axis_centre = (rational(axis_pose[0]), rational(axis_pose[1]))
    axis_original = capture(densities, axis_centre, Fraction(0), core)
    axis_scaled = axis_original * Fraction(197, 200)
    assert all(domains[0] <= coordinate <= side - domains[0] for coordinate in axis_centre)
    assert axis_original >= 1
    assert axis_scaled < 1
    return {
        "schema": "n108-review-max-audit/v1",
        "status": "EXACT_PREMISES_AND_FIVE_POSES_PASS",
        "coverage": (
            "Exact input premises; retained receipt inventories; four native 99/100 "
            "control witnesses and the source 197/200 axis pose. "
            "No universal coverage decision and no native replay."
        ),
        "candidate": str(candidate_path.relative_to(repo)),
        "input_sha256": {"json": raw_digest, "gzip": compressed_digest},
        "n": n,
        "side": str(side),
        "core": str(core),
        "step": str(step),
        "directions": last + 1,
        "source_rectangles": len(seq(candidate["rectangles"])),
        "distinct_expanded_rectangles": len(densities),
        "mass": str(mass),
        "mass_deficit": str(n - mass),
        "net_endpoint_polynomial": str(polynomial(end)),
        "last_bin_left": str(last_lower),
        "last_bin_left_polynomial": str(polynomial(last_lower)),
        "shrink_margin": str(1 - core * (1 + step)),
        "tangent_form": str(core * (1 + step / (1 - step * step / 4))),
        "source_receipt_inventory": source_inventory,
        "native_receipt_inventory": native_inventory,
        "source_native_matching_node_counts": matching_nodes,
        "analytic_geometry_controls": 4,
        "samples": samples,
        "source_axis_control": {
            "index": 0,
            "pose": [str(value) for value in axis_centre],
            "original_capture_interval": enclosure(axis_original),
            "scaled_capture_interval": enclosure(axis_scaled),
            "in_domain": True,
            "exactly_below_one": True,
        },
    }


def main() -> None:
    if not __debug__:
        raise RuntimeError("Run without -O: this mathematical audit uses assertions")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    args = parser.parse_args()
    result = run(cast(Path, args.repo))
    sys.stdout.write(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
