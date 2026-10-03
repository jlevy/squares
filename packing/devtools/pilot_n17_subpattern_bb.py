"""Pilot: a branch-and-bound certifier of n17 sub-pattern infeasibility (lane P2, H-267).

A pilot, not a certificate of record. It is the planned independent cross-check of the
ownership-induction kernel (`sqpack.hull_kernel`, `check_n17_subpattern`), and it shares
no code with that kernel or with the float selector (`select_n17_sub_patterns`) apart from
the exact cell polygons of `check_n17_capacity_one_cover`.

Question. On a capacity-one cover of the n17 centre box, a sub-pattern `G` of `k` closed
cells is forbidden when `k` unit squares, centre `i` in cell `i`, any angles, all inside
`[0, U]^2`, cannot have pairwise disjoint interiors. A run either proves that by
exhausting the poses `(x_i, y_i, theta_i)`, angles modulo pi/2, or says it could not.

Pair condition. For squares at angles `theta_i`, `theta_j` and `d = c_j - c_i`, the
separating axis theorem over the eight edge normals reads: the interiors are disjoint iff
`n . d >= g` for one normal `n` at angle `theta_i + k pi/2` or `theta_j + k pi/2`, where
`g = 1/2 + h(theta_j - theta_i)` and `h(a) = (|cos a| + |sin a|)/2` is a unit square's
half-width across a direction at angle `a` to its edges. Both squares' half-widths sum to
`g` on all eight axes, so the eight conditions differ only in the normal.

Method, and why. The selector's best pose for pattern A is a near-lattice: six squares
tilted about 50 degrees, neighbours about one apart along a shared normal, and a worst
penetration of 0.0149 that no single pair carries. The obstruction is collective. A pure
interval branch and bound on all `3k` coordinates sees one constraint at a time, so it
must cut every centre box down to the size of that margin; in 18 or 21 dimensions that is
hopeless. So the tool branches on the `k` angles only, and on each angle box decides the
centres by one linear program in which every pair constraint, every cell and every wall
act together:

* Angles. Each angle lives in one period `[theta0, theta0 + pi/2]`, closed (a superset of
  the half-open period). `theta0 = 0.4` by default, so both axis-aligned squares (at
  pi/2) and the 45-to-50-degree lattices sit inside the period, away from its seam; a
  regime cut by the seam is searched twice per square, measured at a factor of two on A.
* Walls. Containment is `h(theta) <= x, y <= U - h(theta)`; `h` is concave between
  multiples of pi/2, so its least value on an angle interval is at an endpoint or is 1/2.
* Options and windows. For a pair, an *option* is an interval of normal angles. The
  eight normal intervals of a node, intersected (modulo 2 pi) with the pair's window, are
  filtered and overlapping ones merged into their hull, sound because "some normal in the
  hull separates" contains each merged option. Several options are a disjunction the
  search may branch on, giving each child its option as the pair's window; a window is
  inherited, so a decided pair stays decided as the angles shrink.
* Three half-planes per option. Every `d` separated along some `phi` in `[a, b]` (width
  below pi/2) has `n(a) . d >= g`, `n(b) . d >= g` or `n(m) . d >= g cos x`, `x = max(m -
  a, b - m)`: the complement of the three is a polygon whose part in the sector lies under
  the chord, inside the disc of radius `g`, and whose part outside meets the nearer end
  normal below `g`. The loss is second order (`g x^2/2`). `g` is replaced by a lower
  bound `g_lo` over both angle intervals, and each float normal is charged its distance
  to the enclosed one. A wider option falls back to one row about its midpoint, with
  loss `2 tau (S + tau D)` from `n(phi) - n(m) = 2 sin((phi - m)/2) n_perp((phi + m)/2)`.
* Hull cuts. `d = c_j - c_i` is two-dimensional, so the union of a pair's surviving
  half-planes within its d-box has a convex hull computed directly. Its facets off the
  box are the pair's rows `u . d >= v`, with `v` made valid by a rigorous Lagrangian lower
  bound of `u . d` over each half-plane meet the box. This replaces most branching on
  options: on pattern A it cut pair branches by a factor of six and raised the closed
  share of the tree twenty-fivefold in the same time.
* LP, Farkas and bound tightening. One LP holds every cell row, every hull cut and the
  box. `min t : A z - t <= b` with `t* > 0` and multipliers passing the outward-rounded
  dual check below closes the node. Otherwise each centre coordinate is minimised and
  maximised over the same rows (warm re-solves), each bound made valid by the same dual
  check with the coordinate as the cost, the boxes are clipped to the cells again, and
  the node is re-relaxed while a box shrinks by 5 percent; children inherit the boxes.
* Taylor option (`--taylor`, off by default; interval runs write the same bytes). The
  interval rows enter the gap `g = 1/2 + h(theta_j - theta_i)` and the walls' `h(theta)`
  through their least values over the angle box, a first-order loss wherever `h` slopes
  (corner-to-edge contacts, tilted wall squares). With the option the angle offsets
  `t_s = theta_s - c_s` about the box centres become LP columns, and each support gets
  lines through the centre: `h` is the largest of the four sinusoids
  `f = (s1 cos + s2 sin)/2`, each with `|f''| <= sqrt 2/2`, so
  `h(c + t) >= f(c) + f'(c) t - (sqrt 2/4) t^2` for every sign pair, and the two lines
  either side of a kink keep its V. Every plane also reads `nbar . d >= c g - o` at the
  pose's own gap, so a pair gets cuts `u . d - w (t_j - t_i) >= v`, with `u` an interval
  hull facet, `w` a secant slope and `v` a rigorous three-variable Lagrangian bound over
  every plane; a square gets wall rows `x_s - b t_s >= a`. The interval rows stay, so a
  Taylor node is never weaker than the interval one. Certificates carry the centres and
  the lines' slopes (schema v2), and `verify_n17_bb_certificate` re-proves every Taylor
  cut and wall line in exact rationals.
* Other closures. A centre box missing its cell or walls; a pair with no possible option,
  or with `|d| < 1` throughout. A pair with `|d| >= sqrt 2` throughout is dropped.
* Branching. The undecided pair the LP point violates most is split by option.
  Otherwise one angle is bisected: among the squares at least a quarter as wide as the
  widest (`split_ratio`), the one in the pairs the LP point violates most. Splitting the
  widest angle outright refines squares no violated pair involves; on pattern A the
  relevance rule cut the estimated tree sixfold and turned a run that closed 29 percent
  of the tree in ten minutes into a certificate in 499 seconds. When every angle is
  narrower than the resolution floor the node is a near-witness and the run stops,
  unresolved: a feasible pattern ends there, never in a certificate.

The disjunctive LP was preferred to contracting pairs on all four axis families (the
other candidate) because the obstruction is a chain: a pair contractor can only cut a box
when that pair alone is infeasible on it, while one LP adds up the whole chain's slack.
Centres are never branched on: the relaxation loss goes to zero with the angle widths
whatever the centre boxes are, and bound tightening shrinks the boxes for free.

Soundness. Nothing a float solver says is trusted. HiGHS (scipy's bundled build) is used
only to propose multipliers `y >= 0`. With every row `a_r . z <= b_r` valid at every
feasible pose of the node (cell rows from the rational vertices, enclosed outward; cut
rows with float coefficients and a validated right side), `y (A z - b) <= 0` there, so
`sign z_c >= (sign e_c + y A) . z - y b`, whose least value over the centre box is
enclosed outward: a positive bound without a cost closes the node, and with a cost it is
a valid new box bound. Interval floats step outward with `math.nextafter` after every
rounded operation. Cosine and sine are enclosed by `mpmath.iv` at 120 bits at float points
only (cached) and rounded outward; ranges over intervals use the enclosed positions of
the multiples of pi/2. Relative angles use the difference formulas on those enclosures,
so no unenclosed angle is formed. Centre boxes are clipped to cells in exact rationals.
The period's upper end is rounded past `theta0 + pi/2`.

Controls built in. `witness_path` follows a known feasible pose from the root to the
resolution floor and fails if any node on the path closes, loses the pose from its
contracted boxes, or has no child holding it; `--witness-endpoint` runs it on the
endpoint's own pose. `estimate` (`--estimate N`) is Knuth's unbiased tree-size estimator
from random dives, which prices a full run without making it.

What it does not do. It records no proof object beyond counts: a certified verdict is
replayable by rerunning the deterministic search, not by reading the receipt.
"""

from __future__ import annotations

import argparse
import functools
import gzip
import hashlib
import importlib
import json
import math
import random
import time
from collections.abc import Sequence
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path
from typing import Any

import mpmath
import numpy as np

from devtools import check_n17_capacity_one_cover as cover
from devtools import select_n17_sub_patterns as selector

SCHEMA = "n17-subpattern-bb-pilot/v1"
STATUS = (
    "pilot second certifier: a certified verdict is an exact Farkas-checked exhaustion of "
    "the pose space, replayable by rerunning; not yet a record"
)
DEFAULT_DESIGN = cover.UNIQUE_24.name
INF = math.inf
TRIG_PREC = 120
QUANTUM = 2.0**-24
LP_POSITIVE = 1e-12
VIOLATED = 1e-9
DEFAULT_FLOOR = 1e-6
DEFAULT_THETA0 = 0.4
DEFAULT_SPLIT_RATIO = 0.25
# A bound on |f''|/2 for f = (s1 cos + s2 sin)/2, where |f''| = |f| <= sqrt(2)/2: the
# remainder constant of the Taylor rows, at least sqrt(2)/4 = 0.35355339...
TAYLOR_K = 0.35356
MAX_DEPTH = 2000

Iv = tuple[float, float]
Box = tuple[float, float, float, float]
# A plane `(nx, ny, r, c, o)`: `nbar . d >= r`, and `nbar . d >= c g - o` at the pose's gap.
TaylorPlane = tuple[float, float, float, float, float]
# (s1, s2, a, b): `constant + (s1 cos + s2 sin)/2 >= a + b t` for every offset |t| <= rho.
TaylorLine = tuple[int, int, float, float]
# Untyped third-party surfaces: mpmath's interval context, and the HiGHS bindings scipy
# bundles (a warm re-solve there with a new objective costs about 20 microseconds).
iv: Any = mpmath.iv
highs: Any = importlib.import_module("scipy.optimize._highspy._core")
Point = tuple[Fraction, Fraction]


# ---------------------------------------------------------------------------
# Directed-rounding floor
# ---------------------------------------------------------------------------


def dn(x: float) -> float:
    return math.nextafter(x, -INF)


def up(x: float) -> float:
    return math.nextafter(x, INF)


def lower_float(q: Fraction) -> float:
    f = float(q)
    return f if Fraction(f) <= q else dn(f)


def upper_float(q: Fraction) -> float:
    f = float(q)
    return f if Fraction(f) >= q else up(f)


def iadd(a: Iv, b: Iv) -> Iv:
    return dn(a[0] + b[0]), up(a[1] + b[1])


def isub(a: Iv, b: Iv) -> Iv:
    return dn(a[0] - b[1]), up(a[1] - b[0])


def imul(a: Iv, b: Iv) -> Iv:
    products = (a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1])
    return dn(min(products)), up(max(products))


def ineg(a: Iv) -> Iv:
    return -a[1], -a[0]


def magnitude(a: Iv) -> float:
    """The largest absolute value in `a` (exact)."""
    return max(-a[0], a[1])


def least_abs(a: Iv) -> float:
    """The smallest absolute value in `a` (exact)."""
    if a[0] >= 0:
        return a[0]
    if a[1] <= 0:
        return -a[1]
    return 0.0


def up_mul(a: float, b: float) -> float:
    """An upper bound of `a b` for nonnegative `a`, `b`."""
    return up(a * b)


def up_add(a: float, b: float) -> float:
    return up(a + b)


def _iv_float(value: Any) -> Iv:
    """An `mpmath.iv` interval rounded outward to floats."""
    return dn(float(value.a)), up(float(value.b))


def _with_prec(compute: Any) -> Any:
    saved = iv.prec
    iv.prec = TRIG_PREC
    try:
        return compute()
    finally:
        iv.prec = saved


TRIG: dict[float, tuple[Iv, Iv]] = {}
# The angles a recording run evaluates, so that its certificate's table holds exactly
# those (the cache also holds whatever earlier work in the process evaluated).
TRIG_USED: set[float] | None = None


