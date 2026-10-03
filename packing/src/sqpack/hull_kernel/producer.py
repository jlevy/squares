"""A deliberately simple mode-A producer: it proposes, and `sequential` certifies.

Nothing this module returns is evidence. It writes a seed (`generic_wall_seed_v1`) and a
node (`exact_generic_owned_hull_v1`, sequential grammar) for a set of owner cells, and
only `sequential.replay_sequential`, run on exactly those objects, decides whether the
node closes. The policy is the adaptation spec's first producer (section 5, slice 1):

* the seed owns grid points near each cell's vertex centroid, each kept only if
  `ownership` proves it from the cell alone, and gives every owner `bins` uniform rows;
* owners update round-robin in mask order, one complete step each, with no self-hull
  cuts; rows stay uniform unless a `SplitPolicy` bisects them at round ends;
* a row's core is the envelope square: side `(B - slack)/factor` turned to the row's
  midpoint angle, the counting mode's strict core, kept only if `strict_core` accepts it;
* a row's residual is its legal domain minus every other owner's forbidden region
  `K_j - Q_i`, by exact convex subtraction, keeping positive-area pieces of a
  positive-area domain;
* a row's outer domain is its residual's eight supports, rounded outward to `10^-8`;
* the kernel is the intersection of every live row's common-core planes, and it is
  promoted by grid points (denominator `2^20`) inside the hull of the prior hull and the
  kernel, each an exact convex combination of at most three of its vertices.

It stops at the first closure it sees, after `max_rounds` rounds, when a round changes
no owner's rows or hull, or at `stop_at`, leaving the checker time to certify the steps
made so far (a node without closure is a stall, and excludes nothing).
"""

from __future__ import annotations

import hashlib
import json
import math
import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from typing import Any, Protocol

from sqpack.hull_kernel.collision import SUPPORT_NORMALS, outward_round
from sqpack.hull_kernel.counting import row_envelope
from sqpack.hull_kernel.covers import convex_halfplanes
from sqpack.hull_kernel.frame import Frame
from sqpack.hull_kernel.geometry import (
    Budget,
    Halfplane,
    IncompleteError,
    Point,
    Polygon,
    RefusalError,
    area2,
    clip,
    intersect,
    trig,
)
from sqpack.hull_kernel.induction import (
    common_core_planes,
    encode,
    forbidden_regions,
    hull,
    strict_core,
    wall_lines,
)
from sqpack.hull_kernel.node import Row, points
from sqpack.hull_kernel.ownership import ownership
from sqpack.hull_kernel.rational import Q, Z
from sqpack.hull_kernel.sequential import derived_closure, owner_extents

GRID = 2**20


