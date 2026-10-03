"""Exact checker for a D4-symmetric capacity-one cover of the n17 centre box (H-266).

Frame. The container is `[0, U]^2` with `U = 1169/250`, so every contained unit square
has its centre in the closed centre box `B = [1/2, U - 1/2]^2`. Cells are closed convex
polygons with rational vertices inside `B`, stored as their strictly convex hull in
counterclockwise order from the lexicographically least vertex. D4 acts about
`(U/2, U/2)`; `r<k>` turns by `k` quarter turns and `f<k>` reflects `x` first.

Capacity. A cell is accepted by one of two arguments, both exact over the rationals.

* Diameter. Centres of interior-disjoint unit squares are at distance at least one
  (each square holds an open disc of radius 1/2 about its centre), so a closed cell of
  diameter below one holds at most one centre. The check is the largest squared vertex
  distance, strictly below one.
* Depth-width wall lemma. If a cell lies in `{x <= 1/2 + d}` and its `y`-extent is at
  most `w`, two contained interior-disjoint squares with centres in it would have a
  separating gap `g <= c d + s w - 1 - (c/2)(c + s - 1)` along a unit normal `(c, s)`
  with `c, s >= 0`. Capacity one follows when `G(d, w)`, the maximum of that bound over
  the closed quarter circle, is negative. With `tau = tan(theta/2)`,
  `c = (1 - tau^2)/(1 + tau^2)` and `s = 2 tau/(1 + tau^2)`, `(1 + tau^2)^2 G` is a
  quartic `P(tau)` on `[0, 1]`, and `P < 0` is proved by negative Bernstein coefficients
  on closed dyadic `tau` intervals, cross-checked by an exact Sturm root count. The
  other three walls follow by D4. A corner cell is a wall cell of its vertical wall with
  `d = w` equal to its side; the second wall it touches is not used. The lemma is the
  H259 wall lemma with depth and width decoupled; its proof is reviewed separately, and
  this module checks only its hypothesis.

Coverage. An exact vertical-slab sweep. The critical abscissae are every vertex, the
two sides of `B`, and every crossing of two edges of different cells. Between two
consecutive critical abscissae no edge ends and no two edges cross, so the order of all
edge lines is constant on the open slab and coverage of the vertical segment at its
midpoint decides coverage of the whole open slab; each critical vertical line is then
checked separately. A failure returns an uncovered rational witness point.

States. Existential closed-cell assignments, the H260 convention: a state is a set of
17 cells that can receive the 17 centres, each centre in a closed cell containing it.
Capacity one makes every choice of containing cells injective, so every packing at the
cap has at least one state, overlaps may give it several, and no seam priority is used.
The state set is all 17-subsets of the cells, which D4 preserves once the cell set is
D4-invariant; the orbit count is Burnside's average of exact cycle-polynomial fixed
counts.

Endpoint. The H256 layout (`check_n17_endpoint_feasibility._layout`) is evaluated in
exact interval arithmetic over the exp-238 root box, rounded outward to `10^-40`, and
embedded concentrically by `((U - S)/2, (U - S)/2)`. The slider family moves square 5
by `-a e_x`, square 11 by `-b v` and square 13 by `+z v` from the H256 centroid, and
square 6 anywhere in a declared box. A seam is a cell edge not on the boundary of `B`;
margins are Euclidean distances to the seams of the assigned cell, and are minimised
over the family by evaluating each linear margin at the vertices of its slider range.
The family is in one state when a single assignment of the 17 labels to distinct cells
holds every member with margin at least `1/1000`.

Unique state. Overlapping cells let one centre sit in two closed cells, and then the
family realises a second state that no sound engine can exclude. The state is unique
when, besides the common assignment, every family centre over the slider domain lies at
least `1/1000` outside every other cell. Distance outside is bounded below by separating
axes: for each edge line of the other cell the outward signed distance is linear, so its
least value over the family's hull is taken at a corner of an outward member rectangle.
"""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import time
from dataclasses import dataclass, replace
from fractions import Fraction as Q
from math import comb
from pathlib import Path
from typing import Any

from devtools.check_n17_endpoint_feasibility import Box, _layout

SCHEMA = "n17-capacity-one-cover/v1"
U = Q(1169, 250)
LO = Q(1, 2)
HI = U - LO
CENTRE = U / 2
TARGET = 17
SEAM_MARGIN = Q(1, 1000)
ORBIT_THRESHOLD = 135196  # H-266: N <= 25 and at most 135,196 D4 orbits
ROOT_ROUNDING = 10**40
SQRT_SCALE = 10**12
MAX_BERNSTEIN_DEPTH = 24
D4 = ("r0", "r1", "r2", "r3", "f0", "f1", "f2", "f3")
WALLS = ("W", "E", "S", "N")
REPO = Path(__file__).resolve().parents[2]
CERTIFICATE = (
    REPO / "packing/campaign/series/series-000-smoke-and-calibration/results/"
    "exp-238-n17-endpoint-feasibility/run-001/certificate.json"
)

Point = tuple[Q, Q]
BoxPoint = tuple[Box, Box]
Poly = list[Q]


# ---------------------------------------------------------------------------
# Design and cells
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Design:
    """A D4-symmetric ring-plus-Voronoi cover, all parameters exact.

    `tabs` pairs a representative interior site offset (from the centre) with extra hull
    points (offsets from the centre) for that site's cell; D4 carries both to the orbit.
    `clips` pairs a representative site offset with closed halfplanes `(a, b, c)`, kept as
    `a x + b y <= c` in offsets from the centre, cut from that cell after the tabs; D4
    turns the normal `(a, b)` with the site. With `per_wall` odd, `middle_width` and
    `middle_depth` set the middle side cell of each wall; the other side cells share the
    rest of the wall equally and keep `depth`.
    """

    name: str
    corner: Q
    depth: Q
    per_wall: int
    axis: Q | None
    diagonal: Q | None
    centre_site: bool
    tabs: tuple[tuple[Point, tuple[Point, ...]], ...]
    clips: tuple[tuple[Point, tuple[tuple[Q, Q, Q], ...]], ...] = ()
    middle_width: Q | None = None
    middle_depth: Q | None = None


@dataclass(frozen=True)
class Cell:
    name: str
    kind: str
    vertices: tuple[Point, ...]


