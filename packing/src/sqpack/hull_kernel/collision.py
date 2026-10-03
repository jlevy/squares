"""Self-hull cuts, universal collision and the support outer domain of a capture row.

Copies of the frame-generic functions of the frozen capture transition pilot
(`packing/devtools/check_n11_capture_transition_pilot.py`, SHA-256 `22c5b4d1...`) and of
its integer backend (`packing/devtools/n11_integer_collision.py`, `4a1f71cd...`), with
n11's `B` read from the frame and the arithmetic unchanged:

* `self_hull_cuts`: a cut `n.x <= u` on an owner's centre is necessary when, for every
  angle of the row, the square must contain the owner's own owned hull `K_i`; checked by
  four quadratics in the half-angle `t` per cut;
* `universal_collision`, rational and integer: a closed region whose every vertex lies,
  for every live row `(D_r, Q_j^r)` of a partner's complete pose cover, in every facet
  `n.p <= h + min over D_r of n.y` of `Q_j^r - Q_i`; a centre there overlaps the partner
  in every pose it can still take. The integer form lifts points to homogeneous integer
  coordinates and decides every inequality by cross-multiplication; the cached form
  (`cached_universal_collision`, on `prepare_rows` and a `FacetCache`) checks the same
  inequalities with the facets memoised by the pair of cores and each facet's minimum
  over `D_r` memoised on the partner row;
* `support_outer_domain`: a row's residual hull clipped to the world by the eight
  support directions, rounded outward to `10^-8`, and `common_core_output`, which checks
  a row's published common-core planes and eight support bounds.

The transition pilot's strict core and wall lines are `induction.strict_core` and
`induction.wall_lines`: the same quadratics on the same values, with different messages.
What stays in the pilot is n11's capture bookkeeping (phase-two references, round 14,
the root-self node), which is not a primitive.
"""

from __future__ import annotations

import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from functools import cmp_to_key
from math import gcd, lcm
from typing import Any

from sqpack.hull_kernel.covers import convex_halfplanes
from sqpack.hull_kernel.frame import Frame
from sqpack.hull_kernel.geometry import (
    Budget,
    Halfplane,
    IncompleteError,
    Polygon,
    RefusalError,
    area2,
    intersect,
    quadratic_nonnegative,
    require,
)
from sqpack.hull_kernel.induction import hull, same
from sqpack.hull_kernel.rational import Q, Z

SUPPORT_NORMALS = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))
OUTWARD_GRID = 10**8

type HomogeneousPoint = tuple[Z, Z, Z]


def _remaining(budget: Budget) -> None:
    if time.monotonic() >= budget.deadline:
        raise IncompleteError("capture row wall ceiling")


