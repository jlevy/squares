"""Heuristic selector of forbidden n17 occupancy sub-patterns (H-267). Not a certificate.

What it selects. On a capacity-one cover of the n17 centre box (H-266), a sub-pattern is
a set `G` of `k` cells. It is *forbidden* when `k` unit squares, each with its centre in
its own closed cell of `G`, any orientations, all inside the cap container `[0, U]^2`,
cannot have pairwise disjoint interiors. Every state containing a forbidden pattern, in
any D4 image, is excluded. This module only *selects* candidates: it searches hard for a
feasible placement and flags a pattern when every attempt leaves a penetration above a
margin. A flag is a float heuristic. The prover (the n11 kernel adapted to n17) must
certify each flagged pattern before any exclusion counts, and the counts here are what
certification of all of them would give, not a result.

Patterns tested. A pattern is tested only when it is connected in the interaction graph,
whose edges join cells at distance below sqrt(2): two unit squares with centres at least
sqrt(2) apart lie in discs that meet in at most a point, so such a pair never collides,
and a disconnected pattern is feasible exactly when each component is. The reduction is
exact for the consumer, because a disconnected forbidden pattern contains a smaller
connected forbidden one. On the minimal cover it removes little (212 of 276 cell pairs
interact), so the budget knob is the window: with `--window W` a pattern is tested only
when the union of its cells fits in an axis-aligned `W x W` square of the centre box,
the local shape of n11's fields. The default is no window, which tests every connected
class. Classes are taken up to D4, bottom up by arity, and a pattern containing an
already flagged one is skipped, since the consumer needs only the minimal flagged set.

Restriction to survivors. With `--restrict-to-survivors K`, at every arity `k >= K` a
class is tested only when it lies in some state that survives every flag of arity below
`k`; the classes this skips beyond the superset rule are counted per arity as
`restricted_out`, beside the number of surviving states it used. The flags come in whole
D4 orbits, so the surviving states are closed under D4, and a class lies in an image of
a surviving state exactly when its canonical mask lies in a surviving state. The
restriction is exact for the consumer. A class in no surviving state can remove only
states that are already removed. And every connected `k - 1`-cell sub-pattern of a class
that is tested lies in the same surviving state, which survives the lower flags too, so it
was tested, and the class gets the warm starts, the generator and so the verdict it gets
without the option; by induction the two runs agree on every tested class and on every
survivor count. They differ only in flagging classes that remove nothing. `--count-only`
measures the restriction without searching, under the flags of an earlier receipt
(`--flags-from`). The option is off by default, and the receipt is then unchanged.

Priority. Flags are crowds: at arity 7, seed 1, all 41 new flags have at most two pairs
of cells that do not interact, against 8,211 of the 43,052 classes tested. Where the
restriction applies, classes are therefore searched fewest missing pairs first, so a
wall ceiling cuts the least crowded, and `--max-missing-pairs D` keeps only those with at
most `D` missing pairs. That subset is a priority choice, not exact: the classes it
defers are unsearched, their flags unknown, and they leave no warm start for the arity
above, so it is meant for the last arity of a run.

Search. Variables are the centres, the angles, and for each interacting pair a
separating line (normal angle and offset). The penalty sums squared hinge violations of
every square vertex against the container walls, every centre against its cell's
halfplanes, and every vertex against its side of each pair's line. It is C^1 and zero
exactly on feasible placements with a witnessing line per pair, touching included.
Each attempt is an L-BFGS-B descent; a promising attempt is polished. The verdict
measure is not the penalty but the true violation of the pose: the largest of every
pair's separating-axis penetration, every container excursion and every cell
excursion, in length units. Starts are, in order, the witnesses of the pattern's
`k - 1`-cell sub-patterns with one square added at random, uniform random poses, then
basin hops from the best pose found; a pattern still unplaced gets a deep stage of
redrawn witnesses, random poses and narrow and wide hops (`Budget`). Last, the finish:
one long descent of the same penalty from the best pose (`FINISH`, on by default since
H-267's residue survey; `--no-finish` restores the search without it). A pattern is
flagged only if every attempt and the finish end above the margin; the best violation
found is reported with it. The search must be strong, not only the margin careful: on the
bulk-exclusion lane's design (`ring-3-voronoi-8`) its sampling proxy flagged eleven
arity-five classes, and this search places every one, most in one to three attempts. The
finish exists because an attempt's descent stops at 600 iterations and is polished only
below 1e-4: on the endpoint's own 17-cell state every attempt stalls near 2e-3, and the
one long descent places it exactly.

Re-checking flags (`--recheck RECEIPT ...`). Each class an earlier receipt flagged is
searched again under the current budget: its `k - 1`-cell sub-patterns first, each by the
search without its deep stage, and their witnesses then warm start the class's own full
search, as in a sweep. The receipt lists each flag as still flagged with its new best
penetration, or placed with its pose, and the survivors over the flags that remain.

Determinism. Every pattern draws from its own generator, seeded by the run seed and the
pattern's cell mask, and uses only results of lower arities, so the receipt apart from
timings is the same for any worker count and scheduling.

Positive controls, checked first. The endpoint (H256 layout over the exp-238 root box,
embedded at the cap) is placed in its own state on the cover, and its violation at its
own pose is evaluated; every sub-pattern of that state, in every D4 image, is witnessed
feasible there and can never be flagged. The search itself runs blind to that pose, so
any endpoint sub-pattern it would have flagged is counted as a false flag, and the run
fails if there is one. Tight controls shrink the endpoint's cells to small boxes about
its centres, so the endpoint's touching contacts are close to the only placements, and
the search must still reach the margin. The margin is chosen so these pass with room.

Consumer. Every `17`-subset of the cells is a closed capacity-one assignment (the H260
convention of `check_n17_capacity_one_cover`). States containing a flagged pattern in
any D4 image are removed by direct bitmask enumeration, survivors are counted, and their
D4 orbits are counted twice, by Burnside's fixed counts and by distinct canonical forms.
A greedy order of the flagged classes, each taking the most surviving states left, is
the order in which certifying them pays most.
"""

from __future__ import annotations

import argparse
import contextlib
import copy
import ctypes
import functools
import hashlib
import itertools
import json
import math
import time
from collections.abc import Iterator
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import minimize

from devtools import check_n17_capacity_one_cover as cover
from devtools.check_n17_endpoint_feasibility import THETA_LABELS
from devtools.provenance import provenance

SCHEMA = "n17-sub-pattern-selector/v1"
COUNT_SCHEMA = "n17-sub-pattern-class-count/v1"
STATUS = (
    "heuristic selector, not a certificate: a flagged pattern is one the float search "
    "could not place; the prover must certify each flagged pattern before any exclusion "
    "counts"
)
DEFAULT_DESIGN = cover.UNIQUE_24.name
DESIGN_COMMIT = {cover.UNIQUE_24.name: "0dabde12"}
CAP = float(cover.U)
TARGET = cover.TARGET
MARGIN = 1e-6
POLISH_BELOW = 1e-4
# One long descent of the selector's penalty, the finish. Measured by the residue survey on
# the endpoint's state: from the search's best attempt at 1.7e-3, 1,605 iterations reach a
# penalty of exactly zero.
FINISH: dict[str, Any] = {"maxiter": 20000, "ftol": 1e-30, "gtol": 1e-20, "maxcor": 30}
RECHECK_SCHEMA = "n17-sub-pattern-recheck/v1"
INTERACTION = math.sqrt(2.0) + 1e-9
ENDPOINT_POSE_TOLERANCE = 1e-12
TIGHT_HALF_SIDE = 1e-3
# The bytes this process imported, read now: a receipt written later must not name the file
# on disk then, which may have been edited while a long run was searching.
PROVENANCE = provenance(Path(__file__))
CORNER_X = np.array([-0.5, 0.5, 0.5, -0.5])
CORNER_Y = np.array([-0.5, -0.5, 0.5, 0.5])

Floats = NDArray[np.float64]


# ---------------------------------------------------------------------------
# Geometry
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Geometry:
    """Float cells, their halfplanes, a permutation group on them, and the cap."""

    cap: float
    names: tuple[str, ...]
    polygons: tuple[Floats, ...]
    halfplanes: tuple[Floats, ...]
    group: tuple[tuple[int, ...], ...]
    actions: tuple[str, ...]
    interact: NDArray[np.bool_]
    lower: Floats
    upper: Floats


def _ccw(polygon: Floats) -> Floats:
    x, y = polygon[:, 0], polygon[:, 1]
    area = float(np.dot(x, np.roll(y, -1)) - np.dot(np.roll(x, -1), y))
    return polygon if area > 0 else polygon[::-1].copy()


def _halfplanes(polygon: Floats) -> Floats:
    """Rows `(a, b, c)` with unit `(a, b)`: the closed cell is `a x + b y <= c`."""
    rows: list[list[float]] = []
    for index in range(len(polygon)):
        start, end = polygon[index], polygon[(index + 1) % len(polygon)]
        ex, ey = float(end[0] - start[0]), float(end[1] - start[1])
        length = math.hypot(ex, ey)
        a, b = ey / length, -ex / length
        rows.append([a, b, a * float(start[0]) + b * float(start[1])])
    return np.array(rows)


