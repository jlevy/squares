"""A fixed-angle separating-axis cell tree with exact leaf certificates (X-046 rung 0).

The family ``F_{a,m}[l, r]``: ``a`` unit squares with actual orientation 0 and ``m`` unit
squares sharing one orientation ``theta`` modulo quarter turns, with the half-tangent
``t = tan(theta/2)`` in a closed rational box ``[l, r]`` inside ``[0, 1)``.  Centres and the
container side ``S`` are free; the container is ``[0, S]^2``.  H-236 is ``F_{6,5}`` on a box
of half-width ``10^-6`` around Trump's half-tangent.

**Relaxation.**  Each tilted square is replaced by its *core*: the square of rational side
``lam`` at the rational half-tangent ``(l + r)/2``, with ``lam`` the largest value, rounded
down to ``CORE_DIGITS`` decimals, whose corners stay inside the rotated unit square at both
endpoint angles.  `core_in_window` then proves exactly that every core vertex lies in the
unit square at *every* angle of the window: each edge functional ``u(phi) . v`` is
``|v| cos(phi - arg v)``, so its maximum over the swept normal window is at an endpoint
unless ``arg v`` lies inside the window, in which case the check is ``|v|^2 <= 1/4``.
The core is convex, so it lies in every square of the window.  This is the inscribed
square of X-046's rotational core (conv of its four corners) rather than the octagon: it
loses first order along the whole edge instead of only at the corners, but it has four
edge normals instead of eight, which halves every tilted pair's branching.  At rung 0's
window, about ``3.5e-6`` radians, the extra loss is below ``1e-6`` in side.

Any packing of the family at an angle in the box is therefore a packing of the cores at
the same centres and side, and a lower bound on core packings is a lower bound on the
family.

**Cells.**  Two convex polygons with disjoint interiors are separated by a line parallel
to an edge of one of them, so a pair ``(i, j)`` has finitely many candidate axes: the
union of the two cores' edge normals, both centrally symmetric.  Choosing axis ``n``
(pointing from ``i`` to ``j``) imposes ``n . (c_j - c_i) >= h_i(n) + h_j(n)``, with ``h``
the support function.  A node fixes axes for some pairs; its LP minimizes ``S`` subject
to containment, the fixed pairs and the symmetry rows, and is a relaxation of every core
packing in the node.  Branching on a pair makes one child per candidate axis, so the
children cover the node.  The pair branched is the one most overlapped at the node's LP
optimum (the smallest overlap over its candidate axes, maximized over pairs).

**Symmetry.**  Two families of rows, both optional and both declared in the header:

- *Quadrant.*  Let ``g`` be the sum over one declared class of ``c_i - (S/2, S/2)``.  A
  quarter turn about the container centre maps a family packing to a family packing
  (``theta + pi/2`` is ``theta`` modulo quarter turns) and turns ``g`` by ``pi/2``; of the
  four turns, at least one puts ``g`` in the closed quadrant ``g_x >= 0, g_y >= 0``.  Rows:
  ``sum_class x_i - (m/2) S >= 0`` and the same in ``y``.
- *Order.*  Squares of one class are the same set up to translation, so relabelling
  within a class maps packings to packings.  Sorting each class by
  ``x + ORDER_EPSILON * y`` gives the rows ``l(c_{i+1}) - l(c_i) >= 0``.

The class sums are invariant under relabelling, so turning first and sorting second
satisfies both families at once: no packing is lost, only relabelled or turned.

**Leaves.**  Every LP has the variable box ``[0, VARIABLE_CAP]``; a packing with
``S <= VARIABLE_CAP`` has every centre inside it.  For a multiplier vector ``y >= 0``,
every point of the box satisfying the rows ``A z >= b`` obeys
``c . z >= b . y + sum_k min over [l_k, u_k] of (c - A^T y)_k z_k`` -- the bound is exact
for any rational ``y``, so HiGHS proposes ``y`` in floating point and the bound is then
evaluated in `Fraction` arithmetic.  The multipliers are written as the decimal strings
the evaluation read, so the certificate is exactly the rational vector that was checked.

- ``c``: a dual bound on ``S`` strictly above the target's upper end.
- ``f``: a Farkas vector, ``b . y + sum_k min_box (-A^T y)_k z_k > 0``: the node's rows
  have no solution in the box.
- ``t``: an equality-degenerate leaf.  With ``S`` capped at the target's upper end, every
  centre coordinate is bounded above and below by a certified dual bound, and the whole
  enclosure lies strictly within the declared radius of the declared labelled image.  For
  H-236 the image is a labelled Trump image and the radius is BC-240's ``rho``: a packing
  in the leaf at side ``<= U`` is then within ``rho`` of the image in the anchored
  33-coordinate sup norm (the angle window is far inside ``rho`` and axis angles are
  exact), so the local theorem makes it the image.  For the ``n = 5`` control there is no
  local theorem, and ``t`` leaves are a capture statement only.
- ``u``: unresolved -- the node cap, the wall cap, an open leaf (a feasible core packing
  below the target with no violated pair, not captured), or a tight bound the float
  multipliers could not certify.

**Output.**  A gzip JSON-lines tree in depth-first pre-order: one header, then one line per
node.  A branch line names its pair and option count and is followed by its children,
each carrying the option index it takes.  `fixed_angle_tree_check` replays it without
this module.

    uv run --frozen python -m cases.trump11.fixed_angle_tree h236 \\
        --out ../attic/rung0/h236.jsonl.gz --summary ../attic/rung0/h236-summary.json

**Boxes (rung 1, H-112).**  The ``box`` preset runs the same family, cores, rows and
certificates on a declared box ``--t-lo``/``--t-hi``, taken as exact rationals, against
U's rational upper end or a declared ``--target``; `box_setup` says when the Trump image
applies.  It stops at the first open leaf, since no branching inside the box can close
one.  The ``h236`` preset and every control are unchanged.
"""

from __future__ import annotations

import argparse
import dataclasses
import functools
import gzip
import importlib
import json
import math
import multiprocessing
import os
import random
import statistics
import sys
import time
from collections import Counter
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import datetime
from fractions import Fraction
from pathlib import Path
from typing import IO, Any

import numpy as np

from cases.trump11.packing import build

SCHEMA = "fixed-angle-tree/v1"
ORDER_EPSILON = Fraction(1, 4)
CORE_DIGITS = 15
BOX_DIGITS = 12
FIELD_DIGITS = 45
VARIABLE_CAP = Fraction(4)
VIOLATION_TOLERANCE = 1e-9
SMALL_MULTIPLIER = 1e-15
# BC-240's preferred local radius, in the labelled anchored 33-coordinate sup norm.
TRUMP_RHO = Fraction(808514697, 200000000000)

type Vec = tuple[Fraction, Fraction]
type Direction = tuple[int, int]
type Pair = tuple[int, int]
type Interval = tuple[Fraction, Fraction]


# -- exact geometry ---------------------------------------------------------------------


