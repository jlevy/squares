#!/usr/bin/env python3
"""Close a witness's free grid slack and straighten its near-axis squares, exactly.

Usage, from `packing/`, after
`uv run --frozen --all-extras --group dev python -m devtools.regularize_grid_slack`:

    --n 302 303 --run-dir DIR [--near-axis-degrees 0.5] [--trust 0.45] [--time-limit 120]

A prototype generator for the regularized drawing layer
(`docs/project/policies/regularization-policy.md`). The atlas shades a square by how many
of its four sides it shares whole with a wall or a same-angle neighbour, so a grid region
reads as one dark hue only when its squares sit flush and aligned. Where they do not,
the census `devtools.census_drawing_regularity` names the faces: slack, a misaligned or
staggered neighbour, a near miss of a few millionths, or a neighbour a hair off the
axes. This tool asks which of those the packing can close at the record's own side, and
closes them, in five steps:

1. **The exact frame.** `regularize_same_side.exact_frame`: a rational witness's own
   geometry, or a decimal witness's 36-digit rational promotion at centre dilation 1;
   its side is `s_W`. Where no view exists at `s_W` and the record's verified upper bound
   `U` is rational and above it, the same squares are tried again in a box of side `U`,
   the policy's `bound` frame (a decimal witness whose printed side truncates its
   optimum, n = 171 and 198). Where `U` is rational and below `s_W`, the box of side `U`
   is tried first: a view at `s_W` would draw the packing above the best known side
   (owner, 13 October 2026). Every rotation stays the witness's own exact one, except:
2. **Straightening.** Each square tilted by less than `--near-axis-degrees` (default half a
   degree, the workbench's colour tolerance; any nonzero tilt, including those under the
   house's `1e-6` radians) is turned to the axes about its centre, when the placement
   below is still feasible with it turned. All of them are tried together first; when
   that is infeasible, one at a time from the smallest tilt, each kept only if the
   placement stays feasible. Feasibility is the LP's with the separating normals chosen
   at the start, so a refusal says no placement was found, not that none exists.
3. **Placement (MILP).** With every rotation fixed, a unit square's separation from a
   neighbour along a chosen face normal is linear in the two centres, and every point
   meeting those inequalities is a packing (upstream's `reg.place`, evand/square-packing,
   uses the same fact). Each centre may move by at most `--trust` per coordinate from the
   witness's and by at most `MOVE_BOUND` in L1, so by at most `1/2`: the generator's
   trust region, which keeps the placement near the witness's pose and its big-M
   constants tight. The bound holds in binary64, on the placement: the exact re-solve may
   move a centre up to `BLOWUP` (`1e-6`) further, so a view's largest move is at most
   `1/2 + 1e-6`. The policy measures a move and gates nothing on it (section 3, since 13
   October 2026). A binary per *coincidence* -- two squares of
   exactly one rotation class flush across a face with no offset along it, or an axis
   square flush on a wall: exactly a full shared side under the house rule -- is
   switched on by big-M constraints, and the objective maximizes full shared sides
   (two per pair, one per wall, the house total), with the L1 move from the witness as a
   tie-break worth less than one side. Every contact the witness already has under the
   house rule or the stage rule (`census_atlas_contact_shades`'s replicas) is kept as a
   constraint: the house residual of a pair or wall may not grow, and a stage contact
   stays within `STAGE_MARGIN` of its rule's `0.01` (or within its own residual, if that
   is larger). This is upstream's coincidence MILP (`reg.coincidences`) with three
   changes: it starts from the witness's own pose (no KKT solve), its tie-break is
   staying close to the witness rather than gravity, and it may not trade an existing
   contact away. Tilted squares translate with the rest; when that attempt yields no
   view, they are held at their exact poses and the step runs again.
4. **Re-placement (LP).** The chosen coincidences become equalities and the walls fixed
   coordinates; an LP minimizes the L1 move from the witness. HiGHS meets an equality to
   about `1e-10`, so every closed contact is tight at the `1e-9` the next step detects.
   A chosen set the MIP tolerance let through but no exact placement meets is thinned by
   an elastic LP (`replace_flush`).
5. **The exact re-solve.** `regularize_same_side`'s parts in its order -- rotations matched
   exactly (axis-aligned, or the witness's own rational rotation), the contacts tight at
   the float pose as rows over `Q`, elimination in relax mode -- then both maintained
   exact routes, `sqpack.witness.exact_verify` and the independent checker. Only a pose
   both routes accept is a view. Two ways of choosing the rows are tried, as
   `exact_view` describes: the witness's own contacts among unchanged squares (n = 105
   has near contacts `1e-12` apart along nearly parallel faces, which closing would pin
   through a near-singular pair of rows), or every tight row, as the resolver does (a
   decimal promotion's near contacts of up to `1e-8`).

**What decides.** The exact routes decide validity; the float MILP and LP only propose a
pose. Identity is measured by `regularize_evand.identity` (`arrangement_gap` under the
box's eight symmetries, with the straightened squares as the named angle changes), and
the house and stage histograms by `regularize_evand.contact_shades`, against the witness
and against the project's current view of the count; a total that falls is reported as
the decision table's refusal (row 7). The drawing is measured by the house renderer
through `census_drawing_regularity.regularity`.

**Admission.** A run writes only into `--run-dir`, never into `witnesses/` or `atlas/`.
This module also decides a finished run's views by the policy's decision table
(`decided`) and gives the ones row 10 admits to the layer in its terms (`admitted`,
`admitted_views`); only `python -m devtools.regularize_evand layer --grid-run DIR
--grid-counts N ...` writes them into it.

**Limits.** A prototype, run on request. The MILP stops at `--time-limit` with its
best incumbent, so "the slack the packing forces" is what the incumbent leaves within the
trust region, not a proof that no placement closes more. Pairs whose rotations differ by
less than the house's tolerance but are not one exact class cannot coincide here; a
square straightened from a near-axis class loses the contacts it had with its own class
until the placement closes them again, and the regression report says so.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import time
import warnings
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field, replace
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import linprog, milp
from scipy.sparse import csr_array
from strif import atomic_output_file

from devtools import census_atlas_contact_shades as shades
from devtools import census_drawing_regularity as regularity
from devtools import regularize_axis_components as layer
from devtools import regularize_evand as driver
from devtools import regularize_same_side as same
from devtools.build_known_best_atlas import frame_from_witness
from devtools.regularized_drawings import grid_written_method
from devtools.retained_data import git_blob
from sqpack.render import render_packing_svg
from sqpack.render.model import RenderSpec
from sqpack.witness import validate_witness_document, witness_document
from sqpack.yamlio import load_yaml

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
KNOWN_BEST = ROOT / "witnesses/known-best"
WITNESS_SCHEMA = ROOT / "witnesses/witness.schema.yaml"
FORBIDDEN_OUTPUT_ROOTS = (ROOT / "witnesses", ROOT / "atlas")
GENERATOR = "regularize_grid_slack/1"
"""A prototype's version: changed by hand with any change that changes a view."""

METHOD = (
    "regularize_grid_slack/1: Evan Daniel's coincidence placement (evand/square-packing "
    "search/regularize reg.coincidences and reg.place, MIT), ported to start from the "
    "witness's exact frame and to keep its contacts, then the same-side exact re-solve"
)
"""The credit a view carries: the policy's section 7 credits a port of his method."""
NEAR_AXIS_DEGREES = 0.5
TRUST = 0.45
"""Per coordinate; with `MOVE_BOUND` a centre moves less than `1/2` from the witness in
the placement. Positive: `--trust 0` is refused."""
MOVE_BOUND = 0.5
"""A centre's L1 move from the witness in the binary64 placement: the trust region that
keeps its distance under `1/2` there and the placement's big-M constants tight; the exact
re-solve may add up to `BLOWUP`. The policy measures the move and no longer gates on it
(section 3)."""
TIME_LIMIT = 120.0
STAGE_MARGIN = 0.0099
"""A kept stage contact stays this close; the stage's frame rounds centres to `1e-6`."""
DEFAULT_SETTINGS = {
    "near_axis_degrees": NEAR_AXIS_DEGREES,
    "trust": TRUST,
    "time_limit": TIME_LIMIT,
    "stage_margin": STAGE_MARGIN,
}
"""What a run reports in `settings` when no option changes it; the layer's generator block."""
EPSILON = 1e-9
"""A kept house residual may always grow to this, three orders under the house's `2e-6`.
A floor at the LP's own noise (`1e-12`) leaves rows a few `1e-12` wide, which HiGHS
cannot meet (n = 211: a square at 0.0012 degrees could not be straightened), and a
residual this small is closed exactly by the re-solve's `1e-9` tight set anyway."""
UNMOVED = 1e-9
"""A square the LP moved by less than this keeps its exact centre in the re-solve."""
BLOWUP = 1e-6
"""A re-solved centre this far from the placement means nearly parallel tight rows."""
MAX_REOPEN_ROUNDS = 32
WATCH = 1e-6
"""Contacts this close to the placement are watched by the exact solve: see `BLOWUP`."""
FLOAT_OVERLAP = 1e-12
"""An overlap binary64 sees this clearly is refused before the exact routes run."""
EXACT_GAP = 1e-13
"""A tight row between two unchanged squares is closed only if the witness's own gap is
this small: what is left is the witness's exact contacts and its rotation classes' merge."""
LP_TOLERANCE = 1e-10
HIGHS_RETRIES: tuple[tuple[float | None, bool], ...] = (
    (None, True),
    (1e-9, True),
    (1e-7, True),
    (None, False),
    (1e-9, False),
)
"""HiGHS feasibility tolerance (its default where `None`) and presolve, in the order tried."""
ELASTIC_PRICE = 1e6
"""The price of a unit of slack on a coincidence in the elastic re-placement."""
DROP_SLACK = 1e-9
HOUSE = shades.RULES[0]
STAGE = shades.RULES[1]

type Vector = tuple[float, float]
type Key = tuple[Fraction, Fraction]