def cos_sin(theta: float) -> tuple[Iv, Iv]:
    """Enclosures of `cos theta` and `sin theta` at a float point (exactly representable).

    Cached in `TRIG`, which a saved certificate writes out as its table of enclosures.
    """
    if TRIG_USED is not None:
        TRIG_USED.add(theta)
    cached = TRIG.get(theta)
    if cached is not None:
        return cached

    def compute() -> tuple[Iv, Iv]:
        x = iv.mpf(theta)
        return _iv_float(iv.cos(x)), _iv_float(iv.sin(x))

    result: tuple[Iv, Iv] = _with_prec(compute)
    TRIG[theta] = result
    return result


def _multiple_of_half_pi(k: int) -> Iv:
    return _with_prec(lambda: _iv_float(iv.pi * k / 2)) if k else (0.0, 0.0)


HALF_PI_MULTIPLES = {k: _multiple_of_half_pi(k) for k in range(-4, 9)}
HALF_PI = HALF_PI_MULTIPLES[1]
TWO_PI = HALF_PI_MULTIPLES[4]


def might_contain(lo: float, hi: float, point: Iv) -> bool:
    """Whether `[lo, hi]` may contain a real known only to lie in `point`."""
    return lo <= point[1] and hi >= point[0]


def contains_half_pi_multiple(lo: float, hi: float) -> bool:
    """Conservatively, whether the real interval `[lo, hi]` meets `(pi/2) Z`."""
    if up(hi - lo) >= HALF_PI[0]:
        return True
    return any(might_contain(lo, hi, value) for value in HALF_PI_MULTIPLES.values())


def h_from(c: Iv, s: Iv) -> float:
    """A lower bound of `(|cos| + |sin|)/2` from enclosures of both."""
    return dn((least_abs(c) + least_abs(s)) / 2)


def h_lower(lo: float, hi: float) -> float:
    """A lower bound of `h(theta) = (|cos theta| + |sin theta|)/2` over `[lo, hi]`.

    `h` is at least 1/2, equals 1/2 at multiples of pi/2, and is concave between two
    consecutive ones, so on an interval meeting none its least value is at an endpoint.
    """
    if contains_half_pi_multiple(lo, hi):
        return 0.5
    return max(0.5, min(h_from(*cos_sin(lo)), h_from(*cos_sin(hi))))


def cos_sin_difference(p: float, q: float) -> tuple[Iv, Iv]:
    """Enclosures of `cos(p - q)` and `sin(p - q)` for the exact real `p - q`."""
    cp, sp = cos_sin(p)
    cq, sq = cos_sin(q)
    return iadd(imul(cp, cq), imul(sp, sq)), isub(imul(sp, cq), imul(cp, sq))


def gap_lower(ti: Iv, tj: Iv) -> float:
    """A lower bound of `g = 1/2 + h(theta_j - theta_i)` over the two angle intervals."""
    if tj[0] <= ti[1] and ti[0] <= tj[1]:
        return 1.0
    lo, hi = dn(tj[0] - ti[1]), up(tj[1] - ti[0])
    if contains_half_pi_multiple(lo, hi):
        return 1.0
    low_end = h_from(*cos_sin_difference(tj[0], ti[1]))
    high_end = h_from(*cos_sin_difference(tj[1], ti[0]))
    return max(1.0, dn(0.5 + min(low_end, high_end)))


# ---------------------------------------------------------------------------
# The pattern
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Pattern:
    """Closed convex cells with exact rows, and the container side."""

    names: tuple[str, ...]
    polygons: tuple[tuple[Point, ...], ...]
    cap: Fraction
    rows: tuple[tuple[tuple[Fraction, Fraction, Fraction], ...], ...] = field(init=False)
    lp_rows: tuple[tuple[tuple[float, float, float, float], ...], ...] = field(init=False)
    pairs: tuple[tuple[int, int], ...] = field(init=False)

    def __post_init__(self) -> None:
        exact: list[tuple[tuple[Fraction, Fraction, Fraction], ...]] = []
        floats: list[tuple[tuple[float, float, float, float], ...]] = []
        for polygon in self.polygons:
            hull = cover.convex_hull(list(polygon))
            cell_rows: list[tuple[Fraction, Fraction, Fraction]] = []
            cell_floats: list[tuple[float, float, float, float]] = []
            for index, start in enumerate(hull):
                end = hull[(index + 1) % len(hull)]
                a, b = end[1] - start[1], start[0] - end[0]
                c = a * start[0] + b * start[1]
                cell_rows.append((a, b, c))
                norm = math.hypot(float(a), float(b))
                cell_floats.append((float(a) / norm, float(b) / norm, float(c) / norm, norm))
            exact.append(tuple(cell_rows))
            floats.append(tuple(cell_floats))
        object.__setattr__(self, "rows", tuple(exact))
        object.__setattr__(self, "lp_rows", tuple(floats))
        count = len(self.polygons)
        object.__setattr__(
            self, "pairs", tuple((i, j) for i in range(count) for j in range(i + 1, count))
        )

    @property
    def k(self) -> int:
        return len(self.polygons)


def cover_pattern(names: Sequence[str], design: str = DEFAULT_DESIGN) -> Pattern:
    cells = {cell.name: cell for cell in cover.build_cover(cover.DESIGNS[design])}
    missing = [name for name in names if name not in cells]
    if missing:
        raise ValueError(f"unknown cells {missing}")
    ordered = sorted(names, key=list(cells).index)
    return Pattern(tuple(ordered), tuple(cells[name].vertices for name in ordered), cover.U)


def bounding_box(polygon: Sequence[Point]) -> Box:
    xs, ys = [p[0] for p in polygon], [p[1] for p in polygon]
    return (
        lower_float(min(xs)),
        upper_float(max(xs)),
        lower_float(min(ys)),
        upper_float(max(ys)),
    )


@functools.lru_cache(maxsize=200_000)
def clip_to_box(polygon: tuple[Point, ...], box: Box) -> Box | None:
    """The outward float bounding box of `polygon` meet `box`, exactly; None when empty."""
    xl, xh, yl, yh = (Fraction(value) for value in box)
    one, zero = Fraction(1), Fraction(0)
    current = list(polygon)
    for a, b, c in ((-one, zero, -xl), (one, zero, xh), (zero, -one, -yl), (zero, one, yh)):
        current = cover.clip(current, a, b, c)
        if not current:
            return None
    clipped = bounding_box(current)
    return (
        max(box[0], clipped[0]),
        min(box[1], clipped[1]),
        max(box[2], clipped[2]),
        min(box[3], clipped[3]),
    )


# ---------------------------------------------------------------------------
# Nodes, options and the relaxation
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Node:
    angles: tuple[Iv, ...]
    boxes: tuple[Box, ...]
    windows: tuple[Iv | None, ...]
    depth: int
    share: float = 1.0


@dataclass(frozen=True)
class Option:
    """A normal-angle interval and its relaxed row `nbar . d >= bound` (d = c_j - c_i)."""

    lo: float
    hi: float
    nx: float
    ny: float
    bound: float
    loss: float


@dataclass(frozen=True)
class PairTerm:
    """A pair's state on a node.

    `kind` is `separated` (always disjoint), `disc` or `pair` (never disjoint),
    `decided` (one option) or `undecided`. `cuts` are valid rows `u . d >= v`;
    `planes` are half-planes one of which every disjoint pose satisfies.
    """

    kind: str
    options: list[Iv] = field(default_factory=list[Iv])
    cuts: list[tuple[float, float, float]] = field(
        default_factory=list[tuple[float, float, float]]
    )
    planes: list[tuple[float, float, float]] = field(
        default_factory=list[tuple[float, float, float]]
    )
    # Every normal-angle piece `(lo, hi, m)` of the node within the window, alive or not,
    # with the point `m` its planes use; what a saved certificate records for the pair.
    pieces: list[tuple[float, float, float]] = field(
        default_factory=list[tuple[float, float, float]]
    )
    # Taylor mode only: cuts `u . d - w (t_j - t_i) >= v` as `(ux, uy, w, v, line)`.
    taylor: list[tuple[float, float, float, float, TaylorLine]] = field(
        default_factory=list[tuple[float, float, float, float, TaylorLine]]
    )


@dataclass(frozen=True)
class Row:
    """`sum values . z[columns] <= rhs` for the LP, and the verified row it stands for.

    The verified row (`exact` coefficients and `exact_rhs`, as outward float intervals)
    holds at every feasible pose of the node; the LP row is it divided by `norm`, so an LP
    multiplier `y` is the verified multiplier `y / norm`.
    """

    columns: tuple[int, ...]
    values: tuple[float, ...]
    rhs: float
    norm: float
    exact: tuple[Iv, ...]
    exact_rhs: Iv
    owner: int = -1  # the pair a cut row belongs to; -1 for a cell row, -2 for a wall row
    # Taylor mode only: the certificate entry of a Taylor cut or a wall row.
    record: tuple[Any, ...] | None = None


def column_spans(boxes: Sequence[Box], offsets: Sequence[Iv] = ()) -> list[Iv]:
    """The LP's column ranges: x and y per square, then (Taylor mode) the angle offsets."""
    spans: list[Iv] = []
    for box in boxes:
        spans.extend(((box[0], box[1]), (box[2], box[3])))
    spans.extend(offsets)
    return spans


def dual_bound(
    rows: Sequence[Row],
    multipliers: Sequence[float],
    spans: Sequence[Iv],
    cost: tuple[int, float] | None,
) -> float:
    """A lower bound of `sign z[column]` (or of 0) over the node, from any `y >= 0`.

    At a feasible pose `y . (A z - b) <= 0`, so `sign z_c >= (sign e_c + y A) . z - y b`,
    whose least value over the column ranges is enclosed outward here. With no cost, a
    positive result says the node holds no feasible pose (the Farkas check).
    """
    combined: list[Iv] = [(0.0, 0.0)] * len(spans)
    if cost is not None:
        combined[cost[0]] = (cost[1], cost[1])
    right: Iv = (0.0, 0.0)
    for row, weight in zip(rows, multipliers, strict=True):
        if weight <= 0.0:
            continue
        y = weight / row.norm
        scaled = (y, y)
        for column, coefficient in zip(row.columns, row.exact, strict=True):
            combined[column] = iadd(combined[column], imul(scaled, coefficient))
        right = iadd(right, imul(scaled, row.exact_rhs))
    least = 0.0
    for coefficient, span in zip(combined, spans, strict=True):
        least = dn(least + imul(coefficient, span)[0])
    return dn(least - right[1])


@dataclass
class Evaluation:
    pruned: str | None
    boxes: tuple[Box, ...] = ()
    terms: list[tuple[int, PairTerm]] = field(default_factory=list[tuple[int, PairTerm]])
    lp_depth: float | None = None
    point: list[float] | None = None
    farkas_failed: bool = False
    # Which pairs closed the node: the pair itself for `pair` and `disc`, and each pair's
    # share of the Farkas multipliers (cells as -1) for `lp`. Diagnostic only.
    blame: dict[int, float] = field(default_factory=dict[int, float])


def _quantised(lo: float, hi: float) -> float:
    middle = 0.5 * (lo + hi)
    snapped = round(middle / QUANTUM) * QUANTUM
    return snapped if lo <= snapped <= hi else middle


def relax(lo: float, hi: float, dx: Iv, dy: Iv, *, d_max: float, g_lo: float) -> Option:
    """The relaxed row of "some normal at an angle in [lo, hi] separates"."""
    m = _quantised(lo, hi)
    c, s = cos_sin(m)
    nx, ny = 0.5 * (c[0] + c[1]), 0.5 * (s[0] + s[1])
    eps = max(up(c[1] - c[0]), up(s[1] - s[0]))
    tau = up(max(up(m - lo), up(hi - m)) / 2)
    perp = magnitude(iadd(imul(ineg(s), dx), imul(c, dy)))
    loss = up_mul(2 * tau, up_add(perp, up_mul(tau, d_max)))
    loss = up_add(loss, up_mul(eps, up_add(magnitude(dx), magnitude(dy))))
    return Option(lo, hi, nx, ny, dn(g_lo - loss), loss)


def option_possible(option: Option, dx: Iv, dy: Iv) -> bool:
    reach = iadd(imul((option.nx, option.nx), dx), imul((option.ny, option.ny), dy))
    return reach[1] >= option.bound