def rotation(half_tangent: Fraction) -> Vec:
    """``(cos theta, sin theta)`` for ``theta = 2 atan(half_tangent)``, exactly."""
    denominator = 1 + half_tangent * half_tangent
    return (1 - half_tangent * half_tangent) / denominator, 2 * half_tangent / denominator


def primitive(x: Fraction, y: Fraction) -> Direction:
    """The coprime integer vector with the direction of ``(x, y)``."""
    scale = math.lcm(x.denominator, y.denominator)
    a, b = int(x * scale), int(y * scale)
    divisor = math.gcd(a, b)
    if divisor == 0:
        raise ValueError("a direction must be nonzero")
    return a // divisor, b // divisor


def _half_plane(direction: Direction) -> int:
    x, y = direction
    return 0 if y > 0 or (y == 0 and x > 0) else 1


def _angular_compare(first: Direction, second: Direction) -> int:
    """Counter-clockwise order from the positive x axis, decided exactly."""
    halves = _half_plane(first) - _half_plane(second)
    if halves:
        return halves
    cross = first[0] * second[1] - first[1] * second[0]
    return -1 if cross > 0 else (1 if cross < 0 else 0)


@dataclass(frozen=True)
class Core:
    """A square of side ``side`` at half-tangent ``half_tangent``, centred at the origin."""

    half_tangent: Fraction
    side: Fraction

    @functools.cached_property
    def vertices(self) -> tuple[Vec, ...]:
        c, s = rotation(self.half_tangent)
        h = self.side / 2
        return tuple(
            (h * (c * a - s * b), h * (s * a + c * b))
            for a, b in ((1, 1), (-1, 1), (-1, -1), (1, -1))
        )

    @functools.cached_property
    def normals(self) -> tuple[Direction, ...]:
        a, b = primitive(*rotation(self.half_tangent))
        return (a, b), (-b, a), (-a, -b), (b, -a)

    def support(self, direction: Vec) -> Fraction:
        return max(direction[0] * vx + direction[1] * vy for vx, vy in self.vertices)


AXIS_CORE = Core(Fraction(0), Fraction(1))


def core_in_window(core: Core, left: Fraction, right: Fraction) -> bool:
    """Every vertex of ``core`` lies in the unit square at every angle of ``[left, right]``."""
    if not 0 <= left <= right < 1:
        return False
    ends = [rotation(left), rotation(right)]
    for vx, vy in core.vertices:
        for turn in range(4):
            (ax, ay), (bx, by) = (_turn(end, turn) for end in ends)
            if ax * vx + ay * vy > Fraction(1, 2) or bx * vx + by * vy > Fraction(1, 2):
                return False
            inside_window = ax * vy - ay * vx >= 0 and vx * by - vy * bx >= 0
            if inside_window and vx * vx + vy * vy > Fraction(1, 4):
                return False
    return True


def _turn(vector: Vec, quarter_turns: int) -> Vec:
    x, y = vector
    for _ in range(quarter_turns % 4):
        x, y = -y, x
    return x, y


def window_core(left: Fraction, right: Fraction) -> Core:
    """The rational square core of the window ``[left, right]`` of half-tangents."""
    if left == right:
        return Core(left, Fraction(1))
    middle = (left + right) / 2
    cm, sm = rotation(middle)
    ratio: Fraction | None = None
    for end in (left, right):
        ce, se = rotation(end)
        cos_d, sin_d = cm * ce + sm * se, sm * ce - cm * se
        bound = 1 / (abs(cos_d) + abs(sin_d))
        ratio = bound if ratio is None else min(ratio, bound)
    assert ratio is not None
    scale = 10**CORE_DIGITS
    core = Core(middle, Fraction(math.floor(ratio * scale), scale))
    if not core_in_window(core, left, right):
        raise ValueError("the rounded core is not inside the window")
    return core


# -- the family and its rows ------------------------------------------------------------


@dataclass(frozen=True)
class Family:
    axis_count: int
    tilted_count: int
    left: Fraction
    right: Fraction

    @property
    def count(self) -> int:
        return self.axis_count + self.tilted_count

    @property
    def width(self) -> int:
        return 2 * self.count + 1

    @property
    def side_column(self) -> int:
        return 2 * self.count

    @functools.cached_property
    def tilted_core(self) -> Core:
        return window_core(self.left, self.right)

    def core(self, index: int) -> Core:
        return AXIS_CORE if index < self.axis_count else self.tilted_core

    def classes(self) -> list[range]:
        return [
            block
            for block in (range(self.axis_count), range(self.axis_count, self.count))
            if len(block)
        ]

    @functools.cached_property
    def pairs(self) -> tuple[Pair, ...]:
        return tuple((i, j) for i in range(self.count) for j in range(i + 1, self.count))

    @functools.cache  # noqa: B019 - one Family per run; the cache is the row table
    def axes(self, i: int, j: int) -> tuple[Direction, ...]:
        union = set(self.core(i).normals) | set(self.core(j).normals)
        return tuple(sorted(union, key=functools.cmp_to_key(_angular_compare)))


@dataclass(frozen=True)
class Row:
    """``sum coefficients . z >= rhs``, with ``coefficients`` as ``(column, value)``."""

    label: str
    coefficients: tuple[tuple[int, Fraction], ...]
    rhs: Fraction


def _row(label: str, entries: dict[int, Fraction], rhs: Fraction) -> Row:
    return Row(label, tuple(sorted((k, v) for k, v in entries.items() if v)), rhs)


def base_rows(family: Family, quadrant: str, epsilon: Fraction | None) -> list[Row]:
    """Containment rows for every square, then the declared symmetry rows."""
    n, side = family.count, family.side_column
    one = Fraction(1)
    rows: list[Row] = []
    for i in range(n):
        core = family.core(i)
        hx, hy = core.support((one, Fraction(0))), core.support((Fraction(0), one))
        rows.extend(
            (
                _row(f"wall:{i}:L", {i: one}, hx),
                _row(f"wall:{i}:R", {side: one, i: -one}, hx),
                _row(f"wall:{i}:B", {n + i: one}, hy),
                _row(f"wall:{i}:T", {side: one, n + i: -one}, hy),
            )
        )
    if epsilon is not None:
        for block in family.classes():
            for i in block[:-1]:
                entries = {i + 1: one, n + i + 1: epsilon, i: -one, n + i: -epsilon}
                rows.append(_row(f"order:{i}", entries, Fraction(0)))
    if quadrant != "none":
        block = quadrant_class(family, quadrant)
        half = Fraction(len(block), 2)
        rows.append(_row("quad:x", {**dict.fromkeys(block, one), side: -half}, Fraction(0)))
        y_entries = {**{n + i: one for i in block}, side: -half}
        rows.append(_row("quad:y", y_entries, Fraction(0)))
    return rows


def quadrant_class(family: Family, quadrant: str) -> range:
    if quadrant == "axis":
        return range(family.axis_count)
    if quadrant == "tilted":
        return range(family.axis_count, family.count)
    raise ValueError(f"unknown quadrant class {quadrant!r}")


