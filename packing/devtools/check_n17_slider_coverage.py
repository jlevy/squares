"""H-268: the n17 slides of any packing in the endpoint's state lie in a certified box.

Claim. Take any packing of 17 unit squares in `[0, S]^2`, `S <= S*` (the H-258 frame:
lower-left corner fixed), whose 45 non-slider coordinates lie within `r = 1/5000` of
the endpoint family (exp-244's neighbourhood) and whose square 6 has its centre in the
closed cell `side-S2` of `check_n17_capacity_one_cover`, at any orientation. Then the
slides satisfy `0 <= a <= A`, `b* <= b <= B` and `Z <= z <= z*`, with `A`, `Z`, `B`
the thresholds passed and `b*`, `z*` exact (closed forms below, enclosed over the root
box). `--design` picks the cover (default the unique-state design; the tabbed one stays
reproducible), and the endpoint's state on it must put square 6 in `side-S2`.

Everything is in the cover frame (the endpoint embedded concentrically), with every
endpoint quantity an exact interval over the exp-238 root box (`cover.endpoint`).

Inner rectangles. A unit square whose centre is displaced by `|delta| <= r sqrt 2`
and turned by `|omega| <= r` from its nominal pose contains the nominal square shrunk
to half-side `H = 1/2 - 2r`: a point with nominal frame coordinates bounded by `H`
has, in the moved frame, a coordinate at most `H (1 + r) + r sqrt 2
= 1/2 - r (3/2 - sqrt 2) - 2 r^2 < 1/2`. A slider moving over an interval (`a` for
square 5 along `-e_x`, `b` for 11 along `-v`, `z` for 13 along `+v`) gives the
intersection of these shrunk squares over the interval, a rectangle shorter along the
slide by the interval's width. Each such set is replaced by a rectangle with rational
centre and rational unit axes (`t` rounded to `2^-32`), shrunk by `2^-28` more, and its
containment in the exact set is checked vertex by vertex in interval arithmetic over the
root box. If two of these inner rectangles overlap (strict separating-axis test on
exact rationals), the two real squares overlap; if one leaves the outer container
bound, its square leaves the container.

Square 6. It is a full unit square at an unknown turn `phi`, which by the square's
symmetry ranges over `[0, pi/2]`, parametrised by `tau = tan(phi/2)` in `[0, 1]` so
that `cos phi` and `sin phi` are exact monotone rationals on every `tau` interval
(rounded outward to `2^-40`). A box of `(tau, x6, y6)` inside the cell is closed when,
for every point of it, square 6 overlaps one inner rectangle (all four separating
axes overlap strictly, with interval bounds) or leaves the container.

Slide domain. Each slider's physical range comes from its centre lying at least `1/2`
from every wall. The `(a, z)` domain is split adaptively: a part inside the target is
accepted, and every other part must be closed by a pair overlap among squares 5, 13 and
the non-slider squares, by the container, or by a branch and bound over square 6.
Because the intersection rectangle of square 5 over `[a1, a2]` keeps its left face at
`a1`, and that of square 13 over `[z1, z2]` keeps its lower-right face at `z2`, a wide
slide interval loses nothing on the face that squeezes square 6. The `(b, z)` domain,
with `z` above the certified `Z`, is closed the same way by squares 11 and 13 without
square 6.

The other faces. `a >= 0` is the container (`a_floor`). `b >= b*` is the 9/11 face,
which the local theorem drops but every packing obeys, through an exact separating-axis
lemma (`separation_lemma`, `b_floor`); `b* = -1.68496 r`. `z <= z*` joins that bound
to the 11/13 face (`z_ceiling`), with a pair cover above `Z_SPLIT`; `z* = 0.0241003`.
Square 13's own cell in the endpoint's state gives a second, independent ceiling
(`cell_slide_range`; `0.027916` on the unique design). The tight thresholds are then
re-proved with `z` capped and `a` floored.

Controls. Replacing the cell by every centre the container allows, or deleting square
13, must leave an open box for the `a` bound; deleting square 9 must leave the ceiling
cover open.

Not covered. The exp-238 root box is used; the exp-237 midpoint the local theorem uses
lies inside it. Squares 5, 11 and 13 turn by at most `r`, as in exp-244. `b*` and `z*`
are exact for the pairs they use; other contacts (9 on the left wall and on square 3)
may make the true extremes less negative or lower.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
import time
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from devtools import check_n17_capacity_one_cover as cover
from devtools.check_n17_endpoint_feasibility import THETA_LABELS, Box
from devtools.check_n17_local_minimum import DECLARED_BOX, DECLARED_RADIUS

SCHEMA = "n17-slider-coverage/v2"
SIX_CELL = "side-S2"
DEFAULT_DESIGN = cover.UNIQUE_24.name
LEGACY_DESIGN = cover.TABBED_24.name
SLIDERS = frozenset((5, 6, 11, 13))
GRID = 2**40
ANGLE_GRID = 2**32
KAPPA = Q(1, 2**28)
MAX_SLIDE_WIDTH = Q(7, 8)
SLIDE_STEP = Q(1, 2**12)
SIX_STEP = Q(1, 2**11)
SIX_NODE_LIMIT = 200_000
CONTROL_NODE_LIMIT = 20_000
Z_SPLIT = Q(1, 32)
# The H-268 thresholds (a_max, z_min, b_max) over the whole physical z range, and the
# tighter ones proved once z is capped by `z_ceiling` and a is floored by `a_floor`.
THRESHOLDS = (Q(21, 100), Q(-1, 20), Q(3, 40))
TIGHT = (Q(23, 200), Q(-49, 1000), Q(37, 500))
NEAR = Q(3, 2)

Interval = tuple[Q, Q]


def _down(value: Q, grid: int = GRID) -> Q:
    return Q(math.floor(value * grid), grid)


def _up(value: Q, grid: int = GRID) -> Q:
    return Q(math.ceil(value * grid), grid)


def _mul(a: Interval, b: Interval) -> Interval:
    values = (a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1])
    return min(values), max(values)


def _scale(k: Q, a: Interval) -> Interval:
    return (k * a[0], k * a[1]) if k >= 0 else (k * a[1], k * a[0])


def _add(a: Interval, b: Interval) -> Interval:
    return a[0] + b[0], a[1] + b[1]


def _abs_lo(a: Interval) -> Q:
    return Q(0) if a[0] <= 0 <= a[1] else min(abs(a[0]), abs(a[1]))


def _abs_hi(a: Interval) -> Q:
    return max(abs(a[0]), abs(a[1]))


@dataclass(frozen=True)
class Rect:
    """A rectangle: centre, unit axis `u` (with `v = (-u_y, u_x)`), half-extents."""

    cx: Q
    cy: Q
    ux: Q
    uy: Q
    p: Q
    q: Q

    def support(self, nx: Q, ny: Q) -> Q:
        return self.p * abs(nx * self.ux + ny * self.uy) + self.q * abs(
            -nx * self.uy + ny * self.ux
        )

    def vertices(self) -> tuple[tuple[Q, Q], ...]:
        vx, vy = -self.uy, self.ux
        return tuple(
            (
                self.cx + i * self.p * self.ux + j * self.q * vx,
                self.cy + i * self.p * self.uy + j * self.q * vy,
            )
            for i in (1, -1)
            for j in (1, -1)
        )

    def record(self) -> dict[str, str]:
        return {
            "centre": f"{float(self.cx):.9f},{float(self.cy):.9f}",
            "half": f"{float(self.p):.9f},{float(self.q):.9f}",
        }


def rects_overlap(first: Rect, second: Rect) -> bool:
    """Strict interior overlap of two rectangles, by all four separating axes."""
    dx, dy = second.cx - first.cx, second.cy - first.cy
    for nx, ny in (
        (first.ux, first.uy),
        (-first.uy, first.ux),
        (second.ux, second.uy),
        (-second.uy, second.ux),
    ):
        if abs(nx * dx + ny * dy) >= first.support(nx, ny) + second.support(nx, ny):
            return False
    return True


def leaves(rect: Rect, outer: Interval) -> bool:
    """Some vertex strictly outside the outer container bound."""
    lo, hi = outer
    return any(not (lo <= x <= hi and lo <= y <= hi) for x, y in rect.vertices())


@dataclass(frozen=True)
class Pose:
    """A square's exact nominal pose: centre and `u` axis as root-box intervals."""

    cx: Box
    cy: Box
    ux: Box
    uy: Box
    approx: tuple[Q, Q]