class GridSlackError(ValueError):
    """A count this tool cannot regularize, with the stage that refused it."""


@dataclass(frozen=True)
class Settings:
    near_axis_degrees: float = NEAR_AXIS_DEGREES
    trust: float = TRUST
    time_limit: float = TIME_LIMIT

    def __post_init__(self) -> None:
        # The tie-break's weight divides by the trust region (`place`), and a region of
        # no width moves nothing (review B of #530, B5).
        if not self.trust > 0:
            raise GridSlackError(f"the trust region must be positive, not {self.trust}")


def positive(text: str) -> float:
    """A command-line value that must be a positive number."""
    value = float(text)
    if not value > 0:
        raise argparse.ArgumentTypeError(f"{text} is not positive")
    return value


@dataclass
class Geometry:
    """The float picture the MILP works on: start centres and fixed rotations."""

    side: float
    x0: np.ndarray
    y0: np.ndarray
    rotation: list[Vector]
    key: list[Key]
    """Each rotation's class modulo a quarter turn, exactly: the canonical turn."""
    axis: list[bool]
    snapped: list[int] = field(default_factory=list)
    frozen: list[bool] = field(default_factory=list)
    """Squares held at their exact start: the tilted ones, when an attempt freezes them."""


def canonical(rotation: same.Rotation) -> Key:
    """The quarter turn of `rotation` with `c > 0, s >= 0`: one key per class."""
    for quarter in range(4):
        c, s = same.turn(rotation, quarter)
        if c > 0 and s >= 0:
            return c, s
    raise GridSlackError("a rotation with no canonical quarter turn")


def tilt_degrees(rotation: same.Rotation) -> float:
    """Distance from the axes modulo a quarter turn, in degrees."""
    return same.class_distance(same.degrees_of(rotation), 0.0)


def view_poses(frame: same.Frame, snapped: Sequence[int]) -> list[same.GeneratorPose]:
    """The witness's own pose, with the `snapped` squares turned to the axes."""
    turned = set(snapped)
    poses: list[same.GeneratorPose] = []
    for index, ((x, y), rotation) in enumerate(
        zip(frame.centers, frame.rotations, strict=True)
    ):
        degrees = "0" if index in turned else repr(same.degrees_of(rotation))
        poses.append(
            same.GeneratorPose(same.plain_decimal(x, 50), same.plain_decimal(y, 50), degrees)
        )
    return poses


def geometry(frame: same.Frame, snapped: Sequence[int], *, freeze: bool = False) -> Geometry:
    """The start of the placement, rotations matched exactly as the re-solve will."""
    matched = same.match_rotations(frame, view_poses(frame, snapped))
    return Geometry(
        side=float(frame.side),
        x0=np.array([float(x) for x, _ in frame.centers]),
        y0=np.array([float(y) for _, y in frame.centers]),
        rotation=[(float(m.rotation[0]), float(m.rotation[1])) for m in matched],
        key=[canonical(m.rotation) for m in matched],
        axis=[m.source is None for m in matched],
        snapped=list(snapped),
        frozen=[freeze and m.source is not None for m in matched],
    )


# --------------------------------------------------------------------------- constraints


@dataclass
class Rows:
    """Linear rows `lo <= a . v <= hi` over the placement's variables."""

    entries: list[dict[int, float]] = field(default_factory=list)
    lo: list[float] = field(default_factory=list)
    hi: list[float] = field(default_factory=list)
    labels: list[str] = field(default_factory=list)

    def add(self, coefficients: dict[int, float], lo: float, hi: float, label: str) -> None:
        self.entries.append(coefficients)
        self.lo.append(lo)
        self.hi.append(hi)
        self.labels.append(label)

    def matrix(self, columns: int) -> csr_array:
        data: list[float] = []
        rows: list[int] = []
        cols: list[int] = []
        for row, coefficients in enumerate(self.entries):
            for column, value in coefficients.items():
                rows.append(row)
                cols.append(column)
                data.append(value)
        return csr_array((data, (rows, cols)), shape=(len(self.entries), columns))


def _pair_form(i: int, j: int, vector: Vector) -> dict[int, float]:
    """`vector . (c_j - c_i)` as a row."""
    vx, vy = vector
    return {2 * i: -vx, 2 * i + 1: -vy, 2 * j: vx, 2 * j + 1: vy}


def _support(rotation: Vector, normal: Vector) -> float:
    return same.support_f(rotation, normal)


def best_normal(g: Geometry, i: int, j: int) -> tuple[Vector, float, float]:
    """Upstream's `best_normal` at the start: the face normal of either square with the
    largest gap, oriented from `i` to `j`; returns it, the supports' sum and the gap."""
    dx, dy = g.x0[j] - g.x0[i], g.y0[j] - g.y0[i]
    best: tuple[Vector, float, float] | None = None
    for own in (i, j):
        c, s = g.rotation[own]
        for fx, fy in ((c, s), (-s, c)):
            sign = -1.0 if fx * dx + fy * dy < 0 else 1.0
            normal = (sign * fx, sign * fy)
            reach = _support(g.rotation[i], normal) + _support(g.rotation[j], normal)
            gap = normal[0] * dx + normal[1] * dy - reach
            if best is None or gap > best[2]:
                best = (normal, reach, gap)
    if best is None:  # Defensive: two squares always have four normals.
        raise GridSlackError("no separating normal")
    return best


def near_pairs(g: Geometry, reach: float) -> list[tuple[int, int]]:
    """Index pairs `i < j` whose start centres are within `reach`."""
    dx = g.x0[:, None] - g.x0[None, :]
    dy = g.y0[:, None] - g.y0[None, :]
    close = np.triu(dx * dx + dy * dy < reach * reach, 1)
    return [(int(i), int(j)) for i, j in zip(*np.nonzero(close), strict=True)]


def separation_rows(g: Geometry, trust: float) -> Rows:
    """Every pair that could meet within the trust region, kept apart along its normal."""
    rows = Rows()
    for i, j in near_pairs(g, math.sqrt(2) + 2 * math.sqrt(2) * trust + 0.05):
        normal, reach, _gap = best_normal(g, i, j)
        rows.add(_pair_form(i, j, normal), reach, math.inf, f"apart {i + 1} {j + 1}")
    return rows


def coordinate_bounds(g: Geometry, trust: float) -> tuple[np.ndarray, np.ndarray]:
    """The trust region intersected with the container, per centre coordinate."""
    n = len(g.rotation)
    lo, hi = np.empty(2 * n), np.empty(2 * n)
    for i in range(n):
        for axis, (start, normal) in enumerate(((g.x0[i], (1.0, 0.0)), (g.y0[i], (0.0, 1.0)))):
            extent = _support(g.rotation[i], normal)
            low, high = max(extent, start - trust), min(g.side - extent, start + trust)
            if g.frozen[i] or low > high:  # Held, or past its wall by rounding.
                low = high = start if g.frozen[i] else min(max(start, extent), g.side - extent)
            lo[2 * i + axis], hi[2 * i + axis] = low, high
    return lo, hi


@dataclass(frozen=True)
class Candidate:
    """A coincidence the MILP may switch on: a flush pair or an axis square on a wall."""

    kind: str
    """`pair` or `wall`."""
    i: int
    j: int
    """The partner, or for a wall its axis (0 or 1)."""
    along: Vector
    """Pair: the face normal from `i` to `j`; wall: the inward axis."""
    across: Vector
    high: bool = False
    """Wall: the far wall at `s_W`."""


def _class_axes(rotation: Vector) -> tuple[Vector, Vector]:
    c, s = rotation
    return (c, s), (-s, c)


def candidates(g: Geometry, trust: float) -> list[Candidate]:
    """Every coincidence reachable from the start within the trust region."""
    found: list[Candidate] = []
    for i, j in near_pairs(g, 1 + 2 * math.sqrt(2) * trust + 0.05):
        if g.key[i] != g.key[j]:
            continue
        dx, dy = g.x0[j] - g.x0[i], g.y0[j] - g.y0[i]
        for face, across in (_class_axes(g.rotation[i]), _class_axes(g.rotation[i])[::-1]):
            distance = face[0] * dx + face[1] * dy
            along = face if distance >= 0 else (-face[0], -face[1])
            offset = across[0] * dx + across[1] * dy
            if abs(abs(distance) - 1) < 2 * trust and abs(offset) < 2 * trust:
                found.append(Candidate("pair", i, j, along, across))
    for i, axis in enumerate(g.axis):
        if not axis:
            continue
        for coordinate, start in ((0, g.x0[i]), (1, g.y0[i])):
            if start - 0.5 < trust:
                found.append(Candidate("wall", i, coordinate, (0.0, 0.0), (0.0, 0.0)))
            if g.side - 0.5 - start < trust:
                found.append(
                    Candidate("wall", i, coordinate, (0.0, 0.0), (0.0, 0.0), high=True)
                )
    return found


def _id_index(witness: Mapping[str, Any]) -> dict[str, int]:
    return {str(row["id"]): index for index, row in enumerate(witness["squares"])}


WALL_FACES = {"wall-left": (0, False), "wall-right": (0, True), "wall-bottom": (1, False)}
WALL_FACES["wall-top"] = (1, True)


@dataclass
class Kept:
    """The witness's contacts the placement must keep, and those it cannot state."""

    rows: Rows
    unstated: list[str]


