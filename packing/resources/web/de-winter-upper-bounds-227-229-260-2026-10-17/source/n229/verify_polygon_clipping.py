#!/usr/bin/env python3
"""Exact unit-square feasibility via convex clipping and intersection area.

This is a third algorithmic check implemented within the same campaign, using
its shared rational witness inputs. It is not outside independent authorship.
No SAT or rotated-axis separation test is used. Axis-aligned bounding boxes
only prune pairs whose intersection has zero width or zero height.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import time
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

Point = tuple[F, F]
Polygon = list[Point]
DISCLOSURE = (
    "Implemented by another agent within the same campaign, using the same "
    "shared rational witnesses. Algorithmically distinct from the existing "
    "SAT/projection checks; not verification by an outside independent author."
)


class VerificationError(ValueError):
    def __init__(self, code: str, message: str, **details):
        super().__init__(message)
        self.code = code
        self.details = details


def rational(value) -> F:
    if type(value) not in (str, int):
        raise VerificationError("invalid_rational", "Use rational strings or integers")
    try:
        return F(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise VerificationError("invalid_rational", str(exc)) from exc


def sub(a: Point, b: Point) -> Point:
    return a[0] - b[0], a[1] - b[1]


def cross(a: Point, b: Point) -> F:
    return a[0] * b[1] - a[1] * b[0]


def signed_twice_area(poly: Polygon) -> F:
    if len(poly) < 3:
        return F(0)
    return sum((cross(poly[i], poly[(i + 1) % len(poly)]) for i in range(len(poly))), F(0))


def intersection_point(start: Point, end: Point, ds: F, de: F) -> Point:
    # ds and de have opposite inside classifications, so the denominator is
    # nonzero; exact interpolation includes endpoint and collinear contacts.
    t = ds / (ds - de)
    return start[0] + t * (end[0] - start[0]), start[1] + t * (end[1] - start[1])


def deduplicate(poly: Polygon) -> Polygon:
    result: Polygon = []
    for point in poly:
        if not result or result[-1] != point:
            result.append(point)
    if len(result) > 1 and result[0] == result[-1]:
        result.pop()
    return result


def convex_intersection(subject: Polygon, clip: Polygon) -> Polygon:
    """Sutherland–Hodgman clipping with exact rational half-plane predicates."""
    result = list(subject)
    for i, a in enumerate(clip):
        if not result:
            break
        b = clip[(i + 1) % len(clip)]
        edge = sub(b, a)
        previous = result[-1]
        ds = cross(edge, sub(previous, a))
        previous_inside = ds >= 0
        output: Polygon = []
        for current in result:
            de = cross(edge, sub(current, a))
            current_inside = de >= 0
            if current_inside:
                if not previous_inside:
                    output.append(intersection_point(previous, current, ds, de))
                output.append(current)
            elif previous_inside:
                output.append(intersection_point(previous, current, ds, de))
            previous, ds, previous_inside = current, de, current_inside
        result = deduplicate(output)
    return result


def intersection_area(a: Polygon, b: Polygon) -> tuple[F, int]:
    clipped = convex_intersection(a, b)
    return abs(signed_twice_area(clipped)) / 2, len(clipped)


def square_vertices(center: tuple[F, F], basis: tuple[F, F]) -> Polygon:
    x, y = center
    c, s = basis
    return [
        (x + (i * c - j * s) / 2, y + (i * s + j * c) / 2)
        for i, j in [(-1, -1), (1, -1), (1, 1), (-1, 1)]
    ]


def box(poly: Polygon) -> tuple[F, F, F, F]:
    return min(p[0] for p in poly), min(p[1] for p in poly), max(p[0] for p in poly), max(p[1] for p in poly)


def boxes_have_zero_area_intersection(a, b) -> bool:
    return min(a[2], b[2]) <= max(a[0], b[0]) or min(a[3], b[3]) <= max(a[1], b[1])


def certify(witness: dict, expected_n: int | None = None) -> dict:
    started = time.monotonic()
    squares = witness.get("squares")
    n = witness.get("n")
    if not isinstance(squares, list) or type(n) is not int or n != len(squares):
        raise VerificationError("count_mismatch", "Declared count differs from square list")
    if expected_n is not None and n != expected_n:
        raise VerificationError("count_mismatch", "Witness count differs from registry", expected=expected_n, actual=n)
    if n < 1:
        raise VerificationError("count_mismatch", "A packing must contain at least one square")
    side = rational(witness["side"])
    if side <= 0:
        raise VerificationError("invalid_side", "Container side must be positive")
    polygons: list[Polygon] = []
    bounds = []
    wall_clearance = side
    for index, square in enumerate(squares):
        if len(square.get("center", [])) != 2 or len(square.get("basis", [])) != 2:
            raise VerificationError("invalid_geometry", "Expected two center and two basis coordinates", square=index)
        center = tuple(map(rational, square["center"]))
        basis = tuple(map(rational, square["basis"]))
        c, s = basis
        if c * c + s * s != 1:
            raise VerificationError("nonunit_basis", "Basis has nonunit squared norm", square=index)
        poly = square_vertices(center, basis)
        if signed_twice_area(poly) != 2:
            raise VerificationError("invalid_unit_geometry", "Square area is not exactly one", square=index)
        for k in range(4):
            e = sub(poly[(k + 1) % 4], poly[k])
            f = sub(poly[(k + 2) % 4], poly[(k + 1) % 4])
            if e[0] * e[0] + e[1] * e[1] != 1 or e[0] * f[0] + e[1] * f[1] != 0:
                raise VerificationError("invalid_unit_geometry", "Invalid edge length or right angle", square=index)
        for vertex_index, (x, y) in enumerate(poly):
            if not (0 <= x <= side and 0 <= y <= side):
                raise VerificationError("wall_violation", "Vertex outside enclosing square", square=index, vertex=vertex_index)
            wall_clearance = min(wall_clearance, x, y, side - x, side - y)
        polygons.append(poly)
        bounds.append(box(poly))
    pruned = clipped = degenerate = max_vertices = 0
    for i, j in combinations(range(n), 2):
        if boxes_have_zero_area_intersection(bounds[i], bounds[j]):
            pruned += 1
            continue
        area, vertices = intersection_area(polygons[i], polygons[j])
        clipped += 1
        max_vertices = max(max_vertices, vertices)
        if vertices in (1, 2):
            degenerate += 1
        if area > 0:
            raise VerificationError("positive_intersection_area", "Two square interiors overlap", pair=[i, j], exact_area=str(area))
    total = n * (n - 1) // 2
    assert pruned + clipped == total
    return {
        "valid": True,
        "n": n,
        "side_exact": str(side),
        "unit_geometry_checked_exactly": n,
        "wall_containment_checked_exactly": True,
        "minimum_wall_clearance_exact": str(wall_clearance),
        "all_pairs_considered": total,
        "pairs_pruned_by_zero_area_bounding_box": pruned,
        "pairs_clipped_with_exact_rationals": clipped,
        "degenerate_point_or_segment_intersections": degenerate,
        "maximum_clipped_polygon_vertices": max_vertices,
        "all_pair_intersection_areas_zero": True,
        "total_positive_intersection_area_exact": "0",
        "algorithm": "convex polygon clipping and exact shoelace intersection area",
        "arithmetic": "Python fractions.Fraction, with no floating-point tolerance",
        "authorship_disclosure": DISCLOSURE,
        "elapsed_seconds": time.monotonic() - started,
    }


def check(q: dict) -> dict:
    """Portable package API: exact feasibility result, or VerificationError."""
    return certify(q)


def algorithm_self_tests() -> list[dict]:
    axis = square_vertices((F(0), F(0)), (F(1), F(0)))
    cases = [
        ("identical", axis, F(1)),
        ("half_width_overlap", square_vertices((F(1, 2), F(0)), (F(1), F(0))), F(1, 2)),
        ("edge_touch", square_vertices((F(1), F(0)), (F(1), F(0))), F(0)),
        ("vertex_touch", square_vertices((F(1), F(1)), (F(1), F(0))), F(0)),
        ("separated", square_vertices((F(2), F(0)), (F(1), F(0))), F(0)),
        ("rational_rotation", square_vertices((F(0), F(0)), (F(3, 5), F(4, 5))), F(5, 6)),
        ("tiny_positive_sliver", square_vertices((1 - F(1, 10**12), F(0)), (F(1), F(0))), F(1, 10**12)),
    ]
    results = []
    for name, polygon, expected in cases:
        actual, vertices = intersection_area(axis, polygon)
        if actual != expected:
            raise AssertionError(f"Area self-test {name}: {actual} != {expected}")
        results.append({"name": name, "expected_area": str(expected), "computed_area": str(actual), "passed": True, "intersection_vertices": vertices})
    return results


def negative_controls(witness: dict) -> list[dict]:
    n = witness["n"]
    tests = []
    wrong = copy.deepcopy(witness)
    wrong["n"] = n + 1
    tests.append(("wrong_count", wrong, "count_mismatch"))
    duplicate = copy.deepcopy(witness)
    duplicate["squares"][1] = copy.deepcopy(duplicate["squares"][0])
    tests.append(("duplicated_square", duplicate, "positive_intersection_area"))
    invalid = copy.deepcopy(witness)
    invalid["squares"][0]["basis"] = ["2", "0"]
    tests.append(("invalid_unit_basis", invalid, "nonunit_basis"))
    shrunken = copy.deepcopy(witness)
    maximum_vertex = max(
        coordinate
        for square in witness["squares"]
        for point in square_vertices(tuple(map(rational, square["center"])), tuple(map(rational, square["basis"])))
        for coordinate in point
    )
    shrunken["side"] = str(maximum_vertex - F(1, 10**6))
    tests.append(("shrunken_box", shrunken, "wall_violation"))
    result = []
    for name, control, expected in tests:
        try:
            certify(control, expected_n=n)
        except VerificationError as exc:
            passed = exc.code == expected
            result.append({"name": name, "rejected": True, "expected_error": expected, "actual_error": exc.code, "passed": passed, "details": exc.details})
            if not passed:
                raise AssertionError(f"Wrong rejection for {name}: {exc.code}") from exc
        else:
            raise AssertionError(f"Negative control {name} was accepted")
    return result


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=Path("verification/verified_records.json"))
    parser.add_argument("--output", type=Path, default=Path("audit_2026-10-17"))
    parser.add_argument("--witness", type=Path)
    parser.add_argument("--expected-n", type=int)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    self_tests = algorithm_self_tests()
    (args.output / "polygon_area_self_tests.json").write_text(json.dumps(self_tests, indent=2) + "\n")
    if args.witness:
        witness = json.loads(args.witness.read_text())
        print(json.dumps(certify(witness, args.expected_n), indent=2))
        return
    registry = json.loads(args.registry.read_text())
    results, controls = {}, {}
    for ns, entry in sorted(registry.items(), key=lambda item: int(item[0])):
        path = Path(entry["witness"])
        witness = json.loads(path.read_text())
        if rational(witness["side"]) != rational(entry["certified_side_exact"]):
            raise VerificationError("registry_side_mismatch", "Registry and witness exact sides differ", n=int(ns))
        result = certify(witness, int(ns))
        result.update(witness=str(path), witness_sha256=sha256(path))
        results[ns] = result
        controls[ns] = negative_controls(witness)
        (args.output / f"polygon_area_n{ns}.json").write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps({"n": int(ns), "valid": result["valid"], "clipped_pairs": result["pairs_clipped_with_exact_rationals"], "seconds": result["elapsed_seconds"]}), flush=True)
        (args.output / "polygon_area_results.json").write_text(json.dumps({"registry": str(args.registry), "registry_sha256": sha256(args.registry), "checker": Path(__file__).name, "checker_sha256": sha256(Path(__file__)), "authorship_disclosure": DISCLOSURE, "results": results}, indent=2) + "\n")
        (args.output / "polygon_area_negative_controls.json").write_text(json.dumps(controls, indent=2) + "\n")


if __name__ == "__main__":
    main()
