"""Sufficient closed-tile certificates for near-axis angle charts.

This source/toy kernel has no target data, search, or CLI. It proves only the
point-hit clause supplied to ``check_cover``; it cannot decide H-036. A failed
Bernstein test means unresolved, including an actual negative assigned-point
inequality: a different point could still hit that square.

Triangles are closed leaves of a fixed binary subdivision of the unit square,
or the complete fixed sixths-by-thirds grid used by ``grid_obligations``.
This avoids a new general mesh validator: ``sqpack.cover.validate_triangle_mesh``
also imposes edge-length constraints irrelevant to these parameter-space tiles.
Each split joins one edge's exact midpoint to its opposite vertex. Complete
prefix trees therefore cover every seam and boundary, not merely almost every
point. Coefficients may be rational or in the positive Q(sqrt(2)) embedding;
tile vertices and angle endpoints remain rational. The near-45-degree chart is
not implemented. Design: campaign/series/series-000-smoke-and-calibration/
results/agenda-026/bc-255-angle-instrument-design.md.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from fractions import Fraction
from math import comb

from sqpack.field import FieldElement, NumberField

type Scalar = Fraction | FieldElement
type Polynomial = tuple[Scalar, ...]
type Point = tuple[Scalar, Scalar]
type RationalPoint = tuple[Fraction, Fraction]
type Triangle = tuple[RationalPoint, RationalPoint, RationalPoint]
type Interval = tuple[Fraction, Fraction]
type GridIndex = tuple[int, int, int]
type GridObligation = tuple[int, int, int, int, int]

MAX_DEGREE = 4
MAX_SIGN_DEPTH = 8
MAX_TILE_DEPTH = 12
MAX_TILES = 2048
MAX_SLABS = 64
MAX_INPUT_BITS = 2048
ZERO = Fraction(0)
ONE = Fraction(1)
HALF = Fraction(1, 2)
DENOMINATOR = (ONE, ZERO, ONE)
COS_NUMERATOR = (ONE, ZERO, -ONE)
SIN_NUMERATOR = (ZERO, Fraction(2))


def _rational(value: Fraction) -> None:
    if type(value) is not Fraction:
        raise ValueError("exact Fraction inputs required; floats and booleans are refused")
    if max(value.numerator.bit_length(), value.denominator.bit_length()) > MAX_INPUT_BITS:
        raise ValueError("rational input exceeds the declared bit limit")


def _coefficient_field(values: tuple[Scalar, ...]) -> NumberField | None:
    field: NumberField | None = None
    for value in values:
        if isinstance(value, FieldElement):
            if field is not None and value.field is not field:
                raise ValueError("coefficients come from different number fields")
            field = value.field
            if len(value.coeffs) != 2:
                raise ValueError("only degree-two Q(sqrt(2)) coefficients are supported")
            for coefficient in value.coeffs:
                _rational(coefficient)
        else:
            _rational(value)
    if field is not None and (
        field.degree != 2 or field.alpha * field.alpha != 2 or field.alpha.sign() <= 0
    ):
        raise ValueError("only the positive Q(sqrt(2)) field embedding is supported")
    return field


def _polynomial(value: Polynomial) -> Polynomial:
    if not value or len(value) > MAX_DEGREE + 1:
        raise ValueError("polynomial must have one to five coefficients")
    _coefficient_field(value)
    return value


def _add(left: Polynomial, right: Polynomial) -> Polynomial:
    return tuple(
        (left[i] if i < len(left) else ZERO) + (right[i] if i < len(right) else ZERO)
        for i in range(max(len(left), len(right)))
    )


def _scale(value: Polynomial, factor: Scalar) -> Polynomial:
    return tuple(factor * coefficient for coefficient in value)


def _multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    result: list[Scalar] = [ZERO] * (len(left) + len(right) - 1)
    for i, first in enumerate(left):
        for j, second in enumerate(right):
            result[i + j] += first * second
    return tuple(result)


def evaluate(polynomial: Polynomial, value: Fraction) -> Scalar:
    """Exact Horner evaluation, also valid at a zero-dimensional angle slab."""
    result: Scalar = ZERO
    for coefficient in reversed(polynomial):
        result = result * value + coefficient
    return result


def bernstein_coefficients(polynomial: Polynomial, low: Fraction, high: Fraction) -> Polynomial:
    """Convert p(low + (high-low)w) exactly, keeping its declared degree."""
    _polynomial(polynomial)
    _rational(low)
    _rational(high)
    if low > high:
        raise ValueError("angle interval is reversed")
    degree = len(polynomial) - 1
    if low == high:
        return (evaluate(polynomial, low),) * (degree + 1)
    power = tuple(
        sum(
            (
                polynomial[k] * comb(k, j) * low ** (k - j) * (high - low) ** j
                for k in range(j, degree + 1)
            ),
            ZERO,
        )
        for j in range(degree + 1)
    )
    return tuple(
        sum((power[j] * Fraction(comb(i, j), comb(degree, j)) for j in range(i + 1)), ZERO)
        for i in range(degree + 1)
    )


@dataclass(frozen=True)
class SignResult:
    """Nonempty unresolved leaves prevent a proof; no negative verdict exists."""

    checked_leaves: int
    unresolved: tuple[Interval, ...]

    @property
    def proved(self) -> bool:
        return not self.unresolved


def certify_nonnegative(
    polynomial: Polynomial, low: Fraction, high: Fraction, *, max_depth: int = 0
) -> SignResult:
    """Bounded left-first bisection with nonnegative Bernstein coefficients.

    Zero coefficients and identically zero polynomials are valid on closed slabs.
    Interior tangencies need not certify after any finite rational subdivision.
    """
    if type(max_depth) is not int or not 0 <= max_depth <= MAX_SIGN_DEPTH:
        raise ValueError("sign subdivision depth is outside the declared limit")
    pending = [(low, high, 0)]
    unresolved: list[Interval] = []
    checked = 0
    while pending:
        first, last, depth = pending.pop()
        coefficients = bernstein_coefficients(polynomial, first, last)
        if all(value >= 0 for value in coefficients):
            checked += 1
        elif depth == max_depth or first == last:
            checked += 1
            unresolved.append((first, last))
        else:
            midpoint = (first + last) / 2
            pending.extend(((midpoint, last, depth + 1), (first, midpoint, depth + 1)))
    return SignResult(checked, tuple(unresolved))


def closed_tiles(paths: tuple[str, ...]) -> dict[str, Triangle]:
    """Reconstruct a complete closed triangulation from prefix-free leaf paths.

    Root 0 is (0,0),(1,0),(1,1); root 1 is (0,0),(1,1),(0,1).
    A child bit selects one half after bisecting the first edge. Recursion rotates
    vertices so subsequent splits do not repeatedly bisect the same edge. Exact
    child unions equal their parent, including the common segment and its ends.
    """
    if not 2 <= len(paths) <= MAX_TILES or len(set(paths)) != len(paths):
        raise ValueError("tile inventory is empty, duplicate, or above the declared cap")
    if any(
        not path or len(path) > MAX_TILE_DEPTH + 1 or set(path) - {"0", "1"} for path in paths
    ):
        raise ValueError("invalid or over-depth binary tile path")
    leaves = set(paths)
    ancestors = {path[:length] for path in paths for length in range(1, len(path))}
    if leaves & ancestors:
        raise ValueError("tile inventory overlaps an ancestor and descendant")
    pending: list[tuple[str, Triangle]] = [
        ("1", ((ZERO, ZERO), (ONE, ONE), (ZERO, ONE))),
        ("0", ((ZERO, ZERO), (ONE, ZERO), (ONE, ONE))),
    ]
    result: dict[str, Triangle] = {}
    while pending:
        path, triangle = pending.pop()
        if path in leaves:
            result[path] = triangle
        elif path in ancestors:
            first, second, third = triangle
            midpoint = ((first[0] + second[0]) / 2, (first[1] + second[1]) / 2)
            pending.extend(
                (
                    (path + "1", (second, third, midpoint)),
                    (path + "0", (third, first, midpoint)),
                )
            )
        else:
            raise ValueError(f"closed triangulation is missing tile {path!r}")
    return result


def _chart(low: Fraction, high: Fraction) -> Polynomial:
    _rational(low)
    _rational(high)
    if not -Fraction(1, 4) < low <= high < Fraction(1, 4):
        raise ValueError("near-axis chart requires -1/4 < low <= high < 1/4")
    if low < 0 < high:
        raise ValueError("split the sign chart at zero; do not drop either closed half")
    sign = -ONE if low < 0 else ONE
    # cos(theta)>0 on this chart, sin(theta) has the sign of t.
    return _scale(_add(COS_NUMERATOR, _scale(SIN_NUMERATOR, sign)), HALF)


def membership_polynomials(
    side: Scalar, point: Point, vertex: RationalPoint, low: Fraction, high: Fraction
) -> tuple[Polynomial, Polynomial, Polynomial, Polynomial]:
    """Derive d^2(1/2 - a dot (p-F_t(z))) for a=u,-u,v,-v.

    d=1+t^2 is positive; H/d=(|cos|+|sin|)/2. Each center numerator
    H+(side*d-2H)z is quadratic, so each cleared inequality is quartic and
    affine in z. One fixed point at all three vertices implies the entire
    closed triangle. This alone does not check the positive-width guard.
    """
    _coefficient_field((side, *point))
    for value in vertex:
        _rational(value)
    if len(point) != 2 or len(vertex) != 2 or not all(0 <= value <= 1 for value in vertex):
        raise ValueError("membership needs a point and a unit-domain vertex")
    half_extent = _chart(low, high)
    width = _add(_scale(DENOMINATOR, side), _scale(half_extent, -Fraction(2)))
    delta = tuple(
        _add(
            _scale(DENOMINATOR, coordinate),
            _scale(_add(half_extent, _scale(width, parameter)), -ONE),
        )
        for coordinate, parameter in zip(point, vertex, strict=True)
    )
    along = _add(_multiply(COS_NUMERATOR, delta[0]), _multiply(SIN_NUMERATOR, delta[1]))
    across = _add(
        _scale(_multiply(SIN_NUMERATOR, delta[0]), -ONE), _multiply(COS_NUMERATOR, delta[1])
    )
    half_denominator_squared = _scale(_multiply(DENOMINATOR, DENOMINATOR), HALF)
    return (
        _add(half_denominator_squared, _scale(along, -ONE)),
        _add(half_denominator_squared, along),
        _add(half_denominator_squared, _scale(across, -ONE)),
        _add(half_denominator_squared, across),
    )


@dataclass(frozen=True)
class TileSlab:
    """Closed angle slab with one unchanged marked-point index per tile."""

    low: Fraction
    high: Fraction
    assignments: tuple[tuple[str, int], ...]


@dataclass(frozen=True)
class UnresolvedInequality:
    """A sufficient tile obligation that was not proved, not a square escape."""

    slab: int
    tile: str
    vertex: int
    axis: int
    intervals: tuple[Interval, ...]


@dataclass(frozen=True)
class CoverResult:
    """Exact closed cover of the supplied near-axis domain, if proved."""

    inequalities_checked: int
    unresolved: tuple[UnresolvedInequality, ...]

    @property
    def proved(self) -> bool:
        return not self.unresolved


def _validate_slabs(
    side: Scalar, points: tuple[Point, ...], domain: Interval, slabs: tuple[TileSlab, ...]
) -> None:
    _coefficient_field((side, *(coordinate for point in points for coordinate in point)))
    if side <= 0 or not points or len(points) > MAX_TILES:
        raise ValueError("positive side and a bounded nonempty marked-point set required")
    for point in points:
        if len(point) != 2:
            raise ValueError("marked point must have two coordinates")
        for coordinate in point:
            if not 0 <= coordinate <= side:
                raise ValueError("marked point is outside the container")
    point_keys = {
        tuple(
            tuple(coordinate.coeffs)
            if isinstance(coordinate, FieldElement)
            else (coordinate, ZERO)
            for coordinate in point
        )
        for point in points
    }
    if len(point_keys) != len(points):
        raise ValueError("marked-point inventory has duplicates")
    if len(domain) != 2:
        raise ValueError("requested domain must have two endpoints")
    for endpoint in domain:
        _rational(endpoint)
    if domain[0] > domain[1] or not 1 <= len(slabs) <= MAX_SLABS:
        raise ValueError("requested domain or slab count is invalid")
    next_low = domain[0]
    for slab in slabs:
        half_extent = _chart(slab.low, slab.high)
        if slab.low != next_low or (slab.low == slab.high and domain[0] != domain[1]):
            raise ValueError("slabs must cover the requested domain in order without gaps")
        width = _add(_scale(DENOMINATOR, side), _scale(half_extent, -Fraction(2)))
        if not all(value > 0 for value in bernstein_coefficients(width, slab.low, slab.high)):
            raise ValueError("strictly positive center-box width was not certified")
        next_low = slab.high
    if next_low != domain[1] or (domain[0] == domain[1] and len(slabs) != 1):
        raise ValueError("slabs narrow or extend the requested domain")


def check_cover(
    side: Scalar,
    points: tuple[Point, ...],
    domain: Interval,
    slabs: tuple[TileSlab, ...],
    *,
    sign_depth: int = 0,
) -> CoverResult:
    """Replay all tile/vertex/axis obligations; never infer geometry from failure.

    The requested domain and marked points are separate inputs, not claims taken
    from the certificate. A future target adapter must bind them to a frozen
    source. No standalone file parser, target binding, or run budget is provided
    by this in-memory kernel.
    """
    _validate_slabs(side, points, domain, slabs)
    unresolved: list[UnresolvedInequality] = []
    checked = 0
    for slab_index, slab in enumerate(slabs):
        tiles = closed_tiles(tuple(path for path, _ in slab.assignments))
        labels = dict(slab.assignments)
        if any(
            type(label) is not int or not 0 <= label < len(points) for label in labels.values()
        ):
            raise ValueError("tile has an unknown marked-point label")
        for path, triangle in tiles.items():
            point = points[labels[path]]
            for vertex_index, vertex in enumerate(triangle):
                for axis_index, polynomial in enumerate(
                    membership_polynomials(side, point, vertex, slab.low, slab.high)
                ):
                    result = certify_nonnegative(
                        polynomial, slab.low, slab.high, max_depth=sign_depth
                    )
                    checked += 1
                    if not result.proved:
                        unresolved.append(
                            UnresolvedInequality(
                                slab_index, path, vertex_index, axis_index, result.unresolved
                            )
                        )
    return CoverResult(checked, tuple(unresolved))


def fixed_grid_triangles() -> dict[GridIndex, Triangle]:
    """The complete closed 6x3 root grid, with no subdivision or supplied vertices.

    Row-major rectangles exactly cover [0,1]^2. Each diagonal joins LL to UR;
    triangles (LL,LR,UR) and (LL,UR,UL) include their shared diagonal and all
    boundary points. The inventory is constructed, never inferred from area.
    """
    result: dict[GridIndex, Triangle] = {}
    for row in range(3):
        for column in range(6):
            left, right = Fraction(column, 6), Fraction(column + 1, 6)
            bottom, top = Fraction(row, 3), Fraction(row + 1, 3)
            result[row, column, 0] = ((left, bottom), (right, bottom), (right, top))
            result[row, column, 1] = ((left, bottom), (right, top), (left, top))
    return result


def grid_obligations(
    side: Scalar,
    points: tuple[Point, ...],
    assignments: tuple[tuple[int, ...], ...],
    *,
    low: Fraction = ZERO,
    high: Fraction = ZERO,
) -> Iterator[tuple[GridObligation, bool]]:
    """Yield 432 fixed-grid signed checks on one closed slab, defaulting to theta=0.

    A caller must consume the complete iterator before claiming a cover. A failed
    entry is only an unresolved assigned-point obligation, not a square escape.
    This reuses the same field, center-map, membership and Bernstein proof as the
    binary interface; only the fixed closed root inventory differs.
    """
    if len(assignments) != 3 or any(len(row) != 6 for row in assignments):
        raise ValueError("the complete 3x6 assignment matrix is required")
    if any(
        type(label) is not int or not 0 <= label < len(points)
        for row in assignments
        for label in row
    ):
        raise ValueError("grid has an unknown marked-point label")
    _validate_slabs(side, points, (low, high), (TileSlab(low, high, ()),))
    for (row, column, triangle_index), triangle in fixed_grid_triangles().items():
        point = points[assignments[row][column]]
        for vertex_index, vertex in enumerate(triangle):
            for axis_index, polynomial in enumerate(
                membership_polynomials(side, point, vertex, low, high)
            ):
                result = certify_nonnegative(polynomial, low, high, max_depth=0)
                yield (row, column, triangle_index, vertex_index, axis_index), result.proved
