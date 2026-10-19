"""Audit Overbeck's pinned n=11 certificate and exercise its checker boundaries.

This complements the complete upstream replay; it does not replace that replay.
The structural and quadratic checks do not import upstream code. Optional source
probes run in the explicitly selected upstream environment, keeping Numba out of
the project's dependencies. All measurements are retained in the output receipt.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib
import importlib.metadata
import json
import platform
import subprocess
import sys
import tempfile
import time
from bisect import bisect_left, bisect_right
from collections import Counter
from decimal import Decimal, localcontext
from fractions import Fraction
from itertools import pairwise, product
from math import comb
from pathlib import Path
from typing import Any

CERTIFICATE_SHA256 = "57e9927da5c13f42dd8bcbf8f08c84363635fece626657ee63a810c61cd44458"
SOURCE_COMMIT = "6a733f339395c3514f2ab63d8c4aa64cf63c0b5a"
SOURCE_MANIFEST_SHA256 = "17b9ca8fc7020bebffb0f10cbc2206d631265538a89fe1ada5fd76acf31a1b7a"
Point = tuple[Fraction, Fraction]


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key {key}")
        result[key] = value
    return result


def read_certificate(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == CERTIFICATE_SHA256, "wrong certificate bytes")
    return json.loads(raw, object_pairs_hook=unique_object)


def verify_source_tree(directory: Path) -> dict[str, Any]:
    """Bind executable probes to the reviewed release, even outside a Git checkout."""
    directory = directory.resolve()
    raw = (directory / "MANIFEST.json").read_bytes()
    require(hashlib.sha256(raw).hexdigest() == SOURCE_MANIFEST_SHA256, "wrong source manifest")
    manifest = json.loads(raw, object_pairs_hook=unique_object)
    require(manifest["format"] == "sha256-manifest-v1", "unknown source manifest")
    expected = {"MANIFEST.json"}
    for entry in manifest["files"]:
        relative = Path(entry["path"])
        require(not relative.is_absolute() and ".." not in relative.parts, "unsafe source path")
        require(relative.as_posix() not in expected, "repeated source manifest path")
        expected.add(relative.as_posix())
        path = directory / relative
        require(path.resolve().is_relative_to(directory), "source file escapes source tree")
        data = path.read_bytes()
        require(
            len(data) == entry["bytes"] and hashlib.sha256(data).hexdigest() == entry["sha256"],
            f"altered source file: {relative}",
        )
    # Ignore ordinary repository and execution caches, but reject injected modules.
    # The probe child uses a fresh bytecode-cache path, so ignored pyc files cannot run.
    for path in directory.rglob("*"):
        relative = path.relative_to(directory)
        if any(part in (".git", ".cache", "__pycache__") for part in relative.parts):
            continue
        require(not path.is_symlink(), f"source symlink: {relative}")
        if path.is_file():
            require(relative.as_posix() in expected, f"unrecorded source file: {relative}")
    return {
        "reviewed_source_commit": SOURCE_COMMIT,
        "manifest_sha256": SOURCE_MANIFEST_SHA256,
        "verified_files": len(manifest["files"]),
        "source_tree": str(directory),
    }


def images(point: tuple[int, int], side: int) -> set[tuple[int, int]]:
    result: set[tuple[int, int]] = set()
    for start in (point, point[::-1]):
        x, y = start
        for _ in range(4):
            result.add((x, y))
            x, y = side - y, x
    return result


def structure(certificate: dict[str, Any]) -> dict[str, Any]:
    """Reconstruct budgets and D4 invariance independently of both scanners."""
    denominator = certificate["coordinate_denominator"]
    weight_denominator = certificate["weight_denominator"]
    require(type(denominator) is int and denominator > 0, "coordinate denominator")
    require(type(weight_denominator) is int and weight_denominator > 0, "weight denominator")
    scaled_side = Fraction(certificate["L"]) * denominator
    require(scaled_side.denominator == 1, "nonintegral container")
    side = int(scaled_side)
    points: list[tuple[int, int]] = []
    weights: list[int] = []
    positive_orbits = 0
    for x, y, weight in certificate["point_orbits"]:
        require(all(type(v) is int for v in (x, y, weight)), "noninteger site or weight")
        require(0 <= x <= side and 0 <= y <= side and weight >= 0, "invalid point")
        orbit = sorted(images((x, y), side))
        points.extend(orbit)
        weights.extend([weight] * len(orbit))
        positive_orbits += weight > 0
    require(len(set(points)) == len(points), "duplicate physical site")
    lookup = {point: index for index, point in enumerate(points)}
    budgets: Counter[str] = Counter({"points": sum(weights)})
    counts: Counter[str] = Counter({"points": sum(w > 0 for w in weights)})
    orbit_counts: Counter[str] = Counter({"points": positive_orbits})
    absolute = sum(weights)
    active_sites = {index for index, weight in enumerate(weights) if weight > 0}
    maximum_feature_size = 1
    for atom in certificate["charge_orbits"]:
        members, threshold, weight = atom["sets"], atom["threshold"], atom["weight"]
        require(type(weight) is int and weight >= 0, "negative or noninteger charge")
        require(bool(members), "empty charge orbit")
        size = len(members[0])
        require(
            size in (3, 5) and type(threshold) is int and 1 <= threshold <= size, "threshold"
        )
        for member in members:
            require(len(member) == size and len(set(member)) == size, "repeated charge site")
            require(
                all(type(i) is int and 0 <= i < len(points) for i in member), "charge index"
            )
        expected: set[tuple[int, ...]] = set()
        for reflect in (False, True):
            current = [points[index] for index in members[0]]
            if reflect:
                current = [(y, x) for x, y in current]
            for _ in range(4):
                expected.add(tuple(sorted(lookup[point] for point in current)))
                current = [(side - y, x) for x, y in current]
        require(
            expected == set(map(tuple, members)) and len(expected) == len(members), "D4 orbit"
        )
        name = f"{threshold}-of-{size}"
        if weight > 0:
            maximum_feature_size = max(maximum_feature_size, size)
            for member in members:
                active_sites.update(member)
        budgets[name] += len(members) * (size // threshold) * weight
        counts[name] += len(members) * (weight > 0)
        orbit_counts[name] += weight > 0
        absolute += (
            len(members)
            * weight
            * sum(
                comb(size, j) * comb(j - 1, threshold - 1) for j in range(threshold, size + 1)
            )
        )
    total = sum(budgets.values())
    minimum = certificate["minimum_units"]
    require(type(minimum) is int and minimum > 0, "minimum must be a positive integer")
    require(total == certificate["budget_units"], "incorrect counting budget")
    require(11 * minimum > total, "no strict counting contradiction")
    require(absolute < 2**50, "insufficient accumulation headroom")
    return {
        "physical_sites": len(points),
        "active_physical_sites": len(active_sites),
        "site_orbits": len(certificate["point_orbits"]),
        "positive_orbits_by_family": dict(orbit_counts),
        "physical_features_by_family": dict(counts),
        "budget_units_by_family": dict(budgets),
        "budget_units": total,
        "minimum_units": minimum,
        "surplus_units": 11 * minimum - total,
        "absolute_expanded_weight_units": absolute,
        "headroom_limit": 2**50,
        "native_padded_member_slots": sum(counts.values()) * maximum_feature_size,
    }


def quadratic_minimum(
    coefficients: tuple[Fraction, Fraction, Fraction], left: Fraction, right: Fraction
) -> Fraction:
    constant, linear, square = coefficients
    points = [left, right]
    if square > 0:
        vertex = -linear / (2 * square)
        if left < vertex < right:
            points.append(vertex)
    return min(constant + linear * point + square * point**2 for point in points)


def containment(certificate: dict[str, Any]) -> dict[str, Any]:
    parent = Fraction(certificate["A"])
    side = Fraction(certificate["L"])
    require(
        side == Fraction(191, 50) and side / parent == Fraction(31, 8), "wrong claimed side"
    )
    cursor = Fraction(0)
    minimum_numerator: Fraction | None = None
    for raw in certificate["entries"]:
        require(all(isinstance(value, str) for value in raw), "rational fields must be strings")
        left, right, direction, core = map(Fraction, raw)
        require(left == cursor and 0 <= left < right < 1, "angle partition")
        require(0 <= direction < 1 and 0 < core < parent, "core or direction range")
        cosine = (1 - direction**2) / (1 + direction**2)
        sine = 2 * direction / (1 + direction**2)
        for horizontal, vertical in product((-1, 1), repeat=2):
            # Dot each independently rotated core vertex with both parent axes.
            # Multiplication by 1+u^2 leaves a rational quadratic on [left,right].
            dot = horizontal * cosine - vertical * sine
            cross = horizontal * sine + vertical * cosine
            polynomial = (parent - core * dot, -2 * core * cross, parent + core * dot)
            value = quadratic_minimum(polynomial, left, right)
            require(value > 0, "core reaches a parent boundary")
            minimum_numerator = (
                value if minimum_numerator is None else min(minimum_numerator, value)
            )
        radius = parent * min((1 + 2 * u - u**2) / (1 + u**2) for u in (left, right)) / 2
        envelope = (parent - 2 * radius, 2 * parent, -parent - 2 * radius)
        require(quadratic_minimum(envelope, left, right) >= 0, "centre envelope too small")
        require(0 < radius < side / 2, "centre domain has no interior")
        cursor = right
    require(cursor**2 + 2 * cursor > 1, "missing folded orientations")
    return {
        "intervals": len(certificate["entries"]),
        "strict_quadratic_inequalities": 4 * len(certificate["entries"]),
        "centre_envelope_inequalities": len(certificate["entries"]),
        "minimum_positive_quadratic_numerator": str(minimum_numerator),
        "last_half_angle": str(cursor),
        "angle_coverage_surplus": str(cursor**2 + 2 * cursor - 1),
    }


def clip_vertical(polygon: list[Point], boundary: Fraction, *, keep_right: bool) -> list[Point]:
    result: list[Point] = []
    for previous, current in zip(polygon, polygon[1:] + polygon[:1], strict=True):
        p_inside = previous[0] >= boundary if keep_right else previous[0] <= boundary
        q_inside = current[0] >= boundary if keep_right else current[0] <= boundary
        if p_inside != q_inside:
            proportion = (boundary - previous[0]) / (current[0] - previous[0])
            result.append((boundary, previous[1] + proportion * (current[1] - previous[1])))
        if q_inside:
            result.append(current)
    return result


def sampled_geometry(source: Any, certificate: dict[str, Any]) -> dict[str, Any]:
    """Check every slab of selected rows by general polygon clipping, plus dense sums."""
    data, jobs, _ = source.validate(certificate)
    published = json.loads(
        (Path(source.__file__).parent / "evidence/portable/python.json").read_text()
    )
    least_row = min(published["rows"], key=lambda row: row["minimum_units"])["row"]
    selected = sorted({0, 1, len(jobs) // 2, least_row, len(jobs) - 1})
    records = []
    for row in selected:
        arrays, meta = source.geometry(*data, *jobs[row], meta=True)
        tree = source.accumulate(*arrays)
        dense = source.accumulate(*arrays, direct=True)
        require(tuple(tree) == tuple(dense), "segment tree differs from direct array")
        require(
            int(tree[0]) == published["rows"][row]["minimum_units"], "published row differs"
        )
        direction, _, half_domain = jobs[row]
        cosine = (1 - direction**2) / (1 + direction**2)
        sine = 2 * direction / (1 + direction**2)
        factor = meta["scale"] * meta["R"]
        polygon = [
            ((cosine * x + sine * y) * factor, (-sine * x + cosine * y) * factor)
            for x, y in (
                (-half_domain, -half_domain),
                (half_domain, -half_domain),
                (half_domain, half_domain),
                (-half_domain, half_domain),
            )
        ]
        require(polygon == meta["poly"], "rotated domain mismatch")
        slabs = 0
        for index, (left, right) in enumerate(zip(meta["xe"], meta["xe"][1:], strict=False)):
            if arrays[-2][index] < 0:
                require(
                    right <= min(p[0] for p in polygon) or left >= max(p[0] for p in polygon),
                    "unscanned slab intersects domain interior",
                )
                continue
            clipped = clip_vertical(polygon, Fraction(left), keep_right=True)
            clipped = clip_vertical(clipped, Fraction(right), keep_right=False)
            lower = min(y for _, y in clipped)
            upper = max(y for _, y in clipped)
            expected = bisect_right(meta["ye"], lower) - 1, bisect_left(meta["ye"], upper)
            require(
                expected == (int(arrays[-2][index]), int(arrays[-1][index])),
                "slab query mismatch",
            )
            slabs += 1
        records.append(
            {
                "row": row,
                "minimum_units": int(tree[0]),
                "clipped_slabs": slabs,
                "cells": int(tree[1]),
                "dense_matches_segment_tree": True,
            }
        )
    return {"rows": records, "scope": "Selected rows only; all slabs per selected row."}


def mutation_probes(source: Any, certificate: dict[str, Any]) -> list[dict[str, str]]:
    names = (
        "negative_point_weight",
        "negative_charge_weight",
        "duplicate_point_orbit",
        "missing_charge_image",
        "duplicate_charge_site",
        "out_of_range_charge_site",
        "understated_budget",
        "angle_partition_gap",
        "truncated_angle_coverage",
        "nonstrict_core",
        "wrong_container",
        "insufficient_counting_margin",
        "core_touches_parent",
        "ambiguous_charge_schema",
        "expanded_weight_overflow",
    )
    records = []
    for name in names:
        altered = copy.deepcopy(certificate)
        match name:
            case "negative_point_weight":
                altered["point_orbits"][0][2] = -1
            case "negative_charge_weight":
                altered["charge_orbits"][0]["weight"] = -1
            case "duplicate_point_orbit":
                altered["point_orbits"].append(altered["point_orbits"][0])
            case "missing_charge_image":
                altered["charge_orbits"][0]["sets"].pop()
            case "duplicate_charge_site":
                altered["charge_orbits"][0]["sets"][0][0] = altered["charge_orbits"][0]["sets"][
                    0
                ][1]
            case "out_of_range_charge_site":
                altered["charge_orbits"][0]["sets"][0][0] = 10**9
            case "understated_budget":
                altered["budget_units"] -= 1
            case "angle_partition_gap":
                altered["entries"][1][0] = "1/10"
            case "truncated_angle_coverage":
                altered["entries"] = altered["entries"][:2]
            case "nonstrict_core":
                altered["entries"][0][3] = altered["A"]
            case "wrong_container":
                altered["L"] = "4"
            case "insufficient_counting_margin":
                altered["minimum_units"] = altered["budget_units"] // 11
            case "core_touches_parent":
                left, right, direction, _ = map(Fraction, altered["entries"][1])
                cosine, sine = source.trig(direction)
                widths = []
                for endpoint in (left, right):
                    parent_cosine, parent_sine = source.trig(endpoint)
                    widths.append(
                        cosine * parent_cosine
                        + sine * parent_sine
                        + abs(cosine * parent_sine - sine * parent_cosine)
                    )
                altered["entries"][1][3] = str(Fraction(altered["A"]) / max(widths))
            case "ambiguous_charge_schema":
                altered["threshold_orbits"] = []
            case "expanded_weight_overflow":
                x, y, old_weight = altered["point_orbits"][0]
                side = int(Fraction(altered["L"]) * altered["coordinate_denominator"])
                altered["point_orbits"][0][2] = 2**50
                altered["budget_units"] += len(images((x, y), side)) * (2**50 - old_weight)
                altered["minimum_units"] = altered["budget_units"] // 11 + 1
        try:
            source.validate(altered)
        except ValueError as error:
            records.append({"mutation": name, "result": "REFUSED", "reason": str(error)})
        else:
            raise ValueError(f"upstream accepted mutation: {name}")
    # A structurally valid raised minimum must fail a coverage decision, not merely
    # schema validation. One exact row suffices to refute the modified certificate.
    altered = copy.deepcopy(certificate)
    altered["minimum_units"] *= 2
    data, jobs, _ = source.validate(altered)
    minimum, _, _ = source.accumulate(*source.geometry(*data, *jobs[0]))
    require(
        int(minimum) < altered["minimum_units"], "raised-minimum coverage control did not fail"
    )
    records.append(
        {
            "mutation": "doubled_required_charge",
            "result": "REFUSED_BY_COVERAGE",
            "reason": f"row 0 gives {int(minimum)} < {altered['minimum_units']}",
        }
    )
    return records


def gap_arithmetic() -> dict[str, str]:
    with localcontext() as context:
        context.prec = 60
        lower = Decimal(31) / 8
        previous = Decimal(955000) * Decimal(518400042893309449).sqrt() / 179696714646249
        upper = Decimal("3.87708359002281417730789706010096")
        return {
            "prior_T026_approximation": str(previous),
            "reported_upper_approximation": str(upper),
            "new_lower": str(lower),
            "remaining_gap_approximation": str(upper - lower),
            "percent_of_T026_gap_closed_approximation": str(
                100 * (lower - previous) / (upper - previous)
            ),
            "scope": (
                "Decimal arithmetic on the T-026 expression and retained upper approximation; "
                "not an optimum proof."
            ),
        }


def reconcile_replay(directory: Path, certificate: dict[str, Any]) -> dict[str, Any]:
    """Require complete fresh receipt coverage before reporting a local proof replay."""
    aggregate = json.loads(
        (directory / "RESULT.json").read_text(), object_pairs_hook=unique_object
    )
    python = json.loads(
        (directory / "python.json").read_text(), object_pairs_hook=unique_object
    )
    javascript = json.loads(
        (directory / "secondary/RESULT.json").read_text(), object_pairs_hook=unique_object
    )
    controls = json.loads(
        (directory / "controls.json").read_text(), object_pairs_hook=unique_object
    )
    require(
        aggregate["status"] == "PASS_FRESH_PORTABLE_FULL_VERIFICATION", "launcher did not pass"
    )
    require(python["status"] == "PASS_FULL_EXACT_PYTHON_REPLAY", "Python replay did not pass")
    require(
        javascript["status"] == "PASS_FULL_EXACT_BIGINT_REPLAY",
        "JavaScript replay did not pass",
    )
    require(controls["status"] == "PASS_INDEPENDENT_EXACT_CONTROLS", "controls did not pass")
    for result in (aggregate, python, javascript, controls):
        require(
            result["certificate_sha256"] == CERTIFICATE_SHA256, "replay bound to other bytes"
        )
    count = len(certificate["entries"])
    bound = Fraction(certificate["L"]) / Fraction(certificate["A"])
    require(
        Fraction(aggregate["bound"]) == Fraction(python["bound"]) == bound,
        "replay bound differs",
    )
    require(
        Fraction(python["parent_side"])
        == Fraction(javascript["parent_side"])
        == Fraction(certificate["A"]),
        "replay parent side differs",
    )
    require(
        aggregate["intervals"] == python["intervals"] == count, "replay interval count differs"
    )
    require(
        [row["row"] for row in python["rows"]] == list(range(count)), "incomplete Python rows"
    )
    histogram = Counter(str(row["minimum_units"]) for row in python["rows"])
    require(
        dict(histogram) == python["histogram"] == javascript["histogram"], "histograms differ"
    )
    require(sum(histogram.values()) == count, "histogram does not cover every row")
    ranges = javascript["ranges"]
    require(
        bool(ranges) and ranges[0][0] == 0 and ranges[-1][1] == count, "JavaScript endpoints"
    )
    require(all(left < right for left, right in ranges), "empty JavaScript range")
    require(all(a[1] == b[0] for a, b in pairwise(ranges)), "JavaScript gap")
    require(javascript["range"] == [0, count], "JavaScript range header differs")
    require(not javascript["escape_rows"], "JavaScript found an escape")
    part_slabs = 0
    for left, right in ranges:
        part = json.loads(
            (directory / f"secondary/range-{left}-{right}.json").read_text(),
            object_pairs_hook=unique_object,
        )
        require(part["status"] == "PASS_EXACT_MOVABLE_SUPPORT_SCAN", "JavaScript range failed")
        require(
            part["certificate_sha256"] == CERTIFICATE_SHA256,
            "JavaScript range certificate differs",
        )
        require(part["range"] == [left, right], "JavaScript range receipt differs")
        require(
            Fraction(part["parent_side"]) == Fraction(certificate["A"]),
            "JavaScript range parent differs",
        )
        require(
            part["budget_units"] == certificate["budget_units"],
            "JavaScript range budget differs",
        )
        require(not part["escape_rows"], "JavaScript range found an escape")
        partial_histogram = Counter(
            str(row["minimum_units"]) for row in python["rows"][left:right]
        )
        require(
            part["histogram"] == dict(partial_histogram), "JavaScript range histogram differs"
        )
        require(
            part["minimum_units"] == min(map(int, partial_histogram)),
            "JavaScript range minimum differs",
        )
        part_slabs += part["center_slabs"]
    require(part_slabs == javascript["center_slabs"], "JavaScript slab total differs")
    minimum = min(row["minimum_units"] for row in python["rows"])
    require(
        minimum
        == certificate["minimum_units"]
        == aggregate["minimum_units"]
        == python["minimum_units"]
        == javascript["minimum_units"],
        "minimum differs",
    )
    require(
        aggregate["budget_units"]
        == python["budget_units"]
        == javascript["budget_units"]
        == certificate["budget_units"],
        "replay budget differs",
    )
    require(
        aggregate["surplus_units"]
        == python["counting_surplus_units"]
        == 11 * minimum - certificate["budget_units"]
        > 0,
        "replay counting surplus differs",
    )
    require(
        Fraction(python["strict_core_margin"]) == Fraction(1, 10**12),
        "replay margin differs from the reviewed pinned certificate",
    )
    for field in ("slabs", "cells"):
        require(
            sum(row[field] for row in python["rows"]) == python[field],
            f"Python {field} differs",
        )
    require(controls["containment"]["intervals"] == count, "premise controls incomplete")
    require(
        controls["containment"]["quadratic_inequalities"] == 4 * count,
        "quadratic count differs",
    )
    boundary_rows = controls["boundary_samples"]["rows"]
    require(
        sum(row["centres"] for row in boundary_rows)
        == controls["boundary_samples"]["total_centres"],
        "boundary sample count differs",
    )
    require(
        min(row["minimum_charge"] for row in boundary_rows)
        == controls["boundary_samples"]["minimum_sampled_charge"]
        >= minimum,
        "boundary sample charge differs",
    )
    return {
        "status": aggregate["status"],
        "certificate_sha256": CERTIFICATE_SHA256,
        "bound": str(bound),
        "parent_side": certificate["A"],
        "scope": (
            "Receipt consistency and complete recorded coverage; "
            "not a signed execution attestation."
        ),
        "intervals": count,
        "minimum_units": minimum,
        "histogram_bins": len(histogram),
        "python_slabs": python["slabs"],
        "python_cells": python["cells"],
        "javascript_slabs": javascript["center_slabs"],
        "python_seconds": python["seconds"],
        "javascript_seconds": javascript["seconds"],
        "controls_seconds": controls["seconds"],
        "boundary_centres": controls["boundary_samples"]["total_centres"],
        "minimum_sampled_charge": controls["boundary_samples"]["minimum_sampled_charge"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--upstream-tree", type=Path)
    parser.add_argument("--upstream-python", type=Path)
    parser.add_argument("--full-replay", type=Path)
    parser.add_argument("--probe-source", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    certificate = read_certificate(args.certificate)
    if args.probe_source:
        require(args.upstream_tree is not None, "--upstream-tree required")
        source_identity = verify_source_tree(args.upstream_tree)
        with tempfile.TemporaryDirectory(prefix="n11-audit-bytecode-") as bytecode:
            sys.pycache_prefix = bytecode
            sys.dont_write_bytecode = True
            sys.path.insert(0, str(args.upstream_tree.resolve()))
            source = importlib.import_module("exact_mixed")
            print(
                json.dumps(
                    {
                        "source_verification": source_identity,
                        "mutations": mutation_probes(source, certificate),
                        "sampled_geometry": sampled_geometry(source, certificate),
                        "runtime": {
                            "python": sys.version,
                            "platform": platform.platform(),
                            "packages": {
                                name: importlib.metadata.version(name)
                                for name in ("numpy", "numba", "llvmlite")
                            },
                        },
                    }
                )
            )
        return 0
    require(args.output is not None, "--output required")
    start = time.monotonic()
    result = {
        "status": "PASS_SOURCE_DISTINCT_PREMISE_CONTROLS",
        "certificate_sha256": CERTIFICATE_SHA256,
        "reviewed_certificate_source_commit": SOURCE_COMMIT,
        "scope": (
            "Complete premises and selected scanner controls; "
            "complete upstream replay remains required."
        ),
        "structure": structure(certificate),
        "containment": containment(certificate),
        "gap_arithmetic": gap_arithmetic(),
    }
    if args.upstream_tree is not None or args.upstream_python is not None:
        if args.upstream_tree is None or args.upstream_python is None:
            raise ValueError(
                "both upstream tree and interpreter are required for source probes"
            )
        result["source_verification"] = verify_source_tree(args.upstream_tree)
        command = [
            str(args.upstream_python),
            str(Path(__file__).resolve()),
            str(args.certificate.resolve()),
            "--probe-source",
            "--upstream-tree",
            str(args.upstream_tree.resolve()),
        ]
        completed = subprocess.run(
            command, check=True, capture_output=True, text=True, timeout=300
        )
        result["source_probes"] = json.loads(completed.stdout)
        result["status"] = "PASS_SOURCE_DISTINCT_PREMISE_AND_ADVERSARIAL_CONTROLS"
        result["source_probe_stderr"] = completed.stderr
        optimized = subprocess.run(
            [str(args.upstream_python), "-O", str(args.upstream_tree / "verify.py"), "--help"],
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
        require(
            optimized.returncode != 0 and "assertions" in optimized.stderr, "-O guard missing"
        )
        result["optimized_launcher_control"] = {
            "returncode": optimized.returncode,
            "stderr": optimized.stderr.strip(),
        }
    if args.full_replay is not None:
        require(
            args.upstream_tree is not None,
            "replay reconciliation requires a verified source tree",
        )
        result["full_replay"] = reconcile_replay(args.full_replay, certificate)
    result["seconds"] = time.monotonic() - start
    # The upstream probe environment intentionally has no project-only dependencies.
    from strif import atomic_write_text  # noqa: PLC0415

    atomic_write_text(args.output, json.dumps(result, indent=2) + "\n", make_parents=True)
    print(
        json.dumps(
            {
                "status": result["status"],
                "seconds": result["seconds"],
                "receipt": str(args.output),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