def outward_round(value: Q) -> Q:
    """Round up to the `10^-8` grid."""
    return Q(-((-value.numerator * OUTWARD_GRID) // value.denominator), OUTWARD_GRID)


def support_outer_domain(residual: Sequence[Polygon], world: Polygon) -> Polygon:
    """The residual's eight outward-rounded supports, clipped to the owner's world."""
    vertices = [point for region in residual for point in region]
    if not vertices:
        return []
    lines = [
        (Q(nx), Q(ny), outward_round(max(nx * x + ny * y for x, y in vertices)))
        for nx, ny in SUPPORT_NORMALS
    ]
    return hull(intersect(world, lines))


def self_hull_cuts(
    frame: Frame, supplied: Sequence[Halfplane], owned: Polygon, lo: Q, hi: Q
) -> list[Halfplane]:
    """Admit each proposed cut `n.x <= u` as necessary for an owner whose hull is `owned`."""
    require(bool(owned), "empty accepted owned hull")
    scale = frame.scale
    result: list[Halfplane] = []
    for nx, ny, upper in supplied:
        require((nx, ny) != (0, 0), "zero self-cut normal")
        allowance = upper - min(nx * x + ny * y for x, y in owned)
        for sx in (-1, 1):
            for sy in (-1, 1):
                a = sx * nx + sy * ny
                d = sx * ny - sy * nx
                require(
                    quadratic_nonnegative(
                        allowance - scale * a / 2, -scale * d, allowance + scale * a / 2, lo, hi
                    ),
                    "self-cut excludes a possible square center",
                )
        result.append((nx, ny, upper))
    return result


def facets(poly: Polygon) -> list[Halfplane]:
    convex_hull = hull(poly)
    require(len(convex_hull) >= 3 and area2(convex_hull) > 0, "degenerate collision hull")
    return [
        (b[1] - a[1], a[0] - b[0], (b[1] - a[1]) * a[0] + (a[0] - b[0]) * a[1])
        for a, b in zip(convex_hull, convex_hull[1:] + convex_hull[:1], strict=True)
    ]


def universal_collision(
    query_core: Polygon,
    query_domain: Polygon,
    partner_rows: Sequence[tuple[Polygon, Polygon]],
    region: Polygon,
    *,
    budget: Budget,
) -> int:
    """Check a closed inner region of every possible partner-core collision set."""
    require(bool(partner_rows), "empty partner family requires separate contradiction")
    require(all(area2(core) > 0 for _, core in partner_rows), "partner core")
    require(area2(query_core) > 0, "query core")
    query_lines = convex_halfplanes(query_domain)
    for x, y in region:
        require(
            all(nx * x + ny * y <= upper for nx, ny, upper in query_lines),
            "collision region escapes query domain",
        )
    checks = 0
    for domain, core in partner_rows:
        _remaining(budget)
        difference = hull([(x - qx, y - qy) for x, y in core for qx, qy in query_core])
        for nx, ny, upper in facets(difference):
            bound = upper + min(nx * x + ny * y for x, y in domain)
            for x, y in region:
                checks += 1
                require(nx * x + ny * y <= bound, "region escapes universal collision set")
    return checks


def normalized_line(nx: Q, ny: Q, upper: Q) -> Halfplane:
    require((nx, ny) != (0, 0), "zero common-core normal")
    scale = abs(nx) if nx else abs(ny)
    return nx / scale, ny / scale, upper / scale


def common_core_output(
    row: Mapping[str, Any], core: Polygon, residual: Sequence[Polygon], world: Polygon
) -> int:
    """A row's published planes and support bounds equal the ones its residual implies."""
    vertices = [point for polygon in residual for point in polygon]
    planes = row["common_core_halfplanes"]
    bounds = row["outer_bounds"]
    if not vertices:
        require(
            planes == [] and bounds == [] and row["outer_domain"] == [],
            "empty residual retained output",
        )
        return 0
    expected = {
        normalized_line(nx, ny, upper + min(nx * x + ny * y for x, y in vertices))
        for nx, ny, upper in facets(core)
    }
    actual = {
        normalized_line(Q(item["normal"][0]), Q(item["normal"][1]), Q(item["upper"]))
        for item in planes
    }
    require(len(planes) == len(expected) and actual == expected, "common-core output planes")
    require(len(bounds) == len(SUPPORT_NORMALS), "outer-support inventory")
    lines: list[Halfplane] = []
    for item, (nx, ny) in zip(bounds, SUPPORT_NORMALS, strict=True):
        require(tuple(item["normal"]) == (nx, ny), "outer-support normal differs")
        upper = Q(item["upper"])
        require(
            all(nx * x + ny * y <= upper for x, y in vertices), "outer support cuts residual"
        )
        lines.append((Q(nx), Q(ny), upper))
    outer = intersect(world, lines)
    require(
        same([(Q(x), Q(y)) for x, y in row["outer_domain"]], outer),
        "row outer domain differs",
    )
    return len(planes)


def encode_homogeneous(point: tuple[Q, Q]) -> HomogeneousPoint:
    """Lift a rational point with a positive common denominator."""
    x, y = point
    z = lcm(x.denominator, y.denominator)
    return x.numerator * (z // x.denominator), y.numerator * (z // y.denominator), z


def compare_homogeneous(a: HomogeneousPoint, b: HomogeneousPoint) -> int:
    """Compare exact affine coordinates lexicographically."""
    dx = a[0] * b[2] - b[0] * a[2]
    dy = a[1] * b[2] - b[1] * a[2]
    value = dx or dy
    return (value > 0) - (value < 0)


def orientation(a: HomogeneousPoint, b: HomogeneousPoint, c: HomogeneousPoint) -> Z:
    """Return a determinant with the exact affine orientation sign."""
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    )


def homogeneous_hull(points: list[HomogeneousPoint]) -> list[HomogeneousPoint]:
    """Return the exact CCW convex hull, removing affine duplicates and collinearity."""
    ordered = sorted(points, key=cmp_to_key(compare_homogeneous))
    unique: list[HomogeneousPoint] = []
    for point in ordered:
        require(point[2] > 0, "nonpositive homogeneous denominator")
        if not unique or compare_homogeneous(unique[-1], point):
            unique.append(point)
    if len(unique) <= 1:
        return unique
    lower: list[HomogeneousPoint] = []
    upper: list[HomogeneousPoint] = []
    for point in unique:
        while len(lower) > 1 and orientation(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)
    for point in reversed(unique):
        while len(upper) > 1 and orientation(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    return lower[:-1] + upper[:-1]


@dataclass(frozen=True)
class PreparedRow:
    """A live partner row with its homogeneous forms and the memo of its domain minima.

    `minima` holds, by facet direction in lowest terms, the least value of `d . y` over
    the domain as `(value, denominator)`; a facet `n = g d` with `g > 0` has minimum
    `g` times that. It is a pure function of the domain, which never changes.
    """

    domain: Polygon
    core: Polygon
    centers: tuple[HomogeneousPoint, ...]
    partner: tuple[HomogeneousPoint, ...]
    minima: dict[tuple[Z, Z], tuple[Z, Z]] = field(default_factory=dict)

    def minimum(self, nx: Z, ny: Z) -> tuple[Z, Z]:
        """`min over the domain of n . y` as `(value, denominator)`, from the memo."""
        g = gcd(nx, ny)
        direction = (nx // g, ny // g)
        found = self.minima.get(direction)
        if found is None:
            dx, dy = direction
            least: tuple[Z, Z] | None = None
            for x, y, z in self.centers:
                value = dx * x + dy * y
                if least is None or value * least[1] < least[0] * z:
                    least = value, z
            if least is None:
                raise RefusalError("empty partner domain")
            found = self.minima[direction] = least
        return g * found[0], found[1]


def prepare_rows(rows: Sequence[tuple[Polygon, Polygon]]) -> list[PreparedRow]:
    """Each live partner row encoded once, with the obligations the reference form checks
    on every use checked here once: a nonempty domain and a core of positive area."""
    prepared: list[PreparedRow] = []
    for domain, core in rows:
        require(bool(domain) and area2(core) > 0, "partner core or domain")
        prepared.append(
            PreparedRow(
                domain,
                core,
                tuple(encode_homogeneous(point) for point in domain),
                tuple(encode_homogeneous(point) for point in core),
            )
        )
    return prepared


def as_prepared(rows: Sequence[PreparedRow | tuple[Polygon, Polygon]]) -> list[PreparedRow]:
    """Partner rows in prepared form: prepared ones as they are, raw pairs encoded."""
    prepared: list[PreparedRow] = []
    raw: list[tuple[Polygon, Polygon]] = []
    for row in rows:
        if isinstance(row, PreparedRow):
            prepared.append(row)
        else:
            raw.append(row)
    return prepared + prepare_rows(raw) if raw else prepared


FacetKey = tuple[tuple[HomogeneousPoint, ...], tuple[HomogeneousPoint, ...]]
FacetCache = dict[FacetKey, list[tuple[Z, Z, Z]]]


def difference_facets(
    query: tuple[HomogeneousPoint, ...], partner: tuple[HomogeneousPoint, ...]
) -> list[tuple[Z, Z, Z]]:
    """The facets `(nx, ny, upper)` of the hull of `partner - query`, exactly as
    `integer_universal_collision` builds them."""
    difference = homogeneous_hull(
        [
            (x * qz - qx * z, y * qz - qy * z, z * qz)
            for x, y, z in partner
            for qx, qy, qz in query
        ]
    )
    require(len(difference) >= 3, "degenerate collision hull")
    return [
        (b[1] * a[2] - a[1] * b[2], a[0] * b[2] - b[0] * a[2], a[0] * b[1] - a[1] * b[0])
        for a, b in zip(difference, difference[1:] + difference[:1], strict=True)
    ]


def cached_universal_collision(
    query_core: Polygon,
    query_domain: Polygon,
    partner_rows: Sequence[PreparedRow],
    region: Polygon,
    *,
    budget: Budget,
    facets: FacetCache,
) -> int:
    """`integer_universal_collision` with its facets memoised by the pair of cores.

    The facets of `Q_r - Q_i` depend on the two cores alone and a node has at most
    `bins` distinct cores, so they are built once per pair and read back by the exact
    homogeneous vertices; the minimum of each facet over `D_r` comes from the row's memo.
    The inequalities, their order and the check count are the reference form's.
    """
    require(bool(partner_rows), "empty partner family requires separate contradiction")
    require(area2(query_core) > 0, "query core")
    query_lines = convex_halfplanes(query_domain)
    require(
        all(nx * x + ny * y <= bound for x, y in region for nx, ny, bound in query_lines),
        "collision region escapes query domain",
    )
    query = tuple(encode_homogeneous(point) for point in query_core)
    vertices = [encode_homogeneous(point) for point in region]
    checks = 0
    for row in partner_rows:
        _remaining(budget)
        key = (query, row.partner)
        found = facets.get(key)
        if found is None:
            found = facets[key] = difference_facets(query, row.partner)
        for nx, ny, upper in found:
            value, denominator = row.minimum(nx, ny)
            rhs = upper * denominator + value
            for x, y, z in vertices:
                checks += 1
                require(
                    (nx * x + ny * y) * denominator <= rhs * z,
                    "region escapes universal collision set",
                )
    return checks


def integer_universal_collision(
    query_core: Polygon,
    query_domain: Polygon,
    partner_rows: Sequence[tuple[Polygon, Polygon]],
    region: Polygon,
    *,
    budget: Budget,
) -> int:
    """`universal_collision` on homogeneous integers; the same verdict and check count."""
    require(bool(partner_rows), "empty partner family requires separate contradiction")
    require(area2(query_core) > 0, "query core")
    query_lines = convex_halfplanes(query_domain)
    require(
        all(nx * x + ny * y <= bound for x, y in region for nx, ny, bound in query_lines),
        "collision region escapes query domain",
    )
    query = [encode_homogeneous(point) for point in query_core]
    vertices = [encode_homogeneous(point) for point in region]
    checks = 0
    for domain, core in partner_rows:
        _remaining(budget)
        require(bool(domain) and area2(core) > 0, "partner core or domain")
        partner = [encode_homogeneous(point) for point in core]
        centers = [encode_homogeneous(point) for point in domain]
        difference = homogeneous_hull(
            [
                (x * qz - qx * z, y * qz - qy * z, z * qz)
                for x, y, z in partner
                for qx, qy, qz in query
            ]
        )
        require(len(difference) >= 3, "degenerate collision hull")
        for a, b in zip(difference, difference[1:] + difference[:1], strict=True):
            nx = b[1] * a[2] - a[1] * b[2]
            ny = a[0] * b[2] - b[0] * a[2]
            upper = a[0] * b[1] - a[1] * b[0]
            minimum: tuple[Z, Z] | None = None
            for x, y, z in centers:
                value = nx * x + ny * y
                if minimum is None or value * minimum[1] < minimum[0] * z:
                    minimum = value, z
            if minimum is None:
                raise RefusalError("empty partner domain")
            value, denominator = minimum
            rhs = upper * denominator + value
            for x, y, z in vertices:
                checks += 1
                require(
                    (nx * x + ny * y) * denominator <= rhs * z,
                    "region escapes universal collision set",
                )
    return checks