def kept_contacts(witness: Mapping[str, Any], g: Geometry) -> Kept:
    """Rows keeping every house and stage contact of the witness from getting worse."""
    exact, frame, _degrees = shades.packings_from_witness(dict(witness))
    index = _id_index(witness)
    rows, unstated = Rows(), []
    house = shades.edge_rule_contacts(exact, HOUSE)
    for i, found in enumerate(house):
        for contact in found:
            if contact.other in WALL_FACES:
                if not g.axis[i]:
                    unstated.append(f"house {i + 1} {contact.other}: not axis-aligned")
                    continue
                axis, high = WALL_FACES[contact.other]
                _wall_row(rows, g, i, axis=axis, high=high)
                continue
            j = index[contact.other]
            if j < i:
                continue
            if g.key[i] != g.key[j]:
                unstated.append(f"house {i + 1} {j + 1}: two rotation classes")
                continue
            _flush_rows(rows, g, i, j)
    stage = shades.centre_rule_contacts(frame, STAGE)
    for i, found in enumerate(stage):
        for contact in found:
            if contact.other in WALL_FACES:
                axis, high = WALL_FACES[contact.other]
                start = (g.x0, g.y0)[axis][i]
                offset = (g.side - 0.5 - start) if high else (start - 0.5)
                bound = max(abs(offset), STAGE_MARGIN)
                centre = g.side - 0.5 if high else 0.5
                rows.add(
                    {2 * i + axis: 1.0}, centre - bound, centre + bound, f"stage {i + 1} wall"
                )
                continue
            j = index[contact.other]
            if j < i:
                continue
            _stage_rows(rows, g, i, j)
    return Kept(rows, unstated)


def _wall_row(rows: Rows, g: Geometry, i: int, *, axis: int, high: bool) -> None:
    """Keep an axis square's house wall residual from growing."""
    start = (g.x0, g.y0)[axis][i]
    extent = _support(g.rotation[i], (1.0, 0.0) if axis == 0 else (0.0, 1.0))
    if high:
        bound = max(g.side - extent - start, EPSILON)
        rows.add({2 * i + axis: 1.0}, g.side - extent - bound, math.inf, f"house {i + 1} wall")
    else:
        bound = max(start - extent, EPSILON)
        rows.add({2 * i + axis: 1.0}, -math.inf, extent + bound, f"house {i + 1} wall")


def _flush_rows(rows: Rows, g: Geometry, i: int, j: int) -> None:
    """Keep a same-class pair's offsets across and along its shared face from growing."""
    dx, dy = g.x0[j] - g.x0[i], g.y0[j] - g.y0[i]
    first, second = _class_axes(g.rotation[i])
    along, across = (
        (first, second)
        if abs(first[0] * dx + first[1] * dy) >= abs(second[0] * dx + second[1] * dy)
        else (second, first)
    )
    distance = along[0] * dx + along[1] * dy
    if distance < 0:
        along = (-along[0], -along[1])
        distance = -distance
    offset = across[0] * dx + across[1] * dy
    gap = max(abs(distance - 1), EPSILON)
    shift = max(abs(offset), EPSILON)
    label = f"house {i + 1} {j + 1}"
    rows.add(_pair_form(i, j, along), 1 - gap, 1 + gap, label)
    rows.add(_pair_form(i, j, across), -shift, shift, label)


def _stage_rows(rows: Rows, g: Geometry, i: int, j: int) -> None:
    """Keep a stage contact within the stage's gap, in square `i`'s frame."""
    dx, dy = g.x0[j] - g.x0[i], g.y0[j] - g.y0[i]
    u, v = _class_axes(g.rotation[i])
    along, across = u[0] * dx + u[1] * dy, v[0] * dx + v[1] * dy
    if abs(abs(across) - 1) < abs(abs(along) - 1):
        u, v, along, across = v, u, across, along
    sign = 1.0 if along >= 0 else -1.0
    reach = max(abs(abs(along) - 1), STAGE_MARGIN)
    shift = max(abs(across), STAGE_MARGIN)
    label = f"stage {i + 1} {j + 1}"
    rows.add(_pair_form(i, j, (sign * u[0], sign * u[1])), 1 - reach, 1 + reach, label)
    rows.add(_pair_form(i, j, v), -shift, shift, label)


# --------------------------------------------------------------------------- placement


@dataclass
class Placement:
    status: str
    x: np.ndarray | None
    y: np.ndarray | None
    chosen: list[Candidate]
    objective: float | None
    bound: float | None
    seconds: float
    detail: dict[str, Any] = field(default_factory=dict)


def _l1_rows(rows: Rows, g: Geometry) -> None:
    """`u_k >= |v_k - v0_k|` for each coordinate, auxiliaries after the coordinates."""
    n = len(g.rotation)
    for k in range(2 * n):
        start = g.x0[k // 2] if k % 2 == 0 else g.y0[k // 2]
        aux = 2 * n + k
        rows.add({aux: 1.0, k: -1.0}, -start, math.inf, "move")
        rows.add({aux: 1.0, k: 1.0}, start, math.inf, "move")
    for i in range(n):
        rows.add({2 * n + 2 * i: 1.0, 2 * n + 2 * i + 1: 1.0}, 0.0, MOVE_BOUND, "move bound")


def feasible(g: Geometry, kept: Rows, trust: float) -> bool:
    """Whether any placement exists with these rotations: an LP with no objective.

    It holds the rows `place` holds, the move bound included (`_l1_rows`, with their
    auxiliary columns), so a straightening it accepts never leaves the placement
    infeasible (review B of #530, B5).
    """
    n = len(g.rotation)
    rows = separation_rows(g, trust)
    _extend(rows, kept)
    _l1_rows(rows, g)
    lo, hi = coordinate_bounds(g, trust)
    result = linprog(
        np.zeros(4 * n),
        bounds=[*zip(lo, hi, strict=True), *[(0.0, None)] * (2 * n)],
        method="highs",
        options={"primal_feasibility_tolerance": LP_TOLERANCE},
        **_two_sided(rows, 4 * n),
    )
    return bool(result.status == 0)


def _extend(rows: Rows, other: Rows) -> None:
    rows.entries.extend(other.entries)
    rows.lo.extend(other.lo)
    rows.hi.extend(other.hi)
    rows.labels.extend(other.labels)


def _two_sided(rows: Rows, columns: int) -> dict[str, Any]:
    """`linprog`'s one-sided `A_ub`/`A_eq` form of two-sided rows."""
    matrix = rows.matrix(columns).tocsr()
    upper_rows: list[int] = []
    upper_rhs: list[float] = []
    signs: list[float] = []
    eq_rows: list[int] = []
    eq_rhs: list[float] = []
    for k, (lo, hi) in enumerate(zip(rows.lo, rows.hi, strict=True)):
        if lo == hi:
            eq_rows.append(k)
            eq_rhs.append(lo)
            continue
        if math.isfinite(hi):
            upper_rows.append(k)
            upper_rhs.append(hi)
            signs.append(1.0)
        if math.isfinite(lo):
            upper_rows.append(k)
            upper_rhs.append(-lo)
            signs.append(-1.0)
    arguments: dict[str, Any] = {}
    if upper_rows:
        upper = matrix[upper_rows, :]
        arguments["A_ub"] = csr_array(upper.multiply(np.array(signs)[:, None]))
        arguments["b_ub"] = np.array(upper_rhs)
    if eq_rows:
        arguments["A_eq"] = matrix[eq_rows, :]
        arguments["b_eq"] = np.array(eq_rhs)
    return arguments


def _milp(
    objective: np.ndarray,
    rows: Rows,
    columns: int,
    *,
    bounds: tuple[np.ndarray, np.ndarray],
    integrality: np.ndarray,
    settings: Settings,
) -> Any:
    """HiGHS through `milp`, retried over `HIGHS_RETRIES` until it returns a point.

    HiGHS checks its own MIP solution at the end and reports a solve error, with no point,
    when a row is off by more than its feasibility tolerance: a binary `1e-6` short of one
    times a big-M is such a row. Which tolerance and presolve setting avoids it depends on
    the model (n = 154 needed `1e-9`; n = 302 and 303 with wider kept rows needed the
    defaults), and the point is only a proposal that `replace_flush` re-solves, so each
    setting is tried in turn. `milp` passes options it does not know to HiGHS verbatim,
    with a warning this silences.
    """
    result: Any = None
    for tolerance, presolve in HIGHS_RETRIES:
        options: dict[str, Any] = {
            "time_limit": settings.time_limit,
            "mip_rel_gap": 0.0,
            "presolve": presolve,
        }
        if tolerance is not None:
            options["mip_feasibility_tolerance"] = tolerance
            options["primal_feasibility_tolerance"] = tolerance
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message="Unrecognized options detected")
            result = milp(
                objective,
                # `milp` takes `(A, lb, ub)` and `(lb, ub)` for its constraints and bounds.
                constraints=(rows.matrix(columns), np.array(rows.lo), np.array(rows.hi)),
                integrality=integrality,
                bounds=bounds,
                options=options,
            )
        if result.x is not None:
            break
    return result