def _mid(box: Box) -> Q:
    return Q(round((box.lo + box.hi) / 2 * GRID), GRID)


def inner_rect(pose: Pose, offset: tuple[Box, Box], half_u: Q, half_v: Q) -> Rect | None:
    """A rational rectangle inside the pose's shrunk square moved by `offset`, checked."""
    if half_u <= KAPPA or half_v <= KAPPA:
        return None
    cx, cy = pose.cx + offset[0], pose.cy + offset[1]
    rect = Rect(_mid(cx), _mid(cy), *pose.approx, half_u - KAPPA, half_v - KAPPA)
    for x, y in rect.vertices():
        ex, ey = Box.point(x) - cx, Box.point(y) - cy
        along_u = (pose.ux * ex + pose.uy * ey).absolute().hi
        along_v = (pose.ux * ey - pose.uy * ex).absolute().hi
        if along_u > half_u or along_v > half_v:
            raise ValueError("inner rectangle is not inside the exact shrunk square")
    return rect


@dataclass(frozen=True)
class Scene:
    poses: dict[int, Pose]
    v: tuple[Box, Box]
    outer: Interval
    half: Q
    radius: Q
    cell: tuple[Q, Q, Q, Q]
    fixed: dict[int, Rect]
    provenance: dict[str, Any]
    design: str


def _cell_box(name: str, design: str = DEFAULT_DESIGN) -> tuple[Q, Q, Q, Q]:
    for cell in cover.build_cover(cover.DESIGNS[design]):
        if cell.name == name:
            xs = [x for x, _ in cell.vertices]
            ys = [y for _, y in cell.vertices]
            if len(cell.vertices) != 4 or len(set(xs)) != 2 or len(set(ys)) != 2:
                raise ValueError("square 6's cell must be an axis-parallel rectangle")
            return min(xs), max(xs), min(ys), max(ys)
    raise ValueError(f"no cell {name}")


def build_scene(
    radius: Q = DECLARED_RADIUS,
    cell: tuple[Q, Q, Q, Q] | None = None,
    design: str = DEFAULT_DESIGN,
) -> Scene:
    t_box, b_box, provenance = cover.load_root_box(cover.CERTIFICATE)
    point = cover.endpoint(t_box, b_box)
    aux = point.aux
    t_q = Q(round(t_box.lo * ANGLE_GRID), ANGLE_GRID)
    b_q = Q(round(b_box.lo * ANGLE_GRID), ANGLE_GRID)
    theta = ((1 - t_q * t_q) / (1 + t_q * t_q), 2 * t_q / (1 + t_q * t_q))
    beta = ((1 - b_q * b_q) / (1 + b_q * b_q), -2 * b_q / (1 + b_q * b_q))
    one, zero = Box.point(Q(1)), Box.point(Q(0))
    poses: dict[int, Pose] = {}
    for label, (cx, cy) in enumerate(point.centres, start=1):
        if label in THETA_LABELS:
            poses[label] = Pose(cx, cy, Box.cast(aux["c"]), Box.cast(aux["s"]), theta)
        elif label == 16:
            poses[label] = Pose(cx, cy, Box.cast(aux["d"]), -Box.cast(aux["e"]), beta)
        else:
            poses[label] = Pose(cx, cy, one, zero, (Q(1), Q(0)))
    shift = Box.cast(point.shift)
    outer = (shift.lo, cover.U - shift.lo)
    half = Q(1, 2) - 2 * radius
    six_cell = _cell_box(SIX_CELL, design) if cell is None else cell
    origin = (zero, zero)
    fixed = {
        label: rect
        for label, pose in poses.items()
        if label not in SLIDERS and (rect := inner_rect(pose, origin, half, half)) is not None
    }
    vx, vy = point.v
    return Scene(
        poses=poses,
        v=(Box.cast(vx), Box.cast(vy)),
        outer=outer,
        half=half,
        radius=radius,
        cell=six_cell,
        fixed=fixed,
        provenance=provenance,
        design=design,
    )