def chord_pieces(lo: float, hi: float, g_lo: float) -> list[tuple[float, float]]:
    """Normal angles and right sides of three half-planes covering an option.

    Every `d` with `n(phi) . d >= g` for some `phi` in `[lo, hi]` (width below pi/2) has
    `n(lo) . d >= g`, `n(hi) . d >= g` or `n(m) . d >= g cos(x)`, `x = max(m - lo, hi -
    m)`: the complement of the three is a polygon whose part in the sector `[lo, hi]`
    lies under the chord, inside the disc of radius `g`, and whose part outside the
    sector meets the nearer end normal below `g`. `cos x >= 1 - x^2/2`.
    """
    if up(hi - lo) >= HALF_PI[0]:
        return []
    m = _quantised(lo, hi)
    x = up(max(up(m - lo), up(hi - m)))
    chord = dn(g_lo * dn(1.0 - up(x * x) / 2))
    return [(lo, g_lo), (hi, g_lo), (m, chord)]


def piece_possible(angle: float, rhs: float, dx: Iv, dy: Iv) -> bool:
    c, s = cos_sin(angle)
    return iadd(imul(c, dx), imul(s, dy))[1] >= rhs


def piece_option(lo: float, hi: float, angle: float, rhs: float, *, dx: Iv, dy: Iv) -> Option:
    """The row `nbar . d >= rhs - |nbar - n(angle)| |d|_1` of one half-plane."""
    c, s = cos_sin(angle)
    eps = max(up(c[1] - c[0]), up(s[1] - s[0]))
    slack = up_mul(eps, up_add(magnitude(dx), magnitude(dy)))
    return Option(lo, hi, 0.5 * (c[0] + c[1]), 0.5 * (s[0] + s[1]), dn(rhs - slack), slack)


Halfplane = tuple[float, float, float]


def option_halfplanes(
    lo: float, hi: float, dx: Iv, dy: Iv, *, d_max: float, g_lo: float
) -> list[Halfplane]:
    """Float half-planes `nx dx + ny dy >= r`, one of which holds at every pose using
    the option, restricted to those the d-box can meet (empty: the option is impossible).
    """
    return [plane[:3] for plane in option_planes(lo, hi, dx, dy, d_max=d_max, g_lo=g_lo)]


def chord_factor(lo: float, hi: float) -> float:
    """The chord plane's factor `dn(1 - x^2/2) <= cos x`, as `chord_pieces` computes it."""
    m = _quantised(lo, hi)
    x = up(max(up(m - lo), up(hi - m)))
    return dn(1.0 - up(x * x) / 2)


def option_planes(
    lo: float, hi: float, dx: Iv, dy: Iv, *, d_max: float, g_lo: float
) -> list[TaylorPlane]:
    """The half-planes of `option_halfplanes`, each with its factor and offset.

    Each `(nx, ny, r, c, o)` has `r = c g_lo - o` up to outward rounding, and every pose
    that uses it satisfies `nbar . d >= c g - o` at its own gap `g`: `c = 1` and
    `o` the enclosure slack for an end plane, `c` the chord factor for the chord plane,
    `c = 1` and `o` the whole loss for the relaxed plane of a wide option.
    """
    pieces = chord_pieces(lo, hi, g_lo)
    found: list[tuple[Option, float]] = []
    if pieces:
        factors = (1.0, 1.0, chord_factor(lo, hi))
        found = [
            (piece_option(lo, hi, angle, rhs, dx=dx, dy=dy), factor)
            for (angle, rhs), factor in zip(pieces, factors, strict=True)
            if piece_possible(angle, rhs, dx, dy)
        ]
    else:
        found = [(relax(lo, hi, dx, dy, d_max=d_max, g_lo=g_lo), 1.0)]
    return [
        (option.nx, option.ny, option.bound, factor, option.loss)
        for option, factor in found
        if option_possible(option, dx, dy)
    ]


# ---------------------------------------------------------------------------
# The Taylor relaxation of the trigonometric coefficients (opt-in)
# ---------------------------------------------------------------------------


def offset_span(span: Iv, centre: float) -> Iv:
    """An enclosure of `theta - centre` for theta in `span`."""
    return dn(span[0] - centre), up(span[1] - centre)


def possible_signs(value: Iv, lo: float, hi: float, parity: int) -> list[int]:
    """Signs a sinusoid can take on [lo, hi]: both if it may vanish there.

    `parity` 1 is the cosine (zero at odd multiples of pi/2), 0 the sine (even ones);
    `value` encloses it at a point of the interval.
    """
    vanishes = up(hi - lo) >= HALF_PI[0] or any(
        k % 2 == parity and might_contain(lo, hi, multiple)
        for k, multiple in HALF_PI_MULTIPLES.items()
    )
    if vanishes or value[0] <= 0.0 <= value[1]:
        return [1, -1]
    return [1] if value[0] > 0.0 else [-1]


def taylor_lines(c: Iv, s: Iv, rho: float, span: Iv, *, constant: float) -> list[TaylorLine]:
    """Lines below `constant + h` over an angle interval, from its centre's enclosures.

    `h(a) = (|cos a| + |sin a|)/2` is the largest of `f(a) = (s1 cos a + s2 sin a)/2`
    over the four sign pairs, so `h >= f` for each, and `f'' = -f`, `|f''| <= sqrt 2/2`.
    At the centre `f(t) >= f(0) + f'(0) t - TAYLOR_K t^2`, and with the float slope `b`
    in the enclosure of `f'(0)`, `f'(0) t >= b t - |f'(0) - b| rho`. One line per sign
    pair `h` can follow on `span` (where `cos`, `sin` keep a sign, one; across a zero,
    both, which together keep the kink).
    """
    lines: list[TaylorLine] = []
    for s1 in possible_signs(c, span[0], span[1], 1):
        for s2 in possible_signs(s, span[0], span[1], 0):
            cos_part = c if s1 > 0 else ineg(c)
            sin_part = s if s2 > 0 else ineg(s)
            f = iadd(cos_part, sin_part)
            # f' = (s2 cos - s1 sin)/2; both halvings below are exact.
            slope = isub(c if s2 > 0 else ineg(c), s if s1 > 0 else ineg(s))
            f = (0.5 * f[0], 0.5 * f[1])
            slope = (0.5 * slope[0], 0.5 * slope[1])
            b = 0.5 * (slope[0] + slope[1])
            spread = max(up(slope[1] - b), up(b - slope[0]))
            loss = up_add(up_mul(spread, rho), up_mul(TAYLOR_K, up_mul(rho, rho)))
            lines.append((s1, s2, dn(dn(constant + f[0]) - loss), b))
    return lines


def taylor_plane_min(
    u: tuple[float, float],
    w: float,
    plane: TaylorPlane,
    line: TaylorLine,
    boxes: tuple[Iv, Iv, Iv],
) -> float:
    """A lower bound of `u . d - w t` over the boxes meet `nbar . d - c b t >= c a - o`.

    For any `lam >= 0` the objective is at least `(u - lam nbar) . d + (lam c b - w) t +
    lam (c a - o)`, bounded below over the boxes; the candidates are 0 and the multipliers
    that cancel one coefficient, which include the optimal one.
    """
    nx, ny, _, c, o = plane
    _, _, a, b = line
    dx, dy, dt = boxes
    candidates = [0.0]
    for numerator, denominator in ((u[0], nx), (u[1], ny), (w, c * b)):
        if denominator != 0.0:
            candidates.append(numerator / denominator)
    best = -INF
    for lam in candidates:
        if not lam >= 0.0 or math.isinf(lam):
            continue
        scaled = (lam, lam)
        cx = isub((u[0], u[0]), imul(scaled, (nx, nx)))
        cy = isub((u[1], u[1]), imul(scaled, (ny, ny)))
        ct = isub(imul(imul(scaled, (c, c)), (b, b)), (w, w))
        constant = imul(scaled, isub(imul((c, c), (a, a)), (o, o)))
        value = iadd(iadd(imul(cx, dx), imul(cy, dy)), iadd(imul(ct, dt), constant))[0]
        best = max(best, value)
    return best


def taylor_cuts(
    facets: list[Halfplane],
    planes: list[TaylorPlane],
    lines: list[TaylorLine],
    boxes: tuple[Iv, Iv, Iv],
) -> list[tuple[float, float, float, float, TaylorLine]]:
    """Valid cuts `u . d - w t >= v` per gap line, for each interval hull facet `u`.

    `w` is the secant slope of the facet's float value across the offset box, a choice;
    `v` is the rigorous least value over every plane (`taylor_plane_min`).
    """
    dx, dy, dt = boxes
    cuts: list[tuple[float, float, float, float, TaylorLine]] = []
    for line in lines:
        _, _, a, b = line
        if not dn(a - up_mul(abs(b), magnitude(dt))) > 0.0:
            # The line must stay positive over the offsets: a reader's exact chord factor
            # and gap constant are then at least these, and its half-spaces lie inside.
            continue
        for ux, uy, _ in facets:
            u = (ux, uy)

            def level(
                t: float, u: tuple[float, float] = u, a: float = a, b: float = b
            ) -> float:
                return min(
                    plane_min(u, (nx, ny, c * (a + b * t) - o), dx, dy)
                    for nx, ny, _, c, o in planes
                )

            w = (level(dt[1]) - level(dt[0])) / (dt[1] - dt[0]) if dt[1] > dt[0] else 0.0
            if not math.isfinite(w):
                w = 0.0
            v = min(taylor_plane_min(u, w, plane, line, boxes) for plane in planes)
            if math.isfinite(v):
                cuts.append((ux, uy, w, v, line))
    return cuts


def clip_box(dx: Iv, dy: Iv, plane: Halfplane) -> list[tuple[float, float]]:
    """Approximate vertices of the d-box meet a half-plane (floats; selection only)."""
    corners = [(dx[0], dy[0]), (dx[1], dy[0]), (dx[1], dy[1]), (dx[0], dy[1])]
    nx, ny, r = plane
    result: list[tuple[float, float]] = []
    for index, start in enumerate(corners):
        end = corners[(index + 1) % 4]
        f_start = nx * start[0] + ny * start[1] - r
        f_end = nx * end[0] + ny * end[1] - r
        if f_start >= 0:
            result.append(start)
        if f_start * f_end < 0:
            t = f_start / (f_start - f_end)
            result.append(
                (start[0] + t * (end[0] - start[0]), start[1] + t * (end[1] - start[1]))
            )
    return result