def _segment_distance(point: Floats, start: Floats, end: Floats) -> float:
    edge = end - start
    t = float(np.clip(np.dot(point - start, edge) / np.dot(edge, edge), 0.0, 1.0))
    return float(np.linalg.norm(point - start - t * edge))


def _cross(origin: Floats, a: Floats, b: Floats) -> float:
    return float(
        (a[0] - origin[0]) * (b[1] - origin[1]) - (a[1] - origin[1]) * (b[0] - origin[0])
    )


def _segments_cross(p: Floats, q: Floats, r: Floats, s: Floats) -> bool:
    """Proper crossing only; touching and collinear contact put a vertex in the other cell."""
    return (_cross(p, q, r) * _cross(p, q, s) < 0) and (_cross(r, s, p) * _cross(r, s, q) < 0)


def polygon_distance(first: Floats, second: Floats) -> float:
    """Distance between two convex polygons, zero when they meet."""
    for a, b in ((first, second), (second, first)):
        planes = _halfplanes(b)
        for x, y in a:
            if np.all(planes[:, 0] * x + planes[:, 1] * y <= planes[:, 2] + 1e-12):
                return 0.0
    edges_first = [(first[i], first[(i + 1) % len(first)]) for i in range(len(first))]
    edges_second = [(second[i], second[(i + 1) % len(second)]) for i in range(len(second))]
    for p, q in edges_first:
        for r, s in edges_second:
            if _segments_cross(p, q, r, s):
                return 0.0
    best = math.inf
    for a, b in ((first, second), (second, first)):
        for point in a:
            for index in range(len(b)):
                best = min(best, _segment_distance(point, b[index], b[(index + 1) % len(b)]))
    return best


def make_geometry(
    polygons: list[Floats],
    names: list[str],
    *,
    cap: float = CAP,
    group: list[tuple[int, ...]] | None = None,
    actions: list[str] | None = None,
) -> Geometry:
    polygons = [_ccw(np.asarray(polygon, dtype=np.float64)) for polygon in polygons]
    count = len(polygons)
    interact = np.zeros((count, count), dtype=np.bool_)
    for i, j in itertools.combinations(range(count), 2):
        near = polygon_distance(polygons[i], polygons[j]) < INTERACTION
        interact[i, j] = interact[j, i] = near
    identity = tuple(range(count))
    return Geometry(
        cap=cap,
        names=tuple(names),
        polygons=tuple(polygons),
        halfplanes=tuple(_halfplanes(polygon) for polygon in polygons),
        group=tuple(group) if group is not None else (identity,),
        actions=tuple(actions) if actions is not None else ("r0",),
        interact=interact,
        lower=np.array([polygon.min(axis=0) for polygon in polygons]),
        upper=np.array([polygon.max(axis=0) for polygon in polygons]),
    )


def cover_geometry(design_name: str = DEFAULT_DESIGN) -> Geometry:
    """The named H-266 cover as float cells with its D4 permutations."""
    cells = cover.build_cover(cover.DESIGNS[design_name])
    permutations = cover.d4_permutations(cells)
    if permutations is None:
        raise ValueError(f"design {design_name} is not D4-invariant")
    polygons = [np.array([[float(x), float(y)] for x, y in cell.vertices]) for cell in cells]
    return make_geometry(
        polygons,
        [cell.name for cell in cells],
        group=[tuple(permutations[action]) for action in cover.D4],
        actions=list(cover.D4),
    )


def mask_of(cells: tuple[int, ...] | list[int]) -> int:
    return sum(1 << cell for cell in cells)


def cells_of(mask: int) -> tuple[int, ...]:
    return tuple(index for index in range(mask.bit_length()) if mask >> index & 1)


def image_mask(mask: int, permutation: tuple[int, ...]) -> int:
    return sum(1 << permutation[cell] for cell in cells_of(mask))


def canonical(mask: int, group: tuple[tuple[int, ...], ...]) -> int:
    return min(image_mask(mask, permutation) for permutation in group)


def orbit(mask: int, group: tuple[tuple[int, ...], ...]) -> set[int]:
    return {image_mask(mask, permutation) for permutation in group}


def connected(geometry: Geometry, cells: tuple[int, ...]) -> bool:
    seen, stack = {cells[0]}, [cells[0]]
    while stack:
        current = stack.pop()
        for other in cells:
            if other not in seen and geometry.interact[current, other]:
                seen.add(other)
                stack.append(other)
    return len(seen) == len(cells)


def missing_pairs(geometry: Geometry, mask: int) -> int:
    """The pairs of the pattern's cells that do not interact; zero for mutual neighbours."""
    cells = list(cells_of(mask))
    near = int(np.count_nonzero(np.triu(geometry.interact[np.ix_(cells, cells)], 1)))
    return len(cells) * (len(cells) - 1) // 2 - near


def window_side(geometry: Geometry, cells: tuple[int, ...]) -> float:
    """The side of the least axis-aligned square holding the union of the cells."""
    index = list(cells)
    extent = geometry.upper[index].max(axis=0) - geometry.lower[index].min(axis=0)
    return float(extent.max())


def pattern_classes(geometry: Geometry, arity: int, window: float | None) -> list[int]:
    """Canonical masks of the connected (and windowed) classes of one arity, sorted."""
    classes: set[int] = set()
    for cells in itertools.combinations(range(len(geometry.names)), arity):
        if window is not None and window_side(geometry, cells) > window:
            continue
        if connected(geometry, cells):
            classes.add(canonical(mask_of(cells), geometry.group))
    return sorted(classes)


def occurring_classes(classes: list[int], alive: NDArray[np.int64]) -> set[int]:
    """The classes whose mask lies in some state of `alive`.

    For `alive` closed under the group, as the survivors of whole flagged orbits are, this
    is the set of classes that occur in some group image of a surviving state.
    """
    return {mask for mask in classes if bool(np.any((alive & mask) == mask))}


def split_classes(
    classes: list[int], flagged_images: list[int], alive: NDArray[np.int64] | None
) -> tuple[list[int], list[int], list[int]]:
    """Classes pruned as supersets of a flag, restricted out, and to be tested.

    `alive` is `None` where the restriction does not apply, and nothing is restricted out.
    """
    pruned = [m for m in classes if any(f & m == f for f in flagged_images)]
    pruned_set = set(pruned)
    candidates = [m for m in classes if m not in pruned_set]
    if alive is None:
        return pruned, [], candidates
    occurring = occurring_classes(candidates, alive)
    restricted = [m for m in candidates if m not in occurring]
    return pruned, restricted, [m for m in candidates if m in occurring]


# ---------------------------------------------------------------------------
# One pattern: penalty, violation, local descent
# ---------------------------------------------------------------------------