# ---------------------------------------------------------------------------
# Slider rectangles
# ---------------------------------------------------------------------------


def five_rect(scene: Scene, a: Interval) -> Rect | None:
    mid, width = (a[0] + a[1]) / 2, a[1] - a[0]
    offset = (Box.point(-mid), Box.point(Q(0)))
    return inner_rect(scene.poses[5], offset, scene.half - width / 2, scene.half)


def along_v_rect(scene: Scene, label: int, w: Interval, sign: int) -> Rect | None:
    mid, width = (w[0] + w[1]) / 2, w[1] - w[0]
    offset = (scene.v[0] * (sign * mid), scene.v[1] * (sign * mid))
    return inner_rect(scene.poses[label], offset, scene.half, scene.half - width / 2)


def physical_range(scene: Scene, label: int, direction: tuple[Box, Box]) -> Interval:
    """Range of `w` with the centre `c + w d + eps u` (|eps| <= r) at least 1/2 from walls."""
    pose = scene.poses[label]
    lo, hi = scene.outer
    eps = Box(-scene.radius, scene.radius)
    lows: list[Q] = []
    highs: list[Q] = []
    for centre, step, wobble in (
        (pose.cx, direction[0], eps * pose.ux),
        (pose.cy, direction[1], eps * pose.uy),
    ):
        if step.lo <= 0 <= step.hi:
            if step.lo == step.hi:
                continue
            raise ValueError("slide direction component straddles zero")
        first = (Box.point(lo + Q(1, 2)) - centre - wobble) / step
        second = (Box.point(hi - Q(1, 2)) - centre - wobble) / step
        if step.lo > 0:
            lows.append(first.lo)
            highs.append(second.hi)
        else:
            lows.append(second.lo)
            highs.append(first.hi)
    return _down(max(lows), 2**10), _up(min(highs), 2**10)


# ---------------------------------------------------------------------------
# Square 6
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SixBox:
    t: Interval
    x: Interval
    y: Interval


def trig(t: Interval) -> tuple[Interval, Interval]:
    t1, t2 = t
    cos = (_down((1 - t2 * t2) / (1 + t2 * t2)), _up((1 - t1 * t1) / (1 + t1 * t1)))
    sin = (_down(2 * t1 / (1 + t1 * t1)), _up(2 * t2 / (1 + t2 * t2)))
    return cos, sin


def six_overlaps(rect: Rect, box: SixBox, cos: Interval, sin: Interval) -> bool:
    """Square 6 overlaps `rect` at every point of `box` (outward interval bounds)."""
    dx = (box.x[0] - rect.cx, box.x[1] - rect.cx)
    dy = (box.y[0] - rect.cy, box.y[1] - rect.cy)
    for nx, ny, extent in ((rect.ux, rect.uy, rect.p), (-rect.uy, rect.ux, rect.q)):
        reach = _abs_hi(_add(_scale(nx, dx), _scale(ny, dy)))
        along = _add(_scale(nx, cos), _scale(ny, sin))
        across = _add(_scale(-nx, sin), _scale(ny, cos))
        if reach >= extent + (_abs_lo(along) + _abs_lo(across)) / 2:
            return False
    neg_sin = (-sin[1], -sin[0])
    for ax, ay in ((cos, sin), (neg_sin, cos)):
        reach = _abs_hi(_add(_mul(ax, dx), _mul(ay, dy)))
        on_u = _add(_scale(rect.ux, ax), _scale(rect.uy, ay))
        on_v = _add(_scale(-rect.uy, ax), _scale(rect.ux, ay))
        if reach >= Q(1, 2) + rect.p * _abs_lo(on_u) + rect.q * _abs_lo(on_v):
            return False
    return True


def six_leaves(box: SixBox, cos: Interval, sin: Interval, outer: Interval) -> bool:
    lo, hi = outer
    reach = (_abs_lo(cos) + _abs_lo(sin)) / 2
    return (
        box.x[1] - reach < lo
        or box.x[0] + reach > hi
        or box.y[1] - reach < lo
        or box.y[0] + reach > hi
    )


def _split(box: SixBox) -> tuple[SixBox, SixBox]:
    widths = (2 * (box.t[1] - box.t[0]), box.x[1] - box.x[0], box.y[1] - box.y[0])
    axis = widths.index(max(widths))
    lo, hi = (box.t, box.x, box.y)[axis]
    mid = (lo + hi) / 2
    parts = [(box.t, box.x, box.y), (box.t, box.x, box.y)]
    left, right = list(parts[0]), list(parts[1])
    left[axis], right[axis] = (lo, mid), (mid, hi)
    return SixBox(*left), SixBox(*right)


@dataclass
class SixResult:
    closed: bool
    nodes: int
    witness: SixBox | None
    exhausted: bool = False


def six_cover(
    obstacles: list[Rect],
    cell: tuple[Q, Q, Q, Q],
    outer: Interval,
    *,
    node_limit: int = SIX_NODE_LIMIT,
) -> SixResult:
    """Branch and bound: every turn and every centre of square 6 in the cell is blocked."""
    x0, x1, y0, y1 = cell
    near = [
        rect
        for rect in obstacles
        if max(rect.cx - x1, x0 - rect.cx, 0) ** 2 + max(rect.cy - y1, y0 - rect.cy, 0) ** 2
        < (NEAR + max(rect.p, rect.q)) ** 2
    ]
    stack = [SixBox((Q(i, 8), Q(i + 1, 8)), (x0, x1), (y0, y1)) for i in range(8)]
    nodes = 0
    while stack:
        box = stack.pop()
        nodes += 1
        if nodes > node_limit:
            return SixResult(closed=False, nodes=nodes, witness=box, exhausted=True)
        cos, sin = trig(box.t)
        if six_leaves(box, cos, sin, outer) or any(
            six_overlaps(rect, box, cos, sin) for rect in near
        ):
            continue
        if max(box.t[1] - box.t[0], box.x[1] - box.x[0], box.y[1] - box.y[0]) <= SIX_STEP:
            return SixResult(closed=False, nodes=nodes, witness=box)
        stack.extend(_split(box))
    return SixResult(closed=True, nodes=nodes, witness=None)