def place(g: Geometry, kept: Rows, settings: Settings) -> Placement:
    """Maximize full shared sides within the trust region, then re-place exactly flush."""
    started = time.perf_counter()
    n = len(g.rotation)
    found = candidates(g, settings.trust)
    columns = 4 * n + len(found)
    rows = separation_rows(g, settings.trust)
    _extend(rows, kept)
    _l1_rows(rows, g)
    for k, candidate in enumerate(found):
        z = 4 * n + k
        if candidate.kind == "pair":
            i, j = candidate.i, candidate.j
            along = _pair_form(i, j, candidate.along)
            across = _pair_form(i, j, candidate.across)
            dx, dy = g.x0[j] - g.x0[i], g.y0[j] - g.y0[i]
            # Big-M per candidate: two centres within MOVE_BOUND each change a projection
            # of their difference by at most 2 * MOVE_BOUND, and tight M keeps HiGHS honest.
            reach = 2 * MOVE_BOUND + 0.01
            m_along = abs(candidate.along[0] * dx + candidate.along[1] * dy - 1) + reach
            m_across = abs(candidate.across[0] * dx + candidate.across[1] * dy) + reach
            rows.add({**along, z: m_along}, -math.inf, 1 + m_along, "coincide")
            rows.add({**along, z: -m_along}, 1 - m_along, math.inf, "coincide")
            rows.add({**across, z: m_across}, -math.inf, m_across, "coincide")
            rows.add({**across, z: -m_across}, -m_across, math.inf, "coincide")
        else:
            column = 2 * candidate.i + candidate.j
            start = (g.x0, g.y0)[candidate.j][candidate.i]
            if candidate.high:  # s - 1/2 - v <= M (1 - z)
                m_wall = abs(g.side - 0.5 - start) + MOVE_BOUND + 0.01
                rows.add({column: -1.0, z: m_wall}, -math.inf, m_wall - g.side + 0.5, "wall")
            else:  # v - 1/2 <= M (1 - z)
                m_wall = abs(start - 0.5) + MOVE_BOUND + 0.01
                rows.add({column: 1.0, z: m_wall}, -math.inf, m_wall + 0.5, "wall")
    lo, hi = coordinate_bounds(g, settings.trust)
    weight = 0.5 / (2 * n * settings.trust)
    objective = np.concatenate(
        [
            np.zeros(2 * n),
            np.full(2 * n, weight),
            np.array([-2.0 if c.kind == "pair" else -1.0 for c in found]),
        ]
    )
    result = _milp(
        objective,
        rows,
        columns,
        bounds=(
            np.concatenate([lo, np.zeros(2 * n), np.zeros(len(found))]),
            np.concatenate([hi, np.full(2 * n, np.inf), np.ones(len(found))]),
        ),
        integrality=np.concatenate([np.zeros(4 * n), np.ones(len(found))]),
        settings=settings,
    )
    milp_seconds = time.perf_counter() - started
    detail: dict[str, Any] = {
        "candidates": len(found),
        "rows": len(rows.entries),
        "milp_status": int(result.status),
        "milp_message": str(result.message),
        "milp_seconds": round(milp_seconds, 2),
    }
    if result.x is None:
        return Placement("milp-failed", None, None, [], None, None, milp_seconds, detail)
    chosen = [c for c, z in zip(found, result.x[4 * n :], strict=True) if z > 0.5]
    bound = getattr(result, "mip_dual_bound", None)
    detail["sides_switched_on"] = sum(2 if c.kind == "pair" else 1 for c in chosen)
    replaced = replace_flush(g, kept, chosen, settings)
    detail.update(replaced.detail)
    replaced.objective = float(result.fun)
    replaced.bound = None if bound is None else float(bound)
    replaced.seconds = time.perf_counter() - started
    replaced.detail = detail
    return replaced


def _flush(g: Geometry, candidate: Candidate) -> list[tuple[dict[int, float], float]]:
    """A coincidence as equality rows `a . v = t`."""
    if candidate.kind == "pair":
        i, j = candidate.i, candidate.j
        return [
            (_pair_form(i, j, candidate.along), 1.0),
            (_pair_form(i, j, candidate.across), 0.0),
        ]
    target = g.side - 0.5 if candidate.high else 0.5
    return [({2 * candidate.i + candidate.j: 1.0}, target)]


def _flush_lp(
    g: Geometry, kept: Rows, chosen: Sequence[Candidate], settings: Settings, *, elastic: bool
) -> Any:
    """The L1-nearest placement with `chosen` flush: exactly, or, `elastic`, with a priced
    slack on each equality so that an inconsistent set still solves and shows which."""
    n = len(g.rotation)
    rows = separation_rows(g, settings.trust)
    _extend(rows, kept)
    _l1_rows(rows, g)
    equalities = [row for candidate in chosen for row in _flush(g, candidate)]
    columns = 4 * n + (2 * len(equalities) if elastic else 0)
    for k, (coefficients, target) in enumerate(equalities):
        if elastic:  # a . v + s+ - s- = t
            plus, minus = 4 * n + 2 * k, 4 * n + 2 * k + 1
            rows.add({**coefficients, plus: 1.0, minus: -1.0}, target, target, "flush")
        else:
            rows.add(coefficients, target, target, "flush")
    lo, hi = coordinate_bounds(g, settings.trust)
    objective = np.concatenate(
        [np.zeros(2 * n), np.ones(2 * n), np.full(columns - 4 * n, ELASTIC_PRICE)]
    )
    lower = np.concatenate([lo, np.zeros(columns - 2 * n)])
    upper = np.concatenate([hi, np.full(columns - 2 * n, np.inf)])
    return linprog(
        objective,
        bounds=list(zip(lower, upper, strict=True)),
        method="highs",
        options={
            "primal_feasibility_tolerance": LP_TOLERANCE,
            "dual_feasibility_tolerance": LP_TOLERANCE,
        },
        **_two_sided(rows, columns),
    )


def replace_flush(
    g: Geometry, kept: Rows, chosen: Sequence[Candidate], settings: Settings
) -> Placement:
    """The LP with the chosen coincidences as equalities, nearest the witness in L1.

    The MILP meets its rows only to HiGHS's MIP tolerance, about `1e-6`, so a chosen set
    can be inconsistent by less than that (a row of squares a hair too wide for its two
    walls). Then an elastic LP prices a slack on every equality, the coincidences it
    cannot meet within `1e-9` are dropped, and the exact LP runs again on the rest.
    """
    started = time.perf_counter()
    n = len(g.rotation)
    kept_set = list(chosen)
    result = _flush_lp(g, kept, kept_set, settings, elastic=False)
    detail: dict[str, Any] = {"lp_status": int(result.status), "dropped": 0}
    if result.status != 0:
        relaxed = _flush_lp(g, kept, kept_set, settings, elastic=True)
        if relaxed.status == 0:
            slacks = np.asarray(relaxed.x)[4 * n :]
            position, survivors = 0, []
            for candidate in kept_set:
                width = 2 * len(_flush(g, candidate))
                if float(np.max(slacks[position : position + width])) <= DROP_SLACK:
                    survivors.append(candidate)
                position += width
            detail["dropped"] = len(kept_set) - len(survivors)
            kept_set = survivors
            result = _flush_lp(g, kept, kept_set, settings, elastic=False)
            detail["lp_status"] = int(result.status)
    seconds = time.perf_counter() - started
    detail["lp_seconds"] = round(seconds, 2)
    if result.status != 0 or result.x is None:
        return Placement("lp-failed", None, None, kept_set, None, None, seconds, detail)
    values = np.asarray(result.x)
    return Placement(
        "placed",
        values[0 : 2 * n : 2],
        values[1 : 2 * n : 2],
        kept_set,
        None,
        None,
        seconds,
        detail,
    )


def choose_snaps(
    witness: Mapping[str, Any], frame: same.Frame, settings: Settings, *, freeze: bool
) -> tuple[list[int], list[int], list[float]]:
    """The near-axis squares that can be straightened, those that cannot, and the tilts."""
    tilts = [tilt_degrees(rotation) for rotation in frame.rotations]
    near = sorted(
        (index for index, tilt in enumerate(tilts) if 0 < tilt < settings.near_axis_degrees),
        key=lambda index: (tilts[index], index),
    )
    if not near:
        return [], [], tilts
    g = geometry(frame, near, freeze=freeze)
    if feasible(g, kept_contacts(witness, g).rows, settings.trust):
        return near, [], tilts
    kept_snaps: list[int] = []
    refused: list[int] = []
    for index in near:
        trial = geometry(frame, [*kept_snaps, index], freeze=freeze)
        if feasible(trial, kept_contacts(witness, trial).rows, settings.trust):
            kept_snaps.append(index)
        else:
            refused.append(index)
    return kept_snaps, refused, tilts


# --------------------------------------------------------------------------- the exact view


def float_poses(
    frame: same.Frame, g: Geometry, placement: Placement
) -> tuple[list[same.GeneratorPose], set[int]]:
    """The placement as the re-solve reads it, and the squares it changed.

    A square the LP moved by less than `UNMOVED`, or a frozen one, keeps its exact centre:
    the LP's noise of `1e-12` would otherwise reach the re-solve. A straightened square is
    changed whether it moved or not.
    """
    if placement.x is None or placement.y is None:
        raise GridSlackError("no placement")
    turned = set(g.snapped)
    poses: list[same.GeneratorPose] = []
    changed: set[int] = set(turned)
    for index, ((x, y), rotation) in enumerate(
        zip(frame.centers, frame.rotations, strict=True)
    ):
        fx, fy = float(placement.x[index]), float(placement.y[index])
        moved = abs(fx - g.x0[index]) > UNMOVED or abs(fy - g.y0[index]) > UNMOVED
        degrees = "0" if index in turned else repr(same.degrees_of(rotation))
        if moved and not g.frozen[index]:
            changed.add(index)
            poses.append(same.GeneratorPose(repr(fx), repr(fy), degrees))
        else:
            poses.append(
                same.GeneratorPose(
                    same.plain_decimal(x, 50), same.plain_decimal(y, 50), degrees
                )
            )
    return poses, changed


def rational_bound(n: int) -> Fraction | None:
    """The record's verified upper bound `U` where it is a rational number exactly: its
    exact form a fraction, or no exact form beside the printed decimal. A closed form's
    60-digit value is not the bound, so no view is solved at it."""
    facts = driver.case_facts(n)
    if facts["verified_upper_bound"] is None:
        return None
    if facts["exact_form"] is not None:
        try:
            Fraction(str(facts["exact_form"]).replace(" ", ""))
        except ValueError:
            return None
    return driver.upper_bound(facts)


def frame_for(witness: Mapping[str, Any], relation: str) -> same.Frame | None:
    """The exact frame at `s_W` (`same`), or the same squares at `U` (`bound`) where the
    record's verified upper bound is rational (`rational_bound`) and not `s_W`: above it,
    a box the view may still fit; below it, the best known side, which the owner asked a
    view to reach (13 October 2026). A box of a closed form's 60-digit value would be a
    side above `U`, labelled `bound`, so none is tried (review B of #530, B1)."""
    frame = same.exact_frame(witness)
    if relation == "same":
        return frame
    upper = rational_bound(int(witness["n"]))
    if upper is None or upper == frame.side:
        return None
    return replace(
        frame,
        side=upper,
        derivation=f"{frame.derivation}, in a box of the verified upper bound U",
    )