def content_sha256(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _grid(value: Q) -> Q:
    return Q(round(value * GRID), GRID)


def _encode_point(point: Point) -> list[str]:
    return [str(point[0]), str(point[1])]


def seed_points(frame: Frame, owner: int, *, budget: Budget) -> list[Point]:
    """Grid points near the cell's vertex centroid that `ownership` proves owned."""
    cell = frame.world(owner)
    cx = sum((x for x, _ in cell), Q()) / len(cell)
    cy = sum((y for _, y in cell), Q()) / len(cell)
    candidates = [(_grid(cx), _grid(cy))]
    candidates.extend(
        (_grid(cx + (x - cx) * fraction), _grid(cy + (y - cy) * fraction))
        for x, y in cell
        for fraction in (Q(1, 8), Q(1, 4))
    )
    owned: list[Point] = []
    for point in dict.fromkeys(candidates):
        try:
            ownership(frame, owner, point, budget=Budget(budget.deadline, 4000))
        except IncompleteError, RefusalError:
            continue
        owned.append(point)
    return owned


def build_seed(
    frame: Frame, mask: Sequence[int], *, bins: int, budget: Budget
) -> dict[str, Any]:
    groups: dict[str, list[list[str]]] = {}
    cells: dict[str, list[Row]] = {}
    for owner in mask:
        owned = seed_points(frame, owner, budget=budget)
        groups[str(owner)] = [_encode_point(point) for point in owned]
        rows: list[Row] = []
        for index in range(bins):
            lo, hi = Q(index, bins), Q(index + 1, bins)
            domain = intersect(frame.world(owner), wall_lines(frame, lo, hi))
            rows.append(
                {
                    "interval": [str(lo), str(hi)],
                    "residual_polygons": [encode(domain)] if domain else [],
                    "outer_domain": encode(domain),
                    "outer_bounds": [],
                    "reference": {"kind": "wall_seed", "owner": owner, "row": index},
                }
            )
        cells[str(owner)] = rows
    return {
        "schema": "generic_wall_seed_v1",
        "mask_index": None,
        "mask": list(mask),
        "U": str(frame.cap),
        "B": str(frame.scale),
        "bins": bins,
        "groups": groups,
        "cells": cells,
        "world": [encode(frame.world(cell)) for cell in range(len(frame.cells))],
    }


def envelope_core(frame: Frame, lo: Q, hi: Q) -> Polygon:
    """The row's strict core: the envelope square turned to the midpoint angle."""
    side, _, c, s = row_envelope(frame, (lo, hi))
    for _ in range(8):
        half = side / 2
        core = hull(
            [(c * u - s * v, s * u + c * v) for u in (-half, half) for v in (-half, half)]
        )
        try:
            strict_core(frame, core, lo, hi)
        except RefusalError:
            side *= 1 - Q(1, 2**20)
            continue
        return core
    raise RefusalError("no envelope core is strictly inside the row")


def subtract(pieces: list[Polygon], region: Polygon, *, keep_area_only: bool) -> list[Polygon]:
    """Convex pieces covering the closure of `pieces` minus the closed convex `region`."""
    planes = convex_halfplanes(region)
    result: list[Polygon] = []
    for piece in pieces:
        rest = piece
        for a, b, c in planes:
            outside = clip(rest, (-a, -b, -c))
            if outside and (area2(outside) > 0 or not keep_area_only):
                result.append(outside)
            rest = clip(rest, (a, b, c))
            if not rest:
                break
    return result


def _barycentric(original: Polygon, point: Point) -> tuple[list[int], list[Q]] | None:
    if len(original) == 1:
        return ([0], [Q(1)]) if original[0] == point else None
    if len(original) == 2:
        return ([original.index(point)], [Q(1)]) if point in original else None
    ax, ay = original[0]
    for j in range(1, len(original) - 1):
        (bx, by), (cx, cy) = original[j], original[j + 1]
        det = (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)
        if det == 0:
            continue
        px, py = point[0] - ax, point[1] - ay
        u = (px * (cy - ay) - py * (cx - ax)) / det
        v = ((bx - ax) * py - (by - ay) * px) / det
        if u >= 0 and v >= 0 and u + v <= 1:
            return [0, j, j + 1], [1 - u - v, u, v]
    return None


def compress(original: Polygon) -> tuple[list[Point], list[dict[str, Any]]]:
    """Grid points inside `original`, each with its exact convex-combination witness.

    When every vertex is already a grid point (seed points and kernel points are), the
    vertices are kept, each its own witness; otherwise grid points are pulled inward.
    """
    if all((x * GRID).denominator == 1 and (y * GRID).denominator == 1 for x, y in original):
        return list(original), [
            {"point": _encode_point(point), "indices": [index], "weights": ["1"]}
            for index, point in enumerate(original)
        ]
    n = len(original)
    cx = sum((x for x, _ in original), Q()) / n
    cy = sum((y for _, y in original), Q()) / n
    chosen: dict[Point, tuple[list[int], list[Q]]] = {}
    for x, y in original:
        for pull in (Q(1, 2**12), Q(1, 2**8), Q(1, 2**4), Q(1, 4)):
            point = (_grid(x + (cx - x) * pull), _grid(y + (cy - y) * pull))
            witness = _barycentric(original, point)
            if witness is not None:
                chosen.setdefault(point, witness)
                break
    if not chosen:
        for index, point in enumerate(original):
            if (point[0] * GRID).denominator == 1 and (point[1] * GRID).denominator == 1:
                chosen[point] = ([index], [Q(1)])
    if not chosen:
        raise RefusalError("no grid point lies in the compression source hull")
    selected = list(chosen.items())
    return [point for point, _ in selected], [
        {
            "point": _encode_point(point),
            "indices": indices,
            "weights": [str(weight) for weight in weights],
        }
        for point, (indices, weights) in selected
    ]


def octagon_core(frame: Frame, lo: Q, hi: Q) -> Polygon:
    """A second-order strict core: the two end-angle squares' intersection, scaled in.

    Both end squares have half-side `h = (B - slack)/2`. A unit vector `u` at an angle
    between the ends is `(sin(b - x) u_a + sin(x - a) u_b)/sin(D)` for row width `D`, so for
    a point `p` in both end squares `|p.u| <= h (sin(b - x) + sin(x - a))/sin(D)
    <= h/cos(D/2)`, and the same holds for the normal direction. Scaling the octagon by
    `cos^2(D/2) = (1 + cos D)/2`, which is rational in the half-angle chart, therefore puts
    it strictly inside every square of the row, losing about `D^2/4` of its size where
    the envelope core loses about `D/2`. `strict_core` checks it exactly all the same.
    """
    half = (frame.scale - frame.core_slack) / 2
    (ca, sa), (cb, sb) = trig(lo), trig(hi)
    square = [
        (ca * u - sa * v, sa * u + ca * v)
        for u, v in ((-half, -half), (half, -half), (half, half), (-half, half))
    ]
    octagon = intersect(
        square, [(cb, sb, half), (-cb, -sb, half), (-sb, cb, half), (sb, -cb, half)]
    )
    shrink = (1 + ca * cb + sa * sb) / 2
    core = hull([(shrink * x, shrink * y) for x, y in octagon])
    strict_core(frame, core, lo, hi)
    return core


CORES = {"envelope": envelope_core, "octagon": octagon_core}
# `CollisionTerms.pairs` is emptied at a step's start once it holds more pairs than this.
# Uniform rows give at most `bins` squared, which a production keeps throughout; adaptive
# rows give many more. The terms are a pure function of the two cores, so emptying the
# memo recomputes them and changes nothing produced.
TERM_MEMO_PAIRS = 1 << 15


class CoreCache(dict[tuple[Q, Q], Polygon]):
    """Strict cores by row interval, all of one kind (`CORES`)."""

    def __init__(self, kind: str = "envelope") -> None:
        super().__init__()
        if kind not in CORES:
            raise RefusalError(f"unknown core kind: {kind}")
        self.kind = kind


def cached_core(
    frame: Frame, lo: Q, hi: Q, cores: dict[tuple[Q, Q], Polygon] | None
) -> Polygon:
    build = CORES[cores.kind] if isinstance(cores, CoreCache) else envelope_core
    if cores is None:
        return build(frame, lo, hi)
    if (lo, hi) not in cores:
        cores[(lo, hi)] = build(frame, lo, hi)
    return cores[(lo, hi)]


RowKey = tuple[str, str]


@dataclass(frozen=True)
class PartnerRow:
    """One live partner row, with what every query row reuses computed once.

    `own` holds, for each outward edge normal `n` of the partner core `Q_r`, the support
    `max over Q_r of n.v` plus `min over D_r of n.y`: the part of that facet's bound that
    does not depend on the query core. `key` is the row's interval, which names its core
    within one production, and `domain_max` memoises `max over D_r of m.v` by the query
    core's key and normal index, a pure function of the domain.
    """

    domain: Polygon
    core: Polygon
    own: tuple[tuple[Q, Q, Q], ...]
    float_domain: tuple[tuple[float, float], ...]
    float_own: tuple[tuple[float, float, float], ...]
    key: RowKey = ("", "")
    domain_max: dict[tuple[RowKey, int], Q] = field(default_factory=dict)


def _normals(polygon: Polygon) -> list[tuple[Q, Q]]:
    """Outward edge normals of a counterclockwise convex polygon."""
    return [
        (b[1] - a[1], a[0] - b[0])
        for a, b in zip(polygon, polygon[1:] + polygon[:1], strict=True)
    ]


def prepare_partner(domain: Polygon, core: Polygon, key: RowKey = ("", "")) -> PartnerRow:
    own = tuple(
        (
            nx,
            ny,
            max(nx * x + ny * y for x, y in core) + min(nx * x + ny * y for x, y in domain),
        )
        for nx, ny in _normals(core)
    )
    return PartnerRow(
        domain,
        core,
        own,
        tuple((float(x), float(y)) for x, y in domain),
        tuple((float(a), float(b), float(c)) for a, b, c in own),
        key,
    )


@dataclass(frozen=True)
class CoreTerms:
    """One core's outward normals and its support in each of them."""

    normals: tuple[tuple[Q, Q], ...]
    own_max: tuple[Q, ...]


class CollisionTerms:
    """The core-only terms of `collision_planes`, memoised by row interval within one
    production (where an interval names one core): a core's own terms, and for a pair of
    cores the support of each in the other's normals. The planes built from them are the
    same `Fraction` values as the uncached form's, so the floats the prefilter clips with
    and the regions written are unchanged.
    """

    def __init__(self) -> None:
        self.cores: dict[RowKey, CoreTerms] = {}
        self.pairs: dict[tuple[RowKey, RowKey], tuple[tuple[Q, ...], tuple[Q, ...]]] = {}

    def core(self, key: RowKey, core: Polygon) -> CoreTerms:
        found = self.cores.get(key)
        if found is None:
            normals = tuple(_normals(core))
            found = self.cores[key] = CoreTerms(
                normals, tuple(max(mx * x + my * y for x, y in core) for mx, my in normals)
            )
        return found

    def pair(
        self, key: RowKey, core: Polygon, query: CoreTerms, partner: PartnerRow
    ) -> tuple[tuple[Q, ...], tuple[Q, ...]]:
        """`min over the query core of n.w` for each partner normal `n`, and `min over the
        partner core of m.v` for each query normal `m`."""
        found = self.pairs.get((key, partner.key))
        if found is None:
            found = self.pairs[(key, partner.key)] = (
                tuple(min(nx * x + ny * y for x, y in core) for nx, ny, _ in partner.own),
                tuple(
                    min(mx * x + my * y for x, y in partner.core) for mx, my in query.normals
                ),
            )
        return found


def cached_collision_planes(
    key: RowKey, core: Polygon, partner: PartnerRow, terms: CollisionTerms
) -> list[Halfplane]:
    """`collision_planes` with its core-only terms read from `terms`: the same planes."""
    query = terms.core(key, core)
    in_query, in_partner = terms.pair(key, core, query, partner)
    planes: list[Halfplane] = [
        (nx, ny, own - in_query[index]) for index, (nx, ny, own) in enumerate(partner.own)
    ]
    for index, (mx, my) in enumerate(query.normals):
        furthest = partner.domain_max.get((key, index))
        if furthest is None:
            furthest = partner.domain_max[(key, index)] = max(
                mx * x + my * y for x, y in partner.domain
            )
        planes.append((-mx, -my, query.own_max[index] - in_partner[index] - furthest))
    return planes


def collision_planes(core: Polygon, partner: PartnerRow) -> list[Halfplane]:
    """The facets of `Q_r - Q_i`, each shifted by `min over D_r`, by edge merge.

    A Minkowski sum's facet normals are its summands' edge normals: `Q_r`'s, with support
    `h_r(n) - min over Q_i of n.w`, and `-Q_i`'s, which are `-m` for each normal `m` of
    `Q_i`, with support `max over Q_i of m.w - min over Q_r of m.v`. The planes cut out
    exactly the polygon the hull of the pairwise differences bounds, with no hull built.
    """
    planes: list[Halfplane] = [
        (nx, ny, own - min(nx * x + ny * y for x, y in core)) for nx, ny, own in partner.own
    ]
    for mx, my in _normals(core):
        planes.append(
            (
                -mx,
                -my,
                max(mx * x + my * y for x, y in core)
                - min(mx * x + my * y for x, y in partner.core)
                - max(mx * x + my * y for x, y in partner.domain),
            )
        )
    return planes


def _integer_planes(planes: list[Halfplane]) -> list[tuple[Z, Z, Z]]:
    result: list[tuple[Z, Z, Z]] = []
    for a, b, c in planes:
        scale = math.lcm(a.denominator, b.denominator, c.denominator)
        result.append(
            (
                a.numerator * (scale // a.denominator),
                b.numerator * (scale // b.denominator),
                c.numerator * (scale // c.denominator),
            )
        )
    return result


def _satisfies(planes: list[tuple[Z, Z, Z]], point: Point) -> bool:
    """`a x + b y <= c` for every integer plane, at a rational point, by cross-multiplying."""
    x, y = point
    z = math.lcm(x.denominator, y.denominator)
    px, py = x.numerator * (z // x.denominator), y.numerator * (z // y.denominator)
    return all(a * px + b * py <= c * z for a, b, c in planes)


def collision_region(
    core: Polygon,
    domain: Polygon,
    partner_rows: list[PartnerRow],
    *,
    key: RowKey | None = None,
    terms: CollisionTerms | None = None,
) -> Polygon:
    """A convex part of `domain` every centre of which collides with every partner pose.

    The exact set is the domain cut by every facet `n.p <= h + min over D_r of n.y` of
    every live partner row's `Q_r - Q_i` (`collision_planes`). It is located in floating
    point; the region returned is the hull of grid points pulled inside it and of the
    domain's own vertices, each kept only if it satisfies every one of those halfplanes and
    the domain's exactly, in integers; the checker verifies the same inequalities itself.
    With `key` and `terms` the planes come from the memoised form, with the same values.
    """
    if not _float_collision(core, domain, partner_rows):
        return []
    if key is None or terms is None:
        planes = [
            plane for partner in partner_rows for plane in collision_planes(core, partner)
        ]
    else:
        planes = [
            plane
            for partner in partner_rows
            for plane in cached_collision_planes(key, core, partner, terms)
        ]
    region = [(float(x), float(y)) for x, y in domain]
    for a, b, c in planes:
        region = _float_clip(region, float(a), float(b), float(c))
        if len(region) < 3:
            return []
    integer = _integer_planes(planes + convex_halfplanes(domain))
    cx = sum(x for x, _ in region) / len(region)
    cy = sum(y for _, y in region) / len(region)
    kept = [vertex for vertex in domain if _satisfies(integer, vertex)]
    for x, y in region:
        for pull in (2.0**-12, 2.0**-6, 2.0**-3):
            point = (
                Q(round((x + (cx - x) * pull) * GRID), GRID),
                Q(round((y + (cy - y) * pull) * GRID), GRID),
            )
            if _satisfies(integer, point):
                kept.append(point)
                break
    polygon = hull(kept)
    return polygon if len(polygon) >= 3 and area2(polygon) > 0 else []


def _float_collision(core: Polygon, domain: Polygon, partner_rows: list[PartnerRow]) -> bool:
    """Whether the collision set meets the domain in floating point: a cheap prefilter
    that only decides whether the exact construction is worth attempting."""
    query = [(float(x), float(y)) for x, y in core]
    query_normals = [
        (b[1] - a[1], a[0] - b[0]) for a, b in zip(query, query[1:] + query[:1], strict=True)
    ]
    region = [(float(x), float(y)) for x, y in domain]
    for partner in partner_rows:
        partner_core = [(float(x), float(y)) for x, y in partner.core]
        planes = [
            (nx, ny, own - min(nx * x + ny * y for x, y in query))
            for nx, ny, own in partner.float_own
        ]
        planes.extend(
            (
                -mx,
                -my,
                max(mx * x + my * y for x, y in query)
                - min(mx * x + my * y for x, y in partner_core)
                - max(mx * x + my * y for x, y in partner.float_domain),
            )
            for mx, my in query_normals
        )
        for a, b, c in planes:
            region = _float_clip(region, a, b, c)
            if len(region) < 3:
                return False
    return True


PartnerMemo = dict[int, tuple[Row, PartnerRow]]


def partner_cover(
    frame: Frame,
    accepted: list[Row],
    cores: dict[tuple[Q, Q], Polygon],
    memo: PartnerMemo | None = None,
) -> tuple[list[dict[str, Any]], list[PartnerRow]]:
    """A partner's complete pose cover in the grammar, and its live rows.

    `memo` keeps each accepted row's `PartnerRow`, by the identity of the row object it
    was built from (held in the entry, so the identity cannot be reused), across the
    steps that republish the row unchanged; a replaced row object builds a new one, and
    `produce` drops the replaced row's entry.
    """
    given: list[dict[str, Any]] = []
    live: list[PartnerRow] = []
    for row in accepted:
        vertices = [
            vertex for polygon in row["residual_polygons"] for vertex in points(polygon)
        ]
        item: dict[str, Any] = {
            "reference": row["reference"],
            "interval": row["interval"],
            "domain": [],
            "core": [],
        }
        if vertices:
            lo, hi = (Q(value) for value in row["interval"])
            domain, core = hull(vertices), cached_core(frame, lo, hi, cores)
            item["domain"], item["core"] = encode(domain), encode(core)
            entry = None if memo is None else memo.get(id(row))
            if entry is not None and entry[0] is row:
                prepared = entry[1]
            else:
                prepared = prepare_partner(
                    domain, core, (row["interval"][0], row["interval"][1])
                )
                if memo is not None:
                    memo[id(row)] = (row, prepared)
            live.append(prepared)
        given.append(item)
    return given, live


def bounded_vertices(original: Polygon, limit: int) -> list[int]:
    """Indices of at most `limit` vertices, dropping the one that costs least area first."""
    kept = list(range(len(original)))
    while len(kept) > max(limit, 3):
        losses = []
        for position, index in enumerate(kept):
            a = original[kept[position - 1]]
            b = original[index]
            c = original[kept[(position + 1) % len(kept)]]
            losses.append(abs((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])))
        kept.pop(losses.index(min(losses)))
    return kept


def produce_row(
    frame: Frame,
    *,
    node_id: str,
    step_index: int,
    row_index: int,
    owner: int,
    predecessor: Row,
    groups: dict[int, Polygon],
    partners: dict[int, list[PartnerRow]] | None = None,
    cores: dict[tuple[Q, Q], Polygon] | None = None,
    terms: CollisionTerms | None = None,
    interval: tuple[Q, Q] | None = None,
) -> tuple[dict[str, Any], Row, list[Halfplane]]:
    """One row from its accepted predecessor: over the predecessor's own interval, or,
    for a refined row, over `interval`, which lies inside it."""
    if interval is None:
        lo, hi = (Q(value) for value in predecessor["interval"])
        key: RowKey = (predecessor["interval"][0], predecessor["interval"][1])
    else:
        lo, hi = interval
        key = (str(lo), str(hi))
    reference = {"kind": "phase3", "node": node_id, "step": step_index, "row": row_index}
    required = intersect(hull(points(predecessor["outer_domain"])), wall_lines(frame, lo, hi))
    accepted: Row = {
        "interval": [str(lo), str(hi)],
        "reference": reference,
        "outer_domain": [],
        "residual_polygons": [],
    }
    row: dict[str, Any] = {
        "interval": [str(lo), str(hi)],
        "prior_reference": predecessor["reference"],
        "reference": reference,
        "input_domain": encode(required),
        "core_vertices": [],
        "collision_regions": [],
        "residual_polygons": [],
        "common_core_halfplanes": [],
        "outer_bounds": [],
        "outer_domain": [],
    }
    if not required:
        return row, accepted, []
    core = cached_core(frame, lo, hi, cores)
    row["core_vertices"] = encode(core)
    pieces = [list(required)]
    positive = area2(required) > 0
    removed = [region for region in forbidden_regions(groups, owner, core) if region]
    for partner, live in sorted((partners or {}).items()):
        region = collision_region(core, required, live, key=key, terms=terms)
        if region:
            row["collision_regions"].append({"partner": partner, "vertices": encode(region)})
            removed.append(region)
    for region in removed:
        pieces = subtract(pieces, region, keep_area_only=positive)
        if not pieces:
            break
    residual = [hull(piece) for piece in pieces]
    vertices = [point for piece in residual for point in piece]
    planes = common_core_planes(hull(core), vertices)
    row["residual_polygons"] = [encode(piece) for piece in residual]
    row["common_core_halfplanes"] = [
        {"normal": [str(nx), str(ny)], "upper": str(upper)} for nx, ny, upper in planes
    ]
    if vertices:
        bounds = [
            (Q(nx), Q(ny), outward_round(max(nx * x + ny * y for x, y in vertices)))
            for nx, ny in SUPPORT_NORMALS
        ]
        outer = hull(intersect(frame.world(owner), bounds))
        row["outer_bounds"] = [
            {"normal": [str(nx), str(ny)], "upper": str(upper)} for nx, ny, upper in bounds
        ]
        row["outer_domain"] = encode(outer)
        accepted["outer_domain"] = encode(outer)
        accepted["residual_polygons"] = [encode(piece) for piece in residual]
    return row, accepted, planes


def _float_clip(
    polygon: list[tuple[float, float]], a: float, b: float, c: float
) -> list[tuple[float, float]]:
    out: list[tuple[float, float]] = []
    for p, q in zip(polygon, polygon[1:] + polygon[:1], strict=True):
        dp, dq = a * p[0] + b * p[1] - c, a * q[0] + b * q[1] - c
        if dp <= 0:
            out.append(p)
        if dp * dq < 0:
            z = dp / (dp - dq)
            out.append((p[0] + z * (q[0] - p[0]), p[1] + z * (q[1] - p[1])))
    return out


def kernel_points(frame: Frame, planes: list[Halfplane]) -> list[Point]:
    """Grid points proved, exactly, to satisfy every plane; the region is found in floats.

    Clipping a box by a few hundred exact halfplanes in turn compounds denominators, so
    the plane intersection is located in floating point only to choose candidates; each
    candidate is a grid point checked exactly against every plane, as the checker will.
    """
    if not planes:
        return []
    side = float(frame.length)
    region = [(0.0, 0.0), (side, 0.0), (side, side), (0.0, side)]
    for a, b, c in planes:
        region = _float_clip(region, float(a), float(b), float(c))
        if not region:
            return []
    cx = sum(x for x, _ in region) / len(region)
    cy = sum(y for _, y in region) / len(region)
    candidates = [(Q(round(cx * GRID), GRID), Q(round(cy * GRID), GRID))]
    candidates.extend(
        (
            Q(round((x + (cx - x) * pull) * GRID), GRID),
            Q(round((y + (cy - y) * pull) * GRID), GRID),
        )
        for x, y in region
        for pull in (2.0**-12, 2.0**-6, 0.25, 0.5)
    )
    return [
        point
        for point in dict.fromkeys(candidates)
        if all(0 <= coordinate <= frame.length for coordinate in point)
        and all(a * point[0] + b * point[1] <= c for a, b, c in planes)
    ]


AXIS_PEAK = math.sqrt(2) - 1  # the half-angle of the diagonal, where (cos + sin)/2 peaks


def _half_extent(t: float) -> float:
    """A unit square's axis-parallel half-extent `(cos + sin)/2` at half-angle `t`."""
    return (1 - t * t + 2 * t) / (2 * (1 + t * t))


def wall_loss(frame: Frame, lo: Q, hi: Q, residual: Sequence[Point]) -> float:
    """How much nearer a wall a row's legal box lets a centre sit than its own turn allows,
    when a residual vertex lies in that band; zero otherwise.

    The legal box of `[lo, hi]` uses the least half-extent over the row, so a square turned
    elsewhere in the row may sit up to the difference into the wall, about half the row's
    angular width near an axis and nothing at the diagonal. A split priority only, in
    floating point: nothing here is evidence.
    """
    a, b = float(lo), float(hi)
    least = min(_half_extent(a), _half_extent(b))
    most = (
        _half_extent(AXIS_PEAK) if a < AXIS_PEAK < b else max(_half_extent(a), _half_extent(b))
    )
    scale, offset = float(frame.scale), float((frame.cap - frame.inner_cap) / 2)
    low, high = scale * (offset + most), scale * (float(frame.cap) - offset - most)
    near = any(
        min(float(x), float(y)) < low or max(float(x), float(y)) > high for x, y in residual
    )
    return most - least if near else 0.0


@dataclass(frozen=True)
class SplitPolicy:
    """Opt-in adaptive rows; without one every owner keeps the seed's uniform rows.

    At a round's end, a live row whose outer domain has not shrunk for `patience` rounds
    running (a new half against the row it refines) is a candidate if its halves are no
    narrower than `1/floor` in `t`. Candidates are bisected, the widest wall loss first
    (`wall_loss`), then the widest row, while the rows over all owners stay within
    `max_rows`. At the owner's next step both halves cite the split row as their accepted
    predecessor, which is the refinement the checker's `complete_refinement` admits.
    """

    floor: int
    max_rows: int
    patience: int = 1

    def __post_init__(self) -> None:
        if self.floor <= 0 or self.max_rows <= 0 or self.patience <= 0:
            raise RefusalError("a split policy needs a positive floor, ceiling and patience")


Plan = list[tuple[tuple[Q, Q] | None, Row]]
"""An owner's next step: each row's interval (None for the predecessor's own) and the
accepted row it refines."""


def split_rows(
    frame: Frame,
    mask: Sequence[int],
    *,
    rows: dict[int, list[Row]],
    plans: dict[int, Plan],
    history: dict[tuple[int, str, str], tuple[Q, int]],
    policy: SplitPolicy,
) -> int:
    """Bisect the round's stuck rows into `plans`, by `SplitPolicy`; return how many.

    `history` holds, by owner and interval, the outer-domain area a row is measured
    against and how many rounds running it has not shrunk; it is updated in place.
    """
    candidates: list[tuple[float, Q, int, Q, int, int]] = []
    for position, owner in enumerate(mask):
        for index, row in enumerate(rows[owner]):
            key = (owner, row["interval"][0], row["interval"][1])
            outer = points(row["outer_domain"])
            area = area2(hull(outer)) if outer else Q()
            before = history.get(key)
            stuck = (
                before[1] + 1
                if row["residual_polygons"] and before is not None and area >= before[0]
                else 0
            )
            history[key] = (area, stuck)
            lo, hi = (Q(value) for value in row["interval"])
            if stuck >= policy.patience and (hi - lo) * policy.floor >= 2:
                residual = [v for poly in row["residual_polygons"] for v in points(poly)]
                weight = wall_loss(frame, lo, hi, residual)
                candidates.append((-weight, lo - hi, position, lo, owner, index))
    room = policy.max_rows - sum(len(plans[owner]) for owner in mask)
    chosen = sorted(candidates)[: max(room, 0)]
    by_owner: dict[int, set[int]] = {}
    for *_, owner, index in chosen:
        by_owner.setdefault(owner, set()).add(index)
    for owner, indices in by_owner.items():
        plan: Plan = []
        for index, row in enumerate(rows[owner]):
            if index not in indices:
                plan.append((None, row))
                continue
            lo, hi = (Q(value) for value in row["interval"])
            middle = (lo + hi) / 2
            for half in ((lo, middle), (middle, hi)):
                plan.append((half, row))
                history[(owner, str(half[0]), str(half[1]))] = (
                    history[(owner, row["interval"][0], row["interval"][1])][0],
                    0,
                )
        plans[owner] = plan
    return len(chosen)


class StepLog(Protocol):
    """Where `produce` keeps its steps: it appends each and counts them, nothing more, so
    a log that writes them out holds none of them (`check_n17_subpattern.SpilledSteps`)."""

    def append(self, step: dict[str, Any], /) -> None: ...

    def __len__(self) -> int: ...


@dataclass
class Production:
    seed: dict[str, Any]
    node: dict[str, Any]
    rounds: list[dict[str, Any]] = field(default_factory=list)
    outcome: str = "stalled"


def produce(
    frame: Frame,
    mask: Sequence[int],
    *,
    bins: int = 64,
    max_rounds: int = 8,
    budget: Budget,
    node_id: str = "n17-subpattern",
    progress: Callable[[dict[str, Any]], None] | None = None,
    collision: bool = True,
    hull_limit: int | None = 16,
    stop_at: float | None = None,
    core: str = "envelope",
    split: SplitPolicy | None = None,
    step_log: StepLog | None = None,
) -> Production:
    """Seed, then round-robin complete steps until closure, a stall or the round cap.

    With `split`, rows are refined at round ends (`split_rows`), and a round that changes
    nothing stalls only if it split nothing either. The node's steps are a list unless a
    `step_log` is given, which becomes them.
    """
    seed = build_seed(frame, mask, bins=bins, budget=budget)
    seed_sha = content_sha256(seed)
    groups = {owner: hull(points(seed["groups"][str(owner)])) for owner in mask}
    rows: dict[int, list[Row]] = {
        owner: [
            {
                "interval": row["interval"],
                "reference": row["reference"],
                "outer_domain": row["outer_domain"],
                "residual_polygons": row["residual_polygons"],
            }
            for row in seed["cells"][str(owner)]
        ]
        for owner in mask
    }
    initial = {
        "groups": {str(owner): encode(groups[owner]) for owner in mask},
        "cell_references": {
            str(owner): [row["reference"] for row in rows[owner]] for owner in mask
        },
    }
    steps: StepLog = [] if step_log is None else step_log
    closure: dict[str, Any] | None = None
    production = Production(seed, {})
    cores = CoreCache(core)
    terms = CollisionTerms()
    memo: PartnerMemo = {}
    previous: list[dict[str, Any]] | None = None
    plans: dict[int, Plan] = {owner: [(None, row) for row in rows[owner]] for owner in mask}
    history: dict[tuple[int, str, str], tuple[Q, int]] = {}
    for round_index in range(max_rounds):
        for owner in mask:
            if time.monotonic() >= budget.deadline:
                raise IncompleteError("producer wall ceiling")
            if stop_at is not None and steps and time.monotonic() >= stop_at:
                production.outcome = "time_cap"
                break
            if len(terms.pairs) > TERM_MEMO_PAIRS:
                terms.pairs.clear()
            step_index = len(steps)
            prior_hulls = {str(other): encode(groups[other]) for other in mask}
            covers: dict[str, list[dict[str, Any]]] = {}
            partners: dict[int, list[PartnerRow]] = {}
            if collision:
                for other in mask:
                    if other != owner:
                        given, live = partner_cover(frame, rows[other], cores, memo)
                        if live:
                            covers[str(other)], partners[other] = given, live
            produced = [
                produce_row(
                    frame,
                    node_id=node_id,
                    step_index=step_index,
                    row_index=index,
                    owner=owner,
                    predecessor=predecessor,
                    groups=groups,
                    partners=partners,
                    cores=cores,
                    terms=terms,
                    interval=interval,
                )
                for index, (interval, predecessor) in enumerate(plans[owner])
            ]
            planes = [plane for _, _, row_planes in produced for plane in row_planes]
            kernel = kernel_points(frame, planes)
            step: dict[str, Any] = {
                "index": step_index,
                "owner": owner,
                "allowed_half_angle": ["0", "1"],
                "prior_partner_pose_covers": covers,
                "prior_owned_hulls": prior_hulls,
                "rows": [row for row, _, _ in produced],
                "complete": True,
                "common_owned_kernel": [_encode_point(point) for point in kernel],
            }
            if any(accepted["residual_polygons"] for _, accepted, _ in produced) and (
                groups[owner] or kernel
            ):
                original = hull(groups[owner] + kernel)
                new_points, witnesses = compress(original)
                receipt: dict[str, Any] = {
                    "vertices": [_encode_point(point) for point in new_points],
                    "witnesses": witnesses,
                    "denominator": GRID,
                    "original_vertices": len(original),
                    "retained_vertices": len(new_points),
                }
                if hull_limit is not None and new_points == original:
                    keep = bounded_vertices(original, hull_limit)
                    new_points = [original[index] for index in keep]
                    receipt.update(
                        vertices=[_encode_point(point) for point in new_points],
                        witnesses=[witnesses[index] for index in keep],
                        retained_vertices=len(new_points),
                        mode="replace",
                    )
                    groups[owner] = hull(new_points)
                else:
                    groups[owner] = hull(groups[owner] + new_points)
                step["compression_source_hull"] = encode(original)
                step["inner_grid_compression"] = receipt
            rows[owner] = [accepted for _, accepted, _ in produced]
            plans[owner] = [(None, row) for row in rows[owner]]
            # A replaced row is never a partner again, so its memo entry only held memory.
            current = {id(row) for accepted_rows in rows.values() for row in accepted_rows}
            for key in [key for key in memo if key not in current]:
                del memo[key]
            steps.append(step)
            if progress is not None:
                event: dict[str, Any] = {
                    "round": round_index,
                    "step": step_index,
                    "owner": frame.cell_names[owner],
                    "live_rows": sum(1 for row in rows[owner] if row["residual_polygons"]),
                    "owned_hull_vertices": len(groups[owner]),
                }
                if split is not None:
                    event["rows"] = len(rows[owner])
                progress(event)
            closure = derived_closure(owner, step_index, groups, rows)
            if closure is not None:
                break
        extents = [owner_extents(frame, owner, rows[owner], groups[owner]) for owner in mask]
        record: dict[str, Any] = {"round": round_index, "steps": len(steps), "extents": extents}
        production.rounds.append(record)
        if production.outcome == "time_cap":
            break
        if closure is not None:
            production.outcome = "closed"
            break
        splits = 0
        if split is not None:
            splits = split_rows(
                frame, mask, rows=rows, plans=plans, history=history, policy=split
            )
            record["splits"] = splits
            record["planned_rows"] = sum(len(plans[owner]) for owner in mask)
        if extents == previous and not splits:
            production.outcome = "stalled"
            break
        previous = extents
    else:
        production.outcome = "round_cap"
    source = {"sha256": seed_sha}
    production.node = {
        "schema": "exact_generic_owned_hull_v1",
        "node_id": node_id,
        "parent": None,
        "constraints": [],
        "guard_source": None,
        "mask_index": None,
        "mask": list(mask),
        "U": str(frame.cap),
        "B": str(frame.scale),
        "source": source,
        "initial": initial,
        "steps": steps,
        "final_state": {
            "mask_index": None,
            "mask": list(mask),
            "U": str(frame.cap),
            "B": str(frame.scale),
            "constraints": [],
            "guard": {},
            "guard_source": None,
            "source": source,
            "world": seed["world"],
            "groups": {str(owner): encode(groups[owner]) for owner in mask},
            "cells": {str(owner): rows[owner] for owner in mask},
        },
        "contradiction": closure,
        "closed": closure is not None,
        "terminal": closure is not None,
        "mask_exclusion_proved": False,
        "global_optimality_proved": False,
    }
    return production