# ---------------------------------------------------------------------------
# The slide domains
# ---------------------------------------------------------------------------


@dataclass
class Outcome:
    passed: bool
    leaves: dict[str, int]
    six_nodes: int
    failure: dict[str, Any] | None


def _pair_reason(rects: dict[str, Rect], fixed: dict[int, Rect], outer: Interval) -> str | None:
    for name, rect in rects.items():
        if leaves(rect, outer):
            return f"{name}-container"
        for label, other in fixed.items():
            if rects_overlap(rect, other):
                return f"{name}-{label}"
    names = sorted(rects)
    for i, first in enumerate(names):
        for second in names[i + 1 :]:
            if rects_overlap(rects[first], rects[second]):
                return f"{first}-{second}"
    return None


def slide_cover(
    scene: Scene,
    a_max: Q,
    z_min: Q,
    *,
    without: frozenset[int] = frozenset(),
    node_limit: int = SIX_NODE_LIMIT,
    z_cap: Q | None = None,
    a_floor_value: Q | None = None,
) -> Outcome:
    """Every `(a, z)` outside `a <= a_max, z >= z_min` is infeasible.

    `z_cap` and `a_floor_value` cut the domain at a ceiling and a floor already proved
    for every packing in the premises (`z_ceiling`, `a_floor`); without them the whole
    physical range is searched.
    """
    a_range = physical_range(scene, 5, (Box.point(Q(-1)), Box.point(Q(0))))
    z_range = physical_range(scene, 13, scene.v)
    if z_cap is not None:
        z_range = (z_range[0], min(z_range[1], z_cap))
    if a_floor_value is not None:
        a_range = (max(a_range[0], a_floor_value), a_range[1])
    fixed = {label: rect for label, rect in scene.fixed.items() if label not in without}
    stack: list[tuple[Interval, Interval]] = [(a_range, z_range)]
    counts: dict[str, int] = {}
    six_nodes = 0
    while stack:
        a, z = stack.pop()
        if a[1] <= a_max and z[0] >= z_min:
            counts["target"] = counts.get("target", 0) + 1
            continue
        if a[0] < a_max < a[1]:
            stack += [((a[0], a_max), z), ((a_max, a[1]), z)]
            continue
        if z[0] < z_min < z[1]:
            stack += [(a, (z[0], z_min)), (a, (z_min, z[1]))]
            continue
        wide_a, wide_z = a[1] - a[0], z[1] - z[0]
        if max(wide_a, wide_z) > MAX_SLIDE_WIDTH:
            stack += _halve(a, z)
            continue
        rects: dict[str, Rect] = {}
        five = five_rect(scene, a)
        if five is not None:
            rects["5"] = five
        if 13 not in without:
            thirteen = along_v_rect(scene, 13, z, 1)
            if thirteen is not None:
                rects["13"] = thirteen
        reason = _pair_reason(rects, fixed, scene.outer)
        if reason is None:
            result = six_cover(
                [*fixed.values(), *rects.values()],
                scene.cell,
                scene.outer,
                node_limit=node_limit,
            )
            six_nodes += result.nodes
            if result.closed:
                reason = "six"
            elif result.exhausted or max(wide_a, wide_z) <= SLIDE_STEP:
                witness = result.witness
                return Outcome(
                    passed=False,
                    leaves=counts,
                    six_nodes=six_nodes,
                    failure={
                        "node_limit_reached": result.exhausted,
                        "a": [str(a[0]), str(a[1])],
                        "z": [str(z[0]), str(z[1])],
                        "six_box": None
                        if witness is None
                        else {
                            "tau": [float(v) for v in witness.t],
                            "x": [float(v) for v in witness.x],
                            "y": [float(v) for v in witness.y],
                        },
                    },
                )
        if reason is None:
            stack += _halve(a, z)
            continue
        key = "six" if reason == "six" else "pair"
        counts[key] = counts.get(key, 0) + 1
    return Outcome(passed=True, leaves=counts, six_nodes=six_nodes, failure=None)


def _halve(a: Interval, z: Interval) -> list[tuple[Interval, Interval]]:
    if a[1] - a[0] >= z[1] - z[0]:
        mid = (a[0] + a[1]) / 2
        return [((a[0], mid), z), ((mid, a[1]), z)]
    mid = (z[0] + z[1]) / 2
    return [(a, (z[0], mid)), (a, (mid, z[1]))]


def b_cover(scene: Scene, b_max: Q, z_min: Q) -> Outcome:
    """Every `(b, z)` with `z >= z_min` and `b > b_max` is infeasible (squares 11, 13)."""
    minus_v = (-scene.v[0], -scene.v[1])
    b_range = physical_range(scene, 11, minus_v)
    z_range = physical_range(scene, 13, scene.v)
    stack: list[tuple[Interval, Interval]] = [
        ((max(b_range[0], b_max), b_range[1]), (z_min, z_range[1]))
    ]
    counts: dict[str, int] = {}
    while stack:
        b, z = stack.pop()
        if b[1] <= b[0]:
            continue
        wide = max(b[1] - b[0], z[1] - z[0])
        if wide <= MAX_SLIDE_WIDTH:
            candidates = (
                ("11", along_v_rect(scene, 11, b, -1)),
                ("13", along_v_rect(scene, 13, z, 1)),
            )
            rects = {name: rect for name, rect in candidates if rect is not None}
            reason = _pair_reason(rects, scene.fixed, scene.outer)
            if reason is not None:
                counts["pair"] = counts.get("pair", 0) + 1
                continue
            if wide <= SLIDE_STEP:
                return Outcome(
                    passed=False,
                    leaves=counts,
                    six_nodes=0,
                    failure={"b": [str(b[0]), str(b[1])], "z": [str(z[0]), str(z[1])]},
                )
        if b[1] - b[0] >= z[1] - z[0]:
            mid = (b[0] + b[1]) / 2
            stack += [((b[0], mid), z), ((mid, b[1]), z)]
        else:
            mid = (z[0] + z[1]) / 2
            stack += [(b, (z[0], mid)), (b, (mid, z[1]))]
    return Outcome(passed=True, leaves=counts, six_nodes=0, failure=None)