# The lane F exploratory design, rationalised: corners 0.78, depth 0.911, three sides per
# wall, sites 0.516 (axis) and 0.5825 (diagonal, per coordinate).
VORONOI_24 = Design(
    name="ring-3-voronoi-8",
    corner=Q(39, 50),
    depth=Q(911, 1000),
    per_wall=3,
    axis=Q(129, 250),
    diagonal=Q(233, 400),
    centre_site=False,
    tabs=(),
)
# The seam fix: each axis cell is the hull of its Voronoi cell and four tab points. For
# the bottom axis cell they are (+-2/25, -197/200), which take square 13's slide down to
# depth 1169/500 - 197/200 - 1/2 = 853/1000, and (+-33/100, -19/25), whose D4 images
# hold square 11's slide along -v inside the west axis cell.
TABBED_24 = replace(
    VORONOI_24,
    name="ring-3-voronoi-8-tabbed",
    tabs=(
        (
            (Q(0), -Q(129, 250)),
            (
                (Q(2, 25), -Q(197, 200)),
                (-Q(2, 25), -Q(197, 200)),
                (Q(33, 100), -Q(19, 25)),
                (-Q(33, 100), -Q(19, 25)),
            ),
        ),
    ),
)
# A 25-cell variant for the recipe box B_W: the interior is the 3 x 3 grid of side 309/500
# (centre, axis and diagonal sites at 309/500), and the bottom cell's tabs
# (+-3/25, -26/25) take square 13's longer B_W slide. Any 25-cell cover has at least
# C(25, 17)/8 = 135,196.875 D4 orbits of states, above H-266's threshold of 135,196.
GRID_25 = Design(
    name="ring-3-grid-9-tabbed",
    corner=Q(39, 50),
    depth=Q(911, 1000),
    per_wall=3,
    axis=Q(309, 500),
    diagonal=Q(309, 500),
    centre_site=True,
    tabs=(((Q(0), -Q(309, 500)), ((Q(3, 25), -Q(26, 25)), (-Q(3, 25), -Q(26, 25)))),),
)
# The unique-state design. Square 13 slides across S1's top `y = 1.411`, and no convex,
# mirror-symmetric S1 can stay 1/1000 below the slide while the strip it gives up stays
# covered: (2083/1000, 13703/10000) is then at distance >= 1 from the box centre, which
# every axis cell holds, at distance >= 1 from its mirror in the diagonal, which the
# diagonal cell would also hold, and 0.803 from S0's start, past S0's admissible width.
# Square 13 moves to side S1 instead. S1 is deepened to 93/100 and narrowed to 257/375,
# inside the wall lemma's curve (w_max(93/100) > 0.6905), and the corners grow to 79/100
# so that S0 and S2 keep 529/750. Each axis cell is cut at S1's top (`y >= 143/100` for
# interior-S), which leaves square 13 outside it, and its tab points (+-17/50, -227/250)
# meet S1's top corners, so the cut strip stays covered. Each diagonal cell is cut below
# the chord through the axis tab (-19/25, -33/100) and (-3/10, -3/10), and its mirror,
# which takes square 11's slide out of interior-SW; the axis cells cover what it removes.
UNIQUE_24 = replace(
    TABBED_24,
    name="ring-3-voronoi-8-tabbed-unique",
    corner=Q(79, 100),
    middle_width=Q(257, 375),
    middle_depth=Q(93, 100),
    tabs=(
        (
            (Q(0), -Q(129, 250)),
            (
                (Q(33, 100), -Q(19, 25)),
                (-Q(33, 100), -Q(19, 25)),
                (Q(17, 50), -Q(227, 250)),
                (-Q(17, 50), -Q(227, 250)),
            ),
        ),
    ),
    clips=(
        ((Q(0), -Q(129, 250)), ((Q(0), Q(-1), Q(227, 250)),)),
        ((-Q(233, 400), -Q(233, 400)), ((Q(-3), Q(46), -Q(129, 10)),)),
    ),
)
DESIGNS = {design.name: design for design in (VORONOI_24, TABBED_24, UNIQUE_24, GRID_25)}


def cross(origin: Point, a: Point, b: Point) -> Q:
    return (a[0] - origin[0]) * (b[1] - origin[1]) - (a[1] - origin[1]) * (b[0] - origin[0])


def convex_hull(points: list[Point] | tuple[Point, ...]) -> tuple[Point, ...]:
    """Strictly convex counterclockwise hull, starting at the least vertex (canonical)."""
    ordered = sorted(set(points))
    if len(ordered) < 3:
        raise ValueError("a cell needs three affinely independent vertices")
    lower: list[Point] = []
    for point in ordered:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)
    upper: list[Point] = []
    for point in reversed(ordered):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    hull = tuple(lower[:-1] + upper[:-1])
    if len(hull) < 3:
        raise ValueError("a cell must have positive area")
    return hull


def d4_apply(action: str, point: Point) -> Point:
    """Apply one D4 element about the box centre: optional x-reflection, then turns."""
    x, y = point[0] - CENTRE, point[1] - CENTRE
    if action[0] == "f":
        x = -x
    for _ in range(int(action[1])):
        x, y = -y, x
    return x + CENTRE, y + CENTRE


def clip(polygon: list[Point], a: Q, b: Q, c: Q) -> list[Point]:
    """Keep the closed halfplane `a x + b y <= c` (Sutherland-Hodgman, exact)."""
    result: list[Point] = []
    for index, start in enumerate(polygon):
        end = polygon[(index + 1) % len(polygon)]
        f_start = a * start[0] + b * start[1] - c
        f_end = a * end[0] + b * end[1] - c
        if f_start <= 0:
            result.append(start)
        if f_start * f_end < 0:
            t = f_start / (f_start - f_end)
            result.append(
                (start[0] + t * (end[0] - start[0]), start[1] + t * (end[1] - start[1]))
            )
    return result


def voronoi_cell(site: Point, sites: list[Point], region: list[Point]) -> list[Point]:
    polygon = list(region)
    for other in sites:
        if other == site:
            continue
        a, b = other[0] - site[0], other[1] - site[1]
        c = (other[0] ** 2 + other[1] ** 2 - site[0] ** 2 - site[1] ** 2) / 2
        polygon = clip(polygon, a, b, c)
        if not polygon:
            break
    return polygon


def _rectangle(x0: Q, x1: Q, y0: Q, y1: Q) -> tuple[Point, ...]:
    return convex_hull([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])


def _compass(offset: Point) -> str:
    x, y = offset
    vertical = "S" if y < 0 else "N" if y > 0 else ""
    horizontal = "W" if x < 0 else "E" if x > 0 else ""
    return (vertical + horizontal) or "C"


def side_spans(design: Design) -> list[tuple[Q, Q, Q]]:
    """`(start, end, depth)` of each side cell along a wall, from the low corner."""
    corner, wall = design.corner, HI - LO - 2 * design.corner
    widths = [wall / design.per_wall] * design.per_wall
    depths = [design.depth] * design.per_wall
    if design.middle_width is not None or design.middle_depth is not None:
        if design.per_wall % 2 == 0:
            raise ValueError("a middle side cell needs an odd number of side cells")
        middle = design.per_wall // 2
        if design.middle_width is not None:
            rest = (wall - design.middle_width) / (design.per_wall - 1)
            widths = [rest] * design.per_wall
            widths[middle] = design.middle_width
        if design.middle_depth is not None:
            depths[middle] = design.middle_depth
    spans: list[tuple[Q, Q, Q]] = []
    start = LO + corner
    for width, depth in zip(widths, depths, strict=True):
        spans.append((start, start + width, depth))
        start += width
    return spans