def pair_row(family: Family, i: int, j: int, option: int) -> Row:
    """The separating-axis row for pair ``(i, j)`` along its ``option``-th candidate."""
    direction = family.axes(i, j)[option]
    scale = max(abs(direction[0]), abs(direction[1]))
    n = (Fraction(direction[0], scale), Fraction(direction[1], scale))
    rhs = family.core(i).support(n) + family.core(j).support(n)
    k = family.count
    entries = {i: -n[0], k + i: -n[1], j: n[0], k + j: n[1]}
    return _row(f"pair:{i}:{j}:{option}", entries, rhs)


# -- exact certificates -----------------------------------------------------------------


def certified_bound(
    rows: dict[str, Row],
    weights: dict[str, Fraction],
    objective: dict[int, Fraction],
    bounds: Sequence[Interval],
) -> Fraction:
    """``b . y + sum_k min over bounds of (c - A^T y)_k z_k``, exactly."""
    residual = dict(objective)
    total = Fraction(0)
    for label, weight in weights.items():
        if weight < 0:
            raise ValueError("multipliers must be nonnegative")
        row = rows[label]
        total += weight * row.rhs
        for column, value in row.coefficients:
            residual[column] = residual.get(column, Fraction(0)) - weight * value
    for column, value in residual.items():
        low, high = bounds[column]
        total += min(value * low, value * high)
    return total


def farkas_margin(
    rows: dict[str, Row], weights: dict[str, Fraction], bounds: Sequence[Interval]
) -> Fraction:
    """``b . y + sum_k min over bounds of (-A^T y)_k z_k``; positive means no solution."""
    return certified_bound(rows, weights, {}, bounds)


def _weights(values: Sequence[float], labels: Sequence[str]) -> dict[str, str]:
    return {
        label: repr(float(value))
        for label, value in zip(labels, values, strict=True)
        if value > SMALL_MULTIPLIER
    }


def _exact(weights: dict[str, str]) -> dict[str, Fraction]:
    return {label: Fraction(text) for label, text in weights.items()}


# -- HiGHS, incrementally ---------------------------------------------------------------


@dataclass
class Solve:
    status: str
    value: float
    point: np.ndarray
    duals: list[float]
    ray: list[float] | None


class Model:
    """A HiGHS model whose rows form a stack, re-solved warm after each push or pop.

    `scipy.optimize.linprog` rebuilds the model on every call (about 1.6 ms here); the
    persistent `_Highs` object scipy bundles re-solves a pushed row in about 0.07 ms.
    It is looked up by name because it is scipy's internal binding: only its float
    proposals are used, and every decision is made by the exact evaluation above.
    """

    def __init__(self, width: int, side_column: int, cap: float):
        core = importlib.import_module("scipy.optimize._highspy._core")
        self._inf = vars(core)["kHighsInf"]
        self._highs = vars(core)["_Highs"]()
        highs, quiet = self._highs, False
        highs.setOptionValue("output_flag", quiet)
        highs.setOptionValue("presolve", "off")
        highs.setOptionValue("primal_feasibility_tolerance", 1e-10)
        highs.setOptionValue("dual_feasibility_tolerance", 1e-10)
        empty_index, empty_value = np.array([], dtype=np.int32), np.array([], dtype=np.float64)
        for column in range(width):
            cost = 1.0 if column == side_column else 0.0
            highs.addCol(cost, 0.0, cap, 0, empty_index, empty_value)
        self.width, self.side_column, self.cap = width, side_column, cap
        self.labels: list[str] = []

    def push(self, row: Row) -> None:
        index = np.array([k for k, _ in row.coefficients], dtype=np.int32)
        value = np.array([float(v) for _, v in row.coefficients], dtype=np.float64)
        self._highs.addRow(float(row.rhs), self._inf, len(index), index, value)
        self.labels.append(row.label)

    def pop(self) -> None:
        last = len(self.labels) - 1
        self._highs.deleteRows(1, np.array([last], dtype=np.int32))
        self.labels.pop()

    def set_objective(self, column: int, sign: float) -> None:
        costs = np.zeros(self.width, dtype=np.float64)
        costs[column] = sign
        self._highs.changeColsCost(self.width, np.arange(self.width, dtype=np.int32), costs)

    def set_side_cap(self, cap: float) -> None:
        self._highs.changeColBounds(self.side_column, 0.0, cap)

    def solve(self) -> Solve:
        highs = self._highs
        highs.run()
        status = highs.modelStatusToString(highs.getModelStatus())
        if status == "Optimal":
            solution = highs.getSolution()
            point = np.array(solution.col_value, dtype=np.float64)
            value = float(highs.getInfo().objective_function_value)
            return Solve("optimal", value, point, list(solution.row_dual), None)
        if status == "Infeasible":
            _, has_ray, ray = highs.getDualRay()
            return Solve(
                "infeasible", math.inf, np.zeros(0), [], list(ray) if has_ray else None
            )
        return Solve(status, math.nan, np.zeros(0), [], None)


# -- images -----------------------------------------------------------------------------


@dataclass(frozen=True)
class Image:
    """A labelled pose the degenerate leaves are matched to, with its radius."""

    name: str
    rotation: int
    labels: tuple[int, ...]
    centres: tuple[tuple[Interval, Interval], ...]
    radius: Fraction
    theorem: bool

    def column_intervals(self) -> list[Interval]:
        return [c[0] for c in self.centres] + [c[1] for c in self.centres]

    def floats(self) -> np.ndarray:
        return np.array(
            [float((lo + hi) / 2) for lo, hi in self.column_intervals()], dtype=np.float64
        )


def _order_key(point: tuple[float, float]) -> float:
    return point[0] + float(ORDER_EPSILON) * point[1]


def trump_setup(half_width: Fraction) -> tuple[Family, Interval, Image, dict[str, Any]]:
    """The H-236 box, U's enclosure and the labelled Trump image the rows select."""
    squares, side, field = build()
    field.refine_to(FIELD_DIGITS)
    u_lo, u_hi = field.root_bounds()
    u_enclosure = field.enclose(side)
    scale = 10**BOX_DIGITS
    left = Fraction(math.floor((u_lo - half_width) * scale), scale)
    right = Fraction(math.ceil((u_hi + half_width) * scale), scale)
    family = Family(6, 5, left, right)
    centres = []
    for corners in squares:
        cx = (corners[0][0] + corners[1][0] + corners[2][0] + corners[3][0]) * Fraction(1, 4)
        cy = (corners[0][1] + corners[1][1] + corners[2][1] + corners[3][1]) * Fraction(1, 4)
        centres.append((cx, cy))
    tilted_centroid = [
        sum(float(c[k]) for c in centres[6:]) - 5 * float(side) / 2 for k in (0, 1)
    ]
    turns = next(turn for turn in range(4) if min(_turn_float(tilted_centroid, turn)) > 0)
    turned = []
    for cx, cy in centres:
        x, y = cx, cy
        for _ in range(turns):
            x, y = side - y, x
        turned.append((x, y))
    floats = [(float(x), float(y)) for x, y in turned]
    labels = tuple(
        sorted(range(6), key=lambda i: _order_key(floats[i]))
        + sorted(range(6, 11), key=lambda i: _order_key(floats[i]))
    )
    image_centres = tuple(
        (field.enclose(turned[label][0]), field.enclose(turned[label][1])) for label in labels
    )
    image = Image("trump11", turns, labels, image_centres, TRUMP_RHO, theorem=True)
    extra = {
        "u_enclosure": [str(u_lo), str(u_hi)],
        "requested_half_width": str(half_width),
        "tilted_centroid_offset": tilted_centroid,
    }
    return family, u_enclosure, image, extra