# ---------------------------------------------------------------------------
# The faces square 6 does not reach: a >= 0, b >= b*, z <= z*
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Trig:
    """Outward rational bounds on `sin r`, `cos r`, `tan r` and `sec r`."""

    sin: Box
    cos: Box
    tan: Box
    sec: Box


def trig_radius(radius: Q) -> Trig:
    """Alternating Taylor bounds, valid for `0 < r <= 1`."""
    if not 0 < radius <= 1:
        raise ValueError("the turn radius must lie in (0, 1]")
    sin = Box(radius - radius**3 / 6, radius)
    cos = Box(1 - radius**2 / 2, 1 - radius**2 / 2 + radius**4 / 24)
    return Trig(sin=sin, cos=cos, tan=sin / cos, sec=cos.reciprocal())


@dataclass(frozen=True)
class Stack:
    """Square `upper` on square `lower` along `v`: `c_upper - c_lower = tau u + gap v`."""

    upper: int
    lower: int
    tau: Box
    gap: Box


def stack(scene: Scene, upper: int, lower: int) -> Stack:
    top, bottom = scene.poses[upper], scene.poses[lower]
    dx, dy = top.cx - bottom.cx, top.cy - bottom.cy
    ux, uy = bottom.ux, bottom.uy
    vx, vy = scene.v
    return Stack(upper, lower, ux * dx + uy * dy, vx * dx + vy * dy)


def separation_lemma(lateral: Box, normal: Box, trig: Trig) -> bool:
    """The hypotheses under which two frame squares can only separate along `+v`.

    Two closed unit squares turned by at most `r` from the frame, with centre difference
    `T u + D v` (`T` in `lateral`, `D` in `normal`), have disjoint interiors only through
    a normal `R(omega) v` with `D cos omega - T sin omega >= 1`, provided
    `|T| + |D| sin r < 1` (no `u`-type normal separates), `D > -1 + |T| sin r` (no
    `-v`-type normal does) and `T <= -sin r` (so `(1 + T sin w)/cos w` falls on
    `[-r, r]` and its least value is `sec r + T tan r`, at `w = r`).
    """
    t_abs = lateral.absolute().hi
    d_abs = normal.absolute().hi
    return (
        t_abs + d_abs * trig.sin.hi < 1
        and normal.lo > -1 + t_abs * trig.sin.hi
        and lateral.hi <= -trig.sin.hi
    )


def _l1(first: Box, second: Box) -> Box:
    """`|first| + |second|` as an interval."""
    return first.absolute() + second.absolute()


@dataclass
class Face:
    passed: bool
    record: dict[str, Any]


def endpoint_state(design: str) -> dict[int, cover.Cell]:
    """The endpoint's occupancy state on the design: each label's assigned cell."""
    cells = cover.build_cover(cover.DESIGNS[design])
    t_box, b_box, _ = cover.load_root_box(cover.CERTIFICATE)
    record = cover.family_state(cells, cover.endpoint(t_box, b_box), cover.ENDPOINT)
    if not record["one_state"]:
        raise ValueError(f"the endpoint has no state on {design}")
    by_name = {cell.name: cell for cell in cells}
    return {entry["label"]: by_name[entry["cell"]] for entry in record["squares"]}


def cell_slide_range(
    pose: Pose, cell: cover.Cell, step: tuple[Box, Box], wobble: tuple[Box, Box], radius: Q
) -> Interval | None:
    """Slides `w` with the centre `c + w step + eps wobble` (`|eps| <= r`) in the cell.

    Each edge of the counterclockwise cell is a halfplane `cross(E, q - p) >= 0`; the
    centre's unknown `eps` is taken at its worst, so the interval holds every member.
    """
    lows: list[Q] = []
    highs: list[Q] = []
    count = len(cell.vertices)
    for index in range(count):
        px, py = cell.vertices[index]
        qx, qy = cell.vertices[(index + 1) % count]
        ex, ey = qx - px, qy - py
        base = (pose.cy - py) * ex - (pose.cx - px) * ey
        slope = step[1] * ex - step[0] * ey
        spread = (wobble[1] * ex - wobble[0] * ey).absolute().hi * radius
        if slope.lo > 0:
            numerator = -base.hi - spread
            lows.append(numerator / (slope.hi if numerator >= 0 else slope.lo))
        elif slope.hi < 0:
            numerator = base.hi + spread
            highs.append(numerator / (-slope.hi if numerator >= 0 else -slope.lo))
        elif slope.lo != 0 or slope.hi != 0:
            raise ValueError("slide direction straddles a cell edge")
        elif base.hi + spread < 0:
            return None
    if not lows or not highs:
        raise ValueError("the cell does not bound the slide on both sides")
    return max(lows), min(highs)


def a_floor(scene: Scene) -> Face:
    """`a >= 0`: square 5 starts on the right wall, and a turn only widens its reach.

    The H-258 frame keeps the container's lower-left corner at the origin, so a packing of
    side `S <= S*` has its right wall at `S`. Square 5's centre is `x5* - a` with
    `x5* = S* - 1/2` in `_layout`, and its reach to the right is
    `h(omega5) = (|cos omega5| + |sin omega5|)/2 >= 1/2`, so
    `S* - 1/2 - a + h(omega5) <= S <= S*` gives `a >= h(omega5) - 1/2 + (S* - S) >= 0`.
    Neither `eta5` nor the size of `omega5` enters; equality holds at the endpoint itself.
    The one datum, `x5* = S* - 1/2`, is checked exactly at the root box's rational
    midpoint, where the layout's point intervals are exact (it is the literal entry
    `(side - half, half)` of the H256 layout, so it holds at every root parameter).
    """
    t_mid = (Q(scene.provenance["t_box"][0]) + Q(scene.provenance["t_box"][1])) / 2
    b_mid = (Q(scene.provenance["b_box"][0]) + Q(scene.provenance["b_box"][1])) / 2
    point = cover.endpoint(Box.point(t_mid), Box.point(b_mid))
    x5, y5 = point.centres[4]
    shift = point.shift
    wall = Box.point(cover.U) - shift
    on_wall = (
        all(box.lo == box.hi for box in (x5, y5, shift))
        and x5 + Q(1, 2) == wall
        and y5 - Q(1, 2) == shift
    )
    return Face(
        passed=on_wall,
        record={
            "a_min": "0",
            "exact": True,
            "attained": "at the endpoint (omega5 = 0, S = S*)",
            "square_5_on_right_wall_exact": on_wall,
            "method": "container: a >= h(omega5) - 1/2 + (S* - S) >= 0",
        },
    )