def ring_cells(design: Design) -> list[Cell]:
    corner = design.corner
    cells = [
        Cell("corner-SW", "corner", _rectangle(LO, LO + corner, LO, LO + corner)),
        Cell("corner-SE", "corner", _rectangle(HI - corner, HI, LO, LO + corner)),
        Cell("corner-NW", "corner", _rectangle(LO, LO + corner, HI - corner, HI)),
        Cell("corner-NE", "corner", _rectangle(HI - corner, HI, HI - corner, HI)),
    ]
    for j, (a0, a1, depth) in enumerate(side_spans(design)):
        cells.extend(
            (
                Cell(f"side-S{j}", "side", _rectangle(a0, a1, LO, LO + depth)),
                Cell(f"side-N{j}", "side", _rectangle(a0, a1, HI - depth, HI)),
                Cell(f"side-W{j}", "side", _rectangle(LO, LO + depth, a0, a1)),
                Cell(f"side-E{j}", "side", _rectangle(HI - depth, HI, a0, a1)),
            )
        )
    return cells


def interior_sites(design: Design) -> list[Point]:
    representatives: list[Point] = []
    if design.axis is not None:
        representatives.append((Q(0), -design.axis))
    if design.diagonal is not None:
        representatives.append((-design.diagonal, -design.diagonal))
    if design.centre_site:
        representatives.append((Q(0), Q(0)))
    return sorted(
        {
            d4_apply(action, (CENTRE + ox, CENTRE + oy))
            for action in D4
            for ox, oy in representatives
        }
    )


def interior_cells(design: Design) -> list[Cell]:
    depth = design.depth
    region = [(LO + depth, LO + depth), (HI - depth, LO + depth), (HI - depth, HI - depth)]
    region.append((LO + depth, HI - depth))
    sites = interior_sites(design)
    extras: dict[Point, set[Point]] = {site: set() for site in sites}
    for (ox, oy), tabs in design.tabs:
        representative = (CENTRE + ox, CENTRE + oy)
        for action in D4:
            image = d4_apply(action, representative)
            if image not in extras:
                raise ValueError("a tab representative is not an interior site")
            extras[image].update(
                d4_apply(action, (CENTRE + tx, CENTRE + ty)) for tx, ty in tabs
            )
    cuts: dict[Point, set[tuple[Q, Q, Q]]] = {site: set() for site in sites}
    for (ox, oy), halfplanes in design.clips:
        representative = (CENTRE + ox, CENTRE + oy)
        for action in D4:
            image = d4_apply(action, representative)
            if image not in cuts:
                raise ValueError("a clip representative is not an interior site")
            for a, b, c in halfplanes:
                nx, ny = d4_apply(action, (CENTRE + a, CENTRE + b))
                cuts[image].add((nx - CENTRE, ny - CENTRE, c))
    cells: list[Cell] = []
    for site in sites:
        base = voronoi_cell(site, sites, region)
        polygon = list(convex_hull([*base, *extras[site]]))
        for a, b, c in sorted(cuts[site]):
            # a (x - C) + b (y - C) <= c, in absolute coordinates.
            polygon = clip(polygon, a, b, c + (a + b) * CENTRE)
        name = "interior-" + _compass((site[0] - CENTRE, site[1] - CENTRE))
        cells.append(Cell(name, "interior", convex_hull(polygon)))
    return cells


def build_cover(design: Design) -> list[Cell]:
    return ring_cells(design) + interior_cells(design)


# ---------------------------------------------------------------------------
# Capacity: exact diameter and the depth-width wall lemma
# ---------------------------------------------------------------------------


