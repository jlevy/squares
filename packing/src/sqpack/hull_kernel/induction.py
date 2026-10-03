"""Mode A's row geometry: one owner's angle row updated against the others' owned hulls.

Copies of the geometric functions of the frozen fresh-wall generic checker
(`packing/devtools/check_n11_generic_fresh.py`, SHA-256 `e8fcfd02...`), with n11's
`B`, `L` and wall bounds read from the frame and the arithmetic unchanged:

* `hull`, `convex`, `same` and `encode`, the exact polygon normal forms;
* `wall_lines`, the legal centre box of a row, from the frame's centred box;
* `strict_core`, the vertex quadratics proving a proposed core polygon lies strictly
  inside the square of side `B` at every angle of the row;
* `forbidden_regions`, the Minkowski sets `K_j - Q_i`: a centre there puts a point of
  another owner's owned hull inside the core, an interior overlap;
* `common_core_planes`, the facets of the core shifted by the residual's support: a
  point satisfying every row's planes lies in the core at every surviving pose;
* `convex_combination`, the exact check behind compressing a promoted hull.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from sqpack.hull_kernel.frame import Frame
from sqpack.hull_kernel.geometry import (
    Halfplane,
    Point,
    Polygon,
    area2,
    quadratic_nonnegative,
    require,
    trig,
)
from sqpack.hull_kernel.rational import Q


def hull(values: Polygon) -> Polygon:
    """Exact monotone-chain convex hull, including singleton/segment inputs."""
    ordered = sorted(set(values))
    if len(ordered) <= 2:
        return ordered

    def turn(a: Point, b: Point, c: Point) -> Q:
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

    lower: Polygon = []
    upper: Polygon = []
    for point in ordered:
        while len(lower) >= 2 and turn(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)
    for point in reversed(ordered):
        while len(upper) >= 2 and turn(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    return lower[:-1] + upper[:-1]


def convex(polygon: Polygon) -> Polygon:
    """A proposed region in hull normal form; refuses an empty or nonconvex one."""
    require(bool(polygon), "empty proposed region")
    if len(polygon) <= 2:
        return hull(polygon)
    turns = [
        (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])
        for a, b, c in zip(
            polygon, polygon[1:] + polygon[:1], polygon[2:] + polygon[:2], strict=True
        )
    ]
    require(all(t >= 0 for t in turns) or all(t <= 0 for t in turns), "nonconvex region")
    result = hull(polygon)
    require(area2(polygon) == area2(result), "region differs from its hull")
    return result


def same(left: Polygon, right: Polygon) -> bool:
    return hull(left) == hull(right)


def encode(polygon: Polygon) -> list[list[str]]:
    return [[str(x), str(y)] for x, y in hull(polygon)]


def wall_lines(frame: Frame, lo: Q, hi: Q) -> list[Halfplane]:
    """The legal centre box of a row `[lo, hi]`, in field coordinates."""
    width = min(sum(trig(t), Q()) for t in (lo, hi))
    require(
        quadratic_nonnegative(1 - width, Q(2), -1 - width, lo, hi),
        "full-angle legal-wall envelope fails",
    )
    low, high = frame.field_centre_bounds(width / 2)
    return [
        (Q(1), Q(0), high),
        (Q(-1), Q(0), -low),
        (Q(0), Q(1), high),
        (Q(0), Q(-1), -low),
    ]


def quadratic_strict(a: Q, b: Q, c: Q, lo: Q, hi: Q) -> bool:
    """Whether `a + b t + c t^2 > 0` on the closed interval, by its exact extrema."""
    probes = [lo, hi]
    if c > 0:
        vertex = -b / (2 * c)
        if lo < vertex < hi:
            probes.append(vertex)
    return all(a + b * t + c * t * t > 0 for t in probes)


def strict_core(frame: Frame, core: Polygon, lo: Q, hi: Q) -> None:
    """Refuse unless every core vertex is strictly inside the square at every angle."""
    scale = frame.scale
    require(len(core) >= 3 and area2(core) > 0, "empty or degenerate proposed core")
    for x, y in core:
        for sign in (-1, 1):
            require(
                quadratic_strict(
                    scale / 2 - sign * x, -2 * sign * y, scale / 2 + sign * x, lo, hi
                )
                and quadratic_strict(
                    scale / 2 - sign * y, 2 * sign * x, scale / 2 + sign * y, lo, hi
                ),
                "core vertex fails complete-angle strict containment",
            )


def minkowski_sum(left: Polygon, right: Polygon) -> Polygon:
    """`hull([p + q for p in left for q in right])`, built from the sum's own vertices.

    The Minkowski sum of two convex polygons is traced by merging their edges by angle:
    from the lowest vertex of each, the summand whose next edge turns first advances.
    Every vertex of the sum is a point visited that way, and every point visited is a
    pairwise sum, so the hull of the visited points is the hull of all the pairwise
    sums -- the same polygon from the same `hull`, in the same vertex order -- from
    `len(left) + len(right)` points rather than their product. A summand whose hull has
    fewer than three vertices, or a merge that does not close in that many steps, falls
    back to the pairwise sums.
    """
    a, b = hull(left), hull(right)
    n, m = len(a), len(b)
    visited: Polygon = []
    if n >= 3 and m >= 3:
        start_a = min(range(n), key=lambda k: (a[k][1], a[k][0]))
        start_b = min(range(m), key=lambda k: (b[k][1], b[k][0]))
        i = j = 0
        for _ in range(n + m):
            if i == n and j == m:
                break
            p, q = a[(start_a + i) % n], b[(start_b + j) % m]
            visited.append((p[0] + q[0], p[1] + q[1]))
            p2, q2 = a[(start_a + i + 1) % n], b[(start_b + j + 1) % m]
            cross = (p2[0] - p[0]) * (q2[1] - q[1]) - (p2[1] - p[1]) * (q2[0] - q[0])
            if cross >= 0 and i < n:
                i += 1
            if cross <= 0 and j < m:
                j += 1
        if i != n or j != m:
            visited = []
    if not visited:
        visited = [(p[0] + q[0], p[1] + q[1]) for p in a for q in b]
    return hull(visited)


def forbidden_regions(prior: Mapping[int, Polygon], owner: int, core: Polygon) -> list[Polygon]:
    """`K_j - Q_i` for every other owner `j`, in the prior state's owner order."""
    negated = [(-x, -y) for x, y in core]
    return [minkowski_sum(group, negated) for other, group in prior.items() if other != owner]


def common_core_planes(core: Polygon, vertices: Polygon) -> list[Halfplane]:
    """Each core facet `(n, h)` shifted to `n.x <= h + min over residual vertices of n.v`."""
    planes: list[Halfplane] = []
    if vertices:
        for p, q in zip(core, core[1:] + core[:1], strict=True):
            nx, ny = q[1] - p[1], p[0] - q[0]
            planes.append(
                (nx, ny, nx * p[0] + ny * p[1] + min(nx * x + ny * y for x, y in vertices))
            )
    return planes


def convex_combination(
    original: Polygon, indices: Sequence[int], weights: Sequence[Q]
) -> Point | None:
    """The exact combination, or None if the witness is not a convex combination of 1-3."""
    if not (
        1 <= len(indices) == len(weights) <= 3
        and all(type(index) is int and 0 <= index < len(original) for index in indices)
        and all(weight >= 0 for weight in weights)
        and sum(weights, Q()) == 1
    ):
        return None
    x, y = (
        sum(
            (
                weight * original[index][axis]
                for index, weight in zip(indices, weights, strict=True)
            ),
            Q(),
        )
        for axis in (0, 1)
    )
    return x, y