def b_floor(scene: Scene, b_top: Q) -> tuple[Face, Box]:
    """`b >= b*` from the 9/11 face alone, and `b*` exactly (an interval over the root box).

    Square 9 above square 11: `T = tau0 + u.delta9 - eps11`, `D = D0 + v.delta9 + b`,
    with `delta9 = (xi9, eta9)` and `eps11 = u.V11` each within `r`. By
    `separation_lemma` every packing has `D >= sec r + T tan r`, so
    `b >= sec r - D0 + tau0 tan r - eps11 tan r + (tan r u - v).delta9`, linear in the
    perturbations; its least value over the box is

        b* = sec r - D0 + tau0 tan r - r tan r - r (|tan r ux - vx| + |tan r uy - vy|),

    attained by two touching squares both turned by `+r`, square 11 moved `+r` along `u`
    and square 9 by `-r sign(tan r u - v)`. The lemma's hypotheses are checked on the whole
    range `b in [physical low, b_top]`.
    """
    trig = trig_radius(scene.radius)
    pair = stack(scene, 9, 11)
    r = scene.radius
    pose = scene.poses[11]
    ux, uy = pose.ux, pose.uy
    vx, vy = scene.v
    reach_u = r * _l1(ux, uy).hi
    reach_v = r * _l1(vx, vy).hi
    lateral = pair.tau + Box(-reach_u - r, reach_u + r)
    b_low = physical_range(scene, 11, (-vx, -vy))[0]
    normal = pair.gap + Box(-reach_v, reach_v) + Box(min(b_low, Q(0)), b_top)
    lemma = separation_lemma(lateral, normal, trig)
    weights = _l1(trig.tan * ux - vx, trig.tan * uy - vy)
    exact = trig.sec - pair.gap + pair.tau * trig.tan - trig.tan * r - weights * r
    return (
        Face(
            passed=lemma and exact.hi < 0,
            record={
                "b_star": _box_record(exact),
                "b_star_over_r": [float(exact.lo / r), float(exact.hi / r)],
                "certified_floor": str(_down(exact.lo)),
                "lemma_hypotheses": lemma,
                "lemma_range_b": [str(min(b_low, Q(0))), str(b_top)],
                "tau0": _box_record(pair.tau),
                "D0": _box_record(pair.gap),
                "method": (
                    "9/11 separating-axis lemma; least value at both squares turned by +r, "
                    "eps11 = +r, delta9 = -r sign(tan r u - v)"
                ),
            },
        ),
        exact,
    )


def z_ceiling(
    scene: Scene, b_floor_value: Q, b_max: Q, z_min: Q, z_split: Q
) -> tuple[Face, Box]:
    """`z <= z*` from the chain 9/11/13, closed above `z_split` by the pair cover.

    Square 11 above square 13: `T' = tau1 + eps11 - eps13`, `D' = D1 - b - z`. For
    `z in [z_min, z_split]` and `b in [b*, b_max]` the lemma gives
    `z <= D1 - b - sec r - T' tan r`, and with the 9/11 bound on `b` (the same `eps11`
    and `delta9`), `eps11` cancels:

        z* = D1 + D0 - 2 sec r - (tau0 + tau1) tan r + r tan r
             + r (|vx - tan r ux| + |vy - tan r uy|),

    attained when 9, 11 and 13 touch in a column, all turned by `+r`. Above `z_split`
    every `(b, z)` with `b in [b_floor, b_max]` is closed by an overlap of the inner
    rectangles of 11 and 13 with each other, the non-sliders or the container.
    """
    trig = trig_radius(scene.radius)
    low, high = stack(scene, 9, 11), stack(scene, 11, 13)
    r = scene.radius
    pose = scene.poses[11]
    ux, uy = pose.ux, pose.uy
    vx, vy = scene.v
    lateral = high.tau + Box(-2 * r, 2 * r)
    normal = high.gap - Box(b_floor_value, b_max) - Box(z_min, z_split)
    lemma = separation_lemma(lateral, normal, trig)
    weights = _l1(vx - trig.tan * ux, vy - trig.tan * uy)
    exact = (
        high.gap
        + low.gap
        - 2 * trig.sec
        - (low.tau + high.tau) * trig.tan
        + trig.tan * r
        + weights * r
    )
    cover = z_cover(scene, (b_floor_value, b_max), z_split)
    ceiling = _up(exact.hi)
    return (
        Face(
            passed=lemma and ceiling < z_split and cover.passed,
            record={
                "z_star": _box_record(exact),
                "certified_ceiling": str(ceiling),
                "lemma_hypotheses": lemma,
                "lemma_range": {
                    "b": [str(b_floor_value), str(b_max)],
                    "z": [str(z_min), str(z_split)],
                },
                "tau1": _box_record(high.tau),
                "D1": _box_record(high.gap),
                "z_split": str(z_split),
                "above_split": _outcome_record(cover),
                "method": (
                    "11/13 and 9/11 separating-axis lemmas joined through b (eps11 cancels); "
                    "pair cover of 11 and 13 above z_split"
                ),
            },
        ),
        exact,
    )