def squared_diameter(vertices: tuple[Point, ...]) -> Q:
    return max(
        (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 for p, q in itertools.combinations(vertices, 2)
    )


def _poly_add(a: Poly, b: Poly) -> Poly:
    size = max(len(a), len(b))
    return [
        (a[i] if i < len(a) else Q(0)) + (b[i] if i < len(b) else Q(0)) for i in range(size)
    ]


def _poly_scale(a: Poly, factor: Q) -> Poly:
    return [factor * value for value in a]


def _poly_mul(a: Poly, b: Poly) -> Poly:
    result = [Q(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            result[i + j] += x * y
    return result


def _poly_trim(a: Poly) -> Poly:
    result = list(a)
    while result and result[-1] == 0:
        result.pop()
    return result


def poly_value(a: Poly, x: Q) -> Q:
    value = Q(0)
    for coefficient in reversed(a):
        value = value * x + coefficient
    return value


def wall_polynomial(depth: Q, width: Q) -> Poly:
    """Coefficients, low degree first, of `P(tau) = (1 + tau^2)^2 G(c(tau), s(tau))`."""
    one_minus = [Q(1), Q(0), Q(-1)]  # c (1 + tau^2)
    two_tau = [Q(0), Q(2)]  # s (1 + tau^2)
    denominator = [Q(1), Q(0), Q(1)]  # 1 + tau^2
    # (c + s - 1)(1 + tau^2) = (1 - tau^2) + 2 tau - (1 + tau^2) = 2 tau - 2 tau^2.
    bracket = [Q(0), Q(2), Q(-2)]
    result = _poly_scale(_poly_mul(one_minus, denominator), depth)
    result = _poly_add(result, _poly_scale(_poly_mul(two_tau, denominator), width))
    result = _poly_add(result, _poly_scale(_poly_mul(denominator, denominator), Q(-1)))
    result = _poly_add(result, _poly_scale(_poly_mul(one_minus, bracket), Q(-1, 2)))
    return _poly_trim(result) or [Q(0)]


def wall_bound(depth: Q, width: Q, tau: Q) -> Q:
    """The wall-lemma bound `c d + s w - 1 - (c/2)(c + s - 1)` at `tau = tan(theta/2)`."""
    c = (1 - tau * tau) / (1 + tau * tau)
    s = 2 * tau / (1 + tau * tau)
    return c * depth + s * width - 1 - c * (c + s - 1) / 2


def to_bernstein(coefficients: Poly, degree: int) -> Poly:
    """Bernstein coefficients on [0, 1] of a polynomial given low degree first."""
    padded = coefficients + [Q(0)] * (degree + 1 - len(coefficients))
    return [
        sum(
            (Q(comb(j, k), comb(degree, k)) * padded[k] for k in range(j + 1)),
            start=Q(0),
        )
        for j in range(degree + 1)
    ]


def split_bernstein(coefficients: Poly) -> tuple[Poly, Poly]:
    """de Casteljau at the midpoint: Bernstein coefficients of both halves."""
    left, right = [coefficients[0]], [coefficients[-1]]
    current = list(coefficients)
    while len(current) > 1:
        current = [(current[i] + current[i + 1]) / 2 for i in range(len(current) - 1)]
        left.append(current[0])
        right.append(current[-1])
    return left, right[::-1]


def bernstein_negative(
    coefficients: Poly, max_depth: int = MAX_BERNSTEIN_DEPTH
) -> tuple[list[tuple[Q, Q, Q]], Q | None]:
    """Prove `P < 0` on [0, 1]: closed pieces with their largest Bernstein coefficient.

    Returns `(pieces, None)` on success, or `(pieces so far, tau)` with `P(tau) >= 0`
    exactly when an endpoint coefficient (a value of `P`) is nonnegative, or `tau = -1`
    if the depth budget ran out first.
    """
    degree = max(len(coefficients) - 1, 1)
    stack = [(Q(0), Q(1), to_bernstein(coefficients, degree), 0)]
    pieces: list[tuple[Q, Q, Q]] = []
    while stack:
        low, high, bernstein, level = stack.pop()
        largest = max(bernstein)
        if largest < 0:
            pieces.append((low, high, largest))
            continue
        if bernstein[0] >= 0:
            return pieces, low
        if bernstein[-1] >= 0:
            return pieces, high
        if level >= max_depth:
            return pieces, Q(-1)
        left, right = split_bernstein(bernstein)
        middle = (low + high) / 2
        stack.append((middle, high, right, level + 1))
        stack.append((low, middle, left, level + 1))
    pieces.sort()
    return pieces, None


def _poly_remainder(numerator: Poly, divisor: Poly) -> Poly:
    remainder = _poly_trim(numerator)
    divisor = _poly_trim(divisor)
    while len(remainder) >= len(divisor) and remainder:
        factor = remainder[-1] / divisor[-1]
        shift = len(remainder) - len(divisor)
        for i, value in enumerate(divisor):
            remainder[shift + i] -= factor * value
        remainder = _poly_trim(remainder)
    return remainder


def _sign_changes(sequence: list[Poly], x: Q) -> int:
    signs = [value for value in (poly_value(p, x) for p in sequence) if value != 0]
    return sum(1 for a, b in itertools.pairwise(signs) if (a < 0) != (b < 0))


def sturm_root_count(coefficients: Poly, low: Q, high: Q) -> int:
    """Distinct real roots in `(low, high]` by Sturm's theorem, exact."""
    first = _poly_trim(coefficients)
    derivative = _poly_trim([i * value for i, value in enumerate(first)][1:])
    sequence = [first]
    if derivative:
        sequence.append(derivative)
        while True:
            remainder = _poly_remainder(sequence[-2], sequence[-1])
            if not remainder:
                break
            sequence.append([-value for value in remainder])
    return _sign_changes(sequence, low) - _sign_changes(sequence, high)


def decimal(value: Q, digits: int = 6) -> str:
    """Round toward minus infinity to `digits` places (a lower bound, as text)."""
    scaled = math.floor(value * 10**digits)
    sign = "-" if scaled < 0 else ""
    whole, fraction = divmod(abs(scaled), 10**digits)
    return f"{sign}{whole}.{fraction:0{digits}d}"


def wall_lemma(depth: Q, width: Q) -> dict[str, Any]:
    """Exact proof or refusal that `max G(d, w) < 0` over the closed quarter circle."""
    polynomial = wall_polynomial(depth, width)
    pieces, failure = bernstein_negative(polynomial)
    sturm = sturm_root_count(polynomial, Q(0), Q(1))
    at_zero, at_one = poly_value(polynomial, Q(0)), poly_value(polynomial, Q(1))
    sturm_negative = sturm == 0 and at_zero < 0 and at_one < 0
    record: dict[str, Any] = {
        "depth": str(depth),
        "width": str(width),
        "polynomial_low_degree_first": [str(value) for value in polynomial],
        "P_at_tau_0": str(at_zero),
        "P_at_tau_1": str(at_one),
        "sturm_roots_in_0_1": sturm,
        "sturm_negative": sturm_negative,
    }
    contiguous = (
        bool(pieces)
        and pieces[0][0] == 0
        and pieces[-1][1] == 1
        and all(left[1] == right[0] for left, right in itertools.pairwise(pieces))
    )
    if failure is None and contiguous:
        # On a piece, G = P/(1 + tau^2)^2 <= (max Bernstein)/(1 + high^2)^2 < 0.
        upper = max(largest / (1 + high * high) ** 2 for _, high, largest in pieces)
        lower = max(
            wall_bound(depth, width, tau) for piece in pieces for tau in (piece[0], piece[1])
        )
        record.update(
            {
                "passed": sturm_negative,
                "bernstein_pieces": len(pieces),
                "tau_pieces": [[str(low), str(high)] for low, high, _ in pieces],
                "max_G_upper_bound": decimal(upper, 9),
                "max_G_lower_bound": decimal(lower, 9),
            }
        )
    else:
        record.update(
            {
                "passed": False,
                "refuting_tau": None if failure is None else str(failure),
                "G_at_refuting_tau": (
                    None
                    if failure is None or failure < 0
                    else str(wall_bound(depth, width, failure))
                ),
            }
        )
    return record


def wall_extents(vertices: tuple[Point, ...]) -> dict[str, tuple[Q, Q]]:
    """(depth, tangential width) of a cell against each wall, in the lemma's frame."""
    xs = [x for x, _ in vertices]
    ys = [y for _, y in vertices]
    x_extent, y_extent = max(xs) - min(xs), max(ys) - min(ys)
    return {
        "W": (max(xs) - LO, y_extent),
        "E": (HI - min(xs), y_extent),
        "S": (max(ys) - LO, x_extent),
        "N": (HI - min(ys), x_extent),
    }


def capacity_proof(cell: Cell, cache: dict[tuple[Q, Q], dict[str, Any]]) -> dict[str, Any]:
    """Diameter first; otherwise the wall lemma against the shallowest wall that works."""
    diameter2 = squared_diameter(cell.vertices)
    record: dict[str, Any] = {
        "cell": cell.name,
        "squared_diameter": str(diameter2),
        "diameter_lower_bound": decimal(_sqrt_lower(diameter2)),
    }
    if diameter2 < 1:
        record.update({"argument": "diameter", "passed": True})
        return record
    extents = wall_extents(cell.vertices)
    for wall in sorted(WALLS, key=lambda name: (extents[name][0], WALLS.index(name))):
        depth, width = extents[wall]
        if depth < 0 or depth >= 1 or width >= 1:
            continue
        key = (depth, width)
        if key not in cache:
            cache[key] = wall_lemma(depth, width)
        if cache[key]["passed"]:
            record.update(
                {
                    "argument": "wall-lemma",
                    "wall": wall,
                    "depth": str(depth),
                    "width": str(width),
                    "passed": True,
                }
            )
            return record
    record.update({"argument": None, "passed": False})
    return record


def _sqrt_upper(value: Q, scale: int = SQRT_SCALE) -> Q:
    root = math.isqrt(math.ceil(value * scale * scale))
    while Q(root, scale) ** 2 < value:
        root += 1
    return Q(root, scale)


def _sqrt_lower(value: Q, scale: int = SQRT_SCALE) -> Q:
    root = math.isqrt(math.floor(value * scale * scale))
    while root > 0 and Q(root, scale) ** 2 > value:
        root -= 1
    return Q(root, scale)


# ---------------------------------------------------------------------------
# Coverage of the centre box
# ---------------------------------------------------------------------------


def _edges(vertices: tuple[Point, ...]) -> list[tuple[Point, Point]]:
    return [(vertices[i], vertices[(i + 1) % len(vertices)]) for i in range(len(vertices))]


def _segment_crossing_x(a: tuple[Point, Point], b: tuple[Point, Point]) -> Q | None:
    (p, p2), (q, q2) = a, b
    r = (p2[0] - p[0], p2[1] - p[1])
    s = (q2[0] - q[0], q2[1] - q[1])
    denominator = r[0] * s[1] - r[1] * s[0]
    if denominator == 0:
        return None
    t = ((q[0] - p[0]) * s[1] - (q[1] - p[1]) * s[0]) / denominator
    u = ((q[0] - p[0]) * r[1] - (q[1] - p[1]) * r[0]) / denominator
    if 0 <= t <= 1 and 0 <= u <= 1:
        return p[0] + t * r[0]
    return None


def _vertical_interval(vertices: tuple[Point, ...], x: Q) -> tuple[Q, Q] | None:
    if not min(v[0] for v in vertices) <= x <= max(v[0] for v in vertices):
        return None
    ys: list[Q] = []
    for start, end in _edges(vertices):
        if start[0] == end[0]:
            if start[0] == x:
                ys.extend((start[1], end[1]))
        elif min(start[0], end[0]) <= x <= max(start[0], end[0]):
            ys.append(start[1] + (x - start[0]) * (end[1] - start[1]) / (end[0] - start[0]))
    return (min(ys), max(ys)) if ys else None


def _line_gap(cells: list[Cell], x: Q) -> Point | None:
    """An uncovered point of the segment `{x} x [LO, HI]`, or None if it is covered."""
    intervals = sorted(
        interval
        for interval in (_vertical_interval(cell.vertices, x) for cell in cells)
        if interval is not None
    )
    reached = LO
    for low, high in intervals:
        if low > reached:
            return x, (reached + low) / 2
        reached = max(reached, high)
    if reached < HI:
        return x, (reached + HI) / 2
    return None


def coverage(cells: list[Cell]) -> dict[str, Any]:
    """Exact closed coverage of the centre box by the union of the cells."""
    for cell in cells:
        if any(not (LO <= x <= HI and LO <= y <= HI) for x, y in cell.vertices):
            return {"passed": False, "reason": f"{cell.name} leaves the centre box"}
    critical: set[Q] = {LO, HI}
    critical.update(x for cell in cells for x, _ in cell.vertices)
    tagged = [
        (
            index,
            edge,
            min(edge[0][0], edge[1][0]),
            max(edge[0][0], edge[1][0]),
            min(edge[0][1], edge[1][1]),
            max(edge[0][1], edge[1][1]),
        )
        for index, cell in enumerate(cells)
        for edge in _edges(cell.vertices)
    ]
    for first, second in itertools.combinations(tagged, 2):
        if first[0] == second[0]:
            continue
        if first[3] < second[2] or second[3] < first[2]:
            continue
        if first[5] < second[4] or second[5] < first[4]:
            continue
        crossing = _segment_crossing_x(first[1], second[1])
        if crossing is not None:
            critical.add(crossing)
    abscissae = sorted(x for x in critical if LO <= x <= HI)
    probes = abscissae + [(a + b) / 2 for a, b in itertools.pairwise(abscissae)]
    for x in probes:
        gap = _line_gap(cells, x)
        if gap is not None:
            return {
                "passed": False,
                "reason": "uncovered point",
                "witness": [str(gap[0]), str(gap[1])],
                "critical_abscissae": len(abscissae),
            }
    return {
        "passed": True,
        "critical_abscissae": len(abscissae),
        "vertical_lines_checked": len(probes),
    }


# ---------------------------------------------------------------------------
# D4 action and the Burnside count
# ---------------------------------------------------------------------------


def d4_permutations(cells: list[Cell]) -> dict[str, list[int]] | None:
    """The permutation of cell indices induced by each D4 element, or None if not closed."""
    index = {cell.vertices: k for k, cell in enumerate(cells)}
    if len(index) != len(cells):
        return None
    permutations: dict[str, list[int]] = {}
    for action in D4:
        images: list[int] = []
        for cell in cells:
            image = convex_hull([d4_apply(action, vertex) for vertex in cell.vertices])
            if image not in index:
                return None
            images.append(index[image])
        permutations[action] = images
    return permutations


def cycle_lengths(permutation: list[int]) -> list[int]:
    seen: set[int] = set()
    lengths: list[int] = []
    for start in range(len(permutation)):
        length, current = 0, start
        while current not in seen:
            seen.add(current)
            current = permutation[current]
            length += 1
        if length:
            lengths.append(length)
    return lengths


def fixed_subsets(permutation: list[int], size: int) -> int:
    """Subsets of the given size fixed by the permutation: unions of whole cycles."""
    coefficients = [1] + [0] * size
    for length in cycle_lengths(permutation):
        for degree in range(size, length - 1, -1):
            coefficients[degree] += coefficients[degree - length]
    return coefficients[size]


def burnside(permutations: dict[str, list[int]], size: int = TARGET) -> dict[str, Any]:
    fixed = {
        action: fixed_subsets(permutation, size) for action, permutation in permutations.items()
    }
    total = sum(fixed.values())
    if total % len(D4):
        raise ValueError("Burnside sum is not divisible by eight")
    cells = len(next(iter(permutations.values())))
    return {
        "cells": cells,
        "states": comb(cells, size),
        "fixed_counts": fixed,
        "cycle_profiles": {
            action: sorted(cycle_lengths(permutation))
            for action, permutation in permutations.items()
        },
        "fixed_sum": total,
        "orbits": total // len(D4),
    }


# ---------------------------------------------------------------------------
# The H256 endpoint family
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SliderDomain:
    """Slider ranges from the H256 centroid; square 6 in a box when `free_six`."""

    name: str
    a: tuple[Q, ...]
    b: tuple[Q, ...]
    z: tuple[Q, ...]
    free_six: bool


ENDPOINT = SliderDomain("h256-centroid", (Q(0),), (Q(0),), (Q(0),), free_six=False)
# The H256 triangle and the route review's slides, rounded outward: a <= T/s, b <= T,
# z in [-2T/3, T/3]. `domain_containment` proves the containment over the root box.
TRIANGLE = SliderDomain(
    "h256-triangle-box",
    (Q(0), Q(3, 25)),
    (Q(0), Q(3, 40)),
    (Q(-1, 20), Q(1, 40)),
    free_six=True,
)
# The local-theorem recipe's declared box B_W.
RECIPE_BOX = SliderDomain(
    "recipe-B_W",
    (Q(0), Q(1, 4)),
    (Q(0), Q(1, 12)),
    (Q(-1, 8), Q(1, 16)),
    free_six=True,
)
# Square 6, free in the family: its centre in [R - 1/5, R] x [1/2, 3/4] before embedding,
# which holds the triangle's range [R - T/s, R] and a turn of 0.18 rad, whose support
# (cos + sin)/2 < 0.582 bounds the centre height on the wall.
SIX_BOX_WIDTH = Q(1, 5)
SIX_BOX_HEIGHT = (Q(1, 2), Q(3, 4))


def load_root_box(path: Path) -> tuple[Box, Box, dict[str, Any]]:
    """The exp-238 root box `m +- eta`, rounded outward to a 10^-40 grid."""
    raw = path.read_bytes()
    document = json.loads(raw)
    box = document["geometry"]["box"]
    midpoint = [Q(value) for value in box["midpoint"]]
    radii = [Q(value) for value in box["inclusion_bounds"]]
    rounded = [
        Box(
            Q(math.floor((m - r) * ROOT_ROUNDING), ROOT_ROUNDING),
            Q(math.ceil((m + r) * ROOT_ROUNDING), ROOT_ROUNDING),
        )
        for m, r in zip(midpoint, radii, strict=True)
    ]
    provenance = {
        "certificate": str(path.relative_to(REPO)) if path.is_relative_to(REPO) else str(path),
        "certificate_sha256": hashlib.sha256(raw).hexdigest(),
        "criterion_passed": document.get("criterion_passed") is True,
        "t_box": [str(rounded[0].lo), str(rounded[0].hi)],
        "b_box": [str(rounded[1].lo), str(rounded[1].hi)],
    }
    return rounded[0], rounded[1], provenance


@dataclass(frozen=True)
class Endpoint:
    centres: tuple[BoxPoint, ...]
    v: BoxPoint
    shift: Box
    aux: dict[str, Any]


def endpoint(t: Box, b: Box) -> Endpoint:
    side, aux, centres = _layout(t, b, Box.point(Q(1, 2)))
    shift = (Box.point(U) - side) * Q(1, 2)
    return Endpoint(
        centres=tuple((x + shift, y + shift) for x, y in centres),
        v=(aux["v"][0], aux["v"][1]),
        shift=shift,
        aux=aux,
    )


def family_points(point: Endpoint, label: int, domain: SliderDomain) -> list[BoxPoint]:
    x, y = point.centres[label - 1]
    vx, vy = point.v
    if label == 5:
        return [(x - a, y) for a in domain.a]
    if label == 11:
        return [(x - vx * b, y - vy * b) for b in domain.b]
    if label == 13:
        return [(x + vx * z, y + vy * z) for z in domain.z]
    if label == 6 and domain.free_six:
        right = point.aux["R"] + point.shift
        xs = (right - SIX_BOX_WIDTH, right)
        ys = tuple(point.shift + height for height in SIX_BOX_HEIGHT)
        return [(px, py) for px in xs for py in ys]
    return [(x, y)]


def _is_box_edge(start: Point, end: Point) -> bool:
    return any((start[axis] == end[axis] == bound) for axis in (0, 1) for bound in (LO, HI))


def outward(box: Box, grid: int = ROOT_ROUNDING) -> tuple[Q, Q]:
    """The interval rounded outward to a `1/grid` lattice, as plain bounds."""
    return Q(math.floor(box.lo * grid), grid), Q(math.ceil(box.hi * grid), grid)


def seam_margin(cell: Cell, point: tuple[tuple[Q, Q], tuple[Q, Q]]) -> tuple[Q, bool]:
    """A lower bound on the distance to the cell's seams, and whether it is >= 1/1000.

    `point` is a rectangle `([x_lo, x_hi], [y_lo, y_hi])`; each signed edge distance is
    linear, so its least value is taken at the corner its coefficients select. Negative
    values mean the point is not proved inside the cell.
    """
    (x_lo, x_hi), (y_lo, y_hi) = point
    least: Q | None = None
    clear = True
    for start, end in _edges(cell.vertices):
        ex, ey = end[0] - start[0], end[1] - start[1]
        # signed = ex (y - y_s) - ey (x - x_s), minimised over the rectangle.
        low = ex * ((y_lo if ex >= 0 else y_hi) - start[1]) - ey * (
            (x_hi if ey >= 0 else x_lo) - start[0]
        )
        length2 = ex * ex + ey * ey
        if low < 0:
            value = low / _sqrt_lower(length2)
            if least is None or value < least:
                least = value
            clear = False
            continue
        if _is_box_edge(start, end):
            continue
        clear = clear and low * low >= SEAM_MARGIN**2 * length2
        bound = low / _sqrt_upper(length2)
        if least is None or bound < least:
            least = bound
    return (least if least is not None else Q(10)), clear


def _matching(candidates: dict[int, list[int]], labels: list[int]) -> dict[int, int] | None:
    owner: dict[int, int] = {}

    def augment(label: int, visited: set[int]) -> bool:
        for cell in candidates[label]:
            if cell in visited:
                continue
            visited.add(cell)
            if cell not in owner or augment(owner[cell], visited):
                owner[cell] = label
                return True
        return False

    for label in labels:
        if not augment(label, set()):
            return None
    return {label: cell for cell, label in owner.items()}


def family_state(cells: list[Cell], point: Endpoint, domain: SliderDomain) -> dict[str, Any]:
    """One assignment holding every family member with margin >= 1/1000, if any."""
    labels = list(range(1, TARGET + 1))
    margins: dict[int, dict[int, tuple[Q, bool]]] = {}
    for label in labels:
        members = [(outward(x), outward(y)) for x, y in family_points(point, label, domain)]
        margins[label] = {}
        for index, cell in enumerate(cells):
            xs = [vertex[0] for vertex in cell.vertices]
            ys = [vertex[1] for vertex in cell.vertices]
            if any(
                x[1] < min(xs) or x[0] > max(xs) or y[1] < min(ys) or y[0] > max(ys)
                for x, y in members
            ):
                continue  # some member is exactly outside the cell's bounding box
            values = [seam_margin(cell, member) for member in members]
            least = min(value for value, _ in values)
            if least >= 0:
                margins[label][index] = (least, all(clear for _, clear in values))
    thresholds = sorted(
        {value for row in margins.values() for value, clear in row.values() if clear},
        reverse=True,
    )
    assignment: dict[int, int] | None = None
    for threshold in thresholds:
        candidates = {
            label: [
                index
                for index, (value, clear) in margins[label].items()
                if clear and value >= threshold
            ]
            for label in labels
        }
        assignment = _matching(candidates, labels)
        if assignment is not None:
            break
    squares = []
    for label in labels:
        containing = {
            cells[index].name: decimal(value) for index, (value, _) in margins[label].items()
        }
        entry: dict[str, Any] = {"label": label, "cells_with_nonnegative_margin": containing}
        if assignment is not None:
            chosen = assignment[label]
            entry["cell"] = cells[chosen].name
            entry["margin_lower_bound"] = decimal(margins[label][chosen][0])
        squares.append(entry)
    record: dict[str, Any] = {
        "domain": domain.name,
        "sliders": {
            "a": [str(value) for value in domain.a],
            "b": [str(value) for value in domain.b],
            "z": [str(value) for value in domain.z],
            "square_6": (
                {
                    "x": f"[R - {SIX_BOX_WIDTH}, R] + shift",
                    "y": [str(value) for value in SIX_BOX_HEIGHT],
                }
                if domain.free_six
                else "H256 centroid"
            ),
        },
        "one_state": assignment is not None,
        "squares": squares,
    }
    if assignment is not None:
        least_label = min(labels, key=lambda label: margins[label][assignment[label]][0])
        record["least_margin_lower_bound"] = decimal(
            margins[least_label][assignment[least_label]][0]
        )
        record["least_margin_square"] = least_label
        record["state"] = sorted(cells[index].name for index in assignment.values())
    else:
        record["unassignable"] = [
            label for label in labels if not any(clear for _, clear in margins[label].values())
        ]
    return record


def outside_distance(
    cell: Cell, members: list[tuple[tuple[Q, Q], tuple[Q, Q]]]
) -> tuple[Q, bool]:
    """A lower bound on the distance from the members' hull to the cell, and whether >= 1/1000.

    Each member is a rectangle `([x_lo, x_hi], [y_lo, y_hi])`. For every edge line of the
    cell the outward signed distance is linear, so its least value over the hull of the
    rectangles is taken at a rectangle corner; the cell lies on the inner side, so the
    largest of these least values bounds the distance from below (separating axes). A
    negative value means no edge line separates the family from the cell.
    """
    best: Q | None = None
    clear = False
    for start, end in _edges(cell.vertices):
        ex, ey = end[0] - start[0], end[1] - start[1]
        # outward = ey (x - x_s) - ex (y - y_s), minimised over every member rectangle.
        low = min(
            ey * ((x_lo if ey >= 0 else x_hi) - start[0])
            - ex * ((y_hi if ex >= 0 else y_lo) - start[1])
            for (x_lo, x_hi), (y_lo, y_hi) in members
        )
        length2 = ex * ex + ey * ey
        if low > 0:
            clear = clear or low * low >= SEAM_MARGIN**2 * length2
            bound = low / _sqrt_upper(length2)
        else:
            bound = low / _sqrt_lower(length2)
        if best is None or bound > best:
            best = bound
    assert best is not None
    return best, clear


def unique_state(
    cells: list[Cell], point: Endpoint, domain: SliderDomain, family: dict[str, Any]
) -> dict[str, Any]:
    """Whether the family's state is unique: each centre at least 1/1000 outside every cell
    other than its assigned one, over the whole slider domain.

    `family` is the `family_state` record for the same cells and domain; without a common
    state there is nothing to make unique. Per square, the least lower bound on the
    distance outside any other cell is reported with that cell.
    """
    if not family["one_state"]:
        return {"domain": domain.name, "unique": False, "reason": "no common state"}
    assigned = {entry["label"]: entry["cell"] for entry in family["squares"]}
    squares: list[dict[str, Any]] = []
    second: list[int] = []
    least: tuple[Q, int] | None = None
    for label in range(1, TARGET + 1):
        members = [(outward(x), outward(y)) for x, y in family_points(point, label, domain)]
        nearest: tuple[Q, str] | None = None
        clear = True
        for cell in cells:
            if cell.name == assigned[label]:
                continue
            distance, cell_clear = outside_distance(cell, members)
            clear = clear and cell_clear
            if nearest is None or distance < nearest[0]:
                nearest = (distance, cell.name)
        assert nearest is not None
        if not clear:
            second.append(label)
        if least is None or nearest[0] < least[0]:
            least = (nearest[0], label)
        squares.append(
            {
                "label": label,
                "cell": assigned[label],
                "nearest_other_cell": nearest[1],
                "outside_lower_bound": decimal(nearest[0]),
                "clear": clear,
            }
        )
    assert least is not None
    return {
        "domain": domain.name,
        "unique": not second,
        "squares_in_a_second_cell": second,
        "least_outside_lower_bound": decimal(least[0]),
        "least_outside_square": least[1],
        "squares": squares,
    }


def domain_containment(point: Endpoint) -> dict[str, Any]:
    """Prove the triangle box holds the H256 slides: T/s, T, 2T/3, T/3 against its ends."""
    slack, sine = point.aux["T"], point.aux["s"]
    reach = slack / sine
    checks = {
        "a: T/s <= 3/25": reach.hi <= TRIANGLE.a[-1],
        "b: T <= 3/40": slack.hi <= TRIANGLE.b[-1],
        "z: 2T/3 <= 1/20": (slack * Q(2, 3)).hi <= -TRIANGLE.z[0],
        "z: T/3 <= 1/40": (slack * Q(1, 3)).hi <= TRIANGLE.z[-1],
        "square 6: T/s <= 1/5": reach.hi <= SIX_BOX_WIDTH,
    }
    return {
        "T": [decimal(slack.lo, 9), decimal(slack.hi + Q(1, 10**9), 9)],
        "T_over_s": [decimal(reach.lo, 9), decimal(reach.hi + Q(1, 10**9), 9)],
        "checks": checks,
        "passed": all(checks.values()),
    }


# ---------------------------------------------------------------------------
# Controls
# ---------------------------------------------------------------------------


def falsifier_control() -> dict[str, Any]:
    """The H259 pair: two contained interior-disjoint squares in one H259 central cell."""
    a = Q(919, 1250)
    cell = Cell(
        "h259-centre", "interior", _rectangle(LO + 2 * a, LO + 3 * a, LO + 2 * a, LO + 3 * a)
    )
    u = (Q(21, 29), Q(20, 29))
    offset = Q(101, 200)
    centres = [
        (CENTRE + sign * offset * u[0], CENTRE + sign * offset * u[1]) for sign in (1, -1)
    ]
    support = (u[0] + u[1]) / 2  # axis support of a square with frame u, v
    gap = 2 * offset - 1  # directed separation along u minus two half-widths
    inside = all(
        LO + 2 * a <= x <= LO + 3 * a and LO + 2 * a <= y <= LO + 3 * a for x, y in centres
    )
    contained = all(
        support <= x <= U - support and support <= y <= U - support for x, y in centres
    )
    box_cell = Cell(
        "falsifier-pair-box",
        "interior",
        _rectangle(
            min(x for x, _ in centres),
            max(x for x, _ in centres),
            min(y for _, y in centres),
            max(y for _, y in centres),
        ),
    )
    cache: dict[tuple[Q, Q], dict[str, Any]] = {}
    refused = [capacity_proof(cell, cache), capacity_proof(box_cell, cache)]
    return {
        "pair_centres": [[str(x), str(y)] for x, y in centres],
        "pair_gap_along_u": str(gap),
        "pair_in_h259_cell": inside,
        "pair_contained": contained,
        "capacity_refusals": refused,
        "passed": gap > 0 and inside and contained and not any(r["passed"] for r in refused),
    }


def run_controls(design: Design, cells: list[Cell]) -> dict[str, Any]:
    cache: dict[tuple[Q, Q], dict[str, Any]] = {}
    unit = Cell(
        "unit-diameter",
        "interior",
        _rectangle(CENTRE - Q(3, 10), CENTRE + Q(3, 10), CENTRE - Q(2, 5), CENTRE + Q(2, 5)),
    )
    unit_record = capacity_proof(unit, cache)
    wide_corner = wall_lemma(Q(4, 5), Q(4, 5))
    wide_side = wall_lemma(design.depth, Q(3, 4))
    holed = coverage(cells[:-1])
    shallow = coverage(
        ring_cells(replace(design, depth=design.depth - Q(1, 1000)))
        + [cell for cell in cells if cell.kind == "interior"]
    )
    broken = list(cells)
    victim = broken[-1]
    broken[-1] = Cell(
        victim.name, victim.kind, convex_hull([*victim.vertices, (CENTRE, LO + Q(1, 3))])
    )
    asymmetric = d4_permutations(broken) is None
    falsifier = falsifier_control()
    return {
        "h259_falsifier": falsifier,
        "unit_diameter_cell": {
            "squared_diameter": unit_record["squared_diameter"],
            "refused": not unit_record["passed"],
        },
        "wall_lemma_refusals": {
            "corner_4/5": {
                "refused": not wide_corner["passed"],
                "refuting_tau": wide_corner.get("refuting_tau"),
            },
            "side_depth_3/4": {
                "refused": not wide_side["passed"],
                "refuting_tau": wide_side.get("refuting_tau"),
            },
        },
        "hole_without_last_cell": {
            "refused": not holed["passed"],
            "witness": holed.get("witness"),
        },
        "ring_gap_depth_minus_1/1000": {
            "refused": not shallow["passed"],
            "witness": shallow.get("witness"),
        },
        "asymmetric_cell_refused": asymmetric,
        "passed": (
            falsifier["passed"]
            and not unit_record["passed"]
            and not wide_corner["passed"]
            and not wide_side["passed"]
            and not holed["passed"]
            and not shallow["passed"]
            and asymmetric
        ),
    }


# ---------------------------------------------------------------------------
# Receipt
# ---------------------------------------------------------------------------


def cell_record(cell: Cell) -> dict[str, Any]:
    return {
        "name": cell.name,
        "kind": cell.kind,
        "vertices": [[str(x), str(y)] for x, y in cell.vertices],
    }


def check_design(
    design: Design, certificate: Path = CERTIFICATE, *, controls: bool = True
) -> dict[str, Any]:
    """Every exact check of H-266 for one design, as a JSON-ready receipt."""
    clock = time.perf_counter()
    cells = build_cover(design)
    cache: dict[tuple[Q, Q], dict[str, Any]] = {}
    capacities = [capacity_proof(cell, cache) for cell in cells]
    covered = coverage(cells)
    permutations = d4_permutations(cells)
    census = burnside(permutations) if permutations is not None else None
    t, b, provenance = load_root_box(certificate)
    point = endpoint(t, b)
    family = {
        domain.name: family_state(cells, point, domain)
        for domain in (ENDPOINT, TRIANGLE, RECIPE_BOX)
    }
    uniqueness = {
        domain.name: unique_state(cells, point, domain, family[domain.name])
        for domain in (ENDPOINT, TRIANGLE, RECIPE_BOX)
    }
    containment = domain_containment(point)
    receipt: dict[str, Any] = {
        "schema": SCHEMA,
        "design": {
            "name": design.name,
            "cap": str(U),
            "centre_box": [str(LO), str(HI)],
            "corner": str(design.corner),
            "depth": str(design.depth),
            "per_wall": design.per_wall,
            "side_width": str(side_spans(design)[0][1] - side_spans(design)[0][0]),
            "side_spans": [
                {"start": str(a0), "end": str(a1), "depth": str(depth)}
                for a0, a1, depth in side_spans(design)
            ],
            "middle_width": None if design.middle_width is None else str(design.middle_width),
            "middle_depth": None if design.middle_depth is None else str(design.middle_depth),
            "axis_site": None if design.axis is None else str(design.axis),
            "diagonal_site": None if design.diagonal is None else str(design.diagonal),
            "centre_site": design.centre_site,
            "tabs": [
                {
                    "site_offset": [str(x) for x in site],
                    "points": [[str(x), str(y)] for x, y in tabs],
                }
                for site, tabs in design.tabs
            ],
            "clips": [
                {
                    "site_offset": [str(x) for x in site],
                    "halfplanes_a_b_c": [[str(v) for v in plane] for plane in planes],
                }
                for site, planes in design.clips
            ],
        },
        "cells": [cell_record(cell) for cell in cells],
        "capacity": {
            "cells": capacities,
            "wall_lemma_proofs": list(cache.values()),
            "passed": all(record["passed"] for record in capacities),
            "corner_rule": (
                "a corner cell is a wall cell of its vertical wall (W or E) with depth and "
                "width equal to its side; the horizontal wall is not used"
            ),
        },
        "coverage": covered,
        "d4": {
            "invariant": permutations is not None,
            "permutations": permutations,
        },
        "census": census,
        "state_convention": (
            "existential closed-cell assignments (H260): a state is a 17-subset of cells "
            "that receives the 17 centres, each in a closed cell containing it; capacity "
            "one makes every such choice injective, overlaps may give a packing several "
            "states, and no seam priority is used"
        ),
        "endpoint": {
            "root": provenance,
            "slider_containment": containment,
            "family": family,
            "unique_state": uniqueness,
        },
        "seam_margin_required": str(SEAM_MARGIN),
    }
    if controls:
        receipt["controls"] = run_controls(design, cells)
    passed = (
        receipt["capacity"]["passed"]
        and covered["passed"]
        and permutations is not None
        and containment["passed"]
        and family[TRIANGLE.name]["one_state"]
        and uniqueness[TRIANGLE.name]["unique"]
        and provenance["criterion_passed"]
        and len(cells) <= 25
        and census is not None
        and census["orbits"] <= ORBIT_THRESHOLD
        and (not controls or receipt["controls"]["passed"])
    )
    receipt["criterion"] = {
        "cells": len(cells),
        "capacity": receipt["capacity"]["passed"],
        "coverage": covered["passed"],
        "d4_invariant": permutations is not None,
        "orbits": None if census is None else census["orbits"],
        "orbit_threshold": ORBIT_THRESHOLD,
        "root_certificate_passed": provenance["criterion_passed"],
        "controls": None if not controls else receipt["controls"]["passed"],
        "family_one_state_triangle": family[TRIANGLE.name]["one_state"],
        "family_one_state_recipe_box": family[RECIPE_BOX.name]["one_state"],
        "family_unique_state_triangle": uniqueness[TRIANGLE.name]["unique"],
        "passed": passed,
    }
    receipt["module_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    receipt["seconds"] = round(time.perf_counter() - clock, 3)
    return receipt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("--design", choices=sorted(DESIGNS), default=UNIQUE_24.name)
    _ = parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    _ = parser.add_argument("--output", type=Path, help="write the receipt here as well")
    arguments = parser.parse_args(argv)
    receipt = check_design(DESIGNS[arguments.design], arguments.certificate)
    text = json.dumps(receipt, indent=1, sort_keys=True)
    if arguments.output is not None:
        _ = arguments.output.write_text(text + "\n", encoding="utf-8")
    summary = {key: receipt[key] for key in ("schema", "criterion", "module_sha256", "seconds")}
    print(json.dumps(summary, indent=1, sort_keys=True))
    return 0 if receipt["criterion"]["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