class Problem:
    """The smooth penetration penalty and the true violation for one pattern.

    A pose is a `(k, 3)` array of centre `x`, centre `y` and angle, in the order of
    `cells`. The descent vector adds a normal angle and an offset per interacting pair.
    """

    def __init__(
        self, geometry: Geometry, cells: tuple[int, ...], *, fast: bool = False
    ) -> None:
        self.cap = geometry.cap
        self.cells = cells
        k = len(cells)
        self.k = k
        pairs = [
            (a, b)
            for a, b in itertools.combinations(range(k), 2)
            if geometry.interact[cells[a], cells[b]]
        ]
        self.p = len(pairs)
        self.first = np.array([a for a, _ in pairs], dtype=np.intp)
        self.second = np.array([b for _, b in pairs], dtype=np.intp)
        width = max(len(geometry.halfplanes[cell]) for cell in cells)
        self.plane_a = np.zeros((k, width))
        self.plane_b = np.zeros((k, width))
        self.plane_c = np.ones((k, width))
        self.plane_count = [len(geometry.halfplanes[cell]) for cell in cells]
        for row, cell in enumerate(cells):
            planes = geometry.halfplanes[cell]
            self.plane_a[row, : len(planes)] = planes[:, 0]
            self.plane_b[row, : len(planes)] = planes[:, 1]
            self.plane_c[row, : len(planes)] = planes[:, 2]
        self.polygons = [geometry.polygons[cell] for cell in cells]
        self.lower = geometry.lower[list(cells)]
        self.upper = geometry.upper[list(cells)]
        # The vectorised penalty: both ends of every pair in one array, the scatter to the
        # squares as one product with an incidence matrix. Equal to `penalty` up to the
        # order of floating-point sums.
        self.ends = np.concatenate([self.first, self.second])
        self.side = np.concatenate([np.ones(self.p), -np.ones(self.p)])[:, None]
        self.incidence = np.zeros((k, 2 * self.p))
        self.incidence[self.ends, np.arange(2 * self.p)] = 1.0
        self.objective = self.penalty_vectorised if fast else self.penalty

    def pack(self, pose: Floats) -> Floats:
        """The descent vector of a pose, each pair's line through the centres' midpoint."""
        x, y = pose[:, 0], pose[:, 1]
        dx = x[self.second] - x[self.first]
        dy = y[self.second] - y[self.first]
        phi = np.arctan2(dy, dx)
        offset = (np.cos(phi) * (x[self.first] + x[self.second])) / 2 + (
            np.sin(phi) * (y[self.first] + y[self.second])
        ) / 2
        return np.concatenate([x, y, pose[:, 2], phi, offset])

    def pose(self, z: Floats) -> Floats:
        k = self.k
        return np.stack([z[:k], z[k : 2 * k], z[2 * k : 3 * k]], axis=1)

    def penalty(self, z: Floats) -> tuple[float, Floats]:
        """Squared hinge violations and their gradient."""
        k, p, cap = self.k, self.p, self.cap
        x, y, angle = z[:k], z[k : 2 * k], z[2 * k : 3 * k]
        phi, offset = z[3 * k : 3 * k + p], z[3 * k + p :]
        cos_t, sin_t = np.cos(angle)[:, None], np.sin(angle)[:, None]
        ox = cos_t * CORNER_X - sin_t * CORNER_Y
        oy = sin_t * CORNER_X + cos_t * CORNER_Y
        vx, vy = x[:, None] + ox, y[:, None] + oy
        low_x, high_x = np.minimum(vx, 0.0), np.maximum(vx - cap, 0.0)
        low_y, high_y = np.minimum(vy, 0.0), np.maximum(vy - cap, 0.0)
        value = float(
            (low_x * low_x).sum()
            + (high_x * high_x).sum()
            + (low_y * low_y).sum()
            + (high_y * high_y).sum()
        )
        grad_vx = 2.0 * (low_x + high_x)
        grad_vy = 2.0 * (low_y + high_y)
        excess = np.maximum(
            self.plane_a * x[:, None] + self.plane_b * y[:, None] - self.plane_c, 0.0
        )
        value += float((excess * excess).sum())
        grad_x = 2.0 * (excess * self.plane_a).sum(axis=1)
        grad_y = 2.0 * (excess * self.plane_b).sum(axis=1)
        grad_phi = np.zeros(p)
        grad_offset = np.zeros(p)
        if p:
            nx, ny = np.cos(phi)[:, None], np.sin(phi)[:, None]
            vx_first, vy_first = vx[self.first], vy[self.first]
            vx_second, vy_second = vx[self.second], vy[self.second]
            over_first = np.maximum(nx * vx_first + ny * vy_first - offset[:, None], 0.0)
            over_second = np.maximum(offset[:, None] - nx * vx_second - ny * vy_second, 0.0)
            value += float((over_first * over_first).sum() + (over_second * over_second).sum())
            # Elementwise scatter: a BLAS product here would spawn threads per call.
            np.add.at(grad_vx, self.first, 2.0 * over_first * nx)
            np.add.at(grad_vx, self.second, -2.0 * over_second * nx)
            np.add.at(grad_vy, self.first, 2.0 * over_first * ny)
            np.add.at(grad_vy, self.second, -2.0 * over_second * ny)
            turn_first = -ny * vx_first + nx * vy_first
            turn_second = -ny * vx_second + nx * vy_second
            grad_phi = 2.0 * ((over_first * turn_first).sum(axis=1)) - 2.0 * (
                (over_second * turn_second).sum(axis=1)
            )
            grad_offset = -2.0 * over_first.sum(axis=1) + 2.0 * over_second.sum(axis=1)
        grad_x += grad_vx.sum(axis=1)
        grad_y += grad_vy.sum(axis=1)
        grad_t = (grad_vy * ox - grad_vx * oy).sum(axis=1)
        return value, np.concatenate([grad_x, grad_y, grad_t, grad_phi, grad_offset])

    def penalty_vectorised(self, z: Floats) -> tuple[float, Floats]:
        """`penalty` with fewer array operations; equal up to rounding of the sums."""
        k, p, cap = self.k, self.p, self.cap
        x, y, angle = z[:k], z[k : 2 * k], z[2 * k : 3 * k]
        cos_t, sin_t = np.cos(angle)[:, None], np.sin(angle)[:, None]
        ox = cos_t * CORNER_X - sin_t * CORNER_Y
        oy = sin_t * CORNER_X + cos_t * CORNER_Y
        vx, vy = x[:, None] + ox, y[:, None] + oy
        out_x = vx - np.clip(vx, 0.0, cap)
        out_y = vy - np.clip(vy, 0.0, cap)
        excess = np.maximum(
            self.plane_a * x[:, None] + self.plane_b * y[:, None] - self.plane_c, 0.0
        )
        value = float(np.vdot(out_x, out_x) + np.vdot(out_y, out_y) + np.vdot(excess, excess))
        grad_vx, grad_vy = 2.0 * out_x, 2.0 * out_y
        grad_x = 2.0 * (excess * self.plane_a).sum(axis=1)
        grad_y = 2.0 * (excess * self.plane_b).sum(axis=1)
        grad_phi = np.zeros(p)
        grad_offset = np.zeros(p)
        if p:
            phi, offset = z[3 * k : 3 * k + p], z[3 * k + p :]
            nx = np.tile(np.cos(phi), 2)[:, None]
            ny = np.tile(np.sin(phi), 2)[:, None]
            ends_x, ends_y = vx[self.ends], vy[self.ends]
            over = np.maximum(
                self.side * (nx * ends_x + ny * ends_y - np.tile(offset, 2)[:, None]), 0.0
            )
            value += float(np.vdot(over, over))
            weight = 2.0 * self.side * over
            grad_vx += self.incidence @ (weight * nx)
            grad_vy += self.incidence @ (weight * ny)
            turn = (weight * (nx * ends_y - ny * ends_x)).sum(axis=1)
            pull = weight.sum(axis=1)
            grad_phi = turn[:p] + turn[p:]
            grad_offset = -(pull[:p] + pull[p:])
        grad_x += grad_vx.sum(axis=1)
        grad_y += grad_vy.sum(axis=1)
        grad_t = (grad_vy * ox - grad_vx * oy).sum(axis=1)
        return value, np.concatenate([grad_x, grad_y, grad_t, grad_phi, grad_offset])

    def violations(self, pose: Floats) -> dict[str, float]:
        """True violations of a pose in length units: pair, container and cell."""
        x, y, angle = pose[:, 0], pose[:, 1], pose[:, 2]
        support = (np.abs(np.cos(angle)) + np.abs(np.sin(angle))) / 2
        container = np.max(
            [support - x, x - (self.cap - support), support - y, y - (self.cap - support)]
        )
        cell = np.max(self.plane_a * x[:, None] + self.plane_b * y[:, None] - self.plane_c)
        pair = 0.0
        if self.p:
            first, second = self.first, self.second
            dx, dy = x[second] - x[first], y[second] - y[first]
            axes = np.stack(
                [
                    angle[first],
                    angle[first] + np.pi / 2,
                    angle[second],
                    angle[second] + np.pi / 2,
                ]
            )
            reach = np.abs(np.cos(axes) * dx + np.sin(axes) * dy)
            gap = (
                reach
                - (np.abs(np.cos(angle[first] - axes)) + np.abs(np.sin(angle[first] - axes)))
                / 2
                - (np.abs(np.cos(angle[second] - axes)) + np.abs(np.sin(angle[second] - axes)))
                / 2
            )
            pair = float(-gap.max(axis=0).min())
        return {
            "pair": max(pair, 0.0),
            "container": max(float(container), 0.0),
            "cell": max(float(cell), 0.0),
        }

    def violation(self, pose: Floats) -> float:
        return max(self.violations(pose).values())

    def random_centre(self, row: int, rng: np.random.Generator) -> tuple[float, float]:
        low, high = self.lower[row], self.upper[row]
        width = self.plane_count[row]
        a, b, c = (
            self.plane_a[row, :width],
            self.plane_b[row, :width],
            self.plane_c[row, :width],
        )
        for _ in range(1000):
            x, y = rng.uniform(low[0], high[0]), rng.uniform(low[1], high[1])
            if np.all(a * x + b * y <= c):
                return float(x), float(y)
        centre = self.polygons[row].mean(axis=0)
        return float(centre[0]), float(centre[1])

    def random_pose(self, rng: np.random.Generator) -> Floats:
        pose = np.empty((self.k, 3))
        for row in range(self.k):
            pose[row, :2] = self.random_centre(row, rng)
        pose[:, 2] = rng.uniform(0.0, np.pi / 2, self.k)
        return pose

    def descend(self, pose: Floats, *, polish: bool, early_stop: bool = False) -> Floats:
        """One L-BFGS-B descent; with `early_stop`, it ends once the penalty is negligible.

        A penalty at most `EARLY_STOP_PENALTY` bounds every hinge term by its square root,
        1e-7, so every wall, cell and separating-line excursion is below a tenth of the
        margin, and the pose is placed whatever further descent would do.
        """
        options: dict[str, Any] = (
            {"maxiter": 1500, "ftol": 1e-24, "gtol": 1e-18, "maxcor": 30}
            if polish
            else {"maxiter": 600, "ftol": 1e-15, "gtol": 1e-12, "maxcor": 20}
        )
        callback = _stop_when_negligible if early_stop else None
        result = minimize(
            self.objective,
            self.pack(pose),
            jac=True,
            method="L-BFGS-B",
            options=options,
            callback=callback,
        )
        return self.pose(np.asarray(result.x, dtype=np.float64))


EARLY_STOP_PENALTY = 1e-14


def _stop_when_negligible(intermediate_result: Any) -> None:
    if intermediate_result.fun <= EARLY_STOP_PENALTY:
        raise StopIteration