def z_cover(
    scene: Scene, b: Interval, z_from: Q, *, without: frozenset[int] = frozenset()
) -> Outcome:
    """Every `(b, z)` with `b` in the interval and `z >= z_from` is infeasible."""
    fixed = {label: rect for label, rect in scene.fixed.items() if label not in without}
    z_range = physical_range(scene, 13, scene.v)
    stack_: list[tuple[Interval, Interval]] = [(b, (z_from, max(z_from, z_range[1])))]
    counts: dict[str, int] = {}
    while stack_:
        bb, zz = stack_.pop()
        if zz[1] <= zz[0] or bb[1] <= bb[0]:
            continue
        wide = max(bb[1] - bb[0], zz[1] - zz[0])
        if wide <= MAX_SLIDE_WIDTH:
            candidates = (
                ("11", along_v_rect(scene, 11, bb, -1)),
                ("13", along_v_rect(scene, 13, zz, 1)),
            )
            rects = {name: rect for name, rect in candidates if rect is not None}
            if _pair_reason(rects, fixed, scene.outer) is not None:
                counts["pair"] = counts.get("pair", 0) + 1
                continue
            if wide <= SLIDE_STEP:
                return Outcome(
                    passed=False,
                    leaves=counts,
                    six_nodes=0,
                    failure={"b": [str(bb[0]), str(bb[1])], "z": [str(zz[0]), str(zz[1])]},
                )
        if bb[1] - bb[0] >= zz[1] - zz[0]:
            mid = (bb[0] + bb[1]) / 2
            stack_ += [((bb[0], mid), zz), ((mid, bb[1]), zz)]
        else:
            mid = (zz[0] + zz[1]) / 2
            stack_ += [(bb, (zz[0], mid)), (bb, (mid, zz[1]))]
    return Outcome(passed=True, leaves=counts, six_nodes=0, failure=None)


def _box_record(box: Box) -> dict[str, Any]:
    return {"lo": float(box.lo), "hi": float(box.hi), "width": float(box.hi - box.lo)}


# ---------------------------------------------------------------------------
# Receipt
# ---------------------------------------------------------------------------


def _outcome_record(outcome: Outcome) -> dict[str, Any]:
    return {
        "passed": outcome.passed,
        "leaves": outcome.leaves,
        "six_nodes": outcome.six_nodes,
        "failure": outcome.failure,
    }


def _slide_ranges(scene: Scene, state: dict[int, cover.Cell]) -> dict[str, Interval | None]:
    one, zero = Box.point(Q(1)), Box.point(Q(0))
    vx, vy = scene.v
    u = (scene.poses[11].ux, scene.poses[11].uy)
    across = (zero, one)
    return {
        "a": cell_slide_range(scene.poses[5], state[5], (-one, zero), across, scene.radius),
        "b": cell_slide_range(scene.poses[11], state[11], (-vx, -vy), u, scene.radius),
        "z": cell_slide_range(scene.poses[13], state[13], (vx, vy), u, scene.radius),
    }


def _interval_record(interval: Interval | None) -> dict[str, Any] | None:
    if interval is None:
        return None
    return {
        "exact": [str(interval[0]), str(interval[1])],
        "float": [float(interval[0]), float(interval[1])],
    }


