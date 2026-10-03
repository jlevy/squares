"""Standing verifier of saved n17 kernel certificates (seed and node), in exact rationals.

Retained from lane R3's review verifier (exp-249, `audit-W7/verify_cert.py.txt`), with its
mathematics unchanged and its independence kept: it imports nothing from
`sqpack.hull_kernel`, from the checker `check_n17_subpattern`, from the selector or from
the branch and bound. The cells and the cap come from `check_n17_capacity_one_cover`'s
exact polygons, or from a JSON cells file whose SHA-256 the caller states.

What it re-derives, from scratch:

- both objects' digests (the file names) and their canonical JSON; the node's source is
  the seed; the seed's world is the cells; the mask is the node's;
- the seed: every owned point is owned (bisection on the half-angle with an interval
  product bound), every row is the cell cut by the row's legal box;
- every step's rows: a partition of the half-angle range `[0, 1]` in exact rationals, in
  order, with no gap and no overlap, each row citing by reference one of the owner's
  accepted rows whose interval contains it; the seed's rows are the uniform grid, and a
  step may split an accepted row into narrower ones, which then replace it;
- the owned-hull chain through every step: the prior hulls equal the state, kernel points
  satisfy every live row's common-core planes (recomputed from the published core and
  residual vertices), compression witnesses are exact convex combinations on the grid;
- every partner pose cover: its domain is the hull of the partner's current residual
  vertices, its core is strictly inside the partner's square over the row;
- for the rows checked in full: the required domain (the predecessor's outer domain cut
  by the legal box of the row's own interval), the strict core, every collision
  region against every live partner row and every facet of the exact Minkowski
  difference, and coverage of the required domain by forbidden, collision and residual
  regions by an exact vertical sweep (every event abscissa, and one probe inside every
  open slab between two of them);
- the closure: derived after each step and equal to the declared one, with no step after
  it, and the final state equal to the derived one.

Arithmetic. The collision facets and the row cover run on homogeneous integers, with
`Fraction` kept for everything else. A Minkowski difference's facets come from the two
cores' edge normals: a Minkowski sum of convex polygons has exactly the edge directions
of its summands, so these are the hull's facets up to positive scaling, as many of them,
with parallel directions merged and their supports added. The sweep compares ordinates
by cross-multiplication. Four caches hold pure functions of exact inputs and nothing
else: the facets of a (partner core, core) pair, the least value of `n . y` over a
partner row's domain by direction, the forbidden region of an (owned hull, core) pair,
and a partner row's admitted cover, reused at a later step only when that step publishes
identical domain and core lists for the same accepted row. `covered_by_area`, the
area-subtraction form of the cover, is kept as the reference the tests hold the sweep
against.

Modes. Full, the default, checks every row of every step and is what admission requires.
`--sample N` checks `N` rows per step drawn by a seeded generator, and every row of the
closure step: a planning check, not an admission.

The receipt names the seed's and node's digests, the cells' source, the mask, the closure,
the mode and the counts, this module's SHA-256 read at import, and PASS or FAIL with the
first failure.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import random
import time
from collections.abc import Sequence
from dataclasses import dataclass, field
from fractions import Fraction as Q
from itertools import pairwise
from pathlib import Path
from typing import Any

SCHEMA = "n17-certificate-verification/v1"
KIND = "kernel"
MODULE_SHA256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
HULL_LIMIT = 16
GRID = 2**20

Point = tuple[Q, Q]
Plane = tuple[Q, Q, Q]


class VerificationError(Exception):
    """The certificate fails a check; the message names the first that failed."""


def require(condition: bool, message: str) -> None:  # noqa: FBT001
    if not condition:
        raise VerificationError(message)


def point(v: Any) -> Point:
    return (Q(v[0]), Q(v[1]))


def poly(vertices: Any) -> list[Point]:
    return [point(p) for p in vertices]


# ---------------------------------------------------------------------------
# Geometry, written independently of the kernel
# ---------------------------------------------------------------------------


def cross(o: Point, a: Point, b: Point) -> Q:
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def hull(points: list[Point]) -> list[Point]:
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts
    lower: list[Point] = []
    upper: list[Point] = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def area2(polygon: list[Point]) -> Q:
    if len(polygon) < 3:
        return Q(0)
    n = len(polygon)
    return abs(
        sum(
            (
                polygon[i][0] * polygon[(i + 1) % n][1]
                - polygon[(i + 1) % n][0] * polygon[i][1]
                for i in range(n)
            ),
            Q(0),
        )
    )


def clip_closed(polygon: list[Point], a: Q, b: Q, c: Q) -> list[Point]:
    """The polygon cut to the closed half-plane `a x + b y <= c`, exactly."""
    if not polygon:
        return []
    out: list[Point] = []
    n = len(polygon)
    for i in range(n):
        p, q = polygon[i], polygon[(i + 1) % n]
        fp, fq = a * p[0] + b * p[1] - c, a * q[0] + b * q[1] - c
        if fp <= 0:
            out.append(p)
        if (fp < 0 < fq) or (fq < 0 < fp):
            t = fp / (fp - fq)
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    result: list[Point] = []
    for p in out:
        if not result or result[-1] != p:
            result.append(p)
    if len(result) > 1 and result[0] == result[-1]:
        result.pop()
    return result


def planes_of(polygon: list[Point]) -> list[Plane]:
    """Outward half-planes `(a, b, c)`, `a x + b y <= c`, of a convex polygon."""
    h = hull(polygon)
    require(len(h) >= 3, "planes of a degenerate polygon")
    out: list[Plane] = []
    for i in range(len(h)):
        p, q = h[i], h[(i + 1) % len(h)]
        a, b = q[1] - p[1], p[0] - q[0]
        out.append((a, b, a * p[0] + b * p[1]))
    return out


def inside(polygon: list[Point], pt: Point) -> bool:
    return all(a * pt[0] + b * pt[1] <= c for a, b, c in planes_of(polygon))


def same_set(first: list[Point], second: list[Point]) -> bool:
    return hull(first) == hull(second)


def trig(t: Q) -> tuple[Q, Q]:
    return (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)


def wall_box(lo: Q, hi: Q, cap: Q) -> list[Point]:
    """The closed legal centre box for the half-angle row `[lo, hi]`.

    `cos + sin` is concave in the angle on `[0, pi/2]` and the chart is monotone, so its
    least value on the row is at an endpoint.
    """
    h = min(sum(trig(t), Q(0)) for t in (lo, hi)) / 2
    return [(h, h), (cap - h, h), (cap - h, cap - h), (h, cap - h)]


def intersect_convex(polygon: list[Point], other: list[Point]) -> list[Point]:
    for a, b, c in planes_of(other):
        polygon = clip_closed(polygon, a, b, c)
        if not polygon:
            break
    return polygon


def quad_min_positive(a0: Q, a1: Q, a2: Q, lo: Q, hi: Q) -> bool:
    """`a0 + a1 t + a2 t^2 > 0` on `[lo, hi]`, by the endpoints and an interior vertex."""
    values = [a0 + a1 * lo + a2 * lo * lo, a0 + a1 * hi + a2 * hi * hi]
    if a2 > 0:
        tv = -a1 / (2 * a2)
        if lo < tv < hi:
            values.append(a0 + a1 * tv + a2 * tv * tv)
    return min(values) > 0


def core_strict(core: list[Point], lo: Q, hi: Q) -> bool:
    """Every core vertex has both body coordinates below 1/2 in size over the row.

    The body coordinates are `c x + s y` and `-s x + c y` with the half-angle chart's
    `c`, `s`; both conditions are multiplied by `1 + t^2 > 0`.
    """
    half = Q(1, 2)
    for x, y in core:
        for sg in (1, -1):
            if not quad_min_positive(half - sg * x, -2 * sg * y, half + sg * x, lo, hi):
                return False
            if not quad_min_positive(half - sg * y, 2 * sg * x, half + sg * y, lo, hi):
                return False
    return True


def minkowski_diff(first: list[Point], second: list[Point]) -> list[Point]:
    """`hull(first - second)` for convex polygons."""
    return hull([(a[0] - b[0], a[1] - b[1]) for a in first for b in second])


def owned(
    cell: list[Point], pt: Point, cap: Q, *, lo: Q = Q(0), hi: Q = Q(1), depth: int = 0
) -> bool:
    """The point is strictly inside the square for every centre in the cell cut by the
    legal box and every half-angle in `[lo, hi]`: bisection with an interval product bound.
    """
    legal = intersect_convex(list(cell), wall_box(lo, hi, cap))
    if not legal:
        return True
    c_lo, s_lo = trig(lo)
    c_hi, s_hi = trig(hi)
    c_min, c_max = min(c_lo, c_hi), max(c_lo, c_hi)
    s_min, s_max = min(s_lo, s_hi), max(s_lo, s_hi)
    ok = True
    for vx, vy in legal:
        dx, dy = pt[0] - vx, pt[1] - vy
        for a, d in ((dx, dy), (dy, -dx)):
            values = [a * cc + d * ss for cc in (c_min, c_max) for ss in (s_min, s_max)]
            if max(abs(v) for v in values) >= Q(1, 2):
                ok = False
                break
        if not ok:
            break
    if ok:
        return True
    if depth >= 18:
        return False
    mid = (lo + hi) / 2
    return owned(cell, pt, cap, lo=lo, hi=mid, depth=depth + 1) and owned(
        cell, pt, cap, lo=mid, hi=hi, depth=depth + 1
    )


def subtract_pieces(pieces: list[list[Point]], region: list[Point]) -> list[list[Point]]:
    """Closed convex pieces tiling, up to boundaries, the pieces minus the region."""
    planes = planes_of(region)
    out: list[list[Point]] = []
    for piece in pieces:
        rest = piece
        for a, b, c in planes:
            outside = clip_closed(rest, -a, -b, -c)
            if outside and area2(outside) > 0:
                out.append(outside)
            rest = clip_closed(rest, a, b, c)
            if not rest or area2(rest) == 0:
                break
    return out


def covered_by_area(domain: list[Point], regions: list[list[Point]]) -> tuple[bool, int]:
    """Whether the closed convex regions cover the domain (of positive area), exactly.

    The uncovered set is relatively open, so it is nonempty exactly when the leftover
    area is positive.
    """
    pieces = [domain]
    for region in regions:
        if len(hull(region)) < 3:
            continue
        pieces = subtract_pieces(pieces, region)
        if not pieces:
            return True, 0
    left = sum((area2(p) for p in pieces), Q(0))
    return left == 0, len(pieces)


# ---------------------------------------------------------------------------
# Homogeneous integers: the collision facets and the row cover without Fraction
# ---------------------------------------------------------------------------

HPoint = tuple[int, int, int]
Ratio = tuple[int, int]
Direction = tuple[int, int]
Facet = tuple[int, int, int, int]


def homogeneous(pt: Point) -> HPoint:
    """`(x, y)` as integers `(X, Y, Z)` with `x = X/Z`, `y = Y/Z` and `Z > 0`."""
    x, y = pt
    z = x.denominator * y.denominator // math.gcd(x.denominator, y.denominator)
    return x.numerator * (z // x.denominator), y.numerator * (z // y.denominator), z


def ratio_lt(a: Ratio, b: Ratio) -> bool:
    """`a < b` for ratios with positive denominators."""
    return a[0] * b[1] < b[0] * a[1]


def normalised(numerator: int, denominator: int) -> Ratio:
    """The ratio in lowest terms with a positive denominator, so equal values are equal."""
    if denominator < 0:
        numerator, denominator = -numerator, -denominator
    g = math.gcd(numerator, denominator)
    return numerator // g, denominator // g


def between(a: Ratio, b: Ratio) -> Ratio:
    """A ratio strictly inside `(a, b)` with small terms: the continued-fraction choice.

    An integer inside the interval is taken when there is one; otherwise the interval is
    shifted into `[0, 1]` and inverted, which exchanges its ends, and the answer is
    `whole + 1/inner`. The terms stay about the size of the gap's, where the midpoint
    would carry the product of both ends' denominators.
    """
    an, ad = a
    bn, bd = b
    whole = an // ad
    if (whole + 1) * bd < bn:
        return whole + 1, 1
    rest_an, rest_bn = an - whole * ad, bn - whole * bd
    if rest_an == 0:
        k = bd // rest_bn + 1
        return whole * k + 1, k
    n, d = between((bd, rest_bn), (ad, rest_an))
    return whole * n + d, n


def ratio_extremes(values: Sequence[Ratio]) -> tuple[Ratio, Ratio]:
    least = most = values[0]
    for value in values[1:]:
        if ratio_lt(value, least):
            least = value
        elif ratio_lt(most, value):
            most = value
    return least, most


def directions(polygon: Sequence[HPoint]) -> list[Direction]:
    """Outward normals of a counterclockwise convex polygon's edges, each in lowest terms."""
    out: list[Direction] = []
    count = len(polygon)
    for i in range(count):
        px, py, pz = polygon[i]
        qx, qy, qz = polygon[(i + 1) % count]
        nx, ny = qy * pz - py * qz, px * qz - qx * pz
        g = math.gcd(nx, ny)
        out.append((nx // g, ny // g))
    return out


def support(polygon: Sequence[HPoint], nx: int, ny: int, *, largest: bool) -> Ratio:
    """The largest, or the least, value of `n . v` over the polygon's vertices."""
    best_n, best_d = 0, 0
    for x, y, z in polygon:
        value = nx * x + ny * y
        if best_d == 0:
            better = True
        elif largest:
            better = value * best_d > best_n * z
        else:
            better = value * best_d < best_n * z
        if better:
            best_n, best_d = value, z
    return best_n, best_d


def difference_facets(partner: Sequence[HPoint], core: Sequence[HPoint]) -> list[Facet]:
    """The facets `n . p <= h` of `partner - core`, the hull of the vertex differences.

    A Minkowski sum of convex polygons has exactly the edge directions of its summands,
    so the facets of `partner + (-core)` are the outward normals of `partner` and the
    negated normals of `core`, each direction once, with support `max over partner of
    n . v` minus `min over core of n . w`. These are the hull's facets up to positive
    scaling, and as many of them. Each is `(nx, ny, hn, hd)` for `n . p <= hn/hd`,
    `hd > 0`.
    """
    facets: dict[Direction, Facet] = {}
    negated = [(-nx, -ny) for nx, ny in directions(core)]
    for nx, ny in [*directions(partner), *negated]:
        if (nx, ny) in facets:
            continue
        top_n, top_d = support(partner, nx, ny, largest=True)
        low_n, low_d = support(core, nx, ny, largest=False)
        facets[(nx, ny)] = (nx, ny, top_n * low_d - low_n * top_d, top_d * low_d)
    return list(facets.values())


@dataclass(frozen=True)
class Edge:
    """A non-vertical edge: its polygon, its closed x range, and its line.

    The line is `a x + b y + c = 0` with `b > 0`, so the ordinate at `x = X/W` is
    `-(a X + c W) / (b W)`, a ratio with a positive denominator.
    """

    polygon: int
    lo: Ratio
    hi: Ratio
    a: int
    b: int
    c: int


Vertical = tuple[int, Ratio, Ratio]
Section = tuple[Ratio, Ratio]


def compile_edges(
    polygons: Sequence[Sequence[HPoint]],
) -> tuple[list[Edge], dict[Ratio, list[Vertical]]]:
    """Every polygon's edges: the non-vertical ones as lines, the vertical ones by x."""
    edges: list[Edge] = []
    verticals: dict[Ratio, list[Vertical]] = {}
    for index, polygon in enumerate(polygons):
        count = len(polygon)
        for i in range(count):
            px, py, pz = polygon[i]
            qx, qy, qz = polygon[(i + 1) % count]
            a, b, c = py * qz - qy * pz, qx * pz - px * qz, px * qy - qx * py
            if b == 0:
                low, high = ratio_extremes([(py, pz), (qy, qz)])
                verticals.setdefault(normalised(px, pz), []).append((index, low, high))
                continue
            if b < 0:
                a, b, c = -a, -b, -c
            low, high = ratio_extremes([(px, pz), (qx, qz)])
            edges.append(Edge(index, low, high, a, b, c))
    return edges, verticals


def sweep_events(
    polygons: Sequence[Sequence[HPoint]], edges: Sequence[Edge], left: Ratio, right: Ratio
) -> list[Ratio]:
    """Every vertex abscissa in `[left, right]` and every crossing of two edges there.

    Edges are taken in order of their left end, against the edges whose x range still
    reaches the current left end; two edges with the same slope never cross.
    """
    events: set[Ratio] = set()
    for polygon in polygons:
        for x, _, z in polygon:
            if not ratio_lt((x, z), left) and not ratio_lt(right, (x, z)):
                events.add(normalised(x, z))
    order = sorted(range(len(edges)), key=lambda i: Q(*edges[i].lo))
    active: list[int] = []
    for i in order:
        edge = edges[i]
        if ratio_lt(edge.hi, left) or ratio_lt(right, edge.lo):
            continue
        active = [j for j in active if not ratio_lt(edges[j].hi, edge.lo)]
        for j in active:
            other = edges[j]
            det = edge.a * other.b - edge.b * other.a
            if det == 0:
                continue
            xn = edge.b * other.c - edge.c * other.b
            if det < 0:
                xn, det = -xn, -det
            start = ratio_extremes([edge.lo, other.lo, left])[1]
            stop = ratio_extremes([edge.hi, other.hi, right])[0]
            if not ratio_lt((xn, det), start) and not ratio_lt(stop, (xn, det)):
                events.add(normalised(xn, det))
        active.append(i)
    return sorted(events, key=lambda r: Q(*r))


def section_covered(target: Section, spans: list[Section]) -> bool:
    """Whether closed intervals cover the closed target, merging them by lower end.

    The sort key is the float of each lower end; the order is then confirmed exactly on
    every adjacent pair and redone with exact keys when it fails. The merge is exact,
    and a mis-sorted list could only make it refuse, never accept.
    """
    if len(spans) > 1:
        spans.sort(key=lambda span: span[0][0] / span[0][1])
        if any(ratio_lt(spans[i + 1][0], spans[i][0]) for i in range(len(spans) - 1)):
            spans.sort(key=lambda span: Q(*span[0]))
    low, high = target
    cursor = low
    for span_low, span_high in spans:
        if ratio_lt(span_high, cursor):
            continue
        if ratio_lt(cursor, span_low):
            return False
        if ratio_lt(cursor, span_high):
            cursor = span_high
        if not ratio_lt(cursor, high):
            return True
    return not ratio_lt(cursor, high)


def _widen(found: Section | None, low: Ratio, high: Ratio) -> Section:
    if found is None:
        return low, high
    return (
        low if ratio_lt(low, found[0]) else found[0],
        high if ratio_lt(found[1], high) else found[1],
    )


def covered_by_sweep(domain: list[Point], regions: list[list[Point]]) -> tuple[bool, Q | None]:
    """Whether the closed convex regions cover the domain, by an exact vertical sweep.

    Every polygon's vertex abscissa in the domain's x range and every crossing of two
    non-vertical edges there is an event. Between two consecutive events no edge begins
    or ends and no two edges cross, so the order of the edges' ordinates is constant on
    the open slab and coverage of the vertical section at one interior abscissa decides
    the whole slab; each event abscissa is checked on its own. At every probe the closed
    sections of the regions must cover the closed section of the domain. Points and
    segments cover no area and are left out; the regions are convex polygons in hull
    order. Returns the first uncovered abscissa, or None.
    """
    polygons: list[tuple[HPoint, ...]] = [tuple(homogeneous(v) for v in domain)]
    polygons.extend(
        tuple(homogeneous(v) for v in region) for region in regions if len(region) >= 3
    )
    left, right = ratio_extremes([(x, z) for x, _, z in polygons[0]])
    edges, verticals = compile_edges(polygons)
    positions = sweep_events(polygons, edges, left, right)
    require(
        positions[0] == normalised(*left) and positions[-1] == normalised(*right),
        "row domain endpoint missing",
    )
    probes = [positions[0]]
    for a, b in pairwise(positions):
        probes.extend((between(a, b), b))
    starts = sorted(range(len(edges)), key=lambda i: Q(*edges[i].lo))
    ends = sorted(range(len(edges)), key=lambda i: Q(*edges[i].hi))
    live: set[int] = set()
    started = ended = 0
    for probe in probes:
        while started < len(starts) and not ratio_lt(probe, edges[starts[started]].lo):
            live.add(starts[started])
            started += 1
        while ended < len(ends) and ratio_lt(edges[ends[ended]].hi, probe):
            live.discard(ends[ended])
            ended += 1
        xn, xd = probe
        sections: dict[int, Section] = {}
        for i in live:
            edge = edges[i]
            ordinate = (-(edge.a * xn + edge.c * xd), edge.b * xd)
            sections[edge.polygon] = _widen(sections.get(edge.polygon), ordinate, ordinate)
        for polygon, low, high in verticals.get(probe, ()):
            sections[polygon] = _widen(sections.get(polygon), low, high)
        target = sections.get(0)
        require(target is not None, "coverage probe outside domain")
        assert target is not None
        spans = [section for polygon, section in sections.items() if polygon != 0]
        if not section_covered(target, spans):
            return False, Q(*probe)
    return True, None


@dataclass
class CoverRow:
    """A partner row's admitted pose cover, kept on the accepted row.

    `domain_given` and `core_given` are the published lists exactly as admitted. A later
    step that publishes the same lists for the same accepted row has the same proof; any
    other publication is proved afresh. `minima` memoises the least value of `n . y`
    over the domain by facet direction, a pure function of the admitted domain.
    """

    domain_given: object
    core_given: object
    domain: tuple[HPoint, ...]
    core: tuple[HPoint, ...]
    minima: dict[Direction, Ratio] = field(default_factory=dict[Direction, Ratio])

    def minimum(self, nx: int, ny: int) -> Ratio:
        found = self.minima.get((nx, ny))
        if found is None:
            found = self.minima[(nx, ny)] = support(self.domain, nx, ny, largest=False)
        return found


# ---------------------------------------------------------------------------
# The cells, the objects and the state
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Cells:
    """The frame: cell names and exact polygons in order, the cap, and their source."""

    names: tuple[str, ...]
    polygons: tuple[tuple[Point, ...], ...]
    cap: Q
    source: dict[str, Any]


def cover_cells() -> Cells:
    """The n17 unique-state cover's exact cells, from the cover tool."""
    from devtools import check_n17_capacity_one_cover as cover  # noqa: PLC0415

    cells = cover.build_cover(cover.UNIQUE_24)
    return Cells(
        tuple(cell.name for cell in cells),
        tuple(tuple((Q(x), Q(y)) for x, y in cell.vertices) for cell in cells),
        Q(cover.U),
        {"kind": "cover", "design": cover.UNIQUE_24.name},
    )


def file_cells(path: Path, sha256: str) -> Cells:
    """Cells from a JSON file `{"U", "order", "cells"}` whose digest must be `sha256`."""
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    require(digest == sha256, f"cells file digest {digest} is not the stated one")
    data = json.loads(raw)
    names = tuple(data["order"])
    return Cells(
        names,
        tuple(tuple(poly(data["cells"][name])) for name in names),
        Q(data["U"]),
        {"kind": "file", "path": str(path), "sha256": digest},
    )


def load_object(path: Path, kind: str) -> tuple[dict[str, Any], str]:
    """A gzipped canonical JSON object named by the SHA-256 of its bytes."""
    raw = gzip.decompress(path.read_bytes())
    digest = hashlib.sha256(raw).hexdigest()
    require(path.name == f"{kind}-{digest}.json.gz", f"{kind} digest mismatch: {digest}")
    document = json.loads(raw)
    canonical = json.dumps(document, sort_keys=True, separators=(",", ":")).encode()
    require(hashlib.sha256(canonical).hexdigest() == digest, f"{kind} is not canonical JSON")
    return document, digest


@dataclass
class Row:
    interval: tuple[Q, Q]
    reference: Any
    outer: list[Point]
    residual: list[list[Point]]
    cover: CoverRow | None = None


CorePair = tuple[tuple[HPoint, ...], tuple[HPoint, ...]]
HullPair = tuple[tuple[Point, ...], tuple[Point, ...]]


@dataclass
class State:
    cells: list[list[Point]]
    cap: Q
    bins: int
    mask: list[int]
    groups: dict[int, list[Point]] = field(default_factory=dict[int, list[Point]])
    rows: dict[int, list[Row]] = field(default_factory=dict[int, list[Row]])
    stats: dict[str, int] = field(default_factory=dict[str, int])
    facets: dict[CorePair, list[Facet]] = field(default_factory=dict[CorePair, list[Facet]])
    forbidden: dict[HullPair, list[Point]] = field(default_factory=dict[HullPair, list[Point]])

    def tick(self, key: str, amount: int = 1) -> None:
        self.stats[key] = self.stats.get(key, 0) + amount

    def difference(self, partner: tuple[HPoint, ...], core: tuple[HPoint, ...]) -> list[Facet]:
        """The facets of `partner - core`, computed once per pair of cores."""
        found = self.facets.get((partner, core))
        if found is None:
            found = self.facets[(partner, core)] = difference_facets(partner, core)
        return found

    def forbidden_region(self, group: list[Point], core: list[Point]) -> list[Point]:
        """`hull(group - core)`, computed once per pair of owned hull and core."""
        key = (tuple(group), tuple(core))
        found = self.forbidden.get(key)
        if found is None:
            found = self.forbidden[key] = minkowski_diff(group, core)
        return found


def check_frame(seed: dict[str, Any], node: dict[str, Any], cells: Cells) -> list[int]:
    require(seed["schema"] == "generic_wall_seed_v1", "seed schema")
    require(node["schema"] == "exact_generic_owned_hull_v1", "node schema")
    for document in (seed, node):
        require(Q(document["U"]) == cells.cap, "the cap is not the cells' cap")
        require(Q(document["B"]) == 1, "field and physical coordinates differ")
    mask = seed["mask"]
    require(node["mask"] == mask, "the node's mask is not the seed's")
    require(
        isinstance(mask, list)
        and len(set(mask)) == len(mask) >= 2
        and all(isinstance(k, int) and 0 <= k < len(cells.names) for k in mask),
        "the mask is not a set of cell indices",
    )
    require(
        node["parent"] is None and node["constraints"] == [] and node["guard_source"] is None,
        "the node is not a root node",
    )
    require(len(seed["world"]) == len(cells.names), "the seed's world has the wrong size")
    for k, polygon in enumerate(cells.polygons):
        require(same_set(poly(seed["world"][k]), list(polygon)), f"world cell {k} differs")
    return mask


def check_seed(state: State, seed: dict[str, Any], node: dict[str, Any]) -> None:
    bins = state.bins
    for o in state.mask:
        points = poly(seed["groups"][str(o)])
        for pt in points:
            require(owned(state.cells[o], pt, state.cap), f"seed point {pt} of {o} not owned")
        state.groups[o] = hull(points)
        seed_rows = seed["cells"][str(o)]
        require(len(seed_rows) == bins, f"seed owner {o} has the wrong number of rows")
        rows: list[Row] = []
        for i, r in enumerate(seed_rows):
            lo, hi = Q(r["interval"][0]), Q(r["interval"][1])
            require((lo, hi) == (Q(i, bins), Q(i + 1, bins)), f"seed row {o}/{i} interval")
            domain = intersect_convex(list(state.cells[o]), wall_box(lo, hi, state.cap))
            require(same_set(poly(r["outer_domain"]), domain), f"seed row {o}/{i} domain")
            residual = [poly(x) for x in r["residual_polygons"]]
            require(
                (residual == [] and domain == [])
                or (len(residual) == 1 and same_set(residual[0], domain)),
                f"seed row {o}/{i} residual",
            )
            require(
                r["reference"] == {"kind": "wall_seed", "owner": o, "row": i},
                f"seed row {o}/{i} reference",
            )
            rows.append(
                Row((lo, hi), r["reference"], hull(domain), [hull(x) for x in residual])
            )
        state.rows[o] = rows
        state.tick("seed_points", len(points))
        state.tick("seed_rows", len(seed_rows))
    for o in state.mask:
        require(
            same_set(poly(node["initial"]["groups"][str(o)]), state.groups[o]),
            f"initial group {o}",
        )
        require(
            node["initial"]["cell_references"][str(o)] == [r.reference for r in state.rows[o]],
            f"initial references {o}",
        )


def admit_cover(row: Row, item: dict[str, Any], si: int, pj: int) -> CoverRow:
    """Prove one published partner row: its domain is the hull of the accepted row's
    residual vertices, and its core is strictly inside the square over the row."""
    vertices = [v for polygon in row.residual for v in polygon]
    domain = hull(vertices)
    require(
        same_set(poly(item["domain"]), domain),
        f"step {si} partner {pj} row {row.reference['row']} domain",
    )
    core = hull(poly(item["core"]))
    require(len(core) >= 3 and area2(core) > 0, f"step {si}: partner {pj} core")
    require(core_strict(core, *row.interval), f"step {si} partner {pj} core not strict")
    return CoverRow(
        item["domain"],
        item["core"],
        tuple(homogeneous(v) for v in domain),
        tuple(homogeneous(v) for v in core),
    )


def check_partners(state: State, step: dict[str, Any], si: int) -> dict[int, list[CoverRow]]:
    owner = step["owner"]
    partners: dict[int, list[CoverRow]] = {}
    for key, items in step["prior_partner_pose_covers"].items():
        pj = int(key)
        require(pj in state.mask and pj != owner, f"step {si}: partner {pj}")
        rows = state.rows[pj]
        require(len(items) == len(rows), f"step {si}: partner {pj} cover length")
        live: list[CoverRow] = []
        for item, r in zip(items, rows, strict=True):
            require(item["reference"] == r.reference, f"step {si}: partner {pj} reference")
            interval = (Q(item["interval"][0]), Q(item["interval"][1]))
            require(interval == r.interval, f"step {si}: partner {pj} interval")
            if not any(r.residual):
                require(item["domain"] == [] and item["core"] == [], f"step {si}: dead row")
                continue
            cover = r.cover
            if (
                cover is None
                or cover.domain_given != item["domain"]
                or cover.core_given != item["core"]
            ):
                cover = admit_cover(r, item, si, pj)
                r.cover = cover
            live.append(cover)
        require(bool(live), f"step {si}: empty partner cover")
        partners[pj] = live
        state.tick("partner_rows", len(live))
    return partners


def check_collisions(
    state: State,
    row: dict[str, Any],
    *,
    where: str,
    core: list[Point],
    required: list[Point],
    partners: dict[int, list[CoverRow]],
) -> list[list[Point]]:
    regions: list[list[Point]] = []
    core_h = tuple(homogeneous(v) for v in core)
    required_planes: list[Plane] | None = None
    for item in row["collision_regions"]:
        pj = item["partner"]
        require(pj in partners, f"{where}: collision partner {pj}")
        region = hull(poly(item["vertices"]))
        require(len(region) >= 3 and area2(region) > 0, f"{where}: degenerate region")
        if required_planes is None:
            required_planes = planes_of(required)
        require(
            all(a * v[0] + b * v[1] <= c for v in region for a, b, c in required_planes),
            f"{where}: collision region escapes the required domain",
        )
        region_h = [homogeneous(v) for v in region]
        for cover in partners[pj]:
            facets = state.difference(cover.core, core_h)
            require(len(facets) >= 3, f"{where}: degenerate difference")
            for nx, ny, hn, hd in facets:
                mn, md = cover.minimum(nx, ny)
                bound_n, bound_d = hn * md + mn * hd, hd * md
                state.tick("collision_facet_checks", len(region))
                for x, y, z in region_h:
                    require(
                        (nx * x + ny * y) * bound_d <= bound_n * z,
                        f"{where} partner {pj}: region escapes the collision set",
                    )
        regions.append(region)
        state.tick("collision_regions")
    return regions


def check_cover(
    state: State,
    owner: int,
    *,
    where: str,
    core: list[Point],
    required: list[Point],
    regions: tuple[list[list[Point]], list[list[Point]]],
) -> None:
    """The required domain is covered by forbidden, collision and residual regions."""
    collisions, residual = regions
    forbidden = [
        state.forbidden_region(state.groups[oj], core)
        for oj in state.mask
        if oj != owner and state.groups[oj]
    ]
    every = forbidden + collisions + residual
    if area2(required) > 0:
        ok, probe = covered_by_sweep(hull(required), every)
        require(ok, f"{where}: required domain NOT covered (uncovered at x={probe})")
    else:
        points = list(required)
        if len(points) == 2:
            points.append(
                ((points[0][0] + points[1][0]) / 2, (points[0][1] + points[1][1]) / 2)
            )
        for pt in points:
            require(
                any(inside(r, pt) for r in every if len(hull(r)) >= 3)
                or any(pt in r for r in residual),
                f"{where}: degenerate row uncovered",
            )
    state.tick("cover_checks")


def reference_key(reference: Any) -> str:
    return json.dumps(reference, sort_keys=True, separators=(",", ":"))


def predecessors(accepted: list[Row], rows: list[dict[str, Any]], si: int) -> list[Row]:
    """Each step row's accepted predecessor, after the rows are proved a refinement.

    The rows' intervals partition `[0, 1]` in order: the first starts at 0, each starts
    where the one before ends, each is nonempty, and the last ends at 1. Each row cites by
    `prior_reference` one of the owner's accepted rows, whose interval contains the row's.
    The accepted rows partition `[0, 1]` themselves, so the predecessor is the only one
    that can contain the row, and an unrefined row has exactly its predecessor's interval.
    """
    require(isinstance(rows, list) and len(rows) > 0, f"step {si}: no rows")
    by_reference = {reference_key(r.reference): r for r in accepted}
    require(len(by_reference) == len(accepted), f"step {si}: duplicate accepted reference")
    cursor = Q(0)
    found: list[Row] = []
    for ri, row in enumerate(rows):
        where = f"step {si} row {ri}"
        lo, hi = Q(row["interval"][0]), Q(row["interval"][1])
        require(lo == cursor, f"{where}: interval {'gap' if lo > cursor else 'overlap'}")
        require(lo < hi <= 1, f"{where}: interval is empty or ends past 1")
        cursor = hi
        prior = by_reference.get(reference_key(row["prior_reference"]))
        require(prior is not None, f"{where}: prior reference is not an accepted row")
        assert prior is not None
        require(
            prior.interval[0] <= lo and hi <= prior.interval[1],
            f"{where}: interval escapes its predecessor",
        )
        found.append(prior)
    require(cursor == 1, f"step {si}: the rows do not reach the end of the interval")
    return found


def check_step(
    state: State, step: dict[str, Any], si: int, node_id: Any, full: set[int]
) -> tuple[list[Row], list[Plane], bool]:
    owner = step["owner"]
    partners = check_partners(state, step, si)
    new_rows: list[Row] = []
    all_planes: list[Plane] = []
    any_live = False
    cited = predecessors(state.rows[owner], step["rows"], si)
    for ri, (row, prior) in enumerate(zip(step["rows"], cited, strict=True)):
        where = f"step {si} row {ri}"
        lo, hi = Q(row["interval"][0]), Q(row["interval"][1])
        require(
            row["reference"] == {"kind": "phase3", "node": node_id, "step": si, "row": ri},
            f"{where}: reference",
        )
        require(row.get("self_hull_cuts", []) == [], f"{where}: self-hull cuts")
        required = (
            intersect_convex(list(prior.outer), wall_box(lo, hi, state.cap))
            if prior.outer
            else []
        )
        residual = [hull(poly(x)) for x in row["residual_polygons"]]
        vertices = [v for polygon in residual for v in polygon]
        if not required:
            require(
                residual == []
                and row["collision_regions"] == []
                and row["common_core_halfplanes"] == []
                and row["outer_bounds"] == []
                and row["outer_domain"] == [],
                f"{where}: a dead row carries data",
            )
            new_rows.append(Row((lo, hi), row["reference"], [], []))
            continue
        core = hull(poly(row["core_vertices"]))
        require(len(core) >= 3 and area2(core) > 0, f"{where}: degenerate core")
        require(core_strict(core, lo, hi), f"{where}: core not strict")
        planes: list[Plane] = []
        if vertices:
            for k in range(len(core)):
                p, q = core[k], core[(k + 1) % len(core)]
                a, b = q[1] - p[1], p[0] - q[0]
                least = min(a * v[0] + b * v[1] for v in vertices)
                planes.append((a, b, a * p[0] + b * p[1] + least))
        published = [
            (Q(it["normal"][0]), Q(it["normal"][1]), Q(it["upper"]))
            for it in row["common_core_halfplanes"]
        ]
        require(set(published) == set(planes), f"{where}: common-core planes")
        all_planes.extend(planes)
        bounds = [
            (Q(it["normal"][0]), Q(it["normal"][1]), Q(it["upper"]))
            for it in row["outer_bounds"]
        ]
        if vertices:
            any_live = True
            require(len(bounds) == 8, f"{where}: outer bounds")
            for a, b, c in bounds:
                require(all(a * v[0] + b * v[1] <= c for v in vertices), f"{where}: bound")
            outer = list(state.cells[owner])
            for a, b, c in bounds:
                outer = clip_closed(outer, a, b, c)
            outer = hull(outer)
            require(same_set(poly(row["outer_domain"]), outer), f"{where}: outer domain")
        else:
            require(bounds == [] and row["outer_domain"] == [], f"{where}: dead bounds")
            outer = []
        if ri in full:
            state.tick("rows_full")
            regions = check_collisions(
                state, row, where=where, core=core, required=required, partners=partners
            )
            check_cover(
                state,
                owner,
                where=where,
                core=core,
                required=required,
                regions=(regions, residual),
            )
        new_rows.append(Row((lo, hi), row["reference"], outer, residual))
    return new_rows, all_planes, any_live


def compress(
    state: State, step: dict[str, Any], si: int, planes: list[Plane], *, any_live: bool
) -> None:
    owner = step["owner"]
    kernel = poly(step["common_owned_kernel"])
    for pt in kernel:
        require(0 <= pt[0] <= state.cap and 0 <= pt[1] <= state.cap, f"step {si}: kernel")
        require(
            all(a * pt[0] + b * pt[1] <= c for a, b, c in planes),
            f"step {si}: kernel point fails a plane",
        )
    if not (any_live and (state.groups[owner] or kernel)):
        require("inner_grid_compression" not in step, f"step {si}: unexpected compression")
        return
    original = hull(state.groups[owner] + kernel)
    require(same_set(poly(step["compression_source_hull"]), original), f"step {si}: source")
    record = step["inner_grid_compression"]
    points = poly(record["vertices"])
    require(len(points) == len(record["witnesses"]) > 0, f"step {si}: witnesses")
    for pt, witness in zip(points, record["witnesses"], strict=True):
        indices, weights = witness["indices"], [Q(x) for x in witness["weights"]]
        require(
            1 <= len(indices) <= 3
            and all(0 <= k < len(original) for k in indices)
            and all(x >= 0 for x in weights)
            and sum(weights) == 1,
            f"step {si}: witness weights",
        )
        combined = (
            sum(x * original[k][0] for k, x in zip(indices, weights, strict=True)),
            sum(x * original[k][1] for k, x in zip(indices, weights, strict=True)),
        )
        require(combined == pt == point(witness["point"]), f"step {si}: witness point")
        require(
            (pt[0] * GRID).denominator == 1 and (pt[1] * GRID).denominator == 1,
            f"step {si}: off the grid",
        )
    if record.get("mode") == "replace":
        state.groups[owner] = hull(points)
    else:
        state.groups[owner] = hull(state.groups[owner] + points)
    require(len(state.groups[owner]) <= HULL_LIMIT, f"step {si}: owned hull too large")


def derive_closure(state: State, owner: int, si: int) -> dict[str, Any] | None:
    if not any(r.residual for r in state.rows[owner]):
        return {"kind": "all_parent_poses_forbidden", "owner": owner, "step": si}
    for oj in sorted(state.mask):
        if oj != owner and state.groups[oj] and state.groups[owner]:
            common = (
                intersect_convex(list(state.groups[owner]), state.groups[oj])
                if len(state.groups[oj]) >= 3
                else []
            )
            if common:
                return {
                    "kind": "owned_hulls_intersect",
                    "owners": sorted((owner, oj)),
                    "step": si,
                }
    return None


def check_final(state: State, node: dict[str, Any], *, stall: bool) -> None:
    final = node["final_state"]
    for o in state.mask:
        require(same_set(poly(final["groups"][str(o)]), state.groups[o]), f"final group {o}")
        require(len(final["cells"][str(o)]) == len(state.rows[o]), f"final rows {o}")
        for recorded, r in zip(final["cells"][str(o)], state.rows[o], strict=True):
            require(recorded["reference"] == r.reference, f"final reference {o}")
            require(
                same_set(poly(recorded["outer_domain"]), r.outer)
                if r.outer
                else recorded["outer_domain"] == [],
                f"final outer domain {o}",
            )
            require(
                len(recorded["residual_polygons"]) == len(r.residual)
                and all(
                    same_set(poly(a), b)
                    for a, b in zip(recorded["residual_polygons"], r.residual, strict=True)
                ),
                f"final residual {o}",
            )
    require(node["closed"] is (not stall) and node["terminal"] is (not stall), "closed flags")
    require(
        node["mask_exclusion_proved"] is False and node["global_optimality_proved"] is False,
        "the node claims more than a closure",
    )


def verify_objects(
    directory: Path,
    cells: Cells,
    *,
    sample: int | None = None,
    sample_seed: int = 12345,
    progress: bool = False,
) -> dict[str, Any]:
    """Verify the seed and node saved in `directory`; raises on the first failure."""
    seeds = sorted(directory.glob("seed-*.json.gz"))
    nodes = sorted(directory.glob("node-*.json.gz"))
    require(
        len(seeds) == 1 and len(nodes) == 1, "the directory must hold one seed and one node"
    )
    seed, seed_sha = load_object(seeds[0], "seed")
    node, node_sha = load_object(nodes[0], "node")
    require(node["source"]["sha256"] == seed_sha, "the node's source is not the seed")
    mask = check_frame(seed, node, cells)
    bins = seed["bins"]
    require(isinstance(bins, int) and bins > 0, "bins")
    state = State([list(p) for p in cells.polygons], cells.cap, bins, mask)
    clock = time.perf_counter()
    check_seed(state, seed, node)
    contradiction = node["contradiction"]
    stall = contradiction is None
    closure_step = -1 if stall else contradiction["step"]
    rng = random.Random(sample_seed)
    derived: dict[str, Any] | None = None
    steps = node["steps"]
    for si, step in enumerate(steps):
        require(
            step["index"] == si and step["owner"] in mask and step["complete"] is True,
            f"step {si}: header",
        )
        require(step["allowed_half_angle"] == ["0", "1"], f"step {si}: allowed half-angle")
        owner = step["owner"]
        for o in mask:
            require(
                same_set(poly(step["prior_owned_hulls"][str(o)]), state.groups[o]),
                f"step {si}: prior hull {o}",
            )
        count = len(step["rows"])
        full = (
            set(range(count))
            if sample is None or si == closure_step
            else set(rng.sample(range(count), min(sample, count)))
        )
        new_rows, planes, any_live = check_step(state, step, si, node["node_id"], full)
        compress(state, step, si, planes, any_live=any_live)
        state.rows[owner] = new_rows
        state.tick("steps")
        derived = derive_closure(state, owner, si)
        if progress:
            live = sum(1 for r in new_rows if r.residual)
            print(
                json.dumps(
                    {
                        "step": si,
                        "owner": owner,
                        "live_rows": live,
                        "rows_checked_in_full": len(full),
                        "closure": derived is not None,
                        "seconds": round(time.perf_counter() - clock, 1),
                    }
                ),
                flush=True,
            )
        if derived is not None:
            require(
                si == closure_step
                and derived["kind"] == contradiction["kind"]
                and derived.get("owner") == contradiction.get("owner"),
                f"step {si}: the derived closure is not the declared one",
            )
            require(si == len(steps) - 1, "steps after the closure")
            break
    else:
        require(stall, "no closure derived")
    check_final(state, node, stall=stall)
    return {
        "certificate": {"seed_sha256": seed_sha, "node_sha256": node_sha},
        "mask": mask,
        "cells": [cells.names[k] for k in mask],
        "bins": bins,
        "closure": contradiction,
        "closed": not stall,
        "counts": dict(sorted(state.stats.items())),
    }


def verify(
    directory: Path,
    cells: Cells,
    *,
    sample: int | None = None,
    sample_seed: int = 12345,
    progress: bool = False,
) -> dict[str, Any]:
    """The verification receipt: PASS only for a closed certificate that checks in full."""
    clock = time.perf_counter()
    receipt: dict[str, Any] = {
        "schema": SCHEMA,
        "verifier": KIND,
        "verifier_sha256": MODULE_SHA256,
        "directory": str(directory),
        "cells_source": cells.source,
        "mode": "full" if sample is None else "sample",
        "sample_rows_per_step": sample,
        "sample_seed": None if sample is None else sample_seed,
    }
    try:
        result = verify_objects(
            directory, cells, sample=sample, sample_seed=sample_seed, progress=progress
        )
    except VerificationError as failure:
        receipt.update(status="FAIL", failure=str(failure))
    except (
        KeyError,
        TypeError,
        ValueError,
        IndexError,
        AttributeError,
        ZeroDivisionError,
        OSError,
    ) as failure:
        receipt.update(status="FAIL", failure=f"malformed certificate: {failure!r}")
    else:
        receipt.update(result)
        closed = result["closed"]
        receipt.update(
            status="PASS" if closed else "FAIL",
            failure=None if closed else "the node is a stall, not a closure",
        )
    receipt["seconds"] = round(time.perf_counter() - clock, 3)
    return receipt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("directory", type=Path, help="holds seed-*.json.gz, node-*.json.gz")
    _ = parser.add_argument("--cells", type=Path, help="a JSON cells file instead of the cover")
    _ = parser.add_argument("--cells-sha256", help="the cells file's SHA-256, required with it")
    _ = parser.add_argument("--sample", type=int, default=None, help="rows per step (sample)")
    _ = parser.add_argument("--sample-seed", type=int, default=12345)
    _ = parser.add_argument("--output", type=Path, required=True, help="the receipt")
    _ = parser.add_argument("--progress", action="store_true")
    arguments = parser.parse_args(argv)
    if arguments.cells is not None:
        if not arguments.cells_sha256:
            parser.error("--cells needs --cells-sha256")
        cells = file_cells(arguments.cells, arguments.cells_sha256)
    else:
        cells = cover_cells()
    receipt = verify(
        arguments.directory,
        cells,
        sample=arguments.sample,
        sample_seed=arguments.sample_seed,
        progress=arguments.progress,
    )
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    _ = arguments.output.write_text(json.dumps(receipt, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: receipt.get(k) for k in ("status", "failure", "mode", "seconds")}))
    return 0 if receipt["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