@functools.cache
def _blas_thread_controls() -> tuple[tuple[Any, Any], ...]:
    """The thread setter and getter of every loaded scipy-openblas; empty if none is found."""
    maps = Path("/proc/self/maps")
    if not maps.exists():
        return ()
    paths = sorted(
        {
            line.split()[-1]
            for line in maps.read_text(encoding="utf-8").splitlines()
            if "openblas" in line.lower() and line.split()[-1].startswith("/")
        }
    )
    controls: list[tuple[Any, Any]] = []
    for path in paths:
        try:
            library = ctypes.CDLL(path)
        except OSError:
            continue
        for suffix in ("64_", ""):
            setter = getattr(library, f"scipy_openblas_set_num_threads{suffix}", None)
            getter = getattr(library, f"scipy_openblas_get_num_threads{suffix}", None)
            if setter is not None and getter is not None:
                controls.append((setter, getter))
                break
    return tuple(controls)


@contextlib.contextmanager
def single_thread_blas() -> Iterator[None]:
    """One BLAS thread while searching, restored after.

    L-BFGS-B's dense steps are tiny here, and waking a thread pool on each of them made a
    search ten times slower in wall time and twice as expensive in CPU (measured).
    """
    controls = _blas_thread_controls()
    saved = [int(getter()) for _, getter in controls]
    for setter, _ in controls:
        setter(1)
    try:
        yield
    finally:
        for (setter, _), count in zip(controls, saved, strict=True):
            setter(count)


@dataclass
class Verdict:
    """A pattern's search outcome: the best pose and its violation over all attempts."""

    mask: int
    cells: tuple[int, ...]
    feasible: bool
    violation: float
    pose: Floats
    attempts: int
    found_by: str
    components: dict[str, float] = field(default_factory=dict[str, float])


@dataclass(frozen=True)
class Budget:
    """Attempts per pattern: sub-pattern warm starts, random starts, basin hops.

    The deep stage runs only for a pattern the first stage could not place: the
    sub-pattern witnesses again with the added square redrawn, alternating with random
    poses, then hops alternating between the narrow and the wide kick. At seed 1 the first
    stage alone flagged two arity-six classes that other seeds placed in 3 and 77 to 127
    attempts, one of them excluding half of all states, which is what the deep stage is for.
    With `finish`, a pattern still unplaced gets one long descent from its best pose.
    """

    starts: int = 12
    hops: int = 24
    hop_centre: float = 0.08
    hop_angle: float = 0.35
    deep_starts: int = 256
    deep_hops: int = 256
    wide_centre: float = 0.25
    wide_angle: float = 0.8
    margin: float = MARGIN
    finish: bool = True
    early_stop: bool = False
    fast_penalty: bool = False


def finish(problem: Problem, pose: Floats) -> Floats:
    """One long descent of the selector's penalty from a pose (`FINISH`)."""
    with single_thread_blas():
        result = minimize(
            problem.objective, problem.pack(pose), jac=True, method="L-BFGS-B", options=FINISH
        )
    return problem.pose(np.asarray(result.x, dtype=np.float64))


def search(
    geometry: Geometry,
    cells: tuple[int, ...],
    rng: np.random.Generator,
    budget: Budget,
    warm: list[tuple[int, Floats]] | None = None,
) -> Verdict:
    """Try hard to place the pattern; feasible as soon as one pose is within the margin."""
    return search_resumable(geometry, cells, rng, budget, warm)[0]


@dataclass
class Checkpoint:
    """A search's state after its first `deep_starts_done` deep starts, still unplaced.

    A budget with the same prefix (`budget_prefix`) and at least as many deep starts, on a
    generator with the same seed and from the same warm starts, passes through exactly this
    state: the attempts so far, the best pose, the generator's state and the warm starts are
    all it carries forward. It may resume here instead of repeating the attempts before it.
    """

    mask: int
    prefix: Budget
    stream: tuple[Any, ...]
    deep_starts_done: int
    best: tuple[float, Floats] | None
    attempts: int
    rng_state: dict[str, Any]
    templates: list[tuple[int, Floats]]


def budget_prefix(budget: Budget) -> Budget:
    """The fields that decide a class's search, warm starts included, up to any point in
    its deep starts: all but the deep stage's length, the deep hops and the wide kick.

    The finish stays in. The class's own search reaches it only after the deep stage, but
    `recheck_flag` searches the sub-patterns with this budget less its deep stage, finish
    included, and their witnesses are the class's warm starts.
    """
    return replace(budget, deep_starts=0, deep_hops=0, wide_centre=0.0, wide_angle=0.0)


def generator_stream(rng: np.random.Generator) -> tuple[Any, ...]:
    """The seed a generator was made from, which a resumed search must share."""
    seed = rng.bit_generator.seed_seq
    if isinstance(seed, np.random.SeedSequence):
        return (repr(seed.entropy), seed.spawn_key)
    return (repr(seed),)


def search_resumable(
    geometry: Geometry,
    cells: tuple[int, ...],
    rng: np.random.Generator,
    budget: Budget,
    warm: list[tuple[int, Floats]] | None = None,
    *,
    checkpoint_at: int | None = None,
    resume: Checkpoint | None = None,
) -> tuple[Verdict, Checkpoint | None]:
    """`search`, also returning its state after `checkpoint_at` deep starts (None if it is
    placed), or continuing from a checkpoint, which holds its own warm starts."""
    if resume is not None and (
        warm is not None
        or resume.mask != mask_of(cells)
        or resume.prefix != budget_prefix(budget)
        or resume.stream != generator_stream(rng)
        or resume.deep_starts_done > budget.deep_starts
    ):
        raise ValueError(
            "the checkpoint was written for another pattern, seed or budget prefix"
        )
    with single_thread_blas():
        return _search(
            geometry, cells, rng, budget, warm, checkpoint_at=checkpoint_at, resume=resume
        )