def run(
    a_max: Q,
    z_min: Q,
    b_max: Q,
    *,
    design: str = DEFAULT_DESIGN,
    tight: tuple[Q, Q, Q] | None = None,
    z_split: Q = Z_SPLIT,
    controls: bool = True,
) -> dict[str, Any]:
    started = time.monotonic()
    scene = build_scene(design=design)
    state = endpoint_state(design)
    timings: dict[str, float] = {}
    stage = time.monotonic()
    claim = slide_cover(scene, a_max, z_min)
    timings["a_z"] = time.monotonic() - stage
    stage = time.monotonic()
    b_outcome = b_cover(scene, b_max, z_min)
    timings["b"] = time.monotonic() - stage

    # The faces square 6 does not reach, and what the endpoint's cells give.
    stage = time.monotonic()
    a_face = a_floor(scene)
    b_face, b_star = b_floor(scene, b_max)
    b_low = _down(b_star.lo)
    z_face, _ = z_ceiling(scene, b_low, b_max, z_min, z_split)
    z_chain = Q(z_face.record["certified_ceiling"])
    cells = _slide_ranges(scene, state)
    z_cell = cells["z"]
    caps = [z_chain] if z_face.passed and claim.passed and b_outcome.passed else []
    if z_cell is not None:
        caps.append(_up(z_cell[1]))
    z_cap = min(caps) if caps else None
    timings["faces"] = time.monotonic() - stage

    tight_record: dict[str, Any] | None = None
    box_a, box_z, box_b = a_max, z_min, b_max
    if tight is not None:
        stage = time.monotonic()
        tight_a, tight_z, tight_b = tight
        floor = Q(0) if a_face.passed else None
        tight_az = slide_cover(scene, tight_a, tight_z, z_cap=z_cap, a_floor_value=floor)
        tight_bz = b_cover(scene, tight_b, tight_z) if tight_az.passed else None
        timings["tight"] = time.monotonic() - stage
        tight_record = {
            "a_max": str(tight_a),
            "z_min": str(tight_z),
            "b_max": str(tight_b),
            "z_cap": None if z_cap is None else str(z_cap),
            "a_z": _outcome_record(tight_az),
            "b": None if tight_bz is None else _outcome_record(tight_bz),
        }
        if tight_az.passed:
            box_a, box_z = min(a_max, tight_a), max(z_min, tight_z)
            if tight_bz is not None and tight_bz.passed:
                box_b = min(b_max, tight_b)

    control_records: dict[str, Any] = {}
    if controls:
        stage = time.monotonic()
        lo, hi = scene.outer
        whole = (lo + Q(1, 2), hi - Q(1, 2), lo + Q(1, 2), hi - Q(1, 2))
        whole_scene = build_scene(cell=whole, design=design)
        refused_whole = slide_cover(whole_scene, a_max, z_min, node_limit=CONTROL_NODE_LIMIT)
        refused_13 = slide_cover(scene, a_max, z_min, without=frozenset({13}))
        free_b = physical_range(scene, 11, (-scene.v[0], -scene.v[1]))[0]
        refused_floor = z_cover(scene, (free_b, b_max), z_split, without=frozenset({9}))
        control_records = {
            "whole_box_cell_refused": not refused_whole.passed,
            "whole_box_cell": _outcome_record(refused_whole),
            "without_13_refused": not refused_13.passed,
            "without_13": _outcome_record(refused_13),
            "without_9_refused": not refused_floor.passed,
            "without_9": _outcome_record(refused_floor),
        }
        timings["controls"] = time.monotonic() - stage

    a_cell, b_cell = cells["a"], cells["b"]
    certified: dict[str, Interval] = {
        "a": (
            max(Q(0), a_cell[0]) if a_cell else Q(0),
            min(box_a, a_cell[1]) if a_cell else box_a,
        ),
        "b": (
            max(b_low, b_cell[0]) if b_cell else b_low,
            min(box_b, b_cell[1]) if b_cell else box_b,
        ),
        "z": (
            max(box_z, z_cell[0]) if z_cell else box_z,
            z_cap if z_cap is not None else Q(10),
        ),
    }
    declared: dict[str, tuple[Q, Q]] = dict(zip(("a", "b", "z"), DECLARED_BOX, strict=True))
    inside = {
        name: declared[name][0] <= low and high <= declared[name][1]
        for name, (low, high) in certified.items()
    }
    widened = {
        name: [str(min(declared[name][0], low)), str(max(declared[name][1], high))]
        for name, (low, high) in certified.items()
    }
    checks = {
        "a_z_bound": claim.passed,
        "b_bound": b_outcome.passed,
        "state_cell_of_6": state[6].name == SIX_CELL,
        "a_floor": a_face.passed,
        "b_floor": b_face.passed,
        "z_ceiling": z_face.passed or (z_cell is not None and z_cap is not None),
    }
    if controls:
        checks["controls_refused"] = bool(
            control_records["whole_box_cell_refused"]
            and control_records["without_13_refused"]
            and control_records["without_9_refused"]
        )
    timings["total"] = time.monotonic() - started
    source = Path(__file__).read_bytes()
    return {
        "schema": SCHEMA,
        "scope": (
            "H-268 slide bounds: square 6 in its cell of the endpoint's state at any turn, "
            "the other non-slider coordinates within the radius, the container [0, S]^2 with "
            "S <= S*; exact rationals, outward intervals"
        ),
        "module_sha256": hashlib.sha256(source).hexdigest(),
        "design": design,
        "root": scene.provenance,
        "radius": str(scene.radius),
        "state": {str(label): cell.name for label, cell in sorted(state.items())},
        "cell": {"name": SIX_CELL, "box": [str(v) for v in scene.cell]},
        "outer_container": [str(v) for v in scene.outer],
        "thresholds": {"a_max": str(a_max), "z_min": str(z_min), "b_max": str(b_max)},
        "margins": {
            "a": str(DECLARED_BOX[0][1] - a_max),
            "z": str(z_min - DECLARED_BOX[2][0]),
            "b": str(DECLARED_BOX[1][1] - b_max),
        },
        "a_z": _outcome_record(claim),
        "b": {"z_min_used": str(z_min), **_outcome_record(b_outcome)},
        "faces": {
            "a_floor": a_face.record,
            "b_floor": b_face.record,
            "z_ceiling_chain": z_face.record,
            "cells_of_the_state": {
                "premise": (
                    "each slider's centre in its own cell of the endpoint's state, with its "
                    "u (or eta5) coordinate within the radius"
                ),
                "cells": {"a": state[5].name, "b": state[11].name, "z": state[13].name},
                "ranges": {name: _interval_record(value) for name, value in cells.items()},
            },
            "z_cap": None if z_cap is None else str(z_cap),
        },
        "premise_by_face": {
            "a_min": "container (square 5's cell gives only a >= -shift)",
            "a_max": "square 6 in its cell, with z <= z_cap",
            "b_min": "9/11 nonoverlap (square 11's cell gives far less)",
            "b_max": "11/13 nonoverlap with z >= z_min",
            "z_min": "square 6 in its cell",
            "z_max": (
                "least of square 13's cell and the 9/11/13 chain"
                if z_cell is not None
                else "the 9/11/13 chain"
            ),
        },
        "tight": tight_record,
        "certified_box": {
            name: {
                "exact": [str(low), str(high)],
                "float": [float(low), float(high)],
                "inside_declared": inside[name],
            }
            for name, (low, high) in certified.items()
        },
        "declared_box": {name: [str(v) for v in pair] for name, pair in declared.items()},
        "inside_declared_box": all(inside.values()),
        "smallest_containing_box": widened,
        "controls": control_records,
        "checks": checks,
        "passed": all(checks.values()),
        "timing_seconds": {key: round(value, 3) for key, value in timings.items()},
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or SCHEMA).splitlines()[0])
    parser.add_argument("--design", choices=sorted(cover.DESIGNS), default=DEFAULT_DESIGN)
    parser.add_argument("--a-max", type=Q, default=THRESHOLDS[0])
    parser.add_argument("--z-min", type=Q, default=THRESHOLDS[1])
    parser.add_argument("--b-max", type=Q, default=THRESHOLDS[2])
    parser.add_argument("--tight-a", type=Q, default=TIGHT[0])
    parser.add_argument("--tight-z", type=Q, default=TIGHT[1])
    parser.add_argument("--tight-b", type=Q, default=TIGHT[2])
    parser.add_argument("--no-tight", action="store_true")
    parser.add_argument("--z-split", type=Q, default=Z_SPLIT)
    parser.add_argument("--no-controls", action="store_true")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args(argv)
    tight = None if args.no_tight else (args.tight_a, args.tight_z, args.tight_b)
    try:
        receipt = run(
            args.a_max,
            args.z_min,
            args.b_max,
            design=args.design,
            tight=tight,
            z_split=args.z_split,
            controls=not args.no_controls,
        )
    except (ValueError, OSError, KeyError) as error:
        print(json.dumps({"schema": SCHEMA, "passed": False, "error": str(error)}))
        return 2
    encoded = json.dumps(receipt, sort_keys=True, indent=1)
    if args.output is not None:
        args.output.write_text(encoded + "\n")
    keys = ("passed", "design", "checks", "inside_declared_box", "timing_seconds")
    summary = {key: receipt[key] for key in keys}
    summary["certified_box"] = {
        name: entry["exact"] for name, entry in receipt["certified_box"].items()
    }
    sys.stdout.write(json.dumps(summary, sort_keys=True) + "\n")
    return 0 if receipt["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