def _turn_float(vector: Sequence[float], turns: int) -> tuple[float, float]:
    x, y = vector[0], vector[1]
    for _ in range(turns):
        x, y = -y, x
    return x, y


def sqrt2_enclosure(digits: int) -> Interval:
    scale = 10**digits
    root = math.isqrt(2 * scale * scale)
    return Fraction(root, scale), Fraction(root + 1, scale)


def goebel_setup(half_width: Fraction, radius: Fraction) -> tuple[Family, Interval, Image]:
    """The n = 5 control box around 45 degrees, s(5)'s enclosure and Goebel's image."""
    r_lo, r_hi = sqrt2_enclosure(FIELD_DIGITS)
    t_lo, t_hi = r_lo - 1, r_hi - 1  # tan(pi/8) = sqrt(2) - 1
    scale = 10**BOX_DIGITS
    left = Fraction(math.floor((t_lo - half_width) * scale), scale)
    right = Fraction(math.ceil((t_hi + half_width) * scale), scale)
    family = Family(4, 1, left, right)
    s_lo, s_hi = 2 + r_lo / 2, 2 + r_hi / 2
    half = Fraction(1, 2)
    near: Interval = (half, half)
    far: Interval = (s_lo - half, s_hi - half)
    middle: Interval = (s_lo / 2, s_hi / 2)
    corners = [(near, near), (near, far), (far, near), (far, far)]
    corners.sort(key=lambda c: _order_key((float(c[0][0]), float(c[1][0]))))
    centres = (*corners, (middle, middle))
    image = Image("goebel5", 0, (0, 1, 2, 3, 4), tuple(centres), radius, theorem=False)
    return family, (s_lo, s_hi), image


def box_setup(
    left: Fraction,
    right: Fraction,
    *,
    axis_count: int = 6,
    tilted_count: int = 5,
    trump: bool = True,
) -> tuple[Family, Interval, Image | None, dict[str, Any]]:
    """The declared box ``[left, right]``, U's enclosure, and the Trump image if it applies.

    With ``trump``, a six-plus-five box that meets the enclosure of Trump's half-tangent
    ``t*`` gets the labelled image only if it holds that whole enclosure and its angle
    reach ``2 max(u_hi - left, right - u_lo)`` is below ``rho``, the reader's own test at
    a wider enclosure; any other box meeting ``t*`` is refused, since it would need the
    theorem it cannot use.  A box away from ``t*`` has no image, so the producer cannot
    write a ``t`` leaf there and the reader refuses one.
    """
    if not 0 <= left < right < 1:
        raise ValueError("a box needs 0 <= t_lo < t_hi < 1")
    if axis_count < 0 or tilted_count < 1:
        raise ValueError("a box needs at least one tilted square")
    _, u_enclosure, trump_image, setup = trump_setup(Fraction(1, 10**6))
    root_lo, root_hi = (Fraction(bound) for bound in setup["u_enclosure"])
    meets = (axis_count, tilted_count) == (6, 5) and left <= root_hi and root_lo <= right
    image = None
    if trump and meets:
        if not left <= root_lo <= root_hi <= right:
            raise ValueError("the box straddles an end of t*'s enclosure")
        if 2 * max(root_hi - left, right - root_lo) >= trump_image.radius:
            raise ValueError("the box holds t* but is too wide for rho; split it")
        image = trump_image
    family = Family(axis_count, tilted_count, left, right)
    return family, u_enclosure, image, {"u_enclosure": setup["u_enclosure"]}


# -- the search -------------------------------------------------------------------------


@dataclass
class Config:
    family: Family
    target: Fraction
    target_label: str
    quadrant: str
    epsilon: Fraction | None
    image: Image | None
    node_cap: int
    wall_cap: float
    child_order: str = "natural"
    stop_on_open: bool = False
    strong: int = 1
    split_depth: int | None = None
    root_path: tuple[tuple[int, int, int], ...] = ()
    deadline: float | None = None