def attempts_for(witness: Mapping[str, Any]) -> tuple[tuple[str, bool], ...]:
    """`ATTEMPTS`, or `BOUND_FIRST` where the witness's side is above a rational `U`: a
    view at `s_W` would draw the packing above the best known side (owner, 13 October
    2026), so it is tried only after no view at the bound could be found."""
    try:
        side = same.exact_frame(witness).side
    except same.SameSideError:
        return ATTEMPTS
    upper = rational_bound(int(witness["n"]))
    return BOUND_FIRST if upper is not None and upper < side else ATTEMPTS


@dataclass
class Exact:
    """The re-solve of one placement: the view, or why there is none."""

    witness: dict[str, Any] | None
    report: dict[str, Any]


def _squares_of(row: same.Row) -> set[int]:
    return {column // 2 for column in row.coefficients}


def closable(
    rows: Sequence[same.Row], frame: same.Frame, changed: set[int]
) -> tuple[list[same.Row], list[same.Row]]:
    """The tight rows to close, and those left open.

    A row between squares the placement left alone is closed only if the witness's own
    centres close it or overlap across it (a signed gap of at most `EXACT_GAP`): a near
    contact of the source, `1e-12` apart along two nearly parallel faces at n = 105, is
    not a contact, and closing it pins a centre through a near-singular pair of rows,
    while a decimal witness's promotion can overlap by up to its `1e-8` tolerance, which
    only closing separates. Upstream's `reg.refine` keeps the first half of the rule
    (`1e-14` at 80 digits).
    """
    values = {
        2 * index + axis: centre[axis]
        for index, centre in enumerate(frame.centers)
        for axis in (0, 1)
    }
    kept: list[same.Row] = []
    left: list[same.Row] = []
    for row in rows:
        closes = _squares_of(row) & changed or float(row.gap(values)) <= EXACT_GAP
        (kept if closes else left).append(row)
    return kept, left


def anchor(rows: Sequence[same.Row], fixed: Mapping[int, Fraction]) -> list[same.Row]:
    """`rows` with the `fixed` columns substituted by their values: the same contacts, in
    the same order, over the remaining columns. A row left with no column is kept, so the
    elimination reads it as dependent (its gap is zero) or relaxed (its gap has a sign), and
    a negative one is reported penetrated like any other."""
    if not fixed:
        return list(rows)
    anchored: list[same.Row] = []
    for row in rows:
        moved = sum(
            (
                value * fixed[column]
                for column, value in row.coefficients.items()
                if column in fixed
            ),
            Fraction(0),
        )
        anchored.append(
            replace(
                row,
                coefficients={
                    column: value
                    for column, value in row.coefficients.items()
                    if column not in fixed
                },
                rhs=row.rhs - moved,
            )
        )
    return anchored


def settle_reopening(
    rows: Sequence[same.Row],
    left: Sequence[same.Row],
    generator: Sequence[tuple[Fraction, Fraction]],
    fixed: Mapping[int, Fraction] | None = None,
) -> tuple[same.Solution, list[same.Row], int, int]:
    """`regularize_same_side.settle` on `rows`; a row left open that the solution
    penetrates is closed after all, in its priority place, and the solve repeated.

    Columns in `fixed` are held at their values (an anchored square keeps its exact
    centre): they are substituted out of every row before the elimination and are neither
    pinned nor free in the solution."""
    fixed = dict(fixed or {})
    closing = list(rows)
    waiting = list(left)
    reopened = 0
    rounds_left = MAX_REOPEN_ROUNDS
    while True:
        solution, promoted, rounds = same.settle(
            anchor(closing, fixed), len(generator), generator, mode="relax"
        )
        if fixed:
            solution = replace(
                solution,
                values={**solution.values, **fixed},
                free_columns=[c for c in solution.free_columns if c not in fixed],
            )
        penetrated = [row for row in waiting if row.gap(solution.values) < 0]
        rounds_left -= 1
        if not penetrated or rounds_left == 0:
            return solution, promoted, rounds, reopened
        reopened += len(penetrated)
        closing = sorted([*closing, *penetrated], key=lambda row: row.priority)
        waiting = [row for row in waiting if all(row is not other for other in penetrated)]


def float_clearance(
    side: Fraction, matched: Sequence[same.Matched], centers: Sequence[same.Point]
) -> tuple[float, str]:
    """The least gap of an exact pose in binary64, over near pairs and walls, and where."""
    rotations = [(float(m.rotation[0]), float(m.rotation[1])) for m in matched]
    g = Geometry(
        side=float(side),
        x0=np.array([float(x) for x, _ in centers]),
        y0=np.array([float(y) for _, y in centers]),
        rotation=rotations,
        key=[],
        axis=[],
        frozen=[False] * len(rotations),
    )
    worst, where = math.inf, ""
    for i, j in near_pairs(g, math.sqrt(2) + 0.01):
        gap = best_normal(g, i, j)[2]
        if gap < worst:
            worst, where = gap, f"squares {i + 1} and {j + 1}"
    for i, rotation in enumerate(rotations):
        for axis, start in enumerate((g.x0[i], g.y0[i])):
            extent = _support(rotation, (1.0, 0.0) if axis == 0 else (0.0, 1.0))
            for gap in (start - extent, g.side - extent - start):
                if gap < worst:
                    worst, where = gap, f"square {i + 1} and a wall"
    return worst, where


@dataclass
class Settled:
    """One way of closing the tight set, and what the cheap checks found."""

    rows: str
    """`witness-contacts` (closable's rule), `all-tight` (the resolver's own), or
    closable's rule with unchanged squares held at their exact centres: the tilted ones
    (`anchored-tilted`) or all of them (`anchored`)."""
    solution: same.Solution
    centers: list[same.Point]
    record: dict[str, Any]
    refusal: str | None


ANCHORED = ("anchored-tilted", "anchored")
"""The fallbacks, tried after both ways of closing fail. Elimination pins an unchanged
square through any chain of tight rows, so a chain through a moved square can move it by
a few `1e-35` and leave a contact between two unchanged tilted squares as far inside
(n = 272: squares 254 and 255 at 19.7 degrees, the promotion loop's 16 rounds spent).
Holding unchanged squares at the witness's exact centres keeps the witness's own exact
contacts among them, and leaves the moved squares to close against them."""


def anchored_squares(
    rows: str, frame: same.Frame, matched: Sequence[same.Matched], changed: set[int]
) -> list[int]:
    """The squares `rows` holds at their exact centres: unchanged, with their own exact
    rotation (a class merged onto another square's rotation is not the witness's pose),
    and tilted for `anchored-tilted`."""
    if rows not in ANCHORED:
        return []
    return [
        index
        for index, m in enumerate(matched)
        if index not in changed
        and canonical(m.rotation) == canonical(frame.rotations[index])
        and (rows == "anchored" or m.source is not None)
    ]


def settle_variant(
    rows: str,
    *,
    frame: same.Frame,
    poses: Sequence[same.GeneratorPose],
    matched: Sequence[same.Matched],
    tight: Sequence[same.Row],
    watched: Sequence[same.Row],
    changed: set[int],
) -> Settled:
    """Close the tight set one way and run the checks that need no exact route.

    `watched` are the contacts within `WATCH` of the placement but not tight: closed only
    if the exact solution, which may move a pinned centre by up to `BLOWUP`, penetrates
    them.
    """
    generator = [(same.rounded_fraction(p.x), same.rounded_fraction(p.y)) for p in poses]
    if rows == "all-tight":
        closing, left = list(tight), []
    else:
        closing, left = closable(tight, frame, changed)
    left = [*left, *watched]
    held = anchored_squares(rows, frame, matched, changed)
    fixed = {2 * index + axis: frame.centers[index][axis] for index in held for axis in (0, 1)}
    solution, promoted, rounds, reopened = settle_reopening(closing, left, generator, fixed)
    centers = [(solution.values[2 * i], solution.values[2 * i + 1]) for i in range(len(poses))]
    displacement = max(
        math.hypot(float(x) - float(p.x), float(y) - float(p.y))
        for (x, y), p in zip(centers, poses, strict=True)
    )
    penetrated = [row for row in solution.relaxed if row.gap(solution.values) < 0]
    record: dict[str, Any] = {
        "rows": rows,
        "closed": len(closing) + reopened,
        "left_open": len(left) - reopened,
        "reopened": reopened,
        "used": len(solution.used),
        "dependent": len(solution.dependent),
        "relaxed": len(solution.relaxed),
        "promoted": len(promoted),
        "rounds": rounds,
        "free_coordinates": len(solution.free_columns),
        "anchored": len(held),
        "displacement": displacement,
    }
    refusal = None
    if penetrated:
        refusal = f"penetrated: {len(penetrated)} relaxed rows overlap at this side"
    elif displacement > BLOWUP:
        refusal = f"ill-conditioned: a re-solved centre moved {displacement:.3g}"
    else:
        clearance, where = float_clearance(frame.side, matched, centers)
        record["float_clearance"] = clearance
        if clearance < -FLOAT_OVERLAP:
            refusal = f"overlap in binary64: {where}, {clearance:.3g}"
    record["refusal"] = refusal
    return Settled(rows, solution, centers, record, refusal)


def verified_variant(
    variant: Settled,
    witness: Mapping[str, Any],
    frame: same.Frame,
    matched: Sequence[same.Matched],
    view_id: str,
) -> tuple[Settled, dict[str, Any]] | None:
    """A settled variant written as a witness and decided on both exact routes, or None
    with the reason recorded on the variant, so the next way of closing is tried."""
    try:
        document = same.same_side_witness(
            witness, frame, variant.centers, matched, view_id=view_id
        )
    except ValueError as error:  # Elimination fill-in past Python's integer-text limit.
        variant.refusal = variant.record["refusal"] = f"literal-too-long: {error}"
        return None
    verdicts = same.verify_both(document, variant.centers, matched, frame.side)
    variant.record["verdicts"] = verdicts
    if not (verdicts["exact_verify"]["passed"] and verdicts["independent"]["passed"]):
        variant.refusal = variant.record["refusal"] = (
            "overlap: an exact route refuses the re-solved pose"
        )
        return None
    return variant, document


def exact_view(
    witness: Mapping[str, Any],
    frame: same.Frame,
    poses: Sequence[same.GeneratorPose],
    changed: set[int],
    relation: str,
) -> Exact:
    """The placement re-solved exactly in `frame` and decided on both exact routes.

    These are `regularize_same_side.resolve`'s parts in its order -- `match_rotations`,
    `tight_rows`, `settle` in relax mode, `same_side_witness`, `verify_both` -- with two
    changes: which tight rows are closed, and the frame's side, which is `U` for a
    `bound` view. Two ways of closing are tried, the first that passes the cheap checks
    is verified: `closable`'s rule (the witness's own contacts among squares the
    placement left alone) and the resolver's (every row tight at the placement). A
    rational witness's contacts are exact, so its rule comes first; a decimal witness's
    promotion carries near contacts of up to its `1e-8` tolerance, which only the
    resolver's closes consistently, so it comes first there. A relaxed row left
    penetrated (the side too small), a re-solved centre more than `BLOWUP` from the
    placement (nearly parallel rows) or an overlap binary64 already sees refuses a way
    before the expensive verification. When both ways fail, at a cheap check, at a
    literal past Python's integer-text limit or on an exact route, closable's rule is
    tried again with the unchanged squares held at their exact centres (`ANCHORED`):
    first the tilted ones, then all of them.
    """
    started = time.perf_counter()
    view_id = regularized_id(witness)
    matched = same.match_rotations(frame, poses)
    tight = same.tight_rows(frame, poses, matched)
    keys = {row.priority for row in tight}
    watched = [
        row
        for row in same.tight_rows(frame, poses, matched, tight=WATCH)
        if row.priority not in keys
    ]
    order = (
        ("witness-contacts", "all-tight", *ANCHORED)
        if frame.kind == "rational"
        else ("all-tight", "witness-contacts", *ANCHORED)
    )
    report: dict[str, Any] = {
        "relation": relation,
        "side": same.literal(frame.side),
        "tight": len(tight),
        "watched": len(watched),
        "settled": [],
    }
    tried: list[Settled] = []
    found: tuple[Settled, dict[str, Any]] | None = None
    for rows in order:
        variant = settle_variant(
            rows,
            frame=frame,
            poses=poses,
            matched=matched,
            tight=tight,
            watched=watched,
            changed=changed,
        )
        tried.append(variant)
        report["settled"].append(variant.record)
        if variant.refusal is None:
            found = verified_variant(variant, witness, frame, matched, view_id)
            if found is not None:
                break
    report["seconds"] = round(time.perf_counter() - started, 2)
    if found is None:
        report["refusal"] = "; ".join(f"{v.rows}: {v.refusal}" for v in tried)
        return Exact(None, report)
    chosen, document = found
    solution = chosen.solution
    report["verdicts"] = chosen.record.pop("verdicts")
    document["claim"]["coordinate_provenance"] = "verified"
    if relation == "bound":
        document["claim"]["limitations"] = document["claim"]["limitations"].replace(
            "at the witness's side", "at the record's verified upper bound U"
        )
    document["certificate"] = {
        "side_relation": relation,
        "derived_from": witness["id"],
        "exact_frame": {"kind": frame.kind, "derivation": frame.derivation},
        "resolve": {
            "tool": "devtools.regularize_same_side's parts, in devtools.regularize_grid_slack",
            "mode": "relax",
            "rows": chosen.rows,
            "rows_used": len(solution.used),
            "rows_left_open": chosen.record["left_open"],
            "rows_relaxed": len(solution.relaxed),
            "free_coordinates": len(solution.free_columns),
            "anchored_squares": chosen.record["anchored"],
        },
        "replay": "uv run --frozen packing-witness verify <this file>",
    }
    return Exact(document, report)


def regularized_id(witness: Mapping[str, Any]) -> str:
    """The id of a witness's view, as `exact_view` writes it and admission holds it."""
    return f"{witness['id']}-regularized"


ATTEMPTS = (("same", False), ("same", True), ("bound", False), ("bound", True))
"""Frames and whether tilted squares are frozen, tried in order until one gives a view."""
BOUND_FIRST = (("bound", False), ("bound", True), ("same", False), ("same", True))
"""The order where the witness's side is above the bound (`attempts_for`)."""


def attempt(
    witness: Mapping[str, Any],
    frame: same.Frame,
    relation: str,
    settings: Settings,
    *,
    freeze: bool,
) -> tuple[Exact | None, dict[str, Any], list[int]]:
    """One placement and its exact re-solve in one frame."""
    started = time.perf_counter()
    snaps, unsnapped, tilts = choose_snaps(witness, frame, settings, freeze=freeze)
    record: dict[str, Any] = {
        "relation": relation,
        "frozen_tilted": freeze,
        "straightened": [
            {"square": index + 1, "degrees": round(tilts[index], 6)} for index in snaps
        ],
        "not_straightened": [
            {"square": index + 1, "degrees": round(tilts[index], 6)} for index in unsnapped
        ],
    }
    g = geometry(frame, snaps, freeze=freeze)
    kept = kept_contacts(witness, g)
    record["kept_rows"] = len(kept.rows.entries)
    record["unstated_contacts"] = kept.unstated
    placement = place(g, kept.rows, settings)
    record["placement"] = {
        "status": placement.status,
        "objective": placement.objective,
        "dual_bound": placement.bound,
        "coincidences": len(placement.chosen),
        "seconds": round(placement.seconds, 2),
        **placement.detail,
    }
    if placement.status != "placed" or placement.x is None or placement.y is None:
        record["refusal"] = f"placement: {placement.status}"
        record["seconds"] = round(time.perf_counter() - started, 2)
        return None, record, snaps
    moves = np.hypot(np.asarray(placement.x) - g.x0, np.asarray(placement.y) - g.y0)
    record["float_moves"] = {
        "max": float(moves.max()),
        "moved_beyond_1e-6": int((moves > 1e-6).sum()),
    }
    poses, changed = float_poses(frame, g, placement)
    record["changed_squares"] = len(changed)
    exact = exact_view(witness, frame, poses, changed, relation)
    record["exact"] = exact.report
    if exact.witness is None:
        record["refusal"] = exact.report.get("refusal")
    record["seconds"] = round(time.perf_counter() - started, 2)
    return exact, record, snaps


def regularize(
    witness: Mapping[str, Any], settings: Settings
) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    """The view of one witness at `s_W`, else at `U`, or why there is none; and the report."""
    started = time.perf_counter()
    report: dict[str, Any] = {
        "generator": GENERATOR,
        "settings": {
            "near_axis_degrees": settings.near_axis_degrees,
            "trust": settings.trust,
            "time_limit": settings.time_limit,
            "stage_margin": STAGE_MARGIN,
        },
        "attempts": [],
    }
    for relation, freeze in attempts_for(witness):
        try:
            frame = frame_for(witness, relation)
        except same.SameSideError as error:
            report["refusal"] = f"no-exact-frame: {error.detail}"
            break
        if frame is None:
            continue
        exact, record, snaps = attempt(witness, frame, relation, settings, freeze=freeze)
        report["attempts"].append(record)
        if exact is None or exact.witness is None:
            continue
        view = exact.witness
        certificate = view.setdefault("certificate", {})
        certificate.update(
            kind="regularized-view",
            label="regularized",
            generator=GENERATOR,
            straightened=[index + 1 for index in snaps],
            frozen_tilted=freeze,
            method=METHOD,
        )
        report["relation"] = relation
        report["straightened"] = record["straightened"]
        report.pop("refusal", None)
        report["seconds"] = round(time.perf_counter() - started, 2)
        return view, report
    report.setdefault(
        "refusal",
        "; ".join(
            f"{r['relation']}/{r['frozen_tilted']}: {r.get('refusal')}"
            for r in report["attempts"]
        ),
    )
    report["seconds"] = round(time.perf_counter() - started, 2)
    return None, report


def own_pairing(
    view: Sequence[driver.Placed], source: Sequence[driver.Placed], named: Sequence[int]
) -> dict[str, Any]:
    """The view against the witness square for square, as this generator keeps them: the
    largest move and the turned squares (0-based, as `driver.identity` lists them).

    `driver.identity` pairs by `arrangement_gap`, which takes whichever of the box's eight
    symmetries gives the least largest move. A witness that is nearly symmetric can win
    under a reflection by a hair, and then pairs tilted squares with mirror partners of
    another angle: n = 259 reported 16 unnamed turns under symmetry 5, with none under its
    own pairing and the same largest move, 0.0638. The generator moves and turns squares
    in place, so its own pairing is the one the view was made by; both are reported.
    """
    turned = [
        index
        for index, ((_x, _y, c, s), (_u, _v, a, b)) in enumerate(zip(view, source, strict=True))
        if min(abs(c * b - s * a), abs(c * a + s * b)) > driver.TURN_BOUND
    ]
    largest = max(
        math.hypot(float(x - u), float(y - v))
        for (x, y, _c, _s), (u, v, _a, _b) in zip(view, source, strict=True)
    )
    return {
        "basis": "square for square, the generator's own pairing (symmetry 0)",
        "max_move": f"{largest:.6e}",
        "turned": turned,
        "unnamed_turns": sorted(set(turned) - set(named)),
    }


def measure(
    n: int, witness: Mapping[str, Any], view: Mapping[str, Any], straightened: Sequence[int]
) -> dict[str, Any]:
    """Identity, contact histograms against the witness and the current view, and the
    house renderer's evenness of the drawing."""
    frame = driver.source_frame(witness)
    side, placements, _corners = driver.view_geometry(view)
    reference = frame.side if frame.side is not None else Fraction(frame.side_text)
    named = [index - 1 for index in straightened]
    ident = driver.identity((side, placements), (reference, frame.placements), named, "witness")
    ident["own_pairing"] = own_pairing(placements, frame.placements, named)
    shaded = driver.contact_shades(n, witness, view, "witness")
    return {
        "identity": ident,
        "shades": shaded,
        "totals_fall": driver.totals_fall(shaded),
        "visible_change": driver.visible_change(ident, shaded),
        "drawing": regularity.regularity(view),
    }


def drawing(n: int, witness: Mapping[str, Any], view: Mapping[str, Any]) -> str:
    """The view drawn by the house renderer, stating the record's own evidence."""
    source = frame_from_witness(dict(witness))
    frame = replace(
        frame_from_witness(dict(view)),
        evidence=source.evidence,
        check=source.check,
        label=f"n={n} regularized (grid-slack prototype)",
        source_id=str(view["id"]),
        source_url=source.source_url,
    )
    return render_packing_svg(
        frame,
        spec=RenderSpec(
            overlays=frozenset(),
            title=f"Known-best packing of {n} unit squares, regularized (prototype)",
            description=(
                f"A regularized derived view of the known-best n={n} construction made by "
                "the grid-slack prototype, never the source witness. It changes no side, "
                "frontier value or evidence tier; the evidence stated is the record's."
            ),
        ),
    )


def _guard(run_dir: Path) -> Path:
    resolved = run_dir.resolve()
    for forbidden in FORBIDDEN_OUTPUT_ROOTS:
        if resolved.is_relative_to(forbidden.resolve()):
            raise GridSlackError(f"refusing to write under {forbidden}")
    return resolved


def _write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(path) as temporary:
        temporary.write_bytes(data)


def load_source(n: int) -> dict[str, Any]:
    document = load_yaml((KNOWN_BEST / f"n-{n:03d}.yaml").read_text(encoding="utf-8"))
    return document["witness"]


def source_record(n: int, data: bytes, witness: Mapping[str, Any]) -> dict[str, Any]:
    """The witness a run read, as its report names it: path, id, the digest of the bytes
    read, and its exact side `s_W` where it has a rational frame (review B of #530, B3).

    The digest is provenance only. Nothing compares it, and no verdict is bound to it
    (OR-18): an edit that leaves the packing as it was must not refuse a run. Nor can the
    id tell a re-housed witness from the one the run read, since a known-best witness's
    id is fixed per count. Whether a run still describes the witness a count holds today
    is decided by the admitting layer (#548's `admitted()`): it holds `s_W_exact` to the
    exact side of today's witness and measures identity again against it, comparing
    regenerated semantic results as OR-16 asks. The view itself is decided there too, on
    both exact routes as its file is then (`view_decided`).
    """
    try:
        side: str | None = same.literal(same.exact_frame(witness).side)
    except same.SameSideError:
        side = None
    return {
        "path": f"packing/witnesses/known-best/n-{n:03d}.yaml",
        "id": witness.get("id"),
        "witness_sha256": hashlib.sha256(data).hexdigest(),
        "s_W_exact": side,
    }


def run_one(n: int, run_dir: Path, settings: Settings) -> dict[str, Any]:
    """Regularize one count into `run_dir/n-NNN/`, and its report.

    An earlier run's view, drawing and report are removed first, so a re-run that finds
    no view, or stops, leaves none of them beside its own (review B of #530, B4). The
    report records when it was written (`finished`, UTC), which dates the run in the
    layer's index (`run_block`) as a copy or restore of the directory cannot. The
    report records the view's bytes by their Git blob id as provenance only: nothing
    compares it, and its verdicts are not bound to it (OR-18). The admitting layer reads
    the view file as it is then and decides it again on both exact routes, with its side
    and id held to this report's (`admitted`, `view_decided`).
    """
    directory = _guard(run_dir) / f"n-{n:03d}"
    for stale in ("report.json", "view.yaml.gz", "drawing.svg"):
        (directory / stale).unlink(missing_ok=True)
    data = (KNOWN_BEST / f"n-{n:03d}.yaml").read_bytes()
    witness = load_yaml(data.decode("utf-8"))["witness"]
    view, report = regularize(witness, settings)
    report["n"] = n
    report["source"] = source_record(n, data, witness)
    if view is not None:
        text = witness_document(view)
        validate_witness_document(
            load_yaml(text), path=directory / "view.yaml", fallback_schema=WITNESS_SCHEMA
        )
        stored = gzip.compress(text.encode("utf-8"), mtime=0)
        _write(directory / "view.yaml.gz", stored)
        report["view"] = {"path": "view.yaml.gz", "git_blob": git_blob(stored)}
        straightened = [row["square"] for row in report["straightened"]]
        report["measured"] = measure(n, witness, view, straightened)
        _write(directory / "drawing.svg", drawing(n, witness, view).encode("utf-8"))
    report["finished"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    _write(
        directory / "report.json", (json.dumps(report, indent=1, default=str) + "\n").encode()
    )
    return report


# --------------------------------------------------------------------------------------
# Admission: a run's views as the regularized layer draws them
# --------------------------------------------------------------------------------------


def decided(
    report: Mapping[str, Any],
    witness: Mapping[str, Any],
    routes: Mapping[str, bool] | None = None,
    *,
    upper: Fraction | None = None,
) -> driver.Decision:
    """The policy's decision table (section 4) applied to one count's view, as the driver
    applies it to its own: the exact routes, the side against `s_W` and `U`, and the
    per-square and total contact counts decide; the pairing, unnamed turns and largest
    move are measured and named in the reason, and decide nothing (rows 6 and 9, retired
    13 October 2026). `U` is the case record's, held exactly, unless `upper` is given, as
    `devtools.register_regularized_bounds` gives the view's own side to ask how the view
    is decided once it is registered.

    The exact routes are `routes` where admission ran them on the view as it is now
    (`view_decided`), else the verdicts the run recorded, as a run's own summary reads
    them (`run_block`)."""
    if "measured" not in report:
        return driver.classify(
            driver.Measured("same", produced=False, status=str(report.get("refusal")))
        )
    measured = report["measured"]
    ident = measured["identity"]
    shaded = measured["shades"]
    verdicts = report["attempts"][-1]["exact"]["verdicts"]
    side = Fraction(str(report["attempts"][-1]["exact"]["side"]))
    frame = driver.source_frame(witness)
    printed = frame.side if frame.side is not None else None
    # `U` held exactly (`verified_bound`): a closed form is compared with the side as the
    # root it is, not read as unknown; `upper` is `U` only where it is rational. A given
    # `upper` is a rational `U`, held so.
    if upper is None:
        bound = driver.verified_bound(driver.case_facts(int(report["n"])))
        upper = None if bound is None else bound.rational
    else:
        bound = driver.VerifiedBound(None, rational=upper)
    relation = driver.side_relation(side, printed, upper)
    current = shaded.get("against_current") or {}
    return driver.classify(
        driver.Measured(
            "same" if relation == "same" else "solved",
            produced=True,
            routes=dict(routes)
            if routes is not None
            else {
                "exact_verify": bool(verdicts["exact_verify"]["passed"]),
                "independent": bool(verdicts["independent"]["passed"]),
            },
            relation=relation,
            side=side,
            upper=upper,
            bound=bound,
            one_to_one=bool(ident.get("one_to_one")),
            unnamed_turns=tuple(ident.get("unnamed_turns") or ()),
            regressions=len(shaded.get("regressions") or [])
            + len(current.get("regressions") or []),
            max_move=Fraction(str(ident["max_move"])) if ident.get("max_move") else None,
            visible_change=bool(measured.get("visible_change")),
            totals_fall=bool(measured.get("totals_fall")),
        )
    )


def admitted(directory: Path, run_id: str) -> driver.Admitted:
    """One count's grid-slack view, admitted by the decision table's row 10, in the
    layer's terms (`devtools.regularize_evand.admit_views` writes it).

    The view admitted is the file in the run directory as it is now, decided again before
    anything is measured on it (#548 review C, C1): both exact routes run on it, and its
    exact side and id must be the ones its report decided (`view_decided`). The table
    decides on those routes, and the entry records them, never the report's verdicts, so
    a file edited, copied in or restored beside another report is refused rather than
    drawn with a verdict it never earned.

    The run read the known-best witness of the checkout it ran in; the entry is about the
    witness this checkout holds. So admission holds the view to it, not to the run's
    digests (#548 review B4): the run's exact side `s_W` (`source.s_W_exact`) must be this
    witness's, and the view's identity, shades and contacts are measured again against
    this witness (`measure`) and decided by the table on those measurements, so the entry
    never records what was measured on another witness. A view that no longer pairs one
    to one with it is refused. The run's witness digest and its view's blob id are its
    provenance, kept in its report and compared with nothing (OR-16, OR-18). A report from
    before the run recorded `s_W` is admitted on the measurement made here alone, and the
    entry says so (`measured.source_note`).
    """
    report = json.loads((directory / "report.json").read_text(encoding="utf-8"))
    n = int(report["n"])
    if report.get("generator") != GENERATOR:
        raise GridSlackError(f"n={n}: a view of {report.get('generator')}, not {GENERATOR}")
    path = KNOWN_BEST / f"n-{n:03d}.yaml"
    data = path.read_bytes()
    witness = load_yaml(data.decode("utf-8"))["witness"]
    ran_on = report.get("source")
    ran_side = ran_on.get("s_W_exact") if isinstance(ran_on, Mapping) else None
    view_path = directory / "view.yaml.gz"
    view: dict[str, Any] = {}
    routes: dict[str, bool] | None = None
    if "measured" in report:
        if not view_path.is_file():
            raise GridSlackError(
                f"n={n}: no {view_path.name} beside the report that decided it"
            )
        if ran_side is not None:
            own = same.exact_frame(witness).side
            if Fraction(str(ran_side)) != own:
                raise GridSlackError(
                    f"n={n}: the run read a witness at s_W = {ran_side}, and this checkout's "
                    f"is at {same.literal(own)}: run the count again on this witness"
                )
        view, routes = view_decided(n, report, view_path, witness)
        straightened = [row["square"] for row in report.get("straightened") or []]
        report = {**report, "measured": measure(n, witness, view, straightened)}
        if not report["measured"]["identity"].get("one_to_one"):
            raise GridSlackError(
                f"n={n}: the view does not pair one to one with this checkout's witness"
            )
    decision = decided(report, witness, routes)
    if decision.decision != "admit" or routes is None:
        raise GridSlackError(f"n={n}: not admitted: row {decision.row}, {decision.reason}")
    measured = report["measured"]
    ident = measured["identity"]
    shaded = measured["shades"]
    side = Fraction(str(view["side"]))
    printed = driver.source_frame(witness).side
    facts = driver.case_facts(n)
    bound = driver.verified_bound(facts)
    relation = driver.side_relation(side, printed, driver.upper_bound(facts))
    record: dict[str, Any] = {
        "n": n,
        "of_witness": witness["id"],
        "provenance": driver.packing_credit(
            facts, (witness.get("source") or {}).get("key"), relation
        ),
        "by": "project",
        "method": grid_written_method(METHOD),
        "side": "same" if relation == "same" else "solved",
    }
    # No `changes`: the register counts there the free squares a regularizer turns, and
    # the squares straightened here are any within `--near-axis-degrees` of the axes,
    # load-bearing or not; their largest turn is the identity's `max_turn_deg`.
    record["identity"] = {
        "basis": "measured",
        "measured_in": driver.LAYER_INDEX_PATH,
        "one_to_one": bool(ident["one_to_one"]),
        "moved": int(ident["moved"]),
        "max_move": float(ident["max_move"]),
        "max_turn_deg": float(ident["max_turn_deg"]),
    }
    current = shaded.get("against_current") or {}
    return driver.Admitted(
        n=n,
        generator=GENERATOR,
        run={"id": run_id, "output": "grid"},
        source={
            "witness": relative_source(n),
            "id": str(witness["id"]),
            "scalar_kind": str(witness["scalar"]["kind"]),
            "sha256": hashlib.sha256(data).hexdigest(),
        },
        side={
            "reported": str(witness["side"]),
            "view": driver.literal(side),
            "relation": relation,
            "view_minus_reported": f"{float(side - printed):.3e}" if printed else "-",
            # `s_V - U` as the driver prints it (`minus_U`), a closed form's included.
            "view_minus_verified_upper_bound": (
                f"{bound.difference(side):.3e}" if bound is not None else None
            ),
        },
        view=dict(view),
        provenance=dict(view.get("certificate") or {}),
        routes={
            "repository_verifier": routes["exact_verify"],
            "independent_checker": routes["independent"],
        },
        decision={
            "row": decision.row,
            "decision": decision.decision,
            "reason": decision.reason,
        },
        measured={
            "identity_by": f"{driver.IDENTITY_BY}, in devtools.regularize_grid_slack, again "
            "at admission against this checkout's witness",
            "shades_by": f"{driver.SHADES_BY}, in devtools.regularize_grid_slack, again at "
            "admission against this checkout's witness",
            "contacts": {
                rule: {
                    "before": list(shaded[rule]["before"]),
                    "after": list(shaded[rule]["after"]),
                }
                for rule in ("house", "stage")
            },
            "symmetry": int(ident.get("symmetry") or 0),
            "regressions": len(shaded.get("regressions") or [])
            + len(current.get("regressions") or []),
            "level": None,
            "groups": [],
            **({} if ran_side is not None else {"source_note": UNRECORDED_SIDE}),
        },
        regularization=record,
        house_after=list(shaded["house"]["after"]),
    )


def view_decided(
    n: int, report: Mapping[str, Any], path: Path, witness: Mapping[str, Any]
) -> tuple[dict[str, Any], dict[str, bool]]:
    """A run's view file (`path`) read as it is now, and the exact routes' verdicts on it,
    or GridSlackError when it is not the view its report decided (#548 review C, C1).

    `regularize_evand.decided_refusal` decides it as `layer_refusal` decides a driver
    view: the file must read as a valid rational witness, `exact_verify` and the
    independent checker must both accept it and decide it as the run recorded
    (`attempts[-1].exact.verdicts`), and its exact side and id must be the run's
    (`attempts[-1].exact.side`, and `regularized_id` of this checkout's witness, whose id
    is fixed per count). Nothing is compared by digest or Git blob id (OR-16, OR-18).
    """
    attempts = report.get("attempts") or [{}]
    exact = attempts[-1].get("exact") or {}
    verdicts = exact.get("verdicts") or {}
    try:
        document = load_yaml(gzip.decompress(path.read_bytes()).decode("utf-8"))
        validate_witness_document(document, path=path, fallback_schema=WITNESS_SCHEMA)
        view: dict[str, Any] = document["witness"]
        routes, refusal = driver.decided_refusal(
            path.name,
            view,
            recorded={
                route: bool((verdicts.get(route) or {}).get("passed"))
                for route in ("exact_verify", "independent")
            },
            decided={"side": exact.get("side"), "id": regularized_id(witness)},
        )
    except Exception as error:  # a view that does not read is refused
        message = f"n={n}: {path.name} does not read as a rational view: {error}"
        raise GridSlackError(message) from error
    if refusal is not None:
        raise GridSlackError(f"n={n}: not admitted: {refusal}")
    return view, routes


UNRECORDED_SIDE = (
    "the run's report records no exact side of the witness it read: the view is held to "
    "this checkout's witness by the measurements made again at admission"
)
"""An entry's note where the grid run predates recording the witness's exact side."""


def relative_source(n: int) -> str:
    return (KNOWN_BEST / f"n-{n:03d}.yaml").relative_to(REPO).as_posix()


def generator_block(settings: Mapping[str, Any]) -> dict[str, Any]:
    """This generator as the layer's index describes it."""
    return {
        "tool": "packing/devtools/regularize_grid_slack.py",
        "generated_by": (
            "python -m devtools.regularize_grid_slack --n N ... --run-dir DIR, admitted by "
            "python -m devtools.regularize_evand layer --grid-run DIR --grid-counts N ..."
        ),
        "method": METHOD,
        "credit": layer.EVAND_CREDIT,
        "settings": dict(settings),
    }


def run_block(run_dir: Path, run_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    """A run as the layer's index records it, and its settings: every count's decision
    by the table and the seconds its reports record. The run kept no receipt of its own
    CPU time, so the cost is those seconds, summed, at one worker a count. Reports another
    version of this generator wrote into the same directory are not this run's: they are
    counted apart, and their views are never admitted here (`admitted`).

    The run is dated by the latest time its reports record (`finished`, written by
    `run_one`), never by the files' modification times, which Git does not keep and a
    copy or a restore resets (#548 review C, C2, as B5 is for the driver). A report from
    before the time was recorded was written before any that records one, so the latest
    recorded time stands; where none records one the date is `None`, which
    `regularize_evand.dated_runs` fills from the index's own record of the run."""
    decisions: dict[str, int] = {}
    seconds = 0.0
    settings: dict[str, Any] = {}
    finished: list[str] = []
    counts = 0
    others = 0
    for path in sorted(run_dir.glob("n-*/report.json")):
        report = json.loads(path.read_text(encoding="utf-8"))
        if report.get("generator") != GENERATOR:
            others += 1
            continue
        n = int(report["n"])
        witness = load_source(n)
        word = decided(report, witness).decision
        decisions[word] = decisions.get(word, 0) + 1
        seconds += float(report.get("seconds") or 0)
        settings = dict(report.get("settings") or settings)
        if report.get("finished"):
            finished.append(str(report["finished"]))
        counts += 1
    block = {
        "id": run_id,
        "generator": GENERATOR,
        "finished": max(finished)[:10] if finished else None,
        "parameters": {**settings, **({"other_versions_left_out": others} if others else {})},
        "counts": counts,
        "decisions": dict(sorted(decisions.items())),
        "cost": {
            "cpu_seconds": round(seconds, 2),
            "wall_seconds": round(seconds, 2),
            "workers": 1,
            "note": "per-count seconds the reports record, summed; no receipt of the run's own",
        },
    }
    return block, settings


def admitted_views(
    run_dir: Path, counts: Sequence[int]
) -> tuple[list[driver.Admitted], dict[str, Any], dict[str, Any]]:
    """The views of `counts` in a finished run, each admitted by the decision table, with
    the run and this generator as the layer's index records them."""
    run_id = f"grid-slack-{run_dir.name}"
    views = [admitted(run_dir / f"n-{n:03d}", run_id) for n in counts]
    run, _settings = run_block(run_dir, run_id)
    # The generator's block keeps its defaults: runs at other thresholds are admitted
    # beside one another (owner, 13 October 2026), and each run's parameters say its own.
    return views, run, generator_block(DEFAULT_SETTINGS)


def summary(report: Mapping[str, Any]) -> str:
    n = report["n"]
    if "measured" not in report:
        return f"n={n}: no view ({report.get('refusal')}); {report['seconds']} s"
    measured = report["measured"]
    drawn = measured["drawing"]
    ident = measured["identity"]
    shaded = measured["shades"]
    return (
        f"n={n} ({report['relation']}): light {drawn['light_axis']}, uneven "
        f"{drawn['uneven_axis']} of {drawn['axis']} axis, near-axis {drawn['near_axis']}; "
        f"house {shaded['house']}, stage {shaded['stage']}; totals fall "
        f"{measured['totals_fall']}; one-to-one {ident.get('one_to_one')} max move "
        f"{ident.get('max_move')}; {report['seconds']} s"
    )


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    command.add_argument("--n", type=int, nargs="+", required=True)
    command.add_argument("--run-dir", type=Path, required=True)
    command.add_argument("--near-axis-degrees", type=float, default=NEAR_AXIS_DEGREES)
    command.add_argument("--trust", type=positive, default=TRUST)
    command.add_argument("--time-limit", type=float, default=TIME_LIMIT)
    return command


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    settings = Settings(args.near_axis_degrees, args.trust, args.time_limit)
    failed = 0
    for n in args.n:
        try:
            print(summary(run_one(n, args.run_dir, settings)), flush=True)
        except (GridSlackError, same.SameSideError) as error:
            failed += 1
            print(f"n={n}: refused: {error}", flush=True)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