def _search(
    geometry: Geometry,
    cells: tuple[int, ...],
    rng: np.random.Generator,
    budget: Budget,
    warm: list[tuple[int, Floats]] | None,
    *,
    checkpoint_at: int | None = None,
    resume: Checkpoint | None = None,
) -> tuple[Verdict, Checkpoint | None]:
    problem = Problem(geometry, cells, fast=budget.fast_penalty)
    best: tuple[float, Floats] | None = None
    attempts = 0
    snapshot: Checkpoint | None = None

    def attempt(start: Floats, how: str) -> Verdict | None:
        nonlocal best, attempts
        attempts += 1
        pose = problem.descend(start, polish=False, early_stop=budget.early_stop)
        value = problem.violation(pose)
        if budget.margin < value < POLISH_BELOW:
            polished = problem.descend(pose, polish=True, early_stop=budget.early_stop)
            polished_value = problem.violation(polished)
            if polished_value < value:
                pose, value = polished, polished_value
        if best is None or value < best[0]:
            best = (value, pose)
        if value <= budget.margin:
            return Verdict(
                mask_of(cells),
                cells,
                feasible=True,
                violation=value,
                pose=pose,
                attempts=attempts,
                found_by=how,
                components=problem.violations(pose),
            )
        return None

    def hop(centre: float, angle: float) -> Floats:
        assert best is not None
        start = best[1].copy()
        start[:, :2] += rng.normal(0.0, centre, (problem.k, 2))
        start[:, 2] += rng.normal(0.0, angle, problem.k)
        return start

    def redraw(template: tuple[int, Floats]) -> Floats:
        row, start = template[0], template[1].copy()
        start[row, :2] = problem.random_centre(row, rng)
        start[row, 2] = rng.uniform(0.0, np.pi / 2)
        return start

    def keep(done: int) -> None:
        nonlocal snapshot
        if checkpoint_at != done:
            return
        snapshot = Checkpoint(
            mask_of(cells),
            budget_prefix(budget),
            generator_stream(rng),
            done,
            best,
            attempts,
            dict(copy.deepcopy(rng.bit_generator.state)),
            templates,
        )

    if resume is not None:
        best, attempts = resume.best, resume.attempts
        rng.bit_generator.state = copy.deepcopy(resume.rng_state)
        templates = resume.templates
        first_deep = resume.deep_starts_done
    else:
        templates = warm or []
        first_deep = 0
        for _, start in templates:
            outcome = attempt(start, "warm")
            if outcome is not None:
                return outcome, None
        for _ in range(budget.starts):
            outcome = attempt(problem.random_pose(rng), "random")
            if outcome is not None:
                return outcome, None
        for _ in range(budget.hops):
            outcome = attempt(hop(budget.hop_centre, budget.hop_angle), "hop")
            if outcome is not None:
                return outcome, None
    keep(first_deep)
    for index in range(first_deep, budget.deep_starts):
        if templates and index % 2 == 0:
            start, how = redraw(templates[(index // 2) % len(templates)]), "deep-warm"
        else:
            start, how = problem.random_pose(rng), "deep-random"
        outcome = attempt(start, how)
        if outcome is not None:
            return outcome, None
        keep(index + 1)
    for index in range(budget.deep_hops):
        start = (
            hop(budget.hop_centre, budget.hop_angle)
            if index % 2 == 0
            else hop(budget.wide_centre, budget.wide_angle)
        )
        outcome = attempt(start, "deep-hop")
        if outcome is not None:
            return outcome, None
    assert best is not None
    feasible, how = False, "none"
    if budget.finish:
        attempts += 1
        finished = finish(problem, best[1])
        finished_value = problem.violation(finished)
        if finished_value < best[0]:
            best = (finished_value, finished)
        if finished_value <= budget.margin:
            feasible, how = True, "finish"
    value, pose = best
    verdict = Verdict(
        mask_of(cells),
        cells,
        feasible=feasible,
        violation=value,
        pose=pose,
        attempts=attempts,
        found_by=how,
        components=problem.violations(pose),
    )
    return verdict, None if feasible else snapshot


def pattern_rng(seed: int, mask: int) -> np.random.Generator:
    return np.random.default_rng(np.random.SeedSequence([seed, mask]))


# ---------------------------------------------------------------------------
# Witness transport under the group
# ---------------------------------------------------------------------------


def transform_pose(
    geometry: Geometry, cells: tuple[int, ...], pose: Floats, element: int
) -> tuple[tuple[int, ...], Floats]:
    """The image of a witness under one group element, rows sorted by image cell."""
    action = geometry.actions[element]
    permutation = geometry.group[element]
    half = geometry.cap / 2
    x, y, angle = pose[:, 0] - half, pose[:, 1] - half, pose[:, 2].copy()
    if action[0] == "f":
        x, angle = -x, -angle
    for _ in range(int(action[1])):
        x, y = -y, x
        angle = angle + np.pi / 2
    image = np.stack([x + half, y + half, np.mod(angle, np.pi / 2)], axis=1)
    targets = [permutation[cell] for cell in cells]
    order = sorted(range(len(cells)), key=lambda row: targets[row])
    return tuple(targets[row] for row in order), image[order]


def warm_starts(
    geometry: Geometry,
    cells: tuple[int, ...],
    witnesses: dict[int, Floats],
    rng: np.random.Generator,
) -> list[tuple[int, Floats]]:
    """Each `k - 1`-cell witness, with the missing square (its row) added at random."""
    problem: Problem | None = None
    starts: list[tuple[int, Floats]] = []
    for row, _ in enumerate(cells):
        rest = cells[:row] + cells[row + 1 :]
        witness = witnesses.get(mask_of(rest))
        if witness is None:
            continue
        if problem is None:
            problem = Problem(geometry, cells)
        start = np.empty((len(cells), 3))
        start[:row], start[row + 1 :] = witness[:row], witness[row:]
        start[row, :2] = problem.random_centre(row, rng)
        start[row, 2] = rng.uniform(0.0, np.pi / 2)
        starts.append((row, start))
    return starts


# ---------------------------------------------------------------------------
# The endpoint and the positive controls
# ---------------------------------------------------------------------------


def _middle(value: Any) -> float:
    return float((value.lo + value.hi) / 2)


def endpoint_pose(design_name: str = DEFAULT_DESIGN) -> dict[str, Any]:
    """The endpoint's cells and pose on the cover: label, cell index, centre and angle."""
    design = cover.DESIGNS[design_name]
    cells = cover.build_cover(design)
    t, b, _ = cover.load_root_box(cover.CERTIFICATE)
    point = cover.endpoint(t, b)
    family = cover.family_state(cells, point, cover.ENDPOINT)
    if not family["one_state"]:
        raise ValueError(f"the endpoint is in no single state of {design_name}")
    index = {cell.name: k for k, cell in enumerate(cells)}
    theta = math.atan2(_middle(point.aux["u"][1]), _middle(point.aux["u"][0]))
    beta = math.atan2(_middle(point.aux["p"][1]), _middle(point.aux["p"][0]))
    rows: list[tuple[int, int, float, float, float]] = []
    for entry in family["squares"]:
        label = entry["label"]
        x, y = point.centres[label - 1]
        angle = theta if label in THETA_LABELS else beta if label == 16 else 0.0
        rows.append((index[entry["cell"]], label, _middle(x), _middle(y), angle))
    rows.sort()
    return {
        "cells": tuple(row[0] for row in rows),
        "labels": tuple(row[1] for row in rows),
        "pose": np.array([[row[2], row[3], math.fmod(row[4], math.pi / 2)] for row in rows]),
    }


def endpoint_witnesses(
    geometry: Geometry, endpoint: dict[str, Any], max_arity: int
) -> tuple[set[int], dict[str, Any]]:
    """Every class of an endpoint sub-pattern, witnessed feasible at the endpoint pose."""
    cells: tuple[int, ...] = endpoint["cells"]
    pose: Floats = endpoint["pose"]
    whole = Problem(geometry, cells).violations(pose)
    witnessed: set[int] = set()
    worst = 0.0
    for arity in range(1, max_arity + 1):
        for rows in itertools.combinations(range(len(cells)), arity):
            sub = tuple(cells[row] for row in rows)
            worst = max(worst, Problem(geometry, sub).violation(pose[list(rows)]))
            witnessed.add(canonical(mask_of(sub), geometry.group))
    record = {
        "state": [geometry.names[cell] for cell in cells],
        "labels": list(endpoint["labels"]),
        "violation_at_pose": whole,
        "worst_sub_pattern_violation_at_pose": worst,
        "tolerance": ENDPOINT_POSE_TOLERANCE,
        "witnessed_classes": len(witnessed),
        "passed": max(whole.values()) <= ENDPOINT_POSE_TOLERANCE
        and worst <= ENDPOINT_POSE_TOLERANCE,
    }
    return witnessed, record


def tight_control(
    geometry: Geometry,
    endpoint: dict[str, Any],
    rows: tuple[int, ...],
    *,
    seed: int,
    budget: Budget,
    half_side: float = TIGHT_HALF_SIDE,
) -> dict[str, Any]:
    """Endpoint squares in small boxes about their own centres, searched from random poses."""
    pose: Floats = endpoint["pose"]
    boxes = [
        np.array(
            [
                [pose[row, 0] - half_side, pose[row, 1] - half_side],
                [pose[row, 0] + half_side, pose[row, 1] - half_side],
                [pose[row, 0] + half_side, pose[row, 1] + half_side],
                [pose[row, 0] - half_side, pose[row, 1] + half_side],
            ]
        )
        for row in rows
    ]
    tight = make_geometry(
        boxes,
        [f"endpoint-{endpoint['labels'][row]}" for row in rows],
        cap=geometry.cap,
    )
    cells = tuple(range(len(rows)))
    verdict = search(tight, cells, pattern_rng(seed, mask_of(rows)), budget)
    return {
        "labels": [endpoint["labels"][row] for row in rows],
        "half_side": half_side,
        "best_violation": verdict.violation,
        "attempts": verdict.attempts,
        "passed": verdict.feasible,
    }


def contact_clusters(endpoint: dict[str, Any], size: int) -> list[tuple[int, ...]]:
    """Sets of endpoint squares grown from each square through its nearest neighbours."""
    pose: Floats = endpoint["pose"]
    centres = pose[:, :2]
    clusters: set[tuple[int, ...]] = set()
    for seed_row in range(len(centres)):
        chosen = [seed_row]
        while len(chosen) < size:
            distance = np.min(
                np.linalg.norm(centres[:, None, :] - centres[None, chosen, :], axis=2), axis=1
            )
            distance[chosen] = math.inf
            chosen.append(int(np.argmin(distance)))
        clusters.add(tuple(sorted(chosen)))
    return sorted(clusters)


# ---------------------------------------------------------------------------
# The sweep
# ---------------------------------------------------------------------------

_WORKER: dict[str, Any] = {}


def _initialise(geometry: Geometry, budget: Budget, seed: int) -> None:
    _WORKER.update(geometry=geometry, budget=budget, seed=seed)


def _solve(
    task: tuple[int, list[tuple[int, Floats]]],
) -> tuple[int, bool, float, Floats, int, str]:
    mask, sub_witnesses = task
    geometry: Geometry = _WORKER["geometry"]
    cells = cells_of(mask)
    rng = pattern_rng(_WORKER["seed"], mask)
    witnesses = {mask_of(cells[:row] + cells[row + 1 :]): w for row, w in sub_witnesses}
    warm = warm_starts(geometry, cells, witnesses, rng)
    verdict = search(geometry, cells, rng, _WORKER["budget"], warm)
    return (
        mask,
        verdict.feasible,
        verdict.violation,
        verdict.pose,
        verdict.attempts,
        verdict.found_by,
    )


def _sub_witness_payload(
    cells: tuple[int, ...], witnesses: dict[int, Floats]
) -> list[tuple[int, Floats]]:
    payload: list[tuple[int, Floats]] = []
    for row in range(len(cells)):
        witness = witnesses.get(mask_of(cells[:row] + cells[row + 1 :]))
        if witness is not None:
            payload.append((row, witness))
    return payload


def sweep(
    geometry: Geometry,
    *,
    max_arity: int,
    seed: int,
    budget: Budget,
    window: float | None = None,
    workers: int = 1,
    witnessed: set[int] | None = None,
    timeout: float | None = None,
    progress: bool = False,
    restrict_from: int | None = None,
    size: int = TARGET,
    progress_every: int | None = None,
    max_missing: int | None = None,
) -> dict[str, Any]:
    """Bottom-up search of every connected class; flags, false flags and timings.

    With `restrict_from`, each arity from it on tests only the classes lying in a state of
    `size` cells that survives the flags of lower arities, fewest missing pairs first. With
    `max_missing` as well, it tests at those arities only the classes with at most that many
    non-interacting pairs, a priority subset that is not exact.
    """
    if max_missing is not None and restrict_from is None:
        raise ValueError("max_missing applies only where the restriction does")
    clock = time.perf_counter()
    witnessed = witnessed or set()
    witnesses: dict[int, Floats] = {}
    flagged: dict[int, dict[str, Any]] = {}
    flagged_masks: list[int] = []
    false_flags: list[dict[str, Any]] = []
    levels: dict[str, Any] = {}
    executor = (
        ProcessPoolExecutor(
            max_workers=workers, initializer=_initialise, initargs=(geometry, budget, seed)
        )
        if workers > 1
        else None
    )
    if executor is None:
        _initialise(geometry, budget, seed)
    complete = True
    states: NDArray[np.int64] | None = None
    restricted_total = 0
    try:
        for arity in range(1, max_arity + 1):
            level_clock = time.perf_counter()
            classes = pattern_classes(geometry, arity, window)
            alive: NDArray[np.int64] | None = None
            if restrict_from is not None and arity >= restrict_from:
                if states is None:
                    states = all_states(len(geometry.names), size)
                alive = survivors(states, flagged_masks)
            pruned, restricted, tested = split_classes(classes, flagged_masks, alive)
            restricted_total += len(restricted)
            deferred: list[int] = []
            if alive is not None:
                # Most crowded first, so a wall ceiling cuts the classes least likely flagged;
                # outcomes are taken in mask order, so a complete level is unaffected.
                missing = {m: missing_pairs(geometry, m) for m in tested}
                if max_missing is not None:
                    deferred = [m for m in tested if missing[m] > max_missing]
                    tested = [m for m in tested if missing[m] <= max_missing]
                tested = sorted(tested, key=lambda m: (missing[m], m))
            tasks = [(mask, _sub_witness_payload(cells_of(mask), witnesses)) for mask in tested]
            results = (
                executor.map(_solve, tasks, chunksize=8)
                if executor is not None
                else map(_solve, tasks)
            )
            outcomes = []
            for outcome in results:
                outcomes.append(outcome)
                if progress_every and len(outcomes) % progress_every == 0:
                    partial = {
                        "arity": arity,
                        "searched_so_far": len(outcomes),
                        "of": len(tasks),
                        "unplaced_so_far": sum(1 for o in outcomes if not o[1]),
                        "seconds": round(time.perf_counter() - level_clock, 3),
                    }
                    print(json.dumps(partial), flush=True)
                if timeout is not None and time.perf_counter() - clock > timeout:
                    complete = False
                    break
            attempts = 0
            found: dict[str, int] = {}
            new_flags = 0
            for mask, feasible, value, pose, count, how in sorted(outcomes, key=lambda o: o[0]):
                attempts += count
                cells = cells_of(mask)
                if feasible:
                    found[how] = found.get(how, 0) + 1
                    for element in range(len(geometry.group)):
                        image_cells, image_pose = transform_pose(geometry, cells, pose, element)
                        witnesses[mask_of(image_cells)] = image_pose
                    continue
                record = {
                    "arity": arity,
                    "cells": [geometry.names[cell] for cell in cells],
                    "indices": list(cells),
                    "best_penetration": value,
                    "attempts": count,
                }
                if mask in witnessed:
                    false_flags.append(record)
                    continue
                new_flags += 1
                flagged[mask] = record
                flagged_masks.extend(sorted(orbit(mask, geometry.group)))
            levels[str(arity)] = {
                "classes": len(classes),
                "pruned_as_supersets": len(pruned),
                "searched": len(outcomes),
                "feasible": sum(found.values()),
                "feasible_by": dict(sorted(found.items())),
                "flagged": new_flags,
                "attempts": attempts,
                "seconds": round(time.perf_counter() - level_clock, 3),
            }
            if alive is not None:
                levels[str(arity)]["restricted_out"] = len(restricted)
                levels[str(arity)]["surviving_states_used"] = int(alive.size)
            if alive is not None and max_missing is not None:
                levels[str(arity)]["deferred_by_missing_pairs"] = len(deferred)
            if progress:
                print(json.dumps({"arity": arity, **levels[str(arity)]}), flush=True)
            if not complete:
                break
    finally:
        if executor is not None:
            executor.shutdown(cancel_futures=True)
    record: dict[str, Any] = {
        "levels": levels,
        "flagged": [flagged[mask] for mask in sorted(flagged)],
        "flagged_masks": sorted(flagged),
        "false_flags": false_flags,
        "complete": complete,
        "seconds": round(time.perf_counter() - clock, 3),
    }
    if restrict_from is not None:
        record["restricted_out"] = restricted_total
    return record


# ---------------------------------------------------------------------------
# Consumer: the exact count of surviving states and orbits
# ---------------------------------------------------------------------------


def all_states(cells: int, size: int) -> NDArray[np.int64]:
    return np.array(
        [mask_of(combination) for combination in itertools.combinations(range(cells), size)],
        dtype=np.int64,
    )


def apply_permutation(
    states: NDArray[np.int64], permutation: tuple[int, ...]
) -> NDArray[np.int64]:
    image = np.zeros_like(states)
    for cell, target in enumerate(permutation):
        image |= ((states >> cell) & 1) << target
    return image


def survivors(states: NDArray[np.int64], forbidden: list[int]) -> NDArray[np.int64]:
    alive = states
    for pattern in sorted(set(forbidden)):
        alive = alive[(alive & pattern) != pattern]
    return alive


def count_orbits(
    alive: NDArray[np.int64], group: tuple[tuple[int, ...], ...]
) -> dict[str, Any]:
    """Burnside's count and the distinct canonical forms, which must agree."""
    images = [apply_permutation(alive, permutation) for permutation in group]
    fixed = [int(np.count_nonzero(image == alive)) for image in images]
    if sum(fixed) % len(group):
        raise ValueError("Burnside sum is not divisible by the group order")
    burnside = sum(fixed) // len(group)
    distinct = int(np.unique(np.min(np.stack(images), axis=0)).size) if alive.size else 0
    if burnside != distinct:
        raise ValueError(f"orbit counts disagree: Burnside {burnside}, canonical {distinct}")
    return {"orbits": burnside, "fixed_counts": fixed}


def consume(
    cells: int,
    group: tuple[tuple[int, ...], ...],
    flagged: list[int],
    *,
    size: int = TARGET,
    endpoint_state: int | None = None,
    states: NDArray[np.int64] | None = None,
) -> dict[str, Any]:
    """States with no flagged pattern in any group image, and their orbits."""
    states = all_states(cells, size) if states is None else states
    forbidden = sorted({image for mask in flagged for image in orbit(mask, group)})
    alive = survivors(states, forbidden)
    record: dict[str, Any] = {
        "states": int(states.size),
        "forbidden_images": len(forbidden),
        "surviving_states": int(alive.size),
        **count_orbits(alive, group),
    }
    if endpoint_state is not None:
        record["endpoint_survives"] = bool(np.any(alive == endpoint_state))
    return record


def greedy_order(
    cells: int,
    group: tuple[tuple[int, ...], ...],
    flagged: list[int],
    *,
    size: int = TARGET,
    states: NDArray[np.int64] | None = None,
) -> list[dict[str, Any]]:
    """Flagged classes in the order that removes the most surviving states first.

    Each class's excluded states are computed once as a packed bit row; a greedy step is
    then a popcount of every row against the states still alive.
    """
    states = all_states(cells, size) if states is None else states
    masks = sorted(set(flagged))
    if not masks:
        return []
    rows = np.empty((len(masks), (states.size + 7) // 8), dtype=np.uint8)
    for row, mask in enumerate(masks):
        hit = np.zeros(states.size, dtype=np.bool_)
        for image in sorted(orbit(mask, group)):
            hit |= (states & image) == image
        rows[row] = np.packbits(hit)
    alive = np.packbits(np.ones(states.size, dtype=np.bool_))
    left = int(states.size)
    remaining = list(range(len(masks)))
    order: list[dict[str, Any]] = []
    while remaining:
        counts = np.bitwise_count(rows[remaining] & alive).sum(axis=1, dtype=np.int64)
        pick = int(np.argmax(counts))
        removes = int(counts[pick])
        if removes == 0:
            order.extend(
                {"mask": masks[row], "removes": 0, "states_left": left} for row in remaining
            )
            break
        row = remaining.pop(pick)
        alive &= ~rows[row]
        left -= removes
        order.append({"mask": masks[row], "removes": removes, "states_left": left})
    return order


def receipt_flags(path: Path, geometry: Geometry, design_name: str) -> list[int]:
    """The canonical masks an earlier receipt flagged, checked against the cover's cells."""
    receipt = json.loads(path.read_text(encoding="utf-8"))
    if receipt.get("design") != design_name or receipt.get("cells") != list(geometry.names):
        raise ValueError(f"{path} was not run on design {design_name} with these cells")
    return sorted(
        {canonical(mask_of(entry["indices"]), geometry.group) for entry in receipt["flagged"]}
    )


def count_classes(
    geometry: Geometry,
    *,
    max_arity: int,
    flagged: list[int],
    window: float | None = None,
    size: int = TARGET,
) -> dict[str, Any]:
    """Per arity, without searching: what the restriction would test under given flags.

    At each arity, the flags of lower arity prune their supersets and leave the surviving
    states; `in_survivors` counts the classes a restricted sweep with those flags would
    test, and `restricted_out` the further classes it would skip. Both those classes and
    the given flags of this arity are tallied by missing pairs, which is what a
    `max_missing_pairs` subset would keep.
    """
    states = all_states(len(geometry.names), size)
    levels: dict[str, Any] = {}
    for arity in range(1, max_arity + 1):
        lower = [mask for mask in flagged if mask.bit_count() < arity]
        images = sorted({image for mask in lower for image in orbit(mask, geometry.group)})
        classes = pattern_classes(geometry, arity, window)
        alive = survivors(states, images)
        pruned, restricted, tested = split_classes(classes, images, alive)
        here = [mask for mask in flagged if mask.bit_count() == arity]
        levels[str(arity)] = {
            "classes": len(classes),
            "flags_below": len(lower),
            "surviving_states_used": int(alive.size),
            "pruned_as_supersets": len(pruned),
            "restricted_out": len(restricted),
            "in_survivors": len(tested),
            "in_survivors_by_missing_pairs": _histogram(geometry, tested),
            "flags_by_missing_pairs": _histogram(geometry, here),
        }
    return levels


def _histogram(geometry: Geometry, masks: list[int]) -> list[int]:
    """Counts of the masks by missing pairs, indexed by the number missing."""
    counts = [missing_pairs(geometry, mask) for mask in masks]
    return [counts.count(missing) for missing in range(max(counts, default=-1) + 1)]


# ---------------------------------------------------------------------------
# Receipt
# ---------------------------------------------------------------------------


def run(
    *,
    design_name: str = DEFAULT_DESIGN,
    max_arity: int = 5,
    seed: int = 1,
    budget: Budget | None = None,
    window: float | None = None,
    workers: int = 1,
    timeout: float | None = None,
    tight_sizes: tuple[int, ...] = (3, 4, 5),
    progress: bool = False,
    restrict_from: int | None = None,
    progress_every: int | None = None,
    max_missing: int | None = None,
) -> dict[str, Any]:
    clock = time.perf_counter()
    budget = budget or Budget()
    geometry = cover_geometry(design_name)
    endpoint = endpoint_pose(design_name)
    endpoint_state = mask_of(endpoint["cells"])
    witnessed, endpoint_record = endpoint_witnesses(geometry, endpoint, max_arity)
    tight = [
        tight_control(geometry, endpoint, rows, seed=seed, budget=budget)
        for size in tight_sizes
        for rows in contact_clusters(endpoint, size)
    ]
    swept = sweep(
        geometry,
        max_arity=max_arity,
        seed=seed,
        budget=budget,
        window=window,
        workers=workers,
        witnessed=witnessed,
        timeout=timeout,
        progress=progress,
        restrict_from=restrict_from,
        progress_every=progress_every,
        max_missing=max_missing,
    )
    states = all_states(len(geometry.names), TARGET)
    by_arity: dict[str, Any] = {}
    for arity in range(1, max_arity + 1):
        masks = [m for m in swept["flagged_masks"] if m.bit_count() <= arity]
        by_arity[str(arity)] = {
            "flagged_classes": len(masks),
            **consume(
                len(geometry.names),
                geometry.group,
                masks,
                endpoint_state=endpoint_state,
                states=states,
            ),
        }
    order = greedy_order(
        len(geometry.names), geometry.group, swept["flagged_masks"], states=states
    )
    by_mask = dict(zip(swept["flagged_masks"], swept["flagged"], strict=True))
    priority = [
        {
            **step,
            "cells": by_mask[step["mask"]]["cells"],
            "best_penetration": by_mask[step["mask"]]["best_penetration"],
        }
        for step in order
    ]
    controls = {
        "endpoint_pose": endpoint_record,
        "tight_endpoint_clusters": {
            "count": len(tight),
            "worst_best_violation": max(
                (entry["best_violation"] for entry in tight), default=0.0
            ),
            "failures": [entry for entry in tight if not entry["passed"]],
        },
        "search_false_flags_on_endpoint_sub_patterns": swept["false_flags"],
    }
    controls["passed"] = (
        endpoint_record["passed"]
        and not controls["tight_endpoint_clusters"]["failures"]
        and not swept["false_flags"]
        and by_arity[str(max_arity)]["endpoint_survives"]
    )
    receipt: dict[str, Any] = {
        "schema": SCHEMA,
        "status": STATUS,
        "design": design_name,
        "design_commit": DESIGN_COMMIT.get(design_name),
        "cap": str(cover.U),
        "cells": list(geometry.names),
        "interaction_edges": int(np.count_nonzero(np.triu(geometry.interact, 1))),
        "parameters": {
            "max_arity": max_arity,
            "seed": seed,
            "starts": budget.starts,
            "hops": budget.hops,
            "hop_centre": budget.hop_centre,
            "hop_angle": budget.hop_angle,
            "deep_starts": budget.deep_starts,
            "deep_hops": budget.deep_hops,
            "wide_centre": budget.wide_centre,
            "wide_angle": budget.wide_angle,
            "margin": budget.margin,
            "polish_below": POLISH_BELOW,
            "window": window,
            "workers": workers,
            "timeout": timeout,
        },
        "controls": controls,
        "sweep": {
            key: swept[key]
            for key in ("levels", "complete", "seconds", "restricted_out")
            if key in swept
        },
        "flagged": swept["flagged"],
        "survivors_by_arity": by_arity,
        "certification_priority": priority,
        "provenance": PROVENANCE,
    }
    if restrict_from is not None:
        receipt["parameters"]["restrict_to_survivors_from"] = restrict_from
    if max_missing is not None:
        receipt["parameters"]["max_missing_pairs"] = max_missing
    if budget.finish:
        receipt["parameters"]["finish"] = FINISH
    receipt["seconds"] = round(time.perf_counter() - clock, 3)
    return receipt


# ---------------------------------------------------------------------------
# Re-checking earlier flags
# ---------------------------------------------------------------------------


def recheck_flag(
    geometry: Geometry,
    mask: int,
    *,
    seed: int,
    budget: Budget,
    witness_cache: dict[tuple[int, Budget], Verdict] | None = None,
    checkpoint_at: int | None = None,
    resume: Checkpoint | None = None,
) -> dict[str, Any]:
    """One flagged class searched again: sub-pattern witnesses first, then the class.

    With `checkpoint_at`, the record also holds the class search's `Checkpoint` after that
    many deep starts (None if it is placed). With `resume`, a checkpoint written here under
    a budget with the same prefix and seed, the class's search continues from it, and no
    sub-pattern is searched: the prefix decides the sub-pattern searches, so the warm starts
    the checkpoint holds are the ones they would give, and the record is the one this budget
    gives from scratch, but for `sub_pattern_attempts`, which is 0.
    """
    cells = cells_of(mask)
    if resume is not None:
        verdict, checkpoint = search_resumable(
            geometry,
            cells,
            pattern_rng(seed, mask),
            budget,
            checkpoint_at=checkpoint_at,
            resume=resume,
        )
        record = recheck_record(geometry, verdict, len(resume.templates), 0)
        if checkpoint_at is not None:
            record["checkpoint"] = checkpoint
        return record
    sub_budget = replace(budget, deep_starts=0, deep_hops=0)
    witnesses: dict[int, Floats] = {}
    sub_attempts = 0
    for row in range(len(cells)):
        sub = cells[:row] + cells[row + 1 :]
        if not connected(geometry, sub):
            continue
        key = (mask_of(sub), sub_budget)
        cached = None if witness_cache is None else witness_cache.get(key)
        if cached is None:
            found = search(geometry, sub, pattern_rng(seed, mask_of(sub)), sub_budget)
            if witness_cache is not None:
                witness_cache[key] = found
            sub_attempts += found.attempts
        else:
            found = cached
        if found.feasible:
            witnesses[mask_of(sub)] = found.pose
    rng = pattern_rng(seed, mask)
    warm = warm_starts(geometry, cells, witnesses, rng)
    verdict, checkpoint = search_resumable(
        geometry, cells, rng, budget, warm, checkpoint_at=checkpoint_at
    )
    record = recheck_record(geometry, verdict, len(witnesses), sub_attempts)
    if checkpoint_at is not None:
        record["checkpoint"] = checkpoint
    return record


def recheck_record(
    geometry: Geometry, verdict: Verdict, witnesses: int, sub_attempts: int
) -> dict[str, Any]:
    """The re-check receipt's entry for one class."""
    cells = verdict.cells
    return {
        "arity": len(cells),
        "cells": [geometry.names[cell] for cell in cells],
        "indices": list(cells),
        "status": "placed" if verdict.feasible else "still-flagged",
        "best_penetration": verdict.violation,
        "components": verdict.components,
        "attempts": verdict.attempts,
        "found_by": verdict.found_by,
        "sub_pattern_witnesses": witnesses,
        "sub_pattern_attempts": sub_attempts,
        "pose": [[float(v) for v in row] for row in verdict.pose],
    }


def recheck(
    receipts: list[Path],
    *,
    design_name: str = DEFAULT_DESIGN,
    seed: int = 1,
    budget: Budget | None = None,
    progress: bool = False,
) -> dict[str, Any]:
    """Every class the receipts flagged, searched again; survivors over those still flagged."""
    clock = time.perf_counter()
    budget = budget or Budget()
    geometry = cover_geometry(design_name)
    earlier: dict[int, dict[str, Any]] = {}
    sources: list[dict[str, str]] = []
    for path in receipts:
        for mask in receipt_flags(path, geometry, design_name):
            earlier.setdefault(mask, {})
        document = json.loads(path.read_text(encoding="utf-8"))
        for flag in document["flagged"]:
            mask = canonical(mask_of(flag["indices"]), geometry.group)
            earlier[mask] = {
                "arity": flag["arity"],
                "best_penetration": flag["best_penetration"],
            }
        sources.append(
            {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        )
    rows: list[dict[str, Any]] = []
    for mask in sorted(earlier, key=lambda m: (m.bit_count(), m)):
        row = recheck_flag(geometry, mask, seed=seed, budget=budget)
        row["earlier_best_penetration"] = earlier[mask]["best_penetration"]
        row["seconds"] = round(time.perf_counter() - clock, 3)
        rows.append(row)
        if progress:
            print(
                json.dumps(
                    {k: row[k] for k in ("arity", "status", "best_penetration", "seconds")}
                ),
                flush=True,
            )
    endpoint_state = mask_of(endpoint_pose(design_name)["cells"])
    states = all_states(len(geometry.names), TARGET)
    surviving = [
        canonical(mask_of(row["indices"]), geometry.group)
        for row in rows
        if row["status"] == "still-flagged"
    ]
    projections: dict[str, Any] = {}
    for top in sorted({row["arity"] for row in rows}):
        for label, masks in (
            ("earlier", [m for m in earlier if m.bit_count() <= top]),
            ("still_flagged", [m for m in surviving if m.bit_count() <= top]),
        ):
            record = consume(
                len(geometry.names),
                geometry.group,
                masks,
                endpoint_state=endpoint_state,
                states=states,
            )
            projections.setdefault(f"arity<={top}", {})[label] = {
                "flagged_classes": len(masks),
                **{k: record[k] for k in ("surviving_states", "orbits", "endpoint_survives")},
            }
    return {
        "schema": RECHECK_SCHEMA,
        "status": STATUS,
        "design": design_name,
        "cells": list(geometry.names),
        "sources": sources,
        "parameters": {
            "seed": seed,
            "starts": budget.starts,
            "hops": budget.hops,
            "deep_starts": budget.deep_starts,
            "deep_hops": budget.deep_hops,
            "margin": budget.margin,
            "finish": FINISH if budget.finish else None,
            "sub_patterns": "every connected k - 1 subset, searched without the deep stage",
        },
        "rechecked": rows,
        "placed": sum(1 for row in rows if row["status"] == "placed"),
        "still_flagged": len(surviving),
        "flagged": [
            {k: row[k] for k in ("arity", "cells", "indices", "best_penetration", "attempts")}
            for row in rows
            if row["status"] == "still-flagged"
        ],
        "projections": projections,
        "provenance": PROVENANCE,
        "seconds": round(time.perf_counter() - clock, 3),
    }


def without_timings(receipt: dict[str, Any]) -> dict[str, Any]:
    """The receipt with wall times removed, for determinism comparisons."""
    text = json.dumps(receipt, sort_keys=True, default=str)
    document = json.loads(text)
    document.pop("seconds", None)
    document["sweep"].pop("seconds", None)
    for level in document["sweep"]["levels"].values():
        level.pop("seconds", None)
    document["parameters"].pop("workers", None)
    return document


def count_main(arguments: argparse.Namespace) -> int:
    """The `--count-only` path: class counts under a receipt's flags, with no search."""
    clock = time.perf_counter()
    geometry = cover_geometry(arguments.design)
    source: Path | None = arguments.flags_from
    flagged = [] if source is None else receipt_flags(source, geometry, arguments.design)
    record = {
        "schema": COUNT_SCHEMA,
        "status": "class counts only; nothing is searched and nothing is certified",
        "design": arguments.design,
        "max_arity": arguments.max_arity,
        "window": arguments.window,
        "state_size": TARGET,
        "flags_from": None if source is None else str(source),
        "flags_from_sha256": None
        if source is None
        else hashlib.sha256(source.read_bytes()).hexdigest(),
        "flagged_classes": len(flagged),
        "levels": count_classes(
            geometry, max_arity=arguments.max_arity, flagged=flagged, window=arguments.window
        ),
        "provenance": PROVENANCE,
        "seconds": round(time.perf_counter() - clock, 3),
    }
    text = json.dumps(record, indent=1, sort_keys=True)
    if arguments.output is not None:
        _ = arguments.output.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("--design", choices=sorted(cover.DESIGNS), default=DEFAULT_DESIGN)
    _ = parser.add_argument("--max-arity", type=int, default=5)
    _ = parser.add_argument("--seed", type=int, default=1)
    _ = parser.add_argument("--starts", type=int, default=Budget.starts)
    _ = parser.add_argument("--hops", type=int, default=Budget.hops)
    _ = parser.add_argument("--deep-starts", type=int, default=Budget.deep_starts)
    _ = parser.add_argument("--deep-hops", type=int, default=Budget.deep_hops)
    _ = parser.add_argument("--margin", type=float, default=MARGIN)
    _ = parser.add_argument("--window", type=float, default=None)
    _ = parser.add_argument("--workers", type=int, default=1)
    _ = parser.add_argument("--timeout", type=float, default=None, help="wall ceiling, s")
    _ = parser.add_argument("--output", type=Path, help="write the receipt here")
    _ = parser.add_argument(
        "--restrict-to-survivors",
        type=int,
        default=None,
        metavar="ARITY",
        help="from this arity on, test only classes lying in a state that survives the "
        "flags of lower arities",
    )
    _ = parser.add_argument(
        "--max-missing-pairs",
        type=int,
        default=None,
        metavar="D",
        help="where the restriction applies, test only classes with at most D "
        "non-interacting pairs (a priority subset, not exact)",
    )
    _ = parser.add_argument(
        "--progress-every", type=int, default=None, help="print a line every N searches"
    )
    _ = parser.add_argument(
        "--count-only",
        action="store_true",
        help="search nothing: count classes per arity and those lying in survivors",
    )
    _ = parser.add_argument(
        "--flags-from", type=Path, default=None, help="with --count-only: a receipt's flags"
    )
    _ = parser.add_argument(
        "--no-finish",
        dest="finish",
        action="store_false",
        help="no long descent from an unplaced pattern's best pose (the search before H-267's "
        "residue survey)",
    )
    _ = parser.add_argument(
        "--recheck",
        type=Path,
        nargs="+",
        default=None,
        metavar="RECEIPT",
        help="search every class these receipts flagged again, and nothing else",
    )
    arguments = parser.parse_args(argv)
    if arguments.count_only:
        return count_main(arguments)
    budget = Budget(
        starts=arguments.starts,
        hops=arguments.hops,
        deep_starts=arguments.deep_starts,
        deep_hops=arguments.deep_hops,
        margin=arguments.margin,
        finish=arguments.finish,
    )
    if arguments.recheck is not None:
        rechecked = recheck(
            arguments.recheck,
            design_name=arguments.design,
            seed=arguments.seed,
            budget=budget,
            progress=True,
        )
        text = json.dumps(rechecked, indent=1, sort_keys=True, default=float)
        if arguments.output is not None:
            _ = arguments.output.write_text(text + "\n", encoding="utf-8")
        summary = {
            k: rechecked[k] for k in ("placed", "still_flagged", "projections", "seconds")
        }
        print(json.dumps(summary, indent=1, sort_keys=True))
        return 0
    receipt = run(
        design_name=arguments.design,
        max_arity=arguments.max_arity,
        seed=arguments.seed,
        budget=budget,
        window=arguments.window,
        workers=arguments.workers,
        timeout=arguments.timeout,
        progress=True,
        restrict_from=arguments.restrict_to_survivors,
        progress_every=arguments.progress_every,
        max_missing=arguments.max_missing_pairs,
    )
    text = json.dumps(receipt, indent=1, sort_keys=True, default=float)
    if arguments.output is not None:
        _ = arguments.output.write_text(text + "\n", encoding="utf-8")
    summary = {
        "status": receipt["status"],
        "controls_passed": receipt["controls"]["passed"],
        "complete": receipt["sweep"]["complete"],
        "levels": receipt["sweep"]["levels"],
        "survivors_by_arity": {
            arity: {
                key: entry[key]
                for key in (
                    "flagged_classes",
                    "surviving_states",
                    "orbits",
                    "endpoint_survives",
                )
            }
            for arity, entry in receipt["survivors_by_arity"].items()
        },
        "seconds": receipt["seconds"],
    }
    print(json.dumps(summary, indent=1, sort_keys=True))
    return 0 if receipt["controls"]["passed"] and receipt["sweep"]["complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