class Search:
    """Depth-first cell tree; every node is written as it is decided."""

    def __init__(self, config: Config, sink: IO[str]):
        self.config = config
        self.family = config.family
        self.sink = sink
        family = self.family
        self.base = base_rows(family, config.quadrant, config.epsilon)
        self.rows: dict[str, Row] = {row.label: row for row in self.base}
        self.model = Model(family.width, family.side_column, float(VARIABLE_CAP))
        for row in self.base:
            self.model.push(row)
        self.bounds: list[Interval] = [(Fraction(0), VARIABLE_CAP)] * family.width
        self.capped: list[Interval] = list(self.bounds)
        self.capped[family.side_column] = (Fraction(0), config.target)
        self.branched: set[int] = set()
        self.root_measure = 1.0
        for i, j, option in config.root_path:
            pair_index = family.pairs.index((i, j))
            self.model.push(self.pair_row(pair_index, option))
            self.branched.add(pair_index)
            self.root_measure /= len(family.axes(i, j))
        self.frontier: list[list[list[int]]] = []
        self._prepare_violation_arrays()
        self.nodes = 0
        self.kinds: Counter[str] = Counter()
        self.depths: Counter[int] = Counter()
        self.leaf_depths: Counter[int] = Counter()
        self.unresolved: list[dict[str, Any]] = []
        self.closed_measure = 0.0
        self.max_bound_below: float = -math.inf
        self.started = time.monotonic()
        self.stopped = ""
        self.image_floats = config.image.floats() if config.image else None
        self.enclosure_reach = 0.0
        self.lp_solves = 0

    # rows and violations

    def pair_row(self, pair_index: int, option: int) -> Row:
        i, j = self.family.pairs[pair_index]
        label = f"pair:{i}:{j}:{option}"
        row = self.rows.get(label)
        if row is None:
            row = pair_row(self.family, i, j, option)
            self.rows[label] = row
        return row

    def _prepare_violation_arrays(self) -> None:
        family = self.family
        width = max(len(family.axes(i, j)) for i, j in family.pairs)
        count = len(family.pairs)
        self.first = np.array([i for i, _ in family.pairs], dtype=np.int64)
        self.second = np.array([j for _, j in family.pairs], dtype=np.int64)
        self.unit = np.zeros((count, width, 2), dtype=np.float64)
        self.reach = np.full((count, width), np.inf, dtype=np.float64)
        for p, (i, j) in enumerate(family.pairs):
            for k, (a, b) in enumerate(family.axes(i, j)):
                norm = math.hypot(a, b)
                n = (Fraction(a), Fraction(b))
                self.unit[p, k] = (a / norm, b / norm)
                reach = family.core(i).support(n) + family.core(j).support(n)
                self.reach[p, k] = float(reach) / norm

    def violations(self, point: np.ndarray) -> np.ndarray:
        n = self.family.count
        dx = point[self.second] - point[self.first]
        dy = point[n + self.second] - point[n + self.first]
        gaps = self.unit[:, :, 0] * dx[:, None] + self.unit[:, :, 1] * dy[:, None] - self.reach
        depth = -gaps.max(axis=1)
        if self.branched:
            depth[list(self.branched)] = -np.inf
        return depth

    def strongest(self, point: np.ndarray) -> int | None:
        """Among the ``strong`` most violated pairs, the one with fewest open children.

        A child is open when its float LP is feasible and at most the target.  Fewest
        open children first (a pair with one open child is forced and costs no width),
        then the largest smallest child value.  This only chooses *which* pair to
        branch; every option of the chosen pair is still a child.
        """
        depth = self.violations(point)
        order = np.argsort(-depth)[: self.config.strong]
        candidates = [int(p) for p in order if depth[p] > VIOLATION_TOLERANCE]
        if len(candidates) <= 1:
            return candidates[0] if candidates else None
        target = float(self.config.target)
        best, best_score = None, (-math.inf, -math.inf, -math.inf)
        for pair in candidates:
            values = []
            for option in range(len(self.family.axes(*self.family.pairs[pair]))):
                self.model.push(self.pair_row(pair, option))
                solve = self.model.solve()
                self.model.pop()
                self.lp_solves += 1
                closed = solve.status == "infeasible" or solve.value > target
                values.append(math.inf if closed else solve.value)
            finite = [v for v in values if v != math.inf]
            score = (-len(finite), min(values), sum(finite) - len(finite) * target)
            if score > best_score:
                best, best_score = pair, score
            if not finite:
                break
        return best

    def most_violated(self, points: Sequence[np.ndarray]) -> int | None:
        best, best_depth = None, VIOLATION_TOLERANCE
        for point in points:
            depth = self.violations(point)
            index = int(depth.argmax())
            if depth[index] > best_depth:
                best, best_depth = index, float(depth[index])
        return best

    # output

    def emit(self, record: dict[str, Any]) -> None:
        self.sink.write(json.dumps(record, separators=(",", ":")))
        self.sink.write("\n")

    def out_of_budget(self) -> bool:
        if self.stopped:
            return True
        deadline = self.config.deadline
        if self.nodes >= self.config.node_cap:
            self.stopped = "node-cap"
        elif (deadline is not None and time.time() >= deadline) or (
            time.monotonic() - self.started >= self.config.wall_cap
        ):
            self.stopped = "wall-cap"
        return bool(self.stopped)

    # certificates

    def bound_certificate(self, solve: Solve) -> dict[str, str] | None:
        weights = _weights(solve.duals, self.model.labels)
        objective = {self.family.side_column: Fraction(1)}
        bound = certified_bound(self.rows, _exact(weights), objective, self.bounds)
        return weights if bound > self.config.target else None

    def farkas_certificate(self, solve: Solve) -> dict[str, str] | None:
        if solve.ray is None:
            return None
        for sign in (1.0, -1.0):
            weights = _weights([sign * v for v in solve.ray], self.model.labels)
            if weights and farkas_margin(self.rows, _exact(weights), self.bounds) > 0:
                return weights
        return None

    def enclosure(self) -> tuple[dict[str, Any] | None, list[np.ndarray]]:
        """Certified centre bounds at ``S <= target``; ``None`` if not within the radius."""
        image = self.config.image
        assert image is not None
        family, model = self.family, self.model
        model.set_side_cap(float(self.config.target) + 1e-12)
        low_certs: list[dict[str, str]] = []
        high_certs: list[dict[str, str]] = []
        points: list[np.ndarray] = []
        offsets: list[float] = []
        intervals = image.column_intervals()
        inside = True
        try:
            for column in range(2 * family.count):
                for sign, sink in ((1, low_certs), (-1, high_certs)):
                    model.set_objective(column, float(sign))
                    solve = model.solve()
                    if solve.status != "optimal":
                        return None, points
                    points.append(solve.point)
                    weights = _weights(solve.duals, model.labels)
                    bound = certified_bound(
                        self.rows, _exact(weights), {column: Fraction(sign)}, self.capped
                    )
                    lo, hi = intervals[column]
                    if sign > 0:
                        inside = inside and bound > hi - image.radius
                        offsets.append(float(lo - bound))
                    else:
                        inside = inside and -bound < lo + image.radius
                        offsets.append(float(-bound - hi))
                    sink.append(weights)
        finally:
            model.set_objective(family.side_column, 1.0)
            model.set_side_cap(model.cap)
        if not inside:
            return None, points
        self.enclosure_reach = max(self.enclosure_reach, *offsets)
        return {"lo": low_certs, "hi": high_certs, "reach": max(offsets)}, points

    # the tree

    def run(self) -> None:
        self.visit(len(self.config.root_path), None, self.root_measure)

    def current_path(self) -> list[list[int]]:
        labels = self.model.labels[len(self.base) :]
        return [[int(part) for part in label.split(":")[1:]] for label in labels]

    def probe(self, rng: random.Random) -> tuple[float, int]:
        """One Knuth dive: an unbiased estimate of the tree's node count, and its depth.

        The dive follows the tree's own branching rule and takes one option uniformly at
        random; a node counts as a leaf when its float LP is infeasible or above the
        target, or when it has no violated pair.  Leaves are not certified here.
        """
        estimate, weight, pushed = 0.0, 1.0, []
        target = float(self.config.target)
        try:
            while True:
                estimate += weight
                solve = self.model.solve()
                self.lp_solves += 1
                if solve.status != "optimal" or solve.value > target:
                    break
                pair = self.strongest(solve.point)
                if pair is None:
                    break
                options = len(self.family.axes(*self.family.pairs[pair]))
                self.branched.add(pair)
                self.model.push(self.pair_row(pair, rng.randrange(options)))
                pushed.append(pair)
                weight *= options
        finally:
            for pair in reversed(pushed):
                self.model.pop()
                self.branched.discard(pair)
        return estimate, len(pushed)

    def knuth(self, probes: int, seed: int) -> dict[str, Any]:
        rng = random.Random(seed)
        estimates, depths = [], []
        for _ in range(probes):
            estimate, depth = self.probe(rng)
            estimates.append(estimate)
            depths.append(depth)
        mean = statistics.fmean(estimates)
        error = statistics.stdev(estimates) / math.sqrt(probes) if probes > 1 else math.nan
        ordered = sorted(estimates)
        return {
            "probes": probes,
            "seed": seed,
            "mean_nodes": mean,
            "standard_error": error,
            "log10_mean": math.log10(mean),
            "median_estimate": statistics.median(estimates),
            "quantiles_10_50_90_99": [
                ordered[int(q * (probes - 1))] for q in (0.1, 0.5, 0.9, 0.99)
            ],
            "max_estimate": ordered[-1],
            "share_of_mean_from_top_1pct": sum(ordered[-max(1, probes // 100) :])
            / sum(ordered),
            "depth_histogram": {str(k): v for k, v in sorted(Counter(depths).items())},
            "wall_seconds": round(time.monotonic() - self.started, 3),
            "lp_solves": self.lp_solves,
        }

    def visit(self, depth: int, option: int | None, measure: float) -> None:
        head: dict[str, Any] = {"o": option}
        if self.out_of_budget():
            self.leaf(head | {"u": self.stopped}, depth, "u", {"reason": self.stopped})
            return
        split = self.config.split_depth
        if split is not None and depth >= split:
            self.emit(head | {"s": len(self.frontier)})
            self.frontier.append(self.current_path())
            self.kinds["s"] += 1
            return
        self.nodes += 1
        self.lp_solves += 1
        self.depths[depth] += 1
        solve = self.model.solve()
        immediate = self.immediate(solve)
        if immediate is not None:
            kind, payload = immediate
            detail = {"reason": payload["u"]} if kind == "u" else None
            self.leaf(head | payload, depth, kind, detail)
            if kind != "u":
                self.closed_measure += measure
            return
        self.max_bound_below = max(self.max_bound_below, solve.value)
        pair = self.strongest(solve.point)
        if pair is None and self.near_image(solve.point):
            certificate, points = self.enclosure()
            if certificate is not None:
                self.leaf(head | {"t": certificate, "v": solve.value}, depth, "t")
                self.closed_measure += measure
                return
            pair = self.most_violated(points)
        if pair is None:
            reason = "open" if solve.value <= float(self.config.target) else "tight"
            detail = {"reason": reason, "value": solve.value, "point": solve.point.tolist()}
            self.leaf(head | {"u": reason, "v": solve.value}, depth, "u", detail)
            if self.config.stop_on_open:
                self.stopped = "stopped-on-open"
            return
        self.branch(depth, head, pair, solve.value, measure)

    def immediate(self, solve: Solve) -> tuple[str, dict[str, Any]] | None:
        """The leaf a solved node closes to without branching, if any."""
        if solve.status == "infeasible":
            weights = self.farkas_certificate(solve)
            return ("f", {"f": weights}) if weights is not None else ("u", {"u": "no-farkas"})
        if solve.status != "optimal":
            return "u", {"u": solve.status}
        if solve.value > float(self.config.target):
            weights = self.bound_certificate(solve)
            if weights is not None:
                return "c", {"c": weights, "v": solve.value}
        return None

    def near_image(self, point: np.ndarray) -> bool:
        if self.image_floats is None or self.config.image is None:
            return False
        count = 2 * self.family.count
        gap = np.abs(point[:count] - self.image_floats).max()
        return bool(gap < float(self.config.image.radius))

    def leaf(
        self,
        record: dict[str, Any],
        depth: int,
        kind: str,
        detail: dict[str, Any] | None = None,
    ) -> None:
        self.emit(record)
        self.kinds[kind] += 1
        self.leaf_depths[depth] += 1
        if detail is not None and len(self.unresolved) < 10_000:
            self.unresolved.append(detail | {"depth": depth, "path": self.current_path()})

    def branch(
        self, depth: int, head: dict[str, Any], pair: int, value: float, measure: float
    ) -> None:
        i, j = self.family.pairs[pair]
        options = len(self.family.axes(i, j))
        self.emit(head | {"b": [i, j], "n": options, "v": value})
        self.kinds["b"] += 1
        order = list(range(options))
        if self.config.child_order == "bound":
            values = []
            for k in order:
                self.model.push(self.pair_row(pair, k))
                values.append(self.model.solve().value)
                self.model.pop()
            order.sort(key=lambda k: values[k])
        self.branched.add(pair)
        for k in order:
            self.model.push(self.pair_row(pair, k))
            self.visit(depth + 1, k, measure / options)
            self.model.pop()
        self.branched.discard(pair)

    def summary(self) -> dict[str, Any]:
        wall = time.monotonic() - self.started
        return {
            "nodes_solved": self.nodes,
            "lp_solves": self.lp_solves,
            "leaves": dict(self.kinds),
            "branch_nodes": self.kinds.get("b", 0),
            "stopped": self.stopped or "complete",
            "closed": self.kinds.get("u", 0) == 0,
            "wall_seconds": round(wall, 3),
            "nodes_per_second": round(self.nodes / wall, 1) if wall else None,
            "closed_measure": self.closed_measure,
            "depth_histogram": {str(k): v for k, v in sorted(self.depths.items())},
            "leaf_depth_histogram": {str(k): v for k, v in sorted(self.leaf_depths.items())},
            "max_lp_value_expanded": self.max_bound_below,
            "max_enclosure_reach_beyond_image": self.enclosure_reach,
            "unresolved_sample": self.unresolved[:200],
            "unresolved_recorded": len(self.unresolved),
        }


# -- presets and the command line -------------------------------------------------------


def trump_cell(config: Config, pairs: int = 16) -> tuple[tuple[int, int, int], ...]:
    """The ``pairs`` tightest pairs at the Trump image, each on its best separating axis."""
    image = config.image
    if image is None:
        raise ValueError("the Trump cell needs the Trump image")
    with Path(os.devnull).open("w", encoding="utf-8") as sink:
        search = Search(dataclasses.replace(config, root_path=()), sink)
    point, n = image.floats(), config.family.count
    dx = point[search.second] - point[search.first]
    dy = point[n + search.second] - point[n + search.first]
    gaps = search.unit[:, :, 0] * dx[:, None] + search.unit[:, :, 1] * dy[:, None]
    gaps -= search.reach
    tightest = sorted(np.argsort(gaps.max(axis=1))[:pairs].tolist())
    return tuple((*config.family.pairs[p], int(gaps[p].argmax())) for p in tightest)


def header(config: Config, extra: dict[str, Any]) -> dict[str, Any]:
    family = config.family
    core = family.tilted_core if family.tilted_count else AXIS_CORE
    image = config.image
    return {
        "schema": SCHEMA,
        "family": {
            "axis_count": family.axis_count,
            "tilted_count": family.tilted_count,
            "left": str(family.left),
            "right": str(family.right),
        },
        "core": {"half_tangent": str(core.half_tangent), "side": str(core.side)},
        "target": {"label": config.target_label, "upper": str(config.target)},
        "variable_cap": str(VARIABLE_CAP),
        "symmetry": {
            "quadrant": config.quadrant,
            "order_epsilon": None if config.epsilon is None else str(config.epsilon),
        },
        "image": None
        if image is None
        else {
            "name": image.name,
            "rotation": image.rotation,
            "labels": list(image.labels),
            "radius": str(image.radius),
            "theorem": image.theorem,
            "centres": [[[str(v) for v in axis] for axis in c] for c in image.centres],
        },
        "caps": {"nodes": config.node_cap, "wall_seconds": config.wall_cap},
        "root_path": [list(step) for step in config.root_path],
        "split_depth": config.split_depth,
        "child_order": config.child_order,
        "strong_branching": config.strong,
        "extra": extra,
    }


def preset(name: str, args: argparse.Namespace) -> tuple[Config, dict[str, Any]]:
    common = {
        "node_cap": args.node_cap,
        "wall_cap": args.wall_cap,
        "strong": args.strong,
        "epsilon": ORDER_EPSILON,
    }
    if name in {"h236", "control-n11-negative", "control-n11-negative-cell"}:
        family, (_, u_hi), image, extra = trump_setup(Fraction(1, 10**6))
        if name == "h236":
            config = Config(family, u_hi, "U", "tilted", image=image, **common)
        elif name == "control-n11-negative-cell":
            # Trump's own cell at U + 1/1000 with no local theorem: it must stay open
            cell = trump_cell(Config(family, u_hi, "U", "tilted", image=image, **common))
            target = u_hi + Fraction(1, 1000)
            config = Config(
                family,
                target,
                "U+1/1000",
                "tilted",
                image=None,
                stop_on_open=True,
                root_path=cell,
                **common,
            )
        else:
            target = u_hi + Fraction(1, 1000)
            config = Config(
                family,
                target,
                "U+1/1000",
                "tilted",
                image=None,
                child_order="bound",
                stop_on_open=True,
                **common,
            )
        return config, extra
    if name in {"control-n5", "control-n5-capture"}:
        family, (s_lo, s_hi), goebel = goebel_setup(Fraction(1, 10**4), Fraction(1, 20))
        extra = {"s5_enclosure": [str(s_lo), str(s_hi)]}
        if name == "control-n5":
            target = s_lo - Fraction(1, 1000)
            return Config(family, target, "s5-1/1000", "tilted", image=None, **common), extra
        target = s_hi + Fraction(1, 1000)
        return Config(family, target, "s5+1/1000", "tilted", image=goebel, **common), extra
    if name.startswith("control-axis-"):
        count, sign = name.removeprefix("control-axis-").split("-")
        family = Family(int(count), 0, Fraction(0), Fraction(0))
        # ceil(sqrt(n)) is exact for axis-parallel unit squares: a grid of k^2 marks with
        # spacing below 1 puts a mark inside every open unit square when S < k + 1.
        answer = math.isqrt(int(count) - 1) + 1
        delta = Fraction(1, 1000) if sign == "above" else -Fraction(1, 1000)
        label = f"{answer}{'+' if sign == 'above' else '-'}1/1000"
        return Config(
            family, answer + delta, label, "axis", image=None, stop_on_open=True, **common
        ), {"axis_answer": answer}
    if name == "box":
        # U's upper end with the Trump image where it applies; a declared target never
        # takes the image, so a t leaf cannot stand in for a bound above that target
        counts = (args.axis_count, args.tilted_count)
        if args.t_lo is None or args.t_hi is None:
            raise SystemExit("the box preset needs --t-lo and --t-hi")
        if args.target is None and counts != (6, 5):
            raise SystemExit("U is the six-plus-five target; other counts need --target")
        if args.target is not None and not 0 < args.target < VARIABLE_CAP:
            raise SystemExit("the target must lie inside the variable box")
        try:
            family, (_, u_hi), image, extra = box_setup(
                args.t_lo,
                args.t_hi,
                axis_count=counts[0],
                tilted_count=counts[1],
                trump=args.target is None,
            )
        except ValueError as error:
            raise SystemExit(str(error)) from error
        target, label = (u_hi, "U") if args.target is None else (args.target, str(args.target))
        return Config(
            family, target, label, "tilted", image=image, stop_on_open=True, **common
        ), extra
    raise SystemExit(f"unknown preset {name!r}")


PRESETS = (
    "h236",
    "control-n11-negative",
    "control-n11-negative-cell",
    "control-n5",
    "control-n5-capture",
    "control-axis-2-below",
    "control-axis-2-above",
    "control-axis-4-below",
    "control-axis-4-above",
    "control-axis-5-below",
    "control-axis-5-above",
    "box",
)


def run(
    config: Config, extra: dict[str, Any], out: Path, progress: Callable[[str], None]
) -> dict[str, Any]:
    out.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(out, "wt", encoding="utf-8") as sink:
        sink.write(json.dumps({"header": header(config, extra)}) + "\n")
        search = Search(config, sink)
        sys.setrecursionlimit(max(sys.getrecursionlimit(), 10_000))
        search.run()
    result = search.summary()
    progress(
        f"{result['stopped']}: {result['nodes_solved']} nodes, leaves {result['leaves']}, "
        f"{result['wall_seconds']} s"
    )
    return result


def subtree_directory(out: Path) -> Path:
    return out.parent / (out.name.removesuffix(".jsonl.gz") + ".sub")


def _grow_subtree(task: tuple[Config, dict[str, Any], str, int, list[list[int]]]) -> dict:
    config, extra, directory, index, path = task
    root = tuple((step[0], step[1], step[2]) for step in path)
    sub = dataclasses.replace(config, split_depth=None, root_path=root)
    out = Path(directory) / f"sub-{index:05d}.jsonl.gz"
    return run(sub, extra, out, lambda _: None) | {"index": index}


def frontier_paths(top: Path) -> list[tuple[tuple[int, int, int], ...]]:
    """The frontier cells of a split top tree, numbered as its ``s`` leaves number them."""
    stack: list[list[Any]] = []  # [i, j, option count, children seen, current option]
    paths: list[tuple[tuple[int, int, int], ...]] = []
    with gzip.open(top, "rt", encoding="utf-8") as stream:
        next(stream)
        for line in stream:
            node = json.loads(line)
            if stack:
                stack[-1][3] += 1
                stack[-1][4] = node["o"]
            if "b" in node:
                stack.append([*node["b"], node["n"], 0, None])
                continue
            if "s" in node:
                if node["s"] != len(paths):
                    raise ValueError("the top tree's frontier leaves are out of sequence")
                paths.append(tuple((f[0], f[1], f[4]) for f in stack))
            while stack and stack[-1][3] == stack[-1][2]:
                stack.pop()
    return paths


def _grow_resumed(
    task: tuple[Config, dict[str, Any], str, int, tuple[tuple[int, int, int], ...], float],
) -> dict:
    """Re-grow one subtree from scratch; the old file is replaced only when this one ends.

    A task that starts after ``launch_by`` writes its root as a ``wall-cap`` leaf.
    """
    config, extra, directory, index, root, launch_by = task
    if time.time() >= launch_by:
        config = dataclasses.replace(config, deadline=launch_by)
    sub = dataclasses.replace(config, split_depth=None, root_path=root)
    final = Path(directory) / f"sub-{index:05d}.jsonl.gz"
    partial = final.with_name(final.name + ".part")
    result = run(sub, extra, partial, lambda _: None)
    partial.replace(final)
    return result | {"index": index}


def run_resume(
    config: Config,
    extra: dict[str, Any],
    out: Path,
    *,
    indices: Sequence[int],
    workers: int,
    launch_by: float,
    stop_at: float,
    progress: Callable[[str], None],
) -> dict[str, Any]:
    """Re-run the listed subtrees of an existing split tree; the top tree is only read."""
    started = time.monotonic()
    directory = subtree_directory(out)
    paths = frontier_paths(out)
    for index in indices:
        old = directory / f"sub-{index:05d}.jsonl.gz"
        if old.exists():
            with gzip.open(old, "rt", encoding="utf-8") as stream:
                recorded = json.loads(next(stream))["header"]["root_path"]
            if recorded != [list(step) for step in paths[index]]:
                raise ValueError(f"subtree {index}'s file does not match the top tree")
    shared = dataclasses.replace(
        config, deadline=stop_at, wall_cap=max(1.0, stop_at - time.time())
    )
    extra = extra | {"subtree_directory": directory.name, "resumed": True}
    tasks = [
        (shared, extra, str(directory), index, paths[index], launch_by) for index in indices
    ]
    summaries = []
    with multiprocessing.get_context("spawn").Pool(workers) as pool:
        for done, result in enumerate(pool.imap_unordered(_grow_resumed, tasks), 1):
            summaries.append(result)
            progress(
                f"{done}/{len(tasks)} resumed: sub {result['index']} {result['stopped']} "
                f"{result['nodes_solved']} nodes, {time.monotonic() - started:.0f} s"
            )
    return aggregate(summaries, time.monotonic() - started, len(tasks))


def run_parallel(
    config: Config,
    extra: dict[str, Any],
    out: Path,
    *,
    workers: int,
    split_depth: int,
    progress: Callable[[str], None],
) -> dict[str, Any]:
    """A top tree cut at ``split_depth``, then one worker file per frontier subtree."""
    started = time.monotonic()
    shared = dataclasses.replace(config, deadline=time.time() + config.wall_cap)
    top = dataclasses.replace(shared, split_depth=split_depth)
    directory = subtree_directory(out)
    directory.mkdir(parents=True, exist_ok=True)
    extra = extra | {"subtree_directory": directory.name}
    with gzip.open(out, "wt", encoding="utf-8") as sink:
        sink.write(json.dumps({"header": header(top, extra)}) + "\n")
        search = Search(top, sink)
        search.run()
    summaries = [search.summary()]
    progress(f"top tree: {search.nodes} nodes, {len(search.frontier)} subtrees")
    tasks = [
        (shared, extra, str(directory), index, path)
        for index, path in enumerate(search.frontier)
    ]
    with multiprocessing.get_context("spawn").Pool(workers) as pool:
        for done, result in enumerate(pool.imap_unordered(_grow_subtree, tasks), 1):
            summaries.append(result)
            if done % 25 == 0 or done == len(tasks):
                progress(f"{done}/{len(tasks)} subtrees, {time.monotonic() - started:.0f} s")
    return aggregate(summaries, time.monotonic() - started, len(tasks))


def aggregate(summaries: list[dict[str, Any]], wall: float, subtrees: int) -> dict[str, Any]:
    kinds: Counter[str] = Counter()
    depths: Counter[str] = Counter()
    leaf_depths: Counter[str] = Counter()
    stops: Counter[str] = Counter()
    unresolved: list[dict[str, Any]] = []
    for summary in summaries:
        kinds.update(summary["leaves"])
        depths.update(summary["depth_histogram"])
        leaf_depths.update(summary["leaf_depth_histogram"])
        stops[summary["stopped"]] += 1
        unresolved.extend(summary["unresolved_sample"][: max(0, 200 - len(unresolved))])
    nodes = sum(summary["nodes_solved"] for summary in summaries)
    return {
        "nodes_solved": nodes,
        "lp_solves": sum(summary["lp_solves"] for summary in summaries),
        "leaves": dict(kinds),
        "subtrees": subtrees,
        "stopped_by_file": dict(stops),
        "closed": kinds.get("u", 0) == 0,
        "wall_seconds": round(wall, 3),
        "nodes_per_second": round(nodes / wall, 1) if wall else None,
        "closed_measure": sum(summary["closed_measure"] for summary in summaries),
        "depth_histogram": dict(sorted(depths.items(), key=lambda item: int(item[0]))),
        "leaf_depth_histogram": dict(
            sorted(leaf_depths.items(), key=lambda item: int(item[0]))
        ),
        "max_lp_value_expanded": max(s["max_lp_value_expanded"] for s in summaries),
        "max_enclosure_reach_beyond_image": max(
            s["max_enclosure_reach_beyond_image"] for s in summaries
        ),
        "unresolved_sample": unresolved,
        "unresolved_recorded": sum(s["unresolved_recorded"] for s in summaries),
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    parser.add_argument("preset", choices=PRESETS)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--node-cap", type=int, default=1_000_000)
    parser.add_argument("--wall-cap", type=float, default=7200.0)
    parser.add_argument("--strong", type=int, default=1, help="pairs scored per branch")
    parser.add_argument("--probes", type=int, default=0, help="Knuth dives instead of a tree")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--workers", type=int, default=0, help="parallel subtree workers")
    parser.add_argument("--split-depth", type=int, default=3)
    parser.add_argument("--resume-subtrees", help="comma-separated subtree indices of --out")
    parser.add_argument("--stop-launching-at", help="ISO time; later subtrees start capped")
    parser.add_argument("--stop-at", help="ISO time at which running subtrees stop")
    parser.add_argument("--t-lo", type=Fraction, help="box preset: exact lower half-tangent")
    parser.add_argument("--t-hi", type=Fraction, help="box preset: exact upper half-tangent")
    parser.add_argument("--target", type=Fraction, help="box preset: exact target, not U")
    parser.add_argument("--axis-count", type=int, default=6, help="box preset only")
    parser.add_argument("--tilted-count", type=int, default=5, help="box preset only")
    args = parser.parse_args(argv)
    config, extra = preset(args.preset, args)
    if args.probes:
        with Path(os.devnull).open("w", encoding="utf-8") as sink:
            estimate = Search(config, sink).knuth(args.probes, args.seed)
        print(json.dumps(estimate))
        result = {"preset": args.preset, "header": header(config, extra), "knuth": estimate}
    elif args.resume_subtrees:
        launch_by = datetime.fromisoformat(args.stop_launching_at).timestamp()
        stop_at = datetime.fromisoformat(args.stop_at).timestamp()
        result = run_resume(
            config,
            extra,
            args.out,
            indices=[int(part) for part in args.resume_subtrees.split(",")],
            workers=args.workers or 1,
            launch_by=launch_by,
            stop_at=stop_at,
            progress=lambda text: print(text, flush=True),
        )
        result = {"preset": args.preset, "tree": str(args.out), "resumed": True, **result}
    elif args.workers:
        result = run_parallel(
            config,
            extra,
            args.out,
            workers=args.workers,
            split_depth=args.split_depth,
            progress=lambda text: print(text, flush=True),
        )
        result = {"preset": args.preset, "tree": str(args.out), **result}
    else:
        result = run(config, extra, args.out, print)
        result = {"preset": args.preset, "tree": str(args.out), **result}
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