def float_hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    ordered = sorted(set(points))
    if len(ordered) < 3:
        return ordered

    def turn(o: tuple[float, float], a: tuple[float, float], b: tuple[float, float]) -> float:
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower: list[tuple[float, float]] = []
    for point in ordered:
        while len(lower) >= 2 and turn(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)
    upper: list[tuple[float, float]] = []
    for point in reversed(ordered):
        while len(upper) >= 2 and turn(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    return lower[:-1] + upper[:-1]


def plane_min(u: tuple[float, float], plane: Halfplane, dx: Iv, dy: Iv) -> float:
    """A lower bound of `min u . d` over the d-box meet `n . d >= r`.

    For any `lam >= 0`, `u . d = (u - lam n) . d + lam n . d >= min over the box of
    (u - lam n) . d + lam r`; the candidates are 0 and the two multipliers that cancel a
    component, the optimal one for a vertex on a box edge.
    """
    nx, ny, r = plane
    candidates = [0.0]
    if nx != 0.0:
        candidates.append(u[0] / nx)
    if ny != 0.0:
        candidates.append(u[1] / ny)
    best = -INF
    for lam in candidates:
        if not lam >= 0.0 or math.isinf(lam):
            continue
        scaled = (lam, lam)
        cx = isub((u[0], u[0]), imul(scaled, (nx, nx)))
        cy = isub((u[1], u[1]), imul(scaled, (ny, ny)))
        value = iadd(iadd(imul(cx, dx), imul(cy, dy)), imul(scaled, (r, r)))[0]
        best = max(best, value)
    return best


def hull_cuts(planes: list[Halfplane], dx: Iv, dy: Iv) -> list[Halfplane]:
    """Valid cuts `u . d >= v` from the convex hull of the union of the planes in the box."""
    points = [vertex for plane in planes for vertex in clip_box(dx, dy, plane)]
    hull = float_hull(points)
    if len(hull) < 3:
        return []
    span = max(dx[1] - dx[0], dy[1] - dy[0], 1e-12)
    tolerance = 1e-9 * span
    cuts: list[Halfplane] = []
    for index, start in enumerate(hull):
        end = hull[(index + 1) % len(hull)]
        on_side = any(
            abs(start[axis] - bound) <= tolerance and abs(end[axis] - bound) <= tolerance
            for axis, bounds in ((0, dx), (1, dy))
            for bound in bounds
        )
        if on_side:
            continue
        ex, ey = end[0] - start[0], end[1] - start[1]
        length = math.hypot(ex, ey)
        if length <= tolerance:
            continue
        u = (-ey / length, ex / length)  # inward normal of a counterclockwise hull
        value = min(plane_min(u, plane, dx, dy) for plane in planes)
        box_least = iadd(imul((u[0], u[0]), dx), imul((u[1], u[1]), dy))[0]
        if value > box_least + tolerance:
            cuts.append((u[0], u[1], value))
    return cuts


def base_pieces(ti: Iv, tj: Iv) -> list[Iv]:
    """The eight normal-angle intervals of a pair, outward rounded."""
    pieces: list[Iv] = []
    for theta in (ti, tj):
        for k in range(4):
            shift = HALF_PI_MULTIPLES[k]
            pieces.append((dn(theta[0] + shift[0]), up(theta[1] + shift[1])))
    return pieces


def in_window(piece: Iv, window: Iv | None) -> list[Iv]:
    """The parts of `piece`, shifted by multiples of 2 pi, inside the window."""
    if window is None:
        return [piece]
    parts: list[Iv] = []
    for turns in (-1, 0, 1):
        if turns:
            shift = HALF_PI_MULTIPLES[4 * turns] if turns > 0 else ineg(TWO_PI)
            shifted = (dn(piece[0] + shift[0]), up(piece[1] + shift[1]))
        else:
            shifted = piece
        lo, hi = max(shifted[0], window[0]), min(shifted[1], window[1])
        if lo <= hi:
            parts.append((lo, hi))
    return parts


def merge(pieces: list[Iv], gap_factor: float) -> list[Iv]:
    if not pieces:
        return []
    ordered = sorted(pieces)
    merged = [ordered[0]]
    for lo, hi in ordered[1:]:
        last_lo, last_hi = merged[-1]
        allowance = gap_factor * max(last_hi - last_lo, hi - lo)
        if lo <= last_hi + allowance:
            merged[-1] = (last_lo, max(last_hi, hi))
        else:
            merged.append((lo, hi))
    return merged


def difference_box(first: Box, second: Box) -> tuple[Iv, Iv]:
    """Enclosures of `c_j - c_i` for `c_i` in `first` and `c_j` in `second`."""
    return (
        (dn(second[0] - first[1]), up(second[1] - first[0])),
        (dn(second[2] - first[3]), up(second[3] - first[2])),
    )


def squared_range(dx: Iv, dy: Iv) -> Iv:
    near_x, near_y = least_abs(dx), least_abs(dy)
    far_x, far_y = magnitude(dx), magnitude(dy)
    return (
        dn(dn(near_x * near_x) + dn(near_y * near_y)),
        up(up(far_x * far_x) + up(far_y * far_y)),
    )


# ---------------------------------------------------------------------------
# One node
# ---------------------------------------------------------------------------


@dataclass
class Settings:
    theta0: float = DEFAULT_THETA0
    floor: float = DEFAULT_FLOOR
    merge_gap: float = 0.0
    max_seconds: float = 600.0
    max_nodes: int | None = None
    split_ratio: float = DEFAULT_SPLIT_RATIO
    obbt_rounds: int = 3
    obbt_repeat: float = 0.05
    taylor: bool = False


@dataclass(frozen=True)
class TaylorContext:
    """A node's angle centres, offset ranges and wall lines (Taylor mode)."""

    centres: tuple[float, ...]
    offsets: tuple[Iv, ...]
    walls: tuple[tuple[TaylorLine, ...], ...]


class Solver:
    def __init__(self, pattern: Pattern, settings: Settings) -> None:
        if not -math.pi <= settings.theta0 <= math.pi:
            # The enclosed multiples of pi/2 reach [-2 pi, 4 pi]; angles must stay inside.
            raise ValueError("theta0 must lie in [-pi, pi]")
        self.pattern = pattern
        self.settings = settings
        self.cap_hi = upper_float(pattern.cap)
        self.cell_boxes = tuple(bounding_box(polygon) for polygon in pattern.polygons)
        self.pair_cache: dict[tuple[Any, ...], PairTerm] = {}
        self.highs = highs._Highs()  # noqa: SLF001
        self.highs.setOptionValue("output_flag", False)  # noqa: FBT003
        self.recorder: Recorder | None = None
        self.taylor: TaylorContext | None = None
        self.cell_rows: list[Row] = []
        for square, (exact, floats) in enumerate(
            zip(pattern.rows, pattern.lp_rows, strict=True)
        ):
            for (a, b, c), (fa, fb, fc, norm) in zip(exact, floats, strict=True):
                self.cell_rows.append(
                    Row(
                        (2 * square, 2 * square + 1),
                        (fa, fb),
                        fc,
                        norm,
                        ((lower_float(a), upper_float(a)), (lower_float(b), upper_float(b))),
                        (lower_float(c), upper_float(c)),
                    )
                )

    def root(self) -> Node:
        theta0 = self.settings.theta0
        top = up(theta0 + HALF_PI[1])
        return Node(
            angles=tuple((theta0, top) for _ in range(self.pattern.k)),
            boxes=self.cell_boxes,
            windows=tuple(None for _ in self.pattern.pairs),
            depth=0,
        )

    def contract(self, node: Node) -> tuple[Box, ...] | None:
        boxes: list[Box] = []
        for index, (box, angle) in enumerate(zip(node.boxes, node.angles, strict=True)):
            h = h_lower(*angle)
            far = up(self.cap_hi - h)
            walled = (max(box[0], h), min(box[1], far), max(box[2], h), min(box[3], far))
            if walled[0] > walled[1] or walled[2] > walled[3]:
                return None
            clipped = clip_to_box(self.pattern.polygons[index], walled)
            if clipped is None:
                return None
            boxes.append(clipped)
        return tuple(boxes)

    def pair_term(self, node: Node, boxes: tuple[Box, ...], index: int) -> PairTerm:
        """One pair on the node: its kind, its options, the hull cuts and the pieces."""
        i, j = self.pattern.pairs[index]
        key = (index, node.angles[i], node.angles[j], node.windows[index], boxes[i], boxes[j])
        cached = self.pair_cache.get(key)
        if cached is not None:
            return cached
        dx, dy = difference_box(boxes[i], boxes[j])
        squared = squared_range(dx, dy)
        term: PairTerm
        if squared[0] >= 2.0:
            term = PairTerm("separated")
        elif squared[1] < 1.0:
            term = PairTerm("disc")
        else:
            g_lo = gap_lower(node.angles[i], node.angles[j])
            d_max = up(math.sqrt(squared[1]))
            pieces = [
                part
                for piece in base_pieces(node.angles[i], node.angles[j])
                for part in in_window(piece, node.windows[index])
            ]
            planes: list[Halfplane] = []
            full: list[TaylorPlane] = []
            alive: list[Iv] = []
            for piece in pieces:
                found = option_planes(*piece, dx, dy, d_max=d_max, g_lo=g_lo)
                if found:
                    alive.append(piece)
                    planes.extend(plane[:3] for plane in found)
                    full.extend(found)
            recorded = [(lo, hi, _quantised(lo, hi)) for lo, hi in pieces]
            if not alive:
                term = PairTerm("pair", pieces=recorded)
            else:
                options = merge(alive, self.settings.merge_gap)
                cuts = hull_cuts(planes, dx, dy)
                term = PairTerm(
                    "undecided" if len(options) > 1 else "decided",
                    options,
                    cuts,
                    planes,
                    recorded,
                    self.pair_taylor(node, (i, j), cuts, full, (dx, dy))
                    if self.settings.taylor
                    else [],
                )
        if len(self.pair_cache) > 400_000:
            self.pair_cache.clear()
        self.pair_cache[key] = term
        return term

    # -- the Taylor relaxation ------------------------------------------------------------

    def taylor_context(self, node: Node) -> TaylorContext:
        """Each square's centre angle, offset range and wall lines `h >= a + b t`."""
        centres = tuple(0.5 * (lo + hi) for lo, hi in node.angles)
        offsets = tuple(
            offset_span(span, centre) for span, centre in zip(node.angles, centres, strict=True)
        )
        walls = tuple(
            tuple(taylor_lines(*cos_sin(centre), magnitude(offset), span, constant=0.0))
            for span, centre, offset in zip(node.angles, centres, offsets, strict=True)
        )
        return TaylorContext(centres, offsets, walls)

    def pair_taylor(
        self,
        node: Node,
        pair: tuple[int, int],
        facets: list[Halfplane],
        planes: list[TaylorPlane],
        d_box: tuple[Iv, Iv],
    ) -> list[tuple[float, float, float, float, TaylorLine]]:
        """Taylor cuts of one pair: gap lines at the centre relative angle, then cuts."""
        i, j = pair
        ti, tj = node.angles[i], node.angles[j]
        ci, cj = 0.5 * (ti[0] + ti[1]), 0.5 * (tj[0] + tj[1])
        oi, oj = offset_span(ti, ci), offset_span(tj, cj)
        dt = (dn(oj[0] - oi[1]), up(oj[1] - oi[0]))
        relative = (dn(tj[0] - ti[1]), up(tj[1] - ti[0]))
        lines = taylor_lines(*cos_sin_difference(cj, ci), magnitude(dt), relative, constant=0.5)
        return taylor_cuts(facets, planes, lines, (d_box[0], d_box[1], dt))

    def taylor_row(self, index: int, cut: tuple[float, float, float, float, TaylorLine]) -> Row:
        """`u . (c_j - c_i) - w (t_j - t_i) >= v` as a row `<= -v`."""
        i, j = self.pattern.pairs[index]
        k = self.pattern.k
        ux, uy, w, v, (s1, s2, _, b) = cut
        values = (ux, uy, -ux, -uy, -w, w)
        return Row(
            (2 * i, 2 * i + 1, 2 * j, 2 * j + 1, 2 * k + i, 2 * k + j),
            values,
            -v,
            1.0,
            tuple((value, value) for value in values),
            (-v, -v),
            index,
            ("u", index, ux, uy, v, w, s1, s2, b),
        )

    def wall_rows(self, boxes: tuple[Box, ...]) -> list[Row]:
        """`h(theta_s) <= x_s, y_s <= U - h(theta_s)` through each wall line, unless slack."""
        assert self.taylor is not None
        k = self.pattern.k
        cap_lo = lower_float(self.pattern.cap)
        rows: list[Row] = []
        for s, (box, lines, offset) in enumerate(
            zip(boxes, self.taylor.walls, self.taylor.offsets, strict=True)
        ):
            reach = magnitude(offset)
            for s1, s2, a, b in lines:
                swing = abs(b) * reach
                for axis, (lo, hi) in enumerate(((box[0], box[1]), (box[2], box[3]))):
                    column = 2 * s + axis
                    if lo <= a + swing + 1e-9:
                        rows.append(
                            Row(
                                (column, 2 * k + s),
                                (-1.0, b),
                                -a,
                                1.0,
                                ((-1.0, -1.0), (b, b)),
                                (-a, -a),
                                -2,
                                ("w", s, axis, 1, s1, s2, b, a),
                            )
                        )
                    if hi >= self.cap_hi - a - swing - 1e-9:
                        rhs = (dn(cap_lo - a), up(self.cap_hi - a))
                        rows.append(
                            Row(
                                (column, 2 * k + s),
                                (1.0, b),
                                rhs[1],
                                1.0,
                                ((1.0, 1.0), (b, b)),
                                rhs,
                                -2,
                                ("w", s, axis, -1, s1, s2, b, a),
                            )
                        )
        return rows

    def spans(self, boxes: Sequence[Box]) -> list[Iv]:
        return column_spans(boxes, self.taylor.offsets if self.taylor is not None else ())

    def assess(self, node: Node) -> Evaluation:
        """Contract, relax, solve and tighten until the boxes stop shrinking."""
        self.taylor = self.taylor_context(node) if self.settings.taylor else None
        boxes = self.contract(node)
        if boxes is None:
            return Evaluation("cell")
        evaluation = Evaluation(None, boxes)
        for _ in range(self.settings.obbt_rounds + 1):
            if self.recorder is not None:
                self.recorder.begin_round(boxes)
            evaluation, rows = self.relaxation(node, boxes)
            if evaluation.pruned is None:
                self.solve_lp(evaluation, rows)
            if evaluation.pruned is not None or self.settings.obbt_rounds == 0:
                break
            following = self.next_boxes(evaluation, rows)
            if following is None:
                break
            boxes = following
        return evaluation

    def relaxation(self, node: Node, boxes: tuple[Box, ...]) -> tuple[Evaluation, list[Row]]:
        terms: list[tuple[int, PairTerm]] = []
        rows = list(self.cell_rows)
        for index in range(len(self.pattern.pairs)):
            term = self.pair_term(node, boxes, index)
            if self.recorder is not None:
                self.recorder.terms[index] = term
            if term.kind in ("disc", "pair"):
                if self.recorder is not None:
                    self.recorder.closed_by_pair(index, term.kind)
                return Evaluation(term.kind, blame={index: 1.0}), rows
            if term.kind in ("decided", "undecided"):
                terms.append((index, term))
                rows.extend(self.cut_row(index, cut) for cut in term.cuts)
                rows.extend(self.taylor_row(index, cut) for cut in term.taylor)
        if self.taylor is not None:
            rows.extend(self.wall_rows(boxes))
        return Evaluation(None, boxes, terms), rows

    def next_boxes(self, evaluation: Evaluation, rows: list[Row]) -> tuple[Box, ...] | None:
        """Tighten the evaluation's boxes; the new boxes when worth another round."""
        boxes = evaluation.boxes
        tightened = self.tighten(evaluation, rows)
        if tightened is None:
            evaluation.pruned = "obbt"
            return None
        evaluation.boxes = tightened
        if self.recorder is not None:
            self.recorder.tightened(tightened)
        shrink = max(
            1.0 - (new[hi] - new[lo]) / max(old[hi] - old[lo], 1e-300)
            for new, old in zip(tightened, boxes, strict=True)
            for lo, hi in ((0, 1), (2, 3))
        )
        return tightened if shrink >= self.settings.obbt_repeat else None

    # -- the linear program, the Farkas check and bound tightening ---------------------

    def cut_row(self, index: int, cut: Halfplane) -> Row:
        """`u . (c_j - c_i) >= v` as `u . c_i - u . c_j <= -v`."""
        i, j = self.pattern.pairs[index]
        ux, uy, v = cut
        values = (ux, uy, -ux, -uy)
        return Row(
            (2 * i, 2 * i + 1, 2 * j, 2 * j + 1),
            values,
            -v,
            1.0,
            tuple((value, value) for value in values),
            (-v, -v),
            index,
        )

    def columns(self) -> int:
        """Centres, then angle offsets in Taylor mode, then the LP's slack `t`."""
        return (3 if self.taylor is not None else 2) * self.pattern.k + 1

    def load(self, rows: list[Row], boxes: tuple[Box, ...]) -> None:
        n = self.columns()
        lp = highs.HighsLp()
        lp.num_col_ = n
        lp.num_row_ = len(rows)
        cost = np.zeros(n)
        cost[-1] = 1.0
        lp.col_cost_ = cost
        offsets = self.taylor.offsets if self.taylor is not None else ()
        lp.col_lower_ = np.array([*self._interleave(boxes, 0), *(o[0] for o in offsets), -1.0])
        lp.col_upper_ = np.array(
            [*self._interleave(boxes, 1), *(o[1] for o in offsets), highs.kHighsInf]
        )
        lp.row_lower_ = np.full(len(rows), -highs.kHighsInf)
        lp.row_upper_ = np.array([row.rhs for row in rows])
        starts, indices, values = [0], [], []
        for row in rows:
            indices.extend(row.columns)
            values.extend(row.values)
            indices.append(n - 1)
            values.append(-1.0)
            starts.append(len(indices))
        lp.a_matrix_.format_ = highs.MatrixFormat.kRowwise
        lp.a_matrix_.start_ = np.array(starts, dtype=np.int32)
        lp.a_matrix_.index_ = np.array(indices, dtype=np.int32)
        lp.a_matrix_.value_ = np.array(values, dtype=np.float64)
        lp.a_matrix_.num_col_ = n
        lp.a_matrix_.num_row_ = len(rows)
        self.highs.passModel(lp)

    @staticmethod
    def _interleave(boxes: tuple[Box, ...], side: int) -> list[float]:
        return [bound for box in boxes for bound in (box[side], box[2 + side])]

    def run(self) -> tuple[float, list[float], list[float]] | None:
        self.highs.run()
        if self.highs.getModelStatus() != highs.HighsModelStatus.kOptimal:
            return None
        solution = self.highs.getSolution()
        value = float(self.highs.getInfo().objective_function_value)
        point = [float(v) for v in solution.col_value]
        duals = [max(0.0, -float(v)) for v in solution.row_dual]
        return value, point, duals

    def solve_lp(self, evaluation: Evaluation, rows: list[Row]) -> None:
        self.load(rows, evaluation.boxes)
        outcome = self.run()
        if outcome is None:
            evaluation.farkas_failed = True
            return
        value, point, duals = outcome
        evaluation.lp_depth = value
        evaluation.point = point[: 2 * self.pattern.k]
        if value <= LP_POSITIVE:
            return
        if dual_bound(rows, duals, self.spans(evaluation.boxes), None) > 0.0:
            evaluation.pruned = "lp"
            if self.recorder is not None:
                self.recorder.farkas(rows, duals)
            total = sum(duals) or 1.0
            for row, weight in zip(rows, duals, strict=True):
                if weight > 0.0:
                    evaluation.blame[row.owner] = (
                        evaluation.blame.get(row.owner, 0.0) + weight / total
                    )
        else:
            evaluation.farkas_failed = True

    def tighten(self, evaluation: Evaluation, rows: list[Row]) -> tuple[Box, ...] | None:
        """Bound every centre coordinate over the relaxation; None when one is empty."""
        k = self.pattern.k
        n = self.columns()
        bounds = [list(box) for box in evaluation.boxes]
        self.highs.changeColBounds(n - 1, 0.0, 0.0)
        columns = np.arange(n, dtype=np.int32)
        for column in range(2 * k):
            square, axis = divmod(column, 2)
            for sign in (1.0, -1.0):
                cost = np.zeros(n)
                cost[column] = sign
                self.highs.changeColsCost(n, columns, cost)
                outcome = self.run()
                if outcome is None:
                    continue
                current = tuple((b[0], b[1], b[2], b[3]) for b in bounds)
                bound = dual_bound(rows, outcome[2], self.spans(current), (column, sign))
                slot = 2 * axis + (0 if sign > 0 else 1)
                improved = (sign > 0 and bound > bounds[square][slot]) or (
                    sign < 0 and -bound < bounds[square][slot]
                )
                if improved:
                    bounds[square][slot] = bound if sign > 0 else -bound
                    if self.recorder is not None:
                        self.recorder.bound(column, sign, bound, rows, outcome[2])
                lo, hi = bounds[square][2 * axis], bounds[square][2 * axis + 1]
                if lo > hi:
                    if self.recorder is not None:
                        self.recorder.emptied("bounds")
                    return None
                self.highs.changeColBounds(column, lo, hi)
        boxes: list[Box] = []
        for index, b in enumerate(bounds):
            clipped = clip_to_box(self.pattern.polygons[index], (b[0], b[1], b[2], b[3]))
            if clipped is None:
                if self.recorder is not None:
                    self.recorder.emptied("cell")
                return None
            boxes.append(clipped)
        return tuple(boxes)

    # -- branching --------------------------------------------------------------------

    def children(self, node: Node, evaluation: Evaluation) -> tuple[str, list[Node]] | None:
        """Split the most violated disjunction, else the most relevant wide angle."""
        pattern, point, boxes = self.pattern, evaluation.point, evaluation.boxes
        widths = [hi - lo for lo, hi in node.angles]
        relevance = [0.0] * pattern.k
        chosen: tuple[float, int, PairTerm] | None = None
        if point is not None:
            for index, term in evaluation.terms:
                i, j = pattern.pairs[index]
                dx, dy = point[2 * j] - point[2 * i], point[2 * j + 1] - point[2 * i + 1]
                violation = min(r - (nx * dx + ny * dy) for nx, ny, r in term.planes)
                if violation <= VIOLATED:
                    continue
                relevance[i] += violation
                relevance[j] += violation
                if term.kind == "undecided" and (chosen is None or violation > chosen[0]):
                    chosen = (violation, index, term)
        if chosen is not None:
            _, index, term = chosen
            kids: list[Node] = []
            for option in term.options:
                windows = list(node.windows)
                windows[index] = option
                kids.append(
                    Node(
                        node.angles,
                        boxes,
                        tuple(windows),
                        node.depth + 1,
                        node.share / len(term.options),
                    )
                )
            return "pair", kids
        widest = max(widths)
        if widest < self.settings.floor:
            return None
        square = max(
            range(pattern.k),
            key=lambda s: (widths[s] >= self.settings.split_ratio * widest, relevance[s]),
        )
        lo, hi = node.angles[square]
        middle = 0.5 * (lo + hi)
        kids = []
        for part in ((lo, middle), (middle, hi)):
            angles = list(node.angles)
            angles[square] = part
            kids.append(
                Node(tuple(angles), boxes, node.windows, node.depth + 1, node.share / 2)
            )
        return "angle", kids


# ---------------------------------------------------------------------------
# The search
# ---------------------------------------------------------------------------


def pose_violation(pattern: Pattern, pose: Sequence[tuple[float, float, float]]) -> float:
    """Diagnostic, in floats: the worst pair penetration, cell or wall excursion of a pose.

    Near zero at a resolution-floor stop is evidence (not proof) that the pattern is
    feasible, so that a selector flag on it is false.
    """
    worst = 0.0
    cap = float(pattern.cap)
    for (x, y, theta), rows in zip(pose, pattern.lp_rows, strict=True):
        half = (abs(math.cos(theta)) + abs(math.sin(theta))) / 2
        worst = max(worst, half - x, x + half - cap, half - y, y + half - cap)
        worst = max(worst, *(a * x + b * y - c for a, b, c, _ in rows))
    for i, j in pattern.pairs:
        (xi, yi, ti), (xj, yj, tj) = pose[i], pose[j]
        alpha = tj - ti
        g = 0.5 + (abs(math.cos(alpha)) + abs(math.sin(alpha))) / 2
        reach = max(
            math.cos(theta + k * math.pi / 2) * (xj - xi)
            + math.sin(theta + k * math.pi / 2) * (yj - yi)
            for theta in (ti, tj)
            for k in range(4)
        )
        worst = max(worst, g - reach)
    return worst


def describe(node: Node, evaluation: Evaluation | None, pattern: Pattern) -> dict[str, Any]:
    boxes = evaluation.boxes if evaluation is not None and evaluation.boxes else node.boxes
    point = None if evaluation is None else evaluation.point
    witness = None
    if point is not None:
        witness = pose_violation(
            pattern,
            [
                (point[2 * s], point[2 * s + 1], 0.5 * (lo + hi))
                for s, (lo, hi) in enumerate(node.angles)
            ],
        )
    return {
        "depth": node.depth,
        "angles": [list(angle) for angle in node.angles],
        "angles_degrees": [
            [round(math.degrees(lo), 6), round(math.degrees(hi), 6)] for lo, hi in node.angles
        ],
        "max_angle_width": max(hi - lo for lo, hi in node.angles),
        "centre_boxes": {
            name: list(box) for name, box in zip(pattern.names, boxes, strict=True)
        },
        "windows": {
            f"{pattern.names[i]}|{pattern.names[j]}": list(window)
            for (i, j), window in zip(pattern.pairs, node.windows, strict=True)
            if window is not None
        },
        "lp_depth": None if evaluation is None else evaluation.lp_depth,
        "lp_point": None if evaluation is None else evaluation.point,
        "undecided_pairs": None
        if evaluation is None
        else sum(term.kind == "undecided" for _, term in evaluation.terms),
        "midpoint_pose_violation": witness,
    }


def separating_normals(
    pose: Sequence[tuple[float, float, float]], i: int, j: int
) -> list[tuple[float, float]]:
    """`(phi, margin)` for the eight normals of a pair at a pose (floats; diagnostic)."""
    (xi, yi, ti), (xj, yj, tj) = pose[i], pose[j]
    alpha = tj - ti
    g = 0.5 + (abs(math.cos(alpha)) + abs(math.sin(alpha))) / 2
    result: list[tuple[float, float]] = []
    for theta in (ti, tj):
        for k in range(4):
            phi = theta + k * math.pi / 2
            result.append((phi, math.cos(phi) * (xj - xi) + math.sin(phi) * (yj - yi) - g))
    return result


def in_window_float(phi: float, window: Iv | None, tolerance: float) -> bool:
    if window is None:
        return True
    return any(
        window[0] - tolerance <= phi + turns * 2 * math.pi <= window[1] + tolerance
        for turns in (-1, 0, 1)
    )


def node_holds(
    node: Node, pattern: Pattern, pose: Sequence[tuple[float, float, float]], tolerance: float
) -> bool:
    """Whether a pose lies in a node: angles, and a separating normal in every window."""
    if not all(lo <= t <= hi for (lo, hi), (_, _, t) in zip(node.angles, pose, strict=True)):
        return False
    for (i, j), window in zip(pattern.pairs, node.windows, strict=True):
        if window is None:
            continue
        normals = separating_normals(pose, i, j)
        if not any(
            margin >= -tolerance and in_window_float(phi, window, tolerance)
            for phi, margin in normals
        ):
            return False
    return True


def witness_path(
    pattern: Pattern,
    settings: Settings,
    pose: Sequence[tuple[float, float, float]],
    tolerance: float = 1e-9,
) -> dict[str, Any]:
    """Follow a known feasible pose from the root to the floor; nothing on it may close.

    A soundness control independent of the verdict: every node on the path must stay
    open, keep the pose inside its contracted centre boxes, and have a child holding it.
    """
    period = math.pi / 2
    theta0 = settings.theta0
    pose = [(x, y, theta0 + (t - theta0) % period) for x, y, t in pose]
    solver = Solver(pattern, settings)
    node = solver.root()
    steps = 0
    failure: str | None = None
    while True:
        steps += 1
        evaluation = solver.assess(node)
        if evaluation.pruned is not None:
            failure = f"closed by {evaluation.pruned} at depth {node.depth}"
            break
        outside = [
            pattern.names[s]
            for s, (box, (x, y, _)) in enumerate(zip(evaluation.boxes, pose, strict=True))
            if not (
                box[0] - tolerance <= x <= box[1] + tolerance
                and box[2] - tolerance <= y <= box[3] + tolerance
            )
        ]
        if outside:
            failure = f"contracted boxes lost {outside} at depth {node.depth}"
            break
        if node.depth >= MAX_DEPTH:
            break
        outcome = solver.children(node, evaluation)
        if outcome is None:
            break
        holding = [kid for kid in outcome[1] if node_holds(kid, pattern, pose, tolerance)]
        if not holding:
            failure = f"no {outcome[0]} child holds the pose at depth {node.depth}"
            break
        node = holding[0]
    return {
        "steps": steps,
        "final_depth": node.depth,
        "final_max_angle_width": max(hi - lo for lo, hi in node.angles),
        "passed": failure is None,
        "failure": failure,
    }


def selector_witness(
    names: Sequence[str], seed: int
) -> list[tuple[float, float, float]] | None:
    """A placement found by the selector's float search, if it finds one with no violation."""
    geometry = selector.cover_geometry(DEFAULT_DESIGN)
    cells = tuple(sorted(geometry.names.index(name) for name in names))
    verdict = selector.search(
        geometry, cells, selector.pattern_rng(seed, selector.mask_of(cells)), selector.Budget()
    )
    if not verdict.feasible or verdict.violation > 0.0:
        return None
    rows = {geometry.names[cell]: row for row, cell in enumerate(cells)}
    return [
        (
            float(verdict.pose[rows[name], 0]),
            float(verdict.pose[rows[name], 1]),
            float(verdict.pose[rows[name], 2]),
        )
        for name in names
    ]


def endpoint_witness(names: Sequence[str]) -> list[tuple[float, float, float]]:
    """The endpoint's pose (the selector's embedding) on the named cells of its state."""
    endpoint = selector.endpoint_pose()
    cells = [cell.name for cell in cover.build_cover(cover.DESIGNS[DEFAULT_DESIGN])]
    rows = {cells[cell]: row for row, cell in enumerate(endpoint["cells"])}
    pose = endpoint["pose"]
    return [
        (float(pose[rows[name], 0]), float(pose[rows[name], 1]), float(pose[rows[name], 2]))
        for name in names
    ]


def estimate(pattern: Pattern, settings: Settings, dives: int, seed: int = 1) -> dict[str, Any]:
    """Knuth's estimate of the search tree's size, from random root-to-leaf dives.

    A dive takes a uniformly random child at each node; with branching factors
    `b_0, b_1, ...` along it, `1 + b_0 + b_0 b_1 + ...` is an unbiased estimate of the
    node count, so the mean over dives estimates the size and, with the measured
    seconds per node, the wall cost of a full run. A dive that reaches the resolution
    floor has found a near-witness: the run would not close there.
    """
    rng = random.Random(seed)
    solver = Solver(pattern, settings)
    started = time.perf_counter()
    sizes: list[float] = []
    depths: list[int] = []
    floor_hits = 0
    evaluated = 0
    for _ in range(dives):
        node, weight, size = solver.root(), 1.0, 1.0
        while True:
            evaluated += 1
            evaluation = solver.assess(node)
            if evaluation.pruned is not None:
                break
            outcome = solver.children(node, evaluation) if node.depth < MAX_DEPTH else None
            if outcome is None:
                floor_hits += 1
                break
            kids = outcome[1]
            weight *= len(kids)
            size += weight
            node = kids[rng.randrange(len(kids))]
        sizes.append(size)
        depths.append(node.depth)
    seconds = time.perf_counter() - started
    per_node = seconds / max(evaluated, 1)
    mean = sum(sizes) / len(sizes)
    ordered = sorted(sizes)
    return {
        "dives": dives,
        "seed": seed,
        "floor_hits": floor_hits,
        "estimated_nodes_mean": mean,
        "estimated_nodes_median": ordered[len(ordered) // 2],
        "estimated_nodes_max": ordered[-1],
        "mean_leaf_depth": sum(depths) / len(depths),
        "seconds_per_node": per_node,
        "estimated_wall_seconds": mean * per_node,
        "seconds": round(seconds, 3),
    }


# ---------------------------------------------------------------------------
# Saved certificates
# ---------------------------------------------------------------------------

CERTIFICATE_SCHEMA = "n17-subpattern-bb-certificate/v1"
TAYLOR_SCHEMA = "n17-subpattern-bb-certificate/v2"


def rational(value: float | Fraction) -> str:
    """An exact rational as "p/q" in lowest terms (a float is a dyadic rational)."""
    if isinstance(value, Fraction):
        return f"{value.numerator}/{value.denominator}"
    numerator, denominator = value.as_integer_ratio()
    return f"{numerator}/{denominator}"


def canonical_bytes(document: Any) -> bytes:
    return json.dumps(
        document, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False
    ).encode("ascii")


def write_named(directory: Path, document: Any) -> str:
    """Write gzipped canonical JSON named by the SHA-256 of its uncompressed bytes."""
    data = canonical_bytes(document)
    name = hashlib.sha256(data).hexdigest()
    (directory / f"{name}.json.gz").write_bytes(gzip.compress(data, mtime=0))
    return name


def read_named(directory: Path, name: str) -> Any:
    """Read a saved document, refusing one whose bytes do not hash to its name."""
    data = gzip.decompress((directory / f"{name}.json.gz").read_bytes())
    if hashlib.sha256(data).hexdigest() != name:
        raise ValueError(f"{name}: content does not match its name")
    return json.loads(data)


def boxes_record(boxes: Sequence[Box]) -> list[list[str]]:
    return [[rational(value) for value in box] for box in boxes]


CERTIFICATE_README = """\
n17 sub-pattern branch-and-bound certificate (schema n17-subpattern-bb-certificate/v1)
Written by packing/devtools/pilot_n17_subpattern_bb.py --save-certificate.

FILES
Every *.json.gz file is gzip of canonical JSON (keys sorted, separators "," and ":",
ASCII) and is named by the SHA-256 of its uncompressed bytes. The manifest names the
enclosure table ("trig") and the node chunks ("chunks", in processing order); its
"summary" gives the verdict, whether the tree is complete, and the node and leaf counts.
Every number a check uses exactly is a string "p/q" in lowest terms. A value written from
a binary64 float is that float's exact value. Integers (indices, signs) are JSON ints.

CLAIM
U = header.cap. Cell s is header.cells[s], a closed convex polygon with vertices listed
counterclockwise; edge e runs from vertex e to vertex e+1 (cyclically). The claim: no k
unit squares, square s centred in cell s, at any angles, all inside [0,U]^2, have
pairwise disjoint interiors. Angles are taken modulo pi/2 in header.root_angles, a closed
interval of width greater than pi/2. M_k = header.half_pi_multiples[k] is an enclosure
[lo, hi] of k pi/2; "pi/2-lower" is M_1 lo.

For a pair p, (i, j) = header.pairs[p] and d = c_j - c_i. The squares are disjoint iff
n(phi) . d >= g for some phi in {theta_i + k pi/2, theta_j + k pi/2 : k = 0..3}, with
n(phi) = (cos phi, sin phi), g = 1/2 + h(theta_j - theta_i), h(a) = (|cos a| + |sin a|)/2.

ENCLOSURES
trig[t] = [cos_lo, cos_hi, sin_lo, sin_hi, nx, ny] for each angle t (a key "p/q"):
cos t and sin t lie in the two intervals (mpmath.iv at 120 bits, rounded outward to
binary64); (nx, ny) is the float normal the planes at t use (any vector would do: the
check charges its distance to the enclosure). A reader can confirm the enclosures with
any rigorous sin and cos.

TREE
A node record: id, parent (null at the root), angles (per square [lo, hi]), windows
([p, lo, hi]: pair p is separated along a normal whose angle, modulo 2 pi, is in
[lo, hi]), rounds, closed (a reason, or null), and for an open node "split" and "final".
The node's region: angles in its intervals, each windowed pair separated in its window,
centres in its inherited boxes (header.root_boxes at the root, else the parent's final).
  T1 The root has header.root_angles and no windows.
  T2 A node with closed null has a split, and its children (records with parent = id):
     "angle" [s, a]: two children equal to the node except square s's interval, which is
     [lo, a] and [a, hi], with lo <= a <= hi.
     "pair" [p, W]: one child per window in W, equal to the node except pair p's window,
     which is that window; covering is checked by P4.
  T3 A node with closed not null has no children; summary.complete is true and every
     record is closed or split. Then every pose of the root lies in a closed leaf.

ROUNDS (a node's rounds in order; round r relaxes over boxes B_r = "boxes")
Boxes are [xl, xh, yl, yh] per square. A reader may keep its own exact boxes and only
check that each recorded box contains them; every check below gets easier on smaller
boxes, and every recomputed quantity below is at least as tight in exact arithmetic as
the outward float it replaces.
  B1 Round 0: from the inherited boxes, for square s with angle [a, b]: h_lo = 1/2 if
     b - a >= pi/2-lower or [a, b] meets some M_k; otherwise the larger of 1/2 and
     min over t in {a, b} of (|cos t| lower + |sin t| lower)/2 from trig (h is concave
     between multiples of pi/2). Intersect with [h_lo, U - h_lo]^2, then with the cell
     (exact clipping), take the bounding box; B_0 contains it. closed "cell" with no
     rounds means this is empty for some square.
  B2 "next" is B_{r+1}: the box after the round's "bounds", clipped to the cells as in B1.

PAIRS IN A ROUND (for each pair listed in the round's "pairs")
Dx = [xj_lo - xi_hi, xj_hi - xi_lo] and Dy likewise from B_r. With angle intervals
[ai, bi] and [aj, bj]:
  P1 g_lo = 1 if aj <= bi and ai <= bj, or bj - ai - (aj - bi) >= pi/2-lower, or
     [aj - bi, bj - ai] meets some M_k. Otherwise g_lo = max(1, 1/2 + min of h at
     aj - bi and at bj - ai), each h bounded below as in B1 from enclosures of cos and
     sin of the difference: cos(p - q) = cos p cos q + sin p sin q and
     sin(p - q) = sin p cos q - cos p sin q in interval arithmetic on trig.
  P2 "pairs"[p] lists pieces [lo, hi, m] with lo <= m <= hi. For each family [a, b] in
     {[ai, bi], [aj, bj]} and k = 0..3, the set {t + k pi/2 : t in [a, b]} meet the
     pair's window (modulo 2 pi; no window means all angles) lies in the union of the
     pieces' [lo, hi] (modulo 2 pi).
  P3 Planes. eps(t) = max(cos_hi - cos_lo, sin_hi - sin_lo) and
     E = max|Dx| + max|Dy|. A plane is nbar . d >= r with nbar = (nx, ny) of trig at its
     angle. If hi - lo < pi/2-lower the piece has three planes, at lo, hi and m, with
     base right sides g_lo, g_lo and g_lo (1 - x^2/2), x = max(m - lo, hi - m), and
     r = base - eps(angle) E. Lemma (module docstring): every d with n(phi) . d >= g for
     some phi in [lo, hi] satisfies one of n(lo) . d >= g, n(hi) . d >= g,
     n(m) . d >= g cos x. Otherwise the piece has one plane at m with
     r = g_lo - 2 tau (S + tau D) - eps(m) E, tau = max(m - lo, hi - m)/2,
     S >= max over the d-box and the enclosure at m of |-sin(m) dx + cos(m) dy|,
     D >= max |d| over the d-box. A plane is impossible when max over the d-box of
     nbar . d < r, or (three-plane case) when max over the d-box and the enclosure at
     its angle of n . d < base.
  P4 For a "pair" split [p, W] (made on the last round): every piece of pair p lies in a
     window of W (modulo 2 pi) or has every plane impossible.

CLOSURES AND ROWS
  C1 "closed_pair" [p, "disc"]: max |d|^2 over the d-box < 1. [p, "pair"]: every plane
     of every piece of p is impossible.
  C2 Row ["c", s, e]: a x_s + b y_s <= c for edge e of cell s from (x0, y0) to (x1, y1),
     a = y1 - y0, b = x0 - x1, c = a x0 + b y0. Row ["u", t]: cuts[t] = [p, ux, uy, v]
     reads ux (x_j - x_i) + uy (y_j - y_i) >= v, that is
     ux x_i + uy y_i - ux x_j - uy y_j <= -v. It is valid when v <= min over every
     possible plane of p (P3) of min over the d-box meet the plane of u . d.
  C3 closed "lp": the last round's "farkas" [[row, y], ...] with y >= 0 satisfies
     min over z in B_r of sum y (a_row . z - b_row) > 0, so the round's region is empty.
  C4 "bounds", in order: [col, sign, value, [[row, y], ...]], col = 2 s + axis (axis 0
     is x). sign z_col >= value holds when value <= min over the current box of
     (sign e_col + sum y a_row) . z - sum y b_row. Then the current box's lower bound
     (sign 1) becomes value, or its upper bound (sign -1) becomes -value. The current box
     starts as B_r.
  C5 closed "obbt": "emptied" is "bounds" (some lower bound exceeds its upper bound) or
     "cell" (a tightened box misses its cell).
"""


TAYLOR_README = """
TAYLOR MODE (schema n17-subpattern-bb-certificate/v2; header.settings.taylor is true)
The angles enter the LP. K = header.settings.taylor_k must be at least sqrt(2)/4.
  X1 Each node has "taylor": {"centres": [c_s]}. Column 2k + s of every row is the
     offset t_s = theta_s - c_s, ranging over T_s = [lo_s - c_s, hi_s - c_s]; the Farkas
     and bound checks (C3, C4) take their minimum over these ranges too.
  X2 A gap line of pair p = (i, j) for signs (s1, s2) and slope b: with
     alpha0 = c_j - c_i, A = [T_j lo - T_i hi, T_j hi - T_i lo], rho = max(-A lo, A hi),
     f = (s1 cos + s2 sin)/2 and f' = (s2 cos - s1 sin)/2 at alpha0,
     a = 1/2 + f - |f' - b| rho - K rho^2 (each term bounded below). Then
     g >= a + b (t_j - t_i) at every pose of the node, since h >= f for every sign pair
     and |f''| = |f| <= sqrt(2)/2.
  X3 Every possible plane of P3 also reads nbar . d >= c g - o at the pose's own gap g:
     c = 1 and o = eps E for an end plane, c = 1 - x^2/2 and o = eps E for the chord
     plane, c = 1 and o = 2 tau (S + tau D) + eps E for a wide piece's plane.
  X4 A cut with eight fields [p, ux, uy, v, w, s1, s2, b] is a Taylor cut:
     ux (x_j - x_i) + uy (y_j - y_i) - w (t_j - t_i) >= v. It is valid when v <= the
     least, over every possible plane of p, of u . d - w t over d in the d-box, t in A
     and nbar . d >= c (a + b t) - o, with a from X2 at (s1, s2, b). Each least value is
     a three-variable LP with one constraint: the largest of its Lagrangian bounds at
     lambda = 0 and at the lambdas cancelling one coefficient. The pilot writes one only
     when a - |b| rho > 0, so exact recomputation only shrinks the planes.
  X5 A row ["w", t] reads walls[t] = [s, axis, side, s1, s2, b, a]: a wall line of
     square s about c_s with constant 0, valid when a <= f - |f' - b| rho_s - K rho_s^2
     (X2 with f, f' at c_s and rho_s = max(-T_s lo, T_s hi)). With z = x_s (axis 0) or
     y_s (axis 1), side 1 is -z + b t_s <= -a (z >= h >= a + b t_s) and side -1 is
     z + b t_s <= U - a.
"""


class Recorder:
    """Writes what an independent reader needs to re-verify every closure of a run.

    One record per node, in processing order, in chunks; the format and the checks are in
    the README this writes beside them (`CERTIFICATE_README`). Passive: it reads what the
    solver computed and changes nothing the search does.
    """

    def __init__(self, directory: Path, solver: Solver, chunk_nodes: int = 500) -> None:
        global TRIG_USED  # noqa: PLW0603 - the recording window of the enclosure cache
        TRIG_USED = set()
        directory.mkdir(parents=True, exist_ok=True)
        self.directory = directory
        self.solver = solver
        self.chunk_nodes = chunk_nodes
        self.chunks: list[str] = []
        self.buffer: list[dict[str, Any]] = []
        self.cell_refs: dict[int, list[Any]] = {}
        position = 0
        for square, rows in enumerate(solver.pattern.rows):
            for edge in range(len(rows)):
                self.cell_refs[id(solver.cell_rows[position])] = ["c", square, edge]
                position += 1
        self.node: dict[str, Any] = {}
        self.rounds: list[tuple[dict[str, Any], dict[int, PairTerm], set[int]]] = []
        self.terms: dict[int, PairTerm] = {}
        self.cut_index: dict[tuple[Any, ...], int] = {}

    # -- per node and per round ----------------------------------------------------------

    def begin_node(self, ident: int, parent: int | None, node: Node) -> None:
        self.node = {
            "id": ident,
            "parent": parent,
            "angles": [[rational(lo), rational(hi)] for lo, hi in node.angles],
            "windows": [
                [index, rational(window[0]), rational(window[1])]
                for index, window in enumerate(node.windows)
                if window is not None
            ],
        }
        if self.solver.settings.taylor:
            self.node["taylor"] = {
                "centres": [rational(0.5 * (lo + hi)) for lo, hi in node.angles]
            }
        self.rounds = []

    def begin_round(self, boxes: Sequence[Box]) -> None:
        self.terms = {}
        self.cut_index = {}
        record: dict[str, Any] = {"boxes": boxes_record(boxes), "cuts": []}
        self.rounds.append((record, self.terms, set()))

    def ref(self, row: Row) -> list[Any]:
        if row.record is not None:
            return self.taylor_ref(row.record)
        if row.owner < 0:
            return self.cell_refs[id(row)]
        record, _, referenced = self.rounds[-1]
        key = (row.owner, row.values[0], row.values[1], row.rhs)
        index = self.cut_index.get(key)
        if index is None:
            index = len(record["cuts"])
            self.cut_index[key] = index
            record["cuts"].append(
                [
                    row.owner,
                    rational(row.values[0]),
                    rational(row.values[1]),
                    rational(-row.rhs),
                ]
            )
            referenced.add(row.owner)
        return ["u", index]

    def taylor_ref(self, entry: tuple[Any, ...]) -> list[Any]:
        """A Taylor cut (into `cuts`, eight fields) or a wall row (into `walls`)."""
        record, _, referenced = self.rounds[-1]
        index = self.cut_index.get(entry)
        if index is not None:
            return [entry[0], index]
        if entry[0] == "u":
            _, pair, ux, uy, v, w, s1, s2, b = entry
            index = len(record["cuts"])
            record["cuts"].append(
                [
                    pair,
                    rational(ux),
                    rational(uy),
                    rational(v),
                    rational(w),
                    s1,
                    s2,
                    rational(b),
                ]
            )
            referenced.add(pair)
        else:
            _, square, axis, side, s1, s2, b, a = entry
            walls = record.setdefault("walls", [])
            index = len(walls)
            walls.append([square, axis, side, s1, s2, rational(b), rational(a)])
        self.cut_index[entry] = index
        return [entry[0], index]

    def multipliers(self, rows: Sequence[Row], duals: Sequence[float]) -> list[list[Any]]:
        # Exactly the verified multipliers `dual_bound` applies: `weight / norm`.
        return [
            [self.ref(row), rational(weight / row.norm)]
            for row, weight in zip(rows, duals, strict=True)
            if weight > 0.0
        ]

    def farkas(self, rows: Sequence[Row], duals: Sequence[float]) -> None:
        self.rounds[-1][0]["farkas"] = self.multipliers(rows, duals)

    def bound(
        self,
        column: int,
        sign: float,
        value: float,
        rows: Sequence[Row],
        duals: Sequence[float],
    ) -> None:
        self.rounds[-1][0].setdefault("bounds", []).append(
            [column, 1 if sign > 0 else -1, rational(value), self.multipliers(rows, duals)]
        )

    def emptied(self, how: str) -> None:
        self.rounds[-1][0]["emptied"] = how

    def tightened(self, boxes: Sequence[Box]) -> None:
        self.rounds[-1][0]["next"] = boxes_record(boxes)

    def closed_by_pair(self, index: int, kind: str) -> None:
        record, _, referenced = self.rounds[-1]
        record["closed_pair"] = [index, kind]
        referenced.add(index)

    def end_node(
        self, closed: str | None, split: dict[str, Any] | None, final: Sequence[Box]
    ) -> None:
        rounds: list[dict[str, Any]] = []
        for record, terms, referenced in self.rounds:
            record["pairs"] = {
                str(index): [
                    [rational(lo), rational(hi), rational(m)]
                    for lo, hi, m in terms[index].pieces
                ]
                for index in sorted(referenced)
            }
            rounds.append(record)
        self.node["rounds"] = rounds
        self.node["closed"] = closed
        if split is not None:
            self.node["split"] = split
            self.node["final"] = boxes_record(final)
        self.buffer.append(self.node)
        if len(self.buffer) >= self.chunk_nodes:
            self.flush()

    def split_record(self, node: Node, how: str, kids: Sequence[Node]) -> dict[str, Any]:
        if how == "angle":
            square = next(
                s for s in range(len(node.angles)) if kids[0].angles[s] != node.angles[s]
            )
            return {"angle": [square, rational(kids[0].angles[square][1])]}
        index = next(
            i for i in range(len(node.windows)) if kids[0].windows[i] != node.windows[i]
        )
        self.rounds[-1][2].add(index)
        windows: list[list[str]] = []
        for kid in kids:
            window = kid.windows[index]
            assert window is not None
            windows.append([rational(window[0]), rational(window[1])])
        return {"pair": [index, windows]}

    # -- files -------------------------------------------------------------------------

    def flush(self) -> None:
        if self.buffer:
            self.chunks.append(write_named(self.directory, {"nodes": self.buffer}))
            self.buffer = []

    def close(self, summary: dict[str, Any]) -> str:
        """Write the remaining nodes, the enclosure table, the manifest and the README."""
        global TRIG_USED  # the recording window of the enclosure cache closes here
        self.flush()
        used, TRIG_USED = TRIG_USED or set(), None
        solver, pattern = self.solver, self.solver.pattern
        trig = write_named(
            self.directory,
            {
                "trig": {
                    rational(theta): [
                        rational(c[0]),
                        rational(c[1]),
                        rational(s[0]),
                        rational(s[1]),
                        rational(0.5 * (c[0] + c[1])),
                        rational(0.5 * (s[0] + s[1])),
                    ]
                    for theta, (c, s) in sorted(TRIG.items())
                    if theta in used
                }
            },
        )
        root = solver.root()
        header = {
            "pattern": list(pattern.names),
            "cells": [
                [[rational(x), rational(y)] for x, y in cover.convex_hull(list(polygon))]
                for polygon in pattern.polygons
            ],
            "cap": rational(pattern.cap),
            "pairs": [list(pair) for pair in pattern.pairs],
            "root_angles": [[rational(lo), rational(hi)] for lo, hi in root.angles],
            "root_boxes": boxes_record(root.boxes),
            "half_pi_multiples": {
                str(k): [rational(v[0]), rational(v[1])]
                for k, v in sorted(HALF_PI_MULTIPLES.items())
            },
            "settings": {
                "theta0": rational(solver.settings.theta0),
                "split_ratio": solver.settings.split_ratio,
                "obbt_rounds": solver.settings.obbt_rounds,
                "obbt_repeat": solver.settings.obbt_repeat,
                "merge_gap": solver.settings.merge_gap,
                "floor": solver.settings.floor,
            },
            "module_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        }
        taylor = solver.settings.taylor
        if taylor:
            # Only in Taylor mode, so that an interval certificate's bytes do not change.
            header["settings"]["taylor"] = True
            header["settings"]["taylor_k"] = rational(TAYLOR_K)
        manifest = write_named(
            self.directory,
            {
                "schema": TAYLOR_SCHEMA if taylor else CERTIFICATE_SCHEMA,
                "header": header,
                "trig": trig,
                "chunks": self.chunks,
                "summary": summary,
            },
        )
        readme = CERTIFICATE_README + (TAYLOR_README if taylor else "")
        (self.directory / "README.txt").write_text(
            readme + f"\nThis certificate's manifest: {manifest}.json.gz\n",
            encoding="utf-8",
        )
        return manifest


def load_certificate(directory: Path, manifest: str) -> dict[str, Any]:
    """The manifest, the enclosure table and every node record, each hash-checked."""
    document = read_named(directory, manifest)
    nodes: list[dict[str, Any]] = []
    for chunk in document["chunks"]:
        nodes.extend(read_named(directory, chunk)["nodes"])
    return {
        "manifest": document,
        "trig": read_named(directory, document["trig"])["trig"],
        "nodes": nodes,
    }


def search(
    pattern: Pattern,
    settings: Settings,
    *,
    progress: bool = False,
    certificate: Path | None = None,
) -> dict[str, Any]:
    wall, cpu = time.perf_counter(), time.process_time()
    solver = Solver(pattern, settings)
    recorder = None if certificate is None else Recorder(certificate, solver)
    solver.recorder = recorder
    stack: list[tuple[Node, int | None]] = [(solver.root(), None)]
    nodes = leaves = max_depth = 0
    reasons: dict[str, int] = {}
    branches: dict[str, int] = {}
    farkas_failures = 0
    closed = 0.0
    blame: dict[str, dict[str, float]] = {}
    smallest: tuple[float, dict[str, Any]] | None = None
    verdict = "certified-infeasible"
    stop: dict[str, Any] | None = None
    next_report = 10.0
    while stack:
        elapsed = time.perf_counter() - wall
        if elapsed > settings.max_seconds or (
            settings.max_nodes is not None and nodes >= settings.max_nodes
        ):
            verdict = "unresolved-at-budget"
            break
        if progress and elapsed > next_report:
            next_report += 30.0
            print(
                json.dumps(
                    {
                        "seconds": round(elapsed, 1),
                        "nodes": nodes,
                        "leaves": leaves,
                        "open": len(stack),
                        "max_depth": max_depth,
                        "closed_share": closed,
                        "reasons": reasons,
                        "smallest_width": None if smallest is None else smallest[0],
                    }
                ),
                flush=True,
            )
        node, parent = stack.pop()
        ident = nodes
        nodes += 1
        max_depth = max(max_depth, node.depth)
        if recorder is not None:
            recorder.begin_node(ident, parent, node)
        evaluation = solver.assess(node)
        farkas_failures += int(evaluation.farkas_failed)
        if evaluation.pruned is not None:
            leaves += 1
            closed += node.share
            tally = blame.setdefault(evaluation.pruned, {})
            for owner, share in evaluation.blame.items():
                label = (
                    "cells"
                    if owner < 0
                    else "|".join(pattern.names[s] for s in pattern.pairs[owner])
                )
                tally[label] = tally.get(label, 0.0) + share
            reasons[evaluation.pruned] = reasons.get(evaluation.pruned, 0) + 1
            if recorder is not None:
                recorder.end_node(evaluation.pruned, None, evaluation.boxes)
            continue
        width = max(hi - lo for lo, hi in node.angles)
        if smallest is None or width < smallest[0]:
            smallest = (width, describe(node, evaluation, pattern))
        if node.depth >= MAX_DEPTH:
            verdict = "unresolved-at-depth-cap"
            stop = describe(node, evaluation, pattern)
            break
        outcome = solver.children(node, evaluation)
        if outcome is None:
            verdict = "unresolved-at-resolution-floor"
            stop = describe(node, evaluation, pattern)
            break
        how, kids = outcome
        branches[how] = branches.get(how, 0) + 1
        if recorder is not None:
            split = recorder.split_record(node, how, kids)
            recorder.end_node(None, split, evaluation.boxes)
        stack.extend((kid, ident) for kid in reversed(kids))
    record: dict[str, Any] = {
        "verdict": verdict,
        "nodes": nodes,
        "leaves": leaves,
        "open_at_stop": len(stack) if verdict != "certified-infeasible" else 0,
        "max_depth": max_depth,
        "prune_reasons": dict(sorted(reasons.items())),
        "branches": dict(sorted(branches.items())),
        "farkas_failures": farkas_failures,
        "closed_tree_share": closed,
        "closures_by_pair": {
            reason: dict(
                sorted(((k, round(v, 3)) for k, v in tally.items()), key=lambda kv: -kv[1])[:8]
            )
            for reason, tally in sorted(blame.items())
        },
        "wall_seconds": round(time.perf_counter() - wall, 3),
        "cpu_seconds": round(time.process_time() - cpu, 3),
    }
    if verdict != "certified-infeasible":
        record["stopped_at"] = stop
        record["smallest_unresolved"] = None if smallest is None else smallest[1]
    if recorder is not None:
        record["certificate_manifest"] = recorder.close(
            {
                "verdict": verdict,
                "complete": verdict == "certified-infeasible",
                "nodes": nodes,
                "leaves": leaves,
            }
        )
    return record


# ---------------------------------------------------------------------------
# Command line
# ---------------------------------------------------------------------------


def pattern_from_receipt(path: Path, index: int) -> list[str]:
    receipt = json.loads(path.read_text(encoding="utf-8"))
    return list(receipt["certification_priority"][index]["cells"])


def endpoint_cells(rows: Sequence[int]) -> list[str]:
    """Cells of the endpoint's own state (the selector's embedding), by row."""
    endpoint = selector.endpoint_pose()
    names = [cell.name for cell in cover.build_cover(cover.DESIGNS[DEFAULT_DESIGN])]
    return [names[endpoint["cells"][row]] for row in rows]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--cells", help="comma-separated cell names")
    source.add_argument("--receipt", type=Path, help="selector receipt (with --index)")
    source.add_argument(
        "--endpoint-rows", help="comma-separated rows of the endpoint's own state (control)"
    )
    parser.add_argument("--index", type=int, default=0, help="certification_priority index")
    parser.add_argument("--label", default="")
    parser.add_argument("--control", action="store_true", help="must never certify")
    parser.add_argument("--max-seconds", type=float, default=600.0)
    parser.add_argument("--max-nodes", type=int, default=None)
    parser.add_argument("--theta0", type=float, default=DEFAULT_THETA0)
    parser.add_argument("--floor", type=float, default=DEFAULT_FLOOR)
    parser.add_argument("--merge-gap", type=float, default=0.0)
    parser.add_argument("--split-ratio", type=float, default=DEFAULT_SPLIT_RATIO)
    parser.add_argument("--obbt-rounds", type=int, default=3)
    parser.add_argument(
        "--taylor",
        action="store_true",
        help="first-order Taylor rows for the gap and wall supports (angles enter the LP)",
    )
    parser.add_argument("--seed", type=int, default=1, help="seed of the --estimate dives")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--progress", action="store_true")
    parser.add_argument(
        "--estimate", type=int, default=0, help="Knuth dives instead of a full search"
    )
    parser.add_argument(
        "--save-certificate",
        type=Path,
        default=None,
        metavar="DIR",
        help="write every closure, the tree and the enclosures for an independent check",
    )
    parser.add_argument(
        "--witness-selector",
        type=int,
        default=None,
        metavar="SEED",
        help="also follow a zero-violation placement found by the selector's search",
    )
    parser.add_argument(
        "--witness-endpoint",
        action="store_true",
        help="also follow the endpoint's own pose from the root (a control on its state)",
    )
    args = parser.parse_args(argv)
    control = args.control
    if args.cells:
        names = args.cells.split(",")
        origin: dict[str, Any] = {"cells": names}
    elif args.receipt:
        names = pattern_from_receipt(args.receipt, args.index)
        origin = {"receipt": str(args.receipt), "index": args.index}
    else:
        rows = [int(row) for row in args.endpoint_rows.split(",")]
        names = endpoint_cells(rows)
        origin = {"endpoint_rows": rows}
        control = True
    pattern = cover_pattern(names)
    settings = Settings(
        theta0=args.theta0,
        floor=args.floor,
        merge_gap=args.merge_gap,
        max_seconds=args.max_seconds,
        max_nodes=args.max_nodes,
        split_ratio=args.split_ratio,
        obbt_rounds=args.obbt_rounds,
        taylor=args.taylor,
    )
    witness = None
    if args.witness_endpoint:
        witness = witness_path(pattern, settings, endpoint_witness(pattern.names))
    elif args.witness_selector is not None:
        found = selector_witness(pattern.names, args.witness_selector)
        witness = (
            {"passed": True, "failure": None, "note": "the selector found no exact placement"}
            if found is None
            else {"pose": found, **witness_path(pattern, settings, found)}
        )
    if witness is not None:
        print(json.dumps({"witness_path": witness}), flush=True)
    result = (
        {"verdict": "estimate-only", **estimate(pattern, settings, args.estimate, args.seed)}
        if args.estimate
        else search(
            pattern, settings, progress=args.progress, certificate=args.save_certificate
        )
    )
    receipt: dict[str, Any] = {
        "schema": SCHEMA,
        "status": STATUS,
        "label": args.label,
        "design": DEFAULT_DESIGN,
        "cap": str(cover.U),
        "pattern": list(pattern.names),
        "source": origin,
        "control": control,
        "parameters": {
            "theta0": settings.theta0,
            "floor": settings.floor,
            "merge_gap": settings.merge_gap,
            "max_seconds": settings.max_seconds,
            "max_nodes": settings.max_nodes,
            "split_ratio": settings.split_ratio,
            "obbt_rounds": settings.obbt_rounds,
            "taylor": settings.taylor,
        },
        "module_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        **result,
    }
    if witness is not None:
        receipt["witness_path"] = witness
    if control and result["verdict"] == "certified-infeasible":
        receipt["soundness_failure"] = "a control pattern was certified"
    if witness is not None and not witness["passed"]:
        receipt["soundness_failure"] = f"witness path: {witness['failure']}"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    keys = (
        "label",
        "pattern",
        "verdict",
        "nodes",
        "leaves",
        "max_depth",
        "wall_seconds",
        "estimated_nodes_mean",
        "estimated_wall_seconds",
        "floor_hits",
    )
    print(json.dumps({key: receipt[key] for key in keys if key in receipt}))
    return 1 if "soundness_failure" in receipt else 0


if __name__ == "__main__":
    raise SystemExit(main())
