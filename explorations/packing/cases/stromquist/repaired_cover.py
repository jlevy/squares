#!/usr/bin/env python3
"""Certify the preregistered one-coordinate repair of Stromquist's Theorem 2.

H-041 is deliberately source-distinct.  The archived paper fixes the printed
Figure 14 point ``G=(4/5,37/20)``; this checker proves a different finite
certificate with ``G'=(79/100,37/20)`` and records that one-coordinate delta.

Every decisive calculation is exact in ``Q(sqrt(5))`` or in rational interval
arithmetic.  In particular, the Lemma 4 cubic is filtered through the unsquared
sign condition before its stationary value is bounded.  Floating point and
search do not decide any claim.  Replay rebuilds the complete record and checks
it byte-for-byte after rejecting duplicate or stale certificate inventories.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import tempfile
import time
from collections import Counter, deque
from collections.abc import Callable
from dataclasses import dataclass
from fractions import Fraction
from itertools import pairwise
from pathlib import Path
from typing import cast

ROOT = Path(__file__).resolve().parents[2]
PDF = ROOT / "resources/papers/stromquist-2003-packing-10-or-11-unit-squares.pdf"
RAW_SOURCE = ROOT / ("resources/papers/stromquist-2003-packing-10-or-11-unit-squares.raw.md")

SCHEMA_VERSION = 1
PDF_SHA256 = "146ac14a015910a95d0c25bf986f6073bcccd21a29ee754a45dcc0d4224d5e0b"
RAW_SOURCE_SHA256 = "5808f3152c2d3a409c54d1f6ebb2636b7500eb22d489ccf9908435007d8a1d6b"
PAGE_9_SVG_SHA256 = "95c80e60a018a19c01ebe6a681acfc5a1833c0beb5b433ce200a55df58127d82"
PAGE_9_TOPOLOGY_PATH_SHA256 = "2aa5004d2e86b1a7be3d9c6463880b8a797e19b8a0999489420c6889357f4839"
FIGURE13_POINT_SHA256 = "7ff0aaf32d5ea83ffd95c9b2c3cc1dcc0257e144bd75bbc8233296cdef4db8a1"
PRINTED_FIGURE14_POINT_SHA256 = (
    "62868418be08db7c8bf8f21c7cb6d66ac500b1d7b7f0ce593a7703b8e2c4ea0b"
)
REPAIRED_FIGURE14_POINT_SHA256 = (
    "fbe5ac7694a2f1a12a91ab9c2585e19f4b563c1b0e11520a51ce128dac1f24e3"
)
FIGURE14_TOPOLOGY_SHA256 = "c6b2c3d491b7b13f65e65f0d133d6eaeb3b493ba43676840341a57f96a149631"
SQRT_BOUND_SCALE = 10**24


def _fraction(value: int | Fraction) -> Fraction:
    return value if isinstance(value, Fraction) else Fraction(value)


@dataclass(frozen=True)
class Q5:
    """One exact element ``rational + radical * sqrt(5)``."""

    rational: Fraction = Fraction(0)
    radical: Fraction = Fraction(0)

    @classmethod
    def from_value(cls, value: int | Fraction | Q5) -> Q5:
        if isinstance(value, Q5):
            return value
        return cls(_fraction(value))

    def __add__(self, other: int | Fraction | Q5) -> Q5:
        right = self.from_value(other)
        return Q5(self.rational + right.rational, self.radical + right.radical)

    def __radd__(self, other: int | Fraction | Q5) -> Q5:
        return self + other

    def __neg__(self) -> Q5:
        return Q5(-self.rational, -self.radical)

    def __sub__(self, other: int | Fraction | Q5) -> Q5:
        return self + (-self.from_value(other))

    def __rsub__(self, other: int | Fraction | Q5) -> Q5:
        return self.from_value(other) - self

    def __mul__(self, other: int | Fraction | Q5) -> Q5:
        right = self.from_value(other)
        return Q5(
            self.rational * right.rational + 5 * self.radical * right.radical,
            self.rational * right.radical + self.radical * right.rational,
        )

    def __rmul__(self, other: int | Fraction | Q5) -> Q5:
        return self * other

    def __truediv__(self, other: int | Fraction | Q5) -> Q5:
        right = self.from_value(other)
        denominator = right.rational**2 - 5 * right.radical**2
        if denominator == 0:
            raise ZeroDivisionError("division by zero in Q(sqrt(5))")
        return Q5(
            (self.rational * right.rational - 5 * self.radical * right.radical) / denominator,
            (self.radical * right.rational - self.rational * right.radical) / denominator,
        )

    def __rtruediv__(self, other: int | Fraction | Q5) -> Q5:
        return self.from_value(other) / self

    def __pow__(self, exponent: int) -> Q5:
        if exponent < 0:
            return (Q5.from_value(1) / self) ** (-exponent)
        result = Q5.from_value(1)
        base = self
        power = exponent
        while power:
            if power & 1:
                result *= base
            base *= base
            power >>= 1
        return result

    def sign(self) -> int:
        """Return the exact sign without a floating approximation."""
        a = self.rational
        b = self.radical
        if b == 0:
            return (a > 0) - (a < 0)
        if b > 0:
            if a >= 0:
                return 1
            comparison = 5 * b**2 - a**2
            return (comparison > 0) - (comparison < 0)
        if a <= 0:
            return -1
        comparison = a**2 - 5 * b**2
        return (comparison > 0) - (comparison < 0)

    def is_zero(self) -> bool:
        return self.rational == 0 and self.radical == 0

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Q5):
            return self.rational == other.rational and self.radical == other.radical
        if isinstance(other, (int, Fraction)):
            return self == Q5.from_value(other)
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.rational, self.radical))

    def __lt__(self, other: int | Fraction | Q5) -> bool:
        return (self - other).sign() < 0

    def __le__(self, other: int | Fraction | Q5) -> bool:
        return (self - other).sign() <= 0

    def __gt__(self, other: int | Fraction | Q5) -> bool:
        return (self - other).sign() > 0

    def __ge__(self, other: int | Fraction | Q5) -> bool:
        return (self - other).sign() >= 0

    def text(self) -> str:
        if self.radical == 0:
            return fraction_text(self.rational)
        if self.rational == 0:
            return f"{fraction_text(self.radical)}*sqrt(5)"
        sign = "+" if self.radical > 0 else "-"
        return f"{fraction_text(self.rational)}{sign}{fraction_text(abs(self.radical))}*sqrt(5)"


ZERO = Q5()
ONE = Q5.from_value(1)
SQRT5 = Q5(Fraction(0), Fraction(1))
A0 = Fraction(2, 5) * SQRT5
SIDE = 2 + 2 * A0
CENTER = SIDE / 2
U = 1 - A0 / 2
V = 1 + A0 / 2

Point = tuple[Q5, Q5]
Face = tuple[str, ...]
Edge = tuple[str, str]
Polynomial = tuple[Q5, ...]


def q(value: int | Fraction | Q5) -> Q5:
    return Q5.from_value(value)


def point(x: int | Fraction | Q5, y: int | Fraction | Q5) -> Point:
    return q(x), q(y)


def fraction_text(value: Fraction) -> str:
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_digest(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def point_record(value: Point) -> list[str]:
    return [coordinate.text() for coordinate in value]


def points_digest(points: dict[str, Point]) -> str:
    return canonical_digest({name: point_record(points[name]) for name in sorted(points)})


def add_points(left: Point, right: Point) -> Point:
    return left[0] + right[0], left[1] + right[1]


def scale_point(value: Point, scalar: Q5) -> Point:
    return value[0] * scalar, value[1] * scalar


def subtract_points(left: Point, right: Point) -> Point:
    return left[0] - right[0], left[1] - right[1]


def cross(left: Point, right: Point) -> Q5:
    return left[0] * right[1] - left[1] * right[0]


def orient(first: Point, second: Point, third: Point) -> Q5:
    return cross(subtract_points(second, first), subtract_points(third, first))


def squared_distance(first: Point, second: Point) -> Q5:
    delta = subtract_points(first, second)
    return delta[0] ** 2 + delta[1] ** 2


def polygon_area2(vertices: tuple[Point, ...]) -> Q5:
    return sum(
        (
            cross(vertices[index], vertices[(index + 1) % len(vertices)])
            for index in range(len(vertices))
        ),
        ZERO,
    )


def normalized_edge(first: str, second: str) -> Edge:
    return cast(Edge, tuple(sorted((first, second))))


def edges_for_face(face: Face) -> tuple[Edge, ...]:
    return tuple(
        normalized_edge(face[index], face[(index + 1) % len(face)])
        for index in range(len(face))
    )


def between(value: Q5, first: Q5, second: Q5) -> bool:
    low, high = (first, second) if first <= second else (second, first)
    return low <= value <= high


def segments_cross_strict(first: tuple[Point, Point], second: tuple[Point, Point]) -> bool:
    a, b = first
    c, d = second
    ab_c = orient(a, b, c).sign()
    ab_d = orient(a, b, d).sign()
    cd_a = orient(c, d, a).sign()
    cd_b = orient(c, d, b).sign()
    if ab_c * ab_d < 0 and cd_a * cd_b < 0:
        return True
    if ab_c == 0 and between(c[0], a[0], b[0]) and between(c[1], a[1], b[1]):
        return True
    if ab_d == 0 and between(d[0], a[0], b[0]) and between(d[1], a[1], b[1]):
        return True
    if cd_a == 0 and between(a[0], c[0], d[0]) and between(a[1], c[1], d[1]):
        return True
    return cd_b == 0 and between(b[0], c[0], d[0]) and between(b[1], c[1], d[1])


def validate_noncrossing(points: dict[str, Point], edges: tuple[Edge, ...]) -> None:
    if len(edges) != len(set(edges)):
        raise ValueError("edge inventory contains a duplicate")
    for index, first in enumerate(edges):
        for second in edges[index + 1 :]:
            if set(first) & set(second):
                continue
            if segments_cross_strict(
                (points[first[0]], points[first[1]]),
                (points[second[0]], points[second[1]]),
            ):
                raise ValueError(f"nonadjacent edges cross: {first}, {second}")


def connected_vertices(edges: tuple[Edge, ...]) -> set[str]:
    adjacency: dict[str, set[str]] = {}
    for first, second in edges:
        adjacency.setdefault(first, set()).add(second)
        adjacency.setdefault(second, set()).add(first)
    if not adjacency:
        return set()
    root = min(adjacency)
    reached = {root}
    queue = deque([root])
    while queue:
        vertex = queue.popleft()
        for neighbour in adjacency[vertex]:
            if neighbour not in reached:
                reached.add(neighbour)
                queue.append(neighbour)
    return reached


def _poly_trim(polynomial: Polynomial) -> Polynomial:
    coefficients = list(polynomial)
    while len(coefficients) > 1 and coefficients[-1].is_zero():
        coefficients.pop()
    return tuple(coefficients)


def poly_derivative(polynomial: Polynomial) -> Polynomial:
    return _poly_trim(
        tuple(index * coefficient for index, coefficient in enumerate(polynomial[1:], 1))
    )


def poly_add(left: Polynomial, right: Polynomial) -> Polynomial:
    length = max(len(left), len(right))
    return _poly_trim(
        tuple(
            (left[index] if index < len(left) else ZERO)
            + (right[index] if index < len(right) else ZERO)
            for index in range(length)
        )
    )


def poly_subtract(left: Polynomial, right: Polynomial) -> Polynomial:
    return poly_add(left, tuple(-coefficient for coefficient in right))


def poly_multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    result = [ZERO] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            result[left_index + right_index] += left_value * right_value
    return _poly_trim(tuple(result))


def poly_evaluate(polynomial: Polynomial, value: Fraction) -> Q5:
    result = ZERO
    exact_value = q(value)
    for coefficient in reversed(polynomial):
        result = result * exact_value + coefficient
    return result


def poly_divmod(
    numerator: Polynomial, denominator: Polynomial
) -> tuple[Polynomial, Polynomial]:
    divisor = _poly_trim(denominator)
    if len(divisor) == 1 and divisor[0].is_zero():
        raise ZeroDivisionError("zero Sturm divisor")
    quotient = [ZERO] * max(1, len(numerator) - len(divisor) + 1)
    remainder = list(_poly_trim(numerator))
    while len(remainder) >= len(divisor) and not (
        len(remainder) == 1 and remainder[0].is_zero()
    ):
        degree = len(remainder) - len(divisor)
        factor = remainder[-1] / divisor[-1]
        quotient[degree] = factor
        for index, coefficient in enumerate(divisor):
            remainder[degree + index] = remainder[degree + index] - factor * coefficient
        while len(remainder) > 1 and remainder[-1].is_zero():
            remainder.pop()
    return _poly_trim(tuple(quotient)), _poly_trim(tuple(remainder))


def sturm_sequence(polynomial: Polynomial) -> tuple[Polynomial, ...]:
    sequence = [_poly_trim(polynomial), poly_derivative(polynomial)]
    while len(sequence[-1]) > 1:
        _, remainder = poly_divmod(sequence[-2], sequence[-1])
        if all(coefficient.is_zero() for coefficient in remainder):
            break
        sequence.append(tuple(-coefficient for coefficient in remainder))
    return tuple(sequence)


def sign_variations(sequence: tuple[Polynomial, ...], value: Fraction) -> int:
    signs = [poly_evaluate(polynomial, value).sign() for polynomial in sequence]
    if 0 in signs:
        raise ValueError("Sturm endpoint is a polynomial root")
    return sum(left != right for left, right in pairwise(signs))


def root_count(sequence: tuple[Polynomial, ...], lower: Fraction, upper: Fraction) -> int:
    if lower >= upper:
        raise ValueError("root-isolation interval is not increasing")
    return sign_variations(sequence, lower) - sign_variations(sequence, upper)


def lemma4_cubic(a: Q5) -> Polynomial:
    """Equation (2), low-degree coefficient first."""
    return (
        a**2 - 1,
        a**2 - 2 * a + 3,
        -(2 * a + 2),
        q(2),
    )


@dataclass(frozen=True)
class RootIntervals:
    low_maximum: tuple[Fraction, Fraction]
    minimum: tuple[Fraction, Fraction]
    extraneous: tuple[Fraction, Fraction]


DENOMINATOR = 10**12
ROOT_INTERVALS = {
    "sqrt_4_5": RootIntervals(
        (Fraction(128400289459, DENOMINATOR), Fraction(128400289460, DENOMINATOR)),
        (Fraction(853041620789, DENOMINATOR), Fraction(853041620790, DENOMINATOR)),
        (Fraction(912985280750, DENOMINATOR), Fraction(912985280751, DENOMINATOR)),
    ),
    "s_minus_2_85": RootIntervals(
        (Fraction(67734141574, DENOMINATOR), Fraction(67734141575, DENOMINATOR)),
        (Fraction(923640871094, DENOMINATOR), Fraction(923640871095, DENOMINATOR)),
        (Fraction(947479369331, DENOMINATOR), Fraction(947479369332, DENOMINATOR)),
    ),
    "0_95": RootIntervals(
        (Fraction(54264400181, DENOMINATOR), Fraction(54264400182, DENOMINATOR)),
        (Fraction(939246817865, DENOMINATOR), Fraction(939246817866, DENOMINATOR)),
        (Fraction(956488781953, DENOMINATOR), Fraction(956488781954, DENOMINATOR)),
    ),
}


def sqrt_fraction_bounds(value: Fraction) -> tuple[Fraction, Fraction]:
    if value < 0:
        raise ValueError("cannot bound the square root of a negative rational")
    scaled_floor = math.isqrt(value.numerator * SQRT_BOUND_SCALE**2 // value.denominator)
    lower = Fraction(scaled_floor, SQRT_BOUND_SCALE)
    if lower**2 == value:
        return lower, lower
    upper = Fraction(scaled_floor + 1, SQRT_BOUND_SCALE)
    if not lower**2 < value < upper**2:
        raise AssertionError("rational square-root enclosure failed")
    return lower, upper


def stationary_value_bounds(
    interval: tuple[Fraction, Fraction],
) -> tuple[Fraction, Fraction]:
    """Enclose ``sqrt(1-x^2)+x^2/(1+x)`` at the stationary root."""
    lower_x, upper_x = interval
    lower_sqrt, _ = sqrt_fraction_bounds(1 - upper_x**2)
    _, upper_sqrt = sqrt_fraction_bounds(1 - lower_x**2)
    lower = lower_sqrt + lower_x**2 / (1 + lower_x)
    upper = upper_sqrt + upper_x**2 / (1 + upper_x)
    return lower, upper


def derivative_sign_at(a: Q5, value: Fraction) -> int:
    exact_value = q(value)
    if exact_value >= a:
        return 1
    unsquared_comparison = (1 - exact_value) ** 3 - (1 + exact_value) * (a - exact_value) ** 2
    return unsquared_comparison.sign()


def root_certificate(a: Q5, interval_name: str) -> dict[str, object]:
    intervals = ROOT_INTERVALS[interval_name]
    ordered = (intervals.low_maximum, intervals.minimum, intervals.extraneous)
    sequence = sturm_sequence(lemma4_cubic(a))
    if root_count(sequence, Fraction(0), Fraction(1)) != 3:
        raise ValueError(f"Lemma 4 cubic for {interval_name} does not have three roots")
    if any(root_count(sequence, *interval) != 1 for interval in ordered):
        raise ValueError(f"a declared {interval_name} root interval is not isolating")
    if sum(root_count(sequence, *interval) for interval in ordered) != 3:
        raise ValueError(f"the {interval_name} intervals do not exhaust the cubic roots")
    if not ordered[0][1] < ordered[1][0] < ordered[1][1] < ordered[2][0]:
        raise ValueError(f"the {interval_name} intervals overlap or are misordered")
    if not q(ordered[0][1]) < a or not q(ordered[1][1]) < a:
        raise ValueError(f"a valid {interval_name} root violates x <= a")
    if not q(ordered[2][0]) > a:
        raise ValueError(f"the {interval_name} extraneous root did not violate x <= a")
    between_valid = (ordered[0][1] + ordered[1][0]) / 2
    after_minimum = (ordered[1][1] + ordered[2][0]) / 2
    signs = (
        derivative_sign_at(a, Fraction(0)),
        derivative_sign_at(a, between_valid),
        derivative_sign_at(a, after_minimum),
    )
    if signs != (1, -1, 1):
        raise ValueError(f"the {interval_name} stationary-point classification failed")
    lower, upper = stationary_value_bounds(intervals.minimum)
    if not upper < 1:
        raise ValueError(f"the {interval_name} selected minimum is not below the endpoint")
    return {
        "parameter": a.text(),
        "cubic_coefficients_low_degree_first": [value.text() for value in lemma4_cubic(a)],
        "sturm_root_count_0_1": 3,
        "root_intervals": [
            [fraction_text(lower_bound), fraction_text(upper_bound)]
            for lower_bound, upper_bound in ordered
        ],
        "unsquared_filter": {
            "valid_root_indices": [0, 1],
            "extraneous_root_indices": [2],
            "required_relation": "x<=a",
        },
        "derivative_signs": [1, -1, 1],
        "global_minimum_root_index": 1,
        "f_lower": fraction_text(lower),
        "f_upper": fraction_text(upper),
    }


def validate_lemma4(a: Q5, b: Q5, interval_name: str) -> dict[str, object]:
    if not ((a + 2) ** 2 > 8 and a < 1):
        raise ValueError("Lemma 4 requires 2*sqrt(2)-2 < a < 1")
    if not 0 < b < 1:
        raise ValueError("Lemma 4 requires 0 < b < 1")
    distance_squared = a**2 + (b - 1) ** 2
    if distance_squared > 1:
        raise ValueError("Lemma 4 endpoint lies farther than one from (0,1)")
    roots = root_certificate(a, interval_name)
    lower = Fraction(str(roots["f_lower"]))
    if q(lower) < b:
        raise ValueError(
            f"Lemma 4 threshold fails: certified f(a)>={fraction_text(lower)} < {b.text()}"
        )
    return {
        "a": a.text(),
        "b": b.text(),
        "distance_squared": distance_squared.text(),
        "threshold": roots,
        "threshold_passed": True,
    }


def validate_lemma4_failure(a: Q5, b: Q5, interval_name: str) -> dict[str, object]:
    roots = root_certificate(a, interval_name)
    upper = Fraction(str(roots["f_upper"]))
    if not q(upper) < b:
        raise ValueError("the requested Lemma 4 failure is not certified")
    return {
        "a": a.text(),
        "b": b.text(),
        "f_upper": fraction_text(upper),
        "threshold_failed": True,
    }


@dataclass(frozen=True)
class Lemma4Placement:
    identifier: str
    polygon: Face
    origin: Point
    u_axis: Point
    v_axis: Point
    a: Q5
    b: Q5
    interval_name: str


def transformed_point(origin: Point, u_axis: Point, v_axis: Point, u: Q5, v: Q5) -> Point:
    return add_points(
        origin,
        add_points(scale_point(u_axis, u), scale_point(v_axis, v)),
    )


def validate_lemma4_placement(
    placement: Lemma4Placement, points: dict[str, Point]
) -> dict[str, object]:
    if cross(placement.u_axis, placement.v_axis) ** 2 != 1:
        raise ValueError(f"{placement.identifier} local axes are not an isometry")
    expected = {
        transformed_point(placement.origin, placement.u_axis, placement.v_axis, q(0), q(0)),
        transformed_point(placement.origin, placement.u_axis, placement.v_axis, q(0), q(1)),
        transformed_point(
            placement.origin, placement.u_axis, placement.v_axis, placement.a, q(0)
        ),
        transformed_point(
            placement.origin,
            placement.u_axis,
            placement.v_axis,
            placement.a,
            placement.b,
        ),
    }
    actual = {points[name] for name in placement.polygon}
    if actual != expected:
        raise ValueError(f"{placement.identifier} is not its declared canonical quadrilateral")
    certificate = validate_lemma4(placement.a, placement.b, placement.interval_name)
    return {
        "id": placement.identifier,
        "polygon": list(placement.polygon),
        "origin": point_record(placement.origin),
        "u_axis": point_record(placement.u_axis),
        "v_axis": point_record(placement.v_axis),
        **certificate,
    }


def triangle_edge_certificate(points: dict[str, Point], face: Face) -> dict[str, object]:
    if len(face) != 3 or len(set(face)) != 3:
        raise ValueError(f"not a three-vertex triangle: {face}")
    distances = {
        "-".join(edge): squared_distance(points[edge[0]], points[edge[1]])
        for edge in edges_for_face(face)
    }
    if any(value > 1 for value in distances.values()):
        raise ValueError(f"triangle has an edge longer than one: {face}")
    return {
        "vertices": list(face),
        "squared_edge_lengths": {
            name: value.text() for name, value in sorted(distances.items())
        },
    }


def validate_triangle_mesh(
    points: dict[str, Point],
    faces: tuple[Face, ...],
    boundary: Face,
    *,
    expected_faces: int,
    declared_edges: tuple[Edge, ...] | None = None,
) -> dict[str, object]:
    if len(faces) != expected_faces:
        raise ValueError(f"expected {expected_faces} faces, got {len(faces)}")
    face_keys = [tuple(sorted(face)) for face in faces]
    if len(face_keys) != len(set(face_keys)):
        raise ValueError("triangle inventory contains a duplicate face")
    if any(len(face) != 3 or len(set(face)) != 3 for face in faces):
        raise ValueError("mesh contains a degenerate or nontriangular face")
    if any(vertex not in points for face in faces for vertex in face):
        raise ValueError("mesh references an unknown vertex")

    signed_areas = [polygon_area2(tuple(points[name] for name in face)) for face in faces]
    signs = {area.sign() for area in signed_areas}
    boundary_area = polygon_area2(tuple(points[name] for name in boundary))
    if signs != {boundary_area.sign()} or 0 in signs:
        raise ValueError("mesh faces do not share the boundary's nonzero orientation")

    incidence = Counter(edge for face in faces for edge in edges_for_face(face))
    boundary_edges = set(edges_for_face(boundary))
    if {edge for edge, count in incidence.items() if count == 1} != boundary_edges:
        raise ValueError("single-incidence edges are not exactly the declared boundary")
    if any(count not in (1, 2) for count in incidence.values()):
        raise ValueError("a mesh edge has invalid face incidence")
    derived_edges = tuple(sorted(incidence))
    if declared_edges is not None:
        if len(declared_edges) != len(set(declared_edges)):
            raise ValueError("declared mesh edge inventory contains a duplicate")
        if tuple(sorted(declared_edges)) != derived_edges:
            raise ValueError("declared mesh edges omit or invent an edge")
    validate_noncrossing(points, derived_edges)

    vertices = {vertex for face in faces for vertex in face}
    if connected_vertices(derived_edges) != vertices:
        raise ValueError("mesh edge graph is disconnected")
    if len(vertices) - len(derived_edges) + len(faces) != 1:
        raise ValueError("mesh violates the disk Euler characteristic")
    if sum(signed_areas, ZERO) != boundary_area:
        raise ValueError("mesh face areas do not exactly tile the boundary polygon")
    triangle_certificates = [triangle_edge_certificate(points, face) for face in faces]
    absolute_areas = [area if area.sign() > 0 else -area for area in signed_areas]
    minimum_area2 = min(absolute_areas)
    return {
        "face_count": len(faces),
        "edge_count": len(derived_edges),
        "vertex_count": len(vertices),
        "boundary_edge_count": len(boundary_edges),
        "euler_characteristic": 1,
        "signed_area_twice": boundary_area.text(),
        "minimum_abs_face_area_twice": minimum_area2.text(),
        "faces": triangle_certificates,
        "edges": [list(edge) for edge in derived_edges],
        "boundary": list(boundary),
        "all_edges_at_most_one": True,
        "noncrossing": True,
    }


def edge_on_container(points: dict[str, Point], edge: Edge) -> bool:
    first, second = points[edge[0]], points[edge[1]]
    return (
        (first[0].is_zero() and second[0].is_zero())
        or (first[0] == SIDE and second[0] == SIDE)
        or (first[1].is_zero() and second[1].is_zero())
        or (first[1] == SIDE and second[1] == SIDE)
    )


def validate_vertices_in_container(
    points: dict[str, Point], vertices: set[str]
) -> dict[str, object]:
    unknown = vertices - points.keys()
    if unknown:
        raise ValueError(f"tiling references unknown vertices: {sorted(unknown)}")
    ordered = sorted(vertices)
    outside = [
        name
        for name in ordered
        if not (0 <= points[name][0] <= SIDE and 0 <= points[name][1] <= SIDE)
    ]
    if outside:
        raise ValueError(f"tiling vertices lie outside [0,SIDE]^2: {outside}")
    return {
        "container_x_interval": ["0", SIDE.text()],
        "container_y_interval": ["0", SIDE.text()],
        "vertex_count": len(ordered),
        "vertices": {name: point_record(points[name]) for name in ordered},
        "all_vertices_in_closed_container": True,
    }


def validate_square_tiling(
    points: dict[str, Point], faces: tuple[Face, ...], *, expected_faces: int
) -> dict[str, object]:
    if len(faces) != expected_faces:
        raise ValueError(f"expected {expected_faces} tiling faces, got {len(faces)}")
    keys = [tuple(sorted(face)) for face in faces]
    if len(keys) != len(set(keys)):
        raise ValueError("tiling contains a duplicate face")
    vertices = {vertex for face in faces for vertex in face}
    containment = validate_vertices_in_container(points, vertices)
    signed_areas = [polygon_area2(tuple(points[name] for name in face)) for face in faces]
    signs = {area.sign() for area in signed_areas}
    if len(signs) != 1 or 0 in signs:
        raise ValueError("tiling faces do not have one nonzero orientation")
    orientation_sign = signs.pop()
    absolute_area2 = sum((area * orientation_sign for area in signed_areas), ZERO)
    if absolute_area2 != 2 * SIDE**2:
        raise ValueError("tiling face areas do not sum to the exact container area")

    incidence = Counter(edge for face in faces for edge in edges_for_face(face))
    if any(count not in (1, 2) for count in incidence.values()):
        raise ValueError("tiling edge incidence is not one or two")
    boundary_edges = {edge for edge, count in incidence.items() if count == 1}
    if not boundary_edges or any(
        not edge_on_container(points, edge) for edge in boundary_edges
    ):
        raise ValueError("tiling has a non-container single-incidence edge")
    edges = tuple(sorted(incidence))
    validate_noncrossing(points, edges)
    if connected_vertices(edges) != vertices:
        raise ValueError("tiling edge graph is disconnected")
    if len(vertices) - len(edges) + len(faces) != 1:
        raise ValueError("tiling violates the disk Euler characteristic")
    return {
        "face_count": len(faces),
        "edge_count": len(edges),
        "vertex_count": len(vertices),
        "boundary_edge_count": len(boundary_edges),
        "euler_characteristic": 1,
        "signed_area_twice": (2 * SIDE**2 * orientation_sign).text(),
        "noncrossing": True,
        "all_internal_edges_have_two_incident_faces": True,
        "all_boundary_edges_lie_on_container": True,
        "vertex_containment": containment,
    }


K4_ACTIONS = (
    ("identity", False, False),
    ("reflect_x", True, False),
    ("reflect_y", False, True),
    ("reflect_xy", True, True),
)


def apply_k4(value: Point, *, reflect_x: bool, reflect_y: bool) -> Point:
    x, y = value
    return SIDE - x if reflect_x else x, SIDE - y if reflect_y else y


def validate_k4_actions(actions: tuple[tuple[str, bool, bool], ...]) -> dict[str, object]:
    if actions != K4_ACTIONS:
        raise ValueError("Figure 13 symmetry must be exactly the centerline Klein four")
    images = {
        apply_k4(
            point(Fraction(1, 3), Fraction(2, 3)),
            reflect_x=reflect_x,
            reflect_y=reflect_y,
        )
        for _, reflect_x, reflect_y in actions
    }
    if len(images) != 4:
        raise ValueError("K4 actions are not faithful")
    return {
        "order": 4,
        "group": "C2 x C2 (horizontal and vertical centerline reflections)",
        "actions": [name for name, _, _ in actions],
    }


def figure13_points() -> dict[str, Point]:
    return {
        "P0": point(1, 1),
        "P1": point(CENTER, 1),
        "P2": point(SIDE - 1, 1),
        "M0": point(U, CENTER),
        "M1": point(V, CENTER),
        "M2": point(SIDE - V, CENTER),
        "M3": point(SIDE - U, CENTER),
        "T0": point(1, SIDE - 1),
        "T1": point(CENTER, SIDE - 1),
        "T2": point(SIDE - 1, SIDE - 1),
    }


FIGURE13_TRIANGLES: tuple[Face, ...] = (
    ("M0", "P0", "M1"),
    ("P0", "P1", "M1"),
    ("M1", "P1", "M2"),
    ("P1", "P2", "M2"),
    ("M2", "P2", "M3"),
    ("T0", "M0", "M1"),
    ("T0", "M1", "T1"),
    ("T1", "M1", "M2"),
    ("T1", "M2", "T2"),
    ("T2", "M2", "M3"),
)


def figure13_geometry() -> tuple[dict[str, Point], tuple[Face, ...], tuple[Face, ...]]:
    points = {
        **figure13_points(),
        "K00": point(0, 0),
        "K10": point(1, 0),
        "KC0": point(CENTER, 0),
        "KR0": point(SIDE - 1, 0),
        "KS0": point(SIDE, 0),
        "L1": point(0, 1),
        "LC": point(0, CENTER),
        "LR": point(0, SIDE - 1),
        "LTOP": point(0, SIDE),
        "R1": point(SIDE, 1),
        "RC": point(SIDE, CENTER),
        "RR": point(SIDE, SIDE - 1),
        "RTOP": point(SIDE, SIDE),
        "TOP1": point(1, SIDE),
        "TOPC": point(CENTER, SIDE),
        "TOPR": point(SIDE - 1, SIDE),
    }
    covered = (
        ("K00", "K10", "P0", "L1"),
        ("KR0", "KS0", "R1", "P2"),
        ("LR", "T0", "TOP1", "LTOP"),
        ("T2", "RR", "RTOP", "TOPR"),
        ("L1", "P0", "M0", "LC"),
        ("LC", "M0", "T0", "LR"),
        ("P2", "R1", "RC", "M3"),
        ("M3", "RC", "RR", "T2"),
        *FIGURE13_TRIANGLES,
    )
    exceptions = (
        ("K10", "KC0", "P1", "P0"),
        ("KC0", "KR0", "P2", "P1"),
        ("T0", "T1", "TOPC", "TOP1"),
        ("T1", "T2", "TOPR", "TOPC"),
    )
    return points, covered, exceptions


def figure13_lemma4_placements() -> tuple[Lemma4Placement, ...]:
    return (
        Lemma4Placement(
            "left_lower",
            ("L1", "P0", "M0", "LC"),
            point(0, 1),
            point(0, 1),
            point(1, 0),
            A0,
            U,
            "sqrt_4_5",
        ),
        Lemma4Placement(
            "left_upper",
            ("LC", "M0", "T0", "LR"),
            point(0, SIDE - 1),
            point(0, -1),
            point(1, 0),
            A0,
            U,
            "sqrt_4_5",
        ),
        Lemma4Placement(
            "right_lower",
            ("P2", "R1", "RC", "M3"),
            point(SIDE, 1),
            point(0, 1),
            point(-1, 0),
            A0,
            U,
            "sqrt_4_5",
        ),
        Lemma4Placement(
            "right_upper",
            ("M3", "RC", "RR", "T2"),
            point(SIDE, SIDE - 1),
            point(0, -1),
            point(-1, 0),
            A0,
            U,
            "sqrt_4_5",
        ),
    )


def validate_polygon_partition(
    points: dict[str, Point],
    faces: tuple[Face, ...],
    boundary: Face,
    *,
    expected_faces: int,
) -> dict[str, object]:
    if len(faces) != expected_faces:
        raise ValueError(f"expected {expected_faces} partition faces, got {len(faces)}")
    keys = [tuple(sorted(face)) for face in faces]
    if len(keys) != len(set(keys)):
        raise ValueError("polygon partition has duplicate faces")
    areas = [polygon_area2(tuple(points[name] for name in face)) for face in faces]
    boundary_area = polygon_area2(tuple(points[name] for name in boundary))
    if {area.sign() for area in areas} != {boundary_area.sign()} or boundary_area.is_zero():
        raise ValueError("polygon partition orientations disagree")
    if sum(areas, ZERO) != boundary_area:
        raise ValueError("polygon partition areas do not sum to its boundary")
    incidence = Counter(edge for face in faces for edge in edges_for_face(face))
    if {edge for edge, count in incidence.items() if count == 1} != set(
        edges_for_face(boundary)
    ):
        raise ValueError("polygon partition boundary incidence is incomplete")
    if any(count not in (1, 2) for count in incidence.values()):
        raise ValueError("polygon partition has invalid edge incidence")
    edges = tuple(sorted(incidence))
    validate_noncrossing(points, edges)
    return {
        "face_count": len(faces),
        "edge_count": len(edges),
        "signed_area_twice": boundary_area.text(),
        "noncrossing": True,
    }


def figure13_certificate() -> dict[str, object]:
    points, covered, exceptions = figure13_geometry()
    source_points = figure13_points()
    seeds = (source_points["P0"], source_points["P1"], source_points["M0"], source_points["M1"])
    orbit = {
        apply_k4(seed, reflect_x=reflect_x, reflect_y=reflect_y)
        for seed in seeds
        for _, reflect_x, reflect_y in K4_ACTIONS
    }
    if orbit != set(source_points.values()) or len(orbit) != 10:
        raise ValueError("Figure 13 seed orbit does not reproduce the ten-point manifest")
    quarter_turn_image = point(SIDE - 1, CENTER)
    if quarter_turn_image in orbit:
        raise ValueError("Figure 13 unexpectedly has quarter-turn symmetry")

    representative_exception = frozenset(points[name] for name in exceptions[0])
    exception_orbit = {
        frozenset(
            apply_k4(value, reflect_x=reflect_x, reflect_y=reflect_y)
            for value in representative_exception
        )
        for _, reflect_x, reflect_y in K4_ACTIONS
    }
    actual_exceptions = {frozenset(points[name] for name in face) for face in exceptions}
    if exception_orbit != actual_exceptions:
        raise ValueError("Figure 13 exceptions are not exactly one K4 orbit")

    tiling = validate_square_tiling(points, covered + exceptions, expected_faces=22)
    if len(covered) != 18 or len(exceptions) != 4:
        raise ValueError("Figure 13 cover/exception inventory drifted")
    for face in FIGURE13_TRIANGLES:
        certificate = triangle_edge_certificate(points, face)
        squared_lengths = certificate["squared_edge_lengths"]
        if not isinstance(squared_lengths, dict) or sorted(squared_lengths.values()) != [
            "1",
            "1",
            "4/5",
        ]:
            raise ValueError("Figure 13 congruent-triangle metric drifted")
    lemma4 = [
        validate_lemma4_placement(placement, points)
        for placement in figure13_lemma4_placements()
    ]
    corner_rectangles = covered[:4]
    if any(
        max(
            squared_distance(points[face[index]], points[face[(index + 1) % 4]])
            for index in range(4)
        )
        > 1
        for face in corner_rectangles
    ):
        raise ValueError("a Figure 13 Lemma 1 corner rectangle exceeds unit side")
    point_digest = points_digest(source_points)
    if point_digest != FIGURE13_POINT_SHA256:
        raise ValueError("Figure 13 exact point manifest digest drifted")
    triangle_mesh_summary: dict[str, object] = {
        "all_edges_at_most_one": True,
    }
    return {
        "point_manifest": {
            name: point_record(source_points[name]) for name in sorted(source_points)
        },
        "point_digest": point_digest,
        "source_seed_names": ["P0", "P1", "M0", "M1"],
        "symmetry": validate_k4_actions(K4_ACTIONS),
        "quarter_turn_counterexample": {
            "source_point": "P1",
            "image": point_record(quarter_turn_image),
            "image_absent": True,
        },
        "cover": {
            "lemma1_corner_cells": [list(face) for face in covered[:4]],
            "lemma4_side_cells": lemma4,
            "lemma2_triangles": [
                triangle_edge_certificate(points, face) for face in FIGURE13_TRIANGLES
            ],
            "covered_cell_count": len(covered),
            "exception_rectangles": [list(face) for face in exceptions],
            "exception_count": len(exceptions),
            "tiling": tiling,
            "boundary_closure": lemma2_boundary_closure(triangle_mesh_summary),
        },
        "localization": {
            "statement": (
                "a box avoiding all ten points has center in one of four exception "
                "rectangles related by K4"
            ),
            "representative": list(exceptions[0]),
            "certified": True,
        },
    }


def point_in_closed_convex_polygon(value: Point, polygon: tuple[Point, ...]) -> bool:
    signs = {
        orient(polygon[index], polygon[(index + 1) % len(polygon)], value).sign()
        for index in range(len(polygon))
    }
    signs.discard(0)
    return len(signs) <= 1


def lemma6_exact_constants() -> dict[str, object]:
    sin_double = 5 - 2 * SQRT5
    sum_sin_cos = SQRT5 - 1
    if not 0 < sin_double < 1 or not sum_sin_cos > 0:
        raise ValueError("Lemma 6 trigonometric root sign premises failed")
    if sum_sin_cos**2 != 1 + sin_double:
        raise ValueError("Lemma 6 sin/cos identity failed")
    if not sum_sin_cos > Fraction(28, 25):
        raise ValueError("Lemma 6 apex-height prerequisite failed")
    product_sin_cos = sin_double / 2
    if not product_sin_cos > 0:
        raise ValueError("Lemma 6 D(theta_0) denominator is not positive")
    if (sum_sin_cos - 1) / product_sin_cos != A0:
        raise ValueError("Lemma 6 D(theta_0)=sqrt(4/5) identity failed")
    tan_lower = Fraction(3, 25) * SQRT5
    sin_double_at_lower = 2 * tan_lower / (1 + tan_lower**2)
    if not 0 < tan_lower < 1 or not 0 < sin_double_at_lower < 1:
        raise ValueError("Lemma 6 tangent-comparison domain premises failed")
    if not sin_double_at_lower < sin_double:
        raise ValueError("Lemma 6 exact tangent lower bound failed")
    if not 1 + tan_lower / SQRT5 == Fraction(28, 25):
        raise ValueError("Lemma 6 height threshold normalization failed")

    # D'(t) has the sign of (t-1)F(t), where
    # F=t^2+t+1-(t+1)sqrt(1+t^2).  Squaring its positive sides leaves t^2,
    # so F>0 for t>0 and D decreases on 0<t<1.  D is symmetric about 45 degrees.
    t_squared_plus_t_plus_one = (q(1), q(1), q(1))
    t_plus_one = (q(1), q(1))
    t_squared_plus_one = (q(1), q(0), q(1))
    d_monotonicity_gap = poly_subtract(
        poly_multiply(t_squared_plus_t_plus_one, t_squared_plus_t_plus_one),
        poly_multiply(poly_multiply(t_plus_one, t_plus_one), t_squared_plus_one),
    )
    if d_monotonicity_gap != (q(0), q(0), q(1)):
        raise ValueError("Lemma 6 D monotonicity identity failed")
    d_left_positive = (
        all(coefficient.sign() >= 0 for coefficient in t_squared_plus_t_plus_one)
        and t_squared_plus_t_plus_one[0].sign() > 0
    )
    d_right_positive = (
        all(coefficient.sign() >= 0 for coefficient in t_plus_one)
        and t_plus_one[0].sign() > 0
        and all(coefficient.sign() >= 0 for coefficient in t_squared_plus_one)
        and t_squared_plus_one[0].sign() > 0
    )
    if not d_left_positive or not d_right_positive:
        raise ValueError("Lemma 6 D monotonicity squaring signs failed")

    # For h(t)=1+(D(t)-1/sqrt(5))*t, h'(t)>0 follows after squaring from
    # (1+t+2t^2)^2-(1+t^2)(2t+1/sqrt(5))^2, whose coefficients are positive.
    height_left = (q(1), q(1), q(2))
    height_right = (SQRT5 / 5, q(2))
    height_derivative_gap = poly_subtract(
        poly_multiply(height_left, height_left),
        poly_multiply(t_squared_plus_one, poly_multiply(height_right, height_right)),
    )
    if len(height_derivative_gap) != 4 or any(
        coefficient.sign() <= 0 for coefficient in height_derivative_gap
    ):
        raise ValueError("Lemma 6 height monotonicity polynomial failed")
    height_left_positive = all(coefficient.sign() > 0 for coefficient in height_left)
    height_right_positive = all(coefficient.sign() > 0 for coefficient in height_right)
    if not height_left_positive or not height_right_positive:
        raise ValueError("Lemma 6 height monotonicity squaring signs failed")
    tangent_map_derivative_numerator = (q(2), q(0), q(-2))
    tangent_map_increases_below_one = (
        tangent_map_derivative_numerator == (q(2), q(0), q(-2))
        and tangent_map_derivative_numerator[0].sign() > 0
        and tangent_map_derivative_numerator[2].sign() < 0
    )
    sign_premises = {
        "sin_2theta0_in_open_unit_interval": 0 < sin_double < 1,
        "sin_theta0_plus_cos_theta0_positive": sum_sin_cos > 0,
        "sin_theta0_cos_theta0_positive": product_sin_cos > 0,
        "tangent_lower_bound_in_open_unit_interval": 0 < tan_lower < 1,
        "tangent_map_derivative_positive_on_0_1": tangent_map_increases_below_one,
        "D_factor_left_side_positive": d_left_positive,
        "D_factor_right_side_positive": d_right_positive,
        "D_squared_gap_t_squared_strictly_positive_for_t_gt_zero": (
            d_monotonicity_gap == (q(0), q(0), q(1))
        ),
        "height_derivative_left_side_positive": height_left_positive,
        "height_derivative_right_side_positive": height_right_positive,
        "height_derivative_squared_gap_positive": all(
            coefficient.sign() > 0 for coefficient in height_derivative_gap
        ),
    }
    if not all(sign_premises.values()):
        failed = sorted(name for name, passed in sign_premises.items() if not passed)
        raise ValueError(f"Lemma 6 squared-inequality sign premises failed: {failed}")
    return {
        "sin_2theta0": sin_double.text(),
        "sin_theta0_plus_cos_theta0": sum_sin_cos.text(),
        "D_theta0": A0.text(),
        "tan_theta0_strict_lower_bound": tan_lower.text(),
        "critical_height_strict_lower_bound": "28/25",
        "D_monotonicity_squared_gap_coefficients": [
            coefficient.text() for coefficient in d_monotonicity_gap
        ],
        "height_derivative_squared_gap_coefficients": [
            coefficient.text() for coefficient in height_derivative_gap
        ],
        "squared_inequality_sign_premises": {
            "angle_domain": "0<theta<=45 degrees, hence 0<t=tan(theta)<=1",
            "tangent_map_derivative": "2(1-t^2)/(1+t^2)^2 > 0 for 0<t<1",
            **sign_premises,
            "all_sign_premises_checked_before_squaring": True,
        },
        "D_outside_central_angle_interval_strictly_exceeds_a": True,
        "critical_height_increases_from_theta0_to_45_degrees": True,
        "identities_replayed_exactly": True,
    }


def triple_forcing_certificate() -> dict[str, object]:
    points = {
        "BASE1": point(1, 0),
        "BASEC": point(CENTER, 0),
        "P0": point(1, 1),
        "P1": point(CENTER, 1),
        "A1": point(1, Fraction(9, 10)),
        "A2": point(CENTER, Fraction(9, 10)),
        "A3": point(V, Fraction(28, 25)),
    }
    exception = ("BASE1", "BASEC", "P1", "P0")
    a2_quad = ("BASE1", "BASEC", "A2", "P0")
    a2_cap = ("P0", "A2", "P1")
    a1_quad = ("BASE1", "BASEC", "P1", "A1")
    a1_cap = ("A1", "P1", "P0")
    a2_partition = validate_polygon_partition(
        points,
        (a2_quad, a2_cap),
        ("BASE1", "BASEC", "A2", "P1", "P0"),
        expected_faces=2,
    )
    a1_partition = validate_polygon_partition(
        points,
        (a1_quad, a1_cap),
        ("BASE1", "BASEC", "P1", "P0", "A1"),
        expected_faces=2,
    )
    a2_placement = Lemma4Placement(
        "force_A2",
        a2_quad,
        points["BASE1"],
        point(1, 0),
        point(0, 1),
        A0,
        q(Fraction(9, 10)),
        "sqrt_4_5",
    )
    a1_placement = Lemma4Placement(
        "force_A1",
        a1_quad,
        points["BASEC"],
        point(-1, 0),
        point(0, 1),
        A0,
        q(Fraction(9, 10)),
        "sqrt_4_5",
    )
    a1_triangle = triangle_edge_certificate(points, a1_cap)
    a2_triangle = triangle_edge_certificate(points, a2_cap)

    lemma6_pentagon_names = ("BASE1", "BASEC", "P1", "A3", "P0")
    lemma6_pentagon = tuple(points[name] for name in lemma6_pentagon_names)
    if polygon_area2(lemma6_pentagon).sign() <= 0:
        raise ValueError("Lemma 6 pentagon orientation failed")
    if not all(
        point_in_closed_convex_polygon(points[name], lemma6_pentagon) for name in exception
    ):
        raise ValueError("the representative exception is not inside the Lemma 6 pentagon")
    if points["A3"] != point(1 + A0 / 2, Fraction(28, 25)):
        raise ValueError("Lemma 6 apex does not match A3")
    return {
        "representative_exception": list(exception),
        "avoided_figure13_points": ["P0", "P1"],
        "avoided_container_boundary": "y=0",
        "A1": {
            "lemma4": validate_lemma4_placement(a1_placement, points),
            "complement_triangle": a1_triangle,
            "partition": a1_partition,
        },
        "A2": {
            "lemma4": validate_lemma4_placement(a2_placement, points),
            "complement_triangle": a2_triangle,
            "partition": a2_partition,
        },
        "A3": {
            "lemma6_pentagon": list(lemma6_pentagon_names),
            "exception_contained": True,
            "exact_constants": lemma6_exact_constants(),
        },
        "symmetry_normalization": {
            "action": (
                "apply the K4 isometry carrying the actual exception to the representative"
            ),
            "scope": (
                "reflect the container and every box before defining the repaired Figure 14 set"
            ),
            "unavoidability_invariance": "the inverse reflection carries the certificate back",
        },
        "logical_conclusion": (
            "avoidance of y=0, P0, and P1 leaves A1, A2, and A3 as the forced alternatives"
        ),
        "all_three_forced_in_same_box": True,
    }


def figure14_points(g_x: Fraction) -> dict[str, Point]:
    return {
        "A1": point(1, Fraction(9, 10)),
        "A2": point(CENTER, Fraction(9, 10)),
        "A3": point(V, Fraction(28, 25)),
        "B": point(SIDE - 1, 1),
        "C": point(SIDE - Fraction(9, 10), CENTER),
        "D": point(SIDE - 1, SIDE - 1),
        "E": point(CENTER, SIDE - Fraction(9, 10)),
        "F": point(1, SIDE - 1),
        "G": point(g_x, Fraction(37, 20)),
        "H": point(Fraction(3, 2), Fraction(21, 10)),
        "I": point(Fraction(21, 10), Fraction(21, 10)),
        "J": point(Fraction(21, 10), Fraction(3, 2)),
    }


FIGURE14_BOUNDARY: Face = ("F", "E", "D", "C", "B", "A2", "A3", "A1", "G")
FIGURE14_TRIANGLES: tuple[Face, ...] = (
    ("F", "E", "H"),
    ("E", "I", "H"),
    ("E", "D", "I"),
    ("D", "C", "I"),
    ("C", "J", "I"),
    ("I", "J", "H"),
    ("C", "B", "J"),
    ("B", "A2", "J"),
    ("A2", "A3", "J"),
    ("A3", "H", "J"),
    ("A3", "G", "H"),
    ("G", "F", "H"),
    ("G", "A3", "A1"),
)


def figure14_geometry(g_x: Fraction) -> tuple[dict[str, Point], tuple[Face, ...]]:
    points = {
        **figure14_points(g_x),
        "K00": point(0, 0),
        "BOT1": point(1, 0),
        "BOTC": point(CENTER, 0),
        "BOTR": point(SIDE - 1, 0),
        "K40": point(SIDE, 0),
        "L09": point(0, Fraction(9, 10)),
        "L185": point(0, Fraction(37, 20)),
        "LS1": point(0, SIDE - 1),
        "K04": point(0, SIDE),
        "R1": point(SIDE, 1),
        "RC": point(SIDE, CENTER),
        "RS1": point(SIDE, SIDE - 1),
        "K44": point(SIDE, SIDE),
        "TOP1": point(1, SIDE),
        "TOPC": point(CENTER, SIDE),
        "TOPR": point(SIDE - 1, SIDE),
    }
    outer = (
        ("K00", "L09", "A1", "BOT1"),
        ("BOTR", "B", "R1", "K40"),
        ("LS1", "K04", "TOP1", "F"),
        ("D", "TOPR", "K44", "RS1"),
        ("BOT1", "A1", "A2", "BOTC"),
        ("A1", "A3", "A2"),
        ("L09", "L185", "G", "A1"),
        ("L185", "LS1", "F", "G"),
        ("F", "TOP1", "TOPC", "E"),
        ("E", "TOPC", "TOPR", "D"),
        ("C", "D", "RS1", "RC"),
        ("B", "C", "RC", "R1"),
        ("BOTC", "A2", "B", "BOTR"),
    )
    return points, outer


def figure14_lemma4_placements(g_x: Fraction) -> tuple[Lemma4Placement, ...]:
    repaired_b = q(g_x)
    return (
        Lemma4Placement(
            "A2_B",
            ("BOTC", "A2", "B", "BOTR"),
            point(SIDE - 1, 0),
            point(-1, 0),
            point(0, 1),
            A0,
            q(Fraction(9, 10)),
            "sqrt_4_5",
        ),
        Lemma4Placement(
            "B_C",
            ("B", "C", "RC", "R1"),
            point(SIDE, 1),
            point(0, 1),
            point(-1, 0),
            A0,
            q(Fraction(9, 10)),
            "sqrt_4_5",
        ),
        Lemma4Placement(
            "C_D",
            ("C", "D", "RS1", "RC"),
            point(SIDE, SIDE - 1),
            point(0, -1),
            point(-1, 0),
            A0,
            q(Fraction(9, 10)),
            "sqrt_4_5",
        ),
        Lemma4Placement(
            "D_E",
            ("E", "TOPC", "TOPR", "D"),
            point(SIDE - 1, SIDE),
            point(-1, 0),
            point(0, -1),
            A0,
            q(Fraction(9, 10)),
            "sqrt_4_5",
        ),
        Lemma4Placement(
            "E_F",
            ("F", "TOP1", "TOPC", "E"),
            point(1, SIDE),
            point(1, 0),
            point(0, -1),
            A0,
            q(Fraction(9, 10)),
            "sqrt_4_5",
        ),
        Lemma4Placement(
            "F_G",
            ("L185", "LS1", "F", "G"),
            point(0, SIDE - 1),
            point(0, -1),
            point(1, 0),
            SIDE - Fraction(57, 20),
            repaired_b,
            "s_minus_2_85",
        ),
        Lemma4Placement(
            "G_A1",
            ("L09", "L185", "G", "A1"),
            point(0, Fraction(9, 10)),
            point(0, 1),
            point(1, 0),
            q(Fraction(19, 20)),
            repaired_b,
            "0_95",
        ),
    )


def validate_lemma3_bottom(points: dict[str, Point], face: Face) -> dict[str, object]:
    expected = {
        point(1, 0),
        point(CENTER, 0),
        point(1, Fraction(9, 10)),
        point(CENTER, Fraction(9, 10)),
    }
    if {points[name] for name in face} != expected:
        raise ValueError("Figure 14 bottom rectangle geometry drifted")
    b = q(Fraction(9, 10))
    left = A0 + 2 * b
    if not A0 <= 1 or not b <= 1 or not left**2 <= 8:
        raise ValueError("Figure 14 bottom rectangle fails Lemma 3")
    return {
        "polygon": list(face),
        "a": A0.text(),
        "b": b.text(),
        "a_plus_2b": left.text(),
        "condition_a_plus_2b_at_most_2sqrt2": True,
    }


def lemma2_boundary_closure(mesh: dict[str, object]) -> dict[str, object]:
    if mesh.get("all_edges_at_most_one") is not True:
        raise ValueError("boundary closure requires every Lemma 2 edge to be at most one")
    return {
        "box_semantics": "open square of side L>1",
        "edge_argument": (
            "a center on a segment of length <=1 is within <=1/2 of an endpoint; "
            "the open box contains the open Euclidean disk of radius L/2>1/2"
        ),
        "vertices": "a center at a marked vertex contains that vertex",
        "closed_cell_union": True,
        "all_shared_triangle_boundaries_covered": True,
    }


def figure14_certificate(g_x: Fraction) -> dict[str, object]:
    points, outer = figure14_geometry(g_x)
    source_points = figure14_points(g_x)
    mesh = validate_triangle_mesh(
        points,
        FIGURE14_TRIANGLES,
        FIGURE14_BOUNDARY,
        expected_faces=13,
    )
    topology_digest = canonical_digest(
        {"boundary": FIGURE14_BOUNDARY, "faces": FIGURE14_TRIANGLES}
    )
    if topology_digest != FIGURE14_TOPOLOGY_SHA256:
        raise ValueError("Figure 14 vector-path topology digest drifted")
    full_tiling = validate_square_tiling(points, outer + FIGURE14_TRIANGLES, expected_faces=26)
    if len(outer) != 13:
        raise ValueError("Figure 14 outer face inventory drifted")
    corner_faces = outer[:4]
    if any(
        max(
            squared_distance(points[face[index]], points[face[(index + 1) % 4]])
            for index in range(4)
        )
        > 1
        for face in corner_faces
    ):
        raise ValueError("a Figure 14 Lemma 1 corner rectangle exceeds unit side")
    lemma3 = validate_lemma3_bottom(points, outer[4])
    cap = triangle_edge_certificate(points, outer[5])
    lemma4 = [
        validate_lemma4_placement(placement, points)
        for placement in figure14_lemma4_placements(g_x)
    ]
    point_digest = points_digest(source_points)
    expected_point_digest = {
        Fraction(4, 5): PRINTED_FIGURE14_POINT_SHA256,
        Fraction(79, 100): REPAIRED_FIGURE14_POINT_SHA256,
    }.get(g_x)
    if expected_point_digest is None or point_digest != expected_point_digest:
        raise ValueError("Figure 14 exact point manifest digest drifted")
    return {
        "point_manifest": {
            name: point_record(source_points[name]) for name in sorted(source_points)
        },
        "point_digest": point_digest,
        "outer_cover": {
            "lemma1_corner_rectangles": [list(face) for face in corner_faces],
            "lemma3_bottom_rectangle": lemma3,
            "lemma2_bottom_cap": cap,
            "lemma4_quadrilaterals": lemma4,
            "inventory": {
                "lemma1": 4,
                "lemma3": 1,
                "lemma2_cap": 1,
                "lemma4": 7,
                "total": 13,
            },
        },
        "central_mesh": mesh,
        "topology_digest": topology_digest,
        "full_tiling": full_tiling,
        "boundary_closure": lemma2_boundary_closure(mesh),
        "unavoidable": True,
    }


def source_distinct_delta() -> dict[str, object]:
    printed = figure14_points(Fraction(4, 5))
    repaired = figure14_points(Fraction(79, 100))
    changes = [
        {
            "point": name,
            "printed": point_record(printed[name]),
            "repaired": point_record(repaired[name]),
        }
        for name in sorted(printed)
        if printed[name] != repaired[name]
    ]
    if changes != [
        {
            "point": "G",
            "printed": ["4/5", "37/20"],
            "repaired": ["79/100", "37/20"],
        }
    ]:
        raise ValueError("H-041 is not the preregistered one-coordinate source delta")
    if points_digest(printed) != PRINTED_FIGURE14_POINT_SHA256:
        raise ValueError("printed Figure 14 point digest drifted")
    if points_digest(repaired) != REPAIRED_FIGURE14_POINT_SHA256:
        raise ValueError("repaired Figure 14 point digest drifted")
    return {
        "printed_point_digest": points_digest(printed),
        "repaired_point_digest": points_digest(repaired),
        "changed_coordinates": changes,
        "source_attribution": "repair proposed after H-010 falsification; not Stromquist's set",
    }


def source_binding() -> dict[str, object]:
    pdf_hash = sha256(PDF)
    raw_hash = sha256(RAW_SOURCE)
    if pdf_hash != PDF_SHA256:
        raise ValueError(f"Stromquist PDF hash drifted: {pdf_hash}")
    if raw_hash != RAW_SOURCE_SHA256:
        raise ValueError(f"Stromquist raw-source hash drifted: {raw_hash}")
    raw_text = RAW_SOURCE.read_text()
    if "G = (.8, 1.85)" not in raw_text:
        raise ValueError("bound source no longer contains the printed Figure 14 G coordinate")
    return {
        "paper": "Walter Stromquist, Packing 10 or 11 Unit Squares in a Square (2003)",
        "pdf": str(PDF.relative_to(ROOT)),
        "pdf_sha256": pdf_hash,
        "raw_source": str(RAW_SOURCE.relative_to(ROOT)),
        "raw_source_sha256": raw_hash,
        "figure_page": 9,
        "independent_vector_extraction": {
            "pdftocairo_page9_svg_sha256": PAGE_9_SVG_SHA256,
            "topology_path_sha256": PAGE_9_TOPOLOGY_PATH_SHA256,
            "role": "provenance attestation only; exact formulas and topology decide",
            "runtime_verified": False,
            "decisive": False,
        },
        "printed_G_token_present": True,
        "decisive_runtime_hashes_verified": ["pdf_sha256", "raw_source_sha256"],
    }


def capacity_certificate(
    *,
    point_capacity: int = 1,
    initial_boxes: int = 11,
    figure13_points_count: int = 10,
    figure14_points_count: int = 12,
    forced_points_in_special_box: int = 3,
) -> dict[str, object]:
    if point_capacity != 1:
        raise ValueError("pairwise-disjoint open boxes give each marked point capacity one")
    if initial_boxes <= figure13_points_count * point_capacity:
        raise ValueError("Figure 13 pigeonhole node no longer forces an avoiding box")
    remaining_boxes = initial_boxes - 1
    remaining_points = figure14_points_count - forced_points_in_special_box
    if remaining_boxes <= remaining_points * point_capacity:
        raise ValueError("the final 3+9 capacity contradiction was weakened away")
    if (
        initial_boxes,
        figure13_points_count,
        figure14_points_count,
        forced_points_in_special_box,
        remaining_boxes,
        remaining_points,
    ) != (11, 10, 12, 3, 10, 9):
        raise ValueError("capacity inventory drifted from H-041's preregistered chain")
    return {
        "point_capacity": point_capacity,
        "capacity_reason": "pairwise-disjoint open boxes cannot share a marked point",
        "node_1": {
            "boxes": initial_boxes,
            "figure13_points": figure13_points_count,
            "conclusion": "at least one box avoids all ten points",
        },
        "node_5": {
            "special_box_consumes": forced_points_in_special_box,
            "consumption_semantics": (
                "at least these three points; consuming more only strengthens the count"
            ),
            "remaining_boxes": remaining_boxes,
            "remaining_figure14_points": remaining_points,
            "contradiction": f"{remaining_boxes}>{remaining_points}",
        },
        "certified": True,
    }


def validate_selected_root(a: Q5, interval_name: str, selected_index: int) -> None:
    certificate = root_certificate(a, interval_name)
    if selected_index != certificate["global_minimum_root_index"]:
        raise ValueError("record selected a non-minimizing or extraneous Lemma 4 root")


def validate_record_invariants(record: dict[str, object]) -> None:
    if record.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("record schema version is stale")
    binding = record.get("source_binding")
    if not isinstance(binding, dict):
        raise TypeError("record source binding is malformed")
    if (
        binding.get("pdf_sha256") != PDF_SHA256
        or binding.get("raw_source_sha256") != RAW_SOURCE_SHA256
    ):
        raise ValueError("record source binding is stale")
    nodes = record.get("five_node_chain")
    if not isinstance(nodes, list):
        raise TypeError("record five-node chain is malformed")
    node_ids = [node.get("id") for node in nodes if isinstance(node, dict)]
    if node_ids != [1, 2, 3, 4, 5] or len(node_ids) != len(set(node_ids)):
        raise ValueError("record duplicates, omits, or reorders a proof node")
    figure14 = record.get("figure14_repaired")
    if not isinstance(figure14, dict):
        raise TypeError("record Figure 14 certificate is malformed")
    mesh = figure14.get("central_mesh")
    if not isinstance(mesh, dict):
        raise TypeError("record Figure 14 mesh is malformed")
    faces = mesh.get("faces")
    edges = mesh.get("edges")
    if not isinstance(faces, list) or len(faces) != 13:
        raise ValueError("record omits or duplicates a Figure 14 face")
    face_keys = []
    for face in faces:
        if not isinstance(face, dict) or not isinstance(face.get("vertices"), list):
            raise TypeError("record contains a malformed Figure 14 face")
        face_keys.append(tuple(sorted(str(name) for name in face["vertices"])))
    if len(face_keys) != len(set(face_keys)):
        raise ValueError("record duplicates a Figure 14 face")
    if not isinstance(edges, list) or len(edges) != len({tuple(edge) for edge in edges}):
        raise ValueError("record duplicates or malforms a Figure 14 edge")


def _raises_expected_error(action: Callable[[], object]) -> bool:
    try:
        action()
    except TypeError, ValueError:
        return True
    return False


def run_selftests(core_record: dict[str, object]) -> dict[str, bool]:
    repaired_points, repaired_outer = figure14_geometry(Fraction(79, 100))
    outside_points = dict(repaired_points)
    outside_points["H"] = point(SIDE + Fraction(1, 100), Fraction(21, 10))
    repaired_vertices = {
        vertex for face in repaired_outer + FIGURE14_TRIANGLES for vertex in face
    }
    derived_edges = tuple(
        sorted({edge for face in FIGURE14_TRIANGLES for edge in edges_for_face(face)})
    )
    stale = copy.deepcopy(core_record)
    stale_binding = stale["source_binding"]
    if not isinstance(stale_binding, dict):
        raise TypeError("internal stale-record fixture is malformed")
    stale_binding["pdf_sha256"] = "0" * 64
    duplicate_record = copy.deepcopy(core_record)
    duplicate_nodes = duplicate_record["five_node_chain"]
    if not isinstance(duplicate_nodes, list):
        raise TypeError("internal duplicate-record fixture is malformed")
    duplicate_nodes.append(copy.deepcopy(duplicate_nodes[-1]))
    results = {
        "printed_g_080_threshold_failure_certified": validate_lemma4_failure(
            q(Fraction(19, 20)), q(Fraction(4, 5)), "0_95"
        )["threshold_failed"]
        is True,
        "printed_g_080_full_cover_rejected": _raises_expected_error(
            lambda: figure14_certificate(Fraction(4, 5))
        ),
        "omitted_face_rejected": _raises_expected_error(
            lambda: validate_triangle_mesh(
                repaired_points,
                FIGURE14_TRIANGLES[:-1],
                FIGURE14_BOUNDARY,
                expected_faces=13,
            )
        ),
        "duplicated_face_rejected": _raises_expected_error(
            lambda: validate_triangle_mesh(
                repaired_points,
                (*FIGURE14_TRIANGLES[:-1], FIGURE14_TRIANGLES[0]),
                FIGURE14_BOUNDARY,
                expected_faces=13,
            )
        ),
        "omitted_edge_rejected": _raises_expected_error(
            lambda: validate_triangle_mesh(
                repaired_points,
                FIGURE14_TRIANGLES,
                FIGURE14_BOUNDARY,
                expected_faces=13,
                declared_edges=derived_edges[:-1],
            )
        ),
        "duplicated_edge_rejected": _raises_expected_error(
            lambda: validate_triangle_mesh(
                repaired_points,
                FIGURE14_TRIANGLES,
                FIGURE14_BOUNDARY,
                expected_faces=13,
                declared_edges=(*derived_edges, derived_edges[0]),
            )
        ),
        "outside_tiling_vertex_rejected": _raises_expected_error(
            lambda: validate_vertices_in_container(outside_points, repaired_vertices)
        ),
        "d4_misuse_rejected": _raises_expected_error(
            lambda: validate_k4_actions((*K4_ACTIONS, ("swap_axes", False, False)))
        ),
        "bad_threshold_rejected": _raises_expected_error(
            lambda: validate_lemma4(q(Fraction(19, 20)), q(Fraction(81, 100)), "0_95")
        ),
        "extraneous_root_rejected": _raises_expected_error(
            lambda: validate_selected_root(q(Fraction(19, 20)), "0_95", 2)
        ),
        "weakened_capacity_rejected": _raises_expected_error(
            lambda: capacity_certificate(point_capacity=2)
        ),
        "duplicate_record_node_rejected": _raises_expected_error(
            lambda: validate_record_invariants(duplicate_record)
        ),
        "stale_record_source_rejected": _raises_expected_error(
            lambda: validate_record_invariants(stale)
        ),
    }
    if not all(results.values()):
        failed = sorted(name for name, passed in results.items() if not passed)
        raise AssertionError(f"H-041 adversarial selftests failed: {failed}")
    return results


def build_core_record() -> dict[str, object]:
    binding = source_binding()
    delta = source_distinct_delta()
    figure13 = figure13_certificate()
    triple = triple_forcing_certificate()
    figure14 = figure14_certificate(Fraction(79, 100))
    capacity = capacity_certificate()
    nodes = [
        {
            "id": 1,
            "claim": "eleven boxes and ten capacity-one points force an avoiding box",
            "certificate": capacity["node_1"],
            "passed": True,
        },
        {
            "id": 2,
            "claim": "every Figure 13 avoider localizes to the K4 exception orbit",
            "certificate": figure13["localization"],
            "passed": True,
        },
        {
            "id": 3,
            "claim": "the localized avoiding box contains A1, A2, and A3",
            "certificate": {
                "all_three_forced_in_same_box": triple["all_three_forced_in_same_box"]
            },
            "passed": True,
        },
        {
            "id": 4,
            "claim": "the repaired Figure 14 twelve-point set is unavoidable",
            "certificate": {
                "unavoidable": figure14["unavoidable"],
                "full_tiling": figure14["full_tiling"],
            },
            "passed": True,
        },
        {
            "id": 5,
            "claim": "one box consuming three points leaves ten boxes for nine points",
            "certificate": capacity["node_5"],
            "passed": True,
        },
    ]
    return {
        "schema_version": SCHEMA_VERSION,
        "hypothesis": "H-041",
        "subject": {
            "n": 11,
            "container_side": SIDE.text(),
            "field": "Q(sqrt(5))",
            "box_semantics": "pairwise-disjoint open squares of side strictly greater than 1",
        },
        "source_binding": binding,
        "source_distinct_repair": delta,
        "figure13": figure13,
        "triple_forcing": triple,
        "figure14_repaired": figure14,
        "capacity": capacity,
        "five_node_chain": nodes,
        "determination": {
            "outcome": "criterion_met",
            "claim": (
                "G'=(79/100,37/20) restores the complete five-node Stromquist "
                "lower-bound mechanism"
            ),
            "scope": (
                "the repaired point set is a post-falsification construction and is "
                "not attributed to Stromquist"
            ),
        },
    }


def build_result() -> dict[str, object]:
    core = build_core_record()
    core["selftests"] = run_selftests(core)
    validate_record_invariants(core)
    return core


def write_text_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            delete=False,
        ) as temporary:
            temporary.write(text)
            temporary.flush()
            temporary_name = temporary.name
        Path(temporary_name).replace(path)
    finally:
        if temporary_name is not None:
            temporary_path = Path(temporary_name)
            if temporary_path.exists():
                temporary_path.unlink()


def replay_record(path: Path) -> dict[str, object]:
    loaded = json.loads(path.read_text())
    if not isinstance(loaded, dict):
        raise TypeError("retained H-041 record is not a JSON object")
    validate_record_invariants(loaded)
    expected = build_result()
    if loaded != expected:
        raise ValueError("retained H-041 record does not match an exact rebuild")
    return {
        "schema_version": SCHEMA_VERSION,
        "hypothesis": "H-041",
        "record_replayed": True,
        "determination_outcome": "criterion_met",
        "selftests": expected["selftests"],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--record", type=Path, help="write the deterministic exact record")
    mode.add_argument("--replay", type=Path, help="rebuild and compare an exact record")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    started = time.monotonic()
    try:
        if args.replay is not None:
            summary = replay_record(args.replay)
        else:
            result = build_result()
            if args.record is not None:
                write_text_atomic(
                    args.record, json.dumps(result, indent=2, sort_keys=True) + "\n"
                )
            summary = {
                "schema_version": SCHEMA_VERSION,
                "hypothesis": "H-041",
                "record_written": args.record is not None,
                "determination_outcome": "criterion_met",
                "selftests": result["selftests"],
            }
    except (OSError, TypeError, ValueError, AssertionError, ZeroDivisionError) as error:
        print(f"H-041 certificate failed: {error}")
        return 1
    summary["elapsed_seconds"] = round(time.monotonic() - started, 6)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
